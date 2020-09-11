import DatabaseObject
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import intersection
from toontown.toon import DistributedToonAI
from toontown.estate import DistributedHouseAI
from toontown.pets import DistributedPetAI
from toontown.toon import InventoryBase
from pandac.PandaModules import *
from toontown.quest import Quests
from toontown.toon import NPCToons
import time

HEAL_TRACK = 0
TRAP_TRACK = 1
LURE_TRACK = 2
SOUND_TRACK = 3
THROW_TRACK = 4
SQUIRT_TRACK = 5
DROP_TRACK = 6

class AvatarGetter(DirectObject.DirectObject):
    # Gets just one avatar at a time.  You can munge properties on the
    # avatar and write it back to the database.  self.av is the
    # avatar.

    # An incrementing sequence number unique to each getter object.
    nextSequence = 1

    def __init__(self, air):
        self.air = air
        self.dclass = self.air.dclassesByName['DistributedToonAI']
        self.av = None
        self.gotAvatarEvent = 'AvatarGetter-%s' % (self.nextSequence)
        AvatarGetter.nextSequence += 1

    def getAvatar(self, avId, fields=None, event=None):
        # Requests a particular avatar.  The avatar will be requested
        # from the database and stored in self.av when the response is
        # heard back from the database, at some time in the future.
        self.av = None
        self.event = event

        self.acceptOnce(self.gotAvatarEvent, self.__gotData)

        db = DatabaseObject.DatabaseObject(self.air, avId)
        db.doneEvent = self.gotAvatarEvent
        if fields is None:
            fields = db.getDatabaseFields(self.dclass)
        elif 'setDNAString' not in fields:
            # we need this to check if it's a Toon
            fields.append('setDNAString')
        db.getFields(fields)
        print "Avatar %s requested." % avId

    def saveAvatarAll(self):
        # Writes all the fields on the current avatar back to the
        # database.
        db = DatabaseObject.DatabaseObject(self.air, self.av.doId)
        db.storeObject(self.av)
        print "Saved avatar %s." % (self.av.doId)

    def saveAvatar(self, *fields):
        # Writes only the named fields (strings passed as parameters)
        # on the current avatar back to the database.
        if (len(fields) == 0):
            print "Specify the fields to save in the parameter list, or use saveAvatarAll()."
        else:
            db = DatabaseObject.DatabaseObject(self.air, self.av.doId)
            db.storeObject(self.av, fields)
            print "Saved %d fields on avatar %s." % (len(fields), self.av.doId)

    def __gotData(self, db, retcode):
        if retcode == 0 and db.values.has_key('setDNAString'):
            self.av = DistributedToonAI.DistributedToonAI(self.air)
            self.av.doId = db.doId
            self.av.inventory = InventoryBase.InventoryBase(self.av)
            self.av.teleportZoneArray = []
            db.fillin(self.av, self.dclass)

            # to prevent mem leaks, you should call toon.patchDelete at
            # some point.

            print 'Got avatar %s, "%s".' % (self.av.doId, self.av.name)
            if self.event is not None:
                messenger.send(self.event, [self.av])
        else:
            print "Could not get avatar %s, retcode = %s." % (db.doId, retcode)
            if self.event is not None:
                messenger.send(self.event, [None])

