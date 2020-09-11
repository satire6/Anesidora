
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.coghq import BarrelBase

from otp.level import BasicEntities
from direct.directnotify import DirectNotifyGlobal

class DistributedBarrelBase(BasicEntities.DistributedNodePathEntity,
                            BarrelBase.BarrelBase):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBarrelBase")

    def __init__(self, cr):
        self.rewardPerGrabMax = 0
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)
        self.grabSoundPath = "phase_4/audio/sfx/SZ_DD_treasure.mp3"
        self.rejectSoundPath = "phase_4/audio/sfx/ring_miss.mp3"
        self.animTrack = None
        self.shadow = 0
        self.barrelScale = .5
        self.sphereRadius = 3.2
        self.playSoundForRemoteToons = 1
        self.gagNode = None
        self.gagModel = None
        self.barrel = None
        
    def disable(self):
        BasicEntities.DistributedNodePathEntity.disable(self)
        self.ignoreAll()
        if self.animTrack:
            self.animTrack.pause()
            self.animTrack = None
            
    def generate(self):
        """generate(self)
        This method is called when the DistributedEntity is reintroduced
        to the world, either for the first time or from the cache.
        """
        BasicEntities.DistributedNodePathEntity.generate(self)
        
    def delete(self):
        BasicEntities.DistributedNodePathEntity.delete(self)

        self.gagNode.removeNode()
        del self.gagNode

        if self.barrel:
            self.barrel.removeNode()
            del self.barrel
            self.barrel = None

    def announceGenerate(self):
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)

        # At this point DistributedEntity has filled out all its
        # attributes.  We can now load the model and apply the label
        
        # Load the model, (using loadModelOnce), and child it to the nodepath
        self.loadModel()

        # Make a sphere, name it uniqueName("treasureSphere"), and child it
        # to the nodepath.
        self.collSphere = CollisionSphere(0, 0, 0, self.sphereRadius)
        # Make the sphere intangible
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.uniqueName("barrelSphere"))
        self.collNode.setIntoCollideMask(WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.barrel.attachNewNode(self.collNode)
        self.collNodePath.hide()
        self.applyLabel()
        
        # Add a hook looking for collisions with localToon, and call
        # requestGrab.
        self.accept(self.uniqueName('enterbarrelSphere'),
                    self.handleEnterSphere)
        
    def loadModel(self):
        # Load the sound effect
        self.grabSound = base.loadSfx(self.grabSoundPath)
        self.rejectSound = base.loadSfx(self.rejectSoundPath)

        # load the barrel model
        self.barrel = loader.loadModel("phase_4/models/cogHQ/gagTank")
        
        self.barrel.setScale(self.barrelScale)
        self.barrel.reparentTo(self)

        # set up the node to which the label will be parented
        # use dcs node once a locator is added
        dcsNode = self.barrel.find("**/gagLabelDCS")
        dcsNode.setColor(.15,.15,.1)

        self.gagNode = self.barrel.attachNewNode("gagNode")
        self.gagNode.setPosHpr(0.0,-2.62,4.0,0,0,0)
        # desaturate the label a bit
        self.gagNode.setColorScale(.7,.7,.6,1)

    def handleEnterSphere(self, collEntry=None):
        localAvId = base.localAvatar.getDoId()
        self.d_requestGrab()

    def d_requestGrab(self):
        self.sendUpdate("requestGrab", [])

    def setGrab(self, avId):
        self.notify.debug("handleGrab %s" % avId)
        # this function handles client-side 'grabbed' behavior

        # Save the avId for later, we may need it if there is an unexpected
        # exit.
        self.avId = avId

        if avId == base.localAvatar.doId:
            # First, do not try to grab this treasure anymore.
            self.ignore(self.uniqueName('entertreasureSphere'))
            # dim the barrel since we've already acquired our prize
            # and can't use it again
            self.barrel.setColorScale(.5,.5,.5,1)

        # Play a sound effect, if appropriate
        if self.playSoundForRemoteToons or \
           (self.avId == base.localAvatar.getDoId()):
            base.playSfx(self.grabSound)
            
        # Create the flying treasure track
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        flytime = 1.0
        self.animTrack = Sequence(
            LerpScaleInterval(self.barrel,
                              .2,
                              1.1*self.barrelScale,
                              blendType = "easeInOut"),
            LerpScaleInterval(self.barrel,
                              .2,
                              self.barrelScale,
                              blendType = "easeInOut"),
            Func(self.resetBarrel),
            name = self.uniqueName("animTrack"))

        self.animTrack.start()

    def setReject(self):
        # don't do anything
        self.notify.debug("I was rejected!!!!!")
        return

    def resetBarrel(self):
        # reset the scale
        self.barrel.setScale(self.barrelScale)

        # listen to grab attempts again
        self.accept(self.uniqueName('entertreasureSphere'),
                    self.handleEnterSphere)

