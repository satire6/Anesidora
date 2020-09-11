import DistributedBattleAI
from direct.directnotify import DirectNotifyGlobal

class BattleManagerAI:

    """ This class used to assume that there was one battle cell per zone.
    It now supports any number of battle cells per zone, and requires that
    you pass in 'battle cell IDs' to identify battle cells. There is nothing
    magic about battle cell IDs, they just have to be unique and map
    one-to-one with the battle cells. For systems that happen to have one
    battle cell per zone, like the streets, it should be perfectly fine to
    use zoneIds as battle cell IDs. """

    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    def __init__(self, air):
        """__init__(air)
        """
        self.air = air
        self.cellId2battle = {}
        self.battleConstructor = DistributedBattleAI.DistributedBattleAI

    def cellHasBattle(self, cellId):
        """ cellHasBattle(cellId)
        """
        return (self.cellId2battle.has_key(cellId))

    def getBattle(self, cellId):
        if self.cellId2battle.has_key(cellId):
            return self.cellId2battle[cellId]
        return None

    def newBattle(self, cellId, zoneId, pos, suit, toonId,
                  finishCallback=None, maxSuits=4, interactivePropTrackBonus = -1):
        """ newBattle(zoneId, pos, suit, toonId, finishCallback, maxSuits)
        """
        if self.cellId2battle.has_key(cellId):
            # if a battle already exists here, don't create a new one,
            # but instead make the suit join the battle or fly away.

            # This is an extremely rare case; normally a suit won't
            # try to start a battle where a battle is already taking
            # place.
            self.notify.info("A battle is already present in the suit's zone!")
            if not self.requestBattleAddSuit(cellId, suit):
                # No room for the suit, fly him away.
                suit.flyAwayNow()

            battle = self.cellId2battle[cellId]
            battle.signupToon(toonId, pos[0], pos[1], pos[2])

        else:
            # Generate a new battle.  This is the normal case.
            battle = self.battleConstructor(
                self.air, self,
                pos, suit, toonId, zoneId, finishCallback, maxSuits, interactivePropTrackBonus = interactivePropTrackBonus)
            battle.generateWithRequired(zoneId)
            battle.battleCellId = cellId
            self.cellId2battle[cellId] = battle
            
        return battle

    def requestBattleAddSuit(self, cellId, suit):
        """ requestBattleAddSuit(zoneId, suit)
        """
        assert(self.cellId2battle.has_key(cellId))
        return (self.cellId2battle[cellId].suitRequestJoin(suit))

    def destroy(self, battle):
        """ destroy(battle)
        """
        cellId = battle.battleCellId
        self.notify.debug('BattleManager - destroying battle %d' % cellId)
        assert(self.cellId2battle.has_key(cellId))
        del self.cellId2battle[cellId]
        battle.requestDelete()
