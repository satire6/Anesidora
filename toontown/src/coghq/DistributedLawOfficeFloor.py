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

if __dev__:
    from otp.level import EditorGlobals

class DistributedLawOfficeFloor(DistributedLevel.DistributedLevel,
                         LawOfficeBase.LawOfficeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawOffice')

    def __init__(self, cr):
        DistributedLevel.DistributedLevel.__init__(self, cr)
        LawOfficeBase.LawOfficeBase.__init__(self)

        self.suitIds = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        self.suitsInitialized = 0
        self.goonClipPlanes = {}
        
    def createEntityCreator(self):
        return FactoryEntityCreator.FactoryEntityCreator(level=self)

    def generate(self):
        #print("LAW OFFICE FLOOR GENERATE")
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
        #self.accept('lawOfficeFloorDone', self.handleFloorDone)
        
        #print("local Avatar Position %s" % (base.localAvatar.getPos()))
        #base.localAvatar.setPos(0,0,0)
        #import pdb; pdb.set_trace()
        
        
        

    def delete(self):
        #print("LAW OFFICE FLOOR DELETE")
        
        DistributedLevel.DistributedLevel.delete(self)
        
        # remove factory menu from SpeedChat
        base.localAvatar.chatMgr.chatInputSpeedChat.removeFactoryMenu()
        # remove special camera views
        self.factoryViews.delete()
        del self.factoryViews
        self.ignore('SOSPanelEnter')
        if __debug__:
            base.factory = None
        if __dev__:
            bboard.removeIfEqual(EditorGlobals.EditTargetPostName, self)
       
        
    # required fields
    def setLawOfficeId(self, id):
        LawOfficeBase.LawOfficeBase.setLawOfficeId(self, id)

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
        #print("LEVEL ANNOUNCE GENERATE")
        self.notify.debug('levelAnnounceGenerate')
        #import pdb; pdb.set_trace() # toon detached by here
        DistributedLevel.DistributedLevel.levelAnnounceGenerate(self)

        # create our spec
        # NOTE: in dev, the AI will probably send us another spec to use
        specModule = FactorySpecs.getFactorySpecModule(self.lawOfficeId)
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
        #import pdb; pdb.set_trace() 
        #print("LEVEL ANNOUNCE GENERATE DONE") #toon detached by here
        
        

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
             TTLocalizer.FactoryNames[self.lawOfficeId]),
            modelCount, 1, TTLocalizer.TIP_COGHQ)
        # let 'er rip.
        DistributedLevel.DistributedLevel.privGotSpec(self, levelSpec)
        loader.endBulkLoad("factory")
        messenger.send("LawOffice_Spec_Loaded")

        def printPos(self=self):
            # print position of localToon relative to the zone that he's in
            pos = base.localAvatar.getPos(self.getZoneNode(self.lastToonZone))
            h = base.localAvatar.getH(self.getZoneNode(self.lastToonZone))
            print 'factory pos: %s, h: %s, zone %s' % (
                repr(pos), h, self.lastToonZone)
            posStr = "X: %.3f" % pos[0] + "\nY: %.3f" % pos[1] + \
                  "\nZ: %.3f" % pos[2] + "\nH: %.3f" % h + \
                  "\nZone: %s" % str(self.lastToonZone)
            base.localAvatar.setChat(posStr,CFThought,0)
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
        
    def handleFloorDone(self):
        self.sendUpdate("readyForNextFloor")

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
                for suit in suits:
                    suit.comeOutOfReserve()
            assert not hasattr(self, 'relatedObjectMgrRequest')
            self.relatedObjectMgrRequest = self.cr.relatedObjectMgr.requestObjects(
                    newSuitIds, bringOutOfReserve)

    def reservesJoining(self):
        assert(self.notify.debug("reservesJoining"))
        # play track reserves joining battle
        pass

    def getCogSpec(self, cogId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.lawOfficeId)
        return cogSpecModule.CogData[cogId]

    def getReserveCogSpec(self, cogId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.lawOfficeId)
        return cogSpecModule.ReserveCogData[cogId]

    def getBattleCellSpec(self, battleCellId):
        cogSpecModule = FactorySpecs.getCogSpecModule(self.lawOfficeId)
        return cogSpecModule.BattleCells[battleCellId]

    def getFloorOuchLevel(self):
        return 2

    def getGoonPathId(self):
        return 'sellbotFactory'

    def getTaskZoneId(self):
        return self.lawOfficeId

    def getBossTaunt(self):
        return TTLocalizer.FactoryBossTaunt
    def getBossBattleTaunt(self):
        return TTLocalizer.FactoryBossBattleTaunt
        
    def placeLocalToon(self):
        initialZoneEnt = None
        # the entrancePoint entities register themselves with us
        if self.entranceId in self.entranceId2entity:
            epEnt = self.entranceId2entity[self.entranceId]
            #epEnt.placeToon(base.localAvatar,
            #                self.avIdList.index(base.localAvatar.doId),
            #                len(self.avIdList))
            initialZoneEnt = self.getEntity(epEnt.getZoneEntId())
        elif self.EmulateEntrancePoint:
            self.notify.debug('unknown entranceId %s' % self.entranceId)
            #base.localAvatar.reparentTo(render)
            #base.localAvatar.setPosHpr(0,0,0,0,0,0)
            self.notify.debug('showing all zones')
            self.setColorZones(1)
            # put the toon in a random zone to start
            zoneEntIds = list(self.entType2ids['zone'])
            zoneEntIds.remove(LevelConstants.UberZoneEntId)
            if len(zoneEntIds):
                zoneEntId = random.choice(zoneEntIds)
                initialZoneEnt = self.getEntity(zoneEntId)
                #base.localAvatar.setPos(
                #    render,
                #    initialZoneEnt.getZoneNode().getPos(render))
            else:
                initialZoneEnt = self.getEntity(
                    LevelConstants.UberZoneEntId)
                #base.localAvatar.setPos(render,0,0,0)

        if initialZoneEnt is not None:
            # kickstart the visibility
            self.enterZone(initialZoneEnt.entId)

    
