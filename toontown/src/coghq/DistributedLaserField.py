from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from StomperGlobals import *
from direct.distributed import ClockDelta
from direct.showbase.PythonUtil import lerp
import math
from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from otp.level import BasicEntities
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.coghq import BattleBlocker
from toontown.toonbase import TTLocalizer
import random

class DistributedLaserField(BattleBlocker.BattleBlocker):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLaserField')
    
    laserFieldModels = ['phase_9/models/cogHQ/square_stomper',]
    
    def __init__(self, cr):
        BattleBlocker.BattleBlocker.__init__(self, cr)
        node = hidden.attachNewNode('DistributedNodePathEntity')
        
        #battle blocker stuff
        if not hasattr(self, "radius"):
            self.radius = 5
        if not hasattr(self, "blockerX"):
            self.blockerX = 0.0
        if not hasattr(self, "blockerY"):
            self.blockerY = 0.0
            
        self.blockerZ = -10000
        
        self.gridWireGN = None;
        self.gridBeamGN = None;
        
        self.traceWireGN = None;
        self.traceBeamGN = None;
        
        self.gridSeed = 0
        self.gridScaleX = 2.0
        self.gridScaleY = 2.0
        self.zFloat = 0.05
        
        self.projector = Point3(0,0,25)
        
        self.tracePath = []
        self.gridData = [[0,0]] * 2
        self.gridNumX = 2
        self.gridNumY = 2
        #(coordX, coordY, bright?)
        self.tracePath.append ((0.51, 0.51, 1))
        self.tracePath.append ((0.59, 0.51, 1))
        self.tracePath.append ((0.55, 0.59, 1))
        self.tracePath.append ((0.51, 0.51, 1))
        
        self.gridSymbols = [] #vertex data for various grid indexes
        self.makeGridSymbols()
        
        self.isToonIn = 0
        self.toonX = -1
        self.toonY = -1
        
        self.isToonInRange = 0
        self.detectCount = 0
        self.cameraHold = None
        
        self.gridGame = "some game"
        self.gridGameText = " " 
        self.activeLF = 1
        
        #self.WireGN=GeomNode("grid")
        
        #self.wireNode = NodePath.NodePath(self.WireGN)
        self.successSound = loader.loadSfx("phase_11/audio/sfx/LB_capacitor_discharge_3.mp3")
        self.successTrack = Parallel(SoundInterval(self.successSound, node=self, volume=.8))
        
        self.failSound = loader.loadSfx("phase_11/audio/sfx/LB_sparks_1.mp3")
        self.failTrack = Parallel(SoundInterval(self.failSound, node=self, volume=.8))        
        
    def generateInit(self):
        self.notify.debug('generateInit')
        BattleBlocker.BattleBlocker.generateInit(self)

    def generate(self):
        self.notify.debug('generate')
        BasicEntities.DistributedNodePathEntity.generate(self)
        
        
    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        BattleBlocker.BattleBlocker.announceGenerate(self)
        # at this point all the entity attributes have been initialized
        # we can load the model now.

        self.gridWireNode = self.attachNewNode("grid Wire Node")
        self.gridWireGN=GeomNode("grid wire")
        self.gridWireNode.attachNewNode(self.gridWireGN)
        self.gridWireNode.setRenderModeWireframe()
        self.gridWireNode.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.gridWireNode.setTwoSided(True)
        self.gridWireNode.setBin('fixed', 1)
        self.gridWireNode.setDepthWrite(False)
        
        self.gridBeamNode = self.attachNewNode("grid Beam Node")
        self.gridBeamGN=GeomNode("grid beam")
        self.gridBeamNode.attachNewNode(self.gridBeamGN)
        self.gridBeamNode.setTransparency(TransparencyAttrib.MAlpha)
        self.gridBeamNode.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.gridBeamNode.setTwoSided(True)
        self.gridBeamNode.setBin('fixed', 1)
        self.gridBeamNode.setDepthWrite(False)
        
        self.traceWireNode = self.attachNewNode("trace Wire Node")
        self.traceWireGN=GeomNode("trace Wire")
        self.traceWireNode.attachNewNode(self.traceWireGN)
        self.traceWireNode.setRenderModeWireframe()
        self.traceWireNode.setTransparency(TransparencyAttrib.MAlpha)
        self.traceWireNode.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.traceWireNode.setTwoSided(True)
        self.traceWireNode.setBin('fixed', 1)
        self.traceWireNode.setDepthWrite(False)
        
        self.traceBeamNode = self.attachNewNode("trace Beam Node")
        self.traceBeamGN=GeomNode("trace Beam")
        self.traceBeamNode.attachNewNode(self.traceBeamGN)
        self.traceBeamNode.setTransparency(TransparencyAttrib.MAlpha)
        self.traceBeamNode.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.traceBeamNode.setTwoSided(True)
        self.traceBeamNode.setBin('fixed', 1)
        self.traceBeamNode.setDepthWrite(False)
        
        self.loadModel()
        
        self.detectName = (("laserField %s") % (self.doId))
        taskMgr.doMethodLater(0.1, self.__detect, self.detectName)
        
    def initCollisionGeom(self):
        pass #overwritting battle blocker
        #import pdb; pdb.set_trace()
        
    def setGridGame(self, gameName):
        self.gridGame = gameName
        self.gridGameText = gameName
        if gameName == "MineSweeper":
            self.gridGameText = TTLocalizer.LaserGameMine
        elif gameName == "Roll":
            self.gridGameText = TTLocalizer.LaserGameRoll
        elif gameName == "Avoid":
            self.gridGameText = TTLocalizer.LaserGameAvoid
        elif gameName == "Drag":
            self.gridGameText = TTLocalizer.LaserGameDrag
        else:
            self.gridGameText = TTLocalizer.LaserGameDefault

    def setActiveLF(self, active = 1):
        if active:
            self.activeLF = 1
        else:
            self.activeLF = 0
            
    def setSuccess(self, success):
        if success:
            self.successTrack.start()
        else:
            self.failTrack.start()
            self.cSphereNodePath.setPos(self.blockerX, self.blockerY,0)
        
    def makeGridSymbols(self):
        #blank
        symbolBlank = [(0),(1.0, 0.0, 0.0),()]
        
        #one
        symbolOne = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.45, 0.8),\
                        (0.55, 0.8),\
                        (0.55, 0.2),\
                        (0.45, 0.2),\
                        (0.45, 0.8),)]
                        
        #two
        symbolTwo = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.45),\
                        (0.4, 0.45),\
                        (0.4, 0.3),\
                        (0.7, 0.3),\
                        (0.7, 0.2),\
                        (0.3, 0.2),\
                        (0.3, 0.55),\
                        (0.6, 0.55),\
                        (0.6, 0.7),\
                        (0.3, 0.7),\
                        (0.3, 0.8),)]
                        
        #three
        symbolThree = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.3, 0.2),\
                        (0.3, 0.3),\
                        (0.6, 0.3),\
                        (0.6, 0.45),\
                        (0.4, 0.45),\
                        (0.4, 0.55),\
                        (0.6, 0.55),\
                        (0.6, 0.7),\
                        (0.3, 0.7),\
                        (0.3, 0.8),)]
                        
        #four
        symbolFour = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #FIVE NEED TO FIX
        symbolFive = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #Six
        symbolSix = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #Seven
        symbolSeven = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #Eight
        symbolEight = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #Nine
        symbolNine = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.4, 0.8),\
                        (0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.8),\
                        (0.7, 0.8),\
                        (0.7, 0.2),\
                        (0.6, 0.2),\
                        (0.6, 0.5),\
                        (0.3, 0.5),\
                        (0.3, 0.8),)]
                        
        #basic square
        symbolSquare = [ (None),\
                        (1.0, 0.0, 0.0),\
                        ((0.1, 0.9),\
                        (0.9, 0.9),\
                        (0.9, 0.1),\
                        (0.1, 0.1),\
                        (0.1, 0.9),)]
                        
        #triangle
        symbolTriangle = [(None),\
                        (0.0, 1.0, 0.0),\
                        ((0.1, 0.1),\
                        (0.5, 0.9),\
                        (0.9, 0.1),\
                        (0.1, 0.1),)]
                        
        #blue square
        symbolBlueSquare = [ (None),\
                        (0.3, 0.3, 1.0),\
                        ((0.1, 0.9),\
                        (0.9, 0.9),\
                        (0.9, 0.1),\
                        (0.1, 0.1),\
                        (0.1, 0.9),)]
                        
        #hidden bomb
        symbolHiddenBomb = [ (self.sendFail),\
                        (1.0, 0.0, 0.0),\
                        ((0.1, 0.9),\
                        (0.9, 0.9),\
                        (0.9, 0.1),\
                        (0.1, 0.1),\
                        (0.1, 0.9),)]
        #bomb
        symbolBomb = [ (self.sendFail),\
                        (1.0, 0.0, 0.0),\
                        ((0.8, 1.0),\
                        (1.0, 0.8),\
                        (0.8, 0.6),\
                        (0.8, 0.4),\
                        (0.6, 0.2),\
                        (0.4, 0.2),\
                        (0.2, 0.4),\
                        (0.2, 0.6),\
                        (0.4, 0.8),\
                        (0.6, 0.8),\
                        (0.8, 1.0),)]
                        
        #bomb
        symbolSkull = [ (self.sendFail),\
                        (1.0, 0.0, 0.0),\
                        ((0.5, 0.9),\
                        (0.7, 0.8),\
                        (0.7, 0.6),\
                        (0.6, 0.5),\
                        (0.6, 0.4),\
                        (0.5, 0.4),\
                        (0.5, 0.3),\
                        (0.7, 0.4),\
                        (0.8, 0.4),\
                        (0.8, 0.3),\
                        \
                        (0.7, 0.3),\
                        (0.6, 0.25),\
                        (0.7, 0.2),\
                        (0.8, 0.2),\
                        (0.8, 0.1),\
                        (0.7, 0.1),\
                        (0.5, 0.2),\
                        (0.3, 0.1),\
                        (0.2, 0.1),\
                        (0.2, 0.2),\
                        \
                        (0.3, 0.2),\
                        (0.4, 0.25),\
                        (0.3, 0.3),\
                        (0.2, 0.3),\
                        (0.2, 0.4),\
                        (0.3, 0.4),\
                        (0.5, 0.3),\
                        (0.5, 0.4),\
                        (0.4, 0.4),\
                        (0.4, 0.5),\
                        \
                        (0.3, 0.6),\
                        (0.3, 0.8),\
                        (0.5, 0.9),)]
                        
        #dot
        symbolDot      = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.4, 0.6),\
                        (0.6, 0.6),\
                        (0.6, 0.4),\
                        (0.4, 0.4),\
                        (0.4, 0.6),)]
                        
        #dot
        symbolRedX      = [(None),\
                        (1.0, 0.0, 0.0),\
                        ((0.3, 0.8),\
                        (0.5, 0.6),\
                        (0.7, 0.8),\
                        (0.8, 0.7),\
                        (0.6, 0.5),\
                        (0.8, 0.3),\
                        (0.7, 0.2),\
                        (0.5, 0.4),\
                        (0.3, 0.2),\
                        (0.2, 0.3),\
                        (0.4, 0.5),\
                        (0.2, 0.7),\
                        (0.3, 0.8),)]
                        
        #select
        self.symbolSelect = [ 
                        (1.0, 0.0, 0.0),\
                        ((0.05, 0.95),\
                        (0.95, 0.95),\
                        (0.95, 0.05),\
                        (0.05, 0.05),\
                        (0.05, 0.95),)]
                        
       #dot
        symbolBlueDot      = [(None),\
                        (0.5, 0.5, 1.0),\
                        ((0.5, 0.7),\
                        (0.7, 0.5),\
                        (0.5, 0.3),\
                        (0.3, 0.5),\
                        (0.5, 0.7),)]
                        
        self.gridSymbols = []                
        self.gridSymbols.append(symbolBlank)    #0
        self.gridSymbols.append(symbolOne)      #1
        self.gridSymbols.append(symbolTwo)      #2
        self.gridSymbols.append(symbolThree)    #3
        self.gridSymbols.append(symbolFour)     #4
        self.gridSymbols.append(symbolFive)     #5
        self.gridSymbols.append(symbolSix)      #6
        self.gridSymbols.append(symbolSeven)    #7
        self.gridSymbols.append(symbolEight)    #8
        self.gridSymbols.append(symbolNine)     #9
        self.gridSymbols.append(symbolSquare)   #10
        self.gridSymbols.append(symbolHiddenBomb) #11
        self.gridSymbols.append(symbolSkull)    #12
        self.gridSymbols.append(symbolTriangle) #13
        self.gridSymbols.append(symbolDot) #14
        self.gridSymbols.append(symbolBlueSquare)   #15
        self.gridSymbols.append(symbolRedX)   #16
        self.gridSymbols.append(symbolBlueDot)   #17
        

        
    def sendFail(self):
        #print("Bomb!!!")
        self.battleStart()
        self.sendUpdate('trapFire',[])
        

        
    def battleStart(self):
        self.startBattle()
        
    def __detect(self, task):
        #print "detect beat"
        
        distance = self.centerNode.getDistance(localAvatar)
        greaterDim = self.gridScaleX
        if self.gridScaleY > self.gridScaleX:
            greaterDim = self.gridScaleY
            
        self.detectCount += 1
        if self.detectCount > 5:   
            #print("Range:%s Dimension:%s" % (distance, greaterDim * 0.75))
            self.detectCount = 0
            
        if distance < (greaterDim * 0.75):
            if not self.isToonInRange:
                self.doToonInRange()
            if localAvatar.getPos(self)[0] > 0 \
                and localAvatar.getPos(self)[0] < self.gridScaleX \
                and localAvatar.getPos(self)[1] > 0 \
                and localAvatar.getPos(self)[1] < self.gridScaleY:
                self.__toonHit()
            else:
                if self.isToonIn:
                    self.toonX = -1
                    self.toonY = -1
                    self.isToonIn = 0
                    self.genGrid()
                self.isToonIn = 0
        else:
            if self.isToonInRange:
                self.doToonOutOfRange()

        taskMgr.doMethodLater(0.1, self.__detect, self.detectName)
        return Task.done
        
        
    def doToonInRange(self):
        #print("toon in Range")
        self.isToonInRange = 1
        if self.activeLF:
            #self.cameraHold = base.localAvatar.getIdealCameraPos()
            
            camHeight = base.localAvatar.getClampedAvatarHeight()
            heightScaleFactor = (camHeight * 0.3333333333)
            defLookAt = Point3(0.0, 1.5, camHeight)
                         
            cameraPoint = Point3(0.0, (-20.0 * heightScaleFactor), (camHeight + 8.0))
    
            #base.localAvatar.setCameraSettings(cameraSetting[0])
            base.localAvatar.setIdealCameraPos(cameraPoint)
            self.level.stage.showInfoText(self.gridGameText)
        
    def doToonOutOfRange(self):
        #print("toon out of Range")
        self.isToonInRange = 0
        #base.localAvatar.setIdealCameraPos(self.cameraHold)
        base.localAvatar.setCameraPositionByIndex(base.localAvatar.cameraIndex)
        self.cameraHold = None
        
    def __toonHit(self):
        #print "Toon Hit"
        
        posX = localAvatar.getPos(self)[0] 
        posY = localAvatar.getPos(self)[1]
        tileX = int(posX / (self.gridScaleX / self.gridNumX))
        tileY = int(posY / (self.gridScaleY / self.gridNumY))
        oldX = self.toonX
        oldY = self.toonY
        #print("tile %s %s %s" % (tileX, tileY, self.gridData[tileX][tileY]))
        if (self.toonX != tileX or self.toonY != tileY) or (not self.isToonIn):
            self.toonX = tileX
            self.toonY = tileY
            self.isToonIn = 1
            if self.gridData[tileX][tileY] < len(self.gridSymbols):
                tileFunction = self.gridSymbols[self.gridData[tileX][tileY]][0]
                if tileFunction:
                    tileFunction()
            self.sendHit(self.toonX, self.toonY, oldX, oldY)
            self.genGrid()
        self.isToonIn = 1
        
    def __testTile(self):
        if self.toonX >= 0 and self.toonY >= 0 and self.toonX < self.gridNumX and self.toonY < self.gridNumY:
                if self.gridData[self.toonX][self.toonY] < len(self.gridSymbols):
                    tileFunction = self.gridSymbols[self.gridData[self.toonX][self.toonY]][0]
                    if tileFunction:
                        tileFunction()
        
        
    def sendHit(self, newX, newY, oldX, oldY):
        if self.toonX >= 0:
            self.sendUpdate('hit', [newX, newY, oldX, oldY])
        
    def disable(self):
        self.notify.debug('disable')
        if self.failTrack.isPlaying():
            self.failTrack.finish()
        if self.successTrack.isPlaying():
            self.successTrack.finish()
        # stop things
        self.ignoreAll()
        taskMgr.remove(self.detectName)

            
        BattleBlocker.BattleBlocker.disable(self)

    def delete(self):
        self.notify.debug('delete')
        # unload things
        self.unloadModel()
        BattleBlocker.BattleBlocker.delete(self)
        
    def loadModel(self):
        self.rotateNode = self.attachNewNode('rotate')
        self.model = None
        #self.model = loader.loadModel(self.laserFieldModels[self.modelPath])
        #self.model.reparentTo(self.rotateNode)
        
        self.centerNode = self.attachNewNode('center')
        self.centerNode.setPos(self.gridScaleX * 0.5, self.gridScaleY * 0.5, 0.0)

        #self.createDymnGeom();
        self.genGrid()
        #self.genTrace()
            
    def unloadModel(self):
        if self.model:
            self.model.removeNode()
            del self.model
            self.model = None
            
    def genTrace(self):
        
        wireRed = 1.0
        wireGreen = 0.0
        wireBlue = 0.0
        wireAlpha = 0.5
        
        beamRed = 0.04
        beamGreen = 0.0
        beamBlue = 0.0
        beamAlpha = 0.1
        
        self.gFormat = GeomVertexFormat.getV3cp()
        self.traceWireVertexData = GeomVertexData("holds my vertices", self.gFormat, Geom.UHDynamic)
        self.traceWireVertexWriter = GeomVertexWriter(self.traceWireVertexData, "vertex")
        self.traceWireColorWriter = GeomVertexWriter(self.traceWireVertexData, "color")

        
        self.traceBeamVertexData = GeomVertexData("holds my vertices", self.gFormat, Geom.UHDynamic)
        self.traceBeamVertexWriter = GeomVertexWriter(self.traceBeamVertexData, "vertex")
        self.traceBeamColorWriter = GeomVertexWriter(self.traceBeamVertexData, "color")
        
        self.traceWireVertexWriter.addData3f(self.projector[0], self.projector[1], self.projector[2]) #origin
        self.traceWireColorWriter.addData4f(wireRed, wireGreen, wireBlue, wireAlpha)
        
        self.traceBeamVertexWriter.addData3f(self.projector[0], self.projector[1], self.projector[2]) #origin
        self.traceBeamColorWriter.addData4f(0.0, 0.0, 0.0, 0.0)
        
        for vertex in self.tracePath:
        
                self.traceWireVertexWriter.addData3f(vertex[0] * self.gridScaleX, vertex[1] * self.gridScaleY, self.zFloat)
                self.traceWireColorWriter.addData4f(wireRed, wireGreen, wireBlue, wireAlpha)
                
                self.traceBeamVertexWriter.addData3f(vertex[0] * self.gridScaleX, vertex[1] * self.gridScaleY, self.zFloat)
                self.traceBeamColorWriter.addData4f(beamRed, beamGreen, beamBlue, beamAlpha)
                
        #self.traceWireTris=GeomTriangles(Geom.UHDynamic) # triangle obejcet
        self.traceBeamTris=GeomTriangles(Geom.UHStatic) # triangle obejcet
        self.traceWireTris=GeomLinestrips(Geom.UHStatic) # triangle obejcet
        
        vertexCounter = 1
        
        sizeTrace = len(self.tracePath)
        chainTrace = sizeTrace - 1
        previousTrace = 1
        
        #print ("gen trace")
        for countVertex in range(0, sizeTrace):
            self.traceWireTris.addVertex(countVertex + 1)
        self.traceWireTris.closePrimitive()
            
        for countVertex in range(0, chainTrace):
            self.traceBeamTris.addVertex(0)
            self.traceBeamTris.addVertex(countVertex + 1)
            self.traceBeamTris.addVertex(countVertex + 2)
            self.traceBeamTris.closePrimitive()
        
        self.traceWireGeom=Geom(self.traceWireVertexData)
        self.traceWireGeom.addPrimitive(self.traceWireTris)
        self.traceWireGN.addGeom(self.traceWireGeom)
        
        self.traceBeamGeom=Geom(self.traceBeamVertexData)
        self.traceBeamGeom.addPrimitive(self.traceBeamTris)
        self.traceBeamGN.addGeom(self.traceBeamGeom)

    def createGrid(self):
        #print("CREATING DYNAMIC GEOM")
        
        gridScaleX = self.gridScaleX / self.gridNumX
        gridScaleY = self.gridScaleY / self.gridNumY
        
        red = 0.25
        green = 0.25
        blue = 0.25
        alpha = 0.5
        
        beamRed = 0.04
        beamGreen = 0.04
        beamBlue = 0.04
        beamAlpha = 0.1
        
        
        self.gFormat = GeomVertexFormat.getV3cp()
        self.gridVertexData = GeomVertexData("holds my vertices", self.gFormat, Geom.UHDynamic)
        self.gridVertexWriter = GeomVertexWriter(self.gridVertexData, "vertex")
        self.gridColorWriter = GeomVertexWriter(self.gridVertexData, "color")

        
        self.beamVertexData = GeomVertexData("holds my vertices", self.gFormat, Geom.UHDynamic)
        self.beamVertexWriter = GeomVertexWriter(self.beamVertexData, "vertex")
        self.beamColorWriter = GeomVertexWriter(self.beamVertexData, "color")
        
        self.gridVertexWriter.addData3f(self.projector[0], self.projector[1], self.projector[2]) #origin
        self.gridColorWriter.addData4f(red, green, blue, 0.0)
        
        self.beamVertexWriter.addData3f(self.projector[0], self.projector[1], self.projector[2]) #origin
        self.beamColorWriter.addData4f(0.0, 0.0, 0.0, 0.0)
        
        #import pdb; pdb.set_trace()
        
        #setup the vertexs
        
        border = 0.4
        
        #print("Adding vertexes")
        
        for column in range(0, self.gridNumX):
            columnLeft = 0.0 + gridScaleX * column
            columnRight = columnLeft + gridScaleX
            rowBottom = 0
            for row in range(0, self.gridNumY):
                rowTop = rowBottom + gridScaleY
                if self.gridData[column][row] and self.gridData[column][row] < len(self.gridSymbols):
                    #print("got symbol")
                    gridColor = self.gridSymbols[self.gridData[column][row]][1]
                    gridSymbol = self.gridSymbols[self.gridData[column][row]][2]
                    #print(gridSymbol)
                    sizeSymbol = len(gridSymbol)
                    
                    for iVertex in range(sizeSymbol):
                        vertex = gridSymbol[iVertex]
                        self.gridVertexWriter.addData3f(columnLeft + (vertex[0] * gridScaleX), rowBottom + (vertex[1] * gridScaleY), self.zFloat)
                        self.gridColorWriter.addData4f(gridColor[0] * red, gridColor[1] * green, gridColor[2] * blue, alpha)
                        
                        self.beamVertexWriter.addData3f(columnLeft + (vertex[0] * gridScaleX), rowBottom + (vertex[1] * gridScaleY), self.zFloat)
                        self.beamColorWriter.addData4f(gridColor[0] * beamRed, gridColor[1] * beamGreen, gridColor[2] * beamBlue, beamAlpha)
                rowBottom = rowTop
                
        if self.isToonIn:
            gridSymbol = self.symbolSelect[1]
            gridColor = self.symbolSelect[0]
            sizeSymbol = len(gridSymbol)
            for iVertex in range(sizeSymbol):
                vertex = gridSymbol[iVertex]
                self.gridVertexWriter.addData3f((self.toonX * gridScaleX) + (vertex[0] * gridScaleX), (self.toonY * gridScaleY) + (vertex[1] * gridScaleY), self.zFloat)
                self.gridColorWriter.addData4f(gridColor[0] * red, gridColor[1] * green, gridColor[2] * blue, alpha)
                
                self.beamVertexWriter.addData3f((self.toonX * gridScaleX) + (vertex[0] * gridScaleX), (self.toonY * gridScaleY) + (vertex[1] * gridScaleY), self.zFloat)
                self.beamColorWriter.addData4f(gridColor[0] * beamRed, gridColor[1] * beamGreen, gridColor[2] * beamBlue, beamAlpha)
                    
                
        #create geometry and faces
        self.gridTris=GeomLinestrips(Geom.UHDynamic) # triangle obejcet
        self.beamTris=GeomTriangles(Geom.UHDynamic) # triangle obejcet
        
        #print("Adding faces")
        vertexCounter = 1
        #print("grid data")
        #print self.gridData
        #print("on data")
        for column in range(0, self.gridNumX):
            #print self.gridData[column]
            for row in range(0, self.gridNumY):
                if self.gridData[column][row] and self.gridData[column][row] < len(self.gridSymbols):
                    gridSymbol = self.gridSymbols[self.gridData[column][row]][2]
                    sizeSymbol = len(gridSymbol)
                    for iVertex in range(sizeSymbol):
                        self.gridTris.addVertex(vertexCounter + iVertex)
                    self.gridTris.closePrimitive()
                    for iVertex in range(sizeSymbol -1):
                        self.beamTris.addVertex(0)
                        self.beamTris.addVertex(vertexCounter + iVertex + 0)
                        self.beamTris.addVertex(vertexCounter + iVertex + 1)
                        self.beamTris.closePrimitive()
                    
                    vertexCounter += sizeSymbol
                    
        if self.isToonIn:
            gridSymbol = self.symbolSelect[1]
            sizeSymbol = len(gridSymbol)
            for iVertex in range(sizeSymbol):
                self.gridTris.addVertex(vertexCounter + iVertex)
            self.gridTris.closePrimitive()
            for iVertex in range(sizeSymbol -1):
                self.beamTris.addVertex(0)
                self.beamTris.addVertex(vertexCounter + iVertex + 0)
                self.beamTris.addVertex(vertexCounter + iVertex + 1)
                self.beamTris.closePrimitive()
                
        self.wireGeom=Geom(self.gridVertexData)
        self.wireGeom.addPrimitive(self.gridTris)
        self.gridWireGN.addGeom(self.wireGeom)
        
        self.beamGeom=Geom(self.beamVertexData)
        self.beamGeom.addPrimitive(self.beamTris) 
        self.gridBeamGN.addGeom(self.beamGeom)

        
    def setGrid(self, gridNumX, gridNumY):
        #print("setGrid")
        self.gridNumX = gridNumX
        self.gridNumY = gridNumY
        #self.gridScaleX = gridScale
        #self.gridScaleY = gridScale
        
        self.gridData = []
        for i in range(0 ,gridNumX):
            self.gridData.append([0] * gridNumY)
        self.genGrid()
            
        
    def getGrid(self):
        return self.gridNumX, self.gridNumY
        
    def setGridScaleX(self, gridScale):
        self.gridScaleX = gridScale
        self.centerNode.setPos(self.gridScaleX * 0.5, self.gridScaleY * 0.5, 0.0)
        self.blockerX = self.gridScaleX * 0.5
        self.cSphereNodePath.setPos(self.blockerX, self.blockerY,self.blockerZ)
        self.genGrid()
        
    def setGridScaleY(self, gridScale):
        self.gridScaleY = gridScale
        self.centerNode.setPos(self.gridScaleX * 0.5, self.gridScaleY * 0.5, 0.0)
        self.blockerY = self.gridScaleY
        self.cSphereNodePath.setPos(self.blockerX, self.blockerY,self.blockerZ)
        self.genGrid()
        
        
    def setField(self, fieldData):
        if fieldData[0] != self.gridNumX or fieldData[1] != self.gridNumY:
            self.setGrid(fieldData[0], fieldData[1])
        fieldCounter = 2;
        for column in range(0 ,self.gridNumX):
            for row in range(0 ,self.gridNumY):
                if len(fieldData) > fieldCounter:
                    self.gridData[column][row] = fieldData[fieldCounter]
                    fieldCounter += 1
        #print("set field")
        #print fieldData
        #print self.gridData
        self.genGrid()
        self.__testTile()
        #self.sendHit()
        
                    
    def getField(self):
        fieldData.append(self.game.gridNumX)
        fieldData.append(self.game.gridNumY)
        fieldData = []
        for column in range(0 ,self.game.gridNumX):
            for row in range(0 ,self.game.gridNumY):
                    fieldData.append(self.game.gridData[column][row])
        return fieldData
        
    def setSeed(self, seed):
        #print("setting seed")
        self.gridSeed = seed
        random.seed(seed)
        for column in range(0, self.gridNumX):
            #print self.gridData
            for row in range(0, self.gridNumY):
                rint = random.randint(0,2)
                self.gridData[column][row] = rint
                #print rint
        #print self.gridData
                    
        self.genGrid()
        
    def getSeed(self):
        return self.gridSeed
        
    def setMode(self, mode):
        self.mode = mode
        
    def getMode(self):
        return self.mode
        
    def setProjector(self, projPoint):
        self.projector = projPoint
        if self.gridWireGN and self.gridBeamGN:
            self.genGrid()
        
        
    def genGrid(self):
        if self.activeLF:
            #print("Gen Grid Size %s %s" % (self.gridScaleX, self.gridScaleY))
            if self.gridWireGN:
                self.gridWireGN.removeAllGeoms()
            if self.gridBeamGN:
                self.gridBeamGN.removeAllGeoms()
            if self.gridWireGN and self.gridBeamGN:
                self.createGrid()
                #print("gen grid succeeded")
            else:
                pass
                #print("gen grid failed")
            
    def hideSuit(self, suitIdarray):
        #print("hiding suits %s" % (suitIdarray))
        for suitId in suitIdarray:
            #suit = base.cr.doId2do[suitId]
            suit = base.cr.doId2do.get(suitId)
            if suit:
                #suit.setPos(suit.getPos()[0], suit.getPos()[1], suit.getPos()[2] - 1000.0)
                suit.stash()
                #suit.hide()
                #suit.ignoreCollisions() #this doesn't exist
            else:
                #print("warning no suit")
                pass
                
    def showSuit(self, suitIdarray):
        #print("showing suits %s" % (suitIdarray))
        for suitId in suitIdarray:
            suit = base.cr.doId2do.get(suitId)
            #suit = base.cr.doId2do[suitId]
            if suit:
                #suit.setPos(suit.getPos()[0], suit.getPos()[1], suit.getPos()[2] + 1000.0)
                suit.unstash()
                suit.setVirtual()
                #suit.show()
                #suit.unignoreCollisions() #this doesn't exist
            else:
                #print("warning no suit")
                pass
                
    def initCollisionGeom(self):
        print("Laser Field initCollisionGeom")
        self.blockerX = self.gridScaleX * 0.5
        self.blockerY = self.gridScaleY
        self.cSphere = CollisionSphere(0, 0, 0 ,self.blockerX)
        self.cSphereNode = CollisionNode("battleBlocker-%s-%s" %
                                         (self.level.getLevelId(), self.entId))
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.setPos(self.blockerX, self.blockerY,self.blockerZ)
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.cSphere.setTangible(0)

        self.enterEvent = "enter" + self.cSphereNode.getName()
        self.accept(self.enterEvent, self.__handleToonEnter)
        
    def __handleToonEnter(self, collEntry):
        self.notify.debug ("__handleToonEnter, %s" % self.entId)
        self.startBattle()
            
        

        
            
    
