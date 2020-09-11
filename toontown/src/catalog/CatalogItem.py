from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


import types
import sys

# This is created in decodeCatalogItem, below, as a map that reverses
# the lookup for the indexes defined in CatalogItemTypes.py.
CatalogReverseType = None

# This is the current version number that is written to the datagram
# stream describing how the CatalogItems are formatted.  It is similar
# to the bam minor version number.  When you introduce a change to the
# code that makes old records invalid, increment the version number,
# and put the appropriate conditionals in the decodeDatagram() methods
# based on the version number.  This helps us avoid having to do
# database patches every time something changes here.
CatalogItemVersion = 8
# version 2: adds pr to posHpr
# version 3: makes wallpaper type 16-bit
# version 4: make wallpaper color index a customization option
# version 5: use new hprs instead of old hprs (temp-hpr-fix)
# version 6: add loyaltyDays to Clothing, Emote,
# version 7: add cost to RentalItem
# version 8: add specialEventId 

# How much default markup for backorder items?
CatalogBackorderMarkup = 1.2

# How much to reduce for sale items?
CatalogSaleMarkdown = 0.75

# These are bits that represent the additional data that might be
# stored in the blob along with the CatalogItem.  This must be known
# in order to properly decode the CatalogItem into or from a blob;
# context will indicate which values are appropriate to store along
# with the CatalogItem.
Customization   = 0x01
DeliveryDate    = 0x02
Location        = 0x04
WindowPlacement = 0x08
GiftTag         = 0x10 #usually contains the name of the sender

# These are flags that indicate which kind of catalog the item is
# stored on.  This is not stored on the item itself, but is rather
# stored on the list.
CatalogTypeUnspecified = 0
CatalogTypeWeekly = 1
CatalogTypeBackorder = 2
CatalogTypeMonthly = 3
CatalogTypeLoyalty = 4

