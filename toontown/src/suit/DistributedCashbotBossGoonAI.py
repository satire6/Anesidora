from pandac.PandaModules import *
from direct.task.TaskManagerGlobal import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
import GoonGlobals
from direct.task.Task import Task
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from toontown.coghq import DistributedCashbotBossObjectAI
from direct.showbase import PythonUtil
import DistributedGoonAI
import math
import random

class DistributedCashbotBossGoonAI(DistributedGoonAI.DistributedGoonAI,
                                   DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI):

    """ This is a goon that walks around in the Cashbot CFO final
    battle scene, tormenting Toons, and also providing ammo for
    defeating the boss. """

    legLength = 10

    # A table of likely directions for the next choice at each point.
    # The table contains (heading, weight), where heading is the
    # direction of choice, and weight is the relative preference of
    # this direction over the others.
    directionTable = [
        (0, 15),
        (10, 10),
        (-10, 10),
        (20, 8),
        (-20, 8),
        (40, 5),
        (-40, 5),
        (60, 4),
        (-60, 4),
        (80, 3),
        (-80, 3),
        (120, 2),
        (-120, 2),
        (180, 1),
        ]

    offMask = BitMask32(0)
    onMask = CollisionNode.getDefaultCollideMask()

    def __init__(self, air, boss):
        DistributedGoonAI.DistributedGoonAI.__init__(self, air, 0)
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.__init__(self, air, boss)

        # A tube covering our intended path, so other goons will see
        # and avoid us.
        cn = CollisionNode('tubeNode')
        self.tube = CollisionTube(0, 0, 0, 0, 0, 0, 2)
        cn.addSolid(self.tube)
        self.tubeNode = cn
        self.tubeNodePath = self.attachNewNode(self.tubeNode)

        # A spray of feeler wires so we can choose an empty path.
        self.feelers = []
        cn = CollisionNode('feelerNode')
        self.feelerLength = self.legLength * 1.5
        feelerStart = 1
        for heading, weight in self.directionTable:
            rad = deg2Rad(heading)
            x = -math.sin(rad)
            y = math.cos(rad)
            seg = CollisionSegment(x * feelerStart, y * feelerStart , 0,
                                   x * self.feelerLength, y * self.feelerLength, 0)
            cn.addSolid(seg)
            self.feelers.append(seg)
        cn.setIntoCollideMask(self.offMask)
        self.feelerNodePath = self.attachNewNode(cn)

        self.isWalking = 0

        self.cTrav = CollisionTraverser('goon')
        self.cQueue = CollisionHandlerQueue()

        self.cTrav.addCollider(self.feelerNodePath, self.cQueue)
        
    def requestBattle(self, pauseTime):
        avId = self.air.getAvatarIdFromSender()

        # Here we ask the boss to damage the toon, instead of asking
        # the level to do it.
        
        avatar = self.air.doId2do.get(avId)
        if avatar:
            self.boss.damageToon(avatar, self.strength)

        DistributedGoonAI.DistributedGoonAI.requestBattle(self, pauseTime)

    def sendMovie(self, type, avId=0, pauseTime=0):
        # Overridden from DistributedGoonAI.
        if type == GoonGlobals.GOON_MOVIE_WALK:
            self.demand('Walk')
        elif type == GoonGlobals.GOON_MOVIE_BATTLE:
            self.demand('Battle')
        elif type == GoonGlobals.GOON_MOVIE_STUNNED:
            self.demand('Stunned')
        elif type == GoonGlobals.GOON_MOVIE_RECOVERY:
            self.demand('Recovery')
        else:
            self.notify.warning("Ignoring movie type %s" % (type))

    def __chooseTarget(self, extraDelay = 0):
        # Chooses a random point to walk towards.
        direction = self.__chooseDirection()
        if direction == None:
            # No place to go; just blow up.
            self.target = None
            self.arrivalTime = None
            self.b_destroyGoon()
            return
        
        heading, dist = direction
        dist = min(dist, self.legLength)
        targetH = PythonUtil.reduceAngle(self.getH() + heading)

        # How long will it take to rotate to position?
        origH = self.getH()    
        h = PythonUtil.fitDestAngle2Src(origH, targetH)
        delta = abs(h - origH)
        turnTime = delta / (self.velocity * 5)

        # And how long will it take to walk to position?
        walkTime = dist / self.velocity

        self.setH(targetH)
        self.target = self.boss.scene.getRelativePoint(self, Point3(0, dist, 0))

        self.departureTime = globalClock.getFrameTime()
        self.arrivalTime = self.departureTime + turnTime + walkTime + extraDelay

        self.d_setTarget(self.target[0], self.target[1], h,
                         globalClockDelta.localToNetworkTime(self.arrivalTime))

    def __chooseDirection(self):

        # Chooses a direction to walk in next.  We do this by
        # examining a few likely directions, and we choose the one
        # with the clearest path (e.g. the fewest safes and other
        # goons in the way), with some randomness thrown in for fun.

        # Hack to prevent self-intersection.
        self.tubeNode.setIntoCollideMask(self.offMask)
        self.cTrav.traverse(self.boss.scene)
        self.tubeNode.setIntoCollideMask(self.onMask)

        entries = {}

        # Walk through the entries from farthest to nearest, so that
        # nearer collisions on the same segment will override farther
        # ones.
        self.cQueue.sortEntries()

        for i in range(self.cQueue.getNumEntries() - 1, -1, -1):
            entry = self.cQueue.getEntry(i)
            dist = Vec3(entry.getSurfacePoint(self)).length()

            if dist < 1.2:
                # Too close; forget it.
                dist = 0
            
            entries[entry.getFrom()] = dist

        # Now get the lengths of the various paths, and accumulate a
        # score table.  Each direction gets a score based on the
        # distance to the next obstruction, and its weighted
        # preference.
        netScore = 0
        scoreTable = []
        for i in range(len(self.directionTable)):
            heading, weight = self.directionTable[i]
            seg = self.feelers[i]
            dist = entries.get(seg, self.feelerLength)

            score = dist * weight
            netScore += score
            scoreTable.append(score)

        if netScore == 0:
            # If no paths were any good, bail.
            self.notify.info("Could not find a path for %s" % (self.doId))
            return None

        # And finally, choose a random direction from the table,
        # with a random distribution weighted by score.
        s = random.uniform(0, netScore)
        for i in range(len(self.directionTable)):
            s -= scoreTable[i]
            if s <= 0:
                heading, weight = self.directionTable[i]
                seg = self.feelers[i]
                dist = entries.get(seg, self.feelerLength)
                return (heading, dist)

        # Shouldn't be possible to fall off the end, but maybe there
        # was a roundoff error.
        self.notify.warning("Fell off end of weighted table.")
        return (0, self.legLength)

    def __startWalk(self):
        # Generate a do-later method to "walk" the goon to his target
        # square by the specified time.  Actually, on the AI the goon
        # just stands where he is until the time expires, but no one
        # cares about that.
        assert not self.isWalking
        
        if self.arrivalTime == None:
            return

        now = globalClock.getFrameTime()
        availableTime = self.arrivalTime - now

        if availableTime > 0:
            # Change the tube to encapsulate our path to our target point.
            point = self.getRelativePoint(self.boss.scene, self.target)
            self.tube.setPointB(point)
            self.node().resetPrevTransform()
            
            taskMgr.doMethodLater(availableTime, self.__reachedTarget,
                                  self.uniqueName('reachedTarget'))
            self.isWalking = 1
        else:
            self.__reachedTarget(None)

    def __stopWalk(self, pauseTime = None):
        if self.isWalking:
            # Stop the walk do-later.
            taskMgr.remove(self.uniqueName('reachedTarget'))

            # Place us at the appropriate point along the path.
            if pauseTime == None:
                now = globalClock.getFrameTime()
                t = (now - self.departureTime) / (self.arrivalTime - self.departureTime)
            else:
                t = pauseTime / (self.arrivalTime - self.departureTime)
                
            t = min(t, 1.0)
            pos = self.getPos()
            self.setPos(pos + (self.target - pos) * t)

            # The tube is now a sphere.
            self.tube.setPointB(0, 0, 0)
            
            self.isWalking = 0

    def __reachedTarget(self, task):
        self.__stopWalk()
        self.__chooseTarget()
        self.__startWalk()

    def __recoverWalk(self, task):
        self.demand('Walk')
        return Task.done

    def doFree(self, task):
        # This method is fired as a do-later when we enter WaitFree.
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.doFree(self, task)
        self.demand('Walk')
        return Task.done

    ### Messages ###

    def requestStunned(self, pauseTime):
        avId = self.air.getAvatarIdFromSender()

        if avId not in self.boss.involvedToons:
            return

        if self.state == 'Stunned' or self.state == 'Grabbed':
            # Already stunned, or just picked up by a magnet; don't
            # stun again.
            return

        # Stop the goon right where he is.
        self.__stopWalk(pauseTime)

        # And it poops out a treasure right there.
        self.boss.makeTreasure(self)
        
        DistributedGoonAI.DistributedGoonAI.requestStunned(self, pauseTime)


    def hitBoss(self, impact):
        avId = self.air.getAvatarIdFromSender()

        self.validate(avId, impact <= 1.0,
                      'invalid hitBoss impact %s' % (impact))

        if avId not in self.boss.involvedToons:
            return
        
        if self.state == 'Dropped' or self.state == 'Grabbed':
            if not self.boss.heldObject:
                # A goon can only hurt the boss when he's got a helmet on.
                damage = int(impact * 25 * self.scale)
                self.boss.recordHit(max(damage, 2))
            
        self.b_destroyGoon()

    def d_setTarget(self, x, y, h, arrivalTime):
        self.sendUpdate('setTarget', [x, y, h, arrivalTime])

    def d_destroyGoon(self):
        self.sendUpdate('destroyGoon')

    def b_destroyGoon(self):
        self.d_destroyGoon()
        self.destroyGoon()

    def destroyGoon(self):
        # The client or AI informs the world that the goon has
        # shuffled off this mortal coil.

        self.demand('Off')

        # We don't actually delete the goon; instead, we leave it in
        # the boss's pool to recycle later.
    
    ### FSM States ###

    def enterOff(self):
        self.tubeNodePath.stash()
        self.feelerNodePath.stash()

    def exitOff(self):
        self.tubeNodePath.unstash()
        self.feelerNodePath.unstash()

    def enterGrabbed(self, avId, craneId):
        DistributedCashbotBossObjectAI.DistributedCashbotBossObjectAI.enterGrabbed(self, avId, craneId)

        # If a goon is grabbed while he's just waking up, it
        # interrupts the wake-up process.  Ditto for a goon in battle
        # mode.
        taskMgr.remove(self.taskName('recovery'))
        taskMgr.remove(self.taskName('resumeWalk'))
        
    def enterWalk(self):
        # The goon is prowling about, looking for trouble.
        
        self.avId = 0
        self.craneId = 0

        self.__chooseTarget()
        self.__startWalk()
        self.d_setObjectState('W', 0, 0)

    def exitWalk(self):
        self.__stopWalk()

    def enterEmergeA(self):
        # The goon is emerging from door a.

        self.avId = 0
        self.craneId = 0

        h = 0
        dist = 15
        pos = self.boss.getPos()
        walkTime = dist / self.velocity

        self.setPosHpr(pos[0], pos[1], pos[2], h, 0, 0)
        self.d_setPosHpr(pos[0], pos[1], pos[2], h, 0, 0)
        self.target = self.boss.scene.getRelativePoint(self, Point3(0, dist, 0))
        self.departureTime = globalClock.getFrameTime()
        self.arrivalTime = self.departureTime + walkTime

        self.d_setTarget(self.target[0], self.target[1], h,
                         globalClockDelta.localToNetworkTime(self.arrivalTime))

        self.__startWalk()
        self.d_setObjectState('a', 0, 0)

        taskMgr.doMethodLater(walkTime, self.__recoverWalk, self.uniqueName('recoverWalk'))

    def exitEmergeA(self):
        self.__stopWalk()
        taskMgr.remove(self.uniqueName('recoverWalk'))

    def enterEmergeB(self):
        # The goon is emerging from door b.

        self.avId = 0
        self.craneId = 0

        h = 180
        dist = 15
        pos = self.boss.getPos()
        walkTime = dist / self.velocity

        self.setPosHpr(pos[0], pos[1], pos[2], h, 0, 0)
        self.d_setPosHpr(pos[0], pos[1], pos[2], h, 0, 0)
        self.target = self.boss.scene.getRelativePoint(self, Point3(0, dist, 0))
        self.departureTime = globalClock.getFrameTime()
        self.arrivalTime = self.departureTime + walkTime

        self.d_setTarget(self.target[0], self.target[1], h,
                         globalClockDelta.localToNetworkTime(self.arrivalTime))

        self.__startWalk()
        self.d_setObjectState('b', 0, 0)

        taskMgr.doMethodLater(walkTime, self.__recoverWalk, self.uniqueName('recoverWalk'))

    def exitEmergeB(self):
        self.__stopWalk()
        taskMgr.remove(self.uniqueName('recoverWalk'))

    def enterBattle(self):
        self.d_setObjectState('B', 0, 0)

    def exitBattle(self):
        taskMgr.remove(self.taskName("resumeWalk"))

    def enterStunned(self):
        self.d_setObjectState('S', 0, 0)

    def exitStunned(self):
        taskMgr.remove(self.taskName("recovery"))

    def enterRecovery(self):
        self.d_setObjectState('R', 0, 0)
        taskMgr.doMethodLater(2.0, self.__recoverWalk, self.uniqueName('recoverWalk'))

    def exitRecovery(self):
        self.__stopWalk()
        taskMgr.remove(self.uniqueName('recoverWalk'))
