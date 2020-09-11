"""
@author: Schell Games
3-16-2010
"""
from direct.showbase.DirectObject import DirectObject

from pandac.PandaModules import NodePath, VBase4, Fog

from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame.MazeMapGui import MazeMapGui

import CogdoMazeGameGlobals
from CogdoMazeGameGlobals import CogdoMazeLockInfo

class DistCogdoMazeGame(DistributedMinigame):
    """
    Maze Cogdominium Minigame client Distributed Object!
    Class is primarily a controller for the networking/game events.
    Visuals are handled by CogdoMazeGame instead.
    """
    notify = directNotify.newCategory("DistCogdoMazeGame")

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.game = CogdoMazeGame(self)

    def load(self):
        DistributedMinigame.load(self)
        self._remoteActionEventName = self.uniqueName("doAction")
        self.game.load()

    def unload(self):
        self.game.unload()
        DistributedMinigame.unload(self)

    def onstage(self):
        DistributedMinigame.onstage(self)
        self.game.onstage()

    def offstage(self):
        self.game.offstage()
        DistributedMinigame.offstage(self)

    # broadcast
    def setGameReady(self):
        if DistributedMinigame.setGameReady(self):
            return

        self.game.ready()

    # broadcast
    def setGameStart(self, timestamp):
        DistributedMinigame.setGameStart(self, timestamp)

        self.game.start()

    # broadcast
    def setGameExit(self):
        DistributedMinigame.setGameExit(self)

        self.game.exit()

    # required broadcast ram
    def setLocks(self, toonIds, spawnPointsX, spawnPointsY):
        self.lockInfoList = []
        self.locksInfo = {}

        for i in range(len(toonIds)):
            lockInfo = CogdoMazeLockInfo(toonIds[i], spawnPointsX[i], spawnPointsY[i])
            self.lockInfoList.append(lockInfo)
            self.locksInfo[lockInfo.toonId] = lockInfo

    def d_sendRequestAction(self, action, data):
        self.sendUpdate("requestAction", [action, data])


    # broadcast
    def doAction(self, action, data):
        self.notify.debugCall()

        assert action in CogdoMazeGameGlobals.GameActions
        if data == base.localAvatar.doId: return

        messenger.send(self._remoteActionEventName, [action, data])


    def getTitle(self):
        return "Cogdominium Maze Game"

    def getInstructions(self):
        return ""

    def getRemoteActionEventName(self):
        return self._remoteActionEventName

from toontown.minigame.Maze import Maze

