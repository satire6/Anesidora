from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
import CatalogItemTypes
import CatalogItem
from CatalogWallpaperItem import getAllWallpapers
from CatalogFlooringItem import getAllFloorings
from CatalogMouldingItem import getAllMouldings
from CatalogWainscotingItem import getAllWainscotings
from CatalogFurnitureItem import getAllFurnitures
from toontown.toontowngui.TeaserPanel import TeaserPanel
from otp.otpbase import OTPGlobals

CATALOG_PANEL_WORDWRAP = 10
CATALOG_PANEL_CHAT_WORDWRAP = 9

class CatalogItemPanel(DirectFrame):
    """
    CatalogItemPanel

    This class presents the graphical represntation of a catalog item in the
    Catalog GUI.
    """
    def __init__(self, parent=aspect2d, parentCatalogScreen = None ,**kw):
        optiondefs = (
            # Define type of DirectGuiWidget
            ('item',                                  None,  DGG.INITOPT),
            ('type',    CatalogItem.CatalogTypeUnspecified,  DGG.INITOPT),
            ('relief',                                None,     None),
            )
        self.parentCatalogScreen = parentCatalogScreen;
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectFrame.__init__(self, parent)
        self.loaded = 0
        
        # Loading is done lazily as we display each item.
        # This reduces the initial load time when first opening the catalog
        # and nicely spreads it out
        # self.load()
        # Call initialization methods
        self.initialiseoptions(CatalogItemPanel)
        assert parentCatalogScreen != None, "parentCatalogScreen: is none"
        
    def load(self):
        # Loading is guarded so things only get loaded once
        if self.loaded:
            return
        self.loaded = 1
        # Init variables
        self.verify = None
        # Some items know how to draw themselves.  Put this first so
        # it will be below any text on the frame.
        # Add a picture Frame so draw order is preserved if you change
        # the picture
        self.pictureFrame = self.attachNewNode('pictureFrame')
        self.pictureFrame.setScale(0.15)
        self.itemIndex = 0
        self.ival = None
        # If this is an item that needs customization, add buttons
        # to scroll through variations
        typeCode = self['item'].getTypeCode()
        if (self['item'].needsCustomize() and
            ((typeCode == CatalogItemTypes.WALLPAPER_ITEM) or
             (typeCode == CatalogItemTypes.FLOORING_ITEM) or
             (typeCode == CatalogItemTypes.MOULDING_ITEM) or
             (typeCode == CatalogItemTypes.FURNITURE_ITEM) or
             (typeCode == CatalogItemTypes.WAINSCOTING_ITEM) or 
             (typeCode == CatalogItemTypes.TOON_STATUE_ITEM))):
            if typeCode == CatalogItemTypes.WALLPAPER_ITEM:
                self.items = getAllWallpapers(self['item'].patternIndex)
            elif typeCode == CatalogItemTypes.FLOORING_ITEM:
                self.items = getAllFloorings(self['item'].patternIndex)
            elif typeCode == CatalogItemTypes.MOULDING_ITEM:
                self.items = getAllMouldings(self['item'].patternIndex)
            elif typeCode == CatalogItemTypes.FURNITURE_ITEM:
                self.items = getAllFurnitures(self['item'].furnitureType)
            elif typeCode == CatalogItemTypes.TOON_STATUE_ITEM:
                    self.items = self['item'].getAllToonStatues()
            elif typeCode == CatalogItemTypes.WAINSCOTING_ITEM:
                self.items = getAllWainscotings(self['item'].patternIndex)
            self.numItems = len(self.items)
            if self.numItems > 1:
                guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
                nextUp = guiItems.find('**/arrow_up')
                nextRollover = guiItems.find('**/arrow_Rollover')
                nextDown = guiItems.find('**/arrow_Down')
                prevUp = guiItems.find('**/arrowUp')
                prevDown = guiItems.find('**/arrowDown1')
                prevRollover = guiItems.find('**/arrowRollover')
                self.nextVariant = DirectButton(
                    parent = self,
                    relief = None,
                    image = (nextUp, nextDown, nextRollover, nextUp),
                    image3_color = (1,1,1,.4),
                    pos = (0.13,0,0),
                    command = self.showNextVariant,
                    )
                self.prevVariant = DirectButton(
                    parent = self,
                    relief = None,
                    image = (prevUp, prevDown, prevRollover, prevUp),
                    image3_color = (1,1,1,.4),
                    pos = (-0.13,0,0),
                    command = self.showPrevVariant,
                    state = DGG.DISABLED,
                    )
                self.variantPictures = [(None, None)] * self.numItems
            else:
                self.variantPictures = [(None, None)]
            self.showCurrentVariant()
        else:
            # Some items know how to draw themselves.  Put this first so
            # it will be below any text on the frame.

            picture,self.ival = self['item'].getPicture(base.localAvatar)
            if picture:
                picture.reparentTo(self)
                picture.setScale(0.15)
                
            self.items = [self['item']]
            self.variantPictures = [(picture, self.ival)]
        # type label
        self.typeLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0,0,0.24),
            scale = 0.075,
            text = self['item'].getTypeName(),
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_wordwrap = CATALOG_PANEL_WORDWRAP,
            )
        # aux text label
        self.auxText = DirectLabel(
            parent = self,
            relief = None,
            scale = 0.05,
            pos = (-0.20, 0, 0.16),
            )
        # Put this one at a jaunty angle
        self.auxText.setHpr(0,0,-30)

        self.nameLabel = DirectLabel(
            parent = self,
            relief = None,
            text = self['item'].getDisplayName(),
            text_fg = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_scale = TTLocalizer.CIPnameLabel,
            text_wordwrap = CATALOG_PANEL_WORDWRAP + TTLocalizer.CIPwordwrapOffset,
            )

        if self['item'].getTypeCode() == CatalogItemTypes.CHAT_ITEM:
            # adjust wordwrap as the bubbles are narrower
            self.nameLabel['text_wordwrap'] = CATALOG_PANEL_CHAT_WORDWRAP
            # Center the text vertically on the chat balloon based
            # on the number of rows of text
            numRows = self.nameLabel.component('text0').textNode.getNumRows()
            if numRows == 1:
                namePos = (0,0,-0.06)
            elif numRows == 2:
                namePos = (0,0,-0.03)
            else:
                namePos = (0,0,0)
            nameScale = 0.063
        else:
            namePos = (0,0,-.22)
            nameScale = 0.06
        self.nameLabel.setPos(*namePos)
        self.nameLabel.setScale(nameScale)

        priceStr = str(self['item'].getPrice(self['type'])) + " " + TTLocalizer.CatalogCurrency
        priceScale = 0.07
        # prepend sale sign if necessary
        if self['item'].isSaleItem():
            priceStr = TTLocalizer.CatalogSaleItem + priceStr
            priceScale = 0.06
        # price label
        self.priceLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0,0,-0.3),
            scale = priceScale,
            text = priceStr,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getSignFont(),
            text_align = TextNode.ACenter,
            )

        # buy button
        buttonModels = loader.loadModel(
            "phase_3.5/models/gui/inventory_gui")
        upButton = buttonModels.find("**/InventoryButtonUp")
        downButton = buttonModels.find("**/InventoryButtonDown")
        rolloverButton = buttonModels.find("**/InventoryButtonRollover")
        
        buyText = TTLocalizer.CatalogBuyText
        
        if self['item'].isRental():
           buyText = TTLocalizer.CatalogRentText 

        self.buyButton = DirectButton(
            parent = self,
            relief = None,
            pos = (0.2, 0, 0.15),
            scale = (0.7,1,0.8),
            text = buyText,
            text_scale = (0.06, 0.05),
            text_pos = (-0.005,-0.01),
            image = (upButton,
                     downButton,
                     rolloverButton,
                     upButton,                     
                     ),
            image_color = (1.0, 0.2, 0.2, 1),
            # Make the rollover button pop out
            image0_color = Vec4(1.0, 0.4, 0.4, 1),
            # Make the disabled button fade out
            image3_color = Vec4(1.0, 0.4, 0.4, 0.4),
            command = self.__handlePurchaseRequest,
            )
        #self.updateBuyButton()

        soundIcons = loader.loadModel('phase_5.5/models/gui/catalogSoundIcons')
        soundOn = soundIcons.find('**/sound07')
        
        soundOff = soundIcons.find('**/sound08')

        self.soundOnButton = DirectButton(
            parent = self,
            relief = None,
            pos = (0.2, 0, -0.15),
            scale = (0.7,1,0.8),
            #geom = soundOn,
            #text = TTLocalizer.CatalogSndOnText,
            text_scale = (0.06, 0.05),
            text_pos = (-0.005,-0.01),
            image = (upButton,
                     downButton,
                     rolloverButton,
                     upButton,                     
                     ),
            image_color = (0.2, 0.5, 0.2, 1),
            # Make the rollover button pop out
            image0_color = Vec4(0.4, 0.5, 0.4, 1),
            # Make the disabled button fade out
            image3_color = Vec4(0.4, 0.5, 0.4, 0.4),
            command = self.handleSoundOnButton,
            )
        self.soundOnButton.hide()
        soundOn.setScale(0.1)
        soundOn.reparentTo(self.soundOnButton)

        self.soundOffButton = DirectButton(
            parent = self,
            relief = None,
            pos = (0.2, 0, -0.15),
            scale = (0.7,1,0.8),
            #text = TTLocalizer.CatalogSndOffText,
            text_scale = (0.06, 0.05),
            text_pos = (-0.005,-0.01),
            image = (upButton,
                     downButton,
                     rolloverButton,
                     upButton,                     
                     ),
            image_color = (0.2, 1.0, 0.2, 1),
            # Make the rollover button pop out
            image0_color = Vec4(0.4, 1.0, 0.4, 1),
            # Make the disabled button fade out
            image3_color = Vec4(0.4, 1.0, 0.4, 0.4),
            command = self.handleSoundOffButton,
            )
        self.soundOffButton.hide()
        soundOff = self.soundOffButton.attachNewNode('soundOff')
        soundOn.copyTo(soundOff)
        #soundOff.setScale(0.1)
        soundOff.reparentTo(self.soundOffButton)        
        
        upGButton = buttonModels.find("**/InventoryButtonUp")
        downGButton = buttonModels.find("**/InventoryButtonDown")
        rolloverGButton = buttonModels.find("**/InventoryButtonRollover")
        
        ##if len(base.localAvatar.friendsList) > 0:
        self.giftButton = DirectButton(
            parent = self,
            relief = None,
            pos = (0.2, 0, 0.15),
            scale = (0.7,1,0.8),
            text = TTLocalizer.CatalogGiftText,
            text_scale = (0.06, 0.05),
            text_pos = (-0.005,-0.01),
            image = (upButton,
                     downButton,
                     rolloverButton,
                     upButton,                     
                     ),
            image_color = (1.0, 0.2, 0.2, 1),
            # Make the rollover button pop out
            image0_color = Vec4(1.0, 0.4, 0.4, 1),
            # Make the disabled button fade out
            image3_color = Vec4(1.0, 0.4, 0.4, 0.4),
            command = self.__handleGiftRequest,
            )
        self.updateButtons()
        
    def showNextVariant(self):
        messenger.send('wakeup')
        self.hideCurrentVariant()
        self.itemIndex += 1
        if self.itemIndex >= self.numItems - 1:
            self.itemIndex = self.numItems - 1
            self.nextVariant['state'] = DGG.DISABLED
        else:
            self.nextVariant['state'] = DGG.NORMAL
        self.prevVariant['state'] = DGG.NORMAL
        self.showCurrentVariant()
        
    def showPrevVariant(self):
        messenger.send('wakeup')
        self.hideCurrentVariant()
        self.itemIndex -= 1
        if self.itemIndex < 0:
            self.itemIndex = 0
            self.prevVariant['state'] = DGG.DISABLED
        else:
            self.prevVariant['state'] = DGG.NORMAL
        self.nextVariant['state'] = DGG.NORMAL
        self.showCurrentVariant()
        
    def showCurrentVariant(self):
        newPic, self.ival = self.variantPictures[self.itemIndex]
        if self.ival:
            self.ival.finish()
        if not newPic:
            variant = self.items[self.itemIndex]
            newPic, self.ival = variant.getPicture(base.localAvatar)
            self.variantPictures[self.itemIndex] = (newPic, self.ival)
        newPic.reparentTo(self.pictureFrame)
        if self.ival:
            self.ival.loop()
        if (self['item'].getTypeCode() == CatalogItemTypes.TOON_STATUE_ITEM):        
            if hasattr(self, 'nameLabel'):
                self.nameLabel['text'] = self.items[self.itemIndex].getDisplayName()
                self['item'].gardenIndex = self.items[self.itemIndex].gardenIndex
            
    def hideCurrentVariant(self):
        currentPic = self.variantPictures[self.itemIndex][0]
        if currentPic:
            currentPic.detachNode()
            
    def unload(self):
        if not self.loaded:
            DirectFrame.destroy(self)
            return
        self.loaded = 0
        
        # Getting Toon Statue to the first pose before exiting.
        if (self['item'].getTypeCode() == CatalogItemTypes.TOON_STATUE_ITEM):
            self['item'].deleteAllToonStatues()
            self['item'].gardenIndex = self['item'].startPoseIndex
            self.nameLabel['text'] = self['item'].getDisplayName()
                
        # Cleanup any items created during requestPurchase
        self['item'].requestPurchaseCleanup()
        # Clear out instance variables
        for picture, ival in self.variantPictures:
            if picture:
                picture.destroy()
            if ival:
                ival.finish()
        self.variantPictures=None
        if self.ival:
            self.ival.finish()
        self.ival = None
        if(len(self.items)):
            self.items[0].cleanupPicture()

        self.pictureFrame.remove()
        self.pictureFrame=None
        self.items=[]
        if self.verify:
            self.verify.cleanup()
        DirectFrame.destroy(self)
        
    def destroy(self):
        # this is only so the DirectGui code cleans us up properly
        self.parentCatalogScreen=None
        self.unload()

    def getTeaserPanel(self):
         # display the appropriate page of the feature browser for this catalog item type
         typeName = self['item'].getTypeName()
         if (typeName == TTLocalizer.EmoteTypeName) or (typeName == TTLocalizer.ChatTypeName):
             page = 'emotions'
         elif (typeName == TTLocalizer.GardenTypeName) or (typeName == TTLocalizer.GardenStarterTypeName):
             page = 'gardening'
         else:
             # default
             page = 'clothing'
         def showTeaserPanel():
             TeaserPanel(pageName=page)
         return showTeaserPanel

    def updateBuyButton(self):
        # display the correct button based on item status
        # if reached purchase limit
        if not self.loaded:
            return

        # Only paid members can purchase
        if not base.cr.isPaid():
            self.buyButton['command'] = self.getTeaserPanel()
            
        #print (self['item'].getName())
        # Show if on order
        self.buyButton.show()
        
        typeCode = self['item'].getTypeCode()
        orderCount = base.localAvatar.onOrder.count(self['item'])        
        if (orderCount > 0):
            if orderCount > 1:
                auxText = "%d %s" % (orderCount, TTLocalizer.CatalogOnOrderText)
            else:
                auxText = TTLocalizer.CatalogOnOrderText
                #self.buyButton.hide() 
        else:
            auxText = ""
        # else if you have the current nametag
        isNameTag = (typeCode == CatalogItemTypes.NAMETAG_ITEM)
        if isNameTag and not (localAvatar.getGameAccess() == OTPGlobals.AccessFull):
            # If the item panel is the free player nametag
            if (self['item'].nametagStyle == 100):
                if (localAvatar.getFont() == ToontownGlobals.getToonFont()):
                    auxText = TTLocalizer.CatalogCurrent
                    self.buyButton['state'] = DGG.DISABLED
        elif isNameTag and (self['item'].nametagStyle == localAvatar.getNametagStyle()):
            auxText = TTLocalizer.CatalogCurrent
            self.buyButton['state'] = DGG.DISABLED
        elif (self['item'].reachedPurchaseLimit(base.localAvatar)):
            max = self['item'].getPurchaseLimit()
            # Override aux text
            if max <= 1:
                auxText = TTLocalizer.CatalogPurchasedText
                if self['item'].hasBeenGifted(base.localAvatar):
                    auxText = TTLocalizer.CatalogGiftedText
            else:
                auxText = TTLocalizer.CatalogPurchasedMaxText
            self.buyButton['state'] = DGG.DISABLED
            #self.buyButton.hide()
        # else if can afford
        elif ( hasattr(self['item'], 'noGarden') and
               self['item'].noGarden(base.localAvatar)):
            auxText = TTLocalizer.NoGarden
            self.buyButton['state'] = DGG.DISABLED        
        elif ( hasattr(self['item'], 'isSkillTooLow') and
               self['item'].isSkillTooLow(base.localAvatar)):
            auxText = TTLocalizer.SkillTooLow
            self.buyButton['state'] = DGG.DISABLED
        elif ( hasattr(self['item'], 'getDaysToGo') and
               self['item'].getDaysToGo(base.localAvatar)):
            auxText = TTLocalizer.DaysToGo % self['item'].getDaysToGo(base.localAvatar)
            self.buyButton['state'] = DGG.DISABLED            
        elif ( self['item'].getPrice(self['type']) <=
              (base.localAvatar.getMoney() +
               base.localAvatar.getBankMoney()) ):
            self.buyButton['state'] = DGG.NORMAL          
            self.buyButton.show()            
        # else ghosted buy button
        else:
            self.buyButton['state'] = DGG.DISABLED          
            self.buyButton.show()
        self.auxText['text'] = auxText
        
    def __handlePurchaseRequest(self):
        # prompt the user to verify purchase
        if self['item'].replacesExisting() and self['item'].hasExisting():
            message = TTLocalizer.CatalogOnlyOnePurchase % {
                'old' : self['item'].getYourOldDesc(),
                'item' : self['item'].getName(),
                'price' : self['item'].getPrice(self['type']),
                }
        else:
            if self['item'].isRental():
                message = TTLocalizer.CatalogVerifyRent % {
                    'item' : self['item'].getName(),
                    'price' : self['item'].getPrice(self['type']),
                    }
            else:
                message = TTLocalizer.CatalogVerifyPurchase % {
                    'item' : self['item'].getName(),
                    'price' : self['item'].getPrice(self['type']),
                    }
            
        self.verify = TTDialog.TTGlobalDialog(
            doneEvent = "verifyDone",
            message = message,
            style = TTDialog.TwoChoice)
        self.verify.show()
        self.accept("verifyDone", self.__handleVerifyPurchase)
        
    def __handleVerifyPurchase(self):
        # prompt the user to verify purchase
        status = self.verify.doneStatus
        self.ignore("verifyDone")
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if (status == "ok"):
            # ask the AI to clear this purchase
            item = self.items[self.itemIndex]
            messenger.send("CatalogItemPurchaseRequest", [item])
            self.buyButton['state'] = DGG.DISABLED 
            
    def __handleGiftRequest(self):
        # prompt the user to verify purchase
        if self['item'].replacesExisting() and self['item'].hasExisting():
            message = TTLocalizer.CatalogOnlyOnePurchase % {
                'old' : self['item'].getYourOldDesc(),
                'item' : self['item'].getName(),
                'price' : self['item'].getPrice(self['type']),
                }
        else:
            friendIndex = self.parentCatalogScreen.friendGiftIndex
            friendText = "Error";
            numFriends = len(base.localAvatar.friendsList) + len(base.cr.avList) - 1
            if numFriends > 0:
                    #friendPair = base.localAvatar.friendsList[self.parentCatalogScreen.friendGiftIndex]
                    #handle = base.cr.identifyFriend(friendPair[0]) 
                    #friendText = self.parentCatalogScreen.friendGiftHandle.getName()
                    friendText = self.parentCatalogScreen.receiverName
            message = TTLocalizer.CatalogVerifyGift % {
                'item' : self['item'].getName(),
                'price' : self['item'].getPrice(self['type']),
                'friend' : friendText,
                }
            
        self.verify = TTDialog.TTGlobalDialog(
            doneEvent = "verifyGiftDone",
            message = message,
            style = TTDialog.TwoChoice)
        self.verify.show()
        self.accept("verifyGiftDone", self.__handleVerifyGift)
               
    def __handleVerifyGift(self):
        # prompt the user to verify purchase
        status = self.verify.doneStatus
        self.ignore("verifyGiftDone")
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if (status == "ok"):
            # ask the AI to clear this purchase
            self.giftButton['state'] =  DGG.DISABLED
            item = self.items[self.itemIndex]
            messenger.send("CatalogItemGiftPurchaseRequest", [item])
            
    def updateButtons(self, giftActivate = 0):
        if self.parentCatalogScreen.gifting == -1:
            self.updateBuyButton()
            if self.loaded:
                self.giftButton.hide()
        else:
            #print("update gift button")
            self.updateGiftButton(giftActivate)
            if self.loaded:
                self.buyButton.hide()
                        
    def updateGiftButton(self, giftUpdate = 0):
        # display the correct button based on item status
        # if reached purchase limit
        if not self.loaded:
            return
        self.giftButton.show()
        if giftUpdate == 0:
            return

        # Only paid members can purchase gifts
        if not base.cr.isPaid():
            self.giftButton['command'] = self.getTeaserPanel()
         
        self.auxText['text'] = " "
        numFriends = len(base.localAvatar.friendsList) + len(base.cr.avList) - 1
        if numFriends > 0:
            # Start as ghosted and disabled
            self.giftButton['state'] = DGG.DISABLED 
            #self.giftButton['state'] = DGG.NORMAL  #REMOVE ME          
            self.giftButton.show()
            #return # REMOVE ME
            #friendPair = base.localAvatar.friendsList[self.parentCatalogScreen.friendGiftIndex]
            #if it's not a gift hide it
            auxText = " "
            if (self['item'].isGift() <= 0):
                self.giftButton.show()
                self.giftButton['state'] = DGG.DISABLED
                auxText = TTLocalizer.CatalogNotAGift
                self.auxText['text'] = auxText
                return
                #print "not a gift"
                #self.giftButton.hide()
            #otherwise if you have a valid avater for your friend attempt to activate the button
            elif (self.parentCatalogScreen.gotAvatar == 1):
                avatar = self.parentCatalogScreen.giftAvatar #aliasing the giftAvater
                #if it is for the other gender then fail
                if((self['item'].forBoysOnly() and avatar.getStyle().getGender() == 'f') or (self['item'].forGirlsOnly() and avatar.getStyle().getGender() == 'm')):
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED
                    auxText = TTLocalizer.CatalogNoFit
                    self.auxText['text'] = auxText
                    #print "fit"
                    return
                #if it's purchase limit is reached fail
                elif(self['item'].reachedPurchaseLimit(avatar)):
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED 
                    auxText = TTLocalizer.CatalogPurchasedGiftText
                    self.auxText['text'] = auxText
                    #print "limit"
                    return
                #if their onGiftorder box is full
                elif len(avatar.mailboxContents) + len(avatar.onGiftOrder) >= ToontownGlobals.MaxMailboxContents:
                    self.giftButton.show()
                    self.giftButton['state'] = DGG.DISABLED
                    auxText = TTLocalizer.CatalogMailboxFull
                    self.auxText['text'] = auxText
                    #print "full"
                    return
                #if can you afford it activate the gift button
                elif ( self['item'].getPrice(self['type']) <=
                      (base.localAvatar.getMoney() +
                       base.localAvatar.getBankMoney()) ):
                    self.giftButton['state'] = DGG.NORMAL          
                    self.giftButton.show()  

    def handleSoundOnButton(self):
        """Handle the user clicking on the sound."""
        #import pdb; pdb.set_trace()
        item = self.items[self.itemIndex]        
        self.soundOnButton.hide()
        self.soundOffButton.show()
        if hasattr(item, 'changeIval'):
            if self.ival:
                self.ival.finish()
                self.ival = None
            self.ival = item.changeIval(volume = 1)
            self.ival.loop()        

    def handleSoundOffButton(self):
        """Handle the user clicking off the sound."""
        #import pdb; pdb.set_trace()
        item = self.items[self.itemIndex]        
        self.soundOffButton.hide()
        self.soundOnButton.show()
        if hasattr(item, 'changeIval'):
            if self.ival:
                self.ival.finish()
                self.ival = None
            self.ival = item.changeIval(volume = 0)
            self.ival.loop()           
