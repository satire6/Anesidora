"""CountryClubRoomBase module: contains the CountryClubRoomBase class"""

from toontown.toonbase import ToontownGlobals

class CountryClubRoomBase:
    """ common functionality shared by DistributedCountryClubRoom/AI """
    def __init__(self):
        pass

    def setCountryClubId(self, countryClubId):
        """call this w/ countryClubId as soon as you have it"""
        self.countryClubId = countryClubId
        # countryClubIds are 'logical' zoneIds (we don't actually go to the countryClubId
        # zone)
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(countryClubId)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def getCogTrack(self):
        return self.cogTrack

    if __dev__:
        def getCountryClubEntityTypeReg(self):
            # return an EntityTypeRegistry with information about the
            # entity types that countryClubys use
            # Use the same types as factories
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
