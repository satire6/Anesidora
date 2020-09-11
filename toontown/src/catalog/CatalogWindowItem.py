from pandac.PandaModules import *
import CatalogAtticItem
import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer


WVTModelName = 0
WVTBasePrice = 1
WVTSkyName = 2

# These index numbers are written to the database.  Don't mess with them.
# Also see TTLocalizer.WindowViewNames.

# The third entry in the is the name of the backdrop node for a hack Drose
# and I put in to fix some draw order problems in the render2d drawing
# of the window views. If not None, we find the node and do some hacky
# rendering/draworder/binning tricks to get it to draw properly behind
# alpha'd items in front of it.

WindowViewTypes = {
    10 : ("phase_5.5/models/estate/Garden1", 900, None),
    20 : ("phase_5.5/models/estate/GardenA", 900, None),         # Initial View
    30 : ("phase_5.5/models/estate/GardenB", 900, None),
    40 : ("phase_5.5/models/estate/cityView", 900, None),        # Catalog Series 1
    50 : ("phase_5.5/models/estate/westernView", 900, None),     # Catalog Series 2
    60 : ("phase_5.5/models/estate/underwaterView", 900, None),  # Catalog Series 2
    70 : ("phase_5.5/models/estate/tropicView", 900, None),      # Catalog Series 1
    80 : ("phase_5.5/models/estate/spaceView", 900, None),       # Catalog Series 2
    90 : ("phase_5.5/models/estate/PoolView", 900, None),        # Catalog Series 3
    100 : ("phase_5.5/models/estate/SnowView", 900, None),       # Catalog Series 3
    110 : ("phase_5.5/models/estate/FarmView", 900, None),       # Catalog Series 3
    120 : ("phase_5.5/models/estate/IndianView", 900, None),     # Catalog Series 4
    130 : ("phase_5.5/models/estate/WesternMainStreetView", 900, None),    # Catalog Series 4
    # Warning!  8-bit index number.  255 max value.
    }

class CatalogWindowItem(CatalogAtticItem.CatalogAtticItem):
    """CatalogWindowItem

    # This represents a view to hang outside a window in a house.
    
    """
    
    def makeNewItem(self, windowType, placement = None):
        self.windowType = windowType
        self.placement = placement
        CatalogAtticItem.CatalogAtticItem.makeNewItem(self)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.WindowViewTypeName

    def getName(self):
        return TTLocalizer.WindowViewNames.get(self.windowType)

    def recordPurchase(self, avatar, optional):
        # Updates the appropriate field on the avatar to indicate the
        # purchase (or delivery).  This makes the item available to
        # use by the avatar.  This method is only called on the AI side.
        self.giftTag = None
        house, retcode = self.getHouseInfo(avatar)
        if retcode >= 0:
            house.addWindow(self)
        return retcode

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 4 * 60  # 4 hours.
    
    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.
        frame = self.makeFrame()
        model = self.loadModel()

        # This 3-d model will be drawn in the 2-d scene.
        model.setDepthTest(1)
        model.setDepthWrite(1)

        # Set up clipping planes to cut off the parts of the view that
        # would extend beyond the frame.
        clipperLeft = PlaneNode('clipper')
        clipperRight = PlaneNode('clipper')
        clipperTop = PlaneNode('clipper')
        clipperBottom = PlaneNode('clipper')
        clipperLeft.setPlane(Plane(Vec3(1, 0, 0), Point3(-1, 0, 0)))
        clipperRight.setPlane(Plane(Vec3(-1, 0, 0), Point3(1, 0, 0)))
        clipperTop.setPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 1)))
        clipperBottom.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -1)))
        model.setClipPlane(frame.attachNewNode(clipperLeft))
        model.setClipPlane(frame.attachNewNode(clipperRight))
        model.setClipPlane(frame.attachNewNode(clipperTop))
        model.setClipPlane(frame.attachNewNode(clipperBottom))

        # Fix draw order of background
        bgName = WindowViewTypes[self.windowType][WVTSkyName]
        if bgName:
            bgNodePath = model.find("**/" + bgName)
            if not bgNodePath.isEmpty():
                # Put it at the front of the list to be drawn first
                bgNodePath.reparentTo(model, -1)
        
        # Get rid of the window frame that is in the model
        windowFrame = model.find("**/frame")
        if not windowFrame.isEmpty():
            windowFrame.removeNode()
            
        model.setPos(0,2,0)
        model.setScale(0.4)
        model.reparentTo(frame)

        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogWindowItem(%s%s)" % (
            self.windowType,
            self.formatOptionalData(store))

    def getFilename(self):
        type = WindowViewTypes[self.windowType]
        return type[WVTModelName]

    def formatOptionalData(self, store = ~0):
        # This is used within output() to format optional data
        # (according to the bits indicated in store).
        result = CatalogAtticItem.CatalogAtticItem.formatOptionalData(self, store)
        if (store & CatalogItem.WindowPlacement) and self.placement != None:
            result += ", placement = %s" % (self.placement)
        return result

    def compareTo(self, other):
        return self.windowType - other.windowType

    def getHashContents(self):
        return self.windowType

    def getBasePrice(self):
        return WindowViewTypes[self.windowType][WVTBasePrice]

    def loadModel(self):
        type = WindowViewTypes[self.windowType]
        model = loader.loadModel(type[WVTModelName])

        return model

    def decodeDatagram(self, di, versionNumber, store):
        CatalogAtticItem.CatalogAtticItem.decodeDatagram(self, di, versionNumber, store)
        self.placement = None
        if store & CatalogItem.WindowPlacement:
            self.placement = di.getUint8()
        self.windowType = di.getUint8()

        # The following will generate an exception if
        # self.windowType is invalid.
        wvtype = WindowViewTypes[self.windowType]

    def encodeDatagram(self, dg, store):
        CatalogAtticItem.CatalogAtticItem.encodeDatagram(self, dg, store)
        if store & CatalogItem.WindowPlacement:
            dg.addUint8(self.placement)
        dg.addUint8(self.windowType)
