"""
   CogDisguiseGlobals module:

   Contains constants for the various classes for public consumption
"""

from toontown.suit import SuitDNA
import types
from toontown.toonbase import TTLocalizer

# how many parts are required for the different depts
PartsPerSuit = ( 17, 14, 12, 10 )

# how many of the 17 total parts do we care about for the different depts
PartsPerSuitBitmasks = (
    131071, # 111 111 11111 111 111 = 17 parts
    130175, # 111 111 10001 111 111 = 14 parts
    56447,  # 011 011 10001 111 111 = 12 parts
    56411,  # 011 011 10001 011 011 = 10 parts
    )

# the complete set of bits that are used to represent suit parts
AllBits = 131071  # 111 111 11111 111 111

# minimum number of parts to lose if the bossbot zaps you
MinPartLoss = 2

# maximum number of parts to lose if the bossbot zaps you
MaxPartLoss = 4

# how many merits needed for promotion per level per dept
MeritsPerLevel = (
     # bossbots
     (100, 130, 160, 190, 800), # f 1-5
     (160, 210, 260, 310, 1300), # p 2-6
     (260, 340, 420, 500, 2100), # ym 3-7
     (420, 550, 680, 810, 3400), # mm 4-8
     (680, 890, 1100, 1310, 5500), # ds 5-9
     (1100, 1440, 1780, 2120, 8900), # hh 6-10
     (1780, 2330, 2880, 3430, 14400), # cr 7-11
     (2880, 3770, 4660, 5500, 23300, # tbc 8-12
     # these are at irregular intervals to correspond with laff point bonuses
      2880, 23300, # tbc 13-14
      2880, 3770, 4660, 5500, 23300, # tbc 15-19
      2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, # tbc 20-29
      2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, # tbc 30-39
      2880, 3770, 4660, 5500, 6440, 7330, 8220, 9110, 10000, 23300, # tbc 40-49
      0), # tbc

     # lawbots
     (60, 80, 100, 120, 500), # bf 1-5
     (100, 130, 160, 190, 800), # b 2-6
     (160, 210, 260, 310, 1300), # dt 3-7
     (260, 340, 420, 500, 2100), # ac 4-8
     (420, 550, 680, 810, 3400), # bs 5-9
     (680, 890, 1100, 1310, 5500), # sd 6-10
     (1100, 1440, 1780, 2120, 8900), # le 7-11
     (1780, 2330, 2880, 3430, 14400, # bw 8-12
      # these are at irregular intervals to correspond with laff point bonuses
      1780, 14400, # bw 13-14
      1780, 2330, 2880, 3430, 14400, # bw 15-19
      1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, # bw 20-29
      1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, # bw 30-39
      1780, 2330, 2880, 3430, 3980, 4530, 5080, 5630, 6180, 14400, # bw 40-49
      0), # bw 50

     # cashbots
     (40, 50, 60, 70, 300),  # sc 1-5
     (60, 80, 100, 120, 500), # pp 2-6
     (100, 130, 160, 190, 800), # tw 3-7
     (160, 210, 260, 310, 1300), # bc 4-8
     (260, 340, 420, 500, 2100), # nc 5-9
     (420, 550, 680, 810, 3400), # mb 6-10
     (680, 890, 1100, 1310, 5500), # ls 7-11
     (1100, 1440, 1780, 2120, 8900, # rb 8-12
      # these are at irregular intervals to correspond with laff point bonuses
      1100, 8900, # rb 13-14
      1100, 1440, 1780, 2120, 8900, # rb 15-19
      1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, # rb 20-29
      1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, # rb 30-39
      1100, 1440, 1780, 2120, 2460, 2800, 3140, 3480, 3820, 8900, # rb 40-49
      0), # rb 50

     # sellbots
     (20, 30, 40, 50, 200),  # cc 1-5
     (40, 50, 60, 70, 300),  # tm 2-6
     (60, 80, 100, 120, 500), # nd 3-7
     (100, 130, 160, 190, 800), # gh 4-8
     (160, 210, 260, 310, 1300), # ms 5-9
     (260, 340, 420, 500, 2100), # tf 6-10
     (420, 550, 680, 810, 3400), # m 7-11
     (680, 890, 1100, 1310, 5500, # mh 8-12
      680, 5500, # mh 13-14
      680, 890, 1100, 1310, 5500, # mh 15-19
      680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, # mh 20-29
      680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, # mh 30-39
      680, 890, 1100, 1310, 1520, 1730, 1940, 2150, 2360, 5500, # mh 40-49
      0), # mh 50

     )

