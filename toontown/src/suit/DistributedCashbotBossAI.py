from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.coghq import DistributedCashbotBossCraneAI
from toontown.coghq import DistributedCashbotBossSafeAI
from toontown.suit import DistributedCashbotBossGoonAI
from toontown.coghq import DistributedCashbotBossTreasureAI
from toontown.battle import BattleExperienceAI
from toontown.chat import ResistanceChat
from direct.fsm import FSM
import DistributedBossCogAI
import SuitDNA
import random
import math

class DistributedCashbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossAI')

    maxGoons = 8

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'm')
        FSM.FSM.__init__(self, 'DistributedCashbotBossAI')
        self.cranes = None
        self.safes = None
        self.goons = None
        self.treasures = {}
        self.grabbingTreasures = {}
        self.recycledTreasures = []

        # The treasures will look for this quantity on their
        # "TreasurePlanner", which is the boss cog.  This is just the
        # initial default value; we reassign each treasure
        # differently.
        self.healAmount = 0

        # Choose a random reward up front in case they succeed.
        self.rewardId = ResistanceChat.getRandomId()
        self.rewardedToons = []
        
        # We need a scene to do the collision detection in.
        self.scene = NodePath('scene')
        self.reparentTo(self.scene)

        # And some solids to keep the goons constrained to our room.
        cn = CollisionNode('walls')
        cs = CollisionSphere(0, 0, 0, 13)
        cn.addSolid(cs)
        cs = CollisionInvSphere(0, 0, 0, 42)
        cn.addSolid(cs)
        self.attachNewNode(cn)
        

        # By "heldObject", we mean the safe he's currently wearing as
        # a helmet, if any.  It's called a heldObject because this is
        # the way the cranes refer to the same thing, and we use the
        # same interface to manage this.
        self.heldObject = None

        self.waitingForHelmet = 0
        self.avatarHelmets = {}

        self.bossMaxDamage = ToontownGlobals.CashbotBossMaxDamage

    def generate(self):
        """
        Inheritors should put functions that require self.zoneId or
        other networked info in this function.
        """
        DistributedBossCogAI.DistributedBossCogAI.generate(self)

        if __dev__:
            self.scene.reparentTo(self.getRender())
            
    def getHoodId(self):
        return ToontownGlobals.CashbotHQ

    def formatReward(self):
        # Returns the reward indication to write to the event log.
        return str(self.rewardId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(1, ToontownGlobals.CashbotBossBattleOnePosHpr)
    
    def generateSuits(self, battleNumber):
        cogs =  self.invokeSuitPlanner(11, 0)
        skelecogs =  self.invokeSuitPlanner(12, 1)

        # Now combine the lists of suits together, so that they all
        # come out mix-and-match.
        activeSuits = cogs['activeSuits'] + skelecogs['activeSuits']
        reserveSuits = cogs['reserveSuits'] + skelecogs['reserveSuits']

        random.shuffle(activeSuits)

        # We might have ended up with too many suits on the
        # activeSuits list.  If that happens, put the overflow suits
        # on the reserve list, with a 100% joinChance.
        while len(activeSuits) > 4:
            suit = activeSuits.pop()
            reserveSuits.append((suit, 100))

        # We must keep the reserveSuits sorted in increasing order of
        # joinChance.
        def compareJoinChance(a, b):
            return cmp(a[1], b[1])
        reserveSuits.sort(compareJoinChance)
        
        return { 'activeSuits' : activeSuits, 'reserveSuits' : reserveSuits }

    def removeToon(self, avId):
        # The toon leaves the zone, either through disconnect, death,
        # or something else.  Tell all of the safes, cranes, and goons.

        if self.cranes != None:
            for crane in self.cranes:
                crane.removeToon(avId)

        if self.safes != None:
            for safe in self.safes:
                safe.removeToon(avId)

        if self.goons != None:
            for goon in self.goons:
                goon.removeToon(avId)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)

    def __makeBattleThreeObjects(self):
        if self.cranes == None:
            # Generate all of the cranes.
            self.cranes = []
            for index in range(len(ToontownGlobals.CashbotBossCranePosHprs)):
                crane = DistributedCashbotBossCraneAI.DistributedCashbotBossCraneAI(self.air, self, index)
                crane.generateWithRequired(self.zoneId)
                self.cranes.append(crane)

        if self.safes == None:
            # And all of the safes.
            self.safes = []
            for index in range(len(ToontownGlobals.CashbotBossSafePosHprs)):
                safe = DistributedCashbotBossSafeAI.DistributedCashbotBossSafeAI(self.air, self, index)
                safe.generateWithRequired(self.zoneId)
                self.safes.append(safe)

        if self.goons == None:
            # We don't actually make the goons right now, but we make
            # a place to hold them.
            self.goons = []

    def __resetBattleThreeObjects(self):
        if self.cranes != None:
            for crane in self.cranes:
                crane.request('Free')

        if self.safes != None:
            for safe in self.safes:
                safe.request('Initial')

    def __deleteBattleThreeObjects(self):
        if self.cranes != None:
            for crane in self.cranes:
                crane.request('Off')
                crane.requestDelete()
            self.cranes = None

        if self.safes != None:
            for safe in self.safes:
                safe.request('Off')
                safe.requestDelete()
            self.safes = None

        if self.goons != None:
            for goon in self.goons:
                goon.request('Off')
                goon.requestDelete()
            self.goons = None

    def doNextAttack(self, task):
        assert self.notify.debug("%s.doNextAttack()" % (self.doId))
        # Choose an attack and do it.

        # For now, we only do the directed attack.
        self.__doDirectedAttack()

        # Make sure we're waiting for a helmet.
        if self.heldObject == None and not self.waitingForHelmet:
            self.waitForNextHelmet()

    def __doDirectedAttack(self):
        # Choose the next toon in line to get the assault.
        if self.toonsToAttack:
            toonId = self.toonsToAttack.pop(0)
            while toonId not in self.involvedToons:
                # Oops, this toon is gone.
                if not self.toonsToAttack:
                    # Say, everyone's gone.
                    self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                    return
                toonId = self.toonsToAttack.pop(0)
                
            self.toonsToAttack.append(toonId)
            self.b_setAttackCode(ToontownGlobals.BossCogSlowDirectedAttack, toonId)

    def reprieveToon(self, avId):
        # Moves the indicated toon to the tail of the attack queue.
        if avId in self.toonsToAttack:
            i = self.toonsToAttack.index(avId)
            del self.toonsToAttack[i]
            self.toonsToAttack.append(avId)

    def makeTreasure(self, goon):
        # Places a treasure, as pooped out by the given goon.  We
        # place the treasure at the goon's current position, or at
        # least at the beginning of its current path.  Actually, we
        # ignore Z, and always place the treasure at Z == 0,
        # presumably the ground.

        if self.state != 'BattleThree':
            return

        # The BossCog acts like a treasure planner as far as the
        # treasure is concerned.
        pos = goon.getPos(self)

        # The treasure pops out and lands somewhere nearby.  Let's
        # start by choosing a point on a ring around the boss, based
        # on our current angle to the boss.
        v = Vec3(pos[0], pos[1], 0.0)
        if not v.normalize():
            v = Vec3(1, 0, 0)
        v = v * 27

        # Then perterb that point by a distance in some random
        # direction.
        angle = random.uniform(0.0, 2.0 * math.pi)
        radius = 10
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        
        fpos = self.scene.getRelativePoint(self, Point3(v[0] + dx, v[1] + dy, 0))

        if goon.strength <= 10:
            style = ToontownGlobals.ToontownCentral
            healAmount = 3

        elif goon.strength <= 15:
            style = random.choice(
                [ToontownGlobals.DonaldsDock,
                 ToontownGlobals.DaisyGardens,
                 ToontownGlobals.MinniesMelodyland]) 
            healAmount = 10

        else:
            style = random.choice(
                [ToontownGlobals.TheBrrrgh,
                 ToontownGlobals.DonaldsDreamland])
            healAmount = 12

        if self.recycledTreasures:
            # Reuse a previous treasure object
            treasure = self.recycledTreasures.pop(0)
            treasure.d_setGrab(0)
            treasure.b_setGoonId(goon.doId)
            treasure.b_setStyle(style)
            treasure.b_setPosition(pos[0], pos[1], 0)
            treasure.b_setFinalPosition(fpos[0], fpos[1], 0)
            
        else:
            # Create a new treasure object
            treasure = DistributedCashbotBossTreasureAI.DistributedCashbotBossTreasureAI(
                self.air, self, goon,
                style, fpos[0], fpos[1], 0)
            treasure.generateWithRequired(self.zoneId)

        treasure.healAmount = healAmount
        self.treasures[treasure.doId] = treasure

    def grabAttempt(self, avId, treasureId):
        # An avatar has attempted to grab a treasure.
        av = self.air.doId2do.get(avId)
        if not av:
            return
        
        treasure = self.treasures.get(treasureId)
        if treasure:
            if treasure.validAvatar(av):
                del self.treasures[treasureId]
                treasure.d_setGrab(avId)
                self.grabbingTreasures[treasureId] = treasure
                # Wait a few seconds for the animation to play, then
                # recycle the treasure.
                taskMgr.doMethodLater(5, self.__recycleTreasure,
                                      treasure.uniqueName('recycleTreasure'),
                                      extraArgs = [treasure])
            else:
                treasure.d_setReject()

    def __recycleTreasure(self, treasure):
        if self.grabbingTreasures.has_key(treasure.doId):
            del self.grabbingTreasures[treasure.doId]
            self.recycledTreasures.append(treasure)

    def deleteAllTreasures(self):
        for treasure in self.treasures.values():
            treasure.requestDelete()
        self.treasures = {}

        for treasure in self.grabbingTreasures.values():
            taskMgr.remove(treasure.uniqueName('recycleTreasure'))
            treasure.requestDelete()
        self.grabbingTreasures = {}

        for treasure in self.recycledTreasures:
            treasure.requestDelete()
        self.recycledTreasures = []

    def getMaxGoons(self):
        # Returns the number of goons to make.
        t = self.getBattleThreeTime()
        if t <= 1.0:
            # Normally, we make the specified number.
            return self.maxGoons

        elif t <= 1.1:
            # If the battle goes into overtime, we throw out one
            # additional goon every three minutes until they all
            # succumb.
            return self.maxGoons + 1
        
        elif t <= 1.2:
            return self.maxGoons + 2

        elif t <= 1.3:
            return self.maxGoons + 3

        elif t <= 1.4:
            return self.maxGoons + 4

        else:
            return self.maxGoons + 8

        
    def makeGoon(self, side = None):
        if side == None:
            side = random.choice(['EmergeA', 'EmergeB'])            
        
        # First, look to see if we have a goon we can recycle.
        goon = self.__chooseOldGoon()
        if goon == None:
            # No, no old goon; is there room for a new one?
            if len(self.goons) >= self.getMaxGoons():
                return

            # make a new one.
            goon = DistributedCashbotBossGoonAI.DistributedCashbotBossGoonAI(self.air, self)
            goon.generateWithRequired(self.zoneId)
            self.goons.append(goon)

        if self.getBattleThreeTime() > 1.0:
            # If the battle goes into overtime, we only make
            # SuperGoons.
            goon.STUN_TIME = 4
            goon.b_setupGoon(velocity = 8,
                             hFov = 90,
                             attackRadius = 20,
                             strength = 30,
                             scale = 1.8)
        else:
            # Normally, we make regular goons.
            goon.STUN_TIME = self.progressValue(30, 8)
            goon.b_setupGoon(velocity = self.progressRandomValue(3, 7),
                             hFov = self.progressRandomValue(70, 80),
                             attackRadius = self.progressRandomValue(6, 15),
                             strength = int(self.progressRandomValue(5, 25)),
                             scale = self.progressRandomValue(0.5, 1.5))
        
        goon.request(side)

    def __chooseOldGoon(self):
        # Walks through the list of goons managed by the boss to see
        # if any of them have recently been deleted and can be
        # recycled.
        for goon in self.goons:
            if goon.state == 'Off':
                return goon
                
    def waitForNextGoon(self, delayTime):
        currState = self.getCurrentOrNextState()
        if (currState == 'BattleThree'):
            taskName = self.uniqueName('NextGoon')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextGoon, taskName)

    def stopGoons(self):
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)

    def doNextGoon(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzy:
            self.makeGoon()

        # How long to wait for the next goon?

        delayTime = self.progressValue(10, 2)
        self.waitForNextGoon(delayTime)
                
    def waitForNextHelmet(self):
        currState = self.getCurrentOrNextState()
        if (currState == 'BattleThree'):
            taskName = self.uniqueName('NextHelmet')
            taskMgr.remove(taskName)
            delayTime = self.progressValue(45, 15)
            taskMgr.doMethodLater(delayTime, self.__donHelmet, taskName)
            self.waitingForHelmet = 1

    def __donHelmet(self, task):
        self.waitingForHelmet = 0
        if self.heldObject == None:
            # Ok, the boss wants to put on a helmet now.  He can have
            # his special safe 0, which was created for just this
            # purpose.
            safe = self.safes[0]
            safe.request('Grabbed', self.doId, self.doId)
            self.heldObject = safe

    def stopHelmets(self):
        self.waitingForHelmet = 0
        taskName = self.uniqueName('NextHelmet')
        taskMgr.remove(taskName)

    def acceptHelmetFrom(self, avId):
        # Returns true if we can accept a helmet from the indicated
        # avatar, false otherwise.  Each avatar gets a timeout of five
        # minutes after giving us a helmet, so we don't accept too
        # many helmets from the same avatar--this cuts down on helmet
        # griefing.
        now = globalClock.getFrameTime()
        then = self.avatarHelmets.get(avId, None)
        if then == None or (now - then > 300):
            self.avatarHelmets[avId] = now
            return 1

        return 0
        

    def magicWordHit(self, damage, avId):
        # Called by the magic word "~bossBattle hit damage"
        if self.heldObject:
            # Drop the current helmet.
            self.heldObject.demand('Dropped', avId, self.doId)
            self.heldObject.avoidHelmet = 1
            self.heldObject = None
            self.waitForNextHelmet()

        else:
            # Ouch!
            self.recordHit(damage)
        
    def magicWordReset(self):
        # Resets all of the cranes and safes.
        # Called only by the magic word "~bossBattle reset"
        if self.state == 'BattleThree':
            self.__resetBattleThreeObjects()
        
    def magicWordResetGoons(self):
        # Resets all of the goons.
        # Called only by the magic word "~bossBattle goons"
        if self.state == 'BattleThree':
            if self.goons != None:
                for goon in self.goons:
                    goon.request('Off')
                    goon.requestDelete()
                self.goons = None

            self.__makeBattleThreeObjects()

    def recordHit(self, damage):
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.recordHit(%s, %s)' % (self.doId, avId, damage))
        if not self.validate(avId, avId in self.involvedToons,
                             'recordHit from unknown avatar'):
            return

        if self.state != 'BattleThree':
            return

        # Record a successful hit in battle three.
        self.b_setBossDamage(self.bossDamage + damage)

        if self.bossDamage >= self.bossMaxDamage:
            # Congratulations!
            self.b_setState('Victory')

        elif self.attackCode != ToontownGlobals.BossCogDizzy:
            if damage >= ToontownGlobals.CashbotBossKnockoutDamage:
                # A particularly good hit (when he's not already
                # dizzy) will make the boss dizzy for a little while.
                self.b_setAttackCode(ToontownGlobals.BossCogDizzy)
                self.stopHelmets()
            else:
                self.b_setAttackCode(ToontownGlobals.BossCogNoAttack)
                self.stopHelmets()
                self.waitForNextHelmet()
        
    def b_setBossDamage(self, bossDamage):
        self.d_setBossDamage(bossDamage)
        self.setBossDamage(bossDamage)

    def setBossDamage(self, bossDamage):
        assert self.notify.debug('%s.setBossDamage(%s)' % (self.doId, bossDamage))
        self.reportToonHealth()
        self.bossDamage = bossDamage

    def d_setBossDamage(self, bossDamage):
        self.sendUpdate('setBossDamage', [bossDamage])

    def d_setRewardId(self, rewardId):
        self.sendUpdate('setRewardId', [rewardId])

    def applyReward(self):
        # The client has reached that point in the movie where he
        # should have the reward applied to him.
        
        avId = self.air.getAvatarIdFromSender()
        if avId in self.involvedToons and \
           avId not in self.rewardedToons:
            self.rewardedToons.append(avId)
            toon = self.air.doId2do.get(avId)
            if toon:
                toon.doResistanceEffect(self.rewardId)

    ##### Off state #####

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.rewardedToons = []

    def exitOff(self):
        DistributedBossCogAI.DistributedBossCogAI.exitOff(self)

    ##### Introduction state #####

    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)

        # We want to have cranes and safes visible in the next room
        # for the introduction cutscene.
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)

        # Clean up battle objects until we need them again later.
        self.__deleteBattleThreeObjects()

    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        assert self.notify.debug('%s.enterPrepareBattleThree()' % (self.doId))

        self.resetBattles()

        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

        # The clients will play a cutscene.  When they are done
        # watching the movie, we continue.

        self.barrier = self.beginBarrier(
            "PrepareBattleThree", self.involvedToons, 55,
            self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState("BattleThree")
        
    def exitPrepareBattleThree(self):

        if self.newState != 'BattleThree':
            self.__deleteBattleThreeObjects()
        
        self.ignoreBarrier(self.barrier)

    ##### BattleThree state #####

    def enterBattleThree(self):
        assert self.notify.debug('%s.enterBattleThree()' % (self.doId))

        # It's important to set our position correctly even on the AI,
        # so the goons can orient to the center of the room.
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)

        # Just in case we didn't pass through PrepareBattleThree state.
        self.__makeBattleThreeObjects()
        self.__resetBattleThreeObjects()

        self.reportToonHealth()

        # A list of toons to attack.  We start out with the list in
        # random order.
        self.toonsToAttack = self.involvedToons[:]
        random.shuffle(self.toonsToAttack)

        self.b_setBossDamage(0)
        self.battleThreeStart = globalClock.getFrameTime()
        
        self.resetBattles()
        self.waitForNextAttack(15)
        self.waitForNextHelmet()

        # Make four goons up front to keep things interesting from the
        # beginning.
        self.makeGoon(side = 'EmergeA')
        self.makeGoon(side = 'EmergeB')
        taskName = self.uniqueName('NextGoon')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(2, self.__doInitialGoons, taskName)
        
    def __doInitialGoons(self, task):
        self.makeGoon(side = 'EmergeA')
        self.makeGoon(side = 'EmergeB')
        self.waitForNextGoon(10)

    def exitBattleThree(self):
        helmetName = self.uniqueName('helmet')
        taskMgr.remove(helmetName)

        if self.newState != 'Victory':
            self.__deleteBattleThreeObjects()
        self.deleteAllTreasures()
        self.stopAttacks()
        self.stopGoons()
        self.stopHelmets()
        self.heldObject = None
          
    

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
            'isVP' : 0,
            'isCFO' : 1,
            'isSupervisor' : 0,
            'isVirtual' : 0,
            'activeToons' : self.involvedToons[:],
            })

        self.barrier = self.beginBarrier(
            "Victory", self.involvedToons, 30,
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

        # Don't forget to give the toon the resistance chat reward and the
        # promotion!
        
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.addResistanceMessage(self.rewardId)
                toon.b_promote(self.deptIndex)

    def exitVictory(self):
        self.__deleteBattleThreeObjects()
    

    ##### Epilogue state #####

    def enterEpilogue(self):
        DistributedBossCogAI.DistributedBossCogAI.enterEpilogue(self)

        # Tell the clients now what the reward Id will be.
        self.d_setRewardId(self.rewardId)
