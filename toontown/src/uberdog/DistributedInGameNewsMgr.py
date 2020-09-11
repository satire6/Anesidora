import socket
import datetime
import os
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.DistributedObject import DistributedObject
from toontown.toonbase import ToontownGlobals
from toontown.uberdog import InGameNewsResponses

class DistributedInGameNewsMgr(DistributedObject ):
    """
    Uberdog object that keeps track of the last time in game news has been updated
    """
    notify = directNotify.newCategory('InGameNewsMgr')
    neverDisable = 1

    def __init__(self, cr):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        DistributedObject.__init__(self, cr)
        base.cr.inGameNewsMgr = self

    def delete(self):
        """Delete ourself."""
        DistributedObject.delete(self)
        self.cr.inGameNewsMgr  = None
        
    def disable(self):
        self.notify.debug( "i'm disabling InGameNewsMgr  rightnow.")
        DistributedObject.disable(self)
        
    def generate(self):
        # Called when the client loads
        self.notify.debug("BASE: generate")
        DistributedObject.generate(self)
        

    def setLatestIssueStr(self, issueStr):
        """We normally get this once, we could get this when a new issue is released while logged in."""
        # the string we get is in utc
        assert self.notify.debugStateCall(self)
        self.latestIssueStr = issueStr
        self.latestIssue = base.cr.toontownTimeManager.convertUtcStrToToontownTime(issueStr)
        messenger.send('newIssueOut')
        self.notify.info('latestIssue=%s' % self.latestIssue)
        pass

    def getLatestIssueStr(self):
        """We normally get this once, we could get this when a new issue is released while logged in."""
        assert self.notify.debugStateCall(self)
        # why are we here
        pass    

    def getLatestIssue(self):
        """Return the latest issue as coming from the uberdog server."""
        return self.latestIssue
