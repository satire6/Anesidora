import direct
from libdirect import HttpRequest
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.ai import AIMsgTypes
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.http.WebRequest import WebRequestDispatcher

from direct.task import Task
import Queue
import socket

#--------------------------------------------------

class RenderJob:
    """
    A single 'render this avatar' task.
    Record-keeping object for the dispatcher.
    """
    def __init__(self,jobId,replyTo,assignedTo,avatarId,writeToFile):
        self.jobId = jobId
        self.replyTo = replyTo
        self.assignedTo = assignedTo
        self.avatarId = avatarId
        self.writeToFile = writeToFile

#--------------------------------------------------

class SnapshotDispatcherUD(DistributedObjectGlobalUD):
    """
    Uberdog object for queuing and routing avatar
    render requests.  Happens to use the DC system
    for messaging but could easily be switched to UDP.
    """
    notify = directNotify.newCategory('SnapshotDispatcherUD')

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)

        self.air = air

        self.HTTPListenPort = uber.snapshotDispatcherHTTPListenPort
        self.renderOutputPrefix = uber.snapshotOutputRootDir
        self.renderOutputFormat = uber.snapshotOutputFormat

        self.numServed = 0
        self.numErrors = 0
        self.numServedAtLastLog = 0

        # Unassigned work
        self.jobQueue = Queue.Queue()

        # If the queue gets longer than this, log warnings
        self.maxSafeJobQueueLength = 1000

        # Assigned but incomplete work
        self.jobsInProgress = {}

        # Which renderers have work outstanding?
        self.rendererIsBusy = {}

        # Jobs we completed recently (so we can avoid doing them again)
        self.recentlyDeletedAvatars = {}

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("SnapshotDispatcher")
        self.webDispatcher.landingPage.setDescription("SnapshotDispatcher routes render jobs to any number of SnapshotRenderers.")
        self.webDispatcher.landingPage.addQuickStat("Total Renders", 0, 0)
        self.webDispatcher.registerGETHandler("getSnapshot",self.handleHTTPGetSnapshot)
        self.webDispatcher.registerGETHandler("queueSnapshot",self.handleHTTPQueueSnapshot)
        self.webDispatcher.listenOnPort(self.HTTPListenPort)

        self.air.setConnectionName("SnapshotDispatcherUD")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))

    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.sendUpdateToChannel(
            AIMsgTypes.CHANNEL_CLIENT_BROADCAST, "online", [])
        self.sendUpdateToChannel(
            AIMsgTypes.OTP_CHANNEL_AI_AND_UD_BROADCAST, "online", [])
        self.startCheckingIncomingHTTP()
        self.startMonitoringJobQueueSize()
        self.startLoggingStatus()

    def delete(self):
        assert self.notify.debugCall()
        self.ignoreAll()
        DistributedObjectGlobalUD.delete(self)

    def _idToFilename(self,avatarId):
        """
        Maps an avatarId to an output file with absolute path
        """
        subdirAndName = "%d/%d/%d/%d" % ((avatarId / 1000000000),
                                         (avatarId / 1000000) % 1000,
                                         (avatarId / 1000) % 1000,
                                         (avatarId))
        return self.renderOutputPrefix + \
               subdirAndName + \
               "." + \
               self.renderOutputFormat

    def startCheckingIncomingHTTP(self):
        uber.taskMgr.remove('pollHTTPTask')
        uber.taskMgr.doMethodLater(0.3,self.pollHTTPTask,'pollHTTPTask')

    def stopCheckingIncomingHTTP(self):
        uber.taskMgr.remove('pollHTTPTask')

    def startMonitoringJobQueueSize(self):
        uber.taskMgr.remove('monitorJobQueueTask')
        uber.taskMgr.doMethodLater(60.0,self.monitorJobQueueTask,'monitorJobQueueTask')

    def stopMonitoringJobQueueSize(self):
        uber.taskMgr.remove('monitorJobQueueTask')

    def startLoggingStatus(self):
        uber.taskMgr.remove('logStatusTask')
        uber.taskMgr.doMethodLater(300.0,self.logStatusTask,'logStatusTask')

    def stopLoggingStatus(self):
        uber.taskMgr.remove('logStatusTask')


    # -- Tasks --

    def pollHTTPTask(self,task):
        """
        Task that polls the HTTP server for new requests.
        """
        self.webDispatcher.poll()
        return Task.again

    def monitorJobQueueTask(self,task):
        """
        Task that checks to make sure the job queue is at a reasonable size.
        """
        if self.jobQueue._qsize() > self.maxSafeJobQueueLength:
            self.notify.warning("Job queue may be backed up!  %s jobs outstanding." % self.jobQueue._qsize())
        return Task.again

    def logStatusTask(self,task):
        """
        Task that writes normal status information to the log at a regular interval.
        """
        self.notify.info("Inc/cumu processed: %s/%s  |  Failures: %s  |  Now queued: %s" % (self.numServed - self.numServedAtLastLog,
                                                                                         self.numServed,
                                                                                         self.numErrors,
                                                                                         self.jobQueue._qsize()))
        self.numServedAtLastLog = self.numServed
        self.webDispatcher.landingPage.updateQuickStat("Total Renders", self.numServed)
        return Task.again

    def clearRecentDeleteRecord(self,avatarId):
        self.notify.debug("Removing deletion record for %s." % avatarId)
        self.recentlyDeletedAvatars.pop(avatarId,None)


    # -- HTTP Handlers --
    
    def handleHTTPGetSnapshot(self,replyTo,**kw):
        avatarId = kw.get("avatarId",None)
        if avatarId is None:
            replyTo.respondHTTP("400 Bad Request","<html><body>Error 400: Bad Request<br><br>You must specify an avatarId.</body></html>\r\n")
            return

        try:
            id = int(avatarId)
        except:
            replyTo.respondHTTP("400 Bad Request","<html><body>Error 400: Bad Request<br><br>Error parsing avatarId.</body></html>\r\n")
            return

        self.requestRender(id,replyTo)

    def handleHTTPQueueSnapshot(self,replyTo,**kw):
        avatarId = kw.get("avatarId",None)
        if avatarId is None:
            replyTo.respondHTTP("400 Bad Request","<html><body>Error 400: Bad Request<br><br>You must specify an avatarId.</body></html>\r\n")
            return

        try:
            id = int(avatarId)
        except:
            replyTo.respondHTTP("400 Bad Request","<html><body>Error 400: Bad Request<br><br>Error parsing avatarId.</body></html>\r\n")
            return

        self.requestRender(id)

        replyTo.respond("<html><body>Queue successful.</body></html>\r\n")


    # -- Distributed Methods --

    def requestRender(self,avatarId,replyTo=None):
        """
        Only outside entry point to the snapshot system.
        'Please render this avatar' method.
        Called from DC space or in response to an HTTP query.
        Work is queued up and later retrieved for processing
        by a call from a SnapshotRenderer, which will report
        back when it's finished the task (or failed to).
        """
        if avatarId in self.recentlyDeletedAvatars:
            self.notify.debug("Ignoring requestRender for deleted avatar %s." % avatarId)
            if replyTo is not None:
                replyTo.respondHTTP("400 Bad Request",
                                    "<html><body>Error 400: Bad Request<br><br>The avatar you specified could not be found.</body></html>\r\n")
            return
        self.numServed += 1
        jobId = self.numServed
        writeToFile = self._idToFilename(avatarId)
        self.jobQueue.put_nowait(RenderJob(jobId,replyTo,None,avatarId,writeToFile))
        self.notify.debug("Job %d: Queued" % jobId)


    def avatarDeleted(self,avatarId):
        """
        Message sent by the AvatarManager when an avatar gets deleted.
        'Please ignore any requests to render this guy.'
        """
        self.notify.debug("Creating deletion record for %s." % avatarId)
        self.recentlyDeletedAvatars[avatarId] = 1
        uber.taskMgr.doMethodLater(1800.0,self.clearRecentDeleteRecord,'clearRecentDeleteRecord-%s'%avatarId,[avatarId])
        
        
    def requestNewWork(self,rendererLoc):
        """
        Update received from a SnapshotRenderer.
        'I am idle, give me work!'
        Send the SnapshotRenderer some work.
        If we've already sent him work, ignore this request
        until he responds or times out.
        """
        if self.rendererIsBusy.setdefault(rendererLoc,False):
            self.notify.debug("Ignoring work request from %d because he already has work outstanding." % rendererLoc)
            return
        try:
            job = self.jobQueue.get_nowait()
        except Queue.Empty:
            # No work to give!  Do nothing.
            return

        job.assignedTo = rendererLoc
        self.rendererIsBusy[rendererLoc] = True
        self.jobsInProgress[job.jobId] = job
        self.air.sendUpdateToGlobalDoId("SnapshotRendererUD",
                                        "requestRender",
                                        rendererLoc,
                                        [job.jobId,
                                         job.avatarId,
                                         job.writeToFile])
        self.notify.debug("Job %d: Sent to renderer %d" % (job.jobId,rendererLoc))
        # insert a task to report failure if we don't hear back
        uber.taskMgr.doMethodLater(20.0,self.jobTimedOut,"rendertimeout-%d"%job.jobId,[job.jobId])


    def jobTimedOut(self,jobId,task=None):
        self.notify.warning("Timed out waiting for a response from job %d!" % jobId)
        self.numErrors += 1
        job = self.jobsInProgress.pop(jobId,None)
        if job is not None:
            self.notify.warning("Job %d was attempting to render avId %d." % (jobId,job.avatarId))
            self.rendererIsBusy[job.assignedTo] = False
            if job.replyTo is not None:
                job.replyTo.timeout()
        else:
            self.notify.warning("Didn't have a job %d listed when we got the timeout." % jobId)
        return Task.done

    def cancelTimeout(self,jobId):
        uber.taskMgr.remove("rendertimeout-%d" % jobId)

    def errorFetchingAvatar(self,rendererLoc,jobId):
        """
        Update received from a SnapshotRenderer.
        'I had an error trying to get this avatar's data.'
        The avatar probably doesn't exist so we should
        report back that we failed (if someone is waiting)
        and give up.
        
        Also, send the SnapshotRenderer more work.
        """
        self.numErrors += 1
        job = self.jobsInProgress.pop(jobId,None)
        self.cancelTimeout(jobId)
        if job is None:
            self.notify.warning("Got back an error for an unrecognized job: %d" % jobId)
            return

        self.notify.warning("errorFetchingAvatar from renderer %d for job %d on avatar %d." % (rendererLoc,jobId,job.avatarId))

        self.rendererIsBusy[job.assignedTo] = False

        if job.replyTo is not None:
            job.replyTo.respondHTTP("400 Bad Request",
                                    "<html><body>Error 400: Bad Request<br><br>The avatar you specified could not be found.</body></html>\r\n")

        self.requestNewWork(rendererLoc)


    def errorRenderingAvatar(self,rendererLoc,jobId):
        """
        Update received from a SnapshotRenderer.
        'I had an error trying to render this avatar.'
        The avatar exists but we couldn't render him
        for some reason.  Report back that we failed
        (if someone is waiting) and give up.
        
        Also, send the SnapshotRenderer more work.
        """
        self.numErrors += 1
        job = self.jobsInProgress.pop(jobId,None)
        self.cancelTimeout(jobId)
        if job is None:
            self.notify.warning("Got back an error for an unrecognized job: %d" % jobId)
            return

        self.notify.warning("errorRenderingAvatar from renderer %d for job %d on avatar %d." % (rendererLoc,jobId,job.avatarId))

        self.rendererIsBusy[job.assignedTo] = False

        if job.replyTo is not None:
            job.replyTo.respondHTTP("503 Internal Server Error",
                                    "<html><body>Error 503: Internal Server Error<br><br>There was an error rendering your avatar.</body></html>")

        self.requestNewWork(rendererLoc)


    def renderSuccessful(self,rendererLoc,jobId):
        """
        Update received from a SnapshotRenderer.
        'I successfully rendered this avatar.'
        Report back that we succeeded (if someone is
        waiting).
        
        Also, send the SnapshotRenderer more work.
        """
        job = self.jobsInProgress.pop(jobId,None)
        self.cancelTimeout(jobId)
        if job is None:
            self.notify.warning("Got back success for an unrecognized job: %d" % jobId)
            return

        self.notify.debug("Job %d: Successfully rendered avatar %d" % (jobId,job.avatarId))

        self.rendererIsBusy[job.assignedTo] = False

        if job.replyTo is not None:
            job.replyTo.respond("<html><body>%s</body></html>"%job.writeToFile)

        self.requestNewWork(rendererLoc)
        

