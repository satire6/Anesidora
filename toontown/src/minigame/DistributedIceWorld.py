from pandac.PandaModules import Vec4, BitMask32, Quat, Point3, NodePath
from pandac.PandaModules import OdePlaneGeom, OdeBody, OdeSphereGeom, OdeMass, \
     OdeUtil, OdeBoxGeom
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import DistributedMinigamePhysicsWorld
from toontown.minigame import IceGameGlobals
from toontown.golf import BuildGeometry

# multiply a meters value by this constant to get feet
MetersToFeet = 3.2808399
# multiply a feet value by this constant to get meters
FeetToMeters = 1.0 / MetersToFeet
    
class DistributedIceWorld(DistributedMinigamePhysicsWorld.DistributedMinigamePhysicsWorld):
    """Base class client minigame physics.
    
    Should not have any hardcoded info which is specific to a given game.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMinigamePhysicsWorld")


    # ODE Collision bits
    # 0 - floor
    # 1 - fence
    # 2
    # 3
    # 4
    # 5
    # 6
    # 7
    # 8 - tire 0
    # 9 - tire 1
    # 10 - tire 2
    # 11 - tire 3
    floorCollideId = 1
    floorMask = BitMask32(floorCollideId)
    wallCollideId = 1 << 1
    wallMask = BitMask32( wallCollideId)
    obstacleCollideId = 1 << 2
    obstacleMask = BitMask32 (obstacleCollideId)

    tireCollideIds = [ 1<<8, 1 <<9, 1<<10, 1<<11]
    tire0Mask = BitMask32( tireCollideIds[0])
    tire1Mask = BitMask32( tireCollideIds[1])
    tire2Mask = BitMask32( tireCollideIds[2])
    tire3Mask = BitMask32( tireCollideIds[3])

    allTiresMask =  tire0Mask | tire1Mask | tire2Mask | tire3Mask
    tireMasks = (tire0Mask, tire1Mask, tire2Mask, tire3Mask)

    tireDensity = 1 # 1 kg per foot cubed
                          

    tireSurfaceType = 0
    iceSurfaceType = 1
    fenceSurfaceType = 2

    #tireCollideId = 1 << 12
    
    def __init__(self,cr):
        """Create the Ice world."""
        DistributedMinigamePhysicsWorld.DistributedMinigamePhysicsWorld.__init__(self,cr)

    def delete(self):
        """Remove ourself from the world."""
        DistributedMinigamePhysicsWorld.DistributedMinigamePhysicsWorld.delete(self)
        if hasattr(self, 'floor'):
            # the floor seems to be destroyed automatically in ODE 0.9
            # at least I see the number of constructors and destructors match up
            # self.floor.destroy() # we get a c++ crash now if we call this
            self.floor = None


    def setupSimulation(self):
        """Setup the ice game specific parameters."""
        DistributedMinigamePhysicsWorld.DistributedMinigamePhysicsWorld.setupSimulation(self)
        # toontown uses feet, 1 meter = 3.2808399 feet
        # for this game lets express mass in kilograms
        # so gravity at 9.8 meters per seconds squared becomes        
        self.world.setGravity(0,0,-32.174)

        # ODE's default is meter, kilograms, seconds, let's change the defaults
        # do we need to change global ERP value,
        # that controls how much error correction is performed in each time step
        # default is 0.2
        self.world.setAutoDisableFlag(1) # lets try auto disable
        self.world.setAutoDisableLinearThreshold(0.5 * MetersToFeet)
        # skipping AutoDisableAngularThreshold as that is radians per second
        # self.world.setAutoDisableAngularThreshold(0.01)
        # don't consider rotation for auto disable
        self.world.setAutoDisableAngularThreshold(OdeUtil.getInfinity())
        self.world.setAutoDisableSteps(10)

        # Set and the global CFM (constraint force mixing) value.
        # Typical values are in the range 10-9 -- 1.
        # The default is 10-5 if single precision is being used
        self.world.setCfm(1E-5 * MetersToFeet)

        # Our surfaces
        # 0 = tire
        # 1 = ice
        # 2 = fence
        self.world.initSurfaceTable(3) # 3 types of surfaces

        # PN_uint8 pos1, PN_uint8 pos2,  - surface0, surface1
        #            dReal mu, - 0 frictionless, 1 infinite friction
        #            dReal bounce, # Restitution parameter 0 not bouncy, 1 max bouncy
        #            dReal bounce_vel, #The minimum incoming velocity necessary for bounce.
        #                              Incoming velocities below this will
        #                              effectively have a bounce parameter of 0.
        #            dReal soft_erp, # Contact normal "softness" parameter. 
        #            dReal soft_cfm, # Contact normal "softness" paramete
        #            dReal slip,     # The coefficients of force-dependent-slip (FDS) 
        #            dReal dampen)   # dampening constant
        
        # the most usual collision, tire against ice
        self.world.setSurfaceEntry(0, 1,
                                   0.2, # near frictionless
                                   0, # not bouncy
                                   0, # bounce_vel
                                   0, # soft_erp
                                   0, # soft_cfm
                                   0, # slip
                                   0.1, # dampen
                                   )
        # tire against tire                           
        self.world.setSurfaceEntry(0, 0,
                                   0.1, # friction
                                   0.9, # bounciness
                                   0.1, # bounce_vel
                                   0, # soft_erp
                                   0, # soft_cfm
                                   0, # slip
                                   0, # dampen
                                   )

        # tire against fence
        self.world.setSurfaceEntry(0, 2,
                                   0.9, # friction
                                   0.9, # bounciness
                                   0.1, # bounce_vel
                                   0, # soft_erp
                                   0, # soft_cfm
                                   0, # slip
                                   0, # dampen
                                   )        
        
        # Create a plane geom which prevent the objects from falling forever
        self.floor = OdePlaneGeom(self.space, Vec4(0.0,0.0,1.0,-20.0))
        self.floor.setCollideBits( self.allTiresMask ) # we only collide against tires
        self.floor.setCategoryBits( self.floorMask)
 

        # normal pointing towards +x axis
        self.westWall = OdePlaneGeom(self.space, Vec4(1.0, 0.0, 0.0, IceGameGlobals.MinWall[0]))
        self.westWall.setCollideBits(  self.allTiresMask )  # we only collide against tires
        self.westWall.setCategoryBits(self.wallMask)
        self.space.setSurfaceType(self.westWall, self.fenceSurfaceType)
        self.space.setCollideId(self.westWall, self.wallCollideId)
        
        # normal pointing towards -x axis
        self.eastWall = OdePlaneGeom(self.space, Vec4(-1.0, 0.0, 0.0, -IceGameGlobals.MaxWall[0]))
        self.eastWall.setCollideBits(  self.allTiresMask )   # we only collide against tires
        self.eastWall.setCategoryBits(self.wallMask)
        self.space.setSurfaceType(self.eastWall, self.fenceSurfaceType)        
        self.space.setCollideId(self.eastWall, self.wallCollideId)

        # normal pointing toward the +y axis
        self.southWall = OdePlaneGeom(self.space, Vec4(0.0, 1.0, 0.0, IceGameGlobals.MinWall[1]))
        self.southWall.setCollideBits( self.allTiresMask)   # we only collide against tires
        self.southWall.setCategoryBits( self.wallMask)
        self.space.setSurfaceType(self.southWall, self.fenceSurfaceType)        
        self.space.setCollideId(self.southWall, self.wallCollideId)
        
        # normal pointing toward the -y axis
        self.northWall = OdePlaneGeom(self.space, Vec4(0.0, -1.0, 0.0, -IceGameGlobals.MaxWall[1]))
        self.northWall.setCollideBits( self.allTiresMask)   # we only collide against tires
        self.northWall.setCategoryBits( self.wallMask)
        self.space.setSurfaceType(self.northWall, self.fenceSurfaceType)        
        self.space.setCollideId(self.northWall, self.wallCollideId)

        # a temporary floor at z=0, until we implement ice with holes
        self.floorTemp = OdePlaneGeom(self.space, Vec4(0.0,0.0,1.0, 0.0))
        self.floorTemp.setCollideBits( self.allTiresMask)   # we only collide against tires
        self.floorTemp.setCategoryBits( self.floorMask )
        self.space.setSurfaceType( self.floorTemp, self.iceSurfaceType)
        self.space.setCollideId(self.floorTemp, self.floorCollideId)        
        
        self.space.setAutoCollideWorld(self.world)
        self.space.setAutoCollideJointGroup(self.contactgroup)

        self.totalPhysicsSteps = 0

    def createTire(self, tireIndex):
        """Create one physics tire. Returns a (nodePath, OdeBody, OdeGeom) tuple"""
        if (tireIndex <0) or (tireIndex >= len(self.tireMasks)):
            self.notify.error('invalid tireIndex %s' % tireIndex)
        self.notify.debug("create tireindex %s" % (tireIndex))
        zOffset = 0
        # for now the tires are spheres
        body = OdeBody(self.world)
        mass = OdeMass()
        mass.setSphere(self.tireDensity, IceGameGlobals.TireRadius)
        body.setMass(mass)
        body.setPosition( IceGameGlobals.StartingPositions[tireIndex][0],
                          IceGameGlobals.StartingPositions[tireIndex][1],
                          IceGameGlobals.StartingPositions[tireIndex][2]
                          )
        #body.setAutoDisableFlag(1)
        #body.setAutoDisableLinearThreshold(1.01 * MetersToFeet)
        # skipping AutoDisableAngularThreshold as that is radians per second
        #body.setAutoDisableAngularThreshold(0.1)
        body.setAutoDisableDefaults()
        
        geom = OdeSphereGeom(self.space, IceGameGlobals.TireRadius)
        self.space.setSurfaceType( geom, self.tireSurfaceType)
        self.space.setCollideId(geom,  self.tireCollideIds[tireIndex])

        self.massList.append(mass)
        self.geomList.append(geom)

        # a tire collides against other tires, the wall and the floor
        geom.setCollideBits( self.allTiresMask | self.wallMask | self.floorMask | self.obstacleMask) 
        geom.setCategoryBits( self.tireMasks[tireIndex])
        geom.setBody(body)
        
        if self.notify.getDebug():
            self.notify.debug('tire geom id')
            geom.write()
            self.notify.debug(' -')
            
        if self.canRender:
            testTire = render.attachNewNode("tire holder %d" % tireIndex)
            smileyModel = NodePath() # loader.loadModel('models/misc/smiley') # smiley!
            if not smileyModel.isEmpty():
                smileyModel.setScale(IceGameGlobals.TireRadius)
                smileyModel.reparentTo(testTire)
                smileyModel.setAlphaScale(0.5)
                smileyModel.setTransparency(1)
            testTire.setPos(IceGameGlobals.StartingPositions[tireIndex])
            #debugAxis = loader.loadModel('models/misc/xyzAxis')
            if 0: #not debugAxis.isEmpty():
                debugAxis.reparentTo(testTire)
                debugAxis.setScale(IceGameGlobals.TireRadius / 10.0)
                debugAxis2 = loader.loadModel('models/misc/xyzAxis')
                debugAxis2.reparentTo(testTire)
                debugAxis2.setScale(-IceGameGlobals.TireRadius / 10.0)
            # lets create a black tire
            #tireModel = loader.loadModel('phase_3/models/misc/sphere')
            tireModel = loader.loadModel("phase_4/models/minigames/ice_game_tire")
            # assuming it has a radius of 1
            tireHeight = 1
            #tireModel.setScale(IceGameGlobals.TireRadius, IceGameGlobals.TireRadius, 1)
            #tireModel.setZ( 0 - IceGameGlobals.TireRadius + (tireHeight /2.0))
            #tireModel.setColor(0,0,0)
            tireModel.setZ( -IceGameGlobals.TireRadius + 0.01)
            tireModel.reparentTo(testTire)
            #tireModel.setAlphaScale(0.5)
            #tireModel.setTransparency(1)
                                         
            self.odePandaRelationList.append((testTire, body))
        else:
            testTire = None
            self.bodyList.append((None, body))
        return testTire, body, geom        

    def placeBodies(self):
        """Make the nodePaths match up to the physics bodies."""
        # lets see if a sphere can simulate a tire by just taking out P and R
        for pair in self.odePandaRelationList:
            pandaNodePathGeom = pair[0]
            odeBody = pair[1]
            if pandaNodePathGeom:
                pandaNodePathGeom.setPos(odeBody.getPosition())
                # rotation = (odeBody.getRotation() * (180.0/math.pi))
                pandaNodePathGeom.setQuat(Quat(odeBody.getQuaternion()[0],odeBody.getQuaternion()[1],odeBody.getQuaternion()[2],odeBody.getQuaternion()[3]))
                pandaNodePathGeom.setP(0)
                pandaNodePathGeom.setR(0)
                newQuat = pandaNodePathGeom.getQuat()
                odeBody.setQuaternion(newQuat)

    def postStep(self):
        """Called after one physics step."""
        # since we change the bodie's rotation, make sure that it's called
        # every step so that it is deterministic and syncs correctly
        DistributedMinigamePhysicsWorld.DistributedMinigamePhysicsWorld.postStep(self)
        self.placeBodies()
        self.totalPhysicsSteps += 1

    def createObstacle(self, pos, obstacleIndex, cubicObstacle):
        """Create one physics obstacle. Returns a nodePath """        
        if cubicObstacle:
            return self.createCubicObstacle(pos, obstacleIndex)
        else:
            return self.createCircularObstacle(pos, obstacleIndex)

    def createCircularObstacle(self, pos, obstacleIndex):
        """Create one physics obstacle. Returns a nodePath"""
        self.notify.debug("create obstacleindex %s" % (obstacleIndex))
        
        geom = OdeSphereGeom(self.space, IceGameGlobals.TireRadius)
        geom.setCollideBits( self.allTiresMask)   # we only collide against tires
        geom.setCategoryBits( self.obstacleMask)
        self.space.setCollideId(geom, self.obstacleCollideId)
 
        #tireModel = loader.loadModel('phase_3/models/misc/sphere')
        tireModel = loader.loadModel("phase_4/models/minigames/ice_game_tirestack")
        
        # assuming it has a radius of 1
        tireHeight = 1
        #tireModel.setScale(IceGameGlobals.TireRadius, IceGameGlobals.TireRadius,  IceGameGlobals.TireRadius)
        #tireModel.setZ( 0 - IceGameGlobals.TireRadius + (tireHeight /2.0))
        #tireModel.setZ(IceGameGlobals.TireRadius)
        tireModel.setPos(pos)
        #tireModel.setColor(0.5,0.5,0.5)
        tireModel.reparentTo(render)
        geom.setPosition(tireModel.getPos())

        # the real assets are set at Z zero
        tireModel.setZ(0)
        return tireModel

    def createCubicObstacle(self, pos, obstacleIndex):
        """Create one physics obstacle. Returns a nodePath"""
        self.notify.debug("create obstacleindex %s" % (obstacleIndex))
        sideLength = IceGameGlobals.TireRadius *2
        geom = OdeBoxGeom(self.space, sideLength, sideLength, sideLength)
        geom.setCollideBits( self.allTiresMask)   # we only collide against tires
        geom.setCategoryBits( self.obstacleMask)
        self.space.setCollideId(geom, self.obstacleCollideId)
 
        #tireModel = render.attachNewNode('cubicObstacle-%d'% obstacleIndex)
        #BuildGeometry.addBoxGeom(tireModel, sideLength, sideLength, sideLength)
        #tireModel.setPos(pos)
        #tireModel.setColor(0.5,0.5,0.5)

        tireModel = loader.loadModel("phase_4/models/minigames/ice_game_crate")
        tireModel.setPos(pos)
        tireModel.reparentTo(render)

        geom.setPosition(tireModel.getPos())

        # the real assets are set at Z zero
        tireModel.setZ(0)        
        return tireModel

        
        
