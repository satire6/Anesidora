from direct.distributed.DistributedObject import DistributedObject

class DistributedInterestOpener(DistributedObject):
    """
    Delays opening of an interest set underneath this object until a
    specific set of doIds is present on the client.
    See also DistributedInterestOpenerAI.py
    """
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.generate(self)
        self.childInterest = None
        print 'DistributedInterestOpener.generate'

    def disable(self):
        self._removeInterest()
        del self.childInterest
        DistributedObject.disable(self)

    def setChildZones(self, childZones):
        self.childZones = childZones

    def setRequiredDoIds(self, requiredDoIds):
        self.requiredDoIds = requiredDoIds
        print 'DistributedInterestOpener.setRequiredDoIds'
        if self.childInterest is None:
            self.getObject(self.requiredDoIds, self._openInterest)
        else:
            # we've already got an interest open; change it
            self.getObject(self.requiredDoIds, self._alterInterest)
            
    def _openInterest(self):
        print 'DistributedInterestOpener._openInterest: %s' % self.getDoId()
        self.childInterest = self.cr.addInterest(
            self.getDoId(), self.childZones,
            self.uniqueName('interestOpener'))

    def _alterInterest(self):
        print 'DistributedInterestOpener._alterInterest'
        self.cr.alterInterest(self.childInterest, self.getDoId(),
                              self.childZones,
                              self.uniqueName('interestOpenerAlter'))

    def _removeInterest(self):
        print 'DistributedInterestOpener._removeInterest'
        if self.childInterest is not None:
            self.getRepository().removeInterest(self.childInterest)
        self.childInterest = None
