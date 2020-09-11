from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import formatTimeExact

Settings = ScratchPad(
    DetectWindow = config.GetFloat('code-redemption-spam-detect-window', 30.), # minutes
    DetectThreshold = config.GetInt('code-redemption-spam-detect-threshold', 10),
    FirstPenalty = config.GetFloat('code-redemption-spam-first-penalty', .5), # minutes
    PenaltyMultiplier = config.GetFloat('code-redemption-spam-penalty-multiplier', 2.),
    MaxPenaltyDays = config.GetFloat('code-redemption-spam-max-penalty-days', 2.),
    PenaltyResetDays = config.GetFloat('code-redemption-penalty-reset-days', 7.),
    )

class TTCodeRedemptionSpamDetector:
    notify = directNotify.newCategory('TTCodeRedemptionSpamDetector')

    def __init__(self):
        self._avId2tracker = {}
        if __dev__:
            #self._tester = TTCRSDTester(self)
            pass
        self._cullTask = taskMgr.doMethodLater(10 * 60, self._cullTrackers, uniqueName('cullCodeSpamTrackers'))

    def destroy(self):
        if __dev__:
            #self._tester.destroy()
            self._tester = None

    def codeSubmitted(self, avId):
        if avId not in self._avId2tracker:
            self._avId2tracker[avId] = TTCRSDTracker(avId)
        self._avId2tracker[avId].codeSubmitted()

    def avIsBlocked(self, avId):
        tracker = self._avId2tracker.get(avId)
        if tracker:
            return tracker.avIsBlocked()
        return False

    def _cullTrackers(self, task=None):
        # remove records for avIds that have gone long enough without spamming
        avIds = self._avId2tracker.keys()
        for avId in avIds:
            tracker = self._avId2tracker.get(avId)
            if tracker.isExpired():
                self.notify.debug('culling code redemption spam tracker for %s' % avId)
                self._avId2tracker.pop(avId)
        return task.again

class TTCRSDTracker:
    notify = directNotify.newCategory('TTCodeRedemptionSpamDetector')

    def __init__(self, avId):
        self._avId = avId
        self._timestamps = []
        self._lastTimestamp = None
        self._penaltyDuration = 0
        self._penaltyUntil = 0

    def codeSubmitted(self):
        now = globalClock.getRealTime()
        self.notify.debug('codeSubmitted by %s @ %s' % (self._avId, now))
        if self._penaltyActive():
            return
        self._timestamps.append(now)
        self._lastTimestamp = now
        self.update()

    def isExpired(self):
        if self._lastTimestamp is None:
            return True
        now = globalClock.getRealTime()
        # if they've gone for X days without spamming, we can wipe that toon's record
        amnestyDelay = Settings.PenaltyResetDays * 24 * 60 * 60
        return now > (self._lastTimestamp + amnestyDelay)

    def update(self):
        self._trimTimestamps()
        if (not self._penaltyActive()) and self._overThreshold():
            if self._penaltyDuration == 0:
                self._penaltyDuration = Settings.FirstPenalty * 60 # seconds/min
            else:
                self._penaltyDuration = self._penaltyDuration * Settings.PenaltyMultiplier
            MaxPenaltySecs = Settings.MaxPenaltyDays * 24 * 60 * 60
            if self._penaltyDuration > MaxPenaltySecs:
                self._penaltyDuration = MaxPenaltySecs
            self._penaltyUntil = globalClock.getRealTime() + self._penaltyDuration
            self._timestamps = self._timestamps[Settings.DetectThreshold:]
            durationStr = formatTimeExact(self._penaltyDuration)
            self.notify.info('time penalty for %s: %s' % (self._avId, durationStr))

    def avIsBlocked(self):
        self.update()
        return self._penaltyActive()

    def _trimTimestamps(self):
        now = globalClock.getRealTime()
        cutoff = now - (Settings.DetectWindow * 60) # seconds/min
        while len(self._timestamps):
            if self._timestamps[0] < cutoff:
                self._timestamps = self._timestamps[1:]
            else:
                break

    def _penaltyActive(self):
        return globalClock.getRealTime() < self._penaltyUntil

    def _overThreshold(self):
        return len(self._timestamps) > Settings.DetectThreshold

if __dev__:
    class TTCRSDTester(DirectObject):
        notify = directNotify.newCategory('TTCodeRedemptionSpamDetector')

        def __init__(self, detector):
            self._detector = detector
            self._idGen = SerialNumGen()
            self.notify.info('starting tests...')
            self._thresholdTest()
            self._timeoutTest()
            
        def destroy(self):
            self._detector = None
            
        def _thresholdTest(self):
            avId = self._idGen.next()
            for i in xrange(Settings.DetectThreshold+1):
                self._detector.codeSubmitted(avId)
                if i < Settings.DetectThreshold:
                    assert not self._detector.avIsBlocked(avId)
                else:
                    assert self._detector.avIsBlocked(avId)
            self.notify.info('threshold test passed.')
                    
        def _timeoutTest(self):
            avId = self._idGen.next()
            for i in xrange(Settings.DetectThreshold+1):
                self._detector.codeSubmitted(avId)
            assert self._detector.avIsBlocked(avId)
            self._timeoutTestStartT = globalClock.getRealTime()
            penaltyDuration = Settings.FirstPenalty * 60
            self._timeoutTestEventT = penaltyDuration
            self.doMethodLater(Settings.FirstPenalty * 60 * .5, Functor(self._timeoutEarlyTest, avId),
                               uniqueName('timeoutEarlyTest'))
            self.doMethodLater(Settings.FirstPenalty * 60 * 10, Functor(self._timeoutLateTest, avId),
                               uniqueName('timeoutLateTest'))
            
        def _timeoutEarlyTest(self, avId, task=None):
            # only do this test if we didn't chug
            if (globalClock.getRealTime() - self._timeoutTestStartT) < (self._timeoutTestEventT * .9):
                assert self._detector.avIsBlocked(avId)
            return task.done
        
        def _timeoutLateTest(self, avId, task=None):
            assert not self._detector.avIsBlocked(avId)
            for i in xrange(Settings.DetectThreshold+1):
                self._detector.codeSubmitted(avId)
            assert self._detector.avIsBlocked(avId)
            self._timeoutLateTestStartT = globalClock.getRealTime()
            penaltyDuration = Settings.PenaltyMultiplier * Settings.FirstPenalty * 60
            self._timeoutLateTestEventT = penaltyDuration
            self.doMethodLater(penaltyDuration * .5, Functor(self._timeoutSecondEarlyTest, avId),
                               uniqueName('timeoutSecondEarlyTest'))
            self.doMethodLater(penaltyDuration * 1.5, Functor(self._timeoutSecondLateTest, avId),
                               uniqueName('timeoutSecondLateTest'))
            return task.done

        def _timeoutSecondEarlyTest(self, avId, task=None):
            # only do this test if we didn't chug
            if (globalClock.getRealTime() - self._timeoutLateTestStartT) < (self._timeoutLateTestEventT * .9):
                assert self._detector.avIsBlocked(avId)
            return task.done

        def _timeoutSecondLateTest(self, avId, task=None):
            assert not self._detector.avIsBlocked(avId)
            self.notify.info('timeout test passed.')
            return task.done
