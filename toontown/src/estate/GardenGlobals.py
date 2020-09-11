from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
import random

# Each plant will have a growthLevel.
# This growthLevel will never decrease, unless going from fruiting to full grown.
# Each plant will have a curWaterLevel.
# When each epoch triggers, the curWaterLevel is decremented. If it started
# positive then the growthLevel of the plant will increase by 1. If it started
# at zero or negative, the plant now becomes wilted.

# An explanation of growth thresholds:
#
# Each tree starts with 0 growthLevel.
# Each epoch (currently 24 hours), it gains 1 growthLevel if it has water.
# The 3 numbers listed shows the progression from seedling to established,
# established to full grown, full grown to fruiting.
# A value of (7,14,21) means on the 7th epoch it will switch to the established
# model, on the 14th epoch it will switch to the full grown model
# on the 21st epoch it will bear fruit.
# A value of (1,1,2) means when the 1st epoch triggers, it will skip the
# established model and switch to full grown.  On the 2nd epoch, it will
# bear fruit.
# A value of (1,1,1) means when the 1st epoch triggers, it will skip the
# established model and switch to full grown. and it's immediately pickable.
# A value of (1,3,2) is illegal.

# maxWaterLevel:  this value is in epochs
#
# A value of 4 for example, means it can store 4 epochs worth of water
# A value of 1 means it's a finicky plant and needs watering every epoch

# minWaterLevel: this value is in epochs
#
# Each epoch, we decrement the current water level of the plant, and we
# don't go below this value.
# A value of -1 means it takes only 1 epoch to switch from wilted to healthy.
# A value of -4 (assuming it was neglected for 4 epochs), it will take 4
# epochs of watering for it to switch from wilted to healthy.

# The varieties array applies only to flowers and statuaries.
#
# The 1st number is the recipe index.
# The 2nd number is the color index of the object, look it up in FlowerColors.
# The 3rd number is how much the flower sells for
#
# If you add new varieties, add it at the end. Don't change the order.
#
# The pinballScore is used by statuary to override the default pinball score
# in ToontownGlobals
#
# worldScale if defined, is the scale we use when displaying in the 3d world
#
# photoPos, photoScale, photoHeading and photoPitch, if defined affect how it looks in FlowerPhoto.py
#

# How many unique flowers we need to get the next flower laff bonus
FLOWERS_PER_BONUS = 10

# do we use the garden accelerator from the shtiker book, or do we plant it?
ACCELERATOR_USED_FROM_SHTIKER_BOOK = True

# Collection enums
COLLECT_NO_UPDATE = 0
COLLECT_NEW_ENTRY = 1

gardenNotify = DirectNotifyGlobal.directNotify.newCategory("GardenGlobals")

# These codes indicate the category of item we might have pulled out,
# or the reason we failed to pull anything out.
FlowerItem = 2
FlowerItemNewEntry = 9

#kinds of items that can be planted
INVALID_TYPE = -1
GAG_TREE_TYPE = 0
FLOWER_TYPE = 1
STATUARY_TYPE = 2
##STATUARY_TOON_TYPE = 3


WATERING_CAN_SMALL = 0
WATERING_CAN_MEDIUM = 1
WATERING_CAN_LARGE= 2
WATERING_CAN_HUGE = 3
MAX_WATERING_CANS = 4

# Skill pts indicates how much skill pts you need to graduate
# to the next level shovel.
# For the highest shovel it will represent the maximum,
WateringCanAttributes = {
    0 : {
          'numBoxes' : 2,
          'skillPts' : 100,
          'name' : TTLocalizer.WateringCanSmall,
          },
    1 : {
          'numBoxes' : 2,
          'skillPts' : 200,
          'name' : TTLocalizer.WateringCanMedium,
          },
    2 : {
          'numBoxes' : 2,
          'skillPts' : 400,
          'name' : TTLocalizer.WateringCanLarge,
          },
    3 : {
          'numBoxes' : 2,
          'skillPts' : 1000,
          'name' : TTLocalizer.WateringCanHuge,
          },
    }


def getWateringCanPower(wateringCan , wateringCanSkill):
    """
    based on his shovel and his current shovel skill,
    how many jelly beans can we use
    """
    assert wateringCan < MAX_WATERING_CANS
    numBoxes = 0
    for curWateringCan in range(wateringCan + 1):
        wateringCanAttrib = WateringCanAttributes[curWateringCan]
        curBoxes = wateringCanAttrib['numBoxes']
        skill = wateringCanAttrib['skillPts']
        if (wateringCanSkill >= skill):
            if curWateringCan == wateringCan:
                gardenNotify.warning("this shouldn't happen wateringCanSkill %d >= skill %d" % (wateringCanSkill, skill))
            wateringCanSkill = skill -1

        if curWateringCan == wateringCan:
            skillPtPerBox = skill / curBoxes
            numBoxes += 1 + ( int(wateringCanSkill) / int(skillPtPerBox))
        else:
            numBoxes += curBoxes
    return numBoxes

def getMaxWateringCanPower():
    retval = 0
    for wateringCanAttrib in WateringCanAttributes.values():
        retval += wateringCanAttrib['numBoxes']
    return retval

# we could probably increase this
FlowerColors = [
    (0.804, 0.2, 0.2), # red
    (0.922, 0.463, 0.0),   # orange
    (0.5, 0.2, 1.0), # violet
    (0.4, 0.4, 1.0),       # blue
    (0.953, 0.545, 0.757), # pink
    (.992, .843, .392),    # yellow
    (1.0, 1.0, 1.0),    # pure white
    (0.5,0.8,0.5), # green
    ]
FLOWER_RED = 0
FLOWER_ORANGE = 1
FLOWER_VIOLET = 2
FLOWER_BLUE = 3
FLOWER_PINK = 4
FLOWER_YELLOW = 5
FLOWER_WHITE = 6
FLOWER_GREEN = 7

