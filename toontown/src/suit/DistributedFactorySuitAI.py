from otp.ai.AIBaseGlobal import *

from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
import DistributedSuitBaseAI
import SuitDialog

class DistributedFactorySuitAI(DistributedSuitBaseAI.DistributedSuitBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedFactorySuitAI')

    def __init__(self, air, suitPlanner):
        """__init__(air, suitPlanner)"""
        DistributedSuitBaseAI.DistributedSuitBaseAI.__init__(self, air, 
                                                             suitPlanner)

        self.blocker = None
        self.battleCellIndex = None
        self.chasing = 0
        self.factoryGone = 0

    def factoryIsGoingDown(self):
        self.factoryGone = 1
        
    def delete(self):
        if not self.factoryGone:
            self.setBattleCellIndex(None)
        del self.blocker
        self.ignoreAll()
        DistributedSuitBaseAI.DistributedSuitBaseAI.delete(self)

    def setLevelDoId(self, levelDoId):
        self.levelDoId = levelDoId
    def getLevelDoId(self):
        return self.levelDoId

    def setCogId(self, cogId):
        self.cogId = cogId
    def getCogId(self):
        return self.cogId
        
    def setReserve(self, reserve):
        self.reserve = reserve
    def getReserve(self):
        return self.reserve

    def requestBattle(self, x, y, z, h, p, r):
        """requestBattle(x, y, z, h, p, r)
        """
        toonId = self.air.getAvatarIdFromSender()

        if self.notify.getDebug():
            self.notify.debug(str(self.getDoId()) + \
                              str(self.zoneId) + \
                              ': request battle with toon: %d' % toonId)

        # Store the suit's actual pos and hpr on the client
        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        # Request a battle from the suit planner
        if (self.sp.requestBattle(self, toonId)):
            if self.notify.getDebug():
                self.notify.debug("Suit %d requesting battle in zone %d with toon %d" %
                                  (self.getDoId(), self.zoneId, toonId))
        else:
            # Suit tells toon to get lost
            if self.notify.getDebug():
                self.notify.debug('requestBattle from suit %d, toon %d- denied by battle manager' % (toonId, self.getDoId()))
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle(toonId)

    def getConfrontPosHpr(self):
        """ getConfrontPosHpr()
        """
        return (self.confrontPos, self.confrontHpr)

    def setBattleCellIndex(self, battleCellIndex):
        self.sp.suitBattleCellChange(self,
                                     oldCell=self.battleCellIndex,
                                     newCell=battleCellIndex)
        self.battleCellIndex = battleCellIndex
        # attach any battle blockers for this cell
        self.attachBattleBlocker()
        # and listen for any other blockers that might be created for this cell
        self.accept(self.sp.getBattleBlockerEvent(self.battleCellIndex), self.attachBattleBlocker)
        
    def getBattleCellIndex(self):
        return self.battleCellIndex

    def attachBattleBlocker(self):
        blocker = self.sp.battleMgr.battleBlockers.get(self.battleCellIndex)
        self.blocker = blocker
            
    def setAlert(self, avId):
        #if self.chasing:
        #    return
        
        # make sure the avId is the same as the message sender
        if avId == self.air.getAvatarIdFromSender():
            av = self.air.doId2do.get(avId)
            if av:
                self.chasing = avId
                # if we are already in a battle don't send the confront
                # TODO figure out a better way if this suit is already in a battle
                if self.sp.battleMgr.cellHasBattle(self.battleCellIndex):
                    pass
                else:
                    self.sendUpdate("setConfrontToon", [avId])

    def setStrayed(self):
        if self.chasing > 0:
            # tell the clients the Suit has gone too far,
            # and let them move the suit back into position
            self.chasing = 0
            self.sendUpdate("setReturn", [])

    def resume( self ):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    called by battles to tell this suit that it is no
        //              longer part of a battle, and it should carry on.
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """

        self.notify.debug("Suit %s resume" % (self.doId))

        if self.currHP <= 0:
            messenger.send(self.getDeathEvent())
            # If the suit's dead, take it out.
            self.notify.debug("Suit %s dead after resume" % (self.doId))
            self.requestRemoval()

        else:
            # return the suit to it's original waiting position
            # (or path, if/when the factory suits are walking on paths)
            self.sendUpdate("setReturn", [])
        return None

    def isForeman(self):
        return self.boss
        
    def setVirtual(self, isVirtual = 1):
        self.virtual = isVirtual
        
    def getVirtual(self):
        return self.virtual
