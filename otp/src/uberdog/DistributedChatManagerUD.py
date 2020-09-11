"""
The Avatar Manager UD handles all chat accross all
districts.
"""

from otp.ai import AIMsgTypes
from otp.distributed import OtpDoGlobals

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

if __debug__:
    from direct.directnotify.DirectNotifyGlobal import directNotify
    notify = directNotify.newCategory('ChatManagerUD')

if uber.wantSwitchboard:
    from otp.switchboard.sbWedge import sbWedge
    from direct.task import Task

    class udWedge(sbWedge):
        def __init__(self,wedgeName,dcmUD):
            sbWedge.__init__(self,wedgeName)
            self.dcmUD = dcmUD
        def recvWhisper(self,recipientId,senderId,msgText):
            self.log("**Whisper from %d received for %d: %s"%(senderId,recipientId,msgText))
            if uber.GEMdemoWhisperRecipientDoid == 0:
                self.log.error("SB demo enabled but no recipient DOID specified!")
            self.dcmUD.sendWhisperFrom(uber.GEMdemoWhisperRecipientDoid,uber.GEMdemoWhisperRecipientDoid,msgText)

#-----------------------------------------------------------------------------

class DistributedChatManagerUD(DistributedObjectGlobalUD):
    """
    The Avatar Manager UD is a global object.

    See Also:
        "otp/src/guild/ChatManager.py"
        "otp/src/guild/ChatManagerAI.py"
        "otp/src/configfiles/otp.dc"
    """
    if __debug__:
        notify = notify

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)
        
        self.asyncRequests = {}
        self.isAccountOnline={}
        
        self.avatarLoction={}
        self.avatarCrew={}
        self.avatarGuild={}

        if uber.wantSwitchboard:
            self.sb = udWedge("pirates",self)

            def CheckWedge(task):
                self.sb.pyroDaemon.handleRequests(0)
                return Task.cont

            uber.taskMgr.add(CheckWedge,'checkwedge')
    
    def announceGenerate(self):
        assert self.notify.debugCall()
        self.accept("accountOnline", self.accountOnline, [])
        self.accept("accountOffline", self.accountOffline, [])
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
        self.asyncRequests={}
        DistributedObjectGlobalUD.delete(self)

    #----------------------------------
    
    def accountOnline(self, accountId):
        assert self.notify.debugCall()
        assert accountId
        self.air.writeServerEvent('accountOnline', accountId, '')
        if self.isAccountOnline.has_key(accountId):
            assert self.notify.debug(
                "\n\nWe got a duplicate account online notice %s"%(accountId,))
        if accountId and not self.isAccountOnline.has_key(accountId):
            self.isAccountOnline[accountId]=None
            ## self.asyncRequests[accountId]=self.accountOnlineAsyncRequest(accountId)

    def accountOffline(self, accountId):
        assert self.notify.debugCall()
        self.air.writeServerEvent('accountOffline', accountId, '')
        i = self.asyncRequests.pop(accountId, None)
        if i is not None:
            i.delete()
        return self.isAccountOnline.pop(accountId, None)
    
    def checkAvatarId(self, avatarId):
        if not avatarId:
            # SUSPICIOUS
            self.notify.warning("Bogus avatarId (%s)"%avatarId)
        ## elif not self.isAvatarOnline.has_key(avatarId):
            ## # SUSPICIOUS
            ## self.notify.warning(
                ## "Got a request from an avatar (%s) that is not online"%
                ## accountId)
        elif self.asyncRequests.has_key(avatarId):
            # The timeout on the client might be too low or we may be being
            # attacked.
            self.notify.warning(
                "Too many requests at once from avatar %s"%avatarId)
        else:
            return True
        return False

    #----------------------------------
    
    def sendAdminChat(self, message):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(
            AIMsgTypes.CHANNEL_CLIENT_BROADCAST, "adminChat", [0, message])

    def setAvatarLocation(self, avatarId, parentId, zoneId):
        sender = self.air.getSenderReturnChannel()
        assert self.notify.debugCall("sender:%s"%(sender,))
        self.avatarLocation[avatarId]=(parendId<<32)+zoneId
        
    def setAvatarCrew(self, avatarId, zoneId):
        sender = self.air.getSenderReturnChannel()
        assert self.notify.debugCall("sender:%s"%(sender,))
        self.avatarCrew[avatarId]=(
            OtpDoGlobals.OTP_DO_ID_PIRATES_CREW_MANAGER<<32)+zoneId
        
    def setAvatarGuild(self, avatarId, zoneId):
        sender = self.air.getSenderReturnChannel()
        assert self.notify.debugCall("sender:%s"%(sender,))
        self.avatarGuild[avatarId]=(
            OtpDoGlobals.OTP_DO_ID_PIRATES_GUILD_MANAGER<<32)+zoneId
        
  
    # Client to location (zone)
    def chatTo(self, message, chatFlags):
        accountId = self.air.getAccountIdFromSender()
        if not accountId:
            assert self.notify.debugCall("accountId:%s (zero!)"%(accountId,))
            return
        if not self.isAccountOnline.has_key(accountId):
            assert self.notify.debugCall("accountId:%s (not online!)"%(accountId,))
            return
        assert self.notify.debugCall("accountId:%s"%(accountId,))

        #IAN - bye bye buggy five lines
        #location=self.avatarLocation.get(accountId)
        #if location is not None:
        #    self.sendChatFrom(accountId, location, message)
        #else:
        #    assert self.notify.debug("Unknown location for %s"%(accountId,))

        if uber.wantSwitchboardHacks:
            print "DistributedChatManagerUD->Switchboard: %s" % message
            self.sb.sendWhisper(1,2,message)

        ## chatPermissions=self.isAvatarOnline.get(accountId)
        ## if chatPermissions is not None:
            ## self.sendUpdateToChannel(
                ## chatPermissions.getLocation(), "chatTo", [message])
        
    def sendChatFrom(self, fromId, location, message, chatFlags=0):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(location, "chatFrom", [fromId, message])
        

    def speedChatTo(self, msgIndex):
        accountId = self.air.getAccountIdFromSender()
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        if self.checkAvatarId(avatarId):
            location=self.avatarLocation.get(accountId)
            if location is not None:
                self.sendSpeedChatFrom(accountId, location, message)
            else:
                assert self.notify.debug("Unknown location for %s"%(accountId,))
        
    def sendSpeedChatFrom(self, fromId, location, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(location, "speedChatFrom", [fromId, msgIndex])
        

    def speedChatCustomTo(self, msgIndex):
        accountId = self.air.getAccountIdFromSender()
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        if self.checkAvatarId(avatarId):
            location=self.avatarLocation.get(accountId)
            if location is not None:
                self.sendSpeedChatCustomFrom(accountId, location, message)
            else:
                assert self.notify.debug("Unknown location for %s"%(accountId,))
        
    def sendSpeedChatCustomFrom(self, fromId, location, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(location, "speedChatCustomFrom", [fromId, msgIndex])
        

    # Client to avatar (doId)
    def whisperTo(self, toId, message):
        accountId = self.air.getAccountIdFromSender()
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        if self.checkAvatarId(avatarId):
            chatPermissions=self.isAccountOnline.has_key(accountId)
            if chatPermissions is not None:
                self.sendWhisperFrom(accountId, toId, message)
            else:
                assert self.notify.debug("Unknown permissions for %s"%(accountId,))
        
    def sendWhisperFrom(self, fromId, toId, message):
        assert self.notify.debugCall()
        if uber.wantSwitchboardHacks:
            print "Sending whisper to %d: %s" % (toId,message)
            self.sendUpdateToAvatarId(toId, "whisperFrom", [fromId, message])
        else:
            self.sendUpdateToChannel(toId, "whisperFrom", [fromId, msgIndex])

        
    def whisperSCTo(self, toId, msgIndex):
        accountId = self.air.getAccountIdFromSender()
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        if self.checkAvatarId(avatarId):
            chatPermissions=self.isAccountOnline.has_key(accountId)
            if chatPermissions is not None:
                self.sendWhisperSCFrom(accountId, toId, message)
            else:
                assert self.notify.debug("Unknown permissions for %s"%(accountId,))
        
    def sendWhisperSCFrom(self, fromId, toId, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(toId, "whisperSCFrom", [fromId, msgIndex])
        
    def whisperSCCustomTo(self, toId, msgIndex):
        accountId = self.air.getAccountIdFromSender()
        if not accountId:
            assert self.notify.debugCall("accountId:%s (zero!)"%(accountId,))
            return
        if not self.isAccountOnline.has_key(accountId):
            assert self.notify.debugCall("accountId:%s (not online!)"%(accountId,))
            return
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        chatPermissions=self.isAccountOnline.has_key(accountId)
        if chatPermissions is not None:
            self.sendWhisperSCCustomFrom(accountId, toId, message)
        else:
            assert self.notify.debug("Unknown permissions for %s"%(accountId,))
        
    def sendWhisperSCCustomFrom(self, fromId, toId, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(toId, "whisperSCCustomFrom", [fromId, msgIndex])
        
    def whisperSCEmoteTo(self, toId, emoteId):
        accountId = self.air.getAccountIdFromSender()
        if not accountId:
            assert self.notify.debugCall("accountId:%s (zero!)"%(accountId,))
            return
        if not self.isAccountOnline.has_key(accountId):
            assert self.notify.debugCall("accountId:%s (not online!)"%(accountId,))
            return
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        chatPermissions=self.isAccountOnline.has_key(accountId)
        if chatPermissions is not None:
            self.sendWhisperSCEmoteFrom(accountId, toId, message)
        else:
            assert self.notify.debug("Unknown permissions for %s"%(accountId,))
        
    def sendWhisperSCEmoteFrom(self, fromId, toId, emoteId):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(toId, "whisperSCEmoteFrom", [fromId, emoteId])
        
    def whisperIgnored(self, fromId):
        assert self.notify.debugCall()
        

    # Client to crew (zone)
    def crewChatTo(self, message):
        accountId = self.air.getAccountIdFromSender()
        if not accountId:
            assert self.notify.debugCall("accountId:%s (zero!)"%(accountId,))
            return
        if not self.isAccountOnline.has_key(accountId):
            assert self.notify.debugCall("accountId:%s (not online!)"%(accountId,))
            return
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        crewChannel=self.avatarCrew.crew(accountId)
        if crewChannel is not None:
            self.sendCrewChatFrom(accountId, crewChannel, message)
        else:
            assert self.notify.debug("Unknown crew for %s"%(accountId,))
        
    def sendCrewChatFrom(self, fromId, toId, message):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(toId, "crewChatFrom", [fromId, emoteId])
        

    # Client to guild (zone)
    def guildChatTo(self, message):
        accountId = self.air.getAccountIdFromSender()
        if not accountId:
            assert self.notify.debugCall("accountId:%s (zero!)"%(accountId,))
            return
        if not self.isAccountOnline.has_key(accountId):
            assert self.notify.debugCall("accountId:%s (not online!)"%(accountId,))
            return
        assert self.notify.debugCall("accountId:%s"%(accountId,))
        guildChannel=self.avatarGuild.get(accountId)
        if guildChannel is not None:
            self.sendCrewChatFrom(accountId, guildChannel, message)
        else:
            assert self.notify.debug("Unknown guild for %s"%(accountId,))
        
    def sendGuildChatFrom(self, fromId, toId, message):
        assert self.notify.debugCall()
        self.sendUpdateToChannel(toId, "guildChatFrom", [fromId, emoteId])
        
