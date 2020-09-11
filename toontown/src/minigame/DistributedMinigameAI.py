from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from toontown.ai.ToonBarrier import *
from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.shtiker import PurchaseManagerAI
from toontown.shtiker import NewbiePurchaseManagerAI
import MinigameCreatorAI
from direct.task import Task
import random
import MinigameGlobals
from direct.showbase import PythonUtil
import TravelGameGlobals
from toontown.toonbase import ToontownGlobals

# Codes to indicate avatar state
EXITED = 0
EXPECTED = 1
JOINED = 2
READY = 3

# Number of default points
DEFAULT_POINTS = 1
MAX_POINTS = 7

# allow some extra time for clients to load minigame assets
JOIN_TIMEOUT = 40. + MinigameGlobals.latencyTolerance
READY_TIMEOUT = (MinigameGlobals.MaxLoadTime +
                 MinigameGlobals.rulesDuration +
                 MinigameGlobals.latencyTolerance)
# Time to wait for avatars to exit
# NOTE: in some minigames this will include celebration time
EXIT_TIMEOUT = 20. + MinigameGlobals.latencyTolerance

class DistributedMinigameAI(DistributedObjectAI.DistributedObjectAI):

    """
    This is the base class for all Distributed Minigames on the AI.
    """

    # private so as not to conflict with subclass notify
    notify = directNotify.newCategory("DistributedMinigameAI")

    def __init__(self, air, minigameId):
        try:
            self.DistributedMinigameAI_initialized
        except:
            
            self.DistributedMinigameAI_initialized = 1

            DistributedObjectAI.DistributedObjectAI.__init__(self, air)

            self.minigameId = minigameId

            # prefix every state name with 'framework' to avoid naming overlaps
            # with minigame subclasses
            self.frameworkFSM = ClassicFSM.ClassicFSM(
                'DistributedMinigameAI',
                [State.State('frameworkOff',
                             self.enterFrameworkOff,
                             self.exitFrameworkOff,
                             ['frameworkWaitClientsJoin']),
                 State.State('frameworkWaitClientsJoin',
                             self.enterFrameworkWaitClientsJoin,
                             self.exitFrameworkWaitClientsJoin,
                             ['frameworkWaitClientsReady',
                              'frameworkWaitClientsExit',
                              'frameworkCleanup']),
                 State.State('frameworkWaitClientsReady',
                             self.enterFrameworkWaitClientsReady,
                             self.exitFrameworkWaitClientsReady,
                             ['frameworkGame',
                              'frameworkWaitClientsExit',
                              'frameworkCleanup']),
                 State.State('frameworkGame',
                             self.enterFrameworkGame,
                             self.exitFrameworkGame,
                             ['frameworkWaitClientsExit',
                              'frameworkCleanup']),
                 State.State('frameworkWaitClientsExit',
                             self.enterFrameworkWaitClientsExit,
                             self.exitFrameworkWaitClientsExit,
                             ['frameworkCleanup']),
                 State.State('frameworkCleanup',
                             self.enterFrameworkCleanup,
                             self.exitFrameworkCleanup,
                             ['frameworkOff']),
                 ],
                # Initial State
                'frameworkOff',
                # Final State
                'frameworkOff',
                )
            
            self.frameworkFSM.enterInitialState()

            # Actual avatars that will play the game
            self.avIdList = []

            self.stateDict = {}
            self.scoreDict = {}

            self.difficultyOverride  = None
            self.trolleyZoneOverride = None

            self.metagameRound = -1
            self.startingVotes = {} #the votes that carry over 

    def addChildGameFSM(self, gameFSM):
        """ inheritors should call this with their game ClassicFSM """
        self.frameworkFSM.getStateNamed('frameworkGame').addChild(gameFSM)

    def removeChildGameFSM(self, gameFSM):
        """ inheritors should call this with their game ClassicFSM """
        self.frameworkFSM.getStateNamed('frameworkGame').removeChild(gameFSM)

    def setExpectedAvatars(self, avIds):
        """
        Whoever created this minigame on the AI should call this to tell
        us who will be playing the game. The DistributedMinigameAI then
        waits to hear join messages from each of the avIds. Or instead
        of joining, we might hear an exitEvent instead.
        """
        assert len(avIds) > 0 and len(avIds) <= 4
        assert 0 not in avIds
        assert None not in avIds

        self.avIdList = avIds
        self.numPlayers = len(self.avIdList)
        self.notify.debug("BASE: setExpectedAvatars: expecting avatars: "
                          + str(self.avIdList))

    def setNewbieIds(self, newbieIds):
        """
        Minigame creator should call this to let us know which players
        are playing for the first time.
        """
        assert len(newbieIds) >= 0 and len(newbieIds) <= 4
        assert 0 not in newbieIds
        assert None not in newbieIds

        self.newbieIdList = newbieIds
        if len(self.newbieIdList) > 0:
            self.notify.debug('BASE: setNewbieIds: %s' % self.newbieIdList)

    def setTrolleyZone(self, trolleyZone):
        """
        This must be called before the object is generated
        trolleyZone is the zone that the toons were in before
        entering this minigame
        """
        self.trolleyZone = trolleyZone

    def setDifficultyOverrides(self, difficultyOverride, trolleyZoneOverride):
        """
        This must be called before the object is generated
        difficultyOverride is the difficulty value that should be used
        and sent to the clients
        trolleyZoneOverride is similar
        """
        self.difficultyOverride = difficultyOverride
        if self.difficultyOverride is not None:
            # modify difficultyOverride so that it will convert to an
            # integer and back without losing any precision
            self.difficultyOverride = (
                MinigameGlobals.QuantizeDifficultyOverride(difficultyOverride))
        self.trolleyZoneOverride = trolleyZoneOverride

    def setMetagameRound(self, roundNum):
        """
        -1 means it's a normal minigame
        any other number means its that round typically
        0 - travel game
        1 - minigame resulting from travel game
        2 - travel game
        3 - minigame resulting from travel game
        4 - travel game
        5 - minigame resulting from travel game
        """
        self.metagameRound = roundNum

    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        # kick off the ClassicFSM
        self.frameworkFSM.request('frameworkWaitClientsJoin')

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("BASE: delete: deleting AI minigame object")
        del self.frameworkFSM
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def isSinglePlayer(self):
        """
        returns nonzero if there is only one player
        """
        if self.numPlayers == 1:
            return 1
        else:
            return 0

    """
    def b_setParticipants(self, avIds):
        self.setParticipants(avIds)
        self.d_setParticipants(avIds)

    def d_setParticipants(self, avIds):
        self.notify.debug("BASE: Sending setParticipants")
        self.sendUpdate("setParticipants", [avIds])

    def setParticipants(self, avIds):
        self.notify.debug("BASE: setParticipants: game will be played by "
                          "these avatars: %s" % avIds)
    """

    def getParticipants(self):
        # getter for setParticipants
        # note that clients will not be able to access the avatars until
        # setGameReady() is called
        return self.avIdList

    def getTrolleyZone(self):
        # getter for setTrolleyZone
        return self.trolleyZone

    def getDifficultyOverrides(self):
        # getter for difficulty overrides
        response = [self.difficultyOverride,
                    self.trolleyZoneOverride]

        if response[0] is None:
            response[0] = MinigameGlobals.NoDifficultyOverride
        else:
            # convert the difficulty override to an integer so that
            # the AI and clients will have the exact same value
            response[0] *= MinigameGlobals.DifficultyOverrideMult
            response[0] = int(response[0])

        if response[1] is None:
            response[1] = MinigameGlobals.NoTrolleyZoneOverride
        return response

    def b_setGameReady(self):
        self.setGameReady()
        self.d_setGameReady()

    def d_setGameReady(self):
        self.notify.debug("BASE: Sending setGameReady")
        self.sendUpdate("setGameReady", [])

    def setGameReady(self):
        """
        This method gets called when all avatars have joined
        """
        self.notify.debug("BASE: setGameReady: game ready with avatars: %s" %
                          self.avIdList)

        self.normalExit = 1

    def b_setGameStart(self, timestamp):
        # send the distributed message first, so that any network msgs
        # sent by the subclass upon start of the game will arrive
        # after the game start msg
        self.d_setGameStart(timestamp)
        self.setGameStart(timestamp)

    def d_setGameStart(self, timestamp):
        self.notify.debug("BASE: Sending setGameStart")
        self.sendUpdate("setGameStart", [timestamp])

    def setGameStart(self, timestamp):
        """
        This method gets called when all avatars are ready
        Inheritors should call this plus the code to start the game
        """
        self.notify.debug("BASE: setGameStart")

    def b_setGameExit(self):
        self.d_setGameExit()
        self.setGameExit()

    def d_setGameExit(self):
        self.notify.debug("BASE: Sending setGameExit")
        self.sendUpdate("setGameExit", [])

    def setGameExit(self):
        """
        This method gets called when it's time for avatars to exit the game
        """
        self.notify.debug("BASE: setGameExit")

    def setGameAbort(self):
        """
        This gets called in the case of an unexpected abort
        If the minigame needs to do anything before we send the abort
        msg to the clients, override this func (but be sure to call
        this func on the base class)
        """
        self.notify.debug("BASE: setGameAbort")
        self.normalExit = 0
        self.sendUpdate("setGameAbort", [])
        # only transition to cleanup after we've sent the gameAbort msg
        self.frameworkFSM.request("frameworkCleanup")

    def handleExitedAvatar(self, avId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly.
        We have decided when this happens, we will just kill the
        minigame altogether
        """
        # TODO: what if they have all exited already?
        self.notify.warning("BASE: handleExitedAvatar: avatar id exited: " +
                            str(avId))
        self.stateDict[avId] = EXITED

        # Send the game exit update to kill the minigame and cause
        # all the clients to exit and cleanup
        self.setGameAbort()

    def gameOver(self):
        """
        Called by the subclass to indicate to the framework ClassicFSM
        that the game is over and the framework ClassicFSM should move ahead
        into cleanup state
        """
        self.notify.debug("BASE: gameOver")
        # wait for the clients to tell us they've exited
        self.frameworkFSM.request('frameworkWaitClientsExit')

    # Framework state machine functions

    def enterFrameworkOff(self):
        self.notify.debug("BASE: enterFrameworkOff")

    def exitFrameworkOff(self):
        pass

    def enterFrameworkWaitClientsJoin(self):
        """
        This state waits for all of the clients to join.
        see setAvatarJoined
        """
        self.notify.debug("BASE: enterFrameworkWaitClientsJoin")
        for avId in self.avIdList:
            self.stateDict[avId] = EXPECTED
            self.scoreDict[avId] = DEFAULT_POINTS
            # listen for this avatar's exit event
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            self.handleExitedAvatar, extraArgs=[avId])

        def allAvatarsJoined(self=self):
            self.notify.debug("BASE: all avatars joined")
            # Everybody is here, wait for them to read the rules
            self.b_setGameReady()
            # wait for clients to be ready
            self.frameworkFSM.request('frameworkWaitClientsReady')

        def handleTimeout(avIds, self=self):
            self.notify.debug("BASE: timed out waiting for clients %s "
                              "to join" % avIds)
            self.setGameAbort()

        self.__barrier = ToonBarrier(
            'waitClientsJoin',
            self.uniqueName('waitClientsJoin'),
            self.avIdList, JOIN_TIMEOUT,
            allAvatarsJoined, handleTimeout)

        # at this point, it's not possible for any avatars to have
        # already joined
        
    def setAvatarJoined(self):
        """
        This is a distributed update that gets called from the clients
        when this distributed object is created on their machine. Each time
        we hear that a single avatar has joined, we check to see if they
        have all joined.
        """
        # check to make sure this message is still relevant
        if (self.frameworkFSM.getCurrentState().getName() !=
            'frameworkWaitClientsJoin'):
            self.notify.debug("BASE: Ignoring setAvatarJoined message")
            return

        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("BASE: setAvatarJoined: avatar id joined: " +
                          str(avId))
        self.air.writeServerEvent('minigame_joined',avId,'%s|%s' % (self.minigameId, self.trolleyZone))
        self.stateDict[avId] = JOINED
        self.notify.debug("BASE: setAvatarJoined: new states: " +
                          str(self.stateDict))

        self.__barrier.clear(avId)

    def exitFrameworkWaitClientsJoin(self):
        self.__barrier.cleanup()
        del self.__barrier

    def enterFrameworkWaitClientsReady(self):
        """
        This state waits for all of the clients to be ready.
        see setAvatarReady
        """
        self.notify.debug("BASE: enterFrameworkWaitClientsReady")

        def allAvatarsReady(self=self):
            self.notify.debug("BASE: all avatars ready")
            # Everybody is here, start the game
            self.frameworkFSM.request('frameworkGame')

        def handleTimeout(avIds, self=self):
            self.notify.debug("BASE: timed out waiting for clients %s "
                              "to report 'ready'" % avIds)
            self.setGameAbort()

        self.__barrier = ToonBarrier(
            'waitClientsReady',
            self.uniqueName('waitClientsReady'),
            self.avIdList, READY_TIMEOUT,
            allAvatarsReady, handleTimeout)

        # some clients may already be ready
        for avId in self.stateDict.keys():
            if self.stateDict[avId] == READY:
                self.__barrier.clear(avId)

        self.notify.debug("  safezone: %s" % self.getSafezoneId())
        self.notify.debug("difficulty: %s" % self.getDifficulty())

    def setAvatarReady(self):
        """
        This is a distributed update that gets called from the clients
        when they are ready. Usually this means they have finished reading
        the rules panel. Each time we hear that a single avatar is ready,
        we check to see if they are all ready. If they are all ready, we
        send a setGameStart to actually start playing the minigame.
        """
        # check to make sure this message is still relevant
        # note that it's possible for one client to report 'joined' and
        # 'ready' before another client has even reported 'joined'
        if (self.frameworkFSM.getCurrentState().getName() not in
            ['frameworkWaitClientsReady', 'frameworkWaitClientsJoin']):
            self.notify.debug("BASE: Ignoring setAvatarReady message")
            return
        
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("BASE: setAvatarReady: avatar id ready: " +
                          str(avId))
        self.stateDict[avId] = READY
        self.notify.debug("BASE: setAvatarReady: new avId states: " +
                          str(self.stateDict))

        # if we're in the waitClientsReady state, update the barrier;
        # otherwise, just having set this avatar's stateDict entry is
        # sufficient (the barrier will be updated accordingly when we
        # enter the waitClientsReady state)
        if (self.frameworkFSM.getCurrentState().getName() ==
            'frameworkWaitClientsReady'):
            self.__barrier.clear(avId)

    def exitFrameworkWaitClientsReady(self):
        self.__barrier.cleanup()
        del self.__barrier

    def enterFrameworkGame(self):
        """
        The primary job of this state is to kick off the subclass
        gameFSM (which should be a child state machine of this state)
        """
        self.notify.debug("BASE: enterFrameworkGame")
        self.gameStartTime = globalClock.getRealTime()
        self.b_setGameStart(globalClockDelta.localToNetworkTime(\
                            self.gameStartTime))

    def exitFrameworkGame(self):
        pass

    def enterFrameworkWaitClientsExit(self):
        """
        this state waits for all of the clients to report that they
        have exited the minigame
        """
        self.notify.debug("BASE: enterFrameworkWaitClientsExit")
        # tell the clients to leave
        self.b_setGameExit()

        def allAvatarsExited(self=self):
            self.notify.debug("BASE: all avatars exited")
            # go to the cleanup state
            self.frameworkFSM.request('frameworkCleanup')

        def handleTimeout(avIds, self=self):
            """
            Well, we did not hear from all the clients that they exited, but
            it has been long enough. Go ahead and get out of here
            """
            self.notify.debug("BASE: timed out waiting for clients %s "
                              "to exit" % avIds)
            self.frameworkFSM.request('frameworkCleanup')

        # time out on waiting for clients to exit - then abort
        self.__barrier = ToonBarrier(
            'waitClientsExit',
            self.uniqueName('waitClientsExit'),
            self.avIdList, EXIT_TIMEOUT,
            allAvatarsExited, handleTimeout)

        # process any toons that have already exited
        for avId in self.stateDict.keys():
            if self.stateDict[avId] == EXITED:
                self.__barrier.clear(avId)

    def setAvatarExited(self):
        """
        This is a distributed update that gets called from the clients
        when they leave after the game is over
        """
        # check to make sure this message is still relevant
        if (self.frameworkFSM.getCurrentState().getName() !=
            'frameworkWaitClientsExit'):
            self.notify.debug("BASE: Ignoring setAvatarExit message")
            return
        
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("BASE: setAvatarExited: avatar id exited: " +
                          str(avId))
        self.stateDict[avId] = EXITED
        self.notify.debug("BASE: setAvatarExited: new avId states: " +
                          str(self.stateDict))

        self.__barrier.clear(avId)

    def exitFrameworkWaitClientsExit(self):
        self.__barrier.cleanup()
        del self.__barrier
        
    def hasScoreMult(self):
        return 1

    def enterFrameworkCleanup(self):
        self.notify.debug("BASE: enterFrameworkCleanup: normalExit=%s" %
                          self.normalExit)

        # scale the scores based on the neighborhood
        # use self.getSafezoneId to pick up debug overrides
        scoreMult = MinigameGlobals.getScoreMult(self.getSafezoneId())
        if not self.hasScoreMult():
            scoreMult = 1.0
        self.notify.debug('score multiplier: %s' % scoreMult)
        for avId in self.avIdList:
            assert avId not in [0, None]
            self.scoreDict[avId] *= scoreMult

        # create a score list that parallels the avIdList
        scoreList = []
        if not self.normalExit:
            # if game exited abnormally, pick a uniform number of points
            # for all toons
            randReward = random.randrange(DEFAULT_POINTS, MAX_POINTS+1)
        for avId in self.avIdList:
            assert avId not in [0, None]
            # put in some bogus points if we have requested abort
            if self.normalExit:
                score = int(self.scoreDict[avId]+.5)
                if score > 255:
                    self.notify.warning('avatar %s got %s jellybeans playing minigame %s in zone %s' %
                                        (avId,
                                         score,
                                         self.minigameId,
                                         self.getSafezoneId()))
                    score = 255
                elif score < 0:
                    # RAU just in case I miss something in ice game
                    score = 0
                scoreList.append(score)
            else:
                scoreList.append(randReward)

        # Delete yourself
        self.requestDelete()

        if self.metagameRound > -1:
            self.handleMetagamePurchaseManager(scoreList)
        else:
            self.handleRegularPurchaseManager(scoreList)

        self.frameworkFSM.request('frameworkOff')

    def handleMetagamePurchaseManager(self,scoreList):
        """
        metagame being played, handle play again and consider newbies
        """
        self.notify.debug('self.newbieIdList = %s' % self.newbieIdList)
        votesToUse = self.startingVotes
        
        if hasattr(self,'currentVotes'):
            votesToUse = self.currentVotes

        votesArray = []
        for avId in self.avIdList:
            if votesToUse.has_key(avId):
                votesArray.append(votesToUse[avId])
            else:
                self.notify.warning('votesToUse=%s does not have avId=%d' % (votesToUse,avId))
                votesArray.append(0)

        
        if self.metagameRound < TravelGameGlobals.FinalMetagameRoundIndex:
            newRound = self.metagameRound # let purchaseManager handle incrementing it

            # if this is not the travel game, add the beans we earned to the votes list
            # also make sure it's not the last game
            if not self.minigameId == ToontownGlobals.TravelGameId:
                for index in range(len(scoreList)):
                    votesArray[index] += scoreList[index]

            self.notify.debug('votesArray = %s' % votesArray)

            desiredNextGame = None
            if hasattr(self,'desiredNextGame'):
                desiredNextGame = self.desiredNextGame

            numToons = 0;
            lastAvId = 0
            for avId in self.avIdList:
                av = simbase.air.doId2do.get(avId)
                if av :
                    numToons +=1
                    lastAvId = avId
            doNewbie = False                    
            if numToons == 1 and lastAvId in self.newbieIdList:
                doNewbie = True

            if doNewbie:
                # newbie PM gets a single newbie, and we also give it the
                # list of all players; note that we don't give newbie PMs the
                # 'newbie list' -- that's only for the regular PM.
                pm = NewbiePurchaseManagerAI.NewbiePurchaseManagerAI(
                    self.air, lastAvId, self.avIdList, scoreList, self.minigameId,
                    self.trolleyZone)
                # We have no idea if the newbie PM is going to be around longer
                # than the 'regular' minigame->purchase->minigame... sequence.
                # We have to reference-count the zone. PMs decrement the zone
                # reference count when all participants leave to the playground.
                MinigameCreatorAI.acquireMinigameZone(self.zoneId)
                pm.generateWithRequired(self.zoneId)
            else:
                pm = PurchaseManagerAI.PurchaseManagerAI(
                    self.air, self.avIdList, scoreList, self.minigameId,
                    self.trolleyZone, self.newbieIdList, votesArray, newRound,
                    desiredNextGame)
                pm.generateWithRequired(self.zoneId)
        else:
            # this is the last minigame, handle newbies. and playAgain
            # also for now weare doing a regular minigame if only 1 person
            # presses play again, 
            self.notify.debug('last minigame, handling newbies')
            
            # create separate NewbiePurchaseManagerAIs for the noobs
            for id in self.newbieIdList:
                # newbie PM gets a single newbie, and we also give it the
                # list of all players; note that we don't give newbie PMs the
                # 'newbie list' -- that's only for the regular PM.
                pm = NewbiePurchaseManagerAI.NewbiePurchaseManagerAI(
                    self.air, id, self.avIdList, scoreList, self.minigameId,
                    self.trolleyZone)
                # We have no idea if the newbie PM is going to be around longer
                # than the 'regular' minigame->purchase->minigame... sequence.
                # We have to reference-count the zone. PMs decrement the zone
                # reference count when all participants leave to the playground.
                MinigameCreatorAI.acquireMinigameZone(self.zoneId)
                pm.generateWithRequired(self.zoneId)

            if len(self.avIdList) > len(self.newbieIdList):
                # Create a PurchaseManager
                pm = PurchaseManagerAI.PurchaseManagerAI(
                    self.air, self.avIdList, scoreList, self.minigameId,
                    self.trolleyZone, self.newbieIdList,
                    votesArray = votesArray,
                    metagameRound = self.metagameRound)
                pm.generateWithRequired(self.zoneId)
            
        
        
    def handleRegularPurchaseManager(self, scoreList):
        """
        regular minigame, handle purchase manager stuff
        """
        # create separate NewbiePurchaseManagerAIs for the noobs
        for id in self.newbieIdList:
            # newbie PM gets a single newbie, and we also give it the
            # list of all players; note that we don't give newbie PMs the
            # 'newbie list' -- that's only for the regular PM.
            pm = NewbiePurchaseManagerAI.NewbiePurchaseManagerAI(
                self.air, id, self.avIdList, scoreList, self.minigameId,
                self.trolleyZone)
            # We have no idea if the newbie PM is going to be around longer
            # than the 'regular' minigame->purchase->minigame... sequence.
            # We have to reference-count the zone. PMs decrement the zone
            # reference count when all participants leave to the playground.
            MinigameCreatorAI.acquireMinigameZone(self.zoneId)
            pm.generateWithRequired(self.zoneId)

        if len(self.avIdList) > len(self.newbieIdList):
            # Create a PurchaseManager
            pm = PurchaseManagerAI.PurchaseManagerAI(
                self.air, self.avIdList, scoreList, self.minigameId,
                self.trolleyZone, self.newbieIdList)
            pm.generateWithRequired(self.zoneId)


    def exitFrameworkCleanup(self):
        pass

    def requestExit(self):
        """
        This is a handler for debugging... it lets players request an
        immediate end to the minigame.
        """
        self.notify.debug(
            "BASE: requestExit: client has requested the game to end")
        self.setGameAbort()

    # time-related utility functions
    def local2GameTime(self, timestamp):
        """
        given a local-time timestamp, returns the corresponding
        timestamp relative to the start of the game
        """
        return timestamp - self.gameStartTime

    def game2LocalTime(self, timestamp):
        """
        given a game-time timestamp, returns the corresponding
        local timestamp
        """
        return timestamp + self.gameStartTime

    def getCurrentGameTime(self):
        return self.local2GameTime(globalClock.getFrameTime())

    # difficulty-related utility functions
    def getDifficulty(self):
        """ returns 0..1 """
        if self.difficultyOverride is not None:
            return self.difficultyOverride
        if hasattr(self.air, 'minigameDifficulty'):
            return float(self.air.minigameDifficulty)
        return MinigameGlobals.getDifficulty(self.getSafezoneId())

    def getSafezoneId(self):
        """
        returns 1000-multiple safezone zoneId;
        can be matched to safezone IDs in ToontownGlobals.py
        """
        if self.trolleyZoneOverride is not None:
            return self.trolleyZoneOverride
        if hasattr(self.air, 'minigameSafezoneId'):
            return MinigameGlobals.getSafezoneId(self.air.minigameSafezoneId)
        return MinigameGlobals.getSafezoneId(self.trolleyZone)

    def logPerfectGame(self, avId):
        """ records the fact that this avatar had a perfect game """
        self.air.writeServerEvent('perfectMinigame',
                                  avId, '%s|%s|%s' % (
            self.minigameId, self.trolleyZone, self.avIdList))

    def logAllPerfect(self):
        """ records a perfect game for all participants """
        for avId in self.avIdList:
            self.logPerfectGame(avId)

    def getStartingVotes(self):
        """
        make sure we return it in the same order as avIdList
        """
        retval = []
        for avId in self.avIdList:
            if self.startingVotes.has_key(avId):
                retval.append( self.startingVotes[avId])
            else:
                self.notify.warning('how did this happen? avId=%d not in startingVotes %s' %
                                    (avId, self.startingVotes))
                retval.append(0)
        return retval

    def setStartingVote(self, avId, startingVote):
        self.startingVotes[avId] = startingVote
        self.notify.debug('setting starting vote of avId=%d to %d' % (avId,startingVote))

    def getMetagameRound(self):
        return self.metagameRound
