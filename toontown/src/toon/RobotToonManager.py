# Is being run outside of Toontown? Then you need to create a window
# and a base
try:
    base
except NameError:
    from direct.directbase import DirectStart
    # Let the world know there is no localAvatar
    base.localAvatar = None

from direct.showbase.DirectObject import DirectObject
from direct.showbase import ShowBase
from RobotToon import *
from toontown.battle.BattleProps import *
from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals
from pandac.PandaModules import *
from toontown.leveleditor.PieMenu import *
from direct.directtools.DirectSelection import SelectionRay
from direct.showbase.TkGlobal import *
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from tkSimpleDialog import askstring, askfloat
from tkMessageBox import showwarning, showinfo
from direct.tkwidgets.AppShell import *
from direct.tkwidgets.SceneGraphExplorer import *
from direct.interval.IntervalGlobal import *
from toontown.battle.SuitBattleGlobals import SuitAttributes
from toontown.makeatoon import NameGenerator
from direct.tkwidgets import Valuator
from direct.tkwidgets import Slider
import ToonDNA
from direct.task.Task import Task
from toontown.suit import SuitDNA
from toontown.suit import Suit
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
import __builtin__
from toontown.hood import SkyUtil
from direct.distributed.PyDatagram import PyDatagram
from toontown.pets import PetDNA
import sys, os
import string
import Pmw

from toontown.leveleditor.LevelStyleManager import *

from toontown.effects import Fireworks, FireworkShows, FireworkGlobals
from toontown.battle import BattleParticles

try:
    if direct is None:
        base.startDirect()
except AttributeError:
    base.startDirect()

# Note: While adding names to the ToonTopsDict make sure there is a space after the number.
# For eg: 'xx - ' and not 'xx-'. The code will crash if there is no space.
ToonTopsDict = {
    0 : '00 - solid',
    1 : '01 - single stripe',
    2 : '02 - collar',
    3 : '03 - double stripe',
    4 : '04 - multiple stripes',
    5 : '05 - collar w/ pocket',
    6 : '06 - flower print',
    7 : '07 - flower trim',
    8 : '08 - hawaiian',
    9 : '09 - collar w/ 2 pockets',
    10 : '10 - bowling shirt ',
    11 : '11 - special, vest',
    12 : '12 - denim vest',
    13 : '13 - peasant',
    14 : '14 - collar w/ ruffles',
    15 : '15 - peasant w/ mid stripe',
    16 : '16 - soccer jersey',
    17 : '17 - lightning bolt',
    18 : '18 - jersey 19',
    19 : '19 - guayavera',
    20 : '20 - hearts',
    21 : '21 - stars',
    22 : '22 - flower',
    23 : '23 - blue with 3 yellow stripes',
    24 : '24 - pink and beige with flower',
    25 : '25 - yellow hooded sweatshirt',
    26 : '26 - blue stripes',
    27 : '27 - yellow with palm tree',
    28 : '28 - orange',
    29 : '29 - ghost (Halloween)',
    30 : '30 - pumpkin (Halloween)',
    31 : '31 - snowman (Winter Holiday)',
    32 : '32 - snowflakes (Winter Holiday)',
    33 : '33 - candy canes (Winter Holiday)',
    34 : '34 - scarf (Winter Holiday)',
    35 : '35 - Blue and gold wavy stripes',
    36 : '36 - Blue and pink with bows',
    37 : '37 - Lime green with stripe',
    38 : '38 - Purple with stars',
    39 : '39 - Red kimono with checkerboard',
    40 : '40 - Aqua kimono with white stripes',
    41 : '41 - Pink heart border (Valentine)',
    42 : '42 - Red hearts (Valentine)',
    43 : '43 - Winged heart (Valentine)',
    44 : '44 - Flaming heart (Valentine)',
    45 : '45 - Tie Dye',
    46 : '46 - Blue and white stripe',
    47 : '47 - (St. Pats) Four Leaf Clover',
    48 : '48 - (St. Pats) Pot O Gold',
    49 : '49 - (T-shirt Contest) Fishing Vest',
    50 : '50 - (T-shirt Contest) Fish Tank',
    51 : '51 - (T-shirt Contest) Paw Print',
    52 : '52 - (Western) Cowboy Shirt',
    53 : '53 - (Western) Cowboy Shirt',
    54 : '54 - (Western) Cowboy Shirt',
    55 : '55 - (Western) Cowboy Shirt',
    56 : '56 - (Western) Cowboy Shirt',
    57 : '57 - (Western) Cowboy Shirt',
    58 : '58 - (July 4th) Flag Shirt',
    59 : '59 - (July 4th) Fireworks Shirt',
    60 : '60 - (Catalog 7) Green Shirt',
    61 : '61 - (Catalog 7) Purple w/Flower Shirt',
    62 : '62 - (T-shirtContest 2) Multicolor shirt w/ backpack',
    63 : '63 - (T-shirtContest 2) Lederhosen',
    64 : '64 - (T-shirtContest 2) Watermelon',
    65 : '65 - (T-shirtContest 2) Race Shirt (UK winner)',

    # Pyjama series
    66 : '66 - Blue Banana Pajama shirt',
    67 : '67 - Red Horn Pajama shirt',
    68 : '68 - Purple Glasses Pajama shirt',

    # 2009 Valentines Day Shirts
    69 : '69 - Valentines Shirt 1',
    70 : '70 - Valentines Shirt 2',
    
    # Special award shirts
    71 : '71 - Striped Shirt',
    72 : '72 - Fishing Shirt 1',
    73 : '73 - Fishing Shirt 2',
    74 : '74 - Gardening Shirt 1',
    75 : '75 - Gardening Shirt 2',
    76 : '76 - Party Shirt 1',
    77 : '77 - Party Shirt 2',
    78 : '78 - Racing Shirt 1',
    79 : '79 - Racing Shirt 2',
    80 : '80 - Summer Shirt 1',
    81 : '81 - Summer Shirt 2',    
    82 : '82 - Golf Shirt 1',
    83 : '83 - Golf Shirt 2',
    84 : '84 - Halloween Costume Shirt 1',
    85 : '85 - Halloween Costume Shirt 2',
    86 : '86 - Marathon Shirt 1',
    87 : '87 - Save Building Shirt 1',
    88 : '88 - Save Building Shirt 2',
    89 : '89 - Toontask Shirt 1',
    90 : '90 - Toontask Shirt 2',
    91 : '91 - Trolley Shirt 1',
    92 : '92 - Trolley Shirt 2',
    93 : '93 - Winter Shirt 1',
    94 : '94 - Halloween Costume Shirt 3',
    95 : '95 - Halloween Costume Shirt 4',
    96 : '96 - Valentines angel wings',
    97 : '97 - Scientist top 1',
    98 : '98 - Scientist top 2',
    99 : '99 - Scientist top 3',
    100 : '100 - Silly Mailbox Shirt',
    101 : '101 - Silly Trashcan Shirt',
    102 : '102 - Loony Labs Shirt',
    103 : '103 - Silly Hydrant Shirt',
    104 : '104 - Sillymeter Whistle Shirt',
    105 : '105 - Silly Cog-Crusher Shirt',
    106 : '106 - Most Cogs Defeated Shirt',
    107 : '107 - Victory Party Shirt 1',
    108 : '108 - Victory Party Shirt 2',
    }

# Note: While adding names to the ToonTopsDict make sure there is a space after the number.
# For eg: 'xx - ' and not 'xx-'. The code will crash if there is no space.

BoyBottomsDict = {
    0 : '00 - plain w/ pockets',
    1 : '01 - belt',
    2 : '02 - cargo',
    3 : '03 - hawaiian',
    4 : '04 - side stripes',
    5 : '05 - soccer shorts ',
    6 : '06 - flames side stripes',
    7 : '07 - denim',
    8 : "08 - Valentine's Day",
    9 : '09 - Orange/blue stripes',
    10 : '10 - Blue/gold stripes',
    11 : '11 - Leprechaun Shorts',
    12 : "12 - Cowboy Shorts 1",
    13 : "13 - Cowboy Shorts 2",
    14 : "14 - July 4th Shorts",
    15 : "15 - Green stripes",

    # Pyjama shorts
    16 : "16 - Blue Banana Pajama pants",
    17 : "17 - Red Horn Pajama pants",
    18 : "18 - Purple Glasses Pajama pants",

    # Winter Holiday Shorts
    19 : "19 - Winter Holiday Shorts Style 1",
    20 : "20 - Winter Holiday Shorts Style 2",
    21 : "21 - Winter Holiday Shorts Style 3",
    22 : "22 - Winter Holiday Shorts Style 4",

    # 2009 Valentines Day Shorts
    23 : "23 - Valentines Shorts 1",
    24 : "24 - Valentines Shorts 2",
    
    # Special award clothing
    25 : "25 - Fishing",
    26 : "26 - Gardening",
    27 : "27 - Party",
    28 : "28 - Racing",
    29 : "29 - Summer",
    30 : '30 - Golf Shorts 1',
    31 : '31 - Halloween Costume Shorts 1',
    32 : '32 - Halloween Costume Shorts 2',
    33 : '33 - Save Building Shorts 1',
    34 : '34 - Trolley Shorts 1',
    35 : '35 - Halloween Costume Shorts 3',
    36 : '36 - Halloween Costume Shorts 4',
    37 : '37 - Scientist bottom 1',
    38 : '38 - Scientist bottom 2',
    39 : '39 - Scientist bottom 3',
    40 : '40 - Cog-Crusher Shorts',
    }

GirlBottomsDict = {
    0 : '00 - solid',
    1 : '01 - polka dots',
    2 : '02 - vertical stripes',
    3 : '03 - horizontal stripe',
    4 : '04 - flower print',
    5 : '05 - plain w/ pockets',
    6 : '06 - flower',
    7 : '07 - 2 pockets',
    8 : '08 - denim1',
    9 : '09 - denim2',
    10 : '10 - blue with tan',
    11 : '11 - purple with pink',
    12 : '12 - teal with yellow',
    13 : "13 - Valentine's Day",
    14 : '14 - Rainbow skirt',
    15 : '15 - Leprechaun shorts',
    16 : '16 - Cowboy Skirt 1',
    17 : '17 - Cowboy Skirt 2',
    18 : '18 - July 4th Skirt',
    19 : '19 - Blue with flower',

    # Pyjama shorts
    20 : '20 - Blue Banana Pajama pants',
    21 : '21 -  Red Horn Pajama pants',
    22 : '22 - Purple Glasses Pajama pants',

    # Winter Holiday Skirts
    23 : '23 - Winter Holiday Skirt Style 1',
    24 : '24 - Winter Holiday Skirt Style 2',
    25 : '25 - Winter Holiday Skirt Style 3',
    26 : '26 - Winter Holiday Skirt Style 4',

    # 2009 Valentines Day Skirts
    27 : '27 - Valentines Skirt 1',
    28 : '28 - Valentines Skirt 2',
    
    # Special award clothing
    29 : "29 - Fishing",
    30 : "30 - Gardening",
    31 : "31 - Party",
    32 : "32 - Racing",
    33 : "33 - Summer",
    34 : '34 - Golf Skirt 1',
    35 : '35 - Halloween Costume Skirt 1',
    36 : '36 - Halloween Costume Skirt 2',
    37 : '37 - Save Building Skirt 1',
    38 : '38 - Trolley Skirt 1',
    39 : '39 - Halloween Costume Skirt 3',
    40 : '40 - Halloween Costume Skirt 4',
    41 : '41 - Scientist bottom 1',
    42 : '42 - Scientist bottom 2',
    43 : '43 - Scientist bottom 3',
    44 : '44 - Cog-Crusher Shorts',
    }

ChatCategories = {
    1: 'Basic',
    100 : 'HELLO',
    200 : "GOODBYE",
    300 : "HAPPY",
    400 : "SAD",
    500 : "FRIENDLY",
    600 : "You...",
    700 : "I like...",
    800 : "SORRY",
    900 : "STINKY",
    1000 : "PLACES",
    1100 : "Let's go...",
    1200 : "TOONTASKS",
    1300 : "I think...",
    1400 : "BATTLE",
    1500 : "BATTLE Submenu",
    1600 : "GAG SHOP",
    1700 : "FACTORY",
    1800 : "Sellbot Factory 1",
    1900 : "Sellbot Factory 2",
    2000 : "Option Page Colors",
    10000 : "Promotional",
    20000 : "Cog Phrases",
    20100 : "Cog Phrases",
    20200 : "Cog Phrases",
    20300 : "Cog Phrases",
    21000 : "DOODLES",
    21200 : "DOODLES Tricks",
    50000 : "PIRATES",
    50100 : "PIRATES Common",
    50200 : "PIRATES Insults",
    50300 : "PIRATES Places",
    60100 : "GATEWAY Greetings",
    60200 : "GATEWAY Bye",
    60300 : "GATEWAY Happy",
    60400 : "GATEWAY Sad",
    60500 : "GATEWAY Places",    
    }

chatDict = OTPLocalizer.SpeedChatStaticText
chatKeys = chatDict.keys()
chatKeys.sort()

customChatDict = OTPLocalizer.CustomSCStrings
customChatKeys = customChatDict.keys()
customChatKeys.sort()

faceoffTaunts = OTPLocalizer.SuitFaceoffTaunts
faceoffTauntsKeys = faceoffTaunts.keys()
faceoffTauntsKeys.sort()

attackTaunts = TTLocalizer.SuitAttackTaunts
attackTauntsKeys = attackTaunts.keys()
attackTauntsKeys.sort()

namegen = NameGenerator.NameGenerator()

ToonAnimList = [
    "angry",
    "applause",
    "bank",
    "book",
    "bored",
    "bow",
    "cast",
    "catch-eatneutral",
    "catch-eatnrun",
    "catch-intro-throw",
    "catch-neutral",
    "catch-run",
    "confused",
    "conked",
    "cringe",
    "curtsy",
    "down",
    "firehose",
    "fish",
    "fish-end",
    "fish-neutral",
    "happy-dance",
    "hold-bottle",
    "hold-magnet",
    "hypnotize",
    "juggle",
    "jump",
    "jump-idle",
    "jump-land",
    "jump-squat",
    "left",
    "lose",
    "melt",
    "neutral",
    "phoneBack",
    "phoneNeutral",
    "pole",
    "pole-neutral",
    "pushbutton",
    "reel",
    "reel-H",
    "reel-neutral",
    "right",
    "run",
    "running-jump",
    "running-jump-idle",
    "running-jump-land",
    "running-jump-squat",
    "sad-neutral",
    "sad-walk",
    "shrug",
    "sidestep-left",
    "sit",
    "sit-start",
    "slip-backward",
    "slip-forward",
    "smooch",
    "sound",
    "spit",
    "sprinkle-dust",
    "struggle",
    "swim",
    "takePhone",
    "teleport",
    "think",
    "throw",
    "tickle",
    "toss",
    "tug-o-war",
    "up",
    "victory",
    "walk",
    "water-gun",
    "wave",
    ]

SuitAnimList = [
    Suit.AllSuits,
    Suit.AllSuitsMinigame,
    Suit.AllSuitsTutorialBattle,
    Suit.AllSuitsBattle
    ]

SuitAnimCategories = [
    'All',
    'Minigame',
    'Tutorial',
    'Battle'
    ]

SuitTrackList = [
    'Corporate',
    'Legal',
    'Financial',
    'Sales'
    ]

