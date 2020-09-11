from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog import RejectCode

globalFriendSecret = None

AccountSecret = 0
AvatarSecret = 1
BothSecrets = 2

def showFriendSecret(secretType=AvatarSecret):
    """
    Added optional parameter to offer the choice between account and avatar friend tokens.
    """
    # A module function to open the global secret panel.
    global globalFriendSecret
    if not base.cr.isPaid():
        # bring up teaser panel
        chatMgr = base.localAvatar.chatMgr
        chatMgr.fsm.request("trueFriendTeaserPanel")
    elif not base.cr.isParentPasswordSet():
        # non-COPPA gamecard user: prompt to leave game and set parent password
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in ['DisneyOnline-AP', 'DisneyOnline-UK', 'JP', 'DE', 'BR', 'FR']:
            chatMgr = base.localAvatar.chatMgr
            if not base.cr.isPaid():
                chatMgr.fsm.request("unpaidChatWarning")
            else:
                chatMgr.paidNoParentPassword = 1
                chatMgr.fsm.request("unpaidChatWarning")
        else:
            chatMgr.paidNoParentPassword = 1
            chatMgr.fsm.request("noSecretChatAtAll")
            # bring up dialog for true friends
            # open chat with true friends

    elif not base.cr.allowSecretChat():
        # If we're paid but have not yet activated secrets, pop up the
        # dialog to do this.
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in ['DisneyOnline-AP', 'DisneyOnline-UK', 'JP', 'DE', 'BR', 'FR']:
            chatMgr = base.localAvatar.chatMgr
            if not base.cr.isPaid():
                chatMgr.fsm.request("unpaidChatWarning")
            else:
                chatMgr.paidNoParentPassword = 1
                chatMgr.fsm.request("unpaidChatWarning")
        else:
            # we no longer offer the ability to enable chat in game
            #chatMgr.fsm.request("noSecretChatWarning")
            chatMgr.fsm.request("noSecretChatAtAll")
    elif base.cr.needParentPasswordForSecretChat():
        # If we're paid but have the flag set to require the Parent Password to be
        # entered to get or use a Secret Friends password, pop up the
        # dialog to get the Parent Password.
        unloadFriendSecret()
        globalFriendSecret = FriendSecretNeedsParentLogin(secretType)
        globalFriendSecret.enter()
    else:
        # Otherwise, actually open the secrets panel.
        openFriendSecret(secretType)

def openFriendSecret(secretType):
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
    globalFriendSecret = FriendSecret(secretType)
    globalFriendSecret.enter()

def hideFriendSecret():
    # A module function to close the global secret panel if it is open.
    if globalFriendSecret != None:
        globalFriendSecret.exit()

def unloadFriendSecret():
    # A module function to completely unload the global secret panel.
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
        globalFriendSecret = None
    

