import CatalogItem
import CatalogAtticItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from CatalogSurfaceColors import *

# Surface type.  This must be a contiguous series in the range 0-3 to
# index into DistributedHouse.activeWallpaper.
STWallpaper = 0
STMoulding = 1
STFlooring = 2
STWainscoting = 3
NUM_ST_TYPES = 4

class CatalogSurfaceItem(CatalogAtticItem.CatalogAtticItem):
    """CatalogSurfaceItem

    Parent class for all house surface items (wallpapers, flooring
    moulding, and wainscotings.  These specify the texture/color
    combination for walls and trim.
    """

    def makeNewItem(self):
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)
        
    def setPatternIndex(self, patternIndex):
        self.patternIndex = patternIndex

    def setColorIndex(self, colorIndex):
        self.colorIndex = colorIndex

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def recordPurchase(self, avatar, optional):
        # Updates the appropriate field on the avatar to indicate the
        # purchase (or delivery).  This makes the item available to
        # use by the avatar.  This method is only called on the AI side.
        self.giftTag = None
        house, retcode = self.getHouseInfo(avatar)
        if retcode >= 0:
            house.addWallpaper(self)
        return retcode

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 60  # 1 hour.

