import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from pandac.PandaModules import *
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkHandle import TalkHandle
import time
from otp.chat.TalkGlobals import *
from otp.chat.ChatGlobals import *
from libotp import CFSpeech, CFTimeout, CFThought


"""
The purpose of this assistant is to organize everything you need
for chat into one class. It does not rewire the paths for talk.
It is only client side and does not actually send or receive any
messages.

It's become required because talk functionality has become fractured
and is now spread between the playerFriendsManager, the
avatarFriendsManager, the clientRepository, and the DistributedAvatar.
This assistant makes all this functionality available from a single 
point of contact.

The only unique functionality is does is talk logging.

It contains helper functions to send and receive talk and logs that
chat whenever these helper functions are used. Each sender function
is hardwired to another function, and each receiver function must be
hardwired into another function:

Example:
   Calling sendOpenSpeedChat also calls base.localAvatar.b_setSC
   from within the assistant

Counter Example:
   Calling avatar.setSC needs to call receiveWhisperSpeedChat
   from outside the assistant

This assistant also contains functions to determine whether or not
you can chat with any given avatar or player, one example is
'checkWhisperTypedChatAvatar'. The idea is that these checks
relate directly to the gui buttons a player would use to send messages.

JML

talk message data structure is (
                            timeStamp,          #0
                            body,               #1
                            senderAvatarId,     #2
                            senderAvatarName,   #3
                            senderAccountId,    #4
                            senderAccountName,  #5
                            receiverAvatarId,   #6
                            receiverAvatarName, #7
                            receiverAccountId,  #8
                            receiverAccountName,#9
                            talkType,           #10
                            extraInfo,          #11
                           )
                           
(timeStamp, message, doId, accountId, avatarName, accountName, type, typeInfo)                           
"""


ThoughtPrefix = '.'

