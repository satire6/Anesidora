import DistributedTreasureAI
from toontown.toonbase import ToontownGlobals

class DistributedSZTreasureAI(DistributedTreasureAI.DistributedTreasureAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedTreasureAI.DistributedTreasureAI.__init__(self, air,
                                                             treasurePlanner,
                                                             x, y, z)
        self.healAmount = treasurePlanner.healAmount

    # override the validate function to indicate that only toons who
    # need healing can pick up treasures.
    def validAvatar(self, av):
        return (av.hp > 0) and (av.hp < av.maxHp)


    # override the grab function and try to heal the toon
    def d_setGrab(self, avId):
        DistributedTreasureAI.DistributedTreasureAI.d_setGrab(self, avId)
        # Boost that laff meter, if you can
        if self.air.doId2do.has_key(avId):
            av = self.air.doId2do[avId]
            # Only toons with positive hp get rewarded for treasures.
            if (av.hp > 0) and (av.hp < av.maxHp):
                # Modify the heal amount based on which holiday is running. 
                if simbase.air.holidayManager.currentHolidays.has_key(ToontownGlobals.VALENTINES_DAY):
                    av.toonUp(self.healAmount * 2)
                else:
                    av.toonUp(self.healAmount)
                
