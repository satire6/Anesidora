"""DistributedPetAI module: contains the DistributedPetAI class"""

from pandac.PandaModules import *
from direct.showbase.PythonUtil import weightedChoice, randFloat, lerp
from direct.showbase.PythonUtil import contains, list2dict, clampScalar
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNodeAI
from direct.distributed import DistributedSmoothNodeBase
from direct.distributed import ClockDelta
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
from direct.task import Task
from otp.movement import Mover
from toontown.pets import PetChase, PetFlee, PetWander, PetLeash
from toontown.pets import PetCollider, PetSphere, PetLookerAI
from toontown.pets import PetConstants, PetDNA, PetTraits
from toontown.pets import PetObserve, PetBrain, PetMood
from toontown.pets import PetActionFSM, PetBase, PetGoal, PetTricks
from direct.fsm import FSM
from toontown.toon import DistributedToonAI
from toontown.ai import ServerEventBuffer
import random
import time
import string
import copy
from direct.showbase.PythonUtil import StackTrace


class DistributedPetAI(DistributedSmoothNodeAI.DistributedSmoothNodeAI,
                       PetLookerAI.PetLookerAI, PetBase.PetBase):
    """AI-side implementation of Toon pet"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPetAI")
    #notify.setDebug(True)

    # Dictionaries used for switch-like statements to reduce if-else logic
    movieTimeSwitch = { PetConstants.PET_MOVIE_FEED: PetConstants.FEED_TIME,
                        PetConstants.PET_MOVIE_SCRATCH: PetConstants.SCRATCH_TIME,
                        PetConstants.PET_MOVIE_CALL: PetConstants.CALL_TIME }

    movieDistSwitch = { PetConstants.PET_MOVIE_FEED: PetConstants.FEED_DIST.get,
                        PetConstants.PET_MOVIE_SCRATCH: PetConstants.SCRATCH_DIST.get }
    
    def __init__(self, air, dna = None):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)
        PetLookerAI.PetLookerAI.__init__(self)
        self.ownerId = 0
        self.petName = 'unnamed'
        self.traitSeed = 0
        self.safeZone = ToontownGlobals.ToontownCentral
        self.initialDNA = dna

        # if this flag is false by the time we're generated, we won't try
        # to start the pet up normally; useful for creating the pet just
        # so we can set its DB values
        self.active = 1
        self.activated = 0
        # if the pet wanders off too far, we delete him, and stop broadcasting
        # position updates
        self._outOfBounds = False

        self.traitList = [0] * PetTraits.PetTraits.NumTraits

        self.head = -1
        self.ears = -1
        self.nose = -1
        self.tail = -1
        self.bodyTexture = 0
        self.color = 0
        self.colorScale = 0
        self.eyeColor = 0
        self.gender = 0
        self.movieMode = None
        self.lockMoverEnabled = 0

        self.trickAptitudes = []

        self.inEstate = 0
        self.estateOwnerId = None
        self.estateZones = []

        self.lastSeenTimestamp = self.getCurEpochTimestamp()

        # cache required mood components until we have a self.mood to give
        # them to
        self.requiredMoodComponents = {}
        
        # create our distributed trait and mood funcs
        # Keep track of all the funcs that we stuff into our dict
        self.__funcsToDelete = []
        self.__generateDistTraitFuncs()
        self.__generateDistMoodFuncs()

        self.busy = 0

        # to set walking speed, etc.
        self.gaitFSM = ClassicFSM.ClassicFSM(
            'petGaitFSM',
            [State.State('off', self.gaitEnterOff, self.gaitExitOff),
             State.State('neutral', self.gaitEnterNeutral, self.gaitExitNeutral),
             State.State('happy', self.gaitEnterHappy, self.gaitExitHappy),
             State.State('sad', self.gaitEnterSad, self.gaitExitSad),
             ],
            # init
            'off',
            # final
            'off',
            )
        self.gaitFSM.enterInitialState()

        # enters mode where pet detects that he's stuck on a collision and
        # decides to do something different
        self.unstickFSM = ClassicFSM.ClassicFSM(
            'unstickFSM',
            [State.State('off', self.unstickEnterOff, self.unstickExitOff),
             State.State('on', self.unstickEnterOn, self.unstickExitOn),
             ],
            # init
            'off',
            # final
            'off',
            )
        self.unstickFSM.enterInitialState()

        if __dev__:
            self.pscMoveResc = PStatCollector('App:Show code:petMove:Reschedule')

    # call this before generating the pet if you do not want the pet to
    # be active, i.e. if you just want to set some DB vals on the pet
    def setInactive(self):
        self.active = 0

    if __debug__:
        # these are debug functions to prepare new pets
        def _initFakePet(self, ownerId, name, traitSeed=0,
                         safeZone=ToontownGlobals.ToontownCentral):
            # Initializes a 'fake' pet (not represented in the database).
            # Call before generate.
            self.setOwnerId(ownerId)
            self.setPetName(name)
            self.traits = PetTraits.PetTraits(traitSeed=traitSeed,
                                              safeZoneId=safeZone)

        def _setMedianTraits(self, szId):
            # call this on an existing pet to set all his traits to median
            # values for a particular safe zone. For gameplay balancing.
            for i in xrange(PetTraits.PetTraits.NumTraits):
                traitName = PetTraits.getTraitNames()[i]
                traitDesc = PetTraits.PetTraits.TraitDescs[i]
                distrib = traitDesc[1]
                min, max = distrib.getMinMax(szId)
                setterName = self.getSetterName(traitName, 'b_set')
                self.__dict__[setterName]((min + max) / 2.)
                
        def _setLowTraits(self, szId):
            # call this on an existing pet to set all his traits to the
            # lowest values for a particular safe zone. For gameplay balancing.
            for i in xrange(PetTraits.PetTraits.NumTraits):
                traitName = PetTraits.getTraitNames()[i]
                traitDesc = PetTraits.PetTraits.TraitDescs[i]
                distrib = traitDesc[1]
                min, max = distrib.getMinMax(szId)
                setterName = self.getSetterName(traitName, 'b_set')
                self.__dict__[setterName](min)
                
        def _setHighTraits(self, szId):
            # call this on an existing pet to set all his traits to the
            # highest values for a particular safe zone. For gameplay
            # balancing.
            for i in xrange(PetTraits.PetTraits.NumTraits):
                traitName = PetTraits.getTraitNames()[i]
                traitDesc = PetTraits.PetTraits.TraitDescs[i]
                distrib = traitDesc[1]
                min, max = distrib.getMinMax(szId)
                setterName = self.getSetterName(traitName, 'b_set')
                self.__dict__[setterName](max)
                
        def _setTypicalTraits(self, szId):
            # call this on an existing pet to set all his traits to typical
            # random values for a particular safezone. For gameplay balancing.
            for i in xrange(PetTraits.PetTraits.NumTraits):
                traitName = PetTraits.getTraitNames()[i]
                traitDesc = PetTraits.PetTraits.TraitDescs[i]
                distrib = traitDesc[1]
                value = distrib.getRandValue(szId)
                setterName = self.getSetterName(traitName, 'b_set')
                self.__dict__[setterName](value)
            
    def _initDBVals(self, ownerId, name=None, traitSeed=0, dna=None,
                    safeZone=ToontownGlobals.ToontownCentral):
        # Initializes the DB fields for a new, generated pet object to
        # valid/safe values.
        self.b_setOwnerId(ownerId)
        if name is None:
            name = 'pet%s' % self.doId
        self.b_setPetName(name)
        self.b_setTraitSeed(traitSeed)
        self.b_setSafeZone(safeZone)

        traits = PetTraits.PetTraits(traitSeed, safeZone)
        for traitName in PetTraits.getTraitNames():
            setter = self.getSetterName(traitName, 'b_set')
            self.__dict__[setter](traits.getTraitValue(traitName))
        self.traits = traits

        # initialize the mood components to zero
        for component in PetMood.PetMood.Components:
            setterName = self.getSetterName(component, 'b_set')
            self.__dict__[setterName](0.)

        # if this assert fails, we need to update this function's handling
        # of the DNA since it has grown or shrunk
        assert PetDNA.NumFields == 9, 'Pet DNA changed'
        if not dna:
            dna = PetDNA.getRandomPetDNA()

        self.setDNA(dna)
        
        self.b_setLastSeenTimestamp(self.getCurEpochTimestamp())
        for component in PetMood.PetMood.Components:
            self.setMoodComponent(component, 0.)

        # the trick aptitude code will expand this with zeroes
        self.b_setTrickAptitudes([])

    def setDNA(self, dna):
        head, ears, nose, tail, body, color, colorScale, eyes, gender = dna

        self.b_setHead(head)
        self.b_setEars(ears)
        self.b_setNose(nose)
        self.b_setTail(tail)
        self.b_setBodyTexture(body)
        self.b_setColor(color)
        self.b_setColorScale(colorScale)
        self.b_setEyeColor(eyes)
        self.b_setGender(gender)
        
    def handleZoneChange(self, newZoneId, oldZoneId):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.handleZoneChange(
            self, newZoneId, oldZoneId)
        # we want to stop listening to observes as soon as we change to the
        # quiet zone
        self.ignore(PetObserve.getEventName(oldZoneId))
        self.accept(PetObserve.getEventName(newZoneId),
                    self.brain.observe)

    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        # we've changed to a non-quiet zone
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.handleLogicalZoneChange(
            self, newZoneId, oldZoneId)
        self.announceZoneChange(newZoneId, oldZoneId)
        # re-create our PetSphere, since it holds a handle to a collision
        # traverser, which is zone-specific
        self.destroySphereImpulse()
        self.createSphereImpulse()

    def announceZoneChange(self, newZoneId, oldZoneId):
        DistributedPetAI.notify.debug('%s.announceZoneChange: %s->%s' %
                                      (self.doId, oldZoneId, newZoneId))
        # make other pets observe this zone change
        broadcastZones = list2dict([newZoneId,oldZoneId])
        self.estateOwnerId = simbase.air.estateMgr.getOwnerFromZone(newZoneId)
        if self.estateOwnerId:
            if __dev__:
                assert self.doId in self.air.getObjectsOfClassInZone(
                    self.parentId, self.zoneId, self.__class__)
            self.inEstate = 1
            self.estateZones = simbase.air.estateMgr.getEstateZones(
                self.estateOwnerId)
            #broadcastZones.update(list2dict(self.estateZones))
        else:
            self.inEstate = 0
            self.estateZones = []

        PetObserve.send(broadcastZones.keys(),
                        PetObserve.PetActionObserve(
            PetObserve.Actions.CHANGE_ZONE, self.doId,
            (oldZoneId, newZoneId)))

    def getOwnerId(self):
        return self.ownerId
    def b_setOwnerId(self, ownerId):
        self.d_setOwnerId(ownerId)
        self.setOwnerId(ownerId)
    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getPetName(self):
        return self.petName
    def b_setPetName(self, petName):
        self.d_setPetName(petName)
        self.setPetName(petName)
    def d_setPetName(self, petName):
        self.sendUpdate('setPetName', [petName])
    def setPetName(self, petName):
        self.petName = petName
        # set the nodepath name, for kicks
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.setName(self,
                                                                self.petName)

    def getTraitSeed(self):
        return self.traitSeed
    def b_setTraitSeed(self, traitSeed):
        self.d_setTraitSeed(traitSeed)
        self.setTraitSeed(traitSeed)
    def d_setTraitSeed(self, traitSeed):
        self.sendUpdate('setTraitSeed', [traitSeed])
    def setTraitSeed(self, traitSeed):
        self.traitSeed = traitSeed

    def getSafeZone(self):
        return self.safeZone
    def b_setSafeZone(self, safeZone):
        self.d_setSafeZone(safeZone)
        self.setSafeZone(safeZone)
    def d_setSafeZone(self, safeZone):
        self.sendUpdate('setSafeZone', [safeZone])
    def setSafeZone(self, safeZone):
        self.safeZone = safeZone

    def getPetName(self):
        return self.petName
    def b_setPetName(self, petName):
        self.d_setPetName(petName)
        self.setPetName(petName)
    def d_setPetName(self, petName):
        self.sendUpdate('setPetName', [petName])
    def setPetName(self, petName):
        self.petName = petName
        # set the nodepath name, for kicks
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.setName(self,
                                                                self.petName)

    """ looks like this is not used
    def getTraits(self):
        return self.traitList
    def b_setTraits(self, traitList):
        self.d_setTraits(traitList)
        self.setTraits(traitList)
    def d_setTraits(self, traitList):
        self.sendUpdate('setTraits', [traitList])
        """
    def setTraits(self, traitList):
        self.traitList = traitList
            
    # get, b_set, d_set, and set funcs are generated for each trait
    def __generateDistTraitFuncs(self):
        for i in xrange(PetTraits.PetTraits.NumTraits):
            traitName = PetTraits.getTraitNames()[i]
            getterName = self.getSetterName(traitName, 'get')
            b_setterName = self.getSetterName(traitName, 'b_set')
            d_setterName = self.getSetterName(traitName, 'd_set')
            setterName = self.getSetterName(traitName)
            def traitGetter(i=i):
                return self.traitList[i]
            def b_traitSetter(value, setterName=setterName,
                              d_setterName=d_setterName):
                self.__dict__[d_setterName](value)
                self.__dict__[setterName](value)
            def d_traitSetter(value, setterName=setterName):
                self.sendUpdate(setterName, [value])
            def traitSetter(value, i=i):
                self.traitList[i] = value
            # put the funcs onto self
            self.__dict__[getterName] = traitGetter
            self.__dict__[b_setterName] = b_traitSetter
            self.__dict__[d_setterName] = d_traitSetter
            self.__dict__[setterName] = traitSetter

            self.__funcsToDelete.append(getterName)
            self.__funcsToDelete.append(b_setterName)
            self.__funcsToDelete.append(d_setterName)
            self.__funcsToDelete.append(setterName)

    def getHead(self):
        return self.head
    def b_setHead(self, head):
        self.d_setHead(head)
        self.setHead(head)
    def d_setHead(self, head):
        self.sendUpdate('setHead', [head])
    def setHead(self, head):
        self.head = head

    def getEars(self):
        return self.ears
    def b_setEars(self, ears):
        self.d_setEars(ears)
        self.setEars(ears)
    def d_setEars(self, ears):
        self.sendUpdate('setEars', [ears])
    def setEars(self, ears):
        self.ears = ears

    def getNose(self):
        return self.nose
    def b_setNose(self, nose):
        self.d_setNose(nose)
        self.setNose(nose)
    def d_setNose(self, nose):
        self.sendUpdate('setNose', [nose])
    def setNose(self, nose):
        self.nose = nose

    def getTail(self):
        return self.tail
    def b_setTail(self, tail):
        self.d_setTail(tail)
        self.setTail(tail)
    def d_setTail(self, tail):
        self.sendUpdate('setTail', [tail])
    def setTail(self, tail):
        self.tail = tail

    def getBodyTexture(self):
        return self.bodyTexture
    def b_setBodyTexture(self, bodyTexture):
        self.d_setBodyTexture(bodyTexture)
        self.setBodyTexture(bodyTexture)
    def d_setBodyTexture(self, bodyTexture):
        self.sendUpdate('setBodyTexture', [bodyTexture])
    def setBodyTexture(self, bodyTexture):
        self.bodyTexture = bodyTexture

    def getColor(self):
        return self.color
    def b_setColor(self, color):
        self.d_setColor(color)
        self.setColor(color)
    def d_setColor(self, color):
        self.sendUpdate('setColor', [color])
    def setColor(self, color):
        self.color = color

    def getColorScale(self):
        return self.colorScale
    def b_setColorScale(self, colorScale):
        self.d_setColorScale(colorScale)
        self.setColorScale(colorScale)
    def d_setColorScale(self, colorScale):
        self.sendUpdate('setColorScale', [colorScale])
    def setColorScale(self, colorScale):
        self.colorScale = colorScale

    def getEyeColor(self):
        return self.eyeColor
    def b_setEyeColor(self, eyeColor):
        self.d_setEyeColor(eyeColor)
        self.setEyeColor(eyeColor)
    def d_setEyeColor(self, eyeColor):
        self.sendUpdate('setEyeColor', [eyeColor])
    def setEyeColor(self, eyeColor):
        self.eyeColor = eyeColor

    def getGender(self):
        return self.gender
    def b_setGender(self, gender):
        self.d_setGender(gender)
        self.setGender(gender)
    def d_setGender(self, gender):
        self.sendUpdate('setGender', [gender])
    def setGender(self, gender):
        self.gender = gender

    def teleportIn(self, timestamp=None):
        self.notify.debug("DPAI: teleportIn")
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.notify.debug("DPAI: sending update @ ts = %s" % timestamp)
        self.sendUpdate("teleportIn", [timestamp])
        return None

    def teleportOut(self, timestamp=None):
        self.notify.debug("DPAI: teleportOut")
        timestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        self.notify.debug("DPAI: sending update @ ts = %s" % timestamp)
        self.sendUpdate("teleportOut", [timestamp])
        return None
        
    def getLastSeenTimestamp(self):
        return self.lastSeenTimestamp
    def b_setLastSeenTimestamp(self, timestamp):
        self.d_setLastSeenTimestamp(timestamp)
        self.setLastSeenTimestamp(timestamp)
    def d_setLastSeenTimestamp(self, timestamp):
        self.sendUpdate('setLastSeenTimestamp', [timestamp])
    def setLastSeenTimestamp(self, timestamp):
        self.lastSeenTimestamp = timestamp

    def getCurEpochTimestamp(self):
        # returns timestamp value for 'now' in epoch time, which is how we
        # store the 'last seen' timestamp in the database
        return int(time.time())

    def getTimeSinceLastSeen(self):
        t = time.time() - self.lastSeenTimestamp
        return max(0., t)

    def __handleMoodSet(self, component, value):
        # THIS IS ONLY TO BE USED BY THE MOOD SET HANDLERS
        # see requiredMoodComponents comment in __init__
        if self.isGenerated():
            self.mood.setComponent(component, value)
        else:
            self.requiredMoodComponents[component] = value

    def __handleMoodGet(self, component):
        # THIS IS ONLY TO BE USED BY THE MOOD GET HANDLERS
        if self.isGenerated():
            return self.mood.getComponent(component)
        else:
            return 0.

    # get, b_set, d_set, and set funcs are generated for each mood component
    # this is one of the original function sets:
    """
    def getHunger(self):
        return self.__handleMoodGet('hunger')
    def b_setHunger(self, hunger):
        # our mood obj will gen an event which will cause d_set to be called
        self.setHunger(hunger)
    def d_setHunger(self, hunger):
        self.sendUpdate('setHunger', [hunger])
    def setHunger(self, hunger):
        self.__handleMoodSet('hunger', hunger)"""

    def __generateDistMoodFuncs(self):
        # generate a get, b_set, d_set, and set func for each mood component
        for compName in PetMood.PetMood.Components:
            getterName = self.getSetterName(compName, 'get')
            setterName = self.getSetterName(compName)
            def moodGetter(compName=compName):
                return self.__handleMoodGet(compName)
            def b_moodSetter(value, setterName=setterName):
                # our mood obj will gen an event which will cause d_set
                # to be called
                self.__dict__[setterName](value)
            def d_moodSetter(value, setterName=setterName):
                #print 'sending %s(%s)' % (setterName, value)
                self.sendUpdate(setterName, [value])
            def moodSetter(value, compName=compName):
                self.__handleMoodSet(compName, value)
            # put the funcs onto self
            self.__dict__[getterName] = moodGetter
            self.__dict__['b_%s' % setterName] = b_moodSetter
            self.__dict__['d_%s' % setterName] = d_moodSetter
            self.__dict__[setterName] = moodSetter

            self.__funcsToDelete.append(getterName)
            self.__funcsToDelete.append('b_%s' % setterName)
            self.__funcsToDelete.append('d_%s' % setterName)
            self.__funcsToDelete.append(setterName)

            
    def getTrickAptitudes(self):
        return self.trickAptitudes
    def b_setTrickAptitudes(self, aptitudes):
        self.setTrickAptitudes(aptitudes, local=1)
        self.d_setTrickAptitudes(aptitudes)
    def d_setTrickAptitudes(self, aptitudes):
        if __dev__:
            for aptitude in aptitudes:
                assert 0. <= aptitude <= 1.
        # Fill the array out with zeroes, up to the current number of
        # available tricks, to avoid confusion.
        while (len(aptitudes) < (len(PetTricks.Tricks)-1)):
            aptitudes.append(0.)
        self.sendUpdate('setTrickAptitudes', [aptitudes])
    def setTrickAptitudes(self, aptitudes, local=0):
        if not local:
            DistributedPetAI.notify.debug('setTrickAptitudes: %s' % aptitudes)
        # Fill the array out with zeroes, up to the current number of
        # available tricks, to avoid confusion.
        while (len(self.trickAptitudes) < (len(PetTricks.Tricks)-1)):
            self.trickAptitudes.append(0.)
        self.trickAptitudes = aptitudes
    def getTrickAptitude(self, trickId):
        assert trickId in PetTricks.Tricks
        if trickId > (len(self.trickAptitudes)-1):
            return 0.
        return self.trickAptitudes[trickId]
    def setTrickAptitude(self, trickId, aptitude, send=1):
        # use this func to set aptitudes individually; you can prevent
        # a message from being sent out by setting send=0, but don't forget
        # to then call one of the above functions to distribute the new
        # values to clients when you're done
        assert trickId != PetTricks.Tricks.BALK
        aptitude = clampScalar(aptitude, 0., 1.)
        aptitudes = self.trickAptitudes
        # This while loop produces the old behavior: the array will be only
        # as long as it needs to be. So a pet with no aptitude on any trick
        # will have an empty aptitude array instead of a populated array of
        # zeroes (i.e. [0, 0, 0, 0, 0, 0, 0]), and a pet with aptitude only
        # for trick 3 will have an array like [0, 0, 0, 1] instead of the
        # full array, i.e. [0, 0, 0, 1, 0, 0, 0].  This 'sparse' array has
        # caused confusion. See the changes above that fill out the entire
        # array.
        while ((len(aptitudes)-1) < trickId):
            aptitudes.append(0.)
        if aptitudes[trickId] != aptitude:
            aptitudes[trickId] = aptitude
            if send:
                self.b_setTrickAptitudes(aptitudes)
            else:
                self.setTrickAptitudes(aptitudes, local=1)

    def generate(self):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.generate(self)
        self._hasCleanedUp = False
        self.setHasRequestedDelete(False)
        self.b_setParent(ToontownGlobals.SPHidden)

        self.lockedDown = 0

        self.leashMode = 0
        self.leashAvId = None
        self.leashGoal = None

        self.trickLogger = ServerEventBuffer.ServerEventMultiAccumulator(
            self.air, 'petTricksPerformed', self.doId)
        self.trickFailLogger = ServerEventBuffer.ServerEventMultiAccumulator(
            self.air, 'petTricksFailed', self.doId)
        self.feedLogger = ServerEventBuffer.ServerEventAccumulator(
            self.air, 'petFeedings', self.doId)
        self.scratchLogger = ServerEventBuffer.ServerEventAccumulator(
            self.air, 'petScratchings', self.doId)

        # calculate our traits
        # don't use the trait values from the DB, this should circumvent
        # the corrupted doodle problem
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone)
        """
        self.traits = PetTraits.PetTraits(
            self.traitSeed, self.safeZone,
            traitValueList=copy.copy(self.traitList))
            """

        # don't do this when the pet is being created
        # (see PetManagerAI.createNewPetFromSeed, in handleGetPet)
        if not hasattr(self, '_beingCreatedInDB'):
            # if there are any new traits, we need to set their generated value in
            # the DB.
            for i in xrange(len(self.traitList)):
                value = self.traitList[i]
                if value == 0.:
                    traitName = PetTraits.getTraitNames()[i]
                    traitValue = self.traits.getTraitValue(traitName)
                    DistributedPetAI.notify.info(
                        '%s: initializing new trait \'%s\' to %s, seed=%s' %
                        (self.doId, traitName, traitValue, self.traitSeed))
                    setterName = self.getSetterName(traitName, 'b_set')
                    self.__dict__[setterName](traitValue)

        # create our mood manager. we need to have self.traits first.
        self.mood = PetMood.PetMood(self)

        # if we're just creating this pet so we can manipulate its DB vals,
        # stop here
        if not self.active:
            return

        self.activated = 1

        # simulate an initial zone change, for the benefit of the pet
        # observe system
        self.announceZoneChange(self.zoneId, ToontownGlobals.QuietZone)

        self.b_setParent(ToontownGlobals.SPRender)
        """
        # this doesn't always work correctly, and is not important
        if self.ownerIsInSameZone():
            owner = self._getOwner()
            # our owner may be in the zone, but may still be under hidden
            if self.isSameGraph(owner):
                self.setPosHpr(owner, 4, 4, 0, 135, 0, 0)
                """
        # TODO: this will need to change when pets show up in places other
        # than the estate exterior
        self.setPos(randFloat(-20,20), randFloat(-20,20), 0)
        self.setH(randFloat(360))

        # if a dna was passed on instantiation, set it now
        if self.initialDNA:
            self.setDNA(self.initialDNA)
        
        # pass in the cached required mood component values
        for mood, value in self.requiredMoodComponents.items():
            self.mood.setComponent(mood, value, announce=0)
        self.requiredMoodComponents = {}

        # create our brain
        self.brain = PetBrain.PetBrain(self)

        # the mover will push us around
        self.mover = Mover.Mover(self)

        # The mover that will push us around for the trick
        self.lockMover = Mover.Mover(self)
        
        # cache some impulse objects
        self.createImpulses()

        self.enterPetLook()

        # our 'motor control'
        self.actionFSM = PetActionFSM.PetActionFSM(self)
        #self.actionFSM.request('Neutral')
        self.teleportIn()

        # kickstart the gait FSM
        self.handleMoodChange(distribute=0)

        # we may be created simultaneously with other pets; add some
        # jitter to the start of our processing, to try and spread the
        # processing out over time
        taskMgr.doMethodLater(
            simbase.petMovePeriod * random.random(),
            self.move, self.getMoveTaskName())

        self.startPosHprBroadcast()

        # listen for incoming pet observes (observations)
        self.accept(PetObserve.getEventName(self.zoneId),
                    self.brain.observe)

        # listen for mood changes
        self.accept(self.mood.getMoodChangeEvent(),
                    self.handleMoodChange)

        self.mood.start()
        self.brain.start()

    # for PetLookerAI
    def _isPet(self):
        return 1

    def setHasRequestedDelete(self, flag):
        self._requestedDeleteFlag = flag
    def hasRequestedDelete(self):
        return self._requestedDeleteFlag

    def requestDelete(self, task=None):
        DistributedPetAI.notify.info('PetAI.requestDelete: %s, owner=%s' %
                                     (self.doId, self.ownerId))
        if self.hasRequestedDelete():
            # try to kill crash when requestDelete called twice
            DistributedPetAI.notify.info('PetAI.requestDelete: %s, owner=%s returning immediately' %
                                     (self.doId, self.ownerId))
            return
        # record the fact that we've requested a delete
        self.setHasRequestedDelete(True)

        # record the 'last-seen' timestamp
        self.b_setLastSeenTimestamp(self.getCurEpochTimestamp())

        DistributedSmoothNodeAI.DistributedSmoothNodeAI.requestDelete(self)

    def _doDeleteCleanup(self):
        self.trickLogger.destroy()
        self.trickFailLogger.destroy()
        self.feedLogger.destroy()
        self.scratchLogger.destroy()
        del self.trickLogger
        del self.trickFailLogger
        del self.feedLogger
        del self.scratchLogger
        
        # remove any hooks
        taskMgr.remove(self.uniqueName("clearMovie"))
        taskMgr.remove(self.uniqueName("PetMovieWait"))
        taskMgr.remove(self.uniqueName("PetMovieClear"))
        taskMgr.remove(self.uniqueName('PetMovieComplete'))
        taskMgr.remove(self.getLockMoveTaskName())
        taskMgr.remove(self.getMoveTaskName())

        # simulate a final zone change to the quiet zone, for the benefit
        # of the pet observe system
        if hasattr(self, "zoneId"):
            self.announceZoneChange(ToontownGlobals.QuietZone, self.zoneId)
        else:
            myDoId = "No doId"
            myTaskName = "No task name"
            myStackTrace = StackTrace().trace
            myOldStackTrace = "No Trace"
            
            if hasattr(self, "doId"):
                myDoId = self.doId
            if task:
                myTaskName = task.name
            if hasattr(self, "destroyDoStackTrace"):
                myOldStackTrace = self.destroyDoStackTrace.trace
            

            simbase.air.writeServerEvent("Pet RequestDelete duplicate", myDoId, "from task %s" % (myTaskName))
            simbase.air.writeServerEvent("Pet RequestDelete duplicate StackTrace", myDoId, "%s" % myStackTrace)
            simbase.air.writeServerEvent("Pet RequestDelete duplicate OldStackTrace", myDoId, "%s" % myOldStackTrace)
            
            DistributedPetAI.notify.warning("double requestDelete from task %s" % (myTaskName))
        self.setParent(hidden)

        if hasattr(self, "activated"):
            if self.activated:
                self.activated = 0
                # already done above
                #taskMgr.remove(self.getMoveTaskName())
                self.brain.destroy()
                del self.brain
                self.actionFSM.destroy()
                del self.actionFSM
                self.exitPetLook()
                self.destroyImpulses()
                self.mover.destroy()
                del self.mover
                self.lockMover.destroy()
                del self.lockMover
                # this was causing trouble when it was done before destruction
                # of actionFSM. If a pet was doing a trick, the broadcast task
                # was being restarted. It shouldn't matter anymore, since
                # DistributedSmoothNodeBase makes sure the task is stopped
                # on deletion.
                self.stopPosHprBroadcast()
            
        if hasattr(self, "mood"):
            self.mood.destroy()
            del self.mood
        if hasattr(self, "traits"):
            del self.traits
        
        try:
            for funcName in self.__funcsToDelete:
                del self.__dict__[funcName]
        except:
            pass

        # this needs to be one of the last things deleted
        if hasattr(self, "gaitFSM"):
            if self.gaitFSM:
                self.gaitFSM.requestFinalState()
            del self.gaitFSM

        if hasattr(self, "unstickFSM"):
            if self.unstickFSM:
                self.unstickFSM.requestFinalState()
            del self.unstickFSM

        if __dev__:
            del self.pscMoveResc

        PetLookerAI.PetLookerAI.destroy(self)
        self.ignoreAll()

        self._hasCleanedUp = True

    def delete(self):
        DistributedPetAI.notify.info('PetAI.delete: %s, owner=%s' %
                                     (self.doId, self.ownerId))

        # if we didn't request a delete, but the server sent us a delete,
        # make sure we clean up
        if not self._hasCleanedUp:
            self._doDeleteCleanup()

        self.setHasRequestedDelete(False)

        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)

    def patchDelete(self):
        # called by the patcher to remove cyclical references and prevent
        # memory leak
        for funcName in self.__funcsToDelete:
            del self.__dict__[funcName]

        del self.gaitFSM
        del self.unstickFSM

        if __dev__:
            del self.pscMoveResc

        PetLookerAI.PetLookerAI.destroy(self)
        # prevent a crash; we do not own our doId and do not have a zoneId
        self.doNotDeallocateChannel = True
        self.zoneId = None
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        self.ignoreAll()

    def createImpulses(self):
        # for efficiency, create these impulses up-front and use them when
        # needed
        self.createSphereImpulse()
        #self.chaseImpulse = PetChase.PetChase()
        self.chaseImpulse = CPetChase()
        #self.fleeImpulse = PetFlee.PetFlee()
        self.fleeImpulse = CPetFlee()
        self.wanderImpulse = PetWander.PetWander()

        # Impulses for the trick
        #self.lockSphereImpulse = PetSphere.PetSphere(petRadius, self.getCollTrav())
        self.lockChaseImpulse = CPetChase()

    def destroyImpulses(self):
        #self.chaseImpulse.destroy()
        #self.fleeImpulse.destroy()
        self.wanderImpulse.destroy()
        #self.colliderImpulse.destroy()
        del self.chaseImpulse
        del self.fleeImpulse
        del self.wanderImpulse
        #del self.colliderImpulse
        self.destroySphereImpulse()

        #self.lockSphereImpulse.destroy()
        #del self.lockSphereImpulse
        del self.lockChaseImpulse

    def createSphereImpulse(self):
        petRadius = 1.
        collTrav = self.getCollTrav()
        if collTrav is None:
            DistributedPetAI.notify.warning(
                'no collision traverser for zone %s' % self.zoneId)
        else:
            self.sphereImpulse = PetSphere.PetSphere(petRadius, collTrav)
            # this is always on
            self.mover.addImpulse('sphere', self.sphereImpulse)

        """
        # TODO: 1 or 2? or is this something different?
        petRadius = 2.
        self.colliderImpulse = PetCollider.PetCollider(
            petRadius, self.getCollTrav())
            """

    def destroySphereImpulse(self):
        self.mover.removeImpulse('sphere')
        if hasattr(self, 'sphereImpulse'):
            self.sphereImpulse.destroy()
            del self.sphereImpulse

    def getMoveTaskName(self):
        return 'petMove-%s' % self.doId
    def getLockMoveTaskName(self):
        return 'petLockMove-%s' % (self.doId)

    def move(self, task=None):
        
        if self.isEmpty():
            try:
                self.air.writeServerEvent("Late Pet Move Call", self.doId, " ")
            except:
                pass
            taskMgr.remove(task.name)
            return Task.done
            
        
        if not self.isLockMoverEnabled():
            self.mover.move()

        # modulate the position broadcast frequency based on how crowded
        # the zone is
        numNearby = len(self.brain.nearbyAvs)-1 # owner is always there
        minNearby = 5
        if numNearby > minNearby:
            # this delay was arrived at empirically
            delay = .08 * (numNearby-minNearby)
            # randomly jitter the delay so that all the pets don't move
            # simultaneously
            self.setPosHprBroadcastPeriod(PetConstants.PosBroadcastPeriod +
                                          lerp(delay*.75,delay,random.random())
                                          )

        # make sure the pet doesn't run off into the hills and crash
        # the AI server (out-of-bounds DC values passed in to setPos)
        maxDist = 1000
        if abs(self.getX()) > maxDist or abs(self.getY()) > maxDist:
            DistributedPetAI.notify.warning(
                'deleting pet %s before he wanders off too far' % self.doId)
            self._outOfBounds = True
            self.stopPosHprBroadcast()
            self.requestDelete()
            # in this case make sure we don't schedule another run of this task
            return Task.done
            
        # schedule the next move
        if __dev__:
            self.pscMoveResc.start()
        taskMgr.doMethodLater(simbase.petMovePeriod, self.move,
                              self.getMoveTaskName())
        if __dev__:
            self.pscMoveResc.stop()
        return Task.done

    def startPosHprBroadcast(self):
        if self._outOfBounds:
            return
        # force XYH only
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.startPosHprBroadcast(
            self,
            period=simbase.petPosBroadcastPeriod,
            type=DistributedSmoothNodeBase.DistributedSmoothNodeBase.BroadcastTypes.XYH)

    # you can call these funcs to influence the pet's mood
    def setMoodComponent(self, component, value):
        assert 0. <= value <= 1.
        setter = self.getSetterName(component, 'b_set')
        self.__dict__[setter](value)
    def addToMood(self, component, delta):
        # delta is in [-1..1]
        # delta will be added to component, and result is clamped to [0..1]
        assert -1. <= delta <= 1.
        value = self.mood.getComponent(component)
        value += delta
        self.setMoodComponent(component, clampScalar(value, 0., 1.))
    def lerpMood(self, component, factor):
        # factor is in [-1..1]
        # [-1..0] will lerp towards zero, [0..1] will lerp towards one.
        assert -1. <= factor <= 1.
        curVal = self.mood.getComponent(component)
        if factor < 0:
            self.setMoodComponent(component, lerp(curVal, 0.,-factor))
        else:
            self.setMoodComponent(component, lerp(curVal, 1., factor))
    def addToMoods(self, mood2delta):
        for mood, delta in mood2delta.items():
            self.addToMood(mood, delta)
    def lerpMoods(self, mood2factor):
        for mood, factor in mood2factor.items():
            self.lerpMood(mood, factor)
    if __debug__:
        def maxMood(self):
            self.mood.max()
        def minMood(self):
            self.mood.min()

    def handleMoodChange(self, components=[], distribute=1):
        # this gets called whenever the PetMood updates a mood component
        if len(components) == 0:
            components = PetMood.PetMood.Components

        if distribute:
            # send distributed updates for the components that changed
            # did all of the components change?
            if len(components) == len(PetMood.PetMood.Components):
                values = []
                # order is VERY important here
                for comp in PetMood.PetMood.Components:
                    values.append(self.mood.getComponent(comp))
                #print 'sending ALL moods'
                self.sendUpdate('setMood', values)
            else:
                for comp in components:
                    # do some function-call jujitsu
                    setter = self.getSetterName(comp, 'd_set')
                    self.__dict__[setter](self.mood.getComponent(comp))

        # update the gait FSM
        # map our complex mood to the simple anim mood set using the
        # shared functions in PetBase (shared with the client)
        if self.isExcited():
            self.gaitFSM.request('happy')
        elif self.isSad():
            self.gaitFSM.request('sad')
        else:
            self.gaitFSM.request('neutral')

    def isContented(self):
        assert contains(
            list(PetMood.PetMood.Components) + [PetMood.PetMood.Neutral],
            PetMood.PetMood.ContentedMoods)
        return self.mood.getDominantMood() in PetMood.PetMood.ContentedMoods

    #------------------------------------------------------------------
    # public interface for other AI objects to influence this pet
    # as an actual pet/animal
    def call(self, avatar):
        self.brain.observe(PetObserve.PetPhraseObserve(
            PetObserve.Phrases.COME, avatar.doId))
        self.__petMovieStart(avatar.doId)
        
    def feed(self, avatar):
        if avatar.takeMoney(PetConstants.FEED_AMOUNT):
            self.startLockPetMove(avatar.doId)
            self.brain.observe(PetObserve.PetActionObserve(
                PetObserve.Actions.FEED, avatar.doId))
            self.feedLogger.addEvent()

    def scratch(self, avatar):
        self.startLockPetMove(avatar.doId)
        self.brain.observe(PetObserve.PetActionObserve(
            PetObserve.Actions.SCRATCH, avatar.doId))
        self.scratchLogger.addEvent()
    #------------------------------------------------------------------

    def lockPet(self):
        # call this when you need to lock the pet down in order to play
        # a movie on him
        DistributedPetAI.notify.debug('%s: lockPet' % self.doId)

        # Had to change this because stopPosHprBroadcast was not being
        # called to run the lockMover. This guarantees that there is an
        # intermediate lock phase, and a final lock phase. Intermediate
        # doesn't allow the normal mover to run, but it allows the lockMover
        # to position the pet for a movie. The final lock phase stops both
        # movers and truly locks the pet down.
        if not self.lockedDown:
            self.stopPosHprBroadcast()
        self.lockedDown += 1

    def isLockedDown(self):
        return self.lockedDown != 0

    def unlockPet(self):
        # call this when you're done playing the movie
        DistributedPetAI.notify.debug('%s: unlockPet' % self.doId)

        if self.lockedDown <= 0:
            DistributedPetAI.notify.warning(
                '%s: unlockPet called on unlocked pet' % self.doId)
        else:
            self.lockedDown -= 1
            if not self.lockedDown and not self.isDeleted():
                self.startPosHprBroadcast()

    # these are for magic words
    def handleStay(self, avatar):
        self.brain.observe(PetObserve.PetPhraseObserve(
            PetObserve.Phrases.STAY, avatar.doId))
    def handleShoo(self, avatar):
        self.brain.observe(PetObserve.PetPhraseObserve(
            PetObserve.Phrases.GO_AWAY, avatar.doId))

    # gait states
    def gaitEnterOff(self):
        pass
    def gaitExitOff(self):
        pass
    
    def gaitEnterNeutral(self):
        self.mover.setFwdSpeed(PetConstants.FwdSpeed)
        self.mover.setRotSpeed(PetConstants.RotSpeed)
    def gaitExitNeutral(self):
        pass

    def gaitEnterHappy(self):
        self.mover.setFwdSpeed(PetConstants.HappyFwdSpeed)
        self.mover.setRotSpeed(PetConstants.HappyRotSpeed)
    def gaitExitHappy(self):
        pass

    def gaitEnterSad(self):
        self.mover.setFwdSpeed(PetConstants.SadFwdSpeed)
        self.mover.setRotSpeed(PetConstants.SadRotSpeed)
    def gaitExitSad(self):
        pass

    # unstick FSM
    def unstickEnterOff(self):
        pass
    def unstickExitOff(self):
        pass

    def unstickEnterOn(self):
        # queue of timestamps of collisions
        self._collisionTimestamps = []
        self.accept(self.mover.getCollisionEventName(), self._handleCollided)
    def _handleCollided(self, collEntry):
        now = globalClock.getFrameTime()
        self._collisionTimestamps.append(now)
        while ((now - self._collisionTimestamps[0]) >
                PetConstants.UnstickSampleWindow):
            del self._collisionTimestamps[0:1]
        if (len(self._collisionTimestamps) >
                PetConstants.UnstickCollisionThreshold):
            self._collisionTimestamps = []
            DistributedPetAI.notify.debug('unsticking pet %s' % self.doId)
            self.brain._unstick()
    def unstickExitOn(self):
        pass

    # get info on our owner
    def ownerIsOnline(self):
        return self.ownerId in simbase.air.doId2do
    def ownerIsInSameZone(self):
        if not self.ownerIsOnline():
            return 0
        return self.zoneId == simbase.air.doId2do[self.ownerId].zoneId

    # these functions return dicts of nearby avatars
    def _getOwnerDict(self):
        """returns in a dict to match format of other calls"""
        if self.owner is not None:
            if self.ownerIsInSameZone():
                return {self.ownerId: self.owner}
        return {}
    def _getFullNearbyToonDict(self):
        """includes owner"""
        toons = self.air.getObjectsOfClassInZone(
            self.air.districtId, self.zoneId,
            DistributedToonAI.DistributedToonAI)
        return toons
    def _getNearbyToonDict(self):
        """does not include owner"""
        toons = self._getFullNearbyToonDict()
        # exclude our owner
        if self.ownerId in toons:
            del toons[self.ownerId]
        return toons
    def _getNearbyPetDict(self):
        # pick a pet to chase
        pets = self.air.getObjectsOfClassInZone(
            self.air.districtId, self.zoneId, DistributedPetAI)
        # exclude ourselves
        if self.doId in pets:
            del pets[self.doId]
        return pets
    def _getNearbyAvatarDict(self):
        avs = self._getFullNearbyToonDict()
        avs.update(self._getNearbyPetDict())
        return avs

    # these return a single nearby avatar, randomly chosen
    def _getOwner(self):
        return self.air.doId2do.get(self.ownerId)
    def _getNearbyToon(self):
        nearbyToonDict = self._getFullNearbyToonDict()
        if not len(nearbyToonDict):
            return None
        return nearbyToonDict[random.choice(nearbyToonDict.keys())]
    def _getNearbyToonNonOwner(self):
        nearbyToonDict = self._getNearbyToonDict()
        if not len(nearbyToonDict):
            return None
        return nearbyToonDict[random.choice(nearbyToonDict.keys())]
    def _getNearbyPet(self):
        nearbyPetDict = self._getNearbyPetDict()
        if not len(nearbyPetDict):
            return None
        return nearbyPetDict[random.choice(nearbyPetDict.keys())]
    def _getNearbyAvatar(self):
        nearbyAvDict = self._getNearbyAvatarDict()
        if not len(nearbyAvDict):
            return None
        return nearbyAvDict[random.choice(nearbyAvDict.keys())]

    #
    # pet movie methods
    #

    def isBusy(self):
        return (self.busy > 0)

    def freeAvatar(self, avId):
        # Free this avatar, probably because he requested interaction while
        # I was busy. This can happen when two avatars request interaction
        # at the same time. The AI will accept the first, sending a setMovie,
        # and free the second
        self.sendUpdateToAvatarId(avId, "freeAvatar", [])

    def avatarInteract(self, avId):
        # an avatar has approached the pet and requested to interact
        assert(self.notify.debug("avatar enter avId: %s busy: %s " % (avId, self.busy)))

        av = self.air.doId2do.get(avId)
        
        if av is None:
            self.notify.warning("Avatar: %s not found" % (avId))
            return 0

        if self.isBusy():
            self.notify.debug("freeing avatar!")
            self.freeAvatar(avId)
            return 0

        self.busy = avId

        self.notify.debug("sending update")
        self.sendUpdateToAvatarId(avId, "avatarInteract", [avId])
        
        # handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])
        return 1

    def rejectAvatar(self, avId):
        self.notify.error("rejectAvatar: should not be called by a pet!")

    def d_setMovie(self, avId, flag):
        # tell the client to do its thing
        self.sendUpdate("setMovie",
                        [flag, avId,
                         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def sendClearMovie(self, task=None):
        assert(self.notify.debug('sendClearMovie()'))
        # Ignore unexpected exits on whoever I was busy with
        if self.air != None:
            self.ignore(self.air.getAvatarExitEvent(self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.busy = 0
        self.d_setMovie(0, PetConstants.PET_MOVIE_CLEAR)
        return Task.done
        
    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.sendClearMovie()

    ######################################################################
    # Method: handleAvPetInteraction
    # Purpose: This method should be called whenever an Avatar/Pet
    #          Interaction occurs. For example, when the Avatar feeds the
    #          pet. It starts the overall process of running an interaction
    #          movie. This should typically be called by any magic words or
    #          the PetAvatarPanel buttons that will generate the interaction.
    # Input: mode - type of interaction that is occuring
    #        avId - id of the avatar that the pet is interacting with.
    # Output: None
    ######################################################################
    def handleAvPetInteraction(self, mode, avId):
        # Setup the avatar interaction and call the observation callback
        # method.
        if mode not in (PetConstants.PET_MOVIE_SCRATCH,
                        PetConstants.PET_MOVIE_FEED,
                        PetConstants.PET_MOVIE_CALL):
            self.air.writeServerEvent('suspicious', avId,
                                      'DistributedPetAI: unknown mode: %s' % (mode))
            return
        if self.avatarInteract(avId):
            self.notify.debug("handleAvPetInteraction() avatarInteract calling callback")
            # Set the current movie mode for the interaction
            self.movieMode = mode

            # We need to get the pet up to the avatar before anything happens!
            # A callback method dictionary which emulates a c-like switch.
            callback = { PetConstants.PET_MOVIE_SCRATCH : self.scratch,
                         PetConstants.PET_MOVIE_FEED : self.feed,
                         PetConstants.PET_MOVIE_CALL : self.call }.get(mode)
            callback(self.air.doId2do.get(avId))
        else:
            self.notify.debug("handleAvPetInteraction() avatarInteract was busy or unhappy")

    ######################################################################
    # Method: __petMovieStart
    # Purpose: This method arranges for the particular interaction to
    #          start.
    # Input: avId - id of the avatar that the pet is interacting with.
    # Output: None
    ######################################################################
    def __petMovieStart(self, avId):
        # send out a single movie command
        self.d_setMovie(avId, self.movieMode)
        # schedule cleanup
        time = self.movieTimeSwitch.get(self.movieMode)
        taskMgr.doMethodLater(time, self.__petMovieComplete,
                              self.uniqueName('PetMovieComplete'))
        return

    def __petMovieComplete(self, task=None):
        # clean up after pet movie in simpler, single-message movie scheme
        # Disable the Lock Mover so that the normal mover can resume
        # and unlock the Pet
        self.disableLockMover()
        self.unlockPet()
        self.sendClearMovie()
        self.movieMode = None
        return Task.done

    ######################################################################
    # Method: startLockPetMove
    # Purpose: This sets up the secondary pet mover (self.lockMover) and
    #          the secondary chaseImpulse( self.lockChaseImpulse) to move
    #          the pet to the avatar so that an interaction can occur.
    # Input: avId - id of the avatar that the pet is interacting with.
    # Output: None
    ######################################################################
    def startLockPetMove(self, avId):
        # Set the intermediate lock phase, ie where the main Pet mover
        # (self.mover) no longer moves the pet.
        self.enableLockMover()

        # We are no longer using the original mover. Instead, we will
        # have our mover bring the pet over to the toon via a new chase impulse
        # that will have its own min_dist set.
        self.lockChaseImpulse.setTarget(self.air.doId2do.get(avId))
        self.lockMover.addImpulse('LockTarget', self.lockChaseImpulse)
        self.lockMover.setFwdSpeed(self.mover.getFwdSpeed())
        self.lockMover.setRotSpeed(self.mover.getRotSpeed())

        # Returns the minimum distance for the pet to approach the toon based
        # on toon leg size. How tall is the toon?
        dist_Callable = self.movieDistSwitch.get(self.movieMode)
        dist = dist_Callable(
            self.air.doId2do.get(avId).getStyle().getLegSize())
        
        self.lockChaseImpulse.setMinDist(dist)

        # Dist list is used to store the last three distance checks. It is
        # necessary because the AI toon does not necessarily reach the min_dist
        # set above for some reason. Thus, the movie would hang because the dist
        # check is waiting to reach that distance, but the pet is no longer moving.
        self.distList = [0,0,0]

        # Start the movement task
        self.__lockPetMoveTask(avId) 

    ######################################################################
    # Method: getAverageDist
    # Purpose: This method returns the average distance from the dist
    #          values found in the distList.
    # Input: None
    # Output: returns the average distance
    ######################################################################
    def getAverageDist(self):
        sum = 0
        for i in self.distList:
            sum += i
        return (sum / 3.0)

    ######################################################################
    # Method: __lockPetMoveTask
    # Purpose: This method moves the pet towards the avatar so that it is
    #          in the proper distance for the interaction to take place.
    # Input: avId - id of the Avatar for which the pet will interact
    # Output: None
    ######################################################################
    def __lockPetMoveTask(self, avId):
        # In case the pet or toon has been deleted without cleaning up this
        # task, we need to do some checking first
        if (not hasattr(self, 'air') or not self.air.doId2do.has_key(avId)):
            self.notify.warning("avId: %s gone or self deleted!" % avId)
            # TODO: do we need to do some cleanup here?
            return Task.done

        av = self.air.doId2do.get(avId)

        # Retrieve the current distance between the pet and the avatar. Store
        # it in the dist list.
        dist = av.getDistance(self)
        self.distList.append(dist)
        if len(self.distList) > 3:
            self.distList.pop(0)

        # We need to calculate the distance the pet should come within for
        # toons of varying size. Shorter toons need the pet to come in closer,
        # while tall toons need them to stay out a little further.
        if self.movieDistSwitch.has_key(self.movieMode):
            dist_Callable = self.movieDistSwitch.get(self.movieMode)
            movieDist = dist_Callable(av.getStyle().getLegSize())
        else:
            self.notify.warning("movieMode: %s not in movieSwitchDist map!" % self.movieMode)
            return Task.done

        avgDist = self.getAverageDist()

        # Distance check to see if the pet is within the minimum distance
        # radius that we were hoping for. At the time of this implementation,
        # a pet mover does not throw a message once it has reached the minimum
        # distance. So we must check to know when we should continue.
        if (dist-movieDist)> .25 and abs(avgDist-dist)> 0.1:
            self.lockMover.move()
            taskMgr.doMethodLater(simbase.petMovePeriod,
                                  self.__lockPetMoveTask,
                                  self.getLockMoveTaskName(), [avId])
        else:
            # Distance check has been met, thus we continue on with the
            # movie. 
            self.endLockPetMove(avId)

        return Task.done

    ######################################################################
    # Method: endLockPetMove
    # Purpose: This method stops the places the final lock on the avatar
    #          cleans up the lockMover. It then tells the client to
    #          begin the actual movie since the Pet is now in place.
    # Input: avId - id of the Avatar for which the pet will interact
    # Output: None
    ######################################################################
    def endLockPetMove(self, avId):
        del self.distList
        taskMgr.remove(self.getLockMoveTaskName())

        # Apply the final lock on the pet.
        self.lockPet()
        self.lockMover.removeImpulse('LockTarget')
        self.__petMovieStart(avId)

    def enableLockMover(self):
        assert self.lockMoverEnabled >= 0
        if self.lockMoverEnabled == 0:
            self.brain._startMovie()
        self.lockMoverEnabled += 1
    def isLockMoverEnabled(self):
        return (self.lockMoverEnabled > 0)
    def disableLockMover(self):
        assert self.lockMoverEnabled >= 0
        if self.lockMoverEnabled > 0:
            self.lockMoverEnabled -= 1
            if self.lockMoverEnabled == 0:
                self.brain._endMovie()
            
    # TRICK APTITUDE LOGIC
    def _willDoTrick(self, trickId):
        # Use this to determine whether or not the pet will do a particular
        # trick. This takes into account the pet's aptitude toward
        # the particular trick, as well as the pet's fatigue state.
        if self.isContented():
            minApt = PetTricks.MinActualTrickAptitude
            maxApt = PetTricks.MaxActualTrickAptitude
        else:
            minApt = PetTricks.NonHappyMinActualTrickAptitude
            maxApt = PetTricks.NonHappyMaxActualTrickAptitude
        randVal = random.random()
        cutoff = lerp(minApt, maxApt, self.getTrickAptitude(trickId))
        # even less likely to do the trick if fatigued
        if self.mood.isComponentActive('fatigue'):
            cutoff *= .5
        # Apply base accuracy for the specific trick
        assert(PetTricks.TrickAccuracies.has_key(trickId))
        cutoff *= PetTricks.TrickAccuracies[trickId]
        DistributedPetAI.notify.debug('_willDoTrick: %s / %s' % (
            randVal, cutoff))
        return randVal < cutoff

    def _handleDidTrick(self, trickId):
        # the pet just finished doing this trick; update his stats
        DistributedPetAI.notify.debug('_handleDidTrick: %s' % trickId)
        if trickId == PetTricks.Tricks.BALK:
            return
        aptitude = self.getTrickAptitude(trickId)
        self.setTrickAptitude(trickId,
                              aptitude + PetTricks.AptitudeIncrementDidTrick)
        # pets get tired after a trick
        self.addToMood('fatigue', lerp(PetTricks.MaxTrickFatigue,
                                       PetTricks.MinTrickFatigue,
                                       aptitude))
        self.trickLogger.addEvent(trickId)

    def _handleGotPositiveTrickFeedback(self, trickId, magnitude):
        if trickId == PetTricks.Tricks.BALK:
            return
        # the pet did a trick, and someone praised him; update his stats
        assert 0. <= magnitude <= 1.
        self.setTrickAptitude(
            trickId,
            self.getTrickAptitude(trickId) +
            (PetTricks.MaxAptitudeIncrementGotPraise * magnitude))
        
    # LEASH MAGIC WORD
    def toggleLeash(self, avId):
        # FOR DEBUGGING
        # if leash is on, follow this avatar
        if self.leashMode:
            self.leashMode = 0
            self.leashAvId = None
            self.brain.goalMgr.removeGoal(self.leashGoal)
            del self.leashGoal
            response = 'leash OFF'
        else:
            self.leashMode = 1
            self.leashAvId = avId
            self.leashGoal = PetGoal.ChaseAvatarLeash(avId)
            self.brain.goalMgr.addGoal(self.leashGoal)
            response = 'leash ON'
        # magic word response
        return response
            
