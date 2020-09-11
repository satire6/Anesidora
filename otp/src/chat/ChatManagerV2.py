"""
ChatManagerV2 module: contains the ChatManagerV2 class

ChatManagerV2 varies from the orginal chat manager in that it is only responsible for chat
warnings. Chat sending is handled by the talkAssistant. This was done so that the GUI and 
logic could be free of each other
"""

import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from otp.login import SecretFriendsInfoPanel
from otp.login import PrivacyPolicyPanel
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.login import LeaveToPayDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm.FSM import FSM


class ChatManagerV2(DirectObject.DirectObject):
    """
    contains methods for turning chat inputs
    into onscreen thought/word balloons
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatManagerV2")

    # special methods
    def __init__(self):
        self.openChatWarning = None
        self.unpaidChatWarning = None
        self.teaser = None
        self.paidNoParentPassword = None
        self.noSecretChatAtAll = None
        self.noSecretChatWarning = None
        self.chatMoreInfo = None
        self.chatPrivacyPolicy = None
        self.secretChatActivated = None
        self.problemActivatingChat = None
        self.leaveToPayDialog = None
        
        self.fsm = ClassicFSM.ClassicFSM(
            'chatManager', [
                State.State("off",
                            self.enterOff,
                            self.exitOff),
                State.State("mainMenu",
                            self.enterMainMenu,
                            self.exitMainMenu),
                State.State("openChatWarning",
                            self.enterOpenChatWarning,
                            self.exitOpenChatWarning),
                State.State("leaveToPayDialog",
                            self.enterLeaveToPayDialog,
                            self.exitLeaveToPayDialog),
                State.State("unpaidChatWarning",
                            self.enterUnpaidChatWarning,
                            self.exitUnpaidChatWarning),
                State.State("noSecretChatAtAll",
                            self.enterNoSecretChatAtAll,
                            self.exitNoSecretChatAtAll),
                State.State("noSecretChatWarning",
                            self.enterNoSecretChatWarning,
                            self.exitNoSecretChatWarning),
                State.State("noFriendsWarning",
                            self.enterNoFriendsWarning,
                            self.exitNoFriendsWarning),
                State.State("otherDialog",
                            self.enterOtherDialog,
                            self.exitOtherDialog),
                State.State("activateChat",
                            self.enterActivateChat,
                            self.exitActivateChat),
                State.State("chatMoreInfo",
                            self.enterChatMoreInfo,
                            self.exitChatMoreInfo),
                State.State("chatPrivacyPolicy",
                            self.enterChatPrivacyPolicy,
                            self.exitChatPrivacyPolicy),
                State.State("secretChatActivated",
                            self.enterSecretChatActivated,
                            self.exitSecretChatActivated),
                State.State("problemActivatingChat",
                            self.enterProblemActivatingChat,
                            self.exitProblemActivatingChat),
                ],
                "off",
                "off",
                )
        self.fsm.enterInitialState()
        
        self.accept("Chat-Failed open typed chat test", self.__handleFailOpenTypedChat)
        self.accept("Chat-Failed player typed chat test", self.__handleFailPlayerTypedWhsiper)
        self.accept("Chat-Failed avatar typed chat test", self.__handleFailAvatarTypedWhsiper)
        
    def delete(self):
        self.ignoreAll()
        del self.fsm
        
    def __handleFailOpenTypedChat(self, caller = None):
        self.fsm.request("openChatWarning")
        
    def __handleFailPlayerTypedWhsiper(self, caller = None):
        self.fsm.request("noSecretChatWarning")
        
    def __handleFailAvatarTypedWhsiper(self, caller = None):
        self.fsm.request("noSecretChatWarning")
        
    def __handleLeaveToPayCancel(self):
        assert self.notify.debugStateCall(self)
        self.fsm.request("mainMenu")
    
    def __secretFriendsInfoDone(self):
        assert self.notify.debugStateCall(self)
        self.fsm.request("activateChat")

    def __privacyPolicyDone(self):
        assert self.notify.debugStateCall(self)
        self.fsm.request("activateChat")
        
    def enterOff(self):
        assert self.notify.debugStateCall(self)
        self.ignoreAll()

    def exitOff(self):
        assert self.notify.debugStateCall(self)
        pass
        
    def enterOtherDialog(self):
        assert self.notify.debugStateCall(self)
        
    def exitOtherDialog(self):
        assert self.notify.debugStateCall(self)
        

    def enterUnpaidChatWarning(self):
        self.notify.error("called enterUnpaidChatWarning() on parent class")
        pass

    def exitUnpaidChatWarning(self):
        self.notify.error("called exitUnpaidChatWarning() on parent class")
        pass
        
    def enterNoFriendsWarning(self):
        self.notify.error("called enterNoFriendsWarning() on parent class")
        pass
        
    def exitNoFriendsWarning(self):
        self.notify.error("called exitNoFriendsWarning() on parent class")
        pass
        
    def enterSecretChatActivated(self):
        self.notify.error("called enterSecretChatActivated() on parent class")
        pass
        
    def exitSecretChatActivated(self):
        self.notify.error("called exitSecretChatActivated() on parent class")
        pass

    def enterProblemActivatingChat(self):
        self.notify.error("called enterProblemActivatingChat() on parent class")
        pass
        
    def exitProblemActivatingChat(self):
        self.notify.error("called exitProblemActivatingChat() on parent class")
        pass
        
    def enterChatPrivacyPolicy(self):
        """
        A dialog with lots of information about what it means to
        enable secret friends.
        """
        self.notify.error("called enterChatPrivacyPolicy() on parent class")
        pass
        
    def exitChatPrivacyPolicy(self):
        self.notify.error("called exitChatPrivacyPolicy() on parent class")
        pass
        
    def enterChatMoreInfo(self):
        """
        A dialog with lots of information about what it means to
        enable secret friends.
        """
        self.notify.error("called enterChatMoreInfo() on parent class")
        pass
        
    def exitChatMoreInfo(self):
        self.notify.error("called exitChatMoreInfo() on parent class")
        pass
        
    def enterNoSecretChatWarning(self):
        self.notify.error("called enterNoSecretChatWarning() on parent class")
        pass
        
    def exitNoSecretChatWarning(self):
        self.notify.error("called exitNoSecretChatWarning() on parent class")
        pass
        
    def enterLeaveToPayDialog(self):
        """
        Tell the user that we will exit the 3D client and take
        them to a web page.
        """
        self.notify.error("called enterLeaveToPayDialog() on parent class")
        pass

    def exitLeaveToPayDialog(self):
        self.notify.error("called exitLeaveToPayDialog() on parent class")
        pass

