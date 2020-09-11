#===============================================================================
# Contact: Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: October 14, 2009
# Purpose: Base class for a session-based activity with two teams (AI side).
#
#    Note that this class was originally extracted from
#    DistributedPartyTugOfWarActivityAI.py
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
from direct.distributed import ClockDelta

from toontown.toonbase import TTLocalizer

from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.activityFSMs import TeamActivityAIFSM
from toontown.parties import PartyGlobals

class DistributedPartyTeamActivityAI(DistributedPartyActivityAI):
    notify = directNotify.newCategory("DistributedPartyTeamActivityAI")
    
    def __init__(
        self,
        air, partyDoId, x, y, h,
        activityId,
        minPlayersPerTeam = PartyGlobals.TeamActivityDefaultMinPlayersPerTeam,
        maxPlayersPerTeam = PartyGlobals.TeamActivityDefaultMaxPlayersPerTeam,
        duration = PartyGlobals.TeamActivityDefaultDuration,
        conclusionDuration = PartyGlobals.TeamActivityDefaultConclusionDuration,
        startDelay = PartyGlobals.TeamActivityStartDelay,
        balanceTeams = False,
        calcAdvantage = False,
        canSwitchTeams = False,
        ):
        DistributedPartyActivityAI.__init__(
            self,
            air,
            partyDoId,
            x,
            y,
            h,
            activityId,
            PartyGlobals.ActivityTypes.GuestInitiated,
            )
        self.notify.debug("__init__")
        
        self._minPlayersPerTeam = minPlayersPerTeam
        self._maxPlayersPerTeam = maxPlayersPerTeam
        
        # How long should the conclusion state last in seconds?
        self._conclusionDuration = conclusionDuration
        
        # How long the active state lasts
        self._duration = simbase.config.GetFloat("party-team-activity-duration", duration)
        
        # How long should it wait for more players before going to the active state
        self._startDelay = simbase.config.GetFloat("party-team-activity-start-delay", startDelay)
        
        # Should it calculate whether both team have roughly an equal amount of players?
        self._shouldBalanceTeams = balanceTeams
        
        # Should it calculate the advantage of a smaller team over a larger team?
        self._shouldCalcAdvantage = calcAdvantage
        
        # Can players willingly switch teams before the game starts?
        self._canSwitchTeams = canSwitchTeams
        
        # Do we allow a single player? (This is for testing purposes)
        self._allowSinglePlayer = simbase.config.GetBool("party-team-activity-single-player", False)
        
        self.toonIds = (
            [], # doIds of toons on the left team, ordered from those nearest the water to those furthest
            [], # doIds of toons on the right team, ordered from those nearest the water to those furthest
            )
        
        self.readyToonIds = set()
        
        # Keep track of which side each avatar is on for quick look up during game
        self.toonIdsToTeams = {}

        # state transition request doLater
        self._srTask = None
        
        self.activityFSM = TeamActivityAIFSM(self)
    
    def generate(self):
        DistributedPartyActivityAI.generate(self)
        self.notify.debug("generate")
        
        self.activityFSM.request("WaitForEnough")

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.notify.debug("announceGenerate")
        
    def delete(self):
        self.cleanupRequestLater()
            
        DistributedPartyActivityAI.delete(self)
        
