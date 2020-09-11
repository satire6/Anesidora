"""Toon module: contains the Toon class"""
"""Toon module: contains the Toon class"""

from otp.avatar import Avatar
import ToonDNA
from direct.task.Task import Task
from toontown.suit import SuitDNA
from direct.actor import Actor
import string
from ToonHead import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
import random
from toontown.effects import Wake
import TTEmote
from otp.avatar import Emote
import Motion
from toontown.hood import ZoneUtil
from toontown.battle import SuitBattleGlobals
from otp.otpbase import OTPGlobals
from toontown.effects import DustCloud
from direct.showbase.PythonUtil import Functor
from toontown.distributed import DelayDelete
import types

"""
import Toon
t = Toon.Toon()
import ToonDNA
d = ToonDNA.ToonDNA()
# d.newToon( ('dll', 'md', 'l', 'f') )
d.newToonRandom(gender='f')
t.setDNA(d)
t.loop('neutral')
t.reparentTo(render)
t.setPos(base.localAvatar, 0,0,0)

from pandac.Texture import Texture
shirtTex = loader.loadTexture("/i/beta/toons/maya/work/characterClothing/textures/female_shirt2.rgb")
shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
shirtTex.setMagfilter(Texture.FTLinear)
sleeveTex = loader.loadTexture("/i/beta/toons/maya/work/characterClothing/textures/female_sleeve2.rgb")
sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
sleeveTex.setMagfilter(Texture.FTLinear)
bottomTex = loader.loadTexture("/i/beta/toons/maya/work/characterClothing/textures/female_skirt2.rgb")
bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
bottomTex.setMagfilter(Texture.FTLinear)
for lodName in t.getLODNames():
    thisPart = t.getPart("torso", lodName)
    top = thisPart.find("**/torso-top")
    top.setTexture(shirtTex, 1)
    top.setColor(1,1,1,1)
    sleeves = thisPart.find("**/sleeves")
    sleeves.setTexture(sleeveTex, 1)
    sleeves.setColor(1,1,1,1)
    bottoms = thisPart.findAllMatches("**/torso-bot")
    for bottomNum in range(0, bottoms.getNumPaths()):
        bottom = bottoms.getPath(bottomNum)
        bottom.setTexture(bottomTex, 1)
        bottom.setColor(1,1,1,1)


c = VBase4(0.96875, 0.691406, 0.699219, 1.0)
parts = t.findAllMatches("**/arms")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

parts = t.findAllMatches("**/neck")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

parts = t.findAllMatches("**/torso*")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(1,1,1,1)

parts = t.findAllMatches("**/legs")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

parts = t.findAllMatches("**/feet")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

parts = t.findAllMatches("**/head*")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

parts = t.findAllMatches("**/ear?-*")
for partNum in range(0, parts.getNumPaths()):
    parts.getPath(partNum).setColor(c)

"""

SLEEP_STRING = TTLocalizer.ToonSleepString

# Moved these to OTPGlobals
"""
# Indices into standWalkRunReverse, and also return values from setSpeed().
STAND_INDEX = 0
WALK_INDEX = 1
RUN_INDEX = 2
REVERSE_INDEX = 3
"""

# module vars
DogDialogueArray = []
CatDialogueArray = []
HorseDialogueArray = []
RabbitDialogueArray = []
MouseDialogueArray = []
DuckDialogueArray = []
MonkeyDialogueArray = []
BearDialogueArray = []
PigDialogueArray = []

LegsAnimDict = {}
TorsoAnimDict = {}
HeadAnimDict = {}

Preloaded = []

# list of anims for all toon parts
# create-a-toon
Phase3AnimList = (
    ("neutral", "neutral"),
    ("run", "run"),
    )

# tutorial
Phase3_5AnimList = (
    ("walk", "walk"),
    ("teleport", "teleport"),
    ("book", "book"),
    ("jump", "jump"),
    ("running-jump", "running-jump"),
    ("jump-squat", "jump-zstart"),
    ("jump-idle", "jump-zhang"),
    ("jump-land", "jump-zend"),
    ("running-jump-squat", "leap_zstart"),
    ("running-jump-idle", "leap_zhang"),
    ("running-jump-land", "leap_zend"),
    # squirt (and drop)
    ("pushbutton", "press-button"),
    # throw
    ("throw", "pie-throw"),
    ("victory", "victory-dance"),
    ("sidestep-left", "sidestep-left"),
    # react
    ("conked", "conked"),
    ("cringe", "cringe"),
    # emotes that are available to brand-new toons
    ("wave", "wave"),
    ("shrug", "shrug"),
    ("angry", "angry"),
    ###
    ### Special Animations
    ###
    # tutorial
    ### WARNING: these channels only exist for Flippy!!! (dna: dls, m, m)
    ("tutorial-neutral", "tutorial-neutral"),
    ("left-point", "left-point"),
    ("right-point", "right-point"),
    ("right-point-start", "right-point-start"),
    ("give-props", "give-props"),
    ("give-props-start", "give-props-start"),
    ("right-hand", "right-hand"),
    ("right-hand-start", "right-hand-start"),
    ("duck", "duck"),
    ("sidestep-right", "jump-back-right"),
    # toon hq
    ### WARNING: this cycle only exists for dogMM!!!
    ("periscope", "periscope"),
    )

# minigame
Phase4AnimList = (
    ("sit", "sit"),
    ("sit-start", "intoSit"),
    ("swim", "swim"),
    ("tug-o-war", "tug-o-war"),
    ("sad-walk", "losewalk"),
    ("sad-neutral", "sad-neutral"),
    ("up", "up"),
    ("down", "down"),
    ("left", "left"),
    ("right", "right"),
    # emotes (that must be purchased)
    ("applause", "applause"),
    ("confused", "confused"),
    ("bow", "bow"),
    ("curtsy", "curtsy"),
    ("bored", "bored"),
    ("think", "think"),

    # For use in battle
    ("battlecast", "fish"),

    ("cast", "cast"),
    ("castlong", "castlong"),
    ("fish-end", "fishEND"),
    ("fish-neutral", "fishneutral"),
    ("fish-again", "fishAGAIN"),
    ("reel", "reel"),
    ("reel-H", "reelH"),
    ("reel-neutral", "reelneutral"),
    ("pole", "pole"),
    ("pole-neutral", "poleneutral"),

    ("slip-forward", "slip-forward"),
    ("slip-backward", "slip-backward"),
    # anims for the catching game
    ("catch-neutral", "gameneutral"),
    ("catch-run", "gamerun"),
    ("catch-eatneutral", "eat_neutral"),
    ("catch-eatnrun", "eatnrun"),
    ("catch-intro-throw", "gameThrow"),

    # anims for swing game
    ('swing', 'swing'),
    # pet cycles
    ("pet-start", "petin"),
    ("pet-loop", "petloop"),
    ("pet-end", "petend"),
    
    # For toonhall
    ("scientistJealous", "scientistJealous"),
    ("scientistEmcee", "scientistEmcee"),
    ("scientistWork", "scientistWork"),
    ("scientistGame", "scientistGame"),
    )

# battle
Phase5AnimList = (
    ("water-gun", "water-gun"),
    ("hold-bottle", "hold-bottle"),
    ("firehose", "firehose"),
    ("spit", "spit"),
    # heal
    ("tickle", "tickle"),
    ("smooch", "smooch"),
    ("happy-dance", "happy-dance"),
    ("sprinkle-dust", "sprinkle-dust"),
    ("juggle", "juggle"),
    ("climb", "climb"),
    # sound
    ("sound", "shout"),
    # trap
    ("toss", "toss"),
    # lure
    ("hold-magnet", "hold-magnet"),
    ("hypnotize", "hypnotize"),
    # react
    ("struggle", "struggle"),
    ("lose", "lose"),
    ("melt", "melt"),
    )

# estate
Phase5_5AnimList = (
    ("takePhone", "takePhone"),
    ("phoneNeutral", "phoneNeutral"),
    ("phoneBack", "phoneBack"),
    ("bank", "jellybeanJar"),
    ("callPet", "callPet"),
    ("feedPet", "feedPet"),
    ("start-dig", "into_dig"),
    ("loop-dig", "loop_dig"),
    ("water", "water"),
    )

# estate
Phase6AnimList = (
    ("headdown-putt","headdown-putt"),
    ("into-putt","into-putt"),
    ("loop-putt","loop-putt"),
    ("rotateL-putt","rotateL-putt"),
    ("rotateR-putt","rotateR-putt"),
    ("swing-putt","swing-putt"),
    ("look-putt","look-putt"),
    ("lookloop-putt","lookloop-putt"),
    ("bad-putt","bad-putt"),
    ("badloop-putt","badloop-putt"),
    ("good-putt","good-putt"),
    )

# sellbotHQ
Phase9AnimList = (
    ("push", "push"),
    )

# cashbotHQ
Phase10AnimList = (
    ("leverReach", "leverReach"),
    ("leverPull", "leverPull"),
    ("leverNeutral", "leverNeutral"),
    )

# bossbotHq
Phase12AnimList = (
    )

if not base.config.GetBool('want-new-anims', 1):
    # toon leg models dictionary
    LegDict = { "s":"/models/char/dogSS_Shorts-legs-", \
                "m":"/models/char/dogMM_Shorts-legs-", \
                "l":"/models/char/dogLL_Shorts-legs-" }

    # toon torso models dictionary
    TorsoDict = { "s":"/models/char/dogSS_Naked-torso-", \
                  "m":"/models/char/dogMM_Naked-torso-", \
                  "l":"/models/char/dogLL_Naked-torso-", \
                  "ss":"/models/char/dogSS_Shorts-torso-", \
                  "ms":"/models/char/dogMM_Shorts-torso-", \
                  "ls":"/models/char/dogLL_Shorts-torso-", \
                  "sd":"/models/char/dogSS_Skirt-torso-", \
                  "md":"/models/char/dogMM_Skirt-torso-", \
                  "ld":"/models/char/dogLL_Skirt-torso-" }
else:
    # toon leg models dictionary
    LegDict = { "s":"/models/char/tt_a_chr_dgs_shorts_legs_", \
                "m":"/models/char/tt_a_chr_dgm_shorts_legs_", \
                "l":"/models/char/tt_a_chr_dgl_shorts_legs_" }

    # toon torso models dictionary
    TorsoDict = { "s":"/models/char/dogSS_Naked-torso-", \
                  "m":"/models/char/dogMM_Naked-torso-", \
                  "l":"/models/char/dogLL_Naked-torso-", \
                  "ss":"/models/char/tt_a_chr_dgs_shorts_torso_", \
                  "ms":"/models/char/tt_a_chr_dgm_shorts_torso_", \
                  "ls":"/models/char/tt_a_chr_dgl_shorts_torso_", \
                  "sd":"/models/char/tt_a_chr_dgs_skirt_torso_", \
                  "md":"/models/char/tt_a_chr_dgm_skirt_torso_", \
                  "ld":"/models/char/tt_a_chr_dgl_skirt_torso_" }

# toon head models dictionary is in ToonHead.py.

def loadModels():
    """
    Toon class model and texture initialize
    """
    preloadAvatars = base.config.GetBool("preload-avatars", 0)

    if preloadAvatars:
        # preload the clothing textures
        global Preloaded

        def loadTex(path):
            # Only preload the texture if we have downloaded that phase
            # Peel off the phase and see if it is complete
            #if (path[:5] == "phase"):
            #    # The phase is from the 6th letter up to the /
            #    # This covers the phase_3.5/ case
            #    phaseStr = path[6:path.index('/')]
            #    phase = float(phaseStr)
            #    print phase
            #    if (phase in Launcher.LauncherPhases):
            #        if not self.getPhaseComplete(phase):
            #            return 0
            tex = loader.loadTexture(path)
            tex.setMinfilter(Texture.FTLinearMipmapLinear)
            tex.setMagfilter(Texture.FTLinear)
            Preloaded.append(tex)

        # Boys
        for shirt in ToonDNA.Shirts:
            loadTex(shirt)
        for sleeve in ToonDNA.Sleeves:
            loadTex(sleeve)
        for short in ToonDNA.BoyShorts:
            loadTex(short)

        # Girls
        # Girl bottoms are a tuple (texName, type)
        for bottom in ToonDNA.GirlBottoms:
            loadTex(bottom[0])

        # preload the leg models
        for key in LegDict.keys():
            fileRoot = LegDict[key]
            model = loader.loadModelNode("phase_3" + fileRoot + "1000")
            Preloaded.append(model)
            model = loader.loadModelNode("phase_3" + fileRoot + "500")
            Preloaded.append(model)
            model = loader.loadModelNode("phase_3" + fileRoot + "250")
            Preloaded.append(model)                   

        #preload the torso models
        for key in TorsoDict.keys():
            fileRoot = TorsoDict[key]
            model = loader.loadModelNode("phase_3" + fileRoot + "1000")
            Preloaded.append(model)
            # don't load LOD's for the naked toon
            if (len(key) > 1):
                        model = loader.loadModelNode("phase_3" + fileRoot + "500")
                        Preloaded.append(model)
                        model = loader.loadModelNode("phase_3" + fileRoot + "250")
                        Preloaded.append(model)    

        #preload the head models
        for key in HeadDict.keys():
            fileRoot = HeadDict[key]
            model = loader.loadModelNode("phase_3" + fileRoot + "1000")
            Preloaded.append(model)
            model = loader.loadModelNode("phase_3" + fileRoot + "500")
            Preloaded.append(model)
            model = loader.loadModelNode("phase_3" + fileRoot + "250")
            Preloaded.append(model)

def loadBasicAnims():
    """
    Load the default Toon anims
    """
    loadPhaseAnims()

def unloadBasicAnims():
    """
    Unload the default Toon anims
    """
    loadPhaseAnims(0)

def loadTutorialBattleAnims():
    loadPhaseAnims("phase_3.5")

def unloadTutorialBattleAnims():
    loadPhaseAnims("phase_3.5", 0)

def loadMinigameAnims():
    """
    Load the minigame specific Toon anims
    """
    loadPhaseAnims("phase_4")

def unloadMinigameAnims():
    """
    Unload the minigame specific Toon anims
    """
    loadPhaseAnims("phase_4", 0)

def loadBattleAnims():
    """
    Load the battle specific Toon anims1
    """
    loadPhaseAnims("phase_5")

def unloadBattleAnims():
    """
    Unload the battle specific Toon anims
    """
    loadPhaseAnims("phase_5", 0)

def loadSellbotHQAnims():
    """
    Load the sellbot hq specific Toon anims
    """
    loadPhaseAnims("phase_9")

def unloadSellbotHQAnims():
    """
    Unload the sellbot hq specific Toon anims
    """
    loadPhaseAnims("phase_9", 0)

def loadCashbotHQAnims():
    """
    Load the cashbot hq specific Toon anims
    """
    loadPhaseAnims("phase_10")

def unloadCashbotHQAnims():
    """
    Unload the cashbot hq specific Toon anims
    """
    loadPhaseAnims("phase_10", 0)

def loadBossbotHQAnims():
    """
    Load the bossbot hq specific Toon anims
    """
    loadPhaseAnims("phase_12")

