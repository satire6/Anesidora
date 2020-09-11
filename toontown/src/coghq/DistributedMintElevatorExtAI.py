from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorExtAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
import CogDisguiseGlobals

class DistributedMintElevatorExtAI(DistributedElevatorExtAI.DistributedElevatorExtAI):
    def __init__(self, air, bldg, mintId, antiShuffle = 0, minLaff = 0):
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg, antiShuffle = antiShuffle, minLaff = minLaff)
        self.mintId = mintId
        self.cogDept = ToontownGlobals.cogHQZoneId2deptIndex(self.mintId)
        self.type = ELEVATOR_MINT
        self.countdownTime = ElevatorData[self.type]['countdown']

    def getMintId(self):
        return self.mintId

    def avIsOKToBoard(self, av):
        if not DistributedElevatorExtAI.DistributedElevatorExtAI.avIsOKToBoard(self, av):
            return False

        # At the moment, the design is that a mint elevator should be
        # open to all who want to board.  It was proposed at one point
        # that the mint elevator should be restricted only to those
        # who have a full cog suit, but we have decided not to do
        # that; if we change our minds and decide to lock out the
        # un-"suit"-able after all, move the comment marks below.
        # see also: DistributedMintElevatorExt.rejectBoard

        return True
        #parts = av.getCogParts()
        #return CogDisguiseGlobals.isSuitComplete(parts, self.cogDept)
    
    def elevatorClosed(self):
        numPlayers = self.countFullSeats()

        # It is possible the players exited the district
        if (numPlayers > 0):
            # Create a mint interior just for us

            # Make a nice list for the mint
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            mintZone = self.bldg.createMint(self.mintId, players)
            
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    # Tell each player on the elevator that they should
                    # enter the mint, and which zone it is in
                    self.sendUpdateToAvatarId(avId, "setMintInteriorZone",
                                              [mintZone])
                    # Clear the fill slot
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning("The elevator left, but was empty.")
        self.fsm.request("closed")

    def enterClosed(self):
        DistributedElevatorExtAI.DistributedElevatorExtAI.enterClosed(self)
        # Switch back into opening mode since we allow other Toons onboard
        self.fsm.request('opening')
        
    def sendAvatarsToDestination(self, avIdList):
        if (len(avIdList) > 0):
            mintZone = self.bldg.createMint(self.mintId, avIdList)
            for avId in avIdList:
                if avId:
                    # Tell each player on the elevator that they should enter 
                    # the factory
                    # And which zone it is in
                    self.sendUpdateToAvatarId(avId, 'setMintInteriorZoneForce', 
                                        [mintZone])



