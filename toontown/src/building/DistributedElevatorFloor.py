from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from ElevatorConstants import *
from ElevatorUtils import *
import DistributedElevatorFSM
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from direct.fsm.FSM import FSM
from direct.task import Task

class DistributedElevatorFloor(DistributedElevatorFSM.DistributedElevatorFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElevatorFloor')
    
    defaultTransitions = {
        'Off'             : [ 'Opening', 'Closed'],
        'Opening'         : [ 'WaitEmpty', 'WaitCountdown', 'Opening', 'Closing'  ],
        'WaitEmpty'       : [ 'WaitCountdown', "Closing" ],
        'WaitCountdown'   : [ 'WaitEmpty', 'AllAboard', "Closing", 'WaitCountdown'  ],
        'AllAboard'       : [ 'WaitEmpty', "Closing" ],
        'Closing'         : [ 'Closed', 'WaitEmpty', 'Closing', 'Opening'  ],
        'Closed'          : [ 'Opening' ],
    }
    id = 0    
    
    def __init__(self, cr):
        DistributedElevatorFSM.DistributedElevatorFSM.__init__(self, cr)
        FSM.__init__( self, "ElevatorFloor_%s_FSM" % ( self.id ) )
        # When we get enough information about the elevator, we can
        # set up its nametag.  The nametag points out nearby buildings
        # to the player.
        self.type = ELEVATOR_STAGE
        self.countdownTime = ElevatorData[self.type]['countdown']
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

        

    def setupElevator2(self):
        self.elevatorModel = loader.loadModel("phase_4/models/modules/elevator")
        #self.elevatorModel = loader.loadModel("phase_11/models/lawbotHQ/LB_Elevator")
        #self.elevatorModel.reparentTo(render)
        self.elevatorModel.reparentTo(hidden)
        self.elevatorModel.setScale(1.05)
        self.leftDoor = self.elevatorModel.find("**/left-door")
        self.rightDoor = self.elevatorModel.find("**/right-door")
        # No lights on this elevator
        self.elevatorModel.find("**/light_panel").removeNode()
        self.elevatorModel.find("**/light_panel_frame").removeNode()
        """
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        if self.isSetup:
            # If this particular elevator was previously set up, clear
            # out the old stuff and start over.
            self.elevatorSphereNodePath.removeNode()

        #self.leftDoor = self.bldg.leftDoor
        #self.rightDoor = self.bldg.rightDoor
        DistributedElevatorFSM.DistributedElevatorFSM.setupElevator(self)
        
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
        
    def announceGenerate(self):
        DistributedElevatorFSM.DistributedElevatorFSM.announceGenerate(self)
        if self.latch:
            self.notify.info("Setting latch in announce generate")
            self.setLatch(self.latch)
        
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
        if hasattr(self, "cr"): #might callback to dead object
            marker = self.cr.doId2do.get(self.latch)
            if marker:
                self.elevatorModel.reparentTo(marker)
                return
            taskMgr.doMethodLater(10.0, self._repart2Marker, "elevatorfloor-markerReparent")
            self.notify.warning("Using backup, do method later version of latch")
    
    def _repart2Marker(self, taskFoolio = 0):
        if hasattr(self, "cr"): #might call to dead object
            marker = self.cr.doId2do.get(self.latch)
            if marker:
                self.elevatorModel.reparentTo(marker)
            else:
                self.notify.error("could not find latch even in defered try")
        
    def setPos(self, x, y, z):
        self.elevatorModel.setPos(x, y, z)
    
    def setH(self, H):
        self.elevatorModel.setH(H)
        
    def delete(self):
        DistributedElevatorFSM.DistributedElevatorFSM.delete(self)
        self.elevatorModel.removeNode()
        del self.elevatorModel
        self.ignore("LawOffice_Spec_Loaded")
        self.ignoreAll()

    def disable(self):
        #self.clearNametag()
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
        self.bldg = None
        self.setupElevator()

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
        #print("forcing doors open Floor")
        openDoors(self.leftDoor, self.rightDoor)


    def forceDoorsClosed(self):
        #print("DistributedElevator.forceDoorsClosed %s" % (self.doId))
        #import pdb; pdb.set_trace()
        if self.openDoors.isPlaying():
            #print("door opening playing")
            self.doorsNeedToClose = 1
        else:
            self.closeDoors.finish()
            closeDoors(self.leftDoor, self.rightDoor)

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

            





