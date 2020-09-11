from direct.directnotify import DirectNotifyGlobal
import ZoneUtil
from toontown.building import DistributedBuildingMgrAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from pandac.PandaModules import *
from toontown.toon import NPCToons

class HoodDataAI:
    """

    A HoodDataAI object is created for each neighborhood; it owns the
    pointers to objects such as the suit planners and building
    managers, and can shut itself down cleanly on demand.

    """

    notify = DirectNotifyGlobal.directNotify.newCategory("HoodDataAI")

    def __init__(self, air, zoneId, canonicalHoodId):
        self.air = air
        self.zoneId = zoneId
        self.canonicalHoodId = canonicalHoodId
        self.treasurePlanner = None
        self.buildingManagers = []
        self.suitPlanners = []
        self.doId2do = {}

        # These members are used to balance WelcomeValley hoods.
        self.replacementHood = None
        self.redirectingToMe = []
        self.hoodPopulation = 0
        self.pgPopulation = 0

    def startup(self):
        self.createFishingPonds()
        self.createPartyPeople()
        self.createBuildingManagers()
        self.createSuitPlanners()

    def shutdown(self):
        self.setRedirect(None)

        if self.treasurePlanner:
            self.treasurePlanner.stop()
            self.treasurePlanner.deleteAllTreasuresNow()
            self.treasurePlanner = None

        for suitPlanner in self.suitPlanners:
            suitPlanner.requestDelete()
            del self.air.suitPlanners[suitPlanner.zoneId]
        self.suitPlanners = []

        for buildingManager in self.buildingManagers:
            buildingManager.cleanup()
            del self.air.buildingManagers[buildingManager.branchID]
        self.buildingManagers = []

        ButterflyGlobals.clearIndexes(self.zoneId)
        del self.fishingPonds
        for distObj in self.doId2do.values():
            distObj.requestDelete()
        del self.doId2do
        
        # Break back-pointers
        del self.air


    def addDistObj(self, distObj):
        self.doId2do[distObj.doId] = distObj

    def removeDistObj(self, distObj):
        del self.doId2do[distObj.doId]

    def createPartyPeople(self):
        partyHats = []
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
            dnaData = self.air.dnaDataMap.get(zone[0], None)
            if isinstance(dnaData, DNAData):
                foundPartyHats = self.air.findPartyHats(dnaData, zoneId )
                partyHats += foundPartyHats

        for distObj in partyHats:
            self.addDistObj(distObj)
            # NOTE: The PartyPerson NPCs are created below in createFishingPonds
            #       because that method creates all the NPCs in the hood

    def createFishingPonds(self):
        # Note: A list of fishing ponds is now maintanied for easier access
        #       when generating Pond Bingo Managers for Bingo Night.
        #       (JJT - 07/22/04)
        self.fishingPonds = []
        fishingPondGroups = []
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
            dnaData = self.air.dnaDataMap.get(zone[0], None)
            if isinstance(dnaData, DNAData):
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundFishingPonds, foundFishingPondGroups = self.air.findFishingPonds(dnaData, zoneId, area)
                self.fishingPonds += foundFishingPonds
                fishingPondGroups += foundFishingPondGroups
        for distObj in self.fishingPonds:
            self.addDistObj(distObj)
            # Every pond gets a fisherman
            npcs = NPCToons.createNpcsInZone(self.air, distObj.zoneId)
            # TODO-parties : Ask for clarification on this.
            # Since this creates all the NPCs in the zone, this creates the
            # party people for the party hat as well... but what if there are
            # no fishing ponds??
            for npc in npcs:
                self.addDistObj(npc)

        # Now look in the fishing pond DNAGroups for fishing spots
        fishingSpots = []
        for dnaGroup, distPond in zip(fishingPondGroups, self.fishingPonds):
            fishingSpots += self.air.findFishingSpots(dnaGroup, distPond)
        for distObj in fishingSpots:
            self.addDistObj(distObj)
     
    def createBuildingManagers(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[1]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                dnaStore = self.air.dnaStoreMap[zone[0]]
                mgr = DistributedBuildingMgrAI.DistributedBuildingMgrAI(
                    self.air, zoneId, dnaStore, self.air.trophyMgr)
                self.buildingManagers.append(mgr)
                self.air.buildingManagers[zoneId] = mgr
     
    def createSuitPlanners(self):
        for zone in self.air.zoneTable[self.canonicalHoodId]:
            if zone[2]:
                zoneId = ZoneUtil.getTrueZoneId(zone[0], self.zoneId)
                sp = DistributedSuitPlannerAI.DistributedSuitPlannerAI(
                    self.air, zoneId)
                sp.generateWithRequired(zoneId)
                sp.d_setZoneId(zoneId)

                # be sure to start up necessary tasks so the suit planner
                # is updated when needed
                #
                sp.initTasks()
                self.suitPlanners.append(sp)
                self.air.suitPlanners[zoneId] = sp

    def createButterflies(self, playground):
        ButterflyGlobals.generateIndexes(self.zoneId, playground)
        for i in range(0, ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for j in range(0, ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                bfly = DistributedButterflyAI.DistributedButterflyAI(
                    self.air, playground, i, self.zoneId)
                bfly.generateWithRequired(self.zoneId)
                bfly.start()
                self.addDistObj(bfly)
        

    # WelcomeValley hoods have some additional methods for managing
    # population balancing (via the WelcomeValleyManagerAI class).
    # These are provided here, but are not used for the static hoods.

    def setRedirect(self, replacementHood):
        # Indicates that this hood is now in Removing mode, and all
        # avatar requests to or within this hood are to be redirected
        # to the indicated other hood, which will also immediately
        # begin reporting this hood's population as its own.
        
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.remove(self)
        self.replacementHood = replacementHood
        if self.replacementHood:
            self.replacementHood[0].redirectingToMe.append(self)

    def hasRedirect(self):
        # Returns true if a redirect has been set, false otherwise.
        return self.replacementHood != None

    def getRedirect(self):
        # Returns the hood to which an avatar is to be redirected, or
        # self if redirect has not been enabled.

        if self.replacementHood == None:
            return self
        else:
            return self.replacementHood[0].getRedirect()

    def incrementPopulation(self, zoneId, increment):
        # Adds (or subtracts if negative) the indicated increment to
        # the population counters.  If zoneId represents a playground,
        # the increment is also added to the playground population.

        self.hoodPopulation += increment
        if ZoneUtil.isPlayground(zoneId):
            self.pgPopulation += increment

    def getHoodPopulation(self):
        # Returns the complete population of avatars within the hood,
        # including those within hoods that are currently redirecting
        # to this hood.
        
        population = self.hoodPopulation
        for hood in self.redirectingToMe:
            population += hood.getHoodPopulation()
        return population

    def getPgPopulation(self):
        # Returns the population of avatars within the playground
        # only, including those within hoods that are currently
        # redirecting to this hood.
        
        population = self.pgPopulation
        for pg in self.redirectingToMe:
            population += pg.getPgPopulation()
        return population
