import CatalogGardenItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from toontown.estate import GardenGlobals

class CatalogToonStatueItem(CatalogGardenItem.CatalogGardenItem):
    """
    Represents a Toon Statue Garden Item on the Delivery List.
    CatalogToonStatueItem is derived from CatalogGardenItem for the intention of 
    adding the functionality of customization. The user can cycle through a list 
    of toon statues and choose the statue pose he/she likes.
    
    NOTE: While creating a CatalogToonStatueItem in CatalogGenerator.py ensure the following:
    1) 1st parameter is the poseIndex you want the list to start with
    2) Also endPoseIndex parameters while creating CatalogToonStatueItem
       All poses between the 1st parameter (gardenIndex) and endPoseIndex will be included
       in the list of poses to choose from.
    3) 1st parameter (gardenIndex) should be <= endPoseIndex
    4) While adding more toon statue poses, make sure the specialsIndex of the poses 
       are in numeric succession     
    """

    pictureToonStatue = None
    
    def makeNewItem(self, itemIndex = 105, count  = 1, tagCode = 1, endPoseIndex = 108):
        # The itemIndex has to be less than or equal to the endPoseIndex
        assert (itemIndex <= endPoseIndex) 
        self.startPoseIndex = itemIndex
        self.endPoseIndex = endPoseIndex
        CatalogGardenItem.CatalogGardenItem.makeNewItem(self, itemIndex, count, tagCode)
        
    def needsCustomize(self):
        # Returns true if endPoseIndex - startPoseIndex is more 0, this means there are more than 1 choice
        return ((self.endPoseIndex - self.startPoseIndex) > 0)

    def getPicture(self, avatar):
        # Handle the ToonStatues separately because we have to load a toon statue of the
        # local avatar with a predefined pose instead of a predefined static model
    
        # Don't import this at the top of the file, since this code must run on the AI.
        from toontown.estate import DistributedToonStatuary
        toonStatuary = DistributedToonStatuary.DistributedToonStatuary(None)
        toonStatuary.setupStoneToon(base.localAvatar.style)
        toonStatuary.poseToonFromSpecialsIndex(self.gardenIndex)

        # Toon with the pedestal looks too small in the catalog, so I'm removing the pedestal.
        # Bring the toon up to 0 height, because we do a toon.setZ(70) in DistributedToonStatuary.py
        toonStatuary.toon.setZ(0)
        model, ival = self.makeFrameModel(toonStatuary.toon, 1)

        self.pictureToonStatue = toonStatuary
        
        assert (not self.hasPicture)
        self.hasPicture=True
        return (model, ival)
    
    def cleanupPicture(self):        
        assert self.pictureToonStatue
        self.pictureToonStatue.deleteToon()
        self.pictureToonStatue = None
        CatalogGardenItem.CatalogGardenItem.cleanupPicture(self)        
    
    def decodeDatagram(self, di, versionNumber, store):
        CatalogGardenItem.CatalogGardenItem.decodeDatagram(self, di, versionNumber, store)
        self.startPoseIndex = di.getUint8()
        self.endPoseIndex = di.getUint8()

    def encodeDatagram(self, dg, store):
        CatalogGardenItem.CatalogGardenItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.startPoseIndex)
        dg.addUint8(self.endPoseIndex)
        
    def compareTo(self, other):
        if (self.gardenIndex >= self.startPoseIndex) and (self.gardenIndex <= self.endPoseIndex):
            return 0
        return 1
        
    def getAllToonStatues(self):
        # This function returns a list of all possible toon statues
        self.statueList = []
        for index in range(self.startPoseIndex, self.endPoseIndex + 1):
            self.statueList.append(CatalogToonStatueItem(index, 1, endPoseIndex = index))
        return self.statueList
    
    def deleteAllToonStatues(self):
        # This function deletes all the toon statues in the list
        while len(self.statueList):
            item = self.statueList[0]
            if item.pictureToonStatue:
                item.pictureToonStatue.deleteToon()
            self.statueList.remove(item)