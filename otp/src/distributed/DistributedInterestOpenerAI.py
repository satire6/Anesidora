from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.PythonUtil import makeTuple

class DistributedInterestOpenerAI(DistributedObjectAI):
    """
    Use this class to cause the client to delay opening of an interest
    set (underneath this object) until a specific set of doIds is present
    on the client.
    """
    def __init__(self, air, requiredDoIds, zones=None):
        DistributedObjectAI.__init__(self, air)
        if zones is None:
            zones = (2,)
        else:
            zones = makeTuple(zones)
        self.zones = zones
        self.requiredDoIds = requiredDoIds

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        print 'DistributedInterestOpenerAI.announceGenerate: %s' % self.doId

    def setRequiredDoIds(self, requiredDoIds):
        # call this to change the list of required doIds
        if requiredDoIds != self.requiredDoIds:
            self.requiredDoIds = requiredDoIds
            self.sendUpdate('setRequiredDoIds', [self.requiredDoIds])

    def getChildZones(self):
        return self.zones

    def getRequiredDoIds(self):
        return self.requiredDoIds
