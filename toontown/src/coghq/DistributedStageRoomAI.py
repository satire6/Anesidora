from otp.level import DistributedLevelAI, LevelSpec
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.level import LevelSpec
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals
from toontown.coghq import FactoryEntityCreatorAI, StageRoomSpecs
from toontown.coghq import StageRoomBase, LevelSuitPlannerAI
from toontown.coghq import DistributedStageBattleAI
from toontown.suit import DistributedStageSuitAI

class DistributedStageRoomAI(DistributedLevelAI.DistributedLevelAI,
                            StageRoomBase.StageRoomBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStageRoomAI')

    def __init__(self, air, stageId, stageDoId, zoneId, roomId, roomNum, avIds,
                 battleExpAggreg):
        # pass zero for the entrance id
        DistributedLevelAI.DistributedLevelAI.__init__(self, air, zoneId,
                                                       0, avIds)
        StageRoomBase.StageRoomBase.__init__(self)
        self.setStageId(stageId)
        self.setRoomId(roomId)
        self.roomNum = roomNum
        self.stageDoId = stageDoId
        self.battleExpAggreg = battleExpAggreg

    def createEntityCreator(self):
        return FactoryEntityCreatorAI.FactoryEntityCreatorAI(level=self)

    def getBattleCreditMultiplier(self):
        return ToontownBattleGlobals.getStageCreditMultiplier(self.getFloorNum())

    def getFloorNum(self):
        stage = self.air.getDo(self.stageDoId)
        if stage is None:
            self.notify.warning('getFloorNum: could not find stage %s' % self.stageDoId)
            return 0
        return stage.floorNum
    
    def generate(self):
        self.notify.debug('generate %s: room=%s' % (self.doId, self.roomId))

        # create our spec
        self.notify.debug('loading spec')
        specModule = StageRoomSpecs.getStageRoomSpecModule(self.roomId)
        roomSpec = LevelSpec.LevelSpec(specModule)

        if __dev__:
            # create a factory EntityTypeRegistry and hand it to the spec
            self.notify.debug('creating entity type registry')
            typeReg = self.getStageEntityTypeReg()
            roomSpec.setEntityTypeReg(typeReg)
        
        self.notify.debug('creating entities')
        DistributedLevelAI.DistributedLevelAI.generate(self, roomSpec)

        # TODO: convert suits into Entities
        # create the suits
        # Until they are converted to entities, it's important that
        # the suits are created in the levelZone.

        self.notify.debug('creating cogs')
        cogSpecModule = StageRoomSpecs.getCogSpecModule(self.roomId)
        self.planner = LevelSuitPlannerAI.LevelSuitPlannerAI(
            self.air, self,
            DistributedStageSuitAI.DistributedStageSuitAI,
            DistributedStageBattleAI.DistributedStageBattleAI,
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

        self.notify.debug('finish stage room %s %s creation' %
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
    def getStageId(self):
        return self.stageId
    
    def getRoomId(self):
        # this is the id of the room in the context of the room pool
        return self.roomId

    def getRoomNum(self):
        # this is a zero-based index of the room from the start of the stage,
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
        # This is called by DistributedStageBattleAI when the boss battle
        # is over and the toons won.

        activeVictors = []
        activeVictorIds = []
        for victorId in victorIds:
            toon = self.air.doId2do.get(victorId)
            if toon is not None:
                activeVictors.append(toon)
                activeVictorIds.append(victorId)

        # log that toons beat the stage
        description = '%s|%s' % (self.stageId, activeVictorIds)
        for avId in activeVictorIds:
            self.air.writeServerEvent('stageDefeated', avId, description)

        for toon in activeVictors:
            # update toon's quests
            simbase.air.questManager.toonDefeatedStage(
                toon, self.stageId, activeVictors)

    # call this when the stage boss has been defeated and we're ready
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
            # only have the first room notify the stage itself
            stage = simbase.air.doId2do.get(self.stageDoId)
            if stage is not None:
                stage.allToonsGone()
            else:
                self.notify.warning('no stage %s in allToonsGone' %
                                    self.stageDoId)
