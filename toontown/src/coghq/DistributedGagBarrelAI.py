from toontown.toonbase.ToontownBattleGlobals import *
import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task


class DistributedGagBarrelAI(DistributedBarrelBaseAI.DistributedBarrelBaseAI):

    def __init__(self, level, entId):
        #self.gagTrack = 0
        #self.gagLevel = 0
        x = y = z = h = 0
        self.gagLevelMax = 0
        DistributedBarrelBaseAI.DistributedBarrelBaseAI.__init__(
            self, level, entId)

    def d_setGrab(self, avId):
        # override the base class d_setGrab
        self.notify.debug("d_setGrab %s" % avId)
        self.sendUpdate("setGrab", [avId])

        # Update the inventory
        av = self.air.doId2do.get(avId)
        if av:
            # check track access
            if not av.hasTrackAccess(self.getGagTrack()):
                return

            track = self.getGagTrack()
            level = self.getGagLevel()
            #level = len(Levels[track]) - 1
            
            # only add up to max carry
            maxGags = av.getMaxCarry()
            av.inventory.calcTotalProps()
            numGags = av.inventory.totalProps
            numReward = min(self.getRewardPerGrab(), maxGags-numGags)

            # start adding from the indicated level down, so we max out
            # on higher level gags first
            while numReward > 0 and level >= 0:
                result = av.inventory.addItem(track, level)
                if result <= 0:
                    level -= 1
                else:
                    numReward -= 1

            # use this code if we are just giving out a particular
            # level of gag.  usually though we will just want to give the
            # highest level of this track
            #for i in range(self.getRewardPerGrab()):
            #    ret = av.inventory.addItem(self.getGagTrack(), self.gagLevel)

            # Finally, set the inventory on the client
            av.d_setInventory(av.inventory.makeNetString())
