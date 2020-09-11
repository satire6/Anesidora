"""TwoDSpawnPointMgr module: contains the TwoDSpawnPointMgr class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.toonbase import ToontownGlobals

class TwoDSpawnPointMgr(DirectObject):
    """
    The TwoDSpawnPointMgr class controls all the save and spawn points
    for a 2D Scroller game.
    All the positions are got from ToonBlitzGlobals.py
    savePoint is the point at which the player's game is saved
    loadPoint is the point at which the player is loaded again, if he dies
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDSpawnPointMgr')
    
    def __init__(self, section, spawnPointList):
        self.section = section
        self.game = self.section.sectionMgr.game
        self.spawnPointList = spawnPointList
        
        self.lastSavePoint = 0
        self.showCollSpheres = False
        
        self.savePoints = []
        self.loadPoints = []
        self.collNPList = []
        self.collDict = {}
        
        self.load()
    
    def destroy(self):
        while len(self.collNPList):
            item = self.collNPList[0]
            self.ignore('enter' + self.collNPList[0].node().getName())
            self.collNPList.remove(item)
            item.removeNode()
        self.section = None
        self.game = None
        self.savePoints = None
        self.loadPoints = None
        self.collNPList = None
        self.collDict = None
    
    def load(self):
        if len(self.spawnPointList):
            self.spawnPointsNP = NodePath('SpawnPoints')
            self.spawnPointsNP.reparentTo(self.section.sectionNP)
        
        for point in self.spawnPointList:
            # The spawn point can either have 1 tuple, or 2, NOTHING ELSE!!
            assert(len(point) == 1 or len(point) == 2)
            if len(point) == 1:
                savePoint = point[0]
                loadPoint = point[0]
            else:
                savePoint = point[0]
                loadPoint = point[1]
            
            index = len(self.savePoints)
            self.savePoints.append(savePoint)
            self.loadPoints.append(loadPoint)
            self.setupCollision(index)
            
    def setupCollision(self, index):
        """ 
        Make a sphere, give it a unique name, and place it at the given location
        To create a unique name, we need to be a DistributedObject, so we create
        a unique name using the minigame's id (the class that instantiated me).
        """
        collSphere = CollisionSphere(0, 0, 0, 3)
        collSphereName = 'savePoint%s' %self.section.getSectionizedId(index)
        collSphere.setTangible(0)
        collNode = CollisionNode(self.game.uniqueName(collSphereName))        
        collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        collNode.addSolid(collSphere)
        collNodePath = self.spawnPointsNP.attachNewNode(collNode)
        collNodePath.hide()
        if self.showCollSpheres:
            collNodePath.show()
        
        # Set the position of the collision sphere
        posX, posY, posZ = self.savePoints[index]
        collNodePath.setPos(posX, posY, posZ)
        # Add it to a list for reference
        self.collNPList.append(collNodePath)
        # Maintain a dictionary mapping unique name to index
        self.collDict[collNodePath.getName()] = index
        # Add a hook looking for collisions with localToon
        self.accept(self.game.uniqueName('enter' + collSphereName), self.handleSavePointCollision)
        
    def handleSavePointCollision(self, cevent):
##        self.notify.debug('saved: %s' %cevent)
        savePointName = cevent.getIntoNodePath().getName()
        self.lastSavePoint = self.collDict[savePointName]
        self.section.sectionMgr.updateActiveSection(self.section.indexNum)
        
    def getSpawnPoint(self):
        if (len(self.loadPoints) > 0):
            point = self.loadPoints[self.lastSavePoint]
            return Point3(point[0], point[1], point[2])
        else:
            return Point3(ToonBlitzGlobals.ToonStartingPosition[0],
                          ToonBlitzGlobals.ToonStartingPosition[1],
                          ToonBlitzGlobals.ToonStartingPosition[2])
    
    def setupLastSavePointHandle(self):
        # Add a hook looking for collisions with localToon
        if (len(self.collNPList) > 0):
            self.accept('enter' + self.collNPList[-1].getName(), self.handleLastSavePointCollision)
            self.gameEndX = self.collNPList[-1].getX(render)
    
    def handleLastSavePointCollision(self, cevent):
        # The localToon has reached the last checkpoint.
        self.game.localToonVictory()