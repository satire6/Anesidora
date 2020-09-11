"""DistributedTwoDGame module: contains the DistributedTwoDGame class 

This has a 2D Scroller game type mechanic:
left arrow : makes the toon run left
right arrow: makes the toon run right
up arrow   : makes the toon jump
down arrow : does nothing for now
Ctrl       : makes the toon shoot

DistributedTwoDGame controls are a bit complicated and it uses mechanics of
2 different walkers to make it work.
1) It uses TwoDWalker (in direct/src/controls/), a derivative of GravityWalker 
   for controlling the jump mechanic.
2) It uses the OrthoWalk class along with the TwoDDrive class (in toontown/src/minigame/) 
   for controlling the left-right running. The TwoDDrive class instantiates 
   ArrowKeys, which is used to grab the Ctrl press. This is used for the shooting.

@TODO : Re-write the entire code to make it one concise, so that future classes
can just derive from DistributedTwoDGame for any 2D scroller type of game.
"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase import TTLocalizer
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import DGG
from direct.task.Task import Task
from direct.fsm import ClassicFSM, State
from direct.directnotify import DirectNotifyGlobal
from DistributedMinigame import *
import MinigameAvatarScorePanel, ArrowKeys, ToonBlitzAssetMgr, TwoDCamera
import TwoDSectionMgr, ToonBlitzGlobals, TwoDGameToonSD
from toontown.toonbase import ToontownTimer
from TwoDWalk import *
from TwoDDrive import *

COLOR_RED = VBase4(1, 0, 0, 0.3)

class DistributedTwoDGame(DistributedMinigame):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTwoDGame')
    # define constants that you won't want to tweak here
    
    UpdateLocalToonTask = "ToonBlitzUpdateLocalToonTask" # name of the update task called each frame
    EndGameTaskName = 'endTwoDGame'

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.gameFSM = ClassicFSM.ClassicFSM('DistributedTwoDGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup', 'pause', 'showScores']),
                                State.State('pause',
                                            self.enterPause,
                                            self.exitPause,
                                            ['cleanup', 'play', 'showScores']),
                                State.State('showScores',
                                            self.enterShowScores,
                                            self.exitShowScores,
                                            ['cleanup']),                                            
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
        
        if __debug__:
            base.mg = self
            self.accept('p', self.debugStartPause)
            self.accept('o', self.debugEndPause)
##            self.accept('y', self.localToonVictory)
        
        self.reportedDone = False
        self.showCollSpheres = False

    def getTitle(self):
        return TTLocalizer.TwoDGameTitle        

    def getInstructions(self):
        return TTLocalizer.TwoDGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 200
    
    def __defineConstants(self):
        '''Define all the game contants here.'''
        self.TOON_SPEED = 12.0
        self.MAX_FRAME_MOVE = 1
        self.isHeadInFloor = False
        self.timeToRunToElevator = 1.5

    def setSectionsSelected(self, sectionsSelected):
        """ Set the sectionsSelected as dictated by the AI."""
        self.sectionsSelected = sectionsSelected
    
    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        self.__defineConstants()
        # Load resources and create objects here
        # Create Asset Manager and load assets
        self.assetMgr = ToonBlitzAssetMgr.ToonBlitzAssetMgr(self)
        # Create camera
        self.cameraMgr = TwoDCamera.TwoDCamera(camera)        
        # Create a Section Manager
        self.sectionMgr = TwoDSectionMgr.TwoDSectionMgr(self, self.sectionsSelected)        
        # Get the start and end X values of the game. Required for the progress line.
        self.gameStartX = -40.
        endSection = self.sectionMgr.sections[-1]
        # This is just to confirm that the last section is actually the endSection
        assert endSection.sectionTypeNum == 'end'
        self.gameEndX = endSection.spawnPointMgr.gameEndX
        self.gameLength = self.gameEndX - self.gameStartX
        
        # make a dictionary of TwoDGameToonSDs; they will track
        # toons' states and animate them appropriately
        self.toonSDs = {}
        # add the local toon now, add remote toons as they join
        avId = self.localAvId
        toonSD = TwoDGameToonSD.TwoDGameToonSD(avId, self)
        self.toonSDs[avId] = toonSD
        # The toon with the higher drawNum is rendered closer to the camera.
        # Local toon is rendered with a drawNum of 0. In the progress line the
        # other toons appear in front of the localToon.
        self.toonSDs[avId].createHeadFrame(0)

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        taskMgr.remove(self.UpdateLocalToonTask)
        
        # unload resources and delete objects from load() here        
        for avId in self.toonSDs.keys():
            toonSD = self.toonSDs[avId]
            toonSD.destroy()
        del self.toonSDs
        
        self.cameraMgr.destroy()
        del self.cameraMgr
        
        self.sectionMgr.destroy()
        del self.sectionMgr
        
        for panel in self.scorePanels:
            panel.cleanup()
        del self.scorePanels
        
        self.assetMgr.destroy()
        del self.assetMgr
        
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        
        self.scorePanels = []
        
        # start up the minigame; parent things to render, start playing music...
        self.assetMgr.onstage()
        
        # Displaying the local avatar
        lt = base.localAvatar
        lt.reparentTo(render)
##        lt.setBin('fixed', 10)
        lt.hideName()
        self.__placeToon(self.localAvId)
        lt.setAnimState('Happy', 1.0)
        lt.setSpeed(0,0)
        base.localAvatar.collisionsOn()
        base.localAvatar.setTransparency(1)
        # Create Head Collision for the local avatar
        self.setupHeadCollision()
        
        self.cameraMgr.onstage()
        
        toonSD = self.toonSDs[self.localAvId]
        toonSD.enter()
        toonSD.fsm.request('normal')
        
        self.twoDDrive = TwoDDrive(self, self.TOON_SPEED, maxFrameMove=self.MAX_FRAME_MOVE)
        # at this point we cannot yet show the remote players' toons

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the music...
        self.assetMgr.offstage()
        
        for avId in self.toonSDs.keys():
            self.toonSDs[avId].exit()
        
        base.localAvatar.setTransparency(0)
        
        self.ignore('enterheadCollSphere-into-floor1')
        base.localAvatar.controlManager.currentControls.cTrav.removeCollider(self.headCollNP)
        self.headCollNP.removeNode()
        del self.headCollNP
        
        # Show the laff meter
        base.localAvatar.laffMeter.start()
        
        #@TODO: setIntoBitMask of distAvatarCollNode of all the toons to 0x1
        #@TODO: setBin to default for all toons        
        
        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game; it's safe to show them now.                
        
        drawNum = 0
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                drawNum += 1
                toon.reparentTo(render)
##                toon.setBin('fixed', drawNum)
                toon.setAnimState('Happy', 1.0)
                toon.hideName()
                # Start a smoothing task
                toon.startSmooth()
                toon.startLookAround()
                # Switching off the Bitmask for distAvatarCollNode 
                # so that the toons don't collide against each other
                distCNP = toon.find('**/distAvatarCollNode*')
                distCNP.node().setIntoCollideMask(BitMask32.allOff())
                
                # create the toonSD for this toon
                toonSD = TwoDGameToonSD.TwoDGameToonSD(avId, self)
                self.toonSDs[avId] = toonSD
                toonSD.enter()
                toonSD.fsm.request('normal')
                # The toon with the higher drawNum is rendered closer to the camera
                self.toonSDs[avId].createHeadFrame(drawNum)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules, and are ready to start playing.
        
##        self.twoDDrive = TwoDDrive(self, self.TOON_SPEED, maxFrameMove=self.MAX_FRAME_MOVE)
        
        self.twoDWalk = TwoDWalk(self.twoDDrive, broadcast = not self.isSinglePlayer())
        
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
            scorePanel.setPos(.75 - spacing*((self.numPlayers-1)-i), 0.0, .85)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels.append(scorePanel)
        
        # Transition to the appropriate state
        self.gameFSM.request("play", [timestamp])

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self, timestamp):
        self.notify.debug("enterPlay")
        
        # Calculated to make sure all Lerps will start at the same time
        elapsedTime = globalClockDelta.localElapsedTime(timestamp)
        
        self.sectionMgr.enterPlay(elapsedTime)
        # Enable shootKeyHandler() to handle Ctrl 
        handlers =  [None, None, None, None, self.shootKeyHandler]
        self.twoDDrive.arrowKeys.setPressHandlers(handlers)
        # Start twoDWalk so that left-right walking works
        self.twoDWalk.start()
        
        # Listen to 'jumpStart' to play jump sound
        self.accept('jumpStart', self.startJump)
        # Listen for enemy collision
        self.accept('enemyHit', self.localToonHitByEnemy)
        # Listen for treasure collision
        self.accept('twoDTreasureGrabbed', self.__treasureGrabbed)
        # Listen for for enemy shot
        self.accept('enemyShot', self.__enemyShot)
        
        # This is the local toon task (game loop for the local toon)
        taskMgr.remove(self.UpdateLocalToonTask)
        # Making the priority of this task 1 because this controls the camera.
        # We want the camera pos to be calculated after the toon pos has been
        # calculated, which happens in TwoDDrive.__update().
        taskMgr.add(self.__updateLocalToonTask, self.UpdateLocalToonTask, priority = 1)
            
        # Hide the laff meter
        base.localAvatar.laffMeter.stop()
        
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(ToonBlitzGlobals.GameDuration[self.getSafezoneId()])
        self.timer.countdown(ToonBlitzGlobals.GameDuration[self.getSafezoneId()], self.timerExpired)
        
    def exitPlay(self):
        # Remove all handles so that we don't track Ctrl
        handlers =  [None, None, None, None, None]
        self.twoDDrive.arrowKeys.setPressHandlers(handlers)
        
        # Loop idle animation so that the toon is standing while showing showing the score.
        # Do this only if player is not in victory state.
        if (self.toonSDs[self.localAvId].fsm.getCurrentState().getName() != 'victory'):
            base.localAvatar.b_setAnimState('Happy', 1.0)
        
        # Stop listening to 'jumpStart' because we don't need to play jump sound
        self.ignore('jumpStart')
        self.ignore('enemyHit')
        self.ignore('twoDTreasureGrabbed')
    
    def enterPause(self):
        self.notify.debug('enterPause')
    
    def exitPause(self):
        pass
    
    def enterShowScores(self):
        self.notify.debug("enterShowScores")

        # lerp up the goal bar, score panels
        lerpTrack = Parallel()
        lerpDur = .5
        
        # score panels
        # top/bottom Y
        tY = .6; bY = -.6
        # left/center/right X
        lX = -.7; cX = 0; rX = .7
        scorePanelLocs = (
            ((cX,bY),),
            ((lX,bY),(rX,bY)),
            ((cX,bY),(lX,bY),(rX,bY)),
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
                                  Vec3(panel.getScale())*1.5,
                                  blendType='easeInOut'),
                ))

        self.showScoreTrack = Parallel(
            lerpTrack,
            self.getElevatorCloseTrack(),
            Sequence(Wait(ToonBlitzGlobals.ShowScoresDuration),
                     Func(self.gameOver),
                     ),
            )

        self.showScoreTrack.start()
        
    def exitShowScores(self):
        # calling finish() here would cause problems if we're
        # exiting abnormally, because of the gameOver() call
        self.showScoreTrack.pause()
        del self.showScoreTrack
    
    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        
        self.timer.stop()
        self.timer.destroy()
        del self.timer
        
        taskMgr.remove(self.EndGameTaskName)
        # Stop twoDWalk to stop left-right movement
        self.twoDWalk.stop()
        self.twoDWalk.destroy()
        del self.twoDWalk
        self.twoDDrive = None
        del self.twoDDrive

    def exitCleanup(self):
        pass
    
    def acceptInputs(self):
        # Enable shootKeyHandler() to handle Ctrl
        if hasattr(self, 'twoDDrive'):
            handlers =  [None, None, None, None, self.shootKeyHandler]
            self.twoDDrive.arrowKeys.setPressHandlers(handlers)
            # Start twoDDrive so that left-right walking works
            self.twoDDrive.start()
        
    def ignoreInputs(self):
        # Remove all handles so that we don't track Ctrl
        if hasattr(self, 'twoDDrive'):
            handlers =  [None, None, None, None, None]
            self.twoDDrive.arrowKeys.setPressHandlers(handlers)
            # Stop twoDDrive to stop left-right movement
            self.twoDDrive.lastAction = None
            self.twoDDrive.stop()
    
    def __updateLocalToonTask(self, task):
        dt = globalClock.getDt()
        self.cameraMgr.update()
        
        # ALWAYS keep the toon at y=0
        if self.gameFSM.getCurrentState().getName() == 'play':
            # Only exception is when the local toon has reached the victory state.
            if not self.toonSDs[self.localAvId].fsm.getCurrentState().getName() == 'victory':
                if not (base.localAvatar.getY() == 0):
                    base.localAvatar.setY(0)
        
        # Handle if toon falls into a pit
        if (base.localAvatar.getZ() < -2.):
            self.localToonFellDown()
            
        for avId in self.toonSDs.keys():
            self.toonSDs[avId].update()
                    
        return task.cont
    
    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears
        self.toonSDs[avId].exit(unexpectedExit = True)
        del self.toonSDs[avId]
        # then call the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)
    
    def setupHeadCollision(self):
        collSphere = CollisionSphere(0, 0, 0, 1)
        collSphere.setTangible(1)
        collNode = CollisionNode('headCollSphere')
        collNode.setFromCollideMask(ToontownGlobals.WallBitmask)
        collNode.setIntoCollideMask(BitMask32.allOff())
        collNode.addSolid(collSphere)
        head = base.localAvatar.getPart('head', '1000')
        self.headCollNP = head.attachNewNode(collNode)
        self.headCollNP.setPos(0,0,0.0)        
        # I'm positioning the headCollNP at different Z values because the different animal
        # species have different heights. The headCollNP prevents the toon from going through
        # a floor. For tall toons, I bring the headCollNP lower so that the toon can complete
        # a jump onto a 2nd platform without banging it's head on the 3rd platform. 
        animal = base.localAvatar.style.getAnimal()
        if (animal == 'dog') or (animal == 'bear') or (animal == 'horse'):
            torso = base.localAvatar.style.torso
            legs = base.localAvatar.style.legs
            if ((torso == 'ls') or (torso == 'ld')) and (legs == 'l'):
                self.headCollNP.setZ(-1.3)
            else:
                self.headCollNP.setZ(-0.7)
        elif (animal == 'mouse') or (animal == 'duck'):
            self.headCollNP.setZ(0.5)
        elif (animal == 'cat'):
            self.headCollNP.setZ(-0.3)
        elif (animal == 'rabbit'):
            self.headCollNP.setZ(-0.5)
        elif (animal == 'monkey'):
            self.headCollNP.setZ(0.3)
        elif (animal == 'pig'):
            self.headCollNP.setZ(-0.7)
        
        self.headCollNP.hide()
        if self.showCollSpheres:
            self.headCollNP.show()

        # Setting up the collision event handler
        headCollisionEvent = CollisionHandlerEvent()
        headCollisionEvent.addInPattern("enter%fn-into-%in")
        headCollisionEvent.addOutPattern("%fn-exit-%in")
        # Adding this as a collider to the main local avatar's traverser
        cTrav = base.localAvatar.controlManager.currentControls.cTrav
        cTrav.addCollider(self.headCollNP, headCollisionEvent)
        self.accept('enterheadCollSphere-into-floor1', self.__handleHeadCollisionIntoFloor)
        self.accept('headCollSphere-exit-floor1', self.__handleHeadCollisionExitFloor)
    
    def __handleHeadCollisionIntoFloor(self, cevent):
        # Toon's head is hitting a floor.
        # Making the up velocity 0 when you hit a floor. Only while going up.
        self.isHeadInFloor = True
        if (base.localAvatar.controlManager.currentControls.lifter.getVelocity() > 0):
            base.localAvatar.controlManager.currentControls.lifter.setVelocity(0.)
            # Play collision sound
            self.assetMgr.playHeadCollideSound()
            
    def __handleHeadCollisionExitFloor(self, cevent):
        # Toon's head is exiting the floor.
        # Check this flag before jumping in TwoDDrive.
        self.isHeadInFloor = False
    
    def __placeToon(self, avId):
        """Places a toon in its starting position."""
        toon = self.getAvatar(avId)
        i = self.avIdList.index(avId)
        pos = Point3(ToonBlitzGlobals.ToonStartingPosition[0] + i,
                     ToonBlitzGlobals.ToonStartingPosition[1],
                     ToonBlitzGlobals.ToonStartingPosition[2])
        toon.setPos(pos)
        toon.setHpr(-90, 0, 0)
    
    def startJump(self):
        """
        This function does not control the start of the jump.
        GravityWalker controls jump and sends a msg "jumpStart".
        This function is only called because we are listening to the "jumpStart" msg.
        """
##        self.notify.debug('startJump')
        # Play start jump sound here
        self.assetMgr.playJumpSound()
    
    def checkValidity(self, avId):
        if not self.hasLocalToon: return False
    
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.warning('ignoring msg: av %s performing some action.' % avId)
            return False
        
        # try to see if the avId is valid, return if not
        toon = self.getAvatar(avId)
        if toon == None:
            return False
                
        return True
    
    def shootKeyHandler(self):
        """Handle pressing the Ctrl key."""
        self.toonSDs[self.localAvId].shootGun()
        timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
        self.sendUpdate('showShootGun', [self.localAvId, timestamp])

    def showShootGun(self, avId, timestamp):
        """ called when remote toon shoots gun """
        if self.checkValidity(avId):
            self.notify.debug("avatar %s is shooting water gun" % avId)
            if avId != self.localAvId:
                self.toonSDs[avId].shootGun()
    
    def localToonFellDown(self):
        """ Called when the local toon falls through a hole."""
        if (self.toonSDs[self.localAvId].fsm.getCurrentState().getName() != 'fallDown'):
            self.toonSDs[self.localAvId].fsm.request('fallDown')
            timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
            # Update local toon's score
            self.updateScore(self.localAvId, ToonBlitzGlobals.ScoreLossPerFallDown[self.getSafezoneId()])
            self.sendUpdate('toonFellDown', [self.localAvId, timestamp])
    
    def toonFellDown(self, avId, timestamp):
        """ Called when a remote toon falls through a hole."""
        if self.checkValidity(avId):
            self.notify.debug("avatar %s fell down." % avId)
            if avId != self.localAvId:
                # Update remote toon's score
                self.updateScore(avId, ToonBlitzGlobals.ScoreLossPerFallDown[self.getSafezoneId()])
                self.toonSDs[avId].fsm.request('fallDown')
    
    def localToonHitByEnemy(self):
        """ Called when a suit collides with localToon."""
        # If not already in fallBack or squished state
        currToonState = self.toonSDs[self.localAvId].fsm.getCurrentState().getName()
        if not (currToonState == 'fallBack' or currToonState == 'squish'):
            self.toonSDs[self.localAvId].fsm.request('fallBack')
            timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
            # Update local toon's score
            self.updateScore(self.localAvId, ToonBlitzGlobals.ScoreLossPerEnemyCollision[self.getSafezoneId()])
            self.sendUpdate('toonHitByEnemy', [self.localAvId, timestamp])
        
    def toonHitByEnemy(self, avId, timestamp):
        """ Called when a remote toon is hit by suit."""
        if self.checkValidity(avId):
            self.notify.debug("avatar %s hit by a suit" % avId)
            if avId != self.localAvId:
                # Update remote toon's score
                self.updateScore(avId, ToonBlitzGlobals.ScoreLossPerEnemyCollision[self.getSafezoneId()])
                self.toonSDs[avId].fsm.request('fallBack')
                
    def localToonSquished(self):
        """ Called when the local toon gets squished by a stomper."""
        # If not already in fallBack or squished state
        currToonState = self.toonSDs[self.localAvId].fsm.getCurrentState().getName()
        if not (currToonState == 'fallBack' or currToonState == 'squish'):
            self.toonSDs[self.localAvId].fsm.request('squish')
            timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
            # Update local toon's score
            self.updateScore(self.localAvId, ToonBlitzGlobals.ScoreLossPerStomperSquish[self.getSafezoneId()])
            # Tell others that the local toon got squished
            self.sendUpdate('toonSquished', [self.localAvId, timestamp])
        
    def toonSquished(self, avId, timestamp):
        """ Called whan a remote toon is squished by a stomper."""
        if self.checkValidity(avId):
            self.notify.debug("avatar %s is squished." % avId)
            if (avId != self.localAvId):
                # Update remote toon's score
                self.updateScore(avId, ToonBlitzGlobals.ScoreLossPerStomperSquish[self.getSafezoneId()])
                self.toonSDs[avId].fsm.request('squish')
    
    def localToonVictory(self):
        """ Called when localToon reaches the end of tunnel. """
        if not ToonBlitzGlobals.EndlessGame:
            self.ignoreInputs()
        if not (self.toonSDs[self.localAvId].fsm.getCurrentState().getName() == 'victory'):
            self.toonSDs[self.localAvId].fsm.request('victory')
            timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
            self.sendUpdate('toonVictory', [self.localAvId, timestamp])
        
    def toonVictory(self, avId, timestamp):
        """ Called when a remote toon reaches the end of tunnel. """
        if self.checkValidity(avId):
            self.notify.debug("avatar %s achieves victory" % avId)
            if avId != self.localAvId:
                self.toonSDs[avId].fsm.request('victory')
        
    def addVictoryScore(self, avId, score):
        """ Called by the AI to set the victory score on the toon who has completed the game."""
        if not self.hasLocalToon: return
        # Update the toon's score
        self.updateScore(avId, score)
        # Play sound for the local player
        if (avId == self.localAvId):
            self.assetMgr.threeSparkles.play()
    
    def __treasureGrabbed(self, sectionIndex, treasureIndex):
        """ Handle the local toon grabbing this treasure.
        Another toon may actually get the credit, proceed as if we got it
        """
        self.notify.debug('treasure %s-%s grabbed' %(sectionIndex, treasureIndex))
        # make the treasure react   
        section = self.sectionMgr.sections[sectionIndex]
        section.treasureMgr.treasures[treasureIndex].hideTreasure()
        # play a sound
        self.assetMgr.treasureGrabSound.play()
        # tell the AI we're claiming this treasure
        self.sendUpdate("claimTreasure", [sectionIndex, treasureIndex])
        
    def setTreasureGrabbed(self, avId, sectionIndex, treasureIndex):
        """Update a treasure being grabbed by a toon."""
        if not self.hasLocalToon: return
        # Grab treasure only if we're still playing
        if (self.gameFSM.getCurrentState().getName() == 'play'):
            self.notify.debug("treasure %s-%s grabbed by %s" % (sectionIndex, treasureIndex, avId))
            numSections = len(self.sectionMgr.sections)
            # numSections includes the end section also.
##            assert (sectionIndex < numSections)
            if (sectionIndex < numSections):
                section = self.sectionMgr.sections[sectionIndex]
                
                numTreasures = len(section.treasureMgr.treasures)
##                assert (treasureIndex < numTreasures)
                if (treasureIndex < numTreasures):
                    treasure = section.treasureMgr.treasures[treasureIndex]
                    if avId != self.localAvId:
                        # destroy the treasure
                        treasure.hideTreasure()
                        
                    # Update the toon's score
                    self.updateScore(avId, ToonBlitzGlobals.ScoreGainPerTreasure * treasure.value)
                else:
                    self.notify.error('WHOA!! treasureIndex %s is out of range; numTreasures = %s' %(treasureIndex, numTreasures))
                    base.localAvatar.sendLogMessage('treasureIndex %s is out of range; numTreasures = %s' %(treasureIndex, numTreasures))
            else:
                self.notify.error('WHOA!! sectionIndex %s is out of range; numSections = %s' %(sectionIndex, numSections))
                base.localAvatar.sendLogMessage('sectionIndex %s is out of range; numSections = %s' %(sectionIndex, numSections))
        
    def __enemyShot(self, sectionIndex, enemyIndex):
        """
        Handle the local toon shooting the enemy of enemyIndex.
        Send a message to the AI.
        """
##        self.notify.debug('enemy %s-%s shot' %(sectionIndex, enemyIndex))
        # Play cog hit effect for the local client
        self.sectionMgr.sections[sectionIndex].enemyMgr.enemies[enemyIndex].doShotTrack()
        # play a sound
        
        # tall the AI we're claiming the shot
        self.sendUpdate('claimEnemyShot', [sectionIndex, enemyIndex])
    
    def setEnemyShot(self, avId, sectionIndex, enemyIndex, enemyHealth):
        """
        This method is called by the AI to all the clients.
        enemyIndex has been shot by avId.
        Update effects on the enemyIndex
        If avId is local toon update score.
        """
        if not self.hasLocalToon: return
    
        # Enemy is hit only if we're still playing
        if (self.gameFSM.getCurrentState().getName() == 'play'):
            self.notify.debug('enemy %s is shot by %s. Health left %s' %(enemyIndex, avId, enemyHealth))
            if (enemyHealth > 0):
                # Enemy is still alive.
                # Don't play the shotTrack for the local client, because we already played it.
                if not (avId == self.localAvId):
                    self.sectionMgr.sections[sectionIndex].enemyMgr.enemies[enemyIndex].doShotTrack()
            else:
                enemy  = self.sectionMgr.sections[sectionIndex].enemyMgr.enemies[enemyIndex]
                # Show the spawned treasure
                treasureSpawnPoint = Point3(enemy.suit.getX(), enemy.suit.getY(), enemy.suit.getZ() + enemy.suit.height / 2.)
                self.spawnTreasure(sectionIndex, enemyIndex, treasureSpawnPoint)
                # Enemy just died. Play Death animation.
                enemy.doDeathTrack()
    
    def updateScore(self, avId, deltaScore):
        i = self.avIdList.index(avId)
        self.scores[i] += deltaScore
        self.scorePanels[i].setScore(self.scores[i])
        self.toonSDs[avId].showScoreText(deltaScore)
    
    def spawnTreasure(self, sectionIndex, enemyIndex, pos):
        # Spawn a treasure if we're still playing
        if (self.gameFSM.getCurrentState().getName() == 'play'):
            # Place the correct treasure in the right position and show it
            section = self.sectionMgr.sections[sectionIndex]
            treasure = section.treasureMgr.enemyTreasures[enemyIndex]
            treasure.setTreasurePos(pos)
            treasure.popupEnemyTreasure()
            
    def timerExpired(self):
        self.notify.debug('timer expired')
        if not self.reportedDone:
            if not ToonBlitzGlobals.EndlessGame:
                self.ignoreInputs()
            self.reportedDone = True
            self.sendUpdate('reportDone')
    
    def setEveryoneDone(self):
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.warning('ignoring setEveryoneDone msg')
            return
        
        self.notify.debug('setEveryoneDone')
        def endGame(task, self=self):
            if not ToonBlitzGlobals.EndlessGame:
                self.gameFSM.request('showScores')
            return Task.done
        
        # hide the timer
        self.timer.hide()
        
        taskMgr.doMethodLater(1, endGame, self.EndGameTaskName)
    
    def getElevatorCloseTrack(self):
        leftDoor = self.sectionMgr.exitElevator.find('**/doorL')
        rightDoor = self.sectionMgr.exitElevator.find('**/doorR')
        leftDoorClose = LerpPosInterval(leftDoor, 2, Point3(3.02, 0, 0))
        rightDoorClose = LerpPosInterval(rightDoor, 2, Point3(-3.02, 0, 0))
        return Sequence(Wait(self.timeToRunToElevator),
                        Parallel(leftDoorClose, rightDoorClose))
    
    def debugStartPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        self.sectionMgr.enterPause()
            
    def debugEndPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        self.sectionMgr.exitPause()