# CannonGameGlobals.py: contains cannon game stuff
# used by AI and client

TowerYRange = 200

GameTime = 90

MAX_SCORE = 23
MIN_SCORE = 5

# it takes this many seconds for a cannon to shoot
#FUSE_TIME = 2.
FUSE_TIME = 0.

# AI needs to validate inputs to these ranges
CANNON_ROTATION_MIN = -20
CANNON_ROTATION_MAX = 20
CANNON_ROTATION_VEL = 15.0 # move 15 units every second

CANNON_ANGLE_MIN = 10
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0

def calcScore(t):
    """ t: time in seconds since game start """
    range = MAX_SCORE - MIN_SCORE
    score = MAX_SCORE - (range * (float(t) / GameTime))
    return int(score + .5)
