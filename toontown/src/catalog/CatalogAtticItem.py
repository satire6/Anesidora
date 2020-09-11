import CatalogItem
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals

class CatalogAtticItem(CatalogItem.CatalogItem):
    """CatalogAtticItem

    This is a base class for a family of items (CatalogFurnitureItem,
    CatalogWindowItem, CatalogWallpaperItem) that must all be stored
    in the player's attic.  It contains some common methods that check
    for space available in the attic.

    """

    def storedInAttic(self):
        # Returns true if this kind of item takes up space in the
        # avatar's attic, false otherwise.
        return 1

    def isDeletable(self):
        # Returns true if the item can be deleted from the attic,
        # false otherwise.
        return 1

    def getHouseInfo(self, avatar):
        # Looks up the house for the avatar, and checks the available
        # space in the attic.  A helper function for recordPurchase().

        # Returns a pair: (house, retcode), where house is the house
        # object if it can be determined, and retcode is the return
        # code if there is a failure.  If retcode is positive the
        # object should be added to the attic.

        houseId = avatar.houseId
        if not houseId:
            self.notify.warning("Avatar %s has no houseId associated." % (avatar.doId))
            return (None, ToontownGlobals.P_InvalidIndex)
        house = simbase.air.doId2do.get(houseId)
        if not house:
            self.notify.warning("House %s (for avatar %s) not instantiated." % (houseId, avatar.doId))
            return (None, ToontownGlobals.P_InvalidIndex)

        numAtticItems = len(house.atticItems) + len(house.atticWallpaper) + len(house.atticWindows)
        numHouseItems = numAtticItems + len(house.interiorItems)
        if numHouseItems >= ToontownGlobals.MaxHouseItems and \
           not self.replacesExisting():
            # No more room in the house.
            return (house, ToontownGlobals.P_NoRoomForItem)

        return (house, ToontownGlobals.P_ItemAvailable)

    def requestPurchase(self, phone, callback):
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
        from toontown.toontowngui import TTDialog
        avatar = base.localAvatar

        itemsOnOrder = 0
        for item in avatar.onOrder + avatar.mailboxContents:
            if item.storedInAttic() and not item.replacesExisting():
                itemsOnOrder += 1

        numHouseItems = phone.numHouseItems + itemsOnOrder
        if numHouseItems >= ToontownGlobals.MaxHouseItems and \
           not self.replacesExisting():
            # If the avatar's house is full, pop up a dialog warning
            # the user, and give him a chance to bail out.
            self.requestPurchaseCleanup()
            buttonCallback = PythonUtil.Functor(
                self.__handleFullPurchaseDialog, phone, callback)
            self.dialog = TTDialog.TTDialog(
                style = TTDialog.YesNo,
                text = TTLocalizer.CatalogPurchaseHouseFull,
                text_wordwrap = 15,
                command = buttonCallback,
                )
            self.dialog.show()

        else:
            # The avatar's house isn't full; just buy it.
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)

    def requestPurchaseCleanup(self):
        if hasattr(self, "dialog"):
            self.dialog.cleanup()
            del self.dialog

    def __handleFullPurchaseDialog(self, phone, callback, buttonValue):
        from toontown.toontowngui import TTDialog
        self.requestPurchaseCleanup()
        if buttonValue == DGG.DIALOG_OK:
            # Go ahead and purchase it.
            CatalogItem.CatalogItem.requestPurchase(self, phone, callback)
        else:
            # Don't purchase it.
            callback(ToontownGlobals.P_UserCancelled, self)
        

    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptInAttic
        elif retcode == ToontownGlobals.P_NoRoomForItem:
            return TTLocalizer.CatalogAcceptHouseFull
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)
    
