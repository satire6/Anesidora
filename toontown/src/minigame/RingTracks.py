"""RingTracks.py: contains various Ring Game ring tracks"""

import math
import RingTrack
import RingAction

center = (0,0)
up    = ( 0, 1)
down  = ( 0,-1)
left  = (-1, 0)
right = ( 1, 0)
ul = (-1, 1) # upper-left
ur = ( 1, 1) # upper-right
lr = ( 1,-1) # lower-right
ll = (-1,-1) # lower-left

### these can be used as ringTrack position functions
def ringLerp(t, a,b):
    """lerps between two 2d points; a,b are pairs: (x,y)"""
    assert(type(t) == type(0.))
    omT = 1.-t
    return ((float(a[0])*omT) + (float(b[0])*t), \
            (float(a[1])*omT) + (float(b[1])*t))

def ringClerp(t, a,b):
    """cubically lerps between two 2d points; a,b are pairs: (x,y)"""
    assert(type(t) == type(0.))
    return ringLerp(t*t*(3-(2*t)), a,b)

## call these functions to get 'canned' ring action lists
def getSquareRingActions():
    return (
        [
        RingAction.RingActionFunction(ringClerp, [ul,ur]), # ul to ur
        RingAction.RingActionFunction(ringClerp, [ur,lr]), # ur to lr
        RingAction.RingActionFunction(ringClerp, [lr,ll]), # lr to ll
        RingAction.RingActionFunction(ringClerp, [ll,ul]), # ll to ul
        ],
        [0.25,0.25,0.25,0.25],
        )

def getVerticalSlotActions(x):
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(x,1),(x,-1)]),
        RingAction.RingActionFunction(ringClerp, [(x,-1),(x,1)]),
        ],
        [.5,.5],
        )

def getHorizontalSlotActions(y):
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(1,y),(-1,y)]),
        RingAction.RingActionFunction(ringClerp, [(-1,y),(1,y)]),
        ],
        [.5,.5],
        )

def getCircleRingActions():
    def circlePos(t):
        return (math.sin(t*2.*math.pi), math.cos(t*2.*math.pi))
    return (
        [
        RingAction.RingActionFunction(circlePos, []),
        ],
        [1.],
        )

def getVerticalInfinityRingActions():
    def vertInfPos(t):
        return (0.5*math.sin(2.*t*2.*math.pi), math.cos(t*2.*math.pi))
    return (
        [
        RingAction.RingActionFunction(vertInfPos, []),
        ],
        [1.],
        )

def getHorizontalInfinityRingActions():
    def horizInfPos(t):
        return (math.sin(t*2.*math.pi), 0.5*math.sin(2.*t*2.*math.pi))
    return (
        [
        RingAction.RingActionFunction(horizInfPos, []),
        ],
        [1.],
        )

RingOffset = .4
def getPlusUpRingActions():
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(0,RingOffset),(0,1)]),
        RingAction.RingActionFunction(ringClerp, [(0,1),(0,RingOffset)]),
        ],
        [.5,.5]
        )
def getPlusDownRingActions():
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(0,-RingOffset),(0,-1)]),
        RingAction.RingActionFunction(ringClerp, [(0,-1),(0,-RingOffset)]),
        ],
        [.5,.5]
        )
def getPlusRightRingActions():
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(RingOffset,0),(1,0)]),
        RingAction.RingActionFunction(ringClerp, [(1,0),(RingOffset,0)]),
        ],
        [.5,.5]
        )
def getPlusLeftRingActions():
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(-RingOffset,0),(-1,0)]),
        RingAction.RingActionFunction(ringClerp, [(-1,0),(-RingOffset,0)]),
        ],
        [.5,.5]
        )

def getHalfDomeRingActions():
    def halfDome(t):
        return (math.cos(t*math.pi), -math.sin(t*math.pi))
    x1 = -1.
    x2 = -1./3.
    x3 =  1./3.
    x4 =  1.
    return (
        [
        RingAction.RingActionFunction(ringClerp, [(x1,0),(x2,0)]),
        RingAction.RingActionFunction(ringClerp, [(x2,0),(x3,0)]),
        RingAction.RingActionFunction(ringClerp, [(x3,0),(x4,0)]),
        RingAction.RingActionFunction(halfDome, []),
        ],
        [0.25,0.25,0.25,0.25],
        )
