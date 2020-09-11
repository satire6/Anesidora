import string
from direct.showbase.DirectObject import DirectObject
from direct.directtools.DirectGeometry import *
from direct.controls.ControlManager import *
from direct.controls import GravityWalker
from direct.controls import NonPhysicsWalker
from direct.interval.LerpInterval import LerpFunctionInterval

from otp.avatar import LocalAvatar
from otp.otpbase import OTPGlobals

from toontown.toon import RobotToon

class ToonControlManager(ControlManager):
    def __init__(self, editor):
        self.fStarting = True
        self.editor = editor
        self.configureDriveModeCollisionData()
        ControlManager.__init__(self)
        self.oldFov = base.camLens.getFov()

        self.avatarMoving = 0
        self.isPageUp=0
        self.isPageDown=0
        
        avatarRadius = 1.4
        floorOffset = OTPGlobals.FloorOffset
        reach = 4.0

        self.avatar = LEAvatar(None, None, None)
        base.localAvatar = self.avatar
        self.avatar.doId = 0
        self.avatar.robot = RobotToon.RobotToon()
        self.avatar.robot.reparentTo(self.avatar)
        self.avatar.setHeight(self.avatar.robot.getHeight())
        self.avatar.setName("The Inspector")
        self.avatar.robot.loop('neutral')

        #walkControls=GravityWalker.GravityWalker(gravity = -32.1740 * 2.0)
        walkControls=NonPhysicsWalker.NonPhysicsWalker()
        walkControls.setWallBitMask(OTPGlobals.WallBitmask)
        walkControls.setFloorBitMask(OTPGlobals.FloorBitmask)
        walkControls.initializeCollisions(self.cTrav, self.avatar,
                                          avatarRadius, floorOffset, reach)
        self.add(walkControls, "walk")
        self.use("walk", self.editor)

        # set speeds after adding controls to the control manager
        self.setSpeeds(
            OTPGlobals.ToonForwardSpeed,
            OTPGlobals.ToonJumpForce,
            OTPGlobals.ToonReverseSpeed,
            OTPGlobals.ToonRotateSpeed
            )

        self.avatar.reparentTo(hidden)
        self.avatar.stopUpdateSmartCamera()
        self.fStarting = False
        #ControlManager.disable(self)
    
    def enable(self):
        if self.fStarting:
            return
        
        self.prepareToStart()
        ControlManager.enable(self)

        if base.direct.selected.last:
            base.direct.selected.deselect(base.direct.selected.last)
        
        self.avatarAnimTask = taskMgr.add(self.avatarAnimate, 'avatarAnimTask', 24)
        self.avatar.startUpdateSmartCamera()
        
        self.avatarMoving = 0
        
    def disable(self):
        self.prepareToStop()
        ControlManager.disable(self)


    def lerpCameraP(self, p, time):
        """
        lerp the camera P over time (used by the battle)
        """
        taskMgr.remove('cam-p-lerp')
        if self.avatar:
            self.avatar.stopUpdateSmartCamera()
        def setCamP(p):
            base.camera.setP(p)

        if self.isPageUp:
            fromP = 36.8699
        elif self.isPageDown:
            fromP = -27.5607
        else:
            fromP = 0

        self.camLerpInterval = LerpFunctionInterval(setCamP,
            fromData=fromP, toData=p, duration=time,
            name='cam-p-lerp')
        self.camLerpInterval.start()

    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraP(0, 0.6)
            self.isPageDown = 0
            self.isPageUp = 0
            #self.setCameraPositionByIndex(self.cameraIndex)

        if self.avatar:
            self.avatar.startUpdateSmartCamera()
            
    def pageUp(self):
        if not self.isPageUp:
            self.lerpCameraP(36.8699, 0.6)
            self.isPageDown = 0
            self.isPageUp = 1
            #self.setCameraPositionByIndex(self.cameraIndex)
        else:
            self.clearPageUpDown()

    def pageDown(self):
        if not self.isPageDown:
            self.lerpCameraP(-27.5607, 0.6)
            self.isPageUp = 0
            self.isPageDown = 1
            #self.setCameraPositionByIndex(self.cameraIndex)
        else:
            self.clearPageUpDown()            

    #--------------------------------------------------------------------------
    # Function:   animate avatar model based on if it is moving
    # Parameters: none
    # Changes:
    # Returns:
    #--------------------------------------------------------------------------
    def avatarAnimate(self,task=None):
        moving = self.currentControls.speed or self.currentControls.slideSpeed or self.currentControls.rotationSpeed
        if (moving and
            self.avatarMoving == 0):
            self.clearPageUpDown()
            # moving, play walk anim
            if (self.currentControls.speed < 0 or
                self.currentControls.rotationSpeed):
                self.avatar.robot.loop('walk')
            else:
                self.avatar.robot.loop('run')
            self.avatarMoving = 1
        elif (moving == 0 and
              self.avatarMoving == 1):
            # no longer moving, play neutral anim
            self.avatar.robot.loop('neutral')
            self.avatarMoving = 0
        return Task.cont

    def configureDriveModeCollisionData(self):
        """
        Set up the local avatar for collisions
        """
        # Set up the collision sphere
        # This is a sphere on the ground to detect barrier collisions
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, 1.5)
        self.cSphereNode = CollisionNode('cSphereNode')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = base.camera.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereBitMask = BitMask32.bit(0)
        self.cSphereNode.setFromCollideMask(self.cSphereBitMask)
        self.cSphereNode.setIntoCollideMask(BitMask32.allOff())

        # Set up the collison ray
        # This is a ray cast from your head down to detect floor polygons
        self.cRay = CollisionRay(0.0, 0.0, 6.0, 0.0, 0.0, -1.0)
        self.cRayNode = CollisionNode('cRayNode')
        self.cRayNode.addSolid(self.cRay)
        self.cRayNodePath = base.camera.attachNewNode(self.cRayNode)
        self.cRayNodePath.hide()
        self.cRayBitMask = BitMask32.bit(1)
        self.cRayNode.setFromCollideMask(self.cRayBitMask)
        self.cRayNode.setIntoCollideMask(BitMask32.allOff())

        # set up wall collision mechanism
        self.pusher = CollisionHandlerPusher()
        self.pusher.setInPattern("enter%in")
        self.pusher.setOutPattern("exit%in")

        # set up floor collision mechanism
        self.lifter = CollisionHandlerFloor()
        self.lifter.setInPattern("on-floor")
        self.lifter.setOutPattern("off-floor")
        self.floorOffset = 0.1
        self.lifter.setOffset(self.floorOffset)

        # Limit our rate-of-fall with the lifter.
        # If this is too low, we actually "fall" off steep stairs
        # and float above them as we go down. I increased this
        # from 8.0 to 16.0 to prevent this
        self.lifter.setMaxVelocity(16.0)

        # set up the collision traverser
        self.cTrav = CollisionTraverser("LevelEditor")
        self.cTrav.setRespectPrevTransform(1)

        # activate the collider with the traverser and pusher
        #self.pusher.addCollider(self.cSphereNodePath, base.camera, base.drive.node())
        #self.lifter.addCollider(self.cRayNodePath, base.camera, base.drive.node())
        # A map of zone ID's to a list of nodes that are visible from
        # that zone.
        self.nodeDict = {}
        # A map of zone ID's to the particular node that corresponds
        # to that zone.
        self.zoneDict = {}
        # A list of all visible nodes
        self.nodeList = []
        # Flag for bootstrapping visibility
        self.fVisInit = 0

    def hideAllVisibles(self):
        for i in self.nodeList:
            i.hide()

    def showAllVisibles(self):
        for i in self.nodeList:
            i.show()
            i.clearColor()

    def extractGroupName(self, groupFullName):
        # The Idea here is that group names may have extra flags associated
        # with them that tell more information about what is special about
        # the particular vis zone. A normal vis zone might just be "13001",
        # but a special one might be "14356:safe_zone" or
        # "345:safe_zone:exit_zone"... These are hypotheticals. The main
        # idea is that there are colon separated flags after the initial
        # zone name.
        return(string.split(groupFullName, ":", 1)[0])

    def renameFloorPolys(self, nodeList):
        for i in nodeList:
            # Get all the collision nodes in the vis group
            collNodePaths = i.findAllMatches("**/+CollisionNode")
            numCollNodePaths = collNodePaths.getNumPaths()
            visGroupName = i.node().getName()
            for j in range(numCollNodePaths):
                collNodePath = collNodePaths.getPath(j)
                bitMask = collNodePath.node().getIntoCollideMask()
                if bitMask.getBit(1):
                    # Bit 1 is the floor collision bit. This renames
                    # all floor collision polys to the same name as their
                    # visgroup.
                    collNodePath.node().setName(visGroupName)

    def initVisibilityData(self):
        # First make sure everything is shown
        self.showAllVisibles()
        # A map of zone ID's to a list of nodes that are visible from
        # that zone.
        self.nodeDict = {}
        # A map of zone ID's to the particular node that corresponds
        # to that zone.
        self.zoneDict = {}
        # A list of all visible nodes
        self.nodeList = []
        # NOTE: this should change to find the groupnodes in
        # the dna storage instead of searching through the tree
        for i in range(DNASTORE.getNumDNAVisGroups()):
            groupFullName = DNASTORE.getDNAVisGroupName(i)
            groupName = self.extractGroupName(groupFullName)
            zoneId = int(groupName)
            self.nodeDict[zoneId] = []
            self.zoneDict[zoneId] = self.editor.NPToplevel.find("**/__vis_group__%s_*"%groupName)

            # TODO: we only need to look from the top of the hood
            # down one level to find the vis groups as an optimization
            groupNode = self.editor.NPToplevel.find("**/" + groupFullName)
            if groupNode.isEmpty():
                print "Could not find visgroup"
            self.nodeList.append(groupNode)
            for j in range(DNASTORE.getNumVisiblesInDNAVisGroup(i)):
                visName = DNASTORE.getVisibleName(i, j)
                visNode = self.editor.NPToplevel.find("**/__vis_group__%s_*"%visName)
                self.nodeDict[zoneId].append(visNode)
        # Rename the floor polys to have the same name as the
        # visgroup they are in... This makes visibility possible.
        self.renameFloorPolys(self.nodeList)
        # Init vis flag
        self.fVisInit = 1

    def collisionsOff(self):
        self.cTrav.removeCollider(self.cSphereNodePath)

    def collisionsOn(self):
        self.collisionsOff()
        self.cTrav.addCollider(self.cSphereNodePath, self.pusher)

    def traversalOn(self):
        base.cTrav = self.cTrav

    def traversalOff(self):
        base.cTrav = 0

    def visibilityOn(self):
        self.visibilityOff()
        # Accept event
        self.editor.accept("on-floor", self.enterZone)
        # Add collider
        self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        # Reset lifter
        self.lifter.clear()
        # Reset flag
        self.fVisInit = 1

    def visibilityOff(self):
        self.editor.ignore("on-floor")
        self.cTrav.removeCollider(self.cRayNodePath)
        self.showAllVisibles()

    def enterZone(self, newZone):
        return
        """
        Puts the toon in the indicated zone.  newZone may either be a
        CollisionEntry object as determined by a floor polygon, or an
        integer zone id.  It may also be None, to indicate no zone.
        """
        # First entry into a zone, hide everything
        if self.fVisInit:
            self.hideAllVisibles()
            self.fVisInit = 0
        # Get zone id
        if isinstance(newZone, CollisionEntry):
            # Get the name of the collide node
            try:
                newZoneId = int(newZone.getIntoNode().getName())
            except:
                newZoneId = 0
        else:
            newZoneId = newZone
        # Ensure we have vis data
        assert self.nodeDict
        # Hide the old zone (if there is one)
        if self.__zoneId != None:
            for i in self.nodeDict[self.__zoneId]:
                i.hide()
        # Show the new zone
        if newZoneId != None:
            for i in self.nodeDict[newZoneId]:
                i.show()
        # Make sure we changed zones
        if newZoneId != self.__zoneId:
            if self.panel.fVisZones.get():
                # Set a color override on our zone to make it obvious what
                # zone we're in.
                if self.__zoneId != None:
                    self.zoneDict[self.__zoneId].clearColor()
                if newZoneId != None:
                    self.zoneDict[newZoneId].setColor(0, 0, 1, 1, 100)
            # The new zone is now old
            self.__zoneId = newZoneId

    def prepareToStart(self):
        self.editor.ui.perspView.camera.reparentTo(base.camera)
        self.editor.ui.perspView.camera.setPos(0)
        self.editor.ui.perspView.camera.setHpr(0)
        base.direct.fMouse1 = 0
        base.direct.fMouse2 = 0
        base.direct.fMouse3 = 0        

        base.direct.fAlt = 0
        base.direct.fConntrol = 0
        base.direct.fShift = 0        

        self.editor.accept('page_up', self.pageUp)
        self.editor.accept('page_down', self.pageDown)        
        
        self.avatar.setPos(self.editor.ui.perspView.camera.getPos())
        self.avatar.reparentTo(render)
        """ Lerp down to eye level then switch to Drive mode """
