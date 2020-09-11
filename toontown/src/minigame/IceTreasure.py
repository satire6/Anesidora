"""IceTreasure module: contains the IceTreasure class"""
from pandac.PandaModules import Point3, CollisionSphere, CollisionNode, BitMask32
from direct.interval.IntervalGlobal import Sequence, LerpScaleInterval, \
     Parallel, Func, SoundInterval
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleParticles

class IceTreasure(DirectObject):
    """
    Treasures toons can pickup swinging from ice to ice.  Based on MazeTreasure
    """
    
    notify = DirectNotifyGlobal.directNotify.newCategory("IceTreasure")

    RADIUS = 1.0

    def __init__(self, model, pos, serialNum, gameId, penalty =False ):
        # there are going to be MANY (~650) of these created and destroyed
        # all at once for 4-player games; make it lean
        self.serialNum = serialNum

        self.penalty = penalty

        # the fruit has a bit of height, lets recenter
        center = model.getBounds().getCenter()
        center = Point3(0,0,0)
        self.nodePath = model.copyTo(render)
        self.nodePath.setPos(pos[0] - center[0], pos[1] - center[1], pos[2] - center[2])
        self.nodePath.setZ(0) # real assets have bottom at zero
        self.notify.debug('newPos = %s' % self.nodePath.getPos())
        #self.nodePath.setScale(1.0)

        #if self.penalty:
        #    self.nodePath.setColorScale(0.5,0.5,0.5,1.0)

        # Make a sphere, name it uniquely, and child it
        # to the nodepath.
        if self.penalty:
            self.sphereName = "penaltySphere-%s-%s" % (gameId, self.serialNum)
        else:
            self.sphereName = "treasureSphere-%s-%s" % (gameId, self.serialNum)
        self.collSphere = CollisionSphere(center[0], center[1], center[2], self.RADIUS)
        # Make the sphere intangible
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.sphereName)
        self.collNode.setIntoCollideMask(ToontownGlobals.PieBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = render.attachNewNode(self.collNode)
        self.collNodePath.setPos(pos[0] - center[0], pos[1] - center[1], pos[2] - center[2])        
        self.collNodePath.hide()
        self.track = None

        # Add a hook looking for collisions with localToon
        #self.accept('enter' + self.sphereName, self.__handleEnterSphere)
        
        # now that the treasure and sphere have been placed, flatten the
        # whole silly thing
        # self.nodePath.flattenLight()
        
        if self.penalty:
            #self.nodePath.setScale(1,1,0.5)
            self.tip =self.nodePath.find('**/fusetip')
            #self.tip.setX(2)
            #self.tip.setY(0.5)
            #self.tip.setZ(1.5)
            sparks = BattleParticles.createParticleEffect(file='icetnt')
            self.sparksEffect = sparks
            sparks.start(self.tip)
            self.penaltyGrabSound = loader.loadSfx("phase_4/audio/sfx/MG_cannon_fire_alt.mp3")
            self.penaltyGrabSound.setVolume(0.75)
            kaboomAttachPoint = self.nodePath.attachNewNode('kaboomAttach')
            kaboomAttachPoint.setZ(3)
            self.kaboom = loader.loadModel('phase_4/models/minigames/ice_game_kaboom')
            self.kaboom.reparentTo(kaboomAttachPoint)
            #self.kaboom.hide()
            self.kaboom.setScale(2.0)
            self.kaboom.setBillboardPointEye()
            #self.kaboom.setBin('fixed', serialNum)
            #self.kaboom.setDepthTest(False)
            #self.kaboom.setDepthWrite(False)


    def destroy(self):
        self.ignoreAll()
        if self.penalty:
            self.sparksEffect.cleanup()
            if self.track:
                self.track.finish()

        self.nodePath.removeNode()
        del self.nodePath
        del self.collSphere
        self.collNodePath.removeNode()
        del self.collNodePath
        del self.collNode

            

##     def __handleEnterSphere(self, collEntry):
##         self.ignoreAll()
##         # announce that this treasure was grabbed
##         self.notify.debug('treasuerGrabbed')
##         messenger.send("IceTreasureGrabbed", [self.serialNum])

    def showGrab(self):
        self.nodePath.hide()
        self.collNodePath.hide()
        # disable collisions
        self.collNode.setIntoCollideMask(BitMask32(0))
        if self.penalty:
            self.track = Parallel(
                SoundInterval(self.penaltyGrabSound),
                Sequence(
                   Func(self.kaboom.showThrough),
                   LerpScaleInterval(self.kaboom, duration=0.5, scale =Point3(10,10,10),
                                     blendType='easeOut'),
                   Func(self.kaboom.hide),
                   )
                )
            self.track.start()
                
            
        
