from toontown.catalog.CatalogWallpaperItem import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals

wallpaperDict = {}
wallpaperTextures = []
keys = WallpaperTypes.keys()
keys.sort()

for key in keys:
    wallpaperData = WallpaperTypes[key]
    wallTexture = wallpaperData[WTTextureName]
    if not wallpaperDict.has_key(wallTexture):
        wallpaperDict[wallTexture] = key
        wallpaperTextures.append(wallTexture)

borderDict = {}
borderTextures = []
bkeys = BorderTypes.keys()
bkeys.sort()

for key in bkeys:
    borderData = BorderTypes[key]
    borderTexture = borderData[BDTextureName]
    if not borderDict.has_key(borderTexture):
        borderDict[borderTexture] = key
        borderTextures.append(borderTexture)

wallColorList = list(CTFlatColor) + [CT_WHITE,]
borderColorList = list(CTFlatColorDark) + [CT_WHITE,]

class WallpaperDesignPanel(DirectFrame):
    def __init__(self, parent=aspect2d, **kw):
        optiondefs = (
            ('wallpapers',  wallpaperTextures,                 None),
            ('borders',        borderTextures,                 None),
            ('wallColorList',   wallColorList,                 None),
            ('borderColorList', borderColorList,               None),
            ('numColorCols',               10,                 None),
            ('tabletDim',                 0.1,                 None),
            ('image',  DGG.getDefaultDialogGeom(),                 None),
            ('image_scale',          (4,1,2,),                 None),
            ('image_color', ToontownGlobals.GlobalDialogColor, None),
            ('relief',                   None,                 None),
            ('pos',                   (0,1,0),                 None),
            ('scale',                     0.6,                 None),
            )
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectFrame.__init__(self, parent)

        self.currentPicture = None
        self.patternIndex = 0
        self.borderIndex = 0
        self.colorIndex = 0
        self.borderColorIndex = 0
        self.colorFrame = DirectFrame(parent = self,
                                      relief = None,
                                      scale = 2.0,
                                      pos = (-1.7,0,0.2))
        self.colorTablets = []
        self.makeColorTablets()
        # Create inc/dec buttons
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        self.decButton = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/FndsLst_ScrollUp"),
                     gui.find("**/FndsLst_ScrollDN"),
                     gui.find("**/FndsLst_ScrollUp_Rllvr"),
                     gui.find("**/FndsLst_ScrollUp"),
                     ),
            image_scale = (3.0,3.0,-3.0),
            image3_color = Vec4(1,1,1,0.1),
            pos = (1,0,-0.7),
            command = self.prevPattern,
            state = DGG.DISABLED,
            )
        self.incButton = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/FndsLst_ScrollUp"),
                     gui.find("**/FndsLst_ScrollDN"),
                     gui.find("**/FndsLst_ScrollUp_Rllvr"),
                     gui.find("**/FndsLst_ScrollUp"),
                     ),
            image_scale = 3.0,
            image3_color = Vec4(1,1,1,0.1),
            pos = (1,0,0.7),
            command = self.nextPattern,
            )
        
        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        nextUp = guiItems.find('**/arrow_up')
        nextRollover = guiItems.find('**/arrow_Rollover')
        nextDown = guiItems.find('**/arrow_Down')
        prevUp = guiItems.find('**/arrowUp')
        prevDown = guiItems.find('**/arrowDown1')
        prevRollover = guiItems.find('**/arrowRollover')

        self.nextBorder = DirectButton(
            self, relief = None,
            pos = (1.5,0,-0.4),
            scale = 3.0,
            image = [nextUp, nextDown, nextRollover, nextUp],
            image_color = (.9,.9,.9,1),
            image2_color = (1,1,1,1),
            image3_color = (1,1,1,.1),
            command = self.nextBorder)
        self.prevBorder = DirectButton(
            self, relief = None,
            pos = (0.5,0,-0.4),
            scale = 3.0,
            image = [prevUp, prevDown, prevRollover, prevUp],
            image_color = (.9,.9,.9,1),
            image2_color = (1,1,1,1),
            image3_color = (1,1,1,.1),
            command = self.prevBorder)
        
        buttons = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        cancelButtonImage = (buttons.find('**/CloseBtn_UP'),
                             buttons.find('**/CloseBtn_DN'),
                             buttons.find('**/CloseBtn_Rllvr'))
        self.quitButton = DirectButton(
            parent = self,
            relief = None,
            image = cancelButtonImage,
            pos = (1.8,0,0.8),
            scale = 3,
            command = self.destroy)
        self.info = DirectLabel(parent = self,
                                text = 'info', relief = None,
                                pos = (0,0,-0.9), scale = 0.2)
        # Call initialization functions
        self.initialiseoptions(WallpaperDesignPanel)
    def setColorIndex(self, index):
        assert(index < self['wallColorList'])
        self.colorIndex = index
        self.showPicture()
    def setBorderColorIndex(self, index):
        assert(index < self['borderColorList'])
        self.borderColorIndex = index
        self.showPicture()
    def setPatternIndex(self, index):
        self.patternIndex = index
        self.updateButtons()
        assert(self.patternIndex < len(self['wallpapers']))
        self.showPicture()
    def nextPattern(self):
        self.setPatternIndex(self.patternIndex + 1)
    def prevPattern(self):
        self.setPatternIndex(self.patternIndex - 1)
    def setPatternIndex(self, index):
        self.patternIndex = index
        self.updateButtons()
        assert(self.patternIndex < len(self['wallpapers']))
        self.showPicture()
    def nextBorder(self):
        self.setBorderIndex (self.borderIndex + 1)
    def prevBorder(self):
        self.setBorderIndex (self.borderIndex - 1)
    def setBorderIndex(self, index):
        self.borderIndex = index
        self.updateButtons()
        assert(self.borderIndex < len(self['borders']))
        self.showPicture()
    def updateButtons(self):
        numItems = len(self['wallpapers'])
        if self.patternIndex >= (numItems - 1):
            self.patternIndex = numItems - 1
            self.incButton['state'] = DGG.DISABLED
        else:
            self.incButton['state'] = DGG.NORMAL
        if self.patternIndex <= 0:
            self.patternIndex = 0
            self.decButton['state'] = DGG.DISABLED
        else:
            self.decButton['state'] = DGG.NORMAL
        numItems = len(self['borders'])
        if self.borderIndex >= (numItems - 1):
            self.borderIndex = numItems - 1
            self.nextBorder['state'] = DGG.DISABLED
        else:
            self.nextBorder['state'] = DGG.NORMAL
        if self.borderIndex <= 0:
            self.borderIndex = 0
            self.prevBorder['state'] = DGG.DISABLED
        else:
            self.prevBorder['state'] = DGG.NORMAL
    def loadTexture(self):
        filename = self['wallpapers'][self.patternIndex]
        texture = loader.loadTexture(filename)
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        return texture
    def loadBorderTexture(self):
        filename = self['borders'][self.borderIndex]
        if filename:
            texture = loader.loadTexture(filename)
            texture.setMinfilter(Texture.FTLinearMipmapLinear)
            texture.setMagfilter(Texture.FTLinear)
            return texture
        else:
            return self.loadTexture()
    def getColor(self):
        return self['wallColorList'][self.colorIndex]
    def getColor2(self):
        if self.borderIndex == 0:
            return self.getColor()
        else:
            return self['borderColorList'][self.borderColorIndex]
    def getPicture(self):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        sample = loader.loadModel(
            'phase_5.5/models/estate/wallpaper_sample')
        a = sample.find('**/a')
        b = sample.find('**/b')
        c = sample.find('**/c')

        # Wallpaper gets applied to the top 2/3, with the border
        # on the bottom 1/3.
        a.setTexture(self.loadTexture(), 1)
        a.setColorScale(*self.getColor())
        b.setTexture(self.loadTexture(), 1)
        b.setColorScale(*self.getColor())
        c.setTexture(self.loadBorderTexture(), 1)
        c.setColorScale(*self.getColor2())
        return sample
    def showPicture(self):
        index = self.patternIndex
        if self.currentPicture:
            self.currentPicture.removeNode()
        self.currentPicture = self.getPicture()
        self.info['text'] = ("(%d, %d, %d, %d)" % (
            wallpaperDict[self['wallpapers'][self.patternIndex]],
            self.colorIndex,
            borderDict[self['borders'][self.borderIndex]],
            self.borderColorIndex))
        self.currentPicture.reparentTo(self)
        self.currentPicture.setScale(0.6)
        self.currentPicture.setPos(1,0,0)
    def makeColorTablets(self):
        for t in self.colorTablets:
            t.destroy()
        self.colorTablets = []
        dim = self['tabletDim']
        hd = dim/2.0
        index = 0
        xOffset = 0.0
        yOffset = dim
        # Wallpaper colors
        colorList = self['wallColorList']
        for index in range(len(colorList)):
            if (index % self['numColorCols']) == 0:
                xOffset = 0.0
                yOffset -= dim
            color = colorList[index]
            func = PythonUtil.Functor(self.setColorIndex, index)
            l = DirectButton(self.colorFrame, relief = DGG.RAISED,
                             borderWidth = (0.01,0.01), 
                             frameSize = (-hd, hd, -hd, hd),
                             frameColor = (color[0],color[1],color[2],1),
                             pos = (xOffset,0, yOffset),
                             command = func)
            self.colorTablets.append(l)
            xOffset += dim
        # Border colors
        colorList = self['borderColorList']
        xOffset = 0.0
        yOffset -= 0.1
        for index in range(len(colorList)):
            if (index % self['numColorCols']) == 0:
                xOffset = 0.0
                yOffset -= dim
            color = colorList[index]
            func = PythonUtil.Functor(self.setBorderColorIndex, index)
            l = DirectButton(self.colorFrame, relief = DGG.RAISED,
                             borderWidth = (0.01,0.01), 
                             frameSize = (-hd, hd, -hd, hd),
                             frameColor = (color[0],color[1],color[2],1),
                             pos = (xOffset,0, yOffset),
                             command = func)
            self.colorTablets.append(l)
            xOffset += dim


from toontown.catalog.CatalogItemPanel import *
from toontown.catalog.CatalogWallpaperItem import *
def testWallpapers():
    xPos = -0.9
    zPos = 1.2
    itemList = []
    for i in range(12):
        if (i % 4) == 0:
            xPos = -0.9
            zPos -= 0.6
        index = 1000 + i * 100
        item = CatalogItemPanel(item = CatalogWallpaperItem(index),
                                type = CatalogItem.CatalogTypeWeekly,
                                frameSize = (-0.3, 0.3, -0.3, 0.3),
                                relief = DGG.RAISED,
                                pos = (xPos,1,zPos))
        item.load()
        itemList.append(item)
        xPos += 0.6
    return itemList
