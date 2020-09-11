from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleBase import *
from toontown.coghq import DistributedLevelBattle
from direct.directnotify import DirectNotifyGlobal
from toontown.toon import TTEmote
from otp.avatar import Emote
from toontown.battle import SuitBattleGlobals
import random
from toontown.suit import SuitDNA
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals

class DistributedMintBattle(DistributedLevelBattle.DistributedLevelBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMintBattle')

    def __init__(self, cr):
        """
        cr is a ClientRepository.
        """
        DistributedLevelBattle.DistributedLevelBattle.__init__(self,cr)

        # Add a new reward state to the battle ClassicFSM
        self.fsm.addState(State.State('MintReward',
                                        self.enterMintReward,
                                        self.exitMintReward,
                                        ['Resume']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('MintReward')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('MintReward')

    ##### MintReward state #####

    def enterMintReward(self, ts):
        self.notify.debug('enterMintReward()')
        self.disableCollision()
        self.delayDeleteMembers()
        if (self.hasLocalToon()):
            NametagGlobals.setMasterArrowsOn(0)
            if self.bossBattle:
                messenger.send('localToonConfrontedMintBoss')
        self.movie.playReward(ts, self.uniqueName('building-reward'),
                              self.__handleMintRewardDone)

    def __handleMintRewardDone(self):
        self.notify.debug('mint reward done')
        if (self.hasLocalToon()):
            self.d_rewardDone(base.localAvatar.doId)
        self.movie.resetReward()

        # Now request our local battle object enter the Resume state,
        # which frees us from the battle.  The distributed object may
        # not enter the Resume state yet (it has to wait until all the
        # toons involved have reported back up), but there's no reason
        # we have to wait around for that.
        self.fsm.request('Resume')

    def exitMintReward(self):
        self.notify.debug('exitMintReward()')
        # In case we're observing and the server cuts us off
        # this guarantees all final animations get started and things
        # get cleaned up
        self.movie.resetReward(finish=1)
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)
