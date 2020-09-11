"""GearEntity module: contains the GearEntity class"""

from direct.interval.IntervalGlobal import *
from otp.level import BasicEntities
import MovingPlatform
from pandac.PandaModules import Vec3

class GearEntity(BasicEntities.NodePathEntity):
    ModelPaths = {
        'factory': 'phase_9/models/cogHQ/FactoryGearB',
        'mint': 'phase_10/models/cashbotHQ/MintGear',
        }
    def __init__(self, level, entId):
        self.modelType = 'factory'
        self.entInitialized = False
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.entInitialized = True
        self.initGear()

    def destroy(self):
        self.destroyGear()
        BasicEntities.NodePathEntity.destroy(self)

    def initGear(self):
        # guard against re-entry; we call self.setScale in here, which in
        # turn calls initGear
        if hasattr(self, 'in_initGear'):
            return
        # set the sentry
        self.in_initGear = True
        
        self.destroyGear()
        model = loader.loadModel(GearEntity.ModelPaths[self.modelType])
        self.gearParent = self.attachNewNode('gearParent-%s' % self.entId)

        if self.orientation == 'horizontal':
            # stash vertical collisions
            vertNodes = model.findAllMatches(
                '**/VerticalCollisions')
            for node in vertNodes:
                node.stash()
            mPlat = MovingPlatform.MovingPlatform()
            # this should be collHorizontalFloor...
            mPlat.setupCopyModel(self.getParentToken(), model,
                                 'HorizontalFloor')
            model = mPlat
        else:
            # stash horizontal collisions
            horizNodes = model.findAllMatches(
                '**/HorizontalCollisions')
            for node in horizNodes:
                node.stash()
            # put the model origin in the center (inside) of the gear
            model.setZ(.15)
            model.flattenLight()

        model.setScale(self.gearScale)
        # get rid of any scales, so the toon doesn't freak out when
        # parented to us
        model.flattenLight()
        # incorporate the gear's overall scale
        model.setScale(self.getScale())
        self.setScale(1)
        model.flattenLight()

        if self.orientation == 'vertical':
            # stand the gear up
            self.gearParent.setP(-90)
        self.model = model
        self.model.reparentTo(self.gearParent)

        # start the rotation ival
        self.startRotate()

        # get rid of the sentry
        del self.in_initGear

    def destroyGear(self):
        self.stopRotate()

        if hasattr(self, 'model'):
            if isinstance(self.model, MovingPlatform.MovingPlatform):
                self.model.destroy()
            else:
                self.model.removeNode()
            del self.model

        if hasattr(self, 'gearParent'):
            self.gearParent.removeNode()
            del self.gearParent

    def startRotate(self):
        self.stopRotate()
        try:
            ivalDur = 360./self.degreesPerSec
        except ZeroDivisionError:
            pass
        else:
            hOffset = 360.
            if ivalDur < 0.:
                ivalDur = -ivalDur
                hOffset = -hOffset
            self.rotateIval = LerpHprInterval(self.model, ivalDur,
                                              Vec3(hOffset,0,0),
                                              startHpr=Vec3(0,0,0),
                                              name='gearRot-%s' % self.entId)
            self.rotateIval.loop()
            self.rotateIval.setT(
                (globalClock.getFrameTime() - self.level.startTime) +
                (ivalDur * self.phaseShift))

    def stopRotate(self):
        if hasattr(self, 'rotateIval'):
            self.rotateIval.pause()
            del self.rotateIval

    if __dev__:
        def setDegreesPerSec(self, degreesPerSec):
            if self.entInitialized:
                self.degreesPerSec = degreesPerSec
                self.startRotate()

        def setPhaseShift(self, phaseShift):
            if self.entInitialized:
                self.phaseShift = phaseShift
                self.startRotate()

        def attribChanged(self, attrib, value):
            self.destroyGear()
            self.initGear()

        # make sure to intercept scale changes so we can flatten the scale
        def setScale(self, *args):
            BasicEntities.NodePathEntity.setScale(self, *args)
            if self.entInitialized:
                self.initGear()
        def setSx(self, *args):
            BasicEntities.NodePathEntity.setSx(self, *args)
            if self.entInitialized:
                self.initGear()
        def setSy(self, *args):
            BasicEntities.NodePathEntity.setSy(self, *args)
            if self.entInitialized:
                self.initGear()
        def setSz(self, *args):
            BasicEntities.NodePathEntity.setSz(self, *args)
            if self.entInitialized:
                self.initGear()
