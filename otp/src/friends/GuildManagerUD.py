from itertools import izip
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.distributed import OtpDoGlobals
from otp.ai import AIMsgTypes
from otp.uberdog.UberDogUtil import ManagedAsyncRequest
from otp.uberdog.RejectCode import RejectCode
from otp.ai import AIInterestHandles

from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.friends.FriendInfo import FriendInfo
from otp.friends.GuildDB import NOACTION_FLAG,REVIEW_FLAG,DENY_FLAG,APPROVE_FLAG,ALLDONE_FLAG
from otp.otpbase import OTPLocalizer

import time
import string

#--------------------------------------------------

ONLINE = 1
OFFLINE = 0

GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

MAX_MEMBERS = 500

class GuildManagerUD(DistributedObjectGlobalUD):
    """
    The Avatar Friends Manager is a global object.
    This object handles client requests on avatar-level (as opposed to player-level) friends.

    See Also:
        "otp/src/friends/GuildManager.py"
        "otp/src/friends/PlayerFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('GuildManagerUD')

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)
        self.debugAvId = 0
        
        self.DBuser = uber.config.GetString("mysql-user","ud_rw")
        self.DBpasswd = uber.config.GetString("mysql-passwd","r3adwr1te")

        self.DBhost = uber.config.GetString("guild-db-host","localhost")
        self.DBport = uber.config.GetInt("guild-db-port",3306)
        self.DBname = uber.config.GetString("guild-db-name","guilds")

        from otp.friends.GuildDB import GuildDB
        self.db = GuildDB(host=self.DBhost,
                          port=self.DBport,
                          user=self.DBuser,
                          passwd=self.DBpasswd,
                          dbname=self.DBname)

        self.asyncRequests = {}

        # Maintain a big list of Avatar Names to give out member info with
        self.isAvatarOnline = {}
        self.avatarName = {}
        self.pendingSends = {}
        
        self.avatarId2Guild = {}
        self.avatarId2Rank = {}

        self.avatarId2Invite = {}

        self.avatarId2BandId = {}

        # Maintain information for Token Requests (Generate)

        self.nextTokenRequestId = 0
        self.requestId2AvatarId = {}

        # Maintain information for Token Requests (Redeem)

        self.nextRedeemTokenRequestId = 0
        self.redeemTokenRequestId2AvatarId = {}
        
        # This next one is to hold the time stamp of an avatar's last
        # token redeem request. Format is {avatarId : time)
        # Where time is the epoch; stored in 1 second precision

        self.redeemTokenTimeStamps = {}

        self.accept("avatarOnline", self.avatarOnline)
        self.accept("avatarOffline", self.avatarOffline)

        self.funcTally = {}

        taskMgr.doMethodLater(60.0, self.logFuncTally, "logFuncTally")


    def tallyFunction(self,funcName):
        if funcName not in self.funcTally:
            self.funcTally[funcName] = 1
            funcs = self.funcTally.keys()
            funcs.sort()
            self.notify.info("funcs tallied: %s" % funcs)
        else:
            self.funcTally[funcName] += 1

    def logFuncTally(self,task):
        funcs = self.funcTally.keys()
        funcs.sort()
        str = ["%s" % self.funcTally[f] for f in funcs]
        str = string.join(str," ")
        self.notify.info("funcTally: %s" % str)
        return task.again

    
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
        for i in self.asyncRequests.values():
            i.delete()
        DistributedObjectGlobalUD.delete(self)

    def sendUpdateToGuildChannel(self, guildId, field, parameters):
        if guildId:
            self.sendUpdateToChannel((self.doId<<32)+guildId,
                                     field,
                                     parameters)

            
    def sendUpdateToGuildChannelWithSender(self, guildId, field, parameters):
        messageSender = self.air.getMsgSender()
        if guildId:
            channelId = (self.doId<<32)+guildId
            self.air.sendUpdateToChannelFrom(self, channelId, field, messageSender, parameters)
            

    # Functions called by the client
    def acceptInvite(self):
        self.tallyFunction("acceptInvite")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:
            
            guildId,inviterId = self.avatarId2Invite.pop(avatarId,(0,0))

            if guildId > 0:
                self._addMember(guildId, avatarId)
                self.air.writeServerEvent('acceptGuildInvite', avatarId, '%s|%s' % (inviterId, guildId))
                self.sendUpdateToAvatarId(
                    inviterId, 'guildAcceptInvite', [avatarId])

    def declineInvite(self):
        self.tallyFunction("declineInvite")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:
            
            guildId,inviterId = self.avatarId2Invite.pop(avatarId,(0,0))

            if guildId > 0:
                self.air.writeServerEvent('declineGuildInvite', avatarId, '%s|%s' % (inviterId, guildId))
                self.sendUpdateToAvatarId(
                    inviterId, 'guildRejectInvite', [avatarId, RejectCode.NO_GUILD])

    def createGuild(self):
        self.tallyFunction("createGuild")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:
            
            self.air.writeServerEvent('createGuild', avatarId, '')
            # Add a new guild to the database
            self.db.createGuild(avatarId)
            self._sendStatus(avatarId)

    def _sendFinishedList(self, player):
        """
        Removes the associated pendingSend from the dictionary
        and sends the info to 'player'.
        """
        if self.debugAvId == player:
            assert self.notify.warning('_sendFinishedList(%s)' % (player,))

        guildInfo = self.pendingSends.pop(player, None)
        if guildInfo:
            if 0:
                # alternate coolness
                guildmates, haveData = izip(*guildInfo)
            else:
                guildmates = [x[0] for x in guildInfo]
                haveData = [x[1] for x in guildInfo]

            if __dev__:
                assert False not in haveData
                pass
            if self.debugAvId == player:
                assert self.notify.warning('packaging info...')
            packagedInfo = []
            for guildId,avid,rank in guildmates: 
                # Bundle up all the info into send format
                bandId = self.avatarId2BandId.get(avid)
                if not bandId:
                    bandId = (0, 0)
                packagedInfo.append( ( avid,
                                       self.avatarName.get(avid, 'Unknown'),
                                       rank,
                                       self.isAvatarOnline.get(avid, OFFLINE),
                                       bandId[0],
                                       bandId[1],
                                       )
                                     )
            if self.debugAvId == player:
                for item in packagedInfo:
                    assert self.notify.warning('%s' % (item,))
            # Send information to player
            for member in packagedInfo:
                self.sendUpdateToAvatarId(player,"receiveMember",[member])
            self.sendUpdateToAvatarId(player,"receiveMembersDone",[])
                
    def _sendFinishedLists(self, arrivingPlayer):
        """
        Upon receiving a player's data, look to see if anyone
        was waiting for it.  If so, update that status. If it
        was the last one needed in any pending list, send out
        that list.
        """
        finishedLists = []
        for player,guildInfo in self.pendingSends.iteritems():
            send = True
            for infoItem in guildInfo:
                [(guildId,avId,rank), haveData] = infoItem
                infoItem[1] |= (avId == arrivingPlayer)
                send &= infoItem[1]

                if self.debugAvId == player and \
                   avId == arrivingPlayer:
                    assert self.notify.warning('received info for %s' % (avId,))
            if send:
                if self.debugAvId == player:
                    assert self.notify.warning('finished list, now sending')
                finishedLists.append(player)

        for player in finishedLists:
            self._sendFinishedList(player)

        
    def memberInfo(self, avatarId, context, info):
        """
        We have received our data request from the avatar state
        server. Use it to update our guild member info and then
        send out any pending member lists that this info completes.
        """
        self.tallyFunction("memberInfo")

        self.ignore("doFieldQueryFailed-%s"%context)
        taskMgr.remove("memberInfoFailure-%s"%context)

        name = info['setName'][0]
        bandId = info['setBandId']
        self.avatarName[avatarId] = name
        self.avatarId2BandId[avatarId] = bandId 
        # Initialize this person in isAvatarOnline array
        if not self.isAvatarOnline.setdefault(avatarId, OFFLINE) == OFFLINE:
            # They're online, this must have been the initial name request
            # Tell my guildmates I'm online
            gId = self._getGuildId(avatarId)
            self.sendUpdateToGuildChannel(gId,"recvAvatarOnline",[avatarId, name, bandId[0], bandId[1]])

        self._sendFinishedLists(avatarId)


    def memberInfoFailure(self, avatarId, context):
        """
        This avatarId gave no result from the gamedb.
        Bad avatar.  Get it out of the guild DB and clean up.
        """
        gId = self._getGuildId(avatarId)
        rank = self._getGuildId(avatarId)

        self.notify.warning("Avatar %s not found in gamedb.  Removing from guild %s." % (avatarId, gId))
        self.air.writeServerEvent('removeBrokenGuildMember', avatarId, str(gId))

        self.ignore("doFieldResponse-%s"%context)
        self.ignore("doFieldQueryFailed-%s"%context)
        taskMgr.remove("memberInfoFailure-%s"%context)

        self.db.removeMember(avatarId, gId, rank)

        for recipientId in self.pendingSends.keys():
            info = self.pendingSends.get(recipientId,[])
            newInfo = []
            rep = False
            for [(guildId,memberId,memberRank), haveData] in info:
                if memberId != avatarId:
                    newInfo.append([(guildId,memberId,memberRank), haveData])
                    rep = True
            if rep:
                self.pendingSends[recipientId] = newInfo
                self._sendFinishedLists(0)


    def memberList(self):
        self.tallyFunction("memberList")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId and (avatarId not in self.pendingSends):

            guildId = self._getGuildId(avatarId)

            guildfolk = self.db.getMembers(guildId)

            # queue us a member list send
            haveData = [(avId in self.avatarName) for guildId,avId,rank in guildfolk]

            self.pendingSends[avatarId] = [[x,y] for x,y in izip(guildfolk,haveData)]

            if False not in haveData:
                self._sendFinishedLists(avatarId)
            else:
                for guildmate, haveData in self.pendingSends[avatarId]:
                    if not haveData:
                        avId = guildmate[1]
                        self.requestMemberInfo(avId)
                        
    def requestMemberInfo(self, avId):
        self.tallyFunction("requestMemberInfo")
        context=self.air.allocateContext()
        dclassName="DistributedPlayerPirateUD"
        self.air.contextToClassName[context]=dclassName
        self.acceptOnce("doFieldResponse-%s"%context, self.memberInfo, [avId])
        self.acceptOnce("doFieldQueryFailed-%s"%context, self.memberInfoFailure, [avId])
        taskMgr.doMethodLater(30.0, self.memberInfoFailure, "memberInfoFailure-%s"%context, [avId, context])
        self.air.queryObjectFields(dclassName, ['setName', 'setBandId'], avId, context)

    def setWantName(self, newName):
        self.tallyFunction("setWantName")

        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:

            guildId = self._getGuildId(avatarId)

            # Only the GM can rename the guild
            if self._getGuildRank(avatarId) == GUILDRANK_GM:
                resultmsg = self.db.setWantName(guildId, newName)
                if (resultmsg == 2):
                    # Send a message to the creator that it was denied
                    self.sendUpdateToAvatarId(avatarId,"guildNameReject",[guildId])
            
    def avatarOnline(self, avatarId, avatarType):
        self.tallyFunction("avatarOnline")
        if avatarId:
            # Change status of this avatarId to show they are online
            self.isAvatarOnline[avatarId] = ONLINE
            
            # Also request a name for this avatar for use later
            self.requestMemberInfo(avatarId)
            
            self._sendStatus(avatarId)            

    @report(types = ['args'], dConfigParam = 'orphanedavatar')
    def avatarOffline(self, avatarId):
        self.tallyFunction("avatarOffline")
        # Change status of this avatarId to show they are offline
        self.isAvatarOnline[avatarId] = OFFLINE
        self.avatarId2BandId[avatarId] = (0,0)

        if self.avatarId2Invite.get(avatarId,None):
            self.avatarId2Invite.pop(avatarId,(0,0))

        # Unregister the client from the guild channel
        self.air.removeInterestFromConnection(avatarId,AIInterestHandles.PIRATES_GUILD)
        
        gId = self._getGuildId(avatarId)
        self.sendUpdateToGuildChannel(gId, "recvAvatarOffline",
                                      [avatarId,self.avatarName.get(avatarId,"Unknown")])
        
    def updateRep(self, avatarId, rep):
        if avatarId in self.avatarName:
            self.updateLeaderboardRep(avatarId, self.avatarName.get(avatarId, 'Unknown'), rep)

    def _addMember(self, guildId, avatarId):
        self.tallyFunction("_addMember")
        self.air.writeServerEvent('addGuildMember', avatarId, '%s' % (guildId))

        # Add a new normal member to guild
        self.db.addMember(guildId, avatarId, 1)

    
        self._sendStatus(avatarId)
        name = self.avatarName.get(avatarId)
        if not name:
            name = OTPLocalizer.GuildNewMember
        rank = self.avatarId2Rank.get(avatarId)
        if not rank:
            rank = 1
        isOnline = self.isAvatarOnline.get(avatarId, OFFLINE)
        bandManagerId, bandId = self.avatarId2BandId.get(avatarId, (0,0))
        self.sendUpdateToGuildChannel(guildId, 'recvMemberAdded',
                                      [(avatarId, name, rank, isOnline, bandManagerId, bandId)])

    def removeMember(self, avatarId):
        self.tallyFunction("removeMember")
        senderId = self.air.getAvatarIdFromSender()
        if senderId:

            senderGuild = self._getGuildId(senderId)
            victimGuild = self._getGuildId(avatarId)
            senderRank = self._getGuildRank(senderId)
            victimRank = self._getGuildRank(avatarId)

            # Removing self from guild
            if senderId == avatarId or \
               (senderGuild == victimGuild) and senderRank > victimRank:
                self.air.writeServerEvent('removeGuildMember', avatarId, 'by %s from %s' % (senderId, victimGuild))
                self.db.removeMember(avatarId, victimGuild, victimRank)
                self.sendUpdateToGuildChannel(victimGuild, 'recvMemberRemoved',
                                              [avatarId])
            # Someone's guild/rank is out of synch or we have a hacker
            else:
                assert self.notify.warning("%d (guild %d rank %d) was incapable of removing %d (guild %d rank %d) from guild." % \
                                    (senderId,senderGuild,senderRank,avatarId,victimGuild,victimRank))

            self._sendStatus(avatarId)

    def changeRank(self, avatarId, rank):
        self.tallyFunction("changeRank")
        senderId = self.air.getAvatarIdFromSender()
        if senderId:

            senderGuild = self._getGuildId(senderId)
            senderRank = self._getGuildRank(senderId)
            victimGuild = self._getGuildId(avatarId)

            if rank < GUILDRANK_MEMBER or rank > GUILDRANK_GM:
                assert self.notify.warning("Invalid guild rank %d sent by avatar %d in changeRank request" % (rank,senderId))
                return

            if senderGuild != victimGuild:
                assert self.notify.warning("Guild mismatch in changeRank request from %d for %d." % (senderId,avatarId))
                return

            if senderRank != GUILDRANK_GM:
                assert self.notify.warning("%d tried to changeRank but wasn't allowed (rank=%d)!" % (senderId,senderRank))
                return

            self.air.writeServerEvent('changeGuildRank', avatarId, '%s by %s' % (rank, senderId))
            # Change guild member rank
            self.db.changeRank(avatarId, rank)
            self.sendUpdateToGuildChannel(victimGuild, 'recvMemberUpdateRank', [avatarId, rank])
            self._sendStatus(avatarId)

    def _sendStatus(self,avatarId):
        self.tallyFunction("_sendStatus")
        if avatarId and \
           self.isAvatarOnline.get(avatarId) == ONLINE:
            # Request a guild status update for given avatar
            guildId, name, rank, change = self.getStatus(avatarId)

            # Tell this player's guild manager their guild status
            self.sendGuildStatusUpdate(avatarId, guildId, name, rank)

            # Update the player's avatar with this guild info
            self.sendGuildMemberUpdate(avatarId, guildId, name)

            # If the guild's name has been approved or denied, notify
            # the GM that his "want name" has been processed
            self.checkForNameUpdate(avatarId, guildId, name, rank, change)
            
            # Subscribe or unsubscribe the player from guild chat
            self.updateGuildChatInterest(avatarId, guildId, guildId != 0)

            
    def getStatus(self, avatarId):
        self.tallyFunction("getStatus")
        # Request a guild status update for given avatar
        guildId, name, rank, change = self.db.queryStatus(avatarId)
        self.avatarId2Guild[avatarId] = guildId
        self.avatarId2Rank[avatarId] = rank
        return guildId, name, rank, change

    def sendGuildStatusUpdate(self, avatarId, guildId, name, rank):
        # Tell this player's guild manager their guild status
        self.sendUpdateToAvatarId(avatarId,"guildStatusUpdate",[guildId, name, rank])

    def sendGuildMemberUpdate(self, avatarId, guildId, name):
        # Update the player's avatar with this guild info
        self.air.sendUpdateToDoId("DistributedPlayerPirate", "setGuildId", avatarId, [guildId])
        self.air.sendUpdateToDoId("DistributedPlayerPirate", "setGuildName", avatarId, [name])

    def checkForNameUpdate(self,avatarId, guildId, name, rank, change):
        if (rank == GUILDRANK_GM and change != NOACTION_FLAG):
            # Inform guild leader about name changes
            self.sendUpdateToAvatarId(avatarId, "guildNameChange", [name, change])
            if (change == DENY_FLAG):
                # Name Denied, set back to noaction flag
                self.db.nameProcessed(guildId, NOACTION_FLAG)
            elif (change == APPROVE_FLAG):
                # Name approved, set to all done flag
                self.db.nameProcessed(guildId, ALLDONE_FLAG)

    def updateGuildChatInterest(self, avatarId, guildId, allow):
        if guildId and allow:
            self.air.addInterestToConnection(avatarId,
                                             AIInterestHandles.PIRATES_GUILD,
                                             0,
                                             self.doId,
                                             guildId)
        else:
            self.air.removeInterestFromConnection(avatarId,AIInterestHandles.PIRATES_GUILD)
            
    def statusRequest(self):
        self.tallyFunction("statusRequest")
        # Request a guild status update for the sending avatar
        self._sendStatus(self.air.getAvatarIdFromSender())
        assert False
        
    def requestInvite(self, otherAvatarId):
        self.tallyFunction("requestInvite")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:

            name = self.avatarName.get(avatarId,"Some pirate")
            self.air.writeServerEvent('requestGuildInvite', avatarId, '%s|%s' % (otherAvatarId, name))

            guildid, guildname, guildrank, change = self.db.queryStatus(avatarId)
            print "DEBUG, query came back: ", guildid, " ", guildname
            otherguild, othername, otherrank, otherchange = self.db.queryStatus(otherAvatarId)

            if guildrank < GUILDRANK_OFFICER:
                assert self.notify.warning("%d tried to do a guild invite but was rank %d!" % (avatarId,guildrank))
                return

            # Make sure guild is not overly full
            count = self.db.memberCount(guildid)
            if (count >= MAX_MEMBERS):
                self.sendUpdateToAvatarId(
                    avatarId, 'guildRejectInvite', [otherAvatarId, RejectCode.GUILD_FULL])
                return

            # Make sure not already in guild or invite not already outstanding
            if (otherguild > 0):
                self.sendUpdateToAvatarId(
                    avatarId, 'guildRejectInvite', [otherAvatarId, RejectCode.ALREADY_IN_GUILD])
            elif self.avatarId2Invite.get(otherAvatarId,None):
                self.sendUpdateToAvatarId(
                    avatarId, 'guildRejectInvite', [otherAvatarId, RejectCode.BUSY])
            else:
                self.avatarId2Invite[otherAvatarId] = (guildid,avatarId)
                # Inform the other player that they have been invited
                self.sendUpdateToAvatarId(otherAvatarId, "invitationFrom", [avatarId,name,guildid,guildname])

    def updateLeaderboardRep(self, avatarId, name, rep):
        #print "updateLeaderboardRep: ", avatarId, ", ", name, ", ", rep
        # using the notifier now
        self.notify.info("updateLeaderboardRep: %d, %s, %d" % (avatarId,name,rep))
        self.air.setLeaderboardValue('reputation', avatarId, name, rep, self.getDoId())

    def requestLeaderboardTopTen(self):
        self.tallyFunction("requestLeaderboardTopTen")
        self.sendToId = self.air.getAvatarIdFromSender()
        if self.sendToId:

            dcfile = self.air.getDcFile()
            dclass = dcfile.getClassByName('LeaderBoard')
            dg = dclass.aiFormatUpdate('getTopTenRespondTo',
                               OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                               OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                               self.getDoId(),
                               ["reputation", self.getDoId()])
            self.air.send(dg)

    def testThis(self, args):
        print "DEBUG: sending setValue and getValuesRespondTo"

        dcfile = self.air.getDcFile()
        dclass = dcfile.getClassByName('LeaderBoard')
        dg = dclass.aiFormatUpdate('setValue',
                           OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                           OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                           self.getDoId(),
                           [["guildtest"], 1, "name", 23])
        self.air.send(dg)

        dg = dclass.aiFormatUpdate('getValuesRespondTo',
                           OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                           OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                           self.getDoId(),
                           ["guildtest", [1], self.getDoId()])
        self.air.send(dg)

    def getValuesResponce(self, contest, stuff):
        # This should automatically get called in response by the dclass object
        # No additional catch/subscribe required
        print "DEBUG: GuildManagerUD:getValuesResponce"
        import pdb; pdb.set_trace();

    def getTopTenResponce(self, contest, stuff):
        # This should automatically get called in response by the dclass object
        # No additional catch/subscribe required
        self.sendUpdateToAvatarId(self.sendToId,"leaderboardTopTen", [stuff])
        

    def setTalkGroup(self,fromAV, fromAC, avatarName, chat, mods, flags):
        self.tallyFunction("setTalkGroup")

        #print("Guild Manager - sendTalkGroup")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:
    
            #self.air.writeServerEvent('sendChat', avatarId, '%s' % (chat))
    
            gId = self._getGuildId(avatarId)
            #self.sendUpdateToGuildChannel(gId, "recvChat",[avatarId,msgText,chatFlags,senderDISLid])
            self.sendUpdateToGuildChannelWithSender(gId, "setTalkGroup", [fromAV, fromAC, avatarName, chat, mods, flags])

    def sendWLChat(self,msgText,chatFlags,senderDISLid):
        self.tallyFunction("sendWLChat")
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:

            self.air.writeServerEvent('sendWLChat', avatarId, '%s' % (msgText))
            
            gId = self._getGuildId(avatarId)
            self.sendUpdateToGuildChannel(gId, "recvWLChat", [avatarId,msgText,chatFlags,senderDISLid])

    def sendSC(self,msgIndex):
        self.tallyFunction("sendSC")
        #print "GuildManagerUD.sendSC() called"
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:

            self.air.writeServerEvent('sendSC', avatarId, '%d' % (msgIndex))
            
            gId = self._getGuildId(avatarId)
            self.sendUpdateToGuildChannel(gId, "recvSC", [avatarId,msgIndex])

    def sendSCQuest(self,questInt,msgType,taskNum):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId:

            self.air.writeServerEvent('sendSCQuest', avatarId, '%d' % (taskNum))

            gId = self._getGuildId(avatarId)
            self.sendUpdateToGuildChannel(gId, "recvSCQuest", [avatarId,questInt,msgType,taskNum])
        
    def _getGuildId(self,avatarId):
        if avatarId in self.avatarId2Guild:
            return self.avatarId2Guild[avatarId]
        else:
            guildId, name, rank, change = self.getStatus(avatarId)
            return guildId
            
    def _getGuildRank(self,avatarId):
        if avatarId in self.avatarId2Rank:
            return self.avatarId2Rank[avatarId]
        else:
            guildId, name, rank, change = self.getStatus(avatarId)
            return rank

    def sendTokenRequest(self):
        self.tallyFunction("sendTokenRequest")
        requestId = self.nextTokenRequestId + 1
        self.nextTokenRequestId += 1
        self.requestId2AvatarId[requestId] = self.air.getAvatarIdFromSender()
        # Lets get the guildId for this avatar
        guildId, name, rank, change = self.db.queryStatus(self.air.getAvatarIdFromSender())

        if guildId:
            token = self.db.getFriendToken(guildId, self.requestId2AvatarId[requestId])
            # OK, now that we have the token, lets send it back to the client
            self.recvTokenGenerated(requestId, token)
            self.air.writeServerEvent('sendTokenRequest', self.requestId2AvatarId[requestId], '%s|%d|%d' % (token, guildId, rank))
    
    def recvTokenGenerated(self,requestId, tokenValue):
        # Before responding, let also figure out if the avatar has a
        # existing perm code
        perm = self.db.checkForUnlimitedUseToken(self.requestId2AvatarId[requestId])
        # if perm == None, then make preExistPerm = 0
        # if perm != None, make preExistPerm = 1
        if perm == None:
            preExistPerm = 0
        else:
            preExistPerm = 1
        self.sendUpdateToAvatarId(self.requestId2AvatarId[requestId],
                                  'recvTokenInviteValue',
                                  [tokenValue, preExistPerm])
        # print "Token for request %s: %s" % (requestId,tokenValue)
        self.air.writeServerEvent('recvTokenGenerated', self.requestId2AvatarId[requestId], '%s' % (tokenValue))

    def sendTokenForJoinRequest(self, token, name):
        self.tallyFunction("sendTokenForJoinRequest")

        avatarId = self.air.getAvatarIdFromSender()

        requestId = self.nextRedeemTokenRequestId + 1
        self.nextRedeemTokenRequestId += 1
        self.redeemTokenRequestId2AvatarId[requestId] = avatarId
        
        # Security check. Lets keep track of how quickly users are trying to
        # redeem guild tokens. If someone tries to redeem (repeatedly) without
        # success, (more than two requests, during a two second time span);
        # drop the request
        if avatarId in self.redeemTokenTimeStamps:
            # They have an entry, take the value (epoch) from the dict
            lastTry = self.redeemTokenTimeStamps[self.redeemTokenRequestId2AvatarId[requestId]]
            if lastTry >= int(time.time()) - 2:
                
                # They are trying to redeem too fast
                # update their time stamp in self.redeemTokenTimeStamps
                # and then return

                self.redeemTokenTimeStamps[self.redeemTokenRequestId2AvatarId[requestId]] = int(time.time())
                self.air.writeServerEvent('tokenRedemptionTooFast', self.redeemTokenRequestId2AvatarId[requestId], '%s|%s|' % (self.redeemTokenTimeStamps[self.redeemTokenRequestId2AvatarId[requestId]], int(time.time())))
                return
        else:
            self.redeemTokenTimeStamps[avatarId] = int(time.time())

        # If redeem is sucessful, we'll remove the stamp entry
        # in redeemTokenTimeStamps
        
        try:
            results = self.db.redeemToken(token, avatarId)
        except Exception,e:
            if e.args[0] == "INVALID_TOKEN":
                guildName = '***ERROR - GUILD CODE INVALID***'
                self.sendTokenRedeemMessage(requestId, guildName)
                self.air.writeServerEvent('sendTokenForJoinRequest', avatarId, '%s|0' % (token))
                # Timestamp their request; in case they are trting to redeem
                # to fast.
                self.redeemTokenTimeStamps[avatarId] = int(time.time())
                return
            elif e.args[0] == "GUILD_FULL":
                guildName = '***ERROR - GUILD FULL***'
                self.sendTokenRedeemMessage(requestId, guildName)
                self.air.writeServerEvent('sendTokenForJoinRequest', avatarId, '%s|0' % (token))
                # Timestamp their request; in case they are trting to redeem
                # to fast.
                self.redeemTokenTimeStamps[avatarId] = int(time.time())
                return
            else:
                raise e
        
        guildId = results[0]
        creatorAvId = results[1]
        guildName = str(self.db.getName(guildId))
        if guildName == '0':
            guildName = "Pirate Guild %s" % guildId
        # print 'About to send message with %d, %s' % (requestId, guildName)
        self.sendTokenRedeemMessage(requestId, guildName)
        self.sendTokenRedeemedToTokenCreator(creatorAvId, name)

        self._sendStatus(self.air.getAvatarIdFromSender())
        name = self.avatarName.get(avatarId)
        if not name:
            name = OTPLocalizer.GuildNewMember
        rank = self.avatarId2Rank.get(avatarId)
        if not rank:
            rank = 1
        isOnline = self.isAvatarOnline.get(avatarId, OFFLINE)
        bandManagerId, bandId = self.avatarId2BandId.get(avatarId, (0,0))
        self.sendUpdateToGuildChannel(guildId, 'recvMemberAdded',
                                      [(avatarId, name, rank, isOnline, bandManagerId, bandId)])

        self.air.writeServerEvent('sendTokenForJoinRequest', self.redeemTokenRequestId2AvatarId[requestId], '%s|1' % (token))
        # Now, remove the timestamp from self.redeemTokenTimeStamps
        del self.redeemTokenTimeStamps[self.redeemTokenRequestId2AvatarId[requestId]]

    def sendTokenRedeemMessage(self, requestId, guildName):
        # print 'guildName passed is: ' + str(guildName)
        self.sendUpdateToAvatarId(self.redeemTokenRequestId2AvatarId[requestId],
                                  'recvTokenRedeemMessage',
                                  [guildName])
        # print "recvTokenRedeemMessage sent ID: %d : Gname %s" % (requestId, guildName)

    def sendTokenRedeemedToTokenCreator(self, avIdOfCreator, redeemerName):
        # Send a message to avIdOfCreator, letting them know that
        # redeemerName has redeemed their guild token
        self.sendUpdateToAvatarId(avIdOfCreator, 'recvTokenRedeemedByPlayerMessage', [redeemerName])

    def sendTokenRValue(self, tokenString, rValue):
        # This is called from the client, when an avatar wishes to have a token
        # flagged as multi-use. (The default behavor is one time use)
        # Two values are passed in:
        # tokenString = The Token they wish to modify
        # rValue = The redeem value they wish to apply to the token passed
        # rValue can be as follows...
        # if (rValue > 0) = Code can be redeemed rValue number of times,
        # everytime it is redeemed, the rValue in the DB will need to be decremented.
        # if (rValue == -1) = Code can be redeemed an unlimited number of times
        # if (rValue == -2) = Code has been suspended, but is still assigned;
        # it can be reactivated at a later time.

        avatarId = self.air.getAvatarIdFromSender()
        self.db.changeTokenRValue(avatarId, tokenString, rValue)
        self.notify.debug('Requesting Guild Token DB update for %s, updating rValue: %s, for Token %s' % (avatarId, rValue, tokenString))
        self.air.writeServerEvent('Update_Guild_Token_RValue', avatarId, '%s|%s|' % (tokenString, rValue))

    def sendPermToken(self):
        # Called from the client. When called, this will send back the
        # perm token that the avatar has registered on the system.
        # If none, then return '0'

        avatarId = self.air.getAvatarIdFromSender()
        token = self.db.checkForUnlimitedUseToken(avatarId)
        if token == None:
            token = '0'
        self.sendUpdateToAvatarId(avatarId, 'recvPermToken', [token])

    def sendNonPermTokenCount(self):
        # Called from the client. When called, it will send back a total count
        # of non-perm tokens

        avatarId = self.air.getAvatarIdFromSender()
        tCount = self.db.returnLimitedUseTokens(avatarId)
        self.sendUpdateToAvatarId(avatarId, 'recvNonPermTokenCount', [tCount])

    def sendClearTokens(self, type):
        # Called from the client. A request to clear one of two types of tokens,
        # Clear all one-time and limited multiuse codes, or clear perm code
        # type = 0: Clear onetime use and limited multi-use codes
        # type = 1: Clear perm token code

        avatarId = self.air.getAvatarIdFromSender()
        if type == 0:
            self.db.clearLimitedUseTokens(avatarId)
            return
        if type == 1:
            self.db.clearPermUseTokens(avatarId)
            return

    def sendRequestEmailNotificationPref(self):
        # Called from the client. Request and avatar's email notification prefs

        avatarId = self.air.getAvatarIdFromSender()

        prefs = self.db.getEmailNotificationPref(avatarId)

        # Now that we have the prefs, respond back to the client
        # But before we send, lets check the email address value in prefs.
        # If second value is None, we should probably convert it to a string

        notify = prefs[0]
        emailAddress = prefs[1]
        if emailAddress == None:
            emailAddress = 'None'

        self.sendUpdateToAvatarId(avatarId, 'respondEmailNotificationPref', [notify, emailAddress])

    def sendEmailNotificationPrefUpdate(self, notify, emailAddress):
        # Update the notification prefs for the sending avId

        avatarId = self.air.getAvatarIdFromSender()
        self.db.updateNotificationPref(avatarId, notify, emailAddress)


    def sendAvatarBandId(self, avatarId, bandManagerId, bandId):
        self.tallyFunction("sendAvatarBandId")
        self.avatarId2BandId[avatarId] = (bandManagerId, bandId)
        guildId = self._getGuildId(avatarId)
        self.sendUpdateToGuildChannel(guildId, 'recvMemberUpdateBandId', [avatarId, bandManagerId, bandId])


    """
    # for testing the leaderboard
    # this overwrites getTopTenResponce defined above, only uncomment this for testing

    # >>> uber.air.guildManager.getLeaderboardTopTen('pvpBattle')

    def getLeaderboardTopTen(self, category):
        dcfile = self.air.getDcFile()
        dclass = dcfile.getClassByName('LeaderBoard')
        dg = dclass.aiFormatUpdate('getTopTenRespondTo',
                                   OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                                   OtpDoGlobals.OTP_DO_ID_LEADERBOARD_MANAGER,
                                   self.getDoId(),
                                   [category, self.getDoId()])
        self.air.send(dg)

    def getTopTenResponce(self, category, info):
        print 'TOP 10 RESPONSE (%s): %s' % (category, info)

    """

    def setDebugAvid(self, avId):
        if uber.config.GetBool("guild-manager-ud-debug",0):
            self.debugAvId = avId


    # teleport support
    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def reflectTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        self.tallyFunction("reflectTeleportQuery")
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(sendToId, 'teleportQuery', [avId, localBandMgrId, localBandId, localGuildId, localShardId])

    @report(types = ['deltaStamp', 'args'], dConfigParam = 'teleport')
    def reflectTeleportResponse(self, sendToId, available, shardId, instanceDoId, areaDoId):
        self.tallyFunction("reflectTeleportResponse")
        avId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(sendToId, 'teleportResponse', [avId, available, shardId, instanceDoId, areaDoId])

    def sendMsgToDinghyAI(self, doId, channel, fieldName, args):
        self.tallyFunction("sendMsgToDinghyAI")
        # Send the Friends list back to the AI that called it
        dcfile = self.air.getDcFile()
        dclass = dcfile.getClassByName('DistributedDinghy')
        # param1: field name to be called
        # param2: doId of target object
        # param3: channel to send TO (other object must be listening to this channel)
        # param4: who sent the message
        # param5: arguments to be sent
        dg = dclass.aiFormatUpdate(fieldName,
                                   doId,
                                   channel,
                                   self.getDoId(),
                                   args)
        self.air.send(dg)

    def requestGuildMatesList(self, doId, channel, avId):
        self.tallyFunction("requestGuildMatesList")
        # Send the list of avatars who are in the same guild as avId

        guildId = self.avatarId2Guild.get(avId)
        if not guildId:
            return

        # Now that we have the guild ID, get the list of members
        guildMembers = self.db.getMembers(guildId)

        memberList = []
        for member in guildMembers:
            if member[1] != avId:
                memberList.append(member[1])

        self.sendMsgToDinghyAI(doId, channel, 'responseGuildMatesList', [avId, memberList])

    def updateAvatarName(self, avatarId, avatarName):
        self.tallyFunction("updateAvatarName")

        if avatarId in self.avatarName:
            self.avatarName[avatarId] = avatarName
            self._sendStatus(avatarId)

    def avatarDeleted(self, avatarId):
        self.tallyFunction("avatarDeleted")

        victimGuild = self._getGuildId(avatarId)
        victimRank = self._getGuildRank(avatarId)

        self.db.removeMember(avatarId, victimGuild, victimRank)
        self.sendUpdateToGuildChannel(victimGuild, 'recvMemberRemoved', [avatarId])
