import socket
import datetime
import os
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.http.WebRequest import WebRequestDispatcher
from otp.distributed import OtpDoGlobals
from toontown.toonbase import ToontownGlobals
from toontown.uberdog import InGameNewsResponses

ParentClass = DistributedObjectAI
#ParentClass = DistributedObjectGlobal
class DistributedInGameNewsMgrAI(ParentClass ):
    """
    Uberdog object that keeps track of the last time in game news has been updated
    """
    notify = directNotify.newCategory('DistributedInGameNewsMgrAI')


    def __init__(self, cr):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        ParentClass.__init__(self, cr)
        self.latestIssueStr = ""

    def generate(self):
        """We have zone info but not required fields, register for the special."""
        # IN_GAME_NEWS_MGR_UD_TO_ALL_AI will arrive on this channel
        self.air.registerForChannel(OtpDoGlobals.OTP_DO_ID_TOONTOWN_IN_GAME_NEWS_MANAGER)
        ParentClass.generate(self)

    def announceGenerate(self):
        # tell uberdog we are starting up, so we can get info on the currently running public parties
        # do whatever other sanity checks is necessary here
        DistributedObjectAI.announceGenerate(self)
        self.air.sendUpdateToDoId("DistributedInGameNewsMgr",
                                  'inGameNewsMgrAIStartingUp',
                                  OtpDoGlobals.OTP_DO_ID_TOONTOWN_IN_GAME_NEWS_MANAGER,
                                   [self.doId, self.air.districtId]
                                  )
    def setLatestIssueStr(self, issueStr):
        """We normally get this once, we could get this when a new issue is released while logged in."""
        # we receive this as a utc str
        assert self.notify.debugStateCall(self)
        self.latestIssueStr = issueStr
        pass

    def b_setLatestIssueStr(self, latestIssue):
        self.setLatestIssueStr(latestIssue)
        self.d_setLatestIssueStr(latestIssue)
        
    def d_setLatestIssueStr(self, latestIssue):
        self.sendUpdate("setLatestIssueStr",[self.getLatestIssueStr()])
        

    def getLatestIssueStr(self):
        """We normally get this once, we could get this when a new issue is released while logged in."""
        assert self.notify.debugStateCall(self)
        return self.latestIssueStr
        pass
    

    def newIssueUDtoAI(self, issueStr):
        """Well the UD is telling us we have a new issue, spread it to the clients."""
        self.b_setLatestIssueStr(issueStr)
        
