from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.showbase.PythonUtil import lerp, average, clampScalar
from toontown.toonbase import TTLocalizer
import random, time, weakref

class PetMood:
    """Representation of the mood of a pet. Simulates changes in mood over
    time.
    Can run its own task, or can be hand-cranked.
    Announces when mood has changed.
    You may read components at any time as mood.component.
    When setting components, use mood.setComponent('compName', value); this
    allows the PetMood to announce the change. You could also set a bunch of
    components directly, followed by a call to mood.announceChange()
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("PetMood")

    Neutral = 'neutral'
    # later components have precedence as the dominant mood, all else
    # being equal.
    # TODO: add 'happiness' component?
    # ** Fatigue should come after all positive moods, so that it doesn't
    # get covered up by any of them when training your pet.
    # IF THIS LIST CHANGES, UPDATE DISTRIBUTEDPET.SETMOOD IN TOON.DC
    Components = ('boredom', 'restlessness', 'playfulness', 'loneliness',
                  'sadness', 'affection', 'hunger', 'confusion', 'excitement',
                  'fatigue', 'anger', 'surprise',)
    SerialNum = 0

    # these are the moods in which the pet is basically happy
    ContentedMoods = ('neutral', 'excitement', 'playfulness', 'affection')

    # these are the moods in which the pet is excited
    ExcitedMoods = ('excitement', 'playfulness')
    # these are the moods in which the pet is unhappy
    UnhappyMoods = ('boredom', 'restlessness', 'loneliness', 'sadness',
                    'fatigue', 'hunger', 'anger',)

    # these components will never be dominant
    # playfulness: icon is too confusing
    # TODO: add restlessness when there's somewhere else to go to
    DisabledDominants = ('restlessness', 'playfulness')
    # when active, these components will always override components that
    # appear earlier in the Components list
    AssertiveDominants = ('fatigue', )

    # there's a dictionary of mood adjectives in Localizer that needs to be
    # kept in sync
    assert len(TTLocalizer.PetMoodAdjectives) == (len(Components) + 1) # count neutral

    # for time values, below
    HOUR = 1.
    MINUTE = HOUR/60.
    DAY = 24. * HOUR
    WEEK = 7 * DAY
    LONGTIME = 5000 * WEEK

    # these represent how long it takes for a pet to go from the minimum
    # of each mood component to halfway to the maximum (or from the maximum
    # to the halfway point, depending on the component) in hours.
    # negative if component drifts down
    # Bear in mind that these represent the average time that it will take
    # for a pet to experience an emotion.
    TBoredom = 12 * HOUR
    TRestlessness = 18 * HOUR
    TPlayfulness = -1 * HOUR
    TLoneliness = 24 * HOUR
    TSadness = -1 * HOUR
    TFatigue = -15 * MINUTE
    THunger = 24 * HOUR
    TConfusion = -5 * MINUTE
    TExcitement = -5 * MINUTE
    TSurprise = -5 * MINUTE
    TAffection = -10 * MINUTE

    TAngerDec = -20 * MINUTE
    TAngerInc =  2 * WEEK

    def __init__(self, pet=None):
        self.setPet(pet)
        self.started = 0

        self.serialNum = PetMood.SerialNum
        PetMood.SerialNum += 1

        # initialize components to zero
        for comp in PetMood.Components:
            self.__dict__[comp] = 0.

        # Scale the time values for mood drifts based on tolerance threshold.
        # This exaggerates the effect of the thresholds.
        # Remember that we're calculating how long it will take for the
        # mood component to reach .5
        #
        # TIME FROM FULLY-SATED TO HUNGRY
        # lowest-threshold TTC pet: ~9 hours
        # median-threshold TTC pet: ~24 hours
        # median-threshold  DL pet: ~18 days
        # highest-threshold DL pet: ~28 days
        #
        # pass in True for fastDecay to indicate that it's better for this
        # mood component to drift quickly
        def calcDrift(baseT, trait, fasterDriftIsBetter=False):
            value = trait.percentile
            if not trait.higherIsBetter:
                # this is a trait where lower thresholds are better than
                # higher. Invert the threshold.
                value = 1. - value
            if fasterDriftIsBetter:
                # factor in [2.,.1]
                if value < .5:
                    factor = lerp(2., 1., value*2.)
                else:
                    # Put it on a squared curve
                    rebased = (value-.5)*2.
                    factor = lerp(1., .1, rebased*rebased)
            else:
                # factor in [.75,28]
                if value < .5:
                    factor = lerp(.75, 1., value*2.)
                else:
                    # we want hunger to stretch out to 4 weeks for top-of-the-line
                    # pets, thus 28. Also put it on a squared curve
                    rebased = (value-.5)*2.
                    factor = lerp(1., 28., rebased*rebased)
            return baseT * factor

        pet = self.getPet()
        self.tBoredom      = calcDrift(PetMood.TBoredom, pet.traits.traits['boredomThreshold'])
        self.tRestlessness = calcDrift(PetMood.TRestlessness, pet.traits.traits['restlessnessThreshold'])
        self.tPlayfulness  = calcDrift(PetMood.TPlayfulness, pet.traits.traits['playfulnessThreshold'])
        self.tLoneliness   = calcDrift(PetMood.TLoneliness, pet.traits.traits['lonelinessThreshold'])
        self.tSadness      = calcDrift(PetMood.TSadness, pet.traits.traits['sadnessThreshold'], True)
        self.tFatigue      = calcDrift(PetMood.TFatigue, pet.traits.traits['fatigueThreshold'], True)
        self.tHunger       = calcDrift(PetMood.THunger, pet.traits.traits['hungerThreshold'])
        self.tConfusion    = calcDrift(PetMood.TConfusion, pet.traits.traits['confusionThreshold'], True)
        self.tExcitement   = calcDrift(PetMood.TExcitement, pet.traits.traits['excitementThreshold'])
        self.tSurprise     = calcDrift(PetMood.TSurprise, pet.traits.traits['surpriseThreshold'], True)
        self.tAffection    = calcDrift(PetMood.TAffection, pet.traits.traits['affectionThreshold'])
        self.tAngerDec     = calcDrift(PetMood.TAngerDec, pet.traits.traits['angerThreshold'], True)
        self.tAngerInc     = calcDrift(PetMood.TAngerInc, pet.traits.traits['angerThreshold'])

        self.dominantMood = PetMood.Neutral

    def destroy(self):
        self.stop()
        del self.petRef

    def setPet(self, pet):
        # prevent cyclical reference
        self.petRef = weakref.ref(pet)
    def getPet(self):
        pet = self.petRef()
        if pet is None:
            self.notify.error('pet has been deleted')
        return pet

    def getMoodDriftTaskName(self):
        return 'petMoodDrift-%s' % self.serialNum
    def getMoodChangeEvent(self):
        # passes list of changed mood components (or empty list)
        return 'petMoodChange-%s' % self.serialNum
    def getDominantMoodChangeEvent(self):
        # passes dominant mood component
        return 'petDominantMoodChange-%s' % self.serialNum

    def announceChange(self, components=[]):
        # pass in list of names of components that changed
        # empty list means any and/or all changed
        # since things have changed, delete any cached dominant component
        oldMood = self.dominantMood
        if hasattr(self, 'dominantMood'):
            del self.dominantMood
        newMood = self.getDominantMood()

        messenger.send(self.getMoodChangeEvent(), [components])
        if (newMood != oldMood):
            messenger.send(self.getDominantMoodChangeEvent(), [newMood])

    def getComponent(self, compName):
        assert(compName in PetMood.Components)
        return self.__dict__[compName]

    def setComponent(self, compName, value, announce=1):
        assert(compName in PetMood.Components)
        different = (self.__dict__[compName] != value)
        self.__dict__[compName] = value
        if announce and different:
            self.announceChange([compName])

    def _getComponentThreshold(self, compName):
        # look up the mood component's threshold on the pet trait object
        assert(compName in PetMood.Components)
        # Currently we rely on there being a threshold trait that matches
        # each mood component. We can easily do a remapping here to
        # match a component name to an arbitrary threshold name.
        threshName = compName+'Threshold'
        pet = self.getPet()
        assert(hasattr(pet.traits, threshName))
        return pet.traits.__dict__[threshName]

    def isComponentActive(self, compName):
        return (self.getComponent(compName) >=
                self._getComponentThreshold(compName))

    def anyActive(self, compNames):
        # returns non-zero if any component in compNames is active
        for comp in compNames:
            if self.isComponentActive(comp):
                return 1
        return 0

    def getDominantMood(self):
        # returns the component that is currently the most pressing.
        # if no component is active, defaults to neutral
        if hasattr(self, 'dominantMood'):
            return self.dominantMood

        #print "calculating dominant mood"
        # Calculate the most pressing component.
        # The lower the threshold, the more pressing it is if we've gone
        # over.
        dominantMood = PetMood.Neutral
        priority = 1.
        for comp in PetMood.Components:
            if comp in PetMood.DisabledDominants:
                continue
            value = self.getComponent(comp)
            #print "comp %s is %s" % (comp, value)
            pri = value / max(self._getComponentThreshold(comp), .01)
            if pri >= priority:
                dominantMood = comp
                priority = pri
            elif (comp in PetMood.AssertiveDominants) and (pri >= 1.):
                # this is an active assertive mood; keep it
                dominantMood = comp
                # leave the existing (higher) priority for subsequent
                # priorities to compare to; don't take this lower priority

        self.dominantMood = dominantMood
        return dominantMood

    def makeCopy(self):
        # create a duplicate of this mood as it is right now
        #print "copying mood"
        other = PetMood(self.getPet())
        for comp in PetMood.Components:
            #print "%s is %s" %(comp, self.__dict__[comp])
            other.__dict__[comp] = self.__dict__[comp]
        return other

    # This kicks off a task to periodically update the mood. As currently
    # designed, this should only be used by the AI.
    def start(self):
        # make up for lost time
        pet = self.getPet()
        taskMgr.doMethodLater(
            (simbase.petMoodDriftPeriod / simbase.petMoodTimescale) * random.random(),
            self._driftMoodTask, self.getMoodDriftTaskName())
        self.started = 1

    def stop(self):
        if not self.started:
            return
        self.started = 0
        taskMgr.remove(self.getMoodDriftTaskName())

    def driftMood(self, dt=None, curMood=None):
        # Pass in a dt to simulate mood over a specific amount of time.
        # If dt not passed in, simulates based on time elapsed since last call.
        # Typical call pattern:
        # driftMood(timeSinceLastSeen)
        # driftMood()
        # driftMood()
        # ...
        #
        # If you want to calculate mood drift using another PetMood as the
        # starting point, pass it in as curMood. This is the recommended
        # method for simulating mood on the client, where the results are
        # not being stored in the database:
        # driftMood(timeSinceLastSeen(), lastMood)
        # ...
        # driftMood(timeSinceLastSeen(), lastMood)
        # ...
        # driftMood(timeSinceLastSeen(), lastMood)
        #
        # The resulting mood will match the mood calculated by the AI
        # (using the first method, above) when the pet comes into existence

        # TODO: add variation to this. Over long dt's, add in a sine wave,
        # some random noise, etc.

        #print "dt is %s" % dt
        now = globalClock.getFrameTime()
        if not hasattr(self, 'lastDriftTime'):
            self.lastDriftTime = now
        if dt is None:
            dt = now - self.lastDriftTime
        self.lastDriftTime = now
        
        if dt <= 0.:
            return

        if __debug__:
            try:
                dt *= simbase.petMoodTimescale
            except:
                pass

        if curMood is None:
            curMood = self

        # linear motion, for now
        def doDrift(curValue, timeToMedian, dt=float(dt)):
            # mood = mood + secs/((hrs/2*(mood/2))*(secs/hr))
            """ use this to make sure that the numbers are even moving
            print curValue - (curValue + dt/(timeToMedian*7200))
            """
            newValue = curValue + dt/(timeToMedian*7200)#3600)#60*60)
            return clampScalar(newValue, 0., 1.)
        self.boredom      = doDrift(curMood.boredom, self.tBoredom)
        # these are currently never used
        #self.restlessness = doDrift(curMood.restlessness, self.tRestlessness)
        #self.playfulness  = doDrift(curMood.playfulness, self.tPlayfulness)
        self.loneliness   = doDrift(curMood.loneliness, self.tLoneliness)
        self.sadness      = doDrift(curMood.sadness, self.tSadness)
        self.fatigue      = doDrift(curMood.fatigue, self.tFatigue)
        self.hunger       = doDrift(curMood.hunger, self.tHunger)
        self.confusion    = doDrift(curMood.confusion, self.tConfusion)
        self.excitement   = doDrift(curMood.excitement, self.tExcitement)
        self.surprise     = doDrift(curMood.surprise, self.tSurprise)
        self.affection    = doDrift(curMood.affection, self.tAffection)

        # for the sake of long-haul calculations, do the feedback calcs
        # after the simple independent calcs
        abuse = average(curMood.hunger, curMood.hunger, curMood.hunger,
                        curMood.boredom, curMood.loneliness)
        tipPoint = .6
        if abuse < tipPoint:
            tAnger = lerp(self.tAngerDec, -PetMood.LONGTIME,
                          abuse/tipPoint)
        else:
            tAnger = lerp(PetMood.LONGTIME, self.tAngerInc,
                          (abuse-tipPoint)/(1.-tipPoint))
        self.anger = doDrift(curMood.anger, tAnger)

        self.announceChange()

    def _driftMoodTask(self, task=None):
        self.driftMood()

        # schedule the next drift
        taskMgr.doMethodLater(
            simbase.petMoodDriftPeriod / simbase.petMoodTimescale,
            self._driftMoodTask,
            self.getMoodDriftTaskName())
        return Task.done

    def __repr__(self):
        s = '%s' % self.__class__.__name__
        for comp in PetMood.Components:
            s += '\n %s: %s' % (comp, self.__dict__[comp])
        return s

    if __debug__:
        def max(self):
            for comp in PetMood.Components:
                self.__dict__[comp] = 1.
            self.announceChange()
        def min(self):
            for comp in PetMood.Components:
                self.__dict__[comp] = 0.
            self.announceChange()
