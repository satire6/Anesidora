from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
#from otp.otpbase import OTPGlobals
from otp.distributed import OtpDoGlobals
from otp.ai import AIMsgTypes
#from otp.uberdog.UberDogUtil import ManagedAsyncRequest
from direct.directnotify.DirectNotifyGlobal import directNotify

from direct.task import Task
import Queue
from direct.distributed.AsyncRequest import AsyncRequest
from pandac.PandaModules import Thread

notify = directNotify.newCategory('SnapshotRendererUD')

       
#--------------------------------------------------

class AvatarDNARequest(AsyncRequest):
    notify = notify

    def __init__(self,air,jobId,avatarId,writeToFile):
        assert self.notify.debugCall()
        self.__deleted = False
        AsyncRequest.__init__(self,air)

        self.avatarId = avatarId
        self.jobId = jobId
        self.writeToFile = writeToFile

        self.neededObjects[avatarId] = self.air.doId2do.get(avatarId)
        if self.neededObjects[avatarId] is not None:
            self.finish()
        else:
            self.askForObject(avatarId)

    def timeout(self,task):
        self.air.snapshotRenderer.errorFetchingAvatar(self.jobId,self.avatarId)
        self.delete()

    def finish(self):
        av = self.neededObjects.get(self.avatarId,None)
        if av is None:
            self.air.snapshotRenderer.errorFetchingAvatar(self.jobId,self.avatarId)
        else:
            self.air.snapshotRenderer.renderSnapshot(self.jobId,self.avatarId,av.dna,self.writeToFile)
        
        self.delete()

#--------------------------------------------------

class SnapshotRendererUD(DistributedObjectGlobalUD):
    """
    Uberdog object for rendering avatar pictures in response
    to DC requests.
    """
    notify = notify

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)

        self.air = air

        self.dispatcherLoc = OtpDoGlobals.OTP_DO_ID_SNAPSHOT_DISPATCHER
        self.myLoc = 0
        

    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.sendUpdateToChannel(
            AIMsgTypes.CHANNEL_CLIENT_BROADCAST, "online", [])
        self.sendUpdateToChannel(
            AIMsgTypes.OTP_CHANNEL_AI_AND_UD_BROADCAST, "online", [])
        self.myLoc = self.doId
        self.startAskingForWork()

    def delete(self):
        assert self.notify.debugCall()
        uber.taskMgr.remove('pollForWorkTask')
        self.ignoreAll()
        DistributedObjectGlobalUD.delete(self)

    # -- Internal methods --

    def renderSnapshot(self,jobId,avatarId,avatarDNA,writeToFile):
        print "OTP-level renderSnapshot method called!  You should override this!"

    def errorFetchingAvatar(self,jobId,avatarId):
        """
        Tell the dispatcher we had an error in the current task.
        It should send us back new work or not respond if there's nothing to do.
        """
        self.notify.warning("Error fetching DNA for avatar %d, reporting failure to the dispatcher." % avatarId)
        self.air.sendUpdateToGlobalDoId("SnapshotDispatcherUD","errorFetchingAvatar",self.dispatcherLoc,[self.myLoc,jobId])
        self.startAskingForWork()

    def errorRenderingAvatar(self,jobId,avatarId,avatarDNA):
        """
        Tell the dispatcher we had an error in the current task.
        It should send us back new work or not response if there's nothing to do.
        """
        self.notify.warning("Error rendering an image for avatar %d, reporting failure to the dispatcher.  DNA: %s" % (avatarId,avatarDNA))
        self.air.sendUpdateToGlobalDoId("SnapshotDispatcherUD","errorRenderingAvatar",self.dispatcherLoc,[self.myLoc,jobId])
        self.startAskingForWork()

    def renderSuccessful(self,jobId,avatarId,writeToFile):
        """
        Tell the dispatcher we finished the current task.
        If we don't hear back immediately, there's no new work
        so we need to start polling again
        """
        self.notify.debug("Successfully rendered avatar %d to %s" % (avatarId,writeToFile))
        self.air.sendUpdateToGlobalDoId("SnapshotDispatcherUD","renderSuccessful",self.dispatcherLoc,[self.myLoc,jobId])
        self.startAskingForWork()
        
        

    # -- Distributed Methods --

    def requestRender(self,jobId,avatarId,writeToFile):
        """
        'Please render this avatar' method.
        Called from DC space by a SnapshotDispatcher,
        results in an image being written to disk
        sometime after this function returns.
        """
        self.stopAskingForWork()
        AvatarDNARequest(self.air,jobId,avatarId,writeToFile)


    # -- Task Methods --

    def startAskingForWork(self):
        uber.taskMgr.remove('pollForWorkTask')
        uber.taskMgr.doMethodLater(2.0,self.pollForWorkTask,'pollForWorkTask')

    def stopAskingForWork(self):
        uber.taskMgr.remove('pollForWorkTask')

    def pollForWorkTask(self,task):
        """
        Task that polls the SnapshotDispatcher for rendering jobs.
        If there is work, the dispatcher calls back to requestRender.
        """
        # query the dispatcher for work
        self.air.sendUpdateToGlobalDoId("SnapshotDispatcherUD","requestNewWork",self.dispatcherLoc,[self.myLoc])
        return Task.again

