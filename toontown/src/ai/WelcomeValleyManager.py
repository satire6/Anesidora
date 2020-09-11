from pandac.PandaModules import *

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from direct.showbase import PythonUtil
        
class WelcomeValleyManager(DistributedObject.DistributedObject):
    """WelcomeValleyManager

    """
    notify = DirectNotifyGlobal.directNotify.newCategory("WelcomeValleyManager")

    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    ### DistributedObject methods ###

    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        if base.cr.welcomeValleyManager != None:
            base.cr.welcomeValleyManager.delete()
        base.cr.welcomeValleyManager = self
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        """disable(self)
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """delete(self)
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        self.ignore(ToontownGlobals.SynchronizeHotkey)
        base.cr.welcomeValleyManager = None
        DistributedObject.DistributedObject.delete(self)

# now done locally on the AI
##     def d_clientSetZone(self, zoneId):
##         # Tell the AI which zone we're going to.  We don't bother to
##         # do this for every little zone on the street, just major zone
##         # changes (e.g. through the quiet zone).
##         self.sendUpdate("clientSetZone", [zoneId])

    def requestZoneId(self, origZoneId, callback):
        context = self.getCallbackContext(callback)
        self.sendUpdate("requestZoneIdMessage", [origZoneId, context])


    def requestZoneIdResponse(self, zoneId, context):
        self.doCallbackContext(context, [zoneId])
