#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: Party Dance Activity. Loads up the dance floor and plays the rotation
#          sequences, as well as handles dance moves and toons currently dancing.
#          Toon animation states are handled by PartyDanceActivityToonFSM
#          Dance pattern input is handled through KeyCodes
#          Dance pattern visual is handled through keyCodesGui
#-------------------------------------------------------------------------------
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyDanceActivityBase import DistributedPartyDanceActivityBase
from toontown.toonbase import TTLocalizer

class DistributedPartyDanceActivity(DistributedPartyDanceActivityBase):
    notify = directNotify.newCategory("DistributedPartyDanceActivity")
    
    
    def __init__(self, cr):
        DistributedPartyDanceActivityBase.__init__(self,
                                          cr,
                                          PartyGlobals.ActivityIds.PartyDance,
                                          PartyGlobals.DancePatternToAnims
                                          )
 
    def getInstructions(self):
        return TTLocalizer.PartyDanceActivityInstructions

    def getTitle(self):
        return TTLocalizer.PartyDanceActivityTitle

    def load(self):
        """Load the dance floor, and handle 10 and 20 versions of disco ball."""
        DistributedPartyDanceActivityBase.load(self)
        parentGroup =  self.danceFloor.find("**/discoBall_mesh")
        correctBall = self.danceFloor.find("**/discoBall_10")
        origBall = self.danceFloor.find("**/discoBall_mesh_orig")
        if not correctBall.isEmpty():
            numChildren = parentGroup.getNumChildren()
            for i in xrange(numChildren):
                child = parentGroup.getChild(i)
                if child != correctBall:
                    child.hide()
