from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.avatar.AvatarHandle import AvatarHandle
from otp.ai import AIInterestHandles

GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1


import Queue

class GuildMemberInfo(AvatarHandle):
    def __init__(self, name, isOnline, rank, bandId):
        self.name = name
        self.rank = rank
        self.bandId = bandId
        self.onlineYesNo = isOnline
        
    def getName(self):
        return self.name

    def getRank(self):
        return self.rank
    
    def getBandId(self):
        return self.bandId

    def isOnline(self):
        return self.onlineYesNo
    
    def isUnderstandable(self):
        # This is for compatibility with the ClientRepository's
        # identifyFriend() function
        return True

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        base.cr.guildManager.d_reflectTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId = None):
        base.cr.guildManager.d_reflectTeleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)

class GuildManager(DistributedObjectGlobal):
    """
    See Also:
        "otp/src/friends/GuildManagerUD.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('GuildManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

        self.id2Name = {}
        self.id2BandId = {}
        self.id2Rank = {}
        self.id2Online = {}
        # queue for incoming msgs we can't display yet
        self.pendingMsgs = []

        self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1)

        # These are the email notification preferences for the avatar
        # They are set by respondEmailNotificationPref

        self.emailNotification = 0
        self.emailNotificationAddress = None

        self.receivingNewList = False

        self.spamGateOpen = True

    def _allowMemberList(self,task):
        self.spamGateOpen = True
        return task.done
        
    # Functions called by the client
    def memberList(self):
        if self.spamGateOpen:
            self.sendUpdate("memberList", [])
            self.spamGateOpen = False
            taskMgr.doMethodLater(60.0,self._allowMemberList,"allowMemberList")

    def createGuild(self):
        # Make sure to decline any other guild invitations
        messenger.send("declineGuildInvitation")
        
        self.sendUpdate("createGuild", [])

    def setWantName(self, newName):
        self.sendUpdate("setWantName", [newName])

    def removeMember(self, avatarId):
        self.sendUpdate("removeMember", [avatarId])

    def changeRank(self, avatarId, rank):
        self.sendUpdate("changeRank", [avatarId, rank])

    def statusRequest(self):
        self.sendUpdate("statusRequest", [])

    def requestLeaderboardTopTen(self):
        self.sendUpdate("requestLeaderboardTopTen", [])

    def sendRequestInvite(self, avatarId):
        self.sendUpdate("requestInvite", [avatarId])

    def sendAcceptInvite(self):
        self.sendUpdate("acceptInvite", [])

    def sendDeclineInvite(self):
        self.sendUpdate("declineInvite", [])

    def sendTalk(self,msgText,chatFlags=0):
        self.sendUpdate("setTalkGroup",[0,0,"",msgText,[],0])
        
    def setTalkGroup(self, fromAv, fromAC, avatarName, chat, mods, flags):
        if hasattr(base, "localAvatar"):
            message, scrubbed = localAvatar.scrubTalk(chat, mods)
            base.talkAssistant.receiveGuildTalk(fromAv, fromAC, avatarName, message, scrubbed)
        

    def sendSC(self,msgIndex):
        self.sendUpdate("sendSC",[msgIndex])

    def sendSCQuest(self,questInt,msgType,taskNum):
        self.sendUpdate("sendSCQuest",[questInt,msgType,taskNum])

    def sendTokenRequest(self):
        self.sendUpdate("sendTokenRequest", [])

    def sendTokenForJoinRequest(self, token):
        # print "GuildManager.sendTOkenForJoinRequest() Called : %s" % token
        name = base.localAvatar.getName()
        self.sendUpdate("sendTokenForJoinRequest", [token, name])

    def isInGuild(self, avId):
        return avId in self.id2Name

    def getRank(self, avId):
        return self.id2Rank.get(avId)

    def getBandId(self, avId):
        return self.id2BandId.get(avId)
    
    def getMemberInfo(self, avId):
        if self.isInGuild(avId):
            return GuildMemberInfo(self.id2Name[avId],
                                   self.id2Online[avId],
                                   self.id2Rank[avId],
                                   self.id2BandId[avId],
                                   )
        return None

    def getOptionsFor(self, avId):
        """
        Returns (canpromote, candemote, cankick) based on whether
        localAvatar can perform these operations on avId.

        Returns None if  avId is not in guild.
        """
        if self.isInGuild(avId):
            myRank = localAvatar.getGuildRank()
            hisRank = self.id2Rank[avId]

            canpromote = False 
            candemote = False
            cankick = False

            if myRank == GUILDRANK_GM:
                if hisRank == GUILDRANK_OFFICER:
                    candemote = True
                elif hisRank == GUILDRANK_MEMBER:
                    canpromote = True
            if myRank > GUILDRANK_MEMBER and \
               hisRank <= GUILDRANK_MEMBER:
                cankick = True

            return (canpromote, candemote, cankick)
        else:
            return None
        
    def updateTokenRValue(self, tokenString, rValue):
        # Send this token and redeem value up to the server.
        # The token in tokenString will be assigned the rValue
        # Just to be sure we're sending the right thing, cast rValue to an int
        rValue = int(rValue)
        # print 'Sending following values: %s, %s' % (tokenString, rValue)
        self.sendUpdate("sendTokenRValue", [tokenString, rValue])
        if rValue == -1:
            base.localAvatar.guiMgr.guildPage.receivePermTokenValue(tokenString)

    def requestPermToken(self):
        # Requests the perm member token (if one exists).
        self.sendUpdate("sendPermToken", [])

    def requestNonPermTokenCount(self):
        # Requests a count of the non perm member tokens
        self.sendUpdate('sendNonPermTokenCount', [])

    def requestClearTokens(self, type):
        # Requests tokens are cleared for the calling avatar.
        # type can be one of two types:
        # 0 = One time and limited mulituse codes
        # 1 = Perm Token
        self.sendUpdate("sendClearTokens", [type])


    #Functions called from UD

    def receiveMember(self, member):
        if not self.receivingNewList:
            self.receivingNewList = True
            self.newList = []

        self.newList.append(member)

    def clearMembers(self):
        self.newList = []
        self.receiveMembersDone()

    def receiveMembersDone(self):
        self.receivingNewList = False

        memberlist = self.newList
        self.newList = []

        self.id2Name = {}
        self.id2Rank = {}
        self.id2BandId = {}
        
        # Pass the member list to the guild GUI for use
        for guy in memberlist:
            id = guy[0]
            name = guy[1]
            rank = guy[2]
            isOnline = guy[3]
            self.id2Name[id] = name
            self.id2Rank[id] = rank
            self.id2Online[id] = isOnline
            self.id2BandId[id] = tuple(guy[4:6])

        for id,msg in self.pendingMsgs:
            # move this check to chatAssistant some day
            if not self.cr.avatarFriendsManager.checkIgnored(id):
                #base.talkAssistant.receiveGuildMessage("%s %s %s" % (self.id2Name.get(id,"Unknown"),
                #                                                     OTPLocalizer.GuildPrefix,
                #                                                     msg))
                base.talkAssistant.receiveGuildMessage(msg, id, self.id2Name.get(id,"Unknown"))

        if localAvatar.getGuildId():
            self.accept(self.cr.StopVisibilityEvent,
                        self.handleLogout)
        else:
            self.ignore(self.cr.StopVisibilityEvent)
        
        if hasattr(base, "localAvatar"):    
            base.localAvatar.guiMgr.guildPage.receiveMembers(memberlist)
        messenger.send('guildMemberUpdated', sentArgs = [localAvatar.doId])
        
        
    def guildStatusUpdate(self, guildId, guildName, guildRank):
        if hasattr(base, "localAvatar"):
            base.localAvatar.guildStatusUpdate(guildId, guildName, guildRank)
        self.memberList()

    def guildNameReject(self, guildId):
        if hasattr(base, "localAvatar"):
            base.localAvatar.guildNameReject(guildId)
        
    def guildNameChange(self, guildName, changeStatus):
        if hasattr(base, "localAvatar"):
            base.localAvatar.guildNameChange(guildName, changeStatus)

    def guildNameUpdate(self, avatarId, guildName):
        print "DEBUG - guildNameUpdate for ", avatarId, " to ", guildName

    def invitationFrom(self, avatarId, avatarName, guildId, guildName):
        print "GM invitationFrom %s(%d)" % (avatarName,avatarId)
        if hasattr(base, "localAvatar"):
            base.localAvatar.guiMgr.handleGuildInvitation(avatarId, avatarName, guildId, guildName)

    def retractInvite(self,avatarId):
        print "GM retraction"

    def guildAcceptInvite(self, avatarId):
        # Tell ourselves the person we are inviting accepted us
        print "sending accept event"
        messenger.send(OTPGlobals.GuildAcceptInviteEvent,[avatarId])

    def leaderboardTopTen(self, stuff):
        base.localAvatar.guiMgr.handleTopTen(stuff)

    def guildRejectInvite(self, avatarId, reason):
        # Tell ourselves the person we are inviting rejected us
        messenger.send(OTPGlobals.GuildRejectInviteEvent,[avatarId,reason])

    def rejectInvite(self,avatarId,reason):
        # print "GM rejectInvite to %d because of %d" % (avatarId,reason)
        pass
    



    def recvSC(self,senderId,msgIndex):
        senderName = self.id2Name.get(senderId,None)
        if (senderName):
            # move this check to chatAssistant some day
            if not self.cr.avatarFriendsManager.checkIgnored(senderId):
                displayMess = "%s %s %s" % (senderName, OTPLocalizer.GuildPrefix,
                                            OTPLocalizer.SpeedChatStaticText[msgIndex])
                message = OTPLocalizer.SpeedChatStaticText[msgIndex]
                base.talkAssistant.receiveGuildMessage(message, senderId, senderName)
        else:
            self.pendingMsgs.append([senderId,OTPLocalizer.SpeedChatStaticText[msgIndex]])
            self.memberList()

    def recvSCQuest(self,senderId,questInt,msgType,taskNum):
        senderName = self.id2Name.get(senderId,None)
        message = base.talkAssistant.SCDecoder.decodeSCQuestMsgInt(questInt,msgType,taskNum)
        if (senderName):
            # move this check to chatAssistant some day
            if not self.cr.avatarFriendsManager.checkIgnored(senderId):
                displayMess = "%s %s %s" % (senderName, OTPLocalizer.GuildPrefix, message)
                base.talkAssistant.receiveGuildMessage(message, senderId, senderName)
        else:
            self.pendingMsgs.append([senderId,message])
            self.memberList()

    def recvAvatarOnline(self, avatarId, avatarName, bandManagerId, bandId):
        self.id2Online[avatarId] = True
        # Print out a message in the chat log, update the panel we're looking at, play a tick sound, etc!
        if hasattr(base, 'localAvatar') and \
           avatarId != base.localAvatar.doId:
            # move this check to chatAssistant some day
            if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
                base.talkAssistant.receiveGuildUpdate(avatarId,avatarName,True)
        else:
            return
        # Send message so guild guis can pick up the update
        messenger.send("guildMemberOnlineStatus", [avatarId, 1])
        
    def recvAvatarOffline(self,avatarId,avatarName):
        # Print out a message in the chat log, update the panel we're looking at, play a tick sound, etc!
        # Guard against the case where the localAvatar just logged out and he is hearing his own
        # offline message.
        self.id2BandId[avatarId] = (0,0)
        self.id2Online[avatarId] = False
        if hasattr(base, "localAvatar") and \
           avatarId != base.localAvatar.doId:
            # move this check to chatAssistant some day
            if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
                base.talkAssistant.receiveGuildUpdate(avatarId,avatarName,False)
        # Send message so guild guis can pick up the update
        messenger.send("guildMemberOnlineStatus", [avatarId, 0])

    def recvMemberAdded(self, memberInfo):
        avatarId, avatarName, rank, isOnline, bandManagerId, bandId = memberInfo
        self.id2Name[avatarId] = avatarName
        self.id2Rank[avatarId] = rank
        self.id2BandId[avatarId] = (bandManagerId, bandId)
        self.id2Online[avatarId] = isOnline
        if hasattr(base, "localAvatar"):
            base.localAvatar.guiMgr.guildPage.addMember(memberInfo)
        messenger.send('guildMemberUpdated', sentArgs = [avatarId])
        
    def recvMemberRemoved(self, avatarId):
        if avatarId == localAvatar.doId:
            self.clearMembers()
        else:
            self.id2Name.pop(avatarId, None)
            self.id2Rank.pop(avatarId, None)
            self.id2BandId.pop(avatarId, None)
            self.id2Online.pop(avatarId, None)
            if hasattr(base, 'localAvatar'):
                base.localAvatar.guiMgr.guildPage.removeMember(avatarId)
        messenger.send('guildMemberUpdated', sentArgs = [avatarId])
        
    def recvMemberUpdateRank(self, avatarId, rank):
        self.id2Rank[avatarId] = rank
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.updateGuildMemberRank(avatarId, rank)
        messenger.send('guildMemberUpdated', sentArgs = [avatarId])
        
    def recvMemberUpdateBandId(self, avatarId, bandManagerId, bandId):
        self.id2BandId[avatarId] = (bandManagerId, bandId)
        messenger.send('guildMemberUpdated', sentArgs = [avatarId])
        
    def recvTokenInviteValue(self, tokenValue, preExistPerm):
        # print "Token Received from server: %s" % (tokenValue)
        # if tokenValue == 'TOO_MANY_TOKENS':
            # print "WARNING: This Avatar has too many tokens pending"
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.displayInviteGuild(tokenValue, preExistPerm)

    def recvTokenRedeemMessage(self, guildName):
        # print "Guild (join) message received from server: %s" % (guildName)
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if guildName == '***ERROR - GUILD CODE INVALID***':
                # print "Warning: The guild name is false, request doesn't exist"
                base.localAvatar.guiMgr.guildPage.displayRedeemErrorMessage(OTPLocalizer.GuildRedeemErrorInvalidToken)
            elif guildName == '***ERROR - GUILD FULL***':
                base.localAvatar.guiMgr.guildPage.displayRedeemErrorMessage(OTPLocalizer.GuildRedeemErrorGuildFull)
            else:
                # print "You have joined guild %s" % guildName
                base.localAvatar.guiMgr.guildPage.displayRedeemConfirmMessage(guildName)

    def recvTokenRedeemedByPlayerMessage(self, redeemerName):
        # Display a message in the message stack, indicating that a
        # guild code that a player issued has been redeeemed by the name passed
        # in the string redeemerName
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.notifyTokenGeneratorOfRedeem(redeemerName)

    def recvPermToken(self, token):
        # Response to a request to get the perm invite token for this avatar,
        # should they have one.
        # token will either be the token string 'ABCD1234',
        # or will be '0' (indicating that the avatar does not have a perm token)

        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            if token == '0':
                base.localAvatar.guiMgr.guildPage.receivePermTokenValue(None)
            else:
                base.localAvatar.guiMgr.guildPage.receivePermTokenValue(token)
            
    def requestEmailNotificationPref(self):
        # Request that the guild email notification prefs are sent down
        # to the client

        self.sendUpdate('sendRequestEmailNotificationPref', [])

    def respondEmailNotificationPref(self, notify, emailAddress):
        # Response from the UD, in reference to a request for
        # email notification preferences

        self.emailNotification = notify
        if emailAddress == 'None':
            self.emailNotificationAddress = None
        else:
            self.emailNotificationAddress = emailAddress

    def getEmailNotificationPref(self):
        # Return the email notification prefs

        return [self.emailNotification, self.emailNotificationAddress]

    def requestEmailNotificationPrefUpdate(self, notify, emailAddress):
        # Request that the UD to change the email notification prefs
        # for the avatar.
        # Notify == 0 : Off
        # Notify == 1 : On

        self.sendUpdate("sendEmailNotificationPrefUpdate", [notify, emailAddress])
        # Now set the local client side variables for the notify data

        self.emailNotification = notify
        if emailAddress == 'None':
            self.emailNotificationAddress = None
        else:
            self.emailNotificationAddress = emailAddress

    def recvNonPermTokenCount(self, tCount):
        # Receive count of Non Perm tokens from the UD
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.guildPage.receiveNonPermTokenCount(tCount)


    # teleport support
    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def d_reflectTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        self.sendUpdate('reflectTeleportQuery', [sendToId, localBandMgrId, localBandId, localGuildId, localShardId])

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def teleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        if self.cr.teleportMgr:
            self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId)

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def d_reflectTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId):
        self.sendUpdate('reflectTeleportResponse', [sendToId, available, shardId, instanceDoId, areaDoId])

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def teleportResponse(self, responderId, available,
                         shardId, instanceDoId, areaDoId):
        if self.cr.teleportMgr:
            self.cr.teleportMgr.handleAvatarTeleportResponse(responderId, available, 
                                                             shardId, instanceDoId, areaDoId,
                                                             )

    @report(types = ['args'], dConfigParam = 'guildmgr')
    def handleLogout(self, *args, **kw):
        self.cr.removeAIInterest(AIInterestHandles.PIRATES_GUILD)
