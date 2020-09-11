
from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
import NPCToons
from direct.task.Task import Task

class DistributedNPCBlockerAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        self.tutorial = 0

    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def setTutorial(self, val):
        # If you are in the tutorial you have no timeouts
        self.tutorial = val

    def getTutorial(self):
        return self.tutorial

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        # this avatar has come within range
        assert self.notify.debug("avatar enter " + str(avId))
        DistributedNPCToonBaseAI.avatarEnter(self)

        # Do what the quest manager does for DistributedNPCToon
        av = self.air.doId2do.get(avId)
        if av is None:
            self.notify.warning('toon isnt there! toon: %s' % avId)
            return

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                                self.__handleUnexpectedExit, extraArgs=[avId])

        self.sendStartMovie(avId)

    def sendStartMovie(self, avId):
        assert self.notify.debug('sendStartMovie()')
        self.busy = avId
        self.sendUpdate("setMovie", [NPCToons.BLOCKER_MOVIE_START,
                        self.npcId, avId,
                        ClockDelta.globalClockDelta.getRealNetworkTime()])
        # Timeout
        if (not self.tutorial):
            taskMgr.doMethodLater(NPCToons.CLERK_COUNTDOWN_TIME,
                                self.sendTimeoutMovie,
                                self.uniqueName('clearMovie'))

    def sendTimeoutMovie(self, task):
        assert self.notify.debug('sendTimeoutMovie()')
        self.timedOut = 1
        self.sendUpdate("setMovie", [NPCToons.BLOCKER_MOVIE_TIMEOUT,
                        self.npcId, self.busy,
                        ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        assert self.notify.debug('sendClearMovie()')
        self.busy = 0
        self.timedOut = 0
        self.sendUpdate("setMovie", [NPCToons.BLOCKER_MOVIE_CLEAR,
                        self.npcId, 0,
                        ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        if (not self.tutorial):
            self.sendTimeoutMovie(None)
        return None 
