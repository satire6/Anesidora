from direct.directnotify import DirectNotifyGlobal
from otp.avatar import DistributedAvatarAI
from toontown.battle import BattleExperienceAI
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toon import InventoryBase
from toontown.battle import DistributedBattleFinalAI
from toontown.building import SuitPlannerInteriorAI
from toontown.battle import BattleBase
from pandac.PandaModules import *
import SuitDNA
import random

AllBossCogs = []

class DistributedBossCogAI(DistributedAvatarAI.DistributedAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCogAI')

    def __init__(self, air, dept):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)

        self.dept = dept
        self.dna = SuitDNA.SuitDNA()
        self.dna.newBossCog(self.dept)
        self.deptIndex = SuitDNA.suitDepts.index(self.dept)

        self.resetBattleCounters()

        # These are the toons who will be participating in our
        # battles.
        self.looseToons = []
        self.involvedToons = []
        self.toonsA = []
        self.toonsB = []
        self.nearToons = []

        # These are the suits.
        self.suitsA = []
        self.activeSuitsA = []
        self.suitsB = []
        self.activeSuitsB = []
        self.reserveSuits = []

        self.barrier = None

        # This is the list of state transitions that will be logged in
        # the event manager.
        self.keyStates = [
            'BattleOne',
            'BattleTwo',
            'BattleThree',
            'Victory',
            ]

        # Accumulated hits on the boss during the climactic final
        # battle (battle three)
        self.bossDamage = 0
        self.battleThreeStart = 0
        self.battleThreeDuration = 1800 # Expected battle 3 time in seconds

        # What attack code the boss has currently selected.
        self.attackCode = None
        self.attackAvId = 0
            
        # The number of times we are hit during one dizzy spell.
        self.hitCount = 0

        AllBossCogs.append(self)

    def delete(self):
        self.ignoreAll()
        if self in AllBossCogs:
            i = AllBossCogs.index(self)
            del AllBossCogs[i]
            
        return DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def getDNAString(self):
        return self.dna.makeNetString()


        
    # avatarEnter/avatarExit is used for the ~bossBattle magic word to
    # stage toons in the area.  It probably won't be needed once we
    # integrate everything fully.
    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.avatarEnter(%s)' % (self.doId, avId))

        self.addToon(avId)

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.avatarExit(%s)' % (self.doId, avId))
        self.removeToon(avId)

    # avatarNearEnter/avatarNearExit tell us when a client comes
    # within directed attack range.
    def avatarNearEnter(self):
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.avatarNearEnter(%s)' % (self.doId, avId))

        if avId not in self.nearToons:
            self.nearToons.append(avId)

    def avatarNearExit(self):
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.avatarNearExit(%s)' % (self.doId, avId))

        try:
            self.nearToons.remove(avId)
        except:
            pass

    def __handleUnexpectedExit(self, avId):
        assert self.notify.debug('%s.handleUnexpectedExit(%s)' % (self.doId, avId))
        self.removeToon(avId)

    def addToon(self, avId):
        assert self.notify.debug('%s.addToon(%s)' % (self.doId, avId))        
        if avId not in self.looseToons and avId not in self.involvedToons:
            self.looseToons.append(avId)

            event = self.air.getAvatarExitEvent(avId)
            self.acceptOnce(event, self.__handleUnexpectedExit, extraArgs=[avId])

    def removeToon(self, avId):
        assert self.notify.debug('%s.removeToon(%s)' % (self.doId, avId))        
        resendIds = 0
        try:
            self.looseToons.remove(avId)
        except:
            pass
        try:
            self.involvedToons.remove(avId)
            resendIds = 1
        except:
            pass
        try:
            self.toonsA.remove(avId)
        except:
            pass
        try:
            self.toonsB.remove(avId)
        except:
            pass
        try:
            self.nearToons.remove(avId)
        except:
            pass

        event = self.air.getAvatarExitEvent(avId)
        self.ignore(event)

        assert self.notify.debug('%s. looseToons = %s, involvedToons = %s, toonsA = %s, toonsB = %s' % (self.doId, self.looseToons, self.involvedToons, self.toonsA, self.toonsB))

        if not self.hasToons():
            # There are no more toons, so we should send the cleanup
            # message.  But wait a few seconds first so the last Toon
            # won't see the universe vanish before he finishes his
            # teleport-out animation.
            
            taskMgr.doMethodLater(10, self.__bossDone,
                                  self.uniqueName('BossDone'))

    def __bossDone(self, task):
        self.b_setState('Off')
        messenger.send(self.uniqueName('BossDone'))
        self.ignoreAll()

    def hasToons(self):
        return self.looseToons or self.involvedToons

    def hasToonsAlive(self):
        # see if any toons still alive
        alive = 0
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                hp = toon.getHp()
                if hp > 0:
                    alive = 1
        return alive

    def sendBattleIds(self):
        self.sendUpdate('setBattleIds', [self.battleNumber, self.battleAId, self.battleBId])

    def sendToonIds(self):
        # We need to send the involvedToons list, in addition to the
        # individual toonsA and toonsB lists, just so we don't lose
        # the order of involvedToons (which controls how they are
        # lined up in the elevator).
        self.sendUpdate('setToonIds', [self.involvedToons, self.toonsA, self.toonsB])

    def damageToon(self, toon, deduction):
        toon.takeDamage(deduction)
        assert self.notify.debug('%s. toon %s hit for %s to %s/%s' % (self.doId, toon.doId, deduction, toon.getHp(), toon.getMaxHp()))
        if toon.getHp() <= 0:
            assert self.notify.debug('%s. toon died: %s' % (self.doId, toon.doId))
            self.sendUpdate('toonDied', [toon.doId])

            # Clear out the Toon's inventory.
            empty = InventoryBase.InventoryBase(toon)
            toon.b_setInventory(empty.makeNetString())

            # We'll go ahead and remove the toon now, rather than
            # waiting for him to tell us when he's gone.  That will
            # ensure he's not involved in any more activity even if
            # he's got a slow client (or a rogue client) that doesn't
            # tell us he's gone right away.
            self.removeToon(toon.doId)

    def healToon(self, toon, increment):
        toon.toonUp(increment)
        assert self.notify.debug('%s. toon %s healed to %s/%s' % (self.doId, toon.doId, toon.getHp(), toon.getMaxHp()))

    # setBattleExperience

    def d_setBattleExperience(self):
        assert self.notify.debug('%s.d_setBattleExperience()' % (self.doId))
        self.sendUpdate('setBattleExperience', self.getBattleExperience())

    def getBattleExperience(self):
        result =  BattleExperienceAI.getBattleExperience(
            8, self.involvedToons, self.toonExp,
            self.toonSkillPtsGained, self.toonOrigQuests, self.toonItems,
            self.toonOrigMerits, self.toonMerits,
            self.toonParts, self.suitsKilled, self.helpfulToons)
        return result
    

    def b_setArenaSide(self, arenaSide):
        self.setArenaSide(arenaSide)
        self.d_setArenaSide(arenaSide)

    def setArenaSide(self, arenaSide):
        self.arenaSide = arenaSide

    def d_setArenaSide(self, arenaSide):
        self.sendUpdate('setArenaSide', [arenaSide])

    # setState()

    def b_setState(self, state):
        # It is important to set the local state first, so that
        # objects created here will be available when the client sets
        # its state.
        self.setState(state)
        self.d_setState(state)

    def d_setState(self, state):
        self.sendUpdate('setState', [state])
        
    def setState(self, state):
        self.demand(state)

        if self.air:
            if state in self.keyStates:
                self.air.writeServerEvent("bossBattle", self.doId, "%s|%s|%s|%s" %
                                          (self.dept, state, self.involvedToons,
                                           self.formatReward()))
                

    def getState(self):
        return self.state


    def formatReward(self):
        # Returns the reward indication to write to the event log.
        return 'unspecified'


    ##### Off state #####

    def enterOff(self):
        assert self.notify.debug('enterOff()')
        self.resetBattles()
        self.resetToons()
        self.resetBattleCounters()

    def exitOff(self):
        pass

    ##### WaitForToons state #####

    def enterWaitForToons(self):
        assert self.notify.debug('%s.enterWaitForToons()' % (self.doId))

        # The clients are waiting for all the toons to transition to
        # the same zoneId.  They'll report back when that happens.  If
        # they don't report back, move on anyway.

        self.acceptNewToons()

        self.barrier = self.beginBarrier(
            "WaitForToons", self.involvedToons, 5,
            self.__doneWaitForToons)

    def __doneWaitForToons(self, toons):
        assert self.notify.debug('%s.__doneWaitForToons()' % (self.doId))
        self.b_setState("Elevator")

    def exitWaitForToons(self):
        self.ignoreBarrier(self.barrier)

    ##### Elevator state #####

    def enterElevator(self):
        assert self.notify.debug('%s.enterElevator()' % (self.doId))

        if self.notify.getDebug():
            for toonId in self.involvedToons:
                toon = simbase.air.doId2do.get(toonId)
                if toon:
                    self.notify.debug('%s. involved toon %s, %s/%s' % (self.doId, toonId, toon.getHp(), toon.getMaxHp()))
            

        self.resetBattles()

        # The clients play a movie showing the elevator ride and the
        # doors opening at the top.
        self.barrier = self.beginBarrier(
            "Elevator", self.involvedToons, 30,
            self.__doneElevator)

    def __doneElevator(self, avIds):
        assert self.notify.debug('%s.__doneElevator()' % (self.doId))
        self.b_setState("Introduction")
        
    def exitElevator(self):
        self.ignoreBarrier(self.barrier)

    ##### Introduction state #####

    def enterIntroduction(self):
        assert self.notify.debug('%s.enterIntroduction()' % (self.doId))

        self.resetBattles()

        # Also get the battle objects ready.
        self.arenaSide = None
        self.makeBattleOneBattles()

        # The clients will play a cutscene.  When they are done
        # watching the movie, we continue.

        self.barrier = self.beginBarrier(
            "Introduction", self.involvedToons, 45,
            self.doneIntroduction)

    def doneIntroduction(self, avIds):
        self.b_setState("BattleOne")
        
    def exitIntroduction(self):
        self.ignoreBarrier(self.barrier)

        # we no longer take away cog parts for fighting the VP.
        # Hopefully this will reduce the elevator griefing, since it's
        # not the end of the world to lose a VP battle.

        # Make sure the toons all have their distributed cog suit
        # turned off (since they have turned off their local suit by
        # now)
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setCogIndex(-1)
                #toon.loseCogParts(self.deptIndex)

    ##### BattleOne state #####

    def enterBattleOne(self):
        assert self.notify.debug('%s.enterBattleOne()' % (self.doId))

        # The boss cog unleashes the first round of Cogs from his
        # belly to engage the toons in battle.

        # Begin the battles.
        if self.battleA:
            self.battleA.startBattle(self.toonsA, self.suitsA)
        if self.battleB:
            self.battleB.startBattle(self.toonsB, self.suitsB)

    def exitBattleOne(self):
        self.resetBattles()


    ##### Reward state #####

    def enterReward(self):
        assert self.notify.debug('%s.enterReward()' % (self.doId))
        self.resetBattles()

        self.barrier = self.beginBarrier(
            "Reward", self.involvedToons, BattleBase.BUILDING_REWARD_TIMEOUT,
            self.__doneReward)

    def __doneReward(self, avIds):
        self.b_setState("Epilogue")

    def exitReward(self):
        pass


    ##### Epilogue state #####

    def enterEpilogue(self):
        assert self.notify.debug('%s.enterEpilogue()' % (self.doId))

    def exitEpilogue(self):
        pass


    ##### Frolic state #####

    def enterFrolic(self):
        assert self.notify.debug('%s.enterFrolic()' % (self.doId))
        self.resetBattles()

    def exitFrolic(self):
        pass


    def resetBattleCounters(self):
        # Resets all the statistics about who's won what battles.
        # This should normally only be done at startup.
        
        self.battleNumber = 0
        self.battleA = None
        self.battleAId = 0
        self.battleB = None
        self.battleBId = 0
        self.arenaSide = None
        self.toonSkillPtsGained = {}
        self.toonExp = {}
        self.toonOrigQuests = {}
        self.toonItems = {}
        self.toonOrigMerits = {}
        self.toonMerits = {}
        self.toonParts = {}
        self.suitsKilled = []
        self.helpfulToons = []

    def resetBattles(self):
        # Interrupts any currently-running battles and associated
        # suits.
        sendReset = 0
        if self.battleA:
            self.battleA.requestDelete()
            self.battleA = None
            self.battleAId = 0
            sendReset = 1
        if self.battleB:
            self.battleB.requestDelete()
            self.battleB = None
            self.battleBId = 0
            sendReset = 1
        for suit in self.suitsA + self.suitsB:
            suit.requestDelete()
        for suit, joinChance in self.reserveSuits:
            suit.requestDelete()
        self.suitsA = []
        self.activeSuitsA = []
        self.suitsB = []
        self.activeSuitsB = []
        self.reserveSuits = []
        self.battleNumber = 0

        if sendReset:
            self.sendBattleIds()

    def resetToons(self):
        # Remove all the toons from the A/B division and make them all
        # loose toons again.  This probably won't be used once we're
        # done with the magic word interface.
        if self.toonsA or self.toonsB:
            self.looseToons = self.looseToons + self.involvedToons
            self.involvedToons = []
            self.toonsA = []
            self.toonsB = []
            self.sendToonIds()

    def divideToons(self):
        # Divide the toons randomly into toonsA and toonsB for facing
        # off with the boss cog.

        toons = self.involvedToons[:]
        random.shuffle(toons)

        numToons = min(len(toons), 8)

        # The odd toon ends up randomly on one side or the other,
        # unless there are fewer than four toons (in which case the
        # odd toon always ends up on side A, to give the boss someone
        # to address in the movies).
        if (numToons < 4):
            numToonsB = numToons / 2
        else:
            numToonsB = (numToons + random.choice([0, 1])) / 2
        
        self.toonsA = toons[numToonsB:numToons]
        self.toonsB = toons[:numToonsB]
        self.looseToons += toons[numToons:]
        self.sendToonIds()

    def acceptNewToons(self):
        # Only the non-ghosts get accepted into the battle.
        sourceToons = self.looseToons
        self.looseToons = []
        for toonId in sourceToons:
            toon = self.air.doId2do.get(toonId)
            if toon and not toon.ghostMode:
                self.involvedToons.append(toonId)
            else:
                self.looseToons.append(toonId)
                
        # Fill in the Toon's original experience and merits.  This
        # probably isn't strictly necessary, since it will happen
        # anyway when battle 1 and 2 start, but duplicating this code
        # here allows us to skip directly to battle 3 with a magic
        # word.
        for avId in self.involvedToons:
            toon = self.air.doId2do.get(avId)
            if toon:
                p = []
                for t in ToontownBattleGlobals.Tracks:
                    p.append(toon.experience.getExp(t))
                self.toonExp[avId] = p
                self.toonOrigMerits[avId] = toon.cogMerits[:]

        # Shuffle the toons and divide them into two groups for the
        # two different battles.
        self.divideToons()


    def initializeBattles(self, battleNumber, bossCogPosHpr):
        # Set up the pair of battle objects for the BattleOne or
        # BattleTwo phase.
        self.resetBattles()
        
        if not self.involvedToons:
            self.notify.warning("initializeBattles: no toons!")
            return

        self.battleNumber = battleNumber
        suitHandles = self.generateSuits(battleNumber)
        self.suitsA = suitHandles['activeSuits']
        self.activeSuitsA = self.suitsA[:]
        self.reserveSuits = suitHandles['reserveSuits']

        suitHandles = self.generateSuits(battleNumber)
        self.suitsB = suitHandles['activeSuits']
        self.activeSuitsB = self.suitsB[:]
        self.reserveSuits += suitHandles['reserveSuits']

        if self.toonsA:
            self.battleA = self.makeBattle(
                bossCogPosHpr, ToontownGlobals.BossCogBattleAPosHpr,
                self.handleRoundADone, self.handleBattleADone,
                battleNumber, 0)
            self.battleAId = self.battleA.doId
        else:
            # If we don't have a battleA, all of the suits that would
            # have been in that battle go over to fight in battleB
            # instead.
            self.moveSuits(self.activeSuitsA)
            self.suitsA = []
            self.activeSuitsA = []

            if self.arenaSide == None:
                self.b_setArenaSide(0)

        if self.toonsB:
            self.battleB = self.makeBattle(
                bossCogPosHpr, ToontownGlobals.BossCogBattleBPosHpr,
                self.handleRoundBDone, self.handleBattleBDone,
                battleNumber, 1)
            self.battleBId = self.battleB.doId
        else:
            # If we don't have a battleB, all of the suits that would
            # have been in that battle go over to fight in battleA
            # instead.
            self.moveSuits(self.activeSuitsB)
            self.suitsB = []
            self.activeSuitsB = []

            if self.arenaSide == None:
                self.b_setArenaSide(1)

        self.sendBattleIds()

    def makeBattle(self, bossCogPosHpr, battlePosHpr,
                   roundCallback, finishCallback, battleNumber, battleSide):
        battle = DistributedBattleFinalAI.DistributedBattleFinalAI(
            self.air, self, roundCallback, finishCallback, battleSide)
        self.setBattlePos(battle, bossCogPosHpr, battlePosHpr)

        # Just like the DistributedSuitInteriorAI class, we save a
        # reference to our suitsKilled and toonSkillPtsGained
        # structures in each battle we create.  That way, the battle
        # will directly adjust these structures and we accumulate the
        # toon credits for all battles.
        battle.suitsKilled = self.suitsKilled
        battle.battleCalc.toonSkillPtsGained = self.toonSkillPtsGained
        battle.toonExp = self.toonExp
        battle.toonOrigQuests = self.toonOrigQuests
        battle.toonItems = self.toonItems
        battle.toonOrigMerits = self.toonOrigMerits
        battle.toonMerits = self.toonMerits
        battle.toonParts = self.toonParts
        battle.helpfulToons = self.helpfulToons

        # We get a bonus factor applied toward each attack's
        # experience credit.
        mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(battleNumber)

        # We don't, however, get any particular bonus for an invasion
        # here.
        battle.battleCalc.setSkillCreditMultiplier(mult)

        battle.generateWithRequired(self.zoneId)
        return battle

    def setBattlePos(self, battle, cogPosHpr, battlePosHpr):
        # We need to set up the global position and rotation of the
        # battle objects.  To do this most easily, we create a handful
        # of temporary nodes to do the matrix math for us.  Don't
        # panic, there's no harm in creating an unattached NodePath on
        # the AI!
        
        bossNode = NodePath('bossNode')
        bossNode.setPosHpr(*cogPosHpr)
        battleNode = bossNode.attachNewNode('battleNode')
        battleNode.setPosHpr(*battlePosHpr)

        # The battle rotation is described with an initialSuitPos,
        # which is the direction in which the battle will look,
        # i.e. forward.
        suitNode = battleNode.attachNewNode('suitNode')
        suitNode.setPos(0, 1, 0)

        battle.pos = battleNode.getPos(NodePath())
        battle.initialSuitPos = suitNode.getPos(NodePath())

    def moveSuits(self, active):
        # Move the active suits to the reserve pool so they can emerge
        # on the other side.
        for suit in active:
            self.reserveSuits.append((suit, 0))
        
    def handleRoundADone(self, toonIds, totalHp, deadSuits):
        if self.battleA:
            assert self.notify.debug("%s. battle A round done, toonIds = %s, totalHp = %s, deadSuits = %s, suits = %s" % (self.doId, toonIds, totalHp, deadSuits, self.battleA.suits,))
            self.handleRoundDone(
                self.battleA, self.suitsA, self.activeSuitsA,
                toonIds, totalHp, deadSuits)
        
    def handleRoundBDone(self, toonIds, totalHp, deadSuits):
        if self.battleB:
            assert self.notify.debug("%s. battle B round done, toonIds = %s, totalHp = %s, deadSuits = %s, suits = %s" % (self.doId, toonIds, totalHp, deadSuits, self.battleB.suits,))
            self.handleRoundDone(
                self.battleB, self.suitsB, self.activeSuitsB,
                toonIds, totalHp, deadSuits)

    def handleBattleADone(self, zoneId, toonIds):
        if self.battleA:
            assert self.notify.debug("%s. battle A done, zoneId = %s, toonIds = %s" % (self.doId, zoneId, toonIds))
            self.battleA.requestDelete()
            self.battleA = None
            self.battleAId = 0
            self.sendBattleIds()

        # Battle A was the first finished; the boss cog will roll up
        # on this side to battle two.
        if self.arenaSide == None:
            self.b_setArenaSide(0)

        if not self.battleB and self.hasToons() and self.hasToonsAlive():
            # Both battles are done; move on.
            self.b_setState(self.postBattleState)


    def handleBattleBDone(self, zoneId, toonIds):
        if self.battleB:
            assert self.notify.debug("%s. battle B done, zoneId = %s, toonIds = %s" % (self.doId, zoneId, toonIds))
            self.battleB.requestDelete()
            self.battleB = None
            self.battleBId = 0
            self.sendBattleIds()

        # Battle B was the first finished; the boss cog will roll up
        # on this side to battle two.
        if self.arenaSide == None:
            self.b_setArenaSide(1)

        if not self.battleA and self.hasToons() and self.hasToonsAlive():
            # Both battles are done; move on.
            self.b_setState(self.postBattleState)

    def invokeSuitPlanner(self, buildingCode, skelecog):
        # Creates a suit planner to generate suits to emerge from the
        # boss cog's belly.  The buildingCode is the level number to
        # use from the table in SuitBuildingGlobals.py; skelecog is
        # true to generate skeleton cogs.  The return value is the
        # dictionary { 'activeSuits' : suits, 'reserveSuits' : suits }

        planner = SuitPlannerInteriorAI.SuitPlannerInteriorAI(
            1, buildingCode, self.dna.dept, self.zoneId)
        
        planner.respectInvasions = 0
        suits = planner.genFloorSuits(0)
        
        if skelecog:
            # These cogs have already been generated, so we must do a
            # distributed setSkelecog
            for suit in suits['activeSuits']:
                suit.b_setSkelecog(1)
            for reserve in suits['reserveSuits']:
                suit = reserve[0]
                suit.b_setSkelecog(1)

        return suits

    def generateSuits(self, battleNumber):
        # A derived class should override this to generate the
        # appropriate number and varient of suits for the indicated
        # battle.
        
        raise StandardError, 'generateSuits unimplemented'
        
    def handleRoundDone(self, battle, suits, activeSuits,
                          toonIds, totalHp, deadSuits):
        # Determine if any reserves need to join
        assert self.notify.debug('%s.handleRoundDone() - hp: %d' % (self.doId, totalHp))
        # Calculate the total max HP for all the suits currently on the floor
        totalMaxHp = 0
        for suit in suits:
            totalMaxHp += suit.maxHP

        for suit in deadSuits:
            activeSuits.remove(suit)

        joinedReserves = []
        
        # Determine if any reserve suits need to join
        if (len(self.reserveSuits) > 0 and len(activeSuits) < 4):
            assert(self.notify.debug('%s. potential reserve suits: %d' % \
                (self.doId, len(self.reserveSuits))))
            assert totalHp <= totalMaxHp
            hpPercent = 100 - (totalHp / totalMaxHp * 100.0)
            assert(self.notify.debug('%s. totalHp: %d totalMaxHp: %d percent: %f' \
                % (self.doId, totalHp, totalMaxHp, hpPercent)))
            for info in self.reserveSuits:
                if (info[1] <= hpPercent and
                    len(activeSuits) < 4):
                    assert(self.notify.debug('%s. reserve: %d joining percent: %f' \
                        % (self.doId, info[0].doId, info[1])))
                    suits.append(info[0])
                    activeSuits.append(info[0])
                    joinedReserves.append(info)
            for info in joinedReserves:
                self.reserveSuits.remove(info)

        battle.resume(joinedReserves)

    def getBattleThreeTime(self):
        # Returns the amount of time spent so far in battle three, as
        # a ratio of the expected battle three duration.  This will
        # range 0 .. 1 during the normal course of the battle; if it
        # goes beyond 1, the battle should be considered to be in
        # overtime (and should rapidly become impossibly difficult, to
        # prevent toons from dying a slow, frustrating death).
        
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)
        return t1

    def progressValue(self, fromValue, toValue):
        # Returns an interpolated value from fromValue to toValue,
        # depending on the value of self.bossDamage in the range [0,
        # self.bossMaxDamage].  It is also based on time.

        # That is, lerps the value fromValue to toValue during the
        # course of the battle.

        # t0 is the elapsed damage
        t0 = float(self.bossDamage) / float(self.bossMaxDamage)

        # t1 is the elapsed time
        elapsed = globalClock.getFrameTime() - self.battleThreeStart
        t1 = elapsed / float(self.battleThreeDuration)

        # We actually progress the value based on the larger of the
        # two, so you can't spend all day in the battle.
        t = max(t0, t1)
        
        return fromValue + (toValue - fromValue) * min(t, 1)

    def progressRandomValue(self, fromValue, toValue, radius = 0.2):

        # Similar to progressValue(), but returns a value between
        # fromValue and toValue based not exactly on the current
        # progress through the battle, but rather on a point *near*
        # the current progress through the battle (based on radius,
        # which is in the scale 0 to 0.5).
        
        # The radius starts out at zero and increases linearly to its
        # specified value in the middle of the range, then decreases
        # linearly to zero again.

        t = self.progressValue(0, 1)

        # First, choose a radius that ramps from 0 to radius to 0 again.
        radius = radius * (1.0 - abs(t - 0.5) * 2.0)

        # Then modify t based on a box around that radius.
        t += radius * random.uniform(-1, 1)
        t = max(min(t, 1.0), 0.0)

        return fromValue + (toValue - fromValue) * t

    def reportToonHealth(self):
        # Writes a notify debug message listing all of the involved
        # toons and their current health.  Useful for determining game
        # balancing.
        if self.notify.getDebug():
            str = ''
            for toonId in self.involvedToons:
                toon = self.air.doId2do.get(toonId)
                if toon:
                    str += ', %s (%s/%s)' % (toonId, toon.getHp(), toon.getMaxHp())
            self.notify.debug('%s.toons = %s' % (self.doId, str[2:]))

    def getDamageMultiplier(self):
        """Return a multiplier for our damaging attacks."""
        return 1.0
            
    def zapToon(self, x, y, z, h, p, r, bpx, bpy, attackCode, timestamp):
        # This is sent from the client when he detects a collision
        # with one of the boss attacks.
        avId = self.air.getAvatarIdFromSender()

        if not self.validate(avId, avId in self.involvedToons,
                             'zapToon from unknown avatar'):
            return

        if attackCode == ToontownGlobals.BossCogLawyerAttack and \
           self.dna.dept != 'l':
            self.notify.warning('got lawyer attack but not in CJ boss battle')
            return        

        toon = simbase.air.doId2do.get(avId)
        if toon:
            self.d_showZapToon(avId, x, y, z, h, p, r, attackCode, timestamp)

            damage = ToontownGlobals.BossCogDamageLevels.get(attackCode)
            if damage == None:
                self.notify.warning("No damage listed for attack code %s" % (attackCode))
                damage = 5

            damage *= self.getDamageMultiplier()
            self.damageToon(toon, damage)

            currState = self.getCurrentOrNextState()
            if attackCode ==  ToontownGlobals.BossCogElectricFence and \
               (currState == 'RollToBattleTwo' or currState == 'BattleThree'):
                if bpy < 0 and abs(bpx / bpy) > 0.5:
                    # If the toon hit us largely in the front and on
                    # the side, swat at him.
                    
                    if bpx < 0:
                        self.b_setAttackCode(ToontownGlobals.BossCogSwatRight)
                    else:
                        self.b_setAttackCode(ToontownGlobals.BossCogSwatLeft)

    def d_showZapToon(self, avId, x, y, z, h, p, r, attackCode, timestamp):
        self.sendUpdate('showZapToon', [avId, x, y, z, h, p, r, attackCode, timestamp])

    def b_setAttackCode(self, attackCode, avId = 0):
        self.d_setAttackCode(attackCode, avId)
        self.setAttackCode(attackCode, avId)
        

    def setAttackCode(self, attackCode, avId = 0):
        assert self.notify.debug('%s.setAttackCode(%s, %s)' % (self.doId, attackCode, avId))
        self.attackCode = attackCode
        self.attackAvId = avId

        # How long to wait for the next attack?
        if attackCode == ToontownGlobals.BossCogDizzy or attackCode == ToontownGlobals.BossCogDizzyNow:
            # Stay dizzy for a variable length of time.  It starts out
            # easier and gets harder.
            delayTime = self.progressValue(20, 5)

            # Track the number of hits while we're dizzy.
            self.hitCount = 0

        elif attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)

            # Wait a length of time after the slow attack.
            delayTime += self.progressValue(10, 0)
            
        else:
            delayTime = ToontownGlobals.BossCogAttackTimes.get(attackCode)
            if delayTime == None:
                return

        self.waitForNextAttack(delayTime)

    def d_setAttackCode(self, attackCode, avId = 0):
        self.sendUpdate('setAttackCode', [attackCode, avId])

                                
    def waitForNextAttack(self, delayTime):
        currState = self.getCurrentOrNextState()
        if (currState == 'BattleThree'):
            assert self.notify.debug("%s.Waiting %s seconds for next attack." % (self.doId, delayTime))
            taskName = self.uniqueName('NextAttack')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextAttack, taskName)
        else:
            assert self.notify.debug("%s.Not doing another attack in state %s." % (self.doId, currState))

    def stopAttacks(self):
        taskName = self.uniqueName('NextAttack')
        taskMgr.remove(taskName)

    def doNextAttack(self, task):
        # This may be overridden by a derived class to handle the
        # boss's attacks in battle three.
        self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)

