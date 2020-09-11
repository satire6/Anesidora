"""DistributedToon module: contains the DistributedToon class"""
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *

from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from otp.avatar import DistributedPlayer
from otp.avatar import Avatar, DistributedAvatar
from otp.speedchat import SCDecoders
from otp.chat import TalkAssistant
import Toon
import GMUtils
from direct.task.Task import Task
from direct.distributed import DistributedSmoothNode
from direct.distributed import DistributedObject
from direct.fsm import ClassicFSM
from toontown.hood import ZoneUtil
from toontown.distributed import DelayDelete
from toontown.distributed.DelayDeletable import DelayDeletable
from direct.showbase import PythonUtil
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
import TTEmote
from toontown.shtiker.OptionsPage import speedChatStyles
from toontown.fishing import FishCollection
from toontown.fishing import FishTank
from toontown.suit import SuitDNA
from toontown.coghq import CogDisguiseGlobals
from toontown.toonbase import TTLocalizer
import Experience
import InventoryNew
from toontown.speedchat import TTSCDecoders
from toontown.chat import ToonChatGarbler
from toontown.chat import ResistanceChat
from direct.distributed.MsgTypes import *
from toontown.effects.ScavengerHuntEffects import *
from toontown.estate import FlowerCollection
from toontown.estate import FlowerBasket
from toontown.estate import GardenGlobals
from toontown.estate import DistributedGagTree
from toontown.golf import GolfGlobals
from toontown.parties.PartyGlobals import InviteStatus, PartyStatus
from toontown.parties.PartyInfo import PartyInfo
from toontown.parties.InviteInfo import InviteInfo
from toontown.parties.PartyReplyInfo import PartyReplyInfoBase
from toontown.parties.SimpleMailBase import SimpleMailBase
from toontown.parties import PartyGlobals
from toontown.friends import FriendHandle
import time
import operator

from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, SoundInterval
from toontown.distributed import DelayDelete
from otp.otpbase import OTPLocalizer
import random
import copy



if base.wantKarts:
    from toontown.racing.KartDNA import *

if( __debug__ ):
    import pdb