# masks for pulling out the various parts from the cogParts bit string

leftLegUpper = 1           # 0000 0000 0000 0000 0001
leftLegLower = 2           # 0000 0000 0000 0000 0010
leftLegFoot = 4            # 0000 0000 0000 0000 0100
rightLegUpper = 8          # 0000 0000 0000 0000 1000

rightLegLower = 16         # 0000 0000 0000 0001 0000
rightLegFoot = 32          # 0000 0000 0000 0010 0000
torsoLeftShoulder = 64     # 0000 0000 0000 0100 0000
torsoRightShoulder = 128   # 0000 0000 0000 1000 0000

torsoChest = 256           # 0000 0000 0001 0000 0000
torsoHealthMeter = 512     # 0000 0000 0010 0000 0000
torsoPelvis = 1024         # 0000 0000 0100 0000 0000
leftArmUpper = 2048        # 0000 0000 1000 0000 0000

leftArmLower = 4096        # 0000 0001 0000 0000 0000
leftArmHand = 8192         # 0000 0010 0000 0000 0000
rightArmUpper = 16384      # 0000 0100 0000 0000 0000
rightArmLower = 32768      # 0000 1000 0000 0000 0000

rightArmHand = 65536       # 0001 0000 0000 0000 0000

# for tracks that don't use all of the torso parts
# the torsoLeftShoulder bit is used to represent the entire upper torso
upperTorso = torsoLeftShoulder

leftLegIndex = 0
rightLegIndex = 1
torsoIndex = 2
leftArmIndex = 3
rightArmIndex = 4

PartsQueryShifts = (
    leftLegUpper,
    rightLegUpper,
    torsoLeftShoulder,
    leftArmUpper,
    rightArmUpper,
    )

PartsQueryMasks = (
    leftLegFoot + leftLegLower + leftLegUpper,
    rightLegFoot + rightLegLower + rightLegUpper,
    torsoPelvis + torsoHealthMeter + torsoChest + torsoRightShoulder + torsoLeftShoulder,
    leftArmHand + leftArmLower + leftArmUpper,
    rightArmHand + rightArmLower + rightArmUpper
    )

PartNameStrings = TTLocalizer.CogPartNames
SimplePartNameStrings = TTLocalizer.CogPartNamesSimple

