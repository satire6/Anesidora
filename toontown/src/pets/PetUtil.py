"""
Set of miscellaneous helper functions for Pets
"""

from toontown.pets import PetDNA, PetTraits, PetConstants
from toontown.pets import PetNameGenerator
from direct.showbase import PythonUtil
import random

def getPetInfoFromSeed(seed, safezoneId):
    S = random.getstate()

    random.seed(seed)

    dnaArray = PetDNA.getRandomPetDNA(safezoneId)
    gender = PetDNA.getGender(dnaArray)
    nameString = PetNameGenerator.PetNameGenerator().randomName(gender=gender, seed=seed+safezoneId)
    traitSeed = PythonUtil.randUint31()

    random.setstate(S)
    return (nameString, dnaArray, traitSeed)

def getPetCostFromSeed(seed, safezoneId):
    name, dna, traitSeed = getPetInfoFromSeed(seed, safezoneId)
    traits = PetTraits.PetTraits(traitSeed, safezoneId)
    traitValue = traits.getOverallValue()

    #hack val so we have more '200' jelly bean pets
    traitValue -= 0.3
    traitValue = max(0, traitValue) #clamp to 0
    """ TRAITFIX -- replace traitValue calculation with:
    traitValue = (traitValue - .3) / .7
    traitValue = PythonUtil.clampScalar(traitValue, 0., 1.)
    """

    # DNA rarity is in the range 0(rare) to 1(common)
    rarity = PetDNA.getRarity(dna)

    # traitValue is in the range 0(worthless) to 1(valuable)
    rarity *= (1.0 - traitValue)

    #this will give us a nice curve between .999(rare) and 0(common)
    rarity = pow(0.001, rarity) - 0.001

    minCost, maxCost = PetConstants.ZoneToCostRange[safezoneId]

    # scale this between min and max cost
    cost = (rarity * (maxCost-minCost)) + minCost

    cost = int(cost)
    
    return (cost)

