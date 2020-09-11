

from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
import DistributedDoorEntityBase
from direct.distributed import DistributedObjectAI
from otp.level import DistributedEntityAI
from direct.fsm import FourStateAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task


class Lock(DistributedDoorEntityBase.LockBase,
           DirectObject.DirectObject, FourStateAI.FourStateAI):
    """
    The Lock is not distributed itself, instead it relies on the door
    to get messages and state changes to and from the client.
    
    This was a nested class in DistributedDoorEntity, but the class 
    reloader that I'm using doesn't work with nested classes.  Until
    that gets changed I've moved this here.
    """

    def __init__(self, door, lockIndex, event, isUnlocked):
        self.door = door
        self.lockIndex = lockIndex
        assert(self.debugPrint(
                "Lock(door=%s, lockIndex=%s, event=%s, isUnlocked=%s)"%
                (door, lockIndex, event, isUnlocked)))
        FourStateAI.FourStateAI.__init__(
                self, self.stateNames, durations = self.stateDurations)
        self.unlockEvent = None
        self.setUnlockEvent(event)
        self.setIsUnlocked(isUnlocked)

    def getLockState(self):
        assert(self.debugPrint("getLockState() returning %s"%(self.stateIndex,)))
        assert 0 <= self.stateIndex <= 4
        return self.stateIndex
        
    def setup(self):
        assert(self.debugPrint("takedown()"))
        pass

    def takedown(self):
        assert(self.debugPrint("takedown()"))
        self.ignoreAll()
        FourStateAI.FourStateAI.delete(self)
        del self.door

    def setUnlockEvent(self, event):
        assert(self.debugPrint("setUnlockEvent(event=%s)"%(event,)))
        if self.unlockEvent:
            self.ignore(self.unlockEvent)
        self.unlockEvent = self.door.getOutputEventName(event)
        if self.unlockEvent:
            self.accept(self.unlockEvent, self.setIsUnlocked)

    def distributeStateChange(self):
        """
        Overide FourState base class.
        """
        self.door.sendLocksState()

    def setIsUnlocked(self, isUnlocked):
        assert(self.debugPrint("setIsUnlocked(isUnlocked=%s)"%(isUnlocked,)))
        self.setIsOn(isUnlocked)
        if not isUnlocked:
            # if the door is locking then close the door:
            self.door.locking()
        # locks don't announce their state change: messenger.send(...)

    def setLockState(self, stateIndex):
        assert(self.debugPrint("setLockState(stateIndex=%s)"%(stateIndex,)))
        assert 0 <= self.stateIndex <= 4
        if self.stateIndex!=stateIndex:
            self.fsm.request(self.states[stateIndex])

    def isUnlocked(self):
        assert(self.debugPrint("isUnlocked() returning %s"%(self.isOn(),)))
        return self.isOn()

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.door.notify.debug(
                    "%s (%s) %s"%(self.door.__dict__.get('entId', '?'), 
                                self.lockIndex, 
                                message))



class DistributedDoorEntityAI(
        DistributedDoorEntityBase.DistributedDoorEntityBase,
        DistributedEntityAI.DistributedEntityAI, FourStateAI.FourStateAI):
    """
    DistributedDoorEntityAI class:  The server side representation
    of a Cog HQ door.  This is the object that remembers what the
    door is doing.  The DistributedLockableDoor, is the client side
    version.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedDoorEntityAI')

    def __init__(self, level, entId, zoneId=None):
        """
        level is <what is a level>
        entId is an Entity ID (int).
        zoneId is an int.
        """
        self.entId = entId # used in debugPrint.
        assert(self.debugPrint(
                "DistributedDoorEntityAI(levelDoId=%s, entId=%s, zoneId=%s)"
                %(level.doId, entId, zoneId)))
        # don't overwrite isGenerated()
        self._isGenerated=0
        self.isOpenInput = None
        DistributedEntityAI.DistributedEntityAI.__init__(
                self, level, entId)
        self.stateDurations[2] = self.secondsOpen
        FourStateAI.FourStateAI.__init__(
                self, self.stateNames, durations = self.stateDurations)
        self.setup()
        if zoneId is not None:
            self.generateWithRequired(zoneId)
    
    def generateWithRequired(self, zoneId):
        assert(self.debugPrint("generateWithRequired(zoneId=%s)"%(zoneId,)))
        DistributedEntityAI.DistributedEntityAI.generateWithRequired(self, zoneId)
        self._isGenerated=1

    def delete(self):
        assert(self.debugPrint("delete()"))
        self.takedown()
        FourStateAI.FourStateAI.delete(self)
        DistributedEntityAI.DistributedEntityAI.delete(self)
    
    def getLocksState(self):
        """
        returns stateBits:
            15 through 12: lock 3 state
            11 through  8: lock 2 state
             7 through  4: lock 1 state
             3 through  0: lock 0 state

        Get the state for all four locks.
        Required dc field.
        """
        stateBits = 0x00000000
        
        if hasattr(self, 'locks'): #hack for the editor JML
            stateBits = (
                  ((self.locks[0].getLockState()      ) & 0x0000000f)
                | ((self.locks[1].getLockState() <<  4) & 0x000000f0)
                | ((self.locks[2].getLockState() <<  8) & 0x00000f00)
                #| ((self.locks[3].getLockState() << 12) & 0x0000f000) # fourth lock not yet used.
                )
        assert(self.debugPrint("getLocksState() returning 0x%x"%(stateBits)))
        return stateBits
    
    def sendLocksState(self):
        assert(self.debugPrint("sendLocksState()"))
        if self._isGenerated:
            self.sendUpdate('setLocksState', [self.getLocksState()])
    
    def getDoorState(self):
        """
        Required dc field.
        """
        r = (self.stateIndex, globalClockDelta.getRealNetworkTime())
        assert(self.debugPrint("getDoorState() returning %s"%(r,)))
        return r
    
    def getName(self):
        return "door-%s"%(self.entId,)
    
    def setup(self):
        assert(self.debugPrint("setup()"))
        
        #hack to make this sucker not break the editor JML
        if not hasattr(self, 'unlock0Event'):
            self.unlock0Event = None
        if not hasattr(self, 'unlock1Event'):
            self.unlock1Event = None
        if not hasattr(self, 'unlock2Event'):
            self.unlock2Event = None
        if not hasattr(self, 'unlock3Event'):
            self.unlock3Event = None
        if not hasattr(self, 'isLock0Unlocked'):
            self.isLock0Unlocked = None
        if not hasattr(self, 'isLock1Unlocked'):
            self.isLock1Unlocked = None
        if not hasattr(self, 'isLock2Unlocked'):
            self.isLock2Unlocked = None
        if not hasattr(self, 'isLock3Unlocked'):
            self.isLock3Unlocked = None
            
        self.locks = [
                Lock(self, 0, self.unlock0Event, self.isLock0Unlocked),
                Lock(self, 1, self.unlock1Event, self.isLock1Unlocked),
                Lock(self, 2, self.unlock2Event, self.isLock2Unlocked),
                #Lock(self, 3, self.unlock3Event, self.isLock3Unlocked), # fourth lock not yet used.
                ]
        del self.unlock0Event
        del self.unlock1Event
        del self.unlock2Event
        del self.unlock3Event
        del self.isLock0Unlocked
        del self.isLock1Unlocked
        del self.isLock2Unlocked
        del self.isLock3Unlocked
        if hasattr(self, 'isOpenEvent'):
            self.setIsOpenEvent(self.isOpenEvent)
            del self.isOpenEvent
        if hasattr(self, 'isOpen'):
            self.setIsOpen(self.isOpen)
            del self.isOpen
        
    def takedown(self):
        assert(self.debugPrint("takedown()"))
        self.ignoreAll()
        for i in self.locks:
            i.takedown()
        del self.locks
        
    # These stubbed out functions are not used on the AI (Client Only):
    setScale = DistributedDoorEntityBase.stubFunction
    setColor = DistributedDoorEntityBase.stubFunction
    setModel = DistributedDoorEntityBase.stubFunction
   
    def setIsOpenEvent(self, event):
        assert(self.debugPrint("setIsOpenEvent(event=%s)"%(event,)))
        if self.isOpenEvent:
            self.ignore(self.isOpenEvent)
        self.isOpenEvent = self.getOutputEventName(event)
        if self.isOpenEvent:
            self.accept(self.isOpenEvent, self.setIsOpen)

    def changedOnState(self, isOn):
        assert(self.debugPrint("changedOnState(isOn=%s)"%(isOn,)))
        if hasattr(self, "entId"):
            # The open state is the inverse of the FourState's On value.
            messenger.send(self.getOutputEventName(), [not isOn])
        # else, we're being deleted, ignore the change (do not send message).
    
    def setIsOpen(self, isOpen):
        assert(self.debugPrint("setIsOpen(isOpen=%s)"%(isOpen,)))
        # The open state is the inverse of the FourState's On value.
        self.setIsOn(not isOpen)
    
    def getIsOpen(self):
        assert(self.debugPrint("getIsOpen() returning %s"%(not self.getIsOn(),)))
        # The open state is the inverse of the FourState's On value.
        return not self.getIsOn()
    
    def setSecondsOpen(self, secondsOpen):
        assert(self.debugPrint("setSecondsOpen(secondsOpen=%s)"%(secondsOpen,)))
        if self.secondsOpen != secondsOpen:
            self.secondsOpen = secondsOpen
            if secondsOpen < 0.0:
                secondsOpen = None
            self.stateDurations[2] = secondsOpen
    #        if self.isOpen:
    #            if self.doLaterTask:
    #                self.doLaterTask.remove()
    #                self.doLaterTask = None
    #            if self.secondsOpen >= 0.0:
    #                assert(self.doLaterTask==None)
    #                self.doLaterTask=taskMgr.doMethodLater(
    #                        self.secondsOpen,
    #                        self.closeDoorTask,
    #                        self.uniqueName('door-entity-timer'))

    #def closeDoorTask(self, task):
    #    assert(self.debugPrint("closeDoorTask()"))
    #    self.setIsOpen(0)
    #    self.fsm.request(self.states[3])
    #    return Task.done

    def locking(self):
        """
        The locks for this door call this function when they are locking
        or locked.
        """
        if self.stateIndex == 1 or self.stateIndex == 2:
            # ...the door is opening or open.
            # We should close this door.
            # Request closing:
            self.fsm.request(self.states[3])
        # else:  This door is already closing or closed.

    ##### locks #####
    
    def setUnlock0Event(self, event):
        assert(self.debugPrint("setUnlock0Event(event=%s)"%(event,)))
        self.locks[0].setUnlockEvent(event)
    
    def setUnlock1Event(self, event):
        assert(self.debugPrint("setUnlock1Event(event=%s)"%(event,)))
        self.locks[1].setUnlockEvent(event)
    
    def setUnlock2Event(self, event):
        assert(self.debugPrint("setUnlock2Event(event=%s)"%(event,)))
        self.locks[2].setUnlockEvent(event)
    
    def setUnlock3Event(self, event):
        assert(self.debugPrint("setUnlock3Event(event=%s)"%(event,)))
        #self.locks[3].setUnlockEvent(event) # fourth lock not yet used.
    
    def setIsLock0Unlocked(self, unlocked):
        assert(self.debugPrint("setIsLock0Unlocked(unlocked=%s)"%(unlocked,)))
        self.locks[0].setIsUnlocked(unlocked)
    
    def setIsLock1Unlocked(self, unlocked):
        assert(self.debugPrint("setIsLock1Unlocked(unlocked=%s)"%(unlocked,)))
        self.locks[1].setIsUnlocked(unlocked)
    
    def setIsLock2Unlocked(self, unlocked):
        assert(self.debugPrint("setIsLock2Unlocked(unlocked=%s)"%(unlocked,)))
        self.locks[2].setIsUnlocked(unlocked)
    
    def setIsLock3Unlocked(self, unlocked):
        assert(self.debugPrint("setIsLock3Unlocked(unlocked=%s)"%(unlocked,)))
        #self.locks[3].setIsUnlocked(unlocked) # fourth lock not yet used.

    ##### states #####
    
    def isUnlocked(self):
        """
        Check with each lock and return true if they are all unlocked.
        returns boolean.
        """
        isUnlocked = (
            self.locks[0].isUnlocked()
            and self.locks[1].isUnlocked() 
            and self.locks[2].isUnlocked()
            #and self.locks[3].isUnlocked() # fourth lock not yet used.
            )
        assert(self.debugPrint("isUnlocked() returning %s"%(isUnlocked,)))
        return isUnlocked

    def distributeStateChange(self):
        if self._isGenerated:
            self.sendUpdate('setDoorState', self.getDoorState())
    
    def requestOpen(self):
        assert(self.debugPrint("requestOpen() ...checking locks"))
        if self.isUnlocked():
            assert(self.notify.debug("  avatarId:%s"%(self.air.getAvatarIdFromSender(),)))
            #stateName = self.fsm.getCurrentState().getName()
            if self.fsm.getCurrentState() is not self.states[2]:
                # ...the door is not open.
                # Request the opening state:
                self.fsm.request(self.states[1])
            #else:
            #    self.sendUpdateToAvatarId(avatarId, "rejectInteract", [])
        else:
            # ...the door is locked.
            assert(self.debugPrint("requestOpen() ...locked"))
            #avatarId = self.air.getAvatarIdFromSender()
            #self.sendUpdateToAvatarId(avatarId, "rejectInteract", [])

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('entId', '?'))+' '+message)

    if __dev__:
        def attribChanged(self, attrib, value):
            self.takedown()
            self.setup()

