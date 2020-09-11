from pandac.PandaModules import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse
import math

class PetChase(Impulse.Impulse):
    def __init__(self, target=None, minDist=None, moveAngle=None):
        Impulse.Impulse.__init__(self)
        self.target = target
        # how close do we want to get to the target?
        if minDist is None:
            minDist = 5.
        self.minDist = minDist
        # how much do we need to be facing our target before we start moving?
        if moveAngle is None:
            moveAngle = 20.
        self.moveAngle = moveAngle
        
        # create a node that we'll use to calculate hprs
        self.lookAtNode = NodePath('lookatNode')
        self.lookAtNode.hide()

        # create vectors that we will need every frame
        # don't know what vec class to use yet
        self.vel = None
        self.rotVel = None

    def setTarget(self, target):
        # set a new target (this object is intended to be reused)
        self.target = target

    def destroy(self):
        self.lookAtNode.removeNode()
        del self.lookAtNode
        del self.target
        del self.vel
        del self.rotVel

    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)
        self.lookAtNode.reparentTo(self.nodePath)
        self.vel = self.VecType(0)
        self.rotVel = self.VecType(0)

    def _process(self, dt):
        Impulse.Impulse._process(self, dt)
        me = self.nodePath
        target = self.target

        targetPos = target.getPos(me)
        # work in 2d
        #targetPos.setZ(0)
        #distance = self.VecType(targetPos).length()
        x = targetPos[0]
        y = targetPos[1]
        distance = math.sqrt((x*x) + (y*y))
        self.lookAtNode.lookAt(target)
        relH = reduceAngle(self.lookAtNode.getH(me))

        # turn towards target
        epsilon = .005
        rotSpeed = self.mover.getRotSpeed()
        if relH < -epsilon:
            vH = -rotSpeed
        elif relH > epsilon:
            vH = rotSpeed
        else:
            vH = 0

        # don't oversteer
        if abs(vH*dt) > abs(relH):
            vH = relH / dt

        if (distance > self.minDist) and (abs(relH) < self.moveAngle):
            vForward = self.mover.getFwdSpeed()
        else:
            vForward = 0

        # don't get too close
        distanceLeft = distance - self.minDist
        if (distance > self.minDist) and ((vForward*dt) > distanceLeft):
            vForward = distanceLeft / dt

        if vForward:
            self.vel.setY(vForward)
            self.mover.addShove(self.vel)
        if vH:
            self.rotVel.setX(vH)
            self.mover.addRotShove(self.rotVel)
