from direct.directnotify import DirectNotifyGlobal
from toontown.safezone import DistributedGolfKartAI
from toontown.building import DistributedElevatorExtAI
from toontown.building import ElevatorConstants
from toontown.toonbase import ToontownGlobals

class DistributedCogKartAI( DistributedElevatorExtAI.DistributedElevatorExtAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogKartAI")

    def __init__(self, air, index, x, y, z, h, p, r, bldg, minLaff):
        """__init__(air)
        """
        self.posHpr = (x, y ,z, h, p, r)        
        DistributedElevatorExtAI.DistributedElevatorExtAI.__init__(self, air, bldg, minLaff=minLaff)
        self.type = ElevatorConstants.ELEVATOR_COUNTRY_CLUB
        self.courseIndex = index
        if self.courseIndex == 0:
            self.countryClubId = ToontownGlobals.BossbotCountryClubIntA
        elif self.courseIndex == 1:
            self.countryClubId = ToontownGlobals.BossbotCountryClubIntB
        elif self.courseIndex == 2:
            self.countryClubId = ToontownGlobals.BossbotCountryClubIntC
        else:
            self.countryClubId = 12500
        
    def getPosHpr(self):
        return self.posHpr

    def elevatorClosed(self):
        numPlayers = self.countFullSeats()
        # It is possible the players exited the district
        if (numPlayers > 0):
            # Create a countryClub interior just for us

            # Make a nice list for the countryClub
            players = []
            for i in self.seats:
                if i not in [None, 0]:
                    players.append(i)
            countryClubZone = self.bldg.createCountryClub(self.countryClubId, players)
            
            for seatIndex in range(len(self.seats)):
                avId = self.seats[seatIndex]
                if avId:
                    # Tell each player on the elevator that they should
                    # enter the countryClub, and which zone it is in
                    self.sendUpdateToAvatarId(avId, "setCountryClubInteriorZone",
                                              [countryClubZone])
                    # Clear the fill slot
                    self.clearFullNow(seatIndex)
        else:
            self.notify.warning("The elevator left, but was empty.")
        
        self.fsm.request("closed")
        
        
    def sendAvatarsToDestination(self, avIdList):
        if (len(avIdList) > 0):
            countryClubZone = self.bldg.createCountryClub(self.countryClubId, avIdList)
            for avId in avIdList:
                if avId:
                    # Tell each player on the elevator that they should enter 
                    # the factory
                    # And which zone it is in
                    self.sendUpdateToAvatarId(avId, 'setCountryClubInteriorZoneForce', 
                                        [countryClubZone])

    def getCountryClubId(self):
        """Return the countryClub Id."""
        return self.countryClubId

    def enterClosed(self):
        DistributedElevatorExtAI.DistributedElevatorExtAI.enterClosed(self)
        # Switch back into opening mode since we allow other Toons onboard
        self.fsm.request('opening')
