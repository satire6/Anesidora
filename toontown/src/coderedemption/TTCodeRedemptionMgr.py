from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify

class TTCodeRedemptionMgr(DistributedObject):
    neverDisable = 1

    notify = directNotify.newCategory('TTCodeRedemptionMgr')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.codeRedemptionMgr = self
        self._contextGen = SerialMaskedGen(0xffffffff)
        self._context2callback = {}

    def delete(self):
        if hasattr(base, 'codeRedemptionMgr'):
            if base.codeRedemptionMgr is self:
                del base.codeRedemptionMgr
        self._context2callback = None
        self._contextGen = None
        DistributedObject.delete(self)

    def redeemCode(self, code, callback):
        # callback takes result, awardMgrResult
        # if result is non-zero, there was an error (see TTCodeRedemptionConsts.RedeemErrors)
        # if result is TTCodeRedemptionConsts.AwardCouldntBeGiven, awardMgrResult holds the error code
        #   (see AwardManagerConsts.GiveAwardErrors)
        context = self._contextGen.next()
        self._context2callback[context] = callback
        self.notify.debug('redeemCode(%s, %s)' % (context, code))
        self.sendUpdate('redeemCode', [context, code])
        
    def redeemCodeResult(self, context, result, awardMgrResult):
        self.notify.debug('redeemCodeResult(%s, %s, %s)' % (context, result, awardMgrResult))
        callback = self._context2callback.pop(context)
        callback(result, awardMgrResult)
        