SuitDNAList = [
    'f : flunky',
    'p : pencil pusher',
    'ym : yes man',
    'mm : micromanager',
    'ds : downsizer',
    'hh : head hunter',
    'cr : corporate raider',
    'tbc : the big cheese',

    'bf : bottom feeder',
    'b : blood sucker',
    'dt : double talker',
    'ac : ambulance chaser',
    'bs : back stabber',
    'sd : spin doctor',
    'le : legal eagle',
    'bw : bigwig',

    'sc : short changer',
    'pp : penny pincher',
    'tw : tightwad',
    'bc : bean counter',
    'nc : number cruncher',
    'mb : money bags',
    'ls : load shark',
    'rb : robber baron',

    'cc : cold caller',
    'tm : telemarketer',
    'nd : name dropper',
    'gh : glad hander',
    'ms : mover & shaker',
    'tf : two-face',
    'm : the mingler',
    'mh : Mr. Hollywood',
    ]

DoodleAnimList = [
    'toBeg',
    'beg',
    'fromBeg',
    'backflip',
    'dance',
    'toDig',
    'dig',
    'fromDig',
    'disappear',
    'eat',
    'jump',
    'neutral',
    'neutralHappy',
    'neutralSad',
    'toPet',
    'pet',
    'fromPet',
    'playDead',
    'fromPlayDead',
    'reappear',
    'run',
    'rollover',
    'walkSad',
    'speak',
    'swallow',
    'swim',
    'toBall',
    'walk',
    'walkHappy',
    ]    
        
rtmHelp = "\n- Once the program has loaded hit the ADD RANDOM TOON Button. \
\n- MIDDLE CLICK near the toon to place a COA(center of action) marker. \
\n- Hold the ALT KEY DOWN and use your three mouse buttons to NAVIGATE. \
\n	-LEFT click for ROTATE \
\n	-RIGHT click for ZOOM \
\n	-MIDDLE click to PAN \
\n- Use the ANIMATION PANEL that pops up when you add a toon to manipulate the animations. \
\n- For quickly changing through animations simply RIGHT CLICK anywhere on the screen. \
\n- If the Animation panel is closed you can hit the ANIMS button(in the bottom row) to open it again. \
\n- If you have multiple characters on screen, first select the character with the mouse and then open thier Aimation Panel \
\n- Use the RADIO BUTTONS to change TOON DNA." 

# NEIGHBORHOOD DATA
# If you run this from the command line you can pass in the hood codes
# you want to load. For example:
#    ppython LevelEditor.py DD TT BR
#
if sys.argv[1:]:
    try:
        opts, pargs = getopt.getopt(sys.argv[1:], '')
        hoods = pargs
    except Exception, e:
        print e
# If you do not run from the command line, we just load all of them
# or you can hack this up for your own purposes.
else:
    hoodString = base.config.GetString('level-editor-hoods',
                                       'TT DD BR DG DL MM PA')
    hoods = string.split(hoodString)

# The list of neighborhoods to edit
hoodIds = {'TT' : 'toontown_central',
           'DD' : 'donalds_dock',
           'MM' : 'minnies_melody_land',
           'BR' : 'the_burrrgh',
           'DG' : 'daisys_garden',
           'DL' : 'donalds_dreamland',
           'PA' : 'party_zone',
           }

# Init neighborhood arrays
NEIGHBORHOODS = []
NEIGHBORHOOD_CODES = {}
for hoodId in hoods:
    if hoodIds.has_key(hoodId):
        hoodName = hoodIds[hoodId]
        NEIGHBORHOOD_CODES[hoodName] = hoodId
        NEIGHBORHOODS.append(hoodName)
    else:
        print 'Error: no hood defined for: ', hoodId

# Load DNA
dnaDirectory = Filename.expandFrom(base.config.GetString("dna-directory", "$TTMODELS/src/dna"))

try:
    if dnaLoaded:
        pass
except NameError:
    print "Loading LevelEditor for hoods: ", hoods
    # DNAStorage instance for storing level DNA info
    # We need to use the __builtin__.foo syntax, not the
    # __builtins__["foo"] syntax, since this file runs at the top
    # level.
    __builtin__.DNASTORE = DNASTORE = DNAStorage()
    # Load the generic storage files
    loadDNAFile(DNASTORE, 'phase_4/dna/storage.dna', CSDefault, 1)
    loadDNAFile(DNASTORE, 'phase_5/dna/storage_town.dna', CSDefault, 1)
    loadDNAFile(DNASTORE, 'phase_5.5/dna/storage_estate.dna', CSDefault, 1)
    loadDNAFile(DNASTORE, 'phase_5.5/dna/storage_house_interior.dna', CSDefault, 1)
    # Load all the neighborhood specific storage files
    if 'TT' in hoods:
        loadDNAFile(DNASTORE, 'phase_4/dna/storage_TT.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_4/dna/storage_TT_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_5/dna/storage_TT_town.dna', CSDefault, 1)
    if 'DD' in hoods:
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_DD.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_DD_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_DD_town.dna', CSDefault, 1)
    if 'MM' in hoods:
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_MM.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_MM_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_6/dna/storage_MM_town.dna', CSDefault, 1)
    if 'BR' in hoods:
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_BR.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_BR_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_BR_town.dna', CSDefault, 1)
    if 'DG' in hoods:
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DG.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DG_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DG_town.dna', CSDefault, 1)
    if 'DL' in hoods:
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DL.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DL_sz.dna', CSDefault, 1)
        loadDNAFile(DNASTORE, 'phase_8/dna/storage_DL_town.dna', CSDefault, 1)
    if 'PA' in hoods:
        loadDNAFile(DNASTORE, 'phase_13/dna/storage_party_sz.dna', CSDefault, 1)        
    __builtin__.dnaLoaded = 1

class RobotToonManager(DirectObject):
    def __init__(self, toonParent = None):
        if toonParent is None:
            toonParent = render.attachNewNode('toonTop')
        self.toonParent = toonParent
        self.avatarDict = {}
        self.avatarType = 't'
        self.toonIds = NPCToons.NPCToonDict.keys()
        self.namePlusIds = map(
            lambda id: (TTLocalizer.NPCToonNames.get(id, 'Mystery NPC'), id),
            self.toonIds)
        self.namePlusIds.sort()
        self.numToons = len(self.toonIds)
        self.suitTrack = 'Corporate'
        self.suitLevel = 0
        self.doodleHead = None
        self.doodleEars = None
        self.doodleNose = None
        self.doodleTail = None
        self.doodleBody = None
        self.doodleGender = None
        self.doodleColor = -1
        self.doodleColorScale = -1
        self.doodleEyeColor = -1
        self.selectedToon = None
        self.s1 = loader.loadModel('models/misc/smiley')
        self.s1.reparentTo(render)
        self.s1.hide()
        self.s2 = loader.loadModel('models/misc/smiley')
        self.s2.reparentTo(render)
        self.s2.hide()
        self.fDirectMode = 0
        self.iRay = SelectionRay(base.cam)
        # See if a magin manager exists, if so, use it
        try:
            self.marginManager = base.marginManager
        except AttributeError:
            self.initNametagGlobals()
        self.skyFiles = ["phase_3.5/models/props/TT_sky",
                         "phase_3.5/models/props/BR_sky",
                         "phase_6/models/props/MM_sky",
                         "phase_8/models/props/DL_sky",
                         "phase_9/models/cogHQ/cog_sky",                       
                         ]
        self.skies = []
        for f in self.skyFiles:
            sky = loader.loadModel(f)
            sky.setScale(1.0)
            sky.setFogOff()
            sky.setZ(-10)
            self.skies.append(sky)
        # Just to make compatible with cloud sky
        self.skies[4].attachNewNode('Sky')
        self.skyIndex = -1
        self.sky = self.skies[0]
        self.fGrid = 1
        self.fRender2d = 1
        # Drop a toon
        self.accept('f10', self.makeRandomToon)
        self.accept('f11', self.toggleRender2d)
        self.accept('DIRECT_selectedNodePath', self.findSelectedToon)        
        self.accept('DIRECT-mouse3', self.nextAnim)
        self.accept('f9', base.screenshot)
        if base.__class__ != ShowBase.ShowBase:
            # If not a plain showbase object, add these key bindings
            self.accept('f12', self.toggleDirectMode)
