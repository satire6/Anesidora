from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.fsm.ClassicFSM import *
from direct.fsm.State import *
from direct.distributed.ClockDelta import globalClockDelta
from otp.avatar import Avatar
from direct.actor import Actor
from direct.task import Task
from toontown.pets import PetDNA
from PetDNA import HeadParts, EarParts, NoseParts, TailParts, BodyTypes, BodyTextures, AllPetColors, getColors, ColorScales, PetEyeColors, EarTextures, TailTextures, getFootTexture, getEarTexture, GiraffeTail, LeopardTail, PetGenders
from toontown.toonbase import  TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.showbase import PythonUtil
import random
import types

"""
from toontown.pets import Pet
p = Pet.Pet()
# dna format [head, ears, nose, tail, body, color, colorScale, eyes, gender]
# NOTE: -1 indicates no part (not valid for texture entires 3-6)
p.setDNA([-1,0,0,-1,2,0,4,0,1]) # fluffy!
p.setName('Smiley')
# show the nametag
p.addActive()
p.reparentTo(render)
p.animFSM.request('neutral')
"""

Component2IconDict = {
    'boredom':'Bored',
    'restlessness':None, #TODO: add this when pets can go indoors; this also needs to choose between Inside and Outside
    'playfulness':'Play',
    'loneliness':'Lonely',
    'sadness':'Sad',
    'fatigue':'Sleepy',
    'hunger':'Hungry',
    'confusion':'Confused',
    'excitement':'Surprised', # TODO: change this to Happy
    'anger':'Angry',
    'surprise':'Surprised',
    'affection':'Love',
    }