##         pos = base.direct.camera.getPos()
##         pos.setZ(4.0)
##         hpr = base.direct.camera.getHpr()
##         hpr.set(hpr[0], 0.0, 0.0)
##         t = base.direct.camera.lerpPosHpr(pos, hpr, 1.0, blendType = 'easeInOut',
##                                    task = 'manipulateCamera')
        # Note, if this dies an unatural death, this could screw things up
        # t.uponDeath = self.switchToDriveMode

        self.initVisibilityData()
        base.camera.wrtReparentTo(self.avatar)
        base.camera.setHpr(0, 0, 0)
        base.camera.setPos(0, -11.8125, 3.9375)
        base.camLens.setFov(VBase2(60, 46.8265))        

        # Turn on collisions
        #if self.panel.fColl.get():
        self.collisionsOn()
        # Turn on visiblity
        #if self.panel.fVis.get():
        self.visibilityOn()
        # Turn on collision traversal
        #if self.panel.fColl.get() or self.panel.fVis.get():
        self.traversalOn()

        self.editor.ui.perspView.bt.node().setPrefix('')

    def prepareToStop(self):
        """ Disable player camera controls/enable direct camera control """
        # Turn off collision traversal
        self.traversalOff()
        # Turn on collisions
        self.collisionsOff()
        # Turn on visiblity
        self.visibilityOff()
        base.camera.wrtReparentTo(render)
        # Reset cam
        base.camera.iPos(base.direct.cam)
        base.direct.cam.iPosHpr()
        base.camLens.setFov(self.oldFov)
        # Renable mouse
        #self.editor.enableMouse()
        #base.direct.enable()

        self.editor.ui.perspView.camera.reparentTo(render)
        self.editor.ui.perspView.camera.setPos(base.camera.getPos())
        self.editor.ui.perspView.camera.setHpr(base.camera.getHpr())
        # [gjeon]  disable avatar and controlManager
        self.avatar.reparentTo(hidden)
        self.avatar.stopUpdateSmartCamera()

        self.editor.ignore('page_up')
        self.editor.ignore('page_down')
        self.editor.ui.perspView.bt.node().setPrefix('_le_per_')

# [gjeon] for LevelEditor specific Avatar
class LEAvatar(LocalAvatar.LocalAvatar):
    def __init__(self, cr, chatMgr, chatAssistant, passMessagesThrough = False):
        LocalAvatar.LocalAvatar.__init__(self,  cr, chatMgr, chatAssistant, passMessagesThrough)

    def getAutoRun(self):
        return 0
