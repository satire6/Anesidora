from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.pets import PetTraits
from toontown.pets import PetMood, PetTricks
from toontown.toonbase import ToontownGlobals
import string

class DistributedPetProxy(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPetProxy")

    def __init__(self, cr): 
        DistributedObject.DistributedObject.__init__(self, cr)
        # create our distributed trait and mood funcs
        self.__funcsToDelete = []
        self.__generateDistTraitFuncs()
        self.__generateDistMoodFuncs()
        self.dominantMood = 'neutral'
        self.sendGenerateMessage = 0
        self.trickAptitudes = []
        self.ghostMode = False

        # this tells the pet panel to *not* delete me
        self.bFake = False

    def generate(self):
        # this will be filled in during generation
        DistributedObject.DistributedObject.generate(self)
        self.traitList = [0] * PetTraits.PetTraits.NumTraits

        # cache required mood components until we have a self.mood to give
        # them to
        self.requiredMoodComponents = {}

    def getSetterName(self, valueName, prefix='set'):
        return '%s%s%s' % (prefix, string.upper(valueName[0]), valueName[1:])

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getOwnerId(self):
        return self.ownerId

    def setPetName(self, petName):
        self.petName = petName

    def setTraitSeed(self, traitSeed):
        self.traitSeed = traitSeed

    def setSafeZone(self, safeZone):
        self.safeZone = safeZone

    # setXXX func is generated for each trait
    def __generateDistTraitFuncs(self):
        # generate a set func for each trait
        for i in xrange(PetTraits.PetTraits.NumTraits):
            traitName = PetTraits.getTraitNames()[i]
            setterName = self.getSetterName(traitName)
            def traitSetter(value, self=self, i=i):
                self.traitList[i] = value
            # put the func onto self
            self.__dict__[setterName] = traitSetter
            self.__funcsToDelete.append(setterName)

    def setHead(self, head):
        DistributedPetProxy.notify.debug('setHead: %s' % head)
        self.head = head

    def setEars(self, ears):
        DistributedPetProxy.notify.debug('setEars: %s' % ears)
        self.ears = ears

    def setNose(self, nose):
        DistributedPetProxy.notify.debug('setNose: %s' % nose)
        self.nose = nose

    def setTail(self, tail):
        DistributedPetProxy.notify.debug('setTail: %s' % tail)
        self.tail = tail

    def setBodyTexture(self, bodyTexture):
        DistributedPetProxy.notify.debug('setBodyTexture: %s' % bodyTexture)
        self.bodyTexture = bodyTexture

    def setColor(self, color):
        DistributedPetProxy.notify.debug('setColor: %s' % color)
        self.color = color

    def setColorScale(self, colorScale):
        DistributedPetProxy.notify.debug('setColorScale: %s' % colorScale)
        self.colorScale = colorScale

    def setEyeColor(self, eyeColor):
        DistributedPetProxy.notify.debug('setEyeColor: %s' % eyeColor)
        self.eyeColor = eyeColor

    def setGender(self, gender):
        DistributedPetProxy.notify.debug('setGender: %s' % gender)
        self.gender = gender

    def getDNA(self):
        return self.style

    def getName(self):
        return self.petName

    def getFont(self):
        # All friends are toons.
        return ToontownGlobals.getToonFont()

    def setLastSeenTimestamp(self, timestamp):
        DistributedPetProxy.notify.debug('setLastSeenTimestamp: %s' % timestamp)
        self.lastSeenTimestamp = timestamp

    def getTimeSinceLastSeen(self):
        # returns time since pet was last seen on the AI
        t = self.cr.getServerTimeOfDay() - self.lastSeenTimestamp
        return max(0., t)

    def updateOfflineMood(self):
        # Used by the client to figure out what the pet's mood is when
        # the pet is not currently instantiated on the AI. Once the pet's
        # last-known-mood fields and last-seen timestamp are filled in,
        # and the object is 'fake-generated', you can call this at any
        # time to recalculate the pet's mood.
        self.mood.driftMood(dt=self.getTimeSinceLastSeen(),
                            curMood=self.lastKnownMood)

    def __handleMoodSet(self, component, value):
        # THIS IS ONLY TO BE USED BY THE MOOD SET HANDLERS
        # see requiredMoodComponents comment in __init__
        #print "Doid: %s Comp: %s Value: %s" % (self.doId, component, value)
        if self.isGenerated():
            self.mood.setComponent(component, value)
        else:
            self.requiredMoodComponents[component] = value

    def __generateDistMoodFuncs(self):
        # generate a get, b_set, d_set, and set func for each mood component
        for compName in PetMood.PetMood.Components:
            setterName = self.getSetterName(compName)
            def moodSetter(value, self=self, compName=compName):
                self.__handleMoodSet(compName, value)
            # put the func onto self
            self.__dict__[setterName] = moodSetter
            self.__funcsToDelete.append(setterName)

    def setMood(self, *componentValues):
        for value, name in zip(componentValues, PetMood.PetMood.Components):
            setterName = self.getSetterName(name)
            self.__dict__[setterName](value)

    def announceGenerate(self):
        # don't use the trait values from the DB, this should circumvent
        # the corrupted doodle problem
        DistributedObject.DistributedObject.announceGenerate(self)
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone)
        print self.traits.traits
        """
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone,
                                          traitValueList=self.traitList)
                                          """

        # create our mood manager. we need to have self.traits first.
        self.mood = PetMood.PetMood(self)
        self.lastKnownMood = self.mood.makeCopy()

        # pass in the cached required mood component values
        for mood, value in self.requiredMoodComponents.items():
            self.mood.setComponent(mood, value, announce=0)
        self.requiredMoodComponents = {}

        DistributedPetProxy.notify.debug(
            'time since last seen: %s' % self.getTimeSinceLastSeen())

        self.style = [self.head,
                      self.ears,
                      self.nose,
                      self.tail,
                      self.bodyTexture,
                      self.color,
                      self.colorScale,
                      self.eyeColor,
                      self.gender,
                      ]

        self.setLastSeenTimestamp(self.lastSeenTimestamp)
        self.updateOfflineMood()

        # Throw the event that pet info is available
        #proxyGenerateMessage = "petProxy-%d-generated" % self.doId
        #messenger.send(proxyGenerateMessage)
        self.sendGenerateMessage = 1

    def disable(self):
        if hasattr(self, 'lastKnownMood'):
            self.lastKnownMood.destroy()
            del self.lastKnownMood
        self.mood.destroy()
        del self.mood
        del self.traits

        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        for funcName in self.__funcsToDelete:
            del self.__dict__[funcName]
        DistributedObject.DistributedObject.delete(self)

    def setDominantMood(self, dominantMood):
        self.dominantMood = dominantMood
        # Throw the event that pet info is available
        if self.sendGenerateMessage == 1:
            proxyGenerateMessage = "petProxy-%d-generated" % self.doId
            messenger.send(proxyGenerateMessage)
            self.sendGenerateMessage = 0

    def getDominantMood(self):
        # there are situations where this is being called by PetAvatarPanel
        # before we're fully generated. Not a big deal if the panel erroneously
        # shows the pet as neutral
        #if not hasattr(self, 'mood'):
        #    return PetMood.PetMood.Neutral
        #return self.mood.getDominantMood()
        return self.dominantMood

    def setTrickAptitudes(self, aptitudes):
        self.trickAptitudes = aptitudes

    def isPet(self):
        return True

    def isProxy(self):
        return True