ToonStatuaryTypeIndices = xrange(205,209) #  205,206,206,207,208
ChangingStatuaryTypeIndices = xrange(230,231) # just 230

PlantAttributes = {
    #### Gag trees ####
    # These are now generated programmatically... they use slots 0 - 48

    ###### Flowers ######

    #   Daisy
    49 : { 'name': TTLocalizer.FlowerSpeciesNames[49], #Daisy
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/daisy.bam",
           'fullGrownModel' : "phase_5.5/models/estate/daisy.bam",
           'photoPos' : (0.0, -0.35, -0.361882),
           'photoScale' : 1,
           'photoHeading' : 0,
           'photoPitch' : 35,
           'varieties' : ( (10,FLOWER_YELLOW,1),
                           (11,FLOWER_PINK,2),
                           (12,FLOWER_WHITE,3),
                           (13,FLOWER_RED,4),
                           (14,FLOWER_ORANGE,5),
                           (15,FLOWER_BLUE,6),
                           (16,FLOWER_GREEN,7),
                           (17,FLOWER_VIOLET,8),
                           ),
        },
    #   Tulip
    50 : { 'name': TTLocalizer.FlowerSpeciesNames[50], #Tulip
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/tulip.bam",
           'fullGrownModel' : "phase_5.5/models/estate/tulip.bam",
           'photoPos' : (0.0, -0.35, -0.35),
           'photoScale' : 1,
           'photoHeading' : 0,
           'photoPitch' : 35,
           'varieties' : ( (20,FLOWER_VIOLET,5),
                           (21,FLOWER_RED,6),
                           (22,FLOWER_YELLOW,8),
                           )
        },
    #  Carnation
    51 : { 'name': TTLocalizer.FlowerSpeciesNames[51],
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/carnation.bam",
           'fullGrownModel' : "phase_5.5/models/estate/carnation.bam",
           'photoPos' : (0.0, -0.35, -0.4),
           'photoScale' : 1,
           'photoHeading' : 0,
           'photoPitch' : 35,
           'varieties' : ( (30,FLOWER_PINK,1),
                           (31,FLOWER_YELLOW,2),
                           (32,FLOWER_RED,3),
                           (33,FLOWER_WHITE,5),
                           (34,FLOWER_GREEN,7),
                           )
           },
    #  Lily
    52 : { 'name': TTLocalizer.FlowerSpeciesNames[52],
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/lily.bam",
           'fullGrownModel' : "phase_5.5/models/estate/lily.bam",
           'photoPos' : (0.0174745, -0.05, -0.670513),
           'photoScale' : 1,
           'photoHeading' : 0,
           'photoPitch' : 35,
           'varieties' : ( (40,FLOWER_WHITE,1),
                           (41,FLOWER_GREEN,2),
                           (42,FLOWER_ORANGE,3),
                           (43,FLOWER_PINK,4),
                           (44,FLOWER_RED,5),
                           (45,FLOWER_VIOLET,6),
                           (46,FLOWER_BLUE,7),
                           (47,FLOWER_YELLOW,8),
                           )
           },
    #  Dafodil
    53 : { 'name': TTLocalizer.FlowerSpeciesNames[53],
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/narcissi.bam",
           'fullGrownModel' : "phase_5.5/models/estate/narcissi.bam",
           'photoPos' : (-0.0403175, 0.060933, -0.548368),
           'photoScale' : 1,
           'photoHeading' : 20,
           'photoPitch' : 0,
           'varieties' : ( (50,FLOWER_GREEN,1),
                           (51,FLOWER_WHITE,2),
                           (52,FLOWER_YELLOW,4),
                           (53,FLOWER_PINK,5),
                           )
           },
    #  Pansy
    54 : { 'name': TTLocalizer.FlowerSpeciesNames[54],
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/pansy.bam",
           'fullGrownModel' : "phase_5.5/models/estate/pansy.bam",
           'photoScale' : 2.5,
           'photoHeading' : 0,
           'photoPitch' : 0,
           'varieties' : ( (60,FLOWER_ORANGE,1),
                           (61,FLOWER_WHITE,2),
                           (62,FLOWER_RED,3),
                           (63,FLOWER_YELLOW,4),
                           (64,FLOWER_PINK,6),
                           )

           },

    #  Petunia
    55 : { 'name': TTLocalizer.FlowerSpeciesNames[55],
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -2,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/petunia.bam",
           'fullGrownModel' : "phase_5.5/models/estate/petunia.bam",
           'photoPos' : (0.02, -0.0324585, -0.167735),
           'photoScale' : 1.5,
           'photoHeading' : -20,
           'photoPitch' : 35,
           'varieties' : ( (70,FLOWER_BLUE,7),
                           (71,FLOWER_PINK,8),
                           )

           },
    #    Rose
    56 : { 'name': TTLocalizer.FlowerSpeciesNames[56], #Rose
           'plantType' : FLOWER_TYPE,
           'growthThresholds' : (1,1,1),
           'maxWaterLevel' : getMaxWateringCanPower(),
           'minWaterLevel' : -1,
           'seedlingModel' : "phase_5.5/models/estate/seedling.bam",
           'establishedModel' : "phase_5.5/models/estate/rose.bam",
           'fullGrownModel' : "phase_5.5/models/estate/rose.bam",
           'photoPos' : (0.04396, 0.124797, -0.877291),
           'photoScale' : 1,
           'photoHeading' : 0,
           'photoPitch' : 35,
           'varieties' : ( (0,FLOWER_RED,3),
                           (1,FLOWER_YELLOW,4),
                           (2,FLOWER_PINK,6),
                           (3,FLOWER_WHITE,7),
                           (4,FLOWER_BLUE,8),
                           )
        },
    ###### Statuaries ######
    200 :{ 'name': TTLocalizer.StatuaryDonald,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_donald.bam",
           'worldScale' : 0.05,
           'varieties' : ( (1000,1,0),),
           'pinballScore' : (10,1)
           },
    201 :{ 'name': TTLocalizer.StatuaryMickey1,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_mickey_flute",
           'worldScale' : 0.05,
           'varieties' : ( (1001,1,0),),
           'pinballScore' : (50,1)
           },
    #this item shows up in the planting gui but is not planted in the world
    202 :{ 'name': TTLocalizer.StatuaryGardenAccelerator,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_4/models/props/goofy_statue",
           'varieties' : ( (1002,1,0),)
           },
    203 :{ 'name': TTLocalizer.StatuaryMinnie,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_minnie",
           'worldScale' : 0.05,
           'varieties' : ( (1003,1,0),),
           'pinballScore' : (150,1)
           },
    204 :{ 'name': TTLocalizer.StatuaryMickey2,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_mickey_shovel",
           'worldScale' : 0.05,
           'varieties' : ( (1004,1,0),),
           'pinballScore' : (250,1)
           },
    205 :{ 'name': TTLocalizer.StatuaryToonWave,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_pedestal",
           'worldScale' : 0.05,
           'varieties' : ( (1005,1,0),),
           'pinballScore' : (500,1)
           },
    206 :{ 'name': TTLocalizer.StatuaryToonVictory,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_pedestal",
           'worldScale' : 0.05,
           'varieties' : ( (1006,1,0),),
           'pinballScore' : (500,1)
           },
    207 :{ 'name': TTLocalizer.StatuaryToonCrossedArms,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_pedestal",
           'worldScale' : 0.05,
           'varieties' : ( (1007,1,0),),
           'pinballScore' : (500,1)
           },
    208 :{ 'name': TTLocalizer.StatuaryToonThinking,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_pedestal",
           'worldScale' : 0.05,
           'varieties' : ( (1008,1,0),),
           'pinballScore' : (500,1)
           },    
    230 :{ 'name': TTLocalizer.StatuaryMeltingSnowman,
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/tt_m_prp_ext_snowman",
           'worldScale' : 1.0,
           'varieties' : ( (1030,1,0),),
           'pinballScore' : (500,1),
           'growthThresholds': (1,2) # different models at growth level 0, 1, then 2 and up           
           },    
    254 :{ 'name' : 'reserved tag', #HARDCODED!!!!!!!!!!!! HAHAHA!!!
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_minnie",
           'worldScale' : 0.05,
           'varieties' : ( (2001,1,0),),
           'pinballScore' : (15,1)
          },
    #these reserved tags are used to show a garden that hasn't been started and
    #therefore don't need planter boxes. You use these tags place a single item of this
    #type on the toon's garden item list
    255 :{ 'name' : 'reserved tag', #HARDCODED!!!!!!!!!!!! HAHAHA!!!
           'plantType' : STATUARY_TYPE,
           'model' : "phase_5.5/models/estate/garden_minnie",
           'worldScale' : 0.05,
           'varieties' : ( (2002,1,0),),
           'pinballScore' : (15,1)
          },
}
if ACCELERATOR_USED_FROM_SHTIKER_BOOK:
    del PlantAttributes[202]



