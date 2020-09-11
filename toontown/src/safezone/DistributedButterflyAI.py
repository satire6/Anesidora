from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *

from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import ButterflyGlobals
import random

class DistributedButterflyAI(DistributedObjectAI.DistributedObjectAI):
    
    def __init__(self, air, playground, area, ownerId):
        """__init__(air, area)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        self.playground = playground
        self.area = area
        self.ownerId = ownerId

        self.fsm = ClassicFSM.ClassicFSM('DistributedButterfliesAI',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['Flying', 'Landed']),
                            State.State('Flying',
                                        self.enterFlying,
                                        self.exitFlying,
                                        ['Landed']),
                            State.State('Landed',
                                        self.enterLanded,
                                        self.exitLanded,
                                        ['Flying']),],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()

        (self.curPos, self.curIndex, self.destPos, self.destIndex, 
                self.time) = ButterflyGlobals.getFirstRoute(self.playground,
                                                         self.area, self.ownerId)

        return None

    def delete(self):
        try:
            self.butterfly_deleted
            assert(self.notify.debug("butterfly already deleted"))
        except:
            self.butterfly_deleted = 1
            ButterflyGlobals.recycleIndex(self.curIndex, self.playground, 
                                          self.area, self.ownerId)
            ButterflyGlobals.recycleIndex(self.destIndex, self.playground, 
                                          self.area, self.ownerId)
            self.fsm.request('off')
            del self.fsm
            DistributedObjectAI.DistributedObjectAI.delete(self)

    # setState()

    def d_setState(self, stateIndex, curIndex, destIndex, time):
        self.sendUpdate('setState', [stateIndex, curIndex, destIndex, time,
                                     globalClockDelta.getRealNetworkTime()])

    def getArea(self):
        return [self.playground, self.area]

    def getState(self):
        return [self.stateIndex, self.curIndex,
                self.destIndex, self.time,
                globalClockDelta.getRealNetworkTime()]

    def start(self):
        self.fsm.request('Flying')

    def avatarEnter(self):
        #print 'aha!'
        if (self.fsm.getCurrentState().getName() == 'Landed'):
            self.__ready()
        return None

    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### off state #####

    def enterOff(self):
        self.stateIndex = ButterflyGlobals.OFF
        return None

    def exitOff(self):
        return None

    ##### Flying state #####

    def enterFlying(self):
        self.stateIndex = ButterflyGlobals.FLYING
        # We can let someone else fly to curPos now
        ButterflyGlobals.recycleIndex(self.curIndex, self.playground,
                                      self.area, self.ownerId)
        self.d_setState(ButterflyGlobals.FLYING, self.curIndex, self.destIndex, self.time)
        taskMgr.doMethodLater(self.time, self.__handleArrival,
                                              self.uniqueName('butter-flying'))
        return None

    def exitFlying(self):
        taskMgr.remove(self.uniqueName('butter-flying'))
        return None

    def __handleArrival(self, task):
        # We're at the destination, so curPos is now destPos
        self.curPos = self.destPos
        self.curIndex = self.destIndex
        self.fsm.request('Landed')
        return Task.done

    ##### Landed state #####

    def enterLanded(self):
        self.stateIndex = ButterflyGlobals.LANDED
        self.time = random.random() * ButterflyGlobals.MAX_LANDED_TIME 
        self.d_setState(ButterflyGlobals.LANDED, self.curIndex, self.destIndex, self.time)
        taskMgr.doMethodLater(self.time, self.__ready,
                                                self.uniqueName('butter-ready'))
        return None

    def exitLanded(self):
        taskMgr.remove(self.uniqueName('butter-ready'))
        return None

    def __ready(self, task = None):
        # Figure out where to go
        (self.destPos, self.destIndex, 
            self.time) = ButterflyGlobals.getNextPos(self.curPos, 
                                    self.playground, self.area, self.ownerId)
        self.fsm.request('Flying')
        return Task.done
