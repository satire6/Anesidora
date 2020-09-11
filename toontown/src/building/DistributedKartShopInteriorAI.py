##########################################################################
# Module: DistributedKartShopInteriorAI.py
# Purpose: This module oversees the construction of the KartShop Interior
#          on the AI server side.
# Date: 6/8/05
# Author: jjtaylor (jjtaylor@schellgames.com)
##########################################################################

##########################################################################
# Panda/Direct Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedKartShopInteriorAI( DistributedObjectAI ):
    """
    Purpose: The DistributedKartShopInteriorAI class represents the
    interior of the KartShop on the AI server side.
    """

    ######################################################################
    # Class Variable Definitions
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "DistributedKartShopInteriorAI" )

    def __init__( self, block, air, zoneId ):
        """
        Purpose: The __init__ Method handles the initialization of the
        KartShopInteriorAI object by initializing the super class, and
        setting the instance variables.

        Params: block - the block of the KartShop
                air - The AI Repository which stores all of the
                      distributed objects on the AI Server side.
                zoneId - the kart shops zone id
        Return: None
        """

        # Initialize the Super Class
        DistributedObjectAI.__init__( self, air )

        # Initialize instance variables
        self.block = block
        self.zoneId = zoneId

    def generate( self ):
        """
        Purpose: The generate Method performs the necessary object
        setup.

        Params: None
        Return: None
        """
        DistributedObjectAI.generate( self )

    def getZoneIdAndBlock( self ):
        """
        Purpose: The getZoneIdAndBlock Method returns the zoneId and
        the block of the KartShopInterior.

        Params: None
        Return: [] - containing the zoneId and block.
        """
        return [ self.zoneId, self.block ]
