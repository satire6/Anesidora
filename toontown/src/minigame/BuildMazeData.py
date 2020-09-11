from pandac.PandaModules import *
from direct.showbase import Loader

outputFile = "MazeData.py"

mazeNames = [
    [ # one-player
    "phase_4/models/minigames/maze_1player",
    ],
    [ # two-player
    "phase_4/models/minigames/maze_2player",
    ],
    [ # three-player
    "phase_4/models/minigames/maze_3player",
    ],
    [ # four-player
    "phase_4/models/minigames/maze_4player",
    ],
    ]

CELL_WIDTH = 2 # feet

CollideMask = BitMask32(1)

loader = Loader.Loader(None)
root = NodePath('root')

def fwrite(file, str):
    file.write(str)
    file.write("\n")

def fwritelines(file, strs):
    for str in strs:
        fwrite(file,str)

def calcMazeTopology(mazeNode):
    cRay = CollisionRay(0,0,50,0,0,-1)
    cNode = CollisionNode('cNode')
    cNode.addSolid(cRay)
    cNodePath = root.attachNewNode(cNode)
    cNode.setCollideMask(CollideMask)

    cQueue = CollisionHandlerQueue()

    cTrav = CollisionTraverser("BuildMazeData")
    cTrav.addCollider(cNodePath, cQueue)

    def calcHeight(x, y):
        # returns None if off the edge of maze
        _x = (CELL_WIDTH/2) + (x*CELL_WIDTH)
        _y = (CELL_WIDTH/2) + (y*CELL_WIDTH)
        cNodePath.setPos(_x,_y,0)
        cTrav.traverse(mazeNode)
        if cQueue.getNumEntries() == 0:
            return None
        cQueue.sortEntries()
        collisionPoint = cQueue.getEntry(0).getSurfacePoint(mazeNode)
        return collisionPoint[2]

    # figure out the extents of the maze
    class Crawler:
        NORTH=0
        WEST=1
        SOUTH=2
        EAST=3
        OFFSETS=[[0,-1],
                 [-1,0],
                 [0,1],
                 [1,0],
                 ]
        def __init__(self, startCoord=[0,0]):
            self.curCoord = startCoord
            self.minTX = self.maxTX = 0
            self.minTY = self.maxTY = 0
            
            self.__crawl()

        def __crawl(self):

            def applyDirection(coord, dir):
                offset = self.OFFSETS[dir % len(self.OFFSETS)]
                return [coord[0] + offset[0],
                        coord[1] + offset[1]]

            def isValidMove(coord, dir):
                newCoord = applyDirection(coord, dir)
                return None != calcHeight(*newCoord)

            def attemptMove():
                newCoord = applyDirection(self.curCoord, self.direction)
                if None == calcHeight(*newCoord):
                    return 0
                self.curCoord = newCoord
                # update the maze extents
                self.minTX = min(self.minTX, newCoord[0])
                self.maxTX = max(self.maxTX, newCoord[0])
                self.minTY = min(self.minTY, newCoord[1])
                self.maxTY = max(self.maxTY, newCoord[1])
                return 1

            # first, explore north from the origin
            self.direction = self.NORTH
            while attemptMove():
                pass

            # mark this coordinate as the 'termination coordinate';
            # we will trace around the edge of the maze until we get
            # back to this coord
            terminateCoord = self.curCoord
            leftTerminateCoord = 0

            # crawl the edge of the maze, counter-clockwise
            #
            # algorithm:
            # try to move forward
            # if you couldn't move forward, turn left
            # else if there is a valid space on your right, turn right
            while not (leftTerminateCoord and \
                       (self.curCoord == terminateCoord)):
                if not attemptMove():
                    # turn left
                    self.direction -= 1
                else:
                    leftTerminateCoord = 1
                    # should we turn right?
                    if isValidMove(self.curCoord, self.direction+1):
                        self.direction += 1

    crawler = Crawler()

    mazeWidth  = (crawler.maxTX - crawler.minTX) + 1
    mazeHeight = (crawler.maxTY - crawler.minTY) + 1

    # assuming minTX, minTY is (0,0), calculate the tile offset of the origin
    originTX = -crawler.minTX
    originTY = -crawler.minTY

    # WARNING: this syntax creates shallow copies of the inner list
    #collisionArray = [[0,] * mazeWidth] * mazeHeight

    # create the collision array
    collisionArray = []
    for i in range(mazeHeight):
        collisionArray.append([0,] * mazeWidth)

    def isWall(x,y):
        WALL_THRESHOLD = 1 # this should be higher than the floor,
                           # lower than the walls
        height = calcHeight(x,y)
        if height == None:
            # if there's no floor, treat it like a wall
            return 1
        if height < WALL_THRESHOLD:
            return 0
        return 1

    y = crawler.minTY; yIndex = 0
    while y <= crawler.maxTY:
        x = crawler.minTX; xIndex = 0
        while x <= crawler.maxTX:
            collisionArray[yIndex][xIndex] = isWall(x,y)
            #if isWall(x,y):
            #    print yIndex,xIndex,x,y,collisionArray[yIndex][xIndex]
            x += 1; xIndex += 1
        y += 1; yIndex += 1

    #print collisionArray

    #
    # clean up
    cNodePath.removeNode()

    # returns:
    # collision array (non-zero means wall),
    # maze width, maze height,
    # origin grid x index, origin grid y index
    return (collisionArray, mazeWidth, mazeHeight, originTX, originTY)

