from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.uberdog import DataStoreGlobals

if __debug__:
    from direct.directnotify.DirectNotifyGlobal import directNotify
    notify = directNotify.newCategory('DistributedDataStoreManager')

class DistributedDataStoreManager(DistributedObjectGlobal):
    def __init__(self):
        assert False, 'DistributedDataStoreManager should not be used.'
