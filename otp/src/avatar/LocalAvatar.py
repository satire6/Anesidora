"""LocalAvatar module: contains the LocalAvatar class"""

from pandac.PandaModules import *
from libotp import Nametag, WhisperPopup
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from pandac.PandaModules import *

import Avatar
from direct.controls import ControlManager
import DistributedAvatar
from direct.task import Task
import PositionExaminer
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
import math
import string
#import whrandom
import random
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from direct.gui import DirectGuiGlobals
from otp.otpbase import OTPLocalizer

from direct.controls.GhostWalker import GhostWalker
from direct.controls.GravityWalker import GravityWalker
from direct.controls.ObserverWalker import ObserverWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.SwimWalker import SwimWalker
from direct.controls.TwoDWalker import TwoDWalker
if __debug__:
    from direct.controls.DevWalker import DevWalker

class LocalAvatar(DistributedAvatar.DistributedAvatar,
                  DistributedSmoothNode.DistributedSmoothNode):
    """
    This is the local version of a distributed avatar.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("LocalAvatar")

    wantDevCameraPositions = base.config.GetBool('want-dev-camera-positions', 0)
    wantMouse = base.config.GetBool('want-mouse', 0)

    sleepTimeout = base.config.GetInt('sleep-timeout', 120)
    swimTimeout = base.config.GetInt('afk-timeout', 600)

    __enableMarkerPlacement = base.config.GetBool('place-markers', 0)

    acceptingNewFriends = base.config.GetBool('accepting-new-friends', 1)

    # special methods
    def __init__(self, cr, chatMgr, talkAssistant = None, passMessagesThrough = False):
        """
        cr is a ClientRepository
        """
        try:
            self.LocalAvatar_initialized
            return
        except:
            pass

        self.LocalAvatar_initialized = 1
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)

        # Set up the collision traverser:
        self.cTrav = CollisionTraverser("base.cTrav")
        base.pushCTrav(self.cTrav)
        self.cTrav.setRespectPrevTransform(1)

        self.avatarControlsEnabled=0
        self.controlManager = ControlManager.ControlManager(True, passMessagesThrough)

        # Set up collisions:
        self.initializeCollisions()
        # Set up camera:
        self.initializeSmartCamera()
        self.cameraPositions = []
        # Set animation speed:
        self.animMultiplier = 1.0

        # How long should the button be held to start running:
        self.runTimeout = 2.5

        # Custom SpeedChat messages.
        self.customMessages = []

        # MPG Create chat manager in the child class
        self.chatMgr = chatMgr
        base.talkAssistant = talkAssistant

        # Initially, we have no common chat flags.  The server
        # might or might not assign us some special flags based on
        # our "green" from login.
        self.commonChatFlags = 0
        self.garbleChat = 1

        # This is normally 1, but some funny states may set this
        # to 0 to forbid teleporting away even though we are in
        # walk mode.
        self.teleportAllowed = 1

        # This should be set when the local avatar is placed in movie
        # mode. This is especially true for the pet movies since we
        # want to allow the PetAvatarPanel to pop up if a player clicks
        # on the pet while the avatar is locked down. We want to keep the
        # functionality consistent, but disable any actions that the
        # player may take.
        self.lockedDown = 0

        self.isPageUp=0
        self.isPageDown=0

        # Let derived classes fill these in
        self.soundRun = None
        self.soundWalk = None

        if __debug__:
            if base.config.GetBool('want-dev-walker', 1):
                self.accept('f4', self.useDevControls)
                self.accept('f4-up', self.useWalkControls)

        # Is the toon sleeping?
        self.sleepFlag = 0

        # Is the toon disguised?
        self.isDisguised = 0

        # is the toon moving?
        self.movingFlag = 0
        self.swimmingFlag = 0


        self.lastNeedH = None

        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendOffline', self.__friendOffline)
        self.accept('clickedWhisper', self.clickedWhisper)
        self.accept('playerOnline', self.__playerOnline)
        self.accept('playerOffline', self.__playerOffline)

        # We listen for this event all the time, not just while
        # we're sleeping.  This event serves not just to wake us
        # up, but also to keep us from going to sleep!
        self.sleepCallback = None
        self.accept('wakeup', self.wakeUp)

        self.jumpLandAnimFixTask = None

        self.fov = OTPGlobals.DefaultCameraFov
        self.accept("avatarMoving", self.clearPageUpDown)

        # And our nametag2d probably shouldn't be visible.
        # On reflection, it *should* be visible.  There are times
        # when the localToon is off camera--for instance, when
        # we're looking in the sticker book, or watching a
        # movie--and it would be nice to see our own offscreen
        # chat messages.  However, we don't want to see an arrow
        # pointing to our own name, so instead of hiding the whole
        # thing, we just set it to only show our chat messages.
        self.nametag2dNormalContents = Nametag.CSpeech
        self.showNametag2d()

        # Nor is it pickable.  If we wanted to make it pickable,
        # we only have to change this flag and also add a hook to
        # call self.clickedNametag.
        self.setPickable(0)

    def useSwimControls(self):
        self.controlManager.use("swim", self)

    def useGhostControls(self):
        self.controlManager.use("ghost", self)

    def useWalkControls(self):
        self.controlManager.use("walk", self)

    def useTwoDControls(self):
        self.controlManager.use("twoD", self)

    if __debug__:
        def useDevControls(self):
            self.controlManager.use("dev", self)

    def isLockedDown(self):
        return self.lockedDown

    def lock(self):
        if (self.lockedDown == 1):
            self.notify.debug("lock() - already locked!")
        self.lockedDown = 1

    def unlock(self):
        if (self.lockedDown == 0):
            self.notify.debug("unlock() - already unlocked!")
        self.lockedDown = 0

    def isInWater(self):
        return (self.getZ(render) <= 0.0)

    def isTeleportAllowed(self):
        """
        Returns true if the local avatar is currently allowed to
        teleport away somewhere, false otherwise.
        """
        return self.teleportAllowed and not self.isDisguised

    def setTeleportAllowed(self, flag):
        """
        Sets the flag that indicates whether the toon is allowed to
        teleport away, even if we are in walk mode.  Usually this is
        1, but it may be set to 0 in unusual cases
        """
        self.teleportAllowed = flag
        self.refreshOnscreenButtons()

    def sendFriendsListEvent(self):
        self.wakeUp()
        messenger.send("openFriendsList")

    def delete(self):
        try:
            self.LocalAvatar_deleted
            return
        except:
            self.LocalAvatar_deleted = 1
        self.ignoreAll()
        self.stopJumpLandTask()
        taskMgr.remove('shadowReach')

        base.popCTrav()

        # Precaution in-case the smart camera is being lerped.
        taskMgr.remove('posCamera')

        self.disableAvatarControls()
        self.stopTrackAnimToSpeed()
        self.stopUpdateSmartCamera()
        self.shutdownSmartCamera()
        self.deleteCollisions()
        self.controlManager.delete()
        self.physControls = None
        del self.controlManager
        self.positionExaminer.delete()
        del self.positionExaminer
        taskMgr.remove(self.uniqueName("walkReturnTask"))
        self.chatMgr.delete()
        del self.chatMgr
        del self.soundRun
        del self.soundWalk
        if hasattr(self, "soundWhisper"):
            del self.soundWhisper

        DistributedAvatar.DistributedAvatar.delete(self)

    def shadowReach(self, state):
        if  base.localAvatar.shadowPlacer:
            base.localAvatar.shadowPlacer.lifter.setReach(
                base.localAvatar.getAirborneHeight()+4.0)
        return Task.cont

    def wantLegacyLifter(self):
        return False

    def setupControls(
            self,
            avatarRadius = 1.4,
            floorOffset = OTPGlobals.FloorOffset,
            reach = 4.0,
            wallBitmask = OTPGlobals.WallBitmask,
            floorBitmask = OTPGlobals.FloorBitmask,
            ghostBitmask = OTPGlobals.GhostBitmask,
            ):
        """
        Set up the local avatar for collisions
        """
        if 0:
            # Physics Walker:
            physControls=PhysicsWalker(gravity = -32.1740 * 2.0) # * 2.0 is a hack
            physControls.setWallBitMask(wallBitmask)
            physControls.setFloorBitMask(floorBitmask)
            physControls.initializeCollisions(self.cTrav, self,
                    avatarRadius, floorOffset, reach)
            physControls.setAirborneHeightFunc(self.getAirborneHeight)
            self.controlManager.add(physControls, "phys")
            self.physControls = physControls

        # Avatar Gravity Walker:
        walkControls=GravityWalker(legacyLifter=self.wantLegacyLifter())
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.initializeCollisions(self.cTrav, self,
                avatarRadius, floorOffset, reach)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(walkControls, "walk")
        self.physControls = walkControls

        # Avatar 2D Scroller Walker:
        twoDControls = TwoDWalker()
        twoDControls.setWallBitMask(wallBitmask)
        twoDControls.setFloorBitMask(floorBitmask)
        twoDControls.initializeCollisions(self.cTrav, self,
                avatarRadius, floorOffset, reach)
        twoDControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(twoDControls, "twoD")

        # Avatar swimming:
        swimControls=SwimWalker()
        swimControls.setWallBitMask(wallBitmask)
        swimControls.setFloorBitMask(floorBitmask)
        swimControls.initializeCollisions(self.cTrav, self,
                avatarRadius, floorOffset, reach)
        swimControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(swimControls, "swim")

        # Ghost mode (moving furniture, for example):
        ghostControls=GhostWalker()
        ghostControls.setWallBitMask(ghostBitmask)
        ghostControls.setFloorBitMask(floorBitmask)
        ghostControls.initializeCollisions(self.cTrav, self,
                avatarRadius, floorOffset, reach)
        ghostControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(ghostControls, "ghost")

        # Observer mode (following ai avatars, for example):
        observerControls=ObserverWalker()
        observerControls.setWallBitMask(ghostBitmask)
        observerControls.setFloorBitMask(floorBitmask)
        observerControls.initializeCollisions(self.cTrav, self,
                avatarRadius, floorOffset, reach)
        observerControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(observerControls, "observer")

        # Develpment Debug Walker (fly, walk through walls, run, etc.):
        if __debug__:
                devControls=DevWalker()
                devControls.setWallBitMask(wallBitmask)
                devControls.setFloorBitMask(floorBitmask)
                devControls.initializeCollisions(self.cTrav, self,
                        avatarRadius, floorOffset, reach)
                devControls.setAirborneHeightFunc(self.getAirborneHeight)
                self.controlManager.add(devControls, "dev")

        # Default to the standard avatar walk controls:
        self.controlManager.use("walk", self)
        # Start out disabled otherwise controls will be on
        # while you are still not in walk mode
        self.controlManager.disable()

    # An override of DistributedAvatar's initializeCollisions()
    def initializeCollisions(self):
        """
        Set up the local avatar for collisions
        """
        self.setupControls()

        # HACK: This should be temporary:

    def deleteCollisions(self):
        self.controlManager.deleteCollisions()
        self.ignore("entero157")
        del self.cTrav

    def initializeSmartCameraCollisions(self):
        # SMART-CAMERA STUFF

        # set up the smart camera's collision traverser
        # we need this because normal collisions get handled just before
        # rendering. using the normal collision mechanisms would introduce
        # one frame of lag in the smart camera, allowing the camera to pop
        # through walls momentarily.
        self.ccTrav = CollisionTraverser("LocalAvatar.ccTrav")

        # Set up the camera obstruction test line segment
        # This is a line segment from the visibility point to the ideal
        # camera location
        self.ccLine = CollisionSegment(0.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        self.ccLineNode = CollisionNode('ccLineNode')
        self.ccLineNode.addSolid(self.ccLine)
        self.ccLineNodePath = self.attachNewNode(self.ccLineNode)
        self.ccLineBitMask = OTPGlobals.CameraBitmask
        self.ccLineNode.setFromCollideMask(self.ccLineBitMask)
        self.ccLineNode.setIntoCollideMask(BitMask32.allOff())

        # set up camera collision mechanism
        self.camCollisionQueue = CollisionHandlerQueue()

        # set up camera obstruction collision reciever
        self.ccTrav.addCollider(self.ccLineNodePath, self.camCollisionQueue)

        ## set up a sphere around camera to keep it away from the walls

        # make the sphere
        # the sphere attribs will be calculated later
        self.ccSphere = CollisionSphere(0,0,0,1)
        self.ccSphereNode = CollisionNode('ccSphereNode')
        self.ccSphereNode.addSolid(self.ccSphere)
        self.ccSphereNodePath = base.camera.attachNewNode(self.ccSphereNode)
        self.ccSphereNode.setFromCollideMask(OTPGlobals.CameraBitmask)
        self.ccSphereNode.setIntoCollideMask(BitMask32.allOff())

        # attach a pusher to the sphere
        self.camPusher = CollisionHandlerPusher()
        # Do this when the camera gets activated
        #self.cTrav.addCollider(self.ccSphereNodePath, self.camPusher)
        self.camPusher.addCollider(self.ccSphereNodePath, base.camera)

        # Set a special mode on the pusher so that it doesn't get
        # fooled by walls facing away from the toon.
        self.camPusher.setCenter(self)

        ####
        # create another traverser with a camera pusher
        # sphere so that we can push the camera at will
        self.ccPusherTrav = CollisionTraverser("LocalAvatar.ccPusherTrav")

        # make the sphere
        self.ccSphere2 = self.ccSphere
        self.ccSphereNode2 = CollisionNode('ccSphereNode2')
        self.ccSphereNode2.addSolid(self.ccSphere2)
        self.ccSphereNodePath2 = base.camera.attachNewNode(self.ccSphereNode2)
        self.ccSphereNode2.setFromCollideMask(OTPGlobals.CameraBitmask)
        self.ccSphereNode2.setIntoCollideMask(BitMask32.allOff())

        # attach a pusher to the sphere
        self.camPusher2 = CollisionHandlerPusher()
        self.ccPusherTrav.addCollider(self.ccSphereNodePath2, self.camPusher2)
        self.camPusher2.addCollider(self.ccSphereNodePath2, base.camera)

        # Set a special mode on the pusher so that it doesn't get
        # fooled by walls facing away from the toon.
        self.camPusher2.setCenter(self)

        # create a separate node for the camera's floor-detection ray
        # If we just parented the ray to the camera, it would rotate
        # with the camera and no longer be facing straight down.
        self.camFloorRayNode = self.attachNewNode("camFloorRayNode")

        # set up camera collision mechanisms

        # Set up the "cameraman" collison ray
        # This is a ray cast from the camera down to detect floor polygons
        self.ccRay = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRayNode = CollisionNode('ccRayNode')
        self.ccRayNode.addSolid(self.ccRay)
        self.ccRayNodePath = self.camFloorRayNode.attachNewNode(self.ccRayNode)
        self.ccRayBitMask = OTPGlobals.FloorBitmask
        self.ccRayNode.setFromCollideMask(self.ccRayBitMask)
        self.ccRayNode.setIntoCollideMask(BitMask32.allOff())

        self.ccTravFloor = CollisionTraverser("LocalAvatar.ccTravFloor")

        self.camFloorCollisionQueue = CollisionHandlerQueue()
        self.ccTravFloor.addCollider(self.ccRayNodePath,
                                     self.camFloorCollisionQueue)

        self.ccTravOnFloor = CollisionTraverser("LocalAvatar.ccTravOnFloor")

        # set up another ray to generate on-floor/off-floor events
        self.ccRay2 = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRay2Node = CollisionNode('ccRay2Node')
        self.ccRay2Node.addSolid(self.ccRay2)
        self.ccRay2NodePath = self.camFloorRayNode.attachNewNode(
            self.ccRay2Node)
        self.ccRay2BitMask = OTPGlobals.FloorBitmask
        self.ccRay2Node.setFromCollideMask(self.ccRay2BitMask)
        self.ccRay2Node.setIntoCollideMask(BitMask32.allOff())

        # dummy node for CollisionHandlerFloor to move
        self.ccRay2MoveNodePath = hidden.attachNewNode('ccRay2MoveNode')

        #import pdb; pdb.set_trace()
        self.camFloorCollisionBroadcaster = CollisionHandlerFloor()
        self.camFloorCollisionBroadcaster.setInPattern("on-floor")
        self.camFloorCollisionBroadcaster.setOutPattern("off-floor")
        # detect the floor with ccRay2, and move a dummy node
        self.camFloorCollisionBroadcaster.addCollider(
            self.ccRay2NodePath, self.ccRay2MoveNodePath)

    def deleteSmartCameraCollisions(self):
        del self.ccTrav
        del self.ccLine

        del self.ccLineNode
        self.ccLineNodePath.removeNode()
        del self.ccLineNodePath
        del self.camCollisionQueue

        del self.ccRay
        del self.ccRayNode
        self.ccRayNodePath.removeNode()
        del self.ccRayNodePath

        del self.ccRay2
        del self.ccRay2Node
        self.ccRay2NodePath.removeNode()
        del self.ccRay2NodePath
        self.ccRay2MoveNodePath.removeNode()
        del self.ccRay2MoveNodePath

        del self.ccTravOnFloor
        del self.ccTravFloor
        del self.camFloorCollisionQueue
        del self.camFloorCollisionBroadcaster

        del self.ccSphere
        del self.ccSphereNode
        self.ccSphereNodePath.removeNode()
        del self.ccSphereNodePath

        del self.camPusher
        del self.ccPusherTrav

        del self.ccSphere2
        del self.ccSphereNode2
        self.ccSphereNodePath2.removeNode()
        del self.ccSphereNodePath2

        del self.camPusher2

    def collisionsOff(self):
        self.controlManager.collisionsOff()

    def collisionsOn(self):
        self.controlManager.collisionsOn()

    def recalcCameraSphere(self):
        """ this will adjust the smart camera for new FOV/near plane settings"""
        # get the near-plane params
        nearPlaneDist = base.camLens.getNear()
        hFov = base.camLens.getHfov()
        vFov = base.camLens.getVfov()

        hOff = nearPlaneDist * math.tan(deg2Rad(hFov/2.))
        vOff = nearPlaneDist * math.tan(deg2Rad(vFov/2.))

        # average the points together to get the sphere center
        camPnts = [Point3( hOff, nearPlaneDist,  vOff),
                   Point3(-hOff, nearPlaneDist,  vOff),
                   Point3( hOff, nearPlaneDist, -vOff),
                   Point3(-hOff, nearPlaneDist, -vOff),
                   Point3(0.0, 0.0, 0.0)]

        avgPnt = Point3(0.0,0.0,0.0)
        for camPnt in camPnts:
            avgPnt = avgPnt + camPnt
        avgPnt = avgPnt / len(camPnts)

        #calculate a minimum bounding sphere
        sphereRadius = 0.0
        for camPnt in camPnts:
            dist = Vec3(camPnt - avgPnt).length()
            if (dist > sphereRadius):
                sphereRadius = dist

        # set the new sphere params
        avgPnt = Point3(avgPnt)
        self.ccSphereNodePath.setPos(avgPnt)
        self.ccSphereNodePath2.setPos(avgPnt)
        # note that this also changes ccSphere2 (which is what we want)
        self.ccSphere.setRadius(sphereRadius)

    def putCameraFloorRayOnAvatar(self):
        """place the camera ray on the avatar itself"""
        self.camFloorRayNode.setPos(self, 0,0,5)

    def putCameraFloorRayOnCamera(self):
        """place the camera ray in the center of the camera's collision
        sphere"""
        self.camFloorRayNode.setPos(self.ccSphereNodePath, 0,0,0)

    #def collidedWithWall(self, collisionEntry):
    #    base.playSfx(self.soundWalkCollision)

    # set-up
    def attachCamera(self):
        """
        Make the mouse drive the toon around and make the
        camera go to its viewpoint
        """
        # attach the camera
        camera.reparentTo(self)
        base.enableMouse()
        base.setMouseOnNode(self.node())

        # Do we want mouse navigation?
        self.ignoreMouse=not self.wantMouse

        self.setWalkSpeedNormal()

    def detachCamera(self):
        base.disableMouse()

    def stopJumpLandTask(self):
        if self.jumpLandAnimFixTask:
            self.jumpLandAnimFixTask.remove()
            self.jumpLandAnimFixTask = None

    if 1: # HACK: These are to fix the anmation aftar a jump -- the anim fsm needs to be redone so these are not necessary
        def jumpStart(self):
            if not self.sleepFlag and self.hp > 0:
                self.b_setAnimState("jumpAirborne", 1.0)
                self.stopJumpLandTask()

        def returnToWalk(self, task):
            # Please help this hack:
            if self.sleepFlag:
                state = "Sleep"
            elif self.hp > 0:
                state = "Happy"
            else:
                state = "Sad"
            self.b_setAnimState(state, 1.0)
            return Task.done

        def jumpLandAnimFix(self, jumpTime):
            if self.playingAnim != "run" and self.playingAnim != "walk":
                # We have to be sure to remove this task (along with
                # any other task or doLater we spawn) in the delete()
                # method, so it will be stopped should we get a sudden
                # disconnect from the server.
                return taskMgr.doMethodLater(
                    jumpTime, self.returnToWalk,
                    self.uniqueName("walkReturnTask"))

        def jumpHardLand(self):
            if self.allowHardLand():
                self.b_setAnimState("jumpLand", 1.0)
                self.stopJumpLandTask()
                self.jumpLandAnimFixTask = self.jumpLandAnimFix(1.0)

            # Send an additional position report every time we land so
            # the smoother won't miss the instants when a distributed
            # toon is on the floor.
            if self.d_broadcastPosHpr:
                self.d_broadcastPosHpr()

        def jumpLand(self):
            self.jumpLandAnimFixTask = self.jumpLandAnimFix(0.01)

            # Send an additional position report every time we land so
            # the smoother won't miss the instants when a distributed
            # toon is on the floor.
            if self.d_broadcastPosHpr:
                self.d_broadcastPosHpr()

    def setupAnimationEvents(self):
        assert self.notify.debugStateCall(self)
        self.accept("jumpStart", self.jumpStart, [])
        self.accept("jumpHardLand", self.jumpHardLand, [])
        self.accept("jumpLand", self.jumpLand, [])

    def ignoreAnimationEvents(self):
        assert self.notify.debugStateCall(self)
        self.ignore("jumpStart")
        self.ignore("jumpHardLand")
        self.ignore("jumpLand")

    def allowHardLand(self):
        return ((not self.sleepFlag) and (self.hp > 0))

    def enableSmartCameraViews(self):
        self.accept("tab", self.nextCameraPos, [1])
        self.accept("shift-tab", self.nextCameraPos, [0])
        self.accept("page_up", self.pageUp)
        self.accept("page_down", self.pageDown)

    def disableSmartCameraViews(self):
        self.ignore("tab")
        self.ignore("shift-tab")
        self.ignore("page_up")
        self.ignore("page_down")
        self.ignore("page_down-up")

    def enableAvatarControls(self):
        """
        Activate the tab, page up, arrow keys, etc.
        """
        assert self.notify.debugStateCall(self)
        if self.avatarControlsEnabled:
            assert self.debugPrint("  avatarControlsEnabled=true")
            return
        self.avatarControlsEnabled=1
        self.setupAnimationEvents()
        self.controlManager.enable()

    def disableAvatarControls(self):
        """
        Ignore the tab, page up, arrow keys, etc.
        """
        assert self.notify.debugStateCall(self)
        if not self.avatarControlsEnabled:
            assert self.debugPrint("  avatarControlsEnabled=false")
            return
        self.avatarControlsEnabled=0
        self.ignoreAnimationEvents()
        self.controlManager.disable()
        self.clearPageUpDown()

    def setWalkSpeedNormal(self):
        self.controlManager.setSpeeds(
            OTPGlobals.ToonForwardSpeed,
            OTPGlobals.ToonJumpForce,
            OTPGlobals.ToonReverseSpeed,
            OTPGlobals.ToonRotateSpeed)

    def setWalkSpeedSlow(self):
        self.controlManager.setSpeeds(
            OTPGlobals.ToonForwardSlowSpeed,
            OTPGlobals.ToonJumpSlowForce,
            OTPGlobals.ToonReverseSlowSpeed,
            OTPGlobals.ToonRotateSlowSpeed)

    def pageUp(self):
        if not self.avatarControlsEnabled:
            return
        self.wakeUp()
        if not self.isPageUp:
            self.isPageDown = 0
            self.isPageUp = 1
            self.lerpCameraFov(70, 0.6)
            self.setCameraPositionByIndex(self.cameraIndex)
        else:
            self.clearPageUpDown()

    def pageDown(self):
        if not self.avatarControlsEnabled:
            return
        self.wakeUp()
        if not self.isPageDown:
            self.isPageUp = 0
            self.isPageDown = 1
            self.lerpCameraFov(70,0.6)
            self.setCameraPositionByIndex(self.cameraIndex)
        else:
            self.clearPageUpDown()

    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraFov(self.fov, 0.6)
            self.isPageDown = 0
            self.isPageUp = 0
            self.setCameraPositionByIndex(self.cameraIndex)

    def nextCameraPos(self, forward):
        """
        Cycle to the next camera position in cameraPositions list
        """
        if not self.avatarControlsEnabled:
            return
        self.wakeUp()
        self.__cameraHasBeenMoved = 1 # force the camera to process

        if (forward):
            self.cameraIndex += 1
            if (self.cameraIndex > (len(self.cameraPositions) - 1)):
                self.cameraIndex = 0
        else:
            self.cameraIndex -= 1
            if (self.cameraIndex < 0):
                self.cameraIndex = len(self.cameraPositions)-1
        self.setCameraPositionByIndex(self.cameraIndex)

    def initCameraPositions(self):
        camHeight = self.getClampedAvatarHeight()
        heightScaleFactor = (camHeight * 0.3333333333)

        # default LookAt point is at avatar's height, some distance in front
        defLookAt = Point3(0.0, 1.5, camHeight)

        scXoffset  = 3.0
        # high, places toon under speedchat
        scPosition = (Point3(scXoffset-1, -10.0, camHeight+5.0),
                      Point3(scXoffset, 2.0, camHeight))

        # In general, the camera shots move forward, until you're
        # looking back at the toon, and then switch to the furthest
        # behind the toon and then move forward again.
        #
        # (position, neutral lookat, up lookat, down lookat, disableSmartCam)
        self.cameraPositions = [
            #close shot
            (Point3(0.0, (-9.0 * heightScaleFactor), camHeight),        #pos
             defLookAt,                                                 #fwd
             Point3(0.0, camHeight, camHeight*4.0),                    #up
             Point3(0.0, camHeight, camHeight*-1.0),                    #down
             0,
             ),
            #fireworks shot
            #(Point3(0.0, (-8.0 * heightScaleFactor), camHeight/2.0),        #pos
            # Point3(0.0, 1.5, camHeight*1.8),
            # Point3(0.0, camHeight, camHeight*4.0),                    #up
            # Point3(0.0, camHeight, camHeight*-1.0),                    #down
            # 0,
            # ),
            #first-person
            (Point3(0.0, 0.5, camHeight),                               #pos
             defLookAt,                                                 #fwd
             Point3(0.0, camHeight, camHeight*1.33),                    #up
             Point3(0.0, camHeight, camHeight*0.66),                    #down
             1, # disable the smart cam
             ),
            # If you move this shot out of index 2, be sure to adjust
            # self.nextCameraPos() to match.  Maybe we should at a flag,
            # rather than use a hard coded index.
            # up shot:
            #(Point3(0.0, (1.0 * heightScaleFactor), camHeight),
            #    Point3(0.0, camHeight, camHeight*1.33)),
            #scPosition,
            #third person
            (Point3((5.7 * heightScaleFactor),                          #pos
                    (7.65 * heightScaleFactor),
                    (camHeight + 2.0)),
             Point3(0.0, 1.0, camHeight),
             Point3(0.0, 1.0, camHeight*4.0),
             Point3(0.0, 1.0, camHeight*-1.0),
             0,
             ),
            #extra wide shot
            (Point3(0.0, (-24.0 * heightScaleFactor), (camHeight + 4.0)),
             defLookAt,
             Point3(0.0, 1.5, camHeight * 4.0),
             Point3(0.0, 1.5, camHeight * -1.0),
             0,
             ),
            #wide shot (default)
            (Point3(0.0, (-12.0 * heightScaleFactor), (camHeight + 4.0)),
             defLookAt,
             Point3(0.0, 1.5, camHeight * 4.0),
             Point3(0.0, 1.5, camHeight * -1.0),
             0,
             ),
            ] + self.auxCameraPositions
        if self.wantDevCameraPositions:
            self.cameraPositions+=[
                # Overhead:
                (Point3(0.0, 0.0, camHeight*3),           #pos
                 Point3(0.0, 0.0, 0.0),                   #fwd
                 Point3(0.0, camHeight*2, 0.0),           #up
                 Point3(0.0, -camHeight*2, 0.0),          #down
                 1, # disable the smart cam
                 ),
                # From right:
                (Point3(camHeight*3, 0.0, camHeight),     #pos
                 Point3(0.0, 0.0, camHeight),             #fwd
                 Point3(0.0, camHeight, camHeight*1.1),  #up
                 Point3(0.0, camHeight, camHeight*0.9),  #down
                 1, # disable the smart cam
                 ),
                # Close-up of feet (good for physics testing):
                (Point3(camHeight*3, 0.0, 0.0),          #pos
                 Point3(0.0, 0.0, camHeight),             #fwd
                 Point3(0.0, camHeight, camHeight*1.1),  #up
                 Point3(0.0, camHeight, camHeight*0.9),  #down
                 1, # disable the smart cam
                 ),
                # Dramatic from floor (just for fun):
                #(Point3(1.5, 4.0, -2.0),     #pos
                # Point3(0.0, 0.0, camHeight),             #fwd
                # Point3(0.0, camHeight, camHeight*1.1),  #up
                # Point3(0.0, camHeight, camHeight*0.9),  #down
                # 1, # disable the smart cam
                # ),
                # From left:
                (Point3(-camHeight*3, 0.0, camHeight),     #pos
                 Point3(0.0, 0.0, camHeight),             #fwd
                 Point3(0.0, camHeight, camHeight*1.1),  #up
                 Point3(0.0, camHeight, camHeight*0.9),  #down
                 1, # disable the smart cam
                 ),
                # daisy gardens maze solver
                # This shot is too drastic to include in the release
                # It shows lots of behind the scenes areas
                (Point3(0.0, -60, 60),
                 (defLookAt + Point3(0, 15, 0)),
                 (defLookAt + Point3(0, 15, 0)),
                 (defLookAt + Point3(0, 15, 0)),
                 1, # disable the smart cam
                 ),
                # platformer
                # This is an attempt at a good general purpose
                # camera for jumping from moving platform to moving
                # platform.
                (Point3(0.0, -20, 20),
                 (defLookAt + Point3(0, 5, 0)),
                 (defLookAt + Point3(0, 5, 0)),
                 (defLookAt + Point3(0, 5, 0)),
                 1, # disable the smart cam
                 ),
                ]

    def addCameraPosition(self, camPos = None):
        if camPos == None:
            lookAtNP = self.attachNewNode('lookAt')
            lookAtNP.setPos(base.cam,0,1,0)
            lookAtPos = lookAtNP.getPos()
            camHeight = self.getClampedAvatarHeight()
            camPos = (base.cam.getPos(self),
                      lookAtPos,
                      Point3(0.0, 1.5, camHeight * 4.0),
                      Point3(0.0, 1.5, camHeight * -1.0),
                      1,
                      )
            lookAtNP.removeNode()
        self.auxCameraPositions.append(camPos)
        self.cameraPositions.append(camPos)

    def resetCameraPosition(self):
        self.cameraIndex = 0
        self.setCameraPositionByIndex(self.cameraIndex)

    def removeCameraPosition(self):
        if len(self.cameraPositions) > 1:
            camPos = self.cameraPositions[self.cameraIndex]
            if camPos in self.auxCameraPositions:
                self.auxCameraPositions.remove(camPos)
            if camPos in self.cameraPositions:
                self.cameraPositions.remove(camPos)
            self.nextCameraPos(1)

    def printCameraPositions(self):
        print '['
        for i in range(len(self.cameraPositions)):
            self.printCameraPosition(i)
            print ','
        print ']'

    def printCameraPosition(self, index):
        cp = self.cameraPositions[index]
        print '(Point3(%0.2f, %0.2f, %0.2f),' % (cp[0][0],cp[0][1],cp[0][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[1][0],cp[1][1],cp[1][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[2][0],cp[2][1],cp[2][2])
        print 'Point3(%0.2f, %0.2f, %0.2f),' % (cp[3][0],cp[3][1],cp[3][2])
        print '%d,' % cp[4]
        print ')',

    def posCamera(self, lerp, time):
        """posCamera(self, boolean, float)
        Move the camera to current position as indicated by
        getCompromiseCameraPos(). If lerp is true, lerp the
        motion over time seconds.
        """
        if not lerp:
            # load in the target params
            self.positionCameraWithPusher(
                self.getCompromiseCameraPos(), self.getLookAtPoint())
        else:
            camPos = self.getCompromiseCameraPos()

            # we've got a target camera location and look-at point
            # we need to figure out our desired HPR from this info

            # save current camera params
            savePos = camera.getPos()
            saveHpr = camera.getHpr()

            # load in the target params
            self.positionCameraWithPusher(camPos, self.getLookAtPoint())

            x = camPos[0]
            y = camPos[1]
            z = camPos[2]
            destHpr = camera.getHpr()
            h = destHpr[0]
            p = destHpr[1]
            r = destHpr[2]

            # restore camera params
            camera.setPos(savePos)
            camera.setHpr(saveHpr)

            taskMgr.remove("posCamera")
            camera.lerpPosHpr(x, y, z, h, p, r, time, task="posCamera")

    def getClampedAvatarHeight(self):
        return max(self.getHeight(), 3.0)

    # smart camera functions
    def getVisibilityPoint(self):
        """
        this returns the point that must be visible at all times
        """
        return Point3(0.0, 0.0, self.getHeight())

    # if there is ever a setVisibilityPoint function,
    # make it call self.updateSmartCameraCollisionLineSegment()
    # the way setIdealCameraPos() does

    def setLookAtPoint(self, la):
        """setLookAtPoint(self, Point3)
        setter for the point that the camera should look at
        NOTE: this is not necessarily the point that must be visible;
        see getVisibilityPoint() above
        """
        self.__curLookAt = Point3(la)

    def getLookAtPoint(self):
        """
        getter for the point the camera should look at
        """
        return Point3(self.__curLookAt)

    def setIdealCameraPos(self, pos):
        """setIdealCameraPos(self, Point3)
        setter for the location of where the camera would like to be
        """
        self.__idealCameraPos = Point3(pos)
        self.updateSmartCameraCollisionLineSegment()

    def getIdealCameraPos(self):
        """
        getter for the location of where the camera would like to be
        """
        return Point3(self.__idealCameraPos)

    def setCameraPositionByIndex(self, index):
        """setCameraPositionByIndex(self, int)
        sets the camera's ideal position, lookat point, etc.
        based on an index into the cameraPositions table
        """
        self.notify.debug('switching to camera position %s' % index)
        self.setCameraSettings(self.cameraPositions[index])

    def setCameraPosForPetInteraction(self):
        height = self.getClampedAvatarHeight()
        point = Point3(height*(7/3.), height*(-7/3.), height)

        self.prevIdealPos = self.getIdealCameraPos()
        # TODO: ADD look at functionality

        self.setIdealCameraPos(point)
        self.posCamera(1, 0.7)

    def unsetCameraPosForPetInteraction(self):
        assert hasattr(self, "prevIdealPos")
        self.setIdealCameraPos(self.prevIdealPos)
        del self.prevIdealPos
        self.posCamera(1, 0.7)

    def setCameraSettings(self, camSettings):
        self.setIdealCameraPos(camSettings[0])

        if ((self.isPageUp and self.isPageDown) or
            ((not self.isPageUp) and (not self.isPageDown))):
            self.__cameraHasBeenMoved = 1 # force the camera to process
            self.setLookAtPoint(camSettings[1])
        elif self.isPageUp:
            self.__cameraHasBeenMoved = 1 # force the camera to process
            self.setLookAtPoint(camSettings[2])
        elif self.isPageDown:
            self.__cameraHasBeenMoved = 1 # force the camera to process
            self.setLookAtPoint(camSettings[3])
        else:
            self.notify.error("This case should be impossible.")

        # this camera position may disable the smart camera
        self.__disableSmartCam = camSettings[4]

        if self.__disableSmartCam:
            # If the smart cam is disabled, put the ray right onto the toon.
            # Otherwise, the ray would be floating off in space somewhere
            # relative to the toon, generating events for some random piece
            # of floor, which is *very* bad for the HQ factories.
            self.putCameraFloorRayOnAvatar()

            # if we're disabling the smart camera, reset the floor Z offset
            self.cameraZOffset = 0.0

    def getCompromiseCameraPos(self):
        """
        returns the location of where the camera should be to avoid
        view obstructions
        """
        if (self.__idealCameraObstructed == 0):
            compromisePos = self.getIdealCameraPos()
        else:
            # interpolate the camera position between the
            # ideal camera position and the visibility point,
            # so that it is in front of the obstruction
            visPnt = self.getVisibilityPoint()
            idealPos = self.getIdealCameraPos()
            distance = Vec3(idealPos - visPnt).length()
            ratio = self.closestObstructionDistance / distance
            compromisePos = (idealPos * ratio) + (visPnt * (1 - ratio))
            # lift the camera up a bit, the closer it gets to the avatar
            liftMult = (1.0 - (ratio*ratio))
            compromisePos = Point3(compromisePos[0], compromisePos[1],
                                   compromisePos[2] + \
                                     ((self.getHeight()*0.4) * liftMult))
        compromisePos.setZ(compromisePos[2] + self.cameraZOffset)
        return compromisePos

    def updateSmartCameraCollisionLineSegment(self):
        """
        updates the camera's obstruction-detecting collision-line-segment
        """
        # set back end to ideal camera position
        pointB = self.getIdealCameraPos()
        # set front end to the visibility point, possibly pulled back a bit
        pointA = self.getVisibilityPoint()

        vectorAB = Vec3(pointB - pointA)
        lengthAB = vectorAB.length()

        """
        This doesn't seem to be necessary any more with the new physics

        # keep the line back from the toon a bit to avoid false
        # collisions with objects in front of the toon
        pullbackDist = 1.
        # if the distance between the ideal camera position and
        # the visibility point is less-than-or-equal-to the pullback
        # distance, don't bother pulling the line back from the toon
        if lengthAB > pullbackDist:
            pullbackVector = vectorAB * (pullbackDist / lengthAB)
            pointA = Point3(pointA + Point3(pullbackVector))
            lengthAB -= pullbackDist
            """

        # if pointA and pointB are too close, don't set the
        # segment endpoints. TODO: figure out something smarter.
        if lengthAB > 0.001:
            self.ccLine.setPointA(pointA)
            self.ccLine.setPointB(pointB)


    def initializeSmartCamera(self):
        self.__idealCameraObstructed = 0
        self.closestObstructionDistance = 0.0
        # create self.cameraIndex
        self.cameraIndex = 0
        self.auxCameraPositions = []
        self.cameraZOffset = 0.0

        self.__onLevelGround = 0
        self.__camCollCanMove = 0
        self.__geom = render

        self.__disableSmartCam = 0

        self.initializeSmartCameraCollisions()

        self._smartCamEnabled = False

    def shutdownSmartCamera(self):
        self.deleteSmartCameraCollisions()

    def setOnLevelGround(self, flag):
        self.__onLevelGround = flag

    def setCameraCollisionsCanMove(self, flag):
        self.__camCollCanMove = flag

    def setGeom(self, geom):
        # optimization 1
        self.__geom = geom

    def startUpdateSmartCamera(self, push = 1):
        """
        Spawn a task to update the smart camera every frame
        """
        if self._smartCamEnabled:
            LocalAvatar.notify.warning(
                'redundant call to startUpdateSmartCamera')
            return

        # We use getKey() as a temporary workaround for problem with
        # inherited ==.
        assert camera.getParent().getKey() == self.getKey(), \
               "camera must be parented to localToon before calling " \
               "startUpdateSmartCamera"

        self._smartCamEnabled = True

        # this flag is needed in cases where the camera is created before
        # it's put into the world. When the world suddenly shows up, we
        # jump to where the floor is and set this flag.
        self.__floorDetected = 0

        # In the smart camera update task,
        # we check to see if the camera has moved (wrt render) since
        # the last frame. If it hasn't, then the camera can't possibly
        # have become obstructed, since there is nothing that moves AND
        # obstructs the camera. We can use this knowledge to save some
        # CPU time.
        # When we move the camera explicitly to a new location (i.e. when
        # the user presses TAB), we need to override this check, by setting
        # this flag to a non-zero value.
        self.__cameraHasBeenMoved = 0

        # adjust for any changes to the camera FOV, etc.
        self.recalcCameraSphere()

        # initialize a whole buncha stuff
        # this would all be in initializeSmartCamera() except that self.height
        # is NOT set by the time initializeSmartCamera() is called
        self.initCameraPositions()
        self.setCameraPositionByIndex(self.cameraIndex)
        # slam the camera to its destination
        self.posCamera(0, 0.)
        # self.__instantaneousCamPos holds the current "instantaneous"
        # camera position. this variable is used to keep the camera moving
        # in a straight line towards its target position regardless of how
        # the camera is pushed off-track by its pusher.
        self.__instantaneousCamPos = camera.getPos()

        if push:

            # Activate the camera Pusher
            self.cTrav.addCollider(self.ccSphereNodePath, self.camPusher)
            # activate the on-floor ray
            self.ccTravOnFloor.addCollider(self.ccRay2NodePath,
                                           self.camFloorCollisionBroadcaster)
            self.__disableSmartCam = 0
        else:
            self.__disableSmartCam = 1

        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)

        taskName = self.taskName("updateSmartCamera")
        # remove any old
        taskMgr.remove(taskName)
        # spawn the new task
        # Set the priority somewhere between the collision task and
        # the rendering:
        taskMgr.add(self.updateSmartCamera, taskName, priority=47)

        self.enableSmartCameraViews()

    def stopUpdateSmartCamera(self):
        if not self._smartCamEnabled:
            LocalAvatar.notify.warning(
                'redundant call to stopUpdateSmartCamera')
            return
        self.disableSmartCameraViews()
        # Deactivate the cam pusher
        self.cTrav.removeCollider(self.ccSphereNodePath)
        # Deactivate the on-floor ray
        self.ccTravOnFloor.removeCollider(self.ccRay2NodePath)

        # make sure the floor-detection rays are right on top of the
        # toon (but watch out when we're shutting down and the toon has
        # already been deleted).
        if not base.localAvatar.isEmpty():
            self.putCameraFloorRayOnAvatar()

        taskName = self.taskName("updateSmartCamera")
        taskMgr.remove(taskName)
        self._smartCamEnabled = False

    def updateSmartCamera(self, task):
        if (not self.__camCollCanMove) and (not self.__cameraHasBeenMoved):
            if self.__lastPosWrtRender == camera.getPos(render):
                if self.__lastHprWrtRender == camera.getHpr(render):
                    return Task.cont

        self.__cameraHasBeenMoved = 0
        self.__lastPosWrtRender = camera.getPos(render)
        self.__lastHprWrtRender = camera.getHpr(render)

        self.__idealCameraObstructed = 0

        # if the smart cam is not disabled, check for view obstructions
        if not self.__disableSmartCam:
            # traverse the smart camera line segment collision tree
            self.ccTrav.traverse(self.__geom)
            # check if we have any collisions
            if (self.camCollisionQueue.getNumEntries() > 0):
                # just take the closest one
                self.camCollisionQueue.sortEntries()
                self.handleCameraObstruction(
                    self.camCollisionQueue.getEntry(0))

            # account for the floor
            # optimization 2
            if not self.__onLevelGround:
                self.handleCameraFloorInteraction()

        if not self.__idealCameraObstructed:
            # move the camera a bit
            self.nudgeCamera()

        if not self.__disableSmartCam:
            # tell the pusher to do its thing; keep the camera out of the walls
            self.ccPusherTrav.traverse(self.__geom)
            # make sure the on-floor ray is in the same spot as the camera
            self.putCameraFloorRayOnCamera()

        # now that the camera is in its final pos, do the on-floor traversal
        # (this generates the on-floor event)
        self.ccTravOnFloor.traverse(self.__geom)

        return Task.cont

    def positionCameraWithPusher(self, pos, lookAt):
        """positionCameraWithPusher(self, Point3, Point3)
        Positions the camera at pos, invokes the camera collision
        pusher, and orients the camera towards lookAt
        """
        # load in the target position
        camera.setPos(pos)
        # tell the pusher to do its thing
        self.ccPusherTrav.traverse(self.__geom)
        # look at the target lookAt point
        camera.lookAt(lookAt)

    def nudgeCamera(self):
        """
        Move the camera a little bit closer to its desired
        position as indicated by getCompromiseCameraPos().
        """
        # when the pos or hpr gets within this distance of the target,
        # set it and be done with it
        CLOSE_ENOUGH = 0.1

        # save current camera position
        curCamPos = self.__instantaneousCamPos
        curCamHpr = camera.getHpr()

        # get target camera params
        targetCamPos = self.getCompromiseCameraPos()
        targetCamLookAt = self.getLookAtPoint()

        posDone = 0
        if Vec3(curCamPos - targetCamPos).length() <= CLOSE_ENOUGH:
            camera.setPos(targetCamPos)
            posDone = 1

        ## do this here to get correct HPR
        #targetCamPos.setZ(targetCamPos[2] + self.cameraZOffset)

        ####################
        # we've got a target camera position and look-at point
        # we need to figure out our desired HPR from this info

        ## this is more correct, but slower; it takes the pusher's
        ## effect on the camera HPR into account
        #self.positionCameraWithPusher(targetCamPos, targetCamLookAt)

        # this is less correct but quicker; it ignores the influence
        # of the pusher on the camera HPR
        camera.setPos(targetCamPos)
        camera.lookAt(targetCamLookAt)
        ####################

        targetCamHpr = camera.getHpr()

        hprDone = 0
        if Vec3(curCamHpr - targetCamHpr).length() <= CLOSE_ENOUGH:
            # hpr was just set above
            hprDone = 1

        # can we bail early?
        if posDone and hprDone:
            return

        # move camera every frame according to this normalized percentage
        # of the distance between its current position and its
        # destination position
        # note: here, 'frame' == 1/30 of a second
        lerpRatio = 0.15

        # account for dt
        lerpRatio = 1 - pow((1-lerpRatio), globalClock.getDt()*30.0)

        # calc new instantaneous position
        # (this will be modified if necessary by collision pusher)
        self.__instantaneousCamPos = ((targetCamPos * lerpRatio) +
                                      (curCamPos * (1 - lerpRatio)))

        if self.__disableSmartCam or (not self.__idealCameraObstructed):
            # calc new hpr
            newHpr = (targetCamHpr * lerpRatio) + (curCamHpr * (1 - lerpRatio))
        else:
            # why lerp the hpr at all in smart-cam mode?
            # It was causing a sickening camera-turn
            newHpr = targetCamHpr

        # set new camera params
        camera.setPos(self.__instantaneousCamPos)
        camera.setHpr(newHpr)

    def popCameraToDest(self):
        # get new camera params
        newCamPos = self.getCompromiseCameraPos()
        newCamLookAt = self.getLookAtPoint()

        # set the new camera position with the pusher, so
        # that the HPR gets set correctly and we don't make
        # the player sick
        self.positionCameraWithPusher(newCamPos, newCamLookAt)

        # camera has been 'HOG' moved (Hand Of God)
        # so set the instantaneous position to the new
        # position, taking the pusher into account
        self.__instantaneousCamPos = camera.getPos()

    # camera obstruction detection handler
    def handleCameraObstruction(self, camObstrCollisionEntry):
        # calculate distance of obstruction
        collisionPoint = camObstrCollisionEntry.getSurfacePoint(
            self.ccLineNodePath)
        collisionVec = Vec3(collisionPoint - self.ccLine.getPointA())
        distance = collisionVec.length()

        self.__idealCameraObstructed = 1
        self.closestObstructionDistance = distance

        self.popCameraToDest()


    # camera's floor-ray collision handler
    def handleCameraFloorInteraction(self):
        # figure out a Z offset for the camera

        # first, update the position of the ray's parent node
        # if smart cam is disabled, we should not be moving the ray to
        # where the camera is
        assert not self.__disableSmartCam
        self.putCameraFloorRayOnCamera()

        # traverse the smart camera floor ray collision tree
        self.ccTravFloor.traverse(self.__geom)

        # we might be in here just for the sake of the collision traversal.
        # if so, bail out now.
        if self.__onLevelGround:
            return

        # check if we have any collisions
        if (self.camFloorCollisionQueue.getNumEntries() == 0):
            return

        # get the closest one
        self.camFloorCollisionQueue.sortEntries()
        camObstrCollisionEntry = self.camFloorCollisionQueue.getEntry(0)

        # the intersection point's Z is the floor's offset from the camera;
        # we would normally negate it to get the camera's offset from the floor
        # This is a negative number
        camHeightFromFloor = camObstrCollisionEntry.getSurfacePoint(
            self.ccRayNodePath)[2]

        # the "target height" is the camera's ideal height,
        # translated to the floor that's currently under it
        self.cameraZOffset = camera.getPos()[2] + camHeightFromFloor

        # Don't move down at all because when you are standing on a crate
        # you do not want the camera to be below your feet looking up at you
        if (self.cameraZOffset < 0):
            self.cameraZOffset = 0

        # if this is the first time we've hit floor, pop right to the
        # destination height
        if (self.__floorDetected == 0):
            self.__floorDetected = 1
            self.popCameraToDest()



    def lerpCameraFov(self, fov, time):
        """
        lerp the camera fov over time (used by the battle)
        """
        taskMgr.remove('cam-fov-lerp-play')
        oldFov = base.camLens.getHfov()
        # Fov values often have floating point precision errors
        if (abs(fov - oldFov) > 0.1):
            def setCamFov(fov):
                base.camLens.setFov(fov)
            self.camLerpInterval = LerpFunctionInterval(setCamFov,
                fromData=oldFov, toData=fov, duration=time,
                name='cam-fov-lerp')
            self.camLerpInterval.start()

    def setCameraFov(self, fov):
        """ Sets the camera to a particular fov and remembers this
        fov, so that things like page up and page down that
        temporarily change fov will restore it properly. """

        self.fov = fov
        if not (self.isPageDown or self.isPageUp):
            base.camLens.setFov(self.fov)

    def gotoNode(self, node, eyeHeight = 3):
        """gotoNode(self, NodePath node)

        Puts the avatar at a suitable point nearby, and facing, the
        indicated NodePath, whatever it might be.  This will normally
        be another avatar, as in Goto Friend.
        """
        # The only trick here is to find a place near the destination
        # point that is valid for us to stand.  This will be a point
        # that (a) has a ground, (b) is not already occupied, and (c)
        # is not behind a wall.
        #
        # To find such a suitable point, we'll consider a series of
        # possible points in order from most preferable to least
        # preferable, until we find a match.  This is admittedly a bit
        # expensive, but who really cares?  The PositionExaminer
        # object will examine each point for us.
        possiblePoints = (
            # Try some points in front of the avatar
            Point3(3, 6, 0),
            Point3(-3, 6, 0),

            Point3(6, 6, 0),
            Point3(-6, 6, 0),

            Point3(3, 9, 0),
            Point3(-3, 9, 0),
            Point3(6, 9, 0),
            Point3(-6, 9, 0),
            Point3(9, 9, 0),
            Point3(-9, 9, 0),

            # Try some points to the side
            Point3(6, 0, 0),
            Point3(-6, 0, 0),
            Point3(6, 3, 0),
            Point3(-6, 3, 0),
            Point3(9, 9, 0),
            Point3(-9, 9, 0),

            # Try some points further in front
            Point3(0, 12, 0),
            Point3(3, 12, 0),
            Point3(-3, 12, 0),
            Point3(6, 12, 0),
            Point3(-6, 12, 0),
            Point3(9, 12, 0),
            Point3(-9, 12, 0),

            # Try some points behind
            Point3(0, -6, 0),
            Point3(-3, -6, 0),
            Point3(0, -9, 0),
            Point3(-6, -9, 0))

        for point in possiblePoints:
            pos = self.positionExaminer.consider(node, point, eyeHeight)
            if pos:
                self.setPos(node, pos)
                self.lookAt(node)

                # Don't look exactly at the node; instead, look ten
                # degrees left or right of it.  That way we'll
                # actually be able to see it, without it hiding behind
                # our toon.
                self.setHpr(self.getH() + random.choice((-10, 10)), 0, 0)
                return

        # If we couldn't find a suitable point, just punt and drop us
        # on top of the thing.
        self.setPos(node, 0, 0, 0)

    # Update available custom quicktalker messages
    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages
        messenger.send("customMessagesChanged")

    # Whisper
    def displayWhisper(self, fromId, chatString, whisperType):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This function overrides a similar function in DistributedAvatar.
        """
        sender = None
        sfx = self.soundWhisper

        # MPG we need to identify the sender in a non-toontown specific way
        #sender = base.cr.identifyAvatar(fromId)

        if (whisperType == WhisperPopup.WTNormal or \
            whisperType == WhisperPopup.WTQuickTalker):
            if sender == None:
                return
            # Prefix the sender's name to the message.
            chatString = sender.getName() + ": " + chatString

        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               whisperType)
        if sender != None:
            whisper.setClickable(sender.getName(), fromId)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)

    # Whisper
    def displayWhisperPlayer(self, fromId, chatString, whisperType):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This function overrides a similar function in DistributedAvatar.
        """
        sender = None
        playerInfo = None
        sfx = self.soundWhisper

        # MPG we need to identify the sender in a non-toontown specific way
        #sender = base.cr.identifyAvatar(fromId)
        #sender = idenityPlayer(fromId)
        playerInfo = base.cr.playerFriendsManager.playerId2Info.get(fromId,None)
        if playerInfo == None:
            return
        senderName = playerInfo.playerName

        if (whisperType == WhisperPopup.WTNormal or \
            whisperType == WhisperPopup.WTQuickTalker):
            # Prefix the sender's name to the message.
            chatString = senderName + ": " + chatString

        whisper = WhisperPopup(chatString,
                               OTPGlobals.getInterfaceFont(),
                               whisperType)
        if sender != None:
            whisper.setClickable(senderName, fromId)

        whisper.manage(base.marginManager)
        base.playSfx(sfx)
        #base.chatAssistant.receivePlayerWhisperTypedChat(chatString, fromId)

    # animation
    def setAnimMultiplier(self, value):
        """setAnimMultiplier(self, float)
        Setter for anim playback speed multiplier
        """
        self.animMultiplier = value

    def getAnimMultiplier(self):
        """
        Getter for anim playback speed multiplier
        """
        return self.animMultiplier

    def enableRun(self):
        self.accept("arrow_up", self.startRunWatch)
        self.accept("arrow_up-up", self.stopRunWatch)
        self.accept("control-arrow_up", self.startRunWatch)
        self.accept("control-arrow_up-up", self.stopRunWatch)
        self.accept("alt-arrow_up", self.startRunWatch)
        self.accept("alt-arrow_up-up", self.stopRunWatch)
        self.accept("shift-arrow_up", self.startRunWatch)
        self.accept("shift-arrow_up-up", self.stopRunWatch)

    def disableRun(self):
        self.ignore("arrow_up")
        self.ignore("arrow_up-up")
        self.ignore("control-arrow_up")
        self.ignore("control-arrow_up-up")
        self.ignore("alt-arrow_up")
        self.ignore("alt-arrow_up-up")
        self.ignore("shift-arrow_up")
        self.ignore("shift-arrow_up-up")

    def startRunWatch(self):
        def setRun(ignored):
            messenger.send("running-on")
        taskMgr.doMethodLater(
            self.runTimeout, setRun,
            self.uniqueName('runWatch'))
        return Task.cont

    def stopRunWatch(self):
        taskMgr.remove(self.uniqueName('runWatch'))
        messenger.send("running-off")
        return Task.cont

    def runSound(self):
        self.soundWalk.stop()
        base.playSfx(self.soundRun, looping = 1)

    def walkSound(self):
        self.soundRun.stop()
        base.playSfx(self.soundWalk, looping = 1)

    def stopSound(self):
        self.soundRun.stop()
        self.soundWalk.stop()

    def wakeUp(self):
        # If we are watching to see if Toon falls asleep, there should be
        # a callback set, which tells us we need to restart the task.
        if (self.sleepCallback != None):
            taskMgr.remove(self.uniqueName('sleepwatch'))
            self.startSleepWatch(self.sleepCallback)
        self.lastMoved = globalClock.getFrameTime()
        if self.sleepFlag:
            self.sleepFlag = 0

    def gotoSleep(self):
        if not self.sleepFlag:
            self.b_setAnimState("Sleep", self.animMultiplier)
            self.sleepFlag = 1

    def forceGotoSleep(self):
        # Sad toons don't sleep.
        if (self.hp > 0):
            self.sleepFlag = 0
            self.gotoSleep()

    def startSleepWatch(self, callback):
        self.sleepCallback = callback
        taskMgr.doMethodLater(self.sleepTimeout, callback,
                                self.uniqueName('sleepwatch'))

    def stopSleepWatch(self):
        taskMgr.remove(self.uniqueName('sleepwatch'))
        self.sleepCallback = None

    def startSleepSwimTest(self):
        """
        Spawn a task to check for sleep, this is normally handled by trackAnimToSpeed for some reason
        Sleepwatch appears to be a simple timeout for the sticker book

        """
        taskName = self.taskName("sleepSwimTest")

        # remove any old
        taskMgr.remove(taskName)
        # spawn the new task
        task = Task.Task(self.sleepSwimTest)

        self.lastMoved = globalClock.getFrameTime()
        self.lastState = None
        self.lastAction = None

        self.sleepSwimTest(task)
        taskMgr.add(self.sleepSwimTest, taskName, 35)

    def stopSleepSwimTest(self):
        taskName = self.taskName("sleepSwimTest")
        taskMgr.remove(taskName)
        self.stopSound()

    def sleepSwimTest(self, task):
        now = globalClock.getFrameTime()
        speed, rotSpeed, slideSpeed = self.controlManager.getSpeeds()
        if (speed != 0.0 or rotSpeed != 0.0 or inputState.isSet("jump")):
        # did we just start moving?
            if not self.swimmingFlag:
                self.swimmingFlag = 1
        else:
            # did we just stop moving?
            if self.swimmingFlag:
                self.swimmingFlag = 0
        #print("sleepTest speed %s slide %s jump %s moving %s hp %s time %s timeout %s" % (speed, rotSpeed, inputState.isSet("jump"), self.swimmingFlag, self.hp, now - self.lastMoved, self.swimTimeout))
        if (self.swimmingFlag or self.hp <= 0):
            # The toon is moving or sad; it shouldn't be sleeping now.
            self.wakeUp()
        else:
            # The toon is stationary.  Should we go to sleep?
            if not self.sleepFlag:
                now = globalClock.getFrameTime()
                if now - self.lastMoved > self.swimTimeout:
                    #self.gotoSleep()
                    self.swimTimeoutAction()
                    return Task.done


        return Task.cont

    def swimTimeoutAction(self):
        pass

    def trackAnimToSpeed(self, task):
        #print("trackAnimToSpeed %s" % (random.random()))
        speed, rotSpeed, slideSpeed = self.controlManager.getSpeeds()

        if (speed != 0.0 or rotSpeed != 0.0 or inputState.isSet("jump")):
            # did we just start moving?
            if not self.movingFlag:
                self.movingFlag = 1

                # stop looking around
                self.stopLookAround()
        else:
            # did we just stop moving?
            if self.movingFlag:
                self.movingFlag = 0

                # start looking around
                self.startLookAround()

        if (self.movingFlag or self.hp <= 0):
            # The toon is moving or sad; it shouldn't be sleeping now.
            self.wakeUp()
        else:
            # The toon is stationary.  Should we go to sleep?
            if not self.sleepFlag:
                now = globalClock.getFrameTime()
                if now - self.lastMoved > self.sleepTimeout:
                    self.gotoSleep()

        state = None
        if self.sleepFlag:
            state = "Sleep"
        elif self.hp > 0:
            state = "Happy"
        else:
            state = "Sad"

        if state != self.lastState:
            self.lastState = state
            self.b_setAnimState(state, self.animMultiplier)
            if state == "Sad":
                self.setWalkSpeedSlow()
            else:
                self.setWalkSpeedNormal()

        if self.cheesyEffect == OTPGlobals.CEFlatProfile or \
           self.cheesyEffect == OTPGlobals.CEFlatPortrait:
            # If one of the flat cheesy effects is enabled, rotate the
            # toon slightly when we walks left or right so we can see
            # him.  A better solution might be to attach the camera to
            # the toon with a rubber band, instead of parenting it
            # rigidly to the toon, but this will do for now.
            needH = None
            if rotSpeed > 0.0:
                needH = -10
            elif rotSpeed < 0.0:
                needH = 10
            elif speed != 0.0:
                needH = 0

            if needH != None and self.lastNeedH != needH:
                node = self.getGeomNode().getChild(0)
                lerp = Sequence(LerpHprInterval(node, 0.5, Vec3(needH, 0, 0),
                                                blendType = 'easeInOut'),
                                name = 'cheesy-lerp-hpr',
                                autoPause = 1)
                lerp.start()
                self.lastNeedH = needH
        else:
            self.lastNeedH = None

        action = self.setSpeed(speed, rotSpeed)
        if action != self.lastAction:
            self.lastAction = action
            if self.emoteTrack:
                self.emoteTrack.finish()
                self.emoteTrack = None
            if action == OTPGlobals.WALK_INDEX or action == OTPGlobals.REVERSE_INDEX:
                self.walkSound()
            elif action == OTPGlobals.RUN_INDEX:
                self.runSound()
            else:
                self.stopSound()

        return Task.cont

    def hasTrackAnimToSpeed(self):
        # Returns true if startTrackAnimToSpeed() has been called, and
        # the task is running.
        taskName = self.taskName("trackAnimToSpeed")
        return taskMgr.hasTaskNamed(taskName)

    def startTrackAnimToSpeed(self):
        """
        Spawn a task to match avatar animation with movement speed

            if speed < 0 -> play walk cycle backwards
            if speed = 0
               if rotSpeed = 0 -> neutral cycle
               else -> walk cycle
            if speed > 0 and speed < runCutOff -> walk cycle
            if speed >= runCutOff -> run cycle
        """
        taskName = self.taskName("trackAnimToSpeed")

        # remove any old
        taskMgr.remove(taskName)
        # spawn the new task
        task = Task.Task(self.trackAnimToSpeed)

        self.lastMoved = globalClock.getFrameTime()
        self.lastState = None
        self.lastAction = None

        self.trackAnimToSpeed(task)
        taskMgr.add(self.trackAnimToSpeed, taskName, 35)

    def stopTrackAnimToSpeed(self):
        taskName = self.taskName("trackAnimToSpeed")
        taskMgr.remove(taskName)
        self.stopSound()

    # chat methods
    def startChat(self):
        self.chatMgr.start()
        # listen for outgoing chat messages
        #self.accept("chatUpdate", self.b_setChat)
        #self.accept("chatUpdateSC", self.b_setSC)
        #self.accept("chatUpdateSCCustom", self.b_setSCCustom)
        #self.accept("chatUpdateSCEmote", self.b_setSCEmote)
        #self.accept("whisperUpdate", self.whisperTo)
        #self.accept("whisperUpdateSC", self.whisperSCTo)
        #self.accept("whisperUpdateSCCustom", self.whisperSCCustomTo)
        #self.accept("whisperUpdateSCEmote", self.whisperSCEmoteTo)
        self.accept(OTPGlobals.WhisperIncomingEvent, self.handlePlayerFriendWhisper)
        self.accept(OTPGlobals.ThinkPosHotkey, self.thinkPos)
        self.accept(OTPGlobals.PrintCamPosHotkey, self.printCamPos)
        if self.__enableMarkerPlacement:
            self.accept(OTPGlobals.PlaceMarkerHotkey, self.__placeMarker)

    def stopChat(self):
        self.chatMgr.stop()
        #self.ignore("chatUpdate")
        #self.ignore("chatUpdateSC")
        #self.ignore("chatUpdateSCCustom")
        #self.ignore("chatUpdateSCEmote")
        #self.ignore("whisperUpdate")
        #self.ignore("whisperUpdateSC")
        #self.ignore("whisperUpdateSCCustom")
        #self.ignore("whisperUpdateSCEmote")
        self.ignore(OTPGlobals.WhisperIncomingEvent)
        self.ignore(OTPGlobals.ThinkPosHotkey)
        self.ignore(OTPGlobals.PrintCamPosHotkey)
        if self.__enableMarkerPlacement:
            self.ignore(OTPGlobals.PlaceMarkerHotkey)

    def printCamPos(self):
        # node = base.localAvatar
        node = base.camera.getParent()
        pos = base.cam.getPos(node)
        hpr = base.cam.getHpr(node)
        print 'cam pos = ',`pos`,', cam hpr = ',`hpr`

    def d_broadcastPositionNow(self):
        """
        Forces a broadcast of the toon's current position.  Normally
        this is called immediately before calling
        setParent(OTPGlobals.SPRender), to ensure the remote
        clients don't observe this toon momentarily in the wrong place
        when he appears.
        """
        self.d_clearSmoothing()
        self.d_broadcastPosHpr()

    def travCollisionsLOS(self, n = None):
        if n == None:
            n = self.__geom
        self.ccTrav.traverse(n)

    def travCollisionsFloor(self, n = None):
        if n == None:
            n = self.__geom
        self.ccTravFloor.traverse(n)

    def travCollisionsPusher(self, n = None):
        if n == None:
            n = self.__geom
        self.ccPusherTrav.traverse(n)


    def __friendOnline(self, doId, commonChatFlags=0, whitelistChatFlags = 0):
        """
        Called when a friend comes online, this should report this
        news to the user.
        """
        # The first "online" message we get immediately after adding a
        # new friend is suspect.
        friend = base.cr.identifyFriend(doId)
        if (friend != None) and hasattr(friend,'setCommonAndWhitelistChatFlags'):
            friend.setCommonAndWhitelistChatFlags(commonChatFlags, whitelistChatFlags)

        if self.oldFriendsList != None:
            now = globalClock.getFrameTime()
            elapsed = now - self.timeFriendsListChanged
            if elapsed < 10.0 and self.oldFriendsList.count(doId) == 0:
                # Yep, this is a friend we just added.  Don't report
                # the online message.  But do report future messages.
                self.oldFriendsList.append(doId)
                return

        if friend != None:
            self.setSystemMessage(doId, OTPLocalizer.WhisperFriendComingOnline % (friend.getName()))

    def __friendOffline(self, doId):
        """
        Called when a friend goes offline, this should report this
        news to the user.
        """
        friend = base.cr.identifyFriend(doId)
        if friend != None:
            self.setSystemMessage(0, OTPLocalizer.WhisperFriendLoggedOut % (friend.getName()))

    def __playerOnline(self, playerId):
        playerInfo = base.cr.playerFriendsManager.playerId2Info[playerId]
        if playerInfo:
            self.setSystemMessage(playerId, OTPLocalizer.WhisperPlayerOnline % (playerInfo.playerName, playerInfo.location))

    def __playerOffline(self, playerId):
        playerInfo = base.cr.playerFriendsManager.playerId2Info[playerId]
        if playerInfo:
            self.setSystemMessage(playerId, OTPLocalizer.WhisperPlayerOffline % (playerInfo.playerName))

    def clickedWhisper(self, doId, isPlayer = None):
        """
        Called from the C++ code when the user clicks on a whisper
        message from a friend.
        """
        if not isPlayer:
            friend = base.cr.identifyFriend(doId)
            if friend != None:
                # We request an avatar panel *and* simultaneously open up
                # the whisper-to panel.  We want the avatar panel to allow
                # going to the friend; but sometimes (for instance, in a
                # battle) the avatar panel won't come up, so we also open
                # the whisper-to panel just in case.
                messenger.send("clickedNametag", [friend])
                self.chatMgr.whisperTo(friend.getName(), doId)
        else:
            friend = base.cr.playerFriendsManager.getFriendInfo(doId)
            if friend:
                messenger.send("clickedNametagPlayer", [None, doId])
                self.chatMgr.whisperTo(friend.getName(), None, doId)



    # this is here to ensure that the correct overloaded method is called
    def d_setParent(self, parentToken):
        DistributedSmoothNode.DistributedSmoothNode.d_setParent(
                self, parentToken)

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(id(self))+' '+message)

    def handlePlayerFriendWhisper(self, playerId, charMessage):
        """
        handle player friend message.
        """
        print("handlePlayerFriendWhisper")
        self.displayWhisperPlayer(playerId, charMessage, WhisperPopup.WTNormal)

    def canChat(self):
        """
        Overrided by derived class
        """
        assert(0)
        return 0

