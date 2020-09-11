from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from toontown.building.ElevatorConstants import *
from toontown.building import DistributedElevatorExtAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task

class DistributedLawOfficeElevatorExtAI(DistributedElevatorExtAI.DistributedElevatorExtAI):

    def __init__(self, air, bldg, lawOfficeId, entranceId, antiShuffle = 0, minLaff = 0):
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg, antiShuffle = antiShuffle, minLaff = minLaff)
        self.lawOfficeId = lawOfficeId
        self.entranceId = entranceId

    def getEntranceId(self):
        return self.entranceId

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()

        # It is possible the players exited the district
        if (numPlayers > 0):
            # Create a factory interior just for us

            # Make a nice list for the factory
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            lawOfficeZone = self.bldg.createLawOffice(self.lawOfficeId,
                                                  self.entranceId, players)
            
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    # Tell each player on the elevator that they should enter the factory
                    # And which zone it is in
                    self.sendUpdateToAvatarId(avId, "setLawOfficeInteriorZone", [lawOfficeZone])
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
            officeZone = self.bldg.createLawOffice(self.lawOfficeId, self.entranceId, avIdList)
            for avId in avIdList:
                if avId:
                    # Tell each player on the elevator that they should enter 
                    # the factory
                    # And which zone it is in
                    self.sendUpdateToAvatarId(avId, 'setLawOfficeInteriorZoneForce', 
                                        [officeZone])



