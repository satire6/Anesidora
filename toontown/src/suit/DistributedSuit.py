"""DistributedSuit module: contains the DistributedSuit class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.directtools.DirectGeometry import CLAMP
from direct.task import Task
from otp.avatar import DistributedAvatar
import Suit
from toontown.toonbase import ToontownGlobals
from toontown.battle import DistributedBattle
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import SuitTimings
import SuitBase
import DistributedSuitPlanner
from direct.directnotify import DirectNotifyGlobal
import SuitDialog
from toontown.battle import BattleProps
from toontown.distributed.DelayDeletable import DelayDeletable
import math
import copy
import DistributedSuitBase
from otp.otpbase import OTPLocalizer
import random


# how far outside of a door to stop in WalkFromStreet mode before
# transitioning to ToSuitBuilding or ToToonBuilding.  This distance is
# chosen to roughly match what the DistributedDoor code expects to
# see.
STAND_OUTSIDE_DOOR         = 2.5

# how long after a suit exits a movement interruption that
# the suit ignore's local battle collisions
#
BATTLE_IGNORE_TIME       = 6
BATTLE_WAIT_TIME         = 3
CATCHUP_SPEED_MULTIPLIER = 3

# wether or not to enable battle detection when a suit
# enters bellicose mode
#
ALLOW_BATTLE_DETECT      = 1


class DistributedSuit(DistributedSuitBase.DistributedSuitBase, DelayDeletable):
    """
    DistributedSuit class:  a 'bad guy' which exists on each client's
     machine and helps direct the Suits which exist on the server.  This
     is the object that each individual player interacts with when
     initiating combat.  This guy has all of the attributes of a
     DistributedSuitAI object, plus some more such as collision info
    
    Attributes:
       Derived plus...
       DistributedSuit_initialized (integer), flag indicating if this
           suit has been properly initialized
       fsm, the state machine that this client suit will use, this
           includes states of detecting collisions with toons and
           entering battles
       timeBehind, approximately time in seconds that this suit is
           physically behind in it's path from where the server thinks
           it is, it is up to this suit to make up for this lost time
       moveLerp, used for non-interval movement, keeps track of the
           suit's current move lerp so it can be stopped at any moment
       startTime, time given to this suit from the server that indicates
           when this suit first started moving along its current path
       resumePos, a world location of where the suit last was before it
           joined a battle, when the suit resumes its course, it moves
           to this location before following the normal path again
       mtrack, the suit's current track to animate its motion.
       dna, dna created for the suit, sent to us from the server
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuit')

    # add extra info to the suit's name such as DoId and zone that the
    # suit thinks it is in
    #
    ENABLE_EXPANDED_NAME = 0

    def __init__(self, cr):
        try:
            self.DistributedSuit_initialized
            return
        except:
            self.DistributedSuit_initialized = 1
            
        DistributedSuitBase.DistributedSuitBase.__init__(self, cr)

        # our reference to the local hood's suit planner, the doId of
        # it is sent to us from the server side suit
        #
        self.spDoId = None

        # Our current path information.
        self.pathEndpointStart = 0
        self.pathEndpointEnd = 0
        self.minPathLen = 0
        self.maxPathLen = 0
        self.pathPositionIndex = 0
        self.pathPositionTimestamp = 0.0
        self.pathState = 0
        self.path = None
        self.localPathState = 0

        self.currentLeg = -1
        self.pathStartTime = 0.0
        self.legList = None

        # remember the suit's initial and end state so we dont have to
        # calculate them more than once
        #
        self.initState       = None
        self.finalState      = None

        # Indicates that the suit is in a building or not
        self.buildingSuit = 0

        # Set up the DistributedSuit state machine
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedSuit',
            [State.State('Off',
                         self.enterOff,
                         self.exitOff,
                         ['FromSky',
                          'FromSuitBuilding',
                          'Walk',
                          'Battle',
                          'neutral',
                          'ToToonBuilding',
                          'ToSuitBuilding',
                          'ToCogHQ',
                          'FromCogHQ',
                          'ToSky',
                          'FlyAway',
                          'DanceThenFlyAway',
                          'WalkToStreet',
                          'WalkFromStreet']),
             State.State('FromSky',
                         self.enterFromSky,
                         self.exitFromSky,
                         ['Walk',
                          'Battle',
                          'neutral',
                          'ToSky',
                          'WalkFromStreet']),
             State.State('FromSuitBuilding',
                         self.enterFromSuitBuilding,
                         self.exitFromSuitBuilding,
                         ['WalkToStreet',
                          'Walk',
                          'Battle',
                          'neutral',
                          'ToSky']),
             State.State('WalkToStreet',
                         self.enterWalkToStreet,
                         self.exitWalkToStreet,
                         ['Walk',
                          'Battle',
                          'neutral',
                          'ToSky',
                          'ToToonBuilding',
                          'ToSuitBuilding',
                          'ToCogHQ',
                          'WalkFromStreet']),
             State.State('WalkFromStreet',
                         self.enterWalkFromStreet,
                         self.exitWalkFromStreet,
                         ['ToToonBuilding',
                          'ToSuitBuilding',
                          'ToCogHQ',
                          'Battle',
                          'neutral',
                          'ToSky']),
             State.State('Walk',
                         self.enterWalk,
                         self.exitWalk,
                         ['WaitForBattle',
                          'Battle',
                          'neutral',
                          'WalkFromStreet',
                          'ToSky',
                          'ToCogHQ',
                          'Walk']),
             State.State('Battle',
                         self.enterBattle,
                         self.exitBattle,
                         ['Walk',
                          'ToToonBuilding',
                          'ToCogHQ',
                          'ToSuitBuilding',
                          'ToSky']),
             State.State('neutral',
                         self.enterNeutral,
                         self.exitNeutral,
                         []),
             State.State('WaitForBattle',
                         self.enterWaitForBattle,
                         self.exitWaitForBattle,
                         ['Battle',
                          'neutral',
                          'Walk',
                          'WalkToStreet',
                          'WalkFromStreet',
                          'ToToonBuilding',
                          'ToCogHQ',
                          'ToSuitBuilding',
                          'ToSky']),
             State.State('ToToonBuilding',
                         self.enterToToonBuilding,
                         self.exitToToonBuilding,
                         ['neutral', 'Battle']),
             State.State('ToSuitBuilding',
                         self.enterToSuitBuilding,
                         self.exitToSuitBuilding,
                         ['neutral', 'Battle']),
             State.State('ToCogHQ',
                         self.enterToCogHQ,
                         self.exitToCogHQ,
                         ['neutral', 'Battle']),
             State.State('FromCogHQ',
                         self.enterFromCogHQ,
                         self.exitFromCogHQ,
                         ['neutral', 'Battle', 'Walk']),
             State.State('ToSky',
                         self.enterToSky,
                         self.exitToSky,
                         ['Battle']),
             State.State('FlyAway',
                         self.enterFlyAway,
                         self.exitFlyAway,
                         []),
             State.State('DanceThenFlyAway',
                         self.enterDanceThenFlyAway,
                         self.exitDanceThenFlyAway,
                         []),
             ],
                    # Initial state
                    'Off',
                    # Final state
                    'Off',
                   )

        self.fsm.enterInitialState()
        
        self.soundSequenceList = []
        self.__currentDialogue = None
        
    def generate(self):
        DistributedSuitBase.DistributedSuitBase.generate(self)

    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        for soundSequence in self.soundSequenceList:
            soundSequence.finish()
            
        self.soundSequenceList = []
        
        self.notify.debug("DistributedSuit %d: disabling" % self.getDoId())
        self.resumePath(0)
        self.stopPathNow()
        self.setState('Off')
        DistributedSuitBase.DistributedSuitBase.disable(self)
        return

    def delete(self):
        """
        This method is called when the DistributedObject is
        permanently removed from the world and deleted from
        the cache.
        """
        try:
            self.DistributedSuit_deleted
        except:
            self.DistributedSuit_deleted = 1
            self.notify.debug("DistributedSuit %d: deleting" % self.getDoId())

            del self.fsm
            DistributedSuitBase.DistributedSuitBase.delete(self)
        return

    def setPathEndpoints(self, start, end, minPathLen, maxPathLen):
        """
        This distributed call is sent from the AI when the suit is
        created, and defines the path along the street which the suit
        should walk.

        start and end are indices into the SuitPlanner's array of
        DNASuitPoints.  With these two indices, combined with the
        minPathLen and maxPathLen constraints, we can unambiguously
        define a complete path, along with all timing information
        along that path.
        """
        if self.pathEndpointStart == start and \
           self.pathEndpointEnd == end and \
           self.minPathLen == minPathLen and \
           self.maxPathLen == maxPathLen and \
           self.path != None:
            # The path endpoints haven't changed since last time.
            # Presumably this will happen only when we re-generate a
            # suit that was previously disabled (e.g. we encounter the
            # same suit in the street that we left behind a few
            # minutes ago).

            # In this case, we need do nothing, since the path is
            # already set up from last time.
            return
            
        self.pathEndpointStart = start
        self.pathEndpointEnd = end
        self.minPathLen = minPathLen
        self.maxPathLen = maxPathLen

        self.path = None
        self.pathLength = 0
        self.currentLeg = -1
        self.legList = None
        
        if self.maxPathLen == 0:
            # If the path is empty, do nothing.  This might be the
            # case for a suit within a building, for instance.
            return

        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        self.startPoint = self.sp.pointIndexes[self.pathEndpointStart]
        self.endPoint = self.sp.pointIndexes[self.pathEndpointEnd]

        # Now determine the complete path information based on the
        # starting and ending points.
        path = self.sp.genPath(self.startPoint, self.endPoint,
                               self.minPathLen, self.maxPathLen)
        self.setPath(path)
        self.makeLegList()

    def verifySuitPlanner(self):
        """
        Ensures that this suit has a SuitPlanner set.  Normally this
        is specified at suit creation time, but sometimes the server
        farts and creates the suit before its SuitPlanner object is
        created, leaving self.sp set to None.  This function checks
        that condition and recovers from it, if possible.

        The return value is true if a suit planner is available, false
        if not.
        """
        if self.sp == None and self.spDoId != 0:
            self.notify.warning("Suit %d does not have a suit planner!  Expected SP doId %s." % (self.doId, self.spDoId))
            self.sp = self.cr.doId2do.get(self.spDoId, None)

        if self.sp == None:
            assert self.notify.debug("Cannot create path for suit %d" % (self.doId))
            return 0
        return 1

    def setPathPosition(self, index, timestamp):
        """
        setPathPosition(self, int index, uint16 timestamp)

        This distributed call comes from the AI at suit creation time,
        and every once and a while thereafter, to specify a time in
        the recent past at which the suit should have passed the
        indicated waypoint.

        Updating this information wouldn't normally be necessary--when
        the AI sends an update, we don't actually gain any new
        information--but it's important to keep the timestamp fresh,
        since we use a 16-bit timestamp, which keeps time for only
        about 5 minutes.
        """

        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        # If we didn't generate a path yet--possibly because of a
        # failed setPathEndpoints()--try again now.
        if self.path == None:
            self.setPathEndpoints(self.pathEndpointStart, self.pathEndpointEnd,
                                  self.minPathLen, self.maxPathLen)

        self.pathPositionIndex = index
        self.pathPositionTimestamp = globalClockDelta.networkToLocalTime(timestamp)
        if self.legList != None:
            self.pathStartTime = self.pathPositionTimestamp - self.legList.getStartTime(self.pathPositionIndex)
        
    def setPathState(self, state):
        """
        setPathState(self, int8 state)

        This distributed call comes from the AI at suit creation time,
        and as needed thereafter, to indicated whether the suit is
        actively walking on its path or not.  The values are:

        0 - The suit is not on its path.  Its position is controlled
        by other factors, e.g. the battle system.

        1 - The suit is actively walking on its path.  Its position is
        based on the values set by setPathEndpoints and
        setPathPosition, as well as the current time.

        2 - The suit is flying away right now.

        3 = The suit is in Tutorial Mode. It walks on a prescribed
        rectangle looking for a battle, but it has no path or path
        information. 

        4 - The suit is going to do the victory dance and then
            flying away.
        
        """
        self.pathState = state
        self.resumePath(state)

    def debugSuitPosition(self, elapsed, currentLeg, x, y, timestamp):
        """
        debugSuitPosition(self, float elapsed, int currentLeg,
                          float x, float y, timestamp)

        This distributed call comes from the AI from time to time only
        when debug-suit-positions is configured #t for the AI.  Its
        purpose is just to make noise if the client and the AI
        disagree about where the suit should be right now.
        """

        # We compare real time to frame time so we'll know how big a
        # chug we just got.  A message from the AI might have arrived
        # any time within the previous frame.
        now = globalClock.getFrameTime()
        chug = globalClock.getRealTime() - now
        messageAge = now - globalClockDelta.networkToLocalTime(timestamp, now)

        # If the message seems to come from too far in the past or the
        # future, we're probably just out of sync in general.  Nothing
        # will be reported accurately until we get back in sync.
        if messageAge < -(chug + 0.5) or messageAge > (chug + 1.0):
            print "Apparently out of sync with AI by %0.2f seconds.  Suggest resync!" % (messageAge)
            return

        localElapsed = now - self.pathStartTime

        # At messageAge seconds ago, the AI server saw the suit at
        # elapsed seconds along the path.  Right now, we see the suit
        # at localElapsed seconds along the path.  Do we agree thus
        # far?
        timeDiff = localElapsed - (elapsed + messageAge)
        if abs(timeDiff) > 0.2:
            # We disagree about where the suit is along the path.
            # This could be because we paused the AI or the client.
            print "%s (%d) appears to be %0.2f seconds out of sync along its path.  Suggest '~cogs sync'." % (self.getName(), self.getDoId(), timeDiff)
            return

        # Verify the suit's calculated (x, y) position.  This ensures
        # our path agrees with that from the AI.
        if self.legList == None:
            print "%s (%d) doesn't have a legList yet." % (self.getName(), self.getDoId())
            return
        
        netPos = Point3(x, y, 0.0)
        leg = self.legList.getLeg(currentLeg)
        calcPos = leg.getPosAtTime(elapsed - leg.getStartTime())
        calcPos.setZ(0.0)
        calcDelta = Vec3(netPos - calcPos)
        diff = calcDelta.length()
        if diff > 4.0:
            print "%s (%d) is %0.2f feet from the AI computed path!" % (self.getName(), self.getDoId(), diff)
            print "Probably your DNA files are out of sync."
            return

        # Now verify the suit's actual position.
        localPos = Point3(self.getX(), self.getY(), 0.0)

        localDelta = Vec3(netPos - localPos)
        diff = localDelta.length()
        if diff > 10.0:
            print "%s (%d) in state %s is %0.2f feet from its correct position!" % (self.getName(), self.getDoId(), self.fsm.getCurrentState().getName(), diff)
            print "Should be at (%0.2f, %0.2f), but is at (%0.2f, %0.2f)." % (x, y, localPos[0], localPos[1])
            return

        print "%s (%d) is in the correct position." % (self.getName(), self.getDoId())

    def denyBattle(self):
        DistributedSuitBase.DistributedSuitBase.denyBattle(self)

        # Since we just denied a battle on this leg, don't ask again
        # until we get to the next leg.
        self.disableBattleDetect()
        
    def resumePath(self, state):
        """
        resumePath(self, int state)

        This local call is made to temporarily set the local path
        state, independent of what the server believes the state
        should be.  See setPathState().
        """
        
        if self.localPathState != state:
            self.localPathState = state

            if state == 0:
                # Stop the suit from moving.
                self.stopPathNow()

            elif state == 1:
                # Start the suit moving.
                self.moveToNextLeg(None)

            elif state == 2:
                # Fly away right now from wherever we are.
                self.stopPathNow()
                if self.sp != None:
                    # Go to off state to make sure we can transition to flyaway
                    self.setState('Off')
                    self.setState('FlyAway')

            elif state == 3:
                pass

            elif state == 4:
                # Fly away right now from wherever we are.
                self.stopPathNow()
                if self.sp != None:
                    # Go to off state to make sure we can transition to flyaway
                    self.setState('Off')
                    self.setState('DanceThenFlyAway')

            else:
                self.notify.error("No such state as: " + str(state))

    def moveToNextLeg(self, task):
        """
        This callback function is spawned by a do-later task as each
        leg ETA is reached.  It handles moving the suit to the
        next leg, and all the bookkeeping that goes along with
        that.
        """
        if self.legList == None:
            self.notify.warning("Suit %d does not have a path!" % (self.getDoId()))
            return Task.done
        
        # First, which leg have we reached, anyway?
        now = globalClock.getFrameTime()
        elapsed = now - self.pathStartTime

        nextLeg = self.legList.getLegIndexAtTime(elapsed, self.currentLeg)
        numLegs = self.legList.getNumLegs()

        if self.currentLeg != nextLeg:
            self.currentLeg = nextLeg
            self.doPathLeg(self.legList[nextLeg], elapsed - self.legList.getStartTime(nextLeg))
            
            assert(self.notify.debug("Suit %d reached leg %d of %d." %
                                     (self.getDoId(), nextLeg, numLegs - 1)))

        # Now, which leg should we next wake up for?
        nextLeg += 1

        # Spawn another do-later to get to the next leg.
        if nextLeg < numLegs:
            nextTime = self.legList.getStartTime(nextLeg)
            delay = nextTime - elapsed
            
            name = self.taskName("move")
            taskMgr.remove(name)
            taskMgr.doMethodLater(delay, self.moveToNextLeg, name)

        return Task.done

    def doPathLeg(self, leg, time):
        """
        doPathLeg(self, SuitLeg leg, float time)

        Puts the suit on the indicated leg of its journey, and plays
        whatever animation is appropriate to that leg.  The time
        parameter represents the amount of time into the leg that has
        already elapsed.
        """

        self.fsm.request(SuitLeg.getTypeName(leg.getType()), [leg, time])
        return 0

    def stopPathNow(self):
        """
        Stops the suit wherever it is on the path.  This isn't a clean
        stop; it's then up to the caller to do something interesting
        with the suit's position and animation.
        """
        name = self.taskName("move")
        taskMgr.remove(name)
        self.currentLeg = -1

    def calculateHeading(self, a, b):
        """
        calculateHeading(self, Point3 a, Point3 b)
        
        Returns the heading component required to face the suit in the
        indicated direction to move from point a to point b.
        """
        xdelta = b[0] - a[0]
        ydelta = b[1] - a[1]

        if ydelta == 0:
            if xdelta > 0:
                return -90
            else:
                return 90

        elif xdelta == 0:
            if ydelta > 0:
                return 0
            else:
                return 180

        else:
            angle = math.atan2(ydelta, xdelta)
            return rad2Deg(angle) - 90


    def beginBuildingMove(self, moveIn, doneEvent, suit=0):
        """
        Parameters:  moveIn, 1 if move should be into building, 0 for out
                     doneEvent, event to be sent when move finished
                     suit, wether or not the building is a suit building
        
        Append an extra path section to allow for movement
        either to inside a building or from inside a
        building
        """

        # first find a point in our path so we can get a sense of direction
        # and calculate a new point in the opposite direction
        #
        doorPt = Point3(0)
        buildingPt = Point3(0)
        streetPt = Point3(0)
        if self.virtualPos:
            doorPt.assign(self.virtualPos)
        else:
            doorPt.assign(self.getPos())
        if moveIn:
            streetPt = self.prevPointPos()
        else:
            streetPt = self.currPointPos()

        # calculate a point within the building
        #
        dx = doorPt[0] - streetPt[0]
        dy = doorPt[1] - streetPt[1]
        buildingPt = Point3(doorPt[0] + dx,
                                    doorPt[1] + dy,
                                    doorPt[2])

        if moveIn:
            # if we are moving into the building, all we have to do
            # is move from the current location to the new location
            # within the building, be sure to determine if this is a
            # suit or toon building we are going into, the time it takes
            # for the move might differ
            #
            if suit:
                moveTime = SuitTimings.toSuitBuilding
            else:
                moveTime = SuitTimings.toToonBuilding
            return self.beginMove(doneEvent, buildingPt,
                                   time = moveTime)
        else:
            # if we are moving out of the building, we have to teleport
            # the suit to the new location within the building and tell the
            # suit to move to its original position outside of the building
            #
            return self.beginMove(doneEvent, doorPt, buildingPt,
                                   time=SuitTimings.fromSuitBuilding)
        return None

    def setSPDoId(self, doId):
        """
        Function:    set this suit's suit planner object from the
                     distributed object id given from the server suit
        Parameters:  doId, distributed object id of the suit planner
        """
        self.spDoId = doId
        self.sp = self.cr.doId2do.get(doId, None)
        if self.sp == None and self.spDoId != 0:
            self.notify.warning("Suit %s created before its suit planner, %d" % (self.doId, self.spDoId))


    def d_requestBattle(self, pos, hpr):
        # Make sure the local toon can't continue to run around (and
        # potentially start battles with other suits!)
        self.cr.playGame.getPlace().setState('WaitForBattle')
        self.sendUpdate('requestBattle', [pos[0], pos[1], pos[2],
                                          hpr[0], hpr[1], hpr[2]])

    def __handleToonCollision(self, collEntry):
        """
        Function:    This function is the callback for any
                     collision events that the collision sphere
                     for this bad guy might receive
        Parameters:  collEntry, the collision entry object
        """
        if not base.localAvatar.wantBattles:
            return

        toonId = base.localAvatar.getDoId()
        self.notify.debug('Distributed suit: requesting a Battle with ' +
                          'toon: %d' % toonId)
        self.d_requestBattle(self.getPos(), self.getHpr())

        # the suit on this machine only will go into wait for battle while it
        # is waiting for word back from the server about our battle request
        #
        self.setState('WaitForBattle')


    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    def setAnimState(self, state):
        """
        This is an alias for setState().  It allows Suits to go through
        doors without needing conditionals.
        """
        self.setState(state)

    # Specific State functions

    ##### Off state #####

    # Defined in DistributedSuitBase.py

    ##### FromSky state #####

    def enterFromSky(self, leg, time):
        """
        The suit is flying in from the sky.
        """
        self.enableBattleDetect('fromSky', self.__handleToonCollision)
        self.loop('neutral', 0)

        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        # Set up a track to fly us down from the sky.
        a = leg.getPosA()
        b = leg.getPosB()

        # Rotate to face in the direction we'll be walking.
        h = self.calculateHeading(a, b)
        self.setPosHprScale(a[0], a[1], a[2],
                            h, 0.0, 0.0,
                            1.0, 1.0, 1.0)

        self.mtrack = self.beginSupaFlyMove(a, 1, 'fromSky')
        self.mtrack.start(time)

    def exitFromSky(self):
        self.disableBattleDetect()
        self.mtrack.finish()
        del self.mtrack

        # Clean up stuff the SupaFly track might not have had a chance
        # to (we might have interrupted the track before it was done).
        self.detachPropeller()
    
    ##### WalkToStreet state #####

    def enterWalkToStreet(self, leg, time):
        """
        The suit is walking to the street from a door, either from a toon 
        or suit building.
        """
        self.enableBattleDetect('walkToStreet', self.__handleToonCollision)
        self.loop('walk', 0)
        
        a = leg.getPosA()
        b = leg.getPosB()

        # Adjust the vector to start just outside the door, instead of
        # intersecting it.
        delta = Vec3(b - a)
        length = delta.length()
        delta *= (length - STAND_OUTSIDE_DOOR) / length
        a1 = Point3(b - delta)
        
        # In walk-to-street mode, we might step on the sidewalk, and
        # therefore we need to use the raycast to determine our
        # correct height above the ground.
        self.enableRaycast(1)
        
        h = self.calculateHeading(a, b)
        self.setHprScale(h, 0.0, 0.0,
                         1.0, 1.0, 1.0)

        self.mtrack = Sequence(
            LerpPosInterval(self, leg.getLegTime(), b, startPos = a1),
            name = self.taskName('walkToStreet'))
        self.mtrack.start(time)

    def exitWalkToStreet(self):
        self.disableBattleDetect()
        self.enableRaycast(0)
        self.mtrack.finish()
        del self.mtrack

    ##### WalkFromStreet state #####

    # The suit is walking from the street up to a door, either a suit
    # building side door or a toon building front door.

    def enterWalkFromStreet(self, leg, time):
        self.enableBattleDetect('walkFromStreet', self.__handleToonCollision)
        self.loop('walk', 0)
        
        a = leg.getPosA()
        b = leg.getPosB()

        # Adjust the vector to start just outside the door, instead of
        # intersecting it.
        delta = Vec3(b - a)
        length = delta.length()
        delta *= (length - STAND_OUTSIDE_DOOR) / length
        b1 = Point3(a + delta)
        
        # In walk-from-street mode, we might step on the sidewalk, and
        # therefore we need to use the raycast to determine our
        # correct height above the ground.
        self.enableRaycast(1)
        
        h = self.calculateHeading(a, b)
        self.setHprScale(h, 0.0, 0.0,
                         1.0, 1.0, 1.0)

        self.mtrack = Sequence(
            LerpPosInterval(self, leg.getLegTime(), b1, startPos = a),
            name = self.taskName('walkFromStreet'))
        self.mtrack.start(time)

    def exitWalkFromStreet(self):
        self.disableBattleDetect()
        self.enableRaycast(0)
        self.mtrack.finish()
        del self.mtrack
    
    ##### Walk state #####

    # The suit is just walking around on the street, looking for
    # trouble.

    def enterWalk(self, leg, time):
        self.enableBattleDetect('bellicose', self.__handleToonCollision)
        self.loop('walk', 0)
        
        a = leg.getPosA()
        b = leg.getPosB()

        # In bellicose mode, we're always on the street.  Thus, we
        # don't need the raycast, and we can leave the height at its
        # fixed, known amount.
        
        h = self.calculateHeading(a, b)

        pos = leg.getPosAtTime(time)
        self.setPosHprScale(pos[0], pos[1], pos[2],
                            h, 0.0, 0.0,
                            1.0, 1.0, 1.0)

        self.mtrack = Sequence(
            LerpPosInterval(self, leg.getLegTime(), b, startPos = a),
            name = self.taskName('bellicose'))
        self.mtrack.start(time)

    def exitWalk(self):
        self.disableBattleDetect()
        # Here we only pause, because we might have been interrupted
        # in the middle of a walk down the block, and we'd like to
        # stay where we were.
        self.mtrack.pause()
        del self.mtrack

    ##### ToSky state #####

    # The suit is flying away into the sky, from the normal path.

    def enterToSky(self, leg, time):
        self.enableBattleDetect('toSky', self.__handleToonCollision)
        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        # Set up a track to fly us up into the sky.
        a = leg.getPosA()
        b = leg.getPosB()

        # Rotate to face in the direction we were walking.
        h = self.calculateHeading(a, b)
        self.setPosHprScale(b[0], b[1], b[2],
                            h, 0.0, 0.0,
                            1.0, 1.0, 1.0)

        self.mtrack = self.beginSupaFlyMove(b, 0, 'toSky')
        self.mtrack.start(time)

    def exitToSky(self):
        self.disableBattleDetect()
        self.mtrack.finish()
        del self.mtrack

        # Clean up stuff the SupaFly track might not have had a chance
        # to (we might have interrupted the track before it was done).
        self.detachPropeller()

    ##### FromSuitBuilding state #####

    # The suit is walking out of a suit building side door.

    def enterFromSuitBuilding(self, leg, time):
        self.enableBattleDetect('fromSuitBuilding', self.__handleToonCollision)
        self.loop('walk', 0)

        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return
        
        a = leg.getPosA()
        b = leg.getPosB()

        # Adjust the vector to stop just outside the door (the same
        # point that WalkToStreet will start at).
        delta = Vec3(b - a)
        length = delta.length()
        delta2 = delta * (self.sp.suitWalkSpeed * leg.getLegTime()) / length
        delta *= (length - STAND_OUTSIDE_DOOR) /length
        b1 = Point3(b - delta)
        a1 = Point3(b1 - delta2)
        
        # In walk-from-street mode, we might step on the sidewalk, and
        # therefore we need to use the raycast to determine our
        # correct height above the ground.
        self.enableRaycast(1)
        
        h = self.calculateHeading(a, b)
        self.setHprScale(h, 0.0, 0.0,
                         1.0, 1.0, 1.0)

        self.mtrack = Sequence(
            LerpPosInterval(self, leg.getLegTime(), b1, startPos = a1),
            name = self.taskName('fromSuitBuilding'))
        self.mtrack.start(time)

    def exitFromSuitBuilding(self):
        self.disableBattleDetect()
        self.mtrack.finish()
        del self.mtrack

    ##### ToToonBuilding state #####

    # The suit is walking through a toon building front door.

    # The DistributedDoor code actually takes over from here; this
    # state just needs to stand and wait for the door.
    
    def enterToToonBuilding(self, leg, time):
        self.loop('neutral', 0)

    def exitToToonBuilding(self):
        return
        
    ##### ToSuitBuilding state #####

    # The suit is walking through a suit building side door.

    def enterToSuitBuilding(self, leg, time):
        self.loop('walk', 0)

        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return
        
        a = leg.getPosA()
        b = leg.getPosB()

        # Adjust the vector to start just outside the door (the same
        # point that WalkFromStreet stopped at), and continue on
        # through.
        delta = Vec3(b - a)
        length = delta.length()
        delta2 = delta * (self.sp.suitWalkSpeed * leg.getLegTime()) / length
        delta *= (length - STAND_OUTSIDE_DOOR) /length
        a1 = Point3(a + delta)
        b1 = Point3(a1 + delta2)
        
        self.enableRaycast(1)
        
        h = self.calculateHeading(a, b)
        self.setHprScale(h, 0.0, 0.0,
                         1.0, 1.0, 1.0)

        self.mtrack = Sequence(
            LerpPosInterval(self, leg.getLegTime(), b1, startPos = a1),
            name = self.taskName('toSuitBuilding'))
        self.mtrack.start(time)

    def exitToSuitBuilding(self):
        self.mtrack.finish()
        del self.mtrack

    ##### ToCogHQ state #####

    # The suit is walking through a CogHQ lobby door.

    # The DistributedDoor code actually takes over from here; this
    # state just needs to stand and wait for the door.
    
    def enterToCogHQ(self, leg, time):
        self.loop('neutral', 0)

    def exitToCogHQ(self):
        return

    ##### FromCogHQ state #####

    # The suit is walking through a CogHQ lobby door.

    # The DistributedDoor code actually takes over from here; this
    # state just needs to stand and wait for the door.
    
    def enterFromCogHQ(self, leg, time):
        self.loop('neutral', 0)

        # Don't be parented to render initially (the door will
        # reparent us when it is time).
        self.detachNode()

    def exitFromCogHQ(self):
        self.reparentTo(render)

    ##### Battle state #####

    def enterBattle(self):
        DistributedSuitBase.DistributedSuitBase.enterBattle(self)
        self.resumePath(0)

    ##### Neutral state #####

    def enterNeutral(self):
        # Get ready to pass through a door.
        self.notify.debug('DistributedSuit: Neutral (entering a Door)')
        self.resumePath(0)
        self.loop('neutral', 0)

    def exitNeutral(self):
        return

    ##### WaitForBattle state #####

    def enterWaitForBattle(self):
        DistributedSuitBase.DistributedSuitBase.enterWaitForBattle(self)
        self.resumePath(0)

    ##### FlyAway state #####

    # The suit is flying away into the sky from its current position,
    # prompted by a setPathState(2) directive from the server.  This
    # is almost, but not quite, the same thing as the ToSky state.

    def enterFlyAway(self):
        self.enableBattleDetect('flyAway', self.__handleToonCollision)
        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        b = Point3(self.getPos())

        self.mtrack = self.beginSupaFlyMove(b, 0, 'flyAway')
        self.mtrack.start()

    def exitFlyAway(self):
        self.disableBattleDetect()
        self.mtrack.finish()
        del self.mtrack

        # Clean up stuff the SupaFly track might not have had a chance
        # to (we might have interrupted the track before it was done).
        self.detachPropeller()

    ##### DanceThenFlyAway state #####

    # The suit is flying away into the sky from its current position,
    # prompted by a setPathState(2) directive from the server.  This
    # is almost, but not quite, the same thing as the ToSky state.

    def enterDanceThenFlyAway(self):
        self.enableBattleDetect('danceThenFlyAway', self.__handleToonCollision)
        # If we don't have a suit planner, try again to look it up.
        if not self.verifySuitPlanner():
            return

        danceTrack = self.actorInterval('victory')

        b = Point3(self.getPos())
        flyMtrack = self.beginSupaFlyMove(b, 0, 'flyAway')
        self.mtrack = Sequence(
            danceTrack, flyMtrack,
            name = self.taskName('danceThenFlyAway'))
        self.mtrack.start()

    def exitDanceThenFlyAway(self):
        self.disableBattleDetect()
        self.mtrack.finish()
        del self.mtrack

        # Clean up stuff the SupaFly track might not have had a chance
        # to (we might have interrupted the track before it was done).
        self.detachPropeller()

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt = 1):
        if interrupt and (self.__currentDialogue is not None):
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        # If an AudioSound has been passed in, play that for dialog to
        # go along with the chat.  Interrupt any sound effect currently playing
        if dialogue:
            base.playSfx(dialogue, node=self)
        # If it is a speech-type chat message, and the avatar isn't
        # too far away to hear, play the appropriate sound effect.
        elif (chatFlags & CFSpeech) != 0:
            if (self.nametag.getNumChatPages() > 0):
                # play the dialogue sample

                # We use getChat() instead of chatString, which
                # returns just the current page of a multi-page chat
                # message.  This way we aren't fooled by long pages
                # that end in question marks.
                self.playDialogueForString(self.nametag.getChat())
                if (self.soundChatBubble != None):
                    base.playSfx(self.soundChatBubble, node=self)
            elif (self.nametag.getChatStomp() > 0 ):
                self.playDialogueForString(self.nametag.getStompText(), self.nametag.getStompDelay())
    
    def playDialogueForString(self, chatString, delay = 0.0):
        """
        Play dialogue samples to match the given chat string
        """
        if len(chatString) == 0:
            return
        # use only lower case for searching
        searchString = chatString.lower()
        # determine the statement type
        if (searchString.find(OTPLocalizer.DialogSpecial) >= 0):
            # special sound
            type = "special"
        elif (searchString.find(OTPLocalizer.DialogExclamation) >= 0):
            #exclamation
            type = "exclamation"
        elif (searchString.find(OTPLocalizer.DialogQuestion) >= 0):
            # question
            type = "question"
        else:
            # statement (use two for variety)
            if random.randint(0, 1):
                type = "statementA"
            else:
                type = "statementB"

        # determine length
        stringLength = len(chatString)
        if (stringLength <= OTPLocalizer.DialogLength1):
            length = 1
        elif (stringLength <= OTPLocalizer.DialogLength2):
            length = 2
        elif (stringLength <= OTPLocalizer.DialogLength3):
            length = 3
        else:
            length = 4

        self.playDialogue(type, length, delay)

    def playDialogue(self, type, length, delay = 0.0):
        """playDialogue(self, string, int)
        Play the specified type of dialogue for the specified time
        """

        # Inheritors may override this function or getDialogueArray(),
        # above.
        
        # Choose the appropriate sound effect.
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        
        sfxIndex = None
        if (type == "statementA" or type == "statementB"):
            if (length == 1):
                sfxIndex = 0
            elif (length == 2):
                sfxIndex = 1
            elif (length >= 3):
                sfxIndex = 2
        elif (type == "question"):
            sfxIndex = 3
        elif (type == "exclamation"):
            sfxIndex = 4
        elif (type == "special"):
            sfxIndex = 5
        else:
            notify.error("unrecognized dialogue type: ", type)
            
        if sfxIndex != None and sfxIndex < len(dialogueArray) and \
           dialogueArray[sfxIndex] != None:
            soundSequence = Sequence(Wait(delay),
                            SoundInterval(dialogueArray[sfxIndex], node = None,
                                           listenerNode = base.localAvatar,
                                           loop = 0,
                                           volume = 1.0),
                                           )
            self.soundSequenceList.append(soundSequence)
            soundSequence.start()
            
            self.cleanUpSoundList()
            
    def cleanUpSoundList(self):
        removeList = []
        for soundSequence in self.soundSequenceList:
            if soundSequence.isStopped():
                removeList.append(soundSequence)
        
        for soundSequence in removeList:
            self.soundSequenceList.remove(soundSequence)