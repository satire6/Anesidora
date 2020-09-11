import direct
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.p3d.PackageInstaller import PackageInstaller
from direct.task.TaskManagerGlobal import taskMgr
import sys
import time
import os
import subprocess
import __builtin__

class WebLauncherBase(DirectObject):

    """ This class serves as a "launcher" for the games when launched
    as a plugin on a web page, or via the Panda3D runtime in general
    (e.g. via panda3d.exe).  It attempts to replicate the API
    presented by the old LauncherBase class, to the extent possible.
    In the new world of the Panda3D runtime, it is no longer necessary
    to explicitly manage downloading and patching; the runtime system
    in AppRunner will do this now. """    

    
    notify = directNotify.newCategory("WebLauncherBase")

    # Used to tell browser panda exit status (0 means everything normal)
    PandaErrorCodeKey = "PANDA_ERROR_CODE"
    # Used to keep track of whether or not this is a new installation
    NewInstallationKey = "IS_NEW_INSTALLATION"
    # Used to keep track of the last login name that was entered
    LastLoginKey = "LAST_LOGIN"
    # Used to keep track of the fact that a user has logged in
    UserLoggedInKey = "USER_LOGGED_IN"
    # Used to keep track of the fact that a paid user has logged in
    PaidUserLoggedInKey = "PAID_USER_LOGGED_IN"
    # Referrer code
    ReferrerKey = "REFERRER_CODE"
    # Period timer seconds remaining
    PeriodTimeRemainingKey = "PERIOD_TIME_REMAINING"
    # Period name
    PeriodNameKey = "PERIOD_NAME"
    # Period name
    SwidKey = "SWID"
    # The DISL Token
    DISLTokenKey = "DISLTOKEN"

    # Stores the proxy server (string) (possibly with a :port)
    # Empty string if there is no proxy
    ProxyServerKey = "PROXY_SERVER"
    ProxyDirectHostsKey = "PROXY_DIRECT_HOSTS"

    # This is always empty in the web launcher case (in the classic
    # launcher, it might be different for different environments).
    logPrefix = ''

    class PhaseData:
        def __init__(self, phase):
            self.phase = phase
            self.percent = 0
            self.complete = False
            self.postProcessCallbacks = []

        def markComplete(self):
            """ Called when the phase has been fully downloaded.  This
            function should invoke any postProcessCallbacks recorded, on
            the appropriate task chain(s), and then mark the phase
            complete and send the phaseComplete event. """
            
            self.__nextCallback(None, 'default')

        def __nextCallback(self, currentCallback, currentTaskChain):
            # Perform the callback's function.
            if currentCallback:
                currentCallback()

            # Grab the next callback off the list, and execute it.
            if self.postProcessCallbacks:
                callback, taskChain = self.postProcessCallbacks[0]
                del self.postProcessCallbacks[0]
                if taskChain != currentTaskChain:
                    # Switch to the next task chain.
                    print "switching to %s" % (taskChain)
                    taskMgr.add(self.__nextCallback, 'phaseCallback-%s' % (self.phase),
                                taskChain = taskChain, extraArgs = [callback, taskChain])
                    return

            # No more callbacks.  Send the phaseComplete event.
            self.complete = True
            messenger.send('phaseComplete-%s' % (self.phase), taskChain = 'default')


    def __init__(self, appRunner):
        self.appRunner = appRunner
        __builtin__.launcher = self

        appRunner.exceptionHandler = self.exceptionHandler

        # Get the game info from the web page.
        gameInfoStr = appRunner.getToken('gameInfo')
        if gameInfoStr:
            self.gameInfo = appRunner.evalScript(gameInfoStr, needsResponse = True)
        else:
            # No game info available; create a dummy object instead.
            class DummyGameInfo:
                pass
            self.gameInfo = DummyGameInfo()

        self.phasesByPackageName = {}
        self.phaseData = {}
        self.allPhasesComplete = False
        for phase, packageName in self.LauncherPhases:
            self.phasesByPackageName[packageName] = phase
            self.phaseData[phase] = self.PhaseData(phase)
            self.acceptOnce('phaseComplete-%s' % (phase), self.__gotPhaseComplete)

        self.packageInstaller = None
        self.started = False

        self.setPandaErrorCode(0)
        self.setServerVersion("dev")

        self.WIN32 = (os.name == 'nt')

        if self.WIN32:
            # Vista = windows 2.6
            self.VISTA = (sys.getwindowsversion()[3] == 2 and sys.getwindowsversion()[0] == 6)
        else:
            # it can't be Vista
            self.VISTA = 0

        # Fake download hash values
        self.launcherFileDbHash = HashVal()
        self.serverDbFileHash = HashVal()

        # Is this the test server?
        self.testServerFlag = self.getTestServerFlag()
        self.notify.info("isTestServer: %s" % (self.testServerFlag))
            
        # Write to the log
        print "\n\nStarting %s..." % self.GameName
        print ("Current time: " + time.asctime(time.localtime(time.time()))
               + " " + time.tzname[0])
        print "sys.argv = ", sys.argv
        print "tokens = ", appRunner.tokens
        print "gameInfo = ", self.gameInfo

        # Run an external command to get the system hardware
        # information into a log file.  First, we have to change the
        # current directory (dxdiag, in particular, insists on this).
        cwd = os.getcwd()
        os.chdir(appRunner.logDirectory.toOsSpecific())
        self.notify.info('chdir: %s' % (appRunner.logDirectory.toOsSpecific()))

        hwprofile = 'hwprofile.log'
        command = None
        if sys.platform == "darwin":
            command = '/usr/sbin/system_profiler >%s' % (hwprofile)
            shell = True
        elif sys.platform == "linux":
            command = '(cat /proc/cpuinfo; cat /proc/meminfo; /sbin/ifconfig -a) >%s' % (hwprofile)
            shell = True
        else:
            command = 'dxdiag /t %s' % (hwprofile)
            shell = False

        self.notify.info(command)
        try:
            self.hwpipe = subprocess.Popen(command, shell=shell)
        except OSError:
            self.notify.warning('Could not run hwpipe command')
            self.hwpipe = None

        # Now we can change the directory back.
        os.chdir(cwd)

        if self.hwpipe:
            self.notify.info('hwpipe pid: %s' % (self.hwpipe.pid))
            taskMgr.add(self.__checkHwpipe, 'checkHwpipe')

    def __gotPhaseComplete(self):
        """ A hook added to a phaseComplete message.  When all
        phaseCompletes have been sent, trigger the allPhasesComplete
        message. """

        if self.allPhasesComplete:
            # Already sent.
            return

        for phaseData in self.phaseData.values():
            if not phaseData.complete:
                # More to come later.
                return

        # All phases are now complete.  Tell the world.
        self.allPhasesComplete = True
        print "launcherAllPhasesComplete"
        messenger.send("launcherAllPhasesComplete", taskChain = 'default')
            

    def __checkHwpipe(self, task):
        """ Checks to see if the hwpipe process has finished, so we
        can report it to the log. """
        if self.hwpipe.poll() is None:
            # Still waiting.
            return task.cont

        #hwpipeout = self.hwpipe.communicate()
        #self.notify.info('hwpipe output: %s' % (hwpipeout[0]))
        #self.notify.info('hwpipe error: %s' % (hwpipeout[1]))
        self.notify.info('hwpipe finished: %s' % (self.hwpipe.returncode))
        return task.done

    def isDummy(self):
        # This is not the DummyLauncher.
        return False

    def setRegistry(self, key, value):
        self.notify.info('DEPRECATED setRegistry: %s = %s' % (key, value))
        return

    def getRegistry(self, key):
        self.notify.info('DEPRECATED getRegistry: %s' % (key))
        return None

    def getValue(self, key, default=None):
        return getattr(self.gameInfo, key, default)

    def setValue(self, key, value):
        setattr(self.gameInfo, key, value)

    def getVerifyFiles(self):
        # TODO: take this out when we ship.
        return config.GetInt('launcher-verify', 0)

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return self.getValue('GAME_SERVER', '')
        
    def getPhaseComplete(self, phase):
        return (self.phaseData[phase].complete)
        
    def getPercentPhaseComplete(self, phase):
        return self.phaseData[phase].percent

    def addPhasePostProcess(self, phase, func, taskChain = 'default'):
        """ Adds a post-process callback function to the phase
        download.  When the indicated phase is successfully
        downloaded, the given function will be called, on the
        specified taskChain.  The phase will not be marked fully
        downloaded, and the phaseComplete event will not be sent,
        until the callback function has completed.

        If the phase is already complete at the time this function is
        called, the callback function is called immediately, in the
        current task. """

        if self.getPhaseComplete(phase):
            # Already downloaded.
            func()
            return

        self.phaseData[phase].postProcessCallbacks.append((func, taskChain))

    def getBlue(self):
        # Games that potentially use a blue token should override
        return None

    def getPlayToken(self):
        # Games that potentially use a playtoken should override
        return None

    def getDISLToken(self):
        """
        Get the DISLToken out of the store and return it.  The
        DISLToken is not saved; if this method is called a second
        time it will return None.
        """
        DISLToken = self.getValue(self.DISLTokenKey)
        if DISLToken == "NO DISLTOKEN":
            DISLToken = None
        return DISLToken

    def startDownload(self):
        assert not self.packageInstaller

        self.packageInstaller = WebLauncherInstaller(self)

        for phase, packageName in self.LauncherPhases:
            self.packageInstaller.addPackage(packageName)

        self.packageInstaller.donePackages()
    

    #============================================================
    # Interface of launcher to the rest of the game
    #============================================================

    def isTestServer(self):
        return self.testServerFlag

    def recordPeriodTimeRemaining(self, secondsRemaining):
        self.setValue(self.PeriodTimeRemainingKey, int(secondsRemaining))

    def recordPeriodName(self, periodName):
        self.setValue(self.PeriodNameKey, periodName)

    def recordSwid(self, swid):
        self.setValue(self.SwidKey, swid)

    def getGoUserName(self):
        return self.goUserName

    def setGoUserName(self, userName):
        self.goUserName = userName

    def setPandaWindowOpen(self):
        # This is called when the Panda window is successfully opened.
        # It used to be an important signal in the old ActiveX world.
        # It is now a no-op.
        pass

    def setPandaErrorCode(self, code):
        """
        Set the exit code of panda. 0 means everything ok
        """
        self.pandaErrorCode = code
        self.gameInfo.pandaErrorCode = code

    def getPandaErrorCode(self):
        return self.pandaErrorCode

    def setDisconnectDetailsNormal(self):
        self.disconnectCode = 0
        self.disconnectMsg = 'normal'
        self.gameInfo.disconnectCode = self.disconnectCode
        self.gameInfo.disconnectMsg = self.disconnectMsg
        
    def setDisconnectDetails(self, newCode, newMsg):
        if newCode is None:
            newCode = 0
        self.disconnectCode = newCode
        self.disconnectMsg = newMsg
        self.gameInfo.disconnectCode = self.disconnectCode
        self.gameInfo.disconnectMsg = self.disconnectMsg
        self.notify.warning("disconnected with code: %s - %s" % (self.gameInfo.disconnectCode,self.gameInfo.disconnectMsg))
        
    def setServerVersion(self, version):
        """
        Set the server version. Exposed to gameInfo.
        """
        self.ServerVersion = version
        self.gameInfo.ServerVersion = version
        
    def getServerVersion(self):
        return self.ServerVersion

    def getIsNewInstallation(self):
        """
        is this a new installation?
        """
        result = self.getValue(self.NewInstallationKey, 1)
        result = base.config.GetBool("new-installation", result)
        return result

    def setIsNotNewInstallation(self):
        """
        Set that this is no longer a new installation
        (has created account or logged in)
        """
        self.setValue(self.NewInstallationKey, 0)

    def getLastLogin(self):
        """
        Get the last login
        """
        return self.getValue(self.LastLoginKey, '')

    def setLastLogin(self, login):
        """
        Set a new 'last login'
        """
        self.setValue(self.LastLoginKey, login)

    def setUserLoggedIn(self):
        """
        Set that a user has logged in.
        """
        self.setValue(self.UserLoggedInKey, '1')  # since these are flags they should really be 1, not '1'

    def setPaidUserLoggedIn(self):
        """
        Set that a paid user has logged in
        """
        self.setValue(self.PaidUserLoggedInKey, '1') # since these are flags they should really be 1, not '1'

    def getReferrerCode(self):
        """
        Get the referrer code
        """
        return self.getValue(self.ReferrerKey, None)

    def exceptionHandler(self):
        """ This callback is assigned to the
        appRunner.exceptionHandler pointer, so we get notified on an
        unexpected Python exception. """
        
        # A Python exception is error code 12 for the installer.
        self.setPandaErrorCode(12)
        self.notify.warning("Handling Python exception.")

        if hasattr(__builtin__, "base") and \
           getattr(base, "cr", None):
            # Tell the AI (if we have one) why we're going down.
            if base.cr.timeManager:
                from otp.otpbase import OTPGlobals
                base.cr.timeManager.setDisconnectReason(OTPGlobals.DisconnectPythonError)
                base.cr.timeManager.setExceptionInfo()

            # Tell the server we're gone too.
            base.cr.sendDisconnect()

        if hasattr(__builtin__, "base"):
            # Clean up showbase correctly.
            base.destroy()

        self.notify.info("Exception exit.\n")
        import traceback
        traceback.print_exc()
        sys.exit()

    def isDownloadComplete(self):
        return self.allPhasesComplete


