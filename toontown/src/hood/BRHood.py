
from pandac.PandaModules import *
import ToonHood
from toontown.town import BRTownLoader
from toontown.safezone import BRSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class BRHood(ToonHood.ToonHood):
    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = TheBrrrgh
        # Create the town state data
        self.townLoaderClass = BRTownLoader.BRTownLoader
        # Create the safe zone state data
        self.safeZoneLoaderClass = BRSafeZoneLoader.BRSafeZoneLoader
        self.storageDNAFile = "phase_8/dna/storage_BR.dna"
        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {WINTER_DECORATIONS : ['phase_8/dna/winter_storage_BR.dna'],
                                      HALLOWEEN_PROPS : ['phase_8/dna/halloween_props_storage_BR.dna']}
        # The sky is actually in phase 6 because DD uses it too
        self.skyFile = "phase_3.5/models/props/BR_sky"
        self.spookySkyFile = "phase_3.5/models/props/BR_sky"
        self.titleColor = (0.3, 0.6, 1.0, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed("BRHood").addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed("BRHood").removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        
    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)
            
    def exit(self):
        ToonHood.ToonHood.exit(self)
    
