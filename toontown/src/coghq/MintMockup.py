from pandac.PandaModules import *
from direct.showbase.PythonUtil import Enum
import random

def zoneNum2str(num):
    return 'ZONE%02i.mb' % num

class Room(NodePath):
    ModulePath = '/i/beta/toons/maya/work/CogHeadquarters/CogFactoriesInteriors/AllFactories/MintFactory/'

    StartingRooms  = ('ZONE03a.mb', 'ZONE16a.mb')
    MiddleRooms    = ('ZONE04a.mb', 'ZONE07a.mb', 'ZONE08a.mb', 'ZONE10a.mb',
                      'ZONE13a.mb', 'ZONE15a.mb', 'ZONE17a.mb', 'ZONE18a.mb',
                      'ZONE19a.mb')
    ConnectorRooms = ('connectors/connector_7cubeL2.mb',
                      'connectors/connector_7cubeR2.mb')
    EndingRooms    = ('ZONE11a.mb', 'ZONE22a.mb', 'ZONE31a.mb')

    AllRooms = StartingRooms + MiddleRooms + ConnectorRooms + EndingRooms

    def __init__(self, name=None, num=None, dbg=0):
        self.loaded = False
        self.num = num
        self.name = name
        NodePath.__init__(self, hidden.attachNewNode(
            'MintRoom-%s' % self._getModelName()))
        self.load()
        self.reparentTo(render)
        if dbg:
            self.showAxes()
            self.ls()
            print self.getPos(render)

    def __del__(self):
        self.unload()

    def load(self):
        if self.loaded:
            return
        self.loaded = True
        self.model = loader.loadModel(
            Room.ModulePath + self._getModelName())
        self.model.reparentTo(self)
        self.entrances = self._getEntrances()
        self.exits = self._getExits()

    def attachTo(self, other, otherDoor=None, thisDoor=None, rng=random):
        assert len(other.exits)
        assert len(self.entrances)
        if otherDoor is None:
            otherDoor = rng.choice(other.exits)
        if thisDoor is None:
            thisDoor = rng.choice(self.entrances)
        self.reparentTo(otherDoor)
        self.clearMat()
        # position our door at our origin so that it's on top of the other door
        self.model.setPos(Vec3(0)-thisDoor.getPos(self.model))
        # rotate so that our door is facing the right way
        self.setH(-thisDoor.getH(otherDoor))
        #print 'H: %s' % self.getH()
        self.wrtReparentTo(other.getParent())

    def showAxes(self):
        self.axes = []
        axis = loader.loadModel("models/misc/xyzAxis.bam")
        axis.setColorOff()
        # last 1 overrides default colorScale
        axis.setColorScale(1,1,1,1,1)
        for doorway in self.entrances + self.exits:
            self.axes.append(axis.copyTo(doorway))
        self.axes.append(axis.copyTo(self.model))
        self.axes[-1].setScale(.6)

    def isolateAxis(self, index):
        for i in range(len(self.axes)):
            if i == index:
                self.axes[i].show()
            else:
                self.axes[i].hide()

    def hideAxes(self):
        for axis in self.axes:
            axis.removeNode()
        del self.axes

    def unload(self):
        if not self.loaded:
            return
        self.loaded = False
        self.model.removeNode()

    def _getModelName(self):
        if self.name is not None:
            return self.name
        return zoneNum2str(self.num)

    def _getEntrances(self):
        return self.model.findAllMatches('**/ENTRANCE*')
    def _getExits(self):
        return self.model.findAllMatches('**/EXIT*')

class MintLevel(NodePath):
    def __init__(self, roomNames):
        # roomNames is list of room module model names
        NodePath.__init__(self, hidden.attachNewNode('MintLevel'))
        self.rooms = []
        for name in roomNames:
            room = Room(name=name)
            if not len(self.rooms):
                room.reparentTo(self)
            else:
                room.attachTo(self.rooms[-1])
            self.rooms.append(room)

def createLevel(numRooms=None, seed=None, rooms=None):
    # pass in # of rooms/rand seed, OR list of room #s/names
    # # of rooms & rand seed both default to 'pick at random'
    if rooms is None:
        if seed is None:
            seed = random.randrange(0,50)
        rng = random.Random(seed)

        if numRooms is None:
            numRooms = rng.randrange(2,8)
        assert numRooms>=2

        StartingRooms = Room.StartingRooms
        EndingRooms = Room.EndingRooms
        MiddleRooms = list(Room.MiddleRooms)
        MiddleRooms.sort()

        roomNames = []
        def getARoom(choices, rng, alreadyChosen):
            while 1:
                room = rng.choice(choices)
                if room not in alreadyChosen:
                    return room
        def addRoomWithConnector(roomName, rng):
            # no connector if this is the first room
            if len(roomNames):
                connector = rng.choice(Room.ConnectorRooms)
                roomNames.append(connector)
            roomNames.append(roomName)
        # pick a starting room
        addRoomWithConnector(getARoom(StartingRooms, rng, roomNames), rng)
        for i in range(numRooms-2):
            addRoomWithConnector(getARoom(MiddleRooms, rng, roomNames), rng)
        # pick an ending room
        addRoomWithConnector(getARoom(EndingRooms, rng, roomNames), rng)
    else:
        roomNames = []
        for roomName in rooms:
            if type(roomName) == type(1):
                roomName = zoneNum2str(roomName)
            roomNames.append(roomName)

    #print roomNames
    return MintLevel(roomNames)

class MintDemo:
    def __init__(self):
        self.level = None
        self.newLevel()
    def destroy(self):
        self.level.removeNode()
        try:
            base.cr.playGame.hood.loader.geom.unstash()
        except:
            pass
    def cache(self):
        # cache all the modules in memory
        for name in Room.AllRooms:
            r = Room(name=name)
            r.unload()
    def newLevel(self, numRooms=None):
        if numRooms == None:
            numRooms = random.randrange(3,7)
        if self.level is not None:
            self.level.removeNode()
            self.level = None
        try:
            base.cr.playGame.hood.loader.geom.stash()
        except:
            pass
        self.level = createLevel(numRooms=numRooms)
        self.level.reparentTo(render)
        base.localAvatar.clearMat()

"""
from toontown.coghq import MintMockup
roomLists=[[3,4,6,7,8,10,13,14,15,17,18,19,24,27,11],[3,20],[16,22],[3,30],[16,31]]

# make sure we cover all the rooms
from PythonUtil import union, sameElements
assert(sameElements(MintMockup.Room.Model2doorways.keys(), map(MintMockup.zoneNum2str, reduce(union, roomLists)) + list(MintMockup.Room.ConnectorRooms)))

levels=[]
for list in roomLists:
    rooms = []
    for room in list:
        if len(rooms):
            rooms.append(random.choice(MintMockup.Room.ConnectorRooms))
        rooms.append(room)
    levels.append(MintMockup.createLevel(rooms=rooms))
    levels[-1].reparentTo(hidden)

levels[0].reparentTo(render)
"""
