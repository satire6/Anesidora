from direct.showbase import DirectObject
from toontown.toonbase import ToontownGlobals
from toontown.ai import DatabaseObject
from toontown.ai import ToontownAIMsgTypes
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.showbase.PythonUtil import Functor
from toontown.pets import PetUtil
from toontown.pets import PetNameGenerator

class PetManagerAI(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("PetManagerAI")
    #notify.setDebug(1)
    
    def __init__(self, air):
        self.air = air
        self.serialNum = 0

        # this table holds petId->zoneId of pets that have already requested
        # deletion, but are not yet deleted, that need to show up in a
        # particular zone
        self._petsToGenerateAfterDeletion = {}

        # this table holds toonAvId->(estateOwnerId, estateZoneId) for
        # toons that we have been told are in an estate but have not yet
        # changed zones to the estate
        self._toonsPendingEstateArrival = {}
        # table of avId to list of event names that are being used to
        # listen for whether or not the toon made it to the estate.
        self._pendingToonEvents = {}

        # listen for Toons entering estates
        self.accept(self.air.estateMgr.getAvEnterEvent(),
                    self.handleToonEnterEstate)
        self.accept(self.air.estateMgr.getAvExitEvent(),
                    self.handleToonExitEstate)

    def destroy(self):
        self.__stopGenerateAfterDelete()
        del self._petsToGenerateAfterDeletion
        del self._toonsPendingEstateArrival
        del self._pendingToonEvents
        self.ignoreAll()

    def handleToonEnterEstate(self, avId, ownerId, zoneId):
        assert(PetManagerAI.notify.debug('toon going to estate: %s %s %s' % (
            avId, ownerId, zoneId)))
        toon = simbase.air.doId2do[avId]
        # is the toon already in the estate zone?       
        if toon.zoneId == zoneId:
            self._onToonArriveInEstate(avId, ownerId, zoneId)
        else:
            self.accept(toon.getLogicalZoneChangeEvent(),
                        Functor(self._toonChangedZone, avId))
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            Functor(self._toonDidntMakeItToEstate, avId))

            self._toonsPendingEstateArrival[avId] = (ownerId, zoneId)
            self._pendingToonEvents[avId] = [
                toon.getLogicalZoneChangeEvent(),
                self.air.getAvatarExitEvent(avId),
                ]

    def _cancelToonZoneChangeListen(self, avId):
        # stop listening/waiting for the toon to go to an estate
        PetManagerAI.notify.debug('_cancelToonZoneChangeListen: %s' % avId)
        assert avId in self._toonsPendingEstateArrival
        assert avId in self._pendingToonEvents
        for event in self._pendingToonEvents[avId]:
            self.ignore(event)
        del self._toonsPendingEstateArrival[avId]
        del self._pendingToonEvents[avId]

    def _toonDidntMakeItToEstate(self, avId):
        # we were waiting for this toon to change zones to a particular
        # estate, but he went away before it could happen
        assert avId in self._toonsPendingEstateArrival, (
            '_toonDidntMakeItToEstate: %s not in pending list' % avId)
        self._cancelToonZoneChangeListen(avId)

    def _toonChangedZone(self, avId, newZoneId, oldZoneId):
        # we're waiting for this toon to enter an estate; he has changed
        # zones. Check if it's the estate
        assert avId in self._toonsPendingEstateArrival, (
            '_toonChangedZone: avId %s not in self._toonsPendingEstateArrival'
            % avId)
        ownerId, zoneId = self._toonsPendingEstateArrival[avId]
        if newZoneId == zoneId:
            self._cancelToonZoneChangeListen(avId)
            self._onToonArriveInEstate(avId, ownerId, zoneId)
        else:
            PetManagerAI.notify.info('toon changed zones to %s, waiting for '
                                     'estate zone %s' % (newZoneId, zoneId))

    def _onToonArriveInEstate(self, avId, ownerId, zoneId):
        assert(PetManagerAI.notify.debug('toon arrived in estate: %s %s %s' % (
            avId, ownerId, zoneId)))
        # put the toon into estate mode (for now this is only necessary
        # when pets are around)
        toon = simbase.air.doId2do.get(avId)
        if toon is None:
            PetManagerAI.notify.warning(
                'got toonEnterEstate event but Toon %s does not exist' % avId)
            return
        toon.enterEstate(ownerId, zoneId)

        # summon the pets
        # is this toon the estate owner?
        if avId == ownerId:
            # summon every pet that lives in the estate
            estate = simbase.air.estateMgr.estate.get(ownerId)
            if estate is None:
                PetManagerAI.notify.warning(
                    'got toonEnterEstate but %s\'s estate does not exist' %
                    ownerId)
                return
            petIds = estate.petIds
        else:
            # just call up this Toon's pet
            petIds = [toon.getPetId()]

        for petId in petIds:
            if petId != 0:
                if petId not in simbase.air.doId2do:
                    self.generatePetInZone(petId, zoneId)
                else:
                    # pet is already generated; there's a good chance that
                    # the pet has already requested to be deleted, but is
                    # still around pending a reply
                    self.movePetToZone(petId, zoneId)

    def handleToonExitEstate(self, avId, ownerId, zoneId):
        assert(PetManagerAI.notify.debug('handleToonExitEstate: %s %s %s' % (
            avId, ownerId, zoneId)))
        if avId in self._toonsPendingEstateArrival:
            pendOwnerId, pendZoneId = self._toonsPendingEstateArrival[avId]
            if pendOwnerId != ownerId:
                PetManagerAI.notify.debug(
                    "toon pending arrival in %s's estate, not %s's" % (
                    pendOwnerId, ownerId))
            elif pendZoneId != zoneId:
                # zone mismatch??
                PetManagerAI.notify.warning(
                    "toon %s going to %s's estate, but in zone %s" % (
                    pendOwnerId, ownerId, pendZoneId))
            else:
                PetManagerAI.notify.debug('cancelling pending toon arrival in '
                                          'estate zone %s' % zoneId)
                self._cancelToonZoneChangeListen(avId)
        else:
            # take the toon out of estate mode (for now this is only necessary
            # when pets are around)
            toon = simbase.air.doId2do.get(avId)
            if toon is None:
                PetManagerAI.notify.debug("av %s not in doId2do" % avId)
            elif toon.isInEstate():
                PetManagerAI.notify.debug("PetManagerAI - Exit Estate toonId:%s ownerId:%s" %(avId, ownerId))
                toon.exitEstate(ownerId, zoneId)
            else:
                PetManagerAI.notify.warning(
                    'toon %s already out of estate mode' % avId)

    def _getNextSerialNum(self):
        num = self.serialNum
        self.serialNum += 1
        return num

    def generatePetInZone(self, petId, zoneId):
        def handleGetPet(success, pet, petId=petId, zoneId=zoneId):
            if success:
                def doGenPet(pet, petId, zoneId):
                    # create pet in the quiet zone so that it gets a
                    # zone change msg when entering its destination
                    pet.dbObject = 1
                    pet.generateWithRequiredAndId(petId, self.air.districtId, zoneId)
                    simbase.air.setAIReceiver(petId)
                if petId not in simbase.air.doId2do:
                    simbase.air.requestDeleteDoId(petId)
                    doGenPet(pet, petId, zoneId)
                else:
                    self.notify.warning(
                        'handleGetPet(%s): %s is already in doId2do' % (
                        petId, simbase.air.doId2do[petId].__class__.__name__))
                    petDO = simbase.air.doId2do[petId]
                    petDO.requestDelete()
                    self.acceptOnce(simbase.air.getDeleteDoIdEvent(petId),
                                    Functor(doGenPet, pet, petId, zoneId))
            else:
                PetManagerAI.notify.warning(
                    'error generating pet %s' % (petId))
        self.getPetObject(petId, handleGetPet)

    def movePetToZone(self, petId, zoneId):
        """call this function to make a pet show up in a particular zone.
        This correctly handles the following situations:
        - the pet is not instantiated
        - the pet is instantiated
        - the pet has requested deletion and is awaiting a delete
        """
        def doGenPetInZone(self, petId, zoneId):
            self.generatePetInZone(petId, zoneId)            
        if petId not in simbase.air.doId2do:
            simbase.air.requestDeleteDoId(petId)
            doGenPetInZone(self, petId, zoneId)
        else:
            self.notify.warning(
                'movePetToZone(%s): %s is already in doId2do' % (
                petId, simbase.air.doId2do[petId].__class__.__name__))
            petDO = simbase.air.doId2do[petId]
            if hasattr(petDO,'hasRequestedDelete') and petDO.hasRequestedDelete():
                self.notify.info('movePetToZone NOT calling requestDelete again')
            else:
                if not hasattr(petDO, 'hasRequestedDelete'):
                    self.notify.warning('petDO=%s petId=%s does not have hasRequestedDelete' % (petDO,petId))
                petDO.requestDelete()
            self.acceptOnce(simbase.air.getDeleteDoIdEvent(petId),
                            Functor(doGenPetInZone, self, petId, zoneId))

        # old
        #if petId not in simbase.air.doId2do:
        #    self.generatePetInZone(petId, zoneId)
        #    return
        #pet = simbase.air.doId2do[petId]
        #if not pet.hasRequestedDelete():
        #    pet.requestDelete()
        #self._addPetToGenerateAfterDeletion(petId, zoneId)

    def _addPetToGenerateAfterDeletion(self, petId, zoneId):
        # call this to cause this pet to be re-generated once it has been
        # deleted (use this if we need to move a pet to a different zone,
        # but it has just requested to be deleted)
        if len(self._petsToGenerateAfterDeletion) == 0:
            self.__startGenerateAfterDelete()
        self._petsToGenerateAfterDeletion[petId] = zoneId

    def __getGenAfterDelTask(self):
        return 'PetManagerAI-doGenerateAfterDelete'
    def __startGenerateAfterDelete(self):
        # kick off a task to generate pets once they've been deleted
        taskMgr.add(self.__doGenerateAfterDelete, self.__getGenAfterDelTask())
    def __stopGenerateAfterDelete(self):
        taskMgr.remove(self.__getGenAfterDelTask())
    def __doGenerateAfterDelete(self, task):
        # if a pet has been deleted, generate it in the new zone
        assert len(self._petsToGenerateAfterDeletion) > 0
        petIds = self._petsToGenerateAfterDeletion.keys()
        for petId in petIds:
            if petId not in simbase.air.doId2do:
                zoneId = self._petsToGenerateAfterDeletion[petId]
                del self._petsToGenerateAfterDeletion[petId]
                self.generatePetInZone(petId, zoneId)

        if len(self._petsToGenerateAfterDeletion) == 0:
            return Task.done
        return Task.cont

    def getPetObject(self, petId, callback):
        """get an instance of a pet
        callback must accept (success, pet)
        pet is undefined if !success

        On success, pet MUST be instantiated with
        DistributedObjectAI.generateWithRequiredAndId, using the
        correct pet doId.
        """
        doneEvent = 'readPet-%s' % self._getNextSerialNum()
        dbo = DatabaseObject.DatabaseObject(
            self.air, petId, doneEvent=doneEvent)
        pet = dbo.readPet()

        def handlePetRead(dbo, retCode, callback=callback, pet=pet):
            success = (retCode == 0)
            if not success:
                PetManagerAI.notify.warning('pet DB read failed')
                pet = None
            callback(success, pet)
        self.acceptOnce(doneEvent, handlePetRead)

    def createNewPetObject(self, callback):
        """ creates a new pet object in the DB """
        # callback must accept (success, petId)
        # petId is undefined if !success
        doneEvent = 'createPetObject-%s' % self._getNextSerialNum()
        dbo = DatabaseObject.DatabaseObject(self.air, doneEvent=doneEvent)

        def handleCreateNewPet(dbo, retCode, callback=callback):
            success = (retCode == 0)
            if success:
                petId = dbo.doId
            else:
                PetManagerAI.notify.warning('pet creation failed')
                petId = None
            callback(success, petId)

        self.acceptOnce(doneEvent, handleCreateNewPet)
        dbo.createObject(ToontownAIMsgTypes.DBSERVER_PET_OBJECT_TYPE)

    def deletePetObject(self, petId):
        """ USE WITH CAUTION, this could delete any DB record (such as
        Toons or Houses) """
        assert petId != 0
        PetManagerAI.notify.warning('deleting pet %s' % petId)
        self.air.writeServerEvent('deletePetObject', petId, '')
        dbo = DatabaseObject.DatabaseObject(self.air, petId)
        dbo.deleteObject()

    def assignPetToToon(self, petId, toonId):
        # toon must be logged in
        # we could deal directly with the database for toons that are not
        # logged in, but we don't need that for the pet system
        toon = self.air.doId2do.get(toonId)
        if toon is None:
            return 0
        # we must have already discarded our last pet
        if toon.getPetId() != 0:
            oldPetId = toon.getPetId()
            PetManagerAI.notify.warning(
                'assignPetToToon: assigning pet %s to toon who already '
                'has pet %s!' % (petId, oldPetId))
            self.air.writeServerEvent('errorOverwriteExistingPet', toonId,
                                      '%s|%s' % (oldPetId, petId))
        else:
            self.air.writeServerEvent('assignPet', toonId, '%s' % petId)
            toon.b_setPetId(petId)

    def createNewPetFromSeed(self, toonId, seed, gender = -1, nameIndex = -1, safeZoneId = ToontownGlobals.ToontownCentral):
        def handleCreate(success, petId):
            def summonPet(petId, callback):
                def handleGetPet(success, pet, petId=petId):
                    if success:
                        # we don't want our pet to start examining his
                        # environment, etc., we just want to initialize his
                        # DB fields
                        pet.setInactive()
                        pet._beingCreatedInDB = True
                        pet.dbObject = 1
                        pet.generateWithRequiredAndId(petId, 
                                                  self.air.districtId,
                                                  ToontownGlobals.QuietZone)
                        simbase.air.setAIReceiver(petId)
                    callback(success, pet)
                simbase.air.petMgr.getPetObject(petId, handleGetPet)

            if success:
                def handlePetGenerated(success, pet):
                    if success:
                        name, dna, traitSeed = PetUtil.getPetInfoFromSeed(seed, safeZoneId)
                        if gender != -1:
                            #make sure the size of the dna array hasn't changed
                            assert(len(dna) == 9)
                            dna[8] = gender
                        if nameIndex != -1:
                            name = PetNameGenerator.PetNameGenerator().getName(nameIndex)
                        pet._initDBVals(toonId, name, traitSeed, dna,
                                        safeZoneId)
                        self.assignPetToToon(petId, toonId)
                        message = '%s|%s|%s|%s|%s' % (
                            petId, name, pet.getSafeZone(), dna,
                            pet.traits.getValueList())
                        self.air.writeServerEvent('adoptPet', toonId, message)
                        pet.requestDelete()
                    else:
                        PetManagerAI.notify.warning('error summoning pet %s' % petId)
                # since this is the first time the pet is being
                # created, and we're going to be setting properties
                # on the pet, generate it in the Quiet zone first,
                # then move it to the requested zone.
                summonPet(petId, callback=handlePetGenerated)
            else:
                PetManagerAI.notify.warning('error creating pet for %s' % toonId)
        self.createNewPetObject(handleCreate)
    
    def deleteToonsPet(self, toonId):
        """ delete the toon's current pet. Pet objects (like all DB objects)
        are written to a separate XML file upon deletion. """
        # toon must be logged in
        toon = self.air.doId2do.get(toonId)
        if toon is None:
            PetManagerAI.notify.warning('deleteToonsPet: %s not logged in!' %
                                        toonId)
            return 1
        curPetId = toon.getPetId()
        # we have to have a pet to delete a pet
        if curPetId == 0:
            PetManagerAI.notify.warning('deleteToonsPet: %s has no pet!' %
                                        toonId)
            return 2

        pet = simbase.air.doId2do.get(curPetId)
        if pet is not None:
            PetManagerAI.notify.warning('deleteToonsPet: %s has tried to delete a pet that is in memory: %s' %
                                        (toonId, curPetId))
            pet.requestDelete()

        self.air.writeServerEvent('deleteToonsPet', toonId, '%s' % curPetId)
        toon.b_setPetId(0)
        self.deletePetObject(curPetId)
        return 0

    def getAvailablePets(self, numDaysPetAvailable, numPetsPerDay):
        """
        This should get called when we first enter the PetChooser.
        It creates the list of toons that are available here.
        """

        import random, time
        S = random.getstate()

        curDay = int( time.time() / 60.0 / 60.0 / 24.0 )
        seedMax = 2**30    #or something like that
        seeds = []

        #get a seed for each day
        for i in range(numDaysPetAvailable):
            random.seed(curDay + i)
            #get a seed for each pet
            for j in range(numPetsPerDay):
                seeds.append( random.randrange(seedMax) )

        return seeds
                
        random.setstate(S)
        
