import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

class DistributedBeanBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):
    def __init__(self, level, entityId):
        x = y = z = h = 0
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(
            self, level, entityId)
        
    def d_setGrab(self, avId):
        # override the base class d_setGrab
        self.notify.debug("d_setGrab %s" % avId)
        self.sendUpdate("setGrab", [avId])

        # Update the inventory
        av = self.air.doId2do.get(avId)
        if av:
            av.addMoney(self.rewardPerGrab)
    
