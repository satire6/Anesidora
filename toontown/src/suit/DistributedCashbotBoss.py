from direct.interval.IntervalGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
import DistributedBossCog
from direct.task.Task import Task
import DistributedCashbotBossGoon
import SuitDNA
from toontown.toon import Toon
from toontown.toon import ToonDNA
from direct.fsm import FSM
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from toontown.building import ElevatorUtils
from toontown.building import ElevatorConstants
from toontown.battle import MovieToonVictory
from toontown.battle import RewardPanel
from toontown.distributed import DelayDelete
from toontown.chat import ResistanceChat
from toontown.coghq import CogDisguiseGlobals
from pandac.PandaModules import *
import random
import math

# This pointer keeps track of the one DistributedCashbotBoss that
# should appear within the avatar's current visibility zones.  If
# there is more than one DistributedCashbotBoss visible to a client at
# any given time, something is wrong.
OneBossCog = None

TTL = TTLocalizer
class DistributedCashbotBoss(DistributedBossCog.DistributedBossCog, FSM.FSM):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCashbotBoss')

    numFakeGoons = 3

    def __init__(self, cr):
        DistributedBossCog.DistributedBossCog.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedSellbotBoss')

        self.resistanceToon = None
        self.resistanceToonOnstage = 0
        self.cranes = {}
        self.safes = {}
        self.goons = []

        self.bossMaxDamage = ToontownGlobals.CashbotBossMaxDamage

        self.elevatorType = ElevatorConstants.ELEVATOR_CFO

        #hack for quick access while debugging
        base.boss = self

    def announceGenerate(self):
        DistributedBossCog.DistributedBossCog.announceGenerate(self)

        # at this point all our attribs have been filled in.
        self.setName(TTLocalizer.CashbotBossName)
        nameInfo = TTLocalizer.BossCogNameWithDept % {
            "name":  self.name,
            "dept":  (SuitDNA.getDeptFullname(self.style.dept)),
            }
        self.setDisplayName(nameInfo)

        # Our goal in this battle is to drop stuff on the CFO's head.
        # For this, we need a target.
        target = CollisionSphere(2, 0, 0, 3)
        targetNode = CollisionNode('headTarget')
        targetNode.addSolid(target)
        targetNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.headTarget = self.neck.attachNewNode(targetNode)

        # And he gets a big bubble around his torso, just to keep
        # things from falling through him.  It's a big sphere so
        # things will tend to roll off him instead of landing on him.
        shield = CollisionSphere(0, 0, 0.8, 7)
        shieldNode = CollisionNode('shield')
        shieldNode.addSolid(shield)
        shieldNode.setCollideMask(ToontownGlobals.PieBitmask)
        shieldNodePath = self.pelvis.attachNewNode(shieldNode)
                               

        # By "heldObject", we mean the safe he's currently wearing as
        # a helmet, if any.  It's called a heldObject because this is
        # the way the cranes refer to the same thing, and we use the
        # same interface to manage this.
        self.heldObject = None

        self.bossDamage = 0

        # The BossCog actually owns the environment geometry.  Not
        # sure if this is a great idea, but it's the way we did it
        # with the sellbot boss, and the comment over there seems to
        # think it's a great idea. :)
        self.loadEnvironment()

        # Set up the caged toon.
        self.__makeResistanceToon()

        # Set up a physics manager for the cables and the objects
        # falling around in the room.

        self.physicsMgr = PhysicsManager()
        integrator = LinearEulerIntegrator()
        self.physicsMgr.attachLinearIntegrator(integrator)

        fn = ForceNode('gravity')
        self.fnp = self.geom.attachNewNode(fn)
        gravity = LinearVectorForce(0, 0, -32)
        fn.addForce(gravity)
        self.physicsMgr.addLinearForce(gravity)

        # Enable the special CFO chat menu.
        localAvatar.chatMgr.chatInputSpeedChat.addCFOMenu()

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
        self.demand('Off')

        self.unloadEnvironment()
        self.__cleanupResistanceToon()

        self.fnp.removeNode()
        self.physicsMgr.clearLinearForces()

        self.battleThreeMusic.stop()
        self.epilogueMusic.stop()

        localAvatar.chatMgr.chatInputSpeedChat.removeCFOMenu()

        global OneBossCog
        if OneBossCog == self:
            OneBossCog = None

    def __makeResistanceToon(self):
        # Generates the Resistance Toon (tm), who will be our initial
        # guide and then callously abandon us to our fate.
        if self.resistanceToon:
            return

        npc = Toon.Toon()
        npc.setName(TTLocalizer.ResistanceToonName)
        npc.setPickable(0)
        npc.setPlayerType(NametagGroup.CCNonPlayer)
        dna = ToonDNA.ToonDNA()
        dna.newToonRandom(11237, 'f', 1)
        dna.head = "pls"
        npc.setDNAString(dna.makeNetString())

        npc.animFSM.request("neutral")

        self.resistanceToon = npc
        self.resistanceToon.setPosHpr(*ToontownGlobals.CashbotRTBattleOneStartPosHpr)

        # determine a random suit to put him in
        state = random.getstate()
        random.seed(self.doId)
        self.resistanceToon.suitType = SuitDNA.getRandomSuitByDept("m")
        random.setstate(state)

        # Make some goons for the resistance toon to play with
        self.fakeGoons = []
        for i in range(self.numFakeGoons):
            goon = DistributedCashbotBossGoon.DistributedCashbotBossGoon(base.cr)
            goon.doId = -1 - i
            goon.setBossCogId(self.doId)
            goon.generate()
            goon.announceGenerate()
            self.fakeGoons.append(goon)
        self.__hideFakeGoons()

    def __cleanupResistanceToon(self):
        self.__hideResistanceToon()
        if self.resistanceToon:
            self.resistanceToon.removeActive()
            self.resistanceToon.delete()
            self.resistanceToon = None

            for i in range(self.numFakeGoons):
                self.fakeGoons[i].disable()
                self.fakeGoons[i].delete()
                self.fakeGoons[i] = None

    def __showResistanceToon(self, withSuit):
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
        if self.resistanceToonOnstage:
            self.resistanceToon.removeActive()
            self.resistanceToon.detachNode()
            self.resistanceToonOnstage = 0

    def __hideFakeGoons(self):
        if self.fakeGoons:
            for goon in self.fakeGoons:
                goon.request('Off')

    def __showFakeGoons(self, state):
        print self.fakeGoons
        if self.fakeGoons:
            for goon in self.fakeGoons:
                goon.request(state)

            

    ##### Environment #####

    def loadEnvironment(self):
        DistributedBossCog.DistributedBossCog.loadEnvironment(self)

        self.midVault = loader.loadModel('phase_10/models/cogHQ/MidVault.bam')
        self.endVault = loader.loadModel('phase_10/models/cogHQ/EndVault.bam')
        self.lightning = loader.loadModel('phase_10/models/cogHQ/CBLightning.bam')
        self.magnet = loader.loadModel('phase_10/models/cogHQ/CBMagnet.bam')
        self.craneArm = loader.loadModel('phase_10/models/cogHQ/CBCraneArm.bam')
        self.controls = loader.loadModel('phase_10/models/cogHQ/CBCraneControls.bam')
        self.stick = loader.loadModel('phase_10/models/cogHQ/CBCraneStick.bam')
        self.safe = loader.loadModel('phase_10/models/cogHQ/CBSafe.bam')
        self.eyes = loader.loadModel('phase_10/models/cogHQ/CashBotBossEyes.bam')
        self.cableTex = self.craneArm.findTexture('MagnetControl')

        # Get the eyes ready for putting outside the helmet.
        self.eyes.setPosHprScale(4.5, 0, -2.5,
                                 90, 90, 0,
                                 0.4, 0.4, 0.4)
        self.eyes.reparentTo(self.neck)
        self.eyes.hide()

        # Position the two rooms relative to each other, and so that
        # the floor is at z == 0
        self.midVault.setPos(0, -222, -70.7)
        self.endVault.setPos(84, -201, -6)

        self.geom = NodePath('geom')
        self.midVault.reparentTo(self.geom)
        self.endVault.reparentTo(self.geom)

        # Clear out unneeded backstage models from the EndVault, if
        # they're in the file.
        self.endVault.findAllMatches('**/MagnetArms').detach()
        self.endVault.findAllMatches('**/Safes').detach()
        self.endVault.findAllMatches('**/MagnetControlsAll').detach()

        # Flag the collisions in the end vault so safes and magnets
        # don't try to go through the wall.
        cn = self.endVault.find('**/wallsCollision').node()
        cn.setIntoCollideMask(OTPGlobals.WallBitmask | ToontownGlobals.PieBitmask | (BitMask32.lowerOn(3) << 21))        

        # Get the rolling doors.

        # This is the door to Somewhere Else, through which the boss
        # makes his entrance.
        self.door1 = self.midVault.find('**/SlidingDoor1/')

        # This is the door from the mid vault to the end vault.
        # Everyone proceeds through this door to the final battle
        # scene.
        self.door2 = self.midVault.find('**/SlidingDoor/')

        # This is the door from the end vault back to the mid vault.
        # The boss makes his "escape" through this door.
        self.door3 = self.endVault.find('**/SlidingDoor/')

        # Load the elevator model
        elevatorModel = loader.loadModel("phase_10/models/cogHQ/CFOElevator")

        # Set up an origin for the elevator.
        elevatorOrigin = self.midVault.find('**/elevator_origin')
        elevatorOrigin.setScale(1)

        elevatorModel.reparentTo(elevatorOrigin)

        leftDoor = elevatorModel.find('**/left_door')
        leftDoor.setName("left-door")
        rightDoor = elevatorModel.find('**/right_door')
        rightDoor.setName("right-door")
        self.setupElevator(elevatorOrigin)
        ElevatorUtils.closeDoors(leftDoor, rightDoor, ElevatorConstants.ELEVATOR_CFO)

        # Find all the wall polygons and replace them with planes,
        # which are solid, so there will be zero chance of safes or
        # toons slipping through a wall.
        walls = self.endVault.find('**/RollUpFrameCillison')
        walls.detachNode()
        self.evWalls = self.replaceCollisionPolysWithPlanes(walls)
        self.evWalls.reparentTo(self.endVault)

        # Initially, these new planar walls are stashed, so they don't
        # cause us trouble in the intro movie or in battle one.  We
        # will unstash them when we move to battle three.
        self.evWalls.stash()
        
        # Also replace the floor polygon with a plane, and rename it
        # so we can detect a collision with it.
        floor = self.endVault.find('**/EndVaultFloorCollision')
        floor.detachNode()
        self.evFloor = self.replaceCollisionPolysWithPlanes(floor)
        self.evFloor.reparentTo(self.endVault)
        self.evFloor.setName('floor')

        # Also, put a big plane across the universe a few feet below
        # the floor, to catch things that fall out of the world.
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        planeNode = CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geom.attachNewNode(planeNode)

        self.geom.reparentTo(render)

    def unloadEnvironment(self):
        DistributedBossCog.DistributedBossCog.unloadEnvironment(self)
        
        self.geom.removeNode()

    def replaceCollisionPolysWithPlanes(self, model):
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
                    

    def __makeGoonMovieForIntro(self):
        goonTrack = Parallel()
        goon = self.fakeGoons[0]
        goonTrack.append(
            Sequence(goon.posHprInterval(0, Point3(111, -287, 0), VBase3(165, 0, 0)),
                     goon.posHprInterval(9, Point3(101, -323, 0), VBase3(165, 0, 0)),
                     goon.hprInterval(1, VBase3(345, 0, 0)),
                     goon.posHprInterval(9, Point3(111, -287, 0), VBase3(345, 0, 0)),
                     goon.hprInterval(1, VBase3(165, 0, 0)),
                     goon.posHprInterval(9.5, Point3(104, -316, 0), VBase3(165, 0, 0)),
                     #Wait(3.5),
                     Func(goon.request, 'Stunned'),
                     Wait(1),
                     )
            )
        goon = self.fakeGoons[1]
        goonTrack.append(
            Sequence(goon.posHprInterval(0, Point3(119, -315, 0), VBase3(357, 0, 0)),
                     goon.posHprInterval(9, Point3(121, -280, 0), VBase3(357, 0, 0)),
                     goon.hprInterval(1, VBase3(177, 0, 0)),
                     goon.posHprInterval(9, Point3(119, -315, 0), VBase3(177, 0, 0)),
                     goon.hprInterval(1, VBase3(357, 0, 0)),
                     goon.posHprInterval(9, Point3(121, -280, 0), VBase3(357, 0, 0)),
                     )
            )
        goon = self.fakeGoons[2]
        goonTrack.append(
            Sequence(goon.posHprInterval(0, Point3(102, -320, 0), VBase3(231, 0, 0)),
                     goon.posHprInterval(9, Point3(127, -337, 0), VBase3(231, 0, 0)),
                     goon.hprInterval(1, VBase3(51, 0, 0)),
                     goon.posHprInterval(9, Point3(102, -320, 0), VBase3(51, 0, 0)),
                     goon.hprInterval(1, VBase3(231, 0, 0)),
                     goon.posHprInterval(9, Point3(127, -337, 0), VBase3(231, 0, 0)),
                     )
            )
        return Sequence(Func(self.__showFakeGoons, 'Walk'),
                        goonTrack,
                        Func(self.__hideFakeGoons))
        
    def makeIntroductionMovie(self, delayDeletes):

        # Generate an interval which shows the toons meeting the
        # Resistance Toon, and the introduction of the CFO, etc.,
        # leading to the events of battle one.

        # We need to protect our movie against any of the toons
        # disconnecting while the movie plays.
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete.DelayDelete(
                    toon, 'CashbotBoss.makeIntroductionMovie'))

        rtTrack = Sequence()

        startPos = Point3(ToontownGlobals.CashbotBossOffstagePosHpr[0],
                          ToontownGlobals.CashbotBossOffstagePosHpr[1],
                          ToontownGlobals.CashbotBossOffstagePosHpr[2])
        battlePos = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[0],
                           ToontownGlobals.CashbotBossBattleOnePosHpr[1],
                           ToontownGlobals.CashbotBossBattleOnePosHpr[2])
        battleHpr = VBase3(ToontownGlobals.CashbotBossBattleOnePosHpr[3],
                           ToontownGlobals.CashbotBossBattleOnePosHpr[4],
                           ToontownGlobals.CashbotBossBattleOnePosHpr[5])

        bossTrack = Sequence()

        # Put him on stage.
        bossTrack.append(Func(self.reparentTo, render))
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisForwardHpr))
        bossTrack.append(Func(self.loop, 'Ff_neutral'))

        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(battlePos, hpr, battlePos, battleHpr, 0)
        bossTrack.append(track)

        bossTrack.append(Func(self.getGeomNode().setH, 0))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisReversedHpr))

        # Create a track for the fake goons
        goonTrack = self.__makeGoonMovieForIntro()
        
        attackToons = TTL.CashbotBossCogAttack

        rToon = self.resistanceToon
        rToon.setPosHpr(*ToontownGlobals.CashbotRTBattleOneStartPosHpr)

        track = Sequence(
            #Cut to resistance toon
            Func(camera.setPosHpr, 82, -219, 5, 267, 0, 0),
            Func(rToon.setChatAbsolute, TTL.ResistanceToonWelcome, CFSpeech),
            Wait(3),

            #start the goons on their paths
            Sequence(goonTrack, duration=0),
            #Func(goonTrack.start),
            
            #RT runs to the endvault door and opens it
            Parallel(camera.posHprInterval(4, Point3(108, -244, 4), VBase3(211.5, 0, 0)),
                     Sequence(Func(rToon.suit.setPlayRate, 1.4, 'walk'),
                              Func(rToon.suit.loop, 'walk'),
                              Parallel(rToon.hprInterval(1, VBase3(180, 0, 0)),
                                       rToon.posInterval(3, VBase3(120, -255, 0)),
                                       Sequence(Wait(2),     #clear the chat 2 seconds in
                                                Func(rToon.clearChat),
                                                ),
                                       ),
                              Func(rToon.suit.loop, 'neutral'),
                              self.door2.posInterval(3, VBase3(0, 0, 30)),
                              ),
                     ),
                     

            
            #Cut to the CFO rolling in
            Func(rToon.setHpr, 0, 0, 0),
            Func(rToon.setChatAbsolute, TTL.ResistanceToonTooLate, CFSpeech),
            Func(camera.reparentTo, render),
            Func(camera.setPosHpr, 61.1, -228.8, 10.2, -90, 0, 0),
            #Open the CFO door
            self.door1.posInterval(2, VBase3(0, 0, 30)),
            #Roll the CFO in and close the door
            Parallel(bossTrack,
                     Sequence(Wait(3),
                              Func(rToon.clearChat),
                              self.door1.posInterval(3, VBase3(0, 0, 0))),
                     ),
                              

            #Close-up of the CFO...
            Func(self.setChatAbsolute, TTL.CashbotBossDiscoverToons1, CFSpeech),
            camera.posHprInterval(1.5, Point3(93.3, -230, 0.7), VBase3(-92.9, 39.7, 8.3)),
            Func(self.setChatAbsolute, TTL.CashbotBossDiscoverToons2, CFSpeech),
            Wait(4),
            
            # Cut to toons losing their cog suits.
            Func(self.clearChat),
            self.loseCogSuits(self.toonsA + self.toonsB, render, (113,-228,10,90,0,0)),
            Wait(1),
            Func(rToon.setHpr, 0, 0, 0),
            self.loseCogSuits([rToon], render, (133,-243,5,143,0,0), True),

            #RT tells the toons to fight and runs off to open the door
            Func(rToon.setChatAbsolute, TTL.ResistanceToonKeepHimBusy, CFSpeech),
            Wait(1),
            Func(self.__showResistanceToon, False),  #this turns off his cog suit...
            Sequence(Func(rToon.animFSM.request, 'run'),
                     rToon.hprInterval(1, VBase3(180, 0, 0)),  #turn him around
                     Parallel(Sequence(rToon.posInterval(1.5, VBase3(109, -294, 0)),
                                       Parallel(Func(rToon.animFSM.request, 'jump')),
                                       rToon.posInterval(1.5, VBase3(93.935, -341.065, 2)),
                                       ),
                              self.door2.posInterval(3, VBase3(0, 0, 0))),
                     Func(rToon.animFSM.request, 'neutral'),
                     ),

            #clean up the toons' eyes
            self.toonNormalEyes(self.involvedToons),
            self.toonNormalEyes([self.resistanceToon], True),

            #cut back to the CFO and move the toons in to place
            Func(rToon.clearChat),
            Func(camera.setPosHpr, 93.3, -230, 0.7, -92.9, 39.7, 8.3),

            Func(self.setChatAbsolute, attackToons, CFSpeech),
            Wait(2),
            Func(self.clearChat),
            )

        return Sequence(Func(camera.reparentTo, render),
                        track)

    def __makeGoonMovieForBattleThree(self):
        #start them each walking back and forth between 2 points
        goonPosHprs = [
            [Point3(111, -287, 0), VBase3(165, 0, 0),
             Point3(101, -323, 0), VBase3(165, 0, 0) ],
            [Point3(119, -315, 0), VBase3(357, 0, 0),
             Point3(121, -280, 0), VBase3(357, 0, 0) ],
            [Point3(102, -320, 0), VBase3(231, 0, 0),
             Point3(127, -337, 0), VBase3(231, 0, 0) ]
            ]

        #we're gonna leave this guy on the side... stunned
        mainGoon = self.fakeGoons[0]
        
        goonLoop = Parallel()
        print self.fakeGoons
        for i in range(1, self.numFakeGoons):
            #print i
            goon = self.fakeGoons[i]
            goonLoop.append(
                Sequence(goon.posHprInterval(8, goonPosHprs[i][0], goonPosHprs[i][1]),
                         goon.posHprInterval(8, goonPosHprs[i][2], goonPosHprs[i][3]),
                         )
                )

        goonTrack = Sequence(
            Func(self.__showFakeGoons, 'Walk'),
            Func(mainGoon.request, 'Stunned'),
            Func(goonLoop.loop),
            Wait(20),
            #Func(self.__hideFakeGoons),
            )
        return goonTrack
        
    def makePrepareBattleThreeMovie(self, delayDeletes, crane, safe):

        # Generate an interval which shows the toons meeting the
        # Resistance Toon, and the introduction of the CFO, etc.,
        # leading to the events of battle one.
            
        # We need to protect our movie against any of the toons
        # disconnecting while the movie plays.
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                delayDeletes.append(DelayDelete.DelayDelete(
                    toon, 'CashbotBoss.makePrepareBattleThreeMovie'))

        startPos = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[0],
                          ToontownGlobals.CashbotBossBattleOnePosHpr[1],
                          ToontownGlobals.CashbotBossBattleOnePosHpr[2])
        battlePos = Point3(ToontownGlobals.CashbotBossBattleThreePosHpr[0],
                           ToontownGlobals.CashbotBossBattleThreePosHpr[1],
                           ToontownGlobals.CashbotBossBattleThreePosHpr[2])
        startHpr = Point3(ToontownGlobals.CashbotBossBattleOnePosHpr[3],
                          ToontownGlobals.CashbotBossBattleOnePosHpr[4],
                          ToontownGlobals.CashbotBossBattleOnePosHpr[5])
        battleHpr = VBase3(ToontownGlobals.CashbotBossBattleThreePosHpr[3],
                           ToontownGlobals.CashbotBossBattleThreePosHpr[4],
                           ToontownGlobals.CashbotBossBattleThreePosHpr[5])
        finalHpr = VBase3(135, 0, 0)

        bossTrack = Sequence()

        bossTrack.append(Func(self.reparentTo, render))
        bossTrack.append(Func(self.getGeomNode().setH, 180))
        bossTrack.append(Func(self.pelvis.setHpr, self.pelvisForwardHpr))
        bossTrack.append(Func(self.loop, 'Ff_neutral'))

        track, hpr = self.rollBossToPoint(startPos, startHpr, startPos, battleHpr, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(startPos, None, battlePos, None, 0)
        bossTrack.append(track)
        track, hpr = self.rollBossToPoint(battlePos, battleHpr, battlePos, finalHpr, 0)
        bossTrack.append(track)

        #bossTrack.append(Func(self.getGeomNode().setH, 0))

        #grab the resistance toon and put him in his starting spot
        rToon = self.resistanceToon
        rToon.setPosHpr(93.935, -341.065, 0, -45, 0, 0)

        #get a crane/goon to play with
        goon = self.fakeGoons[0]
        crane = self.cranes[0]

        #craneTrack = Sequence(crane.crane.posInterval(1, Point3(0, 30, 0)),
        #                      Wait(0.5),
        #                      crane.crane.posInterval(1, Point3(0, 20, 0)),
        #                      Wait(0.5),
        #                      )

        # create a track for the goons in the scene  (this only goes to the
        # point of interaction with the resistance toon
        #goonTrack = self.__makeGoonMovieForBattleThree()
        
        #build the sequence
        track = Sequence(
            Func(self.__hideToons),
            #set up the crane and goon
            Func(crane.request, 'Movie'),
            #Func(goon.request, 'LocalGrabbed', -1, crane.doId),
            Func(crane.accomodateToon, rToon),
            Func(goon.request, 'Stunned'),
            Func(goon.setPosHpr, 104, -316, 0, 165, 0, 0),

            #open the door and roll the boss through
            Parallel(self.door2.posInterval(4.5, VBase3(0, 0, 30)),
                     self.door3.posInterval(4.5, VBase3(0, 0, 30)),
                     bossTrack,
                     ),

            #Cut to the resistance toon... he's gonna show the players something
            Func(rToon.loop, 'leverNeutral'),
            Func(camera.reparentTo, self.geom),
            Func(camera.setPosHpr, 105, -326, 5, 136.3, 0, 0),
            Func(rToon.setChatAbsolute, TTL.ResistanceToonWatchThis, CFSpeech),
            Wait(2),
            Func(rToon.clearChat),

            #Cut to the CFO telling the RT to knock it off
            Func(camera.setPosHpr, 105, -326, 20, -45.3, 11, 0),
            Func(self.setChatAbsolute, TTL.CashbotBossGetAwayFromThat, CFSpeech),
            Wait(2),
            Func(self.clearChat),

            #The RT is having fun... cut to him doing the safe thing
            camera.posHprInterval(1.5, Point3(105, -326, 5),
                                  Point3(136.3, 0, 0),
                                  blendType='easeInOut'),

            #tell em what to do
            Func(rToon.setChatAbsolute, TTL.ResistanceToonCraneInstructions1, CFSpeech),
            Wait(4),

            Func(rToon.setChatAbsolute, TTL.ResistanceToonCraneInstructions2, CFSpeech),
            Wait(4),

            Func(rToon.setChatAbsolute, TTL.ResistanceToonCraneInstructions3, CFSpeech),
            Wait(4),

            Func(rToon.setChatAbsolute, TTL.ResistanceToonCraneInstructions4, CFSpeech),
            Wait(4),

            Func(rToon.clearChat),

            # Cut to the recovering goon
            Func(camera.setPosHpr, 102, -323.6, 0.9, -10.6, 14, 0),
            Func(goon.request, 'Recovery'),
            Wait(2),

            # Cut to the surprised resistance toon 
            Func(camera.setPosHpr, 95.4, -332.6, 4.2, 167.1, -13.2, 0),
            Func(rToon.setChatAbsolute, TTL.ResistanceToonGetaway, CFSpeech),
            Func(rToon.animFSM.request, 'jump'),
            Wait(1.8),
            Func(rToon.clearChat),

            #Cut to the goon chasing rtoon... close the door
            Func(camera.setPosHpr, 109.1, -300.7, 13.9, -15.6, -13.6, 0),
            Func(rToon.animFSM.request, 'run'),
            Func(goon.request, 'Walk'),
            Parallel(self.door3.posInterval(3, VBase3(0, 0, 0)),
                     rToon.posHprInterval(3, Point3(136, -212.9, 0), VBase3(-14,0,0),
                                          startPos = Point3(110.8, -292.7, 0),
                                          startHpr = VBase3(-14, 0, 0)),
                     goon.posHprInterval(3, Point3(125.2, -243.5, 0), VBase3(-14,0,0),
                                         startPos = Point3(104.8, -309.5, 0),
                                         startHpr = VBase3(-14, 0, 0)),
                     ),

            Func(self.__hideFakeGoons),
            Func(crane.request, 'Free'),

            #fix the CFO's orientation
            Func(self.getGeomNode().setH, 0),
        
            #move the toons to their positions
            self.moveToonsToBattleThreePos(self.involvedToons),

            Func(self.__showToons),
            )

        return Sequence(Func(camera.reparentTo, self),
                        Func(camera.setPosHpr, 0, -27, 25, 0, -18, 0),
                        track)

    def moveToonsToBattleThreePos(self, toons):
        track = Parallel()
        for i in range(len(toons)):
            toon = base.cr.doId2do.get(toons[i])
            if toon:
                posHpr = ToontownGlobals.CashbotToonsBattleThreeStartPosHpr[i]
                pos = Point3(*posHpr[0:3])
                hpr = VBase3(*posHpr[3:6])
                track.append(
                    toon.posHprInterval(0.2, pos, hpr)
                    )

        return track
                
    def makeBossFleeMovie(self):
        # Generate an interval which shows the boss giving up and
        # running out the door, only to be nailed by a passing train.

        hadEnough = TTLocalizer.CashbotBossHadEnough
        outtaHere = TTLocalizer.CashbotBossOuttaHere

        loco = loader.loadModel('phase_10/models/cogHQ/CashBotLocomotive')
        car1 = loader.loadModel('phase_10/models/cogHQ/CashBotBoxCar')
        car2 = loader.loadModel('phase_10/models/cogHQ/CashBotTankCar')
        trainPassingSfx = base.loadSfx('phase_10/audio/sfx/CBHQ_TRAIN_pass.mp3')
        boomSfx = loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.mp3')

        rollThroughDoor = self.rollBossToPoint(
            fromPos = Point3(120, -280, 0), fromHpr = None,
            toPos = Point3(120, -250, 0), toHpr = None,
            reverse = 0)
        rollTrack = Sequence(
            Func(self.getGeomNode().setH, 180),
            rollThroughDoor[0],
            Func(self.getGeomNode().setH, 0))

        # Generate a track that shows one long train running by (which
        # it achieves by running the same two cars repeatedly past
        # the door).

        # The trains move at 300 ft/s, so a gap of this much time puts
        # car2 80 ft behind car1.
        g = 80.0/300.0
        trainTrack = Track(
            (0*g, loco.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (1*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (2*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (3*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (4*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (5*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (6*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (7*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (8*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (9*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (10*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (11*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (12*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (13*g, car2.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            (14*g, car1.posInterval(0.5, Point3(0, -242, 0), startPos=Point3(150, -242, 0))),
            )

        bossTrack = Track(
            (0.0, Sequence(Func(camera.reparentTo, render),
                           Func(camera.setPosHpr, 105, -280, 20, -158, -3, 0),
                           Func(self.reparentTo, render),
                           Func(self.show),
                           Func(self.clearChat),
                           Func(self.setPosHpr, *ToontownGlobals.CashbotBossBattleThreePosHpr),
                           Func(self.reverseHead),
                           ActorInterval(self, 'Fb_firstHit'),
                           ActorInterval(self, 'Fb_down2Up'))),
            (1.0, Func(self.setChatAbsolute, hadEnough, CFSpeech)),
            (5.5, Parallel(Func(camera.setPosHpr, 100, -315, 16, -20, 0, 0),
                           Func(self.hideBattleThreeObjects),
                           Func(self.forwardHead),
                           Func(self.loop, 'Ff_neutral'),
                           rollTrack,
                           self.door3.posInterval(2.5, Point3(0, 0, 25),
                                                  startPos = Point3(0, 0, 18)),
                           )),
            (5.5, Func(self.setChatAbsolute, outtaHere, CFSpeech)),
            (5.5, SoundInterval(trainPassingSfx)),
            (8.1, Func(self.clearChat)),
            (9.4, Sequence(Func(loco.reparentTo, render),
                           Func(car1.reparentTo, render),
                           Func(car2.reparentTo, render),
                           trainTrack,
                           Func(loco.detachNode),
                           Func(car1.detachNode),
                           Func(car2.detachNode),
                           Wait(2))),
            (9.5, SoundInterval(boomSfx)),
            (9.5, Sequence(self.posInterval(0.4, Point3(0, -250, 0)),
                           Func(self.stash))),
            )
            
        return bossTrack

    def grabObject(self, obj):
        # Grab a safe and put it on as a helmet.  This method mirrors
        # a similar method on DistributedCashbotBossCrane.py; it goes
        # through the same API as a crane picking up a safe.

        # This is only called by DistributedCashbotBossObject.enterGrabbed().
        assert self.heldObject == None
        
        obj.wrtReparentTo(self.neck)
        obj.hideShadows()
        obj.stashCollisions()

        if obj.lerpInterval:
            obj.lerpInterval.finish()

        obj.lerpInterval = Parallel(
            obj.posInterval(ToontownGlobals.CashbotBossToMagnetTime, Point3(-1, 0, 0.2)),
            obj.quatInterval(ToontownGlobals.CashbotBossToMagnetTime, VBase3(0, -90, 90)),
            Sequence(Wait(ToontownGlobals.CashbotBossToMagnetTime), ShowInterval(self.eyes)),
            obj.toMagnetSoundInterval)
        obj.lerpInterval.start()

        self.heldObject = obj

    def dropObject(self, obj):
        # Drop a helmet on the ground.
        
        # This is only called by DistributedCashbotBossObject.exitGrabbed().
        assert self.heldObject == obj

        if obj.lerpInterval:
            obj.lerpInterval.finish()
            obj.lerpInterval = None
        
        obj = self.heldObject
        obj.wrtReparentTo(render)
        obj.setHpr(obj.getH(), 0, 0)
        self.eyes.hide()

        # Actually, we shouldn't reveal the shadows until it
        # reaches the ground again.  This will do for now.
        obj.showShadows()
        obj.unstashCollisions()

        self.heldObject = None

    def setBossDamage(self, bossDamage):
        if bossDamage > self.bossDamage:
            delta = bossDamage - self.bossDamage
            self.flashRed()
            self.doAnimate('hit', now=1)
            self.showHpText(-delta, scale = 5)
            
        self.bossDamage = bossDamage
        self.updateHealthBar()

    def setRewardId(self, rewardId):
        self.rewardId = rewardId

    def d_applyReward(self):
        self.sendUpdate('applyReward', [])

    def stunAllGoons(self):
        # This is called by the "~bossBattle stun" magic word only.
        # It stuns all of the goons in the final battle sequence.

        for goon in self.goons:
            if goon.state == 'Walk' or goon.state == 'Battle':
                goon.demand("Stunned")
                goon.sendUpdate("requestStunned", [0])

    def destroyAllGoons(self):
        # This is called by the "~bossBattle destroy" magic word only.
        # It destroys all of the goons in the final battle sequence.

        for goon in self.goons:
            if goon.state != 'Off' and not goon.isDead:
                goon.b_destroyGoon()

    def deactivateCranes(self):
        # This locally knocks all toons off cranes.
        for crane in self.cranes.values():
            crane.demand("Free")

    def hideBattleThreeObjects(self):
        # This turns off all the goons, safes, and cranes on the local
        # client.  It's played only during the victory movie, to get
        # these guys out of the way.

        for goon in self.goons:
            goon.demand("Off")

        for safe in self.safes.values():
            safe.demand("Off")

        for crane in self.cranes.values():
            crane.demand("Off")

    def __doPhysics(self, task):
        dt = globalClock.getDt()
        self.physicsMgr.doPhysics(dt)
        return Task.cont

    def __hideToons(self):
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.hide()

    def __showToons(self):
        for toonId in self.involvedToons:
            toon = self.cr.doId2do.get(toonId)
            if toon:
                toon.show()

    def __arrangeToonsAroundResistanceToon(self):
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

    def __talkAboutPromotion(self, speech):
        # Extends the congratulations speech to talk about the earned
        # promotion, if any.  Returns the newly-extended speech.
        
        # don't say anything about a promotion if they've maxed their cog suit
        if self.prevCogSuitLevel < ToontownGlobals.MaxCogSuitLevel:
            newCogSuitLevel = localAvatar.getCogLevels()[
                CogDisguiseGlobals.dept2deptIndex(self.style.dept)]
            # if this is their last promotion, tell them
            if newCogSuitLevel == ToontownGlobals.MaxCogSuitLevel:
                speech += TTLocalizer.ResistanceToonLastPromotion % (ToontownGlobals.MaxCogSuitLevel+1)
            # if they're getting another LP, tell them
            if newCogSuitLevel in ToontownGlobals.CogSuitHPLevels:
                speech += TTLocalizer.ResistanceToonHPBoost
        else:
            # level XX, wow! Thanks for coming back!
            speech += TTLocalizer.ResistanceToonMaxed % (ToontownGlobals.MaxCogSuitLevel+1)

        return speech

    ##### Off state #####

    def enterOff(self):
        DistributedBossCog.DistributedBossCog.enterOff(self)

        if self.resistanceToon:
            self.resistanceToon.clearChat()

    ##### WaitForToons state #####

    def enterWaitForToons(self):
        DistributedBossCog.DistributedBossCog.enterWaitForToons(self)

        self.detachNode()
        self.geom.hide()

        # Disable the caged toon's nametag while we're here in space
        # waiting.
        self.resistanceToon.removeActive()

    def exitWaitForToons(self):
        DistributedBossCog.DistributedBossCog.exitWaitForToons(self)

        self.geom.show()
        self.resistanceToon.addActive()


    ##### Elevator state #####

    def enterElevator(self):
        DistributedBossCog.DistributedBossCog.enterElevator(self)

        # The CFO himself is offstage at this point.
        self.detachNode()

        # Disable the caged toon's nametag while we're in the
        # elevator.
        self.resistanceToon.removeActive()

        self.endVault.stash()
        self.midVault.unstash()
        self.__showResistanceToon(True)
        
    def exitElevator(self):
        DistributedBossCog.DistributedBossCog.exitElevator(self)

        self.resistanceToon.addActive()

    ##### Introduction state #####

    def enterIntroduction(self):
        # Initially, the boss cog is offstage.
        self.detachNode()
        self.stopAnimate()

        self.endVault.unstash()
        self.evWalls.stash()
        self.midVault.unstash()
        self.__showResistanceToon(True)

        base.playMusic(self.stingMusic, looping=1, volume=0.9)

        DistributedBossCog.DistributedBossCog.enterIntroduction(self)

    def exitIntroduction(self):
        DistributedBossCog.DistributedBossCog.exitIntroduction(self)

        self.stingMusic.stop()
        
    ##### BattleOne state #####

    def enterBattleOne(self):
        DistributedBossCog.DistributedBossCog.enterBattleOne(self)

        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleOnePosHpr)
        self.show()
        self.pelvis.setHpr(self.pelvisReversedHpr)
        self.doAnimate()

        self.endVault.stash()
        self.midVault.unstash()
        self.__hideResistanceToon()

    def exitBattleOne(self):
        DistributedBossCog.DistributedBossCog.exitBattleOne(self)

    ##### PrepareBattleThree state #####

    def enterPrepareBattleThree(self):
        assert self.notify.debug('enterPrepareBattleThree()')

        self.controlToons()

        NametagGlobals.setMasterArrowsOn(0)

        intervalName = "PrepareBattleThreeMovie"
        delayDeletes = []

        #grab a crane and put it in to Movie mode
        self.movieCrane = self.cranes[0]
        self.movieSafe = self.safes[1]
        self.movieCrane.request('Movie')

        seq = Sequence(self.makePrepareBattleThreeMovie(delayDeletes,
                                                        self.movieCrane,
                                                        self.movieSafe),
                       Func(self.__beginBattleThree),
                       name = intervalName)
        seq.delayDeletes = delayDeletes
        seq.start()
        self.storeInterval(seq, intervalName)

        self.endVault.unstash()
        self.evWalls.stash()
        self.midVault.unstash()
        self.__showResistanceToon(False)

        taskMgr.add(self.__doPhysics, self.uniqueName('physics'),
                    priority = 25)

    def __beginBattleThree(self):
        intervalName = "PrepareBattleThreeMovie"
        self.clearInterval(intervalName)
        
        self.doneBarrier('PrepareBattleThree')
        
    def exitPrepareBattleThree(self):
        intervalName = "PrepareBattleThreeMovie"
        self.clearInterval(intervalName)
        self.unstickToons()
        self.releaseToons()

        if self.newState == 'BattleThree':
            self.movieCrane.request('Free')
            self.movieSafe.request('Initial')

        NametagGlobals.setMasterArrowsOn(1)

        # Make sure the elevator doors are closed.
        ElevatorUtils.closeDoors(self.leftDoor, self.rightDoor, ElevatorConstants.ELEVATOR_CFO)

        taskMgr.remove(self.uniqueName('physics'))


    ##### BattleThree state #####

    def enterBattleThree(self):
        assert self.notify.debug('enterBattleThree()')
        DistributedBossCog.DistributedBossCog.enterBattleThree(self)

        self.clearChat()
        self.resistanceToon.clearChat()
        self.reparentTo(render)

        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)

        self.happy = 1
        self.raised = 1
        self.forward = 1
        self.doAnimate()

        self.endVault.unstash()
        self.evWalls.unstash()
        self.midVault.stash()
        self.__hideResistanceToon()

        localAvatar.setCameraFov(ToontownGlobals.BossBattleCameraFov)

        self.generateHealthBar()
        self.updateHealthBar()

        base.playMusic(self.battleThreeMusic, looping=1, volume=0.9)

        # It is important to make sure this task runs immediately
        # before the collisionLoop of ShowBase.  That will fix up the
        # z value of the safes, etc., before their position is
        # distributed.
        taskMgr.add(self.__doPhysics, self.uniqueName('physics'),
                    priority = 25)

    def exitBattleThree(self):
        DistributedBossCog.DistributedBossCog.exitBattleThree(self)
        bossDoneEventName = self.uniqueName('DestroyedBoss')
        self.ignore(bossDoneEventName)

        self.stopAnimate()
        self.cleanupAttacks()
        self.setDizzy(0)

        self.removeHealthBar()

        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)

        if self.newState != 'Victory':
            self.battleThreeMusic.stop()

        taskMgr.remove(self.uniqueName('physics'))
        

    ##### Victory state #####

    def enterVictory(self):
        assert self.notify.debug('enterVictory()')
        # No more intervals should be playing.
        self.cleanupIntervals()

        # Boss Cog flees out the door and gets nailed by a passing
        # train.
        self.reparentTo(render)
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)
        self.stopAnimate()

        self.endVault.unstash()
        self.evWalls.unstash()
        self.midVault.unstash()
        self.__hideResistanceToon()
        self.__hideToons()

        self.clearChat()
        self.resistanceToon.clearChat()

        # Important to knock toons off cranes before we control them.
        self.deactivateCranes()

        # This particular crane might get in the way of the camera.
        if self.cranes:
            self.cranes[1].demand('Off')

        # No one owns the toons.
        self.releaseToons(finalBattle = 1)

        # But, we do need to be in movie mode.
        if self.hasLocalToon():
            self.toMovieMode()

        intervalName = "VictoryMovie"

        seq = Sequence(self.makeBossFleeMovie(),
                       Func(self.__continueVictory),
                       name = intervalName)
        seq.start()
        self.storeInterval(seq, intervalName)

        if self.oldState != 'BattleThree':
            base.playMusic(self.battleThreeMusic, looping=1, volume=0.9)

    def __continueVictory(self):
        # Ok, he's gone!  We all move to the reward movie.
        
        self.doneBarrier('Victory')

    def exitVictory(self):
        self.cleanupIntervals()

        # We don't want to release the local toon if we're moving on
        # to the Reward state, since they need to keep dancing.
        if self.newState != 'Reward':
            if self.hasLocalToon():
                self.toWalkMode()

        self.__showToons()

        self.door3.setPos(0, 0, 0)

        if self.newState != 'Reward':
            self.battleThreeMusic.stop()

    ##### Reward state #####

    def enterReward(self):
        assert self.notify.debug('enterReward()')
        # No more intervals should be playing.
        self.cleanupIntervals()
        self.clearChat()
        self.resistanceToon.clearChat()

        # Boss Cog is gone.
        self.stash()
        self.stopAnimate()

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
                delayDeletes.append(DelayDelete.DelayDelete(
                    toon, 'CashbotBoss.enterReward'))
                                    
        ival.delayDeletes = delayDeletes
        ival.start()
        self.storeInterval(ival, intervalName)

        if self.oldState != 'Victory':
            base.playMusic(self.battleThreeMusic, looping=1, volume=0.9)

    def __doneReward(self):
        self.doneBarrier('Reward')
        self.toWalkMode()

    def exitReward(self):
        intervalName = "RewardMovie"
        self.clearInterval(intervalName)

        if self.newState != 'Epilogue':
            self.releaseToons()

        self.unstash()
        self.rewardPanel.destroy()
        del self.rewardPanel

        self.battleThreeMusic.stop()

    ##### Epilogue state #####

    def enterEpilogue(self):
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
        self.resistanceToon.setPosHpr(*ToontownGlobals.CashbotBossBattleThreePosHpr)
        self.resistanceToon.loop('neutral')

        self.__arrangeToonsAroundResistanceToon()
        camera.reparentTo(render)
        camera.setPos(self.resistanceToon, -9, 12, 6)
        camera.lookAt(self.resistanceToon, 0, 0, 3)

        intervalName = "EpilogueMovie"

        text = ResistanceChat.getChatText(self.rewardId)
        menuIndex, itemIndex = ResistanceChat.decodeId(self.rewardId)
        value = ResistanceChat.getItemValue(self.rewardId)
        if menuIndex == ResistanceChat.RESISTANCE_TOONUP:
            if value == -1:
                instructions = TTLocalizer.ResistanceToonToonupAllInstructions
            else:
                instructions = TTLocalizer.ResistanceToonToonupInstructions % (
                    value)

        elif menuIndex == ResistanceChat.RESISTANCE_MONEY:
            if value == -1:
                instructions = TTLocalizer.ResistanceToonMoneyAllInstructions
            else:
                instructions = TTLocalizer.ResistanceToonMoneyInstructions % (
                    value)

        elif menuIndex == ResistanceChat.RESISTANCE_RESTOCK:
            if value == -1:
                instructions = TTLocalizer.ResistanceToonRestockAllInstructions
            else:
                trackName = TTLocalizer.BattleGlobalTracks[value]
                instructions = TTLocalizer.ResistanceToonRestockInstructions % (
                    trackName)
                
        speech = TTLocalizer.ResistanceToonCongratulations % (
            text, instructions)
        speech = self.__talkAboutPromotion(speech)

        self.resistanceToon.setLocalPageChat(speech, 0)

        self.accept("nextChatPage", self.__epilogueChatNext)
        self.accept("doneChatPage", self.__epilogueChatDone)

        base.playMusic(self.epilogueMusic, looping=1, volume=0.9)

    def __epilogueChatNext(self, pageNumber, elapsed):
        if pageNumber == 1:
            # "You're an asset to the Resistance."

            # We don't use the code in TTEmote here, because that
            # forces the toon to say stuff.  So we just steal the
            # ActorIntervals that apply the animation.
            toon = self.resistanceToon
            playRate = 0.75
            track = Sequence(ActorInterval(toon, 'victory', playRate = playRate, startFrame = 0, endFrame = 9),
                             ActorInterval(toon, 'victory', playRate = playRate, startFrame = 9, endFrame = 0),
                             Func(self.resistanceToon.loop, 'neutral'))
            intervalName = "EpilogueMovieToonAnim"
            self.storeInterval(track, intervalName)
            track.start()

        elif pageNumber == 3:
            # Page 3 is the special resistance chat.  Apply it.
            self.d_applyReward()
            ResistanceChat.doEffect(self.rewardId, self.resistanceToon, self.involvedToons)

    def __epilogueChatDone(self, elapsed):
        assert self.notify.debug('epilogueChatDone()')
        self.resistanceToon.setChatAbsolute(TTLocalizer.CagedToonGoodbye, CFSpeech)

        self.ignore("nextChatPage")
        self.ignore("doneChatPage")

        intervalName = "EpilogueMovieToonAnim"
        self.clearInterval(intervalName)
        track = Parallel(
            Sequence(ActorInterval(self.resistanceToon, 'wave'),
                     Func(self.resistanceToon.loop, 'neutral')),
            Sequence(Wait(0.5),
                     Func(self.localToonToSafeZone)))
        self.storeInterval(track, intervalName)
        track.start()
        
    def exitEpilogue(self):
        self.clearInterval("EpilogueMovieToonAnim")
        self.unstash()

        self.epilogueMusic.stop()

    ##### Frolic state #####

    # This state is probably only useful for debugging.  The toons are
    # all free to run around the world.

    def enterFrolic(self):
        DistributedBossCog.DistributedBossCog.enterFrolic(self)
        self.setPosHpr(*ToontownGlobals.CashbotBossBattleOnePosHpr)

        self.releaseToons()
        if self.hasLocalToon():
            self.toWalkMode()
        
        self.door3.setZ(25)
        self.door2.setZ(25)

        self.endVault.unstash()
        self.evWalls.stash()
        self.midVault.unstash()
        self.__hideResistanceToon()

    def exitFrolic(self):
        self.door3.setZ(0)
        self.door2.setZ(0)
