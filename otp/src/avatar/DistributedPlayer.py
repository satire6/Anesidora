"""DistributedPlayer module: contains the DistributedPlayer class"""

from pandac.PandaModules import *
from libotp import WhisperPopup
from libotp import CFQuicktalker, CFPageButton, CFQuitButton, CFSpeech, CFThought, CFTimeout
from otp.chat import ChatGarbler
import string
from direct.task import Task
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from direct.showbase import PythonUtil
from otp.avatar import DistributedAvatar
import time
from otp.avatar import Avatar, PlayerBase
from otp.chat import TalkAssistant
from otp.otpbase import OTPGlobals

#hack, init for client-side outgoing chat filter
if base.config.GetBool('want-chatfilter-hacks',0):
    from otp.switchboard import badwordpy
    import os
    badwordpy.init(os.environ.get('OTP')+'\\src\\switchboard\\','')


class DistributedPlayer(DistributedAvatar.DistributedAvatar,
                        PlayerBase.PlayerBase):
    """Distributed Player class:"""

    # This is the length of time that should elapse before we allow
    # another failed-teleport message to be displayed from the same
    # avatar.
    TeleportFailureTimeout = 60.0

    # Create a default chat garbler (can be overridden by child class)
    chatGarbler = ChatGarbler.ChatGarbler()

    def __init__(self, cr):
        """
        Handle distributed updates
        """
        try:
            self.DistributedPlayer_initialized
        except:
            self.DistributedPlayer_initialized = 1

            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            PlayerBase.PlayerBase.__init__(self)
            
            self.__teleportAvailable = 0

            self.inventory = None
            self.experience = None

            self.friendsList = []
            self.oldFriendsList = None
            self.timeFriendsListChanged = None
            self.ignoreList = []

            self.lastFailedTeleportMessage = {}
            self._districtWeAreGeneratedOn = None

            self.DISLname = ""
            self.DISLid = 0
            
            self.autoRun = 0

            self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1)
            
        
    ### managing ActiveAvatars ###

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        DistributedAvatar.DistributedAvatar.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        try:
            self.DistributedPlayer_deleted
        except:
            self.DistributedPlayer_deleted = 1
            del self.experience
            if self.inventory:
                self.inventory.unload()
            del self.inventory
            DistributedAvatar.DistributedAvatar.delete(self)
        
    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedAvatar.DistributedAvatar.generate(self)

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedAvatar.DistributedAvatar.setLocation(self, parentId, zoneId, teleport)
        # if the avatar just got put somewhere it shouldn't be, delete it
        # this is to prevent hackers from sidling over into an 'uber' zone, thereby
        # keeping themselves on your client even after the client no longer has interest in the
        # original, legitimate zone from which the hacker toon was generated
        if not (parentId in (0, None) and zoneId in (0, None)):
            if not self.cr._isValidPlayerLocation(parentId, zoneId):
                self.cr.disableDoId(self.doId)
                self.cr.deleteObject(self.doId)

    def isGeneratedOnDistrict(self, districtId=None):
        if districtId is None:
            return self._districtWeAreGeneratedOn is not None
        else:
            return self._districtWeAreGeneratedOn == districtId

    def getArrivedOnDistrictEvent(self, districtId=None):
        if districtId is None:
            return 'arrivedOnDistrict'
        else:
            return 'arrivedOnDistrict-%s' % districtId

    def arrivedOnDistrict(self, districtId):
        # we have been generated on this district
        curFrameTime = globalClock.getFrameTime()
        if hasattr(self,"frameTimeWeArrivedOnDistrict") and \
           curFrameTime == self.frameTimeWeArrivedOnDistrict:
            # rare case check if we get the zero from the shard we're leaving 
            # AFTER we get the district id of the shard we were going to
            if districtId == 0 and self._districtWeAreGeneratedOn:
                self.notify.warning("ignoring arrivedOnDistrict 0, since arrivedOnDistrict %d occured on the same frame" % self._districtWeAreGeneratedOn)
                return
        self._districtWeAreGeneratedOn = districtId
        self.frameTimeWeArrivedOnDistrict = globalClock.getFrameTime()
        messenger.send(self.getArrivedOnDistrictEvent(districtId))
        messenger.send(self.getArrivedOnDistrictEvent())

    def setLeftDistrict(self):
        self._districtWeAreGeneratedOn = None

    def hasParentingRules(self):
        # we can't define setParentingRules for the localAvatar in the DC because
        # that would define parenting rules for other players' avatars. Just
        # override this and always return True for the sake of the DoInterestManager
        if self is localAvatar:
            return True

    ### setAccountName ###

    def setAccountName(self, accountName):
        self.accountName = accountName
        
    ### setWhisper ###
        
    def setSystemMessage(self, aboutId, chatString,
                         whisperType = WhisperPopup.WTSystem):
        """setSystemMessage(self, int aboutId, string chatString)

        A message generated from the system (or the AI, or something
        like that).  If this involves another avatar (e.g. Flippy is
        now online), the aboutId is filled in; otherwise, aboutId is
        zero.
        """
        self.displayWhisper(aboutId, chatString, whisperType)
                
    def displayWhisper(self, fromId, chatString, whisperType):
        """displayWhisper(self, int fromId, string chatString, int whisperType)

        Displays the whisper message in whatever capacity makes sense.
        This is separate from setWhisper so we can safely call it by
        name from within setWhisper and expect the derived function to
        override it.
        """
        print "Whisper type %s from %s: %s" % (whisperType, fromId, chatString)
        
        
    def displayWhisperPlayer(self, playerId, chatString, whisperType):
        """
        Displays the whisper message in whatever capacity makes sense.
        This is separate from setWhisper so we can safely call it by
        name from within setWhisper and expect the derived function to
        override it.
        """
        print "WhisperPlayer type %s from %s: %s" % (whisperType, playerId, chatString)

    ### setWhisperSC ###

    def whisperSCTo(self, msgIndex, sendToId, toPlayer):
        """
        Sends a speedchat whisper message to the indicated
        avatar/player.
        """
        if toPlayer:
            base.cr.playerFriendsManager.sendSCWhisper(sendToId, msgIndex)
        else:
            messenger.send("wakeup")
            self.sendUpdate("setWhisperSCFrom", [self.doId, msgIndex], sendToId)

    def setWhisperSCFrom(self, fromId, msgIndex):
        """
        Receive and decode the SpeedChat message.
        """
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return

        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return

        if fromId in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return
        
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, fromId)

    ### setWhisperSCCustom ###

    def whisperSCCustomTo(self, msgIndex, sendToId, toPlayer):
        """
        Sends a speedchat whisper message to the indicated
        toon, prefixed with our own name.
        """
        if toPlayer:
            base.cr.playerFriendsManager.sendSCCustomWhisper(sendToId, msgIndex)
            return
    
        messenger.send("wakeup")
        self.sendUpdate("setWhisperSCCustomFrom", [self.doId, msgIndex],
                        sendToId)

    def _isValidWhisperSource(self, source):
        return True

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        """
        Receive and decode the SC message.
        """
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return

        if not self._isValidWhisperSource(handle):
            self.notify.warning('displayWhisper from non-toon %s' % fromId)
            return

        # new ignore list is handled by the Friends manager's, there are now two types, avatar and player.
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
           # We're ignoring this jerk.
           self.d_setWhisperIgnored(fromId)
           return
        
        if fromId in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return
            
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, fromId)

    ### setWhisperSCEmote ###

    def whisperSCEmoteTo(self, emoteId, sendToId, toPlayer):
        """
        Sends a speedchat whisper message to the indicated
        toon, prefixed with our own name.
        """
        print("whisperSCEmoteTo %s %s %s" % (emoteId, sendToId, toPlayer))
        if toPlayer:
            base.cr.playerFriendsManager.sendSCEmoteWhisper(sendToId, emoteId)
            return
        messenger.send("wakeup")
        self.sendUpdate("setWhisperSCEmoteFrom", [self.doId, emoteId],
                        sendToId)

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        """
        Receive and decode the SC message.
        """
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return

        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return
            
        chatString = SCDecoders.decodeSCEmoteWhisperMsg(emoteId,
                                                        handle.getName())
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTEmote)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_EMOTE, emoteId, fromId)

    def d_setWhisperIgnored(self, sendToId):
        # Don't send this message for the time being.
        # I haven't removed it completely since we may
        # want to send it in the future.
        
        # self.sendUpdate("setWhisperIgnored", [self.doId], sendToId)
        pass

    ### setChat ###
    def setChatAbsolute(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        DistributedAvatar.DistributedAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)
        if not quiet:
            pass

    def b_setChat(self, chatString, chatFlags):
        # Is this a magic word? All magic words begin with a ~
        if (self.cr.wantMagicWords and
            (len(chatString) > 0) and (chatString[0] == "~")):
            # Tell the magic word manager we just said a magic word
            messenger.send("magicWord", [chatString])
        else:
            # HACK for demo - Outgoing dirty word check.  NEVER RELY ON THIS.
            if base.config.GetBool('want-chatfilter-hacks',0):
                if base.config.GetBool('want-chatfilter-drop-offending',0):
                    if badwordpy.test(chatString):
                        return
                else:
                    chatString = badwordpy.scrub(chatString)

            # Local
            # avoid having to check if this is the local toon
            messenger.send("wakeup")
            self.setChatAbsolute(chatString, chatFlags)
            # Distributed
            self.d_setChat(chatString, chatFlags)


    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate("setChat", [chatString, chatFlags, 0])
        
        #self.sendUpdate("setTalk", [0, 0, chatString, []])

        
    def setTalk(self, fromAV, fromAC, avatarName, chat, mods, flags):
        newText, scrubbed = self.scrubTalk(chat, mods)
        self.displayTalk(newText)
        if base.talkAssistant.isThought(newText):
            newText = base.talkAssistant.removeThoughtPrefix(newText)
            base.talkAssistant.receiveThought(fromAV, avatarName, fromAC, None, newText, scrubbed)
        else:
            base.talkAssistant.receiveOpenTalk(fromAV, avatarName, fromAC, None, newText, scrubbed)
        
    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        newText, scrubbed = self.scrubTalk(chat, mods)
        #self.displayTalk(newText)
        self.displayTalkWhisper(fromAV, avatarName, chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.doId, self.getName(), newText, scrubbed)
        
    def displayTalkWhisper(self, fromId, avatarName, chatString, mods):
        """displayTalkWhisper(self, int fromId, string chatString)

        Displays the whisper message in whatever capacity makes sense.
        This is separate from setWhisper so we can safely call it by
        name from within setWhisper and expect the derived function to
        override it.
        """
        print "TalkWhisper from %s: %s" % (fromId, chatString)
        
    def scrubTalk(self, chat, mods):
        """
        returns chat where the mods have been replaced with appropreiate words
        this is not in chat assistant because the replacement needs to be done
        by the object that speeaks them. A pirate says "arr", 
        a duck says "quack", etc..
        """
        return chat

    def setChat(self, chatString, chatFlags, DISLid):
        """setChat(self, string)
        Garble the message if needed, then pass message to setChatAbsolute
        """
        self.notify.error("Should call setTalk")
        chatString = base.talkAssistant.whiteListFilterMessage(chatString)

        if base.cr.avatarFriendsManager.checkIgnored(self.doId):            
            # We're ignoring this jerk.
            return

        # if we don't have chat permission, garble the chat message
        if base.localAvatar.garbleChat and (not self.isUnderstandable()):
            chatString = self.chatGarbler.garble(self, chatString)

        # Clear any buttons or speedchat state from the chat flags;
        # both of these go through a different interface.
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)

        # Also, enforce that either the speech or thought bit is set,
        # and the timeout is set iff speech is set.
        if (chatFlags & CFThought):
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= (CFSpeech | CFTimeout)

        self.setChatAbsolute(chatString, chatFlags)




    ### setSC ###

    def b_setSC(self, msgIndex):
        # Local
        self.setSC(msgIndex)
        # Distributed
        self.d_setSC(msgIndex)

    def d_setSC(self, msgIndex):
        messenger.send("wakeup")
        self.sendUpdate("setSC", [msgIndex])

    def setSC(self, msgIndex):
        """
        Receive and decode the SC message
        """
        
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            # We're ignoring this jerk.
            return

        if self.doId in base.localAvatar.ignoreList:
            # We're ignoring this jerk.
            return
        
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString,
                                 CFSpeech | CFQuicktalker | CFTimeout, quiet = 1)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, self.doId)

    ### setSCCustom ###

    def b_setSCCustom(self, msgIndex):
        # Local
        self.setSCCustom(msgIndex)
        # Distributed
        self.d_setSCCustom(msgIndex)

    def d_setSCCustom(self, msgIndex):
        messenger.send("wakeup")
        self.sendUpdate("setSCCustom", [msgIndex])

    def setSCCustom(self, msgIndex):
        """
        Receive and decode the SC message
        """
        # new ignore list is handled by the Friends manager's, there are now two types, avatar and player.
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            # We're ignoring this jerk.
            return

        if self.doId in base.localAvatar.ignoreList:
            # We're ignoring this jerk.
            return

        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString,
                                 CFSpeech | CFQuicktalker | CFTimeout)
        base.talkAssistant.receiveOpenSpeedChat(TalkAssistant.SPEEDCHAT_CUSTOM, msgIndex, self.doId)

    ### setSCEmote ###

    def b_setSCEmote(self, emoteId):
        self.b_setEmoteState(emoteId,
                             animMultiplier=self.animMultiplier)

    def d_friendsNotify(self, avId, status):
        self.sendUpdate("friendsNotify", [avId, status])

    def friendsNotify(self, avId, status):
        """friendsNotify(self, int32 avId, int8 status)

        This message is sent by the AI to notify the client when
        friends are added or removed without the client's
        participation, if the client happens to be logged in.

        status is one of:

        1 - The indicated avatar is no longer your friend.
        2 - The indicated avatar is now your "special" friend.

        Other changes don't require notification, because the client
        was presumably in direct control.
        """
        avatar = base.cr.identifyFriend(avId)
        if (avatar != None):
            if (status == 1):
                self.setSystemMessage(avId, OTPLocalizer.WhisperNoLongerFriend % avatar.getName())
            elif (status == 2):
                self.setSystemMessage(avId, OTPLocalizer.WhisperNowSpecialFriend % avatar.getName())

    ### teleportQuery ###

    def d_teleportQuery(self, requesterId, sendToId = None):
        self.sendUpdate("teleportQuery", [requesterId], sendToId)
        #print("sending teleportQuery %s %s" % (requesterId, sendToId))

    def teleportQuery(self, requesterId):
        """teleportQuery(self, int requesterId)

        This distributed message is sent peer-to-peer from one client
        who is considering teleporting to another client.  When it is
        received, the receiving client should send back a
        teleportResponse indicating whether she is available to be
        teleported to (e.g. not on a trolley or something), and if so,
        where she is.
        """
        # Only consider teleport requests from toons who are on our
        # friends list, or who are somewhere nearby.
        #print("received teleportQuery %s" % (requesterId))
        #avatar = base.cr.identifyAvatar(requesterId)
        avatar = base.cr.playerFriendsManager.identifyFriend(requesterId)
            
        if avatar != None:
            # new ignore list is handled by the Friends manager's, there are now two types, avatar and player.
            if base.cr.avatarFriendsManager.checkIgnored(requesterId):
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId = requesterId)
                return

            # We're ignoring this jerk.  Send back a suitable response.
            if requesterId in self.ignoreList:
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId = requesterId)
                return

            # If we're in a private party and the requester isn't invited, tell
            # them we're busy (ie: let them down easy, don't rub it in their face)
            if hasattr(base, "distributedParty"):
                if base.distributedParty.partyInfo.isPrivate:
                    # We need to check the guest list of this party and see if
                    # requesterId is on the list
                    if requesterId not in base.distributedParty.inviteeIds:
                        # Sorry, not on the list, send a try-again-later message
                        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId = requesterId)
                        return                        
                                        
                if base.distributedParty.isPartyEnding:        
                    self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId = requesterId)
                    return

            #print("teleport Available %s Ghost %s" % (self.__teleportAvailable, self.ghostMode))            
            if self.__teleportAvailable and not self.ghostMode:
                # Generate a whisper message that so-and-so is teleporting
                # to us.
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperComingToVisit % (avatar.getName()))
            
                # We don't know where we are, so send a teleportQuery
                # to someone who does.  Whoever hangs a hook on this
                # event will call the appropriate teleportResponse.
                messenger.send('teleportQuery', [avatar, self])
                return

            # Generate a whisper message that so-and-so wants to
            # teleport to us, but can't because we're busy.  But don't
            # generate more than one of these per minute or so.
            if self.failedTeleportMessageOk(requesterId):
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % (avatar.getName()))


        # Send back a try-again-later message.
        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId = requesterId)

    def failedTeleportMessageOk(self, fromId):
        """failedTeleportMessageOk(self, int fromId)

        Registers a failure-to-teleport attempt from the indicated
        avatar.  Returns true if it is ok to display this message, or
        false if the message should be suppressed (because we just
        recently displayed one).
        """
        now = globalClock.getFrameTime()
        lastTime = self.lastFailedTeleportMessage.get(fromId, None)
        if lastTime != None:
            elapsed = now - lastTime
            if elapsed < self.TeleportFailureTimeout:
                return 0

        self.lastFailedTeleportMessage[fromId] = now
        return 1

    ### teleportResponse ###

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId,
                           sendToId = None):
        self.sendUpdate("teleportResponse", [avId, available, shardId, hoodId, zoneId], sendToId)

    def teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        messenger.send('teleportResponse', [avId, available, shardId, hoodId, zoneId])

    ### teleportGiveup ###

    def d_teleportGiveup(self, requesterId, sendToId = None):
        self.sendUpdate("teleportGiveup", [requesterId], sendToId)

    def teleportGiveup(self, requesterId):
        """teleportGiveup(self, int requesterId)

        This message is sent after a client has failed to teleport
        successfully to another client, probably because the target
        client didn't stay put.  It just pops up a whisper message to
        that effect.

        """
        avatar = base.cr.identifyAvatar(requesterId)

        if not self._isValidWhisperSource(avatar):
            self.notify.warning('teleportGiveup from non-toon %s' % requesterId)
            return
            
        if avatar != None:
            self.setSystemMessage(requesterId, OTPLocalizer.WhisperGiveupVisit % (avatar.getName()))

    ### teleportGreeting ###

    # This message is sent on completion of teleport, to set up the
    # automatic "Hi, so-and-so" chat balloon.  We can't use setChat
    # because that gets garbled for speedchat-only clients.

    def b_teleportGreeting(self, avId):
        self.d_teleportGreeting(avId)
        self.teleportGreeting(avId)

    def d_teleportGreeting(self, avId):
        self.sendUpdate("teleportGreeting", [avId])

    def teleportGreeting(self, avId):
        # Normally, the greeting will be issued to someone who we have
        # just teleported to, and is therefore in the same zone with
        # us.  If this is so, it is easy to determine what the greeted
        # toon's actual name is; otherwise, something went wrong
        # (maybe our greeted toon just left!) and we can simply ignore
        # the message.

        avatar = base.cr.getDo(avId)
        if isinstance(avatar, Avatar.Avatar):
            self.setChatAbsolute(OTPLocalizer.TeleportGreeting % (
                avatar.getName()), CFSpeech | CFTimeout)
        elif avatar is not None:
            self.notify.warning(
                'got teleportGreeting from %s referencing non-toon %s' % (
                self.doId, avId))

    ### Teleport support functions ###

    def setTeleportAvailable(self, available):
        """setTeleportAvailable(self, bool available)

        Sets the 'teleportAvailable' flag.  When this is true, the
        client is deemed to be available to be teleported to, and
        someone should be listening to teleportQuery messages from the
        messenger.  When it is false, teleport queries from nearby
        toons will automatically be returned with a false response
        without generating a teleportQuery message.
        """
        self.__teleportAvailable = available

    def getTeleportAvailable(self):
        return self.__teleportAvailable

    def getFriendsList(self):
        return self.friendsList

    def setFriendsList(self, friendsList):
        self.oldFriendsList = self.friendsList
        self.friendsList = friendsList
        self.timeFriendsListChanged = globalClock.getFrameTime()
        assert self.notify.debug("setting friends list to %s" % self.friendsList)

        # We want to throw a special event whenever the LocalToon's
        # friends list changes, although not when just any
        # DistributedToon's friends list changes.  It would be cleaner
        # to define this special behavior in LocalToon.py, but as it
        # happens, it won't get called there because of the way
        # ClientDistUpdate.py works.

        # Fortunately, this method will *only* get called for
        # LocalToon, and not for any of the other DistributedToons.
        # So we can get away with putting this here.
        messenger.send('friendsListChanged')

        # When our friends list changes, the set of other avatars we
        # can understand might also change.
        Avatar.reconsiderAllUnderstandable()

    def setDISLname(self, name):
        self.DISLname = name

    def setDISLid(self, id):
        self.DISLid = id

        
    def setAutoRun(self, value):
        self.autoRun = value

    def getAutoRun(self):
        return self.autoRun
