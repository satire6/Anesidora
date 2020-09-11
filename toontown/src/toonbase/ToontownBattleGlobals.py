from ToontownGlobals import *
import math
import TTLocalizer

### ToontownBattle globals: central repository for all battle globals

# defaults for camera

BattleCamFaceOffFov = 30.0
BattleCamFaceOffPos = Point3(0, -10, 4)

# BattleCamDefaultPos = Point3(0, -10, 11)
# BattleCamDefaultHpr = Vec3(0, -45, 0)
BattleCamDefaultPos = Point3(0, -8.6, 16.5)
BattleCamDefaultHpr = Vec3(0, -61, 0)
BattleCamDefaultFov = 80.0
BattleCamMenuFov = 65.0
BattleCamJoinPos = Point3(0, -12, 13)
BattleCamJoinHpr = Vec3(0, -45, 0)

# This might be set true by a magic word to skip over the playback movie.
SkipMovie = 0

# avatar start hp
BaseHp = 15

# avatar track names and numbers
Tracks = TTLocalizer.BattleGlobalTracks
NPCTracks = TTLocalizer.BattleGlobalNPCTracks

TrackColors = ((211/255.0, 148/255.0, 255/255.0),
               (249/255.0, 255/255.0, 93/255.0),
               (79/255.0, 190/255.0, 76/255.0),
               (93/255.0, 108/255.0, 239/255.0),
               (255/255.0, 145/255.0, 66/255.0),
               (255/255.0, 65/255.0, 199/255.0),
               (67/255.0, 243/255.0, 255/255.0),
               )

# TODO: put want-all-props back in with quest system
#try:
#    wantAllProps = base.config.GetBool('want-all-props', 0)
#except:
#    wantAllProps = simbase.config.GetBool('want-all-props', 0)
#if (wantAllProps == 1):
#    for i in range(len(TrackZones)):
#        TrackZones[i] = ToontownCentral

HEAL_TRACK = 0
TRAP_TRACK = 1
LURE_TRACK = 2
SOUND_TRACK = 3
THROW_TRACK = 4
SQUIRT_TRACK = 5
DROP_TRACK = 6
# Special NPC Toon actions
NPC_RESTOCK_GAGS = 7
NPC_TOONS_HIT = 8
NPC_COGS_MISS = 9

MIN_TRACK_INDEX = 0
MAX_TRACK_INDEX = 6

MIN_LEVEL_INDEX = 0
MAX_LEVEL_INDEX = 6

MAX_UNPAID_LEVEL_INDEX = 4

LAST_REGULAR_GAG_LEVEL = 5

UBER_GAG_LEVEL_INDEX = 6

NUM_GAG_TRACKS = 7

# which props buffs which track
PropTypeToTrackBonus = {
    AnimPropTypes.Hydrant: SQUIRT_TRACK,
    AnimPropTypes.Mailbox : THROW_TRACK,
    AnimPropTypes.Trashcan : HEAL_TRACK,
    }


# avatar skill levels (totalled)
#Levels = [0, 10, 50, 140, 300, 550]
#Levels = [0, 10, 50, 250, 750, 2000]
Levels = [[0, 20, 200, 800, 2000, 6000, 10000], # heal
          [0, 20, 100, 800, 2000, 6000, 10000], # trap
          [0, 20, 100, 800, 2000, 6000, 10000], # lure
          [0, 40, 200, 1000, 2500, 7500, 10000], # sound
          [0, 10, 50, 400, 2000, 6000, 10000], # throw
          [0, 10, 50, 400, 2000, 6000, 10000], # squirt
          [0, 20, 100, 500, 2000, 6000, 10000], # drop
          ]
#MaxSkill = 5000
regMaxSkill = 10000
UberSkill = 500
MaxSkill = UberSkill + regMaxSkill
UnpaidMaxSkill = 1999
# This is the maximum amount of experience per track that may be
# earned in one battle (or in one building).
ExperienceCap = 200

# This accuracy (a percentage) is the highest that can ever be attained.
MaxToonAcc = 95

# avatar starting skill level
StartingLevel = 0

