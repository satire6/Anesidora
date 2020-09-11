#===============================================================================
# Contact: Edmundo Ruiz (Schell Games)
# Created: September 2009
#
# Purpose: Distributed controller for Party Cog "Pinata" Activity in the AI
#===============================================================================
from direct.showbase.PythonUtil import bound as clamp

from toontown.toonbase import TTLocalizer

from DistributedPartyTeamActivityAI import DistributedPartyTeamActivityAI
import PartyGlobals
import PartyCogUtils

class DistributedPartyCogActivityAI(DistributedPartyTeamActivityAI):
    notify = directNotify.newCategory("DistributedPartyCogActivityAI")
    
    cogDistances = [0, 0, 0] # [cog0, cog1, cog2] goes from -1.0 to 1.0
    score = [0, 0] # [leftTeam, rightTeam]
    toonScore = {}
    
    highScore = ("", 0) # toonName (in case the toon disconnects), score
    
    def __init__(self, air, doId, x, y ,h):
        DistributedPartyTeamActivityAI.__init__(
            self, air, doId, x, y, h,
            PartyGlobals.ActivityIds.PartyCog,
            minPlayersPerTeam=PartyGlobals.CogActivityMinPlayersPerTeam,
            maxPlayersPerTeam=PartyGlobals.CogActivityMaxPlayersPerTeam,
            duration=PartyGlobals.CogActivityDuration,
            conclusionDuration=PartyGlobals.CogActivityConclusionDuration,
            startDelay=PartyGlobals.CogActivityStartDelay,
            balanceTeams=True,
            calcAdvantage=True,
            canSwitchTeams=True,
            )
        
        self.cogHeadStartZ = PartyGlobals.CogPinataHeadZ
        
#===============================================================================
# Distributed 
#===============================================================================
   
    # broadcast clsend airecv
    def pieHitsCog(self, toonId, timestamp, hitCogNum, x, y, z, direction, hitHead):
        # Count it only if it's the active state. It may be a very delayed hit, sadly.
        if not self.isState("Active"):
            return
        
        assert(self.notify.debugStateCall(self))
        
        if hitHead:
            if z < self.cogHeadStartZ:
                senderId = self.air.getAvatarIdFromSender()
                self.notify.debug("pieHitsCog suspicious behavior for toon: %s, z: %d < %d" % (toonId, z, self.cogHeadStartZ))
                self.air.writeServerEvent(
                    "suspicious",
                    senderId,
                    "Toon %s hits cog head in PartyCogActivity, but the head z %d is less than the expected min z %d." %
                    (toonId, z, self.cogHeadStartZ)
                    )
                
            points = PartyGlobals.CogActivityHitPointsForHead
        else:
            points = PartyGlobals.CogActivityHitPoints
        
        self._addToToonScore(toonId, points)
        
        advantage = self.advantage[self.getTeam(toonId)]
        
        self._updateCogDistance(hitCogNum, direction, advantage, hitHead)
        self.d_broadcastSetCogDistances()
        
    def d_broadcastSetCogDistances(self):
        self.sendUpdate("setCogDistances", [self.cogDistances])
        
    def getHighScore(self):
        return self.highScore
    
    # broadcast ram
    def d_broadcastSetHighScore(self):
        self.sendUpdate("setHighScore", list(self.highScore))
        
#===============================================================================
# Actions 
#===============================================================================

    def _updateCogDistance(self, cogNum, direction, advantage, hitHead):
        if hitHead:
            factor = PartyGlobals.CogPinataPushHeadFactor
        else:
            factor = PartyGlobals.CogPinataPushBodyFactor
            
        distance = self.cogDistances[cogNum] + (factor * direction * advantage)
        
        self.cogDistances[cogNum] = clamp(distance, -1.0, 1.0)

    def _resetCogDistances(self):
        self.cogDistances = [0, 0, 0]
        
    def _resetScores(self):
        self.toonScore.clear()
        self.score = [0, 0]

    def _addToToonScore(self, toonId, points):
        if self.toonScore.has_key(toonId):
            self.toonScore[toonId] += points
            
    def _addToonToTeam(self, toonId, team):
        if DistributedPartyTeamActivityAI._addToonToTeam(self, toonId, team):
            self.toonScore[toonId] = 0
        
    def _removeToonFromTeam(self, toonId, team):
        if DistributedPartyTeamActivityAI._removeToonFromTeam(self, toonId, team) and \
            self.toonScore.has_key(toonId):
            del self.toonScore[toonId]
    
    def _findNewHighScore(self):
        """Check to see if a new high score has been made, and broadcast"""
        highScoreFound = False
        
        for toonId, score in self.toonScore.items():
            if score > self.highScore[1] and self.air.doId2do.has_key(toonId):
                self.highScore = (self.air.doId2do[toonId].getName(), score)
                highScoreFound = True
            
        if highScoreFound:
            self.d_broadcastSetHighScore()

