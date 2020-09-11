"""ChatInputNormal module: contains the ChatInputNormal class"""

from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
import sys
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer

class ChatInputNormal(DirectObject.DirectObject):
    """ChatInputNormal class: controls the chat input bubble, and handles
    chat message construction"""

    # This will hold the local namespace we evaluate '>chat' messages
    # within.
    ExecNamespace = None

    # special methods
    def __init__(self, chatMgr):
        self.chatMgr = chatMgr

        self.normalPos = Vec3(-1.083, 0, 0.804)
        self.whisperPos = Vec3(0.0, 0, 0.71)
        
        self.whisperAvatarName = None
        self.whisperAvatarId = None
        self.toPlayer = 0

        wantHistory = 0
        if __dev__:
            wantHistory = 1
        self.wantHistory = base.config.GetBool('want-chat-history', wantHistory)
        self.history = ['']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0

        # It is up to a derived class, like TTChatInputNormal, to
        # define self.chatFrame, self.chatButton, self.cancelButton,
        # and self.whisperLabel.


    def typeCallback(self, extraArgs):
        messenger.send('enterNormalChat')

    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')
        self.chatFrame.destroy()
        del self.chatFrame
        del self.chatButton
        del self.cancelButton
        del self.chatEntry
        del self.whisperLabel
        del self.chatMgr

    def activateByData(self, whisperAvatarId = None, toPlayer = 0):
        self.toPlayer = toPlayer
        self.whisperAvatarId = whisperAvatarId
        self.whisperAvatarName = base.talkAssistant.findName(self.whisperAvatarId, self.toPlayer)
        if self.whisperAvatarId:
            self.chatFrame.setPos(self.whisperPos)
            self.whisperLabel["text"] = (OTPLocalizer.ChatInputWhisperLabel %
                                         (self.whisperAvatarName))
            self.whisperLabel.show()
        else:
            self.chatFrame.setPos(self.normalPos)
            self.whisperLabel.hide()
        self.chatEntry['focus'] = 1
        self.chatFrame.show()

        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)

    def deactivate(self):
        self.chatEntry.set("")
        self.chatEntry['focus'] = 0
        self.chatFrame.hide()
        self.whisperLabel.hide()
        base.win.closeIme()
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')
        
    def checkForOverRide(self):
        #ChatInputNormal likes to intercept other direct entries
        #too much was hard wired to the chatManagar so I'm adding a final stage override - JML
        return False
    
    def sendChat(self, text):
        """
        Send the text from the entry
        """
        if self.checkForOverRide():
            self.chatEntry.enterText("")
            return
        # Done for now, go away
        self.deactivate()
        self.chatMgr.fsm.request("mainMenu")

        # Filter out empty string
        if text:
            if self.toPlayer:
                if self.whisperAvatarId:
                    #base.cr.playerFriendsManager.sendWhisper(self.whisperAvatarId, text)
                    #base.chatAssistant.sendPlayerWhisperTypedChat(text, self.whisperAvatarId)
                    self.whisperAvatarName = None
                    self.whisperAvatarId = None
                    self.toPlayer = 0
                    
            elif self.whisperAvatarId:
                self.chatMgr.sendWhisperString(text, self.whisperAvatarId)
                self.whisperAvatarName = None
                self.whisperAvatarId = None
            else:
                if self.chatMgr.execChat:
                    # Exec a python command
                    if (text[0] == '>'):
                        text = self.__execMessage(text[1:])
                        base.localAvatar.setChatAbsolute(text, CFSpeech | CFTimeout)
                        return

                base.talkAssistant.sendOpenTalk(text)

                if self.wantHistory:
                    self.addToHistory(text)

    def chatOverflow(self, overflowText):
        """
        When the user types too many lines of text, an event gets thrown
        which calls this function. Right now it just sends the text just
        as if you hit return to complete the sentence.
        """
        self.sendChat(self.chatEntry.get())

    def __execMessage(self, message):
        if not ChatInputNormal.ExecNamespace:
            # Import some useful variables into the ExecNamespace initially.
            ChatInputNormal.ExecNamespace = { }
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
            self.importExecNamespace()

        # Now try to evaluate the expression using ChatInputNormal.ExecNamespace as
        # the local namespace.
        try:
            return str(eval(message, globals(), ChatInputNormal.ExecNamespace))

        except SyntaxError:
            # Maybe it's only a statement, like "x = 1", or
            # "import math".  These aren't expressions, so eval()
            # fails, but they can be exec'ed.
            try:
                exec message in globals(), ChatInputNormal.ExecNamespace
                return 'ok'
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

    # button event handlers
    def cancelButtonPressed(self):
        self.chatEntry.set("")
        self.chatMgr.fsm.request("mainMenu")

    def chatButtonPressed(self):
        self.sendChat(self.chatEntry.get())
    
    def importExecNamespace(self):
        # Derived classes should take advantage of this hook to import
        # useful variables into the chat namespace for developer
        # access.
        pass

    def addToHistory(self, text):
        self.history = [text] + self.history[:self.historySize-1]
        self.historyIndex = 0

    def getPrevHistory(self):
        self.chatEntry.set(self.history[self.historyIndex])
        self.historyIndex += 1
        self.historyIndex %= len(self.history)
        
    def getNextHistory(self):
        self.chatEntry.set(self.history[self.historyIndex])
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
        
    def setPos(self, posX, posY = None, posZ = None):
        if posX and posY and posZ:
            self.chatFrame.setPos(posX,posY,posZ)
        else:
            self.chatFrame.setPos(posX)
            

    
