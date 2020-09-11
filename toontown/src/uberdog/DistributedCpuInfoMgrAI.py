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
class DistributedCpuInfoMgrAI(ParentClass ):
    """
    Uberdog object that keeps track of the last time in game news has been updated
    """
    notify = directNotify.newCategory('DistributedInGameNewsMgrAI')


    def __init__(self, cr):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        ParentClass.__init__(self, cr)
        self.latestIssueStr = ""
        self.avId2Fingerprint = {}
        self.accept("avatarEntered", self.handleAvatarEntered) 

    def generate(self):
        """We have zone info but not required fields, register for the special."""
        # IN_GAME_NEWS_MGR_UD_TO_ALL_AI will arrive on this channel
        self.air.registerForChannel(OtpDoGlobals.OTP_DO_ID_TOONTOWN_CPU_INFO_MANAGER)
        ParentClass.generate(self)

    def announceGenerate(self):
        # tell uberdog we are starting up, so we can get info on the currently running public parties
        # do whatever other sanity checks is necessary here
        DistributedObjectAI.announceGenerate(self)
        #self.air.sendUpdateToDoId("DistributedInGameNewsMgr",
        #                          'inGameNewsMgrAIStartingUp',
        #                          OtpDoGlobals.OTP_DO_ID_TOONTOWN_CPU_INFO_MANAGER,
        #                           [self.doId, self.air.districtId]
        #)
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
        
    def sendCpuInfoToUd(self, info, fingerprint):
        """Prepare to send the info to the UD, we don't have the DISLid yet.""" 
        requesterId = self.air.getAvatarIdFromSender()
        self.avId2Fingerprint[requesterId] = (info,fingerprint)
         
    def handleAvatarEntered(self, avatar):
        """Send the cpu info to the UD once we get the avatar and the DISL id."""
        if avatar.doId in self.avId2Fingerprint:            
            info, fingerprint = self.avId2Fingerprint.get(avatar.doId)            
            dislId = 0
            if avatar:
                try:
                    dislId = avatar.DISLid
                except:
                    pass
            if dislId:
                self.air.sendUpdateToDoId("DistributedCpuInfoMgr",
                                      'setCpuInfoToUd',
                                      OtpDoGlobals.OTP_DO_ID_TOONTOWN_CPU_INFO_MANAGER,
                                      [avatar.doId, dislId, info[:255],fingerprint[:255]]
                                  )
            else:
                self.notify.warning("avId=%s has dislId=%s" % (avatar.doId, dislId))
            del self.avId2Fingerprint[avatar.doId]
 
