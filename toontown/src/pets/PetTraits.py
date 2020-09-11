from direct.showbase.PythonUtil import randFloat, normalDistrib, Enum
from direct.showbase.PythonUtil import clampScalar
from toontown.toonbase import TTLocalizer, ToontownGlobals
import random, copy

# this should match the DC
TraitDivisor = 10000

def getTraitNames():
    if not hasattr(PetTraits, 'TraitNames'):
        # returns ordered list of trait names
        traitNames = []
        for desc in PetTraits.TraitDescs:
            traitNames.append(desc[0])
            PetTraits.TraitNames = traitNames

    return PetTraits.TraitNames

# some standard random distribution functions
def uniform(min, max, rng):
    return randFloat(min, max, rng.random)
def gaussian(min, max, rng):
    return normalDistrib(min, max, rng.gauss)

class TraitDistribution:
    # TraitDistributions describe a distribution from which to generate a
    # trait value. Traits are in [0..1]

    # these are classifications for pet traits
    TraitQuality = Enum('VERY_BAD, BAD, AVERAGE, GOOD, VERY_GOOD')
    # INCREASING means higher value is better
    TraitTypes = Enum('INCREASING, DECREASING')

    # subclasses should set this to a table of szId: (min, max)
    Sz2MinMax = None
    # subclasses should set this to a TraitTypes value
    TraitType = None

    TraitCutoffs = {
        TraitTypes.INCREASING: {TraitQuality.VERY_BAD:  .10,
                                TraitQuality.BAD:       .25,
                                TraitQuality.GOOD:      .75,
                                TraitQuality.VERY_GOOD: .90},
        TraitTypes.DECREASING: {TraitQuality.VERY_BAD:  .90,
                                TraitQuality.BAD:       .75,
                                TraitQuality.GOOD:      .25,
                                TraitQuality.VERY_GOOD: .10},
        }

    def __init__(self, rndFunc=gaussian):
        # randFunc should return in 0..1
        self.rndFunc = rndFunc
        # calculate the lowest and highest trait values
        if not hasattr(self.__class__, 'GlobalMinMax'):
            # don't cover up global min and max funcs
            _min = 1.; _max = 0.
            minMax = self.Sz2MinMax
            for sz in minMax:
                thisMin, thisMax = minMax[sz]
                _min = min(_min, thisMin)
                _max = max(_max, thisMax)
            self.__class__.GlobalMinMax = [_min, _max]

    def getRandValue(self, szId, rng=random):
        min, max = self.getMinMax(szId)
        return self.rndFunc(min, max, rng)

    def getHigherIsBetter(self):
        return self.TraitType == TraitDistribution.TraitTypes.INCREASING

    def getMinMax(self, szId):
        # returns min, max trait values for a given safezone
        return self.Sz2MinMax[szId][0], self.Sz2MinMax[szId][1]
    def getGlobalMinMax(self):
        # returns overall min and max trait values for all safezones
        return self.GlobalMinMax[0], self.GlobalMinMax[1]

    def _getTraitPercent(self, traitValue):
        # internal function, returns value in [0,1] representing the
        # value in relation to the distribution's min and max values
        gMin, gMax = self.getGlobalMinMax()
        # if the min and max have been pulled in tighter since this
        # pet was stored in the database, fudge the numbers
        if traitValue < gMin:
            gMin = traitValue
        elif traitValue > gMax:
            gMax = traitValue
        return (traitValue - gMin) / (gMax - gMin)

    def getPercentile(self, traitValue):
        # returns value in [0,1] representing the value in relation
        # to the distribution's range. 0 is least desirable, 1
        # is most desirable.
        if self.TraitType is TraitDistribution.TraitTypes.INCREASING:
            return self._getTraitPercent(traitValue)
        else:
            return 1. - self._getTraitPercent(traitValue)

    def getQuality(self, traitValue):
        # returns TraitQuality enum given a particular trait value
        TraitQuality = TraitDistribution.TraitQuality
        TraitCutoffs = self.TraitCutoffs[self.TraitType]
        percent = self._getTraitPercent(traitValue)
        if self.TraitType is TraitDistribution.TraitTypes.INCREASING:
            if percent <= TraitCutoffs[TraitQuality.VERY_BAD]:
                return TraitQuality.VERY_BAD
            elif percent <= TraitCutoffs[TraitQuality.BAD]:
                return TraitQuality.BAD
            elif percent >= TraitCutoffs[TraitQuality.VERY_GOOD]:
                return TraitQuality.VERY_GOOD
            elif percent >= TraitCutoffs[TraitQuality.GOOD]:
                return TraitQuality.GOOD
            else:
                return TraitQuality.AVERAGE
        else:
            if percent <= TraitCutoffs[TraitQuality.VERY_GOOD]:
                return TraitQuality.VERY_GOOD
            elif percent <= TraitCutoffs[TraitQuality.GOOD]:
                return TraitQuality.GOOD
            elif percent >= TraitCutoffs[TraitQuality.VERY_BAD]:
                return TraitQuality.VERY_BAD
            elif percent >= TraitCutoffs[TraitQuality.BAD]:
                return TraitQuality.BAD
            else:
                return TraitQuality.AVERAGE

    def getExtremeness(self, traitValue):
        # returns 'extremeness' value in [0..1] for a particular trait value
        percent = self._getTraitPercent(traitValue)
        if percent < .5:
            howExtreme = (.5 - percent) * 2.
        else:
            howExtreme = (percent - .5) * 2.
        return clampScalar(howExtreme, 0., 1.)

