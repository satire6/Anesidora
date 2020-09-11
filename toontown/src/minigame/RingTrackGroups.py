"""RingTrackGroups.py: contains various Ring Game ring track groups"""

import math
import RingGameGlobals
import RingAction
import RingTracks
import RingTrack
import RingTrackGroup
from direct.showbase import PythonUtil

# ringTrackGroup types/difficulty levels
STATIC = 0  # stationary rings
SIMPLE = 1  # simple ring motions
COMPLEX = 2 # complex ring motions
def getRandomRingTrackGroup(type, numRings, rng):
    """
    getRandomRingTrackGroup(STATIC|SIMPLE|COMPLEX, int, rng)
    call this function to get a randomly-generated ringTrackGroup
    of a specific type (aka difficulty level)
    """
    #numRings = 2 #######
    funcTable = trackListGenFuncs[type][numRings-1]
    func = rng.choice(funcTable)
    #func = get_plus_FASTER #######
    tracks, tOffsets, period = func(numRings, rng)
    tracks, tOffsets = __scramble(tracks, tOffsets, rng)
    trackGroup = RingTrackGroup.RingTrackGroup(tracks, period,
                                   trackTOffsets = tOffsets,
                                   reverseFlag = rng.choice([0,1]),
                                   tOffset = rng.random())
    return trackGroup

#### UTIL
def __scramble(tracks, tOffsets, rng):
    """__scramble(list of tracks, list of track offsets(0..1), rng)
    uses rng to re-order tracks in random order"""
    assert(len(tracks) >= 1 and len(tracks) <= 4)
    newTracks = []
    # tOffsets might be None
    if tOffsets == None:
        newTOffsets = None
    else:
        assert(len(tracks) == len(tOffsets))
        newTOffsets = []

    used = [0] * len(tracks)
    count = 0
    while count < len(tracks):
        i = rng.randint(0,len(tracks)-1)
        if not used[i]:
            used[i] = 1
            count += 1
            newTracks.append(tracks[i])
            if newTOffsets != None:
                newTOffsets.append(tOffsets[i])

    return newTracks, newTOffsets

def angleToXY(angle, radius = 1.):
    """returns an x,y pair given an angle and a radius"""
    return [radius * math.sin(angle),
            radius * math.cos(angle)]

def getTightCircleStaticPositions(numRings):
    """
    produces N evenly-spaced positions on a small, zero-centered circle
    returns a list of [x,y] pairs
    """
    assert(numRings >= 1 and numRings <= 4)
    positions = []
    if numRings == 1:
        positions.append([0,0])
    else:
        radius = RingGameGlobals.RING_RADIUS * 1.5 / RingGameGlobals.MAX_TOONXZ
        step = 2.*math.pi / float(numRings)
        for i in range(0,numRings):
            angle = (i * step) + (step / 2.)
            positions.append(angleToXY(angle,
                                       1./3.))
    return positions


#### STATIC RINGTRACKGROUP FUNCTIONS
def get_keypad(numRings, rng):
    """places rings at the 9 'keypad' positions"""
    positions = (
        RingTracks.center,
        RingTracks.up, RingTracks.down,
        RingTracks.left, RingTracks.right,
        RingTracks.ul, RingTracks.ur,
        RingTracks.lr, RingTracks.ll,
        )
    tracks = []
    usedPositions = [None,]
    posScale = 0.7 + (rng.random() * 0.2)
    for i in range(0, numRings):
        # choose an unused position
        pos = None
        while pos in usedPositions:
            pos = rng.choice(positions)
        usedPositions.append(pos)

        # scale the positions
        scaledPos = [0,0]
        scaledPos[0] = pos[0] * posScale
        scaledPos[1] = pos[1] * posScale
        action = RingAction.RingActionStaticPos(scaledPos)
        track = RingTrack.RingTrack([action], [1.])
        tracks.append(track)

    # no per-track time offsets; period doesn't matter either
    return tracks, None, 1.

