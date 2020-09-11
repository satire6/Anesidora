from pandac.PandaModules import *
from libotp import CMover
from direct.directnotify import DirectNotifyGlobal
from otp.movement.PyVec3 import PyVec3

from direct.showbase import PythonUtil
import __builtin__

class Mover(CMover):

    notify = DirectNotifyGlobal.directNotify.newCategory("Mover")

    SerialNum = 0
    Profile = 0

    Pstats = 1

    PSCCpp = 'App:Show code:moveObjects:MoverC++'
    PSCPy  = 'App:Show code:moveObjects:MoverPy'
    PSCInt = 'App:Show code:moveObjects:MoverIntegrate'
    
    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        """objNodePath: nodepath to be moved"""
        CMover.__init__(self, objNodePath, fwdSpeed, rotSpeed)

        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1

        self.VecType = Vec3
        #self.VecType = PyVec3

        # dict of python impulses
        self.impulses = {}

        if Mover.Pstats:
            self.pscCpp = PStatCollector(Mover.PSCCpp)
            self.pscPy  = PStatCollector(Mover.PSCPy)
            self.pscInt = PStatCollector(Mover.PSCInt)

    def destroy(self):
        for name, impulse in self.impulses.items():
            Mover.notify.debug('removing impulse: %s' % name)
            self.removeImpulse(name)

    #@report(types=['args'])
    def addImpulse(self, name, impulse):
        if impulse.isCpp():
            CMover.addCImpulse(self, name, impulse)
        else:
            self.impulses[name] = impulse
            impulse._setMover(self)

    #@report(types=['args'])
    def removeImpulse(self, name):
        if name not in self.impulses:
            if not CMover.removeCImpulse(self, name):
                Mover.notify.warning(
                    "Mover.removeImpulse: unknown impulse '%s'" % name)
            return
        self.impulses[name]._clearMover(self)
        del self.impulses[name]

    def getCollisionEventName(self):
        # this event may be thrown by impulses in order to let other
        # impulses know that a collision has occured. Argument is the
        # collision entry.
        return 'moverCollision-%s' % self.serialNum

    def move(self, dt=-1, profile=0):
        # TODO: account for movement that we didn't cause?

        if Mover.Profile and (not profile):
            # profile
            def func(doMove=self.move):
                for i in xrange(10000):
                    doMove(dt, profile=1)
            __builtin__.func = func
            PythonUtil.startProfile(cmd='func()', filename='profile', sorts=['cumulative'], callInfo=0)
            del __builtin__.func
            return

        if Mover.Pstats:
            self.pscCpp.start()

        # do C++ impulses first
        CMover.processCImpulses(self, dt)

        if Mover.Pstats:
            self.pscCpp.stop()
            self.pscPy.start()

        # now do Python impulses
        for impulse in self.impulses.values():
            impulse._process(self.getDt())

        if Mover.Pstats:
            self.pscPy.stop()
            self.pscInt.start()

        # lastly, do the integration
        CMover.integrate(self)

        if Mover.Pstats:
            self.pscInt.stop()
