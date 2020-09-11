import GardenGlobals
from direct.directnotify import DirectNotifyGlobal
import FlowerBase

class FlowerCollection:
    """
    #RAU adapted from fishing/FishCollection.py
    #translating from fishing to flowers genus->species,  species->variety
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("FlowerCollection")
    
    def __init__(self):
        self.flowerlist = []

    def __len__(self):
        """
        For convenience
        """
        return len(self.flowerlist)

    def getFlower(self):
        """
        Return the current flower list
        """
        return self.flowerlist
    
    def makeFromNetLists(self, speciesList, varietyList):
        """
        Fill in the flower collection based on lists passed in like they are
        in the toon.dc file
        """
        self.flowerlist = []
        # Fill in the lists by running through the parallel lists of properties
        for species, variety in zip(speciesList, varietyList):
            self.flowerlist.append( FlowerBase.FlowerBase(species, variety) )        

    def getNetLists(self):
        """
        Return lists formated for toon.dc style setting and getting
        We store parallel lists of species, and variety in the db
        """
        speciesList = []
        varietyList = []
        for flower in self.flowerlist:
            speciesList.append(flower.getSpecies())
            varietyList.append(flower.getVariety())
        return [speciesList, varietyList]

    def hasFlower(self, species, variety):
        """
        Return 1 if we have the flower specified by this species and variety
        Return 0 if we do not
        """
        for flower in self.flowerlist:
            if (flower.getSpecies() == species) and (flower.getVariety() == variety):
                return 1
        return 0

    def hasSpecies(self, species):
        """
        Return 1 if we have a flower specified by this species
        Return 0 if we do not
        """
        for flower in self.flowerlist:
            if (flower.getSpecies() == species):
                return 1
        return 0

    def getInitialVariety(self, species):
        """
        Used by GardenPage, when we switch to a different species, we may not have
        the variety 0, figure out the lowest one that we have
        """
        retVal = 100000

        for flower in self.flowerlist:
            if flower.getSpecies() == species:
                if flower.getVariety() < retVal:
                    retVal = flower.getVariety()

        if retVal == 100000:
            #let's not give a warning, since this can get called when he has no species 
            #self.notify.warning('did not find an initial variety for species=%d' % species)
            retVal = 0

        return retVal;
        
        
        

    def __collect(self, newFlower, updateCollection):
        """
        This funtion exists to share code between collectFlower and getCollectResult.
        See their documentation for more details
        """
        # Look for this flower type in our list
        for flower in self.flowerlist:
            if ((flower.getVariety() == newFlower.getVariety()) and
                (flower.getSpecies() == newFlower.getSpecies())):
                    # Nope, nothing to update here
                    return GardenGlobals.COLLECT_NO_UPDATE
        if updateCollection:
            self.flowerlist.append(newFlower)
        return GardenGlobals.COLLECT_NEW_ENTRY

    def collectFlower(self, newFlower):
        """
        Record this catch in our collection. Has several possible return values:
        If this flower was not previously in our collection, return COLLECT_NEW_ENTRY
        Otherwise, we already had this flower, nothing to update, return COLLECT_NO_UPDATE
        """
        return self.__collect(newFlower, updateCollection=1)

#    def getCollectResult(self, newFlower):
#        """
#        NOTE: This DOES NOT record the flower in our collection.
#        If this flower was not previously in our collection, return COLLECT_NEW_ENTRY
#        If this flower was already found, and we set a new weight record, return COLLECT_NEW_RECORD
#        Otherwise, we already had this flower, nothing to update, return COLLECT_NO_UPDATE
#        """
#        return self.__collect(newFlower, updateCollection=0)

    def __str__(self):
        numFlower = len(self.flowerlist)
        txt = ("Flower Collection (%s flowers):" % (numFlower))
        for flower in self.flowerlist:
            txt += ("\n" + str(flower))
        return txt
