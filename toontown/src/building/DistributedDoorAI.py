""" DistributedDoorAI module: contains the DistributedDoorAI
    class, the server side representation of a 'landmark door'."""


from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObjectAI
from direct.fsm import State
from toontown.toonbase import ToontownAccessAI

class DistributedDoorAI(DistributedObjectAI.DistributedObjectAI):
    """
    The server side representation of a single door.  This is the 
    object that remembers what the door is doing.  The client side
    version updates the client's display based on the state of the door.
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorAI')

    def __init__(self, air, blockNumber, doorType, doorIndex=0,
                 lockValue=0, swing=3):
        """
        blockNumber: the landmark building number (from the name)
        doorIndex: Each door must have a unique index.
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        assert(self.notify.debug(str(blockNumber)+" DistributedDoorAI("
                "%s, %s)" % ("the air", str(blockNumber))))
        self.block = blockNumber
        self.swing = swing
        self.otherDoor=None
        self.doorType = doorType
        self.doorIndex = doorIndex
        self.setDoorLock(lockValue)
        self.fsm = ClassicFSM.ClassicFSM('DistributedDoorAI_right',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['closing',
                                        'closed',
                                        'opening',
                                        'open']),
                            State.State('closing',
                                        self.enterClosing,
                                        self.exitClosing,
                                        ['closed', 'opening']),
                            State.State('closed',
                                        self.enterClosed,
                                        self.exitClosed,
                                        ['opening']),
                            State.State('opening',
                                        self.enterOpening,
                                        self.exitOpening,
                                        ['open']),
                            State.State('open',
                                        self.enterOpen,
                                        self.exitOpen,
                                        ['closing', 'open'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.fsm.enterInitialState()
        self.exitDoorFSM = ClassicFSM.ClassicFSM('DistributedDoorAI_left',
                           [State.State('off',
                                        self.exitDoorEnterOff,
                                        self.exitDoorExitOff,
                                        ['closing',
                                        'closed',
                                        'opening',
                                        'open']),
                            State.State('closing',
                                        self.exitDoorEnterClosing,
                                        self.exitDoorExitClosing,
                                        ['closed', 'opening']),
                            State.State('closed',
                                        self.exitDoorEnterClosed,
                                        self.exitDoorExitClosed,
                                        ['opening']),
                            State.State('opening',
                                        self.exitDoorEnterOpening,
                                        self.exitDoorExitOpening,
                                        ['open']),
                            State.State('open',
                                        self.exitDoorEnterOpen,
                                        self.exitDoorExitOpen,
                                        ['closing', 'open'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.exitDoorFSM.enterInitialState()
        self.doLaterTask=None
        self.exitDoorDoLaterTask=None
        self.avatarsWhoAreEntering={}
        self.avatarsWhoAreExiting={}

    def delete(self):
        assert(self.debugPrint("delete()"))
        taskMgr.remove(self.uniqueName('door_opening-timer'))
        taskMgr.remove(self.uniqueName('door_open-timer'))
        taskMgr.remove(self.uniqueName('door_closing-timer'))
        taskMgr.remove(self.uniqueName('exit_door_open-timer'))
        taskMgr.remove(self.uniqueName('exit_door_closing-timer'))
        taskMgr.remove(self.uniqueName('exit_door_opening-timer'))
        self.ignoreAll()
        del self.fsm
        del self.exitDoorFSM
        del self.otherDoor
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getDoorIndex(self):
        return self.doorIndex

    def setSwing(self, swing):
        self.swing = swing
    
    def getSwing(self):
        assert(self.debugPrint("getSwing()"))
        return self.swing

    def getDoorType(self):
        return self.doorType
    
    #def openDoor(self):
    #    """if the door is closed, open it"""
    #    assert(self.debugPrint("openDoor()"))
    #    if (self.isClosed()):
    #        self.fsm.request('opening')

    #def closeDoor(self):
    #    """if the door is open, close it"""
    #    assert(self.debugPrint("closeDoor()"))
    #    if (self.isOpen()):
    #        self.fsm.request('closing')
        
    def getZoneIdAndBlock(self):
        r=[self.zoneId, self.block]
        assert(self.debugPrint("getZoneIdAndBlock() returning: "+str(r)))
        return r
    
    def setOtherDoor(self, door):
        assert(self.debugPrint("setOtherDoor(door="+str(door)+")"))
        self.otherDoor=door
    
    def getZoneId(self):
        assert(self.debugPrint("getZoneId() returning "+str(self.zoneId)))
        return self.zoneId
    
    def getState(self):
        assert(self.debugPrint("getState()"))
        return [self.fsm.getCurrentState().getName(),
               globalClockDelta.getRealNetworkTime()]
    
    def getExitDoorState(self):
        assert(self.debugPrint("getExitDoorState()"))
        return [self.exitDoorFSM.getCurrentState().getName(), 
               globalClockDelta.getRealNetworkTime()]
    
    def isOpen(self):
        """return true if the door is open or opening"""
        assert(self.debugPrint("isOpen()"))
        state=self.fsm.getCurrentState().getName()
        return state=='open' or state=='opening'
    
    def isClosed(self):
        """return true if the door is closed, closing, or off"""
        assert(self.debugPrint("isClosed()"))
        return not self.isOpen()
    
    def setDoorLock(self, locked):
        """Prevent avatars from entering this door."""
        self.lockedDoor=locked
        
    def isLockedDoor(self):
        """Find out if the door is locked. 0 means no, positive values
        mean yes. Classes that inherit may attach special meanings to
        different positive values.

        NOTE: the cog hq doors don't seem to respect the no-locked-doors flag. """
        if simbase.config.GetBool('no-locked-doors', 0):
            return 0
        else:
            return self.lockedDoor

    def sendReject(self, avatarID, lockedVal):
        # Zero means the door is unlocked. Positive values mean
        # the door is locked. 
        # Classes that inherit from Distributed Door may
        # attach special meanings to different positive values.
        self.sendUpdateToAvatarId(avatarID, "rejectEnter", [lockedVal])
    
    def requestEnter(self):
        assert(self.debugPrint("requestEnter()"))
        avatarID = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("  avatarID:%s" % (str(avatarID),)))
        lockedVal = self.isLockedDoor()
        
        # Check that player has full access
        if not ToontownAccessAI.canAccess(avatarID, self.zoneId):
            lockedVal = True
            
        if lockedVal:
            self.sendReject(avatarID, lockedVal)
        else:
            self.enqueueAvatarIdEnter(avatarID)
            self.sendUpdateToAvatarId(avatarID, "setOtherZoneIdAndDoId", 
                    [self.otherDoor.getZoneId(), self.otherDoor.getDoId()])
    
    def enqueueAvatarIdEnter(self, avatarID):
        assert(self.debugPrint("enqueueAvatarIdEnter(avatarID=%s)"%(avatarID,)))
        assert(self.debugPrint("enqueueAvatarIdEnter(avatarsWhoAreEntering=%s)"%(self.avatarsWhoAreEntering,)))
        # By storing the avatarID in the key, we're creating a set of
        # unique avatarIDs.
        if not self.avatarsWhoAreEntering.has_key(avatarID):
            self.avatarsWhoAreEntering[avatarID]=1
            self.sendUpdate("avatarEnter", [avatarID])
        self.openDoor(self.fsm)
    
    def openDoor(self, doorFsm):
        assert(self.debugPrint("openTheDoor(doorFsm=)"))
        stateName = doorFsm.getCurrentState().getName()
        if stateName == 'open':
            # Reissue the open state:
            doorFsm.request('open')
        elif stateName != 'opening':
            doorFsm.request('opening')
    
    def requestExit(self):
        assert(self.debugPrint("requestExit()"))
        avatarID = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("  avatarID:%s" % (str(avatarID),)))

        # Make sure you send the avatar exit before telling the door to
        # open Otherwise the client will get the open door and will not be
        # on the list of avatars to walk through the door yet.
        self.sendUpdate("avatarExit", [avatarID])
        # Ok, now enqueue the avatar (which opens the door)
        self.enqueueAvatarIdExit(avatarID)
        
    def enqueueAvatarIdExit(self, avatarID):
        assert(self.debugPrint("enqueueAvatarIdExit(avatarID=%s)"%(avatarID,)))
        assert(self.debugPrint("enqueueAvatarIdExit(avatarsWhoAreExiting=%s)"%(self.avatarsWhoAreExiting,)))
        if self.avatarsWhoAreEntering.has_key(avatarID):
            del self.avatarsWhoAreEntering[avatarID]
        elif not self.avatarsWhoAreExiting.has_key(avatarID):
            self.avatarsWhoAreExiting[avatarID]=1
            self.openDoor(self.exitDoorFSM)
        else:
            assert(self.notify.debug(str(avatarID)
                    +" requested an exit, and they're already exiting"))
    
    def requestSuitEnter(self, avatarID):
        """
        unlike requestEnter(), which is for toons, this is not a
        distributed call; it's made directly from the AI side as the
        suit reaches the end of its path.
        """
        assert(self.debugPrint("requestSuitEnter(avatarID=%s" % (avatarID,)))
        self.enqueueAvatarIdEnter(avatarID)
    
    def requestSuitExit(self, avatarID):
        """
        unlike requestExit(), which is for toons, this is not a
        distributed call; it's made directly from the AI side as the
        suit reaches the end of its path.
        """
        assert(self.debugPrint("requestSuitExit(avatarID=%s" % (avatarID,)))
        # Send the avatar exit first
        self.sendUpdate("avatarExit", [avatarID])
        # Then open the door
        self.enqueueAvatarIdExit(avatarID)
    
    def d_setState(self, state):
        assert(self.debugPrint("d_setState(state="+str(state)+")"))
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])
    
    def d_setExitDoorState(self, state):
        assert(self.debugPrint("d_setExitDoorState(state="+str(state)+")"))
        self.sendUpdate('setExitDoorState', [state, globalClockDelta.getRealNetworkTime()])
    
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('block', '?'))+' '+message)
    
    ##### off state #####
    
    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
    
    def exitOff(self):
        assert(self.debugPrint("exitOff()"))
    
    ##### closing state #####

    def openTask(self, task):
        assert(self.debugPrint("openTask()"))
        self.fsm.request("closing")
        return Task.done
    
    def enterClosing(self):
        assert(self.debugPrint("enterClosing()"))
        self.d_setState('closing')
        self.doLaterTask=taskMgr.doMethodLater(
            1, #CLOSING_DOOR_TIME,    #TODO: define this elsewhere
            self.closingTask,
            self.uniqueName('door_closing-timer'))
    
    def exitClosing(self):
        assert(self.debugPrint("exitClosing()"))
        if self.doLaterTask:
            taskMgr.remove(self.doLaterTask)
            self.doLaterTask=None
    
    ##### closed state #####

    def closingTask(self, task):
        assert(self.debugPrint("closingTask()"))
        self.fsm.request("closed")
        return Task.done
    
    def enterClosed(self):
        assert(self.debugPrint("enterClosed()"))
        self.d_setState('closed')
    
    def exitClosed(self):
        assert(self.debugPrint("exitClosed()"))
    
    ##### opening state #####
    
    def enterOpening(self):
        assert(self.debugPrint("enterOpening()"))
        self.d_setState('opening')
        self.doLaterTask=taskMgr.doMethodLater(
            1, #OPENING_DOOR_TIME,
            #todo: define OPENING_DOOR_TIME elsewhere
            self.openingTask,
            self.uniqueName('door_opening-timer'))
    
    def exitOpening(self):
        assert(self.debugPrint("exitOpening()"))
        if self.doLaterTask:
            taskMgr.remove(self.doLaterTask)
            self.doLaterTask=None
    
    ##### open state #####

    def openingTask(self, task):
        assert(self.debugPrint("openingTask()"))
        self.fsm.request("open")
        return Task.done
    
    def enterOpen(self):
        assert(self.debugPrint("enterOpen()"))
        self.d_setState('open')
        self.avatarsWhoAreEntering={}
        self.doLaterTask=taskMgr.doMethodLater(
            1, #STAY_OPEN_DOOR_TIME,
            #todo: define STAY_OPEN_DOOR_TIME elsewhere
            self.openTask,
            self.uniqueName('door_open-timer'))
    
    def exitOpen(self):
        assert(self.debugPrint("exitOpen()"))
        if self.doLaterTask:
            taskMgr.remove(self.doLaterTask)
            self.doLaterTask=None

    
    ##### Exit Door off state #####
    
    def exitDoorEnterOff(self):
        assert(self.debugPrint("exitDoorEnterOff()"))
    
    def exitDoorExitOff(self):
        assert(self.debugPrint("exitDoorExitOff()"))
    
    ##### Exit Door closing state #####

    def exitDoorOpenTask(self, task):
        assert(self.debugPrint("exitDoorOpenTask()"))
        self.exitDoorFSM.request("closing")
        return Task.done
    
    def exitDoorEnterClosing(self):
        assert(self.debugPrint("exitDoorEnterClosing()"))
        self.d_setExitDoorState('closing')
        self.exitDoorDoLaterTask=taskMgr.doMethodLater(
            1, #CLOSING_DOOR_TIME,    #TODO: define this elsewhere
            self.exitDoorClosingTask,
            self.uniqueName('exit_door_closing-timer'))
    
    def exitDoorExitClosing(self):
        assert(self.debugPrint("exitDoorExitClosing()"))
        if self.exitDoorDoLaterTask:
            taskMgr.remove(self.exitDoorDoLaterTask)
            self.exitDoorDoLaterTask=None
    
    ##### Exit Door closed state #####

    def exitDoorClosingTask(self, task):
        assert(self.debugPrint("exitDoorClosingTask()"))
        self.exitDoorFSM.request("closed")
        return Task.done
    
    def exitDoorEnterClosed(self):
        assert(self.debugPrint("exitDoorEnterClosed()"))
        self.d_setExitDoorState('closed')
    
    def exitDoorExitClosed(self):
        assert(self.debugPrint("exitDoorExitClosed()"))
        if self.exitDoorDoLaterTask:
            taskMgr.remove(self.exitDoorDoLaterTask)
            self.exitDoorDoLaterTask=None
    
    ##### Exit Door opening state #####
    
    def exitDoorEnterOpening(self):
        assert(self.debugPrint("exitDoorEnterOpening()"))
        self.d_setExitDoorState('opening')
        self.exitDoorDoLaterTask=taskMgr.doMethodLater(
            1, #OPENING_DOOR_TIME,
            #todo: define OPENING_DOOR_TIME elsewhere
            self.exitDoorOpeningTask,
            self.uniqueName('exit_door_opening-timer'))
    
    def exitDoorExitOpening(self):
        assert(self.debugPrint("exitDoorExitOpening()"))
        if self.exitDoorDoLaterTask:
            taskMgr.remove(self.exitDoorDoLaterTask)
            self.exitDoorDoLaterTask=None
    
    ##### Exit Door open state #####

    def exitDoorOpeningTask(self, task):
        assert(self.debugPrint("exitDoorOpeningTask()"))
        self.exitDoorFSM.request("open")
        return Task.done
    
    def exitDoorEnterOpen(self):
        assert(self.debugPrint("exitDoorEnterOpen()"))
        # Tell the clients:
        self.d_setExitDoorState('open')
        self.avatarsWhoAreExiting={}
        # Stay open for a little while:
        self.exitDoorDoLaterTask=taskMgr.doMethodLater(
            1, #STAY_OPEN_DOOR_TIME,
            #todo: define STAY_OPEN_DOOR_TIME elsewhere
            self.exitDoorOpenTask,
            self.uniqueName('exit_door_open-timer'))
    
    def exitDoorExitOpen(self):
        assert(self.debugPrint("exitDoorExitOpen()"))
        if self.exitDoorDoLaterTask:
            taskMgr.remove(self.exitDoorDoLaterTask)
            self.exitDoorDoLaterTask=None

