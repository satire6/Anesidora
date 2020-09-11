""" DistributedToonInterior module"""

from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from toontown.toonbase import ToontownGlobals
import cPickle
import ToonInterior
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from direct.fsm import State
import random
import ToonInteriorColors
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA
from toontown.toon import ToonHead

# These four coordinates define the region we have available to fit
# the sign from the front of the building.  Signs will be scaled down
# to fit the smallest dimension, and centered within the box.
SIGN_LEFT = -4
SIGN_RIGHT = 4
SIGN_BOTTOM = -3.5
SIGN_TOP = 1.5

# This is the factor by which the trophy frames are scaled up to make
# room for long names like "FarrtKnocker".
FrameScale = 1.4

class DistributedToonInterior(DistributedObject.DistributedObject):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedToonInterior')
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        assert self.notify.debugStateCall(self)
        self.fsm = ClassicFSM.ClassicFSM('DistributedToonInterior',
                               [State.State('toon',
                                            self.enterToon,
                                            self.exitToon,
                                            ['beingTakenOver']),
                                State.State('beingTakenOver',
                                            self.enterBeingTakenOver,
                                            self.exitBeingTakenOver,
                                            []),
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            []),
                                ],
                               # Initial State
                               'toon',
                               # Final State
                               'off',
                               )
        self.fsm.enterInitialState()
        # self.generate will be called automatically.
        
    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert self.notify.debugStateCall(self)
        DistributedObject.DistributedObject.generate(self)
    
    def announceGenerate(self):
        assert self.notify.debugStateCall(self)
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        assert self.notify.debugStateCall(self)
        self.interior.removeNode()
        del self.interior
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        assert self.notify.debugStateCall(self)
        del self.fsm
        DistributedObject.DistributedObject.delete(self)
    
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
        assert self.notify.debugStateCall(self)
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
                # room has collisions already: remove collisions from models
                c = render.findAllMatches('**/collision')
                c.stash()
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
                    
    
    def setup(self):
        assert self.notify.debugStateCall(self)
        self.dnaStore=base.cr.playGame.dnaStore
        self.randomGenerator=random.Random()
        
        # The math here is a little arbitrary.  I'm trying to get a 
        # substantially different seed for each zondId, even on the 
        # same street.  But we don't want to weigh to much on the 
        # block number, because we want the same block number on 
        # different streets to be different.
        # Here we use the block number and a little of the branchId:
        # seedX=self.zoneId&0x00ff
        # Here we're using only the branchId:
        # seedY=self.zoneId/100
        # Here we're using only the block number:
        # seedZ=256-int(self.block)

        self.randomGenerator.seed(self.zoneId)

        interior = self.randomDNAItem("TI_room", self.dnaStore.findNode)
        assert(not interior.isEmpty())
        self.interior = interior.copyTo(render)

        # Load a color dictionary for this hood:
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        # Replace all the "random_xxx_" nodes:
        self.replaceRandomInModel(self.interior)
        
        # Door:
        doorModelName="door_double_round_ul" # hack  zzzzzzz
        # Switch leaning of the door:
        if doorModelName[-1:] == "r":
            doorModelName=doorModelName[:-1]+"l"
        else:
            doorModelName=doorModelName[:-1]+"r"
        door=self.dnaStore.findNode(doorModelName)
        # Determine where should we put the door:
        door_origin=render.find("**/door_origin;+s")
        doorNP=door.copyTo(door_origin)
        assert(not doorNP.isEmpty())
        assert(not door_origin.isEmpty())
        # The rooms are too small for doors:
        door_origin.setScale(0.8, 0.8, 0.8)
        # Move the origin away from the wall so it does not shimmer
        # We do this instead of decals
        door_origin.setPos(door_origin, 0, -0.025, 0)
        color=self.randomGenerator.choice(self.colors["TI_door"])
        DNADoor.setupDoor(doorNP, 
                          self.interior, door_origin, 
                          self.dnaStore,
                          str(self.block), color)
        # Setting the wallpaper texture with a priority overrides
        # the door texture, if it's decalled.  So, we're going to
        # move it out from the decal, and float it in front of
        # the wall:
        doorFrame = doorNP.find("door_*_flat")
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(color)

        # Grab the sign off the front of the building and copy it into
        # the interior, here.
        sign=hidden.find(
            "**/tb%s:*_landmark_*_DNARoot/**/sign;+s"%(self.block,))
        if not sign.isEmpty():
            signOrigin=self.interior.find("**/sign_origin;+s")
            assert(not signOrigin.isEmpty())
            # Copy, rather than instance, to avoid bug in flatten:
            newSignNP=sign.copyTo(signOrigin)

            # Restore the depth write flag, since the DNA turned it off.
            newSignNP.setDepthWrite(1, 1)
            
            mat=self.dnaStore.getSignTransformFromBlockNumber(int(self.block))

            # Invert the sign transform matrix to undo the
            # transformation that has already placed it on the
            # front of the building.
            inv = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            inv.invertFrom(mat)
            newSignNP.setMat(inv)
            # And flatten out that matrix so we can manipulate it further.
            newSignNP.flattenLight()

            # Now scale the sign to fit the room, and pull it out from
            # the wall a tiny bit.  We actually want to scale it to
            # fit within the box defined by (SIGN_LEFT, SIGN_RIGHT,
            # SIGN_BOTTOM, SIGN_TOP).

            # First, we need to determine the actual bounds of the sign.
            ll = Point3()
            ur = Point3()
            newSignNP.calcTightBounds(ll, ur)
            width = ur[0] - ll[0]
            height = ur[2] - ll[2]

            if width != 0 and height != 0:
                # And how much would we need to scale it in each dimension
                # to make it fit?
                xScale = (SIGN_RIGHT - SIGN_LEFT) / width
                zScale = (SIGN_TOP - SIGN_BOTTOM) / height

                # Now choose the smaller scale of the two, so it will fit
                # within its bounds without being squashed or stretched.
                scale = min(xScale, zScale)

                xCenter = (ur[0] + ll[0]) / 2.0
                zCenter = (ur[2] + ll[2]) / 2.0
                newSignNP.setPosHprScale(
                    (SIGN_RIGHT + SIGN_LEFT) / 2.0 - xCenter * scale, -0.1,
                    (SIGN_TOP + SIGN_BOTTOM) / 2.0 - zCenter * scale,
                    0.0, 0.0, 0.0,
                    scale, scale, scale)

        # Who Saved It:
        trophyOrigin=self.interior.find("**/trophy_origin")
        assert(not trophyOrigin.isEmpty())
        trophy=self.buildTrophy()
        if trophy:
            trophy.reparentTo(trophyOrigin)
            
        del self.colors
        del self.dnaStore
        del self.randomGenerator
            
        # Get rid of any transitions and extra nodes
        self.interior.flattenMedium()
    
    def setZoneIdAndBlock(self, zoneId, block):
        assert self.notify.debugStateCall(self)
        self.zoneId=zoneId
        self.block=block
    
    def setToonData(self, toonData):
        assert self.notify.debugStateCall(self)
        savedBy = cPickle.loads(toonData)
        self.savedBy = savedBy
    
    def buildTrophy(self):
        assert self.notify.debugStateCall(self)
        if self.savedBy == None:
            return None

        numToons = len(self.savedBy)
        pos = 1.25 - 1.25 * numToons
        
        trophy = hidden.attachNewNode('trophy')
        for avId, name, dnaTuple in self.savedBy:
            frame = self.buildFrame(name, dnaTuple)
            frame.reparentTo(trophy)
            frame.setPos(pos, 0, 0)
            pos += 2.5
        return trophy

    def buildFrame(self, name, dnaTuple):
        assert self.notify.debugStateCall(self)
        frame = loader.loadModel('phase_3.5/models/modules/trophy_frame')

        dna = ToonDNA.ToonDNA()
        apply(dna.newToonFromProperties, dnaTuple)

        head = ToonHead.ToonHead()
        head.setupHead(dna)

        head.setPosHprScale(
            0, -0.05, -0.05,
            180, 0, 0,
            0.55, 0.02, 0.55)
        if dna.head[0] == 'r':
            # Give rabbits a bit more space above the head.
            head.setZ(-0.15)
        elif dna.head[0] == 'h':
            # Give horses a bit more space below the head.
            head.setZ(0.05)
        elif dna.head[0] == 'm':
            # Mice should be a bit smaller to fit the ears.
            head.setScale(0.45, 0.02, 0.45)
            
        head.reparentTo(frame)

        nameText = TextNode("trophy")
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0, 0, 0, 1)
        nameText.setWordwrap(5.36 * FrameScale)
        nameText.setText(name)
        
        namePath = frame.attachNewNode(nameText.generate())
        namePath.setPos(0, -0.03, -.6)
        namePath.setScale(0.186 / FrameScale)

        frame.setScale(FrameScale, 1.0, FrameScale)
        return frame
    
    def setState(self, state, timestamp):
        assert self.notify.debugStateCall(self)
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])
    
    def enterOff(self):
        assert self.notify.debugStateCall(self)
    
    def exitOff(self):
        assert self.notify.debugStateCall(self)
    
    def enterToon(self):
        assert self.notify.debugStateCall(self)
    
    def exitToon(self):
        assert self.notify.debugStateCall(self)
    
    def enterBeingTakenOver(self, ts):
        """Kick everybody out of the building"""
        assert self.notify.debugStateCall(self)
        messenger.send("clearOutToonInterior")
    
    def exitBeingTakenOver(self):
        assert self.notify.debugStateCall(self)
