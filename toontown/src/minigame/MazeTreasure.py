"""MazeTreasure module: contains the MazeTreasure class"""

from direct.showbase.DirectObject import DirectObject
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal

class MazeTreasure(DirectObject):
    
    #notify = DirectNotifyGlobal.directNotify.newCategory("MazeTreasure")

    RADIUS = 0.7

    def __init__(self, model, pos, serialNum, gameId):
        # there are going to be MANY (~650) of these created and destroyed
        # all at once for 4-player games; make it lean
        self.serialNum = serialNum
        
        self.nodePath = model.copyTo(render)
        self.nodePath.setPos(pos[0], pos[1], 1.)

        # Make a sphere, name it uniquely, and child it
        # to the nodepath.
        self.sphereName = "treasureSphere%s-%s" % (gameId, self.serialNum)
        self.collSphere = CollisionSphere(0, 0, 0, self.RADIUS)
        # Make the sphere intangible
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.sphereName)
        self.collNode.setIntoCollideMask(WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)
        self.collNodePath.hide()

        # Add a hook looking for collisions with localToon
        self.accept('enter' + self.sphereName, self.__handleEnterSphere)
        
        # now that the treasure and sphere have been placed, flatten the
        # whole silly thing
        self.nodePath.flattenLight()

    def destroy(self):
        self.ignoreAll()

        self.nodePath.removeNode()
        del self.nodePath
        del self.collSphere
        self.collNodePath.removeNode()
        del self.collNodePath
        del self.collNode

    def __handleEnterSphere(self, collEntry):
        self.ignoreAll()
        # announce that this treasure was grabbed
        messenger.send("MazeTreasureGrabbed", [self.serialNum])

    def showGrab(self):
        self.nodePath.reparentTo(hidden)
        # disable collisions
        self.collNode.setIntoCollideMask(BitMask32(0))
