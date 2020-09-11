# MinigameGlobals.py: global minigame values
# used by AI and client

from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil

"""
MINIGAME SCORE TABLES

::MAX JELLYBEANS
Minigame  (1p)  (2p)  (3p)  (4p)
================================
Race       --    --    25    25
Cannon     23    23    23    23
Tag        --    50*   50*   50*
Match      --    23    23    23
Ring       21    29    34    42
Maze       24    30*   30*   30*
Tug        23    23    23    23
Catch      ===see table below==
Diving     ?     ?     ?     ?
Target     ?     ?     ?     ?
Ice        --    24    24    24
Thief      30    28    26    24
Vine       37    37    37    37 # all 19 bananas and finish with 35 secs left
Pairing    32    32    36    40 # all cards with maximum low flip bonus
Photo      35    35    35    35
2D         25    25    25    25
Note that these scores are before the area-based score multiplier is applied.
(see MINIGAME SCORE MULTIPLIERS table below)

* approximate

::CATCH GAME MAX JELLYBEANS
Safezone  (1p)  (2p)  (3p)  (4p)
================================
TTC        14    23    32    42
DD         14    24    36    47
DG         17    29    41    53
MM         18    32    45    59
BR         20    35    50    63
DL         21    38    53    69

Note that these scores are before the area-based score multiplier is applied.
(see MINIGAME SCORE MULTIPLIERS table below)

::MINIGAME SCORE MULTIPLIERS
Safezone  Mult*
==============
TTC       1.0
DD        1.1
DG        1.2
MM        1.3
BR        1.4
DL        1.5

* Round result to the nearest integer to determine final reward

The minimum number of beans you can get from every minigame is one bean (before
the multiplier).

"""

# fudge factor; should be the maximum reasonable time that it
# takes for a client msg to get to the AI server and vice versa
latencyTolerance = 10.

# this should be a conservative estimate of the maximum amount of time
# it might take to load resources for a minigame on a low-end machine
MaxLoadTime = 40.

rulesDuration = 16

DifficultyOverrideMult = int(1 << 16)
def QuantizeDifficultyOverride(diffOverride):
    """ use this function to get the closest value to the input
    difficulty override that can be converted to an integer and back
    (using DifficultyOverrideMult) without losing any precision """
    return (int(round(diffOverride * DifficultyOverrideMult)) /
            float(DifficultyOverrideMult))

NoDifficultyOverride  = 0x7fffffff
NoTrolleyZoneOverride = -1

# this is a list of the Toontown safezones, ordered by 'difficulty'
SafeZones = [
    ToontownGlobals.ToontownCentral,
    ToontownGlobals.DonaldsDock,
    ToontownGlobals.DaisyGardens,
    ToontownGlobals.MinniesMelodyland,
    ToontownGlobals.TheBrrrgh,
    ToontownGlobals.DonaldsDreamland,
    ]

def getDifficulty(trolleyZone):
    """ returns 0..1 """
    hoodZone = getSafezoneId(trolleyZone)
    return float(SafeZones.index(hoodZone)) / (len(SafeZones)-1)

def getSafezoneId(trolleyZone):
    """
    returns 1000-multiple safezone zoneId;
    can be matched to safezone IDs in ToontownGlobals.py
    """
    return ZoneUtil.getCanonicalHoodId(trolleyZone)

def getScoreMult(trolleyZone):
    szId = getSafezoneId(trolleyZone)
    # currently, mults increase linearly from TTC to DL, from 1. to 1.5
    multiplier = PythonUtil.lerp(
        1., 1.5, float(SafeZones.index(szId)) / (len(SafeZones)-1))
    return multiplier



