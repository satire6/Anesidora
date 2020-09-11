from otp.level import DistributedLevelAI, LevelSpec
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.level import LevelSpec
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals
from toontown.coghq import FactoryEntityCreatorAI, CountryClubRoomSpecs
from toontown.coghq import CountryClubRoomBase, LevelSuitPlannerAI
from toontown.coghq import DistributedCountryClubBattleAI
from toontown.suit import DistributedMintSuitAI

class DistributedCountryClubRoomAI(DistributedLevelAI.DistributedLevelAI,
                            CountryClubRoomBase.CountryClubRoomBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCountryClubRoomAI')

    def __init__(self, air, countryClubId, countryClubDoId, zoneId, roomId, roomNum, avIds,
                 battleExpAggreg):
        # pass zero for the entrance id
        DistributedLevelAI.DistributedLevelAI.__init__(self, air, zoneId,
                                                       0, avIds)
        CountryClubRoomBase.CountryClubRoomBase.__init__(self)
        self.setCountryClubId(countryClubId)
        self.countryClubId = countryClubId
        self.setRoomId(roomId)
        self.roomNum = roomNum
        self.countryClubDoId = countryClubDoId
        self.battleExpAggreg = battleExpAggreg

    def createEntityCreator(self):
        return FactoryEntityCreatorAI.FactoryEntityCreatorAI(level=self)

    def getBattleCreditMultiplier(self):
        return ToontownBattleGlobals.getCountryClubCreditMultiplier(self.countryClubId)
    
    def generate(self):
        self.notify.debug('generate %s: room=%s' % (self.doId, self.roomId))

        # create our spec
        self.notify.debug('loading spec')
        specModule = CountryClubRoomSpecs.getCountryClubRoomSpecModule(self.roomId)
        roomSpec = LevelSpec.LevelSpec(specModule)

        if __dev__:
            # create a factory EntityTypeRegistry and hand it to the spec
            self.notify.debug('creating entity type registry')
            typeReg = self.getCountryClubEntityTypeReg()
            roomSpec.setEntityTypeReg(typeReg)
        
        self.notify.debug('creating entities')
        DistributedLevelAI.DistributedLevelAI.generate(self, roomSpec)

        # TODO: convert suits into Entities
        # create the suits
        # Until they are converted to entities, it's important that
        # the suits are created in the levelZone.

        self.notify.debug('creating cogs')
        cogSpecModule = CountryClubRoomSpecs.getCogSpecModule(self.roomId)
        self.planner = LevelSuitPlannerAI.LevelSuitPlannerAI(
            self.air, self,
            DistributedMintSuitAI.DistributedMintSuitAI,
            DistributedCountryClubBattleAI.DistributedCountryClubBattleAI,
            cogSpecModule.CogData,
            cogSpecModule.ReserveCogData,
            cogSpecModule.BattleCells,
            battleExpAggreg=self.battleExpAggreg)
        suitHandles = self.planner.genSuits()
        # alert battle blockers that planner has been created
        messenger.send("plannerCreated-"+str(self.doId))
        
        self.suits = suitHandles['activeSuits']
        self.reserveSuits = suitHandles['reserveSuits']
        self.d_setSuits()

        self.notify.debug('finish mint room %s %s creation' %
                          (self.roomId, self.doId))

    def delete(self):
        self.notify.debug('delete: %s' % self.doId)
        suits = self.suits
        for reserve in self.reserveSuits:
            suits.append(reserve[0])
        self.planner.destroy()
        del self.planner
        for suit in suits:
            if not suit.isDeleted():
                suit.factoryIsGoingDown()
                suit.requestDelete()
        del self.battleExpAggreg
        DistributedLevelAI.DistributedLevelAI.delete(self, deAllocZone=False)

    # required-field getters
    def getCountryClubId(self):
        return self.countryClubId
    
    def getRoomId(self):
        # this is the id of the room in the context of the room pool
        return self.roomId

    def getRoomNum(self):
        # this is a zero-based index of the room from the start of the mint,
        # including hallways
        return self.roomNum

    def getCogLevel(self):
        # this is set on us by the FactoryLevelMgrAI
        return self.cogLevel

    def d_setSuits(self):
        self.sendUpdate('setSuits', [self.getSuits(), self.getReserveSuits()])

    def getSuits(self):
        suitIds = []
        for suit in self.suits:
            suitIds.append(suit.doId)
        return suitIds

    def getReserveSuits(self):
        suitIds = []
        for suit in self.reserveSuits:
            suitIds.append(suit[0].doId)
        return suitIds

    def d_setBossConfronted(self, toonId):
        if toonId not in self.avIdList:
            self.notify.warning(
                'd_setBossConfronted: %s not in list of participants' %
                toonId)
            return
        self.sendUpdate('setBossConfronted', [toonId])

    def setVictors(self, victorIds):
        # This is called by DistributedCountryClubBattleAI when the boss battle
        # is over and the toons won.

        activeVictors = []
        activeVictorIds = []
        for victorId in victorIds:
            toon = self.air.doId2do.get(victorId)
            if toon is not None:
                activeVictors.append(toon)
                activeVictorIds.append(victorId)

        # log that toons beat the mint
        description = '%s|%s' % (self.countryClubId, activeVictorIds)
        for avId in activeVictorIds:
            self.air.writeServerEvent('mintDefeated', avId, description)

    # call this when the mint boss has been defeated and we're ready
    # for the toons to leave
    # when all toons have left, we'll be deleted
    def b_setDefeated(self):
        self.d_setDefeated()
        self.setDefeated()
    def d_setDefeated(self):
        self.sendUpdate('setDefeated')
    def setDefeated(self):
        # we add parts in the battle ai now...
        pass

    def allToonsGone(self, toonsThatCleared):
        DistributedLevelAI.DistributedLevelAI.allToonsGone(self,
                                                           toonsThatCleared)
        if self.roomNum == 0:
            # only have the first room notify the mint itself
            mint = simbase.air.doId2do.get(self.countryClubDoId)
            if mint is not None:
                mint.allToonsGone()
            else:
                self.notify.warning('no mint %s in allToonsGone' %
                                    self.countryClubDoId)
    def challengeDefeated(self):
        """Handle the challenge is this room being defeated by the toons."""
        countryClub = simbase.air.doId2do.get(self.countryClubDoId)
        if countryClub:
            countryClub.roomDefeated(self)

