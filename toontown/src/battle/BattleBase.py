from pandac.PandaModules import *
from toontown.toonbase.ToontownBattleGlobals import *
from direct.task.Timer import *
import math

from direct.directnotify import DirectNotifyGlobal
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer

# locations of the various types of data within the toonAttacks list
# used when calculating attack damage, accuracy bonus, and damage bonus
#
TOON_ID_COL             = 0
TOON_TRACK_COL          = 1 
TOON_LVL_COL            = 2 
TOON_TGT_COL            = 3 
TOON_HP_COL             = 4 
TOON_ACCBONUS_COL       = 5 
TOON_HPBONUS_COL        = 6 
TOON_KBBONUS_COL        = 7 
SUIT_DIED_COL           = 8
SUIT_REVIVE_COL         = 9

# locations of the various types of data within the suitAttacks list
# used when calculating toon attack type, target, and attack damage
#
SUIT_ID_COL             = 0
SUIT_ATK_COL            = 1
SUIT_TGT_COL            = 2
SUIT_HP_COL             = 3
TOON_DIED_COL           = 4
SUIT_BEFORE_TOONS_COL   = 5
SUIT_TAUNT_COL          = 6

# Toon actions and attacks
#
NO_ID = -1
NO_ATTACK = -1
UN_ATTACK = -2
PASS_ATTACK = -3 # used so we can display pass indicator
NO_TRAP = -1
LURE_SUCCEEDED = -1
PASS = 98 
SOS = 99 
NPCSOS = 97
PETSOS = 96
FIRE = 100
# Defined in ToontownBattleGlobals.py
HEAL = HEAL_TRACK
TRAP = TRAP_TRACK
LURE = LURE_TRACK 
SOUND = SOUND_TRACK
THROW = THROW_TRACK
SQUIRT = SQUIRT_TRACK
DROP = DROP_TRACK
# For reference, in ToontownBattleGlobals
# NPC_RESTOCK_GAGS = 7
# NPC_TOONS_HIT = 8
# NPC_COGS_MISS = 9

# Attack times
#
TOON_ATTACK_TIME = 12.0
SUIT_ATTACK_TIME = 12.0

TOON_TRAP_DELAY = 0.8

TOON_SOUND_DELAY = 1.0

TOON_THROW_DELAY = 0.5 
TOON_THROW_SUIT_DELAY = 1.0

TOON_SQUIRT_DELAY = 0.5
TOON_SQUIRT_SUIT_DELAY = 1.0

TOON_DROP_DELAY = 0.8 
TOON_DROP_SUIT_DELAY = 1.0


TOON_RUN_T = 3.3
TIMEOUT_PER_USER = 5

TOON_FIRE_DELAY = 0.5 
TOON_FIRE_SUIT_DELAY = 1.0


# Reward times
#
REWARD_TIMEOUT = 120
FLOOR_REWARD_TIMEOUT = 4
BUILDING_REWARD_TIMEOUT = 300

try:
#    debugBattles = base.config.GetBool('debug-battles', 0)
    CLIENT_INPUT_TIMEOUT = base.config.GetFloat('battle-input-timeout', TTLocalizer.BBbattleInputTimeout)
except:
#    debugBattles = simbase.config.GetBool('debug-battles', 0)
    CLIENT_INPUT_TIMEOUT = simbase.config.GetFloat('battle-input-timeout', TTLocalizer.BBbattleInputTimeout)

def levelAffectsGroup(track, level):
    #return (level % 2)
    return attackAffectsGroup(track, level) #UBER

def attackAffectsGroup(track, level, type=None):
    #if (track == HEAL and (level % 2)):
    #    return 1
    #elif (track == LURE and (level % 2)):
    #    return 1
    #elif (track == SOUND):
    #    return 1
    #elif (track == NPCSOS or type == NPCSOS or track == PETSOS or type == PETSOS):
    #    return 1
    #else:
    #    return 0
    if (track == NPCSOS or type == NPCSOS or track == PETSOS or type == PETSOS):
        return 1
    elif (track >= 0) and (track <= DROP_TRACK):
        return AvPropTargetCat[AvPropTarget[track]][level]
    else:
        return 0


def getToonAttack(id, track=NO_ATTACK, level=-1, target=-1):
    """ getToonAttack(id, track, level, target)
    """
    return [id, track, level, target, [], 0, 0, [], 0, 0]

def getDefaultSuitAttacks():
    """ getDefaultSuitAttacks()
    """
    suitAttacks = [[NO_ID, NO_ATTACK, -1, [], 0, 0, 0], 
                   [NO_ID, NO_ATTACK, -1, [], 0, 0, 0], 
                   [NO_ID, NO_ATTACK, -1, [], 0, 0, 0], 
                   [NO_ID, NO_ATTACK, -1, [], 0, 0, 0]]
    return suitAttacks

def getDefaultSuitAttack():
    """ getDefaultSuitAttack()
    """
    return [NO_ID, NO_ATTACK, -1, [], 0, 0, 0]

