#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: AI component that manages which toons are currently dancing, who entered
#          and exited the dance floor, and broadcasts dance moves to all clients.
#-------------------------------------------------------------------------------

from toontown.parties.DistributedPartyDanceActivityBaseAI import DistributedPartyDanceActivityBaseAI
from toontown.parties import PartyGlobals

# 20 move dance floor
class DistributedPartyDance20ActivityAI(DistributedPartyDanceActivityBaseAI):
    notify = directNotify.newCategory("DistributedPartyDanceActivityAI")
    
    def __init__(self, air, partyDoId, x, y, h):
        self.notify.debug("Intializing.")
        DistributedPartyDanceActivityBaseAI.__init__(self,
                                            air,
                                            partyDoId,
                                            x, y, h,
                                            PartyGlobals.ActivityIds.PartyDance20,
                                            PartyGlobals.DancePatternToAnims20,
                                            )
