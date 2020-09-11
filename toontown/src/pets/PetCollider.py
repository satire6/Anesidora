from pandac.PandaModules import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse
from otp.otpbase import OTPGlobals

class PetCollider(Impulse.Impulse):
    SerialNum = 0
    
    def __init__(self, petRadius, collTrav):
        Impulse.Impulse.__init__(self)
        self.petRadius = petRadius
        self.collTrav = collTrav

        # create vectors that we will need every frame
        # don't know what vec class to use yet
        self.vel = None
        self.rotVel = None
        self.vH = 0

        # create collision solids
        self.fwdCLine   = CollisionSegment(0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        self.leftCLine  = CollisionSegment(0.0, 0.0, 0.0,-1.0, 1.0, 0.0)
        self.rightCLine = CollisionSegment(0.0, 0.0, 0.0, 1.0, 1.0, 0.0)
        self.calcCollLines()

        cLineNode = CollisionNode('cLineNode')
        cLineNode.addSolid(self.fwdCLine)
        cLineNode.addSolid(self.leftCLine)
        cLineNode.addSolid(self.rightCLine)
        cLineNode.setFromCollideMask(OTPGlobals.WallBitmask)
        cLineNode.setIntoCollideMask(BitMask32.allOff())
        self.cLineNodePath = hidden.attachNewNode(cLineNode)

        self.cHandler = CollisionHandlerEvent()
        self.cHandler.addInPattern(self._getCollisionEvent())
        # we want an event on every frame in which we're colliding
        # with anything
        self.cHandler.addAgainPattern(self._getCollisionEvent())

        self.collTrav.addCollider(self.cLineNodePath, self.cHandler)

        self.accept(self._getCollisionEvent(), self.handleCollision)

    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)
        self.cLineNodePath.reparentTo(self.nodePath)
        self.vel = self.VecType(0)
        self.rotVel = self.VecType(0)

    def destroy(self):
        self.ignore(self._getCollisionEvent())
        
        self.collTrav.removeCollider(self.cLineNodePath)
        del self.cHandler
        del self.collTrav
        self.cLineNodePath.removeNode()
        del self.cLineNodePath

        del self.vel

    def calcCollLines(self):
        # one line out in front, one out to each side and forward
        self.fwdCLine.setPointB(Point3(0, self.mover.getFwdSpeed(), 0))
        self.leftCLine.setPointB(Point3(-self.petRadius, self.petRadius, 0))
        self.rightCLine.setPointB(Point3(self.petRadius, self.petRadius, 0))

    def _getSerialNum(self):
        if not hasattr(self, 'serialNum'):
            self.serialNum = PetCollider.SerialNum
            PetCollider.SerialNum += 1
        return self.serialNum

    def _getCollisionEvent(self):
        # this event will be thrown by the Panda collision system
        return 'petFeeler-%s' % self._getSerialNum()
        
    def handleCollision(self, collEntry):
        print 'collision!'
        #print 'collision: %s' % collEntry
        #import pdb
        #pdb.set_trace()
        cPoint = collEntry.getSurfacePoint(self.cLineNodePath)
        cNormal = collEntry.getSurfaceNormal(self.cLineNodePath)
        messenger.send(self.mover.getCollisionEventName(),
                       [cPoint, cNormal])
        """
        dist = self.VecType(cPoint).length()
        # push away from the surface
        # shove more based on how close we are to the collision
        # this assumes that fwdSpeed is the max distance of the
        # collision point
        shoveMag = self.mover.getFwdSpeed() - dist
        #shoveMag = self.getFwdSpeed()
        shove = cNormal * shoveMag * 1.2
        self.vel += shove
        """

    """
    def _process(self, dt):
        Impulse.Impulse._process(self, dt)
        me = self.nodePath
        self.mover.addShove(self.vel)
        self.vel = self.VecType(0)
        if self.vH:
            self.rotVel.setX(self.vH)
            self.vH = 0
            self.mover.addRotShove(self.rotVel)
            """
        
