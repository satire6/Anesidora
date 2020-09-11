
#from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
#from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.fishing import FishGlobals
import GardenGlobals
from direct.actor import Actor

#WARNING Specials Photo is used in both GardenPage.py and PlantingGUI.py

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
        NodePath.NodePath.hide(self)
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

class SpecialsPhoto(NodePath):
    """
    #WARNING Specials Photo is used in both GardenPage.py and PlantingGUI.py
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("SpecialsPhoto")

    # special methods
    def __init__(self, type=None, parent=aspect2d):
        assert self.notify.debugStateCall(self)
        NodePath.__init__(self)
        self.assign(parent.attachNewNode("SpecialsPhoto"))
        self.type = type
        self.actor = None
        self.sound = None
        self.soundTrack = None
        self.track = None
        self.specialsFrame = None

    def destroy(self):
        assert self.notify.debugStateCall(self)
        self.hide()
        if hasattr(self, "background"):
            self.background.destroy()
            del self.background
        if hasattr(self, "specialsFrame") and hasattr(self.specialsFrame,'destroy'):
            self.specialsFrame.destroy()
        if hasattr(self, 'toonStatuary'):
            if self.toonStatuary.toon:
                self.toonStatuary.deleteToon()
        self.type = None
        del self.soundTrack
        del self.track
        self.parent = None

    def update(self, type):
        assert self.notify.debugStateCall(self)
        self.type = type

    def setBackBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert len(bounds) == 4
        self.backBounds=bounds

    def setBackColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert len(colors) == 4
        self.backColor=colors

    def load(self):
        assert self.notify.debugStateCall(self)

    def makeSpecialsFrame(self, actor):
        assert self.notify.debugStateCall(self)
        # NOTE: this may need to go in FishBase eventually
        actor.setDepthTest(1)
        actor.setDepthWrite(1)

        # scale the actor to the frame
        if not hasattr(self, "specialsDisplayRegion"):
            self.specialsDisplayRegion = DirectRegion(parent=self)
            apply(self.specialsDisplayRegion.setBounds, self.backBounds)
            apply(self.specialsDisplayRegion.setColor, self.backColor)
        frame = self.specialsDisplayRegion.load()
        pitch = frame.attachNewNode('pitch')
        rotate = pitch.attachNewNode('rotate')
        scale = rotate.attachNewNode('scale')
        actor.reparentTo(scale)
        # Translate actor to the center.
        bMin,bMax = actor.getTightBounds()
        center = (bMin + bMax)/2.0
        actor.setPos(-center[0], -center[1], -center[2])

        pitch.setY(2.5)


        return frame

    def loadModel(self, specialsIndex):
        if specialsIndex == -1:
            nodePath = self.attachNewNode("blank")
            return nodePath

        # Handle the ToonStatues separately because we have to load a toon statue of the
        # local avatar with a predefined pose instead of a predefined static model
        if specialsIndex >= 105 and specialsIndex <= 108: # This is the range of Special indices in GardenGlobals.py
            # Don't import this at the top of the file, since this code must run on the AI.
            from toontown.estate import DistributedToonStatuary
            self.toonStatuary = DistributedToonStatuary.DistributedToonStatuary(None)
            self.toonStatuary.setupStoneToon(base.localAvatar.style)
            self.toonStatuary.poseToonFromSpecialsIndex(specialsIndex)
            self.toonStatuary.toon.setH(180)

            pedestalModelPath = GardenGlobals.Specials[specialsIndex]['photoModel']
            pedestal = loader.loadModel(pedestalModelPath)
            self.toonStatuary.toon.reparentTo(pedestal)
            pedestal.setScale(GardenGlobals.Specials[specialsIndex]['photoScale'] * 0.5)
            return pedestal

        else:
            modelName = GardenGlobals.Specials[specialsIndex]['photoModel']
            nodePath = loader.loadModel(modelName)
            desat = None

            colorTuple = (1,1,1)

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

            nodePath.setScale(GardenGlobals.Specials[specialsIndex]['photoScale'] * 0.5)
            return nodePath

    def show(self, showBackground=0):
        self.notify.debug('show')
        assert self.notify.debugStateCall(self)
        messenger.send('wakeup')
        if self.specialsFrame:
            if hasattr(self.actor,'cleanup'):
                self.actor.cleanup()
            if hasattr(self, "specialsDisplayRegion"):
                self.specialsDisplayRegion.unload()
            self.hide()
        self.actor = self.loadModel(self.type)
        self.specialsFrame = self.makeSpecialsFrame(self.actor)

        if showBackground:
            if not hasattr(self, "background"):
                background = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                background = background.find("**/Fish_BG")
                self.background = background
            self.background.setPos(0, 15, 0)
            self.background.setScale(11)
            self.background.reparentTo(self.specialsFrame)


    def hide(self):
        NodePath.NodePath.hide(self)
        assert self.notify.debugStateCall(self)
        if hasattr(self, "specialsDisplayRegion"):
            self.specialsDisplayRegion.unload()
            #self.specialsDisplayRegion.hide()
        if hasattr(self, "background"):
            self.background.hide()
            #import pdb; pdb.set_trace()
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
        if hasattr(self, 'toonStatuary'):
            if self.toonStatuary.toon:
                self.toonStatuary.deleteToon()

    def changeVariety(self, variety):
        self.variety = variety


