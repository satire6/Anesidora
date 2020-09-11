"""FactorySpecs.py: contains table of factory specs"""

from toontown.toonbase import ToontownGlobals
import SellbotLegFactorySpec
import SellbotLegFactoryCogs
import LawbotLegFactorySpec
import LawbotLegFactoryCogs

def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]

def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]

# source data for factory specifications
FactorySpecModules = {
    ToontownGlobals.SellbotFactoryInt: SellbotLegFactorySpec,
    ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec, #remove me JML
    }

## until cogs are entities...
CogSpecModules = {
    ToontownGlobals.SellbotFactoryInt: SellbotLegFactoryCogs,
    ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs, #remove me JML
    }

if __dev__:
    import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec

    import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
