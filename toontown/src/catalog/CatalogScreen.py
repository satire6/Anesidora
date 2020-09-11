from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.DirectScrolledList import *
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
import CatalogItem
import CatalogInvalidItem
from toontown.toonbase import TTLocalizer
import CatalogItemPanel
import CatalogItemTypes
from direct.actor import Actor
import random
from toontown.toon import DistributedToon
from direct.directnotify import DirectNotifyGlobal

NUM_CATALOG_ROWS = 3
NUM_CATALOG_COLS = 2


# Center of square frames used for positioning gui elements
CatalogPanelCenters = [[Point3(-0.95, 0, 0.91),
                        Point3(-0.275, 0, 0.91)],
                       [Point3(-0.95, 0, 0.275),
                        Point3(-0.275, 0, 0.275)],
                       [Point3(-0.95, 0, -0.4),
                        Point3(-0.275, 0, -0.4)]]

CatalogPanelColors = {
    CatalogItemTypes.FURNITURE_ITEM : Vec4(0.733, 0.780, 0.933, 1.000),
    CatalogItemTypes.CHAT_ITEM : Vec4(0.922, 0.922, 0.753, 1.0),
    CatalogItemTypes.CLOTHING_ITEM : Vec4(0.918, 0.690, 0.690, 1.000),
    CatalogItemTypes.EMOTE_ITEM : Vec4(0.922, 0.922, 0.753, 1.0),
    CatalogItemTypes.WALLPAPER_ITEM : Vec4(0.749, 0.984, 0.608, 1.000),
    CatalogItemTypes.WINDOW_ITEM : Vec4(0.827, 0.910, 0.659, 1.000),
    }