#===============================================================================
# Actions
#===============================================================================
        
    def _addToonToTeam(self, toonId, team):
        """
        Checks and adds a toon to the team
        
        Parameters
            toonId toon's doId
            team team number based on PartyGlobals.TeamActivityTeams
            
        Returns
            true if it successfully added the toon to the team
        """
        self.notify.debug("_addToonToTeam")
        
        # check team size limits
        if self.isTeamFull(team):
            self.notify.error("Tried to add toonId=%s to %s when it was already full." % (toonId, self.getTeamName(team)))
        # check that toonId isn't already in that team's list
        elif toonId in self.toonIds[team]:
            self.notify.warning("Tried to add toonId=%s to %s when it was already on that team. Ignoring request." % (toonId, self.getTeamName(team)))
        else:
            self.toonIds[team].append(toonId)
            self.toonIdsToTeams[toonId] = team
            self.toonId2joinTime[toonId] = globalClock.getFrameTime()
            
            # listen for this avatar's exit event
            self.acceptOnce(
                self.air.getAvatarExitEvent(toonId),
                self._handleUnexpectedToonExit,
                extraArgs=[toonId],
            )
            
            self.notify.debug("Added toonId=%s to %s." % (toonId, self.getTeamName(team)))
            self.notify.debug("toonIds:\n\t\t%s\n\t\t%s." % (self.toonIds[0], self.toonIds[1]))
            
            return True
        
        return False
    
    def _removeToonFromTeam(self, toonId, team):
        """
        Checks and removes a toon from a team
        
        Parameters
            toonId toon's doId
            team team number based on PartyGlobals.TeamActivityTeams
        
        Returns
            true if it successfully removed the toon from the team
        """
        self.notify.debug("_removeToonFromTeam")
        
        if type(team) != type(1):
            self.notify.warning("Tried to remove toonId=%s from %s, but team is not an integer" % (toonId, str(team)))
        elif not toonId in self.toonIds[team]:
            self.notify.warning("Tried to remove toonId=%s from %s when it was not on that team. Ignoring request." % (toonId, self.getTeamName(team)))
        else:
            self.ignore(self.air.getAvatarExitEvent(toonId))
            self.toonIds[team].remove(toonId)
            del self.toonIdsToTeams[toonId]
            del self.toonId2joinTime[toonId]
            
            self.notify.debug("Removed toonId=%s from %s." % (toonId, self.getTeamName(team)))
            self.notify.debug("toonIds:\n\t\t%s\n\t\t%s." % (self.toonIds[0], self.toonIds[1]))
            
            return True
        
        return False
    
    
    def _removeAllToons(self):
        """Removes all toons from the activity"""
        
        self.notify.debug("removeAllToons")
        
        for team in (PartyGlobals.TeamActivityTeams.LeftTeam, PartyGlobals.TeamActivityTeams.RightTeam, ):
            toonIds = list(self.toonIds[team])[:]
            self.notify.debug("initial toonIds for team %s = %s" % (team,toonIds))
            
            for toonId in toonIds:
                self.notify.debug("removing toon %s" % toonId)
                self._removeToonFromTeam(toonId, team)
                
                self.notify.debug("self.toonIds[team] is now %s" % self.toonIds[team])
        
        self.d_broadcastSetToonsPlaying()
    
    def balanceTeams(self):
        """
        Makes the teams roughly have the same number of toons.
        """
        # We assume that the left team is smaller, but later make the correction
        smallerTeam = PartyGlobals.TeamActivityTeams.LeftTeam
        largerTeam = PartyGlobals.TeamActivityTeams.RightTeam
        
        # If number of players in one team vs the other is more than 1
        if abs(len(self.toonIds[smallerTeam]) - len(self.toonIds[largerTeam])) > 1:
            # We make the correction to the assumption about the smaller team
            if len(self.toonIds[smallerTeam]) > len(self.toonIds[largerTeam]):
                smallerTeam = largerTeam
                largerTeam = 1 - smallerTeam
            
            shiftedToons = False
            # Keep putting toons in the other team until
            # the number of toons in the larger team is close to the other
            # could be the same or one larger depending on the difference
            while abs(len(self.toonIds[largerTeam]) - len(self.toonIds[smallerTeam])) > 1:
                toondId = self.toonIds[largerTeam].pop()
                self.toonIds[smallerTeam].append(toondId)
                self.toonIdsToTeams[toondId] = smallerTeam
                shiftedToons = True
                
                if self.isTeamFull(smallerTeam):
                    break
            
            # Finally send the new list out if any toons shifted teams
            if shiftedToons:
                self.d_broadcastSetToonsPlaying()
                
    def calcAdvantage(self):
        """
        Calculates the advantage factor based on the team size.
        For example, if a team has 3 players and the other has 4, then
        the advantage will be 4/3 (1.333) for the smaller team over and 1
        for the larger team.
        """
        self.resetAdvantage() # For good measure
        
        smallerTeam = PartyGlobals.TeamActivityTeams.LeftTeam
        largerTeam = PartyGlobals.TeamActivityTeams.RightTeam
        
        if len(self.toonIds[smallerTeam]) == 0 or len(self.toonIds[largerTeam]) == 0:
            return
        
        # Find the actual large team
        if len(self.toonIds[smallerTeam]) > len(self.toonIds[largerTeam]):
            smallerTeam = largerTeam
            largerTeam = 1 - smallerTeam
        
            # Set the advantage
            self.advantage[smallerTeam] = len(self.toonIds[largerTeam]) / float(len(self.toonIds[smallerTeam]))
            self.notify.debug("Advantage set to %s" % self.advantage)
            
            # Send the advantage to members of the smaller team
            advantage = self.advantage[smallerTeam]
            
            for toonId in self.toonIds[smallerTeam]:
                self.d_sendSetAdvantageToAvatarId(toonId, advantage)
    
    def resetAdvantage(self):
        """Resets the advantage for both teams back to 1.0"""
        self.advantage = [1.0, 1.0] 
    
