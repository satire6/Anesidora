"""DropPlacer module: contains the DropPlacer base class and derived drop placer classes"""

from direct.showbase.RandomNumGen import RandomNumGen
import CatchGameGlobals
import DropScheduler
from toontown.parties.PartyGlobals import CatchActivityDuration as PartyCatchDuration

# in order to cleanly support different drop 'behaviors', we
# define some classes that choose where to drop things

class DropPlacer:
    """
    this is a base class for objects that will 'place'
    drops according to varying criteria
    'game' should be the catch game object
    'dropTypes' should be a list of drop type names
    """
    def __init__(self, game, dropTypes, startTime=None):
        self.game = game
        self.dropTypes = dropTypes
        self.dtIndex = 0
        self._createScheduler(startTime)
        self._createRng()

    def _createScheduler(self, startTime):
        self.scheduler = DropScheduler.DropScheduler(
            CatchGameGlobals.GameDuration,
            self.game.FirstDropDelay,
            self.game.DropPeriod,
            self.game.MaxDropDuration,
            self.game.FasterDropDelay,
            self.game.FasterDropPeriodMult,
            startTime=startTime)

    def _createRng(self):
        self.rng = self.game.randomNumGen

    def skipPercent(self, percent):
        numSkips = self.scheduler.skipPercent(percent)
        self.dtIndex += numSkips
        return numSkips

    def doneDropping(self, continuous=None):
        """
        returns true when all of the drops have been scheduled
        """
        return self.scheduler.doneDropping(continuous)

    def getDuration(self):
        return self.scheduler.getDuration()

    # DropPlacer implementations should call this to get the
    # current time value
    def getT(self):
        return self.scheduler.getT()

    # DropPlacer implementations should call this after
    # scheduling each drop
    def stepT(self):
        self.scheduler.stepT()

    # DropPlacer implementations should call this function to
    # get the next drop type name
    def getNextDropTypeName(self):
        # if we run out of pre-chosen drop types, drop
        # anvils (i.e. preserve the fruit count; see comments above)
        if self.dtIndex >= len(self.dropTypes):
            self.game.notify.debug('warning: defaulting to anvil')
            typeName = 'anvil'
        else:
            typeName = self.dropTypes[self.dtIndex]
        self.dtIndex += 1
        return typeName

    def getRandomColRow(self):
        # returns a random [column, row] pair
        col = self.rng.randrange(0, self.game.DropColumns)
        row = self.rng.randrange(0, self.game.DropRows)
        return [col, row]

    def getNextDrop(self):
        """
        This function declaration serves only to informally
        define the getNextDrop() interface.
        
        returns list:
        [t, dropTypeName, [gridColumn, gridRow]]
        t is the starting time of the drop, relative to game time
        dropTypeName is the name of the type of object to drop
        gridColumn and gridRow are grid coordinates, zero-based
        """
        raise RuntimeError, \
              'DropPlacer.getNextDrop should never be called'

class RandomDropPlacer(DropPlacer):
    """
    this is the simplest DropPlacer. It just drops items
    in random locations.
    """
    def __init__(self, game, dropTypes, startTime=None):
        DropPlacer.__init__(self, game, dropTypes, startTime=startTime)

    def getNextDrop(self):
        """
        tries to return a drop located in an empty drop region
        see declaration of DropPlacer.getNextDrop, above, for details
        """
        col,row = self.getRandomColRow()
        drop = [self.getT(), self.getNextDropTypeName(), [col,row]]
        self.stepT()
        return drop

