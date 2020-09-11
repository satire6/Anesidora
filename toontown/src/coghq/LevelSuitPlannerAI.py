from pandac.PandaModules import *

from direct.showbase import DirectObject
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
import LevelBattleManagerAI
import types
import random

class LevelSuitPlannerAI(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'LevelSuitPlannerAI')

    def __init__(self, air, level, cogCtor, battleCtor, cogSpecs,
                 reserveCogSpecs, battleCellSpecs, battleExpAggreg=None):
        self.air = air
        self.level = level
        self.cogCtor = cogCtor
        self.cogSpecs = cogSpecs

        # config off reserve suits for test server
        if simbase.config.GetBool('level-reserve-suits', 0):
            self.reserveCogSpecs = reserveCogSpecs
        else:
            self.reserveCogSpecs = []
        self.battleCellSpecs = battleCellSpecs
        self.__genSuitInfos(self.level.getCogLevel(),
                            self.level.getCogTrack())
        self.battleMgr = LevelBattleManagerAI.LevelBattleManagerAI(
            self.air, self.level, battleCtor, battleExpAggreg)

        # create a dict that will keep track of what suits are attached
        # to what battle cell
        self.battleCellId2suits = {}
        for id in self.battleCellSpecs.keys():
            self.battleCellId2suits[id] = []

    def destroy(self):
        self.battleMgr.destroyBattleMgr()
        del self.battleMgr
        self.battleCellId2suits = {}
        self.ignoreAll()
        del self.cogSpecs
        del self.cogCtor
        del self.level
        del self.air
        
    def __genJoinChances( self, num ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        joinChances = []
        for currChance in range( num ):
            joinChances.append( random.randint( 1, 100 ) )
        joinChances.sort( cmp )
        return joinChances

    def __genSuitInfos(self, level, track):
        if __dev__:
            assert type(level) == types.IntType

        def getSuitDict(spec, cogId, level=level, track=track):
            suitDict = {}
            # set defaults
            suitDict['track'] = track
            suitDict.update(spec)
            # calc the cog's zone
            suitDict['zoneId'] = self.level.getEntityZoneId(
                spec['parentEntId'])
            # fix up the cog level
            suitDict['level'] += level
            suitDict['cogId'] = cogId
            return suitDict
        
        # Build a dictionary with types, levels, and locations for suits
        self.suitInfos = {}
        self.suitInfos['activeSuits'] = []
        for i in range(len(self.cogSpecs)):
            spec = self.cogSpecs[i]
            self.suitInfos['activeSuits'].append(getSuitDict(spec, i))

        # reserveSuits
        
        numReserve = len(self.reserveCogSpecs)
        joinChances = self.__genJoinChances(numReserve)
        self.suitInfos['reserveSuits'] = []
        for i in range(len(self.reserveCogSpecs)):
            spec = self.reserveCogSpecs[i]
            suitDict = getSuitDict(spec, i)
            suitDict['joinChance'] = joinChances[i]
            self.suitInfos['reserveSuits'].append(suitDict)

    def __genSuitObject(self, suitDict, reserve):
        suit = self.cogCtor(simbase.air, self)
        dna = SuitDNA.SuitDNA()
        # Will want to be more specific here?
        dna.newSuitRandom(level=SuitDNA.getRandomSuitType(suitDict['level']),
                          dept=suitDict['track'])
        suit.dna = dna
        suit.setLevel(suitDict['level'])
        suit.setSkeleRevives(suitDict.get('revives'))
        suit.setLevelDoId(self.level.doId)
        suit.setCogId(suitDict['cogId'])
        suit.setReserve(reserve)
        if suitDict['skeleton']:
            # 'skelecog' is a required attribute, it will be sent to clients
            # on generate
            suit.setSkelecog(1)
        suit.generateWithRequired(suitDict['zoneId'])
        suit.boss = suitDict['boss']
        return suit

    def genSuits(self):
        # Generate the suits that are active (i.e. are walking around visibly)
        suitHandles = {}

        activeSuits = []
        for activeSuitInfo in self.suitInfos['activeSuits']:
            suit = self.__genSuitObject(activeSuitInfo, 0)
            suit.setBattleCellIndex(activeSuitInfo['battleCell'])
            activeSuits.append(suit)
        #assert(len(activeSuits) > 0)
        suitHandles['activeSuits'] = activeSuits

        # Generate the reserve suits (i.e. that will pop in through the floor,
        # enter from an elevator, or helicopter in from the sky during battle)
        reserveSuits = []
        for reserveSuitInfo in self.suitInfos['reserveSuits']:
            suit = self.__genSuitObject(reserveSuitInfo, 1)
            assert(self.notify.debug("creating reserve suit info: %s, %s" % (suit.doId, reserveSuitInfo)))
            #suit.setBattleCellIndex(reserveSuitInfo['battleCell'])
            reserveSuits.append([suit, reserveSuitInfo['joinChance'],
                                 reserveSuitInfo['battleCell']])
        #assert(len(reserveSuits) > 0)
        suitHandles['reserveSuits'] = reserveSuits

        return suitHandles

    def __suitCanJoinBattle(self, cellId):
        battle = self.battleMgr.getBattle(cellId)
        if not battle.suitCanJoin():
            return 0
        # maybe let suit join?
        # for now, always
        return 1

    def requestBattle(self, suit, toonId):
        cellIndex = suit.getBattleCellIndex()
        cellSpec = self.battleCellSpecs[cellIndex]
        pos = cellSpec['pos']
        zone = self.level.getZoneId(
            self.level.getEntityZoneEntId(cellSpec['parentEntId']))
        maxSuits = 4
        self.battleMgr.newBattle(cellIndex, zone, pos, suit, toonId,
                                 self.__handleRoundFinished,
                                 self.__handleBattleFinished,
                                 maxSuits)

        for otherSuit in self.battleCellId2suits[cellIndex]:
            if otherSuit is not suit:
                if self.__suitCanJoinBattle(cellIndex):
                    self.battleMgr.requestBattleAddSuit(cellIndex, otherSuit)
                else:
                    # I guess we could also just let the suit carry on...
                    # except that it might collide with localToon and
                    # trigger another battle. Yech.
                    ## This crashes; don't assign >4 suits to a battle cell
                    ## for now
                    battle = self.battleMgr.getBattle(cellIndex)
                    if battle:
                        self.notify.warning(
                            'battle not joinable: numSuits=%s, joinable=%s, fsm=%s, toonId=%s' %
                            (len(battle.suits), battle.isJoinable(),
                             battle.fsm.getCurrentState().getName(), toonId))
                    else:
                        self.notify.warning('battle not joinable: no battle for cell %s, toonId=%s' % (cellIndex, toonId))
                        
                    return 0

        return 1

    def __handleRoundFinished(self, cellId, toonIds, totalHp, deadSuits):
        # Determine if any reserves need to join
        assert(self.notify.debug('cell %s, handleRoundDone() - hp: %d' % (cellId,totalHp)))
        # Calculate the total max HP for all the suits currently on the floor
        totalMaxHp = 0
        level = self.level
        battle = self.battleMgr.cellId2battle[cellId]
        for suit in battle.suits:
            totalMaxHp += suit.maxHP

        for suit in deadSuits:
            level.suits.remove(suit)

        assert(self.notify.debug('handleRoundDone() - reserveSuits: %d, battleSuits: %d' % (len(level.reserveSuits),
                                                                                            len(battle.suits))))

        # get a list of reserve suits for this battle cell
        cellReserves = []
        for info in level.reserveSuits:
            if info[2] == cellId:
                assert(self.notify.debug("adding suit %d to cellReserves list" % info[0].doId))
                cellReserves.append(info)

        # Determine if any reserve suits need to join
        numSpotsAvailable = 4 - len(battle.suits)
        if (len(cellReserves) > 0 and numSpotsAvailable > 0):
            assert(self.notify.debug('potential reserve suits: %d' % \
                len(level.reserveSuits)))
            self.joinedReserves = []
            if __dev__:
                assert(totalHp <= totalMaxHp)
            if (len(battle.suits) == 0):
                hpPercent = 100
            else:
                hpPercent = 100 - (totalHp / totalMaxHp * 100.0)
            assert(self.notify.debug('totalHp: %d totalMaxHp: %d percent: %f' \
                % (totalHp, totalMaxHp, hpPercent)))
            for info in cellReserves:
                if (info[1] <= hpPercent and
                    len(self.joinedReserves) < numSpotsAvailable):
                    assert(self.notify.debug('reserve: %d joining percent: %f' \
                        % (info[0].doId, info[1])))
                    level.suits.append(info[0])
                    self.joinedReserves.append(info)
                    info[0].setBattleCellIndex(cellId)
            for info in self.joinedReserves:
                level.reserveSuits.remove(info)
            if (len(self.joinedReserves) > 0):
                # setSuits() triggers the state change on the client

                # SDN: fsm-ify this?
                self.reservesJoining(battle)
                
                level.d_setSuits()
                return

        # See if the battle is done
        if (len(battle.suits) == 0):
            # SDN: add in code to remove toons from level
            #level.fsm.request('BattleDone', [toonIds])
            if battle:
                battle.resume()
        else:
            # No reserve suits to join - tell the battle to continue
            battle = self.battleMgr.cellId2battle.get(cellId)
            if battle:
                battle.resume()

    def __handleBattleFinished(self, zoneId):
        pass
    
    def reservesJoining(self, battle):
        # note, once we put in the animation for suits joining battle
        # we should delay this code by the time it takes to play the animation
        for info in self.joinedReserves:
            battle.suitRequestJoin(info[0])
        battle.resume()
        self.joinedReserves = []
            
    def getDoId(self):
        # This is a dummy function so we don't need to modify DistributedSuit
        return 0

    def removeSuit(self, suit):
        # delete the suit
        suit.requestDelete()

    def suitBattleCellChange(self, suit, oldCell, newCell):
        # oldCell and/or newCell can be None
        if oldCell is not None:
            if oldCell in self.battleCellId2suits:
                self.battleCellId2suits[oldCell].remove(suit)
            else:
                self.notify.warning('FIXME crash bandaid suitBattleCellChange suit.doId =%s, oldCell=%s not in battleCellId2Suits.keys %s' %
                                    (suit.doId, oldCell, self.battleCellId2suits.keys()))
            # remove suit from battle blocker
            blocker = self.battleMgr.battleBlockers.get(oldCell)
            if blocker:
                blocker.removeSuit(suit)
        if newCell is not None:
            self.battleCellId2suits[newCell].append(suit)

            # register suit with the blocker for this newCell
            def addSuitToBlocker(self=self):
                blocker = self.battleMgr.battleBlockers.get(newCell) 
                if blocker:
                    blocker.addSuit(suit)
                    return 1
                return 0

            if not addSuitToBlocker():
                # wait for the creation of this blocker, then add this suit
                self.accept(self.getBattleBlockerEvent(newCell), addSuitToBlocker)
                
    def getBattleBlockerEvent(self, cellId):
        return "battleBlockerAdded-"+str(self.level.doId)+"-"+str(cellId)
