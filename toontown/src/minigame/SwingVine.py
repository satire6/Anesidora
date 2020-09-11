from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedObject
from direct.showutil import Rope
import math
from toontown.toonbase import ToontownGlobals
import VineGameGlobals
import VineSpider

class SwingVine(NodePath.NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('SwingVine')

    defaultNormal = Vec3(1,0,0)
    SwingAnimPeriod = 6.0

    SmallAnimAngle = 10
    NonMovingAnimAngle = 2

    SwingAnimFull =0
    SwingAnimSmall = 1
    SwingAnimMinimal = 2

    MaxNumberOfFramesInSwingAnim = 144    
    
    def __init__(self, vineIndex, x,y, z, length=20, baseAngle=40, period=4, spiderPeriod = 0 ):
        NodePath.__init__(self,'SwingVine')
        self.cableLength = length
        self.numLinks = 3        
        self.links = []
        self.vineIndex = vineIndex
        self.spider = None
        self.spiderPeriod = spiderPeriod
        self.hasSpider = not (spiderPeriod == 0) 

        self.numTubes = self.numLinks * 3
        self.tubeLength = float(self.cableLength) / self.numTubes
        self.tubeLength *= 1.25
        self.tIncrement = 1.0 / self.numTubes
        self.tHalfIncrement = self.tIncrement / 2.0

        self.baseAngle = baseAngle
        self.maxSwingAngle = deg2Rad(-90 + baseAngle)
        self.minSwingAngle = deg2Rad(-90 - baseAngle)
        self.period = period # how many secs to complete one swing cycle

        self.swingingForward = True # which direction are we swinging
        self.swingT = 0 # how far into the swing are we
        self.swingAngle = 0 # what is the current angle of our vine

        self.setPos(x, y, z)        
        self.load()

        # WARNING debug only, comment this out or else it will leak
        # base.vine = self

        # avId is key, (t, positionWrtRender, normal, toonOffset, attachNode, facingRight, swingInterval)
        self.attachedToons = {}

        self.ival=None
        self.spiderIval = None
        self.unloading = False

        self.spiderMovingDown = True

    def load(self):
        self.root = self.attachNewNode('root')
        self.topLink = self.root.attachNewNode('topLink')
        #debugAxis = loader.loadModel('models/misc/xyzAxis')
        #debugAxis.reparentTo(self.topLink)
        #debugAxis.setScale(0.1)
        
        self.setupCable()
        #self.root.setZ(30)
        self.reparentTo(render)

        self.debugTangent = None
        #self.debugTangent = loader.loadModel('models/misc/xyzAxis')
        #self.debugTangent.reparentTo(render)
        #self.debugTangent.setScale(0.05)

        nearBubble = CollisionSphere(0, 0, -self.cableLength/2.0, self.cableLength/2.0)
        nearBubble.setTangible(0)
        nearBubbleNode = CollisionNode('SwingVine')
        nearBubbleNode.setCollideMask(GeomNode.getDefaultCollideMask())
        nearBubbleNode.addSolid(nearBubble)
        #self.attachNewNode(nearBubbleNode)
        
        self.rope.setName('SwingVine-%d' % self.vineIndex)
        #self.rope.ropeNode.setName('SwingVine')

        #self.notify.debug( 'self.rope collideMask = %s' % self.rope.getCollideMask())
        #self.notify.debug( 'self.ropeNode intocollideMask = %s' % self.rope.ropeNode.getIntoCollideMask())
        self.setupTubes()

        if self.hasSpider:
            self.spider = VineSpider.VineSpider()
            self.spiderT = 0.25
        
    def unload(self):
        self.unloading = True
        if self.ival:
            self.ival.finish()
            self.ival = None
        if self.spiderIval:
            self.spiderIval.finish()
            self.spiderIval = None            
        if self.debugTangent:
            self.debugTangent.removeNode()
        for tube in self.tubes:
            tube.removeNode()
        self.tubes = []
        for tube in self.tubes2:
            tube.removeNode()
        self.tubes2 = []        
        if self.hasSpider:
            self.spider.destroy()
            del self.spider
        for toonInfo in self.attachedToons.values():
            attachNode = toonInfo[4]
            if attachNode:
                attachNode.removeNode()
            swingIval = toonInfo[6]
            if swingIval:
                swingIval.finish()
        
        self.removeNode()

            
    def setupCable(self):    
        # The list of links is built up to pass to the Rope class, to
        # make a renderable spline for the cable.
        self.links = []
        self.links.append((self.topLink, Point3(0,0,0)))

        anchor = self.topLink
        for linkNum in xrange(self.numLinks):
            anchor = self.__makeLink(anchor, linkNum)
            
        self.bottomLink = self.links[-1][0]
        self.link1 = self.links[-2][0]            
        self.rope= self.makeSpline()
        self.rope.reparentTo(self.root)

        # setup the vine texture
        myTexture = loader.loadTexture("phase_4/maps/swinging_vine.jpg")
        gameAssets = loader.loadModel("phase_4/models/minigames/vine_game")
        vine = gameAssets.find('**/vine1')
        self.cableTex = vine.findTexture("*")
        if self.cableTex:
            self.cableTex.setWrapV(Texture.WMRepeat)
            self.rope.setTexture(self.cableTex)
            ts = TextureStage.getDefault()
            #self.rope.setTexScale(ts, 0.15, 0.13)
            #self.rope.setTexOffset(ts, 0.83, 0.01)
            self.rope.setTexScale(ts, 1.0, 0.15)
            self.rope.setTransparency(1)
        if self.vineIndex == VineGameGlobals.NumVines -1:
            pass
            # TODO make the last vine different somehow
            # self.setColorScale(1.0, 0.843, 0, 1.0) # set the end vine to a diff color

        if self.cableTex:
            self.setupStaticPart(self.cableTex)
        
    def setupStaticPart(self, vineTexture):
        """Create the non moving part of the vine that goes off the top of the screen."""
        cm = CardMaker('card')
        cm.setFrame(-0.5, 0.5, -0.1, 8)
        self.staticVine = self.attachNewNode(cm.generate())
        self.staticVine.setTexture(vineTexture)
        self.setTransparency(1)

        # create static collisions for the static part
        radius = 0.5
        tubeIndex =0 # name it the same as the first tube
        colNode = CollisionNode('StaticVine-%d-%d' % (self.vineIndex, tubeIndex))
        bz = 0
        az = 58
        quad = CollisionPolygon( Point3(0.25, radius +1, bz),
                                 Point3(0.25, radius +1, az),
                                 Point3(0.25, -radius -1,az),
                                 Point3(0.25, -radius-1, bz))
        colNode.addSolid(quad)
        colNode.setCollideMask(ToontownGlobals.PieBitmask)
        colNode.setBounds(BoundingSphere( Point3(0,0,0), 10))
        self.staticVine.attachNewNode(colNode)

        colNode2 = CollisionNode('StaticVine-%d-%d' % (self.vineIndex, tubeIndex))
        quad2 = CollisionPolygon( Point3(-0.25, -radius -1, bz),
                                  Point3(-0.25, -radius -1, az),
                                  Point3(-0.25, +radius +1,az),
                                  Point3(-0.25, +radius+1, bz))
        colNode2.addSolid(quad2)
        colNode2.setCollideMask(ToontownGlobals.PieBitmask)
        colNode2.setBounds(BoundingSphere( Point3(0,0,0), 10))
        self.staticVine.attachNewNode(colNode2)
        
    def setupTubes(self):
        self.tubes = []
        self.tubes2 = []
        radius = 0.5
        for tubeIndex in xrange(self.numTubes):
            az = self.tubeLength / 2.0
            bz = - self.tubeLength / 2.0
            ct = CollisionTube(0, 0, az, 0, 0, bz, radius)
            ct.setTangible(0)
            colNode = CollisionNode('SwingVine-%d-%d' % (self.vineIndex, tubeIndex))
            
            #colNode.addSolid(ct)

            # let's try using a collisionPoly to stop a fast moving toon moving through a vine
            quad = CollisionPolygon( Point3(0.25, radius +1, bz),
                                     Point3(0.25, radius +1, az),
                                     Point3(0.25, -radius -1,az),
                                     Point3(0.25, -radius-1, bz))
            colNode.addSolid(quad)
            colNode.setCollideMask(ToontownGlobals.PieBitmask)
            # we must increase the bounding volume to make sure he doesn't pass through
            colNode.setBounds(BoundingSphere( Point3(0,0,0), 10))

            colNode2 = CollisionNode('SwingVine-%d-%d' % (self.vineIndex, tubeIndex))
            quad2 = CollisionPolygon( Point3(-0.25, -radius -1, bz),
                                      Point3(-0.25, -radius -1, az),
                                      Point3(-0.25, +radius +1,az),
                                      Point3(-0.25, +radius+1, bz))
            colNode2.addSolid(quad2)
            colNode2.setCollideMask(ToontownGlobals.PieBitmask)
            colNode2.setBounds(BoundingSphere( Point3(0,0,0), 10))

            # RAU I tried parenting the tube to self, but it made the rope disappear
            newTube = render.attachNewNode(colNode)
            self.tubes.append(newTube)
            newTube2 = render.attachNewNode(colNode2)            
            self.tubes2.append(newTube2)

        # calculate proper positions for the tubes
        self.updateTubes()

    def __makeLink(self, anchor, linkNum):
        an = ActorNode('link%s' % (linkNum))
        anp = NodePath(an)
        
        anp.reparentTo(self.root)
        z =  float(linkNum + 1) / float(self.numLinks) * self.cableLength
        #self.notify.debug('computedZ for link %d = %f' % (linkNum, z))
        anp.setPos(self.topLink.getPos())
        anp.setZ( anp.getZ() - z)

        #debugAxis = loader.loadModel('models/misc/xyzAxis')
        #debugAxis.reparentTo(anp)
        #debugAxis.setScale(0.1)

        self.links.append((anp,Point3(0,0,0)))

        return anp

    def makeSpline(self):
        # Use the Rope class to draw a spline between the joints of
        # the cable.
        
        rope = Rope.Rope()
        for i in xrange(len(self.links)):
            pass
            #self.notify.debug('%s %s' % (self.links[i][0], self.links[i][0].getPos()))
            
        rope.setup(min(len(self.links), 4), self.links)
        for i in xrange(len(self.links)):
            pass
            #self.notify.debug('%s %s' % (self.links[i][0], self.links[i][0].getPos()))        
        rope.curve.normalizeKnots()
        self.notify.debug('after normalize Knots')
        for i in xrange(len(self.links)):
            pass
            #self.notify.debug('%s %s' % (self.links[i][0], self.links[i][0].getPos()))           
            
        rn = rope.ropeNode
        #rn.setRenderMode(RopeNode.RMTube)
        rn.setRenderMode(RopeNode.RMBillboard)
        rn.setNumSlices(3)
        rn.setTubeUp(Vec3(0, -1, 0))
        #rn.setUvMode(RopeNode.UVParametric)
        rn.setUvMode(RopeNode.UVDistance )
        rn.setUvDirection(False)
        rn.setThickness(1.0)
        #rn.setThickness(5)

        return rope

    def positionLink1(self, t, angleInRadians):
        #link 1 is in the 2/3 of the way down the rope
        degAngle = rad2Deg(angleInRadians)
        diffFrom90 = degAngle - -90.0
        link1AngleDiff = diffFrom90 * 2 / 3.0
        link1AngleToUse = deg2Rad( -90 + link1AngleDiff)
        lengthToUse = self.cableLength  * 2.0 / 3.0
        link1X = math.cos(link1AngleToUse) * lengthToUse
        link1Z = math.sin(link1AngleToUse) * lengthToUse
        self.link1.setPos(link1X, 0, link1Z)    

    def swingForward(self, t):
        diffAngle = self.maxSwingAngle - self.minSwingAngle
        multiplier = t
        angleToUse = self.minSwingAngle + (multiplier * diffAngle)
        
        newX = math.cos(angleToUse) * self.cableLength
        newZ = math.sin(angleToUse) * self.cableLength
        self.bottomLink.setPos(newX, 0, newZ)

        self.positionLink1(t, angleToUse)
        oldSwingingForward = self.swingingForward
        self.swingingForward = True
        self.swingT = t
        self.swingAngle = angleToUse
        self.updateAttachedStuff()
        if not oldSwingingForward == self.swingingForward:
            self.updateSwingAnims()
        

    def swingBack(self, t):
        diffAngle = self.maxSwingAngle - self.minSwingAngle
        multiplier = t
        angleToUse = self.maxSwingAngle - (multiplier * diffAngle)

        newX = math.cos(angleToUse) * self.cableLength
        newZ = math.sin(angleToUse) * self.cableLength
        self.bottomLink.setPos(newX, 0, newZ)

        self.positionLink1(t, angleToUse)        
        oldSwingingForward = self.swingingForward
        self.swingingForward = False
        self.swingT = t
        self.swingAngle = angleToUse
        self.updateAttachedStuff()
        if not oldSwingingForward == self.swingingForward:
            self.updateSwingAnims()        

    def moveSpiderDown(self, t):
        self.spiderMovingDown = True
        self.spiderT = t

    def moveSpiderUp(self, t):
        self.spiderMovingDown = False
        self.spiderT = 1 -t
        
        
    def startSwing(self):
        forwardX = math.cos(self.maxSwingAngle) * self.cableLength
        forwardZ = math.sin(self.maxSwingAngle) * self.cableLength

        backX = math.cos(self.minSwingAngle) * self.cableLength
        backZ = math.sin(self.minSwingAngle) * self.cableLength

        self.bottomLink.setPos(backX, 0, backZ)

        self.ival = Sequence(LerpFunctionInterval(self.swingForward, duration = self.period /2.0,  blendType = "easeInOut"))
        self.ival.append(LerpFunctionInterval(self.swingBack, duration = self.period /2.0,  blendType = "easeInOut"))
        self.ival.loop()

        if self.hasSpider:
            self.spiderIval = Sequence(LerpFunctionInterval(self.moveSpiderDown,
                                                            duration = self.spiderPeriod /2.0,
                                                            blendType = "easeInOut"))
            self.spiderIval.append(LerpFunctionInterval(self.moveSpiderUp,
                                                        duration = self.spiderPeriod /2.0,
                                                        blendType = "easeInOut"))
            self.spiderIval.loop()

    def stopSwing(self):
        if self.ival:
            self.ival.pause()
        if self.hasSpider and self.spiderIval:
            self.spiderIval.pause()
        if self.hasSpider:
            self.spider.hide()

    def getAttachNode(self, toonId):
        """Return the attachNode for a toon, create one if needed."""
        retval = None
        if self.attachedToons.has_key(toonId):
            existingAttachNode = self.attachedToons[toonId][4]
            if existingAttachNode:
                retval = existingAttachNode
        else:
            retval = render.attachNewNode('vineAttachNode-%s-%s' %
                                          (self.vineIndex,toonId))
        return retval

    def calcOffset(self, toonId):
        """Calculate offset so we can make position based on his left hand, not the feet."""
        offset = Point3(0,0,0)
        toon = base.cr.doId2do.get(toonId)
        if toon:
            toon.pose('swing',86)
            leftHand = toon.find('**/leftHand')
            if not leftHand.isEmpty():
                offset = leftHand.getPos(toon)
                self.notify.debug('offset = %s' % offset)
            else:
                self.notify.warning('left hand not found for toon %d' % toonId)
        else:
            self.notify.warning('toon %d not found' % toonId)
        return offset

    def doubleCheckOffset(self, toonId):
        """In case we somehow got an offset of zero, recalculate it."""
        if self.attachedToons.has_key(toonId):
            curOffset = self.attachedToons[toonId][3]
            if curOffset == Point3.zero():
                newOffset = self.calcOffset(toonId)
                self.attachedToons[toonId][3] = newOffset
                av = base.cr.doId2do.get(toonId)
                self.notify.info('correcting wrong offset %s and changing to %s' % ( curOffset, newOffset))
                if av:
                    av.setPos(-newOffset)                

    def attachToon(self, toonId, t, facingRight, setupAnim = True):
        #av = base.cr.doId2do[toonId]
        self.notify.debug('attachToon toonId=%d vineIndex=%d' % (toonId, self.vineIndex))        
        temp = Vec3(self.defaultNormal)
        
        offset = self.calcOffset(toonId)

        attachNode = self.getAttachNode(toonId)
        if facingRight:
            attachNode.setH(-90)
        else:
            attachNode.setH(90)
        self.attachedToons[toonId] = [t,temp, Vec3(0,0,0), offset, attachNode, facingRight, None]
        av = base.cr.doId2do.get(toonId)
        if av:
            av.reparentTo(attachNode)
            if offset == Point3.zero():
                self.notify.warning('calculated offset for %d is zero' % toonId)
            av.setPos(-offset)
            if setupAnim:
                self.setupSwingAnim( toonId)
            else:
                zDownTheVine = self.getPos().getZ() - t * self.cableLength
                attachNode.setPos(self.getPos())
                attachNode.setZ(zDownTheVine)
        else:
            self.notify.warning('av %d not found' % toonId)

    def changeAttachedToonT(self, toonId, t):
        """
        the toon climbed up or down the vine
        """
        if self.attachedToons.has_key(toonId):
            oldT = self.attachedToons[toonId][0]
            self.attachedToons[toonId][0] = t
            oldSwingType = self.calcSwingAnimType(oldT)
            newSwingType = self.calcSwingAnimType(t)
            # self.notify.debug('oldT=%f newT=%f oldSwing=%d newSwing=%d' % (oldT, t, oldSwingType, newSwingType))
            if oldSwingType != newSwingType:
                self.setupSwingAnim(toonId)
        else:
            self.notify.warning('changeAttachedToonT avId %d was not in the dict' % toonId)
            self.attachToon(toonId, t, 1)

    def changeAttachedToonFacing(self, toonId, facing):
        """
        the toon climbed up or down the vine
        """
        if self.attachedToons.has_key(toonId):
            curT = self.attachedToons[toonId][0]
            self.detachToon(toonId)
            self.attachToon(toonId, curT, facing)
        else:
            self.notify.warning('changeAttachedToonFacing avId %d was not in the dict' % toonId)
            self.attachToon(toonId, VineGameGlobals.VineFellDownT, 1)


    def detachToon(self, toonId):
        assert self.notify.debugStateCall(self)
        self.notify.debug('detachToon toonId=%d vineIndex=%d' % (toonId, self.vineIndex))
        if self.attachedToons.has_key(toonId):
            self.attachedToons[toonId][4].removeNode()
            swingIval = self.attachedToons[toonId][6]
            if swingIval:
                self.notify.debug('deleting swing ival %s' % swingIval)
                #swingIval.pause()
                swingIval.finish()
                self.attachedToons[toonId][6] = None
                del swingIval
            del self.attachedToons[toonId]

    def getAttachedToonInfo(self, toonId):
        if self.attachedToons.has_key(toonId):
            return self.attachedToons[toonId]
        else:
            return None

    def getCenterTForTube(self, tubeIndex):
        retval = self.tIncrement * tubeIndex + self.tHalfIncrement
        return retval

    def updateTubes(self):
        newPoint = Vec3(0,0,0)
        curve = self.rope.ropeNode.getCurve().evaluate()
        for tubeIndex in xrange(self.numTubes):
            tube = self.tubes[tubeIndex]
            t = self.getCenterTForTube(tubeIndex)
            curve.evalPoint(t, newPoint)
            tube.setPos(newPoint)

            tangent = Vec3(0,0,0)
            curve.evalTangent(t, tangent)
            tangent.normalize()

            theta = math.atan2( tangent.getZ(), tangent.getX())
            degrees = rad2Deg(theta)
            rAngle = -90 - degrees
            tube.setR(rAngle)

        for tubeIndex in xrange(self.numTubes):
            tube = self.tubes2[tubeIndex]
            t = self.getCenterTForTube(tubeIndex)
            curve.evalPoint(t, newPoint)
            tube.setPos(newPoint)

            tangent = Vec3(0,0,0)
            curve.evalTangent(t, tangent)
            tangent.normalize()

            theta = math.atan2( tangent.getZ(), tangent.getX())
            degrees = rad2Deg(theta)
            rAngle = -90 - degrees
            tube.setR(rAngle)
            
    def updateSpiders(self):
        curve = self.rope.ropeNode.getCurve().evaluate()
            
        if self.hasSpider:
            t = self.spiderT
            newPoint = Vec3(0,0,0)
            curve.evalPoint(t, newPoint)
            newPoint.setY(-0.5)
            self.spider.setPos(newPoint)
            # make the spider follow the vine
            tangent = Vec3(0,0,0)
            curve.evalTangent(t, tangent)
            theta = math.atan2( tangent.getZ(), tangent.getX())            
            degrees = rad2Deg(theta)
            #self.notify.debug('spider degrees = %f' % degrees)
            pAngle = degrees + 90
            pAngle = -pAngle
            if self.spiderMovingDown:
                self.spider.setR(pAngle)
            else:
                #import pdb; pdb.set_trace()
                self.spider.setR(pAngle-180)

    def updateAttachedStuff(self):
        self.updateTubes()
        self.updateSpiders()
        self.updateAttachedToons()

    def updateAttachedToons(self):
        curve = self.rope.ropeNode.getCurve().evaluate()            
        for avId in self.attachedToons.keys():
            self.doubleCheckOffset(avId)
            t = self.attachedToons[avId][0]
            newPoint = Vec3(0,0,0)
            curve.evalPoint(t, newPoint)
            # av = base.cr.doId2do.get(avId)

            attachNode = self.attachedToons[avId][4]
            attachNode.setPos(newPoint)

            tangent = Vec3(0,0,0)
            curve.evalTangent(t, tangent)
            tangent.normalize()
            #self.notify.debug('tangent = %s' % tangent)            

            unitY = Vec3(0,1,0)
            normal = tangent.cross(unitY)
            #self.notify.debug('normal = %s' % normal)

            theta = math.atan2( tangent.getZ(), tangent.getX())
            degrees = rad2Deg(theta)
            pAngle = degrees + 90
            #lets tone the toon swing down a little
            pAngle *= 0.5

            facingRight = self.attachedToons[avId][5]
            if facingRight:
                #attachNode.setP(pAngle)
                pass
            else:
                #attachNode.setP(-pAngle)
                pass


            if self.debugTangent:
                self.debugTangent.setPos( newPoint + normal)
            self.attachedToons[avId][1] = newPoint
            self.attachedToons[avId][2] = normal

    def getAngularVelocity(self):
        return deg2Rad(self.baseAngle) / self.period / 4.0

    def getLinearSpeed(self, t):
        # simplified version, assumes a circle, it's close enough
        retval = self.getAngularVelocity() * self.cableLength * t
        return retval

    def calcTFromTubeHit(self, colEntry):
        name = colEntry.getIntoNodePath().getName()
        parts = name.split('-')
        if len(parts) < 3:
            return
        tubeIndex = int(parts[2])
        if tubeIndex < 0 or tubeIndex >= len(self.tubes):
            return

        if parts[0] == 'StaticVine':
            # if we hit the static vine always return 0
            retval = 0
        else:
            #import pdb; pdb.set_trace()
            curve = self.rope.ropeNode.getCurve().evaluate()        
            tangent = Vec3(0,0,0)
            centerT = self.getCenterTForTube( tubeIndex)        
            curve.evalTangent(centerT, tangent)
            tangent.normalize()
            #self.notify.debug('tangent = %s' % tangent)

            endPos = colEntry.getSurfacePoint(render)
            #self.notify.debug('endPos = %s' % endPos)
            tubePos = self.tubes[tubeIndex].getPos()
            #self.notify.debug('tubePos = %s' % tubePos)
            vector = endPos - tubePos
            #self.notify.debug('vector = %s' % vector)
            #vector.normalize()
            #self.notify.debug('normalized vector = %s' % vector)        

            projection = vector.dot(tangent)
            self.notify.debug('projection = %s' % projection)
            # we know tangent has length 1, so no need to divide by that


            diffT = projection / self.tubeLength / 2.0

            #self.notify.debug('diffT = %s' % diffT)

            retval = centerT + diffT

            # P = P1 + u(P2-P1)
            P1 = tubePos
            P2 = tubePos + tangent
            P3 = endPos
            u = (P3.getX() - P1.getX()) * (P2.getX() - P1.getX()) +  (P3.getZ() - P1.getZ()) * (P2.getZ() - P1.getZ())
            # skipping the part where u = u / (distance p2 - p1) squared
            self.notify.debug('u=%s' % u)

            x = P1.getX() + u*(P2.getX() - P1.getX())
            z = P1.getZ() + u*(P2.getZ() - P1.getZ())

            perpPoint = Vec3(x, 0, z)
            distanceVector = perpPoint - tubePos
            distance = distanceVector.length()
            diffT = distance / self.cableLength

            retval = centerT + diffT

        if retval > 1:
            retval = 1
        if retval < 0:
            retval = 0

        self.notify.debug('retval = %s' % retval)
        return retval

    def setupSwingAnimFull(self, av, avId):
        """Use the full swing animation on a toon."""
        toonT = self.attachedToons[avId][0]
                
        playRate = ( self.SwingAnimPeriod /self.period)
        #playRate = 1.0
        swingInterval = Sequence()
        duration = (1 - self.swingT) * self.period / 2.0
        if duration < 0.001:
            duration = 0.001        
        # add a fudge
        # duration += 0.1
        #self.notify.debug('swing animDuration=%f' % duration)
        facingRight = self.attachedToons[avId][5]
        if (self.swingingForward and facingRight) or \
           (not self.swingingForward and not facingRight):
            # the anim cycle starts with the vine straight down, swinging right
            maxLeftFrame = 108
            downFrame1 = 143
            downFrame2 = 0
            maxRightFrame = 35
            # lets consider the toons position on the vine
            numLeftFramesChoppedOff = (downFrame1 - maxLeftFrame) * (1 - toonT)
            numRightFramesChoppedOff = (maxRightFrame) * (1 -toonT)
            numLeftFramesChoppedOff = 0
            numRightFramesChoppedOff = 0
            maxLeftFrame += numLeftFramesChoppedOff
            maxRightFrame -= numRightFramesChoppedOff
            # figure out the frame to use based on swingT
            numFirstHalfFrames = downFrame1 - maxLeftFrame + 1
            numSecondHalfFrames = maxRightFrame - downFrame2 + 1
            numFrames = numFirstHalfFrames + numSecondHalfFrames
            framesToChopOff = numFrames * self.swingT
            if framesToChopOff < numFirstHalfFrames:
                startingFrame = maxLeftFrame + framesToChopOff
                halfDur = duration / 2.0
                swing1Dur = (1 - (framesToChopOff / numFirstHalfFrames)) * halfDur
                toonSwing1 = ActorInterval(av, 'swing', startFrame = startingFrame,
                                           endFrame = downFrame1, playRate = playRate, #duration = swing1Dur,
                                           name='swingForward1')
                toonSwing2 = ActorInterval(av, 'swing', startFrame = downFrame2,
                                           endFrame = maxRightFrame, playRate = playRate, #duration = halfDur,
                                           name = 'swingForward2')
                swingInterval.append(toonSwing1)
                swingInterval.append(toonSwing2)
            else:
                secondHalfFramesToChopOff = framesToChopOff - numFirstHalfFrames
                startingFrame = downFrame2 + secondHalfFramesToChopOff
                toonSwing2 = ActorInterval(av, 'swing', startFrame = startingFrame,
                                           endFrame = maxRightFrame, playRate = playRate, #duration = duration,
                                           name='swingForward2')
                swingInterval.append(toonSwing2)
            #swingInterval.append(Func(self.updateSwingAnim, avId))
        else:
            maxRightFrame = 35
            maxLeftFrame = 107
            # lets consider the toons position on the vine
            midFrame = (maxLeftFrame + maxRightFrame) / 2.0
            numLeftFramesChoppedOff = 0
            numRightFramesChoppedOff = 0
            if 0 : #toonT < 0.5:
                playRate = playRate * toonT
                numLeftFramesChoppedOff = (maxLeftFrame - midFrame) * (1 - toonT)
                numRightFramesChoppedOff = (midFrame - maxRightFrame) * (1 -toonT)                
            #self.notify.debug('orig maxRight=%d maxLeft=%d' % ( maxRightFrame, maxLeftFrame))
            maxLeftFrame -= numLeftFramesChoppedOff
            maxRightFrame += numRightFramesChoppedOff
            #self.notify.debug('new maxRight=%f maxLeft=%f' % ( maxRightFrame, maxLeftFrame))
            numFrames = maxLeftFrame - maxRightFrame + 1
            # figure out the frame to use based on swingT
            framesToChopOff = numFrames * self.swingT                    
            startingFrame = maxRightFrame + framesToChopOff
            #self.notify.debug('startFrame=%d endFrame=%d playRate=%f' %(startingFrame, maxLeftFrame, playRate))
            toonSwing = ActorInterval(av, 'swing', startFrame = startingFrame,
                                      endFrame = maxLeftFrame, playRate = playRate)
            swingInterval.append(toonSwing)
            #swingInterval.append(Func(self.updateSwingAnim, avId))

        self.attachedToons[avId][6] = swingInterval
        swingInterval.start()

    def setupSwingAnimSmall(self, av, avId):
        """Use only a very small set of the swing animation for a small angle."""
        swingInterval = Sequence()
        maxLeftFrame = 0
        maxRightFrame = 20
        startingLeftFrame =5
        numFrames =  maxRightFrame -maxLeftFrame + 1
        #numFrames += 1
        #numFrames -= 1
        playRate = ( self.SwingAnimPeriod /self.period)
        duration = (1 - self.swingT) * self.period / 2.0
        #duration = self.period / 2.0
        if duration == 0:
            return
        toonT = self.attachedToons[avId][0] 

        #import pdb; pdb.set_trace()
        framesPerSecondBase = self.MaxNumberOfFramesInSwingAnim / self.SwingAnimPeriod

        desiredFramesPerSecond = numFrames / duration
        slowedPlayRate = desiredFramesPerSecond / framesPerSecondBase
        #self.notify.debug('duration=%f slowedPlayRate=%f' % ( duration, slowedPlayRate))
        facingRight = self.attachedToons[avId][5]
        if (self.swingingForward and facingRight) or \
           (not self.swingingForward and not facingRight):        
            toonSwing1 = ActorInterval(av, 'swing', startFrame = startingLeftFrame  ,
                                      endFrame = maxLeftFrame,
                                      playRate = slowedPlayRate)
            toonSwing2 = ActorInterval(av, 'swing', startFrame = maxLeftFrame +1,
                                      endFrame = maxRightFrame - startingLeftFrame  ,
                                      playRate = slowedPlayRate)            
            swingInterval.append(toonSwing1)
            swingInterval.append(toonSwing2)
        else:
            toonSwing1 = ActorInterval(av, 'swing',
                                       startFrame = maxRightFrame - startingLeftFrame ,
                                       endFrame = maxRightFrame,
                                       playRate = slowedPlayRate)
            toonSwing2 = ActorInterval(av, 'swing', startFrame = maxRightFrame ,
                                      endFrame = startingLeftFrame  ,
                                      playRate = slowedPlayRate)            
            swingInterval.append(toonSwing1)
            swingInterval.append(toonSwing2)

        self.attachedToons[avId][6] = swingInterval
        swingInterval.start()
        
    def setupSwingAnimMinimal(self, av, avId):
        """Use only a extremely small set of the swing animation for a near zero angle."""
        swingInterval = Sequence()
        maxLeftFrame = 88
        maxRightFrame = 84
        duration = (1 - self.swingT) * self.period / 2.0
        if duration < 0.001:
            duration = 0.001
        numFrames =  maxLeftFrame - maxRightFrame + 1
        numFrames *= 2
        framesPerSecondBase = self.MaxNumberOfFramesInSwingAnim / self.SwingAnimPeriod
        desiredFramesPerSecond = numFrames / duration
        slowedPlayRate = desiredFramesPerSecond / framesPerSecondBase
        toonSwing1 = ActorInterval(av, 'swing',
                                   startFrame = maxLeftFrame,
                                   endFrame = maxRightFrame,
                                   playRate = slowedPlayRate,
                                   )
        toonSwing2 = ActorInterval(av, 'swing',
                                   startFrame = maxRightFrame,
                                   endFrame = maxLeftFrame,
                                   playRate = slowedPlayRate,
                                   )
        swingInterval.append(toonSwing1)
        swingInterval.append(toonSwing2)
        self.attachedToons[avId][6] = swingInterval
        swingInterval.start()        
        
    def setupSwingAnim(self, avId):
        """Figure out the swing anim when a toon has just attached to the vine."""
        #assert self.notify.debugStateCall(self)
        if not self.attachedToons.has_key(avId):
            return
        av = base.cr.doId2do.get(avId)
        if not av:
            return
        prevIval = self.attachedToons[avId][6]
        if prevIval:
            prevIval.pause()
            del prevIval        
        # calculate our swing angle
        toonT = self.attachedToons[avId][0]        
        swingAnimType= self.calcSwingAnimType(toonT)
        if swingAnimType == self.SwingAnimFull:
            self.setupSwingAnimFull(av, avId)
        elif swingAnimType == self.SwingAnimSmall:
            self.setupSwingAnimSmall(av, avId)
        else:
            self.setupSwingAnimMinimal(av, avId)
        
    def calcSwingAnimType(self,toonT):
        """Calculate what kind of swing animation based on his position on the vine."""
        angleInDegrees = toonT * self.baseAngle
        retval = self.SwingAnimFull
        if angleInDegrees > 10:
            retval = self.SwingAnimFull
        elif angleInDegrees > 2:
            retval = self.SwingAnimSmall
        else:
            retval = self.SwingAnimMinimal
        return retval
        
    def updateSwingAnims(self):
        """Calculate the new swing anim when the vine has reached max left or max right."""
        if self.unloading:
            return
        
        for avId in self.attachedToons.keys():
            #self.notify.debugStateCall(self)
            self.setupSwingAnim(avId)
