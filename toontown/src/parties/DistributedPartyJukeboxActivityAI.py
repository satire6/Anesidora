#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: AI component that manages which toons are currently dancing, who entered
#          and exited the dance floor, and broadcasts dance moves to all clients.
#-------------------------------------------------------------------------------

from toontown.parties.DistributedPartyJukeboxActivityBaseAI import DistributedPartyJukeboxActivityBaseAI

from toontown.parties import PartyGlobals

class DistributedPartyJukeboxActivityAI(DistributedPartyJukeboxActivityBaseAI ):
    notify = directNotify.newCategory("DistributedPartyJukeboxActivityAI")
    
    def __init__(self, air, partyDoId, x, y, h):
        self.notify.debug("Intializing.")
        DistributedPartyJukeboxActivityBaseAI.__init__(self,
                                            air,
                                            partyDoId,
                                            x, y, h,
                                            PartyGlobals.ActivityIds.PartyJukebox,
                                            PartyGlobals.PhaseToMusicData,
                                            )
    
