import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.estate import GardenGlobals

class CatalogGardenItem(CatalogItem.CatalogItem):
    """
    Represents a Garden Item on the Delivery List
    """

    sequenceNumber = 0

    def makeNewItem(self, itemIndex = 0, count  = 3, tagCode = 1):
        #import pdb; pdb.set_trace()
        self.gardenIndex = itemIndex
        self.numItems = count
        self.giftCode = tagCode
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 1
        else:
            return 100

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder \
           or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1        
        return 0

    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
                return TTLocalizer.CatalogAcceptGarden
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.GardenTypeName

    def getName(self):
        #name = ("Garden Item %s %s" % (self.gardenIndex, self.numItems))
        name = GardenGlobals.Specials[self.gardenIndex]['photoName']
        return name

    def recordPurchase(self, avatar, optional):
        #import pdb; pdb.set_trace()
        #if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
        #    return ToontownGlobals.P_ItemOnOrder
        #else:
        if 1:
            if avatar:
                pass
                avatar.addGardenItem(self.gardenIndex, self.numItems)
                #TODO modify the toon's GardenSpecials field
            return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        photoModel = GardenGlobals.Specials[self.gardenIndex]['photoModel']
        beanJar = loader.loadModel(photoModel)
        frame = self.makeFrame()
        beanJar.reparentTo(frame)

        photoPos = GardenGlobals.Specials[self.gardenIndex]['photoPos']
        beanJar.setPos(*photoPos)
        photoScale = GardenGlobals.Specials[self.gardenIndex]['photoScale']
        #beanJar.setScale(2.5)
        beanJar.setScale(photoScale)

        assert (not self.hasPicture)
        self.hasPicture=True
        return (frame, None)

    def output(self, store = ~0):
        return "CatalogGardenItem(%s%s)" % (
            self.gardenIndex,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return 0

    def getHashContents(self):
        return self.gardenIndex

    def getBasePrice(self):
        # equal to it's worth
        beanCost = GardenGlobals.Specials[self.gardenIndex]['beanCost']
        return beanCost

    def decodeDatagram(self, di, versionNumber, store):
        #import pdb; pdb.set_trace()
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.gardenIndex = di.getUint8()
        self.numItems = di.getUint8()

    def encodeDatagram(self, dg, store):
        #import pdb; pdb.set_trace()
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.gardenIndex)
        dg.addUint8(self.numItems)

    def getRequestPurchaseErrorText(self, retcode):
        """
        Tell the user the item is available and what jelly beans to use it with.
        """
        retval = CatalogItem.CatalogItem.getRequestPurchaseErrorText(self,retcode)
        origText =retval
        
        if retval == TTLocalizer.CatalogPurchaseItemAvailable or \
           retval == TTLocalizer.CatalogPurchaseItemOnOrder:
            #now lets tell them what other beans to plant it with
            recipeKey = GardenGlobals.getRecipeKeyUsingSpecial(self.gardenIndex)
            if not recipeKey == -1:
                retval += GardenGlobals.getPlantItWithString(self.gardenIndex)

                if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
                    if GardenGlobals.ACCELERATOR_USED_FROM_SHTIKER_BOOK:
                        retval = origText
                        retval += TTLocalizer.UseFromSpecialsTab
                    retval += TTLocalizer.MakeSureWatered

        return retval

    def getRequestPurchaseErrorTextTimeout(self):
        """
        #RAU How long do we display RequestPurchaseErrorText.
        Created since we need to display the text longer for garden supplies
        """
        return 20


    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 24 * 60 #24 hrs
        else:
            return 0


    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
            return 1
        else:
            return 0
        #return 1

    def compareTo(self, other):
       if self.gardenIndex != other.gardenIndex:
           return self.gardenIndex - other.gardenIndex
       return self.gardenIndex - other.gardenIndex

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.

        if avatar.onOrder.count(self) != 0:
            # It's on the way.
            return 1

        if avatar.mailboxContents.count(self) != 0:
            # It's waiting in the mailbox.
            return 1

        for specials in avatar.getGardenSpecials():
            if specials[0] == self.gardenIndex:
                if self.gardenIndex == GardenGlobals.GardenAcceleratorSpecial:
                    #we're already carrying it
                    return 1

        # Not found anywhere; go ahead and buy it.
        return 0

    def isSkillTooLow(self, avatar):
        recipeKey = GardenGlobals.getRecipeKeyUsingSpecial(self.gardenIndex)
        recipe = GardenGlobals.Recipes[recipeKey]
        numBeansRequired = len(recipe['beans'])

        canPlant = avatar.getBoxCapability()
        result = False
        if canPlant < numBeansRequired:
            result = True
        # make the Toon Statue special, requiring 639 skill
        if not result and \
           GardenGlobals.Specials.has_key(self.gardenIndex) and \
           GardenGlobals.Specials[self.gardenIndex].has_key('minSkill'):
            minSkill = GardenGlobals.Specials[self.gardenIndex]['minSkill']
            if  avatar.shovelSkill < minSkill:
                result = True
            else:
                result = False
        return result;

    def noGarden(self, avatar):
        """
        if we don't have a garden, we can't buy the fertilizer and statues
        """
        return not avatar.getGardenStarted()

    def isGift(self):
        return 0