#===============================================================================
# Handlers
#===============================================================================
        
    def _handleUnexpectedToonExit(self, toonId):
        """
        Clean up after a toon that dropped.
        """
        self.notify.debug("_handleUnexpectedToonExit( toonId=%d )" % toonId)
        
        # do special responses based on game state
        state = self.activityFSM.getCurrentOrNextState()
        self.notify.debug("currentState = %s" % state)
        
        if state in ("WaitToStart", 'WaitForEnough'):
            # remove toonId from self.toonIds and update clients
            self._removeToonFromTeam(toonId, self.getTeam(toonId))
            self.d_broadcastSetToonsPlaying()
            
            if state != 'WaitForEnough':
                # revert to WaitForEnough if necessary
                if not self.hasEnoughPlayers():
                    self.activityFSM.request("WaitForEnough")
                    
        elif state in ("WaitClientsReady", "Active"):
            # To keep things simple the game will kick everyone out and reset
            # the game state.
            self._removeAllToons()
            self.activityFSM.request("WaitForEnough")
            
        elif state == "Conclusion":
            del self.toonIdsToJellybeanRewards[toonId]
            # remove toonId from self.toonIds and update clients
            self._removeToonFromTeam(toonId, self.getTeam(toonId))
            self.d_broadcastSetToonsPlaying()
            
