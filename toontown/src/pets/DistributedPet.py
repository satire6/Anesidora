"""DistributedPet module: contains the DistributedPet class"""

from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.MsgTypes import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from toontown.pets import Pet, PetBase, PetTraits, PetConstants, PetManager, PetAvatarPanel
from toontown.pets import PetMood, PetTricks
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.distributed import DelayDelete
from toontown.distributed.DelayDeletable import DelayDeletable
import random

if __dev__:
    # import pdb def
    import pdb

BeanColors = (
        VBase4(1.0, 0.2, 0.2, 1.0), # red
        VBase4(0.2, 1.0, 0.2, 1.0), # green
        VBase4(0.2, 0.2, 1.0, 1.0), # blue
        VBase4(0.0, 1.0, 1.0, 1.0), # light blue
        # VBase4(1.0, 0.6, 0.1, 1.0), # orange
        VBase4(1.0, 1.0, 0.0, 1.0), # yellow
        VBase4(1.0, 0.6, 1.0, 1.0), # pink
        VBase4(0.6, 0.0, 0.6, 1.0), # purple
        )

class DistributedPet(DistributedSmoothNode.DistributedSmoothNode,
                     Pet.Pet, PetBase.PetBase, DelayDeletable):
    """client-side implementation of Toon pet"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPet")
    swallowSfx = None
    callSfx = None
    petSfx = None

    def __init__(self, cr, bFake = False):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        Pet.Pet.__init__(self)
        self.bFake = bFake
        self.isLocalToon = 0
        self.inWater = 0
        # create our distributed trait and mood funcs
        self.__funcsToDelete = []
        self.__generateDistTraitFuncs()
        self.__generateDistMoodFuncs()

        self.trickAptitudes = []
        self.avDelayDelete = None

    def generate(self):
        DistributedPet.notify.debug('generate(), fake=%s' % self.bFake)
        if not self.bFake:
            PetManager.acquirePetManager()
        DistributedSmoothNode.DistributedSmoothNode.generate(self)
        self.trickIval = None
        self.movieTrack = None

        # this will be filled in during generation
        self.traitList = [0] * PetTraits.PetTraits.NumTraits



        # cache required mood components until we have a self.mood to give
        # them to
        self.requiredMoodComponents = {}

    def b_setLocation(self, parentId, zoneId):
        if not self.bFake:
            DistributedSmoothNode.DistributedSmoothNode.b_setLocation(self, parentId, zoneId)
    def d_setLocation(self, parentId, zoneId):
        if not self.bFake:
            DistributedSmoothNode.DistributedSmoothNode.d_setLocation(self, parentId, zoneId)
    def setLocation(self, parentId, zoneId):
        if not self.bFake:
            DistributedSmoothNode.DistributedSmoothNode.setLocation(self, parentId, zoneId)

    # debug OSD display
    def getDisplayPrefix(self):
        return 'pet%s' % self.doId
    def display(self, key, value, category=''):
        if self.bFake:
            return 1

        if len(category) > 0:
            category = '-' + category
        onScreenDebug.add('%s%s-%s' % (self.getDisplayPrefix(),
                                       category, key), value)
        return 1
    def clearDisplay(self):
        onScreenDebug.removeAllWithPrefix(self.getDisplayPrefix())
        return 1

    def moodComponentChanged(self, components=[]):
        # update the on-screen debug display
        if len(components) == 0:
            components = PetMood.PetMood.Components
        for comp in components:
            self.display(comp, self.mood.getComponent(comp), 'mood')

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getOwnerId(self):
        return self.ownerId

    def setPetName(self, petName):
        self.petName = petName
        # set the nodepath name, for kicks
        DistributedSmoothNode.DistributedSmoothNode.setName(self, self.petName)
        # make sure the pet's nametag is up-to-date
        if self.isGenerated():
            # unqualified self.setName was resolving to NodePath.setName
            Pet.Pet.setName(self, self.petName)

        messenger.send("petNameChanged", [self])

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
        DistributedPet.notify.debug('setHead: %s' % head)
        self.head = head

    def setEars(self, ears):
        DistributedPet.notify.debug('setEars: %s' % ears)
        self.ears = ears

    def setNose(self, nose):
        DistributedPet.notify.debug('setNose: %s' % nose)
        self.nose = nose

    def setTail(self, tail):
        DistributedPet.notify.debug('setTail: %s' % tail)
        self.tail = tail

    def setBodyTexture(self, bodyTexture):
        DistributedPet.notify.debug('setBodyTexture: %s' % bodyTexture)
        self.bodyTexture = bodyTexture

    def setColor(self, color):
        DistributedPet.notify.debug('setColor: %s' % color)
        self.color = color

    def setColorScale(self, colorScale):
        DistributedPet.notify.debug('setColorScale: %s' % colorScale)
        self.colorScale = colorScale

    def setEyeColor(self, eyeColor):
        DistributedPet.notify.debug('setEyeColor: %s' % eyeColor)
        self.eyeColor = eyeColor

    def setGender(self, gender):
        DistributedPet.notify.debug('setGender: %s' % gender)
        self.gender = gender

    def setLastSeenTimestamp(self, timestamp):
        DistributedPet.notify.debug('setLastSeenTimestamp: %s' % timestamp)
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
        assert(self.bFake)
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

    # setXXX func is generated for each mood component
    # this is one of the original functions:
    """
    def setHunger(self, hunger):
        self.__handleMoodSet('hunger', hunger)"""

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


    def doTrick(self, trickId, timestamp):
        if not self.isLockedDown():
            if self.trickIval is not None and self.trickIval.isPlaying():
                self.trickIval.finish()
            self.trickIval = PetTricks.getTrickIval(self, trickId)
            if trickId == PetTricks.Tricks.BALK:
                mood = self.getDominantMood()
                self.trickIval = Parallel(self.trickIval,
                                          Sequence(Func(self.handleMoodChange, 'confusion'),
                                                   Wait(1.),
                                                   Func(self.handleMoodChange, mood)
                                                   )
                                          )
            self.trickIval.start(globalClockDelta.localElapsedTime(timestamp))

    def getName(self):
        # call the correct getName
        return Pet.Pet.getName(self)

    def announceGenerate(self):
        DistributedPet.notify.debug('announceGenerate(), fake=%s' %
                                    self.bFake)
        DistributedSmoothNode.DistributedSmoothNode.announceGenerate(self)
        if hasattr(self, "petName"):
            Pet.Pet.setName(self, self.petName)

        # don't use the trait values from the DB, this should circumvent
        # the corrupted doodle problem
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone)
        """
        self.traits = PetTraits.PetTraits(self.traitSeed, self.safeZone,
                                          traitValueList=self.traitList)
                                          """

        # create our mood manager. we need to have self.traits first.
        self.mood = PetMood.PetMood(self)

        # pass in the cached required mood component values
        for mood, value in self.requiredMoodComponents.items():
            self.mood.setComponent(mood, value, announce=0)
        self.requiredMoodComponents = {}

        DistributedPet.notify.debug(
            'time since last seen: %s' % self.getTimeSinceLastSeen())

        self.setDNA([self.head,
                     self.ears,
                     self.nose,
                     self.tail,
                     self.bodyTexture,
                     self.color,
                     self.colorScale,
                     self.eyeColor,
                     self.gender,
                     ])

        # Locally store a copy of the pet's DNA on its owner, for
        # convenience.  Really this is just for the catalog system for
        # now, but maybe there will be other applications later.
        av = self.cr.doId2do.get(self.ownerId)
        if av:
            av.petDNA = self.style

        if self.bFake:
            # store a copy of the 'last known' mood state
            self.lastKnownMood = self.mood.makeCopy()
            # and calculate the current mood
            self.updateOfflineMood()
        else:
            self.__initCollisions()
            self.startSmooth()
            self.setActiveShadow(1)

        # make sure the nametag is up-to-date
        self.setPetName(self.petName)
        if not self.bFake:
            self.addActive()

            # start the blink task again because disable stops it
            self.startBlink()

            # only load the sounds for 'real' pets
            if not self.swallowSfx:
                self.swallowSfx = loader.loadSfx('phase_5.5/audio/sfx/beg_eat_swallow.mp3')
            if not self.callSfx:
                self.callSfx = loader.loadSfx('phase_5.5/audio/sfx/call_pet.mp3')
            if not self.petSfx:
                self.petSfx = loader.loadSfx('phase_5.5/audio/sfx/pet_the_pet.mp3')

            # kick-start the emote display
            self.handleMoodChange()
            # and listen for changes
            self.accept(self.mood.getDominantMoodChangeEvent(), self.handleMoodChange)
            # listen for every mood change for debug display
            self.accept(self.mood.getMoodChangeEvent(),
                        self.moodComponentChanged)

    def disable(self):
        DistributedPet.notify.debug('disable(), fake=%s' % self.bFake)
        # free local avatar
        if (self.isLocalToon):
            base.localAvatar.enableSmartCameraViews()
            self.freeAvatar()

        self.ignore(self.mood.getDominantMoodChangeEvent())
        self.ignore(self.mood.getMoodChangeEvent())
        if hasattr(self, 'lastKnownMood'):
            self.lastKnownMood.destroy()
            del self.lastKnownMood
        self.mood.destroy()
        del self.mood
        del self.traits
        self.removeActive()
        if not self.bFake:
            self.stopSmooth()
            self.__cleanupCollisions()
            # stop all animations on disabled pets
            self.stopAnimations()
            # if we're localAv's pet, mark our mood as 'dirty' so that the pet
            # panel will re-query and not use old cached info
            if self.doId == localAvatar.getPetId():
                bboard.post(PetConstants.OurPetsMoodChangedKey, True)
        # clean up any trick movie state
        taskMgr.remove(self.uniqueName('lerpCamera'))
        self.clearDisplay()
        DistributedSmoothNode.DistributedSmoothNode.disable(self)

    def delete(self):
        DistributedPet.notify.debug('delete(), fake=%s' % self.bFake)
        if self.trickIval is not None:
            self.trickIval.finish()
            del self.trickIval

        if self.movieTrack is not None:
            self.movieTrack.finish()
            del self.movieTrack

        # Precaution in case we are in a movie.
        taskMgr.remove(self.uniqueName('Pet-Movie-%s' %self.getDoId()))
        self.clearMovie()

        for funcName in self.__funcsToDelete:
            del self.__dict__[funcName]

        Pet.Pet.delete(self)
        DistributedSmoothNode.DistributedSmoothNode.delete(self)
        if not self.bFake:
            PetManager.releasePetManager()

    def __initCollisions(self):
        # This is a ray cast down to detect floor polygons
        cRay = CollisionRay(0.0, 0.0, 40000.0, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('pet-cRayNode-%s' % self.doId)
        cRayNode.addSolid(cRay)
        cRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.cRayNodePath = self.attachNewNode(cRayNode)

        # set up floor collision mechanism
        self.lifter = CollisionHandlerFloor()
        self.lifter.setInPattern("enter%in")
        self.lifter.setOutPattern("exit%in")
        self.lifter.setOffset(OTPGlobals.FloorOffset)
        # This is how high the pet will reach up to another floor
        # polygon:
        self.lifter.setReach(4.0)
        self.lifter.addCollider(self.cRayNodePath, self)

        # hook into the petManager's collision traverser
        self.cTrav = base.petManager.cTrav
        self.cTrav.addCollider(self.cRayNodePath, self.lifter)

        # check for water after the global collision traversal
        taskMgr.add(self._detectWater, self.getDetectWaterTaskName(),
                    priority=32)

        self.initializeBodyCollisions('pet-%s' % self.doId)

    def __cleanupCollisions(self):
        self.disableBodyCollisions()
        taskMgr.remove(self.getDetectWaterTaskName())
        self.cTrav.removeCollider(self.cRayNodePath)
        del self.cTrav
        self.cRayNodePath.removeNode()
        del self.cRayNodePath
        del self.lifter

    def lockPet(self):
        # call this when you need to lock the pet down in order to play
        # a movie on him
        if not self.lockedDown:
            self.prevAnimState = self.animFSM.getCurrentState().getName()
            # if the movie doesn't do anything, the pet is going to stop moving.
            # put him in neutral
            self.animFSM.request('neutral')
        self.lockedDown += 1

    def isLockedDown(self):
        return self.lockedDown != 0

    def unlockPet(self):
        if self.lockedDown <= 0:
            DistributedPet.notify.warning(
                '%s: unlockPet called on unlockedPet' % self.doId)
        else:
            # call this when you're done playing the movie
            self.lockedDown -= 1
            if not self.lockedDown:
                # make sure the pet is playing the same animation that it was
                # playing when we locked it down
                self.animFSM.request(self.prevAnimState)
                self.prevAnimState = None

    # this is called every frame by the smoothing task
    def smoothPosition(self):
        DistributedSmoothNode.DistributedSmoothNode.smoothPosition(self)
        if not self.lockedDown:
            self.trackAnimToSpeed(self.smoother.getSmoothForwardVelocity(),
                                  self.smoother.getSmoothRotationalVelocity())

    def getDetectWaterTaskName(self):
        return self.uniqueName('detectWater')

    def _detectWater(self, task):
        # this uses localToon's zone info to look up water info
        showWake, wakeWaterHeight = ZoneUtil.getWakeInfo()
        # if showWake is false, don't check for water, there's none around
        self.inWater = 0
        if showWake:
            if self.getZ() <= wakeWaterHeight:
                self.setZ(wakeWaterHeight - PetConstants.SubmergeDistance)
                self.inWater = 1
        return Task.cont

    # override funcs in Pet.py
    def isInWater(self):
        return self.inWater
    def isExcited(self):
        return PetBase.PetBase.isExcited(self)
    def isSad(self):
        return PetBase.PetBase.isSad(self)

    def handleMoodChange(self, mood=None):
        # Normally this is called with the new dominant mood. If not passed in,
        # just query for the dominant mood.
        if mood is None:
            mood = self.mood.getDominantMood()
        # for now, display the pet's mood in a thought balloon
        if mood == PetMood.PetMood.Neutral:
            self.clearChat()
            self.clearMood()
        else:
            #self.setChatAbsolute(TTLocalizer.PetMoodAdjectives[mood], CFThought)
            self.showMood(mood)
        messenger.send('petStateUpdated', [self])

    def getDominantMood(self):
        # there are situations where this is being called by PetAvatarPanel
        # before we're fully generated. Not a big deal if the panel erroneously
        # shows the pet as neutral
        if not hasattr(self, 'mood'):
            return PetMood.PetMood.Neutral
        return self.mood.getDominantMood()

    def getRequestID(self):
        return CLIENT_GET_PET_DETAILS

    def teleportIn(self, timestamp):
        self.lockPet()
        self.animFSM.request("teleportIn", [timestamp])
        self.unlockPet()

    def teleportOut(self, timestamp):
        self.lockPet()
        self.animFSM.request("teleportOut", [timestamp])
        self.unlockPet()

    #
    # pet movie methods
    #

    def avatarInteract(self, avId):
        # Lock down the avatar and prepare to play trick movie
        assert(self.notify.debug("Entering movie mode"))
        place = base.cr.playGame.getPlace()
        place.setState('pet')
        #base.localAvatar.startUpdateSmartCamera()
        base.localAvatar.disableSmartCameraViews()

    def freeAvatar(self):
        # This is a message from the AI used to free the avatar from movie mode
        place = base.cr.playGame.getPlace()
        if place:
            place.setState("walk")
        base.localAvatar.unlock()
        messenger.send('pet-interaction-done')

    def setUpMovieAvatar(self, av):
        # Assign the av pointer and prevent the av from being deleted
        # while it is assigned here.
        self.avDelayDelete = DelayDelete.DelayDelete(av, 'Pet.setUpMovieAvatar')

        # Prepare the avatar for the trick movie
        av.headsUp(self, 0, 0, 0)
        av.stopLookAround()
        #av.lerpLookAt(self.getPos(), time=0.5)

    def holdPetDownForMovie(self):
        # used to be in setUpMovieAvatar but not wanted for call movie
        self.lockPet()
        self.stopSmooth()

    def releasePetFromHoldDown(self):
        # used to be in resetAvatarAndPet but not wanted for call movie
        self.unlockPet()
        self.startSmooth()

    def clearMovieAvatar(self):
        # Allow the avatar that was assigned during the movie to be deleted.
        if self.avDelayDelete:
            self.avDelayDelete.destroy()
            self.avDelayDelete = None

    def clearMovie(self):
        # Reset the pet after trick movie
        assert(self.notify.debug('clearMovie'))
        self.clearMovieAvatar()
        return Task.done

    def resetAvatarAndPet(self, task=None):
        # return to original pos hpr
        #self.clearMat()
        # free local avatar
        if (self.isLocalToon):
            base.localAvatar.enableSmartCameraViews()
            # turn away from the pet so we can see him
            base.localAvatar.setH(base.localAvatar, 30)
            self.freeAvatar()
            self.isLocalToon = 0

        return Task.done

    def _petMovieStart(self, av):
        assert(self.notify.debug('PET_MOVIE_START'))

        if not self.isLocalToon:
            av.stopSmooth()

        self.setUpMovieAvatar(av)

        # if this is the localtoon, lerp the camera
        if (self.isLocalToon):
            base.localAvatar.setCameraPosForPetInteraction()
            base.localAvatar.lock()

    def _getPetMovieCompleteIval(self, av):
        def _petMovieComplete(self=self):
            assert(self.notify.debug('PET_MOVIE_COMPLETE'))
            if self.isLocalToon:
                base.localAvatar.unsetCameraPosForPetInteraction()
            else:
                av.startSmooth()

        return Sequence(
            Func(_petMovieComplete),
            Wait(.8),
            Func(self.resetAvatarAndPet),
            )

    def setMovie(self, mode, avId, timestamp):
        # This is a message from the AI describing a movie between this pet
        # and a Toon that has entered trick mode with us.

        timeStamp = globalClockDelta.localElapsedTime(timestamp)

        # if we need to stop a currently-playing movie ival, do it before
        # we set self.isLocalToon. Otherwise we may crash in
        # LocalAvatar.unsetCameraPosForPetInteraction -- the movie will not
        # be able to clean up correctly wrt localToon/not localToon
        if mode in (PetConstants.PET_MOVIE_CALL,
                    PetConstants.PET_MOVIE_SCRATCH,
                    PetConstants.PET_MOVIE_FEED):
            if self.movieTrack is not None and self.movieTrack.isPlaying():
                self.movieTrack.finish()

        if (avId != 0):
            self.isLocalToon = (avId == base.localAvatar.doId)
            av = base.cr.doId2do.get(avId)
            if av is None:
                self.notify.warning("Avatar %d not found in doId" % (avId))
                return

        assert(self.notify.debug("setMovie: %s %s %s %s" %
                                 (mode, avId, timeStamp, self.isLocalToon)))

        # old movie has been cleared
        if (mode == PetConstants.PET_MOVIE_CLEAR):
            assert(self.notify.debug('PET_MOVIE_CLEAR'))
            self.clearMovie()
            return

        if (mode == PetConstants.PET_MOVIE_CALL):
            assert(self.notify.debug('PET_MOVIE_CALL'))
            try:
                self.movieTrack = Sequence(
                    Func(self._petMovieStart, av),
                    Parallel( av.getCallPetIval(),
                              Sequence(Wait(.54),
                                       SoundInterval(self.callSfx)
                                       )
                              ),
                    self._getPetMovieCompleteIval(av),
                    )
                self.movieTrack.start()
            except StandardError, error:
                print str(error)

        if (mode == PetConstants.PET_MOVIE_SCRATCH):
            assert(self.notify.debug('PET_MOVIE_SCRATCH'))
            try:
                self.movieTrack = Sequence(
                    Func(self._petMovieStart, av),
                    Func(self.holdPetDownForMovie),
                    Parallel( self.getInteractIval(self.Interactions.SCRATCH),
                              av.getScratchPetIval(),
                              SoundInterval(self.petSfx)
                              ),
                    Func(self.releasePetFromHoldDown),
                    self._getPetMovieCompleteIval(av),
                    )
                self.movieTrack.start()
            except StandardError, error:
                print str(error)

        if (mode == PetConstants.PET_MOVIE_FEED):
            assert(self.notify.debug('PET_MOVIE_FEED'))
            # the jellybean has already been taken
            #assert(av.getTotalMoney() >= PetConstants.FEED_AMOUNT)

            # Load the Jellybean
            self.bean = loader.loadModel("phase_4/models/props/jellybean4")
            bean = self.bean.find("**/jellybean")
            bean.setColor(random.choice(BeanColors))
            self.movieTrack = Sequence(
                Func(self._petMovieStart, av),
                Func(self.holdPetDownForMovie),
                Parallel(Func(base.playSfx, self.swallowSfx,
                              0, 1, 1, 2.5, self.bean),
                         Sequence( ActorInterval(self, "toBeg"),
                                   ActorInterval(self, "beg"),
                                   ActorInterval(self, "fromBeg"),
                                   ActorInterval(self, "eat"),
                                   ActorInterval(self, "swallow"),
                                   Func(self.loop, "neutral"),
                                   ),
                         # self.getInteractIval(self.Interactions.BEG),
                         Sequence( Wait(0.3),
                                   ActorInterval(av, "feedPet"),
                                   Func(av.animFSM.request, "neutral")),
                         # av.getFeedPetIval(),
                         Sequence( Wait(0.3),
                                   Func(self.bean.reparentTo, av.rightHand),
                                   Func(self.bean.setPos, .1, 0., .2),
                                   Wait(2.1),
                                   # Make sure all LODs are up to date before
                                   # parenting the bean to render
                                   Func(av.update, 0),
                                   Func(av.update, 1),
                                   Func(av.update, 2),
                                   Func(self.bean.wrtReparentTo, render),
                                   Parallel(
                LerpHprInterval(self.bean,
                                hpr = Point3(random.random() * 360. * 2,
                                             random.random() * 360. * 2,
                                             random.random() * 360. * 2,),
                                duration = 1.2),
                ProjectileInterval(self.bean,
                                   endPos = self.find("**/joint_tongueBase").getPos(render),
                                   duration = 1.2,
                                   gravityMult = 0.45),
                ),
                                   Func(self.bean.removeNode),
                                   # self.getInteractIval(self.Interactions.EAT)
                                   ),
                         ),
                Func(self.releasePetFromHoldDown),
                self._getPetMovieCompleteIval(av),
                )
            self.movieTrack.start()
        return

    def setTrickAptitudes(self, aptitudes):
        self.trickAptitudes = aptitudes
