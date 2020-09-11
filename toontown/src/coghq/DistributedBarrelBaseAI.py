from direct.directnotify import DirectNotifyGlobal
from otp.level import DistributedEntityAI
from direct.task import Task
from toontown.coghq import BarrelBase

class DistributedBarrelBaseAI(DistributedEntityAI.DistributedEntityAI,
                              BarrelBase.BarrelBase):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedBarrelBaseAI")
    def __init__(self, level, entId):
        self.rewardPerGrabMax = 0
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)
        self.usedAvIds = []
        
    def delete(self):
        taskMgr.remove(self.taskName("resetGags"))
        del self.usedAvIds
        del self.pos
        DistributedEntityAI.DistributedEntityAI.delete(self)

    def requestGrab(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("requestGrab %s" % avId)
        if not avId in self.usedAvIds:
            self.usedAvIds.append(avId)
            self.d_setGrab(avId)
        else:
            self.sendUpdate("setReject")

    def d_setGrab(self, avId):
        # the base class d_setGrab just notifies the client that the prize
        # was grabbed.  Subclass functions 
        # should make the appropiate AI calls to credit
        # the avatar with the prize (i.e. jellybeans or gags)
        self.sendUpdate("setGrab", [avId])
        return

    """
    # requestGrab decrements the number of available gags.  This
    # would be better served for an MMP space
    def requestGrab(self):
        avId = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("requestGrab(%s)" % avId))
        if self.numGagsLeft > 0:
            self.numGagsLeft -= 1
            self.d_setGrab(avId)
            # if we just took the last gag, restart the timer
            if self.numGagsLeft == 0:
                taskMgr.doMethodLater(10,
                                      self.resetGags,
                                      self.taskName("resetGags"))
        else:
            self.d_setReject()
        self.sendUpdate("setNumGags", [self.numGagsLeft])
    
    def resetGags(self, task):
        self.numGagsLeft =  self.maxGags
        self.sendUpdate("setNumGags", [self.numGagsLeft])
        return Task.done

    """
    
