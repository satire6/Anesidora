from pandac.PandaModules import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse
from otp.otpbase import OTPGlobals

class PetSphere(Impulse.Impulse):
    SerialNum = 0
    # puts a wall-collision sphere around the pet
    def __init__(self, petRadius, collTrav):
        Impulse.Impulse.__init__(self)
        self.serialNum = PetSphere.SerialNum
        PetSphere.SerialNum += 1
        self.petRadius = petRadius
        # TODO: should this come from the mover?
        self.collTrav = collTrav

    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)

        # create collision solids
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, self.petRadius)
        cSphereNode = CollisionNode('PetSphere')
        cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = hidden.attachNewNode(cSphereNode)
        self.cSphereNodePath.reparentTo(self.nodePath)

        cSphereNode.setFromCollideMask(OTPGlobals.WallBitmask)
        # this is here to make pets collide with each other
        cSphereNode.setIntoCollideMask(OTPGlobals.WallBitmask)
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.setHorizontal(1)
        self.pusher.setInPattern("enter%in")
        self.pusher.setOutPattern("exit%in")
        self.pusher.addCollider(self.cSphereNodePath, self.nodePath)
        self.pusher.addInPattern(self._getCollisionEvent())

        self.collTrav.addCollider(self.cSphereNodePath, self.pusher)

        # listen for collisions
        self.accept(self._getCollisionEvent(), self._handleCollision)

    def _clearMover(self, mover):
        self.ignore(self._getCollisionEvent())
        self.collTrav.removeCollider(self.cSphereNodePath)
        del self.cSphere
        del self.pusher
        del self.collTrav
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath

    def _getCollisionEvent(self):
        # this event will be thrown by the Panda collision system
        return 'petSphereColl-%s' % self.serialNum
    
    def _handleCollision(self, collEntry):
        """
        cPoint = collEntry.getSurfacePoint(self.cSphereNodePath)
        cNormal = collEntry.getSurfaceNormal(self.cSphereNodePath)
        messenger.send(self.mover.getCollisionEventName(),
                       [cPoint, cNormal])
                       """
        messenger.send(self.mover.getCollisionEventName(), [collEntry])
