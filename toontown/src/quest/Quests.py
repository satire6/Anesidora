from otp.otpbase import OTPGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import ToontownGlobals
from toontown.battle import SuitBattleGlobals
from toontown.coghq import CogDisguiseGlobals
import random
from toontown.toon import NPCToons
import copy
import string
from toontown.hood import ZoneUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
import time
import types
import random

# COG TRACKS PER HOOD
# Look in DistributedSuitPlannerAI.py

# COG LEVELS PER HOOD
# TT LEVELS 1,2,3
# DD LEVELS 2,3,4,5,6
# DG LEVELS 2,3,4,5,6
# MM LEVELS 2,3,4,5,6
# BR LEVELS 5,6,7
# DL LEVELS 5,6,7,8,9
#
# COG LEVELS PER DNA
# 
# CORP LEVELS
# f   1,2,3,4,5
# p   2,3,4,5,6
# ym  3,4,5,6,7
# mm  4,5,6,7,8
# ds  5,6,7,8,9
# hh  6,7,8,9,10
# cr  7,8,9,10,11
# tbc 8,9,10,11,12
#
# SALES LEVELS
# cc  1,2,3,4,5
# tm  2,3,4,5,6
# nd  3,4,5,6,7
# gh  4,5,6,7,8
# ms  5,6,7,8,9
# tf  6,7,8,9,10
# m   7,8,9,10,11
# mh  8,9,10,11,12
#
# MONEY LEVELS
# sc  1,2,3,4,5
# pp  2,3,4,5,6
# tw  3,4,5,6,7
# bc  4,5,6,7,8
# nc  5,6,7,8,9
# mb  6,7,8,9,10
# ls  7,8,9,10,11
# rb  8,9,10,11,12
#
# LEGAL LEVELS
# bf  1,2,3,4,5
# b   2,3,4,5,6
# dt  3,4,5,6,7
# ac  4,5,6,7,8
# bs  5,6,7,8,9
# sd  6,7,8,9,10
# le  7,8,9,10,11
# bw  8,9,10,11,12


notify = DirectNotifyGlobal.directNotify.newCategory("Quests")

# Pull some strings out of the localizer for easy access
ItemDict = TTLocalizer.QuestsItemDict
CompleteString = TTLocalizer.QuestsCompleteString
NotChosenString = TTLocalizer.QuestsNotChosenString
DefaultGreeting = TTLocalizer.QuestsDefaultGreeting
DefaultIncomplete = TTLocalizer.QuestsDefaultIncomplete
DefaultIncompleteProgress = TTLocalizer.QuestsDefaultIncompleteProgress
DefaultIncompleteWrongNPC = TTLocalizer.QuestsDefaultIncompleteWrongNPC
DefaultComplete = TTLocalizer.QuestsDefaultComplete
DefaultLeaving = TTLocalizer.QuestsDefaultLeaving
DefaultReject = TTLocalizer.QuestsDefaultReject
DefaultTierNotDone = TTLocalizer.QuestsDefaultTierNotDone
# The default string gets replaced with the quest getstring
DefaultQuest = TTLocalizer.QuestsDefaultQuest
DefaultVisitQuestDialog = TTLocalizer.QuestsDefaultVisitQuestDialog


# Constants used in the NPC movies centrally defined here
GREETING = 0
QUEST = 1
INCOMPLETE = 2
INCOMPLETE_PROGRESS = 3
INCOMPLETE_WRONG_NPC = 4
COMPLETE = 5
LEAVING = 6

# Constants used in the QuestDict
Any = 1
OBSOLETE = 'OBSOLETE' # set the reward to this for removed non-multipart quests

# Are you the start of a multipart quest?
Start = 1
# Or are you the continuation of a multipart quest?
Cont = 0

Anywhere = 1
NA = 2
Same = 3
AnyFish = 4
AnyCashbotSuitPart = 5
AnyLawbotSuitPart = 6
AnyBossbotSuitPart = 7

ToonTailor = 999
ToonHQ = 1000
QuestDictTierIndex = 0
QuestDictStartIndex = 1
QuestDictDescIndex = 2
QuestDictFromNpcIndex = 3
QuestDictToNpcIndex = 4
QuestDictRewardIndex = 5
QuestDictNextQuestIndex = 6
QuestDictDialogIndex = 7
# RecoverItem percentage difficulty
VeryEasy = 100
Easy = 75
Medium = 50
Hard = 25
VeryHard = 20

# Tier constants used in the quest dict
TT_TIER = 0
DD_TIER = 4
DG_TIER = 7
MM_TIER = 8
BR_TIER = 11
DL_TIER = 14
LAWBOT_HQ_TIER = 18
BOSSBOT_HQ_TIER = 32
ELDER_TIER = 49

# The final tier loops
LOOPING_FINAL_TIER = ELDER_TIER

VISIT_QUEST_ID = 1000
TROLLEY_QUEST_ID = 110
FIRST_COG_QUEST_ID = 145
FRIEND_QUEST_ID = 150
PHONE_QUEST_ID = 175

# newbie levels for elder quests
NEWBIE_HP = 25
# Set to 50 HP because that is about what you have at the
# end of Daisy Gardens (45 hp + fishing)
SELLBOT_HQ_NEWBIE_HP = 50
# Set to 85 HP because that is about what you have at the
# end of Donald's Dreamland (81 hp + fishing) -patricia
CASHBOT_HQ_NEWBIE_HP = 85

# pull in factory types from ToontownGlobals
from toontown.toonbase.ToontownGlobals import FT_FullSuit, FT_Leg, FT_Arm, FT_Torso

# We use our own random generator so we can seed it properly
QuestRandGen = random.Random()

def seedRandomGen(npcId, avId, tier, rewardHistory):
    """
    Seed the quest random generator with an npc, av, tier, and rewardHistory
    This guarantees the npc will have consistent behavior when
    approached by the same avatar repeatedly. This helps prevent
    guests from shopping for quests by approaching the same npc multiple
    times in a row.
    """
    QuestRandGen.seed(npcId * 100 + avId + tier + len(rewardHistory))

def seededRandomChoice(seq):
    """
    Return a random choice from seq. Should be preceded by a call
    to seedRandomGen with the relevant parties.
    """
    return QuestRandGen.choice(seq)

def getCompleteStatusWithNpc(questComplete, toNpcId, npc):
    """
    Given the actualy quest complete bool, based on this npc
    and toNpcId, determine if the quest is actually complete
    with this npc. If npc is passed in as None, just return the
    complete status of the quest.
    return values are:
      COMPLETE : quest is complete (was the right npc as well, or None)
      INCOMPLETE_PROGRESS : quest is incomplete because of the progress
      INCOMPLETE_WRONG_NPC : quest is incomplete because this is the wrong npc
      INCOMPLETE : quest is incomplete
    """
    if questComplete:
        if npc:
            if npcMatches(toNpcId, npc):
                return COMPLETE
            else:
                return INCOMPLETE_WRONG_NPC
        else:
            return COMPLETE
    else:
        if npc:
            if npcMatches(toNpcId, npc):
                return INCOMPLETE_PROGRESS
            else:
                return INCOMPLETE
        else:
            return INCOMPLETE

def npcMatches(toNpcId, npc):
    """
    Return true if this npc matches this toNpcId
    This also checks for wildcards and ToonHQ ids
    """
    return (
        # Exact npc match
        (toNpcId == npc.getNpcId()) or
        # Quest did not care who it was
        (toNpcId == Any) or
        # Quest wanted a generic ToonHQ npc and we found one
        ((toNpcId == ToonHQ) and (npc.getHq())) or
        # Quest wanted a generic Tailor npc and we found one
        ((toNpcId == ToonTailor) and (npc.getTailor()))
        )
        
        
def calcRecoverChance(numberNotDone, baseChance, cap = 1):
    chance = baseChance
    avgNum2Kill = 1.0 / (chance / 100.0)
    if numberNotDone >= (avgNum2Kill * 1.5) and cap:
        chance = 1000
    elif numberNotDone > (avgNum2Kill * 0.5):
        diff = float(numberNotDone - (avgNum2Kill * 0.5))
        luck = 1.0 + abs(diff / (avgNum2Kill * 0.5))
        chance *= luck
    return chance


def simulateRecoveryVar(numNeeded, baseChance, list = 0, cap = 1):
    numHave = 0
    numTries = 0
    greatestFailChain = 0
    currentFail = 0
    capHits = 0
    attemptList = {}

    while numHave < numNeeded:
        numTries += 1
        chance = calcRecoverChance(currentFail, baseChance, cap)
        test = random.random() * 100
        if chance == 1000:
            capHits += 1    
        if test < chance:
            numHave += 1
            if currentFail > greatestFailChain:
                greatestFailChain = currentFail
            if attemptList.get(currentFail):
                attemptList[currentFail] += 1
            else:
                attemptList[currentFail] = 1
            currentFail = 0
            
        else:
            currentFail += 1
    
    print("Test results: %s tries, %s longest failure chain, %s cap hits" % (numTries, greatestFailChain, capHits))
    if list:
        print("failures for each succes %s" % (attemptList))

def simulateRecoveryFix(numNeeded, baseChance, list = 0):
    numHave = 0
    numTries = 0
    greatestFailChain = 0
    currentFail = 0
    attemptList = {}

    while numHave < numNeeded:
        numTries += 1
        chance = baseChance
        test = random.random() * 100
        if test < chance:
            numHave += 1
            if currentFail > greatestFailChain:
                greatestFailChain = currentFail
            if attemptList.get(currentFail):
                attemptList[currentFail] += 1
            else:
                attemptList[currentFail] = 1
            currentFail = 0
        else:
            currentFail += 1

    print("Test results: %s tries, %s longest failure chain" % (numTries, greatestFailChain))
    if list:
        print("failures for each succes %s" % (attemptList))

class Quest:
    """
    Base class for all quest types
    """

    # quest validity checks
    # if you know that one of these is wrong, please fix it
    _cogTracks = [Any, 'c', 'l', 'm', 's']
    _factoryTypes = [Any, FT_FullSuit, FT_Leg, FT_Arm, FT_Torso]
    def check(self, cond, msg):
        assert cond, "quest %s: %s" % (self.id, msg)
    def checkLocation(self, location):
        locations = [
            Anywhere,
            ] + TTLocalizer.GlobalStreetNames.keys()
        self.check(location in locations,
                   "invalid location: %s" % location)
    def checkNumCogs(self, num):
        self.check(1,
                   "invalid number of cogs: %s" % num)
    def checkNewbieLevel(self, level):
        self.check(1,
                   "invalid newbie level: %s" % level)
    def checkCogType(self, type):
        types = [Any] + SuitBattleGlobals.SuitAttributes.keys()
        self.check(type in types,
                   "invalid cog type: %s" % type)
    def checkCogTrack(self, track):
        self.check(track in self._cogTracks,
                   "invalid cog track: %s" % track)
    def checkCogLevel(self, level):
        self.check(level >= 1 and level <= 12,
                   "invalid cog level: %s" % level)
    def checkNumSkelecogs(self, num):
        self.check(1,
                   "invalid number of cogs: %s" % num)
    def checkSkelecogTrack(self, track):
        self.check(track in self._cogTracks,
                   "invalid cog track: %s" % track)
    def checkSkelecogLevel(self, level):
        self.check(level >= 1 and level <= 12,
                   "invalid cog level: %s" % level)
    def checkNumSkeleRevives(self, num):
        self.check(1,
                   "invalid number of cogs: %s" % num)
    def checkNumForemen(self, num):
        self.check(num > 0,
                   "invalid number of foremen: %s" % num)
    def checkNumVPs(self, num):
        self.check(num > 0,
                   "invalid number of VPs: %s" % num)
    def checkNumSupervisors(self, num):
        self.check(num > 0,
                   "invalid number of supervisors: %s" % num)
    def checkNumCFOs(self, num):
        self.check(num > 0,
                   "invalid number of CFOs: %s" % num)
    def checkNumBuildings(self, num):
        self.check(1,
                   "invalid num buildings: %s" % num)
    def checkBuildingTrack(self, track):
        self.check(track in self._cogTracks,
                   "invalid building track: %s" % track)
    def checkBuildingFloors(self, floors):
        self.check(floors >= 1 and floors <= 5,
                   "invalid num floors: %s" % floors)
    def checkNumFactories(self, num):
        self.check(1,
                   "invalid num factories: %s" % num)
    def checkFactoryType(self, type):
        self.check(type in self._factoryTypes,
                   "invalid factory type: %s" % type)
    def checkNumMints(self, num):
        self.check(1,
                   "invalid num mints: %s" % num)
    def checkNumCogParts(self, num):
        self.check(1,
                   "invalid num cog parts: %s" % num)
    def checkNumGags(self, num):
        self.check(1,
                   "invalid num gags: %s" % num)
    def checkGagTrack(self, track):
        self.check(track >= ToontownBattleGlobals.MIN_TRACK_INDEX and
                   track <= ToontownBattleGlobals.MAX_TRACK_INDEX,
                   "invalid gag track: %s" % track)
    def checkGagItem(self, item):
        self.check(item >= ToontownBattleGlobals.MIN_LEVEL_INDEX and
                   item <= ToontownBattleGlobals.MAX_LEVEL_INDEX,
                   "invalid gag item: %s" % item)
    def checkDeliveryItem(self, item):
        self.check(ItemDict.has_key(item),
                   "invalid delivery item: %s" % item)
    def checkNumItems(self, num):
        self.check(1,
                   "invalid num items: %s" % num)
    def checkRecoveryItem(self, item):
        self.check(ItemDict.has_key(item),
                   "invalid recovery item: %s" % item)
    def checkPercentChance(self, chance):
        self.check(chance > 0 and chance <= 100,
                   "invalid percent chance: %s" % chance)
    def checkRecoveryItemHolderAndType(self, holder, holderType='type'):
        holderTypes = [
            'type',
            'level',
            'track',
            ]
        self.check(holderType in holderTypes,
                   "invalid recovery item holderType: %s" % holderType)
        if holderType == 'type':
            holders = [
                Any,
                AnyFish,
                ] + SuitBattleGlobals.SuitAttributes.keys()
            self.check(holder in holders,
                       "invalid recovery item holder: %s "
                       "for holderType: %s" % (holder, holderType))
        elif holderType == 'level':
            pass
        elif holderType == 'track':
            self.check(holder in self._cogTracks,
                       "invalid recovery item holder: %s "
                       "for holderType: %s" % (holder, holderType))
    def checkTrackChoice(self, option):
        self.check(option >= ToontownBattleGlobals.MIN_TRACK_INDEX and
                   option <= ToontownBattleGlobals.MAX_TRACK_INDEX,
                   "invalid track option: %s" % option)
    def checkNumFriends(self, num):
        self.check(1,
                   "invalid number of friends: %s" % num)
    def checkNumMinigames(self, num):
        self.check(1,
                   "invalid number of minigames: %s" % num)

    def filterFunc(avatar):
        # The filter func allows us to filter the quest types that we give
        # out to an avatar based on some property of our choosing. This is used
        # for instance to see if avatar has any friends before giving out the friend quest
        # 1 means give the quest, 0 means do not. By default, you can give all quests
        return 1
    filterFunc = staticmethod(filterFunc)

    def __init__(self, id, quest):
        self.id = id
        # The quest is just a list of properties that can be
        # interpreted by each subclass differently
        self.quest = quest
    def getId(self):
        return self.id
    def getType(self):
        return self.__class__
    def getObjectiveStrings(self):
        return [""]
    def getString(self):
        # Simplest description of the quest
        return self.getObjectiveStrings()[0]
    def getRewardString(self, progressString):
        # How the quest appears in the reward panel
        return self.getString() + " : " + progressString
    def getChooseString(self):
        # How the quest appears in the QuestChoiceGui panel
        return self.getString()
    def getPosterString(self):
        # How the quest appears on the QuestPoster
        return self.getString()
    def getHeadlineString(self):
        # Headline used on the QuestPoster
        return self.getString()
    def getDefaultQuestDialog(self):
        # How the NPC describes the quest
        return self.getString() + TTLocalizer.Period
    def getNumQuestItems(self):
        return -1
    def addArticle(self, num, oString):
        if len(oString) == 0:
            return oString
        if num == 1:
            # The singular case now includes the indefinite article (a, an).
            return oString
        else:
            return "%d %s" % (num, oString)
    def __repr__(self):
        return ("Quest type: %s id: %s params: %s" %
                (self.__class__.__name__, self.id, self.quest[0:]))

    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        # For non-Cog quests this is always false.
        return 0
    def doesVPCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog VP death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        # For non-VP quests this is always false.
        return 0
    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog CFO death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        # For non-CFO quests this is always false.
        return 0
    def doesFactoryCount(self, avId, location, avList):
        # If factory counts toward this quest, returns how many times it
        # counts (non-zero). Otherwise, returns zero.
        return 0
    def doesMintCount(self, avId, location, avList):
        # If mint counts toward this quest, returns how many times it
        # counts (non-zero). Otherwise, returns zero.
        return 0
    def doesCogPartCount(self, avId, location, avList):
        # If cog part counts toward this quest, returns how many times it
        # counts (non-zero). Otherwise, returns zero.
        return 0
    def getCompletionStatus(self, av, questDesc, npc=None):
        # Determine if this avatar has completed his quest wrt this npc
        notify.error("Pure virtual - please override me")
        return None
    
class LocationBasedQuest(Quest):
    """
    Virtual Quest Class for quests that are location based. This allows
    us to centralize some of the utilities for dealing with hood and branch
    zones and determining matches for zoneIds
    """
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkLocation(self.quest[0])
    def getLocation(self):
        return self.quest[0]
    def getLocationName(self):
        loc = self.getLocation()
        if loc == Anywhere:
            locName = ""
        # Now you can specify cogs in a hood (singular)
        # or on a particular street (singular).
        # You cannot specify a particular zone that also happens to be
        # a hood identifier (N*1000); it will be interpreted as the entire
        # hood.
        elif loc in ToontownGlobals.hoodNameMap:
            locName = TTLocalizer.QuestInLocationString % {
                'inPhrase' : ToontownGlobals.hoodNameMap[loc][1],
                'location' : ToontownGlobals.hoodNameMap[loc][-1] + TTLocalizer.QuestsLocationArticle}
            
        elif loc in ToontownGlobals.StreetBranchZones:
            locName = TTLocalizer.QuestInLocationString % {
                'inPhrase' : ToontownGlobals.StreetNames[loc][1],
                'location' : ToontownGlobals.StreetNames[loc][-1] + TTLocalizer.QuestsLocationArticle}
        return locName
    def isLocationMatch(self, zoneId):
        loc = self.getLocation()
        # Easy case, anywhere always matches
        if loc is Anywhere:
            return 1
        # If all that is specified is a hood, then just check the hood zone
        if ZoneUtil.isPlayground(loc):
            if loc == ZoneUtil.getCanonicalHoodId(zoneId):
                return 1
            else:
                return 0
        # If a branch is specified, check the branch zone
        else:
            if loc == ZoneUtil.getCanonicalBranchZone(zoneId):
                return 1
            # Is this the *actual* zone? Why would you do that? I'll support it just in case.
            elif loc == zoneId:
                return 1
            else:
                return 0
    def getChooseString(self):
        # How the quest appears in the QuestChoiceGui panel
        return (TTLocalizer.QuestsLocationString % { "string" : self.getString(),
                                                   "location" : self.getLocationName()})
    def getPosterString(self):
        # How the quest appears on the QuestPoster
        return (TTLocalizer.QuestsLocationString % { "string" : self.getString(),
                                                   "location" : self.getLocationName()})
    def getDefaultQuestDialog(self):
        # How the NPC describes the quest
        return ((TTLocalizer.QuestsLocationString + TTLocalizer.Period) % { "string" : self.getString(),
                                                                        "location" : self.getLocationName()})


# TODO: this should be 'ApprenticeQuest'
class NewbieQuest:
    """Virtual Quest Class for quests that involve 'newbie' toons."""
    def getNewbieLevel(self):
        notify.error("Pure virtual - please override me")
    # inheritor must override and call down to this function to avoid
    # diamond-of-death ambiguity
    def getString(self,
                  newStr=TTLocalizer.QuestsCogNewNewbieQuestObjective,
                  oldStr=TTLocalizer.QuestsCogOldNewbieQuestObjective):
        # Return the full string
        laff = self.getNewbieLevel()
        if laff <= NEWBIE_HP:
            return (newStr % (self.getObjectiveStrings()[0]))
        else:
            return (oldStr % {'laffPoints' : laff,
                              'objective' : self.getObjectiveStrings()[0]})
    def getCaption(self):
        laff = self.getNewbieLevel()
        if laff <= NEWBIE_HP:
            return TTLocalizer.QuestsCogNewNewbieQuestCaption % laff
        else:
            return TTLocalizer.QuestsCogOldNewbieQuestCaption % laff
        
    def getNumNewbies(self, avId, avList):
        # given an avatar and a list of participants, returns the number
        # of 'newbies' among the other participants
        newbieHp = self.getNewbieLevel()
        num = 0
        for av in avList:
            if (av.getDoId() != avId and av.getMaxHp() <= newbieHp):
                num += 1  
        return num

class CogQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        # only validate quest[1] and [2] here for pure CogQuests
        # subclasses use them for other things
        if self.__class__ == CogQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogType(self.quest[2])
    def getCogType(self):
        return self.quest[2]
    def getNumQuestItems(self):
        return self.getNumCogs()
    def getNumCogs(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumCogs())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
            
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumCogs() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsCogQuestProgress %
                        {"progress" : questDesc[4], "numCogs" : self.getNumCogs()})
    def getCogNameString(self):
        # Cog, Cogs, Pencil Pusher, Pencil Pushers
        numCogs = self.getNumCogs()
        cogType = self.getCogType()
        if numCogs == 1:
            if cogType == Any:
                return TTLocalizer.ACog
            else:
                return SuitBattleGlobals.SuitAttributes[cogType]['singularname']
        else:
            if cogType == Any:
                return TTLocalizer.Cogs
            else:
                return SuitBattleGlobals.SuitAttributes[cogType]['pluralname']
    def getObjectiveStrings(self):
        # Defeat 3 Pencil Pushers
        # Defeat 3 Cogs
        cogName = self.getCogNameString()
        numCogs = self.getNumCogs()
        if numCogs == 1:
            text = cogName
        else:
            text = TTLocalizer.QuestsCogQuestDefeatDesc % {"numCogs" : numCogs, "cogName" : cogName}
        return (text,)
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsCogQuestDefeat % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)
        cogName = self.getCogNameString()
        numCogs = self.getNumCogs()
        if numCogs == 1:
            text = TTLocalizer.QuestsCogQuestSCStringS
        else:
            text = TTLocalizer.QuestsCogQuestSCStringP
        cogLoc = self.getLocationName()
        return (text % {"cogName" : cogName, "cogLoc" : cogLoc})
    
    def getHeadlineString(self):
        return TTLocalizer.QuestsCogQuestHeadline
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        questCogType = self.getCogType()
        return (
            ((questCogType is Any) or (questCogType is cogDict['type'])) and
            (avId in cogDict['activeToons']) and
            self.isLocationMatch(zoneId))


class CogNewbieQuest(CogQuest, NewbieQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        if self.__class__ == CogNewbieQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogType(self.quest[2])
            self.checkNewbieLevel(self.quest[3])
    def getNewbieLevel(self):
        return self.quest[3]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        if CogQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class CogTrackQuest(CogQuest):
    trackCodes = ['c', 'l', 'm', 's']
    trackNamesS = [TTLocalizer.BossbotS, TTLocalizer.LawbotS,
                   TTLocalizer.CashbotS, TTLocalizer.SellbotS]
    trackNamesP = [TTLocalizer.BossbotP, TTLocalizer.LawbotP,
                   TTLocalizer.CashbotP, TTLocalizer.SellbotP]
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        if self.__class__ == CogTrackQuest:
            self.checkNumCogs(self.quest[1])
            self.checkCogTrack(self.quest[2])
    def getCogTrack(self):
        return self.quest[2]
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumCogs() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsCogTrackQuestProgress %
                        {"progress" : questDesc[4], "numCogs" : self.getNumCogs()})
    def getObjectiveStrings(self):
        # Defeat 3 Corporate Cogs
        numCogs = self.getNumCogs()
        # Get the cog track name
        track = self.trackCodes.index(self.getCogTrack())
        if numCogs == 1:
            text = self.trackNamesS[track]
        else:
            text = TTLocalizer.QuestsCogTrackDefeatDesc % {"numCogs" : numCogs,
                                                         "trackName" : self.trackNamesP[track]}
        return (text,)
        
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsCogTrackQuestDefeat % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)

        numCogs = self.getNumCogs()
        track = self.trackCodes.index(self.getCogTrack())
        if numCogs == 1:
            cogText = self.trackNamesS[track]
            text = TTLocalizer.QuestsCogTrackQuestSCStringS
        else:
            cogText = self.trackNamesP[track]
            text = TTLocalizer.QuestsCogTrackQuestSCStringP
        cogLocName = self.getLocationName()
        return (text % {"cogText" : cogText, "cogLoc" : cogLocName})
    def getHeadlineString(self):
        return TTLocalizer.QuestsCogTrackQuestHeadline
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        questCogTrack = self.getCogTrack()
        return (
            (questCogTrack == cogDict['track']) and
            (avId in cogDict['activeToons']) and
            self.isLocationMatch(zoneId))


class CogLevelQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumCogs(self.quest[1])
        self.checkCogLevel(self.quest[2])
    def getCogType(self):
        return Any
    def getCogLevel(self):
        return self.quest[2]
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumCogs() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsCogLevelQuestProgress %
                        {"progress" : questDesc[4], "numCogs" : self.getNumCogs()})
    def getObjectiveStrings(self):
        # Defeat 3 Level 2+ Cogs
        count = self.getNumCogs()
        level = self.getCogLevel()
        name = self.getCogNameString()
        if count == 1:
            text = TTLocalizer.QuestsCogLevelQuestDesc
        else:
            text = TTLocalizer.QuestsCogLevelQuestDescC

        return (text % { "count" : count,
                         "level" : level,
                         "name"  : name,}, )

    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsCogLevelQuestDefeat % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumCogs():
            return getFinishToonTaskSCStrings(toNpcId)

        count = self.getNumCogs()
        level = self.getCogLevel()
        name = self.getCogNameString()
        if count == 1:
            text = TTLocalizer.QuestsCogLevelQuestDesc
        else:
            text = TTLocalizer.QuestsCogLevelQuestDescI

        objective = text % { "level" : level, "name" : name }
        location = self.getLocationName()
        return (TTLocalizer.QuestsCogLevelQuestSCString % \
                { "objective" : objective,
                  "location" : location} )
    
    def getHeadlineString(self):
        return TTLocalizer.QuestsCogLevelQuestHeadline
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        questCogLevel = self.getCogLevel()
        # Go ahead and count cogs that are higher level too
        return ((questCogLevel <= cogDict['level']) and
                (avId in cogDict['activeToons']) and
                self.isLocationMatch(zoneId)
                )


class SkelecogQBase:
    # mixin/policy class for skelecog quests
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ASkeleton
        else:
            return TTLocalizer.SkeletonP
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return (cogDict['isSkelecog'] and
                (avId in cogDict['activeToons']) and
                self.isLocationMatch(zoneId))
                
class SkelecogQuest(CogQuest, SkelecogQBase):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return SkelecogQBase.doesCogCount(self, avId,
                                          cogDict, zoneId, avList)

class SkelecogNewbieQuest(SkelecogQuest, NewbieQuest):
    def __init__(self, id, quest):
        SkelecogQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        if SkelecogQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0

class SkelecogTrackQuest(CogTrackQuest, SkelecogQBase):
    trackNamesS = [TTLocalizer.BossbotSkelS, TTLocalizer.LawbotSkelS,
                   TTLocalizer.CashbotSkelS, TTLocalizer.SellbotSkelS]
    trackNamesP = [TTLocalizer.BossbotSkelP, TTLocalizer.LawbotSkelP,
                   TTLocalizer.CashbotSkelP, TTLocalizer.SellbotSkelP]
    def __init__(self, id, quest):
        CogTrackQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])
        self.checkSkelecogTrack(self.quest[2])
    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return (SkelecogQBase.doesCogCount(self, avId,
                                           cogDict, zoneId, avList) and
                self.getCogTrack() == cogDict['track'])

class SkelecogLevelQuest(CogLevelQuest, SkelecogQBase):
    def __init__(self, id, quest):
        CogLevelQuest.__init__(self, id, quest)
        self.checkNumSkelecogs(self.quest[1])
        self.checkSkelecogLevel(self.quest[2])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        return SkelecogQBase.getCogNameString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return (SkelecogQBase.doesCogCount(self, avId,
                                           cogDict, zoneId, avList) and
                self.getCogLevel() <= cogDict['level'])

class SkeleReviveQBase:
    # mixin/policy class for skelecog w/revives quests
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.Av2Cog
        else:
            return TTLocalizer.v2CogP
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return (cogDict['hasRevives'] and
                (avId in cogDict['activeToons']) and
                self.isLocationMatch(zoneId))
                
class SkeleReviveQuest(CogQuest, SkeleReviveQBase):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSkeleRevives(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        return SkeleReviveQBase.getCogNameString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return SkeleReviveQBase.doesCogCount(self, avId,
                                          cogDict, zoneId, avList)

class ForemanQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumForemen(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.AForeman
        else:
            return TTLocalizer.ForemanP
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # bool forces 0 or 1 (there's code that pays attention to the
        # numeric value returned to determine how much progress was made)
        return bool(CogQuest.doesCogCount(self, avId,
                                          cogDict, zoneId, avList) and
                    cogDict['isForeman'])

class ForemanNewbieQuest(ForemanQuest, NewbieQuest):
    def __init__(self, id, quest):
        ForemanQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # bool forces 0 or 1 (there's code that pays attention to the
        # numeric value returned to determine how much progress was made)
        if ForemanQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class VPQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumVPs(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ACogVP
        else:
            return TTLocalizer.CogVPs
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0
    def doesVPCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog VP death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return self.isLocationMatch(zoneId)

class VPNewbieQuest(VPQuest, NewbieQuest):
    def __init__(self, id, quest):
        VPQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesVPCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog VP death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        if VPQuest.doesVPCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class SupervisorQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumSupervisors(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ASupervisor
        else:
            return TTLocalizer.SupervisorP
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # bool forces 0 or 1 (there's code that pays attention to the
        # numeric value returned to determine how much progress was made)
        return bool(CogQuest.doesCogCount(self, avId,
                                          cogDict, zoneId, avList) and
                    cogDict['isSupervisor'])

class SupervisorNewbieQuest(SupervisorQuest, NewbieQuest):
    def __init__(self, id, quest):
        SupervisorQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # bool forces 0 or 1 (there's code that pays attention to the
        # numeric value returned to determine how much progress was made)
        if SupervisorQuest.doesCogCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class CFOQuest(CogQuest):
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumCFOs(self.quest[1])
    def getCogType(self):
        return Any
    def getCogNameString(self):
        numCogs = self.getNumCogs()
        if numCogs == 1:
            return TTLocalizer.ACogCFO
        else:
            return TTLocalizer.CogCFOs
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        return 0
    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog CFO death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        return self.isLocationMatch(zoneId)

class CFONewbieQuest(CFOQuest, NewbieQuest):
    def __init__(self, id, quest):
        CFOQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def doesCFOCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog CFO death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        if CFOQuest.doesCFOCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


class RescueQuest(VPQuest):
    """Every time you beat a VP, you rescue an SOS toon."""
    def __init__(self, id, quest):
        VPQuest.__init__(self, id, quest)
    def getNumToons(self):
        return self.getNumCogs()
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumToons() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsRescueQuestProgress %
                        {"progress" : questDesc[4],
                         "numToons" : self.getNumToons()})
    def getObjectiveStrings(self):
        # a Toon, 3 Toons
        numToons = self.getNumCogs()
        if numToons == 1:
            text = TTLocalizer.QuestsRescueQuestToonS
        else:
            text = TTLocalizer.QuestsRescueQuestRescueDesc % {"numToons" : numToons}
        return (text,)
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsRescueQuestRescue % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumToons():
            return getFinishToonTaskSCStrings(toNpcId)
        numToons = self.getNumToons()
        if numToons == 1:
            text = TTLocalizer.QuestsRescueQuestSCStringS
        else:
            text = TTLocalizer.QuestsRescueQuestSCStringP
        toonLoc = self.getLocationName()
        return (text % {"toonLoc" : toonLoc})

    def getHeadlineString(self):
        return TTLocalizer.QuestsRescueQuestHeadline

class RescueNewbieQuest(RescueQuest, NewbieQuest):
    def __init__(self, id, quest):
        RescueQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(
            self,
            newStr=TTLocalizer.QuestsRescueNewNewbieQuestObjective,
            oldStr=TTLocalizer.QuestsRescueOldNewbieQuestObjective)
    def doesVPCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog VP death (as defined by the
        # cogDict) applies towards this quest, or false if it does not.
        if RescueQuest.doesVPCount(self, avId, cogDict, zoneId, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return 0


# TODO: is there any reason for this to be a CogQuest (and not simply a
# LocationBasedQuest)?
class BuildingQuest(CogQuest):
    trackCodes = ['c', 'l', 'm', 's']
    trackNames = [TTLocalizer.Bossbot, TTLocalizer.Lawbot,
                  TTLocalizer.Cashbot, TTLocalizer.Sellbot]
    def __init__(self, id, quest):
        CogQuest.__init__(self, id, quest)
        self.checkNumBuildings(self.quest[1])
        self.checkBuildingTrack(self.quest[2])
        self.checkBuildingFloors(self.quest[3])
    def getNumFloors(self):
        return self.quest[3]
    def getBuildingTrack(self):
        return self.quest[2]
    def getNumQuestItems(self):
        return self.getNumBuildings()
    def getNumBuildings(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumBuildings())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumBuildings() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsBuildingQuestProgressString %
                        {"progress" : questDesc[4],
                         "num" : self.getNumBuildings(),
                         })
    def getObjectiveStrings(self):
        count = self.getNumBuildings()
        floors = TTLocalizer.QuestsBuildingQuestFloorNumbers[self.getNumFloors() - 1]
        buildingTrack = self.getBuildingTrack()
        if buildingTrack == Any:
            type = TTLocalizer.Cog
        else:
            type = self.trackNames[self.trackCodes.index(buildingTrack)]
            
        if count == 1:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDesc
            else:
                text = TTLocalizer.QuestsBuildingQuestDescF
        else:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDescC
            else:
                text = TTLocalizer.QuestsBuildingQuestDescCF

        return (text % { "count" : count,
                         "floors" : floors,
                         "type" : type },)
    
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsBuildingQuestString % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumBuildings():
            return getFinishToonTaskSCStrings(toNpcId)

        count = self.getNumBuildings()
        floors = TTLocalizer.QuestsBuildingQuestFloorNumbers[self.getNumFloors() - 1]
        buildingTrack = self.getBuildingTrack()
        if buildingTrack == Any:
            type = TTLocalizer.Cog
        else:
            type = self.trackNames[self.trackCodes.index(buildingTrack)]
            
        if count == 1:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDesc
            else:
                text = TTLocalizer.QuestsBuildingQuestDescF
        else:
            if floors == '':
                text = TTLocalizer.QuestsBuildingQuestDescI
            else:
                text = TTLocalizer.QuestsBuildingQuestDescIF

        objective = text % { "floors" : floors,
                             "type" : type }
        location = self.getLocationName()
        
        return TTLocalizer.QuestsBuildingQuestSCString % \
               { "objective" : objective,
                 "location" : location }

    def getHeadlineString(self):
        return TTLocalizer.QuestsBuildingQuestHeadline
    def doesCogCount(self, avId, cogDict, zoneId, avList):
        # Returns true if the indicated cog death (as defined by the
        # cogDict) applies towards this quest, or false if it does
        # not.
        # For non-Cog quests this is always false.
        return 0
    def doesBuildingCount(self, avId, avList):
        # For non-newbie quests, building always counts
        return 1


class BuildingNewbieQuest(BuildingQuest, NewbieQuest):
    def __init__(self, id, quest):
        BuildingQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[4])
    def getNewbieLevel(self):
        return self.quest[4]
    def getString(self):
        return NewbieQuest.getString(self)
    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline
    def doesBuildingCount(self, avId, avList):
        return self.getNumNewbies(avId, avList) 


class FactoryQuest(LocationBasedQuest):
    factoryTypeNames = {
        FT_FullSuit : TTLocalizer.Cog,
        FT_Leg : TTLocalizer.FactoryTypeLeg,
        FT_Arm : TTLocalizer.FactoryTypeArm,
        FT_Torso : TTLocalizer.FactoryTypeTorso,
        }
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumFactories(self.quest[1])
    def getNumQuestItems(self):
        return self.getNumFactories()
    def getNumFactories(self):
        return self.quest[1]
    def getFactoryType(self):
        loc = self.getLocation()
        type = Any
        # is it a specific factory?
        if loc in ToontownGlobals.factoryId2factoryType:
            type = ToontownGlobals.factoryId2factoryType[loc]
        return type
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumFactories())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumFactories() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsFactoryQuestProgressString %
                        {"progress" : questDesc[4],
                         "num" : self.getNumFactories(),
                         })
    def getObjectiveStrings(self):
        count = self.getNumFactories()
        factoryType = self.getFactoryType()
        if factoryType == Any:
            type = TTLocalizer.Cog
        else:
            type = FactoryQuest.factoryTypeNames[factoryType]
            
        if count == 1:
            text = TTLocalizer.QuestsFactoryQuestDesc
        else:
            text = TTLocalizer.QuestsFactoryQuestDescC

        return (text % { "count" : count,
                         "type" : type },)
    
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsFactoryQuestString % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumFactories():
            return getFinishToonTaskSCStrings(toNpcId)

        factoryType = self.getFactoryType()
        if factoryType == Any:
            type = TTLocalizer.Cog
        else:
            type = FactoryQuest.factoryTypeNames[factoryType]
            
        count = self.getNumFactories()
        if count == 1:
            text = TTLocalizer.QuestsFactoryQuestDesc
        else:
            text = TTLocalizer.QuestsFactoryQuestDescI

        objective = text % { "type" : type }
        location = self.getLocationName()
        
        return TTLocalizer.QuestsFactoryQuestSCString % \
               { "objective" : objective,
                 "location" : location }

    def getHeadlineString(self):
        return TTLocalizer.QuestsFactoryQuestHeadline

    def doesFactoryCount(self, avId, location, avList):
        return self.isLocationMatch(location)


class FactoryNewbieQuest(FactoryQuest, NewbieQuest):
    def __init__(self, id, quest):
        FactoryQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline
    def doesFactoryCount(self, avId, location, avList):
        if FactoryQuest.doesFactoryCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num 


class MintQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumMints(self.quest[1])
    def getNumQuestItems(self):
        return self.getNumMints()
    def getNumMints(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumMints())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumMints() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsMintQuestProgressString %
                        {"progress" : questDesc[4],
                         "num" : self.getNumMints(),
                         })
    def getObjectiveStrings(self):
        count = self.getNumMints()
        if count == 1:
            text = TTLocalizer.QuestsMintQuestDesc
        else:
            text = TTLocalizer.QuestsMintQuestDescC % {"count" : count}
        return (text,)
    
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsMintQuestString % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumMints():
            return getFinishToonTaskSCStrings(toNpcId)

        count = self.getNumMints()
        if count == 1:
            objective = TTLocalizer.QuestsMintQuestDesc
        else:
            objective = TTLocalizer.QuestsMintQuestDescI

        location = self.getLocationName()
        
        return TTLocalizer.QuestsMintQuestSCString % \
               { "objective" : objective,
                 "location" : location }

    def getHeadlineString(self):
        return TTLocalizer.QuestsMintQuestHeadline

    def doesMintCount(self, avId, location, avList):
        return self.isLocationMatch(location)


