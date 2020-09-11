from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *

import random
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import ToonInteriorColors
from toontown.hood import ZoneUtil


class DistributedGagshopInterior(DistributedObject.DistributedObject):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DistributedGagshopInterior')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore=cr.playGame.dnaStore

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount-1)
        code = self.dnaStore.getCatalogCode(category, index)
        # findFunc will probably be findNode or findTexture
        return findFunc(code)

    def replaceRandomInModel(self, model):
        """Replace named nodes with random items.
        Here are the name     Here is
        prefixes that are     what they
        affected:             do:
        
        random_mox_            change the Model Only.
        random_mcx_            change the Model and the Color.
        random_mrx_            change the Model and Recurse.
        random_tox_            change the Texture Only.
        random_tcx_            change the Texture and the Color.

        x is simply a uniquifying integer because Multigen will not
        let you have multiple nodes with the same name
        
        """
        baseTag="random_"
        npc=model.findAllMatches("**/"+baseTag+"???_*")
        for i in range(npc.getNumPaths()):
            np=npc.getPath(i)
            name=np.getName()
            
            b=len(baseTag)
            category=name[b+4:]
            key1=name[b]
            key2=name[b+1]
            
            assert(key1 in ["m", "t"])
            assert(key2 in ["c", "o", "r"])
            if key1 == "m":
                # ...model.
                model = self.randomDNAItem(category, self.dnaStore.findNode)
                assert(not model.isEmpty())
                newNP = model.copyTo(np)
                if key2 == "r":
                    self.replaceRandomInModel(newNP)
            elif key1 == "t":
                # ...texture.
                texture=self.randomDNAItem(category, self.dnaStore.findTexture)
                assert(texture)
                np.setTexture(texture,100)
                newNP=np
            if key2 == "c":
                if (category == "TI_wallpaper") or (category == "TI_wallpaper_border"):
                    self.randomGenerator.seed(self.zoneId)
                    newNP.setColorScale(
                        self.randomGenerator.choice(self.colors[category]))
                else:
                    newNP.setColorScale(
                        self.randomGenerator.choice(self.colors[category]))

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def chooseDoor(self):
        # I copy/pasted this door string choosing code from
        # DistributedToonInterior.
        # Door:
        doorModelName="door_double_round_ul" # hack  zzzzzzz
        # Switch leaning of the door:
        if doorModelName[-1:] == "r":
            doorModelName=doorModelName[:-1]+"l"
        else:
            doorModelName=doorModelName[:-1]+"r"
        door=self.dnaStore.findNode(doorModelName)
        return door

    def setup(self):
        self.dnaStore=base.cr.playGame.dnaStore
        # Set up random generator
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)

        self.interior = loader.loadModel('phase_4/models/modules/gagShop_interior')
        self.interior.reparentTo(render)


        # Load a color dictionary for this hood:
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        # Replace all the "random_xxx_" nodes:
        self.replaceRandomInModel(self.interior)

        # Pick a door model
        door = self.chooseDoor()
        # Find the door origins
        doorOrigin = render.find("**/door_origin;+s")
        doorNP = door.copyTo(doorOrigin)
        assert(not doorNP.isEmpty())
        assert(not doorOrigin.isEmpty())
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
        doorColor = self.randomGenerator.choice(self.colors["TI_door"])
        DNADoor.setupDoor(doorNP,
                          self.interior, doorOrigin,
                          self.dnaStore, str(self.block), 
                          doorColor)
        doorFrame = doorNP.find("door_*_flat")
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)

        del self.colors
        del self.dnaStore
        del self.randomGenerator
        self.interior.flattenMedium()
                                      
    def disable(self):
        self.interior.removeNode()
        del self.interior
        DistributedObject.DistributedObject.disable(self)
        
