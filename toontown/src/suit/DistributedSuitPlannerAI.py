"""
DistributedSuitPlannerAI module:  contains the DistributedSuitPlannerAI
class which handles management of all suits within a single neighborhood.
"""

# AI code should not import ShowBaseGlobal because it creates a graphics window
# Use AIBaseGlobal instead
from otp.ai.AIBaseGlobal import *

from direct.distributed import DistributedObjectAI
import SuitPlannerBase
import DistributedSuitAI
from toontown.battle import BattleManagerAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
import SuitDNA
from toontown.battle import SuitBattleGlobals
import SuitTimings
from toontown.toon import NPCToons
from toontown.building import HQBuildingAI
from toontown.hood import ZoneUtil
from toontown.building import SuitBuildingGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
import math
import time
import random

class DistributedSuitPlannerAI(DistributedObjectAI.DistributedObjectAI,
                                SuitPlannerBase.SuitPlannerBase):
    """
    manages all suits which exist within
    a single neighborhood (or street), this includes suits in buildings.
    It handles creating suits if the neighborhood needs more, or removing
    suits if there are too many.  This object only exists on the server
    AI.
    
    Attributes:
        suitList (list), list of all suits that this planner controls
    """

    # useful constants for the DistributedSuitPlannerAI
    # various suit numbers used by each suit planner based on
    # which neighborhood it exists in
    #
