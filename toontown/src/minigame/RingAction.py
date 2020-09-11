"""RingAction.py: contains the RingAction class"""

from direct.directnotify import DirectNotifyGlobal
import RingTrack

"""
see RingTrack.py
"""

class RingAction:
    """RingAction abstract base class; should not be used directly"""
    notify = DirectNotifyGlobal.directNotify.newCategory("RingAction")

    def __init__(self):
        pass

    def eval(self, t):
        """eval(self, float:[0..1])
        Evaluates a ringAction at a normalized (0..1) time t
        returns a normalized (x,y) pair
        """
        return (0,0)

class RingActionStaticPos(RingAction):
    """RingActionStaticPos: use for a ring that doesn't move"""
    def __init__(self, pos):
        RingAction.__init__(self)
        self.__pos = pos

    def eval(self, t):
        return self.__pos

class RingActionFunction(RingAction):
    """RingActionFunction: specify ring's motion with a function"""
    def __init__(self, func, args):
        assert(callable(func))

        RingAction.__init__(self)
        self.__func = func
        self.__args = args

    def eval(self, t):
        return self.__func(t, *self.__args)

class RingActionRingTrack(RingAction):
    """RingActionRingTrack: use a ring track to specify ring's motion;
    embed a ring track within another ring track"""
    def __init__(self, ringTrack):
        RingAction.__init__(self)
        self.__track = ringTrack

    def eval(self, t):
        return self.__track.eval(t)
