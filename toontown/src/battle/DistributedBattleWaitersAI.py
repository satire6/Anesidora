from direct.directnotify import DirectNotifyGlobal
from toontown.battle import DistributedBattleFinalAI

# attack properties table
class DistributedBattleWaitersAI(DistributedBattleFinalAI.DistributedBattleFinalAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleWaitersAI')
                    
    def __init__(self, air, bossCog, roundCallback,
                 finishCallback, battleSide):
        DistributedBattleFinalAI.DistributedBattleFinalAI.__init__(
            self, air, bossCog, roundCallback, finishCallback, battleSide)

    def startBattle(self, toonIds, suits):
        self.joinableFsm.request('Joinable')
        for toonId in toonIds:
            if self.addToon(toonId):
                self.activeToons.append(toonId)

        # We have to be sure to tell the players that they're active
        # before we start adding suits.
        self.d_setMembers()

        for suit in suits:
            self.pendingSuits.append(suit)
            #joined =self.suitRequestJoin(suit)
            #assert(joined)

        self.d_setMembers()
        self.needAdjust =1
        self.b_setState('ReservesJoining')
