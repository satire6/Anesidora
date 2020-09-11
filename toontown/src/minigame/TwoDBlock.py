""" TwoDBlock.py: contains the TwoDBlock class """

from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from otp.level import BasicEntities 
from toontown.coghq import MovingPlatform
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import ToonBlitzGlobals

class TwoDBlock(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDBlock')

    def __init__(self, model, index, blockAttribs):
        assert self.notify.debugStateCall(self)
        
        self.moveIval = None
        self.isMovingBlock = False
##        self.model = model
        self.index = index
        
        self.createNewBlock(model, blockAttribs)
    
    def destroy(self):
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
        if self.platform:
            if self.isMovingBlock:
                self.platform.destroy()
            del self.platform
        
    def createNewBlock(self, model, blockAttribs):
        # Do this when you have different block models in one maya file.
        initX, initY, initZ, initH, initP, initR = 0,0,0,0,0,0
        finalX, finalY, finalZ, finalH, finalP, finalR = 0,0,0,0,0,0
        
        blockType = blockAttribs[0]
        typeAttribs = ToonBlitzGlobals.BlockTypes[blockType]
        # Setting block name
        blockName = blockType + '-' + str(self.index)
        self.model = NodePath(blockName)
        
        # Setting type attributes
        # Note: Scale can only be a attribute of a block type. 
        # Individual blocks cannot be scaled as when you like. 
        typeX, typeY, typeZ = typeAttribs[1]
        typeH, typeP, typeR = typeAttribs[2]
        scaleX, scaleY, scaleZ = typeAttribs[3]
        model.setScale(scaleX, scaleY, scaleZ)
        
        # Setting block attributes
        blockPosAttribs = blockAttribs[1]
        initX, initY, initZ = blockPosAttribs[0]
        if (len(blockPosAttribs) == 3):
            self.isMovingBlock = True
            finalX, finalY, finalZ = blockPosAttribs[1]
            posIvalDuration = blockPosAttribs[2]
        
        if (len(blockAttribs) == 3):
            # Block has hpr mentioned in it
            blockHprAttribs = blockAttribs[2]
            initH, initP, initR = blockHprAttribs[0]
            if (len(blockHprAttribs) == 3):
                self.isMovingBlock = True
                finalH, finalP, finalR = blockHprAttribs[1]
                hprIvalDuration = blockHprAttribs[2]
        
        if self.isMovingBlock:
            # Create moving platform
            self.platform = MovingPlatform.MovingPlatform()
            self.platform.setupCopyModel(blockName, model)
            self.platform.reparentTo(self.model)
            
            # Setup the interval that makes the block move back and forth between initPos and finalPos
            self.clearMoveIval()
            forwardIval = LerpPosInterval(self.model, posIvalDuration, 
                                          pos = Point3(finalX, finalY, finalZ),
                                          startPos = Point3(initX, initY, initZ),
                                          name='%s-moveFront' % self.platform.name,
                                          fluid = 1)
            backwardIval = LerpPosInterval(self.model, posIvalDuration, 
                                          pos = Point3(initX, initY, initZ),
                                          startPos = Point3(finalX, finalY, finalZ),
                                          name='%s-moveBack' % self.platform.name,
                                          fluid = 1)
            self.moveIval = Sequence(forwardIval, backwardIval)
            
            # @TODO: Make a self.rotateIval with a LerpHprInterval using initH, initP, initR, finalH, finalP, finalR
            # So far we don't have any rotating blocks
        else:
            # Create stationary block
            self.platform = model.copyTo(self.model)
        
        self.model.flattenLight()            
        self.model.setPos(typeX + initX, typeY + initY, typeZ + initZ)
        self.model.setHpr(typeH + initH, typeP + initP, typeR + initR)
        
    def clearMoveIval(self):
        """Cleanup the block move interval."""
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
        self.moveIval = None
        
    def start(self, elapsedTime):
        if self.moveIval:
            self.moveIval.loop()
            self.moveIval.setT(elapsedTime)
            
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        if self.moveIval:
            self.moveIval.pause()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        if self.moveIval:
            self.moveIval.resume()