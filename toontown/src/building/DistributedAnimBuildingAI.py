from direct.directnotify import DirectNotifyGlobal
from toontown.building import DistributedBuildingAI
from toontown.building import DistributedAnimDoorAI
from toontown.building import DoorTypes

class DistributedAnimBuildingAI(DistributedBuildingAI.DistributedBuildingAI):
    """
    DistributedAnimBuildingAI class:  The server side representation of a
    single ANIMATED building.  This is the object that remember who 'owns' the
    associated building (either the bad guys or the toons).  The child
    of this object, the DistributedBuilding object, is the client side
    version and updates the display that client's display based on who
    'owns' the building.
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimBuildingAI')

    def __init__(self, air, blockNumber, zoneId, trophyMgr):
        """blockNumber: the landmark building number (from the name)"""
        DistributedBuildingAI.DistributedBuildingAI.__init__(self, air, blockNumber, zoneId, trophyMgr)
        
    def createExteriorDoor(self):
        """Return the DistributedDoor for the exterior, with correct door type set"""
        result = DistributedAnimDoorAI.DistributedAnimDoorAI(self.air, self.block,
                                                 DoorTypes.EXT_ANIM_STANDARD)
        return result
