
from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
import DistributedToonAI
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.distributed import ClockDelta
from toontown.toonbase import ToontownGlobals
import NPCToons
from direct.task import Task
from toontown.quest import Quests

class DistributedNPCToonBaseAI(DistributedToonAI.DistributedToonAI):

    def __init__(self, air, npcId, questCallback=None):
        DistributedToonAI.DistributedToonAI.__init__(self, air)
        # Record the repository
        self.air = air
        self.npcId = npcId
        # busy will be replaced with the toon this npc is talking to
        self.busy = 0
        self.questCallback = questCallback
        # Does this NPC give out quests?
        self.givesQuests = 1

    def delete(self):
        taskMgr.remove(self.uniqueName("clearMovie"))
        DistributedToonAI.DistributedToonAI.delete(self)

    def _doPlayerEnter(self):
        pass

    def _doPlayerExit(self):
        pass

    def _announceArrival(self):
        # DistributedToonAI derives from DistributedPlayerAI, which sends
        # out 'arrivedOnDistrict' in announceGenerate. NPCs don't have
        # that field, so we override this func to do nothing.
        pass

    def isPlayerControlled(self):
        # TODO: we shouldn't derive from DistributedPlayerAI
        return False

    def getHq(self):
        """
        Override if you should be considered an HQ Toon
        """
        return 0

    def getTailor(self):
        """
        Override if you should be considered a Tailor
        """
        return 0

    def getGivesQuests(self):
        return self.givesQuests

    def avatarEnter(self):
        # Base class behavior
        pass

    def isBusy(self):
        return (self.busy > 0)

    def getNpcId(self):
        return self.npcId

    def freeAvatar(self, avId):
        # Free this avatar, probably because he requested interaction while
        # I was busy. This can happen when two avatars request interaction
        # at the same time. The AI will accept the first, sending a setMovie,
        # and free the second
        self.sendUpdateToAvatarId(avId, "freeAvatar", [])
        return

    def setPositionIndex(self, posIndex):
        self.posIndex = posIndex
        
    def getPositionIndex(self):
        return self.posIndex
    
