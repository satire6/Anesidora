from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownTimer
from direct.task.Task import Task
from toontown.minigame import Trajectory
import math
from toontown.toon import ToonHead
from toontown.effects import Splash
from toontown.effects import DustCloud
from toontown.minigame import CannonGameGlobals
import CannonGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.distributed import DistributedObject
from toontown.effects import Wake
from direct.controls.ControlManager import CollisionHandlerRayStart

# some constants
LAND_TIME = 2

WORLD_SCALE = 2.

GROUND_SCALE = 1.4 * WORLD_SCALE
CANNON_SCALE = 1.0

FAR_PLANE_DIST = 600 * WORLD_SCALE

# lowest point we should allow the toon to fall
# (just in case he doesn't hit the terrain)
GROUND_PLANE_MIN = -15

CANNON_Y = -int((CannonGameGlobals.TowerYRange/2)*1.3)
CANNON_X_SPACING = 12
CANNON_Z = 20

CANNON_ROTATION_MIN = -55
CANNON_ROTATION_MAX = 50
CANNON_ROTATION_VEL = 15.0 # move 15 units every second

CANNON_ANGLE_MIN = 15
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0

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
#INITIAL_VELOCITY = 94.0
INITIAL_VELOCITY = 80.0

# this is how fast you have to be falling to generate a whistling sound
WHISTLE_SPEED = INITIAL_VELOCITY * 0.35
    

