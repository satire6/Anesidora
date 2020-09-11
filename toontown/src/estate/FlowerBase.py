
# NOTE: This file is imported on the client and AI, so do not import anything
# that the AI will have a problem with (like opening a window)
import GardenGlobals
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal

class FlowerBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('FlowerBase')

    def __init__(self, species, variety):
        self.species = species
        self.variety = variety
        #temp hack code to fix rose
        if self.species not in GardenGlobals.PlantAttributes.keys():
            print "remove me when everyone is updated"
            self.species = 56
            species = 56
        assert self.species in GardenGlobals.PlantAttributes.keys()
        assert self.variety < len(GardenGlobals.PlantAttributes[species]['varieties'])
 
    def getSpecies(self):
        return self.species

    def setSpecies(self, species):
        self.species = species
        assert self.species in GardenGlobals.PlantAttributes.keys()        


    def getVariety(self):
        return self.variety

    def setVariety(self,variety):
        self.variety = variety
        assert self.variety < len(GardenGlobals.PlantAttributes[self.species]['varieties'])                

    def getVitals(self):
        # For convenience, to save from having to call 2 separate functions
        return self.species, self.variety

    def getValue(self):
        """
        Returns the monetary value of this flower
        """
        return GardenGlobals.PlantAttributes[self.species]['varieties'][self.variety][2]
    

    def getSpeciesName(self):
        return TTLocalizer.FlowerSpeciesNames[self.species]

    def getVarietyName(self):
        return self.getFullName() # TTLocalizer.FishSpeciesNames[self.genus][self.species]


    def getFullName(self):
        return GardenGlobals.getFlowerVarietyName(self.species, self.variety)

    def getFullNameWithRecipe(self):
        name = GardenGlobals.getFlowerVarietyName(self.species, self.variety)
        recipeKey = GardenGlobals.PlantAttributes[self.species]['varieties'][self.variety][0]
        name += ' (%s)' % GardenGlobals.Recipes[recipeKey]['beans']
        return name
        
    def __str__(self):
        return ("%s, value: %s" %
                (self.getFullName(),  self.getValue()))
