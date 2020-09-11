#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: AI side of the party hat which is where toon's go to access public
#          parties.
#-------------------------------------------------------------------------------

#from otp.ai.AIBase import *

from direct.distributed import DistributedObjectAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.parties import PartyGlobals

class DistributedPartyGateAI(DistributedObjectAI.DistributedObjectAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyGateAI")

    def __init__(self, air):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def getPartyList(self, avId):
        senderId = self.air.getAvatarIdFromSender()
        if avId != senderId:
            self.air.writeServerEvent('suspicious', senderId, 'someone else trying to get a list of public parties for: avId = %d' % avId)
            return
        self.sendUpdateToAvatarId(avId, "listAllPublicParties", [self.air.partyManager.getAllPublicParties()])
    
    def partyChoiceRequest(self, avId, shardId, zoneId):
        # A toon would like to go to this party.
        # We need to check if the party still has room and is still going (since
        # a good bit of time might have passed while they were looking at the
        # options).
        DistributedPartyGateAI.notify.debug("partyChoiceRequest : avId = %d, shardId = %d, zoneId = %d " % (avId, shardId, zoneId))
        senderId = self.air.getAvatarIdFromSender()
        
        if avId != senderId:
            self.air.writeServerEvent('suspicious', senderId, 'someone else trying to choose a public party for: avId = %d' % avId)
            return

        allPublicPartyInfo = self.air.partyManager.getAllPublicParties()
        
        if len(allPublicPartyInfo) == 0:
            # there are no parties at all
            DistributedPartyGateAI.notify.debug("partyChoiceRequest denied as no parties exist")
            self.sendUpdateToAvatarId(avId, "partyRequestDenied", [PartyGlobals.PartyGateDenialReasons.Unavailable])
        else:
            for partyTuple in allPublicPartyInfo:
                if partyTuple[0] == shardId and partyTuple[1] == zoneId:
                    # the specific party they requested has been found
                    if partyTuple[2] < PartyGlobals.MaxToonsAtAParty:
                        DistributedPartyGateAI.notify.debug("partyChoiceRequest accepted")
                        self.sendUpdateToAvatarId(avId, "setParty", [partyTuple])
                    else:
                        DistributedPartyGateAI.notify.debug("partyChoiceRequest denied as number at party is %d and max allowed is %d" %(partyTuple[2], PartyGlobals.MaxToonsAtAParty))
                        self.sendUpdateToAvatarId(avId, "partyRequestDenied", [PartyGlobals.PartyGateDenialReasons.Full])
                    break # prevent else clause from running
            else:
                # the desired party was not found
                DistributedPartyGateAI.notify.debug("partyChoiceRequest denied as party could not be found")
                self.sendUpdateToAvatarId(avId, "partyRequestDenied", [PartyGlobals.PartyGateDenialReasons.Unavailable])
        
        # We might want to also send a lane for the toon to use when he walks
        # through the hat...  if so, we should do a wait of like 3 seconds, and
        # then free the lane we just sent...
