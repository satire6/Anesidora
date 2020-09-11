"""TwoDEnemyMgr module: contains the TwoDEnemyMgr class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDEnemy

class TwoDEnemyMgr(DirectObject):
    """
    Each section has one TwoDEnemyMgr, which controls all the enemies of that section.    
    All the positions are got from ToonBlitzGlobals.py
    All enemies may or may not be used. It could randomly select x number of enemies
    from the entire list of enemies.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDEnemyMgr')
    
    def __init__(self, section, enemyList):
        self.section = section
        self.enemyList = enemyList
        
        self.load()
    
    def destroy(self):
        self.section = None
        
        while len(self.enemies):
            enemy = self.enemies[0]
            enemy.destroy()
            self.enemies.remove(enemy)
        self.enemies = None
        
    def load(self):
        if len(self.enemyList):
            self.enemiesNP = NodePath('Enemies')
            self.enemiesNP.reparentTo(self.section.sectionNP)
        
        # Creating enemies
        self.enemies = []
        for index in xrange(len(self.enemyList)):
            enemyId = self.section.getSectionizedId(index)
            suitAttribs = self.enemyList[index]
            newEnemy = TwoDEnemy.TwoDEnemy(self, enemyId, suitAttribs)
            newEnemy.suit.reparentTo(self.enemiesNP)
            self.enemies.append(newEnemy)
    
    def enterPlay(self, elapsedTime):
        """ This function is called when the minigame enters the play state."""
        for enemy in self.enemies:
            enemy.start(elapsedTime)
    
    def exitPlay(self):
        """ This function will be called when the minigame exits the play state."""
        pass
    
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        for enemy in self.enemies:
            enemy.enterPause()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        for enemy in self.enemies:
            enemy.exitPause()