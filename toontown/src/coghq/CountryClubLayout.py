from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import invertDictLossless
from toontown.coghq import CountryClubRoomSpecs
from toontown.toonbase import ToontownGlobals
from direct.showbase.PythonUtil import normalDistrib, lerp
import random

def printAllBossbotInfo():
    # print out roomId->room name
    print 'roomId: roomName'
    for roomId, roomName in CountryClubRoomSpecs.BossbotCountryClubRoomId2RoomName.items():
        print '%s: %s' % (roomId, roomName)
    # print out # of battles in each room
    print '\nroomId: numBattles'
    for roomId, numBattles in CountryClubRoomSpecs.roomId2numBattles.items():
        print '%s: %s' % (roomId, numBattles)
    # print out all of the rooms in all countryClub floors
    print '\ncountryClubId floor roomIds'
    printCountryClubRoomIds()
    # print out # of rooms in each countryClub floor
    print '\ncountryClubId floor numRooms'
    printNumRooms()
    # print out # of non-skippable battles in each countryClub floor
    print '\ncountryClubId floor numForcedBattles'
    printNumBattles()
    
# print out info on all countryClub levels for Bossbot
def iterateBossbotCountryClubs(func):
    # func takes CountryClubLayout
    from toontown.toonbase import ToontownGlobals
    for countryClubId in [ToontownGlobals.BossbotCountryClubIntA,
                   ToontownGlobals.BossbotCountryClubIntB,
                   ToontownGlobals.BossbotCountryClubIntC,]:
        for floorNum in xrange(ToontownGlobals.CountryClubNumFloors[countryClubId]):
            func(CountryClubLayout(countryClubId, floorNum))

def printCountryClubInfo():
    def func(ml): print ml
    iterateBossbotCountryClubs(func)
def printCountryClubRoomIds():
    def func(ml): print ml.getCountryClubId(), ml.getFloorNum(), ml.getRoomIds()
    iterateBossbotCountryClubs(func)
def printCountryClubRoomNames():
    def func(ml): print ml.getCountryClubId(), ml.getFloorNum(), ml.getRoomNames()
    iterateBossbotCountryClubs(func)
def printNumRooms():
    def func(ml): print ml.getCountryClubId(), ml.getFloorNum(), ml.getNumRooms()
    iterateBossbotCountryClubs(func)
def printNumBattles():
    def func(ml): print ml.getCountryClubId(), ml.getFloorNum(), ml.getNumBattles()
    iterateBossbotCountryClubs(func)



ClubLayout3_0 = [(0, 2, 5, 9, 17,), 
                 (0, 2, 4, 9, 17,),
                 (0, 2, 5, 9, 18,),
                 ]
ClubLayout3_1 = [(0, 2, 5, 9, 17,),
                 (0, 2, 4, 9, 17,),
                 (0, 2, 5, 9, 18,),
                 ]

ClubLayout3_2 = [(0, 2, 4, 9, 17,),
                 (0, 2, 4, 9, 17,),
                 (0, 2, 6, 9, 18,),
                 ]
                 
ClubLayout6_0 = [(0, 22, 4, 29, 17,),
                 (0, 22, 5, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 5, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 5, 29, 18,),
                 ]

ClubLayout6_1 = [(0, 22, 4, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 4, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 4, 29, 17,),
                 (0, 22, 6, 29, 18,),
                 ]
                 
ClubLayout6_2 = [(0, 22, 4, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 5, 29, 17,),
                 (0, 22, 6, 29, 17,),
                 (0, 22, 5, 29, 17,),
                 (0, 22, 7, 29, 18,),
                 ]
                 
ClubLayout9_0 = [(0, 32, 4, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 6, 39, 18,),
                 ]

ClubLayout9_1 = [(0, 32, 4, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 7, 39, 17,),
                 (0, 32, 7, 39, 18,),
                 ]
                 
ClubLayout9_2 = [(0, 32, 5, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 5, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 6, 39, 17,),
                 (0, 32, 7, 39, 18,),
                 ]

countryClubLayouts = [ClubLayout3_0,
                   ClubLayout3_1,
                   ClubLayout3_2,
                   ClubLayout6_0,
                   ClubLayout6_1,
                   ClubLayout6_2,
                   ClubLayout9_0,
                   ClubLayout9_1,
                   ClubLayout9_2,
               ]

