"""DropScheduler.py: contains the DropScheduler class"""

class DropScheduler:
    """
    this class handles the timing aspect of the drops.
    this functionality is isolated to allow the AI server to calculate
    the number of fruits on its own

    gameDuration is the length of the game in seconds
    firstDropDelay is # of seconds before first obj is dropped
    dropPeriod is # of seconds between drops
    maxDropDuration is length of entire drop for slowest-dropping item
    fasterDropDelay is # of seconds before game starts dropping faster
    fasterDropPeriodMult is multiplier of dropPeriod after fasterDropDelay
    """
    def __init__(self, gameDuration,
                 firstDropDelay, dropPeriod, maxDropDuration,
                 fasterDropDelay, fasterDropPeriodMult, startTime=None):
        self.gameDuration         = gameDuration
        self.firstDropDelay       = firstDropDelay
        # private to emphasize use of getDropPeriod(), below
        self._dropPeriod         = dropPeriod
        self.maxDropDuration      = maxDropDuration
        self.fasterDropDelay      = fasterDropDelay
        self.fasterDropPeriodMult = fasterDropPeriodMult
        if startTime is None:
            startTime = 0
        self._startTime = startTime
        self.curT = self._startTime + self.firstDropDelay

    def getT(self):
        return self.curT

    def getDuration(self):
        return self.gameDuration

    def getDropPeriod(self):
        # start dropping twice as fast near the end of the game
        delay = self._dropPeriod
        if (self.curT - self._startTime) >= self.fasterDropDelay:
            delay *= self.fasterDropPeriodMult
        return delay

    def doneDropping(self, continuous=None):
        """ returns true if an object would land too late if it were dropped
        right now """
        # time at which the slowest object would land if we dropped it now
        landTime = (self.getT() - self._startTime) + self.maxDropDuration
        # extend the end of the game by the drop period, to ensure
        # that one and only one item drops after the timer stops
        if continuous is None:
            continuous = False
        else:
            # if continuous, this scheduler will leave off where a
            # new one begins
            continuous = True
        if continuous:
            maxTime = (self.gameDuration + self.maxDropDuration)
        else:
            maxTime = (self.gameDuration + self.getDropPeriod())
        return landTime >= maxTime

    def skipPercent(self, percent):
        numSkips = 0
        while True:
            prevT = self.curT
            self.stepT()
            if self.curT >= (percent * self.gameDuration):
                self.curT = prevT
                break
            else:
                numSkips += 1

        return numSkips

    def stepT(self):
        self.curT += self.getDropPeriod()

class ThreePhaseDropScheduler(DropScheduler):
    """ scheduler that supports slow, normal, and fast periods """
    def __init__(self, gameDuration,
                 firstDropDelay, dropPeriod, maxDropDuration,
                 slowerDropPeriodMult, normalDropDelay,
                 fasterDropDelay, fasterDropPeriodMult, startTime=None):
        self._slowerDropPeriodMult = slowerDropPeriodMult
        self._normalDropDelay = normalDropDelay
        DropScheduler.__init__(self, gameDuration,
                               firstDropDelay, dropPeriod, maxDropDuration,
                               fasterDropDelay, fasterDropPeriodMult, startTime)

    def getDropPeriod(self):
        delay = self._dropPeriod
        if (self.curT - self._startTime) < self._normalDropDelay:
            delay *= self._slowerDropPeriodMult
        elif (self.curT - self._startTime) >= self.fasterDropDelay:
            delay *= self.fasterDropPeriodMult
        return delay
