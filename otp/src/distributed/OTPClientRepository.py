import sys
import time
import string
import types
import random
import gc
import os


from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from otp.distributed.OtpDoGlobals import *

from direct.interval.IntervalGlobal import ivalMgr
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClientRepositoryBase import ClientRepositoryBase
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.task import Task
from direct.distributed import DistributedSmoothNode
from direct.showbase import PythonUtil, GarbageReport, BulletinBoardWatcher
from direct.showbase.ContainerLeakDetector import ContainerLeakDetector
from direct.showbase import MessengerLeakDetector
from direct.showbase.GarbageReportScheduler import GarbageReportScheduler
from direct.showbase import LeakDetectors
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from otp.avatar import Avatar
from otp.avatar.DistributedPlayer import DistributedPlayer
from otp.login import TTAccount
from otp.login import LoginTTSpecificDevAccount
from otp.login import AccountServerConstants
from otp.login.CreateAccountScreen import CreateAccountScreen
from otp.login import LoginScreen
from otp.otpgui import OTPDialog
from otp.avatar import DistributedAvatar
from otp.otpbase import OTPLocalizer
from otp.login import LoginGSAccount
from otp.login import LoginGoAccount
from otp.login.LoginWebPlayTokenAccount import LoginWebPlayTokenAccount
from otp.login.LoginDISLTokenAccount import LoginDISLTokenAccount
from otp.login import LoginTTAccount
from otp.login import HTTPUtil
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLauncherGlobals
from otp.uberdog import OtpAvatarManager
from otp.distributed import OtpDoGlobals
from otp.ai.GarbageLeakServerEventAggregator import GarbageLeakServerEventAggregator

from PotentialAvatar import PotentialAvatar

class OTPClientRepository(ClientRepositoryBase):
    # Create a notify category
    notify = directNotify.newCategory("OTPClientRepository")

    # The most avatars one account can have
    avatarLimit = 6

    WishNameResult = Enum([
        'Failure', 'PendingApproval', 'Approved', 'Rejected',
        ])

    def __init__(self, serverVersion, launcher = None, playGame = None):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Ancestor init
        ClientRepositoryBase.__init__(self)

        # A derived class should reassign this member to change the
        # response behavior appropriately.
        self.handler = None

        self.launcher = launcher
        # Give base a handle to the launcher
        base.launcher = launcher

        #self.launcher.setDisconnectDetailsNormal()

        self.__currentAvId = 0

        # Specifies which product this is.
        # Valid values are currently:
        #      DisneyOnline-US (US - English)
        #      DisneyOnline-UK (UK - English)
        #      DisneyOnline-AP (AP - English)
        #      Terra-DMC (Spain - Castillian: DMC)
        #      ES (Spain - Castillian: open internet)
        #      JP (Japan - Japanese: open internet)
        #      DE (Germany - German)
        #      BR (Brazil - Portuguese)
        #      FR (France - French)
        self.productName = config.GetString('product-name', 'DisneyOnline-US')

        # Derived classes should fill this in with the Python class of the
        # particular avatar type to create.  This is temporary code for
        # gateway stuff for now.
        self.createAvatarClass = None

        # This will be loaded on demand when it is needed.  We can't
        # load it up front because it may not have been downloaded
        # yet.
        self.systemMessageSfx = None

        # If US version, check the registry to get UK/AP
        reg_deployment = ""
        if (self.productName == 'DisneyOnline-US'):
            if self.launcher:
                if self.launcher.isDummy():
                    reg_deployment = self.launcher.getDeployment()
                else:
                    reg_deployment = self.launcher.getRegistry('DEPLOYMENT')
                    if reg_deployment != 'UK' and reg_deployment != 'AP':
                        # try environment variable for VISTA launcher for UK
                        reg_deployment = self.launcher.getRegistry('GAME_DEPLOYMENT')
                    self.notify.info ('reg_deployment=%s' % reg_deployment)

                if (reg_deployment == 'UK'):
                    self.productName = 'DisneyOnline-UK'
                elif (reg_deployment == 'AP'):
                    self.productName = 'DisneyOnline-AP'

        # Get the "blue" token, if there is one, from the launcher.
        # This is used for people who are logging in via the Disney
        # Magic Connection login system, which happens outside of the
        # game.
        self.blue = None
        if self.launcher:
            self.blue = self.launcher.getBlue()
        # Also check the Config file for testing.
        fakeBlue = config.GetString('fake-blue', '')
        if fakeBlue:
            self.blue = fakeBlue

        # Get the "playToken", if there is one, from the launcher.
        # This is used for people who are logging in via the
        # web page, which happens outside of the game.
        self.playToken = None
        if self.launcher:
            self.playToken = self.launcher.getPlayToken()
        # Also check the Config file for testing.
        fakePlayToken = config.GetString('fake-playtoken', '')
        if fakePlayToken:
            self.playToken = fakePlayToken

        # Get the "DISL Token", if there is one, from the launcher.
        # This is used for people who are logging in via the
        # DISL account system, which happens outside of the game.
        self.DISLToken = None
        if self.launcher:
            self.DISLToken = self.launcher.getDISLToken()
        # Also check the Config file for testing.
        fakeDISLToken = config.GetString('fake-DISLToken', '')
        fakeDISLPlayerName = config.GetString('fake-DISL-PlayerName','')
        if fakeDISLToken:
            self.DISLToken = fakeDISLToken
        elif fakeDISLPlayerName:
            defaultId = 42
            defaultNumAvatars = 4
            defaultNumAvatarSlots = 4
            defaultNumConcur = 1
            subCount = config.GetInt('fake-DISL-NumSubscriptions', 1)
            playerAccountId = config.GetInt('fake-DISL-PlayerAccountId',defaultId)
            self.DISLToken = ("ACCOUNT_NAME=%s" % fakeDISLPlayerName +
                              "&ACCOUNT_NUMBER=%s" % playerAccountId +
                              "&ACCOUNT_NAME_APPROVAL=%s" % config.GetString('fake-DISL-PlayerNameApproved','YES') +
                              "&SWID=%s" % config.GetString('fake-DISL-SWID','{1763AC36-D73F-41C2-A54A-B579E58B69C8}') +
                              "&FAMILY_NUMBER=%s" % config.GetString('fake-DISL-FamilyAccountId','-1') +
                              "&familyAdmin=%s" % config.GetString('fake-DISL-FamilyAdmin','1') +
                              "&PIRATES_ACCESS=%s" % config.GetString('fake-DISL-PiratesAccess','FULL') +
                              "&PIRATES_MAX_NUM_AVATARS=%s" % config.GetInt('fake-DISL-MaxAvatars',defaultNumAvatars) +
                              "&PIRATES_NUM_AVATAR_SLOTS=%s" % config.GetInt('fake-DISL-MaxAvatarSlots',defaultNumAvatarSlots) +
                              "&expires=%s" % config.GetString('fake-DISL-expire','1577898000') +
                              "&OPEN_CHAT_ENABLED=%s" % config.GetString('fake-DISL-OpenChatEnabled','YES') +
                              "&CREATE_FRIENDS_WITH_CHAT=%s" % config.GetString('fake-DISL-CreateFriendsWithChat','YES') +
                              "&CHAT_CODE_CREATION_RULE=%s" % config.GetString('fake-DISL-ChatCodeCreation','YES') +
                              "&FAMILY_MEMBERS=%s" % config.GetString('fake-DISL-FamilyMembers') +
                              "&PIRATES_SUB_COUNT=%s" % subCount)
            for i in range(subCount):
                self.DISLToken += ("&PIRATES_SUB_%s_ACCESS=%s" % (i, config.GetString('fake-DISL-Sub-%s-Access'%i, 'FULL')) +
                                   "&PIRATES_SUB_%s_ACTIVE=%s" % (i, config.GetString('fake-DISL-Sub-%s-Active'%i, 'YES')) +
                                   "&PIRATES_SUB_%s_ID=%s" % (i, config.GetInt('fake-DISL-Sub-%s-Id'%i, playerAccountId) + config.GetInt('fake-DISL-Sub-Id-Offset', 0)) +
                                   "&PIRATES_SUB_%s_LEVEL=%s" % (i, config.GetInt('fake-DISL-Sub-%s-Level'%i, 3)) +
                                   "&PIRATES_SUB_%s_NAME=%s" % (i, config.GetString('fake-DISL-Sub-%s-Name'%i, fakeDISLPlayerName)) +
                                   "&PIRATES_SUB_%s_NUM_AVATARS=%s" % (i, config.GetInt('fake-DISL-Sub-%s-NumAvatars'%i, defaultNumAvatars)) +
                                   "&PIRATES_SUB_%s_NUM_CONCUR=%s" % (i, config.GetInt('fake-DISL-Sub-%s-NumConcur'%i, defaultNumConcur)) +
                                   "&PIRATES_SUB_%s_OWNERID=%s" % (i, config.GetInt('fake-DISL-Sub-%s-OwnerId'%i, playerAccountId)) +
                                   "&PIRATES_SUB_%s_FOUNDER=%s" % (i, config.GetString('fake-DISL-Sub-%s-Founder'%i, 'YES'))
                                   )
            self.DISLToken += ("&WL_CHAT_ENABLED=%s" % config.GetString('fake-DISL-WLChatEnabled','YES') +
                               "&valid=true")
            print self.DISLToken

        # Find out what kind of login we are supposed to used and let
        # us know if it's not found:
        self.requiredLogin=config.GetString("required-login", "auto")
        if (self.requiredLogin=="auto"):
            # Guess which login to used.
            self.notify.info("required-login auto.")
        elif (self.requiredLogin=="green"):
            self.notify.error("The green code is out of date")
        elif (self.requiredLogin=="blue"):
            if (not self.blue):
                self.notify.error("The tcr does not have the required blue login")
        elif (self.requiredLogin=="playToken"):
            if (not self.playToken):
                self.notify.error("The tcr does not have the required playToken login")
        elif (self.requiredLogin=="DISLToken"):
            if (not self.DISLToken):
                self.notify.error("The tcr does not have the required DISL token login")
        elif (self.requiredLogin=="gameServer"):
            self.notify.info("Using game server name/password.")
            self.DISLToken = None
        else:
            self.notify.error("The required-login was not recognized.")

        self.computeValidateDownload()

        # Has the user provided a password to enable magic words?
        self.wantMagicWords = base.config.GetString('want-magic-words', '')

        # Get the HTTPClient from the Launcher, or make up a new client.
        # DummyLauncher does not have an HTTPClient
        if self.launcher and hasattr(self.launcher, 'http'):
            self.http = self.launcher.http
        else:
            self.http = HTTPClient()

        # This method is also deliberately misnamed.
        self.allocateDcFile()

        self.accountOldAuth = config.GetBool('account-old-auth', 0)
        # allow toontown-account-old-auth
        self.accountOldAuth = config.GetBool('%s-account-old-auth' % game.name,
                                             self.accountOldAuth)
        self.useNewTTDevLogin = base.config.GetBool('use-tt-specific-dev-login', False)
        # create a global login/account server interface
        if self.useNewTTDevLogin:
            self.loginInterface = LoginTTSpecificDevAccount.LoginTTSpecificDevAccount(self)
            self.notify.info("loginInterface: LoginTTSpecificDevAccount")
        elif self.accountOldAuth:
            self.loginInterface = LoginGSAccount.LoginGSAccount(self)
            self.notify.info("loginInterface: LoginGSAccount")
        elif self.blue:
            self.loginInterface = LoginGoAccount.LoginGoAccount(self)
            self.notify.info("loginInterface: LoginGoAccount")
        elif self.playToken:
            self.loginInterface = LoginWebPlayTokenAccount(self)
            self.notify.info("loginInterface: LoginWebPlayTokenAccount")
        elif self.DISLToken:
            self.loginInterface = LoginDISLTokenAccount(self)
            self.notify.info("loginInterface: LoginDISLTokenAccount")
        else:
            self.loginInterface = LoginTTAccount.LoginTTAccount(self)
            self.notify.info("loginInterface: LoginTTAccount")

        # This value comes in from the server
        self.secretChatAllowed = base.config.GetBool("allow-secret-chat", 0)
        self.openChatAllowed = base.config.GetBool("allow-open-chat", 0)
        
        # This value comes in from the webAcctParams
        self.secretChatNeedsParentPassword = (
            base.config.GetBool("secret-chat-needs-parent-password", 0)
            or (self.launcher and self.launcher.getNeedPwForSecretKey())
            )

        self.parentPasswordSet = (
            base.config.GetBool("parent-password-set", 0)
            or (self.launcher and self.launcher.getParentPasswordSet()))

        # Is there a signature identifying the particular xrc file in
        # use?
        if __debug__:
            # In the dev environment, the default value comes from the
            # username.
            default = 'dev-%s' % (os.getenv("USER"))
            self.userSignature = base.config.GetString('signature', default);

        else:
            # In the publish environment, the default value is "none".
            self.userSignature = base.config.GetString('signature', 'none');

        # Free time is initially unexpired.  The Login??Account object
        # will fill this in properly at log in.
        self.freeTimeExpiresAt = -1
        self.__isPaid=0

        # We also have a "period timer".  This tracks the number of
        # seconds of gameplay the player has accumulated so far this
        # month (some players have a limited quota of game time per
        # month).  This is unrelated to the free time counter, above.
        self.periodTimerExpired = 0
        self.periodTimerStarted = None
        self.periodTimerSecondsRemaining = None

        # register render and hidden for distributed reparents
        self.parentMgr.registerParent(OTPGlobals.SPRender, base.render)
        # we really don't want to use hidden anymore, just remove from the
        # scene graph entirely by reparenting to an empty nodepath
        self.parentMgr.registerParent(OTPGlobals.SPHidden, NodePath())

        self.timeManager = None

        if config.GetBool('detect-leaks', 0) or config.GetBool('client-detect-leaks', 0):
            self.startLeakDetector()

        if config.GetBool('detect-messenger-leaks', 0) or config.GetBool('ai-detect-messenger-leaks', 0):
            self.messengerLeakDetector = MessengerLeakDetector.MessengerLeakDetector(
                'client messenger leak detector')
            if config.GetBool('leak-messages', 0):
                MessengerLeakDetector._leakMessengerObject()

        if config.GetBool('run-garbage-reports', 0) or config.GetBool('client-run-garbage-reports', 0):
            noneValue = -1.
            reportWait = config.GetFloat('garbage-report-wait', noneValue)
            reportWaitScale = config.GetFloat('garbage-report-wait-scale', noneValue)
            if reportWait == noneValue:
                reportWait = 60. * 2.
            if reportWaitScale == noneValue:
                reportWaitScale = None
            self.garbageReportScheduler = GarbageReportScheduler(waitBetween=reportWait,
                                                                 waitScale=reportWaitScale)

        self._proactiveLeakChecks = (config.GetBool('proactive-leak-checks', 1) and
                                     config.GetBool('client-proactive-leak-checks', 1))
        self._crashOnProactiveLeakDetect = config.GetBool('crash-on-proactive-leak-detect', 1)

        self.activeDistrictMap = {}

        self.serverVersion = serverVersion

        self.waitingForDatabase = None

        # Set up the login state machine. This handles all the state
        # prior to the creation of localToon.
        self.loginFSM = ClassicFSM('loginFSM', [
            State('loginOff',
                  self.enterLoginOff, self.exitLoginOff,
                  ['connect']),
            State('connect',
                  self.enterConnect, self.exitConnect,
                  ['login', 'failedToConnect', 'failedToGetServerConstants']),
            State('login',
                  self.enterLogin, self.exitLogin,
                  ['noConnection',
                   'waitForGameList',
                   'createAccount',
                   'reject',
                   'failedToConnect',
                   'shutdown',
                   ]),
            State('createAccount',
                  self.enterCreateAccount, self.exitCreateAccount,
                  ['noConnection',
                   'waitForGameList',
                   'login',
                   'reject',
                   'failedToConnect',
                   'shutdown',
                   ]),
            State('failedToConnect',
                  self.enterFailedToConnect, self.exitFailedToConnect,
                  ['connect',
                   'shutdown',
                   ]),
            State('failedToGetServerConstants',
                  self.enterFailedToGetServerConstants, self.exitFailedToGetServerConstants,
                  ['connect',
                   'shutdown',
                   'noConnection',
                   ]),
            State('shutdown',
                  self.enterShutdown, self.exitShutdown,
                  ['loginOff',
                   ]),
            State('waitForGameList',
                  self.enterWaitForGameList, self.exitWaitForGameList,
                  ['noConnection',
                   'waitForShardList',
                   'missingGameRootObject',
                   ]),
            State('missingGameRootObject',
                  self.enterMissingGameRootObject, self.exitMissingGameRootObject,
                  ['waitForGameList',
                   'shutdown',
                   ]),
            State('waitForShardList',
                  self.enterWaitForShardList, self.exitWaitForShardList,
                  ['noConnection',
                   'waitForAvatarList',
                   'noShards',
                   ]),
            State('noShards',
                  self.enterNoShards, self.exitNoShards,
                  ['noConnection',
                   'noShardsWait',
                   'shutdown',
                   ]),
            State('noShardsWait',
                  self.enterNoShardsWait, self.exitNoShardsWait,
                  ['noConnection',
                   'waitForShardList',
                   'shutdown',
                   ]),
            State('reject',
                  self.enterReject, self.exitReject,
                  []),
            State('noConnection',
                  self.enterNoConnection, self.exitNoConnection,
                  ['login',
                   'connect',
                   'shutdown',
                   ]),
            State('afkTimeout',
                  self.enterAfkTimeout, self.exitAfkTimeout,
                  ['waitForAvatarList',
                   'shutdown',
                   ]),
            State('periodTimeout',
                  self.enterPeriodTimeout, self.exitPeriodTimeout,
                  ['shutdown',
                   ]),
            State('waitForAvatarList',
                  self.enterWaitForAvatarList, self.exitWaitForAvatarList,
                  ['noConnection',
                   'chooseAvatar',
                   'shutdown',
                   ]),
            State('chooseAvatar',
                  self.enterChooseAvatar, self.exitChooseAvatar,
                  ['noConnection',
                   'createAvatar',
                   'waitForAvatarList',
                   'waitForSetAvatarResponse',
                   'waitForDeleteAvatarResponse',
                   'shutdown',
                   'login',
                   ]),
            State('createAvatar',
                  self.enterCreateAvatar, self.exitCreateAvatar,
                  ['noConnection',
                   'chooseAvatar',
                   'waitForSetAvatarResponse',
                   'shutdown',
                   ]),
            State('waitForDeleteAvatarResponse',
                  self.enterWaitForDeleteAvatarResponse, self.exitWaitForDeleteAvatarResponse,
                  ['noConnection',
                   'chooseAvatar',
                   'shutdown',
                   ]),
            State('rejectRemoveAvatar',
                  self.enterRejectRemoveAvatar, self.exitRejectRemoveAvatar,
                  ['noConnection',
                   'chooseAvatar',
                   'shutdown',
                   ]),
            State('waitForSetAvatarResponse',
                  self.enterWaitForSetAvatarResponse, self.exitWaitForSetAvatarResponse,
                  ['noConnection',
                   'playingGame',
                   'shutdown',
                   ]),
            State('playingGame',
                  self.enterPlayingGame, self.exitPlayingGame,
                  ['noConnection',
                   'waitForAvatarList',
                   'login', # Shticker book may jump to login
                   'shutdown', # The user may alt-f4
                   'afkTimeout',
                   'periodTimeout',
                   'noShards',
                   ]),
            ],
            # initial State
            'loginOff',
            # final State
            'loginOff',
            )

        # Set up the game state machine. This handles all the state
        # after localToon gets created.
        self.gameFSM = ClassicFSM('gameFSM', [
            State('gameOff',
                  self.enterGameOff,
                  self.exitGameOff,
                  ['waitOnEnterResponses']),
            State('waitOnEnterResponses',
                  self.enterWaitOnEnterResponses,
                  self.exitWaitOnEnterResponses,
                  ['playGame', 'tutorialQuestion',
                   'gameOff']),
            State('tutorialQuestion',
                  self.enterTutorialQuestion,
                  self.exitTutorialQuestion,
                  ['playGame', 'gameOff']),
            State('playGame',
                  self.enterPlayGame,
                  self.exitPlayGame,
                  ['gameOff',
                   'closeShard',
                   'switchShards']),
            State('switchShards',
                  self.enterSwitchShards,
                  self.exitSwitchShards,
                  ['gameOff',
                   'waitOnEnterResponses']),
            State('closeShard',
                  self.enterCloseShard,
                  self.exitCloseShard,
                  ['gameOff',
                   'waitOnEnterResponses'
                   ])
            ],
            # initial State
            'gameOff',
            # final State
            'gameOff',
            )

        # The game fsm should be a child of the "playingGame"
        # state of loginFSM.
        self.loginFSM.getStateNamed("playingGame").addChild(self.gameFSM)

        # Put the loginFSM into its initial state
        self.loginFSM.enterInitialState()
        self.loginScreen = None
        self.music = None
        self.gameDoneEvent = "playGameDone"
        self.playGame = playGame(self.gameFSM, self.gameDoneEvent)
        self.shardInterestHandle = None
        self.uberZoneInterest = None
        self.wantSwitchboard = config.GetBool('want-switchboard',0)
        self.wantSwitchboardHacks = base.config.GetBool('want-switchboard-hacks',0)

        # Used for moderation of report-a-player feature
        self.centralLogger = self.generateGlobalObject(
            OtpDoGlobals.OTP_DO_ID_CENTRAL_LOGGER,
            "CentralLogger")

    def startLeakDetector(self):
        if hasattr(self, 'leakDetector'):
            return False
        firstCheckDelay = config.GetFloat('leak-detector-first-check-delay', 2 * 60.)
        self.leakDetector = ContainerLeakDetector(
            'client container leak detector', firstCheckDelay = firstCheckDelay)
        self.objectTypesLeakDetector = LeakDetectors.ObjectTypesLeakDetector()
        self.garbageLeakDetector = LeakDetectors.GarbageLeakDetector()
        self.renderLeakDetector = LeakDetectors.SceneGraphLeakDetector(render)
        self.hiddenLeakDetector = LeakDetectors.SceneGraphLeakDetector(hidden)
        self.cppMemoryUsageLeakDetector = LeakDetectors.CppMemoryUsage()
        self.taskLeakDetector = LeakDetectors.TaskLeakDetector()
        self.messageListenerTypesLeakDetector = LeakDetectors.MessageListenerTypesLeakDetector()
        # this isn't necessary with the current messenger implementation
        #self.messageTypesLeakDetector = LeakDetectors.MessageTypesLeakDetector()
        return True

    def getGameDoId(self):
        return self.GameGlobalsId

