#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: Party Jukebox Activity places a jukebox in the party and controls
#          playback of all the music. Music scheduling is handled on the AI side.
#
# Bug Fixes:
# 1. Fixed occasasion where it can throw an exception on an unloaded GUI:
#    Toon walks to the jukebox, and the Jukebox GUI pops up.
#    Toon adds a song, the "Add Song" button is disabled while the request is sent to the server.
#    While the server is processing the request, the Toon closes the Jukebox GUI, which is unloaded from the client.
#    When the response comes back, the client expects a GUI to be loaded so that it can enable the "Add Song" button again.
#    Solution:
#        make sure that self.gui.isLoaded() is in check first before doing
#        server response operations.
#-------------------------------------------------------------------------------

from toontown.parties.DistributedPartyJukeboxActivityBase import DistributedPartyJukeboxActivityBase
from toontown.parties import PartyGlobals

class DistributedPartyJukeboxActivity(DistributedPartyJukeboxActivityBase):
    notify = directNotify.newCategory("DistributedPartyJukeboxActivity")
    
    def __init__(self, cr):
        DistributedPartyJukeboxActivityBase.__init__(self,
                                          cr,
                                          PartyGlobals.ActivityIds.PartyJukebox,
                                          PartyGlobals.PhaseToMusicData
                                          )

