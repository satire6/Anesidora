from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.building import ElevatorConstants 
from toontown.building import ElevatorUtils
from toontown.building import DistributedElevatorFSM
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from direct.fsm.FSM import FSM
from direct.task import Task
from toontown.distributed import DelayDelete
from direct.showbase import PythonUtil

class DistributedClubElevator(DistributedElevatorFSM.DistributedElevatorFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedClubElevator')
    
    JumpOutOffsets = ((3, 5, 0), (1.5, 4, 0), (-1.5, 4, 0), (-3, 4, 0))
    
    defaultTransitions = {
        'Off'             : [ 'Opening', 'Closed'],
        'Opening'         : [ 'WaitEmpty', 'WaitCountdown', 'Opening', 'Closing'  ],
        'WaitEmpty'       : [ 'WaitCountdown', "Closing", "Off" ],
        'WaitCountdown'   : [ 'WaitEmpty', 'AllAboard', "Closing", 'WaitCountdown'  ],
        'AllAboard'       : [ 'WaitEmpty', "Closing" ],
        'Closing'         : [ 'Closed', 'WaitEmpty', 'Closing', 'Opening'  ],
        'Closed'          : [ 'Opening' ],
    }
    id = 0    
    
    def __init__(self, cr):
        DistributedElevatorFSM.DistributedElevatorFSM.__init__(self, cr)
        FSM.__init__( self, "ElevatorClub_%s_FSM" % ( self.id ) )
        # When we get enough information about the elevator, we can
        # set up its nametag.  The nametag points out nearby buildings
        # to the player.
        # self.type = ElevatorConstants.ELEVATOR_STAGE
        self.type = ElevatorConstants.ELEVATOR_COUNTRY_CLUB
        self.countdownTime = ElevatorConstants.ElevatorData[self.type]['countdown']
        self.nametag = None
        self.currentFloor = -1
        self.isLocked = 0
        self.isEntering = 0
        self.doorOpeningFlag = 0 #for when the door is forced closed while opening
        self.doorsNeedToClose = 0 #for when the door is forced closed while opening
        self.wantState = 0
        #self.latchRoom = None
        self.latch = None
        
        self.lastState = self.state

        self.kartModelPath = 'phase_12/models/bossbotHQ/Coggolf_cart3.bam'
        self.leftDoor = None
        self.rightDoor = None

        # Tracks on toons, for starting and stopping
        # stored by avId : track. There is only a need for one at a time,
        # in fact the point of the dict is to ensure only one is playing at a time
        self.__toonTracks = {}        

        
    def setupElevator(self):
        """setupElevator(self)
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        
        # TODO: place this on a node indexed by the entraceId
        self.elevatorModel = loader.loadModel(
            "phase_11/models/lawbotHQ/LB_ElevatorScaled")
        if not self.elevatorModel:
            self.notify.error("No Elevator Model in DistributedElevatorFloor.setupElevator. Please inform JML. Fool!")
            
        # The big cog icon on the top is only visible at the BossRoom.
        #icon = self.elevatorModel.find('**/big_frame/')
        #if not icon.isEmpty():
        #    icon.hide()

        self.leftDoor = self.elevatorModel.find("**/left-door")
        if self.leftDoor.isEmpty():
            self.leftDoor = self.elevatorModel.find("**/left_door")
            
        self.rightDoor = self.elevatorModel.find("**/right-door")
        if self.rightDoor.isEmpty():
            self.rightDoor = self.elevatorModel.find("**/right_door")

        #self.elevatorModel.setH(180)

        DistributedElevatorFSM.DistributedElevatorFSM.setupElevator(self)
        
    def generate(self):
        DistributedElevatorFSM.DistributedElevatorFSM.generate(self)
        #self.accept("LawOffice_Spec_Loaded", self.__placeElevator)
        
       # Get the state machine stuff for playGame
        self.loader = self.cr.playGame.hood.loader        
        self.golfKart = render.attachNewNode('golfKartNode')
        self.kart = loader.loadModel(self.kartModelPath)
        self.kart.setPos(0, 0, 0)
        self.kart.setScale(1)
        self.kart.reparentTo(self.golfKart)
        #self.golfKart.reparentTo(self.loader.geom)

        # Wheels
        self.wheels = self.kart.findAllMatches('**/wheelNode*')
        self.numWheels = self.wheels.getNumPaths()
        
        # temp only
        self.setPosHpr(0,0,0,0,0,0)
        
    def announceGenerate(self):
        DistributedElevatorFSM.DistributedElevatorFSM.announceGenerate(self)
        if self.latch:
            self.notify.info("Setting latch in announce generate")
            self.setLatch(self.latch)

        angle = self.startingHpr[0]
        angle -= 90
        radAngle = deg2Rad(angle)
        unitVec = Vec3( math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 45.0
        self.endPos =  self.startingPos + unitVec
        self.endPos.setZ(0.5)

        dist = Vec3(self.endPos - self.enteringPos).length()
        wheelAngle = (dist / (4.8 * 1.4 * math.pi)) * 360

        self.kartEnterAnimateInterval = Parallel(
            # start a lerp HPR for each wheel
            LerpHprInterval(self.wheels[0], 5.0, Vec3(self.wheels[0].getH(), wheelAngle, self.wheels[0].getR())),
            LerpHprInterval(self.wheels[1], 5.0, Vec3(self.wheels[1].getH(), wheelAngle, self.wheels[1].getR())),
            LerpHprInterval(self.wheels[2], 5.0, Vec3(self.wheels[2].getH(), wheelAngle, self.wheels[2].getR())),
            LerpHprInterval(self.wheels[3], 5.0, Vec3(self.wheels[3].getH(), wheelAngle, self.wheels[3].getR())),
            name = "CogKartAnimate")

        trolleyExitTrack1 = Parallel(
            LerpPosInterval(self.golfKart, 5.0, self.endPos),
            self.kartEnterAnimateInterval,
            name = "CogKartExitTrack")
        self.trolleyExitTrack = Sequence(
            trolleyExitTrack1,
            # Func(self.hideSittingToons), # we may not need this
            )

        self.trolleyEnterTrack = Sequence(
            LerpPosInterval(self.golfKart, 5.0, self.startingPos, startPos = self.enteringPos))

        self.closeDoors = Sequence(
            self.trolleyExitTrack,
            Func(self.onDoorCloseFinish))
        self.openDoors = Sequence(
            self.trolleyEnterTrack
            )

        self.setPos(0,0,0)
        
    def __placeElevator(self):
        self.notify.debug("PLACING ELEVATOR FOOL!!")
        if self.isEntering:
            elevatorNode = render.find("**/elevator_origin")
            if not elevatorNode.isEmpty():
                self.elevatorModel.setPos(0,0, 0)
                self.elevatorModel.reparentTo(elevatorNode)
            else:
                #explode
                self.notify.debug("NO NODE elevator_origin!!")
        else:
            elevatorNode = render.find("**/SlidingDoor")
            if not elevatorNode.isEmpty():
                self.elevatorModel.setPos(0,10,-15)
                self.elevatorModel.setH(180)
                self.elevatorModel.reparentTo(elevatorNode)
            else:
                #explode
                self.notify.debug("NO NODE SlidingDoor!!")
                
    def setLatch(self, markerId):
        self.notify.info("Setting latch")
        #room = self.cr.doId2do.get(roomId)
        marker = self.cr.doId2do.get(markerId)
        self.latchRequest = self.cr.relatedObjectMgr.requestObjects(
            [markerId], allCallback = self.set2Latch, timeout = 5)
        self.latch = markerId

        
    def set2Latch(self, taskMgrFooler = None):
        self.latchRequest = None
        if hasattr(self, "cr"): #might callback to dead object
            marker = self.cr.doId2do.get(self.latch)
            if marker:
                #self.elevatorModel.reparentTo(marker)
                self.getElevatorModel().reparentTo(marker)
                return
            taskMgr.doMethodLater(10.0, self._repart2Marker, "elevatorfloor-markerReparent")
            self.notify.warning("Using backup, do method later version of latch")
    
    def _repart2Marker(self, taskFoolio = 0):
        if hasattr(self, "cr") and self.cr: #might call to dead object
            marker = self.cr.doId2do.get(self.latch)
            if marker:
                #self.elevatorModel.reparentTo(marker)
                self.getElevatorModel().reparentTo(marker)
            else:
                self.notify.error("could not find latch even in defered try")
        
    def setPos(self, x, y, z):
        self.getElevatorModel().setPos(x, y, z)
    
    def setH(self, H):
        self.getElevatorModel().setH(H)
        
    def delete(self):
        self.request('Off') 
        DistributedElevatorFSM.DistributedElevatorFSM.delete(self)
        self.getElevatorModel().removeNode()
        del self.golfKart
        self.ignore("LawOffice_Spec_Loaded")
        self.ignoreAll()

    def disable(self):
        #self.clearNametag()
        self.request('Off')
        self.clearToonTracks()
        DistributedElevatorFSM.DistributedElevatorFSM.disable(self)
        
    def setEntranceId(self, entranceId):
        self.entranceId = entranceId

        # These hard coded poshprs should be replaced with nodes in the model
        if self.entranceId == 0:
            # Front of the factory (south entrance)
            self.elevatorModel.setPosHpr(62.74, -85.31, 0.00, 2.00, 0.00, 0.00)
        elif self.entranceId == 1:
            # Side of the factory (west entrance)
            self.elevatorModel.setPosHpr(-162.25, 26.43, 0.00, 269.00, 0.00, 0.00)
        else:
            self.notify.error("Invalid entranceId: %s" % entranceId)
    


    def gotBldg(self, buildingList):
        return

    def setFloor(self, floorNumber):
        # Darken the old light:
        if self.currentFloor >= 0:
            self.bldg.floorIndicator[self.currentFloor].setColor(LIGHT_OFF_COLOR)
            
        # Brighten the new light:
        if floorNumber >= 0:
            self.bldg.floorIndicator[floorNumber].setColor(LIGHT_ON_COLOR)

        # Remember the floor:
        self.currentFloor = floorNumber
    
    def handleEnterSphere(self, collEntry):
        #print("Entering Elevator Sphere....")
        # Tell localToon we are considering entering the elevator
        self.cr.playGame.getPlace().detectedElevatorCollision(self)

    def handleEnterElevator(self):
        #print("Entering Elevator....")
        # Only toons with hp can board the elevator.
        if base.localAvatar.hp > 0:
            # Tell the server that this avatar wants to board.
            toon = base.localAvatar
            self.sendUpdate("requestBoard",[])
        else:
            self.notify.warning("Tried to board elevator with hp: %d" %
                                base.localAvatar.hp)

    ##### WaitEmpty state #####

    def enterWaitEmpty(self, ts):
        self.lastState = self.state
        #print("Entering WaitEmpty %s" % (self.doId))
        self.elevatorSphereNodePath.unstash()
        self.forceDoorsOpen()
        # Toons may now try to board the elevator
        self.accept(self.uniqueName('enterelevatorSphere'),
                    self.handleEnterSphere)
        self.accept(self.uniqueName('enterElevatorOK'),
                    self.handleEnterElevator)
        DistributedElevatorFSM.DistributedElevatorFSM.enterWaitEmpty(self, ts)
        
    def exitWaitEmpty(self):
        self.lastState = self.state
        #print("Exiting WaitEmpty")
        self.elevatorSphereNodePath.stash()
        # Toons may not attempt to board the elevator if it isn't waiting
        self.ignore(self.uniqueName('enterelevatorSphere'))
        self.ignore(self.uniqueName('enterElevatorOK'))
        DistributedElevatorFSM.DistributedElevatorFSM.exitWaitEmpty(self)
        
    ##### WaitCountdown state #####

    def enterWaitCountdown(self, ts):
        self.lastState = self.state
        #print("Entering WaitCountdown")
        DistributedElevatorFSM.DistributedElevatorFSM.enterWaitCountdown(self, ts)
        self.forceDoorsOpen()
        self.accept(self.uniqueName('enterElevatorOK'),
                    self.handleEnterElevator)
        self.startCountdownClock(self.countdownTime, ts)

    def exitWaitCountdown(self):
        self.lastState = self.state
        #print("Exiting WaitCountdown")
        self.ignore(self.uniqueName('enterElevatorOK'))
        DistributedElevatorFSM.DistributedElevatorFSM.exitWaitCountdown(self)
        
    def enterClosing(self, ts):
        self.lastState = self.state
        #print("Entering Closing")
        #base.transitions.irisOut(2.0)
        taskMgr.doMethodLater(1.00, self._delayIris, "delayedIris")
        DistributedElevatorFSM.DistributedElevatorFSM.enterClosing(self, ts)
        
    def _delayIris(self, tskfooler = 0):
        base.transitions.irisOut(1.0)
        base.localAvatar.pauseGlitchKiller()
        return Task.done
        
    def kickToonsOut(self):
        #print"TOONS BEING KICKED OUT"
        if not self.localToonOnBoard:
            zoneId = self.cr.playGame.hood.hoodId                
            self.cr.playGame.getPlace().fsm.request('teleportOut', [{
                "loader": ZoneUtil.getLoaderName(zoneId),
                "where": ZoneUtil.getToonWhereName(zoneId),
                "how": "teleportIn",
                "hoodId": zoneId,
                "zoneId": zoneId,
                "shardId": None,
                "avId": -1,
                }])
        
    
    def exitClosing(self):
        self.lastState = self.state
        #print("Exiting Closing")
        DistributedElevatorFSM.DistributedElevatorFSM.exitClosing(self)
        
    def enterClosed(self, ts):
        self.lastState = self.state
        #print("Entering Closed")
        self.forceDoorsClosed()
        self.__doorsClosed(self.getZoneId())
        return
    
    def exitClosed(self):
        self.lastState = self.state
        #print("Exiting Closed")
        DistributedElevatorFSM.DistributedElevatorFSM.exitClosed(self)
        
    def enterOff(self):
        self.lastState = self.state
        #print("Entering Off")
        if self.wantState == 'closed':
            self.demand('Closing')
        elif self.wantState == 'waitEmpty':
            self.demand('WaitEmpty')
        
        DistributedElevatorFSM.DistributedElevatorFSM.enterOff(self)
        
    def exitOff(self):
        self.lastState = self.state
        #print("Exiting Off")
        DistributedElevatorFSM.DistributedElevatorFSM.exitOff(self)
    
    def enterOpening(self, ts):
        self.lastState = self.state
        #print("Entering Opening")
        DistributedElevatorFSM.DistributedElevatorFSM.enterOpening(self,ts)
        
    def exitOpening(self):
        #print("Exiting Opening")
        #print("WE ARE ACTAULLY CALLING exitOpening!!!!")
        #import pdb; pdb.set_trace()
        DistributedElevatorFSM.DistributedElevatorFSM.exitOpening(self)
        self.kickEveryoneOut()
            
        return
        
    def getZoneId(self):
        return 0

    def setBldgDoId(self, bldgDoId):
        # The doId is junk, there is no building object for the factory
        # exterior elevators. Do the appropriate things that
        # DistributedElevator.gotBldg does.
        #import pdb; pdb.set_trace()
        self.bldg = None
        self.setupElevatorKart()

    def setupElevatorKart(self):
        """Setup elevator related fields."""
        # Establish a collision sphere. There must be an easier way!
        collisionRadius = ElevatorConstants.ElevatorData[self.type]['collRadius']
        self.elevatorSphere = CollisionSphere(0, 0, 0, collisionRadius)
        self.elevatorSphere.setTangible(1)
        self.elevatorSphereNode = CollisionNode(self.uniqueName("elevatorSphere"))
        self.elevatorSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.elevatorSphereNode.addSolid(self.elevatorSphere)
        self.elevatorSphereNodePath = self.getElevatorModel().attachNewNode(
            self.elevatorSphereNode)
        self.elevatorSphereNodePath.hide()
        self.elevatorSphereNodePath.reparentTo(self.getElevatorModel())
        self.elevatorSphereNodePath.stash()

        self.boardedAvIds = {}
        self.finishSetup()
        

    def getElevatorModel(self):
        return self.elevatorModel
        
    def kickEveryoneOut(self):
        #makes the toons leave the elevator
        bailFlag = 0
        #print self.boardedAvIds
        for avId, slot in self.boardedAvIds.items():
            #print("Kicking toon out! avId %s Slot %s" % (avId, slot))
            self.emptySlot(slot, avId, bailFlag, globalClockDelta.getRealNetworkTime())
            if avId == base.localAvatar.doId:
                pass

                

    def __doorsClosed(self, zoneId):
        return
        
    def onDoorCloseFinish(self):
        """this is called when the elevator doors finish closing on the client
        """

    def setLocked(self, locked):
        self.isLocked = locked
        if locked:
            if self.state == 'WaitEmpty':
                self.request('Closing') 
            if self.countFullSeats() == 0:
                self.wantState = 'closed'
            else:
                self.wantState = 'opening'
        else:
            self.wantState = 'waitEmpty'
            if self.state == 'Closed':
                self.request('Opening') 
        
    def getLocked(self):
        return self.isLocked

    def setEntering(self, entering):
        self.isEntering = entering
        
    def getEntering(self):
        return self.isEntering
        
        
    def forceDoorsOpen(self):
        """Deliberately do nothing."""
        pass

    def forceDoorsClosed(self):
        """Deliberately do nothing."""
        pass            

    def enterOff(self):
        self.lastState = self.state
        return

    def exitOff(self):
        return
        
        
    def setLawOfficeInteriorZone(self, zoneId):
        if (self.localToonOnBoard):
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : 'factoryInterior', #should be lawOffice
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'hoodId' : hoodId,
                }
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)
    
#    def emptySlot(self, index, avId, bailFlag, timestamp):
#        pass

            
    def getElevatorModel(self):
        return self.golfKart


    def setPosHpr(self, x, y, z, h, p ,r):
        """Set the pos hpr as dictated by the AI."""
        self.startingPos = Vec3(x, y, z)
        self.enteringPos = Vec3(x, y, z - 10)
        self.startingHpr = Vec3(h, 0, 0)
        self.golfKart.setPosHpr( x, y, z, h, 0, 0 )       



    def fillSlot(self, index, avId):
        """Put someone in the kart, as dictated by the AI."""
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
            toon.wrtReparentTo(self.golfKart )

            sitStartDuration = toon.getDuration("sit-start")
            jumpTrack = self.generateToonJumpTrack(toon, index)

            track = Sequence(
                jumpTrack,
                Func(toon.setAnimState, "Sit", 1.0),
                Func(self.clearToonTrack, avId),
                name = toon.uniqueName("fillElevator"),
                autoPause = 1)
            track.delayDelete = DelayDelete.DelayDelete(toon, 'fillSlot')
            self.storeToonTrack(avId, track)
            track.start()

            assert avId not in self.boardedAvIds
            self.boardedAvIds[avId] = None


    def generateToonJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping into the golf kart."""
        av.pose('sit', 47)
        hipOffset = av.getHipsParts()[2].getPos(av)
        
        def getToonJumpTrack( av, seatIndex ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = self.golfKart):
                dest = Point3(0,0,0)
                if hasattr(self, 'golfKart') and self.golfKart:
                    dest = Vec3(self.golfKart.getPos(av.getParent()))
                    seatNode = self.golfKart.find("**/seat" + str(seatIndex + 1))
                    dest += seatNode.getPos(self.golfKart)
                    dna = av.getStyle()
                    dest -= hipOffset
                    if(seatIndex < 2):
                        dest.setY( dest.getY() + 2 * hipOffset.getY())
                    dest.setZ(dest.getZ() + 0.1)
                else:
                    self.notify.warning('getJumpDestinvalid golfKart, returning (0,0,0)') 
                return dest

            def getJumpHpr(av = av, node = self.golfKart):
                hpr = Point3(0,0,0)
                if hasattr(self, 'golfKart') and self.golfKart:
                    hpr = self.golfKart.getHpr(av.getParent())
                    if(seatIndex < 2):
                        hpr.setX( hpr.getX() + 180)
                    else:
                        hpr.setX( hpr.getX() )
                    angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                    hpr.setX(angle)
                else:
                    self.notify.warning('getJumpHpr invalid golfKart, returning (0,0,0)')                    
                return hpr

            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                   Wait( 0.43 ),
                   Parallel( LerpHprInterval( av,
                                              hpr = getJumpHpr,
                                              duration = .9 ),
                             ProjectileInterval( av,
                                                 endPos = getJumpDest,
                                                 duration = .9 )
                             ),
                   )
                )
            return toonJumpTrack

        def getToonSitTrack( av ):
            toonSitTrack = Sequence(

                ActorInterval( av, 'sit-start' ),
                Func( av.loop, 'sit' )
                )
            return toonSitTrack

        toonJumpTrack = getToonJumpTrack( av, seatIndex )
        toonSitTrack = getToonSitTrack( av )
        
        jumpTrack = Sequence(
            Parallel(
                toonJumpTrack,
                Sequence( Wait(1),
                          toonSitTrack,
                          ),
                ),
            Func( av.wrtReparentTo, self.golfKart ),            
            )
        
        return jumpTrack


    def emptySlot(self, index, avId, bailFlag, timestamp):
        """Remove someone as dictated by the AI."""
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

                sitStartDuration = toon.getDuration("sit-start")
                jumpOutTrack = self.generateToonReverseJumpTrack(toon, index)

                # Place it on the appropriate spot relative to the
                # elevator

                track = Sequence(
                    # TODO: Find the right coords for the elevator
                    jumpOutTrack,
                    Func(self.clearToonTrack, avId),
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffElevator, toon),
                    name = toon.uniqueName("emptyElevator"),
                    autoPause = 1)
                track.delayDelete = DelayDelete.DelayDelete(toon, 'ClubElevator.emptySlot')
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

    def generateToonReverseJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping out of the golf kart."""        
        self.notify.debug("av.getH() = %s" % av.getH())
        def getToonJumpTrack( av, destNode ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = destNode):
                dest = node.getPos(av.getParent())
                dest += Vec3(*self.JumpOutOffsets[seatIndex])
                return dest

            def getJumpHpr(av = av, node = destNode):
                hpr = node.getHpr(av.getParent())
                hpr.setX( hpr.getX() + 180)
                angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                hpr.setX(angle)
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                  Wait( 0.1), #43 ),
                  Parallel( #LerpHprInterval( av,
                            #                 hpr = getJumpHpr,
                            #                 duration = .9 ),
                            ProjectileInterval( av,
                                                endPos = getJumpDest,
                                                duration = .9 ) )
                  )
                )  
            return toonJumpTrack

        toonJumpTrack = getToonJumpTrack( av, self.golfKart)
        jumpTrack = Sequence(
            toonJumpTrack,
            Func( av.loop, 'neutral' ),
            Func( av.wrtReparentTo, render ),
            #Func( self.av.setPosHpr, self.exitMovieNode, 0,0,0,0,0,0 ),
            )
        return jumpTrack

    def startCountdownClock(self, countdownTime, ts):
        """Start the countdown clock."""
        # just reverse the text counter
        DistributedElevatorFSM.DistributedElevatorFSM.startCountdownClock(self, countdownTime, ts)
        self.clock.setH(self.clock.getH() + 180)


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
