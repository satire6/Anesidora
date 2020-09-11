import math
import random
from pandac.PandaModules import NametagGroup, CFSpeech, VBase3, CollisionPlane, \
     CollisionNode, CollisionSphere, CollisionTube, NodePath, Plane, Vec3, Vec2,\
     Point3, BitMask32, CollisionHandlerEvent, TextureStage, VBase4, BoundingSphere
from direct.interval.IntervalGlobal import Sequence, Wait, Func, LerpHprInterval, \
     Parallel, LerpPosInterval, Track, ActorInterval, ParallelEndTogether, \
     LerpFunctionInterval, LerpScaleInterval, LerpPosHprInterval, SoundInterval
from direct.task import Task
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.showbase import PythonUtil
from direct.task import Task
from toontown.distributed import DelayDelete
from toontown.toonbase import ToontownGlobals
from toontown.suit import  DistributedBossCog
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.suit import SuitDNA
from toontown.toon import Toon
from toontown.toon import ToonDNA
from toontown.building import ElevatorConstants
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownBattleGlobals
from toontown.battle import RewardPanel
from toontown.battle import MovieToonVictory
from toontown.coghq import CogDisguiseGlobals
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.effects import DustCloud

# This pointer keeps track of the one DistributedBossbotBoss that
# should appear within the avatar's current visibility zones.  If
# there is more than one DistributedSellbotBoss visible to a client at
# any given time, something is wrong.
OneBossCog = None

