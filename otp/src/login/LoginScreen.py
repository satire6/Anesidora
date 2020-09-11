"""LoginScreen module: contains the LoginScreen class"""

import os
import time
from datetime import datetime

from pandac.PandaModules import *

from direct.distributed.MsgTypes import *
from direct.gui.DirectGui import *
from direct.fsm import StateData
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.otpgui import OTPDialog
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog.AccountDetailRecord import AccountDetailRecord, SubDetailRecord

import TTAccount
import GuiScreen

class LoginScreen(StateData.StateData, GuiScreen.GuiScreen):
    """
    Contains methods for displaying the login screen,
    getting and verifying the user's login name
    """
    AutoLoginName = base.config.GetString("%s-auto-login%s"%(game.name, os.getenv("otp_client", "")), "")
    AutoLoginPassword = base.config.GetString("%s-auto-password%s"%(game.name, os.getenv("otp_client", "")), "")

    # Create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LoginScreen")

    ActiveEntryColor = Vec4(1,1,1,1)
    InactiveEntryColor = Vec4(0.8,0.8,0.8,1)

    def __init__(self, cr, doneEvent):
        """
        Set-up the login screen interface and prompt for a user name
        """
        self.notify.debug('__init__')
        StateData.StateData.__init__(self, doneEvent)
        GuiScreen.GuiScreen.__init__(self)
        assert cr.serverVersion
        self.cr = cr
        self.loginInterface = self.cr.loginInterface

        self.userName = ''
        self.password = ''

        self.fsm = ClassicFSM.ClassicFSM('LoginScreen',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['login',
                                         'waitForLoginResponse', # for autologin
                                         ]),
                            State.State('login',
                                        self.enterLogin,
                                        self.exitLogin,
                                        ['waitForLoginResponse',
                                         'login',
                                         'showLoginFailDialog',
                                         ]),
                            State.State('showLoginFailDialog',
                                        self.enterShowLoginFailDialog,
                                        self.exitShowLoginFailDialog,
                                        ['login',
                                         'showLoginFailDialog',
                                         ]),
                            State.State('waitForLoginResponse',
                                        self.enterWaitForLoginResponse,
                                        self.exitWaitForLoginResponse,
                                        ['login',
                                         'showLoginFailDialog',
                                         'showConnectionProblemDialog',
                                         ]),
                            State.State('showConnectionProblemDialog',
                                        self.enterShowConnectionProblemDialog,
                                        self.exitShowConnectionProblemDialog,
                                        ['login',
                                         ]),
                            ],
                           'off',
                           'off',
                           )
        self.fsm.enterInitialState()

    def load(self):
        self.notify.debug('load')
        masterScale = 0.8
        
        textScale = 0.1*masterScale
        entryScale = 0.08*masterScale
        lineHeight = 0.21*masterScale

        buttonScale = 1.15*masterScale
        buttonLineHeight = 0.14*masterScale
        
        # login screen
        self.frame = DirectFrame(
            parent = aspect2d,
            relief = None,
            sortOrder=20,
            )
        self.frame.hide()
        linePos = -0.26

        self.nameLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.21, 0, linePos),
            text = OTPLocalizer.LoginScreenUserName,
            text_scale = textScale,
            text_align = TextNode.ARight,
            )
        self.nameEntry = DirectEntry(
            parent = self.frame,
            relief = DGG.SUNKEN,
            borderWidth = (0.1,0.1),
            scale = entryScale,
            pos = (-0.125, 0.0, linePos),
            width = OTPGlobals.maxLoginWidth,
            numLines = 1,
            focus = 0,
            cursorKeys = 1,
            )
        linePos-=lineHeight

        self.passwordLabel = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (-0.21, 0, linePos),
            text = OTPLocalizer.LoginScreenPassword,
            text_scale = textScale,
            text_align = TextNode.ARight,
            )
        self.passwordEntry = DirectEntry(
            parent = self.frame,
            relief = DGG.SUNKEN,
            borderWidth = (0.1,0.1),
            scale = entryScale,
            pos = (-0.125, 0.0, linePos),
            width = OTPGlobals.maxLoginWidth,
            numLines = 1,
            focus = 0,
            cursorKeys = 1,
            obscured = 1,
            command = self.__handleLoginPassword,
            )
        linePos-=lineHeight

        buttonImageScale = (1.7, 1.1, 1.1)
        self.loginButton = DirectButton(
            parent = self.frame,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = buttonScale,
            text = OTPLocalizer.LoginScreenLogin,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.__handleLoginButton,
            )
        linePos-=buttonLineHeight

        self.createAccountButton = DirectButton(
            parent = self.frame,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = buttonScale,
            text = OTPLocalizer.LoginScreenCreateAccount,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.__handleCreateAccount,
            )
        linePos-=buttonLineHeight

        self.quitButton = DirectButton(
            parent = self.frame,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = buttonScale,
            text = OTPLocalizer.LoginScreenQuit,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            command = self.__handleQuit,
            )
        linePos-=buttonLineHeight

        self.dialogDoneEvent = "loginDialogAck"
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.dialog = dialogClass(
            dialogName = 'loginDialog',
            doneEvent = self.dialogDoneEvent,
            message = "",
            style = OTPDialog.Acknowledge,
            # make sure this dialog shows up over the email panel
            sortOrder = NO_FADE_SORT_INDEX + 100,
            )
        self.dialog.hide()

        self.failDialog = DirectFrame(
            parent = aspect2dp,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,.1,0),
            text = "",
            text_scale = 0.08,
            text_pos = (0.0, 0.3),
            text_wordwrap = 15,
            # make this panel modal-able
            sortOrder = NO_FADE_SORT_INDEX,
            )
        linePos = -.05
        self.failTryAgainButton = DirectButton(
            parent = self.failDialog,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = .9,
            text = OTPLocalizer.LoginScreenTryAgain,
            text_scale = 0.06,
            text_pos = (0,-.02),
            command = self.__handleFailTryAgain,
            )
        linePos-=buttonLineHeight

        self.failCreateAccountButton = DirectButton(
            parent = self.failDialog,
            relief = DGG.RAISED,
            borderWidth = (0.01,0.01),
            pos = (0,0,linePos),
            scale = .9,
            text = OTPLocalizer.LoginScreenCreateAccount,
            text_scale = 0.06,
            text_pos = (0,-.02),
            command = self.__handleFailCreateAccount,
            )
        linePos-=buttonLineHeight

        self.failDialog.hide()
        
        self.connectionProblemDialogDoneEvent = "loginConnectionProblemDlgAck"
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.connectionProblemDialog = dialogClass(
            dialogName = 'connectionProblemDialog',
            doneEvent = self.connectionProblemDialogDoneEvent,
            message = "",
            style = OTPDialog.Acknowledge,
            # make sure this dialog shows up over the email panel
            sortOrder = NO_FADE_SORT_INDEX + 100,
            )
        self.connectionProblemDialog.hide()

        #background.removeNode()
        #guiButton.removeNode()
        #nameBalloon.removeNode()
        
    def unload(self):
        self.notify.debug('unload')
        self.nameEntry.destroy()
        self.passwordEntry.destroy()
        self.failTryAgainButton.destroy()
        self.failCreateAccountButton.destroy()
        self.createAccountButton.destroy()
        self.loginButton.destroy()
        self.quitButton.destroy()
        self.dialog.cleanup()
        del self.dialog
        # call destroy instead of cleanup;
        # failDialog is actually a DirectFrame
        self.failDialog.destroy()
        del self.failDialog
        self.connectionProblemDialog.cleanup()
        del self.connectionProblemDialog
        self.frame.destroy()
        del self.fsm
        del self.loginInterface
        del self.cr

    def enter(self):
        if self.cr.blue:
            # If we have a blue, go straight to it.
            self.userName = 'blue'
            self.password = self.cr.blue
            self.fsm.request("waitForLoginResponse")
        elif self.cr.playToken:
            # If we have a PlayToken, go straight to it.
            self.userName = '*' # Junk value, but may help debugging.
            self.password = self.cr.playToken
            self.fsm.request("waitForLoginResponse")
        elif hasattr(self.cr,"DISLToken") and self.cr.DISLToken:
            # If we have a DISLToken, go straight to it.
            self.userName = '*' # Junk value, but may help debugging.
            self.password = self.cr.DISLToken
            self.fsm.request("waitForLoginResponse")
        elif self.AutoLoginName:
            # Otherwise, we're logging in with in-game user and
            # password; but these might be provided also.
            self.userName = self.AutoLoginName
            self.password = self.AutoLoginPassword
            self.fsm.request("waitForLoginResponse")
        else:
            # In the normal case, we must prompt the user for her
            # username and password.
            self.fsm.request("login")
        
    def exit(self):
        self.frame.hide()
        self.ignore(self.dialogDoneEvent)
        self.fsm.requestFinalState()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterLogin(self):
        # make SURE the password field is obscured
        assert self.passwordEntry['obscured']

        self.cr.resetPeriodTimer(None)

        self.userName = ''
        self.password = ''

        # if there's a 'last login', get it
        self.userName = launcher.getLastLogin()
        # if there's a 'last login', and the user just entered
        # a different login, failed to login, and came back here,
        # ignore the 'last login' value
        if self.userName and self.nameEntry.get():
            if self.userName != self.nameEntry.get():
                self.userName = ''

        self.frame.show()
        self.nameEntry.enterText(self.userName)
        self.passwordEntry.enterText(self.password)

        self.focusList = [self.nameEntry,
                          self.passwordEntry,
                          ]
        # if the username is already filled in, give the
        # password box the focus
        focusIndex = 0
        if self.userName:
            focusIndex = 1
        self.startFocusMgmt(startFocus=focusIndex)

    def exitLogin(self):
        self.stopFocusMgmt()

    def enterShowLoginFailDialog(self, msg):
        base.transitions.fadeScreen(.5)
        self.failDialog['text'] = msg
        self.failDialog.show()

    def __handleFailTryAgain(self):
        self.fsm.request("login")
    def __handleFailCreateAccount(self):
        messenger.send(self.doneEvent, [{'mode': 'createAccount'}])

    def __handleFailNoNewAccountsAck(self):
        # hide the error dialog, and show the login fail dialog again
        self.dialog.hide()
        # can't simply 'show()' the fail dlg again, since the error dlg
        # messes with the screen fade, etc.
        self.fsm.request("showLoginFailDialog", [self.failDialog['text']])

    def exitShowLoginFailDialog(self):
        base.transitions.noTransitions()
        self.failDialog.hide()

    # event handlers

    def __handleLoginPassword(self, password):
        # if there's something in the password field...
        if password != "":
            # if there's something in the account name field...
            if self.nameEntry.get() != "":
                # try to log in
                self.__handleLoginButton()

    def __handleLoginButton(self):
        self.removeFocus()
        
        self.userName = self.nameEntry.get()
        self.password = self.passwordEntry.get()

        # sometimes we deal with accounts that have empty passwords,
        # so allow the user to submit a login with an empty password;
        # a user will get an error message if they accidentally submit
        # a login with an empty pwd; not a big deal in terms of user
        # experience or wasted bandwidth
        if (self.userName == ""): # or self.password == ""):
            self.dialog.setMessage(OTPLocalizer.LoginScreenLoginPrompt)
            self.dialog.show()
            self.acceptOnce(self.dialogDoneEvent, self.__handleEnterLoginAck)
        else:
            self.fsm.request("waitForLoginResponse")

    def __handleQuit(self):
        self.removeFocus()
        messenger.send(self.doneEvent, [{'mode': 'quit'}])

    def __handleCreateAccount(self):
        self.removeFocus()
        messenger.send(self.doneEvent, [{'mode': 'createAccount'}])

    def enterWaitForLoginResponse(self):
        self.cr.handler = self.handleWaitForLoginResponse
        self.cr.userName = self.userName
        self.cr.password = self.password

        try:
            error=self.loginInterface.authorize(self.userName, self.password)
        except TTAccount.TTAccountException, e:
            self.fsm.request('showConnectionProblemDialog', [str(e)])
            return

        if error:
            self.notify.info(error)
            # did it fail because our free time has expired?
            # this used to ask the cr if free time has expired, but we
            # can't rely on the cr for that info at this point, since
            # there was an error
            freeTimeExpired = (self.loginInterface.getErrorCode() == 10)
            if freeTimeExpired:
                # The account has expired; output the account name so we
                # can see it in the log.
                self.cr.logAccountInfo()
                messenger.send(self.doneEvent, [{'mode': 'freeTimeExpired'}])
            else:
                self.fsm.request("showLoginFailDialog", [error])
        else:
            self.loginInterface.sendLoginMsg()
            self.waitForDatabaseTimeout(requestName='WaitForLoginResponse')

    def exitWaitForLoginResponse(self):
        self.cleanupWaitingForDatabase()
        self.cr.handler = None

    def enterShowConnectionProblemDialog(self, msg):
        self.connectionProblemDialog.setMessage(msg)
        self.connectionProblemDialog.show()
        self.acceptOnce(self.connectionProblemDialogDoneEvent,
                        self.__handleConnectionProblemAck)

    def __handleConnectionProblemAck(self):
        self.connectionProblemDialog.hide()
        self.fsm.request('login')

    def exitShowConnectionProblemDialog(self):
        pass

    def handleWaitForLoginResponse(self, msgType, di):
        if msgType == CLIENT_LOGIN_2_RESP:
            self.handleLoginResponseMsg2(di)
        elif msgType == CLIENT_LOGIN_RESP:
            self.handleLoginResponseMsg(di)
        # Pirates DISL login
        elif msgType == CLIENT_LOGIN_3_RESP:
            self.handleLoginResponseMsg3(di)
        elif msgType == CLIENT_LOGIN_TOONTOWN_RESP:
            self.handleLoginToontownResponse(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.cr.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.cr.handleServerDown(di)
        else:
            self.cr.handleMessageType(msgType, di)

    def getExtendedErrorMsg(self, errorString):
        # if it's a DC mismatch, tack the server address onto
        # the end of this error message
        prefix = 'Bad DC Version Compare'
        if len(errorString) < len(prefix):
            return errorString
        if errorString[:len(prefix)] == prefix:
            return '%s%s' % (errorString, ', address=%s' % base.cr.getServerAddress())
        return errorString

    def handleLoginResponseMsg3(self, di):
        #print("LoginScreen - handleLoginResponseMsg3")
        # We having gotten a login response from the server for our
        # normal Pirates login, via the DISL account system
        
        # First, get the local time of day that we receive the message
        # from the server, so we can compare our clock to the server's
        # clock.
        now = time.time()

        # Get the return code
        returnCode = di.getInt8()
        errorString = self.getExtendedErrorMsg(di.getString())

        self.notify.info("Login response return code %s" % (returnCode))

        if returnCode != 0:
            # If the return code is non-zero, something went
            # wrong.  Better just go to reject mode and bail out.
            self.notify.info("Login failed: %s" % (errorString))
            messenger.send(self.doneEvent, [{'mode': 'reject'}])
            return

        accountDetailRecord = AccountDetailRecord()

        # chat permission fields
        accountDetailRecord.openChatEnabled = (di.getString() == "YES")
        accountDetailRecord.createFriendsWithChat = (di.getString() == "YES")
        chatCodeCreation = di.getString()
        accountDetailRecord.chatCodeCreation = (chatCodeCreation == "YES")
        parentControlledChat = (chatCodeCreation == "PARENT")
        access = di.getString()
        if access == "VELVET":
            access = OTPGlobals.AccessVelvetRope
        elif access == "FULL":
            access = OTPGlobals.AccessFull
        else:
            self.notify.warning("Unknown access: %s" % access)
            access = OTPGlobals.AccessUnknown        
        accountDetailRecord.piratesAccess = access
        accountDetailRecord.familyAccountId = di.getInt32()
        accountDetailRecord.playerAccountId = di.getInt32()
        accountDetailRecord.playerName = di.getString()
        accountDetailRecord.playerNameApproved = di.getInt8()
        accountDetailRecord.maxAvatars = di.getInt32()

        # Remember these fields on the client repository
        self.cr.openChatAllowed = accountDetailRecord.openChatEnabled
        self.cr.secretChatAllowed = accountDetailRecord.chatCodeCreation or parentControlledChat
        self.cr.setIsPaid(accountDetailRecord.piratesAccess)
        self.userName = accountDetailRecord.playerName
        self.cr.userName = accountDetailRecord.playerName

        # Now retrieve the subscription information
        accountDetailRecord.numSubs = di.getUint16()

        for i in range(accountDetailRecord.numSubs):
            subDetailRecord = SubDetailRecord()
            subDetailRecord.subId = di.getUint32()
            subDetailRecord.subOwnerId = di.getUint32()
            subDetailRecord.subName = di.getString()
            subDetailRecord.subActive = di.getString()
            access = di.getString()
            if access == "VELVET":
                access = OTPGlobals.AccessVelvetRope
            elif access == "FULL": 
                access = OTPGlobals.AccessFull
            else:
                access = OTPGlobals.AccessUnknown
            subDetailRecord.subAccess = access
            subDetailRecord.subLevel = di.getUint8()
            subDetailRecord.subNumAvatars = di.getUint8()
            subDetailRecord.subNumConcur = di.getUint8()
            subDetailRecord.subFounder = (di.getString() == "YES")
            accountDetailRecord.subDetails[subDetailRecord.subId] = subDetailRecord

        accountDetailRecord.WLChatEnabled = (di.getString() == "YES")
        if accountDetailRecord.WLChatEnabled:
            self.cr.whiteListChatEnabled = 1
        else:
            self.cr.whiteListChatEnabled = 0

        self.notify.info("End of DISL token parse")
        self.notify.info("accountDetailRecord: %s" % accountDetailRecord)

        self.cr.accountDetailRecord = accountDetailRecord
        self.__handleLoginSuccess()
        

    def handleLoginResponseMsg2(self, di):
        #print("LoginScreen - handleLoginResponseMsg2")
        # We having gotten a login response from the server for our
        # normal Toontown login, via the account server.
        
        # First, get the local time of day that we receive the message
        # from the server, so we can compare our clock to the server's
        # clock.
        self.notify.debug('handleLoginResponseMsg2')
        if self.notify.getDebug():
            dgram = di.getDatagram()
            dgram.dumpHex(ostream)
            
        now = time.time()

        # Get the return code
        returnCode = di.getUint8()
        errorString = self.getExtendedErrorMsg(di.getString())

        # The account name and chat flag are redundant if we logged in
        # via a user-supplied username and password, since we already
        # knew these; but if we logged in via LoginGoAccount, we don't
        # know this stuff until the server cracks open the token and
        # sends them back to us.  So we need to save these at least in
        # this case, but it does no harm to save them in all cases
        # anyway.
        self.userName = di.getString()
        self.cr.userName = self.userName
        
        accountDetailRecord = AccountDetailRecord()
        self.cr.accountDetailRecord = accountDetailRecord

        # Chat:
        canChat = di.getUint8()
        self.cr.secretChatAllowed = canChat
        self.notify.info("Chat from game server login: %s" % (canChat))

        # The current time of day at the server
        sec = di.getUint32()
        usec = di.getUint32()
        serverTime = sec + usec / 1000000.0
        self.cr.serverTimeUponLogin = serverTime
        self.cr.clientTimeUponLogin = now
        self.cr.globalClockRealTimeUponLogin = globalClock.getRealTime()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.toontownTimeManager.updateLoginTimes(
                serverTime, now, self.cr.globalClockRealTimeUponLogin)         
        serverDelta = serverTime - now
        self.cr.setServerDelta(serverDelta)
        self.notify.setServerDelta(serverDelta, 28800)

        # Whether the user is paid
        self.isPaid = di.getUint8()
        self.cr.setIsPaid(self.isPaid)
        if self.isPaid:
            launcher.setPaidUserLoggedIn()
        self.notify.info("Paid from game server login: %s" % (self.isPaid))
            
        # default
        self.cr.resetPeriodTimer(None)
        if di.getRemainingSize() >= 4:
            # The amount of time remaining on the user's account for
            # this period, in minutes.
            minutesRemaining = di.getInt32()
            self.notify.info("Minutes remaining from server %s" % (minutesRemaining))

            if (minutesRemaining >= 0):
                self.notify.info("Spawning period timer")
                self.cr.resetPeriodTimer(minutesRemaining * 60)
            elif (self.isPaid):
                self.notify.warning("Negative minutes remaining for paid user (?)")
            else:
                self.notify.warning("Not paid, but also negative minutes remaining (?)")
        else:
            self.notify.info("Minutes remaining not returned from server; not spawning period timer")

        familyStr = di.getString()
        WhiteListResponse = di.getString()
        
        if WhiteListResponse == "YES":
            self.cr.whiteListChatEnabled = 1
        else:
            self.cr.whiteListChatEnabled = 0
        
        if di.getRemainingSize() > 0:
            self.cr.accountDays = self.parseAccountDays(di.getInt32())
        else:
            self.cr.accountDays = 100000

        if di.getRemainingSize() > 0:
            self.lastLoggedInStr = di.getString()
            self.notify.info("last logged in = %s" % self.lastLoggedInStr)
        else:
            self.lastLoggedInStr = ""
        self.cr.lastLoggedIn = datetime.now()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.lastLoggedIn = self.cr.toontownTimeManager.convertStrToToontownTime(self.lastLoggedInStr)
        # old style login_2 does Not have an associated parent account
        self.cr.withParentAccount = False
                
        self.notify.info("Login response return code %s" % (returnCode))

        if returnCode == 0:
            self.__handleLoginSuccess()

        elif returnCode == -13:
            # This error code means the user has entered a valid
            # password, but he has already used up his allowable time
            # for the period.

            # In practice, we never see this error message, since the
            # server sends us the "go get lost" message instead.  So
            # this code is untested.  But it remains, in case the
            # server semantics should change one day.
            self.notify.info("Period Time Expired")
            self.fsm.request("showLoginFailDialog",
                             [OTPLocalizer.LoginScreenPeriodTimeExpired])
        else:
            # If the return code is anything else, something went
            # wrong.  Better just go to reject mode and bail out.
            self.notify.info("Login failed: %s" % (errorString))
            messenger.send(self.doneEvent, [{'mode': 'reject'}])

                
    def handleLoginResponseMsg(self, di):
        #print("LoginScreen - handleLoginResponseMsg2")
        # We having gotten a login response from the server for our
        # old-style Toontown login, via the "account-old-auth 1"
        # Configrc option.  This is normally used only in the
        # developmernt environment.
        self.notify.debug('handleLoginResponseMsg1')
        if self.notify.getDebug():
            dgram = di.getDatagram()
            dgram.dumpHex(ostream)


        # First, get the local time of day that we receive the message
        # from the server, so we can compare our clock to the server's
        # clock.
        now = time.time()
        
        accountDetailRecord = AccountDetailRecord()
        self.cr.accountDetailRecord = accountDetailRecord

        # Get the return code
        returnCode = di.getUint8()
        accountCode = di.getUint32()
        errorString = self.getExtendedErrorMsg(di.getString())

        # The current time of day at the server.
        sec = di.getUint32()
        usec = di.getUint32()
        serverTime = sec + usec / 1000000.0
        serverDelta = serverTime - now
        self.cr.serverTimeUponLogin = serverTime
        self.cr.clientTimeUponLogin = now
        self.cr.globalClockRealTimeUponLogin = globalClock.getRealTime()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.toontownTimeManager.updateLoginTimes(
                serverTime, now, self.cr.globalClockRealTimeUponLogin) 
        
        self.cr.setServerDelta(serverDelta)
        self.notify.setServerDelta(serverDelta, 28800)

        if di.getRemainingSize() > 0:
            self.cr.accountDays = self.parseAccountDays(di.getInt32())
        else:
            self.cr.accountDays = 100000 
            
        if di.getRemainingSize() > 0:
            WhiteListResponse = di.getString()
        else:
            WhiteListResponse = "NO"

        if WhiteListResponse == "YES":
            self.cr.whiteListChatEnabled = 1
        else:
            self.cr.whiteListChatEnabled = 0

        # an example last logged in is "2009-11-09 17:51:51"
        self.lastLoggedInStr = base.config.GetString('last-logged-in',"")
        self.cr.lastLoggedIn = datetime.now()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.lastLoggedIn = self.cr.toontownTimeManager.convertStrToToontownTime(self.lastLoggedInStr)
        # developer login with a config override
        self.cr.withParentAccount = base.config.GetBool('dev-with-parent-account',0)
        
        self.notify.info("Login response return code %s" % (returnCode))
    

        if returnCode == 0:
            # if the return code is good, record the account code
            # and request the avatar list.
            self.__handleLoginSuccess()
        elif returnCode == 12:
            self.notify.info("Bad password")
            self.fsm.request(
                "showLoginFailDialog",
                [OTPLocalizer.LoginScreenBadPassword])
        elif returnCode == 14:
            self.notify.info("Bad word in user name")
            self.fsm.request(
                "showLoginFailDialog",
                [OTPLocalizer.LoginScreenInvalidUserName])
        elif returnCode == 129:
            self.notify.info("Username not found")
            self.fsm.request(
                "showLoginFailDialog",
                [OTPLocalizer.LoginScreenUserNameNotFound])
        else:
            # if the return code is bad, go to reject mode
            self.notify.info("Login failed: %s" % (errorString))
            messenger.send(self.doneEvent, [{'mode': 'reject'}])
            

                
        

    def __handleLoginSuccess(self):
        self.cr.logAccountInfo()
        launcher.setGoUserName(self.userName)
        launcher.setLastLogin(self.userName)

        launcher.setUserLoggedIn()
        if self.loginInterface.freeTimeExpires == -1:
            launcher.setPaidUserLoggedIn()

        if self.loginInterface.needToSetParentPassword():
            # they paid for their account, but got cut off before they
            # could set their chat password. get it now.
            messenger.send(self.doneEvent, [{'mode': 'getChatPassword'}])
        else:
            messenger.send(self.doneEvent, [{'mode': 'success'}])

    def __handleEnterLoginAck(self):
        self.dialog.hide()
        self.fsm.request("login")

    def __handleNoNewAccountsAck(self):
        self.dialog.hide()
        self.fsm.request("login")

    def parseAccountDays(self, accountDays):
        """Return how many this this account has been created, returns 100,000 if error."""
        assert self.notify.debugStateCall(self)
        result = 100000
        if accountDays >= 0:
            result = accountDays
        else:
            self.notify.warning('account days is negative %s' % accountDays)
        self.notify.debug('result=%s' % result)
        return result            

    def handleLoginToontownResponse(self, di):
        """Handle the new toontown specific login response.
        
        We having gotten a toontown specific login response from the
        server for our normal Toontown login, via the account server.
        We can also get here with use-tt-specific-dev-login set to 1
        """
        # First, get the local time of day that we receive the message
        # from the server, so we can compare our clock to the server's
        # clock.
        self.notify.debug('handleLoginToontownResponse')
        if 1: #self.notify.getDebug():
            dgram = di.getDatagram()
            dgram.dumpHex(ostream)
            
        now = time.time()

        # Get the return code
        returnCode = di.getUint8()
        respString = di.getString()
        errorString = self.getExtendedErrorMsg(respString)

        # account number is actually DISL ID
        self.accountNumber = di.getUint32()
        self.cr.DISLIdFromLogin = self.accountNumber
        
        # The account name and chat flag are redundant if we logged in
        # via a user-supplied username and password, since we already
        # knew these; but if we logged in via LoginGoAccount, we don't
        # know this stuff until the server cracks open the token and
        # sends them back to us.  So we need to save these at least in
        # this case, but it does no harm to save them in all cases
        # anyway.
        self.accountName = di.getString()
        # unfortunately the above is ACCOUNT_NAME which is actually DNAME
        # we need the game username, lets add it to the login response
        
        # account name approved is new
        self.accountNameApproved = di.getUint8()
        
        accountDetailRecord = AccountDetailRecord()
        self.cr.accountDetailRecord = accountDetailRecord

        # open chat enabled is new, probably not used in toontown        
        self.openChatEnabled = (di.getString() == "YES")

        # this is CREATE_FRIENDS_WITH_CHAT
        createFriendsWithChat = di.getString()
        canChat = (createFriendsWithChat == 'YES') or (createFriendsWithChat=='CODE')
        self.cr.secretChatAllowed = canChat
        self.notify.info("CREATE_FRIENDS_WITH_CHAT from game server login: %s %s" % (createFriendsWithChat, canChat))

        # this controls if he can make a true friend code,
        # valid values are NO, PARENT and YES
        self.chatCodeCreationRule = di.getString()
        self.cr.chatChatCodeCreationRule = self.chatCodeCreationRule
        self.notify.info("Chat code creation rule = %s" % (self.chatCodeCreationRule))
        # correct the default value from quick launcher
        self.cr.secretChatNeedsParentPassword = (self.chatCodeCreationRule == 'PARENT')

        # The current time of day at the server
        sec = di.getUint32()
        usec = di.getUint32()
        serverTime = sec + usec / 1000000.0
        self.cr.serverTimeUponLogin = serverTime
        self.cr.clientTimeUponLogin = now
        self.cr.globalClockRealTimeUponLogin = globalClock.getRealTime()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.toontownTimeManager.updateLoginTimes(
                serverTime, now, self.cr.globalClockRealTimeUponLogin)         
        serverDelta = serverTime - now
        self.cr.setServerDelta(serverDelta)
        self.notify.setServerDelta(serverDelta, 28800)
        

        # Whether the user is paid
        access = di.getString()
        self.isPaid = (access == 'FULL')
        # correct the default value from quicklauncher
        self.cr.parentPasswordSet = self.isPaid
        self.cr.setIsPaid(self.isPaid)
        if self.isPaid:
            launcher.setPaidUserLoggedIn()
        self.notify.info("Paid from game server login: %s" % (self.isPaid))
     

        WhiteListResponse = di.getString()
        
        if WhiteListResponse == "YES":
            self.cr.whiteListChatEnabled = 1
        else:
            self.cr.whiteListChatEnabled = 0

        self.lastLoggedInStr = di.getString()
        self.cr.lastLoggedIn = datetime.now()
        if hasattr(self.cr, 'toontownTimeManager'):
            self.cr.lastLoggedIn = self.cr.toontownTimeManager.convertStrToToontownTime(self.lastLoggedInStr)
        
        if di.getRemainingSize() > 0:
            self.cr.accountDays = self.parseAccountDays(di.getInt32())
        else:
            self.cr.accountDays = 100000

        self.toonAccountType = di.getString()
        if self.toonAccountType == "WITH_PARENT_ACCOUNT":
            self.cr.withParentAccount = True
        elif self.toonAccountType == "NO_PARENT_ACCOUNT":
            self.cr.withParentAccount = False
        else:
            # we really need one or the other,
            self.notify.error('unknown toon account type %s' % self.toonAccountType)

        self.notify.info("toonAccountType=%s" % self.toonAccountType)
        self.userName = di.getString()
        self.cr.userName = self.userName
                
        self.notify.info("Login response return code %s" % (returnCode))

        if returnCode == 0:
            self.__handleLoginSuccess()

        elif returnCode == -13:
            # This error code means the user has entered a valid
            # password, but he has already used up his allowable time
            # for the period.

            # In practice, we never see this error message, since the
            # server sends us the "go get lost" message instead.  So
            # this code is untested.  But it remains, in case the
            # server semantics should change one day.
            self.notify.info("Period Time Expired")
            self.fsm.request("showLoginFailDialog",
                             [OTPLocalizer.LoginScreenPeriodTimeExpired])
        else:
            # If the return code is anything else, something went
            # wrong.  Better just go to reject mode and bail out.
            self.notify.info("Login failed: %s" % (errorString))
            messenger.send(self.doneEvent, [{'mode': 'reject'}])
