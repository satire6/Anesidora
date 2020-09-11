from otp.ai.AIBaseGlobal import *
from GoonGlobals import *

from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
from toontown.coghq import DistributedCrushableEntityAI
import GoonPathData
from direct.distributed import ClockDelta
import random
from direct.task import Task

class DistributedGoonAI(DistributedCrushableEntityAI.DistributedCrushableEntityAI):
    """
    A simple, dumb robot.
    The robot should be flexible and reusable, for uses in CogHQ basements
    and factories, and perhaps other parts of the game.  Let the goon's
    movement, discovery, and attack methods be modular, so different behavior
    types can be easily plugged in.
    """

    # Send an updated timestamp for each suit after about this many
    # seconds have elapsed since the last timestamp.
    UPDATE_TIMESTAMP_INTERVAL  = 180.0

    # How long does the goon remain stunned?
    STUN_TIME = 4

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoonAI')

    def __init__(self, level, entId):
        # These are default properties.  They are not used in the
        # Entity system, which is used by the normal DistributedGoon
        # class; but the DistributedObject system as used by the
        # DistributedCashbotBossGoon does use them.

        # It is important to initialize these before calling up to the
        # DistributedCrushableEntityAI constructor, which may modify
        # them according to the spec.
        self.hFov = 70
        self.attackRadius = 15
        self.strength = 15
        self.velocity = 4
        self.scale = 1.0

        DistributedCrushableEntityAI.DistributedCrushableEntityAI.__init__(self,
                                                         level, entId)
        self.curInd = 0
        self.dir = GOON_FORWARD
        self.parameterized = 0
        self.width = 1
        self.crushed = 0
        
        self.pathStartTime = None
        self.walkTrackTime = 0.0
        self.totalPathTime = 1.0
        
    def delete(self):
        taskMgr.remove(self.taskName("sync"))
        taskMgr.remove(self.taskName("resumeWalk"))
        taskMgr.remove(self.taskName("recovery"))
        taskMgr.remove(self.taskName("deleteGoon"))
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.delete(self)

    def generate(self):
        self.notify.debug('generate')
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.generate(self)
        if self.level:
            self.level.setEntityCreateCallback(self.parentEntId, self.startGoon)

    def startGoon(self):
        # start path at a randomized point
        ts = 100 * random.random()
        self.sendMovie(GOON_MOVIE_WALK, pauseTime=ts)
        
    def requestBattle(self, pauseTime):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("requestBattle, avId = %s" % avId)

        # For now we don't check the state of the goon and just
        # assume that he can always attack, no matter what state he's in
        
        # Tell the other clients
        self.sendMovie(GOON_MOVIE_BATTLE, avId, pauseTime)

        # Wait a little while and put the goon back in walk mode
        taskMgr.remove(self.taskName("resumeWalk"))
        taskMgr.doMethodLater(5,
                              self.sendMovie,
                              self.taskName("resumeWalk"),
                              extraArgs = (GOON_MOVIE_WALK, avId, pauseTime))

    def requestStunned(self, pauseTime):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug("requestStunned(%s)" % avId)
        
        # For now we don't check the state of the goon and just
        # assume that he can always be stunned, no matter what state he's in

        # Tell the other clients
        self.sendMovie(GOON_MOVIE_STUNNED, avId, pauseTime)

        # Wait a little while and put the goon back in recovery mode
        taskMgr.remove(self.taskName("recovery"))
        taskMgr.doMethodLater(self.STUN_TIME,
                              self.sendMovie,
                              self.taskName("recovery"),
                              extraArgs = (GOON_MOVIE_RECOVERY, avId, pauseTime))

    def requestResync(self, task=None):
        """
        resync(self)

        Broadcasts a walk message to all clients who care.
        This is mainly useful while developing, in case you
        have paused the AI or your client and you are now out of sync.
        We should resync every 5 minutes, so the timestamp doesn't go
        stale.

        The magic word "~resyncGoons" calls this function on every goon
        in the current zone
        """
        self.notify.debug("resyncGoon")
        self.sendMovie(GOON_MOVIE_SYNC)
        self.updateGrid()
        
        return
        
    def sendMovie(self, type, avId=0, pauseTime=0):
        if type == GOON_MOVIE_WALK:
            # record the local time we started walking
            self.pathStartTime = globalClock.getFrameTime()
            # and the time elapsed of the walkTrack
            if self.parameterized:
                self.walkTrackTime = pauseTime % self.totalPathTime
            else:
                self.walkTrackTime = pauseTime
                
            self.notify.debug("GOON_MOVIE_WALK doId = %s, pathStartTime = %s, walkTrackTime = %s" %
                              (self.doId, self.pathStartTime, self.walkTrackTime))

        if type == GOON_MOVIE_WALK or type == GOON_MOVIE_SYNC:
            curT = globalClock.getFrameTime()
            elapsedT = curT - self.pathStartTime
            
            # how far along the track we are in time
            pathT = (self.walkTrackTime + elapsedT)
            if self.parameterized:
                pathT = pathT % self.totalPathTime

            self.sendUpdate("setMovie", [type, avId, pathT,
                                         ClockDelta.globalClockDelta.localToNetworkTime(curT)])
            
            # respawn sync task
            taskMgr.remove(self.taskName("sync"))
            taskMgr.doMethodLater(self.UPDATE_TIMESTAMP_INTERVAL,
                                  self.requestResync,
                                  self.taskName("sync"),
                                  extraArgs=None)
        else:
            self.sendUpdate("setMovie", [type, avId, pauseTime,
                                         ClockDelta.globalClockDelta.getFrameNetworkTime()])
            
    def updateGrid(self):
        """ Figure out our position on the grid. """
        if not self.parameterized:
            return

        if self.grid and hasattr(self, "entId"): # The hasattr call is for a bug (quick) fix.
            # first remove ourselves from the grid so we aren't in there twice
            self.grid.removeObject(self.entId)
            # now add
            if not self.crushed:
                # time elapsed since we started walking
                curT = globalClock.getFrameTime()
                if self.pathStartTime:
                    elapsedT = curT - self.pathStartTime
                else:
                    elapsedT = 0
                
                # how far along the track we are in time
                pathT = (self.walkTrackTime + elapsedT) % self.totalPathTime
                # the point on the track
                pt = self.getPathPoint(pathT)
                #self.notify.debug("updateGrid, pt = %s" % pt)

                if not self.grid.addObjectByPos(self.entId, pt):
                    self.notify.warning("updateGrid: couldn't put goon in grid")
        return

    def doCrush(self, crusherId, axis):
        self.notify.debug("doCrush %s" % self.doId)
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.doCrush(self, crusherId, axis)
        # remove ourselves from grid
        # SDN: take this out for testing
        self.crushed = 1
        self.grid.removeObject(self.entId)

        # delete ourselves, delay some so the client can show it's explosion
        taskMgr.doMethodLater(5.0,
                              self.doDelete,
                              self.taskName("deleteGoon"))

    def doDelete(self, task):
        self.requestDelete()        
        return Task.done
    
    def setParameterize(self, x,y,z, pathIndex):
        # Client tells AI to parameterize its path, for later
        # position calculations on the AI
        
        #JML- seems dangerous for a client to send this kind of message
        #that's why I've added the following safety check.
        if (not hasattr(self, "level")) or (not self.level):
            return #ignore this call on a deleted Goon

        pathId = GoonPathData.taskZoneId2pathId[self.level.getTaskZoneId()]
        pathData = GoonPathData.Paths[pathId]
        self.pathOrigin = Vec3(x,y,z)
        # make sure pathIndex is valid
        if pathIndex > len(pathData):
            self.notify.warning("Invalid path index given, using 0")
            pathIndex = 0

        # get path, and add first point to end to complete the loop    
        pathPts = pathData[pathIndex] + [pathData[pathIndex][0]]
        invVel = 1.0/self.velocity
        t=0
        self.tSeg = [t]
        self.pathSeg = []
        for i in range(len(pathPts)-1):
            ptA = pathPts[i]
            ptB = pathPts[i+1]
            # add in zero-length segments for the goon turning, or pausing to look around
            # at each path point
            t += T_TURN
            self.tSeg.append(t)
            self.pathSeg.append([Vec3(0,0,0),0,ptA])

            # add segment from ptA to ptB
            seg = Vec3(ptB-ptA)
            segLength = seg.length()
            t += invVel * segLength
            self.tSeg.append(t)
            self.pathSeg.append([seg,segLength,ptA])
            
        self.totalPathTime = t
        self.pathPts = pathPts
        self.parameterized = 1
        
    def getPathPoint(self, t):
        for i in range(len(self.tSeg)-1):
            if (t >= self.tSeg[i] and t < self.tSeg[i+1]):
                tSeg = t-self.tSeg[i]
                assert self.tSeg[i+1]-self.tSeg[i] > 0
                t = tSeg/(self.tSeg[i+1]-self.tSeg[i]) # get t in range [0,1)
                seg = self.pathSeg[i][0]
                ptA = self.pathSeg[i][2]
                pt = ptA + seg * t
                return self.pathOrigin + pt
        self.notify.warning("Couldn't find valid path point")
        return Vec3(0,0,0)

    # Distributed properties.  These messages are not actually defined
    # by the toon.dc for the DistributedGoon class itself, but the
    # methods are declared up at this level anyway since this is
    # closer to where they are used.  And maybe one day the
    # DistributedGoon will, in fact, define these.  (At the moment,
    # the DistributedGoon gets all of its properties from the Entity
    # system instead, which completely goes around the
    # DistributedObject system that these methods tie into.)
                
    def b_setVelocity(self, velocity):
        self.setVelocity(velocity)
        self.d_setVelocity(velocity)
        
    def setVelocity(self, velocity):
        self.velocity = velocity
        
    def d_setVelocity(self, velocity):
        self.sendUpdate('setVelocity', [velocity])

    def getVelocity(self):
        return self.velocity
                
    def b_setHFov(self, hFov):
        self.setHFov(hFov)
        self.d_setHFov(hFov)
        
    def setHFov(self, hFov):
        self.hFov = hFov
        
    def d_setHFov(self, hFov):
        self.sendUpdate('setHFov', [hFov])

    def getHFov(self):
        return self.hFov
                
    def b_setAttackRadius(self, attackRadius):
        self.setAttackRadius(attackRadius)
        self.d_setAttackRadius(attackRadius)
        
    def setAttackRadius(self, attackRadius):
        self.attackRadius = attackRadius
        
    def d_setAttackRadius(self, attackRadius):
        self.sendUpdate('setAttackRadius', [attackRadius])

    def getAttackRadius(self):
        return self.attackRadius
                
    def b_setStrength(self, strength):
        self.setStrength(strength)
        self.d_setStrength(strength)
        
    def setStrength(self, strength):
        self.strength = strength
        
    def d_setStrength(self, strength):
        self.sendUpdate('setStrength', [strength])

    def getStrength(self):
        return self.strength
                
    def b_setGoonScale(self, scale):
        self.setGoonScale(scale)
        self.d_setGoonScale(scale)
        
    def setGoonScale(self, scale):
        self.scale = scale
        
    def d_setGoonScale(self, scale):
        self.sendUpdate('setGoonScale', [scale])

    def getGoonScale(self):
        return self.scale

    def b_setupGoon(self, velocity, hFov, attackRadius, strength, scale):
        self.setupGoon(velocity, hFov, attackRadius, strength, scale)
        self.d_setupGoon(velocity, hFov, attackRadius, strength, scale)

    def setupGoon(self, velocity, hFov, attackRadius, strength, scale):
        self.setVelocity(velocity)
        self.setHFov(hFov)
        self.setAttackRadius(attackRadius)
        self.setStrength(strength)
        self.setGoonScale(scale)

    def d_setupGoon(self, velocity, hFov, attackRadius, strength, scale):
        self.sendUpdate('setupGoon', [velocity, hFov, attackRadius, strength, scale])
        
        
