"""DistributedRingGameAI module: contains the DistributedRingGameAI class"""

from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import RingGameGlobals
import random
import types

class DistributedRingGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedRingGameAI_initialized
        except:
            self.DistributedRingGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedRingGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['swimming']),
                                    State.State('swimming',
                                                self.enterSwimming,
                                                self.exitSwimming,
                                                ['cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                ['inactive']),
                                    ],
                                   # Initial State
                                   'inactive',
                                   # Final State
                                   'inactive',
                                   )

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)

            #self.__timeBase = globalClock.getRealTime()
            self.__timeBase = globalClockDelta.localToNetworkTime(globalClock.getRealTime())
            self.selectColorIndices()

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)

        self.gameFSM.request('swimming')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def getTimeBase(self):
        # give the chosen timebase to the clients
        return self.__timeBase

    def getColorIndices(self):
        # return the selected ring colors for all players.
        return self.colorIndices

    def selectColorIndices(self):
        # Choose a random color from the selection in RingGameGlobals
        # for each player.  We don't know at this point how many
        # players we'll have; just choose four colors.
        self.colorIndices = [None, None, None, None]
        chooseFrom = RingGameGlobals.ringColorSelection[:]
        for i in range(0, 4):
            c = random.choice(chooseFrom)
            chooseFrom.remove(c)
            if isinstance(c, types.TupleType):
                c = random.choice(c)
            self.colorIndices[i] = c

    def enterSwimming(self):
        self.notify.debug("enterSwimming")

        # as each toon passes each ring group, they will send a result
        # to us. We are guaranteed to receive a single client's messages
        # in order. However, we may receive client0's result for ring
        # group 1 before we hear client1's result for ring group 0.
        # in other words, we are not guaranteed to have heard the entire
        # set of results for a group of rings before we start hearing
        # the results for later groups of rings.
        self.__nextRingGroup = {}
        for avId in self.avIdList:
            self.__nextRingGroup[avId] = 0
        self.__numRingsPassed = [0] * RingGameGlobals.NUM_RING_GROUPS
        self.__ringResultBitfield = [0] * RingGameGlobals.NUM_RING_GROUPS
        # keep track of which individual toons have perfect games
        self.perfectGames = {}
        for avId in self.avIdList:
            self.perfectGames[avId] = 1

        # zero out the scores
        for avId in self.avIdList:
            self.scoreDict[avId] = 0

    def exitSwimming(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    # network messages
    def setToonGotRing(self, success):
        """
        client (avId) is telling us that they did or did not get
        their ring
        """
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'RingGameAI.setToonGotRing: invalid avId')
            return
        if (self.gameFSM.getCurrentState() is None) or (self.gameFSM.getCurrentState().getName() != 'swimming'):
            self.air.writeServerEvent('suspicious', avId,
                                      'RingGameAI.setToonGotRing: game not in swimming state')
            return
        ringGroupIndex = self.__nextRingGroup[avId]

        # guard against messages that should not be arriving here
        if ringGroupIndex >= RingGameGlobals.NUM_RING_GROUPS:
            self.notify.warning(
                'warning: got extra ToonGotRing msg from av %s' % avId)
            return

        self.__nextRingGroup[avId] += 1

        if not success:
            # if not successful, set this toon's bit
            self.__ringResultBitfield[ringGroupIndex] |= \
                                           1 << self.avIdList.index(avId)
            # reset the perfect flag for this toon
            self.perfectGames[avId] = 0
        else:
            # otherwise, give them a point
            self.scoreDict[avId] += 1

        self.__numRingsPassed[ringGroupIndex] += 1
        if self.__numRingsPassed[ringGroupIndex] >= self.numPlayers:
            # single-player has no group bonus
            if not self.isSinglePlayer():
                # we've heard from everybody about this ring group
                # send out the result and update the scores
                bitfield = self.__ringResultBitfield[ringGroupIndex]
                # if nobody missed, no bits will be set
                if bitfield == 0x00:
                    for id in self.avIdList:
                        self.scoreDict[id] += .5

                self.sendUpdate("setRingGroupResults", [bitfield])

            # if that was the last ring group, we're done
            if ringGroupIndex >= (RingGameGlobals.NUM_RING_GROUPS-1):
                # add a bonus if perfect game, depending on # of players
                # that played perfectly.
                # note that multiplayer games give .5 bonus for each perfect
                # ring group, so a group-perfect game will already have an
                # extra 8 beans per player.
                perfectBonuses = {
                    1 : 5,
                    2 : 5,
                    3 : 10,
                    4 : 18,
                    }
                # tally the number of players that were perfect
                numPerfectToons = 0
                for avId in self.avIdList:
                    if self.perfectGames[avId]:
                        numPerfectToons += 1
                # give out the bonuses
                for avId in self.avIdList:
                    if self.perfectGames[avId]:
                        self.scoreDict[avId] += perfectBonuses[numPerfectToons]
                        self.logPerfectGame(avId)

                # make sure everyone has at least one jbean
                for avId in self.avIdList:
                    self.scoreDict[avId] = max(1, self.scoreDict[avId])
                
                if not RingGameGlobals.ENDLESS_GAME:
                    self.gameOver()