class FriendSecretNeedsParentLogin(StateData.StateData):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendSecretNeedsParentLogin")
    
    def __init__(self, secretType):
        assert self.notify.debugCall()
        StateData.StateData.__init__(self, "friend-secret-needs-parent-login-done")
        self.dialog = None
        self.secretType = secretType
        
    def enter(self):
        assert self.notify.debugCall()
        StateData.StateData.enter(self)
        base.localAvatar.chatMgr.fsm.request("otherDialog")
        # Pop up a dialog indicating the parent account needs to login
        # in order to get to the Secret Friends chat:
        if self.dialog == None:
            guiButton = loader.loadModel("phase_3/models/gui/quit_button")
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            nameBalloon = loader.loadModel("phase_3/models/props/chatbox_input")
            optionsButtonImage = (guiButton.find("**/QuitBtn_UP"),
                                  guiButton.find("**/QuitBtn_DN"),
                                  guiButton.find("**/QuitBtn_RLVR"))
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                             buttons.find('**/ChtBx_OKBtn_DN'),
                             buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (buttons.find('**/CloseBtn_UP'),
                                 buttons.find('**/CloseBtn_DN'),
                                 buttons.find('**/CloseBtn_Rllvr'))

            # The Castillian (and all foreign) version relies on a seperate parent
            # password system. Omit the the password entry field and cancel button.
            withParentAccount = False
            try:
                withParentAccount = base.cr.withParentAccount
            except:
                self.notify.warning("withParentAccount not found in base.cr")
                pass

            if withParentAccount:
                okPos = (-0.22, 0.0, -0.5)
                textPos = (0, 0.25)
                okCommand = self.__handleOKWithParentAccount  
            elif base.cr.productName != "Terra-DMC":
                okPos = (-0.22, 0.0, -0.5)
                textPos = (0, 0.25)
                okCommand = self.__oldHandleOK                
            else:
                self.passwordEntry = None
                okPos = (0, 0, -0.35)
                textPos = (0, 0.125)
                okCommand = self.__handleCancel

            # make the common gui elements
            self.dialog = DirectFrame(
                parent = aspect2dp,
                pos = (0.0, 0.1, 0.2),
                relief = None,
                image = DGG.getDefaultDialogGeom(),
                image_color = OTPGlobals.GlobalDialogColor,
                image_scale = (1.4, 1.0, 1.25),
                image_pos = (0,0,-0.1),
                text = OTPLocalizer.FriendSecretNeedsParentLoginWarning,
                text_wordwrap = 21.5,
                text_scale = 0.055,
                text_pos = textPos,
                textMayChange = 1)
            DirectButton(
                self.dialog,
                image = okButtonImage,
                relief = None,
                text = OTPLocalizer.FriendSecretNeedsPasswordWarningOK,
                text_scale = 0.05,
                text_pos = (0.0, -0.1),
                textMayChange = 0,
                pos = okPos,
                command = okCommand)
            DirectLabel(
                parent = self.dialog,
                relief = None,
                pos = (0, 0, 0.35), 
                text = OTPLocalizer.FriendSecretNeedsPasswordWarningTitle,
                textMayChange = 0,
                text_scale = 0.08)

            # if not foreign, make the domestic only password entry elements
            if base.cr.productName != "Terra-DMC":
                self.usernameLabel = DirectLabel(
                    parent = self.dialog,
                    relief = None,
                    pos = (-0.07, 0.0, -0.1),
                    text = OTPLocalizer.ParentLogin,
                    text_scale = 0.06,
                    text_align = TextNode.ARight,
                    textMayChange = 0)
                self.usernameEntry = DirectEntry(
                    parent = self.dialog,
                    relief = None,
                    image = nameBalloon,
                    image1_color = (0.8, 0.8, 0.8, 1.0),
                    scale = 0.064,
                    pos = (0.0, 0.0, -0.1),
                    width = OTPGlobals.maxLoginWidth,
                    numLines = 1,
                    focus = 1,
                    cursorKeys = 1,
                    obscured = 1,
                    command = self.__handleUsername)
                self.passwordLabel = DirectLabel(
                    parent = self.dialog,
                    relief = None,
                    pos = (-0.02, 0.0, -0.3),
                    text = OTPLocalizer.ParentPassword,
                    text_scale = 0.06,
                    text_align = TextNode.ARight,
                    textMayChange = 0)
                self.passwordEntry = DirectEntry(
                    parent = self.dialog,
                    relief = None,
                    image = nameBalloon,
                    image1_color = (0.8, 0.8, 0.8, 1.0),
                    scale = 0.064,
                    pos = (0.04, 0.0, -0.3),
                    width = OTPGlobals.maxLoginWidth,
                    numLines = 1,
                    focus = 1,
                    cursorKeys = 1,
                    obscured = 1,
                    command = okCommand )
                DirectButton(
                    self.dialog,
                    image = cancelButtonImage,
                    relief = None,
                    text = OTPLocalizer.FriendSecretNeedsPasswordWarningCancel,
                    text_scale = 0.05,
                    text_pos = (0.0, -0.1),
                    textMayChange = 1,
                    pos = (0.2, 0.0, -0.5),
                    command = self.__handleCancel)

                # hide the parent login as it's not valid yet
                if withParentAccount:
                    self.usernameEntry.enterText('')
                    self.usernameEntry['focus'] = 1
                    self.passwordEntry.enterText('')
                    
                else:
                    self.usernameEntry.hide()
                    self.usernameLabel.hide()
                    self.passwordEntry['focus'] = 1
                    self.passwordEntry.enterText('')

            guiButton.removeNode()
            buttons.removeNode()
            nameBalloon.removeNode()
        else:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsParentLoginWarning
            if self.usernameEntry:
                self.usernameEntry['focus'] = 1
                self.usernameEntry.enterText('')
            elif self.passwordEntry:
                self.passwordEntry['focus'] = 1
                self.passwordEntry.enterText('')
            
        self.dialog.show()

    def exit(self):
        assert self.notify.debugCall()
        self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        if self.isEntered:
            base.localAvatar.chatMgr.fsm.request("mainMenu")
            StateData.StateData.exit(self)

    def __handleUsername(self, *args):
        assert self.notify.debugCall()
        # activate password entry
        if self.passwordEntry:
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    def __handleOKWithParentAccount(self, *args):
        assert self.notify.debugCall()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        # we need to store these in base.cr for __enterSecret
        base.cr.parentUsername = username
        base.cr.parentPassword = password        
        tt = base.cr.loginInterface
        try:
            DISLIdFromLogin = base.cr.DISLIdFromLogin
        except:
            DISLIdFromLogin = 0
        if DISLIdFromLogin and ( DISLIdFromLogin != localAvatar.DISLid):
            # we only expect to have 1 DISLId per player, we're screwed if this happens
            self.notify.error("Mismatched DISLIds, fromLogin=%s, localAvatar.dislId=%s" %
                              ( DISLIdFromLogin, localAvatar.DISLid))
        okflag, message = tt.authenticateParentUsernameAndPassword(localAvatar.DISLid,
                                                                   base.cr.password,
                                                                   username,
                                                                   password)
        if okflag:
            self.exit()
            openFriendSecret(self.secretType)
        elif message:
            # Error connecting.
            base.localAvatar.chatMgr.fsm.request("problemActivatingChat")
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % (message)
        else:
            # Wrong password.
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        
        
    def __oldHandleOK(self, *args):
        assert self.notify.debugCall()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        # we need to store these in base.cr for __enterSecret
        base.cr.parentUsername = username
        base.cr.parentPassword = password        
        tt = base.cr.loginInterface
        okflag, message = tt.authenticateParentPassword(base.cr.userName, base.cr.password, password)
        if okflag:
            self.exit()
            openFriendSecret(self.secretType)
        elif message:
            # Error connecting.
            base.localAvatar.chatMgr.fsm.request("problemActivatingChat")
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % (message)
        else:
            # Wrong password.
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    def __handleOK(self, *args):
        assert self.notify.debugCall()
        base.cr.parentUsername = self.usernameEntry.get()
        base.cr.parentPassword = self.passwordEntry.get()
        # we don't have a request for this yet, so pretend we are submitting a limited secret
        base.cr.playerFriendsManager.sendRequestUseLimitedSecret('', base.cr.parentUsername, base.cr.parentPassword)
        self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self.__handleParentLogin)
        # we won't get an answer yet, so spoof a return code
        # self.__handleParentLogin(0)
        # that doesn't work, just immediately close the panel
        self.exit()

    def __handleParentLogin(self, reason):
        # don't know reason codes yet, spoof something
        if reason == 0:
            self.exit()
            openFriendSecret(self.secretType)
        elif reason == 1:
            # Wrong username
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongUsername
            self.usernameEntry['focus'] = 1
            self.usernameEntry.enterText('')
        elif reason == 2:
            # Wrong password
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        else:
            # Error connecting (fall through case)
            base.localAvatar.chatMgr.fsm.request("problemActivatingChat")
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % (message)

    def __handleCancel(self):
        assert self.notify.debugCall()
        self.exit()


