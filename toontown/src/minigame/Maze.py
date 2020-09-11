"""Maze module: contains the Maze class"""
from pandac.PandaModules import VBase3

from toontown.toonbase.ToonBaseGlobal import *

import MazeData

# world space:
#
# +Y is up the screen
# +X is to the right
#
# tile space:
# +Y is up the screen
# +X is to the right

class Maze:
    def __init__(self, mapName):
        self.maze = loader.loadModel(mapName)
        self.maze.setPos(0,0,0)
        self.maze.reparentTo(hidden)

        # get maze dimensions, boolean collision array
        mData = MazeData.mazeData[mapName]
        self.width = mData["width"]
        self.height = mData["height"]
        self.originTX = mData["originX"]
        self.originTY = mData["originY"]
        self.collisionTable = mData["collisionTable"]
        self.treasurePosList = mData["treasurePosList"]
        self.numTreasures = len(self.treasurePosList)

        self.cellWidth = MazeData.CELL_WIDTH

    def destroy(self):
        self.maze.removeNode()
        del self.maze

    def onstage(self):
        self.maze.reparentTo(render)

    def offstage(self):
        self.maze.reparentTo(hidden)

    def setScale(self, xy=1, z=1):
        self.maze.setScale(VBase3(xy, xy, z))

        self.cellWidth = MazeData.CELL_WIDTH * xy

    def isWalkable(self, tX, tY, rejectList=()):
        """ returns true if tile X,Y corresponds to a valid standing space """
        if (tX <= 0 or tY <= 0 or \
            tX >= self.width or tY >= self.height):
            return 0

        return (not self.collisionTable[tY  ][tX  ]) and \
               (not self.collisionTable[tY-1][tX  ]) and \
               (not self.collisionTable[tY  ][tX-1]) and \
               (not self.collisionTable[tY-1][tX-1]) and \
               (not (tX, tY) in rejectList)

    def tile2world(self, TX, TY):
        """ returns 2d point at the corner of tile TX, TY """
        return [(TX-self.originTX)*self.cellWidth,
                (TY-self.originTY)*self.cellWidth]

    def world2tile(self, x, y):
        """ convert from world coords to tile coords """
        return [int((x/self.cellWidth) + self.originTX),
                int((y/self.cellWidth) + self.originTY)]
