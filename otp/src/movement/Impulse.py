from pandac.PandaModules import *
from direct.showbase import DirectObject

class Impulse(DirectObject.DirectObject):
    """derive from this to do something more interesting"""
    def __init__(self):
        self.mover = None
        self.nodePath = None

    def destroy(self):
        pass

    # override this
    # set your impulse's influence for this pass on its Mover
    def _process(self, dt):
        pass

    # called internally by Mover when we're added or removed
    def _setMover(self, mover):
        self.mover = mover
        self.nodePath = self.mover.getNodePath()
        self.VecType = self.mover.VecType
    def _clearMover(self, mover):
        if self.mover == mover:
            self.mover = None
            self.nodePath = None

    def isCpp(self):
        return 0
