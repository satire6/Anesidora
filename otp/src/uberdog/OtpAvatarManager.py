"""
The Avatar Manager handles all the avatar (avatar groups) accross all districts.
"""

from cPickle import loads, dumps
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal

notify = DirectNotifyGlobal.directNotify.newCategory('AvatarManager')


class OtpAvatarManager(DistributedObject.DistributedObject):

    notify = notify

    OnlineEvent = 'GlobalAvatarManagerOnline'

    def __init__(self, cr):
        assert self.notify.debugCall()
        DistributedObject.DistributedObject.__init__(self, cr)
        self.avatars={}
        assert not hasattr(cr, "avatarManager") or cr.avatarManager is None

    def delete(self):
        assert self.notify.debugCall()
        self.ignoreAll()
        self.cr.avatarManager = None
        DistributedObject.DistributedObject.delete(self)
    
    def online(self):
        assert self.notify.debugCall()
        messenger.send(OtpAvatarManager.OnlineEvent)

    #------------------------------------------------------------------------

    def sendRequestAvatarList(self):
        assert self.notify.debugCall()
        self.sendUpdate("requestAvatarList", [0,])

    def rejectAvatarList(self, result):
        assert self.notify.debugCall()
        messenger.send("avatarListFailed", [result])

    def avatarListResponse(self, pickleData):
        assert self.notify.debugCall()
        avatars=loads(pickleData)
        messenger.send("avatarList", [avatars])

    #------------------------------------------------------------------------

    def rejectCreateAvatar(self, result):
        assert self.notify.debugCall()
        messenger.send("createdNewAvatarFailed", [result])

    def createAvatarResponse(self, avatarId, subId, access, founder):
        assert self.notify.debugCall()
        self.notify.info("new avatarId: %s subId: %s access: %s founder: %s" % (avatarId, subId, access, founder))
        messenger.send("createdNewAvatar", [avatarId, subId])

    #------------------------------------------------------------------------

    def sendRequestRemoveAvatar(self, avatarId, subId, confirmPassword):
        assert self.notify.debugCall()
        self.sendUpdate("requestRemoveAvatar", [0, avatarId, subId, confirmPassword])

    def rejectRemoveAvatar(self, reasonId):
        assert self.notify.debugCall()
        messenger.send("rejectRemoveAvatar", [reasonId])

    def removeAvatarResponse(self, avatarId, subId):
        assert self.notify.debugCall()
        messenger.send("removeAvatarResponse", [avatarId, subId])

    #------------------------------------------------------------------------

    def sendRequestShareAvatar(self, avatarId, subId, shared):
        assert self.notify.debugCall()
        self.sendUpdate("requestShareAvatar", [0, avatarId, subId, shared])

    def rejectShareAvatar(self, reasonId):
        assert self.notify.debugCall()
        messenger.send("rejectShareAvatar", [reasonId])

    def shareAvatarResponse(self, avatarId, subId, shared):
        assert self.notify.debugCall()
        messenger.send("shareAvatarResponse", [avatarId, subId, shared])

    #------------------------------------------------------------------------

    def sendRequestAvatarSlot(self, subId, slot):
        assert self.notify.debugCall()
        self.sendUpdate("requestAvatarSlot", [0, subId, slot])

    def rejectAvatarSlot(self, reasonId, subId, slot):
        assert self.notify.debugCall()
        messenger.send("rejectAvatarSlot", [reasonId, subId, slot])

    def avatarSlotResponse(self, subId, slot):
        assert self.notify.debugCall()
        messenger.send("avatarSlotResponse", [subId, slot])

    #------------------------------------------------------------------------

    def sendRequestPlayAvatar(self, avatarId, subId):
        assert self.notify.debugCall()
        self.sendUpdate("requestPlayAvatar", [0, avatarId, subId])

    def rejectPlayAvatar(self, reasonId, avatarId):
        assert self.notify.debugCall()
        messenger.send("rejectPlayAvatar", [reasonId, avatarId])

    def playAvatarResponse(self, avatarId, subId, access, founder):
        assert self.notify.debugCall()
        messenger.send("playAvatarResponse", [avatarId, subId, access, founder])


