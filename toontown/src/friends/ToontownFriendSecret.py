from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer

# This file overrides key methods in FriendSecret to add Toontown specific text to the OTP buttons

from otp.friends.FriendSecret import AccountSecret
from otp.friends.FriendSecret import AvatarSecret
from otp.friends.FriendSecret import BothSecrets

from otp.friends import FriendSecret
from otp.friends.FriendSecret import globalFriendSecret
from otp.friends.FriendSecret import showFriendSecret
from otp.friends.FriendSecret import hideFriendSecret
from otp.friends.FriendSecret import unloadFriendSecret


def openFriendSecret(secretType):
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
    globalFriendSecret = ToontownFriendSecret(secretType)
    globalFriendSecret.enter()

# there is no way to overload module level methods, so hammer it in
FriendSecret.openFriendSecret = openFriendSecret

class ToontownFriendSecret(FriendSecret.FriendSecret):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownFriendSecret")

    def __init__(self, secretType):
        #secretType is specefied in toon/ToonAvatarPanel.py-> __handleSecrets(self):
        FriendSecret.FriendSecret.__init__(self, secretType)
        self.initialiseoptions(ToontownFriendSecret)
        
    def makeFriendTypeButtons(self):
        assert self.notify.debugCall()

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')

        # make an avatar friend
        self.avatarButton = DirectButton(
            parent = self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = TTLocalizer.FriendInviterToon,
            text_scale = 0.07,
            text_pos = (0.0, -0.1),
            pos = (-0.35, 0.0, -0.05),
            command = self._FriendSecret__handleAvatar
            )
        # make a label to show avatar friend desc on rollover
        avatarText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(0.35, 0, -0.3),
            text = TTLocalizer.FriendInviterToonFriendInfo,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.055,
            text_align = TextNode.ACenter,
            )
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()

        # make an account friend
        self.accountButton = DirectButton(
            parent = self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = TTLocalizer.FriendInviterPlayer,
            text_scale = 0.07,
            text_pos = (0.0, -0.1),
            pos = (0.35, 0.0, -0.05),
            command = self._FriendSecret__handleAccount
            )
        # make a label to show feature desc on rollover
        accountText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(-0.35, 0, -0.3),
            text = TTLocalizer.FriendInviterPlayerFriendInfo,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.055,
            text_align = TextNode.ACenter,
            )
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()
        
        buttons.removeNode()

    def __determineSecret(self):
        assert self.notify.debugCall()
        # If we support both types of secrets...
        if self.secretType == BothSecrets:
            # ask the player what type they want
            self._FriendSecret__cleanupFirstPage()
            self.ok1.hide()
            self.changeOptions.hide()
            self.nextText['text'] = TTLocalizer.FriendInviterBegin
            self.nextText.setPos(0, 0, 0.30)
            self.nextText.show()
            self.avatarButton.show()
            self.accountButton.show()
            self.cancel.show()
        else:
            # or just get the secret
            self._FriendSecret__getSecret()

