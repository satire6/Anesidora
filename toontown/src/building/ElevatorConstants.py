from pandac.PandaModules import *


# The various types of elevators
ELEVATOR_NORMAL = 0
ELEVATOR_VP     = 1
ELEVATOR_MINT   = 2
ELEVATOR_CFO    = 3
ELEVATOR_CJ     = 4
ELEVATOR_OFFICE = 5
ELEVATOR_STAGE  = 6
ELEVATOR_BB     = 7
ELEVATOR_COUNTRY_CLUB   = 8 # country club cog golf kart / elevator

# Reasons for rejecting a toons
REJECT_NOREASON = 0
REJECT_SHUFFLE = 1
REJECT_MINLAFF = 2
REJECT_NOSEAT = 3
REJECT_PROMOTION = 4
REJECT_BLOCKED_ROOM = 5 # a room needs to be defeated first
REJECT_NOT_YET_AVAILABLE = 6 # deliberately blocked by devs for now
REJECT_BOARDINGPARTY = 7 #the reject came from the boarding party.
REJECT_NOTPAID = 8

MAX_GROUP_BOARDING_TIME = 6.0

if __dev__:
    try:
        config = simbase.config
    except:
        config = base.config
    elevatorCountdown = config.GetFloat('elevator-countdown', -1)
    if elevatorCountdown != -1:
        bboard.post('elevatorCountdown', elevatorCountdown)

# Constants used for elevator coordination
ElevatorData = {
    ELEVATOR_NORMAL : { "openTime"  : 2.0,
                        "closeTime" : 2.0,
                        "width"     : 3.5,
                        "countdown" : bboard.get('elevatorCountdown',15.0),
                        "sfxVolume" : 1.0,
                        "collRadius": 5,
                        },
    ELEVATOR_VP     : { "openTime"  : 4.0,
                        "closeTime" : 4.0,
                        "width"     : 11.5,
                        "countdown" : bboard.get('elevatorCountdown',30.0),
                        "sfxVolume" : 0.7,
                        "collRadius": 7.5,
                        },
    ELEVATOR_MINT   : { "openTime"  : 2.0,
                        "closeTime" : 2.0,
                        "width"     : 5.875,
                        "countdown" : bboard.get('elevatorCountdown',15.0),
                        "sfxVolume" : 1.0,
                        "collRadius": 5,
                        },
    ELEVATOR_OFFICE : { "openTime"  : 2.0,
                        "closeTime" : 2.0,
                        "width"     : 5.875,
                        "countdown" : bboard.get('elevatorCountdown',15.0),
                        "sfxVolume" : 1.0,
                        "collRadius": 5,
                        },
    ELEVATOR_CFO    : { "openTime"  : 3.0,
                        "closeTime" : 3.0,
                        "width"     : 8.166,
                        "countdown" : bboard.get('elevatorCountdown',30.0),
                        "sfxVolume" : 0.7,
                        "collRadius": 7.5,
                        },
    ELEVATOR_CJ     : { "openTime"  : 4.0,
                        "closeTime" : 4.0,
                        "width"     : 15.8, 
                        "countdown" : bboard.get('elevatorCountdown',30.0),
                        "sfxVolume" : 0.7,
                        "collRadius": 7.5,
                        },
    ELEVATOR_STAGE : { "openTime"  : 4.0,
                        "closeTime" : 4.0,
                        "width"     : 6.5,
                        "countdown" : bboard.get('elevatorCountdown',42.0),
                        "sfxVolume" : 1.0,
                        "collRadius": 9.5,
                        },
    ELEVATOR_BB     : { "openTime"  : 4.0,
                        "closeTime" : 4.0,
                        "width"     : 6.3, 
                        "countdown" : bboard.get('elevatorCountdown',30.0),
                        "sfxVolume" : 0.7,
                        "collRadius": 7.5,
                        },
    ELEVATOR_COUNTRY_CLUB : { "openTime"  : 2.0,
                        "closeTime" : 2.0,
                        "width"     : 5.875,
                        "countdown" : bboard.get('elevatorCountdown',15.0),
                        "sfxVolume" : 1.0,
                        "collRadius": 4,
                        },    
    }

TOON_BOARD_ELEVATOR_TIME = 1.0
TOON_EXIT_ELEVATOR_TIME = 1.0
TOON_VICTORY_EXIT_TIME = 1.0
SUIT_HOLD_ELEVATOR_TIME = 1.0
SUIT_LEAVE_ELEVATOR_TIME = 2.0
# 120 seemed like to long when somebody was just joking
# or griefing by not getting in the elevator. How bout 60?
# ...60 not long enough to account for network lags, apparently
# (is xp being skipped if this times out?)
INTERIOR_ELEVATOR_COUNTDOWN_TIME = 90

# The color of the "off" elevator lights.
LIGHT_OFF_COLOR = Vec4(0.5, 0.5, 0.5, 1.0)

# The color of the "on" elevator light.
LIGHT_ON_COLOR = Vec4(1.0, 1.0, 1.0, 1.0)

ElevatorPoints = [[-1.5, 5, 0.1],  # Back left
                  [1.5, 5, 0.1],   # Back right
                  [-2.5, 3, 0.1],  # Front left
                  [2.5, 3, 0.1],   # Front right
                  [-3.5, 5, 0.1],  # Left of back left
                  [3.5, 5, 0.1],   # Right of back right 
                  [-4, 3, 0.1],    # Left of front left 
                  [4, 3, 0.1]]     # Right of front right
                  
JumpOutOffsets = [[-1.5, -5, -0],  # Slot 1 - Back left
                  [1.5, -5, -0],  # Slot 2 - Back right
                  [-2.5, -7, -0],  # Slot 3 - Front left
                  [2.5, -7, -0],  # Slot 4 - Front right
                  [-3.5, -5, -0],  # Slot 5 - Left of back left
                  [3.5, -5, -0],  # Slot 6 - Right of back right
                  [-4, -7, -0],  # Slot 7 - Left of front left
                  [4, -7, -0]]  # Slot 8 - Right of front right

BigElevatorPoints = [[-2.5, 9, 0.1],    # Back left center
                     [2.5, 9, 0.1],     # Back right center
                     [-8.0, 9, 0.1],    # Back left left
                     [8.0, 9, 0.1],     # Back right right
                     [-2.5, 4, 0.1],    # Front left center
                     [2.5, 4, 0.1],     # Front right center
                     [-8.0, 4, 0.1],    # Front left left
                     [8.0, 4, 0.1]]     # Front right right

BossbotElevatorPoints = [[-2.5, 7.5, 0.1],    # Back left center
                         [2.5, 7.5, 0.1],     # Back right center
                         [-5.5, 7.5, 0.1],    # Back left left
                         [5.5, 7.5, 0.1],     # Back right right
                         [-2.5, 3.5, 0.1],    # Front left center
                         [2.5, 3.5, 0.1],     # Front right center
                         [-5.5, 3.5, 0.1],    # Front left left
                         [5.5, 3.5, 0.1]]     # Front right right     

# The victors will fan out into a semicircle after they leave the
# elevator to observe the transformation.
ElevatorOutPoints = [[-4.6, -5.2, 0.1],  # Back left
                     [4.6, -5.2, 0.1],   # Back right
                     [-1.6, -6.2, 0.1],  # Front left
                     [1.6, -6.2, 0.1]]   # Front right
