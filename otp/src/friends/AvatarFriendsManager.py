from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.uberdog.RejectCode import RejectCode
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer


class AvatarFriendsManager(DistributedObjectGlobal):
    """
    The Avatar Friends Manager is a global object.
    This object handles client requests on avatar-level (as opposed to player-level) friends.

    See Also:
        "otp/src/friends/AvatarFriendsManagerUD.py"
        "otp/src/friends/PlayerFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('AvatarFriendsManager')

    def __init__(self, cr):
        assert self.notify.debugCall()
        DistributedObjectGlobal.__init__(self, cr)
        self.reset()

    def reset(self):
        self.avatarFriendsList = set()
        self.avatarId2Info = {}
        self.invitedAvatarsList = []
        self.ignoredAvatarList = []
        
    #Client only functions
    def addIgnore(self, avId):
        if avId not in self.ignoredAvatarList:
            self.ignoredAvatarList.append(avId)
            base.cr.centralLogger.writeClientEvent('ignoring %s' % (avId,))
        messenger.send("AvatarIgnoreChange")
            
    def removeIgnore(self, avId):
        if avId in self.ignoredAvatarList:
            self.ignoredAvatarList.remove(avId)
            base.cr.centralLogger.writeClientEvent('stopped ignoring %s' % (avId,))
        messenger.send("AvatarIgnoreChange")
            
    def checkIgnored(self, avId):
        """ 
        This should be checked before querying the user for 
        interaction or popping up guis requested by other
        avatars
        """
        return avId and avId in self.ignoredAvatarList

    #Client->UD request functions

    def sendRequestInvite(self,avId):
        self.notify.debugCall()
        self.sendUpdate("requestInvite", [avId])
        self.invitedAvatarsList.append(avId)

    def sendRequestRemove(self,avId):
        self.notify.debugCall()
        self.sendUpdate("requestRemove", [avId])
        if avId in self.invitedAvatarsList:
            self.invitedAvatarsList.remove(avId)


    #Functions called from UD

    def friendConsidering(self,avId):
        self.notify.debugCall()
        messenger.send(OTPGlobals.AvatarFriendConsideringEvent,[1,avId])

    def invitationFrom(self,avId,avatarName):
        self.notify.debugCall()
        messenger.send(OTPGlobals.AvatarFriendInvitationEvent,[avId,avatarName])

    def retractInvite(self,avId):
        self.notify.debugCall()
        messenger.send(OTPGlobals.AvatarFriendRetractInviteEvent,[avId])
        if avId in self.invitedAvatarsList:
            self.invitedAvatarsList.remove(avId)

    def rejectInvite(self,avId,reason):
        self.notify.debugCall()
        messenger.send(OTPGlobals.AvatarFriendRejectInviteEvent,[avId,reason])
        if avId in self.invitedAvatarsList:
            self.invitedAvatarsList.remove(avId)

    def rejectRemove(self,avId,reason):
        self.notify.debugCall()
        messenger.send(OTPGlobals.AvatarFriendRejectRemoveEvent,[avId,reason])



   #Functions called from UD

    def updateAvatarFriend(self,avId,info):
        if hasattr(info, "avatarId") and (not info.avatarId) and avId:
            #info.avatarId wasn't being populated, I think this is fixed now
            # though it's odd to have the data in two places
            info.avatarId = avId
            
        assert self.notify.debugCall()
        if not avId in self.avatarFriendsList:
            self.avatarFriendsList.add(avId)
            self.avatarId2Info[avId] = info #get the data there before we tell you it's there
            messenger.send(OTPGlobals.AvatarFriendAddEvent,[avId,info])
            
        if self.avatarId2Info[avId].onlineYesNo != info.onlineYesNo:
            base.talkAssistant.receiveFriendUpdate(avId, info.getName(), info.onlineYesNo)
                
        self.avatarId2Info[avId] = info
        messenger.send(OTPGlobals.AvatarFriendUpdateEvent,[avId,info])
        if avId in self.invitedAvatarsList:
            self.invitedAvatarsList.remove(avId)
            messenger.send(OTPGlobals.AvatarNewFriendAddEvent,[avId])

    def removeAvatarFriend(self,avId):
        assert self.notify.debugCall()
        self.avatarFriendsList.remove(avId)
        self.avatarId2Info.pop(avId,None)
        messenger.send(OTPGlobals.AvatarFriendRemoveEvent,[avId])
        


    
    def setFriends(self, avatarIds):
        self.notify.debugCall()
        assert 0, "setFriends should not be sent to client."



    # client-called helper functions

    def isFriend(self,avId):
        return self.isAvatarFriend(avId)

    def isAvatarFriend(self, avId):
        return avId in self.avatarFriendsList

    def getFriendInfo(self,avId):
        return self.avatarId2Info.get(avId)
        
    def countTrueFriends(self):
        count = 0
        for id in self.avatarId2Info:
            if self.avatarId2Info[id].openChatFriendshipYesNo:
                count += 1
        return count
