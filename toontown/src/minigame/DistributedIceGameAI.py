"""DistributedIceGameeAI module: contains the DistributedIceGameAI class"""
from pandac.PandaModules import Point3
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm import ClassicFSM, State
from direct.task import Task
from toontown.minigame import DistributedMinigameAI
from toontown.minigame import MinigameGlobals
from toontown.minigame import IceGameGlobals
from toontown.ai.ToonBarrier import ToonBarrier

class DistributedIceGameAI(DistributedMinigameAI.DistributedMinigameAI):
    """AI side class for the ice game."""
    notify = directNotify.newCategory("DistributedIceGameAI")

    def __init__(self, air, minigameId):
        try:
            self.DistributedIceGameAI_initialized
        except:
            self.DistributedIceGameAI_initialized = 1
            DistributedMinigameAI.DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedIceGameAI',
                                   [
                                    State.State('off',
                                                self.enterOff,
                                                self.exitOff,
                                                ['waitClientsChoices']),
                                    State.State('waitClientsChoices',
                                                self.enterWaitClientsChoices,
                                                self.exitWaitClientsChoices,
                                                ['cleanup', 'processChoices']),
                                    State.State('processChoices',
                                                self.enterProcessChoices,
                                                self.exitProcessChoices,
                                                ['waitEndingPositions', 'cleanup']),
                                    State.State('waitEndingPositions',
                                                self.enterWaitEndingPositions,
                                                self.exitWaitEndingPositions,
                                                ['processEndingPositions', 'cleanup']),
                                    State.State('processEndingPositions',
                                                self.enterProcessEndingPositions,
                                                self.exitProcessEndingPositions,
                                                ['waitClientsChoices','scoreMatch',
                                                 'cleanup']),
                                    State.State('scoreMatch',
                                                self.enterScoreMatch,
                                                self.exitScoreMatch,
                                                ['waitClientsChoices','finalResults',
                                                 'cleanup']),
                                    State.State('finalResults',
                                                self.enterFinalResults,
                                                self.exitFinalResults,
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

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)

            # for each avatar, keep track of force and which direction he wants to go
            self.avatarChoices = {}

            # for each avatar, keep track of the ending positions of the tires
            self.avatarEndingPositions = {}

            self.curRound = 0
            self.curMatch = 0

            # a list of the definitive AI arbitrated positions of the tires, 
            self.finalEndingPositions = [Point3(IceGameGlobals.StartingPositions[0]),
                                         Point3(IceGameGlobals.StartingPositions[1]),
                                         Point3(IceGameGlobals.StartingPositions[2]),
                                         Point3(IceGameGlobals.StartingPositions[3]),
                                         ]
    
    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        taskMgr.remove(self.taskName("wait-choices-timeout"))
        taskMgr.remove(self.taskName("endingPositionsTimeout"))
        del self.gameFSM
        DistributedMinigameAI.DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.DistributedMinigameAI.setGameReady(self)
        
        self.numTreasures = IceGameGlobals.NumTreasures[self.getSafezoneId()]
        self.numTreasuresTaken = 0
        self.takenTreasuresTable = [0] * self.numTreasures

        self.numPenalties = IceGameGlobals.NumPenalties[self.getSafezoneId()]
        self.numPenaltiesTaken = 0
        self.takenPenaltiesTable = [0] * self.numPenalties     

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('waitClientsChoices')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.DistributedMinigameAI.setGameAbort(self)
            
    def gameOver(self):
        self.notify.debug("gameOver")
        
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.DistributedMinigameAI.gameOver(self)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

##     def enterPlay(self):
##         self.notify.debug("enterPlay")

##         # when the game is done, call gameOver()
##         #self.gameOver()
##         # set up a barrier to wait for the 'game done' msgs
##         def allToonsDone(self=self):
##             self.notify.debug('allToonsDone')
##             #self.sendUpdate('setEveryoneDone')
##             #if not PairingGameGlobals.EndlessGame:
##             self.gameOver()

##         def handleTimeout(avIds, self=self):
##             self.notify.debug(
##                 'handleTimeout: avatars %s did not report "done"' %
##                 avIds)
##             self.setGameAbort()

##         self.gameDuration = 300
##         self.doneBarrier = ToonBarrier(
##             'waitClientsDone',
##             self.uniqueName('waitClientsDone'),
##             self.avIdList,
##             self.gameDuration + MinigameGlobals.latencyTolerance,
##             allToonsDone, handleTimeout)

##     def exitPlay(self):
##         self.doneBarrier.cleanup()
##         del self.doneBarrier        
##         pass



    def enterCleanup(self):
        """Enter cleanup state."""
        self.notify.debug("enterCleanup")
        self.gameFSM.request('off')

    def exitCleanup(self):
        """Exit cleanup state."""
        pass

    def enterWaitClientsChoices(self):
        """Wait for the clients to choose force and direction."""
        self.notify.debug("enterWaitClientsChoices")
        # Clear out choices for this round
        self.resetChoices()
        self.sendUpdate('setMatchAndRound', [self.curMatch, self.curRound])  
        # tell the clients their new state
        self.sendUpdate('setNewState',['inputChoice'])
        # Start the timeout
        taskMgr.doMethodLater(IceGameGlobals.InputTimeout,
                              self.waitClientsChoicesTimeout,
                              self.taskName("wait-choices-timeout"))
        self.sendUpdate("setTimerStartTime",
                        [globalClockDelta.getFrameNetworkTime()])
              
        pass

    def exitWaitClientsChoices(self):
        """Exit waiting for the clients to choose force and direction."""
        self.notify.debug("exitWaitClientsChoices")
        taskMgr.remove(self.taskName("wait-choices-timeout"))
        pass

    def enterProcessChoices(self):
        """Enter Process Choices State.

        For now let each machine do its own simulation.  If that's clunky,
        do it similar to golf, have one machine do everything then send,
        the movie out.  Difference now is that we have 4 objects moving
        around instead of 1.  Making message size a problem
        """
        forceAndHeading=[]
        for avId in self.avIdList:
            force = self.avatarChoices[avId][0]
            heading = self.avatarChoices[avId][1]
            forceAndHeading.append([force, heading])
        self.notify.debug('tireInputs = %s' % forceAndHeading)
        self.sendUpdate("setTireInputs", [forceAndHeading])
        self.gameFSM.request('waitEndingPositions')
        pass

    def exitProcessChoices(self):
        """Exit Process Choices State."""
        pass

    def enterWaitEndingPositions(self):
        """Wait for the clients to send their finished positions."""
        #TODO start a task to force this state to end
        if self.curRound == 0:
            self.takenTreasuresTable = [0] * self.numTreasures
            self.takenPenaltiesTable = [0] * self.numPenalties
        taskMgr.doMethodLater(IceGameGlobals.InputTimeout,
                              self.waitClientsChoicesTimeout,
                              self.taskName("endingPositionsTimeout"))        
        self.avatarEndingPositions = {}
        pass
    
    def exitWaitEndingPositions(self):
        """Exit Wait Ending Positions State."""
        taskMgr.remove(self.taskName("endingPositionsTimeout"))

    def enterProcessEndingPositions(self):
        """We've received the final positions from each client, arbitrate."""
        # TODO the ending positions should be very close to each other
        # The total number of physics steps taken tends to be +- 3
        # of the others
        # TODO detect if someone is wildly divergent from the others
        # TODO detect if someone is dead center
        averagePos = [Point3(0,0,0), Point3(0,0,0), Point3(0,0,0), Point3(0,0,0)]
        divisor = 0
        for avId in self.avatarEndingPositions.keys():
            divisor += 1
            oneClientEndingPositions = self.avatarEndingPositions[avId]
            avIndex = self.avIdList.index(avId)
            for index in xrange(len(oneClientEndingPositions)):
                pos = oneClientEndingPositions[index]
                averagePos[index] += Point3(pos[0], pos[1], pos[2])
                self.notify.debug('index = %d averagePos = %s' % (index,averagePos))
        sentPos = []
       
        if divisor:
            for newPos in averagePos:
                newPos /= divisor
                newPos.setZ(IceGameGlobals.TireRadius) # always ground them
                sentPos.append([newPos[0], newPos[1], newPos[2]])
        else:
            sentPos = self.finalEndingPositions
        self.sendUpdate('setFinalPositions', [sentPos])

        self.finalEndingPositions = sentPos

        # from here we can go to several different states
        # if the match is not over, go to waitClientsChoices
        # if the match is over, but not the game, go to scoring
        # if the game is over, go to finalResults
        if (self.curMatch == IceGameGlobals.NumMatches -1) and \
           (self.curRound == IceGameGlobals.NumRounds - 1):
            # end the game
            self.gameFSM.request('scoreMatch')
            pass
        elif self.curRound == IceGameGlobals.NumRounds - 1:
            # match is ending, score it
            self.gameFSM.request('scoreMatch')
            pass
        else:
            # match is not yet over
            self.curRound += 1
            self.sendUpdate('setMatchAndRound', [self.curMatch, self.curRound])
            self.gameFSM.request('waitClientsChoices')
        pass

    def exitProcessEndingPositions(self):
        """Exit Process Ending Positions State."""
        pass

    def enterScoreMatch(self):
        """Showing the clients final score from the 3 rounds."""
        #self.scoreCopy = self.scoreDict.deepCopy()
        sortedByDistance = []
        for avId in self.avIdList:
            # center is 0,0,0, so distance is pos.length()
            index = self.avIdList.index(avId)
            pos = Point3(*self.finalEndingPositions[index])
            pos.setZ(0)
            sortedByDistance.append ((avId, pos.length()))

        def compareDistance(x,y):
            if x[1] - y[1] > 0:
                return 1
            elif x[1] - y[1] < 0:
                return -1
            else:
                return 0
        sortedByDistance.sort(cmp = compareDistance)
        
        self.scoresAsList = []
        totalPointsAdded = 0
        for index in xrange(len(self.avIdList)):
            # since the center is at 0,0,0 just query the length
            pos = Point3(*self.finalEndingPositions[index])
            pos.setZ(0)
            length = pos.length()
            points = length / IceGameGlobals.FarthestLength * \
                     (IceGameGlobals.PointsInCorner - \
                      IceGameGlobals.PointsDeadCenter[self.numPlayers])
            points += IceGameGlobals.PointsDeadCenter[self.numPlayers]
            self.notify.debug('length = %s points=%s avId=%d' % (length, points, avId))
            avId = self.avIdList[index]
            bonusIndex = 0
            for sortIndex in xrange(len(sortedByDistance)):
                if sortedByDistance[sortIndex][0] == avId:
                    bonusIndex = sortIndex
            bonusIndex += 4 - len(self.avIdList)
            pointsToAdd = int( points + 0.5) + IceGameGlobals.BonusPointsForPlace[bonusIndex]
            totalPointsAdded += pointsToAdd
            self.scoreDict[avId] += pointsToAdd
            self.scoresAsList.append(self.scoreDict[avId])
        self.curMatch += 1
        self.curRound = 0
        self.sendUpdate('setScores', [self.curMatch, self.curRound, self.scoresAsList])
        self.sendUpdate('setNewState', ['scoring'])
            
        # set up a barrier to wait for the 'game done' msgs
        def allToonsScoringMovieDone(self=self):
            self.notify.debug('allToonsScoringMovieDone')
            if self.curMatch == IceGameGlobals.NumMatches:
                self.gameFSM.request('finalResults')
            else:
                self.gameFSM.request('waitClientsChoices')

        def handleTimeout(avIds, self=self):
            self.notify.debug(
                'handleTimeout: avatars %s did not report "done"' %
                avIds)
            #self.setGameAbort()
            if self.curMatch == IceGameGlobals.NumMatches:
                self.gameFSM.request('finalResults')
            else:
                self.gameFSM.request('waitClientsChoices')

        scoreMovieDuration = IceGameGlobals.FarthestLength * IceGameGlobals.ExpandFeetPerSec
        #scoreMovieDuration += len(self.avIdList) * IceGameGlobals.ScoreIncreaseDuration
        scoreMovieDuration += totalPointsAdded * IceGameGlobals.ScoreCountUpRate

        self.scoringMovieDoneBarrier = ToonBarrier(
            'waitScoringMovieDone',
            self.uniqueName('waitScoringMovieDone'),
            self.avIdList,
            scoreMovieDuration+ MinigameGlobals.latencyTolerance,
            allToonsScoringMovieDone, handleTimeout)
         
        pass

    def exitScoreMatch(self):
        """Exit Score Match state."""
        self.scoringMovieDoneBarrier.cleanup()
        self.scoringMovieDoneBarrier = None
        pass    

    def enterFinalResults(self):
        """Showing the clients final results from the 3 matches."""
        self.checkScores()
        self.sendUpdate('setNewState', ['finalResults'])
        taskMgr.doMethodLater(IceGameGlobals.ShowScoresDuration,
                              self.__doneShowingScores,
                              self.taskName("waitShowScores"))        
        pass

    def exitFinalResults(self):
        """Exit  Final Results state."""
        taskMgr.remove(self.taskName("waitShowScores"))         
        pass

    def __doneShowingScores(self, task):
        self.notify.debug('doneShowingScores')
        self.gameOver()
        return Task.done

    def waitClientsChoicesTimeout(self, task):
        self.notify.debug("waitClientsChoicesTimeout: did not hear from all clients")
        # Anybody who did not choose gets a 0 for their input
        for avId in self.avatarChoices.keys():
            if self.avatarChoices[avId] == (-1,0):
                self.avatarChoices[avId] = (0,0)

        # Go ahead and process choices
        self.gameFSM.request('processChoices')
        return Task.done
    
    def resetChoices(self):
        """Reset all avatar choices."""
        for avId in self.avIdList:
            # Initialize toons to -1 so we can tell they have not picked yet
            self.avatarChoices[avId] = (-1,0)


    def setAvatarChoice(self, force,  direction):
        """Handle getting 1 players choice for force and direction."""
        avatarId = self.air.getAvatarIdFromSender()
        self.notify.debug("setAvatarChoice: avatar: " + str(avatarId)
                          + " votes: " + str(force) + " direction: " + str(direction))

        # Record this choice in the choices dictionary
        # Check to make sure it is valid first
        self.avatarChoices[avatarId] = self.checkChoice(avatarId, force,direction)

        # See if everybody has chosen
        if self.allAvatarsChosen():
            self.notify.debug("setAvatarChoice: all avatars have chosen")
            self.gameFSM.request('processChoices')
        else:
            self.notify.debug("setAvatarChoice: still waiting for more choices")

    def checkChoice(self, avId, force, direction):
        """Make sure the avatar's choices are legal."""
        retForce = force
        retDir = direction
        if retForce < 0:
            retForce = 0
        if retForce > 100:
            retForce = 100

        return (retForce, retDir)

    def allAvatarsChosen(self):
        """
        Returns true if all avatars playing have chosen their votes
        """
        for avId in self.avatarChoices.keys():
            choice = self.avatarChoices[avId]
            if (choice[0] == -1) and not (self.stateDict[avId] == DistributedMinigameAI.EXITED):
                return False
        # If you get here, all avatars must have chosen
        return True           

    def endingPositions(self, positions):
        """Aribitrate on the ending positions."""
        if self.gameFSM.getCurrentState().getName() != 'waitEndingPositions':
            return
        self.notify.debug('got endingPositions from client %s' % positions)
        avId = self.air.getAvatarIdFromSender()
        self.avatarEndingPositions[avId] = positions
        if self.allAvatarsSentEndingPositions():
            self.gameFSM.request('processEndingPositions')

    def allAvatarsSentEndingPositions(self):
        """
        Returns true if all avatars playing have sent their ending positions
        """
        if len( self.avatarEndingPositions) == len(self.avIdList):
            return True
        return False

    def endingPositionsTimeout(self, task):
        """Handle the case when we clients didn't send ending positions."""
        self.notify.debug("endingPositionsTimeout : did not hear from all clients")
        # Go ahead and process choices
        self.gameFSM.request('processEndingPositions')
        return Task.done


    def reportScoringMovieDone(self):
        if self.gameFSM.getCurrentState().getName() != 'scoreMatch':
            return

        avId = self.air.getAvatarIdFromSender()
        # all of the objects on this avatar's client have landed
        # or been caught
        self.notify.debug('reportScoringMovieDone: avatar %s is done' % avId)
        self.scoringMovieDoneBarrier.clear(avId)

    def claimTreasure(self, treasureNum):
        # if the game just ended, ignore this message
        if self.gameFSM.getCurrentState().getName() != 'waitEndingPositions':
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
        if self.takenTreasuresTable[treasureNum]:
            return
        self.takenTreasuresTable[treasureNum] = 1

        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate("setTreasureGrabbed", [avId, treasureNum])
        self.scoreDict[avId] += 1
        self.numTreasuresTaken += 1


    def claimPenalty(self, penaltyNum):
        # if the game just ended, ignore this message
        if self.gameFSM.getCurrentState().getName() != 'waitEndingPositions':
            return
        # we're getting strange AI crashes where a toon claims
        # a penalty, and the toon is not listed in the scoreDict
        avId = self.air.getAvatarIdFromSender()
        if not self.scoreDict.has_key(avId):
            self.notify.warning(
                'PROBLEM: avatar %s called claimPenalty(%s) '
                'but he is not in the scoreDict: %s. avIdList is: %s' %
                (avId, penaltyNum, self.scoreDict, self.avIdList))
            return

        #self.notify.debug("penalty %s claimed by %s" % \
        #                  (penaltyNum, self.air.getAvatarIdFromSender()))

        # give the penalty to the first toon that claims it
        if penaltyNum < 0 or penaltyNum >= self.numPenalties:
            self.air.writeServerEvent('warning', penaltyNum, 'IceGameAI.claimPenalty penaltyNum out of range')
            return
        if self.takenPenaltiesTable[penaltyNum]:
            return
        self.takenPenaltiesTable[penaltyNum] = 1

        avId = self.air.getAvatarIdFromSender()
        self.sendUpdate("setPenaltyGrabbed", [avId, penaltyNum])
        self.scoreDict[avId] -= 1
        self.numPenaltiesTaken += 1

    def checkScores(self):
        """Force everyone to have at least a score of at least 1."""
        self.scoresAsList = []
        for index in xrange(len(self.avIdList)):
            # since the center is at 0,0,0 just query the length
            avId = self.avIdList[index]
            if self.scoreDict[avId]  < 0:
                self.scoreDict[avId] = 1 
            self.scoresAsList.append(self.scoreDict[avId])

