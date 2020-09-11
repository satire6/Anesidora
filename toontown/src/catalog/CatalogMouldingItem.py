from CatalogSurfaceItem import *

# Indicies into Moulding Textures Dictionary
MTTextureName = 0
MTColor = 1
MTBasePrice = 2

# These index numbers are written to the database.  Don't mess with them.
# Also see TTLocalizer.MouldingNames.
MouldingTypes = {
    # Wood - Series 1
    1000 : ("phase_3.5/maps/molding_wood1.jpg", CTBasicWoodColorOnWhite, 150),
    # Plain with colors - Series 1
    1010 : ("phase_5.5/maps/bd_grey_border1.jpg", CTFlatColorDark, 150),
    # Dental wood - Series 2
    1020 : ("phase_5.5/maps/dental_Border_wood_neutral.jpg", CTFlatColorDark, 150),
    # Flowers - Series 2
    1030 : ("phase_5.5/maps/littleFlowers_border.jpg", CTWhite, 150),
    1040 : ("phase_5.5/maps/littleFlowers_border_neutral.jpg", CTFlatColorDark, 150),
    # Ladybug - Unused
    1050 : ("phase_5.5/maps/ladybugs2_Border.jpg", CTFlatColorDark, 150),
    # Valentines
    1060 : ("phase_5.5/maps/bd_grey_border1.jpg", CTValentinesColors, 150),
    # Beach
    1070 : ("phase_5.5/maps/bd_grey_border1.jpg", CTUnderwaterColors, 150),
    # Winter String Lights 1
    1080 : ("phase_5.5/maps/tt_t_ara_int_border_winterLights1.jpg", CTWhite, 150),
    # Winter String Lights 2
    1085 : ("phase_5.5/maps/tt_t_ara_int_border_winterLights2.jpg", CTWhite, 150),
    # Winter String Lights 3
    1090 : ("phase_5.5/maps/tt_t_ara_int_border_winterLights3.jpg", CTWhite, 150),
    # Valentines Day - Cupid
    1100 : ("phase_5.5/maps/tt_t_ara_int_border_valentine_cupid.jpg", CTWhite, 150),
    # Valentines Day - Heart 1
    1110 : ("phase_5.5/maps/tt_t_ara_int_border_valentine_heart1.jpg", CTWhite, 150),
    # Valentines Day - Heart 2
    1120 : ("phase_5.5/maps/tt_t_ara_int_border_valentine_heart2.jpg", CTWhite, 150),
    }

class CatalogMouldingItem(CatalogSurfaceItem):
    """CatalogMouldingItem

    This represents a texture/color combination for moulding.
    """
    
    def makeNewItem(self, patternIndex, colorIndex):
        self.patternIndex = patternIndex
        self.colorIndex = colorIndex
        CatalogSurfaceItem.makeNewItem(self)

    def getTypeName(self):
        # e.g. "wallpaper", "wainscoting", etc.
        return TTLocalizer.SurfaceNames[STMoulding]

    def getName(self):
        name = TTLocalizer.MouldingNames.get(self.patternIndex)
        if name:
            return name
        return self.getTypeName()

    def getSurfaceType(self):
        # Returns a value reflecting the type of surface this
        # pattern is intended to be applied to.
        return STMoulding

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.

##        assert (not self.hasPicture)
        self.hasPicture=True
        
        frame = self.makeFrame()

        sample = loader.loadModel('phase_5.5/models/estate/wallpaper_sample')
        a = sample.find('**/a')
        b = sample.find('**/b')
        c = sample.find('**/c')

        # Moulding gets applied to the top 1/3, with the bottom
        # 2/3 hidden.
        a.setTexture(self.loadTexture(), 1)
        a.setColorScale(*self.getColor())
        b.hide()
        c.hide()

        sample.reparentTo(frame)

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogMouldingItem(%s, %s%s)" % (
            self.patternIndex, self.colorIndex,
            self.formatOptionalData(store))

    def getFilename(self):
        return MouldingTypes[self.patternIndex][MTTextureName]

    def compareTo(self, other):
        if self.patternIndex != other.patternIndex:
            return self.patternIndex - other.patternIndex
        return self.colorIndex - other.colorIndex

    def getHashContents(self):
        return (self.patternIndex, self.colorIndex)

    def getBasePrice(self):
        return MouldingTypes[self.patternIndex][MTBasePrice]

    def loadTexture(self):
        from pandac.PandaModules import Texture
        filename = MouldingTypes[self.patternIndex][MTTextureName]
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
        colors = MouldingTypes[self.patternIndex][MTColor]
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
        wtype = MouldingTypes[self.patternIndex]
        
    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.patternIndex)
        dg.addUint8(self.colorIndex)

def getMouldings(*indexList):
    # This function returns a list of CatalogMouldingItems
    # The returned items will all need to be customized (i.e
    # have a color chosen by the user.  Until customization, 
    # use a default color index of 0 (if the pattern has a color
    # list) or CT_WHITE if the pattern has no color list
    list = []
    for index in indexList:
        list.append(CatalogMouldingItem(index))
    return list
    

def getAllMouldings(*indexList):
    # This function returns a list of all possible
    # CatalogMouldingItems (that is, all color variants) for the
    # indicated type index(es).
    list = []
    for index in indexList:
        colors = MouldingTypes[index][MTColor]
        if colors:
            for n in range(len(colors)):
                list.append(CatalogMouldingItem(index, n))
        else:
            list.append(CatalogMouldingItem(index, 0))
    return list
    

def getMouldingRange(fromIndex, toIndex, *otherRanges):
    # This function returns a list of all possible
    # CatalogMouldingItems (that is, all color variants) for the
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
    
    for patternIndex in MouldingTypes.keys():
        for fromIndex, toIndex in zip(froms,tos):
            if patternIndex >= fromIndex and patternIndex <= toIndex:
                colors = MouldingTypes[patternIndex][MTColor]
                if colors:
                    for n in range(len(colors)):
                        list.append(CatalogMouldingItem(patternIndex, n))
                else:
                    list.append(CatalogMouldingItem(patternIndex, 0))
    return list
