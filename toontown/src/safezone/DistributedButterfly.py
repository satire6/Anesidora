
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from pandac.PandaModules import NodePath
from direct.directutil import Mopath
from toontown.toonbase import ToontownGlobals
from direct.actor import Actor
import ButterflyGlobals
from direct.showbase import RandomNumGen
import random

class DistributedButterfly(DistributedObject.DistributedObject): 

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedButterfly')

    id = 0
    # wings_1 (solid yellow)
    # wings_2 (yellow w/ dots) (1, 1, 1), (0.2, 0, 1), (1, 0, 1), (0.8, 0, 1)
    # wings_3 (solid white) (0.8, 0, 0.8), (0, 0.8, 0.8), (0.9, 0.4, 0.6)
    #           (0.9, 0.4, 0.4), (0.8, 0.5, 0.9), (0.4, 0.1, 0.7)
    # wings_4 (white w/ dots)
    # wings_5 (pale yellow w/ lines) (0.8, 0, 0.8), (0.6, 0.6, 0.9)
    #           (0.7, 0.6, 0.9), (0.8, 0.6, 0.9), (0.9, 0.6, 0.9),
    #           (1, 0.6, 0.9)
    # wings_6 (blue & yellow)
    wingTypes = ('wings_1',
                 'wings_2',
                 'wings_3',
                 'wings_4',
                 'wings_5',
                 'wings_6')
    yellowColors = (Vec4(1, 1, 1, 1), 
                    Vec4(0.2, 0, 1, 1), 
                    Vec4(0.8, 0, 1, 1))
    whiteColors = (Vec4(0.8, 0, 0.8, 1), 
                   Vec4(0, 0.8, 0.8, 1), 
                   Vec4(0.9, 0.4, 0.6, 1), 
                   Vec4(0.9, 0.4, 0.4, 1), 
                   Vec4(0.8, 0.5, 0.9, 1), 
                   Vec4(0.4, 0.1, 0.7, 1))
    paleYellowColors = (Vec4(0.8, 0, 0.8, 1), 
                        Vec4(0.6, 0.6, 0.9, 1), 
                        Vec4(0.7, 0.6, 0.9, 1), 
                        Vec4(0.8, 0.6, 0.9, 1), 
                        Vec4(0.9, 0.6, 0.9, 1), 
                        Vec4(1, 0.6, 0.9, 1))
    shadowScaleBig = Point3(0.07, 0.07, 0.07)
    shadowScaleSmall = Point3(0.01, 0.01, 0.01)

    def __init__(self, cr):
        """__init__(cr)
        """
        DistributedObject.DistributedObject.__init__(self, cr)

        self.fsm = ClassicFSM.ClassicFSM('DistributedButterfly',
                        [State.State('off',
                                self.enterOff,
                                self.exitOff,
                                ['Flying', 'Landed']),
                         State.State('Flying',
                                self.enterFlying,
                                self.exitFlying,
                                ['Landed']),
                         State.State('Landed',
                                self.enterLanded,
                                self.exitLanded,
                                ['Flying'])],
                        # Initial State
                        'off',
                        # Final State
                        'off',
                        )
        self.butterfly = None
        self.butterflyNode = None
        self.curIndex = 0
        self.destIndex = 0
        self.time = 0.0
        self.ival = None
        self.fsm.enterInitialState()

    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedObject.DistributedObject.generate(self)
        if self.butterfly:
            return
        
        self.butterfly = Actor.Actor()
        self.butterfly.loadModel(
            'phase_4/models/props/SZ_butterfly-mod.bam')
        self.butterfly.loadAnims({
            'flutter' : 'phase_4/models/props/SZ_butterfly-flutter.bam',
            'glide' :   'phase_4/models/props/SZ_butterfly-glide.bam',
            'land' :    'phase_4/models/props/SZ_butterfly-land.bam'})
        
        # Randomly choose one of the butterfly wing patterns
        index = self.doId % len(self.wingTypes)
        chosenType = self.wingTypes[index]
        node = self.butterfly.getGeomNode()
        for type in self.wingTypes:
            wing = node.find('**/' + type)    
            if (type != chosenType):
                wing.removeNode()
            else:
                # Choose an appropriate blend color
                if (index == 0 or index == 1):
                    color = self.yellowColors[self.doId % len(self.yellowColors)]
                elif (index == 2 or index == 3):
                    color = self.whiteColors[self.doId % len(self.whiteColors)]
                elif (index == 4):
                    color = self.paleYellowColors[self.doId % len(self.paleYellowColors)]
                else:
                    color = Vec4(1, 1, 1, 1)
                wing.setColor(color)

        # Make another copy of the butterfly model so we can LOD the
        # blending.  Butterflies that are far away won't bother to
        # blend animations; nearby butterflies will use dynamic
        # blending to combine two or more animations at once on
        # playback for a nice fluttering and landing effect.
        self.butterfly2 = Actor.Actor(other = self.butterfly)

        # Allow the nearby butterfly to blend between its three
        # animations.  All animations will be playing all the time;
        # we'll control which one is visible by varying the control
        # effect.
        self.butterfly.enableBlend(blendType = PartBundle.BTLinear)
        self.butterfly.loop('flutter')
        self.butterfly.loop('land')
        self.butterfly.loop('glide')

        # Make a random play rate so all the butterflies will be
        # flapping at slightly different rates.  This doesn't affect
        # the rate at which the butterfly moves, just the rate at
        # which the animation plays on the butterfly.
        rng = RandomNumGen.RandomNumGen(self.doId)
        playRate = 0.6 + 0.8 * rng.random()
        self.butterfly.setPlayRate(playRate, 'flutter')
        self.butterfly.setPlayRate(playRate, 'land')
        self.butterfly.setPlayRate(playRate, 'glide')
        self.butterfly2.setPlayRate(playRate, 'flutter')
        self.butterfly2.setPlayRate(playRate, 'land')
        self.butterfly2.setPlayRate(playRate, 'glide')

        # Also, a random glide contribution ratio.  We'll blend a bit
        # of the glide animation in with the flutter animation to
        # dampen the effect of flutter.  The larger the number here,
        # the greater the dampening effect.  Some butterflies will be
        # more active than others.  (Except when seen from a long way
        # off, because of the LODNode, below.)
        self.glideWeight = rng.random() * 2

        lodNode = LODNode('butterfly-node')
        lodNode.addSwitch(100, 40)   # self.butterfly2
        lodNode.addSwitch(40, 0)     # self.butterfly
        
        self.butterflyNode = NodePath(lodNode)
        self.butterfly2.setH(180.0)
        self.butterfly2.reparentTo(self.butterflyNode)
        self.butterfly.setH(180.0)
        self.butterfly.reparentTo(self.butterflyNode)
        self.__initCollisions()

        # Set up the drop shadow
        self.dropShadow = loader.loadModel(
                                'phase_3/models/props/drop_shadow')
        self.dropShadow.setColor(0, 0, 0, 0.3)
        self.dropShadow.setPos(0, 0.1, -0.05)
        self.dropShadow.setScale(self.shadowScaleBig)
        self.dropShadow.reparentTo(self.butterfly)

    def disable(self):
        """disable(self)
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        self.butterflyNode.reparentTo(hidden)
        if (self.ival != None):
            self.ival.finish()
        self.__ignoreAvatars()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """delete(self)
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        self.butterfly.cleanup()
        self.butterfly = None
        self.butterfly2.cleanup()
        self.butterfly2 = None
        self.butterflyNode.removeNode()
        self.__deleteCollisions()
        self.ival = None
        del self.fsm
        DistributedObject.DistributedObject.delete(self)


    def uniqueButterflyName(self, name):
        DistributedButterfly.id += 1
        return (name + '-%d' % DistributedButterfly.id)

    def __detectAvatars(self):
        self.accept('enter' + self.cSphereNode.getName(),
                        self.__handleCollisionSphereEnter)

    def __ignoreAvatars(self):
        self.ignore('enter' + self.cSphereNode.getName())

    def __initCollisions(self):
        self.cSphere = CollisionSphere(0., 1., 0., 3.)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode(self.uniqueButterflyName('cSphereNode'))
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.butterflyNode.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def __deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath

    def __handleCollisionSphereEnter(self, collEntry):
        """ Response for a toon walking up to this NPC
        """
        assert(self.notify.debug("Entering collision sphere..."))
        # Tell the server
        self.sendUpdate('avatarEnter', [])

    def setArea(self, playground, area):
        self.playground = playground
        self.area = area

    def setState(self, stateIndex, curIndex, destIndex, time, timestamp):
        self.curIndex = curIndex 
        self.destIndex = destIndex 
        self.time = time
        self.fsm.request(ButterflyGlobals.states[stateIndex],
                         [globalClockDelta.localElapsedTime(timestamp)])

    ##### Off state #####

    def enterOff(self, ts=0.0):
        if (self.butterflyNode != None):
            self.butterflyNode.reparentTo(hidden)
        return None

    def exitOff(self):
        if (self.butterflyNode != None):
            self.butterflyNode.reparentTo(render)
        return None

    ##### Flying state #####

    def enterFlying(self, ts):
        self.__detectAvatars()
        curPos = ButterflyGlobals.ButterflyPoints[self.playground][self.area][self.curIndex]
        destPos = ButterflyGlobals.ButterflyPoints[self.playground][self.area][self.destIndex]
        # We'll hit the ground if we go straight from curPos to destPos
        flyHeight = max(curPos[2], destPos[2]) + ButterflyGlobals.BUTTERFLY_HEIGHT[self.playground]
        curPosHigh = Point3(curPos[0], curPos[1], flyHeight)
        destPosHigh = Point3(destPos[0], destPos[1], flyHeight)

        if (ts <= self.time):
            flyTime = self.time - (ButterflyGlobals.BUTTERFLY_TAKEOFF[self.playground] + ButterflyGlobals.BUTTERFLY_LANDING[self.playground])
            self.butterflyNode.setPos(curPos)
            self.dropShadow.show()
            self.dropShadow.setScale(self.shadowScaleBig)
            oldHpr = self.butterflyNode.getHpr()
            self.butterflyNode.headsUp(destPos)
            newHpr = self.butterflyNode.getHpr()
            self.butterflyNode.setHpr(oldHpr)
            takeoffShadowT = 0.2 * ButterflyGlobals.BUTTERFLY_TAKEOFF[self.playground]
            landShadowT = 0.2 * ButterflyGlobals.BUTTERFLY_LANDING[self.playground]
            self.butterfly2.loop('flutter')
            self.ival = Sequence(
                Parallel(
                    LerpPosHprInterval(self.butterflyNode, 
                                       ButterflyGlobals.BUTTERFLY_TAKEOFF[self.playground],
                                       curPosHigh, newHpr),
                    LerpAnimInterval(self.butterfly,
                                     ButterflyGlobals.BUTTERFLY_TAKEOFF[self.playground],
                                     'land', 'flutter'),
                    LerpAnimInterval(self.butterfly,
                                     ButterflyGlobals.BUTTERFLY_TAKEOFF[self.playground],
                                     None, 'glide',
                                     startWeight = 0, endWeight = self.glideWeight),
                    Sequence(
                        LerpScaleInterval(self.dropShadow,
                                          takeoffShadowT,
                                          self.shadowScaleSmall,
                                          startScale = self.shadowScaleBig),
                        HideInterval(self.dropShadow)
                        ),
                    ),
                LerpPosInterval(self.butterflyNode, flyTime, 
                                destPosHigh),
                Parallel(
                    LerpPosInterval(self.butterflyNode,
                                    ButterflyGlobals.BUTTERFLY_LANDING[self.playground],
                                    destPos),
                    LerpAnimInterval(self.butterfly,
                                     ButterflyGlobals.BUTTERFLY_LANDING[self.playground],
                                     'flutter', 'land'),
                    LerpAnimInterval(self.butterfly,
                                     ButterflyGlobals.BUTTERFLY_LANDING[self.playground],
                                     None, 'glide',
                                     startWeight = self.glideWeight, endWeight = 0),
                    Sequence(
                        Wait(ButterflyGlobals.BUTTERFLY_LANDING[self.playground] - landShadowT),
                        ShowInterval(self.dropShadow),
                        LerpScaleInterval(self.dropShadow,
                                          landShadowT,
                                          self.shadowScaleBig,
                                          startScale = self.shadowScaleSmall)
                        ),
                    ),
                name = self.uniqueName("Butterfly"))
            self.ival.start(ts)
        else:
            self.ival = None
            self.butterflyNode.setPos(destPos)
            self.butterfly.setControlEffect('land', 1.0)
            self.butterfly.setControlEffect('flutter', 0.0)
            self.butterfly.setControlEffect('glide', 0.0)
            self.butterfly2.loop('land')
        return None

    def exitFlying(self):
        self.__ignoreAvatars()
        if (self.ival != None):
            self.ival.finish()
            self.ival = None
        return None

    ##### Landed state #####

    def enterLanded(self, ts):
        self.__detectAvatars()
        curPos = ButterflyGlobals.ButterflyPoints[self.playground][self.area][self.curIndex]
        self.butterflyNode.setPos(curPos)
        self.dropShadow.show()
        self.dropShadow.setScale(self.shadowScaleBig)
        self.butterfly.setControlEffect('land', 1.0)
        self.butterfly.setControlEffect('flutter', 0.0)
        self.butterfly.setControlEffect('glide', 0.0)
        self.butterfly2.pose('land', random.randrange(self.butterfly2.getNumFrames('land')))
        return None

    def exitLanded(self):
        self.__ignoreAvatars()
        return None
