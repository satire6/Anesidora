
import sys

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class ObjectServerUD(DistributedObjectUD):
    """
    This is an object to represent the OTP Object Server itself.  You might
    not get a create for this object, but at some point you'll probably
    make contact with it to start an UD or some such.
    
    The server version of this object is created by Roger's code.
    """
    notify = directNotify.newCategory("ObjectServerUD")

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
    
    def delete(self):
        self.air.removeDOFromTables(self)
        DistributedObjectUD.delete(self)

    def setName(self, name):
        self.name=name

    def setDcHash(self, dcHash):
        self.dcHash=dcHash
        if dcHash != self.air.hashVal:
            print "\nBad DC Version compare -- hash value mismatch (district %s, otp_server %s)"%(
                (self.air.hashVal, dcHash))
            sys.exit()
        else:
            print "DC hash matches."
