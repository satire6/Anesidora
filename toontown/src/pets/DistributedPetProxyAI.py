from direct.showbase.PythonUtil import contains, lerp, clampScalar
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.pets import PetTraits, PetTricks
from toontown.pets import PetMood
from toontown.toonbase import ToontownGlobals
import random
import time
import string
import copy

BATTLE_TRICK_HP_MULTIPLIER = 10.0

class DistributedPetProxyAI(DistributedObjectAI.DistributedObjectAI):
    """A way to query pet DNA from the database without creating a 
       DistributedPet object"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPetProxyAI")
    #notify.setDebug(True)

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.ownerId = 0
        self.petName = 'unnamed'
        self.traitSeed = 0
        self.safeZone = ToontownGlobals.ToontownCentral

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

        self.trickAptitudes = []

        self.lastSeenTimestamp = self.getCurEpochTimestamp()

        self.requiredMoodComponents = {}

        # create our distributed trait and mood funcs
        # Keep track of all the funcs that we stuff into our dict
        self.__funcsToDelete = []
        self.__generateDistTraitFuncs()
        self.__generateDistMoodFuncs()

    def getSetterName(self, valueName, prefix='set'):
        return '%s%s%s' % (prefix, string.upper(valueName[0]), valueName[1:])

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
            DistributedPetProxyAI.notify.debug('setTrickAptitudes: %s' % aptitudes)
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
        DistributedObjectAI.DistributedObjectAI.generate(self)

        # calculate our traits
        # don't use the trait values from the DB, this should circumvent
        # the corrupted doodle problem
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone)
        print self.traits.traits
        """
        self.traits = PetTraits.PetTraits(
            self.traitSeed, self.safeZone,
            traitValueList=copy.copy(self.traitList))
            """


        # if there are any new traits, we need to set their generated value in
        # the DB.
        for i in xrange(len(self.traitList)):
            value = self.traitList[i]
            if value == 0.:
                traitName = PetTraits.getTraitNames()[i]
                traitValue = self.traits.getTraitValue(traitName)
                DistributedPetProxyAI.notify.info(
                    '%s: initializing new trait \'%s\' to %s, seed=%s' %
                    (self.doId, traitName, traitValue, self.traitSeed))
                setterName = self.getSetterName(traitName, 'b_set')
                self.__dict__[setterName](traitValue)

        # create our mood manager. we need to have self.traits first.
        self.mood = PetMood.PetMood(self)

        # pass in the cached required mood component values
        for mood, value in self.requiredMoodComponents.items():
            self.mood.setComponent(mood, value, announce=0)
        self.requiredMoodComponents = {}

        # listen for mood changes
        self.accept(self.mood.getMoodChangeEvent(),
                    self.handleMoodChange)

        self.mood.start()

    def broadcastDominantMood(self):
        self.d_setDominantMood(self.mood.getDominantMood())

    def delete(self):
        self.ignore(self.mood.getMoodChangeEvent())
        self.mood.destroy()
        del self.mood
        del self.traits
        for funcName in self.__funcsToDelete:
            del self.__dict__[funcName]
        DistributedObjectAI.DistributedObjectAI.delete(self)

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

    def isContented(self):
        assert contains(
            list(PetMood.PetMood.Components) + [PetMood.PetMood.Neutral],
            PetMood.PetMood.ContentedMoods)
        return self.mood.getDominantMood() in PetMood.PetMood.ContentedMoods

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
        DistributedPetProxyAI.notify.debug('_willDoTrick: %s / %s' % (
            randVal, cutoff))
        return randVal < cutoff

    def _handleDidTrick(self, trickId):
        # the pet just finished doing this trick; update his stats
        DistributedPetProxyAI.notify.debug('_handleDidTrick: %s' % trickId)
        if trickId == PetTricks.Tricks.BALK:
            return
        aptitude = self.getTrickAptitude(trickId)
        self.setTrickAptitude(trickId,
                              aptitude + PetTricks.AptitudeIncrementDidTrick)
        # pets get tired after a trick
        self.addToMood('fatigue', lerp(PetTricks.MaxTrickFatigue,
                                       PetTricks.MinTrickFatigue,
                                       aptitude))
        # MPG: Pet proxies don't have a trick logger
        #self.trickLogger.addEvent(trickId)
        self.d_setDominantMood(self.mood.getDominantMood())

    def attemptBattleTrick(self, trickId):

        # Go ahead and make the pet get a little more excited because
        # he's been called to a battle
        self.lerpMoods({
                'boredom' : -.1,
                'excitement' : .05,
                'loneliness' : -.05,
                })

        if self._willDoTrick(trickId): 
            #print "trick succeeded"
            self._handleDidTrick(trickId)
            self.b_setLastSeenTimestamp(self.getCurEpochTimestamp())
            return 0
        else:
            #print "trick failed"
            #chosenTrick = PetTricks.Tricks.BALK
            self.b_setLastSeenTimestamp(self.getCurEpochTimestamp())
            return 1

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

    def d_setDominantMood(self, dominantMood):
        self.sendUpdate('setDominantMood', [dominantMood])
