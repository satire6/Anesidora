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
from toontown.coghq import DistributedLawOfficeFloorAI
from toontown.coghq import LawOfficeLayout
from toontown.coghq import DistributedLawOfficeElevatorIntAI
from toontown.building import DistributedElevatorFloorAI
from toontown.ai.ToonBarrier import *
from direct.distributed.DistributedObjectAI import *
from direct.showbase import PythonUtil

#DistributedLevelAI.DistributedLevelAI

class DistributedLawOfficeAI(DistributedObjectAI, LawOfficeBase.LawOfficeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawOfficeAI')

    def __init__(self, air, lawOfficeId, zoneId, entranceId, avIds):
        # entranceId is the entrance the toons will come in (based on
        # the elevator they got in)
        #DistributedLevelAI.DistributedLevelAI.__init__(self, air, zoneId,
        #                                               entranceId, avIds)
        DistributedObjectAI.__init__(self, air)
        LawOfficeBase.LawOfficeBase.__init__(self)
        self.setLawOfficeId(lawOfficeId)
        self.layout = None
        self.currentFloor = 0
        self.elevator = None
        self.elevatorB = None
        self.activeElevator = 0
        self.level = None
        self.avIds = avIds
        self.entranceId = entranceId
        
        

    def createEntityCreator(self):
        return FactoryEntityCreatorAI.FactoryEntityCreatorAI(level=self)

    def getBattleCreditMultiplier(self):
        return ToontownBattleGlobals.getFactoryCreditMultiplier(self.lawOfficeId)
    
    def generate(self):
        self.notify.info('generate')

        self.notify.info('start factory %s %s creation, frame=%s' %
                         (self.lawOfficeId, self.doId,
                          globalClock.getFrameCount()))
        
        DistributedObjectAI.generate(self)        
        self.layout = LawOfficeLayout.LawOfficeLayout(self.lawOfficeId)
        
        self.exitEvents = {}
        for avId in self.avIds:
            self.exitEvents[avId] = simbase.air.getAvatarExitEvent(avId)
            self.accept(self.exitEvents[avId], Functor(self.handleAvatarExit, avId))
        
        self.startOffice()
        
    def handleAvatarExit(self, toonId):
        #print("received handleAvatarExit from %s" % (toonId))
        #self.__barrier.clear(toonId)
        #self.avIds.remove(toonId)
        pass
        
    def readyForNextFloor(self):
        toonId = self.air.getAvatarIdFromSender()
        #self.__barrier.clear(toonId)
        #print("received ready for next floor from %s" % (toonId))
        pass
        
       # for avId in list(self.avIds):
        #    av = self.air.doId2do.get(avId)
        #    print("AvID %s Zone %s AvZone %s" % (avId, self.zoneId, av.zoneId))
         #   if not av and avId != toonId:
         #       self.notify.warning("some toon left the district and we didn't hear about it %s" % (avId))
         #       self.handleAvatarExit(toonId)
        #    elif av.zoneId != self.zoneId and avId != toonId:
         #       self.handleAvatarExit(toonId)
            
        
        
    def generateWithRequired(self, zone):
        DistributedObjectAI.generateWithRequired(self, zone)    
        
        
    def startOffice(self):
        #print("LOADING FIRST FLOOR!!!!! %s" % (self.currentFloor))

        # create our first floor
        self.notify.info('loading spec')
        specModule = self.layout.getFloorSpec(self.currentFloor)
        self.level = DistributedLawOfficeFloorAI.DistributedLawOfficeFloorAI(self.air, self.lawOfficeId, self.zoneId, self.entranceId, self.avIds, specModule)
        self.level.setLevelSpec(LevelSpec.LevelSpec(specModule))
        #self.currentFloorZone = self.air.allocateZone()

        self.notify.info('creating entities')
        self.level.generateWithRequired(self.zoneId)
        
        #print("STARTING TOONBARRIER FOR %s" % (self.avIds))
        #self.__barrier = ToonBarrier(
        #    'waitClientsFinishFloor',
        #    self.uniqueName('waitClientsFinishFloor'),
        #    self.avIds, 10000,
        #    self.startNextFloor, self.dumpEveryone)
        
        #Start: Add the connecting elevator--------------------
        
        
        #print("START SETTING UP ELEVATORS!!!")
        self.elevator = DistributedElevatorFloorAI.DistributedElevatorFloorAI(self.air, self.doId, self, self.avIds)
        #self.elevator.setLocked(0)
        self.elevator.setEntering(0)
        self.elevator.generateWithRequired(self.zoneId)
        self.elevatorB = DistributedElevatorFloorAI.DistributedElevatorFloorAI(self.air, self.doId, self, self.avIds)
        #self.elevatorB.setLocked(0)
        self.elevatorB.setEntering(1)
        self.elevatorB.generateWithRequired(self.zoneId)
        #self.unlockElevator()
        #self.elevator.unlock()
        #self.elevatorB.unlock()
        self.exchangeElevators()
        #print("END SETTING UP ELEVATORS!!!")
        

    def delete(self):
        self.notify.info('delete: %s' % self.doId)
        if self.elevator:
            del self.elevator
        if self.level:
            self.level.requestDelete()
            self.level = None
        self.ignoreAll()
        
    
    def exchangeElevators(self):
        if self.activeElevator == 0:
            self.elevator.lock()
            self.elevatorB.unlock()
            self.activeElevator = 1
        else:
            self.elevator.unlock()
            self.elevatorB.lock()
            self.activeElevator = 0
        
        
        
    def startNextFloor(self):
        #print("LOADING NEXT FLOOR!!!!! %s" % (self.currentFloor + 1))
        #print self.layout.floorIds
        
        if self.avIds:
            print self.avIds
            self.currentFloor +=1
            specModule = self.layout.getFloorSpec(self.currentFloor)
            
            #self.currentFloorZone = self.air.allocateZone()
            self.level.requestDelete()
            
            self.level = DistributedLawOfficeFloorAI.DistributedLawOfficeFloorAI(self.air, self.lawOfficeId, self.zoneId, self.entranceId, self.avIds, specModule)
            self.level.setLevelSpec(LevelSpec.LevelSpec(specModule))
            self.level.generateWithRequired(self.zoneId)
            
            print("exchanging elevators")
            self.exchangeElevators()
            self.startSignal()
            
    def startSignal(self):
        self.sendUpdate('startSignal')
    
    def dumpEveryone(self, optArg = None):
        pass

    def getTaskZoneId(self):
        return self.lawOfficeId

    # required-field getters
    def getLawOfficeId(self):
        return self.lawOfficeId


    def getCogLevel(self):
        # this is set on us by the FactoryLevelMgrAI
        return self.level.cogLevel

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
