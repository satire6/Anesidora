"""TwoDTreasureMgr module: contains the TwoDTreasureMgr class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDTreasure
import random

class TwoDTreasureMgr(DirectObject):
    """
    Each section has one TwoDTreasureMgr, which controls all the treasures of that section.    
    All the positions are got from ToonBlitzGlobals.py.
    All treasures may or may not be used. It could randomly select x number of treasures
    from the entire list of treasures.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDTreasureMgr')
    
    def __init__(self, section, treasureList, enemyList):
        self.section = section
        self.treasureList = treasureList
        self.enemyList = enemyList
        self.load()
    
    def destroy(self):
        while len(self.treasures):
            treasure = self.treasures[0]
            treasure.destroy()
            self.treasures.remove(treasure)
        self.treasures = None
        self.section = None
        
    def load(self):
        if len(self.treasureList):
            self.treasuresNP = NodePath('Treasures')
            self.treasuresNP.reparentTo(self.section.sectionNP)
        
        # Creating treasuresNP
        self.treasures = []
        # Create the initial treasures from the treasure list 
        for index in xrange(len(self.treasureList)):
            treasureAttribs = self.treasureList[index][0]
            treasureValue = self.treasureList[index][1]
            self.createNewTreasure(treasureAttribs, treasureValue)
            
        # Create dummy treasures for each enemy in the enemy list
        self.enemyTreasures = []
        # The value of the enemy generated treasure increases when there are more players.
        numPlayers = self.section.sectionMgr.game.numPlayers
        pos = Point3(-1, -1, -1)
        for index in xrange(len(self.enemyList)):
            self.createNewTreasure([pos], numPlayers, isEnemyGenerated = True)
            
    def createNewTreasure(self, attrib, value, isEnemyGenerated = False, model = None):
        """ This method is called while creating treasures from the list and also when an enemy dies."""
        treasureId = self.section.getSectionizedId(len(self.treasures))
        if (model == None):
            model = self.getModel(value, self.section.sectionMgr.game.assetMgr.treasureModelList)
        newTreasure = TwoDTreasure.TwoDTreasure(self, treasureId, attrib[0], value, isEnemyGenerated, model)
        newTreasure.model.reparentTo(self.treasuresNP)
        self.treasures.append(newTreasure)
        if isEnemyGenerated:
            self.enemyTreasures.append(newTreasure)
    
    def getModel(self, value, modelList):
        # Changing value from 1 - 4 to 0 - 3
        value -= 1
        model = modelList[value]
        if (value == 0):
            # Model is a salesIcon
            model.setColor(1, 0.8, 0.8, 1)
        elif (value == 1):
            # Model is a moneyIcon
            model.setColor(0.8, 1, 0.8, 1)
        elif (value == 2):
            # Model is a legalIcon
            model.setColor(0.9, 0.9, 1, 1)
        elif (value == 3):
            # Model is a corpIcon
            model.setColor(1, 1, 0.6, 1)
        return model