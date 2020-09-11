""" DistributedSwitch module: contains the DistributedSwitch
    class, the client side representation of a DistributedSwitchAI."""

from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from otp.level import BasicEntities
import DistributedSwitchBase
import MovingPlatform
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from otp.level import DistributedEntity
#import TTLocalizer

class DistributedSwitch(
        DistributedSwitchBase.DistributedSwitchBase,
        BasicEntities.DistributedNodePathEntity):
    """
    DistributedSwitch class:  The client side 
    representation of a Cog HQ switch.
    
    See Also: DistributedSwitchAI
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedSwitch')

    def __init__(self, cr):
        """
        constructor for the DistributedSwitch
        """
        assert(self.debugPrint("DistributedSwitch()"))
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)
        #assert self.this

        self.fsm = ClassicFSM.ClassicFSM('DistributedSwitch',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['playing',
                                        'attract']),
                            State.State('attract',
                                        self.enterAttract,
                                        self.exitAttract,
                                        ['playing']),
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

        self.node = None
        self.triggerName = ''
        # self.generate will be called automatically.

    def setup(self):
        self.setupSwitch()
        self.setState(self.initialState, self.initialStateTimestamp)
        del self.initialState
        del self.initialStateTimestamp
        self.accept("exit%s"%(self.getName(),), self.exitTrigger)
        self.acceptAvatar()
        
    def takedown(self):
        pass

    # These stubbed out functions are not used on the client (AI Only):
    setIsOnEvent = DistributedSwitchBase.stubFunction
    setIsOn = DistributedSwitchBase.stubFunction
    setSecondsOn = DistributedSwitchBase.stubFunction

    def generate(self):
        """
        This method is called when the DistributedSwitch is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        BasicEntities.DistributedNodePathEntity.generate(self)
        self.track = None
    
    def announceGenerate(self):
        assert(self.debugPrint("announceGenerate()"))
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)
        assert self.this
        self.setup()
    
    def disable(self):
        assert(self.debugPrint("disable()"))
        #self.ignore("exit%s"%(self.getName(),))
        #self.ignore("enter%s"%(self.getName(),))
        self.ignoreAll()
        # Go to the off state when the object is put in the cache
        self.fsm.request("off")
        BasicEntities.DistributedNodePathEntity.disable(self)
        assert(self.track is None)
        self.takedown()
        #?  BasicEntities.DistributedNodePathEntity.destroy(self)
        # self.delete() will automatically be called.

    def delete(self):
        assert(self.debugPrint("delete()"))
        del self.fsm
        BasicEntities.DistributedNodePathEntity.delete(self)
    
    def acceptAvatar(self):
        self.acceptOnce("enter%s"%(self.getName(),), self.enterTrigger)
    
    def rejectInteract(self):
        self.acceptAvatar()

    def avatarExit(self, avatarId):
        self.acceptAvatar()
    
    #def setIsOn(self, isOn):
    #    assert(self.debugPrint("setIsOn(isOn=%s)"%(isOn,)))
    #    self.isOn=isOn
    #    messenger.send(self.getName(), [isOn])
    #
    #def getIsOn(self):
    #    assert(self.debugPrint("setIsOn() returning %s"%(self.isOn,)))
    #    return self.isOn
    
    def getName(self):
        return "switch-%s"%(self.entId,)
    
    def setupSwitch(self):
        """
        Load and position the model.
        """
        pass
    
    def switchOnTrack(self):
        """
        Animate the switch turning on.
        returns a Sequence or None.
        """
        pass
    
    def switchOffTrack(self):
        """
        Animate the switch turning off.
        returns a Sequence or None.
        """
        pass

    def setAvatarInteract(self, avatarId):
        """
        required dc field.
        """
        assert(self.debugPrint("setAvatarInteract(%s)"%(avatarId,)))
        assert(not self.__dict__.has_key(avatarId))
        self.avatarId=avatarId

    def setState(self, state, timestamp):
        """
        required dc field.
        """
        assert(self.debugPrint("setState(%s, %d)" % (state, timestamp)))
        if self.isGenerated():
            self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])
        else:
            self.initialState = state
            self.initialStateTimestamp = timestamp
    
    def enterTrigger(self, args=None):
        assert(self.debugPrint("enterTrigger(args="+str(args)+")"))
        self.sendUpdate("requestInteract")
        # the AI server will reply with avatarInteract or rejectInteract.
    
    def exitTrigger(self, args=None):
        assert(self.debugPrint("exitTrigger(args="+str(args)+")"))
        self.sendUpdate("requestExit")
        # the AI server will reply with avatarExit.

    ##### off state #####
    
    def enterOff(self):
        #assert(self.debugPrint("enterOff()"))
        pass
    
    def exitOff(self):
        #assert(self.debugPrint("exitOff()"))
        pass

    ##### attract state #####
    
    def enterAttract(self, ts):
        assert(self.debugPrint("enterAttract()"))
        track=self.switchOffTrack()
        if track is not None:
            track.start(ts)
            self.track = track
    
    def exitAttract(self):
        assert(self.debugPrint("exitAttract()"))
        if self.track:
            self.track.finish()
        self.track = None
    
    ##### playing state #####
    
    def enterPlaying(self, ts):
        assert(self.debugPrint("enterPlaying()"))
        # Start animation at time stamp:
        track=self.switchOnTrack()
        if track is not None:
            track.start(ts)
            self.track = track
    
    def exitPlaying(self):
        assert(self.debugPrint("exitPlaying()"))
        if self.track:
            self.track.finish()
        self.track = None

    if __dev__:
        def attribChanged(self, attrib, value):
            self.takedown()
            self.setup()
