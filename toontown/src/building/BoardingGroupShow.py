from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from toontown.toonbase import TTLocalizer
from toontown.effects import DustCloud

TRACK_TYPE_TELEPORT = 1
TRACK_TYPE_RUN = 2
TRACK_TYPE_POOF = 3

class BoardingGroupShow:
    notify = DirectNotifyGlobal.directNotify.newCategory('BoardingGroupShow')

    thresholdRunDistance = 25.0
    
    def __init__(self, toon):
        self.toon = toon
        self.avId = self.toon.doId
        self.dustCloudIval = None
        if __debug__:
            base.bgs = self

    def cleanup(self):
        # Cleanup only for the local avatar.
        if (localAvatar.doId == self.avId):
            self.__stopTimer()
            self.clock.removeNode()

    def startTimer(self):
##        ts = globalClockDelta.localElapsedTime(timestamp)
        # Start the countdown clock...
        self.clockNode = TextNode("elevatorClock")
        self.clockNode.setFont(ToontownGlobals.getSignFont())
        self.clockNode.setAlign(TextNode.ACenter)
        self.clockNode.setTextColor(0.5, 0.5, 0.5, 1)
        self.clockNode.setText(str(int(self.countdownDuration)))
        self.clock = aspect2d.attachNewNode(self.clockNode)
        
        # TODO: Get the right coordinates for the elevator clock.
    ##        self.clock.setPosHprScale(0, 2.0, 7.5,
    ##                                  0, 0, 0,
    ##                                  2.0, 2.0, 2.0)

        self.clock.setPos(0, 0, -0.6)
        self.clock.setScale(0.15, 0.15, 0.15)

