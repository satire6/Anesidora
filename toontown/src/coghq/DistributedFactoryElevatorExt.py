from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevatorExt
from toontown.building import DistributedElevator
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer

class DistributedFactoryElevatorExt(DistributedElevatorExt.DistributedElevatorExt):

    def __init__(self, cr):
        DistributedElevatorExt.DistributedElevatorExt.__init__(self, cr)

    def generate(self):
        DistributedElevatorExt.DistributedElevatorExt.generate(self)

    def delete(self):
        self.elevatorModel.removeNode()
        del self.elevatorModel
        DistributedElevatorExt.DistributedElevatorExt.delete(self)

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
        DistributedElevator.DistributedElevator.setupElevator(self)

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

    def setFactoryInteriorZone(self, zoneId):
        if (self.localToonOnBoard):
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : 'factoryInterior',
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'hoodId' : hoodId,
                }
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)
            
    def setFactoryInteriorZoneForce(self, zoneId):
        place = self.cr.playGame.getPlace()
        if place:
            place.fsm.request("elevator", [self, 1])
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : 'factoryInterior',
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'hoodId' : hoodId,
                }
            if hasattr(place, 'elevator') and place.elevator:
                place.elevator.signalDone(doneStatus)
            else:
                self.notify.warning("setMintInteriorZoneForce: Couldn't find playGame.getPlace().elevator, zoneId: %s" %zoneId)
        else:
            self.notify.warning("setFactoryInteriorZoneForce: Couldn't find playGame.getPlace(), zoneId: %s" %zoneId)
            
    def getDestName(self):
        if self.entranceId == 0:
            return TTLocalizer.ElevatorSellBotFactory0
        elif self.entranceId == 1:
            return TTLocalizer.ElevatorSellBotFactory1

