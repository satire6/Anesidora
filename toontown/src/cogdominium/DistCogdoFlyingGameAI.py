"""
@author: Schell Games
3-16-2010
"""
from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.DistributedMinigameAI import EXITED, EXPECTED, JOINED, READY

class DistCogdoFlyingGameAI(DistributedMinigameAI):
    """
    Flying Cogdominium Minigame AI Distributed Object!
    """
    notify = directNotify.newCategory("DistCogdoFlyingGameAI")

    def __init__(self, air, id):
        try:
            self.DistCogdoFlyingGameAI_initialized
        except:
            self.DistCogdoFlyingGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, id)

            print "FLYING COGDO GAME AI CREATED!"

    def areAllPlayersReady(self):
        ready = True

        for avId in self.avIdList:
            ready = ready and (self.stateDict[avId] == READY)

        return ready

    def setAvatarReady(self):
        DistributedMinigameAI.setAvatarReady(self)
