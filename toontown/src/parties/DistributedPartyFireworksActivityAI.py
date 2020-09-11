#-------------------------------------------------------------------------------
# Contact: Rob Gordon
# Created: Oct 2008
#
# Purpose: AI control of fireworks in a party.
#
#-------------------------------------------------------------------------------

# Panda imports
from direct.distributed import ClockDelta
from direct.task import Task

# Toontown imports
from toontown.effects.FireworkShow import FireworkShow

# parties imports
import PartyGlobals
from DistributedPartyActivityAI import DistributedPartyActivityAI
from activityFSMs import FireworksActivityFSM

class DistributedPartyFireworksActivityAI(DistributedPartyActivityAI):

    notify = directNotify.newCategory("DistributedPartyFireworksActivityAI")
    
    def __init__(self, air, partyDoId, x, y, h, eventId=PartyGlobals.FireworkShows.Summer, showStyle=0):
        """
        air: instance of ToontownAIRepository
        eventId: a PartyGlobals.FireworkShows value that tells us which show
                 to run
        """
        DistributedPartyFireworksActivityAI.notify.debug("__init__")
        DistributedPartyActivityAI.__init__(
            self,
            air,
            partyDoId,
            x,
            y,
            h,
            PartyGlobals.ActivityIds.PartyFireworks,
            PartyGlobals.ActivityTypes.HostInitiated,
        )
        self.eventId = eventId
        self.showStyle = showStyle
        self.activityFSM = FireworksActivityFSM(self)
    
    def generate(self):
        DistributedPartyFireworksActivityAI.notify.debug("generate")
        self.activityFSM.request("Idle")
        
    def getEventId(self):
        DistributedPartyFireworksActivityAI.notify.debug("getEventId")
        return self.eventId
    
    def getShowStyle(self):
        DistributedPartyFireworksActivityAI.notify.debug("getShowStyle")
        return self.showStyle
    
    def toonJoinRequest(self):
        """
        The supposed host is requesting the fireworks to start.
        """
        # check that the host sent this message
        senderId = self.air.getAvatarIdFromSender()
        if senderId != self.party.partyInfo.hostId:
            self.air.writeServerEvent('suspicious', senderId, 'A non-host with avId=%d tried to start a host activated activity.' % senderId)
            return
        self.activityFSM.request("Active")
    
    def showComplete(self, task):
        DistributedPartyFireworksActivityAI.notify.debug("showComplete")
        self.activityFSM.request("Disabled")
        
        return Task.done
        
    def delete(self):
        DistributedPartyFireworksActivityAI.notify.debug("delete")
        if hasattr(self, 'activityFSM'):
            self.activityFSM.request('Disabled')
            del self.activityFSM
        DistributedPartyActivityAI.delete(self)
    
    # FSM transition methods
    def startIdle(self):
        DistributedPartyFireworksActivityAI.notify.debug("startIdle")
    
    def finishIdle(self):
        DistributedPartyFireworksActivityAI.notify.debug("finishIdle")
        
    def startActive(self):
        DistributedPartyFireworksActivityAI.notify.debug("startActive")
        messenger.send( PartyGlobals.FireworksStartedEvent )
        showStartTimestamp = ClockDelta.globalClockDelta.getRealNetworkTime()
        # put clients into this state
        self.sendUpdate(
            "setState",
            [
                "Active", # new state
                showStartTimestamp # when the show starts
            ]
        )
        # setup to transition to Disabled after the show is over
        throwAwayShow = FireworkShow()
        showDuration = throwAwayShow.getShowDuration( self.eventId)
        showDuration += 20.0
        taskMgr.doMethodLater(
            PartyGlobals.FireworksPostLaunchDelay + showDuration + PartyGlobals.FireworksTransitionToDisabledDelay,
            self.showComplete,
            self.taskName("waitForShowComplete"),
        )
        del throwAwayShow
        
    def finishActive(self):
        DistributedPartyFireworksActivityAI.notify.debug("finishActive")
        messenger.send( PartyGlobals.FireworksFinishedEvent )
        # clean up doMethodLater
        taskMgr.removeTasksMatching(self.taskName("waitForShowComplete"))
        
    def startDisabled(self):
        DistributedPartyFireworksActivityAI.notify.debug("startDisabled")
        # put clients into this state
        self.sendUpdate(
            "setState",
            [
                "Disabled", # new state
                0 # dummy timestamp
            ]
        )
    
    def finishDisabled(self):
        DistributedPartyFireworksActivityAI.notify.debug("finishDisabled")
    