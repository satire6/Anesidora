"""FlowerSpeciesPanel module: contains the FlowerSpeciesPanel class"""

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
#import FishBase
import GardenGlobals
import FlowerPhoto
from toontown.estate import BeanRecipeGui

class FlowerSpeciesPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory("FlowerSpeciesPanel")

    # special methods
    def __init__(self, species=None, itemIndex=0, *extraArgs):
        """
        genus is an integer key into GardenGlobals.PlantAttributes.
        itemIndex is an integer index into the item list (see optiondefs
            in FlowerBrowser).
        
        Create a DirectFrame for displaying the genus and it's species
        """
        assert self.notify.debugStateCall(self)
        flowerGui = loader.loadModel("phase_3.5/models/gui/fishingBook")

        albumGui = flowerGui.find("**/photo_frame1")
        # The picture frame is in the wrong order, should be drawn first (at the back)
        # RAU 2006/08/01 But since now we have a PictureGroup, just move that

        pictureGroup = albumGui.attachNewNode('PictureGroup')
        hideList = ['corner_backs','shadow','bg','corners','picture']
        for name in hideList:
            temp = flowerGui.find("**/%s" % name)
            if not temp.isEmpty():
                temp.wrtReparentTo(pictureGroup)        

        pictureGroup.setPos(0,0,1.0)

        albumGui.find("**/arrows").removeNode()

        optiondefs = (
            ('relief',                                    None, None),
            ('state',                                   DGG.NORMAL, None),
            ('image',                                 albumGui, None),
            ('image_scale',                (0.025,0.025,0.025), None),
            ('image_pos',                            (0, 1, 0), None),
            ('text',                   TTLocalizer.FlowerUnknown, None),
            ('text_scale',                               0.065, None),
            ('text_fg',                        (0.2,0.1,0.0,1), None),
            ('text_pos',                         (-0.5, -0.34), None),
            ('text_font',   ToontownGlobals.getInterfaceFont(), None),
            ('text_wordwrap',                             13.5, None),
            ('text_align',                      TextNode.ALeft, None),            
            )
        # Merge keyword options with default options
        self.defineoptions({}, optiondefs)
        # Initialize superclasses
        DirectFrame.__init__(self)
        self.initialiseoptions(FlowerSpeciesPanel)
        self.flowerPanel = None
        self.species = None
        self.variety = 0
        self.flowerCollection = extraArgs[0]   
        self.setSpecies(int(species))
        self.setScale(1.2)
        
        albumGui.removeNode()
        self.beanRecipeGui = None

    def destroy(self):
        assert self.notify.debugStateCall(self)
        if self.flowerPanel:
            self.flowerPanel.destroy()
            del self.flowerPanel
        self.flowerCollection = None
        self.cleanupBeanRecipeGui()        
        DirectFrame.destroy(self)


    def load(self):
        assert self.notify.debugStateCall(self)
        pass


        
    def setSpecies(self, species):
        assert self.notify.debugStateCall(self)
        if self.species == species:
            return
        self.species = species
        if self.species != None:
            # load the species image
            if self.flowerPanel:
                self.flowerPanel.destroy()
            #f = FishBase.FishBase(self.species, 0, 0)
            varietyToUse = self.flowerCollection.getInitialVariety(self.species)
            self.variety = varietyToUse
            self.flowerPanel = FlowerPhoto.FlowerPhoto(species = self.species, variety=varietyToUse, parent=self)
            #self.flowerPanel.setPos(-0.23, 1, -0.01)
            zAdj = 0.0131
            xAdj = -0.002
            self.flowerPanel.setPos(-0.229 + xAdj, 1,- 0.01 + zAdj)
            # This is carefully placed over the book image.  Please try to keep
            # this in sync with the book position:
            self.flowerPanel.setSwimBounds(-0.2461, 0.2367, -0.207 + zAdj , 0.2664 + zAdj)
            # Light blue-green water background:
            #self.flowerPanel.setSwimColor(0.47, 1.0, 0.99, 1.0)
            # dark green lawn background
            #self.flowerPanel.setSwimColor(0.25, 0.5, 0.25, 1.0)
            # light gray neutral background
            self.flowerPanel.setSwimColor(0.75, 0.75, 0.75, 1.0)

            varietyList = GardenGlobals.getFlowerVarieties(self.species)
            self.speciesLabels = []
            offset = 0.075
            startPos = ((len(varietyList) / 2) * offset)
            if not len(varietyList) % 2:
                # even len's need a little shift down
                startPos -= offset / 2

            for variety in range(len(varietyList)):
                label = DirectButton(
                    parent=self,
                    frameSize = (0,0.445,-0.02,0.04),
                    relief=None, #DGG.RIDGE,
                    #borderWidth = (0.01,0.01),
                    state = DGG.DISABLED,
                    pos = (0.06, 0, startPos - (variety * offset)),
                    text = TTLocalizer.FlowerUnknown,
                    text_fg = (0.2,0.1,0.0,1),
                    text_scale = (0.045, 0.045, 0.45),
                    text_align = TextNode.ALeft,                    
                    text_font = ToontownGlobals.getInterfaceFont(),
                    command = self.changeVariety,
                    extraArgs = [variety],
                    text1_bg = Vec4(1,1,0,1),
                    text2_bg = Vec4(0.5,0.9,1,1),
                    text3_fg = Vec4(0.4,0.8,0.4,1),
                    )
                self.speciesLabels.append(label)
            

    def show(self):
        assert self.notify.debugStateCall(self)
        self.update()
        DirectFrame.show(self)

    def hide(self):
        assert self.notify.debugStateCall(self)
        if self.flowerPanel is not None:
            self.flowerPanel.hide()
        if self.beanRecipeGui is not None:
            self.beanRecipeGui.hide()            
        DirectFrame.hide(self)

    def showRecipe(self):
        if base.localAvatar.flowerCollection.hasSpecies(self.species):
            self['text'] = TTLocalizer.FlowerSpeciesNames[self.species]
            if base.localAvatar.flowerCollection.hasFlower(self.species,self.variety):
                name = GardenGlobals.getFlowerVarietyName(self.species, self.variety)
                recipeKey = GardenGlobals.PlantAttributes[self.species]['varieties'][self.variety][0]
                #name += ' (%s)' % GardenGlobals.Recipes[recipeKey]['beans']
                self['text'] = name
                self.createBeanRecipeGui(GardenGlobals.Recipes[recipeKey]['beans'])
            else:
                self.cleanupBeanRecipeGui()
        else:
            self['text'] = TTLocalizer.FlowerUnknown
            self.cleanupBeanRecipeGui()            
            
    def update(self):
        assert self.notify.debugStateCall(self)
        if base.localAvatar.flowerCollection.hasSpecies(self.species):# and self.flowerPanel is not None:
            self.flowerPanel.show(showBackground=0)
            self['text'] = TTLocalizer.FlowerSpeciesNames[self.species]
        for variety in range(len(GardenGlobals.getFlowerVarieties(self.species))):
            if base.localAvatar.flowerCollection.hasFlower(self.species, variety):
                name = GardenGlobals.getFlowerVarietyName(self.species, variety)
                #recipeKey = GardenGlobals.PlantAttributes[self.species]['varieties'][variety][0]
                #name += ' (%s)' % GardenGlobals.Recipes[recipeKey]['beans']
                self.speciesLabels[variety]['text'] = name
                self.speciesLabels[variety]['state'] = DGG.NORMAL

        self.showRecipe()
                    
    def changeVariety(self, variety):
        #print 'changing variety to %d' % variety
        self.variety = variety
        self.flowerPanel.changeVariety(variety);
        self.flowerPanel.show()
        self.showRecipe()
        

    def createBeanRecipeGui(self, recipe):
        if self.beanRecipeGui:
            self.beanRecipeGui.destroy()
            
        #These are the 3 potential positions on where to put the recipe
        pos1 = (-0.2,0,-0.365) #bottom of page
        #if hasattr(self,'beanRecipeGui1'):
        #    if self.beanRecipeGui1:
        #        self.beanRecipeGui1.destroy()
        #self.beanRecipeGui1 = BeanRecipeGui.BeanRecipeGui(self, recipe, pos = pos1)
        #
        pos2 = (-0.46,0,0.3) #above flower photo
        #if hasattr(self,'beanRecipeGui2'):
        #    if self.beanRecipeGui2:
        #        self.beanRecipeGui2.destroy()
        #self.beanRecipeGui2 = BeanRecipeGui.BeanRecipeGui(self, recipe, pos = pos2)
        #
        pos3 = (-0.46,0,-0.3) #below flower photo
        #if hasattr(self,'beanRecipeGui3'):
        #    if self.beanRecipeGui3:
        #        self.beanRecipeGui3.destroy()
        #self.beanRecipeGui3 = BeanRecipeGui.BeanRecipeGui(self, recipe, pos = pos3)

        #self.beanRecipeGui = BeanRecipeGui.BeanRecipeGui(self, recipe, pos = pos3)

        pos4 = (-0.6,0,-0.27) #below flower photo in aspect2dp coords
        self.beanRecipeGui = BeanRecipeGui.BeanRecipeGui(aspect2dp,
                                                         recipe,
                                                         pos = pos4,
                                                         scale = 1.3,
                                                         frameColor = (0.8, 0.8, 0.8,1.0),
                                                         )

        
        

    def cleanupBeanRecipeGui(self):
        assert self.notify.debugStateCall(self)
        if self.beanRecipeGui:
            self.beanRecipeGui.destroy()
            self.beanRecipeGui = None
        
