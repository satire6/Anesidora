# These are the basic types of model that a DistributedHouse can be
# Customizations can be made to the houses, but the basic house type
# will remain the same

NUM_HOUSE_TYPES = 6
HOUSE_DEFAULT   = 0
HOUSE_CRAFTSMAN = 1
HOUSE_TEST      = 5

CLEANUP_DELAY = 8      # Cleanup estate after delay, should be longer than grace period
BOOT_GRACE_PERIOD = 5  # Extra time visitors have to finish up at your estate after you leave
CLEANUP_DELAY_AFTER_BOOT = 2

WANT_TELEPORT_TIMEOUT = 0
TELEPORT_TIMEOUT = 15    # Give up after n seconds if we don't get an estateZone back from AI
defaultEntryPoint = (23.875, -13.052, 10.092, 7.52, 0, 0)

houseModels = ["phase_5.5/models/estate/houseA.bam",
               "phase_5.5/models/estate/tt_m_ara_est_house_tiki.bam",
               "phase_5.5/models/estate/tt_m_ara_est_house_tepee.bam",
               "phase_5.5/models/estate/tt_m_ara_est_house_castle.bam",
               "phase_5.5/models/estate/tt_m_ara_est_house_cupcake.bam",
               "phase_5.5/models/estate/test_houseA.bam"]

houseDrops = [(-56.7788, -42.8756, 4.06471, -90, 0, 0),
              (83.3909, -77.5085, 0.0708361,116.565, 0, 0),
              (-69.077, -119.496, 0.025, 77.1957, 0, 0),
              (63.4545, 11.0656, 8.05158, 356.6, 0, 0),
              (43.9315, 76.72, 0.0377455, 248.962, 0, 0),
              (-36.9122, 36.3429, 2.49382, 36.8699, 0, 0),
              ]

gardenDrops = [(25, 68, 0),
               (68, -6, 0),
               (27, -59, 0),
               (-54, -72, 1),
               (-95, -29, 0),
               (-30, 58, 0),
               ]

# house colors are themed to the avatarChooser colors
houseColors = [
    (0.892, 0.453, 0.390), # red
    (0.276, 0.692, 0.539), # green
    (0.639, 0.624, 0.882), # purple
    (0.525, 0.780, 0.935), # blue
    (0.953, 0.545, 0.757), # pink
    (.992, .843, .392),    # yellow
    ]

houseColors2 = [
    (0.792, 0.353, 0.290), # red
    (0.176, 0.592, 0.439), # green
    (0.439, 0.424, 0.682), # purple
    (0.325, 0.580, 0.835), # blue
    (0.753, 0.345, 0.557), # pink
    (.992, .843, .392),    # yellow
    ]

interiorColors = [
    (0.789, 1, 0.7), # pale green
    (1, 1, 0.7), # yellow
    (1, 0.82, 0.7), # peach
    (0.839, 0.651, 0.549), # cantelope
    (0.5, 0.586, 0.4), # forest green
    (0.808, 0.678, 0.510), # tan
    (0.875, 0.937, 1.000), # light blue
    ]

interiorWood = [
    (1.0, 1.0, 1.0),
    (0.690, 0.741, 0.710),  # dark wood
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (1.0, 1.0, 1.0),
    (0.690, 0.741, 0.710),  # dark wood
    ]

archWood = (0.7,0.6,0.5)
atticWood = (.49, .314, .224)
stairWood = (0.651, 0.376, 0.310)
doorWood = (0.647, 0.392, 0.353)
windowWood = (0.557, 0.388, 0.200)

# interior type contains lists of [dnaFile, closet_poshpr, bank_poshpr, hidden_windows]
interiors = [["phase_5.5/dna/house_interior3.dna",
              [-19.45, 24.7018, 0, 0, 0, 0], [-21.4932, 5.76027, 0, 120, 0, 0],
              []],
             ["phase_5.5/dna/house_interior7.dna",
              [-19.45, 24.7018, 0, 0, 0, 0], [-21.4932, 5.76027, 0, 120, 0, 0],
              []],
             ["phase_5.5/dna/house_interior10.dna",
              [-22.5835, 21.8784, 0, 90, 0, 0], [-20.96, 6.49, 0, 120, 0, 0],
              ["c", "e"]],
             ]

NUM_PROPS = 3
PROP_ICECUBE = 0
PROP_FLOWER = 1
PROP_SNOWFLAKE = 2

FURNITURE_MODE_OFF = 0
FURNITURE_MODE_STOP = 1
FURNITURE_MODE_START = 2

# Day/night cycle time
# Make sure DAY_PERIOD + NIGHT_PERIOD = DAY_NIGHT_PERIOD, and such
DAY_NIGHT_PERIOD = 2700
DAY_PERIOD = 2100
NIGHT_PERIOD = 600
HALF_DAY_PERIOD = 1050
HALF_NIGHT_PERIOD = 300

# use shorter values for testing:
#DAY_NIGHT_PERIOD = 40
#DAY_PERIOD = 26
#NIGHT_PERIOD = 14
#HALF_DAY_PERIOD = 13
#HALF_NIGHT_PERIOD = 7

FIREWORKS_MOVIE_CLEAR = 0
FIREWORKS_MOVIE_GUI = 1

