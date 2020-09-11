from AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import GarbageReport
from otp.otpbase import OTPGlobals
from otp.ai.GarbageLeakServerEventAggregatorAI import GarbageLeakServerEventAggregatorAI
import time

class TimeManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManagerAI")

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        if not __dev__:
            # double-check that we're not implementing a client-sendable debug DC method in production
            if hasattr(self, 'checkForGarbageLeaks'):
                self.notify.error('checkForGarbageLeaks should not be defined outside of __dev__')

    def requestServerTime(self, context):
        """requestServerTime(self, int8 context)

        This message is sent from the client to the AI to initiate a
        synchronization phase.  The AI should immediately report back
        with its current time.  The client will then measure the round
        trip.
        """
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        requesterId = self.air.getAvatarIdFromSender()
        timeOfDay = int(time.time())
        self.sendUpdateToAvatarId(requesterId, "serverTime",
                                  [context, timestamp, timeOfDay])
        
    def setDisconnectReason(self, disconnectCode):
        """setDisconnectReason(self, uint8 disconnectCode)

        This method is called by the client just before it leaves a
        shard to alert the AI as to the reason it's going.  If the AI
        doesn't get this message, it can assume the client aborted
        messily or its internet connection was dropped.
        """
        requesterId = self.air.getAvatarIdFromSender()
        self.notify.info("Client %s leaving for reason %s (%s)." % (
            requesterId, disconnectCode,
            OTPGlobals.DisconnectReasons.get(disconnectCode,
                                             'invalid reason')))

        if disconnectCode in OTPGlobals.DisconnectReasons:
            self.air.setAvatarDisconnectReason(requesterId, disconnectCode)
        else:
            self.air.writeServerEvent(
                'suspicious', requesterId, 'invalid disconnect reason: %s' % disconnectCode)
        
    def setExceptionInfo(self, info):
        """setExceptionInfo(self, string info)

        In the case of the client leaving for a Python exception, we
        also follow up the above message with this one, which just
        sends a text string describing the exception for the AI log.
        """
        requesterId = self.air.getAvatarIdFromSender()
        self.notify.info("Client %s exception: %s" % (requesterId, info))
        serverVersion = simbase.config.GetString('server-version','')
        self.air.writeServerEvent('client-exception', requesterId, '%s|%s' % (serverVersion,info))

    def setSignature(self, signature, hash, pyc):
        """
        This method is called by the client at startup time, to send
        the xrc signature and the prc hash to the AI for logging in
        case the client does anything suspicious.
        """
        if signature:
            requesterId = self.air.getAvatarIdFromSender()
            prcHash = HashVal()
            prcHash.setFromBin(hash)
            info = '%s|%s' % (signature, prcHash.asHex())
            self.notify.info('Client %s signature: %s' % (requesterId, info))
            self.air.writeServerEvent('client-signature', requesterId, info)

        pycHash = HashVal()
        pycHash.setFromBin(pyc)
        if pycHash != HashVal():
            info = pycHash.asHex()
            self.notify.info('Client %s py signature: %s' % (requesterId, info))
            self.air.writeServerEvent('client-py-signature', requesterId, info)

    def setCpuInfo(self, info, cacheStatus):
        """
        This method is called by the client at startup time, to send
        the detailed CPU information to the server for logging.
        """
        requesterId = self.air.getAvatarIdFromSender()
        
        self.notify.info('client-cpu %s|%s' % (requesterId, info))
        self.air.writeServerEvent('client-cpu', requesterId, info)
        # We call this cacheStatus, but really it's the mac address or
        # other client fingerprint information, in a simple
        # obfuscating cipher.  Decode it.
        key = 'outrageous'
        p = 0
        fingerprint = ''
        for ch in cacheStatus:
            ic = ord(ch) ^ ord(key[p])
            p += 1
            if p >= len(key):
                p = 0
            fingerprint += chr(ic)

        self.notify.info('client-fingerprint %s|%s' % (requesterId, fingerprint))
        self.air.writeServerEvent('client-fingerprint', requesterId, fingerprint)
        if hasattr(self.air, 'cpuInfoMgr'):
            self.air.cpuInfoMgr.sendCpuInfoToUd(info, fingerprint)


    def setFrameRate(self, fps, deviation, numAvs,
                     locationCode, timeInLocation, timeInGame,
                     gameOptionsCode, vendorId, deviceId,
                     processMemory, pageFileUsage, physicalMemory,
                     pageFaultCount, osInfo, cpuSpeed,
                     numCpuCores, numLogicalCpus, apiName):
        """ This method is called by the client at the interval
        specified by getFrameRateInterval(), to report its current
        frame rate. """

        requesterId = self.air.getAvatarIdFromSender()
        info = '%0.1f fps|%0.3fd|%s avs|%s|%d|%d|%s|0x%04x|0x%04x|%0.1fMB|%0.1fMB|%0.1fMB|%d|%s|%s|%s cpus|%s' % (
            fps, deviation, numAvs, locationCode, timeInLocation,
            timeInGame, gameOptionsCode,
            vendorId, deviceId, processMemory, pageFileUsage, physicalMemory,
            pageFaultCount, '%s.%d.%d.%d' % osInfo, '%0.03f,%0.03f' % cpuSpeed,
            '%d,%d' % (numCpuCores, numLogicalCpus),
            apiName)
        self.notify.info('client-fps %s|%s' % (requesterId, info))
        self.air.writeServerEvent('client-fps', requesterId, info)

    if __dev__:
        def checkForGarbageLeaks(self, wantReply):
            senderId = self.air.getAvatarIdFromSender()
            self.notify.info("checking for garbage leaks requested by %s" % senderId)
            # okay checking for garbage leaks should only be done by devs, it's rare enough i'll flag it
            # as suspicious
            self.air.writeServerEvent('suspicious', senderId, 'checkForGarbageLeaks')
            numLeaks = GarbageReport.checkForGarbageLeaks()
            if wantReply:
                requesterId = self.air.getAvatarIdFromSender()
                self.sendUpdateToAvatarId(requesterId, 'setNumAIGarbageLeaks', [numLeaks])

        def setClientGarbageLeak(self, num, description):
            messenger.send(GarbageLeakServerEventAggregatorAI.ClientLeakEvent, [num, description])