class CogdoMazeGame(DirectObject):
    """
    Handles the visuals/looks of the cogdo maze game
    """
    notify = directNotify.newCategory("CogdoMazeGame")

    UPDATE_TASK_NAME = "CogdoMazeGameUpdate"

    def __init__(self, distGame):
        self.distGame = distGame

    def load(self):
        self.maze = Maze(CogdoMazeGameGlobals.TempMazeFile)
        #self.maze.maze.setColorScale(0.0, 0, 5.0, 1.0)
        self.maze.setScale(2, 1.75)

        self.guiMgr = CogdoMazeGuiManager(self.maze)
        self.audioMgr = CogdoMazeAudioManager()

        self.toonId2Door = {}
        self.keyIdToKey = {}
        self.players = []
        self.toonId2Player = {}
        self.lockId2Lock = {}

        self.localPlayer = CogdoMazeLocalPlayer(len(self.players), base.localAvatar, self, self.guiMgr)
        self._addPlayer(self.localPlayer)

        # TEMP...
        self.sprites = loader.loadModel("cogdominium/mazeSprites.egg")

        # Create door
        pos = self.maze.tile2world(int(self.maze.width / 2), self.maze.height - 1)
        gridPos = self.maze.world2tile(pos[0], pos[1])

        # TEMP
        openDoorModel = self.sprites.find("**/door_open")
        openDoorModel.setScale(8)
        openDoorModel.setZ(0.25)
        closedDoorModel = self.sprites.find("**/door_closed")
        closedDoorModel.setScale(8)
        closedDoorModel.setZ(0.25)

        self.door = CogdoMazeDoor(closedDoorModel, openDoorModel)
        self.door.setPosition(pos[0], pos[1] - 0.05)
        self.door.offstage()
        self.guiMgr.mazeMapGui.addDoor(gridPos[0], gridPos[1], VBase4(1, 1, 1, 1))

        # load key model, keys will be placed when everyone's there
        self.fuseModels = (
            self.sprites.find("**/fuse_white"),
            self.sprites.find("**/fuse_blue"),
            self.sprites.find("**/fuse_yellow"),
            self.sprites.find("**/fuse_red"),
            )
        for fuse in self.fuseModels:
            fuse.setScale(2)
            fuse.setBillboardPointEye()

        self.fuseBoxModels = (
            (self.sprites.find("**/fusebox_white"), self.sprites.find("**/fusebox_white_plugged")),
            (self.sprites.find("**/fusebox_blue"), self.sprites.find("**/fusebox_blue_plugged")),
            (self.sprites.find("**/fusebox_yellow"), self.sprites.find("**/fusebox_yellow_plugged")),
            (self.sprites.find("**/fusebox_red"), self.sprites.find("**/fusebox_red_plugged")),
            )
        for fuseBox in self.fuseBoxModels:
            fuseBox[0].setScale(4)
            fuseBox[1].setScale(4)

        #self._initFog()
        self.accept(self.distGame.getRemoteActionEventName(), self.handleRemoteAction)

    def unload(self):
        self.__stopUpdateTask()
        self.ignoreAll()
        #self._destroyFog()

        self.maze.destroy()
        del self.maze

        self.door.destroy()
        del self.door

        for key in self.keyIdToKey.values():
            key.destroy()
        del self.keyIdToKey

        self.audioMgr.destroy()
        del self.audioMgr

        self.guiMgr.destroy()
        del self.guiMgr

        self.sprites.removeNode()
        del self.sprites

        del self.players
        del self.toonId2Player
        del self.localPlayer

    def _initFog(self):
        self.fog = Fog("MazeFog")
        self.fog.setColor(VBase4(0.3, 0.3, 0.3, 1.0))
        self.fog.setLinearRange(0.0, 100.0)

        self._renderFog = render.getFog()
        render.setFog(self.fog)

    def _destroyFog(self):
        render.clearFog()
        del self.fog
        del self._renderFog

    def onstage(self):
        self.door.onstage()
        self.maze.onstage()

        self.placePlayer(self.localPlayer)
        self.localPlayer.ready()
        self.localPlayer.onstage()

    def offstage(self):
        self.maze.offstage()
        self.door.offstage()
        self.localPlayer.offstage()

    def ready(self):
        # Initialize remote players
        for avId in self.distGame.remoteAvIdList:
            toon = self.distGame.getAvatar(avId)
            if toon is not None:
                player = CogdoMazePlayer(len(self.players), toon)
                self._addPlayer(player)

                self.placePlayer(player)
                player.ready()

        assert len(self.distGame.lockInfoList) <= CogdoMazeGameGlobals.LockColors

        # Initialize locks and keys
        for i in range(len(self.distGame.lockInfoList)):
            lockInfo = self.distGame.lockInfoList[i]
            toon = base.cr.doId2do[lockInfo.toonId]
            color = CogdoMazeGameGlobals.LockColors[i] #toon.style.getHeadColor()
            pos = self.maze.tile2world(lockInfo.tileX, lockInfo.tileY)
            player = self.toonId2Player[lockInfo.toonId]

            # Create and place locks
            lock = CogdoMazeLock(i, lockInfo.toonId, self.fuseBoxModels[i][0], self.fuseBoxModels[i][1], color, pos[0], pos[1] + 1)
            self.door.addLock(lock)
            self.guiMgr.mazeMapGui.addLock(lockInfo.tileX, lockInfo.tileY, color)

            # Create and place keys
            key = CogdoMazeKey(lockInfo.toonId, self.fuseModels[i], color)
            self.keyIdToKey[key.id] = key

            lock.setKey(key)
            player.holdKey(key)

            if toon == self.localPlayer.toon:
                self.lockColorIndex = i

    def start(self):
        self.accept(self.door.enterCollisionEventName, self.handleDoorCollision)

        for lock in self.door.getLocks():
            self.accept(lock.enterCollisionEventName, self.handleLockCollision)

        self.__startUpdateTask()
        self.localPlayer.enable()

        if __debug__:
            self.acceptOnce("escape", self.distGame.d_requestExit)
            self.acceptOnce("home", self.guiMgr.revealMazeMap)

        self.guiMgr.displayNotification("Find the %s fusebox!" % CogdoMazeGameGlobals.LockNames[self.lockColorIndex])

        self.audioMgr.playMusic("normal")

    def exit(self):
        if __debug__:
            self.ignore("escape")
            self.ignore("home")

        self.ignore(self.door.enterCollisionEventName)

        for lock in self.door.getLocks():
            self.ignore(lock.enterCollisionEventName)

        self.__stopUpdateTask()
        self.localPlayer.disable()

    def _addPlayer(self, player):
        self.players.append(player)
        self.toonId2Player[player.toon.doId] = player
        self.guiMgr.mazeMapGui.addPlayer(0, 0, player.toon.style.getHeadColor())

    def _removePlayer(self, player):
        self.players.remove(player)
        self.players.remove(player.toon.doId)

    def __startUpdateTask(self):
        self.__stopUpdateTask()
        taskMgr.add(self.__updateTask, CogdoMazeGame.UPDATE_TASK_NAME, 45)

    def __stopUpdateTask(self):
        taskMgr.remove(CogdoMazeGame.UPDATE_TASK_NAME)

    def __updateTask(self, task):
        self.localPlayer.update()

        for player in self.players:
            curTX, curTY = self.maze.world2tile(player.toon.getX(), player.toon.getY())
            self.guiMgr.updateMazeMapPlayer(player.id, curTX, curTY)

        return Task.cont

    def placePlayer(self, player):
        i = self.distGame.avIdList.index(player.toon.doId)
        pos = self.maze.tile2world(int(self.maze.width / 2), 2)
        player.toon.setPos(
            pos[0] + i * self.maze.cellWidth,
            pos[1],
            0
            )

    def handleRemoteAction(self, action, data):
        if action == CogdoMazeGameGlobals.GameActions.Unlock:
            self.toonUnlocks(data)

        if action == CogdoMazeGameGlobals.GameActions.RevealDoor:
            self.toonRevealsDoor(data)

        if action == CogdoMazeGameGlobals.GameActions.RevealLock:
            self.toonRevealsLock(data)

        elif action == CogdoMazeGameGlobals.GameActions.GameOver:
            self.distGame.gameOver()

    def toonRevealsDoor(self, toonId):
        self.door.revealed = True

        message = None
        nextMessage = None
        if toonId == self.localPlayer.toon.doId:
            message = "You found the elevator door!"
            if self.localPlayer.hasKey():
                nextMessage = "Find the %s fusebox\nto help open the elevator." % CogdoMazeGameGlobals.LockNames[self.lockColorIndex]
        else:
            toon = self.distGame.getAvatar(toonId)
            message = "%s found the elevator door!" % toon.getName()

        if message is not None:
            self.guiMgr.displayNotification(message, nextMessage)


    def toonRevealsLock(self, toonId):
        if toonId == self.localPlayer.toon.doId:
            self.guiMgr.displayNotification("Someone found your fusebox!", "Go to the %s fusebox!" % CogdoMazeGameGlobals.LockNames[self.lockColorIndex])


    def toonEntersDoor(self, toonId):
        player = self.toonId2Player[toonId]
        player.disable()

        self.door.playerEntersDoor(player)

        message = None
        if self.door.getPlayerCount() == len(self.players):
            message = ""
        else:
            message = "Waiting for %d toons to get to elevator door..." % (len(self.players) - self.door.getPlayerCount())

        if message is not None:
            self.guiMgr.displayNotification(message)

    def toonUnlocks(self, toonId):
        player = self.toonId2Player[toonId]
        self.door.unlock(player.getKey().lock.id)
        key = self.toonId2Player[toonId].dropKey()
        key.offstage()

        if player == self.localPlayer:
            self.audioMgr.playSfx("fusePlaced")

        if not self.door.isLocked():
            self.door.open()
            self.audioMgr.playSfx("doorOpen")

        message = None
        nextMessage = None
        if not self.door.isLocked():
            message = "All the fuseboxes are fixed!"
            nextMessage = "Find the elevator door!"
        elif self.door.isLocked() and player == self.localPlayer:
            message = "Help your friends find the other fuseboxes!"
        else:
            if player == self.localPlayer:
                message = "Good job! Now, find the exit!"
            #elif self.localPlayer.getKey() == key:
            #message = "[name] found your fusebox! Go to the [color] fusebox!"

        if message is not None:
            self.guiMgr.displayNotification(message, nextMessage)

    def handleLockCollision(self, collEntry):
        assert self.notify.debugCall()

        intoNodePath = collEntry.getIntoNodePath()
        intoName = intoNodePath.getName()

        nameParts = intoName.split("-")
        assert len(nameParts) > 1
        id = int(nameParts[1])
        lock = self.door.getLock(id)

        if self.localPlayer.hasKey():
            key = self.localPlayer.getKey()
            if lock == key.lock:
                self.toonUnlocks(self.localPlayer.toon.doId)
                self.distGame.d_sendRequestAction(CogdoMazeGameGlobals.GameActions.Unlock, id)
            else:
                self.toonRevealsLock(lock.toonId)
                self.distGame.d_sendRequestAction(CogdoMazeGameGlobals.GameActions.RevealLock, lock.toonId)

    def handleDoorCollision(self, collEntry):
        assert self.notify.debugCall()

        if not self.door.revealed:
            if self.localPlayer.hasKey():
                self.toonRevealsDoor(self.localPlayer.toon.doId)
            self.distGame.d_sendRequestAction(CogdoMazeGameGlobals.GameActions.RevealDoor, 0)

        if not self.localPlayer.hasKey():
            self.toonEntersDoor(self.localPlayer.toon.doId)
            self.distGame.d_sendRequestAction(CogdoMazeGameGlobals.GameActions.EnterDoor, 0)


    def doMazeCollisions(self, oldPos, newPos):
        # we will calculate an offset vector that
        # keeps the toon out of the walls
        offset = newPos - oldPos

        # toons can only get this close to walls
        WALL_OFFSET = 1.

        # make sure we're not in a wall already
        curX = oldPos[0]; curY = oldPos[1]
        curTX, curTY = self.maze.world2tile(curX, curY)
        assert(not self.maze.collisionTable[curTY][curTX])

        def calcFlushCoord(curTile, newTile, centerTile):
            # calculates resulting one-dimensional coordinate,
            # given that the object is moving from curTile to
            # newTile, where newTile is a wall
            EPSILON = 0.01
            if newTile > curTile:
                return ((newTile-centerTile)*self.maze.cellWidth)\
                       -EPSILON-WALL_OFFSET
            else:
                return ((curTile-centerTile)*self.maze.cellWidth)+WALL_OFFSET

        offsetX = offset[0]; offsetY = offset[1]

        WALL_OFFSET_X = WALL_OFFSET
        if offsetX < 0:
            WALL_OFFSET_X = -WALL_OFFSET_X
        WALL_OFFSET_Y = WALL_OFFSET
        if offsetY < 0:
            WALL_OFFSET_Y = -WALL_OFFSET_Y

        # check movement in X direction
        newX = curX + offsetX + WALL_OFFSET_X; newY = curY
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTX != curTX:
            # we've crossed a tile boundary
            if self.maze.collisionTable[newTY][newTX]:
                # there's a wall
                # adjust the X offset so that the toon
                # hits the wall exactly
                offset.setX(calcFlushCoord(curTX, newTX,
                                           self.maze.originTX)-curX)

        newX = curX; newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTY != curTY:
            # we've crossed a tile boundary
            if self.maze.collisionTable[newTY][newTX]:
                # there's a wall
                # adjust the Y offset so that the toon
                # hits the wall exactly
                offset.setY(calcFlushCoord(curTY, newTY,
                                           self.maze.originTY)-curY)

        # at this point, if our new position is in a wall, we're
        # running right into a protruding corner:
        #
        #  \
        #   ###
        #   ###
        #   ###
        #
        offsetX = offset[0]; offsetY = offset[1]

        newX = curX + offsetX + WALL_OFFSET_X
        newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if self.maze.collisionTable[newTY][newTX]:
            # collide in only one of the dimensions
            cX = calcFlushCoord(curTX, newTX, self.maze.originTX)
            cY = calcFlushCoord(curTY, newTY, self.maze.originTY)
            if (abs(cX - curX) < abs(cY - curY)):
                offset.setX(cX - curX)
            else:
                offset.setY(cY - curY)

        return oldPos + offset


