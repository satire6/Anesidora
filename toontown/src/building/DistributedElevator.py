from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from ElevatorConstants import *
from ElevatorUtils import *
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from direct.fsm import State
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.task.Task import Task
from toontown.distributed import DelayDelete
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel
from toontown.building import BoardingGroupShow

class DistributedElevator(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElevator')

    # The jump offsets for a regular elevator are the same for all the slots.
    # There is a difference in jump offsets in cases like the cog kart elevators.                      
    JumpOutOffsets = JumpOutOffsets # Get the values from ElevatorConstants
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.bldgRequest = None
        self.toonRequests = {}
        self.deferredSlots = []
        self.localToonOnBoard = 0
        self.boardedAvIds = {}
        self.openSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_open.mp3")
        self.finalOpenSfx = None
        self.closeSfx = base.loadSfx("phase_5/audio/sfx/elevator_door_close.mp3")
        #Points to Elevator.Elevator when localAvatar steps inside
        self.elevatorFSM=None
        self.finalCloseSfx = None
        self.elevatorPoints = ElevatorPoints
        
        self.fillSlotTrack = None    
        
        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']

        # Tracks on toons, for starting and stopping
        # stored by avId : track. There is only a need for one at a time,
        # in fact the point of the dict is to ensure only one is playing at a time
        self.__toonTracks = {}

        self.fsm = ClassicFSM.ClassicFSM('DistributedElevator',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['opening',
                                         'waitEmpty',
                                         'waitCountdown',
                                         'closing',
                                         'closed',
                                         ]),
                            State.State('opening',
                                        self.enterOpening,
                                        self.exitOpening,
                                        ['waitEmpty', 'waitCountdown']),
                            State.State('waitEmpty',
                                        self.enterWaitEmpty,
                                        self.exitWaitEmpty,
                                        ['waitCountdown']),
                            State.State('waitCountdown',
                                        self.enterWaitCountdown,
                                        self.exitWaitCountdown,
                                        ['waitEmpty', 'closing']),
                            State.State('closing',
                                        self.enterClosing,
                                        self.exitClosing,
                                        ['closed', 'waitEmpty']),
                            State.State('closed',
                                        self.enterClosed,
                                        self.exitClosed,
                                        ['opening']),
                            ],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()
        self.isSetup = 0
        self.__preSetupState = None
        self.bigElevator = 0

        # This is bad. Testing?
        #base.elevator = self

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def setupElevator(self):
        # Assumes you have a self.leftDoor and self.rightDoor defined
        
        # Establish a collision sphere. There must be an easier way!
        collisionRadius = ElevatorData[self.type]['collRadius']
        self.elevatorSphere = CollisionSphere(0, 5, 0, collisionRadius)
        self.elevatorSphere.setTangible(0)
        self.elevatorSphereNode = CollisionNode(self.uniqueName("elevatorSphere"))
        self.elevatorSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.elevatorSphereNode.addSolid(self.elevatorSphere)
        self.elevatorSphereNodePath = self.getElevatorModel().attachNewNode(
            self.elevatorSphereNode)
        self.elevatorSphereNodePath.hide()
        self.elevatorSphereNodePath.reparentTo(self.getElevatorModel())
        self.elevatorSphereNodePath.stash()

        self.boardedAvIds = {}

        # Establish intervals for opening and closing the doors
        self.openDoors = getOpenInterval(self,
                                         self.leftDoor,
                                         self.rightDoor,
                                         self.openSfx,
                                         self.finalOpenSfx,
                                         self.type)
        
        self.closeDoors = getCloseInterval(self,
                                           self.leftDoor,
                                           self.rightDoor,
                                           self.closeSfx,
                                           self.finalCloseSfx,
                                           self.type)

        # put a callback at the end of the 'closeDoors' ival so that we can
        # hide the avatars on board. Otherwise they may still be in the
        # elevator when the doors open.
        self.closeDoors = Sequence(self.closeDoors,
                                   Func(self.onDoorCloseFinish),
                                   )

        self.finishSetup()

    def finishSetup(self):

        # Do all the things that we had to defer until the elevator
        # was fully set up.
        self.isSetup = 1
        self.offsetNP = self.getElevatorModel().attachNewNode('dummyNP')
        
        if self.__preSetupState:
            self.fsm.request(self.__preSetupState, [0])
            self.__preSetupState = None

        for slot in self.deferredSlots:
            self.fillSlot(*slot)

        self.deferredSlots = []

    def disable(self):
        if self.bldgRequest:
            self.cr.relatedObjectMgr.abortRequest(self.bldgRequest)
            self.bldgRequest = None
        for request in self.toonRequests.values():
            self.cr.relatedObjectMgr.abortRequest(request)
        self.toonRequests = {}

        # stop the intervals in case they're playing
        if hasattr(self, "openDoors"):
            self.openDoors.pause()
        if hasattr(self, "closeDoors"):
            self.closeDoors.pause()

        # No more toon animating
        self.clearToonTracks()

        # Go to the off state when the object is put in the cache
        self.fsm.request("off")
        DistributedObject.DistributedObject.disable(self)
    
    def delete(self):
        if self.isSetup:
            self.elevatorSphereNodePath.removeNode()
            del self.elevatorSphereNodePath
            del self.elevatorSphereNode
            del self.elevatorSphere
            del self.bldg
            if self.leftDoor:
                del self.leftDoor
            if self.rightDoor:
                del self.rightDoor
            if hasattr(self, "openDoors"):
                del self.openDoors
            if hasattr(self, "closeDoors"):
                del self.closeDoors
        del self.fsm
        del self.openSfx
        del self.closeSfx
        self.isSetup = 0
        
        self.offsetNP.removeNode()
        # Cleanup any leftover elevator messages while leaving the zone.
        if hasattr(base.localAvatar, "elevatorNotifier"):
            base.localAvatar.elevatorNotifier.cleanup()
        
        DistributedObject.DistributedObject.delete(self)

    def setBldgDoId(self, bldgDoId):
        self.bldgDoId = bldgDoId
        self.bldgRequest = self.cr.relatedObjectMgr.requestObjects(
            [bldgDoId], allCallback = self.gotBldg, timeout = 2)

    def gotBldg(self, buildingList):
        self.bldgRequest = None
        self.bldg = buildingList[0]
        if not self.bldg:
            self.notify.error("setBldgDoId: elevator %d cannot find bldg %d!"
                              % (self.doId, self.bldgDoId))
            return
        self.setupElevator()

    def gotToon(self, index, avId, toonList):
        request = self.toonRequests.get(index)
        if request:
            del self.toonRequests[index]
            self.fillSlot(index, avId)
        else:
            self.notify.error("gotToon: already had got toon in slot %s." % (index))
        

    def setState(self, state, timestamp):
        if self.isSetup:
            self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])
        else:
            # Save the state until we get setup.
            self.__preSetupState = state

    def fillSlot0(self, avId, wantBoardingShow):
        self.fillSlot(0, avId, wantBoardingShow)
    
    def fillSlot1(self, avId, wantBoardingShow):
        self.fillSlot(1, avId, wantBoardingShow)
    
    def fillSlot2(self, avId, wantBoardingShow):
        self.fillSlot(2, avId, wantBoardingShow)
    
    def fillSlot3(self, avId, wantBoardingShow):
        self.fillSlot(3, avId, wantBoardingShow)

    def fillSlot4(self, avId, wantBoardingShow):
        self.fillSlot(4, avId, wantBoardingShow)
    
    def fillSlot5(self, avId, wantBoardingShow):
        self.fillSlot(5, avId, wantBoardingShow)
    
    def fillSlot6(self, avId, wantBoardingShow):
        self.fillSlot(6, avId, wantBoardingShow)
    
    def fillSlot7(self, avId, wantBoardingShow):
        self.fillSlot(7, avId, wantBoardingShow)
    
    def fillSlot(self, index, avId, wantBoardingShow = 0):
        self.notify.debug("%s.fillSlot(%s, %s, ...)" % (self.doId, index, avId))
        request = self.toonRequests.get(index)
        if request:
            self.cr.relatedObjectMgr.abortRequest(request)
            del self.toonRequests[index]
            
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass

        elif not self.cr.doId2do.has_key(avId):
            # It's someone who hasn't been generated yet.
            func = PythonUtil.Functor(
                self.gotToon, index, avId)
                                      
            assert not self.toonRequests.has_key(index)
            self.toonRequests[index] = self.cr.relatedObjectMgr.requestObjects(
                [avId], allCallback = func)

        elif not self.isSetup:
            # We haven't set up the elevator yet.
            self.deferredSlots.append((index, avId, wantBoardingShow))
        
        else:
            # If localToon is boarding, he needs to change state
            if avId == base.localAvatar.getDoId():
                place = base.cr.playGame.getPlace()
                if not place:
                    return
                place.detectedElevatorCollision(self)
                elevator = self.getPlaceElevator()                
                if elevator == None:
                    place.fsm.request('elevator')
                    elevator = self.getPlaceElevator()
                if not elevator:
                    return
                
                self.localToonOnBoard = 1
                
                if hasattr(localAvatar, "boardingParty") and localAvatar.boardingParty:
                    localAvatar.boardingParty.forceCleanupInviteePanel()
                    localAvatar.boardingParty.forceCleanupInviterPanels()
                
                # Cleanup any leftover elevator messages before boarding the elevator.
                if hasattr(base.localAvatar, "elevatorNotifier"):
                    base.localAvatar.elevatorNotifier.cleanup()
                
                cameraTrack = Sequence()
                # Move the camera towards and face the elevator.        
                cameraTrack.append(Func(elevator.fsm.request, "boarding", [self.getElevatorModel()]))
                # Enable the Hop off button.
                cameraTrack.append(Func(elevator.fsm.request, "boarded"))

            toon = self.cr.doId2do[avId]
            # Parent it to the elevator
            toon.stopSmooth()
            # avoid wrtReparent so that we don't muck with the toon's scale
            #toon.wrtReparentTo(self.getElevatorModel())
            
            if not wantBoardingShow:
                toon.setZ(self.getElevatorModel(), self.elevatorPoints[index][2])
                toon.setShadowHeight(0)

            if toon.isDisguised:
                animInFunc = Sequence(Func(toon.suit.loop, "walk"))
                #RAU this stops the dog's ears from flapping too much
                animFunc = Sequence(
                    Func(toon.setAnimState, "neutral", 1.0),
                    Func(toon.suit.loop, "neutral")
                    )
            else:
                animInFunc = Sequence(Func(toon.setAnimState, "run", 1.0))
                animFunc = Func(toon.setAnimState, "neutral", 1.0)
            toon.headsUp(self.getElevatorModel(), apply(Point3, self.elevatorPoints[index]))

            track = Sequence(
                # Pos 1: -1.5, 5, 0
                # Pos 2: 1.5, 5, 0
                # Pos 3: -2.5, 3, 0
                # Pos 4: 2.5, 3, 0
                animInFunc,
                LerpPosInterval(toon, TOON_BOARD_ELEVATOR_TIME * 0.75,
                                apply(Point3, self.elevatorPoints[index]),
                                other=self.getElevatorModel()),
                LerpHprInterval(toon, TOON_BOARD_ELEVATOR_TIME * 0.25,
                                Point3(180, 0, 0),
                                other=self.getElevatorModel()),
                #Func(toon.setAnimState, "neutral", 1.0),
                Func(self.clearToonTrack, avId),
                animFunc,
                name = toon.uniqueName("fillElevator"),
                autoPause = 1)
            
            if wantBoardingShow:
                boardingTrack, boardingTrackType = self.getBoardingTrack(toon, index, False)
                track = Sequence(boardingTrack, track)
                
                if avId == base.localAvatar.getDoId():
                    cameraWaitTime = 2.5
                    if (boardingTrackType == BoardingGroupShow.TRACK_TYPE_RUN):
                        cameraWaitTime = 0.5
                    elif (boardingTrackType == BoardingGroupShow.TRACK_TYPE_POOF):
                        cameraWaitTime = 1
                    cameraTrack = Sequence(Wait(cameraWaitTime), cameraTrack)
                
            if self.canHideBoardingQuitBtn(avId):
                track = Sequence(Func(localAvatar.boardingParty.groupPanel.disableQuitButton), 
                                 track)
                
            # Start the camera track in parallel here
            if avId == base.localAvatar.getDoId():
                track = Parallel(cameraTrack, track)
                
            track.delayDelete = DelayDelete.DelayDelete(toon, 'Elevator.fillSlot')
            self.storeToonTrack(avId, track)
            track.start()
            
            self.fillSlotTrack = track

            assert avId not in self.boardedAvIds
            self.boardedAvIds[avId] = None

    def emptySlot0(self, avId, bailFlag, timestamp, time):
        self.emptySlot(0, avId, bailFlag, timestamp, time)

    def emptySlot1(self, avId, bailFlag, timestamp, time):
        self.emptySlot(1, avId,  bailFlag, timestamp, time)

    def emptySlot2(self, avId, bailFlag, timestamp, time):
        self.emptySlot(2, avId,  bailFlag, timestamp, time)

    def emptySlot3(self, avId, bailFlag, timestamp, time):
        self.emptySlot(3, avId,  bailFlag, timestamp, time)

    def emptySlot4(self, avId, bailFlag, timestamp, time):
        self.emptySlot(4, avId, bailFlag, timestamp, time)

    def emptySlot5(self, avId, bailFlag, timestamp, time):
        self.emptySlot(5, avId,  bailFlag, timestamp)

    def emptySlot6(self, avId, bailFlag, timestamp, time):
        self.emptySlot(6, avId,  bailFlag, timestamp, time)

    def emptySlot7(self, avId, bailFlag, timestamp, time):
        self.emptySlot(7, avId,  bailFlag, timestamp, time)

    def notifyToonOffElevator(self, toon):
        toon.setAnimState("neutral", 1.0)
        if toon == base.localAvatar:
            doneStatus = {
                'where' : 'exit',
                }
            elevator = self.getPlaceElevator()
            if elevator:
                elevator.signalDone(doneStatus)
            self.localToonOnBoard = 0
        else:
            toon.startSmooth()
        return
                
    def emptySlot(self, index, avId, bailFlag, timestamp, timeSent = 0):        
        if self.fillSlotTrack:
            self.fillSlotTrack.finish()
            self.fillSlotTrack = None
        
        #print "Emptying slot: %d for %d" % (index, avId)
        # If localToon is exiting, he needs to change state
        if avId == 0:
            # This means that no one is currently exiting, and no action
            # should be taken
            pass

        elif not self.isSetup:
            # We haven't set up the elevator yet.  Remove the toon
            # from the deferredSlots list, if it is there.
            newSlots = []
            for slot in self.deferredSlots:
                if slot[0] != index:
                    newSlots.append(slot)
                    
            self.deferredSlots = newSlots

        else:
            timeToSet = self.countdownTime
            if timeSent > 0:
                timeToSet = timeSent
            if self.cr.doId2do.has_key(avId):
                # See if we need to reset the clock
                # (countdown assumes we've created a clockNode already)
                if (bailFlag == 1 and hasattr(self, 'clockNode')):
                    if (timestamp < timeToSet and 
                        timestamp >= 0):
                        self.countdown(timeToSet - timestamp)
                    else:
                        self.countdown(timeToSet)
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # avoid wrtReparent so that we don't muck with the toon's scale
                ## Parent it to render
                #toon.wrtReparentTo(render)
                toon.stopSmooth()

                if toon.isDisguised:
                    toon.suit.loop("walk")
                    animFunc = Func(toon.suit.loop, "neutral")
                else:
                    toon.setAnimState("run", 1.0)
                    animFunc = Func(toon.setAnimState, "neutral", 1.0)

                # Place it on the appropriate spot relative to the
                # elevator
                track = Sequence(
                    # TODO: Find the right coords for the elevator
                    LerpPosInterval(toon, TOON_EXIT_ELEVATOR_TIME,
                                    Point3(*self.JumpOutOffsets[index]),
                                    other=self.getElevatorModel()
                                    ),
                    animFunc,
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffElevator, toon),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("emptyElevator"),
                    autoPause = 1)
                
                if self.canHideBoardingQuitBtn(avId):
                    # Enable the Boarding Group Panel Quit Button here if it is relevant.
                    track.append(Func(localAvatar.boardingParty.groupPanel.enableQuitButton))
                    # Enable the Boarding Group GO Button here if it is relevant.
                    track.append(Func(localAvatar.boardingParty.enableGoButton))
                
                track.delayDelete = DelayDelete.DelayDelete(toon, 'Elevator.emptySlot')
                self.storeToonTrack(avId, track)
                track.start()

                # Tell localToon he is exiting (if localToon is on board)
                if avId == base.localAvatar.getDoId():
                    messenger.send("exitElevator")

                # if the elevator is generated as a toon is leaving it,
                # we will not have gotten a corresponding 'fillSlot' message
                # for that toon, hence the toon will not be found in
                # boardedAvIds
                if avId in self.boardedAvIds:
                    del self.boardedAvIds[avId]

            else:
                self.notify.warning("toon: " + str(avId) +
                                                  " doesn't exist, and" +
                                                  " cannot exit the elevator!")

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            return True
        return False

    def handleEnterSphere(self, collEntry):
        self.notify.debug("Entering Elevator Sphere....")
        #print("handleEnterSphere elevator%s avatar%s" % (self.elevatorTripId, localAvatar.lastElevatorLeft))
        if self.allowedToEnter():
            if self.elevatorTripId and (localAvatar.lastElevatorLeft == self.elevatorTripId):
                #print("NO BACKCIES!")
                self.rejectBoard(base.localAvatar.doId, REJECT_SHUFFLE)

            # Only toons with hp can board the elevator.
            elif base.localAvatar.hp > 0:
                # Put localToon into requestBoard mode.
                self.cr.playGame.getPlace().detectedElevatorCollision(self)
                # Tell the server that this avatar wants to board.
                toon = base.localAvatar
                self.sendUpdate("requestBoard",[])
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='cogHQ',
                                                  doneFunc=self.handleOkTeaser)
    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')            

    def rejectBoard(self, avId, reason = 0):
        # This should only be sent to us if our localToon requested
        # permission to board the elevator.
        # reason 0: unknown, 1: shuffle, 2: too low laff, 3: no seat, 4: need promotion
        print("rejectBoard %s" % (reason))
        if hasattr(base.localAvatar, "elevatorNotifier"):
            if reason == REJECT_SHUFFLE:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.ElevatorHoppedOff)
            elif reason == REJECT_MINLAFF:
                base.localAvatar.elevatorNotifier.showMe((TTLocalizer.ElevatorMinLaff % (self.minLaff)))
            elif reason == REJECT_PROMOTION:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.BossElevatorRejectMessage)
            elif reason == REJECT_NOT_YET_AVAILABLE:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.NotYetAvailable)
        assert(base.localAvatar.getDoId() == avId)
        
        doneStatus = {
                'where' : 'reject',
                }
        elevator = self.getPlaceElevator()
        if elevator:
            elevator.signalDone(doneStatus)

    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        timeStr = str(countdownTime)

        if self.clockNode.getText() != timeStr:
            self.clockNode.setText(timeStr)

        if task.time >= task.duration:
            return Task.done
        else:
            return Task.cont

    def countdown(self, duration):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = duration
        taskMgr.remove(self.uniqueName("elevatorTimerTask"))
        return taskMgr.add(countdownTask, self.uniqueName("elevatorTimerTask"))

    def handleExitButton(self):
        # This gets called when the exit button gets pushed.
        localAvatar.lastElevatorLeft = self.elevatorTripId
        self.sendUpdate("requestExit")

    def enterWaitCountdown(self, ts):
        self.elevatorSphereNodePath.unstash()
        # Toons may now try to board the elevator
        self.accept(self.uniqueName('enterelevatorSphere'),
                    self.handleEnterSphere)
        self.accept("elevatorExitButton", self.handleExitButton)
        return

    def exitWaitCountdown(self):
        self.elevatorSphereNodePath.stash()
        # Toons may not attempt to board the elevator if it isn't waiting
        self.ignore(self.uniqueName('enterelevatorSphere'))
        self.ignore("elevatorExitButton")
        self.ignore("localToonLeft")
        # Stop the countdown clock...
        taskMgr.remove(self.uniqueName("elevatorTimerTask"))
        self.clock.removeNode()
        del self.clock
        del self.clockNode

    def enterClosing(self, ts):
        # Close the elevator doors
        if self.localToonOnBoard:
            elevator = self.getPlaceElevator()
            if elevator:
                elevator.fsm.request("elevatorClosing")
        self.closeDoors.start(ts)

    def exitClosing(self):
        return

    def onDoorCloseFinish(self):
        """this is called when the elevator doors finish closing on the client
        """
        # for any avatars that are still parented to us, remove them from the scene graph
        # so that they're not there when the doors open again
        for avId in self.boardedAvIds.keys():
            av = self.cr.doId2do.get(avId)
            if av is not None:
                if av.getParent().compareTo(self.getElevatorModel()) == 0:
                    av.detachNode()
        self.boardedAvIds = {}

    def enterClosed(self, ts):
        self.forceDoorsClosed()
        self.__doorsClosed(self.getZoneId())
        return

    def exitClosed(self):
        return

    def forceDoorsOpen(self):
        openDoors(self.leftDoor, self.rightDoor)

    def forceDoorsClosed(self):
        self.closeDoors.finish()
        closeDoors(self.leftDoor, self.rightDoor)

    def enterOff(self):
        return

    def exitOff(self):
        return

    def enterWaitEmpty(self, ts):
        return

    def exitWaitEmpty(self):
        return
    
    def enterOpening(self, ts):
        # Open the elevator doors
        self.openDoors.start(ts)
        return

    def exitOpening(self):
        return

    def startCountdownClock(self, countdownTime, ts):
        # Start the countdown clock...
        self.clockNode = TextNode("elevatorClock")
        self.clockNode.setFont(ToontownGlobals.getSignFont())
        self.clockNode.setAlign(TextNode.ACenter)
        self.clockNode.setTextColor(0.5, 0.5, 0.5, 1)
        self.clockNode.setText(str(int(countdownTime)))
        self.clock = self.getElevatorModel().attachNewNode(self.clockNode)
        # TODO: Get the right coordinates for the elevator clock.
        self.clock.setPosHprScale(0, 2.0, 7.5,
                                  0, 0, 0,
                                  2.0, 2.0, 2.0)
        if ts < countdownTime:
            self.countdown(countdownTime - ts)

    def _getDoorsClosedInfo(self):
        # return loader, where strings
        return 'suitInterior', 'suitInterior'

    def __doorsClosed(self, zoneId):
        assert(self.notify.debug('doorsClosed()'))
        if (self.localToonOnBoard):
            hoodId = ZoneUtil.getHoodId(zoneId)
            loader, where = self._getDoorsClosedInfo()
            doneStatus = {
                'loader' : loader,
                'where' : where,
                'hoodId' : hoodId,
                'zoneId' : zoneId,
                'shardId' : None,
                }

            elevator = self.elevatorFSM #self.getPlaceElevator()
            del self.elevatorFSM
            elevator.signalDone(doneStatus)

    def getElevatorModel(self):
        self.notify.error("getElevatorModel: pure virtual -- inheritors must override")
        
    def getPlaceElevator(self):
        place = self.cr.playGame.getPlace()
        if place:
            if hasattr(place, "elevator"):
                return place.elevator
            else:
                self.notify.warning("Place was in state '%s' instead of Elevator." % (place.fsm.getCurrentState().getName()))
                place.detectedElevatorCollision(self)
        else:
            self.notify.warning("Place didn't exist")
        return None
        
    def setElevatorTripId(self, id):
        self.elevatorTripId = id
        
    def getElevatorTripId(self):
        return self.elevatorTripId
        
    def setAntiShuffle(self, antiShuffle):
        self.antiShuffle = antiShuffle

    def getAntiShuffle(self):
        return self.antiShuffle

    def setMinLaff(self, minLaff):
        self.minLaff = minLaff

    def getMinLaff(self):
        return self.minLaff
    
    def storeToonTrack(self, avId, track):
        # Clear out any currently playing tracks on this toon
        self.clearToonTrack(avId)
        # Store this new one
        self.__toonTracks[avId] = track

    def clearToonTrack(self, avId):
        # Clear out any currently playing tracks on this toon
        oldTrack = self.__toonTracks.get(avId)
        if oldTrack:
            oldTrack.pause()
            if self.__toonTracks.get(avId):
                DelayDelete.cleanupDelayDeletes(self.__toonTracks[avId])
                del self.__toonTracks[avId]

    def clearToonTracks(self):
        #We can't use an iter because we are deleting keys
        keyList = []
        for key in self.__toonTracks:
            keyList.append(key)
            
        for key in keyList:
            if self.__toonTracks.has_key(key):
                self.clearToonTrack(key)
                
    def getDestName(self):
        return None

    def getOffsetPos(self, seatIndex = 0):
        """
        Get the offset position to where the toon might have to
        teleport to or run to.
        Note: This is the pos reletive to the elevator.
        """
        return self.JumpOutOffsets[seatIndex]
    
    def getOffsetPosWrtToonParent(self, toon, seatIndex = 0):
        """
        Get the offset position to where the toon might have to
        teleport to or run to.
        Note: This is the pos reletive to the toon parent.
        """
        self.offsetNP.setPos(apply(Point3, self.getOffsetPos(seatIndex)))
        return self.offsetNP.getPos(toon.getParent())
    
    def getOffsetPosWrtRender(self, seatIndex = 0):
        """
        Get the offset position to where the toon might have to
        teleport to or run to.
        Note: This is the pos reletive to the render.
        """
        self.offsetNP.setPos(apply(Point3, self.getOffsetPos(seatIndex)))
        return self.offsetNP.getPos(render)
    
    def canHideBoardingQuitBtn(self, avId):
        if (avId == localAvatar.doId) and \
           hasattr(localAvatar, "boardingParty") and \
           localAvatar.boardingParty and \
           localAvatar.boardingParty.groupPanel:
            return True
        else:
            return False
        
    def getBoardingTrack(self, toon, seatIndex, wantToonRotation):
        '''
        Return an interval of the toon teleporting in front of the elevator.
        Note: The offset (second parameter passed to BoardingGroupShow.getBoardingTrack
        is to where the toon will teleport/run to. This offset has to be
        calculated wrt the parent of the toon.
        Eg: For the CogKart the offset should be computed wrt to the cogKart because the
            toon is parented to the cogKart.
            For the other elevators the offset should be computer wrt to render because the
            toon is parented to render.
        '''
        self.boardingGroupShow = BoardingGroupShow.BoardingGroupShow(toon)
        track, trackType = self.boardingGroupShow.getBoardingTrack(self.getElevatorModel(), 
                                                       self.getOffsetPosWrtToonParent(toon, seatIndex), 
                                                       self.getOffsetPosWrtRender(seatIndex),
                                                       wantToonRotation)
        return (track, trackType)
