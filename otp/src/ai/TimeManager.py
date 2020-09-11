# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.distributed.ClockDelta import *
from direct.task import Task

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from direct.showbase import PythonUtil
from direct.showbase import GarbageReport
import time
import os
import sys
import re
        
class TimeManager(DistributedObject.DistributedObject):
    """
    This DistributedObject lives on the AI and on the client side, and
    serves to synchronize the time between them so they both agree, to
    within a few hundred milliseconds at least, what time it is.

    This used to use a push model where the AI side would push the
    time down to the client periodically, but now it uses a pull model
    where the client can request a synchronization check from time to
    time.  It also employs a round-trip measurement to minimize the
    effect of latency.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManager")

    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

        # The number of seconds to wait between automatic
        # synchronizations.  Set to 0 to disable auto sync after
        # startup.
        self.updateFreq = base.config.GetFloat('time-manager-freq', 1800)

        # The minimum number of seconds to wait between two unrelated
        # synchronization attempts.  Increasing this number cuts down
        # on frivolous synchronizations.
        self.minWait = base.config.GetFloat('time-manager-min-wait', 10)

        # The maximum number of seconds of uncertainty to tolerate in
        # the clock delta without trying again.
        self.maxUncertainty = base.config.GetFloat('time-manager-max-uncertainty', 1)

        # The maximum number of attempts to try to get a low-latency
        # time measurement before giving up and accepting whatever we
        # get.
        self.maxAttempts = base.config.GetInt('time-manager-max-attempts', 5)

        # A simulated clock skew for debugging, in seconds.
        self.extraSkew = base.config.GetInt('time-manager-extra-skew', 0)

        if self.extraSkew != 0:
            self.notify.info("Simulating clock skew of %0.3f s" % self.extraSkew)

        self.reportFrameRateInterval = base.config.GetDouble('report-frame-rate-interval', 300.0)

        self.talkResult = 0
        self.thisContext = -1
        self.nextContext = 0
        self.attemptCount = 0
        self.start = 0
        self.lastAttempt = -self.minWait*2

        self.setFrameRateInterval(self.reportFrameRateInterval)

        self._numClientGarbage = 0

    ### DistributedObject methods ###

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        self._gotFirstTimeSync = False
        if self.cr.timeManager != None:
            self.cr.timeManager.delete()
        self.cr.timeManager = self
        DistributedObject.DistributedObject.generate(self)

        self.accept(OTPGlobals.SynchronizeHotkey, self.handleHotkey)
        self.accept('clock_error', self.handleClockError)

        if __dev__ and base.config.GetBool('enable-garbage-hotkey', 0):
            self.accept(OTPGlobals.DetectGarbageHotkey, self.handleDetectGarbageHotkey)

        if self.updateFreq > 0:
            self.startTask()

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.synchronize("TimeManager.announceGenerate")

    def gotInitialTimeSync(self):
        return self._gotFirstTimeSync

    def disable(self):
        """
        This method is called when the DistributedObject is removed from
        active duty and stored in a cache.
        """
        # Warning! disable() is NOT called for TimeManager!  Duh!
        self.ignore(OTPGlobals.SynchronizeHotkey)
        if __dev__:
            self.ignore(OTPGlobals.DetectGarbageHotkey)
        self.ignore('clock_error')
        self.stopTask()
        taskMgr.remove('frameRateMonitor')
        if self.cr.timeManager == self:
            self.cr.timeManager = None
        del self._gotFirstTimeSync
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        self.ignore(OTPGlobals.SynchronizeHotkey)
        self.ignore(OTPGlobals.DetectGarbageHotkey)
        self.ignore('clock_error')
        self.stopTask()
        taskMgr.remove('frameRateMonitor')
        if self.cr.timeManager == self:
            self.cr.timeManager = None
        DistributedObject.DistributedObject.delete(self)

    ### Task management methods ###

    def startTask(self):
        self.stopTask()
        taskMgr.doMethodLater(self.updateFreq, self.doUpdate, "timeMgrTask")

    def stopTask(self):
        taskMgr.remove("timeMgrTask")

    def doUpdate(self, task):
        self.synchronize("timer")
        # Spawn the next one
        taskMgr.doMethodLater(self.updateFreq, self.doUpdate, "timeMgrTask")
        return Task.done

    ### User hotkey handling ###

    def handleHotkey(self):
        # For now, we don't impose any restrictions on the amount of
        # time we must wait between user-suggested resyncs.  Comment
        # this out to change this behavior.
        self.lastAttempt = -self.minWait*2

        if self.synchronize("user hotkey"):
            self.talkResult = 1
        else:
            # This should change to be more generic
            # maybe self.cr.localAv
            base.localAvatar.setChatAbsolute("Too soon.", CFSpeech | CFTimeout)

    ### Automatic clock error handling ###

    def handleClockError(self):
        self.synchronize("clock error")

    ### Synchronization methods ###
        
    def synchronize(self, description):
        """synchronize(self, string description)

        Call this function from time to time to synchronize watches
        with the server.  This initiates a round-trip transaction;
        when the transaction completes, the time will be synced.

        The description is the string that will be written to the log
        file regarding the reason for this synchronization attempt.

        The return value is true if the attempt is made, or false if
        it is too soon since the last attempt.
        """
        now = globalClock.getRealTime()

        if now - self.lastAttempt < self.minWait:
            self.notify.debug("Not resyncing (too soon): %s" % (description))
            return 0
            
        self.talkResult = 0
        self.thisContext = self.nextContext
        self.attemptCount = 0
        self.nextContext = (self.nextContext + 1) & 255
        self.notify.info("Clock sync: %s" % (description))
        self.start = now
        self.lastAttempt = now
        self.sendUpdate("requestServerTime", [self.thisContext])

        return 1

    
    def serverTime(self, context, timestamp, timeOfDay):
        """serverTime(self, int8 context, int32 timestamp, uint32 timeOfDay)

        This message is sent from the AI to the client in response to
        a previous requestServerTime.  It contains the time of day as
        observed by the AI.

        The client should use this, in conjunction with the time
        measurement taken before calling requestServerTime (above), to
        determine the clock delta between the AI and the client
        machines.
        """
        end = globalClock.getRealTime()

        # Compare the AI's current time with that previously reported
        # by the server at login (and adjusted since then by the local
        # clock).  It shouldn't be very different.
        aiTimeSkew = timeOfDay - self.cr.getServerTimeOfDay()

        if context != self.thisContext:
            self.notify.info("Ignoring TimeManager response for old context %d" % (context))
            return
        
        elapsed = end - self.start
        self.attemptCount += 1
        self.notify.info("Clock sync roundtrip took %0.3f ms" % (elapsed * 1000.0))
        self.notify.info("AI time delta is %s from server delta" % (PythonUtil.formatElapsedSeconds(aiTimeSkew)))

        average = (self.start + end) / 2.0 - self.extraSkew
        uncertainty = (end - self.start) / 2.0 + abs(self.extraSkew)

        globalClockDelta.resynchronize(average, timestamp, uncertainty)

        self.notify.info("Local clock uncertainty +/- %.3f s" % (globalClockDelta.getUncertainty()))

        if globalClockDelta.getUncertainty() > self.maxUncertainty:
            if self.attemptCount < self.maxAttempts:
                self.notify.info("Uncertainty is too high, trying again.")
                self.start = globalClock.getRealTime()
                self.sendUpdate("requestServerTime", [self.thisContext])
                return
            self.notify.info("Giving up on uncertainty requirement.")

        if self.talkResult:
            # This should change to be more generic
            # maybe self.cr.localAv
            base.localAvatar.setChatAbsolute("latency %0.0f ms, sync ±%0.0f ms" % (elapsed * 1000.0, globalClockDelta.getUncertainty() * 1000.0), CFSpeech | CFTimeout)
        
        self._gotFirstTimeSync = True
        messenger.send("gotTimeSync")

        
    def setDisconnectReason(self, disconnectCode):
        """setDisconnectReason(self, uint8 disconnectCode)

        This method is called by the client just before it leaves a
        shard to alert the AI as to the reason it's going.  If the AI
        doesn't get this message, it can assume the client aborted
        messily or its internet connection was dropped.
        """
        self.notify.info("Client disconnect reason %s." % (disconnectCode))
        self.sendUpdate("setDisconnectReason", [disconnectCode])
        
    def setExceptionInfo(self):
        """
        In the case of the client leaving for a Python exception, we
        also follow up the above message with this one, which just
        sends a text string describing the exception for the AI log.
        """
        info = PythonUtil.describeException()
        self.notify.info("Client exception: %s" % (info))
        self.sendUpdate("setExceptionInfo", [info])
        self.cr.flush()

    def d_setSignature(self, signature, hash, pyc):
        """
        This method is called by the client at startup time, to send
        the xrc signature and the prc hash to the AI for logging in
        case the client does anything suspicious.
        """
        self.sendUpdate("setSignature", [signature, hash, pyc])

    def sendCpuInfo(self):
        """
        This method is called by the client at startup time, to send
        the detailed CPU information to the server for logging.
        """

        if not base.pipe:
            return

        di = base.pipe.getDisplayInformation()
        if di.getNumCpuCores() == 0 and hasattr(base.pipe, 'lookupCpuData'):
            # If it says we have no CPU's, assume the data hasn't been
            # looked up yet, and look it up now.
            base.pipe.lookupCpuData()
            di = base.pipe.getDisplayInformation()

        di.updateCpuFrequency(0)
        cacheStatus = preloadCache()

        ooghz = 1.0e-009
        cpuSpeed = (di.getMaximumCpuFrequency() * ooghz,
                    di.getCurrentCpuFrequency() * ooghz)

        numCpuCores = di.getNumCpuCores()
        numLogicalCpus = di.getNumLogicalCpus()

        info = '%s|%s|%d|%d|%s|%s cpus' % (
            di.getCpuVendorString(), di.getCpuBrandString(),
            di.getCpuVersionInformation(), di.getCpuBrandIndex(),
            '%0.03f,%0.03f' % cpuSpeed,
            '%d,%d' % (numCpuCores, numLogicalCpus))
        
        print "cpu info: %s" % (info)
        self.sendUpdate("setCpuInfo", [info, cacheStatus])
            
    
    def setFrameRateInterval(self, frameRateInterval):
        """ This message is called at startup time, to start sending
        frame rate reports. """
        
        if frameRateInterval == 0:
            return

        if not base.frameRateMeter:
            # If we're not displaying a frame rate meter, go ahead and
            # set the global clock to the same interval, so we will be
            # reporting the average frame rate over the whole
            # interval.  (If we are displaying a frame rate meter,
            # don't do this, so the frame rate meter will be more
            # responsive.)

            # However, we'll put a cap on the frame rate interval, so
            # it doesn't go unreasonably wide if we set the reporting
            # interval to be fairly slow.
            maxFrameRateInterval = base.config.GetDouble('max-frame-rate-interval', 30.0)
            globalClock.setAverageFrameRateInterval(min(frameRateInterval, maxFrameRateInterval))

        taskMgr.remove('frameRateMonitor')
        taskMgr.doMethodLater(frameRateInterval,
                              self.frameRateMonitor, 'frameRateMonitor')
        
    def frameRateMonitor(self, task):
        """ This method is called every once in a while to report the
        user's average frame rate to the server. """

        from otp.avatar.Avatar import Avatar

        vendorId = 0
        deviceId = 0
        processMemory = 0
        pageFileUsage = 0
        physicalMemory = 0
        pageFaultCount = 0

        osInfo = (os.name, 0, 0, 0)
        cpuSpeed = (0, 0)
        numCpuCores = 0
        numLogicalCpus = 0
        apiName = 'None'

        if getattr(base, 'pipe', None):
            di = base.pipe.getDisplayInformation()
            if (di.getDisplayState() == DisplayInformation.DSSuccess):
                vendorId = di.getVendorId()
                deviceId = di.getDeviceId()

            di.updateMemoryInformation()
            oomb = 1.0 / (1024.0 * 1024.0)
            processMemory = di.getProcessMemory() * oomb
            pageFileUsage = di.getPageFileUsage() * oomb
            physicalMemory = di.getPhysicalMemory() * oomb
            pageFaultCount = di.getPageFaultCount() / 1000.0
            osInfo = (os.name, di.getOsPlatformId(), di.getOsVersionMajor(), di.getOsVersionMinor())
            if sys.platform == 'darwin':
                osInfo = self.getMacOsInfo(osInfo)
            di.updateCpuFrequency(0)

            ooghz = 1.0e-009
            cpuSpeed = (di.getMaximumCpuFrequency() * ooghz,
                        di.getCurrentCpuFrequency() * ooghz)

            numCpuCores = di.getNumCpuCores()
            numLogicalCpus = di.getNumLogicalCpus()
        
            apiName = base.pipe.getInterfaceName()


        self.d_setFrameRate(
            max(0, globalClock.getAverageFrameRate()),
            max(0, globalClock.calcFrameRateDeviation()),
            len(Avatar.ActiveAvatars),
            base.locationCode or '',
            max(0,time.time() - base.locationCodeChanged),
            max(0,globalClock.getRealTime()),
            base.gameOptionsCode,
            vendorId, deviceId, processMemory, pageFileUsage,
            physicalMemory, pageFaultCount, osInfo, cpuSpeed,
            numCpuCores, numLogicalCpus, apiName)

        return task.again
        
    def d_setFrameRate(self, fps, deviation, numAvs,
                       locationCode, timeInLocation, timeInGame,
                       gameOptionsCode, vendorId, deviceId,
                       processMemory, pageFileUsage, physicalMemory,
                       pageFaultCount, osInfo, cpuSpeed,
                       numCpuCores, numLogicalCpus, apiName):
        """ Called by frameRateMonitor to report the current frame
        rate to the server.
        """
        info = '%0.1f fps|%0.3fd|%s avs|%s|%d|%d|%s|0x%04x|0x%04x|%0.1fMB|%0.1fMB|%0.1fMB|%d|%s|%s|%s cpus|%s' % (
            fps, deviation, numAvs, locationCode, timeInLocation,
            timeInGame, gameOptionsCode,
            vendorId, deviceId, processMemory, pageFileUsage, physicalMemory,
            pageFaultCount, '%s.%d.%d.%d' % osInfo, '%0.03f,%0.03f' % cpuSpeed,
            '%d,%d' % (numCpuCores, numLogicalCpus),
            apiName)
        print "frame rate: %s" % (info)

        self.sendUpdate("setFrameRate", [
            fps, deviation, numAvs, locationCode,
            timeInLocation, timeInGame, gameOptionsCode,
            vendorId, deviceId, processMemory, pageFileUsage,
            physicalMemory, pageFaultCount, osInfo, cpuSpeed,
            numCpuCores, numLogicalCpus, apiName])

    if __dev__:
        def handleDetectGarbageHotkey(self):
            self._numClientGarbage = GarbageReport.b_checkForGarbageLeaks(wantReply=True)
            if self._numClientGarbage:
                s = "%s client garbage cycles found, see log" % self._numClientGarbage
            else:
                s = "0 client garbage cycles found"
            localAvatar.setChatAbsolute(s, CFSpeech | CFTimeout)

        def d_checkForGarbageLeaks(self, wantReply):
            # if wantReply is True, AI will send back a setNumAIGarbageLeaks msg
            self.sendUpdate('checkForGarbageLeaks', [wantReply])

        def setNumAIGarbageLeaks(self, numLeaks):
            if self._numClientGarbage and numLeaks:
                s = "%s client and %s AI garbage cycles found, see logs" % (self._numClientGarbage, numLeaks)
            elif numLeaks:
                s = "0 client and %s AI garbage cycles found, see log" % numLeaks
            else:
                s = "0 client and 0 AI garbage cycles found"
            localAvatar.setChatAbsolute(s, CFSpeech | CFTimeout)

        def d_setClientGarbageLeak(self, num, description):
            self.sendUpdate('setClientGarbageLeak', [num, description])

    def getMacOsInfo(self, defaultOsInfo):
        """Return a tuple of os name, platormid, major ver, minor ver."""
        result = defaultOsInfo
        try:
            theFile = open('/System/Library/CoreServices/SystemVersion.plist')
        except IOError:
            # hmm plain darwin box do nothing
            pass
        else:
            key = re.search(
                r'<key>ProductUserVisibleVersion</key>\s*' +
                r'<string>(.*?)</string>', theFile.read())
            theFile.close()
            if key is not None:
                try:
                    verString = key.group(1)
                    # we should now have something like 10.5.8
                    parts = verString.split('.')
                    major = int(parts[0])
                    minor = int(parts[1])
                    bugfix = int(parts[2])
                    # since platform id is -1, i'll put the bug fix number in there instead,  better than an arbitrary number
                    result = (sys.platform,
                              bugfix, # what do we put for platform id?
                              major,
                              minor)
                except Exception, e:
                    self.notify.debug("getMacOsInfo %s" % str(e))
        self.notify.debug('getMacOsInfo returning %s' % str(result))
        return result
                