#===============================================================================
# Distributed
#===============================================================================

    # broadcast required
    # this method is for the client-side dc method setPlayersPerTeam
    def getPlayersPerTeam(self):
        return self._minPlayersPerTeam, self._maxPlayersPerTeam
    
    # broadcast required
    def getDuration(self):
        return self._duration
    
    # broadcast required
    def getCanSwitchTeams(self):
        return self._canSwitchTeams
    
    # clsend airecv
    def toonJoinRequest(self, team):
        """
        A toon is requesting to play tug of war.
        
        Parameters:
          team: The team the toon is trying to join as a
                PartyGlobals.TeamActivityTeams value
        """        
        toonId = self.air.getAvatarIdFromSender()
        self.notify.debug("toonJoinRequest( toon = %s team=%s )" %(toonId, self.getTeamName(team)))
        
        # first make sure the toon is not in any activity
        if self.party.isInActivity(toonId):
            # decline the toon
            self.notify.warning("rejecting toon %d trying to join team %s, but is in some other activity" % (toonId, self.getTeamName(team)))
            self.sendToonJoinResponse(toonId, False, team)
            
            return        
        
        # check team size limits first
        if self.isTeamFull(team):
            # decline the toon
            self.sendToonJoinResponse(toonId, False, team, PartyGlobals.DenialReasons.Full)
            
            return
        
        state = self.activityFSM.getCurrentOrNextState()
        self.notify.debug("toonJoinRequest state = " + state)
        
        if state == "WaitForEnough":
            # add the toon
            self.sendToonJoinResponse(toonId, True, team)
            
            # if we have enough players per team, request next state
            if self.hasEnoughPlayers():
                self.activityFSM.request("WaitToStart")
        elif state == "WaitToStart":
            self.sendToonJoinResponse(toonId, True, team)
        else:
            # decline the toon
            self.sendToonJoinResponse(toonId, False, team)
    
    def sendToonJoinResponse(self, toonId, joined, team, denialReason=PartyGlobals.DenialReasons.Default):
        """
        Broadcast to all clients whether or not this toonId has joined the
        activity.
        
        Parameters:
            toonId- doId of the avatar that is being accepted/rejected
            joined- True if the avatar joined this activity, False otherwise
            team- which team the toon joined, as a PartyGlobals.TeamActivityTeams
                  value
            denialReason- if the toon is being denied, the reason why
        """
        # we purposely do not call the base class version as we track toons in
        # this activity ourselves
        if joined:
            self._addToonToTeam(toonId, team)
            self.d_broadcastSetToonsPlaying()
        else:
            self.sendUpdateToAvatarId(toonId, "joinRequestDenied", [denialReason])
        
        
    # clsend airecv
    def toonExitRequest(self, team):
        """
        Clients call this over the wire when they want to exit this
        activity, but need AI server permission to do so.
        
        Parameters:
            team- which team the toon is on, as a PartyGlobals.TeamActivityTeams
                  value
        """
        # allow toons to leave if the activity is waiting for enough players or
        # waiting to start
        self.notify.debug("toonExitRequest( team=%s )" % self.getTeamName(team))
        
        toonId = self.air.getAvatarIdFromSender()
        state = self.activityFSM.getCurrentOrNextState()
        
        if state == "WaitForEnough":
            # allow the toon to exit
            self.sendToonExitResponse(toonId, True, team)
        elif state == "WaitToStart":
            # allow the toon to exit
            self.sendToonExitResponse(toonId, True, team)
            
            # revert to WaitForEnough if necessary
            if not self.hasEnoughPlayers():
                self.activityFSM.request("WaitForEnough")
        else:
            # decline the toon
            self.sendToonExitResponse(toonId, False, team)    
    
    def sendToonExitResponse(self, toonId, exited, team, denialReason=PartyGlobals.DenialReasons.Default):
        """
        Broadcast to all clients whether or not this toonId has left the activity.
        Subclasses should call this in response to recieving a toonExitRequest
        call.
        Parameters:
            toonId- id of the avatar that made the request to exit
            exited- True if the avatar exited this activity, False otherwise
        """
        self.notify.debug("sendToonExitResponse(toonId=%s, exited=%s, team=%s)"%(toonId, bool(exited), self.getTeamName(team)))
        
        if exited:
            self._removeToonFromTeam(toonId, team)
            self.d_broadcastSetToonsPlaying()
        else:
            self.sendUpdateToAvatarId(toonId, "exitRequestDenied", [denialReason])
    
    # clsend airecv
    def toonSwitchTeamRequest(self):
        senderId = self.air.getAvatarIdFromSender()
        state = self.activityFSM.getCurrentOrNextState()
        
        if not self._canSwitchTeams:
            self.writeServerEvent(
                'suspicious',
                senderId,
                "Trying to switch teams when the team activity does not allow it.")
            return
        
        team = self.getTeam(senderId)
        if team is None: # Might have exited at this point
            return 
        
        # Only allow switching before the activity starts
        if state != "WaitForEnough" and state != "WaitToStart":
            self.d_sendSwitchTeamRequestDeniedToAvatarId(senderId, PartyGlobals.DenialReasons.Default)
            return
        
        otherTeam = 1 - team
            
        if not self.isTeamFull(otherTeam):
            self.toonIds[team].remove(senderId)
            self.toonIds[otherTeam].append(senderId)
            self.toonIdsToTeams[senderId] = otherTeam
            
            self.d_broadcastSetToonsPlaying()
            
            # Check whether we need to change states at this point
            # Depending if the conditions (like if auto balance is on) for this activity there
            # may be enough players to start, or not enough.
            if state == "WaitForEnough" and self.hasEnoughPlayers():
                self.activityFSM.request("WaitToStart")
            elif state == "WaitToStart" and not self.hasEnoughPlayers():
                self.activityFSM.request("WaitForEnough")
        else:
            self.d_sendSwitchTeamRequestDeniedToAvatarId(senderId, PartyGlobals.DenialReasons.Full)
        
        
    # ai to avatar
    def d_sendSwitchTeamRequestDeniedToAvatarId(self, avId, reason):
        self.sendUpdateToAvatarId(
            avId,
            "switchTeamRequestDenied",
            [reason]
            )
    
    # airecv clsend
    def toonReady(self):
        """
        Clients call this over the wire when they are done reading the rules
        and are ready to play the activity.
        """
        self.notify.debug("toonReady")
        
        toonId = self.air.getAvatarIdFromSender()
        state = self.activityFSM.getCurrentOrNextState()
        
        if state != "WaitClientsReady":
            self.notify.warning("Got an unexpected toonReady from toonId=%s while in state %s." % (toonId, state))
        elif not self.isToonPlaying(toonId):
            self.notify.warning("Got an unexpected toonReady from toonId=%s that is not currently in this activity." % toonId)
        else:
            # update set of ready toons
            self.readyToonIds.add(toonId)
            
            # if we've gotten enough readies, then move on to next state
            if len(self.readyToonIds) == self.getNumToonsPlaying():
                self.activityFSM.request("Active")
            
            return True
        
        return False
    
    
    # broadcast ram
    def d_broadcastSetState(self, stateName, timestamp=0, data=0):
        self.sendUpdate("setState", [stateName, timestamp, data])
        
        
    # required broadcast ram
    def d_broadcastSetToonsPlaying(self):
        self.sendUpdate("setToonsPlaying", [self.toonIds[0], self.toonIds[1]])

        
    def d_sendSetAdvantageToAvatarId(self, toonId, advantage):
        self.sendUpdateToAvatarId(toonId, "setAdvantage", [advantage])

    
