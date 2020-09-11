from toontown.coghq import DistributedLevelBattleAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from toontown.battle.BattleBase import *
import CogDisguiseGlobals
from direct.showbase.PythonUtil import addListsByValue

class DistributedBattleFactoryAI(DistributedLevelBattleAI.DistributedLevelBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleFactoryAI')
    
    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId,
                 level, battleCellId,
                 roundCallback=None,
                 finishCallback=None,
                 maxSuits=4):
        DistributedLevelBattleAI.DistributedLevelBattleAI.__init__(
            self, air, battleMgr, pos, suit, toonId, zoneId, level,
            battleCellId, 'FactoryReward', roundCallback, finishCallback,
            maxSuits)

        # We shouldn't get invasion credit for factory battles.  The
        # invasion is happening out on the streets.
        self.battleCalc.setSkillCreditMultiplier(1)

        if self.bossBattle:
            self.level.d_setForemanConfronted(toonId)

        # Add a new reward state to the battle ClassicFSM
        self.fsm.addState(State.State('FactoryReward',
                                        self.enterFactoryReward,
                                        self.exitFactoryReward,
                                        ['Resume']))
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('FactoryReward')

    def getTaskZoneId(self):
        # factoryId is also the factory's location
        return self.level.factoryId

    def handleToonsWon(self, toons):
        # toons just beat the boss
        for toon in toons:
            # Append recovered and unrecovered items onto their respective lists
            recovered, notRecovered = self.air.questManager.recoverItems(
                toon, self.suitsKilled, self.getTaskZoneId())
            self.toonItems[toon.doId][0].extend(recovered)
            self.toonItems[toon.doId][1].extend(notRecovered)
            
            # the merit list must be added by value to the cumulative list
            meritArray = self.air.promotionMgr.recoverMerits(
                toon, self.suitsKilled, self.getTaskZoneId(), getFactoryMeritMultiplier(self.getTaskZoneId()))
            if toon.doId in self.helpfulToons:
                self.toonMerits[toon.doId] = addListsByValue(self.toonMerits[toon.doId], meritArray)
            else:
                self.notify.debug("toon %d not helpful, skipping merits" % toon.doId)

            # only give part at the very end
            if self.bossBattle:
                self.toonParts[toon.doId] = self.air.cogSuitMgr.recoverPart(
                    toon, self.level.factoryType, self.suitTrack,
                    self.getTaskZoneId(), toons)
                self.notify.debug("toonParts = %s" % self.toonParts)

    ##### FactoryReward state #####

    def enterFactoryReward(self):
        # this state is entered when a factory has been defeated
        assert(self.notify.debug('enterFactoryReward()'))
        self.joinableFsm.request('Unjoinable')
        self.runableFsm.request('Unrunable')
        self.resetResponses()
        self.assignRewards()

        self.bossDefeated = 1

        # let the factory know which toons beat it
        self.level.setVictors(self.activeToons[:])

        # Set an upper timeout for the reward movie.  If no toons
        # report back by this time, call it done anyway.
        self.timer.startCallback(BUILDING_REWARD_TIMEOUT, self.serverRewardDone)
        return None

    def exitFactoryReward(self):
        return None

    ##### Resume state #####

    def enterResume(self):
        DistributedLevelBattleAI.DistributedLevelBattleAI.enterResume(self)
        if self.bossBattle and self.bossDefeated:
            self.battleMgr.level.b_setDefeated()
