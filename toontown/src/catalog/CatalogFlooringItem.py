from CatalogSurfaceItem import *

# Indicies into Flooring Textures Dictionary
FTTextureName = 0
FTColor = 1
FTBasePrice = 2

# These index numbers are written to the database.  Don't mess with them.
# Also see TTLocalizer.FlooringNames.
FlooringTypes = {
    ## Series 1 ##
    1000 : ("phase_5.5/maps/floor_wood_neutral.jpg",
            CTBasicWoodColorOnWhite, 150),
    1010 : ("phase_5.5/maps/flooring_carpetA_neutral.jpg",
            CTFlatColorDark, 150),
    1020 : ("phase_4/maps/flooring_tile_neutral.jpg",   # In phase 4 because it's also on the PetShopInterior model.
            CTFlatColorDark, 150),
    1030 : ("phase_5.5/maps/flooring_tileB2.jpg", 
            None, 150),
    # Grass, just for fun 
    1040 : ("phase_4/maps/grass.jpg", None, 150),
    # Beige bricks
    1050 : ("phase_4/maps/floor_tile_brick_diagonal2.jpg", None, 150),
    # Red bricks
    1060 : ("phase_4/maps/floor_tile_brick_diagonal.jpg", None, 150),
    # Square beige tiles
    1070 : ("phase_4/maps/plazz_tile.jpg", None, 150),
    # Sidewalk with colors
    1080 : ("phase_4/maps/sidewalk.jpg", CTFlatColorDark, 150),
    # Boardwalk
    1090 : ("phase_3.5/maps/boardwalk_floor.jpg", None, 150),
    # Dirt
    1100 : ("phase_3.5/maps/dustroad.jpg", None, 150),

    ## Series 2 ##
    # Wood Tile
    1110 : ("phase_5.5/maps/floor_woodtile_neutral.jpg",
            CTBasicWoodColorOnWhite, 150),
    # Floor Tile
    1120 : ("phase_5.5/maps/floor_tile_neutral.jpg",
            CTBasicWoodColorOnWhite + CTFlatColorDark, 150),
    # Floor Tile Honeycomb
    1130 : ("phase_5.5/maps/floor_tile_honeycomb_neutral.jpg",
            CTBasicWoodColorOnWhite, 150),

    ## Series 3 ##
    # Water floor
    1140 : ("phase_5.5/maps/UWwaterFloor1.jpg",
            None, 150),

    # Peach conch tile
    1150 : ("phase_5.5/maps/UWtileFloor4.jpg",
            None, 150),

    # Peach shell tile
    1160 : ("phase_5.5/maps/UWtileFloor3.jpg",
            None, 150),
    
    # Sand shell tile
    1170 : ("phase_5.5/maps/UWtileFloor2.jpg",
            None, 150),

    # Sand conch tile
    1180 : ("phase_5.5/maps/UWtileFloor1.jpg",
            None, 150),

    # Sandy floor
    1190 : ("phase_5.5/maps/UWsandyFloor1.jpg",
            None, 150),
    

    ## WINTER HOLIDAY ##
    # Ice cube
    10000 : ("phase_5.5/maps/floor_icecube.jpg", CTWhite, 225),
    10010 : ("phase_5.5/maps/floor_snow.jpg", CTWhite, 225),

    ## St. Patricks Day ##
    # Gold shamrock
    11000 : ("phase_5.5/maps/StPatsFloor1.jpg", CTWhite, 225),
    # Green shamrock
    11010 : ("phase_5.5/maps/StPatsFloor2.jpg", CTWhite, 225),
    }