CarryLimits = (
    # Heal
    ( ( 10,  0,  0,  0, 0, 0, 0),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1) ), # lvl 7
    # Trap
    ( (  5,  0,  0,  0, 0, 0, 0),   # lvl 1
      (  7,  3,  0,  0, 0, 0, 0),   # lvl 2
      ( 10,  7,  3,  0, 0, 0, 0),   # lvl 3
      ( 15, 10,  7,  3, 0, 0, 0),   # lvl 4
      ( 15, 15, 10,  5, 3, 0, 0),   # lvl 5
      ( 20, 15, 15, 10, 5, 2, 0),   # lvl 6
      ( 20, 15, 15, 10, 5, 2, 1) ),  # lvl 7
    # Lure
    ( ( 10,  0,  0,  0, 0, 0, 0),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1) ), # lvl 7
    # Sound
    ( ( 10,  0,  0,  0, 0, 0, 0),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1) ), # lvl 7
    # Throw
    ( ( 10,  0,  0,  0, 0, 0, 0),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1) ), # lvl 7
    # Squirt
    ( ( 10,  0,  0,  0, 0, 0, 0 ),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0 ),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0 ),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0 ),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0 ),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0 ),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1 ) ), # lvl 7
    # Drop
    ( ( 10,  0,  0,  0, 0, 0, 0),  # lvl 1
      ( 10,  5,  0,  0, 0, 0, 0),  # lvl 2
      ( 15, 10,  5,  0, 0, 0, 0),  # lvl 3
      ( 20, 15, 10,  5, 0, 0, 0),  # lvl 4
      ( 25, 20, 15, 10, 3, 0, 0),  # lvl 5
      ( 30, 25, 20, 15, 7, 3, 0),  # lvl 6
      ( 30, 25, 20, 15, 7, 3, 1) ), # lvl 7
    )

# avatar prop maxes
MaxProps = ( (15, 40), (30, 60), (75, 80) )

# death-list flag masks for BattleExperience
DLF_SKELECOG   = 0x01
DLF_FOREMAN    = 0x02
DLF_VP         = 0x04
DLF_CFO        = 0x08
DLF_SUPERVISOR = 0x10
DLF_VIRTUAL    = 0x20
DLF_REVIVES    = 0x40

# Pie names.  These map to props in BattleProps, but it must be
# defined here beccause BattleProps cannot be included on the AI.
pieNames = ['tart',
            'fruitpie-slice',
            'creampie-slice',
            'fruitpie',
            'creampie',
            'birthday-cake',
            'wedding-cake',
            'lawbook', #used in battle three of lawbot boss
            ]

# avatar prop icon filenames
AvProps = ( ('feather', 'bullhorn', 'lipstick', 'bamboocane', 'pixiedust',
           'baton', 'baton'),
          ('banana', 'rake', 'marbles', 'quicksand', 'trapdoor', 'tnt', 'traintrack'),
          ('1dollar', 'smmagnet', '5dollar', 'bigmagnet', '10dollar',
           'hypnogogs', 'hypnogogs'),
          ('bikehorn', 'whistle', 'bugle', 'aoogah', 'elephant', 'foghorn', 'singing'),
          ('cupcake', 'fruitpieslice', 'creampieslice', 'fruitpie', 'creampie',
           'cake', 'cake'),
          ('flower', 'waterglass', 'waterballoon', 'bottle', 'firehose',
           'stormcloud', 'stormcloud'),
          ('flowerpot', 'sandbag', 'anvil', 'weight', 'safe', 'piano', 'piano')
          ) 

AvPropsNew = ( ('inventory_feather', 'inventory_megaphone', 'inventory_lipstick', 'inventory_bamboo_cane', 'inventory_pixiedust',
           'inventory_juggling_cubes',  'inventory_ladder'),
          ('inventory_bannana_peel', 'inventory_rake', 'inventory_marbles', 'inventory_quicksand_icon', 'inventory_trapdoor',
           'inventory_tnt',  'inventory_traintracks'),
          ('inventory_1dollarbill', 'inventory_small_magnet', 'inventory_5dollarbill', 'inventory_big_magnet',
           'inventory_10dollarbill', 'inventory_hypno_goggles',  'inventory_screen'),
          ('inventory_bikehorn', 'inventory_whistle', 'inventory_bugle', 'inventory_aoogah', 'inventory_elephant', 'inventory_fog_horn', 'inventory_opera_singer'),
          ('inventory_tart', 'inventory_fruit_pie_slice', 'inventory_cream_pie_slice', 'inventory_fruitpie',
           'inventory_creampie', 'inventory_cake', 'inventory_wedding'),
          ('inventory_squirt_flower', 'inventory_glass_of_water', 'inventory_water_gun', 'inventory_seltzer_bottle',
           'inventory_firehose', 'inventory_storm_cloud',  'inventory_geyser'),
          ('inventory_flower_pot', 'inventory_sandbag', 'inventory_anvil', 'inventory_weight', 'inventory_safe_box', 'inventory_piano', 'inventory_ship')
          ) 


