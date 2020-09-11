import DistributedLawnDecor
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBase import *
import GardenGlobals
from toontown.toonbase import TTLocalizer
class DistributedPlantBase(DistributedLawnDecor.DistributedLawnDecor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlantBase')

    def __init__(self, cr):
        assert self.notify.debugStateCall(self)
        DistributedLawnDecor.DistributedLawnDecor.__init__(self, cr)
        self.model = None
        self.growthLevel = -1
        self.waterTrackDict = {}

    def delete(self):
        self.notify.debug('delete')
        for waterTrack in self.waterTrackDict.values():
            if waterTrack:
                waterTrack.finish()
        self.waterTrackDict = None
        DistributedLawnDecor.DistributedLawnDecor.delete(self)

    def disable(self):
        self.notify.debug('disable')
        DistributedLawnDecor.DistributedLawnDecor.disable(self)
        
    def loadModel(self):
        """
        Potentially loadModel could get called a 2nd time when an epoch goes off
        """
        if hasattr(self, 'rotateNode') and self.rotateNode:
            self.rotateNode.removeNode()
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = None
        modelName = self.getModelName()
        self.model = loader.loadModel(modelName)
        self.model.reparentTo(self.rotateNode)
        self.stick2Ground()

    def setupShadow(self):
        DistributedLawnDecor.DistributedLawnDecor.setupShadow(self)
        self.adjustWaterIndicator()

    def setTypeIndex(self, typeIndex):
        assert self.notify.debugStateCall(self)
        self.typeIndex = typeIndex
        self.attributes = GardenGlobals.PlantAttributes[typeIndex]
        self.name = self.attributes['name']
        self.plantType = self.attributes['plantType']
        self.growthThresholds = self.attributes['growthThresholds']
        self.maxWaterLevel = self.attributes['maxWaterLevel']
        self.minWaterLevel = self.attributes['minWaterLevel']
        self.seedlingModel = self.attributes['seedlingModel']
        self.establishedModel = self.attributes['establishedModel']
        self.fullGrownModel = self.attributes['fullGrownModel']
        
    def getTypeIndex(self):
        return self.typeIndex
        
    def setWaterLevel(self, waterLevel):
        self.waterLevel = waterLevel
        
    def getWaterLevel(self):
        return self.waterLevel
        
    def setGrowthLevel(self, growthLevel):
        self.growthLevel = growthLevel
        if self.model:
            self.model.setScale(growthLevel)
        
    def getGrowthLevel(self):
        return self.growthLevel
        
    def getShovelAction(self):
        if self.isFruiting() and not self.isWilted() and self.canBeHarvested():
            #show pick if its fruiting and not wilted
            return TTLocalizer.GardeningPick
        else:
            #show remove otherwise
            return TTLocalizer.GardeningRemove
            
    def getShovelCommand(self):
        return self.handlePicking      
        

    def canBeHarvested(self):
        return True

    def handleEnterPlot(self, colEntry = None):
        assert self.notify.debugStateCall(self)
        #print("Plot Entered; Collision = %s" % (optional))
        #DistributedFlower.py will override and replace this
        dist = self.getDistance(localAvatar)
        self.accept("water-plant", self.__handleWatering)
        base.localAvatar.addShovelRelatedDoId(self.doId)

    def handleExitPlot(self, entry = None):
        assert self.notify.debugStateCall(self)
        DistributedLawnDecor.DistributedLawnDecor.handleExitPlot(self, entry)
        base.localAvatar.removeShovelRelatedDoId(self.doId)
        self.ignore("water-plant")
        
    def handleWatering(self):
        self.startInteraction()
        self.sendUpdate('waterPlant')
        
    def __handleWatering(self, plantToWaterId):
        #never use this
        if plantToWaterId == self.doId:
            self.sendUpdate('waterPlant')
            #print("sending water plant")
        else:
            self.notify.debug("not sending water plant")
            #import pdb; pdb.set_trace()
        assert self.notify.debugStateCall(self)
        #TODO: base amount off of watering can
        #self.sendUpdate('waterPlant', [1])

    # Note the isFruiting, isGTEFruiting ... is seedling is also defined in
    # DistributedPlantBaseAI.py, if any changes are done, make sure they're in sync

    def isFruiting(self):
        retval = self.growthLevel >= self.growthThresholds[2]
        return retval

    def isGTEFruiting(self):
        """
        is greater than or equal to Fruiting
        """
        retval = self.growthLevel >= self.growthThresholds[2]
        return retval        

    def isFullGrown(self):
        """
        returns true only if it's exactly full grown
        """
        if self.growthLevel >= self.growthThresholds[2]:
            #the plant is fruiting
            return False
        elif self.growthLevel >= self.growthThresholds[1]:
            #the plant is full grown
            return True

        return False

    def isGTEFullGrown(self):
        """
        is greater than or equal to full grown
        """
        retval = self.growthLevel >= self.growthThresholds[1]
        return retval

    def isEstablished(self):
        if self.growthLevel >= self.growthThresholds[2]:
            #the plant is fruiting
            return False
        elif self.growthLevel >= self.growthThresholds[1]:
            #the plant is full grown
            return False
        elif self.growthLevel >= self.growthThresholds[0]:
            #the plant is established
            return True
        return False

    def isGTEEstablished(self):
        if self.growthLevel >= self.growthThresholds[0]:
            #the plant is >= established
            return True
        return False

    def isSeedling(self):
        if self.growthLevel >= self.growthThresholds[2]:
            #the plant is fruiting
            return False
        elif self.growthLevel >= self.growthThresholds[1]:
            #the plant is full grown
            return False
        elif self.growthLevel >= self.growthThresholds[0]:
            #the plant is established
            return False
        elif self.growthLevel < self.growthThresholds[0]:
            #the plant is a seedling
            return True

        return False

    def isGTESeedling(self):
        #duh everything >= seedling
        return True
    
    def isWilted(self):
        return self.waterLevel < 0
    
    def getModelName(self):
        if self.growthLevel >= self.growthThresholds[1]:
            #the plant is fruiting
            modelName = self.fullGrownModel
        elif self.growthLevel >= self.growthThresholds[1]:
            #the plant is full grown
            modelName = self.fullGrownModel
        elif self.growthLevel >= self.growthThresholds[0]:
            #the plant is established
            modelName = self.establishedModel
        else:
            #the plant is a seedling
            modelName = self.seedlingModel

        return modelName
        
    def setMovie(self, mode, avId):
        if mode == GardenGlobals.MOVIE_WATER:
            self.doWaterTrack(avId)
        elif mode == GardenGlobals.MOVIE_FINISHPLANTING:
            self.doFinishPlantingTrack(avId)
        elif mode == GardenGlobals.MOVIE_REMOVE:
            self.doDigupTrack(avId)

    def doWaterTrack(self, avId):
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        # load the watering can
        can = toon.getWateringCanModel()
        can.hide()
        can.reparentTo(toon.rightHand)

        track = Sequence()
        
        track.append(self.startCamIval(avId))
        track.append(self.generateToonMoveTrack(toon))
        track.append(Func(can.show))
        track.append(self.generateWaterTrack(toon))
        track.append(Func(can.removeNode))
        track.append(self.stopCamIval(avId))

        if avId == localAvatar.doId:
            track.append(Func(self.sendUpdate, 'waterPlantDone'))
            track.append(Func(self.finishInteraction))

        track.start()
        self.waterTrackDict[avId] = track

    def generateWaterTrack( self, toon ):
        """
        """
        sound = loader.loadSfx('phase_5/audio/sfx/firehose_spray.mp3')
        sound.setPlayRate(0.75)
        waterTrack = Parallel()
        waterTrack.append(
            Sequence( Parallel(ActorInterval( toon, "water" ),
                               SoundInterval( sound, node=toon, volume=0.5 )),
                      Func( toon.loop, 'neutral' ),
                      ),
            
            )

        if hasattr(self,'dropShadow') and self.dropShadow:
            newColor = self.dropShadow.getColor()
            alpha = min(1.0, newColor.getW() + (1/5.0))
            newColor.setW(alpha)
            
            waterTrack.append(
                LerpColorInterval(self.dropShadow, 2.1, newColor)
            )

        return waterTrack
    
    def adjustWaterIndicator(self):
        if self.model:
            color = (self.waterLevel / 5.0) + (1 / 5.0 )
            self.notify.debug('%s %s'  % (self.waterLevel, color))
            if color < 0.2:
                color = 0.2
            if hasattr(self,'dropShadow') and self.dropShadow:
                self.dropShadow.setColor(0.0, 0.0, 0.0, color)
                
    def canBeWatered(self):
        return 1
        
    def finishInteraction(self):
        #print "### PlantBase: finishInteraction"
        DistributedLawnDecor.DistributedLawnDecor.finishInteraction(self)
        #messenger.send("endPlantInteraction")
        base.localAvatar.handleEndPlantInteraction(self)

