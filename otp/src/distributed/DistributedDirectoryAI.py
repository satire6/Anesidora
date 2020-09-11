
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedDirectoryAI(DistributedObjectAI):
    """
    This object has no attributes and none of them get created, but it
    is still needed.  It is used as a parent for the individual games.
    The dc system uses the parenting rules as if this object existed.
    """
    pass
