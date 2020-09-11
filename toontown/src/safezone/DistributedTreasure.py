
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasure(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTreasure")
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.av = None
        self.treasureFlyTrack = None
        self.modelPath = None
        self.nodePath = None
        self.dropShadow = None
        self.modelFindString = None
        self.grabSoundPath = None

        # The default treasure reject sound is the same for all
        # treasures.  Still, particular safe zones can override this
        # if they want to.
        self.rejectSoundPath = "phase_4/audio/sfx/ring_miss.mp3"

        self.playSoundForRemoteToons = 1
        self.scale = 1.
        self.shadow = 1
        self.fly = 1
        self.zOffset = 0.
        self.billboard = 0

    def disable(self):
        self.ignoreAll()
        self.nodePath.detachNode()
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        # Stop the movie (if there is one)
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None
        # Call up the chain
        DistributedObject.DistributedObject.delete(self)

        # Really, we don't want to unloadModel on this, until we're
        # leaving the safezone.  Calling unloadModel will force the
        # next treasure of this type to reload from disk.
        #loader.unloadModel(self.modelPath)
        
        self.nodePath.removeNode()

    def announceGenerate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedObject.DistributedObject.announceGenerate(self)
        
        # Load the model, (using loadModelOnce), and child it to the nodepath
        self.loadModel(self.modelPath, self.modelFindString)
        # animate if necessary
        self.startAnimation()
        # Put this thing in the world
        self.nodePath.wrtReparentTo(render)        
        # Add a hook looking for collisions with localToon, and call
        # requestGrab.
        self.accept(self.uniqueName('entertreasureSphere'),
                    self.handleEnterSphere)

    def handleEnterSphere(self, collEntry=None):
        # Only toons with hp > 0 can pick up treasures.
        #if base.localAvatar.hp > 0:
        localAvId = base.localAvatar.getDoId()

        # if treasure is not going to fly, make it disappear
        # right away
        if not self.fly:
            self.handleGrab(localAvId)

        self.d_requestGrab()

    def d_requestGrab(self):
        self.sendUpdate("requestGrab", [])

    def getSphereRadius(self):
        """getSphereRadius(self)
        This method can be overwritten by an inheritor.
        """
        return 2.0

    def loadModel(self, modelPath, modelFindString = None):
        # Load the sound effect
        self.grabSound = base.loadSfx(self.grabSoundPath)
        self.rejectSound = base.loadSfx(self.rejectSoundPath)

        if self.nodePath == None:
            self.makeNodePath()
        else:
            self.treasure.getChildren().detach()

        # Load the treasure model and put it under our root node.
        model = loader.loadModel(modelPath)
        if modelFindString != None:
            model = model.find("**/" + modelFindString)
            assert model != None
        model.instanceTo(self.treasure)

    def makeNodePath(self):
        self.nodePath = NodePath(self.uniqueName("treasure"))
        if self.billboard:
            self.nodePath.setBillboardPointEye()
        self.nodePath.setScale(0.9*self.scale)

        self.treasure = self.nodePath.attachNewNode('treasure')

        if self.shadow:
            if not self.dropShadow:
                # Load the dropShadow
                self.dropShadow = loader.loadModel(
                    "phase_3/models/props/drop_shadow")
                # Set the shadow color
                self.dropShadow.setColor(0, 0, 0, 0.5)
                self.dropShadow.setPos(0,0,0.025)
                self.dropShadow.setScale(0.4*self.scale)

                # Might as well apply the transforms to the shadow vertices.
                self.dropShadow.flattenLight()
            # Parent the dropShadow to the NodePath root
            self.dropShadow.reparentTo(self.nodePath)

        # Make a sphere, name it uniqueName("treasureSphere"), and child it
        # to the nodepath.
        collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())
        # Make the sphere intangible
        collSphere.setTangible(0)
        collNode = CollisionNode(self.uniqueName("treasureSphere"))
        collNode.setIntoCollideMask(WallBitmask)
        collNode.addSolid(collSphere)
        self.collNodePath = self.nodePath.attachNewNode(collNode)
        self.collNodePath.stash()

    def getParentNodePath(self):
        """getParentNodePath(self)
        This defaults to render, but may be overridden by an inheritor
        """
        return render

    # The handler that catches the initial position established on the AI
    def setPosition(self, x, y, z):
        if not self.nodePath:
            self.makeNodePath()

        self.nodePath.reparentTo(self.getParentNodePath())
        self.nodePath.setPos(x, y, z+self.zOffset)
        self.collNodePath.unstash()

    def setGrab(self, avId):
        if avId == 0:
            # avId of 0 indicates it hasn't been grabbed by anyone.
            return
        
        # ignore this message if we have already called handleGrab
        if self.fly or avId != base.localAvatar.getDoId():
            self.handleGrab(avId)

    def setReject(self):
        # Fade the treasure out and back in again to indicate a failed
        # grab.

        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None

        base.playSfx(self.rejectSound, node = self.nodePath)
        self.treasureFlyTrack = Sequence(
            LerpColorScaleInterval(self.nodePath, 0.8,
                                   colorScale = VBase4(0, 0, 0, 0),
                                   startColorScale = VBase4(1, 1, 1, 1),
                                   blendType = 'easeIn'),
            LerpColorScaleInterval(self.nodePath, 0.2,
                                   colorScale = VBase4(1, 1, 1, 1),
                                   startColorScale = VBase4(0, 0, 0, 0),
                                   blendType = 'easeOut'),
            name = self.uniqueName("treasureFlyTrack"))
        self.treasureFlyTrack.start()
        
    def handleGrab(self, avId):
        # this function handles client-side 'grabbed' behavior
        # NOTE: if the treasure does not fly towards the toon,
        # this function will be called immediately, before the
        # AI comes back and announces that the treasure was grabbed.
        # Someone else may actually end up getting credit for the
        # grab from the AI, after this has been called.
        
        # First, do not try to grab this treasure anymore.
        self.collNodePath.stash()
        # Save the avId for later, we may need it if there is an unexpected
        # exit.
        self.avId = avId

        # Look up the avatar
        if self.cr.doId2do.has_key(avId):
            av = self.cr.doId2do[avId]
            self.av = av
        else:
            # I guess he disconnected... Just hide the treasure
            self.nodePath.detachNode()
            return

        # Play a sound effect, if appropriate
        if self.playSoundForRemoteToons or \
           (self.avId == base.localAvatar.getDoId()):
            base.playSfx(self.grabSound, node = self.nodePath)

        if not self.fly:
            # don't make it fly, just make it disappear
            self.nodePath.detachNode()
            return

        # Reparent the treasure to the toon
        self.nodePath.wrtReparentTo(av)

        # Create the flying treasure track
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None

        # Add a hook in case this avatar gets deleted while the
        # Treasure is flying.
        avatarGoneName = self.av.uniqueName("disable")
        self.accept(avatarGoneName, self.handleUnexpectedExit)

        flytime = 1.0
        track = Sequence(
            LerpPosInterval(self.nodePath,
                            flytime,
                            pos = Point3(0, 0, 3),
                            startPos = self.nodePath.getPos(),
                            blendType = "easeInOut"),
            Func(self.nodePath.detachNode),
            Func(self.ignore, avatarGoneName))

        if self.shadow:
            self.treasureFlyTrack = Sequence(
                HideInterval(self.dropShadow),
                track,
                ShowInterval(self.dropShadow),
                name = self.uniqueName("treasureFlyTrack"))
        else:
            self.treasureFlyTrack = Sequence(
                track,
                name = self.uniqueName("treasureFlyTrack"))

        self.treasureFlyTrack.start()
    
    def handleUnexpectedExit(self):
        # The avatar we were flying the treasure to just disconnected.
        self.notify.warning("While getting treasure, " + str(self.avId) +
                            " disconnected.")
        # Stop the multitrack
        if self.treasureFlyTrack:
            self.treasureFlyTrack.finish()
            self.treasureFlyTrack = None

    def getStareAtNodeAndOffset(self):
        return self.nodePath, Point3()

    def startAnimation(self):
        # Most treasures don't have default animations
        # Estate flying treasures might, so add this base
        # class function
        pass
