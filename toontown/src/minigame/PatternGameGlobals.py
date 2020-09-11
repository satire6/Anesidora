# PatternGameGlobals.py: contains pattern game stuff
# used by AI and client

import MinigameGlobals

# pattern constants
INITIAL_ROUND_LENGTH = 2
ROUND_LENGTH_INCREMENT = 2
NUM_ROUNDS  = 4
TOONTOWN_WORK = 1

# how long the players have to input the pattern
InputTime = 10

# this is how long the AI server will wait for msgs from the clients
# before assuming that the msg is not coming
ClientsReadyTimeout = 5 + MinigameGlobals.latencyTolerance
InputTimeout = InputTime + MinigameGlobals.latencyTolerance
