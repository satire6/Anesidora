#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: DistributedPartyAI controls message passing to the client for parties
#
#-------------------------------------------------------------------------------
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.parties import PartyGlobals
from toontown.parties import PartyUtils

from toontown.parties.DistributedPartyJukeboxActivityAI import DistributedPartyJukeboxActivityAI
from toontown.parties.DistributedPartyCannonActivityAI import DistributedPartyCannonActivityAI
from toontown.parties.DistributedPartyTrampolineActivityAI import DistributedPartyTrampolineActivityAI
from toontown.parties.DistributedPartyVictoryTrampolineActivityAI import DistributedPartyVictoryTrampolineActivityAI
from toontown.parties.DistributedPartyCatchActivityAI import DistributedPartyCatchActivityAI
from toontown.parties.DistributedPartyDanceActivityAI import DistributedPartyDanceActivityAI
from toontown.parties.DistributedPartyTugOfWarActivityAI import DistributedPartyTugOfWarActivityAI
from toontown.parties.DistributedPartyFireworksActivityAI import DistributedPartyFireworksActivityAI
from toontown.parties.DistributedPartyJukebox40ActivityAI import DistributedPartyJukebox40ActivityAI
from toontown.parties.DistributedPartyDance20ActivityAI import DistributedPartyDance20ActivityAI
from toontown.parties.DistributedPartyCogActivityAI import DistributedPartyCogActivityAI

ActivityIdsToClasses = {
    PartyGlobals.ActivityIds.PartyJukebox : DistributedPartyJukeboxActivityAI,
    PartyGlobals.ActivityIds.PartyCannon : DistributedPartyCannonActivityAI,
    PartyGlobals.ActivityIds.PartyTrampoline : DistributedPartyTrampolineActivityAI,
    PartyGlobals.ActivityIds.PartyVictoryTrampoline : DistributedPartyVictoryTrampolineActivityAI,
    PartyGlobals.ActivityIds.PartyCatch : DistributedPartyCatchActivityAI,
    PartyGlobals.ActivityIds.PartyDance : DistributedPartyDanceActivityAI, 
    PartyGlobals.ActivityIds.PartyTugOfWar : DistributedPartyTugOfWarActivityAI,
    PartyGlobals.ActivityIds.PartyFireworks : DistributedPartyFireworksActivityAI,
    PartyGlobals.ActivityIds.PartyClock : None,
    PartyGlobals.ActivityIds.PartyJukebox40 : DistributedPartyJukebox40ActivityAI,
    PartyGlobals.ActivityIds.PartyDance20 : DistributedPartyDance20ActivityAI,
    PartyGlobals.ActivityIds.PartyCog : DistributedPartyCogActivityAI,
    }

