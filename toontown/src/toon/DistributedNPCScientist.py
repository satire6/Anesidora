from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import DistributedNPCToonBase

class DistributedNPCScientist(DistributedNPCToonBase.DistributedNPCToonBase):

    def __init__(self, cr):
        assert self.notify.debug("__init__")
        DistributedNPCToonBase.DistributedNPCToonBase.__init__(self, cr)
            
    def getCollSphereRadius(self):
        return 2.5
        
    def initPos(self):
        #self.clearMat()
        self.setHpr(180, 0, 0)   
        self.setScale(1.0)
        
    def handleCollisionSphereEnter(self, collEntry):
        """
        Response for a toon walking up to this NPC
        """
        assert self.notify.debug("Entering collision sphere...")
        self.nametag3d.setDepthTest(0)
        self.nametag3d.setBin('fixed', 0)
                                                  
    def setChat(self, topic, partPos, partId, progress, flags):
        msg = TTLocalizer.toontownDialogues[topic][(partPos, partId)][progress]
        self.setChatMuted(msg, flags)
        
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
        
        self.setupToonNodes()
        if self.style.getTorsoSize() == "short" and self.style.getAnimal() == "duck":
            sillyReader = loader.loadModel("phase_4/models/props/tt_m_prp_acs_sillyReader")
            for rHand in self.getRightHands():
                placeholder = rHand.attachNewNode("SillyReader")
                sillyReader.instanceTo(placeholder)
                placeholder.setH(180)
                placeholder.setScale(render, 1.0)
                placeholder.setPos(0, 0, 0.1)
        elif (self.style.getTorsoSize() == "long" and self.style.getAnimal() == "monkey") or \
               (self.style.getTorsoSize() == "medium" and self.style.getAnimal() == "horse"):
            clipBoard = loader.loadModel("phase_4/models/props/tt_m_prp_acs_clipboard")
            for rHand in self.getRightHands():
                placeholder = rHand.attachNewNode("ClipBoard")
                clipBoard.instanceTo(placeholder)
                placeholder.setH(180)
                placeholder.setScale(render, 1.0)
                placeholder.setPos(0, 0, 0.1)
                
    def startLookAround(self):
        """
        Override this method from toonhead because we don't want our scientists looking at anything other 
        than what the animation specifies
        """
        pass 
        
    def scientistPlay(self):
        """
        During the scientist play animation
        the scientists lose their props
        """
        if self.style.getTorsoSize() == "short" and self.style.getAnimal() == "duck":
            sillyReaders = self.findAllMatches("**/SillyReader")
            for sillyReader in sillyReaders:
                if not sillyReader.isEmpty():
                    sillyReader.detachNode()
                sillyReader = None
        elif (self.style.getTorsoSize() == "long" and self.style.getAnimal() == "monkey"):
            clipBoards = self.findAllMatches("**/ClipBoard")
            #self.setHpr(250, 0, 0)
            for clipBoard in clipBoards:
                if not clipBoard.isEmpty():
                    clipBoard.detachNode()
                clipBoard = None