class CogdoMazeDoor:
    def __init__(self, closedDoorModel, openDoorModel):
        self.model = NodePath("CogdoMazeDoor")
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)

        self.closedDoorModel = closedDoorModel
        self.closedDoorModel.reparentTo(self.model)

        self.openDoorModel = openDoorModel
        self.openDoorModel.reparentTo(self.model)
        self.openDoorModel.stash()

        self.lockId2lock = {}
        self._open = False
        self.revealed = False
        self.players = []

        self._initCollisions()

    def setPosition(self, x, y):
        self.model.setPos(x, y, 2.5)

    def _initCollisions(self):
        name = "CogdoMazeDoor"
        collSphere = CollisionSphere(0, 0, 0.0, 0.25)
        collSphere.setTangible(0)
        collNode = CollisionNode(name)
        collNode.setFromCollideMask(ToontownGlobals.CatchGameBitmask)
        collNode.addSolid(collSphere)
        self.collNP = self.model.attachNewNode(collNode)

        self.enterCollisionEventName = "enter" + name

    def destroy(self):
        self.model.removeNode()
        del self.model
        del self.openDoorModel
        del self.closedDoorModel

        for lock in self.lockId2lock.values():
            lock.destroy()
        del self.lockId2lock

    def onstage(self):
        self.model.unstash()

    def offstage(self):
        self.model.stash()

    def open(self):
        self._open = True
        self.closedDoorModel.stash()
        self.openDoorModel.unstash()

    def close(self):
        self._open = False
        self.closedDoorModel.unstash()
        self.openDoorModel.stash()

    def addLock(self, lock):
        self.lockId2lock[lock.id] = lock

    def unlock(self, lockId):
        lock = self.lockId2lock.get(lockId)

        if lock is not None and lock.isLocked():
            lock.unlock()
            return True

        return False

    def getLocks(self):
        return self.lockId2lock.values()

    def getLock(self, lockId):
        return self.lockId2lock.get(lockId)

    def isLocked(self):
        return True in [lock.isLocked() for lock in self.lockId2lock.values()]

    def playerEntersDoor(self, player):
        self.players.append(player)

    def getPlayerCount(self):
        return len(self.players)


