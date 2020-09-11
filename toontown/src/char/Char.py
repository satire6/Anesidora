"""Char module: contains the Char class"""

from otp.avatar import Avatar
from pandac.PandaModules import *
from direct.task import Task
import random
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal

AnimDict = {
    "mk": (("walk", "walk", 3),
           ("run", "run", 3),
           ("neutral", "wait", 3),
           ("left-point-start", "left-start", 3.5),
           ("left-point", "left", 3.5),
           ("right-point-start", "right-start", 3.5),
           ("right-point", "right", 3.5),
           ),
    "vmk": (("walk", "sneak", 3),
             ("run", "run", 3),
             ("neutral", "idle", 3),
             ("sneak", "sneak",3),
             ("into_sneak", "into_sneak", 3),
             ("chat", "run", 3),
             ("into_idle", "into_idle", 3),
             ),
    "wmn":(("walk", "walkHalloween3", 3),
                ("neutral", "neutral2", 3),
             ),
    "mn": (("walk", "walk", 3),
           ("run", "run", 3),
           ("neutral", "wait", 3),
           ("left-point-start", "start-Lpoint", 3.5),
           ("left-point", "Lpoint", 3.5),
           ("right-point-start", "start-Rpoint", 3.5),
           ("right-point", "Rpoint", 3.5),
           ("up", "up", 4),
           ("down", "down", 4),
           ("left", "left", 4),
           ("right", "right", 4),
           ),
    "g": (("walk", "Walk", 6),
          ("run", "Run", 6),
          ("neutral", "Wait", 6),
          ),
    "sg": (("walk", "walkStrut2", 6),
              ("neutral", "neutral", 6),
            ),
    "d": (("walk", "walk", 6),
          ("trans", "transition", 6),
          ("neutral", "neutral", 6),
          ("trans-back", "transBack", 6),
          ),
    "dw": (("wheel", "wheel", 6),
              ("neutral", "wheel", 6),
           ),
    "p": (("walk", "walk", 6),
          ("sit", "sit", 6),
          ("neutral", "neutral", 6),
          ("stand", "stand", 6),
          ),
    "wp": (("walk", "walk", 6),
             ("sit", "sitStart", 6),
             ("neutral", "sitLoop", 6),
             ("stand", "sitStop", 6),
             ),
    "cl":(),
    "dd" : (("walk", "walk", 4),
          ("neutral", "idle", 4),
          ),
    "ch" : (("walk", "walk", 6),
          ("neutral", "idle", 6),
          ),
    "da" : (("walk", "walk", 6),
          ("neutral", "idle", 6),
          ),
    }

ModelDict = {
    "mk": "phase_3/models/char/mickey-",
    "vmk": "phase_3.5/models/char/tt_a_chr_csc_mickey_vampire_",
    "mn": "phase_3/models/char/minnie-",
    "wmn" : "phase_3.5/models/char/tt_a_chr_csc_witchMinnie_",
    "g" : "phase_6/models/char/TT_G",
    "sg" : "phase_6/models/char/tt_a_chr_csc_goofyCostume_",
    "d" : "phase_6/models/char/DL_donald-",
    "dw": "phase_6/models/char/donald-wheel-",
    "p" : "phase_6/models/char/pluto-",
    "wp" : "phase_6/models/char/tt_a_chr_csc_plutoCostume_",
    "cl": "phase_5.5/models/estate/Clara_pose2-",
    "dd": "phase_4/models/char/daisyduck_",
    "ch": "phase_6/models/char/chip_",
    "da": "phase_6/models/char/dale_",
    }



LODModelDict = {
    "mk": [1200, 800, 400],
    "vmk": [1200, 800, 400],
    "wmn": [1200, 800, 400],
    "mn": [1200, 800, 400],
    "g" : [1500, 1000, 500],
    "sg": [1200, 800, 400],
    "d" : [1000, 500, 250],
    "dw": [1000],
    "p" : [1000, 500, 300],
    "wp" : [1200, 800, 400],
    "cl": [],
    "dd" : [1600, 800, 400],
    "ch" : [1000, 500, 250],
    "da" : [1000, 500, 250],
    }

