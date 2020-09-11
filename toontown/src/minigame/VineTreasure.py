"""MazeTreasure module: contains the MazeTreasure class"""

from direct.showbase.DirectObject import DirectObject
from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal

class VineTreasure(DirectObject):
    """
    Treasures toons can pickup swinging from vine to vine.  Based on MazeTreasure
    """
    
    notify = DirectNotifyGlobal.directNotify.newCategory("VineTreasure")

    RADIUS = 1.7

    def __init__(self, model, pos, serialNum, gameId ):
        # there are going to be MANY (~650) of these created and destroyed
        # all at once for 4-player games; make it lean
        self.serialNum = serialNum

        # the fruit has a bit of height, lets recenter
        center = model.getBounds().getCenter()
        center = Point3(0,0,0)
        self.nodePath = model.copyTo(render)
        self.nodePath.setPos(pos[0] - center[0], 0 - center[1], pos[2] - center[2])
        self.nodePath.setScale(0.25)

        # Make a sphere, name it uniquely, and child it
        # to the nodepath.
        self.sphereName = "treasureSphere-%s-%s" % (gameId, self.serialNum)
        self.collSphere = CollisionSphere(center[0], center[1], center[2], self.RADIUS)
        # Make the sphere intangible
        self.collSphere.setTangible(0)
        self.collNode = CollisionNode(self.sphereName)
        self.collNode.setIntoCollideMask(WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = render.attachNewNode(self.collNode)
        self.collNodePath.setPos(pos[0] - center[0], 0 - center[1], pos[2] - center[2])        
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
        self.notify.debug('treasuerGrabbed')
        messenger.send("VineTreasureGrabbed", [self.serialNum])

    def showGrab(self):
        self.nodePath.hide()
        self.collNodePath.hide()
        # disable collisions
        self.collNode.setIntoCollideMask(BitMask32(0))
