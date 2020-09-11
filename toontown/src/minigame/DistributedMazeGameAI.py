"""DistributedMazeGameAI module: contains the DistributedMazeGameAI class"""

from DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import PatternGameGlobals
from direct.task.Task import Task
import MazeGameGlobals
import MazeData

class DistributedMazeGameAI(DistributedMinigameAI):
    def __init__(self, air, minigameId):
        try:
            self.DistributedMinigameTemplateAI_initialized
        except:
            self.DistributedMinigameTemplateAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedMazeGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['play']),
                                    State.State('play',
                                                self.enterPlay,
                                                self.exitPlay,
                                                ['waitShowScores',
                                                 'cleanup']),
                                    State.State('waitShowScores',
                                                self.enterWaitShowScores,
                                                self.exitWaitShowScores,
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
        # all of the players have checked in
        # they will now be shown the rules

        # get maze dimensions, boolean collision array
        mazeName = MazeGameGlobals.getMazeName(self.doId, self.numPlayers,
                                               MazeData.mazeNames)
        mData = MazeData.mazeData[mazeName]

        self.numTreasures = len(mData["treasurePosList"])
        self.numTreasuresTaken = 0
        self.takenTable = [0] * self.numTreasures

        # reset scores
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

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

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # Start the game timer
        taskMgr.doMethodLater(MazeGameGlobals.GAME_DURATION,
                              self.timerExpired,
                              self.taskName("gameTimer"))

    def exitPlay(self):
        taskMgr.remove(self.taskName("gameTimer"))

    def claimTreasure(self, treasureNum):
        # if the game just ended, ignore this message
        if (self.gameFSM.getCurrentState() is None) or (self.gameFSM.getCurrentState().getName() != 'play'):
            return

        # we're getting strange AI crashes where a toon claims
        # a treasure, and the toon is not listed in the scoreDict
        avId = self.air.getAvatarIdFromSender()
        if not self.scoreDict.has_key(avId):
            self.notify.warning(
                'PROBLEM: avatar %s called claimTreasure(%s) '
                'but he is not in the scoreDict: %s. avIdList is: %s' %
                (avId, treasureNum, self.scoreDict, self.avIdList))
            return

        #self.notify.debug("treasure %s claimed by %s" % \
        #                  (treasureNum, self.air.getAvatarIdFromSender()))

        # give the treasure to the first toon that claims it
        if treasureNum < 0 or treasureNum >= self.numTreasures:
            self.air.writeServerEvent('warning', treasureNum, 'MazeGameAI.claimTreasure treasureNum out of range')
            return
        if self.takenTable[treasureNum]:
            return
        self.takenTable[treasureNum] = 1

        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate("setTreasureGrabbed", [avId, treasureNum])
        self.scoreDict[avId] += 1
        self.numTreasuresTaken += 1

        # if all treasure is taken, end the game
        if self.numTreasuresTaken >= self.numTreasures:
            self.logAllPerfect()
            self.sendUpdate('allTreasuresTaken', [])
            if not MazeGameGlobals.ENDLESS_GAME:
                self.gameFSM.request('waitShowScores')

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        if not MazeGameGlobals.ENDLESS_GAME:
            self.gameFSM.request('waitShowScores')
        return Task.done

    def enterWaitShowScores(self):
        self.notify.debug("enterWaitShowScores")

        taskMgr.doMethodLater(MazeGameGlobals.SHOWSCORES_DURATION,
                              self.__doneShowingScores,
                              self.taskName("waitShowScores"))

    def __doneShowingScores(self, task):
        self.notify.debug("doneShowingScores")
        # tone down the scores, and make sure everyone has
        # at least one jellybean
        for key in self.scoreDict.keys():
            self.scoreDict[key] = max(1, self.scoreDict[key]/12)

        if self.numTreasuresTaken >= self.numTreasures:
            # increase everybody's score
            for key in self.scoreDict.keys():
                self.scoreDict[key] += 8

        self.gameOver()
        return Task.done

    def exitWaitShowScores(self):
        taskMgr.remove(self.taskName("waitShowScores"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        del self.takenTable

        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
