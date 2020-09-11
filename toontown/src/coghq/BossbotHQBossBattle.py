from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedBossbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class BossbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("BossbotHQBossBattle")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        # This is only used for magic words.
        self.teleportInPosHpr = (88, -214, 0, 210, 0, 0)

        for stateName in ['movie',]:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('crane')

        # force a finalBattle to finalBattle transition to be valid
        # makes life easier when a toon is hit while golfing
        state = self.fsm.getStateNamed('finalBattle')
        state.addTransition('finalBattle')


    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus,
                                              DistributedBossbotBoss.OneBossCog)
        # No need for a sky; this scene is entirely interior.

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)



    def exitCrane(self):
        CogHQBossBattle.CogHQBossBattle.exitCrane(self)

        # If we leave crane mode for any reason--for instance, we got
        # zapped--then tell the pitcher or table to relinquish control.
        messenger.send('exitCrane')
