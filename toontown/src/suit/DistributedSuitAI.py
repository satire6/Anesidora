""" DistributedSuitAI module: contains DistributedSuitAI class"""

# AI code should not import ShowBaseGlobal because it creates a graphics window
# Use AIBaseGlobal instead
from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *

from otp.avatar import DistributedAvatarAI
import SuitTimings
from direct.task import Task
import SuitPlannerBase
import SuitBase
import SuitDialog
import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
from toontown.building import FADoorCodes
import DistributedSuitBaseAI
from toontown.hood import ZoneUtil
import random


class DistributedSuitAI(DistributedSuitBaseAI.DistributedSuitBaseAI):
    """
    /////////////////////////////////////////////////////////////////////
    // DistributedSuitAI class:  the server's version of a 'suit', this
    //  object doesnt have to worry about rendering itself, animating,
    //  or any other visual information, only 'thinking'
    //
    // Attributes:
    //     Derived plus...
    //
    /////////////////////////////////////////////////////////////////////
    """


    SUIT_BUILDINGS             =simbase.config.GetBool('want-suit-buildings',1)

    DEBUG_SUIT_POSITIONS       = simbase.config.GetBool('debug-suit-positions', 0)

    # Send an updated timestamp for each suit after about this many
    # seconds have elapsed since the last timestamp.
    UPDATE_TIMESTAMP_INTERVAL  = 180.0

    myId = 0

    # load a config file value to see if we should print out information
    # about this suit while it is thinking
    #
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitAI')

    def __init__(self, air, suitPlanner):
        """__init__(air, suitPlanner)"""
        DistributedSuitBaseAI.DistributedSuitBaseAI.__init__(self, air, 
                                                                suitPlanner)

        # the track of the suit when it comes out a certain type of a
        # building
        #
        self.bldgTrack = None

        self.branchId = None
        if suitPlanner:
            self.branchId = suitPlanner.zoneId

        self.pathEndpointStart = 0
        self.pathEndpointEnd = 0
        self.minPathLen = 0
        self.maxPathLen = 0
        self.pathPositionIndex = 0
        self.pathPositionTimestamp = 0.0
        self.pathState = 0

        self.currentLeg = 0
        self.legType = SuitLeg.TOff

        # True if this suit flew in from the sky.
        self.flyInSuit = 0

        # True if this suit walked in from a suit building.
        self.buildingSuit = 0

        # True if this suit is planning a toon building takeover.
        self.attemptingTakeover = 0

        # The block number of the building the suit is headed to,
        # either a suit or a toon building, or None.
        self.buildingDestination = None
        self.buildingDestinationIsCogdo = False

    def stopTasks(self):
        taskMgr.remove(self.taskName("flyAwayNow"))
        taskMgr.remove(self.taskName("danceNowFlyAwayLater"))
        taskMgr.remove(self.taskName("move"))
            
    def pointInMyPath(self, point, elapsedTime):
        """
        pointInMyPath(self, DNASuitPoint point, float elapsedTime)

        Returns true if the indicated DNASuitPoint is just ahead of or
        just behind the where the suit will be in elapsedTime seconds
        on his current path.  That is to say, returns true if the
        point is not suitable for another suit to start walking there.
        """
        if self.pathState != 1:
            # We're not even walking on our path.
            return 0

        then = globalClock.getFrameTime() + elapsedTime
        elapsed = then - self.pathStartTime

        if not self.sp:
            assert self.notify.error("%s: looking for point in a nonexistent suitplanner in zone %s" % (self.doId, self.zoneId))

        return self.legList.isPointInRange(point,
                                           elapsed - self.sp.PATH_COLLISION_BUFFER,
                                           elapsed + self.sp.PATH_COLLISION_BUFFER)
        

    def requestBattle(self, x, y, z, h, p, r):
        """requestBattle(x, y, z, h, p, r)
        """
        toonId = self.air.getAvatarIdFromSender()
        if self.air.doId2do.get(toonId) == None:
            # Ignore requests from unknown toons.
            return

        assert self.notify.debug("%s: request battle with toon %s in zone %s" % (self.doId, toonId, self.zoneId))

        # First make sure we're in Bellicose mode (i.e. on a Bellicose leg)
        if self.pathState == 3:
            # We are in tutorialbellicose. No brushoff needed.
            pass
        elif self.pathState != 1:
            # We're not even in path mode.  We must be in a battle already.
            if self.notify.getDebug():
                self.notify.debug('requestBattle() - suit %d not on path' % (self.getDoId()))
            if self.pathState == 2 or self.pathState == 4:
                # Or flying away.
                self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))

            self.d_denyBattle( toonId )
            return

        elif self.legType != SuitLeg.TWalk:
            # We're on a path, but not in bellicose mode.  We're
            # probably walking to or from a building.
            if self.notify.getDebug():
                self.notify.debug('requestBattle() - suit %d not in Bellicose' % (self.getDoId()))

            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle( toonId )
            return

        # Store the suit's actual pos and hpr on the client
        self.confrontPos = Point3(x, y, z)
        self.confrontHpr = Vec3(h, p, r)

        # Request a battle from the suit planner
        if (self.sp.requestBattle(self.zoneId, self, toonId)):
            if self.notify.getDebug():
                self.notify.debug( "Suit %d requesting battle in zone %d" %
                                   (self.getDoId(), self.zoneId) )
        else:
            # Suit tells toon to get lost
            if self.notify.getDebug():
                self.notify.debug('requestBattle from suit %d - denied by battle manager' % (self.getDoId()))
            self.b_setBrushOff(SuitDialog.getBrushOffIndex(self.getStyleName()))
            self.d_denyBattle( toonId )

    def getConfrontPosHpr(self):
        """ getConfrontPosHpr()
        """
        return (self.confrontPos, self.confrontHpr)

    def flyAwayNow(self):
        """
        flyAwayNow(self)

        Sends a message to all client suits to immediately start the
        fly-away animation, and then removes them a short time later.
        """
        self.b_setPathState(2)

        self.stopPathNow()  # just for good measure.
        name = self.taskName("flyAwayNow")
        taskMgr.remove(name)
        taskMgr.doMethodLater(SuitTimings.toSky, self.finishFlyAwayNow, name)

    def danceNowFlyAwayLater(self):
        """
        danceNowFlyAwayLater(self)

        Sends a message to all client suits to immediately start the
        victory dance animation for all suits, and then have them
        fly away.  The final task removes them a short time later.
        """
        self.b_setPathState(4)

        self.stopPathNow()  # just for good measure.
        name = self.taskName("danceNowFlyAwayLater")
        taskMgr.remove(name)
        taskMgr.doMethodLater(SuitTimings.victoryDance + SuitTimings.toSky,
                              self.finishFlyAwayNow, name)

    def finishFlyAwayNow(self, task):
        self.notify.debug("Suit %s finishFlyAwayNow" % (self.doId))
        self.requestRemoval()
        return Task.done

    # setSPDoId - set/get the suit planner doId for this suit, needed for
    #             the client suit so it can get access to the DNA and path
    #             information for the street it is on

    def d_setSPDoId(self, doId):
        self.sendUpdate('setSPDoId', [ doId ])

    def getSPDoId(self):
        if self.sp:
            return self.sp.getDoId()
        else:
            return 0

    def releaseControl(self):
        # Override this function from DistributedSuitBaseAI
        self.b_setPathState(0)

    # setPathEndpoints
    def b_setPathEndpoints(self, start, end, minPathLen, maxPathLen):
        self.setPathEndpoints(start, end, minPathLen, maxPathLen)
        self.d_setPathEndpoints(start, end, minPathLen, maxPathLen)

    def d_setPathEndpoints(self, start, end, minPathLen, maxPathLen):
        self.sendUpdate("setPathEndpoints", [start, end, minPathLen, maxPathLen])

    def setPathEndpoints(self, start, end, minPathLen, maxPathLen):
        self.pathEndpointStart = start
        self.pathEndpointEnd = end
        self.minPathLen = minPathLen
        self.maxPathLen = maxPathLen

    def getPathEndpoints(self):
        return (self.pathEndpointStart, self.pathEndpointEnd,
                self.minPathLen, self.maxPathLen)


    # setPathPosition
    def b_setPathPosition(self, index, timestamp):
        self.setPathPosition(index, timestamp)
        self.d_setPathPosition(index, timestamp)

    def d_setPathPosition(self, index, timestamp):
        self.notify.debug("Suit %d reaches point %d at time %0.2f" % (self.getDoId(), index, timestamp))
        self.sendUpdate("setPathPosition", [index, globalClockDelta.localToNetworkTime(timestamp)])

    def setPathPosition(self, index, timestamp):
        self.pathPositionIndex = index
        self.pathPositionTimestamp = timestamp

    def getPathPosition(self):
        return (self.pathPositionIndex,
                globalClockDelta.localToNetworkTime(self.pathPositionTimestamp))


    # setPathState
    def b_setPathState(self, state):
        self.setPathState(state)
        self.d_setPathState(state)

    def d_setPathState(self, state):
        self.sendUpdate("setPathState", [state])

    def setPathState(self, state):
        if self.pathState != state:
            self.pathState = state
            if state == 0:
                # Stop the suit from moving.
                self.stopPathNow()
            elif state == 1:
                # Start the suit moving.
                self.moveToNextLeg(None)
            elif state == 2:
                # Fly away right now from wherever we are.
                self.stopPathNow()
            elif state == 3:
                pass
            elif state == 4:
                # Do the victory dance and they fly away from wherever we are.
                self.stopPathNow()
            else:
                self.notify.error("Invalid state: " + str(state))

    def getPathState(self):
        return self.pathState

    # debugSuitPosition
    def d_debugSuitPosition(self, elapsed, currentLeg, x, y, timestamp):
        timestamp = globalClockDelta.localToNetworkTime(timestamp)
        self.sendUpdate(
                "debugSuitPosition",
                [elapsed, currentLeg, x, y, timestamp])


    def initializePath(self):
        """
        Sets up some initial parameters about the suit and its path.
        This is called by the suit planner before the suit is
        generated.
        """
        self.makeLegList()
        
        if self.notify.getDebug():
            self.notify.debug("Leg list:")
            print self.legList

        idx1 = self.startPoint.getIndex()
        idx2 = self.endPoint.getIndex()
        self.pathStartTime = globalClock.getFrameTime()

        # Tell all the clients about the suit's path and its start
        # time on that path.
        self.setPathEndpoints(idx1, idx2, self.minPathLen, self.maxPathLen)
        self.setPathPosition(0, self.pathStartTime)

        # We don't call setPathState() yet, because we haven't been
        # generated.
        self.pathState = 1

        self.currentLeg = 0

        # now be sure to properly set the suit's initial zone after setting
        # its path information and we know where the suit will be starting
        #
        self.zoneId = ZoneUtil.getTrueZoneId(self.legList.getZoneId(0), self.branchId)
        self.legType = self.legList.getType(0)

        if self.notify.getDebug():
            self.notify.debug("creating suit in zone %d" % (self.zoneId))

    def resync(self):
        """
        Broadcasts the current position of the suit to all clients who
        care.  This is mainly useful while developing, in case you
        have paused the AI or your client and you are now out of sync.
        The suits would catch up eventually anyway, on the next
        timestamp broadcast (which happens every
        UPDATE_TIMESTAMP_INTERVAL seconds), but this forces it to
        happen now for the impatient.

        The magic word "~cogs sync" calls this function on every suit
        in the current neighborhood.
        """
        self.b_setPathPosition(self.currentLeg, self.pathStartTime + self.legList.getStartTime(self.currentLeg))


    def moveToNextLeg(self, task):
        """
        This callback function is spawned by a do-later task as each
        leg ETA is reached.  It handles moving the suit to the
        next leg, and all the bookkeeping that goes along with
        that.
        """
        # First, which leg have we reached, anyway?
        now = globalClock.getFrameTime()
        elapsed = now - self.pathStartTime

        nextLeg = self.legList.getLegIndexAtTime(elapsed, self.currentLeg)
        numLegs = self.legList.getNumLegs()

        if self.currentLeg != nextLeg:
            self.currentLeg = nextLeg
            self.__beginLegType(self.legList.getType(nextLeg))
            zoneId = self.legList.getZoneId(nextLeg)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.branchId)
            self.__enterZone(zoneId)
            
            self.notify.debug("Suit %d reached leg %d of %d in zone %d." %
                              (self.getDoId(), nextLeg, numLegs - 1,
                               self.zoneId))

            if self.DEBUG_SUIT_POSITIONS:
                leg = self.legList.getLeg(nextLeg)
                pos = leg.getPosAtTime(elapsed - leg.getStartTime())
                self.d_debugSuitPosition(elapsed, nextLeg, pos[0], pos[1], now)


        # Also, make sure our position timestamp doesn't go stale.
        # Every now and then, send an updated timestamp.
        if now - self.pathPositionTimestamp > self.UPDATE_TIMESTAMP_INTERVAL:
            self.resync()

        if self.pathState != 1:
            # If we're not even in path mode, don't wait for the next zone.
            return Task.done

        # Now, which leg should we next wake up for?  Unlike the
        # client code, the AI doesn't really care about stopping for
        # every silly leg.  We only need to know about the next leg in
        # which our zoneId or type changes.
        nextLeg += 1
        while nextLeg + 1 < numLegs and \
              self.legList.getZoneId(nextLeg) == ZoneUtil.getCanonicalZoneId(self.zoneId) and \
              self.legList.getType(nextLeg) == self.legType:
            nextLeg += 1

        # Spawn another do-later to get to the next leg.
        if nextLeg < numLegs:
            nextTime = self.legList.getStartTime(nextLeg)
            delay = nextTime - elapsed

            taskMgr.remove(self.taskName("move"))
            taskMgr.doMethodLater(delay, self.moveToNextLeg, self.taskName("move"))
        else:
            # No more legs.  By now the suit has gone--flown away
            # or inside a building.
            if self.attemptingTakeover:
                # We made it inside our building!
                self.startTakeOver()
            
            #self.notify.debug("Suit %s finished walk to building" % (self.doId))
            self.requestRemoval()
        return Task.done

    def stopPathNow(self):
        """
        Stops the suit wherever it is on the path.  This isn't a clean
        stop; it's then up to the caller to do something interesting
        with the suit's position and animation.
        """
        taskMgr.remove(self.taskName("move"))

    def __enterZone(self, zoneId):
        """
        Switches the suit to the indicated zone.  Normally this is
        called by moveToNextLeg().
        """
        if zoneId != self.zoneId:
            self.sp.zoneChange(self, self.zoneId, zoneId)
            self.air.sendSetZone(self, zoneId)
            self.zoneId = zoneId

            # See if there's a battle going on in our new zone.
            if self.pathState == 1:
                self.sp.checkForBattle(zoneId, self)

    def __beginLegType(self, legType):
        """
        int legType

        Begins a new leg of the indicated type.  Normally this is
        called by moveToNextLeg().
        """
        self.legType = legType
        if legType == SuitLeg.TWalkFromStreet:
            self.checkBuildingState()
        elif legType == SuitLeg.TToToonBuilding:
            self.openToonDoor()
        elif legType == SuitLeg.TToSuitBuilding:
            self.openSuitDoor()
        elif legType == SuitLeg.TToCoghq:
            self.openCogHQDoor(1)
        elif legType == SuitLeg.TFromCoghq:
            self.openCogHQDoor(0)
            

    def resume(self):
        """
        called by battles to tell this suit that it is no
        longer part of a battle, and it should carry on.
        """
        self.notify.debug("Suit %s resume" % (self.doId))

        if self.currHP <= 0:
            # If the suit's dead, take it out.
            self.notify.debug("Suit %s dead after resume" % (self.doId))
            self.requestRemoval()
        else:
            # Otherwise, just fly away.  We could conceivably return
            # to our path from where we left off, but this is
            # complicated and doesn't seem to get us much.

            # This seems to work fine, but *something* is broken now
            # in the suit code, and this is the only thing that
            # changed.  Commenting it out for now in favor of the
            # original flyAwayNow().

            # On second thought, this is so funny we need to have it
            # in there.  Putting it back.
            self.danceNowFlyAwayLater()
            #self.flyAwayNow()

    def prepareToJoinBattle(self):
        self.b_setPathState(0)

    def interruptMove(self):
        """
        this function should be called when a suit is
        interrupted while it is walking, such as when
        the suit encounters a toon it might do battle with
        """
        SuitBase.SuitBase.interruptMove(self)

    def checkBuildingState(self):
        """
        Checks to ensure the building we're headed for is still a toon
        (or suit) building.  If not, flies away.  This is normally
        called as soon as we begin the WalkFromStreet mode.
        """
        blockNumber = self.buildingDestination
        if blockNumber == None:
            return
        
        assert self.sp.buildingMgr.isValidBlockNumber(blockNumber)

        building = self.sp.buildingMgr.getBuilding(blockNumber)

        if self.attemptingTakeover:
            if not building.isToonBlock():
                self.flyAwayNow()
                return

            if not hasattr(building, "door"):
                self.flyAwayNow()
                return

            # Don't bother checking this.  It breaks magic words, and
            # so what if we get an extra building here and there?
            #if self.sp.countNumNeededBuildings() <= 0:
            #    # We don't need any more buildings; forget it.
            #    self.flyAwayNow()
            #    return

            # Also lock the door so toons won't try to enter at the
            # last minute.
            building.door.setDoorLock(FADoorCodes.SUIT_APPROACHING)
        else:
            if not building.isSuitBlock():
                self.flyAwayNow()

    def openToonDoor(self):
        """
        Stands in front of a toon building front door and asks to be
        let in.
        """
        blockNumber = self.buildingDestination
        assert blockNumber != None
        assert self.sp.buildingMgr.isValidBlockNumber(blockNumber)

        building = self.sp.buildingMgr.getBuilding(blockNumber)
        if not building.isToonBlock():
            # Oops, it's a suit building somehow.
            self.flyAwayNow()
            return

        if not hasattr(building, "door"):
            # Hmm, no door.
            self.flyAwayNow()
            return

        building.door.requestSuitEnter(self.getDoId())


    def openSuitDoor(self):
        """
        Stands in front of a suit building side door and asks to be
        let in.
        """
        blockNumber = self.buildingDestination
        assert blockNumber != None
        assert self.sp.buildingMgr.isValidBlockNumber(blockNumber)

        building = self.sp.buildingMgr.getBuilding(blockNumber)
        if not building.isSuitBlock():
            # Oops, it's a toon building somehow.
            self.flyAwayNow()
            return

    def openCogHQDoor(self, enter):
        """
        Stands in front of a CogHQ lobby door and asks to be let in.
        """
        blockNumber = self.legList.getBlockNumber(self.currentLeg)
        try:
            door = self.sp.cogHQDoors[blockNumber]
        except:
            self.notify.error("No CogHQ door %s in zone %s" % (blockNumber, self.sp.zoneId))
            return

        if enter:
            door.requestSuitEnter(self.getDoId())
        else:
            door.requestSuitExit(self.getDoId())
            

    def startTakeOver(self):
        """
        Begins the process of taking over a toon building by a suit.
        """
        if not self.SUIT_BUILDINGS:
            return

        blockNumber = self.buildingDestination
        assert blockNumber != None
        
        if not self.sp.buildingMgr.isSuitBlock(blockNumber):
            self.notify.debug( "Suit %d taking over building %d in %d" % \
                               ( self.getDoId(), blockNumber, self.zoneId ) )
                
            difficulty = self.getActualLevel() - 1
            if self.buildingDestinationIsCogdo:
                self.sp.cogdoTakeOver(blockNumber, difficulty, self.buildingHeight)
            else:
                dept = SuitDNA.getSuitDept(self.dna.name)
                self.sp.suitTakeOver(blockNumber, dept, difficulty, self.buildingHeight)
