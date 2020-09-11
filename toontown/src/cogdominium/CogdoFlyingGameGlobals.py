"""RingGameGlobals: contains values shared by server and client ring games"""

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

class VariableContainer:
    def __init__(self):
        pass

FlyingGame = VariableContainer()

#The effect how fast you get up to max speed
FlyingGame.TOON_ACCELERATION = {
    "forward" : 20.0, 
    "backward": 20.0, 
    "turning" : 50.0,
    "vertical" : 10.0
}
# This effects how quickly the toon movement is dampened
FlyingGame.TOON_DECELERATION = {
    "forward" : 30.0, 
    "backward": 30.0, 
    "turning" : 40.0,
    "vertical" : 10.0
}
# This effects the max velocity in each direction
FlyingGame.TOON_VEL_MAX = {
    "forward" : 20.0, 
    "backward": 10.0, 
    "turning" : 8.0,
    "vertical" : 8.0
}

FlyingGame.DISABLE_DEATH = False
FlyingGame.MULTIPLE_REFUELS_PER_STATION = False
# This sets the player's fuel to max and then doesn't deplete it
FlyingGame.INFINITE_FUEL = False

FlyingGame.FUEL_BURN_RATE = 0.02
FlyingGame.FUEL_START_AMT = 1.0