def unloadBossbotHQAnims():
    """
    Unload the bossbot hq specific Toon anims
    """
    loadPhaseAnims("phase_12", 0)

def loadPhaseAnims(phaseStr="phase_3", loadFlag = 1):
    """loadPhaseAnims(string, int):
    If loadFlag = 1, load the anims for the given phase(default = 'phase_3').
    Otherwise unload them. This is kinda ugly but it keeps from having too
    much redundant code.
    """
    if (phaseStr == "phase_3"):
        animList = Phase3AnimList
    elif (phaseStr == "phase_3.5"):
        animList = Phase3_5AnimList
    elif (phaseStr == "phase_4"):
        animList = Phase4AnimList
    elif (phaseStr == "phase_5"):
        animList = Phase5AnimList
    elif (phaseStr == "phase_5.5"):
        animList = Phase5_5AnimList
    elif (phaseStr == "phase_6"):
        animList = Phase6AnimList
    elif (phaseStr == "phase_9"):
        animList = Phase9AnimList
    elif (phaseStr == "phase_10"):
        animList = Phase10AnimList
    elif (phaseStr == "phase_12"):
        animList = Phase12AnimList
    else:
        # bad phase string
        self.notify.error("Unknown phase string %s" % phaseStr)

    # For now, we are loading on bind and relying on garbage collection
    # to tidy up the model pool. All we actually do here is delete the
    # anim controls from the localToon's dictionary
    for key in LegDict.keys():
        for anim in animList:
            #file = phaseStr + LegDict[key] + anim[1]
            if loadFlag:
                #loader.loadModelNode(file)
                pass
            else:
                #loader.unloadModel(file)
                if LegsAnimDict[key].has_key(anim[0]):
                    if (base.localAvatar.style.legs == key):
                        base.localAvatar.unloadAnims([anim[0]], "legs", None)

    for key in TorsoDict.keys():
        for anim in animList:
            #file = phaseStr + TorsoDict[key] + anim[1]
            if loadFlag:
                #loader.loadModelNode(file)
                pass
            else:
                #loader.unloadModel(file)
                if TorsoAnimDict[key].has_key(anim[0]):
                    if (base.localAvatar.style.torso == key):
                        base.localAvatar.unloadAnims([anim[0]], "torso", None)

    for key in HeadDict.keys():
        # only load anims for dog heads
        if (string.find(key,"d") >= 0):
            for anim in animList:
                #file = phaseStr + HeadDict[key] + anim[1]
                if loadFlag:
                    #loader.loadModelNode(file)
                    pass
                else:
                    #loader.unloadModel(file)
                    if HeadAnimDict[key].has_key(anim[0]):
                        if (base.localAvatar.style.head == key):
                            base.localAvatar.unloadAnims([anim[0]], "head", None)

def compileGlobalAnimList():
    """
    Munge the anim names and file paths into big dictionaries for the
    leg, torso, and head parts. These are used for loading the anims.
    """
    # Nowadays we want all anims in the list. It would save work
    # in loadphaseAnims if we split this into phases. Optimize later.
    phaseList = [Phase3AnimList,Phase3_5AnimList,Phase4AnimList,Phase5AnimList,Phase5_5AnimList,Phase6AnimList,Phase9AnimList,Phase10AnimList, Phase12AnimList]
    phaseStrList = ["phase_3", "phase_3.5", "phase_4", "phase_5", "phase_5.5", "phase_6", "phase_9", "phase_10", "phase_12"]

    for animList in phaseList:
        phaseStr = phaseStrList[phaseList.index(animList)]
        for key in LegDict.keys():
            LegsAnimDict.setdefault(key, {})
            for anim in animList:
                file = phaseStr + LegDict[key] + anim[1]
                LegsAnimDict[key][anim[0]] = file

        for key in TorsoDict.keys():
            TorsoAnimDict.setdefault(key, {})
            for anim in animList:
                file = phaseStr + TorsoDict[key] + anim[1]
                TorsoAnimDict[key][anim[0]] = file

        for key in HeadDict.keys():
            # only load anims for dog heads
            if (string.find(key,"d") >= 0):
                HeadAnimDict.setdefault(key, {})
                for anim in animList:
                    file = phaseStr + HeadDict[key] + anim[1]
                    HeadAnimDict[key][anim[0]] = file

def loadDialog():
    """
    Load the dialogue audio samples
    """
    loadPath = "phase_3.5/audio/dial/"

    # load the dog dialogue
    DogDialogueFiles = ( "AV_dog_short",
                         "AV_dog_med",
                         "AV_dog_long",
                         "AV_dog_question",
                         "AV_dog_exclaim",
                         "AV_dog_howl"
                         )
    # load the audio files and store into the dialogue array
    for file in DogDialogueFiles:
        DogDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the cat dialogue
    catDialogueFiles = ( "AV_cat_short",
                         "AV_cat_med",
                         "AV_cat_long",
                         "AV_cat_question",
                         "AV_cat_exclaim",
                         "AV_cat_howl"
                         )
    # load the audio files and store into the dialogue array
    for file in catDialogueFiles:
        CatDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the horse dialogue
    horseDialogueFiles = ( "AV_horse_short",
                           "AV_horse_med",
                           "AV_horse_long",
                           "AV_horse_question",
                           "AV_horse_exclaim",
                           "AV_horse_howl"
                           )

    # load the audio files and store into the dialogue array
    for file in horseDialogueFiles:
        HorseDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the rabbit dialogue
    rabbitDialogueFiles = ( "AV_rabbit_short",
                            "AV_rabbit_med",
                            "AV_rabbit_long",
                            "AV_rabbit_question",
                            "AV_rabbit_exclaim",
                            "AV_rabbit_howl"
                            )

    # load the audio files and store into the dialogue array
    for file in rabbitDialogueFiles:
        RabbitDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the mouse dialogue
    # for now the mouse reuses the rabbit sounds
    mouseDialogueFiles = ( "AV_mouse_short",
                           "AV_mouse_med",
                           "AV_mouse_long",
                           "AV_mouse_question",
                           "AV_mouse_exclaim",
                           "AV_mouse_howl"
                           )

    # load the audio files and store into the dialogue array
    for file in mouseDialogueFiles:
        MouseDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the duck dialogue array
    duckDialogueFiles = ( "AV_duck_short",
                          "AV_duck_med",
                          "AV_duck_long",
                          "AV_duck_question",
                          "AV_duck_exclaim",
                          "AV_duck_howl"
                          )

    # load the audio files and store into the dialogue array
    for file in duckDialogueFiles:
        DuckDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

    # load the monkey dialogue array
    monkeyDialogueFiles = ( "AV_monkey_short",
                            "AV_monkey_med",
                            "AV_monkey_long",
                            "AV_monkey_question",
                            "AV_monkey_exclaim",
                            "AV_monkey_howl"
                            )

    # load the audio files and store into the dialogue array
    for file in monkeyDialogueFiles:
        MonkeyDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))


    # load the bear dialogue array
    bearDialogueFiles = ( "AV_bear_short",
                            "AV_bear_med",
                            "AV_bear_long",
                            "AV_bear_question",
                            "AV_bear_exclaim",
                            "AV_bear_howl"
                            )

    # load the audio files and store into the dialogue array
    for file in bearDialogueFiles:
        BearDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))


    # load the pig dialogue array
    pigDialogueFiles = ( "AV_pig_short",
                            "AV_pig_med",
                            "AV_pig_long",
                            "AV_pig_question",
                            "AV_pig_exclaim",
                            "AV_pig_howl"
                            )

    # load the audio files and store into the dialogue array
    for file in pigDialogueFiles:
        PigDialogueArray.append(base.loadSfx(loadPath + file + ".mp3"))

def unloadDialog():
    global DogDialogueArray
    global CatDialogueArray
    global HorseDialogueArray
    global RabbitDialogueArray
    global MouseDialogueArray
    global DuckDialogueArray
    global MonkeyDialogueArray
    global BearDialogueArray
    global PigDialogueArray
    DogDialogueArray = []
    CatDialogueArray = []
    HorseDialogueArray = []
    RabbitDialogueArray = []
    MouseDialogueArray = []
    DuckDialogueArray = []
    MonkeyDialogueArray = []
    BearDialogueArray = []
    PigDialogueArray = []


