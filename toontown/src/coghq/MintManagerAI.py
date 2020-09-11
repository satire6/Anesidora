from direct.directnotify import DirectNotifyGlobal
import DistributedMintAI
from toontown.toonbase import ToontownGlobals
from toontown.coghq import MintLayout
from direct.showbase import DirectObject
import random

class MintManagerAI(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('MintManagerAI')

    # magic-word override
    mintId = None

    def __init__(self, air):
        DirectObject.DirectObject.__init__(self)
        self.air = air

    def getDoId(self):
        # DistributedElevatorAI needs this
        return 0

    def createMint(self, mintId, players):
        # check for ~mintId
        for avId in players:
            if bboard.has('mintId-%s' % avId):
                mintId = bboard.get('mintId-%s' % avId)
                break

        numFloors = ToontownGlobals.MintNumFloors[mintId]

        floor = random.randrange(numFloors)
        # check for ~mintFloor
        for avId in players:
            if bboard.has('mintFloor-%s' % avId):
                floor = bboard.get('mintFloor-%s' % avId)
                # bounds check
                floor = max(0, floor)
                floor = min(floor, numFloors-1)
                break

        # check for ~mintRoom
        for avId in players:
            if bboard.has('mintRoom-%s' % avId):
                roomId = bboard.get('mintRoom-%s' % avId)
                for i in xrange(numFloors):
                    layout = MintLayout.MintLayout(mintId, i)
                    if roomId in layout.getRoomIds():
                        floor = i
                else:
                    from toontown.coghq import MintRoomSpecs
                    roomName = MintRoomSpecs.CashbotMintRoomId2RoomName[roomId]
                    MintManagerAI.notify.warning(
                        'room %s (%s) not found in any floor of mint %s' %
                        (roomId, roomName, mintId))

        mintZone = self.air.allocateZone()
        mint = DistributedMintAI.DistributedMintAI(
            self.air, mintId, mintZone, floor, players)
        mint.generateWithRequired(mintZone)
        return mintZone
