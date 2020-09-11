""" DistributedDoorAI module: contains the DistributedDoorAI
    class, the server side representation of a 'landmark door'."""
from direct.directnotify import DirectNotifyGlobal
from toontown.building import DistributedDoorAI

class DistributedAnimDoorAI(DistributedDoorAI.DistributedDoorAI):
    """
    The server side representation of a single anim door of an animated landmark
    building.
    Too many things have changed to stuff it in regular DistributedDoor.py
    """


    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimDoorAI')

    def __init__(self, air, blockNumber, doorType, doorIndex=0,
                 lockValue=0, swing=3):
        """
        blockNumber: the landmark building number (from the name)
        doorIndex: Each door must have a unique index.
        """
        #import pdb; pdb.set_trace()
        assert(self.notify.debug(str(blockNumber)+" DistributedAnimDoorAI("
                "%s, %s)" % ("the air", str(blockNumber))))
        DistributedDoorAI.DistributedDoorAI.__init__(self, air,
                                                     blockNumber, doorType,
                                                     doorIndex, lockValue,
                                                     swing)

