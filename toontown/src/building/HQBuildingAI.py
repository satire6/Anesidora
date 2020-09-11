from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorAI
import DistributedHQInteriorAI
import FADoorCodes
import DoorTypes
from toontown.toon import NPCToons
from toontown.quest import Quests

# This is not a distributed class... It just owns and manages some distributed
# classes.

class HQBuildingAI:
    def __init__(self, air, exteriorZone, interiorZone, blockNumber):
        # While this is not a distributed object, it needs to know about
        # the repository.
        self.air = air
        self.exteriorZone = exteriorZone
        self.interiorZone = interiorZone
        
        self.setup(blockNumber)

    def cleanup(self):
        for npc in self.npcs:
            npc.requestDelete()
        del self.npcs
        self.door0.requestDelete()
        del self.door0
        self.door1.requestDelete()
        del self.door1
        self.insideDoor0.requestDelete()
        del self.insideDoor0
        self.insideDoor1.requestDelete()
        del self.insideDoor1
        self.interior.requestDelete()
        del self.interior
        return

    def setup(self, blockNumber):
        # The interior
        self.interior=DistributedHQInteriorAI.DistributedHQInteriorAI(
            blockNumber, self.air, self.interiorZone)

        #desc = (self.interiorZone, "HQ Officer", ('dls', 'ms', 'm', 'm', 6,0,6,6,40,8), "m", 1, 0)
        #self.npc = NPCToons.createNPC(self.air, Quests.ToonHQ, desc, self.interiorZone)

        self.npcs = NPCToons.createNpcsInZone(self.air, self.interiorZone)

        self.interior.generateWithRequired(self.interiorZone)
        # Outside door 0. 
        door0=DistributedDoorAI.DistributedDoorAI(
            self.air, blockNumber, DoorTypes.EXT_HQ,
            doorIndex=0)
        # Outside door 1. 
        door1=DistributedDoorAI.DistributedDoorAI(
            self.air, blockNumber, DoorTypes.EXT_HQ,
            doorIndex=1)
        # Inside door 0. 
        insideDoor0=DistributedDoorAI.DistributedDoorAI(
            self.air,
            blockNumber,
            DoorTypes.INT_HQ,
            doorIndex=0)
        # Inside door 1.
        insideDoor1=DistributedDoorAI.DistributedDoorAI(
            self.air,
            blockNumber,
            DoorTypes.INT_HQ,
            doorIndex=1)
        # Tell them about each other:
        door0.setOtherDoor(insideDoor0)
        insideDoor0.setOtherDoor(door0)
        door1.setOtherDoor(insideDoor1)
        insideDoor1.setOtherDoor(door1)
        # Put them in the right zones
        door0.zoneId=self.exteriorZone
        door1.zoneId=self.exteriorZone
        insideDoor0.zoneId=self.interiorZone
        insideDoor1.zoneId=self.interiorZone
        # Now that they both now about each other, generate them:
        door0.generateWithRequired(self.exteriorZone)
        door1.generateWithRequired(self.exteriorZone)
        door0.sendUpdate("setDoorIndex", [door0.getDoorIndex()])
        door1.sendUpdate("setDoorIndex", [door1.getDoorIndex()])
        insideDoor0.generateWithRequired(self.interiorZone)
        insideDoor1.generateWithRequired(self.interiorZone)
        insideDoor0.sendUpdate("setDoorIndex", [insideDoor0.getDoorIndex()])
        insideDoor1.sendUpdate("setDoorIndex", [insideDoor1.getDoorIndex()])
        # keep track of them:
        self.door0=door0
        self.door1=door1
        self.insideDoor0=insideDoor0
        self.insideDoor1=insideDoor1        
        return
       
    def isSuitBlock(self):
        # For compatibility with DistributedBuildingAI
        return 0

    def isSuitBuilding(self):
        # For compatibility with DistributedBuildingAI
        return 0

    def isCogdo(self):
        # For compatibility with DistributedBuildingAI
        return 0

    def isEstablishedSuitBlock(self):
        # For compatibility with DistributedBuildingAI
        return 0
