
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedBankMgr(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBankMgr')

    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        if base.cr.bankManager != None:
            base.cr.bankManager.delete()
        base.cr.bankManager = self
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        base.cr.bankManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        base.cr.bankManager = None
        DistributedObject.DistributedObject.delete(self)

    def d_transferMoney(self, amount):
        """
        Ask the AI to transfer money. Positive amount is a deposit to bank.
        """
        self.sendUpdate('transferMoney', [amount])
