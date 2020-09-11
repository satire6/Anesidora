#===============================================================================
# Contact: Edmundo Ruiz (Schell Games)
# Created: September 2009
#
# Purpose: Distributed controller for Party Cog "Pinata" Activity in the client
#===============================================================================
from direct.distributed.ClockDelta import globalClockDelta

from pandac.PandaModules import Point3

from toontown.toonbase import TTLocalizer

import PartyGlobals
from DistributedPartyTeamActivity import DistributedPartyTeamActivity
from PartyCogActivity import PartyCogActivity
from toontown.toon import GMUtils

class DistributedPartyCogActivity(DistributedPartyTeamActivity):
    notify = directNotify.newCategory("DistributedPartyCogActivity")
    
    players = {}
    localPlayer = None
    view = None
    
    def __init__(self, cr):
        DistributedPartyTeamActivity.__init__(
            self, cr,
            PartyGlobals.ActivityIds.PartyCog,
            startDelay=PartyGlobals.CogActivityStartDelay,
            balanceTeams=PartyGlobals.CogActivityBalanceTeams
            )
        
    def load(self):
        DistributedPartyTeamActivity.load(self)
        
        self.view = PartyCogActivity(self)
        self.view.load()
        
    def announceGenerate(self):
        DistributedPartyTeamActivity.announceGenerate(self)
        
        # Because setToonsPlaying is a required field
        # And load is called at announceGenerate
        # The toons that are in that activity to be positioned
        # in the view after we get all the data and the view is loaded.
        for i in range(len(self.toonIds)):
            for toonId in self.toonIds[i]:
                toon = base.cr.doId2do.get(toonId, None)
                if toon:
                    self.view.handleToonJoined(toon, i, lateEntry=True)
        
    def unload(self):
        if hasattr(self, "view") and self.view is not None:
            self.view.unload()
            del self.view
            
        DistributedPartyTeamActivity.unload(self)
        
    def enable(self):
        DistributedPartyTeamActivity.enable(self)
        
    def disable(self):
        DistributedPartyTeamActivity.disable(self)
        
    def getTitle(self):
        return TTLocalizer.PartyCogTitle
    
    def getInstructions(self):
        return TTLocalizer.PartyCogInstructions

#===============================================================================
# Distributed
#===============================================================================

    # broadcast clsend
    def pieThrow(self, toonId, timestamp, h, x, y, z, power):
        """
        Broadcast event coming from another client that announces a that a toon in
        the activity has thrown a pie.
        
        This method handles the visual. Scoring and other is handled by the AI
        with pieHitsCog
        """
        assert(self.notify.debug("Toon %d throwing pie!" % toonId))
        
        # Because we want the throw be immediate and this is a broadcast
        # event, we ignore the request from the local toon.
        # Otherwise, it throws a pie TWICE:
        # Once locally, and once at a request from the server.
        if toonId != base.localAvatar.doId:
            assert(self.notify.debug("pieThrow"))
            
            self.view.pieThrow(toonId, timestamp, h, Point3(x, y, z), power)
            
    def b_pieThrow(self, toon, power):
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        pos = toon.getPos()
        h = toon.getH()
        toonId = toon.doId
        
        self.view.pieThrow(toonId, timestamp, h, pos, power)
        self.d_broadcastPieThrow(toonId, timestamp, h, pos[0], pos[1], pos[2], power)
    
    def d_broadcastPieThrow(self, toonId, timestamp, h, x, y, z, power):
        self.sendUpdate(
            'pieThrow',
            [toonId, timestamp, h, x, y, z, power]
            )
      
      
    # broadcast clsend
    def pieHitsToon(self, toonId, timestamp, x, y, z):
        """
        Broadcast event coming from another client that announces a that a toon in
        the activity was hit with a pie.
        """
        assert(self.notify.debug("pieHitsToon %s" % toonId))
        self.view.pieHitsToon(toonId, timestamp, Point3(x, y, z))
    
    def d_broadcastPieHitsToon(self, toonId, timestamp, pos):
        self.sendUpdate(
            "pieHitsToon",
                [toonId,
                timestamp,
                pos[0], pos[1], pos[2],
                ]
            )
        
    def b_pieHitsToon(self, toonId, timestamp, pos):
        self.view.pieHitsToon(toonId, timestamp, pos)
        self.d_broadcastPieHitsToon(toonId, timestamp, pos)


    # broadcast clsend airecv
    def pieHitsCog(self, toonId, timestamp, hitCogNum, x, y, z, direction, part):
        """
        Broadcast event coming from another client that announces a that a cog in
        the activity was hit with a pie.
        
        Should only be used to display the pie splat. The actual scoring and movement
        is handled on the AI side
        """
        if toonId != base.localAvatar.doId:
            assert(self.notify.debug("pieHitsCog"))
                
            self.view.pieHitsCog(timestamp, hitCogNum, Point3(x, y, z), direction, part)
    
    def b_pieHitsCog(self, timestamp, hitCogNum, pos, direction, part):
        self.view.pieHitsCog(timestamp, hitCogNum, pos, direction, part)
        self.d_broadcastSendPieHitsCog(timestamp, hitCogNum, pos, direction, part)
        
    def d_broadcastSendPieHitsCog(self, timestamp, hitCogNum, pos, direction, part):
        self.sendUpdate(
            "pieHitsCog",
            [base.localAvatar.doId,
                timestamp,
                hitCogNum,
                pos[0], pos[1], pos[2],
                direction,
                part
                ]
            )


    # broadcast ram
    def setCogDistances(self, distances):
        """
        Sets the updated distances of the cogs coming from the AI.
        
        Parameters:
            array of size 3 with distances from -1.0 to -1.0
        """
        assert(self.notify.debug("setCogDistances %s" % distances))
        
        self.view.setCogDistances(distances)
        
        
    # broadcast ram
    def setHighScore(self, toonName, score):
        """
        Displays the high score on the activity sign.
        
        Parameters:
            toonName a string with the name of the last toon that hit a high scoore
            score the score amount the last toon reached
        """
        if GMUtils.testGMIdentity(toonName):
            toonName = GMUtils.handleGMName(toonName)
            
        assert(self.notify.debug("setHighScore %s %d" % (toonName, score)))
            
        self.setSignNote(TTLocalizer.PartyCogSignNote % (toonName, score))
    
