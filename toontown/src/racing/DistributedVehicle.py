
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.distributed import DistributedSmoothNode
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import clampScalar
from otp.otpbase import OTPGlobals
from otp.avatar import ShadowCaster
from toontown.racing import Kart
from toontown.racing.KartDNA import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.effects.Drift import Drift
from toontown.effects.Sparks import Sparks
from direct.interval.ProjectileInterval import *
from toontown.battle.BattleProps import *
import random
from direct.showbase.PythonUtil import randFloat
from direct.task.Task import Task
import math

if __debug__:
    import pdb


iceTurnFactor = 0.25
iceAccelFactor = 0.4

class DistributedVehicle(DistributedSmoothNode.DistributedSmoothNode,
                         Kart.Kart, FSM.FSM): 

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedVehicle")
    #notify.setDebug(True)
    
    cheatFactor = 1.0
    proRacer = 0

    physicsCalculationsPerSecond = 60
    maxPhysicsDt = 1.0
    physicsDt = 1.0 / float(physicsCalculationsPerSecond)
    maxPhysicsFrames = maxPhysicsDt * physicsCalculationsPerSecond
    
    maxSpeed = 200 * cheatFactor #jml

    # higher divisors = worse turn rate
    turnRatio = 1.0 / 0.025 * math.sqrt(cheatFactor) #jml

    accelerationMult = 35
    accelerationBase = 20
    
    if proRacer:
        accelerationMult = 35
        accelerationBase = 30
        

    surfaceModifiers = {
        'asphalt' : {'shake' : 0.1,
                     'driftMin' : 65,
                     'windResistance' : 0.2,
                     'particleColor' : Vec4(0.7,0.7,0.7,1.0),
                     },
        'gravel' :  {'shake' : 0.2,
                     'driftMin' : 65,
                     'windResistance' : 0.2,
                     'particleColor' : Vec4(0.53,0.53,0.53,1.0),
                     },
         'dirt'   : {'shake' : 0.4,
                     'driftMin' : 35,
                     'windResistance' : 0.3,
                     'particleColor' : Vec4(1.0,1.0,1.0,1.0),
                     },
         'grass'  : {'shake' : 0.8,
                     'driftMin' : 15,
                     'windResistance' : 0.4,
                     'particleColor' : Vec4(0.8,0.42,0.8,1.0),
                     },
        'ice'        : {'shake' : 0.0,
                     'driftMin' : 0, #'driftMin does not do anything' ~should be a comment not data! JML
                     'windResistance' : 0.01,
                     'particleColor' : Vec4(1.0,1.0,1.0,1.0),
                     },
        ''        : {'shake' : 0,
                     'driftMin' : 1,
                     'windResistance' : 0.2,
                     'particleColor' : Vec4(1.0,1.0,1.0,1.0),
                     },
         }
    
    SFX_BaseDir = "phase_6/audio/sfx/"
    SFX_WallHits = [ SFX_BaseDir + "KART_Hitting_Wood_Fence.mp3",
                     SFX_BaseDir + "KART_Hitting_Wood_Fence_1.mp3",
                     SFX_BaseDir + "KART_Hitting_Metal_Fence.mp3",
                     SFX_BaseDir + "KART_Hitting_Wall.mp3",
                     ]
    #SFX_WallLoop_Wood =    SFX_BaseDir + "KART_Rubbing_Against_Wood_Fence.wav"
    SFX_SkidLoop_Grass =   SFX_BaseDir + "KART_Skidding_On_Grass.wav"
    SFX_SkidLoop_Asphalt = SFX_BaseDir + "KART_Skidding_On_Asphalt.wav"
    SFX_TurboStart =       SFX_BaseDir + "KART_turboStart.mp3"
    SFX_TurboLoop =        SFX_BaseDir + "KART_turboLoop.wav"
    
    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedVehicle')
        Kart.Kart.__init__(self)
        if base.config.GetBool('want-racer', 0) == 1:
            DistributedVehicle.proRacer = 1
            DistributedVehicle.accelerationMult = 35
            DistributedVehicle.accelerationBase = 30
            
            
        
        self.speedometer = None
        self.speedGauge = None
        self.leanAmount = 0
        self.leftHeld = 0
        self.stopped=False
        self.rightHeld = 0
        self.canRace=False
        self.groundType = "gravel"
        self.offGround=0
        self.turbo = False
        self.ownerId=0
        self.cameraTrack = None
        self.curSpeed = 0
        self.acceleration = 0

        self.imHitMult=1
        self.skidding = False
        self.hittingWall = 0
        base.kart = self
        self.wipeOut=None
        self.gagMovie = None
        self.spinAnim = None
        self.wrongWay = False
        self.wallCollideTrack = None
        self.wheelMaxTurn = 1.0
        self.wheelMinTurn = 0.15
        self.speedMaxTurn = 90
        self.speedMinTurn = 300
        self.wheelTurnTime = 0.6 #time to reach max turn
        self.wheelReturnTime = 0.3 #time to recenter wheel if controls are released
        self.wheelFightTime = 0.2 #time to recenter wheel if controls in different direction from wheel
        self.wheelPosition = 0.0 # -1 is left; 1 is right
        self.outPutCounter = 0
        self.proCameraHeading = 0
        self.proCameraDummyNode = None
        self.cameraArmNode = None
        self.armSwingSpeedPerp = 0.2 #time in seconds to adjust camera
        self.armSwingSpeedPara = 0.7
        self.cameraTightener = 3.0 # range 1.1 to infinity
        self.cameraArmBase = 0
        self.cameraArmExtend = 20
        
        self.pieCount = 0
        self.numPieChunks = 6
        self.pieSlideSpeed = []
        
        for piece in range(self.numPieChunks):
            self.pieSlideSpeed.append(randFloat(0.0,0.2))

        self.wantSmoke = ConfigVariableBool('want-kart-smoke',1).getValue()
        self.wantSparks = ConfigVariableBool('want-kart-sparks',1).getValue()
        
        self.__loadTextures()
            
    def __loadTextures(self):
            self.pieSplatter = loader.loadModel('phase_6/models/karting/pie_splat_1.bam')
        
    def announceGenerate(self):
        DistributedSmoothNode.DistributedSmoothNode.announceGenerate(self)
        self.generateKart()
        self.name = self.uniqueName('vehicle')
        self.posHprBroadcastName = self.uniqueName('vehicleBroadcast')

        # use the highest LOD during racing
        self.LODnode.forceSwitch(self.LODnode.getHighestSwitch())
        
        #create a node to parent the camera to
        self.cameraNode = NodePath('cameraNode')
        self.cameraNode.reparentTo(self)
        
        if self.proRacer:
            
            self.cameraArmNode = render.attachNewNode("cameraArm")
            self.cameraArmNode.reparentTo(self)
            #self.cameraNode.reparentTo(self)
            self.cameraNode.reparentTo(self.cameraArmNode)
        
        self.proCameraDummyNode = render.attachNewNode("proCameraDummy")
        self.proCameraDummyNode.reparentTo(render)

        self.localVehicle = (self.ownerId == localAvatar.doId)
        if self.localVehicle:
            self.setupPhysics()
            self.setupParticles()
            self.__enableCollisions()


        self.forward=NodePath("forward")
        self.forward.setPos(0,1,0)

        ##########################################################
        # Load sounds
        self.wallHitsSfx = []
        for wallHit in self.SFX_WallHits:
            self.wallHitsSfx.append( base.loadSfx(wallHit) )
        #self.wallLoopWoodSfx = base.loadSfx(self.SFX_WallLoop_Wood)
        #self.wallLoopWoodSfx.setLoop()
        self.skidLoopAsphaltSfx = base.loadSfx(self.SFX_SkidLoop_Asphalt)
        self.skidLoopAsphaltSfx.setLoop()
        self.skidLoopGrassSfx = base.loadSfx(self.SFX_SkidLoop_Grass)
        self.skidLoopGrassSfx.setLoop()
        self.turboStartSfx = base.loadSfx(self.SFX_TurboStart)
        self.turboLoopSfx = base.loadSfx(self.SFX_TurboLoop)
        self.turboLoopSfx.setLoop()

        self.forward.reparentTo(self.geom[0])
        self.anvil=globalPropPool.getProp('anvil')
        self.anvil.setScale(5)
        self.anvil.reparentTo(hidden)
        self.anvil.setColor(.1,.1,.1,1)
        self.anvil.setTransparency(1)
        ###########################################################
        # Add the kart to the scene
        self.reparentTo(render)       
        
    def setupPhysics(self):
        self.__setupCollisions()
        ###########################################################
        # Set up all the physics forces
        self.physicsMgr = PhysicsManager()
        self.physicsEpoch = globalClock.getFrameTime()
        self.lastPhysicsFrame = 0
        integrator = LinearEulerIntegrator()
        self.physicsMgr.attachLinearIntegrator(integrator)
        
        # add wind Resistance Force
        fn = ForceNode('windResistance')
        fnp = NodePath(fn)
        fnp.reparentTo(render)
        windResistance = LinearFrictionForce(0.2)
        fn.addForce(windResistance)
        self.physicsMgr.addLinearForce(windResistance)
        self.windResistance = windResistance
        
        #create an engine force
        fn = ForceNode("engine")
        fnp = NodePath(fn)
        fnp.reparentTo(self)
        engine = LinearVectorForce(0, 0, 0)
        fn.addForce(engine)
        self.physicsMgr.addLinearForce(engine)
        self.engine = engine

    def disable(self):
        """
        This method is called when the DistributedSmoothNode is removed from
        active duty and stored in a cache.
        """
        assert self.notify.debug(" Disabling...")
        self.finishMovies()
        self.request('Off')
        self.stopSkid()
        self.stopSmooth()
        if self.localVehicle:
            self.__disableCollisions()
            self.__undoCollisions()
            self.physicsMgr.clearLinearForces()
        self.detachNode()
        #base.cr.parentMgr.unregisterParent(ToontownGlobals.SPDonaldsVehicle)
        #self.ignore('enterdonalds_vehicle_floor')
        #self.ignore('exitdonalds_vehicle_floor')
        DistributedSmoothNode.DistributedSmoothNode.disable(self)
        #self.pieWindShield.hide()
        taskMgr.remove('slidePies')
        #self.ewTrack.finish()
        #self.weTrack.finish()

    def delete(self):
        """
        This method is called when the DistributedSmoothNode is permanently
        removed from the world and deleted from the cache.
        """
        assert self.notify.debug(" Deleting...")
        #self.eastWestMopath.reset()
        #self.westEastMopath.reset()
        #del self.eastWestMopath
        #del self.westEastMopath
        #del self.ewTrack
        #del self.weTrack
        #del self.fsm
        self.stopSmooth()
        Kart.Kart.delete(self)
        DistributedSmoothNode.DistributedSmoothNode.delete(self)
        #self.__deleteControlInterface()
        if self.localVehicle:
            self.ignoreAll()
            if hasattr(self, 'piePieces'):
                for piece in self.piePieces:
                    del piece
            
    def getVelocity(self):
        return self.actorNode.getPhysicsObject().getVelocity()

    def __updateWallCollision(self, entry = None):
        vol = self.curSpeed / 160
        for wallHit in self.wallHitsSfx:
            wallHit.setVolume(vol)
        #self.wallLoopWoodSfx.setPlayRate(vol)
        
    def __wallCollisionStart(self, entry):

        
        #print("Now Hitting Wall")
        self.entry = entry
        self.__wallCollisionStop()
        self.hittingWall = 1
        hitToPlay = random.randrange(0, len(self.wallHitsSfx))
            
        self.wallCollideTrack = Parallel(
            Func(self.wallHitsSfx[hitToPlay].play),
            #Sequence(Wait(0.2),
            #         Func(self.wallLoopWoodSfx.play)
            #         )
            )
            
        self.__updateWallCollision()
        self.wallCollideTrack.start()

        curSpeed = self.actorNode.getPhysicsObject().getVelocity().length()
        if (self.wantSparks and curSpeed > 10):
            if(entry.getSurfaceNormal(self)[0] < 0):
                self.fireSparkParticles('right')
            else:
                self.fireSparkParticles('left')
                
    def __wallCollisionStop(self, entry = None):
        #print("No longer hittingWall")
        self.hittingWall = 0

        if self.wallCollideTrack:
            self.wallCollideTrack.pause()
            #self.wallLoopWoodSfx.stop()
    
    def __setupCollisions(self):
        # We will use a separate collision traverser for walls to 
        # get around the ordering issue (we must check walls before
        # floors)
        self.cWallTrav = CollisionTraverser("KartWall")
        self.cWallTrav.setRespectPrevTransform(True)
        
        ###########################################################
        # A CollisionNode to keep me out of walls, and to
        # keep others from bumping into me.  We use PieBitmask instead
        # of WallBitmask, to protect against objects (like goons)
        # self-colliding.
        self.collisionNode = CollisionNode(self.uniqueName('vehicle'))
        self.collisionNode.setFromCollideMask(OTPGlobals.WallBitmask)
        self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask)
        cs = CollisionSphere(0, 0, 4, 4)
        self.collisionNode.addSolid(cs)
        self.collisionNodePath = NodePath(self.collisionNode)

        #handler = CollisionHandlerPusher()
        #self.wallHandler = CollisionHandlerPusher()
        self.wallHandler = PhysicsCollisionHandler()
        self.wallHandler.setStaticFrictionCoef(0.0)
        self.wallHandler.setDynamicFrictionCoef(0.1)
        self.wallHandler.addCollider(self.collisionNodePath, self)
        self.wallHandler.setInPattern("enterWallCollision")
        self.wallHandler.setOutPattern("exitWallCollision")
        self.cWallTrav.addCollider(self.collisionNodePath, self.wallHandler)
        self.accept("enterWallCollision", self.__wallCollisionStart)
        self.accept("exitWallCollision", self.__wallCollisionStop)

        ###########################################################
        ### Set up floor collisions ###

        # This is a ray cast down to detect floor polygons
        cRay = CollisionRay(0.0, 0.0, 40000.0, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode(self.uniqueName('vehicle-FloorRay'))
        cRayNode.addSolid(cRay)
        cRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.cRayNodePath = self.attachNewNode(cRayNode)
        
        # set up floor collision mechanism
        self.lifter = CollisionHandlerGravity()
        self.lifter.setGravity(32.174 * 3.0)
        self.lifter.addInPattern("floorCollision")
        self.lifter.addAgainPattern("floorCollision")
        self.lifter.setOffset(OTPGlobals.FloorOffset)
        # This is how high the vehicle will reach up to another floor
        # polygon:
        self.lifter.setReach(40.0)
        self.lifter.addCollider(self.cRayNodePath, self)

        # hook into the base collision traverser
        base.cTrav.addCollider(self.cRayNodePath, self.lifter)
        self.accept("floorCollision", self.__groundCollision)

        self.accept("imIn-banana",self.hitBanana)
        #self.accept("imIn-pie",self.hitPie)

        # Be sure to turn off the local avatar's collisions--we don't
        # need them now, and they'll get in the way.
        base.localAvatar.collisionsOff()

    def __undoCollisions(self):
        base.cTrav.removeCollider(self.cRayNodePath)

        # Restore the local avatar's collisions.  This really should
        # be done by the place's FSM, but we don't have a place ?!
        base.localAvatar.collisionsOn()

    def __groundCollision(self, entry):
        ground = entry.getIntoNodePath()
        #if we don't have a surface than just use the old one.
        if ground.getNetTag("surface") == "":  
            return
        self.groundType = ground.getNetTag("surface")
        #self.updateSkid()
        #print self.groundType

    def __enableCollisions(self):
        self.cQueue = []
        self.cRays = NodePath('stickVehicleToFloor')
        self.cRays.reparentTo(self.geom[0])
        for wheelNode in self.wheelBases:
            rayNode = CollisionNode(wheelNode.getName())
            x = wheelNode.getX()
            y = wheelNode.getY()
            # This is a ray cast down to detect floor polygons
            ray = CollisionRay(x, y, 40000.0, 0.0, 0.0, -1.0)
            rayNode.addSolid(ray)
            rayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
            rayNode.setIntoCollideMask(BitMask32.allOff())
            rayNodePath = self.cRays.attachNewNode(rayNode)

            # set up floor collision mechanism
            cQueue = CollisionHandlerQueue()
            self.cWallTrav.addCollider(rayNodePath, cQueue)
            self.cQueue.append(cQueue)
        
        self.collisionNodePath.reparentTo(self)

    #Sets up the lap collisions for this vehicle
    def setupLapCollisions(self):
        #TODO: make this a global
        self.lapBit=BitMask32(0x8000)
        self.lapHandler=CollisionHandlerEvent()
        self.lapHandler.addInPattern('imIn-%in')
        self.cSphere=CollisionSphere(0,0,0,3)
        self.lapNode=CollisionNode("lapChecker")
        self.lapNode.addSolid(self.cSphere)
        self.lapNode.setIntoCollideMask(BitMask32.allOff())
        self.lapNode.setFromCollideMask(self.lapBit)
        
        self.lapNodePath=NodePath(self.lapNode)
        self.lapNodePath.reparentTo(self)

        #self.lapHandler.addCollider(self.lapNode,self.lapNodePath)
        self.cWallTrav.addCollider(self.lapNodePath,self.lapHandler)

    def __disableCollisions(self):
        # stop listening for toons.
        self.ignore("imIn-startLine")
        self.ignore("imIn-quarterLine")        
        self.ignore("imIn-midLine")

    def __handleCollisionSphereEnter(self, collEntry=None):
        assert self.notify.debug("Entering collision sphere...")
        self.d_requestControl()

    def setupParticles(self):
        if (self.wantSmoke):
            self.setupDriftParticles()
        if (self.wantSparks):
            self.setupSparkParticles()
    def updateParticles(self,leanAmount):
        if (self.wantSmoke):
            self.updateDriftParticles(leanAmount)
    def cleanupParticles(self):
        if (self.wantSmoke):
            self.cleanupDriftParticles()
        if (self.wantSparks):
            self.cleanupSparkParticles()
        
    def setupDriftParticles(self):
        smokeMount = self.geom[0].attachNewNode('Smoke Effect')
        backLeft = smokeMount.attachNewNode('Back Left Smokemount')
        backLeft.setPos(self.geom[0].find('**/'+self.wheelData[self.LRWHEEL]['node']).getPos()+Vec3(-0.25,-1.0,-0.5))
        backRight = smokeMount.attachNewNode('Back Right Smokemount')
        backRight.setPos(self.geom[0].find('**/'+self.wheelData[self.RRWHEEL]['node']).getPos()+Vec3(0.25,-1.0,-0.5))

        driftEffects = (Drift(backLeft,backLeft),Drift(backRight,backRight))
        for x in driftEffects:
            x.start()
        self.drifts = driftEffects

        self.driftSeq = Sequence(
            Func(backLeft.show),
            Func(backRight.show),
            Wait(1000000),
            Func(self.drifts[0].effect.getParticlesNamed('particles-1').getRenderer().setColor,Vec4(1.0,1.0,1.0,1.0)),
            Func(self.drifts[1].effect.getParticlesNamed('particles-1').getRenderer().setColor,Vec4(1.0,1.0,1.0,1.0)),
            Func(backLeft.hide),
            Func(backRight.hide),
            )

        self.driftSeqStarted = False
        self.driftParticleForces = [ x.effect.getParticlesNamed('particles-1').getLinearForce(0) for x in self.drifts ]
        self.smokeMount = smokeMount
        backLeft.hide();
        backRight.hide()

    def updateDriftParticles(self,leanAmount):
        for x in self.driftParticleForces:
            x.setAmplitude(leanAmount*30)
            
        if self.skidding and not self.driftSeqStarted:
            self.driftSeqStarted = True
            self.driftSeq.start()
        elif not self.skidding and self.driftSeqStarted:
            self.driftSeqStarted = False
            self.driftSeq.finish()
        
    def cleanupDriftParticles(self):
        self.driftSeq.finish()
        for x in self.drifts:
            x.destroy()
        self.smokeMount.remove()
        
        del self.driftSeq
        del self.driftParticleForces
        del self.drifts
        del self.smokeMount

    def setupSparkParticles(self):
        bodyType = self.kartDNA[ KartDNA.bodyType ]
        endPts = KartDict[bodyType][7]
        
        self.sparkMount = self.geom[0].attachNewNode('Spark Effect')
        left = self.sparkMount.attachNewNode('Left Sparkmount')
        left.setPos(((self.geom[0].find('**/'+self.wheelData[self.LFWHEEL]['node']).getPos() + \
                      self.geom[0].find('**/'+self.wheelData[self.LRWHEEL]['node']).getPos()) / 2.0)+Vec3(0.0,-1.0,1.0))
        left.setScale(0.5)
        right = self.sparkMount.attachNewNode('Right Sparkmount')
        right.setPos(((self.geom[0].find('**/'+self.wheelData[self.RFWHEEL]['node']).getPos() + \
                       self.geom[0].find('**/'+self.wheelData[self.RRWHEEL]['node']).getPos()) / 2.0)+Vec3(0.0,-1.0,1.0))
        right.setScale(0.5);
        self.sparks = (Sparks(right,self.sparkMount),Sparks(left,self.sparkMount))

        self.sparks[0].effect.getParticlesNamed('particles-1').getEmitter().setEndpoint1(endPts[0])
        self.sparks[0].effect.getParticlesNamed('particles-1').getEmitter().setEndpoint2(endPts[1])
        self.sparks[0].effect.getParticlesNamed('particles-1').getLinearForce(0).setAmplitude(-50)
        
        self.sparks[1].effect.getParticlesNamed('particles-1').getEmitter().setEndpoint1(Point3(-endPts[0][0],endPts[0][1],endPts[0][2]))
        self.sparks[1].effect.getParticlesNamed('particles-1').getEmitter().setEndpoint2(Point3(-endPts[1][0],endPts[1][1],endPts[1][2]))
        self.sparks[1].effect.getParticlesNamed('particles-1').getLinearForce(0).setAmplitude(50)

    def fireSparkParticles(self,side):
        spark = self.sparks[{'right':0,'left':1}[side]]

        if not spark.effect.isEnabled():
            spark.effect.getParticlesNamed('particles-1').setBirthRate(0.0200)
            spark.start()
            taskMgr.doMethodLater(0.25,self.stopSparkParticles,'sparkTimer-'+side,extraArgs = [side])
            
    def stopSparkParticles(self,side = None):
        sides = {0:'right',1:'left'}
        if side == None:
            for x in sides.keys():
                self.sparks[x].effect.getParticlesNamed('particles-1').setBirthRate(1000)
                taskMgr.doMethodLater(0.75,self.sparks[x].stop,'stopSparks-'+sides[x],extraArgs = [])
        else:
            spark = self.sparks[{'right':0,'left':1}[side]]
            spark.effect.getParticlesNamed('particles-1').setBirthRate(1000)
            taskMgr.doMethodLater(0.75,spark.stop,'stopSparks-'+side,extraArgs = [])
            
    def cleanupSparkParticles(self):
        taskMgr.remove('sparkTimer-left')
        taskMgr.remove('sparkTimer-right')
        taskMgr.remove('stopSparks-left')
        taskMgr.remove('stopSparks-right')
        for x in self.sparks:
            x.destroy()
        self.sparkMount.remove()

        del self.sparks
        del self.sparkMount
    
    ### Messages to/from the AI ###
    
    def setState(self, state, avId):
        self.notify.debug("SetState received: %s avId: %s" % (state, avId))
        if state == 'C':
            self.demand('Controlled', avId)
        elif state == 'P':
            self.demand('Parked')
        else:
            self.notify.error("Invalid state from AI: %s" % (state))

    def d_requestControl(self):
        self.sendUpdate('requestControl')

    def d_requestParked(self):
        self.sendUpdate('requestParked')

    ##### Off state #####

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ##### Parked state #####

    def enterParked(self):
        pass

    def exitParked(self):
        pass

    #### Controlled state #####
    def enterControlled(self, avId):
        self.avId = avId
        self.toon = base.cr.doId2do.get(avId,None)
        if self.toon:
            self.toon.stopSmooth()
            self.toon.stopPosHprBroadcast()
            for feet in self.toon.getPieces(('legs', 'feet')):
                    feet.hide()
            self.toon.reparentTo(self.toonSeat)
            self.toon.dropShadow.hide()
            self.notify.debug('setting pos of toon%s' % self.toon.doId)
            self.toon.setPosHpr(0, 0, 0, 0, 0, 0)
            self.toon.loop('sit')
            if self.toon.doId == localAvatar.doId:
                self.notify.debug('calling send currentPosition')
                self.toon.sendCurrentPosition()
            self.doHeadScale(self.toon, 1.75)
            self.toon.setShear(0, 0, 0)

        # make all chat appear in the margins
        NametagGlobals.setOnscreenChatForced(1)
        
        if self.localVehicle:
            # The local toon is beginning to control the vehicle.
            camera.reparentTo(self.cameraNode)
            camera.setPosHpr(0, -33, 16, 0, -10, 0)

            self.physicsMgr.attachPhysicalNode(self.node())
            self.__enableControlInterface()
            self.__createPieWindshield()
            self.startPosHprBroadcast()

            self.engineSfxTrack = self.generateEngineStartTrack()
            self.engineSfxTrack.start()
        else:
            self.startSmooth()
            taskName = "updateNonlocalVehicle-%s" % avId
            #taskMgr.remove('updateNonlocalVehicle')
            self.updateNonLocalTask = taskMgr.add(
                self.__updateNonlocalVehicle, taskName)

    def exitControlled(self):
        #import pdb;pdb.set_trace()

        if self.localVehicle:
            # The local toon is no longer in control of the vehicle

            self.stopPosHprBroadcast()
            self.__disableControlInterface()
            self.physicsMgr.removePhysicalNode(self.node())

            self.cleanupParticles()

            camera.reparentTo(localAvatar)
            camera.setPos(localAvatar.cameraPositions[0][0])
            camera.setHpr(0, 0, 0)
            self.engineSfxTrack.finish()
            self.engineSfxTrack = self.generateEngineStopTrack()

        else:
            self.stopSmooth()
            taskMgr.remove(self.updateNonLocalTask)



        if self.toon and not self.toon.isDisabled() and not self.toon.isEmpty():
            self.toon.dropShadow.show()
            self.doHeadScale(self.toon,None)
            self.toon.setPosHpr(self.geom[0], 0, 8, 0, 0, 0, 0)
            for feet in self.toon.getPieces(('legs', 'feet')):
                    feet.show()
            self.toon.reparentTo(render)
            self.toon.loop('neutral')
            self.toon.startSmooth()

        # stop making all chat appear in the margins
        NametagGlobals.setOnscreenChatForced(0)


    def doHeadScale(self, model, scale):
        if scale == None:
            scale = ToontownGlobals.toonHeadScales[model.style.getAnimal()]
            base.localAvatar.clearCheesyEffect()

        for hi in range(model.headParts.getNumPaths()):
            head = model.headParts[hi]
            head.setScale(scale)
            
    def __createPieWindshield(self):
        
        self.piePieces = []
        for piece in range(self.numPieChunks):
            self.piePieces.append(DirectLabel(
            relief = None,
            pos = (0.0, 0.0, 0.0),
            image = self.pieSplatter,
            image_scale = (0.5,0.5,0.5),
            text = " ",
            text_scale = 0.18,
            text_fg = (1,0,1,1),
            text_pos = (-0.00, 0.00, 0),
            text_font = ToontownGlobals.getSignFont(),
            textMayChange = 1,
            ))
            self.piePieces[piece].hide()
            
        #import pdb; pdb.set_trace()
        
    def showPieces(self):
        xRange = 0.3
        for piece in self.piePieces:
            piece.setPos(randFloat(-xRange,xRange),randFloat(-0.1,3.5), randFloat(-0.9,0.9))
            piece.setScale(randFloat(1.1,2.0),1,randFloat(1.1,2.0))
            piece.show()
            xRange += (2.5 / self.numPieChunks)
        for piece in range(self.numPieChunks):
            self.pieSlideSpeed[piece] = (randFloat(0.0,0.2))
        
    def splatPie(self):
        self.showPieces()
        if self.pieCount == 0:
            self.pieCount = 15
            taskMgr.doMethodLater(1, self.__countPies,' ',extraArgs = [])
            taskMgr.add(self.__slidePies, 'slidePies',priority=25)
        else:
            self.pieCount = 15

            
    def __countPies(self):
        if self.pieCount > 0:
            #self.pieWindShield['text'] = ("PIE FOOL FACTOR:%s" % (self.pieCount))
            #self.pieWindShield.show()
            #self.showPieces()
            taskMgr.doMethodLater(1, self.__countPies,' ',extraArgs = [])
            self.pieCount -= 1
        else:
            #self.pieWindShield.hide()
            for piece in self.piePieces:
                piece.hide()
            
    def __slidePies(self, optional = None):
        dt = globalClock.getDt()
        
        for piece in range(self.numPieChunks):
            self.pieSlideSpeed[piece] += randFloat(0.0,0.25 * dt)
            pieSpeed = self.pieSlideSpeed[piece] * dt
            self.piePieces[piece].setPos(self.piePieces[piece].getPos()[0],
                                        self.piePieces[piece].getPos()[1] - pieSpeed,
                                        self.piePieces[piece].getPos()[2] - pieSpeed)
        if self.pieCount == 0:
            return Task.done
        else:        
            return Task.cont
        

    def __enableControlInterface(self):
        if(self.canRace):
            self.enableControls()
        taskMgr.remove('watchVehicleControls')
        taskMgr.add(self.__watchControls, 'watchVehicleControls',priority=25)

        # In case they don't figure it out, hit them over the head
        # with it after a few seconds.
        #taskMgr.doMethodLater(5, self.__displayCraneAdvice,
        #                      self.craneAdviceName)
        #taskMgr.doMethodLater(10, self.__displayMagnetAdvice,
        #                      self.magnetAdviceName)

        # karting gui items here for now - might need to be abstracted if they become cumbersome
        #

        # speedo
        if not self.speedometer:
            cm = CardMaker('speed')
            cm.setFrame(-0.5,0.5,-0.5,0.5)

            self.speedometerImages = aspect2d.attachNewNode('SpeedometerImages')
            self.speedometerImages.setTransparency(True)
            self.speedometerImages.setPos(1.24, 0.0, -0.98)
            self.speedometerImages.setScale(0.75)

            m = loader.loadModel('phase_6/models/karting/speedometer')

            if( self.getBodyColor() == InvalidEntry ):
                bodyColor = getDefaultColor()
            else:
                bodyColor = getAccessory( self.getBodyColor() )
            if( self.getAccessoryColor() == InvalidEntry ):
                accColor = getDefaultColor()
            else:
                accColor = getAccessory( self.getAccessoryColor() )

#            bodyColor = Vec4(0,1,1,1)
#            accColor = Vec4(1,1,0,1)

            self.speedometerImages.attachNewNode(m.find('**/*gauge').node()).setColorScale(1,1,1,1)
            self.speedGauge = self.speedometerImages.attachNewNode(m.find('**/*spin').node())
            self.speedGauge.setColor(1,1,1,1)
                       
            c = (Vec4(1,1,1,1)+accColor)/2.0
            c.setW(1.0)
            self.speedometerImages.attachNewNode(m.find('**/*face').node()).setColorScale(c)
            

            c = (Vec4(2,2,2,2)-accColor)/2.0
            c = (bodyColor + Vec4(1,1,1,1))/2.0
            c.setW(1.0)
            self.speedometerImages.attachNewNode(m.find('**/*tics').node()).setColorScale(c)

            c = (bodyColor + Vec4(1,1,1,1))/2.0
            c.setW(1.0)
            self.speedometerImages.attachNewNode(m.find('**/*ring').node()).setColorScale(c)

##             cm.setName('Face')
##             c = self.speedometerImages.attachNewNode(cm.generate())
##             c.setTexture(loader.loadTexture('src/maps/speedometer_face.tif'),1)
##             c.setColor(0.2,0.2,0.2,1)
##             cm.setName('Gauge')
##             c = self.speedometerImages.attachNewNode(cm.generate())
##             c.setTexture(loader.loadTexture('src/maps/speedometer_gauge.tif'),1)
##             c.setColor(1,1,1,1)
##             cm.setName('Spin')
##             c = self.speedometerImages.attachNewNode(cm.generate())
##             c.setTexture(loader.loadTexture('src/maps/speedometer_spin.tif'),1)
##             c.setColor(1,1,1,1)
##             self.speedGauge = c
##             cm.setName('Tics')
##             c = self.speedometerImages.attachNewNode(cm.generate())
##             c.setTexture(loader.loadTexture('src/maps/speedometer_tics.tif'),1)
##             c.setColor(0,1,0.5,1)
##             cm.setName('Ring')
##             c = self.speedometerImages.attachNewNode(cm.generate())
##             c.setTexture(loader.loadTexture('src/maps/speedometer_ring.tif'),1)
##             c.setColor(0.75,1,1,1)

            self.speedometer = DirectLabel(
                relief = None,
                pos = (1.24, 0.0, -0.98),
                text = str(0),
                text_scale = 0.18,
                text_fg = bodyColor,
                text_pos = (-0.04, 0.02, 0),
                text_font = ToontownGlobals.getSignFont(),
                )

        else:
            self.showSpeedometer()

        self.arrowVert = 0
        self.arrowHorz = 0

    def showSpeedometer(self):
        if self.speedometer:
            self.speedometer.show()
            self.speedometerImages.show()
            
    def hideSpeedometer(self):
        if self.speedometer:
            self.speedometer.hide()
            self.speedometerImages.hide()

    def __disableControlInterface(self):
        assert self.notify.debug("Disabling controls")
        #self.__turnOffMagnet()

        self.hideSpeedometer()
        self.disableControls()

        #NametagGlobals.setOnscreenChatForced(0)
        self.stopSmooth()
        taskMgr.remove('watchVehicleControls')
        #self.__setMoveSound(None)

    def __deleteControlInterface(self):
        if self.speedometer:
            self.speedometer.destroy()
            self.speedometer = None
            self.speedGauge = None
            self.speedometerImages.removeNode()
            self.speedometerImages = None

    def setTurbo(self, setting):
        self.turbo = setting
        if self.turbo:
            self.turboLoopSfx.play()
        else:
            self.turboLoopSfx.stop()

    def interruptTurbo(self):
        self.__stopTurbo()
        if self.cameraTrack:
            self.cameraTrack.finish()
            self.cameraTrack = None
        
    def startTurbo(self):
        # set up some data for our turbo
        newCameraPos = Point3(0, -25, 16)
        newCameraFov = 90
        turboDuration = 3
        startFov = base.camLens.getFov().getX()

        if self.cameraTrack:
            self.cameraTrack.pause()
            
        # create a camera track... modify pos and fov
        cameraZoomIn = Parallel(
            LerpPosInterval(camera, 2, newCameraPos),
            LerpFunc(base.camLens.setFov,
                     fromData = startFov,
                     toData = newCameraFov,
                     duration = 2,
                     ),
            )
        cameraToNormal = Parallel(
            LerpPosInterval(camera, 1, Point3(0,-33,16), newCameraPos),
            LerpFunc(base.camLens.setFov,
                     fromData = newCameraFov,
                     toData=ToontownGlobals.DefaultCameraFov,
                     duration = 1,
                     ),
            )
        self.cameraTrack = Sequence(
            Func(self.turboStartSfx.play),
            cameraZoomIn,
            Func(lambda : self.setTurbo(True)),
            Wait(turboDuration),
            Func(self.__stopTurbo),
            cameraToNormal,
            )
        self.cameraTrack.start()

    def __stopTurbo(self, task = None):
        self.setTurbo(False)
        
    def __controlPressed(self):
        self.__throwGag()
        #self.startTurbo()

    def __controlReleased(self):
        pass


    def __upArrow(self, pressed):
        #self.__incrementChangeSeq()
        #self.__cleanupCraneAdvice()
        if pressed: 
            self.arrowVert = 1
        else:
            if self.arrowVert > 0:
                self.arrowVert = 0
                
    def __downArrow(self, pressed):
        #self.__incrementChangeSeq()
        #self.__cleanupCraneAdvice()
        if pressed:
            self.arrowVert = -1
        else:
            if self.arrowVert < 0:
                self.arrowVert = 0

    def __rightArrow(self, pressed):
        #self.__incrementChangeSeq()
        #self.__cleanupCraneAdvice()
        if pressed:
            self.arrowHorz = 1
            self.rightHeld += 1
        elif self.arrowHorz > 0:
            self.arrowHorz = 0
            self.rightHeld = 0

    def __leftArrow(self, pressed):
        #self.__incrementChangeSeq()
        #self.__cleanupCraneAdvice()
        if pressed:
            self.arrowHorz = -1
            self.leftHeld += 1
        elif self.arrowHorz < 0:
            self.arrowHorz = 0
            self.leftHeld = 0

    def __updateNonlocalVehicle(self, task = None):
        self.curSpeed = self.smoother.getSmoothForwardVelocity()
        rotSpeed = -1*self.smoother.getSmoothRotationalVelocity()

        self.leanAmount = self.curSpeed * rotSpeed / 500.0
        self.leanAmount = clampScalar(self.leanAmount, -10, 10)
        self.__animate()

        return Task.cont
        
    # This  should get called for all cars, not just the local one
    def __animate(self):
        speed = self.curSpeed

        # spin the wheels based on our current Speed
        self.spinWheels(speed/10)

        #modify the pitch of the engine
        enginePitch = clampScalar(speed / 120.0, 0.5, 15)
        self.kartLoopSfx.setPlayRate(enginePitch)

        # modify the volume of the engine based on distance from
        # local avatar
        if not self.localVehicle:
            dist = (self.getPos() - localAvatar.getPos()).length()
        
        #let's keep track of whether we're off the ground or not.
        if self.localVehicle:
            if self.lifter.isOnGround():
                if self.offGround > 10:
                    kart = self.geom[0].find("**/main*")
                    bumpDown1 = kart.posInterval(.1,Vec3(0,0,-1))
                    bumpUp1 =   kart.posInterval(.15,Vec3(0,0,0))
                    bumpDown2 = kart.posInterval(.5,Vec3(0,0,-.4))
                    bumpUp2 =   kart.posInterval(.7,Vec3(0,0,0))
                    bumpSeq = Sequence(bumpDown1,bumpUp1,bumpDown2,bumpUp2)
                    bumpSeq.start()
                self.offGround = 0
            else:
                self.offGround += 1
            
        #add in a little 'jitter' based on the ground type
        if(self.offGround == 0):
            modifier = self.surfaceModifiers[self.groundType]['shake']*(speed/50.0)
        else:
            modifier=1

        roll = self.leanAmount * 1.5
        roll += ((random.random() * 2) - 1) * modifier
        pitch = self.acceleration * -.005
        pitch += ((random.random() * 2) - 1) * modifier

        self.rollSuspension(roll)
        self.pitchSuspension(pitch)
        
        return Task.cont

    
    def __clampPosition(self):
        """
        Make sure our x, y, and z is valid for a distributedSmoothNode.
        Returns True if we did do a clam
        """
        retVal = False;
        if (self.getX() < -3276):
            self.notify.debug("clamping X %d" % self.getX())            
            self.setX(-3276)
            retVal = True
        if (self.getX() > 3276):
            self.notify.debug("clamping X %d" % self.getX())            
            self.setX(3276)            
            retVal = True
        if (self.getY() < -3276):
            self.notify.debug("clamping Y %d" % self.getY())            
            self.setY(-3276)
            retVal = True
        if (self.getY() > 3276):
            self.notify.debug("clamping Y %d" % self.getY())                   
            self.setY(3276)
            retVal = True
        if (self.getZ() < -3276):
            self.notify.debug("clamping Z %d" % self.getZ())
            self.setZ(-3276)
            retVal = True
        if (self.getZ() > 3276):
            self.notify.debug("clamping Z %d" % self.getZ()) 
            self.setZ(3276)
            retVal = True

        return retVal

    def  amIClampingPosition(self):
        return (self.getX() == -3276 or
                self.getX() == 3276 or
                self.getY() == -3276 or
                self.getY() == 3276 or
                self.getZ() == -3276 or
                self.getZ() == 3276)
                
    def __computeTurnRatio(self, speed):
        effectiveSpeed = speed
        if effectiveSpeed > self.speedMinTurn:
            effectiveSpeed = self.speedMinTurn
        #turnRatio = 1.0 / 0.025 * math.sqrt(cheatFactor) #jml
        if effectiveSpeed < self.speedMaxTurn:
            turnRatio = 1.0 * effectiveSpeed
        elif effectiveSpeed >= self.speedMaxTurn:
            turnRatio = 1.0 * (effectiveSpeed * (self.speedMaxTurn / speed))
        #self.turnRatio = turnRatio
        
    def __updateWheelPos(self, dt, curSpeed):
        ratioIntoMax = (curSpeed - self.speedMinTurn) / (self.speedMaxTurn - self.speedMinTurn)
        if ratioIntoMax > 1.0:
            ratioIntoMax = 1.0
        if ratioIntoMax < 0.0:
            ratioIntoMax = 0.0
            
        maxWheelDeflection = (self.wheelMaxTurn * ratioIntoMax) + (self.wheelMinTurn * (1.0 - ratioIntoMax))
        
        if self.wheelPosition * self.arrowHorz > 0:
            self.wheelPosition += self.arrowHorz * dt / self.wheelTurnTime
        else:
            self.wheelPosition += self.arrowHorz * dt / self.wheelFightTime
        
        #recenter wheel if controls are released
        if not self.arrowHorz:
            if self.wheelPosition > 0:
                self.wheelPosition -= dt / self.wheelReturnTime
                if self.wheelPosition < 0:
                    self.wheelPosition = 0
            else:
                self.wheelPosition += dt / self.wheelReturnTime
                if self.wheelPosition > 0:
                    self.wheelPosition = 0
        
        if abs(self.wheelPosition) >= maxWheelDeflection:
            if self.wheelPosition > 0:
                self.wheelPosition = maxWheelDeflection
            else:
                self.wheelPosition = -maxWheelDeflection
        
        #self.outPutCounter += 1
        #if self.outPutCounter > 5:
            #self.outPutCounter = 0           
            #print("curSpeed:%s ratioIntoMax:%s Max %s" % (curSpeed, ratioIntoMax, maxWheelDeflection))
        

    def __watchControls(self, task):
        dt = globalClock.getDt()
        curVelocity = self.actorNode.getPhysicsObject().getVelocity()
        curSpeed = curVelocity.length()
        
        # Get the forward direction of the kart
        fvec = self.forward.getPos(render) - self.getPos(render)
        fvec.normalize()
        
        dotProduct = curVelocity.dot(fvec)
        goingBack = -1
        
        if dotProduct < 0:
            goingBack = 1
        
        if self.proRacer:
            self.__computeTurnRatio(curSpeed)
            self.__updateWheelPos(dt, curSpeed)

        newHForTurning = self.getH()
        if (self.proRacer) or (not self.stopped and self.arrowHorz  and curSpeed > 1):
            #scale the rotation
            if self.proRacer:
                turnHelp = 0
                if self.hittingWall or goingBack == 1:
                    turnHelp = self.arrowHorz
                effectiveSpeed = curSpeed
                if effectiveSpeed > self.speedMinTurn:
                    effectiveSpeed = self.speedMinTurn
                rotation = -goingBack * ((self.wheelPosition * dt * self.turnRatio * -1.8 * curSpeed/100) + (turnHelp * dt * self.turnRatio * -1.2))
                
                self.outPutCounter += 1
                if self.outPutCounter > 5:
                    self.outPutCounter = 0 
                    #print("dotProduct: %s curVelocity: %s goingBack:%s " % (dotProduct, curVelocity, goingBack))
                    
            else:
                rotation = self.arrowHorz * dt * self.turnRatio * -1.2
            #rotate the model
            oldH = self.getH()
            newH = (oldH + rotation) % 360
            self.setH(newH)
            newHForTurning = newH
            if (self.groundType == 'ice'):
                newHForTurning = (oldH + rotation * iceTurnFactor) % 360

        pitch=-self.getP()+5

        #pitch is now biased properly, now move everything below 30 up

        #Goal, lock acceleration at a base of 20
        accelBase = self.accelerationBase
        pitch+=accelBase
        pitch = clampScalar(pitch, accelBase-5, accelBase+5)
        self.accelerationMult=pitch*2

        if (self.groundType == 'ice' ):
            self.accelerationMult *= iceAccelFactor
        
        
        #apply an acceleration
        if self.stopped:
            self.acceleration = 0
        else:
            self.acceleration = self.arrowVert * self.accelerationMult * self.cheatFactor #jml
            if self.proRacer:
                if self.skidding:
                    self.acceleration = self.arrowVert * self.accelerationMult * self.cheatFactor * 0.5
            if self.turbo:
                self.acceleration += (self.accelerationMult*1.5)

        self.engine.setVector(Vec3(0, self.acceleration, 0))
        
        # rotMat is the rotation matrix corresponding to
        # the geometry heading.
        if (self.groundType == 'ice' ):
            rotMat=Mat3.rotateMatNormaxis(newHForTurning, Vec3.up())            
        else:
            rotMat=Mat3.rotateMatNormaxis(self.getH(), Vec3.up())
        curHeading=rotMat.xform(Vec3.forward())
        push=(3-self.getP())*.02
        curHeading.setZ(curHeading.getZ()-min(.2,max(-.2,push)))

        onScreenDebug.append("vehicle curHeading = %s\n"%curHeading.pPrintValues())
        onScreenDebug.append("vehicle H = %s  newHForTurning=%f\n" % (self.getH(), newHForTurning))


        #onScreenDebug.append("vehicle roll = %s\n"%roll)

        #modify the wind resistance based on the ground type
        # (this should be tireFriction or something, but this works :)
        windResistance = self.surfaceModifiers[self.groundType]['windResistance']
        self.windResistance.setCoef(windResistance)

        # Perform exactly n physics calculations per second,
        # regardless of our rendering frame rate.  This will make the
        # race fairer to those with a slower computer.
        
        physicsFrame = int((globalClock.getFrameTime() - self.physicsEpoch) * self.physicsCalculationsPerSecond)
        numFrames = min(physicsFrame - self.lastPhysicsFrame, self.maxPhysicsFrames)
        self.lastPhysicsFrame = physicsFrame

        leanIncrement = (self.arrowHorz * self.physicsDt * self.turnRatio)
        if self.stopped:
            leanIncrement = 0

        driftMin = self.surfaceModifiers[self.groundType]['driftMin'] #* 0.5 #jml
        if self.proRacer:
            driftMin = self.surfaceModifiers[self.groundType]['driftMin'] * 0.2
            if self.skidding:
                driftMin = self.surfaceModifiers[self.groundType]['driftMin']

        # Everything within this loop is performed n times per second
        # with the physics calculations.
        for i in range(numFrames):
            self.physicsMgr.doPhysics(self.physicsDt)

            # set the new tire friction force
            curVelocity = self.actorNode.getPhysicsObject().getVelocity()
            idealVelocity = curHeading * curSpeed
            curVelocity *= self.imHitMult

            # rotate the velocity partially in the direction of the
            # geometry heading
            driftVal = (abs(self.leanAmount) * 16 / self.cheatFactor) + 15 / self.cheatFactor 
            curVelocity = Vec3(((curVelocity * driftVal)+ idealVelocity) / (driftVal+1))

            # cap speed to 200 (600/3)
            curSpeed = curVelocity.length()
            curVelocity.normalize()
            curVelocity *= min(curSpeed, 600)
            self.actorNode.getPhysicsObject().setVelocity(curVelocity)

            # figure out how much to 'lean' the vehicle
            curSpeed = curVelocity.length()
            speedFactor = min(curSpeed, 150) / 162.0
            self.leanAmount = (self.leanAmount + leanIncrement) * speedFactor
            self.leanAmount = clampScalar(self.leanAmount, -10, 10)

        # It's tempting to put this collision traversal in the above
        # loop for more accurate wall collisions, but that would be
        # more expensive, and I don't think we need it.  Besides, we'd
        # have to deal with resetting the previous transform each pass,
        # which would confuse the main collision traverser.
        self.cWallTrav.traverse(render)

        self.curSpeed = curSpeed
        if self.proRacer:
            self.turnWheels(self.wheelPosition * -45)
        else:
            self.turnWheels(self.arrowHorz * -10)
        self.__animate()

        # make sure the camera follows the velocity direction,
        # not the kart facing
        if self.proRacer:
            
            speedProporation = 1.0
            if curSpeed < self.speedMaxTurn:
                speedProporation = 0.0
            else:
                speedProporation = (curSpeed - self.speedMaxTurn) / self.speedMinTurn
                
            cameraDist = self.cameraArmBase + self.cameraArmExtend * speedProporation
                
            cameraOffset = Point3(0, -cameraDist, 0)
            self.cameraNode.setPos(cameraOffset)
            
            behindPos = render.getRelativePoint(self, Point3(0, -30, 0))
            self.proCameraDummyNode.setPos(render, behindPos)
            self.proCameraDummyNode.lookAt(self)
            self.cameraNode.lookAt(self)
            dir1 = self.proCameraDummyNode.getH()
            dir2 = self.proCameraHeading
            
            if dir1 > 180:
                dir1 -= 360
            elif dir1 < -180:
                dir1 += 360
                
            if dir2 > 180:
                dir2 -= 360
            elif dir2 < -180:
                dir2 += 360
                
            self.proCameraHeading = dir2
                
            dif = dir1 - dir2

            if dif > 180:
                dif -= 360
            elif dif < -180:
                dif += 360
            
            speedDif = abs(dif)
            if speedDif > 90:
                speedDif = 90
            
            cameraTightener = 1.0

            if curSpeed > self.speedMinTurn:
                cameraTightener = self.cameraTightener
            else:
                cameraTightener = 1.0 + (curSpeed / self.speedMinTurn) * (self.cameraTightener - 1.0)
                
            swingSpeedRatio = speedDif / 90
            swingSpeed = (self.armSwingSpeedPerp * swingSpeedRatio) + (self.armSwingSpeedPara * (1 - swingSpeedRatio))

            self.proCameraHeading += dif * cameraTightener * (dt / swingSpeed)
            
            
            
            #self.proCameraHeading = self.proCameraDummyNode.getH()
            #self.cameraNode.setH(self.proCameraDummyNode.getH())
            #self.cameraNode.setH(self.proCameraHeading - self.getH())
            self.cameraArmNode.setH(self.proCameraHeading - self.getH())
            #self.cameraArmNode.setH(-90)
            

            
        elif not self.stopped:
            self.cameraNode.setH(self.leanAmount)

        # update drift particles
        self.updateParticles(self.leanAmount)

        if (self.leanAmount > 8 or self.leanAmount < -8) and (self.offGround <= 0):
            #don't do the skid effect if we are in midair
            self.startSkid()
        else:
            self.stopSkid()

        # set the speedometer
        if self.speedometer:
            self.speedometer['text'] = str(int(curSpeed/3))
            self.speedGauge.setR(min(110,max(0,curSpeed/3/120*110)))

        # make sure the car is angled to touch the ground
        if not self.stopped:
            self.stickCarToGround()

        #some hacks so the client doesn't crash due to out range for position
        if self.__clampPosition():
            self.notify.debug("did a clampPosition on %d" % self.doId)
            pass

        return Task.cont
    
    def enableControls(self):
        self.canRace=True
        self.accept('control', self.__controlPressed)
        self.accept('control-up', self.__controlReleased)
        self.accept('InputState-forward', self.__upArrow)
        self.accept('InputState-reverse', self.__downArrow)
        self.accept('InputState-turnLeft', self.__leftArrow)
        self.accept('InputState-turnRight', self.__rightArrow)

    def disableControls(self):
        self.arrowVert = 0
        self.arrowHorz = 0
        
        #self.ignore('escape')
        self.ignore('control')
        self.ignore('control-up')
        self.ignore("tab")
        self.ignore('InputState-forward')
        self.ignore('InputState-reverse')
        self.ignore('InputState-turnLeft')
        self.ignore('InputState-turnRight')

    #A distributed call from the ai that allows it to start and stop the car
    def setInput(self,on):
        if(localAvatar.doId==self.ownerId):
            if(on):
                self.enableControls()
            else:
                self.disableControls()

    def shakeWheel(self, nWheel, floorNode):
        groundType = floorNode.getNetTag('surface')
        modifier = self.surfaceModifiers[groundType]['shake']
        shakeFactor = ((random.random() * 2) - 1) * modifier
        shakeFactor *= (self.curSpeed / 200)

        node = self.wheelCenters[nWheel].find('*Wheel')
        node.setZ(shakeFactor)
        

    def stickCarToGround(self):
        posList = []
        nWheels = len(self.wheelData)

        # Find the first entry for each ray
        for nWheel in range(nWheels):
            cQueue = self.cQueue[nWheel]
            cQueue.sortEntries()
            #import pdb; pdb.set_trace()
            if cQueue.getNumEntries() == 0:
                # If any wheel is not over any collidable ground,
                # never mind.
                return

            entry = cQueue.getEntry(0)

            self.shakeWheel(nWheel, entry.getIntoNodePath())
            pos = entry.getSurfacePoint(render)
            wheelPos = self.wheelBases[nWheel].getPos(render)
            pos = wheelPos - pos
            posList.append(pos)

            # Now be sure the queue is cleared for next time.
            cQueue.clearEntries()

        # Now get the points that each of these detected.
        rf = posList[0].getZ()
        lf = posList[1].getZ()
        rr = posList[2].getZ()
        lr = posList[3].getZ()

        #onScreenDebug.append("vehicle rf = %s\n" % rf)
        #onScreenDebug.append("vehicle lf = %s\n" % lf)
        #onScreenDebug.append("vehicle rr = %s\n" % rr)
        #onScreenDebug.append("vehicle lr = %s\n" % lr)

        # the amount we should 'roll' depends on the averaged
        # right point and the averaged left point
        right = (rf + rr) / 2
        left = (lf + lr) / 2
        rollVal = right-left
        rollVal = clampScalar(rollVal, -1, 1)
        curRoll = self.getR()
        newRoll = curRoll + rollVal*2.0
        self.setR(newRoll)
        if(not self.stopped):
            camera.setR(-newRoll)

        # the amount we should 'pitch' depends on the averaged
        # front point and the averaged rear point
        front = (rf + lf) / 2
        rear = (rr + lr) / 2
        center = (front + rear) / 2
        pitchVal = front-rear
        pitchVal = clampScalar(pitchVal, -1, 1)
        curPitch = self.getP()
        newPitch = curPitch - (pitchVal*2.0)
        #if(self.onGround):
        #    self.geom.setP(newPitch)
        #else:
        self.setP((newPitch+curPitch)/2.0)
        if self.proRacer:
            self.cameraNode.setP(-newPitch)
        elif(not self.stopped):
            self.cameraNode.setP(-newPitch)


    def setBodyType( self, bodyType ):
        """
        Purpose: The setBodyType Method sets the local AI side
        body type of the kart that the toon currently owns.
        
        
        Params: bodyType - the body type of the kart which the toon
        currently owns.
        Return: None
        """
        self.kartDNA[ KartDNA.bodyType ] = bodyType

    def setBodyColor( self, bodyColor ):
        """
        Purpose: The setBodyColor Method appropriately sets
        the body color of the lient on the ai side by updating the
        local kart dna.
        
        Params: bodyColor - the color of the kart body.
        Return: None
        """
        self.kartDNA[ KartDNA.bodyColor ] = bodyColor

    def setAccessoryColor( self, accColor ):
        """
        Purpose: The setAccessoryColor Method appropriately sets
        the accessory color of the local ai side by updating the kart
        dna.

        Params: accColor - the color of the accessories.
        Return: None
        """
        self.kartDNA[ KartDNA.accColor ] = accColor

    def setEngineBlockType( self, ebType ):
        """
        Purpose: The setEngineBlockType Method sets the engine
        block type accessory for the kart by updating the Kart DNA.
        
        Params: ebType - the type of engine block accessory.
        Return: None
        """
        self.kartDNA[ KartDNA.ebType ] = ebType

    def setSpoilerType( self, spType ):
        """
        Purpose: The setSpoilerType Method sets the spoiler
        type accessory for the kart by updating the Kart DNA.
        
        Params: spType - the type of spoiler accessory
        Return: None
        """
        self.kartDNA[ KartDNA.spType ] = spType

    def setFrontWheelWellType( self, fwwType ):
        """
        Purpose: The setFrontWheelWellType Method sets the
        front wheel well accessory for the kart updating the
        Kart DNA.
        
        Params: fwwType - the type of Front Wheel Well accessory
        Return: None
        """
        self.kartDNA[ KartDNA.fwwType ] = fwwType

    def setBackWheelWellType( self, bwwType ):
        """
        Purpose: The setWheelWellType Method sets the Back
        Wheel Wheel accessory for the kart by updating the Kart DNA.
        
        Params: bwwType - the type of Back Wheel Well accessory.
        Return: None
        """
        self.kartDNA[ KartDNA.bwwType ] = bwwType

    def setRimType( self, rimsType ):
        """
        Purpose: The setRimType Method sets the rims accessory
        for the karts tires by updating the Kart DNA.
        
        Params: rimsType - the type of rims for the kart tires.
        Return: None
        """
        self.kartDNA[ KartDNA.rimsType ] = rimsType

    def setDecalType( self, decalType ):
        """
        Purpose: The setDecalType Method sets the decal
        accessory of the kart by updating the Kart DNA.
        
        Params: decalType - the type of decal set for the kart.
        Return: None
        """
        self.kartDNA[ KartDNA.decalType ] = decalType

    def setOwner(self,avId):
        self.ownerId=avId

    def stopCar(self,level):
        #vel=self.actorNode.getPhysicsObject().getVelocity()
        #vel=vel*.1
        self.imHitMult=level
        if(hasattr(self,"cameraTrack") and self.cameraTrack):
           self.cameraTrack.pause()
           cameraToNormal = Parallel(
            LerpPosInterval(camera, 0.05, Point3(0,-33,16),startPos=camera.getPos()),
            LerpFunc(base.camLens.setFov,
                     fromData = base.camLens.getFov()[0],
                     toData=ToontownGlobals.DefaultCameraFov,
                     duration = 0.05,
                     ),
            )
           cameraToNormal.start()
        self.__stopTurbo()
        self.stopped=True

    def startCar(self):
        self.imHitMult=1
        self.stopped=False

    
    def hideAnvil(self):
        self.anvil.reparentTo(hidden)
        self.anvil.setAlphaScale(1)
        self.dropShadow.setScale(self.ShadowScale)

    def spinCar(self,spin):
        self.geom[0].setH(2*spin)


    def playSpin(self,timeStamp):
        delta=-globalClockDelta.networkToLocalTime(timeStamp,globalClock.getFrameTime(),16,100)+globalClock.getFrameTime()
        self.spinAnim=LerpFunc(self.spinCar,fromData=0,toData=360,duration=min(1-delta,0))
        self.spinAnim.start()
        
        

    def __throwGag(self):
        base.race.shootGag()
        

    #Mock up of a gag falling on your head, push tab to test on self
    def dropOnMe(self,timestamp):
        self.anvil.setScale(7,9,7)
        self.anvil.setPos(0,0,75)
        self.anvil.reparentTo(self)
        anvilDrop=ProjectileInterval(self.anvil,startPos = Point3(0,0,100),endPos = Point3(0,0, 0), duration = 1)
        shadowScale=self.dropShadow.scaleInterval(1,self.ShadowScale*2)
        fadeOut=LerpFunc(self.anvil.setAlphaScale,fromData=1,toData=0, duration=.5)
        flattenMe=self.geom[0].scaleInterval(.08,Vec3(1,1,.1))
        unFlatten=Sequence(self.geom[0].scaleInterval(.2,Vec3(1,1,2)),self.geom[0].scaleInterval(.1,1))
        anvilSquish=Parallel(Parallel(anvilDrop,shadowScale),Sequence(Wait(.92),flattenMe))

        anvilStretchFade=Sequence(Parallel(self.anvil.scaleInterval(.2,Vec3(7,9,5)),Func(self.lookUp)),fadeOut)
        self.gagMovie=Sequence(anvilSquish,Func(self.stopCar,.9),anvilStretchFade,Wait(.5),Parallel(unFlatten,Func(self.lookNormal)),Func(self.startCar),Func(self.hideAnvil))
        self.gagMovie.start()

    def lookUp(self):
        # make sure we still have a toon
        if self.toon and self.toon.headParts:
            headParts = self.toon.headParts
            for hi in range(headParts.getNumPaths()):
                head = headParts[hi]
                head.setP(90)

    def lookNormal(self):
        # make sure we still have a toon
        if self.toon and self.toon.headParts:
            headParts = self.toon.headParts
            for hi in range(headParts.getNumPaths()):
                head = headParts[hi]
                head.setP(0)

    def flattenMe(self):
        self.geom[0].setScale(3,3,.1)

    def unFlattenMe(self):
        self.geom[0].setScale(2)

    def startSkid(self):
        if self.skidding == False:
            self.skidding = True
            self.skidLoopAsphaltSfx.play()
            #self.skidLoopGrassSfx.play()
            #self.updateSkid()

    def stopSkid(self):
        if self.skidding == True:
            self.skidding = False
            self.skidLoopAsphaltSfx.stop()
            self.skidLoopGrassSfx.stop()

    def updateSkid(self):
        if self.skidding:
            if self.groundType == 'grass':
                self.skidLoopGrassSfx.setVolume(1)
                self.skidLoopAsphaltSfx.setVolume(0)
            else:
                self.skidLoopGrassSfx.setVolume(0)
                self.skidLoopAsphaltSfx.setVolume(1)

    def dropOnHim(self,timestamp):
        self.anvil.setScale(10,13,10)
        self.anvil.setPos(0,0,75)
        self.anvil.reparentTo(self)
        anvilDrop=ProjectileInterval(self.anvil,startPos = Point3(0,0,100),endPos = Point3(0,0, 0), duration = 1)
        shadowScale=self.dropShadow.scaleInterval(1,self.ShadowScale*4)
        fadeOut=LerpFunc(self.anvil.setAlphaScale,fromData=1,toData=0, duration=.5)
        flattenMe=self.geom[0].scaleInterval(.08,Vec3(1,1,.1))
        unFlatten=Sequence(self.geom[0].scaleInterval(.2,Vec3(1,1,2)),self.geom[0].scaleInterval(.1,1))
        anvilSquish=Parallel(Parallel(anvilDrop,shadowScale),Sequence(Wait(.92),flattenMe))

        anvilStretchFade=Sequence(Parallel(self.anvil.scaleInterval(.2,Vec3(10,13,4)),Func(self.lookUp)),fadeOut)
        self.gagMovie=Sequence(anvilSquish,anvilStretchFade,Wait(.5),Parallel(unFlatten,Func(self.lookNormal)),Func(self.hideAnvil))
        self.gagMovie.start()


    def hitBanana(self):
        #print "yar, got Me"

        if(self.wipeOut):
            self.wipeOut.pause()
            spinAnim=LerpFunc(self.spinCar,fromData=self.geom[0].getH(),toData=360,duration=1)
        else:
            spinAnim=LerpFunc(self.spinCar,fromData=0,toData=360,duration=1)
        self.wipeOut=Sequence(Func(self.stopCar,.99),spinAnim,Func(self.startCar))
        self.wipeOut.start()
        

    def hitPie(self):
        print "yar, got Me with pi!"
        self.splatPie()
        if(self.wipeOut):
            self.wipeOut.pause()
            spinAnim=LerpFunc(self.spinCar,fromData=self.geom[0].getH(),toData=1080,duration=0.5)
        else:
            spinAnim=LerpFunc(self.spinCar,fromData=0,toData=1080,duration=0.5)
        self.wipeOut=Sequence(Func(self.stopCar,.99),spinAnim,Func(self.startCar))
        self.wipeOut.start()

    def finishMovies(self):
        if self.gagMovie:
            self.gagMovie.finish()
            self.gagMovie = None

        if self.wipeOut:
            self.wipeOut.finish()
            self.wipeOut = None

        if self.spinAnim:
            self.spinAnim.finish()
            self.spinAnim = None
