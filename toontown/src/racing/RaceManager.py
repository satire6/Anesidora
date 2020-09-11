from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import random
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import HouseGlobals

class EstateManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManager")
    neverDisable = 1

    def __init__(self, cr):

        DistributedObject.DistributedObject.__init__(self, cr)

        self.availableZones = 0
        self.popupInfo = None

        import pdb; pdb.set_trace()

    def disable(self):
        self.notify.debug( "i'm disabling EstateManager rightnow.")
        #self.ignore("requestEstateZone")
        self.ignore("getLocalEstateZone")
        self.ignoreAll()
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        DistributedObject.DistributedObject.disable(self)

    def allocateMyEstateZone(self):
        # Get a zone for our own estate, i.e. we are going home right now
        self.getLocalEstateZone(base.localAvatar.getDoId())

    def getLocalEstateZone(self, avId):
        # Fullfill client request for estateZone
        name = ""
        if base.localAvatar.doId == avId:
            # going to our own home, provide AI with userName
            name = base.cr.userName
        self.sendUpdate("getEstateZone", [avId, name])
  
    def setEstateZone(self, ownerId, zoneId):
        # The AI is telling us the zone for this avatars estate
        self.notify.debug("setEstateZone(%s, %s)" % (ownerId, zoneId))

        # Send this to other hooks on the client side
        messenger.send("setLocalEstateZone", [ownerId, zoneId])

    def generate(self):
        self.notify.debug("BASE: generate")
        DistributedObject.DistributedObject.generate(self)

        # register with the cr
        base.cr.estateMgr = self
        
        # listen for requests
        #self.accept("requestEstateZone", self.allocateMyEstateZone)
        self.accept("getLocalEstateZone", self.getLocalEstateZone)
        #self.__createRandomNumGen()

        # listen for the generate event, which will be thrown after the
        # required fields are filled in
        self.announceGenerateName = self.uniqueName("generate")
        #self.accept(self.announceGenerateName, self.handleAnnounceGenerate)

    def setAvHouseId(self, avId, houseIds):
        self.notify.debug("setAvHouseId %d" % base.localAvatar.doId)
        for av in base.cr.avList:
            if av.id == avId:
                houseId = houseIds[av.position]
                ownerAv = base.cr.doId2do.get(avId)
                if ownerAv:
                    ownerAv.b_setHouseId(houseId)
                return
                
    def sendAvToPlayground(self, avId, retCode):
        self.notify.debug("sendAvToPlayground: %d" % avId)
        messenger.send("kickToPlayground", [retCode])

    def leaveEstate(self):
        if self.isDisabled():
            self.notify.warning("EstateManager disabled; unable to leave estate.")
            return
        
        self.sendUpdate("exitEstate")
        
    def removeFriend(self, ownerId, avId):
        self.notify.debug("removeFriend ownerId = %s, avId = %s" % (ownerId, avId))
        # The estate owner is  removing avId from his friends list.
        # Notify the AI, and kick the ex-friend out of the estate
        self.sendUpdate("removeFriend", [ownerId, avId])