class MintNewbieQuest(MintQuest, NewbieQuest):
    def __init__(self, id, quest):
        MintQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(self)
    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline
    def doesMintCount(self, avId, location, avList):
        if MintQuest.doesMintCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num 


# recover a cog-suit part from a factory (for your own Cog suit)
# NOTE: this quest has some issues; what happens if you have a full cog suit
# already?
class CogPartQuest(LocationBasedQuest):
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumCogParts(self.quest[1])
    def getNumQuestItems(self):
        return self.getNumParts()
    def getNumParts(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumParts())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumParts() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsCogPartQuestProgressString %
                        {"progress" : questDesc[4],
                         "num" : self.getNumParts(),
                         })
    def getObjectiveStrings(self):
        count = self.getNumParts()
            
        if count == 1:
            text = TTLocalizer.QuestsCogPartQuestDesc
        else:
            text = TTLocalizer.QuestsCogPartQuestDescC

        return (text % { "count" : count },)
    
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsCogPartQuestString % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumParts():
            return getFinishToonTaskSCStrings(toNpcId)

        count = self.getNumParts()
        if count == 1:
            text = TTLocalizer.QuestsCogPartQuestDesc
        else:
            text = TTLocalizer.QuestsCogPartQuestDescI

        objective = text
        location = self.getLocationName()
        
        return TTLocalizer.QuestsCogPartQuestSCString % \
               { "objective" : objective,
                 "location" : location }

    def getHeadlineString(self):
        return TTLocalizer.QuestsCogPartQuestHeadline

    def doesCogPartCount(self, avId, location, avList):
        return self.isLocationMatch(location)


# NOTE: this quest has some issues; what happens if you have a full cog suit
# already? And it currently is more like 'get a cog part and bring a newbie
# along', vs. 'help a new cog recover a cog part'.
class CogPartNewbieQuest(CogPartQuest, NewbieQuest):
    def __init__(self, id, quest):
        CogPartQuest.__init__(self, id, quest)
        self.checkNewbieLevel(self.quest[2])
    def getNewbieLevel(self):
        return self.quest[2]
    def getString(self):
        return NewbieQuest.getString(
            self,
            newStr=TTLocalizer.QuestsCogPartNewNewbieQuestObjective,
            oldStr=TTLocalizer.QuestsCogPartOldNewbieQuestObjective)
    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline
    def doesCogPartCount(self, avId, location, avList):
        if CogPartQuest.doesCogPartCount(self, avId, location, avList):
            return self.getNumNewbies(avId, avList)
        else:
            return num 


class DeliverGagQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkNumGags(self.quest[0])
        self.checkGagTrack(self.quest[1])
        self.checkGagItem(self.quest[2])
    def getGagType(self):
        return (self.quest[1], self.quest[2])
    def getNumQuestItems(self):
        return self.getNumGags()
    def getNumGags(self):
        return self.quest[0]
    def getCompletionStatus(self, av, questDesc, npc=None):
        # Make sure this is the toon we are supposed to deliver to
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        gag = self.getGagType()
        num = self.getNumGags()
        track = gag[0]
        level = gag[1]
        # Check to see if avatar has this gag and if we passed in an npc at all
        # In a sense, this quest is not complete until we are at the npc, so
        # throw that in as a conditional
        # NOTE: distributed toons inventory will be None because it is not
        # a broadcast field. In a battle play movie, we first need to check
        # if the inventory is not None
        questComplete = (npc and
                         av.inventory and
                         (av.inventory.numItem(track, level) >= num))
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumGags() == 1:
                # Return empty string to be consistent with DeliverItemQuest
                return ""
            else:
                return (TTLocalizer.QuestsDeliverGagQuestProgress %
                        {"progress" : questDesc[4],
                         "numGags" : self.getNumGags(),
                         })
    def getObjectiveStrings(self):
        # Deliver 3 Cream Pies
        track, item = self.getGagType()
        num = self.getNumGags()
        if num == 1:
            text = ToontownBattleGlobals.AvPropStringsSingular[track][item]
        else:
            gagName = ToontownBattleGlobals.AvPropStringsPlural[track][item]
            text = TTLocalizer.QuestsItemNameAndNum % {"num" : TTLocalizer.getLocalNum(num),
                                                     "name" : gagName}
        return (text,)

    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsDeliverGagQuestString % self.getObjectiveStrings()[0])
    def getRewardString(self, progress):
        return (TTLocalizer.QuestsDeliverGagQuestStringLong % self.getObjectiveStrings()[0])
    def getDefaultQuestDialog(self):
        return ((TTLocalizer.QuestsDeliverGagQuestStringLong % self.getObjectiveStrings()[0]) +
                "\a" + TTLocalizer.QuestsDeliverGagQuestInstructions)
    def getSCStrings(self, toNpcId, progress):
        if progress >= self.getNumGags():
            return getFinishToonTaskSCStrings(toNpcId)

        # Deliver 3 Cream Pies
        track, item = self.getGagType()
        num = self.getNumGags()
        if num == 1:
            text = TTLocalizer.QuestsDeliverGagQuestToSCStringS
            gagName = ToontownBattleGlobals.AvPropStringsSingular[track][item]
        else:
            text = TTLocalizer.QuestsDeliverGagQuestToSCStringP
            gagName = ToontownBattleGlobals.AvPropStringsPlural[track][item]
        return [(text % { "gagName" : gagName,
                          }),
                TTLocalizer.QuestsDeliverGagQuestSCString,
                ] + getVisitSCStrings(toNpcId)
    def getHeadlineString(self):
        return TTLocalizer.QuestsDeliverGagQuestHeadline

class DeliverItemQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkDeliveryItem(self.quest[0])
    def getItem(self):
        return self.quest[0]
    def getCompletionStatus(self, av, questDesc, npc=None):
        # Make sure this is the toon we are supposed to deliver to
        # Check to see if this is the correct NPC
        # You by definition have the item
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        # If you passed in an npc and it matches, quest is complete
        # otherwise it is incomplete because it is wrong NPC
        if (npc and npcMatches(toNpcId, npc)):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC

    def getProgressString(self, avatar, questDesc):
        # I think empty string looks best here
        return TTLocalizer.QuestsDeliverItemQuestProgress
    def getObjectiveStrings(self):
        # Deliver Hat
        iDict = ItemDict[self.getItem()]
        article = iDict[2]
        itemName = iDict[0]
        return ([article + itemName])
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsDeliverItemQuestString % self.getObjectiveStrings()[0])
    def getRewardString(self, progress):
        return (TTLocalizer.QuestsDeliverItemQuestStringLong % self.getObjectiveStrings()[0])
    def getDefaultQuestDialog(self):
        return (TTLocalizer.QuestsDeliverItemQuestStringLong % self.getObjectiveStrings()[0])
    def getSCStrings(self, toNpcId, progress):
        iDict = ItemDict[self.getItem()]
        article = iDict[2]
        itemName = iDict[0]
        return [TTLocalizer.QuestsDeliverItemQuestSCString %
                {"article" :  article,
                 "itemName" : itemName,
                 },
                ] + getVisitSCStrings(toNpcId)
    def getHeadlineString(self):
        return TTLocalizer.QuestsDeliverItemQuestHeadline

class VisitQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        if (npc and npcMatches(toNpcId, npc)):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC
    def getProgressString(self, avatar, questDesc):
        # I think empty string looks best here
        return TTLocalizer.QuestsVisitQuestProgress
    def getObjectiveStrings(self):
        return [""]
    def getString(self):
        # Return the full string
        return TTLocalizer.QuestsVisitQuestStringShort
    def getChooseString(self):
        return TTLocalizer.QuestsVisitQuestStringLong
    def getRewardString(self, progress):
        return TTLocalizer.QuestsVisitQuestStringLong
    def getDefaultQuestDialog(self):
        return random.choice(DefaultVisitQuestDialog)
    def getSCStrings(self, toNpcId, progress):
        return getVisitSCStrings(toNpcId)
    def getHeadlineString(self):
        return TTLocalizer.QuestsVisitQuestHeadline

class RecoverItemQuest(LocationBasedQuest):
    # Recovered items need:
    #   number of items
    #   item ID
    #   percent chance of finding item in each battle
    #   cog type
    #   flag for holder type if it's cog (type, track, or level)
    def __init__(self, id, quest):
        LocationBasedQuest.__init__(self, id, quest)
        self.checkNumItems(self.quest[1])
        self.checkRecoveryItem(self.quest[2])
        self.checkPercentChance(self.quest[3])
        if len(self.quest) > 5:
            self.checkRecoveryItemHolderAndType(self.quest[4], self.quest[5])
        else:
            self.checkRecoveryItemHolderAndType(self.quest[4])
            
    def testRecover(self, progress):
        test = random.random() * 100
        chance = self.getPercentChance()
        #chance = 10
        numberDone = progress & (pow(2,16) - 1)
        numberNotDone = progress >> 16
        returnTest = None
        
        avgNum2Kill = 1.0 / (chance / 100.0)
        
        if numberNotDone >= (avgNum2Kill * 1.5):
            chance = 100
        elif numberNotDone > (avgNum2Kill * 0.5):
            diff = float(numberNotDone - (avgNum2Kill * 0.5))
            luck = 1.0 + abs(diff / (avgNum2Kill * 0.5))
            chance *= luck
        
        if test <= chance:
            returnTest = 1
            numberNotDone = 0
            numberDone += 1
            #if numberDone == self.getNumItems():
            #    numberDone = 1
            #print("got")
        else:
            returnTest = 0
            numberNotDone += 1
            numberDone += 0
            #print("not got")
            
        returnCount = numberNotDone << 16
        returnCount += numberDone
        #import pdb; pdb.set_trace()
        #print("Quest Done %s NotDone %s Value %s Chance %s" % (numberDone, numberNotDone, returnCount, chance))
        return returnTest, returnCount
        
    def testDone(self, progress):
        numberDone = progress & (pow(2,16) - 1)
        print("Quest number done %s" % (numberDone))
        if numberDone >= self.getNumItems():
            return 1
        else:
            return 0
            
    def getNumQuestItems(self):
        return self.getNumItems()
    def getNumItems(self):
        return self.quest[1]
    def getItem(self):
        return self.quest[2]
    def getPercentChance(self):
        # Percent chance that localToon will find this item
        # each time he encounters the holder
        return self.quest[3]
    def getHolder(self):
        # The person or thing that is holding the item
        return self.quest[4]
    def getHolderType(self):
        # The holder type if holder is a Cog (type, track, or level)
        # Defaults to 'type', which used to be the only option
        if (len(self.quest) == 5):
            return 'type' 
        else:
            return self.quest[5]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        # masking the failures
        forwardProgress = toonProgress & (pow(2,16) - 1)
        questComplete = (forwardProgress >= self.getNumItems())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumItems() == 1:
                # Return empty string like DeliverItemQuest
                return ""
            else:
                progress = questDesc[4] & (pow(2,16) - 1)
                return (TTLocalizer.QuestsRecoverItemQuestProgress %
                        {"progress" : progress,#questDesc[4],
                         "numItems" : self.getNumItems(),
                         })
    def getObjectiveStrings(self):
        # Recover 3 keys from Cogs
        # Recover 3 keys from Pencil Pusher
        # TODO: Recover 3 keys from fishing hole
        holder = self.getHolder()
        holderType = self.getHolderType()
        if holder == Any:
            holderName = TTLocalizer.TheCogs
        elif holder == AnyFish:
            holderName = TTLocalizer.AFish
        elif (holderType == 'type'):
            holderName = SuitBattleGlobals.SuitAttributes[holder]['pluralname']
        elif (holderType == 'level'):
            holderName = TTLocalizer.QuestsRecoverItemQuestHolderString % {'level':TTLocalizer.Level, 'holder':holder, 'cogs':TTLocalizer.Cogs}
        elif (holderType == 'track'):
            if (holder == 'c'):
                holderName = TTLocalizer.BossbotP
            elif (holder == 's'):
                holderName = TTLocalizer.SellbotP
            elif (holder == 'm'):
                holderName = TTLocalizer.CashbotP
            elif (holder == 'l'):
                holderName = TTLocalizer.LawbotP
        item = self.getItem()
        num = self.getNumItems()
        if num == 1:
            itemName = ItemDict[item][2] + ItemDict[item][0]
        else:
            # plural
            itemName = TTLocalizer.QuestsItemNameAndNum % { "num" : TTLocalizer.getLocalNum(num),
                                                          "name" : ItemDict[item][1] }
        return ([itemName, holderName])
    def getString(self):
        return (TTLocalizer.QuestsRecoverItemQuestString %
                {"item"   : self.getObjectiveStrings()[0],
                 "holder" : self.getObjectiveStrings()[1],
                 })
    def getSCStrings(self, toNpcId, progress):
        item = self.getItem()
        num = self.getNumItems()

        # masking the failures
        forwardProgress = progress & (pow(2,16) - 1)

        if forwardProgress >= self.getNumItems():
            if num == 1:
                itemName = ItemDict[item][2] + ItemDict[item][0]
            else:
                itemName = TTLocalizer.QuestsItemNameAndNum % { "num" : TTLocalizer.getLocalNum(num),
                                                              "name" : ItemDict[item][1] }

            if toNpcId == ToonHQ:
                strings = [TTLocalizer.QuestsRecoverItemQuestReturnToHQSCString % itemName,
                           TTLocalizer.QuestsRecoverItemQuestGoToHQSCString,
                           ]
            elif toNpcId:
                npcName, hoodName, buildingArticle, buildingName, toStreet, streetName, isInPlayground = getNpcInfo(toNpcId)
                strings = [TTLocalizer.QuestsRecoverItemQuestReturnToSCString %
                           {"item"    : itemName,
                            "npcName" : npcName,
                            },
                           ]
                if isInPlayground:
                    strings.append(TTLocalizer.QuestsRecoverItemQuestGoToPlaygroundSCString % (hoodName))
                else:
                    strings.append(TTLocalizer.QuestsRecoverItemQuestGoToStreetSCString %
                                   {"to": toStreet,
                                    "street" : streetName,
                                    "hood"   : hoodName,
                                    })
                strings.extend([
                    TTLocalizer.QuestsRecoverItemQuestVisitBuildingSCString % (buildingArticle, buildingName),
                    TTLocalizer.QuestsRecoverItemQuestWhereIsBuildingSCString % (buildingArticle, buildingName),
                    ])

            return strings

        holder = self.getHolder()
        holderType = self.getHolderType()
        locName = self.getLocationName()
        if holder == Any:
            holderName = TTLocalizer.TheCogs
        elif holder == AnyFish:
            holderName = TTLocalizer.TheFish
        elif (holderType == 'type'):
            holderName = SuitBattleGlobals.SuitAttributes[holder]['pluralname']
        elif (holderType == 'level'):
            holderName = TTLocalizer.QuestsRecoverItemQuestHolderString % {'level':TTLocalizer.Level, 'holder':holder, 'cogs':TTLocalizer.Cogs}
        elif (holderType == 'track'):
            if (holder == 'c'):
                holderName = TTLocalizer.BossbotP
            elif (holder == 's'):
                holderName = TTLocalizer.SellbotP
            elif (holder == 'm'):
                holderName = TTLocalizer.CashbotP
            elif (holder == 'l'):
                holderName = TTLocalizer.LawbotP
        if num == 1:
            itemName = ItemDict[item][2] + ItemDict[item][0]
        else:
            # plural
            itemName = TTLocalizer.QuestsItemNameAndNum % { "num" : TTLocalizer.getLocalNum(num),
                                                          "name" : ItemDict[item][1] }

        return (TTLocalizer.QuestsRecoverItemQuestRecoverFromSCString %
                {"item"   : itemName,
                 "holder" : holderName,
                 "loc"    : locName,
                 })
    def getHeadlineString(self):
        return TTLocalizer.QuestsRecoverItemQuestHeadline

class TrackChoiceQuest(Quest):
    # Note: these are a little complicated
    # They popup an interface to choose or cancel, and have no reward
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkTrackChoice(self.quest[0])
        self.checkTrackChoice(self.quest[1])
    def getChoices(self):
        return self.quest[0], self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        if (npc and npcMatches(toNpcId, npc)):
            return COMPLETE
        else:
            return INCOMPLETE_WRONG_NPC
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return NotChosenString
    def getObjectiveStrings(self):
        trackA, trackB = self.getChoices()
        trackAName = ToontownBattleGlobals.Tracks[trackA].capitalize()
        trackBName = ToontownBattleGlobals.Tracks[trackB].capitalize()
        return ([trackAName, trackBName])
    def getString(self):
        return (TTLocalizer.QuestsTrackChoiceQuestString %
                {"trackA" : self.getObjectiveStrings()[0],
                 "trackB" : self.getObjectiveStrings()[1],
                 })
    def getSCStrings(self, toNpcId, progress):
        trackA, trackB = self.getChoices()
        trackAName = ToontownBattleGlobals.Tracks[trackA].capitalize()
        trackBName = ToontownBattleGlobals.Tracks[trackB].capitalize()
        return [TTLocalizer.QuestsTrackChoiceQuestSCString %
                {"trackA" : trackAName,
                 "trackB" : trackBName,
                 },
                TTLocalizer.QuestsTrackChoiceQuestMaybeSCString % trackAName,
                TTLocalizer.QuestsTrackChoiceQuestMaybeSCString % trackBName,
                ] + getVisitSCStrings(toNpcId)
    def getHeadlineString(self):
        return TTLocalizer.QuestsTrackChoiceQuestHeadline

class FriendQuest(Quest):

    def filterFunc(avatar):
        # The filter func allows us to filter the quest types that we give
        # out to an avatar based on some property of our choosing. This is used
        # for instance to see if avatar has any friends before giving out the friend quest
        # 1 means give the quest, 0 means do not
        if (len(avatar.getFriendsList()) == 0):
            return 1
        else:
            return 0
    filterFunc = staticmethod(filterFunc)
    
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
    # Friend quest progress is special. We do not dynamically update
    # the progress because you may not be online when it changes
    # (ie in a secret friend exchange)
    def getCompletionStatus(self, av, questDesc, npc=None):
        # See if your progress is changed, or better yet, check
        # to see if you actually have friends
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = ((toonProgress >= 1) or (len(av.getFriendsList()) > 0))
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ""
    def getString(self):
        return TTLocalizer.QuestsFriendQuestString
    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsFriendQuestSCString
    def getHeadlineString(self):
        return TTLocalizer.QuestsFriendQuestHeadline    
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsFriendQuestString]
    def doesFriendCount(self, av, otherAv):
        return 1

class FriendNewbieQuest(FriendQuest, NewbieQuest):
    def filterFunc(avatar):
        # Override the filter func from the parent class
        return 1
    filterFunc = staticmethod(filterFunc)

    def __init__(self, id, quest):
        FriendQuest.__init__(self, id, quest)
        self.checkNumFriends(self.quest[0])
        self.checkNewbieLevel(self.quest[1])
    def getNumQuestItems(self):
        return self.getNumFriends()
    def getNumFriends(self):
        return self.quest[0]
    def getNewbieLevel(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= self.getNumFriends())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumFriends() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsFriendNewbieQuestProgress %
                        {"progress" : questDesc[4],
                         "numFriends" : self.getNumFriends()})
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsFriendNewbieQuestObjective % (self.getNumFriends()))
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsFriendNewbieQuestString % (self.getNumFriends(), self.getNewbieLevel())]
    def doesFriendCount(self, av, otherAv):
        if (otherAv != None and (otherAv.getMaxHp() <= self.getNewbieLevel())):
            return 1
        return 0

class TrolleyQuest(Quest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= 1)
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ""
    def getString(self):
        return TTLocalizer.QuestsFriendQuestString
    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsTrolleyQuestSCString
    def getHeadlineString(self):
        return TTLocalizer.QuestsTrolleyQuestHeadline
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsTrolleyQuestString]

# NOTE: the mailbox quest has not been used in production yet.
# If you decide to add a MailboxQuest, be sure to test it well.
# It was added, then replaced in the same day by the PhoneQuest.
# -- Joe
class MailboxQuest(Quest):
    # Perhaps this should have a filterFunc
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= 1)
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ""
    def getString(self):
        return TTLocalizer.QuestsMailboxQuestString
    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsMailboxQuestSCString
    def getHeadlineString(self):
        return TTLocalizer.QuestsMailboxQuestHeadline
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsMailboxQuestString]

class PhoneQuest(Quest):
    # Perhaps this should have a filterFunc
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        questComplete = (toonProgress >= 1)
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)
    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            return ""
    def getString(self):
        return TTLocalizer.QuestsPhoneQuestString
    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsPhoneQuestSCString
    def getHeadlineString(self):
        return TTLocalizer.QuestsPhoneQuestHeadline
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsPhoneQuestString]


class MinigameNewbieQuest(Quest, NewbieQuest):
    def __init__(self, id, quest):
        Quest.__init__(self, id, quest)
        self.checkNumMinigames(self.quest[0])
        self.checkNewbieLevel(self.quest[1])
    def getNumQuestItems(self):
        return self.getNumMinigames()
    def getNumMinigames(self):
        return self.quest[0]
    def getNewbieLevel(self):
        return self.quest[1]
    def getCompletionStatus(self, av, questDesc, npc=None):
        questId, fromNpcId, toNpcId, rewardId, toonProgress = questDesc
        # See if your progress is changed
        questComplete = (toonProgress >= self.getNumMinigames())
        return getCompleteStatusWithNpc(questComplete, toNpcId, npc)

    def getProgressString(self, avatar, questDesc):
        if self.getCompletionStatus(avatar, questDesc) == COMPLETE:
            return CompleteString
        else:
            if self.getNumMinigames() == 1:
                return ""
            else:
                return (TTLocalizer.QuestsMinigameNewbieQuestProgress %
                        {"progress" : questDesc[4],
                         "numMinigames" : self.getNumMinigames()})
    def getString(self):
        # Return the full string
        return (TTLocalizer.QuestsMinigameNewbieQuestObjective % (self.getNumMinigames()))
    def getObjectiveStrings(self):
        return [TTLocalizer.QuestsMinigameNewbieQuestString % self.getNumMinigames()]
    def getHeadlineString(self):
        return TTLocalizer.QuestsNewbieQuestHeadline
    def getSCStrings(self, toNpcId, progress):
        if progress:
            return getFinishToonTaskSCStrings(toNpcId)
        return TTLocalizer.QuestsTrolleyQuestSCString
    def doesMinigameCount(self, av, avList):
        newbieHp = self.getNewbieLevel()
        points = 0
        for toon in avList:
            if ((toon != av) and (toon.getMaxHp() <= newbieHp)):
                points += 1
        return points
        


DefaultDialog = {GREETING : DefaultGreeting,
                 QUEST : DefaultQuest,
                 INCOMPLETE : DefaultIncomplete,
                 INCOMPLETE_PROGRESS : DefaultIncompleteProgress,
                 INCOMPLETE_WRONG_NPC : DefaultIncompleteWrongNPC,
                 COMPLETE : DefaultComplete,
                 LEAVING : DefaultLeaving,
                 }



def getQuestFromNpcId(id):
    return QuestDict.get(id)[QuestDictFromNpcIndex]

def getQuestToNpcId(id):
    return QuestDict.get(id)[QuestDictToNpcIndex]

def getQuestDialog(id):
    return QuestDict.get(id)[QuestDictDialogIndex]

def getQuestReward(id, av):
    baseRewardId = QuestDict.get(id)[QuestDictRewardIndex]
    return transformReward(baseRewardId, av)

NoRewardTierZeroQuests = (101, 110, 121, 131, 141, 145, 150, 160, 161, 162, 163)
RewardTierZeroQuests = ()
PreClarabelleQuestIds = NoRewardTierZeroQuests + RewardTierZeroQuests