PartsQueryNames = (
    # bossbots
    {1: PartNameStrings[0], 2: PartNameStrings[1], 4: PartNameStrings[2],
       8: PartNameStrings[3], 16: PartNameStrings[4], 32: PartNameStrings[5],
       64: PartNameStrings[6], 128: PartNameStrings[7], 256: PartNameStrings[8],
       512: PartNameStrings[9], 1024: PartNameStrings[10],
       2048: PartNameStrings[11], 4096: PartNameStrings[12], 8192: PartNameStrings[13],
       16384: PartNameStrings[14], 32768: PartNameStrings[15], 65536: PartNameStrings[16]
     },
    # lawbots
    {1: PartNameStrings[0], 2: PartNameStrings[1], 4: PartNameStrings[2],
     8: PartNameStrings[3], 16: PartNameStrings[4], 32: PartNameStrings[5],
     64: SimplePartNameStrings[0], 128: SimplePartNameStrings[0],  256: SimplePartNameStrings[0],
     512: SimplePartNameStrings[0], 1024: PartNameStrings[10],
     2048: PartNameStrings[11], 4096: PartNameStrings[12], 8192: PartNameStrings[13],
     16384: PartNameStrings[14], 32768: PartNameStrings[15], 65536: PartNameStrings[16]
     },
    # cashbots
    {1: PartNameStrings[0], 2: PartNameStrings[1], 4: PartNameStrings[2],
     8: PartNameStrings[3], 16: PartNameStrings[4], 32: PartNameStrings[5],
     64: SimplePartNameStrings[0], 128: SimplePartNameStrings[0],  256: SimplePartNameStrings[0],
     512: SimplePartNameStrings[0], 1024: PartNameStrings[10],
     2048: PartNameStrings[11], 4096: PartNameStrings[12], 8192: PartNameStrings[12],
     16384: PartNameStrings[14], 32768: PartNameStrings[15], 65536: PartNameStrings[15]
     },
    # sellbots
    {1: PartNameStrings[0], 2: PartNameStrings[1], 4: PartNameStrings[1],
     8: PartNameStrings[3], 16: PartNameStrings[4], 32: PartNameStrings[4],
     64: SimplePartNameStrings[0], 128: SimplePartNameStrings[0],  256: SimplePartNameStrings[0],
     512: SimplePartNameStrings[0], 1024: PartNameStrings[10],
     2048: PartNameStrings[11], 4096: PartNameStrings[12], 8192: PartNameStrings[12],
     16384: PartNameStrings[14], 32768: PartNameStrings[15], 65536: PartNameStrings[15]
     },
    )

# utility functions

def getNextPart(parts, partIndex, dept):
    """
    Returns a nextPart number and name given a partIndex (0=left leg, 1=right leg, 2=torso, 3=left arm,
    4=right arm) and a cog dept number.
    """
    dept = dept2deptIndex(dept)
    needMask = PartsPerSuitBitmasks[dept] & PartsQueryMasks[partIndex]
    haveMask = parts[dept] & PartsQueryMasks[partIndex]

    # turn the 0's in the needMask to 1's in the haveMask
    nextPart = ~needMask | haveMask
    # turn the number to all 1's up to the first 0
    nextPart = nextPart ^ (nextPart + 1)
    # return the number this position represents
    nextPart = (nextPart + 1) >> 1
    return nextPart

def getPartName(partArray):
    # map this into the name array
    index = 0
    for part in partArray:
        if part:
            return PartsQueryNames[index][part]
        index += 1

def isSuitComplete(parts, dept):
    """
    Returns 1 if the suit for given dept is complete, 0 otherwise.
    """
    dept = dept2deptIndex(dept)
    # for each type of part (left arm, etc.)
    for p in range(len(PartsQueryMasks)):
        if getNextPart(parts, p, dept):
            return 0
    return 1


def getTotalMerits(toon, index):
    from toontown.battle import SuitBattleGlobals
    cogIndex = toon.cogTypes[index] + (SuitDNA.suitsPerDept * index)
    cogTypeStr = SuitDNA.suitHeadTypes[cogIndex]
    cogBaseLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
    cogLevel = toon.cogLevels[index] - cogBaseLevel
    # map the cog level to btwn 0 and max
    cogLevel = max(min(cogLevel, len(MeritsPerLevel[cogIndex])-1), 0)
    return MeritsPerLevel[cogIndex][cogLevel]

def getTotalParts(bitString, shiftWidth=32):
    sum = 0
    for shift in range(0, shiftWidth):
        sum = sum + ((bitString >> shift) & 1)
    return sum

def asBitstring(number):
    array = []
    shift = 0
    if number == 0:
        array.insert(0, "0")
    while pow(2, shift) <= number:
        if (number >> shift) & 1:
            array.insert(0, "1")
        else:
            array.insert(0, "0")
        shift += 1
    str = ""
    for i in range(0, len(array)):
        str = str + array[i]
    return str

def asNumber(bitstring):
    num = 0
    for i in range(0, len(bitstring)):
        if bitstring[i] == "1":
            num += pow(2, (len(bitstring) - 1) - i)
    return num

def dept2deptIndex(dept):
    if type(dept) == types.StringType:
        dept = SuitDNA.suitDepts.index(dept)
    return dept