class AvatarIterator(DirectObject.DirectObject):

    # The maximum number of outstanding requests to make to the server
    # at once.
    maxRequests = 20

    # When we come to this many non-avatars in a row, assume we have
    # reached the end of the database.
    endOfListCount = 20

    # The amount of time, in seconds, to elapse between displaying
    # successive avatars.
    printInterval = 1.0

    # An incrementing sequence number unique to each iterator object.
    nextSequence = 1

    def __init__(self, air):
        self.air = air
        self.dclass = self.air.dclassesByName['DistributedToonAI']
        self.dnaDict = {}
        self.nextObjId = None
        self.objIdList = None  # Fill this with a list of objId's to iterate through the list.
        self.requested = []
        self.nonAvatar = 0
        self.gotAvatarEvent = 'AvatarIterator-%s' % (self.nextSequence)
        AvatarIterator.nextSequence += 1

    def start(self, startId = 100000000):
        self.startTime = time.time()
        if self.objIdList != None:
            # Iterate through an explicit list
            self.nextObjId = None
            self.objIdIndex = 0
        else:
            # Iterate through the whole database
            self.nextObjId = startId
        self.accept(self.gotAvatarEvent, self.__gotData)
        self.requested = []
        self.lastPrintTime = 0
        self.getNextAvatar()

    def stop(self):
        self.ignoreAll()
        
    def getNextAvatar(self):
        while len(self.requested) < self.maxRequests:
            if self.nextObjId != None:
                db = DatabaseObject.DatabaseObject(self.air, self.nextObjId)
                db.doneEvent = self.gotAvatarEvent
                db.getFields(self.fieldsToGet(db))
                self.requested.append(self.nextObjId)

            if self.objIdList != None:
                # Iterate through an explicit list
                if self.objIdIndex >= len(self.objIdList):
                    # Done.
                    self.nextObjId = None
                    if len(self.requested) == 0:
                        self.done()
                    return
                
                self.nextObjId = int(self.objIdList[self.objIdIndex])
                self.objIdIndex += 1

            else:
                # Iterate through the whole database
                self.nextObjId += 2
        
    def fieldsToGet(self, db):
        return db.getDatabaseFields(self.dclass)

    def __gotData(self, db, retcode):
        self.requested.remove(db.doId)
        if retcode == 0 and db.values.has_key('setMoney'):
            av = DistributedToonAI.DistributedToonAI(self.air)
            av.doId = db.doId
            av.inventory = InventoryBase.InventoryBase(av)
            av.teleportZoneArray = []
            db.fillin(av, self.dclass)
            self.processAvatar(av, db)
            self.nonAvatar = 0
        else:
            if self.objIdList != None:
                print "Not an avatar: %s" % (db.doId)
            self.nonAvatar += 1

        if self.objIdList != None or self.nonAvatar < self.endOfListCount:
            self.getNextAvatar()
        elif len(self.requested) == 0:
            self.stop()
            self.done()

    def printSometimes(self, av):
        now = time.time()
        if now - self.lastPrintTime > self.printInterval:
            print "%d: %s" % (av.doId, av.name)
            self.lastPrintTime = now

    def processAvatar(self, av, db):
        self.printSometimes(av)

    def done(self):
        now = time.time()
        print "done, %s seconds." % (now - self.startTime)


class HouseIterator(DirectObject.DirectObject):

    # The maximum number of outstanding requests to make to the server
    # at once.
    maxRequests = 20

    # When we come to this many non-houses in a row, assume we have
    # reached the end of the database.
    endOfListCount = 20

    # The amount of time, in seconds, to elapse between displaying
    # successive houses.
    printInterval = 1.0

    # An incrementing sequence number unique to each iterator object.
    nextSequence = 1

    def __init__(self, air):
        self.air = air
        self.dclass = self.air.dclassesByName['DistributedHouseAI']
        self.dnaDict = {}
        self.nextObjId = None
        self.objIdList = None  # Fill this with a list of objId's to iterate through the list.
        self.requested = []
        self.nonHouse = 0
        self.gotHouseEvent = 'HouseIterator-%s' % (self.nextSequence)
        HouseIterator.nextSequence += 1

    def start(self, startId = 100000000):
        self.startTime = time.time()
        if self.objIdList != None:
            # Iterate through an explicit list
            self.nextObjId = None
            self.objIdIndex = 0
        else:
            # Iterate through the whole database
            self.nextObjId = startId
        self.accept(self.gotHouseEvent, self.__gotData)
        self.requested = []
        self.lastPrintTime = 0
        self.getNextHouse()

    def stop(self):
        self.ignoreAll()
        
    def getNextHouse(self):
        while len(self.requested) < self.maxRequests:
            if self.nextObjId != None:
                db = DatabaseObject.DatabaseObject(self.air, self.nextObjId)
                db.doneEvent = self.gotHouseEvent
                db.getFields(self.fieldsToGet(db))
                self.requested.append(self.nextObjId)

            if self.objIdList != None:
                # Iterate through an explicit list
                if self.objIdIndex >= len(self.objIdList):
                    # Done.
                    self.nextObjId = None
                    if len(self.requested) == 0:
                        self.done()
                    return
                
                self.nextObjId = int(self.objIdList[self.objIdIndex])
                self.objIdIndex += 1

            else:
                # Iterate through the whole database
                self.nextObjId += 2
        
    def fieldsToGet(self, db):
        return db.getDatabaseFields(self.dclass)

    def __gotData(self, db, retcode):
        self.requested.remove(db.doId)
        if retcode == 0 and (db.values.has_key('setHouseType') or
                             db.values.has_key('setInteriorWallpaper')):
            # Fill in dummy values of estateId, zoneId, and posIndex
            house = DistributedHouseAI.DistributedHouseAI(
                self.air, db.doId, 0, 0, 0)
            db.fillin(house, self.dclass)
            self.processHouse(house, db)
            self.nonHouse = 0
        else:
            if self.objIdList != None:
                print "Not a house: %s" % (db.doId)
            self.nonHouse += 1

        if self.objIdList != None or self.nonHouse < self.endOfListCount:
            self.getNextHouse()
        elif len(self.requested) == 0:
            self.stop()
            self.done()

    def printSometimes(self, house):
        now = time.time()
        if now - self.lastPrintTime > self.printInterval:
            print "%d: %s" % (house.doId, house.name)
            self.lastPrintTime = now

    def processHouse(self, house, db):
        self.printSometimes(house)

    def done(self):
        now = time.time()
        print "done, %s seconds." % (now - self.startTime)


