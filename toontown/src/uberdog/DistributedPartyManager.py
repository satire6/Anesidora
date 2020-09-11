from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

from pandac.PandaModules import CFSpeech, CFTimeout

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonDNA

from toontown.parties import PartyGlobals

class DistributedPartyManager(DistributedObject):
    neverDisable = 1

    notify = directNotify.newCategory("DistributedPartyManager")
    
    def __init__(self,cr):
        """Construct ourself."""
        DistributedObject.__init__(self, cr)
        base.cr.partyManager = self
        self.allowUnreleased= False
        self.partyPlannerStyle = None
        self.partyPlannerName = None
        self.showDoid = False

    def delete(self):
        """Delete ourself."""
        DistributedObject.delete(self)
        self.cr.partyManager = None
        
    def disable(self):
        self.notify.debug( "i'm disabling DistributedPartyManager rightnow.")
        self.ignore("deallocateZoneIdFromPlannedParty")
        self.ignoreAll() # catch requestPartyZoneComplete
        DistributedObject.disable(self)
        
    def generate(self):
        # Called when the client loads
        self.notify.debug("BASE: generate")
        DistributedObject.generate(self)

        # listen for requests
        self.accept("deallocateZoneIdFromPlannedParty", self.deallocateZoneIdFromPlannedParty)
        
        # listen for the generate event, which will be thrown after the
        # required fields are filled in
        self.announceGenerateName = self.uniqueName("generate")
    
    def deallocateZoneIdFromPlannedParty(self, zoneId):
        self.sendUpdate("freeZoneIdFromPlannedParty", [base.localAvatar.doId, zoneId])
    
