from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.golf import DistributedGolfHoleAI
from pandac.PandaModules import *

def GE():
    simbase.air.golf = DistributedGolfEntranceAI()
    simbase.air.golf.generateWithRequired(2000)
    return simbase.air.golf

class DistributedGolfManagerAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self):
        DistributedObjectAI.DistributedObjectAI.__init__(self, simbase.air)
        self.golfZone = None
    
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    def sendToGolfCourse(self, avId):
        if self.golfZone == None:
            self.golfZone = self.air.allocateZone()
            someHole = DistributedGolfHoleAI.DistributedGolfHoleAI(self.golfZone)
            someHole.generateWithRequired(self.golfZone)
        print("Sending %s to course %s" % (avId, self.golfZone))
        self.sendUpdate("sendToGolfCourse", [avId, self.golfZone])
        
    