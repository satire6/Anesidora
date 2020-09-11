
# It's important to import PandaModules first, in particular before
# importing Task, because once PandaModules is imported, Task.py can
# find pandac.pandaexpressModules.
from pandac.PandaModules import *

import string
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task

class DummyLauncherBase:
    def __init__(self):
        self.logPrefix = ''
        self._downloadComplete = False
        self.phaseComplete = {}
        for phase in self.LauncherPhases:
            self.phaseComplete[phase] = 0
        self.firstPhase = self.LauncherPhases[0]
        self.finalPhase = self.LauncherPhases[-1]
        # Fake download hash values
        self.launcherFileDbHash = HashVal()
        self.serverDbFileHash = HashVal()
        self.setPandaErrorCode(0)
        self.setServerVersion("dev")

    def isDummy(self):
        # Is this the DummyLauncher? Yes
        return 1

    def startFakeDownload(self):
        if ConfigVariableBool('fake-downloads', 0).getValue():
            duration = ConfigVariableDouble('fake-download-duration', 60).getValue()
            self.fakeDownload(duration)
        else:
            for phase in self.LauncherPhases:
                self.phaseComplete[phase] = 100
            self.downloadDoneTask(None)

    def isTestServer(self):
        # Change this depending on what you want to test
        return base.config.GetBool("is-test-server", 0)

    def setPhaseCompleteArray(self, newPhaseComplete):
        # useful for testing
        self.phaseComplete = newPhaseComplete

    def setPhaseComplete(self, phase, percent):
        # again, for testing
        self.phaseComplete[phase] = percent
        
    def getPhaseComplete(self, phase):
        return (self.phaseComplete[phase] >= 100)

    def setPandaWindowOpen(self):
        self.windowOpen = 1

    def setPandaErrorCode(self, code):
        """
        Set the exit code of panda. 0 means everything ok
        """
        self.pandaErrorCode = code

    def getPandaErrorCode(self):
        return self.pandaErrorCode

    def setDisconnectDetailsNormal(self):
        self.disconnectCode = 0
        self.disconnectMsg = 'normal'
        
    def setDisconnectDetails(self, newCode, newMsg):
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
        return base.config.GetBool("new-installation", 0)

    def setIsNotNewInstallation(self):
        pass

    def getLastLogin(self):
        if hasattr(self, 'lastLogin'):
            return self.lastLogin
        return ''

    def setLastLogin(self, login):
        self.lastLogin = login

    def setUserLoggedIn(self):
        self.userLoggedIn = 1

    def setPaidUserLoggedIn(self):
        self.paidUserLoggedIn = 1

    def getGameServer(self):
        return '206.16.11.19'

    def getAccountServer(self):
        return ''

    def getDeployment(self):
        """
        Get the language version 
        """
        return 'US'

    def getBlue(self):
        # This is a test DMC blue - this does not get downloaded though
        # return "aW8gkhzXUIDxVBr4ywXMGYTZFCMVkg0JNzu5lOqqOUAQL9efNvxfVd3TDWeiyHmCNUW5wMgroVq0YzWdSkcbG$StvC4$9RsVmKhuRQSNHV#080siG5BFfNSwuK#vogKAETqbCKnyfAZmC372Y$ndW4YwQMu9MyQ9RgyZWtEYbvy5lgzmHIJr9gJHTS#EQ9nQViRSuKU9ilWUVVABNJrtOXo1kYtcyF#O"
        # return "ummm8ChuwvpzE9X6pCY4XaW9ae3LEx4XAmzdkJN#j5xLOHLnW9YDd#HKs4PTXYrH2GZE0k1vhD0sASZeE5Vp3$3qF#yVLqfeh2We6$eUkwLhZgCGpdihiPWpx9Kc8eHah5dAd$muaI2t2ABaAGaKwNVXpKVuU0Yr9DeXwT1lKS27ZX33Oqhh$bJQgaPw5nc1PIydLhBFOLlxccKN83A4EpM0uxoACo2C";
        # return "EyHDPTHdCX5VFYXS8nvKPudKxaMRyUU4115r2wxO9RLQK7biOax1K9gKPwpzDSdeb8pa9PXni8mYdE#OvdsHorNoyjCMvMkWndpEcBytKp$Hq15PUKIXW2txZ$RyT8m7xPT$CSIMiXf#jCYXtt8gsa9zB2jQXd0SD7f#rm3Xz#6gA9Vv#fE0tIlifz8QK4e3eS7OFxPh$C#wuN4HR$K8KudnUq$VALfZQ5KyL4RlNFH#MnLNyu#lTg"
        return None

    def getPlayToken(self):
        # If you need a test PlayToken, this is the place for it.
        return None

    def getDISLToken(self):
        # If you need a test DISLToken, this is the place for it.
        return None

    def fakeDownloadPhaseTask(self, task):
        percentComplete = min(100, int(round((task.time/float(task.timePerPhase) * 100))))
        # The position in the array is phase-1 because it counts from 0
        self.setPhaseComplete(task.phase, percentComplete)
        messenger.send("launcherPercentPhaseComplete", [task.phase, percentComplete, 0, 0])
        if (percentComplete >= 100.0):
            messenger.send('phaseComplete-' + `task.phase`)
            return Task.done
        else:
            return Task.cont

    def downloadDoneTask(self, task):
        self._downloadComplete = True
        messenger.send("launcherAllPhasesComplete")
        return Task.done

    def fakeDownload(self, timePerPhase):
        self.phaseComplete = {
            1 : 100,
            2 : 100,
            3 : 0,
            3.5 : 0,
            4 : 0,
            5 : 0,
            5.5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0,
            10 : 0,
            11 : 0,
            12 : 0,
            13 : 0,
            }
        phaseTaskList = []
        # Some phases should already be downloaded
        firstPhaseIndex = self.LauncherPhases.index(self.firstPhase)
        for phase in self.LauncherPhases[firstPhaseIndex:]:
            phaseTask = Task(self.fakeDownloadPhaseTask, ("phaseDownload"+str(phase)))
            phaseTask.timePerPhase = timePerPhase
            phaseTask.phase = phase
            phaseTaskList.append(phaseTask)

        phaseTaskList.append(Task(self.downloadDoneTask))
        downloadSequence = Task.sequence(*phaseTaskList)
        taskMgr.remove("downloadSequence")
        taskMgr.add(downloadSequence, "downloadSequence")
