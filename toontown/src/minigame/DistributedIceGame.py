"""DistributedIceGame module: contains the DistributedIceGame class"""
import math
from pandac.PandaModules import Vec3, deg2Rad, Point3, NodePath, VBase4, \
     CollisionHandlerEvent, CollisionNode, CollisionSphere
from direct.fsm import ClassicFSM, State
from direct.distributed.ClockDelta import globalClockDelta
from direct.gui.DirectGui import DirectLabel
from direct.interval.IntervalGlobal import Sequence, LerpScaleInterval, \
     LerpFunctionInterval, Func, Parallel, LerpPosInterval, Wait, SoundInterval, \
     LerpColorScaleInterval
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownTimer
from toontown.minigame import ArrowKeys
from toontown.minigame import DistributedMinigame
from toontown.minigame import DistributedIceWorld
from toontown.minigame import IceGameGlobals
from toontown.minigame import MinigameAvatarScorePanel
from toontown.minigame import IceTreasure

class DistributedIceGame(DistributedMinigame.DistributedMinigame,
                         DistributedIceWorld.DistributedIceWorld):
    """Client side class for the ice game."""
    notify = directNotify.newCategory("DistributedIceGame")

    MaxLocalForce = 100 # what we send out for our maximum input for force
    MaxPhysicsForce = 25000 # what's the maximum physics force toon can give
    
    def __init__(self, cr):
        """Constructor for DistributedVineGame."""
        DistributedMinigame.DistributedMinigame.__init__(self, cr)
        DistributedIceWorld.DistributedIceWorld.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedIceGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['inputChoice']),
                                State.State('inputChoice',
                                            self.enterInputChoice,
                                            self.exitInputChoice,
                                            ['waitServerChoices',
                                             'moveTires',
                                             'displayVotes',
                                             'cleanup']),
                                State.State('waitServerChoices',
                                            self.enterWaitServerChoices,
                                            self.exitWaitServerChoices,
                                            ['moveTires',
                                             'cleanup']),
                                State.State('moveTires',
                                            self.enterMoveTires,
                                            self.exitMoveTires,
                                            ['synch',
                                             'cleanup']),
                                State.State('synch',
                                            self.enterSynch,
                                            self.exitSynch,
                                            ['inputChoice', 'scoring',
                                             'cleanup']),
                                State.State('scoring',
                                            self.enterScoring,
                                            self.exitScoring,
                                            ['cleanup', 'finalResults', 'inputChoice']),
                                State.State('finalResults',
                                            self.enterFinalResults,
                                            self.exitFinalResults,
                                            ['cleanup', ]),                                
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

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        self.cameraThreeQuarterView = (0, -22, 45, 0, -62.89, 0)
        self.tireDict = {}# {avId : (tireNodePath, odeBody, odeGeom)}
        self.forceArrowDict = {} # {avId : forceArrow}

        self.canDrive = False

        # These are None to indicate we have not yet established a
        # timer; they are filled in as we enter the inputChoice state
        # and as the AI reports a start time, respectively.  When both
        # are filled in, the timer will be displayed.
        self.timer = None
        self.timerStartTime = None

        #WARNING remove this or else it will leak
        # base.ice = self

        self.curForce = 0 # 0 to 100, can have fractions
        self.curHeading = 0 # in degrees, may be negative

        self.headingMomentum = 0.0
        self.forceMomentum = 0.0

        self.allTireInputs = None

        self.curRound = 0
        self.curMatch = 0

        self.controlKeyWarningLabel =  DirectLabel(
            text = TTLocalizer.IceGameControlKeyWarning,
            text_fg = VBase4(1,0,0,1),
            relief = None,
            pos = (0.0, 0, 0),
            scale = 0.15)   
        self.controlKeyWarningLabel.hide()

        self.waitingMoveLabel = DirectLabel(
            text = TTLocalizer.IceGameWaitingForPlayersToFinishMove,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.6, 0, -0.75),
            scale = 0.075)   
        self.waitingMoveLabel.hide()

        self.waitingSyncLabel = DirectLabel(
            text = TTLocalizer.IceGameWaitingForAISync,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.6, 0, -0.75),
            scale = 0.075)   
        self.waitingSyncLabel.hide()

        self.infoLabel = DirectLabel(
            text = "",
            text_fg = VBase4(0,0,0,1),
            relief = None,
            pos = (0.0, 0, 0.7),
            scale = 0.075)
        self.updateInfoLabel()

        self.lastForceArrowUpdateTime = 0
        self.sendForceArrowUpdateAsap = False

        self.treasures = []
        self.penalties = []
        self.obstacles = []

        self.controlKeyPressed = False
        self.controlKeyWarningIval = None
        #self.showContacts = True
        
    def delete(self):
        """Remove ourself from the world."""
        DistributedIceWorld.DistributedIceWorld.delete(self)
        DistributedMinigame.DistributedMinigame.delete(self)

        if self.controlKeyWarningIval:
            self.controlKeyWarningIval.finish()
            self.controlKeyWarningIval = None
        self.controlKeyWarningLabel.destroy()
        del self.controlKeyWarningLabel

        self.waitingMoveLabel.destroy()
        del self.waitingMoveLabel
        
        self.waitingSyncLabel.destroy()
        del self.waitingSyncLabel

        self.infoLabel.destroy()
        del self.infoLabel

        for treasure in self.treasures:
            treasure.destroy()
        del self.treasures

        for penalty in self.penalties:
            penalty.destroy()
        del self.penalties

        for obstacle in self.obstacles:
            obstacle.removeNode()
        del self.obstacles

        del self.gameFSM

    def announceGenerate(self):
        """Do stuff dependent on required fields."""
        DistributedMinigame.DistributedMinigame.announceGenerate(self)
        DistributedIceWorld.DistributedIceWorld.announceGenerate(self)
        self.debugTaskName = self.uniqueName('debugTask')
        
    def getTitle(self):
        return TTLocalizer.IceGameTitle

    def getInstructions(self):
        szId = self.getSafezoneId()
        numPenalties = IceGameGlobals.NumPenalties[szId]
        result =  TTLocalizer.IceGameInstructions
        if numPenalties == 0:
            result =  TTLocalizer.IceGameInstructionsNoTnt
        return result
        

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0


    def load(self):
        # load resources and create objects here
        self.notify.debug("load")
        DistributedMinigame.DistributedMinigame.load(self)
        self.music = base.loadMusic("phase_4/audio/bgm/MG_IceGame.mid")
        #self.gameBoard = loader.loadModel("phase_4/models/minigames/toon_cannon_gameground")
        self.gameBoard = loader.loadModel("phase_4/models/minigames/ice_game_icerink")
        #background = loader.loadModel("phase_4/models/minigames/ice_game")
        background = loader.loadModel("phase_4/models/minigames/ice_game_2d")
        background.reparentTo(self.gameBoard)
        self.gameBoard.setPosHpr(0,0,0,0,0,0)
        self.gameBoard.setScale(1.0)
        self.setupSimulation()
        index = 0
        for avId in self.avIdList:
            self.setupTire(avId, index)
            self.setupForceArrow(avId)
            index += 1

        #setup dummy tires
        for index in xrange(len(self.avIdList), 4):
            self.setupTire(-index, index)
            self.setupForceArrow(-index)

        self.showForceArrows(realPlayersOnly = True)
        
        # load markers for walls
        self.westWallModel = NodePath() #loader.loadModel('models/misc/xyzAxis')
        if not self.westWallModel.isEmpty():
            self.westWallModel.reparentTo(self.gameBoard)
            self.westWallModel.setPos(IceGameGlobals.MinWall[0], IceGameGlobals.MinWall[1],0)
            self.westWallModel.setScale(4)
            
        self.eastWallModel = NodePath() #loader.loadModel('models/misc/xyzAxis')
        if not self.eastWallModel.isEmpty():
            self.eastWallModel.reparentTo(self.gameBoard)
            self.eastWallModel.setPos(IceGameGlobals.MaxWall[0], IceGameGlobals.MaxWall[1], 0)
            self.eastWallModel.setScale(4)
            self.eastWallModel.setH(180)
        self.arrowKeys = ArrowKeys.ArrowKeys()    
        self.target = loader.loadModel('phase_3/models/misc/sphere')
        self.target.setScale(0.01)
        self.target.reparentTo(self.gameBoard)
        self.target.setPos(0,0,0)

        #self.scoreCircle = loader.loadModel('phase_3/models/misc/sphere')
        self.scoreCircle = loader.loadModel('phase_4/models/minigames/ice_game_score_circle')
        self.scoreCircle.setScale(0.01)
        self.scoreCircle.reparentTo(self.gameBoard)
        self.scoreCircle.setZ(IceGameGlobals.TireRadius/2.0)
        self.scoreCircle.setAlphaScale(0.5)
        self.scoreCircle.setTransparency(1)
        self.scoreCircle.hide()
        self.treasureModel = loader.loadModel('phase_4/models/minigames/ice_game_barrel')
        #self.penaltyModel = loader.loadModel('phase_4/models/minigames/ice_game_iceblock')
        #self.penaltyModel = loader.loadModel('phase_4/models/minigames/ice_game_tnt')
        self.penaltyModel = loader.loadModel('phase_4/models/minigames/ice_game_tnt2')
        # lets use the upright version of the tnt, but scale it down to match barrel
        self.penaltyModel.setScale(0.75, 0.75, 0.7)
        
        szId = self.getSafezoneId()
        obstacles = IceGameGlobals.Obstacles[szId]
        index = 0
        cubicObstacle = IceGameGlobals.ObstacleShapes[szId]
        for pos in obstacles:
            newPos = Point3(pos[0], pos[1], IceGameGlobals.TireRadius)
            newObstacle = self.createObstacle(newPos, index, cubicObstacle)
            self.obstacles.append(newObstacle)
            index+= 1
            
        # Load the sounds
        self.countSound = loader.loadSfx("phase_3.5/audio/sfx/tick_counter.mp3")
        self.treasureGrabSound = loader.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_bananas.mp3")
        self.penaltyGrabSound = loader.loadSfx("phase_4/audio/sfx/MG_cannon_fire_alt.mp3")

        self.tireSounds=[]
        for tireIndex in xrange(4):
            tireHit = loader.loadSfx("phase_4/audio/sfx/Golf_Hit_Barrier_1.mp3")
            wallHit = loader.loadSfx("phase_4/audio/sfx/MG_maze_pickup.mp3")
            obstacleHit = loader.loadSfx("phase_4/audio/sfx/Golf_Hit_Barrier_2.mp3")
            self.tireSounds.append( {'tireHit': tireHit,
                                          'wallHit' : wallHit,
                                          'obstacleHit' : obstacleHit,
                                          })
        self.arrowRotateSound = loader.loadSfx("phase_4/audio/sfx/MG_sfx_ice_force_rotate.wav")
        self.arrowUpSound = loader.loadSfx("phase_4/audio/sfx/MG_sfx_ice_force_increase_3sec.mp3")
        self.arrowDownSound = loader.loadSfx("phase_4/audio/sfx/MG_sfx_ice_force_decrease_3sec.mp3")
        self.scoreCircleSound = loader.loadSfx("phase_4/audio/sfx/MG_sfx_ice_scoring_1.mp3")
                                          

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        del self.music
        
        self.gameBoard.removeNode()
        del self.gameBoard

        for forceArrow in self.forceArrowDict.values():
            forceArrow.removeNode()
        del self.forceArrowDict

        self.scoreCircle.removeNode()
        del self.scoreCircle

        del self.countSound
        
    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons

        self.gameBoard.reparentTo(render)
        self.__placeToon(self.localAvId)        
        self.moveCameraToTop()

        self.scorePanels = []        

        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.8)
        
    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        self.music.stop()                
        self.gameBoard.hide()
        self.infoLabel.hide()
        for avId in self.tireDict:
            self.tireDict[avId]['tireNodePath'].hide()

        for panel in self.scorePanels:
            panel.cleanup()
        del self.scorePanels        

        for obstacle in self.obstacles:
            obstacle.hide()

        for treasure in self.treasures:
            treasure.nodePath.hide()

        for penalty in self.penalties:
            penalty.nodePath.hide()

        # reset the toons' LODs and show their dropshadows again
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.dropShadow.show()
                av.resetLOD() # we'll use the head frames instead

        taskMgr.remove(self.uniqueName("aimtask"))
        self.arrowKeys.destroy()
        del self.arrowKeys 
            
        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.DistributedMinigame.offstage(self)

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        DistributedMinigame.DistributedMinigame.handleDisabledAvatar(self, avId)

    def setGameReady(self):
        if not self.hasLocalToon:
            return
        self.notify.debug("setGameReady")
        if DistributedMinigame.DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        for index in xrange(self.numPlayers):
            avId = self.avIdList[index]
            # Find the actual avatar in the cr
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)
                toon.forwardSpeed = 0
                toon.rotateSpeed = False
                #toon.setAnimState('Happy', 1.0)
                # Start the smoothing task.
                #toon.startSmooth()
                # hide their dropshadows again
                toon.dropShadow.hide()                    
                toon.setAnimState('Sit')                
                if avId in self.tireDict:
                    tireNp = self.tireDict[avId]['tireNodePath']
                    toon.reparentTo(tireNp)
                    toon.setY(1.0)
                    toon.setZ(-3)
                toon.startLookAround()


    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.

        # make the remote toons stop looking around
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.stopLookAround()

        # Initialize the scoreboard
        self.scores = [0] * self.numPlayers
        spacing = .4
        for i in xrange(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = \
                       MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId,
                                                                         avName)
            scorePanel.setScale(.9)
            scorePanel.setPos(.75 - spacing*((self.numPlayers-1)-i), 0.0, .875)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels.append(scorePanel)                

        self.arrowKeys.setPressHandlers([self.__upArrowPressed,
                                         self.__downArrowPressed,
                                         self.__leftArrowPressed,
                                         self.__rightArrowPressed,
                                         self.__controlPressed])            
        
        # transition to the appropriate state
        # self.gameFSM.request("inputChoice")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def isInPlayState(self):
        """Return true if we are in the play state."""
        if not self.gameFSM.getCurrentState():
            return False
        if not self.gameFSM.getCurrentState().getName() == 'play':
            return False
        return True

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass


