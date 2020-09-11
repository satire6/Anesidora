"""StageRoomBase module: contains the StageRoomBase class"""

from toontown.toonbase import ToontownGlobals

class StageRoomBase:
    """ common functionality shared by DistributedStageRoom/AI """
    def __init__(self):
        pass

    def setStageId(self, stageId):
        """call this w/ stageId as soon as you have it"""
        self.stageId = stageId
        # stageIds are 'logical' zoneIds (we don't actually go to the stageId
        # zone)
        self.cogTrack = ToontownGlobals.cogHQZoneId2dept(stageId)

    def setRoomId(self, roomId):
        self.roomId = roomId

    def getCogTrack(self):
        return self.cogTrack

    if __dev__:
        def getStageEntityTypeReg(self):
            # return an EntityTypeRegistry with information about the
            # entity types that stages use
            # Use the same types as factories
            import FactoryEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(FactoryEntityTypes)
            return typeReg
