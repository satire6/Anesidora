##########################################################################
# Module: DistributedKartPad.py
# Purpose: This class provides the basic methods and data members for
#          derived classes which need to handle a number of karts for
#          racing or viewing.
# Date: 6/28/05
# Author: jjtaylor
##########################################################################

##########################################################################
# Panda Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject

if(__debug__):
    import pdb

class DistributedKartPad(DistributedObject):
    """
    Purpose: Add Comments Here...
    """

    ######################################################################
    # Class Variables
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedKartPad")

    def __init__(self, cr):
        """
        Purpose: Comments go here

        Params: cr - The Toontown Client Repository.
        Return: None
        """

        # Initialize the Super Class
        DistributedObject.__init__(self, cr)
        self.startingBlocks = []

    def delete(self):
        """
        Comment:

        Params: None
        Return: None
        """

        # Remove references to allow for proper memory cleanup.
        del self.startingBlocks

        # Perform the remaining delete operation as defined by the
        # Super Class.
        DistributedObject.delete(self)

    def setArea(self, area):
        """
        Purpose: Comments go here...

        Params: area - the area of the zone where its found.
        Return: None
        """
        self.area = area

    def getArea(self):
        """
        Purpose: Comments go here...

        Params: None
        Return: area - the area of the zone where its found.
        """
        return self.area

    def addStartingBlock(self, block):
        """
        Comment:

        Params: block - the kart block that is associated to the pad.
        Return: None
        """

        self.startingBlocks.append(block)
        self.notify.debug("KartPad %s has added starting block %s" % (self.doId, block.doId))