class CatalogItem:
    """CatalogItem"""
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogItem")

    def __init__(self, *args, **kw):
        # This init function is designed to be directly inherited (not
        # overridden) by each of the base classes.  It performs a
        # dispatch based on the parameter types to construct a
        # CatalogItem either from a datagram or directly from its
        # parameters.

        self.saleItem = 0
        self.deliveryDate = None
        self.posHpr = None
        self.giftTag = None
        self.giftCode = 0
        self.hasPicture = False
        self.volume = 0
        self.specialEventId = 0 # Code assumes that if non zero, then this item is an award
        if (len(args) >= 1 and isinstance(args[0], DatagramIterator)):
            # If we are called with di, versionNumber, store then we
            # meant to decode the CatalogItem from a datagram.
            self.decodeDatagram(*args, **kw)
        else:
            # Otherwise, we are creating a new CatalogItem.
            self.makeNewItem(*args, **kw)

    def isAward(self):
        """Return true if this catalog item is an award."""
        result = self.specialEventId != 0
        return result

    def makeNewItem(self):
        # This is to be used as the primary constructor-from-arguments
        # method for CatalogItem derivatives.
        pass
    
    def needsCustomize(self):
        # Returns true if the item still needs to be customized by the
        # user (e.g. by choosing a color).
        return 0

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 0
        
    def getBackSticky(self):
        #some items should hang around in the back catalog
        itemType = 0 #the types that should stick around
        numSticky = 0 #how many should stick around
        return itemType, numSticky

    def putInBackCatalog(self, backCatalog, lastBackCatalog):
        # Appends the item to the backCatalog.  For reference, the
        # current back catalog is passed in as well; this list will be
        # appended to the backCatalog after all items have been added
        # (so that older items appear at the end of the list).  It is
        # legal to modify the lastBackCatalog list.

        if self.saveHistory() and not self.isSaleItem():
            # There should be only one of a given item in the back
            # catalog at any given time.  If we get more than one, we
            # should remove the old one.
            if not self in backCatalog:
                if self in lastBackCatalog:
                    lastBackCatalog.remove(self)
                backCatalog.append(self)

    def replacesExisting(self):
        # Returns true if an item of this type will, when purchased,
        # replace an existing item of the same type, or false if items
        # accumulate.
        return 0

    def hasExisting(self):
        # If replacesExisting returns true, this returns true if an
        # item of this class is already owned by the avatar, false
        # otherwise.  If replacesExisting returns false, this is
        # undefined.
        return 0

    def getYourOldDesc(self):
        # If replacesExisting returns true, this returns the name of
        # the already existing object, in sentence construct: "your
        # old ...".  If replacesExisting returns false, this is undefined.
        return None

    def storedInCloset(self):
        # Returns true if this kind of item takes up space in the
        # avatar's closet, false otherwise.
        return 0

    def storedInAttic(self):
        # Returns true if this kind of item takes up space in the
        # avatar's attic, false otherwise.
        return 0

    def notOfferedTo(self, avatar):
        # Returns true if the item cannot be bought by the indicated
        # avatar (pass in the actual DistributdAvatarAI object), for
        # instance because the avatar already has one and cannot have
        # two.  This is normally called only on the AI side.
        return 0

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 0

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        return 0
        
    def hasBeenGifted(self, avatar):
        # returns true if this item is on your onGiftOrderList
        if avatar.onGiftOrder.count(self) != 0:
            # someone has given it to you
            return 1
        return 0

    def getTypeName(self):
        # Returns the name of the general type of item.
        # No need to localize this string; it should never be
        # displayed except in case of error.
        return "Unknown Type Item"

    def getName(self):
        # Returns the name of the item.

        # No need to localize this string; it should never be
        # displayed except in case of error.
        return "Unnamed Item"

    def getDisplayName(self):
        # Used in the catalog gui display
        return self.getName()

    def recordPurchase(self, avatar, optional):
        # Updates the appropriate field on the avatar to indicate the
        # purchase (or delivery).  This makes the item available to
        # use by the avatar.  This method is only called on the AI side.

        # The optional parameter may be 0 or some number passed up
        # from the client which has different meaning to the various
        # different kinds of CatalogItems (and may indicate, for
        # instance, the index number of the item to replace).

        # This should return one of the P_* tokens from ToontownGlobals.
        # If the return value is zero or positive, the item is removed
        # from the mailbox.
        
        self.notify.warning("%s has no purchase method." % (self))
        return ToontownGlobals.P_NoPurchaseMethod

    def isSaleItem(self):
        # Returns true if this particular item was tagged as a "sale"
        # item in the catalog generator.  This means (a) it has a
        # reduced price, and (b) it does not get placed in the
        # backorder catalog.
        return self.saleItem
        
    def isGift(self):
        return 1
        
    def isRental(self):
        return 0
        
    def forBoysOnly(self):
        return 0
            
    def forGirlsOnly(self):
        return 0
        
    def setLoyaltyRequirement(self, days):
        self.loyaltyDays = days
        
    def loyaltyRequirement(self):
        """Return. the number of days an account must have to purchase."""
        if not hasattr(self, "loyaltyDays"):
            return 0
        else:
            return self.loyaltyDays

    def getPrice(self, catalogType):
        assert(catalogType != CatalogTypeUnspecified)
        if catalogType == CatalogTypeBackorder:
            return self.getBackPrice()
        elif self.isSaleItem():
            return self.getSalePrice()
        else:
            return self.getCurrentPrice()

    def getCurrentPrice(self):
        # Returns the price of the item when it is listed in the
        # current catalog.
        return int(self.getBasePrice())

    def getBackPrice(self):
        # Returns the price of the item when it is listed in the back
        # catalog.
        return int(self.getBasePrice() * CatalogBackorderMarkup)

    def getSalePrice(self):
        # Returns the price of the item when it is listed in the
        # current catalog as a sale item.
        return int(self.getBasePrice() * CatalogSaleMarkdown)

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 0

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        assert (not self.hasPicture)
        self.hasPicture=True
        return (None, None)

    def cleanupPicture(self):
        assert self.hasPicture
        self.hasPicture=False
        
        

    def requestPurchase(self, phone, callback, optional=-1):
        # Orders the item via the indicated telephone.  Some items
        # will pop up a dialog querying the user for more information
        # before placing the order; other items will order
        # immediately.

        # In either case, the function will return immediately before
        # the transaction is finished, but the given callback will be
        # called later with two parameters: the return code (one of
        # the P_* symbols defined in ToontownGlobals.py), followed by the
        # item itself.

        # This method is only called on the client.

        assert(not self.needsCustomize())
        phone.requestPurchase(self, callback, optional)
        
    def requestGiftPurchase(self, phone, targetDoID,callback, optional=-1):
        # Orders the item via the indicated telephone.  Some items
        # will pop up a dialog querying the user for more information
        # before placing the order; other items will order
        # immediately.

        # In either case, the function will return immediately before
        # the transaction is finished, but the given callback will be
        # called later with two parameters: the return code (one of
        # the P_* symbols defined in ToontownGlobals.py), followed by the
        # item itself.

        # This method is only called on the client.
        
        # assert 0, "Gift Purchase"
        
        assert(not self.needsCustomize())
        phone.requestGiftPurchase(self, targetDoID, callback, optional)
        #base.cr.deliveryManager.sendRequestPurchaseGift(self, targetDoID, callback)


    def requestPurchaseCleanup(self):
        # This will be called on the client side to clean up any
        # objects created in requestPurchase(), above.
        pass

    def getRequestPurchaseErrorText(self, retcode):
        # PLEASE NOTE: this is not usually an error message, usually this returns a confiramtion -JML
        # Returns a string describing the error that occurred on
        # attempting to order the item from the phone.  The input
        # parameter is the retcode returned by
        # phone.requestPurchase().
        if retcode == ToontownGlobals.P_ItemAvailable: # worked can use right away
            return TTLocalizer.CatalogPurchaseItemAvailable
        elif retcode == ToontownGlobals.P_ItemOnOrder: # worked and will be delivered
            return TTLocalizer.CatalogPurchaseItemOnOrder 
        elif retcode == ToontownGlobals.P_MailboxFull: #failure messages
            return TTLocalizer.CatalogPurchaseMailboxFull
        elif retcode == ToontownGlobals.P_OnOrderListFull:
            return TTLocalizer.CatalogPurchaseOnOrderListFull
        else:
            return TTLocalizer.CatalogPurchaseGeneralError % (retcode)
            
    def getRequestGiftPurchaseErrorText(self, retcode):
        # PLEASE NOTE: this is not usually an error message, usually this returns a confiramtion -JML
        # Returns a string describing the error that occurred on
        # attempting to order the item from the phone.  The input
        # parameter is the retcode returned by
        # phone.requestPurchase().
        if retcode == ToontownGlobals.P_ItemAvailable: # worked can use right away
            return TTLocalizer.CatalogPurchaseGiftItemAvailable
        elif retcode == ToontownGlobals.P_ItemOnOrder: # worked and will be delivered
            return TTLocalizer.CatalogPurchaseGiftItemOnOrder 
        elif retcode == ToontownGlobals.P_MailboxFull: #failure messages
            return TTLocalizer.CatalogPurchaseGiftMailboxFull
        elif retcode == ToontownGlobals.P_OnOrderListFull:
            return TTLocalizer.CatalogPurchaseGiftOnOrderListFull
        elif retcode == ToontownGlobals.P_NotAGift:
            return TTLocalizer.CatalogPurchaseGiftNotAGift
        elif retcode == ToontownGlobals.P_WillNotFit:
            return TTLocalizer.CatalogPurchaseGiftWillNotFit
        elif retcode == ToontownGlobals.P_ReachedPurchaseLimit:
            return TTLocalizer.CatalogPurchaseGiftLimitReached
        elif retcode == ToontownGlobals.P_NotEnoughMoney:
            return TTLocalizer.CatalogPurchaseGiftNotEnoughMoney
        else:
            return TTLocalizer.CatalogPurchaseGiftGeneralError % {'friend' : "%s",'error' : retcode}

    def acceptItem(self, mailbox, index, callback):
        # Accepts the item from the mailbox.  Some items will pop up a
        # dialog querying the user for more information before
        # accepting the item; other items will accept it immediately.

        # In either case, the function will return immediately before
        # the transaction is finished, but the given callback will be
        # called later with three parameters: the return code (one of
        # the P_* symbols defined in ToontownGlobals.py), followed by
        # the item itself, and the supplied index number.

        # The index is the position of this item within the avatar's
        # mailboxContents list, which is used by the AI to know which
        # item to remove from the list (and also to doublecheck that
        # we're accepting the expected item).

        # This method is only called on the client.

        mailbox.acceptItem(self, index, callback)
        
    def discardItem(self, mailbox, index, callback):
        print("Item discardItem")
        # Discards the item from the mailbox.  
        # This method is only called on the client.

        mailbox.discardItem(self, index, callback)

    def acceptItemCleanup(self):
        # This will be called on the client side to clean up any
        # objects created in acceptItem(), above.
        pass

    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_NoRoomForItem:
            return TTLocalizer.CatalogAcceptRoomError
        elif retcode == ToontownGlobals.P_ReachedPurchaseLimit:
            return TTLocalizer.CatalogAcceptLimitError
        elif retcode == ToontownGlobals.P_WillNotFit:
            return TTLocalizer.CatalogAcceptFitError
        elif retcode == ToontownGlobals.P_InvalidIndex:
            return TTLocalizer.CatalogAcceptInvalidError
        else:
            return TTLocalizer.CatalogAcceptGeneralError % (retcode)

    def output(self, store = ~0):
        return "CatalogItem"

    def getFilename(self):
        # This returns a filename if it makes sense for the particular
        # item.  This is only used for documentation purposes.
        return ""

    def getColor(self):
        # This returns a VBase4 color which is applied to the above
        # filename, if it makes sense for the particular item.  This
        # may be used for documentation purposes, but some item types
        # define this specifically for their own use.
        return None

    def formatOptionalData(self, store = ~0):
        # This is used within output() to format optional data
        # (according to the bits indicated in store).
        result = ""
        if (store & Location) and self.posHpr != None:
            result += ", posHpr = (%s, %s, %s, %s, %s, %s)" % (self.posHpr)
        return result
    
    def __str__(self):
        return self.output()
    
    def __repr__(self):
        return self.output()

    def compareTo(self, other):
        # All CatalogItem type objects are equivalent.
        # Specializations of this class will redefine this method
        # appropriately.
        return 0

    def getHashContents(self):
        # Specializations of this class will redefine this method to
        # return whatever pieces of the class are uniquely different
        # to each instance.
        return None

    def __cmp__(self, other):
        # If the classes are different, they must be different objects.
        c = cmp(self.__class__, other.__class__)
        if c != 0:
            return c

        # Otherwise, they are the same class; use compareTo.
        return self.compareTo(other)

    def __hash__(self):
        return hash((self.__class__, self.getHashContents()))

    def getBasePrice(self):
        return 0

    def loadModel(self):
        return None

    def decodeDatagram(self, di, versionNumber, store):
        if store & DeliveryDate:
            self.deliveryDate = di.getUint32()
        if store & Location:
            x = di.getArg(STInt16, 10)
            y = di.getArg(STInt16, 10)
            z = di.getArg(STInt16, 100)
            if versionNumber < 2:
                h = di.getArg(STInt16, 10)
                p = 0.0
                r = 0.0
            elif versionNumber < 5:
                h = di.getArg(STInt8, 256.0/360.0)
                p = di.getArg(STInt8, 256.0/360.0)
                r = di.getArg(STInt8, 256.0/360.0)
                hpr = oldToNewHpr(VBase3(h, p, r))
                h = hpr[0]
                p = hpr[1]
                r = hpr[2]
            else:
                h = di.getArg(STInt8, 256.0/360.0)
                p = di.getArg(STInt8, 256.0/360.0)
                r = di.getArg(STInt8, 256.0/360.0)
                
            self.posHpr = (x, y, z, h, p, r)
        if store & GiftTag:
            self.giftTag = di.getString()
        if versionNumber >= 8:
            self.specialEventId = di.getUint8()
        else:
            self.specialEventId = 0

    def encodeDatagram(self, dg, store):
        if store & DeliveryDate:
            dg.addUint32(self.deliveryDate)
        if store & Location:
            dg.putArg(self.posHpr[0], STInt16, 10)
            dg.putArg(self.posHpr[1], STInt16, 10)
            dg.putArg(self.posHpr[2], STInt16, 100)
            dg.putArg(self.posHpr[3], STInt8, 256.0/360.0)
            dg.putArg(self.posHpr[4], STInt8, 256.0/360.0)
            dg.putArg(self.posHpr[5], STInt8, 256.0/360.0)
        if store & GiftTag:
            dg.addString(self.giftTag)
        dg.addUint8(self.specialEventId)
    
    def getTypeCode(self):
        import CatalogItemTypes
        return CatalogItemTypes.CatalogItemTypes[self.__class__]

    def applyColor(self, model, colorDesc):
        """

        This method is used to apply a color/texture description to
        a model.  The colorDesc is a list of tuples, each of which has
        one of the forms:

        (partName, None) - hide the given part(s)
        (partName, "texture name") - apply the texture to the given part(s)
        (partName, (r, g, b, a)) - apply the color to the given part(s)

        """
        if model == None or colorDesc == None:
            return
        for partName, color in colorDesc:
            matches = model.findAllMatches(partName)
            if (color == None):
                matches.hide()

            elif isinstance(color, types.StringType):
                tex = loader.loadTexture(color)
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                for i in range(matches.getNumPaths()):
                    matches.getPath(i).setTexture(tex, 1)

            else:
                needsAlpha = (color[3] != 1)
                color = VBase4(color[0], color[1], color[2], color[3])
                for i in range(matches.getNumPaths()):
                    #matches.getPath(i).setColor(color, 1)
                    matches.getPath(i).setColorScale(color, 1)
                    if needsAlpha:
                        matches.getPath(i).setTransparency(1)

    def makeFrame(self):
        # Returns a DirectFrame suitable for holding models returned
        # by getPicture().
        
        # Don't import this at the top of the file, since this code
        # must run on the AI.
        from direct.gui.DirectGui import DirectFrame

        frame = DirectFrame(parent = hidden,
                            frameSize = (-1.0, 1.0, -1.0, 1.0),
                            relief = None,
                            )
        return frame

    def makeFrameModel(self, model, spin = 1):
        # Returns a (DirectWidget, Interval) pair to spin the
        # indicated model, an arbitrary NodePath, on a panel.  Called
        # only on the client, from getPicture(), by derived classes
        # like CatalogFurnitureItem and CatalogClothingItem.

        frame = self.makeFrame()
        ival = None
        if model:
            # This 3-d model will be drawn in the 2-d scene.
            model.setDepthTest(1)
            model.setDepthWrite(1)

            if spin:
                # We need two nested nodes: one to pitch down to the user,
                # and one to rotate.
                pitch = frame.attachNewNode('pitch')
                rotate = pitch.attachNewNode('rotate')
                scale = rotate.attachNewNode('scale')
                model.reparentTo(scale)
                # Translate model to the center.
                bMin,bMax = model.getTightBounds()
                center = (bMin + bMax)/2.0
                model.setPos(-center[0], -center[1], -center[2])
                pitch.setP(20)
                # Scale the model to fit within a 2x2 box
                bMin,bMax = pitch.getTightBounds()
                center = (bMin + bMax)/2.0
                corner = Vec3(bMax - center)
                #scale.setScale(1.0/corner[2])
                scale.setScale(1.0/max(corner[0],corner[1],corner[2]))
                pitch.setY(2)
                ival = LerpHprInterval(rotate, 10, VBase3(-270, 0, 0),
                                       startHpr = VBase3(90, 0, 0))
            else:
                # This case is simpler, we do not need all the extra nodes
                scale = frame.attachNewNode('scale')
                model.reparentTo(scale)
                # Translate model to the center.
                bMin,bMax = model.getTightBounds()
                center = (bMin + bMax)/2.0
                model.setPos(-center[0], 2, -center[2])
                corner = Vec3(bMax - center)
                #scale.setScale(1.0/corner[2])
                scale.setScale(1.0/max(corner[0],corner[1],corner[2]))
                
        return (frame, ival)

    def getBlob(self, store = 0):
        dg = PyDatagram()
        dg.addUint8(CatalogItemVersion)
        encodeCatalogItem(dg, self, store)
        return dg.getMessage()
        

    def getRequestPurchaseErrorTextTimeout(self):
        """
        #RAU How long do we display RequestPurchaseErrorText.
        Created since we need to display the text longer for garden supplies
        """
        return 6

    def getDaysToGo(self, avatar):
        """Return the number of days the toon has to wait before he can buy this."""
        accountDays = avatar.getAccountDays()
        daysToGo = self.loyaltyRequirement() - accountDays
        if daysToGo <0:
            daysToGo = 0
        return int(daysToGo)
                

