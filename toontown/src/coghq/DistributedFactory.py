from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import random
from otp.level import DistributedLevel
from direct.directnotify import DirectNotifyGlobal
import FactoryBase
import FactoryEntityCreator
import FactorySpecs
from otp.level import LevelSpec
from otp.level import LevelConstants
from toontown.toonbase import TTLocalizer
from toontown.coghq import FactoryCameraViews
if __dev__:
    from otp.level import EditorGlobals

class DistributedFactory(DistributedLevel.DistributedLevel,
                         FactoryBase.FactoryBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFactory')

    def __init__(self, cr):
        DistributedLevel.DistributedLevel.__init__(self, cr)
        FactoryBase.FactoryBase.__init__(self)

        self.suitIds = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        self.suitsInitialized = 0
        self.goonClipPlanes = {}
        
    def createEntityCreator(self):
        return FactoryEntityCreator.FactoryEntityCreator(level=self)

    def generate(self):
        self.notify.debug('generate')
        DistributedLevel.DistributedLevel.generate(self)

        # add special camera views
        self.factoryViews = FactoryCameraViews.FactoryCameraViews(self)

        # add factory menu to SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.addFactoryMenu()

        if __debug__:
            # add a handle for debugging
            base.factory = self
        if __dev__:
            bboard.post(EditorGlobals.EditTargetPostName, self)

        self.accept('SOSPanelEnter', self.handleSOSPanel)

    def delete(self):
        DistributedLevel.DistributedLevel.delete(self)
        # remove factory menu from SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.removeFactoryMenu()
        # remove special camera views
        self.factoryViews.delete()
        del self.factoryViews
        self.ignore('SOSPanelEnter')
        if __debug__:
            del base.factory
        if __dev__:
            bboard.removeIfEqual(EditorGlobals.EditTargetPostName, self)
        
    # required fields
    def setFactoryId(self, id):
        FactoryBase.FactoryBase.setFactoryId(self, id)

    def setForemanConfronted(self, avId):
        assert avId in self.avIdList
        if avId == base.localAvatar.doId:
            return
        av = base.cr.identifyFriend(avId)
        if av is None:
            return
        base.localAvatar.setSystemMessage(
            avId, TTLocalizer.ForemanConfrontedMsg % av.getName())

    def setDefeated(self):
        self.notify.info('setDefeated')
        # foreman has been defeated
        messenger.send('FactoryWinEvent')

    def levelAnnounceGenerate(self):
        self.notify.debug('levelAnnounceGenerate')
        DistributedLevel.DistributedLevel.levelAnnounceGenerate(self)

        # create our spec
        # NOTE: in dev, the AI will probably send us another spec to use
        specModule = FactorySpecs.getFactorySpecModule(self.factoryId)
        factorySpec = LevelSpec.LevelSpec(specModule)
        if __dev__:
            # give the spec a factory EntityTypeRegistry.
            typeReg = self.getEntityTypeReg()
            factorySpec.setEntityTypeReg(typeReg)
        
        DistributedLevel.DistributedLevel.initializeLevel(self, factorySpec)

        # if the AI is sending us a spec, we won't have it yet and the
        # level isn't really initialized yet. So we can't assume that we
        # can start doing stuff here. Much of what used to be here
        # has been moved to FactoryLevelMgr, where it really belongs, but...
        # this could be cleaner.

    def privGotSpec(self, levelSpec):
        # OK, we've got the spec that we're going to use, either the one
        # we provided or the one from the AI. When we call down, the level
        # is going to be initialized, and all the local entities will be
        # created.
        if __dev__:
            # First, give the spec a factory EntityTypeRegistry if it doesn't
            # have one.
            if not levelSpec.hasEntityTypeReg():
                typeReg = self.getEntityTypeReg()
                levelSpec.setEntityTypeReg(typeReg)

        # get this event name before we init the factory
        firstSetZoneDoneEvent = self.cr.getNextSetZoneDoneEvent()
        # wait until the first viz setZone completes before announcing
        # that we're ready to go
        def handleFirstSetZoneDone():
            # NOW we're ready.
            base.factoryReady = 1
            messenger.send('FactoryReady')
        self.acceptOnce(firstSetZoneDoneEvent, handleFirstSetZoneDone)

        # I think this is a reasonable number to use for the model count
        modelCount = len(levelSpec.getAllEntIds())
        loader.beginBulkLoad(
            "factory",
            (TTLocalizer.HeadingToFactoryTitle %
             TTLocalizer.FactoryNames[self.factoryId]),
            modelCount, 1, TTLocalizer.TIP_COGHQ)
        # let 'er rip.
        DistributedLevel.DistributedLevel.privGotSpec(self, levelSpec)
        loader.endBulkLoad("factory")

        def printPos(self=self):
            # print position of localToon relative to the zone that he's in
            pos = base.localAvatar.getPos(self.getZoneNode(self.lastToonZone))
            h = base.localAvatar.getH(self.getZoneNode(self.lastToonZone))
            print 'factory pos: %s, h: %s, zone %s' % (
                repr(pos), h, self.lastToonZone)
            posStr = "X: %.3f" % pos[0] + "\nY: %.3f" % pos[1] + \
                  "\nZ: %.3f" % pos[2] + "\nH: %.3f" % h + \
                  "\nZone: %s" % str(self.lastToonZone)
            base.localAvatar.setChatAbsolute(posStr,CFThought|CFTimeout)
        self.accept('f2',printPos)

        base.localAvatar.setCameraCollisionsCanMove(1)

        # our place will gen this event BEFORE we leave the factory.
        # We need to let the AI know that we've left; if everyone leaves,
        # the AI will destroy the factory.
        self.acceptOnce('leavingFactory', self.announceLeaving)

    def handleSOSPanel(self, panel):
        # make a list of toons that are still in the factory
        avIds = []
        for avId in self.avIdList:
            # if a toon dropped and came back into the game, they won't
            # be in the factory, so they won't be in the doId2do.
            if base.cr.doId2do.get(avId):
                avIds.append(avId)
        panel.setFactoryToonIdList(avIds)

    def disable(self):
        self.notify.debug('disable')

        base.localAvatar.setCameraCollisionsCanMove(0)

        if hasattr(self, 'suits'):
            del self.suits

        if (hasattr(self, 'relatedObjectMgrRequest')
                and self.relatedObjectMgrRequest):
            self.cr.relatedObjectMgr.abortRequest(self.relatedObjectMgrRequest)
            del self.relatedObjectMgrRequest

        DistributedLevel.DistributedLevel.disable(self)

    def setSuits(self, suitIds, reserveSuitIds):
        assert(self.notify.debug("setSuits suits: %s, reserves: %s" % (suitIds, reserveSuitIds)))
        oldSuitIds = list(self.suitIds)
        self.suitIds = suitIds
        self.reserveSuitIds = reserveSuitIds

        # which cogs are coming out of reserve?
        newSuitIds = []
        for suitId in self.suitIds:
            if suitId not in oldSuitIds:
                newSuitIds.append(suitId)
        if len(newSuitIds):
            def bringOutOfReserve(suits):
                assert(self.notify.debug('bringOutOfReserve suits=%s' % suits))
                for suit in suits:
                    if suit:
                        suit.comeOutOfReserve()
            assert not hasattr(self, 'relatedObjectMgrRequest')
            assert(self.notify.debug('requesting Objects %s' % newSuitIds))
            self.relatedObjectMgrRequest = self.cr.relatedObjectMgr.requestObjects(
                    newSuitIds, bringOutOfReserve)

    def reservesJoining(self):
        assert(self.notify.debug("reservesJoining"))
        # play track reserves joining battle
        pass

    def getCogSpec(self, cogId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.factoryId)
        return cogSpecModule.CogData[cogId]

    def getReserveCogSpec(self, cogId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.factoryId)
        return cogSpecModule.ReserveCogData[cogId]

    def getBattleCellSpec(self, battleCellId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.factoryId)
        return cogSpecModule.BattleCells[battleCellId]

    def getFloorOuchLevel(self):
        return 2

    def getGoonPathId(self):
        return 'sellbotFactory'

    def getTaskZoneId(self):
        return self.factoryId

    def getBossTaunt(self):
        return TTLocalizer.FactoryBossTaunt
    def getBossBattleTaunt(self):
        return TTLocalizer.FactoryBossBattleTaunt
    
