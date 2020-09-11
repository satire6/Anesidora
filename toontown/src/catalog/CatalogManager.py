from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class CatalogManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogManager")

    # We should never disable this guy.
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    ### Interface methods ###

    ### DistributedObject methods ###

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        if base.cr.catalogManager != None:
            base.cr.catalogManager.delete()
        base.cr.catalogManager = self
        DistributedObject.DistributedObject.generate(self)

        # The first time a particular toon enters the world, start its
        # catalog system running.
        # We only want Toons to start the catalog manager running, however,
        # not gateway avatars, etc.
        if (hasattr(base.localAvatar, "catalogScheduleNextTime") and
            base.localAvatar.catalogScheduleNextTime == 0):
            self.d_startCatalog()

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        #self.notify.warning("Hey!  The CatalogManager was disabled!")
        base.cr.catalogManager = None
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        #self.notify.warning("Hey!  The CatalogManager was deleted!")
        base.cr.catalogManager = None
        DistributedObject.DistributedObject.delete(self)

    def d_startCatalog(self):
        self.sendUpdate("startCatalog", [])
        

        
