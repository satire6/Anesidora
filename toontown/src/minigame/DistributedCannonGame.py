
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from DistributedMinigame import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownTimer
from direct.task.Task import Task
import Trajectory
import math
from toontown.toon import ToonHead
from toontown.effects import Splash
from toontown.effects import DustCloud
import CannonGameGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

# some constants
LAND_TIME = 2

WORLD_SCALE = 2.

GROUND_SCALE = 1.4 * WORLD_SCALE
CANNON_SCALE = 1.0

FAR_PLANE_DIST = 600 * WORLD_SCALE

CANNON_Y = -int((CannonGameGlobals.TowerYRange/2)*1.3)
CANNON_X_SPACING = 12
CANNON_Z = 20

# send cannon movement messages for the local cannon at this frequency
CANNON_MOVE_UPDATE_FREQ = 0.5

# these determine the range of distances the camera will
# pull back, away from the toon, in-flight
CAMERA_PULLBACK_MIN = 20
CAMERA_PULLBACK_MAX = 40

# this is the maximum offset of the lookAt point, along
# the ground, in a direction perpendicular to the toon's
# flight path
MAX_LOOKAT_OFFSET = 80

# when the toon is this close to the tower (or closer),
# in feet, the camera will pull back, and the lookAt
# point will extend away from the tower (see above)
TOON_TOWER_THRESHOLD = 150

SHADOW_Z_OFFSET = 0.5

TOWER_HEIGHT = 43.85
TOWER_RADIUS = 10.5
BUCKET_HEIGHT = 36 # collide only with the bucket at the top of
                   # the tower, not with the legs

# this is how far away the tower is on the axis that points
# straight out in front of the cannons
TOWER_Y_RANGE = CannonGameGlobals.TowerYRange
# this gets tapered as the tower gets closer to the cannons in Y
TOWER_X_RANGE = int(TOWER_Y_RANGE / 2.)

#INITIAL_VELOCITY = 85.0 #original
INITIAL_VELOCITY = 94.0

# this is how fast you have to be falling to generate a whistling sound
WHISTLE_SPEED = INITIAL_VELOCITY * 0.55