class CogdoMazeLock:
    def __init__(self, id, toonId, model, pluggedModel, color, x=0, y=0):
        self.id = id
        self.toonId = toonId
        self.model = model
        self.pluggedModel = pluggedModel

        self.model.reparentTo(render)
        self.pluggedModel.reparentTo(render)
        self.pluggedModel.stash()

        self.setPosition(x, y)

        self._locked = True
        self.key = None
        self.revealed = False

        self._initCollisions()

    def destroy(self):
        self.model.removeNode()
        del self.model

        self.pluggedModel.removeNode()
        del self.pluggedModel

    def onstage(self):
        if self._locked:
            self.model.unstash()
        else:
            self.pluggedModel.unstash()

    def offstage(self):
        self.model.stash()
        self.pluggedModel.stash()

    def _initCollisions(self):
        name = "CogdoMazeLock-%d" % self.id
        collSphere = CollisionSphere(0, 0, 0.0, 0.25)
        collSphere.setTangible(0)
        collNode = CollisionNode(name)
        collNode.setFromCollideMask(ToontownGlobals.CatchGameBitmask)
        collNode.addSolid(collSphere)
        self.model.attachNewNode(collNode)

        self.enterCollisionEventName = "enter" + name

    def unlock(self):
        self.pluggedModel.unstash()
        self.model.stash()
        self._locked = False

    def isLocked(self):
        return self._locked

    def setPosition(self, x, y, z=2.5):
        self.model.setPos(x, y-0.1, z)
        self.pluggedModel.setPos(self.model, 0, 0, 0)

    def setKey(self, key):
        self.key = key
        self.key.setLock(self)

