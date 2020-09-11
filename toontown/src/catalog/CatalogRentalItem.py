import CatalogItem
import time
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.toontowngui import TTDialog

class CatalogRentalItem(CatalogItem.CatalogItem):
    """CatalogRentalItem

    This is an item that goes away after a period of time.

    """

    def makeNewItem(self, typeIndex, duration, cost):
        self.typeIndex = typeIndex
        self.duration = duration # duration is in minutes
        self.cost = cost
        # this will need to be persistant (db?)
        CatalogItem.CatalogItem.makeNewItem(self)
        
    def getDuration(self):
        return self.duration
    # TODO: who will check for expired items? CatalogManagerAI?
    
    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 0
        
    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder \
           or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        return 0
        
    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1
        
    def getTypeName(self):
        # Returns the name of the general type of item.
        return TTLocalizer.RentalTypeName
        
        
    def getName(self):
        hours = int(self.duration / 60)
        if self.typeIndex == ToontownGlobals.RentalCannon:
            return ("%s %s %s %s" % (hours, TTLocalizer.RentalHours, TTLocalizer.RentalOf , TTLocalizer.RentalCannon))
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            return ("%s %s %s" % (hours, TTLocalizer.RentalHours, TTLocalizer.RentalGameTable))
        else:
            return TTLocalizer.RentalTypeName
            

    def recordPurchase(self, avatar, optional):
        self.notify.debug("rental -- record purchase")
        #if avatar:
        #   avatar.addMoney(self.beanAmount)

        if avatar:
            self.notify.debug("rental -- has avater")
            #zoneId = avatar.zoneId
            #estateOwnerDoId = simbase.air.estateMgr.zone2owner.get(zoneId)
            estate = simbase.air.estateMgr.estate.get(avatar.doId)
            if estate:
                self.notify.debug("rental -- has estate")
                estate.rentItem(self.typeIndex, self.duration)
            else:
                self.notify.debug("rental -- something not there")    
                
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        scale = 1
        heading = 0
        pitch = 30
        roll = 0
        spin = 1
        down = -1
        if self.typeIndex == ToontownGlobals.RentalCannon:
            model = loader.loadModel("phase_4/models/minigames/toon_cannon")
            scale = .5
            heading = 45
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            model = loader.loadModel("phase_6/models/golf/game_table")
        assert (not self.hasPicture)
        self.hasPicture = True

        return self.makeFrameModel(model, spin)

    def output(self, store = ~0):
        return "CatalogRentalItem(%s%s)" % (
            self.typeIndex,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.typeIndex - other.typeIndex

    def getHashContents(self):
        return self.typeIndex

    def getBasePrice(self):
        if self.typeIndex == ToontownGlobals.RentalCannon:
            return self.cost
        elif self.typeIndex == ToontownGlobals.RentalGameTable:
            return self.cost
        else:
            return 50

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        if versionNumber >= 7:
            # we normally add new fields at the end, but this was already added at the start
            # and I didn't want to make the situation worst
            self.cost = di.getUint16()
        else:
            self.cost = 1000
        self.duration = di.getUint16()
        self.typeIndex = di.getUint16()
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.cost)
        dg.addUint16(self.duration)
        dg.addUint16(self.typeIndex)
        
    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 1  # 1 minute.
        
    def isRental(self):
        return 1
        
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
        self.confirmRent = TTDialog.TTGlobalDialog(
            doneEvent = "confirmRent",
            message = TTLocalizer.MessageConfirmRent,
            command = Functor(self.handleRentConfirm, mailbox, index, callback),
            style = TTDialog.TwoChoice)
        #self.confirmRent.msg = msg
        self.confirmRent.show()
        #self.accept("confirmRent", Functor(self.handleRentConfirm, mailbox, index, callback))
        #self.__handleRentConfirm)
        #self.mailbox = mailbox
        #self.mailIndex = index
        #self.mailcallback = callback
        
    def handleRentConfirm(self, mailbox, index, callback, choice):
    #def handleRentConfirm(self, *args):
        #print(args)
        if choice > 0:
            mailbox.acceptItem(self, index, callback)
        else:
            callback(ToontownGlobals.P_UserCancelled, self, index)
        if self.confirmRent:
            self.confirmRent.cleanup()
            self.confirmRent = None
        
    
def getAllRentalItems():
    # Returns a list of all valid CatalogRentalItems.
    list = []
    # no game tables for now
    # TODO since all we offer so far is 48 hours of cannons, values pulled for CatalogGenerator
    # do something else if we have different durations
    for rentalType in (ToontownGlobals.RentalCannon, ):
        list.append(CatalogRentalItem(rentalType,2880,1000))
    return list
