"""FactoryBase module: contains the FactoryBase class"""

import FactorySpecs
from otp.level import LevelSpec
from toontown.toonbase import ToontownGlobals

class LawOfficeBase:
    """ common functionality shared by DistributedLawOffice/AI """
    def __init__(self):
        pass

    def setLawOfficeId(self, factoryId):
        """call this w/ factoryId as soon as you have it"""
        self.lawOfficeId = factoryId
        self.factoryType = ToontownGlobals.factoryId2factoryType[factoryId]
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(factoryId)

    def getCogTrack(self):
        return self.cogTrack

    def getFactoryType(self):
        return self.factoryType

    if __dev__:
        def getEntityTypeReg(self):
            # return an EntityTypeRegistry with information about the
            # entity types that factories use
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
