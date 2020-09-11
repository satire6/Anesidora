from direct.distributed.ClockDelta import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import random

class TreasurePlannerAI(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        "TreasurePlannerAI")

    def __init__(self, zoneId, treasureConstructor, callback=None):
        
        self.zoneId = zoneId
        self.treasureConstructor = treasureConstructor
        # Callback should be a function that takes one argument (avId)
        # It is called when an avatar grabs a treasure so the owner of
        # the treasure planner can implement collection logic like scoring
        self.callback = callback

        # Determine the spawn points
        self.initSpawnPoints()

        # Make a parallel list of what treasures are at what spawn points.
        # None means there is no treasure there right now.
        self.treasures = []
        for spawnPoint in self.spawnPoints:
            self.treasures.append(None)

        # keep a list of the names of the treasure deletion tasks
        self.deleteTaskNames = []

        # These are used to check for a single toon grabbing several
        # treasures in a short interval--highly suspicious behavior!
        self.lastRequestId = None
        self.requestStartTime = None
        self.requestCount = None

    def initSpawnPoints(self):
        # In this function, a list of (x, y, z) tuples should be created
        # that defines all the possible places that treasure might be.
        # The list should be called self.spawnPoints
        self.spawnPoints = []
        return self.spawnPoints

    def numTreasures(self):
        counter = 0
        for treasure in self.treasures:
            if treasure:
                counter += 1
        return counter

    def countEmptySpawnPoints(self):
        counter = 0
        for treasure in self.treasures:
            if treasure == None:
                counter += 1
        return counter

    def nthEmptyIndex(self, n):
        assert(n >= 0)
        emptyCounter = -1
        spawnPointCounter = -1
        while emptyCounter < n:
            spawnPointCounter += 1
            if self.treasures[spawnPointCounter] == None:
                emptyCounter += 1
        return spawnPointCounter

    def findIndexOfTreasureId(self, treasureId):
        counter = 0
        for treasure in self.treasures:
            if treasure == None:
                pass
            else:
                if treasureId == treasure.getDoId():
                    return counter
            counter += 1
        return None

    def placeAllTreasures(self):
        index = 0
        for treasure in self.treasures:
            if not treasure:
                self.placeTreasure(index)
            index += 1

    def placeTreasure(self, index):
        # make sure this spot is empty
        assert (self.treasures[index] == None)
        
        # Get the spawn point xyz
        spawnPoint = self.spawnPoints[index]

        # Create the treasure
        treasure = self.treasureConstructor(simbase.air, self,
                                            spawnPoint[0],
                                            spawnPoint[1],
                                            spawnPoint[2])
        # Generate the treasure
        treasure.generateWithRequired(self.zoneId)
        # Record the presence of the treasure
        self.treasures[index] = treasure

    def grabAttempt(self, avId, treasureId):
        if self.lastRequestId == avId:
            self.requestCount += 1
            now = globalClock.getFrameTime()
            elapsed = now - self.requestStartTime
            if elapsed > 10:
                # Reset the counter after 10 seconds.
                self.requestCount = 1
                self.requestStartTime = now
            else:
                secondsPerGrab = elapsed / self.requestCount
                if self.requestCount >= 3 and secondsPerGrab <= 0.4:
                    simbase.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt %s treasures in %s seconds' % (self.requestCount, elapsed))
        else:
            self.lastRequestId = avId
            self.requestCount = 1
            self.requestStartTime = globalClock.getFrameTime()

        index = self.findIndexOfTreasureId(treasureId)
        if index == None:
            # If it isn't here, it isn't here. Someone else must have
            # grabbed it. 
            pass
        else:
            av = simbase.air.doId2do.get(avId)
            if av == None:
                # If avatar isn't here, do nothing
                simbase.air.writeServerEvent('suspicious', avId, 'TreasurePlannerAI.grabAttempt unknown avatar')
                self.notify.warning("avid: %s does not exist" % avId)

            else:
                # Find the treasure
                treasure = self.treasures[index]
                if treasure.validAvatar(av):
                    # Clear the slot
                    self.treasures[index] = None
                    # Call the grab callback with avId (if we have one)
                    if self.callback:
                        self.callback(avId)
                    # Tell everyone that the treasure was grabbed, and by who.
                    treasure.d_setGrab(avId)
                    # Wait five seconds, then delete the treasure
                    # I assume that five seconds is plenty of time for the treasure
                    # animation to complete on the client.
                    self.deleteTreasureSoon(treasure)
                else:
                    # Reject the attempt.
                    treasure.d_setReject()

    def deleteTreasureSoon(self, treasure):
        # Spawns a task that waits five seconds, then deletes the treasure.
        taskName = treasure.uniqueName("deletingTreasure")
        taskMgr.doMethodLater(5, self.__deleteTreasureNow, taskName,
                              extraArgs = (treasure,))
        self.deleteTaskNames.append(taskName)

    def deleteAllTreasuresNow(self):
        for treasure in self.treasures:
            if treasure:
                treasure.requestDelete()
        # we also have to manually delete all the treasures that
        # have been scheduled for deletion
        for taskName in self.deleteTaskNames:
            tasks = taskMgr.getTasksNamed(taskName)
            assert len(tasks) <= 1
            if len(tasks):
                treasure = tasks[0].getArgs()[0]
                treasure.requestDelete()
                taskMgr.remove(taskName)
        self.deleteTaskNames = []
        # Clear out the treasure list
        self.treasures = []
        for spawnPoint in self.spawnPoints:
            self.treasures.append(None)
            
    def __deleteTreasureNow(self, treasure):
        treasure.requestDelete()
