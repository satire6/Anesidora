from toontown.estate import DistributedHouseAI
from toontown.catalog import CatalogWallpaperItem
from toontown.catalog import CatalogFlooringItem
from toontown.catalog import CatalogMouldingItem
from toontown.catalog import CatalogWainscotingItem
from toontown.catalog import CatalogItemList
import RepairAvatars
import DatabaseObject
import time

# Conversion 
mouldingBase = 1000
wainscotingBase = 1000
flooringBase = 1000
wallpaperBase = 1000

def convertItem(item, fCatalog):
    patternIndex = item.patternIndex
    colorIndex = item.colorIndex
    # This may be None
    newColorIndex = colorIndex
    if (patternIndex >= 101) and (patternIndex <= 111):
        # Flooring
        newPatternIndex = flooringBase + (patternIndex - 101) * 10
        if fCatalog:
            newColorIndex = None
        newItem = CatalogFlooringItem.CatalogFlooringItem(
            newPatternIndex, newColorIndex)
    elif (patternIndex >= 151) and (patternIndex <= 153):
        # Moulding
        if (patternIndex == 151) or (patternIndex == 152):
            newPatternIndex = 1000
        elif patternIndex == 153:
            newPatternIndex = 1010
        if newColorIndex == None:
            newColorIndex = 0
        newItem = CatalogMouldingItem.CatalogMouldingItem(
            newPatternIndex, newColorIndex)
    elif (patternIndex == 201) or (patternIndex == 202):
        # Wainscoting
        if newColorIndex == None:
            newColorIndex = 0
        newPatternIndex = wainscotingBase + (patternIndex - 201) * 10
        newItem = CatalogWainscotingItem.CatalogWainscotingItem(
            newPatternIndex, newColorIndex)
    else:
        # Wallpaper
        newBorderIndex = 0
        newBorderColorIndex = 0
        # Adjust pattern index
        if patternIndex == 1:
            newPatternIndex = 1200
        elif patternIndex == 2:
            newPatternIndex = 1300
        elif patternIndex == 3:
            newPatternIndex = 1600
        elif patternIndex == 4:
            newPatternIndex = 1100
        elif patternIndex == 5:
            newPatternIndex = 1000
        elif patternIndex == 1010:
            newPatternIndex = 1000
        elif patternIndex == 1102:
            newPatternIndex = 1100
        elif patternIndex == 1112:
            newPatternIndex = 1110
        elif patternIndex == 1122:
            newPatternIndex = 1120
        elif patternIndex == 1132:
            newPatternIndex = 1130
        elif patternIndex == 1142:
            newPatternIndex = 1140
        elif patternIndex == 1152:
            newPatternIndex = 1150
        else:
            newPatternIndex = patternIndex
        # Adjust colors
        if patternIndex <= 5:
            if colorIndex is not None:
                newColorIndex = 0
        # Adjust borders
        if patternIndex in [1010]:
            # Now use border pattern 1000
            newBorderIndex = 1000
        elif patternIndex in [4, 1102, 1132]:
            # Now use border pattern 1010
            newBorderIndex = 1010
        elif patternIndex in [1142, 1152]:
            # Now use border pattern 1020
            newBorderIndex = 1020
        elif patternIndex in [1122]:
            # Now use border pattern 1030
            newBorderIndex = 1030
        elif patternIndex in [1112]:
            # Now use border pattern 1040
            newBorderIndex = 1040
        elif patternIndex in [2000, 2100, 2110]:
            # Now use border pattern 1050
            newBorderIndex = 1050
        elif patternIndex in [2010, 2120]:
            # Now use border pattern 1060
            newBorderIndex = 1060
        elif patternIndex in [2020, 2130, 2140]:
            # Now use border pattern 1070
            newBorderIndex = 1070
        else:
            # No border
            newBorderIndex = 0
        # If catalog, change pattern number to group pattern index
        # and set colorIndex and borderIndex to None (non-customized)
        if fCatalog:
            newPatternIndex = newPatternIndex - (newPatternIndex % 100)
            newColorIndex = None
            newBorderIndex = None
        # Return brand shiny new catalog wallpaper item
        newItem = CatalogWallpaperItem.CatalogWallpaperItem(
            newPatternIndex, newColorIndex,
            newBorderIndex, newBorderColorIndex)
    # Copy over som essential fields
    newItem.deliveryDate = item.deliveryDate
    newItem.posHpr = item.posHpr
    return newItem

