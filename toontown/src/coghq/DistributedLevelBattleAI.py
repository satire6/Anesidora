from toontown.battle import DistributedBattleAI
from toontown.battle import DistributedBattleBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import State
from direct.fsm import ClassicFSM
from toontown.battle.BattleBase import *
import CogDisguiseGlobals
from direct.showbase.PythonUtil import addListsByValue

class DistributedLevelBattleAI(DistributedBattleAI.DistributedBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLevelBattleAI')
    
    def __init__(self, air, battleMgr, pos, suit, toonId, zoneId,
                 level, battleCellId, winState,
                 roundCallback=None,
                 finishCallback=None,
                 maxSuits=4):
        """__init__(air, battleMgr, pos, suit, toonId, zoneId,
                    roundCallback, finishCallback, maxSuits)
        """
        self.blocker = None
        self.level = level
        self.battleCellId = battleCellId
        self.winState = winState
        self.roundCallback = roundCallback
        self.suitTrack = suit.dna.dept
        DistributedBattleAI.DistributedBattleAI.__init__(
            self, air, battleMgr, pos, suit, toonId, zoneId,
            finishCallback, maxSuits, tutorialFlag=0, levelFlag=1)

        # figure out if we're a boss battle

        isBossBattle = 0
        for suit in self.battleMgr.level.planner.battleCellId2suits[
            battleCellId]:
            if suit.boss:
                isBossBattle = 1
                break
        self.setBossBattle(isBossBattle)
        self.bossDefeated = 0
        
    def generate(self):
        DistributedBattleAI.DistributedBattleAI.generate(self)
        # attach battle blocker if it exists
        battleBlocker =  self.battleMgr.battleBlockers.get(self.battleCellId)
        if battleBlocker:
            self.blocker = battleBlocker
            battleBlocker.b_setBattle(self.doId)

    def getLevelDoId(self):
        return self.level.doId

    def getBattleCellId(self):
        return self.battleCellId

    def getTaskZoneId(self):
        # override this
        pass

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
            self.roundCallback(self.battleCellId, self.activeToons, totalHp, deadSuits)
            
    def storeSuitsKilledThisBattle(self):
        # this works if there's one battle per floor
        # override if you need to support multiple battles per floor
        self.suitsKilledPerFloor.append(self.suitsKilledThisBattle)

    def resume(self, topFloor=0):
        assert(self.notify.debug('resuming the battle'))
        if (len(self.suits) == 0):
            # Toons won - award experience, etc.
            assert(self.resumeNeedUpdate == 1)
            avList = []
            for toonId in self.activeToons:
                toon = self.getToon(toonId)
                if toon:
                    avList.append(toon)

            self.d_setMembers()

            self.storeSuitsKilledThisBattle()

            # Only give experience if the boss battle just finished
            if (self.bossBattle == 0):
                self.b_setState('Reward')
            else:
                self.handleToonsWon(avList)
                self.d_setBattleExperience()
                self.b_setState(self.winState)  

            # Update the battle blockers
            if self.blocker:
                # don't tell the battle blocker to deactivate unless there
                # were victor toons
                if len(self.activeToons):
                    self.blocker.b_setBattleFinished()
            
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

    def handleToonsWon(self, toons):
        # toons just beat the boss
        # override this
        pass

    ##### Resume state #####
    # Defined in DistributedBattleAI
 
    ##### FaceOff state #####

    # original suit and toon face off and then walk to positions,
    # other toons or suits walk directly to wait positions

    def enterFaceOff(self):
        self.notify.debug('DistributedLevelBattleAI.enterFaceOff()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        # From here on out DistributedBattleAI only controls DistributedSuitAI
        # DistributedBattle controls DistributedSuit
        self.suits[0].releaseControl()
        faceOffTime = self.calcToonMoveTime(self.pos,
                                            self.initialSuitPos) + FACEOFF_TAUNT_T + \
                                            SERVER_BUFFER_TIME
        self.notify.debug("faceOffTime = %s" % faceOffTime)
        self.timer.startCallback(faceOffTime,
                                 self.__serverFaceOffDone)
        return None

    def __serverFaceOffDone(self):
        self.notify.debug('faceoff timed out on server')
        self.ignoreFaceOffDone = 1
        self.handleFaceOffDone()

    def exitFaceOff(self):
        self.notify.debug("DistributedLevelBattleAI.exitFaceOff()")
        self.timer.stop()
        return None

    def faceOffDone(self):
        """ faceOffDone(toonId)
        """
        assert(self.notify.debug("DistributedLevelBattleAI.faceOffDone()"))
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreFaceOffDone == 1):
            self.notify.debug('faceOffDone() - ignoring toon: %d' % toonId)
            return
        elif (self.fsm.getCurrentState().getName() != 'FaceOff'):
            self.notify.warning('faceOffDone() - in state: %s' % \
                        self.fsm.getCurrentState().getName())
            return
        elif (self.toons.count(toonId) == 0):
            self.notify.warning('faceOffDone() - toon: %d not in toon list' % \
                toonId)
            return
        self.notify.debug('toon: %d done facing off' % toonId)
        if not self.ignoreFaceOffDone:
            self.handleFaceOffDone()

    def suitRequestJoin(self, suit):
        """ suitRequestJoin(suit)
        """
        # We redefine this base class function, because in some
        # cases we get this call from a suit that has been pulled
        # into battle by a battleblocker.  We don't want to throw
        # an assertion in that case, as the base class does, so we
        # redefine the function without the assert.
        self.notify.debug('DistributedLevelBattleAI.suitRequestJoin(%d)' % suit.getDoId())

        # make sure we're not trying to add a suit that's
        # already in this battle
        if suit in self.suits:
            self.notify.warning('suit %s already in this battle' % suit.getDoId())
            return 0

        DistributedBattleBaseAI.DistributedBattleBaseAI.suitRequestJoin(self,suit)

    ##### Reward state #####

    def enterReward(self):
        assert(self.notify.debug('enterReward()'))
        self.joinableFsm.request('Unjoinable')
        self.runableFsm.request('Unrunable')

        # In the building battles, we don't expect any toons to send a
        # done message before this (short) timer expires.  This is
        # just the between-floor reward dance, very brief.
        self.timer.startCallback(FLOOR_REWARD_TIMEOUT, self.serverRewardDone)
        return None

    def exitReward(self):
        self.timer.stop()
        return None
