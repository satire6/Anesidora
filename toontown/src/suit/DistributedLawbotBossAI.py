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
from toontown.building import SuitBuildingGlobals
import SuitDNA
import random
from toontown.coghq import DistributedLawbotBossGavelAI
from toontown.suit import DistributedLawbotBossSuitAI
from toontown.coghq import DistributedLawbotCannonAI
from toontown.coghq import DistributedLawbotChairAI
from toontown.toonbase import ToontownBattleGlobals

class DistributedLawbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBossAI')

    # The maximum number of hits we will take while dizzy, once our
    # damage crosses the given threshold.
    limitHitCount = 6
    hitCountDamage = 35

    # The number of pies we award for touching the cage.
    #numPies = ToontownGlobals.FullPies
    numPies = 10

    #the cap we use for the toon level difficulty
    maxToonLevels = 77
    
    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'l')
        FSM.FSM.__init__(self, 'DistributedLawbotBossAI')

        # These are the prosecution lawyers
        self.lawyers = []

        self.cannons = None
        self.chairs = None

        self.gavels = None


        # Choose an NPC toon to be in the cage.
        self.cagedToonNpcId = random.choice(NPCToons.npcFriends.keys())

        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        self.recoverRate = 0
        self.recoverStartTime = 0


        # Accumulated hits on the boss during the climactic final
        # battle (battle three)
        self.bossDamage = ToontownGlobals.LawbotBossInitialDamage

        #are we using cannons in battle two
        self.useCannons = 1

        #how many toon jurors did we seat in battle two
        self.numToonJurorsSeated = 0        

        self.cannonBallsLeft = {}

        self.toonLevels = 0

        #keep track in the server log when they lose the trial
        if not 'Defeat' in self.keyStates:
            self.keyStates.append('Defeat')

        self.toonupValue = 1

        self.bonusState = False
        self.bonusTimeStarted = 0
        self.numBonusStates = 0
        self.battleThreeTimeStarted = 0
        self.battleThreeTimeInMin = 0
        self.numAreaAttacks = 0
        self.lastAreaAttackTime = 0

        self.weightPerToon = {} #each toons evidence weight can be different
        self.cannonIndexPerToon = {} #keep track which cannon a toon used

        self.battleDifficulty = 0 #how difficult is battle three
        
    def delete(self):
        self.notify.debug('DistributedLawbotBossAI.delete')
        self.__deleteBattleThreeObjects()
        self.__deleteBattleTwoObjects()

        taskName = self.uniqueName('clearBonus')            
        taskMgr.remove(taskName)
        
        return DistributedBossCogAI.DistributedBossCogAI.delete(self)


    def getHoodId(self):
        return ToontownGlobals.LawbotHQ

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

        #if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            # The boss wasn't in his vulnerable state, so it doesn't count.
        #    return

        if bossDamage <= 12:
            #change the bossDamage to reflect the bonusWeight
            newWeight = self.weightPerToon.get(avId)
            if newWeight:
                bossDamage = newWeight
            

        if self.bonusState and bossDamage <= 12:
            #we hit the scale and the bonus state is happening
            bossDamage *= ToontownGlobals.LawbotBossBonusWeightMultiplier
            

        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)

        if self.bossDamage >= self.bossMaxDamage:
            #transition directly to victory state,  Lawbot boss does not have NearVictory state while he waits to fall
            self.b_setState('Victory')

        else:
            self.__recordHit()

    def healBoss(self, bossHeal):
        """
        mostly copy and paste from hit boss, without the bossDamage<1 check
        """
        bossDamage = -bossHeal

        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitBoss(%s, %s)' % (self.doId, avId, bossDamage))

        #if not self.validate(avId, avId in self.involvedToons,
        #                     'hitBoss from unknown avatar'):
        #    return

        # We only expect a bossDamage value of 1 from the client.  If
        # a client ever sends some other value, it's cause for
        # immediate and strong suspicion of a hacked client.  However,
        # we honor the strange bossDamage value, partly to make it
        # convenient for testing, and partly to help trap greedy
        # hackers into revealing themselves repeatedly.
        #self.validate(avId, bossDamage == 1,
        #              'invalid bossDamage %s' % (bossDamage))

        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            # This was just a late hit; ignore it.
            return

        #if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            # The boss wasn't in his vulnerable state, so it doesn't count.
        #    return

        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        bossDamage = max(bossDamage, 0) #make sure the damage is not neg
        self.b_setBossDamage(bossDamage, 0, 0)

        #if self.bossDamage >= self.bossMaxDamage:
        if self.bossDamage == 0:
            # the toons lost
            self.b_setState('Defeat')

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
            self.healToon(toon, self.toonupValue)
            self.sendUpdate('toonGotHealed',[toonId])


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
            #this call would call cagedToonBattleThree which has been nuked
            #self.__goodJump(avId)

    def touchWitnessStand(self):
        # This is sent from the client when he touches the witness Stand
        self.touchCage()



    def finalPieSplat(self):
        """
        A client reports he observed the final pie splat that sends
        the boss over the edge.  This moves the state into Victory.
        """
        self.notify.debug("finalPieSplat")
        if self.state != 'NearVictory':
            return
        
        self.b_setState('Victory')

    def doTaunt(self):
        if not self.state == 'BattleThree':
            return
        
        tauntIndex = random.randrange( len(TTLocalizer.LawbotBossTaunts))
        extraInfo = 0;
        if tauntIndex == 0 and self.involvedToons:
            extraInfo = random.randrange( len(self.involvedToons))
        self.sendUpdate('setTaunt', [tauntIndex, extraInfo])
        pass

    def doNextAttack(self, task):
        assert self.notify.debug("%s.doNextAttack()" % (self.doId))

        #TODO this will make the lawyers move in lock step, make each lawyer go on an independent timer
        for lawyer in self.lawyers:
            lawyer.doNextAttack(self)

        self.waitForNextAttack(ToontownGlobals.LawbotBossLawyerCycleTime)
        timeSinceLastAttack = globalClock.getFrameTime() - self.lastAreaAttackTime
        allowedByTime = 15 < timeSinceLastAttack or self.lastAreaAttackTime == 0

        doAttack = random.randrange(1,101)
        self.notify.debug('allowedByTime=%d doAttack=%d' % (allowedByTime,doAttack))
        if doAttack <= ToontownGlobals.LawbotBossChanceToDoAreaAttack and allowedByTime:
            self.__doAreaAttack()
            self.numAreaAttacks += 1
            self.lastAreaAttackTime = globalClock.getFrameTime()
        else:
            chanceToDoTaunt = ToontownGlobals.LawbotBossChanceForTaunt
            action = random.randrange(1,101)
            if action <= chanceToDoTaunt:
                self.doTaunt()
                pass



        #RAU do nothing for now
        return;
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
        #if self.recoverRate:
        #    newRecoverRate = min(200, self.recoverRate * 1.2)
        #else:
        #    newRecoverRate = 2
        #now = globalClock.getFrameTime()
        #self.b_setBossDamage(self.getBossDamage(), newRecoverRate, now)

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
        #import pdb; pdb.set_trace()
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

    def __sendLawyerIds(self):
        lawyerIds = []
        for suit in self.lawyers:
            lawyerIds.append(suit.doId)

        self.sendUpdate('setLawyerIds',[lawyerIds])


    def d_cagedToonBattleThree(self, index, avId):
        self.sendUpdate('cagedToonBattleThree', [index, avId])

    def formatReward(self):
        # Returns the reward indication to write to the event log.
        return str(self.cagedToonNpcId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'RollToBattleTwo'
        self.initializeBattles(1, ToontownGlobals.LawbotBossBattleOnePosHpr)
    
    def generateSuits(self, battleNumber):
        if battleNumber == 1:
            # Battle 1

            # building difficulty 13, first battle with Lawbot Boss. These
            # are normal cogs.
            weakenedValue = ( ( 1, 1 ),
                              ( 2, 2 ),
                              ( 2, 2 ),
                              ( 1, 1 ),
                              ( 1, 1, 1, 1, 1 ) )
            listVersion = list(SuitBuildingGlobals.SuitBuildingInfo)
            #self.notify.debug("listversion = ")
            #print(listversion))
            #self.notify.debug("listVersion[13] = ")
            #print listVersion[13]

            if simbase.config.GetBool('lawbot-boss-cheat',0):
                listVersion[13] = weakenedValue
                SuitBuildingGlobals.SuitBuildingInfo = tuple(listVersion)
            return self.invokeSuitPlanner(13, 0)
        else:
            # Battle 2
            return self.invokeSuitPlanner(13, 1)

    def removeToon(self, avId):
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(0)

        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)


    ##### Off state #####

    def enterOff(self):
        self.notify.debug("enterOff")
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.__deleteBattleThreeObjects()
        self.__resetLawyers()


    ##### Elevator state #####

    def enterElevator(self):
        self.notify.debug("enterElevatro")
        DistributedBossCogAI.DistributedBossCogAI.enterElevator(self)
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage, 0, 0)

    ##### Introduction state #####

    def enterIntroduction(self):
        self.notify.debug("enterIntroduction")
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)

        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage, 0, 0)

        # We want to have cranes and safes visible in the next room
        # for the introduction cutscene.
        #self.__makeBattleThreeObjects()

        #we nees to show the jury chairs
        self.__makeChairs()
        
    def exitIntroduction(self):
        self.notify.debug("exitIntroduction")
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)


    ##### BattleOne state #####

    ##### RollToBattleTwo state #####

    def enterRollToBattleTwo(self):
        assert self.notify.debug('%s.enterRollToBattleTwo()' % (self.doId))

        # Reshuffle the remaining toons for the second pair of battles.
        self.divideToons()


        # The clients will play a movie showing the boss cog moving up
        # to the top of the area for the phase 2 battle.

        #might as well make the cannons in the idle time that we have
        self.__makeCannons()        

        self.barrier = self.beginBarrier(
            "RollToBattleTwo", self.involvedToons, 50,
            self.__doneRollToBattleTwo)

    def __doneRollToBattleTwo(self, avIds):
        #import pdb; pdb.set_trace()     
        assert(self.notify.debug('%s.__doneRollToBattleTwo()' % (self.doId)))        
        self.b_setState("PrepareBattleTwo")

    def exitRollToBattleTwo(self):
        #import pdb; pdb.set_trace()        
        self.ignoreBarrier(self.barrier)


    ##### PrepareBattleTwo state #####


    def enterPrepareBattleTwo(self):
        assert self.notify.debug('%s.enterPrepareBattleTwo()' % (self.doId))

        # The clients will focus in on the caged toon giving some
        # encouragement and advice.  We wait for the clients to click
        # through.

        self.__makeCannons()

        self.barrier = self.beginBarrier(
            "PrepareBattleTwo", self.involvedToons, 45,
            self.__donePrepareBattleTwo)

        self.makeBattleTwoBattles()

    def __donePrepareBattleTwo(self, avIds):
        #import pdb; pdb.set_trace()
        self.b_setState("BattleTwo")

    def exitPrepareBattleTwo(self):
        #import pdb; pdb.set_trace()
        self.ignoreBarrier(self.barrier)

    ##### BattleTwo state #####        

    def __makeCannons(self):
        if self.cannons == None:
            # Generate all of the cannons.
            self.cannons = []

            startPt = Point3(*ToontownGlobals.LawbotBossCannonPosA)
            endPt = Point3(*ToontownGlobals.LawbotBossCannonPosB)
            totalDisplacement = endPt - startPt           
            self.notify.debug('totalDisplacement=%s' % totalDisplacement)
            numToons = len(self.involvedToons)
            stepDisplacement = totalDisplacement / (numToons + 1)
            for index in range(numToons):
                newPos =  stepDisplacement * (index  + 1)
                self.notify.debug('curDisplacement = %s' % newPos)
                newPos += startPt
                self.notify.debug('newPos = %s' % newPos)
                cannon = DistributedLawbotCannonAI.DistributedLawbotCannonAI(
                    self.air, self, index,
                    newPos[0], newPos[1], newPos[2], -90, 0, 0 )
                cannon.generateWithRequired(self.zoneId)
                self.cannons.append(cannon)
        
            if 0:
                for index in range(len(ToontownGlobals.LawbotBossCannonPosHprs)):
                    posHpr = ToontownGlobals.LawbotBossCannonPosHprs[index]
                    cannon = DistributedLawbotCannonAI.DistributedLawbotCannonAI(self.air, self, posHpr[0], posHpr[1], posHpr[2], posHpr[3], posHpr[4], posHpr[5] )
                    cannon.generateWithRequired(self.zoneId)
                    self.cannons.append(cannon)



    def __makeChairs(self):
        if self.chairs == None:
            self.chairs = []
            
            for index in range(12):
                #posHpr = ToontownGlobals.LawbotBossChairPosHprs[index]
                chair = DistributedLawbotChairAI.DistributedLawbotChairAI(self.air, self, index)
                chair.generateWithRequired(self.zoneId)
                #chair.requestEmptyJuror()
                self.chairs.append(chair)
        
            

    def __makeBattleTwoObjects(self):
        self.__makeCannons()
        self.__makeChairs()

    def __deleteCannons(self):
        if self.cannons != None:
            for cannon in self.cannons:
                cannon.requestDelete()
            self.cannons = None

    def __deleteChairs(self):
        if self.chairs  != None:
            for chair in self.chairs:
                chair.requestDelete()
            self.chairs = None

    def __stopChairs(self):
        if self.chairs != None:
            for chair in self.chairs:
                chair.stopCogs()

    def __deleteBattleTwoObjects(self):
        self.__deleteCannons()
        self.__deleteChairs()


    def getCannonBallsLeft(self, avId):
        if self.cannonBallsLeft.has_key(avId):
            return self.cannonBallsLeft[avId]
        else:
            self.notify.warning('getCannonBalsLeft invalid avId: %d' % avId)
            return 0

    def decrementCannonBallsLeft( self ,avId):
        if self.cannonBallsLeft.has_key(avId):
            self.cannonBallsLeft[avId] -= 1
            if self.cannonBallsLeft[avId] < 0:
                self.notify.warning('decrementCannonBallsLeft <0 cannonballs for %d' % avId)
                self.cannonBallsLeft[avId] = 0
        else:
            self.notify.warning('decrementCannonBallsLeft invalid avId: %d' % avId)

        

    def makeBattleTwoBattles(self):
        # Create the battle objects.
        #self.postBattleState = 'PrepareBattleThree'
        self.postBattleState = 'RollToBattleThree'

        if self.useCannons:
            self.__makeBattleTwoObjects()
        else:
            self.initializeBattles(2, ToontownGlobals.LawbotBossBattleTwoPosHpr)



    def enterBattleTwo(self):
        assert self.notify.debug('%s.enterBattleTwo()' % (self.doId))

        
        if self.useCannons:
            self.cannonBallsLeft = {}
            for toonId in self.involvedToons:
                self.cannonBallsLeft[toonId] = ToontownGlobals.LawbotBossCannonBallMax

            for chair in self.chairs:
                chair.requestEmptyJuror()
            

            self.barrier = self.beginBarrier(
                "BattleTwo",
                self.involvedToons,
                ToontownGlobals.LawbotBossJuryBoxMoveTime + 1,
                self.__doneBattleTwo)


        # The boss cog unleashes the second round of Cogs from his
        # belly.

        if not self.useCannons:
            # Begin the battles.
            if self.battleA:
                self.battleA.startBattle(self.toonsA, self.suitsA)
            if self.battleB:
                self.battleB.startBattle(self.toonsB, self.suitsB)

    def __doneBattleTwo(self, avIds):
        #import pdb; pdb.set_trace()     
        assert(self.notify.debug('%s.__doneBattleTwo' % (self.doId)))        

        if self.useCannons:
            #we're already at the judge's spot if we had cannons
            self.b_setState('PrepareBattleThree')
        else:
            self.b_setState("RollToBattleThree")
    

    def exitBattleTwo(self):
        assert self.notify.debug('%s.exitBattleTwo()' % (self.doId))        
        self.resetBattles()

        self.numToonJurorsSeated = 0

        for chair in self.chairs:
            self.notify.debug('chair.state==%s' % chair.state)
            if chair.state == 'ToonJuror':
                self.numToonJurorsSeated += 1

        self.notify.debug('numToonJurorsSeated=%d' % self.numToonJurorsSeated)

        #RAU keep track in server log so we can balance later
        self.air.writeServerEvent("jurorsSeated", self.doId, "%s|%s|%s" %
                                  (self.dept,  self.involvedToons,self.numToonJurorsSeated))

        #delete the cannons but keep the chairs around
        self.__deleteCannons()
        #self.__deleteBattleTwoObjects()

        self.__stopChairs()

    ##### RollToBattleThree state #####

    def enterRollToBattleThree(self):
        assert self.notify.debug('%s.enterRollToBattleThree()' % (self.doId))

        # Reshuffle the remaining toons for the second pair of battles.
        self.divideToons()

        # The clients will play a movie showing the boss cog moving up
        # to the top of the area for the phase 2 battle.

        #import pdb; pdb.set_trace()

        self.barrier = self.beginBarrier(
            "RollToBattleThree", self.involvedToons, 20,
            self.__doneRollToBattleThree)

        #import pdb; pdb.set_trace()

    def __doneRollToBattleThree(self, avIds):
        #import pdb; pdb.set_trace()     
        assert(self.notify.debug('%s.__doneRollToBattleThree()' % (self.doId)))        
        self.b_setState("PrepareBattleThree")

    def exitRollToBattleThree(self):
        #import pdb; pdb.set_trace()        
        self.ignoreBarrier(self.barrier)


    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        """
        The clients will focus in on the witness toon giving some
        encouragement and advice.  We wait for the clients to click
        through.
        """
        
        assert self.notify.debug('%s.enterPrepareBattleThree()' % (self.doId))

        #warning the battle difficulty could conceivably change if
        #someone drops out between this state and the BattleThree state
        #this would only matter if you switch from having toon jurors
        #affect your evidence weight to not, or vice versa.  We could take
        #battle diffculty only from this state, but I think it's better
        #that it's recalculated on BattleThree
        self.calcAndSetBattleDifficulty()


        self.barrier = self.beginBarrier(
            "PrepareBattleThree", self.involvedToons, 45,
            self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState("BattleThree")

    def exitPrepareBattleThree(self):
        self.ignoreBarrier(self.barrier)

    ##### BattleThree state #####

    def enterBattleThree(self):
        assert self.notify.debug('%s.enterBattleThree()' % (self.doId))

        self.battleThreeTimeStarted = globalClock.getFrameTime()
        self.calcAndSetBattleDifficulty()

        self.calculateWeightPerToon();

        diffSettings =  ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
        self.ammoCount = diffSettings[0]
        self.numGavels = diffSettings[1]
        if self.numGavels >= len (ToontownGlobals.LawbotBossGavelPosHprs):
            self.numGavels = len(ToontownGlobals.LawbotBossGavelPosHprs) 
        self.numLawyers = diffSettings[2]
        if self.numLawyers >= len (ToontownGlobals.LawbotBossLawyerPosHprs):
            self.numLawyers = len (ToontownGlobals.LawbotBossLawyerPosHprs) 

        self.toonupValue = diffSettings[3]



        self.notify.debug("diffLevel=%d ammoCount=%d gavels=%d lawyers = %d, toonup=%d" %
                          (self.battleDifficulty, self.ammoCount,
                           self.numGavels, self.numLawyers, self.toonupValue)
                          )

        #RAU keep track in server log so we can balance later
        self.air.writeServerEvent("lawbotBossSettings", self.doId, "%s|%s|%s|%s|%s|%s" %
                                  (self.dept,  self.battleDifficulty, self.ammoCount,
                                   self.numGavels, self.numLawyers,
                                   self.toonupValue)
                                  )
        
        

        self.__makeBattleThreeObjects()

        #Make the prosecution lawyers
        self.__makeLawyers()

        self.numPies = self.ammoCount
        
        self.resetBattles()
        self.setPieType()

        jurorsOver = self.numToonJurorsSeated - ToontownGlobals.LawbotBossJurorsForBalancedScale
        #dmgAdjust could be negative if they do badly in battle two
        dmgAdjust = jurorsOver * ToontownGlobals.LawbotBossDamagePerJuror  
        self.b_setBossDamage(ToontownGlobals.LawbotBossInitialDamage + dmgAdjust, 0, 0)
        # make it close to losing if needed
        if simbase.config.GetBool('lawbot-boss-cheat',0):
            pass
            self.b_setBossDamage(ToontownGlobals.LawbotBossMaxDamage - 1, 0, 0)
        
        
        self.battleThreeStart = globalClock.getFrameTime()

        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.__touchedCage = 0

        # lets just play with one for now
        #self.gavels[0].turnOn()
        for aGavel in self.gavels:
            aGavel.turnOn()

        self.waitForNextAttack(5)


        self.notify.debug('battleDifficulty = %d' % self.battleDifficulty)

        self.numToonsAtStart = len(self.involvedToons)

    def getToonDifficulty(self):
        """
        Get the difficulty factor based on just the toons
        """
        
        highestCogSuitLevel = 0
        totalCogSuitLevels = 0.0
        totalNumToons = 0.0
        
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toonLevel = toon.getNumPromotions(self.dept)
                totalCogSuitLevels += toonLevel
                totalNumToons += 1
                if (toon.cogLevels > highestCogSuitLevel):
                    highestCogSuitLevel = toonLevel

        if not totalNumToons:
            totalNumToons = 1.0
        
        averageLevel = totalCogSuitLevels / totalNumToons
        self.notify.debug('toons average level = %f, highest level = %d' % (averageLevel, highestCogSuitLevel))

        #put a cap on it, otherwise we could go as high as 90
        retval = min (averageLevel, self.maxToonLevels)
        return retval

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

    def __makeBattleThreeObjects(self):
        if self.gavels == None:
            # Generate all of the gavels.
            self.gavels = []
            for index in range(self.numGavels):
                gavel= DistributedLawbotBossGavelAI.DistributedLawbotBossGavelAI(self.air, self, index)
                gavel.generateWithRequired(self.zoneId)
                self.gavels.append(gavel)

    def __deleteBattleThreeObjects(self):
        if self.gavels != None:
            for gavel in self.gavels:
                gavel.request('Off')
                gavel.requestDelete()
            self.gavels = None

    def doBattleThreeInfo(self):
        didTheyWin = 0
        if self.bossDamage == ToontownGlobals.LawbotBossMaxDamage:
            didTheyWin = 1

        self.battleThreeTimeInMin = globalClock.getFrameTime() - self.battleThreeTimeStarted
        self.battleThreeTimeInMin /= 60.0
            

        self.numToonsAtEnd = 0;
        toonHps = []
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                self.numToonsAtEnd += 1
                toonHps.append (toon.hp)
            
        
        self.air.writeServerEvent(
            "b3Info", self.doId,
            "%d|%.2f|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%s|%s" %
            (didTheyWin,
             self.battleThreeTimeInMin,
             self.numToonsAtStart,
             self.numToonsAtEnd,
             self.numToonJurorsSeated,
             self.battleDifficulty,
             self.ammoCount,
             self.numGavels,
             self.numLawyers,
             self.toonupValue,
             self.numBonusStates,
             self.numAreaAttacks,
             toonHps,
             self.weightPerToon
             )
            )

    def exitBattleThree(self):
        self.doBattleThreeInfo()
        
        self.stopAttacks()
        self.stopStrafes()
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        self.__resetLawyers()

        self.__deleteBattleThreeObjects()
        #if self.gavels != None:
        #    for gavel in self.gavels:
        #        gavel.request('Off')
                


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

        
        # Don't forget to give the toon the cog summon reward and the
        # promotion!
        preferredDept = random.randrange(len(SuitDNA.suitDepts))
        typeWeights = ['single']   * 70 + \
                      ['building'] * 27 + \
                      ['invasion'] * 3
        preferredSummonType = random.choice(typeWeights)          
        
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                self.giveCogSummonReward(toon, preferredDept, preferredSummonType)
                toon.b_promote(self.deptIndex)
                
    def giveCogSummonReward(self, toon, prefDeptIndex, prefSummonType):
        """
        Try to make sure we don't give a duplicate reward to a toon.
        If all else fails give a totally random one
        """

        #we could also make cogLevel random
        cogLevel = int (  self.toonLevels / self.maxToonLevels * SuitDNA.suitsPerDept)
        cogLevel = min (cogLevel, SuitDNA.suitsPerDept -1) #at cap we can get an invalid cogLevel
        deptIndex = prefDeptIndex
        summonType = prefSummonType


        hasSummon = toon.hasParticularCogSummons(prefDeptIndex, cogLevel, prefSummonType)
        if (hasSummon):
            #lets find another reward he can use
            self.notify.debug('trying to find another reward')
            if not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'single'):
                summonType = 'single'
            elif not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'building'):
                summonType = 'building'
            elif not toon.hasParticularCogSummons(prefDeptIndex, cogLevel, 'invasion'):
                summonType = 'invasion'
            else:
                #varying the summon type didn't work
                foundOne = False
                for curDeptIndex in range (len (SuitDNA.suitDepts)):
                    if not toon.hasParticularCogSummons(curDeptIndex, cogLevel, prefSummonType):
                        deptIndex = curDeptIndex
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'single'):
                        deptIndex = curDeptIndex
                        summonType = 'single'
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'building'):
                        deptIndex = curDeptIndex
                        summonType = 'building'
                        foundOne = True
                        break
                    elif not toon.hasParticularCogSummons(curDeptIndex, cogLevel, 'invasion'):
                        summonType = 'invasion'
                        deptIndex = curDeptIndex
                        foundOne = True
                        break

                possibleCogLevel = range(SuitDNA.suitsPerDept)
                possibleDeptIndex = range (len(SuitDNA.suitDepts))
                possibleSummonType = ['single','building','invasion']

                typeWeights = ['single']   * 70 + \
                              ['building'] * 27 + \
                              ['invasion'] * 3
        
                #lets try a random search 5 times
                if not foundOne:
                    for i in range(5):
                        randomCogLevel = random.choice(possibleCogLevel)
                        randomSummonType = random.choice(typeWeights)
                        randomDeptIndex = random.choice (possibleDeptIndex)
                        if not toon.hasParticularCogSummons(randomDeptIndex,
                                                            randomCogLevel,
                                                            randomSummonType):
                            foundOne = True
                            cogLevel = randomCogLevel
                            summonType = randomSummonType
                            deptIndex = randomDeptIndex
                            assert(self.notify.debug('found on random try %d' % i))
                            break

                #exhaustively search through everything and try to find one
                for curType in possibleSummonType:
                    if foundOne:
                        break
                    for curCogLevel in possibleCogLevel:
                        if foundOne:
                            break
                        for curDeptIndex in possibleDeptIndex:
                            if foundOne:
                                break
                            if not toon.hasParticularCogSummons(curDeptIndex,
                                                                curCogLevel,
                                                                curType):
                                foundOne = True
                                cogLevel = curCogLevel
                                summonType = curType
                                deptIndex = curDeptIndex
                                assert(self.notify.debug('found on exhaustive search'))
                                
                
                
                if not foundOne:
                    #totally give up, make it random
                    cogLevel = None
                    summonType = None
                    deptIndex = None
                    assert ( self.notify.debug("couldn't find a good reward") )
                else:
                    assert ( self.notify.debug('reward cogLevel=%d deptIndex=%d summonType=%s' %                                      (cogLevel, deptIndex, summonType)))
                    pass
                
                
                    

        
        toon.assignNewCogSummons(cogLevel, summonType, deptIndex)

    def exitVictory(self):
        self.takeAwayPies()

    ##### Defeat state #####

    def enterDefeat(self):
        assert self.notify.debug('%s.enterDefeat()' % (self.doId))
        self.resetBattles()

        self.barrier = self.beginBarrier(
            "Defeat", self.involvedToons, 10,
            self.__doneDefeat)

    def __doneDefeat(self, avIds):

        #hmmm, just set their health to zero?
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                toon.b_setHp(0)

    def exitDefeat(self):
        self.takeAwayPies()



    ##### Frolic state #####

    def enterFrolic(self):
        DistributedBossCogAI.DistributedBossCogAI.enterFrolic(self)
        self.b_setBossDamage(0, 0, 0)


    def setPieType(self):
        # Sets everyone's pie type for the battle.
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                # a pie type of 7 should indicate that it should switch to the evidence button
                
                toon.d_setPieType(ToontownBattleGlobals.MAX_TRACK_INDEX + 1)

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
        #this doesn't look good
        #self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)

        #import pdb; pdb.set_trace()
        #toonId = self.involvedToons[0]        
        #self.b_setAttackCode(ToontownGlobals.BossCogDirectedAttack, toonId)        
        
            
        
    def __resetLawyers(self):
        # Free the suits made with an earlier call to __makeLawyers().
        for suit in self.lawyers:
            #suit.boss = None
            suit.requestDelete()
        self.lawyers = []

    def __makeLawyers(self):
        """
        # Generate a handful of suits that we can see the Boss Cog
        # promoting as we come in.  These shouldn't really need to be
        # true DistributedSuits, but I tried to make just a Suit by
        # itself and it just doesn't work.  It doesn't do any real
        # harm to make DistributedSuits, anyway.
        """

        self.__resetLawyers()

        #bottom feeder is body type c. and throw-paper anim is not included in ttmodels/built
        lawCogChoices = [ "b", "dt", "ac", "bs", "sd", "le", "bw"]

        # 8 suits, 4 on each side.
        for i in range(self.numLawyers): 
            suit = DistributedLawbotBossSuitAI.DistributedLawbotBossSuitAI(self.air, None)            

            # And a random suit type
            suit.dna = SuitDNA.SuitDNA()
            lawCog = random.choice(lawCogChoices)
            suit.dna.newSuit(lawCog)

            suit.setPosHpr( *ToontownGlobals.LawbotBossLawyerPosHprs[i])
            suit.setBoss(self)

            suit.generateWithRequired(self.zoneId)
            self.lawyers.append(suit)

        self.__sendLawyerIds()


    def hitChair(self, chairIndex, npcToonIndex):
        """
        This is sent when the client successfully hits one of the juror chairs from a cannon
        battle three.  We have to take the client's word for it here.
        """
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitChair(%s, %s)' % (self.doId, avId, chairIndex))

        if not self.validate(avId, avId in self.involvedToons,
                             'hitChair from unknown avatar'):
            return

        if not self.chairs:
            #potentially a late hit, just ignore
            return

        if chairIndex <0 or chairIndex >= len(self.chairs):
            self.notify.warning('invalid chairIndex = %d' % chairIndex)
            return

        if not self.state == 'BattleTwo':
            #a late hit, just ignore
            return

        self.chairs[chairIndex].b_setToonJurorIndex(npcToonIndex)
        self.chairs[chairIndex].requestToonJuror()

    def clearBonus(self, taskName):
        if self and hasattr(self,'bonusState'):
            self.bonusState = False

    def startBonusState(self):
        self.notify.debug('startBonusState')
        self.bonusTimeStarted = globalClock.getFrameTime()
        self.bonusState = True
        self.numBonusStates += 1
        #heal the toons
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                self.healToon(toon, ToontownGlobals.LawbotBossBonusToonup)

        #clear it after a certain amount of time
        taskMgr.doMethodLater(ToontownGlobals.LawbotBossBonusDuration , self.clearBonus,self.uniqueName('clearBonus'))

        self.sendUpdate('enteredBonusState',[])

    def areAllLawyersStunned(self):
        for lawyer in self.lawyers:
            if not lawyer.stunned:
                return False
        return True
            
        
    def checkForBonusState(self):
        """
        Whenever a lawyer gets stunned, see if we enter the bonus state
        """
        if self.bonusState:
            #if we're already in the bonus state, do nothing
            return

        if not self.areAllLawyersStunned():
            return

        curTime = globalClock.getFrameTime() 
        delta = curTime - self.bonusTimeStarted;

        if  ToontownGlobals.LawbotBossBonusWaitTime < delta:
            self.startBonusState()

    def toonEnteredCannon(self, toonId, cannonIndex):
        """
        Gets called from DistributedLawbotCannonAI, keep track which
        cannon a toon entered
        """
        self.cannonIndexPerToon[toonId] = cannonIndex        
        pass

    def numJurorsSeatedByCannon( self, cannonIndex):
        """
        how many jurors were seated by a certain cannon
        """
        retVal = 0
        for chair in self.chairs:
            if chair.state == "ToonJuror":
                if chair.toonJurorIndex == cannonIndex:
                    retVal +=1
        return retVal
                
                

    def calculateWeightPerToon(self):
        """
        calculate evidence weight each toon throws, Warning this code
        is duplicated on the client side, update that too if we change this.
        """
        for toonId in self.involvedToons:
            defaultWeight = 1
            bonusWeight = 0
            cannonIndex = self.cannonIndexPerToon.get(toonId)
            if not cannonIndex == None:
                diffSettings =  ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
                if diffSettings[4]:                    
                    bonusWeight = self.numJurorsSeatedByCannon( cannonIndex) - diffSettings[5]
                    if bonusWeight < 0:
                        bonusWeight = 0 


            newWeight = defaultWeight + bonusWeight
            self.weightPerToon[toonId] = newWeight
            self.notify.debug('toon %d has weight of %d' % (toonId, newWeight))


    def b_setBattleDifficulty(self, batDiff):
        self.setBattleDifficulty(batDiff)
        self.d_setBattleDifficulty(batDiff)

    def setBattleDifficulty(self, batDiff):
        self.battleDifficulty = batDiff

    def d_setBattleDifficulty(self, batDiff):
        self.sendUpdate('setBattleDifficulty', [batDiff])

    def calcAndSetBattleDifficulty(self):
        self.toonLevels = self.getToonDifficulty()
        numDifficultyLevels = len(ToontownGlobals.LawbotBossDifficultySettings)
        battleDifficulty = int (  self.toonLevels / self.maxToonLevels * numDifficultyLevels)

        if battleDifficulty >= numDifficultyLevels:
            battleDifficulty = numDifficultyLevels -1

        self.b_setBattleDifficulty(battleDifficulty)
        