#===============================================================================
# FSM
#===============================================================================

    def isState(self, state):
        """
        Checks what the current state of the activity is right now.
        
        Parameters
            state is what state we're checking for
            
        Returns
            true if the current or next state matches the state we're checking for
        """
        return self.activityFSM.getCurrentOrNextState() == state
    
    def __delayedStateRequest(self, nextState):
        self.activityFSM.request(nextState)
        
    def requestLater(self, stateName, delay, delayName):
        """
        Schedule a do method later that requests a state change.
        """
        self.cleanupRequestLater()
        
        self._srTask = taskMgr.doMethodLater(
            delay,
            self.__delayedStateRequest,
            self.taskName(delayName),
            extraArgs=[stateName],
            )
        
    def cleanupRequestLater(self):
        """
        Cancels or cleans up the do method later that would request a state change.
        """
        if self._srTask is not None:
            taskMgr.remove(self._srTask)
            self._srTask = None
        
    def startWaitForEnough(self):
        """
        Wait for for the minimum number players to join the activity.
        """
        self.notify.debug("startWaitForEnough")
        
        # put clients into this state
        self.d_broadcastSetState("WaitForEnough")
    
    def finishWaitForEnough(self):
        """
        There are enough players in the activity to start.
        Transitioning to WaitToStart.
        """
        self.notify.debug("finishWaitForEnough")
        
        
    def startWaitToStart(self):
        """
        Enough players are in.
        
        Wait a few seconds before the activity begins to let more players
        come in and participate.
        """
        self.notify.debug("startWaitToStart")
        
        if self._shouldCalcAdvantage:
            self.resetAdvantage()
            
        # put clients into this state
        self.d_broadcastSetState(
                "WaitToStart", 
                timestamp=ClockDelta.globalClockDelta.getRealNetworkTime()
                )
        
        # start the game after a fixed amount of time
        self.requestLater("WaitClientsReady", self._startDelay, "waitToStartTimer")
    
    def finishWaitToStart(self):
        """
        The wait time is over and now we're displaying the rules on the clients and
        waiting until everyone reads the rules.
        
        Or we're below the number of toons required for the activity,
        so we go back to the WaitForEnough state.
        """
        self.notify.debug("finishWaitToStart")
        
        self.cleanupRequestLater()
        
        
    def startWaitClientsReady(self):
        """
        In the clients with toons participating in this activity, we are
        displaying the rules, and we are waiting for all toons to read them
        before starting the activity.
        """
        self.notify.debug("startWaitClientsReady")
       
        self.readyToonIds.clear() # reset the list of ready toons
        
        if self._shouldBalanceTeams:
            self.balanceTeams()
        
        # put clients into new state
        self.d_broadcastSetState("Rules")
        
    def finishWaitClientsReady(self):
        """
        All toons have read the rules, and we transition to the Active state.
        Or perhaps toons have dropped out of the activity and we're back to WaitForEnough.
        """
        self.notify.debug("finishWaitClientsReady")
        
        
    def startActive(self):
        """
        The activity begins, and lasts a certain amount of minutes before jumping
        to the Conclusion.
        """
        self.notify.debug("startActive")
        
        if self._shouldCalcAdvantage:
            self.calcAdvantage()
        
        # reset game variables
        self.toonIdsToJellybeanRewards.clear()
        
        # put clients into this state
        self.d_broadcastSetState(
            "Active",
            timestamp=ClockDelta.globalClockDelta.getRealNetworkTime()
            )
        
        # end the game after a fixed amount of time
        self.requestLater("Conclusion", self._duration, "gameTimer")
        
        
    def finishActive(self):
        """
        The activity successfully ended and we are going to the conclusion,
        or a participating toon dropped out of the activity and we are going
        back to WaitForEnough. 
        """
        self.notify.debug("finishActive")
        
        self.cleanupRequestLater()

        
    def startConclusion(self):
        """
        Calculates the results and sends them to the participating clients for display.
        Wait a number of seconds before transitioning out.
        """
        self.notify.debug("startConclusion")
        self.computeMatchResults()
        
        # put clients into this state
        self.d_broadcastSetState(
                "Conclusion", # new state
                data=self.getConclusionData()
                )
        
        # schedule to jump to next state
        self.requestLater("WaitForEnough", self._conclusionDuration, "rewardDuration")
    
    def finishConclusion(self):
        """
        Conclusion has ended and we're going back to WaitForEnough.
        """
        self.notify.debug("finishConclusion")
        
        self.cleanupRequestLater()
        
        for toonId, reward in self.toonIdsToJellybeanRewards.items():
            if reward > 0:
                self.sendUpdateToAvatarId(
                    toonId,
                    "showJellybeanReward", [
                    reward,
                    self.air.doId2do[toonId].getMoney(),
                    self.getJellybeanRewardMessage(toonId, reward)
                    ])
        
        # since we send the toon's current money in showJellybeanReward, that needs to happen before issueJellybeanRewards 
        self.issueJellybeanRewards()
        self._removeAllToons()
    
        
