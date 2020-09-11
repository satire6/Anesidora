##########################################################################
# Module: DistributedKartShopInterior.py
# Purpose: This module oversees the construction of the KartShop Interior
#          and KartShop NPCs on the client-side.
# Date: 6/8/05
# Author: jjtaylor (jjtaylor@schellgames.com)
##########################################################################

##########################################################################
# Panda/Direct Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pandac.PandaModules import *

##########################################################################
# Toontwon Import Modules
##########################################################################
from toontown.building import ToonInteriorColors
from toontown.hood import ZoneUtil
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *

if( __debug__ ):
    import pdb

class DistributedKartShopInterior( DistributedObject ):
    """
    Class: DistributedKartShopInterior
    Purpose: The class provides the interior of the KartShop on the
             client side. It also properly sets up the random NPCs
             which are generated as KartShopClerks.
    """

    ######################################################################
    # Class Variable Definitions
    ######################################################################
    notify = DirectNotifyGlobal.directNotify.newCategory( "DistributedKartShopInterior" )


    def __init__( self, cr ):
        """
        Purpose: The __init__ Method sets up the KartShop Interior object
        by initlaizing the super class as well as setting the appropriate
        dnaStore for the object.

        Params: cr - The client repository which maintains all client-side
                     distributed objects.
        Return: None
        """

        # Initialize the Super Class, then set the dna store.
        DistributedObject.__init__( self, cr )
        self.dnaStore = cr.playGame.dnaStore

    def generate( self ):
        """
        Purpose: The generate Method handles the basic generation of the
        KartShopInterior object by generating the super class.

        Params: None
        Return: None                  
        """
        DistributedObject.generate( self )

    def announceGenerate( self ):
        """
        Purpose: The announceGenerate Method tells the super class
        to send a message to the world that the object has been
        generated and all of its required fields have been filled in. It
        also sets up the Interior.

        Params: None
        Return: None
        """

        DistributedObject.announceGenerate( self )
        self.__handleInteriorSetup()

    def disable( self ):
        """
        Purpose: The disable Method performs the necessary cleanup
        of the KartShopInterior object on the client side.

        Params: None
        Return None
        """
        self.interior.removeNode()
        del self.interior
        DistributedObject.disable( self )
        

    def setZoneIdAndBlock( self, zoneId, block ):
        """
        Purpose: The setZoneIdAndBlock Method properly sets the zoneId
        and block of the interior.

        Params: zoneId - the zone id of the interior
                block - the block of the interior
        Return: None
        """
        self.zoneId = zoneId
        self.block = block

    def __handleInteriorSetup( self ):
        """
        Purpose: The __handleInteriorSetup Method properly sets up the
        interior of the Kart Shop on the client side.

        Params: None
        Return: None
        """

        # Load the appropriate Interior Model for the Kart Shop
        self.interior = loader.loadModel( 'phase_6/models/karting/KartShop_Interior' )
        self.interior.reparentTo( render )
        self.interior.flattenMedium()
