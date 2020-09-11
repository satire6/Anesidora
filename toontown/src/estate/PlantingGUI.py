from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.estate import GardenGlobals
from direct.interval.IntervalGlobal import *
from toontown.estate import SpecialsPhoto


USE_SCROLLING_BEAN_BOX = False
JELLY_BEAN_PICKER_HAS_EMPTY_BOX = False
CAN_CHANGE_BEAN_COLOR = True
FORCE_LEFT_TO_RIGHT = True
ONLY_ONE_SPIFFY_BOX_CAN_BE_CLICKED = True
DO_PICKER_INTERVAL = False
PICKER_ALWAYS_UP = True

def loadJellyBean( parent, beanIndex):
    gui = loader.loadModel('phase_5.5/models/estate/jellyBean')
    #bean = gui.find('**/minnieCircle')
    newBean = gui.instanceTo(parent)
    parent.setScale(0.09)
    colors = GardenGlobals.BeanColors[beanIndex]
    #the temp model we're using is a bit dark, so we lghten it up a bit
    parent.setColorScale(colors[0] / 255.0 *1.0,
                         colors[1] /255.0 * 1.0,
                         colors[2] / 255.0 * 1.0,
                         1)


class GenericBoxScrollList(DirectScrolledList):
    """
    This should be able to take a list of either jellybeans,
    or special item images
    """

    def __init__(self, parent , items, **kw):
        # make the scrolling pick list for the fish names
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        #TODO how the heck do I get forceHeight working?
        self.forceHeight = 1
        
        optiondefs = (
            ('parent', parent,    None),
            ('relief', None,    None),
            # inc and dec are DirectButtons
            ('incButton_image', (
                gui.find("**/FndsLst_ScrollUp"),
                gui.find("**/FndsLst_ScrollDN"),
                gui.find("**/FndsLst_ScrollUp_Rllvr"),
                gui.find("**/FndsLst_ScrollUp"),
                ),    None),
            ('incButton_relief',                       None,    None),
            ('incButton_scale',              (1.3,1.3,-1.3),    None),
            ('incButton_pos',                  (0,0,-0.525),    None),
            # Make the disabled button fade out
            ('incButton_image3_color',   Vec4(0.8,0.8,0.8,0.5), None),
            ('decButton_image', (
                gui.find("**/FndsLst_ScrollUp"),
                gui.find("**/FndsLst_ScrollDN"),
                gui.find("**/FndsLst_ScrollUp_Rllvr"),
                gui.find("**/FndsLst_ScrollUp"),
                ),    None),
            ('decButton_relief',                          None, None),
            ('decButton_scale',                  (1.3,1.3,1.3), None),
            ('decButton_pos',                      (0,0,0.525), None),
            # Make the disabled button fade out
            ('decButton_image3_color',   Vec4(0.8,0.8,0.8,0.5), None),
            ('numItemsVisible',                              1, None),
            ('items',                                    items, None),
            ('scrollSpeed',                                1.0, None),
            ('forceHeight',                                  1, None),
            
            #('itemMakeFunction',         FlowerSpeciesPanel.FlowerSpeciesPanel, None),
            #('itemMakeExtraArgs',                         base.localAvatar.flowerCollection, None),
            )
        gui.removeNode()
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectScrolledList.__init__(self, parent, forceHeight = self.forceHeight)
        self.initialiseoptions(GenericBoxScrollList)

        
class BoxItem(NodePath):
    def getHeight(self):
        return 0.05

JellyBeanPickerEndPos = (0, 0, 0.1)
JellyBeanPickerScale = (1.1,1.0,0.13)
if JELLY_BEAN_PICKER_HAS_EMPTY_BOX:
    JellyBeanPickerGeomScale = (1.0,1.0,1.0)
else:
    JellyBeanPickerGeomScale = (0.9,1.0,1.0)

JellyBeanPickerScaleInverse = ( 1.0/JellyBeanPickerScale[0],
                                      1.0/JellyBeanPickerScale[1],
                                      1.0/JellyBeanPickerScale[2]
                                      )
                                      

