from direct.directnotify import DirectNotifyGlobal
import DistributedStageAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import StageLayout
from direct.showbase import DirectObject
import random

class StageManagerAI(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('StageManagerAI')

    # magic-word override
    stageId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        # DistributedElevatorAI needs this
        return 0

    def createStage(self, stageId, players):
        # check for ~stageId
        for avId in players:
            if bboard.has('stageId-%s' % avId):
                stageId = bboard.get('stageId-%s' % avId)
                break

        numFloors = StageLayout.getNumFloors(stageId)

        floor = random.randrange(numFloors)
        # check for ~stageFloor
        for avId in players:
            if bboard.has('stageFloor-%s' % avId):
                floor = bboard.get('stageFloor-%s' % avId)
                # bounds check
                floor = max(0, floor)
                floor = min(floor, numFloors-1)
                break

        # check for ~stageRoom
        for avId in players:
            if bboard.has('stageRoom-%s' % avId):
                roomId = bboard.get('stageRoom-%s' % avId)
                for i in xrange(numFloors):
                    layout = StageLayout.StageLayout(stageId, i)
                    if roomId in layout.getRoomIds():
                        floor = i
                else:
                    from toontown.coghq import StageRoomSpecs
                    roomName = StageRoomSpecs.CashbotStageRoomId2RoomName[roomId]
                    StageManagerAI.notify.warning(
                        'room %s (%s) not found in any floor of stage %s' %
                        (roomId, roomName, stageId))

        stageZone = self.air.allocateZone()
        stage = DistributedStageAI.DistributedStageAI(
            self.air, stageId, stageZone, floor, players)
        stage.generateWithRequired(stageZone)
        return stageZone
