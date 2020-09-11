from direct.distributed import DistributedObject
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogItemList
from direct.directnotify.DirectNotifyGlobal import *

class DistributedFurnitureManager(DistributedObject.DistributedObject):

    notify = directNotify.newCategory("DistributedFurnitureManager")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.director = 0
        self.dfitems = []

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept("releaseDirector", self.releaseDirector)
        
    def disable(self):
        self.ignoreAll()
        if self.cr.furnitureManager == self:
            self.cr.furnitureManager = None
        base.localAvatar.setFurnitureDirector(0, self)
        self.director = 0
        self.notify.debug("disable")
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        self.notify.debug("delete")
        DistributedObject.DistributedObject.delete(self)
        

    def setOwnerId(self, ownerId):
        # Specifies the avatar who owns this furniture.  If this is
        # localtoon, then the FurnitureManager is made accessible
        # globally.
        self.ownerId = ownerId
        if self.ownerId == base.localAvatar.doId:
            self.cr.furnitureManager = self
            if self.cr.objectManager == None:
                import houseDesign
                self.cr.objectManager = houseDesign.ObjectManager()

    def setOwnerName(self, name):
        # Specifies the avatar who owns this furniture.
        self.ownerName = name

    def setInteriorId(self, interiorId):
        # Specifies the doId of the DistributedHouseInterior object
        # that we are moving furniture around for.
        self.interiorId = interiorId

    def getInteriorObject(self):
        # Returns the DistributedHouseInterior we are operating on, or
        # None if there is a problem.
        return self.cr.doId2do.get(self.interiorId)

    def setAtticItems(self, items):
        self.atticItems = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization)

    def setAtticWallpaper(self, items):
        self.atticWallpaper = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization)

    def setAtticWindows(self, items):
        self.atticWindows = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization)

    def setDeletedItems(self, items):
        self.deletedItems = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization)

    def releaseDirector(self):
        # Tells the AI that we are done being the director.
        if self.director == base.localAvatar.doId:
            self.d_suggestDirector(0)

            # We'll boldly send this message locally, without
            # bothering to wait for a reply from the AI.  We assume
            # the AI won't reject our request to stop being the
            # director.
            self.setDirector(0)

    def d_suggestDirector(self, avId):
        # Sends a request to the AI to give the controls to avId (who
        # may be myself or someone else).
        self.sendUpdate("suggestDirector", [avId])

    def setDirector(self, avId):
        # A message from the AI that the controls are being handed to
        # avId, possibly interrupting someone else.
        self.notify.info("Furniture director is now %s" % (avId))
        base.localAvatar.setFurnitureDirector(avId, self)
        self.director = avId

    def d_avatarEnter(self):
        # Informs the AI that we have entered furniture mode.
        self.sendUpdate("avatarEnter", [])

    def d_avatarExit(self):
        # Informs the AI that we are done with furniture mode.
        self.sendUpdate("avatarExit", [])

    def moveItemToAttic(self, dfitem, callback):
        # Requests the AI to move the indicated
        # DistributedFurnitureItem to the attic.  The callback will be
        # called when the operation is complete with two parameters:
        # a ToontownGlobals.FM_* code, followed by the dfitem.item.
        # If successful, the original dfitem will already have been
        # deleted.
        
        context = self.getCallbackContext(callback, [dfitem.item])
        self.sendUpdate("moveItemToAtticMessage", [dfitem.doId, context])

    def moveItemFromAttic(self, index, posHpr, callback):
        # Requests the AI to move the nth item from the attic into the
        # world at the indicated position.  The callback will be
        # called when the operation is complete with three parameters:
        # a ToontownGlobals.FM_* code, followed by the newly generated
        # DistributedFurnitureItem, followed by the supplied item
        # index.
        
        context = self.getCallbackContext(callback, [index])
        self.sendUpdate("moveItemFromAtticMessage",
                        [index, posHpr[0], posHpr[1], posHpr[2],
                         posHpr[3], posHpr[4], posHpr[5], context])

    def deleteItemFromAttic(self, item, index, callback):
        # Requests the AI to delete the nth item from the attic.  The
        # callback will be called when the operation is complete with
        # three parameters: ToontownGlobals.FM_* code, followed by the
        # item and the index.

        # The item and its index number are both passed in as a
        # doublecheck safeguard, to ensure against the AI possibly
        # being out of sync with the client in its list of atticItems.
        
        context = self.getCallbackContext(callback, [item, index])
        blob = item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("deleteItemFromAtticMessage", [blob, index, context])

    def deleteItemFromRoom(self, dfitem, callback):
        # Requests the AI to delete the nth item from the room.  The
        # callback will be called when the operation is complete with
        # two parameters: ToontownGlobals.FM_* code, followed by the
        # dfitem.item.  If successful, the original dfitem will
        # already have been deleted.
        
        context = self.getCallbackContext(callback, [dfitem.item])
        blob = dfitem.item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("deleteItemFromRoomMessage", [blob, dfitem.doId, context])

    def moveWallpaperFromAttic(self, index, room, callback):
        # Requests the AI to move the nth wallpaper item from the
        # wallpaper attic into the world at the indicated room index.
        # The same-type wallpaper currently occupying that room is
        # moved back into the attic in the same position.  The
        # callback will be called when the operation is complete with
        # three parameters: a ToontownGlobals.FM_* code, followed by the
        # item index and the room index.
        
        context = self.getCallbackContext(callback, [index, room])
        self.sendUpdate("moveWallpaperFromAtticMessage",
                        [index, room, context])

    def deleteWallpaperFromAttic(self, item, index, callback):
        # Requests the AI to delete the nth wallpaper item from the
        # wallpaper attic.  The callback will be called when the
        # operation is complete with three parameters: a
        # ToontownGlobals.FM_* code, followed by the item and the
        # index.

        # The item and its index number are both passed in as a
        # doublecheck safeguard, to ensure against the AI possibly
        # being out of sync with the client in its list of
        # atticWallpapers.
        
        context = self.getCallbackContext(callback, [item, index])
        blob = item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("deleteWallpaperFromAtticMessage", [blob, index, context])

    def moveWindowToAttic(self, slot, callback):
        # Requests the AI to move the window in the indicated
        # placement slot to the attic.  The slot is left as a blank
        # wall.

        # The callback will be called when the operation is complete
        # with two parameters: a ToontownGlobals.FM_* code, followed
        # by the placement slot.
        
        context = self.getCallbackContext(callback, [slot])
        self.sendUpdate("moveWindowToAtticMessage", [slot, context])

    def moveWindowFromAttic(self, index, slot, callback):
        # Requests the AI to move the nth window item from the window
        # attic into the world in the indicated placement slot.  If
        # there is already a window at that slot, it is returned to
        # the attic (and FM_SwappedItem is generated); otherwise, the
        # window is moved out of the attic (and FM_MovedItem is
        # generated).

        # The callback will be called when the operation is complete
        # with three parameters: a ToontownGlobals.FM_* code, followed
        # by the item index, and the placement slot index.
        
        context = self.getCallbackContext(callback, [index, slot])
        self.sendUpdate("moveWindowFromAtticMessage",
                        [index, slot, context])

    def moveWindow(self, fromSlot, toSlot, callback):

        # Requests the AI to move the window occupying the indicate
        # placement slot to the indicate destination slot.  If there
        # is already a window at that slot, it is returned to the
        # attic (and FM_SwappedItem is generated); otherwise, the
        # window is moved in place (and FM_MovedItem is generated).

        # The callback will be called when the operation is complete
        # with three parameters: a ToontownGlobals.FM_* code, followed
        # by the from and to slot numbers.
        
        context = self.getCallbackContext(callback, [fromSlot, toSlot])
        self.sendUpdate("moveWindowMessage",
                        [fromSlot, toSlot, context])

    def deleteWindowFromAttic(self, item, index, callback):
        # Requests the AI to delete the nth window item from the
        # window attic.  The callback will be called when the
        # operation is complete with three parameters: a
        # ToontownGlobals.FM_* code, followed by the item and the
        # index.

        # The item and its index number are both passed in as a
        # doublecheck safeguard, to ensure against the AI possibly
        # being out of sync with the client in its list of
        # atticWindows.
        
        context = self.getCallbackContext(callback, [item, index])
        blob = item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("deleteWindowFromAtticMessage", [blob, index, context])

    def recoverDeletedItem(self, item, index, callback):
        # Requests the AI to recover the nth window item from the
        # deleted item list.  The callback will be called when the
        # operation is complete with three parameters: a
        # ToontownGlobals.FM_* code, followed by the item and the
        # supplied index.

        # The item and its index number are both passed in as a
        # doublecheck safeguard, to ensure against the AI possibly
        # being out of sync with the client in its list of
        # deletedItems.
        
        context = self.getCallbackContext(callback, [item, index])
        blob = item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("recoverDeletedItemMessage", [blob, index, context])


    def moveItemToAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def moveItemFromAtticResponse(self, retcode, objectId, context):
        if retcode >= 0:
            dfitem = base.cr.doId2do[objectId]
        else:
            dfitem = None
        self.doCallbackContext(context, [retcode, dfitem])

    def deleteItemFromAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def deleteItemFromRoomResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def moveWallpaperFromAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def deleteWallpaperFromAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def moveWindowToAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def moveWindowFromAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def moveWindowResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def deleteWindowFromAtticResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])

    def recoverDeletedItemResponse(self, retcode, context):
        self.doCallbackContext(context, [retcode])