#### SIMPLE RINGTRACKGROUP FUNCTIONS
# some default pattern periods
fullCirclePeriod = 6.
plusPeriod = 4.

def get_evenCircle(numRings, rng):
    """make the rings move in a circle, evenly spaced"""
    tracks = []
    tOffsets = []
    for i in range(0, numRings):
        actions, durations = RingTracks.getCircleRingActions()
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)
        tOffsets.append(float(i)/numRings)

    return tracks, tOffsets, fullCirclePeriod

def get_followCircle(numRings, rng):
    """make the rings follow each other closely in a circle"""
    tracks = []
    tOffsets = []
    for i in range(0, numRings):
        actions, durations = RingTracks.getCircleRingActions()
        track = RingTrack.RingTrack(actions, durations)
        delay = 0.12
        tracks.append(track)
        tOffsets.append(float(i)*delay)

    return tracks, tOffsets, fullCirclePeriod

def get_evenCircle_withStationaryCenterRings(numRings, rng):
    """make some rings move in a circle, evenly spaced,
    with others in a small, stationary circle around (0,0)"""
    tracks = []
    tOffsets = []
    numCenterRings = rng.randint(1,numRings-1)
    # add the stationary center rings
    positions = getTightCircleStaticPositions(numCenterRings)
    for i in range(0, numCenterRings):
        action = RingAction.RingActionStaticPos(positions[i])
        track = RingTrack.RingTrack([action])
        tracks.append(track)
        tOffsets.append(0)

    numOuterRings = numRings - numCenterRings
    for i in range(0, numOuterRings):
        actions, durations = RingTracks.getCircleRingActions()
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)
        tOffsets.append(float(i)/numOuterRings)

    return tracks, tOffsets, fullCirclePeriod

def __get_Slots(numRings, rng, vertical=1):
    tracks = []
    tOffsets = []

    # calculate fixed positions (X for vertical, Y for horizontal)
    fpTab = []
    for i in range(numRings):
        fpTab.append(PythonUtil.lineupPos(i, numRings, 2./3))
    # move all of the fixed positions by a random amount,
    # staying within bounds
    offset = 1 - fpTab[-1]
    offset = (rng.random() * (offset*2)) - offset
    fpTab = map(lambda x: x+offset, fpTab)
    
    for i in range(0,numRings):
        if vertical:
            getActionsFunc = RingTracks.getVerticalSlotActions
        else:
            getActionsFunc = RingTracks.getHorizontalSlotActions
        actions, durations = getActionsFunc(fpTab[i])
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)
        tOffsets.append((float(i)/numRings) * .5)

    return tracks, tOffsets, fullCirclePeriod

def get_verticalSlots(numRings, rng):
    """make rings oscillate straight up and down, spaced apart
    uniformly in X"""
    return __get_Slots(numRings, rng, vertical=1)

def get_horizontalSlots(numRings, rng):
    """make rings oscillate left and right, spaced apart
    uniformly in Y"""
    return __get_Slots(numRings, rng, vertical=0)

def get_plus(numRings, rng):
    """make rings move in and out from center in a plus pattern"""
    up = RingTracks.getPlusUpRingActions
    down = RingTracks.getPlusDownRingActions
    left = RingTracks.getPlusLeftRingActions
    right = RingTracks.getPlusRightRingActions

    actionSets = {
        # this pattern is not used for 1 ring
        2: [[up, down],
            [left, right]],
        3: [[up, left, right],
            [left, up, down],
            [down, left, right],
            [right, up, down]],
        4: [[up, down, left, right]],
        }

    tracks = []
    actionSet = rng.choice(actionSets[numRings])
    for i in range(0, numRings):
        actions, durations = actionSet[i]()
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)

    return tracks, [0] * numRings, plusPeriod

#### COMPLEX RINGTRACKGROUP FUNCTIONS
infinityPeriod = 5.
fullCirclePeriodFaster = 5.
plusPeriodFaster = 2.5

