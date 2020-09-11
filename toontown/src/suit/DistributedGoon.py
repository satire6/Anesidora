from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from GoonGlobals import *

from direct.fsm import FSM
from direct.distributed import ClockDelta
from otp.level import BasicEntities
from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import DistributedCrushableEntity
from toontown.toonbase import ToontownGlobals
from toontown.coghq import MovingPlatform
import Goon
from direct.task.Task import Task
from otp.level import PathEntity
import GoonDeath
import random


class DistributedGoon(DistributedCrushableEntity.DistributedCrushableEntity,
                      Goon.Goon, FSM.FSM):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoon')

    def __init__(self, cr):
        try:
            self.DistributedGoon_initialized
        except:
            self.DistributedGoon_initialized = 1
            DistributedCrushableEntity.DistributedCrushableEntity.__init__(self, cr)
            Goon.Goon.__init__(self)
            FSM.FSM.__init__(self, 'DistributedGoon')

        # Don't try caching goons.  It seems to be a little bit broken
        # anyway.
        self.setCacheable(0)

        # collision stuff
        self.rayNode = None
        self.checkForWalls = 0
        self.triggerEvent = None

        # animation and walking
        self.animTrack = None
        self.walkTrack = None
        self.pauseTime = 0
        self.paused = 0
        self.path = None
        self.dir = GOON_FORWARD
        self.animMultiplier = 1.0
        self.isDead = 0
        self.isStunned = 0
        self.collapseSound = loader.loadSfx("phase_9/audio/sfx/CHQ_GOON_hunker_down.mp3")
        self.recoverSound = loader.loadSfx("phase_9/audio/sfx/CHQ_GOON_rattle_shake.mp3")
        self.attackSound = loader.loadSfx("phase_9/audio/sfx/CHQ_GOON_tractor_beam_alarmed.mp3")

    def announceGenerate(self):
        DistributedCrushableEntity.DistributedCrushableEntity.announceGenerate(self)

        # if the goonType is set by the Spec use it, otherwise make a default goon
        if hasattr(self, 'goonType'):
            self.initGoon(self.goonType)
        else:
            self.initGoon('pg')            

        # scale the radar depending on fov and attackRadius.
        self.scaleRadar()

        # Set the hat color according to his strength.
        self.colorHat()

        if self.level:
            # enable clip planes
            self.initClipPlanes()

            # set the path the goon walks on
            self.level.setEntityCreateCallback(self.parentEntId,
                                               self.initPath)
        else:
            self.enterOff()
            taskMgr.doMethodLater(0.1,
                                  self.makeCollidable,
                                  self.taskName("makeCollidable"))

        # usually we want the goons to be a little bigger
        self.setGoonScale(self.scale)
        # Figure out walk rate to anim speed multiplier
        self.animMultiplier = self.velocity / (ANIM_WALK_RATE * self.scale)
        self.setPlayRate(self.animMultiplier, 'walk')
        
    def initPath(self):
        """
        Initialize this goon's position and then setup its collision.
        This avoids issues with delays in positioning causing undesired 
        collisions. We found this sequence of events in a bug:
            1.) Goon created at origin, waits for path to load in level.
            2.) Goon's collision activated.
            3.) Path loads, callback positions goon.
            4.) This move shoves the toon. (Not entirely sure why...)
        Clearly there is something wrong in step 4, but this at least sets
        position before collision.
        """
        
        self.enterOff()
        self.setPath()

        taskMgr.doMethodLater(0.1,
                              self.makeCollidable,
                              self.taskName("makeCollidable"))
        
        
    def makeCollidable(self, task):
        """
        Initialize the collision and trigger for this goon. After this
        the goon is collidable, detecting the toon, and responsive to stun.
        """

        self.initCollisions()
    
        # set up stun collisions and body sphere for goon
        self.initializeBodyCollisions()
        triggerName = self.uniqueName('GoonTrigger')
        self.trigger.setName(triggerName)
        self.triggerEvent = 'enter%s' % (triggerName)

        # Start listening for the local toon.
        self.startToonDetect()

    def generate(self):
        DistributedCrushableEntity.DistributedCrushableEntity.generate(self)

    def scaleRadar(self):
        Goon.Goon.scaleRadar(self)
        
        self.trigger = self.radar.find('**/trigger')

        # Make sure the trigger name is set.
        triggerName = self.uniqueName('GoonTrigger')
        self.trigger.setName(triggerName)

    def initCollisions(self):
        # Setup a collision sphere that we can't walk through
        self.cSphere = CollisionSphere(0.0, 0.0, 1.0, 1.0)
        #self.cSphereNode = CollisionNode(self.uniqueName("goonCollSphere"))
        self.cSphereNode = CollisionNode("goonCollSphere")  # change name on generate
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath=self.head.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereBitMask = ToontownGlobals.WallBitmask
        self.cSphereNode.setCollideMask(self.cSphereBitMask)
        self.cSphere.setTangible(1)

        # Setup a sphere to detect "stun" collision with the toon
        self.sSphere = CollisionSphere(0.0, 0.0, self.headHeight+.8, .2)
        #self.sSphereNode = CollisionNode(self.uniqueName("toonSphere"))
        self.sSphereNode = CollisionNode("toonSphere")
        self.sSphereNode.addSolid(self.sSphere)
        self.sSphereNodePath=self.head.attachNewNode(self.sSphereNode)
        self.sSphereNodePath.hide()
        self.sSphereBitMask = ToontownGlobals.WallBitmask
        self.sSphereNode.setCollideMask(self.sSphereBitMask)
        self.sSphere.setTangible(1)

    def initializeBodyCollisions(self):
        self.cSphereNode.setName(self.uniqueName("goonCollSphere"))
        self.sSphereNode.setName(self.uniqueName("toonSphere"))
       
        # If a toon runs directly into the goon without being detected,
        # the goon becomes stunned
        self.accept(self.uniqueName("entertoonSphere"), self.__handleStun)

    def disableBodyCollisions(self):
        self.ignore(self.uniqueName("entertoonSphere"))

    def deleteCollisions(self):
        if hasattr(self, 'sSphereNodePath'):
            self.sSphereNodePath.removeNode()
            del self.sSphereNodePath
            del self.sSphereNode
            del self.sSphere
        
        if hasattr(self, 'cSphereNodePath'):
            self.cSphereNodePath.removeNode()
            del self.cSphereNodePath
            del self.cSphereNode
            del self.cSphere

    def initClipPlanes(self):
        # look for all clip planes in thiz zone
        zoneNum = self.getZoneEntity().getZoneNum()
        clipList = self.level.goonClipPlanes.get(zoneNum)
        if clipList:
            for id in clipList:
                clipPlane = self.level.getEntity(id)
                self.radar.setClipPlane(clipPlane.getPlane())


    def disableClipPlanes(self):
        if self.radar:
            self.radar.clearClipPlane()

    if __dev__:
        def refreshPath(self):
            self.setPath()
            self.request('Off')
            self.request('Walk')

    def setPath(self):
        self.path = self.level.getEntity(self.parentEntId)
        if __dev__:
            if hasattr(self, 'pathChangeEvent'):
                self.ignore(self.pathChangeEvent)
            self.pathChangeEvent = self.path.getChangeEvent()
            self.accept(self.pathChangeEvent, self.refreshPath)
        if self.walkTrack:
            self.walkTrack.pause()
            self.walkTrack = None
        self.walkTrack = self.path.makePathTrack(self, self.velocity,
                                                 self.uniqueName("goonWalk"),
                                                 turnTime = T_TURN)

        # if we are on a grid, tell the AI to parameterize the path
        if self.gridId != None:
            self.sendUpdate("setParameterize", [self.path.pos[0],
                                                self.path.pos[1],
                                                self.path.pos[2],
                                                self.path.pathIndex])
        
    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        self.notify.debug("DistributedGoon %d: disabling" % self.getDoId())
        self.ignoreAll()
        self.stopToonDetect()
        taskMgr.remove(self.taskName("resumeWalk"))
        taskMgr.remove(self.taskName("recoveryDone"))
        self.request('Off')
        self.disableBodyCollisions()
        self.disableClipPlanes()
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None
        if self.walkTrack:
            self.walkTrack.pause()
            self.walkTrack = None
                
        DistributedCrushableEntity.DistributedCrushableEntity.disable(self)
        
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
            self.notify.debug("DistributedGoon %d: deleting" % self.getDoId())
            
            # stop waiting to set collisions
            taskMgr.remove(self.taskName("makeCollidable"))

            # tear down collisions
            self.deleteCollisions()

            self.head.removeNode()
            del self.head
            del self.attackSound
            del self.collapseSound
            del self.recoverSound
            DistributedCrushableEntity.DistributedCrushableEntity.delete(self)
            Goon.Goon.delete(self)

    ##### Off state #####

    def enterOff(self, *args):
        assert self.notify.debug('enterOff()')
        self.hideNametag3d()
        self.hideNametag2d()
        self.hide()
        self.isStunned = 0
        self.isDead = 0

        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None
        if self.walkTrack:
            self.walkTrack.pause()
            self.walkTrack = None

    def exitOff(self):
        self.show()
        self.showNametag3d()
        self.showNametag2d()

    ##### Walk state #####
    # The goon is walking around trying to detect toons
    def enterWalk(self, avId=None, ts=0):
        self.notify.debug('enterWalk, ts = %s' % ts)
        # start the toon detection on enterWalk.
        self.startToonDetect()
        self.loop('walk', 0)

        self.isStunned = 0

        if self.path:
            if not self.walkTrack:
                # this should only happen in debug when using ~resyncGoons
                self.walkTrack = self.path.makePathTrack(self, self.velocity,
                                                         self.uniqueName("goonWalk"),
                                                         turnTime = T_TURN)
            self.startWalk(ts)
            
    def startWalk(self, ts):
        tOffset = ts % self.walkTrack.getDuration()
        self.walkTrack.loop()
        self.walkTrack.pause()
        self.walkTrack.setT(tOffset)
        self.walkTrack.resume()
        self.paused = 0

    def exitWalk(self):
        self.notify.debug('exitWalk')
        self.stopToonDetect()
        if self.walkTrack and not self.paused:
            self.pauseTime = self.walkTrack.pause()
            self.paused = 1
        self.stop()
    

    # The goon has just detected a toon
    def enterBattle(self, avId=None, ts=0):
        
        self.notify.debug('enterBattle')
        self.stopToonDetect()
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        self.isStunned = 0

        # before we play the attack track, start the resume walk timer.
        # This might kick us to enterWalk before even playing the attack
        # track, in high latency cases
        # on second thought, let the AI tell us when to resume walking
        # self.__startResumeWalkTask(ts)

        # stun toon in battle with goon
        #if avId != None:
        #    self.stunToon(avId)
        if avId == base.localAvatar.doId:
            if self.level:
                
                #self.level.b_setOuch(self.strength, "Fall")
                self.level.b_setOuch(self.strength)
        # Get the track for the attack.  Since it is just blinking
        # the eye color, it isn't necessary to sinc with the timestamp
        self.animTrack = self.makeAttackTrack()
        self.animTrack.loop()
        
    
    def exitBattle(self):
        self.notify.debug('exitBattle')
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None
        self.head.setHpr(0,0,0)


    # The toon has temporarily stunned the goon
    def enterStunned(self, ts=0):
        # disable stun sphere
        self.ignore(self.uniqueName("entertoonSphere"))

        self.isStunned = 1
        
        self.notify.debug("enterStunned")
        if self.radar:
            self.radar.hide()

        # before we play the stunned anim, start the recover timer
        # This might kick us to enterWalk before even playing the stun
        # track, in high latency cases
        # on second thought, let the AI tell us when to resume walking
        #self.__startRecoverTask(ts)

        self.animTrack = Parallel(Sequence(ActorInterval(self, 'collapse'),
                                           Func(self.pose, 'collapse', 48)),
                                  SoundInterval(self.collapseSound, node=self),
                                  )

        self.animTrack.start(ts)
    
    def exitStunned(self):
        self.notify.debug("exitStunned")
        if self.radar:
            self.radar.show()
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        # reenable stun sphere
        self.accept(self.uniqueName("entertoonSphere"), self.__handleStun)


    # Goon recovery from being stunned
    def enterRecovery(self, ts=0, pauseTime=0):
        # set a timer to restart the walk track
        self.notify.debug("enterRecovery")

        self.ignore(self.uniqueName("entertoonSphere"))

        self.isStunned = 1

        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        self.animTrack = self.getRecoveryTrack()
                                  
        duration = self.animTrack.getDuration()
        self.animTrack.start(ts)

        # start walk track after recovery plays
        delay = max(0, duration-ts)
        taskMgr.remove(self.taskName("recoveryDone"))
        taskMgr.doMethodLater(delay,
                              self.recoveryDone,
                              self.taskName("recoveryDone"),
                              extraArgs = (pauseTime,))
        
    def getRecoveryTrack(self):
        return Parallel(Sequence(ActorInterval(self, 'recovery'),
                                 Func(self.pose, 'recovery', 96),
                                 ),
                        Func(base.playSfx,self.recoverSound, node=self),
                        )
    
    def recoveryDone(self, pauseTime):
        self.request('Walk', None, pauseTime)
        
    def exitRecovery(self):
        self.notify.debug("exitRecovery")
        taskMgr.remove(self.taskName("recoveryDone"))
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None

        # reenable stun sphere
        self.accept(self.uniqueName("entertoonSphere"), self.__handleStun)

    def makeAttackTrack(self):
        h = self.head.getH()
        freakDeg = 60
        hatZ = self.hat.getZ()
        track = Parallel(Sequence(LerpColorScaleInterval(self.eye, .2,
                                                         Vec4(1,0,0,1)),
                                  LerpColorScaleInterval(self.eye, .2,
                                                         Vec4(0,0,1,1)),
                                  LerpColorScaleInterval(self.eye, .2,
                                                         Vec4(1,0,0,1)),
                                  LerpColorScaleInterval(self.eye, .2,
                                                         Vec4(0,0,1,1)),
                                  Func(self.eye.clearColorScale),
                                  ),
                         SoundInterval(self.attackSound, node=self, volume=.4))
        return track
    
    
    # doDetect looks around for toons
    # Subclasses can override this to use a different detection
    # method
    def doDetect(self):
        pass
        
        
    # doAttack penalizes the toon for being caught by this goon
    # Subclasses can override this to do a different type
    # of attack
    def doAttack(self, avId):
        return

    def __startResumeWalkTask(self, ts):
        resumeTime = 1.5

        if ts < resumeTime:
            # set a timer to put us back in walk mode
            taskMgr.remove(self.taskName("resumeWalk"))
            taskMgr.doMethodLater(resumeTime-ts,
                                  self.request,
                                  self.taskName("resumeWalk"),
                                  extraArgs = ('Walk',))
        else:
            self.request('Walk', ts-resumeTime)
        
    def __reverseWalk(self, task):
        self.request('Walk')
            
        return Task.done

    def __startRecoverTask(self, ts):
        # Stun time should be long enough for collapse animation to play
        # plus any additional time the goon should be out of service
        stunTime = 4.0

        if ts < stunTime:
            # set a timer to put us back in walk mode
            taskMgr.remove(self.taskName("resumeWalk"))
            taskMgr.doMethodLater(stunTime-ts,
                                  self.request,
                                  self.taskName("resumeWalk"),
                                  extraArgs = ('Recovery',))
        else:
            self.request('Recovery', ts-stunTime)
        

    def startToonDetect(self):
        self.radar.show()  # just in case.
        if self.triggerEvent:
            self.accept(self.triggerEvent, self.handleToonDetect)

    def stopToonDetect(self):
        if self.triggerEvent:
            self.ignore(self.triggerEvent)

