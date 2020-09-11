"""PetBase.py"""

from toontown.pets.PetConstants import AnimMoods
from toontown.pets import PetMood
import string

class PetBase:
    """common code shared by client and AI"""
    # I am wont to add functions to the pet object to reduce redundant typing.
    # This is a util func to make names for those getter/setter funcs.
    def getSetterName(self, valueName, prefix='set'):
        return '%s%s%s' % (prefix, string.upper(valueName[0]), valueName[1:])

    # these functions are here so that we are sure to keep all external
    # indications of mood consistent; we don't want a pet bouncing around
    # excitedly while displaying a sad emoticon. By putting these functions
    # in PetBase, the same logic is made available to both the AI and the
    # client.
    def getAnimMood(self):
        if self.mood.getDominantMood() in PetMood.PetMood.ExcitedMoods:
            return AnimMoods.EXCITED
        elif self.mood.getDominantMood() in PetMood.PetMood.UnhappyMoods:
            return AnimMoods.SAD
        else:
            return AnimMoods.NEUTRAL

    def isExcited(self):
        return self.getAnimMood() == AnimMoods.EXCITED
    def isSad(self):
        return self.getAnimMood() == AnimMoods.SAD