QuestDict = {
    # Quest ID : ( tier, start, (questDesc), fromNpc, toNpc, reward, nextQuest, dialog )
    # some quests have 'OBSOLETE' for their reward; this is for obsolete quests
    # that some users might still be working on; the 'OBSOLETE' prevents the
    # quest from being assigned to users in the future

    # This is the tutorial quest
    101 : ( TT_TIER, Start, (CogQuest, Anywhere,  1, 'f'), Any, ToonHQ, NA, (110), DefaultDialog),
    
    # 103 : ( TT_TIER, Start, (DeliverItemQuest, 110), 2018, 2004, 110, NA, DefaultDialog),

    # skip the delivery quest for now...
    #110 : ( TT_TIER, Cont, (TrolleyQuest,), Any, ToonHQ, NA, (120, 130, 140), DefaultDialog),
    110 : ( TT_TIER, Cont, (TrolleyQuest,), Any, ToonHQ, NA, (145), DefaultDialog),

    120 : ( TT_TIER, OBSOLETE, (DeliverItemQuest, 5), ToonHQ, 2002, NA, 121, DefaultDialog),
    121 : ( TT_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 2, VeryEasy, Any, 'type'), 2002, 2002, NA, 150, DefaultDialog),

    130 : ( TT_TIER, OBSOLETE, (DeliverItemQuest, 6), ToonHQ, 2003, NA, 131, DefaultDialog),
    131 : ( TT_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 3, VeryEasy, Any, 'type'), 2003, 2003, NA, 150, DefaultDialog),

    140 : ( TT_TIER, OBSOLETE, (DeliverItemQuest, 4), ToonHQ, 2005, NA, 141, DefaultDialog),
    141 : ( TT_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 1, VeryEasy, Any, 'type'), 2005, 2005, NA, 150, DefaultDialog),

    # This quest replaces the deliver item quests
    145 : ( TT_TIER, Cont, (RecoverItemQuest, ToontownGlobals.ToontownCentral, 1, 20, VeryEasy, Any, 'type'), ToonHQ, ToonHQ, NA, 150, DefaultDialog),

    150 : ( TT_TIER, Cont, (FriendQuest,), Same, Same, NA, 175, DefaultDialog),

    # These are now bypassed, but left in as obsolete
    # because some players on the live site might still be working on them
    160 : ( TT_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.ToontownCentral, 3, 'c'), Same, ToonHQ, NA, 175,
            TTLocalizer.QuestDialogDict[160]),
    161 : ( TT_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.ToontownCentral, 3, 'l'), Same, ToonHQ, NA, 175,
            TTLocalizer.QuestDialogDict[161]),
    162 : ( TT_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.ToontownCentral, 3, 's'), Same, ToonHQ, NA, 175,
            TTLocalizer.QuestDialogDict[162]),
    163 : ( TT_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.ToontownCentral, 3, 'm'), Same, ToonHQ, NA, 175,
            TTLocalizer.QuestDialogDict[163]),

    # If you change this questID (175) make sure you change the constant PHONE_QUEST_ID
    175 : ( TT_TIER, Cont, (PhoneQuest,), Same, ToonHQ, 100, NA, 
            TTLocalizer.QuestDialogDict[175]),

    # First catalog will be delivered here

    # visiting quest 1000 is special
    # VISIT_QUEST_ID : ( 1, 1, (VisitQuest,), Any, Any, NA, NA, DefaultDialog),

    164 : ( TT_TIER+1, Start, (VisitQuest,), Any, 2001, NA, (165),
             TTLocalizer.QuestDialogDict[164]),
    165 : ( TT_TIER+1, Start, (CogQuest, Anywhere,  4, Any), 2001, Same, NA, (166, 167, 168, 169), 
            TTLocalizer.QuestDialogDict[165]),
    166 : ( TT_TIER+1, Cont, (CogTrackQuest, Anywhere,  4, 'c'), Same, Same, NA, (170, 171, 172), 
            TTLocalizer.QuestDialogDict[166]),
    167 : ( TT_TIER+1, Cont, (CogTrackQuest, Anywhere,  4, 'l'), Same, Same, NA, (170, 171, 172), 
            TTLocalizer.QuestDialogDict[167]),
    168 : ( TT_TIER+1, Cont, (CogTrackQuest, Anywhere,  4, 's'), Same, Same, NA, (170, 171, 172), 
            TTLocalizer.QuestDialogDict[168]),
    169 : ( TT_TIER+1, Cont, (CogTrackQuest, Anywhere,  4, 'm'), Same, Same, NA, (170, 171, 172), 
            TTLocalizer.QuestDialogDict[169]),
    170 : ( TT_TIER+1, Cont, (VisitQuest,), Same, 2005, NA, (400),
             TTLocalizer.QuestDialogDict[170]),
    171 : ( TT_TIER+1, Cont, (VisitQuest,), Same, 2311, NA, (400),
             TTLocalizer.QuestDialogDict[171]),
    172 : ( TT_TIER+1, Cont, (VisitQuest,), Same, 2119, NA, (400),
             TTLocalizer.QuestDialogDict[172]),
    400 : ( TT_TIER+1, Cont, (TrackChoiceQuest,
                           ToontownBattleGlobals.SOUND_TRACK,
                           ToontownBattleGlobals.HEAL_TRACK),
            Same, Same, 400, NA,
            TTLocalizer.QuestDialogDict[400]),

    # Toontown central
    1001 : ( TT_TIER+2, Start, (CogQuest, ToontownGlobals.ToontownCentral,  3, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    1002 : ( TT_TIER+2, Start, (CogQuest, ToontownGlobals.ToontownCentral,  4, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    1003 : ( TT_TIER+2, Start, (CogQuest, ToontownGlobals.ToontownCentral,  5, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    1004 : ( TT_TIER+2, Start, (CogQuest, ToontownGlobals.ToontownCentral,  6, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    1005 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'f'), Any, ToonHQ, Any, NA, DefaultDialog),
    1006 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'p'), Any, ToonHQ, Any, NA, DefaultDialog),
    1007 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    1008 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'b'), Any, ToonHQ, Any, NA, DefaultDialog),
    1009 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'sc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1010 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
    1011 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1012 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),

    1013 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 4, 'f'), Any, ToonHQ, Any, NA, DefaultDialog),
    1014 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 4, 'p'), Any, ToonHQ, Any, NA, DefaultDialog),
    1015 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 4, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    1016 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 4, 'b'), Any, ToonHQ, Any, NA, DefaultDialog),
    
    1017 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 1, 'ym'), Any, ToonHQ, Any, NA, DefaultDialog),
    1018 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 1, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    1019 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 1, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    1020 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 1, 'dt'), Any, ToonHQ, Any, NA, DefaultDialog),

    1021 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  2, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    1022 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  6, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    1023 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  3, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    1024 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  4, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    1025 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  4, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    1026 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral,  6, 3), Any, ToonHQ, Any, NA, DefaultDialog),

    1027 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  2, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    1028 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  2, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    1029 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  2, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    1030 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  2, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),
    1031 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  3, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    1032 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  3, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    1033 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  3, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    1034 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  3, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),
    1035 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  5, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    1036 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  5, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    1037 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  5, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    1038 : ( TT_TIER+2, Start, (CogTrackQuest, ToontownGlobals.ToontownCentral,  5, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    # More random quests for TT_TIER+2 are found after 1100.

    # Help out Loopy Lane.  For a reward, you get teleport access to TTC.
    1039 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2135, NA, (1041, 1042, 1043),
             TTLocalizer.QuestDialogDict[1039]),
    1040 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2207, NA, (1041, 1042, 1043),
             TTLocalizer.QuestDialogDict[1040]),
    1041 : ( TT_TIER+2, Cont, (VisitQuest,), Same, 2211, NA, (1044),
             TTLocalizer.QuestDialogDict[1041]),
    1042 : ( TT_TIER+2, Cont, (VisitQuest,), Same, 2209, NA, (1044),
             TTLocalizer.QuestDialogDict[1042]),
    1043 : ( TT_TIER+2, Cont, (VisitQuest,), Same, 2210, NA, (1044),
             TTLocalizer.QuestDialogDict[1043]),
    1044 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 4, 7, VeryEasy, Any, 'type'), Same, Same, NA, (1045),
             TTLocalizer.QuestDialogDict[1044]),
    1045 : ( TT_TIER+2, Cont, (DeliverItemQuest, 8), Same, ToonHQ, 300, NA,
             TTLocalizer.QuestDialogDict[1045]),

    # Funny Money needs to recover their adding machines.  Reward is ability
    # to carry 50 jellybeans
    1046 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2127, NA, (1047),
             TTLocalizer.QuestDialogDict[1046]),
    1047 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 5, 9, VeryEasy, 'm', 'track'), 2127, Same, NA, (1048),
             TTLocalizer.QuestDialogDict[1047]),
    1048 : ( TT_TIER+2, Cont, (DeliverItemQuest, 9), Same, 2131, NA, (1049),
             TTLocalizer.QuestDialogDict[1048]),
    1049 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 10, 2007, VeryEasy, 3, 'level'), Same, Same, NA, (1053),
             TTLocalizer.QuestDialogDict[1049]),
    1053 : ( TT_TIER+2, Cont, (DeliverItemQuest, 9), Same, 2127, 700, NA,
             TTLocalizer.QuestDialogDict[1053]),

    # Used Clown Cars needs to recover tires.  Your reward is the medium pouch
    # so you can now carry 25 gags.
    1054 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2128, NA, (1055),
             TTLocalizer.QuestDialogDict[1054]),
    1055 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 4, 10, Easy, AnyFish), 2128, Same, NA, (1056),
             TTLocalizer.QuestDialogDict[1055]),
    1056 : ( TT_TIER+2, Cont, (VisitQuest,), Same, 2213, NA, (1057),
             TTLocalizer.QuestDialogDict[1056]),
    1057 : ( TT_TIER+2, Cont, (CogLevelQuest, ToontownGlobals.ToontownCentral, 6, 3), Same, Same, NA, (1058),
             TTLocalizer.QuestDialogDict[1057]),
    1058 : ( TT_TIER+2, Cont, (DeliverItemQuest, 11), Same, 2128, 200, NA,
             TTLocalizer.QuestDialogDict[1058]),

    # Ink shortage.  Reward is +2 HP.
    1059 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2302, NA, (1060),
             TTLocalizer.QuestDialogDict[1059]),
    1060 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 1, 12, Medium, AnyFish), 2302, Same, NA, (1062),
             TTLocalizer.QuestDialogDict[1060]),
    1061 : ( TT_TIER+2, Cont, (CogQuest, ToontownGlobals.ToontownCentral, 6, 'p'), Same, Same, 101, NA,
             TTLocalizer.QuestDialogDict[1061]),
    1062 : ( TT_TIER+2, Cont, (CogQuest, ToontownGlobals.ToontownCentral, 6, 'b'), Same, Same, 101, NA,
             TTLocalizer.QuestDialogDict[1062]),

    # Two packages for Dr. ???  Reward is new track. 
    900 : ( TT_TIER+3, Start, (VisitQuest,), Any, 2201, NA, (1063),
             TTLocalizer.QuestDialogDict[900]),
    1063 : ( TT_TIER+3, Start, (RecoverItemQuest, Anywhere, 1, 13, Medium, 3, 'level'), 2201, Same, NA, (1067),
             TTLocalizer.QuestDialogDict[1063]),
    1067 : ( TT_TIER+3, Cont, (DeliverItemQuest, 13), Same, 2112, NA, (1068),
             TTLocalizer.QuestDialogDict[1067]),
    1068 : ( TT_TIER+3, Cont, (CogQuest, ToontownGlobals.ToontownCentral, 10, Any), Same, Same, NA, (1069, 1070, 1071),
             TTLocalizer.QuestDialogDict[1068]),
    1069 : ( TT_TIER+3, Cont, (RecoverItemQuest, Anywhere, 1, 13, Medium, 'm', 'track'), Same, Same, NA, (1072),
             TTLocalizer.QuestDialogDict[1069]),
    1070 : ( TT_TIER+3, Cont, (RecoverItemQuest, Anywhere, 1, 13, Medium, 's', 'track'), Same, Same, NA, (1072),
             TTLocalizer.QuestDialogDict[1070]),
    1071 : ( TT_TIER+3, Cont, (RecoverItemQuest, Anywhere, 1, 13, Medium, 'c', 'track'), Same, Same, NA, (1072),
             TTLocalizer.QuestDialogDict[1071]),
    1072 : ( TT_TIER+3, Cont, (DeliverItemQuest, 13), Same, 2301, NA, (1073),
             TTLocalizer.QuestDialogDict[1072]),
    1073 : ( TT_TIER+3, Cont, (VisitQuest,), Any, 2201, NA, (1074),
             TTLocalizer.QuestDialogDict[1073]),
    1074 : ( TT_TIER+3, Cont, (RecoverItemQuest, Anywhere, 1, 13, Hard, Any), Same, Same, NA, (1075),
             TTLocalizer.QuestDialogDict[1074]),
    1075 : ( TT_TIER+3, Cont, (DeliverItemQuest, 13), Same, 2301, 900, NA,
             TTLocalizer.QuestDialogDict[1075]),

    # 14K Goldfish.  Reward is max quest = 2.
    1076 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2217, NA, (1077),
             TTLocalizer.QuestDialogDict[1076]),
    1077 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 1, 14, Medium, Any), 2217, Same, NA, (1078),
             TTLocalizer.QuestDialogDict[1077]),
    1078 : ( TT_TIER+2, Cont, (DeliverItemQuest, 14), Same, 2302, NA, (1079),
             TTLocalizer.QuestDialogDict[1078]),
    1079 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 15, Easy, 'f'), Same, 2217, NA, (1080),
             TTLocalizer.QuestDialogDict[1079]),
    1092 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 15, Easy, 'sc'), Same, 2217, NA, (1080),
             TTLocalizer.QuestDialogDict[1092]),
    1080 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 4, 15, Easy, AnyFish), Same, Same, 500, NA,
             TTLocalizer.QuestDialogDict[1080]),

    # Sticky Lou glued to floor.  Reward is +3 HP.
    1081 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2208, NA, (1082),
             TTLocalizer.QuestDialogDict[1081]),
    1082 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 1, 16, Medium, 's', 'track'), 2208, Same, NA, (1083),
             TTLocalizer.QuestDialogDict[1082]),
    1083 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 17, Medium, 'l', 'track'), Same, Same, NA, (1084),
             TTLocalizer.QuestDialogDict[1083]),
    1084 : ( TT_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 18, Medium, 'm', 'track'), Same, Same, 102, NA,
             TTLocalizer.QuestDialogDict[1084]),

    # Professor Pete is analyzing Cogs.  Get him some gears and your reward
    # is +1 HP.
    1085 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2003, NA, (1086),
             TTLocalizer.QuestDialogDict[1085]),
    1086 : ( TT_TIER+2, Start, (RecoverItemQuest, Anywhere, 5, 2007, Easy, 2, 'level'), 2003, Same, NA, (1089),
             TTLocalizer.QuestDialogDict[1086]),
    1089 : ( TT_TIER+2, Cont, (DeliverItemQuest, 19), Same, ToonHQ, 100, NA,
             TTLocalizer.QuestDialogDict[1089]),

    # Learn about Cog Radar.  Kill Cogs.  Gain +2 HP. 
    1090 : ( TT_TIER+2, Start, (VisitQuest,), Any, 2119, NA, (1091),
             TTLocalizer.QuestDialogDict[1090]),
    1091 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral, 8, 2), 2119, ToonHQ, 101, NA,
             TTLocalizer.QuestDialogDict[1091]),

    # Next TT_TIER+2 id: 1093


    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    1100 : ( TT_TIER+2, Start, (CogQuest, ToontownGlobals.ToontownCentral, 10, Any), Any, ToonHQ, NA, (1101), DefaultDialog),
    1101 : ( TT_TIER+2, Cont, (DeliverItemQuest, 1000), Any, 2004, 1000, NA, DefaultDialog),

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    1102 : ( TT_TIER+2, Start, (CogLevelQuest, ToontownGlobals.ToontownCentral, 8, 3), Any, ToonHQ, NA, (1103), DefaultDialog),
    1103 : ( TT_TIER+2, Cont, (DeliverItemQuest, 1000), Any, 2004, 1000, NA, DefaultDialog),


    # More random quests for TT_TIER+2
    1105 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'f'), Any, ToonHQ, Any, NA, DefaultDialog),
    1106 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'p'), Any, ToonHQ, Any, NA, DefaultDialog),
    1107 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    1108 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'b'), Any, ToonHQ, Any, NA, DefaultDialog),
    1109 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'sc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1110 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
    1111 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1112 : ( TT_TIER+2, Start, (CogQuest, Anywhere, 2, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),

    # More random quests for TT_TIER+3 # for traliers stuck on last gag track quest
    1205 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'f'), Any, ToonHQ, Any, NA, DefaultDialog),
    1206 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'p'), Any, ToonHQ, Any, NA, DefaultDialog),
    1207 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    1208 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'b'), Any, ToonHQ, Any, NA, DefaultDialog),
    1209 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'sc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1210 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
    1211 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
    1212 : ( TT_TIER+3, Start, (CogQuest, Anywhere, 4, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),    

    # Donald's Dock
    401 : ( DD_TIER, Start, (TrackChoiceQuest,
                          ToontownBattleGlobals.DROP_TRACK,
                          ToontownBattleGlobals.LURE_TRACK),
            Any, ToonHQ, 400, NA,
            TTLocalizer.QuestDialogDict[401]),

    # Optional quests to do while working on the bottleneck quest
    2001 : ( DD_TIER, Start, (CogQuest, Anywhere, 3, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2002 : ( DD_TIER, Start, (CogQuest, Anywhere, 4, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2003 : ( DD_TIER, Start, (CogQuest, Anywhere, 5, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2004 : ( DD_TIER, Start, (CogQuest, Anywhere, 6, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2005 : ( DD_TIER, Start, (CogQuest, Anywhere, 7, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2006 : ( DD_TIER, Start, (CogQuest, Anywhere, 8, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2007 : ( DD_TIER, Start, (CogQuest, Anywhere, 9, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2008 : ( DD_TIER, Start, (CogQuest, Anywhere, 10, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2009 : ( DD_TIER, Start, (CogQuest, Anywhere, 12, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2010 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 2, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    2011 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 3, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    2012 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 2, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    2013 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 4, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    2014 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 4, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    2015 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 5, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    2816 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 4, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2817 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 5, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2818 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 6, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2819 : ( DD_TIER, Start, (CogLevelQuest, Anywhere, 7, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    2020 : ( DD_TIER, Start, (CogQuest, Anywhere, 10, Any), Any, ToonHQ, NA, (2021), DefaultDialog),
    2021 : ( DD_TIER, Cont, (DeliverItemQuest, 1000), Any, 1007, 1000, NA, DefaultDialog),


    # DD is heavy on low-level corporate (bossbot) cogs (levels 2-4)
    # and also medium-level money (cashbot) cogs (levels 3-6).  It's
    # light on legal and sales cogs.
    
      2101 : ( DD_TIER+1, Start, (CogQuest, ToontownGlobals.DonaldsDock, 3, Any), Any, ToonHQ, Any, NA, DefaultDialog),
      2102 : ( DD_TIER+1, Start, (CogQuest, ToontownGlobals.DonaldsDock, 4, Any), Any, ToonHQ, Any, NA, DefaultDialog),
      2103 : ( DD_TIER+1, Start, (CogQuest, ToontownGlobals.DonaldsDock, 5, Any), Any, ToonHQ, Any, NA, DefaultDialog),
      2104 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 6, Any), Any, ToonHQ, Any, NA, DefaultDialog),
      2105 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 7, Any), Any, ToonHQ, Any, NA, DefaultDialog),
      2106 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 8, Any), Any, ToonHQ, Any, NA, DefaultDialog),

      2107 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 6, 'f'),  Any, ToonHQ, Any, NA, DefaultDialog),
      2108 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'p'),  Any, ToonHQ, Any, NA, DefaultDialog),
      2109 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'ym'), Any, ToonHQ, Any, NA, DefaultDialog),
      2110 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 3, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
      2111 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 2, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
      2112 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 1, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),

      2113 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 6, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
      2114 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),
      2115 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
      2116 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 3, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
      2117 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 2, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
      2118 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 1, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),

      2119 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 6, 'sc'), Any, ToonHQ, Any, NA, DefaultDialog),
      2120 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
      2121 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
      2122 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 3, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
      2123 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 2, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
      2124 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 1, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),

      2125 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 6, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
      2126 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'b'),  Any, ToonHQ, Any, NA, DefaultDialog),
      2127 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 4, 'dt'), Any, ToonHQ, Any, NA, DefaultDialog),
      2128 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 3, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
      2129 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 2, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
      2130 : ( DD_TIER+1, Start, (CogQuest, Anywhere, 1, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),

      2131 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 2, 3), Any, ToonHQ, Any, NA, DefaultDialog),
      2132 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 3, 3), Any, ToonHQ, Any, NA, DefaultDialog),
      2133 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 2, 4), Any, ToonHQ, Any, NA, DefaultDialog),
      2134 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 4, 4), Any, ToonHQ, Any, NA, DefaultDialog),
      2135 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 4, 5), Any, ToonHQ, Any, NA, DefaultDialog),
      2136 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 5, 5), Any, ToonHQ, Any, NA, DefaultDialog),
      2137 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 4, 6), Any, ToonHQ, Any, NA, DefaultDialog),
      2138 : ( DD_TIER+1, Start, (CogLevelQuest, ToontownGlobals.DonaldsDock, 6, 6), Any, ToonHQ, Any, NA, DefaultDialog),

      2139 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 3, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
      2140 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 3, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
      2141 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 3, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
      2142 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 3, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

      2143 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 5, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
      2144 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 5, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
      2145 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 5, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
      2146 : ( DD_TIER+1, Start, (CogTrackQuest, ToontownGlobals.DonaldsDock, 5, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

      2147 : ( DD_TIER+1, Start, (CogTrackQuest, Anywhere, 7, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
      2148 : ( DD_TIER+1, Start, (CogTrackQuest, Anywhere, 7, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
      2149 : ( DD_TIER+1, Start, (CogTrackQuest, Anywhere, 7, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
      2150 : ( DD_TIER+1, Start, (CogTrackQuest, Anywhere, 7, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

      2151 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, Any, 1), Any, ToonHQ, Any, NA, DefaultDialog),
      2152 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
      2153 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 2, Any, 1), Any, ToonHQ, Any, NA, DefaultDialog),
      2154 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 2, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
      2155 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, 'm', 1), Any, ToonHQ, Any, NA, DefaultDialog),
      2156 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, 's', 1), Any, ToonHQ, Any, NA, DefaultDialog),
      2157 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, 'c', 1), Any, ToonHQ, Any, NA, DefaultDialog),
      2158 : ( DD_TIER+1, Start, (BuildingQuest, Anywhere, 1, 'l', 1), Any, ToonHQ, Any, NA, DefaultDialog),

      2159 : ( DD_TIER+1, Start, (DeliverGagQuest, 2, ToontownBattleGlobals.THROW_TRACK, 1),
               Any, Any, Any, NA, DefaultDialog),
      2160 : ( DD_TIER+1, Start, (DeliverGagQuest, 1, ToontownBattleGlobals.SQUIRT_TRACK, 1),
               Any, Any, Any, NA, DefaultDialog),
      2161 : ( DD_TIER+1, Start, (DeliverGagQuest, 1, ToontownBattleGlobals.SQUIRT_TRACK, 2),
               Any, Any, Any, NA, DefaultDialog),
      2162 : ( DD_TIER+1, Start, (DeliverGagQuest, 2, ToontownBattleGlobals.THROW_TRACK, 2),
               Any, Any, Any, NA, DefaultDialog),    


    # Billy Budd at the Barnacle Barn has lost an inner tube.  He
    # thinks a Penny Pincher stole it.  Reward: +2 Laff.
    2201 : ( DD_TIER+1, Start, (VisitQuest,), Any, 1101, NA, 2202,
             TTLocalizer.QuestDialogDict[2201]),
    2202 : ( DD_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 2001, Medium, 'pp'), 1101, Same, 101, NA,
             TTLocalizer.QuestDialogDict[2202]),


    # Captain Carl needs you to take his eyeglass prescription to the Doctor Queequeg.
    # Doctor Queequeg in turn needs you to recover eyeglass frames from a flunky.
    # When you deliver the frames to Dr. Q he will fill the prescription and give
    # the toon the glasses to return to Captain Carl. Reward: Large Pouch
    2203 : ( DD_TIER+1, Start, (VisitQuest,), Any, 1102, NA, 2204,
             TTLocalizer.QuestDialogDict[2203]),
    2204 : ( DD_TIER+1, Start, (DeliverItemQuest, 2002), 1102, 1104, NA, 2205,
             TTLocalizer.QuestDialogDict[2204]),
    2205 : ( DD_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 2003, Medium, 'f'), Same, Same, NA, 2206,
             TTLocalizer.QuestDialogDict[2205]),
    2206 : (DD_TIER+1, Cont, (DeliverItemQuest, 2004), Same, 1102, 201, NA,
           TTLocalizer.QuestDialogDict[2206]),


    # Barnacle Barbara at the Barnacle Barn has lost her big white wig.  She
    # says a back stabber stole it.  Reward: Max Money = 60.
    2207 : ( DD_TIER+1, Start, (VisitQuest,), Any, 1201, NA, 2208,
             TTLocalizer.QuestDialogDict[2207]),
    2208 : ( DD_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 2005, Easy, 'bs'), 1201, Same, 701, NA,
            TTLocalizer.QuestDialogDict[2208]),


    # Melville needs some things for his cog fighting sailing voyage. First go see Alice and
    # do what she asks to get some ballast. Then go see Art and do what he asks to get a
    # sailing chart. Reward: teleport access
    2209 : ( DD_TIER+1, Start, (VisitQuest,), Any, 1302, NA, 2210,
              TTLocalizer.QuestDialogDict[2209]),
    2210 : ( DD_TIER+1, Start, (VisitQuest,), 1302, 1301, NA, 2211,
             TTLocalizer.QuestDialogDict[2210]),
    2211 : ( DD_TIER+1, Cont, (CogQuest, ToontownGlobals.DonaldsDock, 5, 'mm'), Same, Same, NA, 2212,
             TTLocalizer.QuestDialogDict[2211]),
    2212 : ( DD_TIER+1, Cont, (DeliverItemQuest, 2006), Same, 1302, NA, 2213,
             TTLocalizer.QuestDialogDict[2212]),
    2213 : ( DD_TIER+1, Cont, (VisitQuest,), Same, 1202, NA, 2214,
             TTLocalizer.QuestDialogDict[2213]),
    2214 : ( DD_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.DonaldsDock, 3, 2007, Hard, Any), Same, Same, NA, 2215,
             TTLocalizer.QuestDialogDict[2214]),
    2215 : ( DD_TIER+1, Cont, (DeliverItemQuest, 2008), Same, 1302, 301, NA,
             TTLocalizer.QuestDialogDict[2215]),
                            

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    2500 : ( DD_TIER+1, Start, (CogQuest, ToontownGlobals.DonaldsDock, 15, Any), Any, ToonHQ, NA, (2501), DefaultDialog),
    2501 : ( DD_TIER+1, Cont, (DeliverItemQuest, 1000), Any, 1007, 1000, NA, DefaultDialog),


    # Optional quests to do while working on the bottleneck quest
    2801 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 3, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2802 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 4, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2803 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 5, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2804 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 6, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2805 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 7, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2806 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 8, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2807 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 9, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2808 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 10, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2809 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 12, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    2810 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 2, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    2811 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 3, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    2812 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 2, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    2813 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 4, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    2814 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 4, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    2815 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 5, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    2816 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 4, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2817 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 5, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2818 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 6, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    2819 : ( DD_TIER+2, Start, (CogLevelQuest, Anywhere, 7, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    2820 : ( DD_TIER+2, Start, (CogQuest, Anywhere, 20, Any), Any, ToonHQ, NA, (2821), DefaultDialog),
    2821 : ( DD_TIER+2, Cont, (DeliverItemQuest, 1000), Any, 1007, 1000, NA, DefaultDialog),




    # Ahab is building a giant prefab crab to confuse the cogs. He will need several cog
    # parts for it. Go see Claggart to get a clovis. Go see Hook to get a clock spring. Get a
    # counter weight from Rocky Shores (or Svetlana, or Cal). Then remove a cog building
    # that's blocking the solar panel on the crab.
    901 : ( DD_TIER+2, Start, (VisitQuest,), Any, 1203, NA, 2902,
            TTLocalizer.QuestDialogDict[901]),
    2902 : (DD_TIER+2, Start, (VisitQuest,), 1203, 1303, NA, 2903,
           TTLocalizer.QuestDialogDict[2902]),
    2903 : (DD_TIER+2, Cont, (DeliverItemQuest, 2009), Same, 1106, NA, 2904,
           TTLocalizer.QuestDialogDict[2903]),
    2904 : (DD_TIER+2, Cont, (DeliverItemQuest, 2010), Same, 1203, NA, 2905,
           TTLocalizer.QuestDialogDict[2904]),
    2905 : (DD_TIER+2, Cont, (VisitQuest, 2009), Same, 1105, NA, 2906,
           TTLocalizer.QuestDialogDict[2905]),
    2906 : (DD_TIER+2, Cont, (DeliverGagQuest, 3, ToontownBattleGlobals.SQUIRT_TRACK, 2), Same, Same, NA, 2907,
           TTLocalizer.QuestDialogDict[2906]),
    2907 : (DD_TIER+2, Cont, (DeliverItemQuest,2011), Same, 1203, NA, (2910, 2915, 2920),
           TTLocalizer.QuestDialogDict[2907]),
    2910 : (DD_TIER+2, Cont, (VisitQuest,), Same, 1107, NA, 2911, TTLocalizer.QuestDialog_2910),
    2911 : (DD_TIER+2, Cont, (CogTrackQuest, ToontownGlobals.DonaldsDock, 4, 'm'), Same, Same, NA, 2925,
           TTLocalizer.QuestDialogDict[2911]),
    2915 : (DD_TIER+2, Cont, (VisitQuest,), Same, 1204, NA, 2916, TTLocalizer.QuestDialog_2910),
    2916 : (DD_TIER+2, Cont, (CogTrackQuest, ToontownGlobals.DonaldsDock, 2, 's'), Same, Same, NA, 2925,
           TTLocalizer.QuestDialogDict[2916]),
    2920 : (DD_TIER+2, Cont, (VisitQuest,), Same, 1204, NA, 2921, TTLocalizer.QuestDialog_2910),
    2921 : (DD_TIER+2, Cont, (CogTrackQuest, ToontownGlobals.DonaldsDock, 6, 'c'), Same, Same, NA, 2925,
           TTLocalizer.QuestDialogDict[2921]),
    2925 : (DD_TIER+2, Cont, (DeliverItemQuest, 2012), Same, 1203, NA, 2926,
            TTLocalizer.QuestDialogDict[2925]),
    2926 : (DD_TIER+2, Cont, (BuildingQuest, ToontownGlobals.DonaldsDock, 1, Any, 2), Same, Same, 900, NA,
           TTLocalizer.QuestDialogDict[2926]),



    # Daisy Garden
    3101 : ( DG_TIER, Start, (CogQuest, ToontownGlobals.DaisyGardens, 8, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    3102 : ( DG_TIER, Start, (CogQuest, ToontownGlobals.DaisyGardens, 10, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    3103 : ( DG_TIER, Start, (CogQuest, ToontownGlobals.DaisyGardens, 12, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    3104 : ( DG_TIER, Start, (CogQuest, Anywhere, 14, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    3105 : ( DG_TIER, Start, (CogQuest, Anywhere, 16, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    3106 : ( DG_TIER, Start, (CogQuest, Anywhere, 18, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    # DG is heavy on sellbots and lawbots; few bossbots or cashbots here.
    3107 : ( DG_TIER, Start, (CogQuest, Anywhere, 10, 'f'),  Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3108 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'p'),  Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3109 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'ym'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3110 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'mm'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3111 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'ds'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3112 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'hh'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),

    3113 : ( DG_TIER, Start, (CogQuest, Anywhere, 10, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
    3114 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),
    3115 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    3116 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    3117 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    3118 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),

    3119 : ( DG_TIER, Start, (CogQuest, Anywhere, 10, 'sc'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3120 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'pp'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3121 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'tw'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3122 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'bc'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3123 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'nc'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3124 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'mb'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),

    3125 : ( DG_TIER, Start, (CogQuest, Anywhere, 10, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    3126 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'b'),  Any, ToonHQ, Any, NA, DefaultDialog),
    3127 : ( DG_TIER, Start, (CogQuest, Anywhere, 8, 'dt'), Any, ToonHQ, Any, NA, DefaultDialog),
    3128 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    3129 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    3130 : ( DG_TIER, Start, (CogQuest, Anywhere, 6, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),

    3131 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 10, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    3132 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 15, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    3133 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 8, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    3134 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 12, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    3135 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 4, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    3136 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 6, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    3137 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 8, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    3138 : ( DG_TIER, Start, (CogLevelQuest, Anywhere, 12, 6), Any, ToonHQ, Any, NA, DefaultDialog),

    3139 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 6, 'm'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3140 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 6, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    3141 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 6, 'c'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3142 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 6, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    3143 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 10, 'm'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3144 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 10, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    3145 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 10, 'c'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3146 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.DaisyGardens, 10, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    3147 : ( DG_TIER, Start, (CogTrackQuest, Anywhere, 14, 'm'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3148 : ( DG_TIER, Start, (CogTrackQuest, Anywhere, 14, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    3149 : ( DG_TIER, Start, (CogTrackQuest, Anywhere, 14, 'c'), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3150 : ( DG_TIER, Start, (CogTrackQuest, Anywhere, 14, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    3151 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 1, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    3152 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    3153 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 3, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    3154 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 4, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    3155 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, 'm', 2), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3156 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, 's', 2), Any, ToonHQ, Any, NA, DefaultDialog),
    3157 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, 'c', 2), Any, ToonHQ, OBSOLETE, NA, DefaultDialog),
    3158 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, 'l', 2), Any, ToonHQ, Any, NA, DefaultDialog),

    # Artie of Artie Choke's Neckties wants you to take a silk necktie
    # to Vine and Dandy menswear.  The shopkeeper at Vine and Dandy
    # complains that the matching suit was stolen last week, and sends
    # you out to recover that.  Reward: +1 Laff.
    3200 : ( DG_TIER, Start, (VisitQuest,), Any, 5101, NA, (3201),
             TTLocalizer.QuestDialogDict[3200]),
    3201 : ( DG_TIER, Start, (DeliverItemQuest, 5001), 5101, 5206, NA, (3203),
             TTLocalizer.QuestDialogDict[3201]),
    3203 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 1, 5002, VeryHard, Any), Same, Same, 100, NA,
             TTLocalizer.QuestDialogDict[3203]),

    # The barber at Crop Top Barbers has lost a pair of scissors.  He
    # thinks a Bloodsucker stole it.  Reward: +1 Laff.
    3204 : ( DG_TIER, Start, (VisitQuest,), Any, 5106, NA, (3205),
             TTLocalizer.QuestDialogDict[3204]),
    3205 : ( DG_TIER, Start, (RecoverItemQuest, Anywhere, 1, 5003, Medium, 'b'), 5106, Same, 100, NA,
             TTLocalizer.QuestDialogDict[3205]),

    # The post officer in Compost Office complains that a bunch of
    # Double Talkers broke in and stole a stack of postcards from his
    # mailbox.  Recover all ten postcards.  Reward: +2 Laff.
    3206 : ( DG_TIER, Start, (VisitQuest,), Any, 5107, NA, (3207),
             TTLocalizer.QuestDialogDict[3206]),
    3207 : ( DG_TIER, Start, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 10, 5004, VeryEasy, 'dt'), 5107, Same, 101, NA,
             TTLocalizer.QuestDialogDict[3207]),

    # OBSOLETE: This quest has been made obsolete to make room for the Sellbot Cog HQ Quest
    # We've been getting complaints from the residents about all the
    # cold callers.  Thin these out a bit.  Then go after the
    # telemarketers too.  Reward: small bag (35 carry).
    3208 : ( DG_TIER, OBSOLETE, (CogQuest, ToontownGlobals.DaisyGardens, 10, 'cc'), Any, ToonHQ, NA, (3209),
             TTLocalizer.QuestDialogDict[3208]),
    3209 : ( DG_TIER, OBSOLETE, (CogQuest, ToontownGlobals.DaisyGardens, 10, 'tm'), Same, Same, 202, NA,
             TTLocalizer.QuestDialogDict[3209]),

    # OBSOLETE: This quest has been made obsolete to make room for the
    # Sellbot Cog HQ Quest. We've been getting complaints from the residents
    # about all the blood suckers.  Thin these out a bunch.  Reward: small
    # bag (35 carry).
    3247 : ( DG_TIER, OBSOLETE, (CogQuest, ToontownGlobals.DaisyGardens, 20, 'b'), Any, ToonHQ, 202, NA,
             TTLocalizer.QuestDialogDict[3247]),

    # Oh no, The Squirting Flower is out of flowers!  Bring them ten
    # of yours.  Then clear the street of cogs.  Reward: +1 Laff.
    3210 : ( DG_TIER, Start, (DeliverGagQuest, 10, ToontownBattleGlobals.SQUIRT_TRACK, 0), Any, 5207, NA, (3211),
             TTLocalizer.QuestDialogDict[3210]),
    3211 : ( DG_TIER, Cont, (CogQuest, 5200, 20, Any), Same, Same, 100, NA,
             TTLocalizer.QuestDialogDict[3211]),

    # OBSOLETE: This quest has been made obsolete to make room for the
    # Sellbot Cog HQ Quest Trellis the Truth has lost a lot of office
    # supplies.  Reward: small bag (35 carry).
    3212 : ( DG_TIER, OBSOLETE, (VisitQuest,), Any, 5208, NA, (3213),
             TTLocalizer.QuestDialogDict[3212]),
    3213 : ( DG_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 1, 5005, VeryHard, Any), 5208, Same, NA, (3214),
             TTLocalizer.QuestDialogDict[3213]),
    3214 : ( DG_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 1, 5006, VeryHard, Any), Same, Same, NA, (3215),
             TTLocalizer.QuestDialogDict[3214]),
    3215 : ( DG_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 1, 5007, VeryHard, Any), Same, Same, NA, (3216),
             TTLocalizer.QuestDialogDict[3215]),
    3216 : ( DG_TIER, OBSOLETE, (RecoverItemQuest, ToontownGlobals.DaisyGardens, 1, 5008, VeryHard, Any), Same, Same, 202, NA,
             TTLocalizer.QuestDialogDict[3216]),

    # We're studying sprockets from Sellbots.  Get us a sprocket from a
    # Name Dropper.  Then get one from a Glad Hander.  Finally, get one
    # from a Mover & Shaker.  Reward: +2 Laff.
    3217 : ( DG_TIER, Start, (RecoverItemQuest, Anywhere, 1, 5010, VeryEasy, 'nd'), ToonHQ, ToonHQ, NA, (3218),
             TTLocalizer.QuestDialogDict[3217]),
    3218 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5010, VeryHard, 'gh'), Same, Same, NA, (3219),
             TTLocalizer.QuestDialogDict[3218]),
    3219 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5010, Easy, 'ms'), Same, Same, 101, NA,
             TTLocalizer.QuestDialogDict[3219]),

    # We're studying sprockets from Lawbots.  Get us a sprocket from an
    # Ambulance Chaser.  Then get one from a Back Stabber.  Finally, get one
    # from a Spin Doctor.  Reward: +2 Laff.
    3244 : ( DG_TIER, Start, (RecoverItemQuest, Anywhere, 1, 5010, VeryEasy, 'ac'), ToonHQ, ToonHQ, NA, (3245),
             TTLocalizer.QuestDialogDict[3244]),
    3245 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5010, VeryHard, 'bs'), Same, Same, NA, (3246),
             TTLocalizer.QuestDialogDict[3245]),
    3246 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5010, VeryHard, 'sd'), Same, Same, 101, NA,
             TTLocalizer.QuestDialogDict[3246]),

    # The Squirting Flower wants you to set a good example for your
    # fellow toons with your squirt attacks.  Go clobber a bunch of
    # cogs.  Reward: +1 Laff.
    3220 : ( DG_TIER, Start, (VisitQuest,), Any, 5207, NA, (3221),
             TTLocalizer.QuestDialogDict[3220]),
    3221 : ( DG_TIER, Start, (CogQuest, ToontownGlobals.DaisyGardens, 20, Any), 5207, Same, 100, NA,
             TTLocalizer.QuestDialogDict[3221]),

    # Demonstrate your skills.  First, take back two one-story
    # buildings; then two two-story buildings; then two three-story
    # buildings.  Reward: carry three quests.
    3222 : ( DG_TIER, Start, (BuildingQuest, Anywhere, 2, Any, 1), ToonHQ, ToonHQ, NA, (3223),
             TTLocalizer.QuestDialogDict[3222]),
    3223 : ( DG_TIER, Cont, (BuildingQuest, Anywhere, 2, Any, 2), Same, Same, NA, (3224),
             TTLocalizer.QuestDialogDict[3223]),
    3224 : ( DG_TIER, Cont, (BuildingQuest, Anywhere, 2, Any, 3), Same, Same, 501, NA,
             TTLocalizer.QuestDialogDict[3224]),

    # The cogs have frightened away The Dew Drop Inn's delivery
    # person.  They need someone to deliver a salad to one of several
    # possible neighborhood persons who ordered one.  Then defeat some
    # cogs.  Reward: +1 Laff.
    3225 : ( DG_TIER, Start, (VisitQuest,), Any, 5108, NA, (3226, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3234),
             TTLocalizer.QuestDialogDict[3225]),
    3226 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5201, NA, (3235),
             TTLocalizer.QuestDialog_3225),
    3227 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5203, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3228 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5204, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3229 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5205, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3230 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5102, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3231 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5103, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3232 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5104, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3233 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5105, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3234 : ( DG_TIER, Start, (DeliverItemQuest, 5011), 5108, 5207, NA, (3235), 
             TTLocalizer.QuestDialog_3225),
    3235 : ( DG_TIER, Cont, (CogQuest, ToontownGlobals.DaisyGardens, 10, Any), Same, 5108, 100, NA,
             TTLocalizer.QuestDialogDict[3235]),
               
    # OBSOLETE: This quest has been made obsolete to make room for the Sellbot Cog HQ Quest
    # Too many Lawbots!  Reclaim 3 lawbot buildings.  Oops, now too
    # many Sellbots!  Reclaim 3 sellbot buildings.  Reward: 80 max jellybeans.
    3236 : ( DG_TIER, OBSOLETE, (BuildingQuest, Anywhere, 3, 'l', 2), Any, ToonHQ, NA, (3237),
             TTLocalizer.QuestDialogDict[3236]),
    3237 : ( DG_TIER, OBSOLETE, (BuildingQuest, Anywhere, 3, 's', 2), Same, Same, 702, NA, 
             TTLocalizer.QuestDialogDict[3237]),
             
    # The Mingler has stolen the Key to Daisy Gardens.  Reclaim it
    # from him.  Oops, not that key, some other one!  Reward: teleport
    # access to Daisy Gardens.
    3238 : ( DG_TIER, Start, (RecoverItemQuest, Anywhere, 1, 2, VeryEasy, 'm'), Any, ToonHQ, NA, (3239),
             TTLocalizer.QuestDialogDict[3238]),
    3239 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5012, Hard, 'm'), Same, Same, 302, NA,
             TTLocalizer.QuestDialogDict[3239]),

    # A Legal Eagle has stolen the Key to Daisy Gardens.  Reclaim it
    # from him.  Oops, not that key, some other one!  Reward: teleport
    # access to Daisy Gardens.
    3242 : ( DG_TIER, Start, (RecoverItemQuest, Anywhere, 1, 2, VeryEasy, 'le'), Any, ToonHQ, NA, (3243),
             TTLocalizer.QuestDialogDict[3242]),
    3243 : ( DG_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 5012, Hard, 'le'), Same, Same, 302, NA,
             TTLocalizer.QuestDialogDict[3243]),

    # OBSOLETE: These two quests have been removed to make way for the Cog HQ quests
    # A Legal Eagle stole a bag of bird seed from Bud's Bird Seed.
    # Reward: +3 Laff.
    3240 : ( DG_TIER, OBSOLETE, (RecoverItemQuest, Anywhere, 1, 5009, Hard, 'le'), Any, 5103, 102, NA,
             TTLocalizer.QuestDialogDict[3240]),

    # Recover 5 3+-story buildings.  Reward: +3 Laff.
    3241 : ( DG_TIER, OBSOLETE, (BuildingQuest, Anywhere, 5, Any, 3), Any, ToonHQ, 102, NA,
             TTLocalizer.QuestDialogDict[3241]),

    # Visit Detective Lima, defeat 5 Sellbots in Sellbot HQ, visit Judge
    # McIntosh, recover Sellbot HQ blueprints, deliver blueprints to
    # Detective Lima. Reward: 35 carry
    3250 : ( DG_TIER, Start, (VisitQuest,), Any, 5317, NA, 3251,
             TTLocalizer.QuestDialogDict[3250]),
    3251 : ( DG_TIER, Start, (CogTrackQuest, ToontownGlobals.SellbotHQ, 5, 's'), 5317, Same, NA, 3252,
             TTLocalizer.QuestDialogDict[3251]),
    3252 : ( DG_TIER, Cont, (VisitQuest,), Same, 5311, NA, 3253,
             TTLocalizer.QuestDialogDict[3252]),
    3253 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.SellbotHQ, 1, 5013, Medium, 's', 'track'),
             Same, Same, NA, 3254, TTLocalizer.QuestDialogDict[3253]),
    3254 : ( DG_TIER, Cont, (DeliverItemQuest, 5013), Same, 5317, 202, NA,
             TTLocalizer.QuestDialogDict[3254]),

    # Quest: Sellbot HQ Memos
    # Reward: +3 laff points (102)
    # Splits into 3 separate NPCs to avoid crowding
    3255 : ( DG_TIER, Start, (VisitQuest,), Any, 5314, NA, 3258,
             TTLocalizer.QuestDialogDict[3255]),
    3256 : ( DG_TIER, Start, (VisitQuest,), Any, 5315, NA, 3258,
             TTLocalizer.QuestDialogDict[3256]),
    3257 : ( DG_TIER, Start, (VisitQuest,), Any, 5316, NA, 3258,
             TTLocalizer.QuestDialogDict[3257]),
    3258 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.SellbotHQ, 1, 5014, VeryEasy, 's', 'track'),
             Same, Same, NA, 3259, TTLocalizer.QuestDialogDict[3258]),
    3259 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.SellbotHQ, 1, 5015, Easy, 's', 'track'),
             Same, Same, NA, 3260, TTLocalizer.QuestDialogDict[3259]),
    3260 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.SellbotHQ, 1, 5016, Easy, 's', 'track'),
             Same, Same, NA, 3261, TTLocalizer.QuestDialogDict[3260]),
    3261 : ( DG_TIER, Cont, (RecoverItemQuest, ToontownGlobals.SellbotHQ, 1, 5017, Medium, 's', 'track'),
             Same, Same, 102, NA, TTLocalizer.QuestDialogDict[3261]),

    # Visit Coach Zucchini, Then defeat the Sellbot HQ Factory.
    # Reward: 80 max jellybeans (702)
    3262 : ( DG_TIER, Start, (VisitQuest,), Any, 5313, NA, 3263,
             TTLocalizer.QuestDialogDict[3262]),
    3263 : ( DG_TIER, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), 5313, 5313, 702, NA,
             TTLocalizer.QuestDialogDict[3263]),

    # Next DG_TIER id: 3264

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    3500 : ( DG_TIER, Start, (CogQuest, ToontownGlobals.DaisyGardens, 25, Any), Any, ToonHQ, NA, (3501), DefaultDialog),
    3501 : ( DG_TIER, Cont, (DeliverItemQuest, 1000), Any, 5007, 1000, NA, DefaultDialog),
    
    # Minnies melodyland
    # We will pick one of these quests depending on what the avatar chose previously
    # DO NOT change these quest indexes, as they are keys used in chooseQuest()
    4001 : ( MM_TIER, Start, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.HEAL_TRACK,),
             Any, ToonHQ, 400, NA,
             TTLocalizer.QuestDialogDict[4001]),
             
    4002 : ( MM_TIER, Start, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.SOUND_TRACK,),
             Any, ToonHQ, 400, NA,
             TTLocalizer.QuestDialogDict[4002]),


    # Optional quests to do while working on the bottleneck quest
    4010 : ( MM_TIER, Start, (CogQuest, Anywhere, 16, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4011 : ( MM_TIER, Start, (CogQuest, Anywhere, 18, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4012 : ( MM_TIER, Start, (CogQuest, Anywhere, 20, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4013 : ( MM_TIER, Start, (CogQuest, Anywhere, 22, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4014 : ( MM_TIER, Start, (CogQuest, Anywhere, 24, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4015 : ( MM_TIER, Start, (CogQuest, Anywhere, 26, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4016 : ( MM_TIER, Start, (CogQuest, Anywhere, 28, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4017 : ( MM_TIER, Start, (CogQuest, Anywhere, 30, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4018 : ( MM_TIER, Start, (CogQuest, Anywhere, 32, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4019 : ( MM_TIER, Start, (CogQuest, Anywhere, 34, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4020 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 20, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4021 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 25, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4022 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 16, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4023 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 20, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4024 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4025 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4026 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 16, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4027 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 18, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4028 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 20, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4029 : ( MM_TIER, Start, (CogLevelQuest, Anywhere, 24, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    4030 : ( MM_TIER, Start, (CogQuest, Anywhere, 45, Any), Any, ToonHQ, NA, (4031), DefaultDialog),
    4031 : ( MM_TIER, Cont, (DeliverItemQuest, 1000), Any, 4008, 1000, NA, DefaultDialog),
    # Sellbot HQ quests
    4040 : ( MM_TIER, Start, (CogQuest, ToontownGlobals.SellbotHQ, 6, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4041 : ( MM_TIER, Start, (CogQuest, ToontownGlobals.SellbotHQ, 6, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4042 : ( MM_TIER, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 3, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4043 : ( MM_TIER, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 3), Any, ToonHQ, Any, NA, DefaultDialog),


    # MM is a little heavy on money (cashbot) cogs, but has a fairly
    # good cog distribution otherwise.  The sellbots in MM are
    # mostly level 2..4, while other type cogs are level 3..6.
    
    4101 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 16, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4102 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 18, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4103 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 20, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4104 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 24, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4105 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 28, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4106 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 32, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    4107 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 20, 'f'),  Any, ToonHQ, Any, NA, DefaultDialog),
    4108 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'p'),  Any, ToonHQ, Any, NA, DefaultDialog),
    4109 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'ym'), Any, ToonHQ, Any, NA, DefaultDialog),
    4110 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    4111 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    4112 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),

    4113 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 20, 'cc'), Any, ToonHQ, Any, NA, DefaultDialog),
    4114 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),
    4115 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    4116 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    4117 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'ms'), None, ToonHQ, Any, NA, DefaultDialog), # don't use
    4118 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'tf'), None, ToonHQ, Any, NA, DefaultDialog), # don't use

    4119 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 20, 'sc'), Any, ToonHQ, Any, NA, DefaultDialog),
    4120 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
    4121 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    4122 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    4123 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    4124 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),

    4125 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 20, 'bf'), Any, ToonHQ, Any, NA, DefaultDialog),
    4126 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'b'),  Any, ToonHQ, Any, NA, DefaultDialog),
    4127 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 16, 'dt'), Any, ToonHQ, Any, NA, DefaultDialog),
    4128 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    4129 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    4130 : ( MM_TIER+1, Start, (CogQuest, Anywhere, 12, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),

    4131 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 20, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4132 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 25, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4133 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 16, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4134 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 20, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4135 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4136 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4137 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 16, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4138 : ( MM_TIER+1, Start, (CogLevelQuest, Anywhere, 24, 6), Any, ToonHQ, Any, NA, DefaultDialog),

    4139 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 15, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    4140 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 15, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    4141 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 15, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    4142 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 15, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    4143 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 24, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    4144 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 24, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    4145 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 24, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    4146 : ( MM_TIER+1, Start, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 24, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    4147 : ( MM_TIER+1, Start, (CogTrackQuest, Anywhere, 30, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    4148 : ( MM_TIER+1, Start, (CogTrackQuest, Anywhere, 30, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    4149 : ( MM_TIER+1, Start, (CogTrackQuest, Anywhere, 30, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    4150 : ( MM_TIER+1, Start, (CogTrackQuest, Anywhere, 30, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    4151 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 1, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4152 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 2, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4153 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 3, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4154 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 4, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4155 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 3, 'm', 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4156 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 3, 's', 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4157 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 3, 'c', 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4158 : ( MM_TIER+1, Start, (BuildingQuest, Anywhere, 3, 'l', 3), Any, ToonHQ, Any, NA, DefaultDialog),

    # Sellbot HQ quests
    4160 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.SellbotHQ, 10, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4161 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.SellbotHQ, 12, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4162 : ( MM_TIER+1, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 6, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4163 : ( MM_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    4164 : ( MM_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    4165 : ( MM_TIER+1, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4166 : ( MM_TIER+1, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),

    # 203: Medium bag
    # Tom's collecting info on how many musical instruments have gone missing since the
    # cog invasion. Run around to the following vendors and get inventory sheets:
    #   Tina's Concertina Concerts, Yuki's Ukelele's, Fifi's Fiddles
    4200 : ( MM_TIER+1, Start, (VisitQuest,), Any, 4101, NA, 4201,
             TTLocalizer.QuestDialogDict[4200]),
    4201 : ( MM_TIER+1, Start, (VisitQuest,), 4101, 4201, NA, 4202,
             TTLocalizer.QuestDialogDict[4201]),
    4202 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4001), Same, 4101, NA, 4203,
             TTLocalizer.QuestDialogDict[4202]),
    4203 : ( MM_TIER+1, Cont, (VisitQuest,), Same, 4301, NA, 4204,
             TTLocalizer.QuestDialogDict[4203]),
    4204 : ( MM_TIER+1, Cont, (CogQuest, ToontownGlobals.MinniesMelodyland, 10, Any), Same, Same, NA, 4205,
             TTLocalizer.QuestDialogDict[4204]),
    4205 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4002), Same, 4101, NA, 4206,
             TTLocalizer.QuestDialogDict[4205]),
    4206 : ( MM_TIER+1, Cont, (VisitQuest,), Same, 4102, NA, 4207,
             TTLocalizer.QuestDialogDict[4206]),
    4207 : ( MM_TIER+1, Cont, (VisitQuest,), Same, 4108, NA, 4208,
             TTLocalizer.QuestDialogDict[4207]),
    4208 : ( MM_TIER+1, Cont, (DeliverGagQuest, 1, ToontownBattleGlobals.THROW_TRACK, 4), Same, Same, NA, 4209,
             TTLocalizer.QuestDialogDict[4208]),
    4209 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4003), Same, 4102, NA, 4210,
             TTLocalizer.QuestDialogDict[4209]),
    4210 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4004), Same, 4101, 203, NA,
             TTLocalizer.QuestDialogDict[4210]),
    
    # 303: MM teleport access
    # Dr. Fret is having trouble getting customers. First he thinks its the Number Crunchers
    # that are scaring everyone away. Then he think its cashbots in general. Finally he asks
    # you take over a cog building before he remembers that he never really had any customers
    # to speak of...
    4211 : ( MM_TIER+1, Start, (VisitQuest,), ToonHQ, 4103, NA, 4212,
             TTLocalizer.QuestDialogDict[4211]),
    4212 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 10, 'nc'), 4103, Same, NA, 4213,
             TTLocalizer.QuestDialogDict[4212]),
    4213 : ( MM_TIER+1, Cont, (CogTrackQuest, ToontownGlobals.MinniesMelodyland, 20, 'm'), Same, Same, NA, 4214,
             TTLocalizer.QuestDialogDict[4213]),
    4214 : ( MM_TIER+1, Cont, (BuildingQuest, Anywhere, 1, 'm', Any), Same, Same, 303, NA,
             TTLocalizer.QuestDialogDict[4214]),

    # 703: max money = 100
    # Gladhanders' have made off with Anna's customers' travel tickets. Retrieve them and
    # then deliver them to the following people:
    #   Lumber Jack, Tabitha, Barry 
    4215 : ( MM_TIER+1, Start, (VisitQuest,), Any, 4302, NA, 4216,
              TTLocalizer.QuestDialogDict[4215]),
    4216 : ( MM_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 4005, VeryHard, 'gh'), 4302, Same, NA, 4217,
              TTLocalizer.QuestDialogDict[4216]),
    4217 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4005), Same, 4203, NA, 4218,
             TTLocalizer.QuestDialogDict[4217]),
    4218 : ( MM_TIER+1, Cont, (VisitQuest,), Any, 4302, NA, 4219,
             TTLocalizer.QuestDialogDict[4218]),
    4219 : ( MM_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 4006, VeryHard, 'gh'), Same, Same, NA, 4220,
             TTLocalizer.QuestDialogDict[4219]),
    4220 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4006), Same, 4308, NA, 4221,
             TTLocalizer.QuestDialogDict[4220]),
    4221 : (MM_TIER+1, Cont, (VisitQuest,), Any, 4302, NA, 4222,
            TTLocalizer.QuestDialogDict[4221]),
    4222 : ( MM_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 4007, VeryHard, 'gh'), Same, Same, NA, 4223,
             TTLocalizer.QuestDialogDict[4222]),
    4223 : ( MM_TIER+1, Cont, (DeliverItemQuest, 4007), Same, 4202, NA, 4224,
             TTLocalizer.QuestDialogDict[4223]),
    4224 : (MM_TIER+1, Cont, (VisitQuest,), Any, 4302, 703, NA,
            TTLocalizer.QuestDialogDict[4224]),

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    4500 : ( MM_TIER+1, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 40, Any), Any, ToonHQ, NA, (4501), DefaultDialog),
    4501 : ( MM_TIER+1, Cont, (DeliverItemQuest, 1000), Any, 4008, 1000, NA, DefaultDialog),
 
    # 902: track completion
    # Visit Leo at Leo's Fenders. He's going to give a concert tonight and needs his castanets
    # polished. Bring them to Carlos who says he can do it, but needs some squid ink to make
    # them nice and black. After you return with the squid ink he will polish them but it will
    # take some time. Go reclaim a one story building in the mean time. Once you return the
    # polished castanets to Leo he asks you to go pick up the lyrics to "A Beatnik Christmas"
    # from Hedy at Lousy Lyrics. Hedy doesn't have a copy, but offers to transcribe it from
    # memory if you will reclaim a two story building on her street. Turns out it is taking
    # longer than she thought to remember the lyrics. Go reclaim a three story building. After
    # this she gives you the lyrics to take to Leo. Leo is overjoyed and finishes your track.
    #902 : ( MM_TIER+2, Start, (CogQuest, ToontownGlobals.MinniesMelodyland, 10, Any), Any, ToonHQ, 900, NA, DefaultDialog),
    902 : ( MM_TIER+2, Start, (VisitQuest,), Any, 4303, NA, 4903,
            TTLocalizer.QuestDialogDict[902]),
    4903 : ( MM_TIER+2, Start, (DeliverItemQuest, 4008), 4303, 4109, NA, 4904,
            TTLocalizer.QuestDialogDict[4903]),
    4904 : ( MM_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 4009, VeryHard, AnyFish), Same, Same, NA, 4905,
             TTLocalizer.QuestDialogDict[4904]),
    4905 : ( MM_TIER+2, Cont, (BuildingQuest, Anywhere, 1, Any, 1), Same, Same, NA, 4906,
             TTLocalizer.QuestDialogDict[4905]),
    4906 : ( MM_TIER+2, Cont, (DeliverItemQuest, 4010), Same, 4303, NA, 4907, 
             TTLocalizer.QuestDialogDict[4906]),
    4907 : ( MM_TIER+2, Cont, (VisitQuest,), Same, 4208, NA, 4908,
             TTLocalizer.QuestDialogDict[4907]),
    4908 : ( MM_TIER+2, Cont, (BuildingQuest, Anywhere, 1, Any, 2), Same, Same, NA, 4909,
             TTLocalizer.QuestDialogDict[4908]),
    4909 : ( MM_TIER+2, Cont, (BuildingQuest, Anywhere, 1, Any, 3), Same, Same, NA, 4910,
             TTLocalizer.QuestDialogDict[4909]),
    4910 : ( MM_TIER+2, Cont, (DeliverItemQuest, 4011), Same, 4303, 900, NA,
             TTLocalizer.QuestDialogDict[4910]),


    # Optional quests to do while working on the bottleneck quest
    4810 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 16, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4811 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 18, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4812 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 20, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4813 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 22, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4814 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 24, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4815 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 26, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4816 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 28, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4817 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 30, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4818 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 32, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4819 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 34, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4820 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 20, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4821 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 25, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    4822 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 16, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4823 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 20, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4824 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4825 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4826 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 16, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4827 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 18, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4828 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 20, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    4829 : ( MM_TIER+2, Start, (CogLevelQuest, Anywhere, 24, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    4830 : ( MM_TIER+2, Start, (CogQuest, Anywhere, 45, Any), Any, ToonHQ, NA, (4831), DefaultDialog),
    4831 : ( MM_TIER+2, Cont, (DeliverItemQuest, 1000), Any, 4008, 1000, NA, DefaultDialog),
    # Sellbot HQ quests
    4840 : ( MM_TIER+2, Start, (CogQuest, ToontownGlobals.SellbotHQ, 12, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4841 : ( MM_TIER+2, Start, (CogQuest, ToontownGlobals.SellbotHQ, 15, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    4842 : ( MM_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 12, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    4843 : ( MM_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4844 : ( MM_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    4845 : ( MM_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    4846 : ( MM_TIER+2, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4847 : ( MM_TIER+2, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 3, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    4848 : ( MM_TIER+2, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),

    # The Brrrgh
    # We will pick one of these quests depending on what the avatar chose previously
    5247 : ( BR_TIER, Start, (VisitQuest,), Any, 3112, NA, (5248),
             TTLocalizer.QuestDialogDict[5247]),
    5248 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 10, 8), 3112, Same, NA, (5249),
             TTLocalizer.QuestDialogDict[5248]),
    5249 : ( BR_TIER, Cont, (RecoverItemQuest, Anywhere, 3, 3018, VeryHard, AnyFish), Same, Same, NA, (5250, 5258, 5259, 5260),
             TTLocalizer.QuestDialogDict[5249]),
    5250 : ( BR_TIER, Cont, (BuildingQuest, Anywhere, 2, "l", 4), Same, Same, NA, (5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008),
             TTLocalizer.QuestDialogDict[5250]),
    5258 : ( BR_TIER, Cont, (BuildingQuest, Anywhere, 2, "c", 4), Same, Same, NA, (5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008),
             TTLocalizer.QuestDialogDict[5258]),
    5259 : ( BR_TIER, Cont, (BuildingQuest, Anywhere, 2, "m", 4), Same, Same, NA, (5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008),
             TTLocalizer.QuestDialogDict[5259]),
    5260 : ( BR_TIER, Cont, (BuildingQuest, Anywhere, 2, "s", 4), Same, Same, NA, (5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008),
             TTLocalizer.QuestDialogDict[5260]),
    5001 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.SOUND_TRACK,
                          ToontownBattleGlobals.DROP_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5002 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.SOUND_TRACK,
                          ToontownBattleGlobals.LURE_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5003 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.HEAL_TRACK,
                          ToontownBattleGlobals.DROP_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5004 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.HEAL_TRACK,
                          ToontownBattleGlobals.LURE_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5005 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.SOUND_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5006 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.HEAL_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5007 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.DROP_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),

    5008 : ( BR_TIER, Cont, (TrackChoiceQuest,
                          ToontownBattleGlobals.TRAP_TRACK,
                          ToontownBattleGlobals.LURE_TRACK,),
             Same, Same, 400, NA, TTLocalizer.TheBrrrghTrackQuestDict),
    
    # Optional quests to do while working on the bottleneck quest
    5020 : ( BR_TIER, Start, (CogQuest, Anywhere, 36, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5021 : ( BR_TIER, Start, (CogQuest, Anywhere, 38, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5022 : ( BR_TIER, Start, (CogQuest, Anywhere, 40, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5023 : ( BR_TIER, Start, (CogQuest, Anywhere, 42, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5024 : ( BR_TIER, Start, (CogQuest, Anywhere, 44, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5025 : ( BR_TIER, Start, (CogQuest, Anywhere, 46, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5026 : ( BR_TIER, Start, (CogQuest, Anywhere, 48, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5027 : ( BR_TIER, Start, (CogQuest, Anywhere, 50, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5028 : ( BR_TIER, Start, (CogQuest, Anywhere, 52, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5029 : ( BR_TIER, Start, (CogQuest, Anywhere, 54, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5030 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 25, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5031 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 30, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5032 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 35, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5033 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 6,  7), Any, ToonHQ, Any, NA, DefaultDialog),
    5034 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 10, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5035 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 20, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5036 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 2,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5037 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 8,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5038 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 10,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5039 : ( BR_TIER, Start, (CogLevelQuest, Anywhere, 12,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    5040 : ( BR_TIER, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 75, Any), Any, ToonHQ, NA, (5041), DefaultDialog),
    5041 : ( BR_TIER, Cont, (DeliverItemQuest, 1000), Any, 3008, 1000, NA, DefaultDialog),
    # Elder quests
    5060 : ( BR_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 5, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5061 : ( BR_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 5, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5062 : ( BR_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 5, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5063 : ( BR_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 5, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5064 : ( BR_TIER, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5065 : ( BR_TIER, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5066 : ( BR_TIER, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5067 : ( BR_TIER, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    # Sellbot HQ quests
    5070 : ( BR_TIER, Start, (CogQuest, ToontownGlobals.SellbotHQ, 20, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5071 : ( BR_TIER, Start, (CogQuest, ToontownGlobals.SellbotHQ, 22, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5072 : ( BR_TIER, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 15, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5073 : ( BR_TIER, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5074 : ( BR_TIER, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 12, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5075 : ( BR_TIER, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 8, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5076 : ( BR_TIER, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5077 : ( BR_TIER, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5078 : ( BR_TIER, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5079 : ( BR_TIER, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5080 : ( BR_TIER, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    5081 : ( BR_TIER, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 5, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5082 : ( BR_TIER, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 2, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5083 : ( BR_TIER, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5084 : ( BR_TIER, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),


    # The Brrgh is heavy on corporate (bossbot) cogs, light on legal.
    # All cogs are level 5..7.
    5101 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 36, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5102 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 40, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5103 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 42, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5104 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 45, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5105 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 50, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5106 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 55, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    5107 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 25, 'p'),  Any, ToonHQ, Any, NA, DefaultDialog),
    5108 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'ym'), Any, ToonHQ, Any, NA, DefaultDialog),
    5109 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    5110 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    5111 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),
    5112 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 8,  'cr'), Any, ToonHQ, Any, NA, DefaultDialog),

    5113 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 25, 'tm'), Any, ToonHQ, Any, NA, DefaultDialog),
    5114 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    5115 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    5116 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    5117 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),
    5118 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 8,  'm'),  Any, ToonHQ, Any, NA, DefaultDialog),

    5119 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 25, 'pp'), Any, ToonHQ, Any, NA, DefaultDialog),
    5120 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    5121 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    5122 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    5123 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),
    5124 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 8,  'ls'), Any, ToonHQ, Any, NA, DefaultDialog),

    5125 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 25, 'b'),  Any, ToonHQ, Any, NA, DefaultDialog),
    5126 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'dt'), Any, ToonHQ, Any, NA, DefaultDialog),
    5127 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 20, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    5128 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    5129 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 15, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),
    5130 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 8,  'le'), Any, ToonHQ, Any, NA, DefaultDialog),

    5131 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 25, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5132 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 30, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5133 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 35, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5134 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 6,  7), Any, ToonHQ, Any, NA, DefaultDialog),
    5135 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 10, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5136 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 20, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5137 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 2,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5138 : ( BR_TIER+1, Start, (CogLevelQuest, Anywhere, 8,  8), Any, ToonHQ, Any, NA, DefaultDialog),

    5139 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 32, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    5140 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 32, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    5141 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 32, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    5142 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 32, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    5143 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 40, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    5144 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 40, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    5145 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 40, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    5146 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 40, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    5147 : ( BR_TIER+1, Start, (CogTrackQuest, Anywhere, 45, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    5148 : ( BR_TIER+1, Start, (CogTrackQuest, Anywhere, 45, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    5149 : ( BR_TIER+1, Start, (CogTrackQuest, Anywhere, 45, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    5150 : ( BR_TIER+1, Start, (CogTrackQuest, Anywhere, 45, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    5151 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 8, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    5152 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 2, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5153 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 5, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5154 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 6, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5155 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 2, 'm', 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5156 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 2, 's', 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5157 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 2, 'c', 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5158 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 2, 'l', 4), Any, ToonHQ, Any, NA, DefaultDialog),

    # Sellbot HQ quests
    5160 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.SellbotHQ, 22, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5161 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.SellbotHQ, 25, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5162 : ( BR_TIER+1, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 16, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5163 : ( BR_TIER+1, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 12, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5164 : ( BR_TIER+1, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 14, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5165 : ( BR_TIER+1, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 10, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5166 : ( BR_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5167 : ( BR_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5168 : ( BR_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5169 : ( BR_TIER+1, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5170 : ( BR_TIER+1, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    5171 : ( BR_TIER+1, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 6, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5172 : ( BR_TIER+1, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 3, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5173 : ( BR_TIER+1, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5174 : ( BR_TIER+1, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),

    # A Downsizer stole Chicken Boy's soccer ball.  If you get it back to him
    # your reward is +1 HP.
    5200 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3110, NA, (5201, 5261, 5262, 5263),
             TTLocalizer.QuestDialogDict[5200]),
    5201 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 3001, VeryHard, 'hh'), 3110, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5201]),
    5261 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 3001, VeryHard, 'tf'), 3110, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5261]),
    5262 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 3001, VeryHard, 'mb'), 3110, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5262]),
    5263 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 3001, VeryHard, 'sd'), 3110, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5263]),

    # Toboggan Ted and his toboggan team crashed while racing and now
    # are a bunch of absent-minded knuckleheads.  Ted sends you to each 
    # team member looking for his large bag.  Each guy has misplaced something
    # that might remind him where the bag is or who another team member is.
    # Your eventual reward is the large bag (max gag = 50).
    5202 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3108, NA, (5203),
             TTLocalizer.QuestDialogDict[5202]),
    5203 : ( BR_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3002, VeryHard, Any), 3108, Same, NA, (5204),
             TTLocalizer.QuestDialogDict[5203]),
    5204 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3205, NA, (5205),
             TTLocalizer.QuestDialogDict[5204]),
    5205 : ( BR_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 3, 3003, Hard, AnyFish), Same, Same, NA, (5206),
             TTLocalizer.QuestDialogDict[5205]),
    5206 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3210, NA, (5207),
             TTLocalizer.QuestDialogDict[5206]),
    5207 : ( BR_TIER+1, Cont, (BuildingQuest, Anywhere, 5, Any, 4), Same, Same, NA, (5208),
             TTLocalizer.QuestDialogDict[5207]),
    5208 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3114, NA, (5209),
             TTLocalizer.QuestDialogDict[5208]),
    5209 : ( BR_TIER+1, Cont, (CogLevelQuest, Anywhere, 20, 7), Same, Same, 204, NA,
             TTLocalizer.QuestDialogDict[5209]),

    # Vidalia Va Voom is in love with Snooty Sinjin.  She writes him a love
    # letter, which gets stolen by the Cogs.  Return the letter to Vidalia
    # who will then ask to deliver it to Sinjin.  Sinjin can't be bothered
    # because 10 wiener dogs have gone missing from his kennel.  Once his dogs
    # are returned, he hands over an IOU for an engagement ring.  Deliver the
    # IOU to Creepy Carl, who wants some fish in exchange for producing the
    # ring.  Deliver the ring to Vidalia to get max money = 120.
    5210 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3206, NA, (5211, 5264, 5265, 5266),
             TTLocalizer.QuestDialogDict[5210]),
    5211 : ( BR_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3004, Medium, 'le'), 3206, Same, NA, (5212),
             TTLocalizer.QuestDialogDict[5211]),
    5264 : ( BR_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3004, Hard, 'ls'), 3206, Same, NA, (5212),
             TTLocalizer.QuestDialogDict[5264]),
    5265 : ( BR_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3004, Hard, 'm'), 3206, Same, NA, (5212),
             TTLocalizer.QuestDialogDict[5265]),
    5266 : ( BR_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3004, Hard, 'cr'), 3206, Same, NA, (5212),
             TTLocalizer.QuestDialogDict[5266]),
    5212 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3004), Same, 3111, NA, (5213),
             TTLocalizer.QuestDialogDict[5212]),
    5213 : ( BR_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 10, 3005, Hard, Any), Same, Same, NA, (5214),
             TTLocalizer.QuestDialogDict[5213]),
    5214 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3119, NA, (5215),
             TTLocalizer.QuestDialogDict[5214]),
    5215 : ( BR_TIER+1, Cont, (CogLevelQuest, Anywhere, 10, 8), Same, Same, NA, (5216),
             TTLocalizer.QuestDialogDict[5215]),
    5216 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3006), Same, 3206, 704, NA,
             TTLocalizer.QuestDialogDict[5216]),

    # Hysterical Harry is flipping out.  He asks to help clear out all the
    # Micromanagers, then all the x's, then all the x's, but nothing seems
    # to calm him.  Maybe Fanny Freezes can cook him up a potion to calm him
    # down.  Fanny asks for a series of ingredients and then gives you
    # the concoction to take to Harry.  Harry drinks it and gives you the 
    # max quest = 4.
    5217 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3113, NA, (5218),
             TTLocalizer.QuestDialogDict[5217]),
    5218 : ( BR_TIER+1, Start, (CogQuest, Anywhere, 10, 'm'), 3113, Same, NA, (5219),
             TTLocalizer.QuestDialogDict[5218]),
    5219 : ( BR_TIER+1, Cont, (CogQuest, Anywhere, 10, 'cr'), Same, Same, NA, (5220),
             TTLocalizer.QuestDialogDict[5219]),
    5220 : ( BR_TIER+1, Cont, (CogQuest, Anywhere, 10, 'ls'), Same, Same, NA, (5221),
             TTLocalizer.QuestDialogDict[5220]),
    5221 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3211, NA, (5222),
             TTLocalizer.QuestDialogDict[5221]),
    5222 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 2, 3007, Hard, AnyFish), Same, Same, NA, (5223),
             TTLocalizer.QuestDialogDict[5222]),
    5223 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3008), Same, 3113, NA, (5224),
             TTLocalizer.QuestDialogDict[5223]),
    5224 : ( BR_TIER+1, Cont, (CogQuest, Anywhere, 5, 'le'), Same, Same, 502, NA,
             TTLocalizer.QuestDialogDict[5224]),

    # Gus Gooseburger wants to reconcile with Grumpy Phil, with your help.
    # You see, Gus baked him some turnip bread which caused Grumpy Phil to
    # break a tooth.  Phil has kept the tooth, but if you delivered it to 
    # Dr. Mumbleface he might be able to repair it.  Wacky comedy ensues when
    # Dr. Mumbleface loses the repaired tooth.  Finally, Phil gets his tooth
    # and lightens up on poor Gus.  Gus responds by baking a loaf of pine cone
    # bread, which breaks another one of Phil's teeth.  You reward is 
    # teleport to the Brrrgh.
    5225 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3106, NA, (5226),
             TTLocalizer.QuestDialogDict[5225]),
    5226 : ( BR_TIER+1, Start, (BuildingQuest, Anywhere, 3, 'm', 4), 3106, Same, NA, (5227),
             TTLocalizer.QuestDialogDict[5226]),
    5227 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3208, NA, (5228),
             TTLocalizer.QuestDialogDict[5227]),
    5228 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3009), Same, 3207, NA, (5229, 5267, 5268, 5269),
             TTLocalizer.QuestDialogDict[5228]),
    5229 : ( BR_TIER+1, Cont, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 8, 'm'), Same, Same, NA, (5230),
             TTLocalizer.QuestDialogDict[5229]),
    5267 : ( BR_TIER+1, Cont, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 8, 's'), Same, Same, NA, (5230),
             TTLocalizer.QuestDialogDict[5267]),
    5268 : ( BR_TIER+1, Cont, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 8, 'l'), Same, Same, NA, (5230),
             TTLocalizer.QuestDialogDict[5268]),
    5269 : ( BR_TIER+1, Cont, (CogTrackQuest, ToontownGlobals.TheBrrrgh, 8, 'c'), Same, Same, NA, (5230, 5270, 5271, 5272),
             TTLocalizer.QuestDialogDict[5269]),
    5230 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3010, Hard, 'rb'), Same, Same, NA, (5231),
             TTLocalizer.QuestDialogDict[5230]),
    5270 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3010, Hard, 'tbc'), Same, Same, NA, (5231),
             TTLocalizer.QuestDialogDict[5270]),
    5271 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3010, Hard, 'mh'), Same, Same, NA, (5231),
             TTLocalizer.QuestDialogDict[5271]),
    5272 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3010, Medium, 'bw'), Same, Same, NA, (5231),
             TTLocalizer.QuestDialogDict[5272]),
    5231 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3010), Same, 3208, NA, (5232),
             TTLocalizer.QuestDialogDict[5231]),
    5232 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3106, NA, (5233),
             TTLocalizer.QuestDialogDict[5232]),
    5233 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3011), Same, 3208, 304, NA,
             TTLocalizer.QuestDialogDict[5233]),

    # Sweaty Pete needs a shower.  First, he needs a gear from a Micromanager
    # to fix a leaky pipe.  Then he needs the companionship of a rubber ducky,
    # which can be caught in the pond.  Finally, he thinks Cogs are spying
    # on him from nearby buildings while he showers.  The reward for solving his
    # problems is a measly +2 HP.
    5243 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3217, NA, (5244),
             TTLocalizer.QuestDialogDict[5243]),
    5244 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 2007, VeryHard, 'mm'), 3217, Same, NA, (5245),
             TTLocalizer.QuestDialogDict[5244]),
    5245 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3017, Hard, AnyFish), Same, Same, NA, (5246),
             TTLocalizer.QuestDialogDict[5245]),
    5246 : ( BR_TIER+1, Cont, (BuildingQuest, ToontownGlobals.TheBrrrgh, 5, Any, 1), Same, Same, 101, NA, # limited to this hood, so no need restricting the number of floors.
             TTLocalizer.QuestDialogDict[5246]),

    # Lounge Lassard was setting up for a gig and the Cogs came in a took
    # his microphone, electronic keyboard, toupee, and platform shoes.  Help
    # him recover these items and he'll reward you with +3 HP
    5251 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3134, NA, (5252),
             TTLocalizer.QuestDialogDict[5251]),
    5252 : ( BR_TIER+1, Start, (RecoverItemQuest, Anywhere, 1, 3019, VeryHard, Any), 3134, Same, NA, (5253, 5273, 5274, 5275),
             TTLocalizer.QuestDialogDict[5252]),
    5253 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3020, VeryHard, "cr"), Same, Same, NA, (5254, 5282, 5283, 5284),
             TTLocalizer.QuestDialogDict[5253]),
    5273 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3020, VeryHard, "m"), Same, Same, NA, (5254, 5282, 5283, 5284),
             TTLocalizer.QuestDialogDict[5273]),
    5274 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3020, VeryHard, "ls"), Same, Same, NA, (5254, 5282, 5283, 5284),
             TTLocalizer.QuestDialogDict[5274]),
    5275 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3020, Hard, "le"), Same, Same, NA, (5254, 5282, 5283, 5284),
             TTLocalizer.QuestDialogDict[5275]),
    5254 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3021, VeryHard, "mh"), Same, Same, 102, NA,
             TTLocalizer.QuestDialogDict[5254]),
    5282 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3021, VeryHard, "tbc"), Same, Same, 102, NA,
             TTLocalizer.QuestDialogDict[5282]),
    5283 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3021, VeryHard, "rb"), Same, Same, 102, NA,
             TTLocalizer.QuestDialogDict[5283]),
    5284 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 1, 3021, Hard, "bw"), Same, Same, 102, NA,
             TTLocalizer.QuestDialogDict[5284]),

    # Wynne Chill wants to trade.  If you wipe out cogs for her, she'll 
    # give you +1 HP. 
    5255 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3228, NA, (5256, 5276),
             TTLocalizer.QuestDialogDict[5255]),
    5256 : ( BR_TIER+1, Cont, (CogTrackQuest, Anywhere, 45, 'c'), 3228, Same, NA, (5257, 5277),
             TTLocalizer.QuestDialogDict[5256]),
    5276 : ( BR_TIER+1, Cont, (CogTrackQuest, Anywhere, 40, 'l'), 3228, Same, NA, (5257, 5277),
             TTLocalizer.QuestDialogDict[5276]),
    5257 : ( BR_TIER+1, Cont, (CogTrackQuest, Anywhere, 45, 's'), Same, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5257]),
    5277 : ( BR_TIER+1, Cont, (CogTrackQuest, Anywhere, 45, 'm'), Same, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5277]),

    # Go see Eddie the Yeti. If you kill some lawbots he'll give you +1 laff.
    5301 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3304, NA, (5302),
             TTLocalizer.QuestDialogDict[5301]),
    5302 : ( BR_TIER+1, Cont, (CogTrackQuest, Anywhere, 90, 'l'), Same, Same, 100, NA,
             TTLocalizer.QuestDialogDict[5302]),

    # Johnny Cashmere is missing several knitting supplies for making sweaters. Help him recover them all
    # and he will knit you a large bag (max gag = 50).
    5303 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3318, NA, (5304),
             TTLocalizer.QuestDialogDict[5303]),
    5304 : ( BR_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 1, 3024, VeryHard, 'l', 'track'), Same, Same, NA, (5305),
             TTLocalizer.QuestDialogDict[5304]),
    5305 : ( BR_TIER+1, Cont, (CogLevelQuest, Anywhere, 20, 7), Same, Same, NA, (5306),
             TTLocalizer.QuestDialogDict[5305]),
    5306 : ( BR_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.TheBrrrgh, 2, 3025, Hard, AnyFish), Same, Same, NA, (5307),
             TTLocalizer.QuestDialogDict[5306]),
    5307 : ( BR_TIER+1, Cont, (BuildingQuest, Anywhere, 5, Any, 4), Same, Same, 204, NA,
             TTLocalizer.QuestDialogDict[5307]),

    # March Harry is scared the Lawbots are going to sue him. He asks you to take out several
    # of them on his street. When this doesn't appease him he sends you too Hysterical Harry
    # to get an alibi for him. When you return with it, he rewards you with max quest = 4.
    5308 : ( BR_TIER+1, Start, (VisitQuest,), Any, 3312, NA, (5309),
             TTLocalizer.QuestDialogDict[5308]),
    5309 : ( BR_TIER+1, Start, (CogTrackQuest, ToontownGlobals.PolarPlace, 30, 'l'), Same, Same, NA, (5310),
             TTLocalizer.QuestDialogDict[5309]),
    5310 : ( BR_TIER+1, Cont, (VisitQuest,), Same, 3113, NA, (5311),
             TTLocalizer.QuestDialogDict[5310]),
    5311 : ( BR_TIER+1, Cont, (RecoverItemQuest, Anywhere, 2, 3026, Medium, 'le'), Same, Same, NA, (5312),
             TTLocalizer.QuestDialogDict[5311]),
    5312 : ( BR_TIER+1, Cont, (DeliverItemQuest, 3026), Same, 3312, 502, NA,
             TTLocalizer.QuestDialogDict[5312]),

    # Elder quests
    5290 : ( BR_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 12, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5291 : ( BR_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 12, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5292 : ( BR_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 12, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5293 : ( BR_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 12, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5294 : ( BR_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5295 : ( BR_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5296 : ( BR_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5297 : ( BR_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    5500 : ( BR_TIER+1, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 75, Any), Any, ToonHQ, NA, (5501), DefaultDialog),
    5501 : ( BR_TIER+1, Cont, (DeliverItemQuest, 1000), Any, 3008, 1000, NA, DefaultDialog),


    # It's time for the final challenge.  Return to Lil Oldman for him to
    # review your progress.  Before you can begin, you must eat, Oldman asks 
    # for lumpy cheese from Big Cheeses to put in your broth.  Then he discovers
    # his spoon is missing - maybe a Robber Baron took it?  Next, Oldman
    # sends you to catch a talking toad from the pond.  The toad whispers
    # something you can't catch, which prompts Oldman to send you out for
    # dessert, maybe popsicles?  It turns out the popsicles were carted off 
    # by a bunch of high level corporate Cogs, so you've got to track them 
    # down.  Finally, Oldman and his toad get their popsicles, and you get
    # your new track.
    903 : ( BR_TIER+2, Start, (VisitQuest,), Any, 3112, NA, (5234, 5278),
            TTLocalizer.QuestDialogDict[903]),
    5234 : ( BR_TIER+2, Start, (RecoverItemQuest, Anywhere, 6, 3012, Medium, 'tbc'), 3112, Same, NA, (5235, 5279),
             TTLocalizer.QuestDialogDict[5234]),
    5278 : ( BR_TIER+2, Start, (RecoverItemQuest, Anywhere, 6, 3022, Medium, 'mh'), 3112, Same, NA, (5235, 5279),
             TTLocalizer.QuestDialogDict[5278]),
    5235 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3013, Hard, 'rb'), Same, Same, NA, (5236),
             TTLocalizer.QuestDialogDict[5235]),
    5279 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3013, Medium, 'bw'), Same, Same, NA, (5236),  # lawbots are a little uncommon in BR
             TTLocalizer.QuestDialogDict[5279]),
    5236 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3014, VeryHard, AnyFish), Same, Same, NA, (5237),
             TTLocalizer.QuestDialogDict[5236]),
    
    5237 : ( BR_TIER+2, Cont, (VisitQuest,), Same, 3128, NA, (5238, 5280),
            TTLocalizer.QuestDialogDict[5237]),
    5238 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 10, 3015, VeryEasy, 'mh'), Same, Same, NA, (5239),
             TTLocalizer.QuestDialogDict[5238]),
    5280 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 10, 3015, VeryEasy, 'tbc'), Same, Same, NA, (5239),
             TTLocalizer.QuestDialogDict[5280]),
    5239 : ( BR_TIER+2, Cont, (DeliverItemQuest, 3015), Same, 3112, NA, (5240, 5281),
             TTLocalizer.QuestDialogDict[5239]),
    5240 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3016, Hard, 'bw'), Same, Same, NA, (5241),
             TTLocalizer.QuestDialogDict[5240]),
    5281 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3023, Hard, 'mh'), Same, Same, NA, (5241),
             TTLocalizer.QuestDialogDict[5281]),
    5241 : ( BR_TIER+2, Cont, (BuildingQuest, Anywhere, 20, Any, 4), Same, Same, NA, (5242),
             TTLocalizer.QuestDialogDict[5241]),
    5242 : ( BR_TIER+2, Cont, (RecoverItemQuest, Anywhere, 1, 3014, VeryHard, AnyFish), Same, Same, 900, NA,
             TTLocalizer.QuestDialogDict[5242]),

    # Optional quests to do while working on the bottleneck quest
    5320 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 36, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5321 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 38, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5322 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 40, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5323 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 42, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5324 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 44, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5325 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 46, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5326 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 48, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5327 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 53, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5328 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 52, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5329 : ( BR_TIER+2, Start, (CogQuest, Anywhere, 54, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5330 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 25, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5331 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 30, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5332 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 35, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5333 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 6,  7), Any, ToonHQ, Any, NA, DefaultDialog),
    5334 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 10, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5335 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 20, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    5336 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 2,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5337 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 8,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5338 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 10,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    5339 : ( BR_TIER+2, Start, (CogLevelQuest, Anywhere, 12,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    5340 : ( BR_TIER+2, Start, (CogQuest, ToontownGlobals.TheBrrrgh, 75, Any), Any, ToonHQ, NA, (5341), DefaultDialog),
    5341 : ( BR_TIER+2, Cont, (DeliverItemQuest, 1000), Any, 3008, 1000, NA, DefaultDialog),
    # Elder quests
    5360 : ( BR_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 20, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5361 : ( BR_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 20, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5362 : ( BR_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 20, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5363 : ( BR_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 20, Any, NEWBIE_HP), Any, ToonHQ, 606, NA, DefaultDialog),
    5364 : ( BR_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5365 : ( BR_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5366 : ( BR_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    5367 : ( BR_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 1, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    # Sellbot HQ quests
    5370 : ( BR_TIER+2, Start, (CogQuest, ToontownGlobals.SellbotHQ, 22, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5371 : ( BR_TIER+2, Start, (CogQuest, ToontownGlobals.SellbotHQ, 25, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    5372 : ( BR_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 16, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    5373 : ( BR_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotHQ, 12, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5374 : ( BR_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 14, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5375 : ( BR_TIER+2, Start, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 10, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5376 : ( BR_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5377 : ( BR_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5378 : ( BR_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5379 : ( BR_TIER+2, Start, (FactoryQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    5380 : ( BR_TIER+2, Start, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    5381 : ( BR_TIER+2, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 6, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    5382 : ( BR_TIER+2, Start, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 3, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    5383 : ( BR_TIER+2, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 1), Any, ToonHQ, Any, NA, DefaultDialog),
    5384 : ( BR_TIER+2, Start, (ForemanQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),


    # Dreamland
    # Cogs in DL are well-balanced.  Levels are 5..9.
    6101 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 60, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6102 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 65, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete to make room for the
    # DL & Cashbot Cog HQ Quests -patricia
    6103 : ( DL_TIER, OBSOLETE, (CogQuest, ToontownGlobals.DonaldsDreamland, 70, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6104 : ( DL_TIER, Start, (CogQuest, Anywhere, 80, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6105 : ( DL_TIER, Start, (CogQuest, Anywhere, 90, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6106 : ( DL_TIER, Start, (CogQuest, Anywhere, 100, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    6107 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'ym'),  Any, ToonHQ, Any, NA, DefaultDialog),
    6108 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    6109 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    6110 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),
    6111 : ( DL_TIER, Start, (CogQuest, Anywhere, 15, 'cr'), Any, ToonHQ, Any, NA, DefaultDialog),
    6112 : ( DL_TIER, Start, (CogQuest, Anywhere, 8,  'tbc'), Any, ToonHQ, Any, NA, DefaultDialog),

    6113 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    6114 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    6115 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    6116 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),
    6117 : ( DL_TIER, Start, (CogQuest, Anywhere, 15, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    6118 : ( DL_TIER, Start, (CogQuest, Anywhere, 8,  'mh'),  Any, ToonHQ, Any, NA, DefaultDialog),

    6119 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    6120 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    6121 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    6122 : ( DL_TIER, OBSOLETE, (CogQuest, Anywhere, 25, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),
    6123 : ( DL_TIER, Start, (CogQuest, Anywhere, 15, 'ls'), Any, ToonHQ, Any, NA, DefaultDialog),
    6124 : ( DL_TIER, Start, (CogQuest, Anywhere, 8,  'rb'), Any, ToonHQ, Any, NA, DefaultDialog),

    6125 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'dt'),  Any, ToonHQ, Any, NA, DefaultDialog),
    6126 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    6127 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    6128 : ( DL_TIER, Start, (CogQuest, Anywhere, 25, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),
    6129 : ( DL_TIER, Start, (CogQuest, Anywhere, 15, 'le'), Any, ToonHQ, Any, NA, DefaultDialog),
    6130 : ( DL_TIER, Start, (CogQuest, Anywhere, 8,  'bw'), Any, ToonHQ, Any, NA, DefaultDialog),

    6131 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 50, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6132 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 40, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    6133 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 35, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    6134 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 30, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    6135 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 25, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    6136 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 20, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    6137 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 15, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    6138 : ( DL_TIER, Start, (CogLevelQuest, Anywhere, 10,10), Any, ToonHQ, Any, NA, DefaultDialog),

    6139 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 50, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    6140 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 50, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    6141 : ( DL_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 50, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    6142 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 50, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    6143 : ( DL_TIER, OBSOLETE, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 55, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    6144 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 55, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    6145 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 55, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    6146 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 55, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    6147 : ( DL_TIER, OBSOLETE, (CogTrackQuest, Anywhere, 70, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    6148 : ( DL_TIER, Start, (CogTrackQuest, Anywhere, 70, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    6149 : ( DL_TIER, Start, (CogTrackQuest, Anywhere, 70, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    6150 : ( DL_TIER, Start, (CogTrackQuest, Anywhere, 70, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    6151 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 10, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    6152 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 6, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    6153 : ( DL_TIER, OBSOLETE, (BuildingQuest, Anywhere, 8, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6154 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 6, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6155 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 2, 'm', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6156 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 2, 's', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6157 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 2, 'c', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6158 : ( DL_TIER, Start, (BuildingQuest, Anywhere, 2, 'l', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # Elder quests
    6160 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 25, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    6161 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 25, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    6162 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 25, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    6163 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 25, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    6164 : ( DL_TIER, Start, (BuildingNewbieQuest, Anywhere, 2, Any, 1, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    6165 : ( DL_TIER, Start, (BuildingNewbieQuest, Anywhere, 2, Any, 1, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    6166 : ( DL_TIER, Start, (BuildingNewbieQuest, Anywhere, 2, Any, 1, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    6167 : ( DL_TIER, Start, (BuildingNewbieQuest, Anywhere, 2, Any, 1, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    # Sellbot HQ quests
    # HQ/Exterior: Cogs level 4-6
    # Factory: Cogs level 4-9, Skelecogs level 5-7, Skelecog Foreman level 11
    # OBSOLETE: These quests have been made obsolete 
    # by the Cashbot Cog HQ Quests -patricia
    6170 : ( DL_TIER, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 40, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6171 : ( DL_TIER, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 45, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6172 : ( DL_TIER, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 50, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6173 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 30, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6174 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6175 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6176 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 15, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6177 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 10, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    6178 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 10, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    6179 : ( DL_TIER, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    6180 : ( DL_TIER, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6181 : ( DL_TIER, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    6182 : ( DL_TIER, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6183 : ( DL_TIER, OBSOLETE, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 20), Any, ToonHQ, Any, NA, DefaultDialog),
    6184 : ( DL_TIER, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 10, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    6185 : ( DL_TIER, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 4, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    6186 : ( DL_TIER, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    6187 : ( DL_TIER, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    # Sellbot HQ Elder quests
    6190 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 15, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6191 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 15, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6192 : ( DL_TIER, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 15, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6193 : ( DL_TIER, Start, (SkelecogNewbieQuest, ToontownGlobals.SellbotHQ, 3, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6194 : ( DL_TIER, Start, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6195 : ( DL_TIER, Start, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    6196 : ( DL_TIER, Start, (ForemanNewbieQuest, ToontownGlobals.SellbotFactoryInt, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),

    # Added quests for new Dreamland Street & Cog HQ
    # Powers Erge, though forgetful, will give you an LP boost
    # if you'll defeat some Cogs for him
    6201 : ( DL_TIER, Start, (VisitQuest,), Any, 9111, NA, 6202, TTLocalizer.QuestDialogDict[6201]),
    6202 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 70, Any), 9111, Same, 100, NA, TTLocalizer.QuestDialogDict[6202]),

    # Susan Siesta wants to get rich but the Cogs are interfering.
    # Take out some Cog buildings and she'll give you the small backpack
    6206 : ( DL_TIER, Start, (VisitQuest,), Any, 9131, NA, 6207, TTLocalizer.QuestDialogDict[6206]),
    6207 : ( DL_TIER, Start, (BuildingQuest, ToontownGlobals.DonaldsDreamland, 8, Any, 4), 9131, Same, 205, NA, TTLocalizer.QuestDialogDict[6207]),

    # Lawful Linda is fixing her answering machine.
    # Help her & she'll give you a 2LP reward.
    6211 : ( DL_TIER, Start, (VisitQuest,), Any, 9217, NA, 6212, TTLocalizer.QuestDialogDict[6211]),
    6212 : ( DL_TIER, Start, (RecoverItemQuest, Anywhere, 3, 6002, Medium, 'bc'), 9217, Same, NA, 6213, TTLocalizer.QuestDialogDict[6212]),
    6213 : ( DL_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 6003, Hard, 'mb'), Same, Same, NA, 6214, TTLocalizer.QuestDialogDict[6213]),
    6214 : ( DL_TIER, Cont, (RecoverItemQuest, Anywhere, 1, 6004, VeryHard, 'pp'), Same, Same, 101, NA, TTLocalizer.QuestDialogDict[6214]),

    # Scratch Rocco's back and he'll scratch yours.
    # In fact, he'll give you a 3 LP bonus.
    6221 : ( DL_TIER, Start, (VisitQuest,), Any, 9119, NA, 6222, TTLocalizer.QuestDialogDict[6221]),
    6222 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 50, 'c'), 9119, Same, 102, NA, TTLocalizer.QuestDialogDict[6222]),
 
    # Nat & PJ will get you acquainted with the new 
    # HQ. And they'll give you your first suit part
    6231 : ( DL_TIER, Start, (VisitQuest,), Any, 9203, NA, 6232, TTLocalizer.QuestDialogDict[6231]),
    6232 : ( DL_TIER, Start, (VisitQuest,), 9203, 9103, NA, 6233, TTLocalizer.QuestDialogDict[6232]),
    6233 : ( DL_TIER, Cont, (CogTrackQuest, ToontownGlobals.CashbotHQ, 10, 'm'), Same, Same, NA, 6234, TTLocalizer.QuestDialogDict[6233]),
    6234 : ( DL_TIER, Cont, (VisitQuest,), Same, 9203, NA, 6235, TTLocalizer.QuestDialogDict[6234]),
    6235 : ( DL_TIER, Cont, (RecoverItemQuest, ToontownGlobals.CashbotHQ, 1, 6001, VeryHard, 'm', 'track'), Same, Same, 4000, NA, TTLocalizer.QuestDialogDict[6235]),

    # The Countess can't concentrate on counting her sheep with all 
    # these Cogs around. Clean up a bit and she'll reward you handsomely.
    # Reward: MaxMoneyReward 705 - 150 jellybeans
    6241 : ( DL_TIER, Start, (VisitQuest,), Any, 9219, NA, 6242, TTLocalizer.QuestDialogDict[6241]),
    6242 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 25, 'nc'), 9219, Same, 705, NA, TTLocalizer.QuestDialogDict[6242]),

    # Zari needs you to run some errands for her and maybe
    # wipe out some Cogs along the way. She'll make it worthwhile
    # though, she'll give you 4 LP if you run the gauntlet.
    6251 : ( DL_TIER, Start, (VisitQuest,), Any, 9221, NA, 6252, TTLocalizer.QuestDialogDict[6251]),
    6252 : ( DL_TIER, Start, (DeliverItemQuest, 6006), 9221, 9222, NA, 6253, TTLocalizer.QuestDialogDict[6252]),
    6253 : ( DL_TIER, Cont, (VisitQuest,), Same, 9221, NA, 6254, TTLocalizer.QuestDialogDict[6253]),
    6254 : ( DL_TIER, Cont, (DeliverItemQuest, 6007), Same, 9210, NA, 6255, TTLocalizer.QuestDialogDict[6254]),
    6255 : ( DL_TIER, Cont, (CogTrackQuest, Anywhere, 70, 'm'), Same, Same, NA, 6256, TTLocalizer.QuestDialogDict[6255]),
    6256 : ( DL_TIER, Cont, (VisitQuest,), Same, 9221, NA, 6257, TTLocalizer.QuestDialogDict[6256]),
    6257 : ( DL_TIER, Cont, (DeliverItemQuest, 6008), Same, 9205, NA, 6258, TTLocalizer.QuestDialogDict[6257]),
    6258 : ( DL_TIER, Cont, (CogQuest, Anywhere, 25, 'ms'), Same, Same, NA, 6259, TTLocalizer.QuestDialogDict[6258]),
    6259 : ( DL_TIER, Cont, (VisitQuest,), Same, 9221, NA, 6260, TTLocalizer.QuestDialogDict[6259]),
    6260 : ( DL_TIER, Cont, (DeliverItemQuest, 6009), Same, 9229, NA, 6261, TTLocalizer.QuestDialogDict[6260]),
    6261 : ( DL_TIER, Cont, (VisitQuest,), Same, 9221, NA, 6262, TTLocalizer.QuestDialogDict[6261]),
    6262 : ( DL_TIER, Cont, (DeliverItemQuest, 6010), Same,  9126, NA, 6263, TTLocalizer.QuestDialogDict[6262]),
    6263 : ( DL_TIER, Cont, (DeliverItemQuest, 6010), Same, 9112, NA, 6264, TTLocalizer.QuestDialogDict[6263]),
    6264 : ( DL_TIER, Cont, (DeliverItemQuest, 6011), Same, 9221, NA, 6265, TTLocalizer.QuestDialogDict[6264]),
    6265 : ( DL_TIER, Cont, (DeliverItemQuest, 6012), Same, 9115, NA, 6266, TTLocalizer.QuestDialogDict[6265]),
    6266 : ( DL_TIER, Cont, (VisitQuest,), Same, 9221, 103, NA, TTLocalizer.QuestDialogDict[6266]),

    # Drowsy Dave will give you teleport access to DL
    # if he can stay awake long enough for you to finish.
    6271 : ( DL_TIER, Start, (VisitQuest,), Any, 9208, NA, 6272, TTLocalizer.QuestDialogDict[6271]),
    6272 : ( DL_TIER, Start, (BuildingQuest, ToontownGlobals.DonaldsDreamland, 2, 'm', 5), 9208, Same, 305, NA, TTLocalizer.QuestDialogDict[6272]),

    # Teddy Blair has a piece of a cog suit to give you if you will
    # clear out some cogs. Of course, his ear plugs make it tough. 
    6281 : ( DL_TIER, Start, (VisitQuest,), Any, 9123, NA, 6282, TTLocalizer.QuestDialogDict[6281]),
    6282 : ( DL_TIER, Start, (CogTrackQuest, ToontownGlobals.DonaldsDreamland, 55, 'm'), 9123, Same, 4001, NA, TTLocalizer.QuestDialogDict[6282]),
    
    # William Teller needs help! Those darn Cashbots swiped his 3
    # reading lamps! Retrieve them and he'll give you
    # another cog Suit piece.
    6291 : ( DL_TIER, Start, (VisitQuest,), Any, 9226, NA, 6292, TTLocalizer.QuestDialogDict[6291]),
    6292 : ( DL_TIER, Start, (RecoverItemQuest, ToontownGlobals.DonaldsDreamland, 1, 6005, VeryHard, 'm', 'track'), 9226, Same, 4002, NA, TTLocalizer.QuestDialogDict[6292]),

    # Cashbot HQ quests
    # HQ/Exterior - 7, 8, 9
    # Mints 10-11, Supervisors - 12
    6301 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.CashbotHQ, 40, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6302 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.CashbotHQ, 45, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6303 : ( DL_TIER, Start, (CogQuest, ToontownGlobals.CashbotHQ, 50, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    6304 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 30, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    6305 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 20, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    6306 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 15, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    6307 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 12, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    # these quest don't work so well now that we have laff limits on HQ elevators
    6308 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.CashbotMintIntB, 10, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    6309 : ( DL_TIER, OBSOLETE, (CogLevelQuest, ToontownGlobals.CashbotMintIntC, 8, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    6310 : ( DL_TIER, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # these quest don't work so well now that we have laff limits on HQ elevators
    6311 : ( DL_TIER, OBSOLETE, (MintQuest, ToontownGlobals.CashbotMintIntB, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6312 : ( DL_TIER, OBSOLETE, (MintQuest, ToontownGlobals.CashbotMintIntC, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    6313 : ( DL_TIER, Start, (SkelecogQuest, ToontownGlobals.CashbotHQ, 20), Any, ToonHQ, Any, NA, DefaultDialog),
    6314 : ( DL_TIER, Start, (SkelecogLevelQuest, ToontownGlobals.CashbotHQ, 10, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    6315 : ( DL_TIER, Start, (SkelecogLevelQuest, ToontownGlobals.CashbotHQ, 6, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    6318 : ( DL_TIER, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # these quest don't work so well now that we have laff limits on HQ elevators
    6319 : ( DL_TIER, OBSOLETE, (SupervisorQuest, ToontownGlobals.CashbotMintIntB, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6320 : ( DL_TIER, OBSOLETE, (SupervisorQuest, ToontownGlobals.CashbotMintIntC, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    # replacements for obsolete quests above
    6321 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 10, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    6322 : ( DL_TIER, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 8, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    6323 : ( DL_TIER, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6324 : ( DL_TIER, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    6325 : ( DL_TIER, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    6326 : ( DL_TIER, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 3), Any, ToonHQ, Any, NA, DefaultDialog),


    # Post Dreamland 1
    7101 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 120, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7102 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 130, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    7103 : ( DL_TIER+1, OBSOLETE, (CogQuest, Anywhere, 140, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7104 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 160, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7105 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 180, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7106 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 200, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    7107 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 70, 'ym'),  Any, ToonHQ, Any, NA, DefaultDialog),
    7108 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 60, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    7109 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    7110 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),
    7111 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 30, 'cr'), Any, ToonHQ, Any, NA, DefaultDialog),
    7112 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 20, 'tbc'), Any, ToonHQ, Any, NA, DefaultDialog),

    7113 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 70, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    7114 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 60, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    7115 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    7116 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),
    7117 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 30, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    7118 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 20, 'mh'),  Any, ToonHQ, Any, NA, DefaultDialog),

    7119 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 70, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    7120 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 60, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    7121 : ( DL_TIER+1, OBSOLETE, (CogQuest, Anywhere, 50, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    7122 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),
    7123 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 30, 'ls'), Any, ToonHQ, Any, NA, DefaultDialog),
    7124 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 20, 'rb'), Any, ToonHQ, Any, NA, DefaultDialog),

    7125 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 70, 'dt'),  Any, ToonHQ, Any, NA, DefaultDialog),
    7126 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 60, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    7127 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    7128 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 50, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),
    7129 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 30, 'le'), Any, ToonHQ, Any, NA, DefaultDialog),
    7130 : ( DL_TIER+1, Start, (CogQuest, Anywhere, 20, 'bw'), Any, ToonHQ, Any, NA, DefaultDialog),

    7131 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 100, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    7132 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 80,  8), Any, ToonHQ, Any, NA, DefaultDialog),
    7133 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 60,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    7134 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 70,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    7135 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 40, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    7136 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 50, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    7137 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 20, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    7138 : ( DL_TIER+1, Start, (CogLevelQuest, Anywhere, 30, 11), Any, ToonHQ, Any, NA, DefaultDialog),

    7139 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 100, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    7140 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 100, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    7141 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 100, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    7142 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 100, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    7143 : ( DL_TIER+1, OBSOLETE, (CogTrackQuest, Anywhere, 120, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    7144 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 120, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    7145 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 120, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    7146 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 120, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    7147 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 140, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    7148 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 140, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    7149 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 140, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    7150 : ( DL_TIER+1, Start, (CogTrackQuest, Anywhere, 140, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    7151 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 20, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    7152 : ( DL_TIER+1, OBSOLETE, (BuildingQuest, Anywhere, 10, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    7153 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 10, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    7154 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 10, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # OBSOLETE: This quest has been made obsolete by the
    # DL & Cashbot Cog HQ Quests -patricia
    7155 : ( DL_TIER+1, OBSOLETE, (BuildingQuest, Anywhere, 5, 'm', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7156 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 5, 's', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7157 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 5, 'c', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7158 : ( DL_TIER+1, Start, (BuildingQuest, Anywhere, 5, 'l', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # Elder quests
    7160 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 35, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    7161 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 35, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    7162 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 35, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    7163 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 35, Any, NEWBIE_HP), Any, ToonHQ, 607, NA, DefaultDialog),
    7164 : ( DL_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 2, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    7165 : ( DL_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 2, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    7166 : ( DL_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 2, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    7167 : ( DL_TIER+1, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 2, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),

    # OBSOLETE: These quests have been made obsolete 
    # by the Cashbot Cog HQ Quests -patricia
    # Sellbot HQ quests
    7170 : ( DL_TIER+1, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 80, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7171 : ( DL_TIER+1, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 90, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7172 : ( DL_TIER+1, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 100, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7173 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 50, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    7174 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 35, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7175 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 35, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7176 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 30, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7177 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 20, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7178 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 20, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7179 : ( DL_TIER+1, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7180 : ( DL_TIER+1, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    7181 : ( DL_TIER+1, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7182 : ( DL_TIER+1, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    7183 : ( DL_TIER+1, OBSOLETE, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 40), Any, ToonHQ, Any, NA, DefaultDialog),
    7184 : ( DL_TIER+1, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 20, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    7185 : ( DL_TIER+1, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 8, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7186 : ( DL_TIER+1, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7187 : ( DL_TIER+1, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    # Sellbot HQ Elder quests
    7190 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 25, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7191 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 25, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7192 : ( DL_TIER+1, Start, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 25, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7193 : ( DL_TIER+1, Start, (SkelecogNewbieQuest, ToontownGlobals.SellbotHQ, 6, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7194 : ( DL_TIER+1, Start, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 2, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7195 : ( DL_TIER+1, Start, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 2, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    7196 : ( DL_TIER+1, Start, (ForemanNewbieQuest, ToontownGlobals.SellbotFactoryInt, 2, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),

    # New DL+1 Tier Quests for Suit parts
    # Get Nina Nightlight another bed for her stock 
    # and she'll give you a suit part
    7201 : ( DL_TIER+1, Start, (VisitQuest,), Any, 9124, NA, 7202, TTLocalizer.QuestDialogDict[7201]),
    7202 : ( DL_TIER+1, Start, (VisitQuest,), 9124, 9128, NA, 7203, TTLocalizer.QuestDialogDict[7202]),
    7203 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7001), Same, 9124, NA, 7204, TTLocalizer.QuestDialogDict[7203]),
    7204 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9128, NA, 7205, TTLocalizer.QuestDialogDict[7204]),
    7205 : ( DL_TIER+1, Cont, (CogQuest, ToontownGlobals.DonaldsDreamland, 140, Any), Same, Same, NA, 7206, TTLocalizer.QuestDialogDict[7205]),
    7206 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7002), Same, 9124, 4003, NA, TTLocalizer.QuestDialogDict[7206]),

    # Here's a quest to pick up a Cog Suit part. 
    # Help Honey Moon get a new bedspread from Ed
    7209 : ( DL_TIER+1, Start, (VisitQuest,), Any, 9232, NA, 7210, TTLocalizer.QuestDialogDict[7209]),
    7210 : ( DL_TIER+1, Start, (VisitQuest,), 9232, 9101, NA, 7211, TTLocalizer.QuestDialogDict[7210]),
    7211 : ( DL_TIER+1, Cont, (CogQuest, Anywhere, 30, 'nc'), Same, Same, NA, 7212, TTLocalizer.QuestDialogDict[7211]),
    7212 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7003), Same, 9232, NA, 7213, TTLocalizer.QuestDialogDict[7212]),
    7213 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9101, NA, 7214, TTLocalizer.QuestDialogDict[7213]),
    7214 : ( DL_TIER+1, Cont, (CogTrackQuest, Anywhere, 65, 'm'), Same, Same, NA, 7215, TTLocalizer.QuestDialogDict[7214]),
    7215 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7004), Same, 9232, 4004, NA, TTLocalizer.QuestDialogDict[7215]),

    # Dreamy Daphne had her pillows stolen but Tex 
    # can help her out. You'll get another Cog Suit part.
    7218 : ( DL_TIER+1, Start, (VisitQuest,), Any, 9109, NA, 7219, TTLocalizer.QuestDialogDict[7218]),
    7219 : ( DL_TIER+1, Start, (VisitQuest,), 9109, 9230, NA, 7220, TTLocalizer.QuestDialogDict[7219]),
    7220 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7005), Same, 9109, NA, 7221, TTLocalizer.QuestDialogDict[7220]),
    7221 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9230, NA, 7222, TTLocalizer.QuestDialogDict[7221]),
    7222 : ( DL_TIER+1, Cont, (BuildingQuest, Anywhere, 10, Any, 3), Same, Same, NA, 7223, TTLocalizer.QuestDialogDict[7222]),
    7223 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7006), Same, 9109, 4005, NA, TTLocalizer.QuestDialogDict[7223]),

    # Sandy Sandman lost her pajamas but Big Mama
    # and Cat can help her out. If you hang in there,
    # you'll get another Cog Suit part.
    7226 : ( DL_TIER+1, Start, (VisitQuest,), Any, 9224, NA, 7227, TTLocalizer.QuestDialogDict[7226]),
    7227 : ( DL_TIER+1, Start, (VisitQuest,), 9224, 9102, NA, 7228, TTLocalizer.QuestDialogDict[7227]),
    7228 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7007), Same, 9224, NA, 7229, TTLocalizer.QuestDialogDict[7228]),
    7229 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9102, NA, 7230, TTLocalizer.QuestDialogDict[7229]),
    7230 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7008), Same, 9224, NA, 7231, TTLocalizer.QuestDialogDict[7230]),
    7231 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9102, NA, 7232, TTLocalizer.QuestDialogDict[7231]),
    7232 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9216, NA, 7233, TTLocalizer.QuestDialogDict[7232]),
    7233 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7009), Same, 9224, NA, 7234, TTLocalizer.QuestDialogDict[7233]),
    7234 : ( DL_TIER+1, Cont, (VisitQuest,), Same, 9216, NA, 7235, TTLocalizer.QuestDialogDict[7234]),
    7235 : ( DL_TIER+1, Cont, (BuildingQuest, Anywhere, 5, 'm', 5), Same, Same, NA, 7236, TTLocalizer.QuestDialogDict[7235]),
    7236 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7010), Same, 9224, 4006, NA, TTLocalizer.QuestDialogDict[7236]),

    # Smudgy Mascara needs Wrinkle Cream but
    # 39's missing ingredients. Help them out
    # and get a piece of Cog suit
    7239 : ( DL_TIER+1, Start, (VisitQuest,), Any, 9114, NA, 7240, TTLocalizer.QuestDialogDict[7239]),
    7240 : ( DL_TIER+1, Start, (VisitQuest,), 9114, 9215, NA, 7241, TTLocalizer.QuestDialogDict[7240]),
    7241 : ( DL_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.DonaldsDreamland, 1, 7011, Hard, AnyFish), Same, Same, NA, 7242, TTLocalizer.QuestDialogDict[7241]),
    7242 : ( DL_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.DonaldsDreamland, 1, 7012, VeryHard, AnyFish), Same, Same, NA, 7243, TTLocalizer.QuestDialogDict[7242]),
    7243 : ( DL_TIER+1, Cont, (RecoverItemQuest, ToontownGlobals.CashbotHQ, 1, 7013, Hard, 'ls'), Same, Same, NA, 7244, TTLocalizer.QuestDialogDict[7243]),
    7244 : ( DL_TIER+1, Cont, (DeliverItemQuest, 7014), Same, 9114, 4007, NA, TTLocalizer.QuestDialogDict[7244]),

    # Cashbot HQ quests
    7250 : ( DL_TIER+1, Start, (CogQuest, ToontownGlobals.CashbotHQ, 80, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7251 : ( DL_TIER+1, Start, (CogQuest, ToontownGlobals.CashbotHQ, 90, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7252 : ( DL_TIER+1, Start, (CogQuest, ToontownGlobals.CashbotHQ, 100, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    7253 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 50, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    7254 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 35, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    7255 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 35, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    7256 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 30, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    7257 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntB, 25, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    # this quest doesn't work so well now that we have laff limits on HQ elevators
    7258 : ( DL_TIER+1, OBSOLETE, (CogLevelQuest, ToontownGlobals.CashbotMintIntC, 20, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    7259 : ( DL_TIER+1, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    7260 : ( DL_TIER+1, Start, (MintQuest, ToontownGlobals.CashbotMintIntB, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    # this quest doesn't work so well now that we have laff limits on HQ elevators
    7261 : ( DL_TIER+1, OBSOLETE, (MintQuest, ToontownGlobals.CashbotMintIntC, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7262 : ( DL_TIER+1, Start, (SkelecogQuest, ToontownGlobals.CashbotHQ, 30), Any, ToonHQ, Any, NA, DefaultDialog),
    7263 : ( DL_TIER+1, Start, (SkelecogLevelQuest, ToontownGlobals.CashbotHQ, 20, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    7264 : ( DL_TIER+1, Start, (SkelecogLevelQuest, ToontownGlobals.CashbotHQ, 10, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    7265 : ( DL_TIER+1, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    7266 : ( DL_TIER+1, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntB, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    # this quest doesn't work so well now that we have laff limits on HQ elevators
    7267 : ( DL_TIER+1, OBSOLETE, (SupervisorQuest, ToontownGlobals.CashbotMintIntC, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    # replacements for obsolete quests above
    7268 : ( DL_TIER+1, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntB, 20, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    7269 : ( DL_TIER+1, Start, (MintQuest, ToontownGlobals.CashbotMintIntB, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    7270 : ( DL_TIER+1, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntB, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    
    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    7500 : ( DL_TIER+1, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 100, Any), Any, ToonHQ, NA, (7501), DefaultDialog),
    7501 : ( DL_TIER+1, Cont, (DeliverItemQuest, 1000), Any, 9010, 1000, NA, DefaultDialog),


    # Post Dreamland 2
    8101 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 240, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8102 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 260, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8103 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 280, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8104 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 320, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8105 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 360, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8106 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 400, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    8107 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 140, 'ym'),  Any, ToonHQ, Any, NA, DefaultDialog),
    8108 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 120, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    8109 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    8110 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),
    8111 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 60, 'cr'), Any, ToonHQ, Any, NA, DefaultDialog),
    8112 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 40,  'tbc'), Any, ToonHQ, Any, NA, DefaultDialog),

    8113 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 140, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    8114 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 120, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    8115 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    8116 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),
    8117 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 60, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    8118 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 40,  'mh'),  Any, ToonHQ, Any, NA, DefaultDialog),

    8119 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 140, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    8120 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 120, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    8121 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    8122 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),
    8123 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 60, 'ls'), Any, ToonHQ, Any, NA, DefaultDialog),
    8124 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 40,  'rb'), Any, ToonHQ, Any, NA, DefaultDialog),

    8125 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 140, 'dt'),  Any, ToonHQ, Any, NA, DefaultDialog),
    8126 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 120, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    8127 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    8128 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 100, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),
    8129 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 60, 'le'), Any, ToonHQ, Any, NA, DefaultDialog),
    8130 : ( DL_TIER+2, Start, (CogQuest, Anywhere, 40,  'bw'), Any, ToonHQ, Any, NA, DefaultDialog),

    8131 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 160,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    8132 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 200,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    8133 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 120, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    8134 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 140, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    8135 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 80, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    8136 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 100, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    8137 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 40, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8138 : ( DL_TIER+2, Start, (CogLevelQuest, Anywhere, 60, 12), Any, ToonHQ, Any, NA, DefaultDialog),

    8139 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 200, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    8140 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 200, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    8141 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 200, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    8142 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 200, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    8143 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 250, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    8144 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 250, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    8145 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 250, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    8146 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 250, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    8147 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 300, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    8148 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 300, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    8149 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 300, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    8150 : ( DL_TIER+2, Start, (CogTrackQuest, Anywhere, 300, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    8151 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 40, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    8152 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 20, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    8153 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 20, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    8154 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 20, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8155 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 10, 'm', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8156 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 10, 's', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8157 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 10, 'c', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8158 : ( DL_TIER+2, Start, (BuildingQuest, Anywhere, 10, 'l', 5), Any, ToonHQ, Any, NA, DefaultDialog),

    # Elder quests
    8160 : ( DL_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 40, Any, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    8161 : ( DL_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 40, Any, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    8162 : ( DL_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 40, Any, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    8163 : ( DL_TIER+2, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 40, Any, NEWBIE_HP), Any, ToonHQ, 608, NA, DefaultDialog),
    8164 : ( DL_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    8165 : ( DL_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    8166 : ( DL_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    8167 : ( DL_TIER+2, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),

    # OBSOLETE: These quests have been made obsolete 
    # by the Cashbot Cog HQ Quests -patricia
    # Sellbot HQ quests
    8170 : ( DL_TIER+2, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 160, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8171 : ( DL_TIER+2, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 180, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8172 : ( DL_TIER+2, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 200, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8173 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 100, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    8174 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 70, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8175 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 70, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8176 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 60, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8177 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 40, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    8178 : ( DL_TIER+2, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 40, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    8179 : ( DL_TIER+2, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8180 : ( DL_TIER+2, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 16), Any, ToonHQ, Any, NA, DefaultDialog),
    8181 : ( DL_TIER+2, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8182 : ( DL_TIER+2, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 16), Any, ToonHQ, Any, NA, DefaultDialog),
    8183 : ( DL_TIER+2, OBSOLETE, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 80), Any, ToonHQ, Any, NA, DefaultDialog),
    8184 : ( DL_TIER+2, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 40, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    8185 : ( DL_TIER+2, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 16, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    8186 : ( DL_TIER+2, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8187 : ( DL_TIER+2, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 16), Any, ToonHQ, Any, NA, DefaultDialog),
    8188 : ( DL_TIER+2, OBSOLETE, (VPQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    8189 : ( DL_TIER+2, OBSOLETE, (RescueQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    # Sellbot HQ Elder quests
    8190 : ( DL_TIER+2, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 30, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8191 : ( DL_TIER+2, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 30, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8192 : ( DL_TIER+2, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 30, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8193 : ( DL_TIER+2, OBSOLETE, (SkelecogNewbieQuest, ToontownGlobals.SellbotHQ, 8, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8194 : ( DL_TIER+2, OBSOLETE, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 3, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8195 : ( DL_TIER+2, OBSOLETE, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 3, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8196 : ( DL_TIER+2, OBSOLETE, (ForemanNewbieQuest, ToontownGlobals.SellbotFactoryInt, 3, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8197 : ( DL_TIER+2, OBSOLETE, (VPNewbieQuest, ToontownGlobals.SellbotHQ, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),
    8198 : ( DL_TIER+2, OBSOLETE, (RescueNewbieQuest, ToontownGlobals.SellbotHQ, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 610, NA, DefaultDialog),

    # Cashbot HQ quests
    8201 : ( DL_TIER+2, Start, (CogQuest, ToontownGlobals.CashbotHQ, 160, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8202 : ( DL_TIER+2, Start, (CogQuest, ToontownGlobals.CashbotHQ, 180, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8203 : ( DL_TIER+2, Start, (CogQuest, ToontownGlobals.CashbotHQ, 200, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    8204 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 100, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    8205 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 90, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    8206 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 80, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    8207 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 60, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    8208 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntB, 50, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    8209 : ( DL_TIER+2, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntC, 40, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    8210 : ( DL_TIER+2, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 16), Any, ToonHQ, Any, NA, DefaultDialog),
    8211 : ( DL_TIER+2, Start, (MintQuest, ToontownGlobals.CashbotMintIntB, 14), Any, ToonHQ, Any, NA, DefaultDialog),
    8212 : ( DL_TIER+2, Start, (MintQuest, ToontownGlobals.CashbotMintIntC, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8213 : ( DL_TIER+2, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntA, 80), Any, ToonHQ, Any, NA, DefaultDialog),
    8214 : ( DL_TIER+2, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntB, 60), Any, ToonHQ, Any, NA, DefaultDialog),
    8215 : ( DL_TIER+2, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntC, 40), Any, ToonHQ, Any, NA, DefaultDialog),
    8216 : ( DL_TIER+2, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 16), Any, ToonHQ, Any, NA, DefaultDialog),
    8217 : ( DL_TIER+2, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntB, 14), Any, ToonHQ, Any, NA, DefaultDialog),
    8218 : ( DL_TIER+2, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntC, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    8219 : ( DL_TIER+2, Start, (CFOQuest, ToontownGlobals.CashbotHQ, 2), Any, ToonHQ, 621, NA, DefaultDialog),

    # Post Dreamland 3
    9101 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 500, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9102 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 600, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9103 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 700, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9104 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 800, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9105 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 900, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9106 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 1000, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    9107 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 300, 'ym'),  Any, ToonHQ, Any, NA, DefaultDialog),
    9108 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 250, 'mm'), Any, ToonHQ, Any, NA, DefaultDialog),
    9109 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'ds'), Any, ToonHQ, Any, NA, DefaultDialog),
    9110 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'hh'), Any, ToonHQ, Any, NA, DefaultDialog),
    9111 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 120, 'cr'), Any, ToonHQ, Any, NA, DefaultDialog),
    9112 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 80,  'tbc'), Any, ToonHQ, Any, NA, DefaultDialog),

    9113 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 280, 'nd'), Any, ToonHQ, Any, NA, DefaultDialog),
    9114 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 240, 'gh'), Any, ToonHQ, Any, NA, DefaultDialog),
    9115 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'ms'), Any, ToonHQ, Any, NA, DefaultDialog),
    9116 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'tf'), Any, ToonHQ, Any, NA, DefaultDialog),
    9117 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 120, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    9118 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 80,  'mh'),  Any, ToonHQ, Any, NA, DefaultDialog),

    9119 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 280, 'tw'), Any, ToonHQ, Any, NA, DefaultDialog),
    9120 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 240, 'bc'), Any, ToonHQ, Any, NA, DefaultDialog),
    9121 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'nc'), Any, ToonHQ, Any, NA, DefaultDialog),
    9122 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'mb'), Any, ToonHQ, Any, NA, DefaultDialog),
    9123 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 120, 'ls'), Any, ToonHQ, Any, NA, DefaultDialog),
    9124 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 80,  'rb'), Any, ToonHQ, Any, NA, DefaultDialog),

    9125 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 280, 'dt'),  Any, ToonHQ, Any, NA, DefaultDialog),
    9126 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 240, 'ac'), Any, ToonHQ, Any, NA, DefaultDialog),
    9127 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'bs'), Any, ToonHQ, Any, NA, DefaultDialog),
    9128 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 200, 'sd'), Any, ToonHQ, Any, NA, DefaultDialog),
    9129 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 120, 'le'), Any, ToonHQ, Any, NA, DefaultDialog),
    9130 : ( DL_TIER+3, Start, (CogQuest, Anywhere, 80,  'bw'), Any, ToonHQ, Any, NA, DefaultDialog),

    9131 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 320,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    9132 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 400,  9), Any, ToonHQ, Any, NA, DefaultDialog),
    9133 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 240, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    9134 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 280, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    9135 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 160, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    9136 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 200, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    9137 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 80, 12), Any, ToonHQ, Any, NA, DefaultDialog),
    9138 : ( DL_TIER+3, Start, (CogLevelQuest, Anywhere, 120, 12), Any, ToonHQ, Any, NA, DefaultDialog),

    9139 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 400, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    9140 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 400, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    9141 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 400, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    9142 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 400, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    9143 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 500, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    9144 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 500, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    9145 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 500, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    9146 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 500, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    9147 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 600, 'm'), Any, ToonHQ, Any, NA, DefaultDialog),
    9148 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 600, 's'), Any, ToonHQ, Any, NA, DefaultDialog),
    9149 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 600, 'c'), Any, ToonHQ, Any, NA, DefaultDialog),
    9150 : ( DL_TIER+3, Start, (CogTrackQuest, Anywhere, 600, 'l'), Any, ToonHQ, Any, NA, DefaultDialog),

    9151 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 400, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    9152 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 200, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    9153 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 200, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    9154 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 200, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # nerfed these to make it easier to find the buildings - grw
    #9155 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, 'm', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    #9156 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, 's', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    #9157 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, 'c', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    #9158 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, 'l', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9155 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9156 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9157 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9158 : ( DL_TIER+3, Start, (BuildingQuest, Anywhere, 100, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    # Elder quests
    9160 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 45, Any, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9161 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 45, Any, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9162 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 45, Any, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9163 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 45, Any, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9164 : ( DL_TIER+3, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9165 : ( DL_TIER+3, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9166 : ( DL_TIER+3, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    9167 : ( DL_TIER+3, Start, (BuildingNewbieQuest, Anywhere, 1, Any, 3, NEWBIE_HP), Any, ToonHQ, 609, NA, DefaultDialog),
    # OBSOLETE: These quests have been made obsolete 
    # by the Cashbot Cog HQ Quests -patricia
    # Sellbot HQ quests
    9170 : ( DL_TIER+3, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 350, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9171 : ( DL_TIER+3, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 400, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9172 : ( DL_TIER+3, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 500, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9173 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 200, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    9174 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 150, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9175 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotHQ, 150, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9176 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 150, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9177 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 100, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    9178 : ( DL_TIER+3, OBSOLETE, (CogLevelQuest, ToontownGlobals.SellbotFactoryInt, 100, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    9179 : ( DL_TIER+3, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 25), Any, ToonHQ, Any, NA, DefaultDialog),
    9180 : ( DL_TIER+3, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 35), Any, ToonHQ, Any, NA, DefaultDialog),
    9181 : ( DL_TIER+3, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 25), Any, ToonHQ, Any, NA, DefaultDialog),
    9182 : ( DL_TIER+3, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 35), Any, ToonHQ, Any, NA, DefaultDialog),
    9183 : ( DL_TIER+3, OBSOLETE, (SkelecogQuest, ToontownGlobals.SellbotFactoryInt, 150), Any, ToonHQ, Any, NA, DefaultDialog),
    9184 : ( DL_TIER+3, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 80, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    9185 : ( DL_TIER+3, OBSOLETE, (SkelecogLevelQuest, ToontownGlobals.SellbotHQ, 32, 6), Any, ToonHQ, Any, NA, DefaultDialog),
    9186 : ( DL_TIER+3, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 25), Any, ToonHQ, Any, NA, DefaultDialog),
    9187 : ( DL_TIER+3, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 35), Any, ToonHQ, Any, NA, DefaultDialog),
    9188 : ( DL_TIER+3, OBSOLETE, (VPQuest, ToontownGlobals.SellbotHQ, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    9189 : ( DL_TIER+3, OBSOLETE, (RescueQuest, ToontownGlobals.SellbotHQ, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    # Sellbot HQ Elder quests
    9190 : ( DL_TIER+3, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 35, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9191 : ( DL_TIER+3, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 35, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9192 : ( DL_TIER+3, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 35, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9193 : ( DL_TIER+3, OBSOLETE, (SkelecogNewbieQuest, ToontownGlobals.SellbotHQ, 10, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9194 : ( DL_TIER+3, OBSOLETE, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 4, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9195 : ( DL_TIER+3, OBSOLETE, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 4, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9196 : ( DL_TIER+3, OBSOLETE, (ForemanNewbieQuest, ToontownGlobals.SellbotFactoryInt, 4, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9197 : ( DL_TIER+3, OBSOLETE, (VPNewbieQuest, ToontownGlobals.SellbotHQ, 2, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9198 : ( DL_TIER+3, OBSOLETE, (RescueNewbieQuest, ToontownGlobals.SellbotHQ, 2, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    # Cashbot HQ quests
    9201 : ( DL_TIER+3, Start, (CogQuest, ToontownGlobals.CashbotHQ, 350, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9202 : ( DL_TIER+3, Start, (CogQuest, ToontownGlobals.CashbotHQ, 400, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9203 : ( DL_TIER+3, Start, (CogQuest, ToontownGlobals.CashbotHQ, 450, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    9204 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 200, 7), Any, ToonHQ, Any, NA, DefaultDialog),
    9205 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 150, 8), Any, ToonHQ, Any, NA, DefaultDialog),
    9206 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotHQ, 100, 9), Any, ToonHQ, Any, NA, DefaultDialog),
    9207 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntA, 200, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    9208 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntB, 150, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    9209 : ( DL_TIER+3, Start, (CogLevelQuest, ToontownGlobals.CashbotMintIntC, 100, 11), Any, ToonHQ, Any, NA, DefaultDialog),
    9210 : ( DL_TIER+3, Start, (MintQuest, ToontownGlobals.CashbotMintIntA, 35), Any, ToonHQ, Any, NA, DefaultDialog),
    9211 : ( DL_TIER+3, Start, (MintQuest, ToontownGlobals.CashbotMintIntB, 30), Any, ToonHQ, Any, NA, DefaultDialog),
    9212 : ( DL_TIER+3, Start, (MintQuest, ToontownGlobals.CashbotMintIntC, 25), Any, ToonHQ, Any, NA, DefaultDialog),
    9213 : ( DL_TIER+3, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntA, 150), Any, ToonHQ, Any, NA, DefaultDialog),
    9214 : ( DL_TIER+3, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntB, 100), Any, ToonHQ, Any, NA, DefaultDialog),
    9215 : ( DL_TIER+3, Start, (SkelecogQuest, ToontownGlobals.CashbotMintIntC, 50), Any, ToonHQ, Any, NA, DefaultDialog),
    9216 : ( DL_TIER+3, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntA, 35), Any, ToonHQ, Any, NA, DefaultDialog),
    9217 : ( DL_TIER+3, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntB, 30), Any, ToonHQ, Any, NA, DefaultDialog),
    9218 : ( DL_TIER+3, Start, (SupervisorQuest, ToontownGlobals.CashbotMintIntC, 25), Any, ToonHQ, Any, NA, DefaultDialog),
    9219 : ( DL_TIER+3, Start, (CFOQuest, ToontownGlobals.CashbotHQ, 3), Any, ToonHQ, 622, NA, DefaultDialog),
    # Cashbot HQ Elder quests
    9220 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.CashbotMintIntA, 35, Any, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9221 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.CashbotMintIntB, 30, Any, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9222 : ( DL_TIER+3, Start, (CogNewbieQuest, ToontownGlobals.CashbotMintIntC, 25, Any, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9223 : ( DL_TIER+3, Start, (SkelecogNewbieQuest, ToontownGlobals.CashbotHQ, 10, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9224 : ( DL_TIER+3, Start, (MintNewbieQuest, ToontownGlobals.CashbotMintIntA, 6, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9225 : ( DL_TIER+3, Start, (MintNewbieQuest, ToontownGlobals.CashbotMintIntB, 4, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9226 : ( DL_TIER+3, Start, (MintNewbieQuest, ToontownGlobals.CashbotMintIntC, 2, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9227 : ( DL_TIER+3, Start, (SupervisorNewbieQuest, ToontownGlobals.CashbotMintIntA, 6, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9228 : ( DL_TIER+3, Start, (SupervisorNewbieQuest, ToontownGlobals.CashbotMintIntB, 4, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    9229 : ( DL_TIER+3, Start, (SupervisorNewbieQuest, ToontownGlobals.CashbotMintIntC, 2, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    # Commented out as there will be far too few players who will fall into this category. Perhaps another time....
    #9230 : ( DL_TIER+3, Start, (CFONewbieQuest, ToontownGlobals.CashbotHQ, 2, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 620, NA, DefaultDialog),

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    9500 : ( DL_TIER+3, Start, (CogQuest, ToontownGlobals.DonaldsDreamland, 1000, Any), Any, ToonHQ, NA, (9501), DefaultDialog),
    9501 : ( DL_TIER+3, Cont, (DeliverItemQuest, 1000), Any, 2004, 1000, NA, DefaultDialog),


    # Elder quests 
    10001 : ( ELDER_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 50, Any, NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),
    10002 : ( ELDER_TIER, Start, (BuildingNewbieQuest, Anywhere, 4, Any, 1, NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),

    # These have issues
    #10003 : ( ELDER_TIER, Start, (FriendNewbieQuest, 2, 20), Any, ToonHQ, Any, NA, DefaultDialog),
    #10004 : ( ELDER_TIER, Start, (MinigameNewbieQuest, 2, 20), Any, ToonHQ, Any, NA, DefaultDialog),

    # Defeat cogs - bread and butter stuff
    10100 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 80, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    10101 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 100, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    10102 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 120, Any), Any, ToonHQ, Any, NA, DefaultDialog),

    # Defeat lots of Cogs for lots of jellybeans
    10103 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 200, Any), Any, ToonHQ, 613, NA, DefaultDialog),
    10104 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 250, Any), Any, ToonHQ, 615, NA, DefaultDialog),
    10105 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 300, Any), Any, ToonHQ, 616, NA, DefaultDialog),
    10106 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 400, Any), Any, ToonHQ, 618, NA, DefaultDialog),

    # Defeat buildings for random rewards
    10110 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 40, Any, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    10111 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 30, Any, 3), Any, ToonHQ, Any, NA, DefaultDialog),
    10112 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 25, Any, 4), Any, ToonHQ, Any, NA, DefaultDialog),
    10113 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 20, Any, 5), Any, ToonHQ, Any, NA, DefaultDialog),
    10114 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 20, 'm', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    10115 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 20, 's', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    10116 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 20, 'c', 5), Any, ToonHQ, Any, NA, DefaultDialog),
    10117 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 20, 'l', 5), Any, ToonHQ, Any, NA, DefaultDialog),

    # Defeat buildings for lots of beans
    10118 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 50, Any, 1), Any, ToonHQ, 620, NA, DefaultDialog),

    # OBSOLETE: These quests have been made obsolete 
    # by the Cashbot Cog HQ Quests -patricia
    # Sellbot HQ quests
    10120 : ( ELDER_TIER, OBSOLETE, (CogQuest, ToontownGlobals.SellbotHQ, 60, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    10121 : ( ELDER_TIER, OBSOLETE, (FactoryQuest, ToontownGlobals.SellbotHQ, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    10122 : ( ELDER_TIER, OBSOLETE, (ForemanQuest, ToontownGlobals.SellbotHQ, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    10123 : ( ELDER_TIER, OBSOLETE, (VPQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    10124 : ( ELDER_TIER, OBSOLETE, (RescueQuest, ToontownGlobals.SellbotHQ, 2), Any, ToonHQ, Any, NA, DefaultDialog),
    # Sellbot HQ Elder/noob quests
    10130 : ( ELDER_TIER, OBSOLETE, (CogNewbieQuest, ToontownGlobals.SellbotHQ, 40, Any, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),
    10131 : ( ELDER_TIER, OBSOLETE, (FactoryNewbieQuest, ToontownGlobals.SellbotHQ, 3, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),
    10132 : ( ELDER_TIER, OBSOLETE, (VPNewbieQuest, ToontownGlobals.SellbotHQ, 1, SELLBOT_HQ_NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),

    # Cashbot HQ quests
    10140 : ( ELDER_TIER, Start, (CogQuest, ToontownGlobals.CashbotHQ, 60, Any), Any, ToonHQ, Any, NA, DefaultDialog),
    10141 : ( ELDER_TIER, Start, (MintQuest, ToontownGlobals.CashbotHQ, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    10142 : ( ELDER_TIER, Start, (SupervisorQuest, ToontownGlobals.CashbotHQ, 10), Any, ToonHQ, Any, NA, DefaultDialog),
    10143 : ( ELDER_TIER, Start, (CFOQuest, ToontownGlobals.CashbotHQ, 2), Any, ToonHQ, 623, NA, DefaultDialog),
    # Cashbot HQ Elder/noob quests
    10145 : ( ELDER_TIER, Start, (CogNewbieQuest, ToontownGlobals.CashbotHQ, 40, Any, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),
    10146 : ( ELDER_TIER, Start, (MintNewbieQuest, ToontownGlobals.CashbotHQ, 3, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, Any, NA, DefaultDialog),
    10147 : ( ELDER_TIER, Start, (SupervisorNewbieQuest, ToontownGlobals.CashbotHQ, 3, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 611, NA, DefaultDialog),
    # Commented out as there will be far too few players who will fall into this category. Perhaps another time....
    #10148 : ( ELDER_TIER, Start, (CFONewbieQuest, ToontownGlobals.CashbotHQ, 1, CASHBOT_HQ_NEWBIE_HP), Any, ToonHQ, 622, NA, DefaultDialog),

    # Clothing quest: defeat some cogs then deliver clothing ticket to NPCTailor
    10200 : ( ELDER_TIER, Start, (CogQuest, Anywhere, 100, Any), Any, ToonHQ, NA, (10201), DefaultDialog),
    10201 : ( ELDER_TIER, Cont, (DeliverItemQuest, 1000), Any, ToonTailor, 1000, NA, DefaultDialog),

    # Clothing quest: defeat some buildings then deliver clothing ticket to NPCTailor
    10202 : ( ELDER_TIER, Start, (BuildingQuest, Anywhere, 25, Any, 1), Any, ToonHQ, NA, (10203), DefaultDialog),
    10203 : ( ELDER_TIER, Cont, (DeliverItemQuest, 1000), Any, ToonTailor, 1000, NA, DefaultDialog),

    # Clothing quest: help a newbie then deliver clothing ticket to NPCTailor
    10204 : ( ELDER_TIER, Start, (CogNewbieQuest, ToontownGlobals.ToontownCentral, 60, Any, NEWBIE_HP), Any, ToonHQ, NA, (10205), DefaultDialog),
    10205 : ( ELDER_TIER, Cont, (DeliverItemQuest, 1000), Any, ToonTailor, 1000, NA, DefaultDialog),
    
    # Clothing quest: help a newbie then deliver clothing ticket to NPCTailor
    10206 : ( ELDER_TIER, Start, (BuildingNewbieQuest, Anywhere, 4, Any, 1, NEWBIE_HP), Any, ToonHQ, NA, (10207), DefaultDialog),
    10207 : ( ELDER_TIER, Cont, (DeliverItemQuest, 1000), Any, ToonTailor, 1000, NA, DefaultDialog),

    # Lawbot HQ suit part quests

    # Professor Flake needs you run all over Toontown to get weather readings to support his Global Climate Change theory.
    11000 : ( LAWBOT_HQ_TIER, Start, (VisitQuest,), Any, 3310, NA, (11001),
              TTLocalizer.QuestDialogDict[11000]),
    11001 : ( LAWBOT_HQ_TIER, Start, (RecoverItemQuest, ToontownGlobals.SillyStreet, 1, 3027, Hard, Any), Same, Same, 4100, NA,
              TTLocalizer.QuestDialogDict[11001]),
    11002 : ( LAWBOT_HQ_TIER+1, Start, (VisitQuest,), Any, 3310, NA, (11003),
              TTLocalizer.QuestDialogDict[11002]),
    11003 : ( LAWBOT_HQ_TIER+1, Start, (RecoverItemQuest, ToontownGlobals.LoopyLane, 1, 3027, Hard, Any), Same, Same, 4101, NA,
              TTLocalizer.QuestDialogDict[11003]),
    11004 : ( LAWBOT_HQ_TIER+2, Start, (VisitQuest,), Any, 3310, NA, (11005),
              TTLocalizer.QuestDialogDict[11004]),
    11005 : ( LAWBOT_HQ_TIER+2, Start, (RecoverItemQuest, ToontownGlobals.PunchlinePlace, 1, 3027, Hard, Any), Same, Same, 4102, NA,
              TTLocalizer.QuestDialogDict[11005]),
    11006 : ( LAWBOT_HQ_TIER+3, Start, (VisitQuest,), Any, 3310, NA, (11007),
              TTLocalizer.QuestDialogDict[11006]),
    11007 : ( LAWBOT_HQ_TIER+3, Start, (RecoverItemQuest, ToontownGlobals.BarnacleBoulevard, 1, 3027, Hard, Any), Same, Same, 4103, NA,
              TTLocalizer.QuestDialogDict[11007]),
    11008 : ( LAWBOT_HQ_TIER+4, Start, (VisitQuest,), Any, 3310, NA, (11009),
              TTLocalizer.QuestDialogDict[11008]),
    11009 : ( LAWBOT_HQ_TIER+4, Start, (RecoverItemQuest, ToontownGlobals.SeaweedStreet, 1, 3027, Hard, Any), Same, Same, 4104, NA,
              TTLocalizer.QuestDialogDict[11009]),
    11010 : ( LAWBOT_HQ_TIER+5, Start, (VisitQuest,), Any, 3310, NA, (11011),
              TTLocalizer.QuestDialogDict[11010]),
    11011 : ( LAWBOT_HQ_TIER+5, Start, (RecoverItemQuest, ToontownGlobals.LighthouseLane, 1, 3027, Hard, Any), Same, Same, 4105, NA,
              TTLocalizer.QuestDialogDict[11011]),
    11012 : ( LAWBOT_HQ_TIER+6, Start, (VisitQuest,), Any, 3310, NA, (11013),
              TTLocalizer.QuestDialogDict[11012]),
    11013 : ( LAWBOT_HQ_TIER+6, Start, (RecoverItemQuest, ToontownGlobals.ElmStreet, 1, 3027, Hard, Any), Same, Same, 4106, NA,
              TTLocalizer.QuestDialogDict[11013]),
    11014 : ( LAWBOT_HQ_TIER+7, Start, (VisitQuest,), Any, 3310, NA, (11015),
              TTLocalizer.QuestDialogDict[11014]),
    11015 : ( LAWBOT_HQ_TIER+7, Start, (RecoverItemQuest, ToontownGlobals.MapleStreet, 1, 3027, Hard, Any), Same, Same, 4107, NA,
              TTLocalizer.QuestDialogDict[11015]),
    11016 : ( LAWBOT_HQ_TIER+8, Start, (VisitQuest,), Any, 3310, NA, (11017),
              TTLocalizer.QuestDialogDict[11016]),
    11017 : ( LAWBOT_HQ_TIER+8, Start, (RecoverItemQuest, ToontownGlobals.OakStreet, 1, 3027, Hard, Any), Same, Same, 4108, NA,
              TTLocalizer.QuestDialogDict[11017]),
    11018 : ( LAWBOT_HQ_TIER+9, Start, (VisitQuest,), Any, 3310, NA, (11019),
              TTLocalizer.QuestDialogDict[11018]),
    11019 : ( LAWBOT_HQ_TIER+9, Start, (RecoverItemQuest, ToontownGlobals.AltoAvenue, 1, 3027, Hard, Any), Same, Same, 4109, NA,
              TTLocalizer.QuestDialogDict[11019]),
    11020 : ( LAWBOT_HQ_TIER+10, Start, (VisitQuest,), Any, 3310, NA, (11021),
              TTLocalizer.QuestDialogDict[11020]),
    11021 : ( LAWBOT_HQ_TIER+10, Start, (RecoverItemQuest, ToontownGlobals.BaritoneBoulevard, 1, 3027, Hard, Any), Same, Same, 4110, NA,
              TTLocalizer.QuestDialogDict[11021]),
    11022 : ( LAWBOT_HQ_TIER+11, Start, (VisitQuest,), Any, 3310, NA, (11023),
              TTLocalizer.QuestDialogDict[11022]),
    11023 : ( LAWBOT_HQ_TIER+11, Start, (RecoverItemQuest, ToontownGlobals.TenorTerrace, 1, 3027, Hard, Any), Same, Same, 4111, NA,
              TTLocalizer.QuestDialogDict[11023]),
    11024 : ( LAWBOT_HQ_TIER+12, Start, (VisitQuest,), Any, 3310, NA, (11025),
              TTLocalizer.QuestDialogDict[11024]),
    11025 : ( LAWBOT_HQ_TIER+12, Start, (RecoverItemQuest, ToontownGlobals.LullabyLane, 1, 3027, Hard, Any), Same, Same, 4112, NA,
              TTLocalizer.QuestDialogDict[11025]),
    11026 : ( LAWBOT_HQ_TIER+13, Start, (VisitQuest,), Any, 3310, NA, (11027),
              TTLocalizer.QuestDialogDict[11026]),
    11027 : ( LAWBOT_HQ_TIER+13, Start, (RecoverItemQuest, ToontownGlobals.PajamaPlace, 1, 3027, Hard, Any), Same, Same, 4113, NA,
              TTLocalizer.QuestDialogDict[11027]),

    # Bossbot HQ suit part quests

    # Quest ID : ( tier, start, (questDesc), fromNpc, toNpc, reward, nextQuest, dialog )
    
    # Shep Ahoy needs you to really take a bite out of the Bossbots to earn your bossbot suit
    12000 : ( BOSSBOT_HQ_TIER, Start, (VisitQuest,), Any, 1222, NA, (12001),
              TTLocalizer.QuestDialogDict[12000]),
    12001 : ( BOSSBOT_HQ_TIER, Start, (CogQuest, Anywhere, 1, 'f'), Same, Same, 4200, NA,
              TTLocalizer.QuestDialogDict[12001]),
    12002 : ( BOSSBOT_HQ_TIER+1, Start, (VisitQuest,), Any, 1222, NA, (12003),
              TTLocalizer.QuestDialogDict[12002]),
    12003 : ( BOSSBOT_HQ_TIER+1, Start, (CogQuest, Anywhere, 1, 'p'), Same, Same, 4201, NA,
              TTLocalizer.QuestDialogDict[12003]),
    12004 : ( BOSSBOT_HQ_TIER+2, Start, (VisitQuest,), Any, 1222, NA, (12005),
              TTLocalizer.QuestDialogDict[12004]),
    12005 : ( BOSSBOT_HQ_TIER+2, Start, (CogQuest, Anywhere, 1, 'ym'), Same, Same, 4202, NA,
              TTLocalizer.QuestDialogDict[12005]),
    12006 : ( BOSSBOT_HQ_TIER+3, Start, (VisitQuest,), Any, 1222, NA, (12007),
              TTLocalizer.QuestDialogDict[12006]),
    12007 : ( BOSSBOT_HQ_TIER+3, Start, (CogQuest, Anywhere, 1, 'mm'), Same, Same, 4203, NA,
              TTLocalizer.QuestDialogDict[12007]),
    12008 : ( BOSSBOT_HQ_TIER+4, Start, (VisitQuest,), Any, 1222, NA, (12009),
              TTLocalizer.QuestDialogDict[12008]),
    12009 : ( BOSSBOT_HQ_TIER+4, Start, (CogQuest, Anywhere, 1, 'ds'), Same, Same, 4204, NA,
              TTLocalizer.QuestDialogDict[12009]),
    12010 : ( BOSSBOT_HQ_TIER+5, Start, (VisitQuest,), Any, 1222, NA, (12011),
              TTLocalizer.QuestDialogDict[12010]),
    12011 : ( BOSSBOT_HQ_TIER+5, Start, (CogQuest, Anywhere, 1, 'hh'), Same, Same, 4205, NA,
              TTLocalizer.QuestDialogDict[12011]),
    12012 : ( BOSSBOT_HQ_TIER+6, Start, (VisitQuest,), Any, 1222, NA, (12013),
              TTLocalizer.QuestDialogDict[12012]),
    12013 : ( BOSSBOT_HQ_TIER+6, Start, (CogQuest, Anywhere, 1, 'cr'), Same, Same, 4206, NA,
              TTLocalizer.QuestDialogDict[12013]),
    12014 : ( BOSSBOT_HQ_TIER+7, Start, (VisitQuest,), Any, 1222, NA, (12015),
              TTLocalizer.QuestDialogDict[12014]),
    12015 : ( BOSSBOT_HQ_TIER+7, Start, (CogQuest, Anywhere, 1, 'tbc'), Same, Same, 4207, NA,
              TTLocalizer.QuestDialogDict[12015]),
    12016 : ( BOSSBOT_HQ_TIER+8, Start, (VisitQuest,), Any, 1222, NA, (12017),
              TTLocalizer.QuestDialogDict[12016]),
    12017 : ( BOSSBOT_HQ_TIER+8, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4208, NA,
              TTLocalizer.QuestDialogDict[12017]),
    12018 : ( BOSSBOT_HQ_TIER+9, Start, (VisitQuest,), Any, 1222, NA, (12019),
              TTLocalizer.QuestDialogDict[12018]),
    12019 : ( BOSSBOT_HQ_TIER+9, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4209, NA,
              TTLocalizer.QuestDialogDict[12019]),
    12020 : ( BOSSBOT_HQ_TIER+10, Start, (VisitQuest,), Any, 1222, NA, (12021),
              TTLocalizer.QuestDialogDict[12020]),
    12021 : ( BOSSBOT_HQ_TIER+10, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4210, NA,
              TTLocalizer.QuestDialogDict[12021]),
    12022 : ( BOSSBOT_HQ_TIER+11, Start, (VisitQuest,), Any, 1222, NA, (12023),
              TTLocalizer.QuestDialogDict[12022]),
    12023 : ( BOSSBOT_HQ_TIER+11, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4211, NA,
              TTLocalizer.QuestDialogDict[12023]),
    12024 : ( BOSSBOT_HQ_TIER+12, Start, (VisitQuest,), Any, 1222, NA, (12025),
              TTLocalizer.QuestDialogDict[12024]),
    12025 : ( BOSSBOT_HQ_TIER+12, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4212, NA,
              TTLocalizer.QuestDialogDict[12025]),
    12026 : ( BOSSBOT_HQ_TIER+13, Start, (VisitQuest,), Any, 1222, NA, (12027),
              TTLocalizer.QuestDialogDict[12026]),
    12027 : ( BOSSBOT_HQ_TIER+13, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4213, NA,
              TTLocalizer.QuestDialogDict[12027]),
    12028 : ( BOSSBOT_HQ_TIER+14, Start, (VisitQuest,), Any, 1222, NA, (12029),
              TTLocalizer.QuestDialogDict[12028]),
    12029 : ( BOSSBOT_HQ_TIER+14, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4214, NA,
              TTLocalizer.QuestDialogDict[12029]),
    12030 : ( BOSSBOT_HQ_TIER+15, Start, (VisitQuest,), Any, 1222, NA, (12031),
              TTLocalizer.QuestDialogDict[12030]),
    12031 : ( BOSSBOT_HQ_TIER+15, Start, (SkeleReviveQuest, Anywhere, 1), Same, Same, 4215, NA,
              TTLocalizer.QuestDialogDict[12031]),
    12032 : ( BOSSBOT_HQ_TIER+16, Start, (VisitQuest,), Any, 2001, 4216, NA,
              TTLocalizer.QuestDialogDict[12032]),
    }
# End QuestDict


# Create the quest tier dict so we can more efficiently
# access quests based on their tier
# This is a dict of {tier : [questId, questId, ...]}
Tier2QuestsDict = {}
for questId, questDesc in QuestDict.items():
    # Only put quests that are singletons or the start of multiquests
    if (questDesc[QuestDictStartIndex] == Start):
        tier = questDesc[QuestDictTierIndex]
        if Tier2QuestsDict.has_key(tier):
            Tier2QuestsDict[tier].append(questId)
        else:
            Tier2QuestsDict[tier] = [questId]

# Quest2RewardDict is a dict of {questId : rewardId}, chasing down multipart quests
# Contains final rewards for all quests 
Quest2RewardDict = {}
# Tier2Reward2QuestsDict is a two-level dict of {tier : {reward : [questId, questId...]}}
Tier2Reward2QuestsDict = {}
# Quest2RemainingStepsDict is a dictionary which records the number of steps until quest completion
Quest2RemainingStepsDict = {}

def getAllRewardIdsForReward(rewardId):
    # maps a rewardId to a list of rewardIds for the purposes of filling
    # in Tier2Reward2QuestsDict; allows 'AnyCashbotSuitPart' quests to be
    # listed under all cashbot suit part rewards
    if rewardId is AnyCashbotSuitPart:
        return range(4000,4011+1)
    if rewardId is AnyLawbotSuitPart:
        return range(4100,4113+1)
    if rewardId is AnyBossbotSuitPart:
        return range(4200,4216+1)
    return (rewardId,)

def findFinalRewardId(questId):
    # A recursive function used to determine the final reward id associated with any quest id
    # Used to initialize Quest2RewardDict, Tier2Reward2QuestsDict, Quest2RemainingStepsDict
    finalRewardId = Quest2RewardDict.get(questId)
    if finalRewardId:
        # Already got it
        remainingSteps = Quest2RemainingStepsDict.get(questId)
    else:
        # New quest id, get description
        try:
            questDesc = QuestDict[questId]
        except KeyError:
            # Hmmm, no description found
            print 'findFinalRewardId: Quest ID: %d not found' % questId
            return -1
        # Is the end of the chain?
        nextQuestId = questDesc[QuestDictNextQuestIndex]
        if nextQuestId == NA:
            # Yes, get reward and record it
            finalRewardId = questDesc[QuestDictRewardIndex]
            remainingSteps = 1
        else:
            # Recurse down chain
            if type(nextQuestId) == type(()):
                # Multiple next links, use first one for ultimate answer
                finalRewardId, remainingSteps = findFinalRewardId(nextQuestId[0])
                # And recurse down the others to initialize them too
                for id in nextQuestId[1:]:
                    # And traverse other paths too
                    findFinalRewardId(id)
            else:
                finalRewardId, remainingSteps = findFinalRewardId(nextQuestId)
            # Increment step counter
            remainingSteps += 1
        # Record final reward for this quest Id and return value
        assert(finalRewardId != NA)
        if finalRewardId != OBSOLETE:
            # Only put quests that are singletons or the start of multiquests into Tier2Reward2QuestsDict
            if (questDesc[QuestDictStartIndex] == Start):
                tier = questDesc[QuestDictTierIndex]
                tier2RewardDict = Tier2Reward2QuestsDict.setdefault(tier, {})
                # list this quest under all applicable reward IDs; for
                # instance, list 'AnyCashbotSuitPart' quests under each
                # cashbot suit part reward
                rewardIds = getAllRewardIdsForReward(finalRewardId)
                for rewardId in rewardIds:
                    questList = tier2RewardDict.setdefault(rewardId, [])
                    questList.append(questId)
        else:
            finalRewardId = None
        Quest2RewardDict[questId] = finalRewardId
        Quest2RemainingStepsDict[questId] = remainingSteps
    return finalRewardId, remainingSteps

# Initialize dictionary
for questId in QuestDict.keys():
    findFinalRewardId(questId)

def getStartingQuests(tier = None):
    startingQuests = []
    for questId in QuestDict.keys():
        if isStartingQuest(questId):
            if tier is None:
                startingQuests.append(questId)
            elif questId in Tier2QuestsDict[tier]:
                startingQuests.append(questId)
    startingQuests.sort()
    return startingQuests
            
def getFinalRewardId(questId, fAll = 0):
    """
    Returns the final rewardId if fAll is set, 
    If fAll flag is not set, returns None if questId is not first part of mulitpart quest or singleton
    so that quest isn't added to avatars reward history in DistributedToonAI.py
    """
    if fAll or isStartingQuest(questId):
        return Quest2RewardDict.get(questId)
    else:
        return None

def isStartingQuest(questId):
    """
    Returns true is this quest is the start of a multipart quest or a singleton quest
    Returns None for invalid QuestIds
    """
    try:
        return (QuestDict[questId][QuestDictStartIndex] == Start)
    except KeyError:
        return None

def getNumChoices(tier):
    """
    Determine how many quest choices are presented to the user in each tier
    The idea is to slowly reveal more choices, starting from 1 or no choice
    """
    if tier in (0,):
        return 0
    if tier in (1,):
        return 2
    else:
        return 3

def getAvatarRewardId(av, questId):
    for quest in av.quests:
        if (questId == quest[0]):
            return quest[3]
    notify.warning('getAvatarRewardId(): quest not found on avatar')
    return None

def getNextQuest(id, currentNpc, av):
    """
    Given this quest id, see if there is another quest in the multipart
    quest. If so, return it. We need the currentNpc so we can decide who
    the next npc is and return that as well
    """
    nextQuest = QuestDict[id][QuestDictNextQuestIndex]
    if nextQuest == NA:
        return NA, NA
    elif type(nextQuest) == type(()):
        nextReward = QuestDict[nextQuest[0]][QuestDictRewardIndex]
        nextNextQuest, nextNextToNpcId = getNextQuest(nextQuest[0], currentNpc, av)
        if (nextReward == 400 and nextNextQuest == NA):
            nextQuest = chooseTrackChoiceQuest(av.getRewardTier(), av)
        else:
            nextQuest = random.choice(nextQuest)

    # If this quest is filtered for this avatar, skip it and
    # go to the next one after that. Oooh, recursion
    if not getQuestClass(nextQuest).filterFunc(av):
        return getNextQuest(nextQuest, currentNpc, av)

    nextToNpcId = getQuestToNpcId(nextQuest)
    if nextToNpcId == Any:
        # TODO: Choose one that is nearby, for now use Mary
        nextToNpcId = 2004
    elif nextToNpcId == Same:
        # If you were an HQ officer, keep it an HQ officer
        if currentNpc.getHq():
            nextToNpcId = ToonHQ
        else:
            nextToNpcId = currentNpc.getNpcId()
    elif nextToNpcId == ToonHQ:
        # TODO
        nextToNpcId = ToonHQ
    return nextQuest, nextToNpcId


def filterQuests(entireQuestPool, currentNpc, av):
    """
    Given this quest pool, this npc and this av, filter out the quests
    that are not allowed for various reasons and return a list of
    the good ones left over.
    Do not choose a quest:
       - this av has already done
       - that involves an avatar already on our quest list
    """
    if notify.getDebug():
        notify.debug('filterQuests: entireQuestPool: %s' % (entireQuestPool))
    # Start with the full list, then remove quests that are invalid
    validQuestPool = dict([(questId, 1) for questId in entireQuestPool])

    if isLoopingFinalTier(av.getRewardTier()):
        # If we are in the looping tier, we do not maintain the quest
        # history, but we still do not want to offer quests the avatar is
        # currently working on. So build the av quest history out of the
        # quest ids he is currently working on.
        history = map(lambda questDesc: questDesc[0], av.quests)
    else:
        # Note: history includes current quests
        history = av.getQuestHistory()
    if notify.getDebug():
        notify.debug('filterQuests: av quest history: %s' % (history))
    
    currentQuests = av.quests
    for questId in entireQuestPool:
        # If we have had this quest before (or have it now),
        # remove it from the validQuestPool
        if questId in history:
            if notify.getDebug():
                notify.debug("filterQuests: Removed %s because in history" % (questId))
            validQuestPool[questId] = 0
            continue

        # If the quest has defined a fromNpcId, check it
        # Throw this quest out if it does not match.
        # Most quests start with Any, so they almost all match.
        potentialFromNpc = getQuestFromNpcId(questId)

        # if ((potentialFromNpc != Any) and
        #    (currentNpc.getNpcId() != potentialFromNpc)):
        if not npcMatches(potentialFromNpc, currentNpc):
            if notify.getDebug():
                notify.debug("filterQuests: Removed %s: potentialFromNpc does not match currentNpc" % (questId))
            validQuestPool[questId] = 0
            # Move on to the next quest
            continue

        # If this potential npc is involved in the current quest in question,
        # do not consider this quest. This will prevent npcs from telling you
        # to visit themselves, for instance.
        potentialToNpc = getQuestToNpcId(questId)
        if (currentNpc.getNpcId() == potentialToNpc):
            if notify.getDebug():
                notify.debug("filterQuests: Removed %s because potentialToNpc is currentNpc" % (questId))
            validQuestPool[questId] = 0
            # Move on to the next quest
            continue

        # See if this quest is filtered for this av
        if not getQuestClass(questId).filterFunc(av):
            if notify.getDebug():
                notify.debug("filterQuests: Removed %s because of filterFunc" % (questId))
            validQuestPool[questId] = 0
            continue

        # If this potentialToNpc from this quest is already involved
        # in a quest on our currentQuest list, remove it
        for quest in currentQuests:
            fromNpcId = quest[1]
            toNpcId = quest[2]
            # Do we really need to check the fromNpcId?
            #if (
            # ((potentialToNpc == fromNpcId) and (fromNpcId != ToonHQ)) or
            # Does the quest we are thinking about taking have the same toNpc
            # as a quest we already have?
            #    ((potentialToNpc == toNpcId) and (toNpcId != ToonHQ)) or
            # Are any of the quests we have from this npc
            #    (currentNpc.getNpcId() == fromNpcId)):
            if ((potentialToNpc == toNpcId) and (toNpcId != ToonHQ)):
                validQuestPool[questId] = 0
                if notify.getDebug():
                    notify.debug("filterQuests: Removed %s because npc involved" % (questId))
                break

    finalQuestPool = filter(lambda key : validQuestPool[key], validQuestPool.keys())
    if notify.getDebug():
        notify.debug("filterQuests: finalQuestPool: %s" % (finalQuestPool))
    return finalQuestPool

def chooseTrackChoiceQuest(tier, av, fixed=0):

    # If we detect that the track array is bad for some reason, let's
    # try to fix it then choose the track again.
    def fixAndCallAgain():
        if ((not fixed) and av.fixTrackAccess()):
            notify.info(("av %s trackAccess fixed: %s"
                            % (av.getDoId(), trackAccess)))
            # Now try choosing the quest again, setting the fixed flag
            # to prevent an infinite loop
            return chooseTrackChoiceQuest(tier, av, fixed=1)
        else:
            # Already tried to fix this once, just return None
            return None        
    
    bestQuest = None
    trackAccess = av.getTrackAccess()
    if (tier == MM_TIER):
        # We need to pick between these two quests based on the trackAccess
        # this av already has
        # 4001 chooses between TRAP and HEAL
        # 4002 chooses between TRAP and SOUND
        if (trackAccess[ToontownBattleGlobals.HEAL_TRACK] == 1):
            # av already has HEAL, give him 4002
            bestQuest = 4002
        elif (trackAccess[ToontownBattleGlobals.SOUND_TRACK] == 1):
            # av already has SOUND, give him 4001
            bestQuest = 4001
        else:
            notify.warning(("av %s has bogus trackAccess: %s"
                            % (av.getDoId(), trackAccess)))
            return fixAndCallAgain()

    elif (tier == BR_TIER):
        # We need to pick between these two quests based on the trackAccess
        # this av already has
        if (trackAccess[ToontownBattleGlobals.TRAP_TRACK] == 1):
            if (trackAccess[ToontownBattleGlobals.SOUND_TRACK] == 1):
                if (trackAccess[ToontownBattleGlobals.DROP_TRACK] == 1):
                    bestQuest = 5004
                elif (trackAccess[ToontownBattleGlobals.LURE_TRACK] == 1):
                    bestQuest = 5003
                else:
                    notify.warning(("av %s has bogus trackAccess: %s"
                                    % (av.getDoId(), trackAccess)))
                    return fixAndCallAgain()
            elif (trackAccess[ToontownBattleGlobals.HEAL_TRACK] == 1):
                if (trackAccess[ToontownBattleGlobals.DROP_TRACK] == 1):
                    bestQuest = 5002
                elif (trackAccess[ToontownBattleGlobals.LURE_TRACK] == 1):
                    bestQuest = 5001
                else:
                    notify.warning(("av %s has bogus trackAccess: %s"
                                    % (av.getDoId(), trackAccess)))
                    return fixAndCallAgain()
        else:
            # If you do not have TRAP, then see the other track you do
            # not have and pick that choice quest
            if (trackAccess[ToontownBattleGlobals.SOUND_TRACK] == 0):
                bestQuest = 5005
            elif (trackAccess[ToontownBattleGlobals.HEAL_TRACK] == 0):
                bestQuest = 5006
            elif (trackAccess[ToontownBattleGlobals.DROP_TRACK] == 0):
                bestQuest = 5007
            elif (trackAccess[ToontownBattleGlobals.LURE_TRACK] == 0):
                bestQuest = 5008
            else:
                notify.warning(("av %s has bogus trackAccess: %s"
                                % (av.getDoId(), trackAccess)))
                return fixAndCallAgain()
    else:
        if notify.getDebug():
            notify.debug(("questPool for reward 400 had no dynamic choice, tier: %s") % (tier))
        bestQuest = seededRandomChoice(Tier2Reward2QuestsDict[tier][400])
    if notify.getDebug():
        notify.debug("chooseTrackChoiceQuest: avId: %s trackAccess: %s tier: %s bestQuest: %s" %
                     (av.getDoId(), trackAccess, tier, bestQuest))
    return bestQuest
    

def chooseMatchingQuest(tier, validQuestPool, rewardId, npc, av):
    """
    Choose a quest from quest pool that matches a reward and this npc
    Only choose quests that are in the validQuestPool
    TODO: match NPC
    """
    # If this is a single part trackChoiceQuest, we need to pick the
    # correct choice based on what the avatar has chosen. If this is
    # a multipart, this will be called on the final quest
    questsMatchingReward = Tier2Reward2QuestsDict[tier].get(rewardId, [])
    if notify.getDebug():
        notify.debug("questsMatchingReward: %s tier: %s = %s" %
                     (rewardId, tier, questsMatchingReward))
    if ((rewardId == 400) and (QuestDict[questsMatchingReward[0]][QuestDictNextQuestIndex] == NA)):
        # Ok, it is not multipart, just pick the track choice
        bestQuest = chooseTrackChoiceQuest(tier, av)
        if notify.getDebug():
            notify.debug("single part track choice quest: %s tier: %s avId: %s trackAccess: %s bestQuest: %s" %
                         (rewardId, tier, av.getDoId(), av.getTrackAccess(), bestQuest))
    else:
        validQuestsMatchingReward = PythonUtil.intersection(questsMatchingReward, validQuestPool)
        if notify.getDebug():
            notify.debug("validQuestsMatchingReward: %s tier: %s = %s" %
                         (rewardId, tier, validQuestsMatchingReward))
        if validQuestsMatchingReward:
            bestQuest = seededRandomChoice(validQuestsMatchingReward)
        else:
            # there were no exact matches
            # check for AnyCashbotSuitPart matches
            questsMatchingReward = Tier2Reward2QuestsDict[tier].get(AnyCashbotSuitPart, [])
            if notify.getDebug():
                notify.debug("questsMatchingReward: AnyCashbotSuitPart tier: %s = %s" %
                             (tier, questsMatchingReward))
            validQuestsMatchingReward = PythonUtil.intersection(questsMatchingReward, validQuestPool)
            if validQuestsMatchingReward:
                if notify.getDebug():
                    notify.debug("validQuestsMatchingReward: AnyCashbotSuitPart tier: %s = %s" %
                                 (tier, validQuestsMatchingReward))
                bestQuest = seededRandomChoice(validQuestsMatchingReward)
            else:
                # still no matches
                # check for AnyLawbotSuitPart matches 
                questsMatchingReward = Tier2Reward2QuestsDict[tier].get(AnyLawbotSuitPart, [])
                if notify.getDebug():
                    notify.debug("questsMatchingReward: AnyLawbotSuitPart tier: %s = %s" %
                                 (tier, questsMatchingReward))
                validQuestsMatchingReward = PythonUtil.intersection(questsMatchingReward, validQuestPool)
                if validQuestsMatchingReward:
                    if notify.getDebug():
                        notify.debug("validQuestsMatchingReward: AnyLawbotSuitPart tier: %s = %s" %
                                     (tier, validQuestsMatchingReward))
                    bestQuest = seededRandomChoice(validQuestsMatchingReward)
                else:
                    # OK, just pick randomly from the Any pool
                    questsMatchingReward = Tier2Reward2QuestsDict[tier].get(Any, [])
                    if notify.getDebug():
                        notify.debug("questsMatchingReward: Any tier: %s = %s" %
                                     (tier, questsMatchingReward))
                    # There better be some of these or it is an error
                    if not questsMatchingReward:
                        notify.warning("chooseMatchingQuests, no questsMatchingReward")
                        return None
                    validQuestsMatchingReward = PythonUtil.intersection(questsMatchingReward, validQuestPool)
                    if not validQuestsMatchingReward:
                        notify.warning("chooseMatchingQuests, no validQuestsMatchingReward")
                        return None
                    if notify.getDebug():
                        notify.debug("validQuestsMatchingReward: Any tier: %s = %s" %
                                     (tier, validQuestsMatchingReward))
                    bestQuest = seededRandomChoice(validQuestsMatchingReward)
    return bestQuest

def transformReward(baseRewardId, av):
    # We need to replace rewardId 900 with the actual rewardId of the
    # TrackCompleteReward that this av is training for.
    # Same with the 800 quests
    if (baseRewardId == 900):
        trackId, progress = av.getTrackProgress()
        if trackId == -1:
            notify.warning("transformReward: asked to transform 900 but av is not training")
            # Just return the original
            actualRewardId = baseRewardId
        else:
            actualRewardId = 900 + 1 + trackId
        return actualRewardId
    elif ((baseRewardId > 800) and (baseRewardId < 900)):
        trackId, progress = av.getTrackProgress()
        # So for drop trackId = 6, do some offsets to get the real reward
        # Each track is in a space of 100 quests
        # Quests start at 1000, so add 200 to get to 1000
        # 801 becomes 801 + 200 + (6 * 100) = 1601
        if trackId < 0:
            # Somehow you are training quests, but did not pick one. This happens
            # when you setQuestTier for instance
            notify.warning("transformReward: av: %s is training a track with none chosen!" %
                           (av.getDoId()))
            # In that case, just switch with a jellybean quest I guess
            # This should not happen in production
            return 601
        else:
            actualRewardId = baseRewardId + 200 + (trackId * 100)
            return actualRewardId
    else:
        # Return the reward unchanged
        return baseRewardId
    

def chooseBestQuests(tier, currentNpc, av):
    """
    Returns a list of questIds from this tier 
    """
    # We seed the random number generator so this npc will present the same
    # quests to this avatar if the avatar thinks he's clever and repeatedly
    # approaches the NPC "shopping" for different quests

    if isLoopingFinalTier(tier):
        # If we are in the looping final tier, we do not maintain any
        # reward history. Instead, just look at what the av is currently
        # working on so we do not offer those at the same time.
        rewardHistory = map(lambda questDesc: questDesc[3], av.quests)
    else:
        rewardHistory = av.getRewardHistory()[1]

    seedRandomGen(currentNpc.getNpcId(), av.getDoId(), tier, rewardHistory)

    # See how many choices of quests we are allowed to have
    numChoices = getNumChoices(tier)
    # Now choose some rewards to help us pick the quests
    rewards = getNextRewards(numChoices, tier, av)
    # If we are out of rewards, return empty
    if not rewards:
        return []

    # Figure out the set of possible quests you could have
    # This will make filtering them faster
    possibleQuests = []
    possibleRewards = list(rewards)
    if Any not in possibleRewards:
        possibleRewards.append(Any)
    for rewardId in possibleRewards:
        possibleQuests.extend(Tier2Reward2QuestsDict[tier].get(rewardId, []))

    # Filter the quest pool down to the ones we have not done,
    # that this npc is not involved in, etc.
    validQuestPool = filterQuests(possibleQuests, currentNpc, av)
    # If we are out of quests, return empty
    if not validQuestPool:
        return []

    # This means you get no choice, but you still get a quest
    if numChoices == 0:
        numChoices = 1

    # Now generate the list of quests we will return
    bestQuests = []
    for i in range(numChoices):
        # If we are out of quests, break
        if len(validQuestPool) == 0:
            break
        # If we are out of rewards, break
        if len(rewards) == 0:
            break

        # Choose one that matches this npc, reward, etc
        rewardId = rewards.pop(0)
        bestQuestId = chooseMatchingQuest(tier, validQuestPool, rewardId, currentNpc, av)
        # If that came back None for some reason, just continue to the next choice
        if bestQuestId is None:
            continue
        # Remove it from consideration in the next pick
        validQuestPool.remove(bestQuestId)

        # Now choose a toNpc for each quest
        # The quest may specify one, if it does return that one
        bestQuestToNpcId = getQuestToNpcId(bestQuestId)
        if bestQuestToNpcId == Any:
            # TODO: choose one that is nearby, for now use Prof Pete
            bestQuestToNpcId = 2003
        elif bestQuestToNpcId == Same:
            # If you were an HQ officer, keep it an HQ officer
            if currentNpc.getHq():
                bestQuestToNpcId = ToonHQ
            else:
                bestQuestToNpcId = currentNpc.getNpcId()
        elif bestQuestToNpcId == ToonHQ:
            # flag as a toon hq npc
            bestQuestToNpcId = ToonHQ
        
        # Append it to the list we are making
        bestQuests.append([bestQuestId, rewardId, bestQuestToNpcId])

    for quest in bestQuests:
        quest[1] = transformReward(quest[1], av)
    return bestQuests


def questExists(id):
    return QuestDict.has_key(id)

def getQuest(id):
    """
    Returns an actual Quest object with properties from this id.
    """
    questEntry = QuestDict.get(id)
    if questEntry:
        questDesc = questEntry[QuestDictDescIndex]
        questClass = questDesc[0]
        # Instantiate a quest object from this class
        return questClass(id, questDesc[1:])
    else:
        # Did not find it
        return None

def getQuestClass(id):
    """
    Sometimes all you need is the quest class, so call this.
    It is more efficient than creating a quest object and asking getType.
    """
    questEntry = QuestDict.get(id)
    if questEntry:
        return questEntry[QuestDictDescIndex][0]
    else:
        # Did not find it
        return None    

def getVisitSCStrings(npcId):
    if npcId == ToonHQ:
        strings = [TTLocalizer.QuestsRecoverItemQuestSeeHQSCString,
                   TTLocalizer.QuestsRecoverItemQuestGoToHQSCString,
                   ]
    elif npcId == ToonTailor:
        strings = [TTLocalizer.QuestsTailorQuestSCString,
                   ]
    elif npcId:
        npcName, hoodName, buildingArticle, buildingName, toStreet, streetName, isInPlayground = getNpcInfo(npcId)
        strings = [TTLocalizer.QuestsVisitQuestSeeSCString % (npcName),
                   ]
        if isInPlayground:
            strings.append(TTLocalizer.QuestsRecoverItemQuestGoToPlaygroundSCString % (hoodName))
        else:
            strings.append(TTLocalizer.QuestsRecoverItemQuestGoToStreetSCString % {'to':toStreet, 'street':streetName, 'hood':hoodName})
        strings.extend([
            TTLocalizer.QuestsRecoverItemQuestVisitBuildingSCString % (buildingArticle, buildingName),
            TTLocalizer.QuestsRecoverItemQuestWhereIsBuildingSCString  % (buildingArticle, buildingName),
            ])

    return strings

def getFinishToonTaskSCStrings(npcId):
    return [
        TTLocalizer.QuestsGenericFinishSCString,
        ] + getVisitSCStrings(npcId)

def chooseQuestDialog(id, status):
    questDialog = getQuestDialog(id).get(status)
    if questDialog == None:
        if status == QUEST:
            quest = getQuest(id)
            questDialog = quest.getDefaultQuestDialog()
        else:
            questDialog = DefaultDialog[status]
    if type(questDialog) == type(()):
        return random.choice(questDialog)
    else:
        return questDialog

# No quest id is needed for rejection since you will not have been
# assigned one. Just use the default rejection list
def chooseQuestDialogReject():
    return random.choice(DefaultReject)

# No quest id is needed for rejection since you will not have been
# assigned one. Just use the default rejection list
def chooseQuestDialogTierNotDone():
    return random.choice(DefaultTierNotDone)

def getNpcInfo(npcId):
    npcName = NPCToons.getNPCName(npcId)
    npcZone = NPCToons.getNPCZone(npcId)
    hoodId = ZoneUtil.getCanonicalHoodId(npcZone)
    hoodName = base.cr.hoodMgr.getFullnameFromId(hoodId)
    buildingArticle = NPCToons.getBuildingArticle(npcZone)    
    buildingName = NPCToons.getBuildingTitle(npcZone)
    branchId = ZoneUtil.getCanonicalBranchZone(npcZone)
    toStreet = ToontownGlobals.StreetNames[branchId][0]    
    streetName = ToontownGlobals.StreetNames[branchId][-1]
    isInPlayground = ZoneUtil.isPlayground(branchId)
    return (npcName, hoodName, buildingArticle, buildingName, toStreet, streetName, isInPlayground)

def getNpcLocationDialog(fromNpcId, toNpcId):
    # Returns (paragraph, buildingName, streetDesc)
    
    if not toNpcId:
        return (None, None, None)

    fromNpcZone = None
    fromBranchId = None
    if fromNpcId:
        fromNpcZone = NPCToons.getNPCZone(fromNpcId)
        fromBranchId = ZoneUtil.getCanonicalBranchZone(fromNpcZone)

    toNpcZone = NPCToons.getNPCZone(toNpcId)
    toBranchId = ZoneUtil.getCanonicalBranchZone(toNpcZone)

    toNpcName, toHoodName, toBuildingArticle, toBuildingName, toStreetTo, toStreetName, isInPlayground = getNpcInfo(toNpcId)

    if (fromBranchId == toBranchId):
        # If you are in the same branch zone, simplify the text to make
        # it sound more natural
        if isInPlayground:
            streetDesc = TTLocalizer.QuestsStreetLocationThisPlayground
        else:
            streetDesc = TTLocalizer.QuestsStreetLocationThisStreet
    else:
        if isInPlayground:
            streetDesc = TTLocalizer.QuestsStreetLocationNamedPlayground % (toHoodName)
        else:
            streetDesc = TTLocalizer.QuestsStreetLocationNamedStreet % {'toStreetName':toStreetName, 'toHoodName':toHoodName}

    paragraph = TTLocalizer.QuestsLocationParagraph % {'building' : TTLocalizer.QuestsLocationBuilding % (toNpcName),
                                                     'buildingName' : toBuildingName,
                                                     'buildingVerb' : TTLocalizer.QuestsLocationBuildingVerb,
                                                     'street' : streetDesc}    

    return (paragraph, toBuildingName, streetDesc)

def fillInQuestNames(text, avName = None, fromNpcId = None, toNpcId = None):
    text = copy.deepcopy(text)
    
    if avName != None:
        text = string.replace(text, '_avName_', avName)

    if toNpcId:
        if toNpcId == ToonHQ:
            toNpcName = TTLocalizer.QuestsHQOfficerFillin
            where = TTLocalizer.QuestsHQWhereFillin
            buildingName = TTLocalizer.QuestsHQBuildingNameFillin
            streetDesc = TTLocalizer.QuestsHQLocationNameFillin
            
        elif toNpcId == ToonTailor:
            toNpcName = TTLocalizer.QuestsTailorFillin
            where = TTLocalizer.QuestsTailorWhereFillin
            buildingName = TTLocalizer.QuestsTailorBuildingNameFillin
            streetDesc = TTLocalizer.QuestsTailorLocationNameFillin
            
        else:
            toNpcName = str(NPCToons.getNPCName(toNpcId))
            where, buildingName, streetDesc = getNpcLocationDialog(fromNpcId, toNpcId)

        text = string.replace(text, '_toNpcName_', toNpcName)
        text = string.replace(text, '_where_', where)
        text = string.replace(text, '_buildingName_', buildingName)
        text = string.replace(text, '_streetDesc_', streetDesc)
            
    return text
    

def getVisitingQuest():
    """
    Returns a visiting Quest object
    """
    return VisitQuest(VISIT_QUEST_ID)

class Reward:
    def __init__(self, id, reward):
        self.id = id
        self.reward = reward
    def getId(self):
        return self.id
    def getType(self):
        return self.__class__
    def getAmount(self):
        return None
    def sendRewardAI(self, av):
        raise "not implemented"
    def countReward(self, qrc):
        raise "not implemented"
    def getString(self):
        return "undefined"
    def getPosterString(self):
        return "base class"

class MaxHpReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getAmount(self):
        return self.reward[0]
    def sendRewardAI(self, av):
        maxHp = av.getMaxHp()
        # Add the amount, but make sure it is not over the global max
        maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + self.getAmount())
        av.b_setMaxHp(maxHp)
        # Also, give them a full heal
        av.toonUp(maxHp)
    def countReward(self, qrc):
        qrc.maxHp += self.getAmount()
    def getString(self):
        return (TTLocalizer.QuestsMaxHpReward % (self.getAmount()))
    def getPosterString(self):
        return (TTLocalizer.QuestsMaxHpRewardPoster % self.getAmount())

class MoneyReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getAmount(self):
        return self.reward[0]
    def sendRewardAI(self, av):
        money = av.getMoney()
        maxMoney = av.getMaxMoney()
        # With banking system, excess money gets put in
        # the bank automatically, without having to check maxMoney
        av.addMoney(self.getAmount())
    def countReward(self, qrc):
        qrc.money += self.getAmount()
    def getString(self):
        amt = self.getAmount()
        if amt == 1:
            return (TTLocalizer.QuestsMoneyRewardSingular)
        else:
            return (TTLocalizer.QuestsMoneyRewardPlural % (amt))
    def getPosterString(self):
        amt = self.getAmount()
        if amt == 1:
            return (TTLocalizer.QuestsMoneyRewardPosterSingular)
        else:
            return (TTLocalizer.QuestsMoneyRewardPosterPlural % (amt))

class MaxMoneyReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getAmount(self):
        return self.reward[0]
    def sendRewardAI(self, av):
        av.b_setMaxMoney(self.getAmount())
    def countReward(self, qrc):
        qrc.maxMoney = self.getAmount()
    def getString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMaxMoneyRewardSingular
        else:
            return (TTLocalizer.QuestsMaxMoneyRewardPlural % (amt))
    def getPosterString(self):
        amt = self.getAmount()
        if amt == 1:
            return TTLocalizer.QuestsMaxMoneyRewardPosterSingular
        else:
            return (TTLocalizer.QuestsMaxMoneyRewardPosterPlural % (amt))

class MaxGagCarryReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getAmount(self):
        return self.reward[0]
    def getName(self):
        return self.reward[1]
    def sendRewardAI(self, av):
        av.b_setMaxCarry(self.getAmount())
    def countReward(self, qrc):
        qrc.maxCarry = self.getAmount()
    def getString(self):
        name = self.getName()
        amt = self.getAmount()
        return (TTLocalizer.QuestsMaxGagCarryReward % {"name" : name, "num" : amt})
    def getPosterString(self):
        name = self.getName()
        amt = self.getAmount()
        return (TTLocalizer.QuestsMaxGagCarryRewardPoster % {"name" : name, "num" : amt})

class MaxQuestCarryReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getAmount(self):
        return self.reward[0]
    def sendRewardAI(self, av):
        av.b_setQuestCarryLimit(self.getAmount())
    def countReward(self, qrc):
        qrc.questCarryLimit = self.getAmount()
    def getString(self):
        amt = self.getAmount()
        return (TTLocalizer.QuestsMaxQuestCarryReward % (amt))
    def getPosterString(self):
        amt = self.getAmount()
        return (TTLocalizer.QuestsMaxQuestCarryRewardPoster % (amt))

class TeleportReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getZone(self):
        return self.reward[0]
    def sendRewardAI(self, av):
        av.addTeleportAccess(self.getZone())
    def countReward(self, qrc):
        qrc.addTeleportAccess(self.getZone())
    def getString(self):
        hoodName = ToontownGlobals.hoodNameMap[self.getZone()][-1]
        return (TTLocalizer.QuestsTeleportReward % (hoodName))
    def getPosterString(self):
        hoodName = ToontownGlobals.hoodNameMap[self.getZone()][-1]
        return (TTLocalizer.QuestsTeleportRewardPoster % (hoodName))

# How much training do you need to learn each track?
TrackTrainingQuotas = {
    ToontownBattleGlobals.HEAL_TRACK : 15,
    ToontownBattleGlobals.TRAP_TRACK : 15,
    ToontownBattleGlobals.LURE_TRACK : 15,
    ToontownBattleGlobals.SOUND_TRACK: 15,
    ToontownBattleGlobals.THROW_TRACK : 15,
    ToontownBattleGlobals.SQUIRT_TRACK : 15,
    ToontownBattleGlobals.DROP_TRACK : 15,
    }
    
class TrackTrainingReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track
    def sendRewardAI(self, av):
        # Start out with 0 progress
        av.b_setTrackProgress(self.getTrack(), 0)
    def countReward(self, qrc):
        # TODO: how will this trackId get filled in?
        # Start out with 0 progress
        qrc.trackProgressId = self.getTrack()
        qrc.trackProgress = 0
    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackTrainingReward % (trackName))
    def getPosterString(self):
        # We do not know which track the user will pick yet, so we do not
        # know the trackName to fill in
        # trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackTrainingRewardPoster)

class TrackProgressReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track
    def getProgressIndex(self):
        return self.reward[1]
    def sendRewardAI(self, av):
        av.addTrackProgress(self.getTrack(), self.getProgressIndex())
    def countReward(self, qrc):
        qrc.addTrackProgress(self.getTrack(), self.getProgressIndex())
    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackProgressReward %
                {"frameNum" : self.getProgressIndex(), "trackName" : trackName})
    def getPosterString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackProgressRewardPoster %
                {"trackName" : trackName, "frameNum" : self.getProgressIndex()})

class TrackCompleteReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getTrack(self):
        track = self.reward[0]
        if track == None:
            track = 0
        return track
    def sendRewardAI(self, av):
        av.addTrackAccess(self.getTrack())
        av.clearTrackProgress()
    def countReward(self, qrc):
        # TODO: how will this trackId get filled in?
        qrc.addTrackAccess(self.getTrack())
        qrc.clearTrackProgress()
    def getString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackCompleteReward % (trackName))
    def getPosterString(self):
        trackName = ToontownBattleGlobals.Tracks[self.getTrack()].capitalize()
        return (TTLocalizer.QuestsTrackCompleteRewardPoster % (trackName))

class ClothingTicketReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def sendRewardAI(self, av):
        return
    def countReward(self, qrc):
        return
    def getString(self):
        return (TTLocalizer.QuestsClothingTicketReward)
    def getPosterString(self):
        return (TTLocalizer.QuestsClothingTicketRewardPoster)
        
class TIPClothingTicketReward(ClothingTicketReward):
    def __init__(self, id, reward):
        ClothingTicketReward.__init__(self, id, reward)
    def getString(self):
        return (TTLocalizer.TIPQuestsClothingTicketReward)
    def getPosterString(self):
        return (TTLocalizer.TIPQuestsClothingTicketRewardPoster)

class CheesyEffectReward(Reward):
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getEffect(self):
        return self.reward[0]
    def getHoodId(self):
        return self.reward[1]
    def getDurationMinutes(self):
        return self.reward[2]
    def sendRewardAI(self, av):
        expireTime = (int)(time.time() / 60 + 0.5) + self.getDurationMinutes()
        av.b_setCheesyEffect(self.getEffect(), self.getHoodId(), expireTime)
    def countReward(self, qrc):
        pass
    def getString(self):
        effect = self.getEffect()
        hoodId = self.getHoodId()
        duration = self.getDurationMinutes()
        string = TTLocalizer.CheesyEffectMinutes
        if duration > 90:
            duration = (int)((duration + 30) / 60)
            string = TTLocalizer.CheesyEffectHours
            if duration > 36:
                duration = (int)((duration + 12) / 24)
                string = TTLocalizer.CheesyEffectDays
        desc = TTLocalizer.CheesyEffectDescriptions[effect][1]
        if (hoodId == 0):
            whileStr = ""
        elif (hoodId == 1):
            whileStr = (TTLocalizer.CheesyEffectExceptIn % (TTLocalizer.ToontownCentral[-1]))
        else:
            hoodName = base.cr.hoodMgr.getFullnameFromId(hoodId)
            whileStr = (TTLocalizer.CheesyEffectWhileYouAreIn % (hoodName))
        if duration:
            return (string % {"time" :       duration,
                              "effectName" : desc,
                              "whileIn" :    whileStr,})
        else:
            return TTLocalizer.CheesyEffectIndefinite % {"effectName" : desc,
                                                       "whileIn" :    whileStr, }
        
    def getPosterString(self):
        effect = self.getEffect()
        desc = TTLocalizer.CheesyEffectDescriptions[effect][0]
        return (TTLocalizer.QuestsCheesyEffectRewardPoster % (desc))

class CogSuitPartReward(Reward):
    trackNames = [TTLocalizer.Bossbot, TTLocalizer.Lawbot,
                   TTLocalizer.Cashbot, TTLocalizer.Sellbot]
    def __init__(self, id, reward):
        Reward.__init__(self, id, reward)
    def getCogTrack(self):
        return self.reward[0]
    def getCogPart(self):
        return self.reward[1]
    def sendRewardAI(self, av):
        dept = self.getCogTrack()
        part = self.getCogPart()
        av.giveCogPart(part, dept)
    def countReward(self, qrc):
        # TODO!
        return
    def getCogTrackName(self):
        index = ToontownGlobals.cogDept2index[self.getCogTrack()]
        return CogSuitPartReward.trackNames[index]
    def getCogPartName(self):
        index = ToontownGlobals.cogDept2index[self.getCogTrack()]
        return CogDisguiseGlobals.PartsQueryNames[index][self.getCogPart()]
    def getString(self):
        return (TTLocalizer.QuestsCogSuitPartReward %
                {'cogTrack':self.getCogTrackName(),
                 'part':self.getCogPartName()})
    def getPosterString(self):
        return (TTLocalizer.QuestsCogSuitPartRewardPoster %
                {'cogTrack':self.getCogTrackName(),
                 'part':self.getCogPartName()})

    

def getRewardClass(id):
    """
    Sometimes all you need is the reward class, so call this.
    It is more efficient than creating a reward object and asking it.
    """
    reward = RewardDict.get(id)
    if reward:
        return reward[0]
    else:
        return None

def getReward(id):
    """
    Create and return an actual reward object from this id
    """
    reward = RewardDict.get(id)
    if reward:
        rewardClass = reward[0]
        return rewardClass(id, reward[1:])
    else:
        notify.warning('getReward(): id %s not found.' % (id))
        return None

def getNextRewards(numChoices, tier, av):
    """
    Generate a list containing the next few required rewards with
    some optional rewards mixed in at random. Then choose randomly
    from this list to return the next rewards.

    If we are at or near the end of the tier, fill in the list
    with optional rewards.
    """
    # list gives us a copy
    rewardTier = list(getRewardsInTier(tier))
    optRewards = list(getOptionalRewardsInTier(tier))

    # give trialers something to do since we won't let them fininsh their last gag track task
    if av.getGameAccess() == OTPGlobals.AccessFull and \
       tier == TT_TIER +3:
        # force paid players to pickup the quest to finish their gag track
        optRewards = [] 

    if isLoopingFinalTier(tier):
        # If we are in the looping final tier, we do not maintain any
        # reward history. Instead, just look at what the av is currently
        # working on so we do not offer those at the same time.
        rewardHistory = map(lambda questDesc: questDesc[3], av.quests)
        if notify.getDebug():
            notify.debug('getNextRewards: current rewards (history): %s' % (rewardHistory))
    else:
        rewardHistory = av.getRewardHistory()[1]
        if notify.getDebug():
            notify.debug('getNextRewards: rewardHistory: %s' % (rewardHistory))

    if notify.getDebug():
            notify.debug('getNextRewards: rewardTier: %s' % (rewardTier))
            notify.debug('getNextRewards: numChoices: %s' % (numChoices))

    # Iterate over the original rewards from the tier, not the rewardTier list
    # because we are going to be modifying rewardTier (removing rewards)
    for rewardId in getRewardsInTier(tier):
        # See if this is a CogSuitPartReward
        # If it is, we do not want to offer a reward for a part the toon already has
        if getRewardClass(rewardId) == CogSuitPartReward:
            # Make sure we do not already have this reward
            deptStr = RewardDict.get(rewardId)[1]
            cogPart = RewardDict.get(rewardId)[2]
            dept = ToontownGlobals.cogDept2index[deptStr]
            if av.hasCogPart(cogPart, dept):
                notify.debug('getNextRewards: already has cog part: %s dept: %s' % (cogPart, dept))
                # The avatar already has this cog part - do not offer the reward
                rewardTier.remove(rewardId)
            else:
                notify.debug('getNextRewards: keeping quest for cog part: %s dept: %s' % (cogPart, dept))

    # Remove the rewards that are in our history
    for rewardId in rewardHistory:
        if rewardId in rewardTier:
            rewardTier.remove(rewardId)
        elif rewardId in optRewards:
            optRewards.remove(rewardId)
        # See if this is the TrackCompleteReward
        elif (rewardId in (901,902,903,904,905,906,907)):
            genericRewardId = 900
            if genericRewardId in rewardTier:
                rewardTier.remove(genericRewardId)
        # See if this is a track progress reward. If so, it will be stored
        # as the actual reward number, like 1301 instead of the generic
        # reward number like 801. To prevent duplicate rewards from being
        # shown, if we see 1301 here, we need to remove 801 from the running
        elif (rewardId > 1000 and rewardId < 1699):
            index = rewardId % 100
            genericRewardId = 800 + index
            if genericRewardId in rewardTier:
                rewardTier.remove(genericRewardId)


    # If you have no choice, just return the first one in the list
    # Make sure there are any on the list
    if numChoices == 0:
        if (len(rewardTier) == 0):
            return []
        else: 
            return [rewardTier[0]]

    # If there are none in the tier, make the player complete the ones he has and
    # do not offer optional rewards
    # Maybe we do not want to do this. Why not let them work on some optional ones?
    # The only downside is people may keep doing optional quests not knowing they
    # are blocking their own progress to the next tier. This is probably the lesser
    # of two evils.
    # if (len(rewardTier) == 0):
    #     notify.debug('getNextRewards: no rewards in tier: %s' % (rewardTier))
    #     return []

    # Since the rewardTier is in order, just grab the first ones
    # remaining in the list, up to numChoices of them
    rewardPool = rewardTier[:numChoices]

    # Fill in the space remaining in reward pool with optional rewards
    # Fill in up to 2 times numChoices options to pick from
    for i in range(len(rewardPool), numChoices*2):
        if optRewards:
            optionalReward = seededRandomChoice(optRewards)
            optRewards.remove(optionalReward)
            rewardPool.append(optionalReward)
        else:
            break
    if notify.getDebug():
        notify.debug('getNextRewards: starting reward pool: %s' % (rewardPool))

    # Any left?
    if len(rewardPool) == 0:
        if notify.getDebug():
            notify.debug('getNextRewards: no rewards left at all')
        return []
    
    # Automatically pick the first one so you will always be presented
    # with a required reward, plus some optional
    finalRewardPool = [rewardPool.pop(0)]

    # Then randomly pick the rest
    for i in range(numChoices-1):
        # Out of rewards
        if len(rewardPool) == 0:
            break
        selectedReward = seededRandomChoice(rewardPool)
        rewardPool.remove(selectedReward)
        finalRewardPool.append(selectedReward)

    if notify.getDebug():
        notify.debug('getNextRewards: final reward pool: %s' % (finalRewardPool))
    return finalRewardPool

    


RewardDict = {
    # Careful: some rewards are deltas, others are absolute

    # HP rewards are deltas from your current max hp
    # in other words if you have 15hp, and you get a +1 MaxHPReward
    # you will now have 15+1=16hp.
    100 : (MaxHpReward, 1),
    101 : (MaxHpReward, 2),
    102 : (MaxHpReward, 3),
    103 : (MaxHpReward, 4),
    104 : (MaxHpReward, 5),
    105 : (MaxHpReward, 6),
    106 : (MaxHpReward, 7),
    107 : (MaxHpReward, 8),
    108 : (MaxHpReward, 9),
    109 : (MaxHpReward, 10),

    # MaxGagCarryRewards are absolute values
    # If you currently carry 20 items, and you get a CarryReward of 25,
    # now you can carry 25, not 20+25.
    200 : (MaxGagCarryReward, 25, TTLocalizer.QuestsMediumPouch),
    201 : (MaxGagCarryReward, 30, TTLocalizer.QuestsLargePouch),
    202 : (MaxGagCarryReward, 35, TTLocalizer.QuestsSmallBag),
    203 : (MaxGagCarryReward, 40, TTLocalizer.QuestsMediumBag),
    204 : (MaxGagCarryReward, 50, TTLocalizer.QuestsLargeBag),
    205 : (MaxGagCarryReward, 60, TTLocalizer.QuestsSmallBackpack),
    206 : (MaxGagCarryReward, 70, TTLocalizer.QuestsMediumBackpack),
    207 : (MaxGagCarryReward, 80, TTLocalizer.QuestsLargeBackpack),

    300 : (TeleportReward, ToontownGlobals.ToontownCentral),
    301 : (TeleportReward, ToontownGlobals.DonaldsDock),
    302 : (TeleportReward, ToontownGlobals.DaisyGardens),
    303 : (TeleportReward, ToontownGlobals.MinniesMelodyland),
    304 : (TeleportReward, ToontownGlobals.TheBrrrgh),
    305 : (TeleportReward, ToontownGlobals.DonaldsDreamland),

    # Dummy stand in reward
    400 : (TrackTrainingReward, None),
    # Real track access rewards - these are used by the QuestManagerAI
    # to assign the track training reward once the track has been chosen
    # by the player. They are not listed in the RewardDict.
    401 : (TrackTrainingReward, ToontownBattleGlobals.HEAL_TRACK),    
    402 : (TrackTrainingReward, ToontownBattleGlobals.TRAP_TRACK),
    403 : (TrackTrainingReward, ToontownBattleGlobals.LURE_TRACK),
    404 : (TrackTrainingReward, ToontownBattleGlobals.SOUND_TRACK),
    405 : (TrackTrainingReward, ToontownBattleGlobals.THROW_TRACK),
    406 : (TrackTrainingReward, ToontownBattleGlobals.SQUIRT_TRACK),
    407 : (TrackTrainingReward, ToontownBattleGlobals.DROP_TRACK),

    # These are absolute values
    500 : (MaxQuestCarryReward, 2),
    501 : (MaxQuestCarryReward, 3),
    502 : (MaxQuestCarryReward, 4),

    # These are deltas
    600 : (MoneyReward, 10),
    601 : (MoneyReward, 20),
    602 : (MoneyReward, 40),
    603 : (MoneyReward, 60),
    604 : (MoneyReward, 100),
    605 : (MoneyReward, 150),
    606 : (MoneyReward, 200),
    607 : (MoneyReward, 250),
    608 : (MoneyReward, 300),
    609 : (MoneyReward, 400),
    610 : (MoneyReward, 500),
    611 : (MoneyReward, 600),    
    612 : (MoneyReward, 700),    
    613 : (MoneyReward, 800),    
    614 : (MoneyReward, 900),    
    615 : (MoneyReward, 1000),    
    616 : (MoneyReward, 1100),    
    617 : (MoneyReward, 1200),    
    618 : (MoneyReward, 1300),    
    619 : (MoneyReward, 1400),    
    620 : (MoneyReward, 1500),
    # Following added to accommodate CFO quests
    621 : (MoneyReward, 1750),
    622 : (MoneyReward, 2000),
    623 : (MoneyReward, 2500),    
    
    # These are absolute values
    700 : (MaxMoneyReward, 50),
    701 : (MaxMoneyReward, 60),
    702 : (MaxMoneyReward, 80),
    703 : (MaxMoneyReward, 100),
    704 : (MaxMoneyReward, 120),
    705 : (MaxMoneyReward, 150),
    706 : (MaxMoneyReward, 200),
    707 : (MaxMoneyReward, 250),

    801 : (TrackProgressReward, None, 1),
    802 : (TrackProgressReward, None, 2),
    803 : (TrackProgressReward, None, 3),
    804 : (TrackProgressReward, None, 4),
    805 : (TrackProgressReward, None, 5),
    806 : (TrackProgressReward, None, 6),
    807 : (TrackProgressReward, None, 7),
    808 : (TrackProgressReward, None, 8),
    809 : (TrackProgressReward, None, 9),
    810 : (TrackProgressReward, None, 10),
    811 : (TrackProgressReward, None, 11),
    812 : (TrackProgressReward, None, 12),
    813 : (TrackProgressReward, None, 13),
    814 : (TrackProgressReward, None, 14),
    815 : (TrackProgressReward, None, 15),
    
    110: (TIPClothingTicketReward,),
    1000: (ClothingTicketReward,),

    1001 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 1),
    1002 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 2),
    1003 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 3),
    1004 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 4),
    1005 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 5),
    1006 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 6),
    1007 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 7),
    1008 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 8),
    1009 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 9),
    1010 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 10),
    1011 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 11),
    1012 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 12),
    1013 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 13),
    1014 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 14),
    1015 : (TrackProgressReward, ToontownBattleGlobals.HEAL_TRACK, 15),

    1101 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 1),
    1102 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 2),
    1103 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 3),
    1104 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 4),
    1105 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 5),
    1106 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 6),
    1107 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 7),
    1108 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 8),
    1109 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 9),
    1110 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 10),
    1111 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 11),
    1112 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 12),
    1113 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 13),
    1114 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 14),
    1115 : (TrackProgressReward, ToontownBattleGlobals.TRAP_TRACK, 15),

    1201 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 1),
    1202 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 2),
    1203 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 3),
    1204 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 4),
    1205 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 5),
    1206 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 6),
    1207 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 7),
    1208 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 8),
    1209 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 9),
    1210 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 10),
    1211 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 11),
    1212 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 12),
    1213 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 13),
    1214 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 14),
    1215 : (TrackProgressReward, ToontownBattleGlobals.LURE_TRACK, 15),

    1301 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 1),
    1302 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 2),
    1303 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 3),
    1304 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 4),
    1305 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 5),
    1306 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 6),
    1307 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 7),
    1308 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 8),
    1309 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 9),
    1310 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 10),
    1311 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 11),
    1312 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 12),
    1313 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 13),
    1314 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 14),
    1315 : (TrackProgressReward, ToontownBattleGlobals.SOUND_TRACK, 15),

    # No throw or squirt since everybody starts with those

    1601 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 1),
    1602 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 2),
    1603 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 3),
    1604 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 4),
    1605 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 5),
    1606 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 6),
    1607 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 7),
    1608 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 8),
    1609 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 9),
    1610 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 10),
    1611 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 11),
    1612 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 12),
    1613 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 13),
    1614 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 14),
    1615 : (TrackProgressReward, ToontownBattleGlobals.DROP_TRACK, 15),

    # This completes the training for a track and assigns access to this track
    900 : (TrackCompleteReward, None),
    # Real track complete rewards - these are used by the QuestManagerAI
    # to assign the track access once the track has been trained completely.
    # They are not listed in the RewardDict.
    901 : (TrackCompleteReward, ToontownBattleGlobals.HEAL_TRACK),    
    902 : (TrackCompleteReward, ToontownBattleGlobals.TRAP_TRACK),
    903 : (TrackCompleteReward, ToontownBattleGlobals.LURE_TRACK),
    904 : (TrackCompleteReward, ToontownBattleGlobals.SOUND_TRACK),
    905 : (TrackCompleteReward, ToontownBattleGlobals.THROW_TRACK),
    906 : (TrackCompleteReward, ToontownBattleGlobals.SQUIRT_TRACK),
    907 : (TrackCompleteReward, ToontownBattleGlobals.DROP_TRACK),

    # Cheesy effect reward ID's are in the 2000 range.  The ID's are
    # based on 2000 + hoodId / 10 + effect.  Most cheesy effects are
    # not allowed in ToontownCentral, which is a generally sane land
    # and safe for newbies.  A particular HoodId means the effect will
    # only be observed while in that hood; a HoodId of 1 means any
    # hood except TTC, and a HoodId of 0 means any hood including TTC.

    # TT
    2205 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 2000, 10),
    2206 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 2000, 10),
    
    # DD
    2101 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1000, 10),
    2102 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1000, 10),
    2105 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 20),
    2106 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 20),

    # DG
    2501 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 5000, 60),
    2502 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 5000, 60),
    2503 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 5000, 20),
    2504 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 5000, 20),
    2505 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 60),
    2506 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 60),

    # MM
    2401 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 120),
    2402 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 120),
    2403 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 4000, 60),
    2404 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 4000, 60),
    2405 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 120),
    2406 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 120),
    2407 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 4000, 30),
    2408 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 4000, 30),
    2409 : (CheesyEffectReward, ToontownGlobals.CETransparent, 4000, 30),
    2410 : (CheesyEffectReward, ToontownGlobals.CENoColor, 4000, 30),

    # BR
    2301 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 360),
    2302 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 360),
    2303 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 360),
    2304 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 360),
    2305 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 1440),
    2306 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 1440),
    2307 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 3000, 240),
    2308 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 3000, 240),
    2309 : (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 120),
    2310 : (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 120),
    2311 : (CheesyEffectReward, ToontownGlobals.CEInvisible, 3000, 120),

    # DL, 24 hrs
    2900 : (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2901 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 1440),
    2902 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 1440),
    2903 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 1440),
    2904 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 1440),
    2905 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 1440),
    2906 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 1440),
    2907 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 1440),
    2908 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 1440),
    2909 : (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 1440),
    2910 : (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 1440),
    2911 : (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 1440),

    # DL+1, 2 days
    2920 : (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2921 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 2880),
    2922 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 2880),
    2923 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 2880),
    2924 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 2880),
    2925 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 2880),
    2926 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 2880),
    2927 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 2880),
    2928 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 2880),
    2929 : (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 2880),
    2930 : (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 2880),
    2931 : (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 2880),

    # DL+2, 7 days
    2940 : (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2941 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 10080),
    2942 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 10080),
    2943 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 10080),
    2944 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 10080),
    2945 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 10080),
    2946 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 10080),
    2947 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 10080),
    2948 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 10080),
    2949 : (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 10080),
    2950 : (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 10080),
    2951 : (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 10080),

    # DL+3, 30 days
    2960 : (CheesyEffectReward, ToontownGlobals.CENormal, 0, 0),
    2961 : (CheesyEffectReward, ToontownGlobals.CEBigHead, 1, 43200),
    2962 : (CheesyEffectReward, ToontownGlobals.CESmallHead, 1, 43200),
    2963 : (CheesyEffectReward, ToontownGlobals.CEBigLegs, 1, 43200),
    2964 : (CheesyEffectReward, ToontownGlobals.CESmallLegs, 1, 43200),
    2965 : (CheesyEffectReward, ToontownGlobals.CEBigToon, 0, 43200),
    2966 : (CheesyEffectReward, ToontownGlobals.CESmallToon, 0, 43200),
    2967 : (CheesyEffectReward, ToontownGlobals.CEFlatPortrait, 1, 43200),
    2968 : (CheesyEffectReward, ToontownGlobals.CEFlatProfile, 1, 43200),
    2969 : (CheesyEffectReward, ToontownGlobals.CETransparent, 1, 43200),
    2970 : (CheesyEffectReward, ToontownGlobals.CENoColor, 1, 43200),
    2971 : (CheesyEffectReward, ToontownGlobals.CEInvisible, 1, 43200),

    # suit part rewards
    4000 : (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegUpper),
    4001 : (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegLower),
    4002 : (CogSuitPartReward, 'm', CogDisguiseGlobals.leftLegFoot),
    4003 : (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegUpper),
    4004 : (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegLower),
    4005 : (CogSuitPartReward, 'm', CogDisguiseGlobals.rightLegFoot),
    4006 : (CogSuitPartReward, 'm', CogDisguiseGlobals.upperTorso),
    4007 : (CogSuitPartReward, 'm', CogDisguiseGlobals.torsoPelvis),
    4008 : (CogSuitPartReward, 'm', CogDisguiseGlobals.leftArmUpper),
    4009 : (CogSuitPartReward, 'm', CogDisguiseGlobals.leftArmLower),
    4010 : (CogSuitPartReward, 'm', CogDisguiseGlobals.rightArmUpper),
    4011 : (CogSuitPartReward, 'm', CogDisguiseGlobals.rightArmLower),

    4100 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegUpper),
    4101 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegLower),
    4102 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftLegFoot),
    4103 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegUpper),
    4104 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegLower),
    4105 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightLegFoot),
    4106 : (CogSuitPartReward, 'l', CogDisguiseGlobals.upperTorso),
    4107 : (CogSuitPartReward, 'l', CogDisguiseGlobals.torsoPelvis),
    4108 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmUpper),
    4109 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmLower),
    4110 : (CogSuitPartReward, 'l', CogDisguiseGlobals.leftArmHand),
    4111 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmUpper),
    4112 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmLower),
    4113 : (CogSuitPartReward, 'l', CogDisguiseGlobals.rightArmHand),

    4200 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegUpper),
    4201 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegLower),
    4202 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftLegFoot),
    4203 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegUpper),
    4204 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegLower),
    4205 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightLegFoot),
    4206 : (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoLeftShoulder),
    4207 : (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoRightShoulder),
    4208 : (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoChest),
    4209 : (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoHealthMeter),
    4210 : (CogSuitPartReward, 'c', CogDisguiseGlobals.torsoPelvis),
    4211 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmUpper),
    4212 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmLower),
    4213 : (CogSuitPartReward, 'c', CogDisguiseGlobals.leftArmHand),
    4214 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmUpper),
    4215 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmLower),
    4216 : (CogSuitPartReward, 'c', CogDisguiseGlobals.rightArmHand),

    # if you add or remove any suit part rewards, update the ranges in
    # getAllRewardIdsForReward()

    }

