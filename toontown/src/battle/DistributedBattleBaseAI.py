from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *
from BattleBase import *
from BattleCalculatorAI import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *
from pandac.PandaModules import *
import BattleExperienceAI
from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal
from toontown.ai import DatabaseObject
from toontown.toon import DistributedToonAI
from toontown.toon import InventoryBase
from toontown.toonbase import ToontownGlobals
import random
from toontown.toon import NPCToons

# attack properties table
class DistributedBattleBaseAI(DistributedObjectAI.DistributedObjectAI,
                              BattleBase):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleBaseAI')
    
    def __init__(self, air, zoneId, finishCallback=None, maxSuits=4,
                 bossBattle=0, tutorialFlag=0, interactivePropTrackBonus = -1):
        """__init__(air, zoneId, finishCallback, maxSuits, bossBattle)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.serialNum = 0

        self.zoneId = zoneId
        self.maxSuits = maxSuits
        self.setBossBattle(bossBattle)
        self.tutorialFlag = tutorialFlag
        self.interactivePropTrackBonus = interactivePropTrackBonus

        # function to call when this battle is about to be destroyed
        self.finishCallback = finishCallback

        self.avatarExitEvents = []
        self.responses = {}
        self.adjustingResponses = {}
        self.joinResponses = {}
        self.adjustingSuits = []
        self.adjustingToons = []

        # Track the number of suits that have ever joined this battle.
        self.numSuitsEver = 0

        BattleBase.__init__(self)

        self.streetBattle = 1
        self.pos = Point3(0, 0, 0)
        self.initialSuitPos = Point3(0, 0, 0)

        self.toonExp = {}
        self.toonOrigQuests = {}
        self.toonItems = {}
        self.toonOrigMerits = {}
        self.toonMerits = {}
        self.toonParts = {}
        self.battleCalc = BattleCalculatorAI(self, tutorialFlag)

        # If there is an invasion, double the exp for the duration of this battle
        # Now, if the invasion ends midway through this battle, the players will
        # continue getting credit. This is ok I guess.
        if self.air.suitInvasionManager.getInvading():
            mult = getInvasionMultiplier()
            self.battleCalc.setSkillCreditMultiplier(mult)

        # see if we have the double xp holiday up
        if self.air.holidayManager.isMoreXpHolidayRunning():
            mult = getMoreXpHolidayMultiplier()
            self.battleCalc.setSkillCreditMultiplier(mult)
            
        self.fsm = None

        self.clearAttacks()

        self.ignoreFaceOffDone = 0
        self.needAdjust = 0
        self.movieHasBeenMade = 0
        self.movieHasPlayed = 0
        self.rewardHasPlayed = 0
        self.movieRequested = 0

        self.ignoreResponses = 0
        self.ignoreAdjustingResponses = 0

        self.taskNames = []
        self.exitedToons = []

        # Maintain a list of all the suits killed in the battle
        # for the quest system and the suit page
        self.suitsKilled = []
        self.suitsKilledThisBattle = []
        self.suitsKilledPerFloor = []

        # Maintain a list of all the suits encountered in the battle
        # for the suit page
        self.suitsEncountered = []
        # these will help
        self.newToons = []
        self.newSuits = []

        self.numNPCAttacks = 0
        self.npcAttacks = {}

        self.pets = {}

        self.fsm = ClassicFSM.ClassicFSM('DistributedBattleAI',
                        [State.State('FaceOff',
                                self.enterFaceOff,
                                self.exitFaceOff,
                                ['WaitForInput',
                                'Resume']),
                        State.State('WaitForJoin',
                                self.enterWaitForJoin,
                                self.exitWaitForJoin,
                                ['WaitForInput', 'Resume']),
                        State.State('WaitForInput',
                                self.enterWaitForInput,
                                self.exitWaitForInput,
                                ['MakeMovie',
                                'Resume']),
                        State.State('MakeMovie',
                                self.enterMakeMovie,
                                self.exitMakeMovie,
                                ['PlayMovie',
                                'Resume']),
                        State.State('PlayMovie',
                                self.enterPlayMovie,
                                self.exitPlayMovie,
                                ['WaitForJoin',
                                'Reward',
                                'Resume']),
                        State.State('Reward',
                                self.enterReward,
                                self.exitReward,
                                ['Resume']),
                        State.State('Resume',
                                self.enterResume,
                                self.exitResume,
                                []),
                        State.State('Off',
                                self.enterOff,
                                self.exitOff,
                                ['FaceOff', 'WaitForJoin'])],
                        # Initial state
                        'Off',
                        # Final state
                        'Off',
                        )

        self.joinableFsm = ClassicFSM.ClassicFSM('Joinable',
                        [State.State('Joinable',
                                self.enterJoinable,
                                self.exitJoinable,
                                ['Unjoinable']),
                        State.State('Unjoinable',
                                self.enterUnjoinable,
                                self.exitUnjoinable,
                                ['Joinable'])],
                        # Initial state
                        'Unjoinable',
                        # Final state
                        'Unjoinable',
                        )
        self.joinableFsm.enterInitialState()

        self.runableFsm = ClassicFSM.ClassicFSM('Runable',
                        [State.State('Runable',
                                self.enterRunable,
                                self.exitRunable,
                                ['Unrunable']),
                        State.State('Unrunable',
                                self.enterUnrunable,
                                self.exitUnrunable,
                                ['Runable'])],
                        # Initial state
                        'Unrunable',
                        # Final state
                        'Unrunable',
                        )
        self.runableFsm.enterInitialState()

        self.adjustFsm = ClassicFSM.ClassicFSM('Adjust',
                        [State.State('Adjusting',
                                self.enterAdjusting,
                                self.exitAdjusting,
                                ['NotAdjusting', 'Adjusting']),
                        State.State('NotAdjusting',
                                self.enterNotAdjusting,
                                self.exitNotAdjusting,
                                ['Adjusting'])],
                        # Initial state
                        'NotAdjusting',
                        # Final state
                        'NotAdjusting',
                        )
        self.adjustFsm.enterInitialState()
        self.fsm.enterInitialState()

        self.startTime = globalClock.getRealTime()
        self.adjustingTimer = Timer()
        

    def clearAttacks(self):
        """ clearAttacks()
        """
        self.toonAttacks = {}
        self.suitAttacks = getDefaultSuitAttacks()

    def requestDelete(self):
        if hasattr(self, 'fsm'):
            # We want to make sure the battle is no longer active once
            # we start deleting it.  If we don't do this, it may
            # continue to fire off tasks until the delete message
            # comes back from the server.
            self.fsm.request('Off')
        self.__removeTaskName(self.uniqueName('make-movie'))
        DistributedObjectAI.DistributedObjectAI.requestDelete(self)

    def delete(self):
        self.notify.debug('deleting battle')
        self.fsm.request('Off')
        self.ignoreAll()
        self.__removeAllTasks()
        del self.fsm
        del self.joinableFsm
        del self.runableFsm
        del self.adjustFsm
        self.__cleanupJoinResponses()
        self.timer.stop()
        del self.timer
        self.adjustingTimer.stop()
        del self.adjustingTimer
        self.battleCalc.cleanup()
        del self.battleCalc
        for suit in self.suits:
            del suit.battleTrap
        del self.finishCallback
        for petProxy in self.pets.values():
            petProxy.requestDelete()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def pause(self):
        self.timer.stop()
        self.adjustingTimer.stop()

    def unpause(self):
        self.timer.resume()
        self.adjustingTimer.resume()

    def abortBattle(self):

        """ Call this function to stop the battle in the middle, no
        matter what; the toons are sent back to the playground and the
        suits will fly away (or do whatever is appropriate for this
        kind of battle).  This is normally called only in response to
        a magic word. """

        self.notify.debug('%s.abortBattle() called.' % (self.doId))

        toonsCopy = self.toons[:]
        for toonId in toonsCopy:
            self.__removeToon(toonId)
            
            if (self.fsm.getCurrentState().getName() == 'PlayMovie' or
                self.fsm.getCurrentState().getName() == 'MakeMovie'):
                self.exitedToons.append(toonId)
                
        # Of course, the last toon is gone now.
        self.d_setMembers()

        self.b_setState('Resume')
        self.__removeAllTasks()
        self.timer.stop()
        self.adjustingTimer.stop()

    def __removeSuit(self, suit):
        self.notify.debug('__removeSuit(%d)' % suit.doId)
        assert(self.suits.count(suit) == 1)
        self.suits.remove(suit)
        assert(self.joiningSuits.count(suit) == 0)
        assert(self.pendingSuits.count(suit) == 0)
        assert(self.adjustingSuits.count(suit) == 0)
        assert(self.activeSuits.count(suit) == 1)
        self.activeSuits.remove(suit)
        if (self.luredSuits.count(suit) == 1):
            self.luredSuits.remove(suit)
        self.suitGone = 1
        del suit.battleTrap

    def findSuit(self, id):
        """ findSuit(id)
        """
        for s in self.suits:
            if (s.doId == id):
                return s
        return None

    def __removeTaskName(self, name):
        if (self.taskNames.count(name)):
            self.taskNames.remove(name)
            self.notify.debug('removeTaskName() - %s' % name)
            taskMgr.remove(name)

    def __removeAllTasks(self):
        for n in self.taskNames:
            self.notify.debug('removeAllTasks() - %s' % n)
            taskMgr.remove(n)
        self.taskNames = []

    def __removeToonTasks(self, toonId):
        name = self.taskName('running-toon-%d' % toonId)
        self.__removeTaskName(name)
        name = self.taskName('to-pending-av-%d' % toonId)
        self.__removeTaskName(name)

    # These are dummy getters for non-level battles. See toon.dc for
    # more info.
    def getLevelDoId(self):
        return 0
    def getBattleCellId(self):
        return 0

    # setPosition()

    def getPosition(self):
        """getPosition()
        """
        self.notify.debug('getPosition() - %s' % self.pos)
        return [self.pos[0], self.pos[1], self.pos[2]]

    # setInitialSuitPos()

    def getInitialSuitPos(self):
        """ getInitialSuitPos()
        """
        p = []
        p.append(self.initialSuitPos[0])
        p.append(self.initialSuitPos[1])
        p.append(self.initialSuitPos[2])
        return p

    # setBossBattle

    def setBossBattle(self, bossBattle):
        """call this before generate"""
        self.bossBattle = bossBattle

    def getBossBattle(self):
        return self.bossBattle

    # setState()

    def b_setState(self, state):
        self.notify.debug('network:setState(%s)' % state)
        stime = globalClock.getRealTime() + SERVER_BUFFER_TIME
        self.sendUpdate('setState', [state, globalClockDelta.localToNetworkTime(stime)])
        self.setState(state)

    def setState(self, state):
        self.fsm.request(state)

    def getState(self):
        return [self.fsm.getCurrentState().getName(),
                globalClockDelta.getRealNetworkTime()]

    # setMembers()

    def d_setMembers(self):
        self.notify.debug('network:setMembers()')
        self.sendUpdate('setMembers', self.getMembers())

    def getMembers(self):
        suits = []
        for s in self.suits:
            suits.append(s.doId)
        joiningSuits = ''
        for s in self.joiningSuits:
            joiningSuits += str(suits.index(s.doId))
        pendingSuits = ''
        for s in self.pendingSuits:
            pendingSuits += str(suits.index(s.doId))
        activeSuits = ''
        for s in self.activeSuits:
            activeSuits += str(suits.index(s.doId))
        luredSuits = ''
        for s in self.luredSuits:
            luredSuits += str(suits.index(s.doId))
        #import pdb; pdb.set_trace()
        suitTraps = ''
        for s in self.suits:
            if (s.battleTrap == NO_TRAP):
                suitTraps += '9'
            elif (s.battleTrap == BattleCalculatorAI.TRAP_CONFLICT):
                suitTraps += '9'
            else:
                suitTraps += str(s.battleTrap)
        toons = []
        for t in self.toons:
            toons.append(t)
        joiningToons = ''
        for t in self.joiningToons:
            joiningToons += str(toons.index(t))
        pendingToons = ''
        for t in self.pendingToons:
            pendingToons += str(toons.index(t))
        activeToons = ''
        for t in self.activeToons:
            activeToons += str(toons.index(t))
        runningToons = ''
        for t in self.runningToons:
            runningToons += str(toons.index(t))
        self.notify.debug('getMembers() - suits: %s joiningSuits: %s pendingSuits: %s activeSuits: %s luredSuits: %s suitTraps: %s toons: %s joiningToons: %s pendingToons: %s activeToons: %s runningToons: %s' % (suits, joiningSuits, pendingSuits, activeSuits, luredSuits, suitTraps, toons, joiningToons, pendingToons, activeToons, runningToons))
        return ([suits, joiningSuits, pendingSuits, activeSuits, luredSuits,
                 suitTraps, toons, joiningToons, pendingToons, activeToons,
                 runningToons, globalClockDelta.getRealNetworkTime()])

    # adjust()

    def d_adjust(self):
        self.notify.debug('network:adjust()')
        self.sendUpdate('adjust', [globalClockDelta.getRealNetworkTime()])
        
    # setInteractivePropTrackBonus

    def getInteractivePropTrackBonus(self):
        return self.interactivePropTrackBonus

    # setZoneId

    def getZoneId(self):
        return self.zoneId

    def getTaskZoneId(self):
        """ this function is here to allow subclasses override the zoneId
        that's used to determine task progress """
        return self.zoneId

    # setMovie

    def d_setMovie(self):
        self.notify.debug('network:setMovie()')
        self.sendUpdate('setMovie', self.getMovie())
        # this seems as good a place as any to update the suit encountered array
        # (we have to make sure the adjusting is all finished and activeToons us updated)
        self.__updateEncounteredCogs()

    def getMovie(self):
        suitIds = []
        for s in self.activeSuits:
            suitIds.append(s.doId)
        p = [self.movieHasBeenMade]
        p.append(self.activeToons)
        p.append(suitIds)
        for t in self.activeToons:
            if (self.toonAttacks.has_key(t)):
                ta = self.toonAttacks[t]
                index = -1
                id = ta[TOON_ID_COL]
                if (id != -1):
                    assert(self.activeToons.count(id))
                    index = self.activeToons.index(id)
                    #import pdb; pdb.set_trace()
                track = ta[TOON_TRACK_COL]
                if ((track == NO_ATTACK or
                     attackAffectsGroup(track, ta[TOON_LVL_COL])) and
                     track != NPCSOS and track != PETSOS):
                    target = -1
                    if (track == HEAL):
                        # If it's a joke, send a joke index number also
                        if (ta[TOON_LVL_COL] == 1):
                            ta[TOON_HPBONUS_COL] = random.randint(0, 10000)
                elif (track == SOS or track == NPCSOS or track == PETSOS):
                    
                    # We need to pass the actual doId in this case
                    target = ta[TOON_TGT_COL]
                elif (track == HEAL):
                    if self.activeToons.count(ta[TOON_TGT_COL]) != 0:
                        target = self.activeToons.index(ta[TOON_TGT_COL])
                    else:
                        target = -1
                else:
                    if suitIds.count(ta[TOON_TGT_COL]) != 0:
                        target = suitIds.index(ta[TOON_TGT_COL])
                    else:
                        target = -1
                p = p + [index,
                         track,
                         ta[TOON_LVL_COL],
                         target]
                p = p + ta[4:]
            else:
                index = self.activeToons.index(t)
                attack = getToonAttack(index)
                p = p + attack
        for i in range(4 - len(self.activeToons)):
            p = p + getToonAttack(-1)
        for sa in self.suitAttacks:
            index = -1
            id = sa[SUIT_ID_COL]
            if (id != -1):
                assert(suitIds.count(id))
                index = suitIds.index(id)
            if (sa[SUIT_ATK_COL] == -1):
                targetIndex = -1
            else:
                targetIndex = sa[SUIT_TGT_COL]
                assert(targetIndex < len(self.activeToons))
                if (targetIndex == -1):
                    self.notify.debug('suit attack: %d must be group' % \
                        sa[SUIT_ATK_COL])
                else:
                    toonId = self.activeToons[targetIndex]
            p = p + [index,
                     sa[SUIT_ATK_COL],
                     targetIndex]
            sa[SUIT_TAUNT_COL] = 0
            if (sa[SUIT_ATK_COL] != -1):
                suit = self.findSuit(id)
                assert(suit != None)
                sa[SUIT_TAUNT_COL] = getAttackTauntIndexFromIndex(suit,
                                                sa[SUIT_ATK_COL])
            p = p + sa[3:]
        return p

    # setChosenToonAttacks

    def d_setChosenToonAttacks(self):
        self.notify.debug('network:setChosenToonAttacks()')
        self.sendUpdate('setChosenToonAttacks', self.getChosenToonAttacks())

    def getChosenToonAttacks(self):
        ids = []
        tracks = []
        levels = []
        targets = []
        for t in self.activeToons:
            if (self.toonAttacks.has_key(t)):
                ta = self.toonAttacks[t]
            else:
                ta = getToonAttack(t)
            assert(t == ta[TOON_ID_COL])
            ids.append(t)
            tracks.append(ta[TOON_TRACK_COL])
            levels.append(ta[TOON_LVL_COL])
            targets.append(ta[TOON_TGT_COL])
        return [ids, tracks, levels, targets]

    # setBattleExperience

    def d_setBattleExperience(self):
        self.notify.debug('network:setBattleExperience()')
        self.sendUpdate('setBattleExperience', self.getBattleExperience())

    def getBattleExperience(self):
        #print ("DistributedBattleBaseAI -getBattleExperience- Active Toons %s" % (self.activeToons))
        returnValue = BattleExperienceAI.getBattleExperience(
            4, self.activeToons, self.toonExp,
            self.battleCalc.toonSkillPtsGained,
            self.toonOrigQuests, self.toonItems, self.toonOrigMerits, self.toonMerits,
            self.toonParts, self.suitsKilled, self.helpfulToons)
        #print ("DistributedBattleBaseAI -getBattleExperienceEnd- Active Toons %s" % (self.activeToons))
        return returnValue

    # Add suit
    
    def getToonUberStatus(self):
        #UBERCHANGE
        fieldList = []
        uberIndex = LAST_REGULAR_GAG_LEVEL + 1
        for toon in self.activeToons:
            toonList = []
            for trackIndex in range(MAX_TRACK_INDEX):
                toonList.append(toon.inventory.numItem(track, uberIndex))
            fieldList.append(encodeUber(toonList))
        return fieldList

    def addSuit(self, suit):
        self.notify.debug('addSuit(%d)' % suit.doId)
        self.newSuits.append(suit)
        self.suits.append(suit)

        # Initialize the suit trap
        suit.battleTrap = NO_TRAP
        self.numSuitsEver += 1
    
    def __joinSuit(self, suit):
        # calculate the time it will take for the suit to go from
        # its current position to its pending position in the battle
        # and create a task to call a function when that time has
        # passed
        #
        # Building battles can have 3 pending suits
        assert(len(self.pendingSuits) <= 3)
        assert(self.joiningSuits.count(suit) == 0)
        #spotIndex = len(self.pendingSuits) + len(self.joiningSuits)
        self.joiningSuits.append(suit)
        toPendingTime = MAX_JOIN_T + SERVER_BUFFER_TIME
        taskName = self.taskName('to-pending-av-%d' % suit.doId)
        self.__addJoinResponse(suit.doId, taskName)

        self.taskNames.append(taskName)
        taskMgr.doMethodLater(toPendingTime,
                              self.__serverJoinDone,
                              taskName,
                              extraArgs = (suit.doId, taskName))

    def __serverJoinDone(self, avId, taskName):
        self.notify.debug('join for av: %d timed out on server' % avId)
        self.__removeTaskName(taskName)
        self.__makeAvPending(avId)
        return Task.done

    def __makeAvPending(self, avId):
        self.notify.debug('__makeAvPending(%d)' % avId)
        self.__removeJoinResponse(avId)
        self.__removeTaskName(self.taskName('to-pending-av-%d' % avId))
        if (self.toons.count(avId) > 0):
            assert(self.joiningToons.count(avId) == 1)
            self.joiningToons.remove(avId)
            assert(self.pendingToons.count(avId) == 0)
            self.pendingToons.append(avId)
        else:
            suit = self.findSuit(avId)
            if (suit != None):
                if(not suit.isEmpty()):
                    # spam debug if the next assert is about to trigger
                    if not (self.joiningSuits.count(suit) == 1):
                        self.notify.warning('__makeAvPending(%d) in zone: %d' % (avId, self.zoneId))
                        self.notify.warning('toons: %s' % (self.toons))
                        self.notify.warning('joining toons: %s' % (self.joiningToons))
                        self.notify.warning('pending toons: %s' % (self.pendingToons))
                        self.notify.warning('suits: %s' % (self.suits))
                        self.notify.warning('joining suits: %s' % (self.joiningSuits))
                        self.notify.warning('pending suits: %s' % (self.pendingSuits))
                    assert(self.joiningSuits.count(suit) == 1)
                    self.joiningSuits.remove(suit)
                    assert(self.pendingSuits.count(suit) == 0)
                    self.pendingSuits.append(suit)
            else:
                self.notify.warning('makeAvPending() %d not in toons or suits' \
                        % avId)
                return
        self.d_setMembers()
        self.needAdjust = 1
        self.__requestAdjust()

    def suitRequestJoin(self, suit):
        """ suitRequestJoin(suit)
        """
        self.notify.debug('suitRequestJoin(%d)' % suit.getDoId())
        # make sure we're not trying to add a suit that's
        # already in this battle
        assert (suit not in self.suits), 'suit already in this battle'
        if (self.suitCanJoin()):
            self.addSuit(suit)
            self.__joinSuit(suit)
            self.d_setMembers()
            suit.prepareToJoinBattle()
            return 1
        else:
            self.notify.warning('suitRequestJoin() - not joinable - joinable state: %s max suits: %d' % (self.joinableFsm.getCurrentState().getName(),
                        self.maxSuits))
            return 0

    # Add/Remove toon

    def addToon(self, avId):
        print ("DBB-addToon %s" % (avId))
        # Returns 1 if the toon is successfully added, 0 otherwise.
        
        self.notify.debug('addToon(%d)' % avId)
        toon = self.getToon(avId)
        if (toon == None):
            return 0

        # Make sure the playground (or estate) toon-up task isn't
        # still running on this Toon.  It shouldn't be, but if it is
        # we'll get very mysterious effects during the battle movie.
        toon.stopToonUp()

        # Prepare to handle an unexpected exit by the avatar
        event = simbase.air.getAvatarExitEvent(avId)
        self.avatarExitEvents.append(event)
        self.accept(event, self.__handleUnexpectedExit, extraArgs=[avId])

        # Also handle avatars that manage to escape to the safezone
        # somehow.
        event = "inSafezone-%s" % (avId)
        self.avatarExitEvents.append(event)
        self.accept(event, self.__handleSuddenExit, extraArgs=[avId, 0])

        self.newToons.append(avId)
        self.toons.append(avId)
        
        toon = simbase.air.doId2do.get(avId)
        if toon:
            if hasattr(self, "doId"):
                toon.b_setBattleId(self.doId)
            else:
                toon.b_setBattleId(-1)
            messageToonAdded = ("Battle adding toon %s" % (avId))
            messenger.send(messageToonAdded, [avId])

        assert(not self.responses.has_key(avId))
        if (self.fsm != None and
            self.fsm.getCurrentState().getName() == 'PlayMovie'):
            self.responses[avId] = 1
        else:
            self.responses[avId] = 0
        assert(not self.adjustingResponses.has_key(avId))
        self.adjustingResponses[avId] = 0

        # Initialize experience per track
        if avId not in self.toonExp:
            p = []
            for t in Tracks:
                p.append(toon.experience.getExp(t))
            self.toonExp[avId] = p

        # Initialize original merits
        if avId not in self.toonOrigMerits:
            self.toonOrigMerits[avId] = toon.cogMerits[:]

        # Initialize merits earned
        if avId not in self.toonMerits:
            self.toonMerits[avId] = [0, 0, 0, 0]

        # Initialize parts found
        if avId not in self.toonOrigQuests:
            # we need to flatten the quests to send them over the wire
            flattenedQuests = []
            for quest in toon.quests:
                flattenedQuests.extend(quest)
            self.toonOrigQuests[avId] = flattenedQuests
            
        # Initialize parts found
        if avId not in self.toonItems:
            self.toonItems[avId] = ([], [])

        return 1

    def __joinToon(self, avId, pos):
        # calculate the time it will take for the toon to go from
        # its current position to its position in the battle and
        # create a task to call a function when that time has passed
        #
        assert(pos != None)
        #assert(len(self.pendingToons) < 3)
        assert(self.joiningToons.count(avId) == 0)
        #spotIndex = len(self.pendingToons) + len(self.joiningToons)
        self.joiningToons.append(avId)
        toPendingTime = MAX_JOIN_T + SERVER_BUFFER_TIME
        taskName = self.taskName('to-pending-av-%d' % avId)
        self.__addJoinResponse(avId, taskName, toon=1)
        taskMgr.doMethodLater(toPendingTime,
                              self.__serverJoinDone,
                              taskName,
                              extraArgs = (avId, taskName))
        self.taskNames.append(taskName)


    def __updateEncounteredCogs(self):
        # If there is a new toon, add all the active suits to the encounter list.
        for toon in self.activeToons:
            if toon in self.newToons:
                # add any suits present to the suits encountered list
                for suit in self.activeSuits:
                    if hasattr(suit, 'dna'):
                        self.suitsEncountered.append({'type': suit.dna.name,
                                                      # Put a copy of active toons in the dict
                                                      # Only they get credit for seeing this suit
                                                      'activeToons': self.activeToons[:]})
                    else:
                        self.notify.warning('Suit has no DNA in zone %s: toons involved = %s' % (self.zoneId, self.activeToons))
                        # fail hard
                        return
                self.newToons.remove(toon)

        # If there is a new suit, add it to all active toons encounter list.
        for suit in self.activeSuits:
            if suit in self.newSuits:
                if hasattr(suit, 'dna'):
                    # add any new suits to all active toons encounter list
                    self.suitsEncountered.append({'type': suit.dna.name,
                                                  # Put a copy of active toons in the dict
                                                  # Only they get credit for seeing this suit
                                                  'activeToons': self.activeToons[:]})
                else:
                    self.notify.warning('Suit has no DNA in zone %s: toons involved = %s' % (self.zoneId, self.activeToons))
                    # fail hard
                    return
                self.newSuits.remove(suit)


    def __makeToonRun(self, toonId, updateAttacks):
        assert(self.activeToons.count(toonId) == 1)
        self.activeToons.remove(toonId)
        assert(self.runningToons.count(toonId) == 0)
        # We want adjusting to occur
        self.toonGone = 1
        self.runningToons.append(toonId)
        taskName = self.taskName('running-toon-%d' % toonId)
        taskMgr.doMethodLater(TOON_RUN_T,
                              self.__serverRunDone,
                              taskName,
                              extraArgs = (toonId, updateAttacks, taskName))
        self.taskNames.append(taskName)

    def __serverRunDone(self, toonId, updateAttacks, taskName):
        self.notify.debug('run for toon: %d timed out on server' % toonId)
        self.__removeTaskName(taskName)
        self.__removeToon(toonId)
        self.d_setMembers()
        if (len(self.toons) == 0):
            self.notify.debug('last toon is gone - battle is finished')
            self.b_setState('Resume')
        else:
            if (updateAttacks == 1):
                self.d_setChosenToonAttacks()
            self.needAdjust = 1
            self.__requestAdjust()
        return Task.done

    def __requestAdjust(self):
        """ Only the server can initiate an adjust
        """
        if (not self.fsm):
            return

        cstate = self.fsm.getCurrentState().getName()
        if (cstate == 'WaitForInput' or cstate == 'WaitForJoin'):
            if (self.adjustFsm.getCurrentState().getName() == 'NotAdjusting'):
                if (self.needAdjust == 1):
                    self.d_adjust()
                    self.adjustingSuits = []
                    for s in self.pendingSuits:
                        self.adjustingSuits.append(s)
                    self.adjustingToons = []
                    for t in self.pendingToons:
                        self.adjustingToons.append(t)
                    self.adjustFsm.request('Adjusting')
                else:
                    self.notify.debug('requestAdjust() - dont need to')
            else:
                self.notify.debug('requestAdjust() - already adjusting')
        else:
            self.notify.debug('requestAdjust() - in state: %s' % cstate)

    def __handleUnexpectedExit(self, avId):
        disconnectCode = self.air.getAvatarDisconnectReason(avId)
        self.notify.warning('toon: %d exited unexpectedly, reason %d' % (avId, disconnectCode))

        # We consider the user to have disconnected unfairly if he
        # exited because of a window closure.  For any other reason,
        # we give him the benefit of a doubt (maybe an internet
        # hiccup, maybe a client crash).
        userAborted = (disconnectCode == ToontownGlobals.DisconnectCloseWindow)

        self.__handleSuddenExit(avId, userAborted)
        
    def __handleSuddenExit(self, avId, userAborted):
        self.__removeToon(avId, userAborted=userAborted)
        if (self.fsm.getCurrentState().getName() == 'PlayMovie' or
            self.fsm.getCurrentState().getName() == 'MakeMovie'):
            self.exitedToons.append(avId)
        # See if the last toon is gone
        self.d_setMembers()
        if (len(self.toons) == 0):
            self.notify.debug('last toon is gone - battle is finished')
            self.__removeAllTasks()
            self.timer.stop()
            self.adjustingTimer.stop()
            self.b_setState('Resume')

        else:
            self.needAdjust = 1
            self.__requestAdjust()

    def __removeSuit(self, suit):
        self.notify.debug('__removeSuit(%d)' % suit.doId)
        assert(self.suits.count(suit) == 1)
        self.suits.remove(suit)
        assert(self.joiningSuits.count(suit) == 0)
        assert(self.pendingSuits.count(suit) == 0)
        assert(self.adjustingSuits.count(suit) == 0)
        assert(self.activeSuits.count(suit) == 1)
        self.activeSuits.remove(suit)
        if (self.luredSuits.count(suit) == 1):
            self.luredSuits.remove(suit)
        self.suitGone = 1
        del suit.battleTrap

    def __removeToon(self, toonId, userAborted=0):
        """remove a toon before victory is achieved (run away, get sad,
        disconnect)"""
        self.notify.debug('__removeToon(%d)' % toonId)
        if self.toons.count(toonId) == 0:
            return

        assert(self.toons.count(toonId) == 1)
        # inform the battleCalculator that the toon is leaving the battle
        # WARNING: this will delete any accumulated experience in the
        # calc's toonSkillPtsGained dict; for parts of the game that
        # accumulate experience over multiple battles, this will destroy
        # the toon's accumulated experience. It seems like a safe assumption
        # that running away, getting sad, or disconnecting should void a
        # toon's accumulated experience.
        self.battleCalc.toonLeftBattle(toonId)
        self.__removeToonTasks(toonId)
        self.toons.remove(toonId)
        if (self.joiningToons.count(toonId) == 1):
            self.joiningToons.remove(toonId)
        if (self.pendingToons.count(toonId) == 1):
            self.pendingToons.remove(toonId)
        if (self.activeToons.count(toonId) == 1):
            # Update suitAttack HP indices, which need to match activeToon list.
            activeToonIdx = self.activeToons.index(toonId)
            self.notify.debug("removing activeToons[%d], updating suitAttacks SUIT_HP_COL to match" % activeToonIdx)
            for i in range(len(self.suitAttacks)):
                if activeToonIdx < len(self.suitAttacks[i][SUIT_HP_COL]):
                    del self.suitAttacks[i][SUIT_HP_COL][activeToonIdx]
                else:
                    self.notify.warning("suitAttacks %d doesn't have an HP column for active toon index %d" % (i, activeToonIdx))
            self.activeToons.remove(toonId)
        if (self.runningToons.count(toonId) == 1):
            self.runningToons.remove(toonId)
        if (self.adjustingToons.count(toonId) == 1):
            self.notify.warning('removeToon() - toon: %d was adjusting!' % \
                toonId)
            self.adjustingToons.remove(toonId)
        self.toonGone = 1

        # Delete this Toon's pet proxy
        if self.pets.has_key(toonId):
            self.pets[toonId].requestDelete()
            del self.pets[toonId]

        # Trigger all the necessary client responses
        self.__removeResponse(toonId)
        self.__removeAdjustingResponse(toonId)
        self.__removeJoinResponses(toonId)

        # Ignore future avatar exit events
        event = simbase.air.getAvatarExitEvent(toonId)
        self.avatarExitEvents.remove(event)
        self.ignore(event)

        # And also stop listening for "avatar escaped" events.
        event = "inSafezone-%s" % (toonId)
        self.avatarExitEvents.remove(event)
        self.ignore(event)
        
        toon = simbase.air.doId2do.get(toonId)
        if toon:
            toon.b_setBattleId(0)
            messageToonReleased = ("Battle releasing toon %s" % (toon.doId))
            messenger.send(messageToonReleased, [toon.doId])

        if (not userAborted):
            # The toon exited the battle, but he may still be in the
            # game.  In case he is, make sure he knows his current HP
            # and inventory.  (He might have crashed out and left the
            # game, but that's ok too.)
            toon = self.getToon(toonId)
            if (toon != None):
                toon.hpOwnedByBattle = 0
                toon.d_setHp(toon.hp)
                toon.d_setInventory(toon.inventory.makeNetString())
                # Tell the cog page manager about the cogs this toon encountered
                self.air.cogPageManager.toonEncounteredCogs(toon, self.suitsEncountered,
                                                            self.getTaskZoneId())
        else:
            # In this case, the toon exited the battle abnormally--he
            # explicitly disconnected.  The toon is no longer in
            # the game, so we can no longer query his current HP or
            # inventory, and we can't update the cog page manager or
            # anything like that.

            if len(self.suits) > 0 and not self.streetBattle:
                # If the toon was in a building battle, and there are
                # still some suits left to the battle, assume the
                # player cheated by pulling the plug or something and
                # impose a penalty.  (We don't impose this penalty for
                # a street battle because the user can always run from
                # a street battle.)

                self.notify.info("toon %d aborted non-street battle; clearing inventory and hp." % (toonId))

                # This is a little tricky because the toon is already
                # gone.  First, we have to create an empty
                # DistributedToonAI object to represent the toon.
                # There is no useful data in this object, so we can't
                # query his hp or anything.
                toon = DistributedToonAI.DistributedToonAI(self.air)
                toon.doId = toonId

                # Now set the inventory and HP to nothing.
                empty = InventoryBase.InventoryBase(toon)
                toon.b_setInventory(empty.makeNetString())
                toon.b_setHp(0)

                # And write these two fields directly to the database.
                db = DatabaseObject.DatabaseObject(self.air, toonId)
                db.storeObject(toon, ["setInventory", "setHp"])

                self.notify.info('killing mem leak from temporary DistributedToonAI %d' % toonId)
                toon.deleteDummy()
                

    def getToon(self, toonId):
        if (self.air.doId2do.has_key(toonId)):
            return self.air.doId2do[toonId]
        else:
            self.notify.warning('getToon() - toon: %d not in repository!' \
                % toonId)
        return None

    # Messages from DistributedBattle

    def toonRequestRun(self):
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
            self.notify.debug('ignoring response from toon: %d' % toonId)
            return
        self.notify.debug('toonRequestRun(%d)' % toonId)
        if (not self.isRunable()):
            self.notify.warning('toonRequestRun() - not runable')
            return
        updateAttacks = 0
        if (self.activeToons.count(toonId) == 0):
            self.notify.warning('toon tried to run, but not found in activeToons: %d'
                                % toonId)
            return

        # See if anyone else is trying to heal the running toon
        for toon in self.activeToons:
            if (self.toonAttacks.has_key(toon)):
                ta = self.toonAttacks[toon]
                track = ta[TOON_TRACK_COL]
                level = ta[TOON_LVL_COL]
                if (ta[TOON_TGT_COL] == toonId or
                    (track == HEAL and attackAffectsGroup(track, level) and
                     len(self.activeToons) <= 2)):
                    healerId = ta[TOON_ID_COL]
                    self.notify.debug('resetting toon: %ds attack' % \
                        healerId)
                    self.toonAttacks[toon] = getToonAttack(toon,
                                                           track=UN_ATTACK)
                    assert(self.responses.has_key(healerId))
                    self.responses[healerId] = 0
                    updateAttacks = 1
        self.__makeToonRun(toonId, updateAttacks)
        self.d_setMembers()
        self.needAdjust = 1
        self.__requestAdjust()

    def toonRequestJoin(self, x, y, z):
        toonId = self.air.getAvatarIdFromSender()
        self.notify.debug('toonRequestJoin(%d)' % toonId)
        self.signupToon(toonId, x, y, z)

    def toonDied(self):
        toonId = self.air.getAvatarIdFromSender()
        self.notify.debug('toonDied(%d)' % toonId)

        if toonId in self.toons:
            toon = self.getToon(toonId)
            if toon:
                toon.hp = -1
                toon.inventory.zeroInv(1)
                self.__handleSuddenExit(toonId, 0)
        

    def signupToon(self, toonId, x, y, z):
        """ signupToon(toonId, x, y, z)

        Adds the toon to the battle.  This can be requested directly
        by the toon (via toonRequestJoin) or by the AI.
        """
        if (self.toons.count(toonId)):
            # If the toon is already part of this battle, ignore the
            # message completely.  Don't even send back a deny
            # message, which would just confuse the client.
            return
        
        if (self.toonCanJoin()):
            if self.addToon(toonId):
                self.__joinToon(toonId, Point3(x, y, z))
                self.d_setMembers()
        else:
            self.notify.warning('toonRequestJoin() - not joinable')
            self.d_denyLocalToonJoin(toonId)

    def d_denyLocalToonJoin(self, toonId):
        self.notify.debug('network: denyLocalToonJoin(%d)' % toonId)
        self.sendUpdateToAvatarId(toonId, 'denyLocalToonJoin', [])

    ##### WaitForInput Responses #####

    def resetResponses(self):
        self.responses = {}
        for t in self.toons:
            self.responses[t] = 0
        self.ignoreResponses = 0

    def allToonsResponded(self):
        for t in self.toons:
            assert(self.responses.has_key(t))
            if (self.responses[t] == 0):
                return 0
        self.ignoreResponses = 1
        return 1

    def __allPendingActiveToonsResponded(self):
        for t in (self.pendingToons + self.activeToons):
            assert(self.responses.has_key(t))
            if (self.responses[t] == 0):
                return 0
        self.ignoreResponses = 1
        return 1

    def __allActiveToonsResponded(self):
        for t in self.activeToons:
            assert(self.responses.has_key(t))
            if (self.responses[t] == 0):
                return 0
        self.ignoreResponses = 1
        return 1

    def __removeResponse(self, toonId):
        assert(self.responses.has_key(toonId))
        del self.responses[toonId]
        if (self.ignoreResponses == 0 and (len(self.toons) > 0)):
            currStateName = self.fsm.getCurrentState().getName()
            if (currStateName == 'WaitForInput'):
                if (self.__allActiveToonsResponded()):
                    self.notify.debug('removeResponse() - dont wait for movie')
                    self.__requestMovie()
            elif (currStateName == 'PlayMovie'):
                if (self.__allPendingActiveToonsResponded()):
                    self.notify.debug('removeResponse() - surprise movie done')
                    self.__movieDone()
            elif (currStateName == 'Reward' or currStateName == 'BuildingReward'):
                if (self.__allActiveToonsResponded()):
                    self.notify.debug('removeResponse() - surprise reward done')
                    self.handleRewardDone()

    ##### Adjust Responses #####

    def __resetAdjustingResponses(self):
        self.adjustingResponses = {}
        for t in self.toons:
            self.adjustingResponses[t] = 0
        self.ignoreAdjustingResponses = 0

    def __allAdjustingToonsResponded(self):
        for t in self.toons:
            assert(self.adjustingResponses.has_key(t))
            if (self.adjustingResponses[t] == 0):
                return 0
        self.ignoreAdjustingResponses = 1
        return 1

    def __removeAdjustingResponse(self, toonId):
        if (self.adjustingResponses.has_key(toonId)):
            del self.adjustingResponses[toonId]
            if (self.ignoreAdjustingResponses == 0 and (len(self.toons) > 0)):
                if (self.__allAdjustingToonsResponded()):
                    self.__adjustDone()

    ##### Join Responses #####

    def __addJoinResponse(self, avId, taskName, toon=0):
        """ Add self as a responder to any other avatar that is joining
            the battle if it's a toon, then create a response dictionary
            for self to join the battle
        """
        if (toon == 1):
            for jr in self.joinResponses.values():
                jr[avId] = 0
        assert(not self.joinResponses.has_key(avId))
        self.joinResponses[avId] = {}
        for t in self.toons:
            self.joinResponses[avId][t] = 0
        self.joinResponses[avId]['taskName'] = taskName

    def __removeJoinResponses(self, avId):
        """ Remove a response dictionary for self joining the battle (if
            one exists), and remove self from any other existing response
            dictionaries
        """
        self.__removeJoinResponse(avId)
        removedOne = 0
        for j in self.joinResponses.values():
            if (j.has_key(avId)):
                del j[avId]
                removedOne = 1
        if (removedOne == 1):
            # See if the join has finished everywhere else
            for t in self.joiningToons:
                if (self.__allToonsRespondedJoin(t)):
                    self.__makeAvPending(t)

    def __removeJoinResponse(self, avId):
        """ Remove a response dictionary for self joining the battle (if
            one exists)
        """
        if (self.joinResponses.has_key(avId)):
            taskMgr.remove(self.joinResponses[avId]['taskName'])
            del self.joinResponses[avId]

    def __allToonsRespondedJoin(self, avId):
        """ Return 1 if all toons in battle have responded that avId has
            successfully joined and is in the pending list
        """
        assert(self.joinResponses.has_key(avId))
        jr = self.joinResponses[avId]
        for t in self.toons:
            assert(jr.has_key(t))
            if (jr[t] == 0):
                return 0
        return 1

    def __cleanupJoinResponses(self):
        for jr in self.joinResponses.values():
            taskMgr.remove(jr['taskName'])
            del jr

    ##### Client Response Messages #####

    def adjustDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreAdjustingResponses == 1):
            self.notify.debug('adjustDone() - ignoring toon: %d' % toonId)
            return
        elif (self.adjustFsm.getCurrentState().getName() != 'Adjusting'):
            self.notify.warning('adjustDone() - in state %s' % \
                self.fsm.getCurrentState().getName())
            return
        elif (self.toons.count(toonId) == 0):
            self.notify.warning('adjustDone() - toon: %d not in toon list' % \
                toonId)
            return
        assert(self.adjustingResponses.has_key(toonId))
        self.adjustingResponses[toonId] += 1
        self.notify.debug('toon: %d done adjusting' % toonId)
        if (self.__allAdjustingToonsResponded()):
            self.__adjustDone()

    def timeout(self):
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
            self.notify.debug('timeout() - ignoring toon: %d' % toonId)
            return
        elif (self.fsm.getCurrentState().getName() != 'WaitForInput'):
            self.notify.warning('timeout() - in state: %s' % \
                        self.fsm.getCurrentState().getName())
            return
        elif (self.toons.count(toonId) == 0):
            self.notify.warning('timeout() - toon: %d not in toon list' % \
                toonId)
            return
        self.toonAttacks[toonId] = getToonAttack(toonId)
        self.d_setChosenToonAttacks()
        assert(self.responses.has_key(toonId))
        self.responses[toonId] += 1
        self.notify.debug('toon: %d timed out' % toonId)
        if (self.__allActiveToonsResponded()):
            self.__requestMovie(timeout=1)

    def movieDone(self):
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
            self.notify.debug('movieDone() - ignoring toon: %d' % toonId)
            return
        elif (self.fsm.getCurrentState().getName() != 'PlayMovie'):
            self.notify.warning('movieDone() - in state %s' % \
                self.fsm.getCurrentState().getName())
            return
        elif (self.toons.count(toonId) == 0):
            self.notify.warning('movieDone() - toon: %d not in toon list' % \
                toonId)
            return
        assert(self.responses.has_key(toonId))
        self.responses[toonId] += 1
        self.notify.debug('toon: %d done with movie' % toonId)
        if (self.__allPendingActiveToonsResponded()):
            self.__movieDone()
        else:
            # Reset the timer to give the slowpokes a few seconds
            # longer than the first (or most recent) toon to reply.
            self.timer.stop()
            self.timer.startCallback(TIMEOUT_PER_USER, self.__serverMovieDone)


    def rewardDone(self):
        """ rewardDone()
        """
        toonId = self.air.getAvatarIdFromSender()
        stateName = self.fsm.getCurrentState().getName()
        if (self.ignoreResponses == 1):
            self.notify.debug('rewardDone() - ignoring toon: %d' % toonId)
            return
        elif (stateName not in ('Reward', 'BuildingReward', 'FactoryReward',
                                'MintReward', 'StageReward', 'CountryClubReward')):
            self.notify.warning('rewardDone() - in state %s' % stateName)
            return
        elif (self.toons.count(toonId) == 0):
            self.notify.warning('rewardDone() - toon: %d not in toon list' % \
                toonId)
            return
        assert(self.responses.has_key(toonId))
        self.responses[toonId] += 1
        self.notify.debug('toon: %d done with reward' % toonId)
        if (self.__allActiveToonsResponded()):
            self.handleRewardDone()
        else:
            # Reset the timer to give the slowpokes a few seconds
            # longer than the first (or most recent) toon to reply.
            self.timer.stop()
            self.timer.startCallback(TIMEOUT_PER_USER, self.serverRewardDone)

    def assignRewards(self):
        if (self.rewardHasPlayed == 1):
            self.notify.debug('handleRewardDone() - reward has already played')
            return
        self.rewardHasPlayed = 1

        BattleExperienceAI.assignRewards(
            self.activeToons, self.battleCalc.toonSkillPtsGained,
            self.suitsKilled, self.getTaskZoneId(), self.helpfulToons)

    def joinDone(self, avId):
        """ joinDone(avId)
        """
        toonId = self.air.getAvatarIdFromSender()
        if (self.toons.count(toonId) == 0):
            self.notify.warning('joinDone() - toon: %d not in toon list' % \
                toonId)
            return
        if (not self.joinResponses.has_key(avId)):
            self.notify.debug('joinDone() - no entry for: %d - ignoring: %d' \
                % (avId, toonId))
            return
        jr = self.joinResponses[avId]
        if (jr.has_key(toonId)):
            jr[toonId] += 1
        self.notify.debug('client with localToon: %d done joining av: %d' % \
                (toonId, avId))
        if (self.__allToonsRespondedJoin(avId)):
            self.__makeAvPending(avId)

    def requestAttack(self, track, level, av):
        """ requestAttack(track, level, av)
        """
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
            self.notify.debug('requestAttack() - ignoring toon: %d' % toonId)
            return
        elif (self.fsm.getCurrentState().getName() != 'WaitForInput'):
            self.notify.warning('requestAttack() - in state: %s' % \
                        self.fsm.getCurrentState().getName())
            return
        elif (self.activeToons.count(toonId) == 0):
            self.notify.warning('requestAttack() - toon: %d not in toon list' \
                % toonId)
            return
        self.notify.debug('requestAttack(%d, %d, %d, %d)' % (toonId, track, \
                level, av))
        toon = self.getToon(toonId)
        if (toon == None):
            self.notify.warning('requestAttack() - no toon: %d' % toonId)
            return
        assert(toon.inventory != None)
        validResponse = 1
        if (track == SOS):
            # TODO: security breach.  We should validate that the
            # avatar is a friend of the toon here, if possible.  Can
            # we do that?
            self.notify.debug('toon: %d calls for help' % toonId)
            self.air.writeServerEvent('friendSOS', toonId, '%s' % (av))
            self.toonAttacks[toonId] = getToonAttack(toonId, track=SOS,
                                                     target=av)
        elif (track == NPCSOS):
            self.notify.debug('toon: %d calls for help' % toonId)
            self.air.writeServerEvent('NPCSOS', toonId, '%s' % (av))
            # Make sure the toon has the friend, and then remove it
            toon = self.getToon(toonId)
            if (toon == None):
                return 
            if (toon.NPCFriendsDict.has_key(av)): 
                npcCollision = 0
                if (self.npcAttacks.has_key(av)):
                    callingToon = self.npcAttacks[av]
                    if (self.activeToons.count(callingToon) == 1):
                        self.toonAttacks[toonId] = getToonAttack(toonId, track=PASS)
                        npcCollision = 1
                if (npcCollision == 0):
                    # MPG - in case people hit the back button, we
                    # need to delete SOS toons in movieDone()
                    #toon.NPCFriendsDict[av] -= 1
                    #if (toon.NPCFriendsDict[av] <= 0):
                    #    del toon.NPCFriendsDict[av]
                    #toon.d_setNPCFriendsDict(toon.NPCFriendsDict)
                    self.toonAttacks[toonId] = getToonAttack(toonId, 
                                track=NPCSOS, level=5, target=av)
                    self.numNPCAttacks += 1
                    self.npcAttacks[av] = toonId
                    #import pdb; pdb.set_trace()
            
        elif (track == PETSOS):
            self.notify.debug('toon: %d calls for pet: %d' % (toonId, av))
            self.air.writeServerEvent('PETSOS', toonId, '%s' % (av))
            # Make sure the toon has the pet
            toon = self.getToon(toonId)
            if (toon == None):
                return
            if not self.validate(toonId, (level in toon.petTrickPhrases), 'requestAttack: invalid pet trickId: %s' % (level)):
                return
            self.toonAttacks[toonId] = getToonAttack(toonId, 
                                track=PETSOS, level=level, target=av)
        elif (track == UN_ATTACK):
            self.notify.debug('toon: %d changed its mind' % toonId)
            self.toonAttacks[toonId] = getToonAttack(toonId, track=UN_ATTACK)
            if (self.responses.has_key(toonId)):
                self.responses[toonId] = 0
            validResponse = 0
        elif (track == PASS):
            assert(self.notify.debug('toon: %d passed' % toonId))
            self.toonAttacks[toonId] = getToonAttack(toonId, track=PASS)
        elif (track == FIRE):
            #assert(self.notify.debug('toon: %d passed' % toonId))
            self.toonAttacks[toonId] = getToonAttack(toonId, track=FIRE, target=av)

        else:
            # If the track is not one of the above special values, it
            # must be one of the valid tracks in
            # ToontownBattleGlobals.
            if not self.validate(toonId, (track >= 0 and track <= MAX_TRACK_INDEX),
                                 'requestAttack: invalid track %s' % (track)):
                return
            if not self.validate(toonId, (level >= 0 and level <= (MAX_LEVEL_INDEX)),
                                 'requestAttack: invalid level %s' % (level)):
                return 

            # For now, we assume that the avId is being correctly
            # validated downstream of here.
           
            if (toon.inventory.numItem(track, level) == 0):
                # TODO: fix BUG: Somehow, this clause is getting executed when
                # the toon still has one prop left...
                self.notify.warning('requestAttack() - toon has no item track: \
                    %d level: %d' % (track, level))
                self.toonAttacks[toonId] = getToonAttack(toonId)
                return
            
            if (track == HEAL):
                # See if the target for the heal is running away
                if (self.runningToons.count(av) == 1 or
                    (attackAffectsGroup(track, level) and
                     len(self.activeToons) < 2)):
                    assert(self.notify.debug('resetting toon: %ds attack' % \
                        toonId))
                    self.toonAttacks[toonId] = getToonAttack(toonId,
                                                             track=UN_ATTACK)
                    validResponse = 0
                else:
                    self.toonAttacks[toonId] = getToonAttack(toonId, track=track,
                                                    level=level, target=av)
            else:
                self.toonAttacks[toonId] = getToonAttack(toonId, track=track,
                                                    level=level, target=av)
                if (av == -1 and not attackAffectsGroup(track, level)):
                    # No target yet; it's not yet a complete attack.
                    validResponse = 0


        self.d_setChosenToonAttacks()
        assert(self.responses.has_key(toonId))
        if (validResponse == 1):
            self.responses[toonId] += 1
        self.notify.debug('toon: %d chose an attack' % toonId)
        if (self.__allActiveToonsResponded()):
            self.__requestMovie()

    def requestPetProxy(self, av):
        toonId = self.air.getAvatarIdFromSender()
        if (self.ignoreResponses == 1):
            self.notify.debug('requestPetProxy() - ignoring toon: %d' % toonId)
            return
        elif (self.fsm.getCurrentState().getName() != 'WaitForInput'):
            self.notify.warning('requestPetProxy() - in state: %s' % \
                        self.fsm.getCurrentState().getName())
            return
        elif (self.activeToons.count(toonId) == 0):
            self.notify.warning('requestPetProxy() - toon: %d not in toon list' \
                % toonId)
            return
        self.notify.debug('requestPetProxy(%s, %s)' % (toonId, av))
        toon = self.getToon(toonId)
        if (toon == None):
            self.notify.warning('requestPetProxy() - no toon: %d' % toonId)
            return

        petId = toon.getPetId() 
        zoneId = self.zoneId
        if (petId == av):
            # See if pet has been generated already
            #if simbase.air.doId2do.has_key(petId):
                # Make sure to move it to the new zone
                #petProxy = simbase.air.doId2do[petId]
                #simbase.air.sendSetZone(petProxy, zoneId)
                #petProxy.zoneId = zoneId
            if not self.pets.has_key(toonId):
                def handleGetPetProxy(success, petProxy, petId=petId, zoneId=zoneId, toonId=toonId):
                    if success:
                        if petId not in simbase.air.doId2do:
                            simbase.air.requestDeleteDoId(petId)
                        else:
                            petDO = simbase.air.doId2do[petId]
                            petDO.requestDelete()
                            simbase.air.deleteDistObject(petDO)
                        petProxy.dbObject = 1                                    
                        petProxy.generateWithRequiredAndId(petId, 
                                                           self.air.districtId,
                                                           zoneId)
                        petProxy.broadcastDominantMood()
                        self.pets[toonId] = petProxy
                    else:
                        self.notify.warning("error generating petProxy: %s" % petId)
                self.getPetProxyObject(petId, handleGetPetProxy)

    # Misc

    def suitCanJoin(self):
        return ((len(self.suits) < self.maxSuits) and (self.isJoinable()))

    def toonCanJoin(self):
        return ((len(self.toons) < 4) and (self.isJoinable()))

    def __requestMovie(self, timeout=0):
        #import pdb; pdb.set_trace()
        if (self.adjustFsm.getCurrentState().getName() == 'Adjusting'):
            self.notify.debug('__requestMovie() - in Adjusting')
            self.movieRequested = 1
        else:
            movieDelay = 0
            if (len(self.activeToons) == 0):
                self.notify.warning('only pending toons left in battle %s, toons = %s' % (self.doId, self.toons))
            elif (len(self.activeSuits) == 0):
                self.notify.warning('only pending suits left in battle %s, suits = %s' % (self.doId, self.suits))
            elif (len(self.activeToons) > 1 and not timeout):
                # If there are multiple toons involved in the battle,
                # pad the start of the movie by 1 second so other
                # toons can see what the last toon chose as his attack
                movieDelay = 1

            self.fsm.request('MakeMovie')
            if movieDelay:
                taskMgr.doMethodLater(0.8, self.__makeMovie,
                                    self.uniqueName('make-movie'))
                self.taskNames.append(self.uniqueName('make-movie'))
            else:
                self.__makeMovie()


    def __makeMovie(self, task=None):
        self.notify.debug('makeMovie()')
        assert(self.isGenerated())
        assert(self.fsm.getCurrentState().getName() == 'MakeMovie')
        # I think the factory battle crash has to do with this doLater firing
        # after the battle has requested delete and before delete is called.
        # See commented-out implementation of requestDelete for proposed
        # solution if this is the case (I could not repro the crash)
        if self._DOAI_requestedDelete:
            self.notify.warning(
                'battle %s requested delete, then __makeMovie was called!' %
                self.doId)
            if hasattr(self, 'levelDoId'):
                self.notify.warning('battle %s in level %s' % (
                    self.doId, self.levelDoId))
            return
        
        self.__removeTaskName(self.uniqueName('make-movie'))
        if (self.movieHasBeenMade == 1):
            self.notify.debug('__makeMovie() - movie has already been made')
            return
        self.movieRequested = 0
        self.movieHasBeenMade = 1
        self.movieHasPlayed = 0
        self.rewardHasPlayed = 0
        # Make sure all toons have an attack entry (even if it's a no-attack)
        for t in self.activeToons:
            if (not self.toonAttacks.has_key(t)):
                self.toonAttacks[t] = getToonAttack(t)
            attack = self.toonAttacks[t]
            
            # Replace any PASS or UN_ATTACK with a NO_ATTACK
            if (attack[TOON_TRACK_COL] == PASS or
                attack[TOON_TRACK_COL] == UN_ATTACK):
                self.toonAttacks[t] = getToonAttack(t)

            if self.toonAttacks[t][TOON_TRACK_COL] != NO_ATTACK:
                # so he didn't pass or un attack, he must have done something useful
                self.addHelpfulToon(t)

        self.battleCalc.calculateRound()
        
        # Tell the toons how much experience they will earn so far.
        # Also, from this point on until the end of the movie, the
        # toons will be allowed to accumulate more than their maxHp,
        # since we'll fix it up at the end of the movie.
        for t in self.activeToons:
            self.sendEarnedExperience(t)

            toon = self.getToon(t)
            if toon != None:
                toon.hpOwnedByBattle = 1
                if toon.immortalMode:
                    # A free toonup first, to guarantee the battle
                    # round won't kill this immortal toon.
                    toon.toonUp(toon.maxHp)
                
        self.d_setMovie()
        self.b_setState('PlayMovie')
        return Task.done

    def sendEarnedExperience(self, toonId):
        # Sends the experience earned so far to the toon, so he can
        # update his display to show which gags are clipped by the
        # experience cap.
        toon = self.getToon(toonId)
        if toon != None:
            expList = self.battleCalc.toonSkillPtsGained.get(toonId, None)
            if expList == None:
                toon.d_setEarnedExperience([])
            else:
                roundList = []
                for exp in expList:
                    roundList.append(int(exp + 0.5))
                toon.d_setEarnedExperience(roundList)


    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    def enterOff(self):
        return None

    def exitOff(self):
        return None

    ##### FaceOff state #####

    def enterFaceOff(self):
        return None

    def exitFaceOff(self):
        return None

    ##### WaitForJoin state #####

    def enterWaitForJoin(self):
        self.notify.debug('enterWaitForJoin()')
        if (len(self.activeSuits) > 0):
            self.b_setState('WaitForInput')
        else:
            self.notify.debug('enterWaitForJoin() - no active suits')
            self.runableFsm.request('Runable')
            self.resetResponses()
            self.__requestAdjust()
        return None

    def exitWaitForJoin(self):
        return None

    ##### WaitForInput state #####

    def enterWaitForInput(self):
        self.notify.debug('enterWaitForInput()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Runable')
        self.resetResponses()
        self.__requestAdjust()
        if not self.tutorialFlag:
            # No timers during tutorial.
            self.timer.startCallback(SERVER_INPUT_TIMEOUT,
                                     self.__serverTimedOut)
        self.npcAttacks = {}

        # handle autoRestock
        for toonId in self.toons:
            if bboard.get('autoRestock-%s' % toonId, False):
                toon = self.air.doId2do.get(toonId)
                if toon is not None:
                    toon.doRestock(0)
        
    def exitWaitForInput(self):
        self.npcAttacks = {}
        self.timer.stop()
        return None

    def __serverTimedOut(self):
        self.notify.debug('wait for input timed out on server')
        self.ignoreResponses = 1
        self.__requestMovie(timeout=1)

    ##### MakeMovie state #####

    def enterMakeMovie(self):
        self.notify.debug('enterMakeMovie()')
        self.runableFsm.request('Unrunable')
        self.resetResponses()
        return None

    def exitMakeMovie(self):
        return None

    ##### PlayMovie state #####

    def enterPlayMovie(self):
        self.notify.debug('enterPlayMovie()')
        self.joinableFsm.request('Joinable')
        self.runableFsm.request('Unrunable')
        self.resetResponses()
        # Estimate an upper bound for the length of the movie
        movieTime = (TOON_ATTACK_TIME * (len(self.activeToons) + \
                     self.numNPCAttacks) + \
                     SUIT_ATTACK_TIME * len(self.activeSuits) + \
                        SERVER_BUFFER_TIME)
        self.numNPCAttacks = 0
        self.notify.debug('estimated upper bound of movie time: %f' % movieTime)
        self.timer.startCallback(movieTime, self.__serverMovieDone)

        # print out the experience table
        #print 'tSPG: %s' % self.battleCalc.toonSkillPtsGained

    def __serverMovieDone(self):
        self.notify.debug('movie timed out on server')
        self.ignoreResponses = 1
        self.__movieDone()

    def serverRewardDone(self):
        self.notify.debug('reward timed out on server')
        self.ignoreResponses = 1
        self.handleRewardDone()

    def handleRewardDone(self):
        self.b_setState('Resume')

    def exitPlayMovie(self):
        self.timer.stop()
        return None

    def __movieDone(self):
        self.notify.debug('__movieDone() - movie is finished')
        if (self.movieHasPlayed == 1):
            self.notify.debug('__movieDone() - movie had already finished')
            return
        self.movieHasBeenMade = 0
        self.movieHasPlayed = 1
        self.ignoreResponses = 1
        needUpdate = 0

        # Calculate toon experience and remove any dead suits
        toonHpDict = {}
        for toon in self.activeToons:
            toonHpDict[toon] = [0, 0, 0]
            actualToon = self.getToon(toon) 
            assert(actualToon != None)
            self.notify.debug("BEFORE ROUND: toon: %d hp: %d" % (toon, actualToon.hp))
        deadSuits = []
        trapDict = {}
        suitsLuredOntoTraps = []
        npcTrapAttacks = []
        for activeToon in (self.activeToons + self.exitedToons):
            if (self.toonAttacks.has_key(activeToon)):
                attack = self.toonAttacks[activeToon]
                track = attack[TOON_TRACK_COL]
                npc_level = None
                if (track == NPCSOS):
                    track, npc_level, npc_hp = NPCToons.getNPCTrackLevelHp(attack[TOON_TGT_COL])
                    if (track == None):
                        track = NPCSOS
                    elif (track == TRAP):
                        npcTrapAttacks.append(attack)
                        toon = self.getToon(attack[TOON_ID_COL])
                        av = attack[TOON_TGT_COL]
                        if (toon != None and toon.NPCFriendsDict.has_key(av)):
                            toon.NPCFriendsDict[av] -= 1
                            if (toon.NPCFriendsDict[av] <= 0):
                                del toon.NPCFriendsDict[av]
                            toon.d_setNPCFriendsDict(toon.NPCFriendsDict)
                        continue
                if (track != NO_ATTACK):
                    toonId = attack[TOON_ID_COL]
                    assert(toonId == activeToon)
                    level = attack[TOON_LVL_COL]
                    if (npc_level != None):
                        level = npc_level
                    if (attack[TOON_TRACK_COL] == NPCSOS):
                        toon = self.getToon(toonId) 
                        av = attack[TOON_TGT_COL]
                        if (toon != None and toon.NPCFriendsDict.has_key(av)):
                            toon.NPCFriendsDict[av] -= 1
                            if (toon.NPCFriendsDict[av] <= 0):
                                del toon.NPCFriendsDict[av]
                            toon.d_setNPCFriendsDict(toon.NPCFriendsDict)
                    elif (track == PETSOS):
                        pass
                    elif (track == FIRE):
                        pass
                    elif (track != SOS):
                        toon = self.getToon(toonId)
                        if (toon != None):
                            check = toon.inventory.useItem(track, level)
                            if check == -1: #check for cheater
                                self.air.writeServerEvent('suspicious', toonId, 'Toon generating movie for non-existant gag track %s level %s' % (track, level))
                                self.notify.warning("generating movie for non-existant gag track %s level %s! avId: %s" % (track, level, toonId))
                            toon.d_setInventory(toon.inventory.makeNetString())
                    hps = attack[TOON_HP_COL]
                    if (track == SOS):
                        self.notify.debug('toon: %d called for help' % toonId)
                    elif (track == NPCSOS):
                        self.notify.debug('toon: %d called for help' % toonId)
                    elif (track == PETSOS):
                        self.notify.debug('toon: %d called for pet' % toonId)
                        for i in range(len(self.activeToons)):
                            toon = self.getToon(self.activeToons[i])
                            if (toon != None):
                                if (i < len(hps)):
                                    hp = hps[i]
                                    # If the PETSOS fails, the hp will be -1
                                    # so skip to avoid losing hp
                                    if hp > 0:
                                        toonHpDict[toon.doId][0] += hp 
                                    self.notify.debug("pet heal: toon: %d healed for hp: %d" % (toon.doId, hp))
                                else:
                                    self.notify.warning("Invalid targetIndex %s in hps %s." % (i, hps))
   
                    elif (track == NPC_RESTOCK_GAGS):
                        for at in self.activeToons:
                            toon = self.getToon(at)
                            if (toon != None):
                                toon.inventory.NPCMaxOutInv(npc_level)
                                toon.d_setInventory(toon.inventory.makeNetString()) 
                    elif (track == HEAL):
                        # Odd level heals affect all toons (except the caster)
                        # except in the case of an NPC heal, which gets all
                        # toons
                        if (levelAffectsGroup(HEAL, level)):
                            for i in range(len(self.activeToons)):
                                at = self.activeToons[i]
                                if (at != toonId or 
                                    attack[TOON_TRACK_COL] == NPCSOS):
                                    toon = self.getToon(at)
                                    if (toon != None):
                                        if i < len(hps):
                                            hp = hps[i]
                                        else:
                                            self.notify.warning("Invalid targetIndex %s in hps %s." % (i, hps))
                                            hp = 0
                                        toonHpDict[toon.doId][0] += hp
                                        self.notify.debug("HEAL: toon: %d healed for hp: %d" % (toon.doId, hp))
                        else:
                            targetId = attack[TOON_TGT_COL]
                            toon = self.getToon(targetId)
                            if ((toon != None) and
                                (targetId in self.activeToons)):
                                targetIndex = self.activeToons.index(targetId)
                                if targetIndex < len(hps):
                                    hp = hps[targetIndex]
                                else:
                                    self.notify.warning("Invalid targetIndex %s in hps %s." % (targetIndex, hps))
                                    hp = 0
                                toonHpDict[toon.doId][0] += hp
                    else:
                        # Odd level lures affect all suits
                        # Sounds affect all suits
                        # NPC drops affect all suits
                        #import pdb; pdb.set_trace()
                        if (attackAffectsGroup(track, level, attack[TOON_TRACK_COL])):
                            for suit in self.activeSuits:
                                targetIndex = self.activeSuits.index(suit)
                                if targetIndex < 0 or targetIndex >= len(hps):
                                    self.notify.warning("Got attack (%s, %s) on target suit %s, but hps has only %s entries: %s" % (track, level, targetIndex, len(hps), hps))
                                else:
                                    hp = hps[targetIndex]
                                    if (hp > 0 and track == LURE):
                                        if suit.battleTrap == UBER_GAG_LEVEL_INDEX:
                                            pass
                                            #trainTrapTriggered = True
                                            
                                        suit.battleTrap = NO_TRAP
                                        needUpdate = 1
                                        # Clear out any traps on this suit
                                        if (trapDict.has_key(suit.doId)):
                                            del trapDict[suit.doId]
                                        if (suitsLuredOntoTraps.count(suit) == 0):
                                            suitsLuredOntoTraps.append(suit)

                                    #WARNING, this section of code is duplicated below
                                    if (track == TRAP):
                                        targetId = suit.doId
                                        if (trapDict.has_key(targetId)):
                                            trapDict[targetId].append(attack)
                                        else:
                                            trapDict[targetId] = [attack]
                                        needUpdate = 1
                                            
                                    died = attack[SUIT_DIED_COL] & (1<<targetIndex)
                                    if (died != 0):
                                        if (deadSuits.count(suit) == 0):
                                            deadSuits.append(suit)
                        else:
                            targetId = attack[TOON_TGT_COL]
                            target = self.findSuit(targetId)
                            if (target != None):
                                targetIndex = self.activeSuits.index(target)
                                # Somehow this is failing sometimes,
                                # causing an AI crash.  As a band-aid,
                                # we'll test that the targetIndex is
                                # valid first.
                                if targetIndex < 0 or targetIndex >= len(hps):
                                    self.notify.warning("Got attack (%s, %s) on target suit %s, but hps has only %s entries: %s" % (track, level, targetIndex, len(hps), hps))
                                else:
                                    hp = hps[targetIndex]
                                    #WARNING this section of code is duplicated above
                                    if (track == TRAP):
                                        if (trapDict.has_key(targetId)):
                                            trapDict[targetId].append(attack)
                                        else:
                                            trapDict[targetId] = [attack]
                                    if (hp > 0 and track == LURE):
                                        oldBattleTrap = target.battleTrap
                                        if oldBattleTrap == UBER_GAG_LEVEL_INDEX:
                                            #trainTrapTriggered = True
                                            pass
                                        target.battleTrap = NO_TRAP
                                        needUpdate = 1
                                        # Clear out any traps on this suit
                                        if (trapDict.has_key(target.doId)):
                                            del trapDict[target.doId]
                                        if (suitsLuredOntoTraps.count(target) == 0):
                                            suitsLuredOntoTraps.append(target)
                                        #at this point we need to clear out the other suits in a traintrack trap
                                        if oldBattleTrap == UBER_GAG_LEVEL_INDEX:
                                            for otherSuit in self.activeSuits:
                                                if not otherSuit == target:
                                                    # Clear out any traps on this suit
                                                    otherSuit.battleTrap = NO_TRAP
                                                    if (trapDict.has_key(otherSuit.doId)):
                                                        del trapDict[otherSuit.doId]
                                                    
                                    died = attack[SUIT_DIED_COL] & (1<<targetIndex)
                                    if (died != 0):
                                        if (deadSuits.count(target) == 0):
                                            deadSuits.append(target)

        self.exitedToons = []

        # See if any traps collided with eachother
        # (trapDict only contains non-NPC traps)
        #import pdb; pdb.set_trace()
        for suitKey in trapDict.keys():
            attackList = trapDict[suitKey]
            # More than one trap on a list indicates a collision
            attack = attackList[0]
            target = self.findSuit(attack[TOON_TGT_COL])
            if attack[TOON_LVL_COL] == UBER_GAG_LEVEL_INDEX:
                targetId = suitKey
                target = self.findSuit(targetId)
            if (len(attackList) == 1):
                assert(target != None)
                if (suitsLuredOntoTraps.count(target) == 0):
                    self.notify.debug("movieDone() - trap set")
                    target.battleTrap = attack[TOON_LVL_COL]
                    needUpdate = 1
                else:
                    target.battleTrap = NO_TRAP
            else:
                assert(len(attackList) > 1)
                self.notify.debug("movieDone() - traps collided")
                if (target != None):
                    target.battleTrap = NO_TRAP

        if self.battleCalc.trainTrapTriggered:
            #necessary when train trap and dollar bill lure used in the same round
            self.notify.debug('Train trap triggered, clearing all traps')
            for otherSuit in self.activeSuits:
                self.notify.debug('suit =%d, oldBattleTrap=%d' %(otherSuit.doId, otherSuit.battleTrap))
                # Clear out any traps on this suit
                otherSuit.battleTrap = NO_TRAP
                #if (trapDict.has_key(otherSuit.doId)):
                #    del trapDict[otherSuit.doId]            

        # Update the lured suits list to match that of the battle calculator
        currLuredSuits = self.battleCalc.getLuredSuits()
        # See if the list has changed
        if (len(self.luredSuits) == len(currLuredSuits)):
            for suit in self.luredSuits:
                if (currLuredSuits.count(suit.doId) == 0):
                    needUpdate = 1
                    break        
        else:
            needUpdate = 1
        self.luredSuits = []
        for i in currLuredSuits:
            assert(self.air.doId2do.has_key(i))
            suit = self.air.doId2do[i]
            assert(suit in self.suits)
            self.luredSuits.append(suit)
            self.notify.debug('movieDone() - suit: %d is lured' % i)

        # Handle NPC traps
        for attack in npcTrapAttacks:
            assert(attack[TOON_TRACK_COL] == NPCSOS)
            track, level, hp = NPCToons.getNPCTrackLevelHp(attack[TOON_TGT_COL])    
            assert(track == TRAP)
            for suit in self.activeSuits:
                # NPC traps are laid on suits that are unlured and currently
                # have no traps in front of them (this includes recently
                # collided traps)
                if (self.luredSuits.count(suit) == 0 and
                    suit.battleTrap == NO_TRAP):
                    suit.battleTrap = level
            # Assume the existence of an NPC trap implies at least one
            # was placed successfully
            needUpdate = 1

        for suit in deadSuits:
            self.notify.debug('removing dead suit: %d' % suit.doId)
            if suit.isDeleted():
                self.notify.debug('whoops, suit %d is deleted.' % suit.doId)
            else:
                self.notify.debug('suit had revives? %d' % suit.getMaxSkeleRevives())
                encounter = {'type': suit.dna.name,
                             'level': suit.getActualLevel(),
                             'track': suit.dna.dept,
                             'isSkelecog': suit.getSkelecog(),
                             'isForeman': suit.isForeman(),
                             'isVP': 0,
                             'isCFO': 0,
                             'isSupervisor': suit.isSupervisor(),
                             'isVirtual': suit.isVirtual(),
                             'hasRevives': suit.getMaxSkeleRevives(),
                             # Put a copy of active toons in the dict
                             # Only they get credit for killing this suit
                             'activeToons': self.activeToons[:],
                             }
                self.suitsKilled.append(encounter)
                self.suitsKilledThisBattle.append(encounter)
                
            self.__removeSuit(suit)
            needUpdate = 1
            suit.resume()

        # Handle the case where the last active suit died but another is
        # joining
        lastActiveSuitDied = 0
        if (len(self.activeSuits) == 0 and len(self.pendingSuits) == 0):
            lastActiveSuitDied = 1

        # Calculate toon hit points and remove any dead toons
        for i in range(4):
            attack = self.suitAttacks[i][SUIT_ATK_COL]
            if (attack != NO_ATTACK):
                suitId = self.suitAttacks[i][SUIT_ID_COL]
                assert(suitId != -1)
                suit = self.findSuit(suitId)
                if (suit == None):
                    self.notify.warning('movieDone() - suit: %d is gone!' % \
                        suitId)
                    continue
                if not (hasattr(suit, "dna") and suit.dna):
                    #RAU couldn't reproduce this crash, log it in case it comes up again
                    toonId = self.air.getAvatarIdFromSender()
                    self.notify.warning("_movieDone avoiding crash, sender=%s but suit has no dna" % toonId)
                    self.air.writeServerEvent('suspicious', toonId, '_movieDone avoiding crash, suit has no dna')
                    continue
                                        
                adict = getSuitAttack(suit.getStyleName(), suit.getLevel(),
                                attack)
                hps = self.suitAttacks[i][SUIT_HP_COL]
                if (adict['group'] == ATK_TGT_GROUP):
                    for activeToon in self.activeToons:
                        toon = self.getToon(activeToon)
                        if (toon != None):
                            targetIndex = self.activeToons.index(activeToon)
                            toonDied = self.suitAttacks[i][TOON_DIED_COL] & \
                                        (1<<targetIndex)
                            if targetIndex >= len(hps):
                                self.notify.warning('DAMAGE: toon %s is no longer in battle!' % (activeToon))
                            else:
                                hp = hps[targetIndex]
                                if (hp > 0):
                                    self.notify.debug('DAMAGE: toon: %d hit for dmg: %d' % (activeToon, hp))
                                    if (toonDied != 0):
                                        toonHpDict[toon.doId][2] = 1
                                    toonHpDict[toon.doId][1] += hp

                elif (adict['group'] == ATK_TGT_SINGLE):
                    targetIndex = self.suitAttacks[i][SUIT_TGT_COL]
                    if (targetIndex >= len(self.activeToons)):
                        self.notify.warning('movieDone() - toon: %d gone!' \
                                % targetIndex)
                        break
                    toonId = self.activeToons[targetIndex]
                    toon = self.getToon(toonId)
                    toonDied = self.suitAttacks[i][TOON_DIED_COL] & \
                                        (1<<targetIndex)
                    if targetIndex >= len(hps):
                        self.notify.warning('DAMAGE: toon %s is no longer in battle!' % (toonId))
                    else:
                        hp = hps[targetIndex]
                        if (hp > 0):
                            self.notify.debug('DAMAGE: toon: %d hit for dmg: %d' % (toonId, hp))
                            if (toonDied != 0):
                                toonHpDict[toon.doId][2] = 1
                            toonHpDict[toon.doId][1] += hp

        # Now we go through and ensure client and AI are on the same
        # page with HP values.
        deadToons = []
        for activeToon in self.activeToons:
            assert(toonHpDict.has_key(activeToon))
            hp = toonHpDict[activeToon]
            toon = self.getToon(activeToon)
            if (toon != None):
                self.notify.debug("AFTER ROUND: currtoonHP: %d toonMAX: %d hheal: %d damage: %d" % (toon.hp, toon.maxHp, hp[0], hp[1]))

                toon.hpOwnedByBattle = 0

                # hpDelta is the amount of heals applied during
                # the round, less the amount of damage taken.
                hpDelta = hp[0] - hp[1]
                if hpDelta >= 0:
                    toon.toonUp(hpDelta, quietly = 1)
                else:
                    toon.takeDamage(-hpDelta, quietly = 1)
                    
                if toon.hp <= 0:
                    # If the toon is now dead, get him out of
                    # the battle.
                    self.notify.debug('movieDone() - toon: %d was killed' % \
                                      activeToon)
                    # __removeToon() will broadcast the dead toon's inv
                    toon.inventory.zeroInv(1)
                    deadToons.append(activeToon)

                self.notify.debug('AFTER ROUND: toon: %d setHp: %d' % \
                                  (toon.doId, toon.hp))
        for deadToon in deadToons:
            self.__removeToon(deadToon)
            needUpdate = 1

        self.clearAttacks()

        # Send an inactive movie message
        self.d_setMovie()
        self.d_setChosenToonAttacks()

        # Defined differently in DistributedBattleAI and
        # DistributedBattleBldgAI
        self.localMovieDone(needUpdate, deadToons, deadSuits,
                                        lastActiveSuitDied)


    ##### Reward state #####

    ##### Resume state #####

    def enterResume(self):
        assert(self.notify.debug('enterResume()'))
        for suit in self.suits:
            self.notify.info('battle done, resuming suit: %d' % suit.doId)
            if suit.isDeleted():
                self.notify.info('whoops, suit %d is deleted.' % suit.doId)
            else:
                suit.resume()

        self.suits = []
        self.joiningSuits = []
        self.pendingSuits = []
        self.adjustingSuits = []
        self.activeSuits = []
        self.luredSuits = []

        # Actually, removing the toons from the battle seems to send
        # them to the playground.  So don't do that.

        #self.toons = []
        #self.joiningToons = []
        #self.pendingToons = []
        #self.activeToons = []
        #self.runningToons = []
        #self.d_setMembers()
        
        for toonId in self.toons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setBattleId(0)
                messageToonReleased = ("Battle releasing toon %s" % (toon.doId))
                messenger.send(messageToonReleased, [toon.doId])

        # Stop responding to avatar exit events
        for exitEvent in self.avatarExitEvents:
            self.ignore(exitEvent)
        
        # Log the suits killed for this battle only, just for
        # marketing purposes.
        eventMsg = {}
        for encounter in self.suitsKilledThisBattle:
            cog = encounter['type']
            level = encounter['level']

            msgName = '%s%s' % (cog, level)

            if encounter['isSkelecog']:
                msgName += "+"
                
            if eventMsg.has_key(msgName):
                eventMsg[msgName] += 1
            else:
                eventMsg[msgName] = 1

        # Now format the message for the AI.
        msgText = ''
        for msgName, count in eventMsg.items():
            if msgText != '':
                msgText += ','
            msgText += '%s%s' % (count, msgName)
        
        self.air.writeServerEvent(
            'battleCogsDefeated', self.doId, "%s|%s" % (msgText,
                                                        self.getTaskZoneId()))


    def exitResume(self):
        pass

    ########################
    ##### Joinable ClassicFSM #####
    ########################

    def isJoinable(self):
        """ isJoinable()
        """
        return (self.joinableFsm.getCurrentState().getName() == 'Joinable')

    ##### Joinable state #####

    # Suits or Toons are allowed to join the battle

    def enterJoinable(self):
        self.notify.debug('enterJoinable()')
        return None

    def exitJoinable(self):
        return None

    ##### Unjoinable state #####

    # Suits or Toons are not allowed to join the battle

    def enterUnjoinable(self):
        self.notify.debug('enterUnjoinable()')
        return None

    def exitUnjoinable(self):
        return None

    ########################
    ##### Runable ClassicFSM #####
    ########################

    def isRunable(self):
        """ isRunable()
        """
        return (self.runableFsm.getCurrentState().getName() == 'Runable')

    ##### Runable state #####

    # Suits or Toons are allowed to run from the battle

    def enterRunable(self):
        self.notify.debug('enterRunable()')
        return None

    def exitRunable(self):
        return None

    ##### Unrunable state #####

    # Suits or Toons are not allowed to run from the battle

    def enterUnrunable(self):
        self.notify.debug('enterUnrunable()')
        return None

    def exitUnrunable(self):
        return None

    ######################
    ##### Adjust ClassicFSM #####
    ######################

    ##### Adjusting state #####

    def __estimateAdjustTime(self):
        """ Clear out the pending lists and estimate an upper bound
            for the time required to adjust
        """
        self.needAdjust = 0
        adjustTime = 0

        if ((len(self.pendingSuits) > 0) or self.suitGone == 1):
            self.suitGone = 0
            pos0 = self.suitPendingPoints[0][0]
            pos1 = self.suitPoints[0][0][0]
            adjustTime = self.calcSuitMoveTime(pos0, pos1)

        if ((len(self.pendingToons) > 0) or self.toonGone == 1):
            self.toonGone = 0
            if (adjustTime == 0):
                pos0 = self.toonPendingPoints[0][0]
                pos1 = self.toonPoints[0][0][0]
                adjustTime = self.calcToonMoveTime(pos0, pos1)

        return adjustTime

    def enterAdjusting(self):
        self.notify.debug('enterAdjusting()')
        self.timer.stop()
        self.__resetAdjustingResponses()
        self.adjustingTimer.startCallback(self.__estimateAdjustTime() +
                        SERVER_BUFFER_TIME, self.__serverAdjustingDone)
        return None

    def __serverAdjustingDone(self):
        if (self.needAdjust == 1):
            self.adjustFsm.request('NotAdjusting')
            self.__requestAdjust()
        else:
            self.notify.debug('adjusting timed out on the server')
            self.ignoreAdjustingResponses = 1
            self.__adjustDone()

    def exitAdjusting(self):
        currStateName = self.fsm.getCurrentState().getName()
        if (currStateName == 'WaitForInput'):
            self.timer.restart()
        elif (currStateName == 'WaitForJoin'):
            self.b_setState('WaitForInput')
        self.adjustingTimer.stop()
        return None

    def __addTrainTrapForNewSuits(self):
        #we need to make sure battleTrap is set for any new suits that join, in case we have a train track trap
        hasTrainTrap = False
        trapInfo = None
        for otherSuit in self.activeSuits:
            if otherSuit.battleTrap == UBER_GAG_LEVEL_INDEX:
                hasTrainTrap = True
        if hasTrainTrap:
            for curSuit in self.activeSuits:
                if not curSuit.battleTrap == UBER_GAG_LEVEL_INDEX:
                    oldBattleTrap = curSuit.battleTrap
                    curSuit.battleTrap = UBER_GAG_LEVEL_INDEX
                    self.battleCalc.addTrainTrapForJoiningSuit(curSuit.doId)
                    self.notify.debug('setting traintrack trap for joining suit %d oldTrap=%s' % (curSuit.doId, oldBattleTrap))        

    def __adjustDone(self):
        for s in self.adjustingSuits:
            assert(self.pendingSuits.count(s) == 1)
            self.pendingSuits.remove(s)
            assert(self.activeSuits.count(s) == 0)
            self.activeSuits.append(s)
        self.adjustingSuits = []
        for toon in self.adjustingToons:
            if (self.pendingToons.count(toon) == 1):
                self.pendingToons.remove(toon)
            else:
                self.notify.warning('adjustDone() - toon: %d not pending!' % \
                        toon.doId)
            if (self.activeToons.count(toon) == 0):
                self.activeToons.append(toon)
                # In case ignoreResponses was set to 1 during adjusting,
                # we need to clear it because a new toon is now active
                self.ignoreResponses = 0
                # Welcome, toon!  Here's your experience earned so far.
                self.sendEarnedExperience(toon)
            else:
                self.notify.warning('adjustDone() - toon: %d already active!' \
                        % toon.doId)
        self.adjustingToons = []

        self.__addTrainTrapForNewSuits()
                
        
        self.d_setMembers()
        self.adjustFsm.request('NotAdjusting')
        if (self.needAdjust == 1):
            self.notify.debug('__adjustDone() - need to adjust again')
            self.__requestAdjust()

    ##### NotAdjusting state #####

    def enterNotAdjusting(self):
        self.notify.debug('enterNotAdjusting()')
        if (self.movieRequested == 1):
            # Make sure last toon didn't just run and adjusting may have
            # resulted in a new active toon who needs to choose an attack
            if (len(self.activeToons) > 0 and
                self.__allActiveToonsResponded()):
                self.__requestMovie()
        return None

    def exitNotAdjusting(self):
        return None

    def getPetProxyObject(self, petId, callback):
        """get an instance of a pet
        callback must accept (success, pet)
        pet is undefined if !success

        On success, pet MUST be instantiated with
        DistributedObjectAI.generateWithRequiredAndId, using the
        correct pet doId.
        """
        doneEvent = 'readPet-%s' % self._getNextSerialNum()
        dbo = DatabaseObject.DatabaseObject(
            self.air, petId, doneEvent=doneEvent)
        pet = dbo.readPetProxy()

        def handlePetProxyRead(dbo, retCode, callback=callback, pet=pet):
            success = (retCode == 0)
            if not success:
                self.notify.warning('pet DB read failed')
                pet = None
            callback(success, pet)
        self.acceptOnce(doneEvent, handlePetProxyRead)

    def _getNextSerialNum(self):
        num = self.serialNum
        self.serialNum += 1
        return num
