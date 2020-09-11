""" DistributedDGFlower module:  contains the DistributedDGFlower
    class which represents the client version of the round,
    spinning flower in Daisy's Garden safezone."""

from pandac.PandaModules import *
from direct.distributed.ClockDelta import *

from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
from direct.task import Task

SPIN_RATE = 1.25

class DistributedDGFlower(DistributedObject.DistributedObject): 
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        
    def generate(self):
        """
        This method is called when the DistributedObject is
        reintroduced to the world, either for the first time
        or from the cache.
        """
        DistributedObject.DistributedObject.generate(self)
        # big, rotating flower
        self.bigFlower = loader.loadModel('phase_8/models/props/DG_flower-mod.bam')
        self.bigFlower.setPos(1.39, 92.91, 2.0)
        self.bigFlower.setScale(2.5)
        self.bigFlower.reparentTo(render)
        
        # set-up collision sphere on the flower
        self.flowerCollSphere = CollisionSphere(0, 0, 0, 4.5)
        self.flowerCollSphereNode = CollisionNode("bigFlowerCollide")
        self.flowerCollSphereNode.addSolid(self.flowerCollSphere)
        self.flowerCollSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.bigFlower.attachNewNode(self.flowerCollSphereNode)

        # set-up trigger sphere on the flower
        self.flowerTrigSphere = CollisionSphere(0, 0, 0, 6.0)
        self.flowerTrigSphere.setTangible(0)
        self.flowerTrigSphereNode = CollisionNode("bigFlowerTrigger")
        self.flowerTrigSphereNode.addSolid(self.flowerTrigSphere)
        self.flowerTrigSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.bigFlower.attachNewNode(self.flowerTrigSphereNode)

        # spawn tasks and hang hooks
        taskMgr.add(self.__flowerSpin,
                                 self.taskName('DG-flowerSpin'))        
        self.accept("enterbigFlowerTrigger", self.__flowerEnter)
        self.accept("exitbigFlowerTrigger", self.__flowerExit)
        
    def disable(self):
        """
        This method is called when the DistributedObject is
        removed from active duty and stored in a cache.
        """
        DistributedObject.DistributedObject.disable(self)
        taskMgr.remove(self.taskName('DG-flowerRaise'))
        taskMgr.remove(self.taskName('DG-flowerSpin'))        
        self.ignore("enterbigFlowerTrigger")
        self.ignore("exitbigFlowerTrigger")
               
    def delete(self):
        """
        This method is called when the DistributedObject is
        permanently removed from the world and deleted from
        the cache.
        """
        DistributedObject.DistributedObject.delete(self)
        self.bigFlower.removeNode()
        del self.bigFlower
        del self.flowerCollSphere
        del self.flowerCollSphereNode
        
    def __flowerSpin(self, task):
        self.bigFlower.setH(self.bigFlower.getH() + SPIN_RATE)
        return Task.cont
        
    def __flowerEnter(self, collisionEntry):
        # tell the server
        self.sendUpdate("avatarEnter", [])
        
    def __flowerExit(self, collisionEntry):
        # tell the server
        self.sendUpdate("avatarExit", [])
        
    def setHeight(self, newHeight):
        # the newHeight is computed by the server
        pos = self.bigFlower.getPos()
        self.bigFlower.lerpPos(pos[0], pos[1], newHeight, 0.5,
                               task=self.taskName("DG-flowerRaise"))