def getNumTiers():
    return len(RequiredRewardTrackDict) - 1

def isLoopingFinalTier(tier):
    return (tier == LOOPING_FINAL_TIER)

def getRewardsInTier(tier):
    return RequiredRewardTrackDict.get(tier, [])

def getNumRewardsInTier(tier):
    return len(RequiredRewardTrackDict.get(tier, []))

def rewardTierExists(tier):
    return RequiredRewardTrackDict.has_key(tier)

def getOptionalRewardsInTier(tier):
    return OptionalRewardTrackDict.get(tier, [])


def getRewardIdFromTrackId(trackId):
    # Given this trackId, return the rewardId for this TrackTrainingReward
    # Since the TrackTrainingRewards start at 401, just add the trackId to it
    return 401 + trackId

# This is the list of required rewards
RequiredRewardTrackDict = {
    # Tier: [reward list in order]
    # Note: We need enough maxHp reward to get from 15 to 100 exactly
    #       Fishing adds an additional 5 HP outside of the quest system
    # Note: Track choices go in their own tier so that the track progress rewards
    #       on the subsequent tier go towards a track we have chosen
    # Note: Because fishing gives out 5 HP, the numbers below are minimums,
    #       the actual Toon's HP could be up to 5 HP more

    # 15 HP
    TT_TIER    : (100,),
    # 16 HP
    TT_TIER+1  : (400,),
    # 16 HP
    TT_TIER+2  : (100,801,200,802,803,101,804,805,102,806,807,100,808,809,101,810,811,500,812,813,700,814,815,300),
    # 25 HP
    TT_TIER+3  : (900,),
    # 25 HP

    DD_TIER    : (400,),
    # 25 HP
    DD_TIER+1  : (100,801,802,201,803,804,101,805,806,102,807,808,100,809,810,101,811,812,701,813,814,815,301),
    # 34 HP
    DD_TIER+2  : (900,),
    # 34 HP

    DG_TIER    : (100,202,101,102,100,101,501,702,302),
    # 43 HP

    MM_TIER    : (400,),
    # 43 HP
    MM_TIER+1  : (100,801,802,203,803,804,101,805,806,102,807,808,100,809,810,101,811,812,703,813,814,815,303),
    # 52 HP
    MM_TIER+2  : (900,),
    # 52 HP

    BR_TIER    : (400,),
    # 52 HP
    BR_TIER+1  : (100,801,802,704,803,804,101,805,806,502,807,808,102,809,810,204,811,812,100,813,814,101,815,304),
    # 61 HP
    BR_TIER+2  : (900,),
    # 61 HP

    # Note: Added first few pieces of Cashbot Cog Suit to DL Tier
    # Note: Added remainder of Cashbot Cog Suit to DL+1-+3, 
    #       redistributed some of the others to even out the tiers a bit
    DL_TIER    : (4000,100,205,101,102,705,103,305,4001,4002),
    # 71 HP
    DL_TIER+1  : (100,206,101,4003,4004,4005,102,4006,4007,4008,706,103,4009,4010,4011,4000,4001,4002),
    # 81 HP
    DL_TIER+2  : (4006,4007,4008,100,4000,4001,4002,4003,101,4004,4005,4009,102,103,4010,4011),
    # 91 HP
    DL_TIER+3  : (4009,4010,4011,100,4000,4001,101,4002,4003,102,4004,4005,102,4006,4007,707,207,4008),
    # 100 HP

    # I'm not sure why these were done as separate teirs - so the rewards could be strictly sequential?
    
    # Lawbot cog suit parts
    LAWBOT_HQ_TIER : (4100,),
    LAWBOT_HQ_TIER+1 : (4101,),
    LAWBOT_HQ_TIER+2 : (4102,),
    LAWBOT_HQ_TIER+3 : (4103,),
    LAWBOT_HQ_TIER+4 : (4104,),
    LAWBOT_HQ_TIER+5 : (4105,),
    LAWBOT_HQ_TIER+6 : (4106,),
    LAWBOT_HQ_TIER+7 : (4107,),
    LAWBOT_HQ_TIER+8 : (4108,),
    LAWBOT_HQ_TIER+9 : (4109,),
    LAWBOT_HQ_TIER+10 : (4110,),
    LAWBOT_HQ_TIER+11 : (4111,),
    LAWBOT_HQ_TIER+12 : (4112,),
    LAWBOT_HQ_TIER+13 : (4113,),

    # Bossbot cog suit parts
    BOSSBOT_HQ_TIER : (4200,),
    BOSSBOT_HQ_TIER+1 : (4201,),
    BOSSBOT_HQ_TIER+2 : (4202,),
    BOSSBOT_HQ_TIER+3 : (4203,),
    BOSSBOT_HQ_TIER+4 : (4204,),
    BOSSBOT_HQ_TIER+5 : (4205,),
    BOSSBOT_HQ_TIER+6 : (4206,),
    BOSSBOT_HQ_TIER+7 : (4207,),
    BOSSBOT_HQ_TIER+8 : (4208,),
    BOSSBOT_HQ_TIER+9 : (4209,),
    BOSSBOT_HQ_TIER+10 : (4210,),
    BOSSBOT_HQ_TIER+11 : (4211,),
    BOSSBOT_HQ_TIER+12 : (4212,),
    BOSSBOT_HQ_TIER+13 : (4213,),
    BOSSBOT_HQ_TIER+14 : (4214,),
    BOSSBOT_HQ_TIER+15 : (4215,),
    BOSSBOT_HQ_TIER+16 : (4216,),

    # Note: Added all Cashbot Cog Suit parts to Elder Tier to ensure
    #       players past DL & DL+1 get the suit.
    ELDER_TIER : (4000,4001,4002,4003,4004,4005,4006,4007,4008,4009,4010,4011,
                   ),
    }

