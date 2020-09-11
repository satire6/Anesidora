from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from ElevatorConstants import *
from ElevatorUtils import *
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.distributed import DistributedObject
from direct.fsm import State
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from direct.task.Task import Task
from toontown.hood import ZoneUtil
from direct.fsm.FSM import FSM


class DistributedElevatorFSM(DistributedObject.DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElevator')
    
    defaultTransitions = {
        'Off'             : [ 'Opening', 'Closed', 'Off'],
        'Opening'         : [ 'WaitEmpty', 'WaitCountdown', 'Opening', 'Closing'  ],
        'WaitEmpty'       : [ 'WaitCountdown', "Closing", "Off" ],
        'WaitCountdown'   : [ 'WaitEmpty', 'AllAboard', "Closing" ],
        'AllAboard'       : [ 'WaitEmpty', "Closing" ],
        'Closing'         : [ 'Closed', 'WaitEmpty', 'Closing', 'Opening'  ],
        'Closed'          : [ 'Opening' ],
    }
    id = 0

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.__init__( self, "Elevator_%s_FSM" % ( self.id ) )
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

        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']

        #self.setupStates()
        #self.enterInitialState()
        self.isSetup = 0
        self.__preSetupState = None
        self.bigElevator = 0
        
        self.offTrack = [None, None, None, None]
        
        self.boardingParty = None
        
        # This is bad. Testing?
        #base.elevator = self

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        
    def setBoardingParty(self, party):
        self.boardingParty = party

    def setupElevator(self):
    
        #print("setting up elevator")
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
        self.openDoors = Sequence(self.openDoors,
                                   Func(self.onDoorOpenFinish),
                                   )
        
        self.closeDoors = Sequence(self.closeDoors,
                                   Func(self.onDoorCloseFinish),
                                   )

        self.finishSetup()

    def finishSetup(self):

        # Do all the things that we had to defer until the elevator
        # was fully set up.
        self.isSetup = 1
        
        if self.__preSetupState:
            self.request(self.__preSetupState, 0)
            self.__preSetupState = None

        for slot in self.deferredSlots:
            self.fillSlot(*slot)

        self.deferredSlots = []

    def disable(self):
        #print("Elevator Disable")
        for track in  self.offTrack:
            if track:
                if track.isPlaying():
                    track.pause()
                    track = None
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
        
        # Go to the off state when the object is put in the cache
        self.request("off")
        DistributedObject.DistributedObject.disable(self)
    
    def delete(self):
        #print("Elevator Delete")
        for track in  self.offTrack:
            if track:
                if track.isPlaying():
                    track.pause()
                    track = None
        self.ignoreAll()
        if self.isSetup:
            self.elevatorSphereNodePath.removeNode()
            del self.elevatorSphereNodePath
            del self.elevatorSphereNode
            del self.elevatorSphere
            del self.bldg
            del self.leftDoor
            del self.rightDoor
            del self.openDoors
            del self.closeDoors
        #del self.fsm
        del self.openSfx
        del self.closeSfx
        self.isSetup = 0
        #FSM.delete(self)
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
        #print("REQUEST FOR STATE HAS BEEN RECEIVED %s" % (state))

        if self.isSetup:
            self.request(state, globalClockDelta.localElapsedTime(timestamp))
        else:
            #print("NOT SETUP FOOL!")
            # Save the state until we get setup.
            self.__preSetupState = state

    def fillSlot0(self, avId):
        self.fillSlot(0, avId)
    
    def fillSlot1(self, avId):
        self.fillSlot(1, avId)
    
    def fillSlot2(self, avId):
        self.fillSlot(2, avId)
    
    def fillSlot3(self, avId):
        self.fillSlot(3, avId)

    def fillSlot4(self, avId):
        self.fillSlot(4, avId)
    
    def fillSlot5(self, avId):
        self.fillSlot(5, avId)
    
    def fillSlot6(self, avId):
        self.fillSlot(6, avId)
    
    def fillSlot7(self, avId):
        self.fillSlot(7, avId)

    def fillSlot(self, index, avId):
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
            self.deferredSlots.append((index, avId))
        
        else:
            # If localToon is boarding, he needs to change state
            if avId == base.localAvatar.getDoId():
                self.localToonOnBoard = 1
                elevator = self.getPlaceElevator()
                elevator.fsm.request("boarding", [self.getElevatorModel()])
                elevator.fsm.request("boarded")

            toon = self.cr.doId2do[avId]
            # Parent it to the elevator
            toon.stopSmooth()
            # avoid wrtReparent so that we don't muck with the toon's scale
            #toon.wrtReparentTo(self.getElevatorModel())
            toon.setZ(self.getElevatorModel(), self.getScaledPoint(index)[2])
            toon.setShadowHeight(0)

            if toon.isDisguised:
                toon.suit.loop("walk")
                animFunc = Func(toon.suit.loop, "neutral")
            else:
                toon.setAnimState("run", 1.0)
                animFunc = Func(toon.setAnimState, "neutral", 1.0)
            toon.headsUp(self.getElevatorModel(), apply(Point3, self.getScaledPoint(index)))

            track = Sequence(
                # Pos 1: -1.5, 5, 0
                # Pos 2: 1.5, 5, 0
                # Pos 3: -2.5, 3, 0
                # Pos 4: 2.5, 3, 0
                LerpPosInterval(toon, TOON_BOARD_ELEVATOR_TIME * 0.75,
                                apply(Point3, self.getScaledPoint(index)),
                                other=self.getElevatorModel()),
                LerpHprInterval(toon, TOON_BOARD_ELEVATOR_TIME * 0.25,
                                Point3(180, 0, 0),
                                other=self.getElevatorModel()),
                #Func(toon.setAnimState, "neutral", 1.0),
                animFunc,
                name = toon.uniqueName("fillElevator"),
                autoPause = 1)
            track.start()

            assert avId not in self.boardedAvIds
            self.boardedAvIds[avId] = index
            #print("Boarded Av Ids %s" % (self.boardedAvIds))

    def emptySlot0(self, avId, bailFlag, timestamp):
        self.emptySlot(0, avId, bailFlag, timestamp)

    def emptySlot1(self, avId, bailFlag, timestamp):
        self.emptySlot(1, avId,  bailFlag, timestamp)

    def emptySlot2(self, avId, bailFlag, timestamp):
        self.emptySlot(2, avId,  bailFlag, timestamp)

    def emptySlot3(self, avId, bailFlag, timestamp):
        self.emptySlot(3, avId,  bailFlag, timestamp)

    def emptySlot4(self, avId, bailFlag, timestamp):
        self.emptySlot(4, avId, bailFlag, timestamp)

    def emptySlot5(self, avId, bailFlag, timestamp):
        self.emptySlot(5, avId,  bailFlag, timestamp)

    def emptySlot6(self, avId, bailFlag, timestamp):
        self.emptySlot(6, avId,  bailFlag, timestamp)

    def emptySlot7(self, avId, bailFlag, timestamp):
        self.emptySlot(7, avId,  bailFlag, timestamp)

    def notifyToonOffElevator(self, toon):
        if self.cr: #hack test
            toon.setAnimState("neutral", 1.0)
            if toon == base.localAvatar:
                print("moving the local toon off the elevator")
                doneStatus = {
                    'where' : 'exit',
                    }
                elevator = self.getPlaceElevator()
                elevator.signalDone(doneStatus)
                self.localToonOnBoard = 0
            else:
                toon.startSmooth()
            return
        else:
            #print("notifyToonOffElevator NOCR")
            pass
                
    def emptySlot(self, index, avId, bailFlag, timestamp):
        print "Emptying slot: %d for %d" % (index, avId)
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
            if self.cr.doId2do.has_key(avId):
                # See if we need to reset the clock
                # (countdown assumes we've created a clockNode already)
                if (bailFlag == 1 and hasattr(self, 'clockNode')):
                    if (timestamp < self.countdownTime and 
                        timestamp >= 0):
                        self.countdown(self.countdownTime - timestamp)
                    else:
                        self.countdown(self.countdownTime)
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
                
                if self.offTrack[index]:
                    if self.offTrack[index].isPlaying():
                        self.offTrack[index].finish()
                        self.offTrack[index] = None
 
                            
                        

                self.offTrack[index] = Sequence(
                    # TODO: Find the right coords for the elevator
                    
                    LerpPosInterval(toon, TOON_EXIT_ELEVATOR_TIME,
                                    Point3(0,-ElevatorData[self.type]['collRadius'],0),
                                    startPos = apply(Point3, self.getScaledPoint(index)),
                                    other=self.getElevatorModel()
                                    ),
                    animFunc,
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffElevator, toon),
                    name = toon.uniqueName("emptyElevator"),
                    autoPause = 1)


                # Tell localToon he is exiting (if localToon is on board)
                if avId == base.localAvatar.getDoId():
                    messenger.send("exitElevator")
                    scale = base.localAvatar.getScale()
                    self.offTrack[index].append(Func(base.camera.setScale, scale))
                    
                self.offTrack[index].start()

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

    def handleEnterSphere(self, collEntry):
        self.notify.debug("Entering Elevator Sphere....")
        print("FSMhandleEnterSphere elevator%s avatar%s" % (self.elevatorTripId, localAvatar.lastElevatorLeft))
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

    def rejectBoard(self, avId, reason = 0):
        # reason 0: unknown, 1: shuffle, 2: too low laff, 3: no seat, 4: need promotion
        # This should only be sent to us if our localToon requested
        # permission to board the elevator.
        print("rejectBoard %s" % (reason))
        if hasattr(base.localAvatar, "elevatorNotifier"):
            if reason == REJECT_SHUFFLE:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.ElevatorHoppedOff)
            elif reason == REJECT_MINLAFF:
                base.localAvatar.elevatorNotifier.showMe((TTLocalizer.ElevatorMinLaff % (self.minLaff)))
            elif reason == REJECT_PROMOTION:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.BossElevatorRejectMessage)
            elif reason == REJECT_BLOCKED_ROOM:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.ElevatorBlockedRoom) 
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
        self.sendUpdate("requestExit")

    def enterWaitCountdown(self, ts):
        self.elevatorSphereNodePath.unstash()
        # Toons may now try to board the elevator
        self.accept(self.uniqueName('enterelevatorSphere'),
                    self.handleEnterSphere)
        self.accept("elevatorExitButton", self.handleExitButton)
        self.lastState = self.state
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
        #print("distributedElevator.enterClosing")
        #print(self.lastState)
        if self.localToonOnBoard:
            elevator = self.getPlaceElevator()
            #elevator.fsm.request("elevatorClosing")
        #if not self.closeDoors.isPlaying() and self.fsm.getCurrentState().getName() != 'closing': #badLine here REMOVE IT!!!
        if self.closeDoors.isPlaying() or self.lastState == 'closed' or self.openDoors.isPlaying():
            self.doorsNeedToClose = 1
        else:
            self.doorsNeedToClose = 0
        self.closeDoors.start(ts)
        #print("closeDoors.start-eC")
        #else:
        #   self.doorsNeedToClose = 1

    def exitClosing(self):
        return
        
    def onDoorOpenFinish(self):
        #print("door open finish")
        pass

    def onDoorCloseFinish(self):
        """this is called when the elevator doors finish closing on the client
        """
        #import pdb; pdb.set_trace()
        # for any avatars that are still parented to us, remove them from the scene graph
        # so that they're not there when the doors open again
        for avId in self.boardedAvIds.keys():
            av = self.cr.doId2do.get(avId)
            if av is not None:
                if av.getParent().compareTo(self.getElevatorModel()) == 0:
                    av.detachNode()
        #self.boardedAvIds = {}

    def enterClosed(self, ts):
        #print("DistributedElevator.enterClosed %s" % (self.doId))
        #self.forceDoorsClosed()
        self.__doorsClosed(self.getZoneId())
        return

    def exitClosed(self):
        #import pdb; pdb.set_trace()
        return

    def forceDoorsOpen(self):
        #print("forcing doors open FSM")
        openDoors(self.leftDoor, self.rightDoor)


    def forceDoorsClosed(self):
        #print("DistributedElevator.forceDoorsClosed %s" % (self.doId))
        #import pdb; pdb.set_trace()
        self.closeDoors.finish()
        closeDoors(self.leftDoor, self.rightDoor)

    def enterOff(self):
        self.lastState = self.state
        return

    def exitOff(self):
        return

    def enterWaitEmpty(self, ts):
        self.lastState = self.state
        return

    def exitWaitEmpty(self):
        return
    
    def enterOpening(self, ts):
        # Open the elevator doors
        self.openDoors.start(ts)
        self.lastState = self.state
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
        self.clock.setPosHprScale(0, 4.4, 6.0,
                                  0, 0, 0,
                                  2.0, 2.0, 2.0)
        if ts < countdownTime:
            self.countdown(countdownTime - ts)

    def __doorsClosed(self, zoneId):
        assert(self.notify.debug('doorsClosed()'))
        if (self.localToonOnBoard):
            self.localAvatar.stopGlitchKiller()
            hoodId = ZoneUtil.getHoodId(zoneId)
            loader = 'suitInterior'
            where = 'suitInterior'
            if base.cr.wantCogdominiums:
                loader = 'cogdoInterior'
                where = 'cogdoInterior'
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
        if not hasattr(place, "elevator"):
            self.notify.warning("Place was in state '%s' instead of Elevator." % (place.state))
            place.detectedElevatorCollision(self)
            return None
        return place.elevator
        
    def getScaledPoint(self, index):
        point = self.elevatorPoints[index]
        #import pdb; pdb.set_trace()
        return point
        
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
        
    def getDestName(self):
        return None
    