def encodeCatalogItem(dg, item, store):
    """encodeCatalogItem

    Encodes a CatalogItem of some type into the datagram stream,
    writing the type number first so that decodeCatalogItem() can
    successfully decode it.
    """
    import CatalogItemTypes
    flags = item.getTypeCode()
    if item.isSaleItem():
        flags |= CatalogItemTypes.CatalogItemSaleFlag
    if item.giftTag != None:
          flags |= CatalogItemTypes.CatalogItemGiftTag  
    dg.addUint8(flags)
    if item.giftTag != None:
        dg.addUint32(item.giftTag)
        if not item.giftCode:
            item.giftCode = 0        
        dg.addUint8(item.giftCode)
    else:
        pass
        #print("No Gift Tag")
    
    item.encodeDatagram(dg, store)


def decodeCatalogItem(di, versionNumber, store):
    """decodeCatalogItem

    This function decodes a CatalogItem of an unknown type from the
    given datagram stream, reversing the logic used by
    encodeCatalogItem().  The new catalog item is returned.
    """

    import CatalogItemTypes
    global CatalogReverseType
    if CatalogReverseType == None:
        # First, we have to create the reverse lookup.
        CatalogReverseType = {}
        for itemClass, index in CatalogItemTypes.CatalogItemTypes.items():
            CatalogReverseType[index] = itemClass

    startIndex = di.getCurrentIndex()
    try:
        flags = di.getUint8()
        typeIndex = flags & CatalogItemTypes.CatalogItemTypeMask
        gift = None
        code = None
        if flags & CatalogItemTypes.CatalogItemGiftTag:  

             gift = di.getUint32()
             code = di.getUint8()
        else:

            pass
        itemClass = CatalogReverseType[typeIndex]
        item = itemClass(di, versionNumber, store = store)
        
    except Exception, e:
        CatalogItem.notify.warning("Invalid catalog item in stream: %s, %s" % (
            sys.exc_info()[0], e))
        d = Datagram(di.getDatagram().getMessage()[startIndex:])
        d.dumpHex(Notify.out())
        #import pdb; pdb.set_trace()#debug on invalid catalog items
        import CatalogInvalidItem
        return CatalogInvalidItem.CatalogInvalidItem()

    if flags & CatalogItemTypes.CatalogItemSaleFlag:
        item.saleItem = 1
    item.giftTag = gift
    item.giftCode = code
       
    return item


def getItem(blob, store = 0):
    """getItem

    Returns the CatalogItem written by a previous call to item.getBlob().
    """
    dg = PyDatagram(blob)
    di = PyDatagramIterator(dg)
    try:
        versionNumber = di.getUint8()
        return decodeCatalogItem(di, versionNumber, store)
    except Exception, e:
        CatalogItem.notify.warning("Invalid catalog item: %s, %s" % (
            sys.exc_info()[0], e))
        dg.dumpHex(Notify.out())
        import CatalogInvalidItem
        return CatalogInvalidItem.CatalogInvalidItem()