# prettier on-screen versions of the prop names
AvPropStrings = TTLocalizer.BattleGlobalAvPropStrings

# prettier on-screen versions of the prop names for singular usage
AvPropStringsSingular = TTLocalizer.BattleGlobalAvPropStringsSingular

# prettier on-screen versions of the prop names for plural usage
AvPropStringsPlural = TTLocalizer.BattleGlobalAvPropStringsPlural

# avatar prop accuracies
AvPropAccuracy = ((70, 70, 70, 70, 70, 70, 100), # Heal
                  (0, 0, 0, 0, 0, 0, 0),       # Trap (always hits)
                  (50, 50, 60, 60, 70, 70, 90), # Lure
                  (95, 95, 95, 95, 95, 95, 95), # Sound
                  (75, 75, 75, 75, 75, 75, 75), # Throw
                  (95, 95, 95, 95, 95, 95, 95), # Squirt
                  (50, 50, 50, 50, 50, 50, 50)  # Drop
                  )
AvLureBonusAccuracy = (60, 60, 70, 70, 80, 80, 100)

AvTrackAccStrings = TTLocalizer.BattleGlobalAvTrackAccStrings

# avatar prop damages
# each entry represents a toon prop track and is a list of pairs,
# the first of each pair represents the damage range (min to max) which
# maps to the second pair which represents the toon's track
# exp.  So the higher the toon's exp in that prop's track, the more damage
# that particular prop can do
#
AvPropDamage = (
    # Heal
    (((8,10),(Levels[0][0], Levels[0][1])),#tickle
     ((15,18),(Levels[0][1], Levels[0][2])),#group Joke
     ((25,30),(Levels[0][2], Levels[0][3])),#kiss
     ((40,45),(Levels[0][3], Levels[0][4])),#group Dance
     ((60,70),(Levels[0][4], Levels[0][5])),#dust
     ((90,120),(Levels[0][5], Levels[0][6])),#group Juggle
     ((210,210),(Levels[0][6], MaxSkill))),#group Dive
    # Trap
    (((10, 12),(Levels[1][0], Levels[1][1])),
     ((18, 20),(Levels[1][1], Levels[1][2])),
     ((30, 35),(Levels[1][2], Levels[1][3])),
     ((45, 50),(Levels[1][3], Levels[1][4])),
     ((60, 70),(Levels[1][4], Levels[1][5])),
     ((90, 180),(Levels[1][5], Levels[1][6])),
     ((195, 195),(Levels[1][6], MaxSkill))),
    # Lure
    (((0,0),(0,0)),
     ((0,0),(0,0)),
     ((0,0),(0,0)),
     ((0,0),(0,0)),
     ((0,0),(0,0)),
     ((0,0),(0,0)),
     ((0,0),(0,0))),
    # Sound
    (((3, 4), (Levels[3][0], Levels[3][1])),
     ((5, 7), (Levels[3][1], Levels[3][2])),
     ((9, 11), (Levels[3][2], Levels[3][3])),
     ((14, 16), (Levels[3][3], Levels[3][4])),
     ((19, 21), (Levels[3][4], Levels[3][5])),
     ((25, 50), (Levels[3][5], Levels[3][6])),
     ((90, 90), (Levels[3][6], MaxSkill))),
    # Throw
    (((4, 6), (Levels[4][0], Levels[4][1])),
     ((8, 10), (Levels[4][1], Levels[4][2])),
     ((14, 17), (Levels[4][2], Levels[4][3])),
     ((24, 27), (Levels[4][3], Levels[4][4])),
     ((36, 40), (Levels[4][4], Levels[4][5])),
     ((48, 100), (Levels[4][5], Levels[4][6])),
     ((120, 120), (Levels[4][6], MaxSkill))),
    # Squirt
    (((3, 4), (Levels[5][0], Levels[5][1])),
     ((6, 8), (Levels[5][1], Levels[5][2])),
     ((10, 12), (Levels[5][2], Levels[5][3])),
     ((18, 21), (Levels[5][3], Levels[5][4])),
     ((27, 30), (Levels[5][4], Levels[5][5])),
     ((36, 80), (Levels[5][5], Levels[5][6])),
     ((105, 105), (Levels[5][6], MaxSkill))),
    # Drop
    (((10, 10), (Levels[6][0], Levels[6][1])),
     ((18, 18), (Levels[6][1], Levels[6][2])),
     ((30, 30), (Levels[6][2], Levels[6][3])),
     ((45, 45), (Levels[6][3], Levels[6][4])),
     ((60, 60), (Levels[6][4], Levels[6][5])),
     ((85, 170), (Levels[6][5], Levels[6][6])),
     ((180, 180), (Levels[6][6], MaxSkill))),
    )

