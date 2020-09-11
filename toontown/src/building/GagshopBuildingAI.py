from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorAI
import DistributedGagshopInteriorAI
import FADoorCodes
import DoorTypes
from toontown.toon import NPCToons
from toontown.quest import Quests

# This is not a distributed class... It just owns and manages some distributed
# classes.

class GagshopBuildingAI:
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
        self.door.requestDelete()
        del self.door
        self.insideDoor.requestDelete()
        del self.insideDoor
        self.interior.requestDelete()
        del self.interior
        return

    def setup(self, blockNumber):
        # The interior
        self.interior=DistributedGagshopInteriorAI.DistributedGagshopInteriorAI(
            blockNumber, self.air, self.interiorZone)

        #desc = (self.interiorZone, "HQ Officer", ('dls', 'ms', 'm', 'm', 6,0,6,6,40,8), "m", 1, 0)
        #self.npc = NPCToons.createNPC(self.air, Quests.ToonHQ, desc, self.interiorZone)

        self.npcs = NPCToons.createNpcsInZone(self.air, self.interiorZone)

        self.interior.generateWithRequired(self.interiorZone)
        # Outside door 
        door=DistributedDoorAI.DistributedDoorAI(
            self.air, blockNumber, DoorTypes.EXT_STANDARD)
        # Inside door 
        insideDoor=DistributedDoorAI.DistributedDoorAI(
            self.air,
            blockNumber,
            DoorTypes.INT_STANDARD)
        # Tell them about each other:
        door.setOtherDoor(insideDoor)
        insideDoor.setOtherDoor(door)
        # Put them in the right zones
        door.zoneId=self.exteriorZone
        insideDoor.zoneId=self.interiorZone
        # Now that they both now about each other, generate them:
        door.generateWithRequired(self.exteriorZone)
        insideDoor.generateWithRequired(self.interiorZone)
        # keep track of them:
        self.door=door
        self.insideDoor=insideDoor
        return
