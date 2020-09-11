from direct.directnotify import DirectNotifyGlobal
import HoodDataAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import MMTreasurePlannerAI
from toontown.classicchars import DistributedMinnieAI
from toontown.safezone import DistributedMMPianoAI

class MMHoodDataAI(HoodDataAI.HoodDataAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MMHoodDataAI")

    def __init__(self, air, zoneId = None):
        hoodId = ToontownGlobals.MinniesMelodyland
        if zoneId == None:
            zoneId = hoodId
        HoodDataAI.HoodDataAI.__init__(self, air, zoneId, hoodId)

    def startup(self):
        HoodDataAI.HoodDataAI.startup(self)

        trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        trolley.generateWithRequired(self.zoneId)
        trolley.start()
        self.addDistObj(trolley)

        self.treasurePlanner = MMTreasurePlannerAI.MMTreasurePlannerAI(self.zoneId)
        self.treasurePlanner.start()

        self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()
        self.addDistObj(self.classicChar)

        # Piano is not compatible with the fishing pond that is there now
        # Perhaps we can work that out later
        # piano = DistributedMMPianoAI.DistributedMMPianoAI(self.air)
        # piano.generateWithRequired(self.zoneId)
        # piano.start()
        # self.addDistObj(piano)
