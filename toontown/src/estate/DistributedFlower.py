from toontown.estate import DistributedPlantBase
from direct.directnotify import DirectNotifyGlobal
from toontown.estate import FlowerBase
from toontown.estate import GardenGlobals
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer

DIRT_AS_WATER_INDICATOR = True
DIRT_MOUND_HEIGHT = 0.3

class DistributedFlower(DistributedPlantBase.DistributedPlantBase, FlowerBase.FlowerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlower')

    def __init__(self, cr):
        DistributedPlantBase.DistributedPlantBase.__init__(self, cr)
        FlowerBase.FlowerBase.__init__(self,49, 0)
        self.confirmDialog = None
        self.stickUp = 1.07
        if DIRT_AS_WATER_INDICATOR:
            self.stickUp += DIRT_MOUND_HEIGHT
        self.collSphereRadius = 2.2
        self.shadowScale = 0.5
        self.collSphereOffset = 0.0
        self.dirtMound = None
        self.sandMound = None

        self.resultDialog = None

    def delete(self):
        DistributedPlantBase.DistributedPlantBase.delete(self)
        del self.dirtMound
        del self.sandMound


    def setTypeIndex(self, typeIndex):
        DistributedPlantBase.DistributedPlantBase.setTypeIndex(self, typeIndex)
        self.setSpecies(typeIndex)

    #There is already a setVariety in FlowerBase
    #def setVariety(self, variety):
    #   self.setVariety(variety)
    def showWiltOrBloom(self):
        if not self.model:
            return
        
        nodePath = self.model
        desat = None
        flowerColorIndex = GardenGlobals.PlantAttributes[self.getSpecies()]['varieties'][self.getVariety()][1]
        colorTuple = GardenGlobals.FlowerColors[flowerColorIndex]

        useWilted = self.waterLevel < 0
        wilt = nodePath.find('**/*wilt*')
        bloom = nodePath.find('**/*bloom*')
        if useWilted:
            wilt.show()
            desat = wilt.find('**/*desat*')
            bloom.hide()
            leaves =wilt.findAllMatches('**/*leaf*')
            for leafIndex in range(leaves.getNumPaths()):
                leaf = leaves.getPath(leafIndex)
                leaf.setColorScale(1.0,0.3,0.1, 1.0)

        else:
            bloom.show()
            desat = bloom.find('**/*desat*')
            wilt.hide()
            
        if desat and not desat.isEmpty():            
            desat.setColorScale( colorTuple[0],
                                    colorTuple[1],
                                    colorTuple[2],
                                    1.0)            
        elif not self.isSeedling():
            #the seedling model does not have a desat node
            nodePath.setColorScale( colorTuple[0],
                                    colorTuple[1],
                                    colorTuple[2],
                                    1.0)            

        
        
    def loadModel(self):
        """
        Load the flower model, then set it to the correct color
        """
        DistributedPlantBase.DistributedPlantBase.loadModel(self)
        self.showWiltOrBloom()

        #because the flower's front is towards the -y axis, do a 180 turn
        self.model.setH(180)
        flowerScale = 2.0
        invFlowerScale = 1.0 / flowerScale
        self.model.setScale(flowerScale)

        if DIRT_AS_WATER_INDICATOR:
            dirtMoundScale = invFlowerScale * 0.73
            self.dirtMound = loader.loadModel("phase_5.5/models/estate/dirt_mound")
            self.dirtMound.reparentTo(self.model)
            self.dirtMound.setScale(dirtMoundScale)
            self.dirtMound.setZ(self.dirtMound.getZ() - DIRT_MOUND_HEIGHT/2.0)
            self.sandMound = loader.loadModel("phase_5.5/models/estate/sand_mound")
            self.sandMound.reparentTo(self.model)
            self.sandMound.setScale(dirtMoundScale)
            self.sandMound.setZ(self.sandMound.getZ() - DIRT_MOUND_HEIGHT/2.0)
            self.adjustWaterIndicator()
        

    def handlePicking(self):
        """
        Confirm if the player really wants to remove or pick the plower.
        """
        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')
        
        fullName = GardenGlobals.getFlowerVarietyName(self.species,
                                                      self.variety)        
        if self.isWilted():
            self.confirmDialog = TTDialog.TTDialog(
                style = TTDialog.YesNo,
                text = TTLocalizer.ConfirmWiltedFlower % {'plant': fullName},
                command = self.confirmCallback
                )
        elif not self.isFruiting():
            self.confirmDialog = TTDialog.TTDialog(
                style = TTDialog.YesNo,
                text = TTLocalizer.ConfirmUnbloomingFlower % {'plant': fullName},
                command = self.confirmCallback
                )
        elif base.localAvatar.isFlowerBasketFull():
            self.confirmDialog = TTDialog.TTDialog(
                style = TTDialog.CancelOnly,
                text = TTLocalizer.ConfirmBasketFull,
                command = self.confirmCallback
                )

        else:
            #we are sure it is going into the flower basket
            shovel = base.localAvatar.shovel
            skill = base.localAvatar.shovelSkill
            shovelPower = GardenGlobals.getShovelPower(shovel, skill)
            giveSkillUp = True
            beansRequired = GardenGlobals.getNumBeansRequired(self.species,
                                                              self.variety)
            if not shovelPower == beansRequired:
                giveSkillUp = False

            if giveSkillUp:
                if skill == GardenGlobals.getMaxShovelSkill():
                    text = TTLocalizer.ConfirmMaxedSkillFlower % {'plant': fullName},
                else:
                    text = TTLocalizer.ConfirmSkillupFlower % {'plant': fullName}
                self.confirmDialog = TTDialog.TTDialog(
                    style = TTDialog.YesNo,
                    text = text,
                    command = self.confirmCallback
                )
            else:
                self.confirmDialog = TTDialog.TTDialog(
                    style = TTDialog.YesNo,
                    text = TTLocalizer.ConfirmNoSkillupFlower % {'plant': fullName},
                    command = self.confirmCallback
                )                
                
        
        self.confirmDialog.show()
        base.localAvatar.setInGardenAction(self)
        base.cr.playGame.getPlace().detectedGardenPlotUse()
        
    def confirmCallback(self, value):
        self.notify.debug('value=%d' % value)
        self.confirmDialog.destroy()
        self.confirmDialog = None
        if value > 0:
            self.doPicking()
        else:
            #base.cr.playGame.getPlace().detectedGardenPlotDone()
            self.finishInteraction()


    def doPicking(self):
        """
        At this point assume we've already asked the player if he really wants
        to pick this flower
        """
        # check if this toon can pick this flower
        if not self.canBePicked():
            self.notify.debug("I don't own this flower, just returning")
            return

        #if we have no space return for now        
        #if base.localAvatar.isFlowerBasketFull():
        #    self.notify.debug('flower basket is full, just returning')
        #    return

        base.localAvatar.showGardeningGui()
        base.localAvatar.removeShovelRelatedDoId(self.doId)
        #base.localAvatar.clearPlantToWater(self.doId)
        base.localAvatar.setInGardenAction(self)
        base.cr.playGame.getPlace().detectedGardenPlotUse()

        self.sendUpdate('removeItem',[])

        
    def setWaterLevel(self, waterLevel):
        DistributedPlantBase.DistributedPlantBase.setWaterLevel(self,waterLevel)
        self.showWiltOrBloom()

        if self.model:
            self.adjustWaterIndicator()

    def setGrowthLevel(self, growthLevel):
        #the base version also changes the scale, we don't want that
        origGrowthLevel = self.growthLevel
        self.growthLevel = growthLevel
        #but we do want to reload the model, since it's probably changed

        #todo don't load the model if not needed
        #a growth level of -1 is invalid, means this is the first time
        #we are getting the info from the server.
        #Also means self.growthThresholds will not be set yet
        if origGrowthLevel > -1 :
            self.loadModel()
            self.makeMovieNode()

    def makeMovieNode(self):
        # create a movieNode... this is where the toon will stand while playing a movie
        self.movieNode = self.rotateNode.attachNewNode('moviePos')
        self.movieNode.setPos(0, 3, 0)
        self.movieNode.setH(180)
        self.stick2Ground()
        


    def setupShadow(self):
        if DIRT_AS_WATER_INDICATOR:
            pass
        else:
            # set up the shadow            
            DistributedPlantBase.DistributedPlantBase.setupShadow(self)
            #do a something a little funky so the shadow shows up on the soil of the garden box
            self.setShadowHeight(-(self.stickUp + 1))
        
    def adjustWaterIndicator(self):
        if DIRT_AS_WATER_INDICATOR:
            if self.dirtMound:
                curWaterLevel = self.waterLevel
                if curWaterLevel > self.maxWaterLevel:
                    curWaterLevel = self.maxWaterLevel
                if curWaterLevel > 0:
                    darkestColorScale = 0.4
                    lightestColorScale = 1.0
                    scaleRange = lightestColorScale - darkestColorScale
                    scaleIncrement = scaleRange / self.maxWaterLevel
                    darker = lightestColorScale -  (scaleIncrement * curWaterLevel)
                    self.dirtMound.setColorScale(darker, darker, darker,1.0)
                    self.sandMound.hide()
                    self.dirtMound.show()
                else:
                    self.sandMound.show()
                    self.dirtMound.hide()
        else:
            if self.model:
                color = (float(self.waterLevel) / self.maxWaterLevel)
                self.dropShadow.setColor(0.0, 0.0, 0.0, color)


    def doResultDialog(self):
        #import pdb; pdb.set_trace()
        self.startInteraction()
        flowerName = GardenGlobals.getFlowerVarietyName(self.species,self.variety)        
        stringToShow = TTLocalizer.getResultPlantedSomethingSentence(flowerName)
                           
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
