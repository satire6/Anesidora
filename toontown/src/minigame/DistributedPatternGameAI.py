"""DistributedPatternGameAI module: contains the DistributedPatternGameAI class"""

from DistributedMinigameAI import *
from toontown.ai.ToonBarrier import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import random
import PatternGameGlobals
import copy

class DistributedPatternGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedPatternGameAI_initialized
        except:
            self.DistributedPatternGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedPatternGameAI',
                                   [
                                    State.State('off',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['waitClientsReady',
                                                 'cleanup']),
                                    State.State('waitClientsReady',
                                                self.enterWaitClientsReady,
                                                self.exitWaitClientsReady,
                                                ['generatePattern',
                                                 'cleanup']),
                                    State.State('generatePattern',
                                                self.enterGeneratePattern,
                                                self.exitGeneratePattern,
                                                ['waitForResults',
                                                 'cleanup']),
                                    State.State('waitForResults',
                                                self.enterWaitForResults,
                                                self.exitWaitForResults,
                                                ['waitClientsReady',
                                                 'cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                []),
                                    ],
                                   # Initial State
                                   'off',
                                   # Final State
                                   'cleanup',
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
        self.__initGameVars()

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('waitClientsReady')

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

    def __initGameVars(self):
        self.pattern = []
        self.round = 0
        self.perfectResults = {}
        for avId in self.avIdList:
            self.perfectResults[avId] = 1
        self.readyClients = []
        self.timeoutTaskName = self.uniqueName('PatternGameResultsTimeout')

    def enterWaitClientsReady(self):
        self.notify.debug("enterWaitClientsReady")

        self.nextRoundBarrier = ToonBarrier(
            'nextRoundReady',
            self.uniqueName('nextRoundReady'),
            self.avIdList, PatternGameGlobals.ClientsReadyTimeout,
            self.__allPlayersReady, self.__clientsReadyTimeout)

        # some players may have already checked in
        for avId in self.readyClients:
            self.nextRoundBarrier.clear(avId)

    def reportPlayerReady(self):
        if self.gameFSM.getCurrentState().getName() != 'waitClientsReady':
            return
        avId = self.air.getAvatarIdFromSender()
        assert not avId in self.readyClients
        if avId not in self.avIdList:
            self.notify.warning(
                'Got reportPlayerReady from an avId: %s not in our list: %s' %
                (avId, self.avIdList))
        else:
            self.readyClients.append(avId)
            self.nextRoundBarrier.clear(avId)

    def __allPlayersReady(self):
        self.readyClients = []
        self.gameFSM.request('generatePattern')

    def __clientsReadyTimeout(self, avIds):
        # hmm, someone hasn't responded.
        self.notify.debug(
            "__clientsReadyTimeout: clients %s have not responded" %
            avIds)

        # abort the minigame
        self.setGameAbort()

    def exitWaitClientsReady(self):
        self.nextRoundBarrier.cleanup()
        del self.nextRoundBarrier

    def enterGeneratePattern(self):
        self.notify.debug("enterGeneratePattern")

        self.round += 1

        # add to the pattern if necessary
        targetLen = PatternGameGlobals.INITIAL_ROUND_LENGTH + \
            (PatternGameGlobals.ROUND_LENGTH_INCREMENT * (self.round-1))
        count = targetLen - len(self.pattern)
        for i in range(0,count):
            # add a random button index to the pattern
            self.pattern.append(random.randint(0,3))

        # don't send the pattern until we're ready for results
        self.gameFSM.request("waitForResults")
        self.sendUpdate("setPattern", [self.pattern])

    def exitGeneratePattern(self):
        pass

    def enterWaitForResults(self):
        self.notify.debug("enterWaitForResults")
        self.results = [None] * self.numPlayers
        self.fastestTime = PatternGameGlobals.InputTime*2
        self.fastestAvId = 0
        # allow some additional time to show the pattern to the players
        self.resultsBarrier = ToonBarrier(
            'results',
            self.uniqueName('results'),
            self.avIdList,
            PatternGameGlobals.InputTimeout + (1. * self.round),
            self.__gotAllPatterns, self.__resultsTimeout)

    def reportButtonPress(self, index, wrong):
        if self.gameFSM.getCurrentState().getName() != 'waitForResults':
            return
        # validate avId, index and wrong
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'PatternGameAI.reportButtonPress avId not on list')
            return
        if index < 0 or index > 3:
            self.air.writeServerEvent('warning', index, 'PatternGameAI.reportButtonPress got bad index')
            return
        if wrong not in [0,1]:
            self.air.writeServerEvent('warning', wrong, "PatternGameAI.reportButtonPress got bad 'wrong'")
            return
            
        self.sendUpdate("remoteButtonPressed", [avId, index, wrong])

    def __resultsTimeout(self, avIds):
        self.notify.debug("__resultsTimeout: %s" % avIds)
        # time's up; simulate a response from whoever didn't respond
        for avId in avIds:
            index = self.avIdList.index(avId)
            assert self.results[index] is None
            self.__acceptPlayerPattern(
                avId, [], PatternGameGlobals.InputTime*2)
        # and proceed
        self.__gotAllPatterns()

    def reportPlayerPattern(self, pattern, totalTime):
        if self.gameFSM.getCurrentState().getName() != 'waitForResults':
            return
        avId = self.air.getAvatarIdFromSender()
        self.__acceptPlayerPattern(avId, pattern, totalTime)
        # update the barrier
        self.resultsBarrier.clear(avId)

    def __acceptPlayerPattern(self, avId, pattern, totalTime):
        index = self.avIdList.index(avId)
        if (self.results[index] != None):
            # Ignore repeated submissions from the same player.
            return
        
        self.results[index] = pattern

        # If the time they took to complete the pattern is less then the
        # current fastest and they got it right, update.  fastestAvId
        # defaults to 0 which becomes important in DistributedPatternGame.py
        if totalTime < self.fastestTime and pattern == self.pattern:
            self.fastestTime = totalTime
            self.fastestAvId = avId
            if self.numPlayers == 1:
                self.fastestAvId = 1
            else:
                # If they were fastest and they're not alone,
                # give them a 2 jelly bonus!
                self.scoreDict[self.fastestAvId] += 2

    def __gotAllPatterns(self):
        # build a list of four patterns, even if there aren't four players
        patterns = [[]] * 4
        for i in range(0, len(self.results)):
            patterns[i] = self.results[i]
            # careful: if a player hasn't responded, their entry in the results
            # table will be None
            if patterns[i] is None:
                patterns[i] = []
        # send the clients all of the patterns and the fastest av
        self.sendUpdate("setPlayerPatterns", patterns + [self.fastestAvId])

        for i in range(0,self.numPlayers):
            avId = self.avIdList[i]

            if not (self.results[i] == self.pattern):
                # update the 'perfect' table
                self.perfectResults[avId] = 0
            else:
                # give that toon some jellybeans!
                self.scoreDict[avId] += self.round
        
        if self.round < PatternGameGlobals.NUM_ROUNDS:
            self.gameFSM.request('waitClientsReady')
        else:
            # increase score of players that had a perfect game
            # (not including bonuses)
            for avId in self.avIdList:
                if self.perfectResults[avId]:
                    self.scoreDict[avId] += 4
                    self.logPerfectGame(avId)

            # the game is over
            self.gameOver()

            # explicitly transition out of the waitForResults state
            # to guard against late results msgs
            self.gameFSM.request('cleanup')

    def exitWaitForResults(self):
        self.resultsBarrier.cleanup()
        del self.resultsBarrier

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass
