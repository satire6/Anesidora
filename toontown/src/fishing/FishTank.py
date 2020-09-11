
import FishBase
import FishGlobals

class FishTank:

    def __init__(self):
        self.fishList = []

    def __len__(self):
        """
        For convenience
        """
        return len(self.fishList)

    def getFish(self):
        """
        Return the current fish list
        """
        return self.fishList
    
    def makeFromNetLists(self, genusList, speciesList, weightList):
        """
        Fill in the fish collection based on lists passed in like they are
        in the toon.dc file
        """
        self.fishList = []
        # Fill in the lists by running through the parallel lists of properties
        for genus, species, weight in zip(genusList, speciesList, weightList):
            self.fishList.append(FishBase.FishBase(genus, species, weight))        

    def getNetLists(self):
        """
        Return lists formated for toon.dc style setting and getting
        We store parallel lists of genus, species, and weight in the db
        """
        genusList = []
        speciesList = []
        weightList = []
        for fish in self.fishList:
            genusList.append(fish.getGenus())
            speciesList.append(fish.getSpecies())
            weightList.append(fish.getWeight())
        return [genusList, speciesList, weightList]

    def hasFish(self, genus, species):
        """
        Return 1 if we have the fish specified by this genus and species
        Return 0 if we do not
        """
        for fish in self.fishList:
            if (fish.getGenus() == genus) and (fish.getSpecies() == species):
                return 1
        return 0

    def hasBiggerFish(self, genus, species, weight):
        """
        Return 1 if we have the fish specified by this genus and species
        and the fish in this tank is heavier or equal to weight.
        Return 0 if we do not.
        """
        for fish in self.fishList:
            if ((fish.getGenus() == genus) and
                (fish.getSpecies() == species) and
                (fish.getWeight() >= weight)):
                return 1
        return 0
    
    def addFish(self, fish):
        """
        Add this fish to our collection
        """
        self.fishList.append(fish)
        return 1

    def removeFishAtIndex(self, index):
        """
        Remove the fish at index
        """
        if index >= len(self.fishList):
            return 0
        else:
            del self.fishList[i]
            return 1

    def generateRandomTank(self):
        import random
        numFish = random.randint(1,20)
        self.fishList = []
        for i in range(numFish):
            genus, species = FishGlobals.getRandomFish()
            weight = FishGlobals.getRandomWeight(genus, species)
            fish = FishBase.FishBase(genus,species,weight)
            self.addFish(fish)

    def getTotalValue(self):
        value = 0
        for fish in self.fishList:
            value += fish.getValue()
        return value
            
    def __str__(self):
        numFish = len(self.fishList)
        value = 0
        txt = ("Fish Tank (%s fish):" % (numFish))
        for fish in self.fishList:
            txt += ("\n" + str(fish))
            value += fish.getValue()
        txt += ("\nTotal value: %s" % (value))
        return txt
    
