""" TwoDWalk.py: contains the TwoDWalk class """

from OrthoWalk import *

class TwoDWalk(OrthoWalk):
    """
    holds TwoDDrive object and broadcasts new positions
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TwoDWalk")

    BROADCAST_POS_TASK = "TwoDWalkBroadcastPos"

    def doBroadcast(self, task):
        dt = globalClock.getDt()
        self.timeSinceLastPosBroadcast += dt
        if self.timeSinceLastPosBroadcast >= self.broadcastPeriod:
            self.timeSinceLastPosBroadcast = 0            
            # broadcast the full position instead of just the xyh.
            # This is the only line different from OrthoWalk.
            self.lt.cnode.broadcastPosHprFull()
        return Task.cont