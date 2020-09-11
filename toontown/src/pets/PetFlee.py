from pandac.PandaModules import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse

class PetFlee(Impulse.Impulse):
    def __init__(self, chaser=None,
                 maxDist=50., moveAngle=20.):
        Impulse.Impulse.__init__(self)
        self.chaser = chaser
        # how far do we want to get from the chaser?
        self.maxDist = maxDist
        # how much do we need to be facing away from our chaser
        # before we start moving?
        self.moveAngle = moveAngle
        
        # create a node that we'll use to calculate hprs
        self.lookAtNode = NodePath('lookatNode')
        self.lookAtNode.hide()

        # create vectors that we will need every frame
        # don't know what vec class to use yet
        self.vel = None
        self.rotVel = None

    def destroy(self):
        self.lookAtNode.removeNode()
        del self.lookAtNode
        del self.chaser
        del self.vel
        del self.rotVel

    def setChaser(self, chaser):
        # set a new chaser (this object is intended to be reused)
        self.chaser = chaser

    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)
        self.lookAtNode.reparentTo(self.nodePath)
        self.vel = self.VecType(0)
        self.rotVel = self.VecType(0)

    def _process(self, dt):
        Impulse.Impulse._process(self, dt)
        me = self.nodePath
        chaser = self.chaser

        chaserPos = chaser.getPos(me)
        # work in 2d
        chaserPos.setZ(0)
        distance = self.VecType(chaserPos).length()
        self.lookAtNode.lookAt(chaser)
        # run away from chaser
        relH = reduceAngle(self.lookAtNode.getH(me) + 180.)

        # turn away from chaser
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

        if (distance < self.maxDist) and (abs(relH) < self.moveAngle):
            vForward = self.mover.getFwdSpeed()
        else:
            vForward = 0

        # don't get too far away
        distanceLeft = self.maxDist - distance
        if (distanceLeft > 0.) and ((vForward*dt) > distanceLeft):
            vForward = distanceLeft / dt

        self.vel.setY(vForward)
        self.rotVel.setX(vH)

        self.mover.addShove(self.vel)
        self.mover.addRotShove(self.rotVel)
