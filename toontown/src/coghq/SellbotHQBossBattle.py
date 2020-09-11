from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.suit import DistributedSellbotBoss
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import CogHQBossBattle

class SellbotHQBossBattle(CogHQBossBattle.CogHQBossBattle):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("SellbotHQBossBattle")
    
    # special methods
    def __init__(self, loader, parentFSM, doneEvent):
        CogHQBossBattle.CogHQBossBattle.__init__(self, loader, parentFSM, doneEvent)
        # This is only used for magic words.
        self.teleportInPosHpr = (0, 95, 18, 180, 0, 0)

    def load(self):
        CogHQBossBattle.CogHQBossBattle.load(self)

    def unload(self):
        CogHQBossBattle.CogHQBossBattle.unload(self)

    def enter(self, requestStatus):
        CogHQBossBattle.CogHQBossBattle.enter(self, requestStatus,
                                              DistributedSellbotBoss.OneBossCog)
        self.__setupHighSky()

    def exit(self):
        CogHQBossBattle.CogHQBossBattle.exit(self)

        self.__cleanupHighSky()
                
    def __setupHighSky(self):
        self.loader.hood.startSky()
        sky = self.loader.hood.sky

        # Rotate the sky around so the more interesting part is
        # visible.
        sky.setH(150)
        sky.setZ(-100)

        """
        # Put some dirty-looking clouds around.
        self.cloudRing = sky.attachNewNode('cloudRing')
        self.cloudRing.setDepthWrite(0)
        self.cloudRing.setBin('background', 50)
        
        cloud = loader.loadModel('phase_4/models/props/test_clouds')
        cloud.find('**/p1').clearBillboard()        
        cloud.setColor(1, 0.8, 0.6, 1)
        cloud.setScale(20, 10, 10)
        cloud.setHpr(180, 0, 0)
        cloud.flattenLight()

        radius = 200
        for angle, z in [(30, -40), (60, -60), (80, -50), (110, -40),
                         (140, -70), (180, -50), (210, -40)]:
            radians = angle / 180.0 * math.pi
            x = radius * math.cos(radians)
            y = radius * math.sin(radians)
            c1 = cloud.copyTo(self.cloudRing)
            c1.setPos(x, y, z)
            c1.headsUp(0, 0, 0)
        """

    def __cleanupHighSky(self):
        # Turn the sky off
        self.loader.hood.stopSky()
        # self.cloudRing.removeNode()
        sky = self.loader.hood.sky
        sky.setH(0)
        sky.setZ(0)


