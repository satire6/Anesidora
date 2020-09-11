from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import StageRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllCashbotInfo():
    # print out roomId->room name
    print 'roomId: roomName'
    for roomId, roomName in StageRoomSpecs.CashbotStageRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)
    # print out # of battles in each room
    print '\nroomId: numBattles'
    for roomId, numBattles in StageRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)
    # print out all of the rooms in all stage floors
    print '\nstageId floor roomIds'
    printStageRoomIds()
    # print out # of rooms in each stage floor
    print '\nstageId floor numRooms'
    printNumRooms()
    # print out # of non-skippable battles in each stage floor
    print '\nstageId floor numForcedBattles'
    printNumBattles()
    
# print out info on all stage levels for Lawbot
def iterateLawbotStages(func):
    # func takes StageLayout
    from toontown.toonbase import ToontownGlobals
    for layoutId in xrange(len(stageLayouts)):
        for floorNum in xrange(getNumFloors(layoutId)):
            func(StageLayout(0, floorNum, layoutId))

def printStageInfo():
    def func(sl): print sl
    iterateLawbotStages(func)
def printRoomUsage():
    usage = {}
    def func(sl):
        for roomId in sl.getRoomIds():
            usage.setdefault(roomId, 0)
            usage[roomId] += 1
    iterateLawbotStages(func)
    roomIds = usage.keys()
    roomIds.sort()
    for roomId in roomIds:
        print '%s: %s' % (roomId, usage[roomId])
def printRoomInfo():
    roomIds = StageRoomSpecs.roomId2numCogs.keys()
    roomIds.sort()
    for roomId in roomIds:
        print 'room %s: %s cogs, %s cogLevels, %s merit cogLevels' % (
            roomId, StageRoomSpecs.roomId2numCogs[roomId],
            StageRoomSpecs.roomId2numCogLevels[roomId],
            StageRoomSpecs.roomId2numMeritCogLevels[roomId])
def printStageRoomIds():
    def func(ml): print ml.getStageId(), ml.getFloorNum(), ml.getRoomIds()
    iterateCashbotStages(func)
def printStageRoomNames():
    def func(ml): print ml.getStageId(), ml.getFloorNum(), ml.getRoomNames()
    iterateCashbotStages(func)
def printNumRooms():
    def func(ml): print ml.getStageId(), ml.getFloorNum(), ml.getNumRooms()
    iterateCashbotStages(func)
def printNumBattles():
    def func(ml): print ml.getStageId(), ml.getFloorNum(), ml.getNumBattles()
    iterateCashbotStages(func)


    
DefaultLayout1 ={0: (0, 1, 2, 3, 1, 2, 4,),
            1: (0, 1, 2, 3, 1, 2, 4,),
            2: (0, 1, 2, 3, 1, 2, 4,),
            3: (0, 1, 2, 3, 1, 2, 4,),
            4: (0, 1, 2, 3, 1, 2, 4,),
            5: (0, 1, 2, 3, 1, 2, 4,),
            6: (0, 1, 2, 3, 1, 2, 4,),
            7: (0, 1, 2, 3, 1, 2, 4,),
            8: (0, 1, 2, 3, 1, 2, 4,),
            9: (0, 1, 2, 3, 1, 2, 4,),
            10: (0, 1, 2, 3, 1, 2, 4,),
            11: (0, 1, 2, 3, 1, 2, 4,),
            12: (0, 1, 2, 3, 1, 2, 4,),
            13: (0, 1, 2, 3, 1, 2, 4,),
            14: (0, 1, 2, 3, 1, 2, 4,),
            15: (0, 1, 2, 3, 1, 2, 4,),
            16: (0, 1, 2, 3, 1, 2, 4,),
            17: (0, 1, 2, 3, 1, 2, 4,),
            18: (0, 1, 2, 3, 1, 2, 4,),
            19: (0, 1, 2, 3, 1, 2, 4,),
            },
            
            
DefaultLayout =[(0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    (0, 5, 2, 3, 5, 2, 1,),
                    ]
                    
testLayout =[(0, 3, 8, 105, 1,),
                    (0, 7, 8, 105, 2,),
                    ]

# entrance
# 0,
# middle
# 7, 8, 10, 11, 12, 100, 101, 102, 103, 104, 105
# final
# 1, 2,

# cog rooms
"""
>>> from toontown.coghq import StageLayout
>>> StageLayout.printRoomInfo()
room 0: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 1: 4 cogs, 45 cogLevels, 45 merit cogLevels
room 2: 4 cogs, 45 cogLevels, 45 merit cogLevels
room 3: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 7: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 8: 8 cogs, 84 cogLevels, 0 merit cogLevels
room 10: 8 cogs, 84 cogLevels, 0 merit cogLevels
room 11: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 12: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 100: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 101: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 102: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 103: 0 cogs, 0 cogLevels, 0 merit cogLevels
room 104: 4 cogs, 42 cogLevels, 42 merit cogLevels
room 105: 4 cogs, 42 cogLevels, 42 merit cogLevels
"""
"""
room frequency (by merits)

0: start room
1,2: end room

0-cog
=====
3: 9
7: 9
8: 19 # laser
10: 16 # laser
11: 9
12: 12 # gag barrels
100: 8
101: 8
102: 8
103: 10

4-cog
=====
104: 21
105: 21

"""

LawOfficeLayout2_0 =[(0, 7, 8, 105, 1,),
                     (0, 10, 104, 103, 1,),
                     (0, 105, 101, 12, 2,),
                     ]

LawOfficeLayout2_1 =[(0, 10, 11, 104, 1,),
                     (0, 100, 105, 8, 1,),
                     (0, 103, 3, 104, 2,),
                     ]

LawOfficeLayout2_2 =[(0, 8, 105, 102, 1,),
                     (0, 100, 104, 10, 1),
                     (0, 101, 105, 3, 2,),
                     ]

LawOfficeLayout3_0 =[(0, 8, 101, 104, 1,),
                     (0, 7, 105, 103, 1,),
                     (0, 100, 8, 104, 1,),
                     (0, 105, 10, 12, 2,),
                     ]

LawOfficeLayout3_1 =[(0, 100, 8, 105, 1,),
                     (0, 103, 10, 104, 1,),
                     (0, 8, 7, 105, 1,),
                     (0, 104, 12, 101, 2,),
                     ]

LawOfficeLayout3_2 =[(0, 103, 104, 100, 1,),
                     (0, 102, 8, 105, 1,),
                     (0, 10, 104, 3, 1,),
                     (0, 105, 10, 11, 2,),
                     ]
            
LawOfficeLayout4_0 =[(0, 3, 7, 105, 1,),
                     (0, 103, 104, 8, 1,),
                     (0, 102, 105, 11, 1,),
                     (0, 8, 104, 100, 1,),
                     (0, 10, 105, 12, 2,),
                     ]
            
LawOfficeLayout4_1 =[(0, 7, 105, 102, 1,),
                     (0, 103, 12, 104, 1,),
                     (0, 101, 104, 8, 1,),
                     (0, 10, 3, 105, 1,),
                     (0, 8, 104, 102, 2,),
                     ]
            
LawOfficeLayout4_2 =[(0, 11, 105, 102, 1,),
                     (0, 3, 104, 8, 1,),
                     (0, 100, 10, 104, 1,),
                     (0, 8, 12, 105, 1,),
                     (0, 104, 102, 11, 2,),
                     ]
            
LawOfficeLayout5_0 =[(0, 104, 10, 7, 1,),
                     (0, 105, 103, 3, 1,),
                     (0, 104, 11, 12, 1,),
                     (0, 101, 8, 105, 1,),
                     (0, 10, 104, 12, 1,),
                     (0, 105, 100, 7, 2,),
                     ]
            
LawOfficeLayout5_1 =[(0, 11, 8, 104, 1,),
                     (0, 102, 10, 105, 1,),
                     (0, 104, 7, 101, 1,),
                     (0, 105, 10, 12, 1,),
                     (0, 8, 11, 105, 1,),
                     (0, 104, 12, 3, 2,),
                     ]
            
LawOfficeLayout5_2 =[(0, 105, 103, 8, 1,),
                     (0, 10, 3, 104, 1,),
                     (0, 105, 103, 101, 1,),
                     (0, 12, 8, 104, 1,),
                     (0, 7, 11, 104, 1,),
                     (0, 105, 12, 10, 2,),
                     ]
            
stageLayouts = [LawOfficeLayout2_0,
                LawOfficeLayout2_1,
                LawOfficeLayout2_2,
                LawOfficeLayout3_0,
                LawOfficeLayout3_1,
                LawOfficeLayout3_2,
                LawOfficeLayout4_0,
                LawOfficeLayout4_1,
                LawOfficeLayout4_2,
                LawOfficeLayout5_0,
                LawOfficeLayout5_1,
                LawOfficeLayout5_2,
                ]
                
stageLayouts1 = [testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                testLayout,
                ]

def getNumFloors(layoutIndex):
    return len(stageLayouts[layoutIndex])

class StageLayout:
    """Given a stageId and a floor number, generates a series of rooms and
    connecting hallways. This is used by the AI and the client, so the data
    it stores is symbolic (it doesn't load any models, it builds tables of
    IDs etc.)"""
    notify = DirectNotifyGlobal.directNotify.newCategory("StageLayout")

    def __init__(self, stageId, floorNum, stageLayout = 0):
        self.stageId = stageId
        self.floorNum = floorNum
        self.roomIds = []
        self.hallways = []
        self.layoutId = stageLayout

        self.roomIds = stageLayouts[stageLayout][floorNum]

        # add one room to account for the entrance room
        self.numRooms = 1 + len(self.roomIds)
        self.numHallways = self.numRooms - 1

        # if we have a baked floor layout, use it; otherwise generate a random
        # layout
        #if ((self.stageId in BakedFloorLayouts) and
        #    (self.floorNum in BakedFloorLayouts[self.stageId])):
        #    self.roomIds = list(BakedFloorLayouts[self.stageId][self.floorNum])flo
        #else:
        #    assert 0, "Stage not in baked layouts!!"

        # pick the hallways
        hallwayRng = self.getRng()
        connectorRoomNames = StageRoomSpecs.CashbotStageConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))
            
        #import pdb; pdb.set_trace()



    def getNumRooms(self):
        return len(self.roomIds)
    def getRoomId(self, n):
        return self.roomIds[n]
    def getRoomIds(self):
        return self.roomIds[:]
    def getRoomNames(self):
        names = []
        for roomId in self.roomIds:
            names.append(StageRoomSpecs.CashbotStageRoomId2RoomName[roomId])
        return names

    def getNumHallways(self):
        return len(self.hallways)
    def getHallwayModel(self, n):
       return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += StageRoomSpecs.roomId2numBattles[roomId]
        return numBattles

    def getNumCogs(self):
        numCogs = 0
        for roomId in self.getRoomIds():
            numCogs += StageRoomSpecs.roomId2numCogs[roomId]
        return numCogs
    def getNumCogLevels(self):
        numLevels = 0
        for roomId in self.getRoomIds():
            numLevels += StageRoomSpecs.roomId2numCogLevels[roomId]
        return numLevels
    def getNumMeritCogLevels(self):
        numLevels = 0
        for roomId in self.getRoomIds():
            numLevels += StageRoomSpecs.roomId2numMeritCogLevels[roomId]
        return numLevels

    def getStageId(self):
        return self.stageId
    def getFloorNum(self):
        return self.floorNum
    
    def getRng(self):
        # returns seeded rng corresponding to this stage floor
        return random.Random(self.stageId * self.floorNum)
    

    def __str__(self):
        return ('StageLayout: id=%s, layout=%s, floor=%s, meritCogLevels=%s, numRooms=%s, numBattles=%s, numCogs=%s' % (
            self.stageId, self.layoutId, self.floorNum, self.getNumMeritCogLevels(),
            self.getNumRooms(), self.getNumBattles(), self.getNumCogs()))
            
    def __repr__(self):
        return str(self)

