from CatalogSurfaceItem import *

# Indicies into Wainscoting Textures Dictionary
WSTTextureName = 0
WSTColor = 1
WSTBasePrice = 2

# These index numbers are written to the database.  Don't mess with them.
# Also see TTLocalizer.WainscotingNames.
WainscotingTypes = {
    # Plain
    1000 : ("phase_3.5/maps/wall_paper_b3.jpg", CTFlatColorDark, 200),
    # Wood version
    1010 : ("phase_5.5/maps/wall_paper_b4_greyscale.jpg",
            CTBasicWoodColorOnWhite, 200),
    # Wood version - series 2
    1020 : ("phase_5.5/maps/wainscotings_neutral.jpg", CTBasicWoodColorOnWhite, 200),
    # Painted, valentines
    1030 : ("phase_3.5/maps/wall_paper_b3.jpg", CTValentinesColors, 200),
    # Painted, underwater colors
    1040 : ("phase_3.5/maps/wall_paper_b3.jpg", CTUnderwaterColors, 200),
    }

class CatalogWainscotingItem(CatalogSurfaceItem):
    """CatalogWainscotingItem

    This represents a texture/color combination for wainscoting.
    
    """
    
    def makeNewItem(self, patternIndex, colorIndex):
        self.patternIndex = patternIndex
        self.colorIndex = colorIndex
        CatalogSurfaceItem.makeNewItem(self)

    def getTypeName(self):
        # e.g. "wallpaper", "wainscoting", etc.
        return TTLocalizer.SurfaceNames[STWainscoting]

    def getName(self):
        name = TTLocalizer.WainscotingNames.get(self.patternIndex)
        if name:
            return name
        return self.getTypeName()

    def getSurfaceType(self):
        # Returns a value reflecting the type of surface this
        # pattern is intended to be applied to.
        return STWainscoting

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

        # Wainscoting gets applied to the bottom 1/3, with the top
        # 2/3 hidden.
        a.hide()
        b.hide()
        c.setTexture(self.loadTexture(), 1)
        c.setColorScale(*self.getColor())

        sample.reparentTo(frame)
        
##        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogWainscotingItem(%s, %s%s)" % (
            self.patternIndex, self.colorIndex,
            self.formatOptionalData(store))

    def getFilename(self):
        return WainscotingTypes[self.patternIndex][WSTTextureName]

    def compareTo(self, other):
        if self.patternIndex != other.patternIndex:
            return self.patternIndex - other.patternIndex
        return self.colorIndex - other.colorIndex

    def getHashContents(self):
        return (self.patternIndex, self.colorIndex)

    def getBasePrice(self):
        return WainscotingTypes[self.patternIndex][WSTBasePrice]

    def loadTexture(self):
        from pandac.PandaModules import Texture
        filename = WainscotingTypes[self.patternIndex][WSTTextureName]
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
        colors = WainscotingTypes[self.patternIndex][WSTColor]
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
        self.colorIndex = di.getUint8()

        # The following will generate an exception if
        # self.patternIndex is invalid.  The other fields can take
        # care of themselves.
        wtype = WainscotingTypes[self.patternIndex]
        
    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.patternIndex)
        dg.addUint8(self.colorIndex)

def getWainscotings(*indexList):
    # This function returns a list of CatalogWainscotingItems
    # The returned items will all need to be customized (i.e
    # have a color chosen by the user.  Until customization, 
    # use a default color index of 0 (if the pattern has a color
    # list) or CT_WHITE if the pattern has no color list
    list = []
    for index in indexList:
        list.append(CatalogWainscotingItem(index))
    return list
    

def getAllWainscotings(*indexList):
    # This function returns a list of all possible
    # CatalogWainscotingItems (that is, all color variants) for the
    # indicated type index(es).
    list = []
    for index in indexList:
        colors = WainscotingTypes[index][WSTColor]
        if colors:
            for n in range(len(colors)):
                list.append(CatalogWainscotingItem(index, n))
        else:
            list.append(CatalogWainscotingItem(index, 0))
    return list
    

def getWainscotingRange(fromIndex, toIndex, *otherRanges):
    # This function returns a list of all possible
    # CatalogWainscotingItems (that is, all color variants) for the
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
    
    for patternIndex in WainscotingTypes.keys():
        for fromIndex, toIndex in zip(froms,tos):
            if patternIndex >= fromIndex and patternIndex <= toIndex:
                colors = WainscotingTypes[patternIndex][WSTColor]
                if colors:
                    for n in range(len(colors)):
                        list.append(CatalogWainscotingItem(patternIndex, n))
                else:
                    list.append(CatalogWainscotingItem(patternIndex, 0))
    return list
