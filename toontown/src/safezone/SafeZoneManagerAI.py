from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SafeZoneManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("SafeZoneManagerAI")

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        # Number of seconds between spontaneous heals
        self.healFrequency = 30 # seconds

    def enterSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        # Make sure the avatar exists.
        if self.air.doId2do.has_key(avId):
            # Find the avatar
            av = self.air.doId2do[avId]
            # Start healing them
            av.startToonUp(self.healFrequency)

        else:
            self.notify.warning(
                "Toon " +
                str(avId) +
                " isn't here, but just entered the safe zone. " +
                "I will ignore this."
                )
        # Send the "avatar escaped to safezone" message, just in case
        # there are any battles going on that involve this avatar.
        event = "inSafezone-%s" % (avId)
        messenger.send(event)

    def exitSafeZone(self):
        avId = self.air.getAvatarIdFromSender()
        # Make sure the avatar exists.
        if self.air.doId2do.has_key(avId):
            # Find the avatar
            av = self.air.doId2do[avId]
            # Start healing them
            av.stopToonUp()
            
