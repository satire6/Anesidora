from direct.fsm import FSM
from otp.otpbase import OTPGlobals
import sys
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer
from direct.task import Task
from otp.chat.ChatInputTyped import ChatInputTyped

class ChatInputWhiteList(FSM.FSM, DirectEntry):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatInputWhiteList")
    
    # This will hold the local namespace we evaluate '>chat' messages
    # within.
    ExecNamespace = None

    # special methods
    def __init__(self, parent = None, **kw):
        FSM.FSM.__init__(self, 'ChatInputWhiteList')
        optiondefs = (
            ('parent', parent, None),
            ('relief', DGG.SUNKEN, None),
            ('text_scale', 0.03, None),
            ('frameSize',(-0.2, 25.3, -0.5, 1.2), None),
            ('borderWidth', (0.003, 0.003), None),
            ('frameColor', (0.9, 0.9, 0.85, 0.8), None),
            ('entryFont', OTPGlobals.getInterfaceFont(), None),
            ('width', 25, None),
            ('numLines', 1, None),
            ('cursorKeys', 1, None),
            ('backgroundFocus', 0, None),
            ('suppressKeys', 1, None),
            ('suppressMouse', 1, None),
            ('command', self.sendChat, None),
            ('failedCommand', self.sendFailed, None),
            ('focus', 0, None),
            ('text', '', None),
            )
        self.defineoptions(kw, optiondefs)
        DirectEntry.__init__(self, parent = parent, **kw)
        self.initialiseoptions(ChatInputWhiteList)

        self.whisperId = None
        #self.bind(DGG.OVERFLOW, self.chatOverflow)

        wantHistory = 0
        if __dev__:
            wantHistory = 1
        self.wantHistory = base.config.GetBool('want-chat-history', wantHistory)
        self.history = ['']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0

        self.whiteList = None
        
        self.active = 0
        self.autoOff = 0
        
        self.alwaysSubmit = False

        from direct.gui import DirectGuiGlobals
        self.bind(DirectGuiGlobals.TYPE,self.applyFilter)
        self.bind(DirectGuiGlobals.ERASE,self.applyFilter)

        tpMgr = TextPropertiesManager.getGlobalPtr()
        Red = tpMgr.getProperties('red')
        Red.setTextColor(1.0,0.0,0.0,1)
        tpMgr.setProperties('WLRed',Red)
        del tpMgr

        self.origFrameColor = self['frameColor']
        self.origTextScale = self['text_scale']
        self.origFrameSize = self['frameSize']

    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')


    def requestMode(self, mode, *args):
        """
        This is done so we can provide some symettry with
        the PChatInputSpeedChat.
        """
        self.request(mode, *args)
        
    def defaultFilter(self, request, *args):
        if request == 'AllChat':
            #if not base.chatAssistant.checkOpenSpeedChat():
            #    messenger.send("Chat-Failed open typed chat test")
            #    return None
            pass
        elif request == 'PlayerWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatPlayer(self.whisperId):
                messenger.send("Chat-Failed player typed chat test")
                return None
        elif request == 'AvatarWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatAvatar(self.whisperId):
                messenger.send("Chat-Failed avatar typed chat test")
                return None
        return FSM.FSM.defaultFilter(self, request, *args)
        

        

    def enterOff(self):
        self.deactivate()

    def exitOff(self):
        self.activate()
    
    def enterAllChat(self):
        self['focus'] = 1
        self.show()

    def exitAllChat(self):
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

    def enterShipPVPChat(self):
        self['focus'] = 1
        self.show()

    def exitShipPVPChat(self):
        pass

    def enterPlayerWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    def exitPlayerWhisper(self):
        self.set(self.tempText)
        self.whisperId = None

    def enterAvatarWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    def exitAvatarWhisper(self):
        self.set(self.tempText)
        self.whisperId = None

    def activate(self):
        self.set("")
        self['focus'] = 1
        self.show()
        self.active = 1
        self.guiItem.setAcceptEnabled(True)
        self.accept('uber-escape',self.handleEscape)
        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)
        
    def deactivate(self):
        self.ignore('uber-escape')
        self.set("")
        self['focus'] = 0
        self.hide()
        self.active = 0
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')
        
    def handleEscape(self):
        localAvatar.chatMgr.deactivateChat()
        
    def isActive(self):
        return self.active

    def _checkShouldFilter(self, text):
        """
        Should we whitelist filter this message or is it
        something special we should leave untouched?
        """
        if len(text) > 0 and text[0] in ['/']:
            return False
        else:
            return True
    
    def sendChat(self, text, overflow = False):
        """
        Send the text from the entry
        """
    
        text = self.get(plain=True)
        #print text
        # Filter out empty string
        if text:
            self.set("")
            if base.config.GetBool("exec-chat", 0) and (text[0] == '>'):
                if text[1:]:
                    # Exec a python command
                    ext = base.talkAssistant.execMessage(text[1:])
                    base.talkAssistant.receiveDeveloperMessage(text)
                    base.talkAssistant.receiveDeveloperMessage(ext)
                    base.localAvatar.setChatAbsolute(ext, CFSpeech | CFTimeout)
                    if self.wantHistory:
                        self.addToHistory(text)
                    localAvatar.chatMgr.deactivateChat()
                    localAvatar.chatMgr.activateChat()

                    #import pdb; pdb.set_trace()
                    self.set(">")
                    self.setCursorPosition(1)
                    return
                else:
                    localAvatar.chatMgr.deactivateChat()
     
            # If slash command, execute it instead of sending chat
            elif base.config.GetBool("want-slash-commands", 1) and (text[0] == '/'):
                base.talkAssistant.executeSlashCommand(text)
            elif (localAvatar.isGM() or base.cr.wantMagicWords) and (text[0] == '`'):
                base.talkAssistant.executeGMCommand(text)
            else:
                self.sendChatByMode(text)

            if self.wantHistory:
                self.addToHistory(text)
        else:
            localAvatar.chatMgr.deactivateChat()
        
        if not overflow:
            self.hide()
            if self.autoOff:
                self.requestMode('Off')
            localAvatar.chatMgr.messageSent()
            

    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send("sentRegularChat")
        if state == 'PlayerWhisper':
            base.talkAssistant.sendAccountTalk(text, self.whisperId)
        elif state == 'AvatarWhisper':
            base.talkAssistant.sendWhisperTalk(text, self.whisperId)
        else:
            base.talkAssistant.sendOpenTalk(text)

    def sendFailed(self, text):
        """
        This function is called when the user tries and fails to submit
        the chat message.  We've disabled submission because there's a
        bad word, and need to give them feedback.  For now, flash the
        field red!
        """
        self['frameColor'] = (0.9, 0.0, 0.0, 0.8)
        def resetFrameColor(task=None):
            self['frameColor'] = self.origFrameColor
            return Task.done
        taskMgr.doMethodLater(0.1,resetFrameColor,"resetFrameColor")
        # Also let them submit if they try again--we'll stomp on any violating words
        self.applyFilter(keyArgs=None,strict=False)
        self.guiItem.setAcceptEnabled(True)
        
    
    def chatOverflow(self, overflowText):
        """
        When the user types too many lines of text, an event gets thrown
        which calls this function. Right now it just sends the text just
        as if you hit return to complete the sentence.
        """
        self.sendChat(self.get(plain=True), overflow = True)
   

    ####################################
    # History functions
    def addToHistory(self, text):
        self.history = [text] + self.history[:self.historySize-1]
        self.historyIndex = 0

    def getPrevHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex += 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))
        
    def getNextHistory(self):
        self.set(self.history[self.historyIndex])
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
        self.setCursorPosition(len(self.get()))


    ####################################
    # Exec-chat functions
    def importExecNamespace(self):
        # Derived classes should take advantage of this hook to import
        # useful variables into the chat namespace for developer
        # access.
        pass
    
    def __execMessage(self, message):
        print ("_execMessage %s" % (message))
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
        text = self.get(plain=True)

        if len(text) > 0:
            if text[0] == '/':
                self.guiItem.setAcceptEnabled(True)
                return
            elif text[0] == '>' and base.config.GetBool("exec-chat", 0):
                self.guiItem.setAcceptEnabled(True)
                return
            elif text[0] == '~' and base.cr.wantMagicWords:
                self.guiItem.setAcceptEnabled(True)
                return

        words = text.split(" ")
        newwords = []
        self.notify.debug("%s" % words)

        okayToSubmit = True

        for word in words:
            if word == "" or self.whiteList.isWord(word):
                newwords.append(word)
            else:
                okayToSubmit = False
                newwords.append("\1WLEnter\1" + word + "\2")

        #if not strict:
        #    newwords[-1] = words[-1]

        if not strict:
            lastword = words[-1]

            if lastword == "" or self.whiteList.isPrefix(lastword):
                newwords[-1] = lastword
            else:
                newwords[-1] = "\1WLEnter\1" + lastword + "\2"

        self.guiItem.setAcceptEnabled((okayToSubmit or self.alwaysSubmit))
        newtext = " ".join(newwords)
        self.set(newtext)