# This is the list of optional rewards
OptionalRewardTrackDict = {
    # Tier: [reward list in order]
    TT_TIER   : (),
    TT_TIER+1 : (),
    TT_TIER+2 : (1000, 601, 601, 602, 602, 2205, 2206, 2205, 2206),

    # we changed TT_TIER+3 to have optional rewards for trialers
    TT_TIER+3 :  (601, 601, 602, 602, 2205, 2206, 2205, 2206),

    DD_TIER   : (1000, 602, 602, 603, 603, 2101, 2102, 2105, 2106),
    DD_TIER+1 : (1000, 602, 602, 603, 603, 2101, 2102, 2105, 2106),
    DD_TIER+2 : (1000, 602, 602, 603, 603, 2101, 2102, 2105, 2106),

    DG_TIER   : (1000, 603, 603, 604, 604, 2501, 2502, 2503, 2504, 2505, 2506),

    MM_TIER   : (1000, 604, 604, 605, 605, 2403, 2404, 2405, 2406, 2407, 2408, 2409),
    MM_TIER+1 : (1000, 604, 604, 605, 605, 2403, 2404, 2405, 2406, 2407, 2408, 2409),
    MM_TIER+2 : (1000, 604, 604, 605, 605, 2403, 2404, 2405, 2406, 2407, 2408, 2409),

    BR_TIER   : (1000, 606, 606, 606, 606, 606, 607, 607, 607, 607, 607,
                 2305, 2306, 2307, 2308, 2309, 2310, 2311),
    BR_TIER+1 : (1000, 606, 606, 606, 606, 606, 607, 607, 607, 607, 607,
                 2305, 2306, 2307, 2308, 2309, 2310, 2311),
    BR_TIER+2 : (1000, 606, 606, 606, 606, 606, 607, 607, 607, 607, 607,
                 2305, 2306, 2307, 2308, 2309, 2310, 2311),
    
    DL_TIER   : (607, 607, 607, 607, 608, 608, 608, 608,
                 2901, 2902, 2907, 2908, 2909, 2910, 2911),
    DL_TIER+1 : (1000, 607, 607, 607, 607, 608, 608, 608, 608,
                 2923, 2924, 2927, 2928, 2929, 2930, 2931),
    DL_TIER+2 : (608, 608, 608, 608, 609, 609, 609, 609,
                 2941, 2942, 2943, 2944, 2947, 2948, 2949, 2950, 2951),
    DL_TIER+3 : (1000, 609, 609, 609, 609, 609, 609,
                 2961, 2962, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971),

    # Heavier on clothing quests and jellybeans
    ELDER_TIER : (1000, 1000,
                  610, 611, 612, 613, 614, 615, 616, 617, 618,
                  2961, 2962, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971),
    }

