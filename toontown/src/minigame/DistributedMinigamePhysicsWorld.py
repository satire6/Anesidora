from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import MinigamePhysicsWorldBase

class DistributedMinigamePhysicsWorld(DistributedObject.DistributedObject, MinigamePhysicsWorldBase.MinigamePhysicsWorldBase):
    """Base class on the client for minigame physics.
    
    Should not have any hardcoded info which is specific to a given game.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedMinigamePhysicsWorld")    

    def __init__(self,cr):
        """Create the MinigamePhysicsWorldBase."""
        DistributedObject.DistributedObject.__init__(self, cr)
        MinigamePhysicsWorldBase.MinigamePhysicsWorldBase.__init__(self, canRender = 1)
    def delete(self):
        """Delete ourself from the world."""
        MinigamePhysicsWorldBase.MinigamePhysicsWorldBase.delete(self)
        DistributedObject.DistributedObject.delete(self)
