import DistributedLawnDecor
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBase import *
from direct.interval.IntervalGlobal import *
import GardenGlobals
from toontown.toonbase import TTLocalizer
from toontown.estate import PlantingGUI
from toontown.estate import PlantTreeGUI
from toontown.estate import ToonStatueSelectionGUI
from toontown.toontowngui import TTDialog
from pandac.PandaModules import Vec4
from pandac.PandaModules import NodePath
import types


class DistributedGardenPlot(DistributedLawnDecor.DistributedLawnDecor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGardenPlot')


    def __init__(self, cr):
        DistributedLawnDecor.DistributedLawnDecor.__init__(self, cr)
        #self.defaultModel = "phase_8/models/props/flower_treasure.bam"


        self.plantPath = NodePath('plantPath')
        self.plantPath.reparentTo(self)
        self.plotScale = 1.0

        self.plantingGuiDoneEvent = "plantingGuiDone"
        self.toonStatueSelectionDoneEvent = "toonStatueSelectionDone"
        self.defaultModel = "phase_5.5/models/estate/dirt_mound"
        self.colorScaler = Vec4(1,1,1,1)

        self.plantingGui = None

    def delete(self):
        if self.plantingGui:
            self.plantingGui.destroy()
            self.plantingGui = None
        DistributedLawnDecor.DistributedLawnDecor.delete(self)



    def announceGenerate(self):
        #need to wait to do this until ownerindex  and plot come in from the ai
        self.plotType = GardenGlobals.whatCanBePlanted(self.ownerIndex, self.plot)
        #differentiate the plot types here
        self.stickUp = 0.0
        if self.getOwnerId() != localAvatar.doId:
            self.defaultModel = None
        elif self.plotType == GardenGlobals.FLOWER_TYPE:
            self.collSphereRadius = 2.0
            self.collSphereOffset = 0.0
            self.plotScale = .70
            self.stickUp = 1.1
           # self.defaultModel = "phase_5.5/models/estate/planterA"
        elif self.plotType == GardenGlobals.GAG_TREE_TYPE:
            self.collSphereRadius = 3.0
            self.plotScale = 1.5
            self.colorScaler = Vec4(1.0,1.0,1.0,1)
            #self.defaultModel = "phase_5.5/models/estate/planterB"
        elif self.plotType == GardenGlobals.STATUARY_TYPE:
            self.collSphereRadius = 3.0
            self.plotScale = 0.075
            self.stickUp = -0.0
            #self.defaultModel = "phase_5.5/models/estate/dirt_mound"
            self.defaultModel = "phase_5.5/models/estate/garden_slab"
        else:
            self.collSphereOffset = 0.0
        self.notify.debug('announceGenerate')
        DistributedLawnDecor.DistributedLawnDecor.announceGenerate(self)

    def loadModel(self):
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = None

        if self.defaultModel:
            self.model = loader.loadModel(self.defaultModel)
            if type(self.plotScale) == types.TupleType:
                self.model.setScale(*self.plotScale)
            else:
                self.model.setScale(self.plotScale)
            self.model.reparentTo(self.rotateNode)
            self.model.setColorScale(self.colorScaler)
            self.stick2Ground()

    def setupShadow(self):
        pass

    def getShovelCommand(self):
        return self.plantSomething

    def getShovelAction(self):
        return self.getPlantingText()

    def handleEnterPlot(self, entry = None):
        #print("plot entered %s" % (self.doId))
        #print entry
        dist = self.getDistance(localAvatar)
        if self.canBePlanted():
            base.localAvatar.addShovelRelatedDoId(self.doId) #, self.plantSomething)

    def handleExitPlot(self, entry = None):
        DistributedLawnDecor.DistributedLawnDecor.handleExitPlot(self, entry)
        #print("plot exited %s" % (self.doId))
        #print entry
        base.localAvatar.removeShovelRelatedDoId(self.doId)
        #base.localAvatar.clearPlantToWater(self.doId)
        #base.localAvatar.hideWateringCanButton()

    def getPlantingText(self):
        plantText = "hardcoding"
        if self.canBePlanted():
            whatCanBePlanted = GardenGlobals.whatCanBePlanted(self.ownerIndex, self.plot)
            plantText = TTLocalizer.GardeningPlant
            if whatCanBePlanted == GardenGlobals.INVALID_TYPE:
                self.notify.warning('whatCanBePlanted returned INVALID_TYPE for %d %d' % (self.ownerIndex, self.plot))
            elif whatCanBePlanted == GardenGlobals.FLOWER_TYPE:
                plantText = TTLocalizer.GardeningPlantFlower
            elif whatCanBePlanted == GardenGlobals.GAG_TREE_TYPE:
                plantText = TTLocalizer.GardeningPlantTree
            elif whatCanBePlanted == GardenGlobals.STATUARY_TYPE:
                plantText = TTLocalizer.GardeningPlantItem
        return plantText


    def canBePlanted(self):
        """
        Other subclasses may extend this function, but at the very least,
        you can't plant on something you don't own
        """
        retval = True
        if not base.localAvatar.doId == self.getOwnerId():
            retval = False

        return retval

    def plantSomething(self):
        whatCanBePlanted = GardenGlobals.whatCanBePlanted(self.ownerIndex, self.plot)
        if whatCanBePlanted == GardenGlobals.INVALID_TYPE:
            self.notify.warning('whatCanBePlanted returned INVALID_TYPE for %d %d' % (self.ownerIndex, self.plot))
        elif whatCanBePlanted == GardenGlobals.FLOWER_TYPE:
            #self.sendUpdate('plantFlower',[48,1])
            self.popupFlowerPlantingGui()
            #self.cr.playGame.getPlace().detectedGardenPlotUse()
            self.startInteraction()

        elif whatCanBePlanted == GardenGlobals.GAG_TREE_TYPE:
            self.popupTreePlantingGui()
            #self.cr.playGame.getPlace().detectedGardenPlotUse()
            self.startInteraction()
        elif whatCanBePlanted == GardenGlobals.STATUARY_TYPE:
            self.popupItemPlantingGui()
            #self.cr.playGame.getPlace().detectedGardenPlotUse()
            self.startInteraction()
            pass
        pass

    def __handleFlowerPlantingDone(self, willPlant = 0, recipeStr = "", special = -1):
        assert self.notify.debugStateCall(self)
        self.ignore(self.plantingGuiDoneEvent)
        self.ignore('stoppedAsleep')
        # Ask the AI to complete the sale
        #self.sendUpdate("completeFlowerSale", [sell])
        self.plantingGui.destroy()
        self.plantingGui = None
        base.localAvatar.showGardeningGui()
        base.localAvatar.removeShovelRelatedDoId(self.doId)

        successPlanting = False
        if willPlant:
            recipeKey = GardenGlobals.getRecipeKey(recipeStr,special)
            if recipeKey >= 0:
                species, variety = GardenGlobals.getSpeciesVarietyGivenRecipe(recipeKey)
                if species >= 0 and variety >= 0:
                    self.sendUpdate('plantFlower',[species,variety])
                    successPlanting = True
            else:
                self.notify.debug("%s %d is not a valid recipe" % (recipeStr,special) )
                burntBeans = len(recipeStr)
                self.sendUpdate('plantNothing', [burntBeans])

        if successPlanting:
            flowerName = GardenGlobals.getFlowerVarietyName(species,variety)
            stringToShow = TTLocalizer.getResultPlantedSomethingSentence(flowerName)

        #   the dialog will now come up after the planting movie
        #    self.resultDialog = TTDialog.TTDialog(
        #        style = TTDialog.Acknowledge,
        #        text = stringToShow,
        #        command = self.resultsCallback
        #        )
        elif willPlant:
            self.resultDialog = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = TTLocalizer.ResultPlantedNothing,
                command = self.popupFlowerPlantingGuiAgain
                )
        else:
            #base.cr.playGame.getPlace().detectedGardenPlotDone()
            self.finishInteraction()

    def popupFlowerPlantingGui(self):
        assert self.notify.debugStateCall(self)
        base.localAvatar.hideGardeningGui()
        self.acceptOnce(self.plantingGuiDoneEvent, self.__handleFlowerPlantingDone)
        self.plantingGui = PlantingGUI.PlantingGUI(self.plantingGuiDoneEvent)
        self.accept('stoppedAsleep', self.__handleFlowerPlantingDone)

    def resultsCallback(self, value):
        self.notify.debug('value=%d' % value)
        self.resultDialog.destroy()
        self.resultDialog = None
        #base.cr.playGame.getPlace().detectedGardenPlotDone()
        self.finishInteraction()

    def popupFlowerPlantingGuiAgain(self, value):
        self.notify.debug('value=%d' % value)
        self.resultDialog.destroy()
        self.resultDialog = None
        self.popupFlowerPlantingGui()

    def popupItemPlantingGuiAgain(self, value):
        self.notify.debug('value=%d' % value)
        self.resultDialog.destroy()
        self.resultDialog = None
        self.popupItemPlantingGui()

    def __handleItemPlantingDone(self, willPlant = 0, recipeStr = "", selectedSpecial = -1):
        assert self.notify.debugStateCall(self)
        self.ignore(self.plantingGuiDoneEvent)
        self.ignore('stoppedAsleep')
        # Ask the AI to complete the sale
        #self.sendUpdate("completeFlowerSale", [sell])
        self.plantingGui.destroy()
        self.plantingGui = None
        base.localAvatar.showGardeningGui()
        base.localAvatar.removeShovelRelatedDoId(self.doId)

        gardenSpecials = base.localAvatar.getGardenSpecials()
        special = -1
        if selectedSpecial >= 0:
            special = gardenSpecials[selectedSpecial][0]

        successPlanting = False
        successToonStatue = False
        if willPlant:
            recipeKey = GardenGlobals.getRecipeKey(recipeStr,special)
            if recipeKey >= 0:
                species, variety = GardenGlobals.getSpeciesVarietyGivenRecipe(recipeKey)
                if species >= 0 and variety >= 0:
                    #make sure it is a statuary and not a flower
                    if GardenGlobals.PlantAttributes[species]['plantType'] == GardenGlobals.STATUARY_TYPE:
                        successPlanting = True
                        # Handle ToonStatues separately because another screen has to be added
                        if species >= 205 and species <= 208:
                            successToonStatue = True
                        else:
                            self.sendUpdate('plantStatuary',[species])
            else:
                self.notify.debug( "%s %d is not a valid recipe" % (recipeStr,special))
                burntBeans = len(recipeStr)
                self.sendUpdate('plantNothing', [burntBeans])

        if successPlanting:
            itemName = GardenGlobals.PlantAttributes[species]['name']
            stringToShow = TTLocalizer.getResultPlantedSomethingSentence(itemName)

        #    self.resultDialog = TTDialog.TTDialog(
        #        style = TTDialog.Acknowledge,
        #        text = stringToShow,
        #        command = self.resultsCallback
        #        )
        elif willPlant:
            self.resultDialog = TTDialog.TTDialog(
                style = TTDialog.Acknowledge,
                text = TTLocalizer.ResultPlantedNothing,
                command = self.popupItemPlantingGuiAgain
                )
        else:
            #base.cr.playGame.getPlace().detectedGardenPlotDone()
            self.finishInteraction()

        if successToonStatue:
            self.popupToonStatueSelectionGui(species)

    def popupItemPlantingGui(self):
        assert self.notify.debugStateCall(self)
        base.localAvatar.hideGardeningGui()
        self.acceptOnce(self.plantingGuiDoneEvent, self.__handleItemPlantingDone)
        self.plantingGui = PlantingGUI.PlantingGUI(self.plantingGuiDoneEvent,True)
        self.plantingGui.showFirstSpecial()
        self.accept('stoppedAsleep', self.__handleItemPlantingDone)

    def popupToonStatueSelectionGui(self, species):
        assert self.notify.debugStateCall(self)
        base.localAvatar.hideGardeningGui()
        self.acceptOnce(self.toonStatueSelectionDoneEvent, self.__handleToonStatueSelectionDone, extraArgs = [species])
        self.toonStatueSelectionGui = ToonStatueSelectionGUI.ToonStatueSelectionGUI(self.toonStatueSelectionDoneEvent,True)
        self.accept('stoppedAsleep', self.__handleToonStatueSelectionDone)

    def popupToonStatueSelectionGuiAgain(self, species):
        assert self.notify.debugStateCall(self)
        self.resultDialog.destroy()
        self.resultDialog = None
        self.popupToonStatueSelectionGui(species)

    def __handleToonStatueSelectionDone(self, species, willPlant = 0, recipeStr = "", dnaCode = -1):
        assert self.notify.debugStateCall(self)
        self.ignore(self.toonStatueSelectionDoneEvent)
        self.ignore('stoppedAsleep')
        self.toonStatueSelectionGui.destroy()
        self.toonStatueSelectionGui = None
        base.localAvatar.showGardeningGui()
        base.localAvatar.removeShovelRelatedDoId(self.doId)

        if willPlant:
            self.sendUpdate('plantToonStatuary',[species, dnaCode])
        else:
            self.popupItemPlantingGui()
