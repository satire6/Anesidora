
from pandac.PandaModules import *
import ToonHood
from toontown.town import TutorialTownLoader
from toontown.toonbase.ToontownGlobals import *
import SkyUtil

class TutorialHood(ToonHood.ToonHood):
    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore,
                                   hoodId)
        self.id = Tutorial
        # Create the town state data
        self.townLoaderClass = TutorialTownLoader.TutorialTownLoader
        # Create the safe zone state data (There is no tutorial safe zone,
        # but we create this because Hood.py will try to del it)
        self.safeZoneLoaderClass = None
        # No storage dna becuase it is all loaded in playgame
        self.storageDNAFile = None
        self.skyFile = "phase_3.5/models/props/TT_sky"
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed("TutorialHood").addChild(self.fsm)
        
    def unload(self):
        self.parentFSM.getStateNamed("TutorialHood").removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        
    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)
        
    def exit(self):
        ToonHood.ToonHood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)

