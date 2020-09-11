from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DeleteManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DeleteManagerAI")

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def setInventory(self, newInventoryString):
        avId = self.air.getAvatarIdFromSender()
        # Make sure the avatar exists.
        if self.air.doId2do.has_key(avId):
            # Find the avatar
            av = self.air.doId2do[avId]
            # Create a new inventory list
            newInv = av.inventory.makeFromNetString(newInventoryString)
            # Delete the items
            av.inventory.setToMin(newInv)
            # Tell the state server
            av.d_setInventory(av.inventory.makeNetString())
        else:
            self.air.writeServerEvent('suspicious', avId, 'DeleteManagerAI.setInventory unknown avatar')
            self.notify.warning(
                "Avatar: " + str(avId) +
                " tried to setInventory, but is not in the district.")
            
        