def findToonAttack(toons, attacks, track):
    """ findToonAttack(toons, attacks, track) 
        Return all attacks of the specified track sorted by increasing level
    """
    foundAttacks = []
    for t in toons:
        if (attacks.has_key(t)):
            attack = attacks[t]
            local_track = attack[TOON_TRACK_COL]
            # If it's an NPC, convert to the appropriate track
            if (track != NPCSOS and attack[TOON_TRACK_COL] == NPCSOS):
                local_track = NPCToons.getNPCTrack(attack[TOON_TGT_COL])    
            if (local_track == track):
                if local_track == FIRE:
                    canFire = 1
                    for attackCheck in foundAttacks:
                        if attackCheck[TOON_TGT_COL] == attack[TOON_TGT_COL]:
                            canFire = 0
                        else:
                            pass
                    if canFire:
                        assert(t == attack[TOON_ID_COL])
                        foundAttacks.append(attack)
                        
                else:
                    assert(t == attack[TOON_ID_COL])
                    foundAttacks.append(attack)
    def compFunc(a, b):
        if (a[TOON_LVL_COL] > b[TOON_LVL_COL]):
            return 1
        elif (a[TOON_LVL_COL] < b[TOON_LVL_COL]):
            return -1
        return 0
    foundAttacks.sort(compFunc)
    return foundAttacks 

# A little pad time added to server time calculations, to allow for
# slow or out-of-sync clients.  In general, the AI server will give
# each client the expected time to complete its movie, plus
# SERVER_BUFFER_TIME, and then will ask all the clients to move on
# with or without the slow one(s).
SERVER_BUFFER_TIME = 2.0

#CLIENT_INPUT_TIMEOUT = TTLocalizer.BBbattleInputTimeout
SERVER_INPUT_TIMEOUT = CLIENT_INPUT_TIMEOUT + SERVER_BUFFER_TIME

# The maximum time we expect a suit to take walk to its position in
# battle.
MAX_JOIN_T = TTLocalizer.BBbattleInputTimeout

# The length of time for a faceoff taunt.
FACEOFF_TAUNT_T = 3.5

# length of time we look at the interactive prop helping toons
FACEOFF_LOOK_AT_PROP_T = 6

# The amount of time it takes to open up the elevator doors and walk
# out.
ELEVATOR_T = 4.0

BATTLE_SMALL_VALUE = 0.0000001

# This is the furthest we expect to have to walk from the face-off to
# get the battle.  If we are further away than this, we suspect we are
# victims of clock skew.
MAX_EXPECTED_DISTANCE_FROM_BATTLE = 50.0