##Tree Utils
def getTreeTrackAndLevel(typeIndex):
    track = typeIndex / 7
    level = typeIndex % 7
    return (track, level)

def getTreeTypeIndex(track, level):
    return ((track * 7) + level)

# fill in the gagtree attributes programmatically
NUM_GAGS = (7 * 7)
for i in range(NUM_GAGS):
    track, level = getTreeTrackAndLevel(i)
    if level <= 6:
        name = TTLocalizer.BattleGlobalAvPropStrings[track][level] + TTLocalizer.GardenGagTree 
    else:
        name = TTLocalizer.GardenUberGag
    attr = {'name': name,
            'plantType' : GAG_TREE_TYPE,
            'growthThresholds' : (level+1, (level+1)*2, (level+1)*3),
            #should we make higher level trees have less maxWaterLevel?
            #thereby forcing the toons to water it more often
            'maxWaterLevel' : getMaxWateringCanPower(),
            'minWaterLevel' : -1,
            'maxFruit' : 9 ,
            'filename' : "phase_5.5/models/estate/gag_tree_stages.bam",
            'seedlingModel' : "gag_tree_small",
            'establishedModel' : "gag_tree_med",
            'fullGrownModel' : "gag_tree_large",
            'varieties' : ((),),
            }
    PlantAttributes[i] = attr

# These bean colors were derived from these files in ttmodels/src/maps
# beanBankJellybeans.tif
# jellybeansjar2.tif
# tot_jar.tif
BeanColors = [
    (255,0,0), #red
    (0,255,0), #green
    (255,165, 0), #orange
    (148,0,211), #violet (dark)
    (0,0,255), #blue
    (255,192,203), #pink
    (255,255,0), #yellow
    (0,255,255), #cyan
    (192,192,192), #silver
    ]


# for beans, R = red, G= Green, O = Orange, V = Violet, B =BLue
# P = Pink, Y = yello, C = Cyan, S = Silver

BeanColorLetters = ['R','G', 'O', 'V', 'B', 'P', 'Y', 'C', 'S']

# Beans will correspond to the color of the bean.
# Order of the beans is important.
# Your shoveling skill will determine how many beans you can plant at one time.
# The special field is for whatever weird things we can come up with.
# (statuaries? seasonal plants? Mistletoe in christmas, etc.)
# -1 for special means it doesn't need a special
# 0 to 47 are reserved for gags

