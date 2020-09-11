"""TwoDStomperMgr module: contains the TwoDStomperMgr class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from toontown.minigame import ToonBlitzGlobals
from toontown.minigame import TwoDStomper

class TwoDStomperMgr(DirectObject):
    """
    Each section has one TwoDStomperMgr, which controls all the stompers of that section.    
    All the positions are got from ToonBlitzGlobals.py.
    All stompers may or may not be used. It could randomly select x number of stompers
    from the entire list of stompers.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDStomperMgr')
    
    def __init__(self, section, stomperList):
        self.section = section
        self.stomperList = stomperList
        
        self.load()
    
    def destroy(self):
        self.section = None
        
        while len(self.stompers):
            stomper = self.stompers[0]
            stomper.destroy()
            self.stompers.remove(stomper)
        self.stompers = None
        
    def load(self):
        if len(self.stomperList):
            self.stompersNP = NodePath('Stompers')
            self.stompersNP.reparentTo(self.section.sectionNP)
        
        self.stompers = []
        for index in xrange(len(self.stomperList)):
            stomperAttribs = self.stomperList[index]
            self.createNewStomper(stomperAttribs)
            
    def createNewStomper(self, attrib, model = None):
        stomperId = self.section.getSectionizedId(len(self.stompers))
        if (model == None):
            model = self.section.sectionMgr.game.assetMgr.stomper
        newStomper = TwoDStomper.TwoDStomper(self, stomperId, attrib, model)
        newStomper.model.reparentTo(self.stompersNP)
        self.stompers.append(newStomper)
        
    def enterPlay(self, elapsedTime):
        """ This function is called when the minigame enters the play state."""
        for stomper in self.stompers:
            stomper.start(elapsedTime)
    
    def exitPlay(self):
        """ This function will be called when the minigame exits the play state."""
        pass
    
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        for stomper in self.stompers:
            stomper.enterPause()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        for stomper in self.stompers:
            stomper.exitPause()