class CatalogFlooringItem(CatalogSurfaceItem):
    """CatalogFlooringItem

    This represents a texture/color combination for floors.

    """
    
    def makeNewItem(self, patternIndex, colorIndex = None):
        self.patternIndex = patternIndex
        self.colorIndex = colorIndex
        CatalogSurfaceItem.makeNewItem(self)

    def needsCustomize(self):
        # Returns true if the item still needs to be customized by the
        # user (e.g. by choosing a color).
        return self.colorIndex == None

    def getTypeName(self):
        # e.g. "wallpaper", "wainscoting", etc.
        return TTLocalizer.SurfaceNames[STFlooring]

    def getName(self):
        name = TTLocalizer.FlooringNames.get(self.patternIndex)
        if name:
            return name
        return self.getTypeName()

    def getSurfaceType(self):
        # Returns a value reflecting the type of surface this
        # pattern is intended to be applied to.
        return STFlooring

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        frame = self.makeFrame()

        sample = loader.loadModel('phase_5.5/models/estate/wallpaper_sample')
        a = sample.find('**/a')
        b = sample.find('**/b')
        c = sample.find('**/c')

        # Flooring gets applied to the whole thing.
        a.setTexture(self.loadTexture(), 1)
        a.setColorScale(*self.getColor())
        b.setTexture(self.loadTexture(), 1)
        b.setColorScale(*self.getColor())
        c.setTexture(self.loadTexture(), 1)
        c.setColorScale(*self.getColor())

        sample.reparentTo(frame)

##        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogFlooringItem(%s, %s%s)" % (
            self.patternIndex, self.colorIndex,
            self.formatOptionalData(store))

    def getFilename(self):
        return FlooringTypes[self.patternIndex][FTTextureName]

    def compareTo(self, other):
        if self.patternIndex != other.patternIndex:
            return self.patternIndex - other.patternIndex
        return 0

    def getHashContents(self):
        return self.patternIndex

    def getBasePrice(self):
        return FlooringTypes[self.patternIndex][FTBasePrice]

    def loadTexture(self):
        from pandac.PandaModules import Texture
        filename = FlooringTypes[self.patternIndex][FTTextureName]
        texture = loader.loadTexture(filename)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture

    def getColor(self):
        if self.colorIndex == None:
            # If no color index is set yet, use first color in color list
            colorIndex = 0
        else:
            colorIndex = self.colorIndex
        colors = FlooringTypes[self.patternIndex][FTColor]
        if colors:
            if colorIndex < len(colors):
                return colors[colorIndex]
            else:
                print "Warning: colorIndex not in colors. Returning white."
                return CT_WHITE
        else:
            return CT_WHITE

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(self, di, versionNumber, store)
        if versionNumber < 3:
            self.patternIndex = di.getUint8()
        else:
            self.patternIndex = di.getUint16()
        if (versionNumber < 4) or (store & CatalogItem.Customization):
            self.colorIndex = di.getUint8()
        else:
            self.colorIndex = None

        # The following will generate an exception if
        # self.patternIndex is invalid.  The other fields can take
        # care of themselves.
        wtype = FlooringTypes[self.patternIndex]
        
    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.patternIndex)
        if (store & CatalogItem.Customization):
            dg.addUint8(self.colorIndex)

def getFloorings(*indexList):
    # This function returns a list of CatalogFlooringItems
    # The returned items will all need to be customized (i.e
    # have a color chosen by the user.  Until customization, 
    # use a default color index of 0 (if the pattern has a color
    # list) or CT_WHITE if the pattern has no color list
    list = []
    for index in indexList:
        list.append(CatalogFlooringItem(index))
    return list

def getAllFloorings(*indexList):
    # This function returns a list of all possible
    # CatalogFlooringItems (that is, all color variants) for the
    # indicated type index(es).
    list = []
    for index in indexList:
        colors = FlooringTypes[index][FTColor]
        if colors:
            for n in range(len(colors)):
                list.append(CatalogFlooringItem(index, n))
        else:
            list.append(CatalogFlooringItem(index, 0))
    return list

def getFlooringRange(fromIndex, toIndex, *otherRanges):
    # This function returns a list of all possible
    # CatalogFlooringItems (that is, all color variants) for the
    # indicated type index(es).

    # Make sure we got an even number of otherRanges
    assert(len(otherRanges)%2 == 0)

    list = []

    froms = [fromIndex,]
    tos = [toIndex,]

    i = 0
    while i < len(otherRanges):
        froms.append(otherRanges[i])
        tos.append(otherRanges[i+1])
        i += 2
    
    for patternIndex in FlooringTypes.keys():
        for fromIndex, toIndex in zip(froms,tos):
            if patternIndex >= fromIndex and patternIndex <= toIndex:
                colors = FlooringTypes[patternIndex][FTColor]
                if colors:
                    for n in range(len(colors)):
                        list.append(CatalogFlooringItem(patternIndex, n))
                else:
                    list.append(CatalogFlooringItem(patternIndex, 0))
    return list
