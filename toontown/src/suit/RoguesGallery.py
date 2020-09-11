from pandac.PandaModules import *
from direct.fsm import StateData
import Suit
import SuitDNA
from toontown.toonbase import ToontownGlobals
import random

class RoguesGallery(StateData.StateData):
    """RoguesGallery

    This generates a presentation of all of the suits in the game,
    just like the printed chart we have on the wall.

    It has no in-game purpose.  It's mainly useful for testing the
    suit dna, and for admiring the suits.

    When load() is called, the gallery is created within the node
    represented by self.gallery.  The enter() and exit() functions, if
    used, set the camera up to look at the gallery, but you can do
    other things with it if you want.  The gallery is scaled to
    correspond with the range of the aspect2d screen coordinates.
    """

    def __init__(self, rognamestr = None):
        StateData.StateData.__init__(self, "roguesDone")

        self.rognamestr = rognamestr

        # Set up the constants that define the size and shape of the
        # gallery.
        self.left = -1.333
        self.right = 1.333
        self.bottom = -1.0
        self.top = 1.0
            
        self.sideMargins = 0.1
        self.topMargins = 0.1
        self.xSpaceBetweenDifferentSuits = 0.01
        self.xSpaceBetweenSameSuits = 0.0
        self.ySpaceBetweenSuits = 0.05

        self.labelScale = 1.0

    def load(self):
        if StateData.StateData.load(self):
            # Compute the derived constants.
            self.width = self.right - self.left - self.sideMargins * 2.0
            self.height = self.top - self.bottom - self.topMargins * 2.0

            if(self.rognamestr == None):
                self.numSuitTypes = SuitDNA.suitsPerDept
                self.numSuitDepts = len(SuitDNA.suitDepts)
            else:
                self.numSuitTypes = 1
                self.numSuitDepts = 1
                self.xSpaceBetweenDifferentSuits = 0.0
                self.xSpaceBetweenSameSuits = 0.0
                self.ySpaceBetweenSuits = 0.0
            
            self.ySuitInc = (
                (self.height + self.ySpaceBetweenSuits) / self.numSuitDepts)
            self.ySuitMaxAllowed = self.ySuitInc - self.ySpaceBetweenSuits

            self.xRowSpace = self.width - (self.numSuitTypes - 1) * self.xSpaceBetweenDifferentSuits - self.numSuitTypes * self.xSpaceBetweenSameSuits

            self.__makeGallery()

    def unload(self):
        if StateData.StateData.unload(self):
            self.gallery.removeNode()
            del self.suits
            del self.actors

    def enter(self):
        if StateData.StateData.enter(self):
            # Temporarily hide everything in render2d and render.  Drastic!
            render.hide()
            aspect2d.hide()

            self.gallery.reparentTo(render2d)
            self.gallery.setMat(base.aspect2d.getMat())

            # Push it back a little to avoid the DX near clipping
            # plane problem.
            self.gallery.setPos(0.0, 10.0, 0.0)

            base.setBackgroundColor(0.6, 0.6, 0.6)

    def exit(self):
        if StateData.StateData.exit(self):
            self.stop()
            
            # Undo the damage we did with enter().
            render.show()
            aspect2d.show()
            self.gallery.reparentTo(hidden)
            self.gallery.clearMat()

            base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

            self.ignoreAll()

    def animate(self):
        """animate(self)

        Animates all the suits in the gallery, just for kicks.
        """
        self.load()

        for suit in self.actors:
            suit.pose("neutral", random.randint(0, suit.getNumFrames("neutral") - 1))
            suit.loop("neutral", 0)

    def stop(self):
        """stop(self)

        Stops all the animation, and restores the suits to a medium frame.
        """
        self.load()

        for suit in self.actors:
            suit.pose("neutral", 30)

    def autoExit(self):
        """autoExit(self)

        Sets up a hook to close the gallery when the user clicks the
        left mouse button.
        """
        self.acceptOnce('mouse1', self.exit)

    def __makeGallery(self):
        """__makeGallery(self)

        Creates the gallery and populates it with suits.
        """
        self.gallery = hidden.attachNewNode('gallery')

        # Ensure the gallery will be depth-tested.  This allows us to
        # parent it to aspect2d (which normally isn't) and still see
        # the suits correctly.
        self.gallery.setDepthWrite(1)
        self.gallery.setDepthTest(1)
        
        self.suits = []
        self.actors = []
        self.text = TextNode("rogues")
        self.text.setFont(ToontownGlobals.getInterfaceFont())
        self.text.setAlign(TextNode.ACenter)
        self.text.setTextColor(0.0, 0.0, 0.0, 1.0)
        
        self.rowHeight = 0.0
        self.minXScale = None

        print "rognamestr='",self.rognamestr,"'\n"

        if((self.rognamestr == None) or (len(self.rognamestr) == 0)):
            for dept in SuitDNA.suitDepts:
                self.__makeDept(dept)
        else:
            self.suitRow = []
            self.rowWidth = 0.0
            self.__makeSuit(None,None,self.rognamestr)
            self.minXScale = self.xRowSpace / self.rowWidth
            self.suits.append((self.rowWidth, self.suitRow))
            del self.suitRow
            
        self.__rescaleSuits()

    def __makeDept(self, dept):
        """__makeDept(self, string dept)

        Makes a row of suits for the indicated department.
        """
        self.suitRow = []
        self.rowWidth = 0.0
        for type in range(self.numSuitTypes):
            self.__makeSuit(dept, type)

        # How much would we need to scale these suits horizontally to
        # use up all of our available space?
        xScale = self.xRowSpace / self.rowWidth

        if self.minXScale == None or self.minXScale > xScale:
            self.minXScale = xScale

        self.suits.append((self.rowWidth, self.suitRow))
        del self.suitRow
        

    def __makeSuit(self, dept, type, name = None):
        """__makeSuit(self, string dept, int type)

        Creates a single suit of the indicated department and type.
        Parents the new suit to self.gallery and adds it to
        self.rowSuits, in both face-on and profile views, and
        accumulates its width.

        """
        dna = SuitDNA.SuitDNA()

        if(name!=None):
            dna.newSuit(name)
        else:
            dna.newSuitRandom(type + 1, dept)

        suit = Suit.Suit()
        suit.setStyle(dna)
        suit.generateSuit()
        suit.pose("neutral", 30)

        # Compute the maximum extents of the suit.  We'll use to
        # scale all the suits to fit their boxes after we're done.
        ll = Point3()
        ur = Point3()
        suit.update()
        suit.calcTightBounds(ll, ur)

        suitWidth = ur[0] - ll[0]
        suitDepth = ur[1] - ll[1]
        suitHeight = ur[2] - ll[2]

        #print "height of %s (%s) is %0.2f" % (dna.name, suit.name, suitHeight)

        self.rowWidth += suitWidth + suitDepth
        self.rowHeight = max(self.rowHeight, suitHeight)

        # Now put the suit in the gallery, once as a head-on, and once
        # as a profile.
        suit.reparentTo(self.gallery)
        suit.setHpr(180.0, 0.0, 0.0)

        profile = Suit.Suit()
        profile.setStyle(dna)
        profile.generateSuit()
        profile.pose("neutral", 30)
        profile.reparentTo(self.gallery)
        profile.setHpr(90.0, 0.0, 0.0)

        self.suitRow.append((type, suitWidth, suit, suitDepth, profile))
        self.actors.append(suit)
        self.actors.append(profile)
        
    def __rescaleSuits(self):
        """__rescaleSuits(self)

        After all the suits have been generated, scales them all down
        to fix their boxes in the gallery, based on the computed
        xSuitMax and ySuitMax.
        """

        # How much will we need to scale to fit each dimension?
        yScale = self.ySuitMaxAllowed / self.rowHeight

        # Our overall scale will be the smaller of those.
        scale = min(self.minXScale, yScale)

        y = self.top - self.topMargins + self.ySpaceBetweenSuits
        for rowWidth, suitRow in self.suits:
            rowWidth *= scale
            extraSpace = self.xRowSpace - rowWidth

            # Distribute all the extra space for this row between each
            # suit.
            extraSpacePerSuit = extraSpace / ((self.numSuitTypes * 2) - 1)
            
            x = self.left + self.sideMargins
            y -= self.ySuitInc
            for type, width, suit, depth, profile in suitRow:
                left = x
                
                width *= scale
                suit.setScale(scale)
                suit.setPos(x + width / 2.0, 0.0, y)
                x += width + self.xSpaceBetweenSameSuits + extraSpacePerSuit

                depth *= scale
                profile.setScale(scale)
                profile.setPos(x + depth / 2.0, 0.0, y)
                x += depth
                right = x
                x += self.xSpaceBetweenDifferentSuits + extraSpacePerSuit

                # Finally put a nametag over the pair of them.
                self.text.setText(suit.getName())
                name = self.gallery.attachNewNode(self.text.generate())
                name.setPos((right + left) / 2.0, 0.0, y + (suit.height + self.labelScale * 0.5) * scale)
                name.setScale(self.labelScale * scale)
