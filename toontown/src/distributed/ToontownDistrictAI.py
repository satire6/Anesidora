from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from otp.distributed.OtpDoGlobals import *
from otp.distributed.DistributedDistrictAI import DistributedDistrictAI
from toontown.distributed import ToontownDistrictStatsAI

class ToontownDistrictAI(DistributedDistrictAI):
    """
    See Also: "toontown/src/distributed/DistributedDistrict.py"
    """
    notify = directNotify.newCategory("ToontownDistrictAI")
    
    def __init__(self, air, name="untitled"):
        DistributedDistrictAI.__init__(self, air, name)
        self.stats = None
        
    def generate(self):        
        DistributedDistrictAI.generate(self)
        self.stats = ToontownDistrictStatsAI.ToontownDistrictStatsAI(self.air)
        self.stats.toontownDistrictId = self.doId
        self.stats.generateOtpObject(self.stats.defaultParent, self.stats.defaultZone)

    def delete(self):
        DistributedDistrictAI.delete(self)        
        if(self.stats is not None):
            self.stats.requestDelete()
            self.stats = None
