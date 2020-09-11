from otp.level import DistributedEntityAI
import DistributedBarrelBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task


class DistributedMazeAI(DistributedEntityAI.DistributedEntityAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMazeAI')

    def __init__(self, level, entId):
        """Create the maze."""
        DistributedEntityAI.DistributedEntityAI.__init__(
            self, level, entId)
        self.roomDoId = level.doId
        self.GameDuration = 60.0
        self.DamageOnFailure = 20
        self.finishedList = []

    def delete(self):
        """Delete ourself and cleanup tasks."""
        self.removeAllTasks()
        DistributedEntityAI.DistributedEntityAI.delete(self)
        
    def announceGenerate(self):
        """Load fields dependent on required fields."""
        DistributedEntityAI.DistributedEntityAI.announceGenerate(self)
        self.mazeEndTimeTaskName = self.uniqueName('mazeEndTime')

    def getRoomDoId(self):
        """Return the doId of the room that contains us."""
        return self.roomDoId
        
    def setClientTriggered(self):
        """A player entered us, start the moles."""
        if not hasattr(self, 'gameStartTime'):
            self.gameStartTime = globalClock.getRealTime()
            self.b_setGameStart(globalClockDelta.localToNetworkTime(\
                            self.gameStartTime))
                            
    def b_setGameStart(self, timestamp):
        # send the distributed message first, so that any network msgs
        # sent by the subclass upon start of the game will arrive
        # after the game start msg
        self.d_setGameStart(timestamp)
        self.setGameStart(timestamp)

    def d_setGameStart(self, timestamp):
        self.notify.debug("BASE: Sending setGameStart")
        self.sendUpdate("setGameStart", [timestamp])

    def setGameStart(self, timestamp):
        """
        This method gets called when all avatars are ready
        Inheritors should call this plus the code to start the game
        """
        self.notify.debug("BASE: setGameStart")
        self.GameDuration = 35.0 + (self.numSections * 15.0)
        self.prepareForGameStartOrRestart()

    def prepareForGameStartOrRestart(self):
        """Zero out needed fields on a start or restart of the mole field."""
        self.doMethodLater(self.GameDuration, self.gameEndingTimeHit, self.mazeEndTimeTaskName  )
        
    def setFinishedMaze(self):
        senderId = self.air.getAvatarIdFromSender()
        if senderId not in self.finishedList:
            toon = simbase.air.doId2do.get(senderId)
            if toon:
                if len(self.finishedList) < 1:
                    toon.toonUp(200.0)
                else:
                    toon.toonUp(20.0)
                lastToon = 0
                if hasattr(self, 'level'):
                    numToons =  len(self.level.presentAvIds)
                    if numToons == (len(self.finishedList) + 1):
                        lastToon = 1
                self.sendUpdate("toonFinished" , [senderId, len(self.finishedList), lastToon])
                #print("toonFinished sent")
            self.finishedList.append(senderId)
        
    def gameEndingTimeHit(self, task):
        """Handle the game hitting its ending time."""
        roomId = self.getLevelDoId()
        room = simbase.air.doId2do.get(roomId)
        if room:
            playerIds = room.presentAvIds
            for avId in playerIds:
                av = simbase.air.doId2do.get(avId)
                if av and (avId not in self.finishedList):

                    self.finishedList.append(avId)
        self.sendUpdate("setGameOver", [])
        
    def damageMe(self):
        senderId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(senderId)
        roomId = self.getLevelDoId()
        room = simbase.air.doId2do.get(roomId)
        if room:
            playerIds = room.presentAvIds
            if av and (senderId in playerIds):
                av.takeDamage(self.DamageOnFailure, quietly=0)
                room.sendUpdate('forceOuch',[self.DamageOnFailure])
