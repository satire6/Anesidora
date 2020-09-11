from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *
from math import *
import math
from direct.fsm.FSM import FSM
from toontown.minigame import ArrowKeys
from direct.showbase import PythonUtil
from direct.task import Task
from direct.distributed.ClockDelta import *
import BuildGeometry
from toontown.golf import GolfGlobals
import random, time

def scalp (vec, scal):
    vec0 = vec[0] * scal
    vec1 = vec[1] * scal
    vec2 = vec[2] * scal
    vec = Vec3(vec0, vec1, vec2)

def length (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

class DistributedPhysicsWorldBase:

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhysicsWorld")    

    def __init__(self, canRender = 1):
        self.canRender = canRender
        
        #universal ODE stuff
        self.world = OdeWorld()
        self.space = OdeSimpleSpace()
        self.contactgroup = OdeJointGroup()
        
        # Items needed to render
        self.bodyList = [] # list of ODE bodies, or ode panda pairs if canRender
        
        self.showContacts = 0
        self.jointMarkers = []
        self.jointMarkerCount = 64
        
        
        #items used to keep track on placement between ode and panda
        if self.canRender:
            self.odePandaRelationList = self.bodyList
            self.root = render.attachNewNode("physics root node")
            self.worldAttach = render.attachNewNode("physics geom attach point")
        else:
            self.root = NodePath("physics root node")
            
        self.placerNode = self.root.attachNewNode("Placer")
        self.subPlacerNode = self.placerNode.attachNewNode("Placer Sub Node")
        
        #movable enviromnmental objects that need to be syncronized 
        self.commonObjectDict = {}
        self.commonId = 0
        
        self.worldAttach = self.root.attachNewNode("physics geom attach point")

        self.timingCycleLength = 10.0
        self.timingCycleOffset = 0.0
        
        self.timingSimTime = 0.0
        self.DTAStep = 1.0 / 60.0
        
    def delete(self):
        self.stopSim()
        
        for index in commonObjectDict:
            entry = commonObjectDict[index]
            entry[2].destroy()
            if len(entry) > 3:
                entry[3].destroy()
        
        if self.canRender:
            for pair in self.odePandaRelationList:
                pair[0].remove()
                pair[1].destroy()
            del self.odePandaRelationList
        else:
            for body in self.bodyList:
                body[1].destroy()
            del self.bodyList
        
        self.placerNode.remove()
        self.root.remove()
        
        for marker in self.jointMarkers:
            marker.remove()
        del self.jointMarkers
        
        self.world.destroy()
        self.space.destroy()
        self.world = None
        self.space = None
        
        
    def setupSimulation(self):
        self.world.setAutoDisableFlag(0)
        self.world.setAutoDisableLinearThreshold(0.15)
        self.world.setAutoDisableAngularThreshold(0.15)
        self.world.setAutoDisableSteps(2)
        self.world.setGravity(0,0,-32.174)
        self.world.setErp(0.8)
        self.world.setCfm(1E-5)
        self.world.initSurfaceTable(3)
        
        self.world.setSurfaceEntry(0,0, 150, 0.15, 0.1, 0.9, 0.00001, 0.0, 0.40)
        self.world.setSurfaceEntry(1,1, 5000, 0.15, 0.1, 0.9, 0.00001, 0.0, 1.00)
        self.world.setSurfaceEntry(2,2, 150, 0.15, 0.1, 0.9, 0.00001, 0.0, 0.40)
        self.world.setSurfaceEntry(0,2, 150, 0.15, 0.1, 0.9, 0.00001, 0.0, 0.40)        
        # grass is 0, ball is 1,  ball hitting grass
        self.world.setSurfaceEntry( pos1 = 0, pos2 = 1,
                                    mu = 5000,
                                    bounce = 0.15,
                                    bounce_vel = 0.1,
                                    soft_erp = 0.9,
                                    soft_cfm = 0.00001,
                                    slip = 0.0,
                                    dampen = 0.35)
        
        # barrier is 2, ball is 1, ball hitting hard barrier
        self.world.setSurfaceEntry( pos1 = 2, pos2 = 1,
                                    mu = 5000,
                                    bounce = 0.90,
                                    bounce_vel = 0.1,
                                    soft_erp = 0,
                                    soft_cfm = 0,
                                    slip = 0.0,
                                    dampen = 0.01)        

        # Create a plane geom which prevent the objects from falling forever
        floor = OdePlaneGeom(self.space, Vec4(0.0,0.0,1.0,-12.0))
        floor.setCollideBits(BitMask32(0x00000000))
        floor.setCategoryBits(BitMask32(0x00000f00))
        
        self.space.setAutoCollideWorld(self.world)
        self.space.setAutoCollideJointGroup(self.contactgroup)
        self.world.setQuickStepNumIterations(8)
        self.DTA = 0.0
        
        self.frameCounter = 0
        
        if self.canRender:
            for count in range(self.jointMarkerCount):
                testMarker = render.attachNewNode("Joint Marker")
                ballmodel = loader.loadModel('models/misc/sphere')
                ballmodel.reparentTo(testMarker)
                ballmodel.setScale(0.1)
                testMarker.setPos(0.0,0.0,-100.0)
                self.jointMarkers.append(testMarker)
        
    def setTimingCycleLength(self, time):
        self.timingCycleLength = time
        
    def getTimingCycleLength(self):
        return self.timingCycleLength
        
    def getCycleTime(self):
        cycleTime = (globalClock.getRealTime() + self.timingCycleOffset) % self.timingCycleLength
        return cycleTime
        
    def setTimeIntoCycle(self, time):
        trueCycleTime = globalClock.getRealTime() % self.timingCycleLength
        self.timingCycleOffset = time - trueCycleTime
        
    def getSimCycleTime(self):
        return self.timingSimTime % self.timingCycleLength
        
    def startSim(self):
        taskMgr.add(self.__simulationTask, "simulation task")
        
    def stopSim(self):
        taskMgr.remove("simulation task")
        
    def __simulationTask(self, task):
        #dt = globalClock.getDt()
        self.DTA += globalClock.getDt()
        self.frameCounter += 1
        if self.frameCounter >= 10:
            self.frameCounter = 0
        
        startTime = globalClock.getRealTime()
    
                
        #self.space.collide((self.odeWorld,self.contactgroup), near_callback)
        colCount = 0
        # Simulation step
        #self.odeWorld.step(dt)
        while self.DTA >= self.DTAStep:
            self.DTA -= self.DTAStep
            self.preStep()
            self.simulate()
            self.postStep()
                    
        if self.canRender:
            self.placeBodies()   
            
        if self.frameCounter == 0:
            endTime = globalClock.getRealTime() - startTime
            #self.notify.debug ("physics Time = %s collision joints %s" % (endTime, colCount))
        
        return task.cont
        
    def simulate(self):
        self.colCount = self.space.autoCollide() # Detect collisions and create contact joints
        self.world.quickStep(self.DTAStep) # Simulate
        
        for bodyPair in self.bodyList:
            self.world.applyDampening(self.DTAStep, bodyPair[1])
        
        self.contactgroup.empty() # Remove all contact joints
        self.commonObjectControl()
        self.timingSimTime = self.timingSimTime + self.DTAStep
        
    def placeBodies(self):
        for pair in self.odePandaRelationList:
            pandaNodePathGeom = pair[0]
            odeBody = pair[1]
            pandaNodePathGeom.setPos(odeBody.getPosition())
            rotation = (odeBody.getRotation() * (180.0/math.pi))
            pandaNodePathGeom.setQuat(Quat(odeBody.getQuaternion()[0],odeBody.getQuaternion()[1],odeBody.getQuaternion()[2],odeBody.getQuaternion()[3]))
            
        
    def preStep(self):
        print "Base class prestep"
        pass
        
    def postStep(self):
        # mark the contact joints
        if self.showContacts and canRender:
            for count in range(self.jointMarkerCount):
                pandaNodePathGeom = self.jointMarkers[count]
                if count < self.colCount:
                    pandaNodePathGeom.setPos(self.space.getContactData((count *3) + 0), self.space.getContactData((count *3) + 1), self.space.getContactData((count *3) + 2))
                else:
                    pandaNodePathGeom.setPos(0.0,0.0,-100.0)
                    
    def commonObjectControl(self):
        time = self.getSimCycleTime()
        for key in self.commonObjectDict:
            entry = self.commonObjectDict[key]
            if entry[1] in [2, 4]:
                motor = entry[3]
                timeData = entry[4]
                forceData = entry[5]
                force = 0.0
                for index in range(len(timeData)):
                    if timeData[index] < time:
                        force = forceData[index]
                motor.setParamVel(force)
        

    def getCommonObjectData(self):
        #print("updateCommonObjects")
        objectStream = []
        for key in self.commonObjectDict:
            objectPair = self.commonObjectDict[key]
            object = objectPair[2]
            pos3 = object.getPosition()
            quat4 = object.getQuaternion()
            anV3 = object.getAngularVel()
            lnV3 = object.getLinearVel()
            
            data = ( objectPair[0], objectPair[1],
                    pos3[0], pos3[1], pos3[2],
                    quat4[0], quat4[1], quat4[2], quat4[3],
                    anV3[0], anV3[1], anV3[2],
                    lnV3[0], lnV3[1], lnV3[2]
                    )
            objectStream.append(data)
        if objectStream == []:
            #print("updateCommonObjects - Empty")
            data = ( 0, 99,
                    0, 0, 0,
                    0, 0, 0, 0,
                    0, 0, 0,
                    0, 0, 0
                    )
            objectStream.append(data)
            
        return objectStream
        
    def useCommonObjectData(self, objectData, enable = 1):
        if objectData[0][1] == 99:
            return
        for data in objectData:
            commonObject = self.commonObjectDict[data[0]]
            commonObject[2].setPosition(data[2], data[3], data[4])
            commonObject[2].setQuaternion(Quat(data[5], data[6], data[7], data[8]))
            commonObject[2].setAngularVel(data[9], data[10], data[11])
            commonObject[2].setLinearVel(data[12], data[13], data[14])
            if enable:
                commonObject[2].enable()
            else:
                commonObject[2].disable()
            
            
    def createCommonObject(self, type, commonId, pos, hpr, sizeX = 0 , sizeY = 0, moveDistance = 0):
        # an Id of None means it's a new object and it probably being created on the AI
        if commonId == None:
            commonId = self.commonId
            self.commonId += 1
            
        vPos = Point3(float(pos[0]), float(pos[1]), float(pos[2]))
        vHpr = Vec3(float(hpr[0]), float(hpr[1]), float(hpr[2]))
        rHpr = Vec3(float(hpr[0]), float(hpr[1]), float(hpr[2]))
        
        self.placerNode.setHpr(vHpr)
        self.placerNode.setPos(vPos)
        
        if type == 0: # create Box
            model, box = self.createBox(self.world, self.space, 10.0, 5.0, 5.0, 5.0)
            box.setPosition(vPos)
            self.placerNode.setHpr(vHpr)
            box.setQuaternion(self.placerNode.getQuat())
            self.commonObjectDict[commonId] = (commonId, type, box)
            
        elif type == 1: #rotating cross
            model, cross = self.createCross(self.world, self.space, 1.0, 3.0, 12.0, 2.0, 2)
            motor = OdeHingeJoint(self.world)
            cross.setPosition(vPos)
            cross.setQuaternion(self.placerNode.getQuat())
            ourAxis = render.getRelativeVector(self.placerNode, Vec3(0,0,1))
            motor.setParamVel(1.5)
            motor.setParamFMax(500000000.0)            
            boxsize = Vec3(1.0, 1.0, 1.0)
            motor.attach(0, cross)
            motor.setAnchor(vPos)
            motor.setAxis(ourAxis)
            self.cross = cross
            cross.enable()
            self.commonObjectDict[commonId] = (commonId, type, cross)            

            
        elif type == 2: #timed sliding gate
            ourAxis = render.getRelativeVector(self.placerNode, Vec3(0,0,1))
            model, box = self.createBox(self.world, self.space, 10.0, 5.0, 5.0, 5.0, 2)
            box.setPosition(vPos)
            box.setQuaternion(self.placerNode.getQuat())
            motor = OdeSliderJoint(self.world)
            motor.attach(box, 0)
            motor.setAxis(ourAxis)
            motor.setParamVel(3.0)
            motor.setParamFMax(5000000.0)  
            motor.setParamHiStop(10.0)
            motor.setParamLoStop(-10.0)
            #base.s = motor
            #(time, )
            timeData = (0.0, 5.0)
            forceData = (3.0, -3.0)
            
            self.commonObjectDict[commonId] = (commonId, type, box, motor, timeData, forceData)
            
        elif type == 3: #Windmill
            
            vPos = Point3(float(pos[0]), float(pos[1]), float(pos[2]))
            vHpr = Vec3(float(hpr[0]), float(hpr[1]), float(hpr[2]))
            self.placerNode.setHpr(vHpr)
            self.placerNode.setPos(vPos)
            self.subPlacerNode.setPos(0,0,0)
        
            
            if self.canRender:
                myModel = loader.loadModel('phase_6/models/golf/windmill')
            else:
                myModel = loader.loadModel('phase_6/models/golf/windmill.bam')
            
            myModel.reparentTo(self.root)
            myModel.setPos(vPos)
            myModel.setHpr(vHpr)
            #import pdb; pdb.set_trace()

            millFan = myModel.find("**/windmillFan0")
            millBase = myModel.find("**/windmillBase0")

            self.windmillFanNodePath = millFan
            self.windmillBaseNodePath = millBase
            
            millData = OdeTriMeshData (millBase)
            millGeom = OdeTriMeshGeom(self.space, millData)
            millGeom.setPosition(self.subPlacerNode.getPos(self.root))
            millGeom.setQuaternion(self.subPlacerNode.getQuat())
            self.space.setCollideId(millGeom, 8) # GolfGlobals.WINDMILL_BASE_COLLIDE_ID
            
            #if not self.canRender:
            #    myModel.remove()
            
            vPos = Point3(float(pos[0]), float(pos[1]), float(pos[2]) + 5)
            vHpr = Vec3(float(hpr[0]), float(hpr[1] + 90), float(hpr[2]) - 90)
            
            self.placerNode.setHpr(vHpr)
            self.placerNode.setPos(vPos)            
            self.subPlacerNode.setPos(0,0,2.5)
            

            
            model, cross = self.createPinWheel(self.world, self.space, 10.0, 0.8, 10.0, 0.6, 0.35, 2, millFan, (0,0,90), (-4.8,0,-2.25))
            motor = OdeHingeJoint(self.world)
            cross.setPosition(self.subPlacerNode.getPos(self.root))
            cross.setQuaternion(self.placerNode.getQuat())
            ourAxis = self.root.getRelativeVector(self.subPlacerNode, Vec3(0,0,1))
            motor.setParamVel(1.5)
            #motor.setParamVel(0)
            motor.setParamFMax(50000.0)            
            boxsize = Vec3(1.0, 1.0, 1.0)
            motor.attach(0, cross)
            motor.setAnchor(self.subPlacerNode.getPos(self.root))
            motor.setAxis(ourAxis)
            self.cross = cross
            cross.enable()
            self.commonObjectDict[commonId] = (commonId, type, cross)
            
        elif type == 4: #moving block
            ourAxis = self.root.getRelativeVector(self.placerNode, Vec3(0,1,0))
            model, box = self.createBox(self.world, self.space, 10.0, sizeX, sizeY, 1.0, 2)
            box.setPosition(vPos)
            box.setQuaternion(self.placerNode.getQuat())
            motor = OdeSliderJoint(self.world)
            motor.attach(box, 0)
            motor.setAxis(ourAxis)
            motor.setParamVel(moveDistance/4.0)
            motor.setParamFMax(5000.0)  
            motor.setParamHiStop(moveDistance)
            motor.setParamLoStop(0)
            #base.s = motor
            #(time, )
            timeData = (0.0, 5.0)
            forceData = (moveDistance/4.0, -moveDistance/4.0)
            print ("Move Distance %s" % (moveDistance))
            
            self.commonObjectDict[commonId] = (commonId, type, box, motor, timeData, forceData)
            
        #needed to send the common object over the wire
        return ([type, commonId, (pos[0], pos[1], pos[2]), (hpr[0], hpr[1], hpr[2]), sizeX, sizeY, moveDistance])

        
        
        
    def createSphere(self, world, space, density, radius, ballIndex = None):
        # Create two bodies
        self.notify.debug("create sphere index %s" % (ballIndex))
        body = OdeBody(world)
        M = OdeMass()
        M.setSphere(density, radius)
        body.setMass(M)
        body.setPosition(0,0,-100)
        
        
        geom = OdeSphereGeom(space, radius)
        self.space.setSurfaceType(geom, 1) # GolfGlobals.BALL_SURFACE
        print (("collide ID is %s") % (self.space.setCollideId(geom, 42))) # GolfGlobals.BALL_COLLIDE_ID
        self.space.getCollideId(geom)
        geom2 = OdeSphereGeom(space, radius)

        
        if ballIndex == 1:
            self.notify.debug("1")
            geom.setCollideBits(BitMask32(0x00ffffff))
            geom.setCategoryBits(BitMask32(0xff000000))
        elif ballIndex == 2:
            self.notify.debug("2")
            geom.setCollideBits(BitMask32(0x00ffffff))
            geom.setCategoryBits(BitMask32(0xff000000))
        elif ballIndex == 3:
            self.notify.debug("3")
            geom.setCollideBits(BitMask32(0x00ffffff))
            geom.setCategoryBits(BitMask32(0xff000000))
        elif ballIndex == 4:
            self.notify.debug("4")
            geom.setCollideBits(BitMask32(0x00ffffff))
            geom.setCategoryBits(BitMask32(0xff000000))
        else:
            geom.setCollideBits(BitMask32(0xffffffff))
            geom.setCategoryBits(BitMask32(0xffffffff))
            
        geom.setBody(body)

        if self.notify.getDebug():
            self.notify.debug('golf ball geom id')
            geom.write()
            self.notify.debug(' -')            

        self.notify.debug("Collide Bits %s" % (geom.getCollideBits()))
        
        if self.canRender:
            testball = render.attachNewNode("Ball Holder")
            ballmodel = loader.loadModel('phase_6/models/golf/golf_ball')
            ballmodel.reparentTo(testball)
            ballmodel.setColor(GolfGlobals.PlayerColors[ballIndex-1])
            testball.setPos(0,0,-100)
            self.odePandaRelationList.append((testball, body))
        else:
            testball = None
            self.bodyList.append((None, body))
        return testball, body

        
        
    def createBox(self, world, space, density, lx, ly, lz, colOnlyBall = 0):
        """Create a box body and its corresponding geom."""
        # Create body
        body = OdeBody(self.world)
        M = OdeMass()
        #M.setBox(density, lx, ly, lz)
        M.setSphere(density, 0.3 * (lx + ly + lz))
        body.setMass(M)
        boxsize = Vec3(lx, ly, lz)
        geom = OdeBoxGeom(space, boxsize)
        geom.setBody(body)
        self.space.setSurfaceType(geom, 0)
        self.space.setCollideId(geom, 7) # GolfGlobals.MOVER_COLLIDE_ID
        
        if colOnlyBall:
                geom.setCollideBits(BitMask32(0x0f000000))
                geom.setCategoryBits(BitMask32(0x00000000))
        elif colOnlyBall == 2:
                geom.setCollideBits(BitMask32(0x00000000))
                geom.setCategoryBits(BitMask32(0x00000000))
                
        if self.canRender:
            # Create a box geom for collision detection
            color = random.choice([Vec4(1.0,0.0,0.5,1.0), Vec4(0.5,0.5,1.0,1.0), Vec4(0.5,1.0,0.5,1.0)])
            boxsize = Vec3(lx, ly, lz)
            boxNodePathGeom, t1, t2 = BuildGeometry.addBoxGeom(self.worldAttach, lx, ly, lz, color, 1)
            boxNodePathGeom.setPos(0,0,-100)
            self.odePandaRelationList.append((boxNodePathGeom, body))
        else:
            boxNodePathGeom = None
            self.bodyList.append((None, body))
            
        return boxNodePathGeom, body
        
    def createCross(self, world, space, density, lx, ly, lz, colOnlyBall = 0, attachedGeo = None, aHPR = None, aPos = None):
        """Create a box body and its corresponding geom."""
        # Create body
        body = OdeBody(self.world)
        M = OdeMass()
        M.setBox(density, lx, ly, lz)
        body.setMass(M)
        body.setFiniteRotationMode(1)

        # Set parameters for drawing the body
        #body.shape = "box"
        boxsize = Vec3(lx, ly, lz)
        boxsize2 = Vec3(ly, lx, lz)
        

        # Create a box geom for collision detection
        geom = OdeBoxGeom(space, boxsize)
        geom.setBody(body)
        self.space.setSurfaceType(geom, 0)
        self.space.setCollideId(geom, 13)
        
        geom2 = OdeBoxGeom(space, boxsize2)
        geom2.setBody(body)
        self.space.setSurfaceType(geom2, 0)
        self.space.setCollideId(geom2, 26)

        self.odePandaRelationList.append((boxNodePathGeom, body))
        
        if colOnlyBall == 1:
                geom.setCollideBits(BitMask32(0x0f000000))
                geom.setCategoryBits(BitMask32(0x00000000))
                geom2.setCollideBits(BitMask32(0x0f000000))
                geom2.setCategoryBits(BitMask32(0x00000000))
        elif colOnlyBall == 2:
                geom.setCollideBits(BitMask32(0x00000000))
                geom.setCategoryBits(BitMask32(0x00000000))
                geom2.setCollideBits(BitMask32(0x00000000))
                geom2.setCategoryBits(BitMask32(0x00000000))
        
        if self.canRender:
            boxNodePathGeom, t1, t2 = BuildGeometry.addBoxGeom(self.worldAttach, lx, ly, lz, Vec4(1.0,1.0,1.0,1.0), 1)
            boxNodePathGeom.setPos(0,0,-100)
            
            boxNodePathGeom2, t1, t2 = BuildGeometry.addBoxGeom(boxNodePathGeom, ly, lx, lz, Vec4(1.0,1.0,1.0,1.0), 1)
            boxNodePathGeom2.setPos(0,0,0)
            
            if attachedGeo:
                attachedGeo.reparentTo(boxNodePathGeom)
                attachedGeo.setHpr(0,0,90)
                attachedGeo.setPos(-4.8,0,-2.0)

            self.odePandaRelationList.append((boxNodePathGeom, body))
        else:
            boxNodePathGeom = None
            self.bodyList.append((None, body))
            
        return boxNodePathGeom, body
        
    def createPinWheel(self, world, space, density, lx, ly, lz, latSlide, colOnlyBall = 0, attachedGeo = None, aHPR = None, aPos = None):
        """Create a box body and its corresponding geom."""
        
        
        # Create body
        #latSlide = 0.35
        body = OdeBody(self.world)
        M = OdeMass()
        M.setBox(density, lx, ly, lz)
        body.setMass(M)
        body.setFiniteRotationMode(1)
        #import pdb; pdb.set_trace()
        
        # Set parameters for drawing the body
        #body.shape = "box"
        boxsize = Vec3(lx, ly * 0.5, lz)
        boxsize2 = Vec3(ly * 0.5, lx, lz)
        
        
        # Create a box geom for collision detection
        geom = OdeBoxGeom(space, boxsize)
        geom.setBody(body)
        geom.setOffsetPosition(-latSlide,ly * 0.25,0)
        self.space.setSurfaceType(geom, 0)
        self.space.setCollideId(geom, 13)
        
        geom2 = OdeBoxGeom(space, boxsize2)
        geom2.setBody(body)
        geom2.setOffsetPosition(ly * 0.25,latSlide ,0)
        self.space.setSurfaceType(geom2, 0)
        self.space.setCollideId(geom2, 13)
        
        geom3 = OdeBoxGeom(space, boxsize)
        geom3.setBody(body)
        geom3.setOffsetPosition(latSlide,-ly * 0.25,0)
        self.space.setSurfaceType(geom3, 0)
        self.space.setCollideId(geom3, 13)
        
        geom4 = OdeBoxGeom(space, boxsize2)
        geom4.setBody(body)
        geom4.setOffsetPosition(-ly * 0.25,-latSlide,0)
        self.space.setSurfaceType(geom4, 0)
        self.space.setCollideId(geom4, 13)
        
        
        if colOnlyBall == 1:
                geom.setCollideBits(BitMask32(0x0f000000))
                geom.setCategoryBits(BitMask32(0x00000000))
                geom2.setCollideBits(BitMask32(0x0f000000))
                geom2.setCategoryBits(BitMask32(0x00000000))
                geom3.setCollideBits(BitMask32(0x0f000000))
                geom3.setCategoryBits(BitMask32(0x00000000))
                geom4.setCollideBits(BitMask32(0x0f000000))
                geom4.setCategoryBits(BitMask32(0x00000000))
        elif colOnlyBall == 2:
                geom.setCollideBits(BitMask32(0x00000000))
                geom.setCategoryBits(BitMask32(0x00000000))
                geom2.setCollideBits(BitMask32(0x00000000))
                geom2.setCategoryBits(BitMask32(0x00000000))
                geom3.setCollideBits(BitMask32(0x00000000))
                geom3.setCategoryBits(BitMask32(0x00000000))
                geom4.setCollideBits(BitMask32(0x00000000))
                geom4.setCategoryBits(BitMask32(0x00000000))
        
        if self.canRender:
            someNodePathGeom = render.attachNewNode("pinwheel")
            if attachedGeo:
                attachedGeo.reparentTo(someNodePathGeom)
                attachedGeo.setHpr(aHPR[0], aHPR[1], aHPR[2])
                attachedGeo.setPos(aPos[0], aPos[1], aPos[2])
        
            else:
                boxNodePathGeom, t1, t2 = BuildGeometry.addBoxGeom(someNodePathGeom, lx, ly * 0.5, lz, Vec4(1.0,1.0,1.0,1.0), 1)
                boxNodePathGeom.setPos(-latSlide,ly * 0.25,0)
                
                boxNodePathGeom2, t1, t2 = BuildGeometry.addBoxGeom(someNodePathGeom, ly * 0.5, lx, lz, Vec4(1.0,1.0,1.0,1.0), 1)
                boxNodePathGeom2.setPos(ly * 0.25,latSlide ,0)
                
                boxNodePathGeom3, t1, t2 = BuildGeometry.addBoxGeom(someNodePathGeom, lx, ly * 0.5, lz, Vec4(1.0,1.0,1.0,1.0), 1)
                boxNodePathGeom3.setPos(latSlide,-ly * 0.25,0)
                
                boxNodePathGeom4, t1, t2 = BuildGeometry.addBoxGeom(someNodePathGeom, ly * 0.5, lx, lz, Vec4(1.0,1.0,1.0,1.0), 1)
                boxNodePathGeom4.setPos(-ly * 0.25,-latSlide,0)

            self.odePandaRelationList.append((someNodePathGeom, body))
        else:
            someNodePathGeom = None
            self.bodyList.append((None, body))
            
        return someNodePathGeom, body


    def attachMarker(self, body):
        if self.canRender:
            testMarker = render.attachNewNode("Joint Marker")
            ballmodel = loader.loadModel('models/misc/sphere')
            ballmodel.reparentTo(testMarker)
            ballmodel.setScale(0.25)
            testMarker.setPos(0.0,0.0,-100.0)
            self.odePandaRelationList.append((testMarker, body))

 