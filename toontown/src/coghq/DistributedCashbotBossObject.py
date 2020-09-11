from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedSmoothNode
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.fsm import FSM
from direct.task import Task

smileyDoId = 1

class DistributedCashbotBossObject(DistributedSmoothNode.DistributedSmoothNode, FSM.FSM):

    """ This is an object that can be picked up an dropped in the
    final battle scene with the Cashbot CFO.  In particular, it's a
    safe or a goon.  """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBossObject')

    # This should be true for objects that will eventually transition
    # from SlidingFloor to Free when they stop moving.
    wantsWatchDrift = 1

    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedCashbotBossObject')

        self.boss = None
        self.avId = 0
        self.craneId = 0
        self.cleanedUp = 0
            
        # A CollisionNode to keep me out of walls and floors, and to
        # keep others from bumping into me.  We use PieBitmask instead
        # of WallBitmask, to protect against objects (like goons)
        # self-colliding.
        self.collisionNode = CollisionNode('object')
        self.collisionNode.setIntoCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.WallBitmask | ToontownGlobals.CashbotBossObjectBitmask | OTPGlobals.CameraBitmask)
        self.collisionNode.setFromCollideMask(ToontownGlobals.PieBitmask | OTPGlobals.FloorBitmask)
        self.collisionNodePath = NodePath(self.collisionNode)

        self.physicsActivated = 0

        self.toMagnetSoundInterval = Sequence()
        self.hitFloorSoundInterval = Sequence()

        # A solid sound for when we get a good hit on the boss.
        self.hitBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_safe_miss.mp3')
        self.hitBossSoundInterval = SoundInterval(self.hitBossSfx)

        # A squishy sound for when we hit the boss, but not hard enough.
        self.touchedBossSfx = loader.loadSfx('phase_5/audio/sfx/AA_drop_sandbag.mp3')
        self.touchedBossSoundInterval = SoundInterval(
            self.touchedBossSfx, duration = 0.8)

        # Cranes will fill in this with the interval to lerp the
        # object to the crane.
        self.lerpInterval = None

    def disable(self):
        self.cleanup()
        self.stopSmooth()
        DistributedSmoothNode.DistributedSmoothNode.disable(self)

    def cleanup(self):
        # is this being called twice?
        if self.cleanedUp:
            return
        else:
            self.cleanedUp = 1

        self.demand('Off')
        self.detachNode()

        self.toMagnetSoundInterval.finish()
        self.hitFloorSoundInterval.finish()
        self.hitBossSoundInterval.finish()
        self.touchedBossSoundInterval.finish()
        del self.toMagnetSoundInterval
        del self.hitFloorSoundInterval
        del self.hitBossSoundInterval
        del self.touchedBossSoundInterval

        self.boss = None

    def setupPhysics(self, name):
        an = ActorNode('%s-%s' % (name, self.doId))
        anp = NodePath(an)
        if not self.isEmpty():
            self.reparentTo(anp)

        # It is important that there be no messenger hooks added on
        # this object at the time we reassign the NodePath.
        assert(not self.getAllAccepting())
        NodePath.assign(self, anp)

        self.physicsObject = an.getPhysicsObject()
        self.setTag('object', str(self.doId))

        self.collisionNodePath.reparentTo(self)
        self.handler = PhysicsCollisionHandler()
        self.handler.addCollider(self.collisionNodePath, self)

        # Set up a collision event so we know when the object hits the
        # floor, or the boss's target.
        self.collideName = self.uniqueName('collide')
        self.handler.addInPattern(self.collideName + '-%in')
        self.handler.addAgainPattern(self.collideName + '-%in')

        self.watchDriftName = self.uniqueName('watchDrift')

    def activatePhysics(self):
        if not self.physicsActivated:
            self.boss.physicsMgr.attachPhysicalNode(self.node())
            base.cTrav.addCollider(self.collisionNodePath, self.handler)
            self.physicsActivated = 1
            self.accept(self.collideName + '-floor', self.__hitFloor)
            self.accept(self.collideName + '-goon', self.__hitGoon)
            self.acceptOnce(self.collideName + '-headTarget', self.__hitBoss)
            self.accept(self.collideName + '-dropPlane', self.__hitDropPlane)

    def deactivatePhysics(self):
        if self.physicsActivated:
            self.boss.physicsMgr.removePhysicalNode(self.node())
            base.cTrav.removeCollider(self.collisionNodePath)
            self.physicsActivated = 0
            self.ignore(self.collideName + '-floor')
            self.ignore(self.collideName + '-goon')
            self.ignore(self.collideName + '-headTarget')
            self.ignore(self.collideName + '-dropPlane')

    def hideShadows(self):
        pass

    def showShadows(self):
        pass

    def stashCollisions(self):
        self.collisionNodePath.stash()

    def unstashCollisions(self):
        self.collisionNodePath.unstash()

    def __hitFloor(self, entry):
        if self.state == 'Dropped' or self.state == 'LocalDropped':
            self.d_hitFloor()
            self.demand('SlidingFloor', localAvatar.doId)

    def __hitGoon(self, entry):
        if self.state == 'Dropped' or self.state == 'LocalDropped':
            goonId = int(entry.getIntoNodePath().getNetTag('doId'))
            goon = self.cr.doId2do.get(goonId)
            if goon:
                self.doHitGoon(goon)

    def doHitGoon(self, goon):
        # Override in a derived class to do something if the object is
        # dropped on a goon.
        pass

    def __hitBoss(self, entry):
        if (self.state == 'Dropped' or self.state == 'LocalDropped') and \
           self.craneId != self.boss.doId:
            vel = self.physicsObject.getVelocity()
            vel = self.crane.root.getRelativeVector(render, vel)
            vel.normalize()
            impact = vel[1]
        
            if impact >= self.getMinImpact():
                print "hit! %s" % (impact)
                self.hitBossSoundInterval.start()
                self.doHitBoss(impact)
            else:
                self.touchedBossSoundInterval.start()
                print "--not hard enough: %s" % (impact)

    def doHitBoss(self, impact):
        # Derived classes can override this to do something specific
        # when we successfully hit the boss.
        self.d_hitBoss(impact)


    def __hitDropPlane(self, entry):
        self.notify.info("%s fell out of the world." % (self.doId))
        self.fellOut()

    def fellOut(self):
        # Override in a derived class to do the right thing when the
        # object falls out of the world.
        raise StandardError, 'fellOut unimplented'

    def getMinImpact(self):
        # This method returns the minimum impact, in feet per second,
        # with which the object should hit the boss before we bother
        # to tell the server.
        return 0

    def __watchDrift(self, task):
        # Checks the object for non-zero velocity.  When the velocity
        # reaches zero in the XY plane, we tell the AI we're done
        # moving it around.
        
        v = self.physicsObject.getVelocity()
        if abs(v[0]) < 0.0001 and abs(v[1]) < 0.0001:
            self.d_requestFree()

            # Go ahead and transition directly to the Free state,
            # anticipating the AI.
            self.demand('Free')

        return Task.cont

    def prepareGrab(self):
        # Specialized classes will override this method to do
        # something appropriate when the object is grabbed by a
        # magnet.
        pass

    def prepareRelease(self):
        # Specialized classes will override this method to undo the
        # effects of prepareGrab(), above, and do something
        # appropriate when the object is released from a magnet.
        pass

    ##### Messages To/From The Server #####

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated objects.
        self.boss = base.cr.doId2do[bossCogId]

    def setObjectState(self, state, avId, craneId):
        if state == 'G':
            self.demand('Grabbed', avId, craneId)
        elif state == 'D':
            if self.state != 'Dropped':
                self.demand('Dropped', avId, craneId)
        elif state == 's':
            if self.state != 'SlidingFloor':
                self.demand('SlidingFloor', avId)
        elif state == 'F':
            self.demand('Free')
        else:
            self.notify.error("Invalid state from AI: %s" % (state))

    def d_requestGrab(self):
        self.sendUpdate('requestGrab')

    def rejectGrab(self):
        # The server tells us we can't have it for whatever reason.
        if self.state == 'LocalGrabbed':
            self.demand('LocalDropped', self.avId, self.craneId)

    def d_requestDrop(self):
        self.sendUpdate('requestDrop')

    def d_hitFloor(self):
        self.sendUpdate('hitFloor')

    def d_requestFree(self):
        self.sendUpdate('requestFree', [self.getX(), self.getY(), self.getZ(), self.getH()])

    def d_hitBoss(self, impact):
        self.sendUpdate('hitBoss', [impact])



    def defaultFilter(self, request, args):
        # We overload the default filter function to disallow *any*
        # state transitions after the object has been disabled or
        # deleted, or before it has been fully generated.
        if self.boss == None:
            raise FSM.RequestDenied, request

        return FSM.FSM.defaultFilter(self, request, args)

    ### FSM States ###

    def enterOff(self):
        # In state Off, the object is not parented to the scene graph.
        # In all other states, it is.
        self.detachNode()

        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None

    def exitOff(self):
        self.reparentTo(render)

    def enterLocalGrabbed(self, avId, craneId):
        # This state is like Grabbed, except that it is only triggered
        # locally.  In this state, we have requested a grab, and we
        # will act as if we have grabbed the object successfully, but
        # we have not yet heard confirmation from the AI so we might
        # later discover that we didn't grab it after all.

        # We're not allowed to drop the object directly from this
        # state.
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        assert(self.crane != None)

        self.hideShadows()
        self.prepareGrab()
        self.crane.grabObject(self)

    def exitLocalGrabbed(self):
        if self.newState != 'Grabbed':
            self.crane.dropObject(self)
            self.prepareRelease()
            del self.crane
            self.showShadows()

    def enterGrabbed(self, avId, craneId):
        # Grabbed by a crane, or by the boss for a helmet.  craneId is
        # the doId of the crane or the doId of the boss himself.

        if self.oldState == 'LocalGrabbed':
            if craneId == self.craneId:
                # This is just the confirmation from the AI that we
                # did, in fact, grab this object with the expected
                # crane; we don't need to do anything else in this
                # state.
                return
            else:
                # Whoops, we had previously grabbed it locally, but it
                # turns out someone else grabbed it instead.
                self.crane.dropObject(self)
                self.prepareRelease()
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        assert(self.crane != None)

        # The "crane" might actually be the boss cog himself!  This
        # happens when the boss takes a safe to wear as a helmet.

        self.hideShadows()
        self.prepareGrab()
        self.crane.grabObject(self)

    def exitGrabbed(self):
        self.crane.dropObject(self)
        self.prepareRelease()
        self.showShadows()
        del self.crane

    def enterLocalDropped(self, avId, craneId):
        # As in LocalGrabbed, above, this state is entered locally
        # when we drop the safe, but we have not yet received
        # acknowledgement from the AI that we've dropped it.
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        assert(self.crane != None)

        assert(self.avId == base.localAvatar.doId)
        self.activatePhysics()
        self.startPosHprBroadcast()
        self.hideShadows()

        # Set slippery physics so it will slide off the boss.
        self.handler.setStaticFrictionCoef(0)
        self.handler.setDynamicFrictionCoef(0)

    def exitLocalDropped(self):
        assert(self.avId == base.localAvatar.doId)
        if self.newState != 'SlidingFloor' and self.newState != 'Dropped':
            self.deactivatePhysics()
            self.stopPosHprBroadcast()
        del self.crane
        self.showShadows()

    def enterDropped(self, avId, craneId):
        # Dropped (or flung) from a player's crane, or from the boss's
        # head.  In this case, craneId is the crane we were dropped
        # from (or the boss doId).
        
        self.avId = avId
        self.craneId = craneId

        self.crane = self.cr.doId2do.get(craneId)
        assert(self.crane != None)

        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast()

            # Set slippery physics so it will slide off the boss.
            self.handler.setStaticFrictionCoef(0)
            self.handler.setDynamicFrictionCoef(0)
        else:
            self.startSmooth()
        self.hideShadows()

    def exitDropped(self):
        if self.avId == base.localAvatar.doId:
            if self.newState != 'SlidingFloor':
                self.deactivatePhysics()
                self.stopPosHprBroadcast()
        else:
            self.stopSmooth()

        del self.crane
        self.showShadows()

    def enterSlidingFloor(self, avId):
        # The object is now sliding across the floor under local
        # control.  Crank up the friction so it will slow down more
        # quickly.

        self.avId = avId

        if self.lerpInterval:
            self.lerpInterval.finish()
            self.lerpInterval = None

        if self.avId == base.localAvatar.doId:
            self.activatePhysics()
            self.startPosHprBroadcast()
            
            self.handler.setStaticFrictionCoef(0.9)
            self.handler.setDynamicFrictionCoef(0.5)

            # Start up a task to watch for it to actually stop drifting.
            # When it does, we notify the AI.
            if self.wantsWatchDrift:
                taskMgr.add(self.__watchDrift, self.watchDriftName)
        else:
            self.startSmooth()

        self.hitFloorSoundInterval.start()

    def exitSlidingFloor(self):
        if self.avId == base.localAvatar.doId:
            taskMgr.remove(self.watchDriftName)
            self.deactivatePhysics()
            self.stopPosHprBroadcast()
        else:
            self.stopSmooth()

    def enterFree(self):
        self.avId = 0
        self.craneId = 0

    def exitFree(self):
        pass