Recipes = {
    # red rose
    0 : { 'beans' : 'RRR',
          'special' : -1,
          },
    # yellow rose
    1 : { 'beans': 'RYOY',
          'special' : -1,
          },
    # pink rose
    2 : { 'beans': 'RPOROP',
          'special' : -1,
          },
    # white rose,
    3 : { 'beans': 'RCOPVCC',
          'special' : -1,
          },
    # blue rose
    4 : { 'beans': 'RBVVBBPB',
          'special' : -1,
          },

    # yellow daisy
    10 : { 'beans': 'Y',
          'special' : -1,
          },
    # pink daisy
    11 : { 'beans': 'YR',
          'special' : -1,
          },
    # white daisy
    12 : { 'beans': 'YRG',
          'special' : -1,
          },
    # red daisy
    13 : { 'beans': 'YRCO',
           'special' : -1,
          },
    # orange daisy
    14 : { 'beans': 'YROOO',
           'special' : -1,
          },
    # blue daisy
    15 : { 'beans': 'YBCVBB',
           'special' : -1,
          },
    # green daisy
    16 : { 'beans': 'YGROGGG',
           'special' : -1,
          },
    # violet daisy
    17 : { 'beans': 'YBVCVROV',
           'special' : -1,
          },
    # violet tulip
    20 : { 'beans': 'VRBVV',
          'special' : -1,
          },
    # red tulip
    21 : { 'beans': 'VRRRVV',
          'special' : -1,
          },
    # yellow tulip
    22 : { 'beans': 'VYYVYOVY',
          'special' : -1,
          },
    # pink carnation
    30 : { 'beans': 'P',
          'special' : -1,
          },
    # yellow carnation
    31 : { 'beans': 'PY',
          'special' : -1,
          },
    # red carnation
    32 : { 'beans': 'PRR',
          'special' : -1,
          },
    # white carnation
    33 : { 'beans': 'PRGBR',
          'special' : -1,
          },
    # green carnation
    34 : { 'beans': 'PGGGGYG',
          'special' : -1,
          },

    # white lily
    40 : { 'beans': 'C',
          'special' : -1,
          },
    # green lily
    41 : { 'beans': 'CG',
          'special' : -1,
          },
    # orange lily
    42 : { 'beans': 'COO',
          'special' : -1,
          },
    # pink lily
    43 : { 'beans': 'COOP',
          'special' : -1,
          },
    # red lily
    44 : { 'beans': 'CRRRR',
          'special' : -1,
          },
    # violet lily
    45 : { 'beans': 'CRVVVV',
          'special' : -1,
          },
    # blue lily
    46 : { 'beans': 'CVCBCBB',
          'special' : -1,
          },
    # yellow lily
    47 : { 'beans': 'CBYYCBYY',
          'special' : -1,
          },
    # green daffodil
    50 : { 'beans': 'G',
          'special' : -1,
          },
    # white daffodil
    51 : { 'beans': 'GC',
          'special' : -1,
          },
    # yellow daffodil
    52 : { 'beans': 'GPYY',
          'special' : -1,
          },

    # pink daffodil
    53 : { 'beans': 'GPBPP',
          'special' : -1,
          },

    # orange pansy
    60 : { 'beans': 'O',
          'special' : -1,
          },

    # white pansy
    61 : { 'beans': 'OC',
          'special' : -1,
          },
    # red pansy
    62 : { 'beans': 'ORR',
          'special' : -1,
          },
    # yellow pansy
    63 : { 'beans': 'OYYR',
          'special' : -1,
          },
    # pink pansy
    64 : { 'beans': 'OPPOBP',
          'special' : -1,
          },

    # blue petunia
    70 : { 'beans': 'BVBVCBB',
          'special' : -1,
          },
    # pink petunia
    71 : { 'beans': 'BPPBROYY',
          'special' : -1,
         },


    # donald statue
    1000 : { 'beans': 'GG',
             'special' : 100
             },
    # mickey flute statue
    1001 : { 'beans': 'SSSS',
             'special' : 101
             },
    # garden accelerator
    1002 : { 'beans': 'S',
             'special' : 102
             },
    # minnie statue
    1003 : { 'beans': 'VVVVVV',
             'special' : 103
             },
    # mickey shovel statue
    1004 : { 'beans': 'OOOOOOOO',
             'special' : 104
             },
    # own toon's statue: pose = wave
    1005 : { 'beans': 'RRRRRRRR',
             'special' : 105
             },
    # own toon's statue: pose = victory
    1006 : { 'beans': 'GGGGGGGG',
             'special' : 106
             },
    # own toon's statue: pose = crossed arms
    1007 : { 'beans': 'BBBBBBBB',
             'special' : 107
             },
    # own toon's statue: pose = thinking
    1008 : { 'beans': 'SSSSSSSS',
             'special' : 108
             },
    # melting snowman
    1030 : { 'beans': 'S',
             'special' : 130
             },    
    # reserved tag recipe, deliberately invalid color
    2001 : { 'beans': 'ZVOVOVO',
             'special' : -1
             },
    # reserved tag recipe, deliberately invalid color
    2002 : { 'beans': 'ZOVOVOV',
             'special' : -1
             },
    }

def getRecipeKey( beans, special):
    """
    returns -1 if not found
    """
    testDict = { 'beans':beans, 'special' :special }
    for key in Recipes.keys():
        recipe = Recipes[key]
        if testDict == recipe:
            return key
    return -1

def getRecipeKeyUsingSpecial( special):
    """
    returns -1 if not found
    WARNING assumes 1 special is not used in 2 recipes
    """
    for key in Recipes.keys():
        recipe = Recipes[key]
        if recipe['special'] == special:
            return key
    return -1


SHOVEL_TIN = 0
SHOVEL_STEEL = 1
SHOVEL_SILVER = 2
SHOVEL_GOLD = 3
MAX_SHOVELS = 4

