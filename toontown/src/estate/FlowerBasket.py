import GardenGlobals
from direct.directnotify import DirectNotifyGlobal
import FlowerBase

class FlowerBasket:
    """
    #RAU adapted from fishing/FishTank.py
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("FlowerBasket")

    def __init__(self):
        self.flowerList = []

    def __len__(self):
        """
        For convenience
        """
        return len(self.flowerList)

    def getFlower(self):
        """
        Return the current flower list
        """
        return self.flowerList
    
    def makeFromNetLists(self, speciesList, varietyList):
        """
        Fill in the flower collection based on lists passed in like they are
        in the toon.dc file
        """
        self.flowerList = []
        # Fill in the lists by running through the parallel lists of properties
        for species, variety in zip(speciesList, varietyList):
            self.flowerList.append(FlowerBase.FlowerBase(species, variety))        

    def getNetLists(self):
        """
        Return lists formated for toon.dc style setting and getting
        We store parallel lists of species, and variety in the db
        """
        speciesList = []
        varietyList = []
        for flower in self.flowerList:
            speciesList.append(flower.getSpecies())
            varietyList.append(flower.getVariety())
        return [ speciesList, varietyList]

    def hasFlower(self, species, variety):
        """
        Return 1 if we have the flower specified by this species and variety
        Return 0 if we do not
        """
        for flower in self.flowerList:
            if (flower.getSpecies() == species) and (flower.getVariety() == variety):
                return 1
        return 0

    def addFlower(self, species, variety):
        """
        Add this fish to our collection
        """
        self.flowerList.append(FlowerBase.FlowerBase(species,variety))
        return 1

    def removeFishAtIndex(self, index):
        """
        Remove the fish at index
        """
        if index >= len(self.flowerList):
            return 0
        else:
            del self.flowerList[i]
            return 1

    def generateRandomBasket(self):
        import random
        numFish = random.randint(1,20)
        self.flowerList = []
        for i in range(numFish):
            species , variety= GardenGlobals.getRandomFlower()
            self.addFlower(species,variety)

    def getTotalValue(self):
        value = 0
        for flower in self.flowerList:
            value += flower.getValue()
        return value;
            
    def __str__(self):
        numFlower = len(self.flowerList)
        value = 0
        txt = ("Flower Basket (%s flower):" % (numFlower))
        for flower in self.flowerList:
            txt += ("\n" + str(flower))
        value = self.getTotalValue()
        txt += ("\nTotal value: %s" % (value))
        return txt
    
