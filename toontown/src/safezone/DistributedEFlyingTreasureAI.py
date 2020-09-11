import DistributedSZTreasureAI

class DistributedEFlyingTreasureAI(DistributedSZTreasureAI.DistributedSZTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedSZTreasureAI.DistributedSZTreasureAI.__init__(self, air,
                                                                 treasurePlanner,
                                                                 x, y, z)
        
