from pandac import PandaModules as PM
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from otp.distributed import OtpDoGlobals
from toontown.coderedemption import TTCodeRedemptionConsts
import random
import string

class TTCRMAIRetryMgr(DirectObject):
    notify = directNotify.newCategory('TTCodeRedemptionMgrAI')

    MinRetryPeriod = 5
    RetryGrowMult = 1.1

    def __init__(self, air, codeRedemptionMgr):
        self.air = air
        self._codeRedemptionMgr = codeRedemptionMgr
        self._serialGen = SerialNumGen()
        self._retryPeriod = self.MinRetryPeriod
        self._redemptions = {}
            
    def addRedemption(self, avId, context, code):
        assert self.notify.debugCall()
        serial = self._serialGen.next()
        self._redemptions[serial] = ScratchPad(avId=avId, context=context, code=code, attemptNum=0)
        self._doRedemption(serial, True)

    def resolveRedemption(self, serial, context, avId, result, awardMgrResult):
        assert self.notify.debugCall()
        if serial not in self._redemptions:
            self.notify.warning('unexpected redemption resolution: %s, %s, %s, %s, %s' % (
                serial, context, avId, result, awardMgrResult))
            return
        info = self._redemptions.pop(serial)
        info.doLater.remove()
        self._retryPeriod = self.MinRetryPeriod
        if hasattr(self, '_stressTestInfo'):
            if (avId, context) in self._stressTestInfo.redemptions:
                code = self._stressTestInfo.redemptions.pop((avId, context))
                self._stressTestInfo.numCodesResolved += 1
                if result:
                    if not TTCodeRedemptionMgrAI.RandomizeStressTestCode:
                        self.notify.info('stress test redemption failed for %s (%s): %s, %s' % (
                            avId, code, result, awardMgrResult))
                else:
                    self.notify.debug('stress test redemption succeeded for %s (%s)' % (
                        avId, code))
                now = globalClock.getRealTime()
                if (now - self._stressTestInfo.lastLogT) > 10:
                    duration = now - self._stressTestInfo.startT
                    self._stressTestInfo.lastLogT = now
                    self.notify.info('stress test progress: %s codes resolved, %s codes/sec' % (
                        self._stressTestInfo.numCodesResolved, (self._stressTestInfo.numCodesResolved / duration)))
                self._checkCleanupStressTest()
        self._codeRedemptionMgr.sendUpdateToAvatarId(avId, 'redeemCodeResult', [context, result, awardMgrResult])

    def _doRedemption(self, serial, directCall, task=None):
        info = self._redemptions.get(serial)
        info.attemptNum += 1
        if info.attemptNum > 1:
            self._retryPeriod = max(self.MinRetryPeriod, self._retryPeriod * self.RetryGrowMult)
            self.notify.info('code redemption retry #%s for %s: %s' % ((info.attemptNum-1), info.avId, info.code))
        self.air.sendUpdateToDoId('TTCodeRedemptionMgr',
                                  'redeemCodeAiToUd',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_CODE_REDEMPTION_MANAGER,
                                  [serial, self._codeRedemptionMgr.doId, info.context, info.code, info.avId]
                                  )
        info.doLater = self.doMethodLater(self._retryPeriod, Functor(self._doRedemption, serial),
                                          uniqueName('CodeRedemptionRetry'))
        return Task.done

    # stress test API
    def startStressTest(self):
        assert not hasattr(self, '_stressTestClosed')
        self._stressTestInfo = ScratchPad()
        self._stressTestInfo.redemptions = {}
        self._stressTestInfo.numCodesSubmitted = 0
        self._stressTestInfo.numCodesResolved = 0
        self._stressTestInfo.startT = globalClock.getRealTime()
        self._stressTestInfo.lastLogT = globalClock.getRealTime()
        self._stressTestInfo.closed = False

    def finishStressTestSubmission(self):
        self._stressTestInfo.closed = True
        self._checkCleanupStressTest()

    def _checkCleanupStressTest(self):
        if self._stressTestInfo.closed and (
            self._stressTestInfo.numCodesSubmitted == self._stressTestInfo.numCodesResolved):
            duration = globalClock.getRealTime() - self._stressTestInfo.startT
            self.notify.info('stress test resolution completed: %s codes resolved, %s codes/sec' % (
                self._stressTestInfo.numCodesResolved, self._stressTestInfo.numCodesResolved / duration))
            del self._stressTestInfo

    def addStressTestRedemption(self, avId, context, code):
        self._stressTestInfo.redemptions[(avId, context)] = code
        self._stressTestInfo.numCodesSubmitted += 1
        self.addRedemption(avId, context, code)

class TTCodeRedemptionMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('TTCodeRedemptionMgrAI')

    WantStressTest = config.GetBool('stress-test-code-redemption', 0)
    StressTestRate = config.GetFloat('stress-test-code-redemption-rate', 3.)
    RandomizeStressTestCode = config.GetBool('randomize-code-redemption-stress-test-code', 0)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self._retryMgr = TTCRMAIRetryMgr(self.air, self)
        self.air.codeRedemptionManager = self
        if self.WantStressTest:
            printStack()
            taskMgr.doMethodLater(10., self._doStressTest,
                                  uniqueName('codeRedemptionStartStressTest'))

    def redeemCode(self, context, code):
        assert self.notify.debugCall()
        # pass it on to the UD w/out checking the content of the parameters; offload the
        # CPU work to the code redemption UD
        avId = self.air.getAvatarIdFromSender()
        self._retryMgr.addRedemption(avId, context, code)

    def redeemCodeResultUdToAi(self, serial, context, avId, result, awardMgrResult):
        assert self.notify.debugCall()
        # pass it back to the toon
        self._retryMgr.resolveRedemption(serial, context, avId, result, awardMgrResult)

    def _doStressTest(self, task):
        self._stressTestCode = 'stresstest'
        fPath = PM.Filename.expandFrom('$TOONTOWN/%scoderedemption/StressTestAvIds.txt' % (
            choice(__dev__, 'src/', ''))).toOsSpecific()
        self._stressTestFile = open(fPath)
        self._stressTestLastSendT = globalClock.getFrameTime()
        self._stressTestStartTime = globalClock.getRealTime()
        self._stressTestAvCount = 0
        self._stressTestLogT = globalClock.getRealTime()
        self.notify.info('starting stress test')
        self._retryMgr.startStressTest()
        taskMgr.add(self._stressTest, uniqueName('codeRedemptionStressTest'))
        return task.done

    def _stressTest(self, task):
        now = globalClock.getFrameTime()
        dt = now - self._stressTestLastSendT
        numCodes = max(0, int(dt * self.StressTestRate))
        self._stressTestLastSendT += (numCodes / float(self.StressTestRate))
        done = False
        while numCodes:
            try:
                line = self._stressTestFile.readline()
            except:
                raise
                done = True
            #print line
            if not done:
                try:
                    avId = int(line)
                except ValueError:
                    done = True
            if done:
                rate = self._stressTestAvCount / (globalClock.getRealTime() - self._stressTestStartTime)
                self.notify.info('stress test submission complete: %s codes submitted, %s codes/sec' % (
                    self._stressTestAvCount, rate))
                self._retryMgr.finishStressTestSubmission()
                return task.done
            if self.RandomizeStressTestCode:
                len = random.randrange(1, 20)
                code = ''
                while len:
                    code += random.choice(string.letters)
                    len -= 1
            else:
                code = self._stressTestCode
            self._retryMgr.addStressTestRedemption(avId, 0, code)
            numCodes -= 1
            self._stressTestAvCount += 1

        now = globalClock.getRealTime()
        if (now - self._stressTestLogT) > 10:
            self._stressTestLogT = now
            rate = self._stressTestAvCount / (globalClock.getRealTime() - self._stressTestStartTime)
            self.notify.info('stress test progress: %s codes submitted, %s codes/sec' % (
                self._stressTestAvCount, rate))

        return task.cont
