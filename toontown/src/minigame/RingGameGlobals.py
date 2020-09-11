"""RingGameGlobals: contains values shared by server and client ring games"""

from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

ENDLESS_GAME = config.GetBool('endless-ring-game', 0)

NUM_RING_GROUPS = 16

MAX_TOONXZ = 10. # the toon's X and Z can each vary between -10 and 10

CollisionRadius = 1.5
CollideMask = ToontownGlobals.CatchGameBitmask

# we should be able to fit four rings next to each other snugly
# in a horizontal (or vertical) line, with half of a ring hanging
# off each end.
# therefore, the playfield half-width is equivalent to 1.5 rings,
# or 3 ring radii
RING_RADIUS = (MAX_TOONXZ / 3.) * 0.9

ringColors = (
    (TTLocalizer.ColorRed,    VBase4(1.0, 0.4, 0.2, 1.0)),
    (TTLocalizer.ColorGreen,  VBase4(0.0, 0.9, 0.2, 1.0)),
    (TTLocalizer.ColorOrange, VBase4(1.0, 0.5, 0.25, 1.0)),
    (TTLocalizer.ColorPurple, VBase4(1.0, 0.0, 1.0, 1.0)),
    (TTLocalizer.ColorWhite,  VBase4(1.0, 1.0, 1.0, 1.0)),
    (TTLocalizer.ColorBlack,  VBase4(0.0, 0.0, 0.0, 1.0)),
    (TTLocalizer.ColorYellow, VBase4(1.0, 1.0, 0.2, 1.0)),
    )

# We don't want red, green, or orange to be picked for the same
# game--they're too difficult to tell apart from each other in the
# fog.  This list specifies which of the above colors should not be
# chosen together, by grouping them into a common tuple.
ringColorSelection = [(0, 1, 2), 3, 4, 5, 6]
