from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPetshopInteriorAI(DistributedObjectAI.DistributedObjectAI):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DistributedPetshopInteriorAI')

    def __init__(self, block, air, zoneId):
        # Right now, this doesn't do much.
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId


    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

        #self.interior = loader.loadModel('phase_4/models/modules/PetShopInterior')
        #render = self.getRender()
        #self.interior.instanceTo(render)

    def getZoneIdAndBlock(self):
        r=[self.zoneId, self.block]
        return r

    
        
