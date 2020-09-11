"""DistributedTwoDGameAI module: contains the DistributedTwoDGameAI class"""

from DistributedMinigameAI import *
from toontown.ai.ToonBarrier import *
from direct.fsm import ClassicFSM, State
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import ToonBlitzGlobals
from math import sqrt

class DistributedTwoDGameAI(DistributedMinigameAI):    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTwoDGameAI')
    
    def __init__(self, air, minigameId):
        try:
            self.DistributedTwoDGameAI_initialized
        except:
            self.DistributedTwoDGame_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)
            
##            simbase.mgAI = self
            
            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTwoDGameAI',
                                   [
                                    State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['play']),
                                    State.State('play',
                                                self.enterPlay,
                                                self.exitPlay,
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
            
            self.finishedBonusDict = {}
            self.finishedTimeLeftDict = {}
            self.numFallDownDict = {}
            self.numHitByEnemyDict = {}
            self.numSquishDict = {}
            self.treasuresCollectedDict = {}
            self.sectionsSelected = []
            self.enemyHealthTable = []
            self.treasureTakenTable = []
            self.sectionIndexList = []

    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    def setTrolleyZone(self, trolleyZone):
        # We need the trolley zone before we can setup the sections, so do it here
        DistributedMinigameAI.setTrolleyZone(self, trolleyZone)
        self.setupSections()
    
    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules
        
        # @TODO: Samik 05/29/08: DistributedTwoDGameAI should decide self.numTreasures & self.numEnemies.
        # It shouldn't directly get it from ToonBlitzGlobals.
        self.numTreasures = ToonBlitzGlobals.NumTreasures
        self.numEnemies = ToonBlitzGlobals.NumEnemies
        self.numTreasuresTaken = 0
        self.numEnemiesKilled = 0
        
        # Reset scores
        for avId in self.scoreDict.keys():
            self.scoreDict[avId] = 0
            self.finishedBonusDict[avId] = 0
            self.finishedTimeLeftDict[avId] = -1
            self.numFallDownDict[avId] = 0
            self.numHitByEnemyDict[avId] = 0
            self.numSquishDict[avId] = 0
            self.treasuresCollectedDict[avId] = [0, 0, 0, 0] # [value1, value2, value3, value4]

        # Maintaining a table for enemy health and another table for treasure taken
        for i in xrange(len(self.sectionsSelected)):
            sectionIndex = self.sectionsSelected[i][0]
            attribs = ToonBlitzGlobals.SectionTypes[sectionIndex]
            enemiesPool = attribs[3]
            # Set up enemy health table
            self.enemyHealthTable += [[]]
            enemyIndicesSelected = self.sectionsSelected[i][1]
            for j in xrange(len(enemyIndicesSelected)):
                # Maintaining this enemy's health in enemyHealthTable
                enemyIndex = enemyIndicesSelected[j]
                enemyType = enemiesPool[enemyIndex][0]
                self.enemyHealthTable[i] += [ToonBlitzGlobals.EnemyBaseHealth]
                self.enemyHealthTable[i][j] *= self.numPlayers
                if ToonBlitzGlobals.EnemyHealthMultiplier.has_key(enemyType):
                    self.enemyHealthTable[i][j] *= ToonBlitzGlobals.EnemyHealthMultiplier[enemyType]
                    
            # Set up the treasure taken table
            self.treasureTakenTable += [[]]
            treasureIndicesSelected = self.sectionsSelected[i][2]
            for j in xrange(len(treasureIndicesSelected)):
                # Maintaining this treasure's taken flag in treasureTakenTable
                self.treasureTakenTable[i] += [0]
            # Adding the enemy generated treasures to this list also.
            enemyIndicesSelected = self.sectionsSelected[i][1]
            for j in xrange(len(enemyIndicesSelected)):
                self.treasureTakenTable[i] += [0]

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
        scoreList = []
        finishedBonusList = []
        timeLeftList = []
        treasureCollectedList = []
        playerErrorList = []
        
        for avId in self.avIdList:
            scoreList.append(self.scoreDict[avId])
            finishedBonusList.append(self.finishedBonusDict[avId])
            timeLeftList.append(self.finishedTimeLeftDict[avId])
            treasureCollectedList.append(self.treasuresCollectedDict[avId])
            playerError = [self.numFallDownDict[avId], self.numHitByEnemyDict[avId], self.numSquishDict[avId]]
            playerErrorList.append(playerError)
            self.scoreDict[avId] = max(0, self.scoreDict[avId])
            jellybeans = sqrt(self.scoreDict[avId] * ToonBlitzGlobals.ScoreToJellyBeansMultiplier)
            self.scoreDict[avId] = max(1, int(jellybeans))
            
        self.air.writeServerEvent('minigame_twoD',
                                  self.doId, '%s|%s|%s|%s|%s|%s|%s|%s|%s' 
                                  %(ToontownGlobals.TwoDGameId, self.getSafezoneId(),
                                  self.avIdList, scoreList, finishedBonusList, 
                                  timeLeftList, treasureCollectedList, playerErrorList,
                                  self.sectionIndexList))
            
        self.notify.debug('minigame_twoD%s: %s|%s|%s|%s|%s|%s|%s|%s|%s'
                          %(self.doId, ToontownGlobals.TwoDGameId,
                          self.getSafezoneId(), self.avIdList, 
                          scoreList, finishedBonusList, timeLeftList,
                          treasureCollectedList, playerErrorList,
                          self.sectionIndexList))
        
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
        
        # set up a barrier to wait for the 'game done' msgs
        def allToonsDone(self=self):
            self.notify.debug('allToonsDone')
            self.sendUpdate('setEveryoneDone')
            if not ToonBlitzGlobals.EndlessGame:
                # Show scores here and then end game
                self.gameOver()

        def handleTimeout(avIds, self=self):
            self.notify.debug('handleTimeout: avatars %s did not report "done"' %avIds)
            self.setGameAbort()
        
        self.doneBarrier = ToonBarrier(
            'waitClientsDone',
            self.uniqueName('waitClientsDone'),
            self.avIdList,
            ToonBlitzGlobals.GameDuration[self.getSafezoneId()] + \
            ToonBlitzGlobals.ShowScoresDuration + MinigameGlobals.latencyTolerance,
            allToonsDone,
            handleTimeout)
        
        # when the game is done, call gameOver()
##        self.gameOver()

    def exitPlay(self):
        pass
    
    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        
        self.doneBarrier.cleanup()
        del self.doneBarrier
        
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def claimTreasure(self, sectionIndex, treasureIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('treasure %s-%s claimed by %s' %(sectionIndex, treasureIndex, avId))
        
        # Check validitiy of sectionIndex
        if (sectionIndex < 0) or (sectionIndex >= len(self.sectionsSelected)):
            self.air.writeServerEvent('warning', sectionIndex, 'TwoDGameAI.claimTreasure sectionIndex out of range.')
            return
        # Check validitiy of treasureIndex
        if (treasureIndex < 0) or (treasureIndex >= len(self.treasureTakenTable[sectionIndex])):
            self.notify.warning('Treasure %s: TwoDGameAI.claimTreasure treasureIndex out of range.' %treasureIndex)
            self.air.writeServerEvent('warning', treasureIndex, 'TwoDGameAI.claimTreasure treasureIndex out of range.')
            return
        # Give the treasure only to the first toon that claims it.
        if self.treasureTakenTable[sectionIndex][treasureIndex]:
            return
        
        initialTreasureList = self.sectionsSelected[sectionIndex][2]
        if (treasureIndex < len(initialTreasureList)):
            # treasureValue can be found from what the AI had initially determined it.
            treasureValue = initialTreasureList[treasureIndex][1]
        else:
            # This is the case of a enemy generated treasure.
            treasureValue = self.numPlayers
        self.treasureTakenTable[sectionIndex][treasureIndex] = treasureValue
        # Register count
        self.treasuresCollectedDict[avId][treasureValue - 1] += 1
        self.scoreDict[avId] += ToonBlitzGlobals.ScoreGainPerTreasure * treasureValue
        self.numTreasuresTaken += 1
        
        self.sendUpdate("setTreasureGrabbed", [avId, sectionIndex, treasureIndex])
        
    def claimEnemyShot(self, sectionIndex, enemyIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('enemy %s-%s shot claimed by %s' %(sectionIndex, enemyIndex, avId))
        
        # Check validitiy of sectionIndex
        if (sectionIndex < 0) or (sectionIndex >= len(self.sectionsSelected)):
            self.air.writeServerEvent('warning', sectionIndex, 'TwoDGameAI.claimEnemyShot sectionIndex out of range.')
            return
        # Check validitiy of enemyIndex
        if (enemyIndex < 0) or (enemyIndex >= len(self.sectionsSelected[sectionIndex][1])):
            self.air.writeServerEvent('warning', enemyIndex, 'TwoDGameAI.claimEnemyShot enemyIndex out of range.')
            return
        
        # send update only if the enemy's health > 0
        if (self.enemyHealthTable[sectionIndex][enemyIndex] > 0):
            self.enemyHealthTable[sectionIndex][enemyIndex] -= ToonBlitzGlobals.DamagePerBullet
            if (self.enemyHealthTable[sectionIndex][enemyIndex] <= 0):
                self.numEnemiesKilled += 1
##                # Add a treasure slot to the treasureTakenTable
##                self.treasureTakenTable[sectionIndex] += [0]
            self.sendUpdate('setEnemyShot', [avId, sectionIndex, enemyIndex, self.enemyHealthTable[sectionIndex][enemyIndex]])
            
    def reportDone(self):
        if self.gameFSM.getCurrentState().getName() != 'play':
            return
        
        avId = self.air.getAvatarIdFromSender()
        # This avatar client's timer is up
        self.notify.debug('reportDone: avatar %s is done' % avId)
        self.doneBarrier.clear(avId)
        
    def toonVictory(self, avId, timestamp):
        """ Called when a remote toon reaches the end of tunnel. """
        if avId not in self.scoreDict.keys():
            self.notify.warning('Avatar %s not in list.' %avId)
            self.air.writeServerEvent('suspicious: ', avId, 'TwoDGameAI.toonVictory toon not in list.')
            return
        
        # This toon has reached the end. Give him bonus points.
        curTime = self.getCurrentGameTime()
        timeLeft = ToonBlitzGlobals.GameDuration[self.getSafezoneId()] - curTime
        self.notify.debug('curTime =%s timeLeft = %s' % (curTime, timeLeft))
        addBonus = int(ToonBlitzGlobals.BaseBonusOnCompletion[self.getSafezoneId()] + \
                       ToonBlitzGlobals.BonusPerSecondLeft * timeLeft)
        self.notify.debug('addBOnus = %d' % addBonus)
        if addBonus < 0:
            addBonus = 0
        
        self.finishedBonusDict[avId] = addBonus
        timeLeftStr = '%.1f' %timeLeft
        self.finishedTimeLeftDict[avId] = timeLeftStr
        self.scoreDict[avId] += addBonus
        
        self.sendUpdate("addVictoryScore", [avId, addBonus])
        
        if self.gameFSM.getCurrentState().getName() != 'play':
            return
        self.doneBarrier.clear(avId)
    
    def toonFellDown(self, avId, timestamp):
        """ Called when a toon falls through a hole."""
        if avId not in self.scoreDict.keys():
            self.notify.warning('Avatar %s not in list.' %avId)
            self.air.writeServerEvent('warning', avId, 'TwoDGameAI.toonFellDown toon not in list.')
            return
        
        # Register count
        self.numFallDownDict[avId] += 1
        # Subtract score for that toon
        self.scoreDict[avId] += ToonBlitzGlobals.ScoreLossPerFallDown[self.getSafezoneId()]
        
    def toonHitByEnemy(self, avId, timestamp):
        """ Called when a toon is hit by suit """
        if avId not in self.scoreDict.keys():
            self.notify.warning('Avatar %s not in list.' %avId)
            self.air.writeServerEvent('warning', avId, 'TwoDGameAI.toonHitByEnemy toon not in list.')
            return
        
        # Register count
        self.numHitByEnemyDict[avId] += 1
        # Subtract score for that toon
        self.scoreDict[avId] += ToonBlitzGlobals.ScoreLossPerEnemyCollision[self.getSafezoneId()]
        
    def toonSquished(self, avId, timestamp):
        """ Called when a toon is squished by a stomper."""
        if avId not in self.scoreDict.keys():
            self.notify.warning('Avatar %s not in list.' %avId)
            self.air.writeServerEvent('warning', avId, 'TwoDGameAI.toonSquished toon not in list.')
            return
        
        # Register count
        self.numSquishDict[avId] += 1
        # Subtract score for that toon
        self.scoreDict[avId] += ToonBlitzGlobals.ScoreLossPerStomperSquish[self.getSafezoneId()]
    
    def setupSections(self):
        """ Make a course by selecting sections based on difficulty and probability of occurence in that safeZone."""
        szId = self.getSafezoneId()
        sectionWeights = ToonBlitzGlobals.SectionWeights[szId]
        numSections = ToonBlitzGlobals.NumSections[szId]
        difficultyPool = []
        difficultyList = []
        sectionsPool = ToonBlitzGlobals.SectionsPool
        sectionTypes = ToonBlitzGlobals.SectionTypes
        sectionsPoolByDifficulty = [[], [], [], [], [], []]
        sectionsSelectedByDifficulty = [[], [], [], [], [], []]
        sectionIndicesSelected = []
        for weight in sectionWeights:
            difficulty, probability = weight
            difficultyPool += [difficulty] * probability
        
        # Now make a list of difficulty from the difficultyPool
        for i in xrange(numSections):
            difficulty = random.choice(difficultyPool)
            difficultyList.append(difficulty)
        # Sort the difficultyList so that the more difficult sections appear at the end of the game
        difficultyList.sort()
        
        # Split SectionsPool into sectionsPoolByDifficulty
        for sectionIndex in sectionsPool:
            difficulty = sectionTypes[sectionIndex][0]
            sectionsPoolByDifficulty[difficulty] += [sectionIndex]   
        
        # Now go through the difficutly list, and select a section from the sectionsPool with that difficulty
        # Do not repeat. If we are out of sections with that difficulty take one from the next difficulty level
        for targetDifficulty in difficultyList:
            whileCount = 0
            difficulty = targetDifficulty
            # If there is no section left to pick from that difficulty level pick one from the next difficulty level
            while not (len(sectionsPoolByDifficulty[difficulty]) > 0):
                difficulty += 1
                if (difficulty >= 5):
                    difficulty = 0
                    whileCount += 1
                    if (whileCount > 1):
                        break
            else:
                sectionIndexChoice = random.choice(sectionsPoolByDifficulty[difficulty])
                # Adding this sectionIndex to the list of selectedSections
                sectionsSelectedByDifficulty[difficulty] += [sectionIndexChoice]
                # Removing this sectionIndex from the list of sectionsPoolByDifficulty
                sectionsPoolByDifficulty[difficulty].remove(sectionIndexChoice)
                
            if (whileCount > 1):
                self.notify.debug('We need more sections than we have choices. We have to now repeat.')
        
        # Fill up sectionIndicesSelected from sectionsSelectedByDifficulty to maintain 1 comprehensive list
        for i in xrange(len(sectionsSelectedByDifficulty)):
            for j in xrange(len(sectionsSelectedByDifficulty[i])):
                sectionIndicesSelected.append(sectionsSelectedByDifficulty[i][j])
        
        # Now go through the sectionIndicesSelected and get their properties
        for i in xrange(len(sectionIndicesSelected)):
            sectionIndex = sectionIndicesSelected[i]
            self.sectionIndexList.append(sectionIndex)
            attribs = sectionTypes[sectionIndex]
            difficulty = attribs[0]
            length = attribs[1]
            blocksPool = attribs[2]
            enemiesPool = attribs[3]
            treasuresPool = attribs[4]
            spawnPointsPool = attribs[5]
            stompersPool = attribs[6]
            
            # Select a random list of numEnemies enemyIndices from the enemyIndicesPool
            enemyIndicesPool = []
            enemyIndicesSelected = []
            if (enemiesPool != None):
                minEnemies, maxEnemies = attribs[7]
                for i in xrange(len(enemiesPool)):
                    enemyIndicesPool += [i]
                numEnemies = maxEnemies * ToonBlitzGlobals.PercentMaxEnemies[szId] / 100
                numEnemies = max(numEnemies, minEnemies)
                for j in xrange(int(numEnemies)):
                    if (len(enemyIndicesPool) == 0):
                        break
                    enemyIndex = random.choice(enemyIndicesPool)
                    enemyIndicesSelected.append(enemyIndex)
                    enemyIndicesPool.remove(enemyIndex)            
                # Sort the indices in enemyIndicesSelected so that they appear in the right order of location in a section
                enemyIndicesSelected.sort()
                
            # Select a random list of numTreasures treasureIndices from the treasureIndicesPool
            treasureIndicesPool = []
            # 1 value treasures have a 40% chance of getting picked and the 4 value treasures have only a 10% chance of getting picked.
            treasureValuePool = []
            for value in range(1, 5):
                treasureValuePool += [value] * ToonBlitzGlobals.TreasureValueProbability[value]
            treasureIndicesSelected = []
            if (treasuresPool != None):
                minTreasures, maxTreasures = attribs[8]
                for i in xrange(len(treasuresPool)):
                    treasureIndicesPool += [i]
                numTreasures = maxTreasures * ToonBlitzGlobals.PercentMaxTreasures[szId] / 100
                numTreasures = max(numTreasures, minTreasures)
                for i in xrange(int(numTreasures)):
                    if (len(treasureIndicesPool) == 0):
                        break
                    treasureIndex = random.choice(treasureIndicesPool)
                    treasureValue = random.choice(treasureValuePool)
                    treasure = (treasureIndex, treasureValue)
                    treasureIndicesPool.remove(treasureIndex)
                    treasureIndicesSelected.append(treasure)
                # Sort the indices in treasureIndicesSelected so that they appear in the right order of location in a section
                treasureIndicesSelected.sort()
                
            # Select a random list of numSpawnPoints spawnPointIndices from the spawnPointIndicesPool
            spawnPointIndicesPool = []
            spawnPointIndicesSelected = []
            if (spawnPointsPool != None):
                minSpawnPoints, maxSpawnPoints = attribs[9]                
                for i in xrange(len(spawnPointsPool)):
                    spawnPointIndicesPool += [i]
                numSpawnPoints = maxSpawnPoints * ToonBlitzGlobals.PercentMaxSpawnPoints[szId] / 100
                numSpawnPoints = max(numSpawnPoints, minSpawnPoints)
                for i in xrange(int(numSpawnPoints)):
                    if (len(spawnPointIndicesPool) == 0):
                        break
                    spawnPoint = random.choice(spawnPointIndicesPool)
                    spawnPointIndicesSelected.append(spawnPoint)
                    spawnPointIndicesPool.remove(spawnPoint)
                # Sort the spawnPoints in a section so that they appear in the right order in the section
                spawnPointIndicesSelected.sort()
            
            # Select a random list of numStompers stomperIndices from the stomperIndicesPool
            stomperIndicesPool = []
            stomperIndicesSelected = []
            if (stompersPool != None):
                minStompers, maxStompers = attribs[10]
                for i in xrange(len(stompersPool)):
                    stomperIndicesPool += [i]
                numStompers = maxStompers * ToonBlitzGlobals.PercentMaxStompers[szId] / 100
                numStompers = max(numStompers, minStompers)
                for i in xrange(int(numStompers)):
                    if (len(stomperIndicesPool) == 0):
                        break
                    stomper = random.choice(stomperIndicesPool)
                    stomperIndicesSelected.append(stomper)
                    stomperIndicesPool.remove(stomper)
                # Sort the indices in stomperIndicesSelected so that they appear in the right order of location in a section
                stomperIndicesSelected.sort()
            
            # Change these attribs and make a tuples: (sectionIndex, enemyIndicesSelected, treasureIndicesSelected, spawnPointIndicesPool)
            # The clients can take the length and the blockList from ToonBlitzGlobals.SectionTypes
            sctionTuple = (sectionIndex, enemyIndicesSelected, treasureIndicesSelected, spawnPointIndicesSelected, stomperIndicesSelected)
            self.sectionsSelected.append(sctionTuple)
            
        # self.sectionsSelected is the finalised list of sections along with enemyIndices, treasureIndices, spawnPointIndices of each section.
        
    def getSectionsSelected(self):
        return self.sectionsSelected