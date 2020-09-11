
#from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
#from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.fishing import FishGlobals
import GardenGlobals
from direct.actor import Actor

class DirectRegion(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory("DirectRegion")

    def __init__(self, parent=aspect2d):
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)
        self.assign(parent.attachNewNode("DirectRegion"))
    
    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.unload()
        self.parent = None

    def setBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert self.notify.debugStateCall(self)
        assert len(bounds) == 4
        self.bounds=bounds
        
    def setColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert self.notify.debugStateCall(self)
        assert len(colors) == 4
        self.color=colors

    def show(self):
        assert self.notify.debugStateCall(self)
    
    def hide(self):
        assert self.notify.debugStateCall(self)

    def load(self):
        assert self.notify.debugStateCall(self)
        if not hasattr(self, "cRender"):
            # Create a separate reality for the fish to swim in:
            self.cRender = NodePath('fishSwimRender')
            # It gets its own camera
            self.fishSwimCamera = self.cRender.attachNewNode('fishSwimCamera')
            self.cCamNode = Camera('fishSwimCam')
            self.cLens = PerspectiveLens()
            self.cLens.setFov(40,40)
            self.cLens.setNear(0.1)
            self.cLens.setFar(100.0)
            self.cCamNode.setLens(self.cLens)
            self.cCamNode.setScene(self.cRender)
            self.fishSwimCam = self.fishSwimCamera.attachNewNode(self.cCamNode)

            cm = CardMaker('displayRegionCard')
            
            assert hasattr(self, "bounds")
            apply(cm.setFrame, self.bounds)
            
            self.card = card = self.attachNewNode(cm.generate())
            assert hasattr(self, "color")
            apply(card.setColor, self.color)
            
            newBounds=card.getTightBounds()
            ll=render2d.getRelativePoint(card, newBounds[0])
            ur=render2d.getRelativePoint(card, newBounds[1])
            newBounds=[ll.getX(), ur.getX(), ll.getZ(), ur.getZ()]
            # scale the -1.0..2.0 range to 0.0..1.0:
            newBounds=map(lambda x: max(0.0, min(1.0, (x+1.0)/2.0)), newBounds)

            self.cDr = base.win.makeDisplayRegion(*newBounds)
            self.cDr.setSort(10)
            self.cDr.setClearColor(card.getColor())
            self.cDr.setClearDepthActive(1)
            self.cDr.setClearColorActive(1)
            self.cDr.setCamera(self.fishSwimCam)
        return self.cRender

    def unload(self):
        assert self.notify.debugStateCall(self)
        if hasattr(self, "cRender"):
            base.win.removeDisplayRegion(self.cDr)
            del self.cRender
            del self.fishSwimCamera
            del self.cCamNode
            del self.cLens
            del self.fishSwimCam
            del self.cDr

