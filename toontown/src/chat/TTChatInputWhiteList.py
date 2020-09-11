#from direct.gui.DirectGui import *
#from otp.otpbase import OTPGlobals
from otp.chat.ChatInputWhiteListFrame import ChatInputWhiteListFrame
from toontown.chat.TTWhiteList import TTWhiteList

from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
import sys
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class TTChatInputWhiteList(ChatInputWhiteListFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory("TTChatInputWhiteList")

    TFToggleKey = base.config.GetString('true-friend-toggle-key','alt')
    TFToggleKeyUp = TFToggleKey + '-up'

    def __init__(self, parent = None, **kw):
        entryOptions = {
            'parent' : self,
            'relief': DGG.SUNKEN,
            'scale': 0.05,
            #'frameSize' : (-0.2, 25.3, -0.5, 1.2),
            #'borderWidth' : (0.1, 0.1),
            'frameColor' : (0.9, 0.9, 0.85, 0.0),
            'pos' : (-0.2,0,0.11),
            'entryFont' : OTPGlobals.getInterfaceFont(),
            'width': 8.6,
            'numLines' : 3,
            'cursorKeys' : 0,
            'backgroundFocus' : 0,
            'suppressKeys' : 0,
            'suppressMouse' : 1,
            'command' : self.sendChat,
            'failedCommand': self.sendFailed,
            'focus' : 0,
            'text' : '',
            'sortOrder' : DGG.FOREGROUND_SORT_INDEX,
            }
        ChatInputWhiteListFrame.__init__(self, entryOptions, parent, **kw)
        #self.initialiseoptions(TTChatInputWhiteList)
        self.whiteList = TTWhiteList()
        base.whiteList = self.whiteList
        base.ttwl = self
        
        
        self.autoOff = 1
        self.sendBy = "Data"
        self.prefilter = 0
        self.promoteWhiteList = 1
        self.typeGrabbed = 0
        
        #self.request("off")
        self.deactivate()
        
        gui = loader.loadModel("phase_3.5/models/gui/chat_input_gui")
        
        self.chatFrame = DirectFrame(
            parent = self,
            image = gui.find("**/Chat_Bx_FNL"),
            relief = None,
            pos = (0.0, 0, 0.0),
            state = DGG.NORMAL,
            #sortOrder = DGG.FOREGROUND_SORT_INDEX,
            )

        #self.chatFrame.hide()

        self.chatButton = DirectButton(
            parent = self.chatFrame,
            image = (gui.find("**/ChtBx_ChtBtn_UP"),
                     gui.find("**/ChtBx_ChtBtn_DN"),
                     gui.find("**/ChtBx_ChtBtn_RLVR"),
                     ),
            pos = (0.182, 0, -0.088),
            relief = None,
            text = ("",
                    OTPLocalizer.ChatInputNormalSayIt,
                    OTPLocalizer.ChatInputNormalSayIt),
            text_scale = 0.06,
            text_fg = Vec4(1,1,1,1),
            text_shadow = Vec4(0,0,0,1),
            text_pos = (0,-0.09),
            textMayChange = 0,
            command = self.chatButtonPressed,
            )

        self.cancelButton = DirectButton(
            parent = self.chatFrame,
            image = (gui.find("**/CloseBtn_UP"),
                     gui.find("**/CloseBtn_DN"),
                     gui.find("**/CloseBtn_Rllvr"),
                     ),
            pos = (-0.151, 0, -0.088),                            
            relief = None,
            text = ("",
                    OTPLocalizer.ChatInputNormalCancel,
                    OTPLocalizer.ChatInputNormalCancel),
            text_scale = 0.06,
            text_fg = Vec4(1,1,1,1),
            text_shadow = Vec4(0,0,0,1),
            text_pos = (0,-0.09),
            textMayChange = 0,
            command = self.cancelButtonPressed,
            )

        self.whisperLabel = DirectLabel(
            parent = self.chatFrame,
            pos = (0.02, 0, 0.23),
            relief = DGG.FLAT,
            frameColor = (1,1,0.5,1),
            frameSize = (-0.23, 0.23, -0.07, 0.05),
            text = OTPLocalizer.ChatInputNormalWhisper,
            text_scale = 0.04,
            text_fg = Vec4(0,0,0,1),
            text_wordwrap = 9.5,
            textMayChange = 1,
            )
        #self.whisperLabel.hide()
        #self.setPos(-0.35, 0.0, 0.7)
        
        self.chatEntry.bind(DGG.OVERFLOW, self.chatOverflow)
        self.chatEntry.bind(DGG.TYPE, self.typeCallback)
        # self.accept("typeEntryGrab", self.handleTypeGrab)
        
        self.trueFriendChat = 0
        if  base.config.GetBool('whisper-to-nearby-true-friends', 1):
            self.accept(self.TFToggleKey, self.shiftPressed)
        
    ## Maintain state of shift key
    def shiftPressed(self):
        """
        Helps maintain the value of the shift key
        so that if it is pressed while sending chat,
        then the chat becomes a whisper to true friends
        in the same zone
        """
        
        assert self.notify.debug('shiftPressed %s' % self.desc)
        self.ignore(self.TFToggleKey)
        self.trueFriendChat = 1
        self.accept(self.TFToggleKeyUp, self.shiftReleased)
        
    def shiftReleased(self):
        """
        Helps maintain the value of the shift key
        so that if it is pressed while sending chat,
        then the chat becomes a whisper to true friends
        in the same zone
        """
        assert self.notify.debug('shiftReleased')
        self.ignore(self.TFToggleKeyUp)
        self.trueFriendChat = 0
        self.accept(self.TFToggleKey, self.shiftPressed)
           
    def handleTypeGrab(self):
        assert self.notify.debug("handleTypeGrab %s" % self.desc)
        self.ignore("typeEntryGrab")
        self.accept("typeEntryRelease", self.handleTypeRelease)
        #self.chatEntry['focus'] = 0
        self.typeGrabbed = 1
        
    def handleTypeRelease(self):
        assert self.notify.debug("handleTypeRelease"  % self.desc)
        self.ignore("typeEntryRelease")
        self.accept("typeEntryGrab", self.handleTypeGrab)
        #self.chatEntry['focus'] = 1
        self.typeGrabbed = 0
        
    def typeCallback(self, extraArgs):
        #if hasattr(base, "whiteList"):
        #    if base.whiteList:
        #        return
        #print("enterNormalChat")
        if self.typeGrabbed:
            return
        
        self.applyFilter(extraArgs)
        if localAvatar.chatMgr.chatInputWhiteList.isActive():
            #print("typeCallback return")
            return
        else:
            #print("send")
            #print self.chatEntry['text']
            messenger.send("wakeup")
            messenger.send('enterNormalChat')
            
    def destroy(self):
        self.chatEntry.destroy()
        self.chatFrame.destroy()
        self.ignoreAll()
        ChatInputWhiteListFrame.destroy(self)
            
        
    def delete(self):
        base.whiteList = None
        ChatInputWhiteListFrame.delete(self)
        
    def sendChat(self, text, overflow = False):
        assert self.notify.debug('sendChat')
        if self.typeGrabbed:
            return
        else:
            ChatInputWhiteListFrame.sendChat(self, self.chatEntry.get())
            
    def sendChatByData(self, text):
        assert self.notify.debug('sendChatByData desc=%s tfChat=%s' % (self.desc,self.trueFriendChat))
        if self.trueFriendChat:            
            for friendId, flags in base.localAvatar.friendsList:
                if flags & ToontownGlobals.FriendChat:
                    self.sendWhisperByFriend(friendId, text)
        elif not self.receiverId:
            base.talkAssistant.sendOpenTalk(text)
        elif self.receiverId and not self.toPlayer:
            base.talkAssistant.sendWhisperTalk(text, self.receiverId)
        elif self.receiverId and self.toPlayer:
            base.talkAssistant.sendAccountTalk(text, self.receiverId)
            
    def sendWhisperByFriend(self, avatarId, text):
        """
        Check whether it is appropriate to send a message to the true
        friend avatarId and then send it.
        """
        online = 0
        if base.cr.doId2do.has_key(avatarId):
            # The avatar is online, and in fact, nearby.
            online = 1
            
        # Uncomment the following section of code if it is required to
        # send whispers to all true friends regardless of zone
##        elif base.cr.isFriend(avatarId):
##            # The avatar is a friend of ours.  Is she online?
##            online = base.cr.isFriendOnline(avatarId)
##
##        hasManager = hasattr(base.cr, "playerFriendsManager")
##        if hasManager:
##            if base.cr.playerFriendsManager.askAvatarOnline(avatarId):
##               online = 1

        # Do we have chat permission with the other avatar?
        avatarUnderstandable = 0
        av = None
        if avatarId:
            av = base.cr.identifyAvatar(avatarId)
        if av != None:
            avatarUnderstandable = av.isUnderstandable()
            
        # To do: find out how to access chat manager from here
        # normalButtonObscured, scButtonObscured = self.isObscured()

        if avatarUnderstandable and online:
        # and not normalButtonObscured:
            base.talkAssistant.sendWhisperTalk(text, avatarId)
        
    def chatButtonPressed(self):
        print("chatButtonPressed")
        if self.okayToSubmit:
            #self.chatEntry.commandFunc(None)
            self.sendChat(self.chatEntry.get())
        else:
            #self.chatEntry.failedCommandFunc(None)
            self.sendFailed(self.chatEntry.get())
            
        
    def cancelButtonPressed(self):
        self.requestMode("Off")
        
        localAvatar.chatMgr.fsm.request("mainMenu")
        
    def enterAllChat(self):
        #print("enterAllChat")
        ChatInputWhiteListFrame.enterAllChat(self)
        self.whisperLabel.hide()
        

    def exitAllChat(self):
        #print("exitAllChat")
        ChatInputWhiteListFrame.exitAllChat(self)
        
    def enterPlayerWhisper(self):
        ChatInputWhiteListFrame.enterPlayerWhisper(self)
        #self.whisperLabel.show()
        self.labelWhisper()

    def exitPlayerWhisper(self):
        ChatInputWhiteListFrame.exitPlayerWhisper(self)
        self.whisperLabel.hide()
        
    def enterAvatarWhisper(self):
        #print("enterAvatarWhisper")
        ChatInputWhiteListFrame.enterAvatarWhisper(self)
        #self.whisperLabel.show()
        self.labelWhisper()

    def exitAvatarWhisper(self):
        #print("exitAvatarWhisper")
        ChatInputWhiteListFrame.exitAvatarWhisper(self)
        self.whisperLabel.hide()
        
    def labelWhisper(self):
        if self.receiverId:
            self.whisperName = base.talkAssistant.findName(self.receiverId, self.toPlayer)
            self.whisperLabel["text"] = (OTPLocalizer.ChatInputWhisperLabel %
                                         (self.whisperName))
            self.whisperLabel.show()
        else:
            self.whisperLabel.hide()
            
    def applyFilter(self,keyArgs,strict=False):
        text = self.chatEntry.get(plain=True)

        if len(text) > 0 and text[0] in ['~','>']:
            self.okayToSubmit = True
        else:
            words = text.split(" ")
            newwords = []
            assert self.notify.debug("%s" % words)

            self.okayToSubmit = True
            
            # If we are true friends then we should italacize bad text
            flag = 0
            for friendId, flags in base.localAvatar.friendsList:
                if flags & ToontownGlobals.FriendChat:
                    flag = 1

            for word in words:
                if word == "" or self.whiteList.isWord(word) or (not base.cr.whiteListChatEnabled):
                    newwords.append(word)
                else:
                    if self.checkBeforeSend:
                        self.okayToSubmit = False
                    else:
                        self.okayToSubmit = True
                    if flag:
                        newwords.append("\1WLDisplay\1" + word + "\2")
                    else:
                        newwords.append("\1WLEnter\1" + word + "\2")

            if not strict:
                lastword = words[-1]

                if lastword == "" or self.whiteList.isPrefix(lastword) or (not base.cr.whiteListChatEnabled):
                    newwords[-1] = lastword
                else:
                    if flag:
                        newwords[-1] = "\1WLDisplay\1" + lastword + "\2"
                    else:
                        newwords[-1] = "\1WLEnter\1" + lastword + "\2"

            newtext = " ".join(newwords)
            self.chatEntry.set(newtext)

        self.chatEntry.guiItem.setAcceptEnabled(self.okayToSubmit)
        
