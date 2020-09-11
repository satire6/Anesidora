import random
import math
from pandac.PandaModules import Point3
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.interval.IntervalGlobal import LerpPosInterval
from toontown.coghq import DistributedFoodBeltAI
from toontown.coghq import DistributedBanquetTableAI
from toontown.coghq import DistributedGolfSpotAI
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.suit import DistributedBossCogAI
from toontown.suit import DistributedSuitAI
from toontown.suit import SuitDNA
from toontown.building import SuitBuildingGlobals
from toontown.battle import DistributedBattleWaitersAI
from toontown.battle import DistributedBattleDinersAI
from toontown.battle import BattleExperienceAI
from direct.distributed.ClockDelta import globalClockDelta

class DistributedBossbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossbotBossAI')

    #the cap we use for the toon level difficulty
    maxToonLevels = 77
    toonUpLevels = [1,2,3,4]
    
    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 'c')
        FSM.FSM.__init__(self, 'DistributedBossbotBossAI')
        self.battleOneBattlesMade = False
        self.battleThreeBattlesMade = False
        self.battleFourSetup = False
        self.foodBelts = []
        self.numTables =1
        self.numDinersPerTable = 3
        self.tables = []
        self.numGolfSpots =4
        self.golfSpots = []
        # keep track if the toons are carrying food or not
        self.toonFoodStatus = {}
        self.bossMaxDamage = ToontownGlobals.BossbotBossMaxDamage
        self.threatDict = {}
        self.keyStates.append('BattleFour')
        self.battleFourStart = 0
        self.battleDifficulty = 0 #how difficult is battle four

        self.movingToTable = False
        self.tableDest = -1
        self.curTable = -1

        self.speedDamage = 0
        self.maxSpeedDamage = ToontownGlobals.BossbotMaxSpeedDamage
        self.speedRecoverRate = ToontownGlobals.BossbotSpeedRecoverRate
        self.speedRecoverStartTime = 0

        self.battleFourTimeStarted = 0
        self.numDinersExploded = 0

        # for tracking purposes
        self.numMoveAttacks = 0
        self.numGolfAttacks = 0
        self.numGearAttacks = 0
        self.numGolfAreaAttacks = 0
        self.numToonupGranted = 0
        self.totalLaffHealed = 0

        self.toonupsGranted = []

        self.doneOvertimeOneAttack = False
        self.doneOvertimeTwoAttack = False

        # what time will he destroy one food belt
        self.overtimeOneTime = simbase.air.config.GetInt('overtime-one-time',1200)
        # what time will he destroy the second food belt
        self.battleFourDuration = simbase.air.config.GetInt('battle-four-duration',1800)
        self.overtimeOneStart = float(self.overtimeOneTime) / self.battleFourDuration

        self.moveAttackAllowed = True

    def delete(self):
        self.notify.debug('DistributedBossbotBossAI.delete')
        self.deleteBanquetTables()
        self.deleteFoodBelts()
        self.deleteGolfSpots()
        return DistributedBossCogAI.DistributedBossCogAI.delete(self)
        
    def enterElevator(self):
        """Handle entering the elevator state."""
        DistributedBossCogAI.DistributedBossCogAI.enterElevator(self)
        # we must make the battle now, since the suits will be immediately seen
        self.makeBattleOneBattles()

    def enterIntroduction(self):
        """Handle enterint the introduction state.
        Copied and pasted to just avoid the call to reset battles.
        """
        # Also get the battle objects ready.
        self.arenaSide = None
        self.makeBattleOneBattles()

        # The clients will play a cutscene.  When they are done
        # watching the movie, we continue.

        self.barrier = self.beginBarrier(
            "Introduction", self.involvedToons, 45,
            self.doneIntroduction)
        
    def makeBattleOneBattles(self):
        """Create the DistributedBattleWaiters."""
        if not self.battleOneBattlesMade:
            self.postBattleState = 'PrepareBattleTwo'
            self.initializeBattles(1, ToontownGlobals.BossbotBossBattleOnePosHpr)
            self.battleOneBattlesMade = True

    def getHoodId(self):
        """Return our canonical hood id."""
        #return ToontownGlobals.BossbotHQ
        return ToontownGlobals.LawbotHQ

    def generateSuits(self, battleNumber):
        """Create and generate the suits for a battle phase."""
        if battleNumber == 1:
            # Battle 1
            # building difficulty 14, first battle with Bossbot Boss. These
            # are normal cogs.
            weakenedValue = ( ( 1, 1 ),
                              ( 2, 2 ),
                              ( 2, 2 ),
                              ( 1, 1 ),
                              ( 1, 1, 1, 1, 1 ) )
            listVersion = list(SuitBuildingGlobals.SuitBuildingInfo)

            if simbase.config.GetBool('bossbot-boss-cheat',0):
                listVersion[14] = weakenedValue
                SuitBuildingGlobals.SuitBuildingInfo = tuple(listVersion)
            retval =  self.invokeSuitPlanner(14, 0)
            return retval;
        else:
            suits = self.generateDinerSuits()
            return suits

    def invokeSuitPlanner(self, buildingCode, skelecog):
        "Call the base clase suit planner, but force 4 active suits at start."""
        suits = DistributedBossCogAI.\
                DistributedBossCogAI.invokeSuitPlanner(self,
                                                       buildingCode,
                                                       skelecog)
        activeSuits = suits['activeSuits'][:]
        reserveSuits = suits['reserveSuits'][:]
        if len(activeSuits) + len(reserveSuits) >= 4:
            while len(activeSuits) < 4:
                activeSuits.append( reserveSuits.pop()[0])
        retval = { 'activeSuits': activeSuits,
                   'reserveSuits': reserveSuits
                   }
        return retval
        
    def makeBattle(self, bossCogPosHpr, battlePosHpr,
                   roundCallback, finishCallback, battleNumber, battleSide):
        """Create and generate one DistributedBattleWaiters."""
        if battleNumber == 1:
            battle = DistributedBattleWaitersAI.DistributedBattleWaitersAI(
                self.air, self, roundCallback, finishCallback, battleSide)
        else:
            battle = DistributedBattleDinersAI.DistributedBattleDinersAI(
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

        # lets add the initial 4 suits already
        activeSuits = self.activeSuitsA
        if battleSide:
            activeSuits = self.activeSuitsB
        for suit in activeSuits:
            battle.addSuit(suit)
        
        battle.generateWithRequired(self.zoneId)
        return battle

    def initializeBattles(self, battleNumber, bossCogPosHpr):
        """Set up the pair of battle objects for the BattleOne or BattleThree phase."""
        self.resetBattles()
        
        if not self.involvedToons:
            self.notify.warning("initializeBattles: no toons!")
            return

        self.battleNumber = battleNumber
        suitHandles = self.generateSuits(battleNumber)
        self.suitsA = suitHandles['activeSuits']
        self.activeSuitsA = self.suitsA[:]
        self.reserveSuits = suitHandles['reserveSuits']

        if battleNumber == 3:
            if self.toonsB:
                # move one of the suits in A to B
                movedSuit = self.suitsA.pop()
                self.suitsB = [movedSuit]
                self.activeSuitsB = [movedSuit]
                self.activeSuitsA.remove(movedSuit)
            else:
                self.suitsB = []
                self.activeSuitsB = []
        else:
            suitHandles = self.generateSuits(battleNumber)
            self.suitsB = suitHandles['activeSuits']
            self.activeSuitsB = self.suitsB[:]
            self.reserveSuits += suitHandles['reserveSuits']

        if self.toonsA:
            if battleNumber == 1:
                self.battleA = self.makeBattle(
                    bossCogPosHpr, ToontownGlobals.WaiterBattleAPosHpr,
                    self.handleRoundADone, self.handleBattleADone,
                    battleNumber, 0)
                self.battleAId = self.battleA.doId
            else:
                self.battleA = self.makeBattle(
                    bossCogPosHpr, ToontownGlobals.DinerBattleAPosHpr,
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
            if battleNumber == 1:
                self.battleB = self.makeBattle(
                    bossCogPosHpr, ToontownGlobals.WaiterBattleBPosHpr,
                    self.handleRoundBDone, self.handleBattleBDone,
                    battleNumber, 1)
                self.battleBId = self.battleB.doId
            else:
                self.battleB = self.makeBattle(
                    bossCogPosHpr, ToontownGlobals.DinerBattleBPosHpr,
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

    ##### PrepareBattleTwo state #####
    def enterPrepareBattleTwo(self):
        """Handle entering the Prepare Battle Two State."""
        assert self.notify.debug('%s.enterPrepareBattleTwo()' % (self.doId))

        # The Clients will see the toons donning waiter disguise.
        # CEO will make brief appearing demanding food.
        # Mata Hairy says give them food till they explode.
        # Walk toons through door
        # Close door

        self.barrier = self.beginBarrier(
            "PrepareBattleTwo", self.involvedToons, 45,
            self.__donePrepareBattleTwo)
        
        #TODO setup the cogs sitting in the tables
        #conveyer belts with food too
        self.createFoodBelts()
        self.createBanquetTables()

    def __donePrepareBattleTwo(self, avIds):
        """Force a transition to the next state once the barrier is done."""
        self.b_setState("BattleTwo")

    def exitPrepareBattleTwo(self):
        """Handle exiting the Prepare Battle Two State."""
        self.ignoreBarrier(self.barrier)

    def createFoodBelts(self):
        """Create the conveyer belts that bring the food out."""
        if self.foodBelts:
            # using ~bossBattle, don't make them twice
            return
        for i in xrange(2):
            newBelt = DistributedFoodBeltAI.DistributedFoodBeltAI(self.air, self, i)
            self.foodBelts.append(newBelt)
            newBelt.generateWithRequired(self.zoneId)

    def deleteFoodBelts(self):
        """Delete the food belts we've created."""
        for belt in self.foodBelts:
            belt.requestDelete()
        self.foodBelts = []

    def createBanquetTables(self):
        """Create the conveyer belts that bring the food out."""
        if self.tables:
            # using ~bossBattle, don't make them twice
            return
        self.calcAndSetBattleDifficulty()
        diffInfo =  ToontownGlobals.BossbotBossDifficultySettings[self.battleDifficulty]
        self.diffInfo = diffInfo
        self.numTables =diffInfo[0]
        self.numDinersPerTable = diffInfo[1]
        dinerLevel = diffInfo[2]
        #self.numTables =2
        #self.numDinersPerTable = 8
        for i in xrange(self.numTables):
            newTable = DistributedBanquetTableAI.DistributedBanquetTableAI(
                self.air, self, i, self.numDinersPerTable, dinerLevel)
            self.tables.append(newTable)
            newTable.generateWithRequired(self.zoneId)

    def deleteBanquetTables(self):
        """Delete the banquet tables we've created."""
        for table in self.tables:
            table.requestDelete()
        self.tables = []
                

    ##### BattleTwo state #####
    def enterBattleTwo(self):
        """Handle entering the Battle Two State."""
        assert self.notify.debug('%s.enterPrepareBattleTwo()' % (self.doId))
        self.resetBattles()
        self.createFoodBelts()
        self.createBanquetTables()
        for belt in self.foodBelts:
            belt.turnOn()
        for table in self.tables:
            table.turnOn()
        self.barrier = self.beginBarrier(
            "BattleTwo",
            self.involvedToons,
            ToontownGlobals.BossbotBossServingDuration + 1,
            self.__doneBattleTwo)            

    def exitBattleTwo(self):
        """Handle exiting the Battle Two State."""
        self.ignoreBarrier(self.barrier)
        for table in self.tables:
            table.goInactive()
        for belt in self.foodBelts:
            belt.goInactive()
        pass

    def __doneBattleTwo(self, avIds):
        """Go to the next state."""
        assert(self.notify.debug('%s.__doneBattleTwo' % (self.doId)))        
        self.b_setState('PrepareBattleThree')


    def requestGetFood(self, beltIndex, foodIndex, foodNum):
        """Handle a toon requesting to get food from the conveyer belts."""
        grantRequest = False
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'BattleTwo':
            grantRequest = False
        elif not (beltIndex, foodNum) in self.toonFoodStatus.values():
            # no one else is carrying it, make sure the toon isn't carrying anything
            if not avId in self.toonFoodStatus:
                grantRequest = True
            elif self.toonFoodStatus[avId] == None:
                grantRequest = True
            
        if grantRequest:
            self.toonFoodStatus[avId] = (beltIndex, foodNum)
            self.sendUpdate('toonGotFood', [avId, beltIndex, foodIndex, foodNum])

    def requestServeFood(self, tableIndex, chairIndex):
        """Handle a toon requesting to get food from the conveyer belts."""
        grantRequest = False
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'BattleTwo':
            grantRequest = False        
        elif tableIndex < len( self.tables):
            table = self.tables[tableIndex]
            dinerStatus = table.getDinerStatus(chairIndex)
            if dinerStatus in ( table.HUNGRY, table.ANGRY):
                if self.toonFoodStatus[avId]:
                    grantRequest = True
            
        if grantRequest:
            self.toonFoodStatus[avId] = None
            table.foodServed(chairIndex)
            self.sendUpdate('toonServeFood', [avId, tableIndex, chairIndex])

    ##### PrepareBattleThree state #####            
    def enterPrepareBattleThree(self):
        """Handle entering the Battle Three State."""
        self.barrier = self.beginBarrier(
            "PrepareBattleThree",
            self.involvedToons,
            ToontownGlobals.BossbotBossServingDuration + 1,
            self.__donePrepareBattleThree)
        
        self.divideToons()                
        self.makeBattleThreeBattles()

    def exitPrepareBattleThree(self):
        """Handle exiting the Prepare Battle Three State."""
        self.ignoreBarrier(self.barrier)
        pass    

    def __donePrepareBattleThree(self, avIds):
        """Go to the next state."""
        assert(self.notify.debug('%s.__doneBattleThree' % (self.doId)))
        self.b_setState('BattleThree')

    def makeBattleThreeBattles(self):
        if not self.battleThreeBattlesMade:
            # we need tables for battle three
            if not self.tables:
                self.createBanquetTables()
                for table in self.tables:
                    table.turnOn()
                    table.goInactive()            
            notDeadList = []
            for table in self.tables:
                tableInfo = table.getNotDeadInfo()
                notDeadList += tableInfo
            self.notDeadList = notDeadList
            self.postBattleState = 'PrepareBattleFour'
            self.initializeBattles(3, ToontownGlobals.BossbotBossBattleThreePosHpr)
            self.battleThreeBattlesMade = True



    def generateDinerSuits(self):
        """Generate the diners that fight."""
        diners = []
        for i in xrange(len(self.notDeadList)):
            if simbase.config.GetBool('bossbot-boss-cheat',0):
                suit = self.__genSuitObject(self.zoneId, 2, 'c', 2, 0)
            else:
                info = self.notDeadList[i]
                suitType = info[2] - 4
                suitLevel = info[2]
                suit = self.__genSuitObject(self.zoneId, suitType, 'c', suitLevel, 1)
            diners.append((suit, 100))
        active = []
        # we make 2 more than the suits left        
        for i in xrange(2):
            if simbase.config.GetBool('bossbot-boss-cheat',0):
                suit = self.__genSuitObject(self.zoneId, 2, 'c', 2, 0)
            else:
                # BAND-AID: notDeadList might be empty?
                suitType = 8
                suitLevel = 12
                suit = self.__genSuitObject(self.zoneId, suitType, 'c', suitLevel, 1)            
            active.append(suit)
        return {'activeSuits': active,
                'reserveSuits': diners
                }

    def __genSuitObject(self, suitZone, suitType, bldgTrack, suitLevel, revives = 0):
        """
        // Function:   generate a distributed suit object
        // Parameters:
        // Changes:
        // Returns:    the suit object created
        """
        newSuit = DistributedSuitAI.DistributedSuitAI( simbase.air, None )
        skel = self.__setupSuitInfo( newSuit, bldgTrack, suitLevel, suitType )
        if skel:
            newSuit.setSkelecog(1)
        newSuit.setSkeleRevives(revives)
        newSuit.generateWithRequired( suitZone )

        # Fill in the name so we can tell one suit from another in printouts.
        newSuit.node().setName('suit-%s' % (newSuit.doId))
        return newSuit

    def __setupSuitInfo( self, suit, bldgTrack, suitLevel, suitType ):
        """
        create dna information for the given suit with the given track
        and suit type
        """
        
        dna = SuitDNA.SuitDNA()
        dna.newSuitRandom( suitType, bldgTrack )
        suit.dna = dna
        self.notify.debug("Creating suit type " + suit.dna.name +
                          " of level " + str( suitLevel ) +
                          " from type " + str( suitType ) +
                          " and track " + str( bldgTrack ) )
        suit.setLevel( suitLevel )

        # We can't make a suit a skeleton until after generate.
        # Pass this info back so we know whether to do it or not
        return False
    
    ##### BattleThree state #####  
    def enterBattleThree(self):
        """Handle entering the Battle Three State."""
        self.makeBattleThreeBattles()
        self.notify.debug('self.battleA = %s' % self.battleA)
        # Begin the battles.
        if self.battleA:
            self.battleA.startBattle(self.toonsA, self.suitsA)
        if self.battleB:
            self.battleB.startBattle(self.toonsB, self.suitsB)

    def exitBattleThree(self):
        """Handle exiting the Prepare Battle Three State."""
        self.resetBattles()
        pass

    ##### PrepareBattleFour state #####
    def enterPrepareBattleFour(self):
        """Handle entering the Prepare Battle Four State."""
        self.resetBattles()
        assert self.notify.debug('%s.enterPrepareBattleFour()' % (self.doId))
        self.setupBattleFourObjects()
        # The Clients will see the CEO doing a speech
        self.barrier = self.beginBarrier(
            "PrepareBattleFour", self.involvedToons, 45,
            self.__donePrepareBattleFour)

    def __donePrepareBattleFour(self, avIds):
        """Force a transition to the next state once the barrier is done."""
        self.b_setState("BattleFour")

    def exitPrepareBattleFour(self):
        """Handle exiting the Prepare Battle Four State."""
        self.ignoreBarrier(self.barrier)


    ##### BattleFour state #####  
    def enterBattleFour(self):
        """Handle entering the Battle Four State."""
        self.battleFourTimeStarted = globalClock.getFrameTime()
        self.numToonsAtStart = len(self.involvedToons)
        self.resetBattles()
        assert self.notify.debug('%s.enterBattleFour()' % (self.doId))
        self.setupBattleFourObjects()
        self.battleFourStart = globalClock.getFrameTime()
        self.waitForNextAttack(5)
        pass
    
    def exitBattleFour(self):
        """Handle exiting the Prepare Battle Four State."""
        self.recordCeoInfo()
        for belt in self.foodBelts:
            belt.goInactive()
        
        pass

    def recordCeoInfo(self):
        """Record info to the server log so we can tune the battle."""
        didTheyWin = 0
        if self.bossDamage == self.bossMaxDamage:
            didTheyWin =1
        self.battleFourTimeInMin = globalClock.getFrameTime() - self.battleFourTimeStarted
        self.battleFourTimeInMin /= 60.0
        self.numToonsAtEnd = 0;
        toonHps = []
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                self.numToonsAtEnd += 1
                toonHps.append (toon.hp)
        self.air.writeServerEvent(
            "ceoInfo", self.doId,
            "%d|%.2f|%d|%d|%d|%d|%d|%d|%s|%s|%.1f|%d|%d|%d|%d|%d}%d|%s|" %
            (didTheyWin,
             self.battleFourTimeInMin,
             self.battleDifficulty,
             self.numToonsAtStart,
             self.numToonsAtEnd,
             self.numTables,
             self.numTables * self.numDinersPerTable,
             self.numDinersExploded,
             toonHps,
             self.involvedToons,
             self.speedDamage,
             self.numMoveAttacks,
             self.numGolfAttacks,
             self.numGearAttacks,
             self.numGolfAreaAttacks,
             self.numToonupGranted,
             self.totalLaffHealed,
             "ceoBugfixes"
             )
            )
             

    def setupBattleFourObjects(self):
        """Setup the AI objects for battle four."""
        if self.battleFourSetup:
            return
        if not self.tables:
            self.createBanquetTables()
            #for table in self.tables:
            #    table.turnOn()
            #    table.goInactive()                        
        for table in self.tables:
            table.goFree()
        if not self.golfSpots:
            self.createGolfSpots()
        self.createFoodBelts()
        for belt in self.foodBelts:
            belt.goToonup()
        self.battleFourSetup = True


    def hitBoss(self, bossDamage):
        """Handle a client telling us he hit the boss.
        
        # This is sent when the client successfully hits the boss during
        # battle three.  We have to take the client's word for it here.
        """
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
        self.validate(avId, bossDamage <= 3,
                      'invalid bossDamage %s' % (bossDamage))
        if bossDamage < 1:
            return

        currState = self.getCurrentOrNextState()
        if currState != 'BattleFour':
            # This was just a late hit; ignore it.
            return

        # increase the damage from tuning
        bossDamage *= 2
        
        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)

        if self.bossDamage >= self.bossMaxDamage:
            # Only set this state locally--the clients will go there
            # by themselves when the boss movie finishes playing out.
            self.b_setState('Victory')

        else:
            self.__recordHit(bossDamage)


    def __recordHit(self, bossDamage):
        """Record that the boss got hit."""
        # Records that the boss has been hit, and counts the number of
        # hits in a period of time.
        now = globalClock.getFrameTime()

        self.hitCount += 1
        #if (self.hitCount < self.limitHitCount or self.bossDamage < self.hitCountDamage):
        #    assert self.notify.debug("%s. %s hits, ignoring." % (self.doId, self.hitCount))
        #    return

        assert self.notify.debug("%s. %s hits!" % (self.doId, self.hitCount))

        # Launch an immediate front attack.
        #self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)
        avId = self.air.getAvatarIdFromSender()
        self.addThreat(avId, bossDamage)

    def getBossDamage(self):
        """Return the current boss damage."""
        return self.bossDamage
 
    def b_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        """Set the damage on the AI and on the clients."""
        self.d_setBossDamage(bossDamage, recoverRate, recoverStartTime)
        self.setBossDamage(bossDamage, recoverRate, recoverStartTime)

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        """Set the boss damage on the AI."""
        assert self.notify.debug('%s.setBossDamage(%s, %s)' % (self.doId, bossDamage, recoverRate))
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        """Tell clients of the boss damage."""
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])


    def getSpeedDamage(self):
        """Return the current  speedDamage as an int."""
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime

        self.notify.debug('elapsed=%s' % elapsed)
        # It is important that we consistently represent bossDamage as
        # an integer value, so there is never any chance of client and
        # AI disagreeing about whether bossDamage < bossMaxDamage.
        floatSpeedDamage = max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0 , 0)
        self.notify.debug('floatSpeedDamage = %s' % floatSpeedDamage)
        return int(max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0 , 0))
    
    def getFloatSpeedDamage(self):    
        """Return the current speedDamage as a float."""
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime

        # It is important that we consistently represent bossDamage as
        # an integer value, so there is never any chance of client and
        # AI disagreeing about whether bossDamage < bossMaxDamage.
        floatSpeedDamage = max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0 , 0)
        self.notify.debug('floatSpeedDamage = %s' % floatSpeedDamage)
        return max(self.speedDamage - self.speedRecoverRate * elapsed / 60.0 , 0)
        
 
    def b_setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        """Set the damage on the AI and on the clients."""
        self.d_setSpeedDamage(speedDamage, recoverRate, recoverStartTime)
        self.setSpeedDamage(speedDamage, recoverRate, recoverStartTime)

    def setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        """Set the speed damage on the AI."""
        assert self.notify.debug('%s.setSpeedDamage(%s, %s)' % (self.doId, speedDamage, recoverRate))
        self.speedDamage = speedDamage
        self.speedRecoverRate = recoverRate
        self.speedRecoverStartTime = recoverStartTime

    def d_setSpeedDamage(self, speedDamage, recoverRate, recoverStartTime):
        """Tell clients of the speed damage."""
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setSpeedDamage', [speedDamage, recoverRate, timestamp])        

    def createGolfSpots(self):
        """Create the golf spots for phase four of the boss battle."""
        if self.golfSpots:
            # using ~bossBattle, don't make them twice
            return
        for i in xrange(self.numGolfSpots):
            newGolfSpot = DistributedGolfSpotAI.DistributedGolfSpotAI(
                self.air, self, i)
            self.golfSpots.append(newGolfSpot)
            newGolfSpot.generateWithRequired(self.zoneId)
            newGolfSpot.forceFree()

    def deleteGolfSpots(self):
        """Delete the golf spots we've created."""
        for spot in self.golfSpots:
            spot.requestDelete()
        self.golfSpots = []


    def ballHitBoss(self, speedDamage):
        """Handle a client telling us he hit the boss with the golf ball
        
        # This is sent when the client successfully hits the boss during
        # battle four.  We have to take the client's word for it here.
        """
        avId = self.air.getAvatarIdFromSender()
        assert self.notify.debug('%s.hitBoss(%s, %s)' % (self.doId, avId, speedDamage))

        if not self.validate(avId, avId in self.involvedToons,
                             'hitBoss from unknown avatar'):
            return

        if speedDamage < 1:
            return

        currState = self.getCurrentOrNextState()
        if currState != 'BattleFour':
            # This was just a late hit; ignore it.
            return
        
        now = globalClock.getFrameTime()
        newDamage = self.getSpeedDamage() + speedDamage
        self.notify.debug('newDamage = %s' % newDamage)
        speedDamage = min(self.getFloatSpeedDamage() + speedDamage, self.maxSpeedDamage)
        #speedDamage = int(speedDamage)
        self.b_setSpeedDamage(speedDamage, self.speedRecoverRate, now)
        self.addThreat(avId, 0.1)
        #self.__recordHit()
        

    ##### Victory state #####

    def enterVictory(self):
        assert self.notify.debug('%s.enterVictory()' % (self.doId))
        self.resetBattles()

        for table in self.tables:
            table.turnOff()
        for golfSpot in self.golfSpots:
            golfSpot.turnOff()
            
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

        # Don't forget to give the toon the pink slip reward and the
        # promotion!
       
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                self.givePinkSlipReward(toon)
                toon.b_promote(self.deptIndex)
                
    def givePinkSlipReward(self, toon):
        """Give a pink slip reward to the toon."""
        self.notify.debug("TODO give pink slip to %s" % toon)
        toon.addPinkSlips(self.battleDifficulty +1)
        pass

    def getThreat(self, toonId):
        """Return the threat level of the toon."""
        if toonId in self.threatDict:
            return self.threatDict[toonId]
        else:
            return 0

    def addThreat(self, toonId, threat):
        """Increase the threat level of the toon."""
        if toonId in self.threatDict:
            self.threatDict[toonId] += threat
        else:
            self.threatDict[toonId] = threat

    def subtractThreat(self, toonId, threat):
        """Increase the threat level of the toon."""
        if toonId in self.threatDict:
            self.threatDict[toonId] -= threat            
        else:
            self.threatDict[toonId] = 0
        if self.threatDict[toonId] < 0:
            self.threatDict[toonId] = 0
        

    def waitForNextAttack(self, delayTime):
        currState = self.getCurrentOrNextState()
        if (currState == 'BattleFour'):
            assert self.notify.debug("%s.Waiting %s seconds for next attack." % (self.doId, delayTime))
            taskName = self.uniqueName('NextAttack')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextAttack, taskName)
        else:
            assert self.notify.debug("%s.Not doing another attack in state %s." % (self.doId, currState))

    def doNextAttack(self, task):
        assert self.notify.debug("%s.doNextAttack()" % (self.doId))
        # Choose an attack and do it.
        attackCode = -1
        optionalParam = None
        if self.movingToTable:
            # we are still doing the move attack
            self.waitForNextAttack(5)
        elif self.attackCode == ToontownGlobals.BossCogDizzyNow:
            # We always choose this particular attack when recovering
            # from dizzy.  It's really the same as the front attack,
            # with extra time for standing up first.
            attackCode = ToontownGlobals.BossCogRecoverDizzyAttack

        else:
            # Choose an attack at random.
            if self.getBattleFourTime() > self.overtimeOneStart and not self.doneOvertimeOneAttack:
                attackCode = ToontownGlobals.BossCogOvertimeAttack
                self.doneOvertimeOneAttack = True
                optionalParam = 0
            elif self.getBattleFourTime() > 1.0 and not self.doneOvertimeTwoAttack:
                attackCode = ToontownGlobals.BossCogOvertimeAttack
                self.doneOvertimeTwoAttack = True
                optionalParam = 1
            else:
                attackCode = random.choice(
                    [ToontownGlobals.BossCogGolfAreaAttack,
                     ToontownGlobals.BossCogDirectedAttack,
                     ToontownGlobals.BossCogDirectedAttack,
                     ToontownGlobals.BossCogDirectedAttack,
                     ToontownGlobals.BossCogDirectedAttack,
                     ])
            
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.__doAreaAttack()
        if attackCode == ToontownGlobals.BossCogGolfAreaAttack:
            self.__doGolfAreaAttack()
        elif attackCode == ToontownGlobals.BossCogDirectedAttack:
            self.__doDirectedAttack()
        elif attackCode >= 0:
            self.b_setAttackCode(attackCode, optionalParam)


    def progressValue(self, fromValue, toValue):
        # Returns an interpolated value from fromValue to toValue,
        # depending on the value of self.bossDamage in the range [0,
        # self.bossMaxDamage].  It is also based on time.

        # That is, lerps the value fromValue to toValue during the
        # course of the battle.
        
        # t0 is the elapsed damage
        t0 = float(self.bossDamage) / float(self.bossMaxDamage)

        # t1 is the elapsed time
        elapsed = globalClock.getFrameTime() - self.battleFourStart
        t1 = elapsed / float(self.battleThreeDuration)

        # We actually progress the value based on the larger of the
        # two, so you can't spend all day in the battle.
        t = max(t0, t1)
        
        progVal = fromValue + (toValue - fromValue) * min(t, 1)
        self.notify.debug('progVal=%s' % progVal)
        import pdb; pdb.set_trace()
        return progVal

    def __doDirectedAttack(self):
        """Do an attack at a toon."""
        toonId = self.getMaxThreatToon()
        self.notify.debug('toonToAttack=%s' % toonId)
        unflattenedToons = self.getUnflattenedToons()
        attackTotallyRandomToon = random.random() < 0.1        
        if unflattenedToons and (attackTotallyRandomToon or toonId==0):
            toonId = random.choice(unflattenedToons)
        if toonId:
            toonThreat = self.getThreat(toonId)
            toonThreat *= 0.25
            threatToSubtract = max( toonThreat, 10)
            self.subtractThreat(toonId, threatToSubtract)
            if self.isToonRoaming(toonId):
                self.b_setAttackCode(ToontownGlobals.BossCogGolfAttack, toonId)
                self.numGolfAttacks += 1
            elif self.isToonOnTable(toonId):
                # lets make him shoot a small percent of the time
                doesMoveAttack = simbase.air.config.GetBool('ceo-does-move-attack',1)
                if doesMoveAttack:
                    chanceToShoot = 0.25
                else:
                    chanceToShoot = 1.0
                # if we have a magic word not to move, then don't move
                if not self.moveAttackAllowed:
                    self.notify.debug('moveAttack is not allowed, doing gearDirectedAttack')
                    chanceToShoot = 1.0
                if random.random() < chanceToShoot:
                    self.b_setAttackCode(ToontownGlobals.BossCogGearDirectedAttack, toonId)
                    self.numGearAttacks += 1
                else:
                    tableIndex = self.getToonTableIndex(toonId)
                    self.doMoveAttack(tableIndex)
            else:
                self.b_setAttackCode(ToontownGlobals.BossCogGolfAttack, toonId)
        else:
            # let's move him to a random table
            uprightTables = self.getUprightTables()
            if uprightTables:
                tableToMoveTo = random.choice(uprightTables)
                self.doMoveAttack(tableToMoveTo)
            else:
                # really nothing to do
                self.waitForNextAttack(4)
    
        
    def doMoveAttack(self, tableIndex):
        """A new attack where the boss runs over a table."""
        self.numMoveAttacks += 1
        self.movingToTable = True
        self.tableDest = tableIndex
        self.b_setAttackCode(ToontownGlobals.BossCogMoveAttack, tableIndex)

    def getUnflattenedToons(self):
        """Return a list of toonsIds who are not flattened."""
        result = []
        uprightTables = self.getUprightTables()
        for toonId in self.involvedToons:
            toonTable = self.getToonTableIndex(toonId)
            if toonTable >=0 and \
               not (toonTable in uprightTables):
                pass
            else:
                result.append(toonId)
        return result
        

    def getMaxThreatToon(self):
        """Return the toon with the most threat."""
        returnedToonId = 0
        maxThreat = 0
        maxToons = []
        for toonId in self.threatDict:
            curThreat = self.threatDict[toonId]
            tableIndex = self.getToonTableIndex(toonId)
            if tableIndex > -1 and self.tables[tableIndex].state == 'Flat':
                # don't attack a flattened toon
                pass
            else:
                if curThreat > maxThreat:
                    maxToons = [toonId]
                    maxThreat = curThreat
                elif curThreat == maxThreat:
                    maxToons.append(toonId)
        if maxToons:
            returnedToonId = random.choice(maxToons)
        return returnedToonId
        
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

    def calcAndSetBattleDifficulty(self):
        self.toonLevels = self.getToonDifficulty()
        numDifficultyLevels = len(ToontownGlobals.BossbotBossDifficultySettings)
        battleDifficulty = int (  self.toonLevels / self.maxToonLevels * numDifficultyLevels)

        if battleDifficulty >= numDifficultyLevels:
            battleDifficulty = numDifficultyLevels -1

        self.b_setBattleDifficulty(battleDifficulty)
        

    def b_setBattleDifficulty(self, batDiff):
        self.setBattleDifficulty(batDiff)
        self.d_setBattleDifficulty(batDiff)

    def setBattleDifficulty(self, batDiff):
        self.battleDifficulty = batDiff

    def d_setBattleDifficulty(self, batDiff):
        self.sendUpdate('setBattleDifficulty', [batDiff])

    def getUprightTables(self):
        """Return a list of table indices who are still upright."""
        tableList = []
        for table in self.tables:
            if table.state != 'Flat':
                tableList.append(table.index)
        return tableList

    def getToonTableIndex(self, toonId):
        """Returns the table index he is on, -1 if he's not on a table"""
        tableIndex = -1
        for table in self.tables:
            if table.avId == toonId:
                tableIndex =  table.index
                break
        return tableIndex

    def getToonGolfSpotIndex(self, toonId):
        """Returns the golfSpot index he is on, -1 if he's not on a golfSpot"""
        golfSpotIndex = -1
        for golfSpot in self.golfSpots:
            if golfSpot.avId == toonId:
                golfSpotIndex =  golfSpot.index
                break
        return golfSpotIndex        

    def isToonOnTable(self, toonId):
        """Returns True if the toon is on a table."""
        result = self.getToonTableIndex(toonId) != -1
        return result

    def isToonOnGolfSpot(self, toonId):
        """Returns True if the toon is on a golf spot."""
        result = self.getToonGolfSpotIndex(toonId) != -1
        return result

    def isToonRoaming(self, toonId):
        result = not self.isToonOnTable(toonId) and not self.isToonOnGolfSpot(toonId)
        return result

    def reachedTable(self, tableIndex):
        """One of the clients has signalled the boss has reached the table."""
        if self.movingToTable and self.tableDest == tableIndex:
            self.movingToTable = False
            self.curTable = self.tableDest
            self.tableDest = -1

    def hitTable(self, tableIndex):
        """One of the clients has signalled the boss has reached the table."""
        self.notify.debug('hitTable tableIndex=%d' % tableIndex)
        if tableIndex < len(self.tables):
            table = self.tables[tableIndex]
            if table.state != 'Flat':
                table.goFlat()

    def awayFromTable(self, tableIndex):
        """One of the clients has signalled the boss has moved away from the table."""
        self.notify.debug('awayFromTable tableIndex=%d' % tableIndex)
        if tableIndex < len(self.tables):
            #import pdb; pdb.set_trace()
            taskName = 'Unflatten-%d' % tableIndex
            unflattenTime= self.diffInfo[3]
            taskMgr.doMethodLater(unflattenTime, self.unflattenTable, taskName, extraArgs=[tableIndex])

    def unflattenTable(self, tableIndex):
        """Unflatten the table."""
        if tableIndex < len(self.tables):
            table = self.tables[tableIndex]
            if table.state == 'Flat':
                if table.avId and \
                   table.avId in self.involvedToons:
                    table.forceControl(table.avId)
                else:
                    table.goFree()

    def incrementDinersExploded(self):
        """Increase the count of diners exploded."""
        self.numDinersExploded +=1

    def magicWordHit(self, damage, avId):
        # Called by the magic word "~bossBattle hit damage"
        self.hitBoss(damage)

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)

    def __doGolfAreaAttack(self):
        self.numGolfAreaAttacks += 1
        self.b_setAttackCode(ToontownGlobals.BossCogGolfAreaAttack)        

 
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
            self.sendUpdate('toonGotHealed',[toonId])

    def requestGetToonup(self, beltIndex, toonupIndex, toonupNum):
        """Handle a toon requesting to get toonup from the conveyer belts."""
        grantRequest = False
        avId = self.air.getAvatarIdFromSender()
        if self.state != 'BattleFour':
            grantRequest = False
        elif not (beltIndex, toonupNum) in self.toonupsGranted:
            # make sure the toon is still there
            toon = simbase.air.doId2do.get(avId)
            if toon:
                # no one else got it
                grantRequest = True
            
        if grantRequest:
            self.toonupsGranted.insert(0, (beltIndex, toonupNum))
            if len(self.toonupsGranted) > 8:
                self.toonupsGranted = self.toonupsGranted[0:8]
            self.sendUpdate('toonGotToonup', [avId, beltIndex, toonupIndex, toonupNum])
            if toonupIndex < len(self.toonUpLevels):
                self.healToon(toon, self.toonUpLevels[toonupIndex])
                self.numToonupGranted += 1
                self.totalLaffHealed += self.toonUpLevels[toonupIndex]
            else:
                self.notify.warning('requestGetToonup this should not happen')
                self.healToon(toon,1)
            
    def toonLeftTable(self, tableIndex):
        """Think if the toon leaving the table will make us do something else."""
        if self.movingToTable and self.tableDest == tableIndex:
            # the toon on the table we are moving to just jumped off.
            if random.random() < 0.5:
                self.movingToTable = False
                self.waitForNextAttack(0)
            
    def getBattleFourTime(self):
        # Returns the amount of time spent so far in battle four, as
        # a ratio of the expected battle three duration.  This will
        # range 0 .. 1 during the normal course of the battle; if it
        # goes beyond 1, the battle should be considered to be in
        # overtime (and should rapidly become impossibly difficult, to
        # prevent toons from dying a slow, frustrating death).
        if self.state != 'BattleFour':
            t1 = 0
        else:
            elapsed = globalClock.getFrameTime() - self.battleFourStart
            t1 = elapsed / float(self.battleFourDuration)
        return t1

    def getDamageMultiplier(self):
        """Return a multiplier for cog attacks."""
        mult = 1.0
        if self.doneOvertimeOneAttack and not self.doneOvertimeTwoAttack:
            mult = 1.25
        if self.getBattleFourTime() > 1.0:
            # we're in overtime make him hit harder
            mult = self.getBattleFourTime() + 1
        return mult

    def toggleMove(self):
        """Handle the magic word to toggle us doing move attacks."""
        self.moveAttackAllowed = not self.moveAttackAllowed
        return self.moveAttackAllowed
