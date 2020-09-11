from direct.fsm import FSM
from otp.otpbase import OTPGlobals
import sys
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer
from direct.task import Task
from otp.chat.ChatInputTyped import ChatInputTyped

class ChatInputWhiteListFrame(FSM.FSM, DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatInputWhiteList")
    
    # This will hold the local namespace we evaluate '>chat' messages
    # within.
    ExecNamespace = None

    # special methods
    def __init__(self, entryOptions, parent = None, **kw):
        FSM.FSM.__init__(self, 'ChatInputWhiteListFrame')
        
        self.okayToSubmit = True
        self.receiverId = None
        DirectFrame.__init__(self,
                             parent = aspect2dp,
                             pos = (0, 0, 0.30),
                             relief = None,
                             image = DGG.getDefaultDialogGeom(),
                             image_scale = (1.6, 1, 1.4),
                             image_pos = (0,0,-0.05),
                             image_color = OTPGlobals.GlobalDialogColor,
                             borderWidth = (0.01, 0.01),
                             )
                             
        optiondefs = {
            'parent' : self,
            'relief': DGG.SUNKEN,
            'scale': 0.05,
            'frameSize' : (-0.2, 25.3, -0.5, 1.2),
            'borderWidth' : (0.1, 0.1),
            'frameColor' : (0.9, 0.9, 0.85, 0.8),
            'pos' : (-0.2,0,0.11),
            'entryFont' : OTPGlobals.getInterfaceFont(),
            'width': 8.6,
            'numLines' : 3,
            'cursorKeys' : 1,
            'backgroundFocus' : 0,
            'suppressKeys' : 1,
            'suppressMouse' : 1,
            'command' : self.sendChat,
            'failedCommand': self.sendFailed,
            'focus' : 0,
            'text' : '',
            'sortOrder' : DGG.FOREGROUND_SORT_INDEX,
            }
            
        entryOptions['parent'] = self
                             


        self.chatEntry = DirectEntry(**entryOptions)

        self.whisperId = None
        self.chatEntry.bind(DGG.OVERFLOW, self.chatOverflow)

        wantHistory = 0
        if __dev__:
            wantHistory = 1
        self.wantHistory = base.config.GetBool('want-chat-history', wantHistory)
        self.history = ['']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0
        
        self.promoteWhiteList = 0# base.config.GetBool('white-list-promotes-to-black', 0)
        self.checkBeforeSend = base.config.GetBool('white-list-check-before-send', 0)

        self.whiteList = None
        
        self.active = 0
        self.autoOff = 0
        self.sendBy = "Mode"
        self.prefilter = 1

        from direct.gui import DirectGuiGlobals
        self.chatEntry.bind(DirectGuiGlobals.TYPE,self.applyFilter)
        self.chatEntry.bind(DirectGuiGlobals.ERASE,self.applyFilter)

        tpMgr = TextPropertiesManager.getGlobalPtr()
        Red = tpMgr.getProperties('red')
        Red.setTextColor(1.0,0.0,0.0,1)
        tpMgr.setProperties('WLRed',Red)
        del tpMgr

        self.origFrameColor = self.chatEntry['frameColor']
        
    def destroy(self):
        from direct.gui import DirectGuiGlobals
        self.chatEntry.unbind(DGG.OVERFLOW)
        self.chatEntry.unbind(DirectGuiGlobals.TYPE)
        self.chatEntry.unbind(DirectGuiGlobals.ERASE)
        self.chatEntry.ignoreAll()
        DirectFrame.destroy(self)
        

    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')


    def requestMode(self, mode, *args):
        """
        This is done so we can provide some symettry with
        the PChatInputSpeedChat.
        """
        # RAU we need to return the result of the self.request
        # so toontown can do fallback to a good state if it fails
        return self.request(mode, *args)
        
    def defaultFilter(self, request, *args):
        if request == 'AllChat':
            if not base.talkAssistant.checkAnyTypedChat():
                messenger.send("Chat-Failed open typed chat test")
                self.notify.warning("Chat-Failed open typed chat test")
                return None
        elif request == 'PlayerWhisper':
            if not base.talkAssistant.checkWhisperTypedChatPlayer(self.whisperId):
                messenger.send("Chat-Failed player typed chat test")
                self.notify.warning("Chat-Failed player typed chat test")
                return None
        elif request == 'AvatarWhisper':
            if not base.talkAssistant.checkWhisperTypedChatAvatar(self.whisperId):
                messenger.send("Chat-Failed avatar typed chat test")
                self.notify.warning("Chat-Failed avatar typed chat test")
                return None
        return FSM.FSM.defaultFilter(self, request, *args)
        
    def enterOff(self):
        assert self.notify.debugStateCall(self)
        self.deactivate()
        localAvatar.chatMgr.fsm.request("mainMenu")

    def exitOff(self):
        assert self.notify.debugStateCall(self)
        self.activate()
    
    def enterAllChat(self):
        assert self.notify.debugStateCall(self)
        self.chatEntry['focus'] = 1
        self.show()

    def exitAllChat(self):
        assert self.notify.debugStateCall(self)
        pass

    def enterGuildChat(self):
        self['focus'] = 1
        self.show()

    def exitGuildChat(self):
        pass

    def enterCrewChat(self):
        self['focus'] = 1
        self.show()
    
    def exitCrewChat(self):
        pass

    def enterPlayerWhisper(self):
        assert self.notify.debugStateCall(self)
        self.tempText = self.chatEntry.get()
        self.activate()

    def exitPlayerWhisper(self):
        assert self.notify.debugStateCall(self)
        self.chatEntry.set(self.tempText)
        self.whisperId = None

    def enterAvatarWhisper(self):
        assert self.notify.debugStateCall(self)                
        self.tempText = self.chatEntry.get()
        self.activate()

    def exitAvatarWhisper(self):
        assert self.notify.debugStateCall(self)        
        self.chatEntry.set(self.tempText)
        self.whisperId = None
        
    def activateByData(self, receiverId = None, toPlayer = 0):
        """Return None if something went wrong, otherwise return the some info on the new state."""
        assert self.notify.debugStateCall(self)
        self.receiverId = receiverId
        self.toPlayer = toPlayer
        result = None
        if not self.receiverId:
            result = self.requestMode("AllChat")
        elif self.receiverId and not self.toPlayer:
            self.whisperId = receiverId
            result = self.requestMode("AvatarWhisper")
        elif self.receiverId and self.toPlayer:
            self.whisperId = receiverId
            result = self.requestMode("PlayerWhisper")
        return result
        

    def activate(self):
        #self.chatEntry.set("")
        assert self.notify.debugStateCall(self)
        self.chatEntry['focus'] = 1
        self.show()
        self.active = 1
        self.chatEntry.guiItem.setAcceptEnabled(False)
        
    def deactivate(self):
        assert self.notify.debugStateCall(self)
        self.chatEntry.set("")
        self.chatEntry['focus'] = 0
        self.hide()
        self.active = 0
        
    def isActive(self):
        return self.active
    
    def sendChat(self, text, overflow = False):
        """
        Send the text from the entry
        """
        # Filter if we're not doing exec or magic word
        if not (len(text) > 0 and text[0] in ['~','>']):
            if self.prefilter:
                words = text.split(" ")
                newwords = []
                for word in words:
                    if word == "" or self.whiteList.isWord(word) or self.promoteWhiteList:
                        newwords.append(word)
                    else:
                        newwords.append(base.whiteList.defaultWord)
                        
                text = " ".join(newwords)
            else:
                text = self.chatEntry.get(plain=True)

        # Filter out empty string
        if text:
            self.chatEntry.set("")

            if base.config.GetBool("exec-chat", 0) and (text[0] == '>'):
                    # Exec a python command
                    text = self.__execMessage(text[1:])
                    base.localAvatar.setChatAbsolute(text, CFSpeech | CFTimeout)
                    return
            else:
                self.sendChatBySwitch(text)

            if self.wantHistory:
                self.addToHistory(text)
        else:
            localAvatar.chatMgr.deactivateChat()
        
        if not overflow:
            self.hide()
            if self.autoOff:
                self.requestMode('Off')
            localAvatar.chatMgr.messageSent()
            
    def sendChatBySwitch(self, text):
        if len(text) > 0 and text[0] == '~':
            base.talkAssistant.sendOpenTalk(text)
        elif self.sendBy == "Mode":
            self.sendChatByMode(text)
        elif self.sendBy == "Data":
            self.sendChatByData(text)
        else:
            self.sendChatByMode(text)
            
    def sendChatByData(self, text):
        if not self.receiverId:
            base.talkAssistant.sendOpenTalk(text)
        elif self.receiverId and not self.toPlayer:
            base.talkAssistant.sendWhisperTalk(text, self.receiverId)
        elif self.receiverId and self.toPlayer:
            base.talkAssistant.sendAccountTalk(text, self.receiverId)
       

    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send("sentRegularChat")
        if state == 'PlayerWhisper':
            base.talkAssistant.sendPlayerWhisperWLChat(text, self.whisperId)
        elif state == 'AvatarWhisper':
            base.talkAssistant.sendAvatarWhisperWLChat(text, self.whisperId)
        elif state == 'GuildChat':
            base.talkAssistant.sendAvatarGuildWLChat(text)
        elif state == 'CrewChat':
            base.talkAssistant.sendAvatarCrewWLChat(text)
        # Temporary hack for magic words
        elif len(text) > 0 and text[0] == '~':
            base.talkAssistant.sendOpenTalk(text)
        else:
            base.talkAssistant.sendOpenTalk(text)

    def sendFailed(self, text):
        """
        This function is called when the user tries and fails to submit
        the chat message.  We've disabled submission because there's a
        bad word, and need to give them feedback.  For now, flash the
        field red!
        """
        if not self.checkBeforeSend:
            self.sendChat(text)
            return
            
        self.chatEntry['frameColor'] = (0.9, 0.0, 0.0, 0.8)
        def resetFrameColor(task=None):
            self.chatEntry['frameColor'] = self.origFrameColor
            return Task.done
        taskMgr.doMethodLater(0.1,resetFrameColor,"resetFrameColor")
        # Also let them submit if they try again--we'll stomp on any violating words
        self.applyFilter(keyArgs=None,strict=True)
        self.okayToSubmit = True
        self.chatEntry.guiItem.setAcceptEnabled(True)
       
        
    
    def chatOverflow(self, overflowText):
        """
        When the user types too many lines of text, an event gets thrown
        which calls this function. Right now it just sends the text just
        as if you hit return to complete the sentence.
        """
        self.notify.debug('chatOverflow')
        self.sendChat(self.chatEntry.get(plain=True), overflow = True)
   

    ####################################
    # History functions
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


    ####################################
    # Exec-chat functions
    def importExecNamespace(self):
        # Derived classes should take advantage of this hook to import
        # useful variables into the chat namespace for developer
        # access.
        pass
    
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

    def applyFilter(self,keyArgs,strict=False):
        text = self.chatEntry.get(plain=True)

        if len(text) > 0 and text[0] in ['~','>']:
            self.okayToSubmit = True
        else:
            words = text.split(" ")
            newwords = []
            self.notify.debug("%s" % words)
    
            self.okayToSubmit = True
    
            for word in words:
                if word == "" or self.whiteList.isWord(word):
                    newwords.append(word)
                else:
                    if self.checkBeforeSend:
                        self.okayToSubmit = False
                    else:
                        self.okayToSubmit = True
                    newwords.append("\1WLEnter\1" + word + "\2")
    
            if not strict:
                lastword = words[-1]
    
                if lastword == "" or self.whiteList.isPrefix(lastword):
                    newwords[-1] = lastword
                else:
                    newwords[-1] = "\1WLEnter\1" + lastword + "\2"
                    
            newtext = " ".join(newwords)
            self.chatEntry.set(newtext)

        self.chatEntry.guiItem.setAcceptEnabled(self.okayToSubmit)

