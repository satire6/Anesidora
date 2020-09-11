from otp.ai.AIBase import *
from direct.distributed.ClockDelta import *

from direct.distributed import DistributedObjectAI

class DistributedTreasureAI(DistributedObjectAI.DistributedObjectAI):

    def __init__(self, air, treasurePlanner, x, y, z):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.treasurePlanner = treasurePlanner
        self.pos = (x, y, z)

    def requestGrab(self):
        # This is the handler that gets called when a localToon tries to grab
        # a DistributedTreasure
        avId = self.air.getAvatarIdFromSender()
        self.treasurePlanner.grabAttempt(avId, self.getDoId())

    def validAvatar(self, av):
        # This is called by the treasure planner to ask if this
        # particular avatar is allowed to have this treasure.
        return 1

    def d_setGrab(self, avId):
        # This is how the treasurePlanner tells everyone that this treasure
        # has been grabbed.
        self.sendUpdate("setGrab", [avId])

    def d_setReject(self):
        # This is how the treasurePlanner tells everyone that this treasure
        # has been attempted for, but rejected.
        self.sendUpdate("setReject", [])

    def getPosition(self):
        # This is needed because setPosition is a required field.
        return self.pos

    def setPosition(self, x, y, z):
        self.pos = (x, y, z)

    def b_setPosition(self, x, y, z):
        self.setPosition(x, y, z)
        self.d_setPosition(x, y, z)

    def d_setPosition(self, x, y, z):
        # This is how the treasurePlanner tells everyone that this treasure
        # has been attempted for, but rejected.
        self.sendUpdate("setPosition", [x, y, z])
