##########################################################################
# Module: KartShopBuildingAI.py
# Purpose: This module oversees the construction of the KartShop Interior
#          and KartShop NPC objects on the AI Server-side.
# Date: 6/9/05
# Author: jjtaylor (jjtaylor@schellgames.com)
##########################################################################

##########################################################################
# Panda/Direct Import Modules
##########################################################################
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *

##########################################################################
# Toontwon Import Modules
##########################################################################
from toontown.building import FADoorCodes, DoorTypes
from toontown.building.DistributedDoorAI import DistributedDoorAI
from toontown.building.DistributedKartShopInteriorAI import DistributedKartShopInteriorAI
from toontown.hood import ZoneUtil
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals

if( __debug__ ):
    import pdb

class KartShopBuildingAI:
    """
    Purpose: The KartShopBuildingAI Class oversees the creation of the
    KartShop Interior Object as well as the NPC clerks that are found
    within the KartShop.
    """

    # Initialize Class Variables
    notify = DirectNotifyGlobal.directNotify.newCategory( "KartShopBuildingAI" )

    def __init__( self, air, exteriorZone, interiorZone, blockNumber ):
        """
        Purpose: The __init__ Method provides the appropriate initialization
        of the KartShopBuildingAI object, including instance variables.

        Params: air - Reference to the AI Repository.
                exteriorZone - b
                interiorZone - b 
                blockNumber - b
        Return: None
        """
        self.air = air
        self.exteriorZone = exteriorZone
        self.interiorZone = interiorZone

        self.setup( blockNumber )

    def cleanup( self ):
        """
        Purpose: The cleanup Method properly handles the cleanup of the
        references and objects that are associated with the 
        """

        # Request Delete for NPC Objects
        for npc in self.npcs:
            npc.requestDelete()
        del self.npcs

        # Request Delete for Door Objects
        self.outsideDoor0.requestDelete()
        self.outsideDoor1.requestDelete()
        self.insideDoor0.requestDelete()
        self.insideDoor1.requestDelete()

        # Remove door object references
        del self.outsideDoor0, self.insideDoor0
        del self.outsideDoor1, self.insideDoor1

        self.kartShopInterior.requestDelete()
        del self.kartShopInterior

    def setup( self, blockNumber ):        
        # Create the Interior Object on the AI Side
        self.kartShopInterior = DistributedKartShopInteriorAI( blockNumber, self.air, self.interiorZone )
        # Initialize the npc clerks.
        self.npcs = NPCToons.createNpcsInZone( self.air, self.interiorZone )

        # Tell the DistributedKartShopInteriorAI object to generate.
        self.kartShopInterior.generateWithRequired( self.interiorZone )

        # Handle the Door Generation.
        # TODO - NEED TO CHANGE THE DOOR DGG.TYPE AND HANDLE IT IN DistributedDoor.py
        self.outsideDoor0 = DistributedDoorAI( self.air, blockNumber, DoorTypes.EXT_KS, doorIndex = 1 )
        self.outsideDoor1 = DistributedDoorAI( self.air, blockNumber, DoorTypes.EXT_KS, doorIndex = 2 )
        self.insideDoor0 = DistributedDoorAI( self.air, blockNumber, DoorTypes.INT_KS, doorIndex = 1 )
        self.insideDoor1 = DistributedDoorAI( self.air, blockNumber, DoorTypes.INT_KS, doorIndex = 2 )

        # Assign inside and outside doors to one another, respectively.
        self.outsideDoor0.setOtherDoor( self.insideDoor0 )
        self.outsideDoor1.setOtherDoor( self.insideDoor1 )
        self.insideDoor0.setOtherDoor( self.outsideDoor0 )
        self.insideDoor1.setOtherDoor( self.outsideDoor1 )
        
        # Place the doors in the proper zones.
        self.outsideDoor0.zoneId = self.exteriorZone
        self.outsideDoor1.zoneId = self.exteriorZone
        self.insideDoor0.zoneId = self.interiorZone
        self.insideDoor1.zoneId = self.interiorZone

        # Generate the Doors
        self.outsideDoor0.generateWithRequired( self.exteriorZone )
        self.outsideDoor1.generateWithRequired( self.exteriorZone )
        self.insideDoor0.generateWithRequired( self.interiorZone )
        self.insideDoor1.generateWithRequired( self.interiorZone )
        
        self.outsideDoor0.sendUpdate( "setDoorIndex", [ self.outsideDoor0.getDoorIndex() ] )
        self.outsideDoor1.sendUpdate( "setDoorIndex", [ self.outsideDoor1.getDoorIndex() ] )
        self.insideDoor0.sendUpdate( "setDoorIndex", [ self.insideDoor0.getDoorIndex() ] )
        self.insideDoor1.sendUpdate( "setDoorIndex", [ self.insideDoor1.getDoorIndex() ] )