# avatar prop target type (0 for single target,
# 1 for group target)
# AvPropTargetCat is a grouping of target types
# for a single track and AvPropTarget is which
# target type group from AvPropTargetCat each
# toon attack track uses
#
ATK_SINGLE_TARGET = 0
ATK_GROUP_TARGET  = 1
AvPropTargetCat = ( ( ATK_SINGLE_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET ),
                    ( ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET ),
                    ( ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET,
                      ATK_GROUP_TARGET ),
                    ( ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_SINGLE_TARGET,
                      ATK_GROUP_TARGET ),                    
                    ) 

AvPropTarget = ( 0, 3, 0, 2, 3, 3, 3)


def getAvPropDamage( attackTrack, attackLevel, exp, organicBonus=False, propBonus = False,
                     propAndOrganicBonusStack = False):
    """
    ////////////////////////////////////////////////////////////////////
    // Function:   get the appropriate prop damage based on various
    //             attributes of the prop and the toon
    // Parameters: attackTrack, the track of the prop
    //             attackLevel, the level of the prop
    //             exp, the toon's exp in the specified track
    // Changes:
    ////////////////////////////////////////////////////////////////////
    """
    # Map a damage value for the prop based on the track exp of the
    # toon, for example, a throw might have 3-6 damage which maps
    # to 0-30 exp.  So at 0 to 7.75 exp, the throw will do 3 damage;
    # at 7.75 to 15.5 exp, the throw will do 4 damage; at 15.5 to 23.25,
    # the throw will do 5 damage; at 23.25 to 30 exp, the throw will
    # do 6 damage;  at more than 30 exp, the throw will max out at 6
    # damage
    #
    minD = AvPropDamage[ attackTrack ][ attackLevel ][0][0]
    maxD = AvPropDamage[ attackTrack ][ attackLevel ][0][1]
    minE = AvPropDamage[ attackTrack ][ attackLevel ][1][0]
    maxE = AvPropDamage[ attackTrack ][ attackLevel ][1][1]
    expVal = min( exp, maxE )
    expPerHp = float((maxE-minE)+1) / float((maxD-minD)+1)
    damage = math.floor( ( expVal - minE ) / expPerHp ) + minD
    # In the gag purchase tutorial the sneak peak gags show as negative
    if damage <= 0:
        damage = minD
    if propAndOrganicBonusStack:
        originalDamage = damage
        if organicBonus:
            damage += getDamageBonus(originalDamage)
        if propBonus:
            damage += getDamageBonus(originalDamage)
    else:
        if organicBonus or propBonus:
            damage += getDamageBonus(damage)
    return damage

def getDamageBonus(normal):
    bonus = int(normal * 0.1)
    if (bonus < 1) and (normal > 0):
        bonus = 1
    return bonus