def calcTreasurePosList(collisionTable, mazeWidth, mazeHeight,
                        originX, originY):
    list = []
    DEADZONE_X_RADIUS = int((mazeWidth/6.)/2)
    DEADZONE_Y_RADIUS = int((mazeHeight/5.)/2)
    y = 0
    while y < mazeHeight-1:
        x = 0
        while x < mazeWidth-1:
            if (abs(x+1-originX) > DEADZONE_X_RADIUS) or \
               (abs(y+1-originY) > DEADZONE_Y_RADIUS):
                if (not collisionTable[y  ][x  ]) and \
                   (not collisionTable[y+1][x  ]) and \
                   (not collisionTable[y  ][x+1]) and \
                   (not collisionTable[y+1][x+1]):
                    list.append(
                        ((x+1-originX)*CELL_WIDTH,
                         (y+1-originY)*CELL_WIDTH,
                         0.1))
            x += 1
        y += 1

    return list


f = open(outputFile, "wb")

fwritelines(
    f,
    ['"""' + outputFile + ': GENERATED FILE, DO NOT EDIT"""',
     '',
     'CELL_WIDTH = ' + `CELL_WIDTH`,
     '',
     'mazeNames = ' + `mazeNames`,
     '',
     'mazeData = {}'
    ])

processedMazes = []
for mazeGroup in mazeNames:
    for mazeName in mazeGroup:
        if mazeName in processedMazes:
            print mazeName + " already added"
            continue
        else:
            processedMazes.append(mazeName)
    
        print "analyzing " + mazeName + "..."
        maze = loader.loadModel(mazeName)
        maze.reparentTo(root)
        maze.setPos(0,0,0)
        maze.setCollideMask(CollideMask)

        # get maze dimensions and boolean collision table
        mazeNode = maze.find("**/maze")
        collisionTable, mazeWidth, mazeHeight, \
                        originX, originY = \
                        calcMazeTopology(mazeNode)

        treasurePosList = calcTreasurePosList(collisionTable,
                                              mazeWidth, mazeHeight,
                                              originX, originY)

        fwrite(f,'')
        fwrite(f,'mazeData["' + mazeName + '"] = {}')
        fwrite(f,'data = mazeData["' + mazeName + '"]')
        fwrite(f,'data["width"] = ' + `mazeWidth`)
        fwrite(f,'data["height"] = ' + `mazeHeight`)
        fwrite(f,'data["originX"] = ' + `originX`)
        fwrite(f,'data["originY"] = ' + `originY`)
    
        fwrite(f,'data["collisionTable"] = [')
        for y in range(mazeHeight):
            f.write('  [')
            for x in range(mazeWidth):
                f.write(`collisionTable[y][x]` + ',')
            f.write('],\n')
        f.write('  ]\n')

        fwrite(f,'data["treasurePosList"] = [')
        for pos in treasurePosList:
            f.write(`pos` + ',\n')
        f.write('  ]\n')

f.close()