class PetIterator(DirectObject.DirectObject):

    # The maximum number of outstanding requests to make to the server
    # at once.
    maxRequests = 10

    # When we come to this many non-pets in a row, assume we have
    # reached the end of the database.
    endOfListCount = 20

    # The amount of time, in seconds, to elapse between displaying
    # successive pets.
    printInterval = 1.0

    # An incrementing sequence number unique to each iterator object.
    nextSequence = 1

    def __init__(self, air):
        self.air = air
        self.dclass = self.air.dclassesByName['DistributedPetAI']
        self.dnaDict = {}
        self.startId = None
        self.endId = None
        self.nextObjId = None
        self.objIdList = None  # Fill this with a list of objId's to iterate through the list.
        self.requested = []
        self.nonPet = 0
        self.gotPetEvent = 'PetIterator-%s' % (self.nextSequence)
        PetIterator.nextSequence += 1

    def start(self, startId = 100000000):
        self.startTime = time.time()
        if self.objIdList != None:
            # Iterate through an explicit list
            self.nextObjId = None
            self.objIdIndex = 0
        else:
            # Iterate through the whole database
            if self.startId == None:
                self.startId = startId
            self.nextObjId = self.startId
        self.accept(self.gotPetEvent, self.__gotData)
        self.requested = []
        self.lastPrintTime = 0
        self.getNextPet()

    def timeToStop(self):
        # override this and return True when appropriate
        if self.objIdList != None:
            return False
        return self.nonPet >= self.endOfListCount
    
    def stop(self):
        self.ignoreAll()
        
    def getNextPet(self):
        if self.timeToStop():
            return
        while len(self.requested) < self.maxRequests:
            if self.nextObjId != None:
                db = DatabaseObject.DatabaseObject(self.air, self.nextObjId)
                db.doneEvent = self.gotPetEvent
                db.getFields(self.fieldsToGet(db))
                self.requested.append(self.nextObjId)

            if self.objIdList != None:
                # Iterate through an explicit list
                if self.objIdIndex >= len(self.objIdList):
                    # Done.
                    self.nextObjId = None
                    if len(self.requested) == 0:
                        self.done()
                    return
                
                self.nextObjId = int(self.objIdList[self.objIdIndex])
                self.objIdIndex += 1

            else:
                # Iterate through the whole database
                self.nextObjId += 2
        
    def fieldsToGet(self, db):
        return db.getDatabaseFields(self.dclass)

    def __gotData(self, db, retcode):
        self.requested.remove(db.doId)
        if retcode == 0 and len(intersection(db.values.keys(),
                                             self.fieldsToGet(None))) > 0:
            pet = DistributedPetAI.DistributedPetAI(self.air)
            db.fillin(pet, self.dclass)
            self.processPet(pet, db)
            self.nonPet = 0
        else:
            if self.objIdList != None:
                print "Not a pet: %s" % (db.doId)
            self.nonPet += 1
            self.getNextPet()

        if self.timeToStop() and (len(self.requested) == 0):
            self.stop()
            self.done()

    def printSometimes(self, pet):
        now = time.time()
        if now - self.lastPrintTime > self.printInterval:
            percent = None
            if self.objIdList != None:
                percent = 100. * self.objIdIndex / len(self.objIdList)
            elif self.endId is not None:
                percent = 100. * ((self.nextObjId - self.startId) /
                                 (self.endId - self.startId))
            if percent is not None:
                print "%s%% complete, %s seconds" % (percent,
                                                     (now - self.startTime))
            else:
                print "%d: %s, %s seconds" % (pet.doId, pet.petName,
                                              (now - self.startTime))
            self.lastPrintTime = now

    def processPet(self, pet, db):
        self.printSometimes(pet)

    def done(self):
        now = time.time()
        print "done, %s seconds." % (now - self.startTime)


