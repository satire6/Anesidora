#-------------------------------------------------------------------------------
# Contact: Mark Wojtowicz
# Created: June 2010
#-------------------------------------------------------------------------------

from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyTrampolineActivityAI import DistributedPartyTrampolineActivityAI

class DistributedPartyVictoryTrampolineActivityAI(DistributedPartyTrampolineActivityAI):
    """ Reskinned trampoline for victory party holiday. """

    def __init__(self, air, partyDoId, x, y, h):
        DistributedPartyTrampolineActivityAI.__init__(self, air, partyDoId, x, y, h, actId=PartyGlobals.ActivityIds.PartyVictoryTrampoline)