class Char(Avatar.Avatar):
    """
    A Char is not a player toon.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("Char")

    def __init__(self):
        try:
            self.Char_initialized
        except:
            self.Char_initialized = 1
            Avatar.Avatar.__init__(self)

            # Characters are generally not pickable.  You can't make
            # friends with Mickey!
            self.setPickable(0)

            # Chars are generally non-player avatars.
            self.setPlayerType(NametagGroup.CCNonPlayer)

            self.dialogueArray =  []
            self.chatterArray = [[], [], []]

    def delete(self):
        try:
            self.Char_deleted
        except:
            self.Char_deleted = 1
            self.unloadDialogue()

            Avatar.Avatar.delete(self)

    def updateCharDNA(self, newDNA):
        """updateCharDNA(self, AvatarDNA)
        update the char's appearance based on new DNA
        """
        if (newDNA.name != self.style.name):
            self.swapCharModel(newDNA)

    def setDNAString(self, dnaString):
        newDNA = CharDNA.CharDNA()
        newDNA.makeFromNetString(dnaString)
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.style:
            self.updateCharDNA(dna)
        else:
            # store the DNA
            self.style = dna

            self.generateChar()

            # this no longer works in the Avatar init!
            # I moved it here for lack of a better place
            # make the drop shadow
            self.initializeDropShadow()
            self.initializeNametag3d()
            self.nametag3d.setBin('fixed', 0)

            # fix Chip and Dales wonky shadow
            if (self.name == "chip") or (self.name == "dale"):
                self.find("**/drop-shadow").setScale(0.33)


    def setLODs(self):
        """
        Get LOD switch distances from dconfig, or use defaults
        """
        # set up the LOD node for avatar LOD
        self.setLODNode()

        # get the switch values
        levelOneIn = base.config.GetInt("lod1-in", 50)
        levelOneOut = base.config.GetInt("lod1-out", 1)
        levelTwoIn = base.config.GetInt("lod2-in", 100)
        levelTwoOut = base.config.GetInt("lod2-out", 50)
        levelThreeIn = base.config.GetInt("lod3-in", 280)
        levelThreeOut = base.config.GetInt("lod3-out", 100)

        # add the LODs
        self.addLOD(LODModelDict[self.style.name][0], levelOneIn, levelOneOut)
        self.addLOD(LODModelDict[self.style.name][1], levelTwoIn, levelTwoOut)
        self.addLOD(LODModelDict[self.style.name][2], levelThreeIn, levelThreeOut)

    def generateChar(self):
        """
        Create a non-player character from dna (an array of strings)
        """
        dna = self.style
        self.name = dna.getCharName()
        self.geoEyes = 0
        # generate the LOD nodes, if necessary
        if (len(LODModelDict[dna.name]) > 1):
            self.setLODs()
        filePrefix = ModelDict[dna.name]
        if (self.name == "mickey"):
            height = 3.0
        elif (self.name == "vampire_mickey"):
            height = 3.0
        elif (self.name == "minnie"):
            height = 3.0
        elif (self.name == "witch_minnie"):
            height = 3.0
        elif (self.name == "goofy"):
            height = 4.8
        elif (self.name == "super_goofy"):
            height = 4.8
        elif (self.name == "donald" or self.name == "donald-wheel"):
            height = 4.5
        elif (self.name == "daisy"):
            height = 4.5
        elif (self.name == "pluto"):
            height = 3.0
        elif (self.name == "western_pluto"):
            height = 4.5
        elif (self.name == "clarabelle"):
            height = 3.0
        elif (self.name == "chip"):
            height = 2.0
        elif (self.name == "dale"):
            height = 2.0

        self.lodStrings = []
        for lod in LODModelDict[self.style.name]:
            self.lodStrings.append(str(lod))

        if self.lodStrings:
            for lodStr in self.lodStrings:
                if (len(self.lodStrings) > 1):
                    lodName = lodStr
                else:
                    lodName = "lodRoot"
                if(self.name == "goofy"):
                    self.loadModel(filePrefix + "-" + lodStr, lodName=lodName)
                else:
                    self.loadModel(filePrefix + lodStr, lodName=lodName)
        else:
            self.loadModel(filePrefix)

        animDict = {}

        animList = AnimDict[self.style.name]
        for anim in animList:
            # anim files may be in different phases
            animFilePrefix = filePrefix[:6] + str(anim[2]) + filePrefix[7:]
            animDict[anim[0]] = animFilePrefix + anim[1]

        # The animations are loaded when used
        for lodStr in self.lodStrings:
            if (len(self.lodStrings) > 1):
                lodName = lodStr
            else:
                lodName = "lodRoot"
            self.loadAnims(animDict, lodName=lodName)

        self.setHeight(height)

        self.loadDialogue(dna.name)

        # set up the mouse ears for rotation
        self.ears = []
        # or self.name == "vampire_mickey"
        if (self.name == "mickey" or self.name == "vampire_mickey" \
            or self.name == "minnie"):
            # Clear the net transforms first, in case we have
            # merge-lod-bundles on (which would mean this is really
            # just one bundle).
            for bundle in self.getPartBundleDict().values():
                bundle = bundle['modelRoot'].getBundle()
                earNull = bundle.findChild("sphere3")
                if not earNull:
                    earNull = bundle.findChild("*sphere3")
                earNull.clearNetTransforms()

            for bundle in self.getPartBundleDict().values():
                charNodepath = bundle['modelRoot'].partBundleNP
                bundle = bundle['modelRoot'].getBundle()
                earNull = bundle.findChild("sphere3")
                if not earNull:
                    earNull = bundle.findChild("*sphere3")
                # import pdb; pdb.set_trace()
                ears = charNodepath.find("**/sphere3")
                if ears.isEmpty():
                    ears = charNodepath.find("**/*sphere3")
                ears.clearEffect(CharacterJointEffect.getClassType())
                earRoot = charNodepath.attachNewNode("earRoot")
                earPitch = earRoot.attachNewNode("earPitch")
                earPitch.setP(40.)
                ears.reparentTo(earPitch)
                # put animation channel on ear root
                earNull.addNetTransform(earRoot.node())
                ears.clearMat()
                # bake in the reverse pitch
                ears.node().setPreserveTransform(ModelNode.PTNone)
                ears.setP(-40.)
                ears.flattenMedium()
                self.ears.append(ears)
                # now make the ears rotate to the camera at this pitch.
                ears.setBillboardAxis()
                
        # set up the blinking eyes
        self.eyes = None
        self.lpupil = None
        self.rpupil = None
        self.eyesOpen = None
        self.eyesClosed = None

        if (self.name == "mickey" or self.name == "minnie"):
            self.eyesOpen = loader.loadTexture("phase_3/maps/eyes1.jpg",
                                               "phase_3/maps/eyes1_a.rgb")
            self.eyesClosed = loader.loadTexture(
                "phase_3/maps/mickey_eyes_closed.jpg",
                "phase_3/maps/mickey_eyes_closed_a.rgb")
                # TODO: other LODs
            self.eyes = self.find("**/1200/**/eyes")
            # this fixes a dual-mode transparency problem
            # that makes the pupils render poorly
            self.eyes.setBin('transparent', 0)
            self.lpupil = self.find("**/1200/**/joint_pupilL")
            self.rpupil = self.find("**/1200/**/joint_pupilR")
            # make them render correctly
            for lodName in self.getLODNames():
                self.drawInFront("joint_pupil?", "eyes*", -3, lodName=lodName)
        elif (self.name == "witch_minnie" or self.name == "vampire_mickey" \
                or self.name == "super_goofy" or self.name == "western_pluto"):
            self.geoEyes = 1
            self.eyeOpenList = []
            self.eyeCloseList = []
            
            if(self.find("**/1200/**/eyesOpen").isEmpty()):
                self.eyeCloseList.append(self.find("**/eyesClosed"))
                self.eyeOpenList.append(self.find("**/eyesOpen"))
            else:
                self.eyeCloseList.append(self.find("**/1200/**/eyesClosed"))
                self.eyeOpenList.append(self.find("**/1200/**/eyesOpen"))

            for part in self.eyeOpenList:
                part.show()

            for part in self.eyeCloseList:
                part.hide()
        elif (self.name == "pluto"):
            self.eyesOpen = loader.loadTexture(
                "phase_6/maps/plutoEyesOpen.jpg",
                "phase_6/maps/plutoEyesOpen_a.rgb")
            self.eyesClosed = loader.loadTexture(
                "phase_6/maps/plutoEyesClosed.jpg",
                "phase_6/maps/plutoEyesClosed_a.rgb")
            # TODO: other LODs
            self.eyes = self.find("**/1000/**/eyes")
            self.lpupil = self.find("**/1000/**/joint_pupilL")
            self.rpupil = self.find("**/1000/**/joint_pupilR")
            # make them render correctly
            for lodName in self.getLODNames():
                self.drawInFront("joint_pupil?", "eyes*", -3, lodName=lodName)
        elif (self.name == "daisy"):
            self.geoEyes = 1
            self.eyeOpenList = []
            self.eyeCloseList = []

            self.eyeCloseList.append(self.find("**/1600/**/eyesclose"))
            self.eyeCloseList.append(self.find("**/800/**/eyesclose"))

            self.eyeOpenList.append(self.find("**/1600/**/eyesclose"))
            self.eyeOpenList.append(self.find("**/800/**/eyesclose"))
            self.eyeOpenList.append(self.find("**/1600/**/eyespupil"))
            self.eyeOpenList.append(self.find("**/800/**/eyespupil"))
            self.eyeOpenList.append(self.find("**/1600/**/eyesopen"))
            self.eyeOpenList.append(self.find("**/800/**/eyesopen"))

            for part in self.eyeOpenList:
                part.show()

            for part in self.eyeCloseList:
                part.hide()

        elif (self.name == "donald-wheel"):
            # set them up for blinking
            self.eyes = self.find("**/eyes")
            self.lpupil = self.find("**/joint_pupilL")
            self.rpupil = self.find("**/joint_pupilR")
            # arrange donalds eyes to render properly
            self.drawInFront("joint_pupil?", "eyes*", -3)

        elif (self.name == "chip") or (self.name == "dale"):
            self.eyesOpen = loader.loadTexture(
                "phase_6/maps/dale_eye1.jpg",
                "phase_6/maps/dale_eye1_a.rgb")
            self.eyesClosed = loader.loadTexture(
                "phase_6/maps/chip_dale_eye1_blink.jpg",
                "phase_6/maps/chip_dale_eye1_blink_a.rgb")
            self.eyes = self.find("**/eyes")
            self.lpupil = self.find("**/pupil_left")
            self.rpupil = self.find("**/pupil_right")
            # hide the existing blink geom
            self.find("**/blink").hide()

        # TODO: Clarabelle blinking

        # Bump up the override parameter on the pupil
        # textures so they won't get overridden when we set
        # the blink texture.
        if self.lpupil != None:
            self.lpupil.adjustAllPriorities(1)
            self.rpupil.adjustAllPriorities(1)

        if self.eyesOpen:
            self.eyesOpen.setMinfilter(Texture.FTLinear)
            self.eyesOpen.setMagfilter(Texture.FTLinear)
        if self.eyesClosed:
            self.eyesClosed.setMinfilter(Texture.FTLinear)
            self.eyesClosed.setMagfilter(Texture.FTLinear)

        # Fix Mickey's screwed up right pupil until the animators redo
        # Well only fix the highest lod since that is the only one noticeable
        if (self.name == "mickey"):
            pupilParent = self.rpupil.getParent()
            pupilOffsetNode = pupilParent.attachNewNode("pupilOffsetNode")
            pupilOffsetNode.setPos(0, 0.025, 0)
            self.rpupil.reparentTo(pupilOffsetNode)

        self.__blinkName = "blink-" + self.name
        
        #import pdb; pdb.set_trace()

    def swapCharModel(self, charStyle):
        """swapCharModel(Self, string)
        Swap out the current char model for the given one
        """
        # out with the old
        for lodStr in self.lodStrings:
            if (len(self.lodStrings) > 1):
                lodName = lodStr
            else:
                lodName = "lodRoot"
            self.removePart("modelRoot", lodName=lodName)

        # in with the new
        self.setStyle(charStyle)
        self.generateChar()

    def getDialogue(self, type, length):
        """playDialogue(self, string, int)
        Play the specified type of dialogue for the specified time
        """
        # Choose the appropriate sound effect.
        sfxIndex = None
        if (type == "statementA" or type == "statementB"):
            if (length == 1):
                sfxIndex = 0
            elif (length == 2):
                sfxIndex = 1
            elif (length >= 3):
                sfxIndex = 2
        elif (type == "question"):
            sfxIndex = 3
        elif (type == "exclamation"):
            sfxIndex = 4
        elif (type == "special"):
            sfxIndex = 5
        else:
            self.notify.error("unrecognized dialogue type: ", type)

        if sfxIndex != None and sfxIndex < len(self.dialogueArray) and \
           self.dialogueArray[sfxIndex] != None:
            return self.dialogueArray[sfxIndex]
        else:
            return None

    def playDialogue(self, type, length, delay = None):
        dialogue = self.getDialogue(type, length)
        base.playSfx(dialogue)

    def getChatterDialogue(self, category, msg):
        try:
            return self.chatterArray[category][msg]
        except IndexError:
            return None

    def getShadowJoint(self):
        return self.getGeomNode()

    #def getShadowJoints(self): #*
    #    return [self.getGeomNode()]

    def getNametagJoints(self):
        """
        Return the CharacterJoint that animates the nametag, in a list.
        """
        # Chars don't animate their nametags.
        return []


    def loadChatterDialogue(self, name, audioIndexArray,
                            loadPath, language):
        """
        Load the dialogue audio samples
        """
        # load the audio files and store into the dialogue array
        chatterTypes = ['greetings', 'comments', 'goodbyes']
        for categoryIndex in range(len(audioIndexArray)):
            chatterType = chatterTypes[categoryIndex]
            for fileIndex in audioIndexArray[categoryIndex]:
                if fileIndex:
                    self.chatterArray[categoryIndex].append(
                        base.loadSfx("%s/CC_%s_chatter_%s%02d.mp3" %
                                     (loadPath, name, chatterType, fileIndex))
                        )
                else:
                    # Just in case you have non contiguous chatter files
                    self.chatterArray[categoryIndex].append(None)

    def loadDialogue(self, char):
        """
        Load the dialogue audio samples
        """
        if self.dialogueArray:
            # We've already got a dialogueArray loaded.
            self.notify.warning("loadDialogue() called twice.")

        self.unloadDialogue()

        language = base.config.GetString("language", "english")

        if (char == "mk"):
            # load Mickey's dialogue array
            dialogueFile = base.loadSfx("phase_3/audio/dial/mickey.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            # load Mickey's chatter
            if language == 'japanese':
                chatterIndexArray = (
                    # Greetings
                    [1,2],
                    # Comments
                    [1,2,3,4],
                    # Goodbyes
                    [1,2,3,4,5],
                    )
                self.loadChatterDialogue("mickey", chatterIndexArray,
                                         "phase_3/audio/dial", language)
        elif (char == "vmk"):
            # load Mickey's dialogue array
            dialogueFile = base.loadSfx("phase_3/audio/dial/mickey.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            # load Mickey's chatter
            if language == 'japanese':
                chatterIndexArray = (
                    # Greetings
                    [1,2],
                    # Comments
                    [1,2,3,4],
                    # Goodbyes
                    [1,2,3,4,5],
                    )
                self.loadChatterDialogue("mickey", chatterIndexArray,
                                         "phase_3/audio/dial", language)
        elif (char == "mn" or char == "wmn"):
            # load Minnie's dialogue array
            dialogueFile = base.loadSfx("phase_3/audio/dial/minnie.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            # load Minnie's chatter
            if language == 'japanese':
                chatterIndexArray = (
                    # Greetings
                    [1,2],
                    # Comments
                    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                    # Goodbyes
                    [1,2,3],
                    )
                self.loadChatterDialogue("minnie", chatterIndexArray,
                                         "phase_3/audio/dial", language)
        elif (char == "dd"):
            # load Daisy's dialogue array
            dialogueFile = base.loadSfx("phase_4/audio/dial/daisy.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            # load Diasy's chatter
            if language == 'japanese':
                chatterIndexArray = (
                    # Greetings
                    [1,2,3],
                    # Comments
                    [1,2,3,4,5,6,7,8,9,10,11,12],
                    # Goodbyes
                    [1,2,3,4],
                    )
                self.loadChatterDialogue("daisy", chatterIndexArray,
                                         "phase_8/audio/dial", language)
        elif (char == "g" or char == "sg"):
            # load Goofy's dialogue array
            dialogueFile = base.loadSfx("phase_6/audio/dial/goofy.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            # load Goofy's chatter
            if language == 'japanese':
                chatterIndexArray = (
                    # Greetings
                    [1,2,3],
                    # Comments
                    [1,2,3,4,5,6,7,8,9,10,11,12],
                    # Goodbyes
                    [1,2,3,4],
                    )
                self.loadChatterDialogue("goofy", chatterIndexArray,
                                         "phase_6/audio/dial", language)
        elif (char == "d" or char == "dw"):
            # load Donald's dialogue array
            dialogueFile = base.loadSfx("phase_6/audio/dial/donald.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
            if char == 'd':
                # load Donalds's chatter
                if language == 'japanese':
                    chatterIndexArray = (
                        # Greetings
                        [1,2],
                        # Comments
                        [1,2,3,4,5,6,7,8,9,10,11],
                        # Goodbyes
                        [1,2,3,4],
                        )
                    self.loadChatterDialogue("donald", chatterIndexArray,
                                             "phase_6/audio/dial", language)
        elif (char == "p" or char == "wp"):
            # load Pluto's dialogue array
            dialogueFile = base.loadSfx("phase_3.5/audio/dial/AV_dog_med.mp3")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
        elif (char == "cl"):
            # TODO: load Clarabelle's dialog array
            dialogueFile = base.loadSfx("phase_3.5/audio/dial/AV_dog_med.mp3")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
        elif (char == "ch"):
            dialogueFile = base.loadSfx("phase_6/audio/dial/chip.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
        elif (char == "da"):
            dialogueFile = base.loadSfx("phase_6/audio/dial/dale.wav")
            for i in range(0,6):
                self.dialogueArray.append(dialogueFile)
        else:
            self.notify.error("unknown character %s" % char)



    def unloadDialogue(self):
        """
        Unload the dialogue audio samples
        """
        self.dialogueArray =  []
        self.chatterArray = [[], [], []]


    ###
    ### Tasks
    ###

    def __blinkOpenEyes(self, task):
        self.openEyes()
        # Do a double blink every once in a while
        r = random.random()
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
        self.closeEyes()
        taskMgr.doMethodLater(0.125, self.__blinkOpenEyes, self.__blinkName)
        return Task.done

    def openEyes(self):
        if (self.geoEyes):
            for part in self.eyeOpenList:
                part.show()
            for part in self.eyeCloseList:
                part.hide()
        else:
            if self.eyes:
                self.eyes.setTexture(self.eyesOpen, 1)
            self.lpupil.show()
            self.rpupil.show()


    def closeEyes(self):
        if (self.geoEyes):
            for part in self.eyeOpenList:
                part.hide()
            for part in self.eyeCloseList:
                part.show()
        else:
            if self.eyes:
                self.eyes.setTexture(self.eyesClosed, 1)
            self.lpupil.hide()
            self.rpupil.hide()


    def startBlink(self):
        """
        Starts the Blink task.
        """
        if (self.eyesOpen or self.geoEyes):
            # remove any old
            taskMgr.remove(self.__blinkName)
            # spawn the new task
            taskMgr.doMethodLater(random.random() * 4 + 1, self.__blinkCloseEyes, self.__blinkName)

    def stopBlink(self):
        if (self.eyesOpen or self.geoEyes):
            taskMgr.remove(self.__blinkName)
            self.openEyes()

##     def startEarTask(self):
##         if self.ears:
##             def earTask(task):
##                 for ear in self.ears:
##                     ear.headsUp(base.camera)
##                 return Task.cont
##             taskMgr.add(earTask, self.style.getCharName() + "-earTask")

##     def stopEarTask(self):
##         if self.ears:
##             taskMgr.remove(self.style.getCharName() + "-earTask")

    def startEarTask(self):
        # This used to be an actual task that would rotate the ears to
        # the camera every frame.  But on reflection, this is just
        # what a billboard does; so now we just make the ears a
        # billboard (above) and this task doesn't need to exist.
        pass

    def stopEarTask(self):
        pass

    def uniqueName(self, idString):
        return (idString + "-" + str(self.this))