class DistributedPartyAI(DistributedObjectAI):
    notify = directNotify.newCategory("DistributedPartyAI")

    def __init__(self, air, avId, zoneId, partyInfo, inviteeIds):
        DistributedObjectAI.__init__(self, air)

        self.notify.debug("created with avId = %s, zoneId = %s, and partyInfo=%s" % (avId, zoneId, partyInfo))
        self.avId = avId
        self.zoneId = zoneId
        self.partyInfo = partyInfo
        self.inviteeIds = inviteeIds
        self.partyStartedTime = self.air.toontownTimeManager.getCurServerDateTime()
        self.partyClockInfo = (0,0,0)
        
        # For the party clock, we need to set aside the x, y, and h
        for activity in self.partyInfo.activityList:
            if activity.activityId == PartyGlobals.ActivityIds.PartyClock:
                self.partyClockInfo = (activity.x, activity.y, activity.h)

        self.hostName = ""
        # try to get the host name at this point here
        toon = simbase.air.doId2do.get(self.partyInfo.hostId)
        if toon:
            self.hostName = toon.getName()            
                                                
        # Keep track of the parties state for toon's coming in to the party
        self.isPartyEnding = False
        self.activityObjects = []
                
    def getPartyState(self):    
        return self.isPartyEnding        
        
    def b_setPartyState(self, partyState):    
        self.isPartyEnding = partyState 
        self.sendUpdate("setPartyState", [partyState])       
    
    def generate(self):
        DistributedPartyAI.notify.debug("DistParty generate: %s" % self.doId)
        DistributedObjectAI.generate(self)

        self.air.writeServerEvent("party_generate",self.partyInfo.partyId, "%d|%d" % (self.doId,self.partyInfo.hostId))
        
        # Log that a GM party has been generated.
        try:
            host = simbase.air.doId2do.get(self.partyInfo.hostId)
            if host.hasGMName():
                self.air.writeServerEvent("party_generate_gm", self.partyInfo.partyId, "%s" % self.partyInfo.hostId)
                assert self.notify.debug("GM-%s's party has started." % self.partyInfo.hostId)
        except:
            pass

        # We want to initialize all the activities that are at this party.
        # We'll loop through the activityList and see if we can import, create,
        # and generate the relevant AI class.  This code assumes that the
        # activity classes are named according to the enum
        # PartyGlobals.ActivityIds
        # for example:
        #     PartyGlobals.ActivityIds.PartyCatch would load
        #     DistributedPartyCatchActivityAI
        for activity in self.partyInfo.activityList:
            # Location and heading in the activityList is in party space, so
            # we convert them to Panda space before passing them into the
            # activities
            #activityName = PartyGlobals.ActivityIds.getString(activity.activityId)
            x = PartyUtils.convertDistanceFromPartyGrid(activity.x, 0)
            y = PartyUtils.convertDistanceFromPartyGrid(activity.y, 1)
            h = PartyUtils.convertDegreesFromPartyGrid(activity.h)
            # Skip the party clock...
            if activity.activityId == PartyGlobals.ActivityIds.PartyClock:
                continue

            # Special case for cannon, add another cannon instead of creating
            # a new instance of the cannon activity
            if activity.activityId == PartyGlobals.ActivityIds.PartyCannon and \
               self.getCannonActivity():
                self.getCannonActivity().spawnCannonAt(x, y, h)
                continue

            actClass = ActivityIdsToClasses[activity.activityId]
            newAct = actClass(self.air, self.doId, x, y ,h)
            newAct.generateWithRequired(self.zoneId)
            self.activityObjects.append(newAct)
                
    def getCannonActivity(self):
        result = None
        for act in self.activityObjects:
            if "DistributedPartyCannonActivityAI" in str(act.__class__):
                result = act
                break
        return result

    def getPartyClockInfo(self):
        return self.partyClockInfo

    def getAvIdsAtParty(self):
        return self.air.partyManager.zoneIdToGuestAvIds[self.zoneId]

    def getPartyStartedTime(self):
        return self.partyStartedTime.strftime("%Y-%m-%d %H:%M:%S")

    def getInviteeIds(self):
        return self.inviteeIds

    def getPartyInfoTuple(self):
        startTime = self.partyInfo.startTime
        endTime = self.partyInfo.endTime
        formattedActivities = []
        for activity in self.partyInfo.activityList:
            oneActivity = (activity.activityId,
                           activity.x,
                           activity.y,
                           activity.h,
                           )
            formattedActivities.append(oneActivity)
        formattedDecors = []
        for decor in self.partyInfo.decors:
            oneDecor = (decor.decorId,
                        decor.x,
                        decor.y,
                        decor.h,
                        )
            formattedDecors.append(oneDecor)
        isPrivate = self.partyInfo.isPrivate
        inviteTheme = self.partyInfo.inviteTheme
            
        return (
            self.partyInfo.partyId,
            self.partyInfo.hostId,
            startTime.year,
            startTime.month,
            startTime.day,
            startTime.hour,
            startTime.minute,
            endTime.year,
            endTime.month,
            endTime.day,
            endTime.hour,
            endTime.minute,
            isPrivate,
            inviteTheme,
            formattedActivities,
            formattedDecors,
            self.partyInfo.status,
        )

    def delete(self):
        DistributedPartyAI.notify.debug("DistParty delete: %s" % self.doId)
        self.ignoreAll()
        try:
            self.Party_deleted
            DistributedPartyAI.notify.debug("party already deleted: %s" % self.Party_deleted)
        except:
            DistributedPartyAI.notify.debug("completing party delete: %s" % self.__dict__.get("zoneId"))
            self.air.writeServerEvent("party_delete",self.partyInfo.partyId, "%d|%d" % (self.doId,self.partyInfo.hostId))
            self.Party_deleted = self.zoneId
            for activityObj in self.activityObjects:
                activityObj.requestDelete()
            self.activityObjects = []
            DistributedObjectAI.delete(self)
            

    def unload(self):
        self.notify.debug("unload")

    def avIdEnteredParty(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if senderId != avId:
            self.air.writeServerEvent('suspicious', senderId, 'someone else trying to enter a party for this avatar: avId = %d' % avId)
            return
        if not self.hostName and self.avId == self.partyInfo.hostId:
            # if we don't have a hostname yet try again
            toon = simbase.air.doId2do.get(self.partyInfo.hostId)
            if toon:
                toonName = toon.getName()
                if toonName:
                    self.b_setHostName(toonName)
            
        self.sendUpdate("setAvIdsAtParty", [self.air.partyManager.zoneIdToGuestAvIds[self.zoneId]])
        totalMoney = -1
        av = simbase.air.doId2do.get(avId)
        if av:
            totalMoney = av.getTotalMoney()
        self.air.writeServerEvent("party_enter",self.partyInfo.partyId, "%d|%d" % (avId,totalMoney))

    def initPartyData(self):
        pass

    def destroyPartyData(self):
        if hasattr(self, "Party_deleted"):
            DistributedPartyAI.notify.debug("destroyPartyData: party already deleted: %s" % self.Party_deleted)
            return
        DistributedPartyAI.notify.debug("destroyPartyData: %s" % self.__dict__.get("zoneId"))
        self.releaseZoneData()

    def getHostName(self):
        """Return the host name."""
        return self.hostName

    def setHostName(self, newName):
        """Set the hostname on the AI only."""
        self.hostName = self.hostName

    def b_setHostName(self, newName):
        """Set the hostname on the ai and client"""
        self.setHostName(newName)
        self.d_setHostName(newName)

    def d_setHostName(self, newName):
        """Send the host name to the client."""
        self.sendUpdate("setHostName", [newName])        
    
    def isInActivity(self, avId):
        """Return true if the avId is busy with an activity."""
        result = False
        for actObj in self.activityObjects:
            if actObj.isInActivity(avId):
                result = True
                break
        return result
        
    
    
