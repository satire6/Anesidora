#-------------------------------------------------------------------------------
# Contact: Jason Pratt
# Created: Oct 2008
#
# Purpose: AI for DistributedPartyTrampolineActivity.
#-------------------------------------------------------------------------------

from direct.task import Task
from direct.distributed import ClockDelta
from toontown.toonbase import ToontownGlobals
from toontown.parties import PartyGlobals
from toontown.ai.ToonBarrier import ToonBarrier
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.activityFSMs import TrampolineActivityFSM
from toontown.toonbase import TTLocalizer

class DistributedPartyTrampolineActivityAI(DistributedPartyActivityAI):
    notify = directNotify.newCategory("DistributedPartyTrampolineActivityAI")

    def __init__(self, air, partyDoId, x, y, h, actId=PartyGlobals.ActivityIds.PartyTrampoline):
        DistributedPartyActivityAI.__init__(self, air, partyDoId, x, y, h, actId, PartyGlobals.ActivityTypes.GuestInitiated)

        self.activityFSM = TrampolineActivityFSM(self)
        # bestHeightInfo is a tuple of toon's name and their height
        self.bestHeightInfo = ("", 0)
        self.accept("NewBestHeightInfo", self.newBestHeightInfo)
        
    def generate(self):
        DistributedPartyTrampolineActivityAI.notify.debug("generate")
        self.activityFSM.request("Idle")

    def toonJoinRequest(self):
        DistributedPartyTrampolineActivityAI.notify.debug("toonJoinRequest")
        senderId = self.air.getAvatarIdFromSender()
        if (self.activityFSM.state == "Idle") and (len(self.toonIds) == 0) and not self.party.isInActivity(senderId):
            self.sendToonJoinResponse(senderId, True)
            self.activityFSM.request("Rules")
        else:
            self.sendToonJoinResponse(senderId, False)

    def toonReady(self):
        DistributedPartyTrampolineActivityAI.notify.debug("toonReady")
        senderId = self.air.getAvatarIdFromSender()
        if (self.activityFSM.state == "Rules") and (senderId in self.toonIds):
            self.activityFSM.request("Active")
        else:
            self.air.writeServerEvent("suspicious", senderId, "trampoline state not Rules or senderId not in toonIdsPlaying, in toonReady")

    def toonExitDemand(self):
        DistributedPartyTrampolineActivityAI.notify.debug("toonExitDemand")
        senderId = self.air.getAvatarIdFromSender()
        if (self.activityFSM.state == "Active") and (senderId in self.toonIds):
            self.activityFSM.request("Idle")

    def _handleUnexpectedToonExit(self, toonId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly.
        """
        DistributedPartyTrampolineActivityAI.notify.debug("_handleUnexpectedToonExit( toonId=%s )" % toonId)
        self.activityFSM.request("Idle")
        DistributedPartyActivityAI._handleUnexpectedToonExit(self, toonId)

    def reportHeightInformation(self, height):
        if height > self.bestHeightInfo[1]:
            senderId = self.air.getAvatarIdFromSender()
            sender = self.air.doId2do[senderId]
            messenger.send("NewBestHeightInfo", [sender.getName(), height])
    
    def newBestHeightInfo(self, toonName, height):
        self.bestHeightInfo = (toonName, height)
        self.sendUpdate("setBestHeightInfo", [toonName, height])

    def getBestHeightInfo(self):
        return self.bestHeightInfo

    def awardBeans(self, numBeansCollected, topHeight):
        senderId = self.air.getAvatarIdFromSender()
        
        if numBeansCollected > PartyGlobals.TrampolineNumJellyBeans:
            self.air.writeServerEvent("suspicious", senderId, "Player claims to have collected more jelly beans (%d) than possible." % numBeansCollected)
        else:
            numWon = numBeansCollected
            if numWon == PartyGlobals.TrampolineNumJellyBeans:
                numWon += PartyGlobals.TrampolineJellyBeanBonus
                if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_DAY):
                    numWon *= PartyGlobals.JellyBeanDayMultiplier
                resultsMessage = TTLocalizer.PartyTrampolineBonusBeanResults % (numBeansCollected, PartyGlobals.TrampolineJellyBeanBonus)
            else:
                if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_DAY):
                    numWon *= PartyGlobals.JellyBeanDayMultiplier
                resultsMessage = TTLocalizer.PartyTrampolineBeanResults % numBeansCollected
            resultsMessage += "\n\n" + TTLocalizer.PartyTrampolineTopHeightResults % topHeight
        
        self.toonIdsToJellybeanRewards = {senderId : numWon}
        self.sendUpdateToAvatarId(senderId, "showJellybeanReward", [numWon, self.air.doId2do[senderId].getMoney(), resultsMessage])
        # since we send the toon's current money in showJellybeanReward, that needs to happen before issueJellybeanRewards
        self.issueJellybeanRewards()

    def requestAnim(self, request):
        self.sendUpdate("requestAnimEcho", [request])

    def removeBeans(self, beansToRemove):
        self.sendUpdate("removeBeansEcho", [beansToRemove])

    def sessionOver(self, task):
        """
        Time is up. Kick the toon off the trampoline.
        """
        DistributedPartyTrampolineActivityAI.notify.debug("sessionOver")
        self.sendUpdate("leaveTrampoline")
        return Task.done

    # FSM transition methods
    def startIdle(self):
        DistributedPartyTrampolineActivityAI.notify.debug("startIdle")
        # remove active toon
        if len( self.toonIds ) > 0:
            self.removeAllToons()
        # put clients into this state
        self.sendUpdate( "setState", ["Idle", # new state
                                       0] ) # dummy timestamp

    def finishIdle(self):
        DistributedPartyTrampolineActivityAI.notify.debug("finishIdle")

    def startRules(self):
        DistributedPartyTrampolineActivityAI.notify.debug("startRules")
        # we do not explicitly tell clients to enter this state as the
        # toonJoinResponse will prompt that change on the clients

    def finishRules(self):
        DistributedPartyTrampolineActivityAI.notify.debug("finishRules")

    def startActive(self):
        DistributedPartyTrampolineActivityAI.notify.debug("startActive")
        # put clients into this state
        self.sendUpdate( "setState", ["Active", # new state
                                      ClockDelta.globalClockDelta.getRealNetworkTime()] ) # start time
        
        # setup to transition to Disabled after time is up
        taskMgr.doMethodLater(
            PartyGlobals.TrampolineDuration,
            self.sessionOver,
            self.taskName("waitForSessionOver"),
        )

    def finishActive(self):
        DistributedPartyTrampolineActivityAI.notify.debug("finishActive")
        # clean up doMethodLater
        taskMgr.removeTasksMatching(self.taskName("waitForSessionOver"))
        
    def delete(self):
        del self.activityFSM
        self.ignore("NewBestHeightInfo")
        DistributedPartyActivityAI.delete(self)
