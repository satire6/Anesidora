# CONNECT ip-address:port HTTP/1.0\012\012

"""
# registry keys for testing
# replace __ with your ttown2 series number
DOWNLOAD_SERVER = http://ttown2.online.disney.com:__20/;http://a.download.toontown.com;http://download.toontown.com
TOONTOWN_PLAYTOKEN = U2FsdGVkX19CmXFvDf2cHjWhlNWRQ+4tdOrtgtuEmb+AGc3zmm+k4NKrsOKPi25g/85VSw9lqd34uReqkJzVgV5bTscgtnMTn8pYFsWhYHxW0F8CHOkblDMHd48Cj4+rDTMDdprNPz1Ad2Ah+tf1phWEK3YnfROukDZtFokrI5zvpJxwu5Jn4Z7D1CutIeVCnyub0hZ9QfUUXtvwuTR/+kQ2NvOFqXHf1Oo0pMGNqiuBiiW30+v+uFM2Na3gLZcsHf+Coa/f8r3ui8izkX8XKusgfX5d4l5L

cd $TOONTOWN/src/publish
./publish -c -s __00

# if your webpage isn't working, install by doing:
/c/ttown-persist/english> chmod +x InstallLauncher.exe
/c/ttown-persist/english> ./InstallLauncher.exe

# then at the command prompt in the installation dir:
Toontown.exe -OO http://localhost http://localhost 0 ""
"""

"""
The Launcher

API to game:

Functions:
----------------------------------------------------------------------
# Ask if a phase is complete (downloaded, extracted, patched, and all)
getPhaseComplete(phase)

# Ask what percent a phase is through its download process.
# returns [0-100]
getPercentPhaseComplete(phase)

# Set that the ingame 3d tutorial has been previously completed
setTutorialComplete()
# Ask if the ingame 3d tutorial has been previously completed
getTutorialComplete()

# Get the top dir of the game
getInstallDir()
# Ask for the blue
getBlue()
# Set that the panda window is open now
setPandaWindowOpen()
# Set that the panda error (or exit) code. 0 means ok
setPandaErrorCode(int)

# Ask if this is a new installation
getIsNewInstallation()
# Set that this is no longer a new installation
# (has created account or logged in)
setIsNotNewInstallation()

# Get the last login
getLastLogin()
# Set a new 'last login'
setLastLogin()

# Set that a user (paid or unpaid) has logged in
setUserLoggedIn()
# Set that a paid user has logged in
setPaidUserLoggedIn()

# Get the referrer code
getReferrerCode()

# Set a new or existing registry value under the game key
setRegistry(name, value)
# Get an existing registry value under the game key
# An error will be raised if the name does not exist
getRegistry(name)

Events:
----------------------------------------------------------------------
Launcher sends the event "phaseComplete-n" when phase n is finished downloading

"""

##################################################
#                                                #
# Toontown Python Game Launcher                  #
#                                                #
##################################################

import os
import sys
import time
import types

#
# Original bootstrap logger that gets LOGGING IMMEDIATELY UP before any
# Panda/Toontown dependencies are imported
#
if 1:   # flip this as necessary
    # Setup the log files
    # We want C++ and Python to both go to the same log so they
    # will be interlaced properly.

    # match log format specified in installerBase.cxx,
    # want this fmt so log files can be sorted oldest first based on name,
    # and so old open handles to logs dont prevent game from starting
    ltime = time.localtime()
    if __debug__:
        logSuffix = 'dev'
    else:
        logSuffix = "%02d%02d%02d_%02d%02d%02d" % (ltime[0]-2000,ltime[1],ltime[2],ltime[3],ltime[4],ltime[5])
    logfile = 'toontownD-' + logSuffix + '.log'

    # Redirect Python output and err to the same file
    class LogAndOutput:
        def __init__(self, orig, log):
            self.orig = orig
            self.log = log
        def write(self, str):
            self.log.write(str)
            self.log.flush()
            self.orig.write(str)
            self.orig.flush()
        def flush(self):
            self.log.flush()
            self.orig.flush()

    # old game log deletion now managed by activeX control
    ## Delete old log files so they do not clog up the disk
    ##if os.path.exists(logfile):
    ##    os.remove(logfile)

    # Open the new one for appending
    # Make sure you use 'a' mode (appending) because both Python and
    # Panda open this same filename to write to. Append mode has the nice
    # property of seeking to the end of the output stream before actually
    # writing to the file. 'w' mode does not do this, so you will see Panda
    # output and Python output not interlaced properly.
    log = open(logfile, 'a')
    logOut = LogAndOutput(sys.__stdout__, log)
    logErr = LogAndOutput(sys.__stderr__, log)
    sys.stdout = logOut
    sys.stderr = logErr

    # Write to the log
    print "\n\nStarting Toontown..."
    print ("Current time: " + time.asctime(time.localtime(time.time()))
           + " " + time.tzname[0])
    print "sys.path = ", sys.path
    print "sys.argv = ", sys.argv

