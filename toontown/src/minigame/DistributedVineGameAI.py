"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""

from DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import VineGameGlobals

class DistributedVineGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedVineGameAI_initialized
        except:
            self.DistributedVineGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedVineGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['play']),
                                    State.State('play',
                                                self.enterPlay,
                                                self.exitPlay,
                                                ['cleanup',
                                                 'waitShowScores']),
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

            # information for all toons
            # key is av Id
            # 0 vineIndex, if -1 then he's not attached to a vine is currently jumping
            # 1 vineT, where is he on the vine
            # 2 posX, - his x position when he jumped
            # 3 posZ - his z position when he jumped 
            # 4 facing right
            # 5 climb direction -1 going up, 0 standing still, 1 going down
            # 6 velX - his X velocity when he jumped
            # 7 velZ - his Z velocity when he jumped
            self.toonInfo = {}            

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)
            self.vineSections = []
            self.finishedBonus = {}
            self.finishedTimeLeft = {}
            self.totalSpiders = 0
            self.calculatedPartialBeans = False

    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")

        for avId in self.avIdList:
            self.updateToonInfo(avId, vineIndex = 0, vineT = VineGameGlobals.VineStartingT)
        
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules
        
        self.numTreasures = VineGameGlobals.NumVines -1
        self.numTreasuresTaken = 0
        self.takenTable = [0] * self.numTreasures
        
        # reset scores
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0
            self.finishedBonus[avId] = 0
            self.finishedTimeLeft[avId] = -1

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
        # Log balancing variables to the event server
        vineReached = []
        scoreList = []
        finishedList = []
        timeLeftList = []
        for avId in self.avIdList:
            vineReached.append(self.toonInfo[avId][0])
            scoreList.append(self.scoreDict[avId])
            finishedList.append(self.finishedBonus[avId])
            timeLeftList.append(self.finishedTimeLeft[avId])
        totalBats = len(VineGameGlobals.BatInfo[self.getSafezoneId()])
        self.air.writeServerEvent('minigame_vine',
                                  self.doId, '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
            ToontownGlobals.VineGameId,
            self.getSafezoneId(), self.avIdList, scoreList,
            self.vineSections, finishedList, timeLeftList,
            vineReached, self.totalSpiders, totalBats)) 
        
        # clean things up in this class
        self.gameFSM.request('cleanup')
        
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")
        self.vines = []
        index = 0

        # Start the game timer
        taskMgr.doMethodLater(VineGameGlobals.GameDuration,
                              self.timerExpired,
                              self.taskName("gameTimer"))        
        #vine = DistributedSwingVineAI.DistributedSwingVineAI(self.air, index, self.doId)
        #vine.generateWithRequired(self.zoneId)
        #self.vines.append(vine)

        # when the game is done, call gameOver()
        #self.gameOver()

    def exitPlay(self):
        taskMgr.remove(self.taskName("gameTimer"))
        for vine in self.vines:
            vine.requestDelete()
        pass
    

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def claimTreasure(self, treasureNum):
        # if the game just ended, ignore this message
        if self.gameFSM.getCurrentState().getName() != 'play':
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

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        if not VineGameGlobals.EndlessGame:
            self.gameFSM.request('waitShowScores')
        return Task.done  

    def enterWaitShowScores(self):
        self.notify.debug("enterWaitShowScores")
        self.awardPartialBeans()
        taskMgr.doMethodLater(VineGameGlobals.ShowScoresDuration,
                              self.__doneShowingScores,
                              self.taskName("waitShowScores"))

    def __doneShowingScores(self, task):
        self.notify.debug('doneShowingScores')
        self.gameOver()
        return Task.done

    def exitWaitShowScores(self):
        taskMgr.remove(self.taskName("waitShowScores"))    

    def reachedEndVine(self, vineIndex):
        """Handle client telling us he reached the end vine."""
        self.notify.debug('reachedEndVine')
        # since we client tells us each new vine he lands on, no need for this
        return
        avId = self.air.getAvatarIdFromSender()
        oldVineIndex = self.toonInfo[avId][0]
        self.updateToonInfo( avId, vineIndex = vineIndex)
        if not oldVineIndex == vineIndex:
            self.checkForEndVine(avId)
            self.checkForEndGame()        
    
    def setNewVine( self, avId, vineIndex, vineT, facingRight):
        """
        toon jumped to a new vine
        """
        self.notify.debug('setNewVine')
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'VineGameAI.setNewVine: invalid avId')
            return
        oldVineIndex = self.toonInfo[avId][0]
        debugStr = 'setNewVine doId=%s avId=%d vineIndex=%s oldVineIndex=%s' % (self.doId, avId, vineIndex, oldVineIndex)
        #self.notify.info('%s' % debugStr)
        #self.air.writeServerEvent('setNewVine',self.doId, '%s' % (debugStr))                
        self.updateToonInfo( avId, vineIndex = vineIndex, vineT = vineT, facingRight = facingRight)
        if not oldVineIndex == vineIndex:
            self.checkForEndVine(avId)
            self.checkForEndGame()

    def checkForEndGame(self):
        allDone = True
        for avId in self.toonInfo:
            if not self.toonInfo[avId][0] == VineGameGlobals.NumVines -1:
                allDone = False
                break
        if allDone:
            if not VineGameGlobals.EndlessGame:
                self.awardPartialBeans()
                self.sendUpdate('allAtEndVine', [])
                self.gameOver()            

    def checkForEndVine( self, avId):
        if self.toonInfo[avId][0] == VineGameGlobals.NumVines -1:
            # this toon has reached the end vine, give him bonus points
            curTime = self.getCurrentGameTime()
            timeLeft = VineGameGlobals.GameDuration - curTime 
            self.notify.debug('curTime =%s timeLeft = %s' % (curTime, timeLeft))
            # we're getting strange AI crashes where a toon claims
            # a treasure, and the toon is not listed in the scoreDict
            if not self.scoreDict.has_key(avId):
                self.notify.warning(
                    'PROBLEM: avatar %s called claimTreasure(%s) '
                    'but he is not in the scoreDict: %s. avIdList is: %s' %
                    (avId, treasureNum, self.scoreDict, self.avIdList))
                return
            addBonus =  int( VineGameGlobals.BaseBonusOnEndVine[self.getSafezoneId()] + \
                                    VineGameGlobals.BonusPerSecondLeft * timeLeft )
            self.notify.debug('addBOnus = %d' % addBonus)
            if addBonus < 0:
                addBonus = 0
            self.finishedBonus[avId] = addBonus
            timeLeftStr = '%.1f' % timeLeft
            self.finishedTimeLeft[avId] = timeLeftStr
            self.scoreDict[avId] += addBonus
            self.sendUpdate("setScore", [avId, self.scoreDict[avId]])

    def updateToonInfo( self, avId, vineIndex = None, vineT =None, posX = None, posZ = None, facingRight = None, climbDir = None, velX = None, velZ = None):
        """
        Update the toon info, if it's None don't change it
        """
        newVineIndex = vineIndex
        newVineT = vineT
        newPosX = posX
        newPosZ = posZ
        newFacingRight = facingRight
        newClimbDir = climbDir
        newVelX = velX
        newVelZ = velZ
        oldInfo = None
        if self.toonInfo.has_key(avId):
            oldInfo = self.toonInfo[avId]
            if vineIndex == None:
                newVineIndex = oldInfo[0]
            if vineT == None:
                newVineT = oldInfo[1]
            if posX == None:
                newPosX = oldInfo[2]
            if posZ == None:
                newPosZ = oldInfo[3]
            if facingRight == None:
                newFacingRight = oldInfo[4]
            if climbDir == None:
                newClimbDir = oldInfo[5]
            if velX == None:
                newVelX = oldInfo[6]
            if velZ == None:
                newVelZ = oldInfo[7]
            
            
        if (newVineIndex < -1) or (newVineIndex >= VineGameGlobals.NumVines):
            #self.notify.warning('invalid vineIndex for %d, forcing 0' % avId)
            newVineIndex = 0
        if (newVineT < 0) or (newVineT > 1):
            #self.notify.warning('invalid vineT for %d, setting to 0' % avId)
            pass
        if not (newFacingRight == 0 or newFacingRight == 1):
            #self.notify.warning('invalid facingRight for %d, forcing to 1' % avId)
            newFacingRight = 1
        if (newPosX < -1000) or (newPosX > 2000):
            #self.notify.warning('invalid posX for %d, forcing to 0' % avId)
            newPosX = 0
        if (newPosZ < -100) or (newPosZ > 1000):
            #self.notify.warning('invalid posZ for %d, forcing to 0' % avId)
            newPosZ = 0
        if (newVelX < -1000) or (newVelX > 1000):
            #self.notify.warning('invalid velX for %d, forcing to 0' % avId)
            newVelX = 0
        if (newVelZ < -1000) or (newVelZ > 1000):
            #self.notify.warning('invalid velZ for %d, forcing to 0' % avId)
            newVelZ = 0                        
        newInfo = [newVineIndex, newVineT, newPosX, newPosZ, newFacingRight, newClimbDir, newVelX, newVelZ]
        
        self.toonInfo[avId] = newInfo

    def setupVineSections(self):
        """
        figure out our course, we can repeat sections
        """
        szId = self.getSafezoneId()
        courseWeights = VineGameGlobals.CourseWeights[szId]
        pool = [[],[],[],[],[],[]]
        for weights in courseWeights:
            section, chances = weights
            numSpiders = VineGameGlobals.getNumSpidersInSection(section)
            pool[numSpiders] += [section] * chances

        maxSpiders = VineGameGlobals.SpiderLimits[szId]
        curSpiders = 0
        for i in range(4):
            spidersLeft = maxSpiders - curSpiders
            validChoices = []
            for numSpiders in range(spidersLeft+1):
                validChoices += pool[numSpiders]
            if not validChoices:
                self.notify.warning('we ran out of valid choices szId=%s, vineSections=%s' %
                                    (szId, self.vineSections))
                validChoices += [0]
            section = random.choice(validChoices)
            curSpiders += VineGameGlobals.getNumSpidersInSection(section)
            self.vineSections.append(section)
            
        self.totalSpiders = curSpiders
        self.notify.debug('calc vineSections = %s' % self.vineSections)

    def getVineSections(self):
        return self.vineSections

    def setTrolleyZone(self, trolleyZone):
        # we need the trolley zone before we can do the vine sections, so do it here
        DistributedMinigameAI.setTrolleyZone(self, trolleyZone)
        self.setupVineSections()

    def awardPartialBeans(self):
        """Give the players some beans for partial completion of the course."""
        if self.calculatedPartialBeans:
            return

        self.calculatedPartialBeans = True
        for avId in self.avIdList:
            vineIndex = self.toonInfo[avId][0]
            if not vineIndex == VineGameGlobals.NumVines -1:
                partialBeans = int( vineIndex / 5.0)
                if self.scoreDict.has_key(avId):
                    self.scoreDict[avId] += partialBeans
                    self.sendUpdate("setScore", [avId, self.scoreDict[avId]])        
                