#===============================================================================
# Utility
#===============================================================================

    def getMaxPlayersPerTeam(self):
        """Returns the maximum number for players allowed per team"""
        return self._maxPlayersPerTeam
    
    def getMinPlayersPerTeam(self):
        """Returns the minimum number for players allowed per team"""
        return self._minPlayersPerTeam

    def getTeamName(self, team):
        """
        Parameters
            team is the team index (see PartyGlobals.TeamActivityTeams)
            
        Returns
            The team name
        """
        return PartyGlobals.TeamActivityTeams.getString(team)

    
    def isTeamFull(self, team):
        """
        Checks if a team is full.
        
        Parameters
            team is the team index (see PartyGlobals.TeamActivityTeams)
            
        Returns
            true if the one of the teams is full.
        """
        return (len(self.toonIds[team]) == self._maxPlayersPerTeam)

    
    def hasEnoughPlayers(self):
        """
        Checks to see if there are enough players to start a game.
        If the config variable party-allow-single-player-teams is set,
        then the test passes if there's a least one player on every team.
        
        Returns
            true if there are enough players for starting the game.
        """
        if self._allowSinglePlayer:
            return (len(self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]) >= 1 or
                len(self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam]) >= 1)
            
        elif self._shouldBalanceTeams:
            # This activity has enough players if the number of players on any side
            # is enough to create two teams.
            # The teams are balanced before right before the game starts.
            return (
                (len(self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]) +
                len(self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam])) >=
                (self._minPlayersPerTeam * 2)
                )

        return (len(self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]) >= self._minPlayersPerTeam and
                len(self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam]) >= self._minPlayersPerTeam) 

            
    def computeMatchResults(self):
        """
        Used to determine the Jellybean rewards. Varies per activity implementation.
        """
        pass


    def getToonsPlaying(self):
        """Returns a 2-dimensional list of Toon IDs in each team."""
        return [self.toonIds[0], self.toonIds[1]]
    
    
    def isInActivity(self, avId):
        """Return true if the avId is busy with us."""
        result = False
        
        for toonList in self.toonIds:
            if avId in toonList:
                result = True
                break
            
        return result

    
    def isToonPlaying(self, toonId):
        """Returns true if a toon is currently in the activity"""
        return (toonId in self.getToonIdsAsList())

    
    def getToonIdsAsList(self):
        """Returns a list of doId's of all toons in this activity."""
        return (self.toonIds[0] + self.toonIds[1])


    def getNumToonsPlaying(self):
        return (len(self.toonIds[0]) + len(self.toonIds[1]))

    
    def getTeam(self, toonId):
        """
        Utility function that returns the team toonId is on, as a 
        PartyGlobals.TeamActivityTeams value, or None if toonId isn't on either team.
        
        Returns
            team index or None
        """
        for i in range(len(PartyGlobals.TeamActivityTeams)):
            if self.toonIds[i].count(toonId) > 0:
                return i

        return None
    
    def getJellybeanRewardMessage(self, toonId, reward):
        """
        Returns the message that should be displayed when the game ends.
        This includes how many jellybeans they made
        """
        return TTLocalizer.PartyTeamActivityRewardMessage % reward