class WebLauncherInstaller(PackageInstaller):
    """ Subclasses PackageInstaller to send the appropriate messages
    as packages are downloaded. """

    def __init__(self, launcher):
        PackageInstaller.__init__(self, launcher.appRunner)
        self.launcher = launcher
        self.lastProgress = None

    def packageProgress(self, package, progress):
        """ This callback is made repeatedly between packageStarted()
        and packageFinished() to update the current progress on the
        indicated package only.  The progress value ranges from 0
        (beginning) to 1 (complete). """

        PackageInstaller.packageProgress(self, package, progress)
        percent = int(progress * 100.0 + 0.5)
        phase = self.launcher.phasesByPackageName[package.packageName]
        self.launcher.phaseData[phase].percent = percent
        if (phase, percent) != self.lastProgress:
            messenger.send('launcherPercentPhaseComplete',
                           [phase, percent, None, None])
            self.lastProgress = (phase, percent)

    def packageFinished(self, package, success):
        """ This callback is made for each package between
        downloadStarted() and downloadFinished() to indicate that a
        package has finished downloading.  If success is true, there
        were no problems and the package is now installed.

        If this package did not require downloading (because it was
        already downloaded), this callback will be made immediately,
        *without* a corresponding call to packageStarted(), and may
        even be made before downloadStarted(). """

        PackageInstaller.packageFinished(self, package, success)
        if not success:
            print "Failed to download %s" % (package.packageName)
            self.launcher.setPandaErrorCode(6)
            sys.exit()
        
        phase = self.launcher.phasesByPackageName[package.packageName]
        self.launcher.phaseData[phase].markComplete()
        
    def downloadFinished(self, success):
        """ This callback is made when all of the packages have been
        downloaded and installed (or there has been some failure).  If
        all packages where successfully installed, success is True.

        If there were no packages that required downloading, this
        callback will be made immediately, *without* a corresponding
        call to downloadStarted(). """

        PackageInstaller.downloadFinished(self, success)
        if not success:
            print "Failed to download all packages."

        # We don't immediately trigger launcherAllPhasesComplete here,
        # because we might still be waiting on one or more
        # postProcessCallbacks.
