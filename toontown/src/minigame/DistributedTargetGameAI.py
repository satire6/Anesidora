"""DistributedTargetGameAI module: contains the DistributedTargetGameAI class"""

from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import TargetGameGlobals
import random
import types

def checkPlace(placeX, placeY, fillSize, placeList):
    goodPlacement = 1
    for place in placeList:
        distance = math.sqrt(((place[0] - placeX) * (place[0] - placeX)) + ((place[1] - placeY) * (place[1] - placeY)))
        distance = distance - (fillSize + place[2])
        if distance <= 0.0:
            goodPlacement = 0
            break
    return goodPlacement

class DistributedTargetGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        #print("entered Init")
        try:
            #print("trying")
            self.DistributedTargetGameAI_initialized
        except:
            #print("excepting")
            self.DistributedTargetGameAI_initialized = 1
            #print("1")
            DistributedMinigameAI.__init__(self, air, minigameId)
            #print("2")

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTargetGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['fly']),
                                    State.State('fly',
                                                self.enterFly,
                                                self.exitFly,
                                                ['cleanup', 'resetRound']),
                                    State.State('resetRound',
                                                self.enterResetRound,
                                                self.exitResetRound,
                                                ['cleanup', 'fly']),
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
            #self.selectColorIndices()
            
            self.round = 2
            self.barrierScore = None
            self.scoreTrack = []

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        del self.scoreTrack
        if hasattr(self, "barrierScore"):
            if self.barrierScore:
                self.barrierScore.cleanup()
                del self.barrierScore
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        # make sure the client has this before setting the seed
        self.sendUpdate("setTrolleyZone", [self.trolleyZone])
        DistributedMinigameAI.setGameReady(self)
        import time
        random.seed(time.time())
        seed = int(random.random() * 4000.0)
        self.sendUpdate("setTargetSeed", [seed])
        random.seed(seed)
        #print ("seed %s" % (seed))
        self.setupTargets()
        
        
    def setupTargets(self):
        fieldWidth = TargetGameGlobals.ENVIRON_WIDTH * 3
        fieldLength = TargetGameGlobals.ENVIRON_LENGTH * 3.70
        self.pattern = TargetGameGlobals.difficultyPatterns[self.getSafezoneId()]
        self.targetList = self.pattern[0]
        self.targetValue = self.pattern[1]
        self.targetSize = self.pattern[2]
        self.targetColors = self.pattern[3]
        self.targetSubParts = self.pattern[4]
        
        highestValue = 0
        
        for value in self.targetValue:
            if value > highestValue:
                highestValue = value
        
        self.placeValue = highestValue * 0.5
        
        self.targetsPlaced = []
        placeList = []
        
        for typeIndex in range(len(self.targetList)):
           for targetIndex in range(self.targetList[typeIndex]):
                goodPlacement = 0
                while not goodPlacement:
                    placeX = random.random()*(fieldWidth * 0.60) - ((fieldWidth * 0.60)  * 0.5)
                    placeY = ((random.random() * 0.60) + (0.00 + (0.40 * ((self.placeValue * 1.0) / (highestValue * 1.0))))) * fieldLength 
                    fillSize = self.targetSize[typeIndex]
                    goodPlacement = checkPlace(placeX, placeY, fillSize, placeList)
                placeList.append((placeX, placeY, fillSize))
                
                subIndex = self.targetSubParts[typeIndex]
                while subIndex:
                    combinedIndex = typeIndex + subIndex - 1
                    self.targetsPlaced.append((placeX, placeY, combinedIndex))
                    subIndex -= 1

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        
        # reset scores
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0
            
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)

        self.gameFSM.request('fly')
        
        
    def setScore(self, scoreX, scoreY, other = None):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'RingGameAI.setScore: invalid avId')
            return
        #if score <= 150:
        #    if self.scoreDict[avId] < score:
        #        self.scoreDict[avId] = score
        #        self.sendUpdate('setSingleScore', [score, avId])
        topValue = 0
        hitTarget = None
        #print self.targetsPlaced
        for target in self.targetsPlaced:
            radius = self.targetSize[target[2]]
            value = self.targetValue[target[2]]
            posX = target[0]
            posY = target[1]
            dx = posX - scoreX
            dy = posY - scoreY
            distance = math.sqrt(dx*dx + dy*dy)
            #print distance
            if (distance < radius) and (topValue < value):
                #print ("hit!")
                topValue = value
                hitTarget = target
                hitX = posX
                hitY = posY
                
        if self.scoreDict[avId] < topValue:
                self.scoreDict[avId] = topValue
                self.sendUpdate('setSingleScore', [topValue, avId])
        
        
        

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


    def enterFly(self):
        self.notify.debug("enterFly")
        self.barrierScore = ToonBarrier(
                'waitClientsScore',
                self.uniqueName('waitClientsScore'),
                self.avIdList, 120,
                self.allAvatarsScore, self.handleTimeout)
        
    def exitFly(self):
        pass
        
    def handleTimeout(self, other = None):
        #self.gameOver()
        pass
        
    def allAvatarsScore(self, other = None):
        if self.round == 0:
            self.gameOver()
        else:
            self.round -= 1
            self.gameFSM.request('resetRound')
            
    def getScoreList(self):
        scoreList = [0,0,0,0]
        avList = [0,0,0,0]
        scoreIndex = 0
        for avId in self.scoreDict.keys():
            scoreList[scoreIndex] = self.scoreDict[avId]
            avList[scoreIndex] = avId
            scoreIndex += 1
        return scoreList
        
            
    def enterResetRound(self):
        #scoreList = [0,0,0,0]
        #avList = [0,0,0,0]
        #scoreIndex = 0
        scoreList = self.getScoreList()
        
        #for avId in self.scoreDict.keys():
        #    scoreList[scoreIndex] = self.scoreDict[avId]
        #    avList[scoreIndex] = avId
        #    scoreIndex += 1
            
        self.scoreTrack.append(scoreList)
        
        self.sendUpdate('setRoundDone', [])
        self.barrierScore.cleanup()
        del self.barrierScore
        taskMgr.doMethodLater(0.1,
                              self.gotoFly,
                              self.taskName("roundReset")) 
        
    def exitResetRound(self):
        pass
        
    def gotoFly(self, extra = None):
        if hasattr(self, "gameFSM"):
            self.gameFSM.request('fly')

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')
        


    def exitCleanup(self):
        pass

    # network messages
    
    def setPlayerDone(self, other = None):
        if not hasattr(self, "barrierScore"):
            return
        #print("received setPlayerDone")
        avId = self.air.getAvatarIdFromSender()
        #import pdb; pdb.set_trace()
        #self.gameOver()
        self.barrierScore.clear(avId)
        #self.b_setGameExit()
        # process any toons that have already exited
        for avId in self.stateDict.keys():
            if self.stateDict[avId] == EXITED:
                self.barrierScore.clear(avId)
        

    def gameOver(self):
        self.notify.debug("gameOver")
        for entry in self.scoreDict:
            if self.scoreDict[entry] == 0:
                self.scoreDict[entry]  = 1             
        self.scoreTrack.append(self.getScoreList())
        statMessage = ("MiniGame Stats : Target Game" + "\nScores" + ("%s" % self.scoreTrack) + "\nAvIds" + ("%s" % self.scoreDict.keys()) + "\nSafeZone" + ("%s" % self.getSafezoneId()))
        
        self.air.writeServerEvent("MiniGame Stats", None, statMessage)
        
        self.sendUpdate('setGameDone', [])
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)
        
    def hasScoreMult(self):
        return 0

        
