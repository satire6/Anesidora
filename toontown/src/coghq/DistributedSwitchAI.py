
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
import DistributedSwitchBase
from direct.task import Task
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from otp.level import DistributedEntityAI


class DistributedSwitchAI(
        DistributedSwitchBase.DistributedSwitchBase,
        DistributedEntityAI.DistributedEntityAI):
    """
    DistributedSwitchAI class:  The server side representation
    of a Cog HQ switch.  This is the object that remembers what the
    switch is doing.  The DistributedSwitch, is the client side
    version.

    model:
      The name of the model to load.
    secondsOn:
      How long the switch will stay on after it has been switched.
      -1.0 means that the switch doesn't switch off again.
      0.0 and up mean that the switch will switch off after that
      many seconds.  Other values are not valid.
    initialState:
      Set the default (i.e. starting) state: 0 == off, 1 == on.
    
    See Also: DistributedSwitch
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedSwitchAI')

    def __init__(self, level, entId, zoneId=None):
        """spec: """
        assert(self.debugPrint(
                "DistributedSwitchAI(levelDoId=%s, entId=%s, zoneId=%s)"
                %(level.doId, entId, zoneId)))
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)
        self.fsm = ClassicFSM.ClassicFSM('DistributedSwitch',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['playing']),
                            # Attract is an idle mode.  It is named attract
                            # because the prop is not interacting with an
                            # avatar, and is therefore trying to attract an
                            # avatar.
                            State.State('attract',
                                        self.enterAttract,
                                        self.exitAttract,
                                        ['playing']),
                            # Playing is for when an avatar is interacting
                            # with the prop.
                            State.State('playing',
                                        self.enterPlaying,
                                        self.exitPlaying,
                                        ['attract'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.fsm.enterInitialState()
        self.avatarId=0
        self.doLaterTask = None
        if zoneId is not None:
            self.generateWithRequired(zoneId)

    def setup(self):
        pass
        
    def takedown(self):
        pass
        
    # These stubbed out functions are not used on the AI (Client Only):
    setScale = DistributedSwitchBase.stubFunction
  
    def delete(self):
        assert(self.debugPrint("delete()"))
        if self.doLaterTask:
            self.doLaterTask.remove()
            self.doLaterTask=None
        del self.fsm
        DistributedEntityAI.DistributedEntityAI.delete(self)
    
    def getAvatarInteract(self):
        assert(self.debugPrint("getAvatarInteract() returning: %s"%(self.avatarId,)))
        return self.avatarId
    
    def getState(self):
        r = [
            self.fsm.getCurrentState().getName(),
            globalClockDelta.getRealNetworkTime()]
        assert(self.debugPrint("getState() returning %s"%(r,)))
        return r
    
    def sendState(self):
        assert(self.debugPrint("sendState()"))
        self.sendUpdate('setState', self.getState())
    
    def setIsOn(self, isOn):
        assert(self.debugPrint("setIsOn(isOn=%s)"%(isOn,)))
        if self.isOn!=isOn:
            self.isOn=isOn
            stateName = self.fsm.getCurrentState().getName()
            if isOn:
                if stateName != 'playing':
                    self.fsm.request('playing')
            else:
                if stateName != 'attract':
                    self.fsm.request('attract')
            messenger.send(self.getOutputEventName(), [isOn])
    
    def getIsOn(self):
        assert(self.debugPrint("getIsOn() returning %s"%(self.isOn,)))
        return self.isOn
    
    def getName(self):
        return "switch-%s"%(self.entId,)

    def switchOffTask(self, task):
        assert(self.debugPrint("switchOffTask()"))
        self.setIsOn(0)
        self.fsm.request("attract")
        return Task.done
    
    def requestInteract(self):
        assert(self.debugPrint("requestInteract()"))
        avatarId = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("  avatarId:%s"%(avatarId,)))
        stateName = self.fsm.getCurrentState().getName()
        if stateName != 'playing':
            self.sendUpdate("setAvatarInteract", [avatarId])
            self.avatarId=avatarId
            self.fsm.request('playing')
        else:
            self.sendUpdateToAvatarId(avatarId, "rejectInteract", [])

    def requestExit(self):
        assert(self.debugPrint("requestExit()"))
        avatarId = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("  avatarId:%s, %s"%(avatarId,self.avatarId)))
        if self.avatarId and avatarId==self.avatarId:
            stateName = self.fsm.getCurrentState().getName()
            if stateName == 'playing':
                self.sendUpdate("avatarExit", [avatarId])
                self.avatarId = None
                if (self.isOn 
                        and self.secondsOn != -1.0
                        and self.secondsOn >= 0.0):
                    assert(self.doLaterTask==None)
                    self.doLaterTask=taskMgr.doMethodLater(
                            self.secondsOn,
                            self.switchOffTask,
                            self.uniqueName('switch-timer'))
        else:
            assert(self.notify.debug("  requestExit: invalid avatarId"))

    ##### off state #####
    
    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
        #self.sendState()
    
    def exitOff(self):
        assert(self.debugPrint("exitOff()"))

    ##### attract state #####
    
    def enterAttract(self):
        assert(self.debugPrint("enterAttract()"))
        self.sendState()
    
    def exitAttract(self):
        assert(self.debugPrint("exitAttract()"))
    
    ##### playing state #####
    
    def enterPlaying(self):
        assert(self.debugPrint("enterPlaying()"))
        self.sendState()
        self.setIsOn(1)
    
    def exitPlaying(self):
        assert(self.debugPrint("exitPlaying()"))
        if self.doLaterTask:
            self.doLaterTask.remove()
            self.doLaterTask=None
    
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('entId', '?'))+' '+message)

    if __dev__:
        def attribChanged(self, attrib, value):
            self.takedown()
            self.setup()

