from pandac.PandaModules import *
import Impulse

class ImpFriction(Impulse.Impulse):
    """friction impulse"""
    def __init__(self, coeff):
        """ coeff: coefficient of friction. 0..1,
        0=no friction, 1=absolute friction"""
        Impulse.Impulse.__init__(self)
        self.coeff = coeff

    def _process(self, dt):
        self.mover._addForce(-self.mover.vel * self.coeff)
        self.mover._addRotForce(-self.mover.rotVel * self.coeff)