TTL = TTLocalizer
class DistributedBossbotBoss(DistributedBossCog.DistributedBossCog, FSM.FSM):
    """
    Heavily adapted from DistributedLawbotBoss.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossbotBoss')
    BallLaunchOffset = Point3(10.5, 8.5, -5)

    def __init__(self, cr):
        """Initialize most fields to zero or None."""
        self.notify.debug("----- __init___")
        DistributedBossCog.DistributedBossCog.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedBossbotBoss')
        self.bossDamage = 0
        self.bossMaxDamage = ToontownGlobals.BossbotBossMaxDamage
        # lets us know values on how to open the elevator
        self.elevatorType = ElevatorConstants.ELEVATOR_BB

        # the resistance toon who guides us
        self.resistanceToon = None
        self.resistanceToonOnstage = 0

        self.battleANode.setPosHpr(*ToontownGlobals.WaiterBattleAPosHpr)
        self.battleBNode.setPosHpr(*ToontownGlobals.WaiterBattleBPosHpr)

        # keep track if the toons are carrying food or not
        self.toonFoodStatus = {}

        # reference to the food belts amd tables
        self.belts = [None,None]
        self.tables = {}
        self.golfSpots = {}

        self.servingTimer = None
        self.notDeadList = None
        self.moveTrack = None

        self.speedDamage = 0
        self.maxSpeedDamage = ToontownGlobals.BossbotMaxSpeedDamage
        self.speedRecoverRate = 0
        self.speedRecoverStartTime = 0
        self.ballLaunch = None
        self.moveTrack = None
        self.lastZapLocalTime = 0
        self.numAttacks = 0
        
    def announceGenerate(self):
        """Handle all required fields having been filled in."""
        DistributedBossCog.DistributedBossCog.announceGenerate(self)
        self.loadEnvironment()
        self.__makeResistanceToon()

        # Enable the special CEO chat menu.
        localAvatar.chatMgr.chatInputSpeedChat.addCEOMenu()

        global OneBossCog
        if OneBossCog != None:
            self.notify.warning("Multiple BossCogs visible.")
        OneBossCog = self

        # Anything in the world we hit that's *not* the BossCog
        # inherits this global pieCode, so the splat will be colored
        # gray.
        render.setTag('pieCode', str(ToontownGlobals.PieCodeNotBossCog))

        # make collisions with this boss do more damage
        self.setTag('attackCode', str(ToontownGlobals.BossCogGolfAttack))

        # Make another bubble--a tube--to serve as a target in battle
        # four.
        target = CollisionTube(0, -2, -2, 0, -1, 9, 4.0)
        targetNode = CollisionNode('BossZap')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.targetNodePath = self.pelvis.attachNewNode(targetNode)
        self.targetNodePath.setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))

        # mark the other collision piece set up in the base class with a pie code
        self.axle.getParent().setTag('pieCode', str(ToontownGlobals.PieCodeBossCog))
        
        # He also gets a disk-shaped shield around his little cog hula
        # hoop.
        disk = loader.loadModel('phase_9/models/char/bossCog-gearCollide')
        disk.find('**/+CollisionNode').setName('BossZap')
        disk.reparentTo(self.pelvis)
        disk.setZ(0.8)        

        # Put a small trigger bubble around the cog so we can tell the
        # AI when the boss touches a table
        closeBubble = CollisionSphere(0, 0, 0, 10)
        closeBubble.setTangible(0)
        closeBubbleNode = CollisionNode('CloseBoss')
        closeBubbleNode.setIntoCollideMask(BitMask32(0))
        closeBubbleNode.setFromCollideMask(ToontownGlobals.BanquetTableBitmask)
        closeBubbleNode.addSolid(closeBubble)
        self.closeBubbleNode = closeBubbleNode
        self.closeHandler = CollisionHandlerEvent()
        self.closeHandler.addInPattern('closeEnter')
        #self.closeHandler.addInPattern('closeEnter-%in')
        self.closeHandler.addOutPattern('closeExit')
        #self.closeHandler.addOutPattern('closeExit-%out')
        self.closeBubbleNodePath = self.attachNewNode(closeBubbleNode)
        base.cTrav.addCollider( self.closeBubbleNodePath, self.closeHandler),        
        self.accept('closeEnter', self.closeEnter)
        self.accept('closeExit', self.closeExit)

        # get a handle to the treads so we can show speed damage
        #import pdb; pdb.set_trace()
        self.treads = self.find('**/treads')

        demotedCeo = Suit.Suit()
        demotedCeo.dna = SuitDNA.SuitDNA()
        demotedCeo.dna.newSuit('f')
        demotedCeo.setDNA(demotedCeo.dna)
        demotedCeo.reparentTo(self.geom)
        demotedCeo.loop('neutral')
        demotedCeo.stash()
        self.demotedCeo = demotedCeo

        self.bossClub = loader.loadModel('phase_12/models/char/bossbotBoss-golfclub')
        overtimeOneClubSequence= Sequence(
            self.bossClub.colorScaleInterval(0.1, colorScale = VBase4(0, 1, 0, 1)),
            self.bossClub.colorScaleInterval(0.3, colorScale = VBase4(1, 1, 1, 1)))
        overtimeTwoClubSequence= Sequence(
            self.bossClub.colorScaleInterval(0.1, colorScale = VBase4(1, 0, 0, 1)),
            self.bossClub.colorScaleInterval(0.3, colorScale = VBase4(1, 1, 1, 1)))
        self.bossClubIntervals = [overtimeOneClubSequence, overtimeTwoClubSequence] 
        self.rightHandJoint = self.find('**/joint17')

        self.setPosHpr(*ToontownGlobals.BossbotBossBattleOnePosHpr)
        self.reparentTo(render)

        self.toonUpSfx = loader.loadSfx('phase_11/audio/sfx/LB_toonup.mp3')
        self.warningSfx = loader.loadSfx('phase_5/audio/sfx/Skel_COG_VO_grunt.mp3')
        self.swingClubSfx = loader.loadSfx('phase_5/audio/sfx/SA_hardball.mp3')
        self.moveBossTaskName = "CEOMoveTask"        
        
    def disable(self):
        """Remove this object from active duty.
        
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        self.notify.debug("----- disable")
        DistributedBossCog.DistributedBossCog.disable(self)
        self.demotedCeo.delete()
        base.cTrav.removeCollider(self.closeBubbleNodePath)
        taskMgr.remove('RecoverSpeedDamage')
        self.request('Off')
        self.unloadEnvironment()
        self.__cleanupResistanceToon()
        if self.servingTimer:
            self.servingTimer.destroy()
            del self.servingTimer

        localAvatar.chatMgr.chatInputSpeedChat.removeCEOMenu()

        global OneBossCog
        if OneBossCog == self:
            OneBossCog = None

        self.promotionMusic.stop()
        self.betweenPhaseMusic.stop()
        self.phaseTwoMusic.stop()
        self.phaseFourMusic.stop()
        self.interruptMove()
        for ival in self.bossClubIntervals:
            ival.finish()
        self.belts = []
        self.tables = {}
        self.removeAllTasks()

    ##### Environment #####

    def loadEnvironment(self):
        """Load most of the assets used in the battle."""
        self.notify.debug("----- loadEnvironment")
        DistributedBossCog.DistributedBossCog.loadEnvironment(self)
        self.geom = loader.loadModel('phase_12/models/bossbotHQ/BanquetInterior_1')

        # do elevator
        self.elevatorEntrance = self.geom.find('**/elevator_origin')
        elevatorModel = loader.loadModel("phase_12/models/bossbotHQ/BB_Inside_Elevator")
        if not elevatorModel:
            # something went wrong, try the outside elevator
            elevatorModel = loader.loadModel("phase_12/models/bossbotHQ/BB_Elevator")
        elevatorModel.reparentTo(self.elevatorEntrance)
        self.setupElevator(elevatorModel)
        self.banquetDoor = self.geom.find('**/door3')

        # Also, put a big plane across the universe a few feet below
        # the floor, to catch things that fall out of the world.
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)        

        self.geom.reparentTo(render)

        # before battles: play the boss theme music
        self.promotionMusic = base.loadMusic(
            'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
            # 'phase_9/audio/bgm/encntr_head_suit_theme.mid')

        # Between  major phases, play the upbeat street battle music
        self.betweenPhaseMusic = base.loadMusic(
            'phase_9/audio/bgm/encntr_toon_winning.mid')
        # Battle two: play new jury music  
        self.phaseTwoMusic = base.loadMusic(
            'phase_12/audio/bgm/BossBot_CEO_v1.mid')
        self.phaseFourMusic = base.loadMusic(
           'phase_12/audio/bgm/BossBot_CEO_v2.mid')

        self.pickupFoodSfx = loader.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.mp3')
        self.explodeSfx = loader.loadSfx('phase_4/audio/sfx/firework_distance_02.mp3')

    def unloadEnvironment(self):
        """Unload the environment, also call base class unload."""
        self.notify.debug("----- unloadEnvironment")

        # remove belt and ball models
        for belt in self.belts:
            if belt:
                belt.cleanup()
        for spot in self.golfSpots.values():
            if spot:
                spot.cleanup()
        self.golfSpots = {}
        self.geom.removeNode()
        del self.geom

        DistributedBossCog.DistributedBossCog.unloadEnvironment(self)
 
    def __makeResistanceToon(self):
        """Generate the resistance toon.
        
        Generates the Resistance Toon (tm), who will be our initial
        guide and then callously abandon us to our fate.
        """
        assert self.notify.debugStateCall(self)
        if self.resistanceToon:
            return

        npc = Toon.Toon()
        npc.setName(TTLocalizer.BossbotResistanceToonName)
        npc.setPickable(0)
        npc.setPlayerType(NametagGroup.CCNonPlayer)
        dna = ToonDNA.ToonDNA()
        dna.newToonRandom(11237, 'm', 1)
        dna.head = "sls"
        npc.setDNAString(dna.makeNetString())

        npc.animFSM.request("neutral")
        npc.loop('neutral')

        self.resistanceToon = npc
        self.resistanceToon.setPosHpr(*ToontownGlobals.BossbotRTIntroStartPosHpr)

        # determine a random suit to put him in
        state = random.getstate()
        random.seed(self.doId)
        self.resistanceToon.suitType = SuitDNA.getRandomSuitByDept("c")
        # test movies with the smalles and biggest suit types!
        #self.resistanceToon.suitType = 'mm' 
        #self.resistanceToon.suitType = 'tbc'
        random.setstate(state)

    def __cleanupResistanceToon(self):
        """Delete the resistance toon."""
        assert self.notify.debugStateCall(self)
        self.__hideResistanceToon()
        if self.resistanceToon:
            self.resistanceToon.takeOffSuit()
            self.resistanceToon.removeActive()
            self.resistanceToon.delete()
            self.resistanceToon = None

    def __showResistanceToon(self, withSuit):
        """Show the resistance toon."""
        assert self.notify.debugStateCall(self)
        if not self.resistanceToonOnstage:
            self.resistanceToon.addActive()
            self.resistanceToon.reparentTo(self.geom)
            self.resistanceToonOnstage = 1

        if withSuit:
            suit = self.resistanceToon.suitType
            self.resistanceToon.putOnSuit(suit, False)
        else:
            self.resistanceToon.takeOffSuit()

    def __hideResistanceToon(self):
        """Hide the resistance toon."""
        assert self.notify.debugStateCall(self)
        if self.resistanceToonOnstage:
            self.resistanceToon.removeActive()
            self.resistanceToon.detachNode()
            self.resistanceToonOnstage = 0

    ##### Elevator state #####

    def enterElevator(self):
        """Handle entering the elevator state."""
        DistributedBossCog.DistributedBossCog.enterElevator(self)

        # Disable the resistance toon's nametag while we're in the
        # elevator.
        self.resistanceToon.removeActive()
        self.__showResistanceToon(True)
        self.resistanceToon.suit.loop('neutral')

        # force the camera to a certain position, to avoid the 1 frame flash
        base.camera.setPos(0,21,7)

        # for now show the CEO
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.BossbotBossBattleOnePosHpr)
        self.loop('Ff_neutral')
        self.show()
         
    #### Intro ####
    def enterIntroduction(self):
        """Enter the intro state."""
        if not self.resistanceToonOnstage:
            self.__showResistanceToon(True)
        DistributedBossCog.DistributedBossCog.enterIntroduction(self)
        base.playMusic(self.promotionMusic, looping=1, volume=0.9)

    def exitIntroduction(self):
        """Exit the intro state."""
        DistributedBossCog.DistributedBossCog.exitIntroduction(self)
        self.promotionMusic.stop()

    def makeIntroductionMovie(self, delayDeletes):
        """Generate an interval which shows the toons meeting the Resistance Toon, etc."""
        rToon = self.resistanceToon
        rToonStartPos = Point3(ToontownGlobals.BossbotRTIntroStartPosHpr[0],
                               ToontownGlobals.BossbotRTIntroStartPosHpr[1],
                               ToontownGlobals.BossbotRTIntroStartPosHpr[2])
        rToonEndPos = rToonStartPos + Point3(40, 0, 0)
        elevCamPosHpr  = ToontownGlobals.BossbotElevCamPosHpr
        closeUpRTCamPos = Point3(elevCamPosHpr[0],
                                 elevCamPosHpr[1],
                                 elevCamPosHpr[2])
        closeUpRTCamHpr = Point3(elevCamPosHpr[3],
                                 elevCamPosHpr[4],
                                 elevCamPosHpr[5])
        closeUpRTCamPos.setY(closeUpRTCamPos.getY() + 20)
        closeUpRTCamPos.setZ(closeUpRTCamPos.getZ() + -2)
        closeUpRTCamHpr = Point3(0,5,0)

        loseSuitCamPos = Point3(rToonStartPos)
        loseSuitCamPos += Point3(0,-5,4)
        loseSuitCamHpr = Point3(180,0,0)

        waiterCamPos = Point3(rToonStartPos)
        waiterCamPos += Point3(-5,-10,5)
        waiterCamHpr = Point3(-30,0,0)
        
        track =Sequence(
            #Cut to resistance toon
            Func(camera.reparentTo, render),
            Func(camera.setPosHpr, *elevCamPosHpr),
            Func(rToon.setChatAbsolute, TTL.BossbotRTWelcome, CFSpeech),
            LerpPosHprInterval(camera, 3, closeUpRTCamPos, closeUpRTCamHpr),
            #Wait(3),
            Func(rToon.setChatAbsolute, TTL.BossbotRTRemoveSuit, CFSpeech),
            Wait(3),

            # Cut to toons losing their cog suits.
            Func(self.clearChat),
            self.loseCogSuits(self.toonsA + self.toonsB, render,
                              (loseSuitCamPos[0], loseSuitCamPos[1], loseSuitCamPos[2],
                               loseSuitCamHpr[0], loseSuitCamHpr[1], loseSuitCamHpr[2])),
            #clean up the toons' eyes
            self.toonNormalEyes(self.involvedToons),
            #self.toonNormalEyes([self.resistanceToon], True),
            Wait(2),

            # Resistance toon tells them to fight the waiters, and walks away
            Func(camera.setPosHpr, closeUpRTCamPos, closeUpRTCamHpr),
            Func(rToon.setChatAbsolute, TTL.BossbotRTFightWaiter, CFSpeech),
            Wait(1),
            LerpHprInterval(camera, 2, Point3(-15,5,0)),
            #Wait(3),
            Sequence(Func(rToon.suit.loop, 'walk'),
                     rToon.hprInterval(1, VBase3(270, 0, 0)),  #turn him around
                     rToon.posInterval(2.5, rToonEndPos),
                     Func(rToon.suit.loop, 'neutral')
                     ),
            Wait(3),
            Func(rToon.clearChat),
            Func(self.__hideResistanceToon)
            )
        return track


    ##### Frolic state #####

    # This state is probably only useful for debugging.  The toons are
    # all free to run around the world.

    def enterFrolic(self):
        """Handle entering the frolic state.
        
        We should only get here through a magic word
        """
        self.notify.debug("----- enterFrolic")
        self.setPosHpr(*ToontownGlobals.BossbotBossBattleOnePosHpr)        
        DistributedBossCog.DistributedBossCog.enterFrolic(self)
        self.show()

    ##### PrepareBattleTwo state #####

    def enterPrepareBattleTwo(self):
        """Do the pre phase 2 movie.

        The Clients will see the toons donning waiter disguise.
        CEO will make brief appearing demanding food.
        Resistance toons says give them food till they explode.
        Walk toons through door
        Close door        
        """
        self.controlToons()
        self.setToonsToNeutral(self.involvedToons)
        # remove the disguise, so we can quickly get here riding up the elevator
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.takeOffSuit()
        self.__showResistanceToon(True)
        self.resistanceToon.setPosHpr(*ToontownGlobals.BossbotRTPreTwoPosHpr)
        self.__arrangeToonsAroundResistanceToon()

        intervalName = "PrepareBattleTwoMovie"
        delayDeletes = []
        seq = Sequence(self.makePrepareBattleTwoMovie(delayDeletes),
                       Func(self.__onToBattleTwo),
                       name = intervalName)
        seq.delayDeletes = delayDeletes
        seq.start()
        self.storeInterval(seq, intervalName)
        base.playMusic(self.betweenPhaseMusic, looping=1, volume=0.9) 

    def makePrepareBattleTwoMovie(self, delayDeletes):
        """Create and return the pre battle two movie."""
        # We need to protect our movie against any of the toons
        # disconnecting while the movie plays.
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete.DelayDelete(
                    toon, 'BossbotBoss.makePrepareBattleTwoMovie'))
        
        rToon = self.resistanceToon
        rToonStartPos = Point3(ToontownGlobals.BossbotRTPreTwoPosHpr[0],
                               ToontownGlobals.BossbotRTPreTwoPosHpr[1],
                               ToontownGlobals.BossbotRTPreTwoPosHpr[2])
        rToonEndPos = rToonStartPos + Point3(-40, 0, 0)

        bossPos = Point3(ToontownGlobals.BossbotBossPreTwoPosHpr[0],
                         ToontownGlobals.BossbotBossPreTwoPosHpr[1],
                         ToontownGlobals.BossbotBossPreTwoPosHpr[2])
        bossEndPos = Point3(ToontownGlobals.BossbotBossBattleOnePosHpr[0],
                         ToontownGlobals.BossbotBossBattleOnePosHpr[1],
                         ToontownGlobals.BossbotBossBattleOnePosHpr[2])
        
        tempNode = self.attachNewNode('temp')
        tempNode.setPos(0,-40,18)

        def getCamBossPos(tempNode=tempNode):
            return tempNode.getPos(render)

        rNode =rToon.attachNewNode('temp2')
        rNode.setPos(-5,25,12)

        def getCamRTPos(rNode =rNode):
            return rNode.getPos(render)
        
         
        track = Sequence(
            Func(camera.reparentTo, render),
            Func(camera.setPos, rToon, 0, 22, 6),
            Func(camera.setHpr, 0, 0, 0),

            
            Func(rToon.setChatAbsolute, TTL.BossbotRTWearWaiter, CFSpeech),
            Wait(3.0),
            self.wearCogSuits( self.toonsA + self.toonsB, render, None, waiter=True),
            Func(rToon.clearChat),
            
            Func(self.setPosHpr, bossPos, Point3(0,0,0)),
            # door opens
            Parallel(
               LerpHprInterval(self.banquetDoor, 2, Point3(90, 0, 0)),
               LerpPosInterval(camera, 2, getCamBossPos),
               ),
            Func(self.setChatAbsolute, TTL.BossbotBossPreTwo1, CFSpeech),
            Wait(3.0),
            Func(self.setChatAbsolute, TTL.BossbotBossPreTwo2, CFSpeech),
            Wait(3.0),
            Parallel(
               LerpHprInterval(self.banquetDoor, 2, Point3(0, 0, 0)),
               LerpPosHprInterval(camera, 2, getCamRTPos, Point3(10,-8,0)),
               ),                                                                    
            Func(self.setPos, bossEndPos),
            Func(self.clearChat),
            
            Func(rToon.setChatAbsolute, TTL.BossbotRTServeFood1, CFSpeech),
            # Open the door as the resistanceToon is talking
            Wait(3.0),
            Func(rToon.setChatAbsolute, TTL.BossbotRTServeFood2, CFSpeech),
            Wait(1.0),
            LerpHprInterval(self.banquetDoor, 2, Point3(120, 0, 0)),
            Sequence(Func(rToon.suit.loop, 'walk'),
                     rToon.hprInterval(1, VBase3(90, 0, 0)),  #turn him around
                     rToon.posInterval(2.5, rToonEndPos),
                     Func(rToon.suit.loop, 'neutral')
                     ),

            # move the toons in
            self.createWalkInInterval(),

            # shut the door and clean up            
            Func(self.banquetDoor.setH, 0),
            Func(rToon.clearChat),
            Func(self.__hideResistanceToon),
            )

        return track

    def createWalkInInterval(self):
        """Create a movie of the toons walking into the banquet room."""
        retval = Parallel()
        delay = 0
        index = 0
        for toonId in self.involvedToons:
            toon = base.cr.doId2do.get(toonId)
            if not toon:
                continue
            destPos = Point3( -14 + (index *4), 25, 0)
            def toWalk(toon):
                if hasattr(toon, 'suit') and toon.suit:
                    toon.suit.loop('walk')
            def toNeutral(toon):
                if hasattr(toon, 'suit') and toon.suit:
                    toon.suit.loop('neutral')
            retval.append( Sequence(
                Wait(delay),
                Func(toon.wrtReparentTo, render),
                Func(toWalk, toon),
                Func(toon.headsUp,0,0,0),
                LerpPosInterval(toon, 3, Point3(0,0,0)),
                Func(toon.headsUp , destPos),
                LerpPosInterval(toon, 3, destPos),
                LerpHprInterval(toon, 1, Point3(0,0,0)),
                Func(toNeutral, toon),
                ))
            if toon == base.localAvatar:
                retval.append( Sequence(
                    Wait(delay),
                    Func(camera.reparentTo,toon),
                    Func(camera.setPos, toon.cameraPositions[0][0]),
                    Func(camera.setHpr, 0, 0, 0)
                         ))
            delay += 1.0
            index += 1
        return retval
        
    def __onToBattleTwo(self, elapsedTime=0):
        """Tell AI we are done with PrepareBattleTwoState."""
        self.doneBarrier('PrepareBattleTwo')

        # Wait a second.  If we don't move on immediately, pop up the
        # "waiting for other players" message.
        #taskMgr.doMethodLater(1, self.__showWaitingMessage,
        #                      self.uniqueName("WaitingMessage"))


    def exitPrepareBattleTwo(self):
        """Cleanup PrepareBattleTwo state."""
        assert self.notify.debugStateCall(self)
        self.clearInterval( "PrepareBattleTwoMovie")
        self.betweenPhaseMusic.stop()
        pass

    def __arrangeToonsAroundResistanceToon(self):
        """Arrange the toons around the resistance toon."""
        radius = 9
        numToons = len(self.involvedToons)
        center = (numToons - 1) / 2.0
        for i in range(numToons):
            toon = self.cr.doId2do.get(self.involvedToons[i])
            if toon:
                angle = 90 - 25 * (i - center)
                radians = angle * math.pi / 180.0
                x = math.cos(radians) * radius
                y = math.sin(radians) * radius
                toon.reparentTo(render)
                toon.setPos(self.resistanceToon, x, y, 0)
                toon.headsUp(self.resistanceToon)
                toon.loop('neutral')
                toon.show()


    ##### BattleTwo state #####
                
    def enterBattleTwo(self):
        """Enter the serving food state."""
        # Let them walk around
        self.releaseToons(finalBattle = 1)
        # put the disguise, so we can quickly get here riding up the elevator
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                self.putToonInCogSuit( toon)
        #setup jury timer
        self.servingTimer = ToontownTimer.ToontownTimer()
        self.servingTimer.posInTopRightCorner()
        self.servingTimer.countdown(ToontownGlobals.BossbotBossServingDuration)
        base.playMusic(self.phaseTwoMusic, looping=1, volume=0.9)

    def exitBattleTwo(self):
        """Do the cleanup for the battle two state."""
        if (self.servingTimer):
            self.servingTimer.destroy()
            del self.servingTimer
            self.servingTimer = None
        for toonId in self.involvedToons:
            self.removeFoodFromToon(toonId)
        self.phaseTwoMusic.stop()

    def setBelt(self, belt, beltIndex):
        """Register the conveyer belt in the room."""        
        if beltIndex < len(self.belts):
            self.belts[beltIndex] = belt

    def localToonTouchedBeltFood(self, beltIndex, foodIndex, foodNum):
        """Handle the local toon touching food on the conveyer belt."""
        avId = base.localAvatar.doId
        doRequest = False
        if not avId in self.toonFoodStatus:
            doRequest = True
        elif not self.toonFoodStatus[avId]:
            doRequest = True
        if doRequest:
            self.sendUpdate('requestGetFood', [beltIndex, foodIndex, foodNum])
            
    def toonGotFood(self, avId,  beltIndex, foodIndex, foodNum):
        """Hande the AI granting a get food request to a toon."""
        if self.belts[beltIndex]:
            self.belts[beltIndex].removeFood(foodIndex)
            self.putFoodOnToon(avId, beltIndex, foodNum)

    def putFoodOnToon(self, avId, beltIndex, foodNum):
        """Put the cog food on the toon's hands."""
        self.toonFoodStatus[avId] = (beltIndex, foodNum)        
        av = base.cr.doId2do.get(avId)
        if av:
            intervalName = self.uniqueName('loadFoodSoundIval-%d' % avId)
            seq = SoundInterval( self.pickupFoodSfx, node = av, name = intervalName)
            oldSeq = self.activeIntervals.get(intervalName)
            if oldSeq:
                oldSeq.finish()
            seq.start()
            self.activeIntervals[intervalName] = seq  
            
            # TODO make sure the animations have the left joint in the correct place
            # when doing toon standing holding food, and toon moving holding food
            foodModel = loader.loadModel('phase_12/models/bossbotHQ/canoffood')
            foodModel.setName('cogFood')
            foodModel.setScale(ToontownGlobals.BossbotFoodModelScale)
            foodModel.reparentTo(av.suit.getRightHand())
            foodModel.setHpr(52.1961, 180.4983, -4.2882)
            curAnim = av.suit.getCurrentAnim()
            self.notify.debug('curAnim=%s' % curAnim)
            if curAnim in ('walk', 'run'):
                av.suit.loop('tray-walk')
            elif curAnim =='neutral':
                self.notify.debug('looping tray-netural')
                av.suit.loop('tray-neutral')
            else:
                self.notify.warning("don't know what to do with anim=%s" % curAnim)

    def removeFoodFromToon(self, avId):
        """Remove the cog food from the toon's hands."""
        self.toonFoodStatus[avId] = None        
        av = base.cr.doId2do.get(avId)        
        if av:
            cogFood = av.find('**/cogFood')
            if not cogFood.isEmpty():
                cogFood.removeNode()

    def detachFoodFromToon(self, avId):
        """Detach the cog food from the toon's hands.

        It will reparent the food to renderm, then return the food nodepath.
        Returns none if there's any problem."""
        cogFood = None
        self.toonFoodStatus[avId] = None        
        av = base.cr.doId2do.get(avId)        
        if av:
            cogFood = av.find('**/cogFood')
            if not cogFood.isEmpty():
                retval = cogFood
                cogFood.wrtReparentTo(render)
            curAnim = av.suit.getCurrentAnim()
            self.notify.debug('curAnim=%s' % curAnim)
            if curAnim == 'tray-walk':
                av.suit.loop('run')
            elif curAnim == 'tray-neutral':
                av.suit.loop('neutral')
            else:
                self.notify.warning("don't know what to do with anim=%s" % curAnim)                              
        return cogFood

    def setTable(self, table, tableIndex):
        """Register one of the banquet tables in the room."""
        self.tables[tableIndex] = table

    def localToonTouchedChair(self, tableIndex, chairIndex):
        """Handle the local toon touching food on the conveyer belt."""
        avId = base.localAvatar.doId
        if (avId in self.toonFoodStatus) and \
           self.toonFoodStatus[avId] != None:
            # we are carrying food, and we touched a chair with a hungry cog
            self.sendUpdate('requestServeFood', [tableIndex, chairIndex])

    def toonServeFood(self, avId, tableIndex, chairIndex):
        """Hande the AI granting a serve food request to a toon."""
        food = self.detachFoodFromToon(avId)
        table = self.tables[tableIndex]
        table.serveFood(food, chairIndex)

    
    ##### Prepare BattleThree state #####        
    def enterPrepareBattleThree(self):
        """Handle entering the Prepare Battle three state """
        self.calcNotDeadList()
        self.battleANode.setPosHpr(*ToontownGlobals.DinerBattleAPosHpr)
        self.battleBNode.setPosHpr(*ToontownGlobals.DinerBattleBPosHpr)        
        self.cleanupIntervals()
        self.controlToons()
        self.setToonsToNeutral(self.involvedToons)
        # put the disguise, so we can quickly get here riding up the elevator
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                self.putToonInCogSuit( toon)        
        intervalName = "PrepareBattleThreeMovie"                
        seq = Sequence(self.makePrepareBattleThreeMovie(),
                       Func(self.__onToBattleThree),
                       name = intervalName)

        seq.start()
        self.storeInterval(seq, intervalName)
        base.playMusic(self.betweenPhaseMusic, looping=1, volume=0.9)  

    def calcNotDeadList(self):
        """Calculate which diners are not dead."""
        if not self.notDeadList:
            self.notDeadList = []
            for tableIndex in xrange(len(self.tables)):
                table = self.tables[tableIndex]
                tableInfo = table.getNotDeadInfo()
                self.notDeadList += tableInfo

    def exitPrepareBattleThree(self):
        """Handle exiting the Prepare Battle three state """
        self.clearInterval( "PrepareBattleThreeMovie")
        self.betweenPhaseMusic.stop()
        pass

    def __onToBattleThree(self, elapsedTime=0):
        """Tell AI we are done with PrepareBattleThreeState."""
        self.doneBarrier('PrepareBattleThree')

    def makePrepareBattleThreeMovie(self):
        """Create and return the pre battle three movie."""
        loseSuitCamAngle = (0,19, 6,-180,-5,0)
        track = Sequence(
            Func(camera.reparentTo, self),
            Func(camera.setPos, Point3(0, -45, 5)),
            Func(camera.setHpr, Point3(0, 14, 0)),
            Func(self.setChatAbsolute, TTL.BossbotPhase3Speech1, CFSpeech),
            Wait(3.0),
            Func(self.setChatAbsolute, TTL.BossbotPhase3Speech2, CFSpeech),
            Wait(3.0),
            Func(camera.setPosHpr, base.localAvatar, *loseSuitCamAngle),
            Wait(1.0),
            self.loseCogSuits(self.toonsA + self.toonsB, base.localAvatar, loseSuitCamAngle),
            self.toonNormalEyes(self.involvedToons),
            Wait(2),
            Func(camera.reparentTo, self),
            Func(camera.setPos, Point3(0, -45, 5)),
            Func(camera.setHpr, Point3(0, 14, 0)),
            Func(self.setChatAbsolute, TTL.BossbotPhase3Speech3, CFSpeech),
            Wait(3.0),
            Func(self.clearChat)
            )

        return track


   #####  BattleThree state #####        
    def enterBattleThree(self):
        """Handle entering the  Battle three state """
        self.cleanupIntervals()
        self.calcNotDeadList()
        for table in self.tables.values():
            table.setAllDinersToSitNeutral()
        self.battleANode.setPosHpr(*ToontownGlobals.DinerBattleAPosHpr)
        self.battleBNode.setPosHpr(*ToontownGlobals.DinerBattleBPosHpr)               
        # self.controlToons() # don't do this so we see laffMeter
        self.setToonsToNeutral(self.involvedToons)
        # remove the disguise, so we can quickly get here riding up the elevator
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.takeOffSuit()
        # Get the credit multiplier
        #mult = ToontownBattleGlobals.getBossBattleCreditMultiplier(3)
        # force it to 1, or maybe even zero
        mult = 1
        localAvatar.inventory.setBattleCreditMultiplier(mult)
        
        # The toons should be in their battle position.
        self.toonsToBattlePosition(self.toonsA, self.battleANode)
        self.toonsToBattlePosition(self.toonsB, self.battleBNode)

        # Now the battle holds the toons.
        self.releaseToons()

        base.playMusic(self.battleOneMusic, looping=1, volume=0.9)                

    def exitBattleThree(self):
        """Handle exiting the Battle three state """
        self.cleanupBattles()
        self.battleOneMusic.stop()

        # No more credit multiplier
        localAvatar.inventory.setBattleCreditMultiplier(1)        
        pass

    def claimOneChair(self):
        """Return one item from the self.notDeadList."""
        chairInfo = None
        if self.notDeadList:
            chairInfo = self.notDeadList.pop()
        return chairInfo
            


    ##### PrepareBattleFour state #####
    def enterPrepareBattleFour(self):
        """Handle entering the Prepare Battle Four State."""
        assert self.notify.debug('%s.enterPrepareBattleFour()' % (self.doId))
        self.controlToons()
        intervalName = "PrepareBattleFourMovie"                
        seq = Sequence(self.makePrepareBattleFourMovie(),
                       Func(self.__onToBattleFour),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)
        base.playMusic(self.phaseFourMusic, looping=1, volume=0.9)  

    def exitPrepareBattleFour(self):
        """Handle exiting the Prepare Battle Four State."""
        self.clearInterval( "PrepareBattleFourMovie")
        self.phaseFourMusic.stop()
        pass

    def makePrepareBattleFourMovie(self):
        """Create and return the pre battle four movie."""
        rToon = self.resistanceToon
        offsetZ = rToon.suit.getHeight() / 2.0
        track = Sequence(
            Func(self.__showResistanceToon, True),
            Func(rToon.setPos, Point3(0,-5,0)),
            Func(rToon.setHpr, Point3(0,0,0)),           
            Func(camera.reparentTo, rToon),
            Func(camera.setPos, Point3(0,13,3 + offsetZ)),
            Func(camera.setHpr, Point3(-180,0,0)),
            Func(self.banquetDoor.setH, 90), 
            Func(rToon.setChatAbsolute, TTL.BossbotRTPhase4Speech1, CFSpeech),
            Wait(4.0),
            Func(rToon.setChatAbsolute, TTL.BossbotRTPhase4Speech2, CFSpeech),
            Wait(4.0),
            Func(self.__hideResistanceToon),
            Func(camera.reparentTo, self),
            Func(camera.setPos, Point3(0, -45, 5)),
            Func(camera.setHpr, Point3(0, 14, 0)),
            Func(self.setChatAbsolute, TTL.BossbotPhase4Speech1, CFSpeech),
            Func(self.banquetDoor.setH, 0), 
            Wait(3.0),
            Func(self.setChatAbsolute, TTL.BossbotPhase4Speech2, CFSpeech),
            Func(self.bossClub.setScale, 0.01),
            Func(self.bossClub.reparentTo, self.rightHandJoint),
            LerpScaleInterval(self.bossClub, 3, Point3(1, 1, 1)),            
            #Wait(3.0),
            Func(self.clearChat),                 
            )

        return track

    def __onToBattleFour(self, elapsedTime=0):
        """Tell AI we are done with PrepareBattleFourState."""
        self.doneBarrier('PrepareBattleFour')


    ##### BattleFour state #####  
    def enterBattleFour(self):
        """Handle entering the Battle Four State."""
        DistributedBossCog.DistributedBossCog.enterBattleFour(self)
        assert self.notify.debug('%s.enterBattleFour()' % (self.doId))
        self.releaseToons(finalBattle = 1)
        self.setToonsToNeutral(self.involvedToons)
        # remove the disguise, so we can quickly get here riding up the elevator
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.takeOffSuit()
        self.bossClub.reparentTo(self.rightHandJoint)
        self.generateHealthBar()
        self.updateHealthBar()
        base.playMusic(self.phaseFourMusic, looping=1, volume=0.9)  
    
    def exitBattleFour(self):
        """Handle exiting the Prepare Battle Four State."""
        DistributedBossCog.DistributedBossCog.exitBattleFour(self)
        self.phaseFourMusic.stop()

    def d_hitBoss(self, bossDamage):
        self.sendUpdate('hitBoss', [bossDamage])

    def d_ballHitBoss(self, bossDamage):
        assert self.notify.debugStateCall(self)
        self.sendUpdate('ballHitBoss', [bossDamage])

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        if bossDamage > self.bossDamage:
            delta = bossDamage - self.bossDamage
            self.flashRed()
            # make the battle harder by not interrupting his attack if he gets hit
            # self.doAnimate('hit', now=1)
            self.showHpText(-delta, scale = 5)
            
        self.bossDamage = bossDamage
        self.updateHealthBar()

    def setGolfSpot(self, golfSpot, golfSpotIndex):
        """Register one of the banquet golfSpots in the room."""
        self.golfSpots[golfSpotIndex] = golfSpot

    ##### Victory state #####

    def enterVictory(self):
        """
        Toons won. Do the CJ lost speech.
        """
        self.notify.debug("----- enterVictory")
        assert self.notify.debug('enterVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.cleanupAttacks()
        self.doAnimate('Ff_neutral', now=1)
        self.stopMoveTask()
        if hasattr(self,'tableIndex'):
            table = self.tables[self.tableIndex]
            table.tableGroup.hide()

        #self.reparentTo(render)
        #self.setPosHpr(*ToontownGlobals.LawbotBossBattleThreePosHpr)
        self.loop('neutral')

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        self.clearChat()
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
        base.playMusic(self.phaseFourMusic, looping=1, volume=0.9)

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
        self.phaseFourMusic.stop()

        #self.battleThreeMusicTime = self.battleThreeMusic.getTime()
        #self.battleThreeMusic.stop()

    def makeVictoryMovie(self):
        """
        Make the victory movie.  
        """
        self.show()
        dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1,)
        dustCloud.reparentTo(self)
        dustCloud.setPos(0, -10, 3)
        dustCloud.setScale(4)
        dustCloud.wrtReparentTo( self.geom)
        dustCloud.createTrack(12)

        newHpr = self.getHpr()
        newHpr.setX( newHpr.getX() + 180)

        bossTrack = Sequence(
            Func(self.show),
            Func(camera.reparentTo, self),
            Func(camera.setPos, Point3(0, -35, 25)),
            Func(camera.setHpr, Point3(0, -20, 0)),
            Func(self.setChatAbsolute, TTL.BossbotRewardSpeech1, CFSpeech),
            Wait(3.0),
            Func(self.setChatAbsolute, TTL.BossbotRewardSpeech2, CFSpeech),
            Wait(2.0),
            Func(self.clearChat),
            Parallel(
               Sequence(
                  Wait(0.5),
                  Func(self.demotedCeo.setPos, self.getPos()),                  
                  Func(self.demotedCeo.setHpr, newHpr),
                  Func(self.hide),
                  Wait(0.5),
                  Func(self.demotedCeo.reparentTo, self.geom),
                  Func(self.demotedCeo.unstash),
                  
                  ),
               Sequence(
                  dustCloud.track,
                  )
                  
               ),
            Wait(2.0),
            Func(dustCloud.destroy),
            )
        return bossTrack

    ##### Reward state #####

    def enterReward(self):
        """
        Show the reward movie, skillups, questsm etc.
        """
        assert self.notify.debug('enterReward()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.resistanceToon.clearChat()

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
                delayDeletes.append(DelayDelete.DelayDelete(toon, 'BossbotBoss.enterReward'))
                                    
        ival.delayDeletes = delayDeletes
        ival.start()
        self.storeInterval(ival, intervalName)

        base.playMusic(self.betweenPhaseMusic, looping=1, volume=0.9)


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
        self.betweenPhaseMusic.stop()

        #self.battleThreeMusicTime = 0
        #self.battleThreeMusic.stop()

    ##### Epilogue state #####

    def enterEpilogue(self):
        """
        Enter the epilogue. Resistance toon thanks us.
        """
        assert self.notify.debug('enterEpilogue()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.resistanceToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()

        # The toons are under our control once again.
        self.controlToons()

        self.__showResistanceToon(False)
        self.resistanceToon.reparentTo(render)
        self.resistanceToon.setPosHpr(*ToontownGlobals.BossbotRTEpiloguePosHpr)
        self.resistanceToon.loop('Sit')        
        self.__arrangeToonsAroundResistanceToonForReward()

        camera.reparentTo(render)
        camera.setPos(self.resistanceToon, -9, 12, 6)
        camera.lookAt(self.resistanceToon, 0, 0, 3)

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

    def makeEpilogueMovie(self):
        """
        Make the epilogue movie.  
        """
        epSpeech = TTLocalizer.BossbotRTCongratulations
        
        epSpeech = self.__talkAboutPromotion(epSpeech)
        
        bossTrack = Sequence (
           Func(self.resistanceToon.animFSM.request,'neutral'),
           Func(self.resistanceToon.setLocalPageChat,epSpeech, 0)
           )
        return bossTrack

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
                speech += TTLocalizer.BossbotRTLastPromotion % (ToontownGlobals.MaxCogSuitLevel+1)
            # if they're getting another LP, tell them
            if newCogSuitLevel in ToontownGlobals.CogSuitHPLevels:
                speech += TTLocalizer.BossbotRTHPBoost
        else:
            # level XX, wow! Thanks for coming back!
            speech += TTLocalizer.BossbotRTMaxed % (ToontownGlobals.MaxCogSuitLevel+1)

        return speech
    

    def __arrangeToonsAroundResistanceToonForReward(self):
        """
        Arrange the toons around the resistance toon
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
                toon.setPos(self.resistanceToon, x, y, 0)
                toon.headsUp(self.resistanceToon)
                toon.loop('neutral')
                toon.show()


    def doDirectedAttack(self, avId, attackCode):
        """Attack the toon by throwing gears at him with no distance limit."""
        toon = base.cr.doId2do.get(avId)
        if toon:
            distance = toon.getDistance(self)
            #self.notify.debug('distance = %s' % distance)
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d' % self.numAttacks)
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
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName)
                node.hide()
                node.setPos(0, 5.85, 4.0)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                h = random.uniform(-720, 720)
                if i == 2:
                    # guarantee one of them to hit if he doesn't move
                    x = 0
                    z = 0

                def detachNode( node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater( node = node):
                    # we must detach the gear on the next frame to still hit
                    # the cheating toons
                    if node.isEmpty():
                        return
                    center = node.node().getBounds().getCenter()
                    node.node().setBounds(BoundingSphere(center, distance*1.5))
                    node.node().setFinal(1)
                    
                    self.doMethodLater(0.005, detachNode,
                                       'detach-%s-%s' % (gearRoot.getName(),node.getName()),
                                       extraArgs = [ node],
                                       )
                gearTrack.append(Sequence(
                    Wait(i * 0.15),
                    Func(node.show),
                    Parallel(node.posInterval(1, Point3(x, distance, z), fluid = 1),
                             node.hprInterval(1, VBase3(h, 0, 0), fluid = 1)),
                    Func(detachNodeLater)))

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

            def detachGearRoot( task, gearRoot = gearRoot):
                if not gearRoot.isEmpty():
                    gearRoot.detachNode()
                return task.done
                
            def detachGearRootLater( gearRoot = gearRoot):
                # we must detach the gear root on the next frame to still hit
                # the cheating toons
                if gearRoot.isEmpty():
                    return
                self.doMethodLater(0.01, detachGearRoot,
                                   'detach-%s' % gearRoot.getName(),
                                   )

            seq = Sequence(
                ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)),
                                    neutral1Anim),
                extraAnim,
                Parallel(Sequence(Wait(0.19),
                                  gearTrack,
                                  Func(detachGearRootLater),
                                  self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                         Sequence(throwAnim, neutral2Anim)))

            self.doAnimate(seq, now = 1, raised = 1)

    def setBattleDifficulty(self, diff):
        """
        We got the battle difficulty from the AI
        """
        self.notify.debug('battleDifficulty = %d' % diff)
        self.battleDifficulty = diff

    def doMoveAttack(self, tableIndex):
        """Attack a toon by flattening a table."""
        self.tableIndex = tableIndex
        table = self.tables[tableIndex]
        fromPos = self.getPos()
        fromHpr = self.getHpr()        
        toPos = table.getPos()
        foo = render.attachNewNode('foo')
        foo.setPos(self.getPos())
        foo.setHpr(self.getHpr())
        foo.lookAt(table.getLocator())
        toHpr = foo.getHpr() 
        toHpr.setX( toHpr.getX() - 180) # heading of zero faces towards -y axis
        foo.removeNode()
        reverse = False
        moveTrack, hpr = self.moveBossToPoint(fromPos, fromHpr, toPos, toHpr, reverse)
        self.moveTrack = moveTrack
        self.moveTrack.start()
        self.storeInterval(self.moveTrack, 'moveTrack')
        

    def interruptMove(self):
        """Stop the CEO from moving."""
        if self.moveTrack and self.moveTrack.isPlaying():
            self.moveTrack.pause()
        self.stopMoveTask()

    def setAttackCode(self, attackCode, avId = 0):
        """Do the indicated attack, on the given toon."""
        # This message is sent from the AI to tell the Boss Cog to
        # animate some attack.
        assert self.notify.debug("setAttackCode(%s, %s) time=%f" %
                                 (attackCode, avId, globalClock.getFrameTime()))        
        if self.state != 'BattleFour':
            return
        self.numAttacks += 1
        self.notify.debug('numAttacks=%d' % self.numAttacks)
        self.attackCode = attackCode
        self.attackAvId = avId
        if attackCode == ToontownGlobals.BossCogMoveAttack:
            # interruptMove stops CEO from moving sideways
            self.interruptMove()
            self.doMoveAttack(avId)
        elif attackCode == ToontownGlobals.BossCogGolfAttack:
            self.interruptMove()
            self.cleanupAttacks()
            self.doGolfAttack(avId, attackCode)
        elif attackCode == ToontownGlobals.BossCogDizzy:
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
             attackCode == ToontownGlobals.BossCogSlowDirectedAttack or \
             attackCode == ToontownGlobals.BossCogGearDirectedAttack:
            # Rotate to face the toon and spit out gears.
            self.interruptMove()
            self.setDizzy(0)
            self.doDirectedAttack(avId, attackCode)
            
        elif attackCode == ToontownGlobals.BossCogGolfAreaAttack:
            self.interruptMove()
            self.setDizzy(0)
            self.doGolfAreaAttack()
            
        elif attackCode == ToontownGlobals.BossCogNoAttack:
            # Just stand up.
            self.setDizzy(0)
            self.doAnimate(None, raised = 1)
        elif attackCode == ToontownGlobals.BossCogOvertimeAttack:
            self.interruptMove()
            self.setDizzy(0)
            self.cleanupAttacks()
            self.doOvertimeAttack(avId)


    def signalAtTable(self):
        """Tell the ai we've reached the table we were moving to."""
        self.sendUpdate('reachedTable',[self.tableIndex])

    def closeEnter(self, colEntry):
        """Handle the CEO we've hit something, probably a table."""
        tableStr = colEntry.getIntoNodePath().getNetTag('tableIndex')
        if tableStr:
            tableIndex = int(tableStr)
            # Note we could hit a different table than the one were were going to.
            self.sendUpdate('hitTable', [tableIndex])

    def closeExit(self, colEntry):
        """Handle the CEO we've hit stopped something, probably a table."""
        #import pdb; pdb.set_trace()        
        tableStr = colEntry.getIntoNodePath().getNetTag('tableIndex')
        if tableStr:
            tableIndex = int(tableStr)
            # Note we could hit a different table than the one were were going to.
            # do not generate an awayFromTable if we are headed to that table
            if self.tableIndex != tableIndex:
                self.sendUpdate('awayFromTable', [tableIndex])

    def setSpeedDamage(self, speedDamage, recoverRate, timestamp):
        """Handle the AI telling us the current speed damage."""
        recoverStartTime = globalClockDelta.networkToLocalTime(timestamp)
        self.speedDamage = speedDamage
        self.speedRecoverRate = recoverRate
        self.speedRecoverStartTime = recoverStartTime

        speedFraction = max( 1 - ( speedDamage/ self.maxSpeedDamage), 0)        
        self.treads.setColorScale( 1, speedFraction, speedFraction, 1)        

        taskName = "RecoverSpeedDamage"
        taskMgr.remove(taskName)

        if self.speedRecoverRate:
            taskMgr.add(self.__recoverSpeedDamage, taskName)
                    

    def getSpeedDamage(self):
        """Return the speed damage, taking into account the recover rate."""
        now = globalClock.getFrameTime()
        elapsed = now - self.speedRecoverStartTime

        # Although the AI side computes and transmits getSpeedDamage()
        # as an integer value, on the client side we return it as a
        # floating-point value, so we can get the smooth transition
        # effect as the speed slowly starts to roll back up.
        return max(self.speedDamage - self.speedRecoverRate * elapsed /60.0 ,0 )

    def getFractionalSpeedDamage(self):
        """Return the current speed damage as a fraction between 0 and 1."""
        result = self.getSpeedDamage() / self.maxSpeedDamage
        return result

    def __recoverSpeedDamage(self, task):
        """Make the speed damage indicator match our current speed damage."""
        speedDamage = self.getSpeedDamage()
        speedFraction = max( 1 - ( speedDamage/ self.maxSpeedDamage), 0)        
        self.treads.setColorScale( 1, speedFraction, speedFraction, 1)
        return task.cont

    def moveBossToPoint(self, fromPos, fromHpr, toPos, toHpr, reverse):
        """Return an interval and Hpr that moves the CEO to a point."""
        assert self.notify.debugStateCall(self)
        vector = Vec3(toPos - fromPos)
        distance = vector.length()
        self.distanceToTravel = distance
        self.notify.debug("self.distanceToTravel = %s" % self.distanceToTravel)

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
        
        turnTime = abs(toHpr[0] - fromHpr[0]) / self.getCurTurnSpeed()

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
        self.toPos = toPos
        self.fromPos = fromPos
        self.dirVector = self.toPos - self.fromPos
        self.dirVector.normalize()
        track = Sequence(Func(self.setPos, fromPos),
                         Func(self.headsUp, toPos),
                         Parallel(self.hprInterval(turnTime, toHpr, fromHpr),
                                  self.rollLeftTreads(turnTime, leftRate),
                                  self.rollRightTreads(turnTime, -leftRate),
                                  #SoundInterval(self.treadsSfx, duration = turnTime, loop = 1, volume = 0.2),
                                  ),
                         Func(self.startMoveTask),
                         )

        # Return both the computed track and the destination hpr
        # (which might be useful for the next sequence).
        return track, toHpr


    def getCurTurnSpeed(self):
        """Return the turn speed, taking into account the current speed damage."""
        result = ToontownGlobals.BossbotTurnSpeedMax - \
                 ((ToontownGlobals.BossbotTurnSpeedMax - ToontownGlobals.BossbotTurnSpeedMin) *
                  self.getFractionalSpeedDamage())
        return result

    def getCurRollSpeed(self):
        """Return the roll speed, taking into account the current speed damage."""
        result = ToontownGlobals.BossbotRollSpeedMax - \
                 ((ToontownGlobals.BossbotRollSpeedMax - ToontownGlobals.BossbotRollSpeedMin) *
                  self.getFractionalSpeedDamage())
        return result

    def getCurTreadSpeed(self):
        """Return the tread speed, taking into account the current speed damage."""
        result = ToontownGlobals.BossbotTreadSpeedMax - \
                 ((ToontownGlobals.BossbotTreadSpeedMax - ToontownGlobals.BossbotTreadSpeedMin) *
                  self.getFractionalSpeedDamage())
        return result
        
    def startMoveTask(self):
        """Start the incremental move boss task."""
        taskMgr.add(self.moveBossTask, self.moveBossTaskName)

    def stopMoveTask(self):
        """Stop the incremental move boss task."""
        taskMgr.remove( self.moveBossTaskName)

    def moveBossTask(self, task):
        """Incrementally move the boss for this frame."""
        dt = globalClock.getDt()
        # check if we've arrived
        distanceTravelledThisFrame = dt * self.getCurRollSpeed()
        diff = self.toPos - self.getPos()
        distanceLeft = diff.length()
 
        def rollTexMatrix(t, object = object):
            object.setTexOffset(TextureStage.getDefault(), t, 0)

        self.treadsLeftPos += dt * self.getCurTreadSpeed()
        self.treadsRightPos += dt * self.getCurTreadSpeed()
        rollTexMatrix( self.treadsLeftPos , self.treadsLeft)
        rollTexMatrix( self.treadsRightPos , self.treadsRight)

        if distanceTravelledThisFrame >= distanceLeft:
            self.setPos(self.toPos)
            self.signalAtTable()
            return Task.done
        else:
            newPos = self.getPos() + self.dirVector * dt * self.getCurRollSpeed()
            self.setPos(newPos)
            return Task.cont
            

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
            if self.isToonRoaming(toon.doId):
                toonTrack += [ActorInterval(toon, 'slip-backward'),]
                toonTrack += [toon.posInterval(0.5, getSlideToPos, fluid = 1)]
        else:
            toonTrack += [ActorInterval(toon, 'slip-forward')]
            
        zapTrack.append(toonTrack)
        
        if toon == localAvatar:
            zapTrack.append(Func(self.disableLocalToonSimpleCollisions))
            currentState = self.state
            if currentState in ( 'BattleFour', 'BattleTwo'):
                zapTrack.append(Func(self.toFinalBattleMode))
            else:
                self.notify.warning('doZapToon going to walkMode, how did this happen?')
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

        zapTrack.delayDelete = DelayDelete.DelayDelete(toon, 'BossbotBoss.doZapToon')
        zapTrack.start(startTime)
        self.storeInterval(zapTrack, zapName)


    def zapLocalToon(self, attackCode, origin = None):
        assert self.notify.debugStateCall(self)
        if self.localToonIsSafe or localAvatar.ghostMode or localAvatar.isStunned:
            return
        if globalClock.getFrameTime() < self.lastZapLocalTime + 1.0:
            return
        else:
            self.lastZapLocalTime = globalClock.getFrameTime()
        self.notify.debug('zapLocalToon frameTime=%s' % globalClock.getFrameTime())
        messenger.send('interrupt-pie')
        
        place = self.cr.playGame.getPlace()
        currentState = None
        if place:
            currentState = place.fsm.getCurrentState().getName()
        if currentState != 'walk' and currentState != 'finalBattle' and currentState != 'crane':
            # Ignore this except when the Toon's in walk mode.
            return
        self.notify.debug('continuing zap')

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

            if self.isToonRoaming(toon.doId):
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

    def getToonTableIndex(self, toonId):
        """Returns the table index he is on, -1 if he's not on a table"""
        tableIndex = -1
        for table in self.tables.values():
            if table.avId == toonId:
                tableIndex =  table.index
                break
        return tableIndex

    def getToonGolfSpotIndex(self, toonId):
        """Returns the golfSpot index he is on, -1 if he's not on a golfSpot"""
        golfSpotIndex = -1
        for golfSpot in self.golfSpots.values():
            if golfSpot.avId == toonId:
                golfSpotIndex =  golfSpot.index
                break
        return golfSpotIndex        

    def isToonOnTable(self, toonId):
        """Returns True if the toon is on a table."""
        result = self.getToonTableIndex(toonId) != -1
        return result

    def isToonOnGolfSpot(self, toonId):
        """Returns True if the toon is on a golf spot."""
        result = self.getToonGolfSpotIndex(toonId) != -1
        return result

    def isToonRoaming(self, toonId):
        result = not self.isToonOnTable(toonId) and not self.isToonOnGolfSpot(toonId)
        return result

    def getGolfBall(self):
        """Return a cog golf ball model."""
        golfRoot = NodePath('golfRoot')
        golfBall = loader.loadModel('phase_6/models/golf/golf_ball')
        golfBall.setColorScale(0.75, 0.75, 0.75, 0.5)
        golfBall.setTransparency(1)
        ballScale = 5
        golfBall.setScale(ballScale)
        golfBall.reparentTo(golfRoot)
        # we need to create a collision sphere called BossZap
        # the golf ball has a radius of 0.25 if it has a scale of 1
        cs = CollisionSphere(0, 0, 0, ballScale * 0.25)
        cs.setTangible(0)
        cn = CollisionNode('BossZap')
        cn.addSolid(cs)
        cn.setIntoCollideMask(ToontownGlobals.WallBitmask)
        cnp = golfRoot.attachNewNode(cn)
        return golfRoot
    
    def doGolfAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            distance = toon.getDistance(self)
            self.notify.debug('distance = %s' % distance)            
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d' % self.numAttacks)
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))          
            gearModel = self.getGolfBall()            
            #gearModel.setScale(0.2)

            self.ballLaunch = NodePath('') #gearRoot.attachNewNode('ballLaunch')
            self.ballLaunch.reparentTo(gearRoot)
            self.ballLaunch.setPos(self.BallLaunchOffset) 
            #axis = loader.loadModel('models/misc/xyzAxis')
            #if axis and not axis.isEmpty():
            #    axis.setScale(1)
            #    axis.reparentTo(self.ballLaunch)

            # First, get just the H value towards the toon.
            gearRoot.headsUp(toon)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)

            #self.notify.debug('toToonH = %s' % toToonH)

            # Now pitch towards the toon so we can throw gears at him.
            gearRoot.lookAt(toon)

            neutral = 'Fb_neutral'
            if not self.twoFaced:
                neutral = 'Ff_neutral'

            gearTrack = Parallel()
            for i in range(5):
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName)
                node.hide()
                #node.setPos(0, 5.85, 4.0)
                node.reparentTo(self.ballLaunch)
                node.wrtReparentTo(gearRoot)
                #node.show()
                distance = toon.getDistance(node)
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                p = random.uniform(-720, -90)
                y = distance + random.uniform(5, 15)
                if i == 2:
                    # guarantee one of them to hit if he doesn't move
                    x = 0
                    z = 0
                    y = distance + 10

                def detachNode( node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater( node = node):
                    # we must detach the gear on the next frame to still hit
                    # the cheating toons
                    if node.isEmpty():
                        return
                    node.node().setBounds(BoundingSphere(Point3(0,0,0), distance*1.5))
                    node.node().setFinal(1)                    
                    self.doMethodLater(0.005, detachNode,
                                       'detach-%s-%s' % (gearRoot.getName(),node.getName()),
                                       extraArgs = [ node],
                                       )


                gearTrack.append(Sequence(
                    Wait( 26.0 / 24.),
                    Wait(i * 0.15),
                    Func(node.show),
                    Parallel(node.posInterval(1, Point3(x, y, z), fluid = 1),
                             node.hprInterval(1, VBase3(0, p, 0), fluid = 1)),
                    Func(detachNodeLater)))

            # A 1-second animation to play while rotating.  It might
            # be the neutral cycle, or the climb-up cycle.
            if not self.raised:
                neutral1Anim = self.getAnim('down2Up')
                self.raised = 1
            else:
                neutral1Anim = ActorInterval(self, neutral, startFrame = 48)
                
            throwAnim = self.getAnim('golf_swing')
            # the golf swing has a duration of 2 seconds
            neutral2Anim = ActorInterval(self, neutral)

            extraAnim = Sequence()
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                # If it's the "slow" attack, pause for a bit longer
                # here to give the player more warning.
                extraAnim = ActorInterval(self, neutral)

            def detachGearRoot( task, gearRoot = gearRoot):
                if not gearRoot.isEmpty():
                    gearRoot.detachNode()
                return task.done
                
            def detachGearRootLater( gearRoot = gearRoot):
                # we must detach the gear root on the next frame to still hit
                # the cheating toons
                self.doMethodLater(0.01, detachGearRoot,
                                   'detach-%s' % gearRoot.getName(),
                                   )
                
            seq = Sequence(
                ParallelEndTogether(self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)),
                                    neutral1Anim),
                extraAnim,
                Parallel(Sequence(Wait(0.19),
                                  gearTrack,
                                  Func(detachGearRootLater),
                                  self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                         Sequence(throwAnim, neutral2Anim),
                         Sequence(Wait(0.85),
                                  SoundInterval(self.swingClubSfx, node=self,
                                                duration = 0.45,
                                                cutOff = 300,
                                                listenerNode = base.localAvatar),
                                  )
                         )
                )
                         

            self.doAnimate(seq, now = 1, raised = 1)


    def doGolfAreaAttack(self):
        toons = []
        for toonId in self.involvedToons:
            toon = base.cr.doId2do.get(toonId)
            if toon:
                toons.append(toon)            
        if not toons:
            return

        neutral = 'Fb_neutral'
        if not self.twoFaced:
            neutral = 'Ff_neutral'

        # A 1-second animation to play while rotating.  It might
        # be the neutral cycle, or the climb-up cycle.
        if not self.raised:
            neutral1Anim = self.getAnim('down2Up')
            self.raised = 1
        else:
            neutral1Anim = ActorInterval(self, neutral, startFrame = 48)

        throwAnim = self.getAnim('golf_swing')
        # the golf swing has a duration of 2 seconds
        neutral2Anim = ActorInterval(self, neutral)

        extraAnim = Sequence()
        if False:
            # If it's the "slow" attack, pause for a bit longer
            # here to give the player more warning.
            extraAnim = ActorInterval(self, neutral)
            
      
        gearModel = self.getGolfBall()            

        # First, get just the H value towards the toon.
        toToonH = self.rotateNode.getH() + 360
        self.notify.debug('toToonH = %s' % toToonH)

        gearRoots = []
        allGearTracks = Parallel()
        for toon in toons:
            gearRoot = self.rotateNode.attachNewNode('gearRoot-atk%d-%d' %
                                                     (self.numAttacks, toons.index(toon)))
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(ToontownGlobals.BossCogGolfAreaAttack))
            gearRoot.lookAt(toon)

            ballLaunch = NodePath('') #gearRoot.attachNewNode('ballLaunch')
            ballLaunch.reparentTo(gearRoot)
            ballLaunch.setPos(self.BallLaunchOffset)             
            
            
            gearTrack = Parallel()
            for i in range(5):
                nodeName = '%s-%s' % (str(i), globalClock.getFrameTime())
                node = gearRoot.attachNewNode(nodeName  )
                node.hide()
                #node.setPos(0, 5.85, 4.0)
                node.reparentTo(ballLaunch)
                node.wrtReparentTo(gearRoot)

                distance = toon.getDistance(node)
                toonPos = toon.getPos(render)
                nodePos = node.getPos(render)
                vector = toonPos-nodePos
                #self.notify.debug('toonPos=%s nodePos=%s length=%s' % (toonPos, nodePos, vector.length()))
                #self.notify.debug('distance = %s' % distance)
                
                #node.show()
                gear = gearModel.instanceTo(node)
                x = random.uniform(-5, 5)
                z = random.uniform(-3, 3)
                p = random.uniform(-720, -90)
                y = distance + random.uniform(5,15)
                if i == 2:
                    # guarantee one of them to hit if he doesn't move
                    x = 0
                    z = 0
                    y = distance +10

                def detachNode( node):
                    if not node.isEmpty():
                        node.detachNode()
                    return Task.done

                def detachNodeLater( node = node):
                    # we must detach the gear on the next frame to still hit
                    # the cheating toons
                    if node.isEmpty():
                        return
                    node.node().setBounds(BoundingSphere(Point3(0,0,0), distance*1.5))
                    node.node().setFinal(1)                    
                    self.doMethodLater(0.005, detachNode,
                                       'detach-%s-%s' % (gearRoot.getName(),node.getName()),
                                       extraArgs = [ node],
                                       )

                gearTrack.append(Sequence(
                    Wait( 26.0 / 24.),
                    Wait(i * 0.15),
                    Func(node.show),
                    Parallel(node.posInterval(1, Point3(x, y, z), fluid = 1),
                             node.hprInterval(1, VBase3(0, p, 0), fluid = 1)),
                    Func(detachNodeLater)))
            allGearTracks.append(gearTrack)

        def detachGearRoots(gearRoots = gearRoots):
            for gearRoot in gearRoots:
                def detachGearRoot( task, gearRoot = gearRoot):
                    if not gearRoot.isEmpty():
                        gearRoot.detachNode()
                    return task.done
                if gearRoot.isEmpty():
                    continue
                self.doMethodLater(0.01, detachGearRoot,
                                       'detach-%s' % gearRoot.getName(),
                                       )
            gearRoots = []

        rotateFire = Parallel(
            self.pelvis.hprInterval(2, VBase3(toToonH + 1440, 0, 0)),
            allGearTracks
            )

        seq = Sequence(
            Func(base.playSfx, self.warningSfx),
            Func(self.saySomething, TTLocalizer.GolfAreaAttackTaunt),
            ParallelEndTogether(self.pelvis.hprInterval(2, VBase3(toToonH, 0, 0)),
                                neutral1Anim),
            extraAnim,
            Parallel(Sequence(#Wait(0.19),
                              rotateFire,
                              Func(detachGearRoots),
                              #self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))
                              Func(self.pelvis.setHpr, VBase3(0,0,0))
                              ),
                     Sequence( throwAnim, neutral2Anim),
                     Sequence(Wait(0.85),
                              SoundInterval(self.swingClubSfx, node=self,
                                            duration = 0.45,
                                            cutOff = 300,
                                            listenerNode = base.localAvatar),
                              ),
                     ))
        self.doAnimate(seq, now = 1, raised = 1)

    def saySomething(self, chatString):
        """
        Make the CEO say something
        """
        intervalName = "CEOTaunt"
        seq = Sequence( name = intervalName)
        seq.append(Func(self.setChatAbsolute, chatString, CFSpeech))
        seq.append( Wait(4.0) )
        seq.append(Func(self.clearChat))
        oldSeq = self.activeIntervals.get(intervalName)
        if oldSeq:
           oldSeq.finish()
        seq.start()          
        self.activeIntervals[intervalName] = seq        
        
    def d_hitToon(self, toonId):
        """Tell the AI the local client healed a toon."""
        self.notify.debug("----- d_hitToon")
        self.sendUpdate('hitToon', [toonId])

    def toonGotHealed(self, toonId):
        """
        A toon got healed, play a sound effect
        """
        toon = base.cr.doId2do.get(toonId)
        if toon:
            base.playSfx(self.toonUpSfx, node = toon)


    def localToonTouchedBeltToonup(self, beltIndex, toonupIndex, toonupNum):
        """Handle the local toon touching toonup on the conveyer belt."""
        avId = base.localAvatar.doId
        doRequest = True
        if doRequest:
            self.sendUpdate('requestGetToonup', [beltIndex, toonupIndex, toonupNum])
            
    def toonGotToonup(self, avId,  beltIndex, toonupIndex, toonupNum):
        """Hande the AI granting a get toonup request to a toon."""
        if self.belts[beltIndex]:
            self.belts[beltIndex].removeToonup(toonupIndex)
        toon = base.cr.doId2do.get(avId)
        if toon:
            base.playSfx(self.toonUpSfx, node = toon)

    def doOvertimeAttack(self, index):
        """Make him shoot one food belt to stop it, and pulse his golf club."""
        attackCode = ToontownGlobals.BossCogOvertimeAttack
        attackBelts = Sequence()
        if index < len(self.belts):
            # avId is actually an index
            belt = self.belts[index]
            self.saySomething(TTLocalizer.OvertimeAttackTaunts[index])
            if index:
                self.bossClubIntervals[0].finish()
                self.bossClubIntervals[1].loop()                
            else:
                self.bossClubIntervals[1].finish()
                self.bossClubIntervals[0].loop()
            distance = belt.beltModel.getDistance(self)
            gearRoot = self.rotateNode.attachNewNode('gearRoot')
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            gearModel = self.getGearFrisbee()
            gearModel.setScale(0.2)

            # First, get just the H value towards the toon.
            gearRoot.headsUp(belt.beltModel)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)

            # Now pitch towards the toon so we can throw gears at him.
            gearRoot.lookAt(belt.beltModel)

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
                    Parallel(node.posInterval(1, Point3(x, distance, z), fluid = 1),
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
                                  Func(self.explodeSfx.play),
                                  self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))),
                         Sequence(throwAnim, neutral2Anim)),
                Func(belt.request,'Inactive')
                )
            attackBelts.append(seq)

        self.notify.debug('attackBelts duration= %.2f' % attackBelts.getDuration())
        self.doAnimate(attackBelts, now = 1, raised = 1)    
