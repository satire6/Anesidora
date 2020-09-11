from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
import DistributedToon
from direct.distributed import DistributedObject
import NPCToons
from toontown.quest import Quests
from direct.distributed import ClockDelta
from toontown.quest import QuestParser
from toontown.quest import QuestChoiceGui
from direct.interval.IntervalGlobal import *
import random 

class DistributedNPCToonBase(DistributedToon.DistributedToon):

    def __init__(self, cr):
        try:
            self.DistributedNPCToon_initialized
        except:
            self.DistributedNPCToon_initialized = 1
            DistributedToon.DistributedToon.__init__(self, cr)
            self.__initCollisions()
            # Not pickable
            self.setPickable(0)
            # These guys are specifically non-player characters.
            self.setPlayerType(NametagGroup.CCNonPlayer)
            
    def disable(self):
        # Ignore the sphere after the finish because
        # the end of the movie adds it in
        self.ignore("enter" + self.cSphereNode.getName())
        # Kill any quest choice guis that may be active
        # Kill any movies that may be playing 
        DistributedToon.DistributedToon.disable(self)

    def delete(self):
        try:
            self.DistributedNPCToon_deleted
        except:
            self.DistributedNPCToon_deleted = 1
            self.__deleteCollisions()
            DistributedToon.DistributedToon.delete(self)

    def generate(self):
        DistributedToon.DistributedToon.generate(self)
        # We cannot get a unique name until we have been generated
        self.cSphereNode.setName(self.uniqueName('NPCToon'))
        self.detectAvatars()
        # Since we know where the NPC will be standing, we can
        # immediately parent him to render.  This initializes the
        # nametag, etc.
        self.setParent(ToontownGlobals.SPRender)
        self.startLookAround()

    def generateToon(self):
        """generateToon(self)
        Create a toon from dna (an array of strings)
        NOTE: DistributedNPCToon overrides this because they do not
        need all this extra junk
        """
        # set up LOD info
        self.setLODs()
        # load the toon legs
        self.generateToonLegs()
        # load the toon head
        self.generateToonHead()
        # load the toon torso
        self.generateToonTorso()
        # color the toon as specified by the dna
        self.generateToonColor()
        self.parentToonParts()
        # Make small toons with big heads
        self.rescaleToon()
        self.resetHeight()

        # Initialize arrays of pointers to useful nodes for the toon
        self.rightHands = []
        self.leftHands = []
        self.headParts = []
        self.hipsParts = []
        self.torsoParts = []
        self.legsParts = []
        self.__bookActors = []
        self.__holeActors = []

    def announceGenerate(self):
        # This method is called after all the required fields have
        # been filled in.  In particular, the DNA will have been set,
        # so we can safely set an animation state.
        self.initToonState()     # This may be overidden by derived classes
        
        DistributedToon.DistributedToon.announceGenerate(self)
        
    def initToonState(self):
        # We'll make all NPC toons loop their neutral cycle by
        # default.  Normally this is sent from the AI, but because the
        # server sometimes loses updates that immediately follow the
        # generate, we might lose that message.
        self.setAnimState("neutral", 0.9, None, None)
        
        # TODO: make this a node path collection
        npcOrigin = render.find("**/npc_origin_" + `self.posIndex`)
        
        # Now he's no longer parented to render, but no one minds.
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.initPos()
        else:
            self.notify.warning("announceGenerate: Could not find npc_origin_" + str(self.posIndex))     
        
    def initPos(self):
        self.clearMat()
        
    def wantsSmoothing(self):
        # This overrides a function from DistributedSmoothNode to
        # indicate that NPC's should not ever be smoothed, even though
        # they do inherit (indirectly) from DistributedSmoothNode.
        return 0

    def detectAvatars(self):
        """
        listen for the collision sphere enter event
        """
        self.accept("enter" + self.cSphereNode.getName(),
                    self.handleCollisionSphereEnter)

    def ignoreAvatars(self):
        """
        Do not listen for the enter coll sphere event.
        """
        self.ignore("enter" + self.cSphereNode.getName())

    def getCollSphereRadius(self):
        return 3.25

    def __initCollisions(self):
        self.cSphere = CollisionTube(0., 1., 0., 0., 1., 5., self.getCollSphereRadius())
        #self.cSphere = CollisionSphere(0., 1., 0., self.getCollSphereRadius())
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode("cSphereNode")
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def __deleteCollisions(self):
        del self.cSphere
        del self.cSphereNode
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath

    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.warning("Don't call me - I'm a base class!")
        # Tell the server
        # self.sendUpdate("avatarEnter", [])

    def setupAvatars(self, av):
        """
        Prepare avatars for the quest movie
        """
        # Ignore avatars now to prevent unnecessary requestInteractions when we know
        # this npc is busy right now. If another toon did manage to request interaction
        # before we starting ignoring, he will get a freeAvatar message from the server
        self.ignoreAvatars()
        # Make us face each other
        # TODO: make this a lerp
        av.headsUp(self, 0, 0, 0)
        self.headsUp(av, 0, 0, 0)
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        # In case the avatar jumped up to interact with us, set his Z back down to our Z
        # This has issues... so I will not enable it just yet
        # We need to clear out the inertia and prevent double enters on the NPC sphere
        # av.setZ(render, self.getZ(render))
        # av.setShadowHeight(0)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def b_setPageNumber(self, paragraph, pageNumber):
        self.setPageNumber(paragraph, pageNumber)
        self.d_setPageNumber(paragraph, pageNumber)

    def d_setPageNumber(self, paragraph, pageNumber):
        timestamp = ClockDelta.globalClockDelta.getFrameNetworkTime()
        self.sendUpdate("setPageNumber", [paragraph, pageNumber, timestamp])
        
    def freeAvatar(self):
        """
        This is a message from the AI used to free the avatar from movie mode
        """
        base.localAvatar.posCamera(0,0)
        base.cr.playGame.getPlace().setState("walk")

    def setPositionIndex(self, posIndex):
        """
        This required field sets the NPC's position index.
        Each zone has N NPCs, and N corresponding NPC origins in the model.
        """
        self.posIndex = posIndex
    
