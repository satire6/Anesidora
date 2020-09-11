"""ChatInputTyped module: contains the ChatInputTyped class"""

from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
import sys
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer

class ChatInputTyped(DirectObject.DirectObject):
    """ChatInputTyped class: controls the chat input bubble, and handles
    chat message construction"""

    # This will hold the local namespace we evaluate '>chat' messages
    # within.
    ExecNamespace = None

    # special methods
    def __init__(self, mainEntry = 0):        
        self.whisperName = None
        self.whisperId = None
        self.toPlayer = 0
        self.mainEntry = mainEntry

        wantHistory = 0
        if __dev__:
            wantHistory = 1
        self.wantHistory = base.config.GetBool('want-chat-history', wantHistory)
        self.history = ['']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0

        # It is up to a derived class, like ChatInputTyped, to
        # define self.chatFrame, self.chatButton, self.cancelButton,
        # and self.whisperLabel.


    def typeCallback(self, extraArgs):
        self.activate()

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
        

    def show(self, whisperId = None, toPlayer = 0):
        self.toPlayer = toPlayer
        self.whisperId = whisperId
        self.whisperName = None
        
        if self.whisperId:
            self.whisperName = base.talkAssistant.findName(whisperId, toPlayer)
            if hasattr(self, "whisperPos"):
                self.chatFrame.setPos(self.whisperPos)
            self.whisperLabel["text"] = (OTPLocalizer.ChatInputWhisperLabel %
                                         (self.whisperName))
            self.whisperLabel.show()
        else:
            if hasattr(self, "normalPos"):
                self.chatFrame.setPos(self.normalPos)
            self.whisperLabel.hide()
            
        self.chatEntry['focus'] = 1
        self.chatEntry.set("")
        self.chatFrame.show()
        self.chatEntry.show()
        self.cancelButton.show()
        self.typedChatButton.hide()
        self.typedChatBar.hide()

        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)

    def hide(self):
        #import pdb; pdb.set_trace()
        self.chatEntry.set("")
        self.chatEntry['focus'] = 0
        self.chatFrame.hide()
        self.chatEntry.hide()
        self.cancelButton.hide()
        self.typedChatButton.show()
        self.typedChatBar.show()
        #base.win.closeIme()
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')
        
    def activate(self):
        self.chatEntry.set("")
        self.chatEntry['focus'] = 1
        self.chatFrame.show()
        self.chatEntry.show()
        self.cancelButton.show()
        self.typedChatButton.hide()
        self.typedChatBar.hide()
        if self.whisperId:
            print("have id")
            if self.toPlayer:
                if not base.talkAssistant.checkWhisperTypedChatPlayer(self.whisperId):
                    messenger.send("Chat-Failed player typed chat test")
                    self.deactivate()
            else:
                if not base.talkAssistant.checkWhisperTypedChatAvatar(self.whisperId):   
                    messenger.send("Chat-Failed avatar typed chat test")
                    self.deactivate()
        else:
            if not base.talkAssistant.checkOpenTypedChat():
                messenger.send("Chat-Failed open typed chat test")
                self.deactivate()
             

            
        
    def deactivate(self):
        self.chatEntry.set("")
        self.chatEntry['focus'] = 0
        self.chatFrame.show()
        self.chatEntry.hide()
        self.cancelButton.hide()
        self.typedChatButton.show()
        self.typedChatBar.show()
        
        
    
    def sendChat(self, text):
        """
        Send the text from the entry
        """
        # Done for now, go away
        self.deactivate()
        #self.chatMgr.fsm.request("mainMenu")
        #print("type send chat id %s toplayer %s" % (self.whisperId, self.toPlayer))

        # Filter out empty string
        if text:
            if self.toPlayer:
                if self.whisperId:
                    #base.chatAssistant.sendPlayerWhisperTypedChat(text, self.whisperId)
                    #self.whisperName = None
                    #self.whisperId = None
                    #self.toPlayer = 0
                    pass
                    
            elif self.whisperId:
                #base.chatAssistant.sendAvatarWhisperTypedChat(text, self.whisperId)
                #self.whisperName = None
                #self.whisperId = None
                pass
            elif base.config.GetBool("exec-chat", 0) and (text[0] == '>'):
                    # Exec a python command
                    text = self.__execMessage(text[1:])
                    base.localAvatar.setChatAbsolute(text, CFSpeech | CFTimeout)
                    return
            else:
                #self.chatMgr.sendChatString(text)
                base.talkAssistant.sendOpenTalk(text)

            if self.wantHistory:
                self.addToHistory(text)
        self.chatEntry.set("")

    def chatOverflow(self, overflowText):
        """
        When the user types too many lines of text, an event gets thrown
        which calls this function. Right now it just sends the text just
        as if you hit return to complete the sentence.
        """
        self.sendChat(self.chatEntry.get())

    def __execMessage(self, message):
        if not ChatInputTyped.ExecNamespace:
            # Import some useful variables into the ExecNamespace initially.
            ChatInputTyped.ExecNamespace = { }
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
            self.importExecNamespace()

        # Now try to evaluate the expression using ChatInputTyped.ExecNamespace as
        # the local namespace.
        try:
            return str(eval(message, globals(), ChatInputTyped.ExecNamespace))

        except SyntaxError:
            # Maybe it's only a statement, like "x = 1", or
            # "import math".  These aren't expressions, so eval()
            # fails, but they can be exec'ed.
            try:
                exec message in globals(), ChatInputTyped.ExecNamespace
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
        self.deactivate()
        #self.chatMgr.fsm.request("mainMenu")

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

    