class AvatarFixer(AvatarIterator):
    def processAvatar(self, av, db):
        self.printSometimes(av)

        changed = av.fixAvatar()
        if changed:
            db2 = DatabaseObject.DatabaseObject(self.air, av.doId)
            db2.storeObject(av, db.values.keys())
            print "%d: %s repaired (account %s)." % (av.doId, av.name, av.accountName)
        return

        numTracks = reduce(lambda a, b: a+b, av.trackArray)
        hp = av.maxHp
        healExp, trapExp, lureExp, soundExp, throwExp, squirtExp, dropExp  = av.experience.experience
        trackProgressId, trackProgress = av.getTrackProgress()
        trackAccess = av.getTrackAccess()
        maxMoney = av.getMaxMoney()
        fixed = 0

        for questDesc in av.quests:

            questId = questDesc[0]
            rewardId = questDesc[3]
            toNpc = questDesc[2]

            if (not Quests.questExists(questId)):
                print 'WARNING: av has quest that is not in quest dict: ', av.doId, questId
                continue

            if (questId in [160, 161, 162, 161]):
                if rewardId != 100:
                    print ('WARNING: av has quest: %s with reward: %s' % (questId, rewardId))
                    questDesc[3] = 100
                    fixed = 1
                    continue

            if (rewardId == 1000):
                if (questId in [1100, 1101, 1102, 1103, 2500, 2501, 3500, 3501, 4500, 4501, 5500, 5501, 7500, 7501, 9500, 9501]):
                    # not fixing because this clothing quest is valid
                    break
                av.removeAllTracesOfQuest(questId, rewardId)
                fixed = 1
                continue
            
            if ((toNpc != 1000) and
                (NPCToons.NPCToonDict[toNpc][5] == NPCToons.NPC_HQ)):
                print ('WARNING: av has quest: %s to visit NPC_HQ: %s' % (questId, toNpc))
                print 'before: ', av.quests
                questDesc[2] = Quests.ToonHQ
                print 'after: ', av.quests
                fixed = 1
                continue

        # If there were any quest fixes, broadcast them now
        if fixed:
            av.b_setQuests(av.quests)

        # Make sure they are not training any tracks they have already trained
        if (trackProgressId >= 0) and (trackAccess[trackProgressId] == 1):
            print ("WARNING: av training track he already has")
            print "Track progress id: ", trackProgressId
            print "Track access: ", trackAccess
            print "Tier: ", av.rewardTier
            if av.rewardTier in [0, 1]:
                print "ERROR: You should not be here"
            elif av.rewardTier in [2, 3]:
                print 'sound or heal'
                if av.trackArray[SOUND_TRACK] and not av.trackArray[HEAL_TRACK]:
                    trackProgressId = HEAL_TRACK
                elif av.trackArray[HEAL_TRACK] and not av.trackArray[SOUND_TRACK]:
                    trackProgressId = SOUND_TRACK
                else:
                    trackProgressId = HEAL_TRACK
                av.b_setTrackProgress(trackProgressId, trackProgress)
                print "Fixed trackProgressId: ", trackProgressId
                fixed = 1
                
            elif av.rewardTier in [4]:
                print "ERROR: You should not be here"
            elif av.rewardTier in [5, 6]:
                print 'drop or lure'
                if av.trackArray[DROP_TRACK] and not av.trackArray[LURE_TRACK]:
                    trackProgressId = LURE_TRACK
                elif av.trackArray[LURE_TRACK] and not av.trackArray[DROP_TRACK]:
                    trackProgressId = DROP_TRACK
                else:
                    trackProgressId = DROP_TRACK
                av.b_setTrackProgress(trackProgressId, trackProgress)                    
                print "Fixed trackProgressId: ", trackProgressId
                fixed = 1
            elif av.rewardTier in [7]:
                print "ERROR: You should not be here"
            elif av.rewardTier in [8]:
                print "ERROR: You should not be here"
            elif av.rewardTier in [9, 10]:
                print 'trap or heal, trap or sound'
                if av.trackArray[SOUND_TRACK] and not av.trackArray[HEAL_TRACK]:
                    trackProgressId = HEAL_TRACK
                elif av.trackArray[HEAL_TRACK] and not av.trackArray[SOUND_TRACK]:
                    trackProgressId = SOUND_TRACK
                else:
                    trackProgressId = TRAP_TRACK
                av.b_setTrackProgress(trackProgressId, trackProgress)                    
                print "Fixed trackProgressId: ", trackProgressId
                fixed = 1
            elif av.rewardTier in [11]:
                print "ERROR: You should not be here"
            elif av.rewardTier in [12, 13]:
                print 'all sort of choices'
                if not av.trackArray[HEAL_TRACK]:
                    trackProgressId = HEAL_TRACK
                elif not av.trackArray[SOUND_TRACK]:
                    trackProgressId = SOUND_TRACK
                elif not av.trackArray[DROP_TRACK]:
                    trackProgressId = DROP_TRACK
                elif not av.trackArray[LURE_TRACK]:
                    trackProgressId = LURE_TRACK
                elif not av.trackArray[TRAP_TRACK]:
                    trackProgressId = TRAP_TRACK
                else:
                    print "ERROR"
                av.b_setTrackProgress(trackProgressId, trackProgress)                    
                print "Fixed trackProgressId: ", trackProgressId
                fixed = 1
            else:
                print "ERROR: You should not be here"
            print

        # clean up track access
        if av.fixTrackAccess():
            fixed = 1

        # This was an unfortunate typo in Quests.py
        if maxMoney == 10:
            print 'bad maxMoney limit == 10'
            av.b_setMaxMoney(100)
            # Fill er up cause we feel bad
            av.b_setMoney(100)
            fixed = 1

        if av.rewardTier == 5:
            if hp < 25 or hp > 34:
                print 'bad hp: ',

            # Somehow they got here without choosing a track
            if trackProgressId == -1:
                print 'bad track training in tier 5!'
                print ('avId: %s, trackProgressId: %s, trackProgress: %s' %
                       (av.doId, trackProgressId, trackProgress))
                av.b_setQuestHistory([])
                av.b_setQuests([])
                # Make them choose again
                av.b_setRewardHistory(4, [])
                av.b_setTrackProgress(-1, 0)
                av.fixAvatar()
                av.inventory.zeroInv()
                av.inventory.maxOutInv()
                av.d_setInventory(av.inventory.makeNetString())
                print 'new track access: ', av.trackArray
                fixed = 1

        elif av.rewardTier == 7:
            if hp < 34 or hp > 43:
                print 'bad hp: ',
            if trackProgressId != -1:
                print 'bad track training in tier 7!'
                av.b_setQuestHistory([])
                av.b_setQuests([])
                av.b_setRewardHistory(7, [])
                av.b_setTrackProgress(-1, 0)
                av.fixAvatar()
                av.inventory.zeroInv()
                av.inventory.maxOutInv()
                av.d_setInventory(av.inventory.makeNetString())
                fixed = 1

        else:
            # Nothing to fix here
            pass

        if fixed:
            db = DatabaseObject.DatabaseObject(self.air, av.doId)
            db.storeObject(av)
            print "Avatar repaired."
            print

        return