##     def __detectLocalToon(self, task):
##         toon = base.localAvatar
##         # check distance from local toon
##         toonPos = toon.getPos()
##         goonPos = self.head.getPos(render)
##         # hack:  the ray is facing backwards if we don't flip the direction manually?!
##         v = goonPos - toonPos
##         distToToon = Vec3(v).length()

##         if (not toon.isStunned) and distToToon < self.attackRadius:
##             # the toon is close enough, and not already stunned
##             # now check if toon is in field of view

##             # get v relative to radar.  Radar is facing Vec3(0,1,0) in its
##             # own coordinate system
##             vRelToRadar = self.radar.getRelativeVector(render, v)
            
##             rayDir = Vec3(vRelToRadar)
##             vRelToRadar.normalize()

##             vDotR = vRelToRadar[1] # == vRelToRadar.dot(Vec3(0,1,0)

##             # err on the side of the player
##             fudge = .05
            
##             if vDotR < 1.0 and vDotR > self.cosHalfFov + fudge:
##                 if self.checkForWalls:
##                     # THIS CODE ISN'T WORKING RIGHT, NOR DO WE NEED
##                     # IT FOR THE CURRENT FACTORY LAYOUT.
                    
##                     # the toon is in the fov,
##                     # now make sure he is not occluded
##                     #rayOrigin = Point3(0,1.5,base.localAvatar.getHeight()/2.0)
##                     rayOrigin = Point3(0,0,self.headHeight)
##                     ray = CollisionRay(rayOrigin, rayDir)
##                     rayNode = CollisionNode(self.uniqueName('goonRay'))
##                     #rayNode.setCollideMask(BitMask32.allOff())
##                     rayBitMask = ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask
##                     rayNode.setFromCollideMask(rayBitMask)
##                     rayNode.setIntoCollideMask(BitMask32.allOff())
##                     #rayNode.setCollideGeom(1)
##                     rayNode.addSolid(ray)
##                     rayNodePath = self.head.attachNewNode(rayNode)
##                     #rayNodePath.show()