class RegionDropPlacer(DropPlacer):
    """
    this DropPlacer will attempt to schedule drops so that
    there is no more than one item dropping in any particular
    'drop region' simultaneously; drop regions are groups of
    drop grid locations that are located in screen space such
    that it's hard to match up multiple drop shadows with
    their respective falling objects (locations are close in X).
    """

    # falling items that don't differ significantly in their screenspace
    # X coordinate tend to be confusing; it's hard to match up
    # a particular item to its shadow when there are several
    # candidate shadows. Therefore, we divide the drop grid
    # into several numbered regions, and stipulate that there
    # should be no more than one falling item per region.
    DropRegionTables = [
        [[1,1,2,3,3],
         [1,1,2,3,3],
         [0,1,2,3,4],
         [0,1,2,3,4],
         [0,1,2,3,4],
         ],
        [[1,2,2,3,3,4],
         [1,1,2,3,4,4],
         [1,1,2,3,4,4],
         [0,1,2,3,4,5],
         [0,1,2,3,4,5],
         [0,1,2,3,4,5],
         ],
        [[1,1,2,2,2,3,3],
         [1,1,2,2,2,3,3],
         [0,1,2,2,2,3,4],
         [0,1,2,2,2,3,4],
         [0,1,2,2,2,3,4],
         [0,1,2,2,2,3,4],
         [0,1,2,2,2,3,4],
         ],
        [[1,2,2,5,6,7,7,3],
         [1,1,2,5,6,7,3,3],
         [0,1,2,5,6,7,3,4],
         [0,1,2,5,6,7,3,4],
         [0,1,2,5,6,7,3,4],
         [0,1,2,5,6,7,3,4],
         [0,1,2,5,6,7,3,4],
         [0,0,1,5,6,3,4,4],
         ],
        [[1,2,2,5,8,6,7,7,3],
         [1,1,2,5,8,6,7,3,3],
         [0,1,2,5,8,6,7,3,4],
         [0,1,2,5,8,6,7,3,4],
         [0,1,2,5,8,6,7,3,4],
         [0,1,2,5,8,6,7,3,4],
         [0,1,2,5,8,6,7,3,4],
         [0,1,2,5,8,6,7,3,4],
         [0,0,1,5,8,6,3,4,4],
         ],
        [[1,2,2,5,8,8,6,7,7,3],
         [1,1,2,5,8,8,6,7,3,3],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,1,2,5,8,8,6,7,3,4],
         [0,0,1,5,8,8,6,3,4,4],
         ],
        [[1,2,2,5,8,10,9,6,7,7,3],
         [1,1,2,5,8,10,9,6,7,3,3],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,1,2,5,8,10,9,6,7,3,4],
         [0,0,1,5,8,10,9,6,3,4,4],
         ],
        [[1,2,2,5,8,10,10,9,6,7,7,3],
         [1,1,2,5,8,10,10,9,6,7,3,3],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,1,2,5,8,10,10,9,6,7,3,4],
         [0,0,1,5,8,10,10,9,6,3,4,4],
         ],
        [[1,2,2,5,8,10,11,12,9,6,7,7,3],
         [1,1,2,5,8,10,11,12,9,6,7,3,3],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,1,2,5,8,10,11,12,9,6,7,3,4],
         [0,0,1,5,8,10,11,12,9,6,3,4,4],
         ],
        ]
    Players2dropTable = [
        DropRegionTables[0],
        DropRegionTables[0],
        DropRegionTables[0],
        DropRegionTables[1],
        DropRegionTables[1],
        DropRegionTables[2],
        DropRegionTables[3],
        DropRegionTables[3],
        DropRegionTables[4],
        DropRegionTables[4],
        DropRegionTables[5],
        DropRegionTables[5],
        DropRegionTables[5],
        DropRegionTables[6],
        DropRegionTables[6],
        DropRegionTables[7],
        DropRegionTables[7],
        DropRegionTables[7],
        DropRegionTables[8],
        DropRegionTables[8],
        ]

    @classmethod
    def getDropRegionTable(cls, numPlayers):
        return cls.Players2dropTable[min(len(cls.Players2dropTable)-1, numPlayers)]

    def __init__(self, game, dropTypes, startTime=None):
        DropPlacer.__init__(self, game, dropTypes, startTime=startTime)
                
        self.DropRegionTable = self.getDropRegionTable(self.game.getNumPlayers())

        assert (len(self.DropRegionTable) == self.game.DropRows)
        assert (len(self.DropRegionTable[0]) == self.game.DropColumns)
        # create a dict that maps drop regions to lists of grid coords
        self.DropRegion2GridCoordList = {}
        for row in range(len(self.DropRegionTable)):
            rowList = self.DropRegionTable[row]
            for column in range(len(rowList)):
                region = rowList[column]
                if not self.DropRegion2GridCoordList.has_key(region):
                    self.DropRegion2GridCoordList[region] = []
                self.DropRegion2GridCoordList[region].append(
                    [row,column])
        # and create a sorted list of drop regions
        self.DropRegions = self.DropRegion2GridCoordList.keys()
        self.DropRegions.sort()

        # keep track of which drop regions have an object in them
        self.emptyDropRegions = self.DropRegions[:]
        self.fallingObjs = []

    def getNextDrop(self):
        """
        tries to return a drop located in an empty drop region
        see declaration of DropPlacer.getNextDrop, above, for details
        """
        t = self.getT()
                
        # will any of the falling objects have landed at this point?
        while len(self.fallingObjs):
            landTime, dropRegion = self.fallingObjs[0]
            # is the oldest object still falling?
            if landTime > t:
                break
            # remove the oldest object; it's landed
            self.fallingObjs = self.fallingObjs[1:]
            # add the drop region back to the available list
            # BUG: the drop regions should have reference counts
            if dropRegion not in self.emptyDropRegions:
                self.emptyDropRegions.append(dropRegion)

        # choose a drop region that's empty; if they're
        # all full, choose any region
        candidates = self.emptyDropRegions
        if len(candidates) == 0:
            candidates = self.DropRegions
        dropRegion = self.rng.choice(candidates)
        # choose a drop row/col in the drop region
        row,col = self.rng.choice(
            self.DropRegion2GridCoordList[dropRegion])
        dropTypeName = self.getNextDropTypeName()
        drop = [t, dropTypeName, [row,col]]

        # add this drop to the priority queue of drops/regions
        duration = self.game.BaselineDropDuration
        self.fallingObjs.append([t + duration, dropRegion])
        if dropRegion in self.emptyDropRegions:
            self.emptyDropRegions.remove(dropRegion)

        self.stepT()
        return drop

