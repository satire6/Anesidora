from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import random
from otp.level import DistributedLevel
from direct.directnotify import DirectNotifyGlobal
import LawOfficeBase
import FactoryEntityCreator
import FactorySpecs
from otp.level import LevelSpec
from otp.level import LevelConstants
from toontown.toonbase import TTLocalizer
from toontown.coghq import FactoryCameraViews
from direct.distributed.DistributedObject import DistributedObject

if __dev__:
    from otp.level import EditorGlobals

class DistributedLawOffice(DistributedObject,
                         LawOfficeBase.LawOfficeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawOffice')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        LawOfficeBase.LawOfficeBase.__init__(self)

        self.suitIds = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        self.suitsInitialized = 0
        self.goonClipPlanes = {}
        self.level = None
        


    def generate(self):
        self.notify.debug('generate')
        self.accept('lawOfficeFloorDone', self.handleFloorDone)
        

    def delete(self):
        #self.level.delete(self)
        # remove factory menu from SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.removeFactoryMenu()

        self.ignore('lawOfficeFloorDone')
        if __debug__:
            del base.factory

        
    # required fields
    def setLawOfficeId(self, id):
        LawOfficeBase.LawOfficeBase.setLawOfficeId(self, id)

 

    def levelAnnounceGenerate(self):
        self.notify.debug('levelAnnounceGenerate')
        #where it really belongs, but...
        # this could be cleaner.



    def handleSOSPanel(self, panel):
        # make a list of toons that are still in the factory
        avIds = []
        for avId in self.avIdList:
            # if a toon dropped and came back into the game, they won't
            # be in the factory, so they won't be in the doId2do.
            if base.cr.doId2do.get(avId):
                avIds.append(avId)
        panel.setFactoryToonIdList(avIds)
        
    def handleFloorDone(self):
        self.sendUpdate("readyForNextFloor")

    def disable(self):
        self.notify.debug('disable')

        base.localAvatar.setCameraCollisionsCanMove(0)



    def getTaskZoneId(self):
        return self.lawOfficeId
        
    def startSignal(self):
        base.camera.setScale(base.localAvatar.getScale())
        localAvatar.setCameraFov(DefaultCameraFov)
        base.camera.clearMat()
        pass