from otp.launcher.LauncherBase import LauncherBase
from otp.otpbase import OTPLauncherGlobals
# LauncherBase sets up import path stuff, import Panda after
from pandac.libpandaexpressModules import *
from toontown.toonbase import TTLocalizer

class ToontownLauncher(LauncherBase):
    GameName = 'Toontown'
    LauncherPhases = [3,3.5,4,5,5.5,6,7,8,9,10,11,12,13]
    TmpOverallMap = [0.25,0.15,0.12,0.17,0.08,0.07,0.05,0.05,0.017,0.011,0.010,0.012,0.010]
    RegistryKey = 'Software\\Disney\\Disney Online\\Toontown'
    ForegroundSleepTime = 0.01
    Localizer = TTLocalizer
    # TODO: take this out when Pirates ships.
    VerifyFiles = 1
    DecompressMultifiles = True
    
    def __init__(self):
        # Get the command line parameters
        # argv[0] : the name of this script
        # argv[1] : python params
        # argv[2] : game server (semicolon-delimited list of url's)
        # argv[3] : account server (single url)
        # argv[4] : test server flag (0 or 1)
        # argv[5] : args to Configrc.exe
        # It is an error not to pass in the right number of command line parameters

        # For backwards compatibility with the launcher, we allow this
        # old script name to be on the command line, and we ignore it
        # if it is there.
        if sys.argv[2] == 'Phase2.py':
            sys.argv = sys.argv[:1] + sys.argv[3:]
        
        if ((len(sys.argv) == 5) or (len(sys.argv) == 6)):
            self.gameServer = sys.argv[2]
            # The account server, from the command line.
            # We don't bother to override these from Configrc, since the
            # TCR and TTLogin classes will do this already.
            self.accountServer = sys.argv[3]
            self.testServerFlag = int(sys.argv[4])
        else:
            # This error message is a little too helpful for potential hackers
            print "Error: Launcher: incorrect number of parameters"
            sys.exit()

        # Used to pass to server for authentication
        self.toontownBlueKey = "TOONTOWN_BLUE"
        # Used to pass to server for authentication
        self.toontownPlayTokenKey = "TOONTOWN_PLAYTOKEN"
        # Used to communicate status back to the Updating Toontown flash movie
        self.launcherMessageKey = "LAUNCHER_MESSAGE"
        # Is the flash game1 done? (int 1 or 0)
        self.game1DoneKey = "GAME1_DONE"
        # Is the flash game2 done? (int 1 or 0)
        self.game2DoneKey = "GAME2_DONE"
        # Is the in-game 3d tutorial done? (int 1 or 0)
        self.tutorialCompleteKey = "TUTORIAL_DONE"

        # Flag for whether the player needs parent password for Secrets:
        #self.needPwForSecretKey = "NEED_PW_FOR_SECRET"
        # Parent Password Key
        #self.chatEligibleKey = "CHATTERBOX"

        # Both these values now come from webAccountParams (not the registry)
        self.toontownRegistryKey = 'Software\\Disney\\Disney Online\\Toontown'
        # This is where all the registry keys are located
        if self.testServerFlag:
            self.toontownRegistryKey = "%s%s" % (self.toontownRegistryKey, 'Test')
        # append any necessary productName to differentiate from US installation
        self.toontownRegistryKey = "%s%s" % (self.toontownRegistryKey, self.getProductName())

        LauncherBase.__init__(self)

        # Before you go further, let's parse the web acct parameters
        self.webAcctParams = "WEB_ACCT_PARAMS"
        self.parseWebAcctParams()
        
        self.mainLoop()

    def getValue(self, key, default=None):
        try:
            return self.getRegistry(key, default)
        except:
            return self.getRegistry(key)

    def setValue(self, key, value):
        self.setRegistry(key, value)

    def getVerifyFiles(self):
        return 1

    def getTestServerFlag(self):
        return self.testServerFlag

    def getGameServer(self):
        return self.gameServer

    def getLogFileName(self):
        return 'toontown'

    def parseWebAcctParams(self):
        """
        Parse the Web Account Params for chat related name-value pairs and store those
        in the launcher class. For security, this registry value is deleted after the
        first iteration. The client can then inquire PlayToken, ChatEligible etc.
        """
        # Allow a developer to stuff it in the config file if
        # necessary.
        s = config.GetString("fake-web-acct-params", '')

        if not s:
            s = self.getRegistry(self.webAcctParams)
            
        # Immediately clear out the Params so it will be more
        # difficult for a hacker to pull it out of the registry.
        self.setRegistry(self.webAcctParams, "")
       
        # Parse the web account params to get chat related values
        # split s to the '&'
        l = s.split('&')
        length = len(l)

        # build a dictionary of the parameters
        dict = {}
        for index in range(0, len(l)):
            args = l[index].split('=')
            if len(args) == 3:
                # extra '=' on first entry: "webAccountParams=foo=1&..."
                name, value = args[-2:]
                dict[name] = int(value)
            elif len(args) == 2:
                name, value = args
                dict[name] = int(value)

        self.secretNeedsParentPasswordKey = 1                
        if dict.has_key('secretsNeedsParentPassword'):
            self.secretNeedsParentPasswordKey = 1 and dict['secretsNeedsParentPassword']
        else:
            self.notify.warning('no secretNeedsParentPassword token in webAcctParams')
        self.notify.info('secretNeedsParentPassword = %d' % self.secretNeedsParentPasswordKey)

        self.chatEligibleKey = 0
        if dict.has_key('chatEligible'):
            self.chatEligibleKey = 1 and dict['chatEligible']
        else:
            self.notify.warning('no chatEligible token in webAcctParams')
        self.notify.info('chatEligibleKey = %d' % self.chatEligibleKey)

    #============================================================
    # Interface of launcher to the rest of the game
    #============================================================

    def getBlue(self):
        """
        Get the blue out of the registry and return it.  The blue is
        not saved; if this method is called a second time it will
        return None.
        """
        blue = self.getValue(self.toontownBlueKey)
        # Immediately clear out the blue so it will be more
        # difficult for a hacker to pull it out of the registry.
        self.setValue(self.toontownBlueKey, "")

        if blue == "NO BLUE":
            blue = None
        return blue

    def getPlayToken(self):
        """
        Get the PlayToken out of the registry and return it.  The
        PlayToken is not saved; if this method is called a second
        time it will return None.
        """
        playToken = self.getValue(self.toontownPlayTokenKey)
        # Immediately clear out the PlayToken so it will be more
        # difficult for a hacker to pull it out of the registry.
        self.setValue(self.toontownPlayTokenKey, "")

        if playToken == "NO PLAYTOKEN":
            playToken = None
        return playToken

    #============================================================
    #   Registry functions
    #============================================================

    def setRegistry(self, name, value):
        # Set this name to this value under the master game registry key

        if not self.WIN32:
            # Outside of Windows, we don't even try to store this stuff.
            return

        # You can only set strings and integers in here
        t = type(value)
        if (t == types.IntType):
            WindowsRegistry.setIntValue(self.toontownRegistryKey, name, value)

        elif (t == types.StringType):
            WindowsRegistry.setStringValue(self.toontownRegistryKey, name,
                                           value)
        else:
            self.notify.warning("setRegistry: Invalid type for registry value: "
                                + `value`)

    def getRegistry(self, name, missingValue = None):
        # Return the value of this key.

        self.notify.info("getRegistry%s" % ((name, missingValue),))
        if not self.WIN32:
            # Outside of windows, we query the environment.
            if (missingValue == None):
                missingValue = ""
            value = os.environ.get(name, missingValue)
            try:
                value = int(value)
            except:
                pass
            return value

        t = WindowsRegistry.getKeyType(self.toontownRegistryKey, name)
        if (t == WindowsRegistry.TInt):
            if (missingValue == None):
                missingValue = 0
            return WindowsRegistry.getIntValue(self.toontownRegistryKey, name,
                                               missingValue)
        elif (t == WindowsRegistry.TString):
            if (missingValue == None):
                missingValue = ""
            return WindowsRegistry.getStringValue(self.toontownRegistryKey, name,
                                                  missingValue)
        else:
            return missingValue

    #============================================================
    # Download functions
    #============================================================

    def getCDDownloadPath(self, origPath, serverFilePath):
        return '%s/%s%s/CD_%d/%s' % (
            origPath, self.ServerVersion, self.ServerVersionSuffix, self.fromCD, serverFilePath)
    def getDownloadPath(self, origPath, serverFilePath):
        return '%s/%s%s/%s' % (
            origPath, self.ServerVersion, self.ServerVersionSuffix, serverFilePath)

    def getPercentPatchComplete(self, bytesWritten):
        if self.totalPatchDownload:
            return LauncherBase.getPercentPatchComplete(self, bytesWritten)
        else:
            return 0

    def hashIsValid(self, serverHash, hashStr):
        return (serverHash.setFromDec(hashStr) or
                serverHash.setFromHex(hashStr))

    def launcherMessage(self, msg):
        LauncherBase.launcherMessage(self, msg)
        self.setRegistry(self.launcherMessageKey, msg)

    def getAccountServer(self):
        return self.accountServer

    def setTutorialComplete(self):
        self.setRegistry(self.tutorialCompleteKey, 0)

    def getTutorialComplete(self):
        return self.getRegistry(self.tutorialCompleteKey, 0)

    def getGame2Done(self):
        return self.getRegistry(self.game2DoneKey, 0)

    def setPandaErrorCode(self, code):
        """
        Set the exit code of panda. 0 means everything ok
        """
        self.pandaErrorCode = code
        if self.WIN32:
            self.notify.info("setting panda error code to %s" % (code))
            exitCode2exitPage = {
                OTPLauncherGlobals.ExitEnableChat: "chat",
                OTPLauncherGlobals.ExitSetParentPassword: "setparentpassword",
                OTPLauncherGlobals.ExitPurchase: "purchase",
                }
            if code in exitCode2exitPage:
                self.setRegistry("EXIT_PAGE", exitCode2exitPage[code])
                self.setRegistry(self.PandaErrorCodeKey, 0)
            else:
                # Under Windows, this (currently) goes to the registry.
                self.setRegistry(self.PandaErrorCodeKey, code)

        else:
            # On OSX, we dump the error code to a file on disk.
            LauncherBase.setPandaErrorCode(self, code)

    def getNeedPwForSecretKey(self):
