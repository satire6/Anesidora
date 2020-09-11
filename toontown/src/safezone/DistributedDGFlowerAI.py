""" DistributedDGFlowerAI module:  contains the DistributedDGFlower
    class which represents the server version of the round,
    spinning flower in Daisy's Garden safezone."""

from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *

from direct.distributed import DistributedObjectAI
from direct.task import Task

HEIGHT_DELTA = 0.5
MAX_HEIGHT = 10.0
MIN_HEIGHT = 2.0

class DistributedDGFlowerAI(DistributedObjectAI.DistributedObjectAI):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // DistributedDGFlowerAI:  server side version of the spinning flower
    //                         located in Daisy's Garden safezone.
    //                         Handles state management of the flower.
    //
    ////////////////////////////////////////////////////////////////////
    """
    def __init__(self, air):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.height = MIN_HEIGHT
        self.avList = []
        return None

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def start(self):
        return None
    
    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if not (avId in self.avList):
            # ad avatar to list
            self.avList.append(avId)
            # compute new height
            if (self.height + HEIGHT_DELTA <= MAX_HEIGHT):
                self.height += HEIGHT_DELTA
                # send update to clients
                self.sendUpdate("setHeight", [self.height])
                
    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if (avId in self.avList):
            # remove avatar from list
            self.avList.remove(avId)
            # compute new height
            if (self.height - HEIGHT_DELTA >= MIN_HEIGHT):
                self.height -= HEIGHT_DELTA
                # send update to clients
                self.sendUpdate("setHeight", [self.height])                
            

# History
#
# 01Nov01    gregw    created.