# Skill pts indicates how much skill pts you need to graduate
# to the next level shovel.
# For the highest shovel it will represent the maximum,
# Needed in case we have more than 1 box for the highest shovel
# so e.g. the skillPts is 800, and numboxes is 2, the last box
# will be unlocked when the gold shovel skil reaches 400
# Ideally the skill pts is evenly divisible by the number of flower hardpoints
# (currently 6)
ShovelAttributes = {
    0 : { 'numBoxes' : 2,
          'skillPts' : 80,
          'name' : TTLocalizer.ShovelTin,
          },
    1 : { 'numBoxes' : 2,
          'skillPts' : 160,
          'name' : TTLocalizer.ShovelSteel,
          },
    2 : { 'numBoxes' : 2,
          'skillPts' : 320,
          'name' : TTLocalizer.ShovelSilver,
          },
    3 : { 'numBoxes' : 2,
          'skillPts' : 640,
          'name' : TTLocalizer.ShovelGold,
          },
    }

def getShovelPower(shovel , shovelSkill):
    """
    based on his shovel and his current shovel skill,
    how many jelly beans can we use
    """
    assert shovel < MAX_SHOVELS
    numBoxes = 0
    for curShovel in range(shovel + 1):
        shovelAttrib = ShovelAttributes[curShovel]
        curBoxes = shovelAttrib['numBoxes']
        skill = shovelAttrib['skillPts']
        if curShovel == shovel:
            if (shovelSkill >= skill):
                gardenNotify.warning("this shouldn't happen shovelSkill %d >= skill %d" % (shovelSkill, skill))
                shovelSkill = skill -1
            skillPtPerBox = skill / curBoxes
            numBoxes += 1 + ( int(shovelSkill) / int(skillPtPerBox))
        else:
            numBoxes += curBoxes
    return numBoxes


def getMaxShovelSkill():
    """
    returns the maximum shovel skill a toon can get
    """
    retVal = 0
    retVal += ShovelAttributes[MAX_SHOVELS-1]['skillPts'] - 1
    return retVal


def getNumberOfShovelBoxes():
    retVal = 0
    for attrib in ShovelAttributes.values():
        retVal += attrib['numBoxes']
    return retVal

def getNumberOfWateringCanBoxes():
    retVal = 0
    for attrib in WateringCanAttributes.values():
        retVal += attrib['numBoxes']
    return retVal


def getNumberOfFlowerVarieties():
    """
    How many Flower Varieties do we have
    """
    retVal = 0
    for attrib in PlantAttributes.values():
        if attrib['plantType'] == FLOWER_TYPE:
            retVal += len( attrib['varieties'])
    return retVal

def getNumberOfFlowerSpecies():
    """
    How many Flower species do we have
    """
    retVal = 0
    for attrib in PlantAttributes.values():
        if attrib['plantType'] == FLOWER_TYPE:
            retVal += 1
    return retVal

def getFlowerVarieties(species):
    """
    return the varieties for this species
    """
    retval = ()
    if species in PlantAttributes.keys():
        attrib = PlantAttributes[species]
        if attrib['plantType'] == FLOWER_TYPE:
            retval = attrib['varieties']
    return retval

def getFlowerSpecies():
    """
    return a list of flower species keys
    """
    retVal = []
    for key in PlantAttributes.keys():
        attrib = PlantAttributes[key]
        if attrib['plantType'] == FLOWER_TYPE:
            retVal.append(key)
    return retVal

def getRandomFlower():
    """
    Useful for debugging
    """
    species = random.choice(getFlowerSpecies())
    variety = random.randint(0, len(PlantAttributes[species]['varieties'])-1)
    return species, variety


def getFlowerVarietyName(species, variety):
    retVal = TTLocalizer.FlowerUnknown
    if species in PlantAttributes.keys():
        attrib = PlantAttributes[species]
        if variety < len(attrib['varieties']) :
            #this block would produce something like 'red rose'
            #varietyTuple = attrib['varieties'][variety]
            #speciesName = attrib['name']
            #colorStr = TTLocalizer.FlowerColorStrings[varietyTuple[1]]
            #retVal = TTLocalizer.FlowerVarietyNameFormat % (colorStr, speciesName)


            #we use the funny flower names now
            funnySpeciesNameList = TTLocalizer.FlowerFunnyNames.get(species)
            if funnySpeciesNameList:
                if variety < len(funnySpeciesNameList):
                    retVal = TTLocalizer.FlowerFunnyNames[species][variety]
        else:
            gardenNotify.warning('warning unknown species=%d variety= %d' % (species, variety))
    else:
        gardenNotify.warning('warning unknown species %d' % species)



    return retVal

def getSpeciesVarietyGivenRecipe(recipeKey):
    """
    returns (-1,-1) if not found
    """
    for species in PlantAttributes.keys():
        attrib = PlantAttributes[species]
        if attrib['plantType'] == GAG_TREE_TYPE:
            continue
        if attrib.has_key('varieties'):
            for variety in range(len(attrib['varieties'])):
                if attrib['varieties'][variety][0] == recipeKey:
                    return (species, variety)
    return (-1,-1)

def getNumBeansRequired(species,variety):
    """
    How many jelly beans do you need to plant this, returns -1 on error
    """
    retval = -1
    if not PlantAttributes.get(species):
        return retval
    if not PlantAttributes[species].has_key('varieties'):
        return retval
    if variety >= len(PlantAttributes[species]['varieties'] ):
        return -1
    recipeKey = PlantAttributes[species]['varieties'][variety][0]

    recipe = Recipes.get(recipeKey)
    if recipe:
        if recipe.has_key('beans'):
            retval = len(recipe['beans'])

    return retval