class AvatarPrinter(AvatarIterator):

    def __init__(self, air):
        AvatarIterator.__init__(self, air)
        self.hoodInfoStore = HoodInfoStore()

    def processAvatar(self, av, db):
        numFriends = 0
        numSecretFriends = 0
        cogCount = 0

        for friend in av.friendsList:
            numFriends += 1
            if friend[1]:
                numSecretFriends += 1

        for cogTotal in av.cogCounts:
            cogCount += cogTotal

        #if ((av.maxHp == 15) and
        #    (av.experience.experience[0] +
        #     av.experience.experience[1] +
        #     av.experience.experience[2] +
        #     av.experience.experience[3] +
        #     av.experience.experience[4] +
        #     av.experience.experience[5] +
        #     av.experience.experience[6]  == 0) and
        #    numFriends == 0):
        #    # Do not count this fella
        #    return


        #oldDna = self.backupDict.get(av.doId)
        #newDna = av.dna.asTuple()
        #if oldDna and (oldDna != newDna):
        #    print '================'
        #    print av.doId
        #    print oldDna
        #    print newDna
            
        #self.dnaDict[av.doId] = av.dna.asTuple()
        #print av.doId, ' finished' #, av.name, "dna: ", av.dna.asTuple()
        #return
        #import ToonDNA
        #newDNA = ToonDNA.ToonDNA()
        #newDNA.newToonFromProperties(*av.dna.asTuple())
        #print 'old: ', av.dna
        #print 'new: ', newDNA

        if av.doId % 10000 == 0:
            print ("Working on avatar: %s" % av.doId)
        #print ("%s, %s, %s, %s, %s" %
        # (av.doId, av.maxHp, len(av.hoodsVisited), len(av.safeZonesVisited), cogCount))
        self.hoodInfoStore.record(av.maxHp, len(av.hoodsVisited), len(av.safeZonesVisited))
        return

        print ("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" %
               (av.doId,
                av.name,
                av.maxHp,
                av.dna.head,
                av.dna.topTex,
                av.dna.botTex,
                av.dna.armColor,
                av.dna.legColor,
                av.dna.headColor,
                numFriends,
                numSecretFriends,
                len(av.hoodsVisited),
                av.rewardTier,
                av.trackArray,
                av.trackProgressId,
                av.trackProgress,
                # Experience is a tuple of 6 values
                av.experience.experience[0],
                av.experience.experience[1],
                av.experience.experience[2],
                av.experience.experience[3],
                av.experience.experience[4],
                av.experience.experience[5],
                av.experience.experience[6],
                ))
                                     


