from otp.level import DistributedLevelAI
from direct.directnotify import DirectNotifyGlobal
import cPickle
import LevelSuitPlannerAI
import LawOfficeBase
from direct.task import Task
import FactoryEntityCreatorAI
import FactorySpecs
from otp.level import LevelSpec
import CogDisguiseGlobals
from toontown.suit import DistributedFactorySuitAI
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals
from toontown.coghq import DistributedBattleFactoryAI
from toontown.coghq import LawOfficeLayout
from toontown.coghq import DistributedLawOfficeElevatorIntAI
from direct.distributed import DistributedObjectAI
from toontown.ai.ToonBarrier import *



class DistributedLawOfficeFloorAI(DistributedLevelAI.DistributedLevelAI, LawOfficeBase.LawOfficeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawOfficeAI')

    def __init__(self, air, lawOfficeId, zoneId, entranceId, avIds, spec):
        # entranceId is the entrance the toons will come in (based on
        # the elevator they got in)
        DistributedLevelAI.DistributedLevelAI.__init__(self, air, zoneId,
                                                       entranceId, avIds)
        LawOfficeBase.LawOfficeBase.__init__(self)
        self.setLawOfficeId(lawOfficeId)
        self.layout = None
        self.elevator = None
        self.level = None
        self.spec = spec

    def createEntityCreator(self):
        return FactoryEntityCreatorAI.FactoryEntityCreatorAI(level=self)

    def getBattleCreditMultiplier(self):
        return ToontownBattleGlobals.getFactoryCreditMultiplier(self.lawOfficeId)
    
    def generate(self):
        self.notify.info('generate')

        self.notify.info('start factory %s %s creation, frame=%s' %
                         (self.lawOfficeId, self.doId,
                          globalClock.getFrameCount()))
                          
        self.layout = LawOfficeLayout.LawOfficeLayout(self.lawOfficeId)
        
        self.startFloor()
        
    def startFloor(self):

        if __debug__:
            simbase.factory = self

        # create our spec
        self.notify.info('loading spec')
        self.factorySpec = LevelSpec.LevelSpec(self.spec)

        if __dev__:
            # create a factory EntityTypeRegistry and hand it to the spec
            self.notify.info('creating entity type registry')
            typeReg = self.getEntityTypeReg()
            self.factorySpec.setEntityTypeReg(typeReg)
        
        self.notify.info('creating entities')
        DistributedLevelAI.DistributedLevelAI.generate(self, self.factorySpec)
        

        self.notify.info('creating cogs')
        cogSpecModule = FactorySpecs.getCogSpecModule(self.lawOfficeId)
        self.planner = LevelSuitPlannerAI.LevelSuitPlannerAI(
            self.air, self,
            DistributedFactorySuitAI.DistributedFactorySuitAI,
            DistributedBattleFactoryAI.DistributedBattleFactoryAI,
            cogSpecModule.CogData,
            cogSpecModule.ReserveCogData,
            cogSpecModule.BattleCells)
        suitHandles = self.planner.genSuits()
        # alert battle blockers that planner has been created
        messenger.send("plannerCreated-"+str(self.doId))
        
        self.suits = suitHandles['activeSuits']
        self.reserveSuits = suitHandles['reserveSuits']
        self.d_setSuits()

        # log that toons entered the factory
        scenario = 0 # placeholder until we have real scenarios
        description = '%s|%s|%s|%s' % (
            self.lawOfficeId, self.entranceId, scenario, self.avIdList)
        for avId in self.avIdList:
            self.air.writeServerEvent('DAOffice Entered', avId, description)

        self.notify.info('finish factory %s %s creation' %
                         (self.lawOfficeId, self.doId))

    def delete(self):
        self.notify.info('delete: %s' % self.doId)
        suits = self.suits
        for reserve in self.reserveSuits:
            suits.append(reserve[0])
        self.planner.destroy()
        del self.planner
        for suit in suits:
            if not suit.isDeleted():
                suit.factoryIsGoingDown()
                suit.requestDelete()
        DistributedLevelAI.DistributedLevelAI.delete(self, False)
        
        #self.notify.debug('delete')
        #if __dev__:
        #    self.removeAutosaveTask()
        #self.destroyLevel()
        #self.ignoreAll()
        #if 0:
        #    self.air.deallocateZone(self.zoneId)
        #DistributedObjectAI.DistributedObjectAI.delete(self)
    
        
    def readyForNextFloor(self):
        toonId = self.air.getAvatarIdFromSender()
        self.__barrier.clear(toonId)
        
    def dumpEveryone(self):
        pass

    def getTaskZoneId(self):
        return self.lawOfficeId

    # required-field getters
    def getLawOfficeId(self):
        return self.lawOfficeId

    def d_setForemanConfronted(self, avId):
        # avatar 'avId' has confronted the factory foreman
        if avId in self.avIdList:
            self.sendUpdate('setForemanConfronted', [avId])
        else:
            self.notify.warning(
                '%s: d_setForemanConfronted: av %s not in av list %s' %
                (self.doId, avId, self.avIdList))

    def setVictors(self, victorIds):
        # This is called by DistributedBattleFactoryAI when the boss battle
        # is over and the toons won.

        activeVictors = []
        activeVictorIds = []
        for victorId in victorIds:
            toon = self.air.doId2do.get(victorId)
            if toon is not None:
                activeVictors.append(toon)
                activeVictorIds.append(victorId)

        # log that toons beat the factory
        scenario = 0 # placeholder until we have real scenarios
        description = '%s|%s|%s|%s' % (
            self.lawOfficeId, self.entranceId, scenario, activeVictorIds)
        for avId in activeVictorIds:
            self.air.writeServerEvent('DAOffice Defeated', avId, description)
            
        for toon in activeVictors:
            # update toon's quests
            # WE ASSUME THAT self.lawOfficeId IS THE 'FAUX-ZONE' OF THE FACTORY
            simbase.air.questManager.toonDefeatedFactory(
                toon, self.lawOfficeId, activeVictors)

        # this causes the toons to leave in the middle of the reward movie
        # see DistributedBattleFactoryAI.enterResume
        #self.b_setDefeated()

    # call this when the factory boss has been defeated and we're ready
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
