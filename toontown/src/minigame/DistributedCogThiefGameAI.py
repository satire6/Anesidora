"""DistributedCogThiefGameAI module: contains the DistributedCogThiefGameAI class"""
import random
from pandac.PandaModules import Point3
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task
from toontown.minigame import DistributedMinigameAI
from toontown.minigame import MinigameGlobals
from toontown.minigame import CogThiefGameGlobals

CTGG = CogThiefGameGlobals
class DistributedCogThiefGameAI(DistributedMinigameAI.DistributedMinigameAI):
    """Client side class for the cog thief  game."""
    notify = directNotify.newCategory("DistributedCogThiefGameAI")
    
    ExplodeWaitTime = 6.0 + CTGG.LyingDownDuration # computed by hitTrack.getDuration
    
    def __init__(self, air, minigameId):
        try:
            self.DistributedCogThiefGameAI_initialized
        except:
            self.DistributedCogThiefGameAI_initialized = 1
            DistributedMinigameAI.DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedCogThiefGameAI',
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
            
            self.cogInfo = {}
            self.barrelInfo = {}


            self.initBarrelInfo()

    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        self.removeAllTasks()
        DistributedMinigameAI.DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        self.initCogInfo()
        DistributedMinigameAI.DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        score = int( CTGG.calcScore(self.getCurrentGameTime()))
        # give everyone that many jbeans
        for avId in self.avIdList:
            self.scoreDict[avId] = score

        # give bonus for saving all the barrels
        if self.getNumBarrelsStolen() == 0:
            # give out the bonuses
            for avId in self.avIdList:
                self.scoreDict[avId] += CTGG.PerfectBonus[len(self.avIdList)-1]
                self.logPerfectGame(avId)            
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")
        self.startSuitGoals()
        # when the game is done, call gameOver()
        #self.gameOver()

        # Start the game timer
        if not config.GetBool('cog-thief-endless', 0):
            taskMgr.doMethodLater(CTGG.GameTime,
                                  self.timerExpired,
                                  self.taskName("gameTimer"))

    def exitPlay(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        taskMgr.remove(self.taskName("gameTimer"))
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass


    def initCogInfo(self):
        """For each cog, initialize the info about him."""
        for cogIndex in xrange(self.getNumCogs()):
            self.cogInfo[cogIndex] = {
                'pos' : Point3(CogThiefGameGlobals.CogStartingPositions[cogIndex]),
                'goal' : CTGG.NoGoal,
                'goalId' : CTGG.InvalidGoalId, # avatar id if he's chasing a toon, barrel index otherwise
                'barrel' : CTGG.NoBarrelCarried
                }

    def initBarrelInfo(self):
        """For each barrel, initialize the info about him."""
        for barrelIndex in xrange(CogThiefGameGlobals.NumBarrels):
            self.barrelInfo[barrelIndex] = {
                'pos' : Point3(CogThiefGameGlobals.BarrelStartingPositions[barrelIndex]),
                'carriedBy' : CTGG.BarrelOnGround,
                'stolen' : False,
                }

    def makeCogCarryBarrel(self, timestamp, clientStamp, cogIndex, barrelIndex):
        """Make the cog carry a barrel."""
        if cogIndex in self.cogInfo and barrelIndex in self.barrelInfo:
            self.barrelInfo[barrelIndex]['carriedBy'] = cogIndex
            self.cogInfo[cogIndex]['barrel'] = barrelIndex
        else:
            self.notify.warning('makeCogCarryBarrel invalid cogIndex=%s barrelIndex=%s'
                                % (cogIndex, barrelIndex))

    def b_makeCogCarryBarrel(self, clientStamp, cogIndex, barrelIndex):
        """Tell AI and clients to make the cog carry the barrel."""
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.notify.debug('b_makeCogCarryBarrel timeStamp=%s clientStamp=%s cog=%s barrel=%s' %
                          (timestamp, clientStamp, cogIndex, barrelIndex))
        self.makeCogCarryBarrel(timestamp, clientStamp, cogIndex, barrelIndex)
        self.d_makeCogCarryBarrel(timestamp, clientStamp, cogIndex, barrelIndex)

    def d_makeCogCarryBarrel(self, timestamp, clientStamp, cogIndex, barrelIndex):
        """Tell the clients the cog is carrying a barrel."""
        pos = self.cogInfo[cogIndex]['pos']
        gameTime = self.getCurrentGameTime()
        self.sendUpdate('makeCogCarryBarrel', [timestamp, clientStamp, cogIndex, barrelIndex,
                                               pos[0], pos[1], pos[2]])

    def makeCogDropBarrel(self, timestamp, clientStamp, cogIndex, barrelIndex, barrelPos):
        """Make the cog drop a barrel."""
        if cogIndex in self.cogInfo and barrelIndex in self.barrelInfo:
            self.barrelInfo[barrelIndex]['carriedBy'] = CTGG.BarrelOnGround
            self.cogInfo[cogIndex]['barrel'] = CTGG.NoBarrelCarried
        else:
            self.notify.warning('makeCogDropBarrel invalid cogIndex=%s barrelIndex=%s'
                                % (cogIndex, barrelIndex))

    def b_makeCogDropBarrel(self, clientStamp, cogIndex, barrelIndex, barrelPos):
        """Tell AI and clients to make the cog drop the barrel."""
        if self.barrelInfo[barrelIndex]['carriedBy'] != cogIndex:
            self.notify.error("self.barrelInfo[%s]['carriedBy'] != %s" %
                              (barrelIndex, cogIndex))
        
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.makeCogDropBarrel(timestamp, clientStamp, cogIndex, barrelIndex, barrelPos)
        self.d_makeCogDropBarrel(timestamp, clientStamp, cogIndex, barrelIndex, barrelPos)

    def d_makeCogDropBarrel(self, timestamp, clientStamp, cogIndex, barrelIndex, barrelPos):
        """Tell the clients the cog is droping a barrel."""
        pos = barrelPos
        gameTime = self.getCurrentGameTime()    
        self.sendUpdate('makeCogDropBarrel', [timestamp, clientStamp, cogIndex, barrelIndex,
                                               pos[0], pos[1], pos[2]])            

    def isCogCarryingABarrel(self, cogIndex):
        """Return true if the cog is carrying any barrel."""
        result = self.cogInfo[cogIndex]['barrel'] > CTGG.NoBarrelCarried
        return result
    
    def isCogCarryingThisBarrel(self, cogIndex, barrelIndex):
        """Return true if the cog is carrying this barrel."""
        result = self.cogInfo[cogIndex]['barrel'] == barrelIndex
        return result    

    def startSuitGoals(self):
        """For each suit, give him something to do."""
        # lets start with one suit, chasing a toon
        #avId = self.avIdList[0]
        #self.chaseToon(0, avId)
        #self.chaseBarrel(0, 0)
        delayTimes = []
        for cogIndex in xrange(self.getNumCogs()):
            delayTimes.append(cogIndex *1.0)
        random.shuffle(delayTimes)
        for cogIndex in xrange(self.getNumCogs()):        
            self.doMethodLater(delayTimes[cogIndex], self.chooseSuitGoal,
                               self.uniqueName('choseSuitGoal-%d-' % cogIndex),
                               extraArgs = [cogIndex])            


    def chaseToon(self, suitNum, avId):
        """Have this suit chase the toon."""
        goalType = CTGG.ToonGoal
        goalId = avId
        self.cogInfo[suitNum]['goal'] = goalType
        self.cogInfo[suitNum]['goalId'] = goalId
        pos = self.cogInfo[suitNum]['pos']
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.notify.debug('chaseToon time=%s suitNum=%s, avId=%s' %(timestamp,
                                                                    suitNum, avId))
        gameTime = self.getCurrentGameTime()
        self.sendUpdate('updateSuitGoal', [timestamp, timestamp, suitNum,  goalType, goalId,
                                           pos[0],pos[1], pos[2]])

    def hitBySuit(self, avId, timestamp, suitNum, x, y ,z):
        """A toon hit a suit, have the suit do something else."""
        assert self.notify.debugStateCall(self)        
        if suitNum >= self.getNumCogs() :
            self.notify.warning('hitBySuit, possible hacker avId=%s' % avId)
            return
        
        barrelIndex = self.cogInfo[suitNum]['barrel']

        # we must set the cog pos before we drop barrel,
        # as that's where we drop the barrel
        if barrelIndex >= 0:
            # the x,y,z we get is actually the cog position, but we drop the
            # barrel right on it
            barrelPos = Point3(x,y,z)
            self.b_makeCogDropBarrel(timestamp, suitNum,  barrelIndex, barrelPos)
        
        startPos = CTGG.CogStartingPositions[suitNum]
        self.cogInfo[suitNum]['pos'] = startPos

        self.cogInfo[suitNum]['goal'] = CTGG.NoGoal
        self.cogInfo[suitNum]['goalId'] = CTGG.InvalidGoalId
        self.sendSuitSync(timestamp, suitNum)
        
        # TODO figure out if we want to chase a toon or go for a barrel
        self.doMethodLater(self.ExplodeWaitTime, self.chooseSuitGoal,
                           self.uniqueName('choseSuitGoal-%d-' % suitNum),
                           extraArgs = [suitNum])

    def sendSuitSync(self, clientstamp, suitNum):
        """Whatever this suit is doing, tell the clients."""
        pos = self.cogInfo[suitNum]['pos'] 
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        goalType = self.cogInfo[suitNum]['goal']
        goalId = self.cogInfo[suitNum]['goalId']
        gameTime = self.getCurrentGameTime()
        self.sendUpdate('updateSuitGoal', [timestamp, clientstamp, suitNum,  goalType, goalId,
                                           pos[0],pos[1], pos[2]])


    def chooseSuitGoal(self,  suitNum):
        """Find something to do for this suit."""
        #self.chaseToon(suitNum, self.avIdList[0])
        barrelIndex = self.findClosestUnassignedBarrel(suitNum)
        if barrelIndex >= 0:
            self.chaseBarrel(suitNum, barrelIndex)
        else:
            noOneChasing = self.avIdList[:]
            # go through and find a toon not being chased
            for key in self.cogInfo:
                if self.cogInfo[key]['goal'] == CTGG.ToonGoal:
                    toonId = self.cogInfo[key]['goalId']
                    if toonId in noOneChasing:
                        noOneChasing.remove(toonId)
            chaseToonId = self.avIdList[0]
            if noOneChasing:
                chaseToonId = random.choice(noOneChasing)
            else:
                chaseToonId = random.choice(self.avIdList)
            self.chaseToon(suitNum, chaseToonId)
        
        #self.chaseBarrel(suitNum, 0)
        

    def chaseBarrel( self, suitNum, barrelIndex):
        """Make this suit try to grab the given barrel."""
        goalType = CTGG.BarrelGoal
        goalId = barrelIndex
        self.cogInfo[suitNum]['goal'] = goalType
        self.cogInfo[suitNum]['goalId'] = goalId
        pos = self.cogInfo[suitNum]['pos']
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(),bits=32)
        self.notify.debug('chaseBarrel time=%s suitNum=%s, barrelIndex=%s' %(timestamp,
                                                                    suitNum, barrelIndex))
        gameTime = self.getCurrentGameTime()
        self.sendUpdate('updateSuitGoal', [timestamp, timestamp, suitNum,  goalType, goalId,
                                           pos[0],pos[1], pos[2]])        

    def getCogCarryingBarrel(self, barrelIndex):
        """Return -1 if no one is carrying barrel, cogIndex otherwise."""
        return self.barrelInfo[barrelIndex]['carriedBy']
        

    def cogHitBarrel(self, clientStamp, cogIndex, barrelIndex, x, y ,z):
        """A cog hit the barrel, see if he should pick it up and run"""
        assert self.notify.debugStateCall(self)
        if cogIndex >= self.getNumCogs() :
            self.notify.warning('cogHitBarrel, possible hacker cogIndex=%s' % cogIndex)
            return
        if barrelIndex >= CTGG.NumBarrels:
            self.notify.warning('cogHitBarrel, possible hacker barrelIndex=%s' % barrelIndex)
            return
        if self.isCogCarryingABarrel(cogIndex):
            # cog is already carrying a barrel ignore
            self.notify.debug('cog is already carrying a barrel ignore')
            return
        if self.cogInfo[cogIndex]['goal'] == CTGG.NoGoal:
            # we got a late hit after he was already moved to starting position
            self.notify.debug('ignoring barrel hit as cog %d has no goal' % cogIndex)
            return
        if self.getCogCarryingBarrel(barrelIndex) == CTGG.BarrelOnGround:
            pos  = Point3(x,y,z)
            returnPosIndex = self.chooseReturnPos(cogIndex, pos)
            self.runAway(clientStamp, cogIndex, pos, barrelIndex, returnPosIndex)

    def chooseReturnPos(self, cogIndex, cogPos):
        """Return the return positions index that we the suit should run to."""
        # for now choose the nearest one and run to it
        shortestDistance = 10000
        shortestReturnIndex = -1
        for retIndex in xrange(len(CTGG.CogReturnPositions)):
            retPos = CTGG.CogReturnPositions[retIndex]
            distance = (cogPos - retPos).length()
            if distance < shortestDistance:
                shortestDistance = distance
                shortestReturnIndex = retIndex
                self.notify.debug('shortest distance=%s index=%s' % (shortestDistance, shortestReturnIndex))
        self.notify.debug('chooseReturnpos returning %s' % shortestReturnIndex)
        return shortestReturnIndex
            

    def runAway(self, clientStamp, cogIndex, cogPos, barrelIndex, returnPosIndex):
        """Make this cog run away to a given reuturn position."""
        # should we use the info on where the toons were last were to influence where
        # we should go?
        assert self.notify.debugStateCall(self)
            
        self.cogInfo[cogIndex]['pos'] = cogPos
        
        self.b_makeCogCarryBarrel(clientStamp, cogIndex, barrelIndex)
        goalType = CTGG.RunAwayGoal
        goalId = returnPosIndex
        self.cogInfo[cogIndex]['goal'] = goalType
        self.cogInfo[cogIndex]['goalId'] = 0

        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        gameTime = self.getCurrentGameTime()
        self.sendUpdate('updateSuitGoal', [timestamp, clientStamp, cogIndex,  goalType, goalId,
                                           cogPos[0],cogPos[1], cogPos[2]])      

        
        
    def pieHitSuit(self, avId, timestamp, suitNum, x, y ,z):
        """A toon hit a suit, have the suit do something else."""
        assert self.notify.debugStateCall(self)        
        if suitNum >= self.getNumCogs() :
            self.notify.warning('hitBySuit, possible hacker avId=%s' % avId)
            return
        
        barrelIndex = self.cogInfo[suitNum]['barrel']

        # we must set the cog pos before we drop barrel,
        # as that's where we drop the barrel
        if barrelIndex >= 0:
            # the x,y,z we get is actually the cog position, but we drop the
            # barrel right on it
            barrelPos = Point3(x,y,z)
            self.b_makeCogDropBarrel(timestamp, suitNum, barrelIndex, barrelPos)
        
        
        startPos = CTGG.CogStartingPositions[suitNum]
        self.cogInfo[suitNum]['pos'] = startPos

        self.cogInfo[suitNum]['goal'] = CTGG.NoGoal
        self.cogInfo[suitNum]['goalId'] = CTGG.InvalidGoalId
        self.sendSuitSync(timestamp, suitNum)
        
        # TODO figure out if we want to chase a toon or go for a barrel
        self.doMethodLater(self.ExplodeWaitTime, self.chooseSuitGoal,
                           self.uniqueName('choseSuitGoal-%d-' % suitNum),
                           extraArgs = [suitNum])

    def findClosestUnassignedBarrel(self, suitNum):
        """Return -1 if none, otherwise returns the closest barrel on the ground, no suit is gunning for."""
        possibleBarrels = []
        for key in self.barrelInfo:
            info = self.barrelInfo[key]
            if info['carriedBy'] == CTGG.BarrelOnGround and not info['stolen']:
                # so barrel is on the ground, and not stolen
                # check if another suit is gunning for it
                if not self.isCogGoingForBarrel(key):
                    possibleBarrels.append(key)

        shortestDistance = 10000
        shortestBarrelIndex = -1
        cogPos = self.cogInfo[suitNum]['pos']
        for possibleIndex in possibleBarrels:
            barrelPos = self.barrelInfo[possibleIndex]['pos']
            distance = (cogPos - barrelPos).length()
            if distance < shortestDistance:
                shortestDistance = distance
                shortestBarrelIndex = possibleIndex
                #self.notify.debug('shortest distance=%s index=%s' % (shortestDistance, shortestBarrelIndex))
        #self.notify.debug('findClosestUnassignedBarrel returning %s' % shortestBarrelIndex)
        return shortestBarrelIndex
                    
    def isCogGoingForBarrel(self, barrelIndex):
        """Return true if any cog is going for the barrel."""
        result = False
        for suitNum in self.cogInfo:
            cogInfo = self.cogInfo[suitNum]
            if cogInfo['goal'] == CTGG.BarrelGoal and cogInfo['goalId'] == barrelIndex:
                result = True
                break
        return result

    def markBarrelStolen(self, clientStamp, barrelIndex):
        """Tell the clients the barrel is stolen, mark it in AI too."""
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.sendUpdate('markBarrelStolen', [timestamp, clientStamp, barrelIndex])
        self.barrelInfo[barrelIndex]['stolen'] = True

    def getNumBarrelsStolen(self):
        """Return the number of stolen barrels."""
        numStolen = 0
        for barrel in self.barrelInfo.values():
            if barrel['stolen']:
                numStolen += 1
        return numStolen
            
        
    def cogAtReturnPos(self, clientstamp, cogIndex, barrelIndex):
        """Handle the client telling us the cog has returned and stolen a barrel."""
        # we may get this from multiple clients, and at different times
        if not cogIndex in self.cogInfo or \
           not barrelIndex in self.barrelInfo:
            avId = self.air.getAvatarIdFromSender()
            self.air.writeServerEvent('suspicious cogAtReturnPos avId=%s, cogIndex=%s, barrelIndex=%s' % (avId, cogIndex, barrelIndex))
            return
            
        if self.cogInfo[cogIndex]['goal'] == CTGG.RunAwayGoal:
            if self.isCogCarryingThisBarrel(cogIndex, barrelIndex):
                # tell the clients to mark the barrel as stolen
                self.markBarrelStolen(clientstamp, barrelIndex)
                
                returnPosIndex = self.cogInfo[cogIndex]['goalId']
                retPos = CTGG.CogReturnPositions[returnPosIndex]
                self.b_makeCogDropBarrel(clientstamp, cogIndex, barrelIndex, retPos)

                startPos = CTGG.CogStartingPositions[cogIndex]
                self.cogInfo[cogIndex]['pos'] = startPos

                self.cogInfo[cogIndex]['goal'] = CTGG.NoGoal
                self.cogInfo[cogIndex]['goalId'] = CTGG.InvalidGoalId                
                # TODO figure out if we want to chase a toon or go for a barrel
                self.doMethodLater(0.5, self.chooseSuitGoal,
                                   self.uniqueName('choseSuitGoal-%d-' % cogIndex),
                                   extraArgs = [cogIndex])
                self.checkForGameOver()

    def checkForGameOver(self):
        """Check if the game is over."""
        numStolen = 0
        for key in self.barrelInfo:
            if self.barrelInfo[key]['stolen']:
                numStolen+=1
        self.notify.debug('numStolen = %s' % numStolen)
        if simbase.config.GetBool('cog-thief-check-barrels', 1):
            if not simbase.config.GetBool('cog-thief-endless', 0):
                if numStolen == len(self.barrelInfo):
                    self.gameOver()

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        self.gameOver()
        return Task.done

    def getNumCogs(self):
        """Return the number of cogs we have for this game."""
        result =  simbase.config.GetInt('cog-thief-num-cogs', 0)
        if not result:
            safezone = self.getSafezoneId()
            result = CTGG.calculateCogs(self.numPlayers, safezone)
        return result
        
