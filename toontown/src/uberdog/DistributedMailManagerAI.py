from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedMailManagerAI(DistributedObjectAI):
    """AI side class for the mail manager."""
    
    notify = directNotify.newCategory("DistributedMailManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)    
        self.accept("avatarEntered", self.__handleAvatarEntered)

    def sendSimpleMail(self, senderId, recipientId, simpleText):
        """Testing to send a simple text message to another."""
        DistributedMailManagerAI.notify.debug("sendSimpleMail( senderId=%d, recipientId=%d, simpleText='%s' )" %(senderId, recipientId, simpleText) )
        self.sendUpdate('sendSimpleMail', [senderId, recipientId, simpleText])

    def __handleAvatarEntered(self, avatar):
        """A toon just logged in, check his mail."""
        DistributedMailManagerAI.notify.debug("__handleAvatarEntered( avatar=%s )" %avatar )
        #import pdb; pdb.set_trace()
        #self.sendUpdate('avatarLoggedIn', [avatar.doId])
    
    def setNumMailItems(self, avatarId, numMailItems):
        DistributedMailManagerAI.notify.debug("setNumMailItems( avatarId=%d, numMailItems=%d )" %(avatarId, numMailItems) )
        toon = simbase.air.doId2do.get(avatarId)
        if toon:
            toon.setNumMailItems(numMailItems)
        
