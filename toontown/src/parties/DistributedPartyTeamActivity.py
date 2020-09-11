#===============================================================================
# Contact: Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: October 14, 2009
# Purpose: Base class for a session-based activity with two teams (client side).
#
#    Note that this class was originally extracted from
#    DistributedPartyTugOfWarActivity.py
#===============================================================================
# Config Overrides:
# party-team-activity-single-player bool
#  Allows the dev to run the activity with a single toon playing in it
#
# party-team-activity-start-delay int
#  How long the game should wait before it starts
#
# party-team-activity-duration int
#  How long the Active states lasts in the game
#===============================================================================
from direct.distributed.ClockDelta import globalClockDelta

from toontown.toonbase import TTLocalizer

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyActivity import DistributedPartyActivity
from toontown.parties.activityFSMs import TeamActivityFSM
from toontown.parties.TeamActivityGui import TeamActivityGui

class DistributedPartyTeamActivity(DistributedPartyActivity):
    notify = directNotify.newCategory("DistributedPartyTeamActivity")
    
    def __init__(
        self,
        cr, activityId,
        startDelay = PartyGlobals.TeamActivityStartDelay,
        balanceTeams = False
        ):
        """
        Parameters
            cr is the instance of ClientRepository
            activityId is the activity's id (set in PartyGlobals)
        """
        DistributedPartyActivity.__init__(
            self,
            cr,
            activityId,
            PartyGlobals.ActivityTypes.GuestInitiated,
            wantRewardGui=True,
            )
        self.notify.debug("__init__")
        
        self.toonIds = (
            [], # left team toon Ids
            [], # right team toon Ids
            )
        
        self.isLocalToonPlaying = False
        self.localToonTeam = None # a PartyGlobals.TeamActivityTeams value
        
        # used to even out a lopsided game
        self.advantage = 1.0
        
        self.waitToStartTimestamp = None # tracks when WaitToStart began for late comers
        
        # These are required fields set by the ai
        self._maxPlayersPerTeam = 0
        self._minPlayersPerTeam = 0
        self._duration = 0
        
        self._startDelay = base.config.GetFloat("party-team-activity-start-delay", startDelay)
        self._willBalanceTeams = balanceTeams
        
        self._currentStatus = ""
        
    
    def load(self):
        """Load the necessary assets"""
        DistributedPartyActivity.load(self)
        assert(self.notify.debug("load"))
        
        self.teamActivityGui = TeamActivityGui(self)
        
        # create state machine and set initial state
        self.activityFSM = TeamActivityFSM(self)
    
    def unload(self):
        DistributedPartyActivity.unload(self)
        
        del self.activityFSM

        self.teamActivityGui.unload()
        del self.teamActivityGui
        
        # delete variables
        if hasattr(self, "toonIds"):
            del self.toonIds
            
        del self.isLocalToonPlaying
        del self.localToonTeam
        del self.advantage
        del self.waitToStartTimestamp

#===============================================================================
# Should be overridden by child class
#===============================================================================

    def handleToonShifted(self, toonId):
        """Toon successfully shifted teams"""
        self.notify.error("handleToonShifted( toonId=%d ) must be overriden by child class." % toonId)

    def handleToonSwitchedTeams(self, toonId):
        """Toon successfully shifted teams"""
        if toonId == base.localAvatar.doId and self._canSwitchTeams:
            if self.isState("WaitForEnough") or self.isState("WaitToStart"):
                self.teamActivityGui.enableExitButton()
                self.teamActivityGui.enableSwitchButton()
        

    def handleToonDisabled(self, toonId):
        """Toon/player has unexpectedly dropped out of the activity (exited game, crashed, disconnected, etc)"""
        self.notify.error("handleToonDisabled( toonId=%d ) must be overriden by child class." % toonId )


    #def handleRewardDone(self):
    #    DistributedPartyTeamActivity.handleRewardDone(self)
    