class DistributedCannon(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCannon")
    
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

    # We used to use the insert key, but nowadays it's the delete key
    # instead (for better Mac compatibility).  We actually support
    # both.
    BUMPER_KEY = "delete"
    BUMPER_KEY2 = "insert"

    INTRO_TASK_NAME = "CannonGameIntro"
    INTRO_TASK_NAME_CAMERA_LERP = "CannonGameIntroCamera"

    def __init__(self, cr):

        DistributedObject.DistributedObject.__init__(self, cr)

        self.avId = 0
        self.av = None
        self.localToonShooting = 0
        self.nodePath = None
        self.collSphere = None
        self.collNode = None
        self.collNodePath = None

        self.madeGui = 0
        self.gui = None

        self.cannonLocation = None
        self.cannonPosition = None
        self.cannon = None
        self.toonModel = None
        self.shadowNode = None
        self.toonHead = None
        self.toonScale = None
        self.estateId = None
        self.targetId = None
        self.splash = None
        self.dustCloud = None
        self.model_Created = 0
        self.lastWakeTime = 0
        
        # The AI will call setOccupied(0), too, but we call it first
        # just to be on the safe side, so we don't try to access a
        # non-existent avatar.
        #self.setOccupied(0)

        # since there are multiple inputs tied to each
        # of these (buttons and keypresses), they are
        # incremented for every button or keypress
        # that is active
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0

        # reset fly/collision info
        self.hitBumper = 0
        self.hitTarget = 0
        self.lastPos = Vec3(0,0,0)
        self.lastVel = Vec3(0,0,0)
        self.vel = Vec3(0,0,0)
        self.landingPos = Vec3(0,0,0)
        self.t = 0
        self.lastT = 0
        self.deltaT = 0
        self.hitTrack = None

        # for shadow lifting as we fly over the terrain
        self.cTrav = None
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.lifter = None

        # for collisions
        self.flyColNode = None
        self.flyColNodePath = None
        
        self.bumperCol = None

        # this is set to true when the local cannon is moving
        self.cannonMoving = 0

        # this is set to true if toon lands in water
        self.inWater = 0
        
        self.localAvId = base.localAvatar.doId

        # create an ClassicFSM for u,u,d,d,l,r,l,r code
        self.nextState = None
        self.nextKey = None
        self.cannonsActive = 0
        self.codeFSM = ClassicFSM.ClassicFSM(
            'CannonCode',
            [State.State('init',
                         self.enterInit,
                         self.exitInit,
                         ['u1', 'init']),
             State.State('u1',
                         self.enteru1,
                         self.exitu1,
                         ['u2', 'init']),
             State.State('u2',
                         self.enteru2,
                         self.exitu2,
                         ['d3', 'init']),
             State.State('d3',
                         self.enterd3,
                         self.exitd3,
                         ['d4', 'init']),
             State.State('d4',
                         self.enterd4,
                         self.exitd4,
                         ['l5', 'init']),
             State.State('l5',
                         self.enterl5,
                         self.exitl5,
                         ['r6', 'init']),
             State.State('r6',
                         self.enterr6,
                         self.exitr6,
                         ['l7', 'init']),
             State.State('l7',
                         self.enterl7,
                         self.exitl7,
                         ['r8', 'init']),
             State.State('r8',
                         self.enterr8,
                         self.exitr8,
                         ['acceptCode', 'init']),
             State.State('acceptCode',
                         self.enterAcceptCode,
                         self.exitAcceptCode,
                         ['init', 'final']),
             State.State('final',
                         self.enterFinal,
                         self.exitFinal,
                         []),
             ],
            # Initial State,
            'init',
            # Final State,
            'final',
            )
        self.codeFSM.enterInitialState()

        self.curPinballScore = 0
        self.curPinballMultiplier = 1
        

        
    def disable(self):
        # I think we should unmake the GUI first, so we are sure all tasks are removed.
        self.__unmakeGui()
        taskMgr.remove(self.taskNameFireCannon)
        taskMgr.remove(self.taskNameShoot)
        taskMgr.remove(self.taskNameFly)
        taskMgr.remove(self.taskNameSmoke)
        self.ignoreAll()
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0)
        self.nodePath.detachNode()
        if self.hitTrack:
            self.hitTrack.finish()
            del self.hitTrack
            self.hitTrack = None
        DistributedObject.DistributedObject.disable(self)

    def __unmakeGui(self):
        if not self.madeGui:
            return
        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        
        self.taskNameFireCannon = self.taskName("fireCannon")
        self.taskNameShoot = self.taskName("shootTask")
        self.taskNameSmoke = self.taskName("smokeTask")
        self.taskNameFly = self.taskName("flyTask")
        
        self.nodePath = NodePath(self.uniqueName('Cannon'))
        self.load()
        self.activateCannons()
        # listen for key presses
        self.listenForCode()

    def listenForCode(self):
        self.accept(self.UP_KEY+"-up", self.__upKeyCode)
        self.accept(self.DOWN_KEY+"-up", self.__downKeyCode)
        self.accept(self.LEFT_KEY+"-up", self.__leftKeyCode)
        self.accept(self.RIGHT_KEY+"-up", self.__rightKeyCode)

    def ignoreCode(self):
        self.ignore(self.UP_KEY+"-up")
        self.ignore(self.DOWN_KEY+"-up")
        self.ignore(self.LEFT_KEY+"-up")
        self.ignore(self.RIGHT_KEY+"-up")
        
    def activateCannons(self):
        if not self.cannonsActive:
            self.cannonsActive = 1
            
            self.onstage()

            # Put the cannon in the world
            self.nodePath.reparentTo(self.getParentNodePath())
            
            # When the localToon steps up to the cannon, we call requestEnter
            self.accept(self.uniqueName('enterCannonSphere'),
                        self.__handleEnterSphere)

    def deActivateCannons(self):
        if self.cannonsActive:
            self.cannonsActive = 0
            self.offstage()
            self.nodePath.reparentTo(hidden)
            self.ignore(self.uniqueName('enterCannonSphere'))
            
    def delete(self):
        self.offstage()
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def __handleEnterSphere(self, collEntry):
        # take toon out of walk so he can't interact with anything while waiting to enter cannon
        self.notify.debug('collEntry: %s' % collEntry)
        base.cr.playGame.getPlace().setState('fishing')
        self.d_requestEnter()

    def d_requestEnter(self):
        self.sendUpdate("requestEnter", [])

    def requestExit(self):
        self.notify.debug('requestExit')
        base.localAvatar.reparentTo(render)
        base.cr.playGame.getPlace().setState("walk")
                    
    def getSphereRadius(self):
        """getSphereRadius(self)
        This method can be overwritten by an inheritor.
        """
        return 1.5

    def getParentNodePath(self):
        """getParentNodePath(self)
        This defaults to render, but may be overridden by an inheritor
        """
        return base.cr.playGame.hood.loader.geom
        #return render

    def setEstateId(self, estateId):
        self.estateId = estateId

    def setTargetId(self, targetId):
        self.notify.debug('setTargetId %d' % targetId)
        self.targetId = targetId        
        
    # The handler that catches the initial position and orientation
    # established on the AI
    def setPosHpr(self, x, y, z, h, p, r):
        self.nodePath.setPosHpr(x, y, z, h, p, r)

    def setMovie(self, mode, avId):
        assert(self.notify.debug("%s setMovie(%s, %s)" % (self.doId, avId, mode)))

        wasLocalToon = self.localToonShooting

        self.avId = avId
        #self.localToonShooting = 0

        if (mode == CannonGlobals.CANNON_MOVIE_CLEAR):
            # No one is in the cannon; it's available.
            self.listenForCode()
            self.setLanded()
            #self.collSphere.setTangible(0)
        elif (mode == CannonGlobals.CANNON_MOVIE_LANDED):
            # Make sure toonHead is hidden.  If someone walks into
            # the zone after we have fired, they will see a setOccupied(avId)
            # message even after the av has left the cannon.
            self.setLanded()
        elif (mode == CannonGlobals.CANNON_MOVIE_FORCE_EXIT):
            self.exitCannon(self.avId)
            self.setLanded()
        elif (mode == CannonGlobals.CANNON_MOVIE_LOAD):
            self.ignoreCode()
            # The cannon is occupied; no one else may be here.
            #self.collSphere.setTangible(1)
            if (self.avId == base.localAvatar.doId):
                # cache the animations we'll use
                base.localAvatar.pose('lose', 110)
                base.localAvatar.pose('slip-forward', 25)

                # put toon in cannon
                base.cr.playGame.getPlace().setState('fishing')
                base.localAvatar.setTeleportAvailable(0)
                base.localAvatar.collisionsOff()

                # Free up two of the nametag cells on the bottom edge
                # of the screen to leave room for the cannon gui.
                base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 0)
                base.setCellsAvailable([base.rightCells[1]], 0)

                self.localToonShooting = 1
                self.__makeGui()
                camera.reparentTo(self.barrel)
                camera.setPos(.5,-2,2.5)

                #reset pinball scores
                self.curPinballScore = 0
                self.curPinballMultiplier =1

                self.incrementPinballInfo(0,0)
                
            if (self.cr.doId2do.has_key(self.avId)):
                # If the toon exists, look it up
                self.av = self.cr.doId2do[self.avId]
                self.acceptOnce(self.av.uniqueName('disable'), 
                                        self.__avatarGone)

                # Parent it to the cannon
                self.av.stopSmooth()

                self.__createToonModels()
            else:
                self.notify.warning("Unknown avatar %d in cannon %d" % (self.avId, self.doId))

        # If the local toon was involved but is no longer, restore
        # walk mode.  We do this down here, after we have twiddled
        # with the tangible flag, so that the toon must walk out and
        # walk back in again in order to generate the enter event
        # again.
        if (wasLocalToon and not self.localToonShooting):
            # Restore the normal nametag cells.
            base.setCellsAvailable([base.bottomCells[3], base.bottomCells[4]], 1)
            base.setCellsAvailable([base.rightCells[1]], 1)
        return

    def __avatarGone(self):
        # Called when the avatar in the fishing spot vanishes.

        # The AI will call setMovie(FORCE_EXIT), too, but we call it first
        # just to be on the safe side, so we don't try to access a
        # non-existent avatar.
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0)

    def load(self):
        assert(self.notify.debug("load"))

        self.cannon = loader.loadModel(
            "phase_4/models/minigames/toon_cannon")
        self.shadow = loader.loadModel(
            "phase_3/models/props/drop_shadow")
        self.shadowNode = hidden.attachNewNode("dropShadow")
        self.shadow.copyTo(self.shadowNode)
        self.smoke = loader.loadModel(
            "phase_4/models/props/test_clouds")
        self.smoke.setBillboardPointEye()
        
        self.cannon.setScale(CANNON_SCALE)
        self.shadowNode.setColor(0,0,0,0.5)

        # put the shadow in the 'fixed' bin, so that it will be
        # drawn correctly in front of the translucent water
        # NOTE: if we put trees or other opaque/transparent
        # objects in the scene, put the shadow in the fixed
        # bin only when it's over the water
        # undo with shadow.clearBin()
        self.shadowNode.setBin('fixed', 0, 1)
        

        # Splash object for when toon hits the water
        self.splash = Splash.Splash(render)
        # Dust cloud object for when toon hits ground
        self.dustCloud = DustCloud.DustCloud(render)
        self.dustCloud.setBillboardPointEye()

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
        self.sndHitHouse   = base.loadSfx(\
                                 "phase_5/audio/sfx/AA_drop_sandbag.mp3")

        # Make a collision sphere to detect when an avatar enters the
        # cannon.
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())
        
        # Make the sphere intangible, initially.
        self.collSphere.setTangible(1)
        self.collNode = CollisionNode(self.uniqueName('CannonSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)
        
        #self.setupMovingShadow()
        self.loadCannonBumper()
        
    def setupMovingShadow(self):
        #self.cTrav = CollisionTraverser("DistributedCannon")
        self.cTrav = base.cTrav
        
        # Set up the collison ray
        # This is a ray cast down to detect floor polygons:
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode('cRayNode')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = self.shadowNode.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = ToontownGlobals.FloorBitmask
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())

        # set up floor collision mechanism
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(ToontownGlobals.FloorOffset)
        # ?Something? is about 20.0 feet high, so start it there:
        self.lifter.setReach(20.0)
        #self.lifter.addCollider(self.cRayNodePath, self.shadowNodePath)

        self.enableRaycast(1)
        
    def enableRaycast(self, enable=1):
        """
        enable/disable raycast, useful for when we know
        when the suit will change elevations
        """
        if (not self.cTrav
                or not hasattr(self, "cRayNode")
                or not self.cRayNode):
            return
        self.notify.debug("-------enabling raycast--------")
        self.cTrav.removeCollider(self.cRayNodePath)
        if enable:
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)

    def __makeGui(self):
        if self.madeGui:
            return

        # set up the cannon aiming/firing gui
        guiModel = "phase_4/models/gui/cannon_game_gui"
        cannonGui = loader.loadModel(guiModel)
        self.aimPad = DirectFrame(image = cannonGui.find("**/CannonFire_PAD"),
                                  relief = None,
                                  pos = (0.7, 0, -0.553333),
                                  scale = 0.8,
                                  )
        cannonGui.removeNode()

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

        self.__enableAimInterface()

        self.madeGui = 1

    def __unmakeGui(self):
        self.notify.debug("__unmakeGui")
        if not self.madeGui:
            return

        self.__disableAimInterface()

        # Do we need to unbind?
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)

        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    def unload(self):
        assert(self.notify.debug("unload"))

        self.ignoreCode()
        del self.codeFSM
        
        # get rid of original cannon model
        if self.cannon:
            self.cannon.removeNode()
            self.cannon = None

        # get rid of original dropshadow model
        if self.shadowNode != None:
            self.shadowNode.removeNode()
            del self.shadowNode

        # get rid of the splash
        if self.splash != None:
            self.splash.destroy()
            del self.splash

        # get rid of the dust cloud
        if self.dustCloud != None:
            self.dustCloud.destroy()
            del self.dustCloud

        # Get rid of audio
        del self.sndCannonMove
        del self.sndCannonFire
        del self.sndHitHouse
        del self.sndHitGround
        del self.sndHitTower
        del self.sndHitWater
        del self.sndWhizz
        del self.sndWin
        
        #get rid of bumper collsion
        self.bumperCol = None
        taskMgr.remove(self.uniqueName("BumperON"))

        if self.av:
            self.__resetToon(self.av)
            # Reset anim an run play rate
            self.av.loop('neutral')
            self.av.setPlayRate(1.0, 'run')
            if hasattr(self.av, "nametag"):
                self.av.nametag.removeNametag(self.toonHead.tag)
        # make sure the blink and lookaround tasks are cleaned up
        if (self.toonHead != None):
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            self.toonHead = None
        if (self.toonModel != None):
            self.toonModel.removeNode()
            self.toonModel = None
        del self.toonScale

        del self.cannonLocation
        del self.cRay
        del self.cRayNode
        if self.cRayNodePath:
            self.cRayNodePath.removeNode()
            del self.cRayNodePath
        del self.lifter
        self.enableRaycast(0)

    def onstage(self):
        assert(self.notify.debug("onstage"))

        # show everything
        self.__createCannon()
        self.cannon.reparentTo(self.nodePath)
        self.splash.reparentTo(render)
        self.dustCloud.reparentTo(render)

    def offstage(self):
        assert(self.notify.debug("offstage"))
        if self.cannon:
            self.cannon.reparentTo(hidden)
        if self.splash:
            self.splash.reparentTo(hidden)
            self.splash.stop()
        if self.dustCloud:
            self.dustCloud.reparentTo(hidden)
            self.dustCloud.stop()

    def __createCannon(self):
        self.barrel = self.cannon.find("**/cannon")
        self.cannonLocation = Point3(0, 0, 0.025)
        self.cannonPosition = [0,CANNON_ANGLE_MIN]
        self.cannon.setPos(self.cannonLocation)
        self.__updateCannonPosition(self.avId)

    def __createToonModels(self):
        self.model_Created = 1
        # create the toon model
        toon = self.av
        # store the toon's original scale
        self.toonScale = toon.getScale()
        # force use of highest LOD
        toon.useLOD(1000)
        # stick the toon under an additional node
        # in order to move the toon's local origin to its waist
        toonParent = render.attachNewNode("toonOriginChange")
        toon.wrtReparentTo(toonParent)
        toon.setPosHpr(0,0,-(toon.getHeight()/2.),0,-90,0)
        self.toonModel = toonParent

        #del self.av.wake
        #self.av.wake = Wake.Wake(render,self.av)
        #self.av.getWake().setBillboardPointEye()
        #self.av.getWake().setScale(.3)
        
        # create the toon head
        self.toonHead = ToonHead.ToonHead()
        self.toonHead.setupHead(self.av.style)
        self.toonHead.reparentTo(hidden)

        # attach a chat balloon to the toonhead
        tag = NametagFloat3d()
        tag.setContents(Nametag.CSpeech | Nametag.CThought)
        tag.setBillboardOffset(0)
        tag.setAvatar(self.toonHead)
        toon.nametag.addNametag(tag)

        tagPath = self.toonHead.attachNewNode(tag.upcastToPandaNode())
        tagPath.setPos(0, 0, 1)
        self.toonHead.tag = tag

        # stuff the toon into his cannon
        self.__loadToonInCannon()

        # hide the avatar's dropshadow
        self.av.dropShadow.hide()

        # create a copy of the drop shadow
        self.dropShadow = self.shadowNode.copyTo(hidden)
        #self.lifter.addCollider(self.cRayNodePath, self.dropShadow)

    def __destroyToonModels(self):
        assert(self.notify.debug("__destroyToonModels"))
        if (self.av != None):
            # show the toons original drop shadows..
            self.av.dropShadow.show()
            # ... and destroy the one used for flight
            if (self.dropShadow != None):
                self.dropShadow.removeNode()
                self.dropShadow = None

            self.hitBumper = 0
            self.hitTarget = 0
            self.angularVel = 0
            self.vel = Vec3(0,0,0)
            self.lastVel = Vec3(0,0,0)
            self.lastPos = Vec3(0,0,0)
            self.landingPos = Vec3(0,0,0)
            self.t = 0
            self.lastT = 0
            self.deltaT = 0
            self.av = None
            self.lastWakeTime = 0
            self.localToonShooting = 0
            
        if (self.toonHead != None):
            self.toonHead.reparentTo(hidden)
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            self.toonHead = None
        if (self.toonModel != None):
            self.toonModel.removeNode()
            self.toonModel = None
        self.model_Created = 0

    def updateCannonPosition(self, avId, zRot, angle):
        # the server is telling us that a cannon has moved (rotated)
        #self.notify.debug("updateCannonPosition: " + str(avId) + \
        #                  ": zRot=" + str(zRot) + ", angle=" + str(angle))
        if avId != self.localAvId:
            self.cannonPosition = [zRot, angle]
            self.__updateCannonPosition(avId)

    def setCannonWillFire(self, avId, fireTime, zRot, angle, timestamp):
        # the server is telling us that a cannon will fire at a specific time
        self.notify.debug("setCannonWillFire: " + str(avId)
                          + ": zRot=" + str(zRot) + ", angle=" + str(angle)
                          + ", time=" + str(fireTime))

        # we might get this message from the server before we even get a
        # chance to createToonModel...for instance if we just walked in the zone
        # If this is the case, don't create a fire task
        if not self.model_Created:
            self.notify.warning("We walked into the zone mid-flight, so we won't see it")
            return

        # set the cannon's position
        # NOTE: do this for the local toon; cannon angles may have been
        # modified by conversion to and from fixed-point, and we want
        # to have the same values that all the other clients have
        self.cannonPosition[0] = zRot
        self.cannonPosition[1] = angle
        self.__updateCannonPosition(avId)

        # create a task to fire off the cannon
        task = Task(self.__fireCannonTask)
        task.avId = avId

        # fireTime is in game time
        ts = globalClockDelta.localElapsedTime(timestamp)
        task.fireTime = fireTime - ts
        if (task.fireTime < 0.0):
            task.fireTime = 0.0
        taskMgr.add(task, self.taskNameFireCannon)

    def exitCannon(self, avId):
        # take down the gui
        self.__unmakeGui()
        #self.__stopFlyTask(self.avId)
        
        # The AI is telling us that avId has been sitting in the
        # cannon too long without firing.  We'll exit him out now.
        if self.avId == avId:
            if self.av:
                #self.av.reparentTo(render)
                self.__resetToonToCannon(self.av)

    # UI crep
    def __enableAimInterface(self):
        self.aimPad.show()

        # listen for key presses
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.accept(self.BUMPER_KEY, self.__bumperKeyPressed)
        self.accept(self.BUMPER_KEY2, self.__bumperKeyPressed)

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
        self.handleCodeKey('left')
        self.__leftReleased()

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY+"-up")
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.handleCodeKey('right')
        self.__rightReleased()

    def __upKeyReleased(self):
        self.ignore(self.UP_KEY+"-up")
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upReleased()

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY+"-up")
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.handleCodeKey('down')
        self.__downReleased()

    def __upKeyCode(self):
        self.handleCodeKey('up')

    def __downKeyCode(self):
        self.handleCodeKey('down')

    def __rightKeyCode(self):
        self.handleCodeKey('right')

    def __leftKeyCode(self):
        self.handleCodeKey('left')
        
    # button event handlers (also used by keyboard event handlers)
    def __firePressed(self):
        self.notify.debug("fire pressed")
        # make sure everyone has the correct position
        self.__broadcastLocalCannonPosition()

        self.__unmakeGui()

        # send the 'cannon lit' message and wait for the server
        # to tell us the time that our cannon will shoot
        self.sendUpdate("setCannonLit",
                        [self.cannonPosition[0],
                         self.cannonPosition[1]])

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

    def __localCannonMoveTask(self, task):
        """ this task moves the cannon
        """
        pos = self.cannonPosition

        # these are used to determine if the cannon actually moved
        oldRot = pos[0]
        oldAng = pos[1]

        # cannon rotation
        rotVel = 0
        if self.leftPressed:
            rotVel += CANNON_ROTATION_VEL
        if self.rightPressed:
            rotVel -= CANNON_ROTATION_VEL
        pos[0] += rotVel * globalClock.getDt()
        if pos[0] < CANNON_ROTATION_MIN:
            pos[0] = CANNON_ROTATION_MIN
        elif pos[0] > CANNON_ROTATION_MAX:
            pos[0] = CANNON_ROTATION_MAX

        # cannon barrel angle
        angVel = 0
        if self.upPressed:
            angVel += CANNON_ANGLE_VEL
        if self.downPressed:
            angVel -= CANNON_ANGLE_VEL
        pos[1] += angVel * globalClock.getDt()
        if pos[1] < CANNON_ANGLE_MIN:
            pos[1] = CANNON_ANGLE_MIN
        elif pos[1] > CANNON_ANGLE_MAX:
            pos[1] = CANNON_ANGLE_MAX

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
                print("Cannon Rot:%s Angle:%s" % (pos[0], pos[1]))

        return Task.cont


    def __broadcastLocalCannonPosition(self):
        # send a position update for the local cannon
        self.sendUpdate("setCannonPosition",
                        [self.cannonPosition[0],
                         self.cannonPosition[1]])

    def __updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0., 0.)
        self.barrel.setHpr(0., self.cannonPosition[1], 0.)
        # squish the shadow to match the barrel pos
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1-.5*float(newP)/maxP
        shadow = self.cannon.find("**/square_drop_shadow")
        shadow.setScale(1,yScale,1)

    def __getCameraPositionBehindCannon(self):
        return Point3(self.cannonLocationDict[self.localAvId][0],
                      CANNON_Y - 5.0, CANNON_Z + 7)

    def __putCameraBehindCannon(self):
        # place the camera behind our cannon
        camera.setPos(self.__getCameraPositionBehindCannon())
        camera.setHpr(0, 0, 0)

    def __loadToonInCannon(self):
        # hide the full toon model
        self.toonModel.reparentTo(hidden)
        # show the toon head
        self.toonHead.startBlink()
        self.toonHead.startLookAround()
        # parent head to the cannon barrel
        self.toonHead.reparentTo(self.barrel)
        # put it up at the muzzle of the cannon, facing down
        self.toonHead.setPosHpr(0,6,0,0,-45,0)
        # restore proper scale (wrt render)
        sc = self.toonScale
        self.toonHead.setScale(render, sc[0], sc[1], sc[2])
        # put body model where it will start it's flight
        self.toonModel.setPos(self.toonHead.getPos(render))

    def __toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def __toDegrees(self, angle):
        return angle * 360.0 / (2.0 * math.pi)

    def __calcFlightResults(self, avId, launchTime):
        """
        returns dict with keys:
        startPos, startHpr, startVel, trajectory, timeOfImpact, hitWhat
        """
        head = self.toonHead
        startPos = head.getPos(render)
        startHpr = head.getHpr(render)

        # get the cannon's orientation relative to render
        hpr = self.barrel.getHpr(render)

        # calc the initial velocity in render space
        rotation = self.__toRadians(hpr[0])
        angle = self.__toRadians(hpr[1])
        horizVel = INITIAL_VELOCITY * math.cos(angle)
        xVel = horizVel * -math.sin(rotation)
        yVel = horizVel * math.cos(rotation)
        zVel = INITIAL_VELOCITY * math.sin(angle)
        startVel = Vec3(xVel, yVel, zVel)

        trajectory = Trajectory.Trajectory(launchTime, startPos, startVel)
        self.trajectory = trajectory
        # check if we hit any treasures along the way
        hitTreasures = self.__calcHitTreasures(trajectory)

        # figure out what will be hit, and when
        timeOfImpact, hitWhat = self.__calcToonImpact(trajectory)
        
        
        return {
            'startPos' : startPos,
            'startHpr' : startHpr,
            'startVel' : startVel,
            'trajectory' : trajectory,
            'timeOfImpact' : 3*timeOfImpact,
            'hitWhat' : hitWhat,
            }

    def __fireCannonTask(self, task):
        """
        spawn a task sequence to shoot the cannon, fly
        the avatar through the air, handle the toon's landing
        """
        launchTime = task.fireTime
        avId = task.avId
        self.inWater = 0
        #self.lastPos = Vec3(0,0,0)
        #self.lastVel = Vec3(0,0,0)
        #self.vel = Vec3(0,0,0)
        #self.landingPos = Vec3(0,0,0)

        assert(self.notify.debug("FIRING CANNON FOR AVATAR " + str(avId)))

        # band-aid for client crash
        if not self.toonHead:
            return Task.done
        
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
        head = self.toonHead
        head.stopBlink()
        head.stopLookAroundNow()
        head.reparentTo(hidden)
        # show the whole body, posbang it to where the
        # head was
        av = self.toonModel
        av.reparentTo(render)
        print("start Pos%s Hpr%s" % (startPos, startHpr))
        av.setPos(startPos)
        barrelHpr = self.barrel.getHpr(render)
        # subtract 90 degrees from hpr since barrels hpr measures the angle from the ground
        # and the toons hpr measures from vUp.
        #av.setHpr(barrelHpr)
        place = base.cr.playGame.getPlace()
        if self.av == base.localAvatar:
            place.fsm.request("stopped")        
        av.setHpr(startHpr)
        
        avatar = self.av
        avatar.loop('swim')
        avatar.setPosHpr(0,0,-(avatar.getHeight()/2.),0,0,0)
        #avatar.setHpr(0,0,0)
        
        # stock the tasks up with the info they need
        # store the info in a shared dictionary
        info = {}
        info['avId'] = avId
        info['trajectory'] = trajectory
        info['launchTime'] = launchTime
        info['timeOfImpact'] = timeOfImpact
        info['hitWhat'] = hitWhat
        info['toon'] = self.toonModel
        info['hRot'] = self.cannonPosition[0]
        info['haveWhistled'] = 0
        info['maxCamPullback'] = CAMERA_PULLBACK_MIN

        if self.localToonShooting:
            camera.reparentTo(self.av)
            camera.setP(45.0)
            camera.setZ(-10.0)

        # Set up collision test
        self.flyColSphere = CollisionSphere(0, 0, 
                                            self.av.getHeight()/2.0, 1.0)
        self.flyColNode = CollisionNode(self.uniqueName('flySphere'))
        self.flyColNode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask)
        self.flyColNode.addSolid(self.flyColSphere)
        self.flyColNodePath = self.av.attachNewNode(self.flyColNode)
        #self.flyColNodePath.show()
        self.flyColNodePath.setColor(1,0,0,1)
        self.handler = CollisionHandlerEvent()
        self.handler.setInPattern(self.uniqueName('cannonHit'))
        base.cTrav.addCollider(self.flyColNodePath, self.handler) 
        self.accept(self.uniqueName('cannonHit'), self.__handleCannonHit)

        # create the tasks
        shootTask = Task(self.__shootTask, self.taskNameShoot)
        smokeTask = Task(self.__smokeTask, self.taskNameSmoke)
        flyTask = Task(self.__flyTask, self.taskNameFly)
        # put the info dict on each task
        shootTask.info = info
        flyTask.info = info
        seqTask = Task.sequence(shootTask, smokeTask, flyTask)
        
        if self.av == base.localAvatar:
                print("disable controls")
                base.localAvatar.disableAvatarControls()
        
        # spawn the new task
        taskMgr.add(seqTask, self.taskName('flyingToon') + "-" + str(avId))
        self.acceptOnce(self.uniqueName("stopFlyTask"), self.__stopFlyTask)
        return Task.done

    def __stopFlyTask(self, avId):
        assert(self.notify.debug("%s(%s)" % (self.uniqueName("stopFlyTask"), avId)))
        taskMgr.remove(self.taskName('flyingToon') + "-" + str(avId))

    def b_setLanded(self):
        self.d_setLanded()
        #self.setLanded()
            
    def d_setLanded(self):
        self.notify.debug("localTOonshooting = %s" % self.localToonShooting)
        # The shooter can tell the server he's landed, and then the server
        # will pass the message along to all the other clients in this zone.
        if self.localToonShooting:
            self.sendUpdate("setLanded", [])

    def setLanded(self):
        self.removeAvFromCannon()

    def removeAvFromCannon(self):
        place = base.cr.playGame.getPlace()
        print("removeAvFromCannon")
        self.notify.debug('self.inWater = %s' % self.inWater)
        if place:
            # this is crashing LIVE
            if not hasattr(place, 'fsm'):
                return
            placeState = place.fsm.getCurrentState().getName()
            print placeState
            if ((self.inWater) or place.toonSubmerged) and (placeState != "fishing"):
                if (self.av != None):
                    self.av.startSmooth()
                    self.__destroyToonModels()
                    return
                    
        self.inWater = 0

        assert(self.notify.debug("%s removeAvFromCannon" % self.doId))
        if (self.av != None):
            assert(self.notify.debug("removeAvFromCannon: destroying toon models"))
            # make sure colliion handling is off
            self.__stopCollisionHandler(self.av)
            self.av.resetLOD()
            
            if self.av == base.localAvatar:
                if place and not self.inWater:
                    #place.setState('walk')
                    place.fsm.request("walk")
                else:
                    #self.av.loop('neutral')
                    pass

            #self.inWater = 0
            self.av.setPlayRate(1.0, 'run')
            self.av.nametag.removeNametag(self.toonHead.tag)
            # this is needed for distributed toons
            if self.av.getParent().getName() == "toonOriginChange":
                self.av.wrtReparentTo(render)
                self.__setToonUpright(self.av)
            if self.av == base.localAvatar:
                self.av.startPosHprBroadcast()
            #self.av.setParent(ToontownGlobals.SPRender)
            self.av.startSmooth()
            self.av.setScale(1,1,1)
            if self.av == base.localAvatar:
                print("enable controls")
                base.localAvatar.enableAvatarControls()
            self.ignore(self.av.uniqueName("disable"))
            self.__destroyToonModels()

        
    def __stopCollisionHandler(self, avatar):
        assert(self.notify.debug("%s __stopCollisionHandler" % self.doId ))
        #if avatar == base.localAvatar:
        if avatar:
            avatar.loop('neutral')
            #camera.reparentTo(avatar)
            # Reset collisions
            if self.flyColNode:
                self.flyColNode = None
            if avatar == base.localAvatar:
                avatar.collisionsOn()
            self.flyColSphere = None
            if self.flyColNodePath:
                base.cTrav.removeCollider(self.flyColNodePath)
                self.flyColNodePath.removeNode()
                self.flyColNodePath = None

            self.handler = None
            #base.cr.playGame.hood.loader.geom.reparentTo(render)
        
    def __handleCannonHit(self, collisionEntry):
        assert(self.notify.debug("%s __handleCannonHit" % self.doId))
        if self.av == None or self.flyColNode == None:
            return
        # ignore cSphere hits (butterflies) and treasureSphere hits
        hitNode = collisionEntry.getIntoNode().getName()

        #collisionEntry.getIntoNodePath().ls()

        self.notify.debug('hitNode = %s' % hitNode)
        self.notify.debug('hitNodePath.getParent = %s' % collisionEntry.getIntoNodePath().getParent())        

        self.vel = self.trajectory.getVel(self.t)
        vel = self.trajectory.getVel(self.t)
        vel.normalize()

        if self.hitBumper:
            vel = self.lastVel * 1
            vel.normalize()
            
        self.notify.debug('normalized vel=%s' % vel)

        #space = collisionEntry.getIntoMat()
        solid = collisionEntry.getInto()
        #space = solid.getMat()        
        intoNormal = collisionEntry.getSurfaceNormal(collisionEntry.getIntoNodePath())
        self.notify.debug('old intoNormal = %s' % intoNormal)
        intoNormal = collisionEntry.getSurfaceNormal(render)
        self.notify.debug('new intoNormal = %s' % intoNormal)
        
        #hitNormal = space.xformVec(intoNormal)
        hitPylonAboveWater = False
        hitPylonBelowWater = False

        if hitNode in ["pier_pylon_collisions_1", "pier_pylon_collisions_3"]:
            if collisionEntry.getSurfacePoint(render)[2] > 0:
                hitPylonAboveWater = True
                self.notify.debug('hitPylonAboveWater = True')
            else:
                hitPylonBelowWater = True
                self.notify.debug('hitPylonBelowWater = True')
                
            

        hitNormal = intoNormal
        if (hitNode.find("cSphere") == 0 or
            hitNode.find("treasureSphere") == 0 or
            hitNode.find("prop") == 0 or
            hitNode.find("distAvatarCollNode") == 0 or
            hitNode.find("CannonSphere") == 0 or
            hitNode.find("plotSphere") == 0 or
            hitNode.find("flySphere") == 0 or
            hitNode.find("mailboxSphere") == 0 or
            hitNode.find("FishingSpotSphere") == 0 or 
            hitNode == "gagtree_collision" or
            hitNode == "sign_collision" or
            hitNode == "FlowerSellBox" or
            hitPylonBelowWater):            
            self.notify.debug("--------------hit and ignoring %s" % hitNode)
            return
        if (vel.dot(hitNormal) > 0) and not hitNode == 'collision_roof' and not hitNode=='collision_fence':
            pass
            self.notify.debug("--------------hit and ignoring backfacing %s, dot=%s" % (hitNode,vel.dot(hitNormal)))
            return

        
        #if self.localToonShooting:
        if 1:
            intoNode = collisionEntry.getIntoNodePath()
            bumperNodes = ["collision_house", "collision_fence", "targetSphere", "collision_roof", "collision_cannon_bumper","statuaryCol"]
            # there is only one for now
            cloudBumpers = ["cloudSphere-0"]
            #cloudBumpers = []
            #for i in range(12):
            #    cloudBumpers.append("cloudSphere-" + str(i))
            bumperNodes += cloudBumpers

            if not hitNode in bumperNodes:
                self.__stopCollisionHandler(self.av)
                self.__stopFlyTask(self.avId)
                self.notify.debug('stopping flying since we hit %s' % hitNode)
                # Since we are done checking for collisions, we can now
                # tell the target whether we hit it or not
                if self.hitTarget == 0:
                    # we missed the target on this shot, let the AI know so
                    # the target can award points and reset
                    messenger.send("missedTarget")
            else:
                # If we hit the house or the bridge, we will ricochet and keep
                # flying, so don't kill the flyTask
                #if self.hitBumper != 1:
                if hitNode == "collision_house":
                    self.__hitHouse(self.av, collisionEntry)
                elif hitNode == "collision_fence":
                    self.__hitFence(self.av, collisionEntry)
                elif hitNode == "collision_roof":
                    self.__hitRoof(self.av, collisionEntry)                    
                elif hitNode == "targetSphere":
                    self.__hitTarget(self.av, collisionEntry, [vel])
                elif hitNode in cloudBumpers:
                    self.__hitCloudPlatform(self.av, collisionEntry)
                elif hitNode == 'collision_cannon_bumper':
                    self.__hitCannonBumper(self.av, collisionEntry)
                elif hitNode == 'statuaryCol':
                    self.__hitStatuary(self.av, collisionEntry)    
                else:
                    self.notify.debug("*************** hit something else ************")
                return
                
            # reparent camera to render now so dustcloud works
            if self.localToonShooting:
                camera.wrtReparentTo(render)
            # hide the drop shadow
            if self.dropShadow:
                self.dropShadow.reparentTo(hidden)
            #pos = collisionEntry.getIntoIntersectionPoint()
            pos = collisionEntry.getSurfacePoint(render)
            hpr = self.av.getHpr()
            #hitPos = space.xformPoint(pos)
            hitPos = collisionEntry.getSurfacePoint(render)

            pos = hitPos
            self.landingPos = pos
            self.notify.debug("hitNode,Normal = %s,%s" % (hitNode, intoNormal))
            
            track = Sequence()
            track.append(Func(self.av.wrtReparentTo, render))
            #track.append(Func(self.av.b_setParent, ToontownGlobals.SPRender))
            if self.localToonShooting:
                track.append(Func(self.av.collisionsOff))
            if ((hitPylonAboveWater) or
                (hitNode in ["matCollisions", "collision1",
                           "floor", "sand_collision",
                           "dirt_collision", "soil1",
                           "collision2", "floor_collision"])) :
                track.append(Func(self.__hitGround, self.av, pos))
                track.append(Wait(1.0))
                track.append(Func(self.__setToonUpright, self.av, self.landingPos))
            elif hitNode == "collision_house":
                track.append(Func(self.__hitHouse, self.av, collisionEntry))
            elif hitNode == "collision_fence" or hitNode == "collision4":
                track.append(Func(self.__hitFence, self.av, collisionEntry))
            elif hitNode == "targetSphere":
                track.append(Func(self.__hitHouse, self.av, collisionEntry))
            elif hitNode == "collision3":
                track.append(Func(self.__hitWater, self.av, pos, collisionEntry))
                track.append(Wait(2.0))
                track.append(Func(self.__setToonUpright, self.av, self.landingPos))
            elif hitNode == "roofOutside" or hitNode == "collision_roof" or hitNode == "roofclision":
                track.append(Func(self.__hitRoof, self.av, collisionEntry))
                track.append(Wait(2.0))
                track.append(Func(self.__setToonUpright, self.av, self.landingPos))
            elif hitNode.find("MovingPlatform") == 0 or hitNode.find("cloudSphere") == 0:
                track.append(Func(self.__hitCloudPlatform, self.av, collisionEntry))
            else:
                self.notify.warning("************* unhandled hitNode=%s parent =%s" % (hitNode, collisionEntry.getIntoNodePath().getParent()))

                #track.append(Wait(.5))
                #track.append(Func(self.av.collisionsOn))
                #t = Sequence(track)
                #t.start()
                #del track
                #return
            
            track.append(Func(self.b_setLanded))
            #track.append(Wait(.5))
            if self.localToonShooting:
                track.append(Func(self.av.collisionsOn))

            if self.hitTrack:
                self.hitTrack.finish()
            self.hitTrack = track
            self.hitTrack.start()

                
    def __hitGround(self, avatar, pos, extraArgs=[]):
        assert(self.notify.debug("__hitGround"))
        hitP = avatar.getPos(render)
        self.notify.debug("hitGround pos = %s, hitP = %s" % (pos, hitP))
        self.notify.debug("avatar hpr = %s" % avatar.getHpr())
        h = self.barrel.getH(render)
        avatar.setPos(pos[0],pos[1],pos[2]+avatar.getHeight()/3.0)
        # make avatar look in direction of velocity
        avatar.setHpr(h,-135,0)
        #p = Point3(self.vel[0],self.vel[1],self.vel[2])
        #avatar.lookAt(self.cannon)
        #avatar.setP(0)
        #avatar.setR(0)
        #toonParent.setPos(pos[0],pos[1],pos[2])
        #toonParent.setHpr(h,-135,0)
        self.notify.debug("parent = %s" % avatar.getParent())
        self.notify.debug("pos = %s, hpr = %s" % (avatar.getPos(render), avatar.getHpr(render))) 
        self.dustCloud.setPos(render, pos[0], pos[1], pos[2]+avatar.getHeight()/3.0)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)
        # Make him wiggle his legs                
        avatar.setPlayRate(2.0, 'run')
        avatar.loop("run")

        
    def __hitHouse(self, avatar, collisionEntry, extraArgs=[]):
        assert(self.notify.debug("__hitHouse"))
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=.2, angVel=3)
        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballHouse]
        self.incrementPinballInfo(pinballScore[0],pinballScore[1])


    def __hitFence(self, avatar, collisionEntry, extraArgs=[]):
        assert(self.notify.debug("__hitFence"))
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=.2, angVel=3)
        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballFence]
        self.incrementPinballInfo(pinballScore[0],pinballScore[1])


    def __hitTarget(self, avatar, collisionEntry, extraArgs=[]):
        assert(self.notify.debug("__hitTarget"))
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=.1, angVel=2)

        pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballTarget]
        self.incrementPinballInfo(pinballScore[0],pinballScore[1])        

        if self.localToonShooting:
            self.hitTarget = 1
            messenger.send("hitTarget", [self.avId, self.lastVel])

            
    # Hitting a bumper means we will bounce off at an angle
    # equal to the reflection of our incoming velocity about
    # the bumper's normal at the point of collision
    def __hitBumper(self, avatar, collisionEntry, sound, kr=.6, angVel=1):
        self.hitBumper = 1

        # play the sound immediately
        base.playSfx(self.sndHitHouse)

        # get the point of collision
        hitP = avatar.getPos(render)
        self.lastPos = hitP

        # find bumper node
        house = collisionEntry.getIntoNodePath()

        # find collision normal on bumper
        normal = collisionEntry.getSurfaceNormal(house)
        normal.normalize()

        # get the normal in world(render) coordinates
        #RAU getIntoMat() deprecated
        #space = collisionEntry.getIntoMat()
        #normal = space.xformVec(normal)

        #solid = collisionEntry.getInto()
        #space = solid.getMat()

        normal = collisionEntry.getSurfaceNormal(render)
        self.notify.debug('normal = %s' % normal)
        
        # find velocity of toon
        vel = self.vel * 1 #we need a copy 
        #vel = render.getRelativeVector(self.av, vel)

        speed = vel.length()
        #if self.deltaT > .00001:
        #    speed = vel.length() / self.deltaT
        vel.normalize()
        #vel = self.trajectory.getVel(self.t)
        #speed = vel.length()
        #vel.normalize()

        self.notify.debug('old vel = %s' % vel)

        # calculate the reflected velocity
        newVel = (normal * 2.0 + vel) * (kr*speed)
        self.lastVel = newVel

        self.notify.debug('new vel = %s' % newVel)

        # impose an angular velocity - 'cause it looks cool!
        self.angularVel = angVel*360

        # put the toon in fetal position while he spins
        t = Sequence(Func(avatar.pose, 'lose', 110))
        t.start()

                     
    def __hitRoof(self, avatar, collisionEntry, extraArgs=[]):
        assert(self.notify.debug("__hitRoof"))

        if True:
            self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.3, angVel=3)
            pinballScore = ToontownGlobals.PinballScoring[ToontownGlobals.PinballRoof]
            self.incrementPinballInfo(pinballScore[0],pinballScore[1])        
            return

        
        # find roof node
        np = collisionEntry.getIntoNodePath() 
        roof = np.getParent()
        
        # find collision normal on roof
        normal = collisionEntry.getSurfaceNormal(np)
        normal.normalize()
        # find velocity of toon
        vel = self.trajectory.getVel(self.t)
        vel.normalize()
        dot = normal.dot(vel)
        self.notify.debug("--------------dot product = %s---------------" % dot)
        
        # create a temp node with a y-axis that lines up with the roof normal
        # and a z-axis that is parallel to the slope of the roof
        temp = render.attachNewNode("temp")
        temp.iPosHpr()
        temp.lookAt(Point3(normal))
        temp.reparentTo(roof)
        #temp.iPos(avatar)
        self.notify.debug("avatar pos = %s, landingPos = %s" % (avatar.getPos(), self.landingPos))
        temp.setPos(render,self.landingPos)
        avatar.reparentTo(temp)
        avatar.setPosHpr(0,0.25,.5,0,270,180)
        avatar.pose('slip-forward', 25)  
        base.playSfx(self.sndHitHouse)
        avatar.setPlayRate(1.0, 'jump')

        # we have to get an inverse color scale, so the toon doesn't change
        # colors when we reparent him to the roof
        #cs = self.cr.playGame.hood.loader.geom.getColorScale()
        #if ((cs[0] > .001) and (cs[1] > .001) and (cs[2] > .001)):
        #    ics = VBase4(1.0/cs[0], 1.0/cs[1], 1.0/cs[2], 1)
        #    print "cs = %s, ics = %s, result = %s,%s,%s" % (cs, ics, cs[0]*ics[0], cs[1]*ics[1],cs[2]*ics[2]) 
        #    avatar.setColorScale(ics)

        h = self.barrel.getH(render)

        t = Sequence(
            LerpPosInterval(avatar, .5, Point3(0,0,-.5), blendType = 'easeInOut'),
            Func(avatar.clearColorScale),
            Func(avatar.wrtReparentTo, render),
            Wait(.3),
            #LerpScaleInterval(avatar, .05, Point3(1,2,.1), blendType = 'easeInOut'),
            #LerpScaleInterval(avatar, .05, 2.0, blendType = 'easeInOut'),
            #LerpScaleInterval(avatar, .05, 1, blendType = 'easeInOut'),
            Parallel(Func(avatar.setP, 0),
                     Func(avatar.play, 'jump', None, 19, 39),
                     LerpHprInterval(avatar, .3,
                                     Vec3(h,0,0),
                                     blendType="easeOut",
                                     ),
                     #LerpScaleInterval(avatar, .5, 1, blendType = 'easeInOut'),
                     ),
            Func(avatar.play, 'neutral'),
            #Func(self.__setToonUpright, self.av, self.av.getPos(render)),
            )
        t.start()
        hitP = avatar.getPos(render)


    def __hitBridge(self, avatar, collisionEntry, extraArgs=[]):
        self.notify.debug("hit bridge")
        hitP = avatar.getPos(render)
        self.dustCloud.setPos(render, hitP[0], hitP[1], hitP[2]-.5)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)

        
    def __hitWater(self, avatar, pos, collisionEntry, extraArgs=[]):
        hitP = avatar.getPos(render)
        if hitP[2] > ToontownGlobals.EstateWakeWaterHeight:
            # we hit the ground before we hit water
            self.notify.debug("we hit the ground before we hit water")
            self.__hitGround(avatar,pos,extraArgs)
            print("but not really")
            return
        
        self.inWater = 1
        self.notify.debug("hit water")
        hitP = avatar.getPos(render)
        # we landed in the water
        avatar.loop('neutral')
        # Show a splash
        self.splash.setPos(hitP)
        self.splash.setZ(ToontownGlobals.EstateWakeWaterHeight)
        self.splash.setScale(2)
        self.splash.play()
        # Play the splash sound
        base.playSfx(self.sndHitWater)
        place = base.cr.playGame.getPlace()
        self.notify.debug("hitWater: submerged = %s" % place.toonSubmerged)
        #avatar.loop('swim')
        # stand the toon upright
        #task.info['toon'].setHpr(task.info['hRot'],0,0)
        #self.__somebodyWon(task.info['avId'])


    def __hitCannonBumper(self, avatar, collisionEntry, extraArgs=[]):
        #import pdb; pdb.set_trace()
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
        score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballCannonBumper]
        self.incrementPinballInfo(score,multiplier)
        return


    def __hitStatuary(self, avatar, collisionEntry, extraArgs=[]):
        #import pdb; pdb.set_trace()
        self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
        score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballStatuary]
        intoNodePath = collisionEntry.getIntoNodePath()
        name = intoNodePath.getParent().getName()
        splitParts = name.split('-')
        if len(splitParts) >= 3:
            score = int(splitParts[1] )
            multiplier = int( splitParts[2])
            
        self.incrementPinballInfo(score,multiplier)
 


    def __hitCloudPlatform(self, avatar, collisionEntry, extraArgs=[]):
        if True:
            #import pdb; pdb.set_trace()
            self.__hitBumper(avatar, collisionEntry, self.sndHitHouse, kr=0.4, angVel=5)
            score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballCloudBumperLow]
            intoNodePath = collisionEntry.getIntoNodePath()

            name = intoNodePath.getParent().getName()
            splitParts = name.split('-')
            if len(splitParts) >= 3:
                score = int(splitParts[1] )
                multiplier = int( splitParts[2])
                            
            self.incrementPinballInfo(score,multiplier)
            return

        
        avatar.reparentTo(collisionEntry.getIntoNodePath())
        #self.__setToonUpright(avatar)
        h = self.barrel.getH(render)
        avatar.setPosHpr(0,0,0,h,0,0)
        messenger.send("hitCloud")

    
    def __setToonUpright(self, avatar, pos=None):
        if avatar:
            if self.inWater:
                avatar.setP(0)
                avatar.setR(0)
                return
            if not pos:
                pos = avatar.getPos(render)
            avatar.setPos(render,pos)
            avatar.loop('neutral')
            place = base.cr.playGame.getPlace()
            h = self.barrel.getH(render)
            p = Point3(self.vel[0],self.vel[1],self.vel[2])
            self.notify.debug("lookat = %s" % p)
            if hasattr(self, "cannon") and self.cannon:
                avatar.lookAt(self.cannon)
            avatar.setP(0)
            avatar.setR(0)
            avatar.setScale(1,1,1)

    def __calcToonImpact(self, trajectory):
        """__calcToonImpact(self, waterTower)
        calculate the result of the toon's trajectory
        check if the toon will land in the water, hit the tower, or hit
        the ground
        returns time of impact, what toon hits
        """
        # calculate when the toon will hit the ground
        # (assume absolute lowest point of terrain is above GROUND_PLANE_MIN)
        t_groundImpact = trajectory.checkCollisionWithGround(GROUND_PLANE_MIN)
        if t_groundImpact >= trajectory.getStartTime():
            # toon will hit the ground (...he'd best...)
            return t_groundImpact, self.HIT_GROUND
        else:
            # toon won't hit the ground??
            self.notify.error("__calcToonImpact: toon never impacts ground?")
            # return something
            return 0.0, self.HIT_GROUND

    def __calcHitTreasures(self, trajectory):
        # find the doIds of the treasures
        # should we do this everytime?  probably, since
        # some treasures might have been deleted or picked up
        estate = self.cr.doId2do.get(self.estateId)
        self.hitTreasures = []
        if estate:
            doIds = estate.flyingTreasureId
            for id in doIds:
                t = self.cr.doId2do.get(id)
                if t:
                    pos = t.pos
                    rad = 10.5
                    height = 10.0
                    t_impact = trajectory.checkCollisionWithCylinderSides(pos, rad, height)
                    if t_impact > 0:
                        self.hitTreasures.append([t_impact,t])
        del estate
        return None


    def __shootTask(self, task):
        base.playSfx(self.sndCannonFire)

        # show the drop shadow
        self.dropShadow.reparentTo(render)

        return Task.done


    def __smokeTask(self, task):
        # smoke cloud after the cannon fires
        self.smoke.reparentTo(self.barrel)
        self.smoke.setPos(0,6,-3)
        self.smoke.setScale(.5)
        # reparent to render, so the smoke doesn't get darker in the nighttime
        self.smoke.wrtReparentTo(render)
        track = Sequence(Parallel(LerpScaleInterval(self.smoke, .5, 3),
                                  LerpColorScaleInterval(self.smoke, .5, Vec4(2,2,2,0))),
                         Func(self.smoke.reparentTo, hidden),
                         Func(self.smoke.clearColorScale),
                         )
        track.start()
        return Task.done
                       

    def __flyTask(self, task):
        toon = task.info['toon']
        if toon.isEmpty():
            # we have deleted this toon, before this task has been ended.  end now
            self.__resetToonToCannon(self.av)
            return Task.done

        curTime = task.time + task.info['launchTime']
        # don't overshoot past the time of landing
        #t = min(curTime, task.info['timeOfImpact'])
        #let him keep going now
        t = curTime
        self.lastT = self.t
        self.t = t
        deltaT = self.t-self.lastT
        self.deltaT = deltaT
        
        #if t >= task.info['timeOfImpact']:
        #    # we are just flying into space at this point, end the fly task
        #    self.__resetToonToCannon(self.av)
        #    return Task.done

        if self.hitBumper:
            #self.notify.debug('in if self.hitBumper')
            pos = self.lastPos + self.lastVel * deltaT
            vel = self.lastVel
            self.lastVel += Vec3(0,0,-32.0)*deltaT
            self.lastPos = pos
            toon.setFluidPos(pos)
            lastH = toon.getH()
            toon.setH(lastH + deltaT*self.angularVel)
            view = 0
            #view = 2
            #self.notify.debug('new pos = %s' % pos)

        else:
            # get position
            pos = task.info['trajectory'].getPos(t)
            
            # update toon position
            toon.setFluidPos(pos)
            #print ("pos(%s,%s,%s)" % (pos[0],pos[1],pos[2]))

            # update drop shadow position
            shadowPos = Point3(pos)
            shadowPos.setZ(SHADOW_Z_OFFSET)
            self.dropShadow.setPos(shadowPos)
            #self.dropShadow.setX(shadowPos[0])
            #self.dropShadow.setY(shadowPos[1])
        
            # set the toon's tilt based on its velocity
            # h rotation is constant, and corresponds to the cannon's
            # z rotation (left to right)
            vel = task.info['trajectory'].getVel(t)
            run = math.sqrt((vel[0] * vel[0]) + (vel[1] * vel[1])) # TODO:
                                                               #precompute this
            rise = vel[2]
            theta = self.__toDegrees(math.atan(rise/run))
            toon.setHpr(self.cannon.getH(render),-90 + theta,0)
            view = 2

        if  pos.getZ() < -20 or pos.getZ() > 1000 :
            # we are just flying into space at this point, end the fly task
            self.notify.debug("stopping fly task toon.getZ()=%.2f" % pos.getZ())
            self.__resetToonToCannon(self.av)
            return Task.done            

        # try out some smoke
        # Create new ripple if its been long enough
        # since the last one
        #wakeDT = self.t - self.lastWakeTime
        #if (wakeDT > ToontownGlobals.WakeRunDelta or
        #    wakeDT > ToontownGlobals.WakeWalkDelta):
        #    self.av.getWake().createRipple(
        #        self.av.getZ(render), rate = 1, startFrame = 4)
        #    self.lastWakeTime = self.t

        #self.notify.debug('self.vel=%s' % self.vel)

        # move the camera above the toon, and look at him
        lookAt = task.info['toon'].getPos(render)
        hpr = task.info['toon'].getHpr(render)
        
        if self.localToonShooting:
            if view == 0:
                camera.wrtReparentTo(render)
            #camera.setPos(render, lookAt[0],50+lookAt[1],20+lookAt[2])
            #camera.setHpr(render, hpr[0], -10, hpr[2])
                camera.lookAt(lookAt)
            elif view == 1: 
                # third person pt of view
                camera.reparentTo(render)
                camera.setPos(render, 100, 100, 35.25)
                camera.lookAt(render, lookAt)
            elif view == 2:
                # fly behind the toon
                if hpr[1] > -90:
                    # set the camera behind the toon (in toon coordinates)
                    camera.setPos(0,0,-30)
                    # now make sure it is always above the toon
                    if camera.getZ() < lookAt[2]:
                        camera.setZ(render, lookAt[2]+10)
                    camera.lookAt(Point3(0,0,0))
        
        # should we play the whistling noise?
        #if task.info['haveWhistled'] == 0:
        #    if -vel[2] > WHISTLE_SPEED:
        #        if t < (task.info['timeOfImpact'] - 0.5):
        #            task.info['haveWhistled'] = 1
        #            base.playSfx(self.sndWhizz)

            # pickup treasures along the way
            self.__pickupTreasures(t)
        
        return Task.cont

    def __pickupTreasures(self, t):
        updatedList = []
        for tList in self.hitTreasures:
            if t > tList[0]:
                messenger.send(tList[1].uniqueName('entertreasureSphere'))
                self.notify.debug("hit something!")
            else:
                updatedList.append(tList)
        self.hitTreasures = updatedList

    def __resetToonToCannon(self, avatar):
        assert(self.notify.debug("__resetToonToCannon"))
        pos = None
        if not avatar:
            if self.avId:
                avatar = base.cr.doId2do.get(self.avId, None)
        if avatar:
            if self.cannon:
                avatar.reparentTo(self.cannon)
                avatar.setPos(2,-4,0)
                avatar.wrtReparentTo(render)
            self.__resetToon(avatar)
        
    def __resetToon(self, avatar, pos = None):
        self.notify.debug("__resetToon")
        if avatar:
            self.__stopCollisionHandler(avatar)
            self.__setToonUpright(avatar, pos)
            if self.localToonShooting:
                self.notify.debug("toon setting position to %s" % pos)
                if pos:
                    base.localAvatar.setPos(pos)
                camera.reparentTo(avatar)
                #place = base.cr.playGame.getPlace()
                #if place:
                #    place.setState('walk')
            self.b_setLanded()

    # ---------------------------------------
    # The contra code
    # ---------------------------------------
    def setActiveState(self, active):
        self.notify.debug("got setActiveState(%s)" % active)
        if active and not self.cannonsActive:
            self.activateCannons()
        elif not active and self.cannonsActive:
            self.deActivateCannons()
        
    def enterInit(self):
        self.nextKey = "up"
        self.nextState = "u1"
    def exitInit(self):
        pass

    def enteru1(self):
        self.nextKey = "up"
        self.nextState = "u2"
    def exitu1(self):
        pass

    def enteru2(self):
        self.nextKey = "down"
        self.nextState = "d3"
    def exitu2(self):
        pass

    def enterd3(self):
        self.nextKey = "down"
        self.nextState = "d4"
    def exitd3(self):
        pass    

    def enterd4(self):
        self.nextKey = "left"
        self.nextState = "l5"
    def exitd4(self):
        pass    

    def enterl5(self):
        self.nextKey = "right"
        self.nextState = "r6"
    def exitl5(self):
        pass    

    def enterr6(self):
        self.nextKey = "left"
        self.nextState = "l7"
    def exitr6(self):
        pass    

    def enterl7(self):
        self.nextKey = "right"
        self.nextState = "r8"
    def exitl7(self):
        pass    

    def enterr8(self):
        self.nextKey = None
        self.nextState = ""
        self.codeFSM.request('acceptCode')
    def exitr8(self):
        pass    

    def enterAcceptCode(self):
        if not self.cannonsActive:
            self.activateCannons()
            self.sendUpdate("setActive", [1])
        else:
            self.deActivateCannons()
            self.sendUpdate("setActive", [0])
        self.codeFSM.request('init')

    def exitAcceptCode(self):
        pass

    def enterFinal(self):
        pass
    def exitFinal(self):
        pass
    
    def handleCodeKey(self, key):
        if self.nextKey and self.nextState:
            if key == self.nextKey:
                self.codeFSM.request(self.nextState)
            else:
                self.codeFSM.request('init')

    def incrementPinballInfo( self,  score,  multiplier):
        #import pdb; pdb.set_trace()
        if base.localAvatar.doId == self.avId:

            self.curPinballScore += score
            self.curPinballMultiplier += multiplier

            #self.notify.debug('------------------------------')
            self.notify.debug('score =%d multiplier=%d  curscore=%d curMult=%d' %
                              (score, multiplier, self.curPinballScore,
                               self.curPinballMultiplier))
            self.d_setPinballInfo()

    def d_setPinballInfo(self):
        #self.notify.debug('----------------------------------------------------------')
        self.notify.debug('d_setPinballInfo %d %d' % (self.curPinballScore, self.curPinballMultiplier))
        target = base.cr.doId2do[self.targetId]
        target.b_setCurPinballScore(self.avId, self.curPinballScore, self.curPinballMultiplier)

    def createBlock(self, collisionName = None):
        """
        returns a nodepath to a square block with collision
        """
        gFormat = GeomVertexFormat.getV3c4()
        myVertexData = GeomVertexData("Cannon bumper vertices", gFormat, Geom.UHDynamic)
        vertexWriter = GeomVertexWriter(myVertexData, "vertex")
        colorWriter = GeomVertexWriter(myVertexData, "color")
        
        vertices = [(-1,1,1), #back left top
                    (1,1,1), #back right top
                    (1,-1,1), #front right top
                    (-1,-1,1), #front left top
                    (-1,1,-1), #back left bottom
                    (1,1,-1), #back right bottom
                    (1,-1,-1), #front right botom
                    (-1,-1,-1), #front left bottom
                    ]
        
        colors = [ (0,0,0,1),
                   (0,0,1,1),
                   (0,1,0,1),
                   (0,1,1,1),
                   (1,0,0,1),
                   (1,0,1,1),
                   (1,1,0,1),
                   (1,1,1,1)
                   ]
        
        
        faces = [ (0,2,1), #top
                  (0,3,2), #top
                  (7,4,5), #bottom
                  (6,7,5), #bottom
                  (2,3,7), #front
                  (2,7,6), #front
                  (4,0,1), #back
                  (5,4,1), #back
                  (0,4,3), #left
                  (3,4,7), #left
                  (1,2,6), #right
                  (1,6,5) # right
                   ]
        

        quads = [ (3,2,1,0), # top
                  (4,5,6,7), #bottom
                  (3,7,6,2), #Front
                  (0,1,5,4), #back
                  (0,4,7,3), #left
                  (1,2,6,5) # right
                  ]
         
        for i in range(len(vertices)):
            #vertex = myVertices[i]
            vertex =vertices[i]
            vertexWriter.addData3f(vertex[0], vertex[1], vertex[2])
            colorWriter.addData4f( *colors[i])
             
        cubeGeom=Geom(myVertexData)            
        tris = GeomTriangles(Geom.UHDynamic)
        tris.makeIndexed()
             
        for face in faces:
            for vertex in face:
                tris.addVertex(vertex)

        tris.closePrimitive()
        cubeGeom.addPrimitive(tris)                   
         
        cubeGN=GeomNode("cubeGeom")
        cubeGN.addGeom(cubeGeom)
         
        if collisionName:
            colNode = CollisionNode(collisionName)                  
        else:
            colNode = CollisionNode("cubeCollision")                  
            
        for quad in quads:
            #for i in range(1):
            #quad = quads[i]
            colQuad = CollisionPolygon(Point3(*vertices[quad[0]]),
                                       Point3(*vertices[quad[1]]),
                                       Point3(*vertices[quad[2]]),
                                       Point3(*vertices[quad[3]])
                                       )
             
            colQuad.setTangible(0)
            colNode.addSolid(colQuad)

        block = NodePath('cubeNodePath')
        block.attachNewNode(cubeGN)
        block.attachNewNode(colNode)
        return block


    def loadCannonBumper(self):
        #self.cannonBumper = self.createBlock('collision_cannon_bumper')
        self.cannonBumper = loader.loadModel("phase_5.5/models/estate/bumper_cloud")
        self.cannonBumper.reparentTo(self.nodePath)
        self.cannonBumper.setScale(4.0)
        # todo: get color of actual owner!
        #self.cannonBumper.setColorScale(base.localAvatar.find("**/neck").getColor())
        # for now: light blue
        self.cannonBumper.setColor(0.52, 0.80, 0.98, 1)
        # change the collision node name
        colCube = self.cannonBumper.find("**/collision")
        colCube.setName("cloudSphere-0")
        self.bumperCol = colCube
        
        self.notify.debug('------------self.cannonBumper.setPos %.2f %.2f %.2f' %
                          (ToontownGlobals.PinballCannonBumperInitialPos[0],
                          ToontownGlobals.PinballCannonBumperInitialPos[1],
                          ToontownGlobals.PinballCannonBumperInitialPos[2]))
                          
        self.cannonBumper.setPos(*ToontownGlobals.PinballCannonBumperInitialPos)
        
    def __bumperKeyPressed(self):

        self.notify.debug('__bumperKeyPressed')
        self.__bumperPressed()

    def __bumperPressed(self):
        """
        Only allow it once, move the cannon bumper somewhere else
        """
        renderPos = base.localAvatar.getPos(render)
        if renderPos[2] > 15.0:
            if not self.localToonShooting:
                return
            self.ignore(self.BUMPER_KEY)
            self.ignore(self.BUMPER_KEY2)
    
    
            self.notify.debug('renderPos %s' % renderPos)
            cannonPos = base.localAvatar.getPos(self.nodePath)
            self.notify.debug('cannonPos %s' % cannonPos)
    
            #set the new bumper position immediately, then tell the ai
            self.setCannonBumperPos(cannonPos[0], cannonPos[1], cannonPos[2])
            self.requestBumperMove(cannonPos[0], cannonPos[1], cannonPos[2])

    def requestBumperMove(self, x, y ,z):
        self.sendUpdate('requestBumperMove', [x,y,z])

    def setCannonBumperPos(self, x, y ,z):
        self.notify.debug('------------setCannonBumperPos %f %f %f' % (x,y,z))
        self.cannonBumper.setPos(x,y,z)
        self.bumperCol.setCollideMask(BitMask32.allOff())
        taskMgr.doMethodLater(0.25, self.turnOnBumperCollision, self.uniqueName("BumperON"))
        
        
    def turnOnBumperCollision(self, whatever = 0):
        if self.bumperCol:
            self.bumperCol.setCollideMask(ToontownGlobals.WallBitmask)
        
        