class TalkAssistant(DirectObject.DirectObject):
    ExecNamespace = None
    """
    contains methods for turning chat inputs
    into onscreen thought/word balloons
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TalkAssistant")
    execChat = base.config.GetBool("exec-chat", 0)

    def __init__(self):
        assert self.notify.debug("TalkAssistant")
        # Store the client repository
        self.logWhispers = 1
        self.whiteList = None
        self.clearHistory()
        self.zeroTimeDay = time.time()
        self.zeroTimeGame = globalClock.getRealTime()
        self.floodThreshold = 10.0
        
        self.useWhiteListFilter = base.config.GetBool('white-list-filter-openchat', 0)
        
        self.lastWhisperDoId = None
        self.lastWhisperPlayerId = None
        self.lastWhisper = None
        
        self.SCDecoder = SCDecoders
        
        
#SETUP AND CLEANUP

    def clearHistory(self):
        self.historyComplete = [] #all messages
        self.historyOpen = [] #open messages
        self.historyUpdates = [] #game updates (exp, friend logins, leveling, etc...)
        self.historyGuild = [] #guild messages and updates
        
        self.historyByDoId = {} #messages to and from a certain doId
        self.historyByDISLId = {} #message to and from a certain DISLId
        
        self.floodDataByDoId = {}
        
        self.labelGuild = OTPLocalizer.TalkGuild
        
        self.handleDict = {}
        
        self.messageCount = 0
        
        self.shownWhiteListWarning = 0
        
    def delete(self):
        self.ignoreAll()
        self.clearHistory()
        
    def start(self):
        pass
        
    def stop(self):
        pass
        
# DATA RETRIEVAL
    def countMessage(self):
        self.messageCount += 1
        return self.messageCount - 1

    def getOpenText(self, numLines, startPoint = 0):
        return self.historyOpen[startPoint:startPoint + numLines]
        
    def getSizeOpenText(self):
        return len(self.historyOpen)
        
    def getCompleteText(self, numLines, startPoint = 0):
        return self.historyComplete[startPoint:startPoint + numLines]
        
    def getCompleteTextFromRecent(self, numLines, startPoint = 0):
        #print("getCompleteText start %s numLines %s" % (startPoint, numLines))
        start = len(self.historyComplete) - startPoint
        if start  < 0:
            start = 0  
            
        backStart = max(start-numLines, 0)

        #print start

        text = self.historyComplete[backStart:start]
        text.reverse()
        return text
        
    def getAllCompleteText(self):
        return self.historyComplete
        
    def getAllHistory(self):
        return self.historyComplete
        
    def getSizeCompleteText(self):
        return len(self.historyComplete)
        
    def getHandle(self, doId):
        return self.handleDict.get(doId)
        
# DATA ADDING

    def doWhiteListWarning(self):
        pass

    def addToHistoryDoId(self, message, doId, scrubbed = 0):
        if (message.getTalkType() == TALK_WHISPER) and (doId != localAvatar.doId):
            self.lastWhisperDoId = doId
            self.lastWhisper = self.lastWhisperDoId
        
        if not self.historyByDoId.has_key(doId):
            self.historyByDoId[doId] = []
        self.historyByDoId[doId].append(message)
        
        if (not self.shownWhiteListWarning) and scrubbed and (doId == localAvatar.doId):
            self.doWhiteListWarning()
            self.shownWhiteListWarning = 1
            
        if not self.floodDataByDoId.has_key(doId):
            self.floodDataByDoId[doId] = [0.0, self.stampTime(), message] #floodRating, lastTime, message
        else:
            oldTime = self.floodDataByDoId[doId][1]
            newTime = self.stampTime()
            timeDiff = newTime - oldTime
            oldRating = self.floodDataByDoId[doId][0]
            contentMult = 1.0
            if len(message.getBody()) < 6:
                contentMult += (0.2 * float(6 - len(message.getBody())))
            if self.floodDataByDoId[doId][2].getBody() == message.getBody():
                contentMult += 1.0
            floodRating = max(0, ((3.0 * contentMult) + oldRating - timeDiff))
            #print ("Flood Time Diff %s %s %s" % (oldTime, newTime, timeDiff))
            #print("Flood Rating %s" % (floodRating))
            self.floodDataByDoId[doId] = [floodRating, self.stampTime(), message]
            
            if floodRating > self.floodThreshold:
                if oldRating < self.floodThreshold:
                    self.floodDataByDoId[doId] = [floodRating + 3.0, self.stampTime(), message]
                    #print("start rejecting")
                    return 1
                else:
                    self.floodDataByDoId[doId] = [oldRating - timeDiff, self.stampTime(), message]
                    #print ("don't even log this")
                    return 2
            
        return 0
        
    def addToHistoryDISLId(self, message, dISLId, scrubbed = 0):
        if (message.getTalkType() == TALK_ACCOUNT) and (dISLId != base.cr.accountDetailRecord.playerAccountId):
            self.lastWhisperPlayerId = dISLId
            self.lastWhisper = self.lastWhisperPlayerId
        if not self.historyByDISLId.has_key(dISLId):
            self.historyByDISLId[dISLId] = []
        self.historyByDISLId[dISLId].append(message)
        
    def addHandle(self, doId, message):
        if doId == localAvatar.doId:
            return
        handle = self.handleDict.get(doId)
        if not handle:
            handle = TalkHandle(doId, message)
            self.handleDict[doId] = handle
        else:
            handle.addMessageInfo(message)
        
# DATA CHECKING

    def stampTime(self):
        # because time.time is giving me so much trouble I'm abstracting the time fuction
        # note: time.time doesn't work correctly. While running directX it only updates once
        # every few minutes, this appears to be a directX "feature"
        #return self.zeroTimeDay + (globalClock.getRealTime() - self.zeroTimeGame)
        return (globalClock.getRealTime() - self.zeroTimeGame)
        
# HELPER FUNCTIONS

    def findName(self, id, isPlayer = 0):
        if isPlayer:
            return self.findPlayerName(id)
        else:
            return self.findAvatarName(id)

            
    def findAvatarName(self, id):
        info = base.cr.identifyAvatar(id)
        if info:
            return info.getName()
        else:
            return ''
    
    def findPlayerName(self, id):
        info = base.cr.playerFriendsManager.getFriendInfo(id)
        if info:
            return info.playerName
        else:
            return ''
        
    def whiteListFilterMessage(self, text):
        if not self.useWhiteListFilter:
            return text
        elif not base.whiteList:
            return "no list"
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "" or base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append(base.whiteList.defaultWord)
                
        newText = " ".join(newwords)
        return newText
        
        
    def colorMessageByWhiteListFilter(self, text):
        if not base.whiteList:
            return text
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "" or base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append("\1WLRed\1" + word + "\2")
                
        newText = " ".join(newwords)
        return newText
        
    def executeSlashCommand(self, text):
        pass
        
    def executeGMCommand(self, text):
        pass
        
    def isThought(self, message):
        """
        message is a string.
        
        Return 1 if the given string contains the thought prefix,
        Return 0 otherwise
        """
        if not message:
            return 0
        elif (len(message) == 0):
            # empty string cannot be a thought
            return 0
        elif (string.find(message, ThoughtPrefix, 0,
                          len(ThoughtPrefix)) >= 0):
            return 1
        else:
            return 0

    def removeThoughtPrefix(self, message):
        """
        message is a string.
        
        Return the string with the thought prefix removed
        """
        if (self.isThought(message)):
            return message[len(ThoughtPrefix):]
        else:
            return message
            
    def fillWithTestText(self):
        hold = self.floodThreshold
        self.floodThreshold = 1000.0
        self.receiveOpenTalk(1001, "Bob the Ghost", None, None, "Hello from the machine")
        self.receiveOpenTalk(1001, "Bob the Ghost", None, None, "More text for ya!")
        self.receiveOpenTalk(1001, "Bob the Ghost", None, None, "Hope this makes life easier")
        self.receiveOpenTalk(1002, "Doug the Spirit", None, None, "Now we need some longer text that will spill over onto two lines")
        self.receiveOpenTalk(1002, "Doug the Spirit", None, None, "Maybe I will tell you")
        self.receiveOpenTalk(1001, "Bob the Ghost", None, None, "If you are seeing this text it is because you are cool")
        self.receiveOpenTalk(1002, "Doug the Spirit", None, None, "That's right, there is no need to call tech support")
        self.receiveOpenTalk(localAvatar.doId, localAvatar.getName, None, None, "Okay I won't call tech support, because I am cool")
        self.receiveGMTalk(1003, "God of Text", None, None, "Good because I have seen it already")
        self.floodThreshold = hold
            
    def printHistoryComplete(self):
        print("HISTORY COMPLETE")
        for message in self.historyComplete:
            print("%s %s %s\n%s\n" % (message.getTimeStamp(), message.getSenderAvatarName(), message.getSenderAccountName(), message.getBody()))
        
    ####################################
    # Exec-chat functions
    def importExecNamespace(self):
        # Derived classes should take advantage of this hook to import
        # useful variables into the chat namespace for developer
        # access.
        pass
        
    def execMessage(self, message):
        print ("execMessage %s" % (message))
        if not TalkAssistant.ExecNamespace:
            # Import some useful variables into the ExecNamespace initially.
            TalkAssistant.ExecNamespace = { }
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
            self.importExecNamespace()

        # Now try to evaluate the expression using ChatInputTyped.ExecNamespace as
        # the local namespace.
        
        try:
            return str(eval(message, globals(), TalkAssistant.ExecNamespace))

        except SyntaxError:
            # Maybe it's only a statement, like "x = 1", or
            # "import math".  These aren't expressions, so eval()
            # fails, but they can be exec'ed.
            try:
                exec message in globals(), TalkAssistant.ExecNamespace
                return "ok"
            except:
                exception = sys.exc_info()[0]
                extraInfo = sys.exc_info()[1]
                if extraInfo:
                    return str(extraInfo)
                else:
                    return str(exception)
        except:
            exception = sys.exc_info()[0]
            extraInfo = sys.exc_info()[1]
            if extraInfo:
                return str(extraInfo)
            else:
                return str(exception)
        
# CHAT PERMISSIONS

    def checkOpenTypedChat(self):
        if base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            return True
        return False

    def checkAnyTypedChat(self):
        """Return True if we have any form of typed chat, whitelist, truefriend or open."""
        if base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            return True
        if base.localAvatar.canChat():
            return True
        return False    
        
    def checkOpenSpeedChat(self):
        return True
        
    def checkWhisperTypedChatAvatar(self, avatarId):
        remoteAvatar = base.cr.doId2do.get(avatarId)
        if remoteAvatar:
            # check for open chat or whitelist chat
            if remoteAvatar.isUnderstandable():
                return True

        if base.localAvatar.commonChatFlags & OTPGlobals.SuperChat:
            return True

        # check for toon friends in different zones
        remoteAvatarOrHandleOrInfo = base.cr.identifyAvatar(avatarId)
        if remoteAvatarOrHandleOrInfo and hasattr(remoteAvatarOrHandleOrInfo,'isUnderstandable'):
            if remoteAvatarOrHandleOrInfo.isUnderstandable():
                return True
        
        # check for player friends
        info =  base.cr.playerFriendsManager.findPlayerInfoFromAvId(avatarId)
        if info:
            if info.understandableYesNo:
                return True

        # check for avatar friend and we both have open chat
        info = base.cr.avatarFriendsManager.getFriendInfo(avatarId)
        if info:
            if info.understandableYesNo:
                return True

        # check for true avatar friends
        if base.cr.getFriendFlags(avatarId) & OTPGlobals.FriendChat:
            return True

        return False            
       
    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True
        
    def checkWhisperTypedChatPlayer(self, playerId):
        info =  base.cr.playerFriendsManager.getFriendInfo(playerId)
        if info:
            if info.understandableYesNo:
                return True
        return False
        
    def checkWhisperSpeedChatPlayer(self, playerId):
        if base.cr.playerFriendsManager.isPlayerFriend(playerId):
            return True
        return False
        
    def checkOpenSpeedChat(self):
        return True
        
    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True
        
    def checkWhisperSpeedChatPlayer(self, playerId):
        if base.cr.playerFriendsManager.isPlayerFriend(playerId):
            return True
        return False
        
    def checkGuildTypedChat(self):
        if localAvatar.guildId:
            return True
        return False
    
    def checkGuildSpeedChat(self):
        if localAvatar.guildId:
            return True
        return False
        
        
#RECEIVE TALK

    def receiveOpenTalk(self, avatarId, avatarName, accountId, accountName, message, scrubbed = 0):
        error = None
        if (not avatarName) and (avatarId):
            avatarName = self.findAvatarName(avatarId)
        if (not accountName) and (accountId):
            accountName = self.findPlayerName(accountId)
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        avatarId, #senderAvatarId
                        avatarName, #senderAvatarName 
                        accountId, #senderAccountId
                        accountName, #senderAccountName
                        None, #receiverAvatarId
                        None, #receiverAvatarName 
                        None, #receiverAccountId
                        None, #receiverAccountName
                        TALK_OPEN, #talkType
                        None) #extraInfo
                        
        if avatarId != localAvatar.doId:
            self.addHandle(avatarId, newMessage)
            
        reject = 0
        if avatarId:
            reject = self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        if reject == 1:
            newMessage.setBody(OTPLocalizer.AntiSpamInChat)            
        if reject != 2:
            self.historyComplete.append(newMessage)
            self.historyOpen.append(newMessage)

            messenger.send("NewOpenMessage", [newMessage])
        
        return error
        
    def receiveWhisperTalk(self, avatarId, avatarName, accountId, accountName, toId, toName, message, scrubbed = 0):
        error = None
        print ("receiveWhisperTalk %s %s %s %s %s" % (avatarId, avatarName, accountId, accountName, message))
        if (not avatarName) and (avatarId):
            avatarName = self.findAvatarName(avatarId)
        if (not accountName) and (accountId):
            accountName = self.findPlayerName(accountId)
            

        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        avatarId, #senderAvatarId
                        avatarName, #senderAvatarName 
                        accountId, #senderAccountId
                        accountName, #senderAccountName
                        toId, #receiverAvatarId
                        toName, #receiverAvatarName 
                        None, #receiverAccountId
                        None, #receiverAccountName
                        TALK_WHISPER, #talkType
                        None) #extraInfo
                        
        if avatarId == localAvatar.doId:
            self.addHandle(toId, newMessage)
        else:    
            self.addHandle(avatarId, newMessage)
            
        self.historyComplete.append(newMessage)
            
        if avatarId:
            self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        messenger.send("NewOpenMessage", [newMessage])
        
        return error
        
        
    def receiveAccountTalk(self, avatarId, avatarName, accountId, accountName, toId, toName, message, scrubbed = 0):
        if (not accountName) and base.cr.playerFriendsManager.playerId2Info.get(accountId):
            accountName = base.cr.playerFriendsManager.playerId2Info.get(accountId).playerName
            #print ("Getting Name %s " % (base.cr.playerFriendsManager.playerId2Info.get(accountId).playerName))
            
        error = None
        if (not avatarName) and (avatarId):
            avatarName = self.findAvatarName(avatarId)
        if (not accountName) and (accountId):
            accountName = self.findPlayerName(accountId)
            

        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        avatarId, #senderAvatarId
                        avatarName, #senderAvatarName 
                        accountId, #senderAccountId
                        accountName, #senderAccountName
                        None, #receiverAvatarId
                        None, #receiverAvatarName 
                        toId, #receiverAccountId
                        toName, #receiverAccountName
                        TALK_ACCOUNT, #talkType
                        None) #extraInfo
            
        self.historyComplete.append(newMessage)
        if avatarId:
            self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId, scrubbed)
        messenger.send("NewOpenMessage", [newMessage])
        
        return error
    
    def receiveGuildTalk(self, fromAv, fromAC, avatarName, message, scrubbed = 0):
        error = None
        if not self.isThought(message):
            
            accountName = self.findName(fromAC, 1)
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            fromAv, #senderAvatarId
                            avatarName, #senderAvatarName 
                            fromAC, #senderAccountId
                            accountName, #senderAccountName
                            None, #receiverAvatarId
                            None, #receiverAvatarName 
                            None, #receiverAccountId
                            None, #receiverAccountName
                            TALK_GUILD, #talkType
                            None) #typeInfo 
                            
            reject = self.addToHistoryDoId(newMessage, fromAv, scrubbed)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)            
            if reject != 2:
                self.historyComplete.append(newMessage)
                self.historyGuild.append(newMessage)
                messenger.send("NewOpenMessage", [newMessage])
                
        return error

    def receiveGMTalk(self, avatarId, avatarName, accountId, accountName, message, scrubbed = 0):
        error = None
        if (not avatarName) and (avatarId):
            avatarName = self.findAvatarName(avatarId)
        if (not accountName) and (accountId):
            accountName = self.findPlayerName(accountId)
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        avatarId, #senderAvatarId
                        avatarName, #senderAvatarName 
                        accountId, #senderAccountId
                        accountName, #senderAccountName
                        None, #receiverAvatarId
                        None, #receiverAvatarName 
                        None, #receiverAccountId
                        None, #receiverAccountName
                        TALK_GM, #talkType
                        None) #extraInfo
                        
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        if avatarId:
            self.addToHistoryDoId(newMessage, avatarId)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        messenger.send("NewOpenMessage", [newMessage])
        
        return error
        
    def receiveThought(self, avatarId, avatarName, accountId, accountName, message, scrubbed = 0):
        error = None
        if (not avatarName) and (avatarId):
            avatarName = self.findAvatarName(avatarId)
        if (not accountName) and (accountId):
            accountName = self.findPlayerName(accountId)
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        avatarId, #senderAvatarId
                        avatarName, #senderAvatarName 
                        accountId, #senderAccountId
                        accountName, #senderAccountName
                        None, #receiverAvatarId
                        None, #receiverAvatarName 
                        None, #receiverAccountId
                        None, #receiverAccountName
                        AVATAR_THOUGHT, #talkType
                        None) #extraInfo
                        
        if avatarId != localAvatar.doId:
            self.addHandle(avatarId, newMessage)
            
        reject = 0
        if avatarId:
            reject = self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        if reject == 1:
            newMessage.setBody(OTPLocalizer.AntiSpamInChat)            
        if reject != 2:
            self.historyComplete.append(newMessage)
            self.historyOpen.append(newMessage)

            messenger.send("NewOpenMessage", [newMessage])
        
        return error

# RECEIVE MESSAGES
            
    def receiveGameMessage(self, message):
        error = None
        if not self.isThought(message):
            
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            None, #senderAvatarId
                            None, #senderAvatarName 
                            None, #senderAccountId
                            None, #senderAccountName
                            localAvatar.doId, #receiverAvatarId
                            localAvatar.getName(), #receiverAvatarName 
                            localAvatar.DISLid, #receiverAccountId
                            localAvatar.DISLname, #receiverAccountName
                            INFO_GAME, #talkType
                            None) #extraInfo
            
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
        messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def receiveSystemMessage(self, message):
        error = None
        if not self.isThought(message):
            
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            None, #senderAvatarId
                            None, #senderAvatarName 
                            None, #senderAccountId
                            None, #senderAccountName
                            localAvatar.doId, #receiverAvatarId
                            localAvatar.getName(), #receiverAvatarName 
                            localAvatar.DISLid, #receiverAccountId
                            localAvatar.DISLname, #receiverAccountName
                            INFO_SYSTEM, #talkType
                            None) #extraInfo
            
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
        messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def receiveDeveloperMessage(self, message):
        error = None

            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        None, #senderAvatarId
                        None, #senderAvatarName 
                        None, #senderAccountId
                        None, #senderAccountName
                        localAvatar.doId, #receiverAvatarId
                        localAvatar.getName(), #receiverAvatarName 
                        localAvatar.DISLid, #receiverAccountId
                        localAvatar.DISLname, #receiverAccountName
                        INFO_DEV, #talkType
                        None) #extraInfo
        
        self.historyComplete.append(newMessage)
        self.historyUpdates.append(newMessage)
        messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def receiveGuildMessage(self, message, senderId, senderName):
        #Should only be used for speedchat
        error = None
        if not self.isThought(message):
            
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            senderId, #senderAvatarId
                            senderName, #senderAvatarName 
                            None, #senderAccountId
                            None, #senderAccountName
                            None, #receiverAvatarId
                            None, #receiverAvatarName 
                            None, #receiverAccountId
                            None, #receiverAccountName
                            TALK_GUILD, #talkType
                            None) #extraInfo 
        
            self.historyComplete.append(newMessage)
            self.historyGuild.append(newMessage)   
        messenger.send("NewOpenMessage", [newMessage])
        return error

        
# RECEIVE UPDATES
    
    def receiveFriendUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        onlineMessage, #message Body
                        friendId, #senderAvatarId
                        friendName, #senderAvatarName 
                        None, #senderAccountId
                        None, #senderAccountName
                        localAvatar.doId, #receiverAvatarId
                        localAvatar.getName(), #receiverAvatarName 
                        localAvatar.DISLid, #receiverAccountId
                        localAvatar.DISLname, #receiverAccountName
                        UPDATE_FRIEND, #talkType
                        None) #extraInfo
                        
        self.addHandle(friendId, newMessage)
        self.historyComplete.append(newMessage)   
        self.historyUpdates.append(newMessage)        
        messenger.send("NewOpenMessage", [newMessage])
        
    def receiveFriendAccountUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        onlineMessage, #message Body
                        None, #senderAvatarId
                        None, #senderAvatarName 
                        friendId, #senderAccountId
                        friendName, #senderAccountName
                        localAvatar.doId, #receiverAvatarId
                        localAvatar.getName(), #receiverAvatarName 
                        localAvatar.DISLid, #receiverAccountId
                        localAvatar.DISLname, #receiverAccountName
                        UPDATE_FRIEND, #talkType
                        None) #extraInfo
            
        self.historyComplete.append(newMessage)   
        self.historyUpdates.append(newMessage)        
        messenger.send("NewOpenMessage", [newMessage])
        
    def receiveGuildUpdate(self, memberId, memberName, isOnline):
        if base.cr.identifyFriend(memberId) is None:
            if isOnline:
                onlineMessage = OTPLocalizer.GuildMemberOnline
            else:
                onlineMessage = OTPLocalizer.GuildMemberOffline
                
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            onlineMessage, #message Body
                            memberId, #senderAvatarId
                            memberName, #senderAvatarName 
                            None, #senderAccountId
                            None, #senderAccountName
                            None, #receiverAvatarId
                            None, #receiverAvatarName 
                            None, #receiverAccountId
                            None, #receiverAccountName
                            UPDATE_GUILD, #talkType
                            None) #extraInfo 
                    
            self.addHandle(memberId, newMessage)
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
            self.historyGuild.append(newMessage)                                       
            messenger.send("NewOpenMessage", [newMessage])
        
# RECEIVE SPEEDCHAT

    def receiveOpenSpeedChat(self, type, messageIndex, senderId, name = None):
        #print("receiveOpenSpeedChat %s %s %s" %(type, messageIndex, senderId))
        error = None

        if (not name) and (senderId):
            name = self.findName(senderId, 0)

        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
            
        if message in (None, ""):
            return
                            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        senderId, #senderAvatarId
                        name, #senderAvatarName 
                        None, #senderAccountId
                        None, #senderAccountName
                        None, #receiverAvatarId
                        None, #receiverAvatarName 
                        None, #receiverAccountId
                        None, #receiverAccountName
                        TALK_OPEN, #talkType
                        None) #extraInfo
                                
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDoId(newMessage, senderId)
        messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def receiveAvatarWhisperSpeedChat(self,  type, messageIndex, senderId, name = None):
        error = None
        
        if (not name) and (senderId):
            name = self.findName(senderId, 0)
            
        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        senderId, #senderAvatarId
                        name, #senderAvatarName 
                        None, #senderAccountId
                        None, #senderAccountName
                        localAvatar.doId, #receiverAvatarId
                        localAvatar.getName(), #receiverAvatarName 
                        localAvatar.DISLid, #receiverAccountId
                        localAvatar.DISLname, #receiverAccountName
                        TALK_WHISPER, #talkType
                        None) #extraInfo
            
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDoId(newMessage, senderId)
        messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def receivePlayerWhisperSpeedChat(self, type, messageIndex, senderId, name = None):
        # dprint("receivePlayerWhisperTypedChat %s  %s %s" %(type, messageIndex, senderId))
        error = None
        
        if (not name) and (senderId):
            name = self.findName(senderId, 1)
            
        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
            
        newMessage = TalkMessage(self.countMessage(), #messageNumber
                        self.stampTime(), #timeStamp
                        message, #message Body
                        None, #senderAvatarId
                        None, #senderAvatarName 
                        senderId, #senderAccountId
                        name, #senderAccountName
                        localAvatar.doId, #receiverAvatarId
                        localAvatar.getName(), #receiverAvatarName 
                        localAvatar.DISLid, #receiverAccountId
                        localAvatar.DISLname, #receiverAccountName
                        TALK_WHISPER, #talkType
                        None) #extraInfo

        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDISLId(newMessage, senderId)
        messenger.send("NewOpenMessage", [newMessage])
        return error
            
# SEND TALK

    def sendOpenTalk(self, message):
        error = None
        if (base.cr.wantMagicWords and
            (len(message) > 0) and (message[0] == "~")):
            messenger.send("magicWord", [message])
            self.receiveDeveloperMessage(message)
        else:
            chatFlags = CFSpeech | CFTimeout
            if self.isThought(message):
                chatFlags = CFThought
            base.localAvatar.sendUpdate("setTalk", [0, 0, "", message, [], 0])
            messenger.send("chatUpdate", [message, chatFlags])
        return error
        
    def sendWhisperTalk(self, message, receiverAvId):
        error = None
        receiver = base.cr.doId2do.get(receiverAvId)
        if receiver:
            receiver.sendUpdate("setTalkWhisper", [0, 0, "", message, [], 0])
        else:
            receiver = base.cr.identifyAvatar(receiverAvId)
            if receiver:
                base.localAvatar.sendUpdate("setTalkWhisper", [0, 0, "", message, [], 0], sendToId = receiverAvId)
            else:
                pass
        return error
        
    def sendAccountTalk(self, message, receiverAccount):
        error = None
        base.cr.playerFriendsManager.sendUpdate("setTalkAccount", [receiverAccount,0, "",message, [], 0])
        return error
        
    def sendGuildTalk(self, message):
        error = None
        if self.checkGuildTypedChat():
            # Guild chat is sent through the guildManager
            base.cr.guildManager.sendTalk(message)
        else:
            print "Guild chat error"
            error = ERROR_NO_GUILD_CHAT
        return error
        
#SEND SPEED CHAT

    def sendOpenSpeedChat(self, type, messageIndex):
        error = None
        # Open Avatar speed chat is sent through the avatar
        if type == SPEEDCHAT_NORMAL:
            messenger.send(SCChatEvent)
            messenger.send("chatUpdateSC", [messageIndex])
            base.localAvatar.b_setSC(messageIndex)

            
        elif type == SPEEDCHAT_EMOTE:
            # do these two events even do anything anymore?
            messenger.send("chatUpdateSCEmote", [messageIndex])
            messenger.send(SCEmoteChatEvent)
            base.localAvatar.b_setSCEmote(messageIndex)
            
        elif type == SPEEDCHAT_CUSTOM:
            messenger.send("chatUpdateSCCustom", [messageIndex])
            messenger.send(SCCustomChatEvent)
            base.localAvatar.b_setSCCustom(messageIndex)
            
        return error
        
    def sendAvatarWhisperSpeedChat(self,  type, messageIndex, receiverId):
        error = None

        if type == SPEEDCHAT_NORMAL:
            base.localAvatar.whisperSCTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)

            
        elif type == SPEEDCHAT_EMOTE:
            base.localAvatar.whisperSCEmoteTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, localAvatar.getName())
            
        elif type == SPEEDCHAT_CUSTOM:
            base.localAvatar.whisperSCCustomTo(messageIndex, receiverId, 0)
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)

            
        if self.logWhispers:
            avatarName = None
            accountId = None
            avatar = base.cr.identifyAvatar(receiverId)
            if avatar:
                avatarName = avatar.getName()
            
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            localAvatar.doId, #senderAvatarId
                            localAvatar.getName(), #senderAvatarName 
                            localAvatar.DISLid, #senderAccountId
                            localAvatar.DISLname, #senderAccountName
                            receiverId, #receiverAvatarId
                            avatarName, #receiverAvatarName 
                            None, #receiverAccountId
                            None, #receiverAccountName
                            TALK_WHISPER, #talkType
                            None) #extraInfo
                            
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            self.addToHistoryDISLId(newMessage, base.cr.accountDetailRecord.playerAccountId)
            messenger.send("NewOpenMessage", [newMessage])
            
        return error
        
    def sendPlayerWhisperSpeedChat(self, type, messageIndex, receiverId):
        error = None
        
        if type == SPEEDCHAT_NORMAL:
            base.cr.speedchatRelay.sendSpeedchat(receiverId, messageIndex)
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            base.cr.speedchatRelay.sendSpeedchatEmote(receiverId, messageIndex)
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, localAvatar.getName())
            return
        elif type == SPEEDCHAT_CUSTOM:
            base.cr.speedchatRelay.sendSpeedchatCustom(receiverId, messageIndex)
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
            
        if self.logWhispers:
            receiverName = self.findName(receiverId, 1)
            
            newMessage = TalkMessage(self.countMessage(), #messageNumber
                            self.stampTime(), #timeStamp
                            message, #message Body
                            localAvatar.doId, #senderAvatarId
                            localAvatar.getName(), #senderAvatarName 
                            localAvatar.DISLid, #senderAccountId
                            localAvatar.DISLname, #senderAccountName
                            None, #receiverAvatarId
                            None, #receiverAvatarName 
                            receiverId, #receiverAccountId
                            receiverName, #receiverAccountName
                            TALK_ACCOUNT, #talkType
                            None) #extraInfo
            
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            self.addToHistoryDISLId(newMessage, base.cr.accountDetailRecord.playerAccountId)
            messenger.send("NewOpenMessage", [newMessage])
        return error
        
    def sendGuildSpeedChat(self, type, msgIndex):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSC(msgIndex)
        else:
            print "Guild Speedchat error"
            error = ERROR_NO_GUILD_CHAT
        return error
        
    def getWhisperReplyId(self):
        if self.lastWhisper:
            toPlayer = 0
            if self.lastWhisper == self.lastWhisperPlayerId:
                toPlayer = 1
            return (self.lastWhisper, toPlayer)
        return (0,0)