class Toon(Avatar.Avatar, ToonHead):
    """Toon class:"""

    notify = DirectNotifyGlobal.directNotify.newCategory("Toon")

    afkTimeout = base.config.GetInt('afk-timeout', 600)
    
    # This is the tuple of allowed animations that can be set by using toon.setAnimState().
    # If you add an animation that you want to do a setAnimState on please add this
    # animation to this list.
    setAnimStateAllowedList = (
        'off',
        'neutral',
        'victory',
        'Happy',
        'Sad',
        'Catching',
        'CatchEating',
        'Sleep',
        'walk',
        'jumpSquat',
        'jump',
        'jumpAirborne',
        'jumpLand',
        'run',
        'swim',
        'swimhold',
        'dive',
        'cringe',
        'OpenBook',
        'ReadBook',
        'CloseBook',
        'TeleportOut',
        'Died',
        'TeleportIn',
        'Emote',
        'SitStart',
        'Sit',
        'Push',
        'Squish',
        'FallDown',
        'GolfPuttLoop',
        'GolfRotateLeft',
        'GolfRotateRight',
        'GolfPuttSwing',
        'GolfGoodPutt',
        'GolfBadPutt',
        'Flattened',
        'CogThiefRunning',
        'ScientistJealous',
        'ScientistEmcee',
        'ScientistWork',
        'ScientistLessWork',
        'ScientistPlay'
        )

    def __init__(self):
        try:
            self.Toon_initialized
            return
        except:
            self.Toon_initialized = 1
        Avatar.Avatar.__init__(self)
        ToonHead.__init__(self)

        self.forwardSpeed = 0.0
        self.rotateSpeed = 0.0

        # Set Avatar Type (Toon, Teen, or Pirate)
        self.avatarType = "toon"

        # These members are only used to track the current actual
        # animation and play rate in effect when motion.standWalkRunReverse
        # is not None.
        self.motion = Motion.Motion(self)
        self.standWalkRunReverse = None
        self.playingAnim = None
        self.soundTeleport = None

        self.cheesyEffect = ToontownGlobals.CENormal
        self.effectTrack = None
        self.emoteTrack = None
        self.emote = None
        self.stunTrack = None

        self.__bookActors = []
        self.__holeActors = []
        self.holeClipPath = None

        self.wake = None
        self.lastWakeTime = 0

        self.numPies = 0
        self.pieType = 0
        self.pieModel = None
        self.__pieModelType = None

        # Stunned if recently hit by stomper
        self.isStunned = 0

        # are we disguised as a suit?
        self.isDisguised = 0

        self.defaultColorScale = None

        self.jar = None

        self.setTag('pieCode', str(ToontownGlobals.PieCodeToon))

        # Define Toon's Font
        # fancy nametag point 1
        self.setFont(ToontownGlobals.getToonFont())

        # chat balloon sound
        self.soundChatBubble = base.loadSfx("phase_3/audio/sfx/GUI_balloon_popup.mp3")

        # The animFSM doesn't really have any restrictions on
        # transitions between states--we don't care which anim
        # state might follow from the current one; we only want to
        # ensure everything gets cleaned up properly.
        self.animFSM = ClassicFSM(
            'Toon',
            [State('off', self.enterOff, self.exitOff),
            State('neutral', self.enterNeutral, self.exitNeutral),
            State('victory', self.enterVictory, self.exitVictory),
            State('Happy', self.enterHappy, self.exitHappy),
            State('Sad', self.enterSad, self.exitSad),
            State('Catching', self.enterCatching, self.exitCatching),
            State('CatchEating', self.enterCatchEating, self.exitCatchEating),
            State('Sleep', self.enterSleep, self.exitSleep),
            State('walk', self.enterWalk, self.exitWalk),
            State('jumpSquat', self.enterJumpSquat, self.exitJumpSquat),
            State('jump', self.enterJump, self.exitJump),
            State('jumpAirborne', self.enterJumpAirborne, self.exitJumpAirborne),
            State('jumpLand', self.enterJumpLand, self.exitJumpLand),
            State('run', self.enterRun, self.exitRun),
            State('swim', self.enterSwim, self.exitSwim),
            State('swimhold', self.enterSwimHold, self.exitSwimHold),
            State('dive', self.enterDive, self.exitDive),
            State('cringe', self.enterCringe, self.exitCringe),
            State('OpenBook', self.enterOpenBook, self.exitOpenBook, ['ReadBook','CloseBook']),
            State('ReadBook', self.enterReadBook, self.exitReadBook),
            State('CloseBook', self.enterCloseBook, self.exitCloseBook),
            State('TeleportOut', self.enterTeleportOut, self.exitTeleportOut),
            State('Died', self.enterDied, self.exitDied),
            State('TeleportedOut', self.enterTeleportedOut, self.exitTeleportedOut),
            State('TeleportIn', self.enterTeleportIn, self.exitTeleportIn),
            State('Emote', self.enterEmote, self.exitEmote),
            State('SitStart', self.enterSitStart, self.exitSitStart),
            State('Sit', self.enterSit, self.exitSit),
            State('Push', self.enterPush, self.exitPush),
            State('Squish', self.enterSquish, self.exitSquish),
            State('FallDown', self.enterFallDown, self.exitFallDown),
            State('GolfPuttLoop', self.enterGolfPuttLoop, self.exitGolfPuttLoop),
            State('GolfRotateLeft', self.enterGolfRotateLeft, self.exitGolfRotateLeft),
            State('GolfRotateRight', self.enterGolfRotateRight, self.exitGolfRotateRight),
            State('GolfPuttSwing', self.enterGolfPuttSwing, self.exitGolfPuttSwing),
            State('GolfGoodPutt', self.enterGolfGoodPutt, self.exitGolfGoodPutt),
            State('GolfBadPutt', self.enterGolfBadPutt, self.exitGolfBadPutt),
            State('Flattened', self.enterFlattened, self.exitFlattened),
            State('CogThiefRunning', self.enterCogThiefRunning, self.exitCogThiefRunning),
            State('ScientistJealous', self.enterScientistJealous, self.exitScientistJealous),
            State('ScientistEmcee', self.enterScientistEmcee, self.exitScientistEmcee),
            State('ScientistWork', self.enterScientistWork, self.exitScientistWork),
            State('ScientistLessWork', self.enterScientistLessWork, self.exitScientistLessWork),
            State('ScientistPlay', self.enterScientistPlay, self.enterScientistPlay),
            ],
            # Initial State
            'off',
            # Final State
            'off',
            )
        self.animFSM.enterInitialState()
        # Note: When you add an animation to this animFSM list also add it to
        # setAnimStateAllowedList if you want to use setAnimState to change to that animation. 

    def stopAnimations(self):
        assert self.notify.debugStateCall(self, "animFsm")
        if not self.animFSM.isInternalStateInFlux():
            self.animFSM.request('off')
        else:
            self.notify.warning('animFSM in flux, state=%s, not requesting off' %
                                self.animFSM.getCurrentState().getName())
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        if self.emoteTrack != None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        if self.stunTrack != None:
            self.stunTrack.finish()
            self.stunTrack = None
        if self.wake:
            self.wake.stop()
            self.wake.destroy()
            self.wake = None
        self.cleanupPieModel()

    def delete(self):
        assert self.notify.debugStateCall(self, "animFsm")
        try:
            self.Toon_deleted
        except:
            self.Toon_deleted = 1
            self.stopAnimations()
            self.rightHands = None
            self.rightHand = None
            self.leftHands = None
            self.leftHand = None
            self.headParts = None
            self.torsoParts = None
            self.hipsParts = None
            self.legsParts = None
            del self.animFSM
            for bookActor in self.__bookActors:
                bookActor.cleanup()
            del self.__bookActors
            for holeActor in self.__holeActors:
                holeActor.cleanup()
            del self.__holeActors
            self.soundTeleport = None
            self.motion.delete()
            self.motion = None
            Avatar.Avatar.delete(self)
            ToonHead.delete(self)

    # toon methods

    def updateToonDNA(self, newDNA, fForce = 0):
        """
        update the toon's appearance based on new DNA
        """
        assert self.notify.debugStateCall(self, "animFsm")
        # Make sure gender is updated (for RobotToons)
        self.style.gender = newDNA.getGender()
        # test and only update the new parts
        oldDNA = self.style
        if fForce or (newDNA.head != oldDNA.head):
            self.swapToonHead(newDNA.head)
        if fForce or (newDNA.torso != oldDNA.torso):
            self.swapToonTorso(newDNA.torso, genClothes = 0)
            self.loop('neutral')
        if fForce or (newDNA.legs != oldDNA.legs):
            self.swapToonLegs(newDNA.legs)
        # easier just to do these color!'s than to check
        self.swapToonColor(newDNA)
        self.__swapToonClothes(newDNA)

    def setDNAString(self, dnaString):
        assert self.notify.debugStateCall(self, "animFsm")
        newDNA = ToonDNA.ToonDNA()
        newDNA.makeFromNetString(dnaString)
        self.setDNA(newDNA)

    def setDNA(self, dna):
        assert self.notify.debugStateCall(self, "animFsm")
        # if we are disguised, don't mess up our custom geom
        if hasattr(self, "isDisguised"):
            if self.isDisguised:
                return

        if self.style:
            self.updateToonDNA(dna)
        else:
            # store the DNA
            self.style = dna

            self.generateToon()

            # this no longer works in the Avatar init!
            # I moved it here for lack of a better place
            # make the drop shadow
            self.initializeDropShadow()
            self.initializeNametag3d()



    def parentToonParts(self):
        """
        attach the toon's parts - recurse over all LODs
        """
        #import pdb; pdb.set_trace()
        assert self.notify.debugStateCall(self, "animFsm")
        # import pdb; pdb.set_trace()
        # attach all the various toon pieces
        if (self.hasLOD()):
            for lodName in self.getLODNames():
                if base.config.GetBool('want-new-anims', 1):
                    if not self.getPart("torso", lodName).find('**/def_head').isEmpty():
                        self.attach("head", "torso", "def_head", lodName)
                    else:
                        self.attach("head", "torso", "joint_head", lodName)
                else:
                    self.attach("head", "torso", "joint_head", lodName)
                self.attach("torso", "legs", "joint_hips", lodName)
        else:
            self.attach("head", "torso", "joint_head")
            self.attach("torso", "legs", "joint_hips")


    def unparentToonParts(self):
        """
        attach all parts to the geomNode - recurse over all LODs
        """
        assert self.notify.debugStateCall(self, "animFsm")
        # unattach the various toon pieces
        if (self.hasLOD()):
            for lodName in self.getLODNames():
                self.getPart("head", lodName).reparentTo(self.getLOD(lodName))
                self.getPart("torso", lodName).reparentTo(self.getLOD(lodName))
                self.getPart("legs", lodName).reparentTo(self.getLOD(lodName))
        else:
            self.getPart("head").reparentTo(self.getGeomNode())
            self.getPart("torso").reparentTo(self.getGeomNode())
            self.getPart("legs").reparentTo(self.getGeomNode())

    def setLODs(self):
        """
        Get LOD switch distances from dconfig, or use defaults
        """
        assert self.notify.debugStateCall(self, "animFsm")
        # set up the LOD node for avatar LOD
        self.setLODNode()

        # get the switch values
        levelOneIn = base.config.GetInt("lod1-in", 20)
        levelOneOut = base.config.GetInt("lod1-out", 0)
        levelTwoIn = base.config.GetInt("lod2-in", 80)
        levelTwoOut = base.config.GetInt("lod2-out", 20)
        levelThreeIn = base.config.GetInt("lod3-in", 280)
        levelThreeOut = base.config.GetInt("lod3-out", 80)

        # add the LODs
        self.addLOD(1000, levelOneIn, levelOneOut)
        self.addLOD(500, levelTwoIn, levelTwoOut)
        self.addLOD(250, levelThreeIn, levelThreeOut)


    def generateToon(self):
        """
        Create a toon from dna (an array of strings)
        NOTE: DistributedNPCToon overrides this because they do not need it all
        """
        assert self.notify.debugStateCall(self, "animFsm")
        # set up LOD info
        self.setLODs()
        # load the toon legs
        self.generateToonLegs()
        # load the toon head
        self.generateToonHead()
        # load the toon torso
        self.generateToonTorso()
        # color the toon as specified by the dna
        self.generateToonColor()
        self.parentToonParts()
        # make small toons with big heads
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()

    def setupToonNodes(self):
        assert self.notify.debugStateCall(self, "animFsm")
        # Initialize arrays of pointers to useful nodes for the toon
        rightHand = NodePath('rightHand')
        self.rightHand = None
        self.rightHands = []
        leftHand = NodePath('leftHand')
        self.leftHands = []
        self.leftHand = None
        for lodName in self.getLODNames():
            hand = self.getPart('torso', lodName).find('**/joint_Rhold')
            if base.config.GetBool('want-new-anims', 1):
                if not self.getPart('torso', lodName).find('**/def_joint_right_hold').isEmpty():
                    hand = self.getPart('torso', lodName).find('**/def_joint_right_hold')
            else:
                hand = self.getPart('torso', lodName).find('**/joint_Rhold')
            self.rightHands.append(hand)
            #import pdb; pdb.set_trace()
            rightHand = rightHand.instanceTo(hand)
            if base.config.GetBool('want-new-anims', 1):
                if not self.getPart('torso', lodName).find('**/def_joint_left_hold').isEmpty():
                    hand = self.getPart('torso', lodName).find('**/def_joint_left_hold')
            else:
                hand = self.getPart('torso', lodName).find('**/joint_Lhold')
            self.leftHands.append(hand)
            leftHand = leftHand.instanceTo(hand)
            # It's important that self.rightHand and self.leftHand
            # reflect the first instance in the list (for the highest
            # level LOD), for historical reasons.
            if self.rightHand == None:
                self.rightHand = rightHand
            if self.leftHand == None:
                self.leftHand = leftHand
        self.headParts = self.findAllMatches('**/__Actor_head')
        self.legsParts = self.findAllMatches('**/__Actor_legs')
        # Hips are under the legs
        self.hipsParts = self.legsParts.findAllMatches('**/joint_hips')
        # Torso is under the hips
        self.torsoParts = self.hipsParts.findAllMatches('**/__Actor_torso')

    def initializeBodyCollisions(self, collIdStr):
        Avatar.Avatar.initializeBodyCollisions(self, collIdStr)

        if not self.ghostMode:
            self.collNode.setCollideMask(self.collNode.getIntoCollideMask() | ToontownGlobals.PieBitmask)

    def getBookActors(self):
        """
        Return the book actors. If they have not been created,
        we need to set them up the first time
        """
        # See if we have already created them
        # If we have, just return them
        if self.__bookActors:
            return self.__bookActors
        # Otherwise we need to load them
        bookActor = Actor.Actor('phase_3.5/models/props/book-mod',
                                {'book': 'phase_3.5/models/props/book-chan'})
        bookActor2 = Actor.Actor(other=bookActor)
        bookActor3 = Actor.Actor(other=bookActor)
        self.__bookActors = [bookActor, bookActor2, bookActor3]
        hands = self.getRightHands()
        for bookActor, hand in zip(self.__bookActors, hands):
            bookActor.reparentTo(hand)
            bookActor.hide()
        return self.__bookActors

    def getHoleActors(self):
        """
        Return the teleport hole actors. If they have not been created,
        we need to set them up the first time
        """
        # See if we have already created them
        # If we have, just return them
        if self.__holeActors:
            return self.__holeActors
        # Otherwise we need to load them
        holeActor = Actor.Actor('phase_3.5/models/props/portal-mod',
                                {'hole': 'phase_3.5/models/props/portal-chan'})
        holeActor2 = Actor.Actor(other=holeActor)
        holeActor3 = Actor.Actor(other=holeActor)
        self.__holeActors = [holeActor, holeActor2, holeActor3]
        for ha in self.__holeActors:
            if hasattr(self, "uniqueName"):
                holeName = self.uniqueName("toon-portal")
            else:
                holeName = "toon-portal"
            ha.setName(holeName)
        return self.__holeActors

    def rescaleToon(self):
        """
        Rescale all the toons. The values are typed in
        ToontownGlobals dictionaries and get set here.
        """
        assert self.notify.debugStateCall(self, "animFsm")
        animalStyle = self.style.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        headScale = ToontownGlobals.toonHeadScales[animalStyle]
        self.setAvatarScale(bodyScale)
        for lod in self.getLODNames():
            self.getPart('head', lod).setScale(headScale)

    def getBodyScale(self):
        animalStyle = self.style.getAnimal()
        bodyScale = ToontownGlobals.toonBodyScales[animalStyle]
        return bodyScale


    def resetHeight(self):
        """
        Reset the height based on the current style, including scales
        """
        assert self.notify.debugStateCall(self, "animFsm")
        if hasattr(self,'style') and self.style:
            animal = self.style.getAnimal()
            bodyScale = ToontownGlobals.toonBodyScales[animal]
            headScale = ToontownGlobals.toonHeadScales[animal][2]
            shoulderHeight = (
                (ToontownGlobals.legHeightDict[self.style.legs] * bodyScale) +
                (ToontownGlobals.torsoHeightDict[self.style.torso] * bodyScale)
                )
            height = (
                shoulderHeight +
                (ToontownGlobals.headHeightDict[self.style.head] * headScale)
                )
            self.shoulderHeight = shoulderHeight
            if self.cheesyEffect == ToontownGlobals.CEBigToon or self.cheesyEffect == ToontownGlobals.CEBigWhite:
                height *= ToontownGlobals.BigToonScale
            elif self.cheesyEffect == ToontownGlobals.CESmallToon:
                height *= ToontownGlobals.SmallToonScale
            self.setHeight(height)

    def generateToonLegs(self, copy = 1):
        """generateToonLegs(self, bool = 0)
        Load the leg models for the toon.
        If copy = 0, don't copy new geometry, instance it.
        """
        legStyle = self.style.legs
        filePrefix = LegDict.get(legStyle)
        if filePrefix is None:
            self.notify.error("unknown leg style: %s" % legStyle)
        # load the models
        self.loadModel("phase_3" + filePrefix + "1000", "legs", "1000", copy)        
        self.loadModel("phase_3" + filePrefix + "500", "legs", "500", copy)
        self.loadModel("phase_3" + filePrefix + "250", "legs", "250", copy)
        if not copy:
            self.showPart("legs", "1000")
            self.showPart("legs", "500")
            self.showPart("legs", "250")
        # load the anims for this type of leg
        self.loadAnims(LegsAnimDict[legStyle], "legs", "1000")
        self.loadAnims(LegsAnimDict[legStyle], "legs", "500")
        self.loadAnims(LegsAnimDict[legStyle], "legs", "250")

    def swapToonLegs(self, legStyle, copy = 1):
        """swapToonLegs(self, string, bool = 1)
        Switch out the current toon models for the given legStyle.
        See ToonDNA for leg type list.
        """
        # unparent all the toon parts
        self.unparentToonParts()
        # Delete the old legs.  It is ok to "remove" them, even if we
        # are working with instances instead of with copies, because
        # of the way instances work.
        self.removePart("legs", "1000")
        self.removePart("legs", "500")
        self.removePart("legs", "250")
        # make the new legs part of the dna
        self.style.legs = legStyle
        # load the new legs
        self.generateToonLegs(copy)
        # color the new legs
        self.generateToonColor()
        # put everything back together
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        # re-make the drop shadows
        del self.shadowJoint # This is a bit of a hack for Make a Toon.
        self.initializeDropShadow()
        self.initializeNametag3d()

    def generateToonTorso(self, copy = 1, genClothes = 1):
        """generateToonTorso(string, bool = 1)
        Load the torso model for the toon.
        If copy = 0, instance geom instead of copying
        """
        torsoStyle = self.style.torso
        filePrefix = TorsoDict.get(torsoStyle)
        if filePrefix is None:
            self.notify.error("unknown torso style: %s" % torsoStyle)
        # load the models
        self.loadModel("phase_3" + filePrefix + "1000", "torso", "1000", copy)
        # this is a hack to support the naked toons
        if (len(torsoStyle) == 1):
            self.loadModel("phase_3" + filePrefix + "1000", "torso", "500", copy)
            self.loadModel("phase_3" + filePrefix + "1000", "torso", "250", copy)
        else:
            self.loadModel("phase_3" + filePrefix + "500", "torso", "500", copy)
            self.loadModel("phase_3" + filePrefix + "250", "torso", "250", copy)                       
        if not copy:
            self.showPart('torso', '1000')
            self.showPart('torso', '500')
            self.showPart('torso', '250')
        # load the anims for this type of torso
        self.loadAnims(TorsoAnimDict[torsoStyle], "torso", "1000")
        self.loadAnims(TorsoAnimDict[torsoStyle], "torso", "500")
        self.loadAnims(TorsoAnimDict[torsoStyle], "torso", "250")
        # if not a naked toon, set the clothing textures
        if (genClothes == 1 and not (len(torsoStyle) == 1)):
            self.generateToonClothes()

    def swapToonTorso(self, torsoStyle, copy = 1, genClothes = 1):
        """swapToonTorso(self, string, bool = 1)
        Switch the current toon torso model for the specified one.
        See ToonDNA for torso style list
        """
        assert self.notify.debug("swapToonTorso() - torso: %s genClothes: %d" % (torsoStyle, genClothes))
        # unparent all the parts
        self.unparentToonParts()
        # delete the old torso model
        self.removePart('torso', '1000')
        self.removePart('torso', '500')
        self.removePart('torso', '250')
        # add the new torso to the dna
        self.style.torso = torsoStyle
        # load the new torso model
        self.generateToonTorso(copy, genClothes)
        # color the new torso
        self.generateToonColor()
        # put everything back together
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()

    def generateToonHead(self, copy = 1):
        """generateToonHead(self, bool = 1)
        Load the head model and textures for the toon.
        If copy = 0, instance geom instead of copying.
        """
        headHeight = ToonHead.generateToonHead(
            self, copy, self.style, ('1000', '500', '250'))
        # load the anims for the dog head only
        if self.style.getAnimal() == 'dog':
            self.loadAnims(HeadAnimDict[self.style.head], "head", "1000")
            self.loadAnims(HeadAnimDict[self.style.head], "head", "500")
            self.loadAnims(HeadAnimDict[self.style.head], "head", "250")




    def swapToonHead(self, headStyle, copy = 1):
        """swapToonHead(self, string)
        Switch the current head model for the specified one.
        See ToonDNA for head style list
        """
        self.stopLookAroundNow()
        # First, make sure our eyes are open.
        self.eyelids.request('open')
        # unparent all parts
        self.unparentToonParts()
        # delete the old head
        self.removePart('head', '1000')
        self.removePart('head', '500')
        self.removePart('head', '250')
        # add the new head to the dna
        self.style.head = headStyle
        # load the new head
        self.generateToonHead(copy)
        # color the new head
        self.generateToonColor()
        # put it all back together
        self.parentToonParts()
        # If the head changes, we need to rescale
        self.rescaleToon()
        self.resetHeight()
        self.eyelids.request("open")
        self.startLookAround()

    def generateToonColor(self):
        """
        Color the toon's parts as specified by the dna.
        Color any LODs by searching for ALL matches.
        """
        ToonHead.generateToonColor(self, self.style)

        armColor = self.style.getArmColor()
        gloveColor = self.style.getGloveColor()
        legColor = self.style.getLegColor()

        for lodName in self.getLODNames():
            torso = self.getPart('torso', lodName)
            # if the toon has no clothes make sure the torso parts colored
            if (len(self.style.torso) == 1):
                # There are multiple torso pieces, so find all matches
                parts = torso.findAllMatches("**/torso*")
                parts.setColor(armColor)
            # Color the arms and neck
            for pieceName in ('arms', 'neck'):
                piece = torso.find('**/' + pieceName)
                piece.setColor(armColor)
            # Color the gloves
            hands = torso.find('**/hands')
            hands.setColor(gloveColor)
            # Color the lower body
            # import pdb; pdb.set_trace()
            legs = self.getPart('legs', lodName)
            for pieceName in ('legs', 'feet'):
                piece = legs.find('**/' + pieceName)
                piece.setColor(legColor)

        # no shoes yet, forget this bit
        # color the front of the feet - may have multiple pieces
        #parts = self.findAllMatches("**/toBall*")
        #parts.setColor(dna.getLegColor())

    def swapToonColor(self, dna):
        """
        Update the avatar's dna and adjust body colors accordingly
        """
        self.setStyle(dna)
        self.generateToonColor()

    def __swapToonClothes(self, dna):
        self.setStyle(dna)
        self.generateToonClothes(fromNet = 1)

    def generateToonClothes(self, fromNet = 0):
        """
        Set the textures and colors described in the dna for the clothes
        """
        # for each lod, get the model, find the parts and bang
        # the appropriate texture
        swappedTorso = 0
        if (self.hasLOD()):
            if (self.style.getGender() == 'f' and fromNet == 0):
                # See if we need to switch torso to change from skirts to
                # shorts or vice versa
                # Only do this once
                try:
                    bottomPair = ToonDNA.GirlBottoms[self.style.botTex]
                except:
                    bottomPair = ToonDNA.GirlBottoms[0]
                if (self.style.torso[1] == 's' and
                    bottomPair[1] == ToonDNA.SKIRT):
                    assert self.notify.debug("genToonClothes() - swapping torso from 's' to 'd', tex: %s" % bottomPair[0])
                    self.swapToonTorso(self.style.torso[0] + 'd',
                                                genClothes = 0)
                    swappedTorso = 1
                elif (self.style.torso[1] == 'd' and
                      bottomPair[1] == ToonDNA.SHORTS):
                    assert self.notify.debug("genToonClothes() - swapping torso from 'd' to 's', tex: %s" % bottomPair[0])
                    self.swapToonTorso(self.style.torso[0] + 's',
                                                genClothes = 0)
                    swappedTorso = 1

            # Setup all the textures and colors for all the LODS ahead of time
            # get the top texture and color
            try:
                texName = ToonDNA.Shirts[self.style.topTex]
            except:
                texName = ToonDNA.Shirts[0]
            shirtTex = loader.loadTexture(texName)
            shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
            shirtTex.setMagfilter(Texture.FTLinear)
            try:
                shirtColor = ToonDNA.ClothesColors[self.style.topTexColor]
            except:
                shirtColor = ToonDNA.ClothesColors[0]
            # set the sleeve texture and color
            try:
                texName = ToonDNA.Sleeves[self.style.sleeveTex]
            except:
                texName = ToonDNA.Sleeves[0]
            sleeveTex = loader.loadTexture(texName)
            sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
            sleeveTex.setMagfilter(Texture.FTLinear)
            try:
                sleeveColor = ToonDNA.ClothesColors[self.style.sleeveTexColor]
            except:
                sleeveColor = ToonDNA.ClothesColors[0]
            # set the bottom texture and color
            if (self.style.getGender() == 'm'):
                try:
                    texName = ToonDNA.BoyShorts[self.style.botTex]
                except:
                    texName = ToonDNA.BoyShorts[0]
            else:
                try:
                    texName = ToonDNA.GirlBottoms[self.style.botTex][0]
                except:
                    texName = ToonDNA.GirlBottoms[0][0]
            bottomTex = loader.loadTexture(texName)
            bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
            bottomTex.setMagfilter(Texture.FTLinear)
            try:
                bottomColor = ToonDNA.ClothesColors[self.style.botTexColor]
            except:
                bottomColor = ToonDNA.ClothesColors[0]
            # Make the color darker
            darkBottomColor = bottomColor * 0.5
            # Fix the alpha back to 1.0
            darkBottomColor.setW(1.0)

            # import pdb; pdb.set_trace()
            # Now apply all the colors and textures
            for lodName in self.getLODNames():
                thisPart = self.getPart("torso", lodName)
                top = thisPart.find("**/torso-top")
                top.setTexture(shirtTex, 1)
                top.setColor(shirtColor)
                sleeves = thisPart.find("**/sleeves")
                sleeves.setTexture(sleeveTex, 1)
                sleeves.setColor(sleeveColor)
                bottoms = thisPart.findAllMatches("**/torso-bot")
                for bottomNum in range(0, bottoms.getNumPaths()):
                    bottom = bottoms.getPath(bottomNum)
                    bottom.setTexture(bottomTex, 1)
                    bottom.setColor(bottomColor)
                caps = thisPart.findAllMatches("**/torso-bot-cap")
                caps.setColor(darkBottomColor)
        return swappedTorso


    # dialog methods
    def getDialogueArray(self):
        # determine what kind of animal we are
        animalType = self.style.getType()
        if (animalType == "dog"):
            dialogueArray = DogDialogueArray
        elif (animalType == "cat"):
            dialogueArray = CatDialogueArray
        elif (animalType == "horse"):
            dialogueArray = HorseDialogueArray
        elif (animalType == "mouse"):
            dialogueArray = MouseDialogueArray
        elif (animalType == "rabbit"):
            dialogueArray = RabbitDialogueArray
        elif (animalType == "duck"):
            dialogueArray = DuckDialogueArray
        elif (animalType == "monkey"):
            dialogueArray = MonkeyDialogueArray
        elif (animalType == "bear"):
            dialogueArray = BearDialogueArray
        elif (animalType == "pig"):
            dialogueArray = PigDialogueArray
        else:
            dialogueArray = None
        return dialogueArray

    def getShadowJoint(self):
        """
        Return the shadow joint
        """
        if hasattr(self, "shadowJoint"):
            return self.shadowJoint
        shadowJoint = NodePath("shadowJoint")
        for lodName in self.getLODNames():
            joint = self.getPart('legs', lodName).find('**/joint_shadow')
            shadowJoint = shadowJoint.instanceTo(joint)
        self.shadowJoint = shadowJoint
        return shadowJoint

    def getNametagJoints(self):
        """
        Return a list of CharacterJoints for each LOD (1000, 500, 250)
        """
        joints = []
        for lodName in self.getLODNames():
            bundle = self.getPartBundle('legs', lodName)
            joint = bundle.findChild('joint_nameTag')
            if joint:
                joints.append(joint)
        return joints

    def getRightHands(self):
        """
        Return a list of right hands for each LOD (1000, 500, 250)
        """
        return self.rightHands

    def getLeftHands(self):
        """
        Return a list of left hands for each LOD (1000, 500, 250)
        """
        return self.leftHands

    def getHeadParts(self):
        return self.headParts

    def getHipsParts(self):
        return self.hipsParts

    def getTorsoParts(self):
        return self.torsoParts

    def getLegsParts(self):
        return self.legsParts


    def findSomethingToLookAt(self):
        """
        Overrides the function in ToonHead to find a point in the
        world to look at, if possible.
        """
        # Sometimes we just choose randomly
        if ((self.randGen.random() < 0.1) or
            (not hasattr(self, "cr"))):
            x = self.randGen.choice((-0.8, -0.5, 0, 0.5, 0.8))
            y = self.randGen.choice((-0.5, 0, 0.5, 0.8))
            # Now look that direction!
            self.lerpLookAt(Point3(x, 1.5, y), blink=1)
            return

        # Crawl through the doId2do to see if there are objects
        # which support the "getStareAtNodeAndOffset" interface
        # Build up a list of nodes around us and pick one to look at
        nodePathList = []
        for id, obj in self.cr.doId2do.items():
            if (hasattr(obj, "getStareAtNodeAndOffset") and
                (obj!=self)):
                node, offset = obj.getStareAtNodeAndOffset()
                # Only include things in front of us
                if node.getY(self) > 0.0:
                    nodePathList.append((node, offset))
        # If we found some, sort them to see what is closest
        if nodePathList:
            # Sort based on distance, closest first
            nodePathList.sort(lambda x,y: cmp(x[0].getDistance(self), y[0].getDistance(self)))
            # If there are more then two, choose one of the closest 2
            if len(nodePathList) >= 2:
                if (self.randGen.random() < 0.9):
                    # ususally choose the closest
                    chosenNodePath = nodePathList[0]
                else:
                    # sometimes choose the next closest
                    chosenNodePath = nodePathList[1]
            else:
                chosenNodePath = nodePathList[0]
            # Do we want to look or stare? Stare is expensive!
            # TODO: optimize this
            # self.startStareAt(chosenNodePath[0], chosenNodePath[1])
            # Now look that direction!
            self.lerpLookAt(chosenNodePath[0].getPos(self), blink=1)
        else:
            # Didnt find any? Just look randomly
            ToonHead.findSomethingToLookAt(self)


    def setupPickTrigger(self):
        """
        Overrides the similar function from Avatar to position the
        trigger polygon in the appropriate place for a Toon.
        """
        Avatar.Avatar.setupPickTrigger(self)
        torso = self.getPart('torso', '1000')
        if torso == None:
            return 0

        self.pickTriggerNp.reparentTo(torso)
        size = self.style.getTorsoSize()
        if size == 'short':
            self.pickTriggerNp.setPosHprScale(0, 0, 0.5, 0, 0, 0, 1.5, 1.5, 2)
        elif size == 'medium':
            self.pickTriggerNp.setPosHprScale(0, 0, 0.5, 0, 0, 0, 1, 1, 2)
        else: # long
            self.pickTriggerNp.setPosHprScale(0, 0, 1, 0, 0, 0, 1, 1, 2)

        return 1

    def showBooks(self):
        for bookActor in self.getBookActors():
            bookActor.show()

    def hideBooks(self):
        for bookActor in self.getBookActors():
            bookActor.hide()

    def getWake(self):
        """
        Returns the wake object associated with this Toon.  Creates it
        if it has not yet been created.
        """
        if (not self.wake):
            self.wake = Wake.Wake(render, self)
        return self.wake

    def getJar(self):
        """
        Returns the jar object associated with this toon.  Creates it
        if it has not yet been created.
        """
        if not self.jar:
            self.jar = loader.loadModel("phase_5.5/models/estate/jellybeanJar")
            # make it line up with the hands a little better
            self.jar.setP(290.0)
            self.jar.setY(0.5)
            self.jar.setZ(0.5)
            # scale so it's invisible
            self.jar.setScale(0.0)
        return self.jar

    def removeJar(self):
        """
        If it exists, remove the jar object associated with this toon.
        """
        if self.jar:
            self.jar.removeNode()
            self.jar = None


    def setSpeed(self, forwardSpeed, rotateSpeed):
        """setSpeed(self, float forwardSpeed, float rotateSpeed)

        Sets the indicated forward velocity and rotational velocities
        of the toon.  This is used when in the Happy and Sad states to
        determine which animation to play.

        The return value is one of RUN_INDEX, WALK_INDEX, etc., or
        None if the animation does not specialize for the various
        actions.
        """
        self.forwardSpeed = forwardSpeed
        self.rotateSpeed = rotateSpeed

        action = None

        if self.standWalkRunReverse != None:
            # If we have a list of anims to play for stand, walk, and
            # run, then choose the appropriate one and play it.
            if (forwardSpeed >= ToontownGlobals.RunCutOff):
                # Running
                action = OTPGlobals.RUN_INDEX
            elif (forwardSpeed > ToontownGlobals.WalkCutOff):
                # Walking
                action = OTPGlobals.WALK_INDEX
            elif (forwardSpeed < -ToontownGlobals.WalkCutOff):
                # Walking backwards
                action = OTPGlobals.REVERSE_INDEX
            elif (rotateSpeed != 0.0):
                # Spin in place
                action = OTPGlobals.WALK_INDEX
            else:
                # Stand still
                action = OTPGlobals.STAND_INDEX

            anim, rate = self.standWalkRunReverse[action]
            # change the motion state before we proceed
            self.motion.enter()
            self.motion.setState(anim, rate)

            if (anim != self.playingAnim):
                self.playingAnim = anim
                self.playingRate = rate
                self.stop()
                self.loop(anim)
                self.setPlayRate(rate, anim)
                # if we are in disguise, play the anim on the suit body too
                if self.isDisguised:
                    rightHand = self.suit.rightHand
                    numChildren = rightHand.getNumChildren()
                    if numChildren > 0:
                        anim = 'tray-' + anim
                        if anim == 'tray-run':
                            anim = 'tray-walk'
                    self.suit.stop()
                    self.suit.loop(anim)
                    self.suit.setPlayRate(rate, anim)
            elif (rate != self.playingRate):
                self.playingRate = rate
                if not self.isDisguised:
                    self.setPlayRate(rate, anim)
                else:
                    self.suit.setPlayRate(rate, anim)

            # Show wake if moving through water
            # This is determined by your height
            showWake, wakeWaterHeight = ZoneUtil.getWakeInfo()
            # Are we walking below water level?
            # Use the showWake flag to short circuit so we do not need to
            # needlessly check Z against render when we do not want wake
            if (showWake and
                (self.getZ(render) < wakeWaterHeight) and
                (abs(forwardSpeed) > ToontownGlobals.WalkCutOff)):
                currT = globalClock.getFrameTime()
                deltaT =  currT - self.lastWakeTime
                # Create new ripple if it's been long enough
                # since the last one
                if (((action == OTPGlobals.RUN_INDEX) and
                     (deltaT > ToontownGlobals.WakeRunDelta)) or
                    (deltaT > ToontownGlobals.WakeWalkDelta)):
                    self.getWake().createRipple(
                        wakeWaterHeight, rate = 1, startFrame = 4)
                    self.lastWakeTime = currT

        return action

    def enterOff(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.setActiveShadow(0)
        self.playingAnim = None

    def exitOff(self):
        pass

    def enterNeutral(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # make the toon start breathing at a random frame
        anim = "neutral"
        self.pose(anim, int(self.getNumFrames(anim) * self.randGen.random()))
        self.loop(anim, restart=0)
        self.setPlayRate(animMultiplier, anim)
        self.playingAnim = anim
        self.setActiveShadow(0)

    def exitNeutral(self):
        self.stop()

    def enterVictory(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # Do the victory dance.  It "started" ts seconds ago;
        # therefore, begin at the appropriate frame.
        anim = "victory"
        frame = int(ts * self.getFrameRate(anim) * animMultiplier)
        self.pose(anim, frame)
        self.loop("victory", restart=0)
        self.setPlayRate(animMultiplier, "victory")
        self.playingAnim = anim
        self.setActiveShadow(0)

    def exitVictory(self):
        self.stop()

    def enterHappy(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # In this state, the Toon automatically switches between the
        # neutral, walk, and run animations, as appropriate.  This is
        # the normal state for walking around in Toontown.
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ("neutral", 1.0),
            ("walk", 1.0),
            ("run", 1.0),
            ("walk", -1.0)
            )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitHappy(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterSad(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # In this state, the Toon automatically switches between the
        # sad-neutral and sad-walk animations, as appropriate.
        self.playingAnim = 'sad'
        self.playingRate = None
        self.standWalkRunReverse = (
            ("sad-neutral", 1.0),
            ("sad-walk", 1.2),
            ("sad-walk", 1.2),
            ("sad-walk", -1.0)
            )
        self.setSpeed(0, 0)

        # disable body emotes
        Emote.globalEmote.disableBody(self, "toon, enterSad")
        self.setActiveShadow(1)

    def exitSad(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        Emote.globalEmote.releaseBody(self, "toon, exitSad")

    def enterCatching(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        # In this state, the Toon stretches his arms out in a catching
        # pose.
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ("catch-neutral", 1.0),
            ("catch-run", 1.0),
            ("catch-run", 1.0),
            ("catch-run", -1.0)
            )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitCatching(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterCatchEating(self, animMultiplier=1, ts=0,
                         callback=None, extraArgs=[]):
        # In this state, the Toon raises his arm to his mouth
        # in an eating action
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ("catch-eatneutral", 1.0),
            ("catch-eatnrun", 1.0),
            ("catch-eatnrun", 1.0),
            ("catch-eatnrun", -1.0)
            )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(0)

    def exitCatchEating(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterWalk(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("walk")
        self.setPlayRate(animMultiplier, "walk")
        self.setActiveShadow(1)

    def exitWalk(self):
        self.stop()

    def getJumpDuration(self):
        # We check the duration on the legs in case there is a frame
        # mismatch between the various animations for the parts.
        if self.playingAnim == 'neutral':
            return self.getDuration('jump', 'legs')
        else:
            return self.getDuration('running-jump', 'legs')

    def enterJump(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        """
        This jump is the old-style emote jump.  It does't actually get the
        avatar's collision sphere airborne.  It is used for the the mini-
        game victory, for example.
        """
        # don't jump if the toon is disguised a a suit
        if not self.isDisguised:
            if self.playingAnim == 'neutral':
                # ...stopped
                anim = "jump"
            else:
                # ...must be moving!
                anim = "running-jump"
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJump(self):
        self.stop()
        self.playingAnim = "neutral"

    def enterJumpSquat(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # don't jump if the toon is disguised a a suit
        if not self.isDisguised:
            if self.playingAnim == 'neutral':
                # ...stopped
                anim = "jump-squat"
            else:
                # ...must be moving!
                anim = "running-jump-squat"
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            #self.play(anim, fromFrame=0, toFrame=16)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJumpSquat(self):
        self.stop()
        self.playingAnim = "neutral"

    def enterJumpAirborne(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # don't jump if the toon is disguised a a suit
        if not self.isDisguised:
            if self.playingAnim == 'neutral':
                # ...stopped
                anim = "jump-idle"
            else:
                # ...must be moving!
                anim = "running-jump-idle"
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            #self.play(anim, fromFrame=17, toFrame=20)
            self.loop(anim)
        self.setActiveShadow(1)

    def exitJumpAirborne(self):
        self.stop()
        self.playingAnim = "neutral"

    def enterJumpLand(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # don't jump if the toon is disguised as a suit
        if not self.isDisguised:
            if self.playingAnim == 'running-jump-idle':
                # ...must be moving!
                anim = "running-jump-land"
                skipStart = 0.2
            else:
                # ...stopped
                anim = "jump-land"
                skipStart = 0.0
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            #frameCount = self.getNumFrames(anim)
            #self.play(anim, fromFrame=int(frameCount*skipStart), toFrame=frameCount-1)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJumpLand(self):
        self.stop()
        self.playingAnim = "neutral"

    def enterRun(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("run")
        self.setPlayRate(animMultiplier, "run")
        Emote.globalEmote.disableBody(self, "toon, enterRun")
        self.setActiveShadow(1)

    def exitRun(self):
        self.stop()
        Emote.globalEmote.releaseBody(self, "toon, exitRun")

    def enterSwim(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableAll(self, "enterSwim")
        self.playingAnim = "swim"
        self.loop("swim")
        self.setPlayRate(animMultiplier, "swim")
        # Change your orientation to be face up
        self.getGeomNode().setP(-89.0)
        self.dropShadow.hide()
        if self.isLocal():
            self.useSwimControls()
        self.nametag3d.setPos(0, -2, 1)
        # Bobbing task
        self.startBobSwimTask()
        self.setActiveShadow(0)

    def enterCringe(self,animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        #print "cringing"
        self.loop("cringe")
        self.getGeomNode().setPos(0,0,-2)
        self.setPlayRate(animMultiplier,"swim")
        #self.setActiveShadow(0)
        #self.dropShadow.hide()
        #self.nametag3d.setPos(0,-2,1)

    def exitCringe(self,animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        #self.loop("cringe")
        #print "end cringe"
        self.stop()
        self.getGeomNode().setPos(0,0,0)
        self.playingAnim="neutral"
        self.setPlayRate(animMultiplier,"swim")
        #self.setActiveShadow(0)
        #self.dropShadow.hide()
        #self.nametag3d.setPos(0,-2,1)

    def enterDive(self,animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        #print "swimming"
        self.loop("swim")
        #self.pose('swim', 55)
        # 40 is arms back, 20 is arms middle
        if hasattr(self.getGeomNode(), 'setPos'):
            self.getGeomNode().setPos(0,0,-2)
            self.setPlayRate(animMultiplier,"swim")
            self.setActiveShadow(0)
            self.dropShadow.hide()
            self.nametag3d.setPos(0,-2,1)

    def exitDive(self):
        #print "end swim"
        self.stop()
        self.getGeomNode().setPos(0,0,0)
        self.playingAnim="neutral"
        self.dropShadow.show()
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def enterSwimHold(self,animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.getGeomNode().setPos(0,0,-2)
        self.nametag3d.setPos(0,-2,1)
        self.pose('swim', 55)

    def exitSwimHold(self):
        self.stop()
        self.getGeomNode().setPos(0,0,0)
        self.playingAnim="neutral"
        self.dropShadow.show()
        self.nametag3d.setPos(0, 0, self.height + 0.5)
        #self.playingAnim="neutral"

    def exitSwim(self):
        self.stop()
        self.playingAnim = "neutral"
        # Stop bobbing task
        self.stopBobSwimTask()
        self.getGeomNode().setPosHpr(0, 0, 0,
                                     0, 0, 0)
        self.dropShadow.show()
        if self.isLocal():
            self.useWalkControls()
        self.nametag3d.setPos(0, 0, self.height + 0.5)
        Emote.globalEmote.releaseAll(self, "exitSwim")

    def startBobSwimTask(self):
        swimTaskName = self.taskName("swimBobTask")
        taskMgr.remove("swimTask")
        taskMgr.remove(swimTaskName)
        self.getGeomNode().setZ(4.0)
        self.nametag3d.setZ(5.0)
        newTask = Task.loop(
            self.getGeomNode().lerpPosXYZ(0, -3, 3, 1, blendType="easeInOut"),
            self.getGeomNode().lerpPosXYZ(0, -3, 4, 1, blendType="easeInOut")
            )
        taskMgr.add(newTask, swimTaskName)

    def stopBobSwimTask(self):
        swimTaskName = self.taskName("swimBobTask")
        taskMgr.remove(swimTaskName)
        self.getGeomNode().setPos(0, 0, 0)
        self.nametag3d.setZ(1.0)

    def enterOpenBook(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableAll(self, "enterOpenBook")
        self.playingAnim = 'openBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        bookTracks = Parallel()
        for bookActor in self.getBookActors():
            bookTracks.append(ActorInterval(bookActor, 'book',
                                            startTime=1.2, endTime=1.5))
        bookTracks.append(ActorInterval(self, 'book', startTime=1.2,
                          endTime=1.5))

        if hasattr(self, "uniqueName"):
            trackName = self.uniqueName("openBook")
        else:
            trackName = "openBook"
        self.track = Sequence(
            Func(self.showBooks),
            bookTracks,
            Wait(0.1),
            name = trackName)

        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)

        self.track.start(ts)
        self.setActiveShadow(0)

    def exitOpenBook(self):
        self.playingAnim = 'neutralob'
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        self.hideBooks()
        self.startLookAround()
        Emote.globalEmote.releaseAll(self, "exitOpenBook")

    def enterReadBook(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableBody(self, "enterReadBook")
        self.playingAnim = 'readBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        self.showBooks()
        for bookActor in self.getBookActors():
            bookActor.pingpong('book', fromFrame=38, toFrame=118)
        self.pingpong('book', fromFrame=38, toFrame=118)
        self.setActiveShadow(0)

    def exitReadBook(self):
        self.playingAnim = 'neutralrb'
        self.hideBooks()
        for bookActor in self.getBookActors():
            bookActor.stop()
        self.startLookAround()
        Emote.globalEmote.releaseBody(self, "exitReadBook")

    def enterCloseBook(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableAll(self, "enterCloseBook")
        self.playingAnim = 'closeBook'
        bookTracks = Parallel()
        for bookActor in self.getBookActors():
            bookTracks.append(ActorInterval(bookActor, 'book',
                                            startTime=4.96, endTime=6.5))
        bookTracks.append(ActorInterval(self, 'book', startTime=4.96,
                          endTime=6.5))
        if hasattr(self, "uniqueName"):
            trackName = self.uniqueName("closeBook")
        else:
            trackName = "closeBook"
        self.track = Sequence(
            Func(self.showBooks),
            bookTracks,
            Func(self.hideBooks),
            name = trackName)

        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)

        self.track.start(ts)
        self.setActiveShadow(0)

    def exitCloseBook(self):
        self.playingAnim = 'neutralcb'
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self, "exitCloseBook")

    def getSoundTeleport(self):
        # This is loaded on demand so it does not need to be downloaded with the tutorial
        # which does not use it
        if not self.soundTeleport:
            self.soundTeleport = base.loadSfx("phase_3.5/audio/sfx/AV_teleport.mp3")
        return self.soundTeleport

    def getTeleportOutTrack(self, autoFinishTrack = 1):
        def showHoles(holes, hands):
            for hole, hand in zip(holes, hands):
                hole.reparentTo(hand)
        def reparentHoles(holes, toon):
            assert len(holes) == 3
            holes[0].reparentTo(toon)
            holes[1].detachNode()
            holes[2].detachNode()
            # When we throw the hole on the ground, it goes into the
            # shadow bin so it will render correctly w.r.t. the
            # ground.
            holes[0].setBin('shadow', 0)
            holes[0].setDepthTest(0)
            holes[0].setDepthWrite(0)
        def cleanupHoles(holes):
            holes[0].detachNode()
            holes[0].clearBin()
            holes[0].clearDepthTest()
            holes[0].clearDepthWrite()
        holes = self.getHoleActors()
        hands = self.getRightHands()
        holeTrack = Track(
            (0.0, Func(showHoles, holes, hands)),
            (0.5, SoundInterval(self.getSoundTeleport(), node = self)),
            (1.708, Func(reparentHoles, holes, self)),
            (3.4, Func(cleanupHoles, holes)),
            )

        if hasattr(self, "uniqueName"):
            trackName = self.uniqueName("teleportOut")
        else:
            trackName = "teleportOut"

        track = Parallel(holeTrack,
                         name = trackName,
                         autoFinish = autoFinishTrack)
        for hole in holes:
            track.append(ActorInterval(hole, 'hole', duration=3.4))

        track.append(ActorInterval(self, 'teleport', duration=3.4))

        return track

    def enterTeleportOut(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        name = self.name
        if hasattr(self, "doId"):
            name += '-' + str( self.doId)
        self.notify.debug('enterTeleportOut %s' % name)
        if self.ghostMode or self.isDisguised:
            # In ghost mode or in a cog suit, just go straight to the callback.
            if callback:
                callback(*extraArgs)
            return

        self.playingAnim = "teleport"
        Emote.globalEmote.disableAll(self, "enterTeleportOut")

        # If the toon is localToon, we do not want to autofinish this
        # interval. When we lose our connection, we interrupt the
        # ivalMgr. This causes all intervals that are autofinish to
        # actually finish. Finishing TeleportOut makes us transition into
        # the next state (like going to the next hood, estate, pick-a-toon,
        # etc). We actually do not want this final transition to take place
        # if our connection has been lost. If we are a DistributedToon we
        # do need the finish to take place because it has a delay delete
        # flag on it.
        if self.isLocal():
            autoFinishTrack = 0
        else:
            autoFinishTrack = 1

        self.track = self.getTeleportOutTrack(autoFinishTrack)

        # It seems like we do not need these and they are causing leaks
        # self.teleportOutCallback = callback
        # self.teleportOutCallbackArgs = extraArgs

        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getName(), self.finishTeleportOut,
                        [callback, extraArgs])

        # Also, make sure the toon is not visible when he passes
        # through to the other side of the hole (in case there is not
        # a ground plane to obscure him there).  We set up a clip
        # plane at the floor level that only affects the toon.
        holeClip = PlaneNode('holeClip')
        self.holeClipPath = self.attachNewNode(holeClip)
        self.getGeomNode().setClipPlane(self.holeClipPath)
        self.nametag3d.setClipPlane(self.holeClipPath)

        self.track.start(ts)
        self.setActiveShadow(0)

    def finishTeleportOut(self, callback=None, extraArgs=[]):
        # It's necessary to clean up the track in finishTeleportOut
        # (which is called when the track finishes itself) even though
        # it is also being cleaned up in exitTeleportOut (which is
        # called whenever we leave the TeleportOut state).

        # This is because cleaning up the track *might* result in the
        # Toon object being deleted, if this is a DistributedToon on
        # the way out and the only thing keeping it around is a
        # DelayDelete object on the track.  We can't have the Toon be
        # deleted while it is exiting from a state, so we arrange to
        # ensure it will be deleted here, instead.

        name = self.name
        if hasattr(self, "doId"):
            name += '-' + str( self.doId)
        self.notify.debug('finishTeleportOut %s' % name)
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None

        # And again, since we might have been deleted by the above
        # operation, we should check first before we try to move on to
        # the next state.
        if hasattr(self, "animFSM"):
            self.animFSM.request('TeleportedOut')

        if callback:
            callback(*extraArgs)

    def exitTeleportOut(self):
        name = self.name
        if hasattr(self, "doId"):
            name += '-' + str( self.doId)
        self.notify.debug('exitTeleportOut %s' % name)
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            self.track = None

        geomNode = self.getGeomNode()

        if geomNode and (not geomNode.isEmpty()):
            self.getGeomNode().clearClipPlane()
        if self.nametag3d and (not self.nametag3d.isEmpty()):
            self.nametag3d.clearClipPlane()
        if self.holeClipPath:
            self.holeClipPath.removeNode()
            self.holeClipPath = None

        # Because we got hidden at the end of the movie.
        Emote.globalEmote.releaseAll(self, "exitTeleportOut")
        if self and not self.isEmpty():
            self.show()

    def enterTeleportedOut(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # In this state, the toon has finished teleporting out and is
        # gone.  This state is normally transitioned to when the
        # teleportOut animation finishes (but it might be skipped if
        # someone requests a transition to another state while the
        # teleportOut animation is still playing).
        self.setActiveShadow(0)

    def exitTeleportedOut(self):
        pass

    def getDiedInterval(self, autoFinishTrack = 1):
        sound = loader.loadSfx('phase_5/audio/sfx/ENC_Lose.mp3')

        if hasattr(self, "uniqueName"):
            trackName = self.uniqueName("died")
        else:
            trackName = "died"

        ival = Sequence(
            Func(Emote.globalEmote.disableBody, self),
            Func(self.sadEyes),
            Func(self.blinkEyes),
            Track((0, ActorInterval(self, 'lose')),
                  (2, SoundInterval(sound, node = self)),
                  (5.333, self.scaleInterval(1.5, VBase3(0.01, 0.01, 0.01), blendType = 'easeInOut'))),
            Func(self.detachNode),
            Func(self.setScale, 1, 1, 1),
            Func(self.normalEyes),
            Func(self.blinkEyes),
            Func(Emote.globalEmote.releaseBody, self),
            name = trackName,
            autoFinish = autoFinishTrack)

        return ival

    def enterDied(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if self.ghostMode:
            # In ghost mode, just go straight to the callback.
            if callback:
                callback(*extraArgs)
            return

        if self.isDisguised:
            self.takeOffSuit()

        self.playingAnim = "lose"
        Emote.globalEmote.disableAll(self, "enterDied")

        if self.isLocal():
            autoFinishTrack = 0
        else:
            autoFinishTrack = 1

        # extended hack: prevent the jumping code from interfering
        if hasattr(self, 'jumpLandAnimFixTask') and self.jumpLandAnimFixTask:
            self.jumpLandAnimFixTask.remove()
            self.jumpLandAnimFixTask = None

        self.track = self.getDiedInterval(autoFinishTrack)

        # tack the callback right onto the interval, to make sure it gets
        # called if we're interrupted.
        if callback:
            self.track = Sequence(
                self.track,
                Func(callback, *extraArgs),
                autoFinish = autoFinishTrack)

        self.track.start(ts)
        self.setActiveShadow(0)

    def finishDied(self, callback=None, extraArgs=[]):
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None

        if hasattr(self, "animFSM"):
            self.animFSM.request('TeleportedOut')

        if callback:
            callback(*extraArgs)

    def exitDied(self):
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None

        Emote.globalEmote.releaseAll(self, "exitDied")
        self.show()

    def getTeleportInTrack(self):
        hole = self.getHoleActors()[0]
        # Put the hole into the shadow bin so it will render correctly
        # w.r.t. the ground.
        hole.setBin('shadow', 0)
        hole.setDepthTest(0)
        hole.setDepthWrite(0)
        holeTrack = Sequence()
        holeTrack.append(Func(hole.reparentTo, self))
        pos = Point3(0, -2.4, 0)
        holeTrack.append(Func(hole.setPos, self, pos))
        holeTrack.append(ActorInterval(hole, 'hole', startTime=3.4,
                                       endTime=3.1))
        holeTrack.append(Wait(0.6))
        holeTrack.append(ActorInterval(hole, 'hole', startTime=3.1,
                                       endTime=3.4))
        def restoreHole(hole):
            hole.setPos(0, 0, 0)
            hole.detachNode()
            hole.clearBin()
            hole.clearDepthTest()
            hole.clearDepthWrite()
        holeTrack.append(Func(restoreHole, hole))

        toonTrack = Sequence(Wait(0.3),
                             Func(self.getGeomNode().show),
                             Func(self.nametag3d.show),
                             ActorInterval(self, 'jump', startTime=0.45))
        if hasattr(self, "uniqueName"):
            trackName = self.uniqueName("teleportIn")
        else:
            trackName = "teleportIn"
        return (Parallel(holeTrack, toonTrack, name = trackName))

    def enterTeleportIn(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if self.ghostMode or self.isDisguised:
            # In ghost mode, or if we're wearing a cog suit, just go
            # straight to the callback.
            if callback:
                callback(*extraArgs)
            return

        # try to fix invisible toons in minigolf zone
        self.show()

        self.playingAnim = "teleport"
        Emote.globalEmote.disableAll(self, "enterTeleportIn")

        # Start by posing to the last frame of the "teleport"
        # animation, which has the toon below the floor.  That way we
        # won't be visible in some bogus pose briefly before we jump
        # out of the hole.
        self.pose("teleport", self.getNumFrames("teleport") - 1)

        # Do not hide the actual localToon because the camera is under that
        self.getGeomNode().hide()
        # Also hide the nametag3d
        self.nametag3d.hide()

        self.track = self.getTeleportInTrack()

        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)

        self.track.start(ts)
        self.setActiveShadow(0)

    def exitTeleportIn(self):
        self.playingAnim = None
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if not self.ghostMode and not self.isDisguised:
            self.getGeomNode().show()
            self.nametag3d.show()
        Emote.globalEmote.releaseAll(self, "exitTeleportIn")

    def enterSitStart(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'sit-start'

        if (self.isLocal()):
            self.track = Sequence(
                ActorInterval(self, 'sit-start'),
                Func(self.b_setAnimState, 'Sit', animMultiplier),
                )
        else:
            self.track = Sequence(
                ActorInterval(self, 'sit-start'),
                )
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitSitStart(self):
        self.playingAnim = 'neutral'
        if (self.track != None):
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseBody(self)

    def enterSit(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'sit'
        self.loop('sit')
        self.setActiveShadow(0)

    def exitSit(self):
        self.playingAnim = 'neutral'
        Emote.globalEmote.releaseBody(self)

    def enterSleep(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.stopLookAround()
        self.stopBlink()
        self.closeEyes()
        self.lerpLookAt(Point3(0, 1, -4))
        self.loop("neutral")
        self.setPlayRate(animMultiplier * 0.4, "neutral")
        self.setChatAbsolute(SLEEP_STRING, CFThought)
        # This is where we send Toons back to the Toon page after they've
        # been sleeping for a while
        if (self == base.localAvatar):
            print("adding timeout task")
            taskMgr.doMethodLater(self.afkTimeout, self.__handleAfkTimeout,
                                  self.uniqueName('afkTimeout'))
        self.setActiveShadow(0)

    def __handleAfkTimeout(self, task):
        print("handling timeout")
        assert self == base.localAvatar
        self.ignore('wakeup')
        # This will check to see if we're actually wearing a suit before
        # doing anything
        self.takeOffSuit()
        base.cr.playGame.getPlace().fsm.request('final')
        self.b_setAnimState('TeleportOut', 1, self.__handleAfkExitTeleport, [0])
        return Task.done

    def __handleAfkExitTeleport(self, requestStatus):
        self.notify.info('closing shard...')
        base.cr.gameFSM.request('closeShard', ['afkTimeout'])



    def exitSleep(self):
        taskMgr.remove(self.uniqueName('afkTimeout'))
        self.startLookAround()
        self.openEyes()
        self.startBlink()
        if self.nametag.getChat() == SLEEP_STRING:
            self.clearChat()
        self.lerpLookAt(Point3(0, 1, 0), time=0.25)
        self.stop()

    def enterPush(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableBody(self)
        self.playingAnim = 'push'
        self.track = Sequence(
            ActorInterval(self, 'push'),
            )
        self.track.loop()
        self.setActiveShadow(1)

    def exitPush(self):
        self.playingAnim = 'neutral'
        if (self.track != None):
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseBody(self)

    def enterEmote(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if len(extraArgs) > 0:
            emoteIndex = extraArgs[0]
        else:
            return

        self.playingAnim = None
        self.playingRate = None

        self.standWalkRunReverse = (
            ("neutral", 1.0),
            ("walk", 1.0),
            ("run", 1.0),
            ("walk", -1.0)
            )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)

        # Wake the toon up
        if (self.isLocal() and emoteIndex != Emote.globalEmote.EmoteSleepIndex):
            if self.sleepFlag:
                # If we were in sleep mode, switch to happy mode
                # before we play the emote.  Not completely sure why
                # this is necessary.
                self.b_setAnimState("Happy", self.animMultiplier)
            self.wakeUp()

        # Play the emote
        duration = 0
        self.emoteTrack, duration = Emote.globalEmote.doEmote(self, emoteIndex, ts)

        self.setActiveShadow(1)

    def doEmote(self, emoteIndex, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # don't play emotes for toons we are ignoring
        if not self.isLocal():
            if base.cr.avatarFriendsManager.checkIgnored(self.doId):
                return

        # Play the emote
        duration = 0
        if self.isLocal():
            self.wakeUp()
            # Make sure the wake up flags are processed before we play the emote
            if self.hasTrackAnimToSpeed():
                self.trackAnimToSpeed(None)
        self.emoteTrack, duration = Emote.globalEmote.doEmote(self, emoteIndex, ts)

    def __returnToLastAnim(self, task):
        if self.playingAnim:
            self.loop(self.playingAnim)
        else:
            if self.hp > 0:
                self.loop('neutral')
            else:
                self.loop('sad-neutral')
        return Task.done

    def __finishEmote(self, task):
        if self.isLocal():
            if self.hp > 0:
                self.b_setAnimState('Happy')
            else:
                self.b_setAnimState('Sad')
        return Task.done

    def exitEmote(self):
        #self.standWalkRunReverse = None
        #self.motion.exit()
        self.stop()
        if self.emoteTrack != None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        taskMgr.remove(self.taskName('finishEmote'))

    def enterSquish(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableAll(self)
        sound = loader.loadSfx('phase_9/audio/sfx/toon_decompress.mp3')

        lerpTime = .1
        node = self.getGeomNode().getChild(0)
        origScale = node.getScale()
        self.track = Sequence(
            LerpScaleInterval(node, lerpTime, VBase3(2,2,.025), blendType = 'easeInOut'),
            Wait(1.0),
            Parallel(
                     Sequence(Wait(.4),
                              LerpScaleInterval(node, lerpTime, VBase3(1.4,1.4,1.4), blendType = 'easeInOut'),
                              LerpScaleInterval(node, lerpTime/2.0, VBase3(.8,.8,.8), blendType = 'easeInOut'),
                              LerpScaleInterval(node, lerpTime/3.0, origScale, blendType = 'easeInOut'),),
                     ActorInterval(self, 'jump', startTime=.2),
                     SoundInterval(sound),
                     ),
            )
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitSquish(self):
        self.playingAnim = 'neutral'
        if (self.track != None):
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self)

    def enterFallDown(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.playingAnim = 'fallDown'
        Emote.globalEmote.disableAll(self)
        self.track = Sequence(ActorInterval(self,'slip-backward'),
                              name = "fallTrack")
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)

    def exitFallDown(self):
        self.playingAnim = 'neutral'
        if (self.track != None):
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        Emote.globalEmote.releaseAll(self)

    def stunToon(self, ts=0, callback=None, knockdown=0):
        if not self.isStunned:
            if self.stunTrack:
                self.stunTrack.finish()
                self.stunTrack = None

            def setStunned(stunned):
                self.isStunned = stunned
                if self == base.localAvatar:
                    messenger.send("toonStunned-" + str(self.doId), [self.isStunned])

            # setup a track that lerps the transparency of the toon
            # up and down to make him appear to flash.  like he's hurt see.
            node = self.getGeomNode()

            lerpTime = .5
            down = self.doToonColorScale(VBase4(1, 1, 1, 0.6), lerpTime)
            up = self.doToonColorScale(VBase4(1, 1, 1, 0.9), lerpTime)
            clear = self.doToonColorScale(self.defaultColorScale, lerpTime)
            #trackName = "stunTrack-" + str(self.doId)
            #stunTrack = Sequence(name = trackName)
            track = Sequence(Func(setStunned, 1),
                             down,up,down,up,down,up,down,clear,
                             Func(self.restoreDefaultColorScale),
                             Func(setStunned, 0))

            if knockdown:
                self.stunTrack = Parallel(ActorInterval(self, animName='slip-backward'),
                                          track,
                                          )
            else:
                self.stunTrack = track

            self.stunTrack.start()

    def getPieces(self, *pieces):
        """getPieces(self, tuple pieces)

        The arguments to this function are of the form:
        ((partName, (pieceName, pieceName, ..., pieceName)),
         (partName, (pieceName, pieceName, ..., pieceName)),
         ...,
         )

        where partName is the name of one part of the toon,
        e.g. 'torso', 'legs', or 'head', and pieceName are the names
        of nodes that may be found under the partName.  This returns a
        list of all the pieces that match among all LOD's.
        """
        results = []
        for lodName in self.getLODNames():
            for partName, pieceNames in pieces:
                part = self.getPart(partName, lodName)
                if part:
                    if type(pieceNames) == types.StringType:
                        pieceNames = (pieceNames,)
                    for pieceName in pieceNames:
                        npc = part.findAllMatches("**/" + pieceName)
                        for i in range (npc.getNumPaths()):
                            results.append(npc[i])
        return results


    ### Cheesy rendering effects.  This is an experiment in
    ### novelty--can we give cheesy rendering effects as rewards for
    ### quests?

    def applyCheesyEffect(self, effect, lerpTime = 0):
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        
        if self.cheesyEffect != effect:
            oldEffect = self.cheesyEffect
            self.cheesyEffect = effect
            if oldEffect == ToontownGlobals.CENormal:
                self.effectTrack = self.__doCheesyEffect(effect, lerpTime)
            elif effect == ToontownGlobals.CENormal:
                self.effectTrack = self.__undoCheesyEffect(oldEffect, lerpTime)
            else:
                self.effectTrack = Sequence(
                    self.__undoCheesyEffect(oldEffect, lerpTime / 2.0),
                    self.__doCheesyEffect(effect, lerpTime / 2.0))
            self.effectTrack.start()

    def clearCheesyEffect(self, lerpTime = 0):
        self.applyCheesyEffect(ToontownGlobals.CENormal, lerpTime = lerpTime)
        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None

    def __doHeadScale(self, scale, lerpTime):
        if scale == None:
            scale = ToontownGlobals.toonHeadScales[self.style.getAnimal()]

        track = Parallel()
        for hi in range(self.headParts.getNumPaths()):
            head = self.headParts[hi]
            track.append(LerpScaleInterval(head, lerpTime, scale, blendType = 'easeInOut'))
        return track

    def __doLegsScale(self, scale, lerpTime):
        if scale == None:
            scale = 1
            invScale = 1
        else:
            invScale = 1.0 / scale

        track = Parallel()
        for li in range(self.legsParts.getNumPaths()):
            legs = self.legsParts[li]
            torso = self.torsoParts[li]
            track.append(LerpScaleInterval(legs, lerpTime, scale, blendType = 'easeInOut'))
            track.append(LerpScaleInterval(torso, lerpTime, invScale, blendType = 'easeInOut'))
        return track

    def __doToonScale(self, scale, lerpTime):
        if scale == None:
            scale = 1

        node = self.getGeomNode().getChild(0)
        track = Sequence(Parallel(LerpHprInterval(node, lerpTime, Vec3(0.0, 0.0, 0.0), blendType = 'easeInOut'),
                                  LerpScaleInterval(node, lerpTime, scale, blendType = 'easeInOut')),
                         Func(self.resetHeight))
        return track

    def doToonColorScale(self, scale, lerpTime, keepDefault = 0):
        # Apply a color scale to the entire toon, probably to make a
        # transparency effect.  This does not correctly handle scaling
        # the alpha all the way down to 0; see doToonGhostColorScale()
        # for that.

        if keepDefault:
            self.defaultColorScale = scale

        if scale == None:
            scale = VBase4(1, 1, 1, 1)

        node = self.getGeomNode()
        caps = self.getPieces(('torso', ('torso-bot-cap')))

        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        if scale[3] != 1:
            for cap in caps:
                track.append(HideInterval(cap))
        track.append(LerpColorScaleInterval(node, lerpTime, scale, blendType = 'easeInOut'))
        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
            for cap in caps:
                track.append(ShowInterval(cap))
        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))

        return track

    def __doPumpkinHeadSwitch(self, lerpTime, toPumpkin):
        node = self.getGeomNode()

        def getDustCloudIval():
            dustCloud = DustCloud.DustCloud(fBillboard=0,wantSound=1)
            dustCloud.setBillboardAxis(2.)
            dustCloud.setZ(3)
            dustCloud.setScale(0.4)
            dustCloud.createTrack()
            return Sequence(
                Func(dustCloud.reparentTo, self),
                dustCloud.track,
                Func(dustCloud.destroy),
                name = 'dustCloadIval'
                )

        dust = getDustCloudIval()

        track = Sequence()
        if toPumpkin:
            track.append(Func(self.stopBlink))
            track.append(Func(self.closeEyes))
            if(lerpTime > 0.0): # this is to keep the dust cloud from occuring with every generate
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            
            def hideParts():
                self.notify.debug("HidePaths")
                for hi in range(self.headParts.getNumPaths()):
                    head = self.headParts[hi]
                    parts = head.getChildren()
                    for pi in range(parts.getNumPaths()):
                        p = parts[pi]
                        if not p.isHidden():
                            p.hide()
                            p.setTag("pumpkin", "enabled")
                            
            track.append(Func(hideParts))
            track.append(Func(self.enablePumpkins,True))
        else:
            if(lerpTime > 0.0):
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
                
            def showHiddenParts():
                self.notify.debug("ShowHiddenPaths")
                for hi in range(self.headParts.getNumPaths()):
                    head = self.headParts[hi]
                    parts = head.getChildren()
                    for pi in range(parts.getNumPaths()):
                        p = parts[pi]
                        if (not self.pumpkins.hasPath(p)) and p.getTag("pumpkin") == "enabled":
                            p.show()
                            p.setTag("pumpkin", "disabled")
            
            track.append(Func(showHiddenParts))            
            track.append(Func(self.enablePumpkins,False))
            track.append(Func(self.startBlink))
        return track
        
    def __doSnowManHeadSwitch(self, lerpTime, toSnowMan):
        node = self.getGeomNode()

        def getDustCloudIval():
            dustCloud = DustCloud.DustCloud(fBillboard=0,wantSound=0)
            dustCloud.setBillboardAxis(2.)
            dustCloud.setZ(3)
            dustCloud.setScale(0.4)
            dustCloud.createTrack()
            return Sequence(
                Func(dustCloud.reparentTo, self),
                dustCloud.track,
                Func(dustCloud.destroy),
                name = 'dustCloadIval'
                )

        dust = getDustCloudIval()

        track = Sequence()
        if toSnowMan:
            track.append(Func(self.stopBlink))
            track.append(Func(self.closeEyes))
            if(lerpTime > 0.0): # this is to keep the dust cloud from occuring with every generate
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            
            def hideParts():
                self.notify.debug("HidePaths")
                for hi in range(self.headParts.getNumPaths()):
                    head = self.headParts[hi]
                    parts = head.getChildren()
                    for pi in range(parts.getNumPaths()):
                        p = parts[pi]
                        if not p.isHidden():
                            p.hide()
                            p.setTag("snowman", "enabled")
                            
            track.append(Func(hideParts))
            track.append(Func(self.enableSnowMen,True))
        else:
            if(lerpTime > 0.0):
                track.append(Func(dust.start))
                track.append(Wait(0.5))
            else:
                dust.finish()
            def showHiddenParts():
                self.notify.debug("ShowHiddenPaths")
                
                for hi in range(self.headParts.getNumPaths()):
                    head = self.headParts[hi]
                    parts = head.getChildren()
                    for pi in range(parts.getNumPaths()):
                        p = parts[pi]
                        if (not self.snowMen.hasPath(p)) and p.getTag("snowman") == "enabled":
                            p.show()
                            p.setTag("snowman", "disabled")
                            
            track.append(Func(showHiddenParts))    
            track.append(Func(self.enableSnowMen,False))
            track.append(Func(self.startBlink))
        return track

    def __doBigAndWhite(self, color, scale, lerpTime):
        # call the two existing functions and combine the tracks
        track = Parallel()
        track.append(self.__doToonColor(color, lerpTime))
        track.append(self.__doToonScale(scale, lerpTime))
        return track

    def __doVirtual(self):
        # call the two existing functions and combine the tracks
        track = Parallel()
        track.append(self.__doToonColor(VBase4(0.25, 0.25, 1.0, 1), 0.0))
        self.setPartsAdd(self.getHeadParts())
        self.setPartsAdd(self.getTorsoParts())
        self.setPartsAdd(self.getHipsParts())
        self.setPartsAdd(self.getLegsParts())
        #self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        #self.setDepthWrite(False)
        #self.setBin('fixed', 1)
        return track

    def __doUnVirtual(self):
        # call the two existing functions and combine the tracks
        track = Parallel()
        track.append(self.__doToonColor(None, 0.0))
        self.setPartsNormal(self.getHeadParts(), 1)
        self.setPartsNormal(self.getTorsoParts(), 1)
        self.setPartsNormal(self.getHipsParts(), 1)
        self.setPartsNormal(self.getLegsParts(), 1)
        #self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
        #self.setDepthWrite(True)
        #self.setBin('default', 0)
        return track

    def setPartsAdd(self, parts):
        #actorNode = self.find("**/__Actor_modelRoot")
        actorCollection = parts #self.getHeadParts() #actorNode.findAllMatches("*")
        for thingIndex in range(0,actorCollection.getNumPaths()):
            thing = actorCollection[thingIndex]
            if thing.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                thing.setDepthWrite(False)
                self.setBin('fixed', 1)


    def setPartsNormal(self, parts, alpha = 0):
        #actorNode = self.find("**/__Actor_modelRoot")
        actorCollection = parts
        for thingIndex in range(0,actorCollection.getNumPaths()):
            thing = actorCollection[thingIndex]
            if thing.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
                thing.setDepthWrite(True)
                self.setBin('default', 0)
                if alpha:
                    thing.setTransparency(1)
                    thing.setBin('transparent', 0)

    def __doToonGhostColorScale(self, scale, lerpTime, keepDefault = 0):

        # This is similar to doToonColorScale, above, except it has
        # additional support for scaling the alpha all the way down to
        # 0 and back again (in particular, it does a show and hide at
        # alpha 0).

        # This doesn't work when toons might be wearing a cog suit,
        # which also monkeys with the show/hide transition on the geom
        # node.  But we only use this method to implement ghost mode,
        # which is currently only invoked in move-furniture mode or
        # via a magic word.

        if keepDefault:
            self.defaultColorScale = scale

        if scale == None:
            scale = VBase4(1, 1, 1, 1)

        node = self.getGeomNode()
        caps = self.getPieces(('torso', ('torso-bot-cap')))

        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        track.append(ShowInterval(node))
        if scale[3] != 1:
            for cap in caps:
                track.append(HideInterval(cap))
        track.append(LerpColorScaleInterval(node, lerpTime, scale, blendType = 'easeInOut'))
        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
            for cap in caps:
                track.append(ShowInterval(cap))
        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))
            track.append(HideInterval(node))

        return track

    def restoreDefaultColorScale(self):
        # Restore the currently active color scale (e.g. after
        # temporarily changing it with a resistance chat or ouch
        # effect).
        node = self.getGeomNode()
        if node:
            if self.defaultColorScale:
                node.setColorScale(self.defaultColorScale)
                if self.defaultColorScale[3] != 1:
                    node.setTransparency(1)
                else:
                    node.clearTransparency()
            else:
                node.clearColorScale()
                node.clearTransparency()

    def __doToonColor(self, color, lerpTime):
        node = self.getGeomNode()

        # Can't lerp setColor, so this is always an instant lerp.
        if color == None:
            return Func(node.clearColor)
        else:
            # An override of 1 to override toon color (but not shadow color)
            return Func(node.setColor, color, 1)

    def __doPartsColorScale(self, scale, lerpTime):
        # color scale only the fleshy parts of the toon--an "invisible man" effect.
        if scale == None:
            scale = VBase4(1, 1, 1, 1)

        node = self.getGeomNode()
        pieces = self.getPieces(('torso', ('arms', 'neck')),
                                ('legs', ('legs', 'feet')),
                                ('head', ('+GeomNode')))
        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        for piece in pieces:
            # Hide/Show only the neutral muzzle. Don't do anything to the emote muzzles.
            if (piece.getName()[:7] == 'muzzle-') and (piece.getName()[-8:] != '-neutral'):
                continue
            track.append(ShowInterval(piece))

        p1 = Parallel()
        for piece in pieces:
            # Hide/Show only the neutral muzzle. Don't do anything to the emote muzzles.
            if (piece.getName()[:7] == 'muzzle-') and (piece.getName()[-8:] != '-neutral'):
                continue
            p1.append(LerpColorScaleInterval(piece, lerpTime, scale, blendType = 'easeInOut'))
        track.append(p1)

        if scale[3] == 1:
            track.append(Func(node.clearTransparency))
        elif scale[3] == 0:
            track.append(Func(node.clearTransparency))
            for piece in pieces:
                # Hide/Show only the neutral muzzle. Don't do anything to the emote muzzles.
                if (piece.getName()[:7] == 'muzzle-') and (piece.getName()[-8:] != '-neutral'):
                    continue
                track.append(HideInterval(piece))

        return track

    def __doCheesyEffect(self, effect, lerpTime):
        # Returns a track that applies the given effect from a normal state.
        if effect == ToontownGlobals.CEBigHead:
            return self.__doHeadScale(2.5, lerpTime)
        elif effect == ToontownGlobals.CESmallHead:
            return self.__doHeadScale(0.5, lerpTime)
        elif effect == ToontownGlobals.CEBigLegs:
            return self.__doLegsScale(1.4, lerpTime)
        elif effect == ToontownGlobals.CESmallLegs:
            return self.__doLegsScale(0.6, lerpTime)
        elif effect == ToontownGlobals.CEBigToon:
            return self.__doToonScale(ToontownGlobals.BigToonScale, lerpTime)
        elif effect == ToontownGlobals.CESmallToon:
            return self.__doToonScale(ToontownGlobals.SmallToonScale, lerpTime)
        elif effect == ToontownGlobals.CEFlatPortrait:
            return self.__doToonScale(VBase3(1, 0.05, 1), lerpTime)
        elif effect == ToontownGlobals.CEFlatProfile:
            return self.__doToonScale(VBase3(0.05, 1, 1), lerpTime)
        elif effect == ToontownGlobals.CETransparent:
            return self.doToonColorScale(VBase4(1, 1, 1, 0.6), lerpTime, keepDefault = 1)
        elif effect == ToontownGlobals.CENoColor:
            return self.__doToonColor(VBase4(1, 1, 1, 1), lerpTime)
        elif effect == ToontownGlobals.CEInvisible:
            return self.__doPartsColorScale(VBase4(1, 1, 1, 0), lerpTime)
        elif effect == ToontownGlobals.CEPumpkin:
            return self.__doPumpkinHeadSwitch(lerpTime,toPumpkin = True)
        elif effect == ToontownGlobals.CEBigWhite:
            return self.__doBigAndWhite(VBase4(1, 1, 1, 1), ToontownGlobals.BigToonScale, lerpTime)
        elif effect == ToontownGlobals.CESnowMan:
            return self.__doSnowManHeadSwitch(lerpTime, toSnowMan = True)
        elif effect == ToontownGlobals.CEVirtual:
            return self.__doVirtual()
        elif effect == ToontownGlobals.CEGhost:
            alpha = 0
            if localAvatar.seeGhosts:
                alpha = 0.2
            return Sequence(
                self.__doToonGhostColorScale(VBase4(1, 1, 1, alpha), lerpTime, keepDefault = 1),
                Func(self.nametag3d.hide))

        # Invalid effect.
        return Sequence()

    def __undoCheesyEffect(self, effect, lerpTime):
        # Returns a track that returns from the given effect to a normal state.
        if effect == ToontownGlobals.CEBigHead:
            return self.__doHeadScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallHead:
            return self.__doHeadScale(None, lerpTime)
        if effect == ToontownGlobals.CEBigLegs:
            return self.__doLegsScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallLegs:
            return self.__doLegsScale(None, lerpTime)
        elif effect == ToontownGlobals.CEBigToon:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CESmallToon:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CEFlatPortrait:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CEFlatProfile:
            return self.__doToonScale(None, lerpTime)
        elif effect == ToontownGlobals.CETransparent:
            return self.doToonColorScale(None, lerpTime, keepDefault = 1)
        elif effect == ToontownGlobals.CENoColor:
            return self.__doToonColor(None, lerpTime)
        elif effect == ToontownGlobals.CEInvisible:
            return self.__doPartsColorScale(None, lerpTime)
        elif effect == ToontownGlobals.CEPumpkin:
            return self.__doPumpkinHeadSwitch(lerpTime,toPumpkin = False)
        elif effect == ToontownGlobals.CEBigWhite:
            return self.__doBigAndWhite(None, None, lerpTime)
        elif effect == ToontownGlobals.CESnowMan:
            return self.__doSnowManHeadSwitch(lerpTime, toSnowMan = False)
        elif effect == ToontownGlobals.CEVirtual:
            return self.__doUnVirtual()
        elif effect == ToontownGlobals.CEGhost:
            return Sequence(
                Func(self.nametag3d.show),
                self.__doToonGhostColorScale(None, lerpTime, keepDefault = 1))

        # Invalid effect.
        return Sequence()


    # special methods for making a toon put on and take off a suit disguise for the cog HQ
    def putOnSuit(self, suitType, setDisplayName=True):
        # suitType = suit dna string (ie "le" for legal eagle)
        if self.isDisguised:
            self.takeOffSuit()

        if not launcher.getPhaseComplete(5):
            # If we haven't downloaded phase 5 yet, don't attempt to
            # wear a suit; that will just crash the client.  This
            # should only be possible if someone is hacking us to wear
            # a suit in the playground.
            return

        # make sure this is a valid suit name
        assert suitType in SuitDNA.suitHeadTypes

        from toontown.suit import Suit

        # generate suit geometry based on this dna
        suit = Suit.Suit()
        dna = SuitDNA.SuitDNA()
        dna.newSuit(suitType)
        suit.setStyle(dna)
        suit.isDisguised = 1
        suit.generateSuit()
        suit.initializeDropShadow()
        suit.setPos(self.getPos())
        suit.setHpr(self.getHpr())
        # hide the suit head as the toon head will be used
        for part in suit.getHeadParts():
            part.hide()

        # reparent the toon head to the suit
        suitHeadNull = suit.find("**/joint_head")
        toonHead = self.getPart('head', '1000')

        # turn off emotions
        Emote.globalEmote.disableAll(self)

        # hide the toon geometry
        toonGeom = self.getGeomNode()
        toonGeom.hide()

        # preserve scale on the head
        worldScale = toonHead.getScale(render)
        self.headOrigScale = toonHead.getScale()
        # we need to add an intermediate node to the head to make the offset work with scale
        headPosNode = hidden.attachNewNode("headPos")
        toonHead.reparentTo(headPosNode)
        toonHead.setPos(0, 0, 0.2)
        headPosNode.reparentTo(suitHeadNull)
        headPosNode.setScale(render, worldScale)
        # reparent the suit geom to the toon
        suitGeom = suit.getGeomNode()
        suitGeom.reparentTo(self)

        # save these for later
        self.suit = suit
        self.suitGeom = suitGeom
        self.setHeight(suit.getHeight())
        self.nametag3d.setPos(0, 0, self.height + 1.3)



        # if we are local hide the sticker book and alter our walk speed
        if self.isLocal():
            if hasattr(self, "book"):
                self.book.obscureButton(1)

            # make toon move at suit movement rates
            self.oldForward = ToontownGlobals.ToonForwardSpeed
            self.oldReverse = ToontownGlobals.ToonReverseSpeed
            self.oldRotate = ToontownGlobals.ToonRotateSpeed
            ToontownGlobals.ToonForwardSpeed = ToontownGlobals.SuitWalkSpeed
            ToontownGlobals.ToonReverseSpeed = ToontownGlobals.SuitWalkSpeed
            ToontownGlobals.ToonRotateSpeed = ToontownGlobals.ToonRotateSlowSpeed

            # stop and restart to make sure these values "take"
            if self.hasTrackAnimToSpeed():
                self.stopTrackAnimToSpeed()
                self.startTrackAnimToSpeed()

            # turn off jump ability
            self.controlManager.disableAvatarJump()

            # add some suit phrases to the speed chat
            indices = range(OTPLocalizer.SCMenuCommonCogIndices[0], OTPLocalizer.SCMenuCommonCogIndices[1] + 1)
            customIndices = OTPLocalizer.SCMenuCustomCogIndices[suitType]
            indices += range(customIndices[0], customIndices[1] + 1)
            self.chatMgr.chatInputSpeedChat.addCogMenu(indices)

        # make sure we start in neutral
        self.suit.loop("neutral")


        # set the flag
        self.isDisguised = 1

        # make our chat and name display the suit font
        self.setFont(ToontownGlobals.getSuitFont())
        if setDisplayName:
            # determine which dept this suit is in order to display the correct level info
            # We print the suit name instead of the dept name, 'cause
            # that's what people care about more.
            suitDept = SuitDNA.suitDepts.index(SuitDNA.getSuitDept(suitType))
            suitName = SuitBattleGlobals.SuitAttributes[suitType]['name']
            self.nametag.setDisplayName(TTLocalizer.SuitBaseNameWithLevel % {
                "name": self.getName(),
                "dept": suitName,
                "level": self.cogLevels[suitDept] + 1})
            self.nametag.setNameWordwrap(9.0)



    def takeOffSuit(self):
        # make sure we are a suit first
        if not self.isDisguised:
            return

        suitType = self.suit.style.name

        # put the toon head back on the toon body
        toonHeadNull = self.find("**/1000/**/def_head")
        if not toonHeadNull:
            toonHeadNull = self.find("**/1000/**/joint_head")
        toonHead = self.getPart('head', '1000')
        toonHead.reparentTo(toonHeadNull)

        # reset the scale and position on the toon head
        toonHead.setScale(self.headOrigScale)
        toonHead.setPos(0,0,0)

        # clean up the intermedita node
        headPosNode = self.suitGeom.find("**/headPos")
        headPosNode.removeNode()

        # hide the suit body
        self.suitGeom.reparentTo(self.suit)
        self.resetHeight()
        self.nametag3d.setPos(0, 0, self.height + 0.5)

        # show the toon geom
        toonGeom = self.getGeomNode()
        toonGeom.show()

        # turn emotes back on
        Emote.globalEmote.releaseAll(self)

        # set the flag
        self.isDisguised = 0

        # turn our font back to the toon font
        self.setFont(ToontownGlobals.getToonFont())
        self.nametag.setNameWordwrap(-1)
        self.setDisplayName(self.getName())

        # if we are local show the sticker book again and reset toon walk speeds
        if self.isLocal():
            if hasattr(self, "book"):
                self.book.obscureButton(0)

            # restore toon movement rates
            ToontownGlobals.ToonForwardSpeed = self.oldForward
            ToontownGlobals.ToonReverseSpeed = self.oldReverse
            ToontownGlobals.ToonRotateSpeed = self.oldRotate

            # stop and restart to make sure these values "take"
            if self.hasTrackAnimToSpeed():
                self.stopTrackAnimToSpeed()
                self.startTrackAnimToSpeed()

            del(self.oldForward)
            del(self.oldReverse)
            del(self.oldRotate)

            # turn jump ability back on
            self.controlManager.enableAvatarJump()

            # remove the cog chat phrases
            self.chatMgr.chatInputSpeedChat.removeCogMenu()


        # clean up these temp var's
        self.suit.delete()
        del(self.suit)
        del(self.suitGeom)

    def makeWaiter(self):
        # Convenience func to make disguise toon look like cog waiter
        if not self.isDisguised:
            return
        self.suit.makeWaiter(self.suitGeom)

    def getPieModel(self):
        # Returns a pie prop for the following intervals.  This is
        # also saved in self.pieModel.
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps

        if self.pieModel != None and self.__pieModelType != self.pieType:
            # Throw away the old pie; we need to get a new pie type.
            self.pieModel.detachNode()
            self.pieModel = None

        if self.pieModel == None:
            self.__pieModelType = self.pieType
            pieName = ToontownBattleGlobals.pieNames[self.pieType]
            self.pieModel = BattleProps.globalPropPool.getProp(pieName)

        return self.pieModel

    def getPresentPieInterval(self, x, y, z, h, p, r):
        # Returns an interval to show the avatar pulling out a pie and
        # weighing it before tossing.  See getTossPieInterval().
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps
        from toontown.battle import MovieUtil

        pie = self.getPieModel()
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        pieType = BattleProps.globalPropPool.getPropType(pieName)
        animPie = Sequence()
        pingpongPie = Sequence()
        if pieType == 'actor':
            animPie = ActorInterval(pie, pieName, startFrame = 0,
                                    endFrame = 31)
            pingpongPie = Func(pie.pingpong, pieName, fromFrame=32, toFrame=47)

        track = Sequence(
            Func(self.setPosHpr, x, y, z, h, p, r),
            Func(pie.reparentTo, self.rightHand),
            Func(pie.setPosHpr, 0, 0, 0, 0, 0, 0),
            Parallel(pie.scaleInterval(1, pie.getScale(),
                                       startScale = MovieUtil.PNT3_NEARZERO),
                     ActorInterval(self, 'throw', startFrame = 0,
                                   endFrame = 31),
                     animPie),
            Func(self.pingpong, 'throw', fromFrame=32, toFrame=47),
            pingpongPie,
            )
        return track

    def getTossPieInterval(self, x, y, z, h, p, r, power,
                           beginFlyIval = Sequence()):
        # Returns (toss, pie, flyPie), where toss is an interval to
        # animate the toon tossing a pie, pie is the interval to
        # animate the pie flying through the air, and pieModel is the
        # model that flies.  This is used in the final BossBattle
        # sequence of CogHQ when we all throw pies directly at the
        # boss cog.

        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps

        pie = self.getPieModel()
        flyPie = pie.copyTo(NodePath('a'))
        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        pieType = BattleProps.globalPropPool.getPropType(pieName)
        animPie = Sequence()
        if pieType == 'actor':
            animPie = ActorInterval(pie, pieName, startFrame = 48)

        sound = loader.loadSfx('phase_3.5/audio/sfx/AA_pie_throw_only.mp3')

        # First, create a ProjectileInterval to compute the relative
        # velocity.

        t = power / 100.0

        # Distance ranges from 100 - 20 ft, time ranges from 1 - 1.5 s.
        dist = 100 - 70 * t
        time = 1 + 0.5 * t
        proj = ProjectileInterval(
            None, startPos = Point3(0, 0, 0), endPos = Point3(0, dist, 0),
            duration = time)
        relVel = proj.startVel

        def getVelocity(toon = self, relVel = relVel):
            return render.getRelativeVector(toon, relVel)

        toss = Track(
            (0, Sequence(Func(self.setPosHpr, x, y, z, h, p, r),
                         Func(pie.reparentTo, self.rightHand),
                         Func(pie.setPosHpr, 0, 0, 0, 0, 0, 0),
                         Parallel(ActorInterval(self, 'throw', startFrame = 48),
                                  animPie),
                         Func(self.loop, 'neutral'),
                         )),
            (16./24., Func(pie.detachNode)))

        fly = Track(
            (14./24., SoundInterval(sound, node = self)),
            (16./24.,
             Sequence(Func(flyPie.reparentTo, render),
                      Func(flyPie.setPosHpr, self,
                           0.52, 0.97, 2.24,
                           89.42, -10.56, 87.94),
                      beginFlyIval,
                      ProjectileInterval(flyPie, startVel = getVelocity, duration = 3),
                      Func(flyPie.detachNode),
                      )),
            )
        return (toss, fly, flyPie)

    def getPieSplatInterval(self, x, y, z, pieCode):
        # Returns an interval showing a pie hitting a target in the
        # world.  See getTossPieInterval(), above.
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps

        pieName = ToontownBattleGlobals.pieNames[self.pieType]
        splatName = 'splat-%s' % (pieName)
        if (pieName == 'lawbook'):
            #we need to create a splat-lawbook asset, while there is none, use the dust instead
            splatName = 'dust'
        splat = BattleProps.globalPropPool.getProp(splatName)
        splat.setBillboardPointWorld(2)

        color = ToontownGlobals.PieCodeColors.get(pieCode)
        if color:
            splat.setColor(*color)

        vol = 1.0
        if (pieName == 'lawbook'):
            sound = loader.loadSfx('phase_11/audio/sfx/LB_evidence_miss.mp3')
            vol = 0.25
        else:
            sound = loader.loadSfx('phase_4/audio/sfx/AA_wholepie_only.mp3')

        ival = Parallel(
            Func(splat.reparentTo, render),
            Func(splat.setPos, x, y, z),
            SoundInterval(sound, node = splat, volume = vol),
            Sequence(ActorInterval(splat, splatName),
                     Func(splat.detachNode)),
            )
        return ival

    def cleanupPieModel(self):
        # Make sure the pie model doesn't stay stuck to the Toon's
        # hand.
        if self.pieModel != None:
            self.pieModel.detachNode()
            self.pieModel = None

    def getFeedPetIval(self):
        return Sequence( ActorInterval(self, "feedPet"),
                         Func(self.animFSM.request, "neutral"))
        #return ActorInterval(self, "feedPet")

    def getScratchPetIval(self):
        return Sequence( ActorInterval(self, "pet-start"),
                         ActorInterval(self, "pet-loop"),
                         ActorInterval(self, "pet-end") )

    def getCallPetIval(self):
        return ActorInterval(self, "callPet")


    def enterGolfPuttLoop(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("loop-putt")

    def exitGolfPuttLoop(self):
        self.stop()

    def enterGolfRotateLeft(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("rotateL-putt")

    def exitGolfRotateLeft(self):
        self.stop()

    def enterGolfRotateRight(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("rotateR-putt")

    def exitGolfRotateRight(self):
        self.stop()

    def enterGolfPuttSwing(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("swing-putt")

    def exitGolfPuttSwing(self):
        self.stop()

    def enterGolfGoodPutt(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("good-putt", restart=0)

    def exitGolfGoodPutt(self):
        self.stop()

    def enterGolfBadPutt(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop("badloop-putt", restart=0)

    def exitGolfBadPutt(self):
        self.stop()

    def enterFlattened(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        Emote.globalEmote.disableAll(self)
        sound = loader.loadSfx('phase_9/audio/sfx/toon_decompress.mp3')

        lerpTime = .1
        node = self.getGeomNode().getChild(0)
        self.origScale = node.getScale()
        self.track = Sequence(
            LerpScaleInterval(node, lerpTime, VBase3(2,2,.025), blendType = 'easeInOut'),
            )
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitFlattened(self):
        self.playingAnim = 'neutral'
        if (self.track != None):
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        node = self.getGeomNode().getChild(0)
        node.setScale(self.origScale)
        Emote.globalEmote.releaseAll(self)

    def enterCogThiefRunning(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        """Enter the running state for the cog thief minigame."""
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ("neutral", 1.0),
            ("run", 1.0),
            ("run", 1.0),
            ("run", -1.0)
            )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitCogThiefRunning(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()        
        
    def enterScientistJealous(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        self.loop("scientistJealous")

    def exitScientistJealous(self):
        self.stop()
   
    def enterScientistEmcee(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        #self.loop("scientistEmcee", fromFrame = 1, toFrame = 315)
        self.loop("scientistEmcee")

    def exitScientistEmcee(self):
        self.stop()
        
    def enterScientistWork(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        self.loop("scientistWork")

    def exitScientistWork(self):
        self.stop()
        
    def enterScientistLessWork(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        self.loop("scientistWork", fromFrame = 319, toFrame=619)

    def exitScientistLessWork(self):
        self.stop()
        
    def enterScientistPlay(self, animMultiplier=1, ts=0,
                      callback=None, extraArgs=[]):
        self.loop("scientistGame")
        if hasattr(self, 'scientistPlay'):
            self.scientistPlay()

    def exitScientistPlay(self):
        self.stop()

# module calls
loadModels()
compileGlobalAnimList()

