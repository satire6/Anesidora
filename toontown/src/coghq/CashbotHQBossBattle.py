from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedCashbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class CashbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CashbotHQBossBattle")
    
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
                                              DistributedCashbotBoss.OneBossCog)
        # No need for a sky; this scene is entirely interior.

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)


    def exitCrane(self):
        CogHQBossBattle.CogHQBossBattle.exitCrane(self)

        # If we leave crane mode for any reason--for instance, we got
        # zapped--then tell the crane to relinquish control.
        messenger.send('exitCrane')