class FriendSecret(DirectFrame, StateData.StateData):
    """
    This is a panel that allows the user to manage 'secrets' that is,
    code words that identify people who are actually friends in real
    life (and thus are entitled to use full chat with each other).

    This panel is the place the user will come to either get a new
    'secret' to give to someone else, or to enter the 'secret' they
    got from someone.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendSecret")

    def __init__(self, secretType):
        assert self.notify.debugCall()
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
        StateData.StateData.__init__(self, "friend-secret-done")
        self.initialiseoptions(FriendSecret)
        self.prefix = OTPGlobals.getDefaultProductPrefix()
        # what types of secret friends will we offer
        self.secretType = secretType
        self.notify.debug("### secretType = %s" % self.secretType)
        # what type of secret friend has the user chosen
        self.requestedSecretType = secretType
        self.notify.debug("### requestedSecretType = %s" % self.requestedSecretType)
        
        
    def unload(self):
        assert self.notify.debugCall()
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()

        del self.introText
        del self.getSecret
        del self.enterSecretText
        del self.enterSecret
        del self.ok1
        del self.ok2
        del self.cancel
        del self.secretText
        del self.avatarButton
        del self.accountButton
        DirectFrame.destroy(self)
        self.ignore('clientCleanup')

    def load(self):
        assert self.notify.debugCall()
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1

        self.introText = DirectLabel(
            parent = self,
            relief = None,
            pos = (0, 0, 0.4),
            scale = 0.05,
            text = OTPLocalizer.FriendSecretIntro,
            text_fg = (0,0,0,1),
            text_wordwrap = 30,
            )
        self.introText.hide()

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")

        self.getSecret = DirectButton(
            parent = self,
            relief = None,
            pos = (0, 0, -0.11),
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = OTPLocalizer.FSgetSecret,
            text = OTPLocalizer.FriendSecretGetSecret,
            text_scale = OTPLocalizer.FSgetSecretButton,
            text_pos = (0,-0.02),
            command = self.__determineSecret,
            )
        self.getSecret.hide()

        self.enterSecretText = DirectLabel(
            parent = self,
            relief = None,
            pos = OTPLocalizer.FSenterSecretTextPos,
            scale = 0.05,
            text = OTPLocalizer.FriendSecretEnterSecret,
            text_fg = (0,0,0,1),
            text_wordwrap = 30,
            )
        self.enterSecretText.hide()

        self.enterSecret = DirectEntry(
            parent = self,
            relief = DGG.SUNKEN,
            scale = 0.06,
            pos = (-0.60, 0, -0.38),
            frameColor = (0.8,0.8,0.5,1),
            borderWidth = (0.1, 0.1),
            numLines = 1,
            width = 20,
            frameSize = (-0.4, 20.4, -0.4, 1.1),
            command = self.__enterSecret
            )

        # This fixes a little problem with the initial frame size.
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()

        self.ok1 = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = OTPLocalizer.FSok1,
            text = OTPLocalizer.FriendSecretEnter,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            pos = (0, 0, -0.5),
            command = self.__ok1,
            )
        self.ok1.hide()

        if base.cr.productName in ['JP', 'DE', 'BR', 'FR']:
            # There should be no 'change secret friends options' button in
            # the UK version.
            # the only thing we do to self.changeOptions is show and hide it;
            # avoid adding a bunch of 'if' statements
            class ShowHide:
                def show(self):
                    pass
                def hide(self):
                    pass
            self.changeOptions = ShowHide()

        self.ok2 = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = OTPLocalizer.FSok2,
            text = OTPLocalizer.FriendSecretOK,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            pos = (0, 0, -0.57),
            command = self.__ok2,
            )
        self.ok2.hide()

        self.cancel = DirectButton(
            parent = self,
            relief = None,
            text = OTPLocalizer.FriendSecretCancel,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = OTPLocalizer.FScancel,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            pos = (0, 0, -0.57),
            command = self.__cancel,
            )
        self.cancel.hide()

        self.nextText = DirectLabel(
            parent = self,
            relief = None,
            pos = (0, 0, 0.30),
            scale = 0.06,
            text = "",
            text_scale = OTPLocalizer.FSnextText,
            text_fg = (0,0,0,1),
            text_wordwrap = 25.5,
            )
        self.nextText.hide()

        self.secretText = DirectLabel(
            parent = self,
            relief = None,
            pos = (0, 0, -0.42),
            scale = 0.1,
            text = "",
            text_fg = (0,0,0,1),
            text_wordwrap = 30,
            )
        self.secretText.hide()

        guiButton.removeNode()

        # moved into it's own method to make overloading easier
        self.makeFriendTypeButtons()
        
        self.accept('clientCleanup', self.__handleCleanup)
        self.accept('walkDone', self.__handleStop)
        
    def __handleStop(self, message):
        self.exit()
        
    def __handleCleanup(self):
        self.unload()

    def makeFriendTypeButtons(self):
        # NOTE: this uses generic text, if you want game-specific text, please inherit and override
        # (see $TOONTOWN/src/friends/ToontownFriendSecret.py for an example)
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')

        # make an avatar friend
        self.avatarButton = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendSecretDetermineSecretAvatar,
            text_scale = 0.07,
            text_pos = (0.0, -0.1),
            pos = (-0.35, 0.0, -0.05),
            command = self.__handleAvatar
            )
        # make a label to show avatar friend desc on rollover
        avatarText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(0.35, 0, -0.3),
            text = OTPLocalizer.FriendSecretDetermineSecretAvatarRollover,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.055,
            text_align = TextNode.ACenter,
            )
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()

        # make an account friend
        self.accountButton = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendSecretDetermineSecretAccount,
            text_scale = 0.07,
            text_pos = (0.0, -0.1),
            pos = (0.35, 0.0, -0.05),
            command = self.__handleAccount
            )
        # make a label to show feature desc on rollover
        accountText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(-0.35, 0, -0.3),
            text = OTPLocalizer.FriendSecretDetermineSecretAccountRollover,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.055,
            text_align = TextNode.ACenter,
            )
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()
        
        buttons.removeNode()

    def enter(self):
        assert self.notify.debugCall()
        if self.isEntered == 1:
            return
        self.isEntered = 1
        # Use isLoaded to avoid redundant loading
        if self.isLoaded == 0:
            self.load()

        self.show()

        # Set us up on the first page.
        self.introText.show()
        self.getSecret.show()
        self.enterSecretText.show()
        self.enterSecret.show()
        self.ok1.show()

        self.ok2.hide()
        self.cancel.hide()
        self.nextText.hide()
        self.secretText.hide()

        # While the entry's on the screen, we have to turn off the
        # background focus on the normal chat entry.  Otherwise,
        # keypresses would start chatting!
        base.localAvatar.chatMgr.fsm.request("otherDialog")

        # And now we can set the focus on our entry.
        self.enterSecret['focus'] = 1

        # The secret panel uses up a lot of space onscreen; in
        # particular, it will hide most of the chat balloons.  Force
        # these to go to the margins.
        NametagGlobals.setOnscreenChatForced(1)

    def exit(self):
        assert self.notify.debugCall()
        if self.isEntered == 0:
            return
        self.isEntered = 0

        # Restore the normal chat behavior.
        NametagGlobals.setOnscreenChatForced(0)

        self.__cleanupFirstPage()
        self.ignoreAll()
        self.accept('clientCleanup', self.unload)
        self.hide()

    def __determineSecret(self):
        assert self.notify.debugCall()
        # If we support both types of secrets...
        if self.secretType == BothSecrets:
            # ask the player what type they want
            self.__cleanupFirstPage()
            self.ok1.hide()
            # NOTE: this uses generic text, if you want game-specific text, please inherit and override
            # (see $TOONTOWN/src/friends/ToontownFriendSecret.py for an example)
            self.nextText['text'] = OTPLocalizer.FriendSecretDetermineSecret
            self.nextText.setPos(0, 0, 0.30)
            self.nextText.show()
            self.avatarButton.show()
            self.accountButton.show()
            self.cancel.show()
        else:
            # or just get the secret
            self.__getSecret()

    def __handleAvatar(self):
        assert self.notify.debugCall()
        self.requestedSecretType = AvatarSecret
        self.__getSecret()

    def __handleAccount(self):
        assert self.notify.debugCall()
        self.requestedSecretType = AccountSecret
        self.__getSecret()

    def __handleCancel(self):
        assert self.notify.debugCall()
        self.exit()
            
    def __getSecret(self):
        assert self.notify.debugCall()
        self.__cleanupFirstPage()
        self.nextText['text'] = OTPLocalizer.FriendSecretGettingSecret
        self.nextText.setPos(0, 0, 0.30)
        self.nextText.show()
        self.avatarButton.hide()
        self.accountButton.hide()
        self.ok1.hide()
        self.cancel.show()
        if self.requestedSecretType == AvatarSecret:
            # If we don't have a FriendManager, something's badly wrong.
            # Most likely we're running in a development environment
            # without an AI client.
            if not base.cr.friendManager:
                self.notify.warning("No FriendManager available.")
                self.exit()
                return
            base.cr.friendManager.up_requestSecret()
            self.accept('requestSecretResponse', self.__gotAvatarSecret)
        else:
            if base.cr.needParentPasswordForSecretChat():
                self.notify.info("### requestLimitedSecret")
                base.cr.playerFriendsManager.sendRequestLimitedSecret(base.cr.parentUsername, base.cr.parentPassword)
            else:
                base.cr.playerFriendsManager.sendRequestUnlimitedSecret()
                self.notify.info("### requestUnlimitedSecret")
            self.accept(OTPGlobals.PlayerFriendNewSecretEvent, self.__gotAccountSecret)
            self.accept(OTPGlobals.PlayerFriendRejectNewSecretEvent, self.__rejectAccountSecret)

    def __gotAvatarSecret(self, result, secret):
        assert self.notify.debugCall()
        self.ignore('requestSecretResponse')

        if result == 1:
            self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
            self.nextText.setPos(*OTPLocalizer.FSgotSecretPos)
            if self.prefix:
                # if desired, prepend a prefix to differentiate from other products
                self.secretText['text'] = self.prefix + ' ' + secret
            else:
                self.secretText['text'] = secret
        else:
            # Oops, too many secrets.
            self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __gotAccountSecret(self, secret):
        assert self.notify.debugCall()
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        
        self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
        self.nextText.setPos(0, 0, 0.47)
        # for now Account friends (i.e. XD Friends) have no unique prefix
        self.secretText['text'] = secret
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __rejectAccountSecret(self, reason):
        assert self.notify.debugCall()
        print "## rejectAccountSecret: reason = ", reason
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        # TODO: handle more reasons
        # Oops, too many secrets.
        self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __enterSecret(self, secret):
        assert self.notify.debugCall()
        # Empty the entry for next time.
        self.enterSecret.set("")

        secret = string.strip(secret)
        if not secret:
            # If the secret is empty, it just means to close down
            # the dialog.
            self.exit()
            return
        
        # If we don't have a FriendManager, something's badly wrong.
        # Most likely we're running in a development environment
        # without an AI client.
        if not base.cr.friendManager:
            self.notify.warning("No FriendManager available.")
            self.exit()
            return
            
        self.__cleanupFirstPage()

        # The client can now prepend a product prefix to all secrets - strip this off if present
        if self.prefix:
            if secret[0:2] == self.prefix:
                secret = secret[3:]
                self.notify.info("### use TT secret")
                self.accept('submitSecretResponse', self.__enteredSecret)
                base.cr.friendManager.up_submitSecret(secret)
            else:
                # this is not a code for this product, they must want to make player true friends
                self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__useAccountSecret)
                self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self.__rejectUseAccountSecret)
                if base.cr.needParentPasswordForSecretChat():
                    self.notify.info("### useLimitedSecret")
                    base.cr.playerFriendsManager.sendRequestUseLimitedSecret(secret, base.cr.parentUsername, base.cr.parentPassword)
                else:
                    self.notify.info("### useUnlimitedSecret")
                    base.cr.playerFriendsManager.sendRequestUseUnlimitedSecret(secret)

        self.nextText['text'] = OTPLocalizer.FriendSecretTryingSecret
        self.nextText.setPos(0, 0, 0.30)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()

    def __enteredSecret(self, result, avId):
        assert self.notify.debugCall()
        self.ignore('submitSecretResponse')

        if result == 1:
            # We made it!
            handle = base.cr.identifyAvatar(avId)
            if handle != None:            
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSuccess % (handle.getName())
            else:
                # Shoot.  We just made friends with someone, but we
                # don't know who it is yet.  We'll have to ask the
                # server who this is, and wait for the response before
                # we can continue.
                self.accept('friendsMapComplete', self.__nowFriends, [avId])
                ready = base.cr.fillUpFriendsMap()
                if ready:
                    self.__nowFriends(avId)
                return

        elif result == 0:
            # Unknown secret.
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretUnknown

        elif result == 2:
            # Friends list full.
            handle = base.cr.identifyAvatar(avId)
            if handle != None:            
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretFull % (handle.getName())
            else:
                self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretFullNoName

        elif result == 3:
            # Self match.
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSelf

        elif result == 4:
            # This doesn't look like our secret friend code - wrong prefix
            self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretWrongProduct % (self.prefix)

        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __useAccountSecret(self, avId, friendInfo):
        assert self.notify.debugCall()
        self.ignore(OTPGlobals.PlayerFriendUpdateEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)

        # todo - pass an avId?
        self.__enteredSecret(1, 0)

    def __rejectUseAccountSecret(self, reason):
        assert self.notify.debugCall("reason = %s" % reason)
        print "## rejectUseAccountSecret: reason = ", reason
        self.ignore(OTPGlobals.PlayerFriendUpdateEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)

        if (reason == RejectCode.RejectCode.FRIENDS_LIST_FULL):
            self.__enteredSecret(2, 0)
        elif (reason == RejectCode.RejectCode.ALREADY_FRIENDS_WITH_SELF):
            self.__enteredSecret(3, 0)
        else:
            # todo: this shouldn't be the fall thru
            self.__enteredSecret(0, 0)

    def __nowFriends(self, avId):
        assert self.notify.debugCall()
        # This is called only from enteredSecret(), after the friend
        # transaction has completed.  This will be called only if the
        # client didn't know the identity of the friend at the time,
        # but it should know now.
        
        self.ignore('friendsMapComplete')

        handle = base.cr.identifyAvatar(avId)
        if handle != None:            
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriends % (handle.getName())
        else:
            # This really shouldn't be possible.
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriendsNoName

        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __ok1(self):
        assert self.notify.debugCall()
        # Clicking "ok" from the front screen is the same thing as
        # pressing Enter in the entry.
        secret = self.enterSecret.get()
        self.__enterSecret(secret)

    def __ok2(self):
        assert self.notify.debugCall()
        # Clicking "ok" from a finished screen just makes the thing go
        # away.
        self.exit()

    def __cancel(self):
        assert self.notify.debugCall()
        # Clicking "cancel" makes the panel close too.
        self.exit()

    def __cleanupFirstPage(self):
        assert self.notify.debugCall()
        # Removes all the widgets etc. that were created for the
        # welcome page, except the introText.

        self.introText.hide()
        self.getSecret.hide()
        self.enterSecretText.hide()
        self.enterSecret.hide()

        # Restore the background focus on the chat entry.
        base.localAvatar.chatMgr.fsm.request("mainMenu")        

        

