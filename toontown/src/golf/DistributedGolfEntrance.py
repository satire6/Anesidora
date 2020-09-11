from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *

class DistributedGolfEntrance(DistributedObject.DistributedObject):
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, base.cr)
        self.golfZone = None
        
    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        
    def sendToGolfCourse(self, avId, zoneId):
        print("sending to golfCourse")
        if avId == localAvatar.doId:
            hoodId = self.cr.playGame.hood.hoodId
            golfRequest = {
                "loader": "safeZoneLoader",
                "where": "golfcourse",
                "how" : "teleportIn",
                "hoodId" : hoodId,
                "zoneId" : zoneId,
                "shardId" : None,
                "avId" : -1,
            }
            base.cr.playGame.getPlace().requestLeave(golfRequest)
            