from direct.showbase.ShowBase import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import *
from direct.distributed.ClockDelta import *
from direct.showbase.PythonUtil import Functor
from direct.showbase.PythonUtil import StackTrace
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.fsm import ClassicFSM
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
from toontown.building import ElevatorConstants
from toontown.toonbase import ToontownTimer

# This pointer keeps track of the one DistributedSellbotBoss that
# should appear within the avatar's current visibility zones.  If
# there is more than one DistributedSellbotBoss visible to a client at
# any given time, something is wrong.
OneBossCog = None

class DistributedLawbotBoss(DistributedBossCog.DistributedBossCog, FSM.FSM):
    """
    Adapted from DistributedSellbotBoss.  The pie became evide, the cage became the witness stand
    """
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBoss')
    #notify.setDebug(1)

    debugPositions = False

    def __init__(self, cr):
        """
        Constructor, initialize most fields to zero or None
        """
        self.notify.debug("----- __init___")
        DistributedBossCog.DistributedBossCog.__init__(self, cr)

        FSM.FSM.__init__(self, 'DistributedLawbotBoss')

        self.lawyers = []
        self.lawyerRequest = None

        self.bossDamage = 0
        self.attackCode = None
        self.attackAvId = 0
        self.recoverRate = 0
        self.recoverStartTime = 0
        self.bossDamageMovie = None

        self.everThrownPie = 0
        self.battleThreeMusicTime = 0
        self.insidesANodePath = None
        self.insidesBNodePath = None


        self.strafeInterval = None
        self.onscreenMessage = None

        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage

        self.elevatorType = ElevatorConstants.ELEVATOR_CJ       

        self.gavels = {}
        self.chairs = {}
        self.cannons = {}

        self.useCannons = 1

        self.juryBoxIval = None
        self.juryTimer = None

        self.witnessToon = None
        self.witnessToonOnstage = False

        self.numToonJurorsSeated = 0

        self.mainDoor = None
        self.reflectedMainDoor = None

        self.panFlashInterval = None

        self.panDamage = ToontownGlobals.LawbotBossDefensePanDamage
        if base.config.GetBool('lawbot-boss-cheat',0):
            self.panDamage = 25

        self.evidenceHitSfx = None
        self.toonUpSfx = None

        self.bonusTimer = None
        
        self.warningSfx = None
        self.juryMovesSfx = None

        self.baseColStashed =False #are the collisions for the scale base stashed
        self.battleDifficulty = 0 #how hard is battle three
        self.bonusWeight = 0 #bonus weight to our evidence due to seating toons
        self.numJurorsLocalToonSeated = 0 #how many jurors did local player seat

        self.cannonIndex = -1 #which cannon the local player used

    def announceGenerate(self):
        """
        At this point all required fields have been filled in
        """
        self.notify.debug("----- announceGenerate")
        DistributedBossCog.DistributedBossCog.announceGenerate(self)
        # at this point all our attribs have been filled in.
        self.setName(TTLocalizer.LawbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {
            "name":  self.name,
            "dept":  (SuitDNA.getDeptFullname(self.style.dept)),
            }
        self.setDisplayName(nameInfo)

        self.piesRestockSfx = loader.loadSfx('phase_5/audio/sfx/LB_receive_evidence.mp3')
        self.rampSlideSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_VP_ramp_slide.mp3')

        self.evidenceHitSfx = loader.loadSfx('phase_11/audio/sfx/LB_evidence_hit.mp3')
        self.warningSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_GOON_tractor_beam_alarmed.mp3')

        self.juryMovesSfx = loader.loadSfx('phase_11/audio/sfx/LB_jury_moves.wav')
        self.toonUpSfx = loader.loadSfx('phase_11/audio/sfx/LB_toonup.mp3')
        
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

        #setup the witness toon
        self.__makeWitnessToon()

        self.__loadMopaths()

        # Enable the special CJ chat menu.
        localAvatar.chatMgr.chatInputSpeedChat.addCJMenu()

        global OneBossCog
        if OneBossCog != None:
            self.notify.warning("Multiple BossCogs visible.")
        OneBossCog = self
        
    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        self.notify.debug("----- disable")
        DistributedBossCog.DistributedBossCog.disable(self)
        self.request('Off')
        self.unloadEnvironment()
        self.__cleanupWitnessToon()
        
        self.__unloadMopaths()

        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        self.__cleanupStrafe()

        self.__cleanupJuryBox()
        

        render.clearTag('pieCode')

        self.targetNodePath.detachNode()

        self.cr.relatedObjectMgr.abortRequest(self.lawyerRequest)
        self.lawyerRequest = None

        self.betweenBattleMusic.stop()
        self.promotionMusic.stop()
        self.stingMusic.stop()
        self.battleTwoMusic.stop()
        self.battleThreeMusic.stop()
        self.epilogueMusic.stop()

        if self.juryTimer:
            self.juryTimer.destroy()
            del self.juryTimer

        if self.bonusTimer:
            self.bonusTimer.destroy()
            del self.bonusTimer            

        localAvatar.chatMgr.chatInputSpeedChat.removeCJMenu()
        
        global OneBossCog
        if OneBossCog == self:
            OneBossCog = None

    def delete(self):
        """
        to fix a crash bug, just keep track if we ever enter delete, 
        """
        self.notify.debug('----- delete')
        DistributedBossCog.DistributedBossCog.delete(self)        

    def d_hitBoss(self, bossDamage):
        self.notify.debug("----- d_hitBoss")
        self.sendUpdate('hitBoss', [bossDamage])

    def d_healBoss(self, bossHeal):
        self.notify.debug("----- d_bossHeal")
        self.sendUpdate('healBoss', [bossHeal])
        

    def d_hitBossInsides(self):
        self.notify.debug("----- d_hitBossInsides")
        self.sendUpdate('hitBossInsides', [])

    def d_hitDefensePan(self):
        self.notify.debug("----- d_hitDefensePan")
        self.sendUpdate('hitDefensePan', [])

    def d_hitProsecutionPan(self):
        self.notify.debug('----- d_hitProsecutionPan')
        self.sendUpdate('hitProsecutionPan', [])
        
    def d_hitToon(self, toonId):
        self.notify.debug("----- d_hitToon")
        self.sendUpdate('hitToon', [toonId])

    def gotToon(self, toon):
        """
        # A new Toon has arrived.  Put him in the right spot, if we
        # know what that is yet.  Normally, we will only see this
        # message in the WaitForToons state, or in the Off state if they
        # came in early (but someone might arrive to the battle very
        # late and see everything already advanced to the next state).
        """
        #self.notify.debug("----- gotToon")
        
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

    def setLawyerIds(self, lawyerIds):
        """
        We got the ids for the lawyers, now request the actual lawyer objects.
        """
        self.lawyers = []
        self.cr.relatedObjectMgr.abortRequest(self.lawyerRequest)
        self.lawyerRequest = self.cr.relatedObjectMgr.requestObjects(
            lawyerIds, allCallback = self.__gotLawyers)


    def __gotLawyers(self, lawyers):
        """
        Our request for the actual lawyer objects has been fulfilled
        """
        self.lawyerRequest = None
        self.lawyers = lawyers

        for i in range(len(self.lawyers)):
            suit = self.lawyers[i]
            suit.fsm.request('neutral')
            suit.loop('neutral')
            suit.setBossCogId(self.doId)


    def setBossDamage(self, bossDamage, recoverRate, timestamp):
        """
        AI telling us the new bossDamage, make the scale reflect it
        """
        #self.notify.debug("----- setBossDamage %d" % bossDamage)
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
                self.notify.debug("finish the movie then transition to NearVictory")
                self.bossDamageMovie.resumeUntil(self.bossDamageMovie.getDuration())
            else:
                # Push him up to the indicated point and he stops.
                self.bossDamageMovie.resumeUntil(self.bossDamage * self.bossDamageToMovie)

                if self.recoverRate:
                    taskMgr.add(self.__recoverBossDamage, taskName)

        self.makeScaleReflectDamage()



    def getBossDamage(self):
        """
        Get the boss damage. For CJ, recover rate should always be zero, so it should match AI
        """
        self.notify.debug("----- getBossDamage")
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime

        # Although the AI side computes and transmits getBossDamage()
        # as an integer value, on the client side we return it as a
        # floating-point value, so we can get the smooth transition
        # effect as the boss slowly starts to roll back up.
        return max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0)

    def __recoverBossDamage(self, task):
        """
        Unused for CJ.
        """
        self.notify.debug("----- __recoverBossDamage")
        if self.bossDamageMovie:
            self.bossDamageMovie.setT(self.getBossDamage() * self.bossDamageToMovie)
        return Task.cont

    def __walkToonToPromotion(self, toonId, delay, mopath, track, delayDeletes):
        """
        # Generates an interval to walk the toon along the mopath
        # towards its destination (which is the toon's current pos).
        """
        self.notify.debug("----- __walkToonToPromotion")
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
            delayDeletes.append(DelayDelete.DelayDelete(toon, 'LawbotBoss.__walkToonToPromotion'))

    def __walkSuitToPoint(self, node, fromPos, toPos):
        """
        Unused for CJ.
        """
        self.notify.debug("----- __walkSuitToPoint")
        vector = Vec3(toPos - fromPos)
        distance = vector.length()

        # These suits walk a little faster than most.  (They're
        # still young.)
        time = distance / (ToontownGlobals.SuitWalkSpeed * 1.8)
        
        return Sequence(Func(node.setPos, fromPos),
                        Func(node.headsUp, toPos),
                        node.posInterval(time, toPos))


    def __makeRollToBattleTwoMovie(self):
        """
        # Generate an interval which shows the Boss Cog rolling to the
        # battle 2 position.
        """
        assert(self.notify.debug("----- __makeRollToBattleTwoMovie"))        

        startPos = Point3(ToontownGlobals.LawbotBossBattleOnePosHpr[0],
                          ToontownGlobals.LawbotBossBattleOnePosHpr[1],
                          ToontownGlobals.LawbotBossBattleOnePosHpr[2])
        if self.arenaSide:
            topRampPos = Point3(*ToontownGlobals.LawbotBossTopRampPosB)
            topRampTurnPos = Point3(*ToontownGlobals.LawbotBossTopRampTurnPosB)
            p3Pos = Point3(*ToontownGlobals.LawbotBossP3PosB)
        else:
            topRampPos = Point3(*ToontownGlobals.LawbotBossTopRampPosA)
            topRampTurnPos = Point3(*ToontownGlobals.LawbotBossTopRampTurnPosA)
            p3Pos = Point3(*ToontownGlobals.LawbotBossP3PosA)
            
        battlePos = Point3(ToontownGlobals.LawbotBossBattleTwoPosHpr[0],
                           ToontownGlobals.LawbotBossBattleTwoPosHpr[1],
                           ToontownGlobals.LawbotBossBattleTwoPosHpr[2])
        battleHpr = VBase3(ToontownGlobals.LawbotBossBattleTwoPosHpr[3],
                           ToontownGlobals.LawbotBossBattleTwoPosHpr[4],
                           ToontownGlobals.LawbotBossBattleTwoPosHpr[5])
        bossTrack = Sequence()

        self.notify.debug("calling setPosHpr") # -23.4, -145.6, 44.0, -10.0, -12.5, 0)")

        #cut to wide shot and boss saying placeholder text
        myInterval = camera.posHprInterval(8, Point3(-22, -100, 35),
                                  Point3(-10, -13, 0),
                                  startPos = Point3(-22, -90, 35),
                                  startHpr = Point3(-10,-13,0),
                                  blendType = 'easeInOut')        
        chatTrack = Sequence(
                     Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempJury1, CFSpeech),
                     Func(camera.reparentTo, localAvatar),
                     Func(camera.setPos, localAvatar.cameraPositions[0][0]),
                     Func(camera.setHpr, 0, 0, 0),
                     Func(self.releaseToons,1),
                    )

        # Turn the boss model around so he rolls forward.
        bossTrack.append(Func(self.getGeomNode().setH, 180))

        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)

        track, hpr = self.rollBossToPoint(battlePos, hpr, battlePos, battleHpr, 0)

        self.makeToonsWait()

        finalPodiumPos = Point3( self.podium.getX(), self.podium.getY(),
                                 self.podium.getZ() + ToontownGlobals.LawbotBossBattleTwoPosHpr[2])

        finalReflectedPodiumPos = Point3(
            self.reflectedPodium.getX(),
            self.reflectedPodium.getY(),
            self.reflectedPodium.getZ() + ToontownGlobals.LawbotBossBattleTwoPosHpr[2])
        
        # Needed to add another stash/unstash boss command because turning the boss cog around causes
        # the player to get stuck in the collision of the boss for some reason.
        return Sequence(
            #Func(self.stickToonsToFloor),
            chatTrack,
            #Func(self.unstickToons),
            bossTrack,
            Func(self.getGeomNode().setH, 0),
            Parallel(
                self.podium.posInterval(5.0, finalPodiumPos),
                self.reflectedPodium.posInterval(5.0, finalReflectedPodiumPos),
                Func(self.stashBoss),
                self.posInterval(5.0, battlePos),
                Func(taskMgr.doMethodLater,.01, self.unstashBoss, 'unstashBoss'),
            ),
            name = self.uniqueName('BattleTwoMovie'))


    def __makeRollToBattleThreeMovie(self):
        """
        No longer used by CJ.
        # Generate an interval which shows the Boss Cog rolling to the
        # battle 3 position.
        """
        assert(self.notify.debug("----- __makeRollToBalleThreeMovie"))        

        startPos = Point3(ToontownGlobals.LawbotBossBattleTwoPosHpr[0],
                          ToontownGlobals.LawbotBossBattleTwoPosHpr[1],
                          ToontownGlobals.LawbotBossBattleTwoPosHpr[2])

            
        battlePos = Point3(ToontownGlobals.LawbotBossBattleThreePosHpr[0],
                           ToontownGlobals.LawbotBossBattleThreePosHpr[1],
                           ToontownGlobals.LawbotBossBattleThreePosHpr[2])
        battleHpr = VBase3(ToontownGlobals.LawbotBossBattleThreePosHpr[3],
                           ToontownGlobals.LawbotBossBattleThreePosHpr[4],
                           ToontownGlobals.LawbotBossBattleThreePosHpr[5])
        bossTrack = Sequence()


        myInterval = camera.posHprInterval(8, Point3(-22, -100, 35),
                                  Point3(-10, -13, 0),
                                  startPos = Point3(-22, -90, 35),
                                  startHpr = Point3(-10,-13,0),
                                  blendType = 'easeInOut')        
        chatTrack = Sequence(
            
                     Func(self.setChatAbsolute, TTLocalizer.LawbotBossTrialChat1, CFSpeech),
                     #Func(camera.reparentTo, render),
                     #myInterval,
                     #Func(camera.setPosHpr, -23.4, -145.6, 44.0, -10.0, -12.5, 0),

                     Func(camera.reparentTo, localAvatar),
                     Func(camera.setPos, localAvatar.cameraPositions[0][0]),
                     Func(camera.setHpr, 0, 0, 0),
                     Func(self.releaseToons, 1),
                    )

        # Turn the boss model around so he rolls forward.
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.loop, 'Ff_neutral'))

        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)

        track, hpr = self.rollBossToPoint(battlePos, hpr, battlePos, battleHpr, 0)
        self.makeToonsWait()
        
        return Sequence(
            #Func(self.stickToonsToFloor),
            chatTrack,
            #Func(self.unstickToons),
            bossTrack,
            Func(self.getGeomNode().setH, 0),
            name = self.uniqueName('BattleTwoMovie'))




    def toNeutralMode(self):
        """
        # Move the localToon to 'walk' mode.
        """
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('waitForBattle')

    
    def makeToonsWait(self):
        """
        # Turn off remote control of the toons.  We'll move them
        # around locally for now.
        """
        self.notify.debug("makeToonsWait")        
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.stopLookAround()
                toon.stopSmooth()

        # Also put the local toon in movie mode so he won't try to
        # walk around on his own.
        if self.hasLocalToon():
            self.toMovieMode()

        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.loop('neutral')
    
    

    def makeEndOfBattleMovie(self, hasLocalToon):
        """
        # Generate an interval 
        # This one is called from DistributedBattleFinal.
        """
        assert self.notify.debug("makeEndOfBattleMovie(%s)" % (hasLocalToon))        
        name = self.uniqueName('Drop')
        seq = Sequence(name = name)

        seq += [Wait(0.0),
                ]
        if hasLocalToon:
            seq += [Func(self.show),
                    Func(camera.reparentTo, localAvatar),
                    Func(camera.setPos, localAvatar.cameraPositions[0][0]),
                    Func(camera.setHpr, 0, 0, 0)]
        seq.append(Func(self.setChatAbsolute, TTLocalizer.LawbotBossPassExam, CFSpeech))           
        seq.append( Wait(5.0) )

        seq.append(Func(self.clearChat))
                

        return seq
    
    def __makeBossDamageMovie(self):
        """
        Unused in CJ
        # Generate an interval which shows the Boss Cog rolling down
        # in retreat as the Toons attack.
        """
        self.notify.debug("---- __makeBossDamageMovie")

        startPos = Point3(ToontownGlobals.LawbotBossBattleThreePosHpr[0],
                          ToontownGlobals.LawbotBossBattleThreePosHpr[1],
                          ToontownGlobals.LawbotBossBattleThreePosHpr[2])
        startHpr = Point3(*ToontownGlobals.LawbotBossBattleThreeHpr)
        bottomPos = Point3(*ToontownGlobals.LawbotBossBottomPos)
        deathPos = Point3(*ToontownGlobals.LawbotBossDeathPos)

        self.setPosHpr(startPos, startHpr)

        bossTrack = Sequence()
        bossTrack.append(Func(self.loop, 'Ff_neutral'))
        track, hpr = self.rollBossToPoint(startPos, startHpr, bottomPos, None, 1)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(bottomPos, startHpr, deathPos, None, 1)
        bossTrack.append(track)

        duration = bossTrack.getDuration()
        return bossTrack


    def __showOnscreenMessage(self, text):
        """
        Shows a screen message.  Stays up forever unless __clearOnscreenMessage is called
        """
        self.notify.debug("----- __showOnscreenmessage")
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
        """
        Clears the screen message, if any
        """
        #self.notify.debug("----- __clearOnscreenMessage")
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None

    def __showWaitingMessage(self, task):
        """
        Show a waiting for other players message
        """
        self.notify.debug("----- __showWaitingMessage")
        self.__showOnscreenMessage(TTLocalizer.BuildingWaitingForVictors)


    ##### Environment #####

    def loadEnvironment(self):
        """
        Load most of the assets used in the battle
        """
        self.notify.debug("----- loadEnvironment")
        DistributedBossCog.DistributedBossCog.loadEnvironment(self)
        
        self.geom = loader.loadModel('phase_11/models/lawbotHQ/LawbotCourtroom3')
        #set the floor at z=0
        self.geom.setPos(0, 0, -71.601)
        self.geom.setScale(1)

        self.elevatorEntrance = self.geom.find('**/elevator_origin')
        
        # The elevatorEntrance has some geometry that it shouldn't.
        self.elevatorEntrance.getChildren().detach()
        self.elevatorEntrance.setScale(1)

        elevatorModel = loader.loadModel("phase_11/models/lawbotHQ/LB_Elevator")
        elevatorModel.reparentTo(self.elevatorEntrance)


        self.setupElevator(elevatorModel)

        # before battles: play the boss theme music
        self.promotionMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
            # 'phase_9/audio/bgm/encntr_head_suit_theme.mid')
        # Between battle one and two: play the upbeat street battle music
        self.betweenBattleMusic = base.loadMusic(
            'phase_9/audio/bgm/encntr_toon_winning.mid')
        # Battle two: play new jury music  
        self.battleTwoMusic = base.loadMusic(
            'phase_11/audio/bgm/LB_juryBG.mid')

        # Also replace the floor polygon with a plane, and rename it
        # so we can detect a collision with it.
        floor = self.geom.find('**/MidVaultFloor1')
        if floor.isEmpty():
            floor = self.geom.find('**/CR3_Floor')
        #floor.detachNode()
        self.evFloor = self.replaceCollisionPolysWithPlanes(floor)
        self.evFloor.reparentTo(self.geom)
        self.evFloor.setName('floor')

        # Also, put a big plane across the universe a few feet below
        # the floor, to catch things that fall out of the world.
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)

        # The boss makes his "escape" through this door.
        self.door3 = self.geom.find('**/SlidingDoor1/')
        if self.door3.isEmpty():
            self.door3 = self.geom.find('**/interior/CR3_Door')

        #get the main door, so we can hide it in the intro movie
        self.mainDoor = self.geom.find('**/Door_1')
        if not self.mainDoor.isEmpty():
            #itemsToHide = ['LawbotCourtroom3_collision_Door_1','CR3_LobbyFrontWall3','wall_4']
            itemsToHide = ['interior/Door_1']
            for str in itemsToHide:
                stuffToHide = self.geom.find('**/%s' % str)
                if not stuffToHide.isEmpty():
                    self.notify.debug('found %s' % stuffToHide)
                    stuffToHide.wrtReparentTo(self.mainDoor)
                else:
                    self.notify.debug('not found %s' % stuffToHide)

        self.reflectedMainDoor = self.geom.find('**/interiorrefl/CR3_Door')
        if not self.reflectedMainDoor.isEmpty():
            itemsToHide = ['Reflections/Door_1']
            for str in itemsToHide:
                stuffToHide = self.geom.find('**/%s' % str)
                if not stuffToHide.isEmpty():
                    self.notify.debug('found %s' % stuffToHide)
                    stuffToHide.wrtReparentTo(self.reflectedMainDoor)
                else:
                    self.notify.debug('not found %s' % stuffToHide)
            
        self.geom.reparentTo(render)
        self.loadWitnessStand()
        self.loadScale()

        self.scaleNodePath.stash()
        self.loadJuryBox()


        self.loadPodium()

        #make the floor reflective
        ug = self.geom.find('**/Reflections')
        ug.setBin('ground',-10)

    def loadJuryBox(self):
        """
        Load the jury box, and put it in the initial position.
        """
        self.juryBox = self.geom.find('**/JuryBox')
        juryBoxPos = self.juryBox.getPos()
        newPos = juryBoxPos - Point3(*ToontownGlobals.LawbotBossJuryBoxRelativeEndPos)

        if not self.debugPositions:
            self.juryBox.setPos( newPos)

        #move / hide the reflected JuryBox
        self.reflectedJuryBox = self.geom.find('**/JuryBox_Geo_Reflect')

        reflectedJuryBoxPos = self.reflectedJuryBox.getPos()
        newReflectedPos = reflectedJuryBoxPos - Point3(*ToontownGlobals.LawbotBossJuryBoxRelativeEndPos)
        if not self.debugPositions:
            self.reflectedJuryBox.setPos(newReflectedPos)
            
        if not self.reflectedJuryBox.isEmpty():
            if self.debugPositions:
                self.reflectedJuryBox.show()            
            else:
                #self.reflectedJuryBox.hide()
                pass
        
        self.reflectedJuryBox.setZ( self.reflectedJuryBox.getZ() + ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[2])
        

    def loadPodium(self):
        """
        Load the podim and put it in the initial position
        """
        self.podium = self.geom.find('**/Podium')
        newZ = self.podium.getZ() - ToontownGlobals.LawbotBossBattleTwoPosHpr[2]
        if not self.debugPositions:
            self.podium.setZ(newZ)

        #move the reflected podium
        self.reflectedPodium = self.geom.find('**/Podium_Geo1_Refl')

        #reflectedZ = self.reflectedPodium.getZ() - ToontownGlobals.LawbotBossBattleTwoPosHpr[2]
        reflectedZ = self.reflectedPodium.getZ() #+ ToontownGlobals.LawbotBossBattleTwoPosHpr[2]
        if not self.debugPositions:
            self.reflectedPodium.setZ(reflectedZ)
        if not self.reflectedPodium.isEmpty():
            if self.debugPositions:
                self.reflectedPodium.show()
            else:
                #self.reflectedPodium.hide()
                pass
        
        

    def loadCannons(self):
        """
        Cannons now done in DistributedLawbotCannon.py
        """
        return
        
    def loadWitnessStand(self):
        """
        Loads the witness stand.
        """
        #temp hide it, set the mailbox to it's position
        self.realWitnessStand = self.geom.find('**/WitnessStand')
        if not self.realWitnessStand.isEmpty():
            if 0: #not self.debugPositions:
                self.realWitnessStand.stash()
                pass
        #also hide the reflected witness stand
        self.reflectedWitnessStand = self.geom.find('**/Witnessstand_Geo_Reflect')
        if not self.reflectedWitnessStand.isEmpty():
            if 0: #not self.debugPositions:
                self.reflectedWitnessStand.stash()
                pass

        colNode = self.realWitnessStand.find('**/witnessStandCollisions/Witnessstand_Collision')
        colNode.setName('WitnessStand')
        

    def loadScale(self):
        """
        Load the scales of injustice.
        """
        self.useProgrammerScale = base.config.GetBool('want-injustice-scale-debug',0)
        if self.useProgrammerScale:
            self.loadScaleOld()
        else:
            self.loadScaleNew()




    def __debugScale(self):
        """
        Print out info about the scale.
        """
        prosecutionPanPos = self.prosecutionPanNodePath.getPos()
        origin = Point3(0,0,0)
        prosecutionPanRelPos = self.scaleNodePath.getRelativePoint(self.prosecutionPanNodePath, origin)
        panRenderPos = render.getRelativePoint(self.prosecutionPanNodePath, origin)
        
        self.notify.debug('prosecutionPanPos = %s' % prosecutionPanPos)
        self.notify.debug('prosecutionPanRelPos = %s' % prosecutionPanRelPos)
        self.notify.debug('panRenderPos = %s' % panRenderPos)
        

        prosecutionLocatorPos = self.prosecutionLocator.getPos()
        prosecutionLocatorRelPos = self.scaleNodePath.getRelativePoint(self.prosecutionLocator, origin)
        locatorRenderPos = render.getRelativePoint(self.prosecutionLocator, origin)
        self.notify.debug('prosecutionLocatorPos = %s ' % prosecutionLocatorPos)
        self.notify.debug('prosecutionLocatorRelPos = %s ' % prosecutionLocatorRelPos)
        self.notify.debug('locatorRenderPos = %s' % locatorRenderPos)


        beamPos = self.beamNodePath.getPos()
        beamRelPos = self.scaleNodePath.getRelativePoint(self.beamNodePath, origin)
        beamRenderPos = render.getRelativePoint(self.beamNodePath, origin)
        self.notify.debug("beamPos = %s" % beamPos)
        self.notify.debug("beamRelPos = %s" % beamRelPos)
        self.notify.debug('beamRenderPos = %s' % beamRenderPos)

        beamBoundsCenter = self.beamNodePath.getBounds().getCenter()
        self.notify.debug('beamBoundsCenter = %s' % beamBoundsCenter)        


        beamLocatorBounds = self.beamLocator.getBounds()
        beamLocatorPos = beamLocatorBounds.getCenter()
        self.notify.debug('beamLocatorPos = %s' % beamLocatorPos)
        
        #self.beamNodePath.wrtReparentTo(render)
        #self.defensePanNodePath.wrtReparentTo(render)        
        #self.scaleNodePath.hide()

    def loadScaleNew(self):
        """
        Loads the Scales of Injustice.  FOr now uses geometry created by the artist
        """
        self.scaleNodePath = loader.loadModel('phase_11/models/lawbotHQ/scale')
        self.beamNodePath = self.scaleNodePath.find('**/scaleBeam')
        self.defensePanNodePath = self.scaleNodePath.find('**/defensePan')
        self.prosecutionPanNodePath = self.scaleNodePath.find('**/prosecutionPan')
        self.defenseColNodePath = self.scaleNodePath.find('**/DefenseCol')
        self.defenseColNodePath.setTag('pieCode',str(ToontownGlobals.PieCodeDefensePan))        
        self.prosecutionColNodePath = self.scaleNodePath.find('**/ProsecutionCol')
        self.prosecutionColNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeProsecutionPan))        
        self.standNodePath = self.scaleNodePath.find('**/scaleStand')
        
        self.scaleNodePath.setPosHpr(*ToontownGlobals.LawbotBossInjusticePosHpr)

        self.defenseLocator = self.scaleNodePath.find('**/DefenseLocator')
        defenseLocBounds = self.defenseLocator.getBounds()
        defenseLocPos = defenseLocBounds.getCenter()
        self.notify.debug("defenseLocatorPos = %s" % defenseLocPos)


        self.defensePanNodePath.setPos(defenseLocPos)
        self.defensePanNodePath.reparentTo(self.beamNodePath)


        self.notify.debug("defensePanNodePath.getPos()=%s" % self.defensePanNodePath.getPos())

        self.prosecutionLocator = self.scaleNodePath.find('**/ProsecutionLocator')

        prosecutionLocBounds = self.prosecutionLocator.getBounds()
        prosecutionLocPos = prosecutionLocBounds.getCenter()
        self.notify.debug("prosecutionLocatorPos = %s" % prosecutionLocPos)
        self.prosecutionPanNodePath.setPos(prosecutionLocPos)
        self.prosecutionPanNodePath.reparentTo(self.beamNodePath)


        self.beamLocator = self.scaleNodePath.find('**/StandLocator1')

        beamLocatorBounds = self.beamLocator.getBounds()
        beamLocatorPos = beamLocatorBounds.getCenter()
        negBeamLocatorPos = -beamLocatorPos
        self.notify.debug('beamLocatorPos = %s' % beamLocatorPos)
        self.notify.debug('negBeamLocatorPos = %s' % negBeamLocatorPos)        

        self.beamNodePath.setPos(beamLocatorPos)

        #self.__debugScale()
        self.scaleNodePath.setScale(*ToontownGlobals.LawbotBossInjusticeScale)

        self.scaleNodePath.wrtReparentTo(self.geom)

        #this is the high collision poly to stop toons standing on the base, but lets pies through
        self.baseHighCol = self.scaleNodePath.find('**/BaseHighCol')
        oldBitMask = self.baseHighCol.getCollideMask()
        newBitMask = oldBitMask & ~ToontownGlobals.PieBitmask
        newBitMask = newBitMask & ~ToontownGlobals.CameraBitmask
        self.baseHighCol.setCollideMask(newBitMask)

        #this is the high collision poly surrounding the defense pan
        self.defenseHighCol = self.scaleNodePath.find('**/DefenseHighCol')
        self.defenseHighCol.stash()
        self.defenseHighCol.setCollideMask(newBitMask)

        #these are the base collissioins
        self.baseTopCol = self.scaleNodePath.find('**/Scale_base_top_collision')
        self.baseSideCol = self.scaleNodePath.find('**/Scale_base_side_col')

        #hide the grey locators
        self.defenseLocator.hide()
        self.prosecutionLocator.hide()
        self.beamLocator.hide()

        

    def loadScaleOld(self):
        """
        Loads the Scales of Injustice.  For now uses geometry created programtically.
        """
        startingTilt = 0; #higher number is good for the players

        #This will be the parent of everything
        self.scaleNodePath = NodePath("injusticeScale")

        #Create the beam geometry
        beamGeom = self.createBlock(0.25,2,0.125, -0.25,-2,-0.125, 0,1.0,0,1.0)
        self.beamNodePath = NodePath("scaleBeam")
        self.beamNodePath.attachNewNode(beamGeom)
        self.beamNodePath.setPos(0,0,3)
        self.beamNodePath.reparentTo (self.scaleNodePath)


        #Create the defense pan geometry
        defensePanGeom = self.createBlock(0.5,0.5,0, -0.5, -0.5, -2, 0, 0, 1.0, 0.25)
        self.defensePanNodePath = NodePath("defensePan")
        self.defensePanNodePath.attachNewNode(defensePanGeom)
        self.defensePanNodePath.setPos(0,-2,0)
        self.defensePanNodePath.reparentTo (self.beamNodePath)


        #Create the collision node for the defense pan
        defenseTube = CollisionTube(0,0,-0.5,
                                    0,0,-1.5,
                                    0.6)
        defenseTube.setTangible(1)
        defenseCollNode = CollisionNode("DefenseCol")        
        defenseCollNode.addSolid(defenseTube)
        self.defenseColNodePath = self.defensePanNodePath.attachNewNode(defenseCollNode)
        self.defenseColNodePath.setTag('pieCode',str(ToontownGlobals.PieCodeDefensePan))
        
        #Create the prosecution pan geometry
        prosecutionPanGeom = self.createBlock(0.5,0.5,0, -0.5, -0.5, -2, 1.0, 0, 0,1.0)
        self.prosecutionPanNodePath = NodePath("prosecutionPan")
        self.prosecutionPanNodePath.attachNewNode(prosecutionPanGeom)
        self.prosecutionPanNodePath.setPos(0,2,0)
        self.prosecutionPanNodePath.reparentTo (self.beamNodePath)


        #Create the collision node for the prosecution pan
        prosecutionTube = CollisionTube(0,0,-0.5,
                                    0,0,-1.5,
                                    0.6)
        prosecutionTube.setTangible(1)
        prosecutionCollNode = CollisionNode(self.uniqueName("ProsecutionCol"))        
        prosecutionCollNode.addSolid(prosecutionTube)
        self.prosecutionColNodePath = self.prosecutionPanNodePath.attachNewNode(prosecutionCollNode)
        self.prosecutionColNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeProsecutionPan))


        #Create the stand geometry
        standGeom = self.createBlock(0.25,0.25,0, -0.25, -0.25, 3)
        self.standNodePath = NodePath("scaleStand")
        self.standNodePath.attachNewNode(standGeom)
        self.standNodePath.reparentTo(self.scaleNodePath)
        

        self.scaleNodePath.setPosHpr(*ToontownGlobals.LawbotBossInjusticePosHpr)
        self.scaleNodePath.setScale(5.0)
        self.scaleNodePath.wrtReparentTo(self.geom)

        self.setScaleTilt(startingTilt)


    def setScaleTilt(self, tilt):
        """
        Tilt the scales of injustice.  Tilt should be in degrees.  A positive number is
        good for the players.
        """
        self.beamNodePath.setP(tilt)

        if self.useProgrammerScale:
            self.defensePanNodePath.setP(-tilt)
            self.prosecutionPanNodePath.setP(-tilt)
        else:
            self.defensePanNodePath.setP(-tilt)
            self.prosecutionPanNodePath.setP(-tilt)            

    def stashBaseCol(self):
        """
        Stash the base collision.
        """
        if not self.baseColStashed:
            self.notify.debug('stashBaseCol')
            self.baseTopCol.stash()
            self.baseSideCol.stash()
            self.baseColStashed = True

    def unstashBaseCol(self):
        """
        Unstash the base collision.
        """
        if self.baseColStashed:
            self.notify.debug('unstashBaseCol')
            self.baseTopCol.unstash()
            self.baseSideCol.unstash()
            self.baseColStashed = False

    def makeScaleReflectDamage(self):
        """
        Set the scale tilt based on the damage.
        Also hide the base collision if the defense pan is low enough.
        """

        diffDamage = self.bossDamage - ToontownGlobals.LawbotBossInitialDamage
        diffDamage *= 1.0

        #potentially initial damage is skewed in favor of the proescution or the defense as we do balancing
        if (diffDamage >= 0):
            percentDamaged = diffDamage / ( ToontownGlobals.LawbotBossMaxDamage - ToontownGlobals.LawbotBossInitialDamage)
            tilt = percentDamaged * ToontownGlobals.LawbotBossWinningTilt
        else:
            percentDamaged = diffDamage / ( ToontownGlobals.LawbotBossInitialDamage - 0)
            tilt = percentDamaged * ToontownGlobals.LawbotBossWinningTilt            

        self.setScaleTilt(tilt)

        if self.bossDamage < ToontownGlobals.LawbotBossMaxDamage * 0.85:
            self.unstashBaseCol()
        else:
            self.stashBaseCol()
        
                  
    def unloadEnvironment(self):
        """
        Unloads the environment, also calls base class unload.
        """
        self.notify.debug("----- unloadEnvironment")
        DistributedBossCog.DistributedBossCog.unloadEnvironment(self)

        self.geom.removeNode()
        del self.geom



    def __loadMopaths(self):
        """
        Unused in CJ.
        """
        self.notify.debug("----- __loadMopaths")
        self.toonsEnterA = Mopath.Mopath()
        self.toonsEnterA.loadFile('phase_9/paths/bossBattle-toonsEnterA')
        self.toonsEnterA.fFaceForward = 1
        self.toonsEnterA.timeScale = 35
        self.toonsEnterB = Mopath.Mopath()
        self.toonsEnterB.loadFile('phase_9/paths/bossBattle-toonsEnterB')
        self.toonsEnterB.fFaceForward = 1
        self.toonsEnterB.timeScale = 35

    def __unloadMopaths(self):
        """
        Unused in CJ
        """
        self.notify.debug("----- __unloadMopaths")
        self.toonsEnterA.reset()
        self.toonsEnterB.reset()




    ##### Off state #####

    def enterOff(self):
        """
        Handle Off state. We can get to this state if unexpectly losing connection to server
        """
        self.notify.debug("----- enterOff")
        DistributedBossCog.DistributedBossCog.enterOff(self)

        if self.witnessToon:
            self.witnessToon.clearChat()
            #temp debug only
            #self.__showWitnessToon()



    ##### WaitForToons state #####

    def enterWaitForToons(self):
        """
        We're about to do battle two or three, wait for the other plaers
        """
        self.notify.debug("----- enterWaitForToons")
        DistributedBossCog.DistributedBossCog.enterWaitForToons(self)

        self.geom.hide()

        # Disable the witness toon's nametag while we're here in space
        # waiting.
        self.witnessToon.removeActive()
        

    def exitWaitForToons(self):
        """
        Other players done or disconnected, move on
        """
        self.notify.debug("----- exitWaitForToons")
        DistributedBossCog.DistributedBossCog.exitWaitForToons(self)

        self.geom.show()

        self.witnessToon.addActive()        


    ##### Elevator state #####

    def enterElevator(self):
        """
        The first state, toons are riding the elevator
        """
        self.notify.debug("----- enterElevator")
        DistributedBossCog.DistributedBossCog.enterElevator(self)


        # Disable the witness toon's nametag while we're in the
        # elevator.
        self.witnessToon.removeActive()

        
        # Set the boss up in the middle of the floor, so we can see
        # him when the doors open.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleOnePosHpr)

        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        self.__hideWitnessToon()

        if not self.mainDoor.isEmpty():
            self.mainDoor.stash()
        if not self.reflectedMainDoor.isEmpty():
            self.reflectedMainDoor.stash()
            

        # Position the camera behind the toons
        camera.reparentTo(self.elevatorModel)
        camera.setPosHpr(0, 30, 8, 180, 0, 0)


    def exitElevator(self):
        """
        Exit elevator state.
        """
        self.notify.debug("----- exitElevator")
        DistributedBossCog.DistributedBossCog.exitElevator(self)

        self.witnessToon.removeActive()
        

    ##### Introduction state #####

    def enterIntroduction(self):
        """
        Enter the Introduction state, CJ speech, toons are revealed.
        """
        # Set the boss up in the middle of the floor, actively
        self.notify.debug("----- enterIntroduction")
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleOnePosHpr)
        self.stopAnimate()

        self.__hideWitnessToon()

        DistributedBossCog.DistributedBossCog.enterIntroduction(self)

        # Make sure the side ramps are extended and the back ramp is
        # retracted.


        base.playMusic(self.promotionMusic, looping=1, volume=0.9)

        if not self.mainDoor.isEmpty():
            self.mainDoor.stash()
        if not self.reflectedMainDoor.isEmpty():
            self.reflectedMainDoor.stash()
            
        
        
    def exitIntroduction(self):
        """
        Exit introduction state.
        """
        self.notify.debug("----- exitIntroduction")
        DistributedBossCog.DistributedBossCog.exitIntroduction(self)

        self.promotionMusic.stop()

        if not self.mainDoor.isEmpty():
            #self.mainDoor.unstash()
            pass
        if not self.reflectedMainDoor.isEmpty():
            self.reflectedMainDoor.unstash()
            

        if not self.elevatorEntrance.isEmpty():
            pass
            #self.elevatorEntrance.hide()
        

    ##### BattleOne state #####

    def enterBattleOne(self):
        """
        Battle one state, fight lots of cogs.
        """
        self.notify.debug("----- LawbotBoss.enterBattleOne ")
        DistributedBossCog.DistributedBossCog.enterBattleOne(self)

        # Boss Cog is still in the middle of the floor.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleOnePosHpr)
        self.clearChat()
        self.loop('Ff_neutral') #just in case we got here through a magic word


        self.notify.debug("self.battleANode = %s" % self.battleANode)
        
        # The toons should be in their battle position.
        #self.toonsToBattlePosition(self.toonsA, self.battleANode)
        #self.toonsToBattlePosition(self.toonsB, self.battleBNode)

        self.__hideWitnessToon()

        if self.battleA == None or self.battleB == None:
            pass
        else:
            pass


    def exitBattleOne(self):
        """
        Done with battle one state.
        """
        self.notify.debug("----- exitBattleOne")
        DistributedBossCog.DistributedBossCog.exitBattleOne(self)

    # helper function for boss temp fix    
    def stashBoss(self):
        self.stash()
    
    # helper function for boss temp fix
    def unstashBoss(self, task):
        self.unstash()
        self.reparentTo(render)
        
    ##### RollToBattleTwo state #####

    def enterRollToBattleTwo(self):
        """
        Rolling to the podium.
        """
        self.notify.debug("----- enterRollToBattleTwo")
        assert self.notify.debug('enterRollToBattleTwo()')

        self.releaseToons(finalBattle = 1)
        # There is a strange collision issue when we try to turn the cog boss
        # So until this is fixed we stash the boss for a split second to not hit the player
        # automatically losing them laff points
        self.stashBoss()
        
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
        taskMgr.doMethodLater(.01, self.unstashBoss, 'unstashBoss')
        
    def __onToPrepareBattleTwo(self):
        """
        Done rolling to podium
        """
        self.notify.debug("----- __onToPrepareBattleTwo")
        # Make sure the boss ends up in his battle position.
        self.unstickBoss()
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleTwoPosHpr)
        self.doneBarrier('RollToBattleTwo')

    def exitRollToBattleTwo(self):
        """
        Exit the roll to battle two state.
        """
        self.notify.debug("----- exitRollToBattleTwo")
        self.unstickBoss()
        intervalName = "RollToBattleTwo"
        self.clearInterval(intervalName)

        self.betweenBattleMusic.stop()

    ##### PrepareBattleTwo state #####

    def enterPrepareBattleTwo(self):
        """
        Show the witness toon talking, and bring out the cannons.
        """
        self.notify.debug("----- enterPrepareBattleTwo")
        assert self.notify.debug('enterPrepareBattleTwo()')
        self.cleanupIntervals()

        self.controlToons()
        #don't leave them in the walking state if we take the control away from player
        self.setToonsToNeutral(self.involvedToons)

        #self.releaseToons(finalBattle = 1)

        self.clearChat()
        self.reparentTo(render)


        #now show our star witness and have him give instructions
        self.__showWitnessToon()

        prepareBattleTwoMovie = self.__makePrepareBattleTwoMovie()

        # Now generate the interval that plays the movie.
        intervalName = "prepareBattleTwo"
        seq = Sequence(prepareBattleTwoMovie,
                       #Func(self.__onToBattleTwo),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        # We see the witness  toon giving us advice 
        # advice for the battle two; we have to click through
        # this advice to move on.
        #self.acceptOnce("doneChatPage", self.__onToBattleTwo)
        self.acceptOnce("doneChatPage", self.__showCannonsAppearing)

        # Let's play the elevator music again; it's dramatic enough to
        # use twice.
        base.playMusic(self.stingMusic, looping=0, volume=1.0)

    def __showCannonsAppearing(self, elapsedTime = 0):
        """
        Show the toons taking out their cannons.
        """
        
        allCannonsAppear = Sequence(
                        Func(self.__positionToonsInFrontOfCannons),
                        Func(camera.reparentTo, localAvatar),
                        Func(camera.setPos, localAvatar.cameraPositions[2][0]),
                        Func(camera.lookAt, localAvatar),
                        )

        multiCannons = Parallel()
        
        index = 0
        self.involvedToons.sort()
        for toonId in self.involvedToons: 
            toon = self.cr.doId2do.get(toonId)
            if toon:
                if self.cannons.has_key(index):
                    cannon = self.cannons[index]
                    cannonSeq = cannon.generateCannonAppearTrack(toon)
                    multiCannons.append(cannonSeq)
                    index += 1                    
                else:
                    self.notify.warning('No cannon %d but we have a toon =%d' % (index,toonId))


        allCannonsAppear.append(multiCannons)

        # Now generate the interval that plays the movie.
        intervalName = "prepareBattleTwoCannonsAppear"
        seq = Sequence(allCannonsAppear,
                       Func(self.__onToBattleTwo),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)
        
    

    def __onToBattleTwo(self, elapsedTime=0):
        """
        Donw with jury.
        """
        self.notify.debug("----- __onToBattleTwo")
        self.doneBarrier('PrepareBattleTwo')

        # Wait a second.  If we don't move on immediately, pop up the
        # "waiting for other players" message.
        taskMgr.doMethodLater(1, self.__showWaitingMessage,
                              self.uniqueName("WaitingMessage"))

    def exitPrepareBattleTwo(self):
        """
        Cleanup PrepareBattleTwo state.
        """
        self.notify.debug("----- exitPrepareBattleTwo")
        self.show()
        taskMgr.remove(self.uniqueName("WaitingMessage"))
        self.ignore("doneChatPage")
        self.__clearOnscreenMessage()
        self.stingMusic.stop()
        
    ##### BattleTwo state #####

    def enterBattleTwo(self):
        """
        Enter the cannons and jury state.
        """
        self.notify.debug("----- enterBattleTwo")
        assert self.notify.debug('enterBattleTwo()')
        self.cleanupIntervals()

        # Get the credit multiplier
        mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(2)
        localAvatar.inventory.setBattleCreditMultiplier(mult)

        # Boss Cog is now on top of the ramp.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleTwoPosHpr)

        # Clear the chat dialogs left over from the transition movie.
        self.clearChat()
        self.witnessToon.clearChat()


        # Now the battle holds the toons.
        self.releaseToons(finalBattle = 1)

        self.__showWitnessToon()
        
        
        # Position the toons to the battle.
        if not self.useCannons:
            self.toonsToBattlePosition(self.toonsA, self.battleANode)
            self.toonsToBattlePosition(self.toonsB, self.battleBNode)

        base.playMusic(self.battleTwoMusic, looping=1, volume=0.9)


        self.startJuryBoxMoving()

        for index in range(len(self.cannons)):
            #make sure I can see the cannon
            cannon = self.cannons[index]
            cannon.cannon.show()
        
        
    def getChairParent(self):
        """
        Where do the jury chairs reparent to.
        """
        return self.juryBox

    def startJuryBoxMoving(self):
        
        curPos = self.juryBox.getPos()
        endingAbsPos = Point3(curPos[0] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[0],
                              curPos[1] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[1],
                              curPos[2] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[2]
                              )
        
        curReflectedPos = self.reflectedJuryBox.getPos()
        reflectedEndingAbsPos = Point3 (curReflectedPos[0] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[0],
                              curReflectedPos[1] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[1],
                              curReflectedPos[2] +
                              ToontownGlobals.LawbotBossJuryBoxRelativeEndPos[2]
                              )
        self.juryBoxIval = Parallel(
            self.juryBox.posInterval( ToontownGlobals.LawbotBossJuryBoxMoveTime, endingAbsPos),
            self.reflectedJuryBox.posInterval( ToontownGlobals.LawbotBossJuryBoxMoveTime, reflectedEndingAbsPos),
            SoundInterval(self.juryMovesSfx, node = self.chairs[2].nodePath, duration = ToontownGlobals.LawbotBossJuryBoxMoveTime,  loop = 1, volume = 1.0),
            )
        
        self.juryBoxIval.start()
        
        #setup jury timer
        self.juryTimer = ToontownTimer.ToontownTimer()
        self.juryTimer.posInTopRightCorner()
        self.juryTimer.countdown(ToontownGlobals.LawbotBossJuryBoxMoveTime)

    def exitBattleTwo(self):
        """
        Done with this state, do the cleanup.
        """
        self.notify.debug("----- exitBattleTwo")
        intervalName = self.uniqueName('Drop')
        self.clearInterval(intervalName)
        self.cleanupBattles()
        self.battleTwoMusic.stop()

        # No more credit multiplier
        localAvatar.inventory.setBattleCreditMultiplier(1)

        if (self.juryTimer):
            self.juryTimer.destroy()
            del self.juryTimer
            self.juryTimer = None

        for chair in self.chairs.values():
            chair.stopCogsFlying()
            


    ##### RollToBattleThree state #####

    def enterRollToBattleThree(self):
        """
        Unused in CJ
        """
        self.notify.debug("----- enterRollToBattleThree")
        assert self.notify.debug('enterRollToBattleThree()')

        self.reparentTo(render)

        
        # The Boss Cog rolls up the ramp into position for battle two,
        # while the Toons are free to run around for a few seconds.
        self.stickBossToFloor()

        # Now generate the interval that plays the movie.
        intervalName = "RollToBattleThree"
        seq = Sequence(self.__makeRollToBattleThreeMovie(),
                       Func(self.__onToPrepareBattleThree),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        base.playMusic(self.betweenBattleMusic, looping=1, volume=0.9)

    def __onToPrepareBattleThree(self):
        """
        Unused in CJ.
        """
        self.notify.debug("----- __onToPrepareBattleThree")
        # Make sure the boss ends up in his battle position.
        self.unstickBoss()
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleThreePosHpr)
        self.doneBarrier('RollToBattleThree')

    def exitRollToBattleThree(self):
        """
        Unused in CJ.
        """
        self.notify.debug("----- exitRollToBattleThree")
        self.unstickBoss()
        intervalName = "RollToBattleThree"
        self.clearInterval(intervalName)

        self.betweenBattleMusic.stop()
        

    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        """
        Witness toon gives us a recap and advice.
        """
        self.notify.debug("----- enterPrepareBattleThree")
        assert self.notify.debug('enterPrepareBattleThree()')
        self.cleanupIntervals()

        self.controlToons()
        #don't leave them in the walking state if we take the control away from player
        self.setToonsToNeutral(self.involvedToons)        
        #self.releaseToons(finalBattle = 1)

        self.clearChat()

        self.reparentTo(render)

        # Retract all of the ramps but the back one.
        base.playMusic(self.betweenBattleMusic, looping=1, volume=0.9)

        self.__showWitnessToon()

        prepareBattleThreeMovie = self.__makePrepareBattleThreeMovie()

        # We see the witness  toon giving us advice 
        # advice for the battle two; we have to click through
        # this advice to move on.
        self.acceptOnce("doneChatPage", self.__onToBattleThree)


        # Now generate the interval that plays the movie.
        intervalName = "prepareBattleThree"
        seq = Sequence(prepareBattleThreeMovie,
                       #Func(self.__onToBattleTwo),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        

    def __onToBattleThree(self, elapsed):
        """
        We're done listening to the witness toon.
        """
        self.notify.debug("----- __onToBattleThree")
        self.doneBarrier('PrepareBattleThree')

        # Wait a second.  If we don't move on immediately, pop up the
        # "waiting for other players" message.
        taskMgr.doMethodLater(1, self.__showWaitingMessage,
                              self.uniqueName("WaitingMessage"))

    def exitPrepareBattleThree(self):
        """
        Done with this state. Do cleanup
        """
        self.notify.debug("----- exitPrepareBattleThree")
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

        self.scaleNodePath.unstash()
        
        localAvatar.setPos(-3,0,0)        
        camera.reparentTo( localAvatar)
        camera.setPos( localAvatar.cameraPositions[0][0])
        camera.setHpr( 0, 0, 0)

        self.clearChat()
        self.witnessToon.clearChat()
        self.reparentTo(render)

        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        # Now we're in pie mode.
        self.accept('enterWitnessStand', self.__touchedWitnessStand)
        self.accept('pieSplat', self.__pieSplat)
        self.accept('localPieSplat', self.__localPieSplat)
        self.accept('outOfPies', self.__outOfPies)
        self.accept('begin-pie', self.__foundPieButton)
        self.accept('enterDefenseCol', self.__enterDefenseCol)
        self.accept('enterProsecutionCol', self.__enterProsecutionCol)

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

        self.setPosHpr(*ToontownGlobals.LawbotBossBattleThreePosHpr)        

        self.bossMaxDamage = ToontownGlobals.LawbotBossMaxDamage
        
        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9)

        self.__showWitnessToon()

        diffSettings = ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
        if diffSettings[4]:
            #ok so we have toon jurors affecting the weight
            # Enable the special CJ chat menu. and include the bonus evidence
            localAvatar.chatMgr.chatInputSpeedChat.removeCJMenu()
            localAvatar.chatMgr.chatInputSpeedChat.addCJMenu(self.bonusWeight)
            

    def __doneBattleThree(self):
        """
        Done with battle three.
        """
        self.notify.debug("----- __doneBattleThree")

        # We've played the boss damage movie all the way to
        # completion; it's time to transition to the NearVictory state.
        self.setState('NearVictory')
        self.unstickBoss()

    def exitBattleThree(self):
        """
        Done with this state, do cleanup
        """
        self.notify.debug("----- exitBattleThree")
        DistributedBossCog.DistributedBossCog.exitBattleThree(self)
        
        #restore the master arrows
        NametagGlobals.setMasterArrowsOn(1)
        
        bossDoneEventName = self.uniqueName('DestroyedBoss')
        self.ignore(bossDoneEventName)
        # Actually, we'll keep the animation going, so we can continue
        # it in the NearVictory state.
        #self.stopAnimate()

        taskMgr.remove(self.uniqueName('StandUp'))

        # No more pies.
        self.ignore('enterWitnessStand')
        self.ignore('pieSplat')
        self.ignore('localPieSplat')
        self.ignore('outOfPies')
        self.ignore('begin-pie')
        self.ignore('enterDefenseCol')
        self.ignore('enterProsecutionCol')

        
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)


        if self.bossDamageMovie:
            self.bossDamageMovie.finish()
        self.bossDamageMovie = None
        self.unstickBoss()

        taskName = "RecoverBossDamage"
        taskMgr.remove(taskName)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()


    ##### NearVictory state #####

    def enterNearVictory(self):
        """
        Unused in CJ
        """
        assert self.notify.debug('enterNearVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        # Boss Cog is on the edge of the precipice, waiting for that
        # one final pie toss.
        self.reparentTo(render)
        self.setPos(*ToontownGlobals.LawbotBossDeathPos)
        self.setHpr(*ToontownGlobals.LawbotBossBattleThreeHpr)
        self.clearChat()




        # No one owns the toons.
        self.releaseToons(finalBattle = 1)

        # Retract all of the ramps but the back one.


        # We're still in pie mode, for the one more ceremonial toss
        # that sends the boss plummeting to his death.

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
        """
        Unused in CJ
        """
        self.notify.debug("----- exitNearVictory")
        # No more pies.

        self.ignore('pieSplat')
        self.ignore('localPieSplat')
        self.ignore('outOfPies')
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)


        self.setDizzy(0)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()

        # Actually, we'll keep the animation going, so we can continue
        # it in the Victory state.
        #self.stopAnimate()

    ##### Victory state #####

    def enterVictory(self):
        """
        Toons won. Do the CJ lost speech.
        """
        self.notify.debug("----- enterVictory")
        assert self.notify.debug('enterVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleThreePosHpr)
        self.loop('neutral')

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        self.clearChat()
        self.witnessToon.clearChat()


        self.controlToons()
        #don't leave them in the walking state if we take the control away from player
        self.setToonsToNeutral(self.involvedToons)        

        self.happy = 1
        self.raised = 1
        self.forward = 1

        # Play the boss's Defense wins animation.
        #self.doAnimate('Ff_speech', now = 1)

        intervalName = "VictoryMovie"

        seq = Sequence(self.makeVictoryMovie(),
                       Func(self.__continueVictory),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)
                       

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def __continueVictory(self):
        """
        # Ok, he's gone!  We all move to the reward movie.
        """
        self.notify.debug("----- __continueVictory")
        self.stopAnimate()

        self.doneBarrier('Victory')

    def exitVictory(self):
        """
        Done with this state, do cleanup
        """
        self.notify.debug("----- exitVictory")
        self.stopAnimate()
        self.unstash()


        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()


    ##### Defeat state #####

    def enterDefeat(self):
        """
        Prosecution pan went down.  Toons lose.
        """
        self.notify.debug("----- enterDefeat")
        assert self.notify.debug('enterDefeat()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)


        self.reparentTo(render)

        self.clearChat()


        # No one owns the toons.
        self.releaseToons(finalBattle = 1)


        self.happy = 0
        self.raised = 0
        self.forward = 1


        intervalName = "DefeatMovie"

        seq = Sequence(self.makeDefeatMovie(),
                       Func(self.__continueDefeat),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)
                       

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def __continueDefeat(self):
        """
        We're done.
        """
        self.notify.debug("----- __continueDefeat")      
        self.stopAnimate()
        self.doneBarrier('Defeat')

    def exitDefeat(self):
        """
        We're done with this state, do cleanup
        """
        self.notify.debug("----- exitDefeat")
        self.stopAnimate()
        self.unstash()


        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        self.battleThreeMusic.stop()


    ##### Reward state #####

    def enterReward(self):
        """
        Show the reward movie, skillups, questsm etc.
        """
        assert self.notify.debug('enterReward()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.witnessToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()



        # The toons are technically free to run around, but localToon
        # starts out locked down for the reward movie.
        self.controlToons()


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
                delayDeletes.append(DelayDelete.DelayDelete(toon, 'LawbotBoss.enterReward'))
                                    
        ival.delayDeletes = delayDeletes
        ival.start()
        self.storeInterval(ival, intervalName)

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9,
                       time = self.battleThreeMusicTime)

    def __doneReward(self):
        """
        We're done with the reward move
        """
        self.notify.debug("----- __doneReward")
        self.doneBarrier('Reward')
        self.toWalkMode()

    def exitReward(self):
        """
        Exit this state. do cleanup
        """
        self.notify.debug("----- exitReward")
        intervalName = "RewardMovie"
        self.clearInterval(intervalName)

        self.unstash()
        self.rewardPanel.destroy()
        del self.rewardPanel


        self.battleThreeMusicTime = 0
        self.battleThreeMusic.stop()

    ##### Epilogue state #####

    def enterEpilogue(self):
        """
        Enter the epilogue. Witness toon thanks us.
        """
        assert self.notify.debug('enterEpilogue()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.witnessToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()



        # The toons are under our control once again.
        self.controlToons()

        self.__showWitnessToon()
        self.witnessToon.reparentTo(render)
        self.witnessToon.setPosHpr(*ToontownGlobals.LawbotBossWitnessEpiloguePosHpr)
        self.witnessToon.loop('Sit')        
        self.__arrangeToonsAroundWitnessToon()

        camera.reparentTo(render)
        camera.setPos(self.witnessToon, -9, 12, 6)
        camera.lookAt(self.witnessToon, 0, 0, 3)

        intervalName = "EpilogueMovie"

        seq = Sequence(self.makeEpilogueMovie(),
                       name = intervalName)

        seq.start()
        self.storeInterval(seq, intervalName)

        self.accept("doneChatPage", self.__doneEpilogue)

        base.playMusic(self.epilogueMusic, looping=1, volume=0.9)

    def __doneEpilogue(self, elapsedTime = 0):
        """
        Done, teleport to safe zone
        """
        self.notify.debug("----- __doneEpilogue")
        #self.doneBarrier('Epilogue')       

        intervalName = "EpilogueMovieToonAnim"
        self.clearInterval(intervalName)
        track = Parallel(
            Sequence(Wait(0.5),
                     Func(self.localToonToSafeZone)))
        self.storeInterval(track, intervalName)
        track.start()
 

    def exitEpilogue(self):
        """
        Done with this state, cleanup
        """
        self.notify.debug("----- exitEpilogue")
        self.clearInterval("EpilogueMovieToonAnim")
        self.unstash()


        self.epilogueMusic.stop()

            
        

    ##### Frolic state #####

    # This state is probably only useful for debugging.  The toons are
    # all free to run around the world.

    def enterFrolic(self):
        """
        We should only get here through a magic word
        """
        self.notify.debug("----- enterFrolic")
        self.setPosHpr(*ToontownGlobals.LawbotBossBattleOnePosHpr)        
        DistributedBossCog.DistributedBossCog.enterFrolic(self)

        self.show()

    ##### Misc. utility functions #####

    def doorACallback(self, isOpen):
        """
        # Called whenever doorA opens or closes.
        """
        #self.notify.debug("----- doorACallback")
        if self.insidesANodePath:
            if isOpen:
                self.insidesANodePath.unstash()
            else:
                self.insidesANodePath.stash()

    def doorBCallback(self, isOpen):
        """
        # Called whenever doorB opens or closes.
        """
        #self.notify.debug("----- doorBCallback")
        if self.insidesBNodePath:
            if isOpen:
                self.insidesBNodePath.unstash()
            else:
                self.insidesBNodePath.stash()

    def __toonsToPromotionPosition(self, toonIds, battleNode):
        """
        Unused in CJ.
        """
        self.notify.debug("----- __toonsToPromotionPosition")

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
        
        

    def __outOfPies(self):
        """
        Tell the user he needs to get more evidence.
        """
        self.notify.debug("----- outOfPies")
        self.__showOnscreenMessage(TTLocalizer.LawbotBossNeedMoreEvidence)
        taskMgr.doMethodLater(20, self.__howToGetPies,
                              self.uniqueName("PieAdvice"))

    def __howToGetPies(self, task):
        """
        Tell user how to get evidence.
        """
        self.notify.debug("----- __howToGetPies")        
        self.__showOnscreenMessage(TTLocalizer.LawbotBossHowToGetEvidence)

    def __howToThrowPies(self, task):
        """
        Tell the user how to throw the evidence
        """
        self.notify.debug("----- __howToThrowPies")
        self.__showOnscreenMessage(TTLocalizer.LawbotBossHowToThrowPies)

    def __foundPieButton(self):
        """
        He knows how to throw evidence.
        """
        #self.notify.debug("----- __foundPieButton")
        self.everThrownPie = 1
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        
    def __touchedWitnessStand(self,entry):
        """
        The avatar has touched the witness stand. he should be given evidence now.
        """        
        assert self.notify.debug('__touchedWitnessStand')

        #I think we can piggy back of the existing cage and pie code
        #Just change how it's presented to the user
        self.sendUpdate('touchWitnessStand',[])
        self.__clearOnscreenMessage()
        taskMgr.remove(self.uniqueName("PieAdvice"))
        base.playSfx(self.piesRestockSfx)

        if not self.everThrownPie:
            taskMgr.doMethodLater(30, self.__howToThrowPies, self.uniqueName('PieAdvice'))
            
    def __pieSplat(self, toon, pieCode):
        """
        # A pie thrown by localToon or some other toon hit something;
        # show a visible reaction if that something is the boss.
        """
        assert self.notify.debug("__pieSplat()")
        
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

        elif pieCode == ToontownGlobals.PieCodeDefensePan:
            #self.notify.debug("Defense Pan hit")
            self.flashRed()
            self.flashPanBlue()
            #you are going to hear this sound a lot, made it softer
            base.playSfx(self.evidenceHitSfx, node=self.defensePanNodePath,volume = 0.25)
            if (toon == localAvatar):
                self.d_hitBoss(self.panDamage)
                
        elif pieCode == ToontownGlobals.PieCodeProsecutionPan:
            #self.notify.debug("Prosecution Pan Hit")
            self.flashGreen()
            if (toon == localAvatar):
                #don't heal the boss if we hit the prosecution pan
                #self.d_healBoss(ToontownGlobals.LawbotBossDefensePanDamage)
                pass
        elif pieCode == ToontownGlobals.PieCodeLawyer:
            pass
            #self.notify.debug("Lawyer hit")
            #hmmmm I don't have the info I need here, localPieSplat has it
        
    def __localPieSplat(self, pieCode, entry):
        """
        Our local toon threw evidence and hit something
        """
        assert self.notify.debug("__localPieSplat()")

        if pieCode == ToontownGlobals.PieCodeLawyer:
            self.__lawyerGotHit(entry)

        
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


    def __lawyerGotHit(self,entry):
        """
        One of the lawyers got hit, tell the AI
        """
        lawyerCol = entry.getIntoNodePath()
        names = lawyerCol.getName().split('-')
        lawyerDoId = int( names[1] )
        for lawyer in self.lawyers:
            if lawyerDoId == lawyer.doId:
                lawyer.sendUpdate('hitByToon',[])

        
    def __finalPieSplat(self, toon, pieCode):
        """
        Unused in CJ
        """
        assert self.notify.debug("__finalPieSplat()")
        # This is the final pie toss that starts the boss's fall.
        # It's really just a formality, since we're already in the
        # Victory state.
        #if pieCode != ToontownGlobals.PieCodeBossCog:
        if pieCode != ToontownGlobals.PieCodeDefensePan:        
            return

        # Tell the AI; the AI will then immediately transition to Victory
        # state.
        self.sendUpdate('finalPieSplat', [])

        # We don't care to hear any more about pies hitting the boss.
        self.ignore('pieSplat')
        

    def cleanupAttacks(self):
        """
        # Stops any attack currently running.
        """
        self.notify.debug("----- cleanupAttacks")
        self.__cleanupStrafe()

    def __cleanupStrafe(self):
        """
        Unused in CJ
        """
        self.notify.debug("----- __cleanupStrage")
        if self.strafeInterval:
            self.strafeInterval.finish()
            self.strafeInterval = None

    def __cleanupJuryBox(self):
        """
        Cleanup the jury box.
        """
        self.notify.debug("----- __cleanupJuryBox")
        if self.juryBoxIval:
            self.juryBoxIval.finish()
            self.juryBoxIval = None

        if self.juryBox:
            self.juryBox.removeNode()
    

    def doStrafe(self, side, direction):
        """
        Unused in CJ
        """
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



    def replaceCollisionPolysWithPlanes(self, model):
        """
        Make the world a safer place to run around in
        """
        newCollisionNode = CollisionNode('collisions')
        newCollideMask = BitMask32(0)
        planes = []

        collList = model.findAllMatches('**/+CollisionNode')
        if not collList:
            collList = [model]
            
        for cnp in collList:
            cn = cnp.node()
            if not isinstance(cn, CollisionNode):
                self.notify.warning("Not a collision node: %s" % (repr(cnp)))
                break
            
            newCollideMask = newCollideMask | cn.getIntoCollideMask()
            for i in range(cn.getNumSolids()):
                solid = cn.getSolid(i)
                if isinstance(solid, CollisionPolygon):
                    # Save the plane defined by this polygon
                    plane = Plane(solid.getPlane())
                    planes.append(plane)
                else:
                    self.notify.warning("Unexpected collision solid: %s" % (repr(solid)))
                    newCollisionNode.addSolid(plane)

        newCollisionNode.setIntoCollideMask(newCollideMask)
        
        # Now sort all of the planes and remove the nonunique ones.
        # We can't use traditional dictionary-based tricks, because we
        # want to use Plane.compareTo(), not Plane.__hash__(), to make
        # the comparison.
        threshold = 0.1
        planes.sort(lambda p1, p2: p1.compareTo(p2, threshold))
        lastPlane = None
        for plane in planes:
            if lastPlane == None or plane.compareTo(lastPlane, threshold) != 0:
                cp = CollisionPlane(plane)
                newCollisionNode.addSolid(cp)
                lastPlane = plane

        return NodePath(newCollisionNode)

    def makeIntroductionMovie(self, delayDeletes):
        """
        # Generate an interval which shows the toons meeting the
        # Resistance Toon, and the introduction of the CFO, etc.,
        # leading to the events of battle one.
        """

        self.notify.debug("----- makeIntroductionMovie")

        # We need to protect our movie against any of the toons
        # disconnecting while the movie plays.
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete.DelayDelete(
                    toon, 'LawbotBoss.makeIntroductionMovie'))


        track = Parallel()

        bossAnimTrack = Sequence(
            ActorInterval(self, 'Ff_speech', startTime = 2, duration = 10, loop = 1),
            #10
            ActorInterval(self, 'Ff_lookRt', duration = 3),
            #13
            ActorInterval(self, 'Ff_lookRt', duration = 3, startTime =3, endTime = 0),
            #16
            ActorInterval(self, 'Ff_neutral', duration = 2),
            # 18
            ActorInterval(self, 'Ff_speech', duration = 7, loop = 1),
            # 25

            # remaining animations mixed in with camera cuts in
            # dialogTrack.
            )
        track.append(bossAnimTrack)

        attackToons = TTLocalizer.BossCogAttackToons
        
        dialogTrack = Track(
            (0, Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempIntro0, CFSpeech)),            
            
            (5.6, Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempIntro1, CFSpeech)),

            (12, Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempIntro2, CFSpeech)),

            (18, Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempIntro3, CFSpeech)),
                          
            (22, Func(self.setChatAbsolute, TTLocalizer.LawbotBossTempIntro4, CFSpeech)),

            # Cut to toons losing their cog suits.
            (24, Sequence(Func(self.clearChat),
                          self.loseCogSuits(self.toonsA +self.toonsB, render, (-2.798, -70, 10,180,0,0)),
                          )),

            # Cut to wide shot of battle arena.  Toons back up and
            # ramps retract.
            (27, Sequence(self.toonNormalEyes(self.involvedToons),
                          Func(self.loop, 'Ff_neutral'),
                          Func (self.setChatAbsolute, attackToons, CFSpeech)
                          )),
            )
        track.append(dialogTrack)

        return Sequence(Func(self.stickToonsToFloor),
                        track,
                        Func(self.unstickToons),
                        name = self.uniqueName('Introduction'))


       
        
    def walkToonsToBattlePosition(self, toonIds, battleNode):
        """
        Unused in CJ
        # Returns a movie showing the toons walking up from promotion
        # position to battle position.
        """
        self.notify.debug("walkToonsToBattlePosition-----------------------------------------------")
        self.notify.debug("toonIds=%s  battleNode=%s" % (toonIds, battleNode))
        ival = Parallel()

        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]

        self.notify.debug("walkToonsToBattlePosition: points = %s" % (points[0][0]))

        #TODO figure out why we are appearing inside the boss for a brief period of time
        #wrong computed coordinate = 4.9, -16.9, 0
        #correct one  -18.1, -21.9,0
        
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                pos, h = points[i]
                origPos = pos;
                self.notify.debug("origPos = %s" % origPos)
                self.notify.debug("batlleNode.getTransform = %s  render.getTransform=%s" % (battleNode.getTransform(), render.getTransform()))
                self.notify.debug("render.getScale()=%s  battleNode.getScale()=%s" % (render.getScale(), battleNode.getScale()))
                myCurPos = self.getPos()
                self.notify.debug("myCurPos = %s" % self.getPos())
                #pos = pos - self.getPos()
                #self.notify.debug("pos-self.getPos() = %s" % pos)
                self.notify.debug("battleNode.parent() = %s" % battleNode.getParent())
                self.notify.debug("battleNode.parent().getPos() = %s" % battleNode.getParent().getPos())

                bnParent = battleNode.getParent()
                battleNode.wrtReparentTo(render)
                bnWorldPos = battleNode.getPos()
                battleNode.wrtReparentTo(bnParent)

                self.notify.debug("battle node world pos = %s" % bnWorldPos)

                pos = render.getRelativePoint(battleNode, pos)
                #pos = battleNode.getPos() + pos
                self.notify.debug("walktToonsToBattlePosition: render.getRelativePoint result = %s" % pos)                

                #self.notify.debug("doing pos - bnWorldPos")
                #pos = pos - bnWorldPos
                
                self.notify.debug("walkToonsToBattlePosition: final pos = %s" % pos)

                
                ival.append(Sequence(
                    Func(toon.setPlayRate, 0.8, 'walk'),
                    Func(toon.loop, 'walk'),
                    toon.posInterval(3, pos),
                    Func(toon.setPlayRate, 1, 'walk'),
                    Func(toon.loop,'neutral'),
                    ))

        return ival


    def toonsToBattlePosition(self, toonIds, battleNode):
        """
        # Position the toons in the list to their appropriate position
        # relative to the indicated battleNode.
        """

        
        self.notify.debug("DistrutedLawbotBoss.toonsToBattlePosition----------------------------------------")
        self.notify.debug("toonIds=%s battleNode=%s" % (toonIds,battleNode))

        points = BattleBase.BattleBase.toonPoints[len(toonIds) - 1]

        self.notify.debug("toonsToBattlePosition: points = %s" % points[0][0])
        
        for i in range(len(toonIds)):
            toon = base.cr.doId2do.get(toonIds[i])
            if toon:
                toon.wrtReparentTo(render)
                pos, h = points[i]

                #self.notify.debug("points = %.2f %.2f %.2f" % (points[0][0], points[0][1], points[0][2])                
                #self.notify.debug("toonsToBattlePosition: battleNode=%s %.2f %.2f %.2f %.2f %.2f %.2f" % (battleNode, pos[0], pos[1], pos[2], h, 0, 0))

                #self.notify.debug("old toon pos %s" % toon.getPos())
                #self.notify.debug("pos=%.2f %.2f %.2f h=%.2f" % (pos[0], pos[1], pos[2], h))
                #self.notify.debug("battleNode.pos = %s" % battleNode.getPos())
                #self.notify.debug("battleNode.hpr = %s" % battleNode.getHpr())

                bnParent = battleNode.getParent()
                battleNode.wrtReparentTo(render)
                bnWorldPos = battleNode.getPos()
                battleNode.wrtReparentTo(bnParent)

                #pos = pos - bnWorldPos
                #toon.setPosHpr(pos[0],pos[1], pos[2], h, 0, 0)

                toon.setPosHpr(battleNode, pos[0], pos[1], pos[2], h, 0, 0)

                self.notify.debug("new toon pos %s " % toon.getPos())
                

    def touchedGavel( self, gavel, entry):
        """
        # The localToon has come into contact with a gavel head.  Zap!
        """
        self.notify.debug('touchedGavel')

        # Get the attack code from the thing we touched.
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning("Node %s has no attackCode tag." % (repr(entry.getIntoNodePath())))
            return
        
        attackCode = int(attackCodeStr)

        into = entry.getIntoNodePath();
        self.zapLocalToon(attackCode, into)
        
        
    def touchedGavelHandle( self, gavel, entry):
        """
        # The localToon has come into contact with a gavel handle.  Zap!
        """        
        attackCodeStr = entry.getIntoNodePath().getNetTag('attackCode')
        if attackCodeStr == '':
            self.notify.warning("Node %s has no attackCode tag." % (repr(entry.getIntoNodePath())))
            return
        
        attackCode = int(attackCodeStr)

        into = entry.getIntoNodePath();
        self.zapLocalToon(attackCode, into)
        

    def createBlock(self, x1, y1, z1, x2, y2, z2, r=1.0, g=1.0, b=1.0, a=1.0):
        """
        Returns a GeomNode rectangular block with x1,y1,z1 in one corner and x2,y2,z2 in the opposite corner.
        r,g,b,a should range from 0 to 1
        """

        gFormat = GeomVertexFormat.getV3n3cpt2()
        myVertexData = GeomVertexData("holds my vertices", gFormat, Geom.UHDynamic)
        vertexWriter = GeomVertexWriter(myVertexData, "vertex")
        normalWriter = GeomVertexWriter(myVertexData, "normal")
        colorWriter = GeomVertexWriter(myVertexData, "color")
        texWriter = GeomVertexWriter(myVertexData, "texcoord")
        
        #setup the vertexs
        vertexWriter.addData3f(x1, y1, z1)
        vertexWriter.addData3f(x2, y1, z1)
        vertexWriter.addData3f(x1, y2, z1)
        vertexWriter.addData3f(x2, y2, z1)
        vertexWriter.addData3f(x1, y1, z2)
        vertexWriter.addData3f(x2, y1, z2)
        vertexWriter.addData3f(x1, y2, z2)
        vertexWriter.addData3f(x2, y2, z2)
        

        for index in range(8):
            normalWriter.addData3f(1.0, 1.0, 1.0)
            colorWriter.addData4f(r, g, b, a)
            texWriter.addData2f(1.0, 1.0)


        #create geometry and faces
        tris=GeomTriangles(Geom.UHDynamic) # triangle obejcet
        tris.addVertex(0) #top
        tris.addVertex(1)
        tris.addVertex(2)
        tris.closePrimitive()

        tris.addVertex(1)
        tris.addVertex(3)
        tris.addVertex(2)
        tris.closePrimitive()

        tris.addVertex(2) #front
        tris.addVertex(3)
        tris.addVertex(6)
        tris.closePrimitive()

        tris.addVertex(3)
        tris.addVertex(7)
        tris.addVertex(6)
        tris.closePrimitive()

        tris.addVertex(0) #right
        tris.addVertex(2)
        tris.addVertex(4)
        tris.closePrimitive()

        tris.addVertex(2)
        tris.addVertex(6)
        tris.addVertex(4)
        tris.closePrimitive()

        tris.addVertex(1) #left
        tris.addVertex(5)
        tris.addVertex(3)
        tris.closePrimitive()

        tris.addVertex(3)
        tris.addVertex(5)
        tris.addVertex(7)
        tris.closePrimitive()


        tris.addVertex(0) #back
        tris.addVertex(4)
        tris.addVertex(5)
        tris.closePrimitive()

        tris.addVertex(1)
        tris.addVertex(0)
        tris.addVertex(5)
        tris.closePrimitive()


        tris.addVertex(4) #bottom
        tris.addVertex(6)
        tris.addVertex(7)
        tris.closePrimitive()

        tris.addVertex(7)
        tris.addVertex(5)
        tris.addVertex(4)
        tris.closePrimitive()

        
        cubeGeom=Geom(myVertexData)
        cubeGeom.addPrimitive(tris) 

        cubeGN=GeomNode("cube")
        cubeGN.addGeom(cubeGeom)

        return cubeGN

        
    def __enterDefenseCol(self,entry):
        self.notify.debug('__enterDefenseCol')

    def __enterProsecutionCol(self, entry):
        self.notify.debug('__enterProsecutionCol')
        

    def makeVictoryMovie(self):
        """
        Make the victory movie.  
        """

        myFromPos = Point3(ToontownGlobals.LawbotBossBattleThreePosHpr[0],
                         ToontownGlobals.LawbotBossBattleThreePosHpr[1],
                         ToontownGlobals.LawbotBossBattleThreePosHpr[2])
        myToPos = Point3( myFromPos[0],
                        myFromPos[1] + 30,
                        myFromPos[2])

        
        rollThroughDoor = self.rollBossToPoint(
            fromPos = myFromPos, fromHpr = None,
            toPos = myToPos, toHpr = None,
            reverse = 0)
        rollTrack = Sequence(
            Func(self.getGeomNode().setH, 180),
            rollThroughDoor[0],
            Func(self.getGeomNode().setH, 0))

        rollTrackDuration = rollTrack.getDuration()
        self.notify.debug('rollTrackDuration = %f' % rollTrackDuration)


        doorStartPos = self.door3.getPos()
        doorEndPos = Point3(doorStartPos[0], doorStartPos[1], doorStartPos[2] + 25)
        bossTrack = Track (
           (0.5, Sequence( Func(self.clearChat),
                           Func(camera.reparentTo, render),
                           Func(camera.setPos,-3,45,25),
                           Func(camera.setHpr,0,10,0),
                           )),
           (1.0, Func(self.setChatAbsolute, TTLocalizer.LawbotBossDefenseWins1, CFSpeech)),
           (5.5, Func(self.setChatAbsolute, TTLocalizer.LawbotBossDefenseWins2, CFSpeech)),
           (9.5, Sequence( Func (camera.wrtReparentTo, render),
                           )),
           (9.6, Parallel( rollTrack,                           
                           Func(self.setChatAbsolute, TTLocalizer.LawbotBossDefenseWins3, CFSpeech),
                           self.door3.posInterval(2, doorEndPos,
                                                  startPos = doorStartPos),
                           )),
            (13.1, Sequence(self.door3.posInterval(1, doorStartPos))),
                                
           )

        retTrack = Parallel(bossTrack,
                            ActorInterval(self,'Ff_speech',loop=1)
                            )
        return bossTrack
        #return retTrack
    
    def makeEpilogueMovie(self):
        """
        Make the epilogue movie.  
        """


        epSpeech = TTLocalizer.WitnessToonCongratulations
        
        epSpeech = self.__talkAboutPromotion(epSpeech)
        
        bossTrack = Sequence (
           Func(self.witnessToon.animFSM.request,'neutral'),
           Func(self.witnessToon.setLocalPageChat,epSpeech, 0)
           )
        return bossTrack


    def makeDefeatMovie(self):
        """
        Make the defeat movie.  
        """
        bossTrack = Track (
           (0.0, Sequence( Func(self.clearChat),
                           Func(self.reverseHead),
                           ActorInterval(self,'Ff_speech'))),
           (1.0, Func(self.setChatAbsolute, TTLocalizer.LawbotBossProsecutionWins, CFSpeech))
           )
        return bossTrack
        
    def __makeWitnessToon(self):
        """
        Make the npc witness.
        
        dnaNetString came from making a player
        type = toon
        gender = m
        head = bss, torso = ss, legs = m
        arm color = 19
        glove color = 0
        leg color = 19
        head color = 19
        top texture = 0
        top texture color = 3
        sleeve texture = 0
        sleeve texture color = 3
        bottom texture = 1
        bottom texture color = 16
        """
        
        dnaNetString = 't\x1b\x00\x01\x01\x00\x03\x00\x03\x01\x10\x13\x00\x13\x13'

        npc = Toon.Toon()
        npc.setDNAString( dnaNetString)
        npc.setName(TTLocalizer.WitnessToonName)
        npc.setPickable(0)
        npc.setPlayerType(NametagGroup.CCNonPlayer)
        #npc.animFSM.request('neutral')
        npc.animFSM.request('Sit')

        self.witnessToon = npc
        self.witnessToon.setPosHpr(*ToontownGlobals.LawbotBossWitnessStandPosHpr)
        

    def __cleanupWitnessToon(self):
        """
        Cleanup the witness toon
        """
        self.__hideWitnessToon()
        if self.witnessToon:
            self.witnessToon.removeActive()
            self.witnessToon.delete()
            self.witnessToon = None

        
    def __showWitnessToon(self):
        """
        Show the witness toon seated on the witness stand
        """
        if not self.witnessToonOnstage:
            self.witnessToon.addActive()
            self.witnessToon.reparentTo(self.geom)
            seatCenter = self.realWitnessStand.find('**/witnessStandSeatEdge')
            center = seatCenter.getPos()
            self.notify.debug('center = %s' % center)
            self.witnessToon.setPos(center)
            self.witnessToon.setH(180)
            self.witnessToon.setZ(self.witnessToon.getZ() - 1.5)
            self.witnessToon.setY(self.witnessToon.getY() - 1.15)
            self.witnessToonOnstage = 1

    def __hideWitnessToon(self):
        """
        Hide the witness toon
        """
        if self.witnessToonOnstage:
            self.witnessToon.removeActive()
            self.witnessToon.detachNode()
            self.witnessToonOnstage = 0

    def __hideToons(self):
        """
        Hide the toons
        """
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.hide()

    def __showToons(self):
        """
        Show the toons
        """
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.show()

    def __arrangeToonsAroundWitnessToon(self):
        """
        Arrange the toons around the witness toon
        """
        radius = 7
        numToons = len(self.involvedToons)
        center = (numToons - 1) / 2.0
        for i in range(numToons):
            toon = self.cr.doId2do.get(self.involvedToons[i])
            if toon:
                angle = 90 - 15 * (i - center)

                radians = angle * math.pi / 180.0
                x = math.cos(radians) * radius
                y = math.sin(radians) * radius
                toon.setPos(self.witnessToon, x, y, 0)
                toon.headsUp(self.witnessToon)
                toon.loop('neutral')
                toon.show()


    def __talkAboutPromotion(self, speech):
        """
        # Extends the congratulations speech to talk about the earned
        # promotion, if any.  Returns the newly-extended speech.
        """
        
        # don't say anything about a promotion if they've maxed their cog suit
        if self.prevCogSuitLevel < ToontownGlobals.MaxCogSuitLevel:
            newCogSuitLevel = localAvatar.getCogLevels()[
                CogDisguiseGlobals.dept2deptIndex(self.style.dept)]
            # if this is their last promotion, tell them
            if newCogSuitLevel == ToontownGlobals.MaxCogSuitLevel:
                speech += TTLocalizer.WitnessToonLastPromotion % (ToontownGlobals.MaxCogSuitLevel+1)
            # if they're getting another LP, tell them
            if newCogSuitLevel in ToontownGlobals.CogSuitHPLevels:
                speech += TTLocalizer.WitnessToonHPBoost
        else:
            # level XX, wow! Thanks for coming back!
            speech += TTLocalizer.WitnessToonMaxed % (ToontownGlobals.MaxCogSuitLevel+1)

        return speech
    

    def __positionToonsInFrontOfCannons(self):
        """
        Put the toons in front of the cannons
        """
        self.notify.debug('__positionToonsInFrontOfCannons')
        index = 0

        self.involvedToons.sort()        
        for toonId in self.involvedToons:
            if self.cannons.has_key(index):
                cannon = self.cannons[index]
                toon = self.cr.doId2do.get(toonId)

                self.notify.debug('cannonId = %d' % cannon.doId)
                cannonPos = cannon.nodePath.getPos(render)
                self.notify.debug('cannonPos = %s' % cannonPos)
                if toon:
                    self.notify.debug('toon = %s' % toon.getName())                
                    toon.reparentTo(cannon.nodePath)
                    toon.setPos(0,8,0)
                    toon.setH(180)
                    renderPos = toon.getPos(render)
                    self.notify.debug('renderPos =%s' % renderPos)
                    index += 1
                          
        self.notify.debug('done with positionToons')
        
        
    def __makePrepareBattleTwoMovie(self):
        """
        move camera to witness toon and make him talk
        """
        chatString = TTLocalizer.WitnessToonPrepareBattleTwo % ToontownGlobals.LawbotBossJurorsForBalancedScale

        movie = Sequence(
            Func(camera.reparentTo,self.witnessToon),
            Func(camera.setPos,0,8,2),
            Func(camera.setHpr,180,10,0),
            Func(self.witnessToon.setLocalPageChat,chatString, 0),
            
#            Wait(10000),
            #Func(camera.reparentTo, localAvatar),
            #Func(camera.setPos, localAvatar.cameraPositions[0][0]),
            #Func(camera.setHpr, 0, 0, 0),
            #allCannonsAppear,            
        )
        return movie

    def __doWitnessPrepareBattleThreeChat(self):
        """
        Talk about the jury result, and advice, and bonus weight
        """
        self.notify.debug('__doWitnessPrepareBattleThreeChat: original self.numToonJurorsSeated = %d' % self.numToonJurorsSeated)
        self.countToonJurors()
        self.notify.debug("after calling self.countToonJurors, numToonJurorsSeated=%d" % self.numToonJurorsSeated)
        if self.numToonJurorsSeated == 0:
            juryResult = TTLocalizer.WitnessToonNoJuror
        elif self.numToonJurorsSeated == 1:
            juryResult = TTLocalizer.WitnessToonOneJuror            
        elif self.numToonJurorsSeated == 12:
            juryResult = TTLocalizer.WitnessToonAllJurors            
        else:
            juryResult = TTLocalizer.WitnessToonSomeJurors % self.numToonJurorsSeated

        juryResult += '\a'

        trialSpeech = juryResult           
        
        trialSpeech += TTLocalizer.WitnessToonPrepareBattleThree

        #insert the text about the bonus weight from toon jurors
        diffSettings = ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
        if diffSettings[4]:
            #ok so we have toon jurors affecting the weight
            newWeight, self.bonusWeight, self.numJurorsLocalToonSeated = self.calculateWeightOfToon(base.localAvatar.doId)
            if self.bonusWeight > 0:
                if self.bonusWeight == 1:
                    juryWeightBonus = TTLocalizer.WitnessToonJuryWeightBonusSingular.get(self.battleDifficulty)
                else:
                    juryWeightBonus = TTLocalizer.WitnessToonJuryWeightBonusPlural.get(self.battleDifficulty)
                if juryWeightBonus:
                    weightBonusText = juryWeightBonus % (self.numJurorsLocalToonSeated, self.bonusWeight)
                    trialSpeech += '\a'
                    trialSpeech += weightBonusText
            
        

        
        self.witnessToon.setLocalPageChat(trialSpeech,0)


    def __makePrepareBattleThreeMovie(self):
        """
        move camera to witness toon and make him talk
        """
 
        movie = Sequence(
            Func(camera.reparentTo, render),
            Func(camera.setPos, -15, 15, 20),
            Func(camera.setHpr, -90,0,0),
            Wait(3),
            Func(camera.reparentTo,self.witnessToon),
            Func(camera.setPos,0,8,2),
            Func(camera.setHpr,180,10,0),
            Func(self.__doWitnessPrepareBattleThreeChat),
            #Func(self.witnessToon.setLocalPageChat,trialSpeech, 0)
            
#            Wait(10000),
#            Func(camera.reparentTo, localAvatar),
#            Func(camera.setPos, localAvatar.cameraPositions[0][0]),
#            Func(camera.setHpr, 0, 0, 0),
        )
        return movie

    def countToonJurors(self):
        """
        run through all the chairs we have and count how many are toons
        """
        self.numToonJurorsSeated = 0
        for key in self.chairs.keys():
            chair = self.chairs[key]
            if chair.state == 'ToonJuror' or \
               (chair.state == None and chair.newState == 'ToonJuror'):
                self.numToonJurorsSeated += 1
                #self.notify.debug('self.numToonJurorsSeated = %d' % self.numToonJurorsSeated)
            
        self.notify.debug('self.numToonJurorsSeated = %d' % self.numToonJurorsSeated)
        
    def cleanupPanFlash(self):
        """
        Cleanup the blue flash
        """
        if self.panFlashInterval:
            self.panFlashInterval.finish()
            self.panFlashInterval = None

    def flashPanBlue(self):
        """
        # Flash the pan blue to emphasize that it's been hit.
        """
        self.cleanupPanFlash()

        intervalName = "FlashPanBlue"
        self.defensePanNodePath.setColorScale(1, 1, 1, 1)
        seq = Sequence(self.defensePanNodePath.colorScaleInterval(0.1, colorScale = VBase4(0, 0, 1, 1)),
                     self.defensePanNodePath.colorScaleInterval(0.3, colorScale = VBase4(1, 1, 1, 1)),
                       name = intervalName)
        self.panFlashInterval = seq
        seq.start()
        self.storeInterval(seq, intervalName)

    def saySomething(self, chatString):
        """
        Make the CJ say something
        """
        intervalName = "ChiefJusticeTaunt"
        seq = Sequence( name = intervalName)
        seq.append(Func(self.setChatAbsolute, chatString, CFSpeech))
        seq.append( Wait(4.0) )
        seq.append(Func(self.clearChat))
        oldSeq = self.activeIntervals.get(intervalName)
        if oldSeq:
           oldSeq.finish()
        seq.start()          
        self.storeInterval(seq, intervalName)
        

    def setTaunt(self, tauntIndex, extraInfo):
        """
        Make the CJ do a taunt
        """
        gotError = False
        if not hasattr(self, 'state'):
            self.notify.warning('returning from setTaunt, no attr state')
            gotError = True
        else:
            if not self.state == 'BattleThree':
                self.notify.warning('returning from setTaunt, not in battle three state, state=%s',self.state)
                gotError = True

        if not hasattr(self, 'nametag'):
            self.notify.warning('returning from setTaunt, no attr nametag')
            gotError = True

        if gotError:
            st = StackTrace()
            print st
            return

        
        chatString = TTLocalizer.LawbotBossTaunts[1]
        if tauntIndex == 0:
            if extraInfo < len(self.involvedToons):
                toonId = self.involvedToons[extraInfo]
                toon = base.cr.doId2do.get(toonId)
                if toon:
                    chatString = TTLocalizer.LawbotBossTaunts[tauntIndex] % toon.getName()
        else:
            chatString = TTLocalizer.LawbotBossTaunts[tauntIndex]
        
        self.saySomething(chatString)

        
        
    def toonGotHealed(self, toonId):
        """
        A toon got healed, play a sound effect
        """
        toon = base.cr.doId2do.get(toonId)
        if toon:
            base.playSfx(self.toonUpSfx, node = toon)

    def hideBonusTimer(self):
        """
        Hide the bonus timer
        """
        if self.bonusTimer:
            self.bonusTimer.hide()

    def enteredBonusState(self):
        """
        We've entered the bonus timer
        """
        self.witnessToon.clearChat()
        text = TTLocalizer.WitnessToonBonus %(
            ToontownGlobals.LawbotBossBonusWeightMultiplier,
            ToontownGlobals.LawbotBossBonusDuration)
        self.witnessToon.setChatAbsolute(text, CFSpeech | CFTimeout)

        base.playSfx(self.toonUpSfx)

        #setup bonus timer
        if not self.bonusTimer:
            self.bonusTimer = ToontownTimer.ToontownTimer()
            self.bonusTimer.posInTopRightCorner()
        self.bonusTimer.show()
        self.bonusTimer.countdown(ToontownGlobals.LawbotBossBonusDuration, self.hideBonusTimer)


    def setAttackCode(self, attackCode, avId = 0):
        """
        Give the toons a warning sound, and a different taunt
        """
        DistributedBossCog.DistributedBossCog.setAttackCode(self,attackCode, avId)
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.saySomething(TTLocalizer.LawbotBossAreaAttackTaunt)
            base.playSfx(self.warningSfx)

    def setBattleDifficulty(self, diff):
        """
        We got the battle difficulty from the AI
        """
        self.notify.debug('battleDifficulty = %d' % diff)
        self.battleDifficulty = diff


    def toonEnteredCannon(self, toonId, cannonIndex):
        """
        Gets called from DistributedLawbotCannon, keep track which
        cannon a toon entered
        """
        if base.localAvatar.doId == toonId:
            self.cannonIndex = cannonIndex

    def numJurorsSeatedByCannon( self, cannonIndex):
        """
        how many jurors were seated by a certain cannon
        """
        retVal = 0
        for chair in self.chairs.values():
            if chair.state == "ToonJuror":
                if chair.toonJurorIndex == cannonIndex:
                    retVal +=1
        return retVal
                             

    def calculateWeightOfToon(self, toonId):
        """
        calculate evidence weight each toon throws, Warning this code
        is duplicated on the server side, update that too if we change this.
        """
        defaultWeight = 1
        bonusWeight = 0
        newWeight = 1
        cannonIndex = self.cannonIndex
        numJurors = 0
        if not cannonIndex == None and cannonIndex >= 0:
            diffSettings =  ToontownGlobals.LawbotBossDifficultySettings[self.battleDifficulty]
            if diffSettings[4]:
                numJurors = self.numJurorsSeatedByCannon( cannonIndex)
                bonusWeight = numJurors - diffSettings[5]
                if bonusWeight < 0:
                    bonusWeight = 0 


            newWeight = defaultWeight + bonusWeight
            self.notify.debug('toon %d has weight of %d' % (toonId, newWeight))
            
        return newWeight, bonusWeight, numJurors
