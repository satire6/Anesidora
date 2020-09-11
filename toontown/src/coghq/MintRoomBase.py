"""MintRoomBase module: contains the MintRoomBase class"""

from toontown.toonbase import ToontownGlobals

class MintRoomBase:
    """ common functionality shared by DistributedMintRoom/AI """
    def __init__(self):
        pass

    def setMintId(self, mintId):
        """call this w/ mintId as soon as you have it"""
        self.mintId = mintId
        # mintIds are 'logical' zoneIds (we don't actually go to the mintId
        # zone)
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(mintId)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def getCogTrack(self):
        return self.cogTrack

    if __dev__:
        def getMintEntityTypeReg(self):
            # return an EntityTypeRegistry with information about the
            # entity types that mints use
            # Use the same types as factories
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
