from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
import DistributedBossCogAI
from direct.directnotify import DirectNotifyGlobal
from otp.avatar import DistributedAvatarAI
import DistributedSuitAI
from toontown.battle import BattleExperienceAI
from direct.fsm import FSM
from toontown.toonbase import ToontownGlobals
from toontown.toon import InventoryBase
from toontown.toonbase import TTLocalizer
from toontown.battle import BattleBase
from toontown.toon import NPCToons
import SuitDNA
import random

class DistributedSellbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotBossAI')

    # The maximum number of hits we will take while dizzy, once our
    # damage crosses the given threshold.
    limitHitCount = 6
    hitCountDamage = 35

    # The number of pies we award for touching the cage.
    numPies = ToontownGlobals.FullPies

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 's')
        FSM.FSM.__init__(self, 'DistributedSellbotBossAI')

        # These are the suits that the Boss Cog is seen promoting when
        # the Toons come in.  Their only purpose is to provide some
        # context in the movie; they don't interact with any of the
        # Toons.
        self.doobers = []

        # Choose an NPC toon to be in the cage.
        self.cagedToonNpcId = random.choice(NPCToons.npcFriends.keys())

        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage
        self.recoverRate = 0
        self.recoverStartTime = 0

    def delete(self):
        return DistributedBossCogAI.DistributedBossCogAI.delete(self)

    def getHoodId(self):
        return ToontownGlobals.SellbotHQ

    def getCagedToonNpcId(self):
        return self.cagedToonNpcId

    def magicWordHit(self, damage, avId):
        # Called by the magic word "~bossBattle hit damage"
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            # Make him dizzy first.
            self.hitBossInsides()
        self.hitBoss(damage)

    def hitBoss(self, bossDamage):
        # This is sent when the client successfully hits the boss during
        # battle three.  We have to take the client's word for it here.
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitBoss(%s, %s)' % (self.doId, avId, bossDamage))

        if not self.validate(avId, avId in self.involvedToons,
                             'hitBoss from unknown avatar'):
            return

        # We only expect a bossDamage value of 1 from the client.  If
        # a client ever sends some other value, it's cause for
        # immediate and strong suspicion of a hacked client.  However,
        # we honor the strange bossDamage value, partly to make it
        # convenient for testing, and partly to help trap greedy
        # hackers into revealing themselves repeatedly.
        self.validate(avId, bossDamage == 1,
                      'invalid bossDamage %s' % (bossDamage))
        if bossDamage < 1:
            return

        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            # This was just a late hit; ignore it.
            return

        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            # The boss wasn't in his vulnerable state, so it doesn't count.
            return

        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)

        if self.bossDamage >= self.bossMaxDamage:
            # Only set this state locally--the clients will go there
            # by themselves when the boss movie finishes playing out.
            self.setState('NearVictory')

        else:
            self.__recordHit()

    def hitBossInsides(self):
        # This is sent when the client successfully lobs a pie inside
        # the boss's chassis.
        
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitBossInsides(%s)' % (self.doId, avId))

        if not self.validate(avId, avId in self.involvedToons,
                             'hitBossInsides from unknown avatar'):
            return

        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            # This was just a late hit; ignore it.
            return

        self.b_setAttackCode(ToontownGlobals.BossCogDizzyNow)
        self.b_setBossDamage(self.getBossDamage(), 0, 0)
        
    def hitToon(self, toonId):
        # This is sent when the client pies another toon during battle
        # three.  We have to take the client's word for it here too.
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitToon(%s, %s)' % (self.doId, avId, toonId))

        if not self.validate(avId, avId != toonId,
                             'hitToon on self'):
            return

        if avId not in self.involvedToons or toonId not in self.involvedToons:
            # Not an error, since either toon might have just died.
            return

        toon = self.air.doId2do.get(toonId)
        if toon:
            self.healToon(toon, 1)


    def touchCage(self):
        # This is sent from the client when he touches the cage,
        # requesting more pies.
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.touchCage(%s)' % (self.doId, avId))

        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree' and currState != 'NearVictory':
            return

        if not self.validate(avId, avId in self.involvedToons,
                             'touchCage from unknown avatar'):
            return

        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(self.numPies)
            toon.__touchedCage = 1
            self.__goodJump(avId)

    def finalPieSplat(self):
        # A client reports he observed the final pie splat that sends
        # the boss over the edge.  This moves the state into Victory.
        if self.state != 'NearVictory':
            return
        
        self.b_setState('Victory')

    def doNextAttack(self, task):
        assert self.notify.debug("%s.doNextAttack()" % (self.doId))
        # Choose an attack and do it.
        if self.attackCode == ToontownGlobals.BossCogDizzyNow:
            # We always choose this particular attack when recovering
            # from dizzy.  It's really the same as the front attack,
            # with extra time for standing up first.
            attackCode = ToontownGlobals.BossCogRecoverDizzyAttack

        else:
            # Choose an attack at random.
            attackCode = random.choice(
                [ToontownGlobals.BossCogAreaAttack,
                 ToontownGlobals.BossCogFrontAttack,
                 ToontownGlobals.BossCogDirectedAttack,
                 ToontownGlobals.BossCogDirectedAttack,
                 ToontownGlobals.BossCogDirectedAttack,
                 ToontownGlobals.BossCogDirectedAttack,
                 ])
            
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.__doAreaAttack()
        elif attackCode == ToontownGlobals.BossCogDirectedAttack:
            self.__doDirectedAttack()
        else:
            self.b_setAttackCode(attackCode)

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

        # Boost the recovery rate a bit with each area attack.
        if self.recoverRate:
            newRecoverRate = min(200, self.recoverRate * 1.2)
        else:
            newRecoverRate = 2
        now = globalClock.getFrameTime()
        self.b_setBossDamage(self.getBossDamage(), newRecoverRate, now)

    def __doDirectedAttack(self):
        if self.nearToons:
            toonId = random.choice(self.nearToons)
            self.b_setAttackCode(ToontownGlobals.BossCogDirectedAttack, toonId)

        else:
            # If we don't have anyone nearby to aim at, stomp in
            # frustration.
            self.__doAreaAttack()
        
    def b_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.d_setBossDamage(bossDamage, recoverRate, recoverStartTime)
        self.setBossDamage(bossDamage, recoverRate, recoverStartTime)

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        assert self.notify.debug('%s.setBossDamage(%s, %s)' % (self.doId, bossDamage, recoverRate))
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

    def getBossDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime

        # It is important that we consistently represent bossDamage as
        # an integer value, so there is never any chance of client and
        # AI disagreeing about whether bossDamage < bossMaxDamage.
        return int(max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0))

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])
                
    def waitForNextStrafe(self, delayTime):
        currState = self.getCurrentOrNextState()
        if (currState == 'BattleThree'):
            assert self.notify.debug("%s.Waiting %s seconds for next strafe." % (self.doId, delayTime))
            taskName = self.uniqueName('NextStrafe')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextStrafe, taskName)
        else:
            assert self.notify.debug("%s.Not doing another strafe in state %s." % (self.doId, currState))

    def stopStrafes(self):
        taskName = self.uniqueName('NextStrafe')
        taskMgr.remove(taskName)

    def doNextStrafe(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            side = random.choice([0, 1])
            direction = random.choice([0, 1])
            assert self.notify.debug('%s.doStrafe(%s, %s)' % (self.doId, side, direction))
            self.sendUpdate('doStrafe', [side, direction])

        # How long to wait for the next strafe?

        delayTime = 9
        self.waitForNextStrafe(delayTime)


    def __sendDooberIds(self):
        dooberIds = []
        for suit in self.doobers:
            dooberIds.append(suit.doId)
            
        self.sendUpdate('setDooberIds', [dooberIds])

    def d_cagedToonBattleThree(self, index, avId):
        self.sendUpdate('cagedToonBattleThree', [index, avId])

    def formatReward(self):
        # Returns the reward indication to write to the event log.
        return str(self.cagedToonNpcId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'RollToBattleTwo'
        self.initializeBattles(1, ToontownGlobals.SellbotBossBattleOnePosHpr)
    
    def generateSuits(self, battleNumber):
        if battleNumber == 1:
            # Battle 1
            return self.invokeSuitPlanner(9, 0)
        else:
            # Battle 2
            return self.invokeSuitPlanner(10, 1)

    def removeToon(self, avId):
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(0)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)


    ##### Off state #####

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.__resetDoobers()

    ##### Elevator state #####

    def enterElevator(self):
        DistributedBossCogAI.DistributedBossCogAI.enterElevator(self)
        self.b_setBossDamage(0, 0, 0)

    ##### Introduction state #####

    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)

        # Make up some suits for the entrance movie.
        self.__makeDoobers()

        self.b_setBossDamage(0, 0, 0)
        
    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)

        self.__resetDoobers()

    ##### BattleOne state #####

    ##### RollToBattleTwo state #####

    def enterRollToBattleTwo(self):
        assert self.notify.debug('%s.enterRollToBattleTwo()' % (self.doId))

        # Reshuffle the remaining toons for the second pair of battles.
        self.divideToons()

        # The clients will play a movie showing the boss cog moving up
        # to the top of the area for the phase 2 battle.

        self.barrier = self.beginBarrier(
            "RollToBattleTwo", self.involvedToons, 45,
            self.__doneRollToBattleTwo)

    def __doneRollToBattleTwo(self, avIds):
        self.b_setState("PrepareBattleTwo")

    def exitRollToBattleTwo(self):
        self.ignoreBarrier(self.barrier)


    ##### PrepareBattleTwo state #####

    def enterPrepareBattleTwo(self):
        assert self.notify.debug('%s.enterPrepareBattleTwo()' % (self.doId))

        # The clients will focus in on the caged toon giving some
        # encouragement and advice.  We wait for the clients to click
        # through.

        self.barrier = self.beginBarrier(
            "PrepareBattleTwo", self.involvedToons, 30,
            self.__donePrepareBattleTwo)

        self.makeBattleTwoBattles()

    def __donePrepareBattleTwo(self, avIds):
        self.b_setState("BattleTwo")

    def exitPrepareBattleTwo(self):
        self.ignoreBarrier(self.barrier)

    ##### BattleTwo state #####

    def makeBattleTwoBattles(self):
        # Create the battle objects.
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(2, ToontownGlobals.SellbotBossBattleTwoPosHpr)

    def enterBattleTwo(self):
        assert self.notify.debug('%s.enterBattleTwo()' % (self.doId))

        # The boss cog unleashes the second round of Cogs from his
        # belly.

        # Begin the battles.
        if self.battleA:
            self.battleA.startBattle(self.toonsA, self.suitsA)
        if self.battleB:
            self.battleB.startBattle(self.toonsB, self.suitsB)

    def exitBattleTwo(self):
        self.resetBattles()

    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        assert self.notify.debug('%s.enterPrepareBattleThree()' % (self.doId))

        # The clients will focus in on the caged toon giving some
        # encouragement and advice.  We wait for the clients to click
        # through.

        self.barrier = self.beginBarrier(
            "PrepareBattleThree", self.involvedToons, 30,
            self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState("BattleThree")

    def exitPrepareBattleThree(self):
        self.ignoreBarrier(self.barrier)

    ##### BattleThree state #####

    def enterBattleThree(self):
        assert self.notify.debug('%s.enterBattleThree()' % (self.doId))
        self.resetBattles()
        self.setPieType()
        self.b_setBossDamage(0, 0, 0)
        self.battleThreeStart = globalClock.getFrameTime()

        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.__touchedCage = 0

        self.waitForNextAttack(5)
        self.waitForNextStrafe(9)

        self.cagedToonDialogIndex = 100
        self.__saySomethingLater()

    def __saySomething(self, task = None):
        # The caged toon looks for something to say.
        index = None
        avId = 0

        if len(self.involvedToons) == 0:
            return

        # Choose a random Toon to "address" from the toons
        # involved.  If that toon has touched the cage, give him
        # the next bit of advice; otherwise, admonish him.
        avId = random.choice(self.involvedToons)
        toon = simbase.air.doId2do.get(avId)
        if toon.__touchedCage:
            if self.cagedToonDialogIndex <= TTLocalizer.CagedToonBattleThreeMaxAdvice:
                index = self.cagedToonDialogIndex
                self.cagedToonDialogIndex += 1
            else:
                # We've used up all the advice.  Occasionally pick one at
                # random to remind everyone.
                if random.random() < 0.2:
                    index = random.randrange(100, TTLocalizer.CagedToonBattleThreeMaxAdvice + 1)

        else:
            # The toon hasn't touched the cage yet.  Tell him how to.
            index = random.randrange(20, TTLocalizer.CagedToonBattleThreeMaxTouchCage + 1)

        if index:
            self.d_cagedToonBattleThree(index, avId)

        self.__saySomethingLater()

    def __saySomethingLater(self, delayTime = 15):
        # Say something in a few seconds.
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.__saySomething, taskName)

    def __goodJump(self, avId):
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return

        index = random.randrange(10, TTLocalizer.CagedToonBattleThreeMaxGivePies + 1)
        self.d_cagedToonBattleThree(index, avId)

        self.__saySomethingLater()

    def exitBattleThree(self):
        self.stopAttacks()
        self.stopStrafes()
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)

    ##### NearVictory state #####

    def enterNearVictory(self):
        assert self.notify.debug('%s.enterNearVictory()' % (self.doId))
        self.resetBattles()

    def exitNearVictory(self):
        pass

    ##### Victory state #####

    def enterVictory(self):
        assert self.notify.debug('%s.enterVictory()' % (self.doId))
        self.resetBattles()

        # add a suit-defeat entry for the VP
        # based on code in DistributedBattleBaseAI.__movieDone
        self.suitsKilled.append({
            'type' : None,
            'level' : None,
            'track' : self.dna.dept,
            'isSkelecog' : 0,
            'isForeman' : 0,
            'isVP' : 1,
            'isCFO' : 0,
            'isSupervisor' : 0,
            'isVirtual' : 0,
            'activeToons' : self.involvedToons[:],
            })

        self.barrier = self.beginBarrier(
            "Victory", self.involvedToons, 10,
            self.__doneVictory)

    def __doneVictory(self, avIds):

        # Tell the client the information it needs to generate a
        # reward movie.
        self.d_setBattleExperience()

        # First, move the clients into the reward start.  They'll
        # build the reward movies immediately.
        self.b_setState("Reward")

        # Now that the clients have started to build their reward
        # movies, we can actually assign all the experience and
        # rewards.  If we did this sooner, the quest reward panel
        # would show the rewards being applied twice.

        # There is no race condition between AI and client here
        # because these messages are sent sequentially on the wire.
        
        BattleExperienceAI.assignRewards(
            self.involvedToons, self.toonSkillPtsGained,
            self.suitsKilled,
            ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)

        # Don't forget to give the toon the NPC SOS reward and the
        # promotion!
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                if not toon.attemptAddNPCFriend(self.cagedToonNpcId, numCalls = 1):
                    self.notify.info("%s.unable to add NPCFriend %s to %s." % (self.doId, self.cagedToonNpcId, toonId))
                toon.b_promote(self.deptIndex)

    def exitVictory(self):
        self.takeAwayPies()

    ##### Frolic state #####

    def enterFrolic(self):
        DistributedBossCogAI.DistributedBossCogAI.enterFrolic(self)
        self.b_setBossDamage(0, 0, 0)


    def __resetDoobers(self):
        # Free the suits made with an earlier call to __makeDoobers().
        for suit in self.doobers:
            suit.requestDelete()
        self.doobers = []

    def __makeDoobers(self):

        # Generate a handful of suits that we can see the Boss Cog
        # promoting as we come in.  These shouldn't really need to be
        # true DistributedSuits, but I tried to make just a Suit by
        # itself and it just doesn't work.  It doesn't do any real
        # harm to make DistributedSuits, anyway.

        self.__resetDoobers()

        # 8 suits, 4 on each side.
        for i in range(8):
            suit = DistributedSuitAI.DistributedSuitAI(self.air, None)

            # Choose a random level for each new suit.
            level = random.randrange(len(SuitDNA.suitsPerLevel))

            # And a random type to match the level.
            suit.dna = SuitDNA.SuitDNA()
            suit.dna.newSuitRandom(level = level, dept = self.dna.dept)
            suit.setLevel(level)

            suit.generateWithRequired(self.zoneId)
            self.doobers.append(suit)

        self.__sendDooberIds()

    def setPieType(self):
        # Sets everyone's pie type for the battle.
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.d_setPieType(4)

    def takeAwayPies(self):
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setNumPies(0)

    def __recordHit(self):
        # Records that the boss has been hit, and counts the number of
        # hits in a period of time.
        now = globalClock.getFrameTime()

        self.hitCount += 1
        if (self.hitCount < self.limitHitCount or self.bossDamage < self.hitCountDamage):
            assert self.notify.debug("%s. %s hits, ignoring." % (self.doId, self.hitCount))
            return

        assert self.notify.debug("%s. %s hits!" % (self.doId, self.hitCount))

        # Launch an immediate front attack.
        self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)
            
        