#===============================================================================
# Utility methods 
#===============================================================================

    def computeMatchResults(self):
        """Determines who was the winning team and rewards the teams accordingly."""
        # Determine how far the cogs were pushed for every team.
        for distance in self.cogDistances:
            if distance < 0.0:
                self.score[PartyGlobals.TeamActivityTeams.LeftTeam] += abs(PartyCogUtils.getCogDistanceUnitsFromCenter(distance))
            elif distance > 0.0:
                self.score[PartyGlobals.TeamActivityTeams.RightTeam] += abs(PartyCogUtils.getCogDistanceUnitsFromCenter(distance))
        
        # Determine who won, who lost:
        if self.score[PartyGlobals.TeamActivityTeams.LeftTeam] < self.score[PartyGlobals.TeamActivityTeams.RightTeam]:
            self.losingTeam = PartyGlobals.TeamActivityTeams.LeftTeam
        elif self.score[PartyGlobals.TeamActivityTeams.RightTeam] < self.score[PartyGlobals.TeamActivityTeams.LeftTeam]:
            self.losingTeam = PartyGlobals.TeamActivityTeams.RightTeam
        else:
            self.losingTeam = PartyGlobals.TeamActivityNeitherTeam
            self.winningTeam = PartyGlobals.TeamActivityNeitherTeam

        # Tie:
        if self.resultIsTie():

            for toonId in self.getToonIdsAsList():
                self.toonIdsToJellybeanRewards[toonId] = PartyGlobals.CogActivityTieBeans

        # One of the teams won:
        else:
            self.winningTeam = 1 - self.losingTeam
            
            winBeans = PartyGlobals.CogActivityWinBeans
            lossBeans = PartyGlobals.CogActivityLossBeans
            
            # The winning team moved all of the cogs all the way:
            if self.resultIsPerfect():
                winBeans = PartyGlobals.CogActivityPerfectWinBeans
                lossBeans = PartyGlobals.CogActivityPerfectLossBeans
            
            for toonId in self.toonIds[self.winningTeam]:
                self.toonIdsToJellybeanRewards[toonId] = winBeans
                
            for toonId in self.toonIds[self.losingTeam]:
                self.toonIdsToJellybeanRewards[toonId] = lossBeans

        self._findNewHighScore()
        
    def getConclusionData(self):
        """Formats the score into a single 32 bit data"""
        return (int(self.score[0]) * 10000 + int(self.score[1]))
  
    def getJellybeanRewardMessage(self, toonId, reward):
        message = None

        if self.resultIsTie():
            message = TTLocalizer.PartyTeamActivityRewardMessage % reward
        elif self.toonIsOnWinningTeam(toonId):
            # "Your team won!\n\nYou got %d jellybeans. Good job!"
            message = TTLocalizer.PartyTeamActivityLocalAvatarTeamWins + "\n\n" +\
                      TTLocalizer.PartyTeamActivityRewardMessage % reward
        else:
            message = TTLocalizer.PartyTeamActivityRewardMessage % reward
        
        return message
    
    def resultIsTie(self):
        """ Returns True if the teams tied. """
        return self.losingTeam == PartyGlobals.TeamActivityNeitherTeam
        
    def resultIsPerfect(self):
        """ Returns True if the winning team moved all of the cogs all the way. """
        return self.score[self.winningTeam] >= 3.0 * PartyGlobals.CogActivityArenaLength / 2.0
        
    def toonIsOnWinningTeam(self, toonId):
        """ Returns True if the given toon was on the winning team. """
        return toonId in self.toonIds[self.winningTeam]
      
#===============================================================================
# FSM
#===============================================================================

    def startConclusion(self):
        # All clients should first and foremost, synchronize cog distances.
        self.d_broadcastSetCogDistances()
        
        DistributedPartyTeamActivityAI.startConclusion(self)
        
    def startWaitForEnough(self):
        DistributedPartyTeamActivityAI.startWaitForEnough(self)
        
        self._resetScores()
        self._resetCogDistances()
        self.d_broadcastSetCogDistances()
