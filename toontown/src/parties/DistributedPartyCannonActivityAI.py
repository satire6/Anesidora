#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Sep 2008
#
# Purpose: DistributedPartyCannonActivityAI handles the creation of AI Dist. Cannons
#          as well as keeping track of which toons are currently flying, including
#          cleanup of those toons. It also listens for when a DCannonAI is lit,
#          so that it can be set to fire on the client side.
#-------------------------------------------------------------------------------

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.parties.DistributedPartyActivityAI import DistributedPartyActivityAI
from toontown.parties.DistributedPartyCannonAI import DistributedPartyCannonAI
from toontown.parties import PartyGlobals

class DistributedPartyCannonActivityAI(DistributedPartyActivityAI):
    notify = directNotify.newCategory("DistributedPartyCannonActivityAI")
    #notify.setDebug(True)

    def __init__(self, air, partyDoId, x, y, h):
        DistributedPartyActivityAI.__init__(self, air, partyDoId, x, y, h, PartyGlobals.ActivityIds.PartyCannon, PartyGlobals.ActivityTypes.Continuous)

        # map of cannons by cannon doId
        self.cannons = {}
        # map of flying toon doIds to firing cannons doIds
        self.flyingToons = {}
        self.flyingToonCloudsHit = {}
        self.toonIdsToJellybeanRewards = {}
        
        # Map of cloudNumber to rgb info
        self.cloudColors = {}

    def announceGenerate(self):
        DistributedPartyActivityAI.announceGenerate(self)
        self.__initCannons()

    def __initCannons(self):
        """
        Initialize Cannon AI instances
        """
        # create the first cannon. Subsequent cannons will be created through
        # spawnCannonAt called from the partyAI itself.
        self.spawnCannonAt(self.x, self.y, self.h)

        # Listen for when a party cannon has been lit
        self.accept(DistributedPartyCannonAI.CANNON_LIT_EVENT, self.__handleFireCannon)
        

    def spawnCannonAt(self, x, y, h):
        cannon = DistributedPartyCannonAI(self.air, self.doId, x, y, 0, h, 0, 0)
        cannon.generateWithRequired(self.zoneId)
        self.cannons[cannon.doId] = cannon
        
    def delete(self):
        self.ignoreAll()
        for cannon in self.cannons.values():
            cannon.requestDelete()
        self.cannons.clear()
        self.flyingToons.clear()
        self.flyingToonCloudsHit.clear()
        self.toonIdsToJellybeanRewards.clear()
        DistributedPartyActivityAI.delete(self)
               
    def __handleFireCannon(self, cannonId, timeEnteredCannon):
        """
        Event handler triggered when a cannon is "lit"
        Sets cannon to fire
        """
        # Confirm that cannon is lit, otherwise ignore and report suspicious behavior
        if self.cannons.has_key(cannonId) and self.cannons[cannonId].isReadyToFire():
            cannon = self.cannons[cannonId]
            toonId = cannon.getToonInsideId()
            
            if toonId and not self.flyingToons.has_key(toonId):
                self.flyingToons[toonId] = cannon.doId
                self.flyingToonCloudsHit[toonId] = 0
                self.toonIdsToJellybeanRewards[toonId] = 0
                self._addToon(toonId)
                # we override toonId2Join times and start it from the time he entered the cannon
                self.notify.debug("changing join time from %s to %s" % (self.toonId2joinTime[toonId], timeEnteredCannon))
                self.toonId2joinTime[toonId] = timeEnteredCannon
            else:                
                self.notify.warning("Trying to fire toon %s who is already flying." % toonId)
                toonId = cannon.getToonInsideId()
                if toonId:
                    self.notify.warning("toon is still inside cannon, forcing him out")
                    cannon.forceInsideToonToExit()
                return

            self.d_setCannonWillFire(cannonId, cannon.rotation, cannon.angle)
        else:
            if self.cannons.has_key(cannonId):
                self.notify.warning("__handleFireCannon failed self.cannons[%d].isReadyToFire() = False" % cannonId)
                cannon = self.cannons[cannonId]
                toonId = cannon.getToonInsideId()
                if toonId:
                    self.notify.warning("Cannon is not lit, forcing him out")
                    cannon.forceInsideToonToExit()
            else:                
                self.notify.warning("__handleFireCannon failed self.cannons.has_key(%d) = False" % cannonId)
            
        # TODO: Write case for suspicious cannon lit call
        
    def _handleUnexpectedToonExit(self, toonId):
        """
        Flying toon client exits, request cleanup.
        """
        if self.flyingToons.has_key(toonId):
            self.notify.warning("Avatar %s has exited unexpectedly." % toonId)
            
            # cannon_movie_force_exit will clean up the avatar on the client
            # and eventually call setLanded to complete the cleanup on AI
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_FORCE_EXIT, toonId)
            self.__cleanupFlyingToon(toonId)
            DistributedPartyActivityAI._handleUnexpectedToonExit(self, toonId)
            
    def __cleanupFlyingToon(self, toonId):
        if self.flyingToons.has_key(toonId):
            self.ignore(self.air.getAvatarExitEvent(toonId))
            del self.flyingToons[toonId]
            del self.flyingToonCloudsHit[toonId]
            self._removeToon(toonId)
            if self.toonIdsToJellybeanRewards.has_key(toonId):
                del self.toonIdsToJellybeanRewards[toonId]
        