##        self.pieMenu = TextPieMenu(['start pos', 'end pos',
##                                    'walk', 'sad-walk', 'run',
##                                    'victory', 'neutral'],
##                                   radius = 0.35,
##                                   action = self.pieMenuCommand)                                   
                                                                      
        self.animDisplay = TextNode('Animation Name')
        self.animDisplay.setText('Animation: None')            
        self.animDisplay.setTextColor(0.5, 0.5, 1.0, 1.0)            
        self.animDisplay.setShadow(0.1, 0.1)
        self.animDisplayNP = aspect2d.attachNewNode(self.animDisplay)        
        self.animDisplayNP.setScale(0.05)  
        self.animDisplayNP.setPos(-1.0,0.0,0.85)  
        
        # [gjeon] to find out currently moving camera in maya mode
        self.mouseMayaCamera = True       
        base.direct.cameraControl.useMayaCamControls = True        
        base.direct.cameraControl.lockRoll = True
        self.styleManager = LevelStyleManager(NEIGHBORHOODS, NEIGHBORHOOD_CODES)

        self.setLastAngle(0.0)

        base.enableParticles()        
                
        self.animPanel = None

    def createToplevel(self, dnaNode, nodePath = None):
        # When you create a new level, data is added to this node
        # When you load a DNA file, you replace this node with the new data
        self.DNAToplevel = dnaNode
        self.DNAData.add(self.DNAToplevel)
        if nodePath:
            # Node path given, use it
            self.NPToplevel = nodePath
            self.NPToplevel.reparentTo(self)
        else:
            # No node path given, traverse
            self.NPToplevel = self.DNAToplevel.traverse(self, DNASTORE, 1)
        # Update parent pointers
        self.DNAParent = self.DNAToplevel
        self.NPParent = self.NPToplevel
        self.VGParent = None
        # Add toplevel node path for suit points
        self.suitPointToplevel = self.NPToplevel.attachNewNode('suitPoints')

    def addProp(self, propType):
        print "addProp %s " % propType
        # Record new prop type
        self.setCurrent('prop_texture', propType)
        # And create new prop
        newDNAProp = DNAProp(propType + '_DNARoot')
        newDNAProp.setCode(propType)
        newDNAProp.setPos(VBase3(0))
        newDNAProp.setHpr(VBase3(0))
        # Now place new prop in the world
        self.initNodePath(newDNAProp)
        
    def toggleReaderPollTask(self):
        self.fReaderPollTask = 1 - self.fReaderPollTask
        if self.fReaderPollTask:
            base.cr.startReaderPollTask()
            direct.selectedNPReadout.setText('POLL START')
            direct.selectedNPReadout.reparentTo(aspect2d)
        else:
            base.cr.stopReaderPollTask()
            direct.selectedNPReadout.setText('POLL STOP')
            direct.selectedNPReadout.reparentTo(aspect2d)
    def printCameraPosition(self):
        base.localAvatar.printCameraPosition(base.localAvatar.cameraIndex)
    def showHiRes(self, switchIn = 10000):
        for t in self.avatarDict.values():
            t.showHiRes(switchIn = switchIn)
    def findToonTop(self):
        if last:
            np = last.findNetTag('robotAvatar')
            if not np.isEmpty():
                np.select()
    def makeRandomToon(self, toNpcId = None):
        # Check for intersection
        entry = self.iRay.pickGeom(
            skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA)
        if not entry:
            # Try again just at the center of the screen
            entry = self.iRay.pickGeom(
                skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA,
                xy = (0, -0.2))
        # If we got a valid intersection point
        if entry:
            self.s1.setPos(camera, entry.getSurfacePoint(entry.getFromNodePath()))
        else:
            self.s1.setPos(camera, 0, 15, -2)
        startPos = Point3(self.s1.getPos())
        endPos = Point3(startPos + Vec3(0,10,0))
        if self.avatarType == 't':
            if toNpcId == None:
                toNpcId = self.toonIds[randint(0,self.numToons)]
            a = RobotToon(description = toNpcId, parent = self.toonParent,
                          startPos = startPos, endPos = endPos)                          
        elif self.avatarType == 's':
            if self.suitTrack == 'Corporate':
                track = 'c'
            elif self.suitTrack == 'Legal':
                track = 'l'
            elif self.suitTrack == 'Financial':
                track = 'm'
            elif self.suitTrack == 'Sales':
                track = 's'
            else:
                track = ['c','l','m','s'][randint(0,3)]
            if self.suitLevel < 0:
                level = randint(1,8)
            else:
                level = self.suitLevel + 1
            a = RobotSuit(description = [level,track],
                          parent = self.toonParent, 
                          startPos = startPos, endPos = endPos)
        else:
            desc = PetDNA.getRandomPetDNA()
            if self.doodleHead != None:
                desc[0] = self.doodleHead
            if self.doodleEars != None:
                desc[1] = self.doodleEars
            if self.doodleNose != None:
                desc[2] = self.doodleNose
            if self.doodleTail != None:
                desc[3] = self.doodleTail
            if self.doodleBody != None:
                desc[4] = self.doodleBody
            # not sure why, but None didn't work as a cardinal value in these cases
            if self.doodleColor != -1:
                desc[5] = self.doodleColor
            if self.doodleColorScale != -1:
                desc[6] = self.doodleColorScale
            if self.doodleEyeColor != -1:
                desc[7] = self.doodleEyeColor
            if self.doodleGender != None:
                desc[8] = self.doodleGender
            a = RobotDoodle(description = desc,
                          parent = self.toonParent, 
                          startPos = startPos, endPos = endPos)
            
        a.nametag.manage(self.marginManager)
        self.avatarDict[a.id()] = a
        a.select() 
        if self.avatarType == 't':        
            self.setToonAnimState('neutral')
        self.faceCamera()
        a.setStartHpr(a.getHpr())
        messenger.send('SGE_Update Explorer', [a])
            
    def makeToonFromProperties(self, properties,
                               pos, hpr,
                               startPos, startHpr,
                               endPos, endHpr, state):
        t = RobotToon(description = properties, parent = self.toonParent,
                      startPos = startPos, startHpr = startHpr,
                      endPos = endPos, endHpr = endHpr)
        t.nametag.manage(self.marginManager)
        t.setPosHpr(pos, hpr)
        self.avatarDict[t.id()] = t
        t.select()
        self.setToonAnimState(state)
        messenger.send('SGE_Update Explorer', [t])
        return t
    def makeToonFromServerString(self, serverString,
                                 pos = Point3(0), hpr = Point3(0),
                                 startPos = Point3(0), startHpr = Point3(0),
                                 endPos = Point3(0,1,0), endHpr = Point3(0),
                                 state = 'neutral'):
        dna = ToonDNA.ToonDNA()
        netString = self.convertServerDNAString(serverString)
        dna.makeFromNetString(netString)
        return self.makeToonFromProperties(
            dna.asTuple(),pos,hpr,startPos,startHpr,endPos,endHpr,state)
    def convertServerDNAString(self, serverString):
        # Strip out blank space and take last 30 characters
        serverString = serverString.replace(' ', '')
        serverString = serverString[-30:]
        # Create a datagram from server string
        dg = PyDatagram()
        for i in range(0,len(serverString),2):
            eval('dg.addUint8(0x%s)' % serverString[i:i+2])
        return dg.getMessage()
    def _setStartPos(self):
        self.setStartPos((self.pieMenu.originX, self.pieMenu.originY))
    def _setEndPos(self):
        self.setEndPos((self.pieMenu.originX, self.pieMenu.originY))
    def setStartPos(self, xy = None):
        # Check for intersection
        entry = self.iRay.pickGeom(
            xy = xy, skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA)
        # If we got a valid intersection point
        if entry and (self.selectedToon != None):
            st = self.selectedToon
            st.setPos(camera, entry.getSurfacePoint(entry.getFromNodePath()))
            st.setStartPos(st.getPos())
            st.setStartHpr(st.getHpr())
            st.updateWalkIval()
    def setEndPos(self, xy = None):
        # Check for intersection
        entry = self.iRay.pickGeom(
            xy = xy, skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA)
        # If we got a valid intersection point
        if entry and (self.selectedToon != None):
            st = self.selectedToon
            st.setPos(camera, entry.getSurfacePoint(entry.getFromNodePath()))
            st.setEndPos(st.getPos())
            st.setEndHpr(st.getHpr())
            st.updateWalkIval()
    def findSelectedToon(self, nodePath):
        id = nodePath.id()
        np = nodePath.findNetTag('robotAvatar')
        if not np.isEmpty():
            if np.id() != nodePath.id():
                np.select()
            self.selectedToon = self.avatarDict.get(np.id())
            if self.panel:
                self.panel.updateToonInfo()
    def makeSuitFromProperties(self, properties,
                               pos, hpr,
                               startPos, startHpr,
                               endPos, endHpr, state):
        t = RobotSuit(description = properties[2], parent = self.toonParent,
                      startPos = startPos, startHpr = startHpr,
                      endPos = endPos, endHpr = endHpr, state = state)
        t.nametag.manage(self.marginManager)
        t.setPosHpr(pos, hpr)
        self.avatarDict[t.id()] = t
        messenger.send('SGE_Update Explorer', [t])
        return t
    def openCrowdFilePanel(self):
        tcfFilename = askopenfilename(
            defaultextension = '.tcf', initialdir = '.',
            filetypes = (('Toon Crowd', '*.tcf'),('All files', '*')),
            title = 'Open Toon Crowd File')
        if tcfFilename:
            self.openCrowdFile(tcfFilename)
    def openCrowdFile(self, tcfFilename):
            filename = Filename(tcfFilename)
            f = open(filename.toOsSpecific(), 'rb')
            rawData = f.readlines()            
            for line in rawData:
                (type,props,pos,hpr,startPos,startHpr,
                 endPos,endHpr,state) = self.parseAvatarProperties(line)
                if type == 't':
                    self.makeToonFromProperties(
                        props,pos,hpr,startPos,startHpr,endPos,endHpr,state)
                else:
                    self.makeSuitFromProperties(
                        props,pos,hpr,startPos,startHpr,endPos,endHpr,state)
            f.close()
    def parseAvatarProperties(self, line):
        line = string.strip(line)
        if line:
            line = line.split('*')
        i = 0
        type = line[i];i+=1
        if type == 't':
            head = line[i];i+=1
            torso = line[i];i+=1
            legs = line[i];i+=1
            gender = line[i];i+=1
            armColor = string.atoi(line[i]);i+=1
            gloveColor = string.atoi(line[i]);i+=1
            legColor = string.atoi(line[i]);i+=1
            headColor = string.atoi(line[i]);i+=1
            topTexture = string.atoi(line[i]);i+=1
            topTextureColor = string.atoi(line[i]);i+=1
            sleeveTexture = string.atoi(line[i]);i+=1
            sleeveTextureColor = string.atoi(line[i]);i+=1
            bottomTexture = string.atoi(line[i]);i+=1
            bottomTextureColor = string.atoi(line[i]);i+=1
            props = [head, torso, legs, gender,
                    armColor, gloveColor, legColor, headColor,
                    topTexture, topTextureColor, sleeveTexture,
                    sleeveTextureColor, bottomTexture,
                    bottomTextureColor]
        else:
            body = line[i];i+=1
            dept = line[i];i+=1
            name = line[i];i+=1
            props = [body, dept, name]
        x = string.atof(line[i]);i+=1
        y = string.atof(line[i]);i+=1
        z = string.atof(line[i]);i+=1
        h = string.atof(line[i]);i+=1
        p = string.atof(line[i]);i+=1
        r = string.atof(line[i]);i+=1
        x1 = string.atof(line[i]);i+=1
        y1 = string.atof(line[i]);i+=1
        z1 = string.atof(line[i]);i+=1
        h1 = string.atof(line[i]);i+=1
        p1 = string.atof(line[i]);i+=1
        r1 = string.atof(line[i]);i+=1
        x2 = string.atof(line[i]);i+=1
        y2 = string.atof(line[i]);i+=1
        z2 = string.atof(line[i]);i+=1
        h2 = string.atof(line[i]);i+=1
        p2 = string.atof(line[i]);i+=1
        r2 = string.atof(line[i]);i+=1
        state = line[i]
        return (type, props,
                Point3(x,y,z),
                Point3(h,p,r),
                Point3(x1,y1,z1),
                Point3(h1,p1,r1),
                Point3(x2,y2,z2),
                Point3(h2,p2,r2),
                state)
    def saveCrowdFile(self):
        tcfFilename = asksaveasfilename(
            defaultextension = '.tcf', initialdir = '.',
            filetypes = (('Toon Crowd', '*.tcf'),('All files', '*')),
            title = 'Save Toon Crowd File')            
        if tcfFilename:
            filename = Filename(tcfFilename)
            f = open(filename.toOsSpecific(), 'wb')
            for t in self.avatarDict.values():
                type = t.style.type
                if type == 't':
                    style = t.style.asTuple()
                    styleStr = ("%s*%s*%s*%s*%d*%d*%d*%d*%d*%d*%d*%d*%d*%d" %
                                (style[0], style[1], style[2], style[3],
                                 style[4], style[5], style[6], style[7],
                                 style[8], style[9], style[10], style[11],
                                 style[12], style[13]))
                else:
                    style = t.style
                    styleStr = ("%s*%s*%s" %
                                (style.body, style.dept, style.name))
                pos = t.getPos()
                hpr = t.getHpr()
                pose = ("%0.2f*%0.2f*%0.2f*%0.2f*%0.2f*%0.2f" %
                        (pos[0],pos[1],pos[2],hpr[0],hpr[1],hpr[2]))
                startPose = ("%0.2f*%0.2f*%0.2f*%0.2f*%0.2f*%0.2f" %
                             (t.startPos[0],t.startPos[1],t.startPos[2],
                              t.startHpr[0],t.startHpr[1],t.startHpr[2]))
                endPose = ("%0.2f*%0.2f*%0.2f*%0.2f*%0.2f*%0.2f" %
                           (t.endPos[0],t.endPos[1],t.endPos[2],
                            t.endHpr[0],t.endHpr[1],t.endHpr[2]))
                state = t.state
                f.write("%s*%s*%s*%s*%s*%s\n" %
                        (type,styleStr,pose,startPose,endPose,state))
            f.close()
    def pieMenuCommand(self, cmd):
        if base.config.GetBool('want-new-anims', 1):
            return
        if self.selectedToon:
            if cmd == 'start pos':
                self._setStartPos()
            elif cmd == 'end pos':
                self._setEndPos()
            else:
                self.selectedToon.setAnimState(cmd)
    def toggleRender2d(self):
        self.fRender2d = 1 - self.fRender2d
        if self.fRender2d:
            render2d.show()
        else:
            render2d.hide()

    def clearToons(self):
        for t in self.avatarDict.values():
            t.nametag.unmanage(self.marginManager)
            t.destroy()
        self.avatarDict = {}
        self.selectedToon = None

    def toggleDirectMode(self):
        self.fDirectMode = 1 - self.fDirectMode
        if self.fDirectMode:
            print 'SWITCH TO DIRECT MODE'
            # Start up direct
            taskMgr.removeTasksMatching('updateSmartCamera*')
            camera.wrtReparentTo(render)
            base.startTk()
            base.startDirect()
            direct.selectedNPReadout.setText('DIRECT MODE')
            direct.selectedNPReadout.reparentTo(aspect2d)
        else:
            print 'SWITCH TO TOONTOWN MODE'
            # Return to toontown mode
            if direct:
                direct.deselectAll()
                direct.disable()
                camera.wrtReparentTo(base.localAvatar)
                base.localAvatar.startUpdateSmartCamera()

    def initNametagGlobals(self):
        """initNametagGlobals(self)

        Should be called once during startup to initialize a few
        defaults for the Nametags.
        """
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModelNode(
            'phase_3/models/props/chatbox'))
        thought3d = ChatBalloon(loader.loadModelNode(
            'phase_3/models/props/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModelNode(
            'phase_3/models/props/chatbox_noarrow'))
        chatButtonGui = loader.loadModel(
            "phase_3/models/gui/chat_button_gui")
        NametagGlobals.setCamera(base.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        NametagGlobals.setMouseWatcher(base.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(
            PGButton.SReady, chatButtonGui.find("**/Horiz_Arrow_UP"))
        NametagGlobals.setPageButton(
            PGButton.SDepressed, chatButtonGui.find("**/Horiz_Arrow_DN"))
        NametagGlobals.setPageButton(
            PGButton.SRollover, chatButtonGui.find("**/Horiz_Arrow_Rllvr"))
        NametagGlobals.setQuitButton(
            PGButton.SReady, chatButtonGui.find("**/CloseBtn_UP"))
        NametagGlobals.setQuitButton(
            PGButton.SDepressed, chatButtonGui.find("**/CloseBtn_DN"))
        NametagGlobals.setQuitButton(
            PGButton.SRollover, chatButtonGui.find("**/CloseBtn_Rllvr"))

        # We don't need these instances any more.
        arrow.removeNode()
        card.removeNode()
        chatButtonGui.removeNode()
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)

        # For now, we'll leave the Toon at the same point as the
        # camera.  When we have a real toon later, we'll change it.
        NametagGlobals.setToon(base.cam)

        # We need a node to be the parent of all of the 2-d onscreen
        # messages along the margins.  This should be in front of many
        # things, but not all things.
        self.marginManager = MarginManager()
        self.margins = \
          base.aspect2d.attachNewNode(
            self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)

        # And define a bunch of cells along the margins.
        mm = self.marginManager
        self.leftCells = [
            mm.addGridCell(0, 1, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 2, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 3, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop)
            ]
        self.bottomCells = [
            mm.addGridCell(0.5, 0, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(1.5, 0, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(2.5, 0, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(3.5, 0, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(4.5, 0, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop)
            ]
        self.rightCells = [
            mm.addGridCell(5, 2, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop),
            mm.addGridCell(5, 1, base.a2dLeft, base.a2dRight,
                           base.a2dBottom, base.a2dTop)
            ]

    def faceCamera(self):
        toon = self.selectedToon
        if toon is None:
            return
        toon.lookAt(camera)
        h = toon.getH(render)
        toon.setHpr(render,h,0,0)

    def toggleSky(self):
        self.stopSky()
        self.skyIndex += 1
        if self.skyIndex >= len(self.skies):
            self.skyIndex = -1
        else:
            self.sky = self.skies[self.skyIndex]
            self.startSky()

    def startSky(self):
        SkyUtil.startCloudSky(self)

    def skyTrack(self, task):
        # Every frame nail the sky to 0, with no rotation
        # Actually we can raise the sky to the lowest point
        # on the horizon since you will not be able to see
        # over or between buildings. Drawing part of the sky
        # that will always be behind buildings is wasteful.
        # DL has some 10 foot fences, so the highest we can
        # currently put the sky is at 10 feet.
        # Actually, the tag minigame uses the sky now, and wants
        # it at 0.0, so until we have real artwork there, just
        # keep it at 0
        # Rotate the sky slowly to simulate clouds passing
        task.h += (globalClock.getDt() * 0.25)
        if not task.cloud1.isEmpty():
            task.cloud1.setH(task.h)
        if not task.cloud2.isEmpty():
            task.cloud2.setH(-task.h * 0.8)
        return Task.cont

    def stopSky(self):
        # Remove the sky task just in case it was spawned.
        taskMgr.remove("skyTrack")
        self.sky.reparentTo(hidden)

    def toggleGrid(self):
        self.fGrid = 1 - self.fGrid
        if self.fGrid:
            direct.grid.enable()
        else:
            direct.grid.disable()

    def popupControls(self):
        self.panel = RobotToonControlPanel(self)

    def destroy(self):
        self.ignore('f9')
        self.ignore('f10')
        self.ignore('f11')
        self.ignore('f12')
        self.ignore('DIRECT_selectedNodePath')
        self.s1.removeNode()
        self.s2.removeNode()
        # self.pieMenu.destroy()
        self.clearToons()

    def getAttribute(self, attribute):
        """ Return specified attribute for current neighborhood """
        return self.styleManager.getAttribute(attribute)

    def setCurrent(self, attribute, newCurrent):
        """ Set neighborhood's current selection for specified attribute """
        self.getAttribute(attribute).setCurrent(newCurrent, fEvent = 0)

    def initNodePath(self, dnaNode, hotKey = None):
        """
        Update DNA to reflect latest style choices and then generate
        new node path and add it to the scene graph
        """
        # Determine dnaNode Class Type
        nodeClass = DNAGetClassType(dnaNode)
        # Did the user hit insert or space?
        if hotKey:
            # Yes, make a new copy of the dnaNode
            dnaNode = dnaNode.__class__(dnaNode)
            # And determine dnaNode type and perform any type specific updates
            if nodeClass.eq(DNA_PROP):
                dnaNode.setCode(self.getCurrent('prop_texture'))
            elif nodeClass.eq(DNA_STREET):
                dnaNode.setCode(self.getCurrent('street_texture'))
            elif nodeClass.eq(DNA_FLAT_BUILDING):
                # If insert, pick a new random style
                if hotKey == 'insert':
                    self.setRandomBuildingStyle(dnaNode, dnaNode.getName())
                    # Get a new building width
                    self.setCurrent('building_width',
                                    self.getRandomWallWidth())
                dnaNode.setWidth(self.getCurrent('building_width'))

        # Position it
        # Check for intersection
        entry = self.iRay.pickGeom(
            skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA)
        if not entry:
            # Try again just at the center of the screen
            entry = self.iRay.pickGeom(
                skipFlags = SKIP_HIDDEN | SKIP_BACKFACE | SKIP_CAMERA,
                xy = (0, -0.2))
        # If we got a valid intersection point
        if entry:
            self.s1.setPos(camera, entry.getSurfacePoint(entry.getFromNodePath()))
        else:
            self.s1.setPos(camera, 0, 15, -2)

        dnaNode.setPos(self.s1.getPos())
        # Initialize angle to match last object
        dnaNode.setHpr(Vec3(self.getLastAngle(), 0, 0))

        # And create the geometry
        newNodePath = dnaNode.traverse(self.toonParent, DNASTORE, 1)
        newNodePath.reparentTo(self.toonParent)

        base.direct.select(newNodePath)
        self.faceCamera()

        messenger.send('SGE_Update Explorer', [newNodePath])

    # Angle of last object added to level
    def setLastAngle(self, angle):
        self.lastAngle = angle

    def getLastAngle(self):
        return self.lastAngle       
                
    def setToonAnimState(self,anim):    
        self.selectedToon.setAnimState(anim)    
        self.animDisplay.setText("Animation: "+str(anim))   
        
        if not self.animPanel:        
            self.showAnimPanel()            
            
        self.animPanel.actorControlList[0].selectAnimNamed(anim)            
        self.animPanel.actorControlList[0].updateDisplay()            
        self.animPanel.actorControlList[0].animMenu.selectitem(anim)            
        self.animPanel.playActorControls()
        self.animPanel.loopVar.set(1)                       
        
    def showAnimPanel(self):
        # show animation panel for currently selected actors
        from direct.tkpanels import AnimPanel        
        if self.selectedToon:
            self.animPanel = AnimPanel.AnimPanel(
                self.selectedToon,session = self)                      
            self.animPanel.setDestroyCallBack(self.animPanelClosed)
                                
        if self.selectedToon and self.selectedToon.state:        
            self.setToonAnimState(self.selectedToon.state)            
                        
    def animPanelClosed(self):    
        self.animPanel = None        
                
    def getState(self):        
        if not self.animPanel:        
            self.showAnimPanel()
        if self.selectedToon:
            self.selectedToon.state = self.animPanel.actorControlList[0]['active'] 
            return self.selectedToon.state
                
    def nextAnim(self, modifiers = 0):
        if not self.animPanel:        
            self.showAnimPanel()
        if self.selectedToon and modifiers==0:        
            currState = self.getState()       
            try:
                i = self.animPanel.actorControlList[0]['animList'].index(currState)        
            except:      
                i = -1            
                    
            newIndex = i+1
            if (newIndex) < len(ToonAnimList):        
                self.setToonAnimState(self.animPanel.actorControlList[0]['animList'][newIndex])                
            else:            
                self.setToonAnimState(self.animPanel.actorControlList[0]['animList'][0])                
        

""" Robot Toon Manager Control Panel module """
class RobotToonControlPanel(AppShell):
    # Override class variables
    appname = 'Robot Toon Manager Panel'
    frameWidth  = 650
    frameHeight = 600
    usecommandarea = 1
    usestatusarea  = 0
    contactname = 'Mark Mine'
    contactphone = '(818) 623-3915'
    contactemail = "Mark.Mine@disney.com"

    def __init__(self, robotToonManager, **kw):
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (
            )
        self.defineoptions(kw, optiondefs)

        self.rtm = robotToonManager        

        AppShell.__init__(self)

    def appInit(self):
        # Initialize any instance variables you use here
        self.fDoIt = 0
        self.colorButtonList = []
        self.topsVariants = []
        self.bottomsVariants = []
        self.npToplevel = None
        self.maleTopsList = ToonDNA.getAllTops('m')
        self.maleTopsDict = self.sortVariants(self.maleTopsList)
        self.maleTopsKeys = self.maleTopsDict.keys()
        self.maleTopsKeys.sort()
        self.maleTopsNames = map(lambda x: ToonTopsDict[x], self.maleTopsKeys)
        self.maleBottomsList = ToonDNA.getAllBottoms('m')
        self.maleBottomsDict = self.sortVariants(self.maleBottomsList)
        self.maleBottomsKeys = self.maleBottomsDict.keys()
        self.maleBottomsKeys.sort()
        self.maleBottomsNames = map(
            lambda x: BoyBottomsDict[x], self.maleBottomsKeys)
        self.femaleTopsList = ToonDNA.getAllTops('f')
        self.femaleTopsDict = self.sortVariants(self.femaleTopsList)
        self.femaleTopsKeys = self.femaleTopsDict.keys()
        self.femaleTopsKeys.sort()
        self.femaleTopsNames = map(lambda x: ToonTopsDict[x],
                                   self.femaleTopsKeys)
        self.femaleBottomsList = ToonDNA.getAllBottoms('f')
        self.femaleBottomsDict = self.sortVariants(self.femaleBottomsList)
        self.femaleSkirtsList = ToonDNA.getAllBottoms('f','skirts')
        self.femaleSkirtsDict = self.sortVariants(self.femaleSkirtsList)
        self.femaleSkirtsKeys = self.femaleSkirtsDict.keys()
        self.femaleSkirtsKeys.sort()
        self.femaleSkirtsNames = map(
            lambda x: GirlBottomsDict[x], self.femaleSkirtsKeys)
        self.femaleShortsList = ToonDNA.getAllBottoms('f','shorts')
        self.femaleShortsDict = self.sortVariants(self.femaleShortsList)
        self.femaleShortsKeys = self.femaleShortsDict.keys()
        self.femaleShortsKeys.sort()
        self.femaleShortsNames = map(
            lambda x: GirlBottomsDict[x], self.femaleShortsKeys)
        self.doodleColorButtonList = []
        self.doodleColorScaleButtonList = []
        self.doodleEyeColorButtonList = []

        self.lastPath = None
        
    def sortVariants(self, styleList):
        styleDict = {}
        styleList.sort()
        for style in styleList:
            idx = style[0]
            variantList = styleDict.get(idx, [])
            variantList.append(style)
            styleDict[idx] = variantList
        return styleDict

    def createInterface(self):
        # Create the tk components
        interior = self.interior()
        menuBar = self.menuBar

        # Create a command entry
        menuBar.addmenu('Crowds', 'Crowd File Operations')
        menuBar.addmenuitem('Crowds', 'command',
                            'Open Crowd File',
                            label = 'Open...',
                            command = self.rtm.openCrowdFilePanel)

        menuBar.addmenuitem('Crowds', 'command',
                            'Save Crowd File',
                            label = 'Save...',
                            command = self.rtm.saveCrowdFile)

        menuBar.addmenuitem('Crowds', 'command',
                            'Clear Crowd',
                            label = 'Clear Crowd...',
                            command = self.rtm.clearToons)

        menuBar.addmenu('Scene', 'Scene File Operations')
        menuBar.addmenuitem('Scene', 'command',
                            'Open DNA Scene File',
                            label = 'Open...',
                            command = self.loadSpecifiedDNAFile)
        menuBar.addmenuitem('Scene', 'command',
                            'Clear Scene',
                            label = 'Clear Scene...',
                            command = self.resetScene)

        menuBar.addmenu('Tools', 'Tools')
        menuBar.addmenuitem('Tools', 'command',
                            'Resize Window',
                            label = 'Resize Window...',
                            command = self.resizeWindow)

        menuBar.addmenuitem('Tools', 'command',
                            'Toggle Anti-Aliasing',
                            label = 'Toggle Anti-Aliasing',
                            command = self.toggleAntiAliasing)

        menuBar.addmenuitem('Tools', 'command',
		            'Import Maya File',
			    label = 'Import Maya File',
			    command = self.importMaya)    
			        
        menuBar.addmenuitem('File', 'command',
                            'Show Anim Panel',
                            label = 'Show Anim Panel',
                            command = self.rtm.showAnimPanel)

        # Paned widget for dividing two halves
        mainFrame = Frame(interior)
        self.framePane = Pmw.PanedWidget(mainFrame, orient = DGG.HORIZONTAL)
        self.explorerFrame = self.framePane.add('left', min = 200)
        self.rightFrame = self.framePane.add('right', min = 300)
        self.notebookFrame = Frame(self.rightFrame)

        self.explorer = SceneGraphExplorer(parent = self.explorerFrame,
                                           nodePath = self.rtm.toonParent,
                                           scrolledCanvas_hull_width = 200,
                                           scrolledCanvas_hull_height = 50)
        self.explorer.pack(fill = BOTH, expand = 1)
        self.explorerFrame.pack(fill = BOTH, expand = 1)
        self.explorer._node.state = 'expanded'

        # Create the notebook pages
        self.notebook = Pmw.NoteBook(self.notebookFrame)
        self.pageOne = self.notebook.add('Toons')
        dnaFrame = Frame(self.pageOne)
        self.serverString = StringVar()
        self.serverStringEntry = Pmw.EntryField(
            parent = dnaFrame,
            labelpos = W,
            label_text = 'Server String',
            entry_width = 20,
            entry_justify = 'right',
            entry_textvar = self.serverString,
            command = self._setServerString)
        self.serverStringEntry.pack(side = LEFT, fill = X, expand = 1)

        self.npcButton = Menubutton(dnaFrame, width = 15,
                                    text = "NPC Toons",
                                    relief = RAISED,
                                    borderwidth = 2)
        self.npcMenu = Menu(self.npcButton, tearoff = 0)
        self.npcButton['menu'] = self.npcMenu
        self.npcButton.pack(side = LEFT, fill = X, expand = 1)
        firstLetter = None
        for name, id in self.rtm.namePlusIds:
            if TextEncoder.upper(name[0]) != firstLetter:
                firstLetter = TextEncoder.upper(name[0])
                subMenu = Menu(self.npcMenu, tearoff = 0)
                self.npcMenu.add_cascade(
                    label = 'NPC %s' % firstLetter, 
                    menu = subMenu)
            subMenu.add_command(
                label = TTLocalizer.NPCToonNames.get(id,'Unnamed NPC'),
                command = lambda id=id: self.rtm.makeRandomToon(id))
        
        dnaFrame.pack(fill = X, expand = 0)
        
        # LOD
        self.lod = StringVar()
        self.lod.set('1000')
        lodFrame = Frame(self.pageOne)
        Label(lodFrame,text='LOD:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            lodFrame, 'LOD', 'high',
            self.lod, '1000', self.selectLOD,
            help = 'high LOD',
            side = LEFT)
        self.newCreateRadiobutton(
            lodFrame, 'LOD', 'medium',
            self.lod, '500', self.selectLOD,
            help = 'medium LOD',
            side = LEFT)
        self.newCreateRadiobutton(
            lodFrame, 'LOD', 'low',
            self.lod, '250', self.selectLOD,
            help = 'low LOD',
            side = LEFT)
        lodFrame.pack(fill = X, expand = 0)        
        
        # GENDER
        self.gender = StringVar()
        self.gender.set('m')
        genderFrame = Frame(self.pageOne)
        Label(genderFrame,text='Gender:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            genderFrame, 'Gender', 'Male',
            self.gender, 'm', self.swapGender,
            help = 'Male Toon',
            side = LEFT)
        self.newCreateRadiobutton(
            genderFrame, 'Gender', 'Female',
            self.gender, 'f', self.swapGender,
            help = 'Female Toon',
            side = LEFT)
        genderFrame.pack(fill = X, expand = 0)

        # HEAD
        self.speciesDict = { 'c' : 'Cat', 'd' : 'Dog', 'f' : 'Duck',
                             'h' : 'Horse', 'm' : 'Mouse', 'r' : 'Rabbit',
                             'p' : 'Monkey', 'b' : 'Bear', 's' : 'Swine' }
        speciesList = self.speciesDict.values()
        speciesList.sort()
        self.headDict = {}
        for head in ToonDNA.toonHeadTypes:
            headList = self.headDict.get(self.speciesDict[head[0]], [])
            headList.append(head)
            self.headDict[self.speciesDict[head[0]]] = headList

        speciesFrame = Frame(self.pageOne)
        Label(speciesFrame, text = 'Species:',
              anchor = W, justify = LEFT,
              width=6).pack(side = LEFT, expand = 0)
        self.species = StringVar()
        self.species.set('Cat')
        for s in speciesList:
            self.newCreateRadiobutton(
                speciesFrame, 'Species', s,
                self.species, s, self.setSpecies,
                help = 'Set species to %s' % s,
                side = LEFT)
        speciesFrame.pack(expand = 0, fill = X)
        
        headFrame = Frame(self.pageOne)
        Label(headFrame, text = 'Head:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.head = StringVar()
        self.head.set('ls')
        self.ssHeadButton = self.newCreateRadiobutton(
            headFrame, 'Head', 'ss',
            self.head, 'ss', self.setHead,
            help = 'Set head to ss',
            side = LEFT)
        self.lsHeadButton = self.newCreateRadiobutton(
            headFrame, 'Head', 'ls',
            self.head, 'ls', self.setHead,
            help = 'Set head to ls',
            side = LEFT)
        self.slHeadButton = self.newCreateRadiobutton(
            headFrame, 'Head', 'sl',
            self.head, 'sl', self.setHead,
            help = 'Set head to sl',
            side = LEFT)
        self.llHeadButton = self.newCreateRadiobutton(
            headFrame, 'Head', 'll',
            self.head, 'll', self.setHead,
            help = 'Set head to ll',
            side = LEFT)
        headFrame.pack(expand = 0, fill = X)

        eyesFrame = Frame(self.pageOne)
        Label(eyesFrame, text = 'Eyes:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.eyes = StringVar()
        self.eyes.set('normal')
        self.normalEyesButton = self.newCreateRadiobutton(
            eyesFrame, 'Eyes', 'normal',
            self.eyes, 'normal', self.setEyes,
            help = 'Set eyes to normal blink',
            side = LEFT)
        self.angryEyesButton = self.newCreateRadiobutton(
            eyesFrame, 'Eyes', 'angry',
            self.eyes, 'angry', self.setEyes,
            help = 'Set eyes to angry blink',
            side = LEFT)
        self.sadEyesButton = self.newCreateRadiobutton(
            eyesFrame, 'Eyes', 'sad',
            self.eyes, 'sad', self.setEyes,
            help = 'Set eyes to sad blink',
            side = LEFT)
        eyesFrame.pack(expand = 0, fill = X)
        
        # Muzzles
        muzzleFrame = Frame(self.pageOne)
        Label(muzzleFrame, text = 'Muzzles: ', width=6, anchor = W, \
                            justify = LEFT).pack(side=LEFT, expand = 0)
        self.muzzle = StringVar()
        self.muzzle.set('normal')
        self.normalMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'normal', self.muzzle, 
            'normal', self.setMuzzle,
            help = 'Set muzzle to normal',
            side = LEFT)
            
        self.angryMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'angry',
            self.muzzle, 'angry', self.setMuzzle,
            help = 'Set muzzle to angry',
            side = LEFT)
            
        self.sadMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'sad',
            self.muzzle, 'sad', self.setMuzzle,
            help = 'Set muzzle to sad',
            side = LEFT)
            
        self.smileMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'smile',
            self.muzzle, 'smile', self.setMuzzle,
            help = 'Set muzzle to smile',
            side = LEFT)
            
        self.laughMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'laugh',
            self.muzzle, 'laugh', self.setMuzzle,
            help = 'Set muzzle to laugh',
            side = LEFT)
            
        self.surpriseMuzzleButton = self.newCreateRadiobutton(
            muzzleFrame, 'Muzzle', 'surprise',
            self.muzzle, 'surprise', self.setMuzzle,
            help = 'Set muzzle to surprise',
            side = LEFT)
        muzzleFrame.pack(expand = 0, fill = X)

        # TORSO
        self.torso = StringVar()
        self.torso.set('ss')
        torsoFrame = Frame(self.pageOne)
        Label(torsoFrame, text = 'Torso:',width=6,
              anchor = W, justify = LEFT).pack(side=LEFT,expand = 0)
        self.ssButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'SS',
            self.torso, 'ss', self.swapTorso,
            help = 'S-Shorts',
            side = LEFT)
        self.msButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'MS',
            self.torso, 'ms', self.swapTorso,
            help = 'M-Shorts',
            side = LEFT)
        self.lsButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'LS',
            self.torso, 'ls', self.swapTorso,
            help = 'L-Shorts',
            side = LEFT)
        self.sdButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'SD',
            self.torso, 'sd', self.swapTorso,
            help = 'S-Dress',
            side = LEFT)
        self.mdButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'MD',
            self.torso, 'md', self.swapTorso,
            help = 'M-Dress',
            side = LEFT)
        self.ldButton = self.newCreateRadiobutton(
            torsoFrame, 'Torso', 'LD',
            self.torso, 'ld', self.swapTorso,
            help = 'L-Dress',
            side = LEFT)
        torsoFrame.pack(fill = X, expand = 0)
        
        # LEGS
        self.legs = StringVar()
        self.legs.set('ss')
        legsFrame = Frame(self.pageOne)
        Label(legsFrame, text = 'Legs:',width=6,
              anchor = W, justify = LEFT).pack(side=LEFT,expand = 0)
        self.sLegsButton = self.newCreateRadiobutton(
            legsFrame, 'Legs', 's',
            self.legs, 's', self.swapLegs,
            help = 'Short Legs',
            side = LEFT)
        self.mLegsButton = self.newCreateRadiobutton(
            legsFrame, 'Legs', 'm',
            self.legs, 'm', self.swapLegs,
            help = 'Medium Legs',
            side = LEFT)
        self.lLegsButton = self.newCreateRadiobutton(
            legsFrame, 'Legs', 'l',
            self.legs, 'l', self.swapLegs,
            help = 'Long Legs',
            side = LEFT)
        legsFrame.pack(fill = X, expand = 0)

        # COLOR MODE
        self.colorMode = StringVar()
        self.colorMode.set('all')
        colorModeFrame = Frame(self.pageOne)
        Label(colorModeFrame, text = 'Color:', width = 6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            colorModeFrame, 'ColorMode', 'All',
            self.colorMode, 'all', None,
            help = 'Set all body colors',
            side = LEFT)
        self.newCreateRadiobutton(
            colorModeFrame, 'ColorMode', 'Arms',
            self.colorMode, 'arms', None,
            help = 'Set arm color',
            side = LEFT)
        self.newCreateRadiobutton(
            colorModeFrame, 'ColorMode', 'Gloves',
            self.colorMode, 'gloves', None,
            help = 'Set gloves color',
            side = LEFT)
        self.newCreateRadiobutton(
            colorModeFrame, 'ColorMode', 'Legs',
            self.colorMode, 'legs', None,
            help = 'Set legs color',
            side = LEFT)
        self.newCreateRadiobutton(
            colorModeFrame, 'ColorMode', 'Head',
            self.colorMode, 'head', None,
            help = 'Set head color',
            side = LEFT)
        colorModeFrame.pack(fill = X, expand = 0)

        # COLOR TABLETS
        colorFrame = Frame(self.pageOne)
        for i in range(2):
            cf = Frame(colorFrame)
            for j in range(14):
                index = i * 14 + j
                if index < 27:
                    color = self.transformRGB(ToonDNA.allColorsList[index])
                    b = Button(cf, width = 1, height = 1, background = color,
                           text = "%d" % index,
                           command = lambda ci=index: self.setToonColor(ci))
                    b.pack(side = LEFT, fill = X, expand = 0)
                    self.colorButtonList.append(b)
            cf.pack(fill = X, expand = 0)
        colorFrame.pack(fill = X, expand = 0)

        # TOP TEXTURE
        topsFrame = Frame(self.pageOne)
        # Create this first so it exists when creating the counter
        self.topsMenu = Pmw.OptionMenu(
            parent = topsFrame,
            labelpos = W,
            label_text = 'Tops:',
            label_width = 8, 
            label_anchor = W, label_justify = LEFT,
            menubutton_width = 25)
        self.topsMenu['command'] = lambda x: self.setTop(x,1)
        self.topsMenu.pack(side = LEFT, fill = X, expand = 0)

        self.topsIndex = IntVar()
        self.topsIndex.set(0)
        self.topsCounter = Pmw.Counter(
            parent = topsFrame,
            entry_textvariable = self.topsIndex,
            entryfield_value = self.topsIndex.get(),
            entryfield_validate = { 'validator' : self.__switchTops },
            entryfield_entry_width = 3)
        self.topsCounter['entryfield_command'] = self.setTopVariant
        self.topsCounter.pack(side = LEFT, fill = X, expand = 0)
        
        topsFrame.pack(fill = X, expand = 0)

        # BOTTOM TEXTURE
        bottomsFrame = Frame(self.pageOne)
        # Create this first so it exists when creating the counter
        self.bottomsMenu = Pmw.OptionMenu(
            parent = bottomsFrame,
            labelpos = W,
            label_text = 'Bottoms',
            label_width = 8,
            label_anchor = W, label_justify = LEFT,
            menubutton_width = 25)
        self.bottomsMenu['command'] = lambda x: self.setBottom(x,1)
        self.bottomsMenu.pack(side = LEFT, fill = X, expand = 0)

        self.bottomsIndex = IntVar()
        self.bottomsIndex.set(0)
        self.bottomsCounter = Pmw.Counter(
            parent = bottomsFrame,
            entry_textvariable = self.bottomsIndex,
            entryfield_value = self.bottomsIndex.get(),
            entryfield_validate = { 'validator' : self.__switchBottoms },
            entryfield_entry_width = 3)
        self.bottomsCounter['entryfield_command'] = self.setBottomVariant
        self.bottomsCounter.pack(side = LEFT, fill = X, expand = 0)
        
        bottomsFrame.pack(fill = X, expand = 0)

        nameFrame = Frame(self.pageOne)
        Label(nameFrame, text = "Name:", width = 8,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0,
                                               fill = X)
        self.toonName = StringVar()
        self.toonName.set('')
        self.nameEntry = Entry(nameFrame, width = 10,
                               textvariable = self.toonName)
        self.nameEntry.bind('<Return>', self.setToonName)
        self.nameEntry.pack(side = LEFT, expand = 1, fill = X)

        self.randomName = Button(nameFrame, text = 'Random Name',
                                 command = self.setRandomToonName)
        self.randomName.pack(side = LEFT, fill = X, expand = 0)

        self.clearName = Button(nameFrame, text = 'Clear Name',
                                 command = self.clearToonName)
        self.clearName.pack(side = LEFT, fill = X, expand = 0)
        nameFrame.pack(fill = X, expand = 0)

        chatFrame = Frame(self.pageOne)
        self.chatButton = Menubutton(chatFrame, width = 8,
                                     text = "SpeedChat",
                                     relief = RAISED,
                                     borderwidth = 2)
        self.chatMenu = Menu(self.chatButton, tearoff = 0)
        self.chatButton['menu'] = self.chatMenu
        self.chatButton.pack(side = LEFT, fill = 'x', expand = 1)
        subMenu = Menu(self.chatMenu, tearoff = 0)
        self.chatMenu.add_cascade(label = 'Basic', menu = subMenu)
        for key in chatKeys:
            if (key % 100) == 0:
                subMenu = Menu(self.chatMenu, tearoff = 0)
                self.chatMenu.add_cascade(label = ChatCategories.get(key,''),
                                          menu = subMenu)
            subMenu.add_command(
                label = chatDict[key],
                command = lambda c=chatDict[key]: self.setToonChat(c))

        self.chatButton2 = Menubutton(chatFrame, width = 8,
                                      text = "Custom Chat",
                                      relief = RAISED,
                                      borderwidth = 2)
        self.chatMenu2 = Menu(self.chatButton2, tearoff = 0)
        self.chatButton2['menu'] = self.chatMenu2
        self.chatButton2.pack(side = LEFT, fill = 'x', expand = 1)
        subMenu = Menu(self.chatMenu2, tearoff = 0)
        self.chatMenu2.add_cascade(label = 'Series 0', menu = subMenu)
        for key in customChatKeys:
            if (key % 100) == 0:
                subMenu = Menu(self.chatMenu2, tearoff = 0)
                self.chatMenu2.add_cascade(
                    label = 'Series %d' % key, 
                    menu = subMenu)
            subMenu.add_command(
                label = customChatDict[key],
                command = lambda c=customChatDict[key]: self.setToonChat(c))

        # Arbitrary string
        self.openChat = Button(chatFrame, text = 'Open Chat',
                               command = self.openToonChat)
        self.openChat.pack(side = LEFT, fill = X, expand = 1)

        # Clear chat string
        self.clearChat = Button(chatFrame, text = 'Clear Chat',
                                command = self.clearToonChat)
        self.clearChat.pack(side = LEFT, fill = X, expand = 1)
        chatFrame.pack(fill = X, expand = 0)

        animFrame = Frame(self.pageOne)        
                
        if not base.config.GetBool('want-new-anims', 1):
            self.animButton = Menubutton(animFrame, width = 18,
                                         text = 'Anims',
                                         relief = RAISED,
                                         borderwidth = 2)
            self.anim = StringVar()
            self.anim.set('')
            self.animMenu = Menu(self.animButton)
            self.animButton['menu'] = self.animMenu
            self.animButton.pack(side = LEFT, expand = 0, fill = X)
            animIndex = 0
            for anim in ToonAnimList:
                if (animIndex % 10) == 0:
                    subMenu = Menu(self.animMenu, tearoff = 0)
                    self.animMenu.add_cascade(label = ToonAnimList[animIndex],
                                              menu = subMenu)
                subMenu.add_command(
                    label = anim,
                    command = lambda a = anim: self.setToonAnim(a))
                animIndex += 1                
        else:        
            self.buttonAdd('Anims',
                       helpMessage='Bring Up Anim Panel',
                       statusMessage='Control Animations!',
                       command=self.rtm.showAnimPanel)
        self.neutralButton = Button(
            animFrame, text = 'Neutral', width = 18,
            command = lambda s=self: s.setToonAnim('neutral'))
        self.neutralButton.pack(side = LEFT, expand = 0, fill = X)
        self.poseSlider = Slider.Slider(animFrame, text = 'Pose:',
                                        min = 0, max = 100, resolution = 1)
        self.poseSlider['command'] = self.poseToon
        self.poseSlider.pack(side = LEFT, fill = X, expand = 0)
        animFrame.pack(expand = 0, fill = X)

        headPoseFrame = Frame(self.pageOne)
        self.headH = Slider.Slider(headPoseFrame, text = 'Head H:',
                                   min = -80, max = 80, resolution = 1,
                                   command = self.setHeadH)
        self.headH.pack(side = LEFT, fill = X, expand = 0)
        self.headP = Slider.Slider(headPoseFrame, text = 'Head P:',
                                   min = -80, max = 80, resolution = 1,
                                   command = self.setHeadP)
        self.headP.pack(side = LEFT, fill = X, expand = 0)
        headPoseFrame.pack(expand=0,fill =X)

        frame = Frame(self.pageOne)
        self.toonSuitTypeButton = Menubutton(frame, width = 18,
                                         text = 'Toon Suit Type',
                                         relief = RAISED,
                                         borderwidth = 2)
        # Associate menu with button and vice versa
        self.toonSuitMenu = Menu(self.toonSuitTypeButton)
        self.toonSuitTypeButton['menu'] = self.toonSuitMenu
        # Pack button
        self.toonSuitTypeButton.pack(side = LEFT, expand = 0, fill = X)
        for suitIndex in range(len(SuitDNAList)):
            if (suitIndex % 8) == 0:
                subMenu = Menu(self.toonSuitMenu, tearoff = 0)
                self.toonSuitMenu.add_cascade(
                    label = SuitTrackList[suitIndex/8],
                    menu = subMenu)
            suit = SuitDNAList[suitIndex]
            suitLabel = suit.split(':')[1].strip()
            subMenu.add_command(
                label = suitLabel,
                command = lambda i = suitIndex: self.putOnSuitSuit(i))
        takeOffSuitButton = Button(frame, text = 'Take off Cog Suit',
                                   command = self.takeOffSuitSuit)
        takeOffSuitButton.pack(side = LEFT, fill = X, expand = 0)
        
        self.handPropChoiceButton = Menubutton(frame, width = 18,
                                         text = 'Choose prop',
                                         relief = RAISED,
                                         borderwidth = 2)
        self.handPropChoiceButton.pack(side = LEFT, expand = 0, fill = X)
        # Associate menu with button and vice versa
        self.props = Menu(self.handPropChoiceButton)
        self.handPropChoiceButton['menu'] = self.props
        for prop in globalPropPool.propTypes.keys():
            self.props.add_command(label = prop, command = lambda selectProp = prop: self.useProp(selectProp))
        frame.pack(fill = X, expand = 0)
        
        frame = Frame(self.pageOne)
        self.addToonButton = Button(frame,
                                    text = 'Add Random Toon',
                                    command = self.rtm.makeRandomToon)
        self.addToonButton.pack(side = LEFT, expand = 1, fill = X)
        
        self.createTestToonButton = Button(frame,
                                    text = 'Create Anim Test Toon',
                                    command = self.createTestToon)
        self.createTestToonButton.pack(side = LEFT, expand = 1, fill = X)
        frame.pack(fill = X, expand = 0)

        #
        # SUIT TAB
        #
        self.pageTwo = self.notebook.add('Suits')

        # SUIT TRACK
        self.suitTrack = StringVar()
        self.suitTrack.set('Corporate')
        trackFrame = Frame(self.pageTwo)
        Label(trackFrame,text='Track:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            trackFrame, 'Track', 'Corporate',
            self.suitTrack, 'Corporate', self.setSuitTrack,
            help = 'Corporate Suit',
            side = LEFT)
        self.newCreateRadiobutton(
            trackFrame, 'Track', 'Legal',
            self.suitTrack, 'Legal', self.setSuitTrack,
            help = 'Legal Suit',
            side = LEFT)
        self.newCreateRadiobutton(
            trackFrame, 'Track', 'Financial',
            self.suitTrack, 'Financial', self.setSuitTrack,
            help = 'Financial Suit',
            side = LEFT)
        self.newCreateRadiobutton(
            trackFrame, 'Track', 'Sales',
            self.suitTrack, 'Sales', self.setSuitTrack,
            help = 'Sales Suit',
            side = LEFT)
        self.newCreateRadiobutton(
            trackFrame, 'Track', 'Random',
            self.suitTrack, 'Random', self.setSuitTrack,
            help = 'Random Suit',
            side = LEFT)
        trackFrame.pack(fill = X, expand = 0)

        # SUIT LEVEL
        self.suitLevel = IntVar()
        self.suitLevel.set(0)
        levelFrame = Frame(self.pageTwo)
        Label(levelFrame,text='Level:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        for i in range(8):
            self.newCreateRadiobutton(
                levelFrame, 'Level', '%d' % i,
                self.suitLevel, i, self.setSuitLevel,
                help = 'Level %d Suit' % i,
                side = LEFT)
        self.newCreateRadiobutton(
            levelFrame, 'Level', 'Random',
            self.suitLevel, -1, self.setSuitLevel,
            help = 'Random Suit Level',
            side = LEFT)
        levelFrame.pack(fill = X, expand = 0)

        # SPECIFIC SUIT
        frame = Frame(self.pageTwo)
        self.suitName = Label(frame, text = 'flunky', width = 14)
        self.suitName.pack(side = LEFT, expand = 0, fill = X)
        Label(frame, text = 'Track:', width = 10).pack(
            side = LEFT, expand = 0, fill = X)
        self.trackLabel = Label(frame, text = 'Corporate', width = 8)
        self.trackLabel.pack(side = LEFT, expand = 0, fill = X)
        Label(frame, text = 'Level:', width = 10).pack(
            side = LEFT, expand = 0, fill = X)
        self.levelLabel = Label(frame, text = '0', width = 8)
        self.levelLabel.pack(side = LEFT, expand = 0, fill = X)
        self.suitTypeButton = Menubutton(frame, width = 18,
                                         text = 'Suit Type',
                                         relief = RAISED,
                                         borderwidth = 2)
        # Associate menu with button and vice versa
        self.suitMenu = Menu(self.suitTypeButton)
        self.suitTypeButton['menu'] = self.suitMenu
        # Pack button
        self.suitTypeButton.pack(side = LEFT, expand = 0, fill = X)
        for suitIndex in range(len(SuitDNAList)):
            if (suitIndex % 8) == 0:
                subMenu = Menu(self.suitMenu, tearoff = 0)
                self.suitMenu.add_cascade(label = SuitTrackList[suitIndex/8],
                                          menu = subMenu)
            suit = SuitDNAList[suitIndex]
            suitLabel = suit.split(':')[1].strip()
            subMenu.add_command(
                label = suitLabel,
                command = lambda i = suitIndex: self.setSuitType(i))
        frame.pack(fill = X, expand = 0)

        suitChatFrame = Frame(self.pageTwo)

        self.suitFaceoffButton = Menubutton(suitChatFrame, width = 8,
                                            text = "Faceoff Taunts",
                                            relief = RAISED,
                                            borderwidth = 2)
        self.suitFaceoffMenu = Menu(self.suitFaceoffButton, tearoff = 0)
        self.suitFaceoffButton['menu'] = self.suitFaceoffMenu
        self.suitFaceoffButton.pack(side = LEFT, fill = 'x', expand = 1)
        for key in faceoffTauntsKeys:
            subMenu = Menu(self.suitFaceoffMenu, tearoff = 0)
            suitName = SuitAttributes[key]['name']
            self.suitFaceoffMenu.add_cascade(label = suitName, menu = subMenu)
            for taunt in faceoffTaunts[key]:
                subMenu.add_command(
                    label = taunt,
                    command = lambda t=taunt: self.setToonChat(t))

        self.suitAttackButton = Menubutton(suitChatFrame, width = 8,
                                           text = "Attack Taunts",
                                           relief = RAISED,
                                           borderwidth = 2)
        self.suitAttackMenu = Menu(self.suitAttackButton, tearoff = 0)
        self.suitAttackButton['menu'] = self.suitAttackMenu
        self.suitAttackButton.pack(side = LEFT, fill = 'x', expand = 1)
        for key in attackTauntsKeys:
            subMenu = Menu(self.suitAttackMenu, tearoff = 0)
            self.suitAttackMenu.add_cascade(label = key, menu = subMenu)
            for taunt in attackTaunts[key]:
                subMenu.add_command(
                    label = taunt,
                    command = lambda t=taunt: self.setToonChat(t))

        # Arbitrary string
        self.openSuitChat = Button(suitChatFrame, text = 'Open Taunt',
                                   command = self.openToonChat)
        self.openSuitChat.pack(side = LEFT, fill = X, expand = 1)

        # Clear suitChat string
        self.clearSuitChat = Button(suitChatFrame, text = 'Clear Suit Taunt',
                                command = self.clearToonChat)
        self.clearSuitChat.pack(side = LEFT, fill = X, expand = 1)
        suitChatFrame.pack(fill = X, expand = 0)

        suitAnimFrame = Frame(self.pageTwo)
        self.suitAnimButton = Menubutton(suitAnimFrame, width = 18,
                                     text = 'SuitAnims',
                                     relief = RAISED,
                                     borderwidth = 2)
        self.suitAnim = StringVar()
        self.suitAnim.set('')
        self.suitAnimMenu = Menu(self.suitAnimButton)
        self.suitAnimButton['menu'] = self.suitAnimMenu
        self.suitAnimButton.pack(side = LEFT, expand = 0, fill = X)
        for catIndex in range(len(SuitAnimCategories)):
            subMenu = Menu(self.suitAnimMenu, tearoff = 0)
            self.suitAnimMenu.add_cascade(label = SuitAnimCategories[catIndex],
                                          menu = subMenu)
            for anim in SuitAnimList[catIndex]:
                subMenu.add_command(
                    label = anim[1],
                    command = lambda a = anim[0]: self.setSuitAnim(a))
        self.suitNeutralButton = Button(
            suitAnimFrame, text = 'Neutral', width = 18,
            command = lambda s=self: s.setSuitAnim('neutral'))
        self.suitNeutralButton.pack(side = LEFT, expand = 0, fill = X)
        self.suitPoseSlider = Slider.Slider(suitAnimFrame, text = 'Pose:',
                                            min = 0, max = 100, resolution = 1)
        self.suitPoseSlider['command'] = self.poseSuit
        self.suitPoseSlider.pack(side = LEFT, fill = X, expand = 0)
        suitAnimFrame.pack(expand = 0, fill = X)

        suitNameFrame = Frame(self.pageTwo)
        self.clearSuitName = Button(suitNameFrame, text = 'Clear Name',
                                    command = self.clearToonName)
        self.clearSuitName.pack(side = LEFT, fill = X, expand = 0)
        suitNameFrame.pack(expand = 0, fill = X)

        self.addSuitButton = Button(self.pageTwo,
                                    text = 'Add Suit',
                                    command = self.addSuit)
        self.addSuitButton.pack(expand = 1, fill = NONE)

        #
        # Doodle Tab
        #
        
        self.pageThree = self.notebook.add('Doodles')

        # Doodle head parts
        self.doodleHead = IntVar()
        self.doodleHead.set(None)
        doodleHeadFrame = Frame(self.pageThree)
        Label(doodleHeadFrame,text='Head Part:',width=8,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleHeadFrame, 'Head', 'None',
            self.doodleHead, -1, self.setDoodleHead,
            help = 'No Head Part (-1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleHeadFrame, 'Head', 'Feathers',
            self.doodleHead, 0, self.setDoodleHead,
            help = 'Head Feathers (0)',
            side = LEFT)
        doodleHeadFrame.pack(fill = X, expand = 0)

        # Doodle ears
        self.doodleEars = IntVar()
        self.doodleEars.set(None)
        doodleEarsFrame = Frame(self.pageThree)
        Label(doodleEarsFrame,text='Ears:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'None',
            self.doodleEars, -1, self.setDoodleEars,
            help = 'No Ears Part (-1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'Horns',
            self.doodleEars, 0, self.setDoodleEars,
            help = 'Horns (0)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'Antennae',
            self.doodleEars, 1, self.setDoodleEars,
            help = 'Antennae (1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'Dog',
            self.doodleEars, 2, self.setDoodleEars,
            help = 'Dog ears (2)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'Cat',
            self.doodleEars, 3, self.setDoodleEars,
            help = 'Cat ears (3)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleEarsFrame, 'Ears', 'Rabbit',
            self.doodleEars, 4, self.setDoodleEars,
            help = 'Rabbit ears (4)',
            side = LEFT)
        doodleEarsFrame.pack(fill = X, expand = 0)

        # Doodle nose
        self.doodleNose = IntVar()
        self.doodleNose.set(None)
        doodleNoseFrame = Frame(self.pageThree)
        Label(doodleNoseFrame,text='Nose:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleNoseFrame, 'Nose', 'None',
            self.doodleNose, -1, self.setDoodleNose,
            help = 'No Nose Part (-1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleNoseFrame, 'Nose', 'Clown',
            self.doodleNose, 0, self.setDoodleNose,
            help = 'Clown Nose (0)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleNoseFrame, 'Nose', 'Dog',
            self.doodleNose, 1, self.setDoodleNose,
            help = 'Dog Nose (1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleNoseFrame, 'Nose', 'Oval',
            self.doodleNose, 2, self.setDoodleNose,
            help = 'Oval-shaped Nose (2)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleNoseFrame, 'Nose', 'Pig',
            self.doodleNose, 3, self.setDoodleNose,
            help = 'Upturned Nose (3)',
            side = LEFT)
        doodleNoseFrame.pack(fill = X, expand = 0)

        # Doodle tail
        self.doodleTail = IntVar()
        self.doodleTail.set(None)
        doodleTailFrame = Frame(self.pageThree)
        Label(doodleTailFrame,text='Tail:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleTailFrame, 'Tail', 'None',
            self.doodleTail, -1, self.setDoodleTail,
            help = 'No Tail Part (-1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleTailFrame, 'Tail', 'Cat',
            self.doodleTail, 0, self.setDoodleTail,
            help = 'Cat Tail (0)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleTailFrame, 'Tail', 'Long',
            self.doodleTail, 1, self.setDoodleTail,
            help = 'Long Tail (1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleTailFrame, 'Tail', 'Bird',
            self.doodleTail, 2, self.setDoodleTail,
            help = 'Feathery Tail (2)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleTailFrame, 'Tail', 'Bunny',
            self.doodleTail, 3, self.setDoodleTail,
            help = 'Fluffy, Cotton Tail (3)',
            side = LEFT)
        doodleTailFrame.pack(fill = X, expand = 0)
        
        # Doodle body
        self.doodleBody = IntVar()
        self.doodleBody.set(None)
        doodleBodyFrame = Frame(self.pageThree)
        Label(doodleBodyFrame,text='Body:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Dots',
            self.doodleBody, 0, self.setDoodleBody,
            help = 'Polka Dots (0)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Stripes',
            self.doodleBody, 1, self.setDoodleBody,
            help = 'Three Stripes (1)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Tiger',
            self.doodleBody, 2, self.setDoodleBody,
            help = 'Tiger Stripes (2)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Tummy',
            self.doodleBody, 3, self.setDoodleBody,
            help = 'Darker Tummy (3)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Turtle',
            self.doodleBody, 4, self.setDoodleBody,
            help = 'Green Turtle (4)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Giraffe',
            self.doodleBody, 5, self.setDoodleBody,
            help = 'Giraffe (5)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleBodyFrame, 'Body', 'Leopard',
            self.doodleBody, 6, self.setDoodleBody,
            help = 'Leopard (6)',
            side = LEFT)
        doodleBodyFrame.pack(fill = X, expand = 0)

        # Doodle main color
        self.doodleColor = IntVar()
        self.doodleColor.set(-1)
        colorFrame = Frame(self.pageThree)
        Label(colorFrame,text='Body Color:',width=16,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        for i in range(2):
            cf = Frame(colorFrame)
            for j in range(13):
                index = i * 13 + j
                color = self.transformRGB(PetDNA.AllPetColors[index])
                b = Button(cf, width = 1, height = 1, background = color,
                           text = "%d" % index,
                           command = lambda ci=index: self.setDoodleColor(ci))
                b.pack(side = LEFT, fill = X, expand = 0)
                self.doodleColorButtonList.append(b)
            cf.pack(fill = X, expand = 0)
        colorFrame.pack(fill = X, expand = 0)
        
        # Doodle part color scale
        self.doodleColorScale = IntVar()
        self.doodleColorScale.set(-1)
        colorFrame = Frame(self.pageThree)
        Label(colorFrame,text='Part Color Scale:',width=16,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        for index in range(len(PetDNA.ColorScales)):
            c = PetDNA.ColorScales[index]
            color = self.transformRGB(VBase4(c/1.2,c/1.2,c/1.2,1.0))
            b = Button(colorFrame, width = 1, height = 1, background = color,
                       text = "%d" % index,
                       command = lambda ci=index: self.setDoodleColorScale(ci))
            b.pack(side = LEFT, fill = X, expand = 0)
            self.doodleColorScaleButtonList.append(b)
        colorFrame.pack(fill = X, expand = 0)

        # Doodle eye color
        self.doodleEyeColor = IntVar()
        self.doodleEyeColor.set(-1)
        colorFrame = Frame(self.pageThree)
        Label(colorFrame,text='Eye Color:',width=16,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        for index in range(len(PetDNA.PetEyeColors)):
            color = self.transformRGB(PetDNA.PetEyeColors[index])
            b = Button(colorFrame, width = 1, height = 1, background = color,
                       text = "%d" % index,
                       command = lambda ci=index: self.setDoodleEyeColor(ci))
            b.pack(side = LEFT, fill = X, expand = 0)
            self.doodleEyeColorButtonList.append(b)
        colorFrame.pack(fill = X, expand = 0)

        # Doodle gender
        self.doodleGender = IntVar()
        self.doodleGender.set(None)
        doodleGenderFrame = Frame(self.pageThree)
        Label(doodleGenderFrame,text='Gender:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            doodleGenderFrame, 'Gender', 'Girl',
            self.doodleGender, 0, self.setDoodleGender,
            help = 'Eyelashes (0)',
            side = LEFT)
        self.newCreateRadiobutton(
            doodleGenderFrame, 'Gender', 'Boy',
            self.doodleGender, 1, self.setDoodleGender,
            help = 'No Eyelashes (1)',
            side = LEFT)
        doodleGenderFrame.pack(fill = X, expand = 0)
        
        # Doodle anim menu
        doodleAnimFrame = Frame(self.pageThree)
        self.doodleAnimButton = Menubutton(doodleAnimFrame, width = 18,
                                           text = 'DoodleAnims',
                                           relief = RAISED,
                                           borderwidth = 2)
        self.doodleAnim = StringVar()
        self.doodleAnim.set('')
        self.doodleAnimMenu = Menu(self.doodleAnimButton)
        self.doodleAnimButton['menu'] = self.doodleAnimMenu
        self.doodleAnimButton.pack(side = LEFT, expand = 0, fill = X)
        animIndex = 0
        for anim in DoodleAnimList:
            if (animIndex % 10) == 0:
                subMenu = Menu(self.doodleAnimMenu, tearoff = 0)
                self.doodleAnimMenu.add_cascade(label = DoodleAnimList[animIndex],
                                          menu = subMenu)
            subMenu.add_command(
                label = anim,
                command = lambda a = anim: self.setDoodleAnim(a))
            animIndex += 1

        # Doodle neutral button
        self.doodleNeutralButton = Button(
            doodleAnimFrame, text = 'Neutral', width = 18,
            command = lambda s=self: s.setDoodleAnim('neutral'))
        self.doodleNeutralButton.pack(side = LEFT, expand = 0, fill = X)
        self.doodlePoseSlider = Slider.Slider(doodleAnimFrame, text = 'Pose:',
                                              min = 0, max = 100, resolution = 1)
        self.doodlePoseSlider['command'] = self.poseDoodle
        self.doodlePoseSlider.pack(side = LEFT, fill = X, expand = 0)
        doodleAnimFrame.pack(expand = 0, fill = X)

        self.addDoodleButton = Button(self.pageThree,
                                      text = 'Add Doodle',
                                      command = self.addDoodle)
        self.addDoodleButton.pack(expand = 1, fill = NONE)


        self.notebook.pack(fill = BOTH, expand = 1)
        self.notebookFrame.pack(fill = BOTH, expand = 1)

        self.fMaya = IntVar()
        self.fMaya.set(1)
        self.mayaButton = Checkbutton(self.rightFrame,
                                      text = 'Maya Cam',
                                      width = 6,
                                      variable = self.fMaya,
                                      command = self.toggleMaya)
        self.mayaButton.pack(side = LEFT, expand = 1, fill = X)

        self.rightFrame.pack(fill = BOTH, expand = 1)
        # Put this here so it isn't called right away
        self.notebook['raisecommand'] = self.switchAvatarType

        self.framePane.pack(fill = BOTH, expand = 1)

        propsPage = self.notebook.add('Props')

        # PROPS
        Label(propsPage, text = 'Props',
              font=('MSSansSerif', 14, 'bold')).pack(expand = 0)
        self.addPropsButton = Button(
            propsPage,
            text = 'ADD PROP',
            command = self.addProp)
        self.addPropsButton.pack(fill = X, padx = 20, pady = 10)
        codes = []
        self.styleManager = self.rtm.styleManager
        
        codes = (self.styleManager.getCatalogCodes('prop') +
                 self.styleManager.getCatalogCodes('holiday_prop'))
        codes.sort()

        self.propSelector = Pmw.ComboBox(
            propsPage,
            dropdown = 0,
            listheight = 200,
            labelpos = W,
            label_width = 12,
            label_anchor = W,
            label_text = 'Prop type:',
            entry_width = 30,
            selectioncommand = self.setPropType,
            scrolledlist_items = codes
            )
        self.propType = self.styleManager.getCatalogCode('prop', 0)
        self.propSelector.selectitem(
            self.styleManager.getCatalogCode('prop', 0))
        self.propSelector.pack(expand = 1, fill = BOTH)

        # Effects tab
        effectsPage = self.notebook.add('Effects')

        self.holiday = IntVar()
        self.holiday.set(0)
        holidayFrame = Frame(effectsPage)
        Label(holidayFrame,text='Holiday:',width=6,
              anchor = W, justify = LEFT).pack(side = LEFT, expand = 0)
        self.newCreateRadiobutton(
            holidayFrame, 'Holiday', 'July 4th',
            self.holiday, 0, None,
            help = 'July 4th',
            side = LEFT)
        self.newCreateRadiobutton(
            holidayFrame, 'Holiday', 'New Year',
            self.holiday, 1, None,
            help = 'New Year',
            side = LEFT)
        holidayFrame.pack(fill = X, expand = 0)

        fireworkTypeFrame = Frame(effectsPage)
        Label(fireworkTypeFrame, text = 'Type:',
              anchor = W, justify = LEFT,
              width=6).pack(side = LEFT, expand = 0)
        self.fireworkType = IntVar()
        self.fireworkType.set(0)
        for i in range(6):
            self.newCreateRadiobutton(
                fireworkTypeFrame, 'FireworkType', '%d'%i,
                self.fireworkType, i, None,
                side = LEFT)
        fireworkTypeFrame.pack(fill = X, expand = 0)

        fireworkButton = Button(
            effectsPage,
            text = 'Firework',
            command = self.firework)
        fireworkButton.pack(fill = X, padx = 20, pady = 10)

        snowButton = Button(
            effectsPage,
            text = 'Toggle Snow',
            command = self.toggleSnow)
        snowButton.pack(fill = X, padx = 20, pady = 10)

        mainFrame.pack(fill = BOTH, expand = 1)
        self.createButtons()

        self.initialiseoptions(RobotToonControlPanel)
        # Enable widget commands
        self.updateToonInfo()
        self.setSuitTrack()
        self.setSuitLevel()
        self.fDoIt = 1
        self.snow = None

    def importMaya(self):
        mbFilename = askopenfilename(
            defaultextension = '.mb',
            filetypes = (('Maya Files', '*.mb'),
                         ('Panda Models', '*.bam *.egg'),
                         ('All files', '*')),
            initialdir = '.',
            title = 'Load Maya File',
            parent = self.component('hull')
            )

        mbFilePath = Filename.fromOsSpecific(mbFilename).getFullpath()
        eggFilePath = os.path.splitext(mbFilePath)[0] + '.egg'
        os.system('maya2egg_bin  -o' + eggFilePath + ' ' + mbFilePath)
        newNode = loader.loadModel(eggFilePath, noCache=True)
        newNode.ls()
        
    def toggleSnow(self):
        if self.snow:
            self.snow.cleanup()
            del self.snow
            del self.snowRender
            self.snow = None
        else:
            self.snow = BattleParticles.loadParticleFile('snowdisk.ptf')
            self.snow.setPos(0, 0, 5)  # start the snow slightly above the camera
            self.snowRender = render.attachNewNode('snowRender')
            self.snowRender.setDepthWrite(0)
            self.snowRender.setBin('fixed', 1)
            self.snowFade = None       
            self.snow.start(camera, self.snowRender)

    def firework(self):
        holidays = [ToontownGlobals.JULY4_FIREWORKS, ToontownGlobals.NEWYEARS_FIREWORKS]
        show = FireworkShows.getShow(holidays[self.holiday.get()], self.fireworkType.get())
        
        mainShow = Sequence()
        currentT = 0
        startT = 0
        for effect in show:
            waitTime, style, colorIndex1, colorIndex2, amp, x, y, z = effect
            if waitTime > 0:
                currentT += waitTime
                mainShow.append(Wait(waitTime))
            # Do not add the firework Ival if our start time is greater than
            # the current time since the Func Interval can not be skipped over
            # and all the skipped over fireworks will otherwise fire at once
            if currentT >= startT:
                mainShow.append(
                    Func(
                         Fireworks.shootFirework,
                         style,
                         x,
                         y,
                         z,
                         colorIndex1,
                         colorIndex2,
                         amp
                    )
                )

        mainShow.start()
    
    def createTestToon(self):
        """
        Create a toon with the following properties:
        Gender: male

        Species: dog
        Head: sl
        Eyes: normal
        Muzzles: normal
        Torso: MS
        Legs: m
        Color: All
        skintone BRIGHT GREEN
        Tops: 00 - solid ,   color 0
        Bottoms: 00 - plain w/ pockets ,  color 0
        """
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties("dsl" ,"ms" ,"m" ,"m" ,15 ,0 ,15 ,15 ,0 ,0 ,0 ,0 ,0 ,0 ,)
        self.rtm.makeToonFromProperties(dna.asTuple(), pos = Point3(0), hpr = Point3(180,0,0),
                                 startPos = Point3(0), startHpr = Point3(0),
                                 endPos = Point3(0,1,0), endHpr = Point3(0),
                                 state = 'neutral')
        self.updateToonInfo()
        
    def addProp(self):
        self.rtm.addProp(self.propType)
        
    def setPropType(self, name):
        self.propType = name
        self.rtm.setCurrent('prop_texture', self.propType)

    # [gjeon] to toggle maya cam mode
    def toggleMaya(self):
        base.direct.cameraControl.lockRoll = self.fMaya.get()
        direct.cameraControl.useMayaCamControls = self.fMaya.get()

    def toggleAntiAliasing(self):
        if render.getAntialias() > 0:
            render.clearAntialias()
        else:
            render.setAntialias(AntialiasAttrib.MAuto)

    def resizeWindow(self):
        text = askstring('New window size', 'Type new window size such as 800x600\n',
                         parent = self.component('hull'))
        tokens = text.split('x')
        if len(tokens) != 2:
            return
        width = string.atoi(tokens[0])
        height = string.atoi(tokens[1])
        
        props = WindowProperties(base.win.getProperties())
        props.setSize(width, height)
        base.win.requestProperties(props)

    def switchAvatarType(self, page = 'Toons'):
        if page == 'Toons':
            self.rtm.avatarType = 't'
        elif page == 'Suits':
            self.rtm.avatarType = 's'
        else:
            self.rtm.avatarType = 'd'
        direct.deselectAll()

    def setSuitName(self):
        if ((self.suitTrack.get() == 'Random') or
            (self.suitLevel.get() < 0)):
            self.suitName['text'] = 'Random'
        else:
            suitIndex = (SuitTrackList.index(self.suitTrack.get()) * 8 +
                         self.suitLevel.get())
            suitName = SuitDNAList[suitIndex].split(':')[1].strip()
            self.suitName['text'] = suitName

    def setSuitTrack(self):
        track = self.suitTrack.get()
        self.trackLabel['text'] = track
        self.rtm.suitTrack = track
        self.setSuitName()

    def setSuitLevel(self):
        level = self.suitLevel.get()
        self.rtm.suitLevel = level
        if level < 0:
            self.levelLabel['text'] = 'Random'
        else:
            self.levelLabel['text'] = '%d' % level
        self.setSuitName()

    def setSuitType(self, suitIndex):
        self.suitTrack.set(['Corporate','Legal',
                            'Financial','Sales'][suitIndex/8])
        self.setSuitTrack()
        self.suitLevel.set(suitIndex % 8)
        self.setSuitLevel()
        
    def useProp(self, prop):
        if not self.rtm.selectedToon:
            return
        if hasattr(self, "propHandle") and self.propHandle:
            self.propHandle.detachNode()
            del self.propHandle
        hands = self.rtm.selectedToon.getRightHands()
        self.propHandle = globalPropPool.getProp(prop)
        handHigh = hands[0].attachNewNode('highLODHand')
        handMed = hands[1].attachNewNode('medLODHand')
        self.propHandle.reparentTo(handHigh)
        
        handHigh.instanceTo(handMed)        
        return prop

    def addSuit(self):
        self.rtm.makeRandomToon()

    def setDoodleHead(self):
        head = self.doodleHead.get()
        self.rtm.doodleHead = head

    def setDoodleEars(self):
        ears = self.doodleEars.get()
        self.rtm.doodleEars = ears

    def setDoodleNose(self):
        nose = self.doodleNose.get()
        self.rtm.doodleNose = nose

    def setDoodleTail(self):
        tail = self.doodleTail.get()
        self.rtm.doodleTail = tail

    def setDoodleBody(self):
        body = self.doodleBody.get()
        self.rtm.doodleBody = body

    def setDoodleGender(self):
        gender = self.doodleGender.get()
        self.rtm.doodleGender = gender

    def setDoodleColor(self, colorIndex):
        self.doodleColor.set(colorIndex)
        self.rtm.doodleColor = colorIndex

    def setDoodleColorScale(self, colorIndex):
        self.doodleColorScale.set(colorIndex)
        self.rtm.doodleColorScale = colorIndex

    def setDoodleEyeColor(self, colorIndex):
        self.doodleEyeColor.set(colorIndex)
        self.rtm.doodleEyeColor = colorIndex
        
    def addDoodle(self):
        self.rtm.makeRandomToon()

    def setTop(self, topName, fUpdateVariants = 0):
        if fUpdateVariants:
            topIndex = int(topName[:3])
            self.topsVariants = self.topsDict[topIndex]
            self.topsCounter.setentry(0)
            self.topsCounter.invoke()

    def __switchTops(self, text):
        value = string.atoi(text)
        if (value < 0) or (value >= len(self.topsVariants)):
            return Pmw.ERROR
        else:
            if self.fDoIt:
                self.topsCounter.invoke()
            return Pmw.OK

    def setTopVariant(self, event = None):
        if self.fDoIt and self.rtm.selectedToon:
            topStyle = self.topsVariants[self.topsIndex.get()]
            st = self.rtm.selectedToon
            st.style.topTex = topStyle[0]
            st.style.topTexColor = topStyle[1]
            st.style.sleeveTex = topStyle[2]
            st.style.sleeveTexColor = topStyle[3]
            st.generateToonClothes()        
            
    def setBottom(self, bottomName, fUpdateVariants = 0):
        if fUpdateVariants:
            bottomIndex = int(bottomName[:2])
            self.bottomsVariants = self.bottomsDict[bottomIndex]
            self.bottomsCounter.setentry(0)
            self.bottomsCounter.invoke()

    def __switchBottoms(self, text):
        if not Pmw.integervalidator(text):
            return Pmw.ERROR
        value = string.atoi(text)
        if (value < 0) or (value >= len(self.bottomsVariants)):
            return Pmw.ERROR
        else:
            if self.fDoIt:
                self.bottomsCounter.invoke()
            return Pmw.OK

    def setBottomVariant(self, event = None):
        if self.fDoIt and self.rtm.selectedToon:
            bottomStyle = self.bottomsVariants[self.bottomsIndex.get()]
            st = self.rtm.selectedToon
            st.style.botTex = bottomStyle[0]
            st.style.botTexColor = bottomStyle[1]
            st.generateToonClothes()        
            
    def setToonColor(self, colorIndex):
        cm = self.colorMode.get()
        st = self.rtm.selectedToon
        if st:
            dna = st.style
            if cm == 'all':
                dna.armColor = colorIndex
                dna.legColor = colorIndex
                dna.headColor = colorIndex
            elif cm == 'arms':
                dna.armColor = colorIndex
            elif cm == 'gloves':
                dna.gloveColor = colorIndex
            elif cm == 'legs':
                dna.legColor = colorIndex
            elif cm == 'head':
                dna.headColor = colorIndex
            st.swapToonColor(dna)

    def updateToonInfo(self):
        st = self.rtm.selectedToon
        if st:
            dna = st.style
            if not hasattr(dna, 'type') or dna.type == 's':
                return
            self.fDoIt = 0
            self.setGender(dna.gender)
            self.species.set(self.speciesDict[dna.head[0]])
            self.setSpecies(fUpdateHead = 0)
            self.head.set(dna.head[1:])
            self.torso.set(dna.torso)
            self.legs.set(dna.legs)
            topStyle = dna.asTuple()[8:12]
            self.topsMenu.invoke(ToonTopsDict[topStyle[0]])
            idx = self.topsVariants.index(topStyle)
            self.topsIndex.set(idx)
            bottomStyle = dna.asTuple()[12:]
            self.bottomsMenu.invoke(self.toonBottomsDict[bottomStyle[0]])
            idx = self.bottomsVariants.index(bottomStyle)
            self.bottomsIndex.set(idx)
            self.fDoIt = 1
    
    def selectLOD(self):
        """
        swap the lod
        """
        st = self.rtm.selectedToon
        if st:
            st.useLOD(self.lod.get())

    def swapGender(self):
        st = self.rtm.selectedToon
        if st:
            oldGender = st.style.gender
            if self.gender.get() != oldGender:
                st.style.gender = self.gender.get()
                topTex = ToonDNA.getRandomTop(st.style.gender)
                botStyle = ToonDNA.getRandomBottom(st.style.gender)
                st.style.topTex = topTex[0]
                st.style.topTexColor = topTex[1]
                st.style.sleeveTex = topTex[2]
                st.style.sleeveTexColor = topTex[3]
                st.style.botTex = botStyle[0]
                st.style.botTexColor = botStyle[1]
                st.swapToonHead(st.style.head)
                # Deal with those damn pants!
                st.style.torso = 'ms'
                st.swapToonTorso(st.style.torso)
                st.generateToonClothes()
                st.loop(st.state)
                self.updateGenderRelatedInfo()

    def setGender(self, gender):
        self.gender.set(gender)
        self.updateGenderRelatedInfo()

    def updateGenderRelatedInfo(self):
        gender = self.gender.get()
        if gender == 'm':
            self.sdButton['state'] = DGG.DISABLED
            self.mdButton['state'] = DGG.DISABLED
            self.ldButton['state'] = DGG.DISABLED
            activeColorList = ToonDNA.defaultBoyColorList
            self.topsDict = self.maleTopsDict
            self.topsNames = self.maleTopsNames
            self.bottomsDict = self.maleBottomsDict
            self.bottomsNames = self.maleBottomsNames
            self.toonBottomsDict = BoyBottomsDict
        elif gender == 'f':
            self.sdButton['state'] = DGG.NORMAL
            self.mdButton['state'] = DGG.NORMAL
            self.ldButton['state'] = DGG.NORMAL
            activeColorList = ToonDNA.defaultGirlColorList
            self.topsDict = self.femaleTopsDict
            self.topsNames = self.femaleTopsNames
            self.bottomsDict = self.femaleBottomsDict
            self.toonBottomsDict = GirlBottomsDict
            st = self.rtm.selectedToon
            if st:
                torso = st.style.torso
                if torso[1] == 'd':
                    self.bottomsNames = self.femaleSkirtsNames
                else:
                    self.bottomsNames = self.femaleShortsNames
            else:
                self.bottomsNames = self.femaleSkirtsNames
        # Update color tablets
        #index = 0
        #for b in self.colorButtonList:
        #    if index in activeColorList:
        #        b['state'] = DGG.NORMAL
        #        b['text'] = index
        #    else:
        #        b['state'] = DGG.DISABLED
        #        b['text'] = 'X'
        #    index += 1
        # Update clothing option menus
        self.topsMenu.setitems(self.topsNames)
        self.bottomsMenu.setitems(self.bottomsNames)
        if self.rtm.selectedToon:
            topTex = self.rtm.selectedToon.style.topTex
            topVariantIndex = ToonTopsDict[topTex]
            botTex = self.rtm.selectedToon.style.botTex
            bottomVariantIndex = self.toonBottomsDict[botTex]
        else:
            topVariantIndex = ToonTopsDict[0]
            bottomVariantIndex = self.toonBottomsDict[0]
        self.topsMenu.invoke(topVariantIndex)
        self.bottomsMenu.invoke(bottomVariantIndex)
        self.topsCounter.checkentry()
        self.bottomsCounter.checkentry()

    def setSpecies(self, fUpdateHead = 1):
        if self.species.get() == 'Mouse':
            self.slHeadButton['state'] = DGG.DISABLED
            self.llHeadButton['state'] = DGG.DISABLED
            if self.head.get() in ['sl', 'll']:
                self.head.set('ss')
        else:
            self.slHeadButton['state'] = DGG.NORMAL
            self.llHeadButton['state'] = DGG.NORMAL
        if fUpdateHead:
            self.setHead()

    def setHead(self):
        if self.species.get() == 'Duck':
            prefix = 'f' # fowl
        elif self.species.get() == 'Monkey':
            prefix = 'p' # primate
        else:
            prefix = self.species.get()[0].lower()
        self.setHeadType(prefix + self.head.get())

    def setHeadType(self, headType):
        st = self.rtm.selectedToon
        if st:
            st.style.head = headType
            st.swapToonHead(st.style.head)
            
            
    def setMuzzle(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.hideNormalMuzzle()
            self.rtm.selectedToon.hideAngryMuzzle()
            self.rtm.selectedToon.hideSadMuzzle()
            self.rtm.selectedToon.hideLaughMuzzle()
            self.rtm.selectedToon.hideSurpriseMuzzle()
            self.rtm.selectedToon.hideSmileMuzzle()
            muzzle = self.muzzle.get()
            if muzzle == 'normal':
                self.rtm.selectedToon.showNormalMuzzle()
            elif muzzle == 'angry':
                self.rtm.selectedToon.showAngryMuzzle()
            elif muzzle  == 'sad':
                self.rtm.selectedToon.showSadMuzzle()
            elif muzzle == 'smile':
                self.rtm.selectedToon.showSmileMuzzle()
            elif muzzle == 'laugh':
                self.rtm.selectedToon.showLaughMuzzle()
            elif muzzle == 'surprise':
                self.rtm.selectedToon.showSurpriseMuzzle()

    def setEyes(self):
        if self.rtm.selectedToon:
            eyes = self.eyes.get()
            if eyes == 'normal':
                self.rtm.selectedToon.normalEyes()
            elif eyes == 'angry':
                self.rtm.selectedToon.angryEyes()
            elif eyes == 'sad':
                self.rtm.selectedToon.sadEyes()
            self.rtm.selectedToon.startBlink()

    def setHeadH(self, h):
        st = self.rtm.selectedToon
        if st:
            head = st.getPart('head', st.getLODNames()[0])
            head.setH(h)

    def setHeadP(self, p):
        st = self.rtm.selectedToon
        if st:
            head = st.getPart('head', st.getLODNames()[0])
            head.setP(p)

    def swapTorso(self):
        self.setTorsoType(self.torso.get())

    def setTorsoType(self, torsoType):
        st = self.rtm.selectedToon
        if st:
            # Is this a girl that is swapping shorts to skirt or vice versa?
            if ((st.style.getGender() == 'f') and
                (torsoType[1] != st.style.torso[1])):
                # Need to change bot texture and color
                if torsoType[1] == 's':
                    st.style.botTex = 5
                else:
                    st.style.botTex = 0
                st.style.botTexColor = 0
                fUpdate = 1
            else:
                fUpdate = 0
            st.style.torso = torsoType
            st.swapToonTorso(st.style.torso)
            st.loop(st.state)
            if fUpdate:
                self.updateGenderRelatedInfo()

    def swapLegs(self):
        self.setLegsType(self.legs.get())

    def setLegsType(self, legsType):
        st = self.rtm.selectedToon
        if st:
            st.style.legs = legsType
            st.swapToonLegs(st.style.legs)
            st.loop(st.state)

    def setToonName(self, event = None):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.nametag.setName(self.toonName.get())
    
    def setRandomToonName(self):
        if self.rtm.selectedToon:
            if self.rtm.selectedToon.style.gender == 'm':
                boy = 1
                girl = 0
            else:
                boy = 0
                girl = 1
            self.rtm.selectedToon.nametag.setName(
                namegen.randomNameMoreinfo(boy = boy, girl = girl)[-1])
    
    def clearToonName(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.nametag.setName('')

    def setToonChat(self, text):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.nametag.setChat(text, CFSpeech)

    def openToonChat(self):
        text = askstring('Open Chat String', 'Phrase:',
                         parent = self.component('hull'))
        self.setToonChat(text)

    def clearToonChat(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.nametag.clearChat()            

    def setToonAnim(self, anim):
        self.anim.set(anim)
        st = self.rtm.selectedToon
        if st:
            if st.style.type == 't':
                numFrames = st.getNumFrames(anim)
                if numFrames is None:
                    numFrames = 100
                else:
                    numFrames = numFrames - 1 
                self.poseSlider['max'] = numFrames
                
                #self.rtm.selectedToon.loop(anim)  
                
                # This will maintain the animation as the body parts change   
                self.rtm.setToonAnimState(anim)
        
    def poseToon(self, frame):
        st = self.rtm.selectedToon
        if st:
            if st.style.type == 't':
                st.stop()
                anim = self.anim.get()
                if anim is None:
                    anim = 'neutral'
                frame = max(0, frame)
                frame = min(frame, st.getNumFrames(anim))
                st.pose(anim, int(frame))

    def setSuitAnim(self, anim):
        self.suitAnim.set(anim)
        st = self.rtm.selectedToon
        if st:
            if ((st.style.type == 's') or
                ((st.style.type == 't') and (hasattr(st, 'suit')) and
                 (st.suit is not None))):
                numFrames = st.getNumFrames(anim)
                if numFrames is None:
                    numFrames = 100
                else:
                    numFrames = numFrames - 1 
                self.suitPoseSlider['max'] = numFrames
                if st.style.type == 's':
                    # Update toon
                    st.loop(anim)
                else:
                    # Update cog suit
                    st.suit.loop(anim)

    def poseSuit(self, frame):
        st = self.rtm.selectedToon
        if st:
            if ((st.style.type == 's') or
                ((st.style.type == 't') and (hasattr(st, 'suit')) and
                 (st.suit is not None))):
                st.stop()
                anim = self.suitAnim.get()
                if anim is None:
                    anim = 'neutral'
                frame = max(0, frame)
                frame = min(frame, st.getNumFrames(anim))
                if st.style.type == 's':
                    # Update toon
                    st.pose(anim, int(frame))
                else:
                    # Update cog suit
                    st.suit.pose(anim, int(frame))

    def putOnSuitSuit(self, suitIndex):
        if self.rtm.selectedToon:
            if isinstance(self.rtm.selectedToon, RobotToon):
                desc = SuitDNAList[suitIndex]
                dna = desc.split(':')[0].strip()
                self.rtm.selectedToon.putOnSuit(dna)

    def takeOffSuitSuit(self):
        if self.rtm.selectedToon:
            if isinstance(self.rtm.selectedToon, RobotToon):
                self.rtm.selectedToon.takeOffSuit()

    def setDoodleAnim(self, anim):
        self.anim.set(anim)
        st = self.rtm.selectedToon
        if st:
            if (isinstance(st.style, types.ListType) or isinstance(st.style, types.TupleType)):
                numFrames = st.getNumFrames(anim)
                if numFrames is None:
                    numFrames = 100
                else:
                    numFrames = numFrames - 1 
                self.poseSlider['max'] = numFrames

                self.rtm.selectedToon.loop(anim)

    def poseDoodle(self, frame):
        st = self.rtm.selectedToon
        if st:
            if (isinstance(st.style, types.ListType) or isinstance(st.style, types.TupleType)):
                st.stop()
                anim = self.anim.get()
                if anim is None:
                    anim = 'neutral'
                frame = max(0, frame)
                frame = min(frame, st.getNumFrames(anim))
                st.pose(anim, int(frame))

    def createButtons(self):
        self.buttonAdd('Stand Up!',
                       helpMessage='Upright selected toon',
                       statusMessage='Stop slouching!',
                       command=self.uprightSelectedToon)
        self.buttonAdd('Face Camera',
                       helpMessage='Turn selected toon toward camera',
                       statusMessage='Look at me!',
                       command=self.rtm.faceCamera)
        self.buttonAdd('Look Around',
                       helpMessage='Start look around task',
                       statusMessage='Look around start',
                       command=self.startToonLookAround)
        self.buttonAdd('Look Ahead',
                       helpMessage='Stop look around task',
                       statusMessage='Look around stop',
                       command=self.stopToonLookAround)
        self.buttonAdd('Toggle Sky',
                       helpMessage='Toggle Sky visibility',
                       statusMessage='Somewhere over the rainbow!',
                       command=self.rtm.toggleSky)
        self.buttonAdd('Toggle Grid',
                       helpMessage='Toggle grid visibility',
                       statusMessage='Show DIRECT Grid',
                       command=self.rtm.toggleGrid)
        self.buttonAdd('Screenshot',
                       helpMessage='Take Screenshot',
                       statusMessage='Say Cheese!',
                       command=self.takeScreenshot)                       
        self.buttonAdd('Log',
                       helpMessage='Log Toon DNA',
                       statusMessage='Write Log',
                       command=self.appendRtmState)
        self.buttonAdd('Render',
                       helpMessage='Render Animation',
                       statusMessage='Go!',
                       command=self.renderMovie)                       
        self.buttonAdd('Help',
                       helpMessage='RTM Help',
                       statusMessage='Click for help',
                       command=self.showHelp)
        

    # STYLE/DNA FILE FUNCTIONS
    def loadSpecifiedDNAFile(self):
        path = dnaDirectory.toOsSpecific()
        if not os.path.isdir(path):
            print 'Robot Toon Manager Warning: Invalid default DNA directory!'
            print 'Using current directory'
            path = '.'
        dnaFilename = askopenfilename(
            defaultextension = '.dna',
            filetypes = (('DNA Files', '*.dna'),('All files', '*')),
            initialdir = path,
            title = 'Load DNA File',
            parent = self.component('hull'))
        if dnaFilename:
            self.loadDNAFromFile(dnaFilename)
        print "Finished Load: ", dnaFilename

    def loadDNAFromFile(self, filename):
        # Reset level, destroying existing scene/DNA hierarcy
        self.resetScene()

        node = loadDNAFile(DNASTORE,
                           Filename.fromOsSpecific(filename).cStr(),
                           CSDefault, 1)

        self.npToplevel = render.attachNewNode(node)

    def resetScene(self):
        if self.npToplevel:
            self.npToplevel.removeNode()
            self.npToplevel = None

    def toggleBalloon(self):
        # 'balloon' shows ballon help
        # 'status' shows status bar
        # 'both' shows in both places
        # 'none' shows nothing
        if self.toggleBalloonVar.get():
            self.balloon().configure(state = 'both')
        else:
            self.balloon().configure(state = 'none')
            
    def onDestroy(self, event):
        """ Called on Robot Toon Manager Panel shutdown """
        del self.rtm

    ### IN SUPPORT OF DEMO
    def _setServerString(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.updateDNA(self.serverString.get())
            self.rtm.selectedToon.loop('neutral')
            self.updateToonInfo()

    def uprightSelectedToon(self):
        if self.rtm.selectedToon:
            h = self.rtm.selectedToon.getH(render)
            self.rtm.selectedToon.setHpr(render,h,0,0)

    def startToonLookAround(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.startLookAround()

    def stopToonLookAround(self):
        if self.rtm.selectedToon:
            self.rtm.selectedToon.stopLookAround()

    def renderMovie(self):
        duration = askfloat('Render duration', 'Type duration of animation in sec.\n',
                         parent = self.component('hull'))

        if duration <= 0:
            return

        self.filename = asksaveasfilename(
            initialdir = self.lastPath,
            title = 'Enter name of file...',
            parent = self.component('hull'))

        if self.filename == None or self.filename == "":
            return

        self.lastPath = os.path.dirname(self.filename)

        if self.filename == None or self.filename == "":
            return        

        lowerFilename = self.filename.lower()

        if not (lowerFilename.endswith('.jpg') or
                lowerFilename.endswith('.png') or
                lowerFilename.endswith('.tif') or
                lowerFilename.endswith('.bmp')):
            filename = self.filename + '.tif'
        else:
            filename = self.filename

        format = filename[-3:]
        filename = filename[:-4]
        base.movie(namePrefix = filename, duration=duration, format=format)
        
    def takeScreenshot(self):
        self.filename = asksaveasfilename(
            initialdir = self.lastPath,
            title = 'Enter name of file...',
            parent = self.component('hull'))

        if self.filename == None or self.filename == "":
            return

        self.lastPath = os.path.dirname(self.filename)

##         self.filename = askstring('Toon Manager Screen Shot', 'Filename:',
##                                   parent = self.component('hull'))
##         if self.filename == None:
##             return

        if self.filename == None or self.filename == "":
            return

        def setText(l,text):
            l['text'] = text
        l = DirectLabel(text = '10', scale = 0.3,
                        text_fg = (1,1,1,1),
                        text_shadow = Vec4(0,0,0,1),
                        relief = None)
        ivalList = []
        for i in range(10,0,-1):
            ivalList.append(Func(setText, l, `i`))
            ivalList.append(Wait(1.0))
        ivalList.append(Func(l.destroy))
        ivalList.append(Func(self._takeScreenshot))
        s = Sequence(*ivalList)
        s.start()

    def _takeScreenshot(self):
        render2d.hide()
        direct.deselectAll()
        base.graphicsEngine.renderFrame()
        #base.screenshot(self.filename)

        lowerFilename = self.filename.lower()

        if not (lowerFilename.endswith('.jpg') or
                lowerFilename.endswith('.png') or
                lowerFilename.endswith('.tif') or
                lowerFilename.endswith('.bmp')):
            filename = self.filename + '.tif'
        else:
            filename = self.filename
        base.screenshot(filename, defaultFilename = 0)
        render2d.show()            
                
    def appendRtmState(self):    
                
        comments = askstring("Comments", "Type your comments", parent = self.component('hull'))        
        
        self.filename = asksaveasfilename(
            initialdir = self.lastPath,
            title = 'Enter name of file...',
            parent = self.component('hull'))            
                        
        self.lastPath = os.path.dirname(self.filename)        
        strList = []   
        strList.append("\nCOMMENTS: ")  
        strList.append(comments)         
        strList.append("\nSPECIES: ")  
        strList.append(self.species.get())   
        strList.append("\nGENDER: ")       
        strList.append(self.gender.get()) 
        strList.append("\nHEAD: ")       
        strList.append(self.head.get()) 
        strList.append("\nTORSO: ")          
        strList.append(self.torso.get())    
        strList.append("\nLEGS: ")     
        strList.append(self.legs.get())  
        strList.append("\nANIM: ")     
        strList.append(str(self.rtm.getState()))
        
        rtmState = "".join(strList)        
        
        if os.path.isfile(self.filename):
            rtmFile = open(self.filename, "r+")    
            rtmFile.seek(0,2)    
            rtmFile.writelines(rtmState)   
        else:
            rtmFile = open(self.filename, "w")
            rtmFile.writelines(rtmState)        
                
        rtmFile.close()           
                
    def showHelp(self):        
        
        showinfo(title='RTM HELP', message = rtmHelp, parent = self.component('hull'))
    
    def setParameterGroup(self, values):
        self.bar1.updateProgress(values[0])
        self.bar2.updateProgress(values[1])
        self.bar3.updateProgress(values[2])
        self.bar4.updateProgress(values[3])

    def setObstacleType(self):
        print 'CHOOSING OBSTACLE DGG.TYPE:', self.obstacleType.get()

    def toggleFun(self):
        if self.getVariable('Obstacle', 'Make Fun?').get():
            print 'THIS IS GOING TO BE FUN!'
        else:
            print 'NOT SO FUN'

    def popupFactoryDialog(self):
        data = askstring('Input Factory Data', 'Factory Data:',
                         parent = self)
        if data:
            self.messageBar().helpmessage(data)

    def toggleGridSnap(self):
        if self._fGridSnap.get():
            print 'Turning on grid!'
        else:
            print 'Turning off grid!'

    def setStomperSize(self, size):
        print 'New Stomper Size:', size       
        


base.rtm = RobotToonManager()
base.rtm.popupControls()
direct.grid.enable()
camera.setPosHpr(0,-60,5,0,0,0)
run()


"""
# TOONS OF THE MONTH
# serverString = '7412010101020302 03000f07000707'
# July
# serverString = '7413000000140100 01050218001818'

# KEEFE AND YOUNG COMMERCIAL
spike = rtm.makeToonFromServerString('0f00741702010103040304020d12001212')
biscuit = rtm.makeToonFromServerString('0f0074030201011c1b131b071008000808')

def RunAction():
    spike.setAnimState('run')
    biscuit.setAnimState('run')

def WalkAction():
    spike.setAnimState('walk')
    biscuit.setAnimState('walk')

tl = Toplevel()
bRun = Button(tl, text = 'Run', command = RunAction)
bRun.pack(expand = 1, fill = X)

bWalk= Button(tl, text = 'Walk', command = WalkAction)
bWalk.pack(expand = 1, fill = X)

"""