#def isGroup(track, level):
#    if ((track == SOUND_TRACK) or
#        (((track == HEAL_TRACK) or (track == LURE_TRACK)) and
#         ((level == 1) or (level == 3) or (level == 5) or (level == 6)))):
#        return 1
#    else:
#        return 0
        
def isGroup(track, level):
    return AvPropTargetCat[AvPropTarget[track]][level]
    
def getCreditMultiplier(floorIndex):
    """
    Returns the skill credit multiplier appropriate for a particular
    floor in a building battle.  The floorIndex is 0 for the first
    floor, up through 4 for the top floor of a five-story building.
    """
    # Currently, this is 1 for the first floor (floor 0), 1.5 for the
    # second floor (floor 1), etc.
    return 1 + floorIndex * 0.5         

def getFactoryCreditMultiplier(factoryId):
    """
    Returns the skill credit multiplier for a particular factory.
    factoryId is the factory-interior zone defined in ToontownGlobals.py.
    """
    # for now, there's only one factory
    return 2.

def getFactoryMeritMultiplier(factoryId):
    """
    Returns the skill merit multiplier for a particular factory.
    factoryId is the factory-interior zone defined in ToontownGlobals.py.
    """
    # Many people complained about how many runs you must make now that 
    # we lowered the cog levels so I have upped this by a factor of two.
    return 4.

def getMintCreditMultiplier(mintId):
    """
    Returns the skill credit multiplier for a particular mint.
    mintId is the mint-interior zone defined in ToontownGlobals.py.
    """
    return {
        CashbotMintIntA : 2.,
        CashbotMintIntB : 2.5,
        CashbotMintIntC : 3.,
        }.get(mintId, 1.)
         
def getStageCreditMultiplier(floor):
    """
    Returns the skill credit multiplier for a particular mint.
    stageId is the stage-interior zone defined in ToontownGlobals.py.
    """
    return getCreditMultiplier(floor)

def getCountryClubCreditMultiplier(countryClubId):
    """
    Returns the skill credit multiplier for a particular mint.
    mintId is the mint-interior zone defined in ToontownGlobals.py.
    """
    return {
        BossbotCountryClubIntA : 2.,
        BossbotCountryClubIntB : 2.5,
        BossbotCountryClubIntC : 3.,
        }.get(countryClubId, 1.)


def getBossBattleCreditMultiplier(battleNumber):
    """
    Returns the skill credit multiplier for the two first battles of
    the final battle sequence with the Senior V.P.  battleNumber is 1
    for the first battle and 2 for the second battle.
    """
    return 1 + battleNumber

def getInvasionMultiplier():
    """
    Returns the skill credit multiplier during invasions.
    This gets multiplied on every street battle and in every interior.
    User must first check to see if there is an invasion.
    """
    return 2.0

def getMoreXpHolidayMultiplier():
    """
    Returns the skill credit multiplier during the more xp holiday.
    This gets multiplied on every street battle and in every interior.
    User must first check to see if there is an invasion.
    """
    return 2.0
    
def encodeUber(trackList):
    bitField = 0
    for trackIndex in range(len(trackList)):
        if trackList[trackIndex] > 0:
            bitField += pow(2,trackIndex)
    return bitField

def decodeUber(flagMask):
    if flagMask == 0:
        return []
    maxPower = 16
    workNumber = flagMask
    workPower = maxPower
    trackList = []
    #print("build")
    #while (workNumber > 0) and (workPower >= 0):
    while (workPower >= 0):
        if workNumber >= pow(2,workPower):
            workNumber -= pow(2,workPower)
            trackList.insert(0, 1) 
        else:
            trackList.insert(0, 0)
        #print("Number %s List %s" % (workNumber, trackList))
        workPower -= 1
    endList = len(trackList)
    foundOne = 0
    #print("compress")
    while not foundOne:
        #print trackList
        if trackList[endList - 1] == 0:
            trackList.pop(endList - 1)
            endList -= 1
        else:
            foundOne = 1
    return trackList
    
def getUberFlag(flagMask, index):
    decode = decodeUber(flagMask)
    if index >= len(decode):
        return 0
    else:
        return decode[index]
        
def getUberFlagSafe(flagMask, index):
    if (flagMask == "unknown") or (flagMask < 0):
        return -1
    else:
        return getUberFlag(flagMask, index)