class JellyBeanPicker(DirectFrame):
    """
    Displays all the jellybeans (including an empty one) and lets the
    choose click one of them
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('PlantingGUI')
   
    def __init__(self, parent,  callBack, boxPosition, **kw):
        assert self.notify.debugStateCall(self)
        self.index = 0
        self.selectedIndex = 0
        self.callBack = callBack
        self.boxPosition = boxPosition

        #optiondefs = ()
        #self.defineoptions(kw, optiondefs)

        DirectFrame.__init__(self,
                             relief = None,
                             state = 'normal',
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = (0.8,0.8,0.8,1.0),
                             geom_scale = JellyBeanPickerGeomScale,
                             #geom_scale = (0.9,1.0,0.13),
                             scale = JellyBeanPickerScale,
                             frameSize = (-1,1,-1,1),
                             pos = (0,0,0),
                             )
        
        self.initialiseoptions(JellyBeanPicker)
        self.jellyBeanBoxList = []
        self.createJellyBeanBoxes()

    def jellyBeanBoxClicked(self, beanIndex):
        assert self.notify.debugStateCall(self)
        if JELLY_BEAN_PICKER_HAS_EMPTY_BOX:
            self.callBack(self.boxPosition, beanIndex)
        else:
            #increment it by 1, since 0 represents the empty box
            self.callBack(self.boxPosition, beanIndex + 1)
            

    def createJellyBeanBox(self, beanIndex, xPos, zPos):
        geomColor = (1,1,1,1)
        state = DGG.NORMAL
        command = self.jellyBeanBoxClicked

        newBox = DirectButton(
                parent = self,
                pos = ( xPos, 0, zPos),
                geom = DGG.getDefaultDialogGeom(),
                geom_scale = (0.1,1.0,0.1),
                geom_color = geomColor,
                scale = JellyBeanPickerScaleInverse,
                relief = None,
                state = state,
                command = command,
                extraArgs = [beanIndex],                
                text = '',
                #text_align = TextNode.ACenter,
                text_pos = (0.0,0.10),
                text_scale = 0.07,
                #text_fg = (1,1,1,1),
                #text_shadow = (0,0,0,1),
                #image = (None,None,None,None),
                text_fg = Vec4(0,0,0,0),
                text1_fg = Vec4(0,0,0,0),
                text2_fg = Vec4(0,0,0,1),
                text3_fg = Vec4(0,0,0,0)
                )
        
        if JELLY_BEAN_PICKER_HAS_EMPTY_BOX:
            #the first box is an empty jelly bean
            if (beanIndex):
                beanParent = newBox.attachNewNode('bean_%d' % (beanIndex-1))
                loadJellyBean(beanParent, beanIndex-1)
        else:
            beanParent = newBox.attachNewNode('bean_%d' % (beanIndex))
            loadJellyBean(beanParent, beanIndex)

            
        self.jellyBeanBoxList.append(newBox)

    def setColorText(self):
        """
        We want the rollover color text to appear only when it is in full scale.
        """
        for beanIndex in range(len(self.jellyBeanBoxList)):
            if JELLY_BEAN_PICKER_HAS_EMPTY_BOX:
                if (beanIndex):
                    box = self.jellyBeanBoxList[beanIndex]
                    box['text'] = TTLocalizer.BeanColorWords[beanIndex-1]
            else:
                box = self.jellyBeanBoxList[beanIndex]
                box['text'] = TTLocalizer.BeanColorWords[beanIndex]
            
    
    def createJellyBeanBoxes(self):
        zCoord = 0 
        xIncrement = 0.095
        xPos = 0
        maxBoxes = len(GardenGlobals.BeanColors)  
        if JELLY_BEAN_PICKER_HAS_EMPTY_BOX:
            #add 1 because of the empty box
            maxBoxes += 1
        startingXCoord = (-0.1 * float(maxBoxes ) / 2.0) + 0.075
        for activeBox in range(maxBoxes):
            xPos = xIncrement * activeBox + startingXCoord
            self.createJellyBeanBox(activeBox, xPos, zCoord)
            
 
class SpiffyBeanBox(DirectButton):
    """
    This bean box will spawn the jelly bean picker and do some spiffy
    animations 
    """
      
    def __init__(self, parent, index, **kw):
        #self.callback = callback
        self.boxIndex = index
        self.selectedIndex = 0

        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        
        DirectButton.__init__(self,
                              parent = parent,
                              
                              )
        self.initialiseoptions(SpiffyBeanBox)
        self.selectedBean = self.attachNewNode('selectedBean')

        
    def getSelectedIndex(self):
        if hasattr(self,"selectedIndex"):
            return self.selectedIndex
        return 0
    
    def setSelectedIndex(self, newIndex):
        self.selectedIndex = newIndex
        self.selectedBean.removeNode()        
        self.selectedBean = self.attachNewNode('selectedBean')        
        if newIndex:
            #subtract 1 to get the real value, since 0 is an empty box
            newIndex -= 1
            loadJellyBean(self.selectedBean, newIndex)
        

class PlantingGUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlantingGUI')    
    def __init__(self, doneEvent, specialBoxActive = False):
        if specialBoxActive:
            instructions = TTLocalizer.GardeningChooseBeansItem
            instructionsPos = (0, 0.4)
        else:
            instructions = TTLocalizer.GardeningChooseBeans
            instructionsPos = (0, 0.35)
            
        DirectFrame.__init__(self,
                             relief = None,
                             state = 'normal',
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = ToontownGlobals.GlobalDialogColor,
                             #geom_scale = (2.0,1,1.5),
                             geom_scale = (1.5,1.0,1.0),
                             frameSize = (-1,1,-1,1),
                             pos = (0,0,0),
                             text = instructions,
                             text_wordwrap = 20,
                             text_scale = .08,
                             text_pos = instructionsPos,
                             )
        self.initialiseoptions(PlantingGUI)

        # Send this when we are done so whoever made us can get a callback
        self.doneEvent = doneEvent

        # Init buttons
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                       buttons.find('**/ChtBx_OKBtn_DN'),
                       buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelImageList = (buttons.find('**/CloseBtn_UP'),
                           buttons.find('**/CloseBtn_DN'),
                           buttons.find('**/CloseBtn_Rllvr'))
        resetImageList = (buttons.find('**/CloseBtn_UP'),
                           buttons.find('**/CloseBtn_DN'),
                           buttons.find('**/CloseBtn_Rllvr'))        
        self.cancelButton = DirectButton(
            parent = self,
            relief = None,
            image = cancelImageList,
            #pos = (0.3, 0, -0.58),
            pos = (-0.3, 0, -0.35),
            text = TTLocalizer.PlantingGuiCancel,
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__cancel,
            )
        self.okButton = DirectButton(
            parent = self,
            relief = None,
            image = okImageList,
            #pos = (0.6, 0, -0.58),
            pos = (0.3, 0, -0.35),
            text = TTLocalizer.PlantingGuiOk,
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__doPlant,
            )
        self.resetButton = DirectButton(
            parent = self,
            relief = None,
            image = resetImageList,
            pos = (0.0, 0, -0.35),
            text = TTLocalizer.PlantingGuiReset,
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__reset,
            )        

        buttons.removeNode()
        
        self.availableBoxes = base.localAvatar.getBoxCapability()
        self.maxBoxes = GardenGlobals.getNumberOfShovelBoxes()
        self.activeBoxesList = []
        self.specialBox = None
        self.specialBoxActive = specialBoxActive

        self.boxList = []
        self.jellyBeanPicker = None
        self.jellyBeanPickerInterval = None

        self.createBoxes()

        #piggy bank code adapted from CatalogScreen.py
        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        # Jellybean indicator
        self.beanBank = DirectLabel(
            self, relief = None,
            image = guiItems.find('**/bean_bank'),
            text = str(base.localAvatar.getMoney() +
                       base.localAvatar.getBankMoney()),
            text_align = TextNode.ARight,
            text_scale = 0.11,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_pos = (0.75,-0.81),
            text_font = ToontownGlobals.getSignFont(),
            pos = (-0.85, 0, 0.2),
            scale = (0.5)
            )
        self.matchBoxesToAvailableMoney()

        if PICKER_ALWAYS_UP:
            self.spiffyBeanBoxClicked(0)

    def destroy(self):
        if self.boxList:
            for box in self.boxList:
                box.destroy()
        self.boxList = []
        DirectFrame.destroy(self)
        self.doneEvent = None
        if self.jellyBeanPickerInterval:
            self.jellyBeanPickerInterval.finish()
        self.jellyBeanPickerInterval = None
        if self.jellyBeanPicker:
            self.jellyBeanPicker.destroy()
        self.jellyBeanPicker = None
        if hasattr(self,'specialPhotoList') and  self.specialPhotoList:
            for photo in self.specialPhotoList:
                photo.destroy()
            self.specialPhotoList = []

    def __cancel(self):
        assert(self.notify.debug("transaction cancelled"))
        messenger.send(self.doneEvent, [0,"",-1])

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')

    def __reset(self):
        assert(self.notify.debug("resetting beans"))
        if self.jellyBeanPicker:
            self.jellyBeanPicker.destroy()        
        for box in self.boxList:
            box.setSelectedIndex(0)

        self.beanBank['text'] = str (base.localAvatar.getMoney() +
                                     base.localAvatar.getBankMoney())
        self.matchBoxesToAvailableMoney()

        if PICKER_ALWAYS_UP:
            self.spiffyBeanBoxClicked(0)

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')            

    def getRecipeStr(self):
        """
        get the text equiv of these beans
        """
        retval = ""
        for box in self.boxList:
            beanIndex = box.getSelectedIndex()
            if beanIndex:
                #subtract 1 to get the real value, since 0 is an empty box
                beanIndex -= 1
                beanLetter = GardenGlobals.BeanColorLetters[beanIndex]
                retval += beanLetter

        return retval
            

    def __doPlant(self):
        recipeStr = self.getRecipeStr()
        selectedSpecial = self.specialButton.getSelectedIndex()
        selectedSpecial -= 1
        messenger.send(self.doneEvent, [1, recipeStr, selectedSpecial])

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')

    def createBoxes(self):
        zCoord = - 0.15
        xIncrement = 0.1
        xPos = 0
        startingXCoord = (-0.1 * float(self.maxBoxes ) / 2.0)   + 0.05       
        for activeBox in range(self.availableBoxes):
            xPos = xIncrement * activeBox + startingXCoord
            if USE_SCROLLING_BEAN_BOX:
                self.createScrollingBeanBox(activeBox, xPos, zCoord, True)
            else:
                self.createSpiffyBeanBox(activeBox, xPos, zCoord, True)            


        for disabledBox in range(self.availableBoxes, self.maxBoxes):
            xPos = xIncrement * disabledBox + startingXCoord
            if USE_SCROLLING_BEAN_BOX:
                self.createScrollingBeanBox(disabledBox, xPos, zCoord, False)
            else:
                self.createSpiffyBeanBox(disabledBox, xPos, zCoord, False)
 

        xPos += xIncrement * 2
        self.createSpecialBox(xPos,zCoord)

    def createSpecialBox(self, xPos, zPos,):
        """
        create the special Box
        """
        geomColor = (1,1,1,1)
        if not self.specialBoxActive:
            geomColor = (0.5,0.5,0.5,1)

        geomScaleX = 0.2
        geomScaleZ = 0.2

        self.specialButtonFrame = DirectFrame(
            parent = self,
            pos = ( xPos, 0, zPos),
            geom = DGG.getDefaultDialogGeom(),
            geom_scale = (geomScaleX,1.0,geomScaleZ),
            geom_color = geomColor,
            relief = None,
            )                  

        items = []
        if self.specialBoxActive:
            #TODO fill items with the images of the special items he can plant
            gardenSpecials = base.localAvatar.getGardenSpecials()
            
            tempItem =  BoxItem(self.attachNewNode('blankSpecial'))
            items.append(tempItem)

            self.specialPhotoList = []
            for item in gardenSpecials:

                tempItem =  BoxItem(self.specialButtonFrame.attachNewNode('temp1'))
                specialsPhoto = SpecialsPhoto.SpecialsPhoto(item[0], parent = tempItem)
                #self.specialsPhoto.setBackBounds(-0.3, 0.3, -0.235, 0.25)
                #self.specialsPhoto.setBackBounds(-0.3, 0.3, -0.235, 0.25)
                specialsPhoto.setBackBounds(  - geomScaleX / 2.0,
                                                   geomScaleX / 2.0,
                                                   - geomScaleZ / 2.0,
                                                   geomScaleZ / 2.0
                                                  )
                
                # Parchment paper background:
                specialsPhoto.setBackColor(1.0, 1.0, 1.0, 1.0)
                
                items.append(tempItem)
                self.specialPhotoList.append(specialsPhoto)

        self.specialButton = GenericBoxScrollList(
            self.specialButtonFrame,
            items,
            incButton_pos = (0,0,-0.135),
            incButton_scale = (0.75,1.0,-1.0),
            decButton_pos = (0,0,0.135),
            decButton_scale = (0.75,1.0,1.0),
            command = self.photoSpecialChanged
            )

    def photoSpecialChanged(self):
        """
        This is pretty hacky, but it works.  
        """
        if not hasattr(self,'specialButton'):
            return

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')        
        
        selectedSpecial = self.specialButton.getSelectedIndex()
        if selectedSpecial == 0:
            for photo in self.specialPhotoList:
                photo.hide()
        else:
            #account for empty box
            selectedSpecial -=1
            self.specialPhotoList[selectedSpecial].show()

    def showFirstSpecial(self):
        if len(self.specialButton['items']) > 1:
            self.specialButton.scrollTo(self.specialButton.getSelectedIndex()+1)
            
    def createScrollingBeanBox(self, index, xPos, zPos, active):
        """
        create a bean box with scroll buttons
        """
        geomColor = (1,1,1,1)
        if not active:
            geomColor = (0.5,0.5,0.5,1)

        boxFrame = DirectFrame(
                parent = self,
                pos = ( xPos, 0, zPos),
                geom = DGG.getDefaultDialogGeom(),
                geom_scale = (0.1,1.0,0.1),
                geom_color = geomColor,
                relief = None,
                )
        
        items = []

        if active:
           #TODO fill items with the images of the special items he can plant
            tempItem =  BoxItem(self.attachNewNode('emptyBean'))
            items.append(tempItem)

            for curBean in range(len(GardenGlobals.BeanColors)):
                tempItem =  BoxItem(self.attachNewNode('bean-%d-%d' %(index,curBean)))
                loadJellyBean(tempItem, curBean)
                items.append(tempItem)
            
        box = GenericBoxScrollList(
            boxFrame,
            items,
            incButton_pos = (0,0,-0.07),
            incButton_scale = (0.4,1.0,-1.0),
            decButton_pos = (0,0,0.065),
            decButton_scale = (0.4,1.0,1.0),
            )
        
        self.boxList.append(box)


    def spiffyBeanBoxClicked(self, index):
        assert self.notify.debugStateCall(self)
        
        if self.jellyBeanPicker:
            self.jellyBeanPicker.destroy()

        outOfMoney = int(self.beanBank['text']) <= 0

        if self.boxList[index].getSelectedIndex() == 0 and outOfMoney:
            #don't let them add a new bean
            #TODO some warning sound or text why the picker doesn't come up
            return

        if not CAN_CHANGE_BEAN_COLOR and self.boxList[index].getSelectedIndex():
            #once you pick a bean color you can't change it
            return
        
        self.jellyBeanPicker = JellyBeanPicker(self, self.selectedNewBeanColor, index)
        self.jellyBeanPicker.setPos(*JellyBeanPickerEndPos)

        if DO_PICKER_INTERVAL:
            #always keep the jelly bean picker up
            boxPos = self.boxList[index].getPos()
            self.jellyBeanPicker.setPos(boxPos)
            
            self.jellyBeanPickerInterval = Sequence(
                Parallel(
                    self.jellyBeanPicker.posInterval(
                        duration = 0.3,
                        pos = VBase3(*JellyBeanPickerEndPos)),
                    self.jellyBeanPicker.scaleInterval(
                        duration = 0.3,
                        startScale = VBase3(JellyBeanPickerScale[0]/10.0,
                                            JellyBeanPickerScale[1],
                                            JellyBeanPickerScale[2]),
                        #scale = VBase3(1,1,1))
                        scale = VBase3(*JellyBeanPickerScale)
                    )
                ),
            Func(self.jellyBeanPicker.setColorText)
            )

            
            self.jellyBeanPickerInterval.start()
        else:
            self.jellyBeanPicker.setColorText()


    def matchBoxesToAvailableMoney(self):
        outOfMoney = int(self.beanBank['text']) <= 0
        if outOfMoney:
            #gray out the empty boxes
            for box in self.boxList:
                if box.getSelectedIndex() == 0:
                    box['state']= DGG.DISABLED
                    box.setState()
                    box.setColorScale(0.5,0.5,0.5,1)
        else:
            for box in self.boxList:
                box['state']=DGG.NORMAL
                box.setState()
                box.setColorScale(1,1,1,1)

        if FORCE_LEFT_TO_RIGHT:
            boxIndexToEnable = len(self.getRecipeStr())
            #these are the boxes to the left of the current box
            for i in range(0,boxIndexToEnable):
                box = self.boxList[i]
                if ONLY_ONE_SPIFFY_BOX_CAN_BE_CLICKED:
                    box['state']= DGG.DISABLED
                    box.setState()
                    box.setColorScale(0.875,0.875,0.875,1)
            
            #this is the current box
            if boxIndexToEnable < self.maxBoxes:
                box = self.boxList[boxIndexToEnable]
                if boxIndexToEnable >= self.availableBoxes:
                    box['state']= DGG.DISABLED
                    box.setState()
                    box.setColorScale(0.5,0.5,0.5,1)

            #these are the boxes to the right of the current box
            for i in range (boxIndexToEnable +1, len(self.boxList)):
                box = self.boxList[i]
                box['state']= DGG.DISABLED
                box.setState()
                box.setColorScale(0.5,0.5,0.5,1)
                

    def selectedNewBeanColor(self, boxPosition, beanIndex):
        assert self.notify.debugStateCall(self)
        self.boxList[boxPosition].setSelectedIndex(beanIndex)
        if self.jellyBeanPicker:
            self.jellyBeanPicker.destroy()
            self.jellyBeanPicker = None

        #update the money count
        cost = len ( self.getRecipeStr() )
        newMoney = base.localAvatar.getMoney() + \
                   base.localAvatar.getBankMoney() - \
                   cost
        self.beanBank['text'] = str(newMoney)

        self.matchBoxesToAvailableMoney()

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')
   
        if PICKER_ALWAYS_UP:
            numBoxesFilled = len (self.getRecipeStr())
            if numBoxesFilled < self.availableBoxes:
                self.spiffyBeanBoxClicked(numBoxesFilled)


    def createSpiffyBeanBox(self, index, xPos, zPos, active):
        """
        create a bean box which uses the jelly bean picker
        """
        assert self.notify.debugStateCall(self)
        geomColor = (1,1,1,1)
        state = DGG.NORMAL
        command = self.spiffyBeanBoxClicked
        if not active:
            geomColor = (0.5,0.5,0.5,1)
            command = None
            state = DGG.DISABLED
        
        newBox = SpiffyBeanBox(
                index = index,
                parent = self,
                pos = ( xPos, 0, zPos),
                geom = DGG.getDefaultDialogGeom(),
                geom_scale = (0.1,1.0,0.1),
                geom_color = geomColor,
                relief = None,
                state = state,
                command = command,
                extraArgs = [index]
                )

        self.boxList.append(newBox)
            
