from pandac.PandaModules import *
from direct.showbase.PythonUtil import reduceAngle, randFloat, normalDistrib
from direct.showbase import DirectObject
from toontown.pets import PetChase
from toontown.pets import PetConstants

class PetWander(CPetChase, DirectObject.DirectObject):
    def __init__(self, minDist=5., moveAngle=20.):
        # create a target node that we'll be moving around
        # it doesn't matter that it's under hidden, we can still compare
        # positions with objects under render
        self.movingTarget = hidden.attachNewNode('petWanderTarget')
        CPetChase.__init__(self, self.movingTarget,
                           minDist, moveAngle)

        self.targetMoveCountdown = 0

        # listen for any detected collisions, and use them when deciding
        # where to go next
        self.collEvent = None
        self.gotCollision = False

    def isCpp(self):
        return 0

    def __ignoreCollisions(self):
        if self.collEvent is not None:
            self.ignore(self.collEvent)
            self.collEvent = None

    def _setMover(self, mover):
        CPetChase.setMover(self, mover)
        self.mover = mover
        self.__ignoreCollisions()
        self.collEvent = mover.getCollisionEventName()
        self.accept(self.collEvent, self._handleCollision)

    def _clearMover(self, mover):
        CPetChase.clearMover(self, mover)
        self.__ignoreCollisions()

    def _handleCollision(self, collEntry):
        self.gotCollision = True
        # stop running against the wall
        self.movingTarget.setPos(self.getNodePath().getPos())
        self.targetMoveCountdown *= .5

    def destroy(self):
        self.__ignoreCollisions()
        self.movingTarget.removeNode()
        del self.movingTarget

    def _process(self, dt):
        self.targetMoveCountdown -= dt
        if self.targetMoveCountdown <= 0.:
            distance = normalDistrib(3.,30.)
            heading = normalDistrib(-(90+45),(90+45))

            # if we bumped into something, go in the opposite direction
            # from where we were about to go
            if self.gotCollision:
                self.gotCollision = False
                heading = heading + 180

            target = self.getTarget()
            target.setPos(self.getNodePath().getPos())
            target.setH(target, heading)
            target.setY(target, distance)

            duration = distance / self.mover.getFwdSpeed()
            self.targetMoveCountdown = duration * randFloat(1.2, 3.)

        CPetChase.process(self, dt)
