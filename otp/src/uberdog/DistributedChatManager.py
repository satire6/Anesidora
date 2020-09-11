"""
The Chat Manager handles all the chat access accross all districts.
"""

from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals

if __debug__:
    from direct.directnotify.DirectNotifyGlobal import directNotify
    notify = directNotify.newCategory('ChatManager')
    

class DistributedChatManager(DistributedObjectGlobal):
    """
    The Chat Manager is a global object.

    See Also:
        "otp/src/guild/DistributedChatManagerAI.py"
        "otp/src/configfiles/otp.dc"
    """
    if __debug__:
        notify = notify

    def __init__(self, cr):
        assert self.notify.debugCall()
        DistributedObjectGlobal.__init__(self, cr)
        self.notify.warning("ChatManager going online")

    def delete(self):
        assert self.notify.debugCall()
        self.ignoreAll()
        self.notify.warning("ChatManager going offline")
        self.cr.chatManager = None
        DistributedObjectGlobal.delete(self)
    
    def online(self):
        assert self.notify.debugCall()
    
    def adminChat(self, aboutId, message):
        """
        aboutId is a doId (This is currently always 0).
        message is a string
        
        This is a chat message from the administrator of the site.
        Making the user immediately aware of this message is probably
        a good idea.  An example message might be, "The servers are
        going down for maintanance in ten minutes!".
        """
        assert self.notify.debugCall()
        self.notify.warning("Admin Chat(%s): %s"%(aboutId, message))
        messenger.send("adminChat", [aboutId, message])
        

    # AI to Client
    #  def aiChat(self, message):
    #      assert self.notify.debugCall()
        

    # AI to UD
    if __debug__:
        def setAvatarLocation(self, avatarId, parentId, zoneId):
            assert 0, "Please don't call this on the client"
            
        def setAvatarCrew(self, avatarId, zoneId):
            assert 0, "Please don't call this on the client"
            
        def setAvatarGuild(self, avatarId, zoneId):
            assert 0, "Please don't call this on the client"
        
  
    # Client to location (zone)
    def sendChatTo(self, message, chatFlags):
        assert self.notify.debugCall()
        self.sendUpdate("chatTo", [message, chatFlags])
        
    def chatFrom(self, fromId, message, chatFlags):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])

    def sendSpeedChatTo(self, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdate("speedChatTo", [msgIndex])
        
    def speedChatFrom(self, fromId, msgIndex):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, msgIndex])
        

    def sendSpeedChatCustomTo(self, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdate("speedChatCustomTo", [msgIndex])
        
    def speedChatCustomFrom(self, fromId, msgIndex):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        

    # Client to avatar (doId)
    def sendWhisperTo(self, toId, message):
        assert self.notify.debugCall()
        self.sendUpdate("whisperTo", [toId, message])
        
    def whisperFrom(self, fromId, message):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        if base.cr.wantSwitchboardHacks:
            print "received whisper on avatar: %s" % message
            whisper = WhisperPopup(message,OTPGlobals.getInterfaceFont(),WhisperPopup.WTNormal)
            whisper.manage(base.marginManager)
        
    def sendWhisperSCTo(self, toId, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCTo", [toId, msgIndex])
        
    def whisperSCFrom(self, fromId, msgIndex):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        
    def sendWhisperSCCustomTo(self, toId, msgIndex):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCCustomTo", [toId, msgIndex])
        
    def whisperSCCustomFrom(self, fromId, msgIndex):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        
    def sendWhisperSCEmoteTo(self, toId, emoteId):
        assert self.notify.debugCall()
        self.sendUpdate("whisperSCEmoteTo", [toId, emoteId])
        
    def whisperSCEmoteFrom(self, fromId, emoteId):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        
    def whisperIgnored(self, fromId):
        assert self.notify.debugCall()
        

    # Client to crew (zone)
    def sendCrewChatTo(self, message):
        assert self.notify.debugCall()
        self.sendUpdate("crewChatTo", [message])
        
    def crewChatFrom(self, fromId, message):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        

    # Client to guild (zone)
    def sendGuildChatTo(self, message):
        assert self.notify.debugCall()
        self.sendUpdate("guildChatTo", [message])
        
    def guildChatFrom(self, fromId, message):
        assert self.notify.debugCall()
        #messenger.send("chat", [fromId, message, chatFlags])
        
