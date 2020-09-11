from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGagshopInteriorAI(DistributedObjectAI.DistributedObjectAI):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DistributedGagshopInteriorAI')

    def __init__(self, block, air, zoneId):
        # Right now, this doesn't do much.
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId
        
    def getZoneIdAndBlock(self):
        r=[self.zoneId, self.block]
        return r

    
        
