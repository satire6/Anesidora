from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from direct.distributed.ClockDelta import *
from direct.showbase.PythonUtil import Functor
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
import DistributedBossCog
from toontown.toonbase import TTLocalizer
import SuitDNA
from toontown.toon import Toon
from toontown.battle import BattleBase
from direct.directutil import Mopath
from direct.showutil import Rope
from toontown.distributed import DelayDelete
from toontown.battle import MovieToonVictory
from toontown.building import ElevatorUtils
from toontown.battle import RewardPanel
from toontown.toon import NPCToons
from direct.task import Task
import random
import math
from toontown.coghq import CogDisguiseGlobals

# This pointer keeps track of the one DistributedSellbotBoss that
# should appear within the avatar's current visibility zones.  If
# there is more than one DistributedSellbotBoss visible to a client at
# any given time, something is wrong.
OneBossCog = None

class DistributedSellbotBoss(DistributedBossCog.DistributedBossCog, FSM.FSM):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotBoss')

    # The cage slowly drops from the ceiling to the floor as the
    # battle progresses.
    cageHeights = [100, 81, 63, 44, 25, 18]

    def __init__(self, cr):
        DistributedBossCog.DistributedBossCog.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedSellbotBoss')

        self.cagedToonNpcId = None
        self.doobers = []
        self.dooberRequest = None
        self.bossDamage = 0
        self.attackCode = None
        self.attackAvId = 0
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossDamageMovie = None
        self.cagedToon = None
        self.cageShadow = None
        self.cageIndex = 0
        self.everThrownPie = 0
        self.battleThreeMusicTime = 0
        self.insidesANodePath = None
        self.insidesBNodePath = None

        self.rampA = None
        self.rampB = None
        self.rampC = None

        self.strafeInterval = None
        self.onscreenMessage = None

        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage

    def announceGenerate(self):
        DistributedBossCog.DistributedBossCog.announceGenerate(self)
        # at this point all our attribs have been filled in.
        self.setName(TTLocalizer.SellbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {
            "name":  self.name,
            "dept":  (SuitDNA.getDeptFullname(self.style.dept)),
            }
        self.setDisplayName(nameInfo)

        self.cageDoorSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_cage_door.mp3')
        self.cageLandSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_cage_land.mp3')
        self.cageLowerSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_cage_lower.mp3')
        self.piesRestockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.mp3')
        self.rampSlideSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_ramp_slide.mp3')
        # We need a different copy of the sfx for each strafe disk.
        self.strafeSfx = []
        for i in range(10):
            self.strafeSfx.append(loader.loadSfx('phase_3.5/audio/sfx/SA_shred.mp3'))

        # Anything in the world we hit that's *not* the BossCog
        # inherits this global pieCode, so the splat will be colored
        # gray.
        render.setTag('pieCode', str(ToontownGlobals.PieCodeNotBossCog))

        # Put some polys inside the boss to detect when a pie gets
        # inside.  That will make the boss dizzy.

        insidesA = CollisionPolygon(
            Point3(4.0, -2.0, 5.0), Point3(-4.0, -2.0, 5.0),
            Point3(-4.0, -2.0, 0.5), Point3(4.0, -2.0, 0.5))
        insidesANode = CollisionNode('BossZap')
        insidesANode.addSolid(insidesA)
        insidesANode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask)
        self.insidesANodePath = self.axle.attachNewNode(insidesANode)
        self.insidesANodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossInsides))
        self.insidesANodePath.stash()

        insidesB = CollisionPolygon(
            Point3(-4.0, 2.0, 5.0), Point3(4.0, 2.0, 5.0),
            Point3(4.0, 2.0, 0.5), Point3(-4.0, 2.0, 0.5))
        insidesBNode = CollisionNode('BossZap')
        insidesBNode.addSolid(insidesB)
        insidesBNode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.WallBitmask)
        self.insidesBNodePath = self.axle.attachNewNode(insidesBNode)
        self.insidesBNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossInsides))
        self.insidesBNodePath.stash()

        # Make another bubble--a tube--to serve as a target in battle
        # three.
        target = CollisionTube(0, -1, 4, 0, -1, 9, 3.5)
        targetNode = CollisionNode('BossZap')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.targetNodePath = self.pelvis.attachNewNode(targetNode)
        self.targetNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))

        # A similar tube, offset slightly backward, forms a shield
        # from behind.  We only want to count hits from the front.
        shield = CollisionTube(0, 1, 4, 0, 1, 7, 3.5)
        shieldNode = CollisionNode('BossZap')
        shieldNode.addSolid(shield)
        shieldNode.setCollideMask(ToontownGlobals.PieBitmask | ToontownGlobals.CameraBitmask)
        shieldNodePath = self.pelvis.attachNewNode(shieldNode)

        # He also gets a disk-shaped shield around his little cog hula
        # hoop.
        disk = loader.loadModel('phase_9/models/char/bossCog-gearCollide')
        disk.find('**/+CollisionNode').setName('BossZap')
        disk.reparentTo(self.pelvis)
        disk.setZ(0.8)
        
        # The BossCog actually owns the environment geometry.  This is
        # mainly so we can move the ramps in and out under control of
        # the FSM here.
        self.loadEnvironment()

        # Set up the caged toon.
        self.__makeCagedToon()

        self.__loadMopaths()

        global OneBossCog
        if OneBossCog != None:
            self.notify.warning("Multiple BossCogs visible.")
        OneBossCog = self
        
    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        DistributedBossCog.DistributedBossCog.disable(self)
        self.request('Off')
        self.unloadEnvironment()
        self.__unloadMopaths()
        self.__cleanupCagedToon()
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        self.__cleanupStrafe()

        render.clearTag('pieCode')

        self.targetNodePath.detachNode()

        self.cr.relatedObjectMgr.abortRequest(self.dooberRequest)
        self.dooberRequest = None

        self.betweenBattleMusic.stop()
        self.promotionMusic.stop()
        self.stingMusic.stop()
        self.battleTwoMusic.stop()
        self.battleThreeMusic.stop()
        self.epilogueMusic.stop()

        global OneBossCog
        if OneBossCog == self:
            OneBossCog = None

    def d_hitBoss(self, bossDamage):
        self.sendUpdate('hitBoss', [bossDamage])

    def d_hitBossInsides(self):
        self.sendUpdate('hitBossInsides', [])

    def d_hitToon(self, toonId):
        self.sendUpdate('hitToon', [toonId])

    def setCagedToonNpcId(self, npcId):
        self.cagedToonNpcId = npcId

    def gotToon(self, toon):
        # A new Toon has arrived.  Put him in the right spot, if we
        # know what that is yet.  Normally, we will only see this
        # message in the WaitForToons state, or in the Off state if they
        # came in early (but someone might arrive to the battle very
        # late and see everything already advanced to the next state).
        stateName = self.state
        assert self.notify.debug("gotToon(%s) in state %s" % (toon.doId, stateName))
        
        if stateName == "Elevator":
            # If the toon arrives late while we're playing the
            # elevator movie, try to pop him into place.

            # Actually, this doesn't work, because we haven't yet
            # received the "setParent" and "setPos" distributed
            # messages, and we're about to.  Do something about this
            # later.
            self.placeToonInElevator(toon)

    def setDooberIds(self, dooberIds):
        self.doobers = []
        self.cr.relatedObjectMgr.abortRequest(self.dooberRequest)
        self.dooberRequest = self.cr.relatedObjectMgr.requestObjects(
            dooberIds, allCallback = self.__gotDoobers)

    def __gotDoobers(self, doobers):
        self.dooberRequest = None
        self.doobers = doobers

    def setBossDamage(self, bossDamage, recoverRate, timestamp):
        recoverStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

        taskName = "RecoverBossDamage"
        taskMgr.remove(taskName)

        if self.bossDamageMovie:
            if self.bossDamage >= self.bossMaxDamage:
                # We did it!  Finish the movie, then transition to
                # NearVictory state.
                self.bossDamageMovie.resumeUntil(self.bossDamageMovie.getDuration())
            else:
                # Push him up to the indicated point and he stops.
                self.bossDamageMovie.resumeUntil(self.bossDamage * self.bossDamageToMovie)

                if self.recoverRate:
                    taskMgr.add(self.__recoverBossDamage, taskName)
                    

    def getBossDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime

        # Although the AI side computes and transmits getBossDamage()
        # as an integer value, on the client side we return it as a
        # floating-point value, so we can get the smooth transition
        # effect as the boss slowly starts to roll back up.
        return max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0)

    def __recoverBossDamage(self, task):
        self.bossDamageMovie.setT(self.getBossDamage() * self.bossDamageToMovie)
        return Task.cont

    def __makeCagedToon(self):
        # Generates a Toon for putting in the cage during the movies,
        # that we are supposedly rescuing.
        if self.cagedToon:
            return

        self.cagedToon = NPCToons.createLocalNPC(self.cagedToonNpcId)
        self.cagedToon.addActive()

        self.cagedToon.reparentTo(self.cage)
        self.cagedToon.setPosHpr(0, -2, 0, 180, 0, 0)
        self.cagedToon.loop('neutral')

        # Also make a polygon to register when we jump up (in battle
        # three) and touch the bottom of the cage.
        
        touch = CollisionPolygon(Point3(-3.0382, 3.0382, -1),
                                 Point3(3.0382, 3.0382, -1),
                                 Point3(3.0382, -3.0382, -1),
                                 Point3(-3.0382, -3.0382, -1))
        touchNode = CollisionNode('Cage')
        touchNode.setCollideMask(ToontownGlobals.WallBitmask)
        touchNode.addSolid(touch)
        self.cage.attachNewNode(touchNode)


    def __cleanupCagedToon(self):
        if self.cagedToon:
            self.cagedToon.removeActive()
            self.cagedToon.delete()
            self.cagedToon = None

    def __walkToonToPromotion(self, toonId, delay, mopath, track, delayDeletes):
        # Generates an interval to walk the toon along the mopath
        # towards its destination (which is the toon's current pos).
        toon = base.cr.doId2do.get(toonId)
        if toon:
            destPos = toon.getPos()

            # Start the toon off at his position within the elevator.
            self.placeToonInElevator(toon)
            toon.wrtReparentTo(render)

            # We cleverly combine the MopathInterval with a
            # LerpPosInterval so that the toon walks off of his mopath
            # to his final destination, in the last few seconds of the
            # interval.  Note that the LerpPos completely replaces the
            # position computed by the Mopath once it kicks in.
            
            ival = Sequence(
                Wait(delay),
                Func(toon.suit.setPlayRate, 1, 'walk'),
                Func(toon.suit.loop, 'walk'),
                toon.posInterval(1, Point3(0, 90, 20)),
                ParallelEndTogether(MopathInterval(mopath, toon),
                                    toon.posInterval(2, destPos,
                                                     blendType = 'noBlend')),
                Func(toon.suit.loop, 'neutral'))
            track.append(ival)
            delayDeletes.append(DelayDelete.DelayDelete(toon, 'SellbotBoss.__walkToonToPromotion'))

    def __walkDoober(self, suit, delay, turnPos, track, delayDeletes):
        # Generates an interval to walk the doober around the Boss Cog
        # and out to the platform to fly away.
        turnPos = Point3(*turnPos)
        turnPosDown = Point3(*ToontownGlobals.SellbotBossDooberTurnPosDown)
        flyPos = Point3(*ToontownGlobals.SellbotBossDooberFlyPos)

        seq = Sequence(
            Func(suit.headsUp, turnPos),
            Wait(delay),
            Func(suit.loop, 'walk', 0),
            self.__walkSuitToPoint(suit, suit.getPos(), turnPos),
            self.__walkSuitToPoint(suit, turnPos, turnPosDown),            
            self.__walkSuitToPoint(suit, turnPosDown, flyPos),
            suit.beginSupaFlyMove(flyPos, 0, 'flyAway'),
            Func(suit.fsm.request, 'Off'),
            )
        track.append(seq)
        delayDeletes.append(DelayDelete.DelayDelete(suit, 'SellbotBoss.__walkDoober'))
        

    def __walkSuitToPoint(self, node, fromPos, toPos):
        vector = Vec3(toPos - fromPos)
        distance = vector.length()

        # These suits walk a little faster than most.  (They're
        # still young.)
        time = distance / (ToontownGlobals.SuitWalkSpeed * 1.8)
        
        return Sequence(Func(node.setPos, fromPos),
                        Func(node.headsUp, toPos),
                        node.posInterval(time, toPos))

    def makeIntroductionMovie(self, delayDeletes):

        # Generate an interval which shows the toons emerging from the
        # elevator, walking down to face the Boss Cog, who is
        # currently busy promoting a group of new Cogs and sending
        # them on their way.  The Boss Cog then begins to promote the
        # Toons, but then discovers the dupe and engages them in
        # battle instead.
        
        track = Parallel()

        # camTrack animates the camera for the first part of the
        # sequence.
        
        # First, the camera will start off aiming at the elevators, so
        # we'll see the toons emerge and start to split off.  Then
        # we'll pull back to look at the room and watch the Boss Cog
        # promote the previous Cogs, while our Toons walk around the
        # perimeter.

        # After that, the camera will be animated by the dialogTrack in
        # cuts synchronized with the boss's dialog.

        camera.reparentTo(render)
        camera.setPosHpr(0, 25, 30, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        # dooberTrack includes the doobers walking down the platform
        # and flying away.  Rather than adding it directly into the
        # movie, we call it with an IndirectInterval, so we can jump
        # around in time.
        
        dooberTrack = Parallel()
        if self.doobers:
            # Start the doobers out around the boss.
            self.__doobersToPromotionPosition(self.doobers[:4], self.battleANode)
            self.__doobersToPromotionPosition(self.doobers[4:], self.battleBNode)

            turnPosA = ToontownGlobals.SellbotBossDooberTurnPosA
            turnPosB = ToontownGlobals.SellbotBossDooberTurnPosB
            self.__walkDoober(self.doobers[0], 0, turnPosA,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[1], 4, turnPosA,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[2], 8, turnPosA,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[3], 12, turnPosA,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[7], 2, turnPosB,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[6], 6, turnPosB,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[5], 10, turnPosB,
                              dooberTrack, delayDeletes)
            self.__walkDoober(self.doobers[4], 14, turnPosB,
                              dooberTrack, delayDeletes)

        # toonTrack shows the toons walking out of the elevator and
        # down to face the Boss Cog.  As above, this is played with an
        # IndirectInterval.

        toonTrack = Parallel()

        # Temporarily put the toons in their final position for the
        # movie, just so we can see what it is and lerp them there.
        self.__toonsToPromotionPosition(self.toonsA, self.battleANode)
        self.__toonsToPromotionPosition(self.toonsB, self.battleBNode)

        delay = 0
        for toonId in self.toonsA:
            self.__walkToonToPromotion(toonId, delay, self.toonsEnterA,
                                       toonTrack, delayDeletes)
            delay += 1

        for toonId in self.toonsB:
            self.__walkToonToPromotion(toonId, delay, self.toonsEnterB,
                                       toonTrack, delayDeletes)
            delay += 1

        # And the elevator doors close behind the last toon.
        toonTrack.append(Sequence(Wait(delay), self.closeDoors))

        self.rampA.request('extended')
        self.rampB.request('extended')
        self.rampC.request('retracted')
        self.clearChat()
        self.cagedToon.clearChat()

        # bossTrack shows the Boss's dialog and animations, and the
        # later camera cuts.
        
        promoteDoobers = TTLocalizer.BossCogPromoteDoobers % (
            SuitDNA.getDeptFullnameP(self.style.dept))
        doobersAway = TTLocalizer.BossCogDoobersAway[self.style.dept]
        welcomeToons = TTLocalizer.BossCogWelcomeToons
        promoteToons = TTLocalizer.BossCogPromoteToons % (
            SuitDNA.getDeptFullnameP(self.style.dept))
        discoverToons = TTLocalizer.BossCogDiscoverToons
        attackToons = TTLocalizer.BossCogAttackToons
        interruptBoss = TTLocalizer.CagedToonInterruptBoss
        rescueQuery = TTLocalizer.CagedToonRescueQuery

        bossAnimTrack = Sequence(
            ActorInterval(self, 'Ff_speech', startTime = 2, duration = 10, loop = 1),
            # 10
            ActorInterval(self, 'ltTurn2Wave', duration = 2),
            # 12
            ActorInterval(self, 'wave', duration = 4, loop = 1),
            # 16
            ActorInterval(self, 'ltTurn2Wave', startTime = 2, endTime = 0),
            # 18
            ActorInterval(self, 'Ff_speech', duration = 7, loop = 1),
            # 25

            # remaining animations mixed in with camera cuts in
            # dialogTrack.
            )
        track.append(bossAnimTrack)
        
        dialogTrack = Track(
            (0, Parallel(camera.posHprInterval(8, Point3(-22, -100, 35),
                                               Point3(-10, -13, 0),
                                               blendType = 'easeInOut'),
                         IndirectInterval(toonTrack, 0, 18))),
            (5.6, Func(self.setChatAbsolute, promoteDoobers, CFSpeech)),
            (9, IndirectInterval(dooberTrack, 0, 9)),

            # Cut to over-the-shoulder shot of Boss Cog waving goodbye
            # to doobers.
            (10, Sequence(Func(self.clearChat),
                          Func(camera.setPosHpr, -23.1, 15.7, 17.2, -160, -2.4, 0))),
            (12, Func(self.setChatAbsolute, doobersAway, CFSpeech)),

            # Cut to wide shot of Boss Cog and Toons and caged toon in
            # background.
            (16, Parallel(Func(self.clearChat),
                          Func(camera.setPosHpr, -25, -99, 10, -14, 10, 0),
                          IndirectInterval(dooberTrack, 14),
                          IndirectInterval(toonTrack, 30))),
            (18, Func(self.setChatAbsolute, welcomeToons, CFSpeech)),
                          
            (22, Func(self.setChatAbsolute, promoteToons, CFSpeech)),
            (22.2, Sequence(Func(self.cagedToon.nametag3d.setScale, 2),
                            Func(self.cagedToon.setChatAbsolute, interruptBoss, CFSpeech),
                            ActorInterval(self.cagedToon, 'wave'),
                            Func(self.cagedToon.loop, 'neutral'))),

            # Cut to head-and-shoulders shot of Boss Cog looking up at
            # source of interruption.
            (25, Sequence(Func(self.clearChat),
                          Func(self.cagedToon.clearChat),
                          Func(camera.setPosHpr, -12, -15, 27, -151, -15, 0),
                          ActorInterval(self, 'Ff_lookRt'),
                          )),

            # Cut to closeup of caged toon.
            (27, Sequence(Func(self.cagedToon.setChatAbsolute, rescueQuery, CFSpeech),
                          Func(camera.setPosHpr, -12, 48, 94, -26, 20, 0),
                          ActorInterval(self.cagedToon, 'wave'),
                          Func(self.cagedToon.loop, 'neutral'))),

            # Cut to shot of Boss Cog looking back at Toons from
            # Toons' eye view.
            (31, Sequence(Func(camera.setPosHpr, -20, -35, 10, -88, 25, 0),
                          Func(self.setChatAbsolute, discoverToons, CFSpeech),
                          Func(self.cagedToon.nametag3d.setScale, 1),
                          Func(self.cagedToon.clearChat),
                          ActorInterval(self, 'turn2Fb'),
                          )),

            # Cut to toons losing their cog suits.
            (34, Sequence(Func(self.clearChat),
                          self.loseCogSuits(self.toonsA, self.battleANode, (0,18,5,-180,0,0)),
                          self.loseCogSuits(self.toonsB, self.battleBNode, (0,18,5,-180,0,0)))),

            # Cut to wide shot of battle arena.  Toons back up and
            # ramps retract.
            (37, Sequence(self.toonNormalEyes(self.involvedToons),
                          Func(camera.setPosHpr, -23.4, -145.6, 44.0, -10.0, -12.5, 0),
                          Func(self.loop, 'Fb_neutral'),
                          Func(self.rampA.request, 'retract'),
                          Func(self.rampB.request, 'retract'),
                          Parallel(self.backupToonsToBattlePosition(self.toonsA, self.battleANode),
                                   self.backupToonsToBattlePosition(self.toonsB, self.battleBNode),
                                   Sequence(Wait(2),
                                            Func(self.setChatAbsolute, attackToons, CFSpeech))),
                          )),
            )
        track.append(dialogTrack)

        return Sequence(Func(self.stickToonsToFloor),
                        track,
                        Func(self.unstickToons),
                        name = self.uniqueName('Introduction'))

    def __makeRollToBattleTwoMovie(self):
        # Generate an interval which shows the Boss Cog rolling to the
        # battle 2 position.

        startPos = Point3(ToontownGlobals.SellbotBossBattleOnePosHpr[0],
                          ToontownGlobals.SellbotBossBattleOnePosHpr[1],
                          ToontownGlobals.SellbotBossBattleOnePosHpr[2])
        if self.arenaSide:
            topRampPos = Point3(*ToontownGlobals.SellbotBossTopRampPosB)
            topRampTurnPos = Point3(*ToontownGlobals.SellbotBossTopRampTurnPosB)
            p3Pos = Point3(*ToontownGlobals.SellbotBossP3PosB)
        else:
            topRampPos = Point3(*ToontownGlobals.SellbotBossTopRampPosA)
            topRampTurnPos = Point3(*ToontownGlobals.SellbotBossTopRampTurnPosA)
            p3Pos = Point3(*ToontownGlobals.SellbotBossP3PosA)
            
        battlePos = Point3(ToontownGlobals.SellbotBossBattleTwoPosHpr[0],
                           ToontownGlobals.SellbotBossBattleTwoPosHpr[1],
                           ToontownGlobals.SellbotBossBattleTwoPosHpr[2])
        battleHpr = VBase3(ToontownGlobals.SellbotBossBattleTwoPosHpr[3],
                           ToontownGlobals.SellbotBossBattleTwoPosHpr[4],
                           ToontownGlobals.SellbotBossBattleTwoPosHpr[5])
        bossTrack = Sequence()

        # Turn the boss model around so he rolls forward.
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.loop, 'Fb_neutral'))

        track, hpr = self.rollBossToPoint(startPos, None, topRampPos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(topRampPos, hpr, topRampTurnPos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(topRampTurnPos, hpr, p3Pos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(p3Pos, hpr, battlePos, None, 0)
        bossTrack.append(track)

        return Sequence(
            bossTrack,
            Func(self.getGeomNode().setH, 0),
            name = self.uniqueName('BattleTwo'))

    def makeEndOfBattleMovie(self, hasLocalToon):
        assert self.notify.debug("makeEndOfBattleMovie(%s)" % (hasLocalToon))
        # Generate an interval which shows the cage dropping a bit
        # further.  This one is called from DistributedBattleFinal.
        name = self.uniqueName('CageDrop')
        seq = Sequence(name = name)

        seq.append(Func(self.cage.setPos, self.cagePos[self.cageIndex]))

        if hasLocalToon:
            seq += [Func(camera.reparentTo, render),
                    Func(camera.setPosHpr, self.cage, 0, -50, 0, 0, 0, 0),
                    Func(localAvatar.setCameraFov, ToontownGlobals.CogHQCameraFov),
                    Func(self.hide)]
        seq += [Wait(0.5),
                Parallel(self.cage.posInterval(1, self.cagePos[self.cageIndex + 1],
                                               blendType = 'easeInOut'),
                         SoundInterval(self.cageLowerSfx, duration = 1)),
                Func(self.cagedToon.nametag3d.setScale, 2),
                Func(self.cagedToon.setChatAbsolute,
                     TTLocalizer.CagedToonDrop[self.cageIndex], CFSpeech),
                Wait(3),
                Func(self.cagedToon.nametag3d.setScale, 1),
                Func(self.cagedToon.clearChat)]
        if hasLocalToon:
            seq += [Func(self.show),
                    Func(camera.reparentTo, localAvatar),
                    Func(camera.setPos, localAvatar.cameraPositions[0][0]),
                    Func(camera.setHpr, 0, 0, 0)]

        self.cageIndex += 1
        return seq
    
    def __makeBossDamageMovie(self):
        # Generate an interval which shows the Boss Cog rolling down
        # in retreat as the Toons attack.

        startPos = Point3(ToontownGlobals.SellbotBossBattleTwoPosHpr[0],
                          ToontownGlobals.SellbotBossBattleTwoPosHpr[1],
                          ToontownGlobals.SellbotBossBattleTwoPosHpr[2])
        startHpr = Point3(*ToontownGlobals.SellbotBossBattleThreeHpr)
        bottomPos = Point3(*ToontownGlobals.SellbotBossBottomPos)
        deathPos = Point3(*ToontownGlobals.SellbotBossDeathPos)

        self.setPosHpr(startPos, startHpr)

        bossTrack = Sequence()
        bossTrack.append(Func(self.loop, 'Fb_neutral'))
        track, hpr = self.rollBossToPoint(startPos, startHpr, bottomPos, None, 1)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(bottomPos, startHpr, deathPos, None, 1)
        bossTrack.append(track)

        duration = bossTrack.getDuration()
        return bossTrack

    def __talkAboutPromotion(self, speech):
        # Extends the congratulations speech to talk about the earned
        # promotion, if any.  Returns the newly-extended speech.
        
        # don't say anything about a promotion if they've maxed their cog suit
        if self.prevCogSuitLevel < ToontownGlobals.MaxCogSuitLevel:
            speech += TTLocalizer.CagedToonPromotion
            newCogSuitLevel = localAvatar.getCogLevels()[
                CogDisguiseGlobals.dept2deptIndex(self.style.dept)]
            # if this is their last promotion, tell them
            if newCogSuitLevel == ToontownGlobals.MaxCogSuitLevel:
                speech += TTLocalizer.CagedToonLastPromotion % (ToontownGlobals.MaxCogSuitLevel+1)
            # if they're getting another LP, tell them
            if newCogSuitLevel in ToontownGlobals.CogSuitHPLevels:
                speech += TTLocalizer.CagedToonHPBoost
        else:
            # level XX, wow! Thanks for coming back!
            speech += TTLocalizer.CagedToonMaxed % (ToontownGlobals.MaxCogSuitLevel+1)

        return speech

    def __makeCageOpenMovie(self):
        # Generate an interval which shows the cage dropping all the
        # way to the ground and opening, to free the trapped toon who
        # bestows upon us a favor.

        # put together what the toon is going to say ahead of time,
        # since setLocalPageChat does not queue up messages
        speech = TTLocalizer.CagedToonThankYou
        speech = self.__talkAboutPromotion(speech)

        name = self.uniqueName('CageOpen')
        seq = Sequence(
            Func(self.cage.setPos, self.cagePos[4]),
            Func(self.cageDoor.setHpr, VBase3(0, 0, 0)),
            Func(self.cagedToon.setPos, Point3(0, -2, 0)),
            Parallel(self.cage.posInterval(0.5, self.cagePos[5],
                                           blendType = 'easeOut'),
                     SoundInterval(self.cageLowerSfx, duration = 0.5)),
            Parallel(self.cageDoor.hprInterval(0.5, VBase3(0, 90, 0),
                                               blendType = 'easeOut'),
                     Sequence(SoundInterval(self.cageDoorSfx), duration = 0)),
            Wait(0.2),
            Func(self.cagedToon.loop, 'walk'),
            self.cagedToon.posInterval(0.8, Point3(0, -6, 0)),
            Func(self.cagedToon.setChatAbsolute,
                 TTLocalizer.CagedToonYippee, CFSpeech),
            ActorInterval(self.cagedToon, 'jump'),
            Func(self.cagedToon.loop, 'neutral'),
            Func(self.cagedToon.headsUp, localAvatar),
            Func(self.cagedToon.setLocalPageChat, speech, 0),
            Func(camera.reparentTo, localAvatar),
            Func(camera.setPos, 0, -9, 9),
            Func(camera.lookAt, self.cagedToon, Point3(0, 0, 2)),
            name = name)

        return seq

    def __showOnscreenMessage(self, text):
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None
            
        self.onscreenMessage = DirectLabel(
            text = text,
            text_fg = VBase4(1,1,1,1),
            text_align = TextNode.ACenter,
            relief = None,
            pos = (0, 0, 0.35),
            scale = 0.1)

    def __clearOnscreenMessage(self):
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None

    def __showWaitingMessage(self, task):
        self.__showOnscreenMessage(TTLocalizer.BuildingWaitingForVictors)

    def __placeCageShadow(self):
        if self.cageShadow == None:
            self.cageShadow = loader.loadModel('phase_3/models/props/drop_shadow')
            self.cageShadow.setPos(0, 77.9, 18)
            self.cageShadow.setColorScale(1, 1, 1, 0.6)
        self.cageShadow.reparentTo(render)

    def __removeCageShadow(self):
        if self.cageShadow != None:
            self.cageShadow.detachNode()

    def setCageIndex(self, cageIndex):
        # Sets the cage to the appropriate height for the given index.
        self.cageIndex = cageIndex
        self.cage.setPos(self.cagePos[self.cageIndex])
        if self.cageIndex >= 4:
            self.__placeCageShadow()
        else:
            self.__removeCageShadow()
            

    ##### Environment #####

    def loadEnvironment(self):
        DistributedBossCog.DistributedBossCog.loadEnvironment(self)
        
        self.geom = loader.loadModel('phase_9/models/cogHQ/BossRoomHQ')
        self.rampA = self.__findRamp('rampA', '**/west_ramp2')
        self.rampB = self.__findRamp('rampB', '**/west_ramp')
        self.rampC = self.__findRamp('rampC', '**/west_ramp1')
        self.cage = self.geom.find('**/cage')

        elevatorEntrance = self.geom.find('**/elevatorEntrance')
        # The elevatorEntrance has some geometry that it shouldn't.
        elevatorEntrance.getChildren().detach()
        elevatorEntrance.setScale(1)

        elevatorModel = loader.loadModel("phase_9/models/cogHQ/cogHQ_elevator")
        elevatorModel.reparentTo(elevatorEntrance)

        self.setupElevator(elevatorModel)

        pos = self.cage.getPos()
        self.cagePos = []
        for height in self.cageHeights:
            self.cagePos.append(Point3(pos[0], pos[1], height))

        self.cageDoor = self.geom.find('**/cage_door')

        # Make the cage be scale 1.0, to fit the Toon inside better.
        self.cage.setScale(1)

        # Draw a chain from the top of the cage support to the bottom
        # of the I-beam.
        self.rope = Rope.Rope(name = 'supportChain')
        self.rope.reparentTo(self.cage)
        self.rope.setup(2, ((self.cage, (0.15, 0.13, 16)),
                            (self.geom, (0.23, 78, 120))))
        self.rope.ropeNode.setRenderMode(RopeNode.RMBillboard)
        self.rope.ropeNode.setUvMode(RopeNode.UVDistance)
        self.rope.ropeNode.setUvDirection(0)

        self.rope.ropeNode.setUvScale(0.8)
        self.rope.setTexture(self.cage.findTexture('hq_chain'))
        self.rope.setTransparency(1)

        # before battles: play the boss theme music
        self.promotionMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
            # 'phase_9/audio/bgm/encntr_head_suit_theme.mid')
        # Between battle one and two: play the upbeat street battle music
        self.betweenBattleMusic = base.loadMusic(
            'phase_9/audio/bgm/encntr_toon_winning.mid')
        # Battle two: play the top-of-the-building battle music
        self.battleTwoMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
        
        self.geom.reparentTo(render)
        

    def unloadEnvironment(self):
        DistributedBossCog.DistributedBossCog.unloadEnvironment(self)

        self.geom.removeNode()
        del self.geom
        del self.cage

        self.rampA.requestFinalState()
        self.rampB.requestFinalState()
        self.rampC.requestFinalState()
        del self.rampA
        del self.rampB
        del self.rampC

    def __loadMopaths(self):
        self.toonsEnterA = Mopath.Mopath()
        self.toonsEnterA.loadFile('phase_9/paths/bossBattle-toonsEnterA')
        self.toonsEnterA.fFaceForward = 1
        self.toonsEnterA.timeScale = 35
        self.toonsEnterB = Mopath.Mopath()
        self.toonsEnterB.loadFile('phase_9/paths/bossBattle-toonsEnterB')
        self.toonsEnterB.fFaceForward = 1
        self.toonsEnterB.timeScale = 35

    def __unloadMopaths(self):
        self.toonsEnterA.reset()
        self.toonsEnterB.reset()

    def __findRamp(self, name, path):
        # Find the ramp in the geom and sets it up for animation.
        ramp = self.geom.find(path)

        # The transform on the ramp node represents the coordinate
        # system in which the ramp can move.  That means we need to
        # animate a child of the ramp node itself in order to remain
        # within this coordinate system.  Since there are multiple
        # children (visible polygons as well as collision nodes), we
        # create our own node for this purpose.
        children = ramp.getChildren()
        animate = ramp.attachNewNode(name)
        children.reparentTo(animate)

        # Now we create a tiny ClassicFSM to manage the ramp's state.
        fsm = ClassicFSM.ClassicFSM(name,
                      [State.State('extend',
                                   Functor(self.enterRampExtend, animate),
                                   Functor(self.exitRampExtend, animate),
                                   ['extended', 'retract', 'retracted']),
                       State.State('extended',
                                   Functor(self.enterRampExtended, animate),
                                   Functor(self.exitRampExtended, animate),
                                   ['retract', 'retracted']),
                       State.State('retract',
                                   Functor(self.enterRampRetract, animate),
                                   Functor(self.exitRampRetract, animate),
                                   ['extend', 'extended', 'retracted']),
                       State.State('retracted',
                                   Functor(self.enterRampRetracted, animate),
                                   Functor(self.exitRampRetracted, animate),
                                   ['extend', 'extended']),
                       State.State('off',
                                   Functor(self.enterRampOff, animate),
                                   Functor(self.exitRampOff, animate)),
                       ],
                      # Initial state
                      'off',
                      # Final state
                      'off',
                      onUndefTransition = ClassicFSM.ClassicFSM.DISALLOW)
        fsm.enterInitialState()

        return fsm

    ##### Ramp states #####

    def enterRampExtend(self, animate):
        intervalName = self.uniqueName('extend-%s' % (animate.getName()))
        adjustTime = 2.0 * (animate.getX()) / 18.0
        ival = Parallel(
            SoundInterval(self.rampSlideSfx, node = animate),
            animate.posInterval(adjustTime, Point3(0, 0, 0),
                                blendType = 'easeInOut',
                                name = intervalName),
            )
        ival.start()
        self.storeInterval(ival, intervalName)

    def exitRampExtend(self, animate):
        intervalName = self.uniqueName('extend-%s' % (animate.getName()))
        self.clearInterval(intervalName)

    def enterRampExtended(self, animate):
        animate.setPos(0, 0, 0)

    def exitRampExtended(self, animate):
        pass

    def enterRampRetract(self, animate):
        intervalName = self.uniqueName('retract-%s' % (animate.getName()))
        adjustTime = 2.0 * (18 - animate.getX()) / 18.0
        ival = Parallel(
            SoundInterval(self.rampSlideSfx, node = animate),
            animate.posInterval(adjustTime, Point3(18, 0, 0),
                                blendType = 'easeInOut',
                                name = intervalName),
            )
        ival.start()
        self.storeInterval(ival, intervalName)

    def exitRampRetract(self, animate):
        intervalName = self.uniqueName('retract-%s' % (animate.getName()))
        self.clearInterval(intervalName)

    def enterRampRetracted(self, animate):
        animate.setPos(18, 0, 0)

    def exitRampRetracted(self, animate):
        pass

    def enterRampOff(self, animate):
        pass

    def exitRampOff(self, animate):
        pass


    ##### Off state #####

    def enterOff(self):
        DistributedBossCog.DistributedBossCog.enterOff(self)

        if self.cagedToon:
            self.cagedToon.clearChat()

        if self.rampA:
            self.rampA.request('off')
        if self.rampB:
            self.rampB.request('off')
        if self.rampC:
            self.rampC.request('off')

    ##### WaitForToons state #####

    def enterWaitForToons(self):
        DistributedBossCog.DistributedBossCog.enterWaitForToons(self)

        self.geom.hide()

        # Disable the caged toon's nametag while we're here in space
        # waiting.
        self.cagedToon.removeActive()

    def exitWaitForToons(self):
        DistributedBossCog.DistributedBossCog.exitWaitForToons(self)

        self.geom.show()
        self.cagedToon.addActive()


    ##### Elevator state #####

    def enterElevator(self):
        DistributedBossCog.DistributedBossCog.enterElevator(self)

        # Make sure the side ramps are extended and the back ramp is
        # retracted.
        self.rampA.request('extended')
        self.rampB.request('extended')
        self.rampC.request('retracted')

        # And the cage is up in the original position.
        self.setCageIndex(0)
        
        # Set the boss up in the middle of the floor, so we can see
        # him when the doors open.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleOnePosHpr)

        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        # Disable the caged toon's nametag while we're in the
        # elevator.
        self.cagedToon.removeActive()
        
    def exitElevator(self):
        DistributedBossCog.DistributedBossCog.exitElevator(self)

        self.cagedToon.addActive()

    ##### Introduction state #####

    def enterIntroduction(self):
        # Set the boss up in the middle of the floor, actively
        # promoting some doobers.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleOnePosHpr)
        self.stopAnimate()

        DistributedBossCog.DistributedBossCog.enterIntroduction(self)

        # Make sure the side ramps are extended and the back ramp is
        # retracted.
        self.rampA.request('extended')
        self.rampB.request('extended')
        self.rampC.request('retracted')

        # And the cage is up in the original position.
        self.setCageIndex(0)

        base.playMusic(self.promotionMusic, looping=1, volume=0.9)
        
    def exitIntroduction(self):
        DistributedBossCog.DistributedBossCog.exitIntroduction(self)

        self.promotionMusic.stop()

    ##### BattleOne state #####

    def enterBattleOne(self):
        DistributedBossCog.DistributedBossCog.enterBattleOne(self)

        # Boss Cog is still in the middle of the floor.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleOnePosHpr)
        self.clearChat()
        self.cagedToon.clearChat()

        # Make sure the ramps are retracted (or on their way there).
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('retract')

        if self.battleA == None or self.battleB == None:
            cageIndex = 1
        else:
            cageIndex = 0
        self.setCageIndex(cageIndex)

    def exitBattleOne(self):
        DistributedBossCog.DistributedBossCog.exitBattleOne(self)

    ##### RollToBattleTwo state #####

    def enterRollToBattleTwo(self):
        assert self.notify.debug('enterRollToBattleTwo()')
        # Disable collision on the toon, there is a collision issue where the boss was 
        # hitting the toons right after the first battle, so we turn off their collision briefly
        # until this issue can be addressed in Panda.
        self.disableToonCollision()
        self.releaseToons()

        # Retract most of the ramps.
        if self.arenaSide:
            self.rampA.request('retract')
            self.rampB.request('extend')
        else:
            self.rampA.request('extend')
            self.rampB.request('retract')
        self.rampC.request('retract')

        self.reparentTo(render)

        # By now, the cage has dropped somewhat.
        self.setCageIndex(2)
        
        # The Boss Cog rolls up the ramp into position for battle two,
        # while the Toons are free to run around for a few seconds.
        self.stickBossToFloor()

        # Now generate the interval that plays the movie.
        intervalName = "RollToBattleTwo"
        seq = Sequence(self.__makeRollToBattleTwoMovie(),
                       Func(self.__onToPrepareBattleTwo),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        base.playMusic(self.betweenBattleMusic, looping=1, volume=0.9)
        #re-enable the collision a little bit later, after the boss has started moving
        taskMgr.doMethodLater(0.5, self.enableToonCollision, 'enableToonCollision')

    def __onToPrepareBattleTwo(self):
        # Make sure the boss ends up in his battle position.
        self.unstickBoss()
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleTwoPosHpr)
        self.doneBarrier('RollToBattleTwo')

    def exitRollToBattleTwo(self):
        self.unstickBoss()
        intervalName = "RollToBattleTwo"
        self.clearInterval(intervalName)

        self.betweenBattleMusic.stop()
        
    def disableToonCollision(self):
        base.localAvatar.collisionsOff()
            
    def enableToonCollision(self, task):
        base.localAvatar.collisionsOn()
            
    ##### PrepareBattleTwo state #####

    def enterPrepareBattleTwo(self):
        assert self.notify.debug('enterPrepareBattleTwo()')
        self.cleanupIntervals()

        self.controlToons()

        self.clearChat()
        self.cagedToon.clearChat()
        self.reparentTo(render)

        # Retract most of the ramps.
        if self.arenaSide:
            self.rampA.request('retract')
            self.rampB.request('extend')
        else:
            self.rampA.request('extend')
            self.rampB.request('retract')
        self.rampC.request('retract')

        self.reparentTo(render)

        # By now, the cage has dropped somewhat.
        self.setCageIndex(2)

        # In this state, we just show a closeup of the cagedToon.
        camera.reparentTo(render)
        camera.setPosHpr(self.cage, 0, -17, 3.3, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov),

        # And the boss cog is actually hidden, because the camera is
        # positioned inside him.
        self.hide()
        
        # We see the caged toon give us some congratulations and
        # advice for defeating the boss cog; we have to click through
        # this advice to move on.
        self.acceptOnce("doneChatPage", self.__onToBattleTwo)
        self.cagedToon.setLocalPageChat(TTLocalizer.CagedToonPrepareBattleTwo, 1)

        # Let's play the elevator music again; it's dramatic enough to
        # use twice.
        base.playMusic(self.stingMusic, looping=0, volume=1.0)

    def __onToBattleTwo(self, elapsed):
        self.doneBarrier('PrepareBattleTwo')

        # Wait a second.  If we don't move on immediately, pop up the
        # "waiting for other players" message.
        taskMgr.doMethodLater(1, self.__showWaitingMessage,
                              self.uniqueName("WaitingMessage"))

    def exitPrepareBattleTwo(self):
        self.show()
        taskMgr.remove(self.uniqueName("WaitingMessage"))
        self.ignore("doneChatPage")
        self.__clearOnscreenMessage()
        self.stingMusic.stop()
        
    ##### BattleTwo state #####

    def enterBattleTwo(self):
        assert self.notify.debug('enterBattleTwo()')
        self.cleanupIntervals()

        # Get the credit multiplier
        mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(2)
        localAvatar.inventory.setBattleCreditMultiplier(mult)

        # Boss Cog is now on top of the ramp.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleTwoPosHpr)

        # Clear the chat dialogs left over from the transition movie.
        self.clearChat()
        self.cagedToon.clearChat()

        # Make sure the ramps are retracted (or on their way there).
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('retract')

        # Now the battle holds the toons.
        self.releaseToons()
        
        # Position the toons to the battle.
        self.toonsToBattlePosition(self.toonsA, self.battleANode)
        self.toonsToBattlePosition(self.toonsB, self.battleBNode)

        if self.battleA == None or self.battleB == None:
            cageIndex = 3
        else:
            cageIndex = 2
        self.setCageIndex(cageIndex)
        base.playMusic(self.battleTwoMusic, looping=1, volume=0.9)


    def exitBattleTwo(self):
        intervalName = self.uniqueName('cageDrop')
        self.clearInterval(intervalName)
        self.cleanupBattles()
        self.battleTwoMusic.stop()

        # No more credit multiplier
        localAvatar.inventory.setBattleCreditMultiplier(1)

    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        assert self.notify.debug('enterPrepareBattleThree()')
        self.cleanupIntervals()

        self.controlToons()

        self.clearChat()
        self.cagedToon.clearChat()
        self.reparentTo(render)

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        self.setCageIndex(4)

        # In this state, we just show a closeup of the cagedToon.
        camera.reparentTo(render)
        camera.setPosHpr(self.cage, 0, -17, 3.3, 0, 0, 0)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov),

        # And the boss cog is actually hidden, because the camera is
        # positioned inside him.
        self.hide()
        
        # We see the caged toon give us some congratulations and
        # advice for defeating the boss cog; we have to click through
        # this advice to move on.
        self.acceptOnce("doneChatPage", self.__onToBattleThree)
        self.cagedToon.setLocalPageChat(TTLocalizer.CagedToonPrepareBattleThree, 1)
        base.playMusic(self.betweenBattleMusic, looping=1, volume=0.9)

    def __onToBattleThree(self, elapsed):
        self.doneBarrier('PrepareBattleThree')

        # Wait a second.  If we don't move on immediately, pop up the
        # "waiting for other players" message.
        taskMgr.doMethodLater(1, self.__showWaitingMessage,
                              self.uniqueName("WaitingMessage"))

    def exitPrepareBattleThree(self):
        self.show()
        taskMgr.remove(self.uniqueName("WaitingMessage"))
        self.ignore("doneChatPage")
        intervalName = "PrepareBattleThree"
        self.clearInterval(intervalName)
        self.__clearOnscreenMessage()
        self.betweenBattleMusic.stop()

    ##### BattleThree state #####

    def enterBattleThree(self):
        assert self.notify.debug('enterBattleThree()')
        DistributedBossCog.DistributedBossCog.enterBattleThree(self)

        self.clearChat()
        self.cagedToon.clearChat()
        self.reparentTo(render)

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        self.setCageIndex(4)

        self.happy = 0
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        # Now we're in pie mode.
        self.accept('enterCage', self.__touchedCage)
        self.accept('pieSplat', self.__pieSplat)
        self.accept('localPieSplat', self.__localPieSplat)
        self.accept('outOfPies', self.__outOfPies)
        self.accept('begin-pie', self.__foundPieButton)

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        # In case they don't figure it out, hit them over the head
        # with it after a few seconds.
        taskMgr.doMethodLater(30, self.__howToGetPies,
                              self.uniqueName("PieAdvice"))

        # Now, the Boss mainly sits there and taunts us, and
        # occasionally attacks us.  But when we hit him, he rolls a
        # little bit farther down the launching area.  We implement
        # this by playing a little bit more of the bossDamageMovie
        # with each hit.
        self.stickBossToFloor()

        self.bossDamageMovie = self.__makeBossDamageMovie()
        bossDoneEventName = self.uniqueName('DestroyedBoss')
        self.bossDamageMovie.setDoneEvent(bossDoneEventName)
        self.acceptOnce(bossDoneEventName, self.__doneBattleThree)
        
        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage
        
        # This factor scales the "max damage" point to the point in
        # the movie where the Boss falls over the edge.
        self.bossDamageToMovie = self.bossDamageMovie.getDuration() / self.bossMaxDamage

        # Leave the boss movie paused at the current damage level.
        self.bossDamageMovie.setT(self.bossDamage * self.bossDamageToMovie)

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9)

    def __doneBattleThree(self):
        # We've played the boss damage movie all the way to
        # completion; it's time to transition to the NearVictory state.
        self.setState('NearVictory')
        self.unstickBoss()

    def exitBattleThree(self):
        DistributedBossCog.DistributedBossCog.exitBattleThree(self)
        bossDoneEventName = self.uniqueName('DestroyedBoss')
        self.ignore(bossDoneEventName)
        # Actually, we'll keep the animation going, so we can continue
        # it in the NearVictory state.
        #self.stopAnimate()

        taskMgr.remove(self.uniqueName('StandUp'))

        # No more pies.
        self.ignore('enterCage')
        self.ignore('pieSplat')
        self.ignore('localPieSplat')
        self.ignore('outOfPies')
        self.ignore('begin-pie')
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.__removeCageShadow()

        self.bossDamageMovie.finish()
        self.bossDamageMovie = None
        self.unstickBoss()

        taskName = "RecoverBossDamage"
        taskMgr.remove(taskName)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()


    ##### NearVictory state #####

    def enterNearVictory(self):
        assert self.notify.debug('enterNearVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        # Boss Cog is on the edge of the precipice, waiting for that
        # one final pie toss.
        self.reparentTo(render)
        self.setPos(*ToontownGlobals.SellbotBossDeathPos)
        self.setHpr(*ToontownGlobals.SellbotBossBattleThreeHpr)
        self.clearChat()
        self.cagedToon.clearChat()

        self.setCageIndex(4)

        # No one owns the toons.
        self.releaseToons(finalBattle = 1)

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        # We're still in pie mode, for the one more ceremonial toss
        # that sends the boss plummeting to his death.
        self.accept('enterCage', self.__touchedCage)
        self.accept('pieSplat', self.__finalPieSplat)
        self.accept('localPieSplat', self.__localPieSplat)
        self.accept('outOfPies', self.__outOfPies)

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)
        
        self.happy = 0
        self.raised = 0
        self.forward = 1
        self.doAnimate()
        self.setDizzy(1)

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def exitNearVictory(self):
        # No more pies.
        self.ignore('enterCage')
        self.ignore('pieSplat')
        self.ignore('localPieSplat')
        self.ignore('outOfPies')
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.__removeCageShadow()
        self.setDizzy(0)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()

        # Actually, we'll keep the animation going, so we can continue
        # it in the Victory state.
        #self.stopAnimate()

    ##### Victory state #####

    def enterVictory(self):
        assert self.notify.debug('enterVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        # Boss Cog is on the edge of the precipice, and immediately
        # falls to his untimely end.
        self.reparentTo(render)
        self.setPos(*ToontownGlobals.SellbotBossDeathPos)
        self.setHpr(*ToontownGlobals.SellbotBossBattleThreeHpr)
        self.clearChat()
        self.cagedToon.clearChat()

        self.setCageIndex(4)

        # No one owns the toons.
        self.releaseToons(finalBattle = 1)

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        self.happy = 0
        self.raised = 0
        self.forward = 1

        # Play the boss's death animation.
        self.doAnimate('Fb_fall', now = 1)

        # We want to know when the above animation finishes playing.
        self.acceptOnce(self.animDoneEvent, self.__continueVictory)

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def __continueVictory(self):
        # Ok, he's gone!  We all move to the reward movie.
        
        self.stopAnimate()
        self.stash()
        self.doneBarrier('Victory')

    def exitVictory(self):
        self.stopAnimate()
        self.unstash()
        self.__removeCageShadow()

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()

    ##### Reward state #####

    def enterReward(self):
        assert self.notify.debug('enterReward()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.cagedToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()

        self.setCageIndex(4)

        # The toons are technically free to run around, but localToon
        # starts out locked down for the reward movie.
        self.releaseToons(finalBattle = 1)
        self.toMovieMode()

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        # Start the reward movie playing.

        panelName = self.uniqueName('reward')
        self.rewardPanel = RewardPanel.RewardPanel(panelName)
        (victory, camVictory) = MovieToonVictory.doToonVictory(
                                1, self.involvedToons,
                                self.toonRewardIds,
                                self.toonRewardDicts,
                                self.deathList,
                                self.rewardPanel,
                                allowGroupShot = 0,
                                uberList = self.uberList)

        ival = Sequence(
            Parallel(victory, camVictory),
            Func(self.__doneReward))

        intervalName = "RewardMovie"
        delayDeletes = []
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete.DelayDelete(toon, 'SellbotBoss.enterReward'))
                                    
        ival.delayDeletes = delayDeletes
        ival.start()
        self.storeInterval(ival, intervalName)

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def __doneReward(self):
        self.doneBarrier('Reward')
        self.toWalkMode()

    def exitReward(self):
        intervalName = "RewardMovie"
        self.clearInterval(intervalName)

        self.unstash()
        self.rewardPanel.destroy()
        del self.rewardPanel
        self.__removeCageShadow()

        self.battleThreeMusicTime = 0
        self.battleThreeMusic.stop()

    ##### Epilogue state #####

    def enterEpilogue(self):
        assert self.notify.debug('enterEpilogue()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.cagedToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()

        self.setCageIndex(4)

        # The toons are under our control once again.
        self.controlToons()

        # Retract all of the ramps but the back one.
        self.rampA.request('retract')
        self.rampB.request('retract')
        self.rampC.request('extend')

        self.__arrangeToonsAroundCage()
        camera.reparentTo(render)
        camera.setPosHpr(-24, 52, 27.5, -53, -13, 0)

        intervalName = "EpilogueMovie"

        seq = Sequence(self.__makeCageOpenMovie(),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        self.accept("nextChatPage", self.__epilogueChatNext)
        self.accept("doneChatPage", self.__epilogueChatDone)

        base.playMusic(self.epilogueMusic, looping=1, volume=0.9)

    def __epilogueChatNext(self, pageNumber, elapsed):
        if pageNumber == 2:
            # "I am in your debt."
            if self.cagedToon.style.torso[1] == 'd':
                track = ActorInterval(self.cagedToon, 'curtsy')
            else:
                track = ActorInterval(self.cagedToon, 'bow')

            track = Sequence(track, Func(self.cagedToon.loop, 'neutral'))
            intervalName = "EpilogueMovieToonAnim"
            self.storeInterval(track, intervalName)
            track.start()

    def __epilogueChatDone(self, elapsed):
        assert self.notify.debug('epilogueChatDone()')
        self.cagedToon.setChatAbsolute(TTLocalizer.CagedToonGoodbye, CFSpeech)

        self.ignore("nextChatPage")
        self.ignore("doneChatPage")

        intervalName = "EpilogueMovieToonAnim"
        self.clearInterval(intervalName)
        track = Parallel(
            Sequence(ActorInterval(self.cagedToon, 'wave'),
                     Func(self.cagedToon.loop, 'neutral')),
            Sequence(Wait(0.5),
                     Func(self.localToonToSafeZone)))
        self.storeInterval(track, intervalName)
        track.start()
        
    def exitEpilogue(self):
        self.clearInterval("EpilogueMovieToonAnim")
        self.unstash()
        self.__removeCageShadow()

        self.epilogueMusic.stop()

    def __arrangeToonsAroundCage(self):
        radius = 15
        numToons = len(self.involvedToons)
        center = (numToons - 1) / 2.0
        for i in range(numToons):
            toon = base.cr.doId2do.get(self.involvedToons[i])
            if toon:
                angle = 270 - 15 * (i - center)

                radians = angle * math.pi / 180.0
                x = math.cos(radians) * radius
                y = math.sin(radians) * radius
                toon.setPos(self.cage, x, y, 0)
                toon.setZ(18.0)
                toon.headsUp(self.cage)
            
        

    ##### Frolic state #####

    # This state is probably only useful for debugging.  The toons are
    # all free to run around the world.

    def enterFrolic(self):
        DistributedBossCog.DistributedBossCog.enterFrolic(self)
        self.setPosHpr(*ToontownGlobals.SellbotBossBattleOnePosHpr)


    ##### Misc. utility functions #####

    def doorACallback(self, isOpen):
        # Called whenever doorA opens or closes.
        if self.insidesANodePath:
            if isOpen:
                self.insidesANodePath.unstash()
            else:
                self.insidesANodePath.stash()

    def doorBCallback(self, isOpen):
        # Called whenever doorB opens or closes.
        if self.insidesBNodePath:
            if isOpen:
                self.insidesBNodePath.unstash()
            else:
                self.insidesBNodePath.stash()

    def __toonsToPromotionPosition(self, toonIds, battleNode):

        # At first, the toons walk down the ramp and stand close to
        # the Boss Cog to receive a promotion.  They don't back up to
        # battle position until a little bit later.

        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]
        
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                toon.reparentTo(render)
                pos, h = points[i]
                toon.setPosHpr(battleNode, pos[0], pos[1] + 10, pos[2], h, 0, 0)
        
    def __doobersToPromotionPosition(self, doobers, battleNode):

        # The doobers start out facing the Boss Cog.
        
        points = BattleBase.BattleBase.toonPoints[len(doobers) - 1]
        
        for i in range(len(doobers)):
            suit = doobers[i]
            suit.fsm.request('neutral')
            suit.loop('neutral')
            pos, h = points[i]
            suit.setPosHpr(battleNode, pos[0], pos[1] + 10, pos[2], h, 0, 0)
        
    def __touchedCage(self, entry):
        assert self.notify.debug("__touchedCage()")
        # The avatar has jumped up to touch the cage; he should be
        # given pies now.
        self.sendUpdate('touchCage', [])
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        base.playSfx(self.piesRestockSfx)

        if not self.everThrownPie:
            taskMgr.doMethodLater(30, self.__howToThrowPies,
                                  self.uniqueName("PieAdvice"))

    def __outOfPies(self):
        self.__showOnscreenMessage(TTLocalizer.BossBattleNeedMorePies)
        taskMgr.doMethodLater(20, self.__howToGetPies,
                              self.uniqueName("PieAdvice"))

    def __howToGetPies(self, task):
        self.__showOnscreenMessage(TTLocalizer.BossBattleHowToGetPies)

    def __howToThrowPies(self, task):
        self.__showOnscreenMessage(TTLocalizer.BossBattleHowToThrowPies)

    def __foundPieButton(self):
        self.everThrownPie = 1
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        
        
    def __pieSplat(self, toon, pieCode):
        assert self.notify.debug("__pieSplat()")
        # A pie thrown by localToon or some other toon hit something;
        # show a visible reaction if that something is the boss.
        if base.config.GetBool('easy-vp', 0):
            if not self.dizzy:
                pieCode = ToontownGlobals.PieCodeBossInsides
        if pieCode == ToontownGlobals.PieCodeBossInsides:
            if toon == localAvatar:
                self.d_hitBossInsides()

            self.flashRed()
        
        elif pieCode == ToontownGlobals.PieCodeBossCog:
            if toon == localAvatar:
                self.d_hitBoss(1)

            if self.dizzy:
                self.flashRed()
                self.doAnimate('hit', now=1)
        
    def __localPieSplat(self, pieCode, entry):
        assert self.notify.debug("__localPieSplat()")
        # A pie thrown by localToon toon hit something; tell the AI if
        # we hit another toon.
        if pieCode != ToontownGlobals.PieCodeToon:
            return

        avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
        if avatarDoId == '':
            self.notify.warning("Toon %s has no avatarDoId tag." % (repr(entry.getIntoNodePath())))
            return

        doId = int(avatarDoId)
        if doId != localAvatar.doId:
            self.d_hitToon(doId)

        
    def __finalPieSplat(self, toon, pieCode):
        assert self.notify.debug("__finalPieSplat()")
        # This is the final pie toss that starts the boss's fall.
        # It's really just a formality, since we're already in the
        # Victory state.
        if pieCode != ToontownGlobals.PieCodeBossCog:
            return

        # Tell the AI; the AI will then immediately transition to Victory
        # state.
        self.sendUpdate('finalPieSplat', [])

        # We don't care to hear any more about pies hitting the boss.
        self.ignore('pieSplat')
        
    def cagedToonBattleThree(self, index, avId):
        assert self.notify.debug('cagedToonBattleThree(%s, %s)' % (index, avId))

        # The caged toon says something during battle three.
        str = TTLocalizer.CagedToonBattleThree.get(index)
        if str:
            toonName = ''
            if avId:
                toon = self.cr.doId2do.get(avId)
                if not toon:
                    self.cagedToon.clearChat()
                    return
                toonName = toon.getName()
            text = str % { 'toon' : toonName }
            self.cagedToon.setChatAbsolute(text, CFSpeech | CFTimeout)

        else:
            self.cagedToon.clearChat()

    def cleanupAttacks(self):
        # Stops any attack currently running.
        self.__cleanupStrafe()

    def __cleanupStrafe(self):
        if self.strafeInterval:
            self.strafeInterval.finish()
            self.strafeInterval = None

    def doStrafe(self, side, direction):
        assert self.notify.debug('doStrafe(%s, %s)' % (side, direction))

        # Spit a stream of gears out either the front or the back
        # door, from left to right (or from right to left).

        gearRoot = self.rotateNode.attachNewNode('gearRoot')
        if side == 0:
            gearRoot.setPos(0, -7, 3)
            gearRoot.setHpr(180, 0, 0)
            door = self.doorA
        else:
            gearRoot.setPos(0, 7, 3)
            door = self.doorB
        
        gearRoot.setTag('attackCode', str(ToontownGlobals.BossCogStrafeAttack))
        gearModel = self.getGearFrisbee()
        gearModel.setScale(0.1)

        t = self.getBossDamage() / 100.0

        gearTrack = Parallel()

        # numGears ranges from 4 to 10
        # time ranges from 5 to 1
        numGears = int(4 + 6 * t + 0.5)
        time = 5.0 - 4.0 * t

        spread = 60 * math.pi / 180.0
        if direction == 1:
            spread = -spread
            
        dist = 50
        rate = time / numGears
        for i in range(numGears):
            node = gearRoot.attachNewNode(str(i))
            node.hide()
            node.setPos(0, 0, 0)
            gear = gearModel.instanceTo(node)
            angle = ((float(i) / (numGears - 1)) - 0.5) * spread
            x = dist * math.sin(angle)
            y = dist * math.cos(angle)
            h = random.uniform(-720, 720)
            gearTrack.append(Sequence(
                Wait(i * rate),
                Func(node.show),
                Parallel(node.posInterval(1, Point3(x, y, 0), fluid = 1),
                         node.hprInterval(1, VBase3(h, 0, 0), fluid = 1),
                         Sequence(SoundInterval(self.strafeSfx[i], volume = 0.2, node = self), duration = 0),
                         ),
                Func(node.detachNode)))

        seq = Sequence(
            Func(door.request, 'open'),
            Wait(0.7),
            gearTrack,
            Func(door.request, 'close'),
            )

        self.__cleanupStrafe()
        self.strafeInterval = seq
        seq.start()