def isRewardOptional(tier, rewardId):
    return ((OptionalRewardTrackDict.has_key(tier)) and
            (rewardId in OptionalRewardTrackDict[tier]))

def getItemName(itemId):
    """
    Return the singular name of this itemId
    """
    return ItemDict[itemId][0]

def getPluralItemName(itemId):
    """
    Return the plural name of this itemId
    """
    return ItemDict[itemId][1]

def avatarHasTrolleyQuest(av):
    """return true if avatar has trolley quest"""
    return ((len(av.quests) == 1) and
            (av.quests[0][0] == TROLLEY_QUEST_ID))

def avatarHasCompletedTrolleyQuest(av):
    """return true if avatar has completed trolley quest;
    only call if avatar has the trolley quest"""
    assert avatarHasTrolleyQuest(av)
    return av.quests[0][4] > 0

def avatarHasFirstCogQuest(av):
    """return true if avatar has first cog defeat quest"""
    return ((len(av.quests) == 1) and
            (av.quests[0][0] == FIRST_COG_QUEST_ID))

def avatarHasCompletedFirstCogQuest(av):
    """return true if avatar has completed first cog defeat quest;
    only call if avatar has the first cog quest"""
    assert avatarHasFirstCogQuest(av)
    return av.quests[0][4] > 0