#===============================================================================
# Party Creation Methods
#===============================================================================

    def allowUnreleasedClient(self):
        """Return do we allow player to buy unreleased activities and decorations on the client."""
        return self.allowUnreleased
        
    def setAllowUnreleaseClient(self, newValue):
        """Set if we allow player to buy unreleased activities and decorations on the client."""
        self.allowUnreleased = newValue

    def toggleAllowUnreleasedClient(self):
        """Toggle allow unreleased on the client, then return the new value."""
        self.allowUnreleased = not self.allowUnreleased
        return self.allowUnreleased
    
    def sendAddParty(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        """Add a new party."""
        #self.sendHello('resr')
        self.sendUpdate('addPartyRequest', [hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, inviteeIds])

    def addPartyResponse (self, hostId, errorCode):
        """Handle being told by AI or uberdog the result of our add party request."""
        # Tell the party planning gui if the add party succeeded or not.
        messenger.send("addPartyResponseReceived", [hostId, errorCode])
        if hasattr(base.localAvatar, "creatingNewPartyWithMagicWord"):
            if base.localAvatar.creatingNewPartyWithMagicWord:
                base.localAvatar.creatingNewPartyWithMagicWord = False
                if errorCode == PartyGlobals.AddPartyErrorCode.AllOk:
                    base.localAvatar.setChatAbsolute("New party entered into database successfully.", CFSpeech | CFTimeout)
                else:
                    base.localAvatar.setChatAbsolute("New party creation failed : %s" % PartyGlobals.AddPartyErrorCode.getString(errorCode), CFSpeech | CFTimeout)
        
        assert self.notify.debugStateCall()

#===============================================================================
# Active Party Management
#===============================================================================

    # Fullfill client request for partyZone
    def requestPartyZone(self, avId, zoneId, callback):
        assert(self.notify.debug("requestPartyZone : avId=%s zoneId=%s" % (avId, zoneId)))
        if zoneId < 0:
            zoneId = 0
        self.acceptOnce("requestPartyZoneComplete", callback)
        # If we're about to plan a party, we want to sell the AI about it
        if hasattr(base.localAvatar, "aboutToPlanParty"):
            if base.localAvatar.aboutToPlanParty:
                self.sendUpdate("getPartyZone", [avId, zoneId, True])
                return
        self.sendUpdate("getPartyZone", [avId, zoneId, False])

    # The AI is telling us the zone for the party this avatar wants to go to
    def receivePartyZone(self, hostId, partyId, zoneId):    
        assert(self.notify.debug("receivePartyZone(%d, %d, %d)" % (hostId, partyId, zoneId)))
        if partyId != 0 and zoneId != 0:
            if base.localAvatar.doId == hostId:
                # We're really starting a party here, disable our go button
                for partyInfo in base.localAvatar.hostedParties:
                    if partyInfo.partyId == partyId:
                        partyInfo.status == PartyGlobals.PartyStatus.Started
                
        messenger.send("requestPartyZoneComplete", [hostId, partyId, zoneId])

    def sendChangePrivateRequest(self, partyId, newPrivateStatus):
        """Request AI to change the party to either private or public."""
        self.sendUpdate('changePrivateRequest', [partyId, newPrivateStatus])

    def changePrivateResponse(self, partyId, newPrivateStatus, errorCode):
        """Handle the response to our request to change private status."""
        if errorCode == PartyGlobals.ChangePartyFieldErrorCode.AllOk:
            # TODO Schell games give feed back to user it was a success
            self.notify.info("succesfully changed private field for the party")
            for partyInfo in localAvatar.hostedParties:
                if partyInfo.partyId == partyId:
                    partyInfo.isPrivate = newPrivateStatus
            # Send this to other hooks on the client side (AFTER updating partyinfo)
            messenger.send("changePartyPrivateResponseReceived", [partyId, newPrivateStatus, errorCode])
        else:
            # Send this to other hooks on the client side (AFTER updating partyinfo)
            messenger.send("changePartyPrivateResponseReceived", [partyId, newPrivateStatus, errorCode])            
            self.notify.info("FAILED changing private field for the party")


    def sendChangePartyStatusRequest(self, partyId, newPartyStatus):
        """Request AI to change the party status."""
        self.sendUpdate('changePartyStatusRequest', [partyId, newPartyStatus])

    def changePartyStatusResponse(self, partyId, newPartyStatus, errorCode, beansRefunded):
        """
        Handle the response to our request to change the party status.
        Only the host gets this.
        """
        self.notify.debug( "changePartyStatusResponse : partyId=%s newPartyStatus=%s errorCode=%s"%(partyId, newPartyStatus, errorCode))
        for partyInfo in localAvatar.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = newPartyStatus
        # Send this to other hooks on the client side (AFTER updating partyinfo)
        messenger.send("changePartyStatusResponseReceived", [partyId, newPartyStatus, errorCode, beansRefunded])

    def sendAvToPlayground(self, avId, retCode):
        assert(self.notify.debug("sendAvToPlayground: %d" % avId))        
        messenger.send(PartyGlobals.KICK_TO_PLAYGROUND_EVENT, [retCode])        
        self.notify.debug("sendAvToPlayground: %d" % avId)

    def leaveParty(self):
        if self.isDisabled():
            self.notify.warning("DistributedPartyManager disabled; unable to leave party.")
            return
        # Tell AI I want outta here
        self.sendUpdate("exitParty",[localAvatar.zoneId])
        
    def removeGuest(self, ownerId, avId):
        self.notify.debug("removeGuest ownerId = %s, avId = %s" % (ownerId, avId))
        # The party owner is removing avId from his party.
        # Notify the AI, and kick the ex-friend out of the party
        self.sendUpdate("removeGuest", [ownerId, avId])
        
    # TODO-parties: Do checks based on the rules about going to the party:
    def isToonAllowedAtParty(self, avId, partyId):
        return PartyGlobals.GoToPartyStatus.AllowedToGo
    
    # TODO-parties: Add TTLocalized reasons based on GoToPartyStatus Enum
    def getGoToPartyFailedMessage(self, reason):
        return ""

    def sendAvatarToParty(self, hostId):
        """
        This is a guest of a party or a host of an already started party asking
        to be sent to the party.  We'll ask the server for the shardId and
        zoneId and then send the avatar to the party.
        """
        DistributedPartyManager.notify.debug("sendAvatarToParty hostId = %s" % hostId)
        self.sendUpdate("requestShardIdZoneIdForHostId", [hostId])

    def sendShardIdZoneIdToAvatar(self, shardId, zoneId):
        """
        We've received the shardId and the zoneId of a party the local avatar
        wants to go to, send them there.
        """
        DistributedPartyManager.notify.debug("sendShardIdZoneIdToAvatar shardId = %s  zoneId = %s" % (shardId, zoneId))
        if shardId == 0 or zoneId == 0:
            base.cr.playGame.getPlace().handleBookClose()
            return
        hoodId = ToontownGlobals.PartyHood
        if shardId == base.localAvatar.defaultShard:
            shardId = None
        base.cr.playGame.getPlace().requestLeave({
            "loader": "safeZoneLoader",
            "where": "party",
            "how" : "teleportIn",
            "hoodId" : hoodId,
            "zoneId" : zoneId,
            "shardId" : shardId,
            "avId" : -1,
        })
        
    def setPartyPlannerStyle(self, dna):
        self.partyPlannerStyle = dna
        
    def getPartyPlannerStyle(self):
        if self.partyPlannerStyle:
            return self.partyPlannerStyle
        else:
            dna = ToonDNA.ToonDNA()
            dna.newToonRandom()
            return dna
        
    def setPartyPlannerName(self, name):
        self.partyPlannerName = name
        
    def getPartyPlannerName(self):
        if self.partyPlannerName:
            return self.partyPlannerName
        else:
            return TTLocalizer.PartyPlannerGenericName

    def toggleShowDoid(self):
        """Toggle allow unreleased on the client, then return the new value."""
        self.showDoid = not self.showDoid
        return self.showDoid    

    def getShowDoid(self):
        """Return do we allow player to buy unreleased activities and decorations on the client."""
        return self.showDoid 
        
