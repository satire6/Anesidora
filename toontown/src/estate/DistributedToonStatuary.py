from toontown.estate import DistributedStatuary
from toontown.estate import DistributedLawnDecor
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBase import *
from pandac.PandaModules import *
from toontown.toon import Toon
from toontown.toon import ToonDNA
import GardenGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import NodePath
from pandac.PandaModules import Point3

def dnaCodeFromToonDNA(dna):
    """This is the code that is stored in the uint16 optional parameter on the statue"""
    def findItemNumInList(wantItem, wantList):
        i = 0
        for item in wantList:
            if item == wantItem:
                break
            i += 1
        return i

    if dna.gender == 'f':
        genderTypeNum = 0
    else:
        genderTypeNum = 1

    # Left shift the bits to get the correct position
    legTypeNum = findItemNumInList(dna.legs, ToonDNA.toonLegTypes) << 1
    torsoTypeNum = findItemNumInList(dna.torso, ToonDNA.toonTorsoTypes) << 3
    headTypeNum = findItemNumInList(dna.head, ToonDNA.toonHeadTypes) << 7

    # OR them together so that we can get the optional parameter
    return headTypeNum | torsoTypeNum | legTypeNum | genderTypeNum

class DistributedToonStatuary(DistributedStatuary.DistributedStatuary):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonStatuary')

    # Note: These are the steps to take while adding a pose to the catalog list of available poses
    # 1) Add 205, 1005, 105 equivalent in GardenGlobals.py
    # 2) Add CatalogGardenItem(106, 1), in CatalogGenerator.py
    # 3) Make sure the correct pose matches in DistributedToonStatuary for 205, 206, etc.
    # 4) Adjust range in DistributedEstateAI.py   from 205 to (Last typeIndex of ToonStatue)
    # 5) Adjust range in DistributedGardenPlot.py from 205 to (Last typeIndex of ToonStatue)
    # 6) Adjust range in CatalogGardenItem.py     from 105 to (Last Specials number of ToonStatue)
    # 7) Adjust range in SpecialsPhoto.py         from 105 to (Last Specials number of ToonStatue)
    # 8) Add the name of the statue to TTLocalizerEnglish.py

    def __init__(self, cr):
        self.notify.debug('constructing DistributedToonStatuary')
        DistributedStatuary.DistributedStatuary.__init__(self, cr)
        # @TODO: Remove this before it goes to test.

        self.toon = None
##        if __debug__:
##            base.toonStatue = self

    def loadModel(self):
        DistributedStatuary.DistributedStatuary.loadModel(self)
        self.model.setScale(self.worldScale*1.5, self.worldScale*1.5, self.worldScale)
        self.getToonPropertiesFromOptional()
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties(self.headType, self.torsoType, self.legType, self.gender, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.setupStoneToon(dna)
        self.poseToonFromTypeIndex(self.typeIndex)
        self.toon.reparentTo(self.model)

    def delete(self):
        self.deleteToon()
        DistributedStatuary.DistributedStatuary.delete(self)
    
    def setupStoneToon(self, dna):
        self.toon = Toon.Toon()
        self.toon.setPos(0,0,0)
        self.toon.setDNA(dna)
        self.toon.initializeBodyCollisions('toonStatue')
        self.toon.stopBlink()
        self.toon.stopLookAround()

        self.gender = self.toon.style.gender
        self.speciesType = self.toon.style.getAnimal()
        self.headType = self.toon.style.head

##        self.removeTextures()
        self.setStoneTexture()
        self.toon.dropShadow.hide()
        self.toon.setZ(70)
        self.toon.setScale(20/1.5, 20/1.5, 20)

    def deleteToon(self):
        self.notify.debug('entering deleteToon')
        # Clean up the toon that is created
        assert self.toon
        self.toon.delete()
        self.toon = None
    
    def copyLocalAvatarToon(self):
        self.toon = Toon.Toon()
        self.toon.reparentTo(render)
        self.toon.setDNA(base.localAvatar.style)
        self.toon.setPos(base.localAvatar, 0, 0, 0)
        self.toon.pose('victory', 30)
        self.toon.setH(180)
        self.speciesType = self.toon.style.getAnimal()
        self.gender = self.toon.style.gender

    def setupCollision(self):
        DistributedStatuary.DistributedStatuary.setupCollision(self)
        # calcTightBounds is giving me a very small radius, probably because the pedestal is a square
        self.colSphereNode.setScale(self.colSphereNode.getScale()*1.5)

    def setupShadow(self):
        pass

    def removeTextures(self):
        '''
        Remove texture from the shirt, sleeves and bottom
        For each LOD, get the model, find the part, clear the texture,
        and set the color to gray.
        '''
##        gray = VBase4(0.6, 0.6, 0.6, 1)
        gray = VBase4(1.6, 1.6, 1.6, 1)
        self.toon.setColor(gray, 10)
##        self.toon.setColorScaleOff(10000)

        for node in self.toon.findAllMatches("**/*"):
            node.setState(RenderState.makeEmpty())
        
        # It looks like the medium and low LODs have some whack texture on them.
        # And only the high LOD has the desaturated textures.
        # Ideally all the LODs should have desaturated textures.
        # Since they don't we'll load the default textures and manually replace them. 
        desatShirtTex = loader.loadTexture("phase_3/maps/desat_shirt_1.jpg")
        desatSleeveTex = loader.loadTexture("phase_3/maps/desat_sleeve_1.jpg")
        desatShortsTex = loader.loadTexture("phase_3/maps/desat_shorts_1.jpg")
        desatSkirtTex = loader.loadTexture("phase_3/maps/desat_skirt_1.jpg")
        
        if (self.toon.hasLOD()):
            for lodName in self.toon.getLODNames():
                torso = self.toon.getPart('torso', lodName)
                
                torsoTop = torso.find('**/torso-top')
                if torsoTop:
                    # Replace whatever texture the toon has with the default desaturated textures.
                    torsoTop.setTexture(desatShirtTex, 1)
                
                sleeves = torso.find('**/sleeves')
                if sleeves:
                    # Replace whatever texture the toon has with the default desaturated textures.
                    sleeves.setTexture(desatSleeveTex, 1)
                
                bottoms = torso.findAllMatches('**/torso-bot*')
                for bottomNum in range(0, bottoms.getNumPaths()):
                    bottom = bottoms.getPath(bottomNum)
                    # Replace whatever texture the toon has with the default desaturated textures.
                    if (self.toon.style.torso[1] == 's'):
                        bottom.setTexture(desatShortsTex, 1)
                    else:
                        bottom.setTexture(desatSkirtTex, 1)

    def setStoneTexture(self):
        gray = VBase4(1.6, 1.6, 1.6, 1)
        self.toon.setColor(gray, 10)
        
        stoneTex = loader.loadTexture('phase_5.5/maps/smoothwall_1.jpg')
        # TextureStage for the entire toon model
        ts = TextureStage('ts')
        ts.setPriority(1)
        self.toon.setTexture(ts, stoneTex)

        # TextureStage for some detailed parts which have colored textures in the geometry
        tsDetail = TextureStage('tsDetail')
        tsDetail.setPriority(2)
        tsDetail.setSort(10)
        tsDetail.setCombineRgb(tsDetail.CMInterpolate, tsDetail.CSTexture, 
                               tsDetail.COSrcColor, tsDetail.CSPrevious, 
                               tsDetail.COSrcColor, tsDetail.CSConstant, 
                               tsDetail.COSrcColor)
        tsDetail.setColor(VBase4(0.5, 0.5, 0.5, 1))

        if (self.toon.hasLOD()):
            for lodName in self.toon.getLODNames():
                head = self.toon.getPart('head', lodName)

                # Make the eyes lighter colored. Its easier to alpha them out, than place another texture
                eyes = head.find('**/eye*')
                if not eyes.isEmpty():
                    eyes.setColor(Vec4(1.4, 1.4, 1.4, .3), 10)
                ears = head.find('**/ears*')
                
                animal = self.toon.style.getAnimal()
                if (animal != 'dog'):
                    muzzle = head.find('**/muzzle*neutral')
                else:
                    muzzle = head.find('**/muzzle*')

                # Extra work for the ears
                if ears != ears.notFound():
                    if self.speciesType == 'cat':
                        ears.setTexture(tsDetail, stoneTex)
##                        tsDetail.setColor(VBase4(0.8, 0.8, 0.8, 1))
                    elif self.speciesType == 'horse':
                        # Horse doesn't reach here because its ear geomNode is not named
                        # instead this is the work around:
                        # ears = head.getChild(0)
                        # ears.setTexture(tsDetail, stoneTex)
                        # tsDetail.setColor(VBase4(0.8, 0.8, 0.8, 1))
                        pass
                    elif self.speciesType == 'rabbit':
                        ears.setTexture(tsDetail, stoneTex)
                    elif self.speciesType == 'monkey':
                        ears.setTexture(tsDetail, stoneTex)
                        ears.setColor(VBase4(0.6, 0.9, 1, 1), 10)

                # Extra work for the muzzles
                if muzzle != muzzle.notFound():
                    # These animals need a simple 2nd texture stage for the muzzle.
                    # Keeping the 2nd Texture Stage for the muzzle so that the has less color
                    # (if the muzzle already had some color) and so that the nose doesn't
                    # appear completely black, it appears grey and has more stone texture.
                    muzzle.setTexture(tsDetail, stoneTex)                    
                    
                if (self.speciesType == 'dog'):
                    nose = head.find('**/nose')
                    if nose != nose.notFound():
                        nose.setTexture(tsDetail, stoneTex)
                            
        # Texture the eye-lashes separately
        tsLashes = TextureStage('tsLashes')
        tsLashes.setPriority(2)
        tsLashes.setMode(tsLashes.MDecal)

        # Lashes only exist in females
        if self.gender == 'f':
            if self.toon.hasLOD():
                # Lashes are there only in the 1st LOD
                head = self.toon.getPart('head', '1000')
            else:
                head = self.toon.getPart('head', 'lodRoot')

            if self.headType[1] == "l":
                openString = "open-long"
                closedString = "closed-long"
            else:
                openString = "open-short"
                closedString = "closed-short"

            lashesOpen = head.find('**/' + openString)
            lashesClosed = head.find('**/' + closedString)

            
            # Alpha-ing out the lashes to make them look gray-ish. 
            # Lashes have a black texture. Need a better way to blend the stoneTex
            # Virtually has no significance in applying the stone Texture to the lashes.
            if lashesOpen != lashesOpen.notFound():
                lashesOpen.setTexture(tsLashes, stoneTex)
                lashesOpen.setColor(VBase4(1, 1, 1, 0.4), 10)
            if lashesClosed != lashesClosed.notFound():
                lashesClosed.setTexture(tsLashes, stoneTex)
                lashesClosed.setColor(VBase4(1, 1, 1, 0.4), 10)

    def setOptional(self, optional):
        self.optional = optional

    def getToonPropertiesFromOptional(self):
        '''
        getToonPropertiesFromOptional extracts the toon properties as encoded in the optional parameter
        the optional parameter - uint16 has the following encoding
        bit 0 : gender
        bits 1 & 2 : legType
        bits 3-6 : torsoType
        bits 7-15 : headType
        '''

        #Bit-mask by the appropriate number and right shift to get the range from 0 to the appropriate number
        genderTypeNum = self.optional & 1
        legTypeNum = (self.optional & 6) >> 1
        torsoTypeNum = (self.optional & 120) >> 3
        headTypeNum = (self.optional & 65408) >> 7

        if genderTypeNum == 0:
            self.gender = 'f'
        else:
            self.gender = 'm'

        # @TODO: change these hardcoded numbers to length of the respective lists

        if legTypeNum <= len(ToonDNA.toonLegTypes):
            self.legType = ToonDNA.toonLegTypes[legTypeNum]
        else:
            assert(self.notify.error('illegal toon leg type'))

        if torsoTypeNum <= len(ToonDNA.toonTorsoTypes):
            self.torsoType = ToonDNA.toonTorsoTypes[torsoTypeNum]
        else:
            assert(self.notify.error('illegal toon torso type'))

        if headTypeNum <= len(ToonDNA.toonHeadTypes):
            self.headType = ToonDNA.toonHeadTypes[headTypeNum]
        else:
            assert(self.notify.error('illegal toon head type'))

    def poseToonFromTypeIndex(self, typeIndex):
        if typeIndex == 205:
            self.toon.pose('wave', 18)
        elif typeIndex == 206:
            self.toon.pose('victory', 116)
        elif typeIndex == 207:
            self.toon.pose('bored', 96)
        elif typeIndex == 208:
            self.toon.pose('think', 59)
##            self.toon.pose('think', 37)

    def poseToonFromSpecialsIndex(self, specialsIndex):
        if specialsIndex == 105:
            self.toon.pose('wave', 18)
        elif specialsIndex == 106:
            self.toon.pose('victory', 116)
        elif specialsIndex == 107:
            self.toon.pose('bored', 96)
        elif specialsIndex == 108:
            self.toon.pose('think', 59)
##            self.toon.pose('think', 37)
