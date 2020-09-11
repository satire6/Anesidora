from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorFloorAI
from toontown.building import DistributedElevatorAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task

class DistributedLawOfficeElevatorIntAI(DistributedElevatorFloorAI.DistributedElevatorFloorAI):

    def __init__(self, air, lawOfficeId, bldg, avIds):
        DistributedElevatorFloorAI.DistributedElevatorFloorAI.__init__(self, air, bldg, avIds)
        self.lawOfficeId = lawOfficeId

        
    def getEntranceId(self):
        return self.entranceId

    def elevatorClosed(self):
        #print("ELEVATOR CLOSED DOING CALCS")
        numPlayers = self.countFullSeats()
        #print(" NUMBER OF PLAYERS IS %s" % (numPlayers))
        # It is possible the players exited the district
        if (numPlayers > 0):
            
            # Create a factory interior just for us

            # Make a nice list for the factory
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            #lawOfficeZone = self.bldg.createLawOffice(self.lawOfficeId,
            #                                      self.entranceId, players)
            
            sittingAvIds = [];
            
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    # Tell each player on the elevator that they should enter the factory
                    # And which zone it is in
                    #self.sendUpdateToAvatarId(avId, "setLawOfficeInteriorZone", [lawOfficeZone])
                    # Clear the fill slot
                    #self.clearFullNow(seatIndex)
                    sittingAvIds.append(avId)
                    pass
            for avId in self.avIds:
                if not avId in sittingAvIds:
                    print("THIS AV ID %s IS NOT ON BOARD" % (avId))
                    
            self.bldg.startNextFloor()                    
            
        else:
            self.notify.warning("The elevator left, but was empty.")
        self.fsm.request("closed")

    def enterClosed(self):
        print("DistributedLawOfficeElevatorIntAI.elevatorClosed %s" % (self.doId))
        #import pdb; pdb.set_trace()
        DistributedElevatorFloorAI.DistributedElevatorFloorAI.enterClosed(self)
        # Switch back into opening mode since we allow other Toons onboard
        if (not self.hasOpenedLocked) or (not self.isLocked):
            self.fsm.request("opening")
            if self.isLocked:
                self.hasOpenedLocked = 1
        