class PetTraits:
    """Describes static traits of a particular pet. Traits are accessible as
    traitsObj.traitName, more information is available in
    traitsObj.traits[traitName]"""

    # define some trait distributions
    class StdIncDistrib(TraitDistribution):
        # for typical traits that are better when they're higher
        TraitType = TraitDistribution.TraitTypes.INCREASING
        Sz2MinMax = {
            ToontownGlobals.ToontownCentral:   (.2, .65),
            ToontownGlobals.DonaldsDock:       (.3, .7),
            ToontownGlobals.DaisyGardens:      (.4, .75),
            ToontownGlobals.MinniesMelodyland: (.5, .8),
            ToontownGlobals.TheBrrrgh:         (.6, .85),
            ToontownGlobals.DonaldsDreamland:  (.7, .9),
            }

    class StdDecDistrib(TraitDistribution):
        # for typical traits that are better when they're lower
        TraitType = TraitDistribution.TraitTypes.DECREASING
        Sz2MinMax = {
            ToontownGlobals.ToontownCentral:   (.35, .8),
            ToontownGlobals.DonaldsDock:       (.3,  .7),
            ToontownGlobals.DaisyGardens:      (.25, .6),
            ToontownGlobals.MinniesMelodyland: (.2,  .5),
            ToontownGlobals.TheBrrrgh:         (.15, .4),
            ToontownGlobals.DonaldsDreamland:  (.1,  .3),
            }

    class ForgetfulnessDistrib(TraitDistribution):
        # for forgetfulness trait values
        TraitType = TraitDistribution.TraitTypes.DECREASING
        Sz2MinMax = {
            ToontownGlobals.ToontownCentral:   (0., 1.),
            ToontownGlobals.DonaldsDock:       (0., .9),
            ToontownGlobals.DaisyGardens:      (0., .8),
            ToontownGlobals.MinniesMelodyland: (0., .7),
            ToontownGlobals.TheBrrrgh:         (0., .6),
            ToontownGlobals.DonaldsDreamland:  (0., .5),
            }

    # ORDER IS VERY IMPORTANT
    # DON'T CHANGE THE ORDER OR INSERT NEW ITEMS ANYWHERE OTHER THAN
    # AT THE END UNLESS YOU'RE SURE YOU KNOW WHAT YOU'RE DOING
    # THESE ARE ALL VALUES IN [0..1]
    #
    # IF WE EVER ADD MORE TRAITS:
    # There is a bug in the way that the value of a pet's traits is
    # calculated; the value is the average of all the traits, but we add
    # up all the traits that have value and then divide by the number of
    # total traits, including those that do not contribute. This has the
    # effect of pulling the value of pet traits down, resulting in cheaper
    # pets. Fixing it pulls the prices back up.
    # This change should be made eventually, but it should happen at a time
    # when we make some other significant change to the pets. I've labeled
    # all of the required changes (commented out) with 'TRAITFIX'
    TraitDescs = (
        # traitName               distribution,            hasWorth),
        ('forgetfulness',         ForgetfulnessDistrib(),  True),
        ('boredomThreshold',      StdIncDistrib(),         True),
        ('restlessnessThreshold', StdIncDistrib(),         True),#False), # TRAITFIX
        ('playfulnessThreshold',  StdDecDistrib(),         True),#False), # TRAITFIX
        ('lonelinessThreshold',   StdIncDistrib(),         True),
        ('sadnessThreshold',      StdIncDistrib(),         True),
        ('fatigueThreshold',      StdIncDistrib(),         True),
        ('hungerThreshold',       StdIncDistrib(),         True),
        ('confusionThreshold',    StdIncDistrib(),         True),
        ('excitementThreshold',   StdDecDistrib(),         True),
        ('angerThreshold',        StdIncDistrib(),         True),
        ('surpriseThreshold',     StdIncDistrib(),         False),
        ('affectionThreshold',    StdDecDistrib(),         True),
        )

    NumTraits = len(TraitDescs)

    # This class acts as a container of attributes that describe a
    # particular trait.
    class Trait:
        def __init__(self, index, traitsObj, value=None):
            self.name, distrib, self.hasWorth = PetTraits.TraitDescs[index]
            # pass in value if we already have it and are not gen'ing it
            if value is not None:
                self.value = value
            else:
                szId = traitsObj.safeZoneId
                self.value = distrib.getRandValue(szId, traitsObj.rng)
                # preemptively quantize the traits to the values that
                # will be stored in the DB
                self.value = (int(self.value * TraitDivisor) /
                              float(TraitDivisor))

            # cache some constants so that we don't have to keep the
            # distribution object around
            self.higherIsBetter = distrib.getHigherIsBetter()
            self.percentile = distrib.getPercentile(self.value)
            self.quality = distrib.getQuality(self.value)
            self.howExtreme = distrib.getExtremeness(self.value)

        def __repr__(self):
            return ('Trait: %s, %s, %s, %s' % (
                self.name, self.value,
                TraitDistribution.TraitQuality.getString(self.quality),
                self.howExtreme))

    def __init__(self, traitSeed, safeZoneId, traitValueList=[]):
        # If you already know (some of) the traits, pass them in as
        # traitValueList. Newly-added traits for an existing pet should
        # have a value of zero; they will be assigned their correct
        # generated value.
        self.traitSeed = traitSeed
        self.safeZoneId = safeZoneId
        self.rng = random.Random(self.traitSeed)
        
        # create dictionary of trait name to Trait object
        self.traits = {}
        for i in xrange(len(PetTraits.TraitDescs)):
            # if we have a valid value for this trait...
            if i < len(traitValueList) and traitValueList[i] > 0.:
                # assign it directly
                trait = PetTraits.Trait(i, self, traitValueList[i])
            else:
                # otherwise, generate the trait value.
                trait = PetTraits.Trait(i, self)
            self.traits[trait.name] = trait
            # add a copy of the trait value on ourselves
            self.__dict__[trait.name] = trait.value
            
        # pre-calculate the extreme traits, ordered by... extremity-ness
        extremeTraits = []
        for trait in self.traits.values():
            if not trait.hasWorth:
                continue
            if trait.quality == TraitDistribution.TraitQuality.AVERAGE:
                continue
            i = 0
            while ((i < len(extremeTraits)) and
                   (extremeTraits[i].howExtreme > trait.howExtreme)):
                i += 1
            extremeTraits.insert(i, trait)
        if __debug__:
            # make sure it's decreasing
            if len(extremeTraits) > 1:
                for i in xrange(len(extremeTraits)-1):
                    assert (extremeTraits[i].howExtreme >=
                            extremeTraits[i+1].howExtreme)
        self.extremeTraits = []
        for trait in extremeTraits:
            self.extremeTraits.append((trait.name, trait.quality))

    def getValueList(self):
        # returns ordered list of trait values
        traitValues = []
        for desc in PetTraits.TraitDescs:
            traitName = desc[0]
            traitValues.append(self.traits[traitName].value)
        return traitValues

    def getTraitValue(self, traitName):
        return self.traits[traitName].value

    def getExtremeTraits(self):
        # returns list of (trait name, TraitQuality enum value)
        # traits are at (or near) either a low or high extreme
        # ordered from most extreme to least
        return copy.copy(self.extremeTraits)

    def getOverallValue(self):
        # returns the 'value' between 0(worthless) and 1(valuable) of a
        # pet's traits currently, just an average of all of the traits

        total = 0
        numUsed = 0
        for trait in self.traits.values():
            if trait.hasWorth:
                if trait.higherIsBetter:
                    value = trait.value
                else:
                    value = 1. - trait.value
                total += value
                numUsed += 1

        value = total / len(self.traits.values())
        """ TRAITFIX -- replace value calculation with:
        value = total / float(numUsed)
        """
        return value

    def getExtremeTraitDescriptions(self):
        # returns localized descriptions of the pets' notable traits,
        # ordered by significance/severity
        descs = []
        # make table of TraitQuality to localizer table index
        TraitQuality = TraitDistribution.TraitQuality
        Quality2index = {
            TraitQuality.VERY_BAD: 0,
            TraitQuality.BAD: 1,
            TraitQuality.GOOD: 2,
            TraitQuality.VERY_GOOD: 3,
            }
        for name, quality in self.extremeTraits:
            descs.append(TTLocalizer.PetTrait2descriptions[name][
                Quality2index[quality]])
        return descs
