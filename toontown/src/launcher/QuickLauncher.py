
import sys
import os
import time
import string
import bz2
import random
# Import DIRECT files
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *

from otp.launcher.LauncherBase import LauncherBase
from toontown.toonbase import TTLocalizer

# Redirect Python output and err to the same file

class QuickLauncher(LauncherBase):
    GameName = 'Toontown'
    ArgCount = 3
    # You should already have completed phase 1 and 2 by the
    # standalone Launcher when Python is fired up.  But we check them
    # anyway.
    LauncherPhases = [1,2,3,3.5,4,5,5.5,6,7,8,9,10,11,12,13]
    TmpOverallMap = [0.01,0.01,0.23,0.15,0.12,0.17,0.08,0.07,0.05,0.05,0.017,0.011,0.010,0.012,0.010]
    ForegroundSleepTime = 0.001
    Localizer = TTLocalizer
    DecompressMultifiles = True

    # We add a ? and random number for cache busting so we never
    # pull a cached version of this file from the web.
    launcherFileDbFilename = 'patcher.ver?%s' % random.randint(1,1000000000)
    CompressionExt = 'bz2'
    PatchExt = 'pch'

    def __init__(self):        
        print "Running: ToontownQuickLauncher"
        
        # Used to pass to server for authentication
        self.toontownBlueKey = "TOONTOWN_BLUE"
        
        # Used to communicate status back to the Updating Toontown flash movie
        self.launcherMessageKey = "LAUNCHER_MESSAGE"
        # Is the flash game1 done? (int 1 or 0)
        self.game1DoneKey = "GAME1_DONE"
        # Is the flash game2 done? (int 1 or 0)
        self.game2DoneKey = "GAME2_DONE"
        # Is the in-game 3d tutorial done? (int 1 or 0)
        self.tutorialCompleteKey = "TUTORIAL_DONE"

        LauncherBase.__init__(self)
        self.useTTSpecificLogin = config.GetBool('tt-specific-login', 0)
        # Used to pass to server for authentication
        if self.useTTSpecificLogin :
            self.toontownPlayTokenKey = "LOGIN_TOKEN"            
        else:
            self.toontownPlayTokenKey = "PLAYTOKEN"
        print ("useTTSpecificLogin=%s" % self.useTTSpecificLogin)
        self.contentDir = '/'

        # HACK: to make connecting to server happy
        self.serverDbFileHash = HashVal()
        self.launcherFileDbHash = HashVal()

        # Full throttle download!
        self.DECREASE_BANDWIDTH = 0
        self.httpChannel.setDownloadThrottle(0)

        # Before you go further, let's parse the web acct parameters
        self.webAcctParams = "WEB_ACCT_PARAMS"
        self.parseWebAcctParams()
        
        # This will cause the game to start immediately
        self.showPhase = -1
        self.maybeStartGame()
        
        self.mainLoop()

    def addDownloadVersion(self, serverFilePath):
        url = URLSpec(self.downloadServer)
        origPath = url.getPath()
        if origPath[-1] == '/':
            url.setPath('%s%s' % (origPath, serverFilePath))
        else:
            url.setPath('%s/%s' % (origPath, serverFilePath))
        return url

    def downloadLauncherFileDbDone(self):
        settings = {}
        for line in self.ramfile.readlines():
            if line.find('=') >= 0:
                key, value = line.strip().split('=')
                settings[key] = value

        self.requiredInstallFiles = []
        # patcher.ver has a line that looks like below. We will parse it now.
        # REQUIRED_INSTALL_FILES=phase_2.mf:1  phase_3.mf:0  phase_4.mf:0
        if sys.platform == 'win32':
            fileList = settings['REQUIRED_INSTALL_FILES']
        elif sys.platform == 'darwin':
            fileList = settings['REQUIRED_INSTALL_FILES_OSX']
        else:
            self.notify.warning('Unknown sys.platform: %s' % sys.platform)
            fileList = settings['REQUIRED_INSTALL_FILES']

        for fileDesc in fileList.split():
            fileName, flag = fileDesc.split(':')
            # TODO: right now I'm wrongly assuming that none of the phases need to be extracted
            # Really, we should store this flag and use it to unpack after decompression
            directions = BitMask32(flag)
            extract = directions.getBit(0)
            required = directions.getBit(1)
            optionalDownload = directions.getBit(2)
            self.notify.info('fileName: %s, flag:=%s directions=%s, extract=%s required=%s optDownload=%s' %
                             (fileName, flag, directions, extract, required, optionalDownload))
            if required:
                self.requiredInstallFiles.append(fileName)
        self.notify.info('requiredInstallFiles: %s' % self.requiredInstallFiles)

        self.mfDetails = {}
        for mfName in self.requiredInstallFiles:
            currentVer = settings['FILE_%s.current' % mfName]
            details = settings['FILE_%s.%s' % (mfName, currentVer)]
            size, hash = details.split()
            self.mfDetails[mfName] = (currentVer, int(size), hash)
            self.notify.info('mfDetails[%s] = %s' % (mfName, self.mfDetails[mfName]))

        self.resumeInstall()

    def resumeMultifileDownload(self):
        curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
        localFilename = Filename(self.topDir, Filename('_%s.%s.%s' %
                                                       (self.currentMfname, curVer, self.CompressionExt)))
        serverFilename = "%s%s.%s.%s" % (self.contentDir, self.currentMfname,
                                         curVer, self.CompressionExt)
        if localFilename.exists():
            # Pick up with a partial download
            fileSize = localFilename.getFileSize()
            self.notify.info('Previous partial download exists for: %s size=%s' % (localFilename.cStr(), fileSize))
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname,
                                   self.downloadMultifileDone,
                                   0, fileSize, self.downloadMultifileWriteToDisk)
        else:
            # Start from the top
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname,
                                   self.downloadMultifileDone,
                                   0, 0, self.downloadMultifileWriteToDisk)

    def resumeInstall(self):
        for self.currentPhaseIndex in range(len(self.LauncherPhases)):
            self.currentPhase = self.LauncherPhases[self.currentPhaseIndex]
            self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]

            self.currentMfname = 'phase_%s.mf' % (self.currentPhase)
            if sys.platform == 'darwin' and (self.currentMfname == 'phase_1.mf' or self.currentMfname == 'phase_2.mf'):
                self.currentMfname = 'phase_%sOSX.mf' % (self.currentPhase)
            if self.currentMfname in self.requiredInstallFiles:
                self.requiredInstallFiles.remove(self.currentMfname)
            else:
                self.notify.warning("avoiding crash ValueError: list.remove(x): x not in list") 
            
            curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
            self.curPhaseFile = Filename(self.topDir, Filename(self.currentMfname))
            self.notify.info('working on: %s' % self.curPhaseFile)
            if self.curPhaseFile.exists():
                self.notify.info('file exists')
                fileSize = self.curPhaseFile.getFileSize()
                clientMd5 = HashVal()
                clientMd5.hashFile(self.curPhaseFile)
                self.notify.info('clientMd5: %s expectedMd5: %s' % (clientMd5, expectedMd5))
                self.notify.info('clientSize: %s expectedSize: %s' % (fileSize, expectedSize))
                if (fileSize == expectedSize) and (clientMd5.asHex() == expectedMd5):
                    self.notify.info('file is up to date')
                    self.finalizePhase()
                    continue
                else:
                    self.notify.info('file is not valid')
                    self.resumeMultifileDownload()
                    return
            else:
                self.notify.info('file does not exist - start download')
                self.resumeMultifileDownload()
                return

        if not self.requiredInstallFiles:
            self.notify.info('ALL PHASES COMPLETE')
            messenger.send("launcherAllPhasesComplete")
            self.cleanup()            
            return

        raise StandardError, 'Some phases not listed in LauncherPhases: %s' % (self.requiredInstallFiles)

    def getDecompressMultifile(self, mfname):
        if not self.DecompressMultifiles:
            self.decompressMultifileDone()
        else:
            # If the multifile is not decompressed, decompress it
            if 1:
                # Decompress the file, then record that it is complete
                self.notify.info('decompressMultifile: Decompressing multifile: ' + mfname)
                curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
                localFilename = Filename(self.topDir, Filename('_%s.%s.%s' % (mfname, curVer, self.CompressionExt)))
                self.decompressMultifile(mfname, localFilename, self.decompressMultifileDone)
            else:
                self.notify.info('decompressMultifile: Multifile already decompressed: %s' % mfname)
                self.decompressMultifileDone()

    def decompressMultifile(self, mfname, localFilename, callback):
        self.notify.info('decompressMultifile: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile %
                             {"name": self.currentPhaseName,
                              "current": self.currentPhaseIndex,
                              "total":   self.numPhases,})
        task = Task(self.decompressMultifileTask)
        task.mfname = mfname
        task.mfFilename = Filename(self.topDir, Filename('_' + task.mfname))
        task.mfFile = open(task.mfFilename.toOsSpecific(), 'wb')
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = bz2.BZ2File(localFilename.toOsSpecific(), 'rb')
        taskMgr.add(task, 'launcher-decompressMultifile')

    def decompressMultifileTask(self, task):
        data = task.decompressor.read(8192)
        if data:
            task.mfFile.write(data)
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                # Time to make an update.
                task.lastUpdate = now
                curSize = task.mfFilename.getFileSize()
                curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
                progress = curSize / float(expectedSize)
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
            return Task.cont
        else:
            task.mfFile.close()
            task.decompressor.close()
            # Delete the bz2 file
            unlinked = task.localFilename.unlink()
            if not unlinked:
                self.notify.warning('unlink failed on file: %s' % task.localFilename.cStr())

            # Move the temp file over top the real one to finalize the extraction.
            realMf = Filename(self.topDir, Filename(self.currentMfname))
            renamed = task.mfFilename.renameTo(realMf)
            if not renamed:
                self.notify.warning('rename failed on file: %s' % task.mfFilename.cStr())
            
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
            if self.dldb:
                self.dldb.setClientMultifileDecompressed(task.mfname)
            # Get rid of the decompressor
            del task.decompressor
            task.callback()
            del task.callback
            return Task.done

    def decompressMultifileDone(self):

        self.finalizePhase()

        self.notify.info('Done updating multifiles in phase: ' + `self.currentPhase`)
        self.progressSoFar += int(round(self.phaseOverallMap[self.currentPhase]*100))
        self.notify.info('progress so far ' + `self.progressSoFar`)
        messenger.send('phaseComplete-' + `self.currentPhase`)

        self.resumeInstall()

    def finalizePhase(self):
        # Get this phase ready for the game to use.
        
        mfFilename = Filename(self.topDir, Filename(self.currentMfname))
        self.MakeNTFSFilesGlobalWriteable(mfFilename)

        # Now that the multifile is available, mount it so we can
        # load files.
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(mfFilename, '.', VirtualFileSystem.MFReadOnly)
        
        # Ok, set the progress to 100 now
        self.setPercentPhaseComplete(self.currentPhase, 100)

    def getValue(self, key, default=None):
        return os.environ.get(key, default)

    def setValue(self, key, value):
        os.environ[key] = str(value)

    def getVerifyFiles(self):
        # TODO: take this out when we ship.
        return config.GetInt('launcher-verify', 0)

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return self.getValue('GAME_SERVER', '')

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

        self.notify.info("webAcctParams = %s" % s)
        
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
        if dict.has_key('secretsNeedsParentPassword'):
            self.secretNeedsParentPasswordKey = 1 and dict['secretsNeedsParentPassword']
            self.notify.info('secretNeedsParentPassword = %d' % self.secretNeedsParentPasswordKey)
        else:
            self.notify.warning('no secretNeedsParentPassword token in webAcctParams')
        if dict.has_key('chatEligible'):
            self.chatEligibleKey = 1 and dict['chatEligible']
            self.notify.info('chatEligibleKey = %d' % self.chatEligibleKey)
        else:
            self.notify.warning('no chatEligible token in webAcctParams')

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
        Get the PlayToken and return it.  The PlayToken is not saved;
        if this method is called a second time it will return None.
        """
        playToken = self.getValue(self.toontownPlayTokenKey)
        # Reset the PlayToken value so it will be more difficult for a
        # hacker to pull it out of the environment block.
        self.setValue(self.toontownPlayTokenKey, "")

        if playToken == "NO PLAYTOKEN":
            playToken = None
        return playToken

    #============================================================
    #   Registry functions
    #============================================================

    def setRegistry(self, name, value):
        return

    def getRegistry(self, name, missingValue = None):
        self.notify.info("getRegistry %s" % ((name, missingValue),))
        self.notify.info("self.VISTA = %s" % self.VISTA)
        self.notify.info("checking env" % os.environ)
        
        if (missingValue == None):
            missingValue = ""
        value = os.environ.get(name, missingValue)
        try:
            value = int(value)
        except:
            pass
        return value

    #============================================================
    # Download functions
    #============================================================

    def getCDDownloadPath(self, origPath, serverFilePath):
        return '%s/%s/CD_%d/%s' % (origPath, self.ServerVersion, self.fromCD, serverFilePath)

    def getDownloadPath(self, origPath, serverFilePath):
        return '%s/%s' % (origPath, serverFilePath)

    def hashIsValid(self, serverHash, hashStr):
        return serverHash.setFromDec(hashStr)

    def getAccountServer(self):
        # Toontown does not connect directly to any account server
        # return None
        # RAU oh yes we do! we need it for parent password authentication
        return self.getValue('ACCOUNT_SERVER', '')
        

    def getGame2Done(self):
        # This function exists only to allow for backwards compatibility
        return True

    def getNeedPwForSecretKey(self):
        if self.useTTSpecificLogin:
            # ok we don't get web account params,
            # this value should have been set from the login response
            self.notify.info("getNeedPwForSecretKey using tt-specific-login")
            try:
                if base.cr.chatChatCodeCreationRule == 'PARENT':
                    return True
                else:
                    return False
            except:
                return True
        else:
            return self.secretNeedsParentPasswordKey

    def getParentPasswordSet(self):
        """
        Get the parent password set key
        """        
        if self.useTTSpecificLogin:
            # ok we don't get web account params,
            # this value should have been set from the login response
            self.notify.info("getParentPasswordSet using tt-specific-login")
            try:
                if base.cr.isPaid():
                    return True
                else:
                    return False
            except:
                # when game is starting up, this may return an incorrect value
                return False
        else:
            return self.chatEligibleKey


    def canLeaveFirstIsland(self):
        return self.getPhaseComplete(4)

    #============================================================
    #  Launcher startup
    #============================================================

    def startGame(self):
        self.newTaskManager()
        eventMgr.restart()
        from toontown.toonbase import ToontownStart
