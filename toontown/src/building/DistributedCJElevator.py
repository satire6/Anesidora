import DistributedElevator
import DistributedBossElevator
from ElevatorConstants import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedCJElevator(DistributedBossElevator.DistributedBossElevator):

    def __init__(self, cr):
        DistributedBossElevator.DistributedBossElevator.__init__(self, cr)
        self.type = ELEVATOR_CJ
        self.countdownTime = ElevatorData[self.type]['countdown']

    def setupElevator(self):
        """setupElevator(self)
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        # TODO: place this on a node indexed by the entraceId
        self.elevatorModel = loader.loadModel(
            "phase_11/models/lawbotHQ/LB_Elevator")

        # The big cog icon on the top is only visible at the BossRoom.
        #icon = self.elevatorModel.find('**/big_frame/')
        #if not icon.isEmpty():
        #    icon.hide()

        self.leftDoor = self.elevatorModel.find("**/left-door")
        if self.leftDoor.isEmpty():
            self.leftDoor = self.elevatorModel.find("**/left_door")
            
        self.rightDoor = self.elevatorModel.find("**/right-door")
        if self.rightDoor.isEmpty():
            self.rightDoor = self.elevatorModel.find("**/right_door")

        geom = base.cr.playGame.hood.loader.geom
        locator = geom.find('**/elevator_locator')
        self.elevatorModel.reparentTo(locator)
        #self.elevatorModel.setH(180)

        DistributedElevator.DistributedElevator.setupElevator(self)
        
    def getDestName(self):
        return TTLocalizer.ElevatorLawBotBoss