##                     cqueue = CollisionHandlerQueue()
##                     world = self.level.geom
##                     trav = CollisionTraverser("DistributedGoon")
##                     trav.addCollider(rayNodePath, cqueue)
##                     trav.traverse(world)

##                     cqueue.sortEntries()

##                     if cqueue.getNumEntries() == 0:
##                         # No objects were between the toon and goon
##                         self.notify.warning("%s: Couldn't find ANYTHING!" % (self.doId))
##                         self.handleToonDetect()
##                     else:
##                         entry = cqueue.getEntry(0)
                        
##                         # if the closest interseciton point is behind our toon
##                         # then we can start the attack, otherwise consider the toon
##                         # hidden from the goon
##                         dist = Vec3(self.getPos(render) - entry.getIntoIntersectionPoint()).length()
##                         if dist > distToToon:
##                             colName = entry.getIntoNode().getName()
##                             self.notify.debug("collider (%s) at d=%s, toon at %s" % (colName, dist,distToToon))
##                             self.handleToonDetect(entry)
##                         else:
##                             colName = entry.getIntoNode().getName()
##                             self.notify.debug("toon is occluded by %s, %s > %s" % (colName, distToToon, dist))

##                     rayNodePath.removeNode()
##                 else:
##                     # not checking for walls
##                     # Battle the toon
##                     self.handleToonDetect()
                    