class DistributedToon(DistributedPlayer.DistributedPlayer,
                      Toon.Toon, DistributedSmoothNode.DistributedSmoothNode, DelayDeletable):
    """DistributedToon class:"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToon")
    partyNotify = DirectNotifyGlobal.directNotify.newCategory("DistributedToon_Party")

    # This can be a class variable because all Toons can share it
    # without problems
    chatGarbler = ToonChatGarbler.ToonChatGarbler()

    #Support for GM avatars
    gmNameTag = None

    def __init__(self, cr, bFake = False):
        try:
            self.DistributedToon_initialized
            return
        except:
            self.DistributedToon_initialized = 1
        
        DistributedPlayer.DistributedPlayer.__init__(self, cr)
        Toon.Toon.__init__(self)
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)


        self.bFake = bFake

        self.kart=None
        
        # Our trophy score will be set by the AI.
        self.trophyScore = 0
        self.trophyStar = None
        self.trophyStarSpeed = 0
        
        # check for teleport cheat
        self.safeZonesVisited = []

        self.NPCFriendsDict = {}

        self.earnedExperience = None
        self.track = None
        self.effect = None
        self.maxCarry = 0
        self.disguisePageFlag = 0

        # These are initialized to None here, but for a LocalToon with
        # the pages created, they will be filled in.
        self.disguisePage = None
        self.sosPage = None
        self.gardenPage = None
        # These are initialized to sensible default values.
        self.cogTypes = [0, 0, 0, 0]
        self.cogLevels = [0, 0, 0, 0]
        self.cogParts = [0, 0, 0, 0]
        self.cogMerits = [0, 0, 0, 0]
        
        self.savedCheesyEffect = CENormal
        self.savedCheesyHoodId = 0
        self.savedCheesyExpireTime = 0

        if hasattr(base, 'wantPets') and base.wantPets:
            self.petTrickPhrases = []

            # This is not guaranteed to be filled in; it will be
            # filled in if the toon and the pet happen to be in the
            # same zone together, or if someone called lookupPetDNA()
            # a "little while" ago.
            self.petDNA = None

        self.customMessages = []
        self.resistanceMessages = []
        self.cogSummonsEarned = []
        self.catalogNotify = ToontownGlobals.NoItems
        self.mailboxNotify = ToontownGlobals.NoItems
        self.simpleMailNotify = ToontownGlobals.NoItems # simple mail for now
        self.inviteMailNotify = ToontownGlobals.NoItems
        self.catalogScheduleCurrentWeek = 0
        self.catalogScheduleNextTime = 0
        self.monthlyCatalog = CatalogItemList.CatalogItemList()
        self.weeklyCatalog = CatalogItemList.CatalogItemList()
        self.backCatalog = CatalogItemList.CatalogItemList()
        self.onOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        #self.onGiftOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)
        self.onGiftOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.mailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
        self.deliveryboxContentsContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.GiftTag)
        self.awardMailboxContents = CatalogItemList.CatalogItemList(store = CatalogItem.Customization)
        self.onAwardOrder = CatalogItemList.CatalogItemList(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.splash = None
        self.tossTrack = None
        self.pieTracks = {}
        self.splatTracks = {}
        self.lastTossedPie = 0

        self.clothesTopsList = []
        self.clothesBottomsList = []

        # tunnel
        self.tunnelTrack = None
        self.tunnelPivotPos = [-14, -6, 0]
        # these values are used to pull the toon towards the center
        # of the tunnel, to keep him out of the walls
        # offset of tunnel center from pivot node
        self.tunnelCenterOffset = 9.
        self.tunnelCenterInfluence = .6 # 0=no effect, 1=converge on center
        self.pivotAngle = 90 + 45

        # index of the toon in the avatar chooser
        self.posIndex = 0

        # housing
        self.houseId = 0

        # This wasn't getting set before it was getting used - SP
        self.money = 0
        self.bankMoney = 0
        self.maxMoney = 0
        self.maxBankMoney = 0

        self.petId = 0
        self.bPetTutorialDone = False
        self.bFishBingoTutorialDone = False
        self.bFishBingoMarkTutorialDone = False
        
        self.accessories = []

        if base.wantKarts:
            self.kartDNA = [ -1 ] * ( getNumFields() )

        #Gardening stuff
        self.flowerCollection = None
        self.shovel = 0
        self.shovelSkill = 0
        self.shovelModel = None
        self.wateringCan = 0
        self.wateringCanSkill = 0
        self.wateringCanModel = None
        self.gardenSpecials = []#[(0,2), (1,2), (2,2), (3,2)]

        self.unlimitedSwing = 0
        self.soundSequenceList = []
        self.boardingParty = None
        self.__currentDialogue = None
        self.mail = None

        # parties
        self.invites = []
        self.hostedParties = []
        self.partiesInvitedTo = []
        self.partyReplyInfoBases = []
        
        # GM related stuff
        self.gmState = 0
        self.gmNameTagEnabled = 0
        self.gmNameTagColor = 'whiteGM'
        self.gmNameTagString = ''
        
    def disable(self):
        for soundSequence in self.soundSequenceList:
            soundSequence.finish()
        self.soundSequenceList = []
        
        if self.boardingParty:
            self.boardingParty.demandDrop()
            self.boardingParty = None
        self.ignore('clientCleanup')
        self.stopAnimations()
        self.clearCheesyEffect()
        self.stopBlink()
        self.stopSmooth()
        self.stopLookAroundNow()
        self.setGhostMode(0)
        if (self.track != None):
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if (self.effect != None):
            #self.effect.stop()
            self.effect.destroy()
            self.effect = None
        if (self.splash != None):
            self.splash.destroy()
            self.splash = None
        if (self.emote != None):
            self.emote.finish()
            self.emote = None
        self.cleanupPies()

        # take off our disguise is present
        if self.isDisguised:
            self.takeOffSuit()
            
        #if self.motion:
        #    self.motion.stop()
        if self.tunnelTrack:
            self.tunnelTrack.finish()
            self.tunnelTrack = None

        # We set the trophy score to 0, mainly to stop the spinning
        # star task should it be running.  If the avatar is
        # regenerated later, setTrophyScore will be called again and
        # restart this.
        self.setTrophyScore(0)
        
        self.removeGMIcon()
                
        DistributedPlayer.DistributedPlayer.disable(self)
        # There is no Toon disable, it is not a distributed object

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        try:
            self.DistributedToon_deleted
        except:
            self.DistributedToon_deleted = 1
            del self.safeZonesVisited
            DistributedPlayer.DistributedPlayer.delete(self)
            Toon.Toon.delete(self)
            DistributedSmoothNode.DistributedSmoothNode.delete(self)

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedPlayer.DistributedPlayer.generate(self)
        DistributedSmoothNode.DistributedSmoothNode.generate(self)
        self.cr.toons[self.doId] = self

        # moved from tcr as the av was not in the doId2do there
        if base.cr.trophyManager != None:
            base.cr.trophyManager.d_requestTrophyScore()
            
        self.startBlink()
        self.startSmooth()

        self.accept('clientCleanup', self._handleClientCleanup)
        

    def _handleClientCleanup(self):
        # make sure we're not holding a DelayDelete on ourselves
        if (self.track != None):
            DelayDelete.cleanupDelayDeletes(self.track)

    # We need to force the Toon version of these to be called, otherwise
    # we get the generic Avatar version which is undefined 
    def setDNAString(self, dnaString):
        Toon.Toon.setDNAString(self, dnaString)

    def setDNA(self, dna):
        Toon.Toon.setDNA(self, dna)

    ### setExperience ###

    def setExperience(self, experience):
        self.experience = Experience.Experience(experience, self)

        if self.inventory:
            self.inventory.updateGUI()

    ### setInventory ###

    def setInventory(self, inventoryNetString):
        # Create a new inventory if we don't already have one
        if not self.inventory:
            self.inventory = InventoryNew.InventoryNew(self,
                                                       inventoryNetString)
        # update the inventory
        self.inventory.updateInvString(inventoryNetString)

    ### setLastHood ###

    def setLastHood(self, lastHood):
        self.lastHood = lastHood

    ### setSCToontask ###
    
    def setBattleId(self, battleId):
        self.battleId = battleId
        messenger.send("ToonBattleIdUpdate", [self.doId])

    def b_setSCToontask(self, taskId, toNpcId, toonProgress, msgIndex):
        # Local
        self.setSCToontask(taskId, toNpcId, toonProgress, msgIndex)
        # Distributed
        self.d_setSCToontask(taskId, toNpcId, toonProgress, msgIndex)
        return None

    def d_setSCToontask(self, taskId, toNpcId, toonProgress, msgIndex):
        messenger.send("wakeup")
        self.sendUpdate("setSCToontask",
                        [taskId, toNpcId, toonProgress, msgIndex])

    def setSCToontask(self, taskId, toNpcId, toonProgress, msgIndex):
        """
        Receive and decode the SC message
        """
        if self.doId in base.localAvatar.ignoreList:
            # We're ignoring this jerk.
            return

        chatString = TTSCDecoders.decodeTTSCToontaskMsg(
            taskId, toNpcId, toonProgress, msgIndex)
        if chatString:
            self.setChatAbsolute(chatString,
                                 CFSpeech | CFQuicktalker | CFTimeout)

    def b_setSCSinging(self, msgIndex):
        """
        Set the Singing speedchat on Local and Distributed avatar.
        """
        # Local
        self.setSCSinging(msgIndex)
        # Distributed
        self.d_setSCSinging(msgIndex)
        return None
    
    def d_setSCSinging(self, msgIndex):
        """
        Set the Singing speedchat on Distributed avatar.
        """
        messenger.send("wakeup")
        self.sendUpdate("setSCSinging", [msgIndex])
    
    def setSCSinging(self, msgIndex):
        """
        Set the Singing speedchat on Local avatar.
        Receive and decode the SC message
        """
        if msgIndex not in OTPLocalizer.SpeedChatStaticText:
            self.sendUpdate('logSuspiciousEvent', ['invalid msgIndex in setSCSinging: %s from %s' % (
                msgIndex, self.doId)])
            return

        if self.doId in base.localAvatar.ignoreList:
            # We're ignoring this jerk.
            return

        chatString = OTPLocalizer.SpeedChatStaticText[msgIndex]
        if chatString:
            self.setChatMuted(chatString, CFSpeech | CFQuicktalker | CFTimeout)
    
    ### setSCResistance ###    
    def d_reqSCResistance(self, msgIndex):
        messenger.send("wakeup")

        # We can't rely on the AI to determine who is nearby, since
        # the AI doesn't always know.  Anytime the client directly
        # moves players around--for instance, during cutscenes,
        # minigames, or battles--the AI has no idea who's where.
        # Also, using zoneId to separate distinct areas isn't reliable
        # either, since in the factory or on the streets, two toons
        # might be in different zones yet still be adjacent.

        # To solve these issues, we have to rely on the client to
        # report who's near him.  A minor security risk, since a
        # hacker could report all sorts of people near him.  We do
        # have a few sanity checks on the AI, but mostly we take the
        # client's word for it.
        
        nearbyPlayers = self.getNearbyPlayers(ResistanceChat.EFFECT_RADIUS)
        self.sendUpdate("reqSCResistance", [msgIndex, nearbyPlayers])

    def getNearbyPlayers(self, radius, includeSelf=True):
        nearbyToons = []
        toonIds = self.cr.getObjectsOfExactClass(DistributedToon)
        for toonId, toon in toonIds.items():
            if toon is not self:
                dist = toon.getDistance(self)
                if dist < radius:
                    nearbyToons.append(toonId)
        if includeSelf:
            nearbyToons.append(self.doId)

        return nearbyToons

    def setSCResistance(self, msgIndex, nearbyToons=[]):
        """
        Receive and decode the SC message
        """
        chatString = TTSCDecoders.decodeTTSCResistanceMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFTimeout)

        ResistanceChat.doEffect(msgIndex, self, nearbyToons)

    ### battleSOS ###

    def d_battleSOS(self, requesterId, sendToId = None):
        self.sendUpdate("battleSOS", [requesterId], sendToId)

    def battleSOS(self, requesterId):
        """battleSOS(self, int requesterId)

        This message is sent after a client has failed to teleport
        successfully to another client, probably because the target
        client didn't stay put.  It just pops up a whisper message to
        that effect.
        """
        avatar = base.cr.identifyAvatar(requesterId)

        if (isinstance(avatar, DistributedToon) or
            isinstance(avatar, FriendHandle.FriendHandle)):
            self.setSystemMessage(requesterId,
                                  TTLocalizer.MovieSOSWhisperHelp % (avatar.getName()),
                                  whisperType = WhisperPopup.WTBattleSOS)
        elif avatar is not None:
            self.notify.warning('got battleSOS from non-toon %s' % requesterId)

    def getDialogueArray(self, *args):
        # Force the right inheritance chain to be called
        return Toon.Toon.getDialogueArray(self, *args)

    def setDefaultShard(self, shard):
        self.defaultShard = shard
        assert self.notify.debug("setting default shard to %s" % shard)
        
    def setDefaultZone(self, zoneId):
        # Now that we have moved the start of the Welcome Valley zones, we need to map
        # invalidated Welcome Valley zoneIds into the new range
        if (zoneId >= 20000) and (zoneId < 22000):
            zoneId = zoneId + 2000
        # Check to see if that zone has been downloaded. It is possible
        # you are playing an old account on a new computer or friend's
        # computer that has not finished the download yet.
        hoodPhase = base.cr.hoodMgr.getPhaseFromHood(zoneId)
        if not base.cr.isPaid() or (launcher and not launcher.getPhaseComplete(hoodPhase)):
            # We will act like your default zone is ToontownCentral
            # since you are not finished downloading the other zones
            # (same deal if you haven't paid)
            assert self.notify.debug("default zone %s not downloaded yet. Reverting to ToontownCentral." % zoneId)
            self.defaultZone = ToontownCentral
        else:
            assert self.notify.debug("setting default zone to %s" % zoneId)
            self.defaultZone = zoneId
                

    def setShtickerBook(self, string):
        assert self.notify.debug("setting Shticker Book to %s" % string)
        
        
    ### AccountType ###
    
    def setAsGM(self, state):
        """ Give GM's special chat abilities """
        self.notify.debug("Setting GM State: %s" %state)
        DistributedPlayer.DistributedPlayer.setAsGM(self, state)
        # if self.gmState:
            # base.localAvatar.chatMgr.addGMSpeedChat()
        
    def d_updateGMNameTag(self):
        # RAU stop the hack chat for now
        # self.sendUpdate('updateGMNameTag', [self.gmNameTagString, self.gmNameTagColor, self.gmNameTagEnabled])
        self.refreshName()
        
    def updateGMNameTag(self, tagString, color, state):
        """ Retrieves the values from the owner's prc file (see setAsGM) if the avatar is an admin """
        # make sure it's a valid UTF-8 string
        try:
            unicode(tagString, 'utf-8')
        except UnicodeDecodeError:
            self.sendUpdate('logSuspiciousEvent', ['invalid GM name tag: %s from %s' % (tagString, self.doId)])
            return
        # TODO: check other fields for malicious values

        # security hole: this allows a hacked client to change his nametag to anything he wants
        """
        self.gmNameTagString = tagString
        self.gmNameTagColor = color
        self.gmNameTagState = state
        self.refreshName()
        """
        
        
    def refreshName(self):
        return
        self.notify.debug("Refreshing GM Nametag String: %s Color: %s State: %s" % 
            (self.gmNameTagString, self.gmNameTagColor, self.gmNameTagEnabled))
        if hasattr(self, "nametag") and self.gmNameTagEnabled:
            self.setDisplayName(self.gmNameTagString)
            self.setName(self.gmNameTagString)
            # A gold star!
            self.trophyStar1 = loader.loadModel('models/misc/smiley')
            self.trophyStar1.reparentTo(self.nametag.getNameIcon())
            self.trophyStar1.setScale(1)
            self.trophyStar1.setZ(2.25)
            self.trophyStar1.setColor(Vec4(0.75,0.75,0.75, 0.75))
            self.trophyStar1.setTransparency(1)
            self.trophyStarSpeed = 15
            # Spinning!
            #taskMgr.add(self.__starSpin1, self.uniqueName("starSpin1"))
        else:
            taskMgr.add(self.__refreshNameCallBack, self.uniqueName("refreshNameCallBack"))
        
    def __starSpin1(self, task):
        now = globalClock.getFrameTime()
        r = now * 90 % 360.0
        self.trophyStar1.setH(r)
        return Task.cont
    
    def __refreshNameCallBack(self, task):
        if hasattr(self, "nametag") and self.nametag.getName() != '':
            self.refreshName()
            return Task.done
        else:
            return Task.cont
        
    ### setTalk ###    
        
    def setTalk(self, fromAV, fromAC, avatarName, chat, mods, flags):
        """ Overridden from Distributed player becase pirates ignores players a different way"""
        
        if base.cr.avatarFriendsManager.checkIgnored(fromAV):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromAV)
            return

        if fromAV in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromAV)
            return            
                
        if base.config.GetBool('want-sleep-reply-on-regular-chat', 0):
            if base.localAvatar.sleepFlag == 1:        
                # I am sleeping so I send an autoreply message            
                self.sendUpdate("setSleepAutoReply" , [base.localAvatar.doId], fromAV)              
            
        newText,scrubbed = self.scrubTalk(chat, mods)
        self.displayTalk(newText)
        base.talkAssistant.receiveOpenTalk(fromAV, avatarName, fromAC, None, newText)

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        """ Overridden from Distributed player becase pirates ignores players a different way"""
        
        if GMUtils.testGMIdentity(avatarName):
            avatarName  = GMUtils.handleGMName(avatarName)
        
        if base.cr.avatarFriendsManager.checkIgnored(fromAV):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromAV)
            return

        if fromAV in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromAV)
            return            
                
        # if base.localAvatar.animFSM.getCurrentState() == base.localAvatar.animFSM.getStateNamed('Sleep'):     
        if base.localAvatar.sleepFlag == 1:   
            # I am sleeping so I send an autoreply message      
            if not base.cr.identifyAvatar(fromAV) == base.localAvatar:
                self.sendUpdate("setSleepAutoReply" , [base.localAvatar.doId], fromAV)      
        
        newText, scrubbed = self.scrubTalk(chat, mods)
        self.displayTalkWhisper(fromAV, avatarName, chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.doId, self.getName(), newText)
        
    def setSleepAutoReply(self, fromId):
        """To be overrided by subclass"""
        pass

    def _isValidWhisperSource(self, source):
        return (isinstance(source, FriendHandle.FriendHandle) or
                isinstance(source, DistributedToon))
        
    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        """
        Receive and decode the SC message.
        """ 
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return

        if not self._isValidWhisperSource(handle):
            self.notify.warning('setWhisperSCEmoteFrom non-toon %s' % fromId)
            return

        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return            
                
        # if base.localAvatar.animFSM.getCurrentState() == base.localAvatar.animFSM.getStateNamed('Sleep'):     
        if base.localAvatar.sleepFlag == 1:   
            # I am sleeping so I send an autoreply message      
            if not base.cr.identifyAvatar(fromId) == base.localAvatar:
                self.sendUpdate("setSleepAutoReply" , [base.localAvatar.doId], fromId) 
            
        chatString = SCDecoders.decodeSCEmoteWhisperMsg(emoteId,
                                                        handle.getName())
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTEmote)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_EMOTE, emoteId, fromId) 
            
    def setWhisperSCFrom(self, fromId, msgIndex):
        """
        Receive and decode the SpeedChat message.
        """
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return

        if not self._isValidWhisperSource(handle):
            self.notify.warning('setWhisperSCFrom non-toon %s' % fromId)
            return

        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return

        if fromId in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)
            return            
                
        if base.localAvatar.sleepFlag == 1:   
            # I am sleeping so I send an autoreply message      
            if not base.cr.identifyAvatar(fromId) == base.localAvatar:
                self.sendUpdate("setSleepAutoReply" , [base.localAvatar.doId], fromId)
        
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.talkAssistant.receiveAvatarWhisperSpeedChat(TalkAssistant.SPEEDCHAT_NORMAL, msgIndex, fromId)   

    ### setWhisperSCToontask ###

    def whisperSCToontaskTo(self, taskId, toNpcId, toonProgress, msgIndex,
                            sendToId):
        """
        Sends a speedchat whisper message to the indicated
        toon, prefixed with our own name.
        """
        messenger.send("wakeup")
        self.sendUpdate("setWhisperSCToontaskFrom",
                        [self.doId, taskId, toNpcId, toonProgress, msgIndex],
                        sendToId)

    def setWhisperSCToontaskFrom(self, fromId,
                                 taskId, toNpcId, toonProgress, msgIndex):
        """
        Receive and decode the SC message.
        """        
        sender = base.cr.identifyAvatar(fromId)
        if sender == None:
            return

        if fromId in self.ignoreList:
            # We're ignoring this jerk.
            self.d_setWhisperIgnored(fromId)

        chatString = TTSCDecoders.decodeTTSCToontaskMsg(
            taskId, toNpcId, toonProgress, msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)

    def setMaxNPCFriends(self, max):
        self.maxNPCFriends = max

    def getMaxNPCFriends(self):
        return self.maxNPCFriends

    def getNPCFriendsDict(self):
        return self.NPCFriendsDict

    def setNPCFriendsDict(self, NPCFriendsList):
        NPCFriendsDict = {}
        for friendPair in NPCFriendsList:
            NPCFriendsDict[friendPair[0]] = friendPair[1]
        self.NPCFriendsDict = NPCFriendsDict

    def setMaxClothes(self, max):
        self.maxClothes = max

    def getMaxClothes(self):
        return self.maxClothes
    
    def getClothesTopsList(self):
        return self.clothesTopsList

    def setClothesTopsList(self, clothesList):
        self.clothesTopsList = clothesList

    def getClothesBottomsList(self):
        return self.clothesBottomsList

    def setClothesBottomsList(self, clothesList):
        self.clothesBottomsList = clothesList

    def catalogGenClothes(self, avId):
        # this is used only when accepting new bottoms from the mailbox
        # after a catalog purchase.
        if avId == self.doId:
            self.generateToonClothes()
            self.loop('neutral')
            
    def isClosetFull(self, extraClothes = 0):
        numClothes = len(self.clothesTopsList)/4 + len(self.clothesBottomsList)/2
        return (numClothes + extraClothes >= self.maxClothes)

    def setMaxHp(self, hitPoints):
        DistributedPlayer.DistributedPlayer.setMaxHp(self, hitPoints)
        # Just in case something has changed with the number of props
        if self.inventory:
            self.inventory.updateGUI()

    def died(self):
        """
        The toon has run out of HP.
        """
        # Tell the world (in particular, tell any battles).
        messenger.send(self.uniqueName('died'))
        
        # make sure we go to a safezone!
        if self.isLocal():
            target_sz = ZoneUtil.getSafeZoneId(self.defaultZone)
            place = self.cr.playGame.getPlace()
            if place and place.fsm:
                place.fsm.request('died', [{
                    "loader" : ZoneUtil.getLoaderName(target_sz),
                    "where" : ZoneUtil.getWhereName(target_sz, 1),
                    'how' : 'teleportIn',
                    'hoodId' : target_sz,
                    'zoneId' : target_sz,
                    'shardId' : None,
                    'avId' : -1,
                    'battle' : 1,
                    }])

    def setInterface(self, string):
        assert self.notify.debug("setting interface to %s" % string)
        
    def setZonesVisited(self, hoods):
        self.safeZonesVisited = hoods
        assert self.notify.debug("setting safe zone list to %s" % self.safeZonesVisited)
        
    def setHoodsVisited(self, hoods):
        self.hoodsVisited = hoods
        assert self.notify.debug("setting hood list to %s" % self.hoodsVisited)
        # For now, visiting any HQ is enough to enable the disguise (and SOS) pages.
        if (ToontownGlobals.SellbotHQ in hoods) or (ToontownGlobals.CashbotHQ in hoods) or (ToontownGlobals.LawbotHQ in hoods):
            self.setDisguisePageFlag(1)

    def wrtReparentTo(self, parent):
        # We need to define this in DistributedToon just to force the
        # right function to be called (we need the
        # DistributedSmoothNode flavor to be called, but it wants to
        # call the NodePath flavor instead).
        DistributedSmoothNode.DistributedSmoothNode.wrtReparentTo(self, parent)
        

    ### setTutorialAck ###
    def setTutorialAck(self, tutorialAck):
        """
        This flag tells whether the player has acknowledged the opportunity
        for a tutorial.
        """
        self.tutorialAck = tutorialAck


    ### setEarnedExperience ###
    def setEarnedExperience(self, earnedExp):
        # The AI uses this to tell the toon how much earned experience he
        # has accumulated so far within a particular battle.  This is
        # important to allow the client to gray out gag buttons when the
        # toon exceeds his experience cap for the battle.
        self.earnedExperience = earnedExp
        

    ### setTunnelIn ###
    def b_setTunnelIn(self, endX, tunnelOrigin):
        timestamp = globalClockDelta.getFrameNetworkTime()
        pos = tunnelOrigin.getPos(render)
        h = tunnelOrigin.getH(render)
        self.setTunnelIn(timestamp, endX, pos[0], pos[1], pos[2], h)
        self.d_setTunnelIn(timestamp, endX, pos[0], pos[1], pos[2], h)

    def d_setTunnelIn(self, timestamp, endX, x, y, z, h):
        self.sendUpdate("setTunnelIn", [timestamp, endX, x, y, z, h])

    def setTunnelIn(self, timestamp, endX, x, y, z, h):
        t = globalClockDelta.networkToLocalTime(timestamp)
        self.handleTunnelIn(t, endX, x, y, z, h)

    def getTunnelInToonTrack(self, endX, tunnelOrigin):
        # create a node that the toon will swing around
        pivotNode = tunnelOrigin.attachNewNode(self.uniqueName('pivotNode'))
        pivotNode.setPos(*self.tunnelPivotPos)
        pivotNode.setHpr(0,0,0)

        pivotY = pivotNode.getY(tunnelOrigin)
        endY = 5.
        straightLerpDur = abs(endY-pivotY) / ToonForwardSpeed
        pivotDur = 2.
        # lerp the toon's X position over the last 90 degrees
        pivotLerpDur = pivotDur * (90./self.pivotAngle)

        self.reparentTo(pivotNode)
        self.setPos(0,0,0)
        # store the X position that the toon should be in at the end
        # of the pivot
        self.setX(tunnelOrigin, endX)
        targetX = self.getX()
        self.setX(self.tunnelCenterOffset + \
                  ((targetX - self.tunnelCenterOffset) * \
                   (1.-self.tunnelCenterInfluence)))
        self.setHpr(tunnelOrigin, 0, 0, 0)
        pivotNode.setH(-self.pivotAngle)

        return Sequence(
            Wait(.8), # give remote clients a fighting chance at
                      # starting their animations in time, so that
                      # toons run around the corner, instead of
                      # popping into existence
            Parallel(
            LerpHprInterval(pivotNode, pivotDur, hpr=Point3(0,0,0),
                            name=self.uniqueName("tunnelInPivot")),
            Sequence(
            Wait(pivotDur - pivotLerpDur),
            LerpPosInterval(self, pivotLerpDur, pos=Point3(targetX,0,0),
                            name=self.uniqueName("tunnelInPivotLerpPos")),
            ),
            ),
            Func(self.wrtReparentTo, render),
            Func(pivotNode.removeNode),
            LerpPosInterval(self, straightLerpDur,
                            pos=Point3(endX, endY, 0.1),
                            other=tunnelOrigin,
                            name=self.uniqueName("tunnelInStraightLerp")),
            )

    def handleTunnelIn(self, startTime, endX, x, y, z, h):
        """
        this handles tunnel in animations for distributed toons
        see LocalToon.py for the local toon animation
        """
        assert self.notify.debug("DistributedToon.handleTunnelIn")

        self.stopSmooth()
        # don't parent to render yet -- offscreen nametag would show up
        #self.reparentTo(render)

        # create a temporary tunnel origin node
        tunnelOrigin = render.attachNewNode('tunnelOrigin')
        tunnelOrigin.setPosHpr(x,y,z,h,0,0)

        self.tunnelTrack = Sequence(
            self.getTunnelInToonTrack(endX, tunnelOrigin),
            Func(tunnelOrigin.removeNode),
            Func(self.startSmooth),
            )
        # add in the smoothing delay
        # TODO: this won't work perfectly until
        # - telemetry is queued even when smoothing is off
        # - we prevent remote toon's Place ClassicFSM from putting them
        #   into the neutral cycle
        tOffset = globalClock.getFrameTime() - \
                  (startTime + self.smoother.getDelay())
        if tOffset < 0.:
            self.tunnelTrack = Sequence(
                Wait(-tOffset),
                self.tunnelTrack,
                )
            self.tunnelTrack.start()
        else:
            self.tunnelTrack.start(tOffset)
    
    ### setTunnelOut ###
    def b_setTunnelOut(self, startX, startY, tunnelOrigin):
        timestamp = globalClockDelta.getFrameNetworkTime()
        pos = tunnelOrigin.getPos(render)
        h = tunnelOrigin.getH(render)
        self.setTunnelOut(timestamp, startX, startY,
                          pos[0], pos[1], pos[2], h)
        self.d_setTunnelOut(timestamp, startX, startY,
                            pos[0], pos[1], pos[2], h)

    def d_setTunnelOut(self, timestamp, startX, startY, x, y, z, h):
        self.sendUpdate("setTunnelOut",
                        [timestamp, startX, startY, x, y, z, h])

    def setTunnelOut(self, timestamp, startX, startY, x, y, z, h):
        t = globalClockDelta.networkToLocalTime(timestamp)
        self.handleTunnelOut(t, startX, startY, x, y, z, h)

    def getTunnelOutToonTrack(self, startX, startY, tunnelOrigin):
        startPos = self.getPos(tunnelOrigin)
        startHpr = self.getHpr(tunnelOrigin)
        reducedAvH = PythonUtil.fitDestAngle2Src(startHpr[0], 180)

        # create a node that the toon will swing around
        pivotNode = tunnelOrigin.attachNewNode(self.uniqueName('pivotNode'))
        pivotNode.setPos(*self.tunnelPivotPos)
        pivotNode.setHpr(0,0,0)

        pivotY = pivotNode.getY(tunnelOrigin)
        straightLerpDur = abs(startY-pivotY) / ToonForwardSpeed
        pivotDur = 2.
        # lerp the toon's X position over the first 90 degrees
        pivotLerpDur = pivotDur * (90./self.pivotAngle)

        def getTargetPos(self=self):
            """ this is a thunk that returns the target pos (relative to
            pivotNode) that the toon should lerp to during the pivot """
            pos = self.getPos()
            return Point3(self.tunnelCenterOffset + \
                          ((pos[0] - self.tunnelCenterOffset) * \
                           (1.-self.tunnelCenterInfluence)),
                          pos[1], pos[2])
        return Sequence(
            Parallel(
            LerpPosInterval(self, straightLerpDur,
                            pos=Point3(startX, pivotY, 0.1),
                            startPos = startPos,
                            other=tunnelOrigin,
                            name=self.uniqueName("tunnelOutStraightLerp")),
            LerpHprInterval(self, straightLerpDur * .8,
                            hpr=Point3(reducedAvH, 0, 0),
                            startHpr = startHpr,
                            other=tunnelOrigin,
                            name=self.uniqueName("tunnelOutStraightLerpHpr")),
            ),
            Func(self.wrtReparentTo, pivotNode),
            Parallel(
            LerpHprInterval(pivotNode, pivotDur,
                            hpr=Point3(-self.pivotAngle,0,0),
                            name=self.uniqueName("tunnelOutPivot")),
            LerpPosInterval(self, pivotLerpDur, pos=getTargetPos,
                            name=self.uniqueName("tunnelOutPivotLerpPos")),
            ),
            Func(self.wrtReparentTo, render),
            Func(pivotNode.removeNode),
            )


    def handleTunnelOut(self, startTime, startX, startY, x, y, z, h):
        """
        this handles tunnel out animations for distributed toons
        see LocalToon.py for the local toon animation
        """
        assert self.notify.debug("DistributedToon.handleTunnelOut")

        # create a temporary tunnel origin node
        tunnelOrigin = render.attachNewNode('tunnelOrigin')
        tunnelOrigin.setPosHpr(x,y,z,h,0,0)

        self.tunnelTrack = Sequence(
            Func(self.stopSmooth),
            self.getTunnelOutToonTrack(startX, startY, tunnelOrigin),
            #Func(self.reparentTo, hidden),
            Func(self.detachNode),
            Func(tunnelOrigin.removeNode),
            )
        # add in the smoothing delay
        tOffset = globalClock.getFrameTime() - \
                  (startTime + self.smoother.getDelay())
        if tOffset < 0.:
            self.tunnelTrack = Sequence(
                Wait(-tOffset),
                self.tunnelTrack,
                )
            self.tunnelTrack.start()
        else:
            self.tunnelTrack.start(tOffset)

    def enterTeleportOut(self, *args, **kw):
        # We override the definition of this function in Toon.py so we
        # can add DelayDelete to the track, so an exiting toon won't
        # disappear mid-teleport.
        Toon.Toon.enterTeleportOut(self, *args, **kw)
        if self.track:
            self.track.delayDelete = DelayDelete.DelayDelete(self, 'enterTeleportOut')

    def exitTeleportOut(self):
        if (self.track != None):
            DelayDelete.cleanupDelayDeletes(self.track)
        Toon.Toon.exitTeleportOut(self)

    ### setAnimState ###

    def b_setAnimState(self, animName, animMultiplier=1.0, callback = None,
                       extraArgs=[]):
        # We set the distributed anim state first, since when we set
        # it locally it might call the callback, which could impact
        # the distributed state.  This is particularly true when our
        # toon gets sleepy and goes to bed in ghost mode.

        self.d_setAnimState(animName, animMultiplier, None, extraArgs)
        self.setAnimState(animName, animMultiplier, None, None, callback, extraArgs)

    def d_setAnimState(self, animName, animMultiplier=1.0, timestamp=None,
                       extraArgs=[]):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("setAnimState", [animName, animMultiplier, timestamp])
        
    def setAnimState(self, animName, animMultiplier=1.0, timestamp=None,
                     animType=None, callback=None, extraArgs=[]):

        # this is a band-aid: somehow animState was getting set to "None"?
        if not animName or (animName == "None"):
            return
        
        if (timestamp == None):
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)

        # protect against bogus anims
        if self.animFSM.getStateNamed(animName):
            if (animName in self.setAnimStateAllowedList):
                self.animFSM.request(
                    animName, [animMultiplier, ts, callback, extraArgs])
            else:
                self.notify.debug('Hacker trying to setAnimState on an illegal animation. Attacking toon = %d' % self.doId)
                base.cr.centralLogger.writeClientEvent('Hacker trying to setAnimState on an illegal animation. Attacking toon = %d' % self.doId)
        else:
            # suspicious
            self.sendUpdate("logSuspiciousEvent", ["setAnimState: " + animName])
            
        self.cleanupPieInHand()

    ### setEmoteState ###

    def b_setEmoteState(self, animIndex, animMultiplier):
        self.setEmoteState(animIndex, animMultiplier)
        self.d_setEmoteState(animIndex, animMultiplier)

    def d_setEmoteState(self, animIndex, animMultiplier):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("setEmoteState", [animIndex, animMultiplier, timestamp])
        
    def setEmoteState(self, animIndex, animMultiplier, timestamp=None):
        # A -1 is considered a clear -- do nothing Because this is a
        # broadcast ram field, one you do any emote, you will always have a
        # value sent to future toons you meet It is wasteful to have your
        # old emote index and make these new toons do all that work to
        # create the emote track, only to have them skip through it since
        # the timestamp will be really far in the past. Instead, it is up
        # to the localToon to "clear" his anim (emote) index after his
        # emote is finished. This is done in Emote.py
        if animIndex == TTEmote.EmoteClear:
            assert self.notify.debug("setEmoteState: clearing emote state")
            return
        
        if (timestamp == None):
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)

        assert(self.notify.debug("setEmoteState: animIndex: %s animMult: %s timestamp: %s" %
               (animIndex, animMultiplier, timestamp)))

        # Put the animName in extraArgs to match the structure of the ClassicFSM
        callback=None
        extraArgs=[]
        extraArgs.insert(0, animIndex)

        self.doEmote(animIndex, animMultiplier, ts, callback, extraArgs)
        #self.animFSM.request(
        #    "Emote", [animMultiplier, ts, callback, extraArgs])

    ### setCogStatus ###
    def setCogStatus(self, cogStatusList):
        assert self.notify.debug("setting cogs to %s" % cogStatusList)
        self.cogs = cogStatusList

    ### setCogCount ###
    def setCogCount(self, cogCountList):
        assert self.notify.debug("setting cogCount to %s" % cogCountList)
        self.cogCounts = cogCountList
        # update the suit page
        if hasattr(self, 'suitPage'):
            self.suitPage.updatePage()


    ### setCogRadar ###
    def setCogRadar(self, radar):
        assert self.notify.debug("setting cog radar to: %s" % radar)
        self.cogRadar = radar
        if hasattr(self, 'suitPage'):
            self.suitPage.updateCogRadarButtons(radar)

    ### setBuildingRadar ###
    def setBuildingRadar(self, radar):
        assert self.notify.debug("setting building radar to: %s" % radar)
        self.buildingRadar = radar
        if hasattr(self, 'suitPage'):
            self.suitPage.updateBuildingRadarButtons(radar)

    ### setCogTypes ###
    def setCogTypes(self, types):
        assert self.notify.debug("setting cog types to: %s" % types)
        self.cogTypes = types
        if self.disguisePage:
            self.disguisePage.updatePage()

    ### setCogLevels ###
    def setCogLevels(self, levels):
        assert self.notify.debug("setting cog levels to: %s" % levels)
        self.cogLevels = levels
        if self.disguisePage:
            self.disguisePage.updatePage()

    def getCogLevels(self):
        return self.cogLevels

    ### setCogParts ###
    def setCogParts(self, parts):
        assert self.notify.debug("setting cog parts to: %s" % parts)
        self.cogParts = parts
        if self.disguisePage:
            self.disguisePage.updatePage()

    def getCogParts(self):
        return self.cogParts

    ### setCogMerits ###
    def setCogMerits(self, merits):
        assert self.notify.debug("setting cog merits to: %s" % merits)
        self.cogMerits = merits
        if self.disguisePage:
            self.disguisePage.updatePage()

    def readyForPromotion(self, dept):
        merits = base.localAvatar.cogMerits[dept]
        totalMerits = CogDisguiseGlobals.getTotalMerits(self, dept)
        #print "print merits[%d]: %d/%d"  % (dept, merits, totalMerits)
        if (merits >= totalMerits):
            return 1
        else:
            return 0
    
    ### setCogIndex ###

    # -1 means we are not disguised as a cog. 0, 1, 2, 3 means we are disguised
    # as a self.cogTypes[index] cog.
    
    def setCogIndex(self, index):
        assert self.notify.debug("setCogIndex: %s isDisguised: %s" % (index, self.isDisguised))
        self.cogIndex = index
        if self.cogIndex == -1:
            # we are not a cog
            if self.isDisguised:
                self.takeOffSuit()
        else:
            # we are a cog
            cogIndex = self.cogTypes[index] + (SuitDNA.suitsPerDept * index)
            cog = SuitDNA.suitHeadTypes[cogIndex]
            self.putOnSuit(cog)

    def isCog(self):
        if self.cogIndex == -1:
            return 0
        else:
            return 1

    ### setDisguisePageFlag ###
    def setDisguisePageFlag(self, flag):
        if flag and hasattr(self, "book"):
            self.loadDisguisePages()

        # We don't attempt to unload the pages if the disguisePageFlag
        # is ever set back to 0, since that doesn't normally happen
        # during gameplay.
        self.disguisePageFlag = flag

    ## Fish collection
    def setFishCollection(self, genusList, speciesList, weightList):
        assert(self.notify.debug("setFishCollection: genusList: %s speciesList: %s weightList: %s" %
                                 (genusList, speciesList, weightList)))
        self.fishCollection = FishCollection.FishCollection()
        self.fishCollection.makeFromNetLists(genusList, speciesList, weightList)

    def getFishCollection(self):
        return self.fishCollection

    ## Max fish tank
    def setMaxFishTank(self, maxTank):
        self.maxFishTank = maxTank

    def getMaxFishTank(self):
        return self.maxFishTank

    ## Fish tank    
    def setFishTank(self, genusList, speciesList, weightList):
        assert(self.notify.debug("setFishTank: genusList: %s speciesList: %s weightList: %s" %
                                 (genusList, speciesList, weightList)))
        self.fishTank = FishTank.FishTank()
        self.fishTank.makeFromNetLists(genusList, speciesList, weightList)
        messenger.send(self.uniqueName("fishTankChange"))

    def getFishTank(self):
        return self.fishTank

    def isFishTankFull(self):
        """
        Return 1 if the fish tank if full to capacity
        Return 0 if there is room for more fish
        """
        return (len(self.fishTank) >= self.maxFishTank)

    ## Fishing Rod
    def setFishingRod(self, rodId):
        assert self.notify.debug("setFishingRod: %s" % rodId)
        self.fishingRod = rodId

    def getFishingRod(self):
        return self.fishingRod

    ## Fishing trophy List
    def setFishingTrophies(self, trophyList):
        assert self.notify.debug("setting fish trophies to %s" % trophyList)
        self.fishingTrophies = trophyList
        
    def getFishingTrophies(self):
        return self.fishingTrophies

    ### setQuests ###
    def setQuests(self, flattenedQuests):
        assert self.notify.debug("setting quests to %s" % flattenedQuests)
        # Build the real quest list from the flattened one from the network
        questList = []
        # A quest is a list with
        #   (questId, npcId, otherId, rewardId, progress)
        questLen = 5
        # Step from 2 to the end, by the questLen
        for i in range(0, len(flattenedQuests), questLen):
            questList.append(flattenedQuests[i:i+questLen])
        self.quests = questList

        if self == base.localAvatar:
            messenger.send("questsChanged")

    def setQuestCarryLimit(self, limit):
        assert self.notify.debug("setting questCarryLimit to %s" % limit)
        self.questCarryLimit = limit

        if self == base.localAvatar:
            messenger.send("questsChanged")

    def getQuestCarryLimit(self):
        return self.questCarryLimit

    ### setMaxCarry ###

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry
        # update the invenotry gui
        if self.inventory:
            self.inventory.updateGUI()

    def getMaxCarry(self):
        return self.maxCarry

    ### Cheesy rendering effects ###

    def setCheesyEffect(self, effect, hoodId, expireTime):
        # if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            # holidayIds = base.cr.newsManager.getHolidayIdList()
            # if effect == ToontownGlobals.CESnowMan and ToontownGlobals.WINTER_CAROLING not in holidayIds:
                # self.savedCheesyEffect = CENormal
                # self.reconsiderCheesyEffect()
                # return
            # elif effect == ToontownGlobals.CEPumpkin and ToontownGlobals.TRICK_OR_TREAT not in holidayIds:
                # self.savedCheesyEffect = CENormal
                # self.reconsiderCheesyEffect()
                # return
        # else:
            # taskMgr.doMethodLater(5.0, self.setCheesyEffect, "waitForNewsManagerToSetCheesyEffect", extraArgs = [effect, hoodId, expireTime])
            # return
        self.savedCheesyEffect = effect
        self.savedCheesyHoodId = hoodId
        self.savedCheesyExpireTime = expireTime

        if self == base.localAvatar:
            self.notify.debug("setCheesyEffect(%s, %s, %s)" %
                             (effect, hoodId, expireTime))
            if effect != ToontownGlobals.CENormal:
                serverTime = time.time() + self.cr.getServerDelta()
                duration = (expireTime * 60) - serverTime
                if duration < 0:
                    self.notify.debug("effect should have expired %s ago." % (PythonUtil.formatElapsedSeconds(-duration)))
                else:
                    self.notify.debug("effect will expire in %s." % (PythonUtil.formatElapsedSeconds(duration)))

        if self.activeState == DistributedObject.ESGenerated:
            # If we get this message while the avatar is already
            # generated, then lerp the effect in smoothly.
            self.reconsiderCheesyEffect(lerpTime = 0.5)
            
        else:
            # Otherwise, if we're getting this message as part of the
            # generate sequence for the avatar, just set it
            # immediately.
            self.reconsiderCheesyEffect()

    def reconsiderCheesyEffect(self, lerpTime = 0):
        # Reconsiders whether to apply the cheesy effect, or disable
        # it, according to the current zoneId, etc.
        #import pdb; pdb.set_trace()
        effect = self.savedCheesyEffect
        hoodId = self.savedCheesyHoodId
        if not self.cr.areCheesyEffectsAllowed():
            effect = CENormal

        if hoodId != 0:
            # Get our current hood and make sure it matches hoodId.
            try:
                currentHoodId = base.cr.playGame.hood.id
            except:
                # Oh, we don't know our current hood yet.  Or maybe
                # we're in our estate.
                currentHoodId = None

            if hoodId == 1:
                # hoodId 1 means any hood except TTC.
                if currentHoodId == ToontownGlobals.ToontownCentral:
                    effect = CENormal
            else:
                # Any other hoodId means only in that hood.
                if currentHoodId != None and currentHoodId != hoodId:
                    effect = CENormal

        if self.ghostMode:
            effect = CEGhost

        self.applyCheesyEffect(effect, lerpTime = lerpTime)

    def setGhostMode(self, flag):
        assert self.notify.debug("setGhostMode: %s" % flag)
        # Ghost mode.  This is kind of like a cheesy effect in that it
        # makes the toon invisible (or nearly invisible depending on
        # whether the local player has seeGhosts enabled), but it also
        # has special meaning when it is applied to the local player
        # (turning off certain collisions, etc.)
        if self.ghostMode != flag:
            self.ghostMode = flag
            if not hasattr(self, "cr"):
                # The toon has already been deleted, forget it.
                return

            if self.activeState <= DistributedObject.ESDisabled:
                self.notify.debug("not applying cheesy effect to disabled Toon")
            elif self.activeState == DistributedObject.ESGenerating:
                self.reconsiderCheesyEffect()
            elif self.activeState == DistributedObject.ESGenerated:
                self.reconsiderCheesyEffect(lerpTime = 0.5)
            else:
                self.notify.warning("unknown activeState: %s" % self.activeState)

            self.showNametag2d()
            self.showNametag3d()

            # No one bumps into ghosts, except maybe other ghosts.
            if hasattr(self, "collNode"):
                if self.ghostMode:
                    self.collNode.setCollideMask(ToontownGlobals.GhostBitmask)
                else:
                    self.collNode.setCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.PieBitmask)
                
            if self.isLocal():
                # Call methods defined on LocalAvatar only.  If we
                # defined stubs here, then we'd get into trouble with
                # the multiple inheritance ambiguity.
                if self.ghostMode:
                    self.useGhostControls()
                else:
                    self.useWalkControls()

    if hasattr(base, 'wantPets') and base.wantPets:
        def setPetTrickPhrases(self, petTricks):
            # this is a list of trick IDs, not speedchat IDs
            self.petTrickPhrases = petTricks
            if self.isLocal():
                messenger.send('petTrickPhrasesChanged')

    # Update available custom speedchat messages
    def setCustomMessages(self, customMessages):
        self.customMessages = customMessages
        if self.isLocal():
            messenger.send("customMessagesChanged")

    # Update available resistance speedchat messages
    # this list should be of the form:
    # [[msg1, msg1Charges], [msg2, msg2Charges], ...]
    def setResistanceMessages(self, resistanceMessages):
        self.resistanceMessages = resistanceMessages
        if self.isLocal():
            messenger.send("resistanceMessagesChanged")

    def getResistanceMessageCharges(self, textId):
        msgs = self.resistanceMessages
        for i in range(len(msgs)):
            if msgs[i][0] == textId:
                return msgs[i][1]

        return 0

    def setCatalogSchedule(self, currentWeek, nextTime):
        self.catalogScheduleCurrentWeek = currentWeek
        self.catalogScheduleNextTime = nextTime

        if self.isLocal():
            self.notify.debug("setCatalogSchedule(%s, %s)" % (currentWeek, nextTime))
            if nextTime:
                serverTime = time.time() + self.cr.getServerDelta()
                duration = (nextTime * 60) - serverTime
                self.notify.debug("next catalog in %s." % (PythonUtil.formatElapsedSeconds(duration)))

    def setCatalog(self, monthlyCatalog, weeklyCatalog, backCatalog):
        self.monthlyCatalog = CatalogItemList.CatalogItemList(monthlyCatalog)
        self.weeklyCatalog = CatalogItemList.CatalogItemList(weeklyCatalog)
        self.backCatalog = CatalogItemList.CatalogItemList(backCatalog)

        # If we never looked at the old catalog, pretend we did now.
        # This will allow the new catalog notify message (which the AI
        # is about to send) to generate a new notification.
        if self.catalogNotify == ToontownGlobals.NewItems:
            self.catalogNotify = ToontownGlobals.OldItems

    def setCatalogNotify(self, catalogNotify, mailboxNotify):
        #noCat = " "
        #noMail = " "
        if len(self.weeklyCatalog) + len(self.monthlyCatalog) == 0:
            catalogNotify = ToontownGlobals.NoItems
            #noCat = "no catalog items"
        if len(self.mailboxContents) == 0:
            mailboxNotify = ToontownGlobals.NoItems
            #noMail = "no mail items"
        #print("Start setCatalogNotify")
        #print("catalogNotify %s %s" % (catalogNotify, noCat))
        #print("mailboxNotify %s %s" % (mailboxNotify, noMail))

        self.catalogNotify = catalogNotify
        self.mailboxNotify = mailboxNotify

        if self.isLocal():
            self.gotCatalogNotify = 1
            self.refreshOnscreenButtons()
            print("local")
        #print("End setCatalogNotify")

    def setDeliverySchedule(self, onOrder):
        self.onOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

        if self == base.localAvatar:
            assert self.notify.debug("setDeliverySchedule(%s)" % (self.onOrder))
            nextTime = self.onOrder.getNextDeliveryDate()
            if nextTime != None:
                serverTime = time.time() + self.cr.getServerDelta()
                duration = (nextTime * 60) - serverTime
                self.notify.debug("next delivery in %s." % (PythonUtil.formatElapsedSeconds(duration)))
            messenger.send("setDeliverySchedule-%s" % (self.doId))

    def setMailboxContents(self, mailboxContents):
        self.mailboxContents = CatalogItemList.CatalogItemList(mailboxContents, store = CatalogItem.Customization)
        messenger.send("setMailboxContents-%s" % (self.doId))
    
    """  
    def setDeliveryboxContents(self, deliveryboxContents):
        self.deliveryboxContents = CatalogItemList.CatalogItemList(deliveryboxContents, store = CatalogItem.Customization | CatalogItem.GiftTag)
    """

    def setAwardSchedule(self, onOrder):
        self.onAwardOrder = CatalogItemList.CatalogItemList(onOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

        if self == base.localAvatar:
            assert self.notify.debug("setAwardSchedule(%s)" % (self.onAwardOrder))
            nextTime = self.onAwardOrder.getNextDeliveryDate()
            if nextTime != None:
                serverTime = time.time() + self.cr.getServerDelta()
                duration = (nextTime * 60) - serverTime
                self.notify.debug("next delivery in %s." % (PythonUtil.formatElapsedSeconds(duration)))
            messenger.send("setAwardSchedule-%s" % (self.doId))
    

    def setAwardMailboxContents(self, awardMailboxContents):
        self.notify.debug("Setting awardMailboxContents to %s." % (awardMailboxContents))
        self.awardMailboxContents = CatalogItemList.CatalogItemList(awardMailboxContents, store = CatalogItem.Customization )
        self.notify.debug("awardMailboxContents is %s." % (self.awardMailboxContents))
        messenger.send("setAwardMailboxContents-%s" % (self.doId))

    def setAwardNotify(self, awardNotify):
        """Handle the AI/Uberdog telling us if we have new, old, or no award."""
        self.notify.debug( "setAwardNotify( %s )" % awardNotify )
        self.awardNotify = awardNotify

        if self.isLocal():
            self.gotCatalogNotify = 1
            self.refreshOnscreenButtons()        

    
    def setGiftSchedule(self, onGiftOrder):
        #self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate | CatalogItem.GiftTag)

        self.onGiftOrder = CatalogItemList.CatalogItemList(onGiftOrder, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if self == base.localAvatar:
            assert self.notify.debug("setGetSchedule(%s)" % (self.onGiftOrder))
            nextTime = self.onGiftOrder.getNextDeliveryDate()
            if nextTime != None:
                serverTime = time.time() + self.cr.getServerDelta()
                duration = (nextTime * 60) - serverTime
                self.notify.debug("next delivery in %s." % (PythonUtil.formatElapsedSeconds(duration)))

    ### SplashEffect ###
    def playSplashEffect(self, x, y, z):
        # Show a splash
        from toontown.effects import Splash
        if self.splash == None:
            self.splash = Splash.Splash(render)
        self.splash.setPos(x, y, z)
        self.splash.setScale(2)
        self.splash.play()
        # Play a splash sound
        place = base.cr.playGame.getPlace()
        if place:
            # this sound is only used in certain locations but a hacked client can request that it be
            # played at any time, even before this client has downloaded a location that supports it
            if hasattr(place.loader, 'submergeSound'):
                base.playSfx(place.loader.submergeSound, node=self)

    def d_playSplashEffect(self, x, y, z):
        # Placeholder parameter to avoid server crash
        self.sendUpdate("playSplashEffect", [x, y, z])

    ### setTrackAccess ###

    def setTrackAccess(self, trackArray):
        self.trackArray = trackArray
        # update the inventory gui
        if self.inventory:
            self.inventory.updateGUI()

    def getTrackAccess(self):
        return self.trackArray


    def hasTrackAccess(self, track):
        """
        Can this toon use this track?
        Returns bool 0/1
        """
        return self.trackArray[track]

    ### setTrackProgress ###

    def setTrackProgress(self, trackId, progress):
        """
        Update your progress training trackId. TrackId is an index into
        ToontownBattleGlobals.Tracks and progress is a bitarray of progress
        markers gathered. A trackId of -1 means you are not training any track.
        """
        assert self.notify.debug("setting track %s progress to %s" % (trackId, progress))
        self.trackProgressId = trackId
        self.trackProgress = progress
        # update the track page
        if hasattr(self, 'trackPage'):
            self.trackPage.updatePage()

    def getTrackProgress(self):
        return [self.trackProgressId, self.trackProgress]

    def getTrackProgressAsArray(self, maxLength = 15):
        shifts = map(operator.rshift, maxLength * [self.trackProgress], \
                     range(maxLength - 1, -1, -1))
        digits = map(operator.mod, shifts, maxLength * [2])
        digits.reverse()
        return digits
       
    ### setTeleportAccess ###

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


    def setQuestHistory(self, questList):
        assert self.notify.debug("setting quest history to %s" % questList)
        self.questHistory = questList

    def getQuestHistory(self):
        return self.questHistory

    def setRewardHistory(self, rewardTier, rewardList):
        assert self.notify.debug("setting reward history to %s" % rewardList)
        self.rewardTier = rewardTier
        self.rewardHistory = rewardList

    def getRewardHistory(self):
        return self.rewardTier, self.rewardHistory


    ### overridden from DistributedSmoothNode ###

    def doSmoothTask(self, task):
        # We override doSmoothTask() instead of smoothPosition(), to
        # save on the overhead of one additional Python call.  And we
        # don't call up to the base class for the same reason.

        self.smoother.computeAndApplySmoothPosHpr(self, self)
        self.setSpeed(self.smoother.getSmoothForwardVelocity(),
                      self.smoother.getSmoothRotationalVelocity())
        return Task.cont

    # this is here to ensure that the correct overloaded method is called
    def d_setParent(self, parentToken):
        DistributedSmoothNode.DistributedSmoothNode.d_setParent(self,
                                                                parentToken)

    ### setEmoteAccess
    def setEmoteAccess(self, bits):
        assert self.notify.debug("setting Emote access to %s" % bits)
        self.emoteAccess = bits
        
        if self == base.localAvatar:
            messenger.send("emotesChanged")

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
    
    ### goHome
    #def b_goHome(self, zoneId):
    #    timestamp = globalClockDelta.getFrameNetworkTime()
    #    self.goHome(timestamp, zoneId)
    #    self.d_goHome(zoneId)

    #def d_goHome(self, zoneId):
    #    timestamp = globalClockDelta.getFrameNetworkTime()
    #    print "i'm going to request my estate zone"
    #    self.sendUpdate("requestEstateZone", [timestamp, zoneId])

    #def goHome(self, timestamp, zoneId):
    #    print "i'm going loco on the client"

    def b_setSpeedChatStyleIndex(self, index):
        realIndexToSend = 0
        if type(index) == type(0) and \
           0 <= index and index < len(speedChatStyles):
            realIndexToSend = index
        else:
            base.cr.centralLogger.writeClientEvent('Hacker alert b_setSpeedChatStyleIndex invalid')
        self.setSpeedChatStyleIndex(realIndexToSend)
        self.d_setSpeedChatStyleIndex(realIndexToSend)
        return None # I don't know why we return None here

    def d_setSpeedChatStyleIndex(self, index):
        realIndexToSend = 0
        if type(index) == type(0) and \
           0 <= index and index < len(speedChatStyles):
            realIndexToSend = index
        else:
            base.cr.centralLogger.writeClientEvent('Hacker alert d_setSpeedChatStyleIndex invalid')
        self.sendUpdate("setSpeedChatStyleIndex", [realIndexToSend])

    def setSpeedChatStyleIndex(self, index):
        realIndexToUse = 0
        if type(index) == type(0) and \
            0 <= index and index < len(speedChatStyles):
            realIndexToUse = index
        else:
            base.cr.centralLogger.writeClientEvent('Hacker victim setSpeedChatStyleIndex invalid attacking toon = %d' % self.doId)
        self.speedChatStyleIndex = realIndexToUse
        # update the background color for our text
        nameKey, arrowColor, rolloverColor, frameColor = \
              speedChatStyles[realIndexToUse]
        self.nametag.setQtColor(
            VBase4(frameColor[0], frameColor[1], frameColor[2], 1))

        if self.isLocal():
            messenger.send("SpeedChatStyleChange", [])

    def getSpeedChatStyleIndex(self):
        return self.speedChatStyleIndex

    ### setMaxMoney ###
    
    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    ### setMoney ###

    def setMoney(self, money):
        if money != self.money:
            self.money = money
            messenger.send(self.uniqueName("moneyChange"), [self.money])
        
    def getMoney(self):
        return self.money

    ### setMaxBankMoney ###

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney

    ### setBankMoney ###

    def setBankMoney(self, money):
        self.bankMoney = money
        messenger.send(self.uniqueName("bankMoneyChange"), [self.bankMoney])

    def getBankMoney(self):
        return self.bankMoney

    def getTotalMoney(self):
        return self.getBankMoney() + self.getMoney()


    ### Tossing a pie (used in final Boss Battle sequence)

    def presentPie(self, x, y, z, h, p, r, timestamp32):
        if self.numPies <= 0:
            # Someone's tossing pies who doesn't have any.
            return
        
        if not launcher.getPhaseComplete(5):
            # We haven't downloaded the pies yet (which are in
            # phase_5, the battle phase), so don't try to show them.
            return

        lastTossTrack = Sequence()
        if self.tossTrack:
            lastTossTrack = self.tossTrack
            tossTrack = None
            
        ts = globalClockDelta.localElapsedTime(timestamp32, bits = 32)

        # Delay the toss by the same amount of time as the smoothing
        # delay, so it will be in sync with the running animation.
        ts -= self.smoother.getDelay()
        ival = self.getPresentPieInterval(x, y, z, h, p, r)

        if (ts > 0):
            # We're already late.
            startTime = ts
            lastTossTrack.finish()
        else:
            # We need to wait a bit.
            ival = Sequence(Wait(-ts),
                            #Func(lastTossTrack.finish),
                            ival)

            # It seems we need to explicitly finish the lastTossTrack
            # now to prevent a hard crash.  Maybe a Python refcount
            # bug?  Investigate later.
            lastTossTrack.finish()
            startTime = 0

        # Naming these intervals turns out to be a really bad idea for
        # now--the CIntervalManager doesn't properly handle this case.
        # Investigate later.
        #ival = Sequence(ival, name = self.uniqueName('presentPie'))
        ival = Sequence(ival)
        ival.start(startTime)
        self.tossTrack = ival

    def tossPie(self, x, y, z, h, p, r, sequence, power, timestamp32):
        if self.numPies <= 0:
            # Someone's tossing pies who doesn't have any.
            return

        # Update this on the client just so we can more accurately
        # validate a volley of pies at once.  The AI will send the
        # official update later.
        if self.numPies != ToontownGlobals.FullPies:
            self.setNumPies(self.numPies - 1)
        self.lastTossedPie = globalClock.getFrameTime()
        
        if not launcher.getPhaseComplete(5):
            # We haven't downloaded the pies yet (which are in
            # phase_5, the battle phase), so don't try to show them.
            return

        lastTossTrack = Sequence()
        if self.tossTrack:
            lastTossTrack = self.tossTrack
            tossTrack = None

        lastPieTrack = Sequence()
        if self.pieTracks.has_key(sequence):
            lastPieTrack = self.pieTracks[sequence]
            del self.pieTracks[sequence]
            
        ts = globalClockDelta.localElapsedTime(timestamp32, bits = 32)

        # Delay the toss by the same amount of time as the smoothing
        # delay, so it will be in sync with the running animation.
        ts -= self.smoother.getDelay()
        toss, pie, flyPie = self.getTossPieInterval(x, y, z, h, p, r, power)

        if (ts > 0):
            # We're already late.
            startTime = ts
            lastTossTrack.finish()
            lastPieTrack.finish()
        else:
            # We need to wait a bit.
            toss = Sequence(Wait(-ts),
                           #Func(lastTossTrack.finish),
                           toss)
            pie = Sequence(Wait(-ts),
                           #Func(lastPieTrack.finish),
                           pie)

            # It seems we need to explicitly finish the lastTossTrack
            # now to prevent a hard crash.  Maybe a Python refcount
            # bug?  Investigate later.
            lastTossTrack.finish()
            lastPieTrack.finish()
            startTime = 0

        # Naming these intervals turns out to be a really bad idea for
        # now--the CIntervalManager doesn't properly handle this case.
        # Investigate later.
        #ival = Sequence(ival, name = self.uniqueName('tossPie'))
        self.tossTrack = toss
        toss.start(startTime)
        pie = Sequence(pie, Func(self.pieFinishedFlying, sequence))
        self.pieTracks[sequence] = pie
        pie.start(startTime)

    def pieFinishedFlying(self, sequence):
        if self.pieTracks.has_key(sequence):
            del self.pieTracks[sequence]

    def pieFinishedSplatting(self, sequence):
        if self.splatTracks.has_key(sequence):
            del self.splatTracks[sequence]

    def pieSplat(self, x, y, z, sequence, pieCode, timestamp32):
        if self.isLocal():
            # LocalToon ignores this message; he tosses his own pies.
            return

        elapsed = globalClock.getFrameTime() - self.lastTossedPie
        if elapsed > 30:
            # Can't make a splat if you didn't toss a pie.
            return

        if not launcher.getPhaseComplete(5):
            # We haven't downloaded the pies yet (which are in
            # phase_5, the battle phase), so don't try to show them.
            return

        lastPieTrack = Sequence()
        if self.pieTracks.has_key(sequence):
            lastPieTrack = self.pieTracks[sequence]
            del self.pieTracks[sequence]

        if self.splatTracks.has_key(sequence):
            lastSplatTrack = self.splatTracks[sequence]
            del self.splatTracks[sequence]
            lastSplatTrack.finish()
            
        ts = globalClockDelta.localElapsedTime(timestamp32, bits = 32)

        # Delay the splat by the same amount of time as the smoothing
        # delay, so it will be in sync with the toss animation.
        ts -= self.smoother.getDelay()
        splat = self.getPieSplatInterval(x, y, z, pieCode)

        splat = Sequence(Func(messenger.send, 'pieSplat', [self, pieCode]),
                         splat)

        if (ts > 0):
            # We're already late.
            startTime = ts
            lastPieTrack.finish()
        else:
            # We need to wait a bit.
            splat = Sequence(Wait(-ts),
                             #Func(lastPieTrack.finish),
                             splat)

            # It seems we need to explicitly finish the lastTossTrack
            # now to prevent a hard crash.  Maybe a Python refcount
            # bug?  Investigate later.
            #lastPieTrack.finish()
            startTime = 0

        # Naming these intervals turns out to be a really bad idea for
        # now--the CIntervalManager doesn't properly handle this case.
        # Investigate later.
        splat = Sequence(splat,
                         Func(self.pieFinishedSplatting, sequence))
                         #name = self.uniqueName('pieSplat'))
        self.splatTracks[sequence] = splat
        splat.start(startTime)


    def cleanupPies(self):
        # Make sure the pie is not in our hand or flying through the air.
        for track in self.pieTracks.values():
            track.finish()
        self.pieTracks = {}
        for track in self.splatTracks.values():
            track.finish()
        self.splatTracks = {}
        self.cleanupPieInHand()

    def cleanupPieInHand(self):
        # Make sure the pie is not parented to our hand.
        if self.tossTrack:
            self.tossTrack.finish()
            self.tossTrack = None

        self.cleanupPieModel()

    def setNumPies(self, numPies):
        self.numPies = numPies
        if self.isLocal():
            self.updatePieButton()
            if numPies == 0:
                self.interruptPie()

    def setPieType(self, pieType):
        self.pieType = pieType
        if self.isLocal():
            self.updatePieButton()

    def setTrophyScore(self, score):
        self.trophyScore = score

        # Update the floating star over our head that we earn for
        # having a certain trophy score.
        
        if self.trophyStar != None:
            self.trophyStar.removeNode()
            self.trophyStar = None

        if self.trophyStarSpeed != 0:
            taskMgr.remove(self.uniqueName("starSpin"))
            self.trophyStarSpeed = 0
            
        if hasattr(self, 'gmIcon') and self.gmIcon:
            return

        if self.trophyScore >= ToontownGlobals.TrophyStarLevels[4]:
            # A gold star!
            self.trophyStar = loader.loadModel('phase_3.5/models/gui/name_star')
            self.trophyStar.reparentTo(self.nametag.getNameIcon())
            self.trophyStar.setScale(2)
            self.trophyStar.setZ(2)
            self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[4])
            self.trophyStarSpeed = 15
            if self.trophyScore >= ToontownGlobals.TrophyStarLevels[5]:
                # Spinning!
                taskMgr.add(self.__starSpin, self.uniqueName("starSpin"))
        elif self.trophyScore >= ToontownGlobals.TrophyStarLevels[2]:
            # A silver star!
            self.trophyStar = loader.loadModel('phase_3.5/models/gui/name_star')
            self.trophyStar.reparentTo(self.nametag.getNameIcon())
            self.trophyStar.setScale(1.5)
            self.trophyStar.setZ(1.6)
            self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[2])
            self.trophyStarSpeed = 10
            if self.trophyScore >= ToontownGlobals.TrophyStarLevels[3]:
                # Spinning!
                taskMgr.add(self.__starSpin, self.uniqueName("starSpin"))
        elif self.trophyScore >= ToontownGlobals.TrophyStarLevels[0]:
            # A bronze star.
            self.trophyStar = loader.loadModel('phase_3.5/models/gui/name_star')
            self.trophyStar.reparentTo(self.nametag.getNameIcon())
            self.trophyStar.setScale(1.5)
            self.trophyStar.setZ(1.6)
            self.trophyStar.setColor(ToontownGlobals.TrophyStarColors[0])
            self.trophyStarSpeed = 8
            if self.trophyScore >= ToontownGlobals.TrophyStarLevels[1]:
                # Spinning!
                taskMgr.add(self.__starSpin, self.uniqueName("starSpin"))

    def __starSpin(self, task):
        now = globalClock.getFrameTime()
        r = now * self.trophyStarSpeed % 360.0
        self.trophyStar.setR(r)
        return Task.cont

    def getZoneId(self):
        """returns actual zone that toon is currently in"""
        place = base.cr.playGame.getPlace()
        if place:
            return place.getZoneId()
        else:
            return None

    def getRequestID(self):
        return CLIENT_GET_AVATAR_DETAILS

    def announceBingo(self):
        #this message is passed by the ai when the toon should say "Bingo!"
        self.setChatAbsolute(TTLocalizer.FishBingoBingo, CFSpeech|CFTimeout)

    def squish(self, damage):
        if self == base.localAvatar:
            base.cr.playGame.getPlace().fsm.request('squished')
            self.stunToon()
            self.setZ(self.getZ(render)+.025)

    def d_squish(self, damage):
        self.sendUpdate("squish", [damage])
        
    def b_squish(self, damage):
        if not self.isStunned:
            self.squish(damage)
            self.d_squish(damage)
            self.playDialogueForString("!")

    def getShadowJoint(self):
        """
        Return the shadow joint
        """
        return Toon.Toon.getShadowJoint(self)

    if base.wantKarts:
        def hasKart( self ):
            """
            Purpose: The hasKart Method determines whether the Toon
            currently owns a kart.

            Params: None
            Return: Bool - True or False
            """
            return ( self.kartDNA[ KartDNA.bodyType ] != -1 )

        def getKartDNA( self ):
            """
            Purpose: The getKartDNA Method obtains the kart dna for the
            toon.

            Params: None
            Return: [] - the kart dna.
            """
            return self.kartDNA

        def setTickets( self, numTickets ):
            """
            Purpose: The setTickets Method sets the number of tickets a toon has.
            Tickets are gained by winning races and events.

            Params: numTickets - the new nubmer of tickets
            Return: None
            """
            self.tickets = numTickets

        def getTickets( self ):
            """
            Purpose: The getTickets Method obtains the number of
            tickets that a toon can has.

            Params: None
            Return: tickets
            """
            return self.tickets

        def getAccessoryByType( self, accType ):
            """
            Purpose: TODO - write this

            Params: None
            Return: None
            """
            return self.kartDNA[ accType ]

        def setCurrentKart(self,avId):
            self.kartId=avId
            
        def releaseKart(self):
            self.kartId=None

        def setKartBodyType( self, bodyType ):
            """
            Purpose: The setKartBodyType Method sets the local client side
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

        def setKartBodyColor( self, bodyColor ):
            """
            Purpose: The d_setKartBodyColor Method appropriately sets
            the body color of the lient on the client side by updating the
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

        def setKartAccessoryColor( self, accColor ):
            """
            Purpose: The setKartAccessoryColor Method appropriately sets
            the accessory color of the local client side by updating the kart
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

        def setKartRimType( self, rimsType ):
            """
            Purpose: The setKartRimType Method sets the rims accessory
            for the karts tires by updating the Kart DNA.

            Params: rimsType - the type of rims for the kart tires.
            Return: None
            """
            self.kartDNA[ KartDNA.rimsType ] = rimsType

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

        def getKartRimType( self ):
            """
            Purpose: The setKartRimType Method sets the rims accessory
            for the karts tires by accessing the Kart DNA.
            
            Params: None
            Return: rimsType - the type of rims for the kart tires.
            """
            return self.kartDNA[ KartDNA.rimsType ]

        def setKartAccessoriesOwned( self, accessories ):
            """
            Purpose: The setKartAccessoriesOwned Method properly sets the
            Accessories owned by the toon on the client side.

            Params: accessories - the ids of the accessories owned.
            Return: None
            """
            #if this list is shorter than 16, make it 16
            while len(accessories) < 16:
                accessories.append(-1)
          
            assert ( len( accessories ) == 16 ), "DistrubtedToon::setKartAccessoriesOwned - len( accessories != 16 )"
            self.accessories = accessories

        def getKartAccessoriesOwned( self ):
            """
            Purpose: The getKartAccessoriesOwned Method retrieves the
            accessories that are owned by the toon on the client side.

            Params: None
            Return: [] - List of Accessories owned by the toon.
            """
            owned = copy.deepcopy(self.accessories)
            while InvalidEntry in owned:
                owned.remove(InvalidEntry)
            return owned

        def requestKartDNAFieldUpdate( self, dnaField, fieldValue ):
            """
            Purpose: The requestAccessoryUpdate Method sends a distributed
            message request to the AI to update the accessory of a
            particular type.

            Params: accessoryType - the kind of accessory to update
                    accessoryId - the new accessory id.
            Return: None
            """
            self.notify.debug( "requestKartDNAFieldUpdate - dnaField %s, fieldValue %s" % ( dnaField, fieldValue ) )
            self.sendUpdate( "updateKartDNAField", [ dnaField, fieldValue ] )            

        def requestAddOwnedAccessory( self, accessoryId ):
            """
            Purpose: The requestAddOwnedAccessory Method sends a distributed
            message request to the AI to add a new accessory to the toon's
            owned accessory list.

            Params: accessoryId - the id of the accessory that has been purchased.
            Return: None
            """
            self.notify.debug( "requestAddOwnedAccessor - purchased accessory %s" % ( accessoryId ) )
            self.sendUpdate( "addOwnedAccessory", [ accessoryId ] )

        def requestRemoveOwnedAccessory( self, accessoryId ):
            """
            Purpose: The requestRemoveOwnedAccessory Method sends a distributed
            message request to the AI to remove an accessory from the toon's
            owned accessory list.

            Params: accessoryId - the id of the accessory that should be removed.
            Return: None
            """
            self.notify.debug( "requestRemoveOwnedAccessor - removed accessory %s" % ( accessoryId ) )
            self.sendUpdate( "removeOwnedAccessory", [ accessoryId ] )

        ## Karting trophy list
        def setKartingTrophies(self, trophyList):
            assert self.notify.debug("setting kart trophies to %s" % trophyList)
            self.kartingTrophies = trophyList
        
        def getKartingTrophies(self):
            return self.kartingTrophies

        ## Karting history list
        def setKartingHistory(self, history):
            assert self.notify.debug("setting kart history to %s" % history)
            self.kartingHistory = history
        
        def getKartingHistory(self):
            return self.kartingHistory

        ## Karting personal best list
        def setKartingPersonalBest(self, bestTimes):
            assert self.notify.debug("setting kart personal best to %s" % bestTimes)
            self.kartingPersonalBest = bestTimes
        
        def getKartingPersonalBest(self):
            return self.kartingPersonalBest

        def setKartingPersonalBest2(self, bestTimes2):
            assert self.notify.debug("setting kart personal best to %s" % bestTimes2)
            self.kartingPersonalBest2 = bestTimes2

        def getKartingPersonalBest2(self):
            return self.kartingPersonalBest2

        def getKartingPersonalBestAll(self):
            return self.kartingPersonalBest + \
                   self.kartingPersonalBest2

    if hasattr(base, 'wantPets') and base.wantPets:
        def setPetId(self, petId):
            self.petId = petId
            if petId == 0:
                self.petDNA = None
            elif self.isLocal():
                # make sure to add the pet to the friendsMap
                base.cr.addPetToFriendsMap()

        def getPetId(self):
            return self.petId

        def getPetId(self):
            return self.petId

        def hasPet(self):
            #print str(self.petId)
            return  (self.petId != 0)

        def b_setPetTutorialDone(self, bDone):
            self.d_setPetTutorialDone(bDone)
            self.setPetTutorialDone(bDone)
        def d_setPetTutorialDone(self, bDone):
            self.sendUpdate('setPetTutorialDone', [bDone])
        def setPetTutorialDone(self, bDone):
            self.bPetTutorialDone = bDone

        def b_setFishBingoTutorialDone(self, bDone):
            self.d_setFishBingoTutorialDone(bDone)
            self.setFishBingoTutorialDone(bDone)
        def d_setFishBingoTutorialDone(self, bDone):
            self.sendUpdate('setFishBingoTutorialDone', [bDone])
        def setFishBingoTutorialDone(self, bDone):
            self.bFishBingoTutorialDone = bDone

        def b_setFishBingoMarkTutorialDone(self, bDone):
            self.d_setFishBingoMarkTutorialDone(bDone)
            self.setFishBingoMarkTutorialDone(bDone)
        def d_setFishBingoMarkTutorialDone(self, bDone):
            self.sendUpdate('setFishBingoMarkTutorialDone', [bDone])
        def setFishBingoMarkTutorialDone(self, bDone):
            self.bFishBingoMarkTutorialDone = bDone

        def b_setPetMovie(self, petId, flag):
            self.d_setPetMovie(petId, flag)
            self.setPetMovie(petId, flag)
        def d_setPetMovie(self, petId, flag):
            self.sendUpdate('setPetMovie', [petId, flag])
        def setPetMovie(self, petId, flag):
            pass

        def lookupPetDNA(self):

            # If self.petId is not 0 but self.petDNA is None, this
            # sends a requst to the server to go look up our pet's
            # DNA.

            # self.petDNA will then be filled in at some unspecified
            # time after lookupPetDNA() has been called.  You don't
            # even get a callback, so you should be prepared for
            # self.petDNA to still be None by the time you need it.

            if self.petId and not self.petDNA:
                from toontown.pets import PetDetail
                PetDetail.PetDetail(self.petId, self.__petDetailsLoaded)
        def __petDetailsLoaded(self, pet):
            self.petDNA = pet.style

    def trickOrTreatTargetMet(self,beanAmount):
        if(self.effect):
            self.effect.stop()
            
        self.effect = TrickOrTreatTargetEffect(beanAmount)
        self.effect.play()

        
    def trickOrTreatMilestoneMet(self):
        if(self.effect):
            self.effect.stop()
            
        self.effect = TrickOrTreatMilestoneEffect()
        self.effect.play()
        
    def winterCarolingTargetMet(self, beanAmount):
        if(self.effect):
            self.effect.stop()
            
        self.effect = WinterCarolingEffect(beanAmount)
        self.effect.play()

    def d_reqCogSummons(self, type, suitIndex):
        if type == 'single':
            pass
        elif type == 'building':
            pass
        elif type == 'invasion':
            pass
        self.sendUpdate("reqCogSummons", [type, suitIndex])

    def cogSummonsResponse(self, returnCode, suitIndex, doId):
        messenger.send("cog-summons-response", [returnCode, suitIndex, doId])

    def setCogSummonsEarned(self, cogSummonsEarned):
        self.cogSummonsEarned = cogSummonsEarned

    def getCogSummonsEarned(self):
        return self.cogSummonsEarned

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



    #////////////////// Gardening Estates Expansion
    # Flower collection
    def setFlowerCollection(self, speciesList, varietyList):
        self.flowerCollection = FlowerCollection.FlowerCollection()
        self.flowerCollection.makeFromNetLists( speciesList, varietyList)

    def getFlowerCollection(self):
        return self.flowerCollection

    ## Max flower basket
    def setMaxFlowerBasket(self, maxFlowerBasket):
        self.maxFlowerBasket = maxFlowerBasket

    def getMaxFlowerBasket(self):
        return self.maxFlowerBasket

    def isFlowerBasketFull(self):
        """
        Return 1 if the flower basket if full to capacity
        Return 0 if there is room for more flower
        """
        return (len(self.flowerBasket) >= self.maxFlowerBasket)
    

    ## Flower Basket
    def setFlowerBasket(self, speciesList, varietyList):
        self.flowerBasket = FlowerBasket.FlowerBasket()
        self.flowerBasket.makeFromNetLists(speciesList, varietyList)
        messenger.send("flowerBasketUpdated")

    def getFlowerBasket(self):
        return self.flowerBasket

    ## Shovel
    def setShovel(self, shovelId):
        self.shovel = shovelId

    def attachShovel(self):
        self.shovelModel = self.getShovelModel()
        self.shovelModel.reparentTo(self.rightHand)
        return self.shovelModel

    def detachShovel(self):
        if self.shovelModel:
            self.shovelModel.removeNode()
    
    def getShovelModel(self):
        shovels = loader.loadModel('phase_5.5/models/estate/shovels')
        shovelId = ['A','B','C','D'][self.shovel]
        shovel = shovels.find('**/shovel' + shovelId)

        shovel.setH(-90)
        shovel.setP(216)
        shovel.setX(0.2)

        #these values came from Richard
        #shovel.setH(62.0) #rotx
        #shovel.setP(85.7) #roty
        #shovel.setR(-158.86) #rotz

        shovel.detachNode()
        shovels.removeNode()
        return shovel
        
    ## ShovelSkill
    def setShovelSkill(self, skillLevel):
        self.shovelSkill = skillLevel

    def getBoxCapability(self):
        """
        based on his shovel and his current shovel skill,
        how many jelly beans can we use
        """
        return GardenGlobals.getShovelPower(self.shovel, self.shovelSkill)
                                         
    ## WateringCan
    def setWateringCan(self, wateringCanId):
        self.wateringCan = wateringCanId

    def attachWateringCan(self):
        self.wateringCanModel = self.getWateringCanModel()
        self.wateringCanModel.reparentTo(self.rightHand)
        return self.wateringCanModel

    def detachWateringCan(self):
        if self.wateringCanModel:
            self.wateringCanModel.removeNode()
        #if hasattr(self,'debugAxis'):
        #    self.debugAxis.removeNode()

    
    def getWateringCanModel(self):
        #if not hasattr(self,'debugAxis'):
        #    self.debugAxis = loader.loadModel('models/misc/xyzAxis')
        #    self.debugAxis.reparentTo(self.rightHand)

                                 #s   x y z    h  p  r    
        scalePosHprsTable = ( (0.25, 0.1, 0 ,0.2,  -90,-125, -45),
                              (0.2, 0.0, 0.25 ,0.2,  -90,-125, -45),
                              (0.2, 0.2, 0.1 ,0.2,  -90,-125, -45),
                              (0.2, 0.0, 0.25 ,0.2,  -90,-125, -45),)        
        
        cans = loader.loadModel('phase_5.5/models/estate/watering_cans')
        canId = ['A','B','C','D'][self.wateringCan]
        can = cans.find('**/water_can' + canId)
        
        can.setScale(scalePosHprsTable[self.wateringCan][0])
        can.setPos( scalePosHprsTable[self.wateringCan][1],
                    scalePosHprsTable[self.wateringCan][2],
                    scalePosHprsTable[self.wateringCan][3])
        can.setHpr( scalePosHprsTable[self.wateringCan][4],
                    scalePosHprsTable[self.wateringCan][5],
                    scalePosHprsTable[self.wateringCan][6])
                    
        
        can.detachNode()
        cans.removeNode()


        if hasattr(base,'rwc'):
            if base.rwc:
                if hasattr(self,'wateringCan2'):
                    self.wateringCan2.removeNode()
                self.wateringCan2 = can.copyTo(self.rightHand)
                #self.wateringCan2.reparentTo(self.rightHand)
            else:
                self.wateringCan2.removeNode()
 
   
        return can
        
    ## WateringCanSkill
    def setWateringCanSkill(self, skillLevel):
        self.wateringCanSkill = skillLevel

    ## GardenSpecials
    def setGardenSpecials(self, specials):
        self.gardenSpecials = specials

        # update the garden page
        if hasattr(self, 'gardenPage') and self.gardenPage:
            self.gardenPage.updatePage()        

    def getGardenSpecials(self):
        return self.gardenSpecials

    def getMyTrees(self):
        treeDict = self.cr.getObjectsOfClass(DistributedGagTree.DistributedGagTree)
        trees = []
        for tree in treeDict.values():
            if tree.getOwnerId() == self.doId:
                trees.append(tree)

        if not trees:
            # what happens when the trees aren;t around right now?
            pass

        return trees

    def isTreePlanted(self, track, level):
        trees = self.getMyTrees()
        for tree in trees:
            if tree.gagTrack == track and tree.gagLevel == level:
                return True

        return False

    def doIHaveRequiredTrees(self, track, level):
        """
        When planting a level 4 gag tree, make sure we have the level 1, 2, and 3 gag tree
        """
        trees = self.getMyTrees()
        trackAndLevelList = []
        for tree in trees:
            trackAndLevelList.append( (tree.gagTrack, tree.gagLevel) )

        haveRequired = True
        
        for curLevel in range(level):
            testTuple = (track, curLevel)
            if not testTuple in trackAndLevelList:
                haveRequired=False
                break

        return haveRequired
        
        
    ### setTrackBonusLevel ###

    def setTrackBonusLevel(self, trackArray):
        self.trackBonusLevel = trackArray
        # update the inventory gui
        if self.inventory:
            self.inventory.updateGUI()

    def getTrackBonusLevel(self, track=None):
        if track == None:
            return self.trackBonusLevel
        else:
            return self.trackBonusLevel[track]

    def checkGagBonus(self, track, level):
        trackBonus = self.getTrackBonusLevel(track)
        return (trackBonus >= level)
            
    ## Garden trophy List
    def setGardenTrophies(self, trophyList):
        assert self.notify.debug("setting fish trophies to %s" % trophyList)
        self.gardenTrophies = trophyList
        
    def getGardenTrophies(self):
        return self.gardenTrophies

    def useSpecialResponse(self, returnCode):
        messenger.send("use-special-response", [returnCode])


    def setGardenStarted(self, bStarted):
        self.gardenStarted = bStarted
        #if hasattr(self, 'gardenPage'):
        #    self.gardenPage.updatePage()
        
    def getGardenStarted(self):
        return self.gardenStarted
        
    def sendToGolfCourse(self, zoneId):
        print("sending to golfCourse")
        hoodId = self.cr.playGame.hood.hoodId
        golfRequest = {
            "loader": "safeZoneLoader",
            "where": "golfcourse",
            "how" : "teleportIn",
            "hoodId" : hoodId,
            "zoneId" : zoneId,
            "shardId" : None,
            "avId" : -1,
        }
        base.cr.playGame.getPlace().requestLeave(golfRequest)

    def getGolfTrophies(self):
        """Get the golf trophies this toon has won."""
        return self.golfTrophies

    def getGolfCups(self):
        """Get the golf cups this toon has won. 10 trophies awards you 1 cup."""
        return self.golfCups

    ## Golf history list
    def setGolfHistory(self, history):
        assert self.notify.debug("setting golf history to %s" % history)
        self.golfHistory = history

        # update our trophies and cups too
        self.golfTrophies =  GolfGlobals.calcTrophyListFromHistory(self.golfHistory)
        self.golfCups = GolfGlobals.calcCupListFromHistory(self.golfHistory)

        # if case we have just finished our first game...
        if hasattr(self, 'book'):
            self.addGolfPage()
        
    def getGolfHistory(self):
        return self.golfHistory

    def hasPlayedGolf(self):
        """Returns True if this toon has ever played golf."""
        retval = False
        for historyValue in self.golfHistory:
            if historyValue:
                retval = True;
                break
        return retval

    def setPackedGolfHoleBest(self, packedHoleBest):
        """Set the packed personal hole best on the client."""
        unpacked = GolfGlobals.unpackGolfHoleBest(packedHoleBest)
        self.setGolfHoleBest(unpacked)

    def setGolfHoleBest(self, holeBest):
        """Set the personal hole best on the client."""
        self.golfHoleBest = holeBest

    def getGolfHoleBest(self):
        """Return the personal hole best."""
        return self.golfHoleBest

    def setGolfCourseBest(self, courseBest):
        """Set the personal course best on the client."""
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

    def getPinkSlips(self):
        if hasattr(self, "pinkSlips"):
            return self.pinkSlips
        else:
            return 0

    def setPinkSlips(self, pinkSlips):
        """Set the number of pink slips."""
        self.pinkSlips = pinkSlips
        
    def setAccess(self, access):
        self.setGameAccess(access)
        self.setDisplayName(self.getName()) #fancy nametag
        #if access == OTPGlobals.AccessFull:  
        #     base.cr.setIsPaid(1)
        #elif access == OTPGlobals.AccessVelvetRope
        #    base.cr.setIsPaid(0)
        #else:
        #    base.cr.setIsPaid(0)
        
    def setGameAccess(self, access):
        self.gameAccess = access
        
    def getGameAccess(self):
        if hasattr(self, "gameAccess"):
            return self.gameAccess
        else:
            return 0
        
   # Name Tag Styles
   
    def setDisplayName(self, str):
        if(self.getGameAccess() == OTPGlobals.AccessFull) and (not self.isDisguised):
            self.setFancyNametag(name = str)
        else:
            self.removeFancyNametag()
            Avatar.Avatar.setDisplayName(self, str)
            
            
    def setFancyNametag(self, name = None):
   
        if name == None:
            name = self.getName()
        #font = ToontownGlobals.getToonFont()
        #self.setFont(font)
        #Avatar.Avatar.setDisplayName(self, name)
        if self.getNametagStyle() == 100:
            self.setFont(ToontownGlobals.getToonFont())
        else:
            self.setFont(ToontownGlobals.getNametagFont(self.getNametagStyle()))
        #self.nametag.setShadow(0.03,0.03)
        Avatar.Avatar.setDisplayName(self, name)
        self.setFont(ToontownGlobals.getToonFont())
        
        
    def removeFancyNametag(self):
        self.nametag.clearShadow()
        pass
        
    def getNametagStyle(self):
        if hasattr(self, "nametagStyle"):
            return self.nametagStyle
        else:
            return 0

    def setNametagStyle(self, nametagStyle):
        """Set the nametag style."""
        if hasattr(self, 'gmToon') and self.gmToon:
            return
        
        # Force a font that has numbers.
        if base.config.GetBool('want-nametag-avids', 0):
            nametagStyle = 0
        
        self.nametagStyle = nametagStyle
        self.setDisplayName(self.getName())

    
    def getAvIdName(self):
        # Add F (Free) or P (Paid) to want-avid-tags suggested by Red for avatar ID tags.
        paidStr = PythonUtil.choice(self.getGameAccess() == OTPGlobals.AccessFull, "P", "F")
        return "%s\n%s (%s)" % (self.getName(), self.doId, paidStr)
        
    def playCurrentDialogue(self, dialogue, chatFlags, interrupt = 1):
        if interrupt and (self.__currentDialogue is not None):
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        # If an AudioSound has been passed in, play that for dialog to
        # go along with the chat.  Interrupt any sound effect currently playing
        if dialogue:
            base.playSfx(dialogue, node=self)
        # If it is a speech-type chat message, and the avatar isn't
        # too far away to hear, play the appropriate sound effect.
        elif (chatFlags & CFSpeech) != 0:
            if (self.nametag.getNumChatPages() > 0):
                # play the dialogue sample

                # We use getChat() instead of chatString, which
                # returns just the current page of a multi-page chat
                # message.  This way we aren't fooled by long pages
                # that end in question marks.
                self.playDialogueForString(self.nametag.getChat())
                if (self.soundChatBubble != None):
                    base.playSfx(self.soundChatBubble, node=self)
            elif (self.nametag.getChatStomp() > 0 ):
                self.playDialogueForString(self.nametag.getStompText(), self.nametag.getStompDelay())
    
    def playDialogueForString(self, chatString, delay = 0.0):
        """
        Play dialogue samples to match the given chat string
        """
        if len(chatString) == 0:
            return
        # use only lower case for searching
        searchString = chatString.lower()
        # determine the statement type
        if (searchString.find(OTPLocalizer.DialogSpecial) >= 0):
            # special sound
            type = "special"
        elif (searchString.find(OTPLocalizer.DialogExclamation) >= 0):
            #exclamation
            type = "exclamation"
        elif (searchString.find(OTPLocalizer.DialogQuestion) >= 0):
            # question
            type = "question"
        else:
            # statement (use two for variety)
            if random.randint(0, 1):
                type = "statementA"
            else:
                type = "statementB"

        # determine length
        stringLength = len(chatString)
        if (stringLength <= OTPLocalizer.DialogLength1):
            length = 1
        elif (stringLength <= OTPLocalizer.DialogLength2):
            length = 2
        elif (stringLength <= OTPLocalizer.DialogLength3):
            length = 3
        else:
            length = 4

        self.playDialogue(type, length, delay)

    def playDialogue(self, type, length, delay = 0.0):
        """playDialogue(self, string, int)
        Play the specified type of dialogue for the specified time
        """

        # Inheritors may override this function or getDialogueArray(),
        # above.
        
        # Choose the appropriate sound effect.
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        
        sfxIndex = None
        if (type == "statementA" or type == "statementB"):
            if (length == 1):
                sfxIndex = 0
            elif (length == 2):
                sfxIndex = 1
            elif (length >= 3):
                sfxIndex = 2
        elif (type == "question"):
            sfxIndex = 3
        elif (type == "exclamation"):
            sfxIndex = 4
        elif (type == "special"):
            sfxIndex = 5
        else:
            self.notify.error("unrecognized dialogue type: ", type)

        if sfxIndex != None and sfxIndex < len(dialogueArray) and \
           dialogueArray[sfxIndex] != None:
            soundSequence = Sequence(Wait(delay),
                            SoundInterval(dialogueArray[sfxIndex], node = None,
                                           listenerNode = base.localAvatar,
                                           loop = 0,
                                           volume = 1.0),
                                           )
            self.soundSequenceList.append(soundSequence)
            soundSequence.start()
            
            self.cleanUpSoundList()
            
    def cleanUpSoundList(self):
        removeList = []
        for soundSequence in self.soundSequenceList:
            if soundSequence.isStopped():
                removeList.append(soundSequence)
        
        for soundSequence in removeList:
            self.soundSequenceList.remove(soundSequence)
                
                                                            
    def sendLogMessage(self, message):
        self.sendUpdate("logMessage", [message])
        
    def setChatAbsolute(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        #isFiltered = 1
        #if isFiltered:
        #    cleanString = self.replaceBadWords(chatString)
        #    DistributedAvatar.DistributedAvatar.setChatAbsolute(self, cleanString, chatFlags, dialogue, interrupt)
        #else:
        DistributedAvatar.DistributedAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)
        #if not quiet:
        #    base.chatAssistant.receiveAvatarOpenTypedChat(chatString, chatFlags, self.doId)
            
    def setChatMuted(self, chatString, chatFlags, dialogue = None, interrupt = 1, quiet = 0):
        """
        This method is a modification of setChatAbsolute in Toontown in which
        just the text of the chat is displayed on the nametag.
        No animal sound is played along with it.
        """
        self.nametag.setChat(chatString, chatFlags)
        # Removing CFSpeech from the chatFlags so that the chat is muted.
        self.playCurrentDialogue(dialogue, (chatFlags - CFSpeech), interrupt)
    
    def displayTalk(self, chatString, mods = None):
        flags = CFSpeech | CFTimeout
        if base.talkAssistant.isThought(chatString):
            flags = CFThought
            chatString = base.talkAssistant.removeThoughtPrefix(chatString)
            
        self.nametag.setChat(chatString, flags)
        if base.toonChatSounds:
            self.playCurrentDialogue(None, flags, interrupt=1)
     
            
    def setMail(self, mail):
        """Set the mail"""
        DistributedToon.partyNotify.debug( "setMail called with %d mail items" % len(mail) )
        self.mail = []
        for i in xrange(len(mail)):
            oneMailItem = mail[i]
            newMail = SimpleMailBase(*oneMailItem)
            self.mail.append(newMail)
            assert self.notify.debug("mail[%d]= %s" % (i, newMail))
        #self.simpleMailNotify= ToontownGlobals.NewItems

        #if self.isLocal():
        #    self.gotCatalogNotify = 1
        #    self.refreshOnscreenButtons()        

    def setSimpleMailNotify(self, simpleMailNotify):
        """Handle the AI/Uberdog telling us if we have new, old, or no simple mail."""
        DistributedToon.partyNotify.debug( "setSimpleMailNotify( %s )" % simpleMailNotify )
        self.simpleMailNotify = simpleMailNotify

        if self.isLocal():
            self.gotCatalogNotify = 1
            self.refreshOnscreenButtons()

    def setInviteMailNotify(self, inviteMailNotify):
        """Handle the AI/Uberdog telling us if we have new, old, or no invite mail."""
        DistributedToon.partyNotify.debug( "setInviteMailNotify( %s )" % inviteMailNotify )
        self.inviteMailNotify = inviteMailNotify

        if self.isLocal():
            self.gotCatalogNotify = 1
            self.refreshOnscreenButtons()

    def setInvites( self, invites):
        """Handle uberdog telling us our invitations.
        This does not include invites we've already rejected."""
        DistributedToon.partyNotify.debug("setInvites called passing in %d invites." % len(invites))
        self.invites = []
        for i in xrange(len(invites)):
            oneInvite=invites[i]
            newInvite = InviteInfo(*oneInvite)
            self.invites.append(newInvite)
            assert self.notify.debug('self.invites[%d]= %s' % (i, newInvite))
        #self.updateInviteMailNotify() # we need to do this after we get partiesInvitedTo

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

    def getInvitesToShowInMailbox(self):
        """Return a list of inviteInfos that should be displayed in the mailbox."""
        # WARNING keep this in sync with DistributedToonAI.getInvitesToShowInMailbox
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
                    appendInvite = False
                # do not show invitations for cancelled parties
                if appendInvite:
                    if partyInfo.status == PartyGlobals.PartyStatus.Cancelled:
                        appendInvite = False
                # do not show mailbox invitations for parties that have finished yesterday
                if appendInvite:
                    # server time and client time may be slightly off, and toon can get mailbox stuck when
                    # they dont return the same value, using yesterday it's still possible but only
                    # at around midnight, which minimizes the possibilty
                    # we use end time because a party could be started 1 minute before it's supposed to end
                    endDate= partyInfo.endTime.date()
                    curDate = base.cr.toontownTimeManager.getCurServerDateTime().date()
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
        DistributedToon.partyNotify.debug("setHostedParties called passing in %d parties." % len(hostedParties))
        self.hostedParties = []
        for i in xrange(len(hostedParties)):
            hostedInfo = hostedParties[i]
            newParty = PartyInfo(*hostedInfo)
            self.hostedParties.append(newParty)
            assert self.notify.debug('self.hostedParties[%d]= %s' % (i,newParty))

    def setPartiesInvitedTo( self, partiesInvitedTo):
        """Handle uberdog telling us details of parties we are invited to."""
        DistributedToon.partyNotify.debug("setPartiesInvitedTo called passing in %d parties." % len(partiesInvitedTo))
        self.partiesInvitedTo = []
        for i in xrange(len(partiesInvitedTo)):
            partyInfo = partiesInvitedTo[i]
            newParty = PartyInfo(*partyInfo)
            self.partiesInvitedTo.append(newParty)
            assert self.notify.debug('self.partiesInvitedTo[%d]= %s' % (i,newParty))
        self.updateInviteMailNotify()

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

    def getInviteForPartyId(self, partyId):
        """Return the invite that matches partyId, None if not found."""
        result = None
        for invite in self.invites:
            if invite.partyId == partyId:
                result = invite
                break
        return result
        
    def setPartyReplies(self, replies):
        """Handle uberdog telling us replies to our hosted parties."""
        DistributedToon.partyNotify.debug("setPartyReplies called passing in %d parties." % len(replies))
        self.partyReplyInfoBases = []
        for i in xrange(len(replies)):
            partyReply = replies[i]
            repliesForOneParty = PartyReplyInfoBase(*partyReply)
            self.partyReplyInfoBases.append(repliesForOneParty)
            assert DistributedToon.partyNotify.debug('self.partyReplyInfoBases[%d]= %s' % (i,repliesForOneParty))

    def setPartyCanStart(self, partyId):
        """Handle uberdog telling us we can start a party that we're hosting."""
        DistributedToon.partyNotify.debug("setPartyCanStart called passing in partyId=%s" % partyId)
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = PartyGlobals.PartyStatus.CanStart
                # we crash if we do the import at the top 
                from toontown.shtiker import EventsPage
                if hasattr(self, "eventsPage") and \
                   base.localAvatar.book.entered and \
                   base.localAvatar.book.isOnPage(self.eventsPage) and \
                   self.eventsPage.getMode() == EventsPage.EventsPage_Host:
                    base.localAvatar.eventsPage.loadHostedPartyInfo()
                if hasattr(self, "displaySystemClickableWhisper"):
                    self.displaySystemClickableWhisper(0, TTLocalizer.PartyCanStart,
                                                     whisperType = WhisperPopup.WTSystem)
                else:
                    self.setSystemMessage(0, TTLocalizer.PartyCanStart)

    def setPartyStatus(self, partyId, newStatus):
        """Handle uberdog telling us there's a change in status for either the hosted or invitedTo parties."""
        DistributedToon.partyNotify.debug("setPartyCanStatus called passing in partyId=%s status=%s" %
                                          (partyId, newStatus))
        
        found = False
        for partyInfo in self.hostedParties:
            if partyInfo.partyId == partyId:
                partyInfo.status = newStatus
                found = True
                #if base.localAvatar.book.entered:
                #    base.localAvatar.eventsPage.loadHostedPartyInfo()
                break
        for partyInfo in self.partiesInvitedTo:
            if partyInfo.partyId == partyId:
                partyInfo.status = newStatus
                found = True
                # we crash if we do the import at the top 
                from toontown.shtiker import EventsPage
                if hasattr(self, "eventsPage") and \
                   base.localAvatar.book.entered and \
                   base.localAvatar.book.isOnPage(self.eventsPage) and \
                   self.eventsPage.getMode() == EventsPage.EventsPage_Invited:
                    base.localAvatar.eventsPage.loadInvitations()
                if newStatus == PartyStatus.Started and hasattr(self, "displaySystemClickableWhisper"):
                    invite = self.getInviteForPartyId(partyId)
                    if invite:
                        name = " "
                        host = base.cr.identifyAvatar(partyInfo.hostId)
                        if host:
                            name = host.getName()
                            if GMUtils.testGMIdentity(name):
                                name  = GMUtils.handleGMName(name)
                        if invite.status == InviteStatus.Accepted:
                            displayStr = TTLocalizer.PartyHasStartedAcceptedInvite % TTLocalizer.GetPossesive(name)
                            self.displaySystemClickableWhisper(-1, displayStr,
                                                               whisperType = WhisperPopup.WTSystem)
                        else:
                            displayStr = TTLocalizer.PartyHasStartedNotAcceptedInvite % TTLocalizer.GetPossesive(name)
                            self.setSystemMessage(partyInfo.hostId, displayStr,
                                                  whisperType = WhisperPopup.WTSystem)
                break
        if not found:
            self.notify.warning("setPartyCanStart can't find partyId=% status=%d" % (partyId, newStatus))

                
    def announcePartyStarted(self, partyId):
        DistributedToon.partyNotify.debug("announcePartyStarted")
        # rely on the party has started system message whispers instead
        return
        
        # get the guest list for this party
        for partyReplyInfo in self.partyReplyInfoBases:
            if partyReplyInfo.partyId == partyId:
                for singleReply in partyReplyInfo.replies:
                    # if this toon is still on my friends list, whisper to them
                    # that my party has started
                    toonId = singleReply.inviteeId
                    if base.cr.isFriend(toonId):
                        if base.cr.isFriendOnline(toonId):
                            if singleReply.status == InviteStatus.Accepted:
                                # 'My party has started!'
                                self.whisperSCTo(5302, toonId, 0)
                                pass
                            else:
                                # they never accepted the invite
                                # 'My party has started!',
                                self.whisperSCTo(5302, toonId, 0)
                                pass

    def updateInvite(self, inviteKey, newStatus):
        """We've gotten confirmation from the uberdog to reject/accept the invite."""
        DistributedToon.partyNotify.debug("updateInvite( inviteKey=%d, newStatus=%s )" %(inviteKey, InviteStatus.getString(newStatus)) )
        for invite in self.invites:
            if invite.inviteKey == inviteKey:
                invite.status = newStatus
                self.updateInviteMailNotify()
                break
            

    def updateReply(self, partyId, inviteeId, newStatus):
        """Someone accepted our invite while we were online."""
        DistributedToon.partyNotify.debug("updateReply( partyId=%d, inviteeId=%d, newStatus=%s )" %(partyId, inviteeId, InviteStatus.getString(newStatus)) )
        for partyReplyInfoBase in self.partyReplyInfoBases:
            if partyReplyInfoBase.partyId == partyId:
                for reply in partyReplyInfoBase.replies:
                    if reply.inviteeId == inviteeId:
                        reply.status = newStatus
                        break

    def scrubTalk(self, message, mods):
        scrubbed = 0
        text = copy.copy(message)
        for mod in mods:
            index = mod[0]
            length = mod[1] - mod[0] + 1
            newText = text[0:index] + length*"" + text[index + length:]
            text = newText

            
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "":
                newwords.append(word)
            elif word[0] == "":
                #newwords.append("Bleep")
                newwords.append("\1WLDisplay\1" + self.chatGarbler.garbleSingle(self, word) + "\2")
                scrubbed = 1
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                # If we are true friends then we shouldn't italacize the text
                flag = 0
                for friendId, flags in self.friendsList:
                    if not (flags & ToontownGlobals.FriendChat):
                        flag = 1
                if flag:
                    scrubbed = 1
                    newwords.append("\1WLDisplay\1" + word + "\2")
                else:
                    newwords.append(word)
                
        newText = " ".join(newwords)
        return newText, scrubbed
        

    def replaceBadWords(self, text):
        words = text.split(" ")
        newwords = []
        for word in words:
            if word == "":
                newwords.append(word)
            elif word[0] == "":
                #newwords.append("Bleep")
                newwords.append("\1WLRed\1" + self.chatGarbler.garbleSingle(self, word) + "\2")
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append("\1WLRed\1" + word + "\2")
                
        newText = " ".join(newwords)
        return newText
                    
    def toonUp(self, hpGained, hasInteractivePropBonus = False):
        # Adjusts the avatar's hp upward by the indicated value
        # (limited by maxHp) and shows green numbers flying out of the
        # avatar's head.

        if self.hp == None or hpGained < 0:
            return

        oldHp = self.hp

        # If hp is below zero, it might mean we're at a timeout in the
        # playground, in which case we respect that it is below zero
        # until we get our head above water.  If our toonUp would
        # take us above zero, then we pretend we started at zero in
        # the first place, ignoring the timeout.
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = min(max(self.hp, 0) + hpGained, self.maxHp)

        hpGained = self.hp - max(oldHp, 0)
        if hpGained > 0:
            self.showHpText(hpGained, hasInteractivePropBonus=hasInteractivePropBonus)
            self.hpChange(quietly = 0)

    def showHpText(self, number, bonus=0, scale=1, hasInteractivePropBonus = False):
        if self.HpTextEnabled and not self.ghostMode:           
            # We don't show zero change.
            if number != 0:
                # Get rid of the number if it is already there.
                if self.hpText:
                    self.hideHpText()
                # Set the font
                self.HpTextGenerator.setFont(OTPGlobals.getSignFont())
                # Show both negative and positive signs
                if number < 0:
                    self.HpTextGenerator.setText(str(number))
                else:
                    hpGainedStr = "+" + str(number)
                    if hasInteractivePropBonus:
                        hpGainedStr += "\n" + TTLocalizer.InteractivePropTrackBonusTerms[0]
                    self.HpTextGenerator.setText(hpGainedStr)
                # No shadow
                self.HpTextGenerator.clearShadow()
                # Put a shadow on there
                #self.HpTextGenerator.setShadow(0.05, 0.05)
                #self.HpTextGenerator.setShadowColor(0, 0, 0, 1)
                # Center the number
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                # Red for negative, green for positive, yellow for bonus
                if bonus == 1:
                    r = 1.0
                    g = 1.0
                    b = 0
                    a = 1
                elif bonus == 2:
                    r = 1.0
                    g = 0.5
                    b = 0
                    a = 1
                elif number < 0:
                    r = 0.9
                    g = 0
                    b = 0
                    a = 1
                else:
                    r = 0
                    g = 0.9
                    b = 0
                    a = 1

                self.HpTextGenerator.setTextColor(r, g, b, a)

                self.hpTextNode = self.HpTextGenerator.generate()
                
                # Put the hpText over the head of the avatar
                self.hpText = self.attachNewNode(self.hpTextNode)
                self.hpText.setScale(scale)
                # Make sure it is a billboard
                self.hpText.setBillboardPointEye()
                # Render it after other things in the scene.
                self.hpText.setBin('fixed', 100)

                # Initial position ... Center of the body... the "tan tien"
                self.hpText.setPos(0, 0, self.height/2)
                seq = Task.sequence(
                    # Fly the number out of the character
                    self.hpText.lerpPos(Point3(0, 0, self.height + 1.5),
                                            1.0,
                                            blendType = 'easeOut'),
                    # Wait 2 seconds
                    Task.pause(0.85),
                    # Fade the number
                    self.hpText.lerpColor(Vec4(r, g, b, a),
                                              Vec4(r, g, b, 0),
                                              0.1),
                    # Get rid of the number
                    Task(self.hideHpTextTask))
                taskMgr.add(seq, self.uniqueName("hpText"))
        else:
            # Just play the sound effect.
            # TODO: Put in the sound effect!
            pass
            
    def setName(self, name = "unknownDistributedAvatar"):
        if GMUtils.testGMIdentity(name):
            self.__handleGMName(name)
            return
        DistributedPlayer.DistributedPlayer.setName(self, name)   
        
    def __handleGMName(self, name):
        """ Parse the name for symbols that will get replaced by prefixes and icons """
                
        gmName = GMUtils.handleGMName(name)
        # self.setDisplayName(gmName)   
        DistributedPlayer.DistributedPlayer.setName(self, gmName)
        self.setNametagStyle(5)
        
        # Now setup the icon
        self.setGMIcon(GMUtils.getGMType(name))
        self.gmToon = True
        
    def setGMIcon(self, prefix=None):      

        if hasattr(self, 'gmIcon') and self.gmIcon:             # Probably has the party gm icon
            return            
        if not prefix:
            prefix = GMUtils.getGMType(self.getName())
            
        if prefix == TTLocalizer.GM_1:
            icons = loader.loadModel('phase_3.5/models/gui/tt_m_gui_trp_toontroop001')
            self.gmIcon = icons.find("**/*whistleIcon*")
            self.gmIcon.setScale(4)
        elif prefix == TTLocalizer.GM_2:
            icons = loader.loadModel('phase_3.5/models/gui/tt_m_gui_trp_toontroop001')
            self.gmIcon = icons.find("**/*whistleIcon*")
            self.gmIcon.setScale(4)
        else:
            # Shouldn't be a GM
            return
        #r = self.nametag.getNametag3d().getBounds().getRadius()
        self.gmIcon.reparentTo(self.nametag.getNameIcon())
        
        # Remove the star if we see it
        self.setTrophyScore(self.trophyScore)
        
        # self.gmIcon.setPos(-(r+1), 0.0, 0.25)
        self.gmIcon.setZ(-2.5)
        self.gmIcon.setY(0.00)
        self.gmIcon.setColor(Vec4(1.0,1.0,1.0, 1.0))
        self.gmIcon.setTransparency(1)
        
        self.gmIconInterval = LerpHprInterval(self.gmIcon, 3.0, Point3(0,0,0), Point3(-360,0,0))
        self.gmIconInterval.loop()      
        
    def setGMPartyIcon(self):           
       
        self.gmIcon = loader.loadModel('phase_3.5/models/gui/tt_m_gui_trp_toontroop001')
        self.gmIcon.reparentTo(self.nametag.getNameIcon())
        self.gmIcon.setScale(3.25)
        
        # Remove the star if we see it
        self.setTrophyScore(self.trophyScore)
        
        # self.gmIcon.setPos(-(r+1), 0.0, 0.25)
        self.gmIcon.setZ(1.0)
        self.gmIcon.setY(0.00)
        self.gmIcon.setColor(Vec4(1.0,1.0,1.0, 1.0))
        self.gmIcon.setTransparency(1)
        
        self.gmIconInterval = LerpHprInterval(self.gmIcon, 3.0, Point3(0,0,0), Point3(-360,0,0))
        self.gmIconInterval.loop()      
        
    def removeGMIcon(self):
        # Stop the gm spin task
        if hasattr(self, 'gmIconInterval') and self.gmIconInterval:
            self.gmIconInterval.finish()
            del self.gmIconInterval        
            
        if hasattr(self, 'gmIcon') and self.gmIcon:
            self.gmIcon.detachNode()
            del self.gmIcon