def validateRecipes(notify):
    """
    Go through the recipes and make sure none of them are the same
    """
    uniqueRecipes = []
    uniqueBeans = []
    numBoxes = getNumberOfShovelBoxes()

    #because we give a description of the special in the specials tab of the garden page
    #we now enfore the rule that a special can only appear in the recipes once
    uniqueSpecials = []

    for key in Recipes.keys():
        recipe = Recipes[key]
        beans = recipe['beans']

        #double check that beans recipe fit in our number of boxes
        if len(beans) > numBoxes:
            notify.warning('numBoxes=%d beans=%s, truncating to %s' % (numBoxes, beans, beans[:numBoxes]))
            beans = beans[:numBoxes]


        #double check we're using valid bean letters
        for letter in beans:
            if not key in (2001,2002):
                assert letter in BeanColorLetters, 'Bad bean %c -- key=%d, beans=%s' % (letter,key,beans)
        testTuple = (beans, recipe['special'])
        assert testTuple not in uniqueRecipes, 'Duplicate recipe %s key=%d' % (testTuple, key)
        uniqueRecipes.append(testTuple)

        #produce a warning if beans is repeated elsewhere
        if beans:
            if beans in uniqueBeans:
                notify.warning('duplicate beans=%s in key=%d' % (beans, key))
            else:
                uniqueBeans.append(beans)

        #double check uniqueness and validity of special
        special = recipe['special']
        if special != -1:
            assert special in Specials.keys(), 'No special %d in Specials dict' % (special)
            assert special not in uniqueSpecials, 'Duplicate special %s key=%d' % (testTuple, key)
            uniqueSpecials.append(special)


    notify.debug( 'recipes are ok')
    pass


def validatePlantAttributes(notify):
    """
    # Go through the plant attributes and make sure:
    # 1) we don't have invalid growth thresholds
    # 2) we don't have two plants with the same recipe
    """
    uniqueRecipes = []

    flowerRecipeDistribution = []
    for i in range (getNumberOfShovelBoxes()+1 ):
        flowerRecipeDistribution.append([])



    for key in PlantAttributes.keys():
        plant = PlantAttributes[key]
        notify.debug('now validating %s' % plant['name'])
        #check growth thresholds
        if plant['plantType'] in (GAG_TREE_TYPE, FLOWER_TYPE):
            growthThresholds = plant['growthThresholds']
            assert len(growthThresholds) == 3, 'Need 3 numbers in growthThresholdskey=%d' % key
            lastValue = 0
            for testValue in growthThresholds:
                assert lastValue <= testValue, 'prevValue <= nextValue growthThreholds=%s' % str(growthThresholds)
                lastValue = testValue
        #check for duplicate recipe
        if plant['plantType'] in (STATUARY_TYPE, FLOWER_TYPE):
            varieties = plant['varieties']
            for variety in varieties:
                recipeNum = variety[0]
                #check if recipeNum is valid
                assert recipeNum in Recipes.keys(), 'Invalid recipeNum %d, key=%d, variety=%s' % (recipeNum, key, str(variety))
                assert recipeNum not in uniqueRecipes, 'duplicate recipe %d, key=%d, variety=%s' % (recipeNum, key, str(variety))
                uniqueRecipes.append(recipeNum)

                #heck while we're at it, produce a distribution report
                if plant['plantType'] == FLOWER_TYPE:
                    recipeLength = len ( Recipes[recipeNum]['beans'])
                    newInfo = ( getFlowerVarietyName(key,list(varieties).index(variety)),
                                Recipes[recipeNum]['beans'],
                                TTLocalizer.FlowerColorStrings[variety[1]] )
                    flowerRecipeDistribution[recipeLength].append(newInfo)

    for numBeans in range(len (flowerRecipeDistribution)):
        notify.debug('%d flowers with %d beans' % (len(flowerRecipeDistribution[numBeans]),numBeans))
        for flower in flowerRecipeDistribution[numBeans]:
            notify.debug('    %s,  beans = %s, color=%s' % (flower[0],flower[1],flower[2]))

    notify.debug( 'plant attributes are ok')
    pass

#hardpoint DGG.TYPES #RAU nuked using GAG_TREE_TYPE, FLOWER_TYPE, STATUARY_TYPE
#so that the numbers match up properly

#hardpoint positions
plots0 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (-54,-13.5, 276.0, GAG_TREE_TYPE), (-7,-48, 343.0, GAG_TREE_TYPE),
    (-40,-75, 27.0, GAG_TREE_TYPE), (-78,-44, 309.0, GAG_TREE_TYPE),
    (-72,-15, 260.0, GAG_TREE_TYPE), (-24,-19, 294.0, GAG_TREE_TYPE),
    (11,-26, 0.0, GAG_TREE_TYPE), (-92,-4, 0.0, GAG_TREE_TYPE),
    (-100,-43, -90.0, STATUARY_TYPE),

)

plots1 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (62,-81, 194.0, GAG_TREE_TYPE), (101,-52, 250.0, GAG_TREE_TYPE),
    (93,-104, 214.0, GAG_TREE_TYPE), (69,-122, 188.0, GAG_TREE_TYPE),
    (92,-120, 184.0, GAG_TREE_TYPE), (113,-29, 250.0, GAG_TREE_TYPE),
    (125,-57, 0.0, GAG_TREE_TYPE), (114,-40, 0.0, GAG_TREE_TYPE),
    (47,-82, -30.0, STATUARY_TYPE),
)

plots2 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (-40,-114, 176.0, GAG_TREE_TYPE), (-44,-148, 162.0, GAG_TREE_TYPE),
    (-97,-99, 138.0, GAG_TREE_TYPE), (-82,-94, 134.0, GAG_TREE_TYPE),
    (-27,-106, 195.0, GAG_TREE_TYPE), (-76,-147, 110.0, GAG_TREE_TYPE),
    (-29,-164, 0.0, GAG_TREE_TYPE), (-107,-94, 0.0, GAG_TREE_TYPE),
    (-97,-114, -60.0, STATUARY_TYPE),
)

plots3 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (59,35, 187.0, GAG_TREE_TYPE), (87,28, 114.0, GAG_TREE_TYPE),
    (67,-16, 78.0, GAG_TREE_TYPE), (24,19, 155.0, GAG_TREE_TYPE),
    (18,31, 172.0, GAG_TREE_TYPE), (74,36, 133.0, GAG_TREE_TYPE),
    (35,-34, 0.0, GAG_TREE_TYPE), (116,17, 0.0, GAG_TREE_TYPE),
    (117,27, 102.0, STATUARY_TYPE),
)

