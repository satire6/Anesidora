from direct.distributed import DistributedObjectAI
from direct.fsm import FSM

class DistributedGolfSpotAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM):
    """ This is one of four golf spots to appear in the corner of the CEO banquet
    room.  """

    def __init__(self, air, boss, index):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedGolfSpotAI')
        self.boss = boss
        self.index = index
        self.avId = 0 # which toon is controlling us
        self.allowControl = True

    def delete(self):
        """Delete ourself."""
        DistributedObjectAI.DistributedObjectAI.delete(self)        

    def getBossCogId(self):
        return self.boss.doId

    def getIndex(self):
        return self.index

    def d_setState(self, state, avId, extraInfo=0):
        self.sendUpdate('setState', [state, avId, extraInfo])

    def requestControl(self):
        # A client wants to start controlling the golfSpot.
        if not self.allowControl:
            return
        avId = self.air.getAvatarIdFromSender()
        
        if avId in self.boss.involvedToons and self.avId == 0 and \
           self.state != 'Off':
            # Also make sure the client isn't controlling some other
            # golfSpot.
            golfSpotId = self.__getGolfSpotId(avId)
            if golfSpotId == 0:
                # one last check, make sure the toon is roaming
                grantRequest = True
                if self.boss and not self.boss.isToonRoaming(avId):
                    grantRequest = False
                if grantRequest:
                    self.request('Controlled', avId)

    def requestFree(self, gotHitByBoss):
        # The client is done controlling the golfSpot.
        avId = self.air.getAvatarIdFromSender()
        
        if avId == self.avId and self.state == 'Controlled':
            self.request('Free', gotHitByBoss)

    def forceFree(self):
        """Force us into the free state."""
        self.request('Free', 0)
    
    def removeToon(self, avId):
        if avId == self.avId:
            self.request('Free')

    def __getGolfSpotId(self, avId):
        # Returns the golfSpotId for the golfSpot that the indicated avatar
        # is controlling, or 0 if none.

        if self.boss and self.boss.golfSpots != None:
            for golfSpot in self.boss.golfSpots:
                if golfSpot.avId == avId:
                    return golfSpot.doId

        return 0

    def turnOff(self):
        # 
        self.request('Off')
        self.allowControl = False


    ### FSM States ###

    def enterOff(self):
        self.sendUpdate('setGoingToReward',[])
        self.d_setState('O',0)
        pass

    def exitOff(self):
        pass

    def enterControlled(self, avId):
        self.avId = avId
        self.d_setState('C', avId)

    def exitControlled(self):
        pass

    def enterFree(self, gotHitByBoss):
        self.avId = 0
        self.d_setState('F', 0, gotHitByBoss)

    def exitFree(self):
        pass
