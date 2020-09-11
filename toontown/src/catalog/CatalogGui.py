from direct.gui.DirectGui import *
from pandac.PandaModules import *
import CatalogItemPanel

# how many items of master list are visible at once in the scrolling list
NUM_ITEMS_SHOWN = 3

class CatalogGui:
    """CatalogGui

    This class presents the user interface to an individual catalog. It consists of
    a title and a scrolling list of catalog items.
    
    """

    def __init__(self, type, list=[], parent=None):

        self.type = type
        self.itemList = list
        self.parent = parent

        self.panelPicker = None
        self.frame = DirectFrame(parent=parent, relief=None)
        self.load()

    def show(self):
        self.frame.show()
        
    def hide(self):
        self.frame.hide()

    def load(self):
        # scrolled list wants a list of strings
        itemStrings = []
        for i in range(0, len(self.itemList)):
            itemStrings.append(self.itemList[i].getName())

        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        # make a scrolled list of item panels
        self.panelPicker = DirectScrolledList(
            parent = self.frame,
            items = itemStrings,
            command = self.scrollItem,
            itemMakeFunction = CatalogItemPanel.CatalogItemPanel,
            itemMakeExtraArgs=[self.itemList, self.type],
            numItemsVisible = NUM_ITEMS_SHOWN,
            pos = (0.5, 0, 0.4),
            # inc and dec are DirectButtons
            incButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_scale = (1.3,1.3,-1.3),
            incButton_pos = (0,0,-1.05),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.3),
            decButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_scale = (1.3,1.3,1.3),
            decButton_pos = (0,0,0.25),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.3),
            )
        
        
    def unload(self):
        # remove all graphical elements
        del self.parent
        del self.itemList
        del self.panelPicker
        self.frame.destroy()
    

    def update(self):
        # call this when toon's money count changes to update the buy buttons
        for item in self.panelPicker['items']:
            if (type(item) != type("")):
                item.updateBuyButton()
            
    def scrollItem(self):
        pass
        
