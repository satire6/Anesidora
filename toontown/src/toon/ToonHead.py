"""
ToonHead module: contains the ToonHead class

This class defines just the head portion of a Toon.  It's useful for
getting a floating head to put in an Avatar panel for instance;
furthermore, Toon inherits from this class to define its own head
piece.

"""

from direct.actor import Actor
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import string
import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.directnotify import DirectNotifyGlobal

# toon head models dictionary
if not base.config.GetBool('want-new-anims', 1):
    HeadDict = { "dls": "/models/char/dogMM_Shorts-head-", \
                "dss":"/models/char/dogMM_Skirt-head-", \
                "dsl":"/models/char/dogSS_Shorts-head-", \
                "dll":"/models/char/dogLL_Shorts-head-", \
                "c":"/models/char/cat-heads-", \
                "h":"/models/char/horse-heads-", \
                "m":"/models/char/mouse-heads-", \
                "r":"/models/char/rabbit-heads-", \
                "f":"/models/char/duck-heads-", \
                "p":"/models/char/monkey-heads-", \
                "b":"/models/char/bear-heads-",\
                "s":"/models/char/pig-heads-"
                 }
else:
    HeadDict = { "dls": "/models/char/tt_a_chr_dgm_shorts_head_", \
                "dss":"/models/char/tt_a_chr_dgm_skirt_head_", \
                "dsl":"/models/char/tt_a_chr_dgs_shorts_head_", \
                "dll":"/models/char/tt_a_chr_dgl_shorts_head_", \
                "c":"/models/char/cat-heads-", \
                "h":"/models/char/horse-heads-", \
                "m":"/models/char/mouse-heads-", \
                "r":"/models/char/rabbit-heads-", \
                "f":"/models/char/duck-heads-", \
                "p":"/models/char/monkey-heads-", \
                "b":"/models/char/bear-heads-",\
                "s":"/models/char/pig-heads-"
                 }

EyelashDict = {"d": "/models/char/dog-lashes", \
               "c": "/models/char/cat-lashes", \
               "h": "/models/char/horse-lashes", \
               "m": "/models/char/mouse-lashes", \
               "r": "/models/char/rabbit-lashes", \
               "f": "/models/char/duck-lashes", \
               "p": "/models/char/monkey-lashes", \
               "b": "/models/char/bear-lashes",\
               "s": "/models/char/pig-lashes"
               }

DogMuzzleDict = { 'dls': '/models/char/dogMM_Shorts-headMuzzles-',
                  'dss': '/models/char/dogMM_Skirt-headMuzzles-',
                  'dsl': '/models/char/dogSS_Shorts-headMuzzles-',
                  'dll': '/models/char/dogLL_Shorts-headMuzzles-'
                }

