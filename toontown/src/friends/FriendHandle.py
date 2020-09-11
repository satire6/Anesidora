from toontown.toonbase import ToontownGlobals
import copy
from toontown.chat import ToonChatGarbler
from toontown.toon import GMUtils

class FriendHandle:
    """FriendHandle

    This is a class object that serves as a structure to hold all the
    details we are entitled to find out about one of our friends.  In
    particular, it can tell us our friend's id number, name, dna, and petId
    and it may be able to tell us more.

    """

    def __init__(self, doId, name, style, petId, isAPet = False):
        self.doId = doId
        self.style = style
        self.commonChatFlags = 0
        self.whitelistChatFlags = 0
        self.petId = petId
        self.isAPet = isAPet
        self.chatGarbler = ToonChatGarbler.ToonChatGarbler()
        
        if GMUtils.testGMIdentity(name):
            self.name = GMUtils.handleGMName(name)
        else:
            self.name = name
    
    def getDoId(self):
        """getDoId(self)
        Return the distributed object id
        """
        return self.doId

    def getPetId(self):
        return self.petId

    def hasPet(self):
        return (self.getPetId() != 0)

    def isPet(self):
        return self.isAPet

    def getName(self):
        return self.name

    def getFont(self):
        # All friends are toons.
        return ToontownGlobals.getToonFont()
        
    def getStyle(self):
        return self.style
    
    def uniqueName(self, idString):
        # This must match DistributedObject.uniqueName().
        return (idString + "-" + str(self.getDoId()))

    def d_battleSOS(self, requesterId):
        base.localAvatar.sendUpdate("battleSOS", [requesterId],
                                      sendToId = self.doId)

    def d_teleportQuery(self, requesterId):
        base.localAvatar.sendUpdate("teleportQuery", [requesterId],
                                      sendToId = self.doId)

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        base.localAvatar.sendUpdate("teleportResponse",
                                      [avId, available, shardId, hoodId, zoneId],
                                      sendToId = self.doId)

    def d_teleportGiveup(self, requesterId):
        base.localAvatar.sendUpdate("teleportGiveup",
                                      [requesterId],
                                      sendToId = self.doId)


    def isUnderstandable(self):
        """isUnderstandable(self)

        Returns true if this avatar can chat freely with localtoon,
        false otherwise.
        """

        # For the moment, commonChatFlags is always 0 for a
        # FriendHandle.  We need to get this information from the
        # server in order for this to work as generally as possible;
        # in the meantime, whispering to distant friends won't respect
        # their common chat flags.

        if self.commonChatFlags & base.localAvatar.commonChatFlags & ToontownGlobals.CommonChat:
            # Both this avatar and the local toon have common chat
            # permission.  OK.
            understandable = 1
            
        elif self.commonChatFlags & ToontownGlobals.SuperChat:
            # This avatar has "super chat" permission, so anyone
            # can understand him.  OK.
            understandable = 1
            
        elif base.localAvatar.commonChatFlags & ToontownGlobals.SuperChat:
            # Local toon has "super chat" permission, so we can
            # understand everyone.  OK.
            understandable = 1

        elif base.cr.getFriendFlags(self.doId) & ToontownGlobals.FriendChat:
            # This avatar is a special friend of the local toon.  OK.
            understandable = 1
            
        elif self.whitelistChatFlags & base.localAvatar.whitelistChatFlags:
             # Both this avatar and the local toon have whitelist chat
             # permission.  OK.
             understandable = 1
        else:
            # Too bad.
            understandable = 0

        return understandable
        
    def scrubTalk(self, message, mods):
        scrubbed = 0
        text = copy.copy(message)
        for mod in mods:
            index = mod[0]
            length = mod[1] - mod[0] + 1
            newText = text[0:index] + length*"" + text[index + length:]
            text = newText
            
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "":
                newwords.append(word)
            elif word[0] == "":
                #newwords.append("Bleep")
                newwords.append("\1WLDisplay\1" + self.chatGarbler.garbleSingle(self, word) + "\2")
                scrubbed =1
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append("\1WLDisplay\1" + word + "\2")
                scrubbed = 1
                
        newText = " ".join(newwords)
        return newText, scrubbed
        

    def replaceBadWords(self, text):
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "":
                newwords.append(word)
            elif word[0] == "":
                #newwords.append("Bleep")
                newwords.append("\1WLRed\1" + self.chatGarbler.garbleSingle(self, word) + "\2")
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append("\1WLRed\1" + word + "\2")
                
        newText = " ".join(newwords)
        return newText
    
    def setCommonAndWhitelistChatFlags(self, commonChatFlags, whitelistChatFlags):
        """Friend came online and otp_server told us his common and whitelist settings."""
        self.commonChatFlags = commonChatFlags
        self.whitelistChatFlags = whitelistChatFlags
