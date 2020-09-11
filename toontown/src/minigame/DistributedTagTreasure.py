from toontown.safezone import DistributedTreasure

class DistributedTagTreasure(DistributedTreasure.DistributedTreasure):
    
    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        self.modelPath = "phase_4/models/props/icecream"
        self.grabSoundPath = "phase_4/audio/sfx/SZ_DD_treasure.mp3"
        # listen for the minigame's offstage event so we can hide ourselves
        # this hook is cleared by an ignoreAll() in DistributedTreasure
        self.accept('minigameOffstage', self.handleMinigameOffstage)

    def handleEnterSphere(self, collEntry):
        # Override the base class grab function
        # Only request the grab if you are not it
        if not base.localAvatar.isIt:
            self.d_requestGrab()
        return None

    def handleMinigameOffstage(self):
        self.nodePath.reparentTo(hidden)