class Pet(Avatar.Avatar):
    """Toontown pet"""

    notify = DirectNotifyGlobal.directNotify.newCategory("Pet")

    SerialNum = 0

    Interactions = PythonUtil.Enum('SCRATCH, BEG, EAT, NEUTRAL')
    InteractAnims = { Interactions.SCRATCH: ('toPet', 'pet', 'fromPet'),
                      Interactions.BEG: ('toBeg', 'beg', 'fromBeg'),
                      Interactions.EAT: ('eat', 'swallow', 'neutral'),
                      Interactions.NEUTRAL: 'neutral' }

    def __init__(self, forGui = 0):
        Avatar.Avatar.__init__(self)
        self.serialNum = Pet.SerialNum
        Pet.SerialNum += 1
        self.lockedDown = 0
        self.setPickable(1)
        self.setPlayerType(NametagGroup.CCNonPlayer)
        self.animFSM = ClassicFSM('petAnimFSM',
                                  [State('off', self.enterOff, self.exitOff),
                                   State('neutral', self.enterNeutral, self.exitNeutral),
                                   State('neutralHappy', self.enterNeutralHappy, self.exitNeutralHappy),
                                   State('neutralSad', self.enterNeutralSad, self.exitNeutralSad),
                                   State('run', self.enterRun, self.exitRun),
                                   State('swim', self.enterSwim, self.exitSwim),
                                   State('teleportIn', self.enterTeleportIn, self.exitTeleportOut),
                                   State('teleportOut', self.enterTeleportOut, self.exitTeleportOut),
                                   State('walk', self.enterWalk, self.exitWalk),
                                   State('walkHappy', self.enterWalkHappy, self.exitWalkHappy),
                                   State('walkSad', self.enterWalkSad, self.exitWalkSad),
                                   ],
                                  # init
                                  'off',
                                  # final
                                  'off',
                                  )
        self.animFSM.enterInitialState()
        self.forGui = forGui
        self.moodModel = None
        # probably don't have a name yet
        self.__blinkName = 'petblink-' + str(self.this)
        self.track = None
        self.soundBackflip = None
        self.soundRollover = None
        self.soundPlaydead = None
        self.soundTeleportIn = None
        self.soundTeleportOut = None
        self.teleportHole = None

    def isPet(self):
        return True

    def stopAnimations(self):
        if self.track:
            self.track.pause()
        self.stopBlink()
        self.animFSM.request('off')

    def delete(self):
        self.stopAnimations()
        self.track = None
        self.soundBackflip = None
        self.soundRollover = None
        self.soundPlaydead = None
        self.soundTeleportIn = None
        self.soundTeleportOut = None
        if self.teleportHole:
            self.teleportHole.cleanup()
            self.teleportHole = None
        self.eyesOpenTexture = None
        self.eyesClosedTexture = None
        self.animFSM = None
        self.eyes = None
        self.rightPupil = None
        self.rightHighlight = None
        self.rightBrow = None
        self.leftPupil = None
        self.leftHighlight = None
        self.leftBrow = None
        self.color = None
        Avatar.Avatar.delete(self)

    def getDNA(self):
        return self.style

    def setDNA(self, dna):
        # dna format [head, ears, nose, tail, body, color, eyes, gender]
        if self.style:
            pass
        else:
            # make sure the dna is valid
            assert(len(dna) == PetDNA.NumFields)

            # store the dna
            self.style = dna
            self.generatePet()
            self.generateMoods()

            # this no longer works in the Avatar init!
            # I moved it here for lack of a better place
            # make the drop shadow
            self.initializeDropShadow()
            self.initializeNametag3d()

            # looks a little big
            self.dropShadow.setScale(0.75)

    def generatePet(self):
        """
        create a pet from dna
        """
        self.loadModel('phase_4/models/char/TT_pets-mod')
        self.loadAnims({
                        'toBeg':'phase_5/models/char/TT_pets-intoBeg',
                        'beg':'phase_5/models/char/TT_pets-beg',
                        'fromBeg':'phase_5/models/char/TT_pets-begOut',
                        'backflip':'phase_5/models/char/TT_pets-backflip',
                        'dance':'phase_5/models/char/TT_pets-heal',
                        'toDig':'phase_5/models/char/TT_pets-intoDig',
                        'dig':'phase_5/models/char/TT_pets-dig',
                        'fromDig':'phase_5/models/char/TT_pets-digToNeutral',
                        'disappear':'phase_5/models/char/TT_pets-disappear',
                        'eat':'phase_5.5/models/char/TT_pets-eat',
                        'jump':'phase_5/models/char/TT_pets-jump',
                        'neutral':'phase_4/models/char/TT_pets-neutral',
                        'neutralHappy':'phase_4/models/char/TT_pets-neutralHappy',
                        'neutralSad':'phase_4/models/char/TT_pets-neutral_sad',
                        'toPet':'phase_5.5/models/char/TT_pets-petin',
                        'pet':'phase_5.5/models/char/TT_pets-petloop',
                        'fromPet':'phase_5.5/models/char/TT_pets-petend',
                        'playDead':'phase_5/models/char/TT_pets-playdead',
                        'fromPlayDead':'phase_5/models/char/TT_pets-deadend',
                        'reappear':'phase_5/models/char/TT_pets-reappear',
                        'run':'phase_5.5/models/char/TT_pets-run',
                        'rollover':'phase_5/models/char/TT_pets-rollover',
                        'walkSad':'phase_5.5/models/char/TT_pets-sadwalk',
                        'speak':'phase_5/models/char/TT_pets-speak',
                        'swallow':'phase_5.5/models/char/TT_pets-swallow',
                        'swim':'phase_5.5/models/char/TT_pets-swim',
                        'toBall':'phase_5.5/models/char/TT_pets-toBall',
                        'walk':'phase_5.5/models/char/TT_pets-walk',
                        'walkHappy':'phase_5.5/models/char/TT_pets-walkHappy',
            })
        self.setHeight(2)
        # name is set by user or subclass

        # determine the color
        color = None
        colorIndex = self.style[5]
        color = AllPetColors[colorIndex]
        # remember this for blinks
        self.color = color

        # set the body and foot texture
        bodyType = self.style[4]
        assert(bodyType < len(BodyTypes))
        body = self.find("**/body")
        tex = loader.loadTexture(BodyTextures[BodyTypes[bodyType]])
        tex.setMinfilter(Texture.FTLinear)
        tex.setMagfilter(Texture.FTLinear)
        body.setTexture(tex, 1)
        body.setColor(color)

        # set the appropriate foot texture
        leftFoot = self.find("**/leftFoot")
        rightFoot = self.find("**/rightFoot")
        texName = getFootTexture(bodyType)
        tex = loader.loadTexture(texName)
        tex.setMinfilter(Texture.FTLinear)
        tex.setMagfilter(Texture.FTLinear)
        leftFoot.setTexture(tex, 1)
        rightFoot.setTexture(tex, 1)
        leftFoot.setColor(color)
        rightFoot.setColor(color)

        # stash all parts
        for part in HeadParts + EarParts + NoseParts + TailParts:
            self.find("**/" + part).stash()

        #
        # unstash the appropriate parts
        #

        # scale the color slightly to accent misc. body parts
        colorScale = ColorScales[self.style[6]]
        partColor = self.amplifyColor(color, colorScale)

        headIndex = self.style[0]
        # if we have a head decoration
        if headIndex != -1:
            assert(headIndex < len(HeadParts))
            head = self.find("**/@@" + HeadParts[headIndex])
            head.setColor(partColor)
            head.unstash()

        earsIndex = self.style[1]
        # if we have ears
        if earsIndex != -1:
            assert(earsIndex < len(EarParts))
            ears = self.find("**/@@" + EarParts[earsIndex])
            ears.setColor(partColor)
            texName = getEarTexture(bodyType, EarParts[earsIndex])
            if texName:
                tex = loader.loadTexture(texName)
                tex.setMinfilter(Texture.FTLinear)
                tex.setMagfilter(Texture.FTLinear)
                ears.setTexture(tex, 1)
            ears.unstash()

        noseIndex = self.style[2]
        # if we have a nose
        if noseIndex != -1:
            assert(noseIndex < len(NoseParts))
            nose = self.find("**/@@" + NoseParts[noseIndex])
            nose.setColor(partColor)
            nose.unstash()

        tailIndex = self.style[3]
        # if we have a tail
        if tailIndex != -1:
            assert(tailIndex < len(TailParts))
            tail = self.find("**/@@" + TailParts[tailIndex])
            tail.setColor(partColor)
            texName = TailTextures[TailParts[tailIndex]]
            if texName:
                # check to see if we have a special tail texture
                if BodyTypes[bodyType] == 'giraffe':
                    texName = GiraffeTail
                elif BodyTypes[bodyType] == 'leopard':
                    texName = LeopardTail
                tex = loader.loadTexture(texName)
                tex.setMinfilter(Texture.FTLinear)
                tex.setMagfilter(Texture.FTLinear)
                tail.setTexture(tex, 1)
            tail.unstash()

        # Reorder the eyes so they don't do any Z-fighting with the
        # head or with each other.
        if not self.forGui:
            # In the 3-D world, we can fix the eyes by putting them
            # all in the fixed bin.
            self.drawInFront("eyeWhites", "body", 1)
            self.drawInFront("rightPupil", "eyeWhites", 2)
            self.drawInFront("leftPupil", "eyeWhites", 2)
            self.drawInFront("rightHighlight", "rightPupil", 3)
            self.drawInFront("leftHighlight", "leftPupil", 3)
        else:
            # In the 2-D panel, we have to reparent them.  This also
            # means we have to elevate the priorities on the pupils so
            # they don't inherit the wrong texture from above.
            self.drawInFront("eyeWhites", "body", -2)
            self.drawInFront("rightPupil", "eyeWhites", -2)
            self.drawInFront("leftPupil", "eyeWhites", -2)
            self.find('**/rightPupil').adjustAllPriorities(1)
            self.find('**/leftPupil').adjustAllPriorities(1)

        # set eye color
        eyes = self.style[7]
        eyeColor = PetEyeColors[eyes]
        self.eyes = self.find("**/eyeWhites")
        self.rightPupil = self.find("**/rightPupil")
        self.leftPupil = self.find("**/leftPupil")
        self.rightHighlight = self.find("**/rightHighlight")
        self.leftHighlight = self.find("**/leftHighlight")
        self.rightBrow = self.find("**/rightBrow")
        self.leftBrow = self.find("**/leftBrow")

        self.eyes.setColor(1, 1,1, 1)
        # we need to increase priority on eyeColor so pupils show
        self.rightPupil.setColor(eyeColor, 2)
        self.leftPupil.setColor(eyeColor, 2)
        self.rightHighlight.setColor(1, 1, 1, 1)
        self.leftHighlight.setColor(1, 1, 1, 1)
        self.rightBrow.setColor(0, 0, 0, 1)
        self.leftBrow.setColor(0, 0, 0, 1)

        self.eyes.setTwoSided(1, 1)
        self.rightPupil.setTwoSided(1, 1)
        self.leftPupil.setTwoSided(1, 1)
        self.rightHighlight.setTwoSided(1, 1)
        self.leftHighlight.setTwoSided(1, 1)
        self.rightBrow.setTwoSided(1, 1)
        self.leftBrow.setTwoSided(1, 1)

        if self.forGui:
            # HACK: highlights look awful in the GUI
            # There is probably a way to make them look better
            # but for know. Bye bye...
            self.rightHighlight.hide()
            self.leftHighlight.hide()

        # set eye texture based on gender
        if self.style[8]:
            self.eyesOpenTexture = loader.loadTexture('phase_4/maps/BeanEyeBoys2.jpg',
                                                      'phase_4/maps/BeanEyeBoys2_a.rgb')
            self.eyesClosedTexture = loader.loadTexture('phase_4/maps/BeanEyeBoysBlink.jpg',
                                                        'phase_4/maps/BeanEyeBoysBlink_a.rgb',)
        else:
            self.eyesOpenTexture = loader.loadTexture('phase_4/maps/BeanEyeGirlsNew.jpg',
                                                      'phase_4/maps/BeanEyeGirlsNew_a.rgb',)
            self.eyesClosedTexture = loader.loadTexture('phase_4/maps/BeanEyeGirlsBlinkNew.jpg',
                                                        'phase_4/maps/BeanEyeGirlsBlinkNew_a.rgb')

        self.eyesOpenTexture.setMinfilter(Texture.FTLinear)
        self.eyesOpenTexture.setMagfilter(Texture.FTLinear)

        self.eyesClosedTexture.setMinfilter(Texture.FTLinear)
        self.eyesClosedTexture.setMagfilter(Texture.FTLinear)
        self.eyesOpen()

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)

        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def amplifyColor(self, color, scale):
        color = color * scale
        for i in (0,1,2):
            if color[i] > 1.0:
                color.setCell(i, 1.0)
        return color

    def generateMoods(self):
        # load the emoticon models
        moodIcons = loader.loadModel('phase_4/models/char/petEmotes')
        self.moodIcons = self.attachNewNode('moodIcons')
        # set Z
        self.moodIcons.setScale(2.0)
        self.moodIcons.setZ(3.65)
        moods = moodIcons.findAllMatches("**/+GeomNode")
        for moodNum in range(0, moods.getNumPaths()):
            mood = moods.getPath(moodNum)
            mood.reparentTo(self.moodIcons)
            # set billboard
            mood.setBillboardPointEye()
            mood.hide()

    def clearMood(self):
        if self.moodModel:
            self.moodModel.hide()
        self.moodModel = None

    def showMood(self, mood):

        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds and (not mood=="confusion"):
                self.speakMood(mood)
                return
            else:
                self.clearChat()      
        else:
            self.clearChat()       

        # the model uses caps
        mood = Component2IconDict[mood]
        if mood is None:
            moodModel = None
        else:
            moodModel = self.moodIcons.find("**/*" + mood + "*")
            # make sure we found a model
            if moodModel.isEmpty():
                self.notify.warning("No such mood!: %s" % (mood))
                return
        # make sure the mood has actually changed
        if self.moodModel == moodModel:
            return
        # hide the old mood
        if self.moodModel:
            self.moodModel.hide()
        # set the new mood
        self.moodModel = moodModel

        if self.moodModel:
            self.moodModel.show()

    def speakMood(self, mood):
        """ 
        The Doodle speaks for April Toons' Week.
        """
        if self.moodModel:
            self.moodModel.hide()
            
        if base.config.GetBool('want-speech-bubble', 1):
            self.nametag.setChat(random.choice(TTLocalizer.SpokenMoods[mood]), CFSpeech)
        else:
            self.nametag.setChat(random.choice(TTLocalizer.SpokenMoods[mood]), CFThought)  # Note: Use CFTimeout?

    def getGenderString(self):
        if self.style:
            if self.style[8]:
                return TTLocalizer.GenderShopBoyButtonText
            else:
                return TTLocalizer.GenderShopGirlButtonText

    def getShadowJoint(self):
        if hasattr(self, "shadowJoint"):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            self.shadowJoint = self
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def getNametagJoints(self):
        """
        Return the CharacterJoint that animates the nametag, in a list.
        """
        joints = []
        bundle = self.getPartBundle('modelRoot')
        joint = bundle.findChild('attachNametag')
        if joint:
            joints.append(joint)
        return joints

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
            # Turn on depth write and test.
            self.getGeomNode().setDepthWrite(1)
            self.getGeomNode().setDepthTest(1)
        else:
            h = 0
        # Find dimension
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = (maxDim+0.0)/biggest
        # find midpoint
        mid = (p1 + d/2.0) * s
        # We must push the head a distance forward in Y so it doesn't
        # intersect the near plane, which is incorrectly set to 0 in
        # DX for some reason.
        self.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2],
                            h, 0, 0,
                            s, s, s)

    def makeRandomPet(self):
        dna = PetDNA.getRandomPetDNA()
        self.setDNA(dna)

    # animFSM states

    # Note there are not states for all anim cycles. Just the ones trackAnim2Speed might trigger

    def enterOff(self):
        self.stop()

    def exitOff(self):
        pass

    def enterBall(self):
        self.setPlayRate(1, 'toBall')
        self.play('toBall')
        # TODO: ball neutral

    def exitBall(self):
        self.setPlayRate(-1, 'toBall')
        self.play('toBall')


    def enterBackflip(self):
        self.play('backflip')

    def exitBackflip(self):
        self.stop('backflip')

    def enterBeg(self):
        delay = self.getDuration('toBeg')
        self.track = Sequence(Func(self.play, 'toBeg'),
                          Wait(delay),
                          Func(self.loop, 'beg')
                          )
        self.track.start()

    def exitBeg(self):
        self.track.pause()
        self.play('fromBeg')

    def enterEat(self):
        self.loop('eat')

    def exitEat(self):
        self.stop('swallow')

    def enterDance(self):
        self.loop('dance')

    def exitDance(self):
        self.stop('dance')

    def enterNeutral(self):
        # make the neutral start at a random frame
        anim = 'neutral'
        self.pose(anim, random.choice(range(0, self.getNumFrames(anim))))
        self.loop(anim, restart=0)

    def exitNeutral(self):
        self.stop('neutral')

    def enterNeutralHappy(self):
        # make the happy neutral start at a random frame
        anim = 'neutralHappy'
        self.pose(anim, random.choice(range(0, self.getNumFrames(anim))))
        self.loop(anim, restart=0)

    def exitNeutralHappy(self):
        self.stop('neutralHappy')

    def enterNeutralSad(self):
        # make the sad neutral start at a random frame
        anim = 'neutralSad'
        self.pose(anim, random.choice(range(0, self.getNumFrames(anim))))
        self.loop(anim, restart=0)

    def exitNeutralSad(self):
        self.stop('neutralSad')

    def enterRun(self):
        self.loop('run')

    def exitRun(self):
        self.stop('run')

    def enterSwim(self):
        self.loop('swim')

    def exitSwim(self):
        self.stop('swim')

    def getTeleportInTrack(self):
        if not self.teleportHole:
            self.teleportHole = Actor.Actor('phase_3.5/models/props/portal-mod',
                                    {'hole': 'phase_3.5/models/props/portal-chan'})
        track = Sequence(
            Wait(1.0),
            Parallel(self.getTeleportInSoundInterval(),
                     Sequence(Func(self.showHole),
                              ActorInterval(self.teleportHole, 'hole', startFrame = 81,
                                            endFrame = 71),
                              ActorInterval(self, 'reappear'),
                              ActorInterval(self.teleportHole, 'hole', startFrame = 71,
                                            endFrame = 81),
                              Func(self.cleanupHole),
                              Func(self.loop, "neutral")
                              ),
                     Sequence(Func(self.dropShadow.hide),
                              Wait(1.0),
                              Func(self.dropShadow.show)
                              )
                     )
            )

        return track

    def enterTeleportIn(self, timestamp):
        self.track = self.getTeleportInTrack()
        self.track.start(globalClockDelta.localElapsedTime(timestamp))

    def exitTeleportIn(self):
         self.track.pause()

    def getTeleportOutTrack(self):
        if not self.teleportHole:
            self.teleportHole = Actor.Actor('phase_3.5/models/props/portal-mod',
                                    {'hole': 'phase_3.5/models/props/portal-chan'})
        track = Sequence(
            Wait(1.0),
            Parallel(self.getTeleportOutSoundInterval(),
                     Sequence(ActorInterval(self, 'toDig'),
                              Parallel(ActorInterval(self, 'dig'),
                                       Func(self.showHole),
                                       ActorInterval(self.teleportHole, 'hole', startFrame = 81,
                                                     endFrame = 71)),
                               ActorInterval(self, 'disappear'),
                               ActorInterval(self.teleportHole, 'hole', startFrame = 71,
                                             endFrame = 81),
                               Func(self.cleanupHole)
                               ),
                      Sequence(Wait(1.0),
                               Func(self.dropShadow.hide)
                               )
                      )
            )
        return track

    def enterTeleportOut(self, timestamp):
        self.track = self.getTeleportOutTrack()
        self.track.start(globalClockDelta.localElapsedTime(timestamp))

    def exitTeleportOut(self):
        self.track.pause()

    # teleport utility methods
    def showHole(self):
        if self.teleportHole:
            self.teleportHole.setBin('shadow', 0)
            self.teleportHole.setDepthTest(0)
            self.teleportHole.setDepthWrite(0)
            self.teleportHole.reparentTo(self)
            self.teleportHole.setScale(0.75)
            self.teleportHole.setPos(0,-1,0)

    def cleanupHole(self):
        if self.teleportHole:
            self.teleportHole.reparentTo(hidden)
            self.teleportHole.clearBin()
            self.teleportHole.clearDepthTest()
            self.teleportHole.clearDepthWrite()

    def getTeleportInSoundInterval(self):
        if not self.soundTeleportIn:
            self.soundTeleportIn = loader.loadSfx('phase_5/audio/sfx/teleport_reappear.mp3')
        return SoundInterval(self.soundTeleportIn)

    def getTeleportOutSoundInterval(self):
        if not self.soundTeleportOut:
            self.soundTeleportOut = loader.loadSfx('phase_5/audio/sfx/teleport_disappear.mp3')
        return SoundInterval(self.soundTeleportOut)

    def enterWalk(self):
        self.loop('walk')

    def exitWalk(self):
        self.stop('walk')

    def enterWalkHappy(self):
        self.loop('walkHappy')

    def exitWalkHappy(self):
        self.stop('walkHappy')

    def enterWalkSad(self):
        self.loop('walkSad')

    def exitWalkSad(self):
        self.stop('walkSad')

    # make animation match motion of character
    def trackAnimToSpeed(self, forwardVel, rotVel, inWater=0):
        # call this with a forward and rotational velocity every frame
        # to automatically update the pet's animation

        # what is the pet doing?
        action = 'neutral'
        if self.isInWater():
            # tread water
            action = 'swim'
        elif (forwardVel > .1) or (abs(rotVel) > .1):
            action = 'walk'

        self.setAnimWithMood(action)

    def setAnimWithMood(self, action):
        # how are they doing the action?
        how = ''
        if self.isExcited():
            how = 'Happy'
        elif self.isSad():
            how = 'Sad'

        if action == 'swim':
            anim = action
        else:
            anim = '%s%s' % (action, how)
        if anim != self.animFSM.getCurrentState().getName():
            self.animFSM.request(anim)

    # override if desired
    def isInWater(self):
        return 0
    def isExcited(self):
        return 0
    def isSad(self):
        return 0

    def startTrackAnimToSpeed(self):
        self.lastPos = self.getPos(render)
        self.lastH = self.getH(render)
        taskMgr.add(self._trackAnimTask, self.getTrackAnimTaskName())
    def stopTrackAnimToSpeed(self):
        taskMgr.remove(self.getTrackAnimTaskName())
        del self.lastPos
        del self.lastH
    def getTrackAnimTaskName(self):
        return 'trackPetAnim-%s' % self.serialNum
    def _trackAnimTask(self, task):
        curPos = self.getPos(render)
        curH = self.getH(render)
        self.trackAnimToSpeed(curPos - self.lastPos, curH - self.lastH)
        self.lastPos = curPos
        self.lastH = curH
        return Task.cont

    # blinks
    def __blinkOpen(self, task):
        self.eyesOpen()
        r = random.random()
        if r < 0.1:
            t = 0.2
        else:
            t = r * 4.0 + 1
        taskMgr.doMethodLater(t, self.__blinkClosed, self.__blinkName)
        return Task.done

    def __blinkClosed(self, task):
        self.eyesClose()
        taskMgr.doMethodLater(0.125, self.__blinkOpen, self.__blinkName)
        return Task.done

    def startBlink(self):
        taskMgr.remove(self.__blinkName)
        self.eyesOpen()
        t = random.random() * 4.0 + 1
        taskMgr.doMethodLater(t, self.__blinkClosed, self.__blinkName)

    def stopBlink(self):
        taskMgr.remove(self.__blinkName)
        self.eyesOpen()

    def eyesOpen(self):
        self.eyes.setColor(1, 1, 1, 1)
        self.eyes.setTexture(self.eyesOpenTexture, 1)
        self.rightPupil.show()
        self.leftPupil.show()
        if not self.forGui:
            self.rightHighlight.show()
            self.leftHighlight.show()

    def eyesClose(self):
        self.eyes.setColor(self.color)
        self.eyes.setTexture(self.eyesClosedTexture, 1)
        self.rightPupil.hide()
        self.leftPupil.hide()
        if not self.forGui:
            self.rightHighlight.hide()
            self.leftHighlight.hide()

    def lockPet(self):
        # call this when you need to lock the pet down in order to play
        # a movie on him
        if not self.lockedDown:
            self.prevAnimState = self.animFSM.getCurrentState().getName()
            # if the movie doesn't do anything, the pet is going to stop moving.
            # put him in neutral
            self.animFSM.request('neutral')
        self.lockedDown += 1

    def isLockedDown(self):
        return self.lockedDown != 0

    def unlockPet(self):
        # call this when you're done playing the movie
        assert (self.lockedDown)
        self.lockedDown -= 1
        if not self.lockedDown:
            # make sure the pet is playing the same animation that it was
            # playing when we locked it down
            self.animFSM.request(self.prevAnimState)
            self.prevAnimState = None

    def getInteractIval(self, interactId):
        anims = self.InteractAnims[interactId]
        #print "getInteractIval: anims = ", anims
        if type(anims) == types.StringType:
            animIval = ActorInterval(self, anims)
        else:
            animIval = Sequence()
            for anim in anims:
                animIval.append(ActorInterval(self, anim))
        return animIval

# test only
def gridPets():
    pets = []
    offsetX = 0
    offsetY = 0
    startPos = base.localAvatar.getPos()
    for body in range(0, len(BodyTypes)):
        colors = getColors(body)
        for color in colors:
            p = Pet()
            p.setDNA([random.choice(range(-1, len(HeadParts))),
                      random.choice(range(-1, len(EarParts))),
                      random.choice(range(-1, len(NoseParts))),
                      random.choice(range(-1, len(TailParts))),
                      body,
                      color,
                      random.choice(range(-1, len(ColorScales))),
                      random.choice(range(0, len(PetEyeColors))),
                      random.choice(range(0, len(PetGenders))),
                      ]
                     )
            p.setPos(startPos[0] + offsetX, startPos[1] + offsetY, startPos[2])
            p.animFSM.request('neutral')
            p.reparentTo(render)
            pets.append(p)
            offsetX += 3
        offsetY += 3
        offsetX = 0
    return pets
