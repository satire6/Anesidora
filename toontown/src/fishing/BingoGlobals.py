#################################################################
# File: BingoGlobals.py
# Purpose: Provides Global Variables for use within all Bingo
#          related files. 
#################################################################

from toontown.toonbase import TTLocalizer

# Card Type Enums
NORMAL_CARD = 0
FOURCORNER_CARD = 1
DIAGONAL_CARD = 2
THREEWAY_CARD = 3
BLOCKOUT_CARD = 4

# A dictionary containing the Card Type ID as a key, with a tuple
# representing different aspects of the card.
# { Key : ( (Color), Base_Reward, Game_Time ) }

         #base color,           button color,         button rollover
Style1 = ((249, 193, 41, 255),  (106, 241, 233, 255), (64, 215, 206, 255) ) #Gold
Style2 = ((138, 241, 106, 255), (246, 129, 220, 255), (221, 113, 197, 255)) #Light Green
Style3 = ((128, 108, 250, 255), (248, 129, 56, 255),  (250, 95, 26, 255)  ) #Purple
Style4 = ((10, 118, 251, 255),  (252, 225, 97, 255),  (245, 207, 29, 255) ) #Blue
Style5 = ((243, 84, 253, 255),  (97, 163, 253, 255),  (48, 129, 240, 255) ) #Light Purple

                                    #color,  reward, time, name,                              help string
CardTypeDict = { NORMAL_CARD :     ( Style1, 10,     140,  TTLocalizer.FishBingoTypeNormal,   TTLocalizer.FishBingoHelpNormal ),
                 FOURCORNER_CARD : ( Style2, 20,     120,  TTLocalizer.FishBingoTypeCorners,  TTLocalizer.FishBingoHelpCorners ),
                 DIAGONAL_CARD :   ( Style3, 40,     180,  TTLocalizer.FishBingoTypeDiagonal, TTLocalizer.FishBingoHelpDiagonals ),
                 THREEWAY_CARD :   ( Style4, 80,     180,  TTLocalizer.FishBingoTypeThreeway, TTLocalizer.FishBingoHelpThreeway ),
                 BLOCKOUT_CARD :   ( Style5, 1000,   90,   TTLocalizer.FishBingoTypeBlockout, TTLocalizer.FishBingoHelpBlockout  ) }

def getGameTime(typeId):
    return CardTypeDict[typeId][2]

def getGameName(typeId):
    return CardTypeDict[typeId][3]

def getJackpot(typeId):
    return CardTypeDict[typeId][1]

def getColor(typeId):
    float_color = map(lambda x: x/255.0, CardTypeDict[typeId][0][0])
    return float_color

def getButtonColor(typeId):
    float_color = map(lambda x: x/255.0, CardTypeDict[typeId][0][1])
    return float_color

def getButtonRolloverColor(typeId):
    float_color = map(lambda x: x/255.0, CardTypeDict[typeId][0][2])
    return float_color

def getHelpString(typeId):
    return CardTypeDict[typeId][4]

#cell colors
CellColorActive =   (1.0, 1.0, 1.0, 1.0)  # a square needed to 'win' a game
CellColorInactive = (0.8, 0.8, 0.8, 1.0)  # a square that is not needed for this game

# Min/Max Number of JBs the super jackpot can
# reach.
ROLLOVER_AMOUNT = 100
MIN_SUPER_JACKPOT = 1000
MAX_SUPER_JACKPOT = 10000

# Win Check Enums
NO_UPDATE = 0
UPDATE = 1
WIN = 2

# Bingo Time Constants
CARD_ROWS = 5
CARD_COLS = 5
CARD_SIZE = 25

# Time Between each state Change
INTRO_SESSION = 5.0
TIMEOUT_SESSION = 15.0
REWARD_TIMEOUT = 5.0
CLOSE_EVENT_TIMEOUT = 5.0

HOUR_BREAK_SESSION = 300
HOUR_BREAK_MIN = 55

NORMAL_GAME = 0
INTERMISSION = 1
CLOSE_EVENT = 2

# Default size of the Card Image. Height is 0.05 greater than width
#CardImageScale = (0.55, 1.0, 0.6)
CardImageScale = (0.035, 0.035, 0.035)

# Default position of the Card upon the screen. This
# is dependent to the size of the card image scale because
# the card is placed at the top of the screen.
#CardPosition = (0.0, 1.0, 1.0-CardImageScale[2]*0.5)
#CardPosition = (0.75, 1.0, -.95+CardImageScale[2]*0.5)
CardPosition = (0.75, 1.0, -.65)
#CardPosition = (-0.75, 1.0, -.95+CardImageScale[2]*0.5)

TutorialPosition = (0.2, 1.0, -0.76)
TutorialScale = 0.6 #(0.5, 0.5, 0.15)
TutorialTextScale = (0.07, 0.233)
# Cell Defaults Image Values. These ensure that no matter
# what value the CardImageScale takes, the card GUI will
# scale accordinly!
CellImageScale = 0.088
GridXOffset = -0.052

FishButtonDict = {
    # (buttonName)
    -1: ("mickeyButton", ),
     0: ("BaloonFishButton", ),
     2: ("CatfishButton", ),
     4: ("ClownfishButton", ),
     6: ("FrozenfishButton", ),
     8: ("starfishButton", ),
    10: ("holyMackrelButton", ),
    12: ("DogfishButton", ),
    14: ("amoreEelButton", ),
    16: ("nursesharkButton", ),
    18: ("kingcrabButton", ),
    20: ("moonfishButton", ),
    22: ("pPlane21", ),
    24: ("poolsharkButton", ),
    26: ("BearacudaButton", ),
    28: ("troutButton", ),
    30: ("pianotunaButton", ),
    32: ("PBJfishButton", ),
    34: ("DevilrayButton", ),
    }

#tutorial type enum
TutorialIntro = 1
TutorialMark = 2
TutorialCard = 3
TutorialBingo = 4



