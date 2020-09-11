from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import random
from otp.level import DistributedLevel
from direct.directnotify import DirectNotifyGlobal
import MintRoomBase, MintRoom
import FactoryEntityCreator
import MintRoomSpecs
from otp.level import LevelSpec, LevelConstants
from toontown.toonbase import TTLocalizer
if __dev__:
    from otp.level import EditorGlobals

# gives you the name of the bboard posting that will be made when a room is
# ready for business
def getMintRoomReadyPostName(doId):
    return 'mintRoomReady-%s' % doId

class DistributedMintRoom(DistributedLevel.DistributedLevel,
                          MintRoomBase.MintRoomBase, MintRoom.MintRoom):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMintRoom')

    # Any non-entrance mint room will not have an entrancePoint entity.
    EmulateEntrancePoint = False
    
    def __init__(self, cr):
        DistributedLevel.DistributedLevel.__init__(self, cr)
        MintRoomBase.MintRoomBase.__init__(self)
        MintRoom.MintRoom.__init__(self)

        self.suitIds = []
        self.suits = []
        self.reserveSuits = []
        self.joiningReserves = []
        self.suitsInitialized = 0
        self.goonClipPlanes = {}
        self.mint = None

    def createEntityCreator(self):
        return FactoryEntityCreator.FactoryEntityCreator(level=self)

    def generate(self):
        self.notify.debug('generate')
        DistributedLevel.DistributedLevel.generate(self)

    def delete(self):
        del self.mint
        DistributedLevel.DistributedLevel.delete(self)
        MintRoom.MintRoom.delete(self)
        self.ignoreAll()
        
    # required fields
    def setMintId(self, mintId):
        self.notify.debug('mintId: %s' % mintId)
        MintRoomBase.MintRoomBase.setMintId(self, mintId)

    def setRoomId(self, roomId):
        self.notify.debug('roomId: %s' % roomId)
        MintRoomBase.MintRoomBase.setRoomId(self, roomId)

    def setRoomNum(self, num):
        self.notify.debug('roomNum: %s' % num)
        MintRoom.MintRoom.setRoomNum(self, num)

    def levelAnnounceGenerate(self):
        self.notify.debug('levelAnnounceGenerate')
        DistributedLevel.DistributedLevel.levelAnnounceGenerate(self)

        # create our spec
        # NOTE: in dev, the AI will probably send us another spec to use
        specModule = MintRoomSpecs.getMintRoomSpecModule(self.roomId)
        roomSpec = LevelSpec.LevelSpec(specModule)
        if __dev__:
            # give the spec a factory EntityTypeRegistry.
            typeReg = self.getMintEntityTypeReg()
            roomSpec.setEntityTypeReg(typeReg)
        
        DistributedLevel.DistributedLevel.initializeLevel(self, roomSpec)

        # if the AI is sending us a spec, we won't have it yet and the
        # level isn't really initialized yet. So we can't assume that we
        # can start doing stuff here. Much of what used to be here
        # has been moved to FactoryLevelMgr, where it really belongs, but...
        # this could be cleaner.

    def getReadyPostName(self):
        return getMintRoomReadyPostName(self.doId)

    def privGotSpec(self, levelSpec):
        # OK, we've got the spec that we're going to use, either the one
        # we provided or the one from the AI. When we call down, the level
        # is going to be initialized, and all the local entities will be
        # created.
        if __dev__:
            # First, give the spec a factory EntityTypeRegistry if it doesn't
            # have one.
            if not levelSpec.hasEntityTypeReg():
                typeReg = self.getMintEntityTypeReg()
                levelSpec.setEntityTypeReg(typeReg)

        # let 'er rip.
        DistributedLevel.DistributedLevel.privGotSpec(self, levelSpec)

        MintRoom.MintRoom.enter(self)

        # our place will gen this event BEFORE we leave the mint.
        # We need to let the AI know that we've left; if everyone leaves,
        # the AI will destroy the mint.
        self.acceptOnce('leavingMint', self.announceLeaving)

        # announce that we're ready
        bboard.post(self.getReadyPostName())

    def fixupLevelModel(self):
        # the level is giving us a chance to modify the room geom before
        # entities get placed. Set up the floor collisions now.
        MintRoom.MintRoom.setGeom(self, self.geom)
        MintRoom.MintRoom.initFloorCollisions(self)

    def setMint(self, mint):
        # the mint gives us a ref to it after we're all set up
        self.mint = mint

    def setBossConfronted(self, avId):
        assert avId in self.avIdList
        self.mint.setBossConfronted(avId)

    def setDefeated(self):
        self.notify.info('setDefeated')
        # boss has been defeated
        from toontown.coghq import DistributedMint
        messenger.send(DistributedMint.DistributedMint.WinEvent)

    # for now, let's ignore visibility, since we may not even need it
    def initVisibility(self, *args, **kw):
        pass
    def shutdownVisibility(self, *args, **kw):
        pass
    def lockVisibility(self, *args, **kw):
        pass
    def unlockVisibility(self, *args, **kw):
        pass
    def enterZone(self, *args, **kw):
        pass
    def updateVisibility(self, *args, **kw):
        pass
    def setVisibility(self, *args, **kw):
        pass
    def resetVisibility(self, *args, **kw):
        pass
    def handleVisChange(self, *args, **kw):
        pass
    def forceSetZoneThisFrame(self, *args, **kw):
        pass

    def getParentTokenForEntity(self, entId):
        # we override this in order to differentiate the parenting tokens for
        # mint-room entities, since multiple mint rooms will be present on
        # the client simultaneously, and we don't want them clashing.

        # this leaves room for 100 editor users, and about 40 rooms.
        if __dev__:
            assert len(EditorGlobals.username2entIdBase) < 100
        assert self.roomNum < 40
        return (1000000 * self.roomNum) + entId

    # states for 'localToon present' FSM
    def enterLtNotPresent(self):
        MintRoom.MintRoom.enterLtNotPresent(self)
        # called when localToon is no longer in this room
        if __dev__:
            # announce that we're no longer available for editing
            bboard.removeIfEqual(EditorGlobals.EditTargetPostName, self)
        self.ignore('f2')

    def enterLtPresent(self):
        MintRoom.MintRoom.enterLtPresent(self)
        # called when localToon is in this room
        if __dev__:
            # announce that we're available for editing
            bboard.post(EditorGlobals.EditTargetPostName, self)

        if self.mint is not None:
            self.mint.currentRoomName = (
                MintRoomSpecs.CashbotMintRoomId2RoomName[self.roomId])

        def printPos(self=self):
            # print position of localToon relative to this zone
            thisZone = self.getZoneNode(LevelConstants.UberZoneEntId)
            pos = base.localAvatar.getPos(thisZone)
            h = base.localAvatar.getH(thisZone)
            roomName = MintRoomSpecs.CashbotMintRoomId2RoomName[self.roomId]
            print 'mint pos: %s, h: %s, room: %s' % (
                repr(pos), h, roomName)
            if self.mint is not None:
                floorNum = self.mint.floorNum
            else:
                floorNum = '???'
            posStr = "X: %.3f" % pos[0] + "\nY: %.3f" % pos[1] + \
                     "\nZ: %.3f" % pos[2] + "\nH: %.3f" % h + \
                     "\nmintId: %s" % self.mintId + \
                     "\nfloor: %s" % floorNum + \
                     "\nroomId: %s" % self.roomId + \
                     "\nroomName: %s" % roomName
            base.localAvatar.setChatAbsolute(posStr,CFThought | CFTimeout)
        self.accept('f2',printPos)

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

        MintRoom.MintRoom.exit(self)

        if hasattr(self, 'suits'):
            del self.suits

        if (hasattr(self, 'relatedObjectMgrRequest')
                and self.relatedObjectMgrRequest):
            self.cr.relatedObjectMgr.abortRequest(self.relatedObjectMgrRequest)
            del self.relatedObjectMgrRequest

        bboard.remove(self.getReadyPostName())

        DistributedLevel.DistributedLevel.disable(self)

    def setSuits(self, suitIds, reserveSuitIds):
        assert(self.notify.debug(
            "setSuits suits: %s, reserves: %s" % (suitIds, reserveSuitIds)))
        oldSuitIds = list(self.suitIds)
        self.suitIds = suitIds
        self.reserveSuitIds = reserveSuitIds

        # this code was never used and was crashing when we fixed
        # DistributedFactorySuit.announceGenerate to call down to
        # its base class
        """
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
            """

    def reservesJoining(self):
        assert(self.notify.debug("reservesJoining"))
        # play track reserves joining battle
        pass

    def getCogSpec(self, cogId):
        cogSpecModule = MintRoomSpecs.getCogSpecModule(self.roomId)
        return cogSpecModule.CogData[cogId]

    def getReserveCogSpec(self, cogId):
        cogSpecModule = MintRoomSpecs.getCogSpecModule(self.roomId)
        return cogSpecModule.ReserveCogData[cogId]

    def getBattleCellSpec(self, battleCellId):
        cogSpecModule = MintRoomSpecs.getCogSpecModule(self.roomId)
        return cogSpecModule.BattleCells[battleCellId]

    def getFloorOuchLevel(self):
        return 8

    def getTaskZoneId(self):
        return self.mintId

    def getBossTaunt(self):
        return TTLocalizer.MintBossTaunt
    def getBossBattleTaunt(self):
        return TTLocalizer.MintBossBattleTaunt

    def __str__(self):
        if hasattr(self, 'roomId'):
            return '%s %s: %s' % (
                self.__class__.__name__,
                self.roomId,
                MintRoomSpecs.CashbotMintRoomId2RoomName[self.roomId],)
        else:
            return 'DistributedMintRoom'
    def __repr__(self):
        return str(self)
