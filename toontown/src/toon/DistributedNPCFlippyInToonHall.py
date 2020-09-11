from pandac.PandaModules import *
from DistributedNPCToon import *

class DistributedNPCFlippyInToonHall(DistributedNPCToon):

    def __init__(self, cr):
        assert self.notify.debug("__init__")
        DistributedNPCToon.__init__(self, cr)
            
    def getCollSphereRadius(self):
        return 4
        
    def initPos(self):
        self.clearMat()
        self.setScale(1.25)
        #self.setHpr(180, 0, 0)
        pass
        
    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        if self.allowedToTalk():
            # Lock down the avatar for quest mode
            base.cr.playGame.getPlace().fsm.request('quest', [self])
            # Tell the server
            self.sendUpdate("avatarEnter", [])
            # make sure this NPCs chat balloon is visible above all others for the locekd down avatar
            self.nametag3d.setDepthTest(0)
            self.nametag3d.setBin('fixed', 0)
            self.lookAt(base.localAvatar)
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='quests',
                                                  doneFunc=self.handleOkTeaser)        