#===============================================================================
# Handlers
#===============================================================================

    def handleToonJoined(self, toonId):
        """
        Whenever a new toon joins the activity, this function is called.
        
        Parameters:
            toonId -- doId of the toon that joined
        """
        DistributedPartyTeamActivity.handleToonJoined(self, toonId)
        
        toon = base.cr.doId2do.get(toonId, None)
        team = self.getTeam(toonId)
        
        if toon is not None and self.view is not None:
            self.view.handleToonJoined(toon, team)
            

    def handleToonExited(self, toonId):
        """
        Whenever a toon exits the activity, this function is called.
        
        Parameters:
            toonId -- doId of the toon that exited
        """
        toon = base.cr.doId2do.get(toonId, None)
        
        if toon is None:
            return
        
        if self.view is not None:
            self.view.handleToonExited(toon)
            
        DistributedPartyTeamActivity.handleToonExited(self, toonId)
            
        
    def handleToonShifted(self, toonId):
        """
        Whenever a toon's order in the team changes, this method is called.
        
        Parameters:
            toonId -- doId of the toon that shifted
        """
        toon = base.cr.doId2do.get(toonId, None)
        
        if toon is None:
            return
        
        if self.view is not None:
            self.view.handleToonShifted(toon)
    
    
    def handleToonSwitchedTeams(self, toonId):
        """
        Whenever a toon's switches teams, this method is called.
        
        Parameters:
            toonId -- doId of the toon that switched
        """
        DistributedPartyTeamActivity.handleToonSwitchedTeams(self, toonId)
        toon = base.cr.doId2do.get(toonId, None)
        
        if toon is None:
            return
        
        if self.view is not None:
            self.view.handleToonSwitchedTeams(toon)
    
    
    def handleToonDisabled(self, toonId):
        """
        A toon dropped unexpectedly from the game. Handle it!
        
        Parameters:
            toonId -- doId of the toon that exited
        """
        if self.view is not None:
            self.view.handleToonDisabled(toonId)
            
#===============================================================================
# FSM Additions
#===============================================================================
    
    def startWaitForEnough(self):
        DistributedPartyTeamActivity.startWaitForEnough(self)
        
        self.view.openArenaDoors()
        self.view.hideCogs()
        
    def startRules(self):
        DistributedPartyTeamActivity.startRules(self)
        
        self.view.closeArenaDoors()
        self.view.showCogs()
        
    def startActive(self):
        DistributedPartyTeamActivity.startActive(self)
        
        self.view.startActivity(self.getCurrentActivityTime())
        self.view.closeArenaDoors()
        
        # That extra second for lag + door intervals and so forth...
        # But show only if the local Toon is not playing in the activity.
        if not self.isLocalToonPlaying:
            self.view.showArenaDoorTimers(
                (self._duration + PartyGlobals.CogActivityConclusionDuration + 1.0) -
                self.getCurrentActivityTime()
                )
        
    def finishActive(self):
        DistributedPartyTeamActivity.finishActive(self)
        
        self.view.stopActivity()
        
    def startConclusion(self, data):
        # Data is the score of the two teams as a single digit:
        # <leftScore><rightScore>
        #
        # Therefore we split it into two with the computations:
        # leftScore = int(data / 10000)
        # rightScore = data % 10000
        #
        # Team score is 4-digit number from 0000 to 1000
        # Divided by 1000.0 will get you the approximate official distance that
        # was given by the AI
        
        DistributedPartyTeamActivity.startConclusion(self, data)
        
        if self.isLocalToonPlaying:
            score = (int(data / 10000), data % 10000)
            winner = 2
        
            # Left team wins
            if score[PartyGlobals.TeamActivityTeams.LeftTeam] > score[PartyGlobals.TeamActivityTeams.RightTeam]:
                winner = PartyGlobals.TeamActivityTeams.LeftTeam
            # Right team wins
            elif score[PartyGlobals.TeamActivityTeams.LeftTeam] < score[PartyGlobals.TeamActivityTeams.RightTeam]:
                winner = PartyGlobals.TeamActivityTeams.RightTeam
                
            if winner < 2:
                if self.getTeam(base.localAvatar.doId) == winner:
                    resultsText = TTLocalizer.PartyTeamActivityLocalAvatarTeamWins
                else:
                    resultsText = TTLocalizer.PartyTeamActivityWins % TTLocalizer.PartyCogTeams[winner]
            else:
                resultsText = TTLocalizer.PartyTeamActivityGameTie
            
            self.view.showResults(resultsText, winner, score)
        
    
    def finishConclusion(self):
        self.view.hideResults()
        
        DistributedPartyTeamActivity.finishConclusion(self)
        
        self.view.hideArenaDoorTimers()
        
