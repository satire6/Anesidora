import DistributedTreasure
from pandac.PandaModules import VBase3, VBase4
from direct.interval.IntervalGlobal import Sequence, Wait, Func, LerpColorScaleInterval, LerpScaleInterval
from toontown.toonbase import ToontownGlobals

class DistributedSZTreasure(DistributedTreasure.DistributedTreasure):
    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)
        
        self.fadeTrack = None
        self.heartThrobIval = None
                
        self.accept('ValentinesDayStart', self.startValentinesDay)
        self.accept('ValentinesDayStop', self.stopValentinesDay)
        
    def delete(self):
        DistributedTreasure.DistributedTreasure.delete(self)
        # Stop the movie (if there is one)
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None
        
        if self.heartThrobIval:
            self.heartThrobIval.finish()
            self.heartThrobIval = None
        
        self.ignore('ValentinesDayStart')
        self.ignore('ValentinesDayStop')
    
    def setHolidayModelPath(self):
        """
        Change the modelPath if a holiday is running.
        """
        # Set the default model path.
        self.defaultModelPath = self.modelPath
        holidayIds = base.cr.newsManager.getHolidayIdList()
        if ToontownGlobals.VALENTINES_DAY in holidayIds:
            self.modelPath = "phase_4/models/props/tt_m_ara_ext_heart"
    
    def loadModel(self, modelPath, modelFindString = None):
        """
        Overiding loadModel of Distributed Treasure to account for holiday based treasures.
        """
        self.setHolidayModelPath()
        DistributedTreasure.DistributedTreasure.loadModel(self, self.modelPath, modelFindString)
    
    def startValentinesDay(self):
        """
        Do some show when the holiday starts.
        Change all the Ice Cream Cones to Hearts when the Valentines Day starts.
        """        
        newModelPath = "phase_4/models/props/tt_m_ara_ext_heart"
        self.replaceTreasure(newModelPath)
        self.startAnimation()
        
    def stopValentinesDay(self):
        """
        Do some show when the holiday ends.
        Change all the Hearts to Cones when the Valentines Day ends.
        """
        self.replaceTreasure(self.defaultModelPath)
        self.stopAnimation()
        
    def replaceTreasure(self, newModelPath):
        """
        The new treasure is replaced with the old treasure with a fadeInOut interval.
        """
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None
            
        def replaceTreasureFunc(newModelPath):
            if self.nodePath == None:
                self.makeNodePath()
            else:
                self.treasure.getChildren().detach()
            # Load the treasure model and put it under our root node.
            model = loader.loadModel(newModelPath)
            model.instanceTo(self.treasure)
            
        def getFadeOutTrack():
            fadeOutTrack = LerpColorScaleInterval(self.nodePath, 0.8,
                                   colorScale = VBase4(0, 0, 0, 0),
                                   startColorScale = VBase4(1, 1, 1, 1),
                                   blendType = 'easeIn')
            return fadeOutTrack
        
        def getFadeInTrack():
            fadeInTrack = LerpColorScaleInterval(self.nodePath, 0.5,
                                       colorScale = VBase4(1, 1, 1, 1),
                                       startColorScale = VBase4(0, 0, 0, 0),
                                       blendType = 'easeOut')
            return fadeInTrack
            
        base.playSfx(self.rejectSound, node = self.nodePath)
        self.fadeTrack = Sequence(
            getFadeOutTrack(),
            Func(replaceTreasureFunc, newModelPath),
            getFadeInTrack(),
            name = self.uniqueName("treasureFadeTrack"))
        self.fadeTrack.start()
    
    def startAnimation(self):
        """
        Make the Safezone Treasures animate if there is an animation associated.
        Currently, only the Valentine's Day Hearts animate.
        """
        holidayIds = base.cr.newsManager.getHolidayIdList()
        if ToontownGlobals.VALENTINES_DAY in holidayIds:
            # Animate the Valentine's Day Hearts here.
            originalScale = self.nodePath.getScale()
            throbScale = VBase3(0.85, 0.85, 0.85)
            throbInIval = LerpScaleInterval(self.nodePath, 0.3, 
                        scale = throbScale,
                        startScale = originalScale,
                        blendType = 'easeIn')
            throbOutIval = LerpScaleInterval(self.nodePath, 0.3, 
                        scale = originalScale,
                        startScale = throbScale,
                        blendType = 'easeOut')
                        
            self.heartThrobIval = Sequence(throbInIval,
                                 throbOutIval,
                                 Wait(0.75))
            self.heartThrobIval.loop()            
    
    def stopAnimation(self):
        """
        Stop anything that is animating.
        """
        if self.heartThrobIval:
            self.heartThrobIval.finish()
            self.heartThrobIval = None
            