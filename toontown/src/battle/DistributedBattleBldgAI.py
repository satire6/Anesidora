from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from BattleBase import *
from BattleCalculatorAI import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *
from direct.showbase.PythonUtil import addListsByValue
import DistributedBattleBaseAI
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
import random
from direct.fsm import State
from direct.fsm import ClassicFSM, State
from direct.showbase import PythonUtil

# attack properties table
class DistributedBattleBldgAI(DistributedBattleBaseAI.DistributedBattleBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleBldgAI')
                    
    def __init__(self, air, zoneId, roundCallback=None,
                 finishCallback=None, maxSuits=4, bossBattle=0):
        """__init__(air, zoneId, suits, toonIds, finishCallback, maxSuits,
                                                        bossBattle)
        """
        DistributedBattleBaseAI.DistributedBattleBaseAI.__init__(self, air,
                        zoneId, finishCallback, maxSuits, bossBattle)
        self.streetBattle = 0
        self.roundCallback = roundCallback

        # Add a new reward state to the battle ClassicFSM
        self.fsm.addState(State.State('BuildingReward',
                                        self.enterBuildingReward,
                                        self.exitBuildingReward,
                                        ['Resume']))
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('BuildingReward')

##         # Add a state for reserve suits to join to the battle ClassicFSM
##         self.fsm.addState(State.State('ReservesJoining',
##                                         self.enterReservesJoining,
##                                         self.exitReservesJoining,
##                                         ['WaitForInput']))
##         playMovieState.addTransition('ReservesJoining')

        self.elevatorPos = Point3(0, -30, 0)
        self.resumeNeedUpdate = 0

    def setInitialMembers(self, toonIds, suits):
        for suit in suits:
            self.addSuit(suit)
        for toonId in toonIds:
            self.addToon(toonId)

        self.fsm.request('FaceOff')

    def delete(self):
        del self.roundCallback
        DistributedBattleBaseAI.DistributedBattleBaseAI.delete(self)

    def faceOffDone(self):
        """ faceOffDone(toonId)
        """
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
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
        assert(self.responses.has_key(toonId))
        self.responses[toonId] += 1
        self.notify.debug('toon: %d done facing off' % toonId)
        if not self.ignoreFaceOffDone:
            if (self.allToonsResponded()):
                self.handleFaceOffDone()

            else:
                # Reset the timer to give the slowpokes a few seconds
                # longer than the first (or most recent) toon to reply.
                self.timer.stop()
                self.timer.startCallback(TIMEOUT_PER_USER, self.__serverFaceOffDone)

    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    ##### FaceOff state #####

    # original suit and toon face off and then walk to positions,
    # other toons or suits walk directly to wait positions

    def enterFaceOff(self):
        self.notify.debug('enterFaceOff()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        # From here on out DistributedBattleAI only controls DistributedSuitAI
        # DistributedBattle controls DistributedSuit
        self.timer.startCallback(self.calcToonMoveTime(self.pos,
                         self.elevatorPos) + FACEOFF_TAUNT_T + \
                                                SERVER_BUFFER_TIME,
                         self.__serverFaceOffDone)
        return None

    def __serverFaceOffDone(self):
        self.notify.debug('faceoff timed out on server')
        self.ignoreFaceOffDone = 1
        self.handleFaceOffDone()

    def exitFaceOff(self):
        self.timer.stop()
        self.resetResponses()
        return None

    def handleFaceOffDone(self):
        assert(len(self.activeSuits) == 0)
        for suit in self.suits:
            self.activeSuits.append(suit)
        assert(len(self.activeToons) == 0)
        for toon in self.toons:
            self.activeToons.append(toon)
            # Set the toon's earned experience so far.
            self.sendEarnedExperience(toon)
        self.d_setMembers()
        self.b_setState('WaitForInput')

    ##### WaitForJoin state #####

    ##### WaitForInput state #####

    ##### PlayMovie state #####

    def localMovieDone(self, needUpdate, deadToons, deadSuits, lastActiveSuitDied):
        assert(self.notify.debug('localMovieDone(%s, %s, %s, %s)' % (needUpdate, deadToons, deadSuits, lastActiveSuitDied)))
        # Stop the server timeout for the movie
        self.timer.stop()

        self.resumeNeedUpdate = needUpdate
        self.resumeDeadToons = deadToons
        self.resumeDeadSuits = deadSuits
        self.resumeLastActiveSuitDied = lastActiveSuitDied

        if (len(self.toons) == 0):
            # Toons lost - close up shop
            assert(self.notify.debug('last toon gone, destroying building'))
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

    def __goToResumeState(self, task):
        self.b_setState('Resume')

    def resume(self, currentFloor=0, topFloor=0):
        assert(self.notify.debug('resuming the battle'))
        if (len(self.suits) == 0):
            # Toons won - award experience, etc.
            assert(self.resumeNeedUpdate == 1)

            self.d_setMembers()

            self.suitsKilledPerFloor.append(self.suitsKilledThisBattle)

            if (topFloor == 0):
                self.b_setState('Reward')
            else:
                # calculate and assign the merits and item recoveries by floor
                for floorNum, cogsThisFloor in PythonUtil.enumerate(self.suitsKilledPerFloor):
                    for toonId in self.activeToons:
                        toon = self.getToon(toonId)
                        if toon:
                            # Append the recovered and not recovered items to their respective lists
                            recovered, notRecovered = self.air.questManager.recoverItems(
                                toon, cogsThisFloor, self.zoneId)
                            self.toonItems[toonId][0].extend(recovered)
                            self.toonItems[toonId][1].extend(notRecovered)
                            # the new merit list must be added by value to the cumulative list
                            meritArray = self.air.promotionMgr.recoverMerits(
                                toon, cogsThisFloor, self.zoneId, getCreditMultiplier(floorNum))

                            if toonId in self.helpfulToons:
                                self.toonMerits[toonId] = addListsByValue(self.toonMerits[toonId], meritArray)
                            else:
                                self.notify.debug("toon %d not helpful, skipping merits" % toonId)

                self.d_setBattleExperience()
                self.b_setState('BuildingReward')
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
        return None

    def exitReservesJoining(self, ts=0):
        return None

    ##### Reward state #####

    def enterReward(self):
        assert(self.notify.debug('enterReward()'))

        # In the building battles, we don't expect any toons to send a
        # done message before this (short) timer expires.  This is
        # just the between-floor reward dance, very brief.
        self.timer.startCallback(FLOOR_REWARD_TIMEOUT, self.serverRewardDone) 
        return None

    def exitReward(self):
        self.timer.stop()
        return None

    ##### BuildingReward state #####

    def enterBuildingReward(self):
        assert(self.notify.debug('enterBuildingReward()'))
        self.resetResponses()
        self.assignRewards()

        # Set an upper timeout for the reward movie.  If no toons
        # report back by this time, call it done anyway.
        self.timer.startCallback(BUILDING_REWARD_TIMEOUT, self.serverRewardDone)
        return None

    def exitBuildingReward(self):
        return None

    ##### Resume state #####

    def enterResume(self):
        DistributedBattleBaseAI.DistributedBattleBaseAI.enterResume(self)

        assert(self.finishCallback != None)
        self.finishCallback(self.zoneId, self.activeToons)

    def exitResume(self):
        DistributedBattleBaseAI.DistributedBattleBaseAI.exitResume(self)

        taskName = self.taskName('finish')
        taskMgr.remove(taskName)
