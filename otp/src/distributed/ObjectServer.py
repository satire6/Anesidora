
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject

class ObjectServer(DistributedObject.DistributedObject):
    """
    This is an object to represent the OTP Object Server itself.  You might
    not get a create for this object, but at some point you'll probably
    make contact with it to start an AI or some such.
    
    The server version of this object is created by Roger's code.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("ObjectServer")

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def setName(self, name):
        self.name=name