##     def enterPlay(self):
##         self.canDrive = True
##         tireBody = self.tireDict[localAvatar.doId]["tireBody"]
##         #tireBody.enable()
##         # enable all the tires
##         for avId in self.tireDict.keys():
##             self.tireDict[localAvatar.doId]["tireBody"].enable()
        
##         self.startSim()
##         self.startDebugTask()
##         self.notify.debug("enterPlay")


##         # when the game is done, call gameOver()
##         # self.gameOver()

##     def exitPlay(self):
##         # Stop music
##         self.stopDebugTask()
##         self.ignoreAll()

    def enterInputChoice(self):
        """Enter the input choice state, choosing force and direction."""
        self.notify.debug("enterInputChoice")
        self.forceLocalToonToTire()
        self.controlKeyPressed = False
        if self.curRound == 0:
            self.setupStartOfMatch()
        else:
            self.notify.debug('self.curRound = %s' % self.curRound)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.hide()
        if self.timerStartTime != None:
            self.startTimer()
        self.showForceArrows(realPlayersOnly = True)
        self.localForceArrow().setPosHpr(0,0,-1.0,0,0,0)
        self.localForceArrow().reparentTo(self.localTireNp())
        self.localForceArrow().setY(IceGameGlobals.TireRadius)
        #self.localForceArrow().wrtReparentTo(self.gameBoard)
        self.localTireNp().headsUp(self.target)
        self.notify.debug('self.localForceArrow() heading = %s' % self.localForceArrow().getH())
        self.curHeading = self.localTireNp().getH()
        self.curForce = 25        
        self.updateLocalForceArrow()

        # lets initialize the other force arrows
        for avId in self.forceArrowDict:
            forceArrow = self.forceArrowDict[avId]
            forceArrow.setPosHpr(0,0,-1.0,0,0,0)
            tireNp = self.tireDict[avId]['tireNodePath']
            forceArrow.reparentTo(tireNp)
            #forceArrow.wrtReparentTo(self.gameBoard)
            forceArrow.setY(IceGameGlobals.TireRadius)
            tireNp.headsUp(self.target)
            #forceArrow.headsUp(self.target)
            self.updateForceArrow(avId, tireNp.getH(), 25)

        
        taskMgr.add(self.__aimTask, self.uniqueName("aimtask"))

        # hide the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.stop()

        self.sendForceArrowUpdateAsap = False
        pass

    def exitInputChoice(self):
        """Exit Input Choice state."""
        #import pdb; pdb.set_trace()
        if not self.controlKeyPressed:
            if self.controlKeyWarningIval:
                self.controlKeyWarningIval.finish()
                self.controlKeyWarningIval = None            
            self.controlKeyWarningIval = Sequence(
                Func(self.controlKeyWarningLabel.show),
                self.controlKeyWarningLabel.colorScaleInterval(10,
                                                               VBase4(1,1,1,0),
                                                               startColorScale=VBase4(1,1,1,1)),
                Func(self.controlKeyWarningLabel.hide)
                )
            self.controlKeyWarningIval.start()

        if self.timer != None:
            self.timer.destroy()
            self.timer = None
        self.timerStartTime = None        
        self.hideForceArrows()
        self.arrowRotateSound.stop()
        self.arrowUpSound.stop()
        self.arrowDownSound.stop()                
        taskMgr.remove(self.uniqueName("aimtask"))
        pass

    def enterWaitServerChoices(self):
        """Waiting for everyone else to finish choosing."""
        self.waitingMoveLabel.show()
        self.showForceArrows(True)
        pass    

    def exitWaitServerChoices(self):
        """Exit wait server choices state."""
        self.waitingMoveLabel.hide()
        self.hideForceArrows()
        pass    

    def enterMoveTires(self):
        """Show the tires moving around."""
        for key in self.tireDict:
            body = self.tireDict[key]['tireBody']
            body.setAngularVel(0,0,0) # make sure it's not spinning when it starts
            body.setLinearVel(0,0,0) # make sure it's not moving  when it starts
        
        for index in xrange(len(self.allTireInputs)):
            input = self.allTireInputs[index]
            avId = self.avIdList[index]
            body = self.getTireBody(avId)
            degs = input[1] +90  # to make zero line up toward +x axis
            tireNp = self.getTireNp(avId)
            tireH = tireNp.getH()
            self.notify.debug('tireH = %s' % tireH)
            radAngle = deg2Rad(degs)
            foo =  NodePath('foo')
            #foo.setH(0)
            #body.setQuaternion(foo.getQuat())
            dirVector = Vec3(math.cos(radAngle), math.sin(radAngle), 0)
            self.notify.debug('dirVector is now=%s' % dirVector)
            inputForce = input[0]
            inputForce /= self.MaxLocalForce # now its 0..1
            inputForce *= self.MaxPhysicsForce
            force = dirVector * inputForce
            self.notify.debug('adding force %s to %d' % (force, avId))
            body.addForce(force)
        self.enableAllTireBodies()
        self.totalPhysicsSteps = 0
        self.startSim()
        taskMgr.add(self.__moveTiresTask, self.uniqueName("moveTiresTtask"))
        pass

    def exitMoveTires(self):
        """Exit Move Tires state."""
        self.forceLocalToonToTire()
        self.disableAllTireBodies()
        self.stopSim()
        self.notify.debug('total Physics steps = %d' % self.totalPhysicsSteps)
        taskMgr.remove(self.uniqueName("moveTiresTtask"))

    def enterSynch(self):
        """Enter synch state."""
        # wait for the AI to send final positions
        #self.gameFSM.request('inputChoice')
        self.waitingSyncLabel.show()
        pass

    def exitSynch(self):
        """Exit Synch State."""
        self.waitingSyncLabel.hide()
        pass

    def enterScoring(self):
        """Enter scoring state."""
        # we should have gotten the new match, new round and new scores by now
        sortedByDistance = []
        for avId in self.avIdList:
            # center is 0,0,0, so distance is pos.length()
            np = self.getTireNp(avId)
            pos = np.getPos()
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
        self.scoreMovie = Sequence()
        curScale = 0.01
        curTime = 0
        self.scoreCircle.setScale(0.01)
        self.scoreCircle.show()
        self.notify.debug('newScores = %s' % self.newScores)
        circleStartTime = 0
        for index in xrange(len(sortedByDistance)):
            distance = sortedByDistance[index][1]
            avId = sortedByDistance[index][0]
            scorePanelIndex = self.avIdList.index(avId)
            time = (distance - curScale) / IceGameGlobals.ExpandFeetPerSec
            if time < 0:
                time = 0.01
            scaleXY = distance + IceGameGlobals.TireRadius
            #scaleXY /= 2.0 # the real scoring circle has a radius of 1, not 0.5
            self.notify.debug('circleStartTime = %s' % circleStartTime)
            self.scoreMovie.append(
                Parallel(LerpScaleInterval( self.scoreCircle, time,
                                            Point3(scaleXY, scaleXY, 1.0)),
                         SoundInterval(self.scoreCircleSound, duration=time, startTime = circleStartTime),
                         )
                )
            circleStartTime += time
            startScore = self.scorePanels[scorePanelIndex].getScore()
            destScore = self.newScores[scorePanelIndex]
            self.notify.debug('for avId %d, startScore=%d, newScores=%d' % (avId, startScore,destScore))
            def increaseScores(t, scorePanelIndex = scorePanelIndex, startScore = startScore,
                               destScore = destScore):
                oldScore = self.scorePanels[scorePanelIndex].getScore()
                diff = destScore - startScore
                newScore = int( startScore + diff*t)
                if newScore > oldScore:
                    base.playSfx(self.countSound)
                self.scorePanels[scorePanelIndex].setScore(newScore)
                self.scores[scorePanelIndex] = newScore
            duration = (destScore - startScore) * IceGameGlobals.ScoreCountUpRate
            tireNp = self.tireDict[avId]['tireNodePath']
            self.scoreMovie.append( Parallel(
                LerpFunctionInterval( increaseScores, duration),
                Sequence(
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,0,0,1)),
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,1,1,1)),
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,0,0,1)),
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,1,1,1)),
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,0,0,1)),
                    LerpColorScaleInterval(tireNp, duration /6.0, VBase4(1,1,1,1)),
                    )
                )
                )
            curScale += distance
        self.scoreMovie.append(Func(self.sendUpdate,'reportScoringMovieDone',[]))
        self.scoreMovie.start()
        pass

    def exitScoring(self):
        """Exit scoring state."""
        self.scoreMovie.finish()
        self.scoreMovie = None
        self.scoreCircle.hide()
        pass

    def enterFinalResults(self):
        """Enter final results state."""
        # lerp up the goal bar, score panels
        lerpTrack = Parallel()
        lerpDur = .5
        
        # score panels
        # top/bottom Y
        tY = .6; bY = -.05
        # left/center/right X
        lX = -.5; cX = 0; rX = .5
        scorePanelLocs = (
            ((cX,bY),),
            ((lX,bY),(rX,bY)),
            ((cX,tY),(lX,bY),(rX,bY)),
            ((lX,tY),(rX,tY),(lX,bY),(rX,bY)),
            )
        scorePanelLocs = scorePanelLocs[self.numPlayers - 1]
        for i in xrange(self.numPlayers):
            panel = self.scorePanels[i]
            pos = scorePanelLocs[i]
            lerpTrack.append(Parallel(
                LerpPosInterval(panel, lerpDur, Point3(pos[0],0,pos[1]),
                                blendType='easeInOut'),
                LerpScaleInterval(panel, lerpDur,
                                  Vec3(panel.getScale())*2.,
                                  blendType='easeInOut'),
                ))

        self.showScoreTrack = Parallel(
            lerpTrack,
            Sequence(Wait(IceGameGlobals.ShowScoresDuration),
                     Func(self.gameOver),
                     ),
            )

        self.showScoreTrack.start()
        pass

    def exitFinalResults(self):
        """Exit final results state."""
        # calling finish() here would cause problems if we're
        # exiting abnormally, because of the gameOver() call
        self.showScoreTrack.pause()
        del self.showScoreTrack
                
        pass
        
    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        # hide the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.start()
        

    def exitCleanup(self):
        pass

    def __placeToon(self, avId):
        """ places a toon in its starting position """
        toon = self.getAvatar(avId)
        if toon:
            toon.setPos(0,0,0)
            toon.setHpr(0,0,0)

    def moveCameraToTop(self):
        camera.reparentTo(render)
        p = self.cameraThreeQuarterView
        camera.setPosHpr(p[0], p[1], p[2], p[3], p[4], p[5])

    def setupTire(self, avId, index):
        """Create tire and setup other tire related fields."""
        tireNp, tireBody, tireOdeGeom = self.createTire( index)
        self.tireDict[avId] = {'tireNodePath' : tireNp,
                               'tireBody' : tireBody,
                               'tireOdeGeom' : tireOdeGeom
                               }
        
        if avId <=0 :
            tireBlocker = tireNp.find('**/tireblockermesh')
            if not tireBlocker.isEmpty():
                tireBlocker.hide()
        if avId == self.localAvId:
            tireNp = self.tireDict[avId]['tireNodePath']

            self.treasureSphereName = "treasureCollider"
            self.treasureCollSphere = CollisionSphere(0,0,0,
                                                      IceGameGlobals.TireRadius)
            self.treasureCollSphere.setTangible(0)
            self.treasureCollNode = CollisionNode(self.treasureSphereName)
            self.treasureCollNode.setFromCollideMask(ToontownGlobals.PieBitmask)
            self.treasureCollNode.addSolid(self.treasureCollSphere)
            self.treasureCollNodePath = tireNp.attachNewNode(self.treasureCollNode)

            #self.treasureCollNodePath.show()
            #self.torso.show()

            self.treasureHandler = CollisionHandlerEvent()
            self.treasureHandler.addInPattern('%fn-intoTreasure')            
            base.cTrav.addCollider(self.treasureCollNodePath, self.treasureHandler)

            eventName = '%s-intoTreasure' % self.treasureCollNodePath.getName()
            self.notify.debug('eventName = %s' % eventName)
            self.accept(eventName, self.toonHitSomething)
    
    def setupForceArrow(self, avId):
        """Create tire and setup other tire related fields."""
        #self.forceArrowDict[avId] = loader.loadModel('models/misc/xyzAxis')
        arrow = loader.loadModel('phase_4/models/minigames/ice_game_arrow')
        #arrow = loader.loadModel('phase_4/models/minigames/ice_game_arrow_2d')
        priority = 0
        if avId < 0:
            priority = -avId
        else:
            priority = self.avIdList.index(avId)
            if avId == self.localAvId:
                priority = 10
        #arrow.setBin('fixed', priority)
        #arrow.setDepthTest(False)
        #arrow.setDepthWrite(False)
        
        self.forceArrowDict[avId] = arrow

    def hideForceArrows(self):
        """Hide all the arrows."""
        for forceArrow in self.forceArrowDict.values():
            forceArrow.hide()

    def showForceArrows(self, realPlayersOnly = True):
        """Show all the force arrows."""
        for avId in self.forceArrowDict:
            if realPlayersOnly:
                if avId > 0:
                    self.forceArrowDict[avId].show()
                else:
                    self.forceArrowDict[avId].hide()
            else:
                self.forceArrowDict[avId].show()

    def localForceArrow(self):
        """Return the local toons force arrow."""
        if self.localAvId in self.forceArrowDict:
            return self.forceArrowDict[self.localAvId]
        else:
            return None
        
    
    def setChoices(self,  input0,  input1,  input2,  input3):
        """Handle the input from all players on which direction and force they'll use."""
        pass
    
    def startDebugTask(self):
        """Start the debugging task."""
        taskMgr.add(self.debugTask, self.debugTaskName)
        
    def stopDebugTask(self):
        """Stop the debugging task"""
        taskMgr.remove(self.debugTaskName)

    def debugTask(self, task):
        """Do stuff we need to debug the game."""
        if self.canDrive and self.tireDict.has_key(localAvatar.doId):
            dt = globalClock.getDt()
            forceMove = 25000
            forceMoveDt = forceMove #* dt
            tireBody = self.tireDict[localAvatar.doId]["tireBody"]
            if self.arrowKeys.upPressed() and not tireBody.isEnabled():
                x = 0
                y = 1                
                tireBody.enable()
                tireBody.addForce(Vec3(x * forceMoveDt, y * forceMoveDt,0))
            if self.arrowKeys.downPressed() and not tireBody.isEnabled():
                x = 0
                y = -1
                tireBody.enable()
                tireBody.addForce(Vec3(x * forceMoveDt, y * forceMoveDt,0))
            if self.arrowKeys.leftPressed() and not tireBody.isEnabled():
                x = -1
                y = 0
                tireBody.enable()
                tireBody.addForce(Vec3(x * forceMoveDt, y * forceMoveDt,0))
            if self.arrowKeys.rightPressed() and not tireBody.isEnabled():
                x = 1
                y = 0
                tireBody.enable()
                tireBody.addForce(Vec3(x * forceMoveDt, y * forceMoveDt,0))                
                  
        return task.cont

    def __upArrowPressed(self):
        """Handle up arrow being pressed."""
        pass

    def __downArrowPressed(self):
        """Handle down arrow being pressed."""
        pass

    def __leftArrowPressed(self):
        """Handle left arrow being pressed."""
        pass
    
    def __rightArrowPressed(self):
        """Handle right arrow being pressed."""
        pass
    
    def __controlPressed(self):
        """Handle control key being pressed."""
        if self.gameFSM.getCurrentState().getName() == 'inputChoice':
            self.sendForceArrowUpdateAsap = True
            self.updateLocalForceArrow()
            self.controlKeyPressed = True
            self.sendUpdate("setAvatarChoice", [self.curForce, self.curHeading])
            self.gameFSM.request('waitServerChoices')
        pass

    def startTimer(self):
        """startTimer(self)
        Starts the timer display running during the inputChoice state,
        once we have received the timerStartTime from the AI.
        """
        now = globalClock.getFrameTime()
        elapsed = now - self.timerStartTime

        #self.timer.setPos(1.16, 0, -0.83)
        self.timer.posInTopRightCorner()
        self.timer.setTime(IceGameGlobals.InputTimeout)
        self.timer.countdown(IceGameGlobals.InputTimeout - elapsed,
                             self.handleChoiceTimeout)
        self.timer.show()

    def setTimerStartTime(self, timestamp):
        """setTimeStartTime(self, int16 timestamp)

        This message is sent from the AI to indicate the point at
        which the timer starts (or started) counting.  It's used to
        synchronize the timer display with the actual countdown on the
        AI.
        """
        if not self.hasLocalToon: return
        self.timerStartTime = globalClockDelta.networkToLocalTime(timestamp)
        if self.timer != None:
            self.startTimer()        

    def handleChoiceTimeout(self):
        """If we timeout locally, send a 0,0 for our choice."""
        self.sendUpdate("setAvatarChoice", [0,0])
        self.gameFSM.request("waitServerChoices")
        pass

    def localTireNp(self):
        """Return the local avatar's tire node path."""
        ret = None
        if self.localAvId in self.tireDict:
            ret = self.tireDict[self.localAvId]['tireNodePath']
        return ret

    def localTireBody(self):
        """Return the ode physics sphere body for the tire."""
        ret = None
        if self.localAvId in self.tireDict:
            ret = self.tireDict[self.localAvId]['tireBody']
        return ret

    def getTireBody(self, avId):
        """Return the ode physics sphere body for the avatar's tire."""
        ret = None
        if avId in self.tireDict:
            ret = self.tireDict[avId]['tireBody']
        return ret

    def getTireNp(self, avId):
        """Return the node path for the avatar's tire."""
        ret = None
        if avId in self.tireDict:
            ret = self.tireDict[avId]['tireNodePath']
        return ret

    def updateForceArrow(self, avId, curHeading, curForce):
        """Update the force arrow of the local player."""
        forceArrow = self.forceArrowDict[avId]
        #forceArrow.setH(curHeading)
        tireNp = self.tireDict[avId]['tireNodePath']
        tireNp.setH(curHeading)
        tireBody = self.tireDict[avId]['tireBody']
        tireBody.setQuaternion(tireNp.getQuat())
        self.notify.debug('curHeading = %s' % curHeading)
        yScale = curForce / 100.0
        # yScale is now normalized between 0 and 1
        yScale *= 1 # arrow has length of 15 feet at scale 1.0
        headY = yScale * 15
        xScale = (yScale - 1) / 2.0 + 1.0
        shaft = forceArrow.find('**/arrow_shaft')
        head = forceArrow.find('**/arrow_head')
        #forceArrow.setScale(xScale, yScale, 1)
        shaft.setScale(xScale,yScale,1)
        head.setPos(0, headY, 0)
        head.setScale(xScale, xScale, 1)
        

    def updateLocalForceArrow(self):
        """Update the force arrow of the local player."""
        avId = self.localAvId
        self.b_setForceArrowInfo(avId, self.curHeading, self.curForce)
        # self.updateForceArrow(avId, self.curHeading, self.curForce)

    def __aimTask(self, task):
        """Handle input and other necessary stuff while in the Input Choice state."""
        if not hasattr(self, 'arrowKeys'):
            return task.done
        dt = globalClock.getDt()
        headingMomentumChange = dt * 60.0
        forceMomentumChange = dt * 160.0
        arrowUpdate = False
        arrowRotating = False
        arrowUp = False
        arrowDown = False
        if self.arrowKeys.upPressed() and not self.arrowKeys.downPressed(): 
            self.forceMomentum += forceMomentumChange
            if self.forceMomentum < 0:
                self.forceMomentum = 0
            if self.forceMomentum > 50:
                self.forceMomentum = 50
            oldForce = self.curForce
            self.curForce += self.forceMomentum * dt
            arrowUpdate = True

            if oldForce < self.MaxLocalForce:            
                arrowUp = True
        elif self.arrowKeys.downPressed() and not self.arrowKeys.upPressed() :
            self.forceMomentum += forceMomentumChange
            if self.forceMomentum < 0:
                self.forceMomentum = 0
            if self.forceMomentum > 50:
                self.forceMomentum = 50
            oldForce = self.curForce
            self.curForce -= self.forceMomentum * dt            
            arrowUpdate = True
            if oldForce > 0.01:
                arrowDown = True
        else:
            self.forceMomentum = 0

        if self.arrowKeys.leftPressed() and not self.arrowKeys.rightPressed():
            self.headingMomentum += headingMomentumChange
            if self.headingMomentum < 0:
                self.headingMomentum = 0
            if self.headingMomentum > 50:
                self.headingMomentum = 50
            self.curHeading += self.headingMomentum * dt
            arrowUpdate = True
            arrowRotating = True
        elif self.arrowKeys.rightPressed() and not self.arrowKeys.leftPressed():
            self.headingMomentum += headingMomentumChange
            if self.headingMomentum < 0:
                self.headingMomentum = 0
            if self.headingMomentum > 50:
                self.headingMomentum = 50
            self.curHeading -= self.headingMomentum * dt
            arrowUpdate = True
            arrowRotating = True
        else:
            self.headingMomentum = 0
            
        if arrowUpdate:
            self.normalizeHeadingAndForce()
            self.updateLocalForceArrow()

        if arrowRotating:
            if not self.arrowRotateSound.status() == self.arrowRotateSound.PLAYING:
                base.playSfx(self.arrowRotateSound, looping = True)
        else:
            self.arrowRotateSound.stop()

        if arrowUp:
            if not self.arrowUpSound.status() == self.arrowUpSound.PLAYING:
                base.playSfx(self.arrowUpSound, looping = False)
        else:
            self.arrowUpSound.stop()            

        if arrowDown:
            if not self.arrowDownSound.status() == self.arrowDownSound.PLAYING:
                base.playSfx(self.arrowDownSound, looping = False)
        else:
            self.arrowDownSound.stop()            

            
        return task.cont

    def normalizeHeadingAndForce(self):
        """Sanity check curHeading and curForce."""
        if self.curForce > self.MaxLocalForce:
            self.curForce = self.MaxLocalForce
        if self.curForce < 0.01:
            self.curForce = 0.01
        #self.curHeading %= 360

    def setTireInputs(self, tireInputs):
        """We've received word from the AI of force and direction for each player."""
        if not self.hasLocalToon: return
        assert self.notify.debugStateCall(self)
        self.allTireInputs = tireInputs
        self.gameFSM.request('moveTires')

    def enableAllTireBodies(self):
        """Enable all the tires."""
        for avId in self.tireDict.keys():
            self.tireDict[avId]["tireBody"].enable()

    def disableAllTireBodies(self):
        """Enable all the tires."""
        for avId in self.tireDict.keys():
            self.tireDict[avId]["tireBody"].disable()

    def areAllTiresDisabled(self):
        """Return true if they are all disabled."""
        for avId in self.tireDict.keys():
            if self.tireDict[avId]["tireBody"].isEnabled():
                return False
        return True
        

    def __moveTiresTask(self, task):
        """Check the tires if they've stopped."""
        if self.areAllTiresDisabled():
            self.sendTirePositions()
            self.gameFSM.request('synch')
            return task.done
        return task.cont

    def sendTirePositions(self):
        """Send the ending tire positions."""
        tirePositions = []
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            tire = self.getTireBody(avId)
            pos = Point3(tire.getPosition())
            tirePositions.append([pos[0], pos[1], pos[2]])

        for index in xrange(len(self.avIdList), 4):
            avId = -index
            tire = self.getTireBody(avId)
            pos = Point3(tire.getPosition())
            tirePositions.append([pos[0], pos[1], pos[2]])
        
        self.sendUpdate('endingPositions',[tirePositions])

    def setFinalPositions(self, finalPos):
        """Handle the AI dictating the tire positions."""
        if not self.hasLocalToon: return
        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            tire = self.getTireBody(avId)
            np = self.getTireNp(avId)
            pos = finalPos[index]
            tire.setPosition(pos[0], pos[1], pos[2])
            np.setPos(pos[0], pos[1], pos[2])

        for index in xrange(len(self.avIdList), 4):
            avId = -index
            tire = self.getTireBody(avId)
            np = self.getTireNp(avId)
            pos = finalPos[index]
            tire.setPosition(pos[0], pos[1], pos[2])
            np.setPos(pos[0], pos[1], pos[2])

        #self.gameFSM.request('inputChoice')

    def updateInfoLabel(self):
        """Update the numbers in the info label."""
        self.infoLabel['text'] = TTLocalizer.IceGameInfo % {
            'curMatch' : self.curMatch +1,
            'numMatch' : IceGameGlobals.NumMatches,
            'curRound' : self.curRound +1,
            'numRound' : IceGameGlobals.NumRounds
            }

    def setMatchAndRound(self,  match,  round):
        """Handle the AI dictating the current match and round numbers."""
        if not self.hasLocalToon: return
        self.curMatch = match
        self.curRound = round
        self.updateInfoLabel()
           
    def setScores(self,  match,  round,  scores):
        """Handle the AI scoring the current match."""
        if not self.hasLocalToon: return
        self.newMatch = match
        self.newRound = round
        self.newScores = scores

    def setNewState(self, state):
        """Handle the AI telling us what state to go to."""
        if not self.hasLocalToon: return
        self.notify.debug('setNewState gameFSM=%s newState=%s' %
                          (self.gameFSM, state))
        self.gameFSM.request(state)
        
    def putAllTiresInStartingPositions(self):
        """Move all the tires to their starting positions."""

        for index in xrange(len(self.avIdList)):
            avId = self.avIdList[index]
            np = self.tireDict[avId]['tireNodePath']
            np.setPos(IceGameGlobals.StartingPositions[index])
            self.notify.debug('avId=%s newPos=%s' % (avId, np.getPos))
            np.setHpr(0,0,0)
            quat = np.getQuat()
            body = self.tireDict[avId]['tireBody']
            body.setPosition(IceGameGlobals.StartingPositions[index])
            body.setQuaternion(quat)                            

            
        for index in xrange(len(self.avIdList),4):
            avId = -index
            np = self.tireDict[avId]['tireNodePath']
            np.setPos(IceGameGlobals.StartingPositions[index])
            self.notify.debug('avId=%s newPos=%s' % (avId, np.getPos))
            np.setHpr(0,0,0)
            quat = np.getQuat()
            body = self.tireDict[avId]['tireBody']
            body.setPosition(IceGameGlobals.StartingPositions[index])
            body.setQuaternion(quat)                            


    def b_setForceArrowInfo(self, avId, force, heading ):
        """Set the force arrow info distributedly."""
        self.setForceArrowInfo( avId, force, heading )
        self.d_setForceArrowInfo( avId, force, heading)
            
    def d_setForceArrowInfo(self, avId, force, heading ):
        """Send the force arrow info."""
        # we need to stop sending this every frame
        sendIt = False
        curTime = self.getCurrentGameTime()
        if self.sendForceArrowUpdateAsap:
            sendIt = True
        elif (curTime - self.lastForceArrowUpdateTime) > 0.2:
            sendIt = True

        if sendIt:
            assert self.notify.debugStateCall(self)
            self.sendUpdate('setForceArrowInfo', [avId, force, heading] )
            self.sendForceArrowUpdateAsap = False
            self.lastForceArrowUpdateTime = self.getCurrentGameTime()

    def setForceArrowInfo(self, avId, force, heading):
        """Set the force arrow info locally."""
        if not self.hasLocalToon: return
        self.updateForceArrow(avId, force, heading)
    
    def setupStartOfMatch(self):
        """Setup everyting for the start of a match."""
        #import pdb; pdb.set_trace()
        self.putAllTiresInStartingPositions()
        szId = self.getSafezoneId()        
        self.numTreasures = IceGameGlobals.NumTreasures[szId]
        if self.treasures:
            # remove all old treasures
            for treasure in self.treasures:
                treasure.destroy()
            self.treasures = []
        #for index in xrange(self.numTreasures):
        index = 0
        treasureMargin = IceGameGlobals.TireRadius + 1.0
        while len(self.treasures) < self.numTreasures:
            xPos = self.randomNumGen.randrange( IceGameGlobals.MinWall[0] + 5,
                                                IceGameGlobals.MaxWall[0] - 5)
            yPos = self.randomNumGen.randrange( IceGameGlobals.MinWall[1] + 5,
                                                 IceGameGlobals.MaxWall[1] - 5)
            self.notify.debug('yPos=%s' % yPos)
            pos = Point3(xPos, yPos, IceGameGlobals.TireRadius)
            newTreasure = IceTreasure.IceTreasure(
                self.treasureModel, pos, index, self.doId, penalty=False )
            goodSpot = True
            # make sure the treasure isn't inside another obstacle or treasure
            for obstacle in self.obstacles:
                if newTreasure.nodePath.getDistance(obstacle) < treasureMargin:
                    goodSpot = False;
                    break
            if goodSpot:
                # test against the other treasures
                for treasure in self.treasures:
                    if newTreasure.nodePath.getDistance(
                        treasure.nodePath) < treasureMargin:
                        goodSpot = False;
                        break
            if goodSpot:
                self.treasures.append(newTreasure)
                index +=1
            else:
                newTreasure.destroy()

        # setup the penalties
        self.numPenalties = IceGameGlobals.NumPenalties[szId]
        if self.penalties:
            # remove all old penalties
            for penalty in self.penalties:
                penalty.destroy()
            self.penalties = []
        #for index in xrange(self.numPenalties):
        index = 0
        while len(self.penalties) < self.numPenalties:
            
            xPos = self.randomNumGen.randrange( IceGameGlobals.MinWall[0] + 5,
                                                IceGameGlobals.MaxWall[0] - 5)
            yPos = self.randomNumGen.randrange( IceGameGlobals.MinWall[1] + 5,
                                                 IceGameGlobals.MaxWall[1] - 5)
            self.notify.debug('yPos=%s' % yPos)            
            pos = Point3(xPos, yPos, IceGameGlobals.TireRadius)
            newPenalty = IceTreasure.IceTreasure(
                self.penaltyModel, pos, index, self.doId, penalty = True)
            goodSpot = True
            # make sure the treasure isn't inside another obstacle or treasure
            for obstacle in self.obstacles:
                if newPenalty.nodePath.getDistance(obstacle) < treasureMargin:
                    goodSpot = False;
                    break
            if goodSpot:
                # test against the other treasures
                for treasure in self.treasures:
                    if newPenalty.nodePath.getDistance(
                        treasure.nodePath) < treasureMargin:
                        goodSpot = False;
                        break
            if goodSpot:
                # test against the other penalties
                for penalty in self.penalties:
                    if newPenalty.nodePath.getDistance(
                        penalty.nodePath) < treasureMargin:
                        goodSpot = False;
                        break                    
            if goodSpot:
                self.penalties.append(newPenalty)
                index += 1
            else:
                newPenalty.destroy()


    def toonHitSomething(self, entry):
        """Handle the toon hitting a treasure."""
        self.notify.debug('---- treasure Enter ---- ')
        self.notify.debug('%s' % entry)
        name = entry.getIntoNodePath().getName()
        parts = name.split('-')
        if len(parts) < 3:
            self.notify.debug('collided with %s, but returning' % name)
            return
        if not int(parts[1]) == self.doId:
            self.notify.debug("collided with %s, but doId doesn't match" % name)
            return
        treasureNum = int(parts[2])
        if 'penalty' in parts[0]:
            self.__penaltyGrabbed(treasureNum)
        else:
            self.__treasureGrabbed(treasureNum)

    def __treasureGrabbed(self, treasureNum):
        """ Handle the local toon grabbing this treasure.
        
        Another toon may actually get the credit, proceed as if we got it
        """
        # make the treasure react
        self.treasures[treasureNum].showGrab()
        # play a sound
        self.treasureGrabSound.play()
        # tell the AI we're claiming this treasure
        self.sendUpdate("claimTreasure", [treasureNum])

    def setTreasureGrabbed(self, avId, treasureNum):
        """Update a treaseure being grabbed by a toon."""
        if not self.hasLocalToon: return
        self.notify.debug("treasure %s grabbed by %s" % (treasureNum, avId))

        if avId != self.localAvId:
            # destroy the treasure
            self.treasures[treasureNum].showGrab()

        # update the toon's score
        i = self.avIdList.index(avId)
        self.scores[i] += 1
        self.scorePanels[i].setScore(self.scores[i])

    def __penaltyGrabbed(self, penaltyNum):
        """ Handle the local toon grabbing this penalty.
        
        Another toon may actually get the credit, proceed as if we got it
        """
        # make the penalty react
        self.penalties[penaltyNum].showGrab()
        # play a sound
        #self.penaltyGrabSound.setVolume(0.75)
        #self.penaltyGrabSound.play()
        # tell the AI we're claiming this treasure
        self.sendUpdate("claimPenalty", [penaltyNum])

    def setPenaltyGrabbed(self, avId, penaltyNum):
        """Update a treasure being grabbed by a toon."""
        if not self.hasLocalToon: return
        self.notify.debug("penalty %s grabbed by %s" % (penaltyNum, avId))

        if avId != self.localAvId:
            # destroy the penalty
            self.penalties[penaltyNum].showGrab()

        # update the toon's score
        i = self.avIdList.index(avId)
        self.scores[i] -= 1
        self.scorePanels[i].setScore(self.scores[i])

    def postStep(self):
        """Play sounds as needed after one simulation step."""
        DistributedIceWorld.DistributedIceWorld.postStep(self)

        #self.notify.debug('in post step --------------------------')
        for count in range(self.colCount):
            c0, c1 = self.getOrderedContacts(count,)
            #self.notify.debug('c0=%s c1=%s' % (c0, c1))
            if c1 in self.tireCollideIds:
                # a tire hit something
                tireIndex = self.tireCollideIds.index(c1)
                if c0 in self.tireCollideIds:
                    # a tire hit another tire                    
                    self.tireSounds[tireIndex]['tireHit'].play()
                elif c0 == self.wallCollideId:
                    # a tire hit a wall
                    self.tireSounds[tireIndex]['wallHit'].play()
                elif c0 == self.obstacleCollideId:
                    # a tire hit an obstacle
                    self.tireSounds[tireIndex]['obstacleHit'].play()
                pass
        
        pass

    def forceLocalToonToTire(self):
        """Force the local toon to be inside the tire."""
        # looks like it's pretty rare, but the local toon can be bumped out
        # of the tire,  this forces him back inside
        toon = localAvatar
        if toon and self.localAvId in self.tireDict:
            tireNp = self.tireDict[self.localAvId]['tireNodePath']
            toon.reparentTo(tireNp)
            toon.setPosHpr(0,0,0,0,0,0)
            toon.setY(1.0)
            toon.setZ(-3)