class CatalogScreen(DirectFrame):
    """
    CatalogScreen
    This class presents the user interface to an individual's catalog.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogScreen")
    
    def __init__(self, parent=aspect2d, **kw):
        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        background = guiItems.find('**/catalog_background')
        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        guiBack = loader.loadModel('phase_5.5/models/gui/package_delivery_panel')
        optiondefs = (
            # Define type of DirectGuiWidget
            ('scale',            0.667,     None),
            ('pos',        (0,1,0.025),     None),
            ('phone',             None,     None),
            ('doneEvent',         None,     None),
            ('image',       background,     None),
            ('relief',            None,     None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectFrame.__init__(self, parent)
        # Create items
        self.friendGiftIndex = 0 #remove this
        self.friendGiftHandle = None #handle to the friend you are gifting
        self.frienddoId = None #doId of the friend you are gifting
        self.receiverName = "Error Nameless Toon"
        self.friends = {}
        self.family = {}
        self.ffList = []
        self.textRolloverColor = Vec4(1,1,0,1)
        self.textDownColor = Vec4(0.5,0.9,1,1)
        self.textDisabledColor = Vec4(0.4,0.8,0.4,1)
        self.giftAvatar = None; #avatar for gifting
        self.gotAvatar = 0; #flag to know if the gifting avatar has been received
        self.allowGetDetails = 1
        self.load(guiItems, guiButton, guiBack)
        # Call initialization functions
        self.initialiseoptions(CatalogScreen)
        self.enableBackorderCatalogButton()
        self.setMaxPageIndex(self.numNewPages)
        self.setPageIndex(-1)
        self.showPageItems()
        self.hide()
        self.clarabelleChatNP = None
        self.clarabelleChatBalloon = None
        self.gifting = -1
        self.createdGiftGui = None
        self.viewing = None

    def show(self):
        # listen for update requests
        self.accept("CatalogItemPurchaseRequest", self.__handlePurchaseRequest)
        self.accept("CatalogItemGiftPurchaseRequest", self.__handleGiftPurchaseRequest)
        self.accept(localAvatar.uniqueName("moneyChange"), self.__moneyChange)
        self.accept(localAvatar.uniqueName("bankMoneyChange"), self.__bankMoneyChange)
        deliveryText = "setDeliverySchedule-%s" % (base.localAvatar.doId)
        self.accept(deliveryText, self.remoteUpdate)

        # Hide the world since we have a fullscreen interface
        # this will improve our framerate a bit while in the catalog
        render.hide()
        DirectFrame.show(self)
        def clarabelleGreeting(task):
            self.setClarabelleChat(TTLocalizer.CatalogGreeting)
        def clarabelleHelpText1(task):
            self.setClarabelleChat(TTLocalizer.CatalogHelpText1)
        taskMgr.doMethodLater(1.0, clarabelleGreeting, "clarabelleGreeting")
        taskMgr.doMethodLater(12.0, clarabelleHelpText1, "clarabelleHelpText1")
        if hasattr(self, "giftToggle"):
            self.giftToggle['state'] = DGG.DISABLED
            self.giftToggle['text'] = TTLocalizer.CatalogGiftToggleWait
        base.cr.deliveryManager.sendAck()
        self.accept("DeliveryManagerAck", self.__handleUDack)
        taskMgr.doMethodLater(10.0, self.__handleNoAck, "ackTimeOut")

    def hide(self):
        self.ignore("CatalogItemPurchaseRequest")
        self.ignore("CatalogItemGiftPurchaseRequest")
        self.ignore("DeliveryManagerAck")
        taskMgr.remove("ackTimeOut")
        self.ignore(localAvatar.uniqueName("moneyChange"))
        self.ignore(localAvatar.uniqueName("bankMoneyChange"))
        deliveryText = "setDeliverySchedule-%s" % (base.localAvatar.doId)
        self.ignore(deliveryText)
        # Show the world once again
        render.show()
        DirectFrame.hide(self)
    def setNumNewPages(self, numNewPages):
        self.numNewPages = numNewPages
    def setNumBackPages(self, numBackPages):
        self.numBackPages = numBackPages
    def setNumLoyaltyPages(self, numLoyaltyPages):
        self.numLoyaltyPages = numLoyaltyPages
    def setPageIndex(self, index):
        self.pageIndex = index
    def setMaxPageIndex(self, numPages):
        self.maxPageIndex = max(numPages - 1, -1)
    def enableBackorderCatalogButton(self):
        self.backCatalogButton['state'] = DGG.NORMAL
        self.newCatalogButton['state'] = DGG.DISABLED
        self.loyaltyCatalogButton['state'] = DGG.DISABLED
    def enableNewCatalogButton(self):
        self.backCatalogButton['state'] = DGG.DISABLED
        self.newCatalogButton['state'] = DGG.NORMAL
        self.loyaltyCatalogButton['state'] = DGG.DISABLED
    def enableLoyaltyCatalogButton(self):
        self.backCatalogButton['state'] = DGG.DISABLED
        self.newCatalogButton['state'] = DGG.DISABLED
        self.loyaltyCatalogButton['state'] = DGG.NORMAL
        
    def modeBackorderCatalog(self):
        self.backCatalogButton['state'] = DGG.DISABLED
        self.newCatalogButton['state'] = DGG.NORMAL
        self.loyaltyCatalogButton['state'] = DGG.NORMAL
    def modeNewCatalog(self):
        self.backCatalogButton['state'] = DGG.NORMAL
        self.newCatalogButton['state'] = DGG.DISABLED
        self.loyaltyCatalogButton['state'] = DGG.NORMAL
    def modeLoyaltyCatalog(self):
        self.backCatalogButton['state'] = DGG.NORMAL
        self.newCatalogButton['state'] = DGG.NORMAL
        self.loyaltyCatalogButton['state'] = DGG.DISABLED
        
    def showNewItems(self, index = None):
        # If you got here, you do not need to see this text
        taskMgr.remove("clarabelleHelpText1")
        messenger.send('wakeup')        
        self.viewing = 'New'
        self.modeNewCatalog()
        self.setMaxPageIndex(self.numNewPages)
        if self.numNewPages == 0:
            self.setPageIndex(-1)
        elif index is not None:
            self.setPageIndex(index)
        else:
            self.setPageIndex(0)
        self.showPageItems()
    def showBackorderItems(self, index = None):
        # If you got here, you do not need to see this text
        taskMgr.remove("clarabelleHelpText1")
        messenger.send('wakeup')
        self.viewing = 'Backorder'
        self.modeBackorderCatalog()
        self.setMaxPageIndex(self.numBackPages)
        if self.numBackPages == 0:
            self.setPageIndex(-1)
        elif index is not None:
            self.setPageIndex(index)
        else:
            self.setPageIndex(0)
        self.showPageItems()
    def showLoyaltyItems(self, index = None):
        # If you got here, you do not need to see this text
        taskMgr.remove("clarabelleHelpText1")
        messenger.send('wakeup')
        self.viewing = 'Loyalty'
        self.modeLoyaltyCatalog()
        self.setMaxPageIndex(self.numLoyaltyPages)
        if self.numLoyaltyPages == 0:
            self.setPageIndex(-1)
        elif index is not None:
            self.setPageIndex(index)
        else:
            self.setPageIndex(0)
        self.showPageItems()
    def showNextPage(self):
        # If you got here, you do not need to see this text
        taskMgr.remove("clarabelleHelpText1")
        messenger.send('wakeup')
        self.pageIndex = self.pageIndex + 1
        if self.viewing == None:
            self.modeNewCatalog()
            self.viewing == 'New'
        
        
        if ((self.viewing == 'New') and
            (self.pageIndex > self.maxPageIndex) and
            (self.numBackPages > 0)):
            self.showBackorderItems()
        if ((self.viewing == 'New') and
            (self.pageIndex > self.maxPageIndex) and
            (self.numLoyaltyPages > 0)):
            self.showLoyaltyItems()
        elif ((self.viewing == 'Backorder') and
            (self.pageIndex > self.maxPageIndex) and
            (self.numLoyaltyPages > 0)):
            self.showLoyaltyItems()
        else:
            # If viewing backorder catalog, just clamp at last page
            self.pageIndex = min(self.pageIndex, self.maxPageIndex)
            self.showPageItems()
            
    def showBackPage(self):
        # If you got here, you do not need to see this text
        taskMgr.remove("clarabelleHelpText1")
        messenger.send('wakeup')
        self.pageIndex = self.pageIndex - 1
        if ((self.viewing == 'Backorder') and
            (self.pageIndex < 0) and
            (self.numNewPages > 0)):
            self.showNewItems(self.numNewPages - 1)
        elif ((self.viewing == 'Loyalty') and
            (self.pageIndex < 0) and
            (self.numBackPages > 0)):
            self.showBackorderItems(self.numBackPages - 1)
        elif ((self.viewing == 'Loyalty') and
            (self.pageIndex < 0) and
            (self.numNewPages > 0)):
            self.showNewItems(self.numNewPages - 1)
        else:
            self.pageIndex = max(self.pageIndex, -1)
            self.showPageItems()
            
    def showPageItems(self):
        self.hidePages()
        if self.viewing == None:
            self.viewing = 'New'
        if self.pageIndex < 0:
            self.closeCover()
        else:
            # Make sure cover is open
            if self.pageIndex == 0:
                self.openCover()
            # Show appropriate catalog page
            if self.viewing == 'New':
                page = self.pageList[self.pageIndex]
                newOrBackOrLoyalty = 0
            elif self.viewing == 'Backorder':
                page = self.backPageList[self.pageIndex]
                newOrBackOrLoyalty = 1
            elif self.viewing == 'Loyalty':
                page = self.loyaltyPageList[self.pageIndex]
                newOrBackOrLoyalty = 2
            page.show()
            for panel in self.panelDict[page.id()]:
                panel.load()
                if panel.ival:
                    panel.ival.loop()
                self.visiblePanels.append(panel)
            # Now color panels
            pIndex = 0
            randGen = random.Random()
            randGen.seed(
                base.localAvatar.catalogScheduleCurrentWeek +
                (self.pageIndex << 8) +
                (newOrBackOrLoyalty << 16))
            for i in range(NUM_CATALOG_ROWS):
                for j in range(NUM_CATALOG_COLS):
                    if pIndex < len(self.visiblePanels):
                        type = self.visiblePanels[pIndex]['item'].getTypeCode()
                        #self.squares[i][j].setColor(CatalogPanelColors[type])
                        self.squares[i][j].setColor(
                            CatalogPanelColors.values()[
                            randGen.randint(0,len(CatalogPanelColors) - 1)])
                        cs = 0.7 + 0.3 * randGen.random()
                        self.squares[i][j].setColorScale(
                            0.7 + 0.3 * randGen.random(),
                            0.7 + 0.3 * randGen.random(),
                            0.7 + 0.3 * randGen.random(),1)
                    else:
                        self.squares[i][j].setColor(
                            CatalogPanelColors[CatalogItemTypes.CHAT_ITEM])
                        self.squares[i][j].clearColorScale()
                    pIndex += 1
            # get the appropriate text"
            if self.viewing == 'New':
                text = TTLocalizer.CatalogNew
            elif self.viewing == 'Loyalty':
                text = TTLocalizer.CatalogLoyalty
            elif self.viewing == 'Backorder':
                text = TTLocalizer.CatalogBackorder
            self.pageLabel['text'] = text + (' - %d' % (self.pageIndex + 1))
            # Adjust next and backorder buttons
            if self.pageIndex < self.maxPageIndex:
                self.nextPageButton.show()
            elif ((self.viewing == 'New') and (self.numBackPages == 0) and (self.numLoyaltyPages == 0)):
                self.nextPageButton.hide()
            elif ((self.viewing == 'Backorder') and (self.numLoyaltyPages == 0)):
                self.nextPageButton.hide()
            elif (self.viewing == 'Loyalty'):
                self.nextPageButton.hide()
 

            self.adjustForSound()
            self.update()

    def adjustForSound(self):
        """Properly set the state for the snd buttons."""
        # first lets count the number of emote items in the visible panels
        numEmoteItems = 0
        emotePanels = []
        for visIndex in xrange(len(self.visiblePanels)):
            panel = self.visiblePanels[visIndex]
            item = panel['item']
            catalogType = item.getTypeCode()
            if catalogType == CatalogItemTypes.EMOTE_ITEM:
                numEmoteItems += 1
                emotePanels.append(panel)
            else:
                # make sure the buttons don't show
                panel.soundOnButton.hide()
                panel.soundOffButton.hide()
                
        if numEmoteItems == 1:
            # we have exactly 1 item, turn on the sound
            emotePanels[0].handleSoundOnButton()
        elif numEmoteItems > 1:
            # we have more than 1, turn off all the sounds
            for panel in emotePanels:
                panel.handleSoundOffButton()
            
            
    def hidePages(self):
        for page in self.pageList:
            page.hide()
        for page in self.backPageList:
            page.hide()
        for page in self.loyaltyPageList:
            page.hide()
        for panel in self.visiblePanels:
            if panel.ival:
                panel.ival.finish()
        self.visiblePanels = []
    def openCover(self):
        self.cover.hide()
        self.hideDummyTabs()
        self.backPageButton.show()
        self.pageLabel.show()
    def closeCover(self):
        self.cover.show()
        self.showDummyTabs()
        self.nextPageButton.show()
        self.backPageButton.hide()
        self.pageLabel.hide()
        self.hidePages()
    def showDummyTabs(self):
        # Put in 2nd back catalog button which is enabled when in down posn
        if self.numNewPages > 0:
            self.newCatalogButton2.show()
        if self.numBackPages > 0:
            self.backCatalogButton2.show()
        if self.numLoyaltyPages > 0:
            self.loyaltyCatalogButton2.show()
        self.newCatalogButton.hide()
        self.backCatalogButton.hide()
        self.loyaltyCatalogButton.hide()
    def hideDummyTabs(self):
        # Put in 2nd back catalog button which is enabled when in down posn
        self.newCatalogButton2.hide()
        self.backCatalogButton2.hide()
        self.loyaltyCatalogButton2.hide()
        if self.numNewPages > 0:
            self.newCatalogButton.show()
        if self.numBackPages > 0:
            self.backCatalogButton.show()
        if self.numLoyaltyPages > 0:
            self.loyaltyCatalogButton.show()
    def packPages(self, panelList, pageList, prefix):
        i = 0
        j = 0
        numPages = 0
        pageName = prefix + '_page%d' % numPages
        for item in panelList:
            if (i==0) and (j==0):
                numPages += 1
                pageName = prefix + '_page%d' % numPages
                page = self.base.attachNewNode(pageName)
                pageList.append(page)
            item.reparentTo(page)
            item.setPos(CatalogPanelCenters[i][j])
            itemList = self.panelDict.get(page.id(), [])
            itemList.append(item)
            self.panelDict[page.id()] = itemList
            j += 1
            if j == NUM_CATALOG_COLS:
                j = 0
                i += 1
            if i == NUM_CATALOG_ROWS:
                i = 0
        return numPages

        
    def load(self, guiItems, guiButton, guiBack):
        # Initialize variables
        self.pageIndex = -1
        self.maxPageIndex = 0
        self.numNewPages = 0
        self.numBackPages = 5
        self.numLoyaltyPages = 0
        self.viewing = 'New'
        self.panelList = []
        self.backPanelList = []
        self.pageList = []
        self.backPageList = []
        self.loyaltyPanelList = []
        self.loyaltyPageList = []
        self.panelDict = {}
        self.visiblePanels = []
        self.responseDialog = None
        # Create components
        # Background, behind catalog items
        catalogBase = guiItems.find('**/catalog_base')
        self.base = DirectLabel(
            self, relief = None, image = catalogBase)
        # Catalog tabs
        newDown = guiItems.find('**/new1')
        newUp = guiItems.find('**/new2')
        backDown = guiItems.find('**/previous2')
        backUp = guiItems.find('**/previous1')
        giftToggleUp = guiItems.find('**/giftButtonUp')
        giftToggleDown = guiItems.find('**/giftButtonDown')
        giftFriends = guiItems.find('**/gift_names')
        
        lift = 0.40
        smash = 0.80

        self.newCatalogButton = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, 0.45, 1.2),
            image = [newDown, newDown, newDown, newUp],
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,lift),
            pressEffect = 0,
            command = self.showNewItems,
            text = TTLocalizer.CatalogNew,
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (-0.40 -lift, 0.13),
            text3_pos = (-0.40 -lift, 0.1),
            text_scale = 0.08,
            text_fg = (0.353, 0.627, 0.627, 1.000),
            text2_fg = (0.353, 0.427, 0.427, 1.000),
            )
        self.newCatalogButton.hide()
        
        self.newCatalogButton2 = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, 0.45, 1.2),
            image = newDown,
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,lift),
            pressEffect = 0,
            command = self.showNewItems,
            text = TTLocalizer.CatalogNew,# + "2",# + "foo",
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (-0.40 - lift, 0.13),
            text_scale = 0.08,
            text_fg = (0.353, 0.627, 0.627, 1.000),
            text2_fg = (0.353, 0.427, 0.427, 1.000),
            )
        self.newCatalogButton2.hide()
        
        self.backCatalogButton = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, -0.2, 0.40),
            image = [backDown, backDown, backDown, backUp],
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,lift),
            pressEffect = 0,
            command = self.showBackorderItems,
            text = TTLocalizer.CatalogBackorder,
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (0.30 - lift,.132),
            text3_pos = (0.30 -lift,.112),
            text_scale = TTLocalizer.CSbackCatalogButton,
            text_fg = (0.392, 0.549, 0.627, 1.000),
            text2_fg = (0.392, 0.349, 0.427, 1.000),
            )
        self.backCatalogButton.hide()
        
        self.backCatalogButton2 = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, -0.2, 0.40),
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,lift),
            image = backDown,
            pressEffect = 0,
            command = self.showBackorderItems,
            text = TTLocalizer.CatalogBackorder,# + "2",# + "foo",
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (0.30 - lift , .132),
            text_scale = TTLocalizer.CSbackCatalogButton,
            text_fg = (0.392, 0.549, 0.627, 1.000),
            text2_fg = (0.392, 0.349, 0.427, 1.000),
            )
        self.backCatalogButton2.hide()
        
        self.loyaltyCatalogButton = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, -0.85, -0.3),
            image = [newDown, newDown, newDown, newUp],
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,-1.4 + lift),
            pressEffect = 0,
            command = self.showLoyaltyItems,
            text = TTLocalizer.CatalogLoyalty,
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (0.95 - lift,.132),
            text3_pos = (0.95 -lift,.112),
            text_scale = 0.065,
            text_fg = (0.353, 0.627, 0.627, 1.000),
            text2_fg = (0.353, 0.427, 0.427, 1.000),
            )
        self.loyaltyCatalogButton.hide()
        
        self.loyaltyCatalogButton2 = DirectButton(
            self.base, relief = None,
            frameSize = (-0.2, 0.25, -0.85, -0.3),
            image_scale = (1.0, 1.0,smash),
            image_pos = (0.0,0.0,-1.4 + lift),
            image = newDown,
            pressEffect = 0,
            command = self.showLoyaltyItems,
            text = TTLocalizer.CatalogLoyalty,# + "2",# + "foo",
            text_font = ToontownGlobals.getSignFont(),
            text_pos = (0.95 - lift , .132),
            text_scale = 0.065,
            text_fg = (0.353, 0.627, 0.627, 1.000),
            text2_fg = (0.353, 0.427, 0.427, 1.000),
            )
        self.loyaltyCatalogButton2.hide()

        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #Friends list 
        self.__makeFFlist()
                
        if len(self.ffList) > 0:
            self.giftToggle = DirectButton(
                self.base,
                relief = None,
                pressEffect = 0,
                image = (giftToggleUp,
                         giftToggleDown,
                         giftToggleUp,
                         ),
                image_scale = (1.0,1,0.7),
                command = self.__giftToggle,
                #state = DGG.DISABLED,
                text = TTLocalizer.CatalogGiftToggleOff,
                text_font = ToontownGlobals.getSignFont(),
                text_pos = TTLocalizer.CSgiftTogglePos,
                text_scale = TTLocalizer.CSgiftToggle,
                text_fg = (0.353, 0.627, 0.627, 1.000),
                text3_fg = (0.15, 0.3, 0.3, 1.000),
                text2_fg = (0.353, 0.427, 0.427, 1.000),
                image_color = Vec4(1.0, 1.0, 0.2, 1.0),
                image1_color = Vec4(0.9, 0.85, 0.2, 1.0),
                image2_color = Vec4(0.9, 0.85, 0.2, 1.0),
                image3_color = Vec4(0.5, 0.45, 0.2, 1.0),
                )
            self.giftToggle.setPos(0.0,0,-0.035)
            
            #says "this gift is for"             
            self.giftLabel = DirectLabel(
                self.base, relief = None,
                image = giftFriends,
                image_scale = (1.15,1,1.14),
                text = " ",#TTLocalizer.CatalogGiftFor, #HARD
                text_font = ToontownGlobals.getSignFont(),
                text_pos = (1.2,-0.97),
                text_scale = 0.07,
                text_fg = (0.392, 0.549, 0.627, 1.000),
                sortOrder = 100,
                textMayChange = 1,
            )
            self.giftLabel.setPos(-0.15,0,0.080)
            self.giftLabel.hide()
            
            #says the name of the friend the gift is for
            self.friendLabel = DirectLabel(
                self.base, relief = None,
                text = "Friend Name", #HARD
                text_font = ToontownGlobals.getSignFont(),
                text_pos = (-0.25,.132),
                text_scale = 0.068,
                text_align = TextNode.ALeft,
                text_fg = (0.992, 0.949, 0.327, 1.000),
                sortOrder = 100,
                textMayChange = 1,
            )
            self.friendLabel.setPos(0.5,0,-0.42)
            self.friendLabel.hide()
           
            gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
            
            self.scrollList = DirectScrolledList(
                parent = self,
                relief = None,
                # inc and dec are DirectButtons
                incButton_image = (gui.find("**/FndsLst_ScrollUp"),
                                   gui.find("**/FndsLst_ScrollDN"),
                                   gui.find("**/FndsLst_ScrollUp_Rllvr"),
                                   gui.find("**/FndsLst_ScrollUp"),
                                   ),
                incButton_relief = None,
                incButton_pos = (0.0, 0.0, -0.316),
                # Make the disabled button darker
                incButton_image1_color = Vec4(1.0, 0.9, 0.4, 1.0),
                incButton_image3_color = Vec4(1.0, 1.0, 0.6, 0.5),
                incButton_scale = (1.0, 1.0, -1.0),
                decButton_image = (gui.find("**/FndsLst_ScrollUp"),
                                   gui.find("**/FndsLst_ScrollDN"),
                                   gui.find("**/FndsLst_ScrollUp_Rllvr"),
                                   gui.find("**/FndsLst_ScrollUp"),
                                   ),
                decButton_relief = None,
                decButton_pos = (0.0, 0.0, 0.117),
                # Make the disabled button darker
                decButton_image1_color = Vec4(1.0, 1.0, 0.6, 1.0),
                decButton_image3_color = Vec4(1.0, 1.0, 0.6, 0.6),
                
                # itemFrame is a DirectFrame
                itemFrame_pos = (-0.17, 0.0, 0.06),
                itemFrame_relief = None,
                # each item is a button with text on it
                numItemsVisible = 8,
                items = [],
                )
            self.scrollList.setPos(1.2,0,-0.58)
            self.scrollList.setScale(1.5)
            self.scrollList.hide()
     
            # Set up a clipping plane to truncate names that would extend
            # off the right end of the scrolled list.
            clipper = PlaneNode('clipper')
            clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.17, 0, 0)))
            clipNP = self.scrollList.attachNewNode(clipper)
            self.scrollList.setClipPlane(clipNP)
   
            #self.__addFamilyToScrollList()
            #self.__updateScrollList()
            
            self.__makeScrollList()
            
            #self.__setFriendLabelName() #sets the label name
            #self.__loadFriend()
            
            friendId = self.ffList[0]
            self.__chooseFriend(self.ffList[0][0], self.ffList[0][1])
            self.update()
            
            self.createdGiftGui = 1;
            
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for i in range(4):

            self.newCatalogButton.component('text%d' % i).setR(90)
            self.newCatalogButton2.component('text%d' % i).setR(90)
            self.backCatalogButton.component('text%d' % i).setR(90)
            self.backCatalogButton2.component('text%d' % i).setR(90)
            self.loyaltyCatalogButton.component('text%d' % i).setR(90)
            self.loyaltyCatalogButton2.component('text%d' % i).setR(90)
        # Squares
        self.squares = [[],[],[],[]]
        for i in range(NUM_CATALOG_ROWS):
            for j in range(NUM_CATALOG_COLS):
                square = guiItems.find('**/square%d%db' % (i+1,j+1))
                # Use normal state to block rollover of new and prev
                # catalog buttons
                label = DirectLabel(self.base, image = square, relief = None,
                                    state = 'normal')
                self.squares[i].append(label)
        def priceSort(a,b,type):
            priceA = a.getPrice(type)
            priceB = b.getPrice(type)
            return priceB - priceA
            
        itemList = (base.localAvatar.monthlyCatalog +
                     base.localAvatar.weeklyCatalog)
        itemList.sort(lambda a,b: priceSort(a,b,CatalogItem.CatalogTypeWeekly))
        itemList.reverse()
        for item in itemList:
            if isinstance(item, CatalogInvalidItem.CatalogInvalidItem):
                self.notify.warning("skipping catalog invalid item %s" % item)
                continue
            
            #check for loyalty program 
            if item.loyaltyRequirement() != 0:
                self.loyaltyPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeLoyalty,
                    parentCatalogScreen = self,
                    ))
                
            else:
                self.panelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeWeekly,
                    parentCatalogScreen = self,
                    ))
            
        itemList = base.localAvatar.backCatalog
        itemList.sort(
            lambda a,b: priceSort(a,b,CatalogItem.CatalogTypeBackorder))
        itemList.reverse()
        for item in itemList:
            if isinstance(item, CatalogInvalidItem.CatalogInvalidItem):
                self.notify.warning("skipping catalog invalid item %s" % item)
                continue
                                    
            #check for loyalty program 
            if item.loyaltyRequirement() != 0:
                self.loyaltyPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeLoyalty,
                    parentCatalogScreen = self,
                    ))
            else:
                self.backPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeBackorder,
                    parentCatalogScreen = self,
                    ))
            
        numPages = self.packPages(self.panelList, self.pageList, 'new')
        self.setNumNewPages(numPages)
        numPages = self.packPages(self.backPanelList,self.backPageList,'back')
        self.setNumBackPages(numPages)
                
        numPages = self.packPages(self.loyaltyPanelList,self.loyaltyPageList,'loyalty')
        self.setNumLoyaltyPages(numPages)

        currentWeek = base.localAvatar.catalogScheduleCurrentWeek - 1

        if currentWeek < 57:
            seriesNumber = currentWeek / ToontownGlobals.CatalogNumWeeksPerSeries + 1
            weekNumber = currentWeek % ToontownGlobals.CatalogNumWeeksPerSeries + 1
        # Catalog Series 5 & 6 are short. Need some special math here.
        elif currentWeek < 65: 
            seriesNumber = 6
            weekNumber = (currentWeek - 56)
        # All catalogs after 5 & 6 now need to get bumped up by
        # one since the last 13 weeks used two series numbers.
        else:
            seriesNumber = currentWeek / ToontownGlobals.CatalogNumWeeksPerSeries + 2
            weekNumber = currentWeek % ToontownGlobals.CatalogNumWeeksPerSeries + 1

        # Cover.  We find the items we want out of the gui object and
        # reparent them to a new node, partly to ensure the ordering
        # is OK, and partly because we don't necessarily want all the
        # nodes.
        geom = NodePath('cover')
        
        cover = guiItems.find('**/cover')

        # if the catalog has wrapped around, wrap around the images too
        maxSeries = (ToontownGlobals.CatalogNumWeeks / ToontownGlobals.CatalogNumWeeksPerSeries) + 1
        coverSeries = ((seriesNumber - 1) % maxSeries) + 1

        coverPicture = cover.find('**/cover_picture%s' % (coverSeries))
        if not coverPicture.isEmpty():
            coverPicture.reparentTo(geom)

        bottomSquare = cover.find('**/cover_bottom')
        topSquare = guiItems.find('**/square12b2')

        if seriesNumber == 1:
            topSquare.setColor(0.651, 0.404, 0.322, 1.000)
            bottomSquare.setColor(0.655, 0.522, 0.263, 1.000)
        else:
            topSquare.setColor(0.651, 0.404, 0.322, 1.000)
            bottomSquare.setColor(0.655, 0.522, 0.263, 1.000)
            
        bottomSquare.reparentTo(geom)
        topSquare.reparentTo(geom)
        cover.find('**/clarabelle_text').reparentTo(geom)
        cover.find('**/blue_circle').reparentTo(geom)
        cover.find('**/clarabelle').reparentTo(geom)
        cover.find('**/circle_green').reparentTo(geom)
        self.cover = DirectLabel(
            self.base, relief = None, geom = geom)
        # Cover Labels

        self.catalogNumber = DirectLabel(
            self.cover,
            relief = None,
            scale = 0.2,
            pos = (-0.22, 0, -0.33),
            text = "#%d" % weekNumber,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont()
            )
        self.catalogSeries = DirectLabel(
            self.cover,
            relief = None,
            scale = (0.22, 1, 0.18),
            pos = (-0.76, 0, -0.90),
            text = TTLocalizer.CatalogSeriesLabel % seriesNumber,
            text_fg = (0.9, 0.9, 0.4, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont()
            )
        self.catalogSeries.setShxz(0.4)
                
        # Rings, visible when catalog is open
        self.rings = DirectLabel(
            self.base, relief = None, geom = guiItems.find('**/rings'))
        # Frame to hold clarabelle character
        self.clarabelleFrame = DirectLabel(
            self, relief = None,
            image = guiItems.find('**/clarabelle_frame'))
        # Hangup button
        hangupGui = guiItems.find('**/hangup')
        hangupRolloverGui = guiItems.find('**/hangup_rollover')
        self.hangup = DirectButton(
            self, relief = None,
            pos = (1.78, 0, -1.3),
            image = [hangupGui, hangupRolloverGui,
                     hangupRolloverGui, hangupGui],
            text = ["", TTLocalizer.CatalogHangUp, TTLocalizer.CatalogHangUp],
            text_fg = Vec4(1),
            text_scale = 0.07,
            text_pos = (0.0,0.14),
            command = self.hangUp)
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
            )
        # Page turners
        nextUp = guiItems.find('**/arrow_up')
        nextRollover = guiItems.find('**/arrow_Rollover')
        nextDown = guiItems.find('**/arrow_Down')
        prevUp = guiItems.find('**/arrowUp')
        prevDown = guiItems.find('**/arrowDown1')
        prevRollover = guiItems.find('**/arrowRollover')
        self.nextPageButton = DirectButton(
            self, relief = None,
            pos = (-0.1,0,-0.9),
            image = [nextUp, nextDown, nextRollover, nextUp],
            image_color = (.9,.9,.9,1),
            image2_color = (1,1,1,1),
            command = self.showNextPage)
        self.backPageButton = DirectButton(
            self, relief = None,
            pos = (-0.1,0,-0.9),
            image = [prevUp, prevDown, prevRollover, prevUp],
            image_color = (.9,.9,.9,1),
            image2_color = (1,1,1,1),
            command = self.showBackPage)
        self.backPageButton.hide()
        self.pageLabel = DirectLabel(
            self.base, relief = None,
            pos = (-1.33,0,-0.9),
            scale = 0.06,
            text = TTLocalizer.CatalogPagePrefix,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getSignFont(),
            text_align = TextNode.ALeft,
            )
        self.loadClarabelle()

    def loadClarabelle(self):
        # Create a separate reality for clarabelle
        self.cRender = NodePath('cRender')
        # It gets its own camera
        self.cCamera = self.cRender.attachNewNode('cCamera')
        self.cCamNode = Camera('cCam')
        self.cLens = PerspectiveLens()
        self.cLens.setFov(40,40)
        self.cLens.setNear(0.1)
        self.cLens.setFar(100.0)
        self.cCamNode.setLens(self.cLens)
        self.cCamNode.setScene(self.cRender)
        self.cCam = self.cCamera.attachNewNode(self.cCamNode)

        self.cDr = base.win.makeDisplayRegion(0.58, 0.82, 0.53, 0.85)
        self.cDr.setSort(1)
            
        self.cDr.setClearDepthActive(1)
        self.cDr.setClearColorActive(1)
        self.cDr.setClearColor(Vec4(0.3,0.3,0.3,1))
        self.cDr.setCamera(self.cCam)

        # Add Clarabelle model
        self.clarabelle = Actor.Actor("phase_5.5/models/char/Clarabelle-zero",
                                      { "listen" : "phase_5.5/models/char/Clarabelle-listens" } )
        self.clarabelle.loop("listen")

        # Force her eyes to render back-to-front, by the simple
        # expedient of parenting them to the fixed bin in order.
        self.clarabelle.find('**/eyes').setBin('fixed', 0)
        self.clarabelle.find('**/pupilL').setBin('fixed', 1)
        self.clarabelle.find('**/pupilR').setBin('fixed', 1)
        self.clarabelle.find('**/glassL').setBin('fixed', 2)
        self.clarabelle.find('**/glassR').setBin('fixed', 2)

        # Get the switchboard too.
        switchboard = loader.loadModel("phase_5.5/models/estate/switchboard")
        switchboard.reparentTo(self.clarabelle)
        switchboard.setPos(0, -2, 0)
        
        # self.clarabelle = Char.Char()
        # clarabelleDNA = CharDNA.CharDNA()
        # clarabelleDNA.newChar('cl')
        # self.clarabelle.setDNA(clarabelleDNA)
        # self.clarabelle.hideName()
        self.clarabelle.reparentTo(self.cRender)
        self.clarabelle.setPosHprScale(-0.56, 6.43, -3.81,
                                       121.61, 0.00, 0.00,
                                       1.00, 1.00, 1.00)
        # Match up existing gui frame
        self.clarabelleFrame.setPosHprScale(-0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00,
                                            1.00, 1.00, 1.00)
    def reload(self):
        for panel in (self.panelList + self.backPanelList + self.loyaltyPanelList):
            panel.destroy()
        def priceSort(a,b,type):
            priceA = a.getPrice(type)
            priceB = b.getPrice(type)
            return priceB - priceA
        # Initialize variables
        self.pageIndex = -1
        self.maxPageIndex = 0
        self.numNewPages = 0
        self.numBackPages = 5
        self.numLoyaltyPages = 0
        self.viewing = 'New'
        self.panelList = []
        self.backPanelList = []
        self.loyaltyList = []
        self.pageList = []
        self.backPageList = []
        self.loyaltyPanelList = []
        self.loyaltyPageList = []
        self.panelDict = {}
        self.visiblePanels = []
        itemList = (base.localAvatar.monthlyCatalog +
                     base.localAvatar.weeklyCatalog)
        itemList.sort(lambda a,b: priceSort(a,b,CatalogItem.CatalogTypeWeekly))
        itemList.reverse()
        for item in itemList:
            if item.loyaltyRequirement() != 0:
                self.loyaltyPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeLoyalty,
                    parentCatalogScreen = self,
                    ))
                
            else:
                self.panelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeWeekly
                    ))
        itemList = base.localAvatar.backCatalog
        itemList.sort(
            lambda a,b: priceSort(a,b,CatalogItem.CatalogTypeBackorder))
        itemList.reverse()
        for item in itemList:
            if item.loyaltyRequirement() != 0:
                self.loyaltyPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeLoyalty,
                    parentCatalogScreen = self,
                    ))
                
            else:
                self.backPanelList.append(
                    CatalogItemPanel.CatalogItemPanel(
                    parent = hidden,
                    item=item,
                    type=CatalogItem.CatalogTypeBackorder
                    ))
        numPages = self.packPages(self.panelList, self.pageList, 'new')
        self.setNumNewPages(numPages)
        numPages = self.packPages(self.backPanelList,self.backPageList,'back')
        self.setNumBackPages(numPages)
        
        numPages = self.packPages(self.loyaltyPanelList,self.loyaltyPageList,'loyalty')
        self.setNumLoyaltyPages(numPages)

        seriesNumber = (base.localAvatar.catalogScheduleCurrentWeek - 1) / ToontownGlobals.CatalogNumWeeksPerSeries + 1
        self.catalogSeries['text'] = Localizer.CatalogSeriesLabel % seriesNumber
        weekNumber = (base.localAvatar.catalogScheduleCurrentWeek - 1) % ToontownGlobals.CatalogNumWeeksPerSeries + 1
        self.catalogNumber['text'] = "#%d" % weekNumber
        self.enableBackorderCatalogButton()
        self.setMaxPageIndex(self.numNewPages)
        self.setPageIndex(-1)
        self.showPageItems()
        
    def unload(self):
        taskMgr.remove("clearClarabelleChat")
        taskMgr.remove("postGoodbyeHangUp")
        taskMgr.remove("clarabelleGreeting")
        taskMgr.remove("clarabelleHelpText1")
        taskMgr.remove("clarabelleAskAnythingElse")
        if self.giftAvatar:
            base.cr.cancelAvatarDetailsRequest(self.giftAvatar)
        # Make sure to remove Hook
        self.hide()
        # remove all graphical elements
        self.destroy()
        # Clean up variables
        del self.base
        del self.squares
        for panel in (self.panelList + self.backPanelList + self.loyaltyPanelList):
            panel.destroy()
        del self.panelList
        del self.backPanelList
        del self.cover
        del self.rings
        del self.clarabelleFrame
        del self.hangup
        del self.beanBank
        del self.nextPageButton
        del self.backPageButton
        del self.newCatalogButton
        del self.newCatalogButton2
        del self.backCatalogButton
        del self.backCatalogButton2
        del self.loyaltyCatalogButton
        del self.loyaltyCatalogButton2
        
        del self.pageLabel
        if self.createdGiftGui:
            del self.giftToggle
            del self.giftLabel
            del self.friendLabel
            del self.scrollList
        self.unloadClarabelle()
        # delete dialog (if present)
        if self.responseDialog:
            self.responseDialog.cleanup()
            self.responseDialog = None
            
        if self.giftAvatar:
            if hasattr(self.giftAvatar, 'doId'):                
                self.giftAvatar.delete()
            else:
                self.giftAvatar = None

    def unloadClarabelle(self):
        base.win.removeDisplayRegion(self.cDr)
        del self.cRender
        del self.cCamera
        del self.cCamNode
        del self.cLens
        del self.cCam
        del self.cDr
        self.clarabelle.cleanup()
        del self.clarabelle

    def hangUp(self):
        self.setClarabelleChat(random.choice(TTLocalizer.CatalogGoodbyeList))
        # Flip to the front cover and hide the arrow and tabs
        # so you can not get out of this mode. We do not want people
        # purchasing items after hanging up
        self.setPageIndex(-1)
        self.showPageItems()
        self.nextPageButton.hide()
        self.backPageButton.hide()
        self.newCatalogButton.hide()
        self.newCatalogButton2.hide()
        self.backCatalogButton.hide()
        self.backCatalogButton2.hide()
        self.loyaltyCatalogButton.hide()
        self.loyaltyCatalogButton2.hide()
        self.hangup.hide()

        # No more helpful text
        taskMgr.remove("clarabelleGreeting")
        taskMgr.remove("clarabelleHelpText1")
        taskMgr.remove("clarabelleAskAnythingElse")
        
        def postGoodbyeHangUp(task):
            messenger.send(self['doneEvent'])
            self.unload()
        taskMgr.doMethodLater(1.5, postGoodbyeHangUp, "postGoodbyeHangUp")
        
    def remoteUpdate(self):
        #print("remoteupdate")
        #print self.gifting
        self.update()

    # button handlers
    def update(self, lock = 0):#, giftActivate = 0):
        #print("update")
        if not hasattr(self.giftAvatar, 'doId'):
            if self.gifting == 1:
                self.__giftToggle()
        # Update amount in jellybean bank if the catalog is still open
        if hasattr(self, "beanBank"):
            self.beanBank['text'] = str(base.localAvatar.getTotalMoney())
            # call this when toon's money count changes to update the buy buttons
            #print lock
            if lock == 0:
                for item in (self.panelList + self.backPanelList + self.loyaltyPanelList):
                    if (type(item) != type("")):
                    #item.updateButtons(giftActivate)

                        item.updateButtons(self.gifting)
                    #item.updateBuyButton()
                    #item.updateGiftButton(giftActivate)
                
    def __handlePurchaseRequest(self, item):
        # ask the user to customize this purchase (if necessary) and
        # then ask AI to make the purchase.
        item.requestPurchase(self['phone'], self.__handlePurchaseResponse)
        # If you are buying something else, she should not say this
        taskMgr.remove("clarabelleAskAnythingElse")
        
    def __handleGiftPurchaseRequest(self, item):
        # ask the user to customize this purchase (if necessary) and
        # then ask AI to make the purchase.
        #friendPair = base.localAvatar.friendsList[self.friendGiftIndex]
        #frienddoId = base.cr.identifyFriend(friendPair[0]).getDoId() 
        item.requestGiftPurchase(self['phone'], self.frienddoId,self.__handleGiftPurchaseResponse)
        # If you are buying something else, she should not say this
        taskMgr.remove("clarabelleAskAnythingElse")

    def __handlePurchaseResponse(self, retCode, item):
        # AI has returned the status of the purchase in retCode
        if retCode == ToontownGlobals.P_UserCancelled:
            # No big deal; the user bailed.
            return
        self.setClarabelleChat(item.getRequestPurchaseErrorText(retCode),
                               item.getRequestPurchaseErrorTextTimeout())
        """
        self.responseDialog = TTDialog.TTDialog(
            style = TTDialog.Acknowledge,
            text = item.getRequestPurchaseErrorText(retCode),
            text_wordwrap = 15,
            fadeScreen = 1,
            command = self.__clearDialog,
            )
        """
        
    def __handleGiftPurchaseResponse(self, retCode, item):
        # AI has returned the status of the purchase in retCode
        if retCode == ToontownGlobals.P_UserCancelled:
            # No big deal; the user bailed.
            return
        if self.isEmpty() or self.isHidden():
            # the user hung up the phone before we got the uberdog response
            return
        self.setClarabelleChat(item.getRequestGiftPurchaseErrorText(retCode) % (self.receiverName));
        self.__loadFriend()

        def askAnythingElse(task):
            self.setClarabelleChat(TTLocalizer.CatalogAnythingElse)
        
        if retCode >= 0:
            # success: update catalog screen and buttons
            # After a while, have Clarabelle ask if there is anything else you would like
            taskMgr.doMethodLater(8, askAnythingElse, "clarabelleAskAnythingElse")
            
            
    def __clearDialog(self, event):
        self.responseDialog.cleanup()
        self.responseDialog = None

    def setClarabelleChat(self, str, timeout=6):
        self.clearClarabelleChat()
        if not self.clarabelleChatBalloon:
            self.clarabelleChatBalloon = loader.loadModel("phase_3/models/props/chatbox.bam")
        self.clarabelleChat = ChatBalloon(self.clarabelleChatBalloon.node())
        chatNode = self.clarabelleChat.generate(
            str,
            ToontownGlobals.getInterfaceFont(),
            10,
            Vec4(0,0,0,1),
            Vec4(1,1,1,1),
            0,
            0,
            0,
            NodePath(),
            0,
            0,
            NodePath(),
            )
        self.clarabelleChatNP = self.attachNewNode(chatNode,1000)
        self.clarabelleChatNP.setScale(0.08)
        self.clarabelleChatNP.setPos(0.7,0,0.6)
        if timeout:
            taskMgr.doMethodLater(timeout, self.clearClarabelleChat, "clearClarabelleChat")
        
    def clearClarabelleChat(self, task=None):
        # Clean up old chat
        taskMgr.remove("clearClarabelleChat")
        if self.clarabelleChatNP:
            self.clarabelleChatNP.removeNode()
            self.clarabelleChatNP = None
            del self.clarabelleChat
        

    def __moneyChange(self, money):
        if self.gifting > 0:
            self.update(1)
        else:
            self.update(0)
        #print ("__moneyChange")

    def __bankMoneyChange(self, bankMoney):
        if self.gifting > 0:
            self.update(1)
        else:
            self.update(0)
        #print ("__bankMoneyChange")

    def checkFamily(self, doId):
        test = 0
        for familyMember in base.cr.avList:
            if familyMember.id == doId:
                test = 1
        return test
        
        
    def __makeFFlist(self):
        for familyMember in base.cr.avList:
            if familyMember.id != base.localAvatar.doId:
                newFF = (familyMember.id, familyMember.name, NametagGroup.CCNonPlayer)
                self.ffList.append(newFF)
        for friendPair in base.localAvatar.friendsList:
            friendId, flags = friendPair
            #print "adding friend"
            handle = base.cr.identifyFriend(friendId)
            if handle and not self.checkFamily(friendId): 
                if hasattr(handle, 'getName'):            
                    colorCode = NametagGroup.CCSpeedChat
                    if (flags & ToontownGlobals.FriendChat):
                        colorCode = NametagGroup.CCFreeChat
                    newFF = (friendPair[0], handle.getName(), colorCode)
                    self.ffList.append(newFF)
                else:
                    self.notify.warning("Bad Handle for getName in makeFFlist")
        hasManager = hasattr(base.cr, "playerFriendsManager")
        if hasManager:
            for avatarId in base.cr.playerFriendsManager.getAllOnlinePlayerAvatars():
                handle = base.cr.playerFriendsManager.getAvHandleFromId(avatarId)
                playerId = base.cr.playerFriendsManager.findPlayerIdFromAvId(avatarId)
                playerInfo = base.cr.playerFriendsManager.getFriendInfo(playerId)
                freeChat = playerInfo.understandableYesNo
                if handle and not self.checkFamily(avatarId): 
                    if hasattr(handle, 'getName'):            
                        colorCode = NametagGroup.CCSpeedChat
                        if freeChat:
                            colorCode = NametagGroup.CCFreeChat
                        newFF = (avatarId, handle.getName(), colorCode)
                        self.ffList.append(newFF)
                    else:
                        self.notify.warning("Bad Handle for getName in makeFFlist")
        #import pdb; pdb.set_trace()
            
    def __makeScrollList(self):
        for ff in self.ffList:
            ffbutton = self.makeFamilyButton(ff[0], ff[1], ff[2])
            if ffbutton:
                #print "adding button"
                self.scrollList.addItem(ffbutton, refresh=0)
                self.friends[ff] = ffbutton
            else:
                pass
                #print "not adding button"
                #import pdb; pdb.set_trace()
        self.scrollList.refresh()
            
        
            
    def makeFamilyButton(self, familyId, familyName, colorCode):

        #print("Making Family Button")
        #print familyId
        # What color should we display the name in?  Use the
        # appropriate nametag color, according to whether we are
        # "special friends" or not.
        fg = NametagGlobals.getNameFg(colorCode, PGButton.SInactive)
        
        #print "made family button"
        
        return DirectButton(
            relief = None,
            text = familyName,
            text_scale = 0.04,
            text_align = TextNode.ALeft,
            text_fg = fg,
            text1_bg = self.textDownColor,
            text2_bg = self.textRolloverColor,
            text3_fg = self.textDisabledColor,
            textMayChange = 0,            
            command = self.__chooseFriend,
            extraArgs = [familyId, familyName],
            )

            
    def __chooseFriend(self, friendId, friendName):
        """selects a friend for loading"""
        #messenger.send('wakeup') # I have no idea what this is for
        #handle = base.cr.identifyFriend(friendId) # the friend handle is throw awayused to get the doId for an avatar
        #if 0 and handle != None:
        #    friendText = handle.getName()
        #    self.friendLabel['text'] = (TTLocalizer.CatalogGiftTo % (friendText))
        #    self.friendGiftHandle = handle;
        #    self.frienddoId = handle.getDoId()
        #    self.__loadFriend()
        messenger.send('wakeup')            
        self.frienddoId = friendId
        self.receiverName = friendName
        self.friendLabel['text'] = (TTLocalizer.CatalogGiftTo % (self.receiverName))
        self.__loadFriend()
            
    def __loadFriend(self):

            #return
            """Requests a detail avatar from the database"""
            if self.allowGetDetails == 0:
                CatalogScreen.notify.warning("smashing requests")
            if self.frienddoId and self.allowGetDetails:
                if self.giftAvatar:
                    if hasattr(self.giftAvatar, 'doId'):
                        self.giftAvatar.delete()
                    self.giftAvatar = None
                self.giftAvatar = DistributedToon.DistributedToon(base.cr) #sets up a dummy avatar
                self.giftAvatar.doId = self.frienddoId #the doId is required for getAvatarDetails to work
                # getAvatarDetails puts a DelayDelete on the avatar, and this
                # is not a real DO, so bypass the 'generated' check
                self.giftAvatar.forceAllowDelayDelete()
                base.cr.getAvatarDetails(self.giftAvatar, self.__handleAvatarDetails, "DistributedToon") #request to the database
                self.gotAvatar = 0 #sets the flag to false so we know we have a database request pending
                self.allowGetDetails = 0
                self.scrollList['state'] = DGG.DISABLED
    
    def __handleAvatarDetails(self, gotData, avatar, dclass):

        """Receives and uses the detail avatar"""
        #if something goes wrong set teh flag as invlaid
        if self.giftAvatar.doId != avatar.doId or gotData == 0:
            CatalogScreen.notify.error("Get Gift Avatar Failed")
            self.gotAvatar = 0
            return
        #otherwise set the flag to valid and update the catalog
        else:
            self.gotAvatar = 1
            self.giftAvatar = avatar
            #self.giftAvatar = DistributedToon.DistributedToon(base.cr) #error test case 1
            #self.giftAvatar = None #error test case 2
            self.scrollList['state'] = DGG.NORMAL
        self.allowGetDetails = 1
        self.update()
        
    def __giftToggle(self):
        messenger.send('wakeup')
        if self.gifting == -1:
            self.gifting = 1
            self.giftLabel.show()
            self.friendLabel.show()
            self.scrollList.show()
            self.giftToggle['text'] = TTLocalizer.CatalogGiftToggleOn
            self.__loadFriend()
        else:
            self.gifting = -1
            self.giftLabel.hide()
            self.friendLabel.hide()
            self.scrollList.hide()
            self.giftToggle['text'] = TTLocalizer.CatalogGiftToggleOff
            self.update()
            
    def __handleUDack(self, caller = None):
        taskMgr.remove("ackTimeOut")
        if hasattr(self, 'giftToggle') and self.giftToggle:
            self.giftToggle['state'] = DGG.NORMAL
            self.giftToggle['text'] = TTLocalizer.CatalogGiftToggleOff
        
    def __handleNoAck(self, caller = None):
        if hasattr(self, 'giftToggle') and self.giftToggle:
            self.giftToggle['text'] = TTLocalizer.CatalogGiftToggleNoAck
        

        
               
        


        
    
        
