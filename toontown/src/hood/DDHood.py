
from pandac.PandaModules import *
import ToonHood
from toontown.town import DDTownLoader
from toontown.safezone import DDSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *

class DDHood(ToonHood.ToonHood):
    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DonaldsDock
        # Create the town state data
        self.townLoaderClass = DDTownLoader.DDTownLoader
        # Create the safe zone state data
        self.safeZoneLoaderClass = DDSafeZoneLoader.DDSafeZoneLoader
        self.storageDNAFile = "phase_6/dna/storage_DD.dna"
        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {WINTER_DECORATIONS : ['phase_6/dna/winter_storage_DD.dna'],
                                      HALLOWEEN_PROPS : ['phase_6/dna/halloween_props_storage_DD.dna']}
        # Donalds Dock reuses The Brrrgh's sky
        self.skyFile = "phase_3.5/models/props/BR_sky"
        self.titleColor = (0.8, 0.6, 0.5, 1.0)
        self.whiteFogColor = Vec4(0.8, 0.8, 0.8, 1)
        self.underwaterFogColor = Vec4(0.0, 0.0, 0.6, 1.0)
        self.spookySkyFile = "phase_3.5/models/props/BR_sky"

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed("DDHood").addChild(self.fsm)
        self.fog = Fog("DDFog")

    def unload(self):
        self.parentFSM.getStateNamed("DDHood").removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        self.fog = None

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)

    def exit(self):
        ToonHood.ToonHood.exit(self)
    
    def setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(self.underwaterFogColor)
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            self.sky.setFog(self.fog)
        
    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(0.0, 400.0)
            render.clearFog()
            render.setFog(self.fog)
            # Insist that fog is on the sky.  This will prevent the
            # sky from being contaminated by the trolley tunnel shadow
            # if we jump on the trolley.
            self.sky.clearFog()
            self.sky.setFog(self.fog)

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()
