""" OrthoWalk.py: contains the OrthoWalk class """

from toontown.toonbase.ToonBaseGlobal import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from OrthoDrive import *
from direct.directnotify import DirectNotifyGlobal

class OrthoWalk:
    """
    holds OrthoDrive object and broadcasts new positions
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("OrthoWalk")

    BROADCAST_POS_TASK = "OrthoWalkBroadcastPos"

    def __init__(self, orthoDrive,
                 collisions=1,
                 broadcast=1,
                 broadcastPeriod=.1,
                 ):
        self.orthoDrive = orthoDrive
        self.collisions = collisions
        self.broadcast = broadcast
        self.broadcastPeriod = broadcastPeriod
        self.priority = self.orthoDrive.priority+1
        self.lt = base.localAvatar

    def destroy(self):
        self.orthoDrive.destroy()
        del self.orthoDrive

    def start(self):
        self.notify.debug("OrthoWalk start")
        if self.collisions:
            self.initCollisions()
        if self.broadcast:
            self.initBroadcast()
        self.orthoDrive.start()

    def stop(self):
        self.notify.debug("OrthoWalk stop")
        self.shutdownCollisions()
        self.shutdownBroadcast()
        self.orthoDrive.stop()

    def initCollisions(self):
        self.notify.debug("OrthoWalk initCollisions")
        lt = base.localAvatar
        lt.collisionsOn()
        self._OrthoWalk__collisionsOn = 1

    def shutdownCollisions(self):
        if not hasattr(self, '_OrthoWalk__collisionsOn'):
            return
        del self._OrthoWalk__collisionsOn
        self.notify.debug("OrthoWalk shutdownCollisions")
        lt = base.localAvatar
        lt.collisionsOff()

    def initBroadcast(self):
        self.notify.debug("OrthoWalk initBroadcast")
        self.timeSinceLastPosBroadcast = 0.
        self.lastPosBroadcast = self.lt.getPos()
        self.lastHprBroadcast = self.lt.getHpr()
        self.storeStop = 0
        # do an initial broadcast of the full position
        lt = self.lt
        lt.d_clearSmoothing()
        lt.sendCurrentPosition()
        taskMgr.remove(self.BROADCAST_POS_TASK)
        taskMgr.add(self.doBroadcast,
                    self.BROADCAST_POS_TASK,
                    priority=self.priority)

    def shutdownBroadcast(self):
        self.notify.debug("OrthoWalk shutdownBroadcast")
        taskMgr.remove(self.BROADCAST_POS_TASK)

    def doBroadcast(self, task):
        dt = globalClock.getDt()
        self.timeSinceLastPosBroadcast += dt
        if self.timeSinceLastPosBroadcast >= self.broadcastPeriod:
            self.timeSinceLastPosBroadcast = 0            
            # broadcast the current position, if changed
            self.lt.cnode.broadcastPosHprXyh()
        return Task.cont