# stagger the rings so they don't interpenetrate
infinityTOffsets = []
def __initInfinityTOffsets():
    offsets = [[],[],[],[]]
    offsets[0] = [0.]
    offsets[1] = [0.,3./4.]
    offsets[2] = [0.,1./3.,2./3.]

    inc = 14./23. # 0.6087; this works.
    #inc = 0.61    # pretty good
    #inc = 19./31. # 0.6129; decent
    for numRings in range(4,5):
        o = [0] * numRings
        accum = 0.
        for i in range(0,numRings):
            o[i] = accum % 1.
            accum += inc
        offsets[numRings-1] = o

    global infinityTOffsets
    infinityTOffsets = offsets
__initInfinityTOffsets()

def get_vertInfinity(numRings, rng):
    """make the rings move in an 8 pattern"""
    tracks = []
    for i in range(0, numRings):
        actions, durations = RingTracks.getVerticalInfinityRingActions()
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)

    return tracks, infinityTOffsets[numRings-1], infinityPeriod

def get_horizInfinity(numRings, rng):
    """make the rings move in a sideways 8 pattern"""
    tracks = []
    for i in range(0, numRings):
        actions, durations = RingTracks.getHorizontalInfinityRingActions()
        track = RingTrack.RingTrack(actions, durations)
        tracks.append(track)

    return tracks, infinityTOffsets[numRings-1], infinityPeriod

def get_evenCircle_withStationaryCenterRings_FASTER(numRings, rng):
    tracks, tOffsets, period = \
        get_evenCircle_withStationaryCenterRings(numRings, rng)
    return tracks, tOffsets, fullCirclePeriodFaster

def get_plus_FASTER(numRings, rng):
    tracks, tOffsets, period = get_plus(numRings, rng)
    return tracks, tOffsets, plusPeriodFaster

########
# TRACK LIST GENERATION FUNC TABLES
allFuncs = [
    [ # static
      get_keypad,
    ],
    [ # simple
      get_evenCircle,
      get_followCircle,
      get_evenCircle_withStationaryCenterRings,
      get_verticalSlots,
      get_horizontalSlots,
      get_plus,
    ],
    [ # complex
      get_vertInfinity,
      get_horizInfinity,
      get_evenCircle_withStationaryCenterRings_FASTER,
      get_plus_FASTER,
    ],
    ]

dontUseFuncs = [
    [ # 1 ring
      get_followCircle,
      get_evenCircle_withStationaryCenterRings,
      get_evenCircle_withStationaryCenterRings_FASTER,
      get_plus,
      get_plus_FASTER,
    ],
    [ # 2 rings
    ],
    [ # 3 rings
    ],
    [ # 4 rings
    ],
    ]

# this will hold the static, simple, and complex functions that should
# be used to generate track lists, given a particular number of rings
#
# i.e. to generate a simple pattern with two rings, choose from
# the trackListGenFuncs[SIMPLE][1] list
trackListGenFuncs = []

def __listComplement(list1, list2):
    """remove list2 members from list1"""
    result = []
    for item in list1:
        if not item in list2:
            result.append(item)
    return result

def __initFuncTables():
    """initialize the function tables
    we maintain tables of track-list-creation functions
    there are separate lists of functions for each possible number
    of rings (1..4)
    """
    # create entries for STATIC, SIMPLE, and COMPLEX
    table = [[],[],[],]
    # for each difficulty level...
    for diff in range(0,len(table)):
        # create entries for 4 different numbers of rings
        table[diff] = [[],[],[],[],]
        # for each number of rings...
        for numRings in range(0,len(table[diff])):
            # make a list of funcs for this difficulty level and
            # this number of rings
            # remove the functions that we shouldn't use for this # of rings
            table[diff][numRings] = __listComplement(allFuncs[diff],
                                                     dontUseFuncs[numRings])

    global trackListGenFuncs
    trackListGenFuncs = table

# initialize the function tables once
__initFuncTables()
