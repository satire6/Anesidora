
from DistributedMinigameAI import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import CannonGameGlobals

class DistributedCannonGameAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        DistributedMinigameAI.__init__(self, air, minigameId)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedCannonGameAI',
                               [State.State('inactive',
                                            self.enterInactive,
                                            self.exitInactive,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            ['inactive']),
                                ],
                               # Initial State
                               'inactive',
                               # Final State
                               'inactive',
                               )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')
        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # Start the game timer
        if not config.GetBool('endless-cannon-game', 0):
            taskMgr.doMethodLater(CannonGameGlobals.GameTime,
                                  self.timerExpired,
                                  self.taskName("gameTimer"))

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        self.gameOver()
        return Task.done

    # distributed functions
    def __playing(self):
        """
        if this returns 0, the game has ended
        """
        if not hasattr(self, 'gameFSM'):
            return 0
        return self.gameFSM.getCurrentState().getName() == 'play'

    def _checkCannonRange(self, zRot, angle, avId):
        # returns non-zero if invalid
        outOfRange = 0
        if zRot < CannonGameGlobals.CANNON_ROTATION_MIN or \
           zRot > CannonGameGlobals.CANNON_ROTATION_MAX:
            self.air.writeServerEvent(
                'suspicious', avId,
                'Cannon game z-rotation out of range: %s' % zRot)
            self.notify.warning('av %s cannon z-rotation out of range: %s' %
                                (avId, zRot))
            outOfRange = 1
        if angle < CannonGameGlobals.CANNON_ANGLE_MIN or \
           angle > CannonGameGlobals.CANNON_ANGLE_MAX:
            self.air.writeServerEvent(
                'suspicious', avId,
                'Cannon game vertical angle out of range: %s' % angle)
            self.notify.warning(
                'av %s cannon vertical angle out of range: %s' % (avId, angle))
            outOfRange = 1
        return outOfRange

    def setCannonPosition(self, zRot, angle):
        if not self.__playing():
            self.notify.debug('ignoring setCannonPosition message')
            return
        avId = self.air.getAvatarIdFromSender()
        # a client is sending a position update for their cannon
        self.notify.debug("setCannonPosition: " + str(avId) +
                          ": zRot=" + str(zRot) + ", angle=" + str(angle))

        if self._checkCannonRange(zRot, angle, avId):
            return

        self.sendUpdate("updateCannonPosition", [avId, zRot, angle])

    def setCannonLit(self, zRot, angle):
        if not self.__playing():
            self.notify.debug('ignoring setCannonLit message')
            return
        avId = self.air.getAvatarIdFromSender()
        # a client is telling us that their cannon's fuse is lit
        self.notify.debug("setCannonLit: " + str(avId) + ": zRot=" +
                          str(zRot) + ", angle=" + str(angle))

        if self._checkCannonRange(zRot, angle, avId):
            return

        fireTime = self.getCurrentGameTime() + CannonGameGlobals.FUSE_TIME
        # set the cannon to go off in the near future
        self.sendUpdate("setCannonWillFire", [avId, fireTime, zRot, angle])

    def setToonWillLandInWater(self, landTime):
        """ landTime is game-relative """
        if not self.__playing():
            self.notify.debug('ignoring setToonWillLandInWater message')
            return
        senderAvId = self.air.getAvatarIdFromSender()
        # a toon will land in the water at some point in the future
        # calculate the score
        score = CannonGameGlobals.calcScore(landTime)
        # give everyone that many jbeans
        for avId in self.avIdList:
            self.scoreDict[avId] = score
        self.notify.debug("setToonWillLandInWater: time=%s, score=%s" % \
                          (landTime, score))

        taskMgr.remove(self.taskName("gameTimer"))
        delay = max(0,landTime - self.getCurrentGameTime())
        #self.notify.debug("setToonWillLandInWater: delay=%s" % delay)
        taskMgr.doMethodLater(delay,
                              self.toonLandedInWater,
                              self.taskName("game-over"))

        self.sendUpdate("announceToonWillLandInWater", [senderAvId, landTime])

    def toonLandedInWater(self, task):
        self.notify.debug("toonLandedInWater")
        # don't call gameOver() more than once
        if self.__playing():
            self.gameOver()
        return Task.done

    def exitPlay(self):
        taskMgr.remove(self.taskName("gameTimer"))
        taskMgr.remove(self.taskName("game-over"))

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