def avatarHasFriendQuest(av):
    """return true if avatar has make a friend quest"""
    return ((len(av.quests) == 1) and
            (av.quests[0][0] == FRIEND_QUEST_ID))

def avatarHasCompletedFriendQuest(av):
    """return true if avatar has completed make a friend quest;
    only call if avatar has the friend quest"""
    assert avatarHasFriendQuest(av)
    return av.quests[0][4] > 0

def avatarHasPhoneQuest(av):
    """return true if avatar has trolley quest"""
    return ((len(av.quests) == 1) and
            (av.quests[0][0] == PHONE_QUEST_ID))

def avatarHasCompletedPhoneQuest(av):
    """return true if avatar has completed trolley quest;
    only call if avatar has the trolley quest"""
    assert avatarHasPhoneQuest(av)
    return av.quests[0][4] > 0

def avatarWorkingOnRequiredRewards(av):
    """
    Return 1 is this avatar is working on any required rewards
    for this tier. 0 otherwise.
    """
    tier = av.getRewardTier()
    # Get a copy of the rewards in this tier
    rewardList = list(getRewardsInTier(tier))

    # Transform rewards
    for i in range(len(rewardList)):
        actualRewardId = transformReward(rewardList[i], av)
        rewardList[i] = actualRewardId

    # Now see if we are working on any
    # Iterate though our rewards and see if they are in the rewardList
    for questDesc in av.quests:
        questId = questDesc[0]
        rewardId = questDesc[3]
        if rewardId in rewardList:
            return 1
        # If this is part of a multipart, our rewardId might be NA
        # If it is, get the final reward id and check that
        elif rewardId == NA:
            rewardId = transformReward(getFinalRewardId(questId, fAll=1), av)
            if rewardId in rewardList:
                return 1
    return 0

