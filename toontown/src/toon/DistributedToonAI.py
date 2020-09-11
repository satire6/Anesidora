from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from direct.directnotify import DirectNotifyGlobal
import ToonDNA
from toontown.suit import SuitDNA
import InventoryBase
import Experience
from otp.avatar import DistributedAvatarAI
from otp.avatar import DistributedPlayerAI
from direct.distributed import DistributedSmoothNodeAI
from toontown.toonbase import ToontownGlobals
from toontown.quest import QuestRewardCounter
from toontown.quest import Quests
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import SuitBattleGlobals
from direct.task import Task
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from direct.showbase import PythonUtil
from direct.distributed.ClockDelta import *
from toontown.toonbase.ToontownGlobals import *
import types
from toontown.fishing import FishGlobals
from toontown.fishing import FishCollection
from toontown.fishing import FishTank
from NPCToons import npcFriends,isZoneProtected
from toontown.coghq import CogDisguiseGlobals
import random
from toontown.chat import ResistanceChat
from toontown.racing import RaceGlobals
from toontown.hood import ZoneUtil
from toontown.toon import NPCToons

from toontown.estate import FlowerCollection
from toontown.estate import FlowerBasket
from toontown.estate import GardenGlobals
from toontown.golf import GolfGlobals

from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfoAI
from toontown.parties.InviteInfo import InviteInfoBase
from toontown.parties.PartyReplyInfo import PartyReplyInfoBase
from toontown.parties.PartyGlobals import InviteStatus

if simbase.wantPets:
    from toontown.pets import PetLookerAI, PetObserve
else:
    class PetLookerAI:
        class PetLookerAI:
            pass

if( simbase.wantKarts ):
    from toontown.racing.KartDNA import *

