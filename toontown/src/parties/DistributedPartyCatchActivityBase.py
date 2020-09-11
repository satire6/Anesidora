import math
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame.DropScheduler import ThreePhaseDropScheduler
from toontown.parties import PartyGlobals

class DistributedPartyCatchActivityBase:
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCatchActivityBase")

    # number of players at which game stops dropping more items
    FallRateCap_Players = 20

    def calcDifficultyConstants(self, numPlayers):
        """ This function calculates the constants that depend on
        the difficulty settings and/or the number of players
        This function can be called repeatedly with different parameters
        at the start of a minigame session. """
        # this is how long the game waits to start dropping stuff
        self.FirstDropDelay = 0.

        # after this many seconds, the game stops dropping things slower
        self.NormalDropDelay = int((1. / 12) * PartyGlobals.CatchActivityDuration)
        # after this many seconds, the game starts dropping things faster
        self.FasterDropDelay = int((9. / 12) * PartyGlobals.CatchActivityDuration)
        DistributedPartyCatchActivityBase.notify.debug(
            'will start dropping fast after %s seconds' % self.FasterDropDelay)

        # how much longer should the drop period be (time between drops)
        # during the 'slower drop' interval at the beginning of the game?
        # 1. == no difference, 2. == 1/2 as fast
        self.SlowerDropPeriodMult = 1.5

        # how much shorter should the drop period be (time between
        # drops) during the 'faster drop' interval at the end of
        # the game? .5 == 2x as fast, 1. == no difference
        self.FasterDropPeriodMult = 1./3

        self.ToonSpeed = 16.0
        # no need to scale up the toon speed when more toons are playing;
        # each individual toon doesn't need to be able to cover the
        # entire stage

        def scaledDimensions(widthHeight, scale):
            """
            returns [w2,h2], where (w2*h2 == scale*w*h) and w/h==w2/h2
            In other words, it returns a width and height whose area is
            'scale' times the area of the provided width and height,
            preserving the width:height ratio.
            """
            # we know:
            # w2*h2 = s*w*h
            # w/h = w2/h2
            #
            # solve for h2 in terms of w2, w, and h
            # w/h = w2/h2
            # h2 = h*w2/w
            #
            # plug it in the other eq
            # w2*h2 = s*w*h
            # w2*h*w2/w = s*w*h
            # w2^2*h/w = s*w*h
            # w2^2 = s*w^2
            # the same holds true for height:
            # h2^2 = s*h^2
            #
            # since width and height cannot be negative:
            # w2 = sqrt(s*w^2)
            # h2 = sqrt(s*h^2)
            w, h = widthHeight
            return [math.sqrt(scale * w * w),
                    math.sqrt(scale * h * h),
                    ]

        # width, height (in feet)
        BaseStageDimensions = [36, 36]
        self.StageAreaScale = 1.0
        self.StageLinearScale = math.sqrt(self.StageAreaScale)
        DistributedPartyCatchActivityBase.notify.debug("StageLinearScale: %s" % self.StageLinearScale)
        self.StageDimensions = scaledDimensions(BaseStageDimensions,
                                                self.StageAreaScale)
        DistributedPartyCatchActivityBase.notify.debug("StageDimensions: %s" % self.StageDimensions)
        self.StageHalfWidth = self.StageDimensions[0] / 2.0
        self.StageHalfHeight = self.StageDimensions[1] / 2.0

        # MinOffscreenHeight (moH): this is a Z height that is just
        # off the top of the screen; it's safe for objects to pop
        # into existence at this height.
        self.MinOffscreenHeight = 30

        # Calculate an onscreen time for the baseline falling objects so
        # that toons can reasonably run from one corner of the stage
        # to the opposite corner in time to catch a fruit.
        #
        # Keep in mind that the toon most likely just caught the previous
        # fruit, most likely close to the end of its fall; that means the
        # next fruit is either halfway through its fall, or even 3/4
        # of the way down during the end-game drop blitz (assuming that
        # the drop period, defined below, is 1/2 of the baseline drop
        # duration)
        #
        # Also keep in mind that the drop period is based off of the
        # _entire_ fall duration of the baseline object, of which
        # the onscreen fall duration is only a part (see definition
        # of self.OffscreenTime, below;
        # fall duration = offscreen time + onscreen time
        distance = math.sqrt(
            (self.StageDimensions[0] * self.StageDimensions[0]) + 
            (self.StageDimensions[1] * self.StageDimensions[1]))
        # when there are more players, each individual toon doesn't need
        # to be able to cover the entire stage...
        distance /= self.StageLinearScale


        ToonRunDuration = distance / self.ToonSpeed
        # this is the ratio of offscreen to onscreen time for the baseline
        # object.
        # 1. == object is offscreen for same duration that it's onscreen
        # .5 == object is offscreen 1/2 as long as it's onscreen
        offScreenOnScreenRatio = 1.
        # this is the fraction of the total baseline object fall duration
        # (offscreen and on, from the moment the shadow shows up to the
        # moment the obj hits the ground) during which the toon should be
        # able to run the full diagonal of the stage
        fraction = (1. / 3) * .85
        # ToonRunDuration = fraction * (FallDur)
        # ToonRunDuration = fraction * (OnscreenDur + OffscreenDur)
        # ToonRunDuration = fraction * (OnscreenDur + (OnscreenDur*OffOnratio))
        # (OnscreenDur + (OnscreenDur*OffOnratio)) = ToonRunDuration / fraction
        # OnscreenDur * (1 + OffOnratio) = ToonRunDuration / fraction
        # OnscreenDur = ToonRunDuration / [fraction * (1 + OffOnratio)]
        self.BaselineOnscreenDropDuration = (
            ToonRunDuration / (fraction * (1. + offScreenOnScreenRatio)))
        DistributedPartyCatchActivityBase.notify.debug("BaselineOnscreenDropDuration=%s" % 
                          self.BaselineOnscreenDropDuration)

        # tOff. How long all objects 'drop' before reaching moH (during this
        # period, you just see the shadow growing on the ground)
        self.OffscreenTime = (offScreenOnScreenRatio * 
                              self.BaselineOnscreenDropDuration)
        DistributedPartyCatchActivityBase.notify.debug("OffscreenTime=%s" % self.OffscreenTime)

        # at this point, we can calculate the total drop duration for
        # baseline objects
        self.BaselineDropDuration = (self.BaselineOnscreenDropDuration + 
                                     self.OffscreenTime)

        # this should be OK as long as we don't make any object types
        # that fall slower than the baseline type...
        self.MaxDropDuration = self.BaselineDropDuration

        # period at which to drop objects; based on the baseline object's
        # fall duration
        self.DropPeriod = self.BaselineDropDuration / 3.
        # dampen the impact of each successive player, on the theory that
        # it's actually more difficult to catch fruit with more players playing
        scaledNumPlayers = (((min(numPlayers, self.FallRateCap_Players) - 1.) * .85) + 1.)
        self.DropPeriod /= scaledNumPlayers

        # figure out how many fruits and anvils will be dropped

        # relative probabilities that a given drop object will
        # be of a particular type
        typeProbs = {'fruit' : 3,
                     'anvil' : 1,
                     }
        # normalize the probabilities to [0..1]
        probSum = reduce(lambda x, y: x + y, typeProbs.values())
        for key in typeProbs.keys():
            typeProbs[key] = float(typeProbs[key]) / probSum

        scheduler = ThreePhaseDropScheduler(
            PartyGlobals.CatchActivityDuration,
            self.FirstDropDelay, self.DropPeriod, self.MaxDropDuration,
            self.SlowerDropPeriodMult, self.NormalDropDelay,
            self.FasterDropDelay, self.FasterDropPeriodMult)

        self.totalDrops = 0
        while not scheduler.doneDropping(continuous=True):
            scheduler.stepT()
            self.totalDrops += 1

        # calc number of fruits
        self.numFruits = int(self.totalDrops * typeProbs['fruit'])
        # however many drop slots are left, that's how many anvils
        # there will be
        self.numAnvils = int(self.totalDrops - self.numFruits)

        self.generationDuration = scheduler.getDuration()
