from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedLawbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class LawbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("LawbotHQBossBattle")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        # This is only used for magic words.
        self.teleportInPosHpr = (88, -214, 0, 210, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus,
                                              DistributedLawbotBoss.OneBossCog)
        # No need for a sky; this scene is entirely interior.

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)