##         """
##         Get the PlayToken out of the registry and return it.  The
##         PlayToken is not saved; if this method is called a second
##         time it will return None.
##         """
##         nameValue = self.getRegistry(self.webAcctParams)
##         needPwForSecretKey = self.getRegistry(self.needPwForSecretKey)
##         # Immediately clear out the PlayToken so it will be more
##         # difficult for a hacker to pull it out of the registry.
##         self.setRegistry(self.needPwForSecretKey, "")
##         return 1 and needPwForSecretKey

        """
        Everything is already parsed if parseWebAcctParams was called 
        """
        return self.secretNeedsParentPasswordKey

    def getParentPasswordSet(self):
        """
        Get the parent password set key
        """
##         return self.getRegistry(self.chatEligibleKey, 0)
        # Everything is already parsed if parseWebAcctParams was called 
        return self.chatEligibleKey

    def MakeNTFSFilesGlobalWriteable(self, pathToSet = None ):
        if not self.WIN32:
            return
        LauncherBase.MakeNTFSFilesGlobalWriteable(self, pathToSet)

    #============================================================
    #  Launcher startup
    #============================================================

    def startGame(self):
        # We'll need to import Phase3.pyo.  Make sure there's not a
        # competing Phase3.py file in the way first.
        try:
            os.remove('Phase3.py')
        except:
            pass
        
        # Read in the Phase3.pyz file
        import Phase3

        self.newTaskManager()

        from direct.showbase.EventManagerGlobal import eventMgr
        eventMgr.restart()
        from toontown.toonbase import ToontownStart
