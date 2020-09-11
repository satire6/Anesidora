from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.friends import FriendResponseCodes



class PlayerFriendsManager(DistributedObjectGlobal):
    """
    The Player Friends Manager is a global object.
    This object handles client requests on player-level (as opposed to avatar-level) friends.

    See Also:
        "otp/src/friends/PlayerFriendsManagerUD.py"
        "otp/src/friends/AvatarFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('PlayerFriendsManager')

    def __init__(self, cr):
        assert self.notify.debugCall()
        DistributedObjectGlobal.__init__(self, cr)
        self.playerFriendsList = set()
        self.playerId2Info = {}
        self.playerAvId2avInfo = {} #a different (game specific) set of info 
        self.accept('gotExtraFriendHandles', self.__handleFriendHandles)

    # Functions called by the client
    def delete(self):
        self.ignoreAll()

    def sendRequestInvite(self,playerId):
        print ("PFM sendRequestInvite id:%s" % (playerId))
        assert self.notify.debugCall()
        self.sendUpdate("requestInvite", [0,playerId,True])

    def sendRequestDecline(self,playerId):
        assert self.notify.debugCall()
        self.sendUpdate("requestDecline", [0,playerId])

    def sendRequestRemove(self,playerId):
        # XXX cannot also use this as a "cancel invite" if we don't know the playerId yet
        assert self.notify.debugCall()
        self.sendUpdate("requestRemove", [0,playerId])

    def sendRequestUnlimitedSecret(self):
        assert self.notify.debugCall()
        self.sendUpdate("requestUnlimitedSecret", [0,])

    def sendRequestLimitedSecret(self,username,password):
        assert self.notify.debugCall()
        self.sendUpdate("requestLimitedSecret", [0,username,password])

    def sendRequestUseUnlimitedSecret(self,secret):
        assert self.notify.debugCall()
        self.sendUpdate("requestUseUnlimitedSecret", [0,secret])

    def sendRequestUseLimitedSecret(self,secret,username,password):
        assert self.notify.debugCall()
        self.sendUpdate("requestUseLimitedSecret", [0,secret,username,password])


    def sendSCWhisper(self,recipientId,msgId):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCTo",[0,recipientId,msgId])

    def sendSCCustomWhisper(self,recipientId,msgId):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCCustomTo",[0,recipientId,msgId])

    def sendSCEmoteWhisper(self,recipientId,msgId):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCEmoteTo",[0,recipientId,msgId])
        
    def setTalkAccount(self, toAc, fromAc, fromName, message, mods, flags):
        #print("setTalkAccount in PFM to:%s from:%s message:%s" % (toAc, fromAc, message))
        localAvatar.displayTalkAccount(fromAc, fromName, message, mods)
        toName = None
        friendInfo = self.getFriendInfo(toAc)
        if friendInfo:
            toName = friendInfo.playerName
        elif toAc == localAvatar.DISLid:
            toName = localAvatar.getName()
        base.talkAssistant.receiveAccountTalk(None, None, fromAc, fromName, toAc, toName, message) 

    #Functions called from UD

    def invitationFrom(self,playerId,avatarName):
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendInvitationEvent,[playerId,avatarName])

    def retractInvite(self,playerId):
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendRetractInviteEvent,[playerId])

    def rejectInvite(self,playerId,reason):
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendRejectInviteEvent,[playerId,reason])
        
    def rejectRemove(self,playerId,reason):
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendRejectRemoveEvent,[playerId,reason])

    def secretResponse(self,secret):
        print ("secretResponse %s"%(secret))
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendNewSecretEvent,[secret])

    def rejectSecret(self,reason):
        print ("rejectSecret %s"%(reason))
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendRejectNewSecretEvent,[reason])

    def rejectUseSecret(self,reason):
        print ("rejectUseSecret %s"%(reason))
        assert self.notify.debugCall()
        messenger.send(OTPGlobals.PlayerFriendRejectUseSecretEvent,[reason])
        
    def invitationResponse(self, playerId, respCode, context):
        if respCode == FriendResponseCodes.INVITATION_RESP_DECLINE:
            messenger.send(OTPGlobals.PlayerFriendRejectInviteEvent,[playerId,respCode])
        elif respCode == FriendResponseCodes.INVITATION_RESP_NEW_FRIENDS:
            pass
            


   #Functions called from UD

    def updatePlayerFriend(self,id,info,isNewFriend):
        assert self.notify.debugCall()
        self.notify.warning("updatePlayerFriend: %s, %s, %s" % (id,info,isNewFriend))
        info.calcUnderstandableYesNo()
        # ugly hack to make temp DNames (Guest0123456789) not look so ugly in Toontown
        if info.playerName[0:5] == 'Guest':
            info.playerName = 'Guest ' + info.playerName[5:]
        if id not in self.playerFriendsList:
            self.playerFriendsList.add(id)
            self.playerId2Info[id] = info
            messenger.send(OTPGlobals.PlayerFriendAddEvent,[id,info,isNewFriend])
        #need to detect if the playerFriend is coming online so we can send a message
        elif self.playerId2Info.has_key(id):
            if (not self.playerId2Info[id].onlineYesNo) and info.onlineYesNo:
                #send "coming online message"
                self.playerId2Info[id] = info
                messenger.send("playerOnline", [id])
                base.talkAssistant.receiveFriendAccountUpdate(id,info.playerName,info.onlineYesNo)
            elif (self.playerId2Info[id].onlineYesNo) and not info.onlineYesNo:
                #send "going offline message"
                self.playerId2Info[id] = info
                messenger.send("playerOffline", [id])
                base.talkAssistant.receiveFriendAccountUpdate(id,info.playerName,info.onlineYesNo)
        if not self.askAvatarKnownHere(info.avatarId):
            self.requestAvatarInfo(info.avatarId)
        self.playerId2Info[id] = info

        av = base.cr.doId2do.get(info.avatarId,None)
        if av is not None:
            av.considerUnderstandable()
        
        messenger.send(OTPGlobals.PlayerFriendUpdateEvent,[id,info])

    def removePlayerFriend(self,id):
        assert self.notify.debugCall()
        if not(id in self.playerFriendsList):
            return
        self.playerFriendsList.remove(id)
        info = self.playerId2Info.pop(id,None)
        if info is not None:
            av = base.cr.doId2do.get(info.avatarId,None)
            if av is not None:
                av.considerUnderstandable()
        messenger.send(OTPGlobals.PlayerFriendRemoveEvent,[id])

    def whisperSCFrom(self,playerId,msg):
        assert self.notify.debugCall()
        # print("whisperSCFrom %s %s" % (playerId,msg))
        base.talkAssistant.receivePlayerWhisperSpeedChat(msg, playerId)

    #client-called helper functions

    def isFriend(self,pId):
        return self.isPlayerFriend(pId)

    def isPlayerFriend(self,pId):
        if not pId:
            return 0
        return pId in self.playerFriendsList
        
    def isAvatarOwnerPlayerFriend(self, avId):
        pId = self.findPlayerIdFromAvId(avId)
        if pId and self.isPlayerFriend(pId):
            return True
        else:
            return False

    def getFriendInfo(self, pId):
        return self.playerId2Info.get(pId)
        
    def findPlayerIdFromAvId(self, avId):
        for playerId in self.playerId2Info:
            if self.playerId2Info[playerId].avatarId == avId:
                if self.playerId2Info[playerId].onlineYesNo:
                    return playerId
        return None
        
    def findAvIdFromPlayerId(self, pId):
        pInfo = self.playerId2Info.get(pId)
        if pInfo:
            return pInfo.avatarId
        else:
            return None
        
    def findPlayerInfoFromAvId(self, avId):
        playerId = self.findPlayerIdFromAvId(avId)
        if playerId:
            return self.getFriendInfo(playerId)
        else:
            return None
        
    def askAvatarOnline(self, avId):
        returnValue = 0
        if self.cr.doId2do.has_key(avId):
            returnValue = 1
        if self.playerAvId2avInfo.has_key(avId):
            playerId = self.findPlayerIdFromAvId(avId)
            if self.playerId2Info.has_key(playerId):
                playerInfo = self.playerId2Info[playerId]
                if playerInfo.onlineYesNo:
                    returnValue = 1
        return returnValue
        
    def countTrueFriends(self):
        count = 0
        for id in self.playerId2Info:
            if self.playerId2Info[id].openChatFriendshipYesNo:
                count += 1
        return count
        
    def askTransientFriend(self, avId):
        if self.playerAvId2avInfo.has_key(avId) and not base.cr.isAvatarFriend(avId):
            return 1
        else:
            return 0
        
    def askAvatarKnown(self, avId):
        if self.askAvatarKnownElseWhere(avId) or self.askAvatarKnownHere(avId):
            return 1
        else:
            return 0
        
    def askAvatarKnownElseWhere(self, avId):
        if hasattr(base, "cr"):
            if base.cr.askAvatarKnown(avId):
                return 1
        return 0

    def askAvatarKnownHere(self, avId):
        if self.playerAvId2avInfo.has_key(avId):
            return 1
        else:
            return 0
        
    def requestAvatarInfo(self, avId):
        if hasattr(base, "cr"):
            #base.cr.requestAvatarInfo(avId) 
            base.cr.queueRequestAvatarInfo(avId) 
        
    def __handleFriendHandles(self, handleList):
        for handle in handleList:
            # this line requires all handles to have the function getDoId, not much of a good way around it.
            self.playerAvId2avInfo[handle.getDoId()] = handle
        messenger.send('friendsListChanged')
            
    def getAvHandleFromId(self, avId):
        if self.playerAvId2avInfo.has_key(avId):
            return self.playerAvId2avInfo[avId]
        else:
            return None
            
    def identifyFriend(self, avId):
        handle = None
        handle = base.cr.identifyFriend(avId)
        if not handle:
            handle = self.getAvHandleFromId(avId)
        return handle
            
    def getAllOnlinePlayerAvatars(self):
        returnList = []
        for avatarId in self.playerAvId2avInfo:
            playerId = self.findPlayerIdFromAvId(avatarId)
            if playerId:
                if self.playerId2Info[playerId].onlineYesNo:
                    returnList.append(avatarId)
        return returnList
        
    def identifyAvatar(self, doId):
        """
        Returns either an avatar or a FriendHandle, whichever we can
        find, to reference the indicated doId.
        """
        if base.cr.doId2do.has_key(doId):
            return base.cr.doId2do[doId]
        else:
            return self.identifyFriend(doId)

    def friendsListFull(self):
        return len(self.playerFriendsList) >= OTPGlobals.MaxPlayerFriends
            
    
            
        
        
        
