from ElevatorConstants import *

# floor and suit information for all suit buildings, organized by each
# level of suit that originally took over the building (minus 1), used
# to determine how many and what level of suits to create for the suit
# interiors
#
#    1  number of floors for this level building
#    2  suit level range, excluding the boss
#    3  boss level range
#    4  base level pool for total suits on each floor of the building
#    5  multipliers for item 4 for each floor of the building, generally
#       each consecutive floor increases the base range of the level pool
#    6 are they v2.0 cogs
#
SuitBuildingInfo = (
    # building difficulty 0 (suit level 1)
    ( ( 1, 1 ),                           # 1
      ( 1, 3 ),                           # 2
      ( 4, 4 ),                           # 3
      ( 8, 10 ),                          # 4
      ( 1, ) ),                           # 5
    # building difficulty 1 (suit level 2)
    ( ( 1, 2 ),
      ( 2, 4 ),
      ( 5, 5 ),
      ( 8, 10 ),
      ( 1, 1.2 ) ),
    # building difficulty 2 (suit level 3)
    ( ( 1, 3 ),
      ( 3, 5 ),
      ( 6, 6 ),
      ( 8, 10 ),
      ( 1, 1.3, 1.6 ) ),
    # building difficulty 3 (suit level 4)
    ( ( 2, 3 ),
      ( 4, 6 ),
      ( 7, 7 ),
      ( 8, 10 ),
      ( 1, 1.4, 1.8 ) ),
    # building difficulty 4 (suit level 5)
    ( ( 2, 4 ),
      ( 5, 7 ),
      ( 8, 8 ),
      ( 8, 10 ),
      ( 1, 1.6, 1.8, 2 ) ),
    # building difficulty 5 (suit level 6)
    ( ( 3, 4 ),
      ( 6, 8 ),
      ( 9, 9 ),
      ( 10, 12 ),
      ( 1, 1.6, 2, 2.4 ) ),
    # building difficulty 6 (suit level 7)
    ( ( 3, 5 ),
      ( 7, 9 ),
      ( 10, 10 ),
      ( 10, 14 ),
      ( 1, 1.6, 1.8, 2.2, 2.4 ) ),
    # building difficulty 7 (suit level 8)
    ( ( 4, 5 ),
      ( 8, 10 ),
      ( 11, 11 ),
      ( 12, 16 ),
      ( 1, 1.8, 2.4, 3, 3.2 ) ),
    # building difficulty 8 (suit level 9)
    ( ( 5, 5 ),
      ( 9, 11 ),
      ( 12, 12 ),
      ( 14, 20 ),
      ( 1.4, 1.8, 2.6, 3.4, 4 ) ),

    # building difficulty 9.  This is a special difficulty level that
    # is used only for the first battle with the Sellbot V.P.  No
    # buildings in the world outside of CogHQ have difficulty level 9.
    ( ( 1, 1 ),
      ( 1, 12 ),
      ( 12, 12 ),
      ( 67, 67 ),
      ( 1, 1, 1, 1, 1 ) ),

    # building difficulty 10.  Same as above, for the second battle with
    # the Sellbot V.P.  These are skelecogs.
    ( ( 1, 1 ),
      ( 8, 12 ),
      ( 12, 12 ),
      ( 100, 100 ),
      ( 1, 1, 1, 1, 1 ) ),

    # building difficulty 11, first battle with Cashbot V.P.  These
    # are normal cogs.
    ( ( 1, 1 ),
      ( 1, 12 ),
      ( 12, 12 ),
      ( 100, 100 ),
      ( 1, 1, 1, 1, 1 ) ),

    # building difficulty 12, first battle with Cashbot V.P., but
    # these are the skelecogs.  In the cashbot battle, both normal
    # cogs and skelecogs are mixed up together.
    ( ( 1, 1 ),
      ( 8, 12 ),
      ( 12, 12 ),
      ( 150, 150 ),
      ( 1, 1, 1, 1, 1 ) ),    

    # building difficulty 13, first battle with Lawbot Boss. These
    # are normal cogs.
    ( ( 1, 1 ),
      ( 8, 12 ),
      ( 12, 12 ),
      ( 275, 275 ),
      ( 1, 1, 1, 1, 1 ) ),

    # building difficulty 14, first battle with Bossbot Boss. These
    # are v2.0 cogs. Even though it has less total suit levels, they
    # are fought twice!
    ( ( 1, 1 ),
      ( 9, 12 ),
      ( 12, 12 ),
      ( 206, 206 ),
      ( 1, 1, 1, 1, 1),
      ( 1, ) ),
    )


SUIT_BLDG_INFO_FLOORS         = 0
SUIT_BLDG_INFO_SUIT_LVLS      = 1
SUIT_BLDG_INFO_BOSS_LVLS      = 2
SUIT_BLDG_INFO_LVL_POOL       = 3
SUIT_BLDG_INFO_LVL_POOL_MULTS = 4
SUIT_BLDG_INFO_REVIVES = 5


# how long it takes for a building to transition from a toon
# to suit building, and vice-versa
#

VICTORY_RUN_TIME = ElevatorData[ELEVATOR_NORMAL]['openTime'] + \
                   TOON_VICTORY_EXIT_TIME
TO_TOON_BLDG_TIME = 8 
VICTORY_SEQUENCE_TIME = VICTORY_RUN_TIME + TO_TOON_BLDG_TIME
CLEAR_OUT_TOON_BLDG_TIME = 4
TO_SUIT_BLDG_TIME = 8


# History
#
# 14Aug01  jlbutler    created.

