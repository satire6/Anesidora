import math
import random
import time
from pandac.PandaModules import TextNode, BitMask32, Point3,\
     Vec3, Vec4, deg2Rad, Mat3, NodePath, VBase4, \
     OdeTriMeshData, OdeTriMeshGeom, OdeRayGeom
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
from direct.gui.DirectGui import DirectWaitBar, DGG, DirectLabel
from direct.task import Task
from direct.fsm.FSM import FSM
from toontown.minigame import ArrowKeys
from direct.showbase import PythonUtil
from toontown.golf import BuildGeometry
from toontown.golf import  DistributedPhysicsWorld
from toontown.golf import GolfGlobals
from direct.interval.IntervalGlobal import Sequence, Parallel, \
     LerpScaleInterval, LerpFunctionInterval, Func, Wait,\
     SoundInterval, ParallelEndTogether, LerpPosInterval, ActorInterval, LerpPosHprInterval, \
     LerpColorScaleInterval, WaitInterval
from direct.actor import Actor
from toontown.golf import GolfHoleBase
from toontown.distributed import DelayDelete

class DistributedGolfHole(DistributedPhysicsWorld.DistributedPhysicsWorld, FSM, GolfHoleBase.GolfHoleBase):

    defaultTransitions = {
        'Off'             : [ 'Cleanup', 'ChooseTee', 'WatchTee' ],
        'ChooseTee'       : [ 'Aim', 'Cleanup'],
        'WatchTee'        : [ 'WatchAim', 'Cleanup', 'WatchTee', 'ChooseTee', 'Aim'],
        'Wait'            : [ 'Aim','WatchAim', 'Playback','Cleanup','ChooseTee','WatchTee' ],
        'Aim'             : [ 'Shoot', 'Playback', 'Cleanup', 'Aim', 'WatchAim' ],
        'WatchAim'        : [ 'WatchAim', 'WatchShoot', 'Playback', 'Cleanup' , 'Aim', 'ChooseTee', 'WatchTee'],
        'Playback'        : [ 'Wait', 'Aim', 'WatchAim', 'Cleanup', 'ChooseTee', 'WatchTee' ],
        'Cleanup'         : ['Off']
    # we can go from WatchAim to Aim when the 2nd golfer aiming drops unexpectedly
    # we can go from WatchTee to ChooseTee when the 2nd golfer teeing drops unexpectedly
    # we can go from WatchTee to WatchTee when the 2nd golfer teeing drops unexpectedly
    # we can go from WatchTee to Aim when the last golfer teeing drops unexpectedly
    # Playback to ChooseTee and Playback to WatchTee happens on unexpected drops
    # WatchAim to ChooseTee and WatchAim to Watchtee happens on unexpected drops
    # Aim to WatchAim can happen if we dont swing and we get kicked out
    }
    id = 0
    notify = directNotify.newCategory("DistributedGolfHole")    
    unlimitedAimTime = base.config.GetBool('unlimited-aim-time', 0)
    unlimitedTeeTime = base.config.GetBool('unlimited-tee-time', 0)

    # The number of seconds it takes to move the power meter to
    # full the first time.
    golfPowerSpeed = base.config.GetDouble('golf-power-speed', 3)

    # The exponent that controls the factor at which the power
    # meter slows down over time.  Values closer to 1.0 slow down less
    # quickly.
    golfPowerExponent = base.config.GetDouble('golf-power-exponent', 0.75)
    
    def __init__(self, cr):
        self.notify.debug("Hole Init")
        DistributedPhysicsWorld.DistributedPhysicsWorld.__init__(self, base.cr)
        GolfHoleBase.GolfHoleBase.__init__(self, 1)
        FSM.__init__( self, "Golf_%s_FSM" % ( self.id ) )
        
        #base.g = self
        self.currentGolfer = 0
        self.ballDict = {}# {avId : (ballNodePath, actorNode, ballActorNodePath)}
        self.ballShadowDict = {}
        self.holeNodes = []
        self.golfCourse = None
        self.golfCourseRequest = None

        self.holePositions = []
        self.timer = None
        self.teeTimer = None
        self.aimStart = None

        self.titleLabel = None

        self.teeInstructions = None
        self.aimInstructions = None
        self.powerReminder = None
        self.lastTimeHeadingSent = 0
        self.lastTempHeadingSent = 0
        
        self.holdCycleTime = 0.0
        self.inPlayBack = 0

        self.swingInterval = None
        self.sfxInterval = None
        self.isLookingAtPutt = False
        self.clubs = {}

        self.camInterval = None
        self.flyOverInterval = None
        self.needToDoFlyOver = True

        self.translucentLastFrame = []
        self.translucentCurFrame = []

        self.localMissedSwings = 0
        self.localToonHitControl = False
        self.warningInterval = None
        
        self.playBackDelayDelete = None
        
        self.aimMomentum = 0.0

        self.lastBumpSfxPos = Point3(0,0,0) # last ball position where we played a bump sfx

        # this will be used to generate textnodes
        self.__textGen = TextNode("golfHoleText")
        self.__textGen.setFont(ToontownGlobals.getSignFont())
        self.__textGen.setAlign(TextNode.ACenter)
        if TTLocalizer.getLanguage() in ['castillian', 'japanese', 'german', 'portuguese', 'french']:
            self.__textGen.setGlyphScale(0.7)

        self.avIdList = []
        self.enterAimStart = 0

    def generate(self):
        self.notify.debug("Hole Generate")
        DistributedPhysicsWorld.DistributedPhysicsWorld.generate(self)
        self.golfPowerTaskName = self.uniqueName('updateGolfPower')

    def announceGenerate(self):
        """Do stuff dependent on required fields."""
        assert self.notify.debugStateCall(self)
        DistributedPhysicsWorld.DistributedPhysicsWorld.announceGenerate(self)
        # we must wait for the holeId to come in from the AI before we setup
        self.setup()
        self.sendReady()
        self.request("Off")

        index = 1
        for avId in self.avIdList:
            self.createBall(avId, index)
            self.createClub(avId)
            index += 1
        if self.avIdList:
            avId = self.avIdList[0]
            self.currentGolfer = avId
        self.currentGolferActive = False

    def delete(self):
        #print("GOLF HOLE DELETE")
        assert self.notify.debugStateCall(self)
        self.removePlayBackDelayDelete()
        self.request('Cleanup')
        taskMgr.remove(self.golfPowerTaskName)
        DistributedPhysicsWorld.DistributedPhysicsWorld.delete(self)
        GolfHoleBase.GolfHoleBase.delete(self)
        if hasattr(self, 'perfectIval'):
            self.perfectIval.pause()
            del self.perfectIval
        self.golfCourse = None
        if self.teeInstructions:
            self.teeInstructions.destroy()
            self.teeInstructions = None
        if self.aimInstructions:
            self.aimInstructions.destory()
            self.aimInstructions = None
        if self.powerReminder:
            self.powerReminder.destroy()
            self.powerReminder = None
        if self.swingInterval:
            self.swingInterval.pause()
            self.swingInterval = None
        if self.sfxInterval:
            self.sfxInterval.pause()
            self.sfxInterval = None
        if self.camInterval:
            self.camInterval.pause()
            self.camInterval = None            
        for club in self.clubs:
            self.clubs[club].removeNode()
        del self.clubs
        if hasattr(self, "scoreBoard"): #ugly!!
            if hasattr(self.scoreBoard, "maximizeB"):
                if self.scoreBoard.maximizeB:
                    self.scoreBoard.maximizeB.hide()
        if not (self.titleLabel == None):
            self.titleLabel.destroy()
            self.notify.debug("Deleted title label")
        self.notify.debug("Delete function")
        if self.flyOverInterval:
            self.flyOverInterval.pause()
        self.flyOverInterval = None
        for key in self.ballShadowDict:
            self.ballShadowDict[key].removeNode()
        self.dropShadowModel.removeNode()
        
    def sendReady(self):
        assert self.notify.debugStateCall(self)
        self.sendUpdate("setAvatarReadyHole", [])

    def createClub(self,avId):
        """Load the golf clubs. Per toon to make things easier."""
        club = NodePath('club-%s'%avId)
        clubModel = loader.loadModel('phase_6/models/golf/putter')
        clubModel.reparentTo(club)
        self.clubs[avId] = club

    def attachClub(self, avId, pointToBall = False):
        """Attach the club to the right hand."""
        club = self.clubs[avId]
        if club :
            av = base.cr.doId2do.get(avId)
            if av:
                av.useLOD(1000)
                lHand = av.getLeftHands()[0]
                club.setPos(0,0,0)
                club.reparentTo(lHand)
                # we have to account for small toons like the mouse
                netScale = club.getNetTransform().getScale()[1]
                counterActToonScale = lHand.find('**/counteractToonScale')
                if counterActToonScale.isEmpty():                    
                    counterActToonScale = lHand.attachNewNode('counteractToonScale')
                    counterActToonScale.setScale( 1 /netScale)
                    self.notify.debug('creating counterActToonScale for %s' % av.getName())
                club.reparentTo(counterActToonScale)
                club.setX(-0.25 * netScale )                
                if pointToBall:
                    club.lookAt(self.clubLookatSpot)
                # self.notify.debug('after lookat, hpr = %s' % club.getHpr())
                
    def createToonRay(self):
        """Create the ray that we will use to push toons up from sidewalks."""
        self.toonRay = OdeRayGeom(self.space, 10.0)
        self.toonRay.setCollideBits( BitMask32(0x00ffffff))
        self.toonRay.setCategoryBits(BitMask32(0x00000000))        
        self.toonRay.setRotation(Mat3(1, 0, 0, 0, -1, 0, 0, 0, -1))
        self.space.setCollideId(self.toonRay, GolfGlobals.TOON_RAY_COLLIDE_ID)
        self.rayList.append(self.toonRay)
        # self.toonRayDebugAxis = loader.loadModel('models/misc/xyzAxis')
        # self.toonRayDebugAxis.setScale(0.1)
        # self.toonRayDebugAxis.reparentTo(render)
        # self.toonRayDebugAxis2 = loader.loadModel('models/misc/xyzAxis')
        # self.toonRayDebugAxis2.setScale(0.1)
        # self.toonRayDebugAxis2.reparentTo(render)
        
    def createSkyRay(self):
        """Create the sky ray."""
        self.skyRay = OdeRayGeom(self.space, 100.0)
        self.skyRay.setCollideBits( BitMask32(0x000000f0))
        self.skyRay.setCategoryBits(BitMask32(0x00000000))        
        self.skyRay.setRotation(Mat3(1, 0, 0, 0, -1, 0, 0, 0, -1))
        self.space.setCollideId(self.skyRay, 78)
        self.rayList.append(self.skyRay)

    def createCameraRay(self):
        """Create the ray that we will use to determine if geoms become translucent."""
        self.cameraRay = OdeRayGeom(self.space, 30.0)
        self.cameraRay.setCollideBits( BitMask32(0x00800000))
        self.cameraRay.setCategoryBits(BitMask32(0x00000000))        
        self.space.setCollideId(self.cameraRay, GolfGlobals.CAMERA_RAY_COLLIDE_ID)
        self.cameraRayNodePath = self.terrainModel.attachNewNode('cameraRayNodePath')
        self.rayList.append(self.cameraRay)
        
    def loadLevel(self):
        GolfHoleBase.GolfHoleBase.loadLevel(self)
        """Load all the assets needed by this golf hole."""
  
        # setup the multiple tee starting positions
        self.teeNodePath = self.terrainModel.find('**/tee0')
        if self.teeNodePath.isEmpty():
            teePos = Vec3(0,0,10)
        else:
            teePos = self.teeNodePath.getPos()
            teePos.setZ(teePos.getZ() + GolfGlobals.GOLF_BALL_RADIUS)
            self.notify.debug('teeNodePath heading = %s' % self.teeNodePath.getH())
        self.teePositions = [teePos]
        teeIndex = 1
        teeNode = self.terrainModel.find('**/tee%d' % teeIndex)
        while not teeNode.isEmpty():
            teePos = teeNode.getPos()
            teePos.setZ(teePos.getZ() + GolfGlobals.GOLF_BALL_RADIUS)
            self.teePositions.append(teePos)
            self.notify.debug('teeNodeP heading = %s' % teeNode.getH())
            teeIndex += 1
            teeNode = self.terrainModel.find('**/tee%d' % teeIndex)
        
        # find the hole's bottom
        self.holeBottomNodePath = self.terrainModel.find('**/holebottom0')
        if self.holeBottomNodePath.isEmpty():
            self.holeBottomPos = Vec3(*self.holeInfo['holePos'][0])
        else:
            self.holeBottomPos = self.holeBottomNodePath.getPos()
        self.holePositions.append(self.holeBottomPos)

        # calculate the center of the course
        minHard = Point3(0,0,0)
        maxHard = Point3(0,0,0)
        self.hardSurfaceNodePath.calcTightBounds(minHard, maxHard)
        centerX = ((minHard[0] + maxHard[0]) / 2.0)
        centerY = ((minHard[1] + maxHard[1]) / 2.0)
        heightX = (centerX - minHard[0]) / math.tan( deg2Rad(23))
        heightY = (centerY - minHard[1]) / math.tan( deg2Rad(18))
        height = max(heightX, heightY)
        self.camTopViewPos = Point3(centerX, centerY, height)
        self.camTopViewHpr = Point3(0,-90,0)

        # create the collision ray to push toons up
        self.createRays()
        self.createToonRay()
        #self.createSkyRay()
        self.createCameraRay()


    def createLocatorDict(self):
        """Create a dictionary of locator numbers to the actual nodepath."""
        self.locDict = {} 
        locatorNum = 1
        curNodePath = self.hardSurfaceNodePath.find('**/locator%d' % locatorNum)
        while not curNodePath.isEmpty():
            self.locDict[locatorNum] = curNodePath
            locatorNum += 1
            curNodePath = self.hardSurfaceNodePath.find('**/locator%d' % locatorNum)
        
    def loadBlockers(self):
        """Load the programmable blockers."""
        loadAll = base.config.GetBool('golf-all-blockers',0)
        self.createLocatorDict()
        self.blockerNums = self.holeInfo['blockers']

        for locatorNum in self.locDict:
            if locatorNum in self.blockerNums or loadAll:
                locator = self.locDict[locatorNum]
                locatorParent = locator.getParent()
                locator.getChildren().wrtReparentTo(locatorParent)
            else:
                self.locDict[locatorNum].removeNode()

        self.hardSurfaceNodePath.flattenStrong()

    def loadSounds(self):
        """Load the sounds we will use."""
        self.hitBallSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Hit_Ball.mp3")
        self.holeInOneSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Hole_In_One.mp3")
        self.holeInTwoPlusSfx = loader.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_fall.mp3")        
        self.ballGoesInStartSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Ball_Goes_In_Start.wav")
        self.ballGoesInLoopSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Ball_Goes_In_Loop.wav")
        self.ballGoesToRestSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Ball_Rest_In_Cup.mp3")
        self.kickedOutSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Sad_Noise_Kicked_Off_Hole.mp3")
        self.crowdBuildupSfx = []
        self.crowdApplauseSfx = []
        self.crowdMissSfx = []
        for i in xrange(4):
            self.crowdBuildupSfx.append(
                loader.loadSfx("phase_6/audio/sfx/Golf_Crowd_Buildup.mp3"))
            self.crowdApplauseSfx.append(
                loader.loadSfx("phase_6/audio/sfx/Golf_Crowd_Applause.mp3"))
            self.crowdMissSfx.append(
                loader.loadSfx("phase_6/audio/sfx/Golf_Crowd_Miss.mp3"))
        self.bumpHardSfx = loader.loadSfx("phase_6/audio/sfx/Golf_Hit_Barrier_3.mp3")
        self.bumpMoverSfx = loader.loadSfx("phase_4/audio/sfx/Golf_Hit_Barrier_2.mp3")
        self.bumpWindmillSfx = loader.loadSfx("phase_4/audio/sfx/Golf_Hit_Barrier_1.mp3")
        
    def setup(self):
        """Setup the level, sounds, gui objects and controls."""
        self.notify.debug("setup golf hole")
        
        self.loadLevel()
        self.loadSounds()

        # please update cleanupGeom as you add or subtract geometry
        
        self.camMove = 0
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.arrowKeys.setPressHandlers([None, None,
                                         self.__leftArrowPressed,
                                         self.__rightArrowPressed,
                                         self.__beginTossGolf])
        self.arrowKeys.setReleaseHandlers([None, None, None, None, self.__endTossGolf])
        
        self.targets = render.attachNewNode("targetGameTargets")
        
        self.ballFollow = render.attachNewNode("nodeAtBall")
        # todo read in the starting tee heading somewhere
        self.startingTeeHeading = self.teeNodePath.getH()
        self.ballFollow.setH(self.startingTeeHeading)
        self.ballFollowToonSpot = self.ballFollow.attachNewNode('toonAimSpot')
        self.ballFollowToonSpot.setX(-2.0)
        self.ballFollowToonSpot.setY(0)
        self.ballFollowToonSpot.setH(-90)
        self.clubLookatSpot = self.ballFollow.attachNewNode('clubLookat')
        self.clubLookatSpot.setY(- (GolfGlobals.GOLF_BALL_RADIUS + 0.1))
        camera.reparentTo(self.ballFollow)
        self.camPosBallFollow = Point3(0.0,-23.0,12.0)
        self.camHprBallFollow = Point3(0, -16.0, 0)
        camera.setPos(self.camPosBallFollow)
        camera.setHpr(self.camHprBallFollow) 

        if self.holeBottomNodePath.isEmpty():
            holePositions = self.holePositions
            for index in xrange(len(holePositions)):
                holePos =  holePositions[index]
                targetNodePathGeom, t1, t2 = BuildGeometry.addCircleGeom(self.targets, 16, 1)
                targetNodePathGeom.setPos(holePos)
                targetNodePathGeom.setBin('ground', 0)
                targetNodePathGeom.setDepthWrite(False)
                targetNodePathGeom.setDepthTest(False)
                targetNodePathGeom.setTransparency(TransparencyAttrib.MAlpha)
                targetNodePathGeom.setColorScale(0.0, 0.0, 0.0, 1.0)
                self.holeNodes.append(targetNodePathGeom)

                holeSphere = CollisionSphere(0,0,0,1)
                holeSphere.setTangible(1)
                holeCNode = CollisionNode("Hole")
                holeCNode.addSolid(holeSphere)
                holeC = targetNodePathGeom.attachNewNode(holeCNode)
                holeC.show()
            holeC.setCollideMask(ToontownGlobals.PieBitmask)

        toon = base.localAvatar
        toon.setPos(0.0,0.0,-100.0)
        toon.b_setAnimState("neutral", 1.0)
        self.pollingCtrl = 0
        self.timeLastCtrl = 0.0

        self.powerBar = DirectWaitBar(
            guiId = 'launch power bar',
            pos = (0.0, 0, -0.65),
            relief = DGG.SUNKEN,
            frameSize = (-2.0,2.0,-0.2,0.2),
            borderWidth = (0.02,0.02),
            scale = 0.25,
            range = 100,
            sortOrder = 50,
            frameColor = (0.5,0.5,0.5,0.5),
            barColor = (1.0,0.0,0.0,1.0),
            text = "",
            text_scale = 0.26,
            text_fg = (1, 1, 1, 1),
            text_align = TextNode.ACenter,
            text_pos = (0,-0.05),
            )
            
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar.hide()

        self.accept('tab', self.tabKeyPressed)
        
        self.putAwayAllToons()

        # hide the hole and wait for flyover
        base.transitions.irisOut(t = 0)
        
        #taskMgr.add(self.__updateTask, "update task")
        
        self.dropShadowModel = loader.loadModel(
            "phase_3/models/props/drop_shadow")
        self.dropShadowModel.setColor(0,0,0,0.5)
        self.dropShadowModel.flattenMedium()
        self.dropShadowModel.hide()

    def switchToAnimState(self, animStateName, forced = False):
        """Switch the local toon to another anim state if not in it already."""
        # temp since we only have anims for male medium torso medium legs
        #dna = base.localAvatar.getStyle()
        #if not( dna.gender == 'm' and (dna.torso =='ms' or dna.torso =='ls')\
        #        and (dna.legs=='m' or dna.legs=='l')):
        #    return
        curAnimState = base.localAvatar.animFSM.getCurrentState()
        curAnimStateName = ''
        if curAnimState:
            curAnimStateName = curAnimState.getName()
        if curAnimStateName != animStateName or forced:
            base.localAvatar.b_setAnimState(animStateName)
        
    def __aimTask(self, task):
        """Handle input and other necessary stuff while in the Aim state."""
        # Gah always point the club at the ball, avoid weird club penetrating ball problems
        self.attachClub(self.currentGolfer, True)
        
        x = -math.sin(self.ballFollow.getH() * 0.0174532925)
        y = math.cos(self.ballFollow.getH() * 0.0174532925)
        
        dt = globalClock.getDt()
        b = self.curGolfBall()
        forceMove = 500
        forceMoveDt = forceMove * dt
        posUpdate = False
        
        momentumChange = dt * 60.0
        
        if (self.arrowKeys.upPressed() or self.arrowKeys.downPressed()) and not self.golfCourse.canDrive(self.currentGolfer):
            posUpdate = True
            self.aimMomentum = 0.0
            self.ballFollow.headsUp(self.holeBottomNodePath)
        elif self.arrowKeys.rightPressed() and not self.arrowKeys.leftPressed():
            self.aimMomentum -= momentumChange
            if self.aimMomentum > 0:
                self.aimMomentum = 0.0
            elif self.aimMomentum < -30.0:
                self.aimMomentum = -30.0
            #self.ballFollow.setH(self.ballFollow.getH() - (30 * dt))
            posUpdate = True
            self.switchToAnimState('GolfRotateLeft')
            self.scoreBoard.hide()
        elif self.arrowKeys.leftPressed() and not self.arrowKeys.rightPressed():
            self.aimMomentum += momentumChange
            if self.aimMomentum < 0.0:
                self.aimMomentum = 0.0
            elif self.aimMomentum > 30.0:
                self.aimMomentum = 30.0
            #self.ballFollow.setH(self.ballFollow.getH() + (30 * dt))
            posUpdate = True
            self.switchToAnimState('GolfRotateRight')
            self.scoreBoard.hide()
        else:
            self.aimMomentum = 0.0
            self.switchToAnimState('GolfPuttLoop')
            
        self.ballFollow.setH(self.ballFollow.getH() + (self.aimMomentum * dt))
        
        # handle our ~golf drive key presses
        if self.arrowKeys.upPressed() and self.golfCourse.canDrive(self.currentGolfer):
            b.enable()
            b.addForce(Vec3(x * forceMoveDt, y * forceMoveDt,0))
        if self.arrowKeys.downPressed() and self.golfCourse.canDrive(self.currentGolfer):
            b.enable()
            b.addForce(Vec3(-x * forceMoveDt, -y * forceMoveDt,0))
        if self.arrowKeys.leftPressed() and self.arrowKeys.rightPressed() and \
           self.golfCourse.canDrive(self.currentGolfer):
            b.enable()
            b.addForce(Vec3(0,0,3000*dt))            

        if posUpdate:
            # self.notify.debug('ballFollowSpot = %s heading = %s' % (self.ballFollowToonSpot.getPos(render), self.ballFollowToonSpot.getH(render)))
            if globalClock.getFrameTime() - self.lastTimeHeadingSent > 0.2:
                self.sendUpdate('setTempAimHeading', [localAvatar.doId, self.ballFollow.getH()])
                self.lastTimeHeadingSent = globalClock.getFrameTime()
                self.lastTempHeadingSent = self.ballFollow.getH()
        else:
            # make sure everyone else has the right heading
            if self.lastTempHeadingSent != self.ballFollow.getH():
                self.sendUpdate('setTempAimHeading', [localAvatar.doId, self.ballFollow.getH()])
                self.lastTimeHeadingSent = globalClock.getFrameTime()
                self.lastTempHeadingSent = self.ballFollow.getH()                
                
        self.setCamera2Ball()
        self.fixCurrentGolferFeet()
        self.adjustClub()
        self.orientCameraRay()
 
        return task.cont

    def fixCurrentGolferFeet(self):
        """Adjust toon position in case he's standing inside the sidewalk."""
        golfer = base.cr.doId2do.get(self.currentGolfer)
        if not golfer:
            return
        golferPos = golfer.getPos(render)
        newPos = Vec3(golferPos[0], golferPos[1], golferPos[2] + 5)
        # if hasattr(self,'toonRayDebug'):
        #     self.toonRayDebug.setPos(newPos)
        # else:
        #     self.toonRayDebug = loader.loadModel('models/misc/xyzAxis')
        #     self.toonRayDebug.reparentTo(render)
        #     self.toonRayDebug.setPos(newPos)
                
        self.toonRay.setPosition(newPos)
        # self.toonRayDebugAxis2.setPos(newPos)

    def adjustClub(self):
        """Change the club so that the head is more or less behind the ball."""
        club = self.clubs[self.currentGolfer]
        if club:
            distance = club.getDistance(self.clubLookatSpot)            
            # from maya the club has a length of 2.058, 
            scaleFactor = distance / 2.058
            # self.notify.debug('scaleFactor  = %s' % scaleFactor)
            club.setScale(1, scaleFactor, 1)

    def resetPowerBar(self):
        """Bring the power and power bar to zero."""
        self.power = 0
        self.powerBar['value'] = self.power
        self.powerBar['text'] = ''

    def sendSwingInfo(self):
        """Send the power bar and angle to the AI."""
        # this is a good point to check for the warning if he hasn't pressed control
        kickHimOut = self.updateWarning()
        if kickHimOut:
            return
        curAimTime = globalClock.getRealTime() - self.enterAimStart
        if curAimTime < 0:
            curAimTime = 0
        if curAimTime > GolfGlobals.AIM_DURATION:
            curAimTime = GolfGlobals.AIM_DURATION
        self.notify.debug('curAimTime = %f' % curAimTime)
        
        x = -math.sin(self.ballFollow.getH() * 0.0174532925)
        y = math.cos(self.ballFollow.getH() * 0.0174532925)
        b = self.curGolfBall()
        # self.upSendCommonObjects()
        if hasattr(base, "golfPower") and base.golfPower != None:
            self.power = float(base.golfPower)
        if not self.swingInfoSent:
            self.sendUpdate("postSwingState", [self.getCycleTime(), self.power, b.getPosition()[0],b.getPosition()[1],b.getPosition()[2], x, y, curAimTime, self.getCommonObjectData()])
        # print "Swing State"
        # print self.getCycleTime()
        # print self.getCommonObjectData()
        self.swingInfoSent = True
        if self.power < 15 and self.golfCourse.scores[localAvatar.doId][self.golfCourse.curHoleIndex] == 0:
            self.powerReminder = DirectLabel(
                text = TTLocalizer.GolfPowerReminder,
                text_shadow = (0,0,0,1),
                text_fg = VBase4(1,1,0.0,1),
                text_align = TextNode.ACenter,
                relief = None,
                pos = (0, 0, 0.80),
                scale = 0.12)
        
    def updateWarning(self):
        """Check if he should be kicked out since he hasn't been swinging.
        Return true if should be kicked out."""
        retval = False
        if not self.localToonHitControl:
            self.localMissedSwings += 1
        else:
            self.localMissedSwings = 0
        if self.localMissedSwings == GolfGlobals.KICKOUT_SWINGS -1:
            self.warningLabel = DirectLabel(
                parent = aspect2d,
                relief = None,
                pos = (0, 0, 0),
                text_align = TextNode.ACenter,
                text = TTLocalizer.GolfWarningMustSwing,
                text_scale = 0.12,
                text_font = ToontownGlobals.getSignFont(),
                text_fg = (1, 0.1, 0.1, 1),
                text_wordwrap = 20,
                )
            self.warningInterval = Sequence(
                LerpColorScaleInterval(self.warningLabel, 10, Vec4(1,1,1,0), startColorScale = Vec4(1,1,1,1), blendType = 'easeIn'),
                Func(self.warningLabel.destroy)
                )
            self.warningInterval.start()
        elif self.localMissedSwings >=  GolfGlobals.KICKOUT_SWINGS:
            self.golfCourse.handleFallingAsleepGolf(None)
            retval = True
        return retval
        
    def assignRecordSwing(self, avId, cycleTime, power, x, y, z, dirX, dirY, commonObjectData):
        ball = self.ballDict[avId]['golfBall']
        holdBallPos = ball.getPosition()
        #holdData = self.getCommonObjectData()
        self.useCommonObjectData(commonObjectData)
        #holdTime = self.timingSimTime
        self.trackRecordBodyFlight(ball, cycleTime, power, Vec3(x,y,z), dirX, dirY)
        ball.setPosition(holdBallPos)
        self.sendUpdate("ballMovie2AI", [cycleTime, avId, self.recording, self.aVRecording, self.ballInHoleFrame, self.ballTouchedHoleFrame, self.ballFirstTouchedHoleFrame, commonObjectData, ])
        self.ballMovie2Client(cycleTime, avId, self.recording, self.aVRecording, self.ballInHoleFrame, self.ballTouchedHoleFrame, self.ballFirstTouchedHoleFrame, commonObjectData)
        #self.useCommonObjectData(holdData)
        #self.setTimeIntoCycle(holdTime)
        
    def __watchAimTask(self, task):
        """Watch another toon aim his shot."""
        self.setCamera2Ball()
        # Gah always point the club at the ball, avoid weird club penetrating ball problems
        self.attachClub(self.currentGolfer, True)
        self.adjustClub()
        self.fixCurrentGolferFeet()
        self.orientCameraRay()

        return task.cont

    def __watchTeeTask(self, task):
        self.setCamera2Ball()
        return task.cont    

    def curGolfBall(self):
        return self.ballDict[self.currentGolfer]['golfBall']
        
    def curGolfBallGeom(self):
        return self.ballDict[self.currentGolfer]['golfBallGeom']
        
    def curBallShadow(self):
        return self.ballShadowDict[self.currentGolfer]

    def cleanupGeom(self):
        """Cleanup all the geometry we create."""
        self.targets.remove()
        self.terrainModel.remove()
        self.powerBar.destroy()

    def cleanupPowerBar(self):
        self.powerBar.hide()
        
    def cleanupPhysics(self):
        """Cleanup all the physics objects we create."""
        # cleanup gravity physics
        pass

    def curBall(self):
        """Return the current ball nodePath."""
        return self.ballDict[self.currentGolfer]['ball']

    def curBallANP(self):
        """Return the current ballActorNodePath."""
        return self.ballDict[self.currentGolfer]['ballActorNodePath']

    def curBallActor(self):
        """Return the current actorNode."""
        return self.ballDict[self.currentGolfer]['ballActor']

    # ==================================================================
    #                            Aim State
    # ==================================================================
    
    def enterAim(self):
        """Enter the state where local toon aims his shot."""
        self.notify.debug("Aim")
        self.notify.debug('currentGolfer = %s' % self.currentGolfer)
        self.switchToAnimState('GolfPuttLoop', forced=True)
        self.swingInfoSent = False
        self.lastState = self.state
        self.aimMomentum = 0.0
        self.enterAimStart = globalClock.getRealTime()
        taskMgr.add(self.__aimTask, "Aim Task")
        self.showOnlyCurGolfer()
        strokes = self.golfCourse.getStrokesForCurHole(self.currentGolfer)
        if strokes:
            self.ballFollow.headsUp(self.holeBottomNodePath)
        self.resetPowerBar()
        self.powerBar.show()
        self.aimDuration = GolfGlobals.AIM_DURATION
        if not self.unlimitedAimTime:
            self.timer = ToontownTimer.ToontownTimer()
            self.timer.posInTopRightCorner()
            self.timer.setTime(self.aimDuration) 
            self.timer.countdown(self.aimDuration, self.timerExpired)
        self.aimInstructions = DirectLabel(
            text = TTLocalizer.GolfAimInstructions,
            text_shadow = (0,0,0,1),
            text_fg = VBase4(1,1,1,1),
            text_align = TextNode.ACenter,
            relief = None,
            pos = (0, 0, -0.80),
            scale = TTLocalizer.DGHAimInstructScale)
        self.skyContact = 1
        self.localToonHitControl = False
        return

    def exitAim(self):
        """Exit the state where local toon aims his shot."""
        localAvatar.wrtReparentTo(render)
        taskMgr.remove("Aim Task")
        taskMgr.remove(self.golfPowerTaskName)
        if self.timer:
            self.timer.stop()
            self.timer.destroy()
            self.timer = None
        self.powerBar.hide()
        if self.aimInstructions:
            self.aimInstructions.destroy()
            self.aimInstructions = None
        return

    def timerExpired(self):
        """Handle the aim timer expiring."""
        taskMgr.remove(self.golfPowerTaskName)
        self.aimStart = None
        self.sendSwingInfo()
        self.resetPowerBar()

    # ==================================================================
    #                            ChooseTee State
    # ==================================================================

    def enterChooseTee(self):
        """Handle entering the choose tee state."""
        self.notify.debug("ChooseTee")
        self.curGolfBallGeom().show()
        self.curBallShadow().show()
        self.lastState = self.state
        taskMgr.add(self.__chooseTeeTask, "ChooseTee Task")
        self.ballFollow.setH(self.startingTeeHeading)
        #self.showOnlyCurGolfer()
        self.localAvatarChosenTee = False
        self.localTempTee = 0
        if len(self.teePositions) > 1:
            self.localTempTee = 1

        self.chooseTeeDuration = GolfGlobals.TEE_DURATION
        if not self.unlimitedTeeTime:
            self.teeTimer = ToontownTimer.ToontownTimer()
            self.teeTimer.posInTopRightCorner()
            self.teeTimer.setTime(self.chooseTeeDuration) 
            self.teeTimer.countdown(self.chooseTeeDuration, self.teeTimerExpired)
            
        self.teeInstructions = DirectLabel(
            text = TTLocalizer.GolfChooseTeeInstructions,
            text_fg = VBase4(1,1,1,1),
            text_align = TextNode.ACenter,
            text_shadow = (0,0,0,1),
            relief = None,
            pos = (0, 0, -0.75),
            scale = TTLocalizer.DGHTeeInstructScale)
        self.powerBar.hide()

        return

    def exitChooseTee(self):
        """Handle exiting the choose tee state."""
        localAvatar.wrtReparentTo(render)
        if hasattr(self, "teeInstructions") and self.teeInstructions:
            self.teeInstructions.destroy()
        self.teeInstructions = None
        taskMgr.remove("ChooseTee Task")
        taskMgr.remove(self.golfPowerTaskName)
        if self.teeTimer:
            self.teeTimer.stop()
            self.teeTimer.destroy()
            self.teeTimer = None
        self.powerBar.show()
        return

    def sendTeeInfo(self):
        """Send the chosen tee to the AI."""
        self.sendUpdate('setAvatarTee', [self.localTempTee])
        self.localAvatarChosenTee = True

    def __chooseTeeTask(self, task):
        """Respond to the user's inputs to choose a starting tee position"""
        if self.localAvatarChosenTee:
            return task.done
        if self.arrowKeys.jumpPressed():
            if self.flyOverInterval and self.flyOverInterval.isPlaying():
                pass
            else:
                self.sendTeeInfo()

        return task.cont

    def changeTee(self, newTee):
        """Change the starting tee for the current golfer."""
        assert self.notify.debugStateCall(self)
        ball = self.curGolfBall()
        ball.setPosition(self.teePositions[newTee])
        self.setCamera2Ball()
        self.fixCurrentGolferFeet()
        self.adjustClub()

    def changeLocalTee(self, newTee):
        """Change the starting tee for the local golfer."""
        self.changeTee(newTee)
        # tell other clients too
        self.sendUpdate('setAvatarTempTee',[localAvatar.doId, newTee])
        self.fixCurrentGolferFeet()
        self.adjustClub()
        
    def __leftArrowPressed(self):
        """Handle the player's initial press of the left arrow key."""
        if self.state != 'ChooseTee':
            return
        self.localTempTee -= 1
        if self.localTempTee < 0:
            self.localTempTee = len(self.teePositions) -1
        self.changeLocalTee(self.localTempTee)
            
    def __rightArrowPressed(self):
        """Handle the player's initial press of the left arrow key."""
        if self.state != 'ChooseTee':
            return
        self.localTempTee += 1
        self.localTempTee %= len(self.teePositions)           
        self.changeLocalTee(self.localTempTee)

    def teeTimerExpired(self):
        """Handle the tee timer expiring."""
        self.sendTeeInfo()

    # ==================================================================
    #                            WatchAim State
    # ==================================================================

    def enterWatchAim(self):
        """Enter the state where we watch another toon aim his shot."""
        self.notify.debug("Watch Aim")
        self.notify.debugStateCall(self)        
        self.notify.debug('currentGolfer = %s' % self.currentGolfer)
        strokes = self.golfCourse.getStrokesForCurHole(self.currentGolfer)
        if strokes:
            self.ballFollow.lookAt(self.holeBottomNodePath)
            self.ballFollow.setP(0)        
        self.showOnlyCurGolfer()
        #taskMgr.add(self.__controlTask, "watchBall")
        taskMgr.add(self.__watchAimTask, "Watch Aim Task")
        pass
    
    def exitWatchAim(self):
        """Exit the state where we watch another toon aim his shot."""
        self.notify.debugStateCall(self)
        av = base.cr.doId2do.get(self.currentGolfer)
        if av:
            heading = av.getH(render)
            toonPos = av.getPos(render)
            av.reparentTo(render)
            av.setH(heading)
            av.setPos(toonPos)
            self.notify.debug('av %s now at position %s' % (av.getName(), av.getPos()))
        else:
            self.notify.debug('could not get avId %d' % self.currentGolfer)
        taskMgr.remove("Watch Aim Task")
        pass

    def enterWatchTee(self):
        """Enter the state where we watch another toon choose his starting tee."""
        self.notify.debug("Watch Tee")
        self.notify.debugStateCall(self)
        self.curGolfBallGeom().show()
        self.ballFollow.setH(self.startingTeeHeading)
        #self.showOnlyCurGolfer()
        self.ballShadowDict[self.currentGolfer].show()
        pass
    
    def exitWatchTee(self):
        """Exit the state where we watch another toon choose his starting tee."""        
        self.notify.debugStateCall(self)
        
        av = base.cr.doId2do.get(self.currentGolfer)
        taskMgr.remove("Watch Tee Task")
        pass    

    def enterWait(self):
        """Handle entering the wait state."""
        self.notify.debug ("Wait")
        self.notify.debugStateCall(self)
        pass
    
    def exitWait(self):
        """Handle exiting the wait state."""        
        self.notify.debugStateCall(self)
        pass
        
    def removePlayBackDelayDelete(self):
        if self.playBackDelayDelete:
            self.playBackDelayDelete.destroy()
            self.playBackDelayDelete = None
        
    def enterPlayback(self):
        """Handle entering the plabyack state."""
        def shiftClubToRightHand():
            club = self.clubs[self.currentGolfer]
            av = base.cr.doId2do.get(self.currentGolfer)
            if av and club:
                club.wrtReparentTo( av.getRightHands()[0])
                #club.setHpr(0,0,0)
        av = base.cr.doId2do.get(self.currentGolfer)
        if not av:
            return
        else:
            self.removePlayBackDelayDelete()
            self.playBackDelayDelete = DelayDelete.DelayDelete(av, 'GolfHole.enterPlayback')

        # handle gracefully if the user exits by closing toontown window
        self.accept('clientCleanup', self._handleClientCleanup)
        
        self.inPlayBack = 1                
        self.setLookingAtPutt(False)
        self.swingInterval = Sequence(
            ActorInterval(av, 'swing-putt', startFrame = 0, endFrame = GolfGlobals.BALL_CONTACT_FRAME),
            Func(self.startBallPlayback),            
            ActorInterval(av, 'swing-putt', startFrame = GolfGlobals.BALL_CONTACT_FRAME, endFrame = 23),
            Func(shiftClubToRightHand),
            Func(self.setLookingAtPutt, True),
            Func(self.removePlayBackDelayDelete),
            )

        # we have to correct for the time the toon swings before he hits the ball
        adjustedBallTouchedHoleTime = self.ballTouchedHoleTime + GolfGlobals.BALL_CONTACT_TIME
        adjustedBallFirstTouchedHoleTime = self.ballFirstTouchedHoleTime + GolfGlobals.BALL_CONTACT_TIME
        adjustedBallDropTime = self.ballDropTime + GolfGlobals.BALL_CONTACT_TIME
        adjustedPlaybackEndTime = self.playbackMovieDuration + GolfGlobals.BALL_CONTACT_TIME

        self.notify.debug('adjustedTimes ballTouched=%.2f ballFirstTouched=%.2f ballDrop=%.2f playbaybackEnd=%.2f' \
                          % (adjustedBallTouchedHoleTime, adjustedBallFirstTouchedHoleTime, adjustedBallDropTime,
                             adjustedPlaybackEndTime))
                             
        if self.ballWillGoInHole:
            curDuration = self.swingInterval.getDuration()
            lookPuttInterval = ActorInterval(av,'look-putt')
            if curDuration < adjustedBallDropTime:
                self.swingInterval.append(lookPuttInterval)
            curDuration = self.swingInterval.getDuration()
            diffTime = adjustedBallDropTime - curDuration
            if diffTime > 0:
                self.swingInterval.append(
                    ActorInterval(av, 'lookloop-putt', endTime = diffTime))
            self.swingInterval.append(
                ActorInterval(av, 'good-putt', endTime = self.playbackMovieDuration , loop=1))

        elif self.ballTouchedHoleTime:
            self.notify.debug('doing self.ballTouchedHoleTime')
            # do the bad putt animation when the ball passes
            curDuration = self.swingInterval.getDuration()
            lookPuttInterval = ActorInterval(av,'look-putt')
            if curDuration < adjustedBallTouchedHoleTime : 
                self.swingInterval.append(lookPuttInterval)
            curDuration = self.swingInterval.getDuration()
            diffTime = adjustedBallTouchedHoleTime - curDuration
            if diffTime > 0:
                self.swingInterval.append(
                    ActorInterval(av, 'lookloop-putt', endTime = diffTime))
            self.swingInterval.append(
                ActorInterval(av, 'bad-putt', endFrame = 32))
            self.swingInterval.append(
                ActorInterval(av, 'badloop-putt',
                              endTime = self.playbackMovieDuration,
                              loop=1))                
        else:
            self.swingInterval.append(
                ActorInterval(av, 'look-putt'))
            self.swingInterval.append(
                ActorInterval(av, 'lookloop-putt', endTime = self.playbackMovieDuration, loop=1))

        # now setup the sfx
        sfxInterval = Parallel()
        # handle ball Hit sound
        ballHitInterval = Sequence(
            Wait(GolfGlobals.BALL_CONTACT_TIME),
            SoundInterval(self.hitBallSfx)
            )
        sfxInterval.append(ballHitInterval)

        # handle ball rattle sounds
        if self.ballWillGoInHole:
            ballRattle = Sequence()
            timeToPlayBallRest = adjustedPlaybackEndTime - self.ballGoesToRestSfx.length()
            if adjustedBallFirstTouchedHoleTime < timeToPlayBallRest:
                diffTime = timeToPlayBallRest - adjustedBallFirstTouchedHoleTime
                # do we have more than enough time to play the full rattling sound?
                if self.ballGoesInStartSfx.length() < diffTime:
                    ballRattle.append(Wait(adjustedBallFirstTouchedHoleTime))
                    ballRattle.append(SoundInterval(self.ballGoesInStartSfx))
                    timeToPlayLoop = adjustedBallFirstTouchedHoleTime + self.ballGoesInStartSfx.length()
                    loopTime = timeToPlayBallRest - timeToPlayLoop
                    # handle null audio file case                    
                    if self.ballGoesInLoopSfx.length() == 0.0:
                        numLoops = 0
                    else:
                        numLoops = int(loopTime / self.ballGoesInLoopSfx.length())
                    self.notify.debug('numLoops=%d loopTime=%f' % (numLoops, loopTime))
                    if loopTime > 0:
                        ballRattle.append(SoundInterval(self.ballGoesInLoopSfx,loop=1, duration = loopTime, seamlessLoop=True))
                    ballRattle.append(SoundInterval(self.ballGoesToRestSfx))
                    self.notify.debug('playing full rattling')
                    # self.notify.debug('ballRattle=%s' % ballRattle)
                else:
                    # we play an abbreviated rattling sound
                    self.notify.debug('playing abbreviated rattling')                    
                    timeToPlayBallGoesIn = adjustedBallFirstTouchedHoleTime
                    ballRattle.append(Wait(timeToPlayBallGoesIn))
                    startTime = self.ballGoesInStartSfx.length() - diffTime
                    self.notify.debug('adjustedBallDropTime=%s diffTime=%s starTime=%s' %
                                  (adjustedBallDropTime, diffTime, startTime))
                    ballRattle.append(SoundInterval(self.ballGoesInStartSfx, startTime = startTime))
                    ballRattle.append(SoundInterval(self.ballGoesToRestSfx))
                    # self.notify.debug('ballRattle=%s' % ballRattle)
            else:
                # just play the abbreviated  goes to rest sfx
                self.notify.debug('playing abbreviated ball goes to rest')
                ballRattle.append(Wait(adjustedBallFirstTouchedHoleTime))
                diffTime = adjustedPlaybackEndTime - adjustedBallFirstTouchedHoleTime
                startTime = self.ballGoesToRestSfx.length() - diffTime
                self.notify.debug('adjustedBallDropTime=%s diffTime=%s starTime=%s' %
                                  (adjustedBallDropTime, diffTime, startTime))
                ballRattle.append(SoundInterval(self.ballGoesToRestSfx, startTime = startTime))
                # self.notify.debug('ballRattle=%s' % ballRattle)
            sfxInterval.append(ballRattle)

        # handle crowd sounds
        crowdBuildupSfx = self.crowdBuildupSfx[ self.avIdList.index(self.currentGolfer)]
        crowdApplauseSfx = self.crowdApplauseSfx[ self.avIdList.index(self.currentGolfer)]
        crowdMissSfx = self.crowdMissSfx[ self.avIdList.index(self.currentGolfer)]
        if self.ballWillGoInHole:
            crowdIval = Sequence()
            buildupLength = crowdBuildupSfx.length()
            self.notify.debug('buildupLength=%s' % buildupLength)
            diffTime = adjustedBallFirstTouchedHoleTime - buildupLength
            if diffTime > 0:
                crowdIval.append(Wait(diffTime))
                crowdIval.append(SoundInterval(crowdBuildupSfx))
                crowdIval.append(SoundInterval(crowdApplauseSfx))
            else:
                startTime = buildupLength - adjustedBallFirstTouchedHoleTime
                self.notify.debug('playing abbreviated crowd build and applause diffTime=%s startTime=%s' %
                                  (diffTime, startTime))                
                crowdIval.append(SoundInterval(crowdBuildupSfx, startTime = startTime))
                crowdIval.append(SoundInterval(crowdApplauseSfx))
            sfxInterval.append(crowdIval)
        elif self.ballFirstTouchedHoleTime:
            crowdIval = Sequence()
            buildupLength = crowdBuildupSfx.length()
            self.notify.debug('touched but not going in buildupLength=%s' % buildupLength)
            diffTime = adjustedBallFirstTouchedHoleTime - buildupLength
            if diffTime > 0:
                self.notify.debug('waiting %.2f to play crowd buildup' % diffTime)
                crowdIval.append(Wait(diffTime))
                crowdIval.append(SoundInterval(crowdBuildupSfx))
                crowdIval.append(SoundInterval(crowdMissSfx))
            else:
                startTime = buildupLength - adjustedBallFirstTouchedHoleTime
                self.notify.debug('playing abbreviated crowd build and miss diffTime=%s startTime=%s' %
                                  (diffTime, startTime))                
                crowdIval.append(SoundInterval(crowdBuildupSfx, startTime = startTime))
                crowdIval.append(SoundInterval(crowdMissSfx))
            sfxInterval.append(crowdIval)            
            
            
        # change swing Interval to parallel, to handle the sfx 
        #temp = self.swingInterval
        #self.swingInterval = Parallel(
        #    temp,
        #    sfxInterval
        #    )

        # we want the sound to continue even when swingInterval is stopped
        if self.sfxInterval:
            sfxInterval.finish()
        self.sfxInterval = sfxInterval
        self.sfxInterval.start()
        self.swingInterval.start()
        pass
        
        
    def exitPlayback(self):
        """Handle exiting the plabyack state."""
        self.notify.debug("Exiting Playback")
        if self.swingInterval:
            self.swingInterval.pause()
        av = base.cr.doId2do.get(self.currentGolfer)
        if av:
            if self.ballWillGoInHole:
                # we need this so we don't get a noticeable pause on the spectator
                av.loop('good-putt', restart=0)
                pass
            elif self.ballTouchedHoleTime:
                pass
            else:
                av.loop('neutral')
        self.setLookingAtPutt(False)
        if av == base.localAvatar:
            if self.ballWillGoInHole:
                av.b_setAnimState('GolfGoodPutt')
            elif self.ballTouchedHoleTime:
                av.b_setAnimState('GolfBadPutt')
            else:
                av.b_setAnimState('neutral')                

        taskMgr.remove("playback task")
        self.curGolfBall().disable()
        self.readyCurrentGolfer(None)
        #self.notify.debug("Playback End time %s cycle %s" % (self.timingSimTime, self.getSimCycleTime()))
        #self.startSim()
        self.inPlayBack = 0
        pass
        if self.powerReminder:
            self.powerReminder.destroy()
            self.powerReminder = None

    def setLookingAtPutt(self, newVal):
        """Change the flag if the current golfer is doing the look-putt anim."""
        self.isLookingAtPutt = newVal

    def getLookingAtPutt(self):
        """return the flag if the current golfer is doing the look-putt anim."""
        return self.isLookingAtPutt 

    def startBallPlayback(self):
        self.playbackFrameNum = 0
        
        self.sourceFrame = self.recording[0]
        self.destFrameNum = 1
        self.destFrame = self.recording[self.destFrameNum]
        
        self.aVSourceFrame = self.aVRecording[0]
        self.aVDestFrameNum = 1
        self.aVDestFrame = self.aVRecording[self.aVDestFrameNum]
        
        # self.timingSimTime = self.holdCycleTime
        # self.useCommonObjectData(self.holdCommonObjectData)
        # taskMgr.add(self.__playbackTask, "playback task", priority = 10)
        # self.stopSim()
        self.inPlayBack = 2        

    def isCurBallInHole(self):
        """Returns True if the current ball is inside a hole, False otherwise."""
        # Warning keep this in sync with the ai version
        retval = False
        ball = self.curGolfBall()
        ballPos = ball.getPosition()
        for holePos in self.holePositions:
            displacement = ballPos - holePos
            length = displacement.length()
            self.notify.debug('hole %s length=%s' % (holePos, length))
            if length <= GolfGlobals.DistanceToBeInHole:
                retval = True;
                break;
        return retval

    def handleBallGoingInHole(self):
        """The ball fell in the hole, give some sort of feedback to the user."""
        par = GolfGlobals.HoleInfo[self.holeId]['par']
        # move the ball underground so it isn't seen
        unlimitedSwing = False
        av = base.cr.doId2do.get(self.currentGolfer)
        if av:
            unlimitedSwing = av.getUnlimitedSwing()
        if not unlimitedSwing:
            self.curGolfBall().setPosition(0,0,-100)
            self.ballShadowDict[self.currentGolfer].setPos(0,0,-100)
            self.ballShadowDict[self.currentGolfer].hide()
        strokes = 3
        if self.golfCourse:
            strokes = self.golfCourse.getStrokesForCurHole(self.currentGolfer)
        else:
            self.notify.warning('self.golfCourse is None')

        diff = strokes - par
        if diff > 0:
            textStr = '+' + str(diff)
        else:
            textStr = diff

        if strokes == 1:
            textStr = TTLocalizer.GolfHoleInOne
        elif diff in TTLocalizer.GolfShotDesc:
            if self.ballWillGoInHole:
                textStr = TTLocalizer.GolfShotDesc[diff]

        # copied and pasted from the perfect stuff in DistributedCatchGame
        perfectTextSubnode = hidden.attachNewNode(
            self.__genText(textStr))
        perfectText = hidden.attachNewNode('perfectText')
        perfectTextSubnode.reparentTo(perfectText)
        # offset the subnode so that the text is centered on both axes
        # we need the parent node so that the text will scale correctly
        frame = self.__textGen.getCardActual()
        offsetY = -abs(frame[2] + frame[3])/2.0 - 1.35
        perfectTextSubnode.setPos(0,0,offsetY)

        perfectText.setColor(1,.1,.1,1)

        def fadeFunc(t, text=perfectText):
            text.setColorScale(1,1,1,t)
        def destroyText(text=perfectText):
            text.removeNode()

        animTrack = Sequence()
        av = base.cr.doId2do.get(self.currentGolfer)
        #if av:
        #    animTrack.append(ActorInterval(av, 'good-putt'))
        animTrack.append(Func(self.golfCourse.updateScoreBoard))
        textTrack = Sequence(
            Func(perfectText.reparentTo, aspect2d),
            Parallel(LerpScaleInterval(perfectText, duration=.5,
                                       scale=.3, startScale=0.),
                     LerpFunctionInterval(fadeFunc,
                                          fromData=0., toData=1.,
                                          duration=.5,)
                     ),
            Wait(2.),
            Parallel(LerpScaleInterval(perfectText, duration=.5,
                                       scale=1.),
                     LerpFunctionInterval(fadeFunc,
                                          fromData=1., toData=0.,
                                          duration=.5,
                                          blendType="easeIn"),
                     ),
            Func(destroyText),
            WaitInterval(.5),
            #Func(endGame, None),
            Func(self.sendUpdate,"turnDone", [])
            )

        soundTrack = Sequence() #SoundInterval(self.sndPerfect)
        if strokes == 1:
            soundTrack.append(SoundInterval(self.holeInOneSfx))
        elif self.hasCurGolferReachedMaxSwing and not self.ballWillGoInHole:
            soundTrack.append(SoundInterval(self.kickedOutSfx))

        self.perfectIval = Parallel(textTrack,
                                    soundTrack,
                                    animTrack)
        self.perfectIval.start()            
        
    
    def __playbackTask(self, task):
        return self.playBackFrame(task)

    def toonRayCollisionCallback(self, x, y, z):
        """Handle getting the position of the toon's feet position."""
        if self.state not in ( 'Aim', 'WatchAim', 'ChooseTee', 'WatchTee'):
            return
        # self.notify.debug('toonRay at %s %s %s' % (x,y,z))
        # self.toonRayDebugAxis.setPos(x, y, z)
        tempPath = render.attachNewNode('temp')
        tempPath.setPos(x, y, z)
        relPos = tempPath.getPos(self.ballFollowToonSpot)
        av = base.cr.doId2do.get(self.currentGolfer)
        if av:
            zToUse = relPos[2]
            if zToUse < (0 - GolfGlobals.GOLF_BALL_RADIUS):
                zToUse = (0 - GolfGlobals.GOLF_BALL_RADIUS)
            av.setPos(0, 0, zToUse)
        tempPath.removeNode()
        
    def preStep(self):
        if self.currentGolferActive:
            GolfHoleBase.GolfHoleBase.preStep(self)

    def postStep(self):
        if self.currentGolferActive:
            GolfHoleBase.GolfHoleBase.postStep(self)
            DistributedPhysicsWorld.DistributedPhysicsWorld.postStep(self)
            if self.inPlayBack == 2:
                self.playBackFrame()
                self.makeCurGolferLookAtBall()
            elif self.state == 'Playback' and self.inPlayBack == 0:
                self.request('Wait')

            self.updateTranslucentObjects()

    def updateTranslucentObjects(self):
        """Solidify or make translucent our objects as appropriate."""
        for translucentNodePathLastFrame in self.translucentLastFrame:
            if translucentNodePathLastFrame not in self.translucentCurFrame:
                # we were translucent 1 frame ago but not anymore
                translucentNodePathLastFrame.setColorScale(1,1,1,1)
        for transNpCurFrame in self.translucentCurFrame:
            if transNpCurFrame  not in self.translucentLastFrame:
                # we are translucent now but not 1 frame ago
                self.notify.debug('making translucent %s' %  transNpCurFrame )
                transNpCurFrame.setColorScale(1,1,1,0.25)
                transNpCurFrame.setTransparency(1)

    def makeCurGolferLookAtBall(self):
        """Make the current golfer look at the ball as it moves."""
        if self.getLookingAtPutt():
            av = base.cr.doId2do.get(self.currentGolfer)
            if av:
                ballPos = self.curGolfBall().getPosition()
                av.headsUp(ballPos[0], ballPos[1], ballPos[2])
                av.setH(av.getH() -90)

            
    def playBackFrame(self):
        """Play back one frame of the golf ball movie."""
        doPrint = 0
        doAVPrint = 0
        lastFrame = self.recording[len(self.recording) - 1][0]
        
        # position
        if self.playbackFrameNum >= self.destFrame[0]:
            self.sourceFrame = self.destFrame
            self.destFrameNum += 1
            doPrint = 1
            if self.destFrameNum < (len(self.recording)):
                self.destFrame = self.recording[self.destFrameNum]
                #print self.destFrame
            else:  
                self.notify.debug("recording length %s" % (len(self.recording)))
                if self.isCurBallInHole() or self.hasCurGolferReachedMaxSwing():
                    self.handleBallGoingInHole()
                    self.request("Wait")
                else:
                    self.golfCourse.updateScoreBoard()
                    self.request("Wait")
                    self.sendUpdate("turnDone", [])
                return
    
        self.projLength = self.destFrame[0] - self.sourceFrame[0]
        self.projPen = self.destFrame[0] - self.playbackFrameNum
        propSource = float(self.projPen) / float(self.projLength)
        propDest = 1.0 - propSource
        
        projX = self.sourceFrame[1] * propSource + self.destFrame[1] * propDest
        projY = self.sourceFrame[2] * propSource + self.destFrame[2] * propDest
        projZ = self.sourceFrame[3] * propSource + self.destFrame[3] * propDest
        
        newPos = Vec3(projX, projY, projZ)
        
        ball = self.curGolfBall()
        ball.setPosition(newPos)
        
        # angular velocity
        
        if self.playbackFrameNum >= self.aVDestFrame[0]:
            self.aVSourceFrame = self.aVDestFrame
            self.aVDestFrameNum += 1
            doAVPrint = 1
            if self.aVDestFrameNum < len(self.aVRecording):
                self.aVDestFrame = self.aVRecording[self.aVDestFrameNum]
                newAV = Vec3(self.aVSourceFrame[1] , self.aVSourceFrame[2] , self.aVSourceFrame[3] )
                #ball.setAngularVel(newAV)
    
        self.projLength = self.aVDestFrame[0] - self.aVSourceFrame[0]
        self.projPen = self.aVDestFrame[0] - self.playbackFrameNum
        propSource = float(self.projPen) / float(self.projLength)
        propDest = 1.0 - propSource
        
        projX = self.aVSourceFrame[1] * propSource + self.aVDestFrame[1] * propDest
        projY = self.aVSourceFrame[2] * propSource + self.aVDestFrame[2] * propDest
        projZ = self.aVSourceFrame[3] * propSource + self.aVDestFrame[3] * propDest
        
        newAV = Vec3(projX, projY, projZ)
        
        ball = self.curGolfBall()
        ball.setAngularVel(newAV)

        if self.playbackFrameNum < (lastFrame - 1):
            ball.enable()
        else:
            ball.disable()
            #print "disable after playback"
        self.setCamera2Ball()
        self.placeBodies() 
        if doAVPrint: 
            #print ("av %s %s" % (self.playbackFrameNum, newAV))
            pass
        if doPrint: 
            
            self.notify.debug(". %s %s %s %s %s" % (self.playbackFrameNum, self.sourceFrame[0], self.destFrame[0], self.destFrameNum, newPos))
        self.playbackFrameNum +=1
        return

        
    def enterCleanup(self):
        #print("GOLF HOLE CLEANUP")
        """Handle entering the cleanup state."""
        assert self.notify.debugStateCall(self)
        taskMgr.remove("update task")
        #taskMgr.remove("golfPhysics")
        if hasattr(self, "arrowKeys"):
            self.arrowKeys.destroy()
        self.arrowKeys = None
        self.ignoreAll()
        if self.swingInterval:
            self.swingInterval.pause()
            self.swingInterval = None
        if self.sfxInterval:
            self.sfxInterval.pause()
            self.sfxInterval = None

        # TODO remove geometry e.g. self.targets.removeNode()
        self.cleanupGeom()
        #self.cleanupPhysics()
        

    def exitCleanup(self):
        """Handle exiting the cleanup state."""
        assert self.notify.debugStateCall(self)        
        pass
        
            
    def setCamera2Ball(self):
        """Set the ball follow to the correct position."""
        # normally the camera is parented to ball follow, but it could be
        # parented to render when in top view
        b = self.curGolfBall()
        ballPos = Point3(b.getPosition()[0],b.getPosition()[1],b.getPosition()[2])
        self.ballFollow.setPos(ballPos)
        
    def hitBall(self, ball,power, x, y):
        #self.sendUpdate("postSwing", [self.getCycleTime(), power, ball.getPosition[0], ball.getPosition[1], ball.getPosition[2], x, y])
        self.performSwing(self, ball, power, x, y)
        
    def ballMovie2Client(self, cycleTime, avId, movie, spinMovie, ballInFrame, ballTouchedHoleFrame, ballFirstTouchedHoleFrame, commonObjectData):
        self.notify.debug("received Movie, number of frames %s %s ballInFrame=%d ballTouchedHoleFrame=%d ballFirstTouchedHoleFrame=%d" % (len(movie), len(spinMovie), ballInFrame, ballTouchedHoleFrame, ballFirstTouchedHoleFrame))
        if self.state == 'Playback':
            self.notify.debug("SMASHED PLAYBACK")
            return
        #self.setTimeIntoCycle(cycleTime, 1)
        #self.timingSimTime = cycleTime

        self.ballShadowDict[avId].show()
        self.holdCycleTime = cycleTime
        self.holdCommonObjectData = commonObjectData
        #self.setTimeIntoCycle(self.holdCycleTime)
        self.useCommonObjectData(self.holdCommonObjectData)
        #print ("Before enterplayback")
        #print self.holdCycleTime
        #print self.holdCommonObjectData
        #self.useCommonObjectData(commonObjectData)
        #print ("Receiving Time in Cycle %s" % (self.getCycleTime()))
        self.recording = movie
        self.aVRecording = spinMovie        
        endingBallPos = Vec3(movie[-1][1],movie[-1][2], movie[-1][3])
        endingFrame = movie[-1][0]
        self.playbackMovieDuration = endingFrame * self.DTAStep
        self.notify.debug('playback movie duration=%s' % self.playbackMovieDuration)
        displacement = self.holePositions[0] - endingBallPos
        self.ballWillGoInHole = False
        if displacement.length()<= GolfGlobals.DistanceToBeInHole:
            self.ballWillGoInHole = True
        self.notify.debug('endingBallPos=%s, distanceToHole=%s, ballWillGoInHole=%s' %
                          (endingBallPos, displacement.length(), self.ballWillGoInHole))
        self.ballDropTime = ballInFrame * self.DTAStep
        self.ballTouchedHoleTime = ballTouchedHoleFrame * self.DTAStep
        self.ballFirstTouchedHoleTime = ballFirstTouchedHoleFrame * self.DTAStep
        if self.state == 'WatchTee':
            self.request('WatchAim')
        self.request('Playback')
        
    def golfersTurn(self, avId):
        """Handle telling us a different avId will take his turn."""
        assert self.notify.debug("golfers Turn %s" % (avId))
        self.readyCurrentGolfer(avId)
        if avId == localAvatar.doId:
            self.setCamera2Ball()
            self.request('Aim')
        else:
            self.setCamera2Ball()
            self.request('WatchAim')
            
            
    def readyCurrentGolfer(self, avId):
         for index in self.ballDict:
             self.ballDict[index]['golfBallOdeGeom'].setCollideBits(BitMask32(0x00000000))
             self.ballDict[index]['golfBallOdeGeom'].setCategoryBits(BitMask32(0x00000000))
             self.ballDict[index]['golfBall'].disable()
         if avId:
             self.currentGolfer = avId
             self.currentGolferActive = True
             if avId in self.ballDict:
                 self.ballDict[avId]['golfBallOdeGeom'].setCollideBits(BitMask32(0x00ffffff))
                 self.ballDict[avId]['golfBallOdeGeom'].setCategoryBits(BitMask32(0xff000000))
         else:
            self.currentGolferActive = False
            
    def setGolferIds(self, avIds):
        """
        called by the AI, this tells us the avatar ids of
        the avatars that will be in the game. NOTE: the avatar
        ids cannot be used to access the avatars until
        setGameReady() is called by the AI!

        This is a required field, so it will be called before the
        object is 'officially' created
        """
        self.avIdList = avIds
        self.numPlayers = len(self.avIdList)

        # -1 means he hasn't chosen a tee pos yet, otherwise its 0-left, 1-center or 2-right
        self.teeChosen = {}
        for avId in self.avIdList:
            self.teeChosen[avId] = -1        

    def setHoleId(self, holeId):
        """Set the hole id as dictated by the AI."""
        assert self.notify.debugStateCall(self)
        self.holeId = holeId
        self.holeInfo = GolfGlobals.HoleInfo[holeId]
        
    def createBall(self, avId, index = None):
        """Create the ball for this avatar."""
        golfBallGeom, golfBall, odeGeom = self.createSphere(self.world, self.space, GolfGlobals.GOLF_BALL_DENSITY, GolfGlobals.GOLF_BALL_RADIUS, index)
        startPos = self.teePositions[0]
        if len (self.teePositions ) > 1:
            startPos = self.teePositions[1]
        golfBall.setPosition( startPos)
        golfBallGeom.hide()

        if self.notify.getDebug():
            self.notify.debug('golf ball body id')
            golfBall.write()
            self.notify.debug(' -')
        

        golfBallGeom.setName('golfBallGeom%s' % avId)
        self.ballDict[avId] = {'golfBall': golfBall,
                               'golfBallGeom' : golfBallGeom,
                               'golfBallOdeGeom' : odeGeom,
                               }
        
        golfBall.disable()
        
        shadow = self.dropShadowModel.copyTo(render)
        #shadow = render.attachNewNode("blank")
        shadow.setBin('shadow', 100)
        shadow.setScale(0.09)
        shadow.setDepthWrite(False)
        shadow.setDepthTest(True)
        self.ballShadowDict[avId] = shadow
        shadow.hide()

    def setGolfCourseDoId(self, golfCourseDoId):
        """set the doid of golf course we are a part of."""
        self.golfCourseDoId = golfCourseDoId
        self.golfCourse = base.cr.doId2do.get(self.golfCourseDoId)

        if not self.golfCourse:
            self.cr.relatedObjectMgr.abortRequest(self.golfCourseRequest)
            self.golfCourseRequest = self.cr.relatedObjectMgr.requestObjects(
                [self.golfCourseDoId],  eachCallback = self.__gotGolfCourse)
        else:
            self.scoreBoard = self.golfCourse.scoreBoard
            self.scoreBoard.hide()

    def __gotGolfCourse(self, golfCourse):
        """Handle the golf course being generated."""
        self.golfCourseRequest = None
        self.golfCourse = golfCourse


    def __genText(self, text):
        self.__textGen.setText(text)
        return self.__textGen.generate()

        
        
    def sendBox(self,  pos0, pos1, pos2,
                       quat0, quat1, quat2, quat3,
                       anV0, anV1, anV2,
                       lnV0, lnV1, lnV2):
        self.swingBox.setPosition(pos0, pos1, pos2)
        self.swingBox.setQuaternion(Quat(quat0, quat1, quat2, quat3))
        self.swingBox.setAngularVel(anV0, anV1, anV2)
        self.swingBox.setLinearVel(lnV0, lnV1, lnV2)
        


    def hasCurGolferReachedMaxSwing(self):
        """Return true if the golfer has reached the maximum number of swings allowed."""
        strokes = self.golfCourse.getStrokesForCurHole(self.currentGolfer)
        maxSwing = self.holeInfo['maxSwing']
        retval = strokes >= maxSwing
        if retval:
            # double check that this golfer doesn't have unlimited swings
            #av = base.cr.doId2do.get(self.activeGolferId)
            #if av:
            #    if av.getUnlimitedSwing():
            #        retval = False
            # for now just show the score even if he has unlimited swing
            # only developers should have access to it anyway
            pass
        return retval

    def __getGolfPower(self, time):
        """Return a value between 0 and 100 to indicate golf power."""
        elapsed = max(time - self.aimStart, 0.0)
        t = elapsed / self.golfPowerSpeed
        t = math.pow(t, self.golfPowerExponent)
        power = int(t * 100) % 200
        if power > 100:
            power = 200 - power
        return power

    def __beginTossGolf(self):
        """Handle player pressing control and starting the power meter."""        
        # The toss-golf key was pressed.
        if self.aimStart != None:
            # This is probably just key-repeat.
            return

        if not self.state == 'Aim':
            return

        if self.swingInfoSent:
            return

        self.localToonHitControl = True
        time = globalClock.getFrameTime()
        self.aimStart = time
        messenger.send('wakeup')

        self.scoreBoard.hide()

        taskMgr.add(self.__updateGolfPower, self.golfPowerTaskName)
        
    def __endTossGolf(self):
        """Handle player releasing control and shooting the ball."""        
        if self.aimStart == None:
            return

        if not self.state == 'Aim':
            return        

        messenger.send('wakeup')

        # The toss-golf key was released.  Toss the golf.
        taskMgr.remove(self.golfPowerTaskName)
        self.aimStart = None
        self.sendSwingInfo()
        self.resetPowerBar()        

    def __updateGolfPower(self, task):
        """Change the value of the power meter."""
        if not self.powerBar:
            print "### no power bar!!!"
            return Task.done

        newPower =  self.__getGolfPower(globalClock.getFrameTime())
        self.power = newPower
        self.powerBar['value'] = newPower
        self.powerBar['text'] = TTLocalizer.GolfPowerBarText % {'power' : newPower}
        
        return Task.cont

    def golferChooseTee(self, avId):
        """Handle the AI telling us this golfer needs to choose his starting tee."""
        assert self.notify.debug("golferChoseTee  %s" % (avId))
        self.readyCurrentGolfer(avId)
        
        #for id in self.avIdList:
        #    av = base.cr.doId2do.get(id)
        #    if av:
        #        av.hide()

        self.putAwayAllToons()
        
        #self.ballShadowDict[self.currentGolfer].show()
        if self.needToDoFlyOver and self.doFlyOverMovie(avId):
            # a request will be done to transition to the right state
            # at end of flyover movie
            pass        
        else:
            if avId == localAvatar.doId:
                self.setCamera2Ball()
                if not self.state == 'ChooseTee':
                    self.request('ChooseTee')
            else:
                self.setCamera2Ball()
                self.request('WatchTee')
            self.takeOutToon(self.currentGolfer)
                
        #av = base.cr.doId2do.get(self.currentGolfer)
        #if av:
        #    av.show()
            

    def setAvatarTempTee(self, avId, tempTee):
        """Handle other player telling us his temporary tee position."""
        assert self.notify.debugStateCall(self)
        if self.state != 'WatchTee':
            return
        if avId != self.currentGolfer:
            self.notify.warning('setAvatarTempTee avId=%s not equal to self.currentGolfer=%s' %(avId, self.currentGolfer))
            return
        self.changeTee(tempTee)

    def setAvatarFinalTee(self,avId, finalTee):
        """Handle ai telling us his final tee position."""
        assert self.notify.debugStateCall(self)
        if avId != self.currentGolfer:
            self.notify.warning('setAvatarTempTee avId=%s not equal to self.currentGolfer=%s' %(avId, self.currentGolfer))
            return
        self.changeTee(finalTee)

    def setTempAimHeading(self, avId, heading):
        """Handle current golfer telling us the heading for his aim."""
        if avId != self.currentGolfer:
            self.notify.warning('setAvatarTempTee avId=%s not equal to self.currentGolfer=%s' %(avId, self.currentGolfer))
            return
        if self.state != 'WatchAim':
            return
        if avId != localAvatar.doId:
            self.ballFollow.setH(heading)

    def stickToonToBall(self, avId):
        """Place the toon near the ball."""
        assert self.notify.debugStateCall(self)
        av = base.cr.doId2do.get(avId)
        if av:
            av.reparentTo(self.ballFollowToonSpot)            
            av.setPos(0,0,0)
            av.setH(0)

    def putAwayToon(self, avId):
        """Place the toon in a spot that can't be seen."""
        assert self.notify.debugStateCall(self)        
        av = base.cr.doId2do.get(avId)
        if av:
            av.reparentTo(render)            
            av.setPos(0,0,-1000)
            av.setH(0)  

    def putAwayAllToons(self):
        for avId in self.avIdList:
            self.putAwayToon(avId)
                
    def takeOutToon(self, avId):
        self.stickToonToBall(avId)
        self.fixCurrentGolferFeet()
        self.attachClub(avId)
        
    def showOnlyCurGolfer(self):
        """Hide everyone else and just show the current golfer."""
        assert self.notify.debugStateCall(self)
        self.notify.debug('curGolfer = %s' % self.currentGolfer)
        self.stickToonToBall(self.currentGolfer)
        self.fixCurrentGolferFeet()
        self.attachClub(self.currentGolfer)
        for avId in self.avIdList:
            if avId != self.currentGolfer:
                self.putAwayToon(avId)

    def tabKeyPressed(self):
        """Change the camera angle when the tab key has been pressed."""
        doInterval = True
        self.notify.debug('tab key pressed')
        if not hasattr(self,'ballFollow'):
            return
        if self.flyOverInterval and self.flyOverInterval.isPlaying():
            return
        if self.camInterval and self.camInterval.isPlaying():
            self.camInterval.pause()
        if base.camera.getParent() == self.ballFollow:
            if doInterval:
                curHpr = camera.getHpr(render)
                angle = PythonUtil.closestDestAngle2(curHpr[0], 0)
                self.camInterval = Sequence(
                    Func(base.camera.wrtReparentTo,render),
                    LerpPosHprInterval(base.camera, 2, self.camTopViewPos, self.camTopViewHpr)
                    )
                self.camInterval.start()
            else:
                base.camera.reparentTo(render)
                base.camera.setPos(self.camTopViewPos)
                base.camera.setHpr(self.camTopViewHpr)
            
        else:
            if doInterval:
                curHpr = camera.getHpr(self.ballFollow)
                angle = PythonUtil.closestDestAngle2(curHpr[0], 0)
                self.camInterval = Sequence(
                    Func(base.camera.wrtReparentTo, self.ballFollow),
                    LerpPosHprInterval(base.camera, 2, self.camPosBallFollow, \
                                       self.camHprBallFollow)
                    )
                self.camInterval.start()
            else:
                base.camera.reparentTo(self.ballFollow)
                base.camera.setPos(self.camPosBallFollow)
                base.camera.setHpr(self.camHprBallFollow)                
            
    def doFlyOverMovie(self, avId):
        """Play the flyOver camera movie. Returns False on any errors"""

        title = GolfGlobals.getCourseName(self.golfCourse.courseId) + ' :\n ' + GolfGlobals.getHoleName(self.holeId) + '\n' + TTLocalizer.GolfPar + ' : ' + ( "%s" % (self.holeInfo['par']))
        self.titleLabel = DirectLabel(
            parent = aspect2d,
            relief = None,
            pos = (0, 0, 0.8),
            text_align = TextNode.ACenter,
            text = title,
            text_scale = 0.12,
            text_font = ToontownGlobals.getSignFont(),
            text_fg = (1, 0.8, 0.4, 1)
            )
        self.titleLabel.setBin('opaque', 19)

        self.titleLabel.hide()
        
        self.needToDoFlyOver = False
        bamFile = self.holeInfo['terrainModel']
        fileName = bamFile.split('/')[-1]
        dotIndex = fileName.find('.')
        baseName = fileName[0:dotIndex]
        camModelName = baseName + '_cammodel.bam'
        cameraName = baseName + '_camera.bam'
        path = bamFile[0: bamFile.find(fileName)]
        camModelFullPath = path + camModelName
        cameraAnimFullPath = path + cameraName

        try:
            self.flyOverActor = Actor.Actor(camModelFullPath, {'camera':cameraAnimFullPath})
        except StandardError:
            # this hole doesn't have the flyover animation, just return
            self.notify.debug("Couldn't find flyover %s" % camModelFullPath)
            return False

        # take away the black screen
        base.transitions.noIris()

        self.flyOverActor.reparentTo(render)
        self.flyOverActor.setBlend(frameBlend = True)

        flyOverJoint = self.flyOverActor.find('**/camera1')
        children = flyOverJoint.getChildren()
        numChild = children.getNumPaths()
        for i in xrange(numChild):
            childNodePath = children.getPath(i)
            childNodePath.removeNode()
        self.flyOverJoint = flyOverJoint

        self.flyOverInterval = Sequence(
            Func(base.camera.reparentTo, flyOverJoint),
            Func(base.camera.clearTransform),
            Func(self.titleLabel.show),
            ActorInterval(self.flyOverActor, 'camera'),
            Func(base.camera.reparentTo,self.ballFollow),
            Func(base.camera.setPos,self.camPosBallFollow),
            Func(base.camera.setHpr,self.camHprBallFollow),
            )

        

        if avId == localAvatar.doId:
            self.flyOverInterval.append(Func(self.setCamera2Ball))
            self.flyOverInterval.append(Func(self.safeRequestToState,'ChooseTee'))
        else:
            self.flyOverInterval.append(Func(self.setCamera2Ball))            
            self.flyOverInterval.append(Func(self.safeRequestToState,'WatchTee'))            

        self.flyOverInterval.append(Func(self.titleLabel.hide))
        self.flyOverInterval.append(Func(self.takeOutToon, avId)) 
       
        self.flyOverInterval.start()
        
        return True

    def avExited(self, avId):
        if self.state == 'Playback' and self.currentGolfer == avId:
            # don't hide the ball so that the movie doesn't look weird
            pass
        else:
            self.ballDict[avId]['golfBallGeom'].hide()

    def orientCameraRay(self):
        """Correct the orientation of the ray to test properly."""
        pos =  base.camera.getPos(self.terrainModel)
        self.cameraRayNodePath.setPos(pos)
        self.cameraRayNodePath.lookAt(self.ballFollow)
        renderPos = self.cameraRayNodePath.getPos(render)
        if renderPos != pos:
            self.notify.debug('orientCamerRay this should not happen')
        ballPos = self.ballFollow.getPos(self.terrainModel)
        dirCam = Vec3( ballPos - pos)
        dirCam.normalize()
        self.cameraRay.set( pos, dirCam)
        
        
    def performSwing(self, ball, power, dirX, dirY):
        startTime = globalClock.getRealTime()

        """Handle the client done swinging and is telling us his angle and velocity."""
        #self.timingSimTime = self.storeAction[1]
        #print("Started sim at %s" % (self.timingSimTime))
        #self.setTimeIntoCycle(self.storeAction[1])
        #cycleTime = self.getCycleTime(1)
        
        avId = base.localAvatar.doId

        position = ball.getPosition()
        x = position[0]
        y = position[1]           
        z = position[2]

        if avId not in self.golfCourse.drivingToons:
            x = position[0]
            y = position[1]
            z = position[2]

        
        self.swingTime = cycleTime
        lift = 0
        ball = self.ball
        # a professional golfer hits a real golf ball with 157 pounds force
        forceMove = 2500 # amount of pounds force to give at 100%

        if power > 50:
            #lift = forceMove * (power - 30.0) * 0.02
            lift = 0 # we deliberately have 0 lift to make it easier
        ball.enable()
        ball.setPosition(x,y,z)
        ball.setLinearVel(0.0,0.0,0.0)
        ball.setAngularVel(0.0,0.0,0.0)
        ball.addForce(Vec3(dirX * forceMove * power /100.0,
                        dirY * forceMove * power / 100.0,
                        lift))
        self.initRecord()
        safety = 0
        self.llv = None
        self.record(ball)
        while (ball.isEnabled() and len(self.recording) < 2000):
            self.preStep()
            self.simulate()
            self.postStep()
            self.record(ball)
            safety += 1
        self.record(ball)
        midTime = globalClock.getRealTime()
        self.processRecording()
        self.processAVRecording()
        self.notify.debug("Recording End time %s cycle %s len %s avLen %s" % (self.timingSimTime, self.getSimCycleTime(), len(self.recording), len(self.aVRecording)))
        self.request("WaitPlayback")
        length = len(self.recording) - 1
        x = self.recording[length][1]
        y = self.recording[length][2]
        z = self.recording[length][3]
        self.ballPos[avId] = Vec3(x,y,z)
        endTime = globalClock.getRealTime()
        diffTime = endTime - startTime
        fpsTime = self.frame / diffTime  
        self.notify.debug ("Time Start %s Mid %s End %s Diff %s Fps %s frames %s" % (startTime, midTime, endTime, diffTime, fpsTime, self.frame))
        self.ballMovie2Client(cycleTime, avId, self.recording, self.aVRecording, self.ballInHoleFrame, self.ballTouchedHoleFrame, self.ballFirstTouchedHoleFrame)


    def handleBallHitNonGrass(self, c0, c1):
        """Handle the ball hitting something non-grass."""
        # we just play a sound depending on what we hit
        if not self.inPlayBack:
            # it's possible for the ball to come to rest against the curb
            return
        golfBallPos = self.curGolfBall().getPosition()
        if self.lastBumpSfxPos == golfBallPos:
            return
        if GolfGlobals.HARD_COLLIDE_ID in [c0, c1]:                                              
            if not (self.bumpHardSfx.status() == self.bumpHardSfx.PLAYING):
                distance = (golfBallPos - self.lastBumpSfxPos).length()
                if distance > 2.0:
                    # don't play bump hard sfx too close to each other
                    base.playSfx(self.bumpHardSfx)
                    self.lastBumpSfxPos = golfBallPos
        elif GolfGlobals.MOVER_COLLIDE_ID in [c0, c1]:
            if not (self.bumpMoverSfx.status() == self.bumpMoverSfx.PLAYING):
                base.playSfx(self.bumpMoverSfx)
                self.lastBumpSfxPos = golfBallPos
        elif GolfGlobals.WINDMILL_BASE_COLLIDE_ID in [c0, c1]:
            if not (self.bumpWindmillSfx.status() == self.bumpWindmillSfx.PLAYING):
                base.playSfx(self.bumpWindmillSfx)
                self.lastBumpSfxPos = golfBallPos

    def safeRequestToState(self, newState):
        """Request a new state if it's a valid transition."""
        doingRequest = False
        if self.state in self.defaultTransitions:
            if newState in self.defaultTransitions[self.state]:
                self.request(newState)
                doingRequest = True
        if not doingRequest:
            self.notify.warning('ignoring transition from %s to %s' % (self.state, newState))
    def doMagicWordHeading(self, heading):
        """We got a magic word to set our heading."""
        if self.state == "Aim":
            self.aimMomentum = 0.0            
            self.ballFollow.setH(float(heading))

    def _handleClientCleanup(self):
        """Handle the user unexpectedly closing the toontown window."""
        assert self.notify.debugStateCall(self)
        self.removePlayBackDelayDelete()
        self.ignore('clientCleanup')

