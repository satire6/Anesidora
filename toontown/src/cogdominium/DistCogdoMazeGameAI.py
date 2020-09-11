"""
@author: Schell Games
3-16-2010
"""
import random

from direct.task.Task import Task

from toontown.minigame.DistributedMinigameAI import DistributedMinigameAI
from toontown.minigame.DistributedMinigameAI import EXITED, EXPECTED, JOINED, READY

import CogdoMazeGameGlobals
from CogdoMazeGameGlobals import CogdoMazeLockInfo

from direct.fsm.FSM import FSM
class DistCogdoMazeGameAI(DistributedMinigameAI, FSM):
    """
    Maze Cogdominium Minigame AI Distributed Object!
    """
    notify = directNotify.newCategory("DistCogdoMazeGameAI")

    TIMER_EXPIRED_TASK_NAME = "CogdoMazeGameTimerExpired"

    def __init__(self, air, id):
        try:
            self.DistMazeCogdoGameAI_initialized
        except:
            self.DistMazeCogdoGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, id)

            self.toonsInDoor = []

    def delete(self):
        DistributedMinigameAI.delete(self)
        taskMgr.remove(self.taskName(DistCogdoMazeGameAI.TIMER_EXPIRED_TASK_NAME))

    def _initLocks(self):
        self.locks = {}

        data = CogdoMazeGameGlobals.TempMazeData
        width = data["width"]
        height = data["height"]

        positions = self._getLockPositions(data, width, height)

        for i in range(len(self.avIdList)):
            self._addLock(self.avIdList[i], positions[i][0], positions[i][1])

    def _getLockPositions(self, data, width, height):
        """
        Splits the maze into 4, shuffles the quadrants, and picks random spots
        to place the locks.

        @return: list of (tileX, tileY) tuples with the positions of the locks
        """
        halfWidth = int(width / 2)
        halfHeight = int(height / 2)

        # 1. Split the maze into 4 quadrants
        quadrants = [
            # (x0, y0, x1, y1)
            (0, 0, halfWidth - 2, halfHeight - 2),
            (halfWidth + 2, 0, width - 1, halfHeight - 2),
            (0, halfHeight + 2, halfWidth - 2, height - 1),
            (halfWidth + 2, halfHeight + 2, width - 1, height - 1)
            ]

        # 2. Shuffle the quadrant order
        random.shuffle(quadrants)

        positions = []

        # 3. pick random available spots, populate list
        for i in range(len(self.avIdList)):
            quadrant = quadrants[i]
            tX = -1
            tY = -1

            while tX < 0 or data["collisionTable"][tY][tX] == 1:
                tX = random.randint(quadrant[0], quadrant[2])
                tY = random.randint(quadrant[1], quadrant[3])

            positions.append((tX, tY))

        return positions

    def _addLock(self, toonId, tX, tY):
        lock = CogdoMazeLockInfo(toonId, tX, tY)
        self.locks[toonId] = lock

    # getter (required broadcast ram)
    def getLocks(self):
        toonIds = []
        spawnPointsX = []
        spawnPointsY = []
        for lock in self.locks.values():
            toonIds.append(lock.toonId)
            spawnPointsX.append(lock.tileX)
            spawnPointsY.append(lock.tileY)

        return toonIds, spawnPointsX, spawnPointsY

    def setExpectedAvatars(self, avIds):
        DistributedMinigameAI.setExpectedAvatars(self, avIds)

        self._initLocks()

    def areAllPlayersReady(self):
        return False not in [(state == READY) for state in self.stateDict.values()]

    def setGameStart(self, timestamp):
        DistributedMinigameAI.setGameStart(self, timestamp)

        self.enterPlay()

    def timerExpiredTask(self, task):
        self.notify.debugCall()

        self.gameOver()
        self.d_broadcastDoAction(CogdoMazeGameGlobals.GameActions.GameOver)

        return Task.done

    def gameOver(self):
        self.exitPlay()
        DistributedMinigameAI.gameOver(self)

    def isDoorLocked(self):
        return True in [lock.locked for lock in self.locks.values()]

    def areAllToonsInDoor(self):
        return len(self.avIdList) == len(self.toonsInDoor)

    def validateSenderId(self, senderId):
        if senderId in self.avIdList:
            return True

        # TODO: Report suspicious event
        return False

#===============================================================================
# DISTRIBUTED
#===============================================================================

    # airecv clsend
    def requestAction(self, action, data):
        self.notify.debugCall()

        senderId = self.air.getAvatarIdFromSender()
        if not self.validateSenderId(senderId):
            return False

        if action == CogdoMazeGameGlobals.GameActions.Unlock:
            if self.locks[senderId].locked:
                self.locks[senderId].locked = False

                self.d_broadcastDoAction(action, senderId)
            else:
                pass # TODO: Suspicious event...

        elif action == CogdoMazeGameGlobals.GameActions.EnterDoor:
            if senderId not in self.toonsInDoor:
                self.toonsInDoor.append(senderId)
                self.d_broadcastDoAction(action, senderId)

                if self.areAllToonsInDoor():
                    self.gameOver()
                    self.d_broadcastDoAction(CogdoMazeGameGlobals.GameActions.GameOver)
            else:
                pass # TODO: Suspicious event...

        elif action == CogdoMazeGameGlobals.GameActions.RevealDoor:
            self.d_broadcastDoAction(action, senderId)

        elif action == CogdoMazeGameGlobals.GameActions.RevealLock:
            self.d_broadcastDoAction(action, data)

        else:
            pass # TODO: Probably report a suspicious event too!

    def d_broadcastDoAction(self, action, data=0):
        self.sendUpdate("doAction", [action, data])

#===============================================================================
# FINITE STATE MACHINE
#===============================================================================

    def enterPlay(self):
        taskMgr.doMethodLater(CogdoMazeGameGlobals.GameDuration,
            self.timerExpiredTask,
            self.taskName(DistCogdoMazeGameAI.TIMER_EXPIRED_TASK_NAME))

    def exitPlay(self):
        taskMgr.remove(self.taskName(DistCogdoMazeGameAI.TIMER_EXPIRED_TASK_NAME))

