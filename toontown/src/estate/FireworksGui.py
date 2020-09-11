from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.DirectScrolledList import *
from toontown.toonbase import ToontownGlobals
import FireworkItemPanel
from direct.directnotify import DirectNotifyGlobal
from toontown.effects import FireworkGlobals
from toontown.effects import Fireworks

# how many items of master list are visible at once in the scrolling list
NUM_ITEMS_SHOWN = 4

class FireworksGui(DirectFrame):
    """FireworksGui

    This class presents the user interface to an individual catalog. It consists of
    a title and a scrolling list of firework items.
    
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("FireworksGui")

    def __init__(self, doneEvent, shootEvent):
        DirectFrame.__init__(self,
                             relief=None,
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = (0, .5, 1, 1),
                             geom_scale = (0.43,1,1.4),
                             pos = (1.1,0,0),
                             )
        self.initialiseoptions(FireworksGui)
        # Send this when we are done so whoever made us can get a callback
        self.doneEvent = doneEvent
        self.shootEvent = shootEvent
        self.itemList = []
        self.type = None
        self.load()

    def load(self):
        # scrolled list wants a list of strings
        itemTypes = [0,1,2,3,4,5]
        itemStrings = []
        for i in itemTypes:
            itemStrings.append(FireworkGlobals.Names[i])
        
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        # make a scrolled list of item panels
        self.panelPicker = DirectScrolledList(
            parent = self,
            items = itemStrings,
            command = self.scrollItem,
            itemMakeFunction = FireworkItemPanel.FireworkItemPanel,
            itemMakeExtraArgs=[self,itemTypes,self.shootEvent],
            numItemsVisible = NUM_ITEMS_SHOWN,
            #pos = (0.5, 0, 0.4),
            # inc and dec are DirectButtons
            incButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_scale = (.5,1,-1),
            incButton_pos = (0,0,-1.08),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.3),
            decButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_scale = (.5,1,1),
            decButton_pos = (0,0,0.20),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.3),
            )
        self.panelPicker.setPos(-.06,0,.42)

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        cancelImageList = (buttons.find('**/CloseBtn_UP'),
                           buttons.find('**/CloseBtn_DN'),
                           buttons.find('**/CloseBtn_Rllvr'))

        self.cancelButton = DirectButton(
            parent = self,
            relief = None,
            image = cancelImageList,
            pos = (0.15, 0, -0.62),
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__cancel,
            )
        buttons.removeNode()

        # create a color picker
        self.hilightColor = VBase4(1,1,1,1)
        self.bgColor = VBase4(.8,.8,.8,1)
        self.colorButtons = []
        for i in Fireworks.colors.keys():
            color = Fireworks.colors[i]
            height = .07
            paddedHeight = .10

            buttonBg = DirectFrame(self,
                                   geom = DGG.getDefaultDialogGeom(),
                                   geom_scale = paddedHeight,
                                   geom_color = self.bgColor,
                                   pos = (.15,0,.50-(paddedHeight+.025)*i),
                                   relief = None,
                                   )
            self.initialiseoptions(buttonBg)
            button = DirectButton(buttonBg,
                                  image = (DGG.getDefaultDialogGeom(),
                                           DGG.getDefaultDialogGeom(),
                                           DGG.getDefaultDialogGeom()),
                                  relief = None,
                                  command = self.__handleColor,
                                  extraArgs = [i])
            button.setScale(height)
            #button.setPos(0.14,0.0,.50-paddedHeight*i)
            button.setColor(color)
            #self.initialiseoptions(button)
            self.colorButtons.append([button,buttonBg])
        self.__initColor(0)
            
    def unload(self):
        # remove all graphical elements
        del self.parent
        del self.itemList
        del self.panelPicker
        
    def update(self):
        # call this to update how many fireworks are left
        pass
    
    def __cancel(self):
        assert(self.notify.debug("transaction cancelled"))
        messenger.send(self.doneEvent)
        return

    def __initColor(self, index):
        # set the initial firework color
        self.colorButtons[index][1]['geom_color'] = self.hilightColor
        self.colorButtons[index][1].setScale(1.2)
        self.curColor = index
        self.fadeColor = 0
        
    def __handleColor(self, index):
        color = Fireworks.colors[index]
        # reset button backgrounds
        for i in range(len(self.colorButtons)):
            self.colorButtons[i][1]['geom_color'] = self.bgColor
            self.colorButtons[i][1].setScale(1)
        
        # enlarge the selected color square
        self.colorButtons[index][1].setScale(1.2)

        # if we are repeatedly clicking the same color, change the background
        # color so we can use it as the fade color for the firework.  Use
        # white as a default
        if index == self.curColor:
            self.fadeColor = (self.fadeColor + 1) % len(Fireworks.colors)
        else:
            self.fadeColor = 0
        self.colorButtons[index][1]['geom_color'] = Fireworks.colors[self.fadeColor]
        self.curColor = index
        
    def scrollItem(self):
        pass
        
    def getCurColor(self):
        return self.curColor, self.fadeColor
        
