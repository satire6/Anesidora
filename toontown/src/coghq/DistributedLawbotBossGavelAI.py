from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM

class DistributedLawbotBossGavelAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM):

    """ This is one of the  gavels in the lawbot
    boss battle room.  """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBossGavelAI')


    def __init__(self, air, boss, index):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedLawbotBossGavelAI')

        self.boss = boss
        self.index = index

        # A collision bubble to discourage the goons from walking
        # through the control area.
        cn = CollisionNode('controls')
        cs = CollisionSphere(0, -6, 0, 6)
        cn.addSolid(cs)
        self.goonShield = NodePath(cn)
        self.goonShield.setPosHpr(*ToontownGlobals.LawbotBossGavelPosHprs[self.index])

        self.avId = 0
        self.objectId = 0

    def getBossCogId(self):
        return self.boss.doId

    def getIndex(self):
        return self.index

    def setState(self, state):
        self.request(state)
    
    def d_setState(self, state):
        newState = state
        if state == 'On':
            newState = 'N'
        elif state == 'Off':
            newState = 'F'
        else:
            assert(self.notify.error("Unknown state %s", state))
        
        self.sendUpdate('setState', [newState])

    def b_setState(self, state):
        self.request(state)
        self.d_setState( state) 
    

    def turnOn(self):
        #we've entered battle three so start stomping
        self.b_setState('On')
    

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