plots4 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (37,101, 350.0, GAG_TREE_TYPE), (15,100, 342.0, GAG_TREE_TYPE),
    (73,92, 0.0, GAG_TREE_TYPE), (74,69, 347.0, GAG_TREE_TYPE),
    (102,62, 334.0, GAG_TREE_TYPE), (86,76, 350.0, GAG_TREE_TYPE),
    (100,78, 327.0, GAG_TREE_TYPE), (15,73, 50.0, GAG_TREE_TYPE),
    (16,87, -140.0, STATUARY_TYPE),
)

plots5 = (
    (0,0, 0.0, FLOWER_TYPE),
    (1,0, 0.0, FLOWER_TYPE),
    (2,0, 0.0, FLOWER_TYPE), (2,1, 0.0, FLOWER_TYPE), (2,2, 0.0, FLOWER_TYPE),
    (3,0, 0.0, FLOWER_TYPE), (3,1, 0.0, FLOWER_TYPE), (3,2, 0.0, FLOWER_TYPE),
    (4,0, 0.0, FLOWER_TYPE), (4,1, 0.0, FLOWER_TYPE),
    (-26,92, 41.0, GAG_TREE_TYPE), (-71,58, 37.0, GAG_TREE_TYPE),
    (-67,21, 243.0, GAG_TREE_TYPE), (-10,-2.6, 178.0, GAG_TREE_TYPE),
    (-60,13.7, 250.0, GAG_TREE_TYPE), (-13,84, 2.0, GAG_TREE_TYPE),
    (-62,65, 0.0, GAG_TREE_TYPE), (-16.6,52.7, 0.0, GAG_TREE_TYPE),
    (-55,70, 213.0, STATUARY_TYPE),
)

estatePlots = (plots0, plots1, plots2, plots3, plots4, plots5)

BOX_ONE = 1
BOX_TWO = 2
BOX_THREE = 3

flowerBoxes0 = (
    (-62.5,-52.5,  182.0, BOX_ONE),
    (-52,-52,  182, BOX_ONE),
    (-64.5,-42, 92.0, BOX_THREE),
    (-49,-43, 266.0, BOX_THREE),
    (-57,-33, 0.0, BOX_TWO),
)
flowerBoxes1 = (
    (85.0,-67.0, 26.0, BOX_ONE),
    (75,-72, 26.0, BOX_ONE),
    (91.0,-74.0, -63.0, BOX_THREE),
    (77,-81, 117.0, BOX_THREE),
    (88,-86, 206.0, BOX_TWO),

)
flowerBoxes2 = (
    (-62,-112, 350.0, BOX_ONE),
    (-72,-110, 350.0, BOX_ONE),
    (-62,-122, 257.0, BOX_THREE),
    (-76,-118, 79.0, BOX_THREE),
    (-71,-129, 169.0, BOX_TWO),
)
flowerBoxes3 = (
    (72,5, 265.0, BOX_ONE),
    (72.5,16, 265.0, BOX_ONE),
    (63,3, 178.0, BOX_THREE),
    (64,19, 355.0, BOX_THREE),
    (54,12, 86.0, BOX_TWO),
)
flowerBoxes4 = (
    (35.5,70, 152.0, BOX_ONE),
    (46,  66, 152.0, BOX_ONE),
    (36.5,79.5, 71.0, BOX_THREE),
    (51.5,74, 247.0, BOX_THREE),
    (47,  86, -19.0, BOX_TWO),
)
flowerBoxes5 = (
    (-26.5, 37.5, 318.0, BOX_ONE),
    (-33, 46, 318.0, BOX_ONE),
    (-32, 30, 217.0, BOX_THREE),
    (-42, 42, 37.0, BOX_THREE),
    (-45, 31, 124.0, BOX_TWO),
)

estateBoxes = (flowerBoxes0, flowerBoxes1, flowerBoxes2, flowerBoxes3, flowerBoxes4, flowerBoxes5)


def whatCanBePlanted( plotIndex, hardPointIndex):
    """
    If the number of hardpoints changes, this must be updated as well.
    """
    retval = INVALID_TYPE

    if plotIndex < len(estatePlots) and plotIndex >= 0:
        if hardPointIndex < len(estatePlots[plotIndex]) and hardPointIndex >=0:
            if len(estatePlots[plotIndex][hardPointIndex]) >= 4:
                retval = estatePlots[plotIndex][hardPointIndex][3]

    if 0:
        #this style will make changing the number of gag trees, flowers and statuaries easier
        #the current style allows for interspersed types.
        typeThresholds  = [5,11,15]

        if __debug__:
            for plot in estatePlots:
                for threshold in typeThresholds:
                    assert threshold < len(plot)
                    pass
                assert typeThresholds[2] == len(plot) - 1


        if 0 <= hardPointIndex  and hardPointIndex < typeThresholds[0]:
            retval = FLOWER_TYPE
        if typeThresholds[0] <= hardPointIndex and hardPointIndex < typeThresholds[1]:
            retval = GAG_TREE_TYPE
        if typeThresholds[1] <= hardPointIndex and hardPointIndex < typeThresholds[2]:
            retval = STATUARY_TYPE
        if typeThresholds[2] <= hardPointIndex and hardPointIndex < typeThresholds[3]:
            retval = STATUARY__TOON_TYPE

    return retval



