from pandac.PandaModules import *
from otp.movement import Impulse

class PetLeash(Impulse.Impulse):
    """keep object from straying farther than 'length' from the origin"""
    def __init__(self, origin, length):
        """origin is a nodepath"""
        Impulse.Impulse.__init__(self)
        self.origin = origin
        self.length = length

    def _process(self, dt):
        Impulse.Impulse._process(self, dt)
        myPos = self.nodePath.getPos()
        myDist = self.VecType(myPos - self.origin.getPos()).length()
        if myDist > self.length:
            excess = myDist - self.length
            shove = self.VecType(myPos)
            shove.normalize()
            shove *= -excess
            self.mover.addShove(shove)
