from pandac.PandaModules import *
from direct.distributed import DistributedSmoothNodeAI
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM
from direct.task import Task

class DistributedCashbotBossObjectAI(DistributedSmoothNodeAI.DistributedSmoothNodeAI, FSM.FSM):

    """ This is an object that can be picked up an dropped in the
    final battle scene with the Cashbot CFO.  In particular, it's a
    safe or a goon.  """

    # This should be true for objects that will eventually transition
    # from SlidingFloor to Free when they stop moving.
    wantsWatchDrift = 1

    def __init__(self, air, boss):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedCashbotBossObjectAI')

        self.boss = boss

        # Put ourselves in the boss's scene for collision detection.
        self.reparentTo(self.boss.scene)

        # A CashbotBossObject may be in one of three states:
        #   uncontrolled by a client (or self-controlled)
        #   stuck to a magnet, controlled by a client
        #   in free-fall, controlled by a client

        self.avId = 0
        self.craneId = 0

    def cleanup(self):
        self.detachNode()
        self.stopWaitFree()

    def delete(self):
        self.cleanup()
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)

    def startWaitFree(self, delayTime):
        # Waits a certain amount of time, then automatically
        # transitions to 'Free' state.  The amount of time to wait
        # depends on what state we started in.
        waitFreeEvent = self.uniqueName('waitFree')
        taskMgr.remove(waitFreeEvent)
        taskMgr.doMethodLater(delayTime, self.doFree, waitFreeEvent)

    def stopWaitFree(self):
        # Interrupts the waiting started by a previous call to
        # startWaitFree().
        waitFreeEvent = self.uniqueName('waitFree')
        taskMgr.remove(waitFreeEvent)
        

    def doFree(self, task):
        # This method is fired as a do-later when we enter WaitFree.
        if not self.isDeleted():
            self.demand('Free')
            p = self.getPos()
            h = self.getH()
            self.d_setPosHpr(p[0], p[1], 0, h, 0, 0)
        return Task.done

    ### Messages ###

    def getBossCogId(self):
        return self.boss.doId

    def d_setObjectState(self, state, avId, craneId):
        self.sendUpdate('setObjectState', [state, avId, craneId])

    def requestGrab(self):
        # A client wants to pick up the object with his magnet.
        avId = self.air.getAvatarIdFromSender()

        if self.state != 'Grabbed' and self.state != 'Off':
            # Also make sure the client is controlling some crane and
            # hasn't grabbed some other object already.
            craneId, objectId = self.__getCraneAndObject(avId)
            if craneId != 0 and objectId == 0:
                self.demand('Grabbed', avId, craneId)
                return

        # The client can't have it.
        self.sendUpdateToAvatarId(avId, 'rejectGrab', [])

    def requestDrop(self):
        # The client holding the object has dropped it from his magnet
        # (but is still controlling its free-fall).
        avId = self.air.getAvatarIdFromSender()

        if avId == self.avId and self.state == 'Grabbed':
            craneId, objectId = self.__getCraneAndObject(avId)
            if craneId != 0 and objectId == self.doId:
                self.demand('Dropped', avId, craneId)

    def hitFloor(self):
        # The client managing the dropping object tells us that it has
        # just struck the floor.
        avId = self.air.getAvatarIdFromSender()

        if avId == self.avId and self.state == 'Dropped':
            self.demand('SlidingFloor', avId)


    def requestFree(self, x, y, z, h):
        # The client controlling the object's free-fall has
        # relinquished all control of it.
        avId = self.air.getAvatarIdFromSender()
        
        if avId == self.avId:
            self.setPosHpr(x, y, 0, h, 0, 0)
            self.demand('WaitFree')

    def hitBoss(self, impact):
        # The client reports successfully striking the boss in the
        # head with this object.
        pass

    def removeToon(self, avId):
        # Elvis has left the building.
        if avId == self.avId:
            self.doFree(None)
            

    def __getCraneAndObject(self, avId):
        # Returns the pair (craneId, objectId) representing the crane
        # that the indicated avatar is controlling, or 0 if none, and
        # the object currently held by that crane's magnet, or 0 if
        # none.  If the object is in Dropped state, it is not listed
        # here.

        if self.boss and self.boss.cranes != None:
            for crane in self.boss.cranes:
                if crane.avId == avId:
                    return (crane.doId, crane.objectId)

        return (0, 0)

    def __setCraneObject(self, craneId, objectId):
        # Marks the indicated crane as having grabbed the indicated
        # object.  An objectId of 0 indicates the crane holds nothing.

        if self.air:
            crane = self.air.doId2do.get(craneId)
            if crane:
                crane.objectId = objectId

    ### FSM States ###

    def enterGrabbed(self, avId, craneId):
        self.avId = avId
        self.craneId = craneId
        self.__setCraneObject(self.craneId, self.doId)
        self.d_setObjectState('G', avId, craneId)

    def exitGrabbed(self):
        self.__setCraneObject(self.craneId, 0)

    def enterDropped(self, avId, craneId):
        self.avId = avId
        self.craneId = craneId
        self.d_setObjectState('D', avId, craneId)
        self.startWaitFree(10)

    def exitDropped(self):
        self.stopWaitFree()
    
    def enterSlidingFloor(self, avId):
        self.avId = avId
        self.d_setObjectState('s', avId, 0)
        if self.wantsWatchDrift:
            self.startWaitFree(5)

    def exitSlidingFloor(self):
        self.stopWaitFree()
    
    def enterWaitFree(self):
        # In this state, we have been asked by the controlling user to
        # free the object.  We will, in just a little bit, but we wait
        # half a second first to give the distributed users a chance
        # to see the object slide to its completion first.  This state
        # is not distributed.
        
        self.avId = 0
        self.craneId = 0

        self.startWaitFree(1)

    def exitWaitFree(self):
        self.stopWaitFree()

    def enterFree(self):
        # The object is finally restored to its resting state.
        
        self.avId = 0
        self.craneId = 0
        self.d_setObjectState('F', 0, 0)

    def exitFree(self):
        pass
