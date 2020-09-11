#===============================================================================
# Contact: Ryan Hipple (Schell Games)
# Created: March 2010
#
# Purpose: Class that generates and displays a minimap for a maze.  It also
#          handles masking out and revealing areas as they are discovered.  The
#          minimap has a layer for the maps walls (self.map), a layer for the
#          mask (self.mask), a layer for content under the mask
#          (self.maskedLayer), and a layer for content above the mask
#          (self.visibleLayer).
#===============================================================================

# python imports
import random

# panda imports
from direct.showbase.PythonUtil import Enum
from direct.gui.DirectGui import DirectFrame, DGG
from pandac.PandaModules import Vec2, VBase4D
from pandac.PandaModules import CardMaker
from pandac.PandaModules import Texture, PNMImage
from pandac.PandaModules import Filename

#TODO:maze: move this to a config or global location

# Default resolution for the mask.  Should be no lower than 32.
# Larger values decrease performance.
DEFAULT_MASK_RESOLUTION = 32

# Default ratio for the reveal radius.  This is essentially the percentage of
# the map that is revealed with each step.
DEFAULT_RADIUS_RATIO = 0.09

# Resolution for the map image that will be generated based on the map data.
MAP_RESOLUTION = 320

# Defines the function used to clear a portion of the mask
MazeRevealType = Enum((
    "SmoothCircle",
    "HardCircle",
    "Square",
))

MAZE_REVEAL_TYPE = MazeRevealType.SmoothCircle