class DistributedCannonGame(DistributedMinigame):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMinigame")

    font = ToontownGlobals.getToonFont()

    LOCAL_CANNON_MOVE_TASK = "localCannonMoveTask"
    REWARD_COUNTDOWN_TASK   = "cannonGameRewardCountdown"

    # flags for objects that the toons can hit
    HIT_GROUND = 0
    HIT_TOWER  = 1
    HIT_WATER  = 2

    # keyboard controls
    FIRE_KEY  = "control"
    UP_KEY    = "arrow_up"
    DOWN_KEY  = "arrow_down"
    LEFT_KEY  = "arrow_left"
    RIGHT_KEY = "arrow_right"

    INTRO_TASK_NAME = "CannonGameIntro"
    INTRO_TASK_NAME_CAMERA_LERP = "CannonGameIntroCamera"

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        # NOTE: it would be nice to be able to kick off the gameFSM
        # before DistributedMinigame goes into its 'game' state
        # currently, gameFSM *is* DistributedMinigame's 'game'
        # state; entering the 'game' state resets the gameFSM =(

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedCannonGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['aim']),
                                State.State('aim',
                                            self.enterAim,
                                            self.exitAim,
                                            ['shoot',
                                             'waitForToonsToLand',
                                             'cleanup']),
                                State.State('shoot',
                                            self.enterShoot,
                                            self.exitShoot,
                                            ['aim',
                                             'waitForToonsToLand',
                                             'cleanup']),
                                State.State('waitForToonsToLand',
                                            self.enterWaitForToonsToLand,
                                            self.exitWaitForToonsToLand,
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

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        # this will hold the locations of the cannons
        # lookup by avId
        self.cannonLocationDict = {}

        # this will hold the current cannon positions
        # consisting of [rotation, angle]
        # lookup by avId
        self.cannonPositionDict = {}

        # this will hold references to the actual cannon models
        # lookup by avId
        self.cannonDict = {}

        # this will hold nodepaths for the toon models, including
        # a translation that places their local origin in their waist
        self.toonModelDict = {}

        # this will hold drop shadow models
        self.dropShadowDict = {}

        # this will hold the toon heads, which are used when the toons
        # are loaded in the cannons, to avoid body parts sticking out
        # of the sides of the cannon barrels
        self.toonHeadDict = {}

        # this will hold the scales of the toons
        self.toonScaleDict = {}

        # This will hold the slip down the side of the tower intervals
        self.toonIntervalDict = {}

        # these keep track of the local cannon controls
        # since there are multiple inputs tied to each
        # of these (buttons and keypresses), they are
        # incremented for every button or keypress
        # that is active
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0

        # this is set to true when the local cannon is moving
        self.cannonMoving = 0

        self.modelCount = 14

    def getTitle(self):
        return TTLocalizer.CannonGameTitle

    def getInstructions(self):
        return TTLocalizer.CannonGameInstructions

    def getMaxDuration(self):
        return CannonGameGlobals.GameTime

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky")
        self.ground = loader.loadModel(
            "phase_4/models/minigames/toon_cannon_gameground")
        self.tower = loader.loadModel(
            "phase_4/models/minigames/toon_cannon_water_tower")
        self.cannon = loader.loadModel(
            "phase_4/models/minigames/toon_cannon")
        self.dropShadow = loader.loadModel(
            "phase_3/models/props/drop_shadow")
        self.hill = loader.loadModel(
            "phase_4/models/minigames/cannon_hill")

        self.sky.setScale(WORLD_SCALE)
        self.ground.setScale(GROUND_SCALE)
        self.cannon.setScale(CANNON_SCALE)
        self.dropShadow.setColor(0,0,0,0.5)
        # make the ground dark so it contrasts with the hill
        self.ground.setColor(0.85, 0.85, 0.85, 1.0)
        # the hill model is 20 feet tall
        self.hill.setScale(1, 1, CANNON_Z / 20.)

        # put the shadow in the 'fixed' bin, so that it will be
        # drawn correctly in front of the translucent water
        # NOTE: if we put trees or other opaque/transparent
        # objects in the scene, put the shadow in the fixed
        # bin only when it's over the water
        # undo with shadow.clearBin()
        self.dropShadow.setBin('fixed', 0, 1)

        # Splash object for when toon hits the water
        self.splash = Splash.Splash(render)
        # Dust cloud object for when toon hits ground
        self.dustCloud = DustCloud.DustCloud(render)

        # load the jellybean jar image
        # this model is 'owned' (read: destroyed) by PurchaseBase
        purchaseModels = loader.loadModel(
                "phase_4/models/gui/purchase_gui")
        self.jarImage = purchaseModels.find("**/Jar")
        self.jarImage.reparentTo(hidden)

        # reward display
        self.rewardPanel = DirectLabel(
            parent = hidden,
            relief = None,
            pos = (1.16, 0.0, 0.45),
            scale = .65,
            text = '',
            text_scale = 0.2,
            text_fg = (0.95, 0.95, 0, 1),
            text_pos = (0, -.13),
            text_font = ToontownGlobals.getSignFont(),
            image = self.jarImage,
            )
        self.rewardPanelTitle = DirectLabel(
            parent = self.rewardPanel,
            relief = None,
            pos = (0, 0, 0.06),
            scale = .08,
            text = TTLocalizer.CannonGameReward,
            text_fg = (.95,.95,0,1),
            text_shadow = (0,0,0,1),
            )

        self.music = base.loadMusic(
            #"phase_3/audio/bgm/create_a_toon.mid"
            #"phase_4/audio/bgm/TC_SZ_activity.mid"
            #"phase_4/audio/bgm/TC_nbrhood.mid"
            #"phase_4/audio/bgm/minigame_race.mid"
            "phase_4/audio/bgm/MG_cannon_game.mid"
            )

        self.sndCannonMove = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_adjust.mp3")
        self.sndCannonFire = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_fire_alt.mp3")
        self.sndHitGround  = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_hit_dirt.mp3")
        self.sndHitTower   = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_hit_tower.mp3")
        self.sndHitWater   = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_splash.mp3")
        self.sndWhizz      = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_whizz.mp3")
        self.sndWin        = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_win.mp3")
        self.sndRewardTick = base.loadSfx(\
                                 "phase_3.5/audio/sfx/tick_counter.mp3")

        # set up the cannon aiming/firing gui
        guiModel = "phase_4/models/gui/cannon_game_gui"
        cannonGui = loader.loadModel(guiModel)
        self.aimPad = DirectFrame(image = cannonGui.find("**/CannonFire_PAD"),
                                  relief = None,
                                  pos = (0.7, 0, -0.553333),
                                  scale = 0.8,
                                  )
        cannonGui.removeNode()
        # hide the interface
        self.aimPad.hide()

        # add the fire and arrow buttons
        self.fireButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Fire_Btn_UP"),
                                                (guiModel, "**/Fire_Btn_DN"),
                                                (guiModel, "**/Fire_Btn_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (0.0115741,0,0.00505051),
                                       scale = 1.,
                                       command = self.__firePressed,
                                       )
        self.upButton = DirectButton(parent = self.aimPad,
                                     image = ((guiModel, "**/Cannon_Arrow_UP"),
                                              (guiModel, "**/Cannon_Arrow_DN"),
                                              (guiModel, "**/Cannon_Arrow_RLVR"),
                                              ),
                                     relief = None,
                                     pos = (0.0115741,0,0.221717),
                                     )
        self.downButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                (guiModel, "**/Cannon_Arrow_DN"),
                                                (guiModel, "**/Cannon_Arrow_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (0.0136112,0,-0.210101),
                                       image_hpr = (0,0,180),
                                       )
        self.leftButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                (guiModel, "**/Cannon_Arrow_DN"),
                                                (guiModel, "**/Cannon_Arrow_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (-0.199352,0,-0.000505269),
                                       image_hpr = (0,0,-90),
                                       )
        self.rightButton = DirectButton(parent = self.aimPad,
                                        image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                 (guiModel, "**/Cannon_Arrow_DN"),
                                                 (guiModel, "**/Cannon_Arrow_RLVR"),
                                                 ),
                                        relief = None,
                                        pos = (0.219167,0,-0.00101024),
                                        image_hpr = (0,0,90),
                                        )

        # set alpha on aim interface
        self.aimPad.setColor(1,1,1,0.9)

        # set up the button press/release handlers
        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler=upHandler : handler())
            button.bind(DGG.B1RELEASE, lambda x, handler=downHandler : handler())
        bindButton(self.upButton, self.__upPressed, self.__upReleased)
        bindButton(self.downButton, self.__downPressed, self.__downReleased)
        bindButton(self.leftButton, self.__leftPressed, self.__leftReleased)
        bindButton(self.rightButton, self.__rightPressed, self.__rightReleased)

        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.hide()

        self.DEBUG_TOWER_RANGE = 0
        # each of these flags imply the states of their opposites
        # (LEFT == !RIGHT, NEAR == !FAR)
        self.DEBUG_CANNON_FAR_LEFT = 0
        self.DEBUG_TOWER_NEAR = 1
        self.DEBUG_TOWER_FAR_LEFT = 1

        if __debug__:
            # this flag will show whether or not you'll win if you shoot
            # with the current cannon orientation
            self.cheat = config.GetBool('cannon-game-cheat', 0)
            
    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        self.sky.removeNode()
        del self.sky

        # No ground
        self.ground.removeNode()
        del self.ground

        # get rid of tower
        self.tower.removeNode()
        del self.tower

        # get rid of original cannon model
        self.cannon.removeNode()
        del self.cannon

        # get rid of the references to the drop shadow
        del self.dropShadowDict

        # get rid of original dropshadow model
        self.dropShadow.removeNode()
        del self.dropShadow

        # get rid of the splash
        self.splash.destroy()
        del self.splash

        # get rid of the dust cloud
        self.dustCloud.destroy()
        del self.dustCloud

        # delete the hill
        self.hill.removeNode()
        del self.hill

        self.rewardPanel.destroy()
        del self.rewardPanel
        self.jarImage.removeNode()
        del self.jarImage
        
        # Get rid of audio
        del self.music
        del self.sndCannonMove
        del self.sndCannonFire
        del self.sndHitGround
        del self.sndHitTower
        del self.sndHitWater
        del self.sndWhizz
        del self.sndWin
        del self.sndRewardTick

        # kill GUI
        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton

        # make sure the blink and lookaround tasks are cleaned up
        for avId in self.toonHeadDict.keys():
            head = self.toonHeadDict[avId]
            head.stopBlink()
            head.stopLookAroundNow()
            av = self.getAvatar(avId)
            if av:
                # Reset anim an run play rate
                av.loop('neutral')
                av.setPlayRate(1.0, 'run')
                av.nametag.removeNametag(head.tag)
            head.delete()
        del self.toonHeadDict
        for model in self.toonModelDict.values():
            model.removeNode()
        del self.toonModelDict
        del self.toonScaleDict
        for interval in self.toonIntervalDict.values():
            interval.finish()
        del self.toonIntervalDict

        # get rid of the cannons
        for avId in self.avIdList:
            self.cannonDict[avId][0].removeNode()
            del self.cannonDict[avId][0]
        del self.cannonDict

        # Goodbye timer
        self.timer.destroy()
        del self.timer

        del self.cannonLocationDict

        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)

        # show everything
        self.__createCannons()
        for avId in self.avIdList:
            self.cannonDict[avId][0].reparentTo(render)

        # generate a random position for the tower
        # (this will gen the same position on all clients)
        self.towerPos = self.getTowerPosition()
        self.tower.setPos(self.towerPos)
        self.tower.reparentTo(render)

        self.sky.reparentTo(render)

        self.ground.reparentTo(render)

        self.hill.setPosHpr(0, CANNON_Y + 2.33, 0, 0, 0, 0)
        self.hill.reparentTo(render)

        self.splash.reparentTo(render)
        self.dustCloud.reparentTo(render)

        # load up the local toon
        self.__createToonModels(self.localAvId)

        camera.reparentTo(render)
        self.__oldCamFar = base.camLens.getFar()
        base.camLens.setFar(FAR_PLANE_DIST)

        self.__startIntro()

        # Iris in
        base.transitions.irisIn(0.4)

        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.8)

    def offstage(self):
        self.notify.debug("offstage")
        self.sky.reparentTo(hidden)
        self.ground.reparentTo(hidden)
        self.hill.reparentTo(hidden)
        self.tower.reparentTo(hidden)
        for avId in self.avIdList:
            self.cannonDict[avId][0].reparentTo(hidden)
            # this dict may not have been filled in
            if self.dropShadowDict.has_key(avId):
                self.dropShadowDict[avId].reparentTo(hidden)

            av = self.getAvatar(avId)
            if av:
                # show the dropshadow again
                av.dropShadow.show()
                # restore the LODs
                av.resetLOD()
        self.splash.reparentTo(hidden)
        self.splash.stop()
        self.dustCloud.reparentTo(hidden)
        self.dustCloud.stop()
        self.__stopIntro()
        base.camLens.setFar(self.__oldCamFar)
        self.timer.reparentTo(hidden)
        self.rewardPanel.reparentTo(hidden)
        DistributedMinigame.offstage(self)

    def getTowerPosition(self):
        """
        Calculate a position for the tower
        This will produce the same result on all clients
        The tower position is chosen from an area shaped roughly
        like the one shown below:

        -------
        \     /  <-- area
         \   /
          ---

        | | | |  <-- cannons

        PHeAr mY MaD @$cii 4rt 5K1LlZ, j0
        """
        # come up with a tower position in a trapezoidal area that is
        # narrow close to the cannons and wide away from them
        yRange = TOWER_Y_RANGE
        # choose a number from yRange*0.3 to yRange
        # don't use the front 1/3 or so of the triangle, it's
        # too close to the cannons
        yMin = yRange * .3
        yMax = yRange
        if self.DEBUG_TOWER_RANGE:
            if self.DEBUG_TOWER_NEAR:
                y = yMin
            else:
                y = yMax
        else:
            y = self.randomNumGen.randint(yMin, yMax)

        xRange = TOWER_X_RANGE
        if self.DEBUG_TOWER_RANGE:
            if self.DEBUG_TOWER_FAR_LEFT:
                x = 0
            else:
                x = xRange
        else:
            x = self.randomNumGen.randint(0, xRange)
        # center x around zero
        x = x - int(xRange / 2.)

        ### DIFFICULTY ###
        if base.wantMinigameDifficulty:
            # pull the tower towards the center, according to the difficulty
            # level; it's easier to hit the tower when it's in the center
            diff = self.getDifficulty()
            # scale is .5 to 1
            scale = .5 + (.5 * diff)
            # x is centered around zero already; just scale it
            x *= scale
            # y is not centered around zero; pull y towards the average
            # of yMin and yMax
            yCenter = (yMin + yMax) / 2.
            y = ((y - yCenter) * scale) + yCenter

        # scale x according to y, so the x range is smaller closer
        # to the cannons; this creates the trapezoid shape
        x = float(x) * (float(y) / float(yRange))
        # center y around zero
        y = y - int(yRange / 2.)

        self.notify.debug("getTowerPosition: " + str(x) + ", " + str(y))
        return Point3(x, y, 0.)

    def __createCannons(self):
        # create the cannons
        for avId in self.avIdList:
            cannon = self.cannon.copyTo(hidden)
            barrel = cannon.find("**/cannon")
            self.cannonDict[avId] = [cannon, barrel]

        # place the cannons in their starting positions
        numAvs = self.numPlayers
        for i in range(numAvs):
            avId = self.avIdList[i]

            # init the cannon location
            self.cannonLocationDict[avId] =\
                 Point3((i * CANNON_X_SPACING) -
                        (((numAvs-1) * CANNON_X_SPACING)/2),
                        CANNON_Y, CANNON_Z)
            if self.DEBUG_TOWER_RANGE:
                if self.DEBUG_CANNON_FAR_LEFT:
                    self.cannonLocationDict[avId] =\
                         Point3((0 * CANNON_X_SPACING) -
                                (((4-1) * CANNON_X_SPACING)/2),
                                CANNON_Y, CANNON_Z)
                else:
                    self.cannonLocationDict[avId] =\
                         Point3((3 * CANNON_X_SPACING) -
                                (((4-1) * CANNON_X_SPACING)/2),
                                CANNON_Y, CANNON_Z)

            # init the cannon position
            self.cannonPositionDict[avId] = [0,
                                             CannonGameGlobals.CANNON_ANGLE_MIN]
            self.cannonDict[avId][0].setPos(self.cannonLocationDict[avId])
            self.__updateCannonPosition(avId)


    # generic minigame distributed functions
    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return

        # create the models for the other toons
        for avId in self.avIdList:
            if avId != self.localAvId:
                self.__createToonModels(avId)

    def __createToonModels(self, avId):
        # create the toon model
        toon = self.getAvatar(avId)
        # store the toon's original scale
        self.toonScaleDict[avId] = toon.getScale()
        # force use of highest LOD
        toon.useLOD(1000)
        # stick the toon under an additional node
        # in order to move the toon's local origin to its waist
        toonParent = render.attachNewNode("toonOriginChange")
        toon.reparentTo(toonParent)
        toon.setPosHpr(0,0,-(toon.getHeight()/2.),0,0,0)
        self.toonModelDict[avId] = toonParent

        # create the toon head
        head = ToonHead.ToonHead()
        head.setupHead(self.getAvatar(avId).style)
        head.reparentTo(hidden)
        self.toonHeadDict[avId] = head

        # attach a chat balloon to the toonhead
        toon = self.getAvatar(avId)
        tag = NametagFloat3d()
        tag.setContents(Nametag.CSpeech | Nametag.CThought)
        tag.setBillboardOffset(0)
        tag.setAvatar(head)
        toon.nametag.addNametag(tag)

        tagPath = head.attachNewNode(tag.upcastToPandaNode())
        tagPath.setPos(0, 0, 1)
        head.tag = tag

        # stuff the toon into his cannon
        self.__loadToonInCannon(avId)

        # hide the avatar's dropshadow
        self.getAvatar(avId).dropShadow.hide()

        # create a copy of the drop shadow
        self.dropShadowDict[avId] = self.dropShadow.copyTo(hidden)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)

        self.__stopIntro()

        # place the camera behind our cannon
        self.__putCameraBehindCannon()

        if not base.config.GetBool('endless-cannon-game', 0):
            # Start counting down the game clock,
            # call __gameTimerExpired when it reaches 0
            self.timer.show()
            self.timer.countdown(CannonGameGlobals.GameTime,
                                 self.__gameTimerExpired)

        self.rewardPanel.reparentTo(aspect2d)
        self.scoreMult = MinigameGlobals.getScoreMult(self.cr.playGame.hood.id)
        self.__startRewardCountdown()

        self.airborneToons = 0
        self.clockStopTime = None

        self.gameFSM.request('aim')

    def __gameTimerExpired(self):
        self.notify.debug("game timer expired")

        # finish the game
        self.gameOver()

    # cannon game-specific distributed functions
    def __playing(self):
        return (self.gameFSM.getCurrentState() !=
                self.gameFSM.getFinalState())
        
    def updateCannonPosition(self, avId, zRot, angle):
        if not self.hasLocalToon: return
        # if the game is already over, ignore this message
        if not self.__playing(): return

        # the server is telling us that a cannon has moved (rotated)
        #self.notify.debug("updateCannonPosition: " + str(avId) + \
        #                  ": zRot=" + str(zRot) + ", angle=" + str(angle))
        if avId != self.localAvId:
            self.cannonPositionDict[avId] = [zRot, angle]
            self.__updateCannonPosition(avId)

    def setCannonWillFire(self, avId, fireTime, zRot, angle):
        if not self.hasLocalToon: return
        # if the game is already over, ignore this message
        if not self.__playing(): return

        # the server is telling us that a cannon will fire at a specific time
        self.notify.debug("setCannonWillFire: " + str(avId)
                          + ": zRot=" + str(zRot) + ", angle=" + str(angle)
                          + ", time=" + str(fireTime))

        # set the cannon's position
        # NOTE: do this for the local toon; cannon angles may have been
        # modified by conversion to and from fixed-point, and we want
        # to have the same values that all the other clients have
        self.cannonPositionDict[avId][0] = zRot
        self.cannonPositionDict[avId][1] = angle
        self.__updateCannonPosition(avId)

        # create a task to fire off the cannon
        task = Task(self.__fireCannonTask)
        task.avId = avId

        # fireTime is in game time
        task.fireTime = fireTime

        timeToWait = task.fireTime - self.getCurrentGameTime()

        # create a task sequence (or not)
        if timeToWait > 0.:
            fireTask = Task.sequence(Task.pause(timeToWait),
                                     task)
        else:
            fireTask = task

        fireTask = task

        taskMgr.add(fireTask, "fireCannon" + str(avId))

        # bump up the number of toons that are 'airborne' (or will be soon)
        self.airborneToons += 1

    def announceToonWillLandInWater(self, avId, landTime):
        if not self.hasLocalToon: return
        # the server is telling us that a toon is going to land
        # in the water at a specific time.
        self.notify.debug("announceToonWillLandInWater: " + str(avId)
                          + ": time=" + str(landTime))

        if self.clockStopTime == None:
            self.clockStopTime = landTime

    # ClassicFSM functions
    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterAim(self):
        self.notify.debug("enterAim")
        self.__enableAimInterface()
        self.__putCameraBehindCannon()

    def exitAim(self):
        self.__disableAimInterface()

    def enterShoot(self):
        self.notify.debug("enterShoot")
        # make sure everyone has the correct position
        self.__broadcastLocalCannonPosition()

        # send the 'cannon lit' message and wait for the server
        # to tell us the time that our cannon will shoot
        self.sendUpdate("setCannonLit",
                        [self.cannonPositionDict[self.localAvId][0],
                         self.cannonPositionDict[self.localAvId][1]])

    def exitShoot(self):
        pass

    def __somebodyWon(self, avId):
        """__somebodyWon(self, avId)
        called when somebody lands in the water
        the avId could be the localToon
        """
        if avId == self.localAvId:
            base.playSfx(self.sndWin)
        # stop the timers
        self.__killRewardCountdown()
        self.timer.stop()
        self.gameFSM.request('waitForToonsToLand')

    def enterWaitForToonsToLand(self):
        self.notify.debug("enterWaitForToonsToLand")
        # there may still be toons in the air
        # if there are airborne toons, gameOver will be called when they
        # have all landed.
        # otherwise, just call gameOver now
        if not self.airborneToons:
            self.gameOver()

    def exitWaitForToonsToLand(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        # Stop music
        self.music.stop()

        self.__killRewardCountdown()
        if hasattr(self, 'jarIval'):
            self.jarIval.finish()
            del self.jarIval

        for avId in self.avIdList:
            # get rid of any tasks that may linger
            taskMgr.remove("fireCannon" + str(avId))
            taskMgr.remove("flyingToon" + str(avId))

    def exitCleanup(self):
        pass

    # UI crep
    def __enableAimInterface(self):
        self.aimPad.show()

        # listen for key presses
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)

        # start the local cannon move task
        self.__spawnLocalCannonMoveTask()

    def __disableAimInterface(self):
        self.aimPad.hide()

        self.ignore(self.FIRE_KEY)
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        self.ignore(self.FIRE_KEY + "-up")
        self.ignore(self.UP_KEY + "-up")
        self.ignore(self.DOWN_KEY + "-up")
        self.ignore(self.LEFT_KEY + "-up")
        self.ignore(self.RIGHT_KEY + "-up")

        # kill the local cannon move task
        self.__killLocalCannonMoveTask()

    # keypress handlers
    def __fireKeyPressed(self):
        self.ignore(self.FIRE_KEY)
        self.accept(self.FIRE_KEY+"-up", self.__fireKeyReleased)
        self.__firePressed()

    def __upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY+"-up", self.__upKeyReleased)
        self.__upPressed()

    def __downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY+"-up", self.__downKeyReleased)
        self.__downPressed()

    def __leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY+"-up", self.__leftKeyReleased)
        self.__leftPressed()

    def __rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY+"-up", self.__rightKeyReleased)
        self.__rightPressed()

    def __fireKeyReleased(self):
        self.ignore(self.FIRE_KEY+"-up")
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.__fireReleased()

    def __leftKeyReleased(self):
        self.ignore(self.LEFT_KEY+"-up")
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.__leftReleased()

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY+"-up")
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.__rightReleased()

    def __upKeyReleased(self):
        self.ignore(self.UP_KEY+"-up")
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upReleased()

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY+"-up")
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.__downReleased()

    # button event handlers (also used by keyboard event handlers)
    def __firePressed(self):
        self.notify.debug("fire pressed")
        self.gameFSM.request('shoot')

    def __upPressed(self):
        self.notify.debug("up pressed")
        self.upPressed = self.__enterControlActive(self.upPressed)

    def __downPressed(self):
        self.notify.debug("down pressed")
        self.downPressed = self.__enterControlActive(self.downPressed)

    def __leftPressed(self):
        self.notify.debug("left pressed")
        self.leftPressed = self.__enterControlActive(self.leftPressed)

    def __rightPressed(self):
        self.notify.debug("right pressed")
        self.rightPressed = self.__enterControlActive(self.rightPressed)

    def __upReleased(self):
        self.notify.debug("up released")
        self.upPressed = self.__exitControlActive(self.upPressed)

    def __downReleased(self):
        self.notify.debug("down released")
        self.downPressed = self.__exitControlActive(self.downPressed)

    def __leftReleased(self):
        self.notify.debug("left released")
        self.leftPressed = self.__exitControlActive(self.leftPressed)

    def __rightReleased(self):
        self.notify.debug("right released")
        self.rightPressed = self.__exitControlActive(self.rightPressed)


    # __enterControlActive and __exitControlActive are used
    # to update the cannon control 'press reference counts'
    # leftPressed, rightPressed, upPressed, and downPressed
    # are all counts of how many devices (button, keys) are
    # activating that particular cannon control -- so if
    # someone is pressing 'right' on the keyboard and also
    # pressing on the 'right' button with the mouse,
    # rightPressed would be set to 2. A value of zero means
    # that the cannon control is inactive.
    def __enterControlActive(self, control):
        return control + 1

    def __exitControlActive(self, control):
        return max(0, control-1)


    if __debug__:
        ###################
        # CHEAT: shows you whether you'll win if you fire with the
        # current cannon orientation
        def __doCheat(self):
            if self.cheat:
                # prevent tons of log spam
                savedDebug = self.notify.debug
                def fakeDebug(str):
                    pass
                self.notify.debug = fakeDebug
                results = self.__calcFlightResults(self.localAvId, 0)
                self.notify.debug = savedDebug
                if results['hitWhat'] == self.HIT_WATER:
                    self.aimPad.setColor(.5,.5,.5,1)
                else:
                    self.aimPad.setColor(1,1,1,1)

        def __clearCheat(self):
            self.aimPad.setColor(1,1,1,1)
        ###################

    def __spawnLocalCannonMoveTask(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0

        self.cannonMoving = 0

        task = Task(self.__localCannonMoveTask)
        task.lastPositionBroadcastTime = 0.
        taskMgr.add(task, self.LOCAL_CANNON_MOVE_TASK)

    def __killLocalCannonMoveTask(self):
        taskMgr.remove(self.LOCAL_CANNON_MOVE_TASK)
        if self.cannonMoving:
            self.sndCannonMove.stop()
            if __debug__:
                self.__clearCheat()

    def __localCannonMoveTask(self, task):
        """ this task moves the cannon
        """
        pos = self.cannonPositionDict[self.localAvId]

        # these are used to determine if the cannon actually moved
        oldRot = pos[0]
        oldAng = pos[1]

        # cannon rotation
        rotVel = 0
        if self.leftPressed:
            rotVel += CannonGameGlobals.CANNON_ROTATION_VEL
        if self.rightPressed:
            rotVel -= CannonGameGlobals.CANNON_ROTATION_VEL
        pos[0] += rotVel * globalClock.getDt()
        if pos[0] < CannonGameGlobals.CANNON_ROTATION_MIN:
            pos[0] = CannonGameGlobals.CANNON_ROTATION_MIN
        elif pos[0] > CannonGameGlobals.CANNON_ROTATION_MAX:
            pos[0] = CannonGameGlobals.CANNON_ROTATION_MAX

        # cannon barrel angle
        angVel = 0
        if self.upPressed:
            angVel += CannonGameGlobals.CANNON_ANGLE_VEL
        if self.downPressed:
            angVel -= CannonGameGlobals.CANNON_ANGLE_VEL
        pos[1] += angVel * globalClock.getDt()
        if pos[1] < CannonGameGlobals.CANNON_ANGLE_MIN:
            pos[1] = CannonGameGlobals.CANNON_ANGLE_MIN
        elif pos[1] > CannonGameGlobals.CANNON_ANGLE_MAX:
            pos[1] = CannonGameGlobals.CANNON_ANGLE_MAX

        if oldRot != pos[0] or oldAng != pos[1]:
            if self.cannonMoving == 0:
                self.cannonMoving = 1
                base.playSfx(self.sndCannonMove, looping=1)

            self.__updateCannonPosition(self.localAvId)

            # periodically send a position update broadcast
            if task.time - task.lastPositionBroadcastTime > \
                                         CANNON_MOVE_UPDATE_FREQ:
                task.lastPositionBroadcastTime = task.time
                self.__broadcastLocalCannonPosition()
        else:
            if self.cannonMoving:
                self.cannonMoving = 0
                self.sndCannonMove.stop()
                # make sure everyone has the correct final position
                self.__broadcastLocalCannonPosition()

        if __debug__:
            self.__doCheat()

        return Task.cont


    def __broadcastLocalCannonPosition(self):
        # send a position update for the local cannon
        self.sendUpdate("setCannonPosition",
                        [self.cannonPositionDict[self.localAvId][0],
                         self.cannonPositionDict[self.localAvId][1]])

    def __updateCannonPosition(self, avId):
        self.cannonDict[avId][0].setHpr(\
                             self.cannonPositionDict[avId][0], 0., 0.)
        self.cannonDict[avId][1].setHpr(\
                             0., self.cannonPositionDict[avId][1], 0.)

    def __getCameraPositionBehindCannon(self):
        return Point3(self.cannonLocationDict[self.localAvId][0],
                      CANNON_Y - 25.0, CANNON_Z + 7)

    def __putCameraBehindCannon(self):
        # place the camera behind our cannon
        camera.setPos(self.__getCameraPositionBehindCannon())
        camera.setHpr(0, 0, 0)

    def __loadToonInCannon(self, avId):
        # hide the full toon model
        self.toonModelDict[avId].detachNode()
        # show the toon head
        head = self.toonHeadDict[avId]
        head.startBlink()
        head.startLookAround()
        # parent head to the cannon barrel
        head.reparentTo(self.cannonDict[avId][1])
        # put it up at the muzzle of the cannon, facing down
        head.setPosHpr(0,6,0,0,-45,0)
        # restore proper scale (wrt render)
        sc = self.toonScaleDict[avId]
        head.setScale(render, sc[0], sc[1], sc[2])

    def __toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def __toDegrees(self, angle):
        return angle * 360.0 / (2.0 * math.pi)

    def __calcFlightResults(self, avId, launchTime):
        """
        returns dict with keys:
        startPos, startHpr, startVel, trajectory, timeOfImpact, hitWhat
        """
        head = self.toonHeadDict[avId]
        startPos = head.getPos(render)
        startHpr = head.getHpr(render)

        # get the cannon's orientation relative to render
        hpr = self.cannonDict[avId][1].getHpr(render)

        # get the tower's position relative to render
        towerPos = self.tower.getPos(render)

        # calc the initial velocity in render space
        rotation = self.__toRadians(hpr[0])
        angle = self.__toRadians(hpr[1])
        horizVel = INITIAL_VELOCITY * math.cos(angle)
        xVel = horizVel * -math.sin(rotation)
        yVel = horizVel * math.cos(rotation)
        zVel = INITIAL_VELOCITY * math.sin(angle)
        startVel = Vec3(xVel, yVel, zVel)

        trajectory = Trajectory.Trajectory(launchTime, startPos, startVel)

        towerList = [towerPos + Point3(0, 0, BUCKET_HEIGHT),
                     TOWER_RADIUS, TOWER_HEIGHT - BUCKET_HEIGHT]

        self.notify.debug('calcFlightResults(%s): rotation(%s), angle(%s), '
                          'horizVel(%s), xVel(%s), yVel(%s), zVel(%s), '
                          'startVel(%s), trajectory(%s), towerList(%s)' %
                          (avId, rotation, angle, horizVel, xVel, yVel, zVel,
                           startVel, trajectory, towerList))

        # figure out what will be hit, and when
        timeOfImpact, hitWhat = self.__calcToonImpact(trajectory, towerList)

        return {
            'startPos' : startPos,
            'startHpr' : startHpr,
            'startVel' : startVel,
            'trajectory' : trajectory,
            'timeOfImpact' : timeOfImpact,
            'hitWhat' : hitWhat,
            }

    def __fireCannonTask(self, task):
        """
        spawn a task sequence to shoot the cannon, fly
        the avatar through the air, handle the toon's landing
        """
        launchTime = task.fireTime
        avId = task.avId

        self.notify.debug("FIRING CANNON FOR AVATAR " + str(avId))

        # calculate the trajectory
        flightResults = self.__calcFlightResults(avId, launchTime)
        # pull all the results into the local namespace
        for key in flightResults:
            exec "%s = flightResults['%s']" % (key, key)

        self.notify.debug("start position: " + str(startPos))
        self.notify.debug("start velocity: " + str(startVel))
        self.notify.debug("time of launch: " + str(launchTime))
        self.notify.debug("time of impact: " + str(timeOfImpact))
        self.notify.debug("location of impact: " +
                          str(trajectory.getPos(timeOfImpact)))
        if hitWhat == self.HIT_WATER:
            self.notify.debug("toon will land in the water")
        elif hitWhat == self.HIT_TOWER:
            self.notify.debug("toon will hit the tower")
        else:
            self.notify.debug("toon will hit the ground")

        # get the toon out of the cannon
        # hide the toon's head
        head = self.toonHeadDict[avId]
        head.stopBlink()
        head.stopLookAroundNow()
        head.reparentTo(hidden)
        # show the whole body, posbang it to where the
        # head was
        av = self.toonModelDict[avId]
        av.reparentTo(render)
        av.setPos(startPos)
        av.setHpr(startHpr)
        avatar = self.getAvatar(avId)
        avatar.loop('swim')
        avatar.setPosHpr(0,0,-(avatar.getHeight()/2.),0,0,0)

        # create the tasks
        shootTask = Task(self.__shootTask)
        flyTask = Task(self.__flyTask)
        seqDoneTask = Task(self.__flySequenceDoneTask)

        # stock the tasks up with the info they need
        # store the info in a shared dictionary
        info = {}
        info['avId'] = avId
        info['trajectory'] = trajectory
        info['launchTime'] = launchTime
        info['timeOfImpact'] = timeOfImpact
        info['hitWhat'] = hitWhat
        info['toon'] = self.toonModelDict[avId]
        info['hRot'] = self.cannonPositionDict[avId][0]
        info['haveWhistled'] = 0
        info['maxCamPullback'] = CAMERA_PULLBACK_MIN
        info['timeEnterTowerXY'], info['timeExitTowerXY'] =\
                trajectory.calcEnterAndLeaveCylinderXY(
                    self.tower.getPos(render), TOWER_RADIUS)

        # put the info dict on each task
        shootTask.info = info
        flyTask.info = info
        seqDoneTask.info = info

        # create the task sequence
        seqTask = Task.sequence(shootTask,
                                flyTask,
                                Task.pause(LAND_TIME),
                                seqDoneTask)

        # spawn the new task
        taskMgr.add(seqTask, 'flyingToon' + str(avId))

        # if this is the local toon and we will land in the water,
        # let the server know
        if avId == self.localAvId:
            if info['hitWhat'] == self.HIT_WATER:
                self.sendUpdate("setToonWillLandInWater",
                                [info['timeOfImpact']])

        return Task.done

    def __calcToonImpact(self, trajectory, waterTower):
        """__calcToonImpact(self, waterTower)
        calculate the result of the toon's trajectory
        check if the toon will land in the water, hit the tower, or hit
        the ground
        waterTower is a list with members [center of tower base (Point3),
                                           tower radius, tower height]
        water tower is represented as a cylinder
        returns time of impact, what toon hits
        """

        self.notify.debug("trajectory: %s" % trajectory)
        self.notify.debug("waterTower: %s" % waterTower)

        waterDiscCenter = Point3(waterTower[0]) # center of tower base --
                                                # be sure to make a
                                                # separate copy
        waterDiscCenter.setZ(waterDiscCenter[2] + waterTower[2]) # center of
                                                                 # tower top
        t_waterImpact = trajectory.checkCollisionWithDisc(waterDiscCenter,
                                                          waterTower[1])
        self.notify.debug('t_waterImpact: %s' % t_waterImpact)
        if t_waterImpact > 0:
            # toon will land in the water
            return t_waterImpact, self.HIT_WATER

        # will the toon hit the tower?
        t_towerImpact = trajectory.checkCollisionWithCylinderSides(
            waterTower[0], waterTower[1], waterTower[2])
        self.notify.debug('t_towerImpact: %s' % t_towerImpact)
        if t_towerImpact > 0:
            # toon will hit the tower
            return t_towerImpact, self.HIT_TOWER

        #calculate when the toon will hit the ground
        t_groundImpact = trajectory.checkCollisionWithGround()
        self.notify.debug('t_groundImpact: %s' % t_groundImpact)
        if t_groundImpact >= trajectory.getStartTime():
            # toon will hit the ground (...he'd best...)
            return t_groundImpact, self.HIT_GROUND
        else:
            # toon won't hit the ground??
            self.notify.error("__calcToonImpact: toon never impacts ground?")
            # return something
            return self.startTime, self.HIT_GROUND

    def __shootTask(self, task):
        base.playSfx(self.sndCannonFire)

        # show the drop shadow
        self.dropShadowDict[task.info['avId']].reparentTo(render)

        return Task.done


    def __flyTask(self, task):
        curTime = task.time + task.info['launchTime']
        # don't overshoot past the time of landing
        t = min(curTime, task.info['timeOfImpact'])

        # get position
        pos = task.info['trajectory'].getPos(t)

        # update toon position
        task.info['toon'].setPos(pos)

        # update drop shadow position
        shadowPos = Point3(pos)
        # if over the tower, raise the shadow up so it's just over the water
        if t >= task.info['timeEnterTowerXY'] and \
           t <= task.info['timeExitTowerXY'] and \
           pos[2] >= (self.tower.getPos(render)[2] + TOWER_HEIGHT):
            shadowPos.setZ(self.tower.getPos(render)[2] +
                           TOWER_HEIGHT + SHADOW_Z_OFFSET)
        else:
            shadowPos.setZ(SHADOW_Z_OFFSET)
        self.dropShadowDict[task.info['avId']].setPos(shadowPos)

        # set the toon's tilt based on its velocity
        # h rotation is constant, and corresponds to the cannon's
        # z rotation (left to right)
        vel = task.info['trajectory'].getVel(t)
        run = math.sqrt((vel[0] * vel[0]) + (vel[1] * vel[1])) # TODO:
                                                               #precompute this
        rise = vel[2]
        theta = self.__toDegrees(math.atan(rise/run))
        task.info['toon'].setHpr(task.info['hRot'],-90 + theta,0)

        # if local toon, update camera position
        if task.info['avId'] == self.localAvId:
            lookAt = self.tower.getPos(render)
            lookAt.setZ(lookAt.getZ() - (TOWER_HEIGHT/2.0))

            # calc distance from toon to tower [in X,Y plane]
            towerPos = Point3(self.towerPos)
            towerPos.setZ(TOWER_HEIGHT)
            ttVec = Vec3(pos - towerPos)
            toonTowerDist = ttVec.length()

            multiplier = 0.

            # are we close enough to the tower to warrant a change
            # in the lookat point?
            if toonTowerDist < TOON_TOWER_THRESHOLD:
                # get a unit vector that is horizontally perpendicular
                # to the toon's flight path
                up = Vec3(0., 0., 1.)
                perp = up.cross(vel)
                perp.normalize()

                # do some dot-prod voodoo to make sure the sign of the
                # unit vector is correct
                if ttVec.dot(perp) > 0.:
                    perp = Vec3(-perp[0], -perp[1], -perp[2])

                a = 1. - (toonTowerDist / TOON_TOWER_THRESHOLD)
                a_2 = a * a
                multiplier = (-2. * a_2 * a) + (3 * a_2)

                # move the lookat away from the tower, along the
                # perpendicular direction, with a distance inversely
                # proportional to the distance from the toon to the
                # tower
                lookAt = lookAt + \
                         (perp * (multiplier * MAX_LOOKAT_OFFSET))

            # get a vector pointing from tower to toon
            foo = Vec3(pos - lookAt)
            foo.normalize()
            task.info['maxCamPullback'] = max(
                task.info['maxCamPullback'],
                (CAMERA_PULLBACK_MIN +
                 (multiplier *
                  (CAMERA_PULLBACK_MAX - CAMERA_PULLBACK_MIN))))
            foo = foo * task.info['maxCamPullback']
            camPos = pos + Point3(foo)
            camera.setPos(camPos)
            camera.lookAt(pos)


        # should we play the whistling noise?
        if task.info['haveWhistled'] == 0:
            if -vel[2] > WHISTLE_SPEED:
                if t < (task.info['timeOfImpact'] - 0.5):
                    task.info['haveWhistled'] = 1
                    base.playSfx(self.sndWhizz)

        # have we landed yet?
        if t == task.info['timeOfImpact']:
            # stop the whistling sound
            if task.info['haveWhistled']:
                self.sndWhizz.stop()

            # hide the drop shadow
            self.dropShadowDict[task.info['avId']].reparentTo(hidden)

            # where did we land?
            avatar = self.getAvatar(task.info['avId'])
            if task.info['hitWhat'] == self.HIT_WATER:
                # we landed in the water
                avatar.loop('neutral')
                # Show a splash
                self.splash.setPos(task.info['toon'].getPos())
                self.splash.setScale(2)
                self.splash.play()
                # Play the splash sound
                base.playSfx(self.sndHitWater)
                # stand the toon upright
                task.info['toon'].setHpr(task.info['hRot'],0,0)
                self.__somebodyWon(task.info['avId'])
            elif task.info['hitWhat'] == self.HIT_TOWER:
                # we hit the tower
                toon = task.info['toon']
                # Compute vector from tower center to toon
                pos = toon.getPos()
                ttVec = Vec3(pos - self.towerPos)
                ttVec.setZ(0)
                ttVec.normalize()
                # Calc angle to get toon lying flat on water tower surface
                h = rad2Deg(math.asin(ttVec[0]))
                toon.setHpr(h,94,0)
                # Offset toon pos to account for sloped bucket walls
                deltaZ = TOWER_HEIGHT-BUCKET_HEIGHT
                sf = min(max(pos[2] - BUCKET_HEIGHT, 0),deltaZ)/deltaZ
                hitPos = pos + Point3(ttVec * (0.75 * sf))
                toon.setPos(hitPos)
                hitPos.setZ(hitPos[2] - 1.0)
                # A small interval to slide toon down the side of the bucket
                s = Sequence(Wait(0.5),
                             toon.posInterval(duration = LAND_TIME - 0.5,
                                              pos = hitPos, blendType = 'easeIn'))
                self.toonIntervalDict[task.info['avId']] = s
                s.start()
                # But clear out avatar offset
                avatar.iPos()
                # Put toon in 'splat' pose
                avatar.pose('slip-forward', 25)
                base.playSfx(self.sndHitTower)
            elif task.info['hitWhat'] == self.HIT_GROUND:
                task.info['toon'].setP(render, -150.0)
                self.dustCloud.setPos(task.info['toon'], 0, 0, -2.5)
                self.dustCloud.setScale(0.35)
                self.dustCloud.play()
                base.playSfx(self.sndHitGround)
                # Make him wiggle his legs                
                avatar.setPlayRate(2.0, 'run')
                avatar.loop("run")
            return Task.done

        return Task.cont

    def __flySequenceDoneTask(self, task):
        # this toon just landed; there's one less toon in the air
        self.airborneToons -= 1

        if self.gameFSM.getCurrentState().getName() == 'waitForToonsToLand':
            # somebody has won
            # if there are no other airborne toons, game is over
            if 0 == self.airborneToons:
                self.gameOver()
        else:
            # game is still in progress
            # stuff the toon back into the cannon
            self.__loadToonInCannon(task.info['avId'])
            # transition back to aim state if local toon
            if task.info['avId'] == self.localAvId:
                self.gameFSM.request('aim')

        return Task.done

    def __startRewardCountdown(self):
        taskMgr.remove(self.REWARD_COUNTDOWN_TASK)
        taskMgr.add(self.__updateRewardCountdown, self.REWARD_COUNTDOWN_TASK)

    def __killRewardCountdown(self):
        taskMgr.remove(self.REWARD_COUNTDOWN_TASK)

    def __updateRewardCountdown(self, task):
        # Reward panel was never created, game ended before it even began.
        if not hasattr(self, 'rewardPanel'):
            return Task.cont
    
        curTime = self.getCurrentGameTime()

        # if it's time for the clock to stop, stop it
        if self.clockStopTime is not None:
            if self.clockStopTime < curTime:
                self.__killRewardCountdown()
                # force the jbean jar to the clockStopTime, so that
                # we show the same number of jbeans that we'll see
                # in the reward screen
                curTime = self.clockStopTime
            
        # if this is the first time through, init the task's
        # record of the score
        score = int(self.scoreMult * CannonGameGlobals.calcScore(curTime)+.5)
        if not hasattr(task, 'curScore'):
            task.curScore = score

        self.rewardPanel['text'] = str(score)

        if task.curScore != score:
            if hasattr(self, 'jarIval'):
                self.jarIval.finish()

            # make the jar animate
            s = self.rewardPanel.getScale()
            self.jarIval = Parallel(\
                Sequence(self.rewardPanel.scaleInterval(.15, s*3./4.,
                                                        blendType='easeOut'),
                         self.rewardPanel.scaleInterval(.15, s,
                                                        blendType='easeIn'),
                         ),
                SoundInterval(self.sndRewardTick),
                name='cannonGameRewardJarThrob')
            self.jarIval.start()

        task.curScore = score

        return Task.cont

    #######################################################################
    # intro fly-by stuff
    #######################################################################

    # So here's the deal with this intro fly-by thing. The view from behind
    # the cannon is a little confusing. You're looking at the back of a
    # cannon that's perched up on this thin little hill. It's tough to see
    # where the hill ends and the grass below starts. On top of that,
    # there's this big tower out there, and unless you've played before,
    # it's kinda tough to tell how big the tower is, and how far away it is.

    # SO, when people join the game and are reading the rules, and then
    # waiting for everyone else to read the rules, we're going to give
    # them a little fly-by from the tower to the cannons, to establish
    # some perspective.

    # The fly-by will start as soon as the minigame shows up on-screen
    # (i.e. when onstage() is called). When everyone is ready to play
    # the game (i.e. when setGameStart() is called), if the camera is
    # still in the fly-by, it will simply cut over to the
    # behind-the-cannon shot.

    def __startIntro(self):
        # timing
        self.T_WATER = 1
        self.T_WATER2LONGVIEW = 1
        self.T_LONGVIEW = 1
        self.T_LONGVIEW2TOONHEAD = 2
        self.T_TOONHEAD = 2
        self.T_TOONHEAD2CANNONBACK = 2

        taskLookInWater = Task(self.__taskLookInWater)
        taskPullBackFromWater = Task(self.__taskPullBackFromWater)
        taskFlyUpToToon = Task(self.__flyUpToToon)
        taskFlyToBackOfCannon = Task(self.__flyToBackOfCannon)

        # all of the tasks will share this common data dictionary
        commonData = {}
        taskLookInWater.data = commonData
        taskPullBackFromWater.data = commonData
        taskFlyUpToToon.data = commonData
        taskFlyToBackOfCannon.data = commonData

        introTask = Task.sequence(taskLookInWater,
                                  Task.pause(self.T_WATER),
                                  taskPullBackFromWater,
                                  Task.pause(self.T_WATER2LONGVIEW + \
                                             self.T_LONGVIEW),
                                  taskFlyUpToToon,
                                  Task.pause(self.T_LONGVIEW2TOONHEAD + \
                                             self.T_TOONHEAD),
                                  taskFlyToBackOfCannon)

        taskMgr.add(introTask, self.INTRO_TASK_NAME)

    def __stopIntro(self):
        taskMgr.remove(self.INTRO_TASK_NAME)
        taskMgr.remove(self.INTRO_TASK_NAME_CAMERA_LERP)
        # reclaim the camera
        camera.wrtReparentTo(render)

    def __spawnCameraLookAtLerp(self, targetPos, targetLookAt, duration):
        """
        This function spawns a camera lerp task that will put the
        camera at the target location, looking at the lookAt point
        """
        # set the new parameters to determine the target HPR
        oldPos = camera.getPos()
        oldHpr = camera.getHpr()

        camera.setPos(targetPos)
        camera.lookAt(targetLookAt)

        # get the target HPR
        targetHpr = camera.getHpr()

        # put the camera back where we found it
        camera.setPos(oldPos)
        camera.setHpr(oldHpr)

        # spawn a camera LERP task
        camera.lerpPosHpr(Point3(targetPos), targetHpr, duration,
                          blendType = "easeInOut",
                          task = self.INTRO_TASK_NAME_CAMERA_LERP)

    def __taskLookInWater(self, task):
        # place the camera a little above the tower, looking into the water
        task.data['cannonCenter'] = Point3(0, CANNON_Y, CANNON_Z)
        task.data['towerWaterCenter'] = Point3(self.towerPos +
                                               Point3(0, 0, TOWER_HEIGHT))
        task.data['vecTowerToCannon'] = Point3(task.data['cannonCenter'] -
                                               task.data['towerWaterCenter'])
        vecAwayFromCannons = Vec3(Point3(0,0,0)-task.data['vecTowerToCannon'])
        vecAwayFromCannons.setZ(0.)
        vecAwayFromCannons.normalize()
        camLoc = Point3(vecAwayFromCannons * 20) + Point3(0, 0, 20)
        camLoc = camLoc + task.data['towerWaterCenter']
        camera.setPos(camLoc)
        camera.lookAt(task.data['towerWaterCenter'])
        task.data['vecAwayFromCannons'] = vecAwayFromCannons
        return Task.done

    def __taskPullBackFromWater(self, task):
        # pull the camera back from the water, so that the cannons can be seen
        camLoc = Point3(task.data['vecAwayFromCannons'] * 40) + \
                 Point3(0, 0, 20)
        camLoc = camLoc + task.data['towerWaterCenter']
        lookAt = task.data['cannonCenter']
        self.__spawnCameraLookAtLerp(camLoc, lookAt, self.T_WATER2LONGVIEW)
        return Task.done

    def __flyUpToToon(self, task):
        # fly the camera up to the local toon's face
        headPos = self.toonHeadDict[self.localAvId].getPos(render)
        camLoc = headPos + Point3(0, 5, 0)
        lookAt = Point3(headPos)
        self.__spawnCameraLookAtLerp(camLoc, lookAt, self.T_LONGVIEW2TOONHEAD)
        return Task.done

    def __flyToBackOfCannon(self, task):
        # we want to pivot around the cannon, 180 degrees
        # while lerping the camera back to the starting position
        # make a node in the center of the cannon, parent
        # the camera under it, and lerpHpr the node
        # simultaneously lerpPos the camera in the node's
        # frame of reference so that it ends up in the
        # start position

        # create the rotation node
        lerpNode = hidden.attachNewNode('CannonGameCameraLerpNode')
        lerpNode.reparentTo(render)
        lerpNode.setPos(self.cannonLocationDict[self.localAvId] +
                        Point3(0,1,0))

        # get the camera's current position, wrt the rotation node
        relCamPos = camera.getPos(lerpNode)
        relCamHpr = camera.getHpr(lerpNode)

        # calculate the final position of the camera wrt the
        # rotated rotation node
        startRotation = lerpNode.getHpr()
        endRotation = Point3(-180, 0, 0)
        lerpNode.setHpr(endRotation)
        camera.setPos(self.__getCameraPositionBehindCannon())
        endPos = camera.getPos(lerpNode)
        lerpNode.setHpr(startRotation)

        # parent the camera to the rotation node, preserving its
        # original position wrt render
        camera.reparentTo(lerpNode)
        camera.setPos(relCamPos)
        camera.setHpr(relCamHpr)

        # rotate the rotation node
        lerpNode.lerpHpr(endRotation, self.T_TOONHEAD2CANNONBACK,
                         blendType = "easeInOut",
                         task = self.INTRO_TASK_NAME_CAMERA_LERP)
        # lerp the camera position
        camera.lerpPos(endPos, self.T_TOONHEAD2CANNONBACK,
                       blendType = "easeInOut",
                       task = self.INTRO_TASK_NAME_CAMERA_LERP)
        return Task.done

