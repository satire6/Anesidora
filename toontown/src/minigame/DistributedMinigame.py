
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import MinigameRulesPanel
from direct.task.Task import Task
from toontown.toon import Toon
from direct.showbase import RandomNumGen
from toontown.toonbase import TTLocalizer
import random
import MinigameGlobals
from direct.showbase import PythonUtil
from toontown.toon import TTEmote
from otp.avatar import Emote

class DistributedMinigame(DistributedObject.DistributedObject):
    """
    This is the base class for Distributed Minigame objects on the
    client.
    """

    # Notify category for Distributed Minigames
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMinigame")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.waitingStartLabel = DirectLabel(
            text = TTLocalizer.MinigameWaitingForOtherPlayers,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.6, 0, -0.75),
            scale = 0.075)   
        self.waitingStartLabel.hide()

        # Initialize the avIdList to an empty list in case
        # we get booted before the avatars are ready
        self.avIdList = []

        self.remoteAvIdList = []

        self.localAvId = base.localAvatar.doId

        # This is the framework finite state machine that takes care
        # of all the business of joining avatars. When this fsm enters
        # the game state, the actual minigame will usually have a child
        # fsm that plays the actual game
        # prefix every state name with 'framework' to avoid naming overlaps
        # with minigame subclasses
        self.frameworkFSM = ClassicFSM.ClassicFSM(
            'DistributedMinigame',
            [State.State('frameworkInit',
                         self.enterFrameworkInit,
                         self.exitFrameworkInit,
                         ['frameworkRules',
                          'frameworkCleanup',
                          'frameworkAvatarExited',
                          ]),
             State.State('frameworkRules',
                         self.enterFrameworkRules,
                         self.exitFrameworkRules,
                         ['frameworkWaitServerStart',
                          'frameworkCleanup',
                          'frameworkAvatarExited',
                          ]),
             State.State('frameworkWaitServerStart',
                         self.enterFrameworkWaitServerStart,
                         self.exitFrameworkWaitServerStart,
                         ['frameworkGame',
                          'frameworkCleanup',
                          'frameworkAvatarExited',
                          ]),
             State.State('frameworkGame',
                         self.enterFrameworkGame,
                         self.exitFrameworkGame,
                         ['frameworkWaitServerFinish',
                          'frameworkCleanup',
                          'frameworkAvatarExited',
                          ]),
             State.State('frameworkWaitServerFinish',
                         self.enterFrameworkWaitServerFinish,
                         self.exitFrameworkWaitServerFinish,
                         ['frameworkCleanup',
                          ]),
             State.State('frameworkAvatarExited',
                         self.enterFrameworkAvatarExited,
                         self.exitFrameworkAvatarExited,
                         ['frameworkCleanup',
                          ]),
             State.State('frameworkCleanup',
                         self.enterFrameworkCleanup,
                         self.exitFrameworkCleanup,
                         []),
             ],
            # Initial State
            'frameworkInit',
            # Final State
            # it's important for the final state to do cleanup;
            # on disconnect, the ClassicFSM will be forced into the
            # final state
            'frameworkCleanup',
            )

        # This fsm is actually a child of the hood fsm
        # Add us to the playGame hood state machine
        hoodMinigameState = self.cr.playGame.hood.fsm.getStateNamed("minigame")
        hoodMinigameState.addChild(self.frameworkFSM)

        # Play Game's minigame state data throws this when the local toon
        # is done reading the rules
        self.rulesDoneEvent = "rulesDone"

        # A hook for debugging, so we can exit minigames quickly
        self.acceptOnce("minigameAbort", self.d_requestExit)

        # put a reference to this game on base, for
        # easy debugging access
        base.curMinigame = self

        # for the load bar
        self.modelCount = 500

        self.cleanupActions = []

        # these are flags that the subclass can manipulate to keep
        # this base class from messing with the toons as the game
        # starts up; see setUsesSmoothing and setUsesLookAround below
        self.usesSmoothing = 0
        self.usesLookAround = 0

        # difficulty debug overrides
        self.difficultyOverride  = None
        self.trolleyZoneOverride = None

        self.hasLocalToon = 0

        # Go to initial state
        self.frameworkFSM.enterInitialState()

        #info needed for trolley metagame
        self.startingVotes = {}
        self.metagameRound = -1
        

    def addChildGameFSM(self, gameFSM):
        """ inheritors should call this with their game ClassicFSM """
        self.frameworkFSM.getStateNamed('frameworkGame').addChild(gameFSM)

    def removeChildGameFSM(self, gameFSM):
        """ inheritors should call this with their game ClassicFSM """
        self.frameworkFSM.getStateNamed('frameworkGame').removeChild(gameFSM)

    def setUsesSmoothing(self):
        self.usesSmoothing = 1
    def setUsesLookAround(self):
        self.usesLookAround = 1

    def getTitle(self):
        """
        Return the title of the minigame.
        Subclasses should redefine. 
        """
        return TTLocalizer.DefaultMinigameTitle

    def getInstructions(self):
        """
        Return the instructions for the minigame.
        Subclasses should redefine.
        """
        return TTLocalizer.DefaultMinigameInstructions

    def getMaxDuration(self):
        """
        subclasses should redefine and return their maximum duration
        in seconds (this is for debugging)
        NOTE: do not include time for reading the instructions
        """
        raise Exception('Minigame implementer: '
                        'you must override getMaxDuration()')

    def __createRandomNumGen(self):
        self.notify.debug("BASE: self.doId=0x%08X" % self.doId)
        # seed the random number generator with the minigame doId
        self.randomNumGen = RandomNumGen.RandomNumGen(self.doId)
        def destroy(self=self):
            self.notify.debug("BASE: destroying random num gen")
            del self.randomNumGen
        self.cleanupActions.append(destroy)

    def generate(self):
        # When this DistributedMinigame is created on the client,
        # the localtoon sends an update to join the minigame
        self.notify.debug("BASE: generate, %s" % self.getTitle())
        DistributedObject.DistributedObject.generate(self)

        self.__createRandomNumGen()

    def announceGenerate(self):
        """
        announceGenerate is called after all of the required fields are
        filled in
        """
        DistributedObject.DistributedObject.announceGenerate(self)
        
        if not self.hasLocalToon: return
        self.notify.debug("BASE: handleAnnounceGenerate: send setAvatarJoined")

        # every once in a while, do an explicit test of the connection
        # breaking just before we send the join msg
        # (at this point, we haven't gotten around to starting the
        # random-abort/disconnect/etc. doLaters)
        if base.randomMinigameNetworkPlugPull and random.random() < (1./25):
            print ('*** DOING RANDOM MINIGAME NETWORK-PLUG-PULL '
                   'BEFORE SENDING setAvatarJoined ***')
            base.cr.pullNetworkPlug()

        # Update the minigame AI to join our local toon doId
        self.sendUpdate("setAvatarJoined", [])

        # if this flag is set to zero, we won't notify the server that
        # we've left at the end of the game
        self.normalExit = 1

        count = self.modelCount
        loader.beginBulkLoad("minigame",
                             (TTLocalizer.HeadingToMinigameTitle % self.getTitle()), count,
                             1, TTLocalizer.TIP_MINIGAME)
        self.load()
        loader.endBulkLoad("minigame")

        # we probably just spent a lot of time loading, so
        # tell globalClock to update the frame timestamp
        globalClock.syncFrameTime()

        # NOTE: if the minigame now spends a lot of time in onstage(),
        # it will eat into the rules-panel display time

        # bring up the lights
        self.onstage()

        def cleanup(self=self):
            self.notify.debug("BASE: cleanup: normalExit=%s" % self.normalExit)

            self.offstage()
            # make sure we clear the screen
            base.cr.renderFrame()
            
            # If we didn't abort, tell the AI we are exiting
            if self.normalExit:
                self.sendUpdate("setAvatarExited", [])

        self.cleanupActions.append(cleanup)

        # Show the rules
        # NOTE: parent ClassicFSM state has not yet been entered; it will
        # try to transition our ClassicFSM to the initial state. As long
        # as there is no rules->init transition defined, we're ok.
        # Ideally, we would wait for the parent state to enter our
        # initial state, and transition to 'rules' at that point.
        # The problem is that the parent state is only entered once
        # per trolley session, regardless of how many minigames
        # are played in that session.
        self.frameworkFSM.request("frameworkRules")

    def disable(self):
        self.notify.debug("BASE: disable")
        self.frameworkFSM.request('frameworkCleanup')
        taskMgr.remove(self.uniqueName('random-abort'))
        taskMgr.remove(self.uniqueName('random-disconnect'))
        taskMgr.remove(self.uniqueName('random-netplugpull'))
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.notify.debug("BASE: delete")
        if self.hasLocalToon:
            self.unload()
        # make sure we're not accepting any events
        self.ignoreAll()
        # Remove this state machine from Hood's state machine
        if self.cr.playGame.hood:
            # hood can become None when a trialer clicks subscribe now while playing
            # in a minigame
            hoodMinigameState = self.cr.playGame.hood.fsm.getStateNamed("minigame")
            hoodMinigameState.removeChild(self.frameworkFSM)
        self.waitingStartLabel.destroy()
        del self.waitingStartLabel
        del self.frameworkFSM
        DistributedObject.DistributedObject.delete(self)

    def load(self):
        self.notify.debug("BASE: load")
        Toon.loadMinigameAnims()

    def onstage(self):
        """
        Set the stage for the minigame. This usually includes parenting
        models to render, positioning the camera, starting the music, etc.
        Subclasses should override to do something meaningful for that game.
        """
        self.notify.debug("BASE: onstage")

        def calcMaxDuration(self=self):
            # try to make sure we cover the entire time range,
            # even if we overestimate
            return (self.getMaxDuration() + MinigameGlobals.rulesDuration) * 1.1

        # if we've simulated a network-plug-pull, don't bother setting
        # up any of these tests
        if not base.cr.networkPlugPulled():
            if base.randomMinigameAbort:
                maxDuration = calcMaxDuration()
                self.randomAbortDelay = random.random() * maxDuration
                taskMgr.doMethodLater(self.randomAbortDelay, self.doRandomAbort,
                                      self.uniqueName('random-abort'))

            if base.randomMinigameDisconnect:
                maxDuration = calcMaxDuration()
                self.randomDisconnectDelay = random.random() * maxDuration
                taskMgr.doMethodLater(self.randomDisconnectDelay,
                                      self.doRandomDisconnect,
                                      self.uniqueName('random-disconnect'))
                
            if base.randomMinigameNetworkPlugPull:
                maxDuration = calcMaxDuration()
                self.randomNetPlugPullDelay = random.random() * maxDuration
                taskMgr.doMethodLater(
                    self.randomNetPlugPullDelay,
                    self.doRandomNetworkPlugPull,
                    self.uniqueName('random-netplugpull'))

    def doRandomAbort(self, task):
        print ("*** DOING RANDOM MINIGAME ABORT AFTER %.2f SECONDS ***" %
               self.randomAbortDelay)
        self.d_requestExit()
        return Task.done

    def doRandomDisconnect(self, task):
        print ("*** DOING RANDOM MINIGAME DISCONNECT AFTER %.2f SECONDS ***" %
               self.randomDisconnectDelay)
        # this is a message that clients cannot send;
        # get booted off the server intentionally
        self.sendUpdate('setGameReady')
        return Task.done

    def doRandomNetworkPlugPull(self, task):
        print ('*** DOING RANDOM MINIGAME NETWORK-PLUG-PULL AFTER '
               '%.2f SECONDS ***' % self.randomNetPlugPullDelay)
        base.cr.pullNetworkPlug()
        return Task.done

    def offstage(self):
        """
        Clears the stage of the minigame. This usually includes parenting
        models to hidden, stopping the music, etc.
        Subclasses should override to do something meaningful for that game.
        """
        self.notify.debug("BASE: offstage")
        # make sure the avatars are hidden
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.detachNode()
        # distributed objects (like the tag game's treasures) that are
        # involved in a minigame should listen for this event, and hide
        # themselves when they get the event
        messenger.send('minigameOffstage')

    def unload(self):
        self.notify.debug("BASE: unload")
        if hasattr(base, 'curMinigame'):
            del base.curMinigame
        Toon.unloadMinigameAnims()

    def setParticipants(self, avIds):
        """
        called by the AI, this tells us the avatar ids of
        the avatars that will be in the game. NOTE: the avatar
        ids cannot be used to access the avatars until
        setGameReady() is called by the AI!

        This is a required field, so it will be called before the
        object is 'officially' created
        """
        self.avIdList = avIds
        self.numPlayers = len(self.avIdList)

        self.hasLocalToon = self.localAvId in self.avIdList
        if not self.hasLocalToon:
            self.notify.warning(
                "localToon (%s) not in list of minigame players: %s" %
                (self.localAvId, self.avIdList))
            return

        """
        if self.localAvId not in self.avIdList:
            self.notify.error(
                "localToon (%s) not in list of minigame players: %s" %
                (self.localAvId, self.avIdList))
                """

        self.notify.info("BASE: setParticipants: %s" % self.avIdList)

        # build the list of remote avatars
        self.remoteAvIdList = []
        for avId in self.avIdList:
            if avId != self.localAvId:
                self.remoteAvIdList.append(avId)

    def setTrolleyZone(self, trolleyZone):
        """
        called by the AI; trolleyZone is used to determine game difficulty
        """
        if not self.hasLocalToon: return
        self.notify.debug("BASE: setTrolleyZone: %s" % trolleyZone)
        self.trolleyZone = trolleyZone

    def setDifficultyOverrides(self, difficultyOverride, trolleyZoneOverride):
        """
        called by the AI; these values (if they're set) override
        the difficulty setting and the safezone ID
        """
        if not self.hasLocalToon: return
        if difficultyOverride != MinigameGlobals.NoDifficultyOverride:
            # to ensure that the AI and the clients have the same
            # difficulty override, it is sent as an integer
            self.difficultyOverride = (
                difficultyOverride /
                float(MinigameGlobals.DifficultyOverrideMult))
        if trolleyZoneOverride != MinigameGlobals.NoTrolleyZoneOverride:
            self.trolleyZoneOverride = trolleyZoneOverride

    def setGameReady(self):
        """
        This method gets called from the AI when all avatars have joined
        If this func returns 0, it is safe to access the toons
        If this func returns non-zero, it is not safe to access the toons;
          in this case, do nothing and wait for server to abort the game
        """
        if not self.hasLocalToon: return
        self.notify.debug("BASE: setGameReady: "
                          "Ready for game with avatars: %s" % self.avIdList)

        self.notify.debug("  safezone: %s" % self.getSafezoneId())
        self.notify.debug("difficulty: %s" % self.getDifficulty())

        self.__serverFinished = 0

        # assert that all of the remote toons are present
        for avId in self.remoteAvIdList:
            # make sure we have this avatar in our dictionary
            if not self.cr.doId2do.has_key(avId):
                # well gollee, the toon is already gone!
                # end the minigame
                self.notify.warning("BASE: toon %s already left or has not "
                                    "yet arrived; waiting for server to "
                                    "abort the game" % avId)
                # one or more avatars are missing, wait for the server
                # to end the game
                return 1

        # listen for the remote toons' disable events
        for avId in self.remoteAvIdList:
            avatar = self.cr.doId2do[avId]
            # Add a hook to hear when this avatar is disabled
            # Add an extra arg so we know which one
            event = avatar.uniqueName("disable")
            self.acceptOnce(event, self.handleDisabledAvatar, [avId])
            def ignoreToonDisable(self=self, event=event):
                self.ignore(event)
            self.cleanupActions.append(ignoreToonDisable)

        # Disable smoothing, etc. for all the toons in the game by default.
        # Some games (e.g. the tag game) may want to turn this back
        # on, but most games want full control over the toons'
        # placement onscreen.
        for avId in self.avIdList:
            # Find the actual avatar in the cr
            avatar = self.getAvatar(avId)
            if avatar:
                if not self.usesSmoothing:
                    avatar.stopSmooth()
                if not self.usesLookAround:
                    avatar.stopLookAround()

        def cleanupAvatars(self=self):
            for avId in self.avIdList:
                # Find the actual avatar in the cr
                avatar = self.getAvatar(avId)
                if avatar:
                    # make sure smoothing is off for all toons
                    # just in case the minigame turned it back on
                    avatar.stopSmooth()
                    # turn the lookaround back on
                    # 'on' is the default state
                    avatar.startLookAround()
        self.cleanupActions.append(cleanupAvatars)

        # all avatars are present, continue
        return 0

    def setGameStart(self, timestamp):
        """
        This method gets called from the AI when all avatars are ready
        Ready usually means they have read the rules
        Inheritors should call this plus the code to start the game
        """
        if not self.hasLocalToon: return
        self.notify.debug("BASE: setGameStart: Starting game")

        self.gameStartTime = \
                    globalClockDelta.networkToLocalTime(timestamp)

        # Enter the game state machine
        self.frameworkFSM.request("frameworkGame")

    def setGameAbort(self):
        """
        This method is called if another player exits the game unexpectedly,
        or if the game exits unexpectedly for debugging reasons. Unlike
        setGameExit, the minigame should not report back to the AI saying
        that they are ready to exit, since the minigame object is probably
        already deleted on the AI.
        """
        if not self.hasLocalToon: return
        self.notify.warning("BASE: setGameAbort: Aborting game")
        self.normalExit = 0
        self.frameworkFSM.request("frameworkCleanup")

    def gameOver(self):
        """
        Called by the subclass to indicate to the framework ClassicFSM
        that the game is over.
        """
        if not self.hasLocalToon: return
        self.notify.debug("BASE: gameOver")
        self.frameworkFSM.request("frameworkWaitServerFinish")

    def getAvatar(self, avId):
        """
        Instead of all the minigames writing code to do avatar lookups
        based on avIds, they should use this function. It returns a toon
        if that toon is in the doId2do. If the ID cannot be resolved
        for some reason, a warning is logged and we return None. Each
        game will have to deal with this.
        Why would an avatar not be in the doId2do? It can happen when
        an avatar quits the game early but we still get a game update
        afterwards.
        """

        # If it is an avatar, look it up in the doid2do
        if self.cr.doId2do.has_key(avId):
            return self.cr.doId2do[avId]
        # I do not know what this avId is
        else:
            self.notify.warning(
                "BASE: getAvatar: No avatar in doId2do with id: " + str(avId))
            return None

    def getAvatarName(self, avId):
        avatar = self.getAvatar(avId)
        if avatar:
            return avatar.getName()
        else:
            return "Unknown"

    def isSinglePlayer(self):
        """
        returns nonzero if there is only one player
        """
        if self.numPlayers == 1:
            return 1
        else:
            return 0

    def handleDisabledAvatar(self, avId):
        """
        Code to deal with an avatar unexpectedly being deleted
        If inheritors override, they should call this base function

        Transitions the frameworkFSM into an 'avatarExited' state (and
        out of 'game' state, for instance)

        The AI will end the game imminently when it detects this case
        """
        self.notify.warning("BASE: handleDisabledAvatar: disabled avId: " +
                            str(avId))
        self.frameworkFSM.request('frameworkAvatarExited')

    def d_requestExit(self):
        self.notify.debug("BASE: Sending requestExit")
        # Abort request, for debugging purposes.
        self.sendUpdate("requestExit", [])

    # Framework state machine functions

    def enterFrameworkInit(self):
        self.notify.debug("BASE: enterFrameworkInit")
        # tune emote access
        self.setEmotes()
        self.cleanupActions.append(self.unsetEmotes)
        
    def exitFrameworkInit(self):
        pass

    def enterFrameworkRules(self):
        """
        At some point during the rules, we might hear the game ready message
        which means all avatars have arrived.
        Tell the play game state data to show the rules
        Inheritors should override this completely
        """
        self.notify.debug("BASE: enterFrameworkRules")

        self.accept(self.rulesDoneEvent, self.handleRulesDone)
        # The rules panel is an onscreen panel
        self.rulesPanel = MinigameRulesPanel.MinigameRulesPanel(
            "MinigameRulesPanel",
            self.getTitle(),
            self.getInstructions(),
            self.rulesDoneEvent)
        self.rulesPanel.load()
        self.rulesPanel.enter()

        # DEBUG: instantly press the play button on the rules panel
        if 0:
            messenger.send(self.rulesDoneEvent)
        
    def exitFrameworkRules(self):
        # Hide the rules
        self.ignore(self.rulesDoneEvent)
        self.rulesPanel.exit()
        self.rulesPanel.unload()
        del self.rulesPanel

    def handleRulesDone(self):
        """
        This is called when the user is finished reading the rules
        Tell the DistributedMinigameAI we are ready.
        Go into the state where we wait for the server to send the
        start message.
        """
        self.notify.debug("BASE: handleRulesDone")

        self.sendUpdate("setAvatarReady", [])
        self.frameworkFSM.request("frameworkWaitServerStart")

    def enterFrameworkWaitServerStart(self):
        self.notify.debug("BASE: enterFrameworkWaitServerStart")
        if self.numPlayers > 1:
            msg = TTLocalizer.MinigameWaitingForOtherPlayers
        else:
            msg = TTLocalizer.MinigamePleaseWait
        self.waitingStartLabel['text'] = msg
        self.waitingStartLabel.show()

    def exitFrameworkWaitServerStart(self):
        self.waitingStartLabel.hide()

    def enterFrameworkGame(self):
        """
        The primary job of this state is to kick off the subclass
        gameFSM which should be a child state machine of this state
        """
        self.notify.debug("BASE: enterFrameworkGame")

    def exitFrameworkGame(self):
        pass

    def enterFrameworkWaitServerFinish(self):
        self.notify.debug("BASE: enterFrameworkWaitServerFinish")
        if self.__serverFinished:
            self.frameworkFSM.request("frameworkCleanup")

    def setGameExit(self):
        """
        This method gets called from the AI when it has determined the
        game is over. Every client should report that they are ready
        to exit upon receiving this message.
        """
        print("setGameExit")
        if not self.hasLocalToon: return
        self.notify.debug("BASE: setGameExit: now safe to exit game")
        if (self.frameworkFSM.getCurrentState().getName() !=
            'frameworkWaitServerFinish'):
            print("not waiting")
            self.__serverFinished = 1
        else:
            print("waiting")
            self.frameworkFSM.request("frameworkCleanup")

    def exitFrameworkWaitServerFinish(self):
        pass

    def enterFrameworkAvatarExited(self):
        """
        This state is entered when an avatar exits unexpectedly
        out of the game, and we get notification that the avatar
        has been deleted, before the server tells us to abort the
        game.
        This state servers two purposes:
        1) to exit whatever state we were in when we got notification
        2) to provide a stable state in which to wait for the server
           to abort the game
        """
        self.notify.debug("BASE: enterFrameworkAvatarExited")

    def exitFrameworkAvatarExited(self):
        pass

    def enterFrameworkCleanup(self):
        self.notify.debug("BASE: enterFrameworkCleanup")
        print("cleanup")

        # invoke all the cleanup actions
        for action in self.cleanupActions:
            action()
        self.cleanupActions = []

        # Ignore all events we might have accepted
        self.ignoreAll()

        if self.hasLocalToon:
            # Let the hood know we are done
            messenger.send(self.cr.playGame.hood.minigameDoneEvent)

            """ this is also in delete()...
            # Remove this state machine from Hood's state machine
            hoodMinigameState = self.cr.playGame.hood.fsm.getStateNamed(
            "minigame")
            hoodMinigameState.removeChild(self.frameworkFSM)
            """

    def exitFrameworkCleanup(self):
        pass

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
        if hasattr(base, 'minigameDifficulty'):
            return float(base.minigameDifficulty)
        return MinigameGlobals.getDifficulty(self.getSafezoneId())

    def getSafezoneId(self):
        """
        returns 1000-multiple safezone zoneId;
        can be matched to safezone IDs in ToontownGlobals.py
        """
        if self.trolleyZoneOverride is not None:
            return self.trolleyZoneOverride
        if hasattr(base, 'minigameSafezoneId'):
            return MinigameGlobals.getSafezoneId(base.minigameSafezoneId)
        return MinigameGlobals.getSafezoneId(self.trolleyZone)

    # setEmotes and unsetEmotes can be overidden by the base
    # classes if different settings are wanted.  But for most
    # minigames, we don't want emotes to be enabled
    def setEmotes(self):
        Emote.globalEmote.disableAll(base.localAvatar)

    def unsetEmotes(self):
        Emote.globalEmote.releaseAll(base.localAvatar)

    def setStartingVotes(self, startingVotesArray):
        if not len(startingVotesArray) == len(self.avIdList):
            self.notify.error('length does not match, startingVotes=%s, avIdList=%s' %
                              (startingVotesArray, self.avIdList))
            return
        
        for index  in range(len( self.avIdList)):
            avId = self.avIdList[index]
            self.startingVotes[avId] = startingVotesArray[index]

        self.notify.debug('starting votes = %s' % self.startingVotes)

    def setMetagameRound(self, metagameRound):
        self.metagameRound = metagameRound