class FlowerPhoto(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory("FlowerPhoto")

    # special methods
    def __init__(self, species=None, variety = None, parent=aspect2d):
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)
        self.assign(parent.attachNewNode("FlowerPhoto"))
        self.species = species
        self.variety = variety
        self.actor = None
        self.sound = None
        self.soundTrack = None
        self.track = None
        self.flowerFrame = None
        
    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.hide()
        if hasattr(self, "background"):
            del self.background
        self.fish = None
        del self.soundTrack
        del self.track
        self.parent = None
        
    def update(self, species, variety):
        assert self.notify.debugStateCall(self)
        self.species = species
        self.variety = variety

    def setSwimBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert len(bounds) == 4
        self.swimBounds=bounds
        
    def setSwimColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert len(colors) == 4
        self.swimColor=colors

    def load(self):
        assert self.notify.debugStateCall(self)
    
    def makeFlowerFrame(self, actor):
        assert self.notify.debugStateCall(self)
        # NOTE: this may need to go in FishBase eventually
        actor.setDepthTest(1)
        actor.setDepthWrite(1)

        # scale the actor to the frame
        if not hasattr(self, "flowerDisplayRegion"):
            self.flowerDisplayRegion = DirectRegion(parent=self)
            apply(self.flowerDisplayRegion.setBounds, self.swimBounds)
            apply(self.flowerDisplayRegion.setColor, self.swimColor)
        frame = self.flowerDisplayRegion.load()
        pitch = frame.attachNewNode('pitch')
        rotate = pitch.attachNewNode('rotate')
        scale = rotate.attachNewNode('scale')
        actor.reparentTo(scale)
        # Translate actor to the center.
        bMin,bMax = actor.getTightBounds()
        center = (bMin + bMax)/2.0
        actor.setPos(-center[0], -center[1], -center[2])

        attrib = GardenGlobals.PlantAttributes[self.species]
        if attrib.has_key('photoPos'):
            self.notify.debug('oldPos = %s' % actor.getPos())
            photoPos = attrib['photoPos']
            self.notify.debug('newPos = %s' % str(photoPos))
            actor.setPos(photoPos[0],photoPos[1],photoPos[2])
        
        scale.setScale(attrib['photoScale'])
        rotate.setH(attrib['photoHeading'])
        pitch.setP(attrib['photoPitch'])
        pitch.setY(1.75)

        return frame

    def loadModel(self, species, variety):        
        modelName = GardenGlobals.PlantAttributes[species]['fullGrownModel']
        nodePath = loader.loadModel(modelName)
        desat = None
        flowerColorIndex = GardenGlobals.PlantAttributes[species]['varieties'][variety][1]
        colorTuple = GardenGlobals.FlowerColors[flowerColorIndex]

        useWilted = 0
        wilt = nodePath.find('**/*wilt*')
        bloom = nodePath.find('**/*bloom*')
        if useWilted:
            wilt.show()
            desat = wilt.find('**/*desat*')
            bloom.hide()

        else:
            bloom.show()
            desat = bloom.find('**/*desat*')
            wilt.hide()
            
        if desat and not desat.isEmpty():            
            desat.setColorScale( colorTuple[0],
                                    colorTuple[1],
                                    colorTuple[2],
                                    1.0)            
        else:
            nodePath.setColorScale( colorTuple[0],
                                    colorTuple[1],
                                    colorTuple[2],
                                    1.0)            
        return nodePath

    def show(self, showBackground=0):
        self.notify.debug('show')
        assert self.notify.debugStateCall(self)
        #import pdb; pdb.set_trace()
        # if we are browsing fish we must be awake        
        messenger.send('wakeup')
        if self.flowerFrame:
            if hasattr(self.actor,'cleanup'):
                self.actor.cleanup()
            if hasattr(self, "flowerDisplayRegion"):
                self.flowerDisplayRegion.unload()
            self.hide()
        #modelName = GardenGlobals.PlantAttributes[self.species]['fullGrownModel']
        ##self.actor = self.fish.getActor() 
        #self.actor = Actor.Actor(modelName)
        self.actor = self.loadModel(self.species,self.variety) #loader.loadModel(modelName)
        #self.actor.setTwoSided(1)
        self.flowerFrame = self.makeFlowerFrame(self.actor)

        if showBackground:
            if not hasattr(self, "background"):
                background = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                background = background.find("**/Fish_BG")
                self.background = background
            self.background.setPos(0, 15, 0)
            self.background.setScale(11)
            self.background.reparentTo(self.flowerFrame)
        """
        self.sound, loop, delay, playRate = self.fish.getSound()       
        if playRate is not None:
            # make a track to play the anim and sound
            self.actor.setPlayRate(playRate, "intro")
            self.actor.setPlayRate(playRate, "swim")
        introDuration = self.actor.getDuration("intro")
        track = Parallel(
            Sequence(
                Func(self.actor.play, "intro"),
                Wait(introDuration),
                Func(self.actor.loop, "swim")))
        # if we have a sound, make a track to loop it
        if self.sound:
            soundTrack = Sequence(
                Wait(delay),
                Func(self.sound.play))
            if loop:
                duration = max(introDuration, self.sound.length())
                soundTrack.append(Wait(duration - delay))
                track.append(Func(soundTrack.loop))
                #soundTrack.setLoop(1)
                #track.append(soundTrack)
                self.soundTrack = soundTrack
            else:
                track.append(soundTrack)
        """
        #track = Sequence()
        #self.track = track
        #self.track.start()

    def hide(self):
        assert self.notify.debugStateCall(self)
        if hasattr(self, "flowerDisplayRegion"):
            self.flowerDisplayRegion.unload()
        if self.actor:
            if hasattr(self.actor,'stop'):
                self.actor.stop()
            self.actor.hide()
        if self.sound:
            self.sound.stop()
            self.sound = None
        if self.soundTrack:
            self.soundTrack.pause()
            self.soundTrack = None
        if self.track:
            self.track.pause()
            self.track = None

    def changeVariety(self, variety):
        self.variety = variety

        