#===============================================================================
# Attributes
#===============================================================================

    # Distributed(clsend airecv)
    def cloudsColorRequest(self):
        self.notify.debug("cloudsColorRequest")
        senderId = self.air.getAvatarIdFromSender()
        cloudColorList = []
        for key, value in self.cloudColors.items():
            cloudColorList.append([key, value[0], value[1], value[2]])
            
        self.d_cloudsColorResponse(senderId, cloudColorList)
        
    def d_cloudsColorResponse(self, avId, cloudColorList):
        self.notify.debug("cloudsColorResponse %s" % cloudColorList)
        self.sendUpdateToAvatarId(avId, "cloudsColorResponse", [cloudColorList])
        
    # Distributed (airecv clsend)
    def requestCloudHit(self, cloudNumber, r, g, b):
        self.notify.debug("requestCloudHit %d (%d, %d, %d)" % (cloudNumber, r, g, b))
        senderId = self.air.getAvatarIdFromSender()
        
        if self.flyingToonCloudsHit.has_key(senderId):
            self.flyingToonCloudsHit[senderId] += 1
            addedJellyBeans = PartyGlobals.CannonJellyBeanReward
            if self.air.holidayManager.isHolidayRunning(ToontownGlobals.JELLYBEAN_DAY):
                addedJellyBeans *= 2
            self.toonIdsToJellybeanRewards[senderId] += addedJellyBeans
            if self.toonIdsToJellybeanRewards[senderId] > PartyGlobals.CannonMaxTotalReward:
                # put a cap so we don't go beyond uint8
                self.toonIdsToJellybeanRewards[senderId] = PartyGlobals.CannonMaxTotalReward
            
            
            self.cloudColors[cloudNumber] = (r, g, b)
            self.d_setCloudHit(cloudNumber, r, g, b)
        
    # Distributed (broadcast)
    def d_setCloudHit(self, cloudNumber, r, g, b):
        self.sendUpdate('setCloudHit', [cloudNumber, r, g, b])

    # Distributed (broadcast ram)
    def d_setMovie(self, mode, toonId):
        """
        Broadcasts movie (state) of activity to client
        """
        self.sendUpdate("setMovie", [mode, toonId])

    # Distributed (broadcast)
    def d_setCannonWillFire(self, cannonId, zRot, angle):
        """
        Broadcasts that a cannon is ready to fire a toon
        """
        self.sendUpdate("setCannonWillFire", [cannonId, zRot, angle])
        
    # Distributed (clsend airecv)
    def setLanded(self, toonId):
        """
        From the client, a toon has landed. Cleanup the toon and inform all clients.
        """
        self.notify.debug("%s setLanded %s" % (self.doId, toonId))
        if self.flyingToons.has_key(toonId):
            
            cloudsHit = self.flyingToonCloudsHit[toonId]
            if cloudsHit:
                jellybeansWon = self.toonIdsToJellybeanRewards[toonId]
                resultsMessage = TTLocalizer.PartyCannonResults % (jellybeansWon, cloudsHit)
                self.sendUpdateToAvatarId(
                    toonId,
                    "showJellybeanReward",
                    [jellybeansWon, self.air.doId2do[toonId].getMoney(), resultsMessage]
                    )
                self.issueJellybeanRewardToToonId(toonId)
            
            self.d_setMovie(PartyGlobals.CANNON_MOVIE_LANDED, toonId)
            self.__cleanupFlyingToon(toonId)

    def isInActivity(self, avId):
        """Return true if the avId is flying or inside a cannon."""
        result = False
        if avId in self.flyingToons:
            result = True
        else:
            for cannon in self.cannons.values():
                if cannon.getToonInsideId() == avId:
                    result = True
                    break;        
        return result