##            self.finishInteraction()

    def popupTreePlantingGui(self):
        assert self.notify.debugStateCall(self)
        base.localAvatar.hideGardeningGui()
        self.acceptOnce(self.plantingGuiDoneEvent, self.__handleTreePlantingDone)
        self.plantingGui = PlantTreeGUI.PlantTreeGUI(self.plantingGuiDoneEvent)
        self.accept('stoppedAsleep', self.__handleTreePlantingDone)

    def __handleTreePlantingDone(self, willPlant = False, gagTrack = None, gagLevel = None):
        assert self.notify.debugStateCall(self)
        self.ignore(self.plantingGuiDoneEvent)
        self.ignore('stoppedAsleep')
        self.plantingGui.destroy()
        self.plantingGui = None
        base.localAvatar.showGardeningGui()
        base.localAvatar.removeShovelRelatedDoId(self.doId)

        if willPlant:
            self.sendUpdate('plantGagTree',[gagTrack, gagLevel])
            #species = GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel)
            #stringToShow = TTLocalizer.ResultPlantedSomething % GardenGlobals.PlantAttributes[species]['name']
            #self.resultDialog = TTDialog.TTDialog(
            #    style = TTDialog.Acknowledge,
            #    text = stringToShow,
            #    command = self.resultsCallback
            #    )
        else:
            #base.cr.playGame.getPlace().detectedGardenPlotDone()
            self.finishInteraction()

    def setMovie(self, mode, avId):
        if mode == GardenGlobals.MOVIE_PLANT:
            self.doPlaceItemTrack(avId)
        elif mode == GardenGlobals.MOVIE_FINISHREMOVING:
            self.doFinishRemovingTrack(avId)
        elif mode == GardenGlobals.MOVIE_PLANT_REJECTED:
            self.doPlantRejectedTrack(avId)

    def doPlantRejectedTrack(self, avId):
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        self.finishMovies()
        self.movie = Sequence()
        self.movie.append(Func( toon.detachShovel ))
        self.movie.append(Func( toon.loop, 'neutral'))

        if avId == localAvatar.doId:
            self.movie.append(Func(self.finishInteraction))
            self.movie.append(Func(self.movieDone))

        self.movie.start()        

    def doFinishRemovingTrack(self, avId):
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        self.finishMovies()

        self.movie = Sequence()

        self.movie.append(Func( toon.detachShovel ))
        if self.model:
            pos = self.model.getPos()
            pos.setZ(pos[2]-1)
            animProp = LerpPosInterval(self.model, 3, self.model.getPos(), pos)
            shrinkProp = LerpScaleInterval(self.model, 3,  scale = self.plotScale, startScale = 0.01)

            objAnimShrink = ParallelEndTogether(animProp, shrinkProp)
            self.movie.append(objAnimShrink)


        self.movie.append(self.stopCamIval(avId))
        self.movie.append(Func( toon.loop, 'neutral'))

        if avId == localAvatar.doId:
            self.movie.append(Func(self.finishInteraction))
            self.movie.append(Func(self.movieDone))

        self.movie.start()

    def doPlaceItemTrack(self, avId, item = None):
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        self.finishMovies()

        # load the shovel
        if avId == localAvatar.doId:
            self.startInteraction()
        shovel = toon.attachShovel()
        shovel.hide()

        moveTrack = self.generateToonMoveTrack(toon)
        placeItemTrack = self.generatePlaceItemTrack(toon, item)
        self.movie = Sequence(self.startCamIval(avId),
                              moveTrack,
                              Func(shovel.show),
                              placeItemTrack,
                              #self.stopCamIval(avId),
                              )

        if avId == localAvatar.doId:
            self.expectingReplacement = 1
            self.movie.append(Func(self.movieDone))

        self.movie.start()

    def generatePlaceItemTrack( self, toon, item ):
        """
        """
        sound = loader.loadSfx('phase_5.5/audio/sfx/burrow.mp3')
        sound.setPlayRate(0.5)
        placeItemTrack = Parallel()
        placeItemTrack.append(
            Sequence( ActorInterval( toon, "start-dig" ),
                      Parallel(ActorInterval( toon, "loop-dig", loop=1, duration=5.13 ),
                               Sequence(Wait(0.25), SoundInterval(sound, node=toon, duration=0.55),
                                        Wait(0.80), SoundInterval(sound, node=toon, duration=0.55),
                                        Wait(1.35), SoundInterval(sound, node=toon, duration=0.55),
                                        ),
                               ),
                      ActorInterval( toon, "start-dig", playRate=-1 ),
                      Func(toon.loop, 'neutral'),
                      Func(toon.detachShovel),
                      )
            )
        if self.model:
            pos = self.model.getPos()
            pos.setZ(pos[2]-1)
            #placeItemTrack.append(LerpPosInterval(self.model, 3, pos))

            animProp = LerpPosInterval(self.model, 3,  pos)
            shrinkProp = LerpScaleInterval(self.model, 3,  scale = 0.01, startScale = self.model.getScale())

            objAnimShrink = ParallelEndTogether(animProp, shrinkProp)
            placeItemTrack.append(objAnimShrink)

        if item:
            placeItemTrack.append(
                Sequence( Func( item.reparentTo, toon.rightHand ),
                          Wait( 0.55 ),
                          Func( item.wrtReparentTo, render ),
                          Parallel( LerpHprInterval( item,
                                                     hpr = self.getHpr( render ),
                                                     duration = 1.2 ),
                                    ProjectileInterval( item,
                                                        endPos = self.getPos( render ),
                                                        duration = 1.2,
                                                        gravityMult = 0.45 ),
                                    ),
                          Func( item.removeNode ),
                          )
                )
        return placeItemTrack

    def makeMovieNode(self):
        # create a movieNode... this is where the toon will stand while playing a movie
        if self.plotType == GardenGlobals.FLOWER_TYPE:
            self.movieNode = self.rotateNode.attachNewNode('moviePos')
            self.movieNode.setPos(0,3,0)
            self.movieNode.setH(180)
            self.stick2Ground()
        else:
            DistributedLawnDecor.DistributedLawnDecor.makeMovieNode(self)

