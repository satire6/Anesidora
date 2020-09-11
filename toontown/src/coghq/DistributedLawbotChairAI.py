from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM
import random

class DistributedLawbotChairAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM):

    """ This is one of the  chairs in the lawbot
    boss battle room.  """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotChairAI')


    def __init__(self, air, boss, index):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedLawbotBossChairAI')

        self.boss = boss
        self.index = index

        # A collision bubble to discourage the goons from walking
        # through the control area.
        cn = CollisionNode('controls')
        cs = CollisionSphere(0, -6, 0, 6)
        cn.addSolid(cs)
        self.goonShield = NodePath(cn)
        self.goonShield.setPosHpr(*ToontownGlobals.LawbotBossChairPosHprs[self.index])

        self.avId = 0
        self.objectId = 0

        self.changeToCogTask = None
        self.startCogFlyTask = None

        #zero or higher if there is a toon Juror on this chair
        self.toonJurorIndex = -1

    def delete(self):
        assert self.notify.debug('delete')
        self.ignoreAll()
        #self.__stopTimeout()
        DistributedObjectAI.DistributedObjectAI.delete(self)

        taskName = self.uniqueName('startCogFlyTask')
        taskMgr.remove(taskName)

        changeTaskName = self.uniqueName('changeToCogJuror')
        taskMgr.remove(changeTaskName)

    def stopCogs(self):
        assert self.notify.debug('stopCogs')
 
        #self.ignoreAll()
        taskName = self.uniqueName('startCogFlyTask')
        taskMgr.remove(taskName)

        changeTaskName = self.uniqueName('changeToCogJuror')
        taskMgr.remove(changeTaskName)
        

    def getBossCogId(self):
        return self.boss.doId

    def getIndex(self):
        return self.index

    def getToonJurorIndex(self):
        return self.toonJurorIndex

    def setToonJurorIndex(self, newVal):
        self.toonJurorIndex = newVal

    def b_setToonJurorIndex(self, newVal):
        self.setToonJurorIndex(newVal)
        self.d_setToonJurorIndex(newVal)

    def d_setToonJurorIndex(self, newVal):
        self.sendUpdate('setToonJurorIndex', [newVal])

    def setState(self, state):
        self.request(state)
     
    def d_setState(self, state):
        newState = state
        if state == 'On':
            newState = 'N'
        elif state == 'Off':
            newState = 'F'
        elif state == 'ToonJuror':
            newState = 'T'
        elif state == 'SuitJuror':
            newState = 'S'
        elif state == 'EmptyJuror':
            newState ='E'
        elif state == 'StopCogs':
            newState ='C'
        else:
            assert(self.notify.error("Unknown state %s", state))
        
        self.sendUpdate('setState', [newState])

    def b_setState(self, state):
        self.request(state)
        self.d_setState( state) 
    

    def turnOn(self):
        #we've entered battle three so start stomping
        self.b_setState('On')

    def requestStopCogs(self):
        self.b_setState('StopCogs')  


    def requestControl(self):
        # A client wants to start controlling the crane.
        avId = self.air.getAvatarIdFromSender()
        
        if avId in self.boss.involvedToons and self.avId == 0:
            # Also make sure the client isn't controlling some other
            # crane.
            craneId = self.__getCraneId(avId)
            if craneId == 0:
                self.request('Controlled', avId)

    def requestFree(self):
        # The client is done controlling the crane.
        avId = self.air.getAvatarIdFromSender()
        
        if avId == self.avId:
            self.request('Free')
    
    def removeToon(self, avId):
        if avId == self.avId:
            self.request('Free')

    def __getCraneId(self, avId):
        # Returns the craneId for the crane that the indicated avatar
        # is controlling, or 0 if none.

        if self.boss and self.boss.cranes != None:
            for crane in self.boss.cranes:
                if crane.avId == avId:
                    return crane.doId

        return 0

    def requestToonJuror(self):
        self.b_setState('ToonJuror')
        if self.changeToCogTask == None:
            #this means no cog flying down to sit
            if (self.startCogFlyTask ==None):
                #avoid the case players are so good they
                #hit the chair before the first cog gets there

                #give a little delay before the cog appears
                delayTime = random.randrange(9,19)
                self.startCogFlyTask = taskMgr.doMethodLater(\
                    delayTime,
                    self.cogFlyAndSit,
                    self.uniqueName('startCogFlyTask'))                

        

    def requestSuitJuror(self):
        self.b_setState('SuitJuror')        

    def requestEmptyJuror(self):
        self.b_setState('EmptyJuror')
        #since this is the first thing that happens start the cogs flying
        delayTime = random.randrange(1,20)
        self.startCogFlyTask = taskMgr.doMethodLater(delayTime,
                                                     self.cogFlyAndSit,
                                                     self.uniqueName('startCogFlyTask'))
        #self.cogFlyAndSit()

    def cogFlyAndSit(self, taskName = None):
        self.notify.debug('cogFlyAndSit')
        self.sendUpdate('showCogJurorFlying',[])
        self.changeToCogTask = taskMgr.doMethodLater(
            ToontownGlobals.LawbotBossCogJurorFlightTime,
            self.changeToCogJuror,
            self.uniqueName('changeToCogJuror')
            )
        if self.startCogFlyTask:
            self.startCogFlyTask = None

    def changeToCogJuror(self, task):
        self.notify.debug('changeToCogJuror')
        self.requestSuitJuror()
        self.changeToCogTask = None


    ### FSM States ###
    def enterOn(self):
        pass

    def exitOn(slef):
        pass

    def enterOff(self):
        self.goonShield.detachNode()

    def exitOff(self):
        pass
        #no Scene    
        #self.goonShield.reparentTo(self.boss.scene)

    def enterControlled(self, avId):
        self.avId = avId
        self.d_setState('C')

    def exitControlled(self):
        if self.objectId:
            # This will be filled in if an object has requested a
            # grab.  In this case, drop the object.
            obj = self.air.doId2do[self.objectId]
            obj.request('Dropped', self.avId, self.doId)

    def enterFree(self):
        self.avId = 0
        self.d_setState('F')

    def exitFree(self):
        pass

    def enterToonJuror(self):
        pass

    def exitToonJuror(self):
        pass

    def enterStopCogs(self):
        self.__stopCogs()

    def exitStopCogs(self):
        assert self.notify.debug('exitStopCogs, oldState=%s' % self.oldState)
        pass
