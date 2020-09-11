from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
from toontown.toonbase import ToontownGlobals
import DistributedSuitBaseAI
import random
from direct.fsm import ClassicFSM, State
from direct.fsm import State

class DistributedLawbotBossSuitAI(DistributedSuitBaseAI.DistributedSuitBaseAI):
    """
    These are meant to represent the lawyers in battle three of Lawbot Boss
    """

    notify = DirectNotifyGlobal.directNotify.newCategory(
                                        'DistributedLawbotBossSuitAI')

    def __init__(self, air, suitPlanner):
        """__init__(air, suitPlanner)"""
        DistributedSuitBaseAI.DistributedSuitBaseAI.__init__(self, air, 
                                                             suitPlanner)
        self.stunned = False
        self.timeToRelease = 3.15 #should match DistributedLawbotBossSuit.py
        self.timeProsecuteStarted = 0
        

        # Set up the DistributedSuit state machine
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedLawbotBossSuitAI',
            [State.State('Off',
                         self.enterOff,
                         self.exitOff,
                         ['neutral']
                         ),
             State.State('neutral',
                         self.enterNeutral,
                         self.exitNeutral,
                         ['PreThrowProsecute',
                          'PreThrowAttack',
                          'Stunned']
                         ),
             State.State('PreThrowProsecute',
                         self.enterPreThrowProsecute,
                         self.exitPreThrowProsecute,
                         ['PostThrowProsecute',
                          'neutral',
                          'Stunned']
                         ),
             State.State('PostThrowProsecute',
                         self.enterPostThrowProsecute,
                         self.exitPostThrowProsecute,
                         ['neutral',
                          'Stunned']
                         ),
             State.State('PreThrowAttack',
                         self.enterPreThrowAttack,
                         self.exitPreThrowAttack,
                         ['PostThrowAttack',
                          'neutral',
                          'Stunned']
                         ),
             State.State('PostThrowAttack',
                         self.enterPostThrowAttack,
                         self.exitPostThrowAttack,
                         ['neutral',
                          'Stunned']
                         ),
             State.State('Stunned',
                         self.enterStunned,
                         self.exitStunned,
                         ['neutral']
                         ),
             ],
            # Initial state
            'Off',
            # Final state
            'Off',
            )
        
        self.fsm.enterInitialState()
        

    def delete(self):
        self.notify.debug("delete %s" % self.doId)
        self.ignoreAll()        
        DistributedSuitBaseAI.DistributedSuitBaseAI.delete(self)
        self.notify.debug('setting self.boss to None')
        self.boss = None
        
        taskName = self.uniqueName('ProsecutionHealsBoss')
        if taskMgr.hasTaskNamed(taskName):
            self.notify.debug('still has task %s' % taskName)
        taskMgr.remove(taskName)
        
        taskName = self.uniqueName('unstun')
        if taskMgr.hasTaskNamed(taskName):
            self.notify.debug('still has task %s' % taskName)
        taskMgr.remove(taskName)

        self.fsm = None

    def requestBattle(self, x, y, z, h, p, r):
        """requestBattle(x, y, z, h, p, r)
        """
        toonId = self.air.getAvatarIdFromSender()

        if self.notify.getDebug():
            self.notify.debug( str( self.getDoId() ) + \
                               str( self.zoneId ) + \
                               ': request battle with toon: %d' % toonId )

        # Store the suit's actual pos and hpr on the client
        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        # Request a battle from the suit planner
        if (self.sp.requestBattle(self.zoneId, self, toonId)):
            self.acceptOnce(self.getDeathEvent(), self._logDeath, [toonId])
            if self.notify.getDebug():
                self.notify.debug( "Suit %d requesting battle in zone %d" %
                                   (self.getDoId(), self.zoneId) )
        else:
            # Suit tells toon to get lost
            if self.notify.getDebug():
                self.notify.debug('requestBattle from suit %d - denied by battle manager' % (self.getDoId()))
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle( toonId )

    def getPosHpr(self):
        return (self.getX(), self.getY(), self.getZ(), self.getH(), self.getP(), self.getR())

    def getConfrontPosHpr(self):
        """ getConfrontPosHpr()
        """
        return (self.confrontPos, self.confrontHpr)

    def _logDeath(self, toonId):
        pass
        #self.air.writeServerEvent('beatFirstCog', toonId, '')

    def doNextAttack(self, lawbotBoss):
        """
        Should we try to hit a toon, or throw stuff on the prosecution evidence.  All random for now
        """

        if self.stunned:
            return
        
        chanceToDoAttack = ToontownGlobals.LawbotBossLawyerChanceToAttack
        action = random.randrange(1,101)
        if action > chanceToDoAttack:
            #we throw stuff at the prosecution pan
            self.doProsecute()
            pass
        else:
            #we hit a toon
            if not lawbotBoss.involvedToons:
                #do an immediate return, no more toons around
                return

            
            toonToAttackId = random.choice(lawbotBoss.involvedToons)
            toon = self.air.doId2do.get(toonToAttackId)

            if not toon:
                self.doProsecute()
                return

            #import pdb; pdb.set_trace()
            toonPos = toon.getPos();
            z2 = toonPos[2] + 1.3 #adjust it slightly higher so we're not aiming for the feet

            
            
            toonPos = Point3(toonPos.getX(), toonPos.getY(), 0)

            lawyerPos = self.getPos();

            lawyerPos = Point3(self.getPos().getX(), self.getPos().getY(), 0)

            #force the lawyer z to be the same
            #lawyerPos[2] += 1.3

            dirVector = toonPos - lawyerPos
            dirVector.normalize()
            dirVector *= 200; #TODO change this to the maximum length inside the court room

            destPos = Point3(lawyerPos[0] + dirVector[0], lawyerPos[1] + dirVector[1], lawyerPos[2] + dirVector[2] + 1.3)
            
            self.d_doAttack(lawyerPos[0], lawyerPos[1], lawyerPos[2], destPos[0], destPos[1], destPos[2] )

            #self.d_doAttack(lawyerPos[0], lawyerPos[1], lawyerPos[2], toonPos[0], toonPos[1], toonPos[2] )            

                
    def doProsecute(self):
        self.notify.debug("doProsecute")

        self.timeProsecuteStarted = globalClockDelta.getRealNetworkTime()
        
        self.d_doProsecute()
        #do the heal boss here
        taskName = self.uniqueName('ProsecutionHealsBoss')

        duration = 5.65 #derived from looking at throwing track duration in DistributedLawbotBossSuit
        taskMgr.doMethodLater(duration , self.__prosecutionHeal, taskName)

    def __prosecutionHeal(self, extraArg):
        self.notify.debug("__prosecutionHeal extraArg %s" % extraArg)
        if self.boss:
            self.boss.healBoss(ToontownGlobals.LawbotBossLawyerHeal)
        

    def d_doProsecute(self):
        self.notify.debug('d_doProsecute')
        self.sendUpdate('doProsecute',[])
        
    def d_doAttack(self, x1,y1,z1, x2,y2,z2):
        self.notify.debug("doAttack: x1=%.2f y1=%.2f z2=%.2f x2=%.2f y2=%.2f z2=%.2f" % (x1,y1,z1,x2,y2,z2))
        self.sendUpdate('doAttack', [x1, y1,z1,x2,y2,z2])

    def setBoss(self, lawbotBoss):
        self.boss = lawbotBoss

    def hitByToon(self):
        self.notify.debug("I got hit by a toon")
        if not self.stunned:
            #remove the task to heal the boss if we get hit before we throw the evidence
            curTime = globalClockDelta.getRealNetworkTime()
            deltaTime =  curTime - self.timeProsecuteStarted
            deltaTime /= 100.0 #convert milliseconds to seconds
            self.notify.debug('deltaTime = %f, curTime=%f, prosecuteStarted=%f' %
                              (deltaTime, curTime, self.timeProsecuteStarted))
            if deltaTime < self.timeToRelease:
                taskName = self.uniqueName('ProsecutionHealsBoss')            
                taskMgr.remove(taskName)
            
            self.sendUpdate('doStun',[])
            self.setStun(True)
            taskName = self.uniqueName('unstun')
            taskMgr.doMethodLater(ToontownGlobals.LawbotBossLawyerStunTime , self.unStun,taskName)
            if self.boss:
                self.boss.checkForBonusState()

    def setStun(self, val):
        self.stunned = val

    def unStun(self, taskName):
        self.setStun(False)



    def enterPreThrowProsecute(self):
        assert(self.notify.debug('enterPreThrowProsecute'))
        return

    def exitPreThrowProsecute(self):
        assert(self.notify.debug('exitPreThrowProsecute'))
        return
             
    def enterPostThrowProsecute(self):
        assert(self.notify.debug('enterPostThrowProsecute'))
        return

    def exitPostThrowProsecute(self):
        assert(self.notify.debug('exitPostThrowProsecute'))
        return
     
    def enterPreThrowAttack(self):
        assert(self.notify.debug('enterPreThrowAttack'))
        return

    def exitPreThrowAttack(self):
        assert(self.notify.debug('exitPreThrowAttack'))
        return
             
    def enterPostThrowAttack(self):
        assert(self.notify.debug('enterPostThrowAttack'))
        return

    def exitPostThrowAttack(self):
        assert(self.notify.debug('exitPostThrowAttack'))
        return

    def enterStunned(self):
        assert(self.notify.debug('enterStunned'))
        return
        
    def exitStunned(self):
        assert(self.notify.debug('exitStunned'))
        return

     
    def enterOff(self):
        assert(self.notify.debug('enterOff'))
        return
        
    def exitOff(self):
        assert(self.notify.debug('exitOff'))
        return

    def enterNeutral(self):
        assert(self.notify.debug('enterNeutral'))
        return
        
    def exitNeutral(self):
        assert(self.notify.debug('exitNeutral'))
        return
