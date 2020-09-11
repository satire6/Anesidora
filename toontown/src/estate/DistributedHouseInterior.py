""" DistributedHouseInterior module"""

from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
import HouseGlobals
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogSurfaceItem
from toontown.catalog import CatalogWallpaperItem
from toontown.catalog import CatalogFlooringItem
from toontown.catalog import CatalogMouldingItem
from toontown.catalog import CatalogWainscotingItem

WindowPlugNames = (
    "**/windowcut_a*",
    "**/windowcut_b*",
    "**/windowcut_c*",
    "**/windowcut_d*",
    "**/windowcut_e*",
    "**/windowcut_f*",
    )

RoomNames = (
    "**/group2",
    "**/group1",
    )
        
WallNames = ("ceiling*", "wall_side_middle*", "wall_front_middle*",
             "windowcut_*")
MouldingNames = ("wall_side_top*", "wall_front_top*")
FloorNames = ("floor*",)
WainscotingNames = ("wall_side_bottom*", "wall_front_bottom*")
BorderNames = ("wall_side_middle*_border", "wall_front_middle*_border",
               "windowcut_*_border")
        
WallpaperPieceNames = (WallNames, MouldingNames, FloorNames, WainscotingNames,
                       BorderNames)

class DistributedHouseInterior(DistributedObject.DistributedObject):
    """
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedHouseInterior')
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        self.houseId = 0
        self.houseIndex = 0
        self.interior = None

        self.exteriorWindowsHidden = 0
        
    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        DistributedObject.DistributedObject.generate(self)
    
    def announceGenerate(self):
        assert(self.debugPrint("announceGenerate()"))
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        assert(self.debugPrint("disable()"))
        self.interior.removeNode()
        del self.interior
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        assert(self.debugPrint("delete()"))
        self.ignore(self.uniqueName('enterclosetSphere'))
        DistributedObject.DistributedObject.delete(self)
    
    def setup(self):
        assert(self.debugPrint("setup()"))

        dnaStore=base.cr.playGame.dnaStore

        # Load the interior for this house
        self.interior = loader.loadModel("phase_5.5/models/estate/tt_m_ara_int_estateHouseA")

        assert(self.interior != None)
        self.interior.reparentTo(render)
        
        # Door:
        doorModelName="door_double_round_ur" # hack  zzzzzzz
        door=dnaStore.findNode(doorModelName)
        # Determine where should we put the door:
        door_origin=self.interior.find("**/door_origin")
        door_origin.setHpr(180,0,0)
        # The rooms are too small for doors:
        door_origin.setScale(0.8, 0.8, 0.8)
        # Move the origin away from the wall so it does not shimmer
        door_origin.setPos(door_origin, 0, -0.025, 0)
        doorNP=door.copyTo(door_origin)
        assert(not doorNP.isEmpty())
        assert(not door_origin.isEmpty())
        # We do this instead of decals
        houseColor = HouseGlobals.atticWood
        color = Vec4(houseColor[0], houseColor[1], houseColor[2], 1)
        DNADoor.setupDoor(doorNP, 
                          door_origin, door_origin, 
                          dnaStore,
                          str(self.houseId), color)

        # Setting the wallpaper texture with a priority overrides
        # the door texture, if it's decalled.  So, we're going to
        # move it out from the decal, and float it in front of
        # the wall:
        doorFrame = doorNP.find("door_*_flat")
        #doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(color)
        assert(not doorFrame.isEmpty())

        # Get rid of any transitions and extra nodes
        self.interior.flattenMedium()

        # Prepare the list of window slots.
        self.windowSlots = []
        for name in WindowPlugNames:
            plugNodes = self.interior.findAllMatches(name)
            if plugNodes.isEmpty():
                self.windowSlots.append((None, None))
            else:
                # Create a new node to attach window views to, and
                # copy the plug's transform to it.
                viewBase = plugNodes[0].getParent().attachNewNode('view')
                viewBase.setTransform(plugNodes[0].getTransform())

                plug = plugNodes[0].getParent().attachNewNode('plug')
                plugNodes.reparentTo(plug)

                # The plug doesn't need a transform any more.
                plug.flattenLight()
                self.windowSlots.append((plug, viewBase))

        # Temporary hack to put the windows where they belong.
        self.windowSlots[2][1].setPosHpr(16.00, -12.00, 5.51, -90, 0, 0)
        self.windowSlots[4][1].setPosHpr(-12.00, 26.00, 5.51, 0, 0, 0)

        # pretty up the interior
        self.__colorWalls()

        # Apply the windows
        self.__setupWindows()
        
        messenger.send("houseInteriorLoaded-%d" % self.zoneId)
      

    def __colorWalls(self):
        # The order here matches the order of ST* parameters in
        # CatalogSurfaceItem.py.
        if not self.wallpaper:
            self.notify.info("No wallpaper in interior; clearing.")
            for str in WallNames + WainscotingNames:
                nodes = self.interior.findAllMatches('**/%s' % (str))
                for node in nodes:
                    node.setTextureOff(1)
            return

        numSurfaceTypes = CatalogSurfaceItem.NUM_ST_TYPES
        numRooms = min(len(self.wallpaper) / numSurfaceTypes, len(RoomNames))

        for room in range(numRooms):
            roomName = RoomNames[room]
            roomNode = self.interior.find(roomName)

            if not roomNode.isEmpty():
                for surface in range(numSurfaceTypes):
                    slot = room * numSurfaceTypes + surface
                    wallpaper = self.wallpaper[slot]
                    color = wallpaper.getColor()
                    texture = wallpaper.loadTexture()
                    for str in WallpaperPieceNames[surface]:
                        nodes = roomNode.findAllMatches('**/%s' % (str))
                        for node in nodes:
                            if str == "ceiling*":
                                # The ceiling doesn't get a texture applied.
                                # And it gets a slightly darker color
                                r,g,b,a = color
                                scale = 0.66
                                r *= scale
                                g *= scale
                                b *= scale
                                node.setColorScale(r,g,b,a)
                            else:
                                node.setColorScale(*color)
                                node.setTexture(texture, 1)

                        if (wallpaper.getSurfaceType() ==
                            CatalogSurfaceItem.STWallpaper):
                            color2 = wallpaper.getBorderColor()
                            texture2 = wallpaper.loadBorderTexture()
                            nodes = roomNode.findAllMatches(
                                '**/%s_border' % (str))
                            for node in nodes:
                                node.setColorScale(*color2)
                                node.setTexture(texture2, 1)

        # The arch gets a fixed color for now.
        nodes = self.interior.findAllMatches('**/arch*')
        for node in nodes:
            node.setColorScale(*(HouseGlobals.archWood + (1,)))
            
    def __setupWindows(self):
        # Remove the old window views, if any.
        for plug, viewBase in self.windowSlots:
            if plug:
                plug.show()
            if viewBase:
                viewBase.getChildren().detach()

        if not self.windows:
            self.notify.info("No windows in interior; returning.")
            return

        for item in self.windows:
            plug, viewBase = self.windowSlots[item.placement]
            if plug:
                plug.hide()

            if viewBase:
                model = item.loadModel()
                model.reparentTo(viewBase)
                if self.exteriorWindowsHidden:
                    # Go ahead and hide the exterior.
                    model.findAllMatches('**/outside').stash()

    def hideExteriorWindows(self):
        # Hide all the stuff hanging outside the windows.

        # Nowadays we actually stash it, so it doesn't become part of
        # the house's bounding volume.
        self.exteriorWindowsHidden = 1
        for item in self.windows:
            plug, viewBase = self.windowSlots[item.placement]
            if viewBase:
                viewBase.findAllMatches('**/outside').stash()

    def showExteriorWindows(self):
        self.exteriorWindowsHidden = 0
        for item in self.windows:
            plug, viewBase = self.windowSlots[item.placement]
            if viewBase:
                viewBase.findAllMatches('**/outside;+s').unstash()
        

    def setHouseId(self, index):
        assert(self.debugPrint("exitToon()"))
        self.houseId = index
        
    def setHouseIndex(self, index):
        self.houseIndex = index

    
    def setWallpaper(self, items):
        self.wallpaper = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization)
        if self.interior:
            self.__colorWalls()
    
    def setWindows(self, items):
        self.windows = CatalogItemList.CatalogItemList(items, store = CatalogItem.Customization | CatalogItem.WindowPlacement)
        if self.interior:
            self.__setupWindows()

    def testWallpaperCombo(self,
                           wallpaperType, wallpaperColorIndex,
                           borderIndex, borderColorIndex,
                           mouldingType, mouldingColorIndex,
                           flooringType, flooringColorIndex,
                           wainscotingType, wainscotingColorIndex):
        wallpaperItem = CatalogWallpaperItem.CatalogWallpaperItem(wallpaperType, wallpaperColorIndex, borderIndex, borderColorIndex )
        mouldingItem = CatalogMouldingItem.CatalogMouldingItem(mouldingType, mouldingColorIndex)
        flooringItem = CatalogFlooringItem.CatalogFlooringItem(flooringType, flooringColorIndex)
        wainscotingItem = CatalogWainscotingItem.CatalogWainscotingItem(wainscotingType, wainscotingColorIndex)
        self.wallpaper = CatalogItemList.CatalogItemList(
            [wallpaperItem, mouldingItem, flooringItem, wainscotingItem,
             wallpaperItem, mouldingItem, flooringItem, wainscotingItem],
            store = CatalogItem.Customization)
        if self.interior:
            self.__colorWalls()
        
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(str(message))




