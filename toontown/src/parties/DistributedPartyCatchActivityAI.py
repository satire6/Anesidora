#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: The Party Catch Activity is like the trolley catch activity, only
#          party-wide.  Toons not in an activity when the lever is pulled are
#          put in this activity and anyone can join in/leave.  Fruit falls
#          beneath the party tree.
#-------------------------------------------------------------------------------
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.parties import PartyGlobals
from toontown.ai.ToonBarrier import ToonBarrier
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.DistributedPartyCatchActivityBase import DistributedPartyCatchActivityBase
from toontown.parties.activityFSMs import CatchActivityFSM

class DistributedPartyCatchActivityAI(DistributedPartyActivityAI, DistributedPartyCatchActivityBase):
    # Notify category for Distributed Party Activitys
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCatchActivityAI")

    class Generation:
        def __init__(self, generation, startTime, numPlayers):
            self.generation = generation
            self.startTime = startTime
            self.numPlayers = numPlayers
            self.caughtList = [0,] * 20

    def __init__(self, air, partyDoId, x, y, h):
        DistributedPartyActivityAI.__init__(self, air, partyDoId, x, y, h, PartyGlobals.ActivityIds.PartyCatch, PartyGlobals.ActivityTypes.HostInitiated)
        self.toonIdsToScores = {}
        # create state machine and set initial state
        self.activityFSM = CatchActivityFSM(self)

    def getStartTimestamp(self):
        return 0

    def getGenerations(self):
        return []

    def generate(self):
        DistributedPartyActivityAI.generate(self)
        self._partyEndedEvent = self.air.partyManager.getPartyEndedEvent(self.party.partyInfo.hostId)
        self.accept(self._partyEndedEvent, self._handlePartyEnded)
        self.conclusionCountdownTask = self.uniqueName("PartyCatchConclusionCountdownTask")
        self.conclusionFinishTask = self.uniqueName("PartyCatchConclusionFinishTask")
        self.activityFSM.request("Idle")
        # game is always running
        self.activityFSM.request("Active")

    def delete(self):
        DistributedPartyCatchActivityAI.notify.debug("delete")
        taskMgr.remove(self.conclusionCountdownTask)
        taskMgr.remove(self.conclusionFinishTask)
        del self.activityFSM
        self.ignore(self._partyEndedEvent)
        DistributedPartyActivityAI.delete(self)

    def _handlePartyEnded(self):
        # since this activity lasts for the entire party, end the activity when the party ends
        # (don't wait until players get kicked out of the party)
        # make sure everyone gets their reward
        for toonId, reward in self.toonIdsToScores.items():
            reward = self.toonIdsToScores[toonId]
            if reward > PartyGlobals.CatchMaxTotalReward:
                # put a cap so we don't go beyond something ridiculous
                reward = PartyGlobals.CatchMaxTotalReward
                self.toonIdsToJellybeanRewards[toonId]  = reward
            self.sendUpdateToAvatarId(toonId, "showJellybeanReward", [
                reward, self.air.doId2do[toonId].getMoney(),
                TTLocalizer.PartyCatchRewardMessage %(self.toonIdsToScores[toonId],reward)])
            self.toonIdsToJellybeanRewards[toonId] = reward
            self.issueJellybeanRewardToToonId(toonId)
        self.removeAllToons()
        self.requestState('Conclusion')

    def _setUpNextGenScheduleTask(self, startT, delay=None):
        if delay is None:
            delay = 0.
        nextGen = self._generation + 1
        task = taskMgr.doMethodLater(
            delay, Functor(self._scheduleNextGeneration, startT),
            'schedNextGen-%s-%s' % (self.doId, nextGen))
        # cancel any pending generations that start after this one
        for gen, item in self._schedTasks.items():
            if item[0] > self._lastGenerationStartTime:
                taskMgr.remove(item[1])
            del self._schedTasks[gen]
        self._schedTasks[nextGen] = (startT, task)

    def getNumPlayers(self):
        return len(self._playerIds)

    def _scheduleNextGeneration(self, startT, task=None):
        # prune out generations that are expired
        tCutoff = (globalClock.getFrameTime() - self.activityStartTime) - self.generationDuration
        # add a minute of wiggle room for laggy client connections
        tCutoff -= 60.
        genIndices = self._id2gen.keys()
        genIndices.sort()
        for genIndex in genIndices:
            timestamp = self._id2gen[genIndex].startTime
            if timestamp <= tCutoff:
                del self._id2gen[genIndex]

        self.calcDifficultyConstants(self.getNumPlayers())

        # try to avoid exploits and griefing by timing this generation relative to the
        # previous generation
        timeDelta = startT - self._lastGenerationStartTime
        quantizedTimeDelta = int(timeDelta / self.DropPeriod) * self.DropPeriod
        if quantizedTimeDelta < timeDelta:
            quantizedTimeDelta += self.DropPeriod
        if __dev__:
            assert quantizedTimeDelta >= timeDelta
        quantizedStartT = self._lastGenerationStartTime + quantizedTimeDelta

        self._generation += 1
        curGenStartTime = quantizedStartT

        self._id2gen[self._generation] = self.Generation(self._generation, curGenStartTime, self.getNumPlayers())
        self._lastGenerationStartTime = curGenStartTime

        # create the data list for the network
        generations = []
        genIndices = self._id2gen.keys()
        genIndices.sort()
        for genIndex in genIndices:
            timestamp = self._id2gen[genIndex].startTime + self.activityStartTime
            numPlayers = self._id2gen[genIndex].numPlayers
            generations.append([genIndex, globalClockDelta.localToNetworkTime(timestamp, bits=32), numPlayers])
        
        self.sendUpdate('setGenerations', [generations])

        nextStartT = curGenStartTime + self.generationDuration
        # sync up the generations relative to the game start time, to preserve the
        # drop frequency interest curve
        nextStartT = (nextStartT / PartyGlobals.CatchActivityDuration) * PartyGlobals.CatchActivityDuration
        delay = ((nextStartT + self.activityStartTime) - globalClock.getRealTime()) * .5
        delay = max(delay, 0.)
        self._genSchedTask = self._setUpNextGenScheduleTask(nextStartT, delay)

##     def requestActivityStart(self):
##         """
##         Called by the client when the host pulls the lever to start this game.
##         """
##         DistributedPartyCatchActivityAI.notify.debug("requestActivityStart")
##         senderId = self.air.getAvatarIdFromSender()
##         if self.activityFSM.state == "Idle":
##             self.activityFSM.request("Active")
##             self.sendUpdateToAvatarId(senderId, "startRequestResponse", [int(True)])
##         else:
##             self.sendUpdateToAvatarId(senderId, "startRequestResponse", [int(False)])

    # Distributed (clsend airecv)
    def toonJoinRequest(self):
        DistributedPartyCatchActivityAI.notify.debug("toonJoinRequest")
        senderId = self.air.getAvatarIdFromSender()
        inActivity = self.party.isInActivity(senderId)
        if inActivity:
            # AI side don't let a toon join multiple activities
            self.sendToonJoinResponse(senderId, joined=False)
            return
        self._playerIds.add(senderId)
        if self.activityFSM.state == "Idle":
            if senderId != self.party.partyInfo.hostId:
                self.air.writeServerEvent('suspicious', senderId, 'non-host trying to start party catch')
                return
            self.sendToonJoinResponse(senderId, joined=True)
            self.activityFSM.request("Active")
        elif self.activityFSM.state == "Active":
            # TODO: check against maximum number of players limit
            self.sendToonJoinResponse(senderId, joined=True)

    def toonExitDemand(self):
        DistributedPartyCatchActivityAI.notify.debug("toonJoinRequest")
        toonId = self.air.getAvatarIdFromSender()
        # make sure this toon is currently playing
        if toonId not in self.toonIds:
            return
        if toonId in self.toonIdsToScores:
            reward = self.toonIdsToScores[toonId]
            
            # if it's jelly bean day give us more jelly beans!
            if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_DAY):
                reward *= PartyGlobals.JellyBeanDayMultiplier
            
            if reward > PartyGlobals.CatchMaxTotalReward:
                # put a cap so we don't go beyond something ridiculous
                reward = PartyGlobals.CatchMaxTotalReward
                self.toonIdsToJellybeanRewards[toonId]  = reward
            self.sendUpdateToAvatarId(toonId, "showJellybeanReward", [
                reward, self.air.doId2do[toonId].getMoney(),
                TTLocalizer.PartyCatchRewardMessage %(self.toonIdsToScores[toonId],reward)])
            del self.toonIdsToScores[toonId]
            self.toonIdsToJellybeanRewards[toonId] = reward
            self.issueJellybeanRewardToToonId(toonId)
        DistributedPartyActivityAI.toonExitDemand(self)
        if toonId in self._playerIds:
            self._playerIds.remove(toonId)
        # number of players changed, start a new generation of drops
        self._setUpNextGenScheduleTask(globalClock.getRealTime() - self.activityStartTime)

    def sendToonJoinResponse(self, toonId, joined):
        # since toons can join mid-activity, make sure to add to scores dictionary if needed
        if joined:
            if not self.toonIdsToScores.has_key(toonId): 
                self.toonIdsToScores[toonId] = 0
        DistributedPartyActivityAI.sendToonJoinResponse(self, toonId, joined)
        # number of players changed, start a new generation of drops
        self._setUpNextGenScheduleTask(globalClock.getRealTime() - self.activityStartTime)

    def _handleUnexpectedToonExit(self, toonId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly.
        """
        DistributedPartyCatchActivityAI.notify.debug("_handleUnexpectedToonExit( toonId=%s )" % toonId)
        DistributedPartyActivityAI._handleUnexpectedToonExit(self, toonId)
        if toonId in self._playerIds:
            self._playerIds.remove(toonId)
        if self.toonIdsToScores.has_key(toonId):
            del self.toonIdsToScores[toonId]
        # number of players changed, start a new generation of drops
        self._setUpNextGenScheduleTask(globalClock.getRealTime() - self.activityStartTime)

    # Distributed (clsend airecv)
    def claimCatch(self, generation, objNum, DropObjTypeId):
        if self.activityFSM.state != 'Active':
            return

        # range check DropObjTypeId
        if DropObjTypeId < 0 or DropObjTypeId >= len(PartyGlobals.DOTypeId2Name):
            self.air.writeServerEvent('warning', DropObjTypeId, 'PartyCatchActivityAI.claimCatch DropObjTypeId out of range')
            return

        gen = self._id2gen.get(generation)
        if gen is None:
            # generation doesn't exist yet (?) or has been deprecated
            self.air.writeServerEvent('warning', generation, 'PartyCatchActivityAI.claimCatch generation is too old or doesn\'t exist yet')
            return

        # sanity check; don't allow hackers to allocate unlimited memory
        if objNum < 0 or objNum > 5000 or objNum >= 2*len(gen.caughtList):
            # DistributedPartyCatchActivityAI.notify.debug('object num %s is too high. ignoring' % objNum)
            self.air.writeServerEvent('warning', objNum, 'PartyCatchActivityAI.claimCatch objNum is too high or negative')
            return

        # double the size of the caught table as needed
        if objNum >= len(gen.caughtList):
            gen.caughtList += [0] * len(gen.caughtList)

        # if nobody's caught this object yet, announce that it's been caught
        if not gen.caughtList[objNum]:
            avId = self.air.getAvatarIdFromSender()
            # make sure this toon is still playing
            if avId not in self._playerIds:
                return
            gen.caughtList[objNum] = 1
            self.sendUpdate('setObjectCaught', [avId, generation, objNum])
            # if it's a good obj, update the score
            objName = PartyGlobals.DOTypeId2Name[DropObjTypeId]
            DistributedPartyCatchActivityAI.notify.debug('avatar %s caught object %s: %s' %
                              (avId, objNum, objName))
            if PartyGlobals.Name2DropObjectType[objName].good:
                self.toonIdsToScores[avId] += 1
                self.fruitsCaught += 1

#    def reportDone(self):
#        if self.activityFSM.state != 'Active':
#            return
#        avId = self.air.getAvatarIdFromSender()
#        # all of the objects on this avatar's client have landed
#        # or been caught
#        DistributedPartyCatchActivityAI.notify.debug('reportDone: avatar %s is done' % avId)

    # FSM transition methods
    def startIdle(self):
        DistributedPartyCatchActivityAI.notify.debug("startIdle")
        self.sendUpdate(
            "setState",
            [
                "Idle", # new state
                0,
            ]
        )
    
    def finishIdle(self):
        DistributedPartyCatchActivityAI.notify.debug("finishIdle")
        
    def startActive(self):
        DistributedPartyCatchActivityAI.notify.debug("startActive")
        self.activityStartTime = globalClock.getRealTime()
        self.sendUpdate('setStartTimestamp', [
            globalClockDelta.localToNetworkTime(self.activityStartTime, bits=32),])
        self.sendUpdate(
            "setState",
            [
                "Active", # new state
                globalClockDelta.localToNetworkTime(self.activityStartTime),
            ]
        )
        # populate the scores dictionary
        self.toonIdsToScores.clear()
        for toonId in self.toonIds:
            self.toonIdsToScores[toonId] = 0
        # and keep track of how many are caught
        self.fruitsCaught = 0
        # game is always running
        #taskMgr.doMethodLater(PartyGlobals.CatchActivityDuration, self.requestState, self.conclusionCountdownTask, ["Conclusion"])
        self._playerIds = set()
        # defines self.generationDuration
        self.calcDifficultyConstants(self.getNumPlayers())
        self._id2gen = {}
        self._generation = -1
        self._lastGenerationStartTime = -self.generationDuration
        self._schedTasks = {}
        self._setUpNextGenScheduleTask(0.)

    def requestState(self, state):
        DistributedPartyCatchActivityAI.notify.debug("requestState : %s" % state)
        self.activityFSM.request(state)

    def finishActive(self):
        DistributedPartyCatchActivityAI.notify.debug("finishActive")

    def startConclusion(self):
        DistributedPartyCatchActivityAI.notify.debug("startIdle")
        self.sendUpdate(
            "setState",
            [
                "Conclusion", # new state
                0,
            ]
        )
    
    def finishConclusion(self):
        DistributedPartyCatchActivityAI.notify.debug("finishIdle")

    def isInActivity(self, toonId):
        """Return true if the toon is doing catch."""
        result = False
        if toonId in self._playerIds:
            result = True
        if result:
            # lets do a validation check here
            # they should be in sync
            if not toonId in self.toonIdsToScores:
                self.notify.warning("toon %d is in playerIds but not in toonIdsToScores" % toonId)
        return result
