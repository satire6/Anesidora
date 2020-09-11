"""TwoDSectionMgr module: contains the TwoDSectionMgr class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDSection
from toontown.minigame import TwoDSpawnPointMgr
from toontown.minigame import TwoDBlock
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

class TwoDSectionMgr(DirectObject):
    """
    There is only one TwoDSectionMgr in the game.
    This class manages all the sections in the game, and places them correctly 
    in the world.
    It places the 1st section at (0, 0, 0) and the next section at (length, 0, 0),
    length being the length of the previous section.
    
    It queries the spawnPointMgrs of all the sections to find out where the player is.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDSectionMgr')
    
    def __init__(self, game, sectionsSelected):
        self.game = game
        
        self.sectionsPool = []
        self.sectionsSelected = []
        self.sections = []
        self.sectionNPList = []
        self.activeSection = 0
        
        self.setupStartSection()
        self.setupSections(sectionsSelected)
        self.setupEndSection(len(sectionsSelected))
    
    def destroy(self):        
        while len(self.sections):
            section = self.sections[0]
            section.destroy()
            self.sections.remove(section)
        self.sections = []
        
        self.sectionsPool = []
        self.sectionsSelected = []
        self.sectionNPList = []
        
        self.startWall.removeNode()
        del self.startWall
        
        self.startPipe.removeNode()
        del self.startPipe
        
        self.startArrow.removeNode()
        del self.startArrow
        
        self.endArrow.removeNode()
        del self.endArrow
        
        self.game = None
        self.activeSection = 0
        
    def setupStartSection(self):
        self.startSectionNP = NodePath('StartSection')
        self.startSectionNP.reparentTo(self.game.assetMgr.world)
        self.startSectionNP.setX(-48)
        # Creating the wall
        self.startWall = self.game.assetMgr.startingWall.copyTo(self.startSectionNP)
        self.startWall.setPos(-28, 0, 4)
        self.startWall.setScale(0.8)
        # Creating the pipe
        self.startPipe = self.game.assetMgr.startingPipe.copyTo(self.startSectionNP)
        self.startPipe.setPos(12, 0, 44)
        # Creating the arrow
        self.startArrow = self.game.assetMgr.arrow.copyTo(self.startSectionNP)
        self.startArrow.setPos(23, 1.5, 12.76)
        # Creating level blocks        
        # We don't create a section for the start section. It does not have a spawnPoint
        # TODO: We could make it a section, dunno if it'll break.
        for index in xrange(len(ToonBlitzGlobals.BlockListStart)):
            blockAttribs = ToonBlitzGlobals.BlockListStart[index]
            fileName = ToonBlitzGlobals.BlockTypes[blockAttribs[0]][0]
            blockIndex = int(fileName[-1])
            blockType = self.game.assetMgr.blockTypes[blockIndex]
            sectionizedId = 'start-' + str(index)
            newBlock = TwoDBlock.TwoDBlock(blockType, sectionizedId, blockAttribs)
            newBlock.model.reparentTo(self.startSectionNP)
            
    def setupEndSection(self, index):
        # Used to compensate for scaling of Cog tunnel sign's
        # original aspect ratio of 1125x813 to a uniform ratio,
        # scale z by factor of 0.7227
        aspectSF = 0.7227
        self.endSectionNP = NodePath('EndSection')
        self.endSectionNP.reparentTo(self.game.assetMgr.world)
        self.endSectionNP.setX(self.incrementX)
        
        # Creating the wall
        self.endWall = self.game.assetMgr.startingWall.copyTo(self.endSectionNP)
        self.endWall.setPos(100, 0, 4)
        self.endWall.setScale(0.8)
        # Creating the arrow
        self.endArrow = self.game.assetMgr.arrow.copyTo(self.endSectionNP)
        self.endArrow.setPos(6, 1.5, 12.76)
        # Creating the exitElevator
        self.exitElevator = self.game.assetMgr.exitElevator.copyTo(self.endSectionNP)
        self.exitElevator.setPos(52, -2, 12.7)
        # Elevator EXIT sign
        cogSignModel = loader.loadModel('phase_4/models/props/sign_sellBotHeadHQ')
        cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
        cogSignSF = 23
        elevatorSignSF = 15
        sideDoor = self.exitElevator.find('**/doorway2')
        sdSign = cogSign.copyTo(sideDoor)
        sdSign.setPosHprScale(0, 1.9, 15, 0, 0, 0,
            elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
        sdSign.node().setEffect(DecalEffect.make())
        sdText = DirectGui.OnscreenText(
            text = TTLocalizer.TwoDGameElevatorExit,
            font = ToontownGlobals.getSuitFont(),
            pos = (0,-0.34), scale = 0.15,
            # required for DecalEffect (must be a GeomNode, not a TextNode)
            mayChange=False,
            parent = sdSign)
        sdText.setDepthWrite(0)
        
        # We create a section for the end section because it has a spawnPoint.
        # Creating a section makes it easier to handle that without repeating code.
        self.sectionNPList.append(self.endSectionNP)
        # Emulating the info what setupSections() in DistributedTwoDGameAI would have sent. 
        endSectionInfo = ('end', [], [], [0], [])
        endSection = TwoDSection.TwoDSection(index, endSectionInfo, self.endSectionNP, self)
        self.sections.append(endSection)
        self.incrementX += endSection.length
    
    def setupSections(self, sectionsSelected):
        # sectionsSelected is a list of tuples sent from the AI. [(), ()]
        # Each tuple represents one section.
        # Tuple Format: (sectionIndex, [list of enemyIndices], [list of treasureIndices], [list of spawnPointIndices])
        # The tuples are in the order we want made and we make self.sections from sectionsSelected on a one-to-one basis
##        self.incrementX = 0
        # Start the 1st section from -24
        self.incrementX = -24
        for index in range(0, len(sectionsSelected)):            
            sectionNP = NodePath('Section' + str(index))
            sectionNP.reparentTo(self.game.assetMgr.world)
            sectionNP.setX(self.incrementX)
            self.sectionNPList.append(sectionNP)
        
            section = TwoDSection.TwoDSection(index, sectionsSelected[index], sectionNP, self)
            self.sections.append(section)
            self.incrementX += section.length
            
    def enterPlay(self, elapsedTime):
        """ This function is called when the minigame enters the play state."""
        for section in self.sections:
            section.enterPlay(elapsedTime)
    
    def exitPlay(self):
        """ This function will be called when the minigame exits the play state."""
        pass
    
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        for section in self.sections:
            section.enterPause()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        for section in self.sections:
            section.exitPause()
            
    def updateActiveSection(self, sectionIndex):
        """ This method is called by the SpawnPointMgr of the section the localAvatar is in."""
        if (self.activeSection != sectionIndex):
            self.activeSection = sectionIndex
            self.notify.debug('Toon is in section %s.' %sectionIndex)
            
    def getLastSpawnPoint(self):
        relativePoint = Point3(self.sections[self.activeSection].spawnPointMgr.getSpawnPoint())
        relativePoint.setX(relativePoint.getX() + self.sectionNPList[self.activeSection].getX())
        return relativePoint
