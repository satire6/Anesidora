from otp.ai.AIBase import *
from BattleBase import *
from BattleCalculatorAI import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *

import DistributedBattleBaseAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import State
from direct.showbase.PythonUtil import addListsByValue
import random
import types

# attack properties table
class DistributedBattleFinalAI(DistributedBattleBaseAI.DistributedBattleBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleFinalAI')

    def __init__(self, air, bossCog, roundCallback,
                 finishCallback, battleSide):
        DistributedBattleBaseAI.DistributedBattleBaseAI.__init__(
            self, air, bossCog.zoneId, finishCallback)
        self.bossCogId = bossCog.doId
        self.battleNumber = bossCog.battleNumber
        self.battleSide = battleSide
        self.streetBattle = 0
        self.roundCallback = roundCallback
        self.elevatorPos = Point3(0, 0, 0)
        self.pos = Point3(0, 30, 0)

        self.resumeNeedUpdate = 0

        # Add a state for reserve suits to join to the battle ClassicFSM
        self.fsm.addState(State.State('ReservesJoining',
                                      self.enterReservesJoining,
                                      self.exitReservesJoining,
                                      ['WaitForJoin']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('ReservesJoining')
        waitForJoinState = self.fsm.getStateNamed('WaitForJoin')
        waitForJoinState.addTransition('ReservesJoining')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('ReservesJoining')

    def getBossCogId(self):
        return self.bossCogId

    def getBattleNumber(self):
        return self.battleNumber

    def getBattleSide(self):
        return self.battleSide

    def startBattle(self, toonIds, suits):
        self.joinableFsm.request('Joinable')
        for toonId in toonIds:
            if self.addToon(toonId):
                self.activeToons.append(toonId)

        # We have to be sure to tell the players that they're active
        # before we start adding suits.
        self.d_setMembers()

        for suit in suits:
            joined = self.suitRequestJoin(suit)
            assert(joined)

        self.d_setMembers()
        self.b_setState('ReservesJoining')

    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    ##### WaitForJoin state #####

    ##### WaitForInput state #####

    ##### PlayMovie state #####

    def localMovieDone(self, needUpdate, deadToons, deadSuits, lastActiveSuitDied):
        # Stop the server timeout for the movie
        self.timer.stop()

        self.resumeNeedUpdate = needUpdate
        self.resumeDeadToons = deadToons
        self.resumeDeadSuits = deadSuits
        self.resumeLastActiveSuitDied = lastActiveSuitDied

        if (len(self.toons) == 0):
            # Toons lost - close up shop
            self.d_setMembers()
            self.b_setState('Resume')
        else:
            # Calculate the total hp of all the suits to see if any 
            # reserves need to join
            assert(self.roundCallback != None)
            totalHp = 0
            for suit in self.suits:
                if (suit.currHP > 0):
                    totalHp += suit.currHP
            # Signal the suit interior that the round is over and wait to
            # hear what to do next
            self.roundCallback(self.activeToons, totalHp, deadSuits)

    def resume(self, joinedReserves):
        assert(self.notify.debug('resuming the battle'))
        if len(joinedReserves) != 0:
            for info in joinedReserves:
                joined = self.suitRequestJoin(info[0])
                assert(joined)
            self.d_setMembers()
            self.b_setState('ReservesJoining')
            
        elif (len(self.suits) == 0):
            # Toons won - award experience, etc.
            assert(self.resumeNeedUpdate == 1)
            battleMultiplier = getBossBattleCreditMultiplier(self.battleNumber)
            for toonId in self.activeToons:
                toon = self.getToon(toonId)
                if toon:
                    # Append the recovered and not recovered items to their respective lists
                    recovered, notRecovered = self.air.questManager.recoverItems(
                      toon, self.suitsKilledThisBattle, self.zoneId)
                    self.toonItems[toonId][0].extend(recovered)
                    self.toonItems[toonId][1].extend(notRecovered)
                    # No need to recover merits - you are about to get a promotion!
                    #meritArray = self.air.promotionMgr.recoverMerits(
                    #    toon, self.suitsKilledThisBattle, self.zoneId, battleMultiplier)
                    #self.toonMerits[toonId] = addListsByValue(self.toonMerits[toonId], meritArray)
            self.d_setMembers()
            self.d_setBattleExperience()
            self.b_setState('Reward')

        else:
            # Continue with the battle
            if (self.resumeNeedUpdate == 1):
                self.d_setMembers()
                if ((len(self.resumeDeadSuits) > 0 and 
                     self.resumeLastActiveSuitDied == 0) or
                     (len(self.resumeDeadToons) > 0)):
                    self.needAdjust = 1
                # Wait for input will call __requestAdjust()
            self.setState('WaitForJoin')

        self.resumeNeedUpdate = 0
        self.resumeDeadToons = []
        self.resumeDeadSuits = []
        self.resumeLastActiveSuitDied = 0

    ##### ReservesJoining state #####

    def enterReservesJoining(self, ts=0):
        assert(self.notify.debug('enterReservesJoining()'))
        self.beginBarrier("ReservesJoining", self.toons, 15,
                          self.__doneReservesJoining)
        
    def __doneReservesJoining(self, avIds):
        self.b_setState('WaitForJoin')
        
    def exitReservesJoining(self, ts=0):
        return None

    ##### Reward state #####

    def enterReward(self):
        assert(self.notify.debug('enterReward()'))

        # In the building battles, we don't expect any toons to send a
        # done message before this (short) timer expires.  This is
        # just the between-floor reward dance, very brief.
        self.timer.startCallback(FLOOR_REWARD_TIMEOUT + 5, self.serverRewardDone) 
        return None

    def exitReward(self):
        self.timer.stop()
        return None

    ##### Resume state #####

    def enterResume(self):
        self.joinableFsm.request('Unjoinable')
        self.runableFsm.request('Unrunable')
        DistributedBattleBaseAI.DistributedBattleBaseAI.enterResume(self)

        assert(self.finishCallback != None)
        self.finishCallback(self.zoneId, self.activeToons)
