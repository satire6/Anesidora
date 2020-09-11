"""
Account module: stub to fulfill the Account toon.dc Distributed Class
This is a class Roger needs for the server to be able to display these values
appropriately in the db web interface.
"""

from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectUD

class AccountUD(DistributedObjectUD.DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccountUD')

    def __init__(self, air):
        assert air
        DistributedObjectUD.DistributedObjectUD.__init__(self, air)

    def setPirate(self, slot, avatarId):
        assert self.notify.debugCall()
        self.pirateAvatars[slot] = avatarId
        assert self.air
        self.sendUpdate('pirateAvatars', self.pirateAvatars)

    def getPirate(self, slot):
        assert self.notify.debugCall()
        return self.pirateAvatars[slot]

    def getSlotLimit(self):
        assert self.notify.debugCall()
        return 6

    def may(self, perm):
        """
        Ask whether the account has permission to <string>.
        """
        assert self.notify.debugCall()
        return 1