#===============================================================================
# Distributed Methods
#===============================================================================

    # broadcast required
    def setPlayersPerTeam(self, min, max):
        """
        Coming from the AI, it sets the minimimum and maximum players
        that can join a team.
        """
        assert(self.notify.debug("setPlayersPerTeam min=%d max=%d" % (min, max)))
        
        self._minPlayersPerTeam = min
        self._maxPlayersPerTeam = max
        
        
    # broadcast required
    def setDuration(self, duration):
        """
        Coming from the AI, it sets how long the active state lasts.
        """
        assert(self.notify.debug("setDuration duration=%d" % duration))
        
        self._duration = duration
        
    # broadcast required
    def setCanSwitchTeams(self, canSwitchTeams):
        self._canSwitchTeams = canSwitchTeams
        
    # clsend airecv
    def d_toonJoinRequest(self, team):
        """
        Send request for local toon to join the activity. Expect a
        joinRequestDenied or handleToonJoined in reply.
        """
        if self.isLocalToonInActivity():
            return
        
        if (self.activityFSM.state in ["WaitForEnough", "WaitToStart"] and
            self._localToonRequestStatus is None):
            assert(self.notify.debug("d_toonJoinRequest( team=%s )" % PartyGlobals.TeamActivityTeams.getString(team)))

            base.cr.playGame.getPlace().fsm.request("activity")
            self.localToonJoining()
            self.sendUpdate("toonJoinRequest", [team])
    
    
    # clsend airecv
    def d_toonExitRequest(self):
        """
        Requests to for local toon to drop out of the activity. Expect a
        exitRequestDenied or handleToonExited in reply.
        """
        # determine which team the local toon is on
        toonId = base.localAvatar.doId
        team = self.getTeam(toonId)
        
        if team is not None:
            if self._localToonRequestStatus is None:
                assert(self.notify.debug("d_toonExitRequest"))
                self.localToonExiting()
                self.sendUpdate("toonExitRequest", [team])
        else:
            self.notify.warning("Not sending exitRequest as localToon has no team.")
            
    # from ai to a single avatar
    def joinRequestDenied(self, reason):
        """Local Toon was not allowed to join activity"""
        DistributedPartyActivity.joinRequestDenied(self, reason)
        self.notify.debug("joinRequestDenied")
        
        # let the local toon know that they were denied
        if reason == PartyGlobals.DenialReasons.Full:
            self.showMessage(TTLocalizer.PartyTeamActivityTeamFull)
        elif reason == PartyGlobals.DenialReasons.Default:
            self.showMessage(TTLocalizer.PartyTeamActivityJoinDenied % self.getTitle())

    # from ai to avatar
    def exitRequestDenied(self, reason):
        """Local Toon was not allowed to exit activity"""
        DistributedPartyActivity.exitRequestDenied(self, reason)
        
        if reason == PartyGlobals.DenialReasons.Default:
            self.showMessage(TTLocalizer.PartyTeamActivityExitDenied % self.getTitle())
            
        if  self.isLocalToonPlaying and \
            (self.isState("WaitToStart") or self.isState("WaitForEnough")):
            self.teamActivityGui.enableExitButton()
            
            if self._canSwitchTeams:
                self.teamActivityGui.enableSwitchButton()
    
    # clsend airecv
    def d_toonSwitchTeamRequest(self):
        assert(self.notify.debug("d_switchTeamRequest"))
        if not self._canSwitchTeams:
            return
        
        self.sendUpdate("toonSwitchTeamRequest")
            
    # from ai to avatar
    def switchTeamRequestDenied(self, reason):
        """Local Toon was not allowed to switch teams"""
        self.notify.debug("switchTeamRequestDenied")
        
        # let the local toon know that they were denied
        if reason == PartyGlobals.DenialReasons.Full:
            # Unlike joinRequestDenied, the toon stays in the activity.
            self.showMessage(TTLocalizer.PartyTeamActivityTeamFull, endState='activity')
        elif reason == PartyGlobals.DenialReasons.Default:
            # Unlike joinRequestDenied, the toon stays in the activity.
            self.showMessage(TTLocalizer.PartyTeamActivitySwitchDenied, endState='activity')
            
        if self.isLocalToonPlaying and \
            (self.isState("WaitToStart") or self.isState("WaitForEnough")) and \
            self._canSwitchTeams:
                self.teamActivityGui.enableSwitchButton()

    # required broadcast ram
    def setToonsPlaying(self, leftTeamToonIds, rightTeamToonIds):
        """
        Overrides DistributedPartyActivity's setToonsPlaying.
        
        Computes who has entered, left, shifted, or switched on each
        team and calls the appropriate handlers.
        """
        assert(self.notify.debug("setToonsPlaying"))
        
        newToonIds = [leftTeamToonIds, rightTeamToonIds]
        (exitedToons, joinedToons, shifters, switchers) = self.getToonsPlayingChanges(self.toonIds, newToonIds)
        
        assert(self.notify.debug("\texitedToons: %s" % exitedToons))
        assert(self.notify.debug("\tjoinedToons: %s" % joinedToons))
        assert(self.notify.debug("\tshifters: %s" % shifters))
        assert(self.notify.debug("\tswitchers: %s" % switchers))
        
        if base.localAvatar.doId in exitedToons:
            # make sure localToon's exit animation plays when the server clears out all players
            self.localToonExiting()
            
        self._processExitedToons(exitedToons)
        
        # update self.toonIds after we have dealt with exited toons so code
        # can still reference teams
        self.setToonIds([leftTeamToonIds, rightTeamToonIds])
        
        self._processJoinedToons(joinedToons)
                    
        # update self.toonIds after we have dealt with exited toons so code
        # can still reference teams
        for toonId in shifters:
            self.handleToonShifted(toonId)
            
        if self._canSwitchTeams:
            for toonId in switchers:
                self.handleToonSwitchedTeams(toonId)
                
        if self.isState("WaitForEnough"):
            self._updateWaitForEnoughStatus()
            
    def _updateWaitForEnoughStatus(self):
        amount = self.getNumToonsNeededToStart()
        
        if self._willBalanceTeams:
            text = TTLocalizer.PartyTeamActivityForMoreWithBalance
        else:
            text = TTLocalizer.PartyTeamActivityForMore
            
        if amount > 1:
            plural = TTLocalizer.PartyTeamActivityForMorePlural
        else:
            plural = ""
            
        self.setStatus(text % (amount, plural))
            

    # broadcast ram
    def setState(self, newState, timestamp, data):
        DistributedPartyActivity.setState( self, newState, timestamp )
        assert(self.notify.debug( "setState( newState=%s, ... )" % newState ))

        # pass additional parameters only to those states that need it
        if newState == "WaitToStart":
            self.activityFSM.request( newState, timestamp )
        elif newState == "Conclusion":
            self.activityFSM.request( newState, data )
        else:
            self.activityFSM.request( newState )
            
            
    # clsend airecv
    def d_toonReady(self):
        """Tells the AI that the local toon is ready to play."""
        assert(self.notify.debug("toonReady"))
        
        self.sendUpdate("toonReady")
        
    # from ai to a single avatar
    def setAdvantage(self, advantage):
        assert(self.notify.debug("setAdvantage %d" % advantage))
        
        self.advantage = advantage
      
