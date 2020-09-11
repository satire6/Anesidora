from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from otp.avatar import DistributedAvatar
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import BattleExperience
from toontown.battle import BattleBase
import BossCog
import SuitDNA
from toontown.coghq import CogDisguiseGlobals
from direct.showbase import Transitions
from toontown.hood import ZoneUtil
from toontown.building import ElevatorUtils
from toontown.building import ElevatorConstants
from toontown.distributed import DelayDelete
from toontown.effects import DustCloud
from toontown.toonbase import TTLocalizer
from toontown.friends import FriendsListManager
from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.showbase import PythonUtil
import random

class DistributedBossCog(DistributedAvatar.DistributedAvatar,
                         BossCog.BossCog):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCog')

    allowClickedNameTag = True #do we let toons click on other toons to see the hp?

    def __init__(self, cr):
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        BossCog.BossCog.__init__(self)

        self.gotAllToons = 0
        self.toonsA = []
        self.toonsB = []
        self.involvedToons = []
        self.toonRequest = None
        self.battleNumber = 0
        self.battleAId = None
        self.battleBId = None
        self.battleA = None
        self.battleB = None
        self.battleRequest = None
        self.arenaSide = 0

        self.toonSphere = None
        self.localToonIsSafe = 0

        self.__toonsStuckToFloor = []
        self.cqueue = None
        self.rays = None
        self.ray1 = None
        self.ray2 = None
        self.ray3 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None

        # These nodes mark the relative positions of the battles that
        # take place on either side of the BossCog.
        self.battleANode = self.attachNewNode('battleA')
        self.battleBNode = self.attachNewNode('battleB')
        self.battleANode.setPosHpr(*ToontownGlobals.BossCogBattleAPosHpr)
        self.battleBNode.setPosHpr(*ToontownGlobals.BossCogBattleBPosHpr)

        self.activeIntervals = {}
        self.flashInterval = None

        self.elevatorType = ElevatorConstants.ELEVATOR_VP

    def announceGenerate(self):
        DistributedAvatar.DistributedAvatar.announceGenerate(self)

        # store the cog-suit level that localToon came in with
        self.prevCogSuitLevel = localAvatar.getCogLevels()[
            CogDisguiseGlobals.dept2deptIndex(self.style.dept)]

        # Put a big trigger bubble around the cog so we can tell the
        # AI when the avatar is within directed-attack range.
        nearBubble = CollisionSphere(0, 0, 0, 50)
        nearBubble.setTangible(0)
        nearBubbleNode = CollisionNode('NearBoss')
        nearBubbleNode.setCollideMask(ToontownGlobals.WallBitmask)
        nearBubbleNode.addSolid(nearBubble)
        self.attachNewNode(nearBubbleNode)
        self.accept('enterNearBoss', self.avatarNearEnter)
        self.accept('exitNearBoss', self.avatarNearExit)

        # Replace the default collision sphere with a pair of tubes
        # along the treads to deflect the toon, and a poly across the
        # top and around the sides to keep out pies.
        self.collNode.removeSolid(0)
        tube1 = CollisionTube(6.5, -7.5, 2, 6.5, 7.5, 2, 2.5)
        tube2 = CollisionTube(-6.5, -7.5, 2, -6.5, 7.5, 2, 2.5)
        roof = CollisionPolygon(
            Point3(-4.4, 7.1, 5.5), Point3(-4.4, -7.1, 5.5),
            Point3(4.4, -7.1, 5.5), Point3(4.4, 7.1, 5.5))
        side1 = CollisionPolygon(
            Point3(-4.4, -7.1, 5.5), Point3(-4.4, 7.1, 5.5),
            Point3(-4.4, 7.1, 0), Point3(-4.4, -7.1, 0))
        side2 = CollisionPolygon(
            Point3(4.4, 7.1, 5.5), Point3(4.4, -7.1, 5.5),
            Point3(4.4, -7.1, 0), Point3(4.4, 7.1, 0))
        front1 = CollisionPolygon(
            Point3(4.4, -7.1, 5.5), Point3(-4.4, -7.1, 5.5),
            Point3(-4.4, -7.1, 5.2), Point3(4.4, -7.1, 5.2))
        back1 = CollisionPolygon(
            Point3(-4.4, 7.1, 5.5), Point3(4.4, 7.1, 5.5),
            Point3(4.4, 7.1, 5.2), Point3(-4.4, 7.1, 5.2))
        self.collNode.addSolid(tube1)
        self.collNode.addSolid(tube2)
        self.collNode.addSolid(roof)
        self.collNode.addSolid(side1)
        self.collNode.addSolid(side2)
        self.collNode.addSolid(front1)
        self.collNode.addSolid(back1)
        self.collNodePath.reparentTo(self.axle)
        self.collNode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask | ToontownGlobals.CameraBitmask)

        # Also listen for collisions with all that.  That hurts!
        self.collNode.setName('BossZap')
        self.setTag('attackCode', str(ToontownGlobals.BossCogElectricFence))
        self.accept('enterBossZap', self.__touchedBoss)

        # Have some bubbles ready to zap the toons with the swat
        # attacks too.
        
        bubbleL = CollisionSphere(10, -5, 0, 10)
        bubbleL.setTangible(0)
        bubbleLNode = CollisionNode('BossZap')
        bubbleLNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleLNode.addSolid(bubbleL)
        self.bubbleL = self.axle.attachNewNode(bubbleLNode)
        self.bubbleL.setTag('attackCode', str(ToontownGlobals.BossCogSwatLeft))
        self.bubbleL.stash()
        
        bubbleR = CollisionSphere(-10, -5, 0, 10)
        bubbleR.setTangible(0)
        bubbleRNode = CollisionNode('BossZap')
        bubbleRNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleRNode.addSolid(bubbleR)
        self.bubbleR = self.axle.attachNewNode(bubbleRNode)
        self.bubbleR.setTag('attackCode', str(ToontownGlobals.BossCogSwatRight))
        self.bubbleR.stash()
        
        bubbleF = CollisionSphere(0, -25, 0, 12)
        bubbleF.setTangible(0)
        bubbleFNode = CollisionNode('BossZap')
        bubbleFNode.setCollideMask(ToontownGlobals.WallBitmask)
        bubbleFNode.addSolid(bubbleF)
        self.bubbleF = self.rotateNode.attachNewNode(bubbleFNode)
        self.bubbleF.setTag('attackCode', str(ToontownGlobals.BossCogFrontAttack))
        self.bubbleF.stash()

    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        DistributedAvatar.DistributedAvatar.disable(self)

        self.battleAId = None
        self.battleBId = None
        self.battleA = None
        self.battleB = None
        self.cr.relatedObjectMgr.abortRequest(self.toonRequest)
        self.toonRequest = None
        self.cr.relatedObjectMgr.abortRequest(self.battleRequest)
        self.battleRequest = None

        self.stopAnimate()
        self.cleanupIntervals()
        self.cleanupFlash()
        self.disableLocalToonSimpleCollisions()
        self.ignoreAll()
        
    def delete(self):
        """
        This method is called when the DistributedObject is
        permanently removed from the world and deleted from
        the cache.
        """
        try:
            self.DistributedBossCog_deleted
        except:
            self.DistributedBossCog_deleted = 1
            self.ignoreAll()
            DistributedAvatar.DistributedAvatar.delete(self)
            BossCog.BossCog.delete(self)
        return


    # We need to force the BossCog version of these to be called, otherwise
    # we get the generic Avatar version which is undefined
    def setDNAString(self, dnaString):
        BossCog.BossCog.setDNAString(self, dnaString)

    def getDNAString(self):
        return self.dna.makeNetString()

    def setDNA(self, dna):
        BossCog.BossCog.setDNA(self, dna)


    def setToonIds(self, involvedToons, toonsA, toonsB):
        self.involvedToons = involvedToons
        self.toonsA = toonsA
        self.toonsB = toonsB

        self.cr.relatedObjectMgr.abortRequest(self.toonRequest)
        self.gotAllToons = 0
        self.toonRequest = self.cr.relatedObjectMgr.requestObjects(
            self.involvedToons, allCallback = self.__gotAllToons,
            eachCallback = self.gotToon)



    def getDialogueArray(self, *args):
        # Force the right inheritance chain to be called
        return BossCog.BossCog.getDialogueArray(self, *args)

    def storeInterval(self, interval, name):
        if name in self.activeIntervals:
            ival = self.activeIntervals[name]
            # if the interval has a delayDelete, finish it now and destroy the delayDeletes
            # otherwise, preserve the original behavior of letting the old interval continue
            # to run if it's running
            if (hasattr(ival, 'delayDelete') or hasattr(ival, 'delayDeletes')):
                self.clearInterval(name, finish=1)
        self.activeIntervals[name] = interval

    def cleanupIntervals(self):
        for interval in self.activeIntervals.values():
            interval.finish()
            DelayDelete.cleanupDelayDeletes(interval)
        self.activeIntervals = {}

    def clearInterval(self, name, finish=1):
        """ Clean up the specified Interval
        """
        if (self.activeIntervals.has_key(name)):
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if self.activeIntervals.has_key(name):
                DelayDelete.cleanupDelayDeletes(ival)
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)

    def finishInterval(self, name):
        """ Force the specified Interval to jump to the end
        """ 
        if (self.activeIntervals.has_key(name)):
            interval = self.activeIntervals[name]
            interval.finish()

    def d_avatarEnter(self):
        assert self.notify.debug("d_avatarEnter()")
        self.sendUpdate('avatarEnter', [])

    def d_avatarExit(self):
        assert self.notify.debug("d_avatarExit()")
        self.sendUpdate('avatarExit', [])

    def avatarNearEnter(self, entry):
        self.sendUpdate('avatarNearEnter', [])

    def avatarNearExit(self, entry):
        self.sendUpdate('avatarNearExit', [])
        

    def hasLocalToon(self):
        # Returns true if localToon is involved in the final movies or
        # battle.  This will generally always be true in production,
        # but during testing a toon might arrive in the middle of a
        # battle-in-progress, and we go a little out of our way to be
        # polite and not crash this player, even though he can't
        # participate.
        doId = localAvatar.doId
        return (doId in self.toonsA) or (doId in self.toonsB)


    def setBattleExperience(self,
                            id0, origExp0, earnedExp0, origQuests0, items0, missedItems0,
                            origMerits0, merits0, parts0,
                            id1, origExp1, earnedExp1, origQuests1, items1, missedItems1,
                            origMerits1, merits1, parts1,
                            id2, origExp2, earnedExp2, origQuests2,items2, missedItems2,
                            origMerits2, merits2, parts2,
                            id3, origExp3, earnedExp3, origQuests3,items3, missedItems3,
                            origMerits3, merits3, parts3,
                            id4, origExp4, earnedExp4, origQuests4, items4, missedItems4,
                            origMerits4, merits4, parts4,
                            id5, origExp5, earnedExp5, origQuests5,items5, missedItems5,
                            origMerits5, merits5, parts5,
                            id6, origExp6, earnedExp6, origQuests6, items6, missedItems6,
                            origMerits6, merits6, parts6,
                            id7, origExp7, earnedExp7, origQuests7, items7, missedItems7,
                            origMerits7, merits7, parts7,
                            deathList, uberList, helpfulToons):
        
        self.deathList = deathList
        self.uberList = uberList
        self.helpfulToons = helpfulToons
        entries = ((id0, origExp0, earnedExp0, origQuests0, items0, missedItems0,
                    origMerits0, merits0, parts0),
                   (id1, origExp1, earnedExp1, origQuests1, items1, missedItems1,
                    origMerits1, merits1, parts1),
                   (id2, origExp2, earnedExp2, origQuests2, items2, missedItems2,
                    origMerits2, merits2, parts2),
                   (id3, origExp3, earnedExp3, origQuests3, items3, missedItems3,
                    origMerits3, merits3, parts3),
                   (id4, origExp4, earnedExp4, origQuests4, items4, missedItems4,
                    origMerits4, merits4, parts4),
                   (id5, origExp5, earnedExp5, origQuests5, items5, missedItems5,
                    origMerits5, merits5, parts5),
                   (id6, origExp6, earnedExp6, origQuests6, items6, missedItems6,
                    origMerits6, merits6, parts6),
                   (id7, origExp7, earnedExp7, origQuests7, items7, missedItems7,
                    origMerits7, merits7, parts7))
                   
        self.toonRewardDicts = BattleExperience.genRewardDicts(entries)
        self.toonRewardIds = [id0,id1,id2,id3,id4,id5,id6,id7]


    def setArenaSide(self, arenaSide):
        self.arenaSide = arenaSide
    
    def setState(self, state):
        self.request(state)

    def gotToon(self, toon):
        # A new Toon has arrived.  Put him in the right spot, if we
        # know what that is yet.  Normally, we will only see this
        # message in the WaitForToons state, or in the Off state if they
        # came in early (but someone might arrive to the battle very
        # late and see everything already advanced to the next state).
        stateName = self.state
        assert self.notify.debug("gotToon(%s) in state %s" % (toon.doId, stateName))

    def __gotAllToons(self, toons):
        # We've seen all the Toons we're expecting.
        assert self.notify.debug("gotAllToons()")
        self.gotAllToons = 1
        messenger.send('gotAllToons')

    def setBattleIds(self, battleNumber, battleAId, battleBId):
        assert self.notify.debug("setBattleIds(%s, %s)" % (battleAId, battleBId))
        self.battleNumber = battleNumber
        self.battleAId = battleAId
        self.battleBId = battleBId

        self.cr.relatedObjectMgr.abortRequest(self.battleRequest)
        self.battleRequest = self.cr.relatedObjectMgr.requestObjects(
            [self.battleAId, self.battleBId],
            allCallback = self.__gotBattles)
        
    def __gotBattles(self, battles):
        assert self.notify.debug("gotBattles(%s, %s)" % (repr(battles[0]), repr(battles[1])))
        self.battleRequest = None

        if self.battleA and self.battleA != battles[0]:
            self.battleA.cleanupBattle()
        
        if self.battleB and self.battleB != battles[1]:
            self.battleB.cleanupBattle()
        
        self.battleA = battles[0]
        self.battleB = battles[1]

    def cleanupBattles(self):
        # Call this to clean up the battle objects and make sure
        # they're not hanging on to toons or camera modes or
        # something.
        assert self.notify.debug("cleanupBattles()")
        
        if self.battleA:
            self.battleA.cleanupBattle()
        if self.battleB:
            self.battleB.cleanupBattle()

    def makeEndOfBattleMovie(self, hasLocalToon):
        assert self.notify.debug("makeEndOfBattleMovie(%s)" % (hasLocalToon))

        # Generate a little interval to be played at the end of a
        # battle, to show progress or encouragement or something.
        return Sequence()

    def controlToons(self):
        # Turn off remote control of the toons.  We'll move them
        # around locally for now.
        assert(self.notify.debug("controlToons"))        
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.stopLookAround()
                toon.stopSmooth()

        # Also put the local toon in movie mode so he won't try to
        # walk around on his own.
        if self.hasLocalToon():
            self.toMovieMode()

    def enableLocalToonSimpleCollisions(self):
        # Enable a simple collision sphere around the local toon so we
        # can lerp him around and not inadvertently push him through
        # walls or floors.
        if not self.toonSphere:
            sphere = CollisionSphere(0, 0, 1, 1)
            sphere.setRespectEffectiveNormal(0)
            sphereNode = CollisionNode('SimpleCollisions')
            sphereNode.setFromCollideMask(ToontownGlobals.WallBitmask | ToontownGlobals.FloorBitmask)
            sphereNode.setIntoCollideMask(BitMask32.allOff())
            sphereNode.addSolid(sphere)
            self.toonSphere = NodePath(sphereNode)
            self.toonSphereHandler = CollisionHandlerPusher()
            self.toonSphereHandler.addCollider(self.toonSphere, localAvatar)
        self.toonSphere.reparentTo(localAvatar)
        base.cTrav.addCollider(self.toonSphere, self.toonSphereHandler)
            
    def disableLocalToonSimpleCollisions(self):
        if self.toonSphere:
            base.cTrav.removeCollider(self.toonSphere)
            self.toonSphere.detachNode()
    
    def toOuchMode(self):
        # Move the localToon to 'ouch' mode: we've been hit by
        # something and can't move while we recover.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('ouch')
    
    def toCraneMode(self):
        # Move the localToon to 'crane' mode: we're not walking the
        # avatar around, but we're still controlling something
        # in-game, e.g. to move the cranes in the CFO battle.
        # Collisions are still active.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('crane')

    def toMovieMode(self):
        # Move the localToon to 'movie' mode: we're totally in control
        # of the game logic, watching a cutscene.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('movie')

    def toWalkMode(self):
        # Move the localToon to 'walk' mode.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('walk')

    def toFinalBattleMode(self):
        # Move the localToon to 'finalBattle' mode.  Similar to walk
        # mode but without a teleport out button.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('finalBattle')

    def releaseToons(self, finalBattle = 0):
        # Allow the toons to control themselves.
        assert(self.notify.debug("releaseToons %d" % finalBattle))
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                if self.battleA and toon in self.battleA.toons:
                    # The battle owns this toon.
                    pass
                elif self.battleB and toon in self.battleB.toons:
                    # The battle owns this toon.
                    pass
                else:
                    toon.startLookAround()
                    toon.startSmooth()
                    toon.wrtReparentTo(render)

                    if toon == localAvatar:
                        if finalBattle:
                            self.toFinalBattleMode()
                        else:
                            self.toWalkMode()

    def stickToonsToFloor(self):
        # Put a CollisionRay to each toon to ensure that it is stuck
        # to the floor during an animation (especially while moving
        # the toons on a mopath).

        # This creates a number of CollisionHandlers which are
        # registered with the CollisionTraverser; these will be
        # disabled when unstickToons() is called.

        # Make sure we don't already have some sticky toons.
        self.unstickToons()

        # First, create a CollisionRay in a node.  This same node is
        # instanced to each toon.
        
        rayNode = CollisionNode('stickToonsToFloor')
        rayNode.addSolid(CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0))
        rayNode.setFromCollideMask(ToontownGlobals.FloorBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        ray = NodePath(rayNode)

        # Also create a lifter.  This same handler can be shared by
        # all toons.
        lifter = CollisionHandlerFloor()
        lifter.setOffset(ToontownGlobals.FloorOffset)
        lifter.setReach(10.0)

        # Now, walk through the list of toons and activate each one with
        # a special lifter.
        for toonId in self.involvedToons:
            toon = base.cr.doId2do.get(toonId)
            if toon:
                toonRay = ray.instanceTo(toon)
                lifter.addCollider(toonRay, toon)
                base.cTrav.addCollider(toonRay, lifter)
                self.__toonsStuckToFloor.append(toonRay)

    def unstickToons(self):
        # Undoes a previous call to stickToonsToFloor(): this
        # removes all of the colliders from the CollisionTraverser and
        # leaves the toons to find their own altitude.
        for toonRay in self.__toonsStuckToFloor:
            base.cTrav.removeCollider(toonRay)
            toonRay.removeNode()
        self.__toonsStuckToFloor = []

    def stickBossToFloor(self):
        # Put a trio of CollisionRays under the Boss Cog, one in
        # front, one in the center, and one behind, so we can do the
        # right thing as he rolls up and over ramps.

        # This creates a pair of CollisionHandlers which are
        # registered with the CollisionTraverser; these will be
        # disabled when unstickBoss() is called.

        self.unstickBoss()

        # First, create three CollisionRays, and put them together in
        # a node.

        self.ray1 = CollisionRay(0.0, 10.0, 20.0, 0.0, 0.0, -1.0)
        self.ray2 = CollisionRay(0.0, 0.0, 20.0, 0.0, 0.0, -1.0)
        self.ray3 = CollisionRay(0.0, -10.0, 20.0, 0.0, 0.0, -1.0)
        
        rayNode = CollisionNode('stickBossToFloor')
        rayNode.addSolid(self.ray1)
        rayNode.addSolid(self.ray2)
        rayNode.addSolid(self.ray3)
        rayNode.setFromCollideMask(ToontownGlobals.FloorBitmask)
        rayNode.setIntoCollideMask(BitMask32.allOff())
        self.rays = self.attachNewNode(rayNode)

        # Now the handler for these will be a CollisionHandlerQueue,
        # which we query directly.  (We can't use a
        # CollisionHandlerFloor, which doesn't know about multiple
        # rays.)
        self.cqueue = CollisionHandlerQueue()
        base.cTrav.addCollider(self.rays, self.cqueue)

    def rollBoss(self, t, fromPos, deltaPos):
        # This method is called each frame during the rollToBattleTwo
        # interval and bossDamage interval.  It applies a lerp from
        # fromPos to toPos, while sticking the boss to the floor, and
        # rotatating him properly.

        # First, set the boss to the appropriate point.
        self.setPos(fromPos + deltaPos * t)

        if not self.cqueue:
            return
        
        # Find the first three entries that correspond to our three
        # rays.
        self.cqueue.sortEntries()
        numEntries = self.cqueue.getNumEntries()
        if numEntries != 0:
            for i in range(self.cqueue.getNumEntries() - 1, -1, -1):
                entry = self.cqueue.getEntry(i)
                solid = entry.getFrom()
                if solid == self.ray1:
                    self.e1 = entry
                elif solid == self.ray2:
                    self.e2 = entry
                elif solid == self.ray3:
                    self.e3 = entry
                else:
                    self.notify.warning("Unexpected ray in __liftBoss")
                    return

            # Now be sure the queue is cleared for next time.
            self.cqueue.clearEntries()

        if not (self.e1 and self.e2 and self.e3):
            self.notify.debug("Some points missed in __liftBoss")
            return
        
        # Now get the three points that each of these detected.
        p1 = self.e1.getSurfacePoint(self)
        p2 = self.e2.getSurfacePoint(self)
        p3 = self.e3.getSurfacePoint(self)

        # Draw a line between p1 and p3 to determine the hypothetical
        # center point if we're going up a ramp.
        p2a = (p1 + p3) / 2

        # Our actual height is based on the higher of p2 and p2a.
        if (p2a[2] > p2[2]):
            center = p2a
        else:
            center = p2
        self.setZ(self, center[2])

        # Now, is the Boss level, or tilted?

        if p1[2] > p2[2] + 0.01 or p3[2] > p2[2] + 0.01:
            # It's tilted by the full ratio if either end point is
            # much above the center point.
            mat = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            if abs(p3[2] - center[2]) < abs(p1[2] - center[2]):
                lookAt(mat, Vec3(p1 - center), CSDefault)
            else:
                lookAt(mat, Vec3(center - p3), CSDefault)
            self.rotateNode.setMat(mat)

        else:
            # Otherwise, it's level.
            self.rotateNode.clearTransform()
        

    def unstickBoss(self):
        # Undoes a previous call to stickBossToFloor(): this
        # removes all of the colliders from the CollisionTraverser and
        # leaves the boss to find its own altitude and orientation.
        if self.rays:
            base.cTrav.removeCollider(self.rays)
            self.rays.removeNode()
            
        self.rays = None
        self.ray1 = None
        self.ray2 = None
        self.ray3 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.rotateNode.clearTransform()

        self.cqueue = None
            
    def rollBossToPoint(self, fromPos, fromHpr, toPos, toHpr, reverse):
        vector = Vec3(toPos - fromPos)
        distance = vector.length()

        if toHpr == None:
            # Compute the destination hpr.
            mat = Mat3(0, 0, 0, 0, 0, 0, 0, 0, 0)
            headsUp(mat, vector, CSDefault)
            scale = VBase3(0, 0, 0)
            shear = VBase3(0, 0, 0)
            toHpr = VBase3(0, 0, 0)
            decomposeMatrix(mat, scale, shear, toHpr, CSDefault)

        if fromHpr:
            # Fit the toHpr to the same semicircle as the supplied
            # fromHpr.
            newH = PythonUtil.fitDestAngle2Src(fromHpr[0], toHpr[0])
            toHpr = VBase3(newH, 0, 0)

        else:
            # If no fromHpr is given, it's the same as toHpr.
            fromHpr = toHpr
            
        turnTime = abs(toHpr[0] - fromHpr[0]) / ToontownGlobals.BossCogTurnSpeed
        if toHpr[0] < fromHpr[0]:
            leftRate = ToontownGlobals.BossCogTreadSpeed
        else:
            leftRate = -ToontownGlobals.BossCogTreadSpeed
        if reverse:
            rollTreadRate = -ToontownGlobals.BossCogTreadSpeed
        else:
            rollTreadRate = ToontownGlobals.BossCogTreadSpeed
            
        rollTime = distance / ToontownGlobals.BossCogRollSpeed
        deltaPos = toPos - fromPos
        track = Sequence(Func(self.setPos, fromPos),
                         Func(self.headsUp, toPos),
                         Parallel(self.hprInterval(turnTime, toHpr, fromHpr),
                                  self.rollLeftTreads(turnTime, leftRate),
                                  self.rollRightTreads(turnTime, -leftRate),
                                  #SoundInterval(self.treadsSfx, duration = turnTime, loop = 1, volume = 0.2),
                                  ),
                         Parallel(LerpFunctionInterval(self.rollBoss,
                                                       duration = rollTime,
                                                       extraArgs = [fromPos, deltaPos]),
                                  self.rollLeftTreads(rollTime, rollTreadRate),
                                  self.rollRightTreads(rollTime, rollTreadRate),
                                  #SoundInterval(self.treadsSfx, duration = rollTime, loop = 1, volume = 0.2),
                                  ),
                         )

        # Return both the computed track and the destination hpr
        # (which might be useful for the next sequence).
        return track, toHpr


    def setupElevator(self, elevatorModel):
        self.elevatorModel = elevatorModel
    
        self.leftDoor = self.elevatorModel.find("**/left-door")
        if self.leftDoor.isEmpty():
            self.leftDoor = self.elevatorModel.find("**/left_door")
        self.rightDoor = self.elevatorModel.find("**/right-door")
        if self.rightDoor.isEmpty():
            self.rightDoor = self.elevatorModel.find("**/right_door")

        self.openSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
        self.finalOpenSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
        self.closeSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
        self.finalCloseSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
        self.openDoors = ElevatorUtils.getOpenInterval(self, self.leftDoor, self.rightDoor,
                                                       self.openSfx, self.finalOpenSfx,
                                                       self.elevatorType)
        self.closeDoors = ElevatorUtils.getCloseInterval(self, self.leftDoor, self.rightDoor,
                                                         self.closeSfx, self.finalCloseSfx,
                                                         self.elevatorType)

        # Guarantee the elevator doors are closed.
        self.closeDoors.start()
        self.closeDoors.finish()

    def putToonInCogSuit(self, toon):
        if not toon.isDisguised:
            deptIndex = SuitDNA.suitDepts.index(self.style.dept)
            toon.setCogIndex(deptIndex)

        # This shouldn't be necessary.
        toon.getGeomNode().hide()
        
    def placeToonInElevator(self, toon):
        self.putToonInCogSuit(toon)
        
        toonIndex = self.involvedToons.index(toon.doId)
        toon.reparentTo(self.elevatorModel)
        toon.setPos(*ElevatorConstants.BigElevatorPoints[toonIndex])
        toon.setHpr(180, 0, 0)
        toon.suit.loop('neutral')

    def toonNormalEyes(self, toons, bArrayOfObjs = False):
        # Returns a track that sets the Toon's eyes to normal, after
        # the loseCogSuits track made them sad.  This will be played
        # during a camera cut.

        if bArrayOfObjs:
            toonObjs = toons
        else:
            toonObjs = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonObjs.append(toon)
        
        seq = Sequence()

        for toon in toonObjs:
            seq.append(Func(toon.normalEyes))
            seq.append(Func(toon.blinkEyes))

        return seq

    def toonDied(self, avId):
        assert self.notify.debug('toonDied(%s)' % (avId))

        # The AI is telling us that a toon has met his untimely end.
        # Maybe it's us!
        if avId == localAvatar.doId:
            self.localToonDied()
            

    def localToonToSafeZone(self):
        assert self.notify.debug('localToonToSafeZone()')
        
        target_sz = ZoneUtil.getSafeZoneId(localAvatar.defaultZone)

        place = self.cr.playGame.getPlace()
        place.fsm.request('teleportOut', [{
            "loader" : ZoneUtil.getLoaderName(target_sz),
            "where" : ZoneUtil.getWhereName(target_sz, 1),
            'how' : 'teleportIn',
            'hoodId' : target_sz,
            'zoneId' : target_sz,
            'shardId' : None,
            'avId' : -1,
            'battle' : 1,
            }])

    def localToonDied(self):
        assert self.notify.debug('localToonToSafeZone()')
        
        target_sz = ZoneUtil.getSafeZoneId(localAvatar.defaultZone)

        place = self.cr.playGame.getPlace()
        place.fsm.request('died', [{
            "loader" : ZoneUtil.getLoaderName(target_sz),
            "where" : ZoneUtil.getWhereName(target_sz, 1),
            'how' : 'teleportIn',
            'hoodId' : target_sz,
            'zoneId' : target_sz,
            'shardId' : None,
            'avId' : -1,
            'battle' : 1,
            }])
    

    def toonsToBattlePosition(self, toonIds, battleNode):
        # Position the toons in the list to their appropriate position
        # relative to the indicated battleNode.

        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]

        self.notify.debug("toonsToBattlePosition: points = %s" % points[0][0])
        
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                toon.reparentTo(render)
                pos, h = points[i]

                self.notify.debug("toonsToBattlePosition: battleNode=%s %.2f %.2f %.2f %.2f %.2f %.2f" % (battleNode, pos[0], pos[1], pos[2], h, 0, 0))

                self.notify.debug("old toon pos %s" % toon.getPos())
                self.notify.debug("pos=%.2f %.2f %.2f h=%.2f" % (pos[0], pos[1], pos[2], h))
                self.notify.debug("battleNode.pos = %s" % battleNode.getPos())
                self.notify.debug("battleNode.hpr = %s" % battleNode.getHpr())
                toon.setPosHpr(battleNode, pos[0], pos[1], pos[2], h, 0, 0)
                self.notify.debug("new toon pos %s " % toon.getPos())
        
    def __touchedBoss(self, entry):
        assert self.notify.debug("__touchedBoss()")
        # The localToon has come into contact with the boss's
        # undercarriage, or one of his attack spheres.  Zap!

        # Get the attack code from the thing we touched.
        self.notify.debug('%s' % entry)
        self.notify.debug('fromPos = %s' % entry.getFromNodePath().getPos(render))
        self.notify.debug('intoPos = %s' % entry.getIntoNodePath().getPos(render))
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning("Node %s has no attackCode tag." % (repr(entry.getIntoNodePath())))
            return
        attackCode = int(attackCodeStr)
        if attackCode == ToontownGlobals.BossCogLawyerAttack and \
           self.dna.dept != 'l':
            self.notify.warning('got lawyer attack but not in CJ boss battle')
            return

        self.zapLocalToon(attackCode)

    def zapLocalToon(self, attackCode, origin = None):
        if self.localToonIsSafe or localAvatar.ghostMode or localAvatar.isStunned:
            return
        messenger.send('interrupt-pie')
        
        place = self.cr.playGame.getPlace()
        currentState = None
        if place:
            currentState = place.fsm.getCurrentState().getName()
        if currentState != 'walk' and currentState != 'finalBattle' and currentState != 'crane':
            # Ignore this except when the Toon's in walk mode.
            return

        toon = localAvatar

        fling = 1 
        shake = 0
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            # For an area attack, we don't fling or move the toons,
            # but we do shake the camera.
            fling = 0
            shake = 1

        if fling:
            if origin == None:
                origin = self
            
            # Face the toon towards the boss's center (so he can get
            # knocked backwards), but keep the camera in the same place.
            camera.wrtReparentTo(render)
            toon.headsUp(origin)
            camera.wrtReparentTo(toon)

        # Also tell the boss where we are relative to him, so he can
        # decide whether to swat at us.
        bossRelativePos = toon.getPos(self.getGeomNode())
        bp2d = Vec2(bossRelativePos[0], bossRelativePos[1])
        bp2d.normalize()
        
        pos = toon.getPos()
        hpr = toon.getHpr()
        timestamp = globalClockDelta.getFrameNetworkTime()

        self.sendUpdate('zapToon', [pos[0], pos[1], pos[2],
                                    hpr[0], hpr[1], hpr[2],
                                    bp2d[0], bp2d[1],
                                    attackCode, timestamp])

        self.doZapToon(toon, fling = fling, shake = shake)

    def showZapToon(self, toonId, x, y, z, h, p, r, attackCode, timestamp):
        # This message comes from the AI to show the indicated
        # distributed toon getting zapped.
        if toonId == localAvatar.doId:
            # Ignore messages about localToon; he already zapped himself.
            return
            
        ts = globalClockDelta.localElapsedTime(timestamp)
        pos = Point3(x, y, z)
        hpr = VBase3(h, p, r)
        fling = 1

        toon = self.cr.doId2do.get(toonId)
        if toon:
            if attackCode == ToontownGlobals.BossCogAreaAttack:
                # For an area attack, we don't fling or move the toons.
                pos = None
                hpr = None
                fling = 0

            else:
                # Delay the zap by the same amount of time as the smoothing
                # delay, so it will be in sync with the running animation.
                ts -= toon.smoother.getDelay()
            
            self.doZapToon(toon, pos = pos, hpr = hpr, ts = ts, fling = fling)

    def doZapToon(self, toon, pos = None, hpr = None, ts = 0,
                    fling = 1, shake = 1):
        # The indicated distributed toon has come into contact with
        # something that hurts him.  Play a little movie showing him
        # getting zapped.
        
        zapName = toon.uniqueName('zap')
        self.clearInterval(zapName)
        
        zapTrack = Sequence(name = zapName)

        if toon == localAvatar:
            # In the case of localToon, set the state to ouch
            # immediately, rather than waiting a frame or two for the
            # interval to get there.
            self.toOuchMode()
            messenger.send('interrupt-pie')

            # But also set up an active collision sphere, similar to
            # the one we have in walk mode, just so the local toon
            # won't get pushed through a wall by our lerp, below.
            self.enableLocalToonSimpleCollisions()
        else:
            zapTrack.append(Func(toon.stopSmooth))

        def getSlideToPos(toon = toon):
            return render.getRelativePoint(toon, Point3(0, -5, 0))

        if pos != None and hpr != None:
            zapTrack.append(Func(toon.setPosHpr, pos, hpr)),

        toonTrack = Parallel()

        if shake and toon == localAvatar:
            toonTrack.append(Sequence(Func(camera.setZ, camera, 1),
                                      Wait(0.15),
                                      Func(camera.setZ, camera, -2),
                                      Wait(0.15),
                                      Func(camera.setZ, camera, 1),
                                      ))

        if fling:
            toonTrack += [ActorInterval(toon, 'slip-backward'),
                          toon.posInterval(0.5, getSlideToPos, fluid = 1)]
        else:
            toonTrack += [ActorInterval(toon, 'slip-forward')]
            
        zapTrack.append(toonTrack)
        
        if toon == localAvatar:
            zapTrack.append(Func(self.disableLocalToonSimpleCollisions))
            currentState = self.state
            if currentState == 'BattleThree':
                zapTrack.append(Func(self.toFinalBattleMode))
            else:
                if hasattr(self, 'chairs'):
                    #if we have chairs, in battle two of lawbot boss
                    zapTrack.append(Func(self.toFinalBattleMode))
                else:
                    zapTrack.append(Func(self.toWalkMode))
        else:
            zapTrack.append(Func(toon.startSmooth))

        if (ts > 0):
            # We're already late.
            startTime = ts
        else:
            # We need to wait a bit.
            zapTrack = Sequence(Wait(-ts), zapTrack)
            startTime = 0

        zapTrack.append(Func(self.clearInterval, zapName))

        zapTrack.delayDelete = DelayDelete.DelayDelete(toon, 'BossCog.doZapToon')
        zapTrack.start(startTime)
        self.storeInterval(zapTrack, zapName)

    def setAttackCode(self, attackCode, avId = 0):
        # This message is sent from the AI to tell the Boss Cog to
        # animate some attack.
        assert self.notify.debug("setAttackCode(%s, %s) time=%f" %
                                 (attackCode, avId, globalClock.getFrameTime()))
        self.attackCode = attackCode
        self.attackAvId = avId

        if attackCode == ToontownGlobals.BossCogDizzy:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate(None, raised = 0, happy = 1)

        elif attackCode == ToontownGlobals.BossCogDizzyNow:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate('hit', happy = 1, now = 1)

        elif attackCode == ToontownGlobals.BossCogSwatLeft:
            self.setDizzy(0)
            self.doAnimate('ltSwing', now = 1)
            
        elif attackCode == ToontownGlobals.BossCogSwatRight:
            self.setDizzy(0)
            self.doAnimate('rtSwing', now = 1)

        elif attackCode == ToontownGlobals.BossCogAreaAttack:
            self.setDizzy(0)
            self.doAnimate('areaAttack', now = 1)

        elif attackCode == ToontownGlobals.BossCogFrontAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now = 1)

        elif attackCode == ToontownGlobals.BossCogRecoverDizzyAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now = 1)

        elif attackCode == ToontownGlobals.BossCogDirectedAttack or \
             attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
            # Rotate to face the toon and spit out gears.
            self.setDizzy(0)
            self.doDirectedAttack(avId, attackCode)

        elif attackCode == ToontownGlobals.BossCogNoAttack:
            # Just stand up.
            self.setDizzy(0)
            self.doAnimate(None, raised = 1)

    def cleanupAttacks(self):
        # Stops any attack currently running.
        pass

    def cleanupFlash(self):
        if self.flashInterval:
            self.flashInterval.finish()
            self.flashInterval = None

    def flashRed(self):
        # Flash the boss cog red to emphasize that he's been hit.
        self.cleanupFlash()
        
        self.setColorScale(1, 1, 1, 1)
        i = Sequence(self.colorScaleInterval(0.1, colorScale = VBase4(1, 0, 0, 1)),
                     self.colorScaleInterval(0.3, colorScale = VBase4(1, 1, 1, 1)))
        self.flashInterval = i
        i.start()

    def flashGreen(self):
        # Flash the boss cog red to emphasize that he's been healed. (Lawyers put evidence on the prosecution pan)
        self.cleanupFlash()

        if not self.isEmpty():
            self.setColorScale(1, 1, 1, 1)
            i = Sequence(self.colorScaleInterval(0.1, colorScale = VBase4(0, 1, 0, 1)),
                         self.colorScaleInterval(0.3, colorScale = VBase4(1, 1, 1, 1)))
            self.flashInterval = i
            i.start()


    def getGearFrisbee(self):
        return loader.loadModel('phase_9/models/char/gearProp')        

    def backupToonsToBattlePosition(self, toonIds, battleNode):
        # Returns a movie showing the toons backing up from promotion
        # position to battle position.
        self.notify.debug("backupToonsToBattlePosition:")
        
        ival = Parallel()

        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]
        
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                pos, h = points[i]
                pos = render.getRelativePoint(battleNode, pos)
                ival.append(Sequence(
                    Func(toon.setPlayRate, -0.8, 'walk'),
                    Func(toon.loop, 'walk'),
                    toon.posInterval(3, pos),
                    Func(toon.setPlayRate, 1, 'walk'),
                    Func(toon.loop,'neutral'),
                    ))

        return ival

    def loseCogSuits(self, toons, battleNode, camLoc, arrayOfObjs = False):
        # Returns a movie showing the line of toons losing their Cog suits.
        seq = Sequence()

        if not toons:
            # If there are no toons in the list, never mind.
            return seq

        self.notify.debug("battleNode=%s camLoc=%s" % (battleNode, camLoc))
        seq.append(Func(camera.setPosHpr, battleNode, *camLoc))

        suitsOff = Parallel()

        #build array of toon objects
        if arrayOfObjs:
            toonArray = toons
        else:
            toonArray = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonArray.append(toon)

        for toon in toonArray:
            dustCloud = DustCloud.DustCloud()
            dustCloud.setPos(0, 2, 3)
            dustCloud.setScale(0.5)

            # In this scene we happen to have four adjacent dust
            # clouds that overlap each other.  To prevent them
            # from clipping each other, we turn off depth write,
            # and then force the clouds to be drawn last in the
            # scene by putting them in the 'fixed' bin.  We can do
            # this because the camera is locked down and we know
            # there is nothing between the dust clouds and the
            # camera.
            dustCloud.setDepthWrite(0)
            dustCloud.setBin('fixed', 0)

            dustCloud.createTrack()
            suitsOff.append(Sequence(
                Func(dustCloud.reparentTo, toon),
                Parallel(dustCloud.track,
                         Sequence(Wait(0.3),
                                  Func(toon.takeOffSuit),
                                  Func(toon.sadEyes),
                                  Func(toon.blinkEyes),
                                  Func(toon.play, 'slip-backward'),
                                  Wait(0.7),
                                  )),
                Func(dustCloud.detachNode),
                Func(dustCloud.destroy)),
                            )

        seq.append(suitsOff)        
        return seq

    def doDirectedAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            gearRoot = self.rotateNode.attachNewNode('gearRoot')
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            gearModel = self.getGearFrisbee()
            gearModel.setScale(0.2)

            # First, get just the H value towards the toon.
            gearRoot.headsUp(toon)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)

            # Now pitch towards the toon so we can throw gears at him.
            gearRoot.lookAt(toon)

            neutral = 'Fb_neutral'
            if not self.twoFaced:
                neutral = 'Ff_neutral'

            gearTrack = Parallel()
            for i in range(4):
                node = gearRoot.attachNewNode(str(i))
                node.hide()
                node.setPos(0, 5.85, 4.0)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                h = random.uniform(-720, 720)
                gearTrack.append(Sequence(
                    Wait(i * 0.15),
                    Func(node.show),
                    Parallel(node.posInterval(1, Point3(x, 50, z), fluid = 1),
                             node.hprInterval(1, VBase3(h, 0, 0), fluid = 1)),
                    Func(node.detachNode)))

            # A 1-second animation to play while rotating.  It might
            # be the neutral cycle, or the climb-up cycle.
            if not self.raised:
                neutral1Anim = self.getAnim('down2Up')
                self.raised = 1
            else:
                neutral1Anim = ActorInterval(self, neutral, startFrame = 48)
                
            throwAnim = self.getAnim('throw')
            neutral2Anim = ActorInterval(self, neutral)

            extraAnim = Sequence()
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                # If it's the "slow" attack, pause for a bit longer
                # here to give the player more warning.
                extraAnim = ActorInterval(self, neutral)

            seq = Sequence(
                ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)),
                                    neutral1Anim),
                extraAnim,
                Parallel(Sequence(Wait(0.19),
                                  gearTrack,
                                  Func(gearRoot.detachNode),
                                  self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                         Sequence(throwAnim, neutral2Anim)))

            self.doAnimate(seq, now = 1, raised = 1)

    def announceAreaAttack(self):
        # The boss cog has finished his area attack.  Any Toons still
        # on the ground at this moment report a hit.

        # This assumes we have a PhysicsWalker in use.  Is there a way
        # to get this information without so many dots?
        if not getattr(localAvatar.controlManager.currentControls, "isAirborne", 0):
            self.zapLocalToon(ToontownGlobals.BossCogAreaAttack)
        

    ##### Environment #####

    def loadEnvironment(self):
        # Elevator: play the introduction-to-danger sting
        self.elevatorMusic = base.loadMusic(
            'phase_7/audio/bgm/tt_elevator.mid')
        self.stingMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')            
            #'phase_9/audio/bgm/encntr_sting_announce.mid')
        # Battle one: play the standard street battle music
        self.battleOneMusic = base.loadMusic(
            'phase_3.5/audio/bgm/encntr_general_bg.mid')
        # Battle three: play the final boss battle music
        self.battleThreeMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
            # 'phase_9/audio/bgm/encntr_suit_winning.mid')
        # Reward: play the reward music
        self.epilogueMusic = base.loadMusic(
            'phase_9/audio/bgm/encntr_hall_of_fame.mid')
            #'phase_9/audio/bgm/CogHQ_finale.mid')            
        

    def unloadEnvironment(self):
        pass

    ##### Off state #####

    def enterOff(self):
        assert self.notify.debug('enterOff()')
        self.cleanupIntervals()
        self.hide()
        self.clearChat()
        self.toWalkMode()

    def exitOff(self):
        self.show()


    ##### WaitForToons state #####

    def enterWaitForToons(self):
        assert self.notify.debug('enterWaitForToons()')

        # Here we are waiting in the dark for the toons to arrive in
        # the elevator.
        self.cleanupIntervals()
        self.hide()

        if self.gotAllToons:
            self.__doneWaitForToons()
        else:
            self.accept('gotAllToons', self.__doneWaitForToons)

        # Put up a black screen while we're waiting.  Use our own
        # Transitions object instead of relying on the one in
        # ShowBase, which other places seem to rudely reset.
        self.transitions = Transitions.Transitions(loader)
        self.transitions.IrisModelName = "phase_3/models/misc/iris"
        self.transitions.FadeModelName = "phase_3/models/misc/fade"
        self.transitions.fadeScreen(alpha = 1)

        NametagGlobals.setMasterArrowsOn(0)
        
    def __doneWaitForToons(self):
        # All the expected toons have arrived; tell the AI so we can
        # move on.
        self.doneBarrier('WaitForToons')

    def exitWaitForToons(self):
        self.show()

        self.transitions.noFade()
        del self.transitions
        NametagGlobals.setMasterArrowsOn(1)

    ##### Elevator state #####

    def enterElevator(self):
        assert self.notify.debug('enterElevator()')

        # Place all the toons in the elevator.
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.stopLookAround()
                toon.stopSmooth()
                self.placeToonInElevator(toon)

        self.toMovieMode()

        # Position the camera behind the toons
        camera.reparentTo(self.elevatorModel)
        camera.setPosHpr(0, 30, 8, 180, 0, 0)

        base.playMusic(self.elevatorMusic, looping=1, volume=1.0)

        ival = Sequence(
            ElevatorUtils.getRideElevatorInterval(self.elevatorType),
            ElevatorUtils.getRideElevatorInterval(self.elevatorType),
            self.openDoors,
            Func(camera.wrtReparentTo, render),
            Func(self.__doneElevator),
            )

        intervalName = "ElevatorMovie"
        ival.start()
        self.storeInterval(ival, intervalName)

    def __doneElevator(self):
        self.doneBarrier('Elevator')
        
    def exitElevator(self):
        intervalName = "ElevatorMovie"
        self.clearInterval(intervalName)
        self.elevatorMusic.stop()

        # Don't release toons yet, since we're about to transfer to
        # Introduction state, and releasing the toon will cause a
        # distributed anim state update that causes a race condition
        # in the movie.
        #self.releaseToons()

        # Close the elevator doors, even though we'll open them again
        # immediately in the next state.
        ElevatorUtils.closeDoors(self.leftDoor,
                                 self.rightDoor,
                                 self.elevatorType)

    ##### Introduction state #####

    def enterIntroduction(self):
        assert self.notify.debug('enterIntroduction()')

        self.controlToons()

        # The elevator doors are open now.
        ElevatorUtils.openDoors(self.leftDoor,
                                self.rightDoor,
                                self.elevatorType)

        # Turn off the onscreen arrows while all this is going
        # on--they're distracting.
        NametagGlobals.setMasterArrowsOn(0)

        intervalName = "IntroductionMovie"
        delayDeletes = []

        seq = Sequence(self.makeIntroductionMovie(delayDeletes),
                       Func(self.__beginBattleOne),
                       name = intervalName)
        seq.delayDeletes = delayDeletes
        seq.start()
        self.storeInterval(seq, intervalName)

    def __beginBattleOne(self):
        intervalName = "IntroductionMovie"
        self.clearInterval(intervalName)
        
        self.doneBarrier('Introduction')

    def exitIntroduction(self):
        self.notify.debug("DistributedBossCog.exitIntroduction:")
        intervalName = "IntroductionMovie"
        self.clearInterval(intervalName)
        self.unstickToons()
        self.releaseToons()

        NametagGlobals.setMasterArrowsOn(1)

        # Make sure the elevator doors are closed.
        ElevatorUtils.closeDoors(self.leftDoor,
                                 self.rightDoor,
                                 self.elevatorType)

    ##### BattleOne state #####

    def enterBattleOne(self):
        assert self.notify.debug('enterBattleOne()')
        self.cleanupIntervals()

        # Get the credit multiplier
        mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(1)
        localAvatar.inventory.setBattleCreditMultiplier(mult)
        
        # The toons should be in their battle position.
        self.toonsToBattlePosition(self.toonsA, self.battleANode)
        self.toonsToBattlePosition(self.toonsB, self.battleBNode)

        # Now the battle holds the toons.
        self.releaseToons()

        base.playMusic(self.battleOneMusic, looping=1, volume=0.9)


    def exitBattleOne(self):
        self.cleanupBattles()
        self.battleOneMusic.stop()

        # No more credit multiplier
        localAvatar.inventory.setBattleCreditMultiplier(1)

    ##### BattleThree state #####

    # Added to enable all boss battles to support clicking on toon nametags.
    # This is a bit of a hack. I suppose we should inherit from FriendsListManager but
    # we really don't want the whole friends list interface...
    
    def enterBattleThree(self):
        assert self.notify.debug('enterBattleThree()')
        self.cleanupIntervals()
        self.releaseToons(finalBattle = 1)
        self.accept('clickedNametag', self.__clickedNameTag)
        self.accept('friendAvatar', self.__handleFriendAvatar)
        self.accept('avatarDetails', self.__handleAvatarDetails)
        NametagGlobals.setMasterArrowsOn(0)        
        NametagGlobals.setMasterNametagsActive(1)
                
        
    def exitBattleThree(self):
        assert self.notify.debug('exitBattleThree()')
        self.ignore('clickedNameTag')
        self.ignore('friendAvatar')
        self.ignore('avatarDetails')
        self.cleanupIntervals()

    def __clickedNameTag(self, avatar):
        self.notify.debug('__clickedNameTag')
        if not (self.state == 'BattleThree' or self.state == 'BattleFour'):
            return
        if not self.allowClickedNameTag:
            return
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):        
                FriendsListManager.FriendsListManager._FriendsListManager__handleClickedNametag(place, avatar)

    def __handleFriendAvatar(self, avId, avName, avDisableName):
        self.notify.debug('__handleFriendAvatar')
        if not (self.state == 'BattleThree' or self.state == 'BattleFour'):
            return
        if not self.allowClickedNameTag:
            return
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):        
                FriendsListManager.FriendsListManager._FriendsListManager__handleFriendAvatar(place, avId, avName, avDisableName)

    def __handleAvatarDetails(self, avId, avName, playerId = None):
        self.notify.debug('__handleAvatarDetails')
        if not (self.state == 'BattleThree' or self.state == 'BattleFour'):
            return
        if not self.allowClickedNameTag:
            return
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):        
                FriendsListManager.FriendsListManager._FriendsListManager__handleAvatarDetails(place, avId, avName, playerId)


    ##### BattleFour state #####

    # Added to enable all boss battles to support clicking on toon nametags.
    # This is a bit of a hack. I suppose we should inherit from FriendsListManager but
    # we really don't want the whole friends list interface...
    
    def enterBattleFour(self):
        assert self.notify.debug('enterBattleFour()')
        self.cleanupIntervals()
        self.releaseToons(finalBattle = 1)
        self.accept('clickedNametag', self.__clickedNameTag)
        self.accept('friendAvatar', self.__handleFriendAvatar)
        self.accept('avatarDetails', self.__handleAvatarDetails)
        NametagGlobals.setMasterArrowsOn(0)        
        NametagGlobals.setMasterNametagsActive(1)
                
        
    def exitBattleFour(self):
        assert self.notify.debug('exitBattleFour()')
        self.ignore('clickedNameTag')
        self.ignore('friendAvatar')
        self.ignore('avatarDetails')
        self.cleanupIntervals()

        
    ##### Frolic state #####

    # This state is probably only useful for debugging.  The toons are
    # all free to run around the world.

    def enterFrolic(self):
        assert self.notify.debug('enterFrolic()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()

        # Boss Cog is hanging out somewhere.
        self.reparentTo(render)
        self.stopAnimate()
        self.pose('Ff_neutral', 0)

        # No one owns the toons.
        self.releaseToons()

    def exitFrolic(self):
        pass

    #### Util methods ####

    def setToonsToNeutral(self, toonIds):
        """
        Make sure all the toons are in neutral state
        """
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                if toon.isDisguised:
                    toon.suit.loop('neutral')
                toon.loop('neutral')
 

    def wearCogSuits(self, toons, battleNode, camLoc, arrayOfObjs = False, waiter = False):
        # Returns a movie showing the line of toons losing their Cog suits.
        seq = Sequence()

        if not toons:
            # If there are no toons in the list, never mind.
            return seq

        self.notify.debug("battleNode=%s camLoc=%s" % (battleNode, camLoc))
        if camLoc:
            seq.append(Func(camera.setPosHpr, battleNode, *camLoc))

        suitsOff = Parallel()

        #build array of toon objects
        if arrayOfObjs:
            toonArray = toons
        else:
            toonArray = []
            for toonId in toons:
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    toonArray.append(toon)

        for toon in toonArray:
            dustCloud = DustCloud.DustCloud()
            dustCloud.setPos(0, 2, 3)
            dustCloud.setScale(0.5)

            # In this scene we happen to have four adjacent dust
            # clouds that overlap each other.  To prevent them
            # from clipping each other, we turn off depth write,
            # and then force the clouds to be drawn last in the
            # scene by putting them in the 'fixed' bin.  We can do
            # this because the camera is locked down and we know
            # there is nothing between the dust clouds and the
            # camera.
            dustCloud.setDepthWrite(0)
            dustCloud.setBin('fixed', 0)

            dustCloud.createTrack()
            makeWaiter = Sequence()
            if waiter:
                makeWaiter = Func(toon.makeWaiter)
            suitsOff.append(Sequence(
                Func(dustCloud.reparentTo, toon),
                Parallel(dustCloud.track,
                         Sequence(Wait(0.3),
                                  Func(self.putToonInCogSuit, toon),
                                  makeWaiter,
                                  Wait(0.7),
                                  )),
                Func(dustCloud.detachNode)))

        seq.append(suitsOff)        
        return seq
