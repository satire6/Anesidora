from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.showbase import PythonUtil
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import Functor
import DistributedEstateAI
from direct.task.Task import Task
import DistributedHouseAI
import HouseGlobals
import random

TELEPORT_TO_OWNER_ONLY = 0

class EstateManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("EstateManagerAI")
    #notify.setDebug(True)

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.previousZone = None
        self.refCount = {}      # dict of lists containing avId's visiting an estate. keyed on owner's avId
        self.estateZone = {}    # dict of tuple of [zoneId, isOwner, userName] keyed on avId
        self.estate = {}        # dict of DistributedEstateAI's keyed on avId
        self.house = {}         # dict of lists of DistributedHouseAI's keyed on avId
        self.account2avId = {}  # mapping of userName to avId that created estate
        self.toBeDeleted = {}   # temporary list of av's to be deleted after a delay
        self.zone2owner = {}    # get the owner of a zone
        self.houseZone2estateZone = {}
        self.avId2pendingEnter = {} # table of avatars that are on their way to an estate

        # Number of seconds between spontaneous heals
        self.healFrequency = 30 # seconds

        self.randomGenerator = random.Random()

        return None

    def delete(self):
        self.notify.debug("BASE: delete: deleting EstateManagerAI object")
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)
        for estate in self.estate.values():
            estate.requestDelete()
            # This automatically gets called by the server
            # estate.delete()
        for hList in self.house.values():
            for house in hList:
                house.requestDelete()
                # This automatically gets called by the server
                # house.delete()
        del self.account2avId
        del self.avId2pendingEnter
        del self.refCount
        del self.estateZone
        del self.randomGenerator

    def getOwnerFromZone(self, zoneId):
        # returns doId of estate owner given a zoneId
        # zoneId can be estate exterior or house interior
        # returns None if zone not found
        estateZoneId = self.houseZone2estateZone.get(zoneId, zoneId)
        return self.zone2owner.get(estateZoneId)

    ## -----------------------------------------------------------
    ## Zone allocation and enter code
    ## -----------------------------------------------------------

    def getEstateZone(self, ownerId, name):
        self.notify.debug("getEstateZone: ownerId=%d, name = %s" % (ownerId, name))

        self.__enterEstate(self.air.getAvatarIdFromSender(), ownerId)

        # if the localToon is not going to his own estate,
        # we need to make sure that the estate has already
        # been created.  If not, we cannot create it, i.e
        # the localToon cannot go to his friends estate if
        # he is not there.

        goingHome = 0
        if ownerId != self.air.getAvatarIdFromSender():
            self.notify.debug("owner id isn't mesgSender %d, %d" % (ownerId, self.air.getAvatarIdFromSender()))
            # we are teleporting to someone in an estate
            avId = self.air.getAvatarIdFromSender()

            # check if they are in the same zone as us
            try:
                if self.estateZone[avId][0] == self.estateZone[ownerId][0]:
                    self.notify.debug("we are staying in the same zone %s, don't delete" % self.estateZone[avId])
                    zoneId = self.estateZone[avId][0]
                    self.__sendZoneToClient(avId, ownerId)
                    return
                else:
                    self.notify.debug("owner zone = %s, av zone = %s" % (self.estateZone[ownerId],self.estateZone[avId]))
            except:
                self.notify.debug("we aren't teleporting to the same estate")

            goingHome = 0
            if not self.estateZone.has_key(ownerId):
                # The person we are visiting is not in this shard
                # (or for some reason is not really in his estate)
                self.notify.warning("Can't go to friends house if he is not there")
                # SDN: tell the client and do something more graceful
                # make sure we don't give this guy toonups
                try:
                    # stop tooning up this visitor, he hasn't reached the estate yet
                    av = self.air.doId2do[self.air.getAvatarIdFromSender()]
                    av.stopToonUp()
                except:
                    self.notify.debug("couldn't stop toonUpTask for av %s" % self.air.getAvatarIdFromSender())
                self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), "setEstateZone", [0, 0])

                return
        else:
            self.notify.debug("we are teleporting to our own estate, %d, %d" % (self.air.getAvatarIdFromSender(), ownerId))
            avId = ownerId
            goingHome = 1

        # first check if we (the message sender) are in an estate already
        avZone = self.estateZone.get(avId)
        if avZone:
            #self.notify.debug('avZone exists, we\'re in an estate')
            # we are already in an estate
            if goingHome:
                #self.notify.debug('goingHome')
                # we are going to our own estate
                if avZone[1]:
                    self.notify.debug("we must have come in as a different avatar")
                    # stop the cleanup task if applicable
                    self.__stopCleanupTask(avId)

                    # but we are already in our own estate, just return the estate zone
                    self.__sendZoneToClient(avId, ownerId)
                else:
                    #self.notify.debug('leaving someone else\'s estate, going to ours')
                    # we are in someone else's estate.  remove references to ourselves
                    self.__exitEstate(avId)

                    # create the estate zone and objects
                    self.__createEstateZoneAndObjects(avId, goingHome, ownerId, name)
                    # this happens later, we don't know the zoneId yet
                    #self._listenForToonEnterEstate(avId, ownerId, zoneId)
            else:
                #self.notify.debug('leaving an estate, going to someone else\'s estate')
                # we are in an estate and going to someone else's estate
                # leave our current estate
                self.__exitEstate(avId)

                # send back to client
                # SDN: we may want to check if the ownerId actually owns
                # the estate here
                self.__sendZoneToClient(avId, ownerId)
                self.__addReferences(avId, ownerId)
                zoneId = self.estateZone[ownerId][0]
                self._listenForToonEnterEstate(avId, ownerId, zoneId)
        else:
            #self.notify.debug('avZone does not exist, we\'re not in an estate')
            # we aren't currently in an estate
            if goingHome:
                #self.notify.debug('going to our home')
                # we are going to our estate
                # create the estate zone and objects
                self.__createEstateZoneAndObjects(avId, goingHome, ownerId, name)
                # this happens later, we don't know the zoneId yet
                #self._listenForToonEnterEstate(avId, ownerId, zoneId)
            else:
                #self.notify.debug('going to someone else\'s estate')
                # we aren't in an estate, and are going to someone else's estate
                # SDN: we may want to check if the ownerId actually owns
                # the estate here
                self.__sendZoneToClient(avId, ownerId)
                self.__addReferences(avId, ownerId)
                zoneId = self.estateZone[ownerId][0]
                self._listenForToonEnterEstate(avId, ownerId, zoneId)

        # this doesn't work here; the estate may not yet be ready
        #self.announceToonEnterEstate(avId, ownerId)

    def getAvEnterEvent(self):
        return 'avatarEnterEstate'
    def getAvExitEvent(self, avId=None):
        # listen for all exits or a particular exit
        # event args:
        #  if avId given: none
        #  if avId not given: avId, ownerId, zoneId
        if avId is None:
            return 'avatarExitEstate'
        else:
            return 'avatarExitEstate-%s' % avId

    def __enterEstate(self, avId, ownerId):
        # Tasks that should always get called when entering an estate

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

        # Toonup
        try:
            av = self.air.doId2do[avId]
            av.startToonUp(self.healFrequency)
        except:
            self.notify.info("couldn't start toonUpTask for av %s" % avId)

    def _listenForToonEnterEstate(self, avId, ownerId, zoneId):
        #self.notify.debug('_listenForToonEnterEstate(avId=%s, ownerId=%s, zoneId=%s)' % (avId, ownerId, zoneId))
        if avId in self.avId2pendingEnter:
            self.notify.warning(
                '_listenForToonEnterEstate(avId=%s, ownerId=%s, zoneId=%s): '
                '%s already in avId2pendingEnter. overwriting' % (
                avId, ownerId, zoneId, avId))
        self.avId2pendingEnter[avId] = (ownerId, zoneId)
        self.accept(DistributedObjectAI.
                    DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId),
                    Functor(self._toonChangedZone, avId))

    def _toonLeftBeforeArrival(self, avId):
        #self.notify.debug('_toonLeftBeforeArrival(avId=%s)' % avId)
        if avId not in self.avId2pendingEnter:
            self.notify.warning('_toonLeftBeforeArrival: av %s not in table' %
                                avId)
            return
        ownerId, zoneId = self.avId2pendingEnter[avId]
        self.notify.warning(
            '_toonLeftBeforeArrival: av %s left server before arriving in '
            'estate (owner=%s, zone=%s)' % (avId, ownerId, zoneId))
        del self.avId2pendingEnter[avId]

    def _toonChangedZone(self, avId, newZoneId, oldZoneId):
        #self.notify.debug('_toonChangedZone(avId=%s, newZoneId=%s, oldZoneId=%s)' % (avId, newZoneId, oldZoneId))
        if avId not in self.avId2pendingEnter:
            self.notify.warning('_toonChangedZone: av %s not in table' %
                                avId)
            return
        av = self.air.doId2do.get(avId)
        if not av:
            self.notify.warning('_toonChangedZone(%s): av not present' % avId)
            return
        ownerId, estateZoneId = self.avId2pendingEnter[avId]
        estateZoneIds = self.getEstateZones(ownerId)
        if newZoneId in estateZoneIds:
            del self.avId2pendingEnter[avId]
            self.ignore(DistributedObjectAI.
                        DistributedObjectAI.staticGetLogicalZoneChangeEvent(avId))
            self.announceToonEnterEstate(avId, ownerId, estateZoneId)

    def announceToonEnterEstate(self, avId, ownerId, zoneId):
        """ announce to the rest of the system that a toon is entering
        an estate """
        EstateManagerAI.notify.debug('announceToonEnterEstate: %s %s %s' %
                                     (avId, ownerId, zoneId))
        messenger.send(self.getAvEnterEvent(), [avId, ownerId, zoneId])

    def announceToonExitEstate(self, avId, ownerId, zoneId):
        """ announce to the rest of the system that a toon is exiting
        an estate """
        EstateManagerAI.notify.debug('announceToonExitEstate: %s %s %s' %
                                     (avId, ownerId, zoneId))
        messenger.send(self.getAvExitEvent(avId))
        messenger.send(self.getAvExitEvent(), [avId, ownerId, zoneId])

    def getEstateZones(self, ownerId):
        # returns all zoneIds that belong to this estate
        zones = []
        estate = self.estate.get(ownerId)
        if estate is not None:
            if not hasattr(estate, 'zoneId'):
                self.notify.warning('getEstateZones: estate %s (owner %s) has no \'zoneId\'' %
                                    (estate.doId, ownerId))
            else:
                zones.append(estate.zoneId)
        houses = self.house.get(ownerId)
        if houses is not None:
            for house in houses:
                if not hasattr(house, 'interiorZoneId'):
                    self.notify.warning('getEstateZones: estate %s (owner %s) house has no interiorZoneId')
                else:
                    zones.append(house.interiorZoneId)
        return zones

    def getEstateHouseZones(self, ownerId):
        # returns all zoneIds that belong to houses on this estate
        zones = []
        houses = self.house.get(ownerId)
        if houses is not None:
            for house in houses:
                if not hasattr(house, 'interiorZoneId'):
                    self.notify.warning('getEstateHouseZones: (owner %s) house has no interiorZoneId')
                else:
                    zones.append(house.interiorZoneId)
        return zones

    def __sendZoneToClient(self, recipient, ownerId):
        try:
            zone = self.estateZone[ownerId][0]
            owner = self.zone2owner[zone]
            self.sendUpdateToAvatarId(recipient, "setEstateZone", [owner, zone])
        except:
            self.notify.warning("zone did not exist for estate owner %d, and visitor %d" % (ownerId, recipient))
            self.sendUpdateToAvatarId(recipient, "setEstateZone", [0, 0])


    def __createEstateZoneAndObjects(self, avId, isOwner, ownerId, name):
        # assume this is only called when isOwner == 1

        # stop any cleanup tasks that might be pending for this avId
        # (note: we might be in a case where we aren't in the toBeDeleted list
        # and still have a cleanup task pending.  this happens when we switch
        # shards)
        self.__stopCleanupTask(avId)

        # first check that we aren't in the toBeDeleted list
        avZone = self.toBeDeleted.get(avId)
        if avZone:

            # move our info back to estateZone
            self.setEstateZone(avId, avZone)
            del self.toBeDeleted[avId]
            return

        # check if our account has an estate created under a different avatar
        if self.__checkAccountSwitchedAvatars(name, avId):
            return

        # request the zone for the owners estate
        zoneId = self.air.allocateZone()
        self.setEstateZone(avId, [zoneId, isOwner, name]) # [zoneId, isOwner, userName (if owner)]
        self.account2avId[name] = avId
        self.zone2owner[zoneId] = avId

        # start a ref count for this zone id
        self.refCount[zoneId] = []

        # don't send a message back yet since the estate is not filled
        # in.  Do this later.
        #self.sendUpdateToAvatarId(avId, "setEstateZone", [avId, zoneId])

        # create the estate and generate the zone
        callback = PythonUtil.Functor(self.handleGetEstate, avId, ownerId)
        self.air.getEstate(avId, zoneId, callback)

    def __removeReferences(self, avId, zoneId):
        try:
            self.clearEstateZone(avId)
            self.refCount[zoneId].remove(avId)
        except:
            self.notify.debug("we weren't in the refcount for %s." % zoneId)
            pass

    def setEstateZone(self, index, info):
        self.estateZone[index] = info

        #print some debug info
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        #str = "%s(%s):Added %s:estateZone=%s" % (defName, lineno, index, self.estateZone)
        str = "%s(%s):Added %s:%s" % (defName, lineno, index, info)
        self.notify.debug(str)

    def clearEstateZone(self, index):
        assert self.estateZone.has_key(index)

        #print some debug info
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        defName = frame.f_code.co_name
        #str = "%s(%s):Removed %s:estateZone=%s" % (defName, lineno, index, self.estateZone)
        str = "%s(%s):Removed %s:%s" % (defName, lineno, index, self.estateZone[index])
        self.notify.debug(str)

        del self.estateZone[index]

    def __addReferences(self, avId, ownerId):
        avZone = self.estateZone.get(ownerId)
        if avZone:
            zoneId = avZone[0]
            self.setEstateZone(avId, [zoneId, 0, ""])  # [zoneId, isOwner, userName (if owner)]
            ref = self.refCount.get(zoneId)
            if ref:
                ref.append(avId)
            else:
                self.refCount[zoneId] = [avId]

    def __checkAccountSwitchedAvatars(self, name, ownerId):
        self.notify.debug("__checkAccountSwitchedAvatars")
        prevAvId = self.account2avId.get(name)
        if prevAvId:
            self.notify.debug("we indeed did switch avatars")
            # the estate exists, remap all references from prevAvId
            # to ownerId

            # first stop the cleanup task
            self.__stopCleanupTask(prevAvId)

            # now remap references
            self.account2avId[name] = ownerId

            #if self.estateZone.has_key(prevAvId):
            if self.toBeDeleted.has_key(prevAvId):
                self.setEstateZone(ownerId, self.toBeDeleted[prevAvId])
                del self.toBeDeleted[prevAvId]
            return 1
        return 0

    def handleGetEstate(self, avId, ownerId, estateId, estateVal,
                        numHouses, houseId, houseVal, petIds, valDict = None):
        self.notify.debug("handleGetEstate %s" % avId)
        # this function is called after the estate data is pulled
        # from the database.  the houseAI object is initialized
        # here, and if values don't exist for certain db fields
        # default values are given.

        # Note:  this is the place where randomized default values
        # should be assigned to the toons house.  For example:
        # door types, windows, colors, house selection, garden placement
        # etc.  The first time the toon visits his house, these
        # defaults will be computed and stored.

        # Note:  this function is only called by the owner of the estate

        # there is a chance that the owner will already have left (by
        # closing the window).  We need to handle that gracefully.

        if not self.estateZone.has_key(ownerId):
            self.notify.warning("Estate info was requested, but the owner left before it could be recived: %d" % estateId)
            return
        elif not avId in self.air.doId2do:
            self.notify.warning("Estate owner %s in self.estateZone, but not in doId2do" % avId)
            return

        # create the DistributedEstateAI object for this avId
        if self.estateZone.has_key(avId):
            if self.air.doId2do.has_key(estateId):
                self.notify.warning("Already have distobj %s, not generating again" % (estateId))
            else:
                self.notify.info('start estate %s init, owner=%s, frame=%s' %
                                 (estateId, ownerId, globalClock.getFrameCount()))

                # give the estate a time seed
                estateZoneId = self.estateZone[avId][0]
                ts = time.time() % HouseGlobals.DAY_NIGHT_PERIOD
                self.randomGenerator.seed(estateId)
                dawn = HouseGlobals.DAY_NIGHT_PERIOD * self.randomGenerator.random()
                estateAI = DistributedEstateAI.DistributedEstateAI(self.air, avId,
                                                                   estateZoneId, ts, dawn, valDict)
                # MPG - We should make sure this works across districts
                estateAI.dbObject = 1
                estateAI.generateWithRequiredAndId(estateId,
                                                   self.air.districtId,
                                                   estateZoneId)



                estateAI.initEstateData(estateVal, numHouses, houseId, houseVal)
                estateAI.setPetIds(petIds)
                self.estate[avId] = estateAI

                # create the DistributedHouseAI's.  This was originally done by the EstateAI
                # but we need to move it here so we can explicitly control when the
                # DistributedHouse objects get deleted from the stateserver.
                self.house[avId] = [None] * numHouses
                for i in range(numHouses):
                    if self.air.doId2do.has_key(houseId[i]):
                        self.notify.warning("doId of house %s conflicts with a %s!" % (houseId[i], self.air.doId2do[houseId[i]].__class__.__name__))

                    else:
                        house = DistributedHouseAI.DistributedHouseAI(self.air,
                                                                      houseId[i],
                                                                      estateId, estateZoneId, i)

                        # get house information
                        house.initFromServerResponse(houseVal[i])
                        self.house[avId][i] = house

                        # Now that we have all the data loaded, officially
                        # generate the distributed object

                        house.dbObject = 1

                        # MPG - We should make sure this works across districts
                        house.generateWithRequiredAndId(houseId[i],
                                                        self.air.districtId,
                                                        estateZoneId)

                        house.setupEnvirons()

                        # Finally, make sure that the house has a good owner,
                        # and then tell the client the house is ready.
                        house.checkOwner()

                        estateAI.houseList.append(house)

                estateAI.postHouseInit()

                #get us a list of the owners of the houses
                avIdList = []
                for id in houseId:
                    avHouse = simbase.air.doId2do.get(id)
                    avIdList.append(avHouse.ownerId)

                if simbase.wantPets:
                    self.notify.debug('creating pet collisions for estate %s' %
                                     estateId)
                    estateAI.createPetCollisions()

                # create a pond bingo manager ai for the new estate
                if simbase.wantBingo:
                    self.notify.info('creating bingo mgr for estate %s' %
                                     estateId)
                    self.air.createPondBingoMgrAI(estateAI)

                self.notify.info('finish estate %s init, owner=%s' %
                                 (estateId, ownerId))

                estateAI.gardenInit(avIdList)

        # Now that the zone is set up, send the notification back to
        # the client.
        self.__sendZoneToClient(avId, ownerId)
        zoneId = self.estateZone[ownerId][0]
        self._listenForToonEnterEstate(avId, ownerId, zoneId)

    ## -----------------------------------------------------------
    ## Cleanup and exit functions
    ## -----------------------------------------------------------

    def exitEstate(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("exitEstate(%s)" % avId)
        # This function is called from client in the normal case,
        # such as teleporting out, door out, exiting the game, etc
        self.__exitEstate(avId)

    def __handleUnexpectedExit(self, avId):
        self.notify.debug("we got an unexpected exit on av: %s:  deleting." % avId)
        taskMgr.remove("estateToonUp-" + str(avId))
        if avId in self.avId2pendingEnter:
            self._toonLeftBeforeArrival(avId)
        self.__exitEstate(avId)
        return None

    def __exitEstate(self, avId):
        self.notify.debug("__exitEstate(%d)" % avId)
        # This is called whenever avId leaves an estate.
        # Determine if avId is the owner.  If so, set
        # a timer to cleanup all of the estate resources
        # and to kick all visitors out.  If we aren't the
        # owner, just remove references of avId from the estate
        avZone = self.estateZone.get(avId)
        if avZone:
            zoneId = avZone[0]
            ownerId = self.zone2owner[zoneId]
            self.announceToonExitEstate(avId, ownerId, zoneId)
            if avZone[1]:
                self.notify.debug("__exitEstate: av %d owns estate" % avId)
                # avId owns the estate
                ownerId = avId

                # warn visitors they have n seconds to finish what they were doing
                self.__warnVisitors(avZone[0])

                # start timers to kick people out and cleanup our resources
                if self.air:
                    self.ignore(self.air.getAvatarExitEvent(avId))
                taskMgr.doMethodLater(HouseGlobals.BOOT_GRACE_PERIOD,
                                      PythonUtil.Functor(self.__bootVisitorsAndCleanup, avId, avZone[0]),
                                      "bootVisitorsAndCleanup-"+str(avId))

                # remove avId references from estateZone
                self.clearEstateZone(avId)
                self.toBeDeleted[avId] = avZone
            else:
                self.notify.debug("__exitEstate: av %d doesn't own estate" % avId)
                # avId doesn't own this estate, just remove references to avId
                # from the data structures
                if self.estateZone.has_key(avId):
                    self.clearEstateZone(avId)
                try:
                    self.refCount[avZone[0]].remove(avId)
                except:
                    self.notify.debug("wasn't in refcount: %s, %s" % (avZone[0], avId))
        else:
            self.notify.debug("__exitEstate can't find zone for %d" % avId)

        # stop the healing
        if self.air.doId2do.has_key(avId):
            # Find the avatar
            av = self.air.doId2do[avId]
            # Stop healing them
            av.stopToonUp()

    def __cleanupEstate(self, avId, zoneId, task):
        self.notify.debug("cleanupEstate avId = %s, zoneId = %s" % (avId, zoneId))
        # we should always be cleaning up things from the toBeDeleted list,
        # not directly from estateZone

        # remove all 'hanging' entries left in estateZone
        # this is caused by:
        #   friend A is visting friend B
        #   friend B exits his estate
        #   friend C attempts to visit friend A at the same time
        for someAvId, avZone in self.estateZone.items():
            if avZone[0] == zoneId:
                # This may be a slow client that just hasn't reported back.
                # If the toon is still in the zone, announce that they've
                # left before cleaning up the tables. When they report in that
                # they've left (client->AI: exitEstate), the code will not
                # find the avatar in the tables and will ignore.
                avatar = simbase.air.doId2do.get(someAvId)
                if ((avatar) and
                    (hasattr(avatar, "estateZones")) and
                    (zoneId in avatar.estateZones) and
                    (avatar.zoneId in avatar.estateZones)):
                    ownerId = self.zone2owner[zoneId]
                    self.notify.warning(
                        "forcing announcement of toon %s exit from %s %s" %
                        (someAvId, ownerId, zoneId))
                    self.announceToonExitEstate(someAvId, ownerId, zoneId)

                self.notify.warning(
                    "Manually removing (bad) entry in estateZone: %s" %
                    someAvId)
                self.clearEstateZone(someAvId)

        # give our zoneId back to the air
        self.air.deallocateZone(zoneId)
        avZone = self.toBeDeleted.get(avId)
        if avZone:
            if avZone[2] != "":
                if self.account2avId.has_key(avZone[2]):
                    self.notify.debug( "removing %s from account2avId" % avZone[2])
                    del self.account2avId[avZone[2]]
            del self.toBeDeleted[avId]
            del self.zone2owner[avZone[0]]

        # delete estate and houses from state server
        self.__deleteEstate(avId)

        # stop listening for unexpectedExit
        self.ignore(self.air.getAvatarExitEvent(avId))

        # refcount should be empty, just delete
        if self.refCount.has_key(zoneId):
            del self.refCount[zoneId]

        return Task.done

    def __stopCleanupTask(self, avId):
        self.notify.debug("stopCleanupTask %s" % avId)
        taskMgr.remove("cleanupEstate-"+str(avId))
        taskMgr.remove("bootVisitorsAndCleanup-"+str(avId))
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])


    def __deleteEstate(self, avId):
        # remove all our objects from the stateserver
        self.notify.debug("__deleteEstate(avId=%s)" % avId)

        # delete from state server
        if self.estate.has_key(avId):
            if self.estate[avId] != None:
                self.estate[avId].destroyEstateData()
                self.notify.debug('DistEstate requestDelete, doId=%s' %
                                  getattr(self.estate[avId], 'doId'))
                self.estate[avId].requestDelete()
                # This automatically gets called by the server
                # self.estate[avId].delete()
                del self.estate[avId]
        # delete the houses
        houses = self.house.get(avId)
        if houses:
            for i in range(len(houses)):
                if self.house[avId][i]:
                    self.house[avId][i].requestDelete()
                    # This automatically gets called by the server
                    # self.house[avId][i].delete()
            del self.house[avId]

    """
    def __bootVisitors(self, zoneId, task):
        try:
            visitors = self.refCount[zoneId][:]
            for avId in visitors:
                self.__bootAv(avId, zoneId)
        except:
            # refCount might have already gotten deleted
            pass
        return Task.done
    """

    def __bootVisitorsAndCleanup(self, ownerId, zoneId, task):
        try:
            visitors = self.refCount[zoneId][:]
            for avId in visitors:
                self.__bootAv(avId, zoneId, ownerId)
        except:
            # refCount might have already gotten deleted
            pass
        taskMgr.doMethodLater(HouseGlobals.CLEANUP_DELAY_AFTER_BOOT,
                              PythonUtil.Functor(self.__cleanupEstate, ownerId, zoneId),
                              "cleanupEstate-"+str(ownerId))
        return Task.done

    def __bootAv(self, avId, zoneId, ownerId, retCode=1):
        messenger.send("bootAvFromEstate-"+str(avId))
        self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, retCode])
        if self.toBeDeleted.has_key(avId):
            del self.toBeDeleted[avId]
        try:
            self.refCount[zoneId].remove(avId)
        except:
            self.notify.debug("didn't have refCount[%s][%s]" % (zoneId,avId))
            pass

    def __warnVisitors(self, zoneId):
        visitors = self.refCount.get(zoneId)
        if visitors:
            for avId in visitors:
                self.sendUpdateToAvatarId(avId, "sendAvToPlayground", [avId, 0])

    def removeFriend(self, ownerId, avId):
        self.notify.debug("removeFriend ownerId = %s, avId = %s" % (ownerId, avId))
        # check if ownerId is in an estate
        ownZone = self.estateZone.get(ownerId)
        if ownZone:
            if ownZone[1]:
                # owner is in his own estate.  kick out avId if he is
                # in the owner's estate.
                avZone = self.estateZone.get(avId)
                if avZone:
                    if avZone[0] == ownZone[0]:
                        # avId is indeed in owner's estate.  boot him
                        self.__bootAv(avId, ownZone[0], ownerId, retCode=2)
                    else:
                        print "visitor not in owners estate"
                else:
                    print "av is not in an estate"

        else:
            print "owner not in estate"

    ## -----------------------------------------------------------
    ## April fools stuff
    ## -----------------------------------------------------------

    def startAprilFools(self):
        self.sendUpdate("startAprilFools",[])

    def stopAprilFools(self):
        self.sendUpdate("stopAprilFools",[])