testLayout =  [ClubLayout3_0,
               ClubLayout3_0,
               ClubLayout3_0,
               ClubLayout6_0,
               ClubLayout6_0,
               ClubLayout6_0,
               ClubLayout9_0,
               ClubLayout9_0,
               ClubLayout9_0,
               ]

countryClubLayouts = testLayout
               

class CountryClubLayout:
    """Given a countryClubId and a floor number, generates a series of rooms and
    connecting hallways. This is used by the AI and the client, so the data
    it stores is symbolic (it doesn't load any models, it builds tables of
    IDs etc.)"""
    notify = DirectNotifyGlobal.directNotify.newCategory("CountryClubLayout")

    def __init__(self, countryClubId, floorNum ,layoutIndex):
        self.countryClubId = countryClubId
        self.floorNum = floorNum
        self.layoutIndex = layoutIndex
        self.roomIds = []
        self.hallways = []
        # add one room to account for the entrance room
        #self.numRooms = 1 + (
        #    ToontownGlobals.CountryClubNumRooms[self.countryClubId][self.floorNum])
        self.numRooms = 1 + (
            ToontownGlobals.CountryClubNumRooms[self.countryClubId][0])        
        self.numHallways = self.numRooms - 1 + 1 # (add 1 for final room)

        self.roomIds = countryClubLayouts[layoutIndex][floorNum]
        
        
        # pick the hallways
        hallwayRng = self.getRng()
        connectorRoomNames = CountryClubRoomSpecs.BossbotCountryClubConnectorRooms
        for i in xrange(self.numHallways):
            self.hallways.append(hallwayRng.choice(connectorRoomNames))

    def _genFloorLayout(self):
        rng = self.getRng()

        # pick the rooms. Make sure we don't get any repeats.
        startingRoomIDs = CountryClubRoomSpecs.BossbotCountryClubEntranceIDs
        middleRoomIDs = CountryClubRoomSpecs.BossbotCountryClubMiddleRoomIDs
        finalRoomIDs = CountryClubRoomSpecs.BossbotCountryClubFinalRoomIDs

        # how many battles do we want?
        numBattlesLeft = ToontownGlobals.CountryClubNumBattles[self.countryClubId]

        # pick the final room first, so we know how many battles we can
        # have in the middle rooms
        finalRoomId = rng.choice(finalRoomIDs)
        numBattlesLeft -= CountryClubRoomSpecs.getNumBattles(finalRoomId)

        middleRoomIds = []
        middleRoomsLeft = self.numRooms-2

        # we want to hit our target number of battles exactly.
        # pick the battle rooms we will use first, then fill in pure-action
        # rooms

        # get dict of numBattles->list of rooms
        numBattles2middleRoomIds = invertDictLossless(
            CountryClubRoomSpecs.middleRoomId2numBattles)

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
            CountryClubLayout.notify.info(
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
        #rng.shuffle(middleRoomIds)
        # temp only for debugging
        middleRoomIds.sort()
        print('middleRoomIds=%s' % middleRoomIds)
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
            names.append(CountryClubRoomSpecs.BossbotCountryClubRoomId2RoomName[roomId])
        return names

    def getNumHallways(self):
        return len(self.hallways)
    def getHallwayModel(self, n):
        return self.hallways[n]

    def getNumBattles(self):
        numBattles = 0
        for roomId in self.getRoomIds():
            numBattles += CountryClubRoomSpecs.roomId2numBattles[roomId]
        return numBattles

    def getCountryClubId(self):
        return self.countryClubId
    def getFloorNum(self):
        return self.floorNum
    
    def getRng(self):
        # returns seeded rng corresponding to this countryClub floor
        return random.Random(self.countryClubId * self.floorNum)
    
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
                CountryClubRoomSpecs.middleRoomId2numBattles[nextRoomId])
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
        return ('CountryClubLayout: id=%s, layoutIndex=%s, floor=%s, numRooms=%s, numBattles=%s' % (
            self.countryClubId, self.layoutIndex, self.floorNum, self.getNumRooms(),
            self.getNumBattles()))
    def __repr__(self):
        return str(self)
    
