from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorAI
import DistributedPetshopInteriorAI
import FADoorCodes
import DoorTypes
from toontown.toon import NPCToons
from toontown.toonbase import ToontownGlobals
from toontown.quest import Quests
from toontown.pets import DistributedPetAI, PetTraits, PetUtil
from toontown.hood import ZoneUtil

# This is not a distributed class... It just owns and manages some distributed
# classes.

class PetshopBuildingAI:
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
        self.interior=DistributedPetshopInteriorAI.DistributedPetshopInteriorAI(
            blockNumber, self.air, self.interiorZone)

        self.npcs = NPCToons.createNpcsInZone(self.air, self.interiorZone)

        seeds = self.air.petMgr.getAvailablePets(1, len(self.npcs))
        #for i in range(len(self.npcs)):
        #    self.wanderingPets = self.createPet(self.npcs[i].doId, seeds[i])

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

    def createPet(self, ownerId, seed):
        zoneId = self.interiorZone
        safeZoneId = ZoneUtil.getCanonicalSafeZoneId(zoneId)
        name, dna, traitSeed = PetUtil.getPetInfoFromSeed(seed, safeZoneId)

        pet = DistributedPetAI.DistributedPetAI(self.air, dna = dna)
        pet.setOwnerId(ownerId)
        pet.setPetName(name)
        pet.traits = PetTraits.PetTraits(traitSeed=traitSeed, safeZoneId=safeZoneId)
        pet.generateWithRequired(zoneId)
        pet.setPos(0, 0, 0)
        pet.b_setParent(ToontownGlobals.SPRender)
