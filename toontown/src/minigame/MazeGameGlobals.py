# MazeGameGlobals.py: contains maze game stuff
# used by both AI and client

from direct.showbase import RandomNumGen

ENDLESS_GAME = config.GetBool('endless-maze-game', 0)

GAME_DURATION = 60.
SHOWSCORES_DURATION = 2.

# each suit will be updated every N tics, where N can vary from suit to suit
SUIT_TIC_FREQ = int(256)

#forcedMaze = 'phase_4/models/minigames/maze_2player'

def getMazeName(gameDoId, numPlayers, mazeNames):
    try:
        return forcedMaze
    except:
        names = mazeNames[numPlayers-1]
        return names[RandomNumGen.randHash(gameDoId) % len(names)]
