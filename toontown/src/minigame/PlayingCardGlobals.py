# RAU modified from pirates
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from pandac.PandaModules import Vec4
# For dealing
Up = 1
Down = 0

# This is toontown, so we may have a different rank, and number of suits for our games
MaxRank = 13
MaxSuit = 4

# Card values
# 00 - 12 = HEARTS  2,3,4...q,k,a
# 13 - 25 = DIAMONDS  2,3,4...q,k,a
# 26 - 38 = CLUBS  2,3,4...q,k,a
# 39 - 51 = SPADES  2,3,4...q,k,a
# 255 is face down/unknown

# Suits
Hearts = 0
Diamonds = 1
Clubs = 2
Spades = 3

Suits = [Hearts, Diamonds, Clubs, Spades]


Unknown = 255

UpColor = Vec4(1,1,1,1)
RolloverColor = Vec4(1,1,0.5,1)
DownColor = Vec4(1,0.9,0.9,1)
DisabledColor = Vec4(1,1,1,0.5)

CardColors = (UpColor, DownColor, RolloverColor, DisabledColor)

def getCardName(value):
    if value == Unknown:
        return TTLocalizer.PlayingCardUnknown
    else:
        rank = value % MaxRank
        suit = value / MaxRank
        return TTLocalizer.getPlayingCardName(suit, rank)

Styles = ['standard']
# Style -> Suit -> Rank -> image nodePath dict
CardImages = {}
_cardImagesInitialized = 0
_modelPathBase = "phase_3.5/models/gui/inventory_icons"

def convertValueToGagTrackAndLevel(value):
    # for a stand deck, converts 0 to 51 to a gag
    assert rank < (ToontownBattleGlobals.MAX_TRACK_INDEX +1) *\
           (ToontownBattleGlobals.MAX_LEVEL_INDEX +1) * MaxSuit
    imageNum = int( rank / MaxSuit)
    track = imageNum  % (ToontownBattleGlobals.MAX_TRACK_INDEX +1)
    level = imageNum / (ToontownBattleGlobals.MAX_TRACK_INDEX+1)
    return track,level

def convertRankToGagTrackAndLevel(rank):
    # for a stand deck, converts 0 to 12 to a gag    
    assert rank < (ToontownBattleGlobals.MAX_TRACK_INDEX +1) *\
           (ToontownBattleGlobals.MAX_LEVEL_INDEX +1)
    track = rank  %( ToontownBattleGlobals.MAX_TRACK_INDEX +1)
    level = rank / (ToontownBattleGlobals.MAX_TRACK_INDEX + 1)
    return track,level

def initCardImages():
    suitCodes = ('h', 'd', 'c', 's')
    rankCodes = ('02', '03', '04', '05', '06','07', '08', '09', '10',
                 '11', '12', '13', '01')

    for style in Styles:
        modelPath = _modelPathBase
        cardModel = loader.loadModel(modelPath)
        cardModel.hide()
        CardImages[style] = {}
        for suitIndex in range(MaxSuit):
            CardImages[style][suitIndex] = {}
            for rankIndex in range(MaxRank):
                track,level = convertRankToGagTrackAndLevel(rankIndex)
                propName = ToontownBattleGlobals.AvPropsNew[track][level]
                cardNode = cardModel.find('**/%s' % propName)
                assert not cardNode.isEmpty()
                CardImages[style][suitIndex][rankIndex] = cardNode
                
        # Card back for this style
        propName = ToontownBattleGlobals.AvPropsNew[ToontownBattleGlobals.MAX_TRACK_INDEX][ToontownBattleGlobals.MAX_LEVEL_INDEX]
        CardImages[style]['back'] = cardModel.find(propName)
        
    global _cardImagesInitialized
    _cardImagesInitialized = 1

def getImage(style, suit, rank):    
    if _cardImagesInitialized == 0:
        initCardImages()
    return CardImages[style][suit][rank]

def getBack(style):
    if _cardImagesInitialized == 0:
        initCardImages()
    return CardImages[style]['back']