class DistributedToonAI(DistributedPlayerAI.DistributedPlayerAI,
                        DistributedSmoothNodeAI.DistributedSmoothNodeAI,
                        PetLookerAI.PetLookerAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonAI")

    maxCallsPerNPC = 100

    # factory type -> cog suit parts
    partTypeIds = {
        ToontownGlobals.FT_FullSuit: (CogDisguiseGlobals.leftLegIndex,
                                      CogDisguiseGlobals.rightLegIndex,
                                      CogDisguiseGlobals.torsoIndex,
                                      CogDisguiseGlobals.leftArmIndex,
                                      CogDisguiseGlobals.rightArmIndex,),
        ToontownGlobals.FT_Leg: (CogDisguiseGlobals.leftLegIndex,
                                 CogDisguiseGlobals.rightLegIndex,),
        ToontownGlobals.FT_Arm: (CogDisguiseGlobals.leftArmIndex,
                                 CogDisguiseGlobals.rightArmIndex,),
        ToontownGlobals.FT_Torso: (CogDisguiseGlobals.torsoIndex,),
        }
    
    def __init__(self, air):
        #if hasattr(simbase, 'trackDistributedToonAI'):
        #    import pdb; pdb.set_trace()
        
        DistributedPlayerAI.DistributedPlayerAI.__init__(self, air)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.__init__(self)
        # Record the repository
        self.air = air
        # Initialize our empty DNA.
        self.dna = ToonDNA.ToonDNA()
        self.inventory = None
        self.fishCollection = None
        self.fishTank = None
        self.experience = None
        self.quests = []
        self.cogs = []
        self.cogCounts = []
        
        self.NPCFriendsDict = {} 

        self.clothesTopsList = []
        self.clothesBottomsList = []

        # initialize these to lists of zeroes in case there is no
        # field in the database yet for old toons created before this
        # field existed.
        self.cogTypes = [0, 0, 0, 0]
        self.cogLevel = [0, 0, 0, 0]
        self.cogParts = [0, 0, 0, 0]
        self.cogRadar = [0, 0, 0, 0]
        self.cogIndex = -1
        self.disguisePageFlag = 0
        self.buildingRadar = [0, 0, 0, 0]
        self.fishingRod = 0
        self.fishingTrophies = []
        self.trackArray = []
        self.emoteAccess = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.maxBankMoney = 1000
        self.gardenSpecials = []#[(0,2), (1,2), (2,2), (3,2)]

        self.houseId = 0
        self.posIndex = 0
        
        self.savedCheesyEffect = ToontownGlobals.CENormal
        self.savedCheesyHoodId = 0
        self.savedCheesyExpireTime = 0
        self.ghostMode = 0
        self.immortalMode = 0
        self.numPies = 0
        self.pieType = 0

        # Most of the time, this is false.  But during a battle round,
        # we set this true, to tell the toon to temporarily accumulate
        # toonups beyond full health (and not to broadcast current hp
        # to the client), so that it can be fixed up after the battle
        # round is over.
        self.hpOwnedByBattle = 0

        if simbase.wantPets:
            self.petTrickPhrases = []

        if simbase.wantBingo:
            self.bingoCheat = False

        self.customMessages = []
        self.catalogNotify = ToontownGlobals.NoItems
        self.mailboxNotify = ToontownGlobals.NoItems
        self.catalogScheduleCurrentWeek = 0
        self.catalogScheduleNextTime = 0
        self.monthlyCatalog = CatalogItemList.CatalogItemList()
        self.weeklyCatalog = CatalogItemList.CatalogItemList()
        self.backCatalog = CatalogItemList.CatalogItemList()
        self.onOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        #self.onGiftOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        self.onGiftOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.mailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
        self.awardMailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
        self.onAwardOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        #self.deliveryboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.GiftTag)

        self.kart = None

        # Initialize the Kart stuff
        if( simbase.wantKarts ):
            self.kartDNA = [ -1 ] * ( getNumFields() )
            self.tickets = 200
            self.allowSoloRace = False
            self.allowRaceTimeout = True
            
        #battle stuff, first used for boarding parties
        self.setBattleId(0)


        #Gardening stuff
        self.gardenStarted = False
        self.flowerCollection = None
        self.shovel = 0
        self.shovelSkill = 0
        self.wateringCan = 0
        self.wateringCanSkill = 0
        
        self.hatePets = 1

        # Golf Stuff
        self.golfHistory = None
        self.golfHoleBest = None
        self.golfCourseBest = None
        self.unlimitedSwing = False
        
        self.previousAccess = None

        # mail stuff
        self.numMailItems = 0
        self.simpleMailNotify = ToontownGlobals.NoItems
        self.inviteMailNotify = ToontownGlobals.NoItems

        # parties
        self.invites = []
        self.hostedParties = []
        self.partiesInvitedTo = []
        self.partyReplyInfoBases = []        

    #def __del__(self):
        #if hasattr(simbase, 'trackDistributedToonAI'):
        #    self.notify.info('---- __del__ DistributedToonAI %d ' % self.doId)            
        #    import pdb; pdb.set_trace()
        #pass


    def generate(self):
        # super spammy hack to track down ai crash
        # self.notify.info('Got generate for %d' % self.doId)
        # self.air.writeServerEvent('generate' , self.doId, '')
        DistributedPlayerAI.DistributedPlayerAI.generate(self)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.generate(self)
        
        
    def announceGenerate(self):
        # super spammy hack to track down ai crash
        # self.notify.info('Got announceGenerate for %d' % self.doId)
        # self.air.writeServerEvent('announceGenerate' , self.doId, '')
        DistributedPlayerAI.DistributedPlayerAI.announceGenerate(self)
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.announceGenerate(self)
        if self.isPlayerControlled():
            messenger.send('avatarEntered', [self])
            
    ### Field definitions

    def sendDeleteEvent(self):
        if simbase.wantPets:
            # before we let the rest of the system know we're about to be
            # deleted, see if we need to notify any pets. The act of sending
            # the event may destroy data that we need in order to notify the
            # pets.
            # Turns out that the EstateMgrAI gets an event from the client
            # telling it that the player has left the estate; on an alt+F4,
            # that comes in before this is called, so we've already left the
            # estate at this point. We still need the 'wasInEstate' mechanism.
            isInEstate = self.isInEstate()
            wasInEstate = self.wasInEstate()
            if isInEstate or wasInEstate:
                # announce to the pets that we're logging out
                PetObserve.send(self.estateZones, PetObserve.PetActionObserve(
                    PetObserve.Actions.LOGOUT, self.doId))
                if wasInEstate:
                    self.cleanupEstateData()
                    
        DistributedAvatarAI.DistributedAvatarAI.sendDeleteEvent(self)
        

            

    def delete(self):
        self.notify.debug('----Deleting DistributedToonAI %d ' % self.doId)
        if self.isPlayerControlled():
            messenger.send('avatarExited', [self])
        if simbase.wantPets:
            if self.isInEstate():
                print "ToonAI - Exit estate toonId:%s" % (self.doId)
                self.exitEstate()
            if self.zoneId != ToontownGlobals.QuietZone:
                # simulate a zone change for the benefit of the pets
                self.announceZoneChange(ToontownGlobals.QuietZone,
                                        self.zoneId)
        
        # Stop the cheesy effect timer if we're waiting.
        taskName = self.uniqueName('cheesy-expires')
        taskMgr.remove(taskName)
        # Stop the catalog timer too.
        taskName = self.uniqueName('next-catalog')
        taskMgr.remove(taskName)
        taskName = self.uniqueName('next-delivery')
        taskMgr.remove(taskName)
        taskName = self.uniqueName('next-award-delivery')
        taskMgr.remove(taskName)        
        taskName = ("next-bothDelivery-%s" % (self.doId))
        taskMgr.remove(taskName)
        self.stopToonUp()
        
        del self.dna
        if self.inventory:
            self.inventory.unload()
        del self.inventory
        del self.experience
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.destroy(self)
        del self.kart
            
        self._sendExitServerEvent()
        
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        DistributedPlayerAI.DistributedPlayerAI.delete(self)

    def deleteDummy(self):
        """
        we create a dummy DistributedToonAI when we close the window in a building battle
        So we need to clear it properly
        """
        self.notify.debug('----deleteDummy DistributedToonAI %d ' % self.doId)        
        if self.inventory:
            self.inventory.unload()
        del self.inventory

        # Stop the catalog timer too. #we get this case when we open a somebody else's closet
        taskName = self.uniqueName('next-catalog')
        taskMgr.remove(taskName)        

    def patchDelete(self):
        # called by the patcher to prevent memory leaks
        del self.dna
        if self.inventory:
            self.inventory.unload()
        del self.inventory
        del self.experience
        if simbase.wantPets:
            PetLookerAI.PetLookerAI.destroy(self)
        # prevent a crash; we do not own our doId and do not have a zoneId
        self.doNotDeallocateChannel = True
        self.zoneId = None
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.delete(self)
        DistributedPlayerAI.DistributedPlayerAI.delete(self)

    def handleLogicalZoneChange(self, newZoneId, oldZoneId):
        DistributedAvatarAI.DistributedAvatarAI.handleLogicalZoneChange(
            self, newZoneId, oldZoneId)

        # make sure ghost mode is disabled on zone change (fixes furniture arranger exploit)
        self.b_setGhostMode(0)
        
        # not quite sure where to do this - we need to assign teleport access
        # to the toon when he enters Goofy Stadium
        zoneId = ZoneUtil.getCanonicalZoneId(newZoneId)
        if zoneId == ToontownGlobals.GoofySpeedway:
            if not self.hasTeleportAccess(ToontownGlobals.GoofySpeedway):
                self.addTeleportAccess(zoneId)
        # NOTE: If others need to listen for zoneId changes then please remove the if statements
        elif zoneId == ToontownGlobals.ToonHall:
            messenger.send("ToonEnteredZone", [self.doId, zoneId])
        zoneId = ZoneUtil.getCanonicalZoneId(oldZoneId)
        if zoneId == ToontownGlobals.ToonHall:
            messenger.send("ToonLeftZone", [self.doId, zoneId])
        if simbase.wantPets:
            isInEstate = self.isInEstate()
            # we may have just left
            wasInEstate = self.wasInEstate()
            if isInEstate or wasInEstate:
                self.announceZoneChange(newZoneId, oldZoneId)
                if wasInEstate:
                    # don't need this data anymore
                    self.cleanupEstateData()

    def announceZoneChange(self, newZoneId, oldZoneId):
        # let the pets know about the zone change
        from toontown.pets import PetObserve

        self.air.welcomeValleyManager.toonSetZone(self.doId, newZoneId)

        # if we're in an estate, make sure to broadcast this message
        # to all estate zones
        broadcastZones = [oldZoneId, newZoneId]
        if self.isInEstate() or self.wasInEstate():
            broadcastZones = union(broadcastZones, self.estateZones)

        PetObserve.send(broadcastZones,
                        PetObserve.PetActionObserve(
            PetObserve.Actions.CHANGE_ZONE, self.doId,
            (oldZoneId, newZoneId)))
        
    def b_setDNAString(self, string):
        self.d_setDNAString(string)
        self.setDNAString(string)

    def d_setDNAString(self, string):
        self.sendUpdate('setDNAString', [string])

    def setDNAString(self, string):
        self.dna.makeFromNetString(string)

    def getDNAString( self ):
        """
        Function:    retrieve the dna information from this suit, called
                     whenever a client needs to create this suit
        Returns:     netString representation of this suit's dna
        """
        return self.dna.makeNetString()

    def getStyle(self):
        # Returns the dna.  This mimicks a similar function on Avatar.py.
        return self.dna

    def b_setExperience(self, experience):
        self.d_setExperience(experience)
        self.setExperience(experience)

    def d_setExperience(self, experience):
        self.sendUpdate('setExperience', [experience])

    def setExperience(self, experience):
        self.experience = Experience.Experience(experience, self)

    def getExperience(self):
        # This returns the experience formatted for the net, not
        # directly usable.
        return self.experience.makeNetString()

    def b_setInventory(self, inventory):        
        self.setInventory(inventory)
        self.d_setInventory(self.getInventory())

    def d_setInventory(self, inventory):
        self.sendUpdate('setInventory', [inventory])

    def setInventory(self, inventoryNetString):
        if self.inventory:
            # Update the inventory
            self.inventory.updateInvString(inventoryNetString)
        else:
            self.inventory = InventoryBase.InventoryBase(self,
                                                         inventoryNetString)
                                                         
        #here we look to see if new gags have been added

        emptyInv = InventoryBase.InventoryBase(self)
        emptyString = emptyInv.makeNetString()
        lengthMatch = len(inventoryNetString) - len(emptyString)
        if lengthMatch != 0:
            #Moving from 7 tracks and 6 levels to 7 tracks and 7 levels
            if len(inventoryNetString) == 42:
                oldTracks = 7
                oldLevels = 6
            elif len(inventoryNetString) == 49:
                oldTracks = 7
                oldLevels = 7
            else:
                #flags for when the solution is unknown
                oldTracks = 0
                oldLevels = 0
                
            if oldTracks == 0 and oldLevels == 0:
                #if no handcoded solution exists we reset the toon's inventory and give them
                #a restock, only including gags you can buy in the shop
                #import pdb; pdb.set_trace()
                #print(lengthMatch)
                #print(self.inventory)
                self.notify.warning("reseting invalid inventory to MAX on toon: %s" % (self.doId))
                self.inventory.zeroInv()
                self.inventory.maxOutInv(1)
                #print(self.inventory)                
            else:    
                #handles the conversion for known solutions
                newInventory = InventoryBase.InventoryBase(self)
                oldList = emptyInv.makeFromNetStringForceSize(inventoryNetString, oldTracks, oldLevels)
                #print("inventory %s" % (self.inventory))
                #print("oldList %s" % (oldList))
                for indexTrack in range(0,oldTracks):
                    for indexGag in range(0,oldLevels):
                        newInventory.addItems(indexTrack, indexGag, oldList[indexTrack][indexGag])
                #print("new inventory %s" % (newInventory))
                self.inventory.unload()
                self.inventory = newInventory
                #import pdb; pdb.set_trace()
            self.d_setInventory(self.getInventory())
            
        
            
            
    def getInventory(self):
        # This returns the inventory formatted for the net, not
        # directly usable.
        return self.inventory.makeNetString()

    def doRestock(self, noUber = 1):
        self.inventory.zeroInv()
        self.inventory.maxOutInv(noUber)
        self.d_setInventory(self.inventory.makeNetString())

    def setDefaultShard(self, shard):
        self.defaultShard = shard
        self.notify.debug("setting default shard to %s" % shard)

    def getDefaultShard(self):
        return self.defaultShard
        
    def setDefaultZone(self, zone):
        self.defaultZone = zone
        self.notify.debug("setting default zone to %s" % zone)        

    def getDefaultZone(self):
        return self.defaultZone

    def setShtickerBook(self, string):
        self.notify.debug("setting shticker book to %s" % string)        

    def getShtickerBook(self):
        return ""

    def d_setFriendsList(self, friendsList):
        self.sendUpdate("setFriendsList", [friendsList])
        return None

    def setFriendsList(self, friendsList):
        self.notify.debug("setting friends list to %s" % self.friendsList)
        self.friendsList = friendsList
        # If the friendsList is nonEmpty, notify the quest manager
        if friendsList:
            # Assume the newest one on the list is the one we just
            # made friends with. Is it? Check with Roger.
            friendId = friendsList[-1]
            # See if the otherAv is logged in
            otherAv = self.air.doId2do.get(friendId)
            # Tell the quest manager. Note: there is a design flaw here
            # whereby the player could remove a friend and still get credit
            # for this a friend quest. Really we need to know when a friend
            # is added, not simply when the friends list changed (add or
            # remove)
            self.air.questManager.toonMadeFriend(self, otherAv)

    def getFriendsList(self):
        return self.friendsList

    def extendFriendsList(self, friendId, friendCode):
        # This is called only by the friend manager when a new friend
        # transaction is successfully completed.  Its purpose is
        # simply to update the AI's own copy of the avatar's friends
        # list, mainly so that the quest manager can reliably know
        # if the avatar has any friends.

        # First, see if we already had this friend.
        for i in range(len(self.friendsList)):
            friendPair = self.friendsList[i]
            if friendPair[0] == friendId:
                # We did.  Update the code.
                self.friendsList[i] = (friendId, friendCode)
                return

        # We didn't already have this friend; tack it on.
        self.friendsList.append((friendId, friendCode))

        # Note that if an avatar *breaks* a friendship, the AI never
        # hears about it.  So our friends list will not be 100%
        # up-to-date, but it will at least be good enough for the
        # quest manager.

    def d_setMaxNPCFriends(self, max):
        self.sendUpdate("setMaxNPCFriends", [self.maxNPCFriends])

    def setMaxNPCFriends(self, max):
        self.maxNPCFriends = max

    def b_setMaxNPCFriends(self, max):
        self.setMaxNPCFriends(max)
        self.d_setMaxNPCFriends(max)
        
    def getMaxNPCFriends(self):
        return self.maxNPCFriends
        
    def getBattleId(self):
        if self.battleId >= 0:
            return self.battleId
        else:
            return 0
        
    def b_setBattleId(self, battleId):
        self.setBattleId(battleId)
        self.d_setBattleId(battleId)        
        
    def d_setBattleId(self, battleId):
        if self.battleId >= 0:
            self.sendUpdate("setBattleId", [battleId])
        else:
            self.sendUpdate("setBattleId", [0])
        
        
    def setBattleId(self, battleId):
        self.battleId = battleId

    def d_setNPCFriendsDict(self, NPCFriendsDict):
        NPCFriendsList = []
        for friend in NPCFriendsDict.keys():
            NPCFriendsList.append((friend, NPCFriendsDict[friend]))
        self.sendUpdate("setNPCFriendsDict", [NPCFriendsList])
        return None

    def setNPCFriendsDict(self, NPCFriendsList):
        self.NPCFriendsDict = {}
        for friendPair in NPCFriendsList:
            self.NPCFriendsDict[friendPair[0]] = friendPair[1] 
        self.notify.debug("setting NPC friends dict to %s" % self.NPCFriendsDict)
    def getNPCFriendsDict(self):
        return self.NPCFriendsDict

    def b_setNPCFriendsDict(self, NPCFriendsList):
        self.setNPCFriendsDict(NPCFriendsList)
        self.d_setNPCFriendsDict(self.NPCFriendsDict)

    def resetNPCFriendsDict(self):
        self.b_setNPCFriendsDict([])
            
    def attemptAddNPCFriend(self, npcFriend, numCalls = 1):
        self.notify.info('%s.attemptAddNPCFriend(%s, %s)' % (self.doId, npcFriend, numCalls))
        if (numCalls <= 0):
            self.notify.warning("invalid numCalls: %d" % numCalls)
            return 0
        if (self.NPCFriendsDict.has_key(npcFriend)):
            self.NPCFriendsDict[npcFriend] += numCalls
        elif (npcFriends.has_key(npcFriend)):
            if (len(self.NPCFriendsDict.keys()) >= self.maxNPCFriends):
                return 0
            self.NPCFriendsDict[npcFriend] = numCalls
        else:
            self.notify.warning("invalid NPC: %d" % npcFriend)
            return 0
        # Make sure the number of calls is capped at the max
        if (self.NPCFriendsDict[npcFriend] > self.maxCallsPerNPC):
            self.NPCFriendsDict[npcFriend] = self.maxCallsPerNPC
        self.d_setNPCFriendsDict(self.NPCFriendsDict)
        return 1

    def d_setMaxClothes(self, max):
        self.sendUpdate("setMaxClothes", [self.maxClothes])

    def setMaxClothes(self, max):
        self.maxClothes = max

    def b_setMaxClothes(self, max):
        self.setMaxClothes(max)
        self.d_setMaxClothes(max)
        
    def getMaxClothes(self):
        return self.maxClothes

    def isClosetFull(self, extraClothes = 0):
        numClothes = len(self.clothesTopsList)/4 + len(self.clothesBottomsList)/2
        return (numClothes + extraClothes >= self.maxClothes)

    def d_setClothesTopsList(self, clothesList):
        self.sendUpdate("setClothesTopsList", [clothesList])
        return None

    def setClothesTopsList(self, clothesList):
        self.clothesTopsList = clothesList

    def b_setClothesTopsList(self, clothesList):
        self.setClothesTopsList(clothesList)
        self.d_setClothesTopsList(clothesList)
        
    def getClothesTopsList(self):
        return self.clothesTopsList    

    # add clothes to list if there is room
    def addToClothesTopsList(self, topTex, topTexColor, 
                                sleeveTex, sleeveTexColor):
        # See if there's any room for another top in the clothes list
        if self.isClosetFull():
            return 0
        
        # See if this top is already there
        index = 0
        for i in range(0, len(self.clothesTopsList), 4):
            if (self.clothesTopsList[i] == topTex and
                self.clothesTopsList[i+1] == topTexColor and
                self.clothesTopsList[i+2] == sleeveTex and
                self.clothesTopsList[i+3] == sleeveTexColor):
                return 0            
        # Add the new top
        self.clothesTopsList.append(topTex)
        self.clothesTopsList.append(topTexColor)
        self.clothesTopsList.append(sleeveTex)
        self.clothesTopsList.append(sleeveTexColor)
        return 1

    # replace item A with item B
    def replaceItemInClothesTopsList(self, topTexA, topTexColorA, 
                                     sleeveTexA, sleeveTexColorA,
                                     topTexB, topTexColorB, 
                                     sleeveTexB, sleeveTexColorB):

        # Find first occurence of top A
        index = 0
        for i in range(0, len(self.clothesTopsList), 4):
            if (self.clothesTopsList[i] == topTexA and
                self.clothesTopsList[i+1] == topTexColorA and
                self.clothesTopsList[i+2] == sleeveTexA and
                self.clothesTopsList[i+3] == sleeveTexColorA):
                # replace with top B
                self.clothesTopsList[i] = topTexB
                self.clothesTopsList[i+1] = topTexColorB
                self.clothesTopsList[i+2] = sleeveTexB
                self.clothesTopsList[i+3] = sleeveTexColorB
                return 1
        return 0

    def removeItemInClothesTopsList(self, topTex, topTexColor, 
                                    sleeveTex, sleeveTexColor):
        # assume the client has already handled the boundary checking
        # but just for sanity, we'll check the length
        listLen = len(self.clothesTopsList) 
        if listLen < 4:
            self.notify.warning("Clothes top list is not long enough to delete anything")
            return 0
                
        # Find first occurence of top
        index = 0
        for i in range(0, listLen, 4):
            if (self.clothesTopsList[i] == topTex and
                self.clothesTopsList[i+1] == topTexColor and
                self.clothesTopsList[i+2] == sleeveTex and
                self.clothesTopsList[i+3] == sleeveTexColor):
                # remove these four elements
                self.clothesTopsList = self.clothesTopsList[0:i] + self.clothesTopsList[i+4:listLen]
                return 1
        return 0
        
    def d_setClothesBottomsList(self, clothesList):
        self.sendUpdate("setClothesBottomsList", [clothesList])
        return None

    def setClothesBottomsList(self, clothesList):
        self.clothesBottomsList = clothesList

    def b_setClothesBottomsList(self, clothesList):
        self.setClothesBottomsList(clothesList)
        self.d_setClothesBottomsList(clothesList)
        
    def getClothesBottomsList(self):
        return self.clothesBottomsList    

    def addToClothesBottomsList(self, botTex, botTexColor):
        # See if there's any room for another bottom in the clothes list
        if self.isClosetFull():
            self.notify.warning("clothes bottoms list is full")
            return 0
        # See if this bottom is already there
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if (self.clothesBottomsList[i] == botTex and
                self.clothesBottomsList[i+1] == botTexColor):
                return 0            
        # Add the new bottom 
        self.clothesBottomsList.append(botTex)
        self.clothesBottomsList.append(botTexColor)
        return 1

    # replace item A with item B
    def replaceItemInClothesBottomsList(self, botTexA, botTexColorA, 
                                        botTexB, botTexColorB):

        # Find first occurence of bottom A
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if (self.clothesBottomsList[i] == botTexA and
                self.clothesBottomsList[i+1] == botTexColorA):
                # replace with bottom B
                self.clothesBottomsList[i] = botTexB
                self.clothesBottomsList[i+1] = botTexColorB
                return 1
        return 0

    def removeItemInClothesBottomsList(self, botTex, botTexColor): 
        # assume the client has already handled the boundary checking
        # but just for sanity, we'll check the length
        listLen = len(self.clothesBottomsList) 
        if listLen < 2:
            self.notify.warning("Clothes bottoms list is not long enough to delete anything")
            return 0

        # Find first occurence of bottom A
        index = 0
        for i in range(0, len(self.clothesBottomsList), 2):
            if (self.clothesBottomsList[i] == botTex and
                self.clothesBottomsList[i+1] == botTexColor):
                # remove these two elements
                self.clothesBottomsList = self.clothesBottomsList[0:i] + self.clothesBottomsList[i+2:listLen]
                return 1
        return 0

    def d_catalogGenClothes(self):
        self.sendUpdate('catalogGenClothes', [self.doId])

    def takeDamage(self, hpLost, quietly = 0, sendTotal = 1):
        # Adds the indicated hit points to the avatar's total.  If
        # quietly is 0 (the default), numbers will fly out of his
        # head; if sendTotal is 1 (the default), the resulting hp
        # value will be sent as well to ensure client and AI are in
        # agreement.  (Without sendTotal, the client will do the
        # arithmetic himself, and presumably will still arrive at the
        # same value.)

        if not self.immortalMode:
            # First, send the message to make the numbers fly out.
            if not quietly:
                self.sendUpdate('takeDamage', [hpLost])

            # Then, we recompute the HP.

            if hpLost > 0 and self.hp > 0:
                self.hp -= hpLost
                if self.hp <= 0:
                    # If you get killed, set your HP to -1 so you have
                    # a timeout in the safezone.
                    self.hp = -1

        if not self.hpOwnedByBattle:
            # We still need to check maxHp even in takeDamage(), since
            # we might have had self.hpOwnedByBattle set previously,
            # allowing the toon to go above maxHp for a time.
            self.hp = min(self.hp, self.maxHp)

            # Finally, send the new total to the client so he's with us.
            if sendTotal:
                self.d_setHp(self.hp)

    @staticmethod
    def getGoneSadMessageForAvId(avId):
        return 'goneSad-%s' % avId

    def getGoneSadMessage(self):
        return self.getGoneSadMessageForAvId(self.doId)

    def setHp(self, hp):
        DistributedPlayerAI.DistributedPlayerAI.setHp(self, hp)
        if hp <= 0:
            messenger.send(self.getGoneSadMessage())

    def b_setTutorialAck(self, tutorialAck):
        self.d_setTutorialAck(tutorialAck)
        self.setTutorialAck(tutorialAck)

    def d_setTutorialAck(self, tutorialAck):
        self.sendUpdate('setTutorialAck', [tutorialAck])

    def setTutorialAck(self, tutorialAck):
        self.tutorialAck = tutorialAck

    def getTutorialAck(self):
        return self.tutorialAck

    def d_setEarnedExperience(self, earnedExp):
        self.sendUpdate('setEarnedExperience', [earnedExp])

    def setInterface(self, string):
        self.notify.debug("setting interface to %s" % string)        

    def getInterface(self):
        return ""
        
    def setZonesVisited(self, hoods):
        self.safeZonesVisited = hoods
        self.notify.debug("setting safe zone list to %s" %
                          self.safeZonesVisited)

    def getZonesVisited(self):
        return self.safeZonesVisited

    def setHoodsVisited(self, hoods):
        self.hoodsVisited = hoods
        self.notify.debug("setting hood zone list to %s" %
                          self.hoodsVisited)

    def getHoodsVisited(self):
        return self.hoodsVisited

    def setLastHood(self, hood):
        self.lastHood = hood

    def getLastHood(self):
        return self.lastHood


    def b_setAnimState(self, animName, animMultiplier):
        self.setAnimState(animName, animMultiplier)
        self.d_setAnimState(animName, animMultiplier)

    def d_setAnimState(self, animName, animMultiplier):
        timestamp = globalClockDelta.getRealNetworkTime()
        self.sendUpdate("setAnimState", [animName, animMultiplier, timestamp])
        return None
        
    def setAnimState(self, animName, animMultiplier, timestamp=0):
        self.animName = animName
        self.animMultiplier = animMultiplier

    ### status of cogs for cog page ###
        
    def b_setCogStatus(self, cogStatusList):
        # update the cog status list
        self.setCogStatus(cogStatusList)
        self.d_setCogStatus(cogStatusList)

    def setCogStatus(self, cogStatusList):
        self.notify.debug("setting cogs to %s" % cogStatusList)
        self.cogs = cogStatusList
        
    def d_setCogStatus(self, cogStatusList):
        self.sendUpdate("setCogStatus", [cogStatusList])

    def getCogStatus(self):
        return self.cogs

    ### count of cog summons available
    
    ### count of cogs defeated for cog page ###
    
    def b_setCogCount(self, cogCountList):
        # update the cog count list
        self.setCogCount(cogCountList)
        self.d_setCogCount(cogCountList)

    def setCogCount(self, cogCountList):
        self.notify.debug("setting cogCounts to %s" % cogCountList)
        self.cogCounts = cogCountList
        
    def d_setCogCount(self, cogCountList):
        self.sendUpdate("setCogCount", [cogCountList])

    def getCogCount(self):
        return self.cogCounts


    ### set cog radar ###

    def b_setCogRadar(self, radar):
        self.setCogRadar(radar)
        self.d_setCogRadar(radar)
        
    def setCogRadar(self, radar):
        if not radar:
            self.notify.warning("cogRadar set to bad value: %s. Resetting to [0,0,0,0]" % radar)
            self.cogRadar = [0,0,0,0]
        else:
            self.cogRadar = radar

    def d_setCogRadar(self, radar):
        self.sendUpdate("setCogRadar", [radar])

    def getCogRadar(self):
        return self.cogRadar

    ### set building radar ###

    def b_setBuildingRadar(self, radar):
        self.setBuildingRadar(radar)
        self.d_setBuildingRadar(radar)
        
    def setBuildingRadar(self, radar):
        if not radar:
            self.notify.warning("buildingRadar set to bad value: %s. Resetting to [0,0,0,0]" % radar)
            self.buildingRadar = [0,0,0,0]
        else:
            self.buildingRadar = radar

    def d_setBuildingRadar(self, radar):
        self.sendUpdate("setBuildingRadar", [radar])

    def getBuildingRadar(self):
        return self.buildingRadar

    ### set cog types ###

    # Cog types indicate which type of cog we are acquiring disguise parts for.
    # There is one entry for each type of cog (corp, legal, money, sales).
    # Each number represents an index into the SuitDNA suitHeadTypes array.

    def b_setCogTypes(self, types):
        self.setCogTypes(types)
        self.d_setCogTypes(types)
        
    def setCogTypes(self, types):
        if not types:
            self.notify.warning("cogTypes set to bad value: %s. Resetting to [0,0,0,0]" % types)
            self.cogTypes = [0,0,0,0]
        else:
            self.cogTypes = types

    def d_setCogTypes(self, types):
        self.sendUpdate("setCogTypes", [types])

    def getCogTypes(self):
        return self.cogTypes

    ### set cog levels ###

    # Cog levels indicate which level of cog we are acquiring disguise parts for.
    # There is one entry for each type of cog (corp, legal, money, sales).
    
    def b_setCogLevels(self, levels):
        self.setCogLevels(levels)
        self.d_setCogLevels(levels)
        
    def setCogLevels(self, levels):
        if not levels:
            self.notify.warning("cogLevels set to bad value: %s. Resetting to [0,0,0,0]" % levels)
            self.cogLevels = [0,0,0,0]
        else:
            self.cogLevels = levels

    def d_setCogLevels(self, levels):
        self.sendUpdate("setCogLevels", [levels])

    def getCogLevels(self):
        return self.cogLevels

    def incCogLevel(self, dept):
        # Increment cog level for this cogType. If new level does not exist
        # for this cogType then increment cogType and set to base level (if we
        # are not on the final cogType!)
        newLevel = self.cogLevels[dept] + 1
        cogTypeStr = SuitDNA.suitHeadTypes[self.cogTypes[dept]]
        lastCog = (self.cogTypes[dept] >= (SuitDNA.suitsPerDept - 1))
        if not lastCog:
            maxLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level'] + 4
        else:
            maxLevel = ToontownGlobals.MaxCogSuitLevel
        # if this is the last level for this cog type
        if newLevel > maxLevel:
            # if not last cog in dept
            if not lastCog:
                # increment cog type and reset level 
                self.cogTypes[dept] += 1
                self.d_setCogTypes(self.cogTypes)
                cogTypeStr = SuitDNA.suitHeadTypes[self.cogTypes[dept]]
                self.cogLevels[dept] = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']
                self.d_setCogLevels(self.cogLevels)
        # else not the last level for this type of cog
        else:
            # just increment the level
            self.cogLevels[dept] += 1
            self.d_setCogLevels(self.cogLevels)
            # give out HP bonuses
            if lastCog:
                if self.cogLevels[dept] in ToontownGlobals.CogSuitHPLevels:
                    maxHp = self.getMaxHp()
                    # Add the amount, but make sure it is not over the
                    # global max
                    maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + 1)
                    self.b_setMaxHp(maxHp)
                    # Also, give them a full heal
                    self.toonUp(maxHp)

        self.air.writeServerEvent('cogSuit', self.doId, "%s|%s|%s" % (
            dept, self.cogTypes[dept], self.cogLevels[dept]))


    def getNumPromotions(self, dept):
        """
        Returns how many times this toon has been promoted in the given dept.
        dept should be 'c', 'l', 'm' or 's'
        New toons will return zero.  There is a cap on the return value. See inc
        """
        if not dept in SuitDNA.suitDepts:
            self.notify.warning('getNumPromotions: Invalid parameter dept=%s' % dept)
            return 0

        deptIndex = SuitDNA.suitDepts.index(dept)
        cogType = self.cogTypes[deptIndex]
        cogTypeStr = SuitDNA.suitHeadTypes[cogType] 
        lowestCogLevel = SuitBattleGlobals.SuitAttributes[cogTypeStr]['level']

        #5 levels per cog Type (determined from visual inspection of SuitBattleGlobals)
        multiple = 5 * cogType
        additional = self.cogLevels[deptIndex] - lowestCogLevel
        numPromotions = multiple + additional
        return numPromotions
        
        
        
        
            
    ### set cog parts ###

    # Cog parts indicate what parts of a cog disguise have been acquired.
    # There is one array entry for each cog type (corp, legal, money, sales).
    #
    # Each cog part number is a binary representation of the which parts the
    # toon has acquired. See CogDisguiseGlobals.py in coghq for details.

    def b_setCogParts(self, parts):
        self.setCogParts(parts)
        self.d_setCogParts(parts)
        
    def setCogParts(self, parts):
        if not parts:
            self.notify.warning("cogParts set to bad value: %s. Resetting to [0,0,0,0]" % parts)
            self.cogParts = [0,0,0,0]
        else:
            self.cogParts = parts

    def d_setCogParts(self, parts):
        self.sendUpdate("setCogParts", [parts])

    def getCogParts(self):
        return self.cogParts

    def giveCogPart(self, part, dept):
        """
        Add the given part to part list for the appropriate department.
        """
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        parts = self.getCogParts()
        parts[dept] = parts[dept] | part
        self.b_setCogParts(parts)

    def hasCogPart(self, part, dept):
        """
        Return 1 if the toon has the cog part, 0 otherwise.
        """
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        if (self.cogParts[dept] & part):
            return 1
        else:
            return 0
        
    def giveGenericCogPart(self, factoryType, dept):
        """
        Add the next part awarded by factories of the indicated type.
        Return the part added.
        """
        for partTypeId in self.partTypeIds[factoryType]:
            nextPart  = CogDisguiseGlobals.getNextPart(
                self.getCogParts(), partTypeId, dept)
            if nextPart:
                break
        if nextPart:
            self.giveCogPart(nextPart, dept)
            return nextPart
        else:
            return None

    def takeCogPart(self, part, dept):
        """
        Remove the given part from part list for the appropriate department.
        NOTE: we no longer support damaged parts
        """
        dept = CogDisguiseGlobals.dept2deptIndex(dept)
        parts = self.getCogParts()
        # if we have the part
        if parts[dept] & part:
            # remove it
            parts[dept] = parts[dept] ^ part
            self.b_setCogParts(parts)

    def loseCogParts(self, dept):
        # Randomly lose MinPartLoss to MaxPartLoss parts

        # First, decide how many parts we should lose.
        loseCount = random.randrange(CogDisguiseGlobals.MinPartLoss,
                                     CogDisguiseGlobals.MaxPartLoss + 1)

        # What parts do we have now?
        parts = self.getCogParts()
        partBitmask = parts[dept]

        # Generate a list of all possible part index numbers 0 .. 16.
        partList = range(17)

        while loseCount > 0 and partList:
            # Choose a random part index from our current pool, and
            # remove that index from future selections.
            losePart = random.choice(partList)
            partList.remove(losePart)

            # Check to see if we have that part.  If we do, remove it
            # and continue; otherwise, do nothing and just keep
            # looking for another part to remove.
            losePartBit = (1 << losePart)
            if partBitmask & losePartBit:
                partBitmask &= ~losePartBit
                loseCount -= 1

        # Now send the distributed update.
        parts[dept] = partBitmask
        self.b_setCogParts(parts)

    ### set cog merits ###

    # Cog merits indicates how many cog promotion merits have been acquired.
    # There is one array entry for each cog type (corp, legal, money, sales).

    def b_setCogMerits(self, merits):
        self.setCogMerits(merits)
        self.d_setCogMerits(merits)
        
    def setCogMerits(self, merits):
        if not merits:
            self.notify.warning("cogMerits set to bad value: %s. Resetting to [0,0,0,0]" % merits)
            self.cogMerits = [0,0,0,0]
        else:
            self.cogMerits = merits

    def d_setCogMerits(self, merits):
        self.sendUpdate("setCogMerits", [merits])

    def getCogMerits(self):
        return self.cogMerits

    def b_promote(self, dept):
        self.promote(dept)
        self.d_promote(dept)
        
    def promote(self, dept):
        # if we are lvl 50, don't require any more merits to be collected
        if self.cogLevels[dept] < ToontownGlobals.MaxCogSuitLevel:
            self.cogMerits[dept] = 0
        self.incCogLevel(dept)

    def d_promote(self, dept):
        merits = self.getCogMerits()
        # if we are lvl 50, don't require any more merits to be collected
        if self.cogLevels[dept] < ToontownGlobals.MaxCogSuitLevel:
            merits[dept] = 0
        self.d_setCogMerits(merits)

    def readyForPromotion(self, dept):
        merits = self.cogMerits[dept]
        totalMerits = CogDisguiseGlobals.getTotalMerits(self, dept)
        if (merits >= totalMerits):
            return 1
        else:
            return 0

    ### cog index ###

    # cog index which cog (in the above cogTypes) we are disguised as

    def b_setCogIndex(self, index):
        self.setCogIndex(index)
        self.d_setCogIndex(index)
        
    def setCogIndex(self, index):
        self.cogIndex = index

    def d_setCogIndex(self, index):
        self.sendUpdate("setCogIndex", [index])

    def getCogIndex(self):
        return self.cogIndex

    ### disguise page flag ###

    # remembers if we have been given the disguise page of our sticker
    # books yet

    def b_setDisguisePageFlag(self, flag):
        self.setDisguisePageFlag(flag)
        self.d_setDisguisePageFlag(flag)

    def setDisguisePageFlag(self, flag):
        self.disguisePageFlag = flag

    def d_setDisguisePageFlag(self, flag):
        self.sendUpdate("setDisguisePageFlag", [flag])

    def getDisguisePageFlag(self):
        return self.disguisePageFlag
    
    ## Fish collection
    def b_setFishCollection(self, genusList, speciesList, weightList):
        # update the caught fish list
        self.setFishCollection(genusList, speciesList, weightList)
        self.d_setFishCollection(genusList, speciesList, weightList)
        
    def d_setFishCollection(self, genusList, speciesList, weightList):
        self.sendUpdate("setFishCollection", [genusList, speciesList, weightList])

    def setFishCollection(self, genusList, speciesList, weightList):
        #import pdb; pdb.set_trace()
        self.fishCollection = FishCollection.FishCollection()
        self.fishCollection.makeFromNetLists(genusList, speciesList, weightList)

    def getFishCollection(self):
        return self.fishCollection.getNetLists()

    ## Max fish tank
    
    def b_setMaxFishTank(self, maxTank):
        self.d_setMaxFishTank(maxTank)
        self.setMaxFishTank(maxTank)

    def d_setMaxFishTank(self, maxTank):
        self.sendUpdate("setMaxFishTank", [maxTank])

    def setMaxFishTank(self, maxTank):
        self.maxFishTank = maxTank

    def getMaxFishTank(self):
        return self.maxFishTank


    ## Fish tank
    
    def b_setFishTank(self, genusList, speciesList, weightList):
        # update the caught fish list
        self.setFishTank(genusList, speciesList, weightList)
        self.d_setFishTank(genusList, speciesList, weightList)
        
    def d_setFishTank(self, genusList, speciesList, weightList):
        self.sendUpdate("setFishTank", [genusList, speciesList, weightList])

    def setFishTank(self, genusList, speciesList, weightList):
        self.fishTank = FishTank.FishTank()
        self.fishTank.makeFromNetLists(genusList, speciesList, weightList)

    def getFishTank(self):
        return self.fishTank.getNetLists()

    def makeRandomFishTank(self):
        self.fishTank.generateRandomTank()
        self.d_setFishTank(*self.fishTank.getNetLists())
        
    def addFishToTank(self, fish):
        # First check our max limit
        numFish = len(self.fishTank)
        if numFish >= self.maxFishTank:
            self.notify.warning("addFishToTank: cannot add fish, tank is full")
            return 0
        else:
            # Perhaps this can fail for some reason
            if self.fishTank.addFish(fish):
                self.d_setFishTank(*self.fishTank.getNetLists())
                return 1
            else:
                self.notify.warning("addFishToTank: addFish failed")
                return 0

    def removeFishFromTankAtIndex(self, index):
        # Try to remove this fish from the tank
        if self.fishTank.removeFishAtIndex(index):
            self.d_setFishTank(*self.fishTank.getNetLists())
            return 1
        else:
            self.notify.warning("removeFishFromTank: cannot find fish")
            return 0


    def b_setFishingRod(self, rodId):
        self.d_setFishingRod(rodId)
        self.setFishingRod(rodId)

    def d_setFishingRod(self, rodId):
        self.sendUpdate("setFishingRod", [rodId])

    def setFishingRod(self, rodId):
        self.fishingRod = rodId

    def getFishingRod(self):
        return self.fishingRod

    ### fishing trophy list ###

    def b_setFishingTrophies(self, trophyList):
        # update the caught fish list
        self.setFishingTrophies(trophyList)
        self.d_setFishingTrophies(trophyList)

    def setFishingTrophies(self, trophyList):
        self.notify.debug("setting fishingTrophies to %s" % trophyList)
        self.fishingTrophies = trophyList
        
    def d_setFishingTrophies(self, trophyList):
        self.sendUpdate("setFishingTrophies", [trophyList])

    def getFishingTrophies(self):
        return self.fishingTrophies


    ### quest list ###
    
    def b_setQuests(self, questList):
        # questList should be a nested list
        # [[quest0 properties], [quest1 properties],...]
        # This needs to be flattened
        flattenedQuests = []
        for quest in questList:
            flattenedQuests.extend(quest)
        self.setQuests(flattenedQuests)
        self.d_setQuests(flattenedQuests)

    def d_setQuests(self, flattenedQuests):
        self.sendUpdate("setQuests", [flattenedQuests])

    def setQuests(self, flattenedQuests):
        self.notify.debug("setting quests to %s" % flattenedQuests)
        # Build the real quest list from the flattened one from the network
        questList = []
        # A quest is a list with
        #   (questId, npcId, otherId, rewardId, progress)
        questLen = 5
        # Step from 2 to the end, by the questLen
        for i in range(0, len(flattenedQuests), questLen):
            questList.append(flattenedQuests[i:i+questLen])
        self.quests = questList

    def getQuests(self):
        # This returns the quests formatted for the net, not directly
        # usable.
        flattenedQuests = []
        for quest in self.quests:
            flattenedQuests.extend(quest)
        return flattenedQuests

    def getQuest(self, id, visitNpcId = None):
        for quest in self.quests:
            if quest[0] == id:
                # If a visitNpc was passed in, make sure that matches too
                # Visit quests all have the same Id, so you must differentiate
                # them with the id of the npc we need to visit
                if visitNpcId:
                    if ((visitNpcId == quest[1]) or
                        (visitNpcId == quest[2])):
                        return quest
                else:
                    return quest
        return None

    def removeQuest(self, id, visitNpcId = None):
        index = -1
        for i in range(len(self.quests)):
            if (self.quests[i][0] == id):
                # If this is a visit quest, we need to make sure the npc
                # we are visiting matches since all visit quests have the
                # same id
                if visitNpcId:
                    otherId = self.quests[i][2]
                    if (visitNpcId == otherId):
                        index = i
                        break
                else:
                    index = i
                    break
        if (index >= 0):
            del self.quests[i]
            self.b_setQuests(self.quests)
            return 1
        else:
            return 0

    def addQuest(self, quest, finalReward, recordHistory=1):
        # Add this quest to this avatar in the database
        # For the final looping tier, we do not want to keep
        # accumulating history so you have the option the nor
        # recordHistory. This will still update quests, but not
        # questHistory or rewardHistory
        self.quests.append(quest)
        self.b_setQuests(self.quests)

        if recordHistory:
            if quest[0] != Quests.VISIT_QUEST_ID:
                # Also add this quest to the history.
                newQuestHistory = self.questHistory + [quest[0]]

                # And then remove all previous occurrences of the visit
                # quest from the quest history list.  This is really just
                # a hack to repair the damage from previous versions of
                # this code, which allowed this quest to accumulate in the
                # history list until we exceeded all available space in
                # the toon's database record.  The first time a particular
                # toon adds a new quest, it will eliminate all of these.
                while newQuestHistory.count(Quests.VISIT_QUEST_ID) != 0:
                    newQuestHistory.remove(Quests.VISIT_QUEST_ID)

                self.b_setQuestHistory(newQuestHistory)

                # Now update the reward history, only if this is a single quest
                # or the start of a multipart quest. In either case, finalReward
                # will be non-None, and we should store it in our history
                if finalReward:
                    newRewardHistory = self.rewardHistory + [finalReward]
                    self.b_setRewardHistory(self.rewardTier, newRewardHistory)

    def removeAllTracesOfQuest(self, questId, rewardId):
        self.notify.warning('removeAllTracesOfQuest: questId: %s rewardId: %s' % (questId, rewardId))
        self.notify.warning('removeAllTracesOfQuest: quests before: %s' % (self.quests))
        self.removeQuest(questId)
        self.notify.warning('removeAllTracesOfQuest: quests after: %s' % (self.quests))
        self.notify.warning('removeAllTracesOfQuest: questHistory before: %s' % (self.questHistory))
        self.removeQuestFromHistory(questId)
        self.notify.warning('removeAllTracesOfQuest: questHistory after: %s' % (self.questHistory))
        self.notify.warning('removeAllTracesOfQuest: reward history before: %s' % (self.rewardHistory))
        self.removeRewardFromHistory(rewardId)
        self.notify.warning('removeAllTracesOfQuest: reward history after: %s' % (self.rewardHistory))

    # The number of quests you can carry at once
    def b_setQuestCarryLimit(self, limit):
        self.setQuestCarryLimit(limit)
        self.d_setQuestCarryLimit(limit)

    def d_setQuestCarryLimit(self, limit):
        self.sendUpdate("setQuestCarryLimit", [limit])

    def setQuestCarryLimit(self, limit):
        self.notify.debug("setting questCarryLimit to %s" % limit)
        self.questCarryLimit = limit

    def getQuestCarryLimit(self):
        return self.questCarryLimit

    def b_setMaxCarry(self, maxCarry):
        self.setMaxCarry(maxCarry)
        self.d_setMaxCarry(maxCarry)

    def d_setMaxCarry(self, maxCarry):
        self.sendUpdate("setMaxCarry", [maxCarry])

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry

    def getMaxCarry(self):
        return self.maxCarry

    ### cheesy rendering effects ###

    def b_setCheesyEffect(self, effect, hoodId, expireTime):
        self.setCheesyEffect(effect, hoodId, expireTime)
        self.d_setCheesyEffect(effect, hoodId, expireTime)

    def d_setCheesyEffect(self, effect, hoodId, expireTime):
        self.sendUpdate("setCheesyEffect", [effect, hoodId, expireTime])

    def setCheesyEffect(self, effect, hoodId, expireTime):
        if simbase.air.holidayManager and \
            ToontownGlobals.WINTER_CAROLING not in simbase.air.holidayManager.currentHolidays \
            and effect == ToontownGlobals.CESnowMan:
            self.b_setCheesyEffect(ToontownGlobals.CENormal, hoodId, expireTime)
            return
        self.savedCheesyEffect = effect
        self.savedCheesyHoodId = hoodId
        self.savedCheesyExpireTime = expireTime

        if self.air.doLiveUpdates:
            taskName = self.uniqueName('cheesy-expires')
            taskMgr.remove(taskName)

            if effect != ToontownGlobals.CENormal:
                # Set a timeout to undo the cheesy effect later.
                duration = expireTime * 60 - time.time()
                if (duration > 0):
                    taskMgr.doMethodLater(duration, self.__undoCheesyEffect, taskName)
                else:
                    # Undo the cheesy effect right away.
                    self.__undoCheesyEffect(None)

    def getCheesyEffect(self):
        return (self.savedCheesyEffect, self.savedCheesyHoodId, self.savedCheesyExpireTime)

    def __undoCheesyEffect(self, task):
        self.b_setCheesyEffect(ToontownGlobals.CENormal, 0, 0)
        return Task.cont

    ### setTrackAccess ###

    def b_setTrackAccess(self, trackArray):
        # local
        self.setTrackAccess(trackArray)
        # distributed
        self.d_setTrackAccess(trackArray)

    def d_setTrackAccess(self, trackArray):
        self.sendUpdate("setTrackAccess", [trackArray])

    def setTrackAccess(self, trackArray):
        self.trackArray = trackArray

    def getTrackAccess(self):
        return self.trackArray

    def addTrackAccess(self, track):
        """
        Give this toon access to gags on this track
        """
        self.trackArray[track] = 1
        self.b_setTrackAccess(self.trackArray)
    
    def removeTrackAccess(self, track):
        """
        Deny this toon access to gags on this track
        """
        self.trackArray[track] = 0
        self.b_setTrackAccess(self.trackArray)

    def hasTrackAccess(self, track):
        """
        Can this toon use this track?
        Returns bool 0/1
        """
        if self.trackArray and track < len(self.trackArray):
            return self.trackArray[track]
        else:
            #RAU this case can happen if we are opening the closet of another toon
            return 0
        

    def fixTrackAccess(self):
        fixed = 0
        healExp, trapExp, lureExp, soundExp, throwExp, squirtExp, dropExp  = self.experience.experience
        numTracks = reduce(lambda a,b: a+b, self.trackArray)
        if self.rewardTier in [0,1,2,3]:
            if numTracks != 2:
                self.notify.warning("bad num tracks in tier: %s, %s" % (self.rewardTier, self.trackArray))
                # They should have throw and squirt only
                self.b_setTrackAccess([0,0,0,0,1,1,0])
                fixed = 1
        elif self.rewardTier in [4,5,6]:
            if numTracks != 3:
                self.notify.warning("bad num tracks in tier: %s, %s" % (self.rewardTier, self.trackArray))
                # Now they had a choice between heal and sound
                # If they have sound but not heal, give them sound
                if (self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not
                    self.trackArray[ToontownBattleGlobals.HEAL_TRACK]):
                    self.b_setTrackAccess([0,0,0,1,1,1,0])
                # If they have heal but not sound, give them heal
                elif (self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not
                      self.trackArray[ToontownBattleGlobals.SOUND_TRACK]):
                    self.b_setTrackAccess([1,0,0,0,1,1,0])
                # If they have both, use exp to determine
                else:
                    # If they are higher in sound, give them sound access
                    if soundExp >= healExp:
                        self.b_setTrackAccess([0,0,0,1,1,1,0])
                        # if they are higher in heal, give them heal access
                    else:
                        self.b_setTrackAccess([1,0,0,0,1,1,0])
                fixed = 1

        elif self.rewardTier in [7,8,9,10]:
            if numTracks != 4:
                self.notify.warning("bad num tracks in tier: %s, %s" % (self.rewardTier, self.trackArray))
                # If they have sound but not heal, give them sound and drop or lure
                if (self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not
                    self.trackArray[ToontownBattleGlobals.HEAL_TRACK]):
                    if dropExp >= lureExp:
                        # sound and drop
                        self.b_setTrackAccess([0,0,0,1,1,1,1])
                    else:
                        # sound and lure
                        self.b_setTrackAccess([0,0,1,1,1,1,0])

                # If they have heal but not sound, give them heal and drop or lure
                elif (self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not
                      self.trackArray[ToontownBattleGlobals.SOUND_TRACK]):
                    if dropExp >= lureExp:
                        # heal and drop
                        self.b_setTrackAccess([1,0,0,0,1,1,1])
                    else:
                        # heal and lure
                        self.b_setTrackAccess([1,0,1,0,1,1,0])

                # Else look at exp to determine if they should have sound or heal
                # then drop or lure
                elif soundExp >= healExp:
                    if dropExp >= lureExp:
                        # sound and drop
                        self.b_setTrackAccess([0,0,0,1,1,1,1])
                    else:
                        # sound and lure
                        self.b_setTrackAccess([0,0,1,1,1,1,0])
                else:
                    if dropExp >= lureExp:
                        # heal and drop
                        self.b_setTrackAccess([1,0,0,0,1,1,1])
                    else:
                        # heal and lure
                        self.b_setTrackAccess([1,0,1,0,1,1,0])

                fixed = 1
        elif self.rewardTier in [11,12,13]:
            if numTracks != 5:
                self.notify.warning("bad num tracks in tier: %s, %s" % (self.rewardTier, self.trackArray))
                if (self.trackArray[ToontownBattleGlobals.SOUND_TRACK] and not
                    self.trackArray[ToontownBattleGlobals.HEAL_TRACK]):
                    if (self.trackArray[ToontownBattleGlobals.DROP_TRACK] and not
                        self.trackArray[ToontownBattleGlobals.LURE_TRACK]):
                        if healExp >= trapExp:
                            self.b_setTrackAccess([1,0,0,1,1,1,1])
                        else:
                            self.b_setTrackAccess([0,1,0,1,1,1,1])
                    else:
                        if healExp >= trapExp:
                            self.b_setTrackAccess([1,0,1,1,1,1,0])
                        else:
                            self.b_setTrackAccess([0,1,1,1,1,1,0])
                elif (self.trackArray[ToontownBattleGlobals.HEAL_TRACK] and not
                      self.trackArray[ToontownBattleGlobals.SOUND_TRACK]):
                    if (self.trackArray[ToontownBattleGlobals.DROP_TRACK] and not
                        self.trackArray[ToontownBattleGlobals.LURE_TRACK]):
                        if soundExp >= trapExp:
                            self.b_setTrackAccess([1,0,0,1,1,1,1])
                        else:
                            self.b_setTrackAccess([1,1,0,0,1,1,1])
                    else:
                        if soundExp >= trapExp:
                            self.b_setTrackAccess([1,0,1,1,1,1,0])
                        else:
                            self.b_setTrackAccess([1,1,1,0,1,1,0])
                fixed = 1
        else:
            if numTracks != 6:
                self.notify.warning("bad num tracks in tier: %s, %s" % (self.rewardTier, self.trackArray))
                # Do not count throw or squirt because you are stuck with those
                sortedExp = [healExp, trapExp, lureExp, soundExp, dropExp]
                # Sort will put the smallest (least exp) first
                sortedExp.sort()
                # Check the least desirable tracks first in case there is a tie
                if trapExp == sortedExp[0]:
                    self.b_setTrackAccess([1,0,1,1,1,1,1])                    
                elif lureExp == sortedExp[0]:
                    self.b_setTrackAccess([1,1,0,1,1,1,1])
                elif dropExp == sortedExp[0]:
                    self.b_setTrackAccess([1,1,1,1,1,1,0])
                elif soundExp == sortedExp[0]:
                    self.b_setTrackAccess([1,1,1,0,1,1,1])
                elif healExp == sortedExp[0]:
                    self.b_setTrackAccess([0,1,1,1,1,1,1])
                else:
                    self.notify.warning("invalid exp?!: %s, %s" % (sortedExp, self.trackArray))
                    # Give the avatar something
                    self.b_setTrackAccess([1,0,1,1,1,1,1])
                fixed = 1

        if fixed:
            # Adjust inventory to fit new tracks
            self.inventory.zeroInv()
            self.inventory.maxOutInv()
            self.d_setInventory(self.inventory.makeNetString())
            self.notify.info("fixed tracks: %s" % (self.trackArray))
            
        return fixed
        

    ### setTrackProgress ###

    def b_setTrackProgress(self, trackId, progress):
        # local
        self.setTrackProgress(trackId, progress)
        # distributed
        self.d_setTrackProgress(trackId, progress)

    def d_setTrackProgress(self, trackId, progress):
        self.sendUpdate("setTrackProgress", [trackId, progress])

    def setTrackProgress(self, trackId, progress):
        """
        Update your progress training trackId. TrackId is an index into
        ToontownBattleGlobals.Tracks and progress is a bitarray of progress
        markers gathered. A trackId of -1 means you are not training any track.
        """
        self.trackProgressId = trackId
        self.trackProgress = progress

    def addTrackProgress(self, trackId, progressIndex):
        """
        Update your progress training trackId with this index.
        """
        if self.trackProgressId != trackId:
            self.notify.warning("tried to update progress on a track toon is not training")
        newProgress = self.trackProgress | (1 << (progressIndex - 1))
        self.b_setTrackProgress(self.trackProgressId, newProgress)

    def clearTrackProgress(self):
        """
        Update your progress training to be empty.
        """
        self.b_setTrackProgress(-1, 0)

    def getTrackProgress(self):
        return [self.trackProgressId, self.trackProgress]

    ### setHoodsVisited ###
    
    def b_setHoodsVisited(self, hoodsVisitedArray):
        # local
        self.hoodsVisited = hoodsVisitedArray
        # distributed
        self.d_setHoodsVisited(hoodsVisitedArray)
   
    def d_setHoodsVisited(self, hoodsVisitedArray):
        self.sendUpdate("setHoodsVisited", [hoodsVisitedArray])

    ### setTeleportAccess ###
    
    def b_setTeleportAccess(self, teleportZoneArray):
        # local
        self.setTeleportAccess(teleportZoneArray)
        # distributed
        self.d_setTeleportAccess(teleportZoneArray)

    def d_setTeleportAccess(self, teleportZoneArray):
        self.sendUpdate("setTeleportAccess", [teleportZoneArray])

    def setTeleportAccess(self, teleportZoneArray):
        self.teleportZoneArray = teleportZoneArray

    def getTeleportAccess(self):
        return self.teleportZoneArray

    def hasTeleportAccess(self, zoneId):
        """
        Return true if this zoneId is in our teleport access array
        (meaning we can teleport to it)
        """
        return (zoneId in self.teleportZoneArray)

    def addTeleportAccess(self, zoneId):
        """
        Give this toon teleport access to this zoneId
        Update the zone array to add this zoneId and
        message to the client to update him too
        """
        # Make sure this is a valid hood zoneId
        assert zoneId in ToontownGlobals.Hoods
        if zoneId not in self.teleportZoneArray:
            self.teleportZoneArray.append(zoneId)
            self.b_setTeleportAccess(self.teleportZoneArray)

    def removeTeleportAccess(self, zoneId):
        """
        Update the zone array to remove this zoneId and send a
        message to the client to update him too
        """
        if zoneId in self.teleportZoneArray:
            self.teleportZoneArray.remove(zoneId)
            self.b_setTeleportAccess(self.teleportZoneArray)


    def b_setQuestHistory(self, questList):
        self.setQuestHistory(questList)
        self.d_setQuestHistory(questList)

    def d_setQuestHistory(self, questList):
        self.sendUpdate("setQuestHistory", [questList])

    def setQuestHistory(self, questList):
        self.notify.debug("setting quest history to %s" % questList)
        self.questHistory = questList

    def getQuestHistory(self):
        return self.questHistory

    def removeQuestFromHistory(self, questId):
        if questId in self.questHistory:
            # Remove it locally
            self.questHistory.remove(questId)
            # And on the server
            self.d_setQuestHistory(self.questHistory)
            return 1
        else:
            return 0

    def removeRewardFromHistory(self, rewardId):
        rewardTier, rewardHistory = self.getRewardHistory()
        if rewardId in rewardHistory:
            rewardHistory.remove(rewardId)
            self.b_setRewardHistory(rewardTier, rewardHistory)
            return 1
        else:
            return 0

    def b_setRewardHistory(self, tier, rewardList):
        self.setRewardHistory(tier, rewardList)
        self.d_setRewardHistory(tier, rewardList)

    def d_setRewardHistory(self, tier, rewardList):
        self.sendUpdate("setRewardHistory", [tier, rewardList])

    def setRewardHistory(self, tier, rewardList):
        self.air.writeServerEvent("questTier", self.getDoId(), str(tier))
        self.notify.debug("setting reward history to tier %s, %s" % (tier, rewardList))
        self.rewardTier = tier
        self.rewardHistory = rewardList

    def getRewardHistory(self):
        return self.rewardTier, self.rewardHistory

    def getRewardTier(self):
        return self.rewardTier

    # TODO
    # If the need ever arises to do upon-login toon DB patching, here's
    # a scheme that drose and I worked out:
    #
    # DistributedToonAI should have a function that validates the toon's DB
    # entries, and sends out updates for any values that need to change.
    # We can't just call this in DistributedToonAI.generate(), though.
    #
    # There is a race condition between generation of the Toon on the AI
    # and on the client; we must make sure that the Toon has been generated
    # on the client before we run the validation function, so that the
    # client will receive any updates we send out. We must also make sure
    # that the client does not start up the game on its end before the AI
    # has had a chance to fix up the Toon's fields.
    #
    # We can add two new messages to DistributedToon in the toon.dc, one
    # going from the AI to the client (QueryReady), the other from the
    # client to the AI (ReplyReady). Neither has any arguments. When the
    # toon is generated on the AI, it will start a task that will send out
    # QueryReady msgs at some interval (or maybe it could be a ram field
    # with a default value, that the AI sets to a different value upon
    # generation).  When the toon is generated on the client, it will enter
    # a mode where it will reply to the first QueryReady msg it receives
    # with a ReplyReady msg.
    #
    # When the AI gets a ReplyReady message, it knows that the client has
    # generated the Toon, and it can go ahead and fix up the toon, sending
    # updates for any fields that change.
    #
    # (Note that it's not important for the DB server to get these updates;
    # if an update is missed, the AI and the client will have the correct
    # values for the rest of the session. The same values will be computed
    # upon subsequent logins, until they eventually make it into the
    # database.  Additionally, if the field is modified during the play
    # session, the old invalid DB value will be overwritten.)
    #
    # The only thing left now is preventing the client from starting up the
    # game before the AI has vetted its Toon. We could withold the
    # TimeManager's first sync reply to the client until the toon has been
    # checked. (see ToontownClientRepository.gotTimeSync) Alternatively, we
    # could add another DC network message on LocalToon that the AI sends
    # just after doing its fixup, and add a new state to the TCR that waits
    # for this message to arrive before proceeding.
    
    # It would also be cool to be able to use AvatarIterators (used to do
    # entire-DB patches) in DistributedToonAI's fixup function.

    def fixAvatar(self):
        # Fix whatever might be out-of-whack in the avatar.  Returns 1
        # if the avatar was broken and has been changed, or 0 if it
        # was fine.

        anyChanged = 0

        # First, recompute and reapply the rewards according to the
        # current quest tier.
        qrc = QuestRewardCounter.QuestRewardCounter()
        if qrc.fixAvatar(self):
            self.notify.info("Fixed avatar %d's quest rewards." % (self.doId))
            anyChanged = 1

        if self.hp > self.maxHp:
            self.notify.info("Changed avatar %d to have hp %d instead of %d, to fit with maxHp" % (self.doId, self.maxHp, self.hp))
            self.b_setHp(self.maxHp)
            anyChanged = 1

        # Make sure we aren't carrying gags we're not allowed to
        # carry, etc.
        inventoryChanged = 0
        carry = self.maxCarry
        
        for track in range(len(ToontownBattleGlobals.Tracks)):
            if not self.hasTrackAccess(track):
                for level in range(len(ToontownBattleGlobals.Levels[track])):
                    count = self.inventory.inventory[track][level]
                    if count != 0:
                        self.notify.info("Changed avatar %d to throw away %d items in track %d level %d; no access to track." % (self.doId, count, track, level))
                        self.inventory.inventory[track][level] = 0
                        inventoryChanged = 1
            else:
                # We have access to the track; what's the highest
                # skill level we have access to?
                curSkill = self.experience.getExp(track)
                for level in range(len(ToontownBattleGlobals.Levels[track])):
                    count = self.inventory.inventory[track][level]
                    if curSkill < ToontownBattleGlobals.Levels[track][level]:
                        if count != 0:
                            self.notify.info("Changed avatar %d to throw away %d items in track %d level %d; no access to level." % (self.doId, count, track, level))
                            self.inventory.inventory[track][level] = 0
                            inventoryChanged = 1
                    else:
                        newCount = min(count, carry)
                        newCount = min(count, self.inventory.getMax(track, level))
                        if count != newCount:
                            self.notify.info("Changed avatar %d to throw away %d items in track %d level %d; too many gags." % (self.doId, count - newCount, track, level))
                            self.inventory.inventory[track][level] = newCount
                            inventoryChanged = 1
                        carry -= newCount

        self.inventory.calcTotalProps()
        if inventoryChanged:
            self.d_setInventory(self.inventory.makeNetString())
            anyChanged = 1
        
        if len(self.quests) > self.questCarryLimit:
            self.notify.info("Changed avatar %d to throw out %d quests; too many quests." % (self.doId, len(self.quests) - self.questCarryLimit))
            self.b_setQuests(self.quests[:self.questCarryLimit])

            # Now that we've removed one of the quests, we need to do
            # the whole thing again, just to make sure we don't lose
            # credit for the quest we have now no longer completed.
            self.fixAvatar()
            anyChanged = 1

        """
        # Also, remove old quest tiers from the questHistory so we
        # keep the database record small.
        if self.questHistory:
            # Get the largest value on the quest history.  This must
            # represent the current tier.
            m = max(self.questHistory)

            # Integer division.
            tier = (m / 1000)
            newQuestHistory = []
            for q in self.questHistory:
                if (q / 1000) == tier:
                    newQuestHistory.append(q)

            if self.questHistory != newQuestHistory:
                self.notify.info("Changed avatar %d to have questHistory %s instead of %s." % (self.doId, newQuestHistory, self.questHistory))
                self.b_setQuestHistory(newQuestHistory)
                anyChanged = 1
        """

        if not (self.emoteAccess[0] and self.emoteAccess[1] and
                self.emoteAccess[2] and self.emoteAccess[3] and
                self.emoteAccess[4]):
            self.emoteAccess[0] = 1
            self.emoteAccess[1] = 1
            self.emoteAccess[2] = 1
            self.emoteAccess[3] = 1
            self.emoteAccess[4] = 1
            self.b_setEmoteAccess(self.emoteAccess)
            self.notify.info("Changed avatar %d to have emoteAccess: %s" % (self.doId, self.emoteAccess))
            anyChanged = 1
            
        return anyChanged

    def b_setEmoteAccess(self, bits):
        self.setEmoteAccess(bits)
        self.d_setEmoteAccess(bits)

    def d_setEmoteAccess(self, bits):
        self.sendUpdate("setEmoteAccess", [bits])

    def setEmoteAccess(self, bits):
        if len(bits) == 20:
            bits.extend([0,0,0,0,0])
            self.b_setEmoteAccess(bits)
        else:
            if len(bits) != len(self.emoteAccess):
                self.notify.warning("New emote access list must be the same size as the old one.")
                return
        self.emoteAccess = bits

    def getEmoteAccess(self):
        return self.emoteAccess

    def setEmoteAccessId(self, id, bit):
        self.emoteAccess[id] = bit
        self.d_setEmoteAccess(self.emoteAccess)
        
    # assign a house to a toon
    def b_setHouseId(self, id):
        self.setHouseId(id)
        self.d_setHouseId(id)

    def d_setHouseId(self, id):
        self.sendUpdate("setHouseId", [id])

    def setHouseId(self, id):
        self.houseId = id

    def getHouseId(self):
        return self.houseId

    def setPosIndex(self, index):
        self.posIndex = index

    def getPosIndex(self):
        return self.posIndex

    # Control the list of custom SpeedChat messages the toon may make.
    def b_setCustomMessages(self, customMessages):
        self.d_setCustomMessages(customMessages)
        self.setCustomMessages(customMessages)

    def d_setCustomMessages(self, customMessages):
        self.sendUpdate('setCustomMessages', [customMessages])

    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages

    def getCustomMessages(self):
        return self.customMessages

    # Control the list of resistance SpeedChat messages the toon may make.
    def b_setResistanceMessages(self, resistanceMessages):
        self.d_setResistanceMessages(resistanceMessages)
        self.setResistanceMessages(resistanceMessages)

    def d_setResistanceMessages(self, resistanceMessages):
        self.sendUpdate('setResistanceMessages', [resistanceMessages])

    def setResistanceMessages(self, resistanceMessages):
        self.resistanceMessages = resistanceMessages

    def getResistanceMessages(self):
        return self.resistanceMessages

    def addResistanceMessage(self, textId):
        msgs = self.getResistanceMessages()
        #look through the array and find the textId
        for i in range(len(msgs)):
            if msgs[i][0] == textId:
                msgs[i][1] += 1
                self.b_setResistanceMessages(msgs)
                return

        #we didn't find the message... add it to the end
        msgs.append([textId, 1])
        self.b_setResistanceMessages(msgs)

    def removeResistanceMessage(self, textId):
        # Removes the indicated resistance message from the Toon's
        # inventory.  Returns true if it was there in the first place,
        # false if it was not.
        
        msgs = self.getResistanceMessages()
        #look through the array and find the textId
        for i in range(len(msgs)):
            if msgs[i][0] == textId:
                msgs[i][1] -= 1
                if msgs[i][1] <= 0:
                    del msgs[i]
                self.b_setResistanceMessages(msgs)
                return 1

        self.notify.warning("Toon %s doesn't have resistance message %s" % (self.doId, textId))
        return 0

    # Control the schedule of catalogs.

    def b_setCatalogSchedule(self, currentWeek, nextTime):
        self.setCatalogSchedule(currentWeek, nextTime)
        self.d_setCatalogSchedule(currentWeek, nextTime)

    def d_setCatalogSchedule(self, currentWeek, nextTime):
        self.sendUpdate("setCatalogSchedule", [currentWeek, nextTime])

    def setCatalogSchedule(self, currentWeek, nextTime):
        self.catalogScheduleCurrentWeek = currentWeek
        self.catalogScheduleNextTime = nextTime

        if self.air.doLiveUpdates:
            # Schedule the next catalog.
            taskName = self.uniqueName('next-catalog')
            taskMgr.remove(taskName)

            # Set a timeout to deliver the catalog later.  We insist on
            # waiting at least 10 seconds mainly to give the avatar enough
            # time to completely manifest on the stateserver before we
            # start sending messages to it.

            duration = max(10.0, nextTime * 60 - time.time())
            taskMgr.doMethodLater(duration, self.__deliverCatalog, taskName)
            #self.notify.info
            #self.air.writeServerEvent('CatalogSPAM', self.doId, " %s avId %s week %s, next catalog in %s." % (
            #    self.getName(), self.doId, currentWeek,
            #    PythonUtil.formatElapsedSeconds(duration)))

    def getCatalogSchedule(self):
        return (self.catalogScheduleCurrentWeek, self.catalogScheduleNextTime)

    def __deliverCatalog(self, task):
        # super spammy hacks to track down ai crash
        # self.notify.info('Got __deliverCatalog for %d' % self.doId)
        # self.air.writeServerEvent('__deliverCatalog' , self.doId, '')
        self.air.catalogManager.deliverCatalogFor(self)
        return Task.done
    

    def b_setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)
        self.d_setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)

    def d_setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.sendUpdate("setCatalog", [monthlyCatalog.getBlob(), weeklyCatalog.getBlob(), backCatalog.getBlob()])

    def setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.monthlyCatalog = CatalogItemList.CatalogItemList(monthlyCatalog)
        self.weeklyCatalog = CatalogItemList.CatalogItemList(weeklyCatalog)
        self.backCatalog = CatalogItemList.CatalogItemList(backCatalog)

    def getCatalog(self):
        return (self.monthlyCatalog.getBlob(), self.weeklyCatalog.getBlob(), self.backCatalog.getBlob())

    def b_setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.setCatalogNotify(catalogNotify, mailboxNotify)
        self.d_setCatalogNotify(catalogNotify, mailboxNotify)

    def d_setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.sendUpdate("setCatalogNotify", [catalogNotify, mailboxNotify])

    def setCatalogNotify(self, catalogNotify, mailboxNotify):
        self.catalogNotify = catalogNotify
        self.mailboxNotify = mailboxNotify

    def getCatalogNotify(self):
        return (self.catalogNotify, self.mailboxNotify)

    def b_setDeliverySchedule(self, onOrder, doUpdateLater = True):
        self.setDeliverySchedule(onOrder, doUpdateLater)
        self.d_setDeliverySchedule(onOrder)

    def d_setDeliverySchedule(self, onOrder):
        self.sendUpdate("setDeliverySchedule", [onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)])




    def setDeliverySchedule(self, onOrder, doUpdateLater = True):
        self.setBothSchedules(onOrder, None)
        return
        #I've rerouted this function to setBothSchedules to resolve a stomping issue with the mailbox feild
        #the original version follows
        
        self.onOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if hasattr(self, 'name'):
            if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air'):
                # Schedule the next delivery.
                taskName = self.uniqueName('next-delivery')
                taskMgr.remove(taskName)
    
                #print("setting item schedule for %s" % (self.getName()))
                # Set a timeout to make the delivery later.  We insist on
                # waiting at least 10 seconds mainly to give the avatar enough
                # time to completely manifest on the stateserver before we
                # start sending messages to it.
                now = (int)(time.time() / 60 + 0.5)
                nextItem = None
                nextTime = self.onOrder.getNextDeliveryDate()
                nextItem = self.onOrder.getNextDeliveryItem()
                if nextItem != None:
                    pass
                    #print(">>current time:%s" % (now))
                    #print("next item time:%s item:%s" % (nextTime, nextItem.getName()))
                else:
                    pass
                    #print("No items for regular delivery")
                if nextTime != None:
                    duration = max(10.0, nextTime * 60 - time.time())
                    taskMgr.doMethodLater(duration, self.__deliverPurchase, taskName)
                
    def getDeliverySchedule(self):
        return self.onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        
    def b_setBothSchedules(self, onOrder, onGiftOrder,doUpdateLater = True):
        self.setBothSchedules(onOrder, onGiftOrder, doUpdateLater)
        self.d_setDeliverySchedule(onOrder)
        
    def setBothSchedules(self, onOrder, onGiftOrder, doUpdateLater = True):
        #this function gets called twice in a row as soon as a toon enters the world
        #this stomps the mailbox field in the database, so I'm using the taskManager
        #as a cache;
        #this function checks to see if it's action "__deliverBothPurchases" aka next-bothDelivery-%s
        #is on the taskmanager, if it is and it wants to act sooner it replaces that action
        
        #We check both the gift and delviery queues.
        #Note:when first called one of those queues will be uninitialized hence all the if None calls
        #also this does need to be called twice as the toon enters the world
        
        #print ("Start setBothSchedules")
        #print ("xxxx.onOrder %s" % (onOrder))
        #print ("self.onOrder %s" % (self.onOrder))
        #print ("xxxx.onGiftOrder %s " % (onGiftOrder))
        #print ("self.onGiftOrder %s" % (self.onGiftOrder))
        if onOrder != None:
            self.onOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if onGiftOrder != None:
            self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

        #if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air') and hasattr(self, 'name'):
        if not hasattr(self, 'air') or (self.air == None):
            return
        if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'name'):            
            taskName = ("next-bothDelivery-%s" % (self.doId))#self.uniqueName('next-bothDelivery')
            #taskMgr.remove(taskName)
            
            now = (int)(time.time() / 60 + 0.5)
            
            nextItem = None
            nextGiftItem = None
            nextTime = None
            nextGiftTime = None
            if self.onOrder:
                nextTime = self.onOrder.getNextDeliveryDate()
                nextItem = self.onOrder.getNextDeliveryItem()
            if self.onGiftOrder:
                nextGiftTime = self.onGiftOrder.getNextDeliveryDate()
                nextGiftItem = self.onGiftOrder.getNextDeliveryItem()
            #print(">>current time:%s" % (now))
            
            if nextItem:
                pass
                #print("next item time:%s item:%s" % (nextTime, nextItem.getName()))
            else:
                pass
                #print("No items for regular delivery")
            if nextGiftItem:
                pass
                #print("next gift time:%s item:%s" % (nextGiftTime, nextGiftItem.getName()))
            else:
                pass
                #print("No items for gift delivery")
                
            if nextTime == None:
                nextTime = nextGiftTime
            if nextGiftTime == None:
                nextGiftTime = nextTime
                
            if nextGiftTime < nextTime:
                nextTime = nextGiftTime
            
            existingDuration = None
            checkTaskList = taskMgr.getTasksNamed(taskName)
            if checkTaskList:
                currentTime = globalClock.getFrameTime()
                assert len(checkTaskList) <= 1
                checkTask = checkTaskList[0]
                existingDuration = checkTask.wakeTime - currentTime
                #print("existingDuration %s" % (existingDuration))
                #import pdb; pdb.set_trace()
                
            
            #print("taskName %s" % (taskName))
            
            if nextTime:
                newDuration = max(10.0, nextTime * 60 - time.time())
                #print("Duration %s" % (newDuration))
                if existingDuration and existingDuration >= newDuration:
                    #print ("replacing duration")
                    taskMgr.remove(taskName)
                    taskMgr.doMethodLater(newDuration, self.__deliverBothPurchases, taskName) #change function
                elif existingDuration and existingDuration < newDuration:
                    #print ("leaving duration")
                    pass
                else:
                    #print ("adding duration")
                    taskMgr.doMethodLater(newDuration, self.__deliverBothPurchases, taskName) #change function
            #print ("End setBothSchedules")
                
    def __deliverBothPurchases(self, task):
        #combines delivering gifts and regular deliveries into one action
        #to keep mailbox contents from getting stomped
        
        #print ("Start __deliverBothPurchases")
        # Get the current time in minutes.
        now = (int)(time.time() / 60 + 0.5)
        # Extract out any items that should have been delivered by now.
        delivered, remaining = self.onOrder.extractDeliveryItems(now)

        #self.notify.info("Delivery for %s: %s." % (self.doId, delivered))
        #print("Delivery for %s" % (self.getName()))
        #print("Delivered %s." % (delivered))
        #print("Remaining %s." % (remaining))
        
        # Extract out any Gift items that should have been delivered by now.
        deliveredGifts, remainingGifts = self.onGiftOrder.extractDeliveryItems(now)
        #self.notify.info("Gift Delivery for %s: %s." % (self.doId, deliveredGifts))
        #print("Gift Delivery for %s" % (self.getName()))
        #print("Delivered %s." % (deliveredGifts))
        #print("Remaining %s." % (remainingGifts))
        simbase.air.deliveryManager.sendDeliverGifts(self.getDoId(), now)  
        
        #b_setMailboxContents must come before b_setCatalogNotify
        #because b_setMailboxContents resets the notification data
        giftItem = CatalogItemList.CatalogItemList(deliveredGifts, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if(len(giftItem) > 0):
            self.air.writeServerEvent("Getting Gift", self.doId, "sender %s receiver %s gift %s" % (giftItem[0].giftTag, self.doId, giftItem[0].getName()))
        self.b_setMailboxContents(self.mailboxContents + delivered + deliveredGifts)
        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)
        self.b_setBothSchedules(remaining, remainingGifts)
         
        #print ("End __deliverBothPurchases")
        return Task.done
        

    def setGiftSchedule(self, onGiftOrder, doUpdateLater = True):
        self.setBothSchedules(None, onGiftOrder)
        return
        #I've rerouted this function to setBothSchedules to resolve a stomping issue with the mailbox feild
        #the original version follows
        
        #self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        #assert 0 , "setting gift schedule"
        if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air') and hasattr(self, 'name'):
            # Schedule the next gift.
            taskName = self.uniqueName('next-gift')
            taskMgr.remove(taskName)
            
            #print("setting gift schedule for %s" % (self.getName()))
            # Set a timeout to make the gift later.  We insist on
            # waiting at least 10 seconds mainly to give the avatar enough
            # time to completely manifest on the stateserver before we
            # start sending messages to it.
            now = (int)(time.time() / 60 + 0.5)
            nextItem = None
            nextTime = self.onGiftOrder.getNextDeliveryDate()
            nextItem = self.onGiftOrder.getNextDeliveryItem()
            if nextItem != None:
                pass
                #print(">>current time:%s" % (now))
                #print("next gift time:%s item:%s" % (nextTime, nextItem.getName()))
            else:
                pass
                #print("No items for gift delivery")
            if nextTime != None:
                #assertString = ("Now: %s Delivery %s" %(now, nextTime))
                #assert 0 , assertString
                duration = max(10.0, nextTime * 60 - time.time())
                duration += 30 #TOTAL HACK to keep __deliverGiftPurchase and __deliverPurchase from stomping each other
                taskMgr.doMethodLater(duration, self.__deliverGiftPurchase, taskName) #change function
        
                
    def getGiftSchedule(self):
        #return self.onGiftOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        return self.onGiftOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        
    def __deliverGiftPurchase(self, task):
        # Move one or more items from the onGiftOrder list to the
        # mailboxContents.
        """
        sends a request for the delivery of gifts to the uberdog
        the return will call the method that receives gifts which will return
        whether or not any new gifts were moved to the the mailbox
        """
             
        # Get the current time in minutes.
        now = (int)(time.time() / 60 + 0.5)

        # Extract out any items that should have been delivered by now.
        delivered, remaining = self.onGiftOrder.extractDeliveryItems(now)

        self.notify.info("Gift Delivery for %s: %s." % (self.doId, delivered))

        self.b_setMailboxContents(self.mailboxContents + delivered) #OLD MAILBOX
        simbase.air.deliveryManager.sendDeliverGifts(self.getDoId(), now)  

        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)
        
        return Task.done

    def __deliverPurchase(self, task):
        # Move one or more items from the onOrder list to the
        # mailboxContents.
        
        # Get the current time in minutes.
        now = (int)(time.time() / 60 + 0.5)

        # Extract out any items that should have been delivered by now.
        delivered, remaining = self.onOrder.extractDeliveryItems(now)

        self.notify.info("Delivery for %s: %s." % (self.doId, delivered))

        self.b_setMailboxContents(self.mailboxContents + delivered)
        self.b_setDeliverySchedule(remaining)
        
        self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NewItems)

        return Task.done

    def b_setMailboxContents(self, mailboxContents):
        self.setMailboxContents(mailboxContents)
        self.d_setMailboxContents(mailboxContents)

    def d_setMailboxContents(self, mailboxContents):
        self.sendUpdate("setMailboxContents", [mailboxContents.getBlob(store = CatalogItem.Customization)])
        if len(mailboxContents) == 0:
            self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NoItems)
        self.checkMailboxFullIndicator()

    def checkMailboxFullIndicator(self):
        """Raises the full indicator if we've got stuff in our mailbox."""
        if self.houseId and hasattr(self, 'air'):
            # Check to see if our house currently exists in the live
            # database.  If it does, we should update its mailbox flag
            # appropriately.
            if self.air:
                house = self.air.doId2do.get(self.houseId)
                if house and house.mailbox:
                    
                    house.mailbox.b_setFullIndicator(len(self.mailboxContents) != 0 or \
                                                     self.numMailItems or  \
                                                     self.getNumInvitesToShowInMailbox() or \
                                                     len(self.awardMailboxContents) != 0) 

    def setMailboxContents(self, mailboxContents):
        self.notify.debug("Setting mailboxContents to %s." % (mailboxContents))
        self.mailboxContents = CatalogItemList.CatalogItemList(mailboxContents, store = CatalogItem.Customization)
        self.notify.debug("mailboxContents is %s." % (self.mailboxContents))

    def getMailboxContents(self):
        return self.mailboxContents.getBlob(store = CatalogItem.Customization)

    """
    def b_setDeliveryboxContents(self, deliveryboxContents):
        self.setDeliveryboxContents(deliveryboxContents)
        self.d_setDeliveryboxContents(deliveryboxContents)
    def d_setDeliveryboxContents(self, deliveryboxContents):
        self.sendUpdate("setDeliveryboxContents", [deliveryboxContents.getBlob(store = CatalogItem.Customization | CatalogItem.GiftTag)])

        if len(deliveryboxContents) == 0:
            self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NoItems)

        if self.houseId:
            # Check to see if our house currently exists in the live
            # database.  If it does, we should update its mailbox flag
            # appropriately.
            house = self.air.doId2do.get(self.houseId)
            if house and house.mailbox:
                house.mailbox.b_setFullIndicator(len(deliveryboxContents) != 0)
        

    def setDeliveryboxContents(self, deliveryboxContents):
        self.notify.debug("Setting deliveryboxContents to %s." % (deliveryboxContents))
        self.deliveryboxContents = CatalogItemList.CatalogItemList(deliveryboxContents, store = CatalogItem.Customization | CatalogItem.GiftTag)
        self.notify.debug("deliveryboxContents is %s." % (self.deliveryboxContents))

    def getDeliveryboxContents(self):
        return self.deliveryboxContents.getBlob(store = CatalogItem.Customization | CatalogItem.GiftTag)
    """
    def b_setGhostMode(self, flag):
        self.setGhostMode(flag)
        self.d_setGhostMode(flag)
        
    def d_setGhostMode(self, flag):
        self.sendUpdate("setGhostMode", [flag])

    def setGhostMode(self, flag):
        self.ghostMode = flag

    def setImmortalMode(self, flag):
        self.immortalMode = flag

    def b_setSpeedChatStyleIndex(self, index):
        self.setSpeedChatStyleIndex(index)
        self.d_setSpeedChatStyleIndex(index)

    def d_setSpeedChatStyleIndex(self, index):
        self.sendUpdate("setSpeedChatStyleIndex", [index])

    def setSpeedChatStyleIndex(self, index):
        self.speedChatStyleIndex = index

    def getSpeedChatStyleIndex(self):
        return self.speedChatStyleIndex

    def b_setMaxMoney(self, maxMoney):
        self.d_setMaxMoney(maxMoney)
        self.setMaxMoney(maxMoney)

    def d_setMaxMoney(self, maxMoney):
        self.sendUpdate('setMaxMoney', [maxMoney])

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def addMoney(self, deltaMoney):
        # Add money to you wallet, and let the rest overflow into the bank
        # if money goes above max, deposit the rest into the bank
        money = deltaMoney + self.money
        pocketMoney = min(money, self.maxMoney)
        # update wallet
        self.b_setMoney(pocketMoney)
        # update bank
        overflowMoney = money-self.maxMoney
        if overflowMoney > 0:
            bankMoney = self.bankMoney + overflowMoney
            self.b_setBankMoney(bankMoney)
        
    def takeMoney(self, deltaMoney, bUseBank = True):
        # Take money from your wallet first, then from your bank
        # if the bool is set

        #do sanity checks
        totalMoney = self.money
        if bUseBank:
            totalMoney += self.bankMoney

        if (deltaMoney > totalMoney):
            self.notify.warning("Not enough money! AvId: %s Has:%s Charged:%s" % (self.doId, totalMoney, deltaMoney))
            return False

        #withdraw funds
        if (bUseBank and (deltaMoney > self.money)):
            self.b_setBankMoney(self.bankMoney - (deltaMoney - self.money))
            self.b_setMoney(0)
        else:
            self.b_setMoney(self.money - deltaMoney)

        return True

    def b_setMoney(self, money):
        
        # Auto-rich cheat: Money never goes down.
        if bboard.get('autoRich-%s' % self.doId, False):
            assert self.notify.debug("%s is ~autoRich, maxing money" % self.doId)
            money = self.getMaxMoney()

        self.setMoney(money)
        self.d_setMoney(money)

    def d_setMoney(self, money):
        self.sendUpdate('setMoney', [money])

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def getTotalMoney(self):
        return (self.money + self.bankMoney)

    def b_setMaxBankMoney(self, maxMoney):
        self.d_setMaxBankMoney(maxMoney)
        self.setMaxBankMoney(maxMoney)

    def d_setMaxBankMoney(self, maxMoney):
        self.sendUpdate("setMaxBankMoney", [maxMoney])

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney
    
    def b_setBankMoney(self, money):
        # SDN: if bank is too small, just make the excess
        # money vanish (for now)
        bankMoney = min(money, self.maxBankMoney)
        self.setBankMoney(bankMoney)
        self.d_setBankMoney(bankMoney)

    def d_setBankMoney(self, money):
        self.sendUpdate("setBankMoney", [money])

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def tossPie(self, x, y, z, h, p, r, sequence, power, timestamp32):
        if not self.validate(
                self.doId, self.numPies > 0,
                'tossPie with no pies available'):
            return
        if self.numPies != ToontownGlobals.FullPies:
            self.b_setNumPies(self.numPies - 1)

    
    def b_setNumPies(self, numPies):
        self.setNumPies(numPies)
        self.d_setNumPies(numPies)

    def d_setNumPies(self, numPies):
        self.sendUpdate('setNumPies', [numPies])

    def setNumPies(self, numPies):
        self.numPies = numPies
    
    def b_setPieType(self, pieType):
        self.setPieType(pieType)
        self.d_setPieType(pieType)

    def d_setPieType(self, pieType):
        self.sendUpdate('setPieType', [pieType])

    def setPieType(self, pieType):
        self.pieType = pieType
    
    def d_setTrophyScore(self, score):
        self.sendUpdate("setTrophyScore", [score])


    ### Auto toon-up functions ###

    def stopToonUp(self):
        taskMgr.remove(self.uniqueName("safeZoneToonUp"))
        self.ignore(self.air.getAvatarExitEvent(self.getDoId()))
        
    def startToonUp(self, healFrequency):
        """
        Starts the auto-toon-up task that occurs whenever the avatar
        is in a playground or in his estate.
        """
        self.stopToonUp()
        self.healFrequency = healFrequency
        self.__waitForNextToonUp()

    def __waitForNextToonUp(self):
        # Spawns a doLater for this av to be healed next time
        taskMgr.doMethodLater(self.healFrequency, self.toonUpTask,
                              self.uniqueName("safeZoneToonUp"))

    def toonUpTask(self, task):
        self.toonUp(1)
        self.__waitForNextToonUp()
        return Task.done

    def toonUp(self, hpGained, quietly = 0, sendTotal = 1):
        # Adds the indicated hit points to the avatar's total.  If
        # quietly is 0 (the default), numbers will fly out of his
        # head; if sendTotal is 1 (the default), the resulting hp
        # value will be sent as well to ensure client and AI are in
        # agreement.  (Without sendTotal, the client will do the
        # arithmetic himself, and presumably will still arrive at the
        # same value.)

        # first clamp toonup to hp limit
        if hpGained > self.maxHp:
            hpGained = self.maxHp
            
        # First, send the message to make the numbers fly out.
        if not quietly:
            self.sendUpdate('toonUp', [hpGained])

        # Then, we recompute the HP.

        # If hp is below zero, it means we're at a timeout in the
        # playground, in which case we respect that it is below zero
        # until we get our head above water.  If our toonup would take
        # us above zero, then we pretend we started at zero in the
        # first place, ignoring the timeout.
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = max(self.hp, 0) + hpGained

        clampedHp = min(self.hp, self.maxHp)
        if not self.hpOwnedByBattle:
            self.hp = clampedHp

        # Finally, send the new total to the client so he's with us.
        if sendTotal and not self.hpOwnedByBattle:
            self.d_setHp(clampedHp)

    def isToonedUp(self):
        return self.hp >= self.maxHp

    def makeBlackCat(self):
        # turn this cat into a black cat
        # are we a cat?
        if self.dna.getAnimal() != 'cat':
            return 'not a cat'
        self.air.writeServerEvent('blackCat', self.doId, '')
        # set the dna
        newDna = ToonDNA.ToonDNA()
        newDna.makeFromNetString(self.dna.makeNetString())
        black = 26
        newDna.updateToonProperties(armColor=black, legColor=black,
                                    headColor=black)
        self.b_setDNAString(newDna.makeNetString())
        # None means no error, return it explicitly
        return None

    def b_announceBingo(self):
        self.d_announceBingo()
        self.announceBingo

    def d_announceBingo(self):
        self.sendUpdate('announceBingo', [])

    def announceBingo(self):
        pass

    def incrementPopulation(self):
        if self.isPlayerControlled():
            DistributedPlayerAI.DistributedPlayerAI.incrementPopulation(self)
    def decrementPopulation(self):
        if self.isPlayerControlled():
            DistributedPlayerAI.DistributedPlayerAI.decrementPopulation(self)

    if __dev__:
        def _logGarbage(self):
            if self.isPlayerControlled():
                DistributedPlayerAI.DistributedPlayerAI._logGarbage(self)

    # stuff for resistance speedchat handling
    def reqSCResistance(self, msgIndex, nearbyPlayers):
        self.d_setSCResistance(msgIndex, nearbyPlayers)

    def d_setSCResistance(self, msgIndex, nearbyPlayers):
        if not ResistanceChat.validateId(msgIndex):
            self.air.writeServerEvent('suspicious', self.doId, 'said resistance %s, which is invalid.' % (msgIndex))
            return

        if not self.removeResistanceMessage(msgIndex):
            self.air.writeServerEvent('suspicious', self.doId, 'said resistance %s, but does not have it.' % (msgIndex))
            return

        affectedPlayers = []
        for toonId in nearbyPlayers:
            toon = self.air.doId2do.get(toonId)
            if not toon:
                self.notify.warning("%s said resistance %s for %s; not on server" % (self.doId, msgIndex, toonId))
            elif toon.__class__ != DistributedToonAI:
                # We check for exact equivalence, not isinstance(), so
                # we don't consider NPC's.
                self.air.writeServerEvent('suspicious', self.doId, 'said resistance %s for %s; object of type %s' % (msgIndex, toonId, toon.__class__.__name__))
            elif toonId in affectedPlayers:
                self.air.writeServerEvent('suspicious', self.doId, 'said resistance %s for %s twice in same message.' % (msgIndex, toonId))
                
            else:
                toon.doResistanceEffect(msgIndex)
                affectedPlayers.append(toonId)

        if len(affectedPlayers) > 50:
            self.air.writeServerEvent('suspicious', self.doId, 'said resistance %s for %s toons.' % (msgIndex, len(affectedPlayers)))
            self.notify.warning('%s said resistance %s for %s toons: %s' % (self.doId, msgIndex, len(affectedPlayers), affectedPlayers))
            

        self.sendUpdate('setSCResistance', [msgIndex, affectedPlayers])

        # log the use of a resistance chat phrase (speakerId, msgType, value, list of affectedToons)
        type = ResistanceChat.getMenuName(msgIndex)
        value = ResistanceChat.getItemValue(msgIndex)
        self.air.writeServerEvent('resistanceChat', self.zoneId,
                                  '%s|%s|%s|%s' % (self.doId, type, value, affectedPlayers) )
        

    def doResistanceEffect(self, msgIndex):
        # Applies the effect of the indicated resistance chat message,
        # as if someone has said it to me.

        msgType, itemIndex = ResistanceChat.decodeId(msgIndex)
        msgValue = ResistanceChat.getItemValue(msgIndex)

        if msgType == ResistanceChat.RESISTANCE_TOONUP:
            # Toon-up
            if msgValue == -1:
                self.toonUp(self.maxHp)
            else:
                self.toonUp(msgValue)
            self.notify.debug("Toon-up for " + self.name)
        elif msgType == ResistanceChat.RESISTANCE_RESTOCK:
            # Restock
            self.inventory.NPCMaxOutInv(msgValue)
            self.d_setInventory(self.inventory.makeNetString())
            self.notify.debug("Restock for " + self.name)
        elif msgType == ResistanceChat.RESISTANCE_MONEY:
            # Rich
            if msgValue == -1:
                self.addMoney(999999)
            else:
                self.addMoney(msgValue)
            self.notify.debug("Money for " + self.name)

    def squish(self, damage):
        self.takeDamage(damage)

    if( simbase.wantKarts ):
        ##################################################################
        # Kart DNA Methods 
        ##################################################################
        def hasKart( self ):
            """
            Purpose: The hasKart Method determines whether the Toon
            currently owns a kart.

            Params: None
            Return: Bool - True or False
            """
            return ( self.kartDNA[ KartDNA.bodyType ] != -1 )
        
        def b_setTickets( self, numTickets ):
            """
            Purpose: The b_setTickets Method sets the number of
            tickets that the toon has by calling local and
            distributed set methods.

            Params: numTickets - the new number of tickets that a toon has.
            Return: None
            """
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.d_setTickets( numTickets )
            self.setTickets( numTickets )

        def d_setTickets( self, numTickets ):
            """
            Purpose: The d_setTickets Method sets the number of
            tickets that the toon has by sending a distributed
            message to the client.

            Params: numTickets - the number of tickets that a toon has.
            Return: None
            """
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.sendUpdate( "setTickets", [ numTickets ] )

        def setTickets( self, numTickets ):
            """
            Purpose: The setTickets Method sets the number of
            tickets that the toon has. Tickets are gained by
            winning races and events.

            Params: numTickets - the new number of tickets that a toon has.
            Return: None
            """
            if numTickets > RaceGlobals.MaxTickets:
                numTickets = RaceGlobals.MaxTickets
            self.tickets = numTickets

        def getTickets( self ):
            """
            Purpose: The getTickets Method obtains the number of
            tickets that a toon can has.

            Params: None
            Return: tickets - the number of tickets a toon has.
            """
            return self.tickets

        ### karting trophy list ###

        def b_setKartingTrophies(self, trophyList):
            # update the trophies won list
            self.setKartingTrophies(trophyList)
            self.d_setKartingTrophies(trophyList)

        def setKartingTrophies(self, trophyList):
            self.notify.debug("setting kartingTrophies to %s" % trophyList)
            self.kartingTrophies = trophyList
        
        def d_setKartingTrophies(self, trophyList):
            self.sendUpdate("setKartingTrophies", [trophyList])

        def getKartingTrophies(self):
            return self.kartingTrophies

        ### karting history list ###

        def b_setKartingHistory(self, history):
            # update the trophies won list
            self.setKartingHistory(history)
            self.d_setKartingHistory(history)

        def setKartingHistory(self, history):
            self.notify.debug("setting kartingHistory to %s" % history)
            self.kartingHistory = history
        
        def d_setKartingHistory(self, history):
            self.sendUpdate("setKartingHistory", [history])

        def getKartingHistory(self):
            return self.kartingHistory

        ### karting personal best list ###

        def b_setKartingPersonalBest(self, bestTimes):
            # update the personal best times list
            best1 = bestTimes[0:6]
            best2 = bestTimes[6:]
            self.setKartingPersonalBest(best1)
            self.setKartingPersonalBest2(best2)
            self.d_setKartingPersonalBest(bestTimes)

        def d_setKartingPersonalBest(self, bestTimes):
            best1 = bestTimes[0:6]
            best2 = bestTimes[6:]
            self.sendUpdate("setKartingPersonalBest", [best1])
            self.sendUpdate("setKartingPersonalBest2", [best2])

        def setKartingPersonalBest(self, bestTimes):
            self.notify.debug("setting karting to %s" % bestTimes)
            self.kartingPersonalBest = bestTimes

        def setKartingPersonalBest2(self, bestTimes2):
            self.notify.debug("setting karting2 to %s" % bestTimes2)
            self.kartingPersonalBest2 = bestTimes2

        def getKartingPersonalBest(self):
            return self.kartingPersonalBest

        def getKartingPersonalBest2(self):
            return self.kartingPersonalBest2

        def getKartingPersonalBestAll(self):
            return self.kartingPersonalBest + \
                   self.kartingPersonalBest2

        def setKartDNA( self, kartDNA ):
            """
            Purpose: The setKartDNA Method provides the opportunity to
            fill out kart DNA in collective way.
            
            Params: kartDNA - the kart dna as a list
            Return: None
            """
            self.b_setKartBodyType( kartDNA[ KartDNA.bodyType ] )
            self.b_setKartBodyColor( kartDNA[ KartDNA.bodyColor ] )
            self.b_setKartAccColor( kartDNA[ KartDNA.accColor ] )
            self.b_setKartEngineBlockType( kartDNA[ KartDNA.ebType ] )
            self.b_setKartSpoilerType( kartDNA[ KartDNA.spType ] )
            self.b_setKartFrontWheelWellType( kartDNA[ KartDNA.fwwType ] )
            self.b_setKartBackWheelWellType( kartDNA[ KartDNA.bwwType ] )
            self.b_setKartRimType( kartDNA[ KartDNA.rimsType ] )
            self.b_setKartDecalType( kartDNA[ KartDNA.decalType ] )

        def b_setKartBodyType( self, bodyType ):
            """
            Purpose: The b_setKartBodyType Method handles the setting of the
            kart body type by appropriately calling the local AI and
            distributed client set methods.

            Params: bodyType - the body type of the kart which the toon
                               currently owns.
            Return: None
            """
            self.d_setKartBodyType( bodyType )
            self.setKartBodyType( bodyType )

        def d_setKartBodyType( self, bodyType ):
            """
            Purpose: The d_setKartBodyType Method handles the distributed
            client call to update the body type on the client for
            the toon.

            Params: bodyType - the body type of the kart which the toon
                               currently owns.
            Return: None
            """
            self.sendUpdate( 'setKartBodyType', [ bodyType ] )

        def setKartBodyType( self, bodyType ):
            """
            Purpose: The setKartBodyType Method sets the local AI side
            body type of the kart that the toon currently owns.

            
            Params: bodyType - the body type of the kart which the toon
                               currently owns.
            Return: None
            """
            self.kartDNA[ KartDNA.bodyType ] = bodyType

        def getKartBodyType( self ):
            """
            Purpose: The getKartBodyType Method obtains the local AI side
            body type of the kart that the toon currently owns.

            Params: None
            Return: bodyType - the body type of the kart.
            """
            return self.kartDNA[ KartDNA.bodyType ]

        def b_setKartBodyColor( self, bodyColor ):
            """
            Purpose: The b_setKartBodyColor Method appropriately sets the
            body color the kart by calling the local and distributed
            set methods.

            Params: bodyColor - the color of the kart body.
            Return: None
            """
            self.d_setKartBodyColor( bodyColor )
            self.setKartBodyColor( bodyColor )

        def d_setKartBodyColor( self, bodyColor ):
            """
            Purpose: The d_setKartBodyColor Method appropriately sets the
            body color of the kart on the client side by sending a
            distributed update message to the client.

            Params: bodyColor - the color of the kart body.
            Return: None
            """
            self.sendUpdate( 'setKartBodyColor', [ bodyColor ] )

        def setKartBodyColor( self, bodyColor ):
            """
            Purpose: The setKartBodyColor Method appropriately sets
            the body color of the lient on the ai side by updating the
            local kart dna.

            Params: bodyColor - the color of the kart body.
            Return: None
            """
            self.kartDNA[ KartDNA.bodyColor ] = bodyColor

        def getKartBodyColor( self ):
            """
            Purpose: The getKartBodyColor Method obtains the current
            body color of the kart.

            Params: None
            Return: bodyColor - the color of the kart body.
            """
            return self.kartDNA[ KartDNA.bodyColor ]

        def b_setKartAccessoryColor( self, accColor ):
            """
            Purpose: The b_setKartAccessoryColor Method appropriately
            sets the accessory color by calling the local and distributed
            set methods.

            Params: accColor - the color of the accessories.
            Return: None
            """
            self.d_setKartAccessoryColor( accColor )
            self.setKartAccessoryColor( accColor )

        def d_setKartAccessoryColor( self, accColor ):
            """
            Purpose: The d_setKartAccessoryColor Method appropriately sets
            the accessory color of the client by sending a distributed
            message to the client.

            Params: accColor - the Color of the accessories.
            Return: None
            """
            self.sendUpdate( 'setKartAccessoryColor', [ accColor ] )

        def setKartAccessoryColor( self, accColor ):
            """
            Purpose: The setKartAccessoryColor Method appropriately sets
            the accessory color of the local ai side by updating the kart
            dna.

            Params: accColor - the color of the accessories.
            Return: None
            """
            self.kartDNA[ KartDNA.accColor ] = accColor

        def getKartAccessoryColor( self ):
            """
            Purpose: The getKartAccessoryColor Method obtains the
            accessory color for the kart.

            Params: None
            Return: accColor - the color of the accessories
            """
            return self.kartDNA[ KartDNA.accColor ]

        def b_setKartEngineBlockType( self, ebType ):
            """
            Purpose: The b_setKartEngineBlockType Method sets the engine
            block type of accessory for the kart by calling the local
            and distributed set methods.

            Params: ebType - the type of engine block accessory.
            Return: None
            """
            self.d_setKartEngineBlockType( ebType )
            self.setKartEngineBlockType( ebType )

        def d_setKartEngineBlockType( self, ebType ):
            """
            Purpose: The d_setKartEngineBlockType Method sets the engine
            block type accessory for the kart by sending a distributed
            message to the client.

            Params: ebType - the type of engine block accessory.
            Return: None
            """
            self.sendUpdate( "setKartEngineBlockType", [ ebType ] )

        def setKartEngineBlockType( self, ebType ):
            """
            Purpose: The setKartEngineBlockType Method sets the engine
            block type accessory for the kart by updating the Kart DNA.
            
            Params: ebType - the type of engine block accessory.
            Return: None
            """
            self.kartDNA[ KartDNA.ebType ] = ebType

        def getKartEngineBlockType( self ):
            """
            Purpose: The getKartEngineBlockType Method obtains the engine
            block type accessory for the kart by accessing the
            current Kart DNA.
                        
            Params: None
            Return: ebType - the type of engine block accessory.
            """
            return self.kartDNA[ KartDNA.ebType ]

        def b_setKartSpoilerType( self, spType ):
            """
            Purpose: The b_setKartSpoilerType Method sets the spoiler
            type accessory for the kart by calling the local and
            distributed set methods.

            Params: spType - the type of spoiler accessory
            Return: None
            """
            self.d_setKartSpoilerType( spType )
            self.setKartSpoilerType( spType )

        def d_setKartSpoilerType( self, spType ):
            """
            Purpose: The d_setKartSpoilerType Method sets the spoiler
            type accessory for the kart by sending a distributed
            message to the client.

            Params: spType - the type of spoiler accessory
            Return: None
            """
            self.sendUpdate( "setKartSpoilerType", [ spType ] )

        def setKartSpoilerType( self, spType ):
            """
            Purpose: The setKartSpoilerType Method sets the spoiler
            type accessory for the kart by updating the Kart DNA.

            Params: spType - the type of spoiler accessory
            Return: None
            """
            self.kartDNA[ KartDNA.spType ] = spType

        def getKartSpoilerType( self ):
            """
            Purpose: The getKartSpoilerType Method obtains the spoiler
            type accessory for the kart by accessing the current Kart DNA.
            
            Params: None
            Return: spType - the type of spoiler accessory 
            """
            return self.kartDNA[ KartDNA.spType ]

        def b_setKartFrontWheelWellType( self, fwwType ):
            """
            Purpose: The b_setKartFrontWheelWellType Method sets the
            front wheel well accessory for the kart by calling the local
            and distributed set methods for the DNA.

            Params: fwwType - the type of Front Wheel Well accessory
            Return: None
            """
            self.d_setKartFrontWheelWellType( fwwType )
            self.setKartFrontWheelWellType( fwwType )

        def d_setKartFrontWheelWellType( self, fwwType ):
            """
            Purpose: The d_setKartFrontWheelWellType Method sets the
            front wheel well accessory for the kart by sending a
            distributed message to the client to update the DNA.

            Params: fwwType - the type of Front Wheel Well accessory
            Return: None
            """
            self.sendUpdate( "setKartFrontWheelWellType", [ fwwType ] )

        def setKartFrontWheelWellType( self, fwwType ):
            """
            Purpose: The setKartFrontWheelWellType Method sets the
            front wheel well accessory for the kart updating the
            Kart DNA.

            Params: fwwType - the type of Front Wheel Well accessory
            Return: None
            """
            self.kartDNA[ KartDNA.fwwType ] = fwwType

        def getKartFrontWheelWellType( self ):
            """
            Purpose: The getKartFrontWheelWellType Method obtains the
            front wheel well accessory for the kart accessing the
            Kart DNA.

            Params: None
            Return: fwwType - the type of Front Wheel Well accessory
            """
            return self.kartDNA[ KartDNA.fwwType ]

        def b_setKartBackWheelWellType( self, bwwType ):
            """
            Purpose: The b_setKartWheelWellType Method sets the Back
            Wheel Wheel accessory for the kart by calling the local
            and distributed set methods.

            Params: bwwType - the type of Back Wheel Well accessory.
            Return: None
            """
            self.d_setKartBackWheelWellType( bwwType )
            self.setKartBackWheelWellType( bwwType )

        def d_setKartBackWheelWellType( self, bwwType ):
            """
            Purpose: The b_setKartWheelWellType Method sets the Back
            Wheel Wheel accessory for the kart by sending a distributed
            message to the client.

            Params: bwwType - the type of Back Wheel Well accessory.
            Return: None
            """
            self.sendUpdate( "setKartBackWheelWellType", [ bwwType ] )

        def setKartBackWheelWellType( self, bwwType ):
            """
            Purpose: The setKartWheelWellType Method sets the Back
            Wheel Wheel accessory for the kart by updating the Kart DNA.

            Params: bwwType - the type of Back Wheel Well accessory.
            Return: None
            """
            self.kartDNA[ KartDNA.bwwType ] = bwwType

        def getKartBackWheelWellType( self ):
            """
            Purpose: The getKartWheelWellType Method obtains the Back
            Wheel Wheel accessory for the kart by accessing the Kart DNA.

            Params: bwwType - the type of Back Wheel Well accessory.
            Return: None
            """
            return self.kartDNA[ KartDNA.bwwType ]

        def b_setKartRimType( self, rimsType ):
            """
            Purpose: The b_setKartRimType Method sets the rims accessory
            for the karts tires by calling the local and distributed
            set methods.

            Params: rimsType - the type of rims for the kart tires.
            Return: None
            """
            self.d_setKartRimType( rimsType )
            self.setKartRimType( rimsType )

        def d_setKartRimType( self, rimsType ):
            """
            Purpose: The d_setKartRimType Method sets the rims accessory
            for the karts tires by sending a distributed message to the
            client for an update.

            Params: rimsType - the type of rims for the kart tires.
            Return: None
            """
            self.sendUpdate( "setKartRimType", [ rimsType ] )

        def setKartRimType( self, rimsType ):
            """
            Purpose: The setKartRimType Method sets the rims accessory
            for the karts tires by updating the Kart DNA.

            Params: rimsType - the type of rims for the kart tires.
            Return: None
            """
            self.kartDNA[ KartDNA.rimsType ] = rimsType

        def getKartRimType( self ):
            """
            Purpose: The setKartRimType Method sets the rims accessory
            for the karts tires by accessing the Kart DNA.
            
            Params: None
            Return: rimsType - the type of rims for the kart tires.
            """
            return self.kartDNA[ KartDNA.rimsType ]

        def b_setKartDecalType( self, decalType ):
            """
            Purpose: The b_setKartDecalType Method sets the decal
            accessory of the kart by calling local and distributed
            set methods.
            
            Params: decalType - the type of decal set for the kart.
            Return: None
            """
            self.d_setKartDecalType( decalType )
            self.setKartDecalType( decalType )

        def d_setKartDecalType( self, decalType ):
            """
            Purpose: The d_setKartDecalType Method sets the decal
            accessory of the kart by sending a distributed message to the
            client to update the DNA.
            
            Params: decalType - the type of decal set for the kart.
            Return: None
            """
            self.sendUpdate( "setKartDecalType", [ decalType ] )

        def setKartDecalType( self, decalType ):
            """
            Purpose: The setKartDecalType Method sets the decal
            accessory of the kart by updating the Kart DNA.
            
            Params: decalType - the type of decal set for the kart.
            Return: None
            """
            self.kartDNA[ KartDNA.decalType ] = decalType

        def getKartDecalType( self ):
            """
            Purpose: The getKartDecalType Method obtains the decal
            accessory of the kart by accessing the Kart DNA.
                        
            Params: None
            Return: decalType - the type of decal set for the kart.
            """
            return self.kartDNA[ KartDNA.decalType ]
        
        def b_setKartAccessoriesOwned( self, accessories ):
            """
            Purpose: The setKartAccessoriesOwned Method handles the
            distributed and local calls to update the Kart Accessories
            owned by the toon on both the client and AI side.

            Params: accessories - The accessories owned.
            Return: None
            """
            self.d_setKartAccessoriesOwned( accessories )
            self.setKartAccessoriesOwned( accessories )

        def d_setKartAccessoriesOwned( self, accessories ):
            """
            Purpose: The d_setKartAccessoriesOwned Method handles the
            distributed call to update the Kart Accessories owned by the
            Toon on the AI Side.

            Params: accessories - The accessories owned.
            Return: None
            """
            self.sendUpdate( 'setKartAccessoriesOwned', [ accessories ] )

        def setKartAccessoriesOwned( self, accessories ):
            """
            Purpose: The setKartAccessoriesOwned Method handles the local
            call to properly set the Accessories owned by the toon on the
            AI Side.

            Params: accessories - the ids of the accessories.
            Return: None
            """
            if( __debug__ ):
                import pdb
                #pdb.set_trace()

            self.accessories = accessories

        def getKartAccessoriesOwned( self ):
            """
            Purpose: The getKartAccessoriesOwned Method retrieves the
            accessories that are owned by the toon on the AI Side.

            Params: None
            Return: [] - List of Accessories owned by the toon.
            """
            owned = copy.deepcopy(self.accessories)
            while InvalidEntry in owned:
                owned.remove(InvalidEntry)
            return owned

        def addOwnedAccessory( self, accessoryId ):
            """
            Purpose: The addOwnedAccessory Method performs the update
            on the accessories owned by the toon. It also provides a
            the appropriate checks on whether the accessory is valid.

            Params: accessoryId - the id of the accessory.
            Return: None
            """
            print "in add owned accessory"
            if( AccessoryDict.has_key( accessoryId ) ):
                # Determine if the toon already owns this accessory.
                if( self.accessories.count( accessoryId ) > 0 ):
                    self.air.writeServerEvent( "suspicious", self.doId, 'attempt to add accessory %s which is already owned!' % ( accessoryId ) )
                    return
                
                # Determine if the toon owns too many accessories.
                if( self.accessories.count( InvalidEntry ) > 0 ):
                    accList = list( self.accessories )
                    index = self.accessories.index( InvalidEntry )
                    accList[ index ] = accessoryId

                    # set the accessory list
                    self.b_setKartAccessoriesOwned( accList )
                else:
                    self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to add accessory %s when accessory inventory is full!' % ( accessoryId ))
                    return
            else:
                self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to add accessory %s which is not a valid accessory.' % ( accessoryId ) )
                return

        def removeOwnedAccessory( self, accessoryId ):
            """
            Purpose: The removeOwnedAccessory Method performs an update
            on the accessories owned by the toon. It also provides the
            appropriate checks to determine whether the accessory to be
            deleted is removed.

            Params: accessoryId - the id of the accessory.
            Return: None
            """
            if( AccessoryDict.has_key( accessoryId ) ):
                # Make certain tha the toon owns this accessory.
                if( self.accessories.count( accessoryId ) == 0 ):
                    self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to remove accessory %s which is not currently owned!' % ( accessoryId ) )
                    return
                else:
                    # TODO - do not allow removal of last set of rims.
                    accList = list( self.accessories )
                    index = self.accessories.index( accessoryId )
                    accList[ index ] = InvalidEntry

                    # log for CS verification
                    self.air.writeServerEvent( 'deletedKartingAccessory', self.doId, '%s' % ( accessoryId ) )
                    
                    # set the accessory owned list
                    self.b_setKartAccessoriesOwned( accList )                
            else:
                self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to remove accessory %s which is not a valid accessory.' % ( accessoryId ) )
                return
            

        def updateKartDNAField( self, dnaField, fieldValue ):
            """
            Purpose: The udpateKartDNAField Method performs the
            the update on an accessory based on a client request.

            Params: accessoryType - the kind of accessory to update
                    accessoryId - the new accessory id.
            Return: None
            """

            # Determine if the field is a valid.
            if( not checkKartFieldValidity( dnaField ) ):
                # Validity Check Failed - log as suspicious
                self.air.writeServerEvent('suspicious', self.doId, 'attempt to update to dna value  %s in the invalid field %s' % (fieldValue, dnaField))
                return

            # Check if it is a kart body type or what can be considered
            # an accessory.
            if( dnaField == KartDNA.bodyType ):
                if( ( fieldValue not in KartDict.keys() ) and ( fieldValue != InvalidEntry ) ):
                    self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update kart body to invalid body %s.' % ( fieldValue ) )
                    return
                self.b_setKartBodyType( fieldValue )
            else:
                # First check non-paint related accessories
                accFields = [ KartDNA.ebType, KartDNA.spType, KartDNA.fwwType,
                              KartDNA.bwwType, KartDNA.rimsType, KartDNA.decalType ]
                colorFields = [ KartDNA.bodyColor, KartDNA.accColor ]
                
                if( dnaField in accFields ):
                    if( fieldValue == InvalidEntry ):
                        # Invalid entries mean that the kart no longer
                        # has a current accessory of this type.
                        self.__updateKartDNAField( dnaField, fieldValue )                        
                    else:
                        # Check to make sure the accessory is owned by the
                        # toon.
                        if( fieldValue not in self.accessories ):
                            # There has been an illegal attempt to update
                            # to an accessory that is not currently owned
                            # by the toon.
                            self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update to accessory %s which is not currently owned.' % ( fieldValue ) )
                            return

                        field = getAccessoryType( fieldValue )
                        if( field == InvalidEntry ):
                            # There has been an illegal attempt to update
                            # an accessory in an invalid field.
                            self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update accessory %s in an illegal field %s' % ( fieldValue, field ) )
                            return
                        elif( field != dnaField ):
                            # There has been an illegal attempt to update
                            # an accessory field that is not the same as
                            # the field specified from the client.
                            self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update accessory %s in a field %s that does not match client specified field %s' % ( fieldValue, field, dnaField ) )
                            return
                        else:
                            pass

                        # Passed validity checks, now update the field
                        # value for the specified dna field.
                        self.__updateKartDNAField( dnaField, fieldValue )

                elif( dnaField in colorFields ):
                    # Check if the field is invalid.
                    if( fieldValue == InvalidEntry ):
                        # Invalid entries mean that the kart no longer
                        # has a current color.                        
                        self.__updateKartDNAField( dnaField, fieldValue )                          
                    else:
                        # Determine if the accessory is currently owned by
                        # the toon.
                        if( fieldValue not in self.accessories ):
                            if( fieldValue != getDefaultColor() ):
                                # An attempt to update to a color that is not
                                # currently owned has been made.
                                self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update to color %s which is not owned!' % ( fieldValue ) )
                                return
                            elif( ( fieldValue == getDefaultColor() ) and ( self.kartDNA[ dnaField ] != InvalidEntry ) ):
                                # An attempt to update the color to the
                                # default color when the dna Field is not
                                # invalid. The color is not owned, thus
                                # the toon should not be able to paint.
                                self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update to default color %s which is not owned!' % ( fieldValue ) )
                                return
                               
                        # Make certain the value is truly a color and not of
                        # another accessory type.
                        #
                        # NOTE: All colors are listed under KartDNA.bodyColor
                        #       in the AccessoryTypeDict.
                        if( getAccessoryType( fieldValue ) != KartDNA.bodyColor ):
                            # The accessory type does not match.
                            self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to update invalid color %s for dna field %s' % ( fieldValue, dnaField ) )
                            return

                        # All checks should have passed at this point, now
                        # update the color.
                        self.__updateKartDNAField( dnaField, fieldValue )

                else:
                    # The specified dna field is not valid!
                    self.air.writeServerEvent( 'suspicious', self.doId, 'attempt to udpate accessory %s in the invalid field %s' %( fieldValue, dnaField ) )
                    return

        def __updateKartDNAField( self, dnaField, fieldValue ):
            """
            """
            if( dnaField == KartDNA.bodyColor ):
                self.b_setKartBodyColor( fieldValue )
            elif( dnaField == KartDNA.accColor ):
                self.b_setKartAccessoryColor( fieldValue )
            elif( dnaField == KartDNA.ebType ):
                self.b_setKartEngineBlockType( fieldValue )
            elif( dnaField == KartDNA.spType ):
                self.b_setKartSpoilerType( fieldValue )
            elif( dnaField == KartDNA.fwwType ):
                self.b_setKartFrontWheelWellType( fieldValue )
            elif( dnaField == KartDNA.bwwType ):
                self.b_setKartBackWheelWellType( fieldValue )
            elif( dnaField == KartDNA.rimsType ):
                self.b_setKartRimType( fieldValue )
            elif( dnaField == KartDNA.decalType ):
                self.b_setKartDecalType( fieldValue )
            else:
                pass
            
        def setAllowSoloRace(self, allowSoloRace):
            self.allowSoloRace = allowSoloRace

        def setAllowRaceTimeout(self, allowRaceTimeout):
            self.allowRaceTimeout = allowRaceTimeout
        
    if simbase.wantPets:
        # PETS
        def getPetId(self):
            return self.petId
        def b_setPetId(self, petId):
            self.d_setPetId(petId)
            self.setPetId(petId)
        def d_setPetId(self, petId):
            self.sendUpdate('setPetId', [petId])
        def setPetId(self, petId):
            self.petId = petId

        # list of tricks that we can train pets in
        # these are trick IDs, not SpeedChat phrases
        def getPetTrickPhrases(self):
            return self.petTrickPhrases
        def b_setPetTrickPhrases(self, tricks):
            self.setPetTrickPhrases(tricks)
            self.d_setPetTrickPhrases(tricks)
        def d_setPetTrickPhrases(self, tricks):
            self.sendUpdate('setPetTrickPhrases', [tricks])
        def setPetTrickPhrases(self, tricks):
            self.petTrickPhrases = tricks

        def deletePet(self):
            if self.petId == 0:
                self.notify.warning("this toon doesn't have a pet to delete!")
                return

            simbase.air.petMgr.deleteToonsPet(self.doId)
            
        def setPetMovie(self, petId, flag):
            self.notify.debug("setPetMovie: petId: %s, flag: %s" % (petId, flag))
            pet = simbase.air.doId2do.get(petId)
            if pet is not None:
                if pet.__class__.__name__ == 'DistributedPetAI':
                    pet.handleAvPetInteraction(flag, self.getDoId())
                else:
                    self.air.writeServerEvent(
                        'suspicious', self.doId,
                        'setPetMovie: playing pet movie %s on non-pet object %s' % (
                        flag, petId))

        def setPetTutorialDone(self, bDone):
            #don't actually USE the boolean... it's just there to tell the db what to store
            self.notify.debug("setPetTutorialDone")
            self.bPetTutorialDone = True

        def setFishBingoTutorialDone(self, bDone):
            #don't actually USE the boolean... it's just there to tell the db what to store
            self.notify.debug("setFishBingoTutorialDone")
            self.bFishBingoTutorialDone = True

        def setFishBingoMarkTutorialDone(self, bDone):
            #don't actually USE the boolean... it's just there to tell the db what to store
            self.notify.debug("setFishBingoMarkTutorialDone")
            self.bFishBingoMarkTutorialDone = True

        def enterEstate(self, ownerId, zoneId):
            DistributedToonAI.notify.debug('enterEstate: %s %s %s' % (
                self.doId, ownerId, zoneId))
            # we should be in the correct zone at this point
            assert self.zoneId == zoneId
            if self.wasInEstate():
                self.cleanupEstateData()

            # create a collision sphere for the pets to collide with
            collSphere = CollisionSphere(0,0,0,self.getRadius())
            collNode = CollisionNode('toonColl-%s' % self.doId)
            collNode.addSolid(collSphere)
            collNode.setFromCollideMask(BitMask32.allOff())
            collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
            self.collNodePath = self.attachNewNode(collNode)
            # start a task to position the collision sphere at Z=0
            # wrt to render
            # this must run after the sphere is moved (distributed updates)
            # and before pet collisions are run
            # This might be more efficient as a single task that moves
            # all spheres to zero in a single pass
            taskMgr.add(self._moveSphere, self._getMoveSphereTaskName(),
                        priority = OTPGlobals.AICollMovePriority)
            self.inEstate = 1
            self.estateOwnerId = ownerId
            self.estateZones = simbase.air.estateMgr.getEstateZones(ownerId)
            self.estateHouseZones = simbase.air.estateMgr.getEstateHouseZones(
                ownerId)

            self.enterPetLook()

        def _getPetLookerBodyNode(self):
            return self.collNodePath

        def _getMoveSphereTaskName(self):
            return 'moveSphere-%s' % self.doId

        def _moveSphere(self, task):
            self.collNodePath.setZ(self.getRender(), 0)
            return Task.cont

        def isInEstate(self):
            return hasattr(self, 'inEstate') and self.inEstate

        def exitEstate(self, ownerId=None, zoneId=None):
            DistributedToonAI.notify.debug('exitEstate: %s %s %s' % (
                self.doId, ownerId, zoneId))
            DistributedToonAI.notify.debug('current zone: %s' % (
                self.zoneId))

            assert self.isInEstate(), "already exitted estate"

            self.exitPetLook()

            taskMgr.remove(self._getMoveSphereTaskName())
            # remove the collision sphere
            self.collNodePath.removeNode()
            del self.collNodePath
            del self.estateOwnerId
            del self.estateHouseZones
            del self.inEstate
            self._wasInEstate = 1

        def wasInEstate(self):
            return hasattr(self, '_wasInEstate') and self._wasInEstate
        def cleanupEstateData(self):
            del self.estateZones
            del self._wasInEstate

        def setSC(self, msgId):
            DistributedToonAI.notify.debug('setSC: %s' % msgId)
            from toontown.pets import PetObserve
            PetObserve.send(self.zoneId,
                            PetObserve.getSCObserve(msgId, self.doId))
            # if the toon uses the pet message "Please don't bother me" pets can see when they are busy
            # positive messages towards the pet disable this
            if msgId in [21006]:
                self.setHatePets(1)
            elif msgId in [21000, 21001, 21003, 21004, 21200, 21201, 21202, 21203, 21204, 21205, 21206]:
                self.setHatePets(0)
            else:
                pass
                            
        def setSCCustom(self, msgId):
            DistributedToonAI.notify.debug('setSCCustom: %s' % msgId)
            from toontown.pets import PetObserve
            PetObserve.send(self.zoneId,
                            PetObserve.getSCObserve(msgId, self.doId))
                            
    def setHatePets(self, hate):
        self.hatePets = hate

    def takeOutKart(self,zoneId=None):
        if not self.kart:
            from toontown.racing import DistributedVehicleAI
            self.kart = DistributedVehicleAI.DistributedVehicleAI(self.air, self.doId)
            if(zoneId):
                self.kart.generateWithRequired(zoneId)
            else:
                self.kart.generateWithRequired(self.zoneId)                
            self.kart.start()
            #self.addDistObj(self.kart)
            #self.kart.request("Controlled", self.doId)
            
    #################################################################
    #  Cog Summoning Methods
    #################################################################
    def reqCogSummons(self, type, suitIndex):
        # RAU moved hasCogSummon and welcome valley checks before doing
        # the summons, otherwise invasion would still happen
        # even if he didn't have an invasion summon

        if type not in ('single', 'building', 'invasion', ):
            self.air.writeServerEvent('suspicious', self.doId, 'invalid cog summons type: %s' % type)
            self.sendUpdate('cogSummonsResponse',  ['fail', suitIndex, 0])
            return

        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.air.writeServerEvent('suspicious', self.doId, 'invalid suitIndex: %s' % suitIndex)
            self.sendUpdate('cogSummonsResponse',  ['fail', suitIndex, 0])
            return
        
        # verify that this is a legitimate summons
        if not self.hasCogSummons(suitIndex, type):
            self.air.writeServerEvent('suspicious', self.doId, 'bogus cog summons')
            self.sendUpdate('cogSummonsResponse',  ['fail', suitIndex, 0])
            return
            
        # make sure we are not on a welcome valley
        if ZoneUtil.isWelcomeValley(self.zoneId):
            self.sendUpdate('cogSummonsResponse', ['fail', suitIndex, 0])
            return
        
        returnCode = None
        if type == 'single':
            returnCode = self.doSummonSingleCog(suitIndex)
        elif type == 'building':
            returnCode = self.doBuildingTakeover(suitIndex)
        elif type == 'invasion':
            returnCode = self.doCogInvasion(suitIndex)

        
        if returnCode:
            # make sure to 'use' the toon's charge
            if returnCode[0] == "success":
                self.air.writeServerEvent('cogSummoned', self.doId, "%s|%s|%s" % (
                    type, suitIndex, self.zoneId))
                self.removeCogSummonsEarned(suitIndex, type)
                
            self.sendUpdate('cogSummonsResponse', returnCode)

    def doSummonSingleCog(self, suitIndex):

        # some debugging to address AI crashes
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning("Bad suit index: %s" % (suitIndex))
            return ['badIndex', suitIndex, 0]
        
        suitName = SuitDNA.suitHeadTypes[suitIndex]

        # get street points and the street's suitplanner
        streetId = ZoneUtil.getBranchZone(self.zoneId)
        if not self.air.suitPlanners.has_key(streetId):
            return ["badlocation", suitIndex, 0]

        sp = self.air.suitPlanners[streetId]
        map = sp.getZoneIdToPointMap()

        # check nearby zones as well
        zones = [self.zoneId, self.zoneId-1, self.zoneId+1]
        
        # are there any points in this zone?
        for zoneId in zones:
            if map.has_key(zoneId):
                points = map[zoneId][:]

                # create the suit
                suit = sp.createNewSuit([], points,
                                        suitName = suitName)
                if suit:
                    return ['success', suitIndex, 0]

        return ['badlocation', suitIndex, 0]
        
        
    def doBuildingTakeover(self, suitIndex):
        streetId = ZoneUtil.getBranchZone(self.zoneId)
        if not self.air.suitPlanners.has_key(streetId):
            self.notify.warning("Street %d is not known." % (streetId))
            return ["badlocation", suitIndex, 0]

        sp = self.air.suitPlanners[streetId]
        bm = sp.buildingMgr

        # try to figure out which door we're standing near
        building = self.findClosestDoor()

        if building == None:
            return ["badlocation", suitIndex, 0]
        
        level = None

        # some debugging to address AI crashes
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning("Bad suit index: %s" % (suitIndex))
            return ['badIndex', suitIndex, 0]

        # determine the track and level to use
        suitName = SuitDNA.suitHeadTypes[suitIndex]
        track = SuitDNA.getSuitDept(suitName)
        type = SuitDNA.getSuitType(suitName)

        # take over the building immediately.
        level, type, track = \
               sp.pickLevelTypeAndTrack(None, type, track)
        building.suitTakeOver(track, level, None)

        self.notify.warning("cogTakeOver %s %s %d %d" % 
                            (track, level, building.block, self.zoneId))

        return ["success", suitIndex, building.doId]
        
    def doCogInvasion(self, suitIndex):
        invMgr = self.air.suitInvasionManager

        if invMgr.getInvading():
            returnCode = 'busy'
        else:
            # some debugging to address AI crashes
            if suitIndex >= len(SuitDNA.suitHeadTypes):
                self.notify.warning("Bad suit index: %s" % (suitIndex))
                return ['badIndex', suitIndex, 0]

            cogType = SuitDNA.suitHeadTypes[suitIndex]
            numCogs = 1000
            if invMgr.startInvasion(cogType, numCogs, False):
                returnCode = 'success'
            else:
                returnCode = 'fail'

        return [returnCode, suitIndex, 0]

    # Control the list of earned cog summons
    def b_setCogSummonsEarned(self, cogSummonsEarned):
        self.d_setCogSummonsEarned(cogSummonsEarned)
        self.setCogSummonsEarned(cogSummonsEarned)

    def d_setCogSummonsEarned(self, cogSummonsEarned):
        self.sendUpdate('setCogSummonsEarned', [cogSummonsEarned])

    def setCogSummonsEarned(self, cogSummonsEarned):
        self.cogSummonsEarned = cogSummonsEarned

    def getCogSummonsEarned(self):
        return self.cogSummonsEarned

    def addCogSummonsEarned(self, suitIndex, type):
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]
        
        if type == "single":
            curSetting |= 0x01
        elif type == "building":
            curSetting |= 0x02
        elif type == "invasion":
            curSetting |= 0x04

        summons[suitIndex] = curSetting
        self.b_setCogSummonsEarned(summons)

    def removeCogSummonsEarned(self, suitIndex, type):
        # Removes the indicated cog summons from the Toon's
        # inventory.  Returns true if it was there in the first place,
        # false if it was not.
        
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]

        if self.hasCogSummons(suitIndex, type):
            if type == "single":
                curSetting &= ~0x01
            elif type == "building":
                curSetting &= ~0x02
            elif type == "invasion":
                curSetting &= ~0x04

            summons[suitIndex] = curSetting
            self.b_setCogSummonsEarned(summons)

        self.notify.warning("Toon %s doesn't have a %s summons for %s" % (self.doId, type, suitIndex))
        return False

    def hasCogSummons(self, suitIndex, type = None):
        summons = self.getCogSummonsEarned()
        curSetting = summons[suitIndex]

        if type == "single":
            return curSetting & 0x01
        elif type == "building":
            return curSetting & 0x02
        elif type == "invasion":
            return curSetting & 0x04

        # just check to see if the toon has *any* for this suit
        return curSetting

    def hasParticularCogSummons(self, deptIndex, level, type ):
        """
        checks if this toon has this particular summon already
        deptIndex should be from 0-3
        level should be from 0-7
        type can be 'single','building','invasion'
        """
        if not deptIndex in range(len(SuitDNA.suitDepts)):
            self.notify.warning('invalid parameter deptIndex %s' % deptIndex)
            return False

        if not level in range(SuitDNA.suitsPerDept):
            self.notify.warning('invalid parameter level %s' % level)
            return False

        suitIndex = deptIndex * SuitDNA.suitsPerDept + level
        retval = self.hasCogSummons( suitIndex, type)
        return retval
        
        
    def assignNewCogSummons(self, level = None, summonType = None, deptIndex = None):
        if level != None:
            if deptIndex in range(len(SuitDNA.suitDepts)):
                #set level and set dept
                dept = deptIndex
            else:
                #set level and random dept
                numDepts = len(SuitDNA.suitDepts)
                dept = random.randrange(0, numDepts)
                
            suitIndex = dept * SuitDNA.suitsPerDept + level
        else:
            if deptIndex in range(len(SuitDNA.suitDepts)):
                #random level and set dept
                randomLevel = random.randrange(0, SuitDNA.suitsPerDept)
                suitIndex = deptIndex * SuitDNA.suitsPerLevel + randomLevel
            else:
                #random level and random dept
                numSuits = len(SuitDNA.suitHeadTypes)
                suitIndex = random.randrange(0, numSuits)

        if summonType in ['single','building','invasion']:
            type = summonType        
        else:
            typeWeights = ['single']   * 70 + \
                          ['building'] * 25 + \
                          ['invasion'] * 5
            type = random.choice(typeWeights)                

        # some debugging to address AI crashes
        if suitIndex >= len(SuitDNA.suitHeadTypes):
            self.notify.warning("Bad suit index: %s" % (suitIndex))

        self.addCogSummonsEarned(suitIndex, type)
        return (suitIndex, type)
        
    def findClosestDoor(self):
        zoneId = self.zoneId
        streetId = ZoneUtil.getBranchZone(zoneId)
        sp = self.air.suitPlanners[streetId]
        if not sp:
            return None
        
        bm = sp.buildingMgr
        if not bm:
            return None
        
        zones = [zoneId, zoneId-1, zoneId+1, zoneId-2, zoneId+2]
        # loop through the valid zones... this ordering means we will
        # find the building closest to the toon
        for zone in zones:
            for i in bm.getToonBlocks():
                building = bm.getBuilding(i)
                extZoneId, intZoneId = building.getExteriorAndInteriorZoneId()
                # make sure this isn't a quest building
                if not NPCToons.isZoneProtected(intZoneId):
                    if hasattr(building, "door"):
                        if building.door.zoneId == zone:
                            return building
        return None


    #////////////////// Gardening Estates Expansion

    ### garden trophy list ###

    def b_setGardenTrophies(self, trophyList):
        # update the caught fish list
        self.setGardenTrophies(trophyList)
        self.d_setGardenTrophies(trophyList)

    def setGardenTrophies(self, trophyList):
        self.notify.debug("setting gardenTrophies to %s" % trophyList)
        self.gardenTrophies = trophyList
        
    def d_setGardenTrophies(self, trophyList):
        self.sendUpdate("setGardenTrophies", [trophyList])

    def getGardenTrophies(self):
        return self.gardenTrophies

    # garden specials

    def setGardenSpecials(self, specials):
        for special in specials:
            if special[1] > 255:
                special[1] = 255
        self.gardenSpecials = specials
        
    def getGardenSpecials(self):
        return self.gardenSpecials
        
    def d_setGardenSpecials(self, specials):
        self.sendUpdate('setGardenSpecials', [specials])
        
    def b_setGardenSpecials(self, specials):
        for special in specials:
            if special[1] > 255:
                newCount = 255
                index = special[0]
                self.gardenSpecials.remove(special)
                self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()
        self.setGardenSpecials(specials)
        self.d_setGardenSpecials(specials)
        
    def addGardenItem(self, index, count):
        for item in self.gardenSpecials:
            if item[0] == index:
                newCount = item[1] + count
                self.gardenSpecials.remove(item)
                self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()
                self.b_setGardenSpecials(self.gardenSpecials)
                return
        self.gardenSpecials.append((index, count))
        self.gardenSpecials.sort()
        self.b_setGardenSpecials(self.gardenSpecials)

    def removeGardenItem(self, index, count):
        for item in self.gardenSpecials:
            if item[0] == index:
                newCount = item[1] - count
                self.gardenSpecials.remove(item)
                if newCount > 0:
                    self.gardenSpecials.append((index, newCount))
                self.gardenSpecials.sort()
                self.b_setGardenSpecials(self.gardenSpecials)
                return
        self.notify.warning("removing garden item %d that toon doesn't have" %
                            index)

    # Flower collection            

    def b_setFlowerCollection(self, speciesList, varietyList):
        # update the collected flower list
        self.setFlowerCollection( speciesList, varietyList)
        self.d_setFlowerCollection( speciesList, varietyList)
        
    def d_setFlowerCollection(self, speciesList, varietyList):
        self.sendUpdate("setFlowerCollection", [speciesList, varietyList])

    def setFlowerCollection(self, speciesList, varietyList):
        self.flowerCollection = FlowerCollection.FlowerCollection()
        self.flowerCollection.makeFromNetLists( speciesList, varietyList)

    def getFlowerCollection(self):
        return self.flowerCollection.getNetLists()

    ## Max flower basket
    
    def b_setMaxFlowerBasket(self, maxFlowerBasket):
        self.d_setMaxFlowerBasket(maxFlowerBasket)
        self.setMaxFlowerBasket(maxFlowerBasket)

    def d_setMaxFlowerBasket(self, maxFlowerBasket):
        self.sendUpdate("setMaxFlowerBasket", [maxFlowerBasket])

    def setMaxFlowerBasket(self, maxFlowerBasket):
        self.maxFlowerBasket = maxFlowerBasket

    def getMaxFlowerBasket(self):
        return self.maxFlowerBasket


    ## Flower Basket
    
    def b_setFlowerBasket(self, speciesList, varietyList):
        # update the picked flower list
        self.setFlowerBasket( speciesList, varietyList)
        self.d_setFlowerBasket( speciesList, varietyList)
        
    def d_setFlowerBasket(self, speciesList, varietyList):
        self.sendUpdate("setFlowerBasket", [speciesList, varietyList])

    def setFlowerBasket(self, speciesList, varietyList):
        self.flowerBasket = FlowerBasket.FlowerBasket()
        self.flowerBasket.makeFromNetLists(speciesList, varietyList)

    def getFlowerBasket(self):
        return self.flowerBasket.getNetLists()

    def makeRandomFlowerBasket(self):
        self.flowerBasket.generateRandomBasket()
        self.d_setFlowerBasket(*self.flowerBasket.getNetLists())
        
    def addFlowerToBasket(self, species, variety):
        # First check our max limit
        numFlower = len(self.flowerBasket)
        if numFlower >= self.maxFlowerBasket:
            self.notify.warning("addFlowerToBasket: cannot add flower, basket is full")
            return 0
        else:
            # Perhaps this can fail for some reason
            if self.flowerBasket.addFlower(species, variety):
                self.d_setFlowerBasket(*self.flowerBasket.getNetLists())
                return 1
            else:
                self.notify.warning("addFlowerToBasket: addFlower failed")
                return 0

    def removeFlowerFromBasketAtIndex(self, index):
        # Try to remove this flower from the basket
        if self.flowerBasket.removeFlowerAtIndex(index):
            self.d_setFlowerBasket(*self.flowerBasket.getNetLists())
            return 1
        else:
            self.notify.warning("removeFishFromTank: cannot find fish")
            return 0

    ## Shovel

    def b_setShovel(self, shovelId):
        self.d_setShovel(shovelId)
        self.setShovel(shovelId)

    def d_setShovel(self, shovelId):
        self.sendUpdate("setShovel", [shovelId])

    def setShovel(self, shovelId):
        self.shovel = shovelId

    def getShovel(self):
        return self.shovel


    ## ShovelSkill

    def b_setShovelSkill(self, skillLevel):
        self.sendGardenEvent()
        if skillLevel >= GardenGlobals.ShovelAttributes[self.shovel]['skillPts']:
            #make sure we dont go past gold shovel
            if self.shovel < GardenGlobals.MAX_SHOVELS - 1:
                self.b_setShovel(self.shovel+1)
                self.setShovelSkill(0)
                self.d_setShovelSkill(0)
                self.sendUpdate("promoteShovel", [self.shovel])

                #log that he got a better shovel
                self.air.writeServerEvent("garden_new_shovel", self.doId, '%d' % self.shovel)
        else:
            self.setShovelSkill(skillLevel)
            self.d_setShovelSkill(skillLevel)

    def d_setShovelSkill(self, skillLevel):
        self.sendUpdate("setShovelSkill", [skillLevel])

    def setShovelSkill(self, skillLevel):
        self.shovelSkill = skillLevel

    def getShovelSkill(self):
        return self.shovelSkill

    ## WateringCan

    def b_setWateringCan(self, wateringCanId):
        self.d_setWateringCan(wateringCanId)
        self.setWateringCan(wateringCanId)

    def d_setWateringCan(self, wateringCanId):
        self.sendUpdate("setWateringCan", [wateringCanId])

    def setWateringCan(self, wateringCanId):
        self.wateringCan = wateringCanId

    def getWateringCan(self):
        return self.wateringCan

    """
    def waterPlant(self, plantId):
        plant = self.air.doId2do.get(plantId)
        if plant:
            waterPower = GardenGlobals.getWateringCanPower(self.wateringCan, self.wateringCanSkill)
            skillUp = plant.waterPlant(waterPower)
            if skillUp:
                self.b_setWateringCanSkill(self.wateringCanSkill+1)
    """

    ## WateringCanSkill

    def b_setWateringCanSkill(self, skillLevel):    
        self.sendGardenEvent()
        if skillLevel >= GardenGlobals.WateringCanAttributes[self.wateringCan]['skillPts']:
           if self.wateringCan < GardenGlobals.MAX_WATERING_CANS -1:
               #make sure we don't go past the max watering can
               self.b_setWateringCan(self.wateringCan+1)
               self.setWateringCanSkill(0)
               self.d_setWateringCanSkill(0)
               self.sendUpdate("promoteWateringCan", [self.wateringCan])

               #log that he got a better watering can
               self.air.writeServerEvent("garden_new_wateringCan", self.doId, '%d' % self.wateringCan)
               
           else:
               #we are at the maximum watering can, ensure skillLevel does not spill over
               skillLevel =  GardenGlobals.WateringCanAttributes[self.wateringCan]['skillPts'] - 1
               self.setWateringCanSkill(skillLevel)
               self.d_setWateringCanSkill(skillLevel)
        else:
            self.setWateringCanSkill(skillLevel)
            self.d_setWateringCanSkill(skillLevel)
        

    def d_setWateringCanSkill(self, skillLevel):
        self.sendUpdate("setWateringCanSkill", [skillLevel])

    def setWateringCanSkill(self, skillLevel):
        self.wateringCanSkill = skillLevel

    def getWateringCanSkill(self):
        return self.wateringCanSkill

    ## TrackBonusLevel

    def b_setTrackBonusLevel(self, trackBonusLevelArray):
        self.setTrackBonusLevel(trackBonusLevelArray)
        self.d_setTrackBonusLevel(trackBonusLevelArray)

    def d_setTrackBonusLevel(self, trackBonusLevelArray):
        self.sendUpdate("setTrackBonusLevel", [trackBonusLevelArray])

    def setTrackBonusLevel(self, trackBonusLevelArray):
        self.trackBonusLevel = trackBonusLevelArray

    def getTrackBonusLevel(self, track=None):
        if track == None:
            return self.trackBonusLevel
        else:
            return self.trackBonusLevel[track]

    def checkGagBonus(self, track, level):
        trackBonus = self.getTrackBonusLevel(track)
        return (trackBonus >= level)

    def giveMeSpecials(self, id = None):
        print("Specials Go!!")
        self.b_setGardenSpecials([(0,3),(1,2),(2,3),(3,2),(4,3),(5,2),(6,3),(7,2),(100,1),(101,3),(102,1)])


    def reqUseSpecial(self, special):
        response = self.tryToUseSpecial(special)
        self.sendUpdate('useSpecialResponse',[response])

    def tryToUseSpecial(self, special) :
        estateOwnerDoId = simbase.air.estateMgr.zone2owner.get(self.zoneId)

        response = 'badlocation'
        doIHaveThisSpecial = False
        for curSpecial in self.gardenSpecials:
            if curSpecial[0] == special and curSpecial[1] > 0:
                doIHaveThisSpecial = True
                break

        if not doIHaveThisSpecial:
            #hmmm how did this happen, trying to plant a special we don't have
            return response
                

        if not self.doId == estateOwnerDoId:
            self.notify.warning("how did this happen, planting an item you don't own")
            return response
        
        if estateOwnerDoId:
            estate = simbase.air.estateMgr.estate.get(estateOwnerDoId)
            if estate and hasattr(estate,'avIdList'):
                #we should have a valid DistributedEstateAI at this point                
                ownerIndex = estate.avIdList.index(estateOwnerDoId)
                if ownerIndex >= 0:
                    estate.doEpochNow(onlyForThisToonIndex = ownerIndex)
                    self.removeGardenItem(special, 1)
                    response = 'success'

                    #log that they used the fertilizer
                    self.air.writeServerEvent("garden_fertilizer", self.doId, '')

        return response
        
    def sendGardenEvent(self):
        if hasattr(self, "estateZones") and hasattr(self, "doId"):
            if simbase.wantPets and self.hatePets:
                # announce to the pets that we're busy
                PetObserve.send(self.estateZones, PetObserve.PetActionObserve(
                        PetObserve.Actions.GARDEN, self.doId))

    def setGardenStarted(self, bStarted):
        self.gardenStarted = bStarted
    def d_setGardenStarted(self, bStarted):
        self.sendUpdate("setGardenStarted", [bStarted])
    def b_setGardenStarted(self, bStarted):
        self.setGardenStarted(bStarted)
        self.d_setGardenStarted(bStarted)
    def getGardenStarted(self):
        return self.gardenStarted

    # log suspicious toon behaviors
    def logSuspiciousEvent(self, eventName):
        self.air.writeServerEvent('suspicious', self.doId, eventName)


    ### golf trophy list ###
    def getGolfTrophies(self):
        """Get the golf trophies this toon has won."""
        return self.golfTrophies

    def getGolfCups(self):
        """Get the golf cups this toon has won. 10 trophies awards you 1 cup."""
        return self.golfCups

    ### golf history list ###

    def b_setGolfHistory(self, history):
        """Set the golf history on the ai and client."""
        # update the trophies won list
        self.setGolfHistory(history)
        self.d_setGolfHistory(history)

    def d_setGolfHistory(self, history):
        """Send the golf history to the client."""
        self.sendUpdate('setGolfHistory',[history])

    def setGolfHistory(self, history):
        """Set the golf history on the ai."""
        self.notify.debug("setting golfHistory to %s" % history)
        self.golfHistory = history

        #update our trophies and cups too
        self.golfTrophies =  GolfGlobals.calcTrophyListFromHistory(self.golfHistory)
        self.golfCups = GolfGlobals.calcCupListFromHistory(self.golfHistory)

    def getGolfHistory(self):
        """Return the golf history."""
        return self.golfHistory

    def b_setGolfHoleBest(self, holeBest):
        """Set the personal hole best on the ai and client."""
        self.setGolfHoleBest(holeBest)
        self.d_setGolfHoleBest(holeBest)

    def d_setGolfHoleBest(self, holeBest):
        """Send the personal hole best to client."""
        packed = GolfGlobals.packGolfHoleBest(holeBest)        
        self.sendUpdate('setPackedGolfHoleBest', [packed])

    def setGolfHoleBest(self, holeBest):
        """Set the personal hole best on the ai."""
        self.golfHoleBest = holeBest

    def getGolfHoleBest(self):
        """Return the personal hole best."""
        return self.golfHoleBest

    def getPackedGolfHoleBest(self):
        """Return the packed personal hole best."""
        packed = GolfGlobals.packGolfHoleBest(self.golfHoleBest)
        return packed

    def setPackedGolfHoleBest(self, packedHoleBest):
        """Set the packed personal hole best on the client."""
        unpacked = GolfGlobals.unpackGolfHoleBest(packedHoleBest)
        self.setGolfHoleBest(unpacked)    


    def b_setGolfCourseBest(self, courseBest):
        """Set the personal course best on the ai and client."""
        self.setGolfCourseBest(courseBest)
        self.d_setGolfCourseBest(courseBest)

    def d_setGolfCourseBest(self, courseBest):
        """Send the personal course best to client."""
        self.sendUpdate('setGolfCourseBest', [courseBest])

    def setGolfCourseBest(self, courseBest):
        """Set the personal course best on the ai."""
        self.golfCourseBest = courseBest

    def getGolfCourseBest(self):
        """Return the personal course best."""
        return self.golfCourseBest    
                                       
    def setUnlimitedSwing(self, unlimitedSwing):
        """Set if we can swing an unlimited number of times in golf."""
        self.unlimitedSwing = unlimitedSwing

    def getUnlimitedSwing(self):
        """Returns true if we can swing an unlimited number of times in golf."""
        return self.unlimitedSwing

    def b_setUnlimitedSwing(self, unlimitedSwing):
        """Set the unlimitedSwing on the ai and client."""
        self.setUnlimitedSwing(unlimitedSwing)
        self.d_setUnlimitedSwing(unlimitedSwing)

    def d_setUnlimitedSwing(self, unlimitedSwing):
        """Send the personal course best to client."""
        self.sendUpdate('setUnlimitedSwing', [unlimitedSwing])

    # Control the pink slips
    def b_setPinkSlips(self, pinkSlips):
        self.d_setPinkSlips(pinkSlips)
        self.setPinkSlips(pinkSlips)

    def d_setPinkSlips(self, pinkSlips):
        self.sendUpdate('setPinkSlips', [pinkSlips])

    def setPinkSlips(self, pinkSlips):
        self.pinkSlips = pinkSlips

    def getPinkSlips(self):
        return self.pinkSlips

    def addPinkSlips(self, amountToAdd):
        pinkSlips = min( self.pinkSlips + amountToAdd, 0xff)
        self.b_setPinkSlips(pinkSlips)
        
    def setPreviousAccess(self, access):
        #stub function for dc compatibility with DistributedPlayerAI
        #used to keep track of access if it changes while play is in session
        self.previousAccess = access
        
    def b_setAccess(self, access):
        self.setAccess(access)
        self.d_setAccess(access)
       
    def d_setAccess(self, access):
        self.sendUpdate("setAccess", [access])

        
    def setAccess(self, access):
        print("Setting Access %s" % (access))
        if access == OTPGlobals.AccessInvalid:
            if not __dev__:
                self.air.writeServerEvent("Setting Access", self.doId, "setAccess not being sent by the OTP Server, changing access to unpaid")
                access = OTPGlobals.AccessVelvetRope
            elif __dev__:
                access = OTPGlobals.AccessFull    
        self.setGameAccess(access)
        
        
    def setGameAccess(self, access):
        self.gameAccess = access
        
    def getGameAccess(self):
        return self.gameAccess
        
   # Name Tag Styles
   
    def b_setNametagStyle(self, nametagStyle):
        self.d_setNametagStyle(nametagStyle)
        self.setNametagStyle(nametagStyle)

    def d_setNametagStyle(self, nametagStyle):
        self.sendUpdate('setNametagStyle', [nametagStyle])

    def setNametagStyle(self, nametagStyle):
        self.nametagStyle = nametagStyle

    def getNametagStyle(self):
        return self.nametagStyle
        
    def logMessage(self, message):
        avId = self.air.getAvatarIdFromSender()
        if __dev__:
            print ("CLIENT LOG MESSAGE %s %s" % (avId, message))
        try:
            self.air.writeServerEvent('clientLog', avId, message)
            
        except:
            self.air.writeServerEvent('suspicious', avId, "client sent us a clientLog that caused an exception")

    def b_setMail(self, mail):
        self.d_setMail(mail)
        self.setMail(mail)

    def d_setMail(self, mail):
        self.sendUpdate('setMail', [mail])

    def setMail(self, mail):
        self.mail = mail

    def setNumMailItems(self, numMailItems):
        self.numMailItems = numMailItems

    def setSimpleMailNotify(self, simpleMailNotify):
        """Handle the uberdog telling us if we have new, old, or no simple mail."""
        self.simpleMailNotify = simpleMailNotify

    def setInviteMailNotify(self, inviteMailNotify):
        """Handle the uberdog telling us if we have new, old, or no invite mail."""
        self.inviteMailNotify = inviteMailNotify
 
    def setInvites( self, invites):
        """Handle uberdog telling us our invitations.
        This does not include invites we've already rejected."""
        self.invites = []
        for i in xrange(len(invites)):
            oneInvite=invites[i]
            newInvite = InviteInfoBase(*oneInvite)
            self.invites.append(newInvite)
            assert self.notify.debug('self.invites[%d]= %s' % (i, newInvite))

    def updateInviteMailNotify(self):
        """Calculate the value for inviteMailNotify, new invite, old invite or no invites"""
        invitesInMailbox = self.getInvitesToShowInMailbox()
        newInvites = 0
        readButNotRepliedInvites = 0
        for invite in invitesInMailbox:
            if invite.status == PartyGlobals.InviteStatus.NotRead:
                newInvites += 1
            elif invite.status == PartyGlobals.InviteStatus.ReadButNotReplied:
                readButNotRepliedInvites += 1
            # we're guaranted that we have the associated partyInfo, but just in case
            if __dev__ :
                partyInfo = self.getOnePartyInvitedTo(invite.partyId)
                if not partyInfo:
                    self.notify.error("party info not found in partiesInvtedTo, partyId = %s" %
                                      str(invite.partyId))
        if newInvites:
            self.setInviteMailNotify(ToontownGlobals.NewItems)
        elif readButNotRepliedInvites:
            self.setInviteMailNotify(ToontownGlobals.OldItems)
        else:
            self.setInviteMailNotify(ToontownGlobals.NoItems)            

    def getNumNonResponseInvites(self):
        """
        Returns the number of invites that have not yet been responded to.
        """
        count = 0
        for i in xrange(len(self.invites)):
            if (self.invites[i].status == InviteStatus.NotRead) or (self.invites[i].status == InviteStatus.ReadButNotReplied):
                count += 1
        return count

    def getInvitesToShowInMailbox(self):
        """Return a list of inviteInfos that should be displayed in the mailbox."""
        # WARNING keep this in sync with DistributedToon.getInvitesToShowInMailbox        
        result = []
        for invite in self.invites:
            appendInvite = True
            if invite.status == InviteStatus.Accepted or \
               invite.status == InviteStatus.Rejected:
                assert( self.notify.debug('Not showing accepted/rejected invite  %s' % invite) )
                appendInvite = False
                
            if appendInvite:
                # some invites are so far in the future we don't have the party info
                partyInfo = self.getOnePartyInvitedTo(invite.partyId)
                if not partyInfo:
                    assert( self.notify.debug('Not showing invite because no party ') )
                    appendInvite = False
                # do not show invitations for cancelled parties
                if appendInvite:
                    if partyInfo.status == PartyGlobals.PartyStatus.Cancelled:
                        assert( self.notify.debug('Not showing invite party is cancelled') )
                        appendInvite = False

                # do not show mailbox invitations for parties that have finished yesterday
                if appendInvite:
                    # server time and client time may be slightly off, and toon can get mailbox stuck when
                    # they dont return the same value, using yesterday it's still possible but only
                    # at around midnight, which minimizes the possibilty
                    # we use end time because a party could be started 1 minute before it's supposed to end
                    endDate= partyInfo.endTime.date()
                    curDate = simbase.air.toontownTimeManager.getCurServerDateTime().date()
                    if endDate < curDate:
                        appendInvite = False
            if appendInvite:
                result.append(invite)
        return result

    def getNumInvitesToShowInMailbox(self):
        """Return how many invites we'll show in the mailbox."""
        result = len(self.getInvitesToShowInMailbox())
        return result

    def setHostedParties( self, hostedParties):
        """Handle uberdog telling us our hosted parties."""
        self.hostedParties = []
        for i in xrange(len(hostedParties)):
            hostedInfo = hostedParties[i]
            newParty = PartyInfoAI(*hostedInfo)
            self.hostedParties.append(newParty)
            assert self.notify.debug('self.hostedParties[%d]= %s' % (i,newParty))

    def setPartiesInvitedTo( self, partiesInvitedTo):
        """Handle uberdog telling us details of parties we are invited to."""
        self.partiesInvitedTo = []
        for i in xrange(len(partiesInvitedTo)):
            partyInfo = partiesInvitedTo[i]
            newParty = PartyInfoAI(*partyInfo)
            self.partiesInvitedTo.append(newParty)
            assert self.notify.debug('self.partiesInvitedTo[%d]= %s' % (i,newParty))
        self.updateInviteMailNotify()
        self.checkMailboxFullIndicator()

    def getOnePartyInvitedTo(self, partyId):
        """Return the partyInfo if partyId is in partiesInvitedTo, return None otherwise."""
        # It is possible to get an invite to a party so far in the future that it gets filtered out
        # hence returning None is a valid result
        result = None
        for i in xrange(len(self.partiesInvitedTo)):
            partyInfo = self.partiesInvitedTo[i]
            if partyInfo.partyId == partyId:
                result = partyInfo
                break
        return result
        
    def setPartyReplyInfoBases(self, replies):
        """Handle uberdog telling us replies to our hosted parties."""
        self.partyReplyInfoBases = []
        for i in xrange(len(replies)):
            partyReply = replies[i]
            repliesForOneParty = PartyReplyInfoBase(*partyReply)
            self.partyReplyInfoBases.append(repliesForOneParty)
            assert self.notify.debug('self.setPartyReplyInfoBases[%d]= %s' % (i,repliesForOneParty))

    def updateInvite(self, inviteKey, newStatus):
        """We've gotten confirmation from the uberdog to reject/accept the invite."""
        for invite in self.invites:
            if invite.inviteKey == inviteKey:
                invite.status = newStatus
                self.updateInviteMailNotify()
                self.checkMailboxFullIndicator()
                break
        

    def updateReply(self, partyId, inviteeId, newStatus):
        """Someone accepted our invite while we were online."""
        for partyReply in self.partyReplyInfoBases:
            if partyReply.partyId == partyId:
                for reply in partyReply.replies:
                    if reply.inviteeId == inviteeId:
                        reply.inviteeId = newStatus
                        break
                        
    def canPlanParty(self):
        """Return true if the toon can plan a party."""
        nonCancelledPartiesInTheFuture = 0
        for partyInfo in self.hostedParties:
            if partyInfo.status != PartyGlobals.PartyStatus.Cancelled and partyInfo.status != PartyGlobals.PartyStatus.Finished:
                nonCancelledPartiesInTheFuture += 1
                if nonCancelledPartiesInTheFuture >= PartyGlobals.MaxHostedPartiesPerToon:
                    break
        result = nonCancelledPartiesInTheFuture < PartyGlobals.MaxHostedPartiesPerToon
        return result
                

    def setPartyCanStart(self, partyId):
        """Handle uberdog telling us we can start a party that we're hosting."""
        self.notify.debug("setPartyCanStart called passing in partyId=%s" % partyId)
        found = False
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = PartyGlobals.PartyStatus.CanStart
                found = True
                break
        if not found:
            self.notify.warning("setPartyCanStart can't find partyId %s" % partyId)
                
    def setPartyStatus(self, partyId, newStatus):
        """Handle uberdog telling us status of a party has changed."""
        self.notify.debug("setPartyStatus  called passing in partyId=%s newStauts=%d" % (partyId,newStatus))
        found = False
        
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = newStatus
                found = True
                break

        info = self.getOnePartyInvitedTo(partyId)
        if info:
            found = True
            info.status = newStatus    
        if not found:
            self.notify.warning("setPartyCanStart can't find hosted or invitedTO partyId %s" % partyId)


    def b_setAwardMailboxContents(self, awardMailboxContents):
        """Set ai's mailbox contents, and update client."""
        self.setAwardMailboxContents(awardMailboxContents )
        self.d_setAwardMailboxContents(awardMailboxContents )

    def d_setAwardMailboxContents(self, awardMailboxContents):
        """Update the client on the new award mailbox contents."""
        self.sendUpdate("setAwardMailboxContents", [awardMailboxContents.getBlob(store = CatalogItem.Customization)])
        # AWARD_TODO figure out how i can set this properly with mailboxContents
        #if len(mailboxContents ) == 0:
        #    self.b_setCatalogNotify(self.catalogNotify, ToontownGlobals.NoItems)

    def setAwardMailboxContents(self, awardMailboxContents):
        """Set AI's mailbox contents."""
        self.notify.debug("Setting awardMailboxContents to %s." % (awardMailboxContents))
        self.awardMailboxContents = CatalogItemList.CatalogItemList(awardMailboxContents, store = CatalogItem.Customization )
        self.notify.debug("awardMailboxContents is %s." % (self.awardMailboxContents))
        if len(awardMailboxContents) == 0:
            self.b_setAwardNotify(ToontownGlobals.NoItems)
        self.checkMailboxFullIndicator()

    def getAwardMailboxContents(self):
        """Return our current award mailbox contents."""
        return self.awardMailboxContents.getBlob(store = CatalogItem.Customization  )


    def b_setAwardSchedule(self, onOrder, doUpdateLater = True):
        """Set AI's award schedule, and update the client."""
        self.setAwardSchedule(onOrder, doUpdateLater)
        self.d_setAwardSchedule(onOrder)

    def d_setAwardSchedule(self, onOrder):
        """Update the client on the new award schedule."""
        self.sendUpdate("setAwardSchedule", [onOrder.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)])

    def setAwardSchedule(self, onAwardOrder, doUpdateLater = True):
        """Set AI's award schedule."""        
        # awards don't have to deal with gifts and own purchased items, so using the original algorithm
        self.onAwardOrder = CatalogItemList.CatalogItemList(onAwardOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if hasattr(self, 'name'):
            if doUpdateLater and self.air.doLiveUpdates and hasattr(self, 'air'):
                # Schedule the next delivery.
                taskName = self.uniqueName('next-award-delivery')
                taskMgr.remove(taskName)
    
                #print("setting item schedule for %s" % (self.getName()))
                # Set a timeout to make the delivery later.  We insist on
                # waiting at least 10 seconds mainly to give the avatar enough
                # time to completely manifest on the stateserver before we
                # start sending messages to it.
                now = (int)(time.time() / 60 + 0.5)
                nextItem = None
                nextTime = self.onAwardOrder.getNextDeliveryDate()
                nextItem = self.onAwardOrder.getNextDeliveryItem()
                if nextItem != None:
                    pass
                    #print(">>current time:%s" % (now))
                    #print("next item time:%s item:%s" % (nextTime, nextItem.getName()))
                else:
                    pass
                    #print("No items for regular delivery")
                if nextTime != None:
                    duration = max(10.0, nextTime * 60 - time.time())
                    taskMgr.doMethodLater(duration, self.__deliverAwardPurchase, taskName)

    def __deliverAwardPurchase(self, task):
        """Move the award from onAwardOrder to mailboxContents."""
        # Move one  from the onAwardOrder list to the
        # awardMailboxContents.
        # Get the current time in minutes.
        now = (int)(time.time() / 60 + 0.5)

        # Extract out any items that should have been delivered by now.
        delivered, remaining = self.onAwardOrder.extractDeliveryItems(now)

        self.notify.info("Award Delivery for %s: %s." % (self.doId, delivered))

        self.b_setAwardMailboxContents(self.awardMailboxContents + delivered)
        self.b_setAwardSchedule(remaining)

        if delivered:
            self.b_setAwardNotify( ToontownGlobals.NewItems)

        return Task.done

    def b_setAwardNotify(self, awardMailboxNotify):
        """Set AI's award notify, and update the client."""
        self.setAwardNotify(awardMailboxNotify)
        self.d_setAwardNotify(awardMailboxNotify)

    def d_setAwardNotify(self, awardMailboxNotify):
        """update the client."""
        self.sendUpdate("setAwardNotify", [awardMailboxNotify])

    def setAwardNotify(self, awardNotify):
        """Set AI's award notify"""
        self.awardNotify = awardNotify

    def hasGMName(self):
        """ Returns True if this toon's name starts with '$', indicating they are special. """
        return self.getName().startswith('$')