class HoodInfoStore:
    def __init__(self):
        self.__printCount = 0
        # Init the values to 0
        self.avatarCount = {15:0,
                            16:0,
                            17:0,
                            18:0,
                            19:0,
                            20:0,
                            }
        self.hoodsVisited = {15: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             16: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             17: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             18: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             19: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             20: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                             }
        self.safeZonesVisited = {15: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 16: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 17: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 18: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 19: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 20: {1:0, 2:0, 3:0, 4:0, 5:0, 6:0},
                                 }

    def maybePrint(self):
        self.__printCount += 1
        if self.__printCount % 100 == 0:
            for hp, count in self.avatarCount.items():
                if count > 0:
                    print ("hp: %d  count: %d  hoods: %s  sz: %s" %
                           (hp, count, self.hoodsVisited[hp], self.safeZonesVisited[hp]))
            print
                
    def record(self, hp, numHoods, numSafeZones):
        self.maybePrint()
        if hp < 21:
            self.avatarCount[hp] += 1
            self.hoodsVisited[hp][numHoods] += 1
            self.safeZonesVisited[hp][numSafeZones] += 1

    
"""
import UtilityStart
import RepairAvatars
r = RepairAvatars.AvatarFixer(simbase.air)
r.start()


import UtilityStart
import RepairAvatars
r = RepairAvatars.AvatarPrinter(simbase.air)
h = RepairAvatars.HoodInfoStore()
r.start()




for avId, backupDna in backupDict.items():
    newDna = newDict.get(avId):
    if newDna and (newDna != backupDna):
        print "================"
        print avId
        print backupDna
        print newDna

from toontown.toon import DistributedToonAI
from toontown.toon import ToonDNA
from toontown.toon import InventoryBase
def fixAv(doId):
    av = DistributedToonAI.DistributedToonAI(simbase.air)
    av.doId = doId
    print doId
    av.inventory = InventoryBase.InventoryBase(av)
    av.teleportZoneArray = []
    db = DatabaseObject.DatabaseObject(simbase.air, av.doId)
    db.fillin(av, simbase.air.dclassesByName['DistributedToonAI'])
    oldD = oldDna.get(doId)
    print 'backup DNA', oldD
    newD = ToonDNA.ToonDNA()
    newD.newToonFromProperties(*oldD)
    print '   new DNA', newD.asTuple()
    av.b_setDNAString(newD.makeNetString())
    db.storeObject(av, ["setDNAString"])
    print 'done'

def fixAv(doId):
    
av = DistributedToonAI.DistributedToonAI(simbase.air)
av.doId = doId
db = DatabaseObject.DatabaseObject(simbase.air, av.doId)
db.getFields(db.getDatabaseFields(simbase.air.dclassesByName['DistributedToonAI']))
db.fillin(av, simbase.air.dclassesByName['DistributedToonAI'])
print doId
progressId, progress = av.getTrackProgress()
trackAccess = av.getTrackAccess()
print "old progressId: %s progress: %s" % (progressId, progress)
print "trackAccess: ", trackAccess
print "Tier: ", av.rewardTier
# av.b_setTrackProgress(trackId, progress)
# db.storeObject(av, ["setTrackProgress"])
print 'done'
    
"""
