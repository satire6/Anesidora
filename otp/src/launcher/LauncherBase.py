
##################################################
#                                                #
# OTP Python Game Launcher Base Class            #
#                                                #
##################################################

import sys
import os
import time
import string
import __builtin__
from pandac.libpandaexpressModules import *
# Import DIRECT files
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.MiniTask import MiniTask, MiniTaskManager
from direct.directnotify.DirectNotifyGlobal import *

# Redirect Python output and err to the same file
class LogAndOutput:
    def __init__(self, orig, log):
        self.orig = orig
        self.log = log
        self.console = False

    def write(self, str):
        self.log.write(str)
        self.log.flush()

        if self.console:
            self.orig.write(str)
            self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()

class LauncherBase(DirectObject):
    # override and redefine
    GameName = 'game'
    ArgCount = 6
    LauncherPhases = [1,2,3,4]
    TmpOverallMap = [.25,.25,.25,.25] # totals to 1.00

    # Various bandwidths (bytes per second).  It is important that the
    # difference between any two adjacent entries not be too large--we
    # should probably never more than double the bandwidth at any
    # step, and stepping less than double is preferable in most cases.
    BANDWIDTH_ARRAY = [1800,    # 14.4 modem
                       3600,    # 28.8 modem
                       4200,    # 33.6 modem
                       6600,    # 56k modem (53.3 actual)
                       8000,    # 64k ISDN
                       12000,
                       16000,   # 128k ISDN
                       24000,
                       32000,
                       48000,   # 384k DSL
                       72000,
                       96000,   # 768k DSL
                       128000,
                       192000,  # 1.5MB DSL/Cable Modem
                       250000,
                       500000,  # LAN
                       750000,
                       1000000,  # 100-base T
                       1250000,
                       1500000,
                       1750000,
                       2000000,
                       3000000,
                       4000000,
                       6000000,
                       8000000,
                       10000000,  # Super fast connection
                       12000000,
                       14000000,
                       16000000,
                       24000000,
                       32000000,
                       48000000,
                       64000000,
                       96000000,
                       128000000,  # Who knows
                       256000000,
                       512000000,
                       1024000000,  # Some day
                      ]

    # These values were extracted from win32con.py
    # This was a very large file to include in our distribution for
    # these few constants, so we'll just pull in the ones we need here
    # import win32con
    win32con_FILE_PERSISTENT_ACLS = 0x00000008

    # Where is the top directory of the game?
    InstallDirKey = "INSTALL_DIR"
    # What is the name of the game log file?
    GameLogFilenameKey = "GAMELOG_FILENAME"
    # Used to tell flash when the window finally opens
    PandaWindowOpenKey = "PANDA_WINDOW_OPEN"
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
    # If patch, then from what CD.
    PatchCDKey = "FROM_CD"
    # The DISL Token
    DISLTokenKey = "DISLTOKEN"

    # Stores the proxy server (string) (possibly with a :port)
    # Empty string if there is no proxy
    ProxyServerKey = "PROXY_SERVER"
    ProxyDirectHostsKey = "PROXY_DIRECT_HOSTS"

    launcherFileDbFilename = 'launcherFileDb'

    webLauncherFlag = False

    def __init__(self):
        self.started = False

        # This line is to ensure that Python is running in opt mode -OO.
        if __debug__:
            print "WARNING: Client should run Python optimized -OO"

        self.taskMgrStarted = False

        # Setup the log files
        # We want C++ and Python to both go to the same log so they
        # will be interlaced properly.

        self._downloadComplete = False
        self.pandaErrorCode = 0

        self.WIN32 = (os.name == 'nt')

        if self.WIN32:
            # Vista = windows 2.6
            self.VISTA = (sys.getwindowsversion()[3] == 2 and sys.getwindowsversion()[0] == 6)
        else:
            # it can't be Vista
            self.VISTA = 0

        # match log format specified in installerBase.cxx,
        # want this fmt so log files can be sorted oldest first based on name,
        # and so old open handles to logs dont prevent game from starting
        ltime = time.localtime()
        logSuffix = "%02d%02d%02d_%02d%02d%02d" % (ltime[0]-2000,ltime[1],ltime[2],ltime[3],ltime[4],ltime[5])
        logPrefix = ''
        if not self.WIN32:
            logPrefix = os.environ.get('LOGFILE_PREFIX', '')
        logfile = logPrefix + self.getLogFileName() + '-' + logSuffix + '.log'
        self.errorfile = 'errorCode'

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

        if sys.platform == "darwin":
            # On OSX, we want to get the system profile into the log.
            os.system('/usr/sbin/system_profiler >>' + logfile)    
        elif sys.platform == "linux2":
            os.system('cat /proc/cpuinfo >>' + logfile) 
            os.system('cat /proc/meminfo >>' + logfile) 
            os.system('/sbin/ifconfig -a >>' + logfile) 

        # Write to the log
        print "\n\nStarting %s..." % self.GameName
        print ("Current time: " + time.asctime(time.localtime(time.time()))
               + " " + time.tzname[0])
        print "sys.path = ", sys.path
        print "sys.argv = ", sys.argv
        print "os.environ = ", os.environ

        if(len(sys.argv)>=self.ArgCount):
            Configrc_args = sys.argv[self.ArgCount-1]
            print("generating configrc using: '" + Configrc_args + "'")
        else:
            Configrc_args = ""
            print("generating standard configrc")

        # This used to be CONFIG_CONFIG, but with the new Config system we
        # don't use the old CONFIG_CONFIG environment variable any more.  We
        # still need to set PRC_EXECUTABLE_ARGS to specify the command-line
        # arguments to pass to Configrc.exe, but the use of Configrc.exe
        # itself is a stopgap until we can replace that system with the newer
        # signed prc file system.
        if os.environ.has_key("PRC_EXECUTABLE_ARGS"):
            print "PRC_EXECUTABLE_ARGS is set to: " + os.environ["PRC_EXECUTABLE_ARGS"]
            print "Resetting PRC_EXECUTABLE_ARGS"

        # Cannot assign to os.environ here; we have to use
        # ExecutionEnvironment to make the low-level prc respect it.
        ExecutionEnvironment.setEnvironmentVariable(
            "PRC_EXECUTABLE_ARGS", '-stdout ' + Configrc_args)

        # Actually, we still have to set CONFIG_CONFIG too, since Configrc.exe
        # itself expects that.
        if os.environ.has_key("CONFIG_CONFIG"):
            print "CONFIG_CONFIG is set to: " + os.environ["CONFIG_CONFIG"]
            print "Resetting CONFIG_CONFIG"
        os.environ["CONFIG_CONFIG"] = ":_:configdir_.:configpath_:configname_Configrc.exe:configexe_1:configargs_-stdout " + Configrc_args

        # Now reload the Configrc file.  We've actually already run it
        # once, but with the wrong command-line options.
        cpMgr = ConfigPageManager.getGlobalPtr()
        cpMgr.reloadImplicitPages()

        # This is our config object until we get the show running
        launcherConfig = getConfigExpress()
        __builtin__.config = launcherConfig

        # We'll need a MiniTaskManager to manage our download tasks
        # before we've downloaded enough to start the real one.
        self.miniTaskMgr = MiniTaskManager()

        # Should the launcher do md5 checks on the files?
        # We should probably take this out completely when we ship
        self.VerifyFiles = self.getVerifyFiles()
        self.setServerVersion(launcherConfig.GetString("server-version", "no_version_set"))
        self.ServerVersionSuffix = launcherConfig.GetString("server-version-suffix", "")

        # How many seconds should elapse between telling the user how the
        # download is progressing?
        self.UserUpdateDelay = launcherConfig.GetFloat('launcher-user-update-delay', 0.5)

        # How much telemetry the game server subtracts out (bytes per second)
        self.TELEMETRY_BANDWIDTH = launcherConfig.GetInt('launcher-telemetry-bandwidth', 2000)

        # If we are above the increase threshold percentage, then we will
        # increase the bandwidth
        self.INCREASE_THRESHOLD = launcherConfig.GetFloat('launcher-increase-threshold', 0.75)

        # If we are below the decrease threshold percentage, we will drop
        # back down to the next lower bandwidth
        self.DECREASE_THRESHOLD = launcherConfig.GetFloat('launcher-decrease-threshold', 0.5)

        # window length in seconds to look back when asking the
        # current byte rate
        self.BPS_WINDOW = launcherConfig.GetFloat('launcher-bps-window', 8.0)

        # Should we decrease the bandwidth when the connection is not
        # going as fast as it had in the past?
        self.DECREASE_BANDWIDTH = launcherConfig.GetBool('launcher-decrease-bandwidth', 1)

        # What is our ceiling on downloader bandwidth?  This is mainly
        # useful for testing.  Set it to 0 to impose no ceiling.
        self.MAX_BANDWIDTH = launcherConfig.GetInt('launcher-max-bandwidth', 0)

        # Give Panda the same log we use
        self.nout = MultiplexStream()
        Notify.ptr().setOstreamPtr(self.nout, 0)
        self.nout.addFile(Filename(logfile))

        if launcherConfig.GetBool('console-output', 0):
            # Dupe output to the console (stderr, stdout) only if a
            # developer has asked us to via the prc file.
            self.nout.addStandardOutput()
            sys.stdout.console = True
            sys.stderr.console = True

        # create a DirectNotify category for the Launcher
        self.notify = directNotify.newCategory("Launcher")

        # The launcher needs a reliable clock for various reasons
        self.clock = TrueClock.getGlobalPtr()

        # This prefix is also prepended to screenshot filenames.
        self.logPrefix = logPrefix

        # Is this the test server?
        self.testServerFlag = self.getTestServerFlag()
        self.notify.info("isTestServer: %s" % (self.testServerFlag))

        # The URL for the download server and directory.
        downloadServerString = launcherConfig.GetString('download-server', '')
        if downloadServerString:
            self.notify.info("Overriding downloadServer to %s." % (downloadServerString))
        else:
            downloadServerString = self.getValue('DOWNLOAD_SERVER', '')
        self.notify.info("Download Server List %s" % (downloadServerString))

        # server is a semicolon-delimited list of URL's.
        self.downloadServerList = []
        for name in string.split(downloadServerString, ';'):
            url = URLSpec(name, 1)
            self.downloadServerList.append(url)

        # self.downloadServer is the current download server we are
        # contemplating.  When it is proven bad, we switch to the next
        # one.
        self.nextDownloadServerIndex = 0
        self.getNextDownloadServer()

        self.gameServer = self.getGameServer()
        self.notify.info("Game Server %s" % (self.gameServer))

        # The number of times to retry each server
        self.downloadServerRetries = 3
        # Number of times to retry a multifile
        self.multifileRetries = 1
        self.curMultifileRetry = 0

        # The number of seconds to wait between retries
        self.downloadServerRetryPause = 1

        # Start at the top of the possible bandwidths, so we can
        # go downward to reach the actual bandwidth.
        self.bandwidthIndex = len(self.BANDWIDTH_ARRAY) - 1
        self.everIncreasedBandwidth = 0

        self.goUserName = ""

        # How much of each step counts towards the 99 percent
        # of having this phase be completely done
        # The last 1 percent is set when everything is done
        self.downloadPercentage = 90
        self.decompressPercentage = 5
        self.extractPercentage = 4

        self.lastLauncherMsg = None

        # Local client side directories
        self.topDir = Filename.fromOsSpecific(self.getValue(self.InstallDirKey, '.'))

        # set the gamelog filename in the registry
        self.setRegistry(self.GameLogFilenameKey, logfile)

        # If need to patch, determine which directory to patch from
        tmpVal = self.getValue(self.PatchCDKey)
        if tmpVal == None:
            self.fromCD = 0
        else:
            self.fromCD = tmpVal
        self.notify.info('patch directory is ' + `self.fromCD`)

        assert self.notify.debug("init: Launcher found install dir: " + self.topDir.cStr())

        # Relative directories from the topDir
        self.dbDir = self.topDir
        self.patchDir = self.topDir
        self.mfDir = self.topDir

        # The directory (within the version directory) in which to
        # find most files on the download server
        self.contentDir = 'content/'



        # The name of the client db file
        self.clientDbFilename = 'client.ddb'
        self.compClientDbFilename = self.clientDbFilename + '.pz'

        # The name of the server db file
        self.serverDbFilename = 'server.ddb'
        self.compServerDbFilename = self.serverDbFilename + '.pz'

        # The file path of the server db file on the download server
        self.serverDbFilePath = self.contentDir + self.compServerDbFilename

        # The file path of the client db file on the download server
        self.clientStarterDbFilePath = self.contentDir + self.compClientDbFilename

        # The file name of the progress meter file
        self.progressFilename = 'progress'
        self.overallComplete = 0
        self.progressSoFar = 0

        # Patch files extension
        self.patchExtension = 'pch'

        # scan for hack programs
        self.scanForHacks()

        # Start downloading at this phase
        self.firstPhase = self.LauncherPhases[0]
        self.finalPhase = self.LauncherPhases[-1]
        # Phase at which we may open a 3d window and start the show
        self.showPhase = 3.5
        self.numPhases = len(self.LauncherPhases)

        # A map of phase number -> percentDone. For example {3:100, 4:50, 5:0}
        self.phaseComplete = {}
        # We need a flag for each phase stating whether downloading the multifile or just patch
        self.phaseNewDownload = {}
        # Also a map of each phase in terms of overall download
        # todo: generate this list as part of build launcher
        self.phaseOverallMap = {}
        tmpOverallMap = self.TmpOverallMap
        tmpPhase3Map = [0.001,0.996,0.0,0.0,0.003]

        # Initialize all phases 0 percent done for starters
        phaseIdx = 0
        for phase in self.LauncherPhases:
            # Clear the registry on each phase's percentage completion
            percentPhaseCompleteKey = "PERCENT_PHASE_COMPLETE_" + `phase`
            self.setRegistry(percentPhaseCompleteKey, 0)
            # Initialize
            self.phaseComplete[phase] = 0
            self.phaseNewDownload[phase] = 0
            # Init each phases percentage in overall download
            self.phaseOverallMap[phase] = tmpOverallMap[phaseIdx]
            phaseIdx += 1

        self.patchList = []
        self.reextractList = []
        self.byteRate = 0
        self.byteRateRequested = 0
        self.resetBytesPerSecond()

        self.dldb = None
        self.currentMfname = None
        self.currentPhaseIndex = 0
        self.currentPhase = self.LauncherPhases[self.currentPhaseIndex]
        self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhaseIndex]

        # Make sure we were able to run Configrc.  Check the server
        # version as a flag for this.
        if self.getServerVersion() == 'no_version_set':
            self.setPandaErrorCode(10)
            self.notify.info("Aborting, Configrc did not run!")
            sys.exit()

        self.launcherMessage(self.Localizer.LauncherStartingMessage)

        # Every download uses this HTTPClient.
        self.http = HTTPClient()

        if self.http.getProxySpec() == '':
            # If the HTTPClient doesn't have a proxy already set from
            # the Configrc file, get this from the registry.
            self.http.setProxySpec(self.getValue(self.ProxyServerKey, ''))
            self.http.setDirectHostSpec(self.getValue(self.ProxyDirectHostsKey, ''))

        self.notify.info("Proxy spec is: %s" % (self.http.getProxySpec()))
        if self.http.getDirectHostSpec() != '':
            self.notify.info("Direct hosts list is: %s" % (self.http.getDirectHostSpec()))

        self.httpChannel = self.http.makeChannel(0)
        self.httpChannel.setDownloadThrottle(1)

        # First, try to find a download server that will talk to us at
        # all.
        connOk = 0
        while not connOk:
            proxies = self.http.getProxiesForUrl(self.downloadServer)
            if proxies == 'DIRECT':
                self.notify.info("No proxy for download.")
            else:
                self.notify.info("Download proxy: %s" % (proxies))

            testurl = self.addDownloadVersion(self.launcherFileDbFilename)
            connOk = self.httpChannel.getHeader(DocumentSpec(testurl))
            statusCode = self.httpChannel.getStatusCode()
            statusString = self.httpChannel.getStatusString()

            if not connOk:
                # No good.
                self.notify.warning("Could not contact download server at %s" % (testurl.cStr()))
                self.notify.warning("Status code = %s %s" % (statusCode, statusString))
                if statusCode == 407 or statusCode == 1407 or \
                   statusCode == HTTPChannel.SCSocksNoAcceptableLoginMethod:
                    self.setPandaErrorCode(3)
                elif statusCode == 404:
                    # A 404 means we're probably trying to access an
                    # old version.  We'll call this a
                    # server-refused-connection error.
                    self.setPandaErrorCode(13)
                elif statusCode < 100:
                    # statusCode below 100 implies the connection
                    # attempt itself failed.  This is usually due to
                    # firewall software interfering.
                    self.setPandaErrorCode(4)
                elif statusCode > 1000:
                    # A status code over 1000 means something went fubar
                    # with the proxy.
                    self.setPandaErrorCode(9)
                else:
                    # Some other status code means we could open a
                    # connection, but couldn't negotiate the download for
                    # some reason.  This is a bigger problem.
                    self.setPandaErrorCode(6)

                if not self.getNextDownloadServer():
                    sys.exit()

        self.notify.info("Download server: %s" % (self.downloadServer.cStr()))

        # Allow us to inc and dec the bandwidth by hand for testing
        if self.notify.getDebug():
            self.accept('page_up', self.increaseBandwidth)
            self.accept('page_down', self.decreaseBandwidth)

        # From now on, we will attempt to re-use the same connection
        # to the download server, once we are connected.
        self.httpChannel.setPersistentConnection(1)

        # Start in the foreground
        self.foreground()
        self.prepareClient()
        self.setBandwidth()
        self.downloadLauncherFileDb()

    def getTime(self):
        return self.clock.getShortTime()

    def isDummy(self):
        # Is this the DummyLauncher? No
        return 0

    def getNextDownloadServer(self):
        if self.nextDownloadServerIndex >= len(self.downloadServerList):
            # There are no more download servers to try.  Too bad.
            self.downloadServer = None
            return 0

        # There are more download servers to try; try the next one.
        self.downloadServer = self.downloadServerList[self.nextDownloadServerIndex]
        self.notify.info("Using download server %s." % (self.downloadServer.cStr()))
        self.nextDownloadServerIndex += 1
        return 1

    def getProductName(self):
        config = getConfigExpress()
        productName = config.GetString('product-name', '')
        if productName and (productName != 'DisneyOnline-US'):
            productName = "_%s" % productName
        else:
            productName = ''
        return productName


    #============================================================
    #   Priority functions
    #============================================================

    def background(self):
        # Make the launcher operate in the background
        self.notify.info('background: Launcher now operating in background')
        self.backgrounded = 1

    def foreground(self):
        # Make the launcher operate in the foreground
        self.notify.info('foreground: Launcher now operating in foreground')
        self.backgrounded = 0

    #============================================================
    #   Registry functions
    #============================================================

    def setRegistry(self, key, value):
        self.notify.info('DEPRECATED setRegistry: %s = %s' % (key, value))
        return

    def getRegistry(self, key):
        self.notify.info('DEPRECATED getRegistry: %s' % (key))
        return None

    #============================================================
    #   Error Handling
    #============================================================

    def handleInitiateFatalError(self, errorCode):
        self.notify.warning('handleInitiateFatalError: ' + errorToText(errorCode))
        # TODO: set error code
        sys.exit()

    def handleDecompressFatalError(self, task, errorCode):
        self.notify.warning('handleDecompressFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDecompressWriteError(self, task, errorCode):
        self.notify.warning('handleDecompressWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDecompressZlibError(self, task, errorCode):
        self.notify.warning('handleDecompressZlibError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleExtractFatalError(self, task, errorCode):
        self.notify.warning('handleExtractFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleExtractWriteError(self, task, errorCode):
        self.notify.warning('handleExtractWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handlePatchFatalError(self, task, errorCode):
        self.notify.warning('handlePatchFatalError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handlePatchWriteError(self, task, errorCode):
        self.notify.warning('handlePatchWriteError: ' + errorToText(errorCode))
        self.miniTaskMgr.remove(task)
        self.handleGenericMultifileError()

    def handleDownloadFatalError(self, task):
        # This function may return if we should try the download
        # again, or it will not return if we are out of download
        # servers to try.

        self.notify.warning('handleDownloadFatalError: status code = %s %s' %
                            (self.httpChannel.getStatusCode(), self.httpChannel.getStatusString()))
        self.miniTaskMgr.remove(task)
        statusCode = self.httpChannel.getStatusCode()
        if statusCode == 404:
            self.setPandaErrorCode(5)
        elif statusCode < 100:
            # statusCode < 100 implies the connection attempt itself
            # failed.  This is usually due to firewall software
            # interfering.  Apparently some firewall software might
            # allow the first connection and disallow subsequent
            # connections; how strange.
            self.setPandaErrorCode(4)
        else:
            # There are other kinds of failures, but these will
            # generally have been caught already by the first test; so
            # if we get here there may be some bigger problem.  Just
            # give the generic "big problem" message.
            self.setPandaErrorCode(6)

        if not self.getNextDownloadServer():
            sys.exit()

    def handleDownloadWriteError(self, task):
        self.notify.warning('handleDownloadWriteError.')
        self.miniTaskMgr.remove(task)
        self.setPandaErrorCode(2)
        sys.exit()

    def handleGenericMultifileError(self):
        if not self.currentMfname:
            # TODO: we got an error outside a multifile. Could have been
            # some error downloading the databases. This case is not
            # handled yet, and should be rare.
            # TODO: We should set an error code
            sys.exit()

        if self.curMultifileRetry < self.multifileRetries:
            self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
            self.curMultifileRetry += 1
            # Ok, something did not work for some reason. Well I guess
            # we have to redownload the entire phase now. I admit, this is
            # a big hammer, but problems in this area tend to be fundamental
            # problems with the initial file data and require a redownload.
            self.notify.info('downloadPatchDone: Recovering from error.'
                             + ' Deleting files in: ' + self.currentMfname)
            # Mark this multifile as incomplete now
            self.dldb.setClientMultifileIncomplete(self.currentMfname)
            # Mark it as size 0
            self.dldb.setClientMultifileSize(self.currentMfname, 0)
            # Redownload this multifile
            self.notify.info('downloadPatchDone: Recovering from error.'
                             + ' redownloading: ' + self.currentMfname)
            # Cleanup the HTTP in case it was halfway into something
            self.httpChannel.reset()
            self.getMultifile(self.currentMfname)
        else:
            self.setPandaErrorCode(6)
            self.notify.info('handleGenericMultifileError: Failed to download multifile')
            sys.exit()

    def foregroundSleep(self):
        # If we are running in the foreground, we do not want to
        # consume all the cpu, so we will sleep for a moment here
        if not self.backgrounded:
            time.sleep(self.ForegroundSleepTime)

    def forceSleep(self):
        # If we are running in the foreground, we do not want to
        # consume all the cpu, so we will sleep for a moment here
        if not self.backgrounded:
            time.sleep(3.00)

    #============================================================
    # Download functions
    #============================================================

    def addDownloadVersion(self, serverFilePath):
        url = URLSpec(self.downloadServer)
        origPath = url.getPath()
        if origPath and origPath[-1] == '/':
            origPath = origPath[:-1]

        if self.fromCD:
            url.setPath(self.getCDDownloadPath(origPath, serverFilePath))
        else:
            url.setPath(self.getDownloadPath(origPath, serverFilePath))

        self.notify.info('***' + url.cStr())

        return url

    def download(self, serverFilePath, localFilename, callback,
                 callbackProgress):
        self.launcherMessage(self.Localizer.LauncherDownloadFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total": self.numPhases,})
        task = MiniTask(self.downloadTask)
        task.downloadRam = 0
        task.serverFilePath = serverFilePath
        task.serverFileURL = self.addDownloadVersion(serverFilePath)
        self.notify.info('Download request: %s' % (task.serverFileURL.cStr()))
        task.callback = callback
        task.callbackProgress = callbackProgress
        task.lastUpdate = 0
        self.resetBytesPerSecond()
        task.localFilename = localFilename

        # Initiate the download
        self.httpChannel.beginGetDocument(DocumentSpec(task.serverFileURL))
        self.httpChannel.downloadToFile(task.localFilename)
        self.miniTaskMgr.add(task, 'launcher-download')

    def downloadRam(self, serverFilePath, callback):
        self.ramfile = Ramfile()

        task = MiniTask(self.downloadTask)
        task.downloadRam = 1
        task.serverFilePath = serverFilePath
        task.serverFileURL = self.addDownloadVersion(serverFilePath)
        self.notify.info('Download request: %s' % task.serverFileURL.cStr())
        task.callback = callback
        task.callbackProgress = None
        task.lastUpdate = 0
        self.resetBytesPerSecond()

        # Initiate the download
        self.httpChannel.beginGetDocument(DocumentSpec(task.serverFileURL))
        self.httpChannel.downloadToRam(self.ramfile)
        self.miniTaskMgr.add(task, 'launcher-download')

    def downloadTask(self, task):
        self.maybeStartGame()
        if self.httpChannel.run():
            # Nothing to read, nothing wrong, come back next frame

            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                self.testBandwidth()

                # We do not update the downloadDb with these files,
                # only multifiles.
                if (task.callbackProgress):
                    task.callbackProgress(task)
                bytesWritten = self.httpChannel.getBytesDownloaded()
                totalBytes = self.httpChannel.getFileSize()
                if totalBytes:
                    pct = int(round(bytesWritten/float(totalBytes) * 100))
                    self.launcherMessage(self.Localizer.LauncherDownloadFilePercent %
                                         {"name": self.currentPhaseName,
                                          "current": self.currentPhaseIndex,
                                          "total":   self.numPhases,
                                          "percent": pct})
                else:
                    self.launcherMessage(self.Localizer.LauncherDownloadFileBytes %
                                         {"name": self.currentPhaseName,
                                          "current": self.currentPhaseIndex,
                                          "total":   self.numPhases,
                                          "bytes":   bytesWritten,})
            self.foregroundSleep()
            return task.cont

        statusCode = self.httpChannel.getStatusCode()
        statusString = self.httpChannel.getStatusString()
        self.notify.info('HTTP status %s: %s' % (statusCode, statusString))

        if self.httpChannel.isValid() and \
           self.httpChannel.isDownloadComplete():
            # We do not update the downloadDb with these files, only
            # multifiles.
            bytesWritten = self.httpChannel.getBytesDownloaded()
            totalBytes = self.httpChannel.getFileSize()
            if totalBytes:
                pct = int(round(bytesWritten/float(totalBytes) * 100))
                self.launcherMessage(self.Localizer.LauncherDownloadFilePercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": pct,})
            else:
                self.launcherMessage(self.Localizer.LauncherDownloadFileBytes %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "bytes":   bytesWritten,})
            # NOTE: we do not set the percent phase complete flag here
            self.notify.info('downloadTask: Download done: %s' % (task.serverFileURL.cStr()))
            # Call the done callback
            task.callback()
            del task.callback
            return task.done

        else:
            # Something screwed up.
            if statusCode == HTTPChannel.SCDownloadOpenError or \
               statusCode == HTTPChannel.SCDownloadWriteError:
                self.handleDownloadWriteError(task)

            elif statusCode == HTTPChannel.SCLostConnection:
                # We started downloading, but we lost the connection
                # midstream.  Try again.
                gotBytes = self.httpChannel.getBytesDownloaded()
                self.notify.info('Connection lost while downloading; got %s bytes.  Reconnecting.' % (gotBytes))
                if task.downloadRam:
                    self.downloadRam(task.serverFilePath, task.callback)
                else:
                    self.download(task.serverFilePath, task.localFilename,
                                  task.callback, None)

            else:
                # 404 not found or some such nonsense.
                if self.httpChannel.isValid():
                    # Huh?
                    self.notify.info('Unexpected situation: no error status, but %s incompletely downloaded.' % (task.serverFileURL.cStr()))
                self.handleDownloadFatalError(task)
                if task.downloadRam:
                    self.downloadRam(task.serverFilePath, task.callback)
                else:
                    self.download(task.serverFilePath, task.localFilename,
                                  task.callback, None)
            return task.done

    #============================================================
    # Download multifile functions
    #============================================================

    def downloadMultifile(self, serverFilename, localFilename, mfname,
                          callback, totalSize, currentSize, callbackProgress):
        if (currentSize != 0) and (currentSize == totalSize):
            assert self.notify.debug('downloadMultifile: already done')
            callback()
            return
        
        self.launcherMessage(self.Localizer.LauncherDownloadFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total":   self.numPhases,})
        task = MiniTask(self.downloadMultifileTask)
        mfURL = self.addDownloadVersion(serverFilename)
        task.mfURL = mfURL
        self.notify.info('downloadMultifile: %s ' % (task.mfURL.cStr()))
        task.callback = callback
        task.callbackProgress = callbackProgress
        task.lastUpdate = 0
        
        self.httpChannel.getHeader(DocumentSpec(task.mfURL))
        if self.httpChannel.isFileSizeKnown():
            task.totalSize = self.httpChannel.getFileSize()
            assert self.notify.debug('totalSize from header=%s' % task.totalSize)
        else:
            task.totalSize = totalSize
            assert self.notify.debug('totalSize from caller=%s' % task.totalSize)
        self.resetBytesPerSecond()
        task.serverFilename = serverFilename
        task.localFilename = localFilename
        task.mfname = mfname

        if currentSize != 0:
            if task.totalSize == currentSize:
                self.notify.info('already have full file! Skipping download.')
                callback()
                return
            
            self.httpChannel.beginGetSubdocument(DocumentSpec(task.mfURL), currentSize, task.totalSize)
            self.httpChannel.downloadToFile(task.localFilename, True)
        else:
            # Full download
            self.httpChannel.beginGetDocument(DocumentSpec(task.mfURL))
            self.httpChannel.downloadToFile(task.localFilename)

        self.miniTaskMgr.add(task, 'launcher-download-multifile')

    def downloadPatchSimpleProgress(self, task):
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        totalBytes = self.httpChannel.getFileSize()
        assert self.notify.debug("downloadPatchSimpleProgress: bytesWritten: %s totalBytes: %s" %
                                 (bytesWritten, totalBytes))
        percentPatchComplete = int(round(bytesWritten/float(totalBytes) * self.downloadPercentage))
        self.setPercentPhaseComplete(self.currentPhase, percentPatchComplete)

    def getPercentPatchComplete(self, bytesWritten):
        return int(round((self.patchDownloadSoFar + bytesWritten)/float(self.totalPatchDownload)
                         * self.downloadPercentage))

    def downloadPatchOverallProgress(self, task):
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        assert self.notify.debug("downloadPatchOverallProgress: bytesWritten: " + str(bytesWritten))

        # Calculate the percent done as an int
        # Only consider the download 90 percent of the process
        # We still need to decompress and extract it too
        #self.notify.info('^^^^^download so far = ' + `bytesWritten` + ' $' + `self.patchDownloadSoFar`)
        percentPatchComplete = self.getPercentPatchComplete(bytesWritten)
            
        # Set the percent done in the phase map for phase_3 only
        # NOTE: this assumes one multifile per phase, that is, the progress
        # through this single multifile represents the progress through the
        # current phase. Do not ever set to 100 to prevent roundup from
        # prematurely reporting 100. Instead only report 99 here
        #self.notify.info('-------percent patch complete = ' + `percentPatchComplete`)
        self.setPercentPhaseComplete(self.currentPhase, percentPatchComplete)

    def downloadMultifileWriteToDisk(self, task):
        self.maybeStartGame()
        startingByte = self.httpChannel.getFirstByteDelivered()
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesWritten = startingByte + bytesDownloaded
        assert self.notify.debug("bytesWritten: " + str(bytesWritten))

        # Read some bytes and write them to disk.
        # The download db needs to be told about these bytes
        # Record that this multifile has been partially downloaded
        if self.dldb:
            self.dldb.setClientMultifileSize(task.mfname, bytesWritten)

        # Calculate the percent done as an int
        # Only consider the download 90 percent of the process
        # We still need to decompress and extract it too
        percentComplete = 0
        if task.totalSize != 0:
            percentComplete = int(round(bytesWritten/float(task.totalSize)
                                        * self.downloadPercentage))
        # Set the percent done in the phase map
        # NOTE: this assumes one multifile per phase, that is, the progress
        # through this single multifile represents the progress through the
        # current phase. Do not ever set to 100 to prevent roundup from
        # prematurely reporting 100. Instead only report 99 here
        self.setPercentPhaseComplete(self.currentPhase, percentComplete)

    def downloadMultifileTask(self, task):
        # This is a hack to get around some weird behavior observed on
        # pirates with the httpChannel
        task.totalSize = self.httpChannel.getFileSize()

        if self.httpChannel.run():
            # Nothing to read, nothing wrong, come back next frame

            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                self.testBandwidth()
                #self.downloadMultifileWriteToDisk(task)
                if (task.callbackProgress):
                    task.callbackProgress(task)
                startingByte = self.httpChannel.getFirstByteDelivered()
                bytesDownloaded = self.httpChannel.getBytesDownloaded()
                bytesWritten = startingByte + bytesDownloaded
                percentComplete = 0
                if task.totalSize != 0:
                    percentComplete = int(round( 100.0 * bytesWritten / float(task.totalSize)))
                
                # We need this feedback if we are on the updating page
                self.launcherMessage(self.Localizer.LauncherDownloadFilePercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": percentComplete})
            self.foregroundSleep()
            return task.cont

        statusCode = self.httpChannel.getStatusCode()
        statusString = self.httpChannel.getStatusString()
        self.notify.info('HTTP status %s: %s' % (statusCode, statusString))

        if self.httpChannel.isValid() and \
           self.httpChannel.isDownloadComplete():
            #self.downloadMultifileWriteToDisk(task)
            if (task.callbackProgress):
                task.callbackProgress(task)
            # NOTE: we do not set the percent phase complete flag here
            self.notify.info('done: %s' % (task.mfname))
            # Record that this multifile has been completely downloaded
            if self.dldb:
                self.dldb.setClientMultifileComplete(task.mfname)
            # Call the done callback
            task.callback()
            del task.callback
            return task.done

        else:
            # Something screwed up.
            if statusCode == HTTPChannel.SCDownloadOpenError or \
               statusCode == HTTPChannel.SCDownloadWriteError:
                self.handleDownloadWriteError(task)

            elif statusCode == HTTPChannel.SCLostConnection:
                # We started downloading, but we lost the connection
                # midstream.  Try again.
                startingByte = self.httpChannel.getFirstByteDelivered()
                bytesDownloaded = self.httpChannel.getBytesDownloaded()
                bytesWritten = startingByte + bytesDownloaded
                
                self.notify.info('Connection lost while downloading; got %s bytes.  Reconnecting.' % (bytesDownloaded))
                self.downloadMultifile(task.serverFilename, task.localFilename,
                                       task.mfname,
                                       task.callback, task.totalSize,
                                       bytesWritten, task.callbackProgress)

            elif (statusCode == 416 or statusCode == HTTPChannel.SCDownloadInvalidRange) and self.httpChannel.getFirstByteRequested() != 0:
                # Invalid subrange.  Screw it; download the whole file again.
                self.notify.info('Invalid subrange; redownloading entire file.')
                self.downloadMultifile(task.serverFilename, task.localFilename,
                                       task.mfname,
                                       task.callback, task.totalSize,
                                       0, task.callbackProgress)
                
            else:
                # 404 not found or some such nonsense.
                if self.httpChannel.isValid():
                    # Huh?
                    self.notify.info('Unexpected situation: no error status, but %s incompletely downloaded.' % (task.mfname))
                self.handleDownloadFatalError(task)
                self.downloadMultifile(task.serverFilename, task.localFilename,
                                       task.mfname,
                                       task.callback, task.totalSize,
                                       0, task.callbackProgress)
            return task.done

    #============================================================
    # Decompress individual file functions
    #============================================================

    def decompressFile(self, localFilename, callback):
        self.notify.info('decompress: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile  %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total":   self.numPhases,})
        task = MiniTask(self.decompressFileTask)
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = Decompressor()
        errorCode = task.decompressor.initiate(task.localFilename)
        if (errorCode > 0):
            self.miniTaskMgr.add(task, 'launcher-decompressFile')
        else:
            self.handleInitiateFatalError(errorCode)

    def decompressFileTask(self, task):
        #if self.notify.getDebug():
        #    beforeTime = self.getTime()
        errorCode = task.decompressor.run()
        #if self.notify.getDebug():
        #    self.notify.debug("decompressTask run(): " + str(self.getTime() - beforeTime))
        if (errorCode == EUOk):
            # Everything is proceeding normally, come back next frame

            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                progress = task.decompressor.getProgress()
                # We need this message if we are on the updating screen
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": int(round(progress * 100)),})
            self.foregroundSleep()
            return task.cont
        elif (errorCode == EUSuccess):
            # Decompression is done
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent %
                                 {"name": self.currentPhaseName,
                                  "current": self.currentPhaseIndex,
                                  "total":   self.numPhases,
                                  "percent": 100,})
            self.notify.info('decompressTask: Decompress done: '
                              + task.localFilename.cStr())
            # Get rid of the decompressor
            del task.decompressor
            task.callback()
            del task.callback
            return task.done
        elif (errorCode == EUErrorAbort):
            self.handleDecompressFatalError(task, errorCode)
            return task.done
        elif ((errorCode == EUErrorWriteOutOfFiles) or
              (errorCode == EUErrorWriteDiskFull) or
              (errorCode == EUErrorWriteDiskSectorNotFound) or
              (errorCode == EUErrorWriteOutOfMemory) or
              (errorCode == EUErrorWriteSharingViolation) or
              (errorCode == EUErrorWriteDiskFault) or
              (errorCode == EUErrorWriteDiskNotFound)
              ):
            self.handleDecompressWriteError(task, errorCode)
            return task.done
        elif (errorCode == EUErrorZlib):
            self.handleDecompressZlibError(task, errorCode)
            return task.done
        elif (errorCode > 0):
            # If we get an error code that is positive, but we are not handling it, throw
            # a warning and continue
            self.notify.warning('decompressMultifileTask: Unknown success return code: '
                                + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('decompressMultifileTask: Unknown return code: '
                              + errorToText(errorCode))
            self.handleDecompressFatalError(task, errorCode)
            return task.done

    #============================================================
    # DecompressMultifile functions
    #============================================================

    def decompressMultifile(self, mfname, localFilename, callback):
        self.notify.info('decompressMultifile: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total":   self.numPhases,})
        task = MiniTask(self.decompressMultifileTask)
        task.mfname = mfname
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = Decompressor()
        errorCode = task.decompressor.initiate(task.localFilename)
        if (errorCode > 0):
            self.miniTaskMgr.add(task, 'launcher-decompressMultifile')
        else:
            self.handleInitiateFatalError(errorCode)

    def decompressMultifileTask(self, task):
        #if self.notify.getDebug():
        #    beforeTime = self.getTime()
        errorCode = task.decompressor.run()
        #if self.notify.getDebug():
        #    self.notify.debug("decompressMultifileTask run(): " + str(self.getTime() - beforeTime))
        if (errorCode == EUOk):
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                progress = task.decompressor.getProgress()
                # We need this message if we are on the updating screen
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": int(round(progress * 100)),})
                percentProgress = int(round(progress * self.decompressPercentage))
                # By now you have completed download, so add that in
                totalPercent = (self.downloadPercentage + percentProgress)
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)

            # Everything is proceeding normally, come back next frame
            self.foregroundSleep()
            return task.cont
        elif (errorCode == EUSuccess):
            # Decompression is done
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": 100, })

            totalPercent = (self.downloadPercentage + self.decompressPercentage)
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('decompressMultifileTask: Decompress multifile done: '
                              + task.localFilename.cStr())
            self.dldb.setClientMultifileDecompressed(task.mfname)
            # Get rid of the decompressor
            del task.decompressor
            task.callback()
            del task.callback
            return task.done
        elif (errorCode == EUErrorAbort):
            self.handleDecompressFatalError(task, errorCode)
            return task.done
        elif ((errorCode == EUErrorWriteOutOfFiles) or
              (errorCode == EUErrorWriteDiskFull) or
              (errorCode == EUErrorWriteDiskSectorNotFound) or
              (errorCode == EUErrorWriteOutOfMemory) or
              (errorCode == EUErrorWriteSharingViolation) or
              (errorCode == EUErrorWriteDiskFault) or
              (errorCode == EUErrorWriteDiskNotFound)
              ):
            self.handleDecompressWriteError(task, errorCode)
            return task.done
        elif (errorCode == EUErrorZlib):
            self.handleDecompressZlibError(task, errorCode)
            return task.done
        elif (errorCode > 0):
            # If we get an error code that is positive, but we are not handling it, throw
            # a warning and continue
            self.notify.warning('decompressMultifileTask: Unknown success return code: '
                                + errorToText(errorCode))
            return task.cont
        else:
            self.notify.warning('decompressMultifileTask: Unknown return code: '
                              + errorToText(errorCode))
            self.handleDecompressFatalError(task, errorCode)
            return task.done

    #============================================================
    # Extract functions
    #============================================================

    def extract(self, mfname, localFilename, destDir, callback):
        self.notify.info('extract: request: ' + localFilename.cStr() +
                          ' destDir: ' + destDir.cStr())
        self.launcherMessage(self.Localizer.LauncherExtractingFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total": self.numPhases,})
        task = MiniTask(self.extractTask)
        task.mfname = mfname
        task.localFilename = localFilename
        task.destDir = destDir
        task.callback = callback
        task.lastUpdate = 0
        task.extractor = Extractor()
        task.extractor.setExtractDir(task.destDir)
        if not task.extractor.setMultifile(task.localFilename):
            self.setPandaErrorCode(6)
            self.notify.info("extract: Unable to open multifile %s" % task.localFilename.cStr())
            sys.exit()

        # Temporary debug output
        #self.dldb.write(Notify.out())

        numFiles = self.dldb.getServerNumFiles(mfname)
        for i in range(numFiles):
            subfile = self.dldb.getServerFileName(mfname, i)
            if not task.extractor.requestSubfile(Filename(subfile)):
                self.setPandaErrorCode(6)
                self.notify.info("extract: Unable to find subfile %s in multifile %s" % (subfile, mfname))
                sys.exit()

        self.notify.info("Extracting %d subfiles from multifile %s." % (numFiles, mfname))
        self.miniTaskMgr.add(task, 'launcher-extract')

    def extractTask(self, task):
        #if self.notify.getDebug():
        #    beforeTime = self.getTime()
        errorCode = task.extractor.step()
        #if self.notify.getDebug():
        #    self.notify.debug("extractTask run(): " + str(self.getTime() - beforeTime))
        if (errorCode == EUOk):
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                progress = task.extractor.getProgress()
                self.launcherMessage(self.Localizer.LauncherExtractingPercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": int(round(progress * 100.0)),})
                percentProgress = int(round(progress * self.extractPercentage))

                # By now you have completed download and decompress, so add those in
                totalPercent = (self.downloadPercentage + self.decompressPercentage + percentProgress)
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            # Everything is proceeding normally, come back next frame
            self.foregroundSleep()
            return task.cont
        elif (errorCode == EUSuccess):
            # Extraction is done
            self.launcherMessage(self.Localizer.LauncherExtractingPercent %
                                 {"name": self.currentPhaseName,
                                  "current": self.currentPhaseIndex,
                                  "total":   self.numPhases,
                                  "percent": 100,})
            totalPercent = (self.downloadPercentage + self.decompressPercentage + self.extractPercentage)
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('extractTask: Extract multifile done: '
                              + task.localFilename.cStr())
            self.dldb.setClientMultifileExtracted(task.mfname)
            # Get rid of the extractor
            del task.extractor
            task.callback()
            del task.callback
            return task.done
        elif (errorCode == EUErrorAbort):
            self.handleExtractFatalError(task, errorCode)
            return task.done
        elif (errorCode == EUErrorFileEmpty):
            self.handleExtractFatalError(task, errorCode)
            return task.done
        elif ((errorCode == EUErrorWriteOutOfFiles) or
              (errorCode == EUErrorWriteDiskFull) or
              (errorCode == EUErrorWriteDiskSectorNotFound) or
              (errorCode == EUErrorWriteOutOfMemory) or
              (errorCode == EUErrorWriteSharingViolation) or
              (errorCode == EUErrorWriteDiskFault) or
              (errorCode == EUErrorWriteDiskNotFound)
              ):
            self.handleExtractWriteError(task, errorCode)
            return task.done
        elif (errorCode > 0):
            # If we get an error code that is positive, but we are not handling it, throw
            # a warning and continue
            self.notify.warning('extractTask: Unknown success return code: '
                                + errorToText(errorCode))
            return task.cont
        else:
            # All other errors are negative, just catch them here for now
            self.notify.warning('extractTask: Unknown error return code: '
                              + errorToText(errorCode))
            self.handleExtractFatalError(task, errorCode)
            return task.done

    #============================================================
    # Patch functions
    #============================================================

    def patch(self, patchFile, patcheeFile, callback):
        self.notify.info('patch: request: ' + patchFile.cStr() +
                          ' patchee: ' + patcheeFile.cStr())
        self.launcherMessage(self.Localizer.LauncherPatchingFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total": self.numPhases,})
        task = MiniTask(self.patchTask)
        task.patchFile = patchFile
        task.patcheeFile = patcheeFile
        task.callback = callback
        task.lastUpdate = 0
        task.patcher = Patcher()
        errorCode = task.patcher.initiate(task.patchFile, task.patcheeFile)
        if (errorCode > 0):
            self.miniTaskMgr.add(task, 'launcher-patch')
        else:
            self.handleInitiateFatalError(errorCode)

    def patchTask(self, task):
        #if self.notify.getDebug():
        #    beforeTime = self.getTime()
        errorCode = task.patcher.run()
        #if self.notify.getDebug():
        #    self.notify.debug("patchTask run(): " + str(self.getTime() - beforeTime))
        if (errorCode == EUOk):
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                progress = task.patcher.getProgress()
                self.launcherMessage(self.Localizer.LauncherPatchingPercent %
                                     {"name": self.currentPhaseName,
                                      "current": self.currentPhaseIndex,
                                      "total":   self.numPhases,
                                      "percent": int(round(progress * 100.0)),})
            # Everything is proceeding normally, come back next frame
            self.foregroundSleep()
            return task.cont
        elif (errorCode == EUSuccess):
            # Patch is done
            self.launcherMessage(self.Localizer.LauncherPatchingPercent %
                                 {"name": self.currentPhaseName,
                                  "current": self.currentPhaseIndex,
                                  "total":   self.numPhases,
                                  "percent": 100,})
            self.notify.info('patchTask: Patch done: ' + task.patcheeFile.cStr())
            # Get rid of the patcher
            del task.patcher
            task.callback()
            del task.callback
            return task.done
        elif (errorCode == EUErrorAbort):
            self.handlePatchFatalError(task, errorCode)
            return task.done
        elif (errorCode == EUErrorFileEmpty):
            self.handlePatchFatalError(task, errorCode)
            return task.done
        elif ((errorCode == EUErrorWriteOutOfFiles) or
              (errorCode == EUErrorWriteDiskFull) or
              (errorCode == EUErrorWriteDiskSectorNotFound) or
              (errorCode == EUErrorWriteOutOfMemory) or
              (errorCode == EUErrorWriteSharingViolation) or
              (errorCode == EUErrorWriteDiskFault) or
              (errorCode == EUErrorWriteDiskNotFound)
              ):
            self.handlePatchWriteError(task, errorCode)
            return task.done
        elif (errorCode > 0):
            # If we get an error code that is positive, but we are not handling it, throw
            # a warning and continue
            self.notify.warning('patchTask: Unknown success return code: '
                                + errorToText(errorCode))
            return task.cont
        else:
            # All other errors are negative, just catch them here for now
            self.notify.warning('patchTask: Unknown error return code: '
                              + errorToText(errorCode))
            self.handlePatchFatalError(task, errorCode)
            return task.done

    #============================================================
    # Overall progress meter functions 
    #============================================================

    def getProgressSum(self, phase):         

        # given the phase lookup its sum
        sum = 0
        for i in xrange(0,len(self.linesInProgress)):
            # search for phase and sum the sizes for each
            if self.linesInProgress[i].find(phase) > -1:
                #split it, find the size, add to the sum
                #self.notify.info(self.linesInProgress[i]);
                nameSizeTuple = self.linesInProgress[i].split()
                # get rid of the L from the number
                numSize = nameSizeTuple[1].split('L')
                sum += string.atoi(numSize[0])
        return sum

    def readProgressFile(self):
        # parse those filenames and their sizes to get a sum
        localFilename = Filename(self.dbDir, Filename(self.progressFilename))
        if not localFilename.exists():
            self.notify.warning("File does not exist: %s" % (localFilename.cStr()))
            self.linesInProgress = []
        else:
            f = open(localFilename.toOsSpecific())
            self.linesInProgress = f.readlines()
            f.close()

            # remove the file it is no longer needed
            localFilename.unlink()
            
        self.progressSum = 0
        token = 'phase_'

        self.progressSum = self.getProgressSum(token)
        # deduct phase_2 files, I don't think this is downloaded
        self.progressSum -= self.getProgressSum(token + '2')
        self.notify.info('total phases to be downloaded = ' + `self.progressSum`)
        # done reading the file, now carry on with client download
        self.checkClientDbExists()


    #============================================================
    #  Main flow control of Launcher
    #============================================================

    def prepareClient(self):
        self.notify.info('prepareClient: Preparing client for install')
        # Make the local directories if they do not already exist
        if not self.topDir.exists():
            self.notify.info('prepareClient: Creating top directory: ' + self.topDir.cStr())
            os.makedirs(self.topDir.toOsSpecific())
        if not self.dbDir.exists():
            self.notify.info('prepareClient: Creating db directory: ' + self.dbDir.cStr())
            os.makedirs(self.dbDir.toOsSpecific())
        if not self.patchDir.exists():
            self.notify.info('prepareClient: Creating patch directory: ' + self.patchDir.cStr())
            os.makedirs(self.patchDir.toOsSpecific())
        if not self.mfDir.exists():
            self.notify.info('prepareClient: Creating mf directory: ' + self.mfDir.cStr())
            os.makedirs(self.mfDir.toOsSpecific())

    def downloadLauncherFileDb(self):
        # We do this whole download of launcherFileDb and verification
        # of the launcher files again, even though the ActiveX
        # installer has presumably done this already, as an additional
        # precaution.  It's possible that a curious user has invoked
        # the exe directly, without going through the web page
        # (and hence without running ActiveX).  Also, we need to have
        # the launcherFileDb contents to pass its hash to the server
        # on login.

        self.notify.info('Downloading launcherFileDb') 
        self.downloadRam(self.launcherFileDbFilename, self.downloadLauncherFileDbDone)
        
    def downloadLauncherFileDbDone(self):
        self.launcherFileDbHash = HashVal()
        self.launcherFileDbHash.hashRamfile(self.ramfile)

        if self.VerifyFiles:
            self.notify.info('Validating Launcher files')
            for fileDesc in self.ramfile.readlines():
                try:
                    filename, hashStr = fileDesc.split(' ', 1)
                except:
                    self.notify.info('Invalid line: "%s"' % (fileDesc))
                    self.failLauncherFileDb('No hash in launcherFileDb')

                serverHash = HashVal()
                if not self.hashIsValid(serverHash, hashStr):
                    self.notify.info('Not a valid hash string: "%s"' % (hashStr))
                    self.failLauncherFileDb('Invalid hash in launcherFileDb')

                localHash = HashVal()
                localFilename = Filename(self.topDir, Filename(filename))
                localHash.hashFile(localFilename)
                if localHash != serverHash:
                    assert self.notify.debug('expected %s' % (serverHash.asDec()))
                    assert self.notify.debug('     got %s' % (localHash.asDec()))
                    self.failLauncherFileDb('%s does not match expected version.' % (filename))

        self.downloadServerDbFile()

    def failLauncherFileDb(self, string):
        self.notify.info(string)
        self.setPandaErrorCode(15)
        sys.exit()
            
    def downloadServerDbFile(self):
        self.notify.info('Downloading server db file')
        self.launcherMessage(self.Localizer.LauncherDownloadServerFileList)
        self.downloadRam(self.serverDbFilePath, self.downloadServerDbFileDone)

    def downloadServerDbFileDone(self):
        self.serverDbFileHash = HashVal()
        self.serverDbFileHash.hashRamfile(self.ramfile)
        
        # Now check to see if we have the client db
        self.readProgressFile()
        #self.checkClientDbExists()

    def checkClientDbExists(self):
        # See if the client database exists. If it does, create the download db.
        clientFilename = Filename(self.dbDir, Filename(self.clientDbFilename))
        if clientFilename.exists():
            self.notify.info('Client Db exists')
            self.createDownloadDb()
        # If it does not, then we need to download the starter client db
        else:
            self.notify.info('Client Db does not exist')
            self.downloadClientDbStarterFile()

    def downloadClientDbStarterFile(self):
        self.notify.info('Downloading Client Db starter file')
        localFilename = Filename(self.dbDir, Filename(self.compClientDbFilename))
        self.download(self.clientStarterDbFilePath,
                      localFilename,
                      self.downloadClientDbStarterFileDone, None)

    def downloadClientDbStarterFileDone(self):
        # Decompress the file. This file is too small to worry about doing it async.
        localFilename = Filename(self.dbDir, Filename(self.compClientDbFilename))
        decompressor = Decompressor()
        decompressor.decompress(localFilename)
        # Ok, now create the download db
        self.createDownloadDb()

    def createDownloadDb(self):
        self.notify.info('Creating downloadDb')
        self.launcherMessage(self.Localizer.LauncherCreatingDownloadDb)
        clientFilename = Filename(self.dbDir, Filename(self.clientDbFilename))
        self.notify.info('Client file name: ' + clientFilename.cStr())
        #serverFilename = Filename(self.dbDir, Filename(self.serverDbFilename))
        self.launcherMessage(self.Localizer.LauncherDownloadClientFileList)
        serverFile = self.ramfile
        decompressor = Decompressor()
        decompressor.decompress(serverFile)
        self.notify.info('Finished decompress')
        self.dldb = DownloadDb(serverFile, clientFilename)
        self.notify.info('created download db')
        self.launcherMessage(self.Localizer.LauncherFinishedDownloadDb)
        # Ok, start going through the phases
        self.currentPhase = self.LauncherPhases[0]
        self.currentPhaseIndex = 1
        self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
        self.updatePhase(self.currentPhase)

    def maybeStartGame(self):
        """
        This function gets called whenever the Launcher determines it has
        finished updating everything that was previously downloaded, and
        either has hit a phase it has not completed, or is completely done.
        Here, we decide if we are in a high enough phase to start the game
        and if we are, throw the event that kicks everything off.
        Note: you will get this event multiple times, so you probably
        want to acceptOnce
        """
        if (not self.started and self.currentPhase >= self.showPhase):
            self.started = True
            self.notify.info("maybeStartGame: starting game")
            self.launcherMessage(self.Localizer.LauncherStartingGame)
            # Go into the background now since Panda will be fired up shortly
            self.background()
            # Put ourselves in the global dict
            __builtin__.launcher = self
            # Start the show
            self.startGame()

    def _runTaskManager(self):
        """ Runs the task manager main loop.  This means running the
        mini task manager initially, until we have started the main
        task manager, and then it runs the main task manager
        instead. """

        if(not self.taskMgrStarted):
            self.miniTaskMgr.run()
            self.notify.info("Switching task managers.")
        taskMgr.run()

    def _stepMiniTaskManager(self, task):
        """ This task is queued up on the main task manager to run the
        mini task manager, until it has no more tasks.  This is used
        to transition from the mini task manager to the main task
        manager. """

        self.miniTaskMgr.step()
        if self.miniTaskMgr.taskList:
            return task.cont
        self.notify.info("Stopping mini task manager.")
        self.miniTaskMgr = None
        return task.done

    def newTaskManager(self):
        """ A derived class should call this, for instance in
        startGame, as soon as the main task manager can be safely
        created. """
        self.taskMgrStarted = True
        if self.miniTaskMgr.running:
            self.miniTaskMgr.stop()

        from direct.task.TaskManagerGlobal import taskMgr
        taskMgr.remove('miniTaskManager')
        taskMgr.add(self._stepMiniTaskManager, 'miniTaskManager')

    def mainLoop(self):
        # Put the whole show in a try..except block, so we can catch Python
        # exceptions and set the appropriate error code.
        try:
            self._runTaskManager()

        except SystemExit:
            # Presumably the window has already been shut down here, but shut
            # it down again for good measure.
            if hasattr(__builtin__, "base"):
                base.destroy()

            self.notify.info("Normal exit.")
            raise

        except:
            # Some unexpected Python exception; this is error code 12 for the
            # installer.
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

    def updatePhase(self, phase):
        self.notify.info('Updating multifiles in phase: ' + `phase`)
        # Phase may need downloading, clear the percentage to 0
        self.setPercentPhaseComplete(self.currentPhase, 0)
        assert(self.dldb)
        # Make a list of the multifile indexes in this phase
        self.phaseMultifileNames = []
        numfiles = self.dldb.getServerNumMultifiles()
        for i in range(self.dldb.getServerNumMultifiles()):
            # What is this multifile's name?
            mfname = self.dldb.getServerMultifileName(i)
            # If this multifile is for this phase, then update it
            if (self.dldb.getServerMultifilePhase(mfname) == phase):
                self.phaseMultifileNames.append(mfname)
        self.updateNextMultifile()

    def updateNextMultifile(self):
        if (len(self.phaseMultifileNames) > 0):
            # Update the first multifile on the list
            self.currentMfname = self.phaseMultifileNames.pop()
            # Reset the retry counter
            self.curMultifileRetry = 0
            self.getMultifile(self.currentMfname)
        else:
            if self.currentMfname is None:
                # Print out some debug info before exiting
                self.notify.warning("no multifile found! See below for debug info:")
                for i in range(self.dldb.getServerNumMultifiles()):
                    mfname = self.dldb.getServerMultifileName(i)
                    phase = self.dldb.getServerMultifilePhase(mfname)
                    print i, mfname, phase
                # This will exit
                self.handleGenericMultifileError()

            decompressedMfname = os.path.splitext(self.currentMfname)[0]
            localFilename = Filename(self.mfDir, Filename(decompressedMfname))

            # find the next phase in the phase list
            nextIndex = self.LauncherPhases.index(self.currentPhase) + 1

            # if admin user crashes during dwnload, want to ensure the files he wrote are readable
            # by non-admins, so do this after every phase
            if nextIndex < len(self.LauncherPhases):
                self.MakeNTFSFilesGlobalWriteable(localFilename)
            else:
                # at the end do the whole directory, just to make sure
                self.MakeNTFSFilesGlobalWriteable()

            # Now that the multifile is available, mount it so we can
            # load files.
            vfs = VirtualFileSystem.getGlobalPtr()
            vfs.mount(localFilename, '.', VirtualFileSystem.MFReadOnly)

            # Phase all done, now set the percent to really be 100
            self.setPercentPhaseComplete(self.currentPhase, 100)
            # Now we are done updating all the multifiles for this phase
            self.notify.info('Done updating multifiles in phase: ' + `self.currentPhase`)
            # Also update the overall progress bar
            self.progressSoFar += int(round(self.phaseOverallMap[self.currentPhase]*100))
            self.notify.info('progress so far ' + `self.progressSoFar`)
            #self.forceSleep()
            
            # Send the phase complete event in case anybody cares
            messenger.send('phaseComplete-' + `self.currentPhase`)
            if nextIndex < len(self.LauncherPhases):
                # go to the next phase
                self.currentPhase = self.LauncherPhases[nextIndex]
                self.currentPhaseIndex = nextIndex + 1
                self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
                self.updatePhase(self.currentPhase)
            else:
                self.notify.info('ALL PHASES COMPLETE')
                self.maybeStartGame()
                messenger.send("launcherAllPhasesComplete")
                self.cleanup()

    def isDownloadComplete(self):
        return self._downloadComplete

    def updateMultifileDone(self):
        # Assuming we are always updating the first multifile on the list,
        # just pop that file off and then work on the next one
        self.updateNextMultifile()

    def downloadMultifileDone(self):
        self.getDecompressMultifile(self.currentMfname)

    def getMultifile(self, mfname):
        self.notify.info('Downloading multifile: ' + mfname)
        # If the multifile does not exist in the client db, add the new record
        if (not self.dldb.clientMultifileExists(mfname)):
            self.maybeStartGame()
            self.notify.info('Multifile does not exist in client db,' +
                              'creating new record: ' + mfname)
            # Create a new (incomplete) record on the client side
            self.dldb.addClientMultifile(mfname)

            curHash = self.dldb.getServerMultifileHash(mfname)
            self.dldb.setClientMultifileHash(mfname, curHash)

            localFilename = Filename(self.mfDir, Filename(mfname))
            if localFilename.exists():
                curSize = localFilename.getFileSize()
                self.dldb.setClientMultifileSize(mfname, curSize)
                if curSize == self.dldb.getServerMultifileSize(mfname):
                    self.dldb.setClientMultifileComplete(mfname)

        # Strip off the pz extension leaving file.mf
        decompressedMfname = os.path.splitext(mfname)[0]
        decompressedFilename = Filename(self.mfDir, Filename(decompressedMfname))

        if (not self.dldb.clientMultifileComplete(mfname) or \
            not self.dldb.clientMultifileDecompressed(mfname)) and \
            decompressedFilename.exists():

            # Hey, the client.ddb thinks this multifile's not
            # completely downloaded (or not completely decompressed),
            # yet the decompressed filename is here on disk.  Check
            # its contents.

            clientMd5 = HashVal()
            clientMd5.hashFile(decompressedFilename)
            clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)
            if clientVer != -1:
                # Not only is it here on disk, but it's the correct
                # version (or at least some recognized version).
                # Someone else must have downloaded it for us, swell.
                # We can move on to patching it.
                
                self.notify.info('Decompressed multifile is already on disk and correct: %s (version %s)' % (mfname, clientVer))
                self.dldb.setClientMultifileComplete(mfname)
                self.dldb.setClientMultifileDecompressed(mfname)

                compressedFilename = Filename(self.mfDir, Filename(mfname))
                compressedFilename.unlink()

                # Maybe someone's extracted the files, too.
                extractedOk = True
                numFiles = self.dldb.getServerNumFiles(mfname)
                for i in range(numFiles):
                    subfile = self.dldb.getServerFileName(mfname, i)
                    fn = Filename(self.mfDir, Filename(subfile))
                    if fn.compareTimestamps(decompressedFilename) <= 0:
                        # Oh, no good.
                        extractedOk = False
                        break

                if extractedOk:
                    self.notify.info('Multifile appears to have been extracted already.')
                    self.dldb.setClientMultifileExtracted(mfname)
                    

        # If the multifile is not complete, finish downloading it
        if (not self.dldb.clientMultifileComplete(mfname) or
            not decompressedFilename.exists()):
            self.maybeStartGame()
            currentSize = self.dldb.getClientMultifileSize(mfname)
            totalSize = self.dldb.getServerMultifileSize(mfname)
            localFilename = Filename(self.mfDir, Filename(mfname))
            if not localFilename.exists():
                currentSize = 0
            else:
                currentSize = min(currentSize, localFilename.getFileSize())                

            if (currentSize == 0):
                self.notify.info('Multifile has not been started, ' +
                                  'downloading new file: ' + mfname)
                # Record what version (hashval) we are working on for
                # future reference. This way if we are interrupted, we know
                # which file we were on when we restart
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)

                #set the new multifile download flag
                self.phaseNewDownload[self.currentPhase] = 1
                # Download the file
                self.downloadMultifile(self.contentDir + mfname, localFilename,
                                       mfname,
                                       self.downloadMultifileDone,
                                       totalSize, 0, self.downloadMultifileWriteToDisk)
            else:
                # See what version we are working on
                clientHash = self.dldb.getClientMultifileHash(mfname)
                # See what the latest version is from the server
                serverHash = self.dldb.getServerMultifileHash(mfname)

                # If we are still working on the latest version, pick up
                # right where we left off
                if (clientHash.eq(serverHash)):
                    self.notify.info('Multifile is not complete, finishing download for %s, size = %s / %s' % (mfname, currentSize, totalSize))
                    # Resume downloading the file
                    self.downloadMultifile(self.contentDir + mfname, localFilename,
                                           mfname,
                                           self.downloadMultifileDone,
                                           totalSize, currentSize, self.downloadMultifileWriteToDisk)
                else:
                    if self.curMultifileRetry < self.multifileRetries:
                        self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                        self.curMultifileRetry += 1
                        # Start over with new version
                        self.notify.info('Multifile is not complete, and is out of date. ' +
                                         'Restarting download with newest multifile')
                        # Mark this multifile as incomplete, with 0 size
                        self.dldb.setClientMultifileIncomplete(self.currentMfname)
                        self.dldb.setClientMultifileSize(self.currentMfname, 0)
                        self.dldb.setClientMultifileHash(self.currentMfname, serverHash)
                        
                        # Ok, now try getting the file
                        self.getMultifile(self.currentMfname)
                    else:
                        self.setPandaErrorCode(6)
                        self.notify.info('getMultifile: Failed to download multifile')
                        sys.exit()
        else:
            self.notify.info('Multifile already complete: ' + mfname)
            # lets show a percentage here of how much we have downloaded
            #self.tempPhaseProgress = self.getProgressSum(mfname)
            #self.progressSoFar += self.tempPhaseProgress
            self.downloadMultifileDone()

    def updateMultifileDone(self):
        # Assuming we are always updating the first multifile on the list,
        # just pop that file off and then work on the next one
        self.updateNextMultifile()

    def downloadMultifileDone(self):
        self.getDecompressMultifile(self.currentMfname)

    def getMultifile(self, mfname):
        self.notify.info('Downloading multifile: ' + mfname)
        # If the multifile does not exist in the client db, add the new record
        if (not self.dldb.clientMultifileExists(mfname)):
            self.maybeStartGame()
            self.notify.info('Multifile does not exist in client db,' +
                              'creating new record: ' + mfname)
            # Create a new (incomplete) record on the client side
            self.dldb.addClientMultifile(mfname)

            if self.DecompressMultifiles:
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)

                localFilename = Filename(self.mfDir, Filename(mfname))
                if localFilename.exists():
                    curSize = localFilename.getFileSize()
                    self.dldb.setClientMultifileSize(mfname, curSize)
                    if curSize == self.dldb.getServerMultifileSize(mfname):
                        self.dldb.setClientMultifileComplete(mfname)

        # Strip off the pz extension leaving file.mf
        decompressedMfname = os.path.splitext(mfname)[0]
        decompressedFilename = Filename(self.mfDir, Filename(decompressedMfname))

        if self.DecompressMultifiles:
            if (not self.dldb.clientMultifileComplete(mfname) or \
                not self.dldb.clientMultifileDecompressed(mfname)) and \
                decompressedFilename.exists():

                # Hey, the client.ddb thinks this multifile's not
                # completely downloaded (or not completely decompressed),
                # yet the decompressed filename is here on disk.  Check
                # its contents.

                clientMd5 = HashVal()
                clientMd5.hashFile(decompressedFilename)
                clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)
                if clientVer != -1:
                    # Not only is it here on disk, but it's the correct
                    # version (or at least some recognized version).
                    # Someone else must have downloaded it for us, swell.
                    # We can move on to patching it.

                    self.notify.info('Decompressed multifile is already on disk and correct: %s (version %s)' % (mfname, clientVer))
                    self.dldb.setClientMultifileComplete(mfname)
                    self.dldb.setClientMultifileDecompressed(mfname)

                    compressedFilename = Filename(self.mfDir, Filename(mfname))
                    compressedFilename.unlink()

                    # Maybe someone's extracted the files, too.
                    extractedOk = True
                    numFiles = self.dldb.getServerNumFiles(mfname)
                    for i in range(numFiles):
                        subfile = self.dldb.getServerFileName(mfname, i)
                        fn = Filename(self.mfDir, Filename(subfile))
                        if fn.compareTimestamps(decompressedFilename) <= 0:
                            # Oh, no good.
                            extractedOk = False
                            break

                    if extractedOk:
                        self.notify.info('Multifile appears to have been extracted already.')
                        self.dldb.setClientMultifileExtracted(mfname)
                    

        # If the multifile is not complete, finish downloading it
        if (not self.dldb.clientMultifileComplete(mfname) or
            not decompressedFilename.exists()):
            self.maybeStartGame()
            currentSize = self.dldb.getClientMultifileSize(mfname)
            totalSize = self.dldb.getServerMultifileSize(mfname)
            localFilename = Filename(self.mfDir, Filename(mfname))
            if not localFilename.exists():
                currentSize = 0

            if (currentSize == 0):
                self.notify.info('Multifile has not been started, ' +
                                  'downloading new file: ' + mfname)
                # Record what version (hashval) we are working on for
                # future reference. This way if we are interrupted, we know
                # which file we were on when we restart
                curHash = self.dldb.getServerMultifileHash(mfname)
                self.dldb.setClientMultifileHash(mfname, curHash)

                #set the new multifile download flag
                self.phaseNewDownload[self.currentPhase] = 1
                # Download the file
                self.downloadMultifile(self.contentDir + mfname, localFilename,
                                       mfname,
                                       self.downloadMultifileDone,
                                       totalSize, 0, self.downloadMultifileWriteToDisk)
            else:
                # See what version we are working on
                clientHash = self.dldb.getClientMultifileHash(mfname)
                # See what the latest version is from the server
                serverHash = self.dldb.getServerMultifileHash(mfname)

                # If we are still working on the latest version, pick up
                # right where we left off
                if (clientHash.eq(serverHash)):
                    self.notify.info('Multifile is not complete, finishing download for %s, size = %s / %s' % (mfname, currentSize, totalSize))
                    # Resume downloading the file
                    self.downloadMultifile(self.contentDir + mfname, localFilename,
                                           mfname,
                                           self.downloadMultifileDone,
                                           totalSize, currentSize, self.downloadMultifileWriteToDisk)
                else:
                    if self.curMultifileRetry < self.multifileRetries:
                        self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                        self.curMultifileRetry += 1
                        # Start over with new version
                        self.notify.info('Multifile is not complete, and is out of date. ' +
                                         'Restarting download with newest multifile')
                        # Mark this multifile as incomplete, with 0 size
                        self.dldb.setClientMultifileIncomplete(self.currentMfname)
                        self.dldb.setClientMultifileSize(self.currentMfname, 0)
                        if self.DecompressMultifiles:
                            self.dldb.setClientMultifileHash(self.currentMfname, serverHash)
                        
                        # Ok, now try getting the file
                        self.getMultifile(self.currentMfname)
                    else:
                        self.setPandaErrorCode(6)
                        self.notify.info('getMultifile: Failed to download multifile')
                        sys.exit()
        else:
            self.notify.info('Multifile already complete: ' + mfname)
            # lets show a percentage here of how much we have downloaded
            #self.tempPhaseProgress = self.getProgressSum(mfname)
            #self.progressSoFar += self.tempPhaseProgress
            self.downloadMultifileDone()

    def getDecompressMultifile(self, mfname):
        if not self.DecompressMultifiles:
            self.decompressMultifileDone()
        else:
            # If the multifile is not decompressed, decompress it
            if (not self.dldb.clientMultifileDecompressed(mfname)):
                self.maybeStartGame()
                # Decompress the file, then record that it is complete
                self.notify.info('decompressMultifile: Decompressing multifile: ' + mfname)
                localFilename = Filename(self.mfDir, Filename(mfname))
                self.decompressMultifile(mfname, localFilename,
                                         self.decompressMultifileDone)
            else:
                self.notify.info('decompressMultifile: Multifile already decompressed: '
                                  + mfname)
                self.decompressMultifileDone()

    def decompressMultifileDone(self):
        # Ok, set the progress higher now
        if (self.phaseNewDownload[self.currentPhase]):
            self.setPercentPhaseComplete(self.currentPhase, 95)
        self.extractMultifile(self.currentMfname)

    def extractMultifile(self, mfname):
        # If the multifile is not extracted, extract it
        if (not self.dldb.clientMultifileExtracted(mfname)):
            self.maybeStartGame()
            # Extract the file, then record that it is complete
            self.notify.info('extractMultifile: Extracting multifile: ' + mfname)
            # Strip off the pz extension leaving file.mf
            decompressedMfname = os.path.splitext(mfname)[0]
            localFilename = Filename(self.mfDir, Filename(decompressedMfname))
            destDir = Filename(self.topDir)
            # The extractor extracts to the directory we pass in, so
            # set the current directory to where we want these files
            # to go, right now they are all relative to the top
            # directory
            self.notify.info('extractMultifile: Extracting: '
                              + localFilename.cStr() + ' to: ' + destDir.cStr())
            self.extract(mfname, localFilename, destDir, self.extractMultifileDone)
        else:
            self.notify.info('extractMultifile: Multifile already extracted: ' + mfname)
            self.extractMultifileDone()

    def extractMultifileDone(self):
        # Ok, set the progress higher now only if it was whole multifile download
        if (self.phaseNewDownload[self.currentPhase]):
            self.setPercentPhaseComplete(self.currentPhase, 99)
        # If we got all the way here, the file is done
        self.notify.info('extractMultifileDone: Finished updating multifile: '
                          + self.currentMfname)
        self.patchMultifile()

    def getPatchFilename(self, fname, currentVersion):
        # Return a filename that will represent the patch file name on
        # the download server from (currentVersion) to (currentVersion+1)
        # Example:
        # fname = foo.rgb.v1
        # patch = foo.rgb.v1.pch
        return (fname + '.v' + `currentVersion` + '.' + self.patchExtension)

    #============================================================
    #  Patching functions
    #============================================================

    def downloadPatches(self):
        if (len(self.patchList) > 0):
            self.currentPatch, self.currentPatchee, self.currentPatchVersion = self.patchList.pop()

            # Patches are compressed
            self.notify.info(self.contentDir)
            self.notify.info(self.currentPatch)

            patchFile = self.currentPatch + '.pz'
            serverPatchFilePath = self.contentDir + patchFile

            self.notify.info(serverPatchFilePath)
            localPatchFilename = Filename(self.patchDir, Filename(patchFile))
            if (self.currentPhase > 3):
                self.download(serverPatchFilePath,
                              localPatchFilename,
                              self.downloadPatchDone,
                              self.downloadPatchSimpleProgress)
            else:
                self.download(serverPatchFilePath,
                              localPatchFilename,
                              self.downloadPatchDone,
                              self.downloadPatchOverallProgress)
        else:
            # Now we are done applying all patches for this multifile
            self.notify.info('applyNextPatch: Done patching multifile: '
                              + `self.currentPhase`)
            # Ok, we are done patching. Lets run through the patchAndHash step
            # again to make sure we are all clean. If it decides we are, it will
            # move on to the next multifile
            self.patchDone()


    def downloadPatchDone(self):
        # record how much you have downloaded; this is harmless if no patch needed
        self.patchDownloadSoFar += self.httpChannel.getBytesDownloaded()
        # Decompress the patch file (perhaps this should be async? these are small files)
        self.notify.info('downloadPatchDone: Decompressing patch file: '
                          + self.currentPatch + '.pz')
        self.decompressFile(Filename(self.patchDir, Filename(self.currentPatch + '.pz')),
                            self.decompressPatchDone)

    def decompressPatchDone(self):
        self.notify.info('decompressPatchDone: Patching file: ' + self.currentPatchee
                         + ' from ver: ' + `self.currentPatchVersion`)
        # Determine the filenames
        patchFile = Filename(self.patchDir, Filename(self.currentPatch))
        patchFile.setBinary()
        patchee = Filename(self.mfDir, Filename(self.currentPatchee))
        patchee.setBinary()
        # Run the patcher async
        self.patch(patchFile, patchee, self.downloadPatches)

    def patchDone(self):
        # Ok, the patch worked
        self.notify.info('patchDone: Patch successful')
        # Cleanup
        del self.currentPatch
        del self.currentPatchee
        del self.currentPatchVersion
        # TODO: only extract the files that changed.
        # For now just extract them all
        # (at least we do not need to patch and hash if we extract)
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        localFilename = Filename(self.mfDir, Filename(decompressedMfname))
        destDir = Filename(self.topDir)
        self.extract(self.currentMfname, localFilename, destDir, self.updateMultifileDone)

    def startReextractingFiles(self):
        # See if there are any files to patch
        self.notify.info('startReextractingFiles: Reextracting ' + `len(self.reextractList)`
                         + ' files for multifile: ' + self.currentMfname)
        self.launcherMessage(self.Localizer.LauncherRecoverFiles)
        # read in the multifile
        self.currentMfile = Multifile()
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        self.currentMfile.openRead(Filename(self.mfDir, Filename(decompressedMfname)))
        self.reextractNextFile()

    def reextractNextFile(self):
        failure = 0
        while (not failure and len(self.reextractList) > 0):
            currentReextractFile = self.reextractList.pop()
            subfileIndex = self.currentMfile.findSubfile(currentReextractFile)
            if subfileIndex >= 0:
                destFilename = Filename(self.topDir, Filename(currentReextractFile))
                result = self.currentMfile.extractSubfile(subfileIndex, destFilename)
                if not result:
                    self.notify.warning('reextractNextFile: Failure on reextract.')
                    failure = 1
            else:
                self.notify.warning('reextractNextFile: File not found in multifile: '
                                    + `currentReextractFile`)
                failure = 1

        if failure:
            # TODO: handle this better
            sys.exit()

        # Now we are done extracting files for this multifile
        self.notify.info('reextractNextFile: Done reextracting files for multifile: '
                         + `self.currentPhase`)
        # Ok, now move on to the next multifile
        del self.currentMfile
        self.updateMultifileDone()

    def patchMultifile(self):
        self.launcherMessage(self.Localizer.LauncherCheckUpdates %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total": self.numPhases,})
        self.notify.info("patchMultifile: Checking for patches on multifile: "
                         + self.currentMfname)

        self.patchList = []

        # Compute the hash
        clientMd5 = HashVal()
        decompressedMfname = os.path.splitext(self.currentMfname)[0]
        localFilename = Filename(self.mfDir, Filename(decompressedMfname))
        clientMd5.hashFile(localFilename)
        clientVer = self.dldb.getVersion(Filename(decompressedMfname), clientMd5)

        # Check the hash results
        if (clientVer == 1):
            # On to the next file, leave the clean flag in the state it is in
            self.patchAndHash()
            return

        elif (clientVer == -1):
            # Invalid hash value, file must be corrupted or simply out of date
            self.notify.info('patchMultifile: Invalid hash for file: ' + self.currentMfname)
            self.maybeStartGame()
            if self.curMultifileRetry < self.multifileRetries:
                self.notify.info('recover attempt: %s / %s' % (self.curMultifileRetry, self.multifileRetries))
                self.curMultifileRetry += 1
                # Start over with new version
                self.notify.info('patchMultifile: Restarting download with newest multifile')
                # Mark this multifile as incomplete, with 0 size
                self.dldb.setClientMultifileIncomplete(self.currentMfname)
                self.dldb.setClientMultifileSize(self.currentMfname, 0)
                # Ok, now try getting the newest file
                self.getMultifile(self.currentMfname)
            else:
                self.setPandaErrorCode(6)
                self.notify.info('patchMultifile: Failed to download multifile')
                sys.exit()
            return

        elif (clientVer > 1):
            self.notify.info('patchMultifile: Old version for multifile: ' +
                             self.currentMfname + ' Client ver: ' + `clientVer`)
            self.maybeStartGame()
            self.totalPatchDownload = 0
            self.patchDownloadSoFar = 0
            for ver in range(1, clientVer):
                patch = self.getPatchFilename(decompressedMfname, ver+1)
                patchee = decompressedMfname
                patchVersion = ver+1
                self.patchList.append((patch, patchee, patchVersion))
                # sum the file size to totalPatchDownload (phase_3 only)
                if (self.currentPhase == 3):
                    self.totalPatchDownload += self.getProgressSum(patch)
            self.notify.info('total patch to be downloaded = ' + `self.totalPatchDownload`)
            self.downloadPatches()
            return

    def patchAndHash(self):
        # Reset the patch and reextract lists
        self.reextractList = []
        # Keep track to see if all the files are clean.
        # Assume they are clean to begin with, and prove me wrong
        self.PAHClean = 1
        self.PAHNumFiles = self.dldb.getServerNumFiles(self.currentMfname)
        self.PAHFileCounter = 0
        if (self.PAHNumFiles > 0):
            task = MiniTask(self.patchAndHashTask)
            task.cleanCallback = self.updateMultifileDone
            task.uncleanCallback = self.startReextractingFiles
            self.miniTaskMgr.add(task, "patchAndHash")
        else:
            self.updateMultifileDone()

    def patchAndHashTask(self, task):
        self.launcherMessage(self.Localizer.LauncherVerifyPhase)
        #self.launcherMessage(self.Localizer.LauncherVerifyPhase %
        #                     (self.currentPhase,
        #                      int(round(self.PAHFileCounter/float(self.PAHNumFiles)*100.0))))
        # See if we are at the end of the list
        if (self.PAHFileCounter == self.PAHNumFiles):
            # If we are return task done
            if self.PAHClean:
                # Everything proceeded as expected. This multifile is DONE!
                task.cleanCallback()
            else:
                # Some files need to be updated
                task.uncleanCallback()
            # Now we are really done with this task
            return task.done
        else:
            # Otherwise increase the counter and do the next file
            i = self.PAHFileCounter
            # Increment for next time
            self.PAHFileCounter += 1

        fname = self.dldb.getServerFileName(self.currentMfname, i)
        fnameFilename = Filename(self.topDir, Filename(fname))

        # See if the file exists, if not, add it to the reextractList and return
        if (not os.path.exists(fnameFilename.toOsSpecific())):
            self.notify.info('patchAndHash: File not found: ' + fname)
            # reextract the file
            self.reextractList.append(fname)
            self.PAHClean = 0
            return task.cont

        if self.VerifyFiles and self.dldb.hasVersion(Filename(fname)):
            # If we recorded versioning information on this file, look
            # it up and see if it matches the expected version.

            # Compute the hash
            clientMd5 = HashVal()
            clientMd5.hashFile(fnameFilename)
            clientVer = self.dldb.getVersion(Filename(fname), clientMd5)

            if (clientVer == 1):
                # On to the next file, leave the clean flag in the state it is in
                return task.cont
            else:
                # Invalid hash value, file must be corrupted or simply out of date
                self.notify.info('patchAndHash: Invalid hash for file: ' + fname)
                # reextract the file
                self.reextractList.append(fname)
                self.PAHClean = 0

        return task.cont

    def launcherMessage(self, msg):
        """
        Display a message on the flash movie
        """
        if msg != self.lastLauncherMsg:
            self.lastLauncherMsg = msg
            self.notify.info(msg)

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

    def getInstallDir(self):
        return self.topDir.cStr()

    def setPandaWindowOpen(self):
        """
        Call this when the window is finally opened so
        flash knows it can exit
        """
        self.setValue(self.PandaWindowOpenKey, 1)

    def setPandaErrorCode(self, code):
        """
        Set the exit code of panda. 0 means everything ok
        """
        self.notify.info("setting panda error code to %s" % (code))
        self.pandaErrorCode = code
        # Note that opening mode 'w' truncates the existing file, which is what we want.
        errorLog = open(self.errorfile, 'w')
        errorLog.write(str(code)+'\n')
        errorLog.flush() # Just to be sure
        errorLog.close()

    def getPandaErrorCode(self):
        return self.pandaErrorCode

    def setDisconnectDetailsNormal(self):
        self.notify.info("Setting Disconnect Details normal")
        self.disconnectCode = 0
        self.disconnectMsg = 'normal'
        
    def setDisconnectDetails(self, newCode, newMsg):
        self.notify.info("New Disconnect Details: %s - %s " % (newCode,newMsg))
        self.disconnectCode = newCode
        self.disconnectMsg = newMsg
        
    def setServerVersion(self, version):
        """
        Set the server version.
        """
        self.ServerVersion = version
        
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

    def getPhaseComplete(self, phase):
        assert(self.phaseComplete.has_key(phase))
        percentDone = self.phaseComplete[phase]
        return (percentDone == 100)

    def setPercentPhaseComplete(self, phase, percent):
        self.notify.info("phase updating %s, %s"%(phase,percent))
        # Set the value locally in our map
        oldPercent = self.phaseComplete[phase]
        # Only udpate things if the percentage has changed
        if (oldPercent != percent):
            self.phaseComplete[phase] = percent
            # Update the download watcher
            messenger.send("launcherPercentPhaseComplete",
                           [phase, percent, self.getBandwidth(), self.byteRate])
            # Also set the value in the registry
            percentPhaseCompleteKey = "PERCENT_PHASE_COMPLETE_" + `phase`
            self.setRegistry(percentPhaseCompleteKey, percent)

            # now calculate an overall percenatage
            # rescale this percent according to weight of this phase
            self.overallComplete = int(round(percent * self.phaseOverallMap[phase])) + self.progressSoFar
            #self.notify.info('overall complete ' + `self.overallComplete` + '%')
            # also set the value in the registry
            self.setRegistry("PERCENT_OVERALL_COMPLETE", self.overallComplete)

    def getPercentPhaseComplete(self, phase):
        # Return the percent [0-100] complete of this phase
        return self.phaseComplete[phase]

        dr = finalRequested - startRequested

        if (dt <= 0.0):
            assert self.notify.debug('getBytesPerSecond: negative dt')
            return -1

        self.byteRate = db / dt
        self.byteRateRequested = dr / dt
        assert self.notify.debug("getBytesPerSecond: db = %s, dr = %s, dt = %s byte rate = %s" %
                                 (db, dr, dt, self.byteRate))
        return self.byteRate

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

        # Actually, here in the lame-duck LauncherBase code, we don't
        # bother to fully implement this method.  Instead, we simply
        # either make the callback immediately, or we hang on a hook
        # on the phaseComplete event to call it then.  This means that
        # that the callback is always made in the made thread, rather
        # than a sub-thread.  It also means that the phaseComplete
        # event is sent *before* the callback is made, rather than
        # after; but because the callback is made in the main thread,
        # we won't be off by more than a frame, and this is all that
        # Pirates requires anyway.  (And Toontown doesn't currently
        # use this method at all.)  Eventually, when this code is
        # phased out altogether, it won't even matter any more.

        if self.getPhaseComplete(phase):
            # Already downloaded.
            func()
            return

        self.acceptOnce('phaseComplete-%s' % (phase), func)

    def testBandwidth(self):
        # Any time we test, go ahead and record the current bandwidth
        self.recordBytesPerSecond()
        # Judging by the current byte rate, determine if we need to increase
        # or decrease the download byte rate request
        byteRate = self.getBytesPerSecond()
        if (byteRate < 0):
            assert self.notify.debug('testBandwidth: not enough data yet')
            return
        assert self.notify.debug('testBandwidth: comparing byteRate %s with getBandwidth %s and byteRateRequested %s.' %
                                 (byteRate, self.getBandwidth(), self.byteRateRequested))

        if (byteRate >= self.getBandwidth() * self.INCREASE_THRESHOLD):
            # If we are nearly meeting the ideal bandwidth we are
            # requesting, then let's try increasing the requested
            # amount.
            self.increaseBandwidth(byteRate)

        elif (byteRate < (self.byteRateRequested * self.DECREASE_THRESHOLD)):
            # If we are not meeting the actual requested amount, let's
            # back off.  The semantic difference between ideal
            # requested bandwidth and actual requested bandwidth is
            # subtle and has to do with what other things the CPU is
            # busy with and the size of the downloaded files.
            self.decreaseBandwidth(byteRate)

    def getBandwidth(self):
        # What is the bandwidth Python thinks it is running at?
        # Of course, if nobody has set it, this may not be the one
        # the httpChannel is using
        if self.backgrounded:
            # If we are running in the background, we need to subtract
            # out the telemetry bandwidth
            bandwidth = (self.BANDWIDTH_ARRAY[self.bandwidthIndex] -
                         self.TELEMETRY_BANDWIDTH)
        else:
            # If we are running in the foreground, we have the entire channel
            bandwidth = (self.BANDWIDTH_ARRAY[self.bandwidthIndex])
        if self.MAX_BANDWIDTH > 0:
            bandwidth = min(bandwidth, self.MAX_BANDWIDTH)

        return bandwidth

    def increaseBandwidth(self, targetBandwidth = None):
        # Change the download byte rate to a higher level in the
        # BANDWIDTH_ARRAY, unless we are already at the highest level
        maxBandwidthIndex = (len(self.BANDWIDTH_ARRAY) - 1)
        if (self.bandwidthIndex == maxBandwidthIndex):
            self.notify.debug('increaseBandwidth: Already at maximum bandwidth')
            return 0

        # Only go one step at a time when increasing bandwidth, even
        # if we have a long way to go.
        self.bandwidthIndex += 1
        assert self.notify.debug('increaseBandwidth: Increasing bandwidth to: '
                                 + `self.getBandwidth()`)
        self.everIncreasedBandwidth = 1
        self.setBandwidth()
        return 1

    def decreaseBandwidth(self, targetBandwidth = None):
        # Check the flag to see if we should do this at all
        if not self.DECREASE_BANDWIDTH:
            return 0

        # Once we have started running the game, we can't fully trust
        # the live bandwidth measurement (because the throughput also
        # depends on CPU availability).  Thus, a client running on an
        # overloaded CPU may observe artificially poor bandwidths.  If
        # we were to take that at face value, we would completely
        # starve the download as we continually drop the available
        # bandwidth estimate downwards.

        # To avoid this problem, we do not decrease the bandwidth any
        # more once we have been backgrounded--we only allow the
        # bandwidth estimate to increase.  However, it is possible
        # that we did not download any content before we were
        # backgrounded, which means we don't have a reliable starting
        # bandwidth estimate; in this case, we will still need to
        # decrease the bandwidth estimate downwards until we find the
        # best starting point; we use the everIncreasedBandwidth flag
        # to indicate whether we have found this point yet or not.
        if self.backgrounded and self.everIncreasedBandwidth:
            assert self.notify.debug('decreaseBandwidth: Running in background, not reducing bandwidth.')
            return 0

        # Change the download byte rate to the next lowest level in the
        # BANDWIDTH_ARRAY, unless we are already at the lowest level
        if (self.bandwidthIndex == 0):
            assert self.notify.debug('decreaseBandwidth: Already at minimum bandwidth')
            return 0
        else:
            self.bandwidthIndex -= 1

            if targetBandwidth:
                # Jump many steps on decreasing bandwidth until we find
                # the closest to our target.
                while self.bandwidthIndex > 0 and \
                      self.BANDWIDTH_ARRAY[self.bandwidthIndex] > targetBandwidth:
                    self.bandwidthIndex -= 1

            assert self.notify.debug('decreaseBandwidth: Decreasing bandwidth to: '
                                     + `self.getBandwidth()`)
            self.setBandwidth()
            return 1

    def setBandwidth(self):
        # Reset the stats or else we will be counting bytes per second
        # with the previous bandwidth
        self.resetBytesPerSecond()
        # Make the current bandwidth effective to the HTTP channel
        self.httpChannel.setMaxBytesPerSecond(self.getBandwidth())

    #============================================================
    # Functions for controlling the bandwidth
    #============================================================

    def resetBytesPerSecond(self):
        self.bpsList = []

    def recordBytesPerSecond(self):
        bytesDownloaded = self.httpChannel.getBytesDownloaded()
        bytesRequested = self.httpChannel.getBytesRequested()
        t = self.getTime()
        self.bpsList.append((t, bytesDownloaded, bytesRequested))
        # Keep the list within the window
        while 1:
            if (len(self.bpsList) == 0):
                break
            ft, fb, fr = self.bpsList[0]
            # If this time is older than the current time - the window
            # get it out of the list
            if (ft < (t - self.BPS_WINDOW)):
                self.bpsList.pop(0)
            else:
                # Get out of the while loop
                break

    def getBytesPerSecond(self):
        # You need at least two data points to determine the byteRate
        # If the list is not primed enough, return -1
        # Do not report until you have enough stats to go off of
        if (len(self.bpsList) < 2):
            assert self.notify.debug('getBytesPerSecond: bpsList not enough elements: %s' % self.bpsList)
            return -1
        startTime, startBytes, startRequested = self.bpsList[0]
        finalTime, finalBytes, finalRequested = self.bpsList[-1]
        dt = finalTime - startTime
        db = finalBytes - startBytes
        dr = finalRequested - startRequested

        if (dt <= 0.0):
            assert self.notify.debug('getBytesPerSecond: negative dt')
            return -1

        self.byteRate = db / dt
        self.byteRateRequested = dr / dt
        assert self.notify.debug("getBytesPerSecond: db = %s, dr = %s, dt = %s byte rate = %s" %
                                 (db, dr, dt, self.byteRate))
        return self.byteRate

    def testBandwidth(self):
        # Any time we test, go ahead and record the current bandwidth
        self.recordBytesPerSecond()
        # Judging by the current byte rate, determine if we need to increase
        # or decrease the download byte rate request
        byteRate = self.getBytesPerSecond()
        if (byteRate < 0):
            assert self.notify.debug('testBandwidth: not enough data yet')
            return
        assert self.notify.debug('testBandwidth: comparing byteRate %s with getBandwidth %s and byteRateRequested %s.' %
                                 (byteRate, self.getBandwidth(), self.byteRateRequested))

        if (byteRate >= self.getBandwidth() * self.INCREASE_THRESHOLD):
            # If we are nearly meeting the ideal bandwidth we are
            # requesting, then let's try increasing the requested
            # amount.
            self.increaseBandwidth(byteRate)

        elif (byteRate < (self.byteRateRequested * self.DECREASE_THRESHOLD)):
            # If we are not meeting the actual requested amount, let's
            # back off.  The semantic difference between ideal
            # requested bandwidth and actual requested bandwidth is
            # subtle and has to do with what other things the CPU is
            # busy with and the size of the downloaded files.
            self.decreaseBandwidth(byteRate)

    def getBandwidth(self):
        # What is the bandwidth Python thinks it is running at?
        # Of course, if nobody has set it, this may not be the one
        # the httpChannel is using
        if self.backgrounded:
            # If we are running in the background, we need to subtract
            # out the telemetry bandwidth
            bandwidth = (self.BANDWIDTH_ARRAY[self.bandwidthIndex] -
                         self.TELEMETRY_BANDWIDTH)
        else:
            # If we are running in the foreground, we have the entire channel
            bandwidth = (self.BANDWIDTH_ARRAY[self.bandwidthIndex])
        if self.MAX_BANDWIDTH > 0:
            bandwidth = min(bandwidth, self.MAX_BANDWIDTH)

        return bandwidth

    def increaseBandwidth(self, targetBandwidth = None):
        # Change the download byte rate to a higher level in the
        # BANDWIDTH_ARRAY, unless we are already at the highest level
        maxBandwidthIndex = (len(self.BANDWIDTH_ARRAY) - 1)
        if (self.bandwidthIndex == maxBandwidthIndex):
            assert self.notify.debug('increaseBandwidth: Already at maximum bandwidth')
            return 0

        # Only go one step at a time when increasing bandwidth, even
        # if we have a long way to go.
        self.bandwidthIndex += 1
        assert self.notify.debug('increaseBandwidth: Increasing bandwidth to: '
                                 + `self.getBandwidth()`)
        self.everIncreasedBandwidth = 1
        self.setBandwidth()
        return 1

    def decreaseBandwidth(self, targetBandwidth = None):
        # Check the flag to see if we should do this at all
        if not self.DECREASE_BANDWIDTH:
            return 0

        # Once we have started running the game, we can't fully trust
        # the live bandwidth measurement (because the throughput also
        # depends on CPU availability).  Thus, a client running on an
        # overloaded CPU may observe artificially poor bandwidths.  If
        # we were to take that at face value, we would completely
        # starve the download as we continually drop the available
        # bandwidth estimate downwards.

        # To avoid this problem, we do not decrease the bandwidth any
        # more once we have been backgrounded--we only allow the
        # bandwidth estimate to increase.  However, it is possible
        # that we did not download any content before we were
        # backgrounded, which means we don't have a reliable starting
        # bandwidth estimate; in this case, we will still need to
        # decrease the bandwidth estimate downwards until we find the
        # best starting point; we use the everIncreasedBandwidth flag
        # to indicate whether we have found this point yet or not.
        if self.backgrounded and self.everIncreasedBandwidth:
            assert self.notify.debug('decreaseBandwidth: Running in background, not reducing bandwidth.')
            return 0

        # Change the download byte rate to the next lowest level in the
        # BANDWIDTH_ARRAY, unless we are already at the lowest level
        if (self.bandwidthIndex == 0):
            assert self.notify.debug('decreaseBandwidth: Already at minimum bandwidth')
            return 0
        else:
            self.bandwidthIndex -= 1

            if targetBandwidth:
                # Jump many steps on decreasing bandwidth until we find
                # the closest to our target.
                while self.bandwidthIndex > 0 and \
                      self.BANDWIDTH_ARRAY[self.bandwidthIndex] > targetBandwidth:
                    self.bandwidthIndex -= 1

            assert self.notify.debug('decreaseBandwidth: Decreasing bandwidth to: '
                                     + `self.getBandwidth()`)
            self.setBandwidth()
            return 1

    def setBandwidth(self):
        # Reset the stats or else we will be counting bytes per second
        # with the previous bandwidth
        self.resetBytesPerSecond()
        # Make the current bandwidth effective to the HTTP channel
        self.httpChannel.setMaxBytesPerSecond(self.getBandwidth())

    def MakeNTFSFilesGlobalWriteable(self, pathToSet = None ):
        if not self.WIN32:
            return
        import win32api

        if(pathToSet == None):
            pathToSet = self.getInstallDir()
        else:
            # make sure both phase_4.mf and phase_4.mf.pz are changed, if they exist
            pathToSet = pathToSet.cStr() + "*"

        DrivePath = pathToSet[0:3]   # assumes INSTALL_DIR and file paths starts with 'DRIVE:\'

        try:
            volname, volsernum, maxfilenamlen, sysflags, filesystemtype = win32api.GetVolumeInformation(DrivePath)
        except:
            return

        # if NTFS, run cacls to change the entire TT dir tree to Everyone:F
        if(self.win32con_FILE_PERSISTENT_ACLS & sysflags):
            self.notify.info('NTFS detected, making files global writeable\n')
            win32dir = win32api.GetWindowsDirectory()
            cmdLine = win32dir + "\\system32\\cacls.exe \"" + pathToSet  + "\" /T /E /C /G Everyone:F > nul"
            os.system(cmdLine)

    #============================================================
    #  Cleanup
    #============================================================

    def cleanup(self):
        self.notify.info('cleanup: cleaning up Launcher')
        self.ignoreAll()
        del self.clock
        del self.dldb
        del self.httpChannel
        del self.http

    #
    # scan for known speed hacks
    #
    def scanForHacks(self):
        if not self.WIN32:
            return
        import _winreg
        hacksInstalled = {}
        hacksRunning = {}
        hackName = [
            '!xSpeed.net',
            'A Speeder',
            'Speed Gear',
            ]

        # scan for registry entries
        #
        knownHacksRegistryKeys = {
          hackName[0]:[
            [_winreg.HKEY_LOCAL_MACHINE,'Software\\Microsoft\\Windows\\CurrentVersion\\Run\\!xSpeed'],
            [_winreg.HKEY_CURRENT_USER,'Software\\!xSpeednethy'],
            [_winreg.HKEY_CURRENT_USER,'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MenuOrder\\Start Menu\\Programs\\!xSpeednet'],
            [_winreg.HKEY_LOCAL_MACHINE,'Software\\Gentee\\Paths\\!xSpeednet'],
            [_winreg.HKEY_LOCAL_MACHINE,'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\!xSpeed.net 2.0'],
          ],
          hackName[1]:[
            [_winreg.HKEY_CURRENT_USER,'Software\\aspeeder'],
            [_winreg.HKEY_LOCAL_MACHINE,'Software\\aspeeder'],
            [_winreg.HKEY_LOCAL_MACHINE,'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\aspeeder'],
          ],
        }
        try:
            for prog in knownHacksRegistryKeys.keys():
                for key in knownHacksRegistryKeys[prog]:
                    try:
                        h = _winreg.OpenKey(key[0], key[1])
                        #print 'found %s in registry %s' % (prog,key[1])
                        hacksInstalled[prog] = 1
                        _winreg.CloseKey(h)
                        break                       # next program when any registry entry found
                    except:
                        pass
        except:
            pass

        # Fallback #1
        # scan MUICache
        # not using libpandaexpress because it doesn't allow enumeration
        #
        knownHacksMUI = {
          '!xspeednet': hackName[0],
          'aspeeder': hackName[1],
          'speed gear': hackName[2],
        }
        i = 0
        try:
            rh = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\ShellNoRoam\\MUICache')
            while 1:
                name,value,type = _winreg.EnumValue(rh, i)
                i += 1
                if type == 1:
                    val = value.lower()
                    for hackprog in knownHacksMUI:
                        if val.find(hackprog) != -1:
                            #print "found %s in MUICache:%s" % (knownHacksMUI[hackprog], val.encode('utf-8'))
                            hacksInstalled[knownHacksMUI[hackprog]] = 1
                            break
            _winreg.CloseKey(rh)
        except:
            #print "%s: stopped at %d" % (sys.exc_info()[0], i)
            pass

        # Fallback #2
        # scan for running hack processes
        #
        try:
            # process access
            import otp.launcher.procapi
        except:
            pass
        else:
            knownHacksExe = {
              '!xspeednet.exe': hackName[0],
              'aspeeder.exe': hackName[1],
              'speedgear.exe': hackName[2],
            }
            try:
                for p in procapi.getProcessList():
                    pname = p.name
                    if knownHacksExe.has_key(pname):
                        hacksRunning[knownHacksExe[pname]] = 1
            except:
                pass

        if len(hacksInstalled) > 0:
            self.notify.info('Third party programs installed:')
            for hack in hacksInstalled.keys():
                self.notify.info(hack)

        if len(hacksRunning) > 0:
            self.notify.info('Third party programs running:')
            for hack in hacksRunning.keys():
                self.notify.info(hack)
            # quit out because 3rd party program hack detected and is running
            self.setPandaErrorCode(8)
            sys.exit()

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
        # Immediately clear out the DISLToken so it will be more
        # difficult for a hacker to play with it
        self.setValue(self.DISLTokenKey, "")
        if DISLToken == "NO DISLTOKEN":
            DISLToken = None
        return DISLToken