from toontown.toonbase import ToontownGlobals

from pandac.PandaModules import CollisionSphere, CollisionNode

class CogdoMazeKey:
    def __init__(self, id, model, color):
        self.id = id
        self.model = model
        self.model.setPos(0, 0, 0)
        self.model.reparentTo(render)
        #self.model.setColor(color)

        self._playerWhoPickedItUp = None
        self.lock = None

    def destroy(self):
        self.model.removeNode()
        del self.model

    def onstage(self):
        self.model.unstash()

    def offstage(self):
        self.model.stash()

    def setPosition(self, x, y, z=0):
        self.model.setPos(x, y, z)

    def heldByPlayer(self, player):
        self._playerWhoPickedItUp = player
        self.enable()

    def drop(self):
        self.model.wrtReparentTo(render)
        self.model.setZ(0)

        self._playerWhoPickedItUp = None

    def disable(self):
        self.model.setAlphaScale(0.5)

    def enable(self):
        self.model.setAlphaScale(1.0)

    def setLock(self, lock):
        self.lock = lock


from direct.fsm.FSM import FSM

class CogdoMazePlayer(FSM):
    """
    Controls the animation state of a player toon in the cogdo maze game.
    """
    _key = None

    def __init__(self, id, toon):
        self.id = id
        self.toon = toon

    def ready(self):
        self.toon.reparentTo(render)
        self.toon.setAnimState('Happy', 1.0)
        self.toon.setSpeed(0, 0)
        self.toon.startSmooth()

    def holdKey(self, key):
        if self._key is None:
            self._key = key
            self._key.heldByPlayer(self)

            self._key.model.reparentTo(self.toon)
            self._key.model.setPos(0, 0, self.toon.getHeight() + 2)

    def dropKey(self):
        key = None
        if self._key is not None:
            key = self._key

            self._key.drop()
            self._key = None

        return key

    def hasKey(self):
        return self._key is not None

    def getKey(self):
        return self._key


