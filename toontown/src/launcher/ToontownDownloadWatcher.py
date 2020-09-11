from direct.directnotify import DirectNotifyGlobal
from otp.launcher.DownloadWatcher import DownloadWatcher
from toontown.toonbase import TTLocalizer

class ToontownDownloadWatcher(DownloadWatcher):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownDownloadWatcher")
    def __init__(self, phaseNames):
        DownloadWatcher.__init__(self, phaseNames)

    def update(self, phase, percent, reqByteRate, actualByteRate):
        """Update our text with a special case for toontorial."""
        DownloadWatcher.update(self, phase, percent, reqByteRate, actualByteRate)
        #RAU for bug TOON-1882 change Downloading Toontorial to Loading Toontorial
        #for TOONWEB-1335 do it for all phases
        phaseName = self.phaseNames[phase]
        self.text['text'] = (TTLocalizer.LoadingDownloadWatcherUpdate % (phaseName))

        