def avatarHasAllRequiredRewards(av, tier):
    """
    Return 1 is this avatar has all the required rewards in his history
    for this tier. 0 otherwise.
    """
    
    # See what rewards we have worked on.
    # NOTE: list() gives us a copy of the reward history so
    # we can play with it without damaging the original.
    rewardHistory = list(av.getRewardHistory()[1])
    # See what rewards we should have for this tier
    rewardList = getRewardsInTier(tier)
    notify.debug("checking avatarHasAllRequiredRewards: history: %s, tier: %s" %
                 (rewardHistory, rewardList))
    for rewardId in rewardList:
        if (rewardId == 900):
            # The 900 reward is changed to one of 901-907 when we know what track they choose
            # Make sure they have one of the following rewards:
            found = 0
            for actualRewardId in (901,902,903,904,905,906,907):
                if actualRewardId in rewardHistory:
                    found = 1
                    rewardHistory.remove(actualRewardId)
                    if notify.getDebug():
                        notify.debug("avatarHasAllRequiredRewards: rewardId 900 found as: %s" %
                                     (actualRewardId))
                    break
            if not found:
                if notify.getDebug():
                    notify.debug("avatarHasAllRequiredRewards: rewardId 900 not found")
                return 0
        else:
            # Track training rewards are replaced, so check the replacement values
            actualRewardId = transformReward(rewardId, av)
            # Now see if the avatar has this reward
            if actualRewardId in rewardHistory:
                # Take it out so we do not count it twice
                rewardHistory.remove(actualRewardId)
            # If this reward is a CogSuitPart, see if the avatar already has
            # the reward and if so, count it as done.
            elif (getRewardClass(rewardId) == CogSuitPartReward):
                deptStr = RewardDict.get(rewardId)[1]
                cogPart = RewardDict.get(rewardId)[2]
                dept = ToontownGlobals.cogDept2index[deptStr]
                if av.hasCogPart(cogPart, dept):
                    if notify.getDebug():
                        notify.debug("avatarHasAllRequiredRewards: rewardId: %s counts, avatar has cog part: %s dept: %s" %
                                     (actualRewardId, cogPart, dept))
                    # Count this as done, since the avatar already has the reward
                    # We do not remove it from the rewardHistory because it is not there
                    # This avatar skipped this quest altogether because they already had
                    # the cog part.
                else:
                    # We can safely bail out here because if you are missing
                    # any single required reward, the answer is 0 - no you are not done
                    if notify.getDebug():
                        notify.debug("avatarHasAllRequiredRewards: CogSuitPartReward: %s not found" %
                                     (actualRewardId))
                    return 0
            else:
                # We can safely bail out here because if you are missing
                # any single required reward, the answer is 0 - no you are not done
                if notify.getDebug():
                    notify.debug("avatarHasAllRequiredRewards: rewardId %s not found" %
                                 (actualRewardId))
                return 0

    if notify.getDebug():
        # All remaining rewards in the list should be optional, let's check.
        # Only do this in debug mode
        notify.debug("avatarHasAllRequiredRewards: remaining rewards: %s" %
                     (rewardHistory))
        for rewardId in rewardHistory:
            if not isRewardOptional(tier, rewardId):
                notify.warning("required reward found, expected only optional: %s" %
                               (rewardId))
        
    # If you made it here, you must have all rewards in your history.
    return 1

def nextQuestList(nextQuest):
    """ given a 'nextQuest' field from a quest,
    returns None or a list of quest ids """
    if nextQuest == NA:
        return None
    seqTypes = (types.ListType, types.TupleType)
    if type(nextQuest) in seqTypes:
        return nextQuest
    else:
        return (nextQuest,)

def checkReward(questId, forked=0):
    """
    for a given quest, check that all paths lead to a reward, and
    that it's the same reward
    'forked' is for internal use, do not override
    """
    #print "checkReward: %s" % questId
    quest = QuestDict[questId]
    reward = quest[5]
    nextQuests = nextQuestList(quest[6])
    if nextQuests is None:
        # this is the end of a quest chain
        assert reward != NA, "end-of-chain quest %s ends with no reward" % questId
        validRewards = RewardDict.keys() + [Any,AnyCashbotSuitPart,AnyLawbotSuitPart,OBSOLETE]
        assert reward in validRewards, "quest %s: unknown reward %s" % (questId, reward)
        if reward is OBSOLETE:
            # this quest is obsolete; notify
            print "warning: quest %s is obsolete" % questId
        return reward
    else:
        # internal quests currently cannot give out rewards
        assert reward is NA, "internal chain quest %s has a reward (%s)" % (questId, reward)
        forked = forked or len(nextQuests) > 1
        firstReward = checkReward(nextQuests[0], forked)
        #print "firstReward: %s" % firstReward
        for qId in nextQuests[1:]:
            thisReward = checkReward(qId, forked)
            #print "thisReward: %s (%s)" % (thisReward, firstReward)
            assert thisReward == firstReward, "quest %s leads to different rewards through chained quests %s(%s) and %s(%s)" % (questId, nextQuests[0], firstReward, qId, thisReward)
        return firstReward

def assertAllQuestsValid():
    print "checking quests..."
    # create one of each quest, to give the assertions a chance
    # to complain
    for questId in QuestDict.keys():
        try:
            quest = getQuest(questId)
        except AssertionError, e:
            err = "invalid quest: %s" % questId
            print err; raise
            # this hides the stack trace
            #raise AssertionError, err

    # check multi-part quests
    for questId in QuestDict.keys():
        quest = QuestDict[questId]
        (tier, start, questDesc, fromNpc,
         toNpc, reward, nextQuest, dialog) = quest

        # NOTE: this rule was bent to fix the problem where
        # you could just sidestep a long difficult quest chain by
        # going to the NPC you were supposed to visit to be offered
        # a different quest. Now the first visit quest and the next
        # are both starting quests so when you walk up to the NPC
        # you are supposed to visit, he will just pick up with the
        # second quest in the chain.
        # -- Joe
        # nextQuests = nextQuestList(nextQuest)
        # if nextQuests is not None:
        #     for qId in nextQuests:
        #         qStart = QuestDict[qId][1]
        #         assert not qStart, 'quest %s chained to start quest %s' % (questId, qId)

        # is this the start of a quest chain?
        if start:
            # check the end reward(s)
            checkReward(questId)