class MazeMapGui(DirectFrame):

    notify = directNotify.newCategory("MazeMapGui")

    def __init__(self, mazeLayout, maskResolution=None, radiusRatio=None):
        """
        Constructor for a MazeMap.  the mazeLayout parameter is a 2d array of
        bools (or ints... maybe more depth will be added with that).
        maskResolution is a value for the resolution of the mask covering the
        map.  It should range from 32 to 256.  radiusRatio is essentially
        the percentage of the map that is revealed with each step.
        """
        DirectFrame.__init__(self,
            relief = None,
            state = DGG.NORMAL,
            sortOrder = DGG.BACKGROUND_SORT_INDEX,
        )

        # store / set parameters
        self._mazeLayout = mazeLayout
        self._maskResolution = maskResolution or DEFAULT_MASK_RESOLUTION
        if radiusRatio is None:
            self._radius = self._maskResolution * DEFAULT_RADIUS_RATIO
        else:
            self._radius = self._maskResolution * radiusRatio

        # store false for all maze cells to represent that none of them have
        # been revealed yet.  This can prevent the expensive call to altering
        # the mask if a cell is already revealed
        self._revealedCells = []
        for y in range( len(self._mazeLayout) ):
            self._revealedCells.append([])
            for x in range( len(self._mazeLayout[0]) ):
                self._revealedCells[y].append(False)

        # create reveal function mappings
        self._revealFunctions = {
            MazeRevealType.SmoothCircle : self._revealSmoothCircle,
            MazeRevealType.HardCircle : self._revealHardCircle,
            MazeRevealType.Square : self._revealSquare,
        }
        self._revealFunction = MAZE_REVEAL_TYPE

        # create the map and the mask
        self.map = self._createMapTextureCard()
        self.map.reparentTo(self)
        self.maskedLayer = self.attachNewNode("maskedLayer")
        self.mask = self._createMaskTextureCard()
        self.mask.reparentTo(self)
        self.visibleLayer = self.attachNewNode("visibleLayer")

        #TODO:maze: handle locks and doors
        self._players = []
        self._locks = []
        self._doors = []

    #--- Initialization, Destruction, and Resetting ---#########################

    def _createMapTextureCard(self):
        """
        This will return a NodePath with a card textured with the minimap.  The
        minimap texture is dynamically created from the map data.
        """
        # create and fill empty map image
        mapImage = PNMImage(MAP_RESOLUTION, MAP_RESOLUTION)
        blockFiles = []
        for i in range(5):
            blockFiles.append(PNMImage())
            #blockFiles[i].read(Filename("mapBlock%i.jpg"%(i+1)))
            # TODO:maze either reference a set of textures for each piece or fill with color
            blockFiles[i].read(Filename('phase_4/maps/male_sleeve4New.jpg'))
        mapImage.fill(0.8, 0.8, 0.8)

        # iterate through the map data and place a block in the map image where appropriate
        for x in range( len(self._mazeLayout[0]) ):
            for y in range( len(self._mazeLayout) ):
                if self._mazeLayout[y][x]:
                    ax = float(x)/len(self._mazeLayout[0]) * MAP_RESOLUTION
                    ay = float(y)/len(self._mazeLayout) * MAP_RESOLUTION

                    #TODO:maze use different blocks for different wall types or items
                    #mapImage.copySubImage(random.choice(blockFiles), int(ax), int(ay), 20, 20, 32, 32)

                    #TODO:maze find the ideal block texture size for the map so we dont
                    #          have to do this strange offset
                    #mapImage.copySubImage(blockFiles[0], int(ax), int(ay), 0, 0, 32, 32)
                    self._drawSquare(mapImage, int(ax), int(ay), 10, VBase4D(0.5, 0.5, 0.5, 1.0))

        # create a texture from the map image
        mapTexture = Texture("mapTexture")
        mapTexture.setupTexture(Texture.TT2dTexture, self._maskResolution, self._maskResolution, 1, Texture.TUnsignedByte, Texture.FRgba)
        mapTexture.setMinfilter(Texture.FTLinear)
        mapTexture.load(mapImage)
        mapTexture.setWrapU(Texture.WMClamp)
        mapTexture.setWrapV(Texture.WMClamp)

        mapImage.clear()
        del mapImage

        # put the texture on a card and return it
        cm = CardMaker("map_cardMaker")
        cm.setFrame(-1.0,1.0,-1.0,1.0)
        map = self.attachNewNode(cm.generate())
        map.setTexture(mapTexture, 1)
        return map

    def _createMaskTextureCard(self):
        """
        This will return a NodePath with a card textured with the map mask.  It
        also creates several other members that re needed to change the mask.
        """
        # create and fill empty mask image
        self._maskImage = PNMImage(self._maskResolution, self._maskResolution, 4)
        for x in range(self._maskResolution):
            for y in range(self._maskResolution):
                #maskImage.setXel(x,y,mapImage.getRed(x/13,y/10),mapImage.getGreen(x/13,y/10),mapImage.getBlue(x/13,y/10))
                self._maskImage.setXelA(x,y,0,0,0,1)

        # create the texture for the mask
        self.maskTexture = Texture("maskTexture")
        self.maskTexture.setupTexture(Texture.TT2dTexture, self._maskResolution, self._maskResolution, 1, Texture.TUnsignedByte, Texture.FRgba)
        self.maskTexture.setMinfilter(Texture.FTLinear)
        self.maskTexture.setWrapU(Texture.WMClamp)
        self.maskTexture.setWrapV(Texture.WMClamp)

        self.maskTexture.load(self._maskImage)
        base.graphicsEngine.renderFrame()

        # put the mask texture on a card and return it
        cm = CardMaker("mask_cardMaker")
        cm.setFrame(-1.0,1.0,-1.0,1.0)
        mask = self.attachNewNode(cm.generate())
        mask.setTexture(self.maskTexture, 1)
        mask.setTransparency(1)
        return mask

    def _drawSquare(self, image, ulx, uly, size, color):
        """
        Draws a square on the supplied PNMImage starting at (ulx, uly) with a
        size of "size" and a color of "color".
        """
        x = int(ulx)
        while x <= ulx + size:
            y = int(uly)
            while y <= uly + size:
                if x > 0 and y > 0 and x < image.getXSize() and y < image.getYSize():
                    image.setXelA( x, y, color )
                y += 1
            x += 1

    def destroy(self):
        del self._mazeLayout
        del self._maskResolution
        del self._radius
        del self._revealedCells

        del self._revealFunctions
        del self._revealFunction

        # remove and delete all nodes
        self.map.removeNode()
        del self.map
        self.mask.removeNode()
        del self.mask
        self.maskedLayer.removeNode()
        del self.maskedLayer
        self.visibleLayer.removeNode()
        del self.visibleLayer

        # remove and delete all lists of nodes
        for p in self._players:
            p.removeNode()
        del self._players
        for k in self._locks:
            k.removeNode()
        del self._locks
        for d in self._doors:
            d.removeNode()
        del self._doors

        self._maskImage.clear()
        del self._maskImage

        self.maskTexture.clear()
        del self.maskTexture

        DirectFrame.destroy(self)

    #--- Reveal shape functions ---#############################################

    def _revealSmoothCircle(self, x, y, center):
        length = (Vec2(x,y)-center).length()
        goalAlpha = max(0.0, (length/float(self._radius)) - 0.5)
        self._maskImage.setXelA(
            x,
            y,
            VBase4D( 0.0, 0.0, 0.0, min(self._maskImage.getAlpha(x,y), goalAlpha*2.0))
        )

    def _revealHardCircle(self, x, y, center):
        length = (Vec2(x,y)-center).length()
        if length <= self._radius:
            self._maskImage.setXelA(x,y,VBase4D(0,0,0,0))

    def _revealSquare(self, x, y, center):
        self._maskImage.setXelA(x,y,VBase4D(0,0,0,0))

    #--- Private Functions ---##################################################

    def _drawHole(self, x, y):
        center = Vec2(x, y)
        ul = center - Vec2(self._radius, self._radius)
        lr = center + Vec2(self._radius, self._radius)
        x = int(ul[0])
        while x <= lr[0]:
            y = int(ul[1])
            while y <= lr[1]:
                if x > 0 and y > 0 and x < self._maskResolution and y < self._maskResolution:
                    self._revealFunctions[self._revealFunction](x, y, center)
                y += 1
            x += 1

        self.maskTexture.load(self._maskImage)
        self.mask.setTexture(self.maskTexture, 1)

    def _tileToActualPosition(self, x, y):
        y = len(self._mazeLayout) - y
        cellWidth = self._maskResolution / len(self._mazeLayout[0])
        cellHeight = self._maskResolution / len(self._mazeLayout)
        ax = float(x)/len(self._mazeLayout[0]) * self._maskResolution
        ax += cellWidth
        ay = float(y)/len(self._mazeLayout) * self._maskResolution
        ay += cellHeight
        return ax, ay

    #--- Member Functions ---###################################################

    def addDoor(self, x, y, color):
        """
        Adds a door to the minimap.  This will add a colored dot to the map
        that represents a door.
        --- This is subject to change pending a new player-lock data system. ---
        """
        assert self.notify.debugCall()

        x, y = self._tileToActualPosition(x, y)

        # TODO:maze: replace with door model / texture
        cm = CardMaker("door_cardMaker")
        cm.setFrame(-0.04,0.04,-0.04,0.04)
        #door = self.visibleLayer.attachNewNode(cm.generate())
        door = self.maskedLayer.attachNewNode(cm.generate())

        door.setColor(color)
        door.setPos(x/self._maskResolution*2.0 - 0.97, 0, y/self._maskResolution*-2.0 + 1.02)

        self._doors.append(door)

    def addLock(self, x, y, color):
        """
        Adds a lock to the minimap.  This will add a colored dot to the map
        that represents a lock.
        --- This is subject to change pending a new player-lock data system. ---
        """
        assert self.notify.debugCall()

        x, y = self._tileToActualPosition(x, y)

        # TODO:maze: replace with lock model / texture
        cm = CardMaker("lock_cardMaker")
        cm.setFrame(-0.04,0.04,-0.04,0.04)
        lock = self.maskedLayer.attachNewNode(cm.generate())

        lock.setColor(color)
        lock.setPos(x/self._maskResolution*2.0 - 0.97, 0, y/self._maskResolution*-2.0 + 1.02)

        self._locks.append(lock)

    def addPlayer(self, x, y, color):
        """
        Adds a player to the minimap.  This will add a colored dot to the map
        that represents the player.  The dot location can then be updated
        using the revealCell call.
        --- This is subject to change pending a new player-lock data system. ---
        """
        assert self.notify.debugCall()

        x, y = self._tileToActualPosition(x, y)

        # TODO:maze: replace with player model / texture
        cm = CardMaker("player_cardMaker")
        cm.setFrame(-0.04,0.04,-0.04,0.04)
        player = self.visibleLayer.attachNewNode(cm.generate())

        player.setColor(color)
        player.setPos(x/self._maskResolution*2.0 - 0.97, 0, y/self._maskResolution*-2.0 + 1.02)

        self._players.append(player)

    def revealCell(self, x, y, playerIndex=None):
        """
        Clears out the mask around the given cell and stores that the cell has
        been revealed to prevent attempting to edit the mask for the cell again.
        """

        ax, ay = self._tileToActualPosition(x, y)

        if not self._revealedCells[y][x]:
            self._drawHole(ax, ay)
            self._revealedCells[y][x] = True

        if playerIndex is not None:
            assert(playerIndex < len(self._players))
            self._players[playerIndex].setPos(ax/self._maskResolution*2.0 - 0.97, 0, ay/self._maskResolution*-2.0 + 1.02)

    def revealAll(self):
        """ Clears out all of the mask. """
        for x in range(self._maskResolution):
            for y in range(self._maskResolution):
                self._maskImage.setXelA(x,y,0,0,0,0)

    def reset(self):
        """ Turns all of the mask on, covering the entire map. """
        for x in range(self._maskResolution):
            for y in range(self._maskResolution):
                self._maskImage.setXelA(x,y,0,0,0,1)
