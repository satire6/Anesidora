from pandac.PandaModules import *
from libotp import CMoverGroup
from otp.movement.Mover import Mover

class MoverGroup(CMoverGroup):
    """group of movers that move simultaneously to optimize for speed"""

    PSCPy     = 'App:Show code:moveObjects:MoverGroupPy'
    PSCCppInt = 'App:Show code:moveObjects:MoverGroupC++AndIntegrate'

    def __init__(self, movers=None):
        CMoverGroup.__init__(self)
        # store a list of the Python Mover objects, apart from
        # the list of C++ Movers stored in CMoverGroup
        self._name2pyMovers = {}
        if movers is not None:
            for mover in movers:
                self.addMover(mover)
        if Mover.Pstats:
            self.pscPy     = PStatCollector(MoverGroup.PSCPy)
            self.pscCppInt = PStatCollector(MoverGroup.PSCCppInt)

    def add(self, name, mover):
        self.addCMover(name, mover)
        self._name2pyMovers[name] = mover
    def remove(self, name):
        self.removeCMover(name)
        if (self._name2pyMovers.has_key(name)):
            del self._name2pyMovers[name]

    def move(self, dt=-1):
        # if dt is -1, CMoverGroup will calculate dt for this frame
        # and return it
        dt = self.setDt(dt)

        # process all the Py impulses first
        if Mover.Pstats:
            self.pscPy.start()
        for mover in self._name2pyMovers.values():
            for impulse in mover.impulses.values():
                impulse._process(dt)
        if Mover.Pstats:
            self.pscPy.stop()

        # now process all C++ impulses and integrate in one step
        if Mover.Pstats:
            self.pscCppInt.start()
        self.processCImpulsesAndIntegrate()
        if Mover.Pstats:
            self.pscCppInt.stop()

    def broadcastPositionUpdates(self):
        for mover in self._name2pyMovers.itervalues():
            mover._posHprBroadcast()
            
