from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from ElevatorConstants import *
from ElevatorUtils import *
import DistributedElevator
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TeaserPanel

class DistributedElevatorExt(DistributedElevator.DistributedElevator):
    def __init__(self, cr):
        DistributedElevator.DistributedElevator.__init__(self, cr)
        # When we get enough information about the elevator, we can
        # set up its nametag.  The nametag points out nearby buildings
        # to the player.
        self.nametag = None
        self.currentFloor = -1

    def setupElevator(self):
        """
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        if self.isSetup:
            # If this particular elevator was previously set up, clear
            # out the old stuff and start over.
            self.elevatorSphereNodePath.removeNode()

        self.leftDoor = self.bldg.leftDoor
        self.rightDoor = self.bldg.rightDoor
        DistributedElevator.DistributedElevator.setupElevator(self)
        self.setupNametag()

    def disable(self):
        self.clearNametag()
        DistributedElevator.DistributedElevator.disable(self)
    
    def setupNametag(self):
        if self.nametag == None:
            self.nametag = NametagGroup()
            self.nametag.setFont(ToontownGlobals.getBuildingNametagFont())
            if TTLocalizer.BuildingNametagShadow:
                self.nametag.setShadow(*TTLocalizer.BuildingNametagShadow)
            self.nametag.setContents(Nametag.CName)
            self.nametag.setColorCode(NametagGroup.CCSuitBuilding)
            self.nametag.setActive(0)
            self.nametag.setAvatar(self.getElevatorModel())

            name = self.cr.playGame.dnaStore.getTitleFromBlockNumber(self.bldg.block)
            if not name:
                name = TTLocalizer.CogsInc
            else:
                name += TTLocalizer.CogsIncExt
                
            self.nametag.setName(name)
            self.nametag.manage(base.marginManager)

    def clearNametag(self):
        if self.nametag != None:
            self.nametag.unmanage(base.marginManager)
            self.nametag.setAvatar(NodePath())
            self.nametag = None

    def getBldgDoorOrigin(self):
        return self.bldg.getSuitDoorOrigin()

    def gotBldg(self, buildingList):
        # Do not call the super class here because we have some extra checks we need to do
        self.bldgRequest = None
        self.bldg = buildingList[0]
        if not self.bldg:
            self.notify.error("setBldgDoId: elevator %d cannot find bldg %d!"
                              % (self.doId, self.bldgDoId))
            return
        if self.getBldgDoorOrigin():
            self.bossLevel = self.bldg.getBossLevel()
            self.setupElevator()
        else:
            self.notify.warning("setBldgDoId: elevator %d cannot find suitDoorOrigin for bldg %d!"
                                % (self.doId, bldgDoId))
            # This is an elevator stuck to a toon building.  This can
            # happen from time to time if the AI crashes before it can
            # write out its .building state file, or if someone
            # removes all the .building files while the AI is down.
            # We have to handle this gracefully; we'll use the isSetup
            # flag for this purpose.
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
        self.notify.debug("Entering Elevator Sphere....")
        
        # If the localAvatar is part of a boarding group and is not a leader,
        # he is not allowed to enter the elevator - Show a message.
        if hasattr(localAvatar, "boardingParty") and \
           localAvatar.boardingParty and \
           localAvatar.boardingParty.getGroupLeader(localAvatar.doId) and \
           localAvatar.boardingParty.getGroupLeader(localAvatar.doId) != localAvatar.doId:
            base.localAvatar.elevatorNotifier.showMe(TTLocalizer.ElevatorGroupMember)
        elif self.allowedToEnter():
            # Tell localToon we are considering entering the elevator
            self.cr.playGame.getPlace().detectedElevatorCollision(self)
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='cogHQ',
                                                  doneFunc=self.handleOkTeaser)

    def handleEnterElevator(self):
        #print("EXT handleEnterSphere elevator%s avatar%s" % (self.elevatorTripId, localAvatar.lastElevatorLeft))
        
        # If the leader of the boarding group wants to enter an elevator do it the Boarding Group style.
        if hasattr(localAvatar, "boardingParty") and \
           localAvatar.boardingParty and \
           localAvatar.boardingParty.getGroupLeader(localAvatar.doId):
            # If you are the leader of the boarding group, do it the boarding group way.
            if localAvatar.boardingParty.getGroupLeader(localAvatar.doId) == localAvatar.doId:
                localAvatar.boardingParty.handleEnterElevator(self)
                        
        elif self.elevatorTripId and (localAvatar.lastElevatorLeft == self.elevatorTripId):
            self.rejectBoard(base.localAvatar.doId, REJECT_SHUFFLE)

        # Only toons with hp can board the elevator.
        elif base.localAvatar.hp > 0:
            # Tell the server that this avatar wants to board.
            toon = base.localAvatar
            self.sendUpdate("requestBoard", [])
        else:
            self.notify.warning("Tried to board elevator with hp: %d" %
                                base.localAvatar.hp)

    ##### WaitEmpty state #####

    def enterWaitEmpty(self, ts):
        self.elevatorSphereNodePath.unstash()
        self.forceDoorsOpen()
        # Toons may now try to board the elevator
        self.accept(self.uniqueName('enterelevatorSphere'),
                    self.handleEnterSphere)
        self.accept(self.uniqueName('enterElevatorOK'),
                    self.handleEnterElevator)
        DistributedElevator.DistributedElevator.enterWaitEmpty(self, ts)
        
    def exitWaitEmpty(self):
        self.elevatorSphereNodePath.stash()
        # Toons may not attempt to board the elevator if it isn't waiting
        self.ignore(self.uniqueName('enterelevatorSphere'))
        self.ignore(self.uniqueName('enterElevatorOK'))
        DistributedElevator.DistributedElevator.exitWaitEmpty(self)
        
    ##### WaitCountdown state #####

    def enterWaitCountdown(self, ts):
        DistributedElevator.DistributedElevator.enterWaitCountdown(self, ts)
        self.forceDoorsOpen()
        self.accept(self.uniqueName('enterElevatorOK'),
                    self.handleEnterElevator)
        self.startCountdownClock(self.countdownTime, ts)

    def exitWaitCountdown(self):
        self.ignore(self.uniqueName('enterElevatorOK'))
        DistributedElevator.DistributedElevator.exitWaitCountdown(self)
        
    def getZoneId(self):
        return self.bldg.interiorZoneId

    def getElevatorModel(self):
        return self.bldg.getSuitElevatorNodePath()

