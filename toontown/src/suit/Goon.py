from pandac.PandaModules import *
from direct.actor import Actor
from otp.avatar import Avatar 
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import GoonGlobals
import SuitDNA
import math

# list of anims per goon type

AnimDict = {
    # Patroller goon
    "pg": (("walk", "-walk"),
           ("collapse", "-collapse"),
           ("recovery", "-recovery"),
           ),
    # Securtiy goon
    "sg": (("walk", "-walk"),
           ("collapse", "-collapse"),
           ("recovery", "-recovery"),
           ),
    }

ModelDict = {
    "pg": ("phase_9/models/char/Cog_Goonie"),
    "sg": ("phase_9/models/char/Cog_Goonie"),
    }

class Goon(Avatar.Avatar):
    """ Goon class: """

    def __init__(self, dnaName=None):
        try:
            self.Goon_initialized
        except:
            self.Goon_initialized = 1
            Avatar.Avatar.__init__(self)

            # Let's preemptively ignore this event, since Goons don't
            # have a nametag anyway (and lighting doesn't even matter
            # in Toontown).  Ignoring this up front will save trouble
            # later.
            self.ignore("nametagAmbientLightChanged")

            # Initial properties
            self.hFov = 70
            self.attackRadius = 15
            self.strength = 15
            self.velocity = 4
            self.scale = 1.0

            if dnaName is not None:
                self.initGoon(dnaName)

    def initGoon(self, dnaName):
        dna = SuitDNA.SuitDNA()
        dna.newGoon(dnaName)
        self.setDNA(dna)
        self.type = dnaName

        self.createHead()
        # HACK: rotate the goon to match Panda coordinates
        self.find("**/actorGeom").setH(180)

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)
        
        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)
        
    def delete(self):
        try:
            self.Goon_deleted
        except:
            self.Goon_deleted = 1
            filePrefix = ModelDict[self.style.name]
            loader.unloadModel(filePrefix + "-zero")

            animList = AnimDict[self.style.name]
            for anim in animList:
                loader.unloadModel(filePrefix + anim[1])

            Avatar.Avatar.delete(self)
        return None

    def setDNAString(self, dnaString):
        self.dna = SuitDNA.SuitDNA()
        self.dna.makeFromNetString(dnaString)
        self.setDNA(self.dna)

    def setDNA(self, dna):
        if self.style:
            pass
        else:
            # store the DNA
            self.style = dna

            self.generateGoon()

            # this no longer works in the Avatar init!
            # I moved it here for lack of a better place
            # make the drop shadow
            self.initializeDropShadow()
            self.initializeNametag3d()

    def generateGoon(self):
        dna = self.style
        filePrefix = ModelDict[dna.name]
        self.loadModel(filePrefix + "-zero")

        animDict = {}
        animList = AnimDict[dna.name]
        for anim in animList:
            animDict[anim[0]] = filePrefix + anim[1]

        self.loadAnims(animDict)
        
    def getShadowJoint(self):
        return self.getGeomNode()

    def getNametagJoints(self):
        """
        Return the CharacterJoint that animates the nametag, in a list.
        """
        # Chars don't animate their nametags.
        return []

    def createHead(self):
        # head and radar for "hot" area
        self.headHeight = 3.0

        # Insert a head rotation node in between exposed joints for the
        # goon's head and hat.  Note: the hat is doing some animating seperately
        # from the head, that is why we have to have two separate exposed
        # nodes for the head and the hat.
        head = self.find("**/joint35")
        if head.isEmpty():
            head = self.find("**/joint40")
        self.hat = self.find("**/joint8")
        parentNode = head.getParent()
        self.head = parentNode.attachNewNode('headRotate')
        head.reparentTo(self.head)
        self.hat.reparentTo(self.head)

        # hide the hat of the other type of goon
        if self.type == "pg":
            self.hat.find("**/security_hat").hide()
        elif self.type == "sg":
            self.hat.find("**/hard_hat").hide()
        else:
            # neither - hide both
            self.hat.find("**/security_hat").hide()
            self.hat.find("**/hard_hat").hide()

        # grab a handle to the eye while we are at it
        self.eye = self.find("**/eye")
        self.eye.setColorScale(1,1,1,1)
        self.eye.setColor(1,1,0,1)

        self.radar = None
        
    def scaleRadar(self):
        # Remove the old radar
        if self.radar:
            self.radar.removeNode()

        self.radar = self.eye.attachNewNode('radar')
        
        # Load a new radar
        model = loader.loadModel("phase_9/models/cogHQ/alphaCone2")
        beam = self.radar.attachNewNode('beam')
        transformNode = model.find('**/transform')
        transformNode.getChildren().reparentTo(beam)
            
        self.radar.setPos(0, -.5, .4)
        self.radar.setTransparency(1)
        self.radar.setDepthWrite(0)

        # scale the width (assumes model width is 21)
        self.halfFov = self.hFov/2.0
        fovRad = self.halfFov * math.pi / 180.0
        self.cosHalfFov = math.cos(fovRad)
        kw = math.tan(fovRad) * self.attackRadius / 10.5

        # scale the length (assumes model length is 25, and headHeight=3)
        kl = math.sqrt(self.attackRadius * self.attackRadius + 9.0) / 25.0

        # Scale the beam to the right radius and fov
        beam.setScale(kw / self.scale, kl / self.scale, kw / self.scale)
        beam.setHpr(0, self.halfFov, 0)        

        # and make sure it reaches the floor.
        p = self.radar.getRelativePoint(beam, Point3(0, -6, -1.8))
        self.radar.setSz(-3.5 / p[2])

        # Bake in the transforms.
        self.radar.flattenMedium()

        # But we keep the color separate so the eye color won't override it.
        self.radar.setColor(1,1,1,.2)

    def colorHat(self):
        if self.type == "pg":
            colorList = GoonGlobals.PG_COLORS
        elif self.type == "sg":
            colorList = GoonGlobals.SG_COLORS
        else:
            return
        
        # make the hat maroonish if these guys are powerful
        if self.strength >= 20:
            # red
            self.hat.setColorScale(colorList[0])
        elif self.strength >= 15:
            # orange
            self.hat.setColorScale(colorList[1])
        else:
            self.hat.clearColorScale()
        