class PartyRegionDropPlacer(RegionDropPlacer):
    def __init__(self, game, generationId, dropTypes, startTime=None):
        self.generationId = generationId
        RegionDropPlacer.__init__(self, game, dropTypes, startTime=startTime)

    def _createRng(self):
        self.rng = RandomNumGen(self.generationId + self.game.doId)

    def _createScheduler(self, startTime):
        self.scheduler = DropScheduler.ThreePhaseDropScheduler(
            PartyCatchDuration,
            self.game.FirstDropDelay,
            self.game.DropPeriod,
            self.game.MaxDropDuration,
            self.game.SlowerDropPeriodMult,
            self.game.NormalDropDelay,
            self.game.FasterDropDelay,
            self.game.FasterDropPeriodMult,
            startTime=startTime)

class PathDropPlacer(DropPlacer):
    """
    this placer drops objects along random 'paths', one
    for each player. The idea is to keep players from frequently
    having to run back and forth across the entire stage.
    """
    def __init__(self, game, dropTypes, startTime=None):
        DropPlacer.__init__(self, game, dropTypes, startTime=startTime)

        # these represent the possible drop location moves that a
        # path can take, in clockwise order
        self.moves = [
            [ 0,-1], # 0, N
            [ 1,-1], # 1, NE
            [ 1, 0], # 2, E
            [ 1, 1], # 3, SE
            [ 0, 1], # 4, S
            [-1, 1], # 5, SW
            [-1, 0], # 6, W
            [-1,-1], # 7, NW
            ]

        # create a list of 'path' descriptors, one for each player
        # be careful to create N *unique* descriptors, not N
        # references to a single descriptor
        self.paths = []
        for i in xrange(self.game.getNumPlayers()):
            # create a new path descriptor and add it to the list
            dir = self.rng.randrange(0,len(self.moves))
            col,row = self.getRandomColRow()
            path = {
                'direction' : dir,
                'location'  : [col,row],
                }
            self.paths.append(path)

        # as we drop items, we'll determine the path locations
        # by cycling through the self.paths list in round-robin fashion
        self.curPathIndex = 0

    def getValidDirection(self, col, row, dir):
        # these lists map invalid directions to the closest valid direction(s)
        # for paths that are at the playfield boundaries
        redirectTop    = [(6,2),2,2,3,4,5,6,6]
        redirectRight  = [0,0,(0,4),4,4,5,6,7]
        redirectBottom = [0,1,2,2,(2,6),6,6,7]
        redirectLeft   = [0,1,2,3,4,4,(4,0),0]
        redirectTopRight    = [6,(6,4),4,4,4,5,6,6]
        redirectBottomRight = [0,0,0,(0,6),6,6,6,7]
        redirectBottomLeft  = [0,1,2,2,2,(2,0),0,0]
        redirectTopLeft     = [2,2,2,3,4,4,4,(4,2)]

        # this is a lookup table to efficiently find the appropriate
        # redirect table
        # mid=00,min=01,max=10,unused=11
        # CCRRb, C=col, R=row
        tables = [               # indx, COL/ROW
            None,                # 0000, mid/mid
            redirectTop,         # 0001, mid/min
            redirectBottom,      # 0010, mid/max
            None,                # 0011, unused
            redirectLeft,        # 0100, min/mid
            redirectTopLeft,     # 0101, min/min
            redirectBottomLeft,  # 0110, min/max
            None,                # 0111, unused
            redirectRight,       # 1000, max/mid
            redirectTopRight,    # 1001, max/min
            redirectBottomRight, # 1010, max/max
            ]

        # calculate the index, based on col and row being on
        # max or min boundaries
        if col == 0:
            colIndex = 1
        elif col == (self.game.DropColumns-1):
            colIndex = 2
        else:
            colIndex = 0
        if row == 0:
            rowIndex = 1
        elif row == (self.game.DropRows-1):
            rowIndex = 2
        else:
            rowIndex = 0
        # column is the 2 high bits
        index = (colIndex << 2) + rowIndex

        redirectTable = tables[index]
        if not redirectTable:
            return dir

        # get a valid direction; might be a list of valid directions
        newDir = redirectTable[dir]
        if type(newDir) != type(1):
            newDir = self.rng.choice(newDir)
        return newDir
        
    def getNextDrop(self):
        """
        schedules the next drop, continuing one of the 'drop paths'
        """
        # get a handle on the current path
        path = self.paths[self.curPathIndex]

        col,row = path['location']
        dir = path['direction']

        # should the path turn or keep going in the same direction?
        turns = [-1, 0, 0, 1]
        turn = self.rng.choice(turns)
        # apply the turn to the path's direction
        if turn:
            dir = ((dir + turn) % len(self.moves))

        # make sure our direction is appropriate, wrt the playfield
        # boundaries
        dir = self.getValidDirection(col, row, dir)

        # step the path's drop location, according to the path
        # direction
        dCol, dRow = self.moves[dir]
        col += dCol
        row += dRow
        col = min(max(col, 0), self.game.DropColumns-1)
        row = min(max(row, 0), self.game.DropRows-1)

        path['location'] = [col,row]
        path['direction'] = dir

        # round-robin to the next drop path
        self.curPathIndex = ((self.curPathIndex+1) %
                             len(self.paths))
                
        drop = [self.getT(), self.getNextDropTypeName(), [col,row]]
        self.stepT()
        return drop