#    NUM_SUITS_WHERE_IS_EVERYBODY = 0
#    NUM_SUITS_PIECE_OF_CAKE      = 1
#    NUM_SUITS_WALK_IN_THE_PARK   = 3
#    NUM_SUITS_LARGE_PILL         = 10
#    NUM_SUITS_ROUGHNECK          = 20
#    NUM_SUITS_FIGHT_THE_POWER    = 30
#    NUM_SUITS_SUITICUS_XTREMICUS = 50

    # various hood specific information that the suit
    # planner for that area will use
    # CCC for now have no suits in 2200 and 2300 since
    # these hoods have no path information
    #                  1 zone in which the associated values apply
    #
    #                  2 minimum number of suits that can exist in this hood
    #                  3 maximum number of suits that can exist in this hood
    #                    The above min/max limit on suits applies only
    #                    to suits that fly in to the zone.  Suits that
    #                    walk in from buildings are on top of this
    #                    limit, and each suit building contributes
    #                    SUIT_BUILDING_NUM_SUITS to the expected
    #                    number of suits in a particular zone.
    #
    #                  4 minimum num buildings that can exist in this hood
    #                  5 maximum num buildings that can exist in this hood
    #                    Note: the min/max number of buildings for a particular
    #                    hood should probably be left as unconstrained as
    #                    possible, to allow the "leaf-blower" system full
    #                    flexibility to dynamically adjust the number of
    #                    buildings everywhere.
    #
    #                  6 weight for chance of new suit building appearing here
    #
    #                  7 maximum number of suits in a battle
    #                  8 Percent chance that a suit will try to join a battle
    #                    based on the ratio of toons currently in the
    #                    battle to suits that have *ever* been in the
    #                    battle.  There are six possible combinations
    #                    where a suit might be able to join.
    #
    #                    Starting from the left most entry,
    #                    the first is if the suits outnumber the toons by 2,
    #                    the second is if the suits outnumber the toons by 1,
    #                    the third is if the suits and toons are balanced,
    #                    the fourth is if the toons outnumber the suits by 1,
    #                    the fifth is if the toons outnumber the suits by 2,
    #                    and the last is if the toons outnumber the suits by 3.
    #
    #                    So in general, as toons outnumber suits, the chance of
    #                    new suits joining the battle increases (at least
    #                    with the current sets of numbers).
    #
    #                  9 chance of picking from each track (corporate, legal,
    #                    money, sales ) (only used when suit does not enter
    #                    the street from a suit building)
    #                 10 all possible suit levels for this hood
    #
    # In general, we set the max suit count fairly high for
    # ToontownCentral, and relatively low for the other zones, because
    # we expect building suits to make up the difference in the other
    # zones.
    
    # how many more buildings (suit & cogdo) do we want now that there
    # are cogdos in the Tooniverse?
    CogdoPopFactor = config.GetFloat('cogdo-pop-factor', 1.5)
    CogdoRatio = min(1., max(0., config.GetFloat('cogdo-ratio', .5)))

    SuitHoodInfo = [
        # TT is heavy on l, light on c
        # Street 2100 is a particularly long street.  Lots of room for cogs.
        [ 2100,                         # ZONE
          5,                            # MIN
          15,                           # MAX
          0,                            # BMIN
          5,                            # BMAX
          20,                           # BWEIGHT
          3,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 25, 25, 25, 25 ),           # TRACK
          ( 1, 2, 3 ),                  # LVL
          [],
          ],
        [ 2200,
          3,
          10,
          0,
          5,
          15,                           # BWEIGHT
          3,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 10, 70, 10, 10 ),
          ( 1, 2, 3 ),
          [],
          ],
        [ 2300,
          3,
          10,
          0,
          5,
          15,                           # BWEIGHT
          3,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 10, 10, 40, 40 ),
          ( 1, 2, 3 ),
          [],
          ],
        
        # Donalds dock
        # DD is heavy on c (2..4), m (3..6), light on l, s
        [ 1100,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 90, 10, 0, 0 ),             # TRACK
          ( 2, 3, 4 ),                  # LVL
          [],
          ], 
        [ 1200,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 90, 10 ),
          ( 3, 4, 5, 6 ),
          [],
          ],
        [ 1300,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 40, 40, 10, 10 ),
          ( 3, 4, 5, 6 ),
          [],
          ],
        
        # The Brrrgh
        # TB is heavy on c, light on l
        [ 3100,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 90, 10, 0, 0 ),             # TRACK
          ( 5, 6, 7 ),                  # LVL
          [],
          ],
        [ 3200,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 10, 20, 30, 40 ),
          ( 5, 6, 7 ),
          [],
          ],
        [ 3300,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 5, 85, 5, 5 ),
          ( 7, 8, 9 ),
          [],
          ],
        
        # Minnies Melodyland
        # MM is heavy on m
        [ 4100,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 50, 50 ),             # TRACK
          ( 2, 3, 4 ),                  # LVL
          [],
          ],
        [ 4200,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 90, 10 ),
          ( 3, 4, 5, 6 ),
          [],
          ],
        [ 4300,
          1,
          5,
          0,
          99,
          100,                          # BWEIGHT
          4,
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 50, 50, 0, 0 ),
          ( 3, 4, 5, 6 ),
          [],
          ],
        
        # Daisy Gardens
        # DG is heavy on s (2..4), l (3..6)
        [ 5100,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 20, 10, 70 ),            # TRACK
          ( 2, 3, 4 ),                  # LVL
          [],
          ],
        [ 5200,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 10, 70, 0, 20 ),            # TRACK
          ( 3, 4, 5, 6 ),               # LVL
          [],
          ],
        [ 5300,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          # Mostly sellbot since it is connected to Sellbot HQ
          ( 5, 5, 5, 85 ),              # TRACK
          ( 3, 4, 5, 6 ),               # LVL
          [],
          ],
        
        # Dreamland
        [ 9100,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 25, 25, 25, 25 ),           # TRACK
          ( 6, 7, 8, 9 ),               # LVL
          [],
          ],

        [ 9200,                         # ZONE
          1,                            # MIN
          5,                            # MAX
          0,                            # BMIN
          99,                           # BMAX
          100,                          # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          # Mostly cashbot since it is connected to Cashbot HQ
          ( 5, 5, 85, 5 ),              # TRACK
          ( 6, 7, 8, 9 ),               # LVL
          [],
          ],

        # Sellbot HQ Exterior
        [ 11000,                        # ZONE
          3,                            # MIN
          15,                           # MAX
          0,                            # BMIN
          0,                            # BMAX
          0,                            # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 0, 100 ),             # TRACK
          ( 4, 5, 6 ),                  # LVL
          [],
          ],
        [ 11200,                        # ZONE
          10,                           # MIN
          20,                           # MAX
          0,                            # BMIN
          0,                            # BMAX
          0,                            # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 0, 100 ),             # TRACK
          ( 4, 5, 6 ),                  # LVL
          [],
          ],

        # Cash HQ Exterior
        [ 12000,                        # ZONE
          10,                           # MIN
          20,                           # MAX
          0,                            # BMIN
          0,                            # BMAX
          0,                            # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 0, 100, 0 ),             # TRACK
          ( 7, 8, 9 ),                  # LVL
          [],
          ],
        
        # Law HQ Exterior
        [ 13000,                        # ZONE
          10,                           # MIN
          20,                           # MAX
          0,                            # BMIN
          0,                            # BMAX
          0,                            # BWEIGHT
          4,                            # SMAX
          ( 1, 5, 10, 40, 60, 80 ),     # JCHANCE
          ( 0, 100, 0, 0 ),             # TRACK
          ( 8, 9, 10 ),                 # LVL
          [],
          ],

        ]

    # index values into the SuitHoodInfo struct above for each type of value
    #
    SUIT_HOOD_INFO_ZONE    = 0
    SUIT_HOOD_INFO_MIN     = 1
    SUIT_HOOD_INFO_MAX     = 2
    SUIT_HOOD_INFO_BMIN    = 3
    SUIT_HOOD_INFO_BMAX    = 4
    SUIT_HOOD_INFO_BWEIGHT = 5
    SUIT_HOOD_INFO_SMAX    = 6
    SUIT_HOOD_INFO_JCHANCE = 7
    SUIT_HOOD_INFO_TRACK   = 8
    SUIT_HOOD_INFO_LVL     = 9
    SUIT_HOOD_INFO_HEIGHTS = 10

    # highest available suit type (flunky, pencil pusher, etc)(1-based)
    #
    # Exclude the big guys from the streets--they live only inside
    # buildings.
    MAX_SUIT_TYPES         = 6

    # How often to upkeep and adjust suit population, in seconds.
    POP_UPKEEP_DELAY         = 10
    POP_ADJUST_DELAY         = 300

    # The time along a path, in seconds, that will be maintained
    # between any two suits for spacing.
    PATH_COLLISION_BUFFER      = 5

    # A hard maximum on the number of suits we try to put in the zone.
    # This overrides any per-zone maximum specified in the above
    # table, and also includes the count of building suits.  The main
    # purpose of this limit is to keep us from wasting resources
    # trying to squeeze 200 suits into a street where they can't
    # possibly fit.  Empirically, with PATH_COLLISION_BUFFER set to 5,
    # we can get as many as 80 suits on one of the long streets in
    # TTC, but only about 40 on some of the shorter streets.
    TOTAL_MAX_SUITS = 50
    
    # The minimum and maximum length of a path that will be acceptable
    # for a given suit assignment, in number of suit points passed.

    # MIN_PATH_LEN should be at least 2, because less than that will
    # cause the AI to crash with assertion failures and array
    # underruns.

    # The longest street is Silly Street with 192 points; a path might
    # therefore need to be as long as 192 + MIN_PATH_LEN points to
    # reach completion.  We define MAX_PATH_LEN to be 300 to give a
    # comfortable margin; setting it higher just makes it take longer
    # to discover disconnected graphs.
    MIN_PATH_LEN = 40
    MAX_PATH_LEN = 300

    # Suits on the takeover march are allowed shorter paths.
    MIN_TAKEOVER_PATH_LEN = 2

    SUITS_ENTER_BUILDINGS    = 1

    # The number of additional suits contributed to the zone by each
    # building, at any given time.  This may be a floating-point
    # number if necessary.
    SUIT_BUILDING_NUM_SUITS  = 1.5

    # Suit building timeouts.  A particular hood may only have so many
    # suit buildings.  After a building has been a suit building for a
    # length of time, it is automatically reconverted to a toon
    # building; however, this timeout is based on the number of suit
    # buildings in the block.  Thus, the more suit buildings there are
    # on a particular block, the more quickly they will reconvert to
    # toon buildings.  This is intended to prevent suit buildings from
    # accumulating in the harder streets and never getting reclaimed.

    # This table is the length of time, in *hours*, for buildings,
    # with one entry for each number of buildings in the street.  None
    # means no timeout.
    
    SUIT_BUILDING_TIMEOUT = [
        None, None, None, None, None, None,   # 0 - 5 buildings: no timeout
        72, 60, 48, 36, 24,                   # 6 - 10 buildings
        12, 6, 3, 1, 0.5,                     # 11 - 15 and higher
        ]

    # How many suit buildings should there be in the whole world at
    # any given time?  This is expressed as a percentage of the total
    # number of buildings.
    TOTAL_SUIT_BUILDING_PCT  = 18 * CogdoPopFactor

    # What is the balance of suit building heights in the world?  The
    # SuitPlanner will attempt to keep this relative weighted ratio of
    # building heights.  For example, if the first number in the
    # following list is 12 and the second number is 24, and the sum of
    # all of the numbers in the list is 85, then 12/85 of the
    # buildings in the world will be 1-story, and 24/85 will be
    # 2-story.
    BUILDING_HEIGHT_DISTRIBUTION = [
        14, 18, 25, 23, 20
        ]

    # We need the total of all BWEIGHT values so we can compute
    # weighted chances properly.  And, we keep the total weights as
    # modified per track, for cases when we want to choose a street to
    # prefer a particular kind of suit building over any other kind.
    TOTAL_BWEIGHT = 0

    # We also need the same count, weighted by the chance of a suit of
    # a particular track appearing in that zone.  This enables us to
    # choose a suitable street to hold a building of a particular
    # track.
    TOTAL_BWEIGHT_PER_TRACK = [0, 0, 0, 0]

    # And again, weighted by the chance of a suit of an appropriate
    # level to create a building of a particular height.
    TOTAL_BWEIGHT_PER_HEIGHT = [0, 0, 0, 0, 0]
    
    for currHoodInfo in SuitHoodInfo:
        weight = currHoodInfo[SUIT_HOOD_INFO_BWEIGHT]
        tracks = currHoodInfo[SUIT_HOOD_INFO_TRACK]
        levels = currHoodInfo[SUIT_HOOD_INFO_LVL]

        # levels is the list of suit levels that may be encountered in
        # this zone.  There's an equal weight chance of each level
        # suit appearing, and each level suit makes a building of the
        # corresponding level, which has a particular chance of being
        # any of a specified number of floors.  Crunch these numbers
        # down into the overall chance of a particular building height
        # on this streeet.
        heights = [0, 0, 0, 0, 0]
        for level in levels:
            minFloors, maxFloors = SuitBuildingGlobals.SuitBuildingInfo[level - 1][0]
            # Remember that buildingHeight is numFloors - 1
            for i in range(minFloors - 1, maxFloors):
                heights[i] += 1

        # Now that we've computed this heights list, store it back on
        # the global structure for future reference.
        currHoodInfo[SUIT_HOOD_INFO_HEIGHTS] = heights
        
        TOTAL_BWEIGHT += weight
        TOTAL_BWEIGHT_PER_TRACK[0] += weight * tracks[0]
        TOTAL_BWEIGHT_PER_TRACK[1] += weight * tracks[1]
        TOTAL_BWEIGHT_PER_TRACK[2] += weight * tracks[2]
        TOTAL_BWEIGHT_PER_TRACK[3] += weight * tracks[3]

        TOTAL_BWEIGHT_PER_HEIGHT[0] += weight * heights[0]
        TOTAL_BWEIGHT_PER_HEIGHT[1] += weight * heights[1]
        TOTAL_BWEIGHT_PER_HEIGHT[2] += weight * heights[2]
        TOTAL_BWEIGHT_PER_HEIGHT[3] += weight * heights[3]
        TOTAL_BWEIGHT_PER_HEIGHT[4] += weight * heights[4]

    # This Configrc constrains the kinds of suits we might create.
    defaultSuitName = simbase.config.GetString('suit-type', 'random')
    if defaultSuitName == 'random':
        defaultSuitName = None

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitPlannerAI')

    def __init__(self, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        SuitPlannerBase.SuitPlannerBase.__init__( self )
        self.air = air
        self.zoneId = zoneId
        self.canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)

        if simbase.air.wantCogdominiums:
            # adjust building populations wrt Cogdos
            if not hasattr(self.__class__, 'CogdoPopAdjusted'):
                self.__class__.CogdoPopAdjusted = True
                for index in xrange(len(self.SuitHoodInfo)):
                    hoodInfo = self.SuitHoodInfo[index]
                    hoodInfo[self.SUIT_HOOD_INFO_BMIN] = int(.5 + (self.CogdoPopFactor *
                                                             hoodInfo[self.SUIT_HOOD_INFO_BMIN]))
                    hoodInfo[self.SUIT_HOOD_INFO_BMAX] = int(.5 + (self.CogdoPopFactor *
                                                             hoodInfo[self.SUIT_HOOD_INFO_BMAX]))

        # remember which entry in SuitHoodInfo this suit planner will be
        # using, this is based on the zone id assigned
        #
        self.hoodInfoIdx = -1
        for index in range(len(self.SuitHoodInfo)):
            currHoodInfo = self.SuitHoodInfo[index]
            if currHoodInfo[ self.SUIT_HOOD_INFO_ZONE ] == self.canonicalZoneId:
                self.hoodInfoIdx = index
        assert self.hoodInfoIdx != -1, "No hood information found in table: zoneId=%s" %zoneId

        # remember the number of suits we want in this hood
        # this could vary based on toons currently in the hood and
        # a random population range that changes over time
        # currDesired is a manual override to create a specific number
        # of suits if it is set to a valid number
        #
        self.currDesired = None
        self.baseNumSuits = \
          (self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_MIN] + \
           self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_MAX]) / 2

        # Remember the number of buildings we are assigned for this
        # particular street.  This will vary between streets as
        # buildings are reclaimed by toons to keep the global number
        # of suit buildings across the shard constant.  But, we have
        # to start out with at least the specified minimum.
        self.targetNumSuitBuildings = \
          self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_BMIN]
        if ZoneUtil.isWelcomeValley(self.zoneId):
            # For now, we won't have any suit buildings in WelcomeValley.
            # It bitches the suit ecology since the WelcomeValley zones
            # can come and go dynamically.
            self.targetNumSuitBuildings = 0

        # This records the tracks requested for the pending buildings.
        # As each building is created, it selects a track from this
        # list, if the list is nonempty.
        self.pendingBuildingTracks = []

        # Similarly, for the number of floors requested for pending
        # buildings.
        self.pendingBuildingHeights = []

        # various lists of suits, most are temporary holding lists,
        # the main list is 'suitList'
        #
        self.suitList        = []
        self.numFlyInSuits = 0
        self.numBuildingSuits = 0
        self.numAttemptingTakeover = 0

        self.zoneInfo = {}

        self.zoneIdToPointMap = None

        # This may be filled in with a list of lobby doors if this
        # happens to be a SuitPlanner for a CogHQExterior.
        self.cogHQDoors = []

        self.battleList = []

        # Create a battle manager AI for the street
        self.battleMgr = BattleManagerAI.BattleManagerAI(self.air)

        # load up the dna to fill in the suit path point information
        #
        self.setupDNA()

        if self.notify.getDebug():
            self.notify.debug( "Creating a building manager AI in zone" +
                               str( self.zoneId ) )
        self.buildingMgr = self.air.buildingManagers.get(self.zoneId)

        # tell all buildings in this building manager which suit
        # planner is in the same hood, and if the building is a
        # suit building, make sure to add it to our list of suit
        # blocks (used to find suit source and destination locations
        # when creating paths)
        #
        if self.buildingMgr:
            blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks, animBldgBlocks = self.buildingMgr.getDNABlockLists()
            for currBlock in blocks:
                bldg = self.buildingMgr.getBuilding( currBlock )
                bldg.setSuitPlannerExt( self )
            for currBlock in animBldgBlocks:
                bldg = self.buildingMgr.getBuilding( currBlock )
                bldg.setSuitPlannerExt( self )

        # The block number to zone map was created for the building
        # and door creation.  Now that it's done, we clear the map:
        self.dnaStore.resetBlockNumbers()

        # now let all of the buildings know what path points they should
        # be associated with
        #
        self.initBuildingsAndPoints()

        # perform a simple path test to make sure we can properly
        # generate a path from two points given to us by the DNAStorage
        #
        #self.performPathTest()

        # set the suit number override if one is provided in the xrc
        #
        numSuits = simbase.config.GetInt( 'suit-count', -1 )
        if numSuits >= 0:
            self.currDesired = numSuits
        suitHood = simbase.config.GetInt( 'suits-only-in-hood', -1 )
        if suitHood >= 0:
            if self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_ZONE] != suitHood:
                self.currDesired = 0

        # an adjustment to the base desired num suits in this hood, this
        # adjustment changes gradually over time
        #
        self.suitCountAdjust          = 0

        return None

    def cleanup(self):
        """
        called before this guy is deleted, remove any
        pending tasks
        """
        # remove the task that updates the suitPlannerAI periodically
        #
        taskMgr.remove( self.taskName('sptUpkeepPopulation') )
        taskMgr.remove( self.taskName('sptAdjustPopulation') )

        for suit in self.suitList:
            suit.stopTasks()
            if suit.isGenerated():
                self.zoneChange(suit, suit.zoneId)
                suit.requestDelete()

        self.suitList = []
        self.numFlyInSuits = 0
        self.numBuildingSuits = 0
        self.numAttemptingTakeover = 0


    def delete(self):
        self.cleanup()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def initBuildingsAndPoints(self):
        """
        let all the buildings know about the suit path
        points that are in front of them, this way the suit
        planner can ask the building for path points which
        suits can use to enter and exit the building
        """
        if not self.buildingMgr:
            return
        if self.notify.getDebug():
            self.notify.debug( "Initializing building points" )

        # We need to associate buildings with their doors.  This just
        # builds a reverse lookup based on the data we already
        # extracted from the DNA file.  Each building should have
        # one front door and one or more side doors.

        self.buildingFrontDoors = {}
        self.buildingSideDoors = {}

        for p in self.frontdoorPointList:
            blockNumber = p.getLandmarkBuildingIndex()
            if p < 0:
                self.notify.warning("No landmark building for (%s) in zone %d" % (repr(p), self.zoneId))

            elif self.buildingFrontDoors.has_key(blockNumber):
                self.notify.warning("Multiple front doors for building %d in zone %d" % (blockNumber, self.zoneId))

            else:
                self.buildingFrontDoors[blockNumber] = p

        for p in self.sidedoorPointList:
            blockNumber = p.getLandmarkBuildingIndex()
            if p < 0:
                self.notify.warning("No landmark building for (%s) in zone %d" % (repr(p), self.zoneId))

            elif self.buildingSideDoors.has_key(blockNumber):
                self.buildingSideDoors[blockNumber].append(p)
            else:
                self.buildingSideDoors[blockNumber] = [p]

        # Now make sure that each building has *at least* one of each
        # kind of door.
        for bldg in self.buildingMgr.getBuildings():
            if isinstance(bldg, HQBuildingAI.HQBuildingAI):
                # Move to the next one
                continue
            blockNumber = bldg.getBlock()[0]
            if not self.buildingFrontDoors.has_key(blockNumber):
                self.notify.warning("No front door for building %d in zone %d" % (blockNumber, self.zoneId))
            if not self.buildingSideDoors.has_key(blockNumber):
                self.notify.warning("No side door for building %d in zone %d" % (blockNumber, self.zoneId))
                

    def countNumSuitsPerTrack(self, count):
        """
        countNumSuitsPerTrack(self, map count)

        Given that count is a map of track letters to counts, e.g. {
        'c':0, 'l':0, 'm':0, 's':0 }, or an empty map, increment each
        count corresponding to the number of suits of that type in the
        neighborhood.  This is only used for magic word fulfillment
        and debug output.
        """
        for suit in self.suitList:
            if count.has_key(suit.track):
                count[suit.track] += 1
            else:
                count[suit.track] = 1

    def countNumBuildingsPerTrack(self, count):
        """
        countNumBuildingsPerTrack(self, map count)

        Given that count is a map of track letters to counts, e.g. {
        'c':0, 'l':0, 'm':0, 's':0 }, or an empty map, increment each
        count corresponding to the number of suit buildings of that
        type in the neighborhood.
        """
        if self.buildingMgr:
            for building in self.buildingMgr.getBuildings():
                if building.isSuitBuilding():
                    if count.has_key(building.track):
                        count[building.track] += 1
                    else:
                        count[building.track] = 1

    def countNumBuildingsPerHeight(self, count):
        """
        countNumBuildingsPerHeight(self, map count)

        Given that count is a map of heights to counts, e.g. { 0:0,
        1:0, 2:0, 3:0, 4:0 }, or an empty map, increment each count
        corresponding to the number of suit buildings of that height
        in the neighborhood.

        Note that the building "height" is the zero-based index into
        the number of floors: height = numFloors - 1.
        """
        if self.buildingMgr:
            for building in self.buildingMgr.getBuildings():
                if building.isSuitBuilding():
                    # buildingHeight is numFloors - 1
                    height = building.numFloors - 1
                    if count.has_key(height):
                        count[height] += 1
                    else:
                        count[height] = 1

    def formatNumSuitsPerTrack(self, count):
        """
        formatNumSuitsPerTrack(self, map count)

        Given a map filled in by a previous call to
        countNumSuitsPerTrack() or countNumBuildingsPerTrack(),
        formats the result as a string.
        """
        result = " "
        for track, num in count.items():
            result += " %s:%d" % (track, num)

        return result[2:]

    def calcDesiredNumFlyInSuits(self):
        """
        Returns the number of fly-in suits that should be walking
        around the neighborhood.
        """

        # first check to see if a manual suit count override has been
        # specified, if not, return base number of suits plus any
        # previously calculated adjustment
        #
        if self.currDesired != None:
            return 0
        return self.baseNumSuits + self.suitCountAdjust

    def calcDesiredNumBuildingSuits(self):
        """
        Returns the number of building suits that should be walking
        around the neighborhood.
        """

        if self.currDesired != None:
            return self.currDesired
        if not self.buildingMgr:
            return 0
        suitBuildings = self.buildingMgr.getEstablishedSuitBlocks()
        return int(len(suitBuildings) * self.SUIT_BUILDING_NUM_SUITS)


    def getZoneIdToPointMap(self):
        """
        Creates a reverse lookup from street zoneId's to lists of
        DNASuitPoints.  This is only used for magic word fulfillment,
        so the map isn't created until it is demanded.  It's fairly
        expensive to create this map, since the points aren't really
        designed to be looked up this way.
        """
        if self.zoneIdToPointMap != None:
            return self.zoneIdToPointMap

        self.zoneIdToPointMap = {}

        for point in self.streetPointList:
            # Determine the zones the point intersects by pulling out
            # all the points adjacent to this one.
            points = self.dnaStore.getAdjacentPoints(point)
            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                p = self.pointIndexes[pi]
                i -= 1

                zoneName = self.dnaStore.getSuitEdgeZone(
                    point.getIndex(), p.getIndex())
                zoneId = int(self.extractGroupName(zoneName))

                if self.zoneIdToPointMap.has_key(zoneId):
                    self.zoneIdToPointMap[zoneId].append(point)
                else:
                    self.zoneIdToPointMap[zoneId] = [point]

        return self.zoneIdToPointMap

    def getStreetPointsForBuilding(self, blockNumber):
        """
        getStreetPointsForBuilding(self, int blockNumber)

        Returns a list of street points in front of the indicated
        building.  This function is only used for magic word
        fulfillment.
        """

        pointList = []
        if self.buildingSideDoors.has_key(blockNumber):
            for doorPoint in self.buildingSideDoors[blockNumber]:
                # given the door point, find the street points in
                # front of it.
                points = self.dnaStore.getAdjacentPoints(doorPoint)

                i = points.getNumPoints() - 1
                while i >= 0:
                    pi = points.getPointIndex(i)
                    point = self.pointIndexes[pi]
                    if point.getPointType() == DNASuitPoint.STREETPOINT:
                        pointList.append(point)
                    i -= 1

        if self.buildingFrontDoors.has_key(blockNumber):
            doorPoint = self.buildingFrontDoors[blockNumber]
            points = self.dnaStore.getAdjacentPoints(doorPoint)

            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                pointList.append(self.pointIndexes[pi])
                i -= 1

        return pointList

    def createNewSuit(self, blockNumbers, streetPoints,
                      toonBlockTakeover = None,
                      cogdoTakeover = None,
                      minPathLen = None,
                      maxPathLen = None,
                      buildingHeight = None,
                      suitLevel = None,
                      suitType = None,
                      suitTrack = None,
                      suitName = None,
                      skelecog = None,
                      revives = None):

        """
        createNewSuit(self, list blockNumbers, list streetPoints)

        Chooses a suitable point from streetPoints (if the list is
        nonempty), or a suit building from blockNumbers, in which to
        create the suit.  Removes unsuitable points from either array.
        If no suitable point or building can be found, returns 0.

        If a suitable starting point is found, creates a new suit and
        starts it walking around.  If the starting point is from the
        streetPoints, the street is flown in from the sky; otherwise,
        it walks out of the chosen building.

        The return value is the suit if one is created, or None otherwise.

        The additional keyword arguments are primarily for the benefit
        of magic words to create suits for special purposes.
        toonBlockTakeover, if specified, is the block number of a toon
        building to take over specifically.  minPathLen and maxPathLen
        put limits on the length of the suit's path, in number of suit
        points.  suitLevel, suitType, and suitTrack define the
        particular kind of suit to create; otherwise, a random suit is
        chosen based on the neighborhood parameters.  suitName is
        another way to specify a type of suit; it may be any of the
        one- or two-letter suit codes, like 'pp' or 'ym'.
        """
        # First, choose a good starting point for the suit.
        startPoint = None
        blockNumber = None

        if self.notify.getDebug():
            self.notify.debug("Choosing origin from %d+%d possibles." % (len(streetPoints), len(blockNumbers)))

        # First, try to create a from-building suit.
        while startPoint == None and len(blockNumbers) > 0:
            bn = random.choice(blockNumbers)
            blockNumbers.remove(bn)

            if self.buildingSideDoors.has_key(bn):
                for doorPoint in self.buildingSideDoors[bn]:
                    # given the door point, find the street points in
                    # front of it.
                    points = self.dnaStore.getAdjacentPoints(doorPoint)

                    # Now iterate through all the street points.
                    # We'll count down from the end just because
                    # that's easier.
                    i = points.getNumPoints() - 1
                    while blockNumber == None and i >= 0:
                        pi = points.getPointIndex(i)
                        p = self.pointIndexes[pi]
                        i -= 1
                        
                        # Now include the travel time from the door point
                        # to the street.
                        startTime = SuitTimings.fromSuitBuilding
                        startTime += self.dnaStore.getSuitEdgeTravelTime(
                            doorPoint.getIndex(), pi,
                            self.suitWalkSpeed)                    

                        if not self.pointCollision(p, doorPoint, startTime):
                            # reset the start time back to our first point.
                            startTime = SuitTimings.fromSuitBuilding
                            startPoint = doorPoint
                            blockNumber = bn


        # Failing that, just fly a suit in.
        while startPoint == None and len(streetPoints) > 0:
            p = random.choice(streetPoints)
            streetPoints.remove(p)

            if not self.pointCollision(p, None, SuitTimings.fromSky):
                startPoint = p
                startTime = SuitTimings.fromSky

        if startPoint == None:
            return None
        
        newSuit = DistributedSuitAI.DistributedSuitAI(simbase.air, self)
        newSuit.startPoint = startPoint

        if blockNumber != None:
            # The suit originates from a building.  This also means it
            # inherits the building's track.
            newSuit.buildingSuit = 1
            if suitTrack == None:
                suitTrack = self.buildingMgr.getBuildingTrack(blockNumber)

        else:
            # The suit flies in from the sky.
            newSuit.flyInSuit = 1

            # Only fly-in suits may attempt building takeovers.  This
            # helps preserve the balance of building tracks on a
            # particular street.  If we did not do this, once a
            # particular building track got a toehold it would have an
            # advantage over the other tracks.
            newSuit.attemptingTakeover = self.newSuitShouldAttemptTakeover()

            if newSuit.attemptingTakeover:
                # Also, if he's attempting a takeover, make him be a
                # suitable track.
                if suitTrack == None and len(self.pendingBuildingTracks) > 0:
                    suitTrack = self.pendingBuildingTracks[0]

                    # Move the suitTrack to the end of the queue, so
                    # the next suit will choose a different track.  We
                    # can't remove it from the queue until the
                    # building actually gets created.
                    del self.pendingBuildingTracks[0]
                    self.pendingBuildingTracks.append(suitTrack)

                if buildingHeight == None and len(self.pendingBuildingHeights) > 0:
                    buildingHeight = self.pendingBuildingHeights[0]
                    del self.pendingBuildingHeights[0]
                    self.pendingBuildingHeights.append(buildingHeight)

        # If we're constrained to create only a particular type of
        # suit, do so.
        if suitName == None:
            # If there is an invasion, the suit name will be picked for us
            suitName, skelecog = self.air.suitInvasionManager.getInvadingCog()
            # If we are still at none, use the default suit 
            if suitName == None:
                suitName = self.defaultSuitName
        
        if suitType == None and suitName != None:
            suitType = SuitDNA.getSuitType(suitName)
            suitTrack = SuitDNA.getSuitDept(suitName)

        if suitLevel == None and buildingHeight != None:
            # Choose an appropriate level suit that will make a
            # building of the requested height.
            suitLevel = self.chooseSuitLevel(self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_LVL],
                                             buildingHeight)
            
        # Now fill in the level, type, and track parameters that
        # haven't been specified yet.
        suitLevel, suitType, suitTrack = \
                   self.pickLevelTypeAndTrack(suitLevel, suitType, suitTrack)
        newSuit.setupSuitDNA(suitLevel, suitType, suitTrack)
        newSuit.buildingHeight = buildingHeight
        
        gotDestination = self.chooseDestination(
            newSuit, startTime,
            toonBlockTakeover = toonBlockTakeover,
            cogdoTakeover = cogdoTakeover,
            minPathLen = minPathLen,
            maxPathLen = maxPathLen)
            
        
        if not gotDestination:
            # No good destination, for some reason.  Delete the suit
            # and return 0 to try again.
            self.notify.debug("Couldn't get a destination in %d!" % (self.zoneId))
            newSuit.doNotDeallocateChannel=None # This is a hack.  See Joe for details.
            newSuit.delete()
            return None

        # Initialize all the path information for passing down to
        # clients.
        newSuit.initializePath()

        # be sure to flag the zone change when this suit is first
        # created
        self.zoneChange(newSuit, None, newSuit.zoneId)

        # if this suit is a skeleton...
        if skelecog:
            newSuit.setSkelecog(skelecog)
            
        # if this suit is a skeleton 2.0...
        if revives:
            newSuit.setSkeleRevives(revives)

        # call 'generate' to create all versions of this suit,
        # including the local server side version, as well as all of
        # the client side versions, this also creates the suit's
        # unique distributed object id
        newSuit.generateWithRequired(newSuit.zoneId)

        # And now we can start the suit walking.
        newSuit.moveToNextLeg(None)

        # now add the suit to our list so we can do things with it when
        # needed
        #
        self.suitList.append(newSuit)

        if newSuit.flyInSuit:
            self.numFlyInSuits += 1

        if newSuit.buildingSuit:
            self.numBuildingSuits += 1

        if newSuit.attemptingTakeover:
            self.numAttemptingTakeover += 1

        return newSuit

    def countNumNeededBuildings(self):
        """
        Returns the number of additional suit buildings we want to try
        to take over.
        """
        if not self.buildingMgr:
            return 0
        numSuitBuildings = len(self.buildingMgr.getSuitBlocks())
        numNeeded = self.targetNumSuitBuildings - numSuitBuildings

        return numNeeded

    def newSuitShouldAttemptTakeover(self):
        """
        Decides whether it is time for a newly-created suit to attempt
        to take over an innocent toon building.  Returns true if so,
        false otherwise.
        """
        if not self.SUITS_ENTER_BUILDINGS:
            return 0

        numNeeded = self.countNumNeededBuildings()

        if self.numAttemptingTakeover >= numNeeded:
            # There's already enough suits on the march.  Never mind.
            self.pendingBuildingTracks = []
            return 0

        self.notify.debug("DSP %d is planning a takeover attempt in zone %d" % (self.getDoId(), self.zoneId))
        return 1


    def chooseDestination(self, suit, startTime,
                          toonBlockTakeover = None,
                          cogdoTakeover = None,
                          minPathLen = None,
                          maxPathLen = None):
        """
        chooseDestination(self, DistributedSuitAI suit, float startTime)

        Given that the suit has already been assigned a starting point
        (suit.startPoint) and that it has already decided whether it
        will attempt to take over a toon building
        (suit.attemptingTakeover), choose a suitable destination point
        for the suit.

        startTime is the number of seconds from now at which the suit
        will start on the path.  This is needed to properly separate
        the suit from other suits.

        The return value is true if a path can be found, or false if not.
        """
        # First, build up the list of all of our possible destinations.
        possibles = []
        backup = []

        if cogdoTakeover is None:
            cogdoTakeover = False

        if toonBlockTakeover != None:
            # The suit is specifically charged with taking over this
            # particular toon building.  This will only happen due to
            # a magic word or something.
            suit.attemptingTakeover = 1

            blockNumber = toonBlockTakeover
            if self.buildingFrontDoors.has_key(blockNumber):
                possibles.append((blockNumber, self.buildingFrontDoors[blockNumber]))
        elif suit.attemptingTakeover:

            # We have all of the toon buildings to choose from, except
            # for the "protected" buildings.
            for blockNumber in self.buildingMgr.getToonBlocks():

                building = self.buildingMgr.getBuilding(blockNumber)
                extZoneId, intZoneId = building.getExteriorAndInteriorZoneId()
            
                if not NPCToons.isZoneProtected(intZoneId):
                    if self.buildingFrontDoors.has_key(blockNumber):
                        possibles.append((blockNumber, self.buildingFrontDoors[blockNumber]))
        else:
            # We have all of the suit buildings that match our DNA
            # track to choose from (corporate suits don't mingle with
            # legal suits), as well as all points in the street.

            if self.buildingMgr:
                for blockNumber in self.buildingMgr.getSuitBlocks():
                    track = self.buildingMgr.getBuildingTrack(blockNumber)
                    if track == suit.track and \
                       self.buildingSideDoors.has_key(blockNumber):
                        for doorPoint in self.buildingSideDoors[blockNumber]:
                            possibles.append((blockNumber, doorPoint))

            # Suits always prefer to walk into suit buildings, if they
            # can find one.  If there aren't any suit buildings to
            # choose from, they'll pick a point on the street to walk
            # to, then fly away from there.
            backup = []
            for p in self.streetPointList:
                backup.append((None, p))

        if self.notify.getDebug():
            self.notify.debug("Choosing destination point from %d+%d possibles." % (len(possibles), len(backup)))

        if len(possibles) == 0:
            possibles = backup
            backup = []

        if minPathLen == None:
            if suit.attemptingTakeover:
                minPathLen = self.MIN_TAKEOVER_PATH_LEN
            else:
                minPathLen = self.MIN_PATH_LEN
        if maxPathLen == None:
            maxPathLen = self.MAX_PATH_LEN

        # Now pull destinations out at random, one at a time, until
        # we're happy with the resulting path.
        retryCount = 0
        while len(possibles) > 0 and retryCount < 50:
            p = random.choice(possibles)
            possibles.remove(p)

            if len(possibles) == 0:
                possibles = backup
                backup = []

            path = self.genPath(suit.startPoint, p[1], minPathLen, maxPathLen)
            if path and not self.pathCollision(path, startTime):
                # The path looks good; take it!
                suit.endPoint = p[1]
                suit.minPathLen = minPathLen
                suit.maxPathLen = maxPathLen
                suit.buildingDestination = p[0]
                suit.buildingDestinationIsCogdo = cogdoTakeover
                suit.setPath(path)
                return 1

            retryCount += 1

        # None of our destinations were suitable.  Probably there was
        # a battle going on very near our starting point, trapping us
        # in a corner or something.
        return 0

    def pathCollision(self, path, elapsedTime):
        """pathCollision(self, DNASuitPath path)

        Returns true if the path is unsuitable because another suit
        will be walking too close by its first point in elapsedTime
        seconds or if there is a battle there right now, or false
        otherwise.
        """
        # Get the first street point in the path, and the point just
        # before that.
        pathLength = path.getNumPoints()

        i = 0
        assert i < pathLength
        pi = path.getPointIndex(i)
        point = self.pointIndexes[pi]

        # Start off with adjacentPoint indicating the second point in
        # the path, in case the first point happens to be a street
        # point.
        adjacentPoint = self.pointIndexes[path.getPointIndex(i + 1)]

        while point.getPointType() == DNASuitPoint.FRONTDOORPOINT or \
              point.getPointType() == DNASuitPoint.SIDEDOORPOINT:
            i += 1
            assert i < pathLength

            lastPi = pi
            pi = path.getPointIndex(i)
            adjacentPoint = point
            point = self.pointIndexes[pi]

            elapsedTime += self.dnaStore.getSuitEdgeTravelTime(
                lastPi, pi, self.suitWalkSpeed)

        result = self.pointCollision(point, adjacentPoint, elapsedTime)

        return result


    def pointCollision(self, point, adjacentPoint, elapsedTime):
        """pointCollision(self, DNASuitPoint point, DNASuitPoint adjacentPoint,
                          float elapsedTime)

        Returns true if the point is unsuitable for starting a path
        because another suit will be walking right there in
        elapsedTime seconds, or if there is a battle there right now.
        See also pathCollision().

        If adjacentPoint is not None, it is a point adjacent to the
        point we are testing, which is used to determine what zone the
        point in question is in (for checking for battles).  If
        adjacentPoint is None, then all adjacent points will be
        checked.
        """
        for suit in self.suitList:
            if suit.pointInMyPath(point, elapsedTime):
                return 1

        if adjacentPoint != None:
            return self.battleCollision(point, adjacentPoint)

        else:
            # Go through all the points adjacent to the indicated one.
            # If there's a battle in any of these, it counts.

            points = self.dnaStore.getAdjacentPoints(point)
            i = points.getNumPoints() - 1
            while i >= 0:
                pi = points.getPointIndex(i)
                p = self.pointIndexes[pi]
                i -= 1

                if self.battleCollision(point, p):
                    return 1

        # No suits or battles in sight.
        return 0

    def battleCollision(self, point, adjacentPoint):
        """battleCollision(self, DNASuitPoint point, DNASuitPoint adjacentPoint)
        Returns true if there is a battle currently underway in the
        zone containing the edge connecting point and adjacentPoint.
        """
        zoneName = self.dnaStore.getSuitEdgeZone(
            point.getIndex(), adjacentPoint.getIndex())
        zoneId = int(self.extractGroupName(zoneName))
        
        return self.battleMgr.cellHasBattle(zoneId)


    def removeSuit(self, suit):
        """
        Removes a suit that's no longer needed.  This deletes the
        DistributedObject and also cleans up any data structures
        referencing the suit in the planner.
        """
        #self.notify.info("Suit planner removing suit %s" % (suit.doId))

        # be sure to clear the zone that the suit is in since it
        # is going to be removed completely
        self.zoneChange( suit, suit.zoneId )

        if self.suitList.count( suit ) > 0:
            self.suitList.remove( suit )

            if suit.flyInSuit:
                self.numFlyInSuits -= 1
            if suit.buildingSuit:
                self.numBuildingSuits -= 1
            if suit.attemptingTakeover:
                self.numAttemptingTakeover -= 1

        assert self.numFlyInSuits + self.numBuildingSuits == len(self.suitList)
        assert self.numAttemptingTakeover == self.countTakeovers()

        suit.requestDelete()
        return

    def countTakeovers(self):
        """
        Returns the number of suits *actually* attempting takeover.
        This is just a verification check against
        self.numAttemptingTakeover; it only gets called when
        assertions are enabled.
        """
        count = 0
        for suit in self.suitList:
            if suit.attemptingTakeover:
                count += 1
        return count

    def __waitForNextUpkeep(self):
        t = (random.random() * 2.0) + self.POP_UPKEEP_DELAY
        taskMgr.doMethodLater(t, self.upkeepSuitPopulation,
                              self.taskName('sptUpkeepPopulation'))

    def __waitForNextAdjust(self):
        t = (random.random() * 10.0) + self.POP_ADJUST_DELAY
        taskMgr.doMethodLater(t, self.adjustSuitPopulation,
                              self.taskName('sptAdjustPopulation'))

    def upkeepSuitPopulation(self, task):
        """
        examine the number of suits that exist and remove
        or add some in order to keep a reasonable balance,
        this should be called every once in a while
        """

        # How many fly-in suits do we expect to have?
        targetFlyInNum = self.calcDesiredNumFlyInSuits()
        targetFlyInNum = min(targetFlyInNum, self.TOTAL_MAX_SUITS - self.numBuildingSuits)

        # We'll need a copy of the list of street points, so we can
        # modify this as we eliminate choices.
        streetPoints = self.streetPointList[:]

        # We create one-fourth of the required number of suits each
        # time.  This will help us get caught up if we are way behind
        # in suits.
        flyInDeficit = (targetFlyInNum - self.numFlyInSuits + 3) / 4

        while flyInDeficit > 0:
            if not self.createNewSuit([], streetPoints):
                break
            
            flyInDeficit -= 1

        # How many from-building suits do we expect to have?  Here we
        # count up the number of from-building suits we want, and add
        # in the number of fly-in suits we couldn't have from above,
        # to bring our total suit count to as close an approximation
        # as possible of our actual target.
        if self.buildingMgr:
            suitBuildings = self.buildingMgr.getEstablishedSuitBlocks()
        else:
            suitBuildings = []

        if self.currDesired != None:
            targetBuildingNum = max(0, self.currDesired - self.numFlyInSuits)
        else:
            targetBuildingNum = int(len(suitBuildings) * self.SUIT_BUILDING_NUM_SUITS)

        targetBuildingNum += flyInDeficit
        targetBuildingNum = min(targetBuildingNum, self.TOTAL_MAX_SUITS - self.numFlyInSuits)

        buildingDeficit = (targetBuildingNum - self.numBuildingSuits + 3) / 4

        # Also, while we create from-building suits, we allow them to
        # fall back to fly-in suits if they can't find a door to walk
        # out of.
        while buildingDeficit > 0:
            if not self.createNewSuit(suitBuildings, streetPoints):
                break
            
            buildingDeficit -= 1

        if self.notify.getDebug() and self.currDesired == None:
            self.notify.debug("zone %d has %d of %d fly-in and %d of %d building suits." %
                              (self.zoneId,
                               self.numFlyInSuits, targetFlyInNum, 
                               self.numBuildingSuits, targetBuildingNum))
            if buildingDeficit != 0:
                self.notify.debug("remaining deficit is %d." % (buildingDeficit))

        # Finally, automatically reconvert the oldest suit building to
        # a toon building, if it's very old.  If no one's taken it
        # over by now, let it go back into the pool.

        if self.buildingMgr:
            suitBuildings = self.buildingMgr.getEstablishedSuitBlocks()
            timeoutIndex = min(len(suitBuildings), len(self.SUIT_BUILDING_TIMEOUT) - 1)
            timeout = self.SUIT_BUILDING_TIMEOUT[timeoutIndex]
            if timeout != None:
                timeout *= 3600.0 # convert hours to seconds

                # Determine the oldest (unoccupied) suit building.
                oldest = None
                oldestAge = 0
                now = time.time()
                for b in suitBuildings:
                    building = self.buildingMgr.getBuilding(b)
                    if hasattr(building, "elevator"):
                        if building.elevator.fsm.getCurrentState().getName() == 'waitEmpty':
                            age = now - building.becameSuitTime
                            if age > oldestAge:
                                oldest = building
                                oldestAge = age

                if oldestAge > timeout:
                    # It's time to reconvert a building.
                    self.notify.info("Street %d has %d buildings; reclaiming %0.2f-hour-old building." % (self.zoneId, len(suitBuildings), oldestAge / 3600.0))
                    oldest.b_setVictorList([0, 0, 0, 0])
                    # Update the trophy manager to let it know these rescuers no longer
                    # get credit for this building
                    oldest.updateSavedBy(None)
                    oldest.toonTakeOver()

        self.__waitForNextUpkeep()
        return Task.done

    def adjustSuitPopulation(self, task):
        """
        randomly adjust the actual suit population over time
        """
        # if our base number of suits is zero, dont do any adjustments since
        # in this case there is most likely a reason we want zero suits in
        # the first place
        hoodInfo = self.SuitHoodInfo[ self.hoodInfoIdx ]
        if hoodInfo[self.SUIT_HOOD_INFO_MAX] == 0:
            self.__waitForNextAdjust()
            return Task.done

        min = hoodInfo[ self.SUIT_HOOD_INFO_MIN ]
        max = hoodInfo[ self.SUIT_HOOD_INFO_MAX ]

        adjustment = random.choice((-2, -1, -1, 0, 0, 0, 1, 1, 2))

        # update the count adjustment to the base number of suits wanted
        # in this hood
        #
        self.suitCountAdjust += adjustment
        # if amount is past the min or max, stop there.
        desiredNum = self.calcDesiredNumFlyInSuits()

        if desiredNum < min:
            self.suitCountAdjust = min - self.baseNumSuits
        elif desiredNum > max:
            self.suitCountAdjust = max - self.baseNumSuits
            
        self.__waitForNextAdjust()
        return Task.done

    def suitTakeOver(self, blockNumber, suitTrack, difficulty, buildingHeight):
        if self.pendingBuildingTracks.count(suitTrack) > 0:
            self.pendingBuildingTracks.remove(suitTrack)
        if self.pendingBuildingHeights.count(buildingHeight) > 0:
            self.pendingBuildingHeights.remove(buildingHeight)
        building = self.buildingMgr.getBuilding(blockNumber)
        building.suitTakeOver(suitTrack, difficulty, buildingHeight)

    def cogdoTakeOver(self, blockNumber, difficulty, buildingHeight):
        if self.pendingBuildingHeights.count(buildingHeight) > 0:
            self.pendingBuildingHeights.remove(buildingHeight)
        building = self.buildingMgr.getBuilding(blockNumber)
        building.cogdoTakeOver(difficulty, buildingHeight)

    def recycleBuilding(self):
        # Ok, now that a building has been reclaimed by a toon, make
        # sure a new building will pop up somewhere else.

        # What's the minimum number of suit buildings on this street?
        bmin = self.SuitHoodInfo[ self.hoodInfoIdx ][ self.SUIT_HOOD_INFO_BMIN ]
        # How many suit buildings do we actually have on this street?
        current = len(self.buildingMgr.getSuitBlocks())
        
        if self.targetNumSuitBuildings > bmin and \
           current <= self.targetNumSuitBuildings:
            # If we have more than the minimum here, and we haven't
            # passed our target number anyway, we can allow the suit
            # building to show up in a different zone.
            self.targetNumSuitBuildings -= 1
            self.assignSuitBuildings(1)

        # If we already have only the minimum number of buildings on
        # this street, we'll just keep the building here.

    def assignInitialSuitBuildings(self):
        """
        This is called at startup after all the
        DistributedSuitPlannerAI objects have been created.  It
        decides how many suit buildings there should be in the world
        and assigns them to random zones, just to get the leaf blower
        system started.
        """
        # First, count up the total number of buildings in the world,
        # and also the total number of suit buildings we've already
        # got assigned (e.g. from minimums per zone).

        totalBuildings = 0
        targetSuitBuildings = 0
        actualSuitBuildings = 0
        for sp in self.air.suitPlanners.values():
            totalBuildings += len(sp.frontdoorPointList)
            targetSuitBuildings += sp.targetNumSuitBuildings
            if sp.buildingMgr:
                actualSuitBuildings += len(sp.buildingMgr.getSuitBlocks())
        wantedSuitBuildings = \
          int(totalBuildings * self.TOTAL_SUIT_BUILDING_PCT / 100)

        self.notify.debug("Want %d out of %d total suit buildings; we currently have %d assigned, %d actual." % (wantedSuitBuildings, totalBuildings, targetSuitBuildings, actualSuitBuildings))

        if actualSuitBuildings > 0:
            # If we already have *some* suit buildings in the world,
            # make sure they're all accounted for before we start
            # handing out more.
            numReassigned = 0
                
            for sp in self.air.suitPlanners.values():
                if sp.buildingMgr:
                    numBuildings = len(sp.buildingMgr.getSuitBlocks())
                else:
                    numBuildings = 0
                if numBuildings > sp.targetNumSuitBuildings:
                    more = numBuildings - sp.targetNumSuitBuildings
                    sp.targetNumSuitBuildings += more
                    targetSuitBuildings += more
                    numReassigned += more

            if numReassigned > 0:
                self.notify.debug("Assigned %d buildings where suit buildings already existed." % (numReassigned))

        if wantedSuitBuildings > targetSuitBuildings:
            # Ask for more buildings.
            additionalBuildings = wantedSuitBuildings - targetSuitBuildings
            self.assignSuitBuildings(additionalBuildings)
                        
        elif wantedSuitBuildings < targetSuitBuildings:
            # Hmm, we have to remove some targeted buildings somewhere.
            extraBuildings = targetSuitBuildings - wantedSuitBuildings
            self.unassignSuitBuildings(extraBuildings)

    def assignSuitBuildings(self, numToAssign):
        """
        After a suit building has been reclaimed by a toon (or at
        startup), locates a new street to assign each new suit building
        to.  This implements the so-called "leaf blower" model of suit
        building management, where reclaiming a building on one street
        causes a building to be taken over on a new street--all you
        can do is push buildings from one place to another; the total
        number of buildings in the world stays constant.
        """
        # Look for a suitable zone.  First, get a copy of the
        # SuitHoodInfo array, so we can remove elements from it as we
        # discover they're unsuitable.
        hoodInfo = self.SuitHoodInfo[:]
        totalWeight = self.TOTAL_BWEIGHT
        totalWeightPerTrack = self.TOTAL_BWEIGHT_PER_TRACK[:]
        totalWeightPerHeight = self.TOTAL_BWEIGHT_PER_HEIGHT[:]

        # Count up the number of each track of building already in the
        # world, so we can try to balance the world by preferring the
        # rarer tracks.
        numPerTrack = {'c': 0, 'l': 0, 'm': 0, 's':0}
        for sp in self.air.suitPlanners.values():
            sp.countNumBuildingsPerTrack(numPerTrack)
            numPerTrack['c'] += sp.pendingBuildingTracks.count('c')
            numPerTrack['l'] += sp.pendingBuildingTracks.count('l')
            numPerTrack['m'] += sp.pendingBuildingTracks.count('m')
            numPerTrack['s'] += sp.pendingBuildingTracks.count('s')

        # Also count up the number of each height of building.
        numPerHeight = {0:0, 1: 0 , 2: 0, 3: 0, 4: 0,}
        for sp in self.air.suitPlanners.values():
            sp.countNumBuildingsPerHeight(numPerHeight)
            numPerHeight[0] += sp.pendingBuildingHeights.count(0)
            numPerHeight[1] += sp.pendingBuildingHeights.count(1)
            numPerHeight[2] += sp.pendingBuildingHeights.count(2)
            numPerHeight[3] += sp.pendingBuildingHeights.count(3)
            numPerHeight[4] += sp.pendingBuildingHeights.count(4)

        # For each building:
        while numToAssign > 0:

            # Choose the track with the smallest representation for
            # this building.
            smallestCount = None
            smallestTracks = []
            for trackIndex in range(4):
                if totalWeightPerTrack[trackIndex]:
                    track = SuitDNA.suitDepts[trackIndex]
                    count = numPerTrack[track]
                    if smallestCount == None or count < smallestCount:
                        smallestTracks = [track]
                        smallestCount = count
                    elif count == smallestCount:
                        smallestTracks.append(track)

            if not smallestTracks:
                self.notify.info("No more room for buildings, with %s still to assign." % (numToAssign))
                return

            # Now smallestTracks is the list of all tracks with the
            # fewest number of buildings.  (There might be more than
            # one with the same number.)
            buildingTrack = random.choice(smallestTracks)
            buildingTrackIndex = SuitDNA.suitDepts.index(buildingTrack)

            # Do that again, choosing a suitable height.
            smallestCount = None
            smallestHeights = []
            for height in range(5):
                if totalWeightPerHeight[height]:
                    count = float(numPerHeight[height]) / float(self.BUILDING_HEIGHT_DISTRIBUTION[height])
                    if smallestCount == None or count < smallestCount:
                        smallestHeights = [height]
                        smallestCount = count
                    elif count == smallestCount:
                        smallestHeights.append(height)

            if not smallestHeights:
                self.notify.info("No more room for buildings, with %s still to assign." % (numToAssign))
                return

            # Remember, buildingHeight is numFloors - 1.
            buildingHeight = random.choice(smallestHeights)
                
            self.notify.info("Existing buildings are (%s, %s), choosing from (%s, %s), chose %s, %s." %
                             (self.formatNumSuitsPerTrack(numPerTrack),
                              self.formatNumSuitsPerTrack(numPerHeight),
                              smallestTracks, smallestHeights,
                              buildingTrack, buildingHeight))
            
            # Look for a suitable street to have this building.
            repeat = 1
            while repeat and buildingTrack != None and buildingHeight != None:
                if len(hoodInfo) == 0:
                    self.notify.warning("No more streets can have suit buildings, with %d buildings unassigned!" % (numToAssign))
                    return
                    
                repeat = 0
                
                currHoodInfo = self.chooseStreetWithPreference(hoodInfo, buildingTrackIndex, buildingHeight)

                # Get the DistributedSuitPlannerAI associated with this zone.
                zoneId = currHoodInfo[ self.SUIT_HOOD_INFO_ZONE ]

                if self.air.suitPlanners.has_key(zoneId):
                    sp = self.air.suitPlanners[zoneId]
                
                    # How many suit buildings does this zone already have?
                    numTarget = sp.targetNumSuitBuildings
                    numTotalBuildings = len(sp.frontdoorPointList)
                else:
                    # There's no SuitPlanner for this zone.  We must
                    # be running with want-suits-everywhere turned
                    # off.
                    numTarget = 0
                    numTotalBuildings = 0
                
                if numTarget >= currHoodInfo[ self.SUIT_HOOD_INFO_BMAX ] or \
                   numTarget >= numTotalBuildings:
                    # This zone has enough buildings.
                    self.notify.info("Zone %d has enough buildings." % (zoneId))
                    hoodInfo.remove(currHoodInfo)
                    weight = currHoodInfo[self.SUIT_HOOD_INFO_BWEIGHT]
                    tracks = currHoodInfo[self.SUIT_HOOD_INFO_TRACK]
                    heights = currHoodInfo[self.SUIT_HOOD_INFO_HEIGHTS]
                    totalWeight -= weight

                    totalWeightPerTrack[0] -= weight * tracks[0]
                    totalWeightPerTrack[1] -= weight * tracks[1]
                    totalWeightPerTrack[2] -= weight * tracks[2]
                    totalWeightPerTrack[3] -= weight * tracks[3]

                    totalWeightPerHeight[0] -= weight * heights[0]
                    totalWeightPerHeight[1] -= weight * heights[1]
                    totalWeightPerHeight[2] -= weight * heights[2]
                    totalWeightPerHeight[3] -= weight * heights[3]
                    totalWeightPerHeight[4] -= weight * heights[4]

                    if totalWeightPerTrack[buildingTrackIndex] <= 0:
                        # Oops, no more of this building track can be
                        # allocated.
                        assert(totalWeightPerTrack[buildingTrackIndex] == 0)
                        buildingTrack = None

                    if totalWeightPerHeight[buildingHeight] <= 0:
                        # Oops, no more of this building height can be
                        # allocated.
                        assert(totalWeightPerHeight[buildingHeight] == 0)
                        buildingHeight = None
                    
                    repeat = 1

            # Ok, now we've got a randomly-chosen zone that wants a
            # building.  Hand it over.
            if buildingTrack != None and buildingHeight != None:
                sp.targetNumSuitBuildings += 1
                sp.pendingBuildingTracks.append(buildingTrack)
                sp.pendingBuildingHeights.append(buildingHeight)
                self.notify.info("Assigning building to zone %d, pending tracks = %s, pending heights = %s" % (zoneId, sp.pendingBuildingTracks, sp.pendingBuildingHeights))
                numPerTrack[buildingTrack] += 1
                numPerHeight[buildingHeight] += 1
                numToAssign -= 1

    def unassignSuitBuildings(self, numToAssign):
        """
        The opposite of assignSuitBuildings(), this removes the
        assignment for the indicated number of buildings.  The
        buildings will remain suit buildings, but when they are
        eventually reclaimed by toons, they will not be replaced by
        more suit buildings.

        This is just called at startup in the case where we have more
        buildings in the world than we actually want to keep.
        """
        # Look for a suitable zone.  First, get a copy of the
        # SuitHoodInfo array, so we can remove elements from it as we
        # discover they're unsuitable.
        hoodInfo = self.SuitHoodInfo[:]
        totalWeight = self.TOTAL_BWEIGHT

        # For each building:
        while numToAssign > 0:
            # Look for a suitable street to pull a building from.
            repeat = 1
            while repeat:
                if len(hoodInfo) == 0:
                    self.notify.warning("No more streets can remove suit buildings, with %d buildings too many!" % (numToAssign))
                    return
                    
                repeat = 0
                currHoodInfo = self.chooseStreetNoPreference(hoodInfo, totalWeight)

                # Get the DistributedSuitPlannerAI associated with this zone.
                zoneId = currHoodInfo[ self.SUIT_HOOD_INFO_ZONE ]

                if self.air.suitPlanners.has_key(zoneId):
                    sp = self.air.suitPlanners[zoneId]
                
                    # How many suit buildings does this zone already have?
                    numTarget = sp.targetNumSuitBuildings
                    numTotalBuildings = len(sp.frontdoorPointList)
                else:
                    # There's no SuitPlanner for this zone.  We must
                    # be running with want-suits-everywhere turned
                    # off.
                    numTarget = 0
                    numTotalBuildings = 0
                
                if numTarget <= currHoodInfo[ self.SUIT_HOOD_INFO_BMIN ]:
                    # This zone can't remove any more buildings.
                    self.notify.info("Zone %d can't remove any more buildings." % (zoneId))
                    hoodInfo.remove(currHoodInfo)
                    totalWeight -= currHoodInfo[ self.SUIT_HOOD_INFO_BWEIGHT ]
                    repeat = 1

            # Ok, now we've got a randomly-chosen zone that can remove a
            # building.
            self.notify.info("Unassigning building from zone %d." % (zoneId))
            sp.targetNumSuitBuildings -= 1
            numToAssign -= 1

    def chooseStreetNoPreference(self, hoodInfo, totalWeight):
        """ Chooses a random street (neighborhood) from the supplied
        SuitHoodInfo list, without preference for any particular track
        or level.  The random decision is weighted based on the
        likelihood of a building appearing in the street at all. """

        assert totalWeight > 0
        c = random.random() * totalWeight

        # Which element does this correspond to?
        t = 0
        for currHoodInfo in hoodInfo:
            weight = currHoodInfo[self.SUIT_HOOD_INFO_BWEIGHT]
            t += weight
            if c < t:
                return currHoodInfo

        # This shouldn't be possible!
        self.notify.warning("Weighted random choice failed!  Total is %s, chose %s" % (t, c))
        assert false
        return random.choice(hoodInfo)

    def chooseStreetWithPreference(self, hoodInfo, buildingTrackIndex,
                                   buildingHeight):
        """
        As above, but the random decision is weighted based on the
        requested track and building height, so that streets that are
        more likely to have buildings of the indicated track and
        height are more likely to be selected.
        """
        # First, we need to figure the total distribution.

        dist = []
        for currHoodInfo in hoodInfo:
            weight = currHoodInfo[self.SUIT_HOOD_INFO_BWEIGHT]
            thisValue = weight * currHoodInfo[self.SUIT_HOOD_INFO_TRACK][buildingTrackIndex] * currHoodInfo[self.SUIT_HOOD_INFO_HEIGHTS][buildingHeight]
            dist.append(thisValue)
            
        totalWeight = sum(dist)
        
        # Pick a random number in the range [0, totalWeight]
        assert totalWeight > 0
        c = random.random() * totalWeight

        t = 0
        for i in range(len(hoodInfo)):
            t += dist[i]
            if c < t:
                return hoodInfo[i]

        # This shouldn't be possible!
        self.notify.warning("Weighted random choice failed!  Total is %s, chose %s" % (t, c))
        assert false
        return random.choice(hoodInfo)

    def chooseSuitLevel(self, possibleLevels, buildingHeight):
        """ Chooses an appropriate suit level, based on the list of
        possible suit levels allowed on this street, for a suit that
        will produce a building of the requested height. """

        choices = []
        for level in possibleLevels:
            minFloors, maxFloors = SuitBuildingGlobals.SuitBuildingInfo[level - 1][0]
            # Remember that buildingHeight is numFloors - 1
            if buildingHeight >= minFloors - 1 and buildingHeight <= maxFloors - 1:
                # This level is allowed.
                choices.append(level)

        return random.choice(choices)

    def initTasks(self):
        """
        this should be called just after creating the
        suit planner in order to set up tasks that will
        update the suit planner occasionally
        """
        # create a looping task sequence that will occasionally update the
        # suit population in the local neighborhood
        self.__waitForNextUpkeep()

        # create a looping task sequence that will occasionally update the
        # adjustment to the number of suits desired in this hood, this gradually
        # changes over time
        self.__waitForNextAdjust()

    def resyncSuits(self):
        """
        This calls resync() on every suit managed by the planner.
        See the comments in DistributedSuitAI.resync().
        """
        for suit in self.suitList:
            suit.resync()

    def flySuits(self):
        """
        This asks all the suits to fly away abruptly.  No good reason
        to do this except for debugging.  "~cogs fly" does this.
        """
        for suit in self.suitList:
            if suit.pathState == 1:
                suit.flyAwayNow()

    def requestBattle(self, zoneId, suit, toonId):
        self.notify.debug('requestBattle() - zone: %d suit: %d toon: %d' % \
                (zoneId, suit.doId, toonId))
        canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        if not self.battlePosDict.has_key(canonicalZoneId):
            # If the zone doesn't have a battle cell, brush off the toon.
            return 0
        
        toon = self.air.doId2do.get(toonId)
        
        # There is a problem of being able to join two battles at once, 
        # so check if we are already in a battle first.
        if toon.getBattleId() > 0:
            self.notify.warning("We tried to request a battle when the toon was already in battle")
            return 0
            
        # Then set our battleID right up here, to lock out any further requests from getting triggered.
        if toon:
            if hasattr(toon, "doId"):
                print ("Setting toonID ", toonId)
                toon.b_setBattleId(toonId)
                
        pos = self.battlePosDict[canonicalZoneId]
        interactivePropTrackBonus = -1
        if simbase.config.GetBool("props-buff-battles", True) and \
           self.cellToGagBonusDict.has_key(canonicalZoneId) :
            tentativeBonusTrack  = self.cellToGagBonusDict[canonicalZoneId]
            # next double check if the holiday for it to buff has started
            trackToHolidayDict = { ToontownBattleGlobals.SQUIRT_TRACK: ToontownGlobals.HYDRANTS_BUFF_BATTLES,
                                   ToontownBattleGlobals.THROW_TRACK: ToontownGlobals.MAILBOXES_BUFF_BATTLES,
                                   ToontownBattleGlobals.HEAL_TRACK: ToontownGlobals.TRASHCANS_BUFF_BATTLES,
                                   }
            if tentativeBonusTrack in trackToHolidayDict:
                holidayId = trackToHolidayDict[tentativeBonusTrack]
                if simbase.air.holidayManager.isHolidayRunning(holidayId ) and \
                   simbase.air.holidayManager.getCurPhase(holidayId) >= 1:
                    interactivePropTrackBonus = tentativeBonusTrack
                
            
        self.battleMgr.newBattle(
            zoneId, zoneId, pos, suit, toonId,
            self.__battleFinished,
            self.SuitHoodInfo[ self.hoodInfoIdx ][ self.SUIT_HOOD_INFO_SMAX ],
            interactivePropTrackBonus)

        # make sure to pull in any suits currently in this zone into
        # the battle, but only if they are in 'Bellicose' and are
        # ready to enter a battle.  We used to make the non-bellicose
        # suits fly away, but that seems like a mistake, since these
        # suits will be entering a door or already flying away or
        # something else equally harmless.
        
        for currOther in self.zoneInfo[ zoneId ]:
            self.notify.debug("Found suit %d in this new battle zone %d" % \
                              ( currOther.getDoId(), zoneId ))
            if currOther != suit:
                if currOther.pathState == 1 and \
                   currOther.legType == SuitLeg.TWalk:
                    self.checkForBattle( zoneId, currOther )

        return 1

    def __battleFinished( self, zoneId ):
        """
        zoneId, the zone in which the battle exists
        
        called when a battle in this neighborhood finishes
        """
        # remove any references to this battle from our battle list
        #
        self.notify.debug( "DistSuitPlannerAI:  battle in zone " +
                           str( zoneId ) + " finished" )
        currBattleIdx = 0
        while currBattleIdx < len( self.battleList):
            currBattle = self.battleList[currBattleIdx]
            if currBattle[0] == zoneId:
                self.notify.debug("DistSuitPlannerAI: battle removed")
                self.battleList.remove( currBattle )
            else:
                currBattleIdx = currBattleIdx + 1
        return None

    def __suitCanJoinBattle( self, zoneId ):
        """
        Function:    look at a battle in a specific zone and calculate
                     if a suit is able to join the battle based on the
                     various join-chance values specified for this suit
                     planner
        Parameters:  zoneId, the zone in which a battle exists
        Returns:     1 if the suit can join, 0 otherwise
        """
        battle = self.battleMgr.getBattle( zoneId )
        if len( battle.suits ) >= 4:
            return 0
        if battle:
            # the chance of a suit joining a battle depends on the suit to
            # toon ratio of the battle, once this chance is obtained, the
            # suit randomly decides if it should join, first check to see
            # if we have a config to tell us that suits always join battles
            # with an empty slot
            #
            if simbase.config.GetBool('suits-always-join', 0):
                 return 1
            jChanceList = self.SuitHoodInfo[ self.hoodInfoIdx ]\
                          [ self.SUIT_HOOD_INFO_JCHANCE ]
            ratioIdx = len( battle.toons ) - battle.numSuitsEver + 2
            if ratioIdx >= 0:
                if ratioIdx < len( jChanceList ):
                    if random.randint( 0, 99 ) < jChanceList[ ratioIdx ]:
                        return 1
                else:
                    self.notify.warning( "__suitCanJoinBattle idx out of range!" )
                    return 1
        return 0

    def checkForBattle(self, zoneId, suit):
        # See if zone has a battle or not
        if (self.battleMgr.cellHasBattle(zoneId)):
            # If zone has a battle, see if there are any spots in it    
            # but first, randomly decide if this suit should even try
            # to join the battle based on the hood's join battle
            # randomness
            if self.__suitCanJoinBattle( zoneId ) and \
               self.battleMgr.requestBattleAddSuit( zoneId, suit ):
                # The suit gets added to the battle and the battle
                # takes control
                pass
            else:
                # Make the suit fly away
                suit.flyAwayNow()
            return 1
        else:
            # There is no battle, so continue
            return 0 

    def postBattleResumeCheck( self, suit ):
        """
        Function:    check to see if a specific suit should, after it
                     gets out of a battle, resume its previous path or
                     if that path is already occupied and the suit
                     should fly away
        Changes:     1 if suit should resume path, 0 to fly away
        """
        self.notify.debug("DistSuitPlannerAI:postBattleResumeCheck:  suit " +
                           str( suit.getDoId() ) + " is leaving battle")
        battleIndex = 0
        for currBattle in self.battleList:
            if suit.zoneId == currBattle[0]:
                self.notify.debug("    battle found" + str( suit.zoneId ) )
                # now that we found the zone in our list of battles, check
                # the first path to see if there is any intersection between
                # the path and this suit's path, if so, then this suit will
                # probably end up conflicting with a previously resumed suit.
                # So lets tell this suit to fly away
                #
                for currPath in currBattle[ 1 ]:
                    for currPathPtSuit in range( suit.currWpt,
                                                 suit.myPath.getNumPoints() ):
                        ptIdx = suit.myPath.getPointIndex( currPathPtSuit )
                        if self.notify.getDebug():
                            self.notify.debug("    comparing" + str( ptIdx ) +
                                              "with" + str( currPath ) )
                        if currPath == ptIdx:
                            if self.notify.getDebug():
                                self.notify.debug("    match found, telling"+ \
                                                  "suit to fly")
                            return 0
            else:
                battleIndex = battleIndex + 1


        # battle was not found, so add one to the list and generate a
        # list of indexes which represent each of the next several
        # path points in this suit's path, so any future suit that
        # exits a battle in this zone will compare its path to this
        # path to check for collisions when they disperse and leave
        # the battle
        #
        pointList = []
        for currPathPtSuit in range( suit.currWpt,
                                     suit.myPath.getNumPoints() ):
            ptIdx = suit.myPath.getPointIndex( currPathPtSuit )
            if self.notify.getDebug():
                self.notify.debug("    appending point with index of" +
                                  str( ptIdx ) )
            pointList.append( ptIdx )

        # add the zone id and the list of indexes
        #
        self.battleList.append( [ suit.zoneId, pointList ] )

        return 1

    def zoneChange( self, suit, oldZone, newZone=None ):
        """
        Function:    notify the suit planner when a suit changes zones
        Parameters:  suit, the suit that is changing zones
                     oldZone, where the suit was previously
                     newZone, where suit is now, None if suit is bye-bye
        """
        # remove any old reference of the suit from the zones list
        #
        if self.zoneInfo.has_key( oldZone ) and \
           suit in self.zoneInfo[ oldZone ]:
            self.zoneInfo[ oldZone ].remove( suit )

        # add the suit to the appropriate zone if one was given
        #
        if newZone != None:
            if not self.zoneInfo.has_key( newZone ):
                self.zoneInfo[ newZone ] = []
            self.zoneInfo[ newZone ].append( suit )

    def d_setZoneId( self, zoneId):
        self.sendUpdate( 'setZoneId', [ self.getZoneId() ] )
    def getZoneId( self ):
        return self.zoneId

    def suitListQuery( self ):
        # just send back a list of suit type indices
        suitIndexList = []
        for suit in self.suitList:
            suitIndexList.append(SuitDNA.suitHeadTypes.index(suit.dna.name))
        self.sendUpdateToAvatarId( self.air.getAvatarIdFromSender(), 'suitListResponse', [ suitIndexList ] )

    def buildingListQuery( self ):
        # send back a list of suit buildings in the format:
        #      [numCorp, numLegal, numMoney, numSales]
        buildingDict = {}
        self.countNumBuildingsPerTrack(buildingDict)
        buildingList = [0, 0, 0, 0]
        for dept in SuitDNA.suitDepts:
            if buildingDict.has_key(dept):
                buildingList[SuitDNA.suitDepts.index(dept)] = buildingDict[dept]
        self.sendUpdateToAvatarId( self.air.getAvatarIdFromSender(), 'buildingListResponse', [ buildingList ] )
        
    def pickLevelTypeAndTrack(self, level = None, type = None, track = None):
        """
        Chooses a suitable suit description in terms of its level and
        type numbers, and track letter.  Normally, all three
        parameters are chosen at random, but for special purposes
        (e.g. magic words), one or more may be passed in as non-None.
        """
        # first randomly choose a level from those available for this hood
        if level == None:
            level = random.choice(
                self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_LVL] )

        # now randomly choose a type of suit based on the level, any given
        # type of suit can only be one of 5 levels
        if type == None:
            typeChoices = range(max(level - 4, 1),
                                min(level, self.MAX_SUIT_TYPES) + 1)
            type = random.choice(typeChoices)
        else:
            # if our type is already specified, we might need to
            # constrain the level to fit.
            level = min(max(level, type), type + 4)

        # now randomly choose a suit 'department', or track, or whatever
        # we are calling it.
        if track == None:
            track = SuitDNA.suitDepts[SuitBattleGlobals.pickFromFreqList(
                self.SuitHoodInfo[self.hoodInfoIdx][self.SUIT_HOOD_INFO_TRACK])]
        self.notify.debug("pickLevelTypeAndTrack: %d %d %s" % (level, type, track))
        return (level, type, track)


# history
#
# 22Jan01    jlbutler    created.
# 23Jan01    jlbutler    added code for removing suits and a function
#                        which handles assigning tasks periodically
# 23Jan01    jlbutler    created 'generateTask' and 'think' functions
# 06Feb01    jlbutler    added 'getBattleCellLocation' so others may ask
#                        the suit planner for the location a specific
#                        battle sphere within a specific zone 
# 12Feb01    jlbutler    derived SuitPlannerAI from SuitPlannerBase, where
#                        common code that the client might need has been
#                        placed
# 19Feb01    jlbutler    added postBattleResumeCheck which allows the suit
#                        planner to decide if a suit, after it leaves a battle,
#                        should resume it's previous path or if it should
#                        fly away
# 19Apr01    jlbutler    added self.zoneInfo to contain a list of zones
#                        and suits that are currently in those zones, useful
#                        for finding suits in a specific area (also added
#                        function zoneChange(...) to help make it easier to
#                        use the new zone list
# 01May01    jlbutler    added the ability for the suit planner to randomly
#                        pick a suit building for a new suit to exit from,
#                        and the suit will be created with the same track
#                        as the building
#