##         return Task.cont

    def handleToonDetect(self, collEntry=None):
        if base.localAvatar.isStunned:
            # It doesn't count if the toon is already stunned.
            return

        if self.state == 'Off':
            return

        # Stop looking for localToon
        self.stopToonDetect()

        # Start the attack now for the local toon to see
        self.request("Battle", base.localAvatar.doId)

        # pause the walk track before sending battle request to
        # the AI so we know what time the walk track was paused
        if self.walkTrack:
            self.pauseTime = self.walkTrack.pause()
            self.paused = 1

        if self.dclass and hasattr(self, 'dclass'):
            self.sendUpdate("requestBattle", [self.pauseTime])
        else:
            self.notify.info( "Goon deleted and still trying to call handleToonDetect()" )
            # Need to get more information on why this case happens.
            
    def __handleStun(self, collEntry):
        # Client side check first to see if we're in a reasonable distance to the goon to stun it.
        toon = base.localAvatar
        if toon:
            toonDistance = self.getPos(toon).length()
            if toonDistance > self.attackRadius:
                self.notify.warning("Stunned a good, but outside of attack radius")
                return
            else:
                self.request("Stunned")

        # pause the walk track before sending battle request to
        # the AI so we know what time the walk track was paused
        if self.walkTrack:
            self.pauseTime = self.walkTrack.pause()
            self.paused = 1

        # Tell the AI we are stunned
        self.sendUpdate("requestStunned", [self.pauseTime])
        
    def setMovie(self, mode, avId, pauseTime, timestamp):
        """
        This is a message from the AI describing a movie for this goon
        """
        # do nothing if dead
        if self.isDead:
            return
        
        ts = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.notify.debug("%s: setMovie(%s,%s,%s,%s)" % (self.doId, mode,avId,pauseTime,ts))
        
        if mode == GOON_MOVIE_BATTLE:
            if self.state != "Battle":
                self.request("Battle", avId, ts)
        elif mode == GOON_MOVIE_STUNNED:
            if self.state != "Stunned":
                # Client side check first to see if we're in a reasonable distance to the goon to stun it.
                toon = base.cr.doId2do.get(avId)
                if toon:
                    toonDistance = self.getPos(toon).length()
                    if toonDistance > self.attackRadius:
                        self.notify.warning("Stunned a goon, but outside of attack radius")
                        return
                    else:
                        self.request("Stunned", ts)
        elif mode == GOON_MOVIE_RECOVERY:
            if self.state != "Recovery":
                self.request("Recovery", ts, pauseTime)
        elif mode == GOON_MOVIE_SYNC:
            if self.walkTrack:
                self.walkTrack.pause()
                self.paused = 1
            if self.state == "Off" or self.state == "Walk":
                self.request("Walk", avId, pauseTime+ts)
        else:
            # walk
            if self.walkTrack:
                self.walkTrack.pause()
                self.walkTrack = None
            self.request("Walk", avId, pauseTime+ts)
        
    def stunToon(self, avId):
        self.notify.debug("stunToon(%s)" % avId)
        # Stun localtoon
        av = base.cr.doId2do.get(avId)
        if av != None:
            av.stunToon()
        
    def isLocalToon(self, avId):
        if avId == base.localAvatar.doId:
            return 1
        return 0
        
    def playCrushMovie(self, crusherId, axis):
        goonPos = self.getPos()
        # randomize the x and z scale a little
        sx = random.uniform(0.3, 0.8) * self.scale
        sz = random.uniform(0.3, 0.8) * self.scale
        crushTrack = Sequence(
            GoonDeath.createGoonExplosion(self.getParent(),
                                          goonPos, VBase3(sx, 1, sz)),
            name = self.uniqueName('crushTrack'),
            autoFinish = 1)
        self.dead()
        crushTrack.start()

    def setVelocity(self, velocity):
        self.velocity = velocity
        # tune play rate
        self.animMultiplier = velocity / (ANIM_WALK_RATE * self.scale)
        self.setPlayRate(self.animMultiplier, 'walk')

    """
    def reverseDirection(self, colEntry=None):
        # Stop walking immediately and reverse direction.
        # This is done simply by switching our self.dir and
        # calling goToNextPoint again
        if self.dir == GOON_FORWARD:
            self.dir = GOON_REVERSE
        else:
            self.dir = GOON_FORWARD

        self.nextInd = (self.curInd + self.dir) % (len(self.path)-1)
        self.goToNextPoint(self.curInd, self.nextInd, self.velocity)
    """

    def dead(self):
        if not self.isDead and not self.isDisabled():
            # goon is dead, stop detecting, it's not fair
            self.stopToonDetect()
            # hide for now
            self.detachNode()
            self.isDead = 1

    def undead(self):
        # start toon detection task again
        if self.isDead:
            self.startToonDetect()
            self.reparentTo(render)
            self.isDead = 0

    def resync(self):
        if not self.isDead:
            # get the AI and client on the same page again
            # (used only in dev environment for now)
            self.sendUpdate("requestResync")
            
    def setHFov(self, hFov):
        if hFov != self.hFov:
            self.hFov = hFov
            if self.isGenerated():
                self.scaleRadar()
            
    def setAttackRadius(self, attackRadius):
        if attackRadius != self.attackRadius:
            self.attackRadius = attackRadius
            if self.isGenerated():
                self.scaleRadar()
        
    def setStrength(self, strength):
        if strength != self.strength:
            self.strength = strength
            if self.isGenerated():
                self.colorHat()

    def setGoonScale(self, scale):
        # This is not named setScale(), so it can be distinct from
        # NodePath.setSale().
        if scale != self.scale:
            self.scale = scale
            if self.isGenerated():
                self.getGeomNode().setScale(self.scale)
                self.scaleRadar()

    def setupGoon(self, velocity, hFov, attackRadius, strength, scale):
        self.setVelocity(velocity)
        self.setHFov(hFov)
        self.setAttackRadius(attackRadius)
        self.setStrength(strength)
        self.setGoonScale(scale)
