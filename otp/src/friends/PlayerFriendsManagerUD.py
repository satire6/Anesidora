from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.task.Task import Task
from otp.otpbase import OTPGlobals
from otp.ai import AIMsgTypes
from otp.uberdog.RejectCode import RejectCode

from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.friends.FriendInfo import FriendInfo
from otp.switchboard.sbWedge import sbWedge

from otp.otpbase import OTPLocalizerEnglish as localizer

import random


#--------------------------------------------------


class PlayerFriendsManagerUD(DistributedObjectGlobalUD,sbWedge):
    """
    The Player Friends Manager is a global object.
    This object handles client requests on player-level (as opposed to avatar-level) friends.

    See Also:
        "otp/src/friends/AvatarFriendsManager.py"
        "otp/src/friends/PlayerFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('PlayerFriendsManagerUD')

    def __init__(self, air, sbListenPort=8888, wedgeName=None, locationName="OTP"):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)

        self.sbName = wedgeName
        self.locationName = locationName
        
        if self.sbName is None:
            self.sbName = "OTP%d" % random.randint(0,99999)

        self.everyoneIsFriends = uber.config.GetBool("everyone-is-friends",0)
        
        self.sbHost = uber.sbNSHost
        self.sbPort = uber.sbNSPort
        self.sbListenPort = uber.sbListenPort
        self.clHost = uber.clHost 
        self.clPort = uber.clPort
        self.allowUnfilteredChat = uber.allowUnfilteredChat
        self.bwDictPath = uber.bwDictPath

        #self.avatarId2FriendsList = {}
        self.playerId2Invitations = {}
        #self.avatarId2Name = {}
        #self.avatarId2Info = {}
        #self.avatarId2Account = {}

        #self.isAvatarOnline = {}

        #self.isAccountOnline = {}

        #self.accountId2Info = {}
        #self.accountId2Friends = {}

        self.accept("avatarOnlinePlusAccountInfo", self.avatarOnlinePlusAccountInfo, [])
        self.accept("avatarOffline", self.avatarOffline, [])

        sbWedge.__init__(self,wedgeName=self.sbName,
                         nsHost=self.sbHost,
                         nsPort=self.sbPort,
                         listenPort=self.sbListenPort,
                         clHost=self.clHost,
                         clPort=self.clPort,
                         allowUnfilteredChat=self.allowUnfilteredChat,
                         bwDictPath=self.bwDictPath)

        def CheckSBWedge(task):
            self.handleRequests(0)
            return Task.cont

        uber.taskMgr.add(CheckSBWedge,'checkSBwedge')


    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.sendUpdateToChannel(
            AIMsgTypes.CHANNEL_CLIENT_BROADCAST, "online", [])
        self.sendUpdateToChannel(
            AIMsgTypes.OTP_CHANNEL_AI_AND_UD_BROADCAST, "online", [])


    def delete(self):
        assert self.notify.debugCall()
        self.ignoreAll()
        DistributedObjectGlobalUD.delete(self)

    #----------------------------------

    def avatarOnline(self,avatarId,avatarType):
        pass

    def avatarOnlinePlusAccountInfo(self,avatarId,accountId,playerName,
                                    playerNameApproved,openChatEnabled,
                                    createFriendsWithChat,chatCodeCreation):
        assert self.notify.debugCall()

        if accountId in [-1, 0]:
            return

        self.log.debug("Account online.  Info: %d, %d, %s, %s, %s, %s, %s"%(avatarId,
                                                                            accountId,
                                                                            playerName,
                                                                            playerNameApproved,
                                                                            openChatEnabled,
                                                                            createFriendsWithChat,
                                                                            chatCodeCreation))
        
        if playerName == "Guest":
            accountInfo = FriendInfo(avatarName="%d"%avatarId,
                                     playerName="%s%d" % (playerName,accountId),
                                     onlineYesNo=1,
                                     openChatEnabledYesNo=openChatEnabled,
                                     avatarId=avatarId,
                                     location=self.locationName,
                                     sublocation="")
        else:
            accountInfo = FriendInfo(avatarName="%d"%avatarId,
                                     playerName=playerName,
                                     onlineYesNo=1,
                                     openChatEnabledYesNo=openChatEnabled,
                                     avatarId=avatarId,
                                     location=self.locationName,
                                     sublocation="")
        # Don't have my avatar name yet, asyncrequest it
        context = self.air.allocateContext()
        dclassName = "DistributedAvatarUD"
        self.air.contextToClassName[context] = dclassName
        self.acceptOnce("doFieldResponse-%s"%context,self.recvAvatarName,[accountId,accountInfo])
        self.air.queryObjectField(dclassName,"setName",avatarId,context)


    def recvAvatarName(self,accountId,accountInfo,context,name):
        self.notify.debug("avatarName fetched for account %d: %s" % (accountId,name[0]))
        accountInfo.avatarName = name[0]

        # asynchronous request to SB which will tell everyone we're here and fetch our friends
        if self.sbConnected:
            self.enterPlayer(accountId,accountInfo)


    def recvFriendsUpdate(self,accountId,accountInfo,friends):
        self.log.debug("recvFriendsUpdate on %d -> %s"%(accountId,str(friends)))
        for friend in friends:
            friendId = friend[0]
            friendInfo = friend[1]

            accountInfo.timestamp = 0
            friendInfo.timestamp = 0

            accountInfo.openChatFriendshipYesNo = friendInfo.openChatFriendshipYesNo

            accountInfo.understandableYesNo = friendInfo.openChatFriendshipYesNo or \
                                              (friendInfo.openChatEnabledYesNo and \
                                               accountInfo.openChatEnabledYesNo)
            
            friendInfo.understandableYesNo = friendInfo.openChatFriendshipYesNo or \
                                             (friendInfo.openChatEnabledYesNo and \
                                              accountInfo.openChatEnabledYesNo)

            if accountInfo.onlineYesNo:
                self.sendUpdateToChannel((3L<<32)+accountId,
                                         "updatePlayerFriend",
                                         [friendId,friendInfo,0])

            self.sendUpdateToChannel((3L<<32)+friend[0],
                                     "updatePlayerFriend",
                                     [accountId,accountInfo,0])


    @report(types = ['args'], dConfigParam = 'orphanedavatar')
    def avatarOffline(self,avatarId):
        assert self.notify.debugCall()

        self.exitAvatar(avatarId)


#----------------------------------------------------------------------


    # Functions called by the client

    def requestInvite(self, senderId, otherPlayerId, secretYesNo=True):
        assert self.notify.debugCall()
        self.sendOpenInvite(senderId,otherPlayerId,secretYesNo)

    def requestDecline(self, senderId, otherId):
        """
        Call this function to retract an invite to or decline an invite from another player.
        """
        self.sendDeclineInvite(senderId,otherId)

    def requestRemove(self, senderId, otherAccountId):
        """
        Call this function if you want to remove an existing friend from your friends list.
        
        otherAccountId may be online or offline.
        """
        accountId = senderId
        self.air.writeServerEvent('requestFriendRemove', accountId, '%s' % otherAccountId)
                
        # update DISL friends list through Switchboard
        self.removeFriendship(accountId,otherAccountId)

    def recvInviteNotice(self, inviteeId, inviterId, inviterAvName):
        self.sendUpdateToChannel((3L<<32)+inviteeId, "invitationFrom", [inviterId,inviterAvName])

    def recvInviteRetracted(self, inviteeId, inviterId):
        self.sendUpdateToChannel((3L<<32)+inviteeId, "retractInvite", [inviterId])

    def recvInviteRejected(self, inviterId, inviteeId, reason):
        self.sendUpdateToChannel((3L<<32)+inviterId, "rejectInvite", [inviteeId, reason])

    def recvFriendshipRemoved(self,accountId,otherAccountId):
        self.notify.debug("recvFriendshipRemoved on %d,%d"%(accountId,otherAccountId))

        self.sendUpdateToChannel((3L<<32)+accountId,"removePlayerFriend",[otherAccountId])
        self.sendUpdateToChannel((3L<<32)+otherAccountId,"removePlayerFriend",[accountId])        


    # SECRETS
    def requestUnlimitedSecret(self,senderId):
        print "# got unlimited secret request"
        self.sendSecretRequest(senderId)
        
    def requestLimitedSecret(self,senderId,parentUsername,parentPassword):
        print "# got limited secret request"
        self.sendSecretRequest(senderId,parentUsername,parentPassword)

    def requestUseUnlimitedSecret(self,senderId,secret):
        self.sendSecretRedeem(senderId,secret)

    def requestUseLimitedSecret(self,senderId,secret,parentUsername,parentPassword):
        self.sendSecretRedeem(senderId,secret,parentUsername,parentPassword)

    def recvAddFriendshipError(self,playerId,error):
        self.sendUpdateToChannel((3L<<32)+playerId,"rejectInvite",[error])

    def recvSecretGenerated(self,playerId,secret):
        self.sendUpdateToChannel((3L<<32)+playerId,"secretResponse",[secret])

    def recvSecretRequestError(self,playerId,error):
        self.sendUpdateToChannel((3L<<32)+playerId,"rejectSecret",[error])

    def recvSecretRedeemError(self,playerId,error):
        self.sendUpdateToChannel((3L<<32)+playerId,"rejectUseSecret",[error])


    # WHISPERS

    def whisperTo(self,senderId,playerId,msg):
        assert self.sbConnected

        self.log.debug("PFMUD whisper - %d to %d: %s" % (senderId,playerId,msg))

        if senderId == -1 or playerId == -1:
            return

        if self._validateChatMessage(playerId,senderId,msg):
            self.sendWhisper(playerId,senderId,msg)


    def whisperWLTo(self,senderId,playerId,msg):
        assert self.sbConnected

        self.log.debug("PFMUD WLwhisper - %d to %d: %s" % (senderId,playerId,msg))

        if senderId == -1 or playerId == -1:
            return

        # Validation being handled by client agents, do not need
        #if self._validateChatMessage(playerId,senderId,msg):
        self.sendWLWhisper(playerId,senderId,msg)


    def whisperSCTo(self,senderId,playerId,msgId):
        assert self.sbConnected

        self.log.debug("PFMUD SCwhisper - %d to %d: %s" % (senderId,playerId,msgId))

        if senderId == -1 or playerId == -1:
            return

        msgText = self._translateWhisper(msgId)

        if msgText is None:
            self.log.security("Invalid SC index: %d to %d: %d" % (senderId,playerId,msgId))
            return

        if self._validateChatMessage(playerId,senderId,msgText):
            self.sendSCWhisper(playerId,senderId,msgText)
            


    def whisperSCCustomTo(self,senderId,playerId,msgId):
        assert self.sbConnected

        self.log.debug("PFMUD SCCustomwhisper - %d to %d: %s" % (senderId,playerId,msgId))
        
        if senderId == -1:
            return

        msgText = self._translateWhisperCustom(msgId)

        if msgText is None:
            self.log.security("Invalid SC custom index: %d to %d: %d" % (senderId,playerId,msgId))
            return

        if self._validateChatMessage(playerId,senderId,msgText):
            self.sendSCWhisper(playerId,senderId,msgText)


    def whisperSCEmoteTo(self,senderId,playerId,msgId):
        assert self.sbConnected

        self.log.debug("PFMUD SCEmotewhisper - %d to %d: %s" % (senderId,playerId,msgId))

        if senderId == -1:
            return

        msgText = self._translateWhisperEmote(msgId)

        if msgText is None:
            self.log.security("Invalid SC emote index: %d to %d: %d" % (senderId,playerId,msgId))
            return

        # XXX Temporarily broken--where does the avatarname come from if we're stateless?
        # Stick the sender's avatar name into the emote message!
        #senderInfo = self.accountId2Info.get(senderId,None)
        #if senderInfo is not None:
        #    msgText = msgText % (senderInfo.avatarName)

        if self._validateChatMessage(playerId,senderId,msgText):
            self.sendSCWhisper(playerId,senderId,msgText)


    def whisperSCQuestTo(self,senderId,playerId,msgData):
        '''
        Quest messages.  Uses product-specific _translateWhisperQuest that should be overridden
        '''
        assert self.sbConnected

        self.log.debug("PFMUD SCQuestwhisper - %d to %d: %s" % (senderId,playerId,msgData))

        if senderId == -1:
            return

        msgText = self._translateWhisperQuest(msgData)

        if msgText is None:
            self.log.security("Invalid SC quest data: %d to %d: %d" % (senderId,playerId,msgData))
            return

        if self._validateChatMessage(playerId,senderId,msgText):
            self.sendSCWhisper(playerId,senderId,msgText)
        

    #WEDGE -> UD functions

    def recvWhisper(self,recipientId,senderId,msgText):
        self.log.debug("Received open whisper from %d to %d: %s" % (senderId,recipientId,msgText))
        self.sendUpdateToChannel((3L<<32)+recipientId,"whisperFrom",[senderId,msgText])

    def recvWLWhisper(self,recipientId,senderId,msgText):
        self.log.debug("Received WLwhisper from %d to %d: %s" % (senderId,recipientId,msgText))
        self.sendUpdateToChannel((3L<<32)+recipientId,"whisperWLFrom",[senderId,msgText])

    def recvSCWhisper(self,recipientId,senderId,msgText):
        self.log.debug("Received SCwhisper from %d to %d: %s" % (senderId,recipientId,msgText))
        self.sendUpdateToChannel((3L<<32)+recipientId,"whisperSCFrom",[senderId,msgText])

    def recvEnterPlayer(self,playerId,playerInfo,friendsList):
        self.log.debug("Saw player %d enter."%playerId)
        self.log.debug("friends list: %s"%friendsList)
        
        for friend in friendsList:
            self.notify.debug("update to %d saying that %d is online" % (friend,playerId))
            friendInfo = friendsList[friend]
            playerInfo.openChatFriendshipYesNo = friendInfo.openChatFriendshipYesNo
            playerInfo.understandableYesNo = friendInfo.openChatFriendshipYesNo or \
                                             (friendInfo.openChatEnabledYesNo and \
                                              playerInfo.openChatEnabledYesNo)
            self.sendUpdateToChannel((3L<<32)+friend,
                                     "updatePlayerFriend",
                                     [playerId,playerInfo,0])


    def recvExitPlayer(self,playerId,playerInfo,friendsList):
        self.log.debug("Saw player %d exit."%playerId)
        self.log.debug("friends list: %s"%friendsList)
        
        for friend in friendsList:
            self.notify.debug("update to %d saying that %d is offline" % (friend,playerId))
            friendInfo = friendsList[friend]
            playerInfo.openChatFriendshipYesNo = friendInfo.openChatFriendshipYesNo
            playerInfo.understandableYesNo = friendInfo.openChatFriendshipYesNo or \
                                             (friendInfo.openChatEnabledYesNo and \
                                              playerInfo.openChatEnabledYesNo)
            self.sendUpdateToChannel((3L<<32)+friend,
                                     "updatePlayerFriend",
                                     [playerId,playerInfo,0])


    # helper functions

    def _getFriendView(self, viewerId, friendId, info=None):
        if info is None:
            info = self.accountId2Info[friendId]
        if self.accountId2Friends.has_key(viewerId):
            if [friendId,True] in self.accountId2Friends[viewerId]:
                info.openChatFriendshipYesNo = 1
            else:
                info.openChatFriendshipYesNo = 0
        elif self.accountId2Friends.has_key(friendId):
            if [viewerId,True] in self.accountId2Friends[friendId]:
                info.openChatFriendshipYesNo = 1
            else:
                info.openChatFriendshipYesNo = 0            
        else:
            info.openChatFriendshipYesNo = 0

        if self._whisperAllowed(viewerId,friendId):
            info.understandableYesNo = 1
        else:
            info.understandableYesNo = 0

        info.timestamp = 0
            
        return info


    def _whisperAllowed(self, fromPlayer, toPlayer):
        fromFriends = self.accountId2Friends.get(fromPlayer)

        if fromFriends:
            if [toPlayer,True] in fromFriends:
                return True
            elif [toPlayer,False] in fromFriends:
                fromInfo = self.accountId2Info.get(fromPlayer)
                toInfo = self.accountId2Info.get(toPlayer)

                if toInfo and fromInfo.openChatEnabledYesNo and toInfo.openChatEnabledYesNo:
                    return True
                else:
                    return False
        else:
            return False


    def _whisperSCAllowed(self, fromPlayer, toPlayer):
        fromFriends = self.accountId2Friends.get(fromPlayer)

        if fromFriends:
            if [toPlayer,True] in fromFriends or [toPlayer,False] in fromFriends:
                return True
            else:
                return False
        else:
            return False

    def _translateWhisper(self,msgId):
        return localizer.SpeedChatStaticText.get(msgId)

    def _translateWhisperCustom(self,msgId):
        return localizer.CustomSCStrings.get(msgId)

    def _translateWhisperEmote(self,msgId):
        if msgId >= len(localizer.EmoteWhispers) or msgId < 0:
            return None
        else:
            return localizer.EmoteWhispers[msgId]

    def _translateWhisperQuest(self,msgData):
        '''
        Translate quest SC data to a text message.
        Product-specific and should be overridden!
        '''
        return None
