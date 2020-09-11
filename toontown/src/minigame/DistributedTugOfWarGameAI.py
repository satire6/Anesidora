"""DistributedTugOfWarGameAI module: contains the DistributedTugOfWarGameAI class"""

from DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import random
from direct.task.Task import Task
import copy
import TugOfWarGameGlobals
import math

class DistributedTugOfWarGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedTugOfWarGameAI_initialized
        except:
            self.DistributedTugOfWarGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTugOfWarGameAI',
                                   [
                                    State.State('off',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['waitClientsReady',
                                                 'cleanup']),
                                    State.State('waitClientsReady',
                                                self.enterWaitClientsReady,
                                                self.exitWaitClientsReady,
                                                ['sendGoSignal',
                                                 'cleanup']),
                                    State.State('sendGoSignal',
                                                self.enterSendGoSignal,
                                                self.exitSendGoSignal,
                                                ['waitForResults',
                                                 'cleanup']),
                                    State.State('waitForResults',
                                                self.enterWaitForResults,
                                                self.exitWaitForResults,
                                                ['waitClientsReady',
                                                 'contestOver',
                                                 'cleanup']),
                                    State.State('contestOver',
                                                self.enterContestOver,
                                                self.exitContestOver,
                                                ['cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                ['off']),
                                    ],
                                   # Initial State
                                   'off',
                                   # Final State
                                   'off',
                                   )

            # Add our game ClassicFSM to the framework ClassicFSM in the game state
            self.addChildGameFSM(self.gameFSM)

        self.switched = 0

        # Keep track of which side each avatar is on
        self.side = {}

        # Add up all the players forces for each side as soon as we get a
        # keyRate update from all players.  
        self.forceDict = [{},{}]
        self.keyRateDict = {}
        self.howManyReported = 0

        # The difference between each side's total force (deltaF) is calculated
        # and from that an absolute offset (deltaX) from each toons original
        # position is calculated. See calculateOffsets function for more info
        self.offsetDict = {}

        # This constant is multiplied by the force to give the deltaX that the
        # toon moves
        self.kMovement = .02
        
        # If we are in a Toon vs. Cog game the AI has
        # to determine how hard the suit is pulling, and send
        # the suit's offset to the clients.  The suitForces array
        # contains (duration, force) pairs.  All the durations should
        # at least add up to the length of the game (40 sec).
        self.suitId = 666
        #self.suitForces = [(6,4), (2,5.5), (2,7.5), (4,8), (4,7), (8,8), (9,8.5), (4,9)]
        self.suitForces = [(6,4), (2,5), (2,6.5), (3,8.0), (5,6), (8,8), (9,8.5), (4,9)]
        self.suitForceMultiplier = .75
        self.curSuitForce = 0
        self.suitOffset = 0
        
        # Variables for determining the outcome of the game.  If contestEnded=1
        # that means someone actually fell in the water.  A list of winners,
        # losers, and tie-ers are sent to the clients, so the toons can react
        # in the correct way (celebrate or sulk).  A time bonus is rewarded for
        # either winning fast, or losing slow
        self.contestEnded = 0
        self.losingSide = -1
        self.winners = []
        self.losers = []
        self.tieers = []
        self.timeBonus = float(TugOfWarGameGlobals.TIME_BONUS_RANGE)

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        del self.side
        del self.forceDict
        del self.keyRateDict
        del self.offsetDict
        del self.suitForces
        del self.winners
        del self.tieers
        del self.losers
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")

        # determine game type
        self.suitType = random.randrange(1,5)
        self.suitJellybeanReward = math.pow(2, self.suitType-1)
        
        if self.isSinglePlayer():
            self.gameType = TugOfWarGameGlobals.TOON_VS_COG
            self.suitForceMultiplier = .58 + float(self.suitType)/10.0
        else:
            randInt = random.randrange(0,10)
            if randInt < 8:
                self.gameType = TugOfWarGameGlobals.TOON_VS_COG
                self.suitForceMultiplier = .65 + float(self.suitType)/16.0
                self.kMovement = .02
            else:
                self.gameType = TugOfWarGameGlobals.TOON_VS_TOON
                self.kMovement = .04

        self.sendUpdate("sendGameType", [self.gameType, self.suitType])
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
        self.currentButtons = [0,0]
        self.readyClients = []

    def enterWaitClientsReady(self):
        self.notify.debug("enterWaitClientsReady")
        # Start the timeout
        taskMgr.doMethodLater(TugOfWarGameGlobals.WAIT_FOR_CLIENTS_TIMEOUT,
                              self.waitForClientsTimeout,
                              self.taskName("clients-timeout"))

    def exitWaitClientsReady(self):
        taskMgr.remove(self.taskName("clients-timeout"))

    def waitForClientsTimeout(self, task):
        self.notify.debug("Done waiting for clients")
        # someone couldn't join, just end the game
        self.sendUpdate("sendStopSignal", [self.winners, self.losers, self.tieers])
        self.gameOver()
        return Task.done
        
    def reportPlayerReady(self, side):
        avId = self.air.getAvatarIdFromSender()
        assert not avId in self.readyClients
        if avId not in self.avIdList or side not in [0,1]:
            self.notify.warning('Got reportPlayerReady from an avId: %s not in our list: %s' %
                                (avId, self.avIdList))
        else:
            self.readyClients.append(avId)
            self.side[avId] = side
            self.forceDict[side][avId] = 0
            self.offsetDict[avId] = 0
        if len(self.readyClients) == self.numPlayers:
            self.readyClients = []
            self.gameFSM.request('sendGoSignal')


    def sendNewAvIdList(self, newAvIdList):
        if not self.switched:
            self.switched = 1
            self.avIdList = newAvIdList
        else:
            if self.avIdList != newAvIdList:
                self.notify.debug("Big trouble in little TugOWar Town")
        
    def enterSendGoSignal(self):
        self.notify.debug("enterSendGoSignal")
        
        # Start the game timer
        taskMgr.doMethodLater(TugOfWarGameGlobals.GAME_DURATION,
                              self.timerExpired,
                              self.taskName("gameTimer"))

        if self.gameType == TugOfWarGameGlobals.TOON_VS_COG:
            # Start the force updates for the suit
            self.curSuitForceInd = 0
            taskMgr.add(self.timeForNewSuitForce,
                        self.taskName("suitForceTimer"))
        taskMgr.doMethodLater(1,
                              self.calcTimeBonus,
                              self.taskName("timeBonusTimer"))
        self.sendUpdate("sendGoSignal",[[0,1]])
        self.gameFSM.request("waitForResults")

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        self.gameFSM.request('contestOver')
        return Task.done

    def timeForNewSuitForce(self, task):
        self.notify.debug("timeForNewSuitForce")
        if self.curSuitForceInd < len(self.suitForces):
            # add or subtract some amount of random force, so the games don't all progress the same way
            randForce = random.random()-.5
            self.curSuitForce = self.suitForceMultiplier * self.numPlayers * (self.suitForces[self.curSuitForceInd][1] + randForce)
            taskMgr.doMethodLater(self.suitForces[self.curSuitForceInd][0],
                                  self.timeForNewSuitForce,
                                  self.taskName("suitForceTimer"))
        self.curSuitForceInd += 1
        return Task.done

    def calcTimeBonus(self, task):
        delta = float(TugOfWarGameGlobals.TIME_BONUS_RANGE)/float(TugOfWarGameGlobals.GAME_DURATION)
        self.timeBonus = self.timeBonus - delta
        taskMgr.doMethodLater(1,
                              self.calcTimeBonus,
                              self.taskName("timeBonusTimer"))
        return Task.done
    
    def exitSendGoSignal(self):
        pass

    def enterWaitForResults(self):
        self.notify.debug("enterWaitForResults")

    def calculateOffsets(self):
        # This function totals the forces on each side of the water.  Then the difference
        # deltaF, between these forces is computed.  This is multiplied by a constant, kMovement,
        # to determine what the deltaX should be - i.e. how much the toons on each side should
        # move as a result of one side applying more force than the other.
        
        # The stronger side should move away from the water a little bit, while the weaker
        # side should move closer.  In a toon-vs-toon battle, the weaker toons should move
        # faster towards the water so we don't have too many stalemates.  In a toon-vs-cog,
        # the weaker toons should not be pulled as fast.  This is a tricky balancing issue.  If
        # there are too many stalemates, change the value of kMovement to something larger.

        f = [0,0]
        # total up all the toon forces on each side
        for i in [0,1]:
            for x in self.forceDict[i].values():
                f[i] += x
        # since the cog is always on the right side (side=0) add that in
        if self.gameType == TugOfWarGameGlobals.TOON_VS_COG:
            f[1] += self.curSuitForce
            
        deltaF = f[1] - f[0]
        deltaX = deltaF * self.kMovement

        # fill the offsetDict
        for avId in self.avIdList:
            # add deltaX to offsetDict
            # or add deltaX/2.0 if avatar is on strong side of the rope
            offset = deltaX
            if self.side[avId] == 0:
                if deltaX < 0:
                    offset = deltaX/2.0
            elif deltaX > 0:
                offset = deltaX/2.0
            self.offsetDict[avId] += offset

        if deltaX < 0:
            self.suitOffset += deltaX
        else:
            self.suitOffset += deltaX/2.0
        
    def reportCurrentKeyRate(self, keyRate, force):
        avId = self.air.getAvatarIdFromSender()
        self.keyRateDict[avId] = keyRate
        self.forceDict[self.side[avId]][avId] = force

        # send the force for this avId to the clients
        self.sendUpdate("remoteKeyRateUpdate", [avId, self.keyRateDict[avId]])

        # send the current position to the clients if we have gotten all the clients forces
        self.howManyReported += 1
        if self.howManyReported == self.numPlayers:
            self.howManyReported = 0
            self.calculateOffsets()
            self.sendUpdate("sendCurrentPosition", [self.offsetDict.keys(), self.offsetDict.values()])
            if self.gameType == TugOfWarGameGlobals.TOON_VS_COG:
                self.sendUpdate("sendSuitPosition", [self.suitOffset])
            
    def reportEndOfContest(self, index):
        if index not in [0,1]:
            self.notify.warning('Got a bad index %s ' %index)
            return
        self.losingSide = index
        self.notify.debug("losing side = %d" % (self.losingSide))
        if self.contestEnded == 0:
            self.contestEnded = 1
            self.gameFSM.request('contestOver')
            
    def __processResults(self):
        # There are two main types of outcomes
        # 1) Someone fell in the water.  This type of outcome should yield the most
        #    jellybeans for the winner, as well as the largest difference in jellybeans
        #    between winner and loser.
        #    A time bonus should be awarded for the winner, for a quick victory.
        #    A smaller time bonus is awarded to the loser for losing, but taking
        #    a long time to do it.  Hopefully this rewards someone that is actually trying.
        # 2) Nobody fell in.  Award the win to the person that is furthest from the water.
        #    In this case there is no time bonus, since the timer expired.
        # The suitJellybeanReward is used to award more points for beating more
        # difficult cogs.
        if self.contestEnded:
            # somebody fell in the water (players go in either the winners list or the losers list)
            # add a timeBonus to the winner for time left on the clock
            self.timeBonus = TugOfWarGameGlobals.TIME_BONUS_MIN + int(self.timeBonus + .5)
            if self.gameType == TugOfWarGameGlobals.TOON_VS_COG:
                if self.losingSide == 1:
                    self.losers.append(self.suitId)
                else:
                    self.winners.append(self.suitId)
                for i in range(0,self.numPlayers):
                    avId = self.avIdList[i]
                    if self.side[avId] != self.losingSide:
                        #self.scoreDict[avId] += (self.suitJellybeanReward + 6 + self.timeBonus)
                        self.scoreDict[avId] = self.suitJellybeanReward + TugOfWarGameGlobals.WIN_JELLYBEANS
                        self.winners.append(avId)
                    else:
                        #self.scoreDict[avId] += (self.suitJellybeanReward/2 + TugOfWarGameGlobals.TIME_BONUS_MAX - self.timeBonus)
                        self.scoreDict[avId] = TugOfWarGameGlobals.LOSS_JELLYBEANS
                        self.losers.append(avId)
            else:       
                for i in range(0,self.numPlayers):
                    avId = self.avIdList[i]
                    if self.side[avId] != self.losingSide:
                        self.scoreDict[avId] = TugOfWarGameGlobals.WIN_JELLYBEANS
                        self.winners.append(avId)
                    else:
                        self.scoreDict[avId] = TugOfWarGameGlobals.LOSS_JELLYBEANS
                        self.losers.append(avId)
        else:
            # nobody fell in, find out who was the closest to falling
            # find out who moved the most in the right (safe) direction
            if self.gameType == TugOfWarGameGlobals.TOON_VS_COG:
                for i in range(0,self.numPlayers):
                    avId = self.avIdList[i]
                    if -self.offsetDict[avId] > self.suitOffset:
                        self.scoreDict[avId] = self.suitJellybeanReward/2 + TugOfWarGameGlobals.TIE_WIN_JELLYBEANS
                        self.winners.append(avId)
                    else:
                        self.scoreDict[avId] = self.suitJellybeanReward/2 + TugOfWarGameGlobals.TIE_LOSS_JELLYBEANS
                        self.losers.append(avId)
                        self.winners.append(self.suitId)
            else:        
                maxOffset = -100
                minOffset = 100
                for i in range(0,self.numPlayers):
                    avId = self.avIdList[i]
                    if self.side[avId] == 0:
                        if -self.offsetDict[avId] > maxOffset:
                            maxOffset = -self.offsetDict[avId]
                        elif -self.offsetDict[avId] < minOffset:
                            minOffset = -self.offsetDict[avId]
                    elif self.side[avId] == 1:
                        if self.offsetDict[avId] > maxOffset:
                            maxOffset = self.offsetDict[avId]
                        elif self.offsetDict[avId] < minOffset:
                            minOffset = self.offsetDict[avId]

                for i in range(0,self.numPlayers):
                    avId = self.avIdList[i]
                    if maxOffset != minOffset:
                        # somebody was winning when timer expired
                        if self.side[avId] == 0:
                            if -self.offsetDict[avId] == maxOffset:
                                self.scoreDict[avId] = TugOfWarGameGlobals.TIE_WIN_JELLYBEANS
                                self.winners.append(avId)
                            else:
                                self.scoreDict[avId] = TugOfWarGameGlobals.TIE_LOSS_JELLYBEANS
                                self.losers.append(avId)
                        elif self.side[avId] == 1:
                            if self.offsetDict[avId] == maxOffset:
                                self.scoreDict[avId] = TugOfWarGameGlobals.TIE_WIN_JELLYBEANS
                                self.winners.append(avId)
                            else:
                                self.scoreDict[avId] = TugOfWarGameGlobals.TIE_LOSS_JELLYBEANS
                                self.losers.append(avId)
                    else:
                        # nobody was winning when timer expired
                        self.scoreDict[avId] += TugOfWarGameGlobals.TIE_JELLYBEANS
                        self.tieers.append(avId)
        # the game is over
        self.gameOver()

    def exitWaitForResults(self):
        pass
    
    def enterContestOver(self):
        self.__processResults()
        self.sendUpdate("sendStopSignal", [self.winners, self.losers, self.tieers])
        pass

    def exitContestOver(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        taskMgr.remove(self.taskName("gameTimer"))
        taskMgr.remove(self.taskName("timeBonusTimer"))
        taskMgr.remove(self.taskName("suitForceTimer"))
        self.gameFSM.request('off')

    def exitCleanup(self):
        pass