#===============================================================================
# Handlers          
#===============================================================================

    def handleToonJoined(self, toonId):
        """Toon successfully joined the activity"""
        assert(self.notify.debug("handleToonJoined %d" % toonId))
        
        if toonId == base.localAvatar.doId:
            self.isLocalToonPlaying = True
            self.localToonTeam = self.getTeam(base.localAvatar.doId)
            
            self.teamActivityGui.load()
            self.teamActivityGui.enableExitButton() # display "hop off" button
            
            if self._canSwitchTeams:
                self.teamActivityGui.enableSwitchButton()
            
            if self.activityFSM.state == "WaitToStart":
                self.showWaitToStartCountdown()
            else:
                self.showStatus() # display game status
 
        
    def handleToonExited(self, toonId):
        """Toon successfully exited the activity"""
        assert(self.notify.debug("handleToonExited %d" % toonId))
        
        if toonId == base.localAvatar.doId:
            self.hideStatus()
            self.teamActivityGui.disableExitButton()
            
            if self._canSwitchTeams:
                self.teamActivityGui.disableSwitchButton()
            
            if self.activityFSM.state == "WaitToStart":
                self.hideWaitToStartCountdown()
            
            self.teamActivityGui.unload()
                
            self.isLocalToonPlaying = False
            self.localToonTeam = None
            
            
    def handleRulesDone(self):
        """
        LocalToon has read the rules.
        """
        self.notify.debug("handleRulesDone")
        
        self.d_toonReady()
        self.activityFSM.request("WaitForServer")
        
    def handleGameTimerExpired(self):
        """Called when the GUI gamer timer expires"""
        pass
  
#===============================================================================
# Utility Methods
#===============================================================================
    
    def getToonsPlayingChanges(self, oldToonIds, newToonIds):
        """
        Returns a tuple of
        (
            list of toonIds of toons who exited
            list of toonIds of toons who joined
            list of toonIds of toons that shifted spots in the same team
            list of toonIds that switched teams
        )
        """
        oldLeftTeam = oldToonIds[0]
        oldRightTeam = oldToonIds[1]
        newLeftTeam = newToonIds[0]
        newRightTeam = newToonIds[1]
        oldToons = set(oldLeftTeam + oldRightTeam)
        newToons = set(newLeftTeam + newRightTeam)
        
        # find toons that are no longer in the game
        exitedToons = oldToons.difference(newToons)
        
        # find toons that just joined the game
        joinedToons = newToons.difference(oldToons)
        
        # find toons that switched spots or switched Teams
        shifters = []
        
        if self._canSwitchTeams:
            switchers = list(set(oldLeftTeam) & set(newRightTeam)) + \
                list(set(oldRightTeam) & set(newLeftTeam))
        else:
            switchers = []
        
        for i in range(len(PartyGlobals.TeamActivityTeams)):
            persistentToons = set(oldToonIds[i]) & set(newToonIds[i])
            for toonId in persistentToons:
                if oldToonIds[i].index(toonId) != newToonIds[i].index(toonId):
                    shifters.append(toonId)

        return(list(exitedToons), list(joinedToons), shifters, switchers)
    
    
    def getMaxPlayersPerTeam(self):
        return self._maxPlayersPerTeam
    
    
    def getMinPlayersPerTeam(self):
        return self._minPlayersPerTeam
    
    
    def getNumToonsNeededToStart(self):
        if self._willBalanceTeams:
            return abs((self._minPlayersPerTeam * 2) - self.getNumToonsPlaying())
        else:
            return self._minPlayersPerTeam

    
    def getToonIdsAsList(self):
        """
        Returns a list of doId's of all toons in this activity.
        """
        return self.toonIds[0] + self.toonIds[1]


    def getNumToonsPlaying(self):
        """Returns the total number of toons in the activity"""
        return (len(self.toonIds[0]) + len(self.toonIds[1]))
    
    
    def getNumToonsInTeam(self, team):
        assert(team >= 0 and team < 2)
        
        return len(self.toonIds[team])
  
    
    def getTeam(self, toonId):
        """
        Utility function that returns the team toonId is on, as a 
        PartyGlobals.TeamActivityTeams value, or None if toonId isn't on either team.
        """
        for i in range(len(PartyGlobals.TeamActivityTeams)):
            if self.toonIds[i].count(toonId) > 0:
                return i
        else:
            return None
   
    
    def getIndex(self, toonId, team):
        """
        Return the index/order of the toon in the team list.
        """
        if self.toonIds[team].count(toonId) > 0:
            return self.toonIds[team].index(toonId)
        else:
            return None
    
#===============================================================================
# Actions
#===============================================================================
    
    def _joinLeftTeam(self, collEntry):
        """Ask the AI if we can join the left team"""
        assert(self.notify.debug("_joinLeftTeam"))
        
        if self.isLocalToonInActivity():
            # the toon is in another activity (probably the cannon), do not 
            # start this one
            return

        self.d_toonJoinRequest(PartyGlobals.TeamActivityTeams.LeftTeam)
        
    def _joinRightTeam(self, collEntry):
        """Ask the AI if we can join the right team"""
        assert(self.notify.debug("_joinRightTeam"))
        
        if self.isLocalToonInActivity():
            # the toon is in another activity (probably the cannon), do not 
            # start this one
            return
        
        self.d_toonJoinRequest(PartyGlobals.TeamActivityTeams.RightTeam)
        
        
    def showWaitToStartCountdown(self):
        """Shows the countdown timer during the WaitToStart state"""
        if self.waitToStartTimestamp is None:
            self.notify.warning("showWaitToStartCountdown was called when self.waitToStartTimestamp was None")
            return
        
        self.teamActivityGui.showWaitToStartCountdown(
            self._startDelay,
            self.waitToStartTimestamp,
            almostDoneCallback=self._onCountdownAlmostDone
            )
        
        self.showStatus()
        self.teamActivityGui.enableExitButton()
        

    def _onCountdownAlmostDone(self):
        if self._canSwitchTeams:
            self.teamActivityGui.disableSwitchButton()
    
    
    def hideWaitToStartCountdown(self):
        self.teamActivityGui.hideWaitToStartCountdown()
        self.teamActivityGui.disableExitButton()
        self.hideStatus()
        
    
    def setStatus(self, text):
        """Sets the status text"""
        self._currentStatus = text
        
        if self.isLocalToonPlaying:
            self.showStatus()
    
    def showStatus(self):
        """Show the status text"""
        if self.teamActivityGui is not None:
            self.teamActivityGui.showStatus(self._currentStatus)
    
    def hideStatus(self):
        """Hides the status text"""
        if self.teamActivityGui is not None:
            self.teamActivityGui.hideStatus()
        
        
