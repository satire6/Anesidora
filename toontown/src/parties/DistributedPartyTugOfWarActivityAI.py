#-------------------------------------------------------------------------------
# Contact: Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: AI control of tug of war activity in a party.
# Changes:
# - Nov 2009 Migrated to DistributedPartyTeamActivityAI
#-------------------------------------------------------------------------------
from toontown.toonbase import ToontownGlobals
from DistributedPartyTeamActivityAI import DistributedPartyTeamActivityAI
import PartyGlobals

class DistributedPartyTugOfWarActivityAI(DistributedPartyTeamActivityAI):
    notify = directNotify.newCategory("DistributedPartyTugOfWarActivityAI")
    
    MaxAbsGlobalOffset = 32
    
    def __init__(self, air, partyDoId, x, y, h):
        DistributedPartyTeamActivityAI.__init__(
            self,
            air, partyDoId, x, y, h,
            PartyGlobals.ActivityIds.PartyTugOfWar,
            minPlayersPerTeam = PartyGlobals.TugOfWarMinimumPlayersPerTeam,
            maxPlayersPerTeam = PartyGlobals.TugOfWarMaximumPlayersPerTeam,
            duration = PartyGlobals.TugOfWarDuration,
            conclusionDuration = PartyGlobals.TugOfWarConclusionDuration,
            startDelay = PartyGlobals.TugOfWarStartDelay,
            calcAdvantage = True,
        )
        self.notify.debug("__init__")
        
        # Add up all the players forces for each side as soon as we get a
        # keyRate update from all players.  
        self.forceDictList = [
            {}, # left team's forces, indexed by toonId 
            {}, # right team's forces, indexed by toonId
        ]
        self.toonIdsToKeyRates = {}
        self.numToonsReported = 0

        self.globalOffset = 0.0 # how far the toons have moved from their initial position

        # Variables for determining the outcome of the game. If
        # endedWithFall=True that means someone actually fell in the water.
        self.endedWithFall = False
        self.losingTeam = PartyGlobals.TeamActivityNeitherTeam
        
        # Override because this code was migrated into the base class
        # And it was written assuming that it was 1v1
        if self._allowSinglePlayer:
            self.notify.warning("This team activity doesn't work party-team-activity-single-player config." +
                " This activity will ignore the config instead.")
            self._allowSinglePlayer = False  

    
    # airecv clsend
    def toonReady(self):
        """
        Clients call this over the wire when they are done reading the rules
        and are ready to play the activity.
        """
        if DistributedPartyTeamActivityAI.toonReady(self):
            senderId = self.air.getAvatarIdFromSender()
            self.forceDictList[self.getTeam(senderId)][senderId] = 0.0
    
    
    def startWaitClientsReady(self):
        self.globalOffset = 0.0
        self.forceDictList = [{}, {}]
        
        DistributedPartyTeamActivityAI.startWaitClientsReady(self)
        
    
    def startActive(self):
        # reset game variables
        self.toonIdsToKeyRates.clear()
        self.numToonsReported = 0
        self.losingTeam = PartyGlobals.TeamActivityNeitherTeam
        self.endedWithFall = False
        
        DistributedPartyTeamActivityAI.startActive(self)

        
    # clsend airecv
    def reportKeyRateForce(self, keyRate, force):
        toonId = self.air.getAvatarIdFromSender()
        self.toonIdsToKeyRates[toonId] = keyRate
        # sometimes the game has cleaned up and we get an old update from a client
        if self.toonIdsToTeams.has_key(toonId):
            self.forceDictList[self.toonIdsToTeams[toonId]][toonId] = force
    
            # send the keyrate for this toonId to the clients so they can update
            # the toon's animation (pulling or not)
            self.sendUpdate("updateToonKeyRate", [toonId, keyRate])
    
            # send the current position to the clients if we have gotten all the clients forces
            self.numToonsReported += 1
            if self.numToonsReported == self.getNumToonsPlaying():
                self.numToonsReported = 0
                self.calculateOffset()
                self.sendUpdate("updateToonPositions", [self.globalOffset])
    
    
    def calculateOffset(self):
        # This function totals the forces on each side of the water.  Then the difference
        # deltaF, between these forces is computed.  This is multiplied by a constant, kMovement,
        # to determine what the deltaX should be - i.e. how much the toons on each side should
        # move as a result of one side applying more force than the other.
        
        forceTotals = [0.0, 0.0] # left team force, right team force
        # total up all the toon forces on each side
        for teamIndex in [0,1]:
            for x in self.forceDictList[teamIndex].values():
                forceTotals[teamIndex] += x
            
        deltaF = forceTotals[1] - forceTotals[0]
        deltaX = deltaF * PartyGlobals.TugOfWarMovementFactor
        
        self.globalOffset += deltaX
        
        # make sure we don't move too far
        if self.globalOffset > self.MaxAbsGlobalOffset:
            self.globalOffset = self.MaxAbsGlobalOffset
        elif self.globalOffset < -self.MaxAbsGlobalOffset:
            self.globalOffset = -self.MaxAbsGlobalOffset

    
    def reportFallIn(self, losingTeam):
        self.notify.debug("reportFallIn( losingTeam=%s )" % PartyGlobals.TeamActivityTeams.getString(losingTeam))
        
        if losingTeam not in PartyGlobals.TeamActivityTeams:
            self.notify.warning("Got an invalid losingTeam value %d" %losingTeam)
            return
        
        # if the losing team has already been reported and this report doesn't match
        if (self.losingTeam != PartyGlobals.TeamActivityNeitherTeam) and (losingTeam != self.losingTeam):
            self.notify.warning("Report of %s as the losingTeam doesn't match previously reported value. Ignoring." %PartyGlobals.TeamActivityTeams.getString(losingTeam))
            return
        
        curState = self.activityFSM.getCurrentOrNextState()
        if curState != "Active":
            # probably late report
            # must be in active state to go to conclusion
            self.notify.warning("got reportFallIn but state is %s, ignoring" % curState)
            return
        
        self.losingTeam = losingTeam
        
        if not self.endedWithFall:
            self.endedWithFall = True
            self.activityFSM.request("Conclusion")
            
            
    def computeMatchResults(self):
        """
        Determine jelly bean rewards. If neither team fell in, determine if it
        was a decisive victory or too close to call (a tie). 
        """
        
        # This seems like the easiest way to get this bean multiplier in for all these different jelly bean cases
        beanMultiplier = 1
        if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_DAY):
            beanMultiplier = PartyGlobals.JellyBeanDayMultiplier
        
        
        if self.endedWithFall:
            winningTeam = 1 - self.losingTeam # take advantage of enum nature of PartyGlobals.TeamActivityTeams
            for toonId in self.toonIds[winningTeam]:
                self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.TugOfWarFallInWinReward * beanMultiplier
            for toonId in self.toonIds[self.losingTeam]:
                self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.TugOfWarFallInLossReward * beanMultiplier
        else:
            # if there is no obvious winner, check how far the teams moved
            if abs(self.globalOffset) < PartyGlobals.TugOfWarTieThreshold:
                # a tie
                self.losingTeam = PartyGlobals.TeamActivityNeitherTeam
                for toonId in self.getToonIdsAsList():
                    self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.TugOfWarTieReward * beanMultiplier
            else:
                if self.globalOffset > 0:
                    # right team wins
                    self.losingTeam = PartyGlobals.TeamActivityTeams.LeftTeam
                else: 
                    # left team wins
                    self.losingTeam = PartyGlobals.TeamActivityTeams.RightTeam
                winningTeam = 1 - self.losingTeam # take advantage of enum nature of PartyGlobals.TeamActivityTeams
                for toonId in self.toonIds[winningTeam]:
                    self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.TugOfWarWinReward * beanMultiplier
                for toonId in self.toonIds[self.losingTeam]:
                    self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.TugOfWarLossReward * beanMultiplier
        
                    
    def getConclusionData(self):
        return self.losingTeam
    
