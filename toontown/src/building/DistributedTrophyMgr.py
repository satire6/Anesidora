
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedTrophyMgr(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTrophyMgr')

    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.trophyManager != None:
            base.cr.trophyManager.delete()
        base.cr.trophyManager = self
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        """disable(self)
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        # Warning! disable() is NOT called for TrophyManager!  Duh!
        base.cr.trophyManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """delete(self)
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        base.cr.trophyManager = None
        DistributedObject.DistributedObject.delete(self)

    def d_requestTrophyScore(self):
        """
        Call this message to request the avatar's current trophy
        score.  This will eventually cause the trophyScoreUpdate
        message (above) to be sent.
        """
        self.sendUpdate('requestTrophyScore', [])