#===============================================================================
# FSM transitions
#===============================================================================

    def toonsCanSwitchTeams(self):
        """
        Check if the local toon can switch to the other team. This is dependent
        on the implementation of the activity, and some will not let the player switch.
        """
        return self._canSwitchTeams
    
    def isState(self, state):
        return hasattr(self, "activityFSM") and self.activityFSM.getCurrentOrNextState() == state
    
    def startWaitForEnough(self):
        """
        Wait for for the minimum number players to join the activity.
        """
        self.notify.debug("startWaitForEnough")
        
        self.advantage = 1.0
        self._updateWaitForEnoughStatus()
        
        if self.isLocalToonPlaying:
            self.teamActivityGui.enableExitButton() # display "hop off" button
            if self._canSwitchTeams:
                self.teamActivityGui.enableSwitchButton()
    
    def finishWaitForEnough(self):
        """
        There are enough players in the activity to start.
        Transitioning to WaitToStart.
        """
        self.notify.debug("finishWaitForEnough")

        
    def startWaitToStart(self, waitStartTimestamp):
        """
        Enough players are in.
        
        Wait a few seconds before the activity begins to let more players
        come in and participate.
        """
        self.notify.debug("startWaitToStart")

        self.waitToStartTimestamp = globalClockDelta.networkToLocalTime(waitStartTimestamp)
        self._updateWaitForEnoughStatus()
    
        # display a countdown showing how long until the game starts
        self.setStatus(TTLocalizer.PartyTeamActivityWaitingToStart)
        
        if self.isLocalToonPlaying:
            self.showWaitToStartCountdown()
                

    def finishWaitToStart(self):
        """
        The wait time is over and now we're displaying the rules on the clients and
        the AI is waiting until everyone reads the rules.
        
        Or we're below the number of toons required for the activity,
        so we go back to the WaitForEnough state.
        """
        self.notify.debug("finishWaitToStart")
        
        if self.isLocalToonPlaying:
            self.hideWaitToStartCountdown()
            
            if self._canSwitchTeams:
                self.teamActivityGui.disableSwitchButton()
        
        self.waitToStartTimestamp = None
        
        
    def startRules(self):
        """
        The activity is currently display the rules to the clients, and waiting
        for all to read them.
        """
        self.notify.debug("startRules")
        # display rules to the local toon if we have one
        if self.isLocalToonPlaying:
            DistributedPartyActivity.startRules(self) # show instructions

    def finishRules(self):
        """
        The clients have finished reading the rules and we're going to the active state.
        Or one the clients dropped and we're back to WaitToStart
        """
        self.notify.debug("finishRules")
        
        if self.isLocalToonPlaying:
            DistributedPartyActivity.finishRules(self) # clean up instructions
        
        # check for a non-standard transition and do additional cleanup as needed
        if self.activityFSM.getCurrentOrNextState() == "WaitForEnough":
            DistributedPartyActivity.finishRules(self) # clean up instructions
        
        
    def startWaitForServer(self):
        """
        Waiting for the server to start the activity.
        """
        self.notify.debug("startWaitForServer")
        
        self.setStatus(TTLocalizer.PartyTeamActivityWaitingForOtherPlayers)
        
    def finishWaitForServer(self):
        """
        Finished waiting for the server. We're either starting the activity
        or we are back to WaitForEnough in case a toon dropped out at the last
        minute.
        """
        self.notify.debug("finishWaitForServer")
        
        # clean up status display
        if self.isLocalToonPlaying:
            self.hideStatus()
        
        
    def startActive(self):
        """
        The activity begins!
        """
        self.notify.debug("startActive")
        
        if self.isLocalToonPlaying:
            self.hideStatus()
            self.teamActivityGui.showTimer(self._duration)
            
    def finishActive(self):
        """
        The activity ends or a toon dropped out causing the activity to go
        back to WaitToStart.
        """
        self.notify.debug("finishActive")
        
        if self.isLocalToonPlaying: 
            self.teamActivityGui.hideTimer()
            self.hideStatus()

        # check for a non-standard transition and do additional cleanup as needed
#        if self.activityFSM.getCurrentOrNextState() == "WaitForEnough":
#            pass # should additional cleanup happen here?
        
        
    def startConclusion(self, data):
        """
        Display the results for the activity.
        
        Parameters
            data is a unsigned 32 bit integer packed with some important
            information regarding the conclusion.
        """
        self.notify.debug("startConclusion")
        
        self.setStatus("")
        
        if self.isLocalToonPlaying:
            # Because conclusion is bypassing d_toonExitRequest during the conclusion, this needs to be
            # set in order for the server to clean up the Toon properly.
            self.localToonExiting()
    
    
    def finishConclusion(self):
        """
        The conclusion timer is over and we're going back to WaitToStart
        for a new cycle.
        """
        self.notify.debug("finishConclusion")
        
        if self.isLocalToonPlaying:
            self.hideStatus()
