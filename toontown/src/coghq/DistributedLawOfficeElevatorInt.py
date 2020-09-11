from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevatorFloor
from toontown.building import DistributedElevator
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer

class DistributedLawOfficeElevatorInt(DistributedElevatorFloor.DistributedElevatorFloor):

    def __init__(self, cr):
        DistributedElevatorFloor.DistributedElevatorFloor.__init__(self, cr)
        

    def generate(self):
        DistributedElevator.DistributedElevator.generate(self)
        self.accept("LawOffice_Spec_Loaded", self.__placeElevator)

    def delete(self):
        self.elevatorModel.removeNode()
        del self.elevatorModel
        DistributedElevatorFloor.DistributedElevatorFloor.delete(self)
        self.ignore("LawOffice_Spec_Loaded")

    def setEntranceId(self, entranceId):
        self.entranceId = entranceId

        # These hard coded poshprs should be replaced with nodes in the model
        if self.entranceId == 0:
            # Front of the factory (south entrance)
            self.elevatorModel.setPosHpr(62.74, -85.31, 0.00, 2.00, 0.00, 0.00)
        elif self.entranceId == 1:
            # Side of the factory (west entrance)
            self.elevatorModel.setPosHpr(-162.25, 26.43, 0.00, 269.00, 0.00, 0.00)
        else:
            self.notify.error("Invalid entranceId: %s" % entranceId)

    def setupElevator(self):
        """setupElevator(self)
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        # TODO: place this on a node indexed by the entraceId
        self.elevatorModel = loader.loadModel("phase_4/models/modules/elevator")
        self.elevatorModel.reparentTo(render)
        self.elevatorModel.setScale(1.05)
        self.leftDoor = self.elevatorModel.find("**/left-door")
        self.rightDoor = self.elevatorModel.find("**/right-door")
        # No lights on this elevator
        self.elevatorModel.find("**/light_panel").removeNode()
        self.elevatorModel.find("**/light_panel_frame").removeNode()
        DistributedElevatorFloor.DistributedElevatorFloor.setupElevator(self)
        #DistributedElevatorFloor.DistributedElevatorFloor.setupElevator(self)
        


            
    def __placeElevator(self):
        self.notify.debug("PLACING ELEVATOR FOOL!!")
        if self.isEntering:
            elevatorNode = render.find("**/elevator_origin")
            if not elevatorNode.isEmpty():
                self.elevatorModel.setPos(0,0, 0)
                self.elevatorModel.reparentTo(elevatorNode)
            else:
                #explode
                self.notify.debug("NO NODE elevator_origin!!")
        else:
            elevatorNode = render.find("**/SlidingDoor")
            if not elevatorNode.isEmpty():
                self.elevatorModel.setPos(0,0,-15)
                self.elevatorModel.reparentTo(elevatorNode)
            else:
                #explode
                self.notify.debug("NO NODE SlidingDoor!!")
        
        
        
    
            

    def getElevatorModel(self):
        return self.elevatorModel

    def setBldgDoId(self, bldgDoId):
        # The doId is junk, there is no building object for the factory
        # exterior elevators. Do the appropriate things that
        # DistributedElevator.gotBldg does.
        self.bldg = None
        self.setupElevator()

    def getZoneId(self):
        return 0

    def __doorsClosed(self, zoneId):
        return

    def setLawOfficeInteriorZone(self, zoneId):
        if (self.localToonOnBoard):
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : 'factoryInterior', #should be lawOffice
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'hoodId' : hoodId,
                }
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)
