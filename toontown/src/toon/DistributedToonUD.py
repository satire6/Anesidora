
from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals

from direct.distributed.DistributedObjectUD import DistributedObjectUD
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogItemTypes
from toontown.catalog import CatalogClothingItem
from toontown.toonbase import ToontownGlobals
import ToonDNA

class DistributedToonUD(DistributedObjectUD):
    
    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.dna = ToonDNA.ToonDNA()
        self.clothesTopsList = []
        self.clothesBottomsList = []
        self.emoteAccess = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.fishingRod = 0
        
        if simbase.wantPets:
            self.petTrickPhrases = []
            
        if simbase.wantBingo:
            self.bingoCheat = False

        self.customMessages = []
        
        self.mailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
        #self.deliveryboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.GiftTag)


    def d_setGiftSchedule(self, onOrder):
        #self.sendUpdate("setGiftSchedule", [onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)])
        self.sendUpdate("setGiftSchedule", [onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)])
        
    """
    def b_setGiftSchedule(self, onOrder, doUpdateLater = True):
        self.setGiftSchedule(onOrder, doUpdateLater)
        self.d_setGiftSchedule(onOrder)
    """


    def setGiftSchedule(self, onGiftOrder, doUpdateLater = True):
        #self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

    def getGiftSchedule(self):
        #return self.onGiftOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        return self.onGiftOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
    
    
    def setDeliverySchedule(self, onOrder, doUpdateLater = True):
        
        self.onOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

    def getDeliverySchedule(self):
        return self.onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
      
    
    def setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.monthlyCatalog = CatalogItemList.CatalogItemList(monthlyCatalog)
        self.weeklyCatalog = CatalogItemList.CatalogItemList(weeklyCatalog)
        self.backCatalog = CatalogItemList.CatalogItemList(backCatalog)
        
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
        
    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def getTotalMoney(self):
        return (self.money + self.bankMoney)
    
    def setBankMoney(self, money):
        self.bankMoney = money
        
    def getBankMoney(self):
        return self.bankMoney
        
    def setMailboxContents(self, mailboxContents):
        self.notify.debug("Setting mailboxContents to %s." % (mailboxContents))
        self.mailboxContents = CatalogItemList.CatalogItemList(mailboxContents, store = CatalogItem.Customization)
        self.notify.debug("mailboxContents is %s." % (self.mailboxContents))

    def getMailboxContents(self):
        return self.mailboxContents.getBlob(store = CatalogItem.Customization)


    def setAwardMailboxContents(self, awardMailboxContents):
        self.notify.debug("Setting awardMailboxContents to %s." % (awardMailboxContents))
        self.awardMailboxContents = CatalogItemList.CatalogItemList(awardMailboxContents, store = CatalogItem.Customization )
        self.notify.debug("awardMailboxContents is %s." % (self.awardMailboxContents))

    def getAwardMailboxContents(self):
        return self.awardMailboxContents.getBlob(store = CatalogItem.Customization  )

    def setAwardSchedule(self, onOrder, doUpdateLater = True):
        
        self.onAwardOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

    def getAwardSchedule(self):
        return self.onAwardOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)       
        
    """        
    def setDeliveryboxContents(self, deliveryboxContents):
        self.deliveryboxContents = CatalogItemList.CatalogItemList(deliveryboxContents, store = CatalogItem.Customization | CatalogItem.GiftTag)
 
    def getDeliveryboxContents(self):
        return self.deliveryboxContents.getBlob(store = CatalogItem.Customization | CatalogItem.GiftTag)
    """
    def setDNAString(self, string):
            self.dna.makeFromNetString(string)

    def getDNAString( self ):
        """
        Function:    retrieve the dna information from this suit, called
                     whenever a client needs to create this suit
        Returns:     netString representation of this suit's dna
        """
        return self.dna.makeNetString()
        
    def getStyle(self):
        return self.dna
        
    def setClothesTopsList(self, clothesList):
        self.clothesTopsList = clothesList
        
    def getClothesTopsList(self):
        return self.clothesTopsList   

    def setClothesBottomsList(self, clothesList):
        self.clothesBottomsList = clothesList
        
    def getClothesBottomsList(self):
        return self.clothesBottomsList

    def setEmoteAccess(self, bits):
        if len(bits) != len(self.emoteAccess):
            self.notify.warning("New emote access list must be the same size as the old one.")
            return
        self.emoteAccess = bits

    def getEmoteAccess(self):
        return self.emoteAccess
        
    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages

    def getCustomMessages(self):
        return self.customMessages
        
    def setPetTrickPhrases(self, tricks):
        self.petTrickPhrases = tricks
        
    def getPetTrickPhrases(self):
        return self.petTrickPhrases
        
    def setFishingRod(self, rodId):
        self.fishingRod = rodId

    def getFishingRod(self):
        return self.fishingRod
        
    def getGardenSpecials(self):
        return self.gardenSpecials
        
    def setGardenSpecials(self, specials):
        self.gardenSpecials = specials

    def checkForItemInCloset(self, clothingItem):
        """Returns None if the clothing item is not in the closet."""
        result = None
        clothingTypeInfo = CatalogClothingItem.ClothingTypes[clothingItem.clothingType]
        styleStr = clothingTypeInfo[1]
        if clothingItem.isShirt():
            # ok check the tops list            
            # we have the style str, check TOON DNA to get shirt and sleeve indices
            shirtStyleInfo = ToonDNA.ShirtStyles[styleStr]
            topTex= shirtStyleInfo[0]
            sleeveTex = shirtStyleInfo[1]
            topTexColor = shirtStyleInfo[2][clothingItem.colorIndex][0]
            sleeveTexColor = shirtStyleInfo[2][clothingItem.colorIndex][1]
            # See if this top is already there
            for i in range(0, len(self.clothesTopsList), 4):
                if (self.clothesTopsList[i] == topTex and
                    self.clothesTopsList[i+1] == topTexColor and
                    self.clothesTopsList[i+2] == sleeveTex and
                    self.clothesTopsList[i+3] == sleeveTexColor):
                    result = ToontownGlobals.P_ItemInCloset
                    break
        else:
            bottomStyleInfo = ToonDNA.BottomStyles[styleStr]
            botTex= bottomStyleInfo[0]
            botTexColor = bottomStyleInfo[1][clothingItem.colorIndex]
            # See if this bottom is already there
            for i in range(0, len(self.clothesBottomsList), 2):
                if (self.clothesBottomsList[i] == botTex and
                    self.clothesBottomsList[i+1] == botTexColor):
                    result = ToontownGlobals.P_ItemInCloset
                    break
        return result

    def checkForItemAlreadyWorn(self, clothingItem):
        """Returns None if the toon is not wearing the clothing item."""
        result = None
        clothingTypeInfo = CatalogClothingItem.ClothingTypes[clothingItem.clothingType]
        styleStr = clothingTypeInfo[1]
        if clothingItem.isShirt():
            # ok check the tops list            
            # we have the style str, check TOON DNA to get shirt and sleeve indices
            shirtStyleInfo = ToonDNA.ShirtStyles[styleStr]
            topTex= shirtStyleInfo[0]
            sleeveTex = shirtStyleInfo[1]
            topTexColor = shirtStyleInfo[2][clothingItem.colorIndex][0]
            sleeveTexColor = shirtStyleInfo[2][clothingItem.colorIndex][1]
            # See if this top is already being worn
            if self.dna.topTex == topTex and \
               self.dna.sleeveTex == sleeveTex and \
               self.dna.topTexColor == topTexColor and \
               self.dna.sleeveTexColor == sleeveTexColor:
                result = ToontownGlobals.P_ItemAlreadyWorn
        else:
            bottomStyleInfo = ToonDNA.BottomStyles[styleStr]
            bottomTex= bottomStyleInfo[0]
            bottomTexColor = bottomStyleInfo[1][clothingItem.colorIndex]
            # See if this bottom is already being worn
            if self.dna.botTex == bottomTex and \
                self.dna.botTexColor == bottomTexColor:
                result = ToontownGlobals.P_ItemAlreadyWorn 
        return result
        
    def checkForDuplicateItem(self, catalogItem):
        """Return None if the catalog item is not in his mailbox, or on him somehow"""
        result = None
        # go through his mailbox
        if catalogItem in self.mailboxContents:
            result = ToontownGlobals.P_ItemInMailbox
        elif catalogItem in self.onOrder:
            result = ToontownGlobals.P_ItemOnOrder
        elif catalogItem in self.onGiftOrder:
            result = ToontownGlobals.P_ItemOnGiftOrder
        elif catalogItem in self.awardMailboxContents:
            result = ToontownGlobals.P_ItemInAwardMailbox
        elif catalogItem in self.onAwardOrder:
            result = ToontownGlobals.P_ItemOnAwardOrder

        # now based on the item type do some other checking
        if not result:
            if catalogItem.getTypeCode() == CatalogItemTypes.CLOTHING_ITEM:
                result = self.checkForItemInCloset(catalogItem)
                if not result:
                    result = self.checkForItemAlreadyWorn(catalogItem)
            elif catalogItem.getTypeCode() == CatalogItemTypes.CHAT_ITEM:
                speedChatIndex = catalogItem.customIndex
                if speedChatIndex in self.customMessages:
                    result = ToontownGlobals.P_ItemInMyPhrases
            elif catalogItem.getTypeCode() == CatalogItemTypes.PET_TRICK_ITEM:
                trickId = catalogItem.trickId
                if trickId in self.petTrickPhrases:
                    result = ToontownGlobals.P_ItemInPetTricks
        return result