class BattleBase:

    notify = DirectNotifyGlobal.directNotify.newCategory('BattleBase')

    # This defines the points where the suits will stand in battle.
    # For each number of suits in the battle (1, 2, 3, or 4), the
    # corresponding element of suitPoints is a list of n (pos, heading)
    # pairs for each of the n suits to stand.
    
    suitPoints = (
        ((Point3(0, 5, 0), 179),
         ),
        ((Point3(2, 5.3, 0), 170),
         (Point3(-2, 5.3, 0), 180),
         ),
        ((Point3(4, 5.2, 0), 170),
         (Point3(0, 6, 0), 179),
         (Point3(-4, 5.2, 0), 190),
         ),
        ((Point3(6, 4.4, 0), 160),
         (Point3(2, 6.3, 0), 170),
         (Point3(-2, 6.3, 0), 190),
         (Point3(-6, 4.4, 0), 200),
         ))
    
    # And this defines the single set of points for suits who are
    # "pending": they have joined the battle, but are waiting for the
    # next round to begin before they take their place.
    suitPendingPoints = (
        (Point3(-4, 8.2, 0), 190),
        (Point3(0, 9, 0), 179),
        (Point3(4, 8.2, 0), 170),
        (Point3(8, 3.2, 0), 160),
        )

    # This is similar to the above, but for toons instead of suits.
    toonPoints = (
        ((Point3(0, -6, 0), 0),
         ),
        ((Point3(1.5, -6.5, 0), 5), 
         (Point3(-1.5, -6.5, 0), -5),
         ),
        ((Point3(3, -6.75, 0), 5),
         (Point3(0, -7, 0), 0),
         (Point3(-3, -6.75, 0), -5),
         ),
        ((Point3(4.5, -7, 0), 10),
         (Point3(1.5, -7.5, 0), 5),
         (Point3(-1.5, -7.5, 0), -5),
         (Point3(-4.5, -7, 0), -10),
         ))

    toonPendingPoints = (
        (Point3(-3, -8, 0), -5),
        (Point3(0, -9, 0), 0),
        (Point3(3, -8, 0), 5),
        (Point3(5.5, -5.5, 0), 20),
        )
    
    # These define the points on the perimeter of the battle circle
    # for suits and toons who are "joining"; this allows the avatar to
    # walk a circle around the battle to get to its pending point,
    # defined above.
    posA = Point3(0, 10, 0)
    posB = Point3(-7.071, 7.071, 0)
    posC = Point3(-10, 0, 0)
    posD = Point3(-7.071, -7.071, 0)
    posE = Point3(0, -10, 0)
    posF = Point3(7.071, -7.071, 0)
    posG = Point3(10, 0, 0)
    posH = Point3(7.071, 7.071, 0)
    allPoints = (posA, posB, posC, posD, posE, posF, posG, posH)
    toonCwise = [posA, posB, posC, posD, posE]
    toonCCwise = [posH, posG, posF, posE]
    suitCwise = [posE, posF, posG, posH, posA]
    suitCCwise = [posD, posC, posB, posA]

    suitSpeed = 4.8
    toonSpeed = 8.0

    def __init__(self):
        """ __init__()
        """
        self.pos = Point3(0, 0, 0)
        self.initialSuitPos = Point3(0, 1, 0)
        self.timer = Timer()
        self.resetLists()

    def resetLists(self):
        """ resetLists()
        """
        self.suits = []
        self.pendingSuits = []
        self.joiningSuits = []
        self.activeSuits = []
        self.luredSuits = []
        self.suitGone = 0

        self.toons = []
        self.joiningToons = []
        self.pendingToons = []
        self.activeToons = []
        self.runningToons = []
        self.toonGone = 0

        # keep track of toons who helped, so we know which toons just passed all the time
        self.helpfulToons = []


    def calcFaceoffTime(self, centerpos, suitpos):
        """ calcFaceoffTime(centerpos, suitpos)
        """
        facing = Vec3(centerpos - suitpos)
        facing.normalize()
        suitdest = Point3(centerpos - Point3(facing * 6.0))
        dist = Vec3(suitdest - suitpos).length()
        return (dist / BattleBase.suitSpeed)

    def calcSuitMoveTime(self, pos0, pos1):
        """ calcSuitMoveTime(pos0, pos1)
        """
        dist = Vec3(pos0 - pos1).length()
        return (dist / BattleBase.suitSpeed)

    def calcToonMoveTime(self, pos0, pos1):
        """ calcToonMoveTime(pos0, pos1)
        """
        dist = Vec3(pos0 - pos1).length()
        return (dist / BattleBase.toonSpeed)

    def buildJoinPointList(self, avPos, destPos, toon=0):
        """ buildJoinPointList(avPos, destPos, toon)

        This function is called when suits or toons ask to join the
        battle and need to figure out how to walk to their selected
        pending point (destPos).  It builds a list of points the
        avatar should walk through in order to get there.  If the list
        is empty, the avatar will walk straight there.
        """
        # In the default case, avatars walk around the perimeter of
        # the battle cell to get to their target point.  Figure out
        # the shortest path around the circle.
        
        # First, find the closest battle join point
        minDist = 999999.0
        nearestP = None
        for p in BattleBase.allPoints:
            dist = Vec3(avPos - p).length()    
            if (dist < minDist):
                nearestP = p
                minDist = dist
        assert(nearestP != None)
        self.notify.debug('buildJoinPointList() - avp: %s nearp: %s' % \
                (avPos, nearestP))

        # See if destPos is the closest point
        dist = Vec3(avPos - destPos).length()
        if (dist < minDist):
            self.notify.debug('buildJoinPointList() - destPos is nearest')
            return []

        if (toon == 1):
            if (nearestP == BattleBase.posE):
                self.notify.debug('buildJoinPointList() - posE')
                plist = [BattleBase.posE] 
            elif (BattleBase.toonCwise.count(nearestP) == 1):
                self.notify.debug('buildJoinPointList() - clockwise')
                index = BattleBase.toonCwise.index(nearestP)
                plist = BattleBase.toonCwise[index+1:]
            else:
                self.notify.debug('buildJoinPointList() - counter-clockwise')
                assert(BattleBase.toonCCwise.count(nearestP) == 1)
                index = BattleBase.toonCCwise.index(nearestP)
                plist = BattleBase.toonCCwise[index+1:]
        else:
            if (nearestP == BattleBase.posA):
                self.notify.debug('buildJoinPointList() - posA')
                plist = [BattleBase.posA]
            elif (BattleBase.suitCwise.count(nearestP) == 1):
                self.notify.debug('buildJoinPointList() - clockwise')
                index = BattleBase.suitCwise.index(nearestP)
                plist = BattleBase.suitCwise[index+1:]
            else:
                self.notify.debug('buildJoinPointList() - counter-clockwise')
                assert(BattleBase.suitCCwise.count(nearestP) == 1)
                index = BattleBase.suitCCwise.index(nearestP)
                plist = BattleBase.suitCCwise[index+1:]

        self.notify.debug('buildJoinPointList() - plist: %s' % plist)
        return plist

    def addHelpfulToon(self, toonId):
        """Add toonId to our helpful toons, make sure it's in the list at most once."""
        if toonId not in self.helpfulToons:
            self.helpfulToons.append(toonId)
        