def convertWallpaperItems(itemList, fCatalog = 0):
    for i in range(len(itemList)):
        item = itemList[i]
        if isinstance(item, CatalogWallpaperItem.CatalogWallpaperItem):
            newItem = convertItem(item, fCatalog)
            # Replace Item
            itemList[i] = newItem

class AvatarWallpaperFixer(RepairAvatars.AvatarIterator):
    # When we come to this many non-avatars in a row, assume we have
    # reached the end of the database.
    endOfListCount = 2000

    def fieldsToGet(self, db):
        return ['setName', 'setMoney', 'setCatalog',
                'setMailboxContents', 'setDeliverySchedule']

    def processAvatar(self, av, db):
        self.printSometimes(av)
        #print "Processing Avatar: %d, %s" % (av.doId, av.name)
        convertWallpaperItems(av.monthlyCatalog, fCatalog = 1)
        convertWallpaperItems(av.weeklyCatalog, fCatalog = 1)
        convertWallpaperItems(av.backCatalog, fCatalog = 1)
        convertWallpaperItems(av.onOrder)
        convertWallpaperItems(av.mailboxContents)
        # Remove Duplicates for backCatalog list
        oldBackCatalog = av.backCatalog
        av.backCatalog = CatalogItemList.CatalogItemList()
        for item in oldBackCatalog:
            if item not in av.backCatalog:
                av.backCatalog.append(item)
        # Make sure stuff in current weekly catalog hasn't already been offered
        oldWeeklyCatalog = av.weeklyCatalog
        av.weeklyCatalog = CatalogItemList.CatalogItemList()
        for item in oldWeeklyCatalog:
            if ((item not in av.backCatalog) and
                (item not in av.weeklyCatalog)):
                av.weeklyCatalog.append(item)
        db2 = DatabaseObject.DatabaseObject(self.air, av.doId)
        db2.storeObject(av, ['setCatalog', 'setMailboxContents',
                             'setDeliverySchedule'])
        return
    def printSometimes(self, av):
        now = time.time()
        if now - self.lastPrintTime > self.printInterval:
            print "Avatar %d: %s" % (av.doId, av.name)
            self.lastPrintTime = now

    

class HouseWallpaperFixer(RepairAvatars.HouseIterator):
    # When we come to this many non-houses in a row, assume we have
    # reached the end of the database.
    endOfListCount = 2000

    def fieldsToGet(self, db):
        return ['setName', 'setHouseType', 'setAtticWallpaper',
                'setInteriorWallpaper', 'setDeletedItems']

    def processHouse(self, house, db):
        self.printSometimes(house)
        #print "Processing house: %d, %s" % (house.doId, house.name)
        convertWallpaperItems(house.atticWallpaper)
        convertWallpaperItems(house.interiorWallpaper)
        convertWallpaperItems(house.deletedItems)
        db2 = DatabaseObject.DatabaseObject(self.air, house.doId)
        db2.storeObject(house, ['setAtticWallpaper', 'setInteriorWallpaper',
                                'setDeletedItems'])

def convertWallpaper():
    f = AvatarWallpaperFixer(simbase.air)
    f.start()
    f2 = HouseWallpaperFixer(simbase.air)
    f2.start()

def convertWallpaperAvatarVals():
    avatarVals = open('avatar.vals')
    avatars = avatarVals.readlines()

    print "Fixing %s avatars" % (len(avatars))
    f = AvatarWallpaperFixer(simbase.air)
    f.objIdList = avatars
    f.start()

def convertWallpaperHouseVals():
    houseVals = open('house.vals')
    houses = houseVals.readlines()
    
    print "Fixing %s houses" % (len(houses))
    f2 = HouseWallpaperFixer(simbase.air)
    f2.objIdList = houses
    f2.start()

"""
import UtilityStart
from CatalogWallpaperConversion import *
convertWallpaper()
"""
