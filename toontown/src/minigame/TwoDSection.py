"""TwoDSection module: contains the TwoDSection class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDBlock
from toontown.minigame import TwoDEnemyMgr
from toontown.minigame import TwoDTreasureMgr
from toontown.minigame import TwoDSpawnPointMgr
from toontown.minigame import TwoDStomperMgr

class TwoDSection(DirectObject):
    """
    TwoDSection represents a section of the game.
    Several TwoDSection s make up the level and all of them controlled by a TwoDSectionMgr.
    Each TwoDSection has one TwoDEnemyMgr, TwoDTreasureMgr, TwoDSpawnPointMgr and a list of blocks.
    
    Each section, during creation, has:
    1) index : index of the order of sections in the game
    2) name : name by which we can identify the section from ToonBlitzGlobals
    3) difficulty : difficulty level of the section
    4) length : length of the section
    5) maxEnemies : maximum number of enemies in the section
    6) maxTreasures : maximum number of treasures in the section
    7) maxSavePoints : maximum number of save points in the section
    8) avgTimeReqd (optional) : average time (in seconds) required to complete the section
    
    This class should take care that the first block starts at (0, 0, 12) and the 
    last block starts at (length, 0, 12). Then remove the last block because the 
    last block is at the same place as the first block of the next section.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDSection')
    
    def __init__(self, indexNum, sectionInfo, sectionNP, sectionMgr):
        self.indexNum = indexNum
        self.sectionNP = sectionNP
        self.sectionMgr = sectionMgr
        
        self.blocks = [] # List of all block objects
        
        self.load(sectionInfo)
    
    def destroy(self):        
        for block in self.blocks:
            block.destroy()
        
        self.enemyMgr.destroy()
        del self.enemyMgr
        
        self.treasureMgr.destroy()
        del self.treasureMgr
        
        self.spawnPointMgr.destroy()
        del self.spawnPointMgr
        
        self.stomperMgr.destroy()
        del self.stomperMgr
        
        self.sectionMgr = None
        self.sectionNP = None
        self.blockList = []
        self.enemyList = []
        self.treasureList = []
        self.spawnPointList = []
    
    def load(self, sectionInfo):
        self.sectionTypeNum = sectionInfo[0]
        enemyIndicesSelected = sectionInfo[1]
        treasureIndicesSelected = sectionInfo[2]
        spawnPointIndicesSelected = sectionInfo[3]
        stomperIndicesSelected = sectionInfo[4]
        
        attribs = ToonBlitzGlobals.SectionTypes[self.sectionTypeNum]
        self.length = attribs[1]
        self.blockList = attribs[2] # The list of all the block attribs        
        enemiesPool = attribs[3] # The list of all the enemy attribs
        treasuresPool = attribs[4] # The list of all the treasure attribs
        spawnPointsPool = attribs[5] # The list of all the spawn point attribs
        stompersPool = attribs[6] # The list of all the stomper attribs
        
        self.enemyList = []
        for enemyIndex in enemyIndicesSelected:
            self.enemyList.append(enemiesPool[enemyIndex])
        self.treasureList = []
        for treasure in treasureIndicesSelected:
            treasureIndex = treasure[0]
            treasureValue = treasure[1]
            treasureAttribs = treasuresPool[treasureIndex]
            self.treasureList.append((treasureAttribs, treasureValue))
        self.spawnPointList = []
        for spawnPointIndex in spawnPointIndicesSelected:
            self.spawnPointList.append(spawnPointsPool[spawnPointIndex])
        self.stomperList = []
        for stomperIndex in stomperIndicesSelected:
            self.stomperList.append(stompersPool[stomperIndex])
        
        self.blocksNP = NodePath('Blocks')
        self.blocksNP.reparentTo(self.sectionNP)
        
        # Validating whether the first block is in the correct place
        if (self.blockList[0][1][0] != (0, 0, 12)):
            self.notify.warning('First block of section %s does not start at (0, 0, 12)' %self.sectionTypeNum)
        
        # Creating level blocks        
        for index in range(0, len(self.blockList)):
            blockAttribs = self.blockList[index]
            fileName = ToonBlitzGlobals.BlockTypes[blockAttribs[0]][0]
            blockIndex = int(fileName[-1])
            blockType = self.sectionMgr.game.assetMgr.blockTypes[blockIndex]
            sectionizedId = self.getSectionizedId(index)
            newBlock = TwoDBlock.TwoDBlock(blockType, sectionizedId, blockAttribs)
            newBlock.model.reparentTo(self.blocksNP)
            self.blocks.append(newBlock)
        
        
        self.enemyMgr = TwoDEnemyMgr.TwoDEnemyMgr(self, self.enemyList)
        self.treasureMgr = TwoDTreasureMgr.TwoDTreasureMgr(self, self.treasureList, self.enemyList)
        self.spawnPointMgr = TwoDSpawnPointMgr.TwoDSpawnPointMgr(self, self.spawnPointList)
        self.stomperMgr = TwoDStomperMgr.TwoDStomperMgr(self, self.stomperList)
        
        if (self.sectionTypeNum == 'end'):
            self.spawnPointMgr.setupLastSavePointHandle()
    
    def enterPlay(self, elapsedTime):
        """ This function is called when the minigame enters the play state."""
        for block in self.blocks:
            block.start(elapsedTime)
        self.enemyMgr.enterPlay(elapsedTime)
        self.stomperMgr.enterPlay(elapsedTime)
    
    def exitPlay(self):
        """ This function will be called when the minigame exits the play state."""
        pass
    
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        for block in self.blocks:
            block.enterPause()
        self.enemyMgr.enterPause()
        self.stomperMgr.enterPause()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        for block in self.blocks:
            block.exitPause()
        self.enemyMgr.exitPause()
        self.stomperMgr.exitPause()
        
    def getSectionizedId(self, num):
        """ This method adds the sectionIndex with a '-' in front of the index provided and returns this string."""
        def getTwoDigitString(index):
            assert (index < 100) # Can't have more than 100 sections or enemies per section
            if (index < 10):
                output = '0' + str(index)
            else:
                output = str(index)
            return output
    
        return getTwoDigitString(self.indexNum) + '-' + getTwoDigitString(num)