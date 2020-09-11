import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from pandac.PandaModules import *
from otp.chat.ChatGlobals import *
from otp.chat.TalkGlobals import *
from otp.speedchat import SpeedChatGlobals
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkAssistant import TalkAssistant
from toontown.speedchat import TTSCDecoders
import time



class TTTalkAssistant(TalkAssistant):
    """
    contains methods for turning chat inputs
    into onscreen thought/word balloons
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TTTalkAssistant")

    def __init__(self):
        TalkAssistant.__init__(self)
        
#SETUP AND CLEANUP

    def clearHistory(self):
        TalkAssistant.clearHistory(self)
        
#TOONTOWN SPECFIC SPEEDCHAT
        
    def sendPlayerWhisperToonTaskSpeedChat(self, taskId, toNpcId, toonProgress, msgIndex, receiverId):
        error = None
        
        base.cr.speedchatRelay.sendSpeedchatToonTask(receiverId, taskId, toNpcId, toonProgress, msgIndex)
        #message = SCDecoders.decodeSCCustomMsg(messageIndex)
        message = TTSCDecoders.decodeTTSCToontaskMsg(
            taskId, toNpcId, toonProgress, msgIndex)
            
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
        
    def sendToonTaskSpeedChat(self, taskId, toNpcId, toonProgress, msgIndex):
        error = None
        # Open Avatar speed chat is sent through the avatar
        messenger.send(SCChatEvent)
        messenger.send("chatUpdateSCToontask", [taskId, toNpcId, toonProgress, msgIndex])
        #base.localAvatar.b_setSCToontask(taskId, toNpcId, toonProgress, msgIndex)            
        return error
