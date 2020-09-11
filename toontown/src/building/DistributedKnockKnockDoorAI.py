"""
DistributedKnockKnockDoorAI module: contains the DistributedKnockKnockDoorAI
class, the server side representation of a DistributedKnockKnockDoor.
"""

from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
import DistributedAnimatedPropAI
from direct.task.Task import Task
from direct.fsm import State


class DistributedKnockKnockDoorAI(DistributedAnimatedPropAI.DistributedAnimatedPropAI):
    """
    The server side representation of a
    single landmark door.  This is the object that remembers what the
    door is doing.  The child of this object, the DistributedDoor
    object, is the client side version and updates the display that
    client's display based on the state of the door.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedKnockKnockDoorAI')

    def __init__(self, air, propId):
        """
        blockNumber: the landmark building number (from the name)
        """
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.__init__(
                self, air, propId)
        assert(self.debugPrint(
                "DistributedKnockKnockDoorAI(%s, %s)"
                %("the air", propId)))
        self.fsm.setName('DistributedKnockKnockDoor')
        self.propId=propId
        self.doLaterTask=None

    ##### off state #####
    
    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterOff(self)
    
    def exitOff(self):
        assert(self.debugPrint("exitOff()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitOff(self)
    
    ##### attract state #####

    def attractTask(self, task):
        assert(self.debugPrint("attractTask()"))
        self.fsm.request("attract")
        return Task.done
    
    def enterAttract(self):
        assert(self.debugPrint("enterAttract()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterAttract(self)
    
    def exitAttract(self):
        assert(self.debugPrint("exitAttract()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitAttract(self)
    
    ##### playing state #####
    
    def enterPlaying(self):
        assert(self.debugPrint("enterPlaying()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.enterPlaying(self)
        assert(self.doLaterTask==None)
        self.doLaterTask=taskMgr.doMethodLater(
            9, #KNOCK_KNOCK_DOOR_TIME,    #TODO: define this elsewhere
            self.attractTask,
            self.uniqueName('knockKnock-timer'))
    
    def exitPlaying(self):
        assert(self.debugPrint("exitPlaying()"))
        DistributedAnimatedPropAI.DistributedAnimatedPropAI.exitPlaying(self)
        taskMgr.remove(self.doLaterTask)
        self.doLaterTask=None


