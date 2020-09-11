#-------------------------------------------------------------------------------
# Contact: Shawn Patton, Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: Sep 2008
#
# Purpose: DistributedPartyActivityAI is the base class for all party activities.
#          It loads up the sign and lever (where applicable)
#-------------------------------------------------------------------------------
from direct.distributed import DistributedObjectAI

from toontown.parties import PartyGlobals

class DistributedPartyActivityAI(DistributedObjectAI.DistributedObjectAI):
    """
    This is the base class for all Distributed Party Activities on the AI. A distributed
    party activity constitutes of any game or area at a party that involves multiple toons
    interacting with it at the same time.
    
    Note that a new notify category is not created here as this class expects
    subclasses to create it.
    """
    
    def __init__(self, air, partyDoId, x, y, h, activityId, activityType):
        """
        x, y and h are in Panda space, not Party Grid space.
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.partyDoId = partyDoId
        self.party = self.air.doId2do.get(partyDoId)
        self.x = x
        self.y = y
        self.h = h
        self.activityId = activityId
        self.activityName = PartyGlobals.ActivityIds.getString(self.activityId)
        self.activityType = activityType

        # Actual avatars that will play the activity
        self.toonIds = []
        self.toonIdsToJellybeanRewards = {}
        self.toonId2joinTime = {}

#-------------------------------------------------------------------------------
# join/exit functions that subclasses should override
#-------------------------------------------------------------------------------
    def toonJoinRequest(self):
        """
        Clients call this over the wire when they want to join/start this
        activity. Subclasses should override this and call sendToonJoinResponse.
        """
        self.notify.error("BASE: toonJoinRequest should be overridden")


    def toonExitRequest(self):
        """
        Clients call this over the wire when they want to exit this
        activity, but need AI server permission to do so.
        Subclasses should override this and call sendToonExitResponse.
        """
        self.notify.error("BASE: toonExitRequest should be overridden")
    
    
    def toonReady(self):
        """
        Clients call this over the wire when they are done reading the rules
        and are ready to play the activity. Subclasses should override this.
        """
        self.notify.error("BASE: toonReady should be overridden")

#-------------------------------------------------------------------------------
    
    def toonExitDemand(self):
        """
        Clients call this over the wire to inform the server that the sender
        has left the activity. Use this for activities where server permission
        is not required for leaving the activity.
        
        A default implementation is provided, which may be extended or
        overridden by subclasses. 
        """
        senderId = self.air.getAvatarIdFromSender()
        self.sendToonExitResponse(senderId, True)
        
        
    def sendToonJoinResponse(self, toonId, joined, denialReason=PartyGlobals.DenialReasons.Default):
        """
        Subclasses should call this in response to recieving a toonJoinRequest
        call.
        
        Parameters:
            toonId- id of the avatar that is being accepted/rejected
            joined- True if the avatar can join this activity, False otherwise
        """
        if joined:
            self._addToon(toonId)
            self.sendUpdate("setToonsPlaying", [self.toonIds])
        else:
            self.sendUpdateToAvatarId(toonId, "joinRequestDenied", [denialReason])
    
    
    def sendToonExitResponse(self, toonId, exited, denialReason=PartyGlobals.DenialReasons.Default):
        """
        Broadcast to all clients whether or not this toonId has left the activity.
        Subclasses should call this in response to recieving a toonExitRequest
        call.
        Parameters:
            toonId- id of the avatar that made the request to exit
            exited- True if the avatar exited this activity, False otherwise
        """
        if exited:
            self._removeToon(toonId)
            self.sendUpdate("setToonsPlaying", [self.toonIds])
        else:
            self.sendUpdateToAvatarId(toonId, "exitRequestDenied", [denialReason])

    
    def isToonPlaying(self, toonId):
        return(toonId in self.toonIds)
    
    
    def removeAllToons(self):
        """
        Base classes should call this when an activity is over and all toons
        should exit.
        """
        self.notify.debug("BASE: removeAllToons %s" % self.toonIds)
        while len(self.toonIds):
            self._removeToon(self.toonIds[0])
        self.sendUpdate("setToonsPlaying", [self.toonIds])
        

    def _addToon(self, toonId):
        """
        Utility function for adding an avatar to the list of playing avatars.
        This call should be the only way you add an toonId to self.toonIds.
        """
        self.notify.debug("BASE: _addToon( toonId=%s )" % toonId)
        if toonId in self.toonIds:
            self.notify.warning("BASE: attempt to add toonId (%s) failed as it was already in self.toonIds" % toonId)
        else:
            self.toonIds.append(toonId)
            self.toonId2joinTime[toonId] = globalClock.getFrameTime()
            # listen for this avatar's exit event
            self.acceptOnce(
                self.air.getAvatarExitEvent(toonId),
                self._handleUnexpectedToonExit,
                extraArgs=[toonId],
            )
    
    
    def _handleUnexpectedToonExit(self, toonId):
        """
        An avatar bailed out because he lost his connection or quit
        unexpectedly. Sub-classes may need to extend this function.
        """
        self.notify.debug("BASE: _handleUnexpectedToonExit( toonId=%s )" % toonId)
        # bypass any subclass checks and let clients know the toon has left the
        # activity
        self._removeToon(toonId)
        self.sendUpdate("setToonsPlaying", [self.toonIds])

    
    def _removeToon(self, toonId):
        """
        Utility function for removing an avatar from the list of playing avatars.
        This call should be the only way you remove an toonId from
        self.toonIds.
        """
        self.notify.debug("BASE: _removeToon( toonId=%s )" % toonId)
        if toonId not in self.toonIds:
            self.notify.warning("BASE: attempt to remove toonId (%s) failed as it was not in toonIds" % toonId)
        else:
            self.toonIds.remove(toonId)
            del self.toonId2joinTime[toonId]
            # stop listening for this avatar's exit event
            self.ignore(self.air.getAvatarExitEvent(toonId))
            # don't delete scores here, as we may want to display score info
            # for dropped players.
            
    
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)
        self.notify.debug("BASE: generate")
        
        
    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.notify.debug("BASE: announceGenerate")
        

    def delete(self):
        self.notify.debug("BASE: delete: deleting AI PartyActivity object")
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)


    def getPartyDoId(self):
        return self.partyDoId
        
        
    def getX(self):
        return self.x


    def getY(self):
        return self.y


    def getH(self):
        return self.h


    def issueJellybeanRewards(self):
        """
        Give the participating toons their jellybean reward.
        """
        now = globalClock.getFrameTime()
        while len(self.toonIdsToJellybeanRewards):
            self.issueJellybeanRewardToToonId(self.toonIdsToJellybeanRewards.keys()[0], now=now)
                
    def issueJellybeanRewardToToonId(self, toonId, now=None):
        """
        Give a specific toon a their jellybean reward.
        """
        if self.toonIdsToJellybeanRewards.has_key(toonId):
            if now is None:
                now = globalClock.getFrameTime()
            reward = self.toonIdsToJellybeanRewards[toonId]
            timePlayed = now - self.toonId2joinTime[toonId]
            # reset 'joined' time to now, in case we give this toon another reward
            self.toonId2joinTime[toonId] = now
            self.__issueJellybeanReward(toonId, reward, timePlayed)
            del self.toonIdsToJellybeanRewards[toonId]
            
    def __issueJellybeanReward(self, toonId, reward, timePlayed):
        """
        Issue a toon a jellybean reward.
        """
        # some activities, like Party Catch, can be left before it is over,
        # so we do not check whether the toonId is in the list of toons in
        # the activity.
        toon = self.air.doId2do.get(toonId)
        if toon is not None:
            self.notify.debug("rewarding %d jellybeans to %s" %(reward, toon.getName()))
            toon.addMoney(reward)
            self.air.writeServerEvent("party_reward", toonId, "%d|%d|%d" % (self.activityId, reward, timePlayed))

    def isInActivity(self, avId):
        """Return true if the avId is busy with us."""
        result = False
        if avId in self.toonIds:
            result = True
        return result


