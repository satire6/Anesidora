
"""
The Toontown Avatar Manager UD handles all the avatar accross all
districts.
"""

from cPickle import loads, dumps

from otp.uberdog.UberDogUtil import ManagedAsyncRequest
from otp.distributed import OtpDoGlobals
from otp.uberdog.OtpAvatarManagerUD import OtpAvatarManagerUD
from otp.uberdog.RejectCode import RejectCode

if __debug__:
    from direct.directnotify.DirectNotifyGlobal import directNotify
    notify = directNotify.newCategory('AvatarManagerUD')

#-----------------------------------------------------------------------------

class AsyncRequestAvatarList(ManagedAsyncRequest):
    if __debug__:
        notify = notify

    def __init__(self, distObj, accountId):
        assert self.notify.debugCall()
        self.rejectString="rejectAvatarList"
        ManagedAsyncRequest.__init__(self, distObj, distObj.air, accountId)
        self.gotAvatars=0
        self.accountId=accountId
        self.askForObjectField("AccountUD", "ACCOUNT_AV_SET", self.accountId)

    def getAvatarData(self, avatars):
        assert self.notify.debugCall()
        avatarData=[]
        for i, slot in zip(avatars, range(6)):
            if i is None:
                avatarData.append(None)
            else:
                ad={}
                ad["name"]=i[0] # i.getName()
                ad["dna"]=i[1] # i.dna
                ad["slot"]=slot
                ad["id"]=i[2] # i.getDoId()
                avatarData.append(ad)
        return avatarData

    def finish(self):
        assert self.notify.debugCall()
        assert self.air is not None
        pirateAvatarsIds=self.neededObjects["pirateAvatars"]
        
        if self.gotAvatars:
            avatars = []
            for doId in pirateAvatarsIds:
                if doId:
                    name = self.neededObjects.get("setName-%s"%(doId,))
                    dna = self.neededObjects.get("setDNAString-%s"%(doId,))
                    avatars.append([name, dna, doId])
                else:
                    avatars.append(None)
            self.sendAvatarList(avatars)
        else:
            for avatarId in pirateAvatarsIds:
                if avatarId:
                    self.gotAvatars=1
                    self.neededObjects["setName-%s"%(avatarId,)]=None
                    self.neededObjects["setDNAString-%s"%(avatarId,)]=None
            if self.gotAvatars:
                # You may want to combine this with the above loop, but that
                # would be bad because we need all the neededObjects listed
                # before we start asking for them (each ask checks for
                # completion).
                for avatarId in pirateAvatarsIds:
                    if avatarId and hasattr(self, "air"):
                        self.askForObjectField(
                            "DistributedPlayerPirateUD",
                            "setName", avatarId, "setName-%s"%(avatarId,))
                        self.askForObjectField(
                            "DistributedPlayerPirateUD",
                            "setDNAString", avatarId, "setDNAString-%s"%(avatarId,))
                return
            else:
                avatars=[None for i in pirateAvatarsIds]
                self.sendAvatarList(avatars)
        ManagedAsyncRequest.finish(self)

    def sendAvatarList(self, avatars):
        assert self.notify.debugCall()
        avatarData=self.getAvatarData(avatars)
        pickleData=dumps(avatarData)
        self.distObj.sendUpdateToAvatarId(
            self.accountId, "avatarListResponse", [pickleData])

#-----------------------------------------------------------------------------

class AsyncRequestCreateAvatar(ManagedAsyncRequest):
    if __debug__:
        notify = notify

    def __init__(self, distObj, accountId, slot, avatarData):
        assert self.notify.debugCall()
        assert accountId
        self.rejectString="rejectCreateAvatar"
        ManagedAsyncRequest.__init__(self, distObj, distObj.air, accountId)
        self.accountId=accountId
        self.slot=slot
        self.avatarData=avatarData

        self.neededObjects[accountId]=None
        self.neededObjects["avatar"]=None
        self.neededObjects["friendsList"]=None

        self.askForObject(accountId)
        self.createObject("avatar", 'DistributedPlayerToon')
        self.createObject("friendsList", 'OtpFriendsList')

    def setupAvatar(self, avatar, friendsList, avatarData):
        assert self.notify.debugCall()
        avatar.saveDNA(avatarData)

    def finish(self):
        assert self.notify.debugCall()
        account=self.neededObjects[self.accountId]
        if not account.may('createAvatar'):
            # This account does not have permission to create an avatar:
            self.sendRejectCode(RejectCode.MAY_NOT_CREATE_AVATAR)
        elif self.slot > account.getSlotLimit():
            # This account doesn't have that many slots.
            self.sendRejectCode(RejectCode.SLOT_OUT_OF_RANGE)
        elif account.getPirate(self.slot):
            # They're trying to create an avatar in an already used slot.
            self.sendRejectCode(RejectCode.SLOT_TAKEN)
        else:
            self.createAvatar()
        ManagedAsyncRequest.finish(self)

    def createAvatar(self):
        assert self.notify.debugCall()
        account = self.neededObjects[self.accountId]
        avatar = self.neededObjects["avatar"]
        friendsList = self.neededObjects["friendsList"]

        avatarId = avatar.getDoId()

        assert avatarId
        assert friendsList.getDoId()

        avatar.sendSetFriendsListId(friendsList.getDoId())
        friendsList.sendSetOwnerId(avatarId)
        
        self.setupAvatar(avatar, friendsList, self.avatarData)

        account.setPirate(self.slot, avatarId)
        self.distObj.sendUpdateToAvatarId(
            self.accountId, "createAvatarResponse", [avatarId])

class DistributedAvatarManagerUD(OtpAvatarManagerUD):
    def __init__(self, air):
        OtpAvatarManagerUD.__init__(self, air)
        self.AsyncRequestAvatarList=AsyncRequestAvatarList
        self.AsyncRequestCreateAvatar=AsyncRequestCreateAvatar
 
