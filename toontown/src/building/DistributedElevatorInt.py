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

class DistributedElevatorInt(DistributedElevator.DistributedElevator):

    def __init__(self, cr):
        DistributedElevator.DistributedElevator.__init__(self, cr)
        self.countdownTime = base.config.GetFloat('int-elevator-timeout', INTERIOR_ELEVATOR_COUNTDOWN_TIME)
    

    def setupElevator(self):
        """setupElevator(self)
        Called when the building doId is set at construction time,
        this method sets up the elevator for business.
        """
        self.leftDoor = self.bldg.leftDoorOut
        self.rightDoor = self.bldg.rightDoorOut
        DistributedElevator.DistributedElevator.setupElevator(self)

    def forcedExit(self, avId):
        # This should only be sent to us if the timer expired on the
        # elevator before we boarded.
        assert(base.localAvatar.getDoId() == avId)
        # Teleport to the last safe zone visited.
        target_sz = base.localAvatar.defaultZone
        base.cr.playGame.getPlace().fsm.request('teleportOut', [{
            "loader" : ZoneUtil.getLoaderName(target_sz),
            "where" : ZoneUtil.getWhereName(target_sz, 1),
            'how' : 'teleportIn',
            'hoodId' : target_sz,
            'zoneId' : target_sz,
            'shardId' : None,
            'avId' : -1,
            }], force = 1)

    ##### WaitCountdown state #####

    def enterWaitCountdown(self, ts):
        DistributedElevator.DistributedElevator.enterWaitCountdown(self, ts)
        # Toons may also teleport away
        self.acceptOnce("localToonLeft", self.__handleTeleportOut)
        self.startCountdownClock(self.countdownTime, ts)

    def __handleTeleportOut(self):
        # Tell the server we are leaving.
        self.sendUpdate('requestBuildingExit', [])

    def exitWaitCountdown(self):
        self.ignore("localToonLeft")
        DistributedElevator.DistributedElevator.exitWaitCountdown(self)

    def getZoneId(self):
        return self.bldg.getZoneId()

    def getElevatorModel(self):
        return self.bldg.elevatorModelOut
