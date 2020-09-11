from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
import cPickle

class DistributedHQInteriorAI(DistributedObjectAI.DistributedObjectAI):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DistributedHQInteriorAI')

    def __init__(self, block, air, zoneId):
        # Right now, this doesn't do much.
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId
        self.tutorial = 0

        # When the leaders change, the trophy mgr will notify us
        self.isDirty = False
        self.accept("leaderboardChanged", self.leaderboardChanged)
        self.accept("leaderboardFlush", self.leaderboardFlush)

    def delete(self):
        # This is important because the tutorial interiors get created and deleted
        self.ignore("leaderboardChanged")
        self.ignore('leaderboardFlush')
        self.ignore("setLeaderBoard")
        self.ignore('AIStarted')
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    def getZoneIdAndBlock(self):
        r=[self.zoneId, self.block]
        return r

    def leaderboardChanged(self):
        # This message is sent when the leaders change.
        self.isDirty = True

    def leaderboardFlush(self):
        # This message is sent every 30 seconds after AI startup, to
        # update the leaderboard if necessary.
        if self.isDirty:
            self.sendNewLeaderBoard()

    def sendNewLeaderBoard(self):
        if self.air:
            self.isDirty = False
            self.sendUpdate("setLeaderBoard", [cPickle.dumps(self.air.trophyMgr.getLeaderInfo(), 1)])

    def getLeaderBoard(self):
        # Since this is a required field, we need a getter
        # This needs to be returned as parallel lists of avIds, name, and scores
        return cPickle.dumps(self.air.trophyMgr.getLeaderInfo(), 1)

    def getTutorial(self):
        return self.tutorial
    
    def setTutorial(self, flag):
        if self.tutorial != flag:
            self.tutorial = flag
            self.sendUpdate("setTutorial", [self.tutorial])