class ToonHead(Actor.Actor):
    """Toon class:"""

    notify = DirectNotifyGlobal.directNotify.newCategory('ToonHead')

    # Eyes open and closed textures for blinks
    EyesOpen = loader.loadTexture('phase_3/maps/eyes.jpg',
                                  'phase_3/maps/eyes_a.rgb')
    EyesOpen.setMinfilter(Texture.FTLinear)
    EyesOpen.setMagfilter(Texture.FTLinear)
    EyesClosed = loader.loadTexture('phase_3/maps/eyesClosed.jpg',
                                    'phase_3/maps/eyesClosed_a.rgb')
    EyesClosed.setMinfilter(Texture.FTLinear)
    EyesClosed.setMagfilter(Texture.FTLinear)

    # Emotional eye textures for tutorial
    EyesSadOpen = loader.loadTexture('phase_3/maps/eyesSad.jpg',
                                  'phase_3/maps/eyesSad_a.rgb')
    EyesSadOpen.setMinfilter(Texture.FTLinear)
    EyesSadOpen.setMagfilter(Texture.FTLinear)
    EyesSadClosed = loader.loadTexture('phase_3/maps/eyesSadClosed.jpg',
                                    'phase_3/maps/eyesSadClosed_a.rgb')
    EyesSadClosed.setMinfilter(Texture.FTLinear)
    EyesSadClosed.setMagfilter(Texture.FTLinear)
    EyesAngryOpen = loader.loadTexture('phase_3/maps/eyesAngry.jpg',
                                  'phase_3/maps/eyesAngry_a.rgb')
    EyesAngryOpen.setMinfilter(Texture.FTLinear)
    EyesAngryOpen.setMagfilter(Texture.FTLinear)
    EyesAngryClosed = loader.loadTexture('phase_3/maps/eyesAngryClosed.jpg',
                                    'phase_3/maps/eyesAngryClosed_a.rgb')
    EyesAngryClosed.setMinfilter(Texture.FTLinear)
    EyesAngryClosed.setMagfilter(Texture.FTLinear)
    EyesSurprised = loader.loadTexture('phase_3/maps/eyesSurprised.jpg',
                                       'phase_3/maps/eyesSurprised_a.rgb')
    EyesSurprised.setMinfilter(Texture.FTLinear)
    EyesSurprised.setMagfilter(Texture.FTLinear)
    Muzzle = loader.loadTexture('phase_3/maps/muzzleShrtGeneric.jpg')
    Muzzle.setMinfilter(Texture.FTLinear)
    Muzzle.setMagfilter(Texture.FTLinear)
    MuzzleSurprised = loader.loadTexture('phase_3/maps/muzzleShortSurprised.jpg')
    MuzzleSurprised.setMinfilter(Texture.FTLinear)
    MuzzleSurprised.setMagfilter(Texture.FTLinear)


    # We define four points around the perimeter of each eye, as
    # seen from the front:
    #
    #   A       B       A       B
    #
    #         *           *
    #     D     C       D     C
    #
    # These four points represent the extremes of motion of the
    # pupil in each of the diagonal directions.  These four
    # points, along with the origin approximated above with *,
    # determine the mapping of pupil directions to pupil
    # coordinates.
    LeftA = Point3(0.06, 0.0, 0.14)
    LeftB = Point3(-0.13, 0.0, 0.1)
    LeftC = Point3(-0.05, 0.0, 0.0)
    LeftD = Point3(0.06, 0.0, 0.0)
    RightA = Point3(0.13, 0.0, 0.1)
    RightB = Point3(-0.06, 0.0, 0.14)
    RightC = Point3(-0.06, 0.0, 0.0)
    RightD = Point3(0.05, 0.0, 0.0)
    # This point is the between LeftA and LeftD where y = 0.
    LeftAD = Point3(LeftA[0] -
                    (LeftA[2] * (LeftD[0] - LeftA[0]) /
                     (LeftD[2] - LeftA[2])),
                    0.0, 0.0)
    # This point is the between LeftB and LeftC where y = 0.
    LeftBC = Point3(LeftB[0] -
                    (LeftB[2] * (LeftC[0] - LeftB[0]) /
                     (LeftC[2] - LeftB[2])),
                    0.0, 0.0)
    # Similarly on the right eye.
    RightAD = Point3(RightA[0] -
                     (RightA[2] * (RightD[0] - RightA[0]) /
                      (RightD[2] - RightA[2])),
                     0.0, 0.0)
    RightBC = Point3(RightB[0] -
                     (RightB[2] * (RightC[0] - RightB[0]) /
                      (RightC[2] - RightB[2])),
                     0.0, 0.0)


    def __init__(self):
        try:
            self.ToonHead_initialized
        except:
            self.ToonHead_initialized = 1
            Actor.Actor.__init__(self)

            # This is a unique string that identifies this particular
            # ToonHead among all others.  It's used to generate task
            # names; we can't necessarily use doId, because we might
            # not have one at this level.
            self.toonName = 'ToonHead-' + str(self.this)

            # Here are some of those task names we were talking about.
            self.__blinkName = 'blink-' + self.toonName
            self.__stareAtName = 'stareAt-' + self.toonName
            self.__lookName = 'look-' + self.toonName
            self.lookAtTrack = None

            # Set up a simple state machine to manage the eyelids.

            self.__eyes = None
            self.__eyelashOpen = None
            self.__eyelashClosed = None
            self.__lod500Eyes = None
            self.__lod250Eyes = None
            self.__lpupil = None
            self.__lod500lPupil = None
            self.__lod250lPupil = None
            self.__rpupil = None
            self.__lod500rPupil = None
            self.__lod250rPupil = None
            self.__muzzle = None
            self.__eyesOpen = ToonHead.EyesOpen
            self.__eyesClosed = ToonHead.EyesClosed
            self.__height = 0.0

            # Create our own random number generator.  We do this
            # mainly so we don't jumble up the random number chain of
            # the rest of the world (making playback from a session
            # more reliable).
            self.randGen = random.Random()
            self.randGen.seed(random.random())

            self.eyelids = ClassicFSM('eyelids',
                                   [State('off',
                                          self.enterEyelidsOff,
                                          self.exitEyelidsOff,
                                          ['open', 'closed', 'surprised']),
                                    State('open',
                                          self.enterEyelidsOpen,
                                          self.exitEyelidsOpen,
                                          ['closed', 'surprised', 'off']),
                                    State('surprised',
                                          self.enterEyelidsSurprised,
                                          self.exitEyelidsSurprised,
                                          ['open', 'closed', 'off']),
                                    State('closed',
                                          self.enterEyelidsClosed,
                                          self.exitEyelidsClosed,
                                          ['open', 'surprised', 'off'])],
                                   # initial State
                                   'off',
                                   # final State
                                   'off',
                                   )

            self.eyelids.enterInitialState()
            self.emote = None

            # This is the node and the point relative to the node that
            # the stareAt task will make the ToonHead look at.
            self.__stareAtNode = NodePath()
            self.__defaultStarePoint = Point3(0, 0, 0)
            self.__stareAtPoint = self.__defaultStarePoint
            self.__stareAtTime = 0
            self.lookAtPositionCallbackArgs = None

        return None

    def delete(self):
        try:
            self.ToonHead_deleted
        except:
            self.ToonHead_deleted = 1
            taskMgr.remove(self.__blinkName)
            taskMgr.remove(self.__lookName)
            taskMgr.remove(self.__stareAtName)
            if self.lookAtTrack:
                self.lookAtTrack.finish()
                self.lookAtTrack = None
            del self.eyelids
            del self.__stareAtNode
            del self.__stareAtPoint
            if self.__eyes:
                del self.__eyes
            if self.__lpupil:
                del self.__lpupil
            if self.__rpupil:
                del self.__rpupil
            if self.__eyelashOpen:
                del self.__eyelashOpen
            if self.__eyelashClosed:
                del self.__eyelashClosed
            self.lookAtPositionCallbackArgs = None
            Actor.Actor.delete(self)

    def setupHead(self, dna, forGui = 0):
        """setupHead(self, AvatarDNA dna)

        Loads the high-resolution head model only and plays the
        neutral animation on it.  Useful only when you want a floating
        head, not a complete Toon.

        If forGui is true, this sets up the head for placement within
        the DirectGui system; specifically, the depth test and write
        transitions are set appropriately, and the eyes are fixed so
        they will render properly.  For making a head to parent in the
        3-d world, leave forGui false.

        This also scales the head by toonHeadScale and toonBodyScale,
        so that all heads are relatively sized.

        """
        self.__height = self.generateToonHead(1, dna, ("1000",), forGui)
        self.generateToonColor(dna)

        animalStyle = dna.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        headScale = ToontownGlobals.toonHeadScales[animalStyle]

        # We also scale up by 1.3 to compensate for legacy code that
        # was written before we started applying the bodyScale.
        self.getGeomNode().setScale(headScale[0] * bodyScale * 1.3,
                                    headScale[1] * bodyScale * 1.3,
                                    headScale[2] * bodyScale * 1.3)

        if forGui:
            # Turn on depth write and test.
            self.getGeomNode().setDepthWrite(1)
            self.getGeomNode().setDepthTest(1)

        if dna.getAnimal() == "dog":
            self.loop("neutral")

    def fitAndCenterHead(self, maxDim, forGui = 0):
        # Compute an xform which centers geometry on origin and scales it
        # to max +/- maxDim/2.0 in size
        p1 = Point3()
        p2 = Point3()
        self.calcTightBounds(p1, p2)
        # Take into account rotation by 180 degrees if necessary
        if forGui:
            h = 180
            # Need to flip max and min
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        else:
            h = 0
        # Find dimension
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = maxDim/biggest
        # find midpoint
        mid = (p1 + d/2.0) * s
        # We must push the head a distance forward in Y so it doesn't
        # intersect the near plane, which is incorrectly set to 0 in
        # DX for some reason.
        self.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2],
                            h, 0, 0,
                            s, s, s)

    def setLookAtPositionCallbackArgs(self, argTuple):
        # findSomethingToLookAt assumes argTuple is an array
        # of obj w/'getLookAtPosition' method, and method argument
        self.lookAtPositionCallbackArgs = argTuple

    def getHeight(self):
        return self.__height

    def getRandomForwardLookAtPoint(self):
        x = self.randGen.choice((-0.8, -0.5, 0, 0.5, 0.8))
        z = self.randGen.choice((-0.5, 0, 0.5, 0.8))
        return Point3(x, 1.5, z)

    def findSomethingToLookAt(self):
        """findSomethingToLookAt(self)

        Picks a random direction at spawns a StareAt task to look in
        that direction.  This is called from time to time by the LookAround task.

        This is overridden in Toon.py to find something in
        particular to look at.

        """
        if(self.lookAtPositionCallbackArgs != None):
            pnt = self.lookAtPositionCallbackArgs[0].getLookAtPosition(self.lookAtPositionCallbackArgs[1],self.lookAtPositionCallbackArgs[2])
            self.startStareAt(self, pnt)
            return

        if(self.randGen.random() < 0.33):
            lookAtPnt = self.getRandomForwardLookAtPoint()
        else:
            lookAtPnt = self.__defaultStarePoint

        # Now look that direction!
        self.lerpLookAt(lookAtPnt, blink=1)

    # Generate and color methods.  These are called by setupHead() and
    # by Toon.py to create and color a head.

    def generateToonHead(self, copy, style, lods, forGui = 0):
        """generateToonHead(self, bool copy, AvatarDNA style,
                            tuple lods)
        Load the head model for the toon.
        If copy = 0, instance geom instead of copying.
        """        
        headStyle = style.head
        #ToonHead.notify.debug('RAU headstyle = %s' % headStyle)

        # this will store the method we need
        # to call to hide various head parts
        fix = None

        # load the appropriate file
        if (headStyle == "dls"):
            # dog, long head, short muzzle
            filePrefix = HeadDict["dls"]
            headHeight = 0.75
        elif (headStyle == "dss"):
            # dog, short head, short muzzle
            filePrefix = HeadDict["dss"]
            headHeight = 0.5
        elif (headStyle == "dsl"):
            # dog, short head, long muzzle
            filePrefix = HeadDict["dsl"]
            headHeight = 0.5
        elif (headStyle == "dll"):
            # dog, long head, long muzzle
            filePrefix = HeadDict["dll"]
            headHeight = 0.75
        elif (headStyle == "cls"):
            # cat, long head, short muzzle
            filePrefix = HeadDict["c"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "css"):
            # cat, short head, short muzzle
            filePrefix = HeadDict["c"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "csl"):
            # cat, short head, long muzzle
            filePrefix = HeadDict["c"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "cll"):
            # cat, long head, long muzzle
            filePrefix = HeadDict["c"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "hls"):
            # horse, long head, short muzzle
            filePrefix = HeadDict["h"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "hss"):
            # horse, short head, short muzzle
            filePrefix = HeadDict["h"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "hsl"):
            # horse, short head, long muzzle
            filePrefix = HeadDict["h"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "hll"):
            # horse, long head, long muzzle
            filePrefix = HeadDict["h"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "mls"):
            # mouse, long head, short muzzle
            filePrefix = HeadDict["m"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "mss"):
            # mouse, short head, short muzzle
            filePrefix = HeadDict["m"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "rls"):
            # rabbit, long head/muzzle, short ears
            filePrefix = HeadDict["r"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "rss"):
            # rabbit, short head/muzzle, short ears
            filePrefix = HeadDict["r"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "rsl"):
            # rabbit, short head/muzzle, long ears
            filePrefix = HeadDict["r"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "rll"):
            # rabbit, long head/muzzle, long ears
            filePrefix = HeadDict["r"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "fls"):
            # duck, long head, short bill
            filePrefix = HeadDict["f"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "fss"):
            # duck, short head, short bill
            filePrefix = HeadDict["f"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "fsl"):
            # duck, short head, long bill
            filePrefix = HeadDict["f"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "fll"):
            # duck, long head, long bill
            filePrefix = HeadDict["f"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "pls"):
            # monkey, long head, short muzzle
            filePrefix = HeadDict["p"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "pss"):
            # monkey, short head, short muzzle
            filePrefix = HeadDict["p"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "psl"):
            # monkey, short head, long muzzle
            filePrefix = HeadDict["p"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "pll"):
            # monkey, long head, long muzzle
            filePrefix = HeadDict["p"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "bls"):
            # bear, long head, short muzzle
            filePrefix = HeadDict["b"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "bss"):
            # bear, short head, short muzzle
            filePrefix = HeadDict["b"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "bsl"):
            # bear, short head, long muzzle
            filePrefix = HeadDict["b"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "bll"):
            # bear, long head, long muzzle
            filePrefix = HeadDict["b"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif (headStyle == "sls"):
            # pig, long head, short muzzle
            filePrefix = HeadDict["s"]
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif (headStyle == "sss"):
            # pig, short head, short muzzle
            filePrefix = HeadDict["s"]
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif (headStyle == "ssl"):
            # pig, short head, long muzzle
            filePrefix = HeadDict["s"]
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif (headStyle == "sll"):
            # pig, long head, long muzzle
            filePrefix = HeadDict["s"]
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        else:
            ToonHead.notify.error("unknown head style: %s" % headStyle)

        # load the model and massage the geometry
        if len(lods) == 1:        
            self.loadModel("phase_3" + filePrefix + lods[0], "head", "lodRoot",
                           copy)
            if not forGui:
                pLoaded = self.loadPumpkin(headStyle[1], None, copy)
                self.loadSnowMan(headStyle[1], None, copy)

            if not copy:
                self.showAllParts('head')
            if fix != None:
                fix(style, None, copy)

            if not forGui:
                if pLoaded:
                    self.__fixPumpkin(style, None, copy)
                else:
                    self.__lods = lods
                    self.__style = style
                    self.__headStyle = headStyle
                    self.__copy = copy

        else:
            for lod in lods:
                self.loadModel("phase_3" + filePrefix + lod, "head", lod, copy)                
                if not forGui:
                    pLoaded = self.loadPumpkin(headStyle[1], lod, copy)
                    self.loadSnowMan(headStyle[1], lod, copy)

                if not copy:
                    self.showAllParts('head', lod)
                if fix != None:
                    fix(style, lod, copy)

                if not forGui:
                    if pLoaded:
                        self.__fixPumpkin(style, lod, copy)
                    else:
                        self.__lods = lods
                        self.__style = style
                        self.__headStyle = headStyle
                        self.__copy = copy

        # use the appropriate eye texture
        self.__fixEyes(style, forGui)
        self.setupEyelashes(style)
        self.eyelids.request("closed")
        self.eyelids.request("open")
        self.setupMuzzles(style)

        return headHeight

    def loadPumpkin(self,headStyle, lod, copy):
        if (hasattr(base, 'launcher') and
            ((not base.launcher) or
             (base.launcher and base.launcher.getPhaseComplete(4)))):

            if not hasattr(self,'pumpkins'):
                self.pumpkins = NodePathCollection()

            ppath = 'phase_4/models/estate/pumpkin_'
            if(headStyle is 'l'):
                if copy:
                    pmodel = loader.loadModel(ppath + 'tall')
                else:
                    pmodel = loader.loadModel(ppath + 'tall')
                ptype = 'tall'
            else:
                if copy:
                    pmodel = loader.loadModel(ppath + 'short')
                else:
                    pmodel = loader.loadModel(ppath + 'short')
                ptype = 'short'

            if pmodel:
                p = pmodel.find('**/pumpkin_'+ptype+'*')
                p.setScale(0.5)
                p.setZ(-0.5)
                p.setH(180)
                if lod:
                    p.reparentTo(self.find('**/' + lod + '/**/__Actor_head'))
                else:
                    p.reparentTo(self.find('**/__Actor_head'))
                self.pumpkins.addPath(p)
                pmodel.remove()
                return True
            else:
                del self.pumpkins
                return False
        else:
            ToonHead.notify.debug("phase_4 not complete yet. Postponing pumpkin head load.")
            
    def loadSnowMan(self, headStyle, lod, copy):
        if hasattr(base, 'launcher') and ((not base.launcher) or 
                    (base.launcher and base.launcher.getPhaseComplete(4))):
            if not hasattr(self, 'snowMen'):
                self.snowMen = NodePathCollection()
            
            snowManPath = 'phase_4/models/props/tt_m_int_snowmanHead_'
            if headStyle is 'l':
                snowManPath = snowManPath+'tall'
            else:
                snowManPath = snowManPath + 'short'
                
            model = loader.loadModel(snowManPath)
            if model:
                model.setScale(0.4)
                model.setZ(-0.5)
                model.setH(180)
                if lod:
                    model.reparentTo(self.getPart('head',lod))
                else:
                    model.reparentTo(self.find('**/__Actor_head'))
                self.snowMen.addPath(model)
                model.stash()
                return True
            else:
                del self.snowMen
                return False
        else:
            ToonHead.notify.debug("phase_4 not loaded yet.")

    def __fixPumpkin(self, style, lodName = None, copy = 1):
        if (lodName == None):
            searchRoot = self
        else:
            searchRoot = self.find("**/" + str(lodName))

        pumpkin = searchRoot.find( "**/__Actor_head/pumpkin*" )
        pumpkin.stash()

    def enablePumpkins(self, enable):
        # This is for the case that the head was generated before the pumpkin model was available, due to phase loading.
        # It uses a few temporary private variables created when the initial pumpkin load attempt failed.
        # If successful, it should clean those variables up.
        if not hasattr(self,'pumpkins'):
            if len(self.__lods) == 1:
                pLoaded = self.loadPumpkin(self.__headStyle[1], None, self.__copy)
                if pLoaded:
                    self.__fixPumpkin(self.__style, None, self.__copy)
            else:
                for lod in self.__lods:
                    pLoaded = self.loadPumpkin(self.__headStyle[1], lod, self.__copy)
                    if pLoaded:
                        self.__fixPumpkin(self.__style, lod, self.__copy)

            if hasattr(self,'pumpkins'):
                for x in ['__lods','__style','__headStyle','__copy']:
                    if hasattr(self,'_ToonHead'+x):
                        delattr(self,'_ToonHead'+x)

        if hasattr(self,'pumpkins'):
            if enable:
                if self.__eyelashOpen:
                    self.__eyelashOpen.stash()
                if self.__eyelashClosed:
                    self.__eyelashClosed.stash()
                self.pumpkins.unstash()
            else:
                if self.__eyelashOpen:
                    self.__eyelashOpen.unstash()
                if self.__eyelashClosed:
                    self.__eyelashClosed.unstash()
                self.pumpkins.stash()
    
    def enableSnowMen(self, enable):
        if not hasattr(self, 'snowMen'):
            if len(self.__lods) == 1:
                self.loadSnowMan(self.__headStyle[1], None, self.__copy)
            else:
                for lod in self.__lds:
                    self.loadSnowMan(self.__headStyle[1], lod, self.__copy)
            
        if hasattr(self, 'snowMen'):
            if enable:
                if self.__eyelashOpen:
                    self.__eyelashOpen.stash()
                if self.__eyelashClosed:
                    self.__eyelashClosed.stash()
                self.snowMen.unstash()
            else:
                if self.__eyelashOpen:
                    self.__eyelashOpen.unstash()
                if self.__eyelashClosed:
                    self.__eyelashClosed.unstash()
                self.snowMen.stash()

    def generateToonColor(self, style):
        """generateToonColor(self, AvatarDNA style)
        Color the toon's parts as specified by the dna.
        Color any LODs by searching for ALL matches.
        """

        # color the head - may have multiple pieces
        parts = self.findAllMatches("**/head*")
        parts.setColor(style.getHeadColor())

        # color the ears, if they are not black
        animalType = style.getAnimal()
        if ((animalType == "cat") or
            (animalType == "rabbit") or
            (animalType == 'bear') or
            (animalType == "mouse") or
            (animalType == "pig")):
            parts = self.findAllMatches("**/ear?-*")
            parts.setColor(style.getHeadColor())

    def __fixEyes(self, style, forGui = 0):
        """__fixEyes(self, AvatarDNA style)
        Make sure the eyes render in proper order, and don't attempt
        to animate the pupils via the animation.  Instead, we may move
        them around directly."""

        mode = -3
        if forGui:
            mode = -2

        if (self.hasLOD()):
            for lodName in self.getLODNames():
                self.drawInFront("eyes*", "head-front*", mode, lodName=lodName)
                # NOTE: had to change all ref's to "joint-" to "joint_" as Maya
                # does not support "-" in node names
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find("**/joint_pupil*").isEmpty():
                        self.drawInFront("joint_pupil*", "eyes*", -1, lodName=lodName)
                    else:                    
                        self.drawInFront("def_*_pupil", "eyes*", -1, lodName=lodName)
                else:
                    self.drawInFront("joint_pupil*", "eyes*", -1, lodName=lodName)  
                              
            # Save the various eye LODs for blinking.
            self.__eyes = self.getLOD(1000).find('**/eyes*')            
            self.__lod500Eyes = self.getLOD(500).find('**/eyes*')
            self.__lod250Eyes = self.getLOD(250).find('**/eyes*')

            # Now make sure the eyes are still white--they might tend to
            # inherit the color from the head otherwise.

            if self.__lod500Eyes.isEmpty():
                self.__lod500Eyes = None
            else:
                self.__lod500Eyes.setColorOff()
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/joint_pupilL*').isEmpty():
                        self.__lod500lPupil = self.__lod500Eyes.find('**/joint_pupilL*')
                        self.__lod500rPupil = self.__lod500Eyes.find('**/joint_pupilR*')
                    else:
                        self.__lod500lPupil = self.__lod500Eyes.find('**/def_left_pupil*')
                        self.__lod500rPupil = self.__lod500Eyes.find('**/def_right_pupil*')
                else:
                    self.__lod500lPupil = self.__lod500Eyes.find('**/joint_pupilL*')
                    self.__lod500rPupil = self.__lod500Eyes.find('**/joint_pupilR*')
            if self.__lod250Eyes.isEmpty():
                self.__lod250Eyes = None
            else:
                self.__lod250Eyes.setColorOff()
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/joint_pupilL*').isEmpty():
                        self.__lod250lPupil = self.__lod250Eyes.find('**/joint_pupilL*')
                        self.__lod250rPupil = self.__lod250Eyes.find('**/joint_pupilR*')
                    else:
                        self.__lod250lPupil = self.__lod250Eyes.find('**/def_left_pupil*')
                        self.__lod250rPupil = self.__lod250Eyes.find('**/def_right_pupil*')
                else:
                    self.__lod250lPupil = self.__lod250Eyes.find('**/joint_pupilL*')
                    self.__lod250rPupil = self.__lod250Eyes.find('**/joint_pupilR*')
        else:
            self.drawInFront("eyes*", "head-front*", mode)
            if base.config.GetBool('want-new-anims', 1):
                if not self.find("joint_pupil*").isEmpty():
                    self.drawInFront("joint_pupil*", "eyes*", -1)
                else:                
                    self.drawInFront("def_*_pupil", "eyes*", -1)
            else:
                self.drawInFront("joint_pupil*", "eyes*", -1)
            # Save the eyes for blinking.
            self.__eyes = self.find('**/eyes*')

        # Now locate each pupil and put it in a local coordinate space so
        # we can easily slide it around on the face.
        if not self.__eyes.isEmpty():
            self.__eyes.setColorOff()
            self.__lpupil = None
            self.__rpupil = None
            if base.config.GetBool('want-new-anims', 1):  
                if not self.find('**/joint_pupilL*').isEmpty():                
                    if self.getLOD(1000): 
                        lp = self.getLOD(1000).find('**/joint_pupilL*')
                        rp = self.getLOD(1000).find('**/joint_pupilR*')                        
                    else:                    
                        lp = self.find('**/joint_pupilL*')
                        rp = self.find('**/joint_pupilR*')
                else:                
                    if not self.getLOD(1000):                    
                        lp = self.find('**/def_left_pupil*')
                        rp = self.find('**/def_right_pupil*')  
                    else:  
                        lp = self.getLOD(1000).find('**/def_left_pupil*')
                        rp = self.getLOD(1000).find('**/def_right_pupil*')
            else:
                lp = self.__eyes.find('**/joint_pupilL*')
                rp = self.__eyes.find('**/joint_pupilR*')                
                                
            if lp.isEmpty() or rp.isEmpty():
                print "Unable to locate pupils."
            else:
                leye = self.__eyes.attachNewNode('leye')
                reye = self.__eyes.attachNewNode('reye')

                # These matrices were determined empirically.  They
                # setup a coordinate space so that the X-Y plane is
                # parallel to the eye, and 0,0,0 is in the pupil's
                # natural resting place.
                lmat = Mat4(0.802174, 0.59709, 0, 0,
                            -0.586191, 0.787531, 0.190197, 0,
                            0.113565, -0.152571, 0.981746, 0,
                            -0.233634, 0.418062, 0.0196875, 1)
                leye.setMat(lmat)

                rmat = Mat4(0.786788, -0.617224, 0, 0,
                            0.602836, 0.768447, 0.214658, 0,
                            -0.132492, -0.16889, 0.976689, 0,
                            0.233634, 0.418062, 0.0196875, 1)
                reye.setMat(rmat)

                # Now move the pupils into their new coordinate
                # spaces, and flatten out the vertices so when they're
                # at (0,0,0) they're in the right place.
                self.__lpupil = leye.attachNewNode('lpupil')
                self.__rpupil = reye.attachNewNode('rpupil')
                lpt = self.__eyes.attachNewNode('')
                rpt = self.__eyes.attachNewNode('')
                lpt.wrtReparentTo(self.__lpupil)
                rpt.wrtReparentTo(self.__rpupil)
                lp.reparentTo(lpt)
                rp.reparentTo(rpt)

                # Also bump up the override parameter on the pupil
                # textures so they won't get overridden when we set
                # the blink texture.                
                
                self.__lpupil.adjustAllPriorities(1)
                self.__rpupil.adjustAllPriorities(1)                    
                if self.__lod500Eyes:
                    self.__lod500lPupil.adjustAllPriorities(1)
                    self.__lod500rPupil.adjustAllPriorities(1)
                if self.__lod250Eyes:
                    self.__lod250lPupil.adjustAllPriorities(1)
                    self.__lod250rPupil.adjustAllPriorities(1)

                # This breaks the "animating" dog eyes.  For now,
                # we'll only flatten if we haven't got a dog.
                animalType = style.getAnimal()
                if animalType != "dog":
                    self.__lpupil.flattenStrong()
                    self.__rpupil.flattenStrong()                    

    def __setPupilDirection(self, x, y):
        """__setPupilDirection(self, float x, float y)

        Sets both pupils to look in the indicated direction, where x
        and y are both in the range [-1 .. 1] and represent the
        direction the eyes should look relative to forward: [0, 0] is
        straight ahead, [-1, 0] is to the left, and [0, 1] is straight
        up.

        """

        # Compute the points on the left and right edges of each eye,
        # corresponding to the y height.
        if y < 0.0:
            y2 = -y
            left1 = self.LeftAD + (self.LeftD - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftC - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightD - self.RightAD) * y2
            right2 = self.RightBC + (self.RightC - self.RightBC) * y2
        else:
            y2 = y
            left1 = self.LeftAD + (self.LeftA - self.LeftAD) * y2
            left2 = self.LeftBC + (self.LeftB - self.LeftBC) * y2
            right1 = self.RightAD + (self.RightA - self.RightAD) * y2
            right2 = self.RightBC + (self.RightB - self.RightBC) * y2

        # Now interpolate between these points based on the x position.
        left0 = Point3(0.0, 0.0,
                       left1[2] -
                       (left1[0] * (left2[2] - left1[2]) /
                        (left2[0] - left1[0])))
        right0 = Point3(0.0, 0.0,
                        right1[2] -
                        (right1[0] * (right2[2] - right1[2]) /
                         (right2[0] - right1[0])))

        if x < 0.0:
            x2 = -x
            left = left0 + (left2 - left0) * x2
            right = right0 + (right2 - right0) * x2
        else:
            x2 = x
            left = left0 + (left1 - left0) * x2
            right = right0 + (right1 - right0) * x2

        self.__lpupil.setPos(left)
        self.__rpupil.setPos(right)

    def __lookPupilsAt(self, node, point):
        """__lookPupilsAt(self, NodePath node, Point3 point)

        Positions the pupils to look, as nearly as possible, toward
        the indicated point in space, relative to the indicated
        NodePath.

        If node is None, it is a special indication that point
        represents a vector relative to the head, not necessarily a
        particular point in space.

        """

        # First, we need to convert the point to the coordinate space
        # of our eyes.

        if node != None:
            mat = node.getMat(self.__eyes)
            point = mat.xformPoint(point)

        # Now, determine the intersection with a plane a certain
        # distance in front of our face of a line drawn from the
        # center of our head through the point.  This maps the point
        # in space to a 2-d pupil offse.

        distance = 1.0
        recip_z = 1.0/max(0.1, point[1])

        x = distance * point[0] * recip_z
        y = distance * point[2] * recip_z

        # Now clamp these to -1 .. 1.
        x = min(max(x, -1), 1)
        y = min(max(y, -1), 1)

        self.__setPupilDirection(x, y)


    def __lookHeadAt(self, node, point, frac = 1.0, lod = None):
        """__lookHeadAt(self, NodePath node, Point3 point, float frac)

        Positions the head to look, as nearly as possible, toward
        the indicated point in space, relative to the indicated
        NodePath.

        If frac is specified, it should be a number between 0 and 1
        and indicates what fraction of the rotation should be made
        this frame.

        If node is None, it is a special indication that point
        represents a vector relative to the head, not necessarily a
        particular point in space.

        The return value is true if we are within 1 degree of our
        target, false otherwise.

        """

        reachedTarget = 1

        # First, we need to get the relative transform from the head's
        # parent.  We'll assume the same transform applies to all
        # heads, and just pick the first LOD head for this.

        if lod == None:
            head = self.getPart('head', self.getLODNames()[0])
        else:
            head = self.getPart('head', lod)

        if node != None:
            headParent = head.getParent()
            mat = node.getMat(headParent)
            point = mat.xformPoint(point)

        rot = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
        lookAt(rot, Vec3(point), Vec3(0, 0, 1), CSDefault)

        scale = VBase3(0, 0, 0)
        hpr = VBase3(0, 0, 0)
        if decomposeMatrix(rot, scale, hpr, CSDefault):
            # Clamp the HPR to a natural range.  I believe H should
            # be in the range -60 .. 60, while P should be in the
            # range -20 .. 30.  More than this seems unnatural.

            hpr = VBase3(min(max(hpr[0], -60), 60),
                         min(max(hpr[1], -20), 30),
                         0)

            if frac != 1:
                # Rotate only part of the way. This must be based on
                # our current rotation.
                currentHpr = head.getHpr()

                reachedTarget = (abs(hpr[0] - currentHpr[0]) < 1.0) and \
                                (abs(hpr[1] - currentHpr[1]) < 1.0)

                hpr = currentHpr + (hpr - currentHpr) * frac


            # Now rotate each of the heads.
            if lod == None:
                for lodName in self.getLODNames():
                    head = self.getPart('head', lodName)
                    head.setHpr(hpr)
            else:
                head.setHpr(hpr)

        return reachedTarget

    def setupEyelashes(self, style):
        # if the toon is male no need to set lashes
        if style.getGender() == 'm':
            # if eyelashes are present, remove them
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
                self.__eyelashOpen = None
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
                self.__eyelashClosed = None
        else:
            # it's a female load the appropriate eyelash models
            if self.__eyelashOpen:
                self.__eyelashOpen.removeNode()
            if self.__eyelashClosed:
                self.__eyelashClosed.removeNode()
            animal = style.head[0]
            model = loader.loadModel('phase_3' + EyelashDict[animal])
            if self.hasLOD():
                # probably can't see them beyond 1st LOD...
                head = self.getPart('head', '1000')
            else:
                head = self.getPart('head', 'lodRoot')
            # determine which type of lash to use (long or short)
            length = style.head[1]
            if length == "l":
                openString = "open-long"
                closedString = "closed-long"
            else:
                openString = "open-short"
                closedString = "closed-short"
            self.__eyelashOpen = model.find("**/" + openString).copyTo(head)
            self.__eyelashClosed = model.find("**/" + closedString).copyTo(head)
            model.removeNode()

    def __fixHeadLongLong(self, style, lodName=None, copy = 1):
        """__fixHeadLongLong(self, AvatarDNA style, string=None, bool = 1)
        Hide all short parts"""
        if (lodName == None):
            searchRoot = self
        else:
            searchRoot = self.find("**/" + str(lodName))

        otherParts = searchRoot.findAllMatches( "**/*short*" )
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).stash()


    def __fixHeadLongShort(self, style, lodName=None, copy = 1):
        """__fixHeadLongShort(self, AvatarDNA style, string=None, bool = 1)
        Hide the short heads and long muzzles - some special cases"""
        animalType = style.getAnimal()
        headStyle = style.head
        if (lodName == None):
            searchRoot = self
        else:
            searchRoot = self.find("**/" + str(lodName))

        # if there are ears to switch
        if (animalType != "duck") and (animalType != "horse"):
            # rabbits are reversed
            if (animalType == "rabbit"):
                if copy:
                    searchRoot.find("**/ears-long").removeNode()
                else:
                    searchRoot.find("**/ears-long").hide()
            else:
                if  copy:
                    searchRoot.find("**/ears-short").removeNode()
                else:
                    searchRoot.find("**/ears-short").hide()

        # rabbits only have one type of eye poly
        if (animalType != "rabbit"):
            if copy:
                searchRoot.find("**/eyes-short").removeNode()
            else:
                searchRoot.find("**/eyes-short").hide()

        # Now every animal except dog has 2 types of pupils except the dog
        if animalType != 'dog':
            if copy:
                searchRoot.find("**/joint_pupilL_short").removeNode()
                searchRoot.find("**/joint_pupilR_short").removeNode()
            else:
                searchRoot.find("**/joint_pupilL_short").stash()
                searchRoot.find("**/joint_pupilR_short").stash()

        # hide the short head
        if copy:
            self.find("**/head-short").removeNode()
            self.find("**/head-front-short").removeNode()
        else:
            self.find("**/head-short").hide()
            self.find("**/head-front-short").hide()

        # rabbits are backwards once again
        if (animalType != "rabbit"):
            muzzleParts = searchRoot.findAllMatches("**/muzzle-long*")
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()
        else:
            muzzleParts = searchRoot.findAllMatches("**/muzzle-short*")
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

    def __fixHeadShortLong(self, style, lodName=None, copy = 1):
        """__fixHeadShortLong(self, AvatarDNA style, string=None, bool = 1)
        Hide the long heads and short muzzles - some special cases"""
        animalType = style.getAnimal()
        headStyle = style.head
        if (lodName == None):
            searchRoot = self
        else:
            searchRoot = self.find("**/" + str(lodName))

        # if there are ears to switch
        if (animalType != "duck") and (animalType != "horse") :
            # rabbits are reversed
            if (animalType == "rabbit"):
                if copy:
                    searchRoot.find("**/ears-short").removeNode()
                else:
                    searchRoot.find("**/ears-short").hide()
            else:
                if copy:
                    searchRoot.find("**/ears-long").removeNode()
                else:
                    searchRoot.find("**/ears-long").hide()

        # rabbits only have one type of eye poly
        if (animalType != "rabbit"):
            if copy:
                searchRoot.find("**/eyes-long").removeNode()
            else:
                searchRoot.find("**/eyes-long").hide()

        # Now every animal except dog has 2 types of pupils except the dog
        if animalType != 'dog':
            if copy:
                searchRoot.find("**/joint_pupilL_long").removeNode()
                searchRoot.find("**/joint_pupilR_long").removeNode()
            else:
                searchRoot.find("**/joint_pupilL_long").stash()
                searchRoot.find("**/joint_pupilR_long").stash()

        # hide the short head
        if copy:
            searchRoot.find("**/head-long").removeNode()
            searchRoot.find("**/head-front-long").removeNode()
        else:
            searchRoot.find("**/head-long").hide()
            searchRoot.find("**/head-front-long").hide()

        # rabbits are backwards once again
        if (animalType != "rabbit"):
            muzzleParts = searchRoot.findAllMatches("**/muzzle-short*")
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()
        else:
            muzzleParts = searchRoot.findAllMatches("**/muzzle-long*")
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

    def __fixHeadShortShort(self, style, lodName=None, copy = 1):
        """__fixHeadShortShort(self, AvatarDNA style, string=None, bool = 1)
        Hide all long parts"""
        if (lodName == None):
            searchRoot = self
        else:
            searchRoot = self.find("**/" + str(lodName))

        otherParts = searchRoot.findAllMatches( "**/*long*" )
        for partNum in range(0, otherParts.getNumPaths()):
            if copy:
                otherParts.getPath(partNum).removeNode()
            else:
                otherParts.getPath(partNum).stash()



    ###
    ### Tasks
    ###

    def __blinkOpenEyes(self, task):
        # Only try to open our eyes if they're currently closed.
        if self.eyelids.getCurrentState().getName() == 'closed':
            self.eyelids.request('open')
        # Do a double blink every once in a while
        r = self.randGen.random()
        if r < 0.1:
            # Short time for a double blink
            t = 0.2
        else:
            # Pick a random time for the next blink
            # We can just reuse r here instead of computing a new one
            t = r * 4.0 + 1.0
        taskMgr.doMethodLater(t, self.__blinkCloseEyes, self.__blinkName)
        return Task.done

    def __blinkCloseEyes(self, task):
        if self.eyelids.getCurrentState().getName() != 'open':
            # If our eyes are not currently open, do nothing and wait
            # till next blink cycle.
            taskMgr.doMethodLater(4.0, self.__blinkCloseEyes, self.__blinkName)

        else:
            # In the normal case, blink the eyes closed then open again.
            self.eyelids.request('closed')
            taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def startBlink(self):
        """startBlink(self)
        Starts the Blink task.
        """
        # remove any old
        taskMgr.remove(self.__blinkName)
        # spawn the new task
        if self.__eyes:
            self.openEyes()
        taskMgr.doMethodLater(self.randGen.random() * 4.0 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        """stopBlink(self)
        """
        taskMgr.remove(self.__blinkName)
        # It appears this function may sometimes be called
        # AFTER some nodepaths have been deleted. Make sure
        # they are still around before proceeding
        if self.__eyes:
            self.eyelids.request('open')

    # state entry functions
    def closeEyes(self):
        self.eyelids.request('closed')

    def openEyes(self):
        self.eyelids.request('open')

    def surpriseEyes(self):
        self.eyelids.request('surprised')

    # these three aren't explicit states, just texture substitutions
    def sadEyes(self):
        self.__eyesOpen = ToonHead.EyesSadOpen
        self.__eyesClosed = ToonHead.EyesSadClosed

    def angryEyes(self):
        self.__eyesOpen = ToonHead.EyesAngryOpen
        self.__eyesClosed = ToonHead.EyesAngryClosed

    def normalEyes(self):
        self.__eyesOpen = ToonHead.EyesOpen
        self.__eyesClosed = ToonHead.EyesClosed

    def blinkEyes(self):
        """blinkEyes(self)
        blinks the eyes once, then starts the blink task to keep blinking.
        """
        taskMgr.remove(self.__blinkName)
        self.eyelids.request('closed')
        taskMgr.doMethodLater(0.1, self.__blinkOpenEyes, self.__blinkName)

    def __stareAt(self, task):
        """stareAt(self, task)

        This task makes the eyes and head track a particular point in
        space, which may be either fixed or moving.  It's defined by
        the __stareAtNode and __stareAtPoint members.

        """

        # Rather than lerping to a particular point, we'll chase the
        # target by moving some fraction of the distance remaining
        # each frame.  This will give us a nice ease-out to the
        # target, and give us an elastic feel as the target moves
        # around our head.

        frac = 2 * globalClock.getDt()  # controls speed of head turning
        reachedTarget = self.__lookHeadAt(
            self.__stareAtNode, self.__stareAtPoint, frac)
        self.__lookPupilsAt(self.__stareAtNode, self.__stareAtPoint)

        if reachedTarget and self.__stareAtNode == None:
            # If we're staring at what we were supposed to, and it's
            # not going to move anywhere, then we might as well
            # stop the task.
            return Task.done
        else:
            return Task.cont

    def doLookAroundToStareAt(self, node, point):
        self.startStareAt(node, point)
        # Restart the look around
        self.startLookAround()

    def startStareAtHeadPoint(self, point):
        # stare at a point relative to own head
        self.startStareAt(self, point)

    def startStareAt(self, node, point):
        """startStareAt(self, NodePath node, Point3 point)

        Starts the StareAt task.  The ToonHead and eyes will rotate
        each frame to track the indicated point, relative to the
        indicated node.

        """
        # remove any old
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None

        self.__stareAtNode = node

        if(point != None):
            self.__stareAtPoint = point
        else:
            self.__stareAtPoint = self.__defaultStarePoint

        self.__stareAtTime = globalClock.getFrameTime()

        # spawn the new task
        taskMgr.add(self.__stareAt, self.__stareAtName)

    def lerpLookAt(self, point, time = 1.0, blink=0):
        """lerpLookAt(self, Point3 point, float time)

        This is similar to startStareAt(), except (a) it can only look
        at a point in space around the head, not at an arbitrary node,
        and (b) it uses an actual lerp to achieve this, rather than
        trying to chase a potentially moving target each frame.  This
        is superior to using startStareAt() when the target is just a
        point, because it gets better ease-in and ease-out effects,
        and because it uses less CPU.

        BUT it has a major artifact: the pupils can 'twitch' far off center before returning to being
        centered as the head turns up and down.  This effect is less noticeable with stareAt

        stopStareAt() can be used to interrupt either the lerp begun
        with lerpLookAt, or the task started with startStareAt().

        """
        # Remove any old tasks
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None


        lodNames = self.getLODNames()
        if lodNames:
            lodName = lodNames[0]
        else:
            # nevermind: we are being deleted
            return 0
        head = self.getPart('head', lodName)

        # First, save the current head and eye position.
        startHpr = head.getHpr()
        startLpupil = self.__lpupil.getPos()
        startRpupil = self.__rpupil.getPos()

        # Now, rotate immediately to the target.  We do this just as a
        # cheesy way to compute the target head and eye position;
        # we'll put it back in a second.
        self.__lookHeadAt(None, point, lod = lodName)
        self.__lookPupilsAt(None, point)

        endHpr = head.getHpr()
        endLpupil = self.__lpupil.getPos() * 0.5
        endRpupil = self.__rpupil.getPos() * 0.5

        # Now restore the positions and begin the lerp.
        head.setHpr(startHpr)
        self.__lpupil.setPos(startLpupil)
        self.__rpupil.setPos(startRpupil)

        # If you are already looking in that general direction, stay there
        if startHpr.almostEqual(endHpr, 10):
            return 0

        # People naturally blink when turning their heads
        if blink:
            self.blinkEyes()

        lookToTgt_TimeFraction = 0.2
        lookToTgtTime = time * lookToTgt_TimeFraction
        returnToEyeCenterTime = time - lookToTgtTime - 0.5
        origin = Point3(0,0,0)

        blendType = "easeOut"
        self.lookAtTrack = Parallel(
            Sequence(
            LerpPosInterval(self.__lpupil, lookToTgtTime, endLpupil, blendType = blendType),
            Wait(0.5),
            LerpPosInterval(self.__lpupil, returnToEyeCenterTime, origin, blendType = blendType),
            ),
            Sequence(
            LerpPosInterval(self.__rpupil, lookToTgtTime, endRpupil, blendType = blendType),
            Wait(0.5),
            LerpPosInterval(self.__rpupil, returnToEyeCenterTime, origin, blendType = blendType),
            ),
            name = self.__stareAtName,
            )

        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            self.lookAtTrack.append(LerpHprInterval(head, time, endHpr, blendType = "easeInOut"))

        self.lookAtTrack.start()

        #lPupilSeq = Task.sequence(
        #    self.__lpupil.lerpPos(endLpupil, lookToTgtTime, blendType = blend_type),
        #    Task.pause(0.5),
        #    self.__lpupil.lerpPos(origin, returnToEyeCenterTime, blendType = blend_type),
        #    )
        #rPupilSeq = Task.sequence(
        #    self.__rpupil.lerpPos(endRpupil, lookToTgtTime, blendType = blend_type),
        #    Task.pause(0.5),
        #    self.__rpupil.lerpPos(origin, returnToEyeCenterTime, blendType = blend_type),
        #    )
        #taskMgr.add(lPupilSeq, self.__stareAtName)
        #taskMgr.add(rPupilSeq, self.__stareAtName)
        return 1

    def stopStareAt(self):
        """stopStareAt(self)

        Stops the StareAt task, and lerps the head back to its neutral
        position.

        """
        self.lerpLookAt(Vec3.forward())

    def stopStareAtNow(self):
        """stopStareAtNow(self)

        Stops the StareAt task, and pops the head back to its neutral
        position.  Useful when you want to delete the head right now
        and you don't want to wait for it to return to neutral.

        """
        taskMgr.remove(self.__stareAtName)
        if self.lookAtTrack:
            self.lookAtTrack.finish()
            self.lookAtTrack = None

        # it seems this maybe getting called AFTER the pupils are deleted...
        if self.__lpupil and self.__rpupil:
            self.__setPupilDirection(0, 0)

        for lodName in self.getLODNames():
            head = self.getPart('head', lodName)
            head.setHpr(0, 0, 0)

    def __lookAround(self, task):
        """lookAround(self, task)
        This task makes the head look in a new direction, chosen by
        findSomethingToLookAt(), every so often.
        """
        self.findSomethingToLookAt()
        t = self.randGen.random() * 4.0 + 3.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)
        return Task.done

    def startLookAround(self):
        """startLookAround(self)
        Starts the LookAround task.
        """
        # remove any old
        taskMgr.remove(self.__lookName)
        # spawn the new task
        t = self.randGen.random() * 5.0 + 2.0
        taskMgr.doMethodLater(t, self.__lookAround, self.__lookName)

    def stopLookAround(self):
        """stopLookAround(self)

        Stops the LookAround task gracefully, by lerping the head back
        to neutral.

        """
        taskMgr.remove(self.__lookName)
        self.stopStareAt()

    def stopLookAroundNow(self):
        """stopLookAroundNow(self)

        Stops the LookAround task suddenly.

        """
        taskMgr.remove(self.__lookName)
        self.stopStareAtNow()

    ###
    ### State transitions
    ###

    def enterEyelidsOff(self):
        """enterEyelidsOff(self)
        """
        pass

    def exitEyelidsOff(self):
        pass

    def enterEyelidsOpen(self):
        """enterEyelidsOpen(self)
        """
        if not self.__eyes.isEmpty():
            self.__eyes.setTexture(self.__eyesOpen, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.show()
            if self.__eyelashClosed:
                self.__eyelashClosed.hide()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(self.__eyesOpen, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(self.__eyesOpen, 1)
            if self.__lpupil:
                self.__lpupil.show()
                self.__rpupil.show()
            if self.__lod500lPupil:
                self.__lod500lPupil.show()
                self.__lod500rPupil.show()
            if self.__lod250lPupil:
                self.__lod250lPupil.show()
                self.__lod250rPupil.show()

    def exitEyelidsOpen(self):
        pass


    def enterEyelidsClosed(self):
        """enterEyelidsClosed(self)
        """
        if not self.__eyes.isEmpty() and self.__eyesClosed:
            self.__eyes.setTexture(self.__eyesClosed, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.hide()
            if self.__eyelashClosed:
                self.__eyelashClosed.show()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(self.__eyesClosed, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(self.__eyesClosed, 1)
            if self.__lpupil:
                self.__lpupil.hide()
                self.__rpupil.hide()
            if self.__lod500lPupil:
                self.__lod500lPupil.hide()
                self.__lod500rPupil.hide()
            if self.__lod250lPupil:
                self.__lod250lPupil.hide()
                self.__lod250rPupil.hide()


    def exitEyelidsClosed(self):
        pass

    def enterEyelidsSurprised(self):
        """enterEyelidsSurprised(self)
        """
        if not self.__eyes.isEmpty() and ToonHead.EyesSurprised:
            self.__eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__eyelashOpen:
                self.__eyelashOpen.hide()
            if self.__eyelashClosed:
                self.__eyelashClosed.hide()
            if self.__lod500Eyes:
                self.__lod500Eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__lod250Eyes:
                self.__lod250Eyes.setTexture(ToonHead.EyesSurprised, 1)
            if self.__muzzle:
                self.__muzzle.setTexture(ToonHead.MuzzleSurprised, 1)
            if self.__lpupil:
                self.__lpupil.show()
                self.__rpupil.show()
            if self.__lod500lPupil:
                self.__lod500lPupil.show()
                self.__lod500rPupil.show()
            if self.__lod250lPupil:
                self.__lod250lPupil.show()
                self.__lod250rPupil.show()

    def exitEyelidsSurprised(self):
        if self.__muzzle:
            self.__muzzle.setTexture(ToonHead.Muzzle, 1)

    def setupMuzzles(self, style):
##        self.__muzzle = self.find("**/1000/**/muzzle*")
        self.__muzzles = []
        self.__surpriseMuzzles = []
        self.__angryMuzzles = []
        self.__sadMuzzles = []
        self.__smileMuzzles = []
        self.__laughMuzzles = []

        def hideAddNonEmptyItemToList(item, list):
            if not item.isEmpty():
                # Also hiding the item
                item.hide()
                list.append(item)

        def hideNonEmptyItem(item):
            if not item.isEmpty():
                item.hide()
##                # For AlphaLerp
##                item.setTransparency(True)
##                item.setColor(1,1,1,0)
##                item.setDepthWrite(1)
##                item.setDepthTest(1)

        if (self.hasLOD()):
            # Save the various muzzle LODs.
            for lodName in self.getLODNames():
                animal = style.getAnimal()
                if (animal != 'dog'):
                    muzzle = self.find('**/' + lodName + '/**/muzzle*neutral')
                # Treating the dog separately
                # Explanation: All the animals have their heads and muzzles in the same maya file
                # The dog has its head in the soft file and the muzzles are coming from a respective maya file
                # @TODO Samik 09-05-2008: Remove all this loading muzzle maya files to clean up how the dog is done
                else:
                    muzzle = self.find('**/' + lodName + '/**/muzzle*')
                    if (lodName == '1000') or (lodName == '500'):
                        filePrefix = DogMuzzleDict[style.head]
                        muzzles = loader.loadModel("phase_3" + filePrefix + lodName)
                        if base.config.GetBool('want-new-anims', 1):
                            if not self.find('**/' + lodName + '/**/def_head').isEmpty():
                                muzzles.reparentTo(self.find('**/' + lodName + '/**/def_head'))
                            else:
                                muzzles.reparentTo(self.find('**/' + lodName + '/**/joint_toHead'))
                        elif self.find('**/' + lodName + '/**/joint_toHead'):
                            muzzles.reparentTo(self.find('**/' + lodName + '/**/joint_toHead'))

                surpriseMuzzle = self.find('**/' + lodName + '/**/muzzle*surprise')
                angryMuzzle = self.find('**/' + lodName + '/**/muzzle*angry')
                sadMuzzle = self.find('**/' + lodName + '/**/muzzle*sad')
                smileMuzzle = self.find('**/' + lodName + '/**/muzzle*smile')
                laughMuzzle = self.find('**/' + lodName + '/**/muzzle*laugh')

                self.__muzzles.append(muzzle)
                hideAddNonEmptyItemToList(surpriseMuzzle, self.__surpriseMuzzles)
                hideAddNonEmptyItemToList(angryMuzzle, self.__angryMuzzles)
                hideAddNonEmptyItemToList(sadMuzzle, self.__sadMuzzles)
                hideAddNonEmptyItemToList(smileMuzzle, self.__smileMuzzles)
                hideAddNonEmptyItemToList(laughMuzzle, self.__laughMuzzles)

##                # For AlphaLerp
##                if not muzzle.isEmpty():
##                    muzzle.setTransparency(True)
##                    muzzle.setDepthWrite(1)
##                    muzzle.setDepthTest(1)

        else:
            if style.getAnimal() != 'dog':
                muzzle = self.find('**/muzzle*neutral')
            # Treating the dog separately
            # Explanation: All the animals have their heads and muzzles in the same maya file
            # The dog has its head in the soft file and the muzzles are coming from a respective maya file
            # @TODO Samik 09-05-2008: Remove all this loading muzzle maya files to clean up how the dog is done
            else:
                muzzle = self.find('**/muzzle*')
                filePrefix = DogMuzzleDict[style.head]
                muzzles = loader.loadModel("phase_3" + filePrefix + '1000')
                if base.config.GetBool('want-new-anims', 1):
                    if not self.find('**/def_head').isEmpty():
                        muzzles.reparentTo(self.find('**/def_head'))
                    else:
                        muzzles.reparentTo(self.find('**/joint_toHead'))
                else:
                    muzzles.reparentTo(self.find('**/joint_toHead'))

            surpriseMuzzle = self.find('**/muzzle*surprise')
            angryMuzzle = self.find('**/muzzle*angry')
            sadMuzzle = self.find('**/muzzle*sad')
            smileMuzzle = self.find('**/muzzle*smile')
            laughMuzzle = self.find('**/muzzle*laugh')

            self.__muzzles.append(muzzle)
##            # For AlphaLerp
##            if not muzzle.isEmpty():
##                    muzzle.setTransparency(True)
##                    muzzle.setDepthWrite(1)
##                    muzzle.setDepthTest(1)

            hideAddNonEmptyItemToList(surpriseMuzzle, self.__surpriseMuzzles)
            hideAddNonEmptyItemToList(angryMuzzle, self.__angryMuzzles)
            hideAddNonEmptyItemToList(sadMuzzle, self.__sadMuzzles)
            hideAddNonEmptyItemToList(smileMuzzle, self.__smileMuzzles)
            hideAddNonEmptyItemToList(laughMuzzle, self.__laughMuzzles)

    def getMuzzles(self):
        """
        Return a list of muzzles for each LOD (1000, 500, 250)
        """
        return self.__muzzles

    def getSurpriseMuzzles(self):
        """
        Return a list of surpriseMuzzles for each LOD (1000, 500, 250)
        """
        return self.__surpriseMuzzles

    def getAngryMuzzles(self):
        """
        Return a list of angryMuzzles for each LOD (1000, 500, 250)
        """
        return self.__angryMuzzles

    def getSadMuzzles(self):
        """
        Return a list of sadMuzzles for each LOD (1000, 500, 250)
        """
        return self.__sadMuzzles

    def getSmileMuzzles(self):
        """
        Return a list of smileMuzzles for each LOD (1000, 500, 250)
        """
        return self.__smileMuzzles

    def getLaughMuzzles(self):
        """
        Return a list of laughMuzzles for each LOD (1000, 500, 250)
        """
        return self.__laughMuzzles

    def showNormalMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__muzzles)):
            self.__muzzles[muzzleNum].show()

    def hideNormalMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__muzzles)):
            self.__muzzles[muzzleNum].hide()

    def showAngryMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__angryMuzzles)):
            self.__angryMuzzles[muzzleNum].show()
            self.__muzzles[muzzleNum].hide()

    def hideAngryMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__angryMuzzles)):
            self.__angryMuzzles[muzzleNum].hide()
            self.__muzzles[muzzleNum].show()

    def showSadMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__sadMuzzles)):
            self.__sadMuzzles[muzzleNum].show()
            self.__muzzles[muzzleNum].hide()

    def hideSadMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__sadMuzzles)):
            self.__sadMuzzles[muzzleNum].hide()
            self.__muzzles[muzzleNum].show()

    def showSmileMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__smileMuzzles)):
            self.__smileMuzzles[muzzleNum].show()
            self.__muzzles[muzzleNum].hide()

    def hideSmileMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__smileMuzzles)):
            self.__smileMuzzles[muzzleNum].hide()
            self.__muzzles[muzzleNum].show()

    def showLaughMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__laughMuzzles)):
            self.__laughMuzzles[muzzleNum].show()
            self.__muzzles[muzzleNum].hide()

    def hideLaughMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__laughMuzzles)):
            self.__laughMuzzles[muzzleNum].hide()
            self.__muzzles[muzzleNum].show()

    def showSurpriseMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__surpriseMuzzles)):
            self.__surpriseMuzzles[muzzleNum].show()
            self.__muzzles[muzzleNum].hide()

    def hideSurpriseMuzzle(self):
        if self.isIgnoreCheesyEffect():
            return
        for muzzleNum in range(len(self.__surpriseMuzzles)):
            self.__surpriseMuzzles[muzzleNum].hide()
            self.__muzzles[muzzleNum].show()

    def isIgnoreCheesyEffect(self):
        if hasattr(self, 'savedCheesyEffect'):
            # Do nothing if the Invisible, NoColor, Pumpkin or BigWhite cheesy effect is ON
            if (self.savedCheesyEffect == 10) \
            or (self.savedCheesyEffect == 11) \
            or (self.savedCheesyEffect == 12) \
            or (self.savedCheesyEffect == 13)  \
            or (self.savedCheesyEffect == 14):
                return True
        return False