##        if ts < countdownTime:
##            self.__countdown(countdownTime - ts, self.__boardingElevatorTimerExpired)
        self.__countdown(self.countdownDuration, self.__boardingElevatorTimerExpired)

    def __countdown(self, duration, callback):
        """
        Spawn the timer task for duration seconds.
        Calls callback when the timer is up
        """
        self.countdownTask = Task(self.__timerTask)
        self.countdownTask.duration = duration
        self.countdownTask.callback = callback

        taskMgr.remove(self.uniqueName(self.avId))
        return taskMgr.add(self.countdownTask, self.uniqueName(self.avId))

    def __timerTask(self, task):
        """
        This is the task for the countdown.
        """
        countdownTime = int(task.duration - task.time)
        timeStr = self.timeWarningText + str(countdownTime)

        if self.clockNode.getText() != timeStr:
            self.clockNode.setText(timeStr)

        if task.time >= task.duration:
            # Time is up, call the callback and return Task.done
            if task.callback:
                task.callback()
            return Task.done
        else:
            return Task.cont

    def __boardingElevatorTimerExpired(self):
        """
        This is where the control goes as soon as the countdown finishes.
        """
        self.notify.debug('__boardingElevatorTimerExpired')
        self.clock.removeNode()

    def __stopTimer(self):
        """
        Get rid of any countdowns
        """
        if self.countdownTask:
            self.countdownTask.callback = None
            taskMgr.remove(self.countdownTask)

    def uniqueName(self, avId):
        """
        Here we're making our own uniqueName method, each avId's sequence should be unique.
        """
        uniqueName = "boardingElevatorTimerTask-" + str(avId)
        return uniqueName

    def getBoardingTrack(self, elevatorModel, offset, offsetWrtRender, wantToonRotation):
        """
        Return an interval of the toon teleporting/running to the front of the elevator.
        This method is called from the elevator.
        Note: The offset is to where the toon will teleport/run to. This offset has to be
        calculated wrt the parent of the toon.
        Eg: For the CogKart the offset should be computed wrt to the cogKart because the
            toon is parented to the cogKart.
            For the other elevators the offset should be computer wrt to render because the
            toon is parented to render.
        """
        self.timeWarningText = TTLocalizer.BoardingTimeWarning
        self.countdownDuration = 6
        trackType = TRACK_TYPE_TELEPORT
        boardingTrack = Sequence()
        # Do anything only if the toon exists.
        if self.toon:            
            # Do the whole timer only for the local avatar
            if (self.avId == localAvatar.doId):
                boardingTrack.append(Func(self.startTimer))
            
            isInThresholdDist = self.__isInThresholdDist(elevatorModel, offset, self.thresholdRunDistance)
            isRunPathClear = self.__isRunPathClear(elevatorModel, offsetWrtRender)
            
            if isInThresholdDist and isRunPathClear:
                boardingTrack.append(self.__getRunTrack(elevatorModel, offset, wantToonRotation))
                trackType = TRACK_TYPE_RUN
            else:
                if self.toon.isDisguised:
                    boardingTrack.append(self.__getPoofTeleportTrack(elevatorModel, offset, wantToonRotation))
                    trackType = TRACK_TYPE_POOF
                else:
                    boardingTrack.append(self.__getTeleportTrack(elevatorModel, offset, wantToonRotation))
            
        # Else return an empty boarding track.
        else:
            pass
        
        # Cleanup whatever you have created in this class at the end of the interval.
        # We don't need this object any more.
        boardingTrack.append(Func(self.cleanup))
        
        return (boardingTrack, trackType)
    
    def __getOffsetPos(self, elevatorModel, offset):
        """
        Get the offset position to where the toon might have to
        teleport to or run to.
        Note: This is the pos reletive to the elevator.
        """
        dest = elevatorModel.getPos(self.toon.getParent())
        dest += Vec3(*offset)        
        return dest
    
    def __getTeleportTrack(self, elevatorModel, offset, wantToonRotation):
        """
        We get the teleport track when the toon is outside the 
        threshold distance away from the elevator.
        The Teleport Track is an interval of the toon teleporting to the
        elevator seat's offset position. After it reaches the offset position
        the boarding the elevator animation takes over.
        """       
        teleportTrack = Sequence()
        # Do anything only if the toon exists.
        if self.toon:
            if wantToonRotation:
                teleportTrack.append(Func(self.toon.headsUp, elevatorModel, offset))
            teleportTrack.append(Func(self.toon.setAnimState, 'TeleportOut'))
            teleportTrack.append(Wait(3.5))
            teleportTrack.append(Func(self.toon.setPos, Point3(offset)))
            teleportTrack.append(Func(self.toon.setAnimState, 'TeleportIn'))
            teleportTrack.append(Wait(1))
            
        # Else return an empty teleport track.
        else:
            pass
        return teleportTrack
    
    def __getPoofTeleportTrack(self, elevatorModel, offset, wantToonRotation):
        """
        We get the poof teleport track when the toon is outside the 
        threshold distance away from the elevator 
        and when the toon is disguised in a cog suit.
        The Poof Teleport Track is an interval of the toon poofing out 
        and poofing into the elevator seat's offset position. 
        After it reaches the offset position
        the boarding the elevator animation takes over.
        """
        teleportTrack = Sequence()
        
        if wantToonRotation:
            teleportTrack.append(Func(self.toon.headsUp, elevatorModel, offset))
        
        def getDustCloudPos():
            toonPos = self.toon.getPos(render)
            return Point3(toonPos.getX(), toonPos.getY(), toonPos.getZ() + 3)
        
        def cleanupDustCloudIval():
            if self.dustCloudIval:
                self.dustCloudIval.finish()
                self.dustCloudIval = None
        
        def getDustCloudIval():
            # Clean up any dust cloud before starting another one
            cleanupDustCloudIval()
            
            dustCloud = DustCloud.DustCloud(fBillboard = 0,wantSound = 1)
            dustCloud.setBillboardAxis(2.)
            dustCloud.setZ(3)
            dustCloud.setScale(0.4)
            dustCloud.createTrack()
            
            self.dustCloudIval =  Sequence(Func(dustCloud.reparentTo, render),
                Func(dustCloud.setPos, getDustCloudPos()),
                dustCloud.track,
                Func(dustCloud.detachNode),
                Func(dustCloud.destroy),
                name = 'dustCloadIval'
                )
            self.dustCloudIval.start()
        
        # Do anything only if the toon exists.
        if self.toon:
            teleportTrack.append(Func(self.toon.setAnimState, 'neutral'))
            teleportTrack.append(Wait(0.5))
            teleportTrack.append(Func(getDustCloudIval))
            teleportTrack.append(Wait(0.25))
            teleportTrack.append(Func(self.toon.hide))
            teleportTrack.append(Wait(1.5))
            teleportTrack.append(Func(self.toon.setPos, Point3(offset)))
            teleportTrack.append(Func(getDustCloudIval))
            teleportTrack.append(Wait(0.25))
            teleportTrack.append(Func(self.toon.show))
            teleportTrack.append(Wait(0.5))
            # Clean up the dust cloud interval once it is done.
            teleportTrack.append(Func(cleanupDustCloudIval))
            
        # Else return an empty teleport track.
        else:
            pass
        return teleportTrack
    
    def __getRunTrack(self, elevatorModel, offset, wantToonRotation):
        """
        We get the run track when the toon is within the threshold distance
        away from the elevator.
        The Run Track is an interval of the toon running to the
        elevator seat's offset position. After it reaches the offset position
        the boarding the elevator animation takes over.
        """
        runTrack = Sequence()
        # Do anything only if the toon exists.
        if self.toon:
            if wantToonRotation:
                runTrack.append(Func(self.toon.headsUp, elevatorModel, offset))
            
            if self.toon.isDisguised:
                runTrack.append(Func(self.toon.suit.loop, "walk"))
            else:
                runTrack.append(Func(self.toon.setAnimState, 'run'))
            runTrack.append(LerpPosInterval(self.toon, 1, Point3(offset)))
        
        # Else return an empty run track.
        else:
            pass
        
        return runTrack
    
    def __isInThresholdDist(self, elevatorModel, offset, thresholdDist):
        """
        Checks to see if the toon is within the threshold distance
        from the elevator.
        """
        diff = Point3(offset) - self.toon.getPos()
        
        if (diff.length() > thresholdDist):
            return False
        else:
            return True
        
    def __isRunPathClear(self, elevatorModel, offsetWrtRender):
        pathClear = True
        source = self.toon.getPos(render)
        dest = offsetWrtRender
        
        # Shoot collision ray from toon to elevator
        collSegment = CollisionSegment(source[0], source[1], source[2],
                                       dest[0], dest[1], dest[2])
        fromObject = render.attachNewNode(CollisionNode('runCollSegment'))
        fromObject.node().addSolid(collSegment)
        fromObject.node().setFromCollideMask(ToontownGlobals.WallBitmask)
        fromObject.node().setIntoCollideMask(BitMask32.allOff())
        
        queue = CollisionHandlerQueue()
        base.cTrav.addCollider(fromObject, queue)
        base.cTrav.traverse(render)
        queue.sortEntries()
        if queue.getNumEntries():
            # Go through all the collision entries
            for entryNum in xrange(queue.getNumEntries()):
                entry = queue.getEntry(entryNum)
                hitObject = entry.getIntoNodePath()            
                # This collision ray might collide against another toon standing in front of it
                # Ignore any toon, including self toon
                # Every toon has a netTag('pieCode') = 3
                if (hitObject.getNetTag('pieCode') != '3'):
                    # This must be a something with a wall bit mask that is not a toon
                    pathClear = False
                            
        base.cTrav.removeCollider(fromObject)
        fromObject.removeNode()
        return pathClear
    
    def getGoButtonShow(self, elevatorName):
        """
        Return an interval of the toon teleporting out with the time.
        This method is called from DistributedBoardingParty.
        """
        self.elevatorName = elevatorName
        self.timeWarningText = TTLocalizer.BoardingGoShow %self.elevatorName
        self.countdownDuration = 4
        goButtonShow = Sequence()
        # Do anything only if the toon exists.
        if self.toon:
            # Do the whole timer only for the local avatar
            if (self.avId == localAvatar.doId):
                goButtonShow.append(Func(self.startTimer))
            goButtonShow.append(self.__getTeleportOutTrack())
            goButtonShow.append(Wait(3))
        # Cleanup whatever you have created in this class at the end of the interval.
        # We don't need this object any more.
        goButtonShow.append(Func(self.cleanup))
        return goButtonShow
        
    def __getTeleportOutTrack(self):
        """
        Return an interval of the toon teleporting out.
        """
        teleportOutTrack = Sequence()
        # Do anything only if the toon exists.
        if self.toon and not self.toon.isDisguised:
            teleportOutTrack.append(Func(self.toon.b_setAnimState, 'TeleportOut'))
        return teleportOutTrack
    
    def getGoButtonPreShow(self):
        """
        Return an interval showing time left for the pre show.
        """
        self.timeWarningText = TTLocalizer.BoardingGoPreShow
        self.countdownDuration = 4
        goButtonPreShow = Sequence()
        # Do anything only if the toon exists.
        if self.toon:
            # Do the whole timer only for the local avatar
            if (self.avId == localAvatar.doId):
                goButtonPreShow.append(Func(self.startTimer))
                goButtonPreShow.append(Wait(3))
        # Cleanup whatever you have created in this class at the end of the interval.
        # We don't need this object any more.
        goButtonPreShow.append(Func(self.cleanup))
        return goButtonPreShow