#################################################
##   _             _       ______ _____ __  __
##  | |           (_)     |  ____/ ____|  \/  |
##  | | ___   __ _ _ _ __ | |__ | (___ | \  / |
##  | |/ _ \ / _` | | '_ \|  __| \___ \| |\/| |
##  | | (_) | (_| | | | | | |    ____) | |  | |
##  |_|\___/ \__, |_|_| |_|_|   |_____/|_|  |_|
##            __/ |
##           |___/
##    __                  _   _
##   / _|                | | (_)
##  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
##  |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
##  | | | |_| | | | | (__| |_| | (_) | | | \__ \
##  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
##
#################################################

    ##### LoginFSM: loginOff state #####
    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterLoginOff(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleMessageType
        self.shardInterestHandle = None

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitLoginOff(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None

    def computeValidateDownload(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Get the string value to pass to the server to validate that
        # we have received the expected files from the download
        # server.  This protects against a hacker spoofing the
        # download server; the server won't allow us to connect unless
        # we produce the expected string.

        if self.launcher:
            # Here the hash comes from the launcher, having been
            # generated from the two control files downloaded from the
            # download server.

            hash = HashVal()
            hash.mergeWith(launcher.launcherFileDbHash)
            hash.mergeWith(launcher.serverDbFileHash)
            self.validateDownload = hash.asHex()
        else:
            # Here the hash is parsed out of the download.par file, in
            # the dev environment.

            self.validateDownload = ''
            basePath = os.path.expandvars('$TOONTOWN') or './toontown'
            downloadParFilename = Filename.expandFrom(
                basePath+'/src/configfiles/download.par')
            if downloadParFilename.exists():
                downloadPar = open(downloadParFilename.toOsSpecific())
                for line in downloadPar.readlines():
                    i = string.find(line, 'VALIDATE_DOWNLOAD=')
                    if i != -1:
                        self.validateDownload = string.strip(line[i + 18:])
                        break

    def getServerVersion(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return self.serverVersion

    ##### LoginFSM: connect state #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterConnect(self, serverList):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # We'll need this later if we need to relogin
        self.serverList = serverList

        # Show a "connecting..." box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.connectingBox = dialogClass(
            message=OTPLocalizer.CRConnecting)
        self.connectingBox.show()
        # Redraw the screen so the box will be visible.
        self.renderFrame()

        self.handler = self.handleMessageType

        self.connect(self.serverList,
                     successCallback = self._handleConnected,
                     failureCallback = self.failedToConnect)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def failedToConnect(self, statusCode, statusString):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.loginFSM.request("failedToConnect", [statusCode, statusString])

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitConnect(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.connectingBox.cleanup()
        del self.connectingBox

    def handleSystemMessage(self, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Got a system message from the server.
        message = ClientRepositoryBase.handleSystemMessage(self, di)

        whisper = WhisperPopup(message, OTPGlobals.getInterfaceFont(),
                               WhisperPopup.WTSystem)
        whisper.manage(base.marginManager)

        if not self.systemMessageSfx:
            # Try to load the sound effect.  This might fail if the
            # phase 3.5 has not yet been downloaded, but that's
            # OK--it's just a sound effect.  For longer term goodness,
            # we should choose a unique sound effect for system
            # messages, and ensure that it is downloaded in phase 3.

            self.systemMessageSfx = base.loadSfx(
                "phase_3.5/audio/sfx/GUI_whisper_3.mp3")

        if self.systemMessageSfx:
            base.playSfx(self.systemMessageSfx)

    def getConnectedEvent(self):
        return 'OTPClientRepository-connected'

    def _handleConnected(self):
        self.launcher.setDisconnectDetailsNormal()
        messenger.send(self.getConnectedEvent())
        self.gotoFirstScreen()

    def gotoFirstScreen(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # attempt to grab the account server constants
        try:
            self.accountServerConstants = AccountServerConstants.AccountServerConstants(self)
        except TTAccount.TTAccountException, e:
            self.notify.debug(str(e))
            self.loginFSM.request('failedToGetServerConstants', [e])
            return

        self.startReaderPollTask()
        # Start sending heartbeats
        self.startHeartbeat()

        # is this a new installation?
        newInstall = launcher.getIsNewInstallation()
        newInstall = base.config.GetBool("new-installation", newInstall)

        self.loginFSM.request("login")

    ##### LoginFSM: login #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterLogin(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Disconnect the currently-playing avatar, if there is one.
        # We need to do this just in case we came directly here from
        # the Shticker book in-game.
        self.sendSetAvatarIdMsg(0)

        # Pop up the login screen.
        self.loginDoneEvent = "loginDone"
        self.loginScreen = LoginScreen.LoginScreen(self, self.loginDoneEvent)
        self.accept(self.loginDoneEvent, self.__handleLoginDone)
        self.loginScreen.load()
        self.loginScreen.enter()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleLoginDone(self, doneStatus):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        mode = doneStatus['mode']
        if (mode == 'success'):
            # if they've logged in, this is not a new install
            self.setIsNotNewInstallation()
            self.loginFSM.request("waitForGameList")
        elif (mode == 'getChatPassword'):
            self.loginFSM.request("parentPassword")
        elif (mode == "freeTimeExpired"):
            self.loginFSM.request("freeTimeInform")
        elif (mode == "createAccount"):
            self.loginFSM.request(
                "createAccount", [{'back': 'login', 'backArgs': []}])
        elif (mode == 'reject'):
            self.loginFSM.request("reject")
        elif (mode == 'quit'):
            self.loginFSM.request("shutdown")
        elif (mode == 'failure'):
            # Looks like failed to connect wants a code and string
            # Not sure what to put here
            self.loginFSM.request("failedToConnect", [-1, "?"])
        else:
            self.notify.error(
                "Invalid doneStatus mode from loginScreen: " + str(mode))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitLogin(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Get rid of the login screen, if there is one.
        if self.loginScreen:
            self.loginScreen.exit()
            self.loginScreen.unload()
            self.loginScreen = None
            self.renderFrame()
        self.ignore(self.loginDoneEvent)
        del self.loginDoneEvent
        self.handler = None

    ##### LoginFSM: createAccount #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterCreateAccount(
            self,
            createAccountDoneData={
                "back":"login",
                "backArgs":[]}):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.createAccountDoneData = createAccountDoneData
        self.createAccountDoneEvent = "createAccountDone"
        self.createAccountScreen = None

        self.createAccountScreen = CreateAccountScreen(
            self, self.createAccountDoneEvent)
        self.accept(self.createAccountDoneEvent,
                    self.__handleCreateAccountDone)
        self.createAccountScreen.load()
        self.createAccountScreen.enter()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleCreateAccountDone(self, doneStatus):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        mode = doneStatus['mode']
        if (mode == 'success'):
            # if they've created an account, this is not a new install
            self.setIsNotNewInstallation()
            self.loginFSM.request("waitForGameList")
        elif (mode == 'reject'):
            self.loginFSM.request("reject")
        elif (mode == 'cancel'):
            self.loginFSM.request(self.createAccountDoneData['back'],
                                  self.createAccountDoneData['backArgs'])
        elif (mode == 'failure'):
            self.loginFSM.request(self.createAccountDoneData['back'],
                                  self.createAccountDoneData['backArgs'])
        elif (mode == 'quit'):
            self.loginFSM.request("shutdown")
        else:
            self.notify.error(
                "Invalid doneStatus mode from CreateAccountScreen: " +
                str(mode))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitCreateAccount(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Get rid of the createAccount screen, if there is one.
        if self.createAccountScreen:
            self.createAccountScreen.exit()
            self.createAccountScreen.unload()
            self.createAccountScreen = None
            self.renderFrame()
        self.ignore(self.createAccountDoneEvent)
        del self.createAccountDoneEvent
        self.handler = None

    ##### LoginFSM: failedToConnect #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterFailedToConnect(self, statusCode, statusString):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleMessageType
        messenger.send("connectionIssue")
        url = self.serverList[0]
        self.notify.warning(
            "Failed to connect to %s (%s %s).  Notifying user." %
            (url.cStr(), statusCode, statusString))

        if statusCode == 1403 or statusCode == 1405 or statusCode == 1400:
            message = OTPLocalizer.CRNoConnectProxyNoPort % (
                url.getServer(), url.getPort(), url.getPort())
            style = OTPDialog.CancelOnly
        else:
            message = OTPLocalizer.CRNoConnectTryAgain % (
                url.getServer(), url.getPort())
            style = OTPDialog.TwoChoice

        # Create a dialog box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.failedToConnectBox = dialogClass(
            message = message,
            doneEvent = "failedToConnectAck",
            text_wordwrap = 18,
            style = style)
        self.failedToConnectBox.show()

        self.notify.info(message)

        # Hang a hook for hitting OK or Cancel
        self.accept("failedToConnectAck", self.__handleFailedToConnectAck)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleFailedToConnectAck(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        doneStatus = self.failedToConnectBox.doneStatus
        if doneStatus == "ok":
            self.loginFSM.request("connect", [self.serverList])
            messenger.send("connectionRetrying")
        elif doneStatus == "cancel":
            self.loginFSM.request("shutdown")
        else:
            self.notify.error("Unrecognized doneStatus: " + str(doneStatus))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitFailedToConnect(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        self.ignore("failedToConnectAck")
        self.failedToConnectBox.cleanup()
        del self.failedToConnectBox

    ##### LoginFSM: failedToGetServerConstants #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterFailedToGetServerConstants(self, e):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleMessageType
        messenger.send("connectionIssue")
        url = AccountServerConstants.AccountServerConstants.getServerURL()

        # If we failed because of a connection error, get the status
        # code.  This may help us report a more useful message to the
        # user.
        statusCode = 0
        if isinstance(e, HTTPUtil.ConnectionError):
            statusCode = e.statusCode
            self.notify.warning(
                "Got status code %s from connection to %s." %
                (statusCode, url.cStr()))
        else:
            self.notify.warning(
                "Didn't get status code from connection to %s." %
                (url.cStr()))

        if statusCode == 1403 or statusCode == 1400:
            message = OTPLocalizer.CRServerConstantsProxyNoPort % (
                url.cStr(), url.getPort())
            style = OTPDialog.CancelOnly
        elif statusCode == 1405:
            message = OTPLocalizer.CRServerConstantsProxyNoCONNECT % (
                url.cStr())
            style = OTPDialog.CancelOnly
        else:
            # Just give a generic message.
            message = (OTPLocalizer.CRServerConstantsTryAgain % url.cStr())
            style = OTPDialog.TwoChoice

        # Create a dialog box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.failedToGetConstantsBox = dialogClass(
            message = message,
            doneEvent = "failedToGetConstantsAck",
            text_wordwrap = 18,
            style = style)
        self.failedToGetConstantsBox.show()

        # Hang a hook for hitting OK or Cancel
        self.accept("failedToGetConstantsAck",
                    self.__handleFailedToGetConstantsAck)

        self.notify.warning(
            "Failed to get account server constants. Notifying user.")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleFailedToGetConstantsAck(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        doneStatus = self.failedToGetConstantsBox.doneStatus
        if doneStatus == "ok":
            self.loginFSM.request("connect", [self.serverList])
            messenger.send("connectionRetrying")
        elif doneStatus == "cancel":
            self.loginFSM.request("shutdown")
        else:
            self.notify.error("Unrecognized doneStatus: " + str(doneStatus))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitFailedToGetServerConstants(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        self.ignore("failedToGetConstantsAck")
        self.failedToGetConstantsBox.cleanup()
        del self.failedToGetConstantsBox

    ##### LoginFSM: shutdown #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterShutdown(self, errorCode = None):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleMessageType
        self.sendDisconnect()
        self.notify.info("Exiting cleanly")
        base.exitShow(errorCode)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitShutdown(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if hasattr(self, 'garbageWatcher'):
            self.garbageWatcher.destroy()
            del self.garbageWatcher
        self.handler = None

    ##### LoginFSM: waitForGameList #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitForGameList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.gameDoDirectory = self.addInterest(
            self.GameGlobalsId, OTP_ZONE_ID_MANAGEMENT,
            "game directory","GameList_Complete")
        self.acceptOnce(
            "GameList_Complete", self.waitForGetGameListResponse)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def waitForGetGameListResponse(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if self.isGameListCorrect():
            if base.config.GetBool('game-server-tests', 0):
                # kick off a game server test suite
                from otp.distributed import GameServerTestSuite
                GameServerTestSuite.GameServerTestSuite(self)
            self.loginFSM.request("waitForShardList")
        else:
            self.loginFSM.request("missingGameRootObject")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def isGameListCorrect(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return 1

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitForGameList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None

    ##### LoginFSM: missingGameRootObject #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterMissingGameRootObject(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.warning("missing some game root objects.")
        self.handler = self.handleMessageType
        # Create a dialog box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.missingGameRootObjectBox = dialogClass(
            message = OTPLocalizer.CRMissingGameRootObject,
            doneEvent = "missingGameRootObjectBoxAck",
            style = OTPDialog.TwoChoice)
        self.missingGameRootObjectBox.show()
        # Hang a hook for hitting OK or Cancel
        self.accept(
            "missingGameRootObjectBoxAck",
            self.__handleMissingGameRootObjectAck)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleMissingGameRootObjectAck(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        doneStatus = self.missingGameRootObjectBox.doneStatus
        # TODO: how should we wait for shards?
        if doneStatus == "ok":
            self.loginFSM.request("waitForGameList")
        elif doneStatus == "cancel":
            self.loginFSM.request("shutdown")
        else:
            self.notify.error("Unrecognized doneStatus: " + str(doneStatus))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitMissingGameRootObject(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        self.ignore("missingGameRootObjectBoxAck")
        self.missingGameRootObjectBox.cleanup()
        del self.missingGameRootObjectBox

    ##### LoginFSM: waitForShardList #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitForShardList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if not self.isValidInterestHandle(self.shardInterestHandle):
            self.shardInterestHandle = self.addInterest(
                self.GameGlobalsId, OTP_ZONE_ID_DISTRICTS, "LocalShardList",
                "ShardList_Complete")
            self.acceptOnce("ShardList_Complete", self._wantShardListComplete)
        else:
            self._wantShardListComplete()


    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitForShardList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.ignore('ShardList_Complete')
        self.handler = None


    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _shardsAreReady(self):
        # make sure there's at least one shard up
        #print self.activeDistrictMap
        for shard in self.activeDistrictMap.values():
            if shard.available:
                return True
        else:
            return False

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _wantShardListComplete(self):
        if self._shardsAreReady():
            self.loginFSM.request("waitForAvatarList")
        else:
            self.loginFSM.request("noShards")


    ##### LoginFSM: noShards #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterNoShards(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        assert self.notify.warning("No shards are available.")
        messenger.send("connectionIssue")
        self.handler = self.handleMessageType
        # Create a dialog box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.noShardsBox = dialogClass(
            message = OTPLocalizer.CRNoDistrictsTryAgain,
            doneEvent = "noShardsAck",
            style = OTPDialog.TwoChoice)
        self.noShardsBox.show()
        # Hang a hook for hitting OK or Cancel
        self.accept("noShardsAck", self.__handleNoShardsAck)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleNoShardsAck(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        doneStatus = self.noShardsBox.doneStatus
        # TODO: how should we wait for shards?
        if doneStatus == "ok":
            messenger.send("connectionRetrying")
            self.loginFSM.request("noShardsWait")
        elif doneStatus == "cancel":
            self.loginFSM.request("shutdown")
        else:
            self.notify.error("Unrecognized doneStatus: " + str(doneStatus))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitNoShards(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        self.ignore("noShardsAck")
        self.noShardsBox.cleanup()
        del self.noShardsBox

    ##### LoginFSM: noShardsWait #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterNoShardsWait(self):
        # pretend that we're trying to reconnect for a while, to
        # cut down on traffic after an AI crash
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Show a "connecting..." box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.connectingBox = dialogClass(
            message=OTPLocalizer.CRConnecting)
        self.connectingBox.show()
        # Redraw the screen so the box will be visible.
        self.renderFrame()
        self.noShardsWaitTaskName = "noShardsWait"
        def doneWait(task, self=self):
            self.loginFSM.request('waitForShardList')
        if __dev__:
            delay = 0.
        else:
            delay = 6.5 + random.random()*2.
        taskMgr.doMethodLater(delay, doneWait,
                              self.noShardsWaitTaskName)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitNoShardsWait(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        taskMgr.remove(self.noShardsWaitTaskName)
        del self.noShardsWaitTaskName
        self.connectingBox.cleanup()
        del self.connectingBox

    ##### LoginFSM: reject #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterReject(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleMessageType

        self.notify.warning("Connection Rejected")
        # tell the activeX control we were rejected by the server.
        launcher.setPandaErrorCode(13)

        sys.exit()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitReject(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None

    ##### LoginFSM: noConnection #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterNoConnection(self):
        messenger.send("connectionIssue")
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # We come here when we've just been dropped by the server for
        # some reason.

        self.resetInterestStateForConnectionLoss()
        self.shardInterestHandle = None

        self.handler = self.handleMessageType

        # Reset our internal current AvatarID number, so we keep in
        # sync with what the server thinks our current AvatarID is (we
        # will have to establish a new connection and get a new
        # AvatarID).  If we don't do this, the server will hang up on
        # us again when we try to reset the currentID to 0 from the
        # login screen.
        self.__currentAvId = 0

        # Stop sending heartbeats
        self.stopHeartbeat()

        # Stop trying to read the connection
        self.stopReaderPollTask()

        # Get GAME_USERNAME value from env.
        gameUsername = launcher.getValue('GAME_USERNAME', base.cr.userName)

        # Look for a good explanation to display for the user.
        if self.bootedIndex != None and OTPLocalizer.CRBootedReasons.has_key(
                self.bootedIndex):
            # We've got a standard reason code for the boot from the server.
            message = (OTPLocalizer.CRBootedReasons[self.bootedIndex]) % {'name' : gameUsername}

        elif self.bootedText != None:
            # We don't recognize this reason code, but we have a text
            # string explanation from the server.
            message = OTPLocalizer.CRBootedReasonUnknownCode % self.bootedIndex

        else:
            # We didn't get a reason for the boot from the server.
            # That probably means the disconnect didn't come from the
            # server, but from some other connectivity problem.
            message = OTPLocalizer.CRLostConnection
            
        # some reasons don't want a reconnect option
        reconnect = 1
        if self.bootedIndex in (152,127):
            reconnect = 0
            
        #report disconnect to launcher for use in exit codes
        self.launcher.setDisconnectDetails(self.bootedIndex, message)

        # Create a dialog box.
        style = OTPDialog.Acknowledge
        if reconnect and self.loginInterface.supportsRelogin():
            message += OTPLocalizer.CRTryConnectAgain
            style = OTPDialog.TwoChoice
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.lostConnectionBox = dialogClass(
            doneEvent = "lostConnectionAck",
            message = message,
            text_wordwrap = 18,
            style = style)
        self.lostConnectionBox.show()

        # Hang a hook for hitting OK or Cancel.
        self.accept("lostConnectionAck", self.__handleLostConnectionAck)

        # Log a message
        self.notify.warning("Lost connection to server. Notifying user.")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleLostConnectionAck(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if self.lostConnectionBox.doneStatus == "ok" and self.loginInterface.supportsRelogin():
            # Go log in again
            self.loginFSM.request("connect", [self.serverList])
        else:
            # Goodbye!
            self.loginFSM.request("shutdown")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitNoConnection(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        # Clean up the dialog box
        self.ignore("lostConnectionAck")
        self.lostConnectionBox.cleanup()
        messenger.send("connectionRetrying")

    ##### LoginFSM: afkTimeout #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterAfkTimeout(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # We need to tell the server to no longer send messages to this
        # toon while we wait for the player to click "ok"
        self.sendSetAvatarIdMsg(0)
        msg = OTPLocalizer.AfkForceAcknowledgeMessage
        dialogClass = OTPGlobals.getDialogClass()
        self.afkDialog = dialogClass(
            text = msg, command = self.__handleAfkOk,
            style = OTPDialog.Acknowledge)
        self.handler = self.handleMessageType

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleAfkOk(self, value):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.loginFSM.request('waitForAvatarList')

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitAfkTimeout(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if (self.afkDialog):
            self.afkDialog.cleanup()
            self.afkDialog = None
        self.handler = None

    ##### LoginFSM: periodTimeout #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterPeriodTimeout(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.sendSetAvatarIdMsg(0)

        # We *could* just log out the user and go back to the login
        # page after the dialog--maybe the user's friend wants to
        # play, after all--but I think it makes more sense to go ahead
        # and boot the user all the way out of the game.
        self.sendDisconnect()

        msg = OTPLocalizer.PeriodForceAcknowledgeMessage
        dialogClass = OTPGlobals.getDialogClass()
        self.periodDialog = dialogClass(text = msg,
                                        command = self.__handlePeriodOk,
                                        style = OTPDialog.Acknowledge)
        self.handler = self.handleMessageType

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handlePeriodOk(self, value):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        base.exitShow()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitPeriodTimeout(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if (self.periodDialog):
            self.periodDialog.cleanup()
            self.periodDialog = None
        self.handler = None

    ##### LoginFSM: waitForAvatarList #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitForAvatarList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleWaitForAvatarList
        self._requestAvatarList()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _requestAvatarList(self):
        self.cleanupWaitingForDatabase()
        self.sendGetAvatarsMsg()
        self.waitForDatabaseTimeout(requestName='WaitForAvatarList')
        self.acceptOnce(OtpAvatarManager.OtpAvatarManager.OnlineEvent,
                        self._requestAvatarList)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendGetAvatarsMsg(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Request a list of avatars
        datagram = PyDatagram()
        # Add a message type
        datagram.addUint16(CLIENT_GET_AVATARS)
        # Send the message
        self.send(datagram)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitForAvatarList(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.cleanupWaitingForDatabase()
        self.ignore(OtpAvatarManager.OtpAvatarManager.OnlineEvent)
        self.handler = None

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleWaitForAvatarList(self, msgType, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if msgType == CLIENT_GET_AVATARS_RESP:
            self.handleGetAvatarsRespMsg(di)
        elif msgType == CLIENT_GET_AVATARS_RESP2:
            assert 0 # obsolete self.handleGetAvatarsResp2Msg(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        else:
            self.handleMessageType(msgType, di)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleGetAvatarsRespMsg(self, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Get the return code
        returnCode = di.getUint8()
        if returnCode == 0:
            # If the return code is good, get the list of avatars
            # First, get the number of avatars
            avatarTotal = di.getUint16()
            assert (avatarTotal <= self.avatarLimit) and (avatarTotal >= 0)
            avList = []

            #print di.getDatagram().dumpHex(ostream)
            for i in range(0, avatarTotal):
                # Get the avatar id number
                avNum = di.getUint32()
                # Get the avatar name waffle
                # avNames is a list of the toon's name, wantName,
                # approvedName, and rejectedName
                #   name is distributed while the other three are
                # specialized for makeatoon process
                avNames = ["","","",""]
                avNames[0] = di.getString()

                avNames[1] = di.getString()
                avNames[2] = di.getString()
                avNames[3] = di.getString()

                # Get the avatar DNA
                avDNA = di.getString()
                # Get the avatar position
                avPosition = di.getUint8()
                # We have to get info about the name here
                aname = di.getUint8()
                # print "aname = " + str(aname)
                # Assemble the data
                potAv = PotentialAvatar(
                    avNum, avNames, avDNA, avPosition, aname)
                # Put it on the list
                avList.append(potAv)

            # save for future use
            self.avList = avList
            # Now, we can move on to choosing an avatar
            self.loginFSM.request("chooseAvatar", [self.avList])
        else:
            # Bad news. Go to "shutdown" mode
            self.notify.error("Bad avatar list return code: " + str(returnCode))
            self.loginFSM.request("shutdown")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleGetAvatarsResp2Msg(self, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Get the return code
        returnCode = di.getUint8()
        if returnCode == 0:
            # If the return code is good, get the list of avatars
            # First, get the number of avatars
            avatarTotal = di.getUint16()
            assert (avatarTotal <= self.avatarLimit) and (avatarTotal >= 0)
            avList = []

            #print di.getDatagram().dumpHex(ostream)
            for i in range(0, avatarTotal):
                # Get the avatar id number
                avNum = di.getUint32()
                # Get the avatar name waffle
                # resp2 reports only the actual avatar name for now
                avNames = ["","","",""]
                avNames[0] = di.getString()

                # resp2 doesn't report avatar DNA
                avDNA = None
                # Get the avatar position
                avPosition = di.getUint8()
                # resp2 doesn't report aname
                aname = None
                # Assemble the data
                potAv = PotentialAvatar(
                    avNum, avNames, avDNA, avPosition, aname)
                # Put it on the list
                avList.append(potAv)

            # save for future use
            self.avList = avList
            # Now, we can move on to choosing an avatar
            self.loginFSM.request("chooseAvatar", [self.avList])
        else:
            # Bad news. Go to "shutdown" mode
            self.notify.error("Bad avatar list return code: " + str(returnCode))
            self.loginFSM.request("shutdown")

    ##### LoginFSM: chooseAvatar #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterChooseAvatar(self, avList):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitChooseAvatar(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass

    ##### LoginFSM: createAvatar #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterCreateAvatar(self, avList, index, newDNA=None):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitCreateAvatar(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendCreateAvatarMsg(self, avDNA, avName, avPosition):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Create a new avatar
        datagram = PyDatagram()
        # Add a message type
        datagram.addUint16(CLIENT_CREATE_AVATAR)
        # Add an echo context ... This appears to be unnecessary
        datagram.addUint16(0)
        # Put in the new name and DNA
        # sdn: we no longer send the name
        #datagram.addString(avName)
        datagram.addString(avDNA.makeNetString())
        datagram.addUint8(avPosition)
        self.newName = avName
        self.newDNA = avDNA
        self.newPosition = avPosition
        # Send the message
        self.send(datagram)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendCreateAvatar2Msg(self, avClass, avDNA, avName, avPosition):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Sends the new create-avatar message that creates an avatar
        # of a type other than DistributedToon.  avClass should be the
        # class of avatar to create,
        # e.g. DistributedPlayerPirate.DistributedPlayerPirate,
        # DistributedTeen.DistributedTeen, or
        # DistributedToon.DistributedToon.

        # Note that avDNA and avName are not sent to the server.

        className = avClass.__name__
        dclass = self.dclassesByName[className]

        datagram = PyDatagram()
        datagram.addUint16(CLIENT_CREATE_AVATAR2)
        datagram.addUint16(0)  # echo context

        datagram.addUint8(avPosition)
        datagram.addUint16(dclass.getNumber())

        self.newName = avName
        self.newDNA = avDNA
        self.newPosition = avPosition
        self.send(datagram)


    ##### LoginFSM: waitForDeleteAvatarResponse #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitForDeleteAvatarResponse(self, potAv):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleWaitForDeleteAvatarResponse
        # Send the delete avatar message
        self.sendDeleteAvatarMsg(potAv.id)
        self.waitForDatabaseTimeout(requestName='WaitForDeleteAvatarResponse')

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendDeleteAvatarMsg(self, avId):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Delete the avatar
        datagram = PyDatagram()
        # Add a message type
        datagram.addUint16(CLIENT_DELETE_AVATAR)
        # Put in the new name and DNA
        datagram.addUint32(avId)
        # Send the message
        self.send(datagram)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitForDeleteAvatarResponse(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.cleanupWaitingForDatabase()
        self.handler = None

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleWaitForDeleteAvatarResponse(self, msgType, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if msgType == CLIENT_DELETE_AVATAR_RESP:
            # code re-use!
            self.handleGetAvatarsRespMsg(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        else:
            self.handleMessageType(msgType, di)

    ##### LoginFSM: rejectRemoveAvatar #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterRejectRemoveAvatar(self, reasonCode):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.warning("Rejected removed avatar. (%s)"%(reasonCode,))
        self.handler = self.handleMessageType
        # Create a dialog box
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.rejectRemoveAvatarBox = dialogClass(
            message = "%s\n(%s)"%(OTPLocalizer.CRRejectRemoveAvatar, reasonCode),
            doneEvent = "rejectRemoveAvatarAck",
            style = OTPDialog.Acknowledge)
        self.rejectRemoveAvatarBox.show()
        # Hang a hook for hitting OK or Cancel
        self.accept("rejectRemoveAvatarAck", self.__handleRejectRemoveAvatar)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def __handleRejectRemoveAvatar(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.loginFSM.request("chooseAvatar")

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitRejectRemoveAvatar(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None
        self.ignore("rejectRemoveAvatarAck")
        self.rejectRemoveAvatarBox.cleanup()
        del self.rejectRemoveAvatarBox

    ##### WaitForSetAvatarResponse state #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitForSetAvatarResponse(self, potAv):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = self.handleWaitForSetAvatarResponse
        # Send the set avatar message
        self.sendSetAvatarMsg(potAv)
        self.waitForDatabaseTimeout(requestName='WaitForSetAvatarResponse')

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitForSetAvatarResponse(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.cleanupWaitingForDatabase()
        self.handler = None

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendSetAvatarMsg(self, potAv):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Add the avatar id
        self.sendSetAvatarIdMsg(potAv.id)
        # Record the avatar data for easy creation
        self.avData = potAv

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def sendSetAvatarIdMsg(self, avId):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if avId != self.__currentAvId:
            self.__currentAvId = avId
            # Choose an avatar
            datagram = PyDatagram()
            # Add a message type
            datagram.addUint16(CLIENT_SET_AVATAR)
            # Add the avatar id
            datagram.addUint32(avId)
            # Send the message
            self.send(datagram)

            if avId == 0:
                # avId 0 means the avatar is logging out; stop the
                # timer.
                self.stopPeriodTimer()
            else:
                # A non-zero avId means an avatar is logging in; start
                # the timer.
                self.startPeriodTimer()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleAvatarResponseMsg(self, di):
        # Inheritors should overwrite
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleWaitForSetAvatarResponse(self, msgType, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
            self.handleAvatarResponseMsg(di)
        elif msgType == CLIENT_GET_PET_DETAILS_RESP:
            self.handleAvatarResponseMsg(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_RESP:
            self.handleGetFriendsList(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_EXTENDED_RESP:
            self.handleGetFriendsListExtended(di)
        elif msgType == CLIENT_FRIEND_ONLINE:
            self.handleFriendOnline(di)
        elif msgType == CLIENT_FRIEND_OFFLINE:
            self.handleFriendOffline(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        else:
            self.handleMessageType(msgType, di)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterPlayingGame(self):
        # override and do whatever is necessary to get the avatar into the game
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitPlayingGame(self):
        # Throw an event so systems can clean themselves up before
        # we scrub around looking for leaks.
        self.notify.info("sending clientLogout")
        messenger.send("clientLogout")

#################################################
##                    _             _       ______ _____ __  __
##                /  | |           (_)     |  ____/ ____|  \/  |
##               /   | | ___   __ _ _ _ __ | |__ | (___ | \  / |
##              /    | |/ _ \ / _` | | '_ \|  __| \___ \| |\/| |
##             /     | | (_) | (_| | | | | | |    ____) | |  | |
##            /      |_|\___/ \__, |_|_| |_|_|   |_____/|_|  |_|
##           /                 __/ |
##          /                 |___/
##         /           __                  _   _
##        /           / _|                | | (_)
##       /           | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
##      /            |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
##     /             | | | |_| | | | | (__| |_| | (_) | | | \__ \
##    /              |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
##
#################################################

    def detectLeaks(self, okTasks=None, okEvents=None):
        if (not __dev__) or \
           configIsToday("allow-unclean-exit"):
            assert self.notify.warning("Not enforcing clean exit.")
            return
        
        leakedTasks = self.detectLeakedTasks(okTasks)
        leakedEvents = self.detectLeakedEvents(okEvents)
        leakedIvals = self.detectLeakedIntervals()
        leakedGarbage = self.detectLeakedGarbage()

        if (leakedTasks or leakedEvents or leakedIvals or leakedGarbage):
            # if we are leaving to do something specific on the website,
            # like buying the game, don't treat leaks as errors
            # this is temporary until we pull in the new launcher code in production
            #errorCode = launcher.getPandaErrorCode()
            errorCode = base.getExitErrorCode()
            if ((errorCode >= OTPLauncherGlobals.NonErrorExitStateStart) and
                (errorCode <= OTPLauncherGlobals.NonErrorExitStateEnd)):
                # log the leaks and continue on
                logFunc = self.notify.warning
                allowExit = True
            else:
                if __debug__:
                    # log the leaks and stop the client
                    logFunc = self.notify.error
                    allowExit = False
                else:
                    # In production, lets log the warning so we can do triage, but let
                    # the user go ahead and exit / logout without submitting a bug.
                    logFunc = self.notify.warning
                    allowExit = False
            if base.config.GetBool("direct-gui-edit", 0):
                logFunc("There are leaks: %s tasks, %s events, %s ivals, %s garbage cycles\nLeaked Events may be due to direct gui editing" %
                        (leakedTasks, leakedEvents, leakedIvals, leakedGarbage))
            else:        
                logFunc("There are leaks: %s tasks, %s events, %s ivals, %s garbage cycles" %
                        (leakedTasks, leakedEvents, leakedIvals, leakedGarbage))
            if allowExit:
                self.notify.info('Allowing client to leave, panda error code %s' % errorCode)
            else:
                base.userExit()
        else:
            self.notify.info("There are no leaks detected.")

    def detectLeakedGarbage(self, callback=None): 
        if not __debug__:
            return 0
        self.notify.info('checking for leaked garbage...')
        if gc.garbage:
            self.notify.warning("garbage already contains %d items" % len(gc.garbage))
        report = GarbageReport.GarbageReport('logout', verbose=True)
        numCycles = report.getNumCycles()
        if numCycles:
            msg = "You can't leave until you take out your garbage. See report above & base.garbage"
            self.notify.info(msg)
        report.destroy()
        return numCycles

    def detectLeakedTasks(self, extraTasks=None):
        # Make sure there are no leftover tasks that shouldn't be here.
        allowedTasks = ["dataLoop",
                        "resetPrevTransform",
                        "doLaterProcessor",
                        "eventManager",
                        "readerPollTask",
                        "heartBeat",
                        "gridZoneLoop",
                        "igLoop",
                        "audioLoop",
                        "asyncLoad",
                        "collisionLoop",
                        "shadowCollisionLoop",
                        "ivalLoop",
                        "downloadSequence",
                        "patchAndHash",
                        "launcher-download",
                        "launcher-download-multifile",
                        "launcher-decompressFile",
                        "launcher-decompressMultifile",
                        "launcher-extract",
                        "launcher-patch",
                        "slowCloseShardCallback",
                        "tkLoop",
                        "manager-update",
                        "downloadStallTask",
                        "clientSleep",
                        jobMgr.TaskName,
                        self.GarbageCollectTaskName,
                        "RedownloadNewsTask", #in another taskChain and taskMgr.remove doesnt work
                        ]
        if extraTasks is not None:
            allowedTasks.extend(extraTasks)
        problems = []
        for task in taskMgr.getTasks():
            if not hasattr(task, 'name'):
                # this allows pure-C++ tasks, which are all
                # 'non-leaking' at the moment
                # TODO: come up with a good way to differentiate
                # C++ & Python tasks that are OK to 'leak' from those
                # that aren't
                continue
            if task.name in allowedTasks:
                continue
            else:
                if hasattr(task, "debugInitTraceback"):
                    print task.debugInitTraceback
                problems.append(task.name)
        if problems:
            print taskMgr
            msg = "You can't leave until you clean up your tasks: {"
            for task in problems:
                msg += "\n  " + task
            msg += "}\n"
            self.notify.info(msg)
            return len(problems)
        else:
            return 0

    def detectLeakedEvents(self, extraHooks=None):
        # Make sure there are no leftover hooks that shouldn't be here.
        allowedHooks = ["destroy-DownloadWatcherBar",
                        "destroy-DownloadWatcherText",
                        "destroy-fade",
                        "f9", "control-f9",
                        "launcherAllPhasesComplete",
                        "launcherPercentPhaseComplete",
                        "newDistributedDirectory",
                        "page_down",
                        "page_up",
                        "panda3d-render-error",
                        "PandaPaused",
                        "PandaRestarted",
                        "phaseComplete-3",
                        "press-mouse2-fade",
                        "print-fade",
                        "release-mouse2-fade",
                        "resetClock",
                        "window-event",
                        "TCRSetZoneDone",
                        "aspectRatioChanged",
                        "newDistributedDirectory", # OTPserver only, but does not hurt either
                        CConnectionRepository.getOverflowEventName(),
                        self._getLostConnectionEvent(),
                        'render-texture-targets-changed',
                        'gotExtraFriendHandles'
                        ]
        if hasattr(loader, 'hook'):
            allowedHooks.append(loader.hook)
        if extraHooks is not None:
            allowedHooks.extend(extraHooks)
        problems = []
        for hook in messenger.getEvents():
            if hook not in allowedHooks:
                problems.append(hook)
        if problems:
            msg = "You can't leave until you clean up your messenger hooks: {"
            for hook in problems:
                whoAccepts = messenger.whoAccepts(hook)
                msg += "\n  %s" % hook
                for obj in whoAccepts:
                    msg += '\n   OBJECT:%s, %s %s' % (obj, obj.__class__, whoAccepts[obj])
                    if hasattr(obj, 'getCreationStackTraceCompactStr'):
                        msg += '\n   CREATIONSTACKTRACE:%s' % obj.getCreationStackTraceCompactStr()
                    else:
                        try:
                            # there are so many ways this could fail that it's in a try block
                            value = whoAccepts[obj]
                            callback = value[0]
                            guiObj = callback.im_self
                            if hasattr(guiObj, 'getCreationStackTraceCompactStr'):
                                msg += '\n   CREATIONSTACKTRACE:%s' % guiObj.getCreationStackTraceCompactStr()
                        except:
                            pass
            msg += "\n}\n"
            self.notify.info(msg)
            return len(problems)
        else:
            return 0

    def detectLeakedIntervals(self):
        # Make sure there are no leftover intervals that shouldn't be here.
        numIvals = ivalMgr.getNumIntervals()
        if numIvals > 0:
            print "You can't leave until you clean up your intervals: {"
            for i in range(ivalMgr.getMaxIndex()):
                # We go through some effort to print each interval in
                # detail.  This means we need to find the interval.
                # Some intervals exist only as C intervals, some only
                # as Python intervals (although most are both).  We
                # prefer the Python pointer if it exists.
                ival = None
                if i < len(ivalMgr.ivals):
                    ival = ivalMgr.ivals[i]
                if ival == None:
                    ival = ivalMgr.getCInterval(i)
                if ival:
                    print ival
                    if hasattr(ival, "debugName"):
                        print ival.debugName
                    if hasattr(ival, "debugInitTraceback"):
                        print ival.debugInitTraceback
            print "}"
            self.notify.info(
                "You can't leave until you clean up your intervals.")
            return numIvals
        else:
            return 0


    def _abandonShard(self):
        # Override and do whatever is necessary to shut down our shard
        # interest without waiting for interest-complete messages.
        self.notify.error('%s must override _abandonShard' %
                          self.__class__.__name__)


#####################################################
##                              ______ _____ __  __
##                             |  ____/ ____|  \/  |
##    __ _  __ _ _ __ ___   ___| |__ | (___ | \  / |
##   / _` |/ _` | '_ ` _ \ / _ \  __| \___ \| |\/| |
##  | (_| | (_| | | | | | |  __/ |    ____) | |  | |
##   \__, |\__,_|_| |_| |_|\___|_|   |_____/|_|  |_|
##    __/ |
##   |___/
##    __                  _   _
##   / _|                | | (_)
##  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
##  |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
##  | | | |_| | | | | (__| |_| | (_) | | | \__ \
##  |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
##
#####################################################

    ##### gameFSM: gameOff #####
    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterGameOff(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.uberZoneInterest = None
        # If cleanGameExit doesn't exist, we haven't run the game yet.
        # If cleanGameExit is True, we're exiting the game through normal means.
        # If False, we got disconnected (or closed the window, etc.)
        if not hasattr(self, 'cleanGameExit'):
            self.cleanGameExit = True

        if self.cleanGameExit:
            if self.isShardInterestOpen():
                # error, we didn't close up the shard interest
                self.notify.error('enterGameOff: shard interest is still open')
            # the cache should be empty at this point
            assert self.cache.isEmpty()
        else:
            # we left the game suddenly and uncleanly (disconnected,
            # closed window, etc.)
            # remove the shard interest manually (don't wait for network
            # deletes)
            if self.isShardInterestOpen():
                self.notify.warning('unclean exit, abandoning shard')
                self._abandonShard()

        self.cleanupWaitAllInterestsComplete()

        del self.cleanGameExit

        # make sure the cache is empty
        self.cache.flush()
        self.doDataCache.flush()

        self.handler = self.handleMessageType
        #Commented out the following lines. Too aggressive, kills preloading
        #benefit from character creation and starting game. Will replace
        #with unloads at the pirates level
        #ModelPool.garbageCollect()
        #TexturePool.garbageCollect()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitGameOff(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.handler = None

    ##### gameFSM: waitOnEnterResponses #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # By default, set cleanGameExit to False, and set it to True
        # before leaving cleanly.
        self.cleanGameExit = False
        self.handler = self.handleWaitOnEnterResponses
        self.handlerArgs = {"hoodId": hoodId,
                            "zoneId": zoneId,
                            "avId": avId}
        ## roger -->changed to some resonable login.. like lowest population
        if shardId is not None:
            district = self.activeDistrictMap.get(shardId)
        else:
            district = None
        if not district:
            self.distributedDistrict = self.getStartingDistrict()
            if self.distributedDistrict is None:
                self.loginFSM.request("noShards")
                return
            shardId = self.distributedDistrict.doId
        else:
            self.distributedDistrict = district

        self.notify.info("Entering shard %s" % (shardId))
        localAvatar.setLocation(shardId, zoneId)

        base.localAvatar.defaultShard = shardId
        # Sleep for a moment to let the messages process on the game
        # server. We can remove this if Roger reworks some of the server.
        # There is a race condition.
        self.waitForDatabaseTimeout(requestName='WaitOnEnterResponses')

        # We will also assume that we picked a good shard and zone.
        # Two responses will come back, and they will be ignored.
        self.handleSetShardComplete()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleWaitOnEnterResponses(self, msgType, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if msgType == CLIENT_GET_FRIEND_LIST_RESP:
            self.handleGetFriendsList(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_EXTENDED_RESP:
            self.handleGetFriendsListExtended(di)
        elif msgType == CLIENT_FRIEND_ONLINE:
            self.handleFriendOnline(di)
        elif msgType == CLIENT_FRIEND_OFFLINE:
            self.handleFriendOffline(di)
        elif msgType == CLIENT_GET_PET_DETAILS_RESP:
            self.handleGetAvatarDetailsResp(di)
        else:
            self.handleMessageType(msgType, di)

    # In the OTP server you do not need to go into the quiet zone
    # to manifest uberzone objects, you can just add interest to the
    # shard's uber zone.

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleSetShardComplete(self):
        self.cleanupWaitingForDatabase()
        # Eventually, this should do some error checking, for now I'll
        # assume that everything is AOK
        hoodId = self.handlerArgs["hoodId"]
        zoneId = self.handlerArgs["zoneId"]
        avId = self.handlerArgs["avId"]

        # We will not go to the quiet zone anymore, now we will just
        # register interest in the zone where the uber objects
        # (TimeManager, etc) live. This happens to be in the District's
        # uber zone (2).
        self.uberZoneInterest = self.addInterest(
            base.localAvatar.defaultShard,
            OTPGlobals.UberZone,
            "uberZone",
            "uberZoneInterestComplete")
        self.acceptOnce("uberZoneInterestComplete", self.uberZoneInterestComplete)
        # Listen for the arrival of the time manager and tutorial manager.
        self.waitForDatabaseTimeout(20, requestName='waitingForUberZone')

    # This replaces the old "reachedQuietZone()"
    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def uberZoneInterestComplete(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.__gotTimeSync = 0

        self.cleanupWaitingForDatabase()

        # Now we're in the UBER zone, and presumably we've seen the
        # TimeManager created by now.  Wait just a little bit longer,
        # if necessary, for the sync message to complete its round
        # trip.
        if self.timeManager == None:
            # If we don't have a time manager, we're probably running
            # without an AI, so never mind.
            self.notify.info("TimeManager is not present.")
            DistributedSmoothNode.globalActivateSmoothing(0, 0)
            self.gotTimeSync()
        else:
            # Since we have a TimeManager, we can enable motion
            # smoothing.  But we don't enable predictive smoothing by
            # default.
            DistributedSmoothNode.globalActivateSmoothing(1, 0)

            # Also get the prc hash and signature, and send 'em up.
            h = HashVal()
            hashPrcVariables(h)

            pyc = HashVal()
            if not __dev__:
                self.hashFiles(pyc)
            
            self.timeManager.d_setSignature(self.userSignature, h.asBin(),
                                            pyc.asBin())
            self.timeManager.sendCpuInfo()

            # Ask the TimeManager to sync us up.
            if self.timeManager.synchronize("startup"):
                self.accept("gotTimeSync", self.gotTimeSync)
                self.waitForDatabaseTimeout(requestName='uberZoneInterest-timeSync')
            else:
                # For some reason, the TimeManager didn't want to
                # sync.  Presumably it just synced for some other
                # reason, so never mind.
                self.notify.info("No sync from TimeManager.")
                self.gotTimeSync()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitWaitOnEnterResponses(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.ignore('uberZoneInterestComplete')
        self.cleanupWaitingForDatabase()
        self.handler = None
        self.handlerArgs = None


    ##### gameFSM: CloseShard #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterCloseShard(self, loginState=None):
        # override and call _removeLocalAvFromStateServer when you're
        # ready
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.info("Exiting shard")
        if loginState is None:
            loginState = "waitForAvatarList"
        self._closeShardLoginState = loginState
        # set a flag to prevent new interests from being opened
        base.cr.setNoNewInterests(True)
        if __debug__:
            base.cr.printInterests()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _removeLocalAvFromStateServer(self):
        assert self.notify.debug("_removeLocalAvFromStateServer: about to sendSetAvatarIdMsg 0")
        # Now we can safely remove the avatar from the state server
        self.sendSetAvatarIdMsg(0)
        self._removeAllOV()
        callback = Functor(self.loginFSM.request, self._closeShardLoginState)
        if base.slowCloseShard:
            taskMgr.doMethodLater(
                base.slowCloseShardDelay*.5,
                Functor(self.removeShardInterest, callback),
                'slowCloseShard')
        else:
            self.removeShardInterest(callback)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _removeAllOV(self):
        # force delete for all owner-view objects, OTP server has done the same on its end
        ownerDoIds = self.doId2ownerView.keys()
        for doId in ownerDoIds:
            self.disableDoId(doId, ownerView=True)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def isShardInterestOpen(self):
        # override this and return True if we've got a shard interest open
        self.notify.error('%s must override isShardInterestOpen' %
                          self.__class__.__name__)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def removeShardInterest(self, callback, task=None):
        self._removeCurrentShardInterest(
            Functor(self._removeShardInterestComplete, callback))
    
    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _removeShardInterestComplete(self, callback):
        # We've removed interest in the current shard. That constitutes
        # a clean game exit. If we enter another shard, this will be set
        # to False again.
        self.cleanGameExit = True
        # flush out the DO cache
        self.cache.flush()
        self.doDataCache.flush()
        if base.slowCloseShard:
            taskMgr.doMethodLater(
                base.slowCloseShardDelay*.5,
                Functor(self._callRemoveShardInterestCallback, callback),
                'slowCloseShardCallback')
        else:
            self._callRemoveShardInterestCallback(callback, None)
    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _callRemoveShardInterestCallback(self, callback, task):
        callback()
        return Task.done

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _removeCurrentShardInterest(self, callback):
        # Override this and do whatever is necessary to close interest
        # in the current shard. Call callback when done.
        self.notify.error('%s must override _removeCurrentShardInterest' %
                          self.__class__.__name__)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitCloseShard(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        del self._closeShardLoginState
        # clear the flag and allow interests to be opened again
        base.cr.setNoNewInterests(False)

    ##### gameFSM: tutorial question #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitTutorialQuestion(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        pass


    ##### gameFSM: play game #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterPlayGame(self, hoodId, zoneId, avId):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Stop the music that started in ToontownStart
        if self.music:
            self.music.stop()
            self.music = None

        self.garbageLeakLogger = GarbageLeakServerEventAggregator(self)

        self.handler = self.handlePlayGame

        self.accept(self.gameDoneEvent, self.handleGameDone)
        base.transitions.noFade()

        self.playGame.load()
        # TODO: pull in bulk load into pirates or OTP
        try:
            loader.endBulkLoad("localAvatarPlayGame")
        except:
            pass
        self.playGame.enter(hoodId, zoneId, avId)

        def checkScale(task):
            # Spammy --> assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
            assert base.localAvatar.getTransform().hasUniformScale()
            return Task.cont
        assert taskMgr.add(checkScale, 'globalScaleCheck')

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def handleGameDone(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # The PlayGame ClassicFSM exited.  This normally happens only when
        # the player wants to teleport to another shard; in that case,
        # we have to back all the way out of the previous PlayGame
        # state, switch shards up here, then go all the way back in on
        # the new shard.

        if self.timeManager:
            self.timeManager.setDisconnectReason(OTPGlobals.DisconnectSwitchShards)

        doneStatus = self.playGame.getDoneStatus()
        how = doneStatus["how"]
        shardId = doneStatus["shardId"]
        hoodId = doneStatus["hoodId"]
        zoneId = doneStatus["zoneId"]
        avId = doneStatus["avId"]

        if how == "teleportIn":
            # We only know how to teleport in when we enter a zone
            # from way up here.
            # Wait for the shard to go away
            self.gameFSM.request(
                "switchShards", [shardId, hoodId, zoneId, avId])
        else:
            self.notify.error("Exited shard with unexpected mode %s" % (how))

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitPlayGame(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        taskMgr.remove('globalScaleCheck')

        self.handler = None
        self.playGame.exit()
        self.playGame.unload()

        self.ignore(self.gameDoneEvent)

        self.garbageLeakLogger.destroy()
        del self.garbageLeakLogger

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def gotTimeSync(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.info("gotTimeSync")
        self.ignore("gotTimeSync")
        self.__gotTimeSync = 1
        self.moveOnFromUberZone()

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def moveOnFromUberZone(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if not self.__gotTimeSync:
            self.notify.info("Waiting for time sync.")
            return

        hoodId = self.handlerArgs["hoodId"]
        zoneId = self.handlerArgs["zoneId"]
        avId = self.handlerArgs["avId"]

        # It's safe to either go into the actual game, or prompt for a
        # tutorial if desired.

        # If the player has acknowledged the tutorial opportunity sometime
        # in the past, just go play the game. Otherwise, ask them if
        # they would like a tutorial.
        if not self.SupportTutorial or base.localAvatar.tutorialAck:
            # No tutorial question... go play the game!
            self.gameFSM.request("playGame", [hoodId, zoneId, avId])
        else:
            if base.config.GetBool('force-tutorial', 1):
                # By default, we ask the tutorial question, unless it
                # is DConfig'ed off.
                # or they clicked on skip tutorial
                if hasattr(self,"skipTutorialRequest") and self.skipTutorialRequest:
                    # hack we go to playGame to get the toon on the AI
                    self.gameFSM.request("playGame", [hoodId, zoneId, avId])
                    # Ask the tutorial manager to skip our tutorial
                    self.gameFSM.request("skipTutorialRequest", [hoodId, zoneId, avId])
                else:
                    self.gameFSM.request("tutorialQuestion", [hoodId, zoneId, avId])
            else:
                # It's been DConfig'ed off. Go play!
                self.gameFSM.request("playGame", [hoodId, zoneId, avId])

    def handlePlayGame(self, msgType, di):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if self.notify.getDebug():
            self.notify.debug("handle play game got message type: " + `msgType`)
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequiredOther(di)
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_DISABLE_RESP:
            self.handleDisable(di)
        elif msgType == CLIENT_OBJECT_DELETE_RESP:
            assert 0
            self.handleDelete(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_RESP:
            self.handleGetFriendsList(di)
        elif msgType == CLIENT_GET_FRIEND_LIST_EXTENDED_RESP:
            self.handleGetFriendsListExtended(di)
        elif msgType == CLIENT_FRIEND_ONLINE:
            self.handleFriendOnline(di)
        elif msgType == CLIENT_FRIEND_OFFLINE:
            self.handleFriendOffline(di)
        elif msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
            self.handleGetAvatarDetailsResp(di)
        elif msgType == CLIENT_GET_PET_DETAILS_RESP:
            self.handleGetAvatarDetailsResp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_UP:
        #Roger wants to remove this     self.handleServerUp(di)
        #Roger wants to remove this elif msgType == CLIENT_SERVER_DOWN:
        #Roger wants to remove this     self.handleServerDown(di)
        #Roger wants to remove this elif msgType == CLIENT_GET_SHARD_LIST_RESP:
        #Roger wants to remove this     self.handleGetShardListResponseMsg(di)
        # Moved to handleMessageType elif msgType == CLIENT_GET_STATE_RESP:
        # Moved to handleMessageType     di.skipBytes(12)
        # Moved to handleMessageType     zoneId = di.getInt32()
        # Moved to handleMessageType     # HACK! This should really be handled.
        # Moved to handleMessageType     pass
        else:
            self.handleMessageType(msgType, di)

    ##### gameFSM: switch shards #####

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def enterSwitchShards(self, shardId, hoodId, zoneId, avId):
        self._switchShardParams = [shardId, hoodId, zoneId, avId]
        # remove any interests in the old shard
        localAvatar.setLeftDistrict()
        self.removeShardInterest(self._handleOldShardGone)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def _handleOldShardGone(self):
        self.gameFSM.request(
            "waitOnEnterResponses", self._switchShardParams)

    @report(types = ['args', 'deltaStamp'], dConfigParam = 'teleport')
    def exitSwitchShards(self):
        pass

#####################################################
##                                           ______ _____ __  __
##             /                            |  ____/ ____|  \/  |
##            /    __ _  __ _ _ __ ___   ___| |__ | (___ | \  / |
##           /    / _` |/ _` | '_ ` _ \ / _ \  __| \___ \| |\/| |
##          /    | (_| | (_| | | | | | |  __/ |    ____) | |  | |
##         /      \__, |\__,_|_| |_| |_|\___|_|   |_____/|_|  |_|
##        /        __/ |
##       /        |___/
##      /          __                  _   _
##     /          / _|                | | (_)
##    /          | |_ _   _ _ __   ___| |_ _  ___  _ __  ___
##   /           |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
##  /            | | | |_| | | | | (__| |_| | (_) | | | \__ \
## /             |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
##
#####################################################

    ###################################################
    # Utility Functions
    ###################################################

    ######### Account information #########

    def isFreeTimeExpired(self):
        """
        Returns 1 if the user has no more free playing time remaining.
             or 0 if the user may still play for free.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if self.accountOldAuth:
            return 0

        # check for the config overrides
        # if true, free-time-expired takes precedence over unlimited-free-time
        if base.config.GetBool("free-time-expired", 0):
            return 1
        if base.config.GetBool("unlimited-free-time", 0):
            return 0

        # -1 == never expires (paid/exempt)
        if self.freeTimeExpiresAt == -1:
            return 0

        # 0 == expired
        if self.freeTimeExpiresAt == 0:
            return 1

        if self.freeTimeExpiresAt < -1:
            self.notify.warning('freeTimeExpiresAt is less than -1 (%s)' %
                                self.freeTimeExpiresAt)

        # freeTimeExpiresAt is an epoch time
        # is it in the past?
        if self.freeTimeExpiresAt < time.time():
            return 1
        else:
            return 0

    def freeTimeLeft(self):
        """
        returns number of seconds of free time that the player has left
        if player has already paid, or they are out of time, returns 0
        (if they've already paid, there's no reason to use this function;
        see isPaid())
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # -1 == never expires (paid/exempt)
        # 0 == expired
        if self.freeTimeExpiresAt == -1 or \
           self.freeTimeExpiresAt == 0:
            return 0

        # freeTimeExpiresAt is an epoch time
        secsLeft = self.freeTimeExpiresAt - time.time()
        # if free time just expired, secsLeft <=0
        # make sure we don't return a negative number
        return max(0, secsLeft)

    def isWebPlayToken(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return self.playToken!=None

    def isBlue(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return self.blue!=None

    def isPaid(self):
        """
        For Toontown:
             Returns 1 if the user has paid or 0 if the user has not paid.
        For Pirates:
             Returns OTPGlobals.AccessUnknown, OTPGlobals.VelvetRope, or OTPGlobals.Full
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        paidStatus = base.config.GetString('force-paid-status', '')
        if not paidStatus:
            return self.__isPaid
        elif paidStatus == 'paid':
            return 1
        elif paidStatus == 'unpaid':
            return 0
        elif paidStatus == 'FULL':
            return OTPGlobals.AccessFull
        elif paidStatus == 'VELVET':
            return OTPGlobals.AccessVelvetRope
        else:
            return 0


    def setIsPaid(self, isPaid):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.__isPaid=isPaid 

    def allowFreeNames(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Do we allow free trialers to name their toon?
        return base.config.GetInt("allow-free-names", 1)

    def allowSecretChat(self):
        """
        Returns true if any keyboard chat, including via the "secret
        friends" interface, should be allowed, or false if all of
        these interfaces should be suppressed for the current player.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return (self.secretChatAllowed or \
               (self.productName == "Terra-DMC" and self.isBlue() and self.secretChatAllowed))
               
    def allowWhiteListChat(self):
        if hasattr(self,'whiteListChatEnabled') and self.whiteListChatEnabled:
            return True
        else:
            return False
            
               
    def allowAnyTypedChat(self):
        if self.allowSecretChat() or self.allowWhiteListChat() or self.allowOpenChat():
            return True
        else:
            return False

    def allowOpenChat(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return self.openChatAllowed

    def isParentPasswordSet(self):
        return self.parentPasswordSet

    def needParentPasswordForSecretChat(self):
        """
        Returns true if the "secret friends" interface requires use of the Parent Password.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        return ((self.isPaid() and self.secretChatNeedsParentPassword) or
                (self.productName == "Terra-DMC" and self.isBlue() and self.secretChatNeedsParentPassword))

    def logAccountInfo(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.info('*** ACCOUNT INFO ***')
        self.notify.info('username: %s' % self.userName)
        if self.blue:
            self.notify.info('paid: %s (blue)' % self.isPaid())
        else:
            self.notify.info('paid: %s' % self.isPaid())
        if not self.isPaid():
            if self.isFreeTimeExpired():
                self.notify.info('free time is expired')
            else:
                secs = self.freeTimeLeft()
                self.notify.info(
                    'free time left: %s' %
                    (PythonUtil.formatElapsedSeconds(secs)))
        if self.periodTimerSecondsRemaining != None:
            self.notify.info(
                'period time left: %s' %
                (PythonUtil.formatElapsedSeconds(self.periodTimerSecondsRemaining)))

    ######### Shard information #########
    def getStartingDistrict(self):
        """
        Get a Proper District For a starting location
        None if no District in core
        """
        district = None

        if len(self.activeDistrictMap.keys()) == 0:
            self.notify.info('no shards')
            return None

        if base.fillShardsToIdealPop:
            # Choose highest-population shard that is not yet
            # a 'high-population' shard
            lowPop, midPop, highPop = base.getShardPopLimits()
            self.notify.debug('low: %s mid: %s high: %s' %
                             (lowPop, midPop, highPop))
            for s in self.activeDistrictMap.values():
                if s.available and s.avatarCount < lowPop:
                    self.notify.debug('%s: pop %s' %
                                     (s.name, s.avatarCount))
                    if district is None:
                        district = s
                    else:
                        # if multiple shards have the same population,
                        # sort them by name so that all clients will
                        # choose the same one
                        if s.avatarCount > district.avatarCount or (
                            (s.avatarCount == district.avatarCount and
                             s.name > district.name)
                            ):
                            district = s

        # if all of the shards are over the cutoff population, pick
        # the lowest-population shard
        if district is None:
            self.notify.debug(
                'all shards over cutoff, picking lowest-population shard')
            for s in self.activeDistrictMap.values():
                if s.available:
                    self.notify.debug('%s: pop %s' %
                                     (s.name, s.avatarCount))
                    if (district is None or
                        (s.avatarCount < district.avatarCount)):
                            district = s

        if district is not None:
            self.notify.debug('chose %s: pop %s' % (district.name, district.avatarCount))
        return district

    def getShardName(self, shardId):
        """
        Returns the name associated with the indicated shard ID, or
        None if the shard is unknown.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        try:
            return self.activeDistrictMap[shardId].name
        except:
            return None

    def isShardAvailable(self, shardId):
        """
        Returns true if the indicated shard is believed to be up and
        running at the moment, false otherwise.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        try:
            return self.activeDistrictMap[shardId].available
        except:
            return 0

    def listActiveShards(self):
        """
        Returns a list of tuples, such that each element of the list
        is a tuple of the form (shardId, name, population,
        welcomeValleyPopulation) for all the shards believed to be
        currently up and running, and accepting avatars.
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        list = []
        for s in self.activeDistrictMap.values():
            if s.available:
                list.append(
                        (s.doId, s.name, s.avatarCount,
                        s.newAvatarCount))
                
        return list


    ######### General senders and handlers #########

    def getPlayerAvatars(self):
        return [i for i in self.doId2do.values()
            if isinstance(i, DistributedPlayer)]

    if 0:
        #Roger wants to remove this
        def handleQueryOneFieldResp(self, di):
            doId = di.getUint32()
            fieldId = di.getUint16()
            context = di.getUint32()
            import pdb
            pdb.set_trace()

    if 0:
        #Roger wants to remove this
        def queryObjectFieldId(self, doId, fieldId, context=0):
            assert self.notify.debugStateCall(self)
            # Create a message
            datagram = PyDatagram()
            # The message type
            datagram.addUint16(CLIENT_QUERY_ONE_FIELD)
            # The doId we're asking about
            datagram.addUint32(doId)
            # The field id
            datagram.addUint16(fieldId)
            # A context that can be used to index the response if needed
            datagram.addUint32(context)
            # Send the message
            self.send(datagram)

    def queryObjectField(self, dclassName, fieldName, doId, context=0):
        assert self.notify.debugStateCall(self)
        assert len(dclassName) > 0
        assert len(fieldName) > 0
        assert doId > 0
        dclass = self.dclassesByName.get(dclassName)
        assert dclass is not None
        if dclass is not None:
            fieldId = dclass.getFieldByName(fieldName).getNumber()
            assert fieldId # is 0 a valid value?
            self.queryObjectFieldId(doId, fieldId, context)

    def allocateDcFile(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # NOTE: do not move this function into DIRECT
        # This method is deliberately misnamed.  It should actually be
        # called loadClientPassphrase(), but we are trying to make it
        # hard for a casual hacker to find it.

        # This method loads the passphrase needed to decode the client
        # private key for the server negotation.

        # This is the current passphrase seed.  It's chosen to
        # resemble an innocent string that's likely to be found in
        # this file.
        dcName = "Shard %s cannot be found."

        # We don't even use the above seed directly; instead, we md5
        # it first, and use the resulting md5 hex string as the actual
        # passphrase.
        hash = HashVal()
        hash.hashString(dcName)
        self.http.setClientCertificatePassphrase(hash.asHex())

    def lostConnection(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        ClientRepositoryBase.lostConnection(self)
        self.loginFSM.request("noConnection")

    def waitForDatabaseTimeout(self, extraTimeout = 0, requestName='unknown'):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        assert self.waitingForDatabase == None
        OTPClientRepository.notify.debug(
            'waiting for database timeout %s at %s' %
            (requestName, globalClock.getFrameTime()))
        # If nothing happens within a few seconds, pop up a dialog to
        # show we're still hanging on, and to give the user a chance
        # to bail.
        taskMgr.remove("waitingForDatabase")
        # tick the clock to ensure we start counting from now, instead
        # of from the beginning of the last frame (whenever that was).
        globalClock.tick()
        taskMgr.doMethodLater((OTPGlobals.DatabaseDialogTimeout + extraTimeout) * choice(__dev__, 10, 1),
                              self.__showWaitingForDatabase,
                              "waitingForDatabase", extraArgs=[requestName])

    def __showWaitingForDatabase(self, requestName):
        messenger.send("connectionIssue")
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        OTPClientRepository.notify.info("timed out waiting for %s at %s" % (
            requestName, globalClock.getFrameTime()))
        dialogClass = OTPGlobals.getDialogClass()
        self.waitingForDatabase = dialogClass(
            text = OTPLocalizer.CRToontownUnavailable,
            dialogName = "WaitingForDatabase",
            buttonTextList = [OTPLocalizer.CRToontownUnavailableCancel],
            style = OTPDialog.CancelOnly,
            command = self.__handleCancelWaiting)
        self.waitingForDatabase.show()
        taskMgr.remove("waitingForDatabase")
        taskMgr.doMethodLater(OTPGlobals.DatabaseGiveupTimeout,
                              self.__giveUpWaitingForDatabase,
                              "waitingForDatabase", extraArgs=[requestName])
        return Task.done

    def __giveUpWaitingForDatabase(self, requestName):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        OTPClientRepository.notify.info("giving up waiting for %s at %s" % (
            requestName, globalClock.getFrameTime()))
        self.cleanupWaitingForDatabase()
        self.loginFSM.request("noConnection")
        return Task.done

    def cleanupWaitingForDatabase(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        if self.waitingForDatabase != None:
            self.waitingForDatabase.hide()
            self.waitingForDatabase.cleanup()
            self.waitingForDatabase = None
        taskMgr.remove("waitingForDatabase")

    def __handleCancelWaiting(self, value):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.loginFSM.request("shutdown")

    def setIsNotNewInstallation(self):
        """
        Call this function whenever the user does something that would
        make this installation no longer 'new' (i.e., creates an account,
        logs in, etc.)
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        launcher.setIsNotNewInstallation()

    def renderFrame(self):
        """
        force a frame render; this is useful for screen transitions,
        where we destroy one screen and load the next; during the load,
        we don't want the user staring at the old screen
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')

        # Make sure any textures are preloaded before we render.
        gsg = base.win.getGsg()
        if gsg:
            render2d.prepareScene(gsg)

        base.graphicsEngine.renderFrame()

    def refreshAccountServerDate(self, forceRefresh=0):
        """ re-get the account server date
        if forceRefresh != 0, will unconditionally perform the get
        returns None on success
        """
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        try:
            self.accountServerDate.grabDate(force=forceRefresh)
        except TTAccount.TTAccountException, e:
            self.notify.debug(str(e))
            return 1


    ##################################################
    # Period Timer functions
    ##################################################

    def resetPeriodTimer(self, secondsRemaining):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Resets the period counter to the indicated number of seconds
        # of gameplay remaining on the clock.  Certain users may be
        # allowed only a limited amount of time in the game per month;
        # this limit is told us by the server when we log in.
        #
        # If secondsRemaining is None, it implies there is no limit.

        assert self.periodTimerStarted == None
        self.periodTimerExpired = 0
        self.periodTimerSecondsRemaining = secondsRemaining

    def recordPeriodTimer(self, task):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Periodically sets the time remaining time in the windows registry
        # so the DMC client can query it for its own display
        freq = 60.0  # How often to record in seconds
        # Write it to the registry using the launcher interface
        elapsed = globalClock.getRealTime() - self.periodTimerStarted
        # Subtract out this dolater time from the running time
        self.runningPeriodTimeRemaining = self.periodTimerSecondsRemaining - elapsed
        self.notify.debug("periodTimeRemaining: %s" % (self.runningPeriodTimeRemaining))
        launcher.recordPeriodTimeRemaining(self.runningPeriodTimeRemaining)
        # Now spawn a dolater waiting for the next
        taskMgr.doMethodLater(freq, self.recordPeriodTimer, "periodTimerRecorder")
        return Task.done

    def startPeriodTimer(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Starts the period timer counting down the number of seconds
        # till we need to boot the player out.
        if self.periodTimerStarted == None and \
           self.periodTimerSecondsRemaining != None:
            self.periodTimerStarted = globalClock.getRealTime()
            taskMgr.doMethodLater(self.periodTimerSecondsRemaining,
                                  self.__periodTimerExpired,
                                  "periodTimerCountdown")
            for warning in OTPGlobals.PeriodTimerWarningTime:
                if self.periodTimerSecondsRemaining > warning:
                    taskMgr.doMethodLater(self.periodTimerSecondsRemaining - warning,
                                          self.__periodTimerWarning,
                                          "periodTimerCountdown")
            # Initialize the running count of seconds remaining
            self.runningPeriodTimeRemaining = self.periodTimerSecondsRemaining
            # Kick off the period timer recording task
            self.recordPeriodTimer(None)

    def stopPeriodTimer(self):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        # Stop the period counter.
        if self.periodTimerStarted != None:
            elapsed = globalClock.getRealTime() - self.periodTimerStarted
            self.periodTimerSecondsRemaining -= elapsed
            self.periodTimerStarted = None
        taskMgr.remove("periodTimerCountdown")
        # Also remove the recorder
        taskMgr.remove("periodTimerRecorder")

    def __periodTimerWarning(self, task):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        base.localAvatar.setSystemMessage(0, OTPLocalizer.PeriodTimerWarning)
        return Task.done

    def __periodTimerExpired(self, task):
        assert self.notify.debugStateCall(self, 'loginFSM', 'gameFSM')
        self.notify.info("User's period timer has just expired!")
        self.stopPeriodTimer()
        self.periodTimerExpired = 1
        self.periodTimerStarted = None
        self.periodTimerSecondsRemaining = None
        messenger.send("periodTimerExpired")
        return Task.done


    def handleMessageType(self, msgType, di):
        if msgType == CLIENT_GO_GET_LOST:
            self.handleGoGetLost(di)
        elif msgType == CLIENT_HEARTBEAT:
            self.handleServerHeartbeat(di)
        elif msgType == CLIENT_SYSTEM_MESSAGE:
            self.handleSystemMessage(di)
        elif msgType == CLIENT_SYSTEMMESSAGE_AKNOWLEDGE:
            self.handleSystemMessageAknowledge(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
            self.handleGenerateWithRequiredOther(di)
        elif msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER_OWNER:
            self.handleGenerateWithRequiredOtherOwner(di)
        elif msgType == CLIENT_OBJECT_UPDATE_FIELD:
            self.handleUpdateField(di)
        elif msgType == CLIENT_OBJECT_DISABLE:
            self.handleDisable(di)
        elif msgType == CLIENT_OBJECT_DISABLE_OWNER:
            self.handleDisable(di, ownerView=True)
        elif msgType == CLIENT_OBJECT_DELETE_RESP:
            self.handleDelete(di)
        elif msgType == CLIENT_DONE_INTEREST_RESP:
            self.gotInterestDoneMessage(di)
        elif msgType == CLIENT_GET_STATE_RESP:
            # TODO: is this message obsolete?
            pass
        elif msgType == CLIENT_OBJECT_LOCATION:
            self.gotObjectLocationMessage(di)
        elif msgType == CLIENT_SET_WISHNAME_RESP:
            self.gotWishnameResponse(di)
        else:
            currentLoginState = self.loginFSM.getCurrentState()
            if currentLoginState:
                currentLoginStateName = currentLoginState.getName()
            else:
                currentLoginStateName = "None"
            currentGameState = self.gameFSM.getCurrentState()
            if currentGameState:
                currentGameStateName = currentGameState.getName()
            else:
                currentGameStateName = "None"
            ClientRepositoryBase.notify.warning(
                "Ignoring unexpected message type: " +
                str(msgType) +
                " login state: " +
                currentLoginStateName +
                " game state: " +
                currentGameStateName)

    def gotInterestDoneMessage(self, di):
        # We just received this message from the server; decide if we
        # should handle it immediately.
        if self.deferredGenerates:
            # No, we'd better wait, since some generates have been
            # deferred.  Instead, we'll queue up the message and
            # handle it in sequence.

            # Make a copy of the dg and di.
            dg = Datagram(di.getDatagram())
            di = DatagramIterator(dg, di.getCurrentIndex())

            self.deferredGenerates.append((CLIENT_DONE_INTEREST_RESP, (dg, di)))

        else:
            # We can handle it immediately.
            self.handleInterestDoneMessage(di)

    def gotObjectLocationMessage(self, di):
        # See gotInterestDoneMessage(), above.
        if self.deferredGenerates:
            dg = Datagram(di.getDatagram())
            di = DatagramIterator(dg, di.getCurrentIndex())
            di2 = DatagramIterator(dg, di.getCurrentIndex())
            doId = di2.getUint32()
            if doId in self.deferredDoIds:
                self.deferredDoIds[doId][3].append((CLIENT_OBJECT_LOCATION, (dg, di)))
            else:
                # if we don't have a deferred generate stored for this object, process it
                # immediately
                self.handleObjectLocation(di)
        else:
            self.handleObjectLocation(di)

    def sendWishName(self, avId, name):
        # see setWishNameAnonymous
        datagram = PyDatagram()
        # Add a message type
        datagram.addUint16(CLIENT_SET_WISHNAME)
        # Put in the new doID
        datagram.addUint32(avId)
        # Put in desired name
        datagram.addString(name)
        # Have TCR Send the message because it has a server open
        self.send(datagram)

    def sendWishNameAnonymous(self, name):
        # use this to test a type-a-name submission without needing an avatar to test it on
        self.sendWishName(0, name)
    
    def getWishNameResultMsg(self):
        # handler must accept args [WishNameResult, avId, name]
        return 'OTPCR.wishNameResult'
        
    def gotWishnameResponse(self, di):
        avId = di.getUint32()
        returnCode = di.getUint16()
        pendingName = ''
        approvedName = ''
        rejectedName = ''
        if returnCode == 0:
            pendingName = di.getString()
            approvedName = di.getString()
            rejectedName = di.getString()

        if approvedName:
            name = approvedName
        elif pendingName:
            name = pendingName
        elif rejectedName:
            name = rejectedName
        else:
            name = ''

        WNR = self.WishNameResult
        if returnCode:
            result = WNR.Failure
        elif rejectedName:
            result = WNR.Rejected
        elif pendingName:
            result = WNR.PendingApproval
        elif approvedName:
            result = WNR.Approved

        messenger.send(self.getWishNameResultMsg(), [result, avId, name])

    def replayDeferredGenerate(self, msgType, extra):
        """ Override this to do something appropriate with deferred
        "generate" messages when they are replayed(). """

        if msgType == CLIENT_DONE_INTEREST_RESP:
            dg, di = extra
            self.handleInterestDoneMessage(di)
        elif msgType == CLIENT_OBJECT_LOCATION:
            dg, di = extra
            self.handleObjectLocation(di)
        else:
            ClientRepositoryBase.replayDeferredGenerate(self, msgType, extra)
            

    @exceptionLogged(append=False)
    def handleDatagram(self, di):
        if self.notify.getDebug():
            print "ClientRepository received datagram:"
            di.getDatagram().dumpHex(ostream)


        msgType = self.getMsgType()
        if msgType == 65535:
            self.lostConnection()
            return

        if self.handler == None:
            self.handleMessageType(msgType, di)
        else:
            self.handler(msgType, di)

        # If we're processing a lot of datagrams within one frame, we
        # may forget to send heartbeats.  Keep them coming!
        self.considerHeartbeat()
        
    def askAvatarKnown(self, avId):
        #place holder, make code game specific
        return 0

    def hashFiles(self, pyc):
        # Looks for extraneous .pyo, .pyc, or .py files on the Python
        # path.  We used to be vulnerable to these, but now they're
        # harmless.  Report 'em anyway.

        for dir in sys.path:
            if dir == '':
                dir = '.'
            if os.path.isdir(dir):
                for filename in os.listdir(dir):
                    if filename.endswith('.pyo') or \
                       filename.endswith('.pyc') or \
                       filename.endswith('.py') or \
                       filename == 'library.zip':
                        pathname = Filename.fromOsSpecific(os.path.join(dir, filename))
                        hv = HashVal()
                        hv.hashFile(pathname)
                        pyc.mergeWith(hv)

    def queueRequestAvatarInfo(self, avId):
        pass
        
    def identifyFriend(self, doId):\
        assert False, 'Must override this in inheriting class'
            
    def identifyPlayer(self, playerId):
        assert False, 'Must override this in inheriting class'
            
    def identifyAvatar(self, doId):
        """
        Returns either an avatar, FriendInfo,
        whichever we can find, to reference the indicated avatar doId.
        """
        info = self.doId2do.get(doId)
        if info:
            return info
        else:
            info = self.identifyFriend(doId)         
        return info


    def sendDisconnect(self):
        if self.isConnected():
            # Tell the game server that we're going:
            datagram = PyDatagram()
            # Add message type
            datagram.addUint16(CLIENT_DISCONNECT)
            # Send the message
            self.send(datagram)
            self.notify.info("Sent disconnect message to server")
            self.disconnect()
        self.stopHeartbeat()

    # override per-game
    def _isPlayerDclass(self, dclass):
        return False
    
    # check if this is a player avatar in a location where they should not be
    def _isValidPlayerLocation(self, parentId, zoneId):
        return True

    # since the client is able to set the location of their avatar at will, we need
    # to make sure we don't try to generate a player at the wrong time
    # in particular this is a response to a hack where a player put their avatar in the
    # zone that is set aside for DistributedDistricts; the avatar generate crashed when
    # referencing localAvatar (since localAvatar hadn't been set up yet)
    def _isInvalidPlayerAvatarGenerate(self, doId, dclass, parentId, zoneId):
        if self._isPlayerDclass(dclass):
            if not self._isValidPlayerLocation(parentId, zoneId):
                base.cr.centralLogger.writeClientEvent(
                    'got generate for player avatar %s in invalid location (%s, %s)' % (
                    doId, parentId, zoneId,
                    ))
                return True
        return False

    def handleGenerateWithRequired(self, di):
        parentId = di.getUint32()
        zoneId = di.getUint32()
        assert parentId == self.GameGlobalsId or parentId in self.doId2do
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]

        if self._isInvalidPlayerAvatarGenerate(doId, dclass, parentId, zoneId):
            return

        dclass.startGenerate()
        # Create a new distributed object, and put it in the dictionary
        distObj = self.generateWithRequiredFields(dclass, doId, di, parentId, zoneId)
        dclass.stopGenerate()

    def handleGenerateWithRequiredOther(self, di):
        parentId = di.getUint32()
        zoneId = di.getUint32()
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        
        dclass = self.dclassesByNumber[classId]

        if self._isInvalidPlayerAvatarGenerate(doId, dclass, parentId, zoneId):
            return

        deferrable = getattr(dclass.getClassDef(), 'deferrable', False)
        if not self.deferInterval or self.noDefer:
            deferrable = False
        
        now = globalClock.getFrameTime()
        if self.deferredGenerates or deferrable:
            # This object is deferrable, or there are already deferred
            # objects in the queue (so all objects have to be held
            # up).
            if self.deferredGenerates or now - self.lastGenerate < self.deferInterval:
                # Queue it for later.
                assert(self.notify.debug("deferring generate for %s %s" % (dclass.getName(), doId)))
                self.deferredGenerates.append((CLIENT_CREATE_OBJECT_REQUIRED_OTHER, doId))
                
                # Keep a copy of the datagram, and move the di to the copy
                dg = Datagram(di.getDatagram())
                di = DatagramIterator(dg, di.getCurrentIndex())
            
                self.deferredDoIds[doId] = ((parentId, zoneId, classId, doId, di), deferrable, dg, [])
                if len(self.deferredGenerates) == 1:
                    # We just deferred the first object on the queue;
                    # start the task to generate it.
                    taskMgr.remove('deferredGenerate')
                    taskMgr.doMethodLater(self.deferInterval, self.doDeferredGenerate, 'deferredGenerate')
                    
            else:
                # We haven't generated any deferrable objects in a
                # while, so it's safe to go ahead and generate this
                # one immediately.
                self.lastGenerate = now
                self.doGenerate(parentId, zoneId, classId, doId, di)
                
        else:
            self.doGenerate(parentId, zoneId, classId, doId, di)

    def handleGenerateWithRequiredOtherOwner(self, di):
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # parentId and zoneId are not relevant here
        parentId = di.getUint32()
        zoneId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]
        dclass.startGenerate()
        # Create a new distributed object, and put it in the dictionary
        distObj = self.generateWithRequiredOtherFieldsOwner(dclass, doId, di)
        dclass.stopGenerate()

    def handleQuietZoneGenerateWithRequired(self, di):
        # Special handler for quiet zone generates -- we need to filter
        parentId = di.getUint32()
        zoneId = di.getUint32()
        assert parentId in self.doId2do
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]
        dclass.startGenerate()
        distObj = self.generateWithRequiredFields(dclass, doId, di, parentId, zoneId)
        dclass.stopGenerate()

    def handleQuietZoneGenerateWithRequiredOther(self, di):
        # Special handler for quiet zone generates -- we need to filter
        parentId = di.getUint32()
        zoneId = di.getUint32()
        assert parentId in self.doId2do
        # Get the class Id
        classId = di.getUint16()
        # Get the DO Id
        doId = di.getUint32()
        # Look up the dclass
        dclass = self.dclassesByNumber[classId]
        dclass.startGenerate()
        distObj = self.generateWithRequiredOtherFields(dclass, doId, di, parentId, zoneId)
        dclass.stopGenerate()

    def handleDisable(self, di, ownerView=False):
        # Get the DO Id
        doId = di.getUint32()
        if not self.isLocalId(doId):
            # disable it.  But we never disable our own objects.
            self.disableDoId(doId, ownerView)

    def sendSetLocation(self, doId, parentId, zoneId):
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_OBJECT_LOCATION)
        datagram.addUint32(doId)
        datagram.addUint32(parentId)
        datagram.addUint32(zoneId)
        self.send(datagram)

    def sendHeartbeat(self):
        datagram = PyDatagram()
        # Add message type
        datagram.addUint16(CLIENT_HEARTBEAT)
        # Send it!
        self.send(datagram)
        self.lastHeartbeat = globalClock.getRealTime()
        # This is important enough to consider flushing immediately
        # (particularly if we haven't run readerPollTask recently).
        self.considerFlush()

    def isLocalId(self, id):
        # compare against localAvatar
        try:
            return localAvatar.doId == id
        except:
            self.notify.debug("In isLocalId(), localAvatar not created yet")
            return False
