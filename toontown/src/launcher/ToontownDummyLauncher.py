from direct.directnotify import DirectNotifyGlobal
from otp.launcher.DummyLauncherBase import DummyLauncherBase
from toontown.launcher.ToontownLauncher import ToontownLauncher

# it's important to derive from DummyLauncherBase first so that Python
# will find its methods before looking at the real launcher
class ToontownDummyLauncher(DummyLauncherBase, ToontownLauncher):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownDummyLauncher")
    def __init__(self):
        DummyLauncherBase.__init__(self)
        # If we are running the show, the first 3 phases must be complete
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.setPhaseComplete(3, 100)
        
        self.tutorialComplete = 1
        self.frequency = 0.0
        self.windowOpen = 0
        # First phase starts at 3.5 for the dummy launcher because if you
        # have opened a window, you must have finished 3
        self.firstPhase = 3.5
        self.pandaErrorCodeKey = "PANDA_ERROR_CODE"
        self.goUserName = ""
        # Period timer minutes remaining
        self.periodTimeRemainingKey = "PERIOD_TIME_REMAINING"
        # Period name
        self.periodNameKey = "PERIOD_NAME"
        # Period name
        self.swidKey = "SWID"
        # Fake registry
        self.reg = {}
        self.startFakeDownload()
        
    def setTutorialComplete(self, complete):
        self.tutorialComplete = complete

    def getTutorialComplete(self):
        return self.tutorialComplete

    def setFrequency(self, freq):
        self.frequency = freq

    def getFrequency(self):
        return self.frequency

    def getInstallDir(self):
        return 'C:\Program Files\Disney\Disney Online\Toontown'

    def getUserName(self):
        return 'dummy'

    def getReferrerCode(self):
        return None

    def setRegistry(self, name, value):
        print "setRegistry[%s] = %s" % (name, value)
        self.reg[name] = value

    def getRegistry(self, name, defaultValue = None):
        if name in self.reg:
            value = self.reg[name]
        else:
            value = defaultValue
        print "getRegistry[%s] = %s" % (name, value)
        return value

    def getGame2Done(self):
        return 1

    def recordPeriodTimeRemaining(self, secondsRemaining):
        self.setRegistry(self.periodTimeRemainingKey, secondsRemaining)

    def recordPeriodName(self, periodName):
        self.setRegistry(self.periodNameKey, periodName)

    def recordSwid(self, swid):
        self.setRegistry(self.swidKey, swid)

    def getGoUserName(self):
        return self.goUserName

    def setGoUserName(self, userName):
        self.goUserName = userName    

    def getParentPasswordSet(self):
        """
        Get the parent password set key
        """
        return 0

    def getNeedPwForSecretKey(self):
        """
        Get the PlayToken out of the registry and return it.  The
        PlayToken is not saved; if this method is called a second
        time it will return None.
        """
        return 0
