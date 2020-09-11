"""Ring.py: contains the ring class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import NodePath
import RingTrack

class Ring(NodePath):
    """ring for ring minigame"""

    def __init__(self, moveTrack, tOffset, posScale = 1.):
        NodePath.__init__(self)
        self.assign(hidden.attachNewNode(\
            base.localAvatar.uniqueName('ring')))

        self.setMoveTrack(moveTrack)
        self.setTOffset(tOffset)
        self.setPosScale(posScale)
        self.setT(0.)

    def setMoveTrack(self, moveTrack):
        self.__moveTrack = moveTrack

    def setTOffset(self, tOffset):
        """setTOffset(self, float)
        tOffset is an offset in (0..1) into the ring's movement
        cycle. The movement of a ring with tOffset==.5 will be
        50% out-of-phase with the movement of a ring with tOffset==0.
        """
        self.__tOffset = float(tOffset)
        assert(self.__tOffset >= 0. and self.__tOffset <= 1.)

    def setPosScale(self, posScale):
        """setPosScale(self, float)
        posScale is a scaling factor for the position of the ring
        the ring's position varies within the 'unit square' of [-1..1,-1..1],
        multiplied by this scaling factor
        """
        self.__posScale = posScale
        assert(self.__posScale > 0.)

    def setT(self, t):
        """setT(self, float:[0..1])
        updates the position of the ring for time t
        """
        pos = self.__moveTrack.eval((t + self.__tOffset) % 1.)
        self.setPos(pos[0] * self.__posScale,
                    0,
                    pos[1] * self.__posScale)
