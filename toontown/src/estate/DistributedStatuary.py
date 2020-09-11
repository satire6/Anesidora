import DistributedLawnDecor
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBase import *
import GardenGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from pandac.PandaModules import NodePath
from pandac.PandaModules import Point3

class DistributedStatuary(DistributedLawnDecor.DistributedLawnDecor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStatuary')
    
    
    def __init__(self, cr):
        self.notify.debug("constructing DistributedStatuary")
        DistributedLawnDecor.DistributedLawnDecor.__init__(self, cr)
        self.confirmDialog = None
        self.resultDialog = None
        
    def loadModel(self):
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = loader.loadModel(self.modelPath)
        #import pdb; pdb.set_trace()
        colNode = self.model.find("**/+CollisionNode")
        if not colNode.isEmpty():
            score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballStatuary]
            if self.pinballScore:
                score = self.pinballScore[0]
                multiplier = self.pinballScore[1]
            scoreNodePath = NodePath("statuary-%d-%d" % (score, multiplier))
            colNode.setName('statuaryCol')
            scoreNodePath.reparentTo( colNode.getParent())
            colNode.reparentTo(scoreNodePath)
        self.model.setScale(self.worldScale)
        self.model.reparentTo(self.rotateNode)

        attrib = GardenGlobals.PlantAttributes[self.typeIndex]
        
        self.stick2Ground()

    def setTypeIndex(self, typeIndex):

        #import pdb; pdb.set_trace()
        
        self.typeIndex = typeIndex
        self.name = GardenGlobals.PlantAttributes[typeIndex]['name']
        self.plantType = GardenGlobals.PlantAttributes[typeIndex]['plantType']
        self.modelPath = GardenGlobals.PlantAttributes[typeIndex]['model']
        self.pinballScore = None
        if GardenGlobals.PlantAttributes[typeIndex].has_key('pinballScore'):
            self.pinballScore = GardenGlobals.PlantAttributes[typeIndex]\
                                ['pinballScore']
        self.worldScale = 1.0
        if GardenGlobals.PlantAttributes[typeIndex].has_key('worldScale'):
            self.worldScale = GardenGlobals.PlantAttributes[typeIndex]['worldScale']
        
    def getTypeIndex(self):
        return self.typeIndex
        
    def setWaterLevel(self, waterLevel):
        self.waterLevel = waterLevel
        
    def getWaterLevel(self):
        return self.waterLevel
        
    def setGrowthLevel(self, growthLevel):
        self.growthLevel = growthLevel
        
    def getGrowthLevel(self):
        return self.growthLevel
        


    def setupCollision(self):
        DistributedLawnDecor.DistributedLawnDecor.setupCollision(self)
        minPt = Point3(0,0,0)
        maxPt = Point3(0,0,0)
        self.model.calcTightBounds(minPt,maxPt)
        #radius = bounds.getRadius()
        self.notify.debug( "max=%s min=%s" % (maxPt,minPt))
        xDiff = maxPt[0] - minPt[0]
        yDiff = maxPt[1] - minPt[1]
        radius = (xDiff * xDiff + yDiff*yDiff) ** 0.5
        #I don't understand why calcTightBounds is giving me such huge numbers back
        radius /= 3
        self.notify.debug( 'xDiff=%s yDiff=%s radius = %s' % (xDiff, yDiff, radius))
        self.colSphereNode.setScale(radius)
        
    def getShovelCommand(self):
        return self.handlePicking

    def getShovelAction(self):
        return TTLocalizer.GardeningRemove

    def handleEnterPlot(self, colEntry = None):
        if self.canBePicked():
            self.notify.debug('entering if')
            base.localAvatar.addShovelRelatedDoId(self.doId)
            base.localAvatar.setShovelAbility(TTLocalizer.GardeningRemove)
            #base.localAvatar.showShovelButton()
        else:
            self.notify.debug('entering else')
            #base.localAvatar.hideShovelButton()
            pass
        #base.localAvatar.hideWateringCanButton()
        #self.handlePicking()
        
    def handlePicking(self):
        """
        Confirm if the player really wants to remove or pick the plower.
        """
        fullName = self.name

        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')        

        self.confirmDialog = TTDialog.TTDialog(
            style = TTDialog.YesNo,
            text = TTLocalizer.ConfirmRemoveStatuary % {'item': fullName},
            command = self.confirmCallback
            )
        self.confirmDialog.show()
        base.cr.playGame.getPlace().detectedGardenPlotUse()
        
    def confirmCallback(self, value):
        self.notify.debug('value=%d' % value)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = None
        if value > 0:
            self.doPicking()
        else:
            base.cr.playGame.getPlace().detectedGardenPlotDone()			 
 
    def doPicking(self):
        """
        At this point assume we've already asked the player if he really wants
        to pick this flower
        """
        #return
        # check if this toon can pick this flower
        if not self.canBePicked():
            self.notify.debug("I don't own this flower, just returning")
            return
        self.handleRemove()


    def handleExitPlot(self, entry = None):
        DistributedLawnDecor.DistributedLawnDecor.handleExitPlot(self, entry)
        base.localAvatar.removeShovelRelatedDoId(self.doId)
        #base.localAvatar.clearPlantToWater(self.doId)


    def doResultDialog(self):
        self.startInteraction()
        itemName = GardenGlobals.PlantAttributes[self.typeIndex]['name']
        stringToShow = TTLocalizer.getResultPlantedSomethingSentence(itemName)
                           
        self.resultDialog = TTDialog.TTDialog(
            style = TTDialog.Acknowledge,
            text = stringToShow,
            command = self.resultsCallback
            )         

    def resultsCallback(self, value):
        self.notify.debug('value=%d' % value)
        if self.resultDialog:
            self.resultDialog.destroy()
            self.resultDialog = None
        self.finishInteraction()

