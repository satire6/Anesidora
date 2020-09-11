from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import MintRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllCashbotInfo():
    # print out roomId->room name
    print 'roomId: roomName'
    for roomId, roomName in MintRoomSpecs.CashbotMintRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)
    # print out # of battles in each room
    print '\nroomId: numBattles'
    for roomId, numBattles in MintRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)
    # print out all of the rooms in all mint floors
    print '\nmintId floor roomIds'
    printMintRoomIds()
    # print out # of rooms in each mint floor
    print '\nmintId floor numRooms'
    printNumRooms()
    # print out # of non-skippable battles in each mint floor
    print '\nmintId floor numForcedBattles'
    printNumBattles()
    
# print out info on all mint levels for Cashbot
def iterateCashbotMints(func):
    # func takes MintLayout
    from toontown.toonbase import ToontownGlobals
    for mintId in [ToontownGlobals.CashbotMintIntA,
                   ToontownGlobals.CashbotMintIntB,
                   ToontownGlobals.CashbotMintIntC,]:
        for floorNum in xrange(ToontownGlobals.MintNumFloors[mintId]):
            func(MintLayout(mintId, floorNum))

def printMintInfo():
    def func(ml): print ml
    iterateCashbotMints(func)
def printMintRoomIds():
    def func(ml): print ml.getMintId(), ml.getFloorNum(), ml.getRoomIds()
    iterateCashbotMints(func)
def printMintRoomNames():
    def func(ml): print ml.getMintId(), ml.getFloorNum(), ml.getRoomNames()
    iterateCashbotMints(func)
def printNumRooms():
    def func(ml): print ml.getMintId(), ml.getFloorNum(), ml.getNumRooms()
    iterateCashbotMints(func)
def printNumBattles():
    def func(ml): print ml.getMintId(), ml.getFloorNum(), ml.getNumBattles()
    iterateCashbotMints(func)

BakedFloorLayouts = {
    12500: {0: (0, 4, 9, 6, 5, 8, 17,),
            1: (0, 15, 13, 16, 7, 6, 22,),
            2: (0, 4, 11, 3, 9, 6, 14, 19,),
            3: (0, 1, 3, 4, 16, 14, 15, 24,),
            4: (0, 15, 5, 8, 9, 11, 10, 21,),
            5: (0, 13, 12, 8, 7, 16, 10, 18,),
            6: (0, 16, 13, 5, 12, 7, 1, 23,),
            7: (0, 10, 12, 7, 3, 13, 16, 8, 20,),
            8: (0, 3, 5, 7, 6, 1, 4, 9, 25,),
            9: (0, 6, 9, 10, 13, 16, 8, 4, 22,),
            10: (0, 13, 1, 7, 2, 16, 11, 3, 19,),
            11: (0, 3, 1, 6, 4, 14, 8, 9, 24,),
            12: (0, 7, 14, 2, 1, 8, 5, 10, 11, 21,),
            13: (0, 13, 6, 4, 11, 3, 9, 10, 8, 17,),
            14: (0, 15, 5, 1, 14, 10, 4, 7, 16, 23,),
            15: (0, 16, 10, 11, 2, 1, 3, 14, 5, 20,),
            16: (0, 5, 8, 10, 6, 3, 15, 14, 7, 25,),
            17: (0, 12, 13, 5, 8, 14, 11, 7, 16, 10, 22,),
            18: (0, 11, 3, 15, 7, 16, 14, 6, 1, 5, 18,),
            19: (0, 10, 16, 11, 3, 5, 12, 13, 7, 14, 24,),
            },
    12600: {0: (0, 8, 1, 6, 14, 2, 5, 9, 17,),
            1: (0, 4, 14, 7, 2, 13, 8, 9, 18,),
            2: (0, 7, 9, 6, 5, 14, 12, 3, 20,),
            3: (0, 6, 2, 13, 16, 7, 5, 3, 9, 22,),
            4: (0, 15, 4, 9, 8, 6, 13, 5, 11, 23,),
            5: (0, 13, 7, 14, 15, 11, 3, 2, 8, 25,),
            6: (0, 5, 14, 2, 11, 7, 16, 10, 15, 18,),
            7: (0, 10, 9, 5, 4, 2, 7, 13, 11, 19,),
            8: (0, 11, 4, 12, 6, 1, 13, 7, 3, 21,),
            9: (0, 15, 16, 5, 13, 9, 14, 4, 6, 3, 23,),
            10: (0, 16, 15, 7, 6, 8, 3, 4, 9, 10, 24,),
            11: (0, 5, 8, 4, 12, 13, 9, 11, 16, 3, 17,),
            12: (0, 13, 16, 7, 4, 12, 3, 6, 5, 1, 19,),
            13: (0, 14, 6, 12, 13, 7, 10, 3, 16, 9, 20,),
            14: (0, 9, 15, 13, 5, 6, 3, 14, 11, 4, 22,),
            15: (0, 13, 14, 3, 12, 16, 11, 9, 4, 5, 7, 24,),
            16: (0, 3, 6, 1, 7, 5, 10, 9, 4, 13, 15, 25,),
            17: (0, 3, 6, 14, 4, 13, 16, 12, 8, 5, 7, 18,),
            18: (0, 11, 13, 4, 1, 15, 6, 3, 8, 9, 16, 20,),
            19: (0, 11, 5, 8, 7, 2, 6, 13, 3, 14, 9, 21,),
            },
    12700: {0: (0, 16, 14, 6, 1, 5, 9, 2, 15, 8, 17,),
            1: (0, 3, 2, 12, 14, 8, 13, 6, 10, 7, 23,),
            2: (0, 15, 9, 5, 12, 7, 4, 11, 14, 16, 21,),
            3: (0, 2, 13, 7, 6, 8, 15, 4, 1, 11, 19,),
            4: (0, 12, 7, 4, 6, 10, 14, 13, 16, 15, 11, 17,),
            5: (0, 10, 2, 9, 13, 4, 8, 1, 15, 14, 11, 23,),
            6: (0, 2, 14, 4, 10, 16, 15, 1, 3, 8, 6, 21,),
            7: (0, 14, 11, 1, 7, 9, 10, 12, 8, 5, 2, 19,),
            8: (0, 9, 11, 8, 5, 1, 4, 3, 7, 15, 2, 17,),
            9: (0, 2, 9, 7, 11, 16, 10, 15, 3, 8, 6, 23,),
            10: (0, 4, 10, 6, 8, 7, 15, 2, 1, 3, 13, 21,),
            11: (0, 10, 14, 8, 6, 9, 15, 5, 1, 2, 13, 19,),
            12: (0, 16, 5, 12, 10, 6, 9, 11, 3, 15, 13, 17,),
            13: (0, 1, 3, 6, 14, 4, 10, 12, 15, 13, 16, 24,),
            14: (0, 8, 7, 14, 9, 1, 2, 6, 16, 10, 15, 13, 21,),
            15: (0, 4, 1, 8, 11, 12, 3, 10, 16, 13, 6, 15, 19,),
            16: (0, 6, 3, 10, 4, 1, 2, 13, 11, 5, 15, 16, 17,),
            17: (0, 6, 16, 5, 12, 11, 1, 8, 14, 15, 9, 10, 24,),
            18: (0, 15, 8, 12, 10, 1, 7, 11, 9, 16, 4, 5, 21,),
            19: (0, 10, 2, 16, 5, 6, 11, 13, 7, 12, 1, 3, 19,),
            },
    }

"""
http://www.chem.qmul.ac.uk/software/download/qmc/ch5.pdf

Selections

We are often concerned with considering selections of objects, rather than
all the objects. In this instance it is important to distinguish between
two different possible situations; one in which the order of the objects is
important and one in which the order is not.

Example

It is possible to select two letters from the letters ABC in 3 ways: AB,
AC, BC. Each selection is called a combination.

However,

If the order of the selection matters then there are 6 ways: AB, BA, AC,
CA, BC, CB. Each arrangement is called a permutation.

In this case, therefore there are 3 combinations and 6 permutations of the
selected two letters.

In general, _provided_ that all the objects are different (dissimilar), then

- the number of combinations of r objects from n objects is:

nCr = n! / [(n-r)! r!]

- the number of permutations of r objects from n objects is:

nPr = n! / (n-r)!

The difference between the two formulae is a factor of r! - this is the
number of ways of arranging r dissimilar objects. For two different
letters, r = 2 and r! = 2 , i.e. for a pair of letters, then each letter
may come first or last, giving rise to two permutations for each
combination.
"""

"""
For the cashbot mint, we have 3 mints with 20 floors each, for a total of
60 floors. On average, we want each floor to have 5 rooms. Each floor is
created by stringing together a sequence of rooms from a central pool of
rooms. The question is: how many unique rooms do we need in order to create
60 unique floors by stringing those rooms together?

We definitely want combinations of rooms, not permutations. First, an
implementation of n-Choose-r:

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

def nCr(n,r):
    return factorial(n)/(factorial(n-r)*factorial(r))

n is the unknown; r is 5. We want nCr(n,5) >= 60.

>>> nCr(8,5)
56
>>> nCr(9,5)
126

We need at least 9 rooms to create 60 unique 5-room combinations.

**This isn't totally correct; we've got three types of rooms: entrances, middle rooms, and final rooms.
"""

class MintLayout:
    """Given a mintId and a floor number, generates a series of rooms and
    connecting hallways. This is used by the AI and the client, so the data
    it stores is symbolic (it doesn't load any models, it builds tables of
    IDs etc.)"""
    notify = DirectNotifyGlobal.directNotify.newCategory("MintLayout")

    def __init__(self, mintId, floorNum):
        self.mintId = mintId
        self.floorNum = floorNum
        self.roomIds = []
        self.hallways = []
        # add one room to account for the entrance room
        self.numRooms = 1 + (
            ToontownGlobals.MintNumRooms[self.mintId][self.floorNum])
        self.numHallways = self.numRooms - 1

        # if we have a baked floor layout, use it; otherwise generate a random
        # layout
        if ((self.mintId in BakedFloorLayouts) and
            (self.floorNum in BakedFloorLayouts[self.mintId])):
            self.roomIds = list(BakedFloorLayouts[self.mintId][self.floorNum])
        else:
            self.roomIds = self._genFloorLayout()

        # pick the hallways
        hallwayRng = self.getRng()
        connectorRoomNames = MintRoomSpecs.CashbotMintConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout(self):
        rng = self.getRng()

        # pick the rooms. Make sure we don't get any repeats.
        startingRoomIDs = MintRoomSpecs.CashbotMintEntranceIDs
        middleRoomIDs = MintRoomSpecs.CashbotMintMiddleRoomIDs
        finalRoomIDs = MintRoomSpecs.CashbotMintFinalRoomIDs

        # how many battles do we want?
        numBattlesLeft = ToontownGlobals.MintNumBattles[self.mintId]

        # pick the final room first, so we know how many battles we can
        # have in the middle rooms
        finalRoomId = rng.choice(finalRoomIDs)
        numBattlesLeft -= MintRoomSpecs.getNumBattles(finalRoomId)

        middleRoomIds = []
        middleRoomsLeft = self.numRooms-2

        # we want to hit our target number of battles exactly.
        # pick the battle rooms we will use first, then fill in pure-action
        # rooms

        # get dict of numBattles->list of rooms
        numBattles2middleRoomIds = invertDictLossless(
            MintRoomSpecs.middleRoomId2numBattles)

        # get list of all battle rooms
        allBattleRooms = []
        for num, roomIds in numBattles2middleRoomIds.items():
            if num > 0:
                allBattleRooms.extend(roomIds)

        # Pick out a list of battle rooms that meets our quota exactly.
        while 1:
            # make a copy of the list of battle rooms, and shuffle it
            allBattleRoomIds = list(allBattleRooms)
            rng.shuffle(allBattleRoomIds)
            battleRoomIds = self._chooseBattleRooms(numBattlesLeft,
                                                    allBattleRoomIds)
            if battleRoomIds is not None:
                break
            MintLayout.notify.info(
                'could not find a valid set of battle rooms, trying again')

        middleRoomIds.extend(battleRoomIds)
        middleRoomsLeft -= len(battleRoomIds)
        
        if middleRoomsLeft > 0:
            # choose action rooms for the rest of the middle rooms
            actionRoomIds = numBattles2middleRoomIds[0]
            for i in xrange(middleRoomsLeft):
                roomId = rng.choice(actionRoomIds)
                actionRoomIds.remove(roomId)
                middleRoomIds.append(roomId)

        roomIds = []
        # pick a starting room
        roomIds.append(rng.choice(startingRoomIDs))
        # add the chosen middle room IDs in random order
        rng.shuffle(middleRoomIds)
        roomIds.extend(middleRoomIds)
        # add the chosen final room
        roomIds.append(finalRoomId)
        return roomIds

    def getNumRooms(self):
        return len(self.roomIds)
    def getRoomId(self, n):
        return self.roomIds[n]
    def getRoomIds(self):
        return self.roomIds[:]
    def getRoomNames(self):
        names = []
        for roomId in self.roomIds:
            names.append(MintRoomSpecs.CashbotMintRoomId2RoomName[roomId])
        return names

    def getNumHallways(self):
        return len(self.hallways)
    def getHallwayModel(self, n):
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += MintRoomSpecs.roomId2numBattles[roomId]
        return numBattles

    def getMintId(self):
        return self.mintId
    def getFloorNum(self):
        return self.floorNum
    
    def getRng(self):
        # returns seeded rng corresponding to this mint floor
        return random.Random(self.mintId * self.floorNum)
    
    def _chooseBattleRooms(self,
                           numBattlesLeft,
                           allBattleRoomIds,
                           baseIndex=0,
                           chosenBattleRooms=None,
                           ):
        # returns list of battle room ids that exactly meet numBattlesLeft.
        # returns None if unable to exactly meet numBattlesLeft.
        # allBattleRoomIds is list of all roomIds to run through in order.

        if chosenBattleRooms is None:
            chosenBattleRooms = []

        # run through all the remaining available rooms, trying each one
        # in sequence as the 'next' room
        while baseIndex < len(allBattleRoomIds):
            # grab the next roomId off the full list
            nextRoomId = allBattleRoomIds[baseIndex]
            baseIndex += 1
            # using this room, how many battles do we still need to fulfill?
            newNumBattlesLeft = (
                numBattlesLeft -
                MintRoomSpecs.middleRoomId2numBattles[nextRoomId])
            if newNumBattlesLeft < 0:
                # nope, this room puts us over the limit. Try the next one.
                continue
            elif newNumBattlesLeft == 0:
                # woohoo! we've hit the limit exactly.
                chosenBattleRooms.append(nextRoomId)
                return chosenBattleRooms
            # let's see if we can hit the target using this room.
            # put the roomId on the 'chosen' list.
            chosenBattleRooms.append(nextRoomId)
            result = self._chooseBattleRooms(newNumBattlesLeft,
                                             allBattleRoomIds,
                                             baseIndex,
                                             chosenBattleRooms)
            if result is not None:
                # we hit the target. pass the result on down.
                return result
            else:
                # this room didn't work out. Pop it off the 'chosen' list
                # and try the next room.
                del chosenBattleRooms[-1:]
        else:
            # we've run out of rooms to try at this level of recursion.
            # return failure.
            return None

    def __str__(self):
        return ('MintLayout: id=%s, floor=%s, numRooms=%s, numBattles=%s' % (
            self.mintId, self.floorNum, self.getNumRooms(),
            self.getNumBattles()))
    def __repr__(self):
        return str(self)
    
