
from pandac.PandaModules import *
import ToonHood
from toontown.town import DGTownLoader
from toontown.safezone import DGSafeZoneLoader
from toontown.toonbase.ToontownGlobals import *
import SkyUtil

class DGHood(ToonHood.ToonHood):
    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = DaisyGardens
        # Create the town state data
        self.townLoaderClass = DGTownLoader.DGTownLoader
        # Create the safe zone state data
        self.safeZoneLoaderClass = DGSafeZoneLoader.DGSafeZoneLoader
        self.storageDNAFile = "phase_8/dna/storage_DG.dna"
        # Dictionary which holds holiday specific lists of Storage DNA Files
        # Keyed off of the News Manager holiday IDs stored in ToontownGlobals
        self.holidayStorageDNADict = {WINTER_DECORATIONS : ['phase_8/dna/winter_storage_DG.dna'],
                                      HALLOWEEN_PROPS : ['phase_8/dna/halloween_props_storage_DG.dna']}
        # Use TT sky until we get a real one
        self.skyFile = "phase_3.5/models/props/TT_sky"
        self.spookySkyFile = "phase_3.5/models/props/BR_sky"
        self.titleColor = (0.8, 0.6, 1.0, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed("DGHood").addChild(self.fsm)
        
    def unload(self):
        self.parentFSM.getStateNamed("DGHood").removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)
        
    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)
        
    def exit(self):
        ToonHood.ToonHood.exit(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        
        # we have the wrong sky; load in the regular sky
        if not (self.sky.getTag("sky") == "Regular"):
            self.endSpookySky()
            
        SkyUtil.startCloudSky(self)
        
    def startSpookySky(self):
        if hasattr(self, "sky") and self.sky:
            self.stopSky()
        self.sky = loader.loadModel(self.spookySkyFile)
        self.sky.setTag("sky", "Halloween")
        self.sky.setScale(1.0)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setColor(0.5,0.5,0.5,1)
        self.sky.setBin("background", 100)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)

        #fade the sky in
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        fadeIn = self.sky.colorScaleInterval( 1.5, Vec4(1, 1, 1, 1),
                                               startColorScale = Vec4(1, 1, 1, 0.25),
                                               blendType = 'easeInOut')
        fadeIn.start()

        # Nowadays we use a CompassEffect to counter-rotate the sky
        # automatically at render time, rather than depending on a
        # task to do this just before the scene is rendered.
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)