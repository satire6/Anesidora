from toontown.battle import BattleManagerAI
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import BattleExperienceAggregatorAI

class LevelBattleManagerAI(BattleManagerAI.BattleManagerAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('LevelBattleManagerAI')

    def __init__(self, air, level, battleCtor, battleExpAggreg=None):
        BattleManagerAI.BattleManagerAI.__init__(self, air)
        self.battleCtor = battleCtor
        self.level = level
        # Create a dict that will hold BattleBlocker references
        # When the battle blocker is created, it will register itself
        # with the battleMgr here
        self.battleBlockers = {}

        if battleExpAggreg is None:
            battleExpAggreg = BattleExperienceAggregatorAI.\
                              BattleExperienceAggregatorAI()
        self.battleExpAggreg = battleExpAggreg

    def destroyBattleMgr(self):
        battles = self.cellId2battle.values()
        for battle in battles:
            self.destroy(battle)
        for cellId, battleBlocker in self.battleBlockers.items():
            if battleBlocker is not None:
                battleBlocker.deactivate()
        del self.battleBlockers
        del self.cellId2battle
        del self.battleExpAggreg
    
    def newBattle(self, cellId, zoneId, pos, suit, toonId,
                  roundCallback=None, finishCallback=None,
                  maxSuits=4):
        """ newBattle(zoneId, pos, suit, toonId, roundCallback, finishCallback, maxSuits)
        """
        battle = self.cellId2battle.get(cellId, None)
        if battle != None:
            # This is a race condition and happens rarely.  It happens when
            # a toon bumps into a battle blocker in almost the same instance
            # as a battle is being created for that battle cell.  The battle
            # blocker thinks a battle has not been started, and tells the suit
            # to create a new one.  By the time the suit does this, the battle
            # has already been created.  Don't add the suit, just add the toon.
            self.notify.debug("battle already created by battle blocker, add toon %d" % toonId)
            battle.signupToon(toonId, pos[0], pos[1], pos[2])
            return battle
        else:
            # Generate a new battle.  This is the normal case.
            battle = self.battleCtor(
                self.air, self,
                pos, suit, toonId, zoneId, self.level,
                cellId, roundCallback, finishCallback, maxSuits)
            # We store the lists of experience in the battle manager and
            # share these pointers in all battles so we can accumulate
            # experience.
            self.battleExpAggreg.attachToBattle(battle)

            # set the exp multiplier
            battle.battleCalc.setSkillCreditMultiplier(
                self.level.getBattleCreditMultiplier())

            # Now that exp is initialized, we can add the toon
            battle.addToon(toonId)

            battle.generateWithRequired(zoneId)
            self.cellId2battle[cellId] = battle
            
        return battle

    def addBattleBlocker(self, blocker, cellId):
        # add to dict
        self.battleBlockers[cellId] = blocker
        # send a message out for suits/battles that are listening
        messenger.send(self.level.planner.getBattleBlockerEvent(cellId))