#specials table
# magicBeans modify what is grown
# gardenItems are drop in items
MAGIC_BEAN_SUBTYPE = 0
GARDEN_ITEM_SUBTYPE = 1
#RAU currently magic beans are not being used
#gagbonus intent is some sort of bonus on the gag trees, not currently used
#photoModel defines what we'll show in the gui
#photoScale is the scale applied to photoModel
#photoPos repositioning for the gui
#photoName the name to use in the gui
#isCatalaog is this sold in the catalog
#beanCost  how many jellybeans does it take to buy this
Specials = {
0 : {'subtype' : MAGIC_BEAN_SUBTYPE,
     'gagbonus' : 1,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeans,
     'description': TTLocalizer.GardenSpecialDiscription,
     'beanCost' : 125
    },
1 : {'subtype': MAGIC_BEAN_SUBTYPE,
     'gagbonus': 2,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeansB,
     'description': TTLocalizer.GardenSpecialDiscriptionB,
     'beanCost' : 125
    },
2 : {'subtype' : MAGIC_BEAN_SUBTYPE,
     'gagbonus' : 1,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeans,
     'description': TTLocalizer.GardenSpecialDiscription,
     'beanCost' : 125
    },
3 : {'subtype': MAGIC_BEAN_SUBTYPE,
     'gagbonus': 2,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeansB,
     'description': TTLocalizer.GardenSpecialDiscriptionB,
     'beanCost' : 125
    },
4 : {'subtype' : MAGIC_BEAN_SUBTYPE,
     'gagbonus' : 1,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeans,
     'description': TTLocalizer.GardenSpecialDiscription,
     'beanCost' : 125
    },
5 : {'subtype': MAGIC_BEAN_SUBTYPE,
     'gagbonus': 2,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeansB,
     'description': TTLocalizer.GardenSpecialDiscriptionB,
     'beanCost' : 125
    },
6 : {'subtype': MAGIC_BEAN_SUBTYPE,
     'gagbonus': 2,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeansB,
     'description': TTLocalizer.GardenSpecialDiscription,
     'beanCost' : 125
    },
7 : {'subtype': MAGIC_BEAN_SUBTYPE,
     'gagbonus': 2,
     'photoModel' : "phase_4/models/props/goofy_statue",
     'photoScale' : 0.1,
     'photoPos' : (0,0,-1),
     'photoName': TTLocalizer.GardenTextMagicBeansB,
     'description': TTLocalizer.GardenSpecialDiscriptionB,
     'beanCost' : 125
    },
100 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_donald",
    'photoScale' : 0.04,
    'photoPos' : (0,0,-1),
    'photoName' : TTLocalizer.StatuaryDonald,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 125

    },
101 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_mickey_flute",
    'photoScale' : 0.025,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryMickey1,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 250
    },
102 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/sack",
    'photoScale' : 1.0,
    'photoPos' : (0,0,-1.0),
    'photoName' : TTLocalizer.StatuaryGardenAccelerator,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 7500,
    'useFromShtiker' : False
    },
103 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_minnie",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryMinnie,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 500
    },
104 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_mickey_shovel",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryMickey2,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 1000
},
105 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_pedestal",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryToonWave,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 5000,
    'minSkill' : 639
    },
106 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_pedestal",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryToonVictory,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 5000,
    'minSkill' : 639
    },
107 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_pedestal",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryToonCrossedArms,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 5000,
    'minSkill' : 639
    },
108 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/garden_pedestal",
    'photoScale' : 0.02,
    'photoPos' : (0,0,-1.05),
    'photoName' : TTLocalizer.StatuaryToonThinking,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 5000,
    'minSkill' : 639
    },
130 : {
    'subtype' : GARDEN_ITEM_SUBTYPE,
    'photoModel' : "phase_5.5/models/estate/tt_m_prp_ext_snowman_icon",
    'photoScale' : 90.0,
    'photoPos' : (0,0,0),    
    'photoName' : TTLocalizer.StatuaryMeltingSnowman,
    'description': TTLocalizer.GardenSpecialDiscription,
    'isCatalog' : True,
    'beanCost' : 25,
    'minSkill' : 0,

    },
}



GardenAcceleratorSpecial = 102
GardenAcceleratorSpecies = 202

if ACCELERATOR_USED_FROM_SHTIKER_BOOK:
    Specials[GardenAcceleratorSpecial]['useFromShtiker'] = True


def getPlantItWithString(special):
    retval = ''
    recipeKey = getRecipeKeyUsingSpecial(special)
    if not recipeKey == -1:
        beanTuple = []
        beanStr = Recipes[recipeKey]['beans']
        for letter in beanStr:
            index = BeanColorLetters.index(letter)
            beanTuple.append(index)
        #now we have the beanTuple, get the equivalent
        beanText = TTLocalizer.getRecipeBeanText(beanTuple)
        retval += TTLocalizer.PlantItWith % beanText
    return retval

#this automatically sets up the description for the Special dictionary
for specialKey in Specials.keys():
    recipeKey = getRecipeKeyUsingSpecial(specialKey)
    if not recipeKey == -1:
        Specials[specialKey]['description'] = getPlantItWithString(specialKey)
        if specialKey == GardenAcceleratorSpecial:
            if ACCELERATOR_USED_FROM_SHTIKER_BOOK:
                Specials[specialKey]['description'] = TTLocalizer.UseFromSpecialsTab
            Specials[specialKey]['description'] += TTLocalizer.MakeSureWatered


#Time of day that the epochs happen
TIME_OF_DAY_FOR_EPOCH = 3

# Movie Modes
MOVIE_HARVEST = 0
MOVIE_PLANT = 1
MOVIE_REMOVE = 2
MOVIE_WATER = 3
MOVIE_FINISHPLANTING = 4
MOVIE_FINISHREMOVING = 5
MOVIE_CLEAR = 6
MOVIE_PLANT_REJECTED = 7

#stuff for garden trophies
TrophyDict = {
    0: (TTLocalizer.GardenTrophyNameDict[0],),
    1: (TTLocalizer.GardenTrophyNameDict[1],),
    2: (TTLocalizer.GardenTrophyNameDict[2],),
    3: (TTLocalizer.GardenTrophyNameDict[3],),
    }




