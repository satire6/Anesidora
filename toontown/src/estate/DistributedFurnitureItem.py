from toontown.toonbase.ToontownGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from toontown.catalog import CatalogItem
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from toontown.toonbase import TTLocalizer
import DistributedHouseItem
from direct.distributed import DistributedSmoothNode
from direct.task import Task
import HouseGlobals

class DistributedFurnitureItem(DistributedHouseItem.DistributedHouseItem,
                               DistributedSmoothNode.DistributedSmoothNode):

    notify = directNotify.newCategory("DistributedFurnitureItem")

    def __init__(self, cr):
        DistributedHouseItem.DistributedHouseItem.__init__(self, cr)
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        # For some reason, DistributedNode does not do this.
        # Maybe because it assumes Actor will?
        NodePath.__init__(self)

        self.localControl = True
        
        self.__broadcastFrequency = 0.25
        self.__adjustStarted = 0
        self.furnitureMgr = None
        self.transmitRelativeTo = None

    def generate(self):
        DistributedHouseItem.DistributedHouseItem.generate(self)
        DistributedSmoothNode.DistributedSmoothNode.generate(self)
        self.__taskName = self.taskName("sendRequestPosHpr")

    def announceGenerate(self):
        DistributedHouseItem.DistributedHouseItem.announceGenerate(self)
        DistributedSmoothNode.DistributedSmoothNode.announceGenerate(self)
        self.load()

    def load(self):
        pass
        
    def disable(self):
        taskMgr.remove(self.__taskName)
        self.stopSmooth()
        self.furnitureMgr.dfitems.remove(self)
        self.furnitureMgr = None
        DistributedHouseItem.DistributedHouseItem.disable(self)
        DistributedSmoothNode.DistributedSmoothNode.disable(self)

    def delete(self):
        self.removeNode()
        del self.item
        DistributedHouseItem.DistributedHouseItem.delete(self)
        DistributedSmoothNode.DistributedSmoothNode.delete(self)

    def setItem(self, furnitureMgrId, blob):
        # We shouldn't get this message twice.
        assert(self.furnitureMgr == None)
        self.furnitureMgr = self.cr.doId2do[furnitureMgrId]
        self.furnitureMgr.dfitems.append(self)
        self.item = CatalogItem.getItem(blob, store = CatalogItem.Customization)
        assert(self.notify.debug("setItem: item: %s" % (self.item)))
        # Assign the actual node path
        self.assign(self.loadModel())
        interior = self.furnitureMgr.getInteriorObject()
        self.reparentTo(interior.interior)

    def loadModel(self):
        # Derived classes can override this to return a different model.
        return self.item.loadModel()

    def startAdjustPosHpr(self):
        assert(self.notify.debug("startAdjustPosHpr"))
        if (self.__adjustStarted):
            return
        self.__adjustStarted = 1
        # Initiate smoothing
        self.clearSmoothing()
        taskMgr.remove(self.__taskName)
        posHpr = self.__getPosHpr()
        self.__oldPosHpr = posHpr
        # Send initial update
        self.sendRequestPosHpr(0, *posHpr)
        # Spawn doLaters to form an efficient task loop
        taskMgr.doMethodLater(self.__broadcastFrequency, self.__posHprBroadcast, self.__taskName)

    def __posHprBroadcast(self, task):
        assert(self.__adjustStarted)
        posHpr = self.__getPosHpr()
        if not self.__comparePosHpr(posHpr, self.__oldPosHpr, 0.1):
            assert(self.notify.debug("posHprBroadcast: NO movement: %s vs. %s" % (posHpr, self.__oldPosHpr)))
            # Item did not move enough, do not send an update
            pass
        else:
            self.__oldPosHpr = posHpr
            assert(self.notify.debug("posHprBroadcast: movement"))
            self.sendRequestPosHpr(0, *posHpr)
        taskMgr.doMethodLater(self.__broadcastFrequency, self.__posHprBroadcast, self.__taskName)
        return Task.done
        
    def stopAdjustPosHpr(self):
        assert(self.notify.debug("stopAdjustPosHpr"))
        if (not self.__adjustStarted):
            return
        self.__adjustStarted = 0
        taskMgr.remove(self.__taskName)
        # Send the final update to be recorded in the db
        posHpr = self.__getPosHpr()
        self.sendRequestPosHpr(1, *posHpr)
        # Do not need this anymore
        del self.__oldPosHpr

    def sendRequestPosHpr(self, final, x,y,z, h,p,r):
        """
        Send a positional update to the AI. If this is a final update for this
        object for a while, pass in final=1. The AI will write the update to the
        database only on final updates as an optimization. If the AI approves this
        request, it will send smooth pos hprs back
        """
        t = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("requestPosHpr", (final, x,y,z, h,p,r, t))

    def setMode(self, mode, avId):
        assert(self.notify.debug("setMode: mode: %s avId: %s" % (mode, avId)))
        # When we start moving the furniture, start smoothing the motion
        # If we are the director, we do not want the smoothing because we
        # are controlling the furniture directly with the mouse
        if mode == HouseGlobals.FURNITURE_MODE_START:
            if avId != base.localAvatar.getDoId():
                self.startSmooth()
        # When we stop moving the furniture, stop smoothing the motion
        # If we are the director, we never started smoothing
        elif mode == HouseGlobals.FURNITURE_MODE_STOP:
            if avId != base.localAvatar.getDoId():
                self.stopSmooth()
        elif mode == HouseGlobals.FURNITURE_MODE_OFF:
            pass
        else:
            self.notify.warning("setMode: unknown mode: %s avId: %s" % (mode, avId))

    def __getPosHpr(self):
        if self.transmitRelativeTo == None:
            pos = self.getPos()
            hpr = self.getHpr()
        else:
            pos = self.getPos(self.transmitRelativeTo)
            hpr = self.getHpr(self.transmitRelativeTo)

        return (pos[0], pos[1], pos[2],
                hpr[0], hpr[1], hpr[2])

    def __comparePosHpr(self, a, b, threshold):
        for i in range(len(a)):
            if (abs(a[i] - b[i]) >= threshold):
                return 1

        return 0