from direct.task.Task import Task

from toontown.minigame.OrthoDrive import OrthoDrive
from toontown.minigame.OrthoWalk import OrthoWalk

class CogdoMazeLocalPlayer(CogdoMazePlayer):
    """
    Controls input, gui, and camera for a local player in the maze game.
    """
    def __init__(self, id, toon, game, guiMgr):
        CogdoMazePlayer.__init__(self, id, toon)
        self.game = game
        self.guiMgr = guiMgr

        self.cameraMgr = CogdoMazeCameraManager(self.toon, self.game.maze, camera, render)

        self.enabled = False

    def onstage(self):
        self.toon.hideName()
        self.cameraMgr.enable()
        self.update()

    def offstage(self):
        self.disable()
        self.cameraMgr.disable()
        self.toon.showName()

    def enable(self):
        if self.enabled: return
        orthoDrive = OrthoDrive(
            CogdoMazeGameGlobals.ToonRunSpeed,
            maxFrameMove=(self.game.maze.cellWidth / 2),
            customCollisionCallback=self.game.doMazeCollisions
            )

        self.orthoWalk = OrthoWalk(
            orthoDrive,
            broadcast=not self.game.distGame.isSinglePlayer()
            )

        self.orthoWalk.start()

        self.guiMgr.showTimer(CogdoMazeGameGlobals.GameDuration, self.disable)
        self.enabled = True

    def disable(self):
        if not self.enabled: return

        self.guiMgr.hideTimer()

        self.orthoWalk.stop()
        self.orthoWalk.destroy()
        del self.orthoWalk

        self.enabled = False

    def update(self):
        self.cameraMgr.update()


import math

from direct.showbase.PythonUtil import bound as clamp
from pandac.PandaModules import VBase3

class CogdoMazeCameraManager:
    def __init__(self, toon, maze, cam, root):
        self.toon = toon
        self.maze = maze
        self.camera = cam
        self.root = root

        self.minPos = self.maze.tile2world(3, 4)
        self.maxPos = self.maze.tile2world(self.maze.width-3, self.maze.height-2)

    def enable(self):
        self.parent = render.attachNewNode('GameCamParent')
        self.parent.reparentTo(self.root)
        self.parent.setPos(self.toon, 0, 0, 0)
        self.parent.setHpr(self.root, 0, 0, 0)
        self.camera.reparentTo(self.parent)

        self.setCameraOffset(
            CogdoMazeGameGlobals.OverheadCameraAngle,
            CogdoMazeGameGlobals.OverheadCameraDistance)

    def setCameraOffset(self, radAngle, distance):
        self.camera.setPos(VBase3(
                0,
                -math.cos(radAngle) * distance,
                math.sin(radAngle) * distance
                ))
        self.camera.lookAt(self.toon)

    def disable(self):
        self.camera.wrtReparentTo(render)

        self.parent.removeNode()
        del self.parent

    def update(self):
        toonPos = self.toon.getPos()

        self.parent.setPos(
            self.toon.getParent(),
            clamp(toonPos.getX(), self.minPos[0], self.maxPos[0]),
            clamp(toonPos.getY(), self.minPos[1], self.maxPos[1]),
            0
            )

from direct.gui.OnscreenText import OnscreenText

from pandac.PandaModules import TextNode

from toontown.toonbase.ToontownTimer import ToontownTimer

