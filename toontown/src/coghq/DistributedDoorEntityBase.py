


def stubFunction(*args):
    """
    This function is a stub out function for callbacks.
    It intenionally ignores all of its parameters and
    does nothing.
    """
    pass


class LockBase:
    stateNames =     ['off',  'locking', 'locked', 'unlocking', 'unlocked']
    stateDurations = [ None,   3.5,       None,     4.0,         None]
    #                  off     off        off       off          on
    #                  locked  locked     locked    locked       unlocked

class DistributedDoorEntityBase:
    stateNames =     ['off',  'opening', 'open', 'closing', 'closed']
    stateDurations = [ None,   5.0,       1.0,    6.0,       None]
    #                  off     off        off     off        on
    #                  open    open       open    open       closed