class CogdoMazeHud:
    LETTERS_PER_SECOND = 4.0
    NEXT_NOTIFICATION_TASK_NAME = "CogdoMazeHud_NextNotification"

    def __init__(self):
        self._initNotificationText()

    def _initNotificationText(self):
        self._notificationText = OnscreenText(
            text="",
            font=ToontownGlobals.getSignFont(),
            pos=(0, -0.8),
            scale=0.11,
            fg=(1.0, 1.0, 0.0, 1.0),
            align=TextNode.ACenter,
            mayChange=True,
            )
        self._notificationText.hide()

    def destroy(self):
        self._stopDelayedNotification()

        self._notificationText.removeNode()
        del self._notificationText

    def displayNotification(self, messageText, nextMessageText=None):
        assert messageText is not None

        self._stopDelayedNotification()

        self._notificationText["text"] = messageText
        self._notificationText.show()

        if nextMessageText is not None:
            taskMgr.doMethodLater(
                len(messageText) / CogdoMazeHud.LETTERS_PER_SECOND,
                self.displayNotification,
                CogdoMazeHud.NEXT_NOTIFICATION_TASK_NAME,
                extraArgs=[nextMessageText]
                )

    def _stopDelayedNotification(self):
        taskMgr.remove(CogdoMazeHud.NEXT_NOTIFICATION_TASK_NAME)


class CogdoMazeGuiManager:
    def __init__(self, maze):
        self.maze = maze

        self.mazeMapGui = MazeMapGui(self.maze.collisionTable)
        self.mazeMapGui.setScale(.25)
        self.mazeMapGui.setPos(1.07, 0.0, 0.73)

        self.hud = CogdoMazeHud()

        self.timer = None

    def _initTimer(self):
        self.timer = ToontownTimer()
        self.timer.hide()
        self.timer.setPos(1.16, 0, -0.83)

    def destroy(self):
        self.hud.destroy()
        self.hud = None
        self.destroyMazeMap()
        self.destroyTimer()

    def destroyMazeMap(self):
        if hasattr(self, "mazeMapGui") and self.mazeMapGui is not None:
            self.mazeMapGui.destroy()
            del self.mazeMapGui

    def destroyTimer(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer.destroy()
            self.timer = None

    def updateMazeMapPlayer(self, player, tileX, tileY):
        self.mazeMapGui.revealCell(tileX, tileY, player)

    def revealMazeMap(self):
        self.mazeMapGui.revealAll()

    def addPlayerToMazeMap(self, keyTilePos, doorTilePos, color):
        self.mazeMapGui.addPlayer(0, 0, color)
        self.mazeMapGui.addKey(keyTilePos[0], keyTilePos[1], color)
        self.mazeMapGui.addDoor(doorTilePos[0], doorTilePos[1], color)

    def showTimer(self, duration, timerExpiredCallback=None):
        if self.timer is None:
            self._initTimer()

        self.timer.setTime(duration)
        self.timer.countdown(duration, timerExpiredCallback)
        self.timer.show()

    def hideTimer(self):
        assert hasattr(self, "timer") and self.timer is not None

        self.timer.hide()
        self.timer.stop()

    def displayNotification(self, message, nextMessage=None):
        self.hud.displayNotification(message, nextMessage)
        #messenger.send(CogdoMazeAudioManager.PLAY_SFX_EVENT, ["notification"])

class CogdoMazeAudioManager(DirectObject):
    PLAY_SFX_EVENT = "CogdoMazeAudioManager_PlaySfx"

    def __init__(self):
        self.currentMusic = None

        self.music = {}
        for name, file in CogdoMazeGameGlobals.MusicFiles.items():
            self.music[name] = base.loadMusic(file)

        self.sfx = {}
        for name, file in CogdoMazeGameGlobals.SfxFiles.items():
            self.sfx[name] = loader.loadSfx(file)

        self.accept(CogdoMazeAudioManager.PLAY_SFX_EVENT, self.playSfx)

    def destroy(self):
        self.stopAll()
        self.ignoreAll()

    def stopMusic(self):
        if self.currentMusic is not None:
            self.currentMusic.stop()

    def playMusic(self, name):
        assert name in self.music.keys()

        if self.currentMusic is not None:
            self.stopMusic()

        self.currentMusic = self.music[name]
        self.currentMusic.setTime(0.0)
        self.currentMusic.setLoop(True)
        self.currentMusic.play()

    def playSfx(self, name):
        assert name in self.sfx.keys()

        self.sfx[name].play()

    def stopAll(self):
        self.stopMusic()




