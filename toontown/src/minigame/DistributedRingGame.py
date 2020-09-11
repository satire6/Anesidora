"""DistributedRingGame module: contains the DistributedRingGame class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from DistributedMinigame import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import ArrowKeys
import Ring
import RingTrack
import RingGameGlobals
import RingGroup
import RingTrackGroups
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class DistributedRingGame(DistributedMinigame):

    UPDATE_ENVIRON_TASK   = "RingGameUpdateEnvironTask"
    UPDATE_LOCALTOON_TASK = "RingGameUpdateLocalToonTask"
    UPDATE_RINGS_TASK     = "RingGameUpdateRingsTask"
    UPDATE_SHADOWS_TASK   = "RingGameUpdateShadowsTask"
    COLLISION_DETECTION_TASK = "RingGameCollisionDetectionTask"
    END_GAME_WAIT_TASK    = "RingGameCollisionDetectionTask"

    COLLISION_DETECTION_PRIORITY = 5
    # update the shadow positions after collisions have been performed
    # but before render
    UPDATE_SHADOWS_PRIORITY = 47

    # result types
    RT_UNKNOWN      = 0
    RT_SUCCESS      = 1
    RT_GROUPSUCCESS = 2
    RT_FAILURE      = 3

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedRingGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['swim']),
                                State.State('swim',
                                            self.enterSwim,
                                            self.exitSwim,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                ],
                               # Initial State
                               'off',
                               # Final State
                               'cleanup',
                               )

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

    def getTitle(self):
        return TTLocalizer.RingGameTitle

    def getInstructions(self):
        p = self.avIdList.index(self.localAvId)

        if self.isSinglePlayer():
            text = TTLocalizer.RingGameInstructionsSinglePlayer
        else:
            text = TTLocalizer.RingGameInstructionsMultiPlayer

        return text % (RingGameGlobals.ringColors[self.colorIndices[p]][0])

    def getMaxDuration(self):
        # calling this here could be problematic; it's easy for now
        #self.defineConstants()
        return (
            (RingGameGlobals.NUM_RING_GROUPS * self.ringGroupArrivalPeriod) +
            self.T_FIRST_RING_GROUP_ARRIVES + self.GAME_END_DELAY)

    def defineConstants(self):
        # Z is up, Y is forward
        # define some tweakable constants
        #self.CAMERA_Y = -35
        #self.CAMERA_Z = -2
        self.CAMERA_Y = -15
        self.TOON_Y = 0
        self.FAR_PLANE_DIST = 150
        tScreenCenterToEdge = 1.
        self.TOONXZ_SPEED = RingGameGlobals.MAX_TOONXZ/tScreenCenterToEdge
        self.WATER_DEPTH = 35.
        self.ENVIRON_LENGTH = 150.
        self.ENVIRON_START_OFFSET = 20. # start _ feet into the environment
        self.TOON_INITIAL_SPACING = 4.
        waterZOffset = 3.
        self.SEA_FLOOR_Z = (-self.WATER_DEPTH/2.) + waterZOffset

        # in world coordinates
        farPlaneDist = (self.CAMERA_Y + self.FAR_PLANE_DIST) - self.TOON_Y

        # how many seconds between each ring group arrival?
        self.ringGroupArrivalPeriod = 3.
        # how much space is there between successive ring groups?
        self.RING_GROUP_SPACING = farPlaneDist / 2.

        self.TOON_SWIM_VEL = (self.RING_GROUP_SPACING /
                              self.ringGroupArrivalPeriod)

        self.T_FIRST_RING_GROUP_ARRIVES = farPlaneDist / self.TOON_SWIM_VEL

        self.WATER_COLOR = Vec4(0,0,0.6,1)

        self.SHADOW_Z_OFFSET = 0.1
        #self.SHADOW_MAX_SCALE = 0.6
        #self.SHADOW_MIN_SCALE = 0.35

        self.Y_VIS_MAX = self.FAR_PLANE_DIST
        self.Y_VIS_MIN = self.CAMERA_Y

        ringRadius = RingGameGlobals.RING_RADIUS * 1.025
        self.RING_RADIUS_SQRD = ringRadius * ringRadius

        self.GAME_END_DELAY = 1.

        self.RING_RESPONSE_DELAY = .1

        self.TOON_LOD = 1000

        self.NumRingGroups = 16

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)

        self.defineConstants()

        self.music = base.loadMusic(
            "phase_4/audio/bgm/MG_toontag.mid"
            )

        self.sndAmbience = base.loadSfx(
            'phase_4/audio/sfx/AV_ambient_water.mp3')
        self.sndPerfect = base.loadSfx(
            "phase_4/audio/sfx/ring_perfect.mp3")
        # don't use the 'swimming forward' sound; we're always swimming
        # forward, and the sound would get irritating

        # load the environment model (water, ground)
        loadBase = "phase_4/models/minigames/"
        self.environModel = loader.loadModel(loadBase + "swimming_game.bam")
        self.environModel.setPos(0,self.ENVIRON_LENGTH/2.,self.SEA_FLOOR_Z)
        self.environModel.flattenMedium()

        # load the ring
        self.ringModel = loader.loadModel(loadBase + "swimming_game_ring.bam")
        self.ringModel.setTransparency(1)
        modelRadius = 4.0
        self.ringModel.setScale(RingGameGlobals.RING_RADIUS / modelRadius)
        self.ringModel.flattenMedium()

        # load the drop shadow
        self.dropShadowModel = loader.loadModel(
            "phase_3/models/props/drop_shadow")
        self.dropShadowModel.setColor(0,0,0,0.5)
        self.dropShadowModel.flattenMedium()

        self.toonDropShadows = []
        self.ringDropShadows = []

        # this will be used to generate textnodes
        self.__textGen = TextNode("ringGame")
        self.__textGen.setFont(ToontownGlobals.getSignFont())
        self.__textGen.setAlign(TextNode.ACenter)

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        del self.__textGen
        del self.toonDropShadows
        del self.ringDropShadows
        self.dropShadowModel.removeNode()
        del self.dropShadowModel
        self.environModel.removeNode()
        del self.environModel
        self.ringModel.removeNode()
        del self.ringModel
        del self.music
        del self.sndAmbience
        del self.sndPerfect
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)

        # arrow key manager
        self.arrowKeys = ArrowKeys.ArrowKeys()

        toon = base.localAvatar
        toon.reparentTo(render)
        toon.setAnimState('swim', 1.0)
        toon.stopBobSwimTask()
        toon.useLOD(self.TOON_LOD)
        self.__placeToon(self.localAvId)
        # hide the avatar's dropshadow
        toon.dropShadow.hide()

        camera.reparentTo(render)
        #camera.setPosHpr(0,self.CAMERA_Y,self.CAMERA_Z,0,0,0)

        # make the camera follow the toon, and make it very wide angle
        camera.reparentTo(base.localAvatar)
        camera.setPosHpr(0, self.CAMERA_Y + self.TOON_Y, 0,
                         0, 0, 0)
        base.camLens.setFov(80)

        # set the far plane
        base.camLens.setFar(self.FAR_PLANE_DIST)

        # set the background color
        base.setBackgroundColor(self.WATER_COLOR)

        # set up the fog
        self.__fog = Fog("ringGameFog")
        if base.wantFog:
            self.__fog.setColor(self.WATER_COLOR)
            self.__fog.setLinearRange(0.1, self.FAR_PLANE_DIST-1.)
            render.setFog(self.__fog)

        # create a node to put all of the environment under
        self.environNode = render.attachNewNode("environNode")
        self.environBlocks = []
        for i in range(0,2):
            instance = self.environModel.instanceUnderNode(self.environNode, "model")
            y = self.ENVIRON_LENGTH*i
            instance.setY(y)
            self.environBlocks.append(instance)
            # add blocks on the left
            for j in range(0,2):
                instance = self.environModel.instanceUnderNode(self.environNode, "blocks")
                x = self.ENVIRON_LENGTH*(j+1)
                instance.setY(y)
                instance.setX(-x)
                self.environBlocks.append(instance)
            # add blocks on the right
            for j in range(0,2):
                instance = self.environModel.instanceUnderNode(self.environNode, "blocks")
                x = self.ENVIRON_LENGTH*(j+1)
                instance.setY(y)
                instance.setX(x)
                self.environBlocks.append(instance)

        # create a node to put all of the rings under
        # this should not be put under the environ node;
        # the environ node periodically 'jumps' back
        self.ringNode = render.attachNewNode("ringNode")

        # create an instance of each sound so that they can be
        # played simultaneously, one for each toon
        # these sounds must be loaded here because we don't know
        # how many players there will be until the minigame has
        # recieved all required fields
        self.sndTable = {
            "gotRing"    : [None] * self.numPlayers,
            "missedRing" : [None] * self.numPlayers,
            }
        for i in range(0,self.numPlayers):
            self.sndTable["gotRing"][i] =  base.loadSfx(\
                  "phase_4/audio/sfx/ring_get.mp3")
            self.sndTable["missedRing"][i] = base.loadSfx(\
                  "phase_4/audio/sfx/ring_miss.mp3")

        # create a drop shadow for the local toon
        self.__addToonDropShadow(self.getAvatar(self.localAvId))

        self.__spawnUpdateEnvironTask()
        self.__spawnUpdateShadowsTask()
        self.__spawnUpdateLocalToonTask()

        # Start music
        base.playMusic(self.music, looping = 0, volume = 0.8)
        if None != self.sndAmbience:
            base.playSfx(self.sndAmbience, looping = 1, volume = 0.8)

    def offstage(self):
        self.notify.debug("offstage")
        DistributedMinigame.offstage(self)

        # Stop music
        self.music.stop()
        if None != self.sndAmbience:
            self.sndAmbience.stop()

        self.__killUpdateLocalToonTask()
        self.__killUpdateShadowsTask()
        self.__killUpdateEnvironTask()

        del self.sndTable

        # remove all toons' shadows
        self.__removeAllToonDropShadows()

        assert(len(self.toonDropShadows) == 0)
        assert(len(self.ringDropShadows) == 0)

        render.clearFog()
        base.camLens.setFar(ToontownGlobals.DefaultCameraFar)
        base.camLens.setFov(ToontownGlobals.DefaultCameraFov)

        # Restore the background color
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

        self.arrowKeys.destroy()
        del self.arrowKeys

        for block in self.environBlocks:
            del block
        self.environNode.removeNode()
        del self.environNode

        self.ringNode.removeNode()
        del self.ringNode

        # reset the toons' LODs and show their dropshadows again
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.dropShadow.show()
                av.resetLOD()
                av.setAnimState('neutral', 1.0)

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # remove the disabled toon's shadow, so that the shadow
        # task doesn't crash when it tries to find the toon
        # also, it would look funny to have a shadow and no toon
        self.__removeToonDropShadow(self.remoteToons[avId])
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def __genText(self, text):
        self.__textGen.setText(text)
        return self.__textGen.generate()

    def __placeToon(self, avId):
        """ places a toon in its starting position """
        toon = self.getAvatar(avId)
        i = self.avIdList.index(avId)
        numToons = float(self.numPlayers)
        x = i * self.TOON_INITIAL_SPACING
        x -= (self.TOON_INITIAL_SPACING * (numToons-1)) / 2.
        toon.setPosHpr(x, self.TOON_Y, 0,
                       0, 0, 0)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return

        if not self.isSinglePlayer():
            # turn off the normal collisions
            base.localAvatar.collisionsOff()

            # put a collision sphere on localToon
            cSphere = CollisionSphere(0.0, 0.0, 0.0,
                                      RingGameGlobals.CollisionRadius)
            cSphereNode = CollisionNode('RingGameSphere-%s' % self.localAvId)
            cSphereNode.addSolid(cSphere)
            cSphereNode.setFromCollideMask(RingGameGlobals.CollideMask)
            cSphereNode.setIntoCollideMask(BitMask32.allOff())
            self.cSphereNodePath = base.localAvatar.attachNewNode(cSphereNode)

            self.pusher = CollisionHandlerPusher()
            self.pusher.addCollider(self.cSphereNodePath, base.localAvatar)
            # if we don't clear this, the toons will stick to each other
            # when moving purely along the X-axis
            self.pusher.setHorizontal(0)

            # create our own collision traverser
            self.cTrav = CollisionTraverser("DistributedRingGame")
            self.cTrav.addCollider(self.cSphereNodePath, self.pusher)

            # create collision spheres on the remote toons
            self.remoteToonCollNPs = {}
            for avId in self.remoteAvIdList:
                toon = self.getAvatar(avId)
                if toon:
                    cSphere = CollisionSphere(0.0, 0.0, 0.0,
                                              RingGameGlobals.CollisionRadius)
                    cSphereNode = CollisionNode('RingGameSphere-%s' % avId)
                    cSphereNode.addSolid(cSphere)
                    cSphereNode.setCollideMask(RingGameGlobals.CollideMask)
                    cSphereNP = toon.attachNewNode(cSphereNode)
                    self.remoteToonCollNPs[avId] = cSphereNP

        # show the remote toons
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)
                toon.setAnimState('swim', 1.0)
                toon.stopBobSwimTask()
                toon.useLOD(self.TOON_LOD)
                # hide the avatar's dropshadows
                toon.dropShadow.hide()
                self.__addToonDropShadow(toon)
                # Start the smoothing task.
                toon.startSmooth()

        # make a table of the remote toons
        # this allows us to destroy the shadows of disabled toons
        self.remoteToons = {}
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            self.remoteToons[avId] = toon

        self.__nextRingGroupResultIndex = 0

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        self.gameFSM.request("swim")

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterSwim(self):
        self.notify.debug("enterSwim")

        self.__ringTimeBase = self.gameStartTime

        self.__numRingGroups = RingGameGlobals.NUM_RING_GROUPS
        self.__ringGroupsPassed = 0

        self.__generateRings()

        self.__spawnUpdateRingsTask()
        self.__spawnCollisionDetectionTask() # localToon/ring collisions

        self.__ringTracks = []

        # show a colored ring at the bottom of the screen
        self.colorRing = self.ringModel.copyTo(hidden)
        self.colorRing.reparentTo(aspect2d)
        self.colorRing.setTwoSided(0)
        self.colorRing.setPos(1.19,10,-0.86)
        self.colorRing.setScale(0.04)

        p = self.avIdList.index(self.localAvId)
        self.colorRing.setColor(\
            RingGameGlobals.ringColors[self.colorIndices[p]][1])

        # this table will hold the results for each ring group;
        # initialize to 'unknown' (we haven't reached them yet)
        self.resultTable = [self.RT_UNKNOWN] * self.__numRingGroups

        # show a tally of the results at the bottom of the screen
        self.__initTallyDisplay()

    def __initTallyDisplay(self):
        # create tally-marker-generating TextNode
        self.__tallyTextNode = TextNode("tally")
        self.__tallyTextNode.setFont(ToontownGlobals.getSignFont())
        self.__tallyTextNode.setAlign(TextNode.ACenter)

        self.tallyMarkers = [None] * self.__numRingGroups

        # create N 'unknown' tally markers
        for i in range(0,self.__numRingGroups):
            self.__createTallyMarker(i, self.RT_UNKNOWN)

    def __destroyTallyDisplay(self):
        for i in range(0, self.__numRingGroups):
            self.__deleteTallyMarker(i)
        del self.tallyMarkers
        del self.__tallyTextNode

    def __createTallyMarker(self, index, result):
        chars = "-OOX"
        colors = (
            Point4(.8,.8,.8,1),
            Point4(0,1,0,1),
            Point4(1,1,0,1),
            Point4(1,0,0,1),
            )

        # if there is already a marker, delete it
        self.__deleteTallyMarker(index)

        self.__tallyTextNode.setText(chars[result])
        node = self.__tallyTextNode.generate()

        tallyText = aspect2d.attachNewNode(node)
        tallyText.setColor(colors[result])
        tallyText.setScale(.1)
        zOffset = 0
        if result == self.RT_UNKNOWN:
            zOffset = 0.015
        xSpacing = .085
        tallyText.setPos(-1. + (xSpacing * index), 0, -.93 + zOffset)
        self.tallyMarkers[index] = tallyText

    def __deleteTallyMarker(self, index):
        marker = self.tallyMarkers[index]
        if None != marker:
            marker.removeNode()
            self.tallyMarkers[index] = None

    def __updateTallyDisplay(self, index):
        self.__createTallyMarker(index, self.resultTable[index])

    def __generateRings(self):
        self.ringGroups = []

        # there are three levels of ring-group difficulty:
        # easy, medium, and hard (0, 1, and 2)
        #
        # easy is static rings that don't move
        # medium is simple patterns (like the big circle)
        # hard is complex or fast patterns (like the figure 8's)

        # number of easy, medium & hard patterns, per neighborhood
        difficultyDistributions = {
            ToontownGlobals.ToontownCentral:   [14,  2,  0],
            ToontownGlobals.DonaldsDock:       [10,  6,  0],
            ToontownGlobals.DaisyGardens:      [ 4, 12,  0],
            ToontownGlobals.MinniesMelodyland: [ 4,  8,  4],
            ToontownGlobals.TheBrrrgh:         [ 4,  6,  6],
            ToontownGlobals.DonaldsDreamland:  [ 2,  6,  8],
            }

        # make sure that the difficulty numbers add up correctly
        for distr in difficultyDistributions.values():
            sum = reduce(lambda x,y: x+y, distr)
            assert sum == self.NumRingGroups

        # these are the difficulty patterns that we can choose from.
        # for each safezone, these patterns must contain the correct
        # number of each difficulty, according to the table above
        difficultyPatterns = {
            ToontownGlobals.ToontownCentral:
            [ [0]*14 + [1]*2 + [2]*0,
              [0,0,0,0, 0,0,0,1] * 2,
              [0,0,0,0, 0,0,0,0, 0,0,0,1, 0,0,0,1],
              ],
            ToontownGlobals.DonaldsDock:
            [ [0]*10 + [1]*6 + [2]*0,
              [0,0,0,0, 0,1,1,1] * 2,
              [0,0,0,1, 0,0,1,1] * 2,
              ],
            ToontownGlobals.DaisyGardens:
            [ [0]*4 + [1]*12 + [2]*0,
              [0,0,1,1, 1,1,1,1] * 2,
              [0,1,1,1, 0,1,1,1] * 2,
              ],
            ToontownGlobals.MinniesMelodyland:
            [ [0]*4 + [1]*8 + [2]*4,
              [0,0,1,1, 1,1,2,2] * 2,
              [0,1,1,1, 1,0,2,2] * 2,
              [0,1,1,2, 0,1,1,2] * 2,
              [0,1,2,1, 0,1,2,1] * 2,
              ],
            ToontownGlobals.TheBrrrgh:
            [ [0]*4 + [1]*6 + [2]*6,
              [0,0,1,1, 1,2,2,2] * 2,
              [0,1,1,1, 0,2,2,2] * 2,
              [0,1,1,2, 0,1,2,2] * 2,
              [0,1,2,1, 0,1,2,2] * 2,
              ],
            ToontownGlobals.DonaldsDreamland:
            [ [0]*2 + [1]*6 + [2]*8,
              [0,1,1,1, 2,2,2,2] * 2,
              [0,1,1,2, 2,1,2,2] * 2,
              [0,1,2,1, 2,1,2,2] * 2,
              ],
            }

        safezone = self.getSafezoneId()
        numGroupsPerDifficulty = difficultyDistributions[safezone]

        # make sure all of the patterns have the right number of each
        # difficulty
        def patternsAreValid(difficultyPatterns=difficultyPatterns,
                             difficultyDistributions=
                             difficultyDistributions):
            # for each safezone
            for sz in difficultyPatterns.keys():
                # for each pattern
                for pattern in difficultyPatterns[sz]:
                    assert len(pattern) == self.NumRingGroups
                    # for each difficulty level
                    for difficulty in [0,1,2]:
                        # is there the correct number of this difficulty
                        # level in the pattern?
                        numGroupsPerDifficulty = difficultyDistributions[sz]
                        if numGroupsPerDifficulty[difficulty] != \
                           pattern.count(difficulty):
                            print 'safezone:', sz
                            print 'pattern:', pattern
                            print 'difficulty:', difficulty
                            print 'expected %s %ss, found %s' % (
                                numGroupsPerDifficulty[difficulty],
                                difficulty,
                                pattern.count(difficulty))
                            return 0
            return 1
        assert patternsAreValid()

        # choose a random pattern
        pattern = self.randomNumGen.choice(
            difficultyPatterns[self.getSafezoneId()])

        # create a list of ring groups
        for i in range(0,self.__numRingGroups):
            numRings = self.numPlayers
            trackGroup = RingTrackGroups.getRandomRingTrackGroup( \
                pattern[i], numRings, self.randomNumGen)
            ringGroup = RingGroup.RingGroup(trackGroup,
                                            self.ringModel,
                                            RingGameGlobals.MAX_TOONXZ,
                                            self.colorIndices)
            for r in range(numRings):
                self.__addRingDropShadow(ringGroup.getRing(r))

            self.ringGroups.append(ringGroup)

            ringGroup.reparentTo(self.ringNode)
            # make the first group arrive at the right time
            firstGroupOffset = self.TOON_Y + \
                        self.T_FIRST_RING_GROUP_ARRIVES * self.TOON_SWIM_VEL
            ringGroup.setY((i * self.RING_GROUP_SPACING) + firstGroupOffset)

    def __destroyRings(self):
        for group in self.ringGroups:
            # clean up ring group
            group.delete()
            group.removeNode()
        # get rid of all ring shadows
        self.__removeAllRingDropShadows()
        del self.ringGroups

    def __spawnUpdateLocalToonTask(self):
        self.__initPosBroadcast()

        taskMgr.remove(self.UPDATE_LOCALTOON_TASK)
        taskMgr.add(self.__updateLocalToonTask, self.UPDATE_LOCALTOON_TASK)

    def __killUpdateLocalToonTask(self):
        taskMgr.remove(self.UPDATE_LOCALTOON_TASK)

    def __initPosBroadcast(self):
        self.__posBroadcastPeriod = 0.2
        self.__timeSinceLastPosBroadcast = 0.
        self.__lastPosBroadcast = self.getAvatar(self.localAvId).getPos()
        self.__storeStop = 0
        # do an initial broadcast of the full position
        lt = self.getAvatar(self.localAvId)
        lt.d_clearSmoothing()
        lt.sendCurrentPosition()

    def __posBroadcast(self, dt):
        self.__timeSinceLastPosBroadcast += dt
        if self.__timeSinceLastPosBroadcast > self.__posBroadcastPeriod:
            self.__timeSinceLastPosBroadcast -= self.__posBroadcastPeriod

            # let DistributedSmoothNode figure out the deltas
            # we could optimize by creating a broadcastXZ func, but ehh
            self.getAvatar(self.localAvId).cnode.broadcastPosHprFull()

    def __updateLocalToonTask(self, task):
        # move the local toon
        dt = globalClock.getDt()

        toonPos = self.getAvatar(self.localAvId).getPos()

        # toonPos is a Point3, make a list
        pos = [toonPos[0], 0, toonPos[2]]

        xVel = 0.
        if self.arrowKeys.leftPressed():
            xVel -= self.TOONXZ_SPEED
        if self.arrowKeys.rightPressed():
            xVel += self.TOONXZ_SPEED
        pos[0] += xVel * dt
        if pos[0] < -RingGameGlobals.MAX_TOONXZ:
            pos[0] = -RingGameGlobals.MAX_TOONXZ
        if pos[0] > RingGameGlobals.MAX_TOONXZ:
            pos[0] = RingGameGlobals.MAX_TOONXZ

        zVel = 0.
        if self.arrowKeys.upPressed():
            zVel += self.TOONXZ_SPEED
        if self.arrowKeys.downPressed():
            zVel -= self.TOONXZ_SPEED
        pos[2] += zVel * dt
        if pos[2] < -RingGameGlobals.MAX_TOONXZ:
            pos[2] = -RingGameGlobals.MAX_TOONXZ
        if pos[2] > RingGameGlobals.MAX_TOONXZ:
            pos[2] = RingGameGlobals.MAX_TOONXZ

        self.getAvatar(self.localAvId).setPos(pos[0], self.TOON_Y, pos[2])

        # this is only applicable in multiplayer, and this task also runs
        # before collisions are set up.
        if hasattr(self, 'cTrav'):
            self.cTrav.traverse(render)

        # periodically send a position update
        self.__posBroadcast(dt)

        return Task.cont

    def exitSwim(self):
        for track in self.__ringTracks:
            track.finish()
        del self.__ringTracks

        self.colorRing.removeNode()
        del self.colorRing

        self.__destroyTallyDisplay()

        del self.resultTable

        taskMgr.remove(self.END_GAME_WAIT_TASK)
        self.__killUpdateRingsTask()
        self.__killCollisionDetectionTask()

        self.__destroyRings()

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        # toon/toon collisions were set up in setGameReady
        if not self.isSinglePlayer():
            # get rid of remote toon collisions
            for np in self.remoteToonCollNPs.values():
                np.removeNode()
            del self.remoteToonCollNPs

            self.cSphereNodePath.removeNode()
            del self.cSphereNodePath
            del self.pusher
            del self.cTrav

            # turn the normal collisions back on
            base.localAvatar.collisionsOn()

    def exitCleanup(self):
        pass

    def __addDropShadow_INTERNAL(self, object, scale_x, scale_y, scale_z,  list):
        """DO NOT CALL THIS DIRECTLY, only from __addToonDropShadow
        and __addRingDropShadow"""
        shadow = self.dropShadowModel.copyTo(render)
        # put the shadow at some ridiculous off-screen location
        shadow.setPos(0,self.CAMERA_Y,-100)
        # And give it the indicated initial scale.
        shadow.setScale(scale_x,scale_y,scale_z)
        list.append([shadow, object])

    def __removeDropShadow_INTERNAL(self, object, list):
        """DO NOT CALL THIS DIRECTLY, only from __removeToonDropShadow
        and __removeRingDropShadow"""
        for i in range(len(list)):
            entry = list[i]
            if entry[1] == object:
                entry[0].removeNode()
                list.pop(i)
                return
        self.notify.warning("parent object " + str(object) +
                            " not found in drop shadow list!")

    def __addToonDropShadow(self, object):
        self.__addDropShadow_INTERNAL(object, 0.5, 0.5, 0.5, self.toonDropShadows)

    def __removeToonDropShadow(self, object):
        self.__removeDropShadow_INTERNAL(object, self.toonDropShadows)

    def __addRingDropShadow(self, object):
        self.__addDropShadow_INTERNAL(object, 1.2, 0.31, 1.0, self.ringDropShadows)

    def __removeRingDropShadow(self, object):
        self.__removeDropShadow_INTERNAL(object, self.ringDropShadows)

    def __removeAllToonDropShadows(self):
        """this removes ALL toon drop shadows; if we unexpectedly have
        to end the game, we may no longer have instances of the
        remote toons, so to be safe, we can just delete them all"""
        for entry in self.toonDropShadows:
            entry[0].removeNode()
        self.toonDropShadows = []

    def __removeAllRingDropShadows(self):
        """this removes ALL ring drop shadows; if we unexpectedly have
        to end the game, we will have some ring shadows left, but we
        won't know which shadows have already been removed"""
        for entry in self.ringDropShadows:
            entry[0].removeNode()
        self.ringDropShadows = []

    def __spawnUpdateShadowsTask(self):
        taskMgr.remove(self.UPDATE_SHADOWS_TASK)
        taskMgr.add(self.__updateShadowsTask,
                    self.UPDATE_SHADOWS_TASK,
                    priority = self.UPDATE_SHADOWS_PRIORITY)

    def __killUpdateShadowsTask(self):
        taskMgr.remove(self.UPDATE_SHADOWS_TASK)

    def __updateShadowsTask(self, task):
        # move the drop shadows
        list = self.toonDropShadows + self.ringDropShadows
        for entry in list:
            object = entry[1]
            y = object.getY(render)
            # if the shadow is beyond the far plane, let it be
            if y > self.Y_VIS_MAX:
                continue
            x = object.getX(render)
            z = self.SEA_FLOOR_Z + self.SHADOW_Z_OFFSET
            shadow = entry[0]
            shadow.setPos(x, y, z)

            # scale the shadow according to the object's Z
            #objZ = objPos[2]
            #a = 1. - ((RingGameGlobals.MAX_TOONXZ + objZ) /
            #          (2. * RingGameGlobals.MAX_TOONXZ))
            #shadowScale = self.SHADOW_MIN_SCALE + \
            #              (a * (self.SHADOW_MAX_SCALE - self.SHADOW_MIN_SCALE))
            #objScale = object.getScale()[0]
            #shadow.setScale(shadowScale * objScale)

        return Task.cont

    def __spawnUpdateEnvironTask(self):
        taskMgr.remove(self.UPDATE_ENVIRON_TASK)
        taskMgr.add(self.__updateEnvironTask, self.UPDATE_ENVIRON_TASK)

    def __killUpdateEnvironTask(self):
        taskMgr.remove(self.UPDATE_ENVIRON_TASK)

    def __updateEnvironTask(self, task):
        # move the environment
        t = globalClock.getFrameTime() - self.__timeBase
        distance = t * self.TOON_SWIM_VEL
        distance %= self.ENVIRON_LENGTH
        distance += self.ENVIRON_START_OFFSET
        self.environNode.setY(-distance)
        return Task.cont

    def __spawnUpdateRingsTask(self):
        taskMgr.remove(self.UPDATE_RINGS_TASK)
        taskMgr.add(self.__updateRingsTask, self.UPDATE_RINGS_TASK)

    def __killUpdateRingsTask(self):
        taskMgr.remove(self.UPDATE_RINGS_TASK)

    def __updateRingsTask(self, task):
        # move the rings
        t = globalClock.getFrameTime() - self.__ringTimeBase
        #t -= 0.5 # delay by _ seconds
        distance = t * self.TOON_SWIM_VEL
        self.ringNode.setY(-distance)

        for ringGroup in self.ringGroups:
            # only update the group's t if the group is visible
            groupY = ringGroup.getY(render)
            if (groupY <= self.Y_VIS_MAX) and (groupY >= self.Y_VIS_MIN):
                ringGroup.setT(t)

        return Task.cont

    def __spawnCollisionDetectionTask(self):
        self.__ringGroupsPassed = 0
        # do this task after localtoon has been moved
        taskMgr.remove(self.COLLISION_DETECTION_TASK)
        taskMgr.add(self.__collisionDetectionTask,
                    self.COLLISION_DETECTION_TASK,
                    priority = self.COLLISION_DETECTION_PRIORITY)

    def __killCollisionDetectionTask(self):
        taskMgr.remove(self.COLLISION_DETECTION_TASK)

    def __makeRingSuccessFadeTrack(self, ring, duration, endScale, ringIndex):
        targetScale = Point3(endScale,endScale,endScale)
        dFade = 0.5 * duration
        dColorChange = duration - dFade
        # Fade the ring to its complement color.
        origColor = ring.getColor()
        targetColor = Point4(1.0 - origColor[0],
                             1.0 - origColor[1],
                             1.0 - origColor[2], 1)

        # ring's shadow gets scaled by shadow task

        def colorChangeFunc(t, ring=ring, targetColor=targetColor,
                            origColor=origColor):
            newColor = (targetColor * t) + (origColor * (1.-t))
            ring.setColor(newColor)
        def fadeFunc(t, ring=ring):
            ring.setColorScale(1,1,1,1.-t)

        fadeAwayTrack = Parallel(
            Sequence(LerpFunctionInterval(colorChangeFunc, fromData=0.,
                                          toData=1., duration=dColorChange),
                     LerpFunctionInterval(fadeFunc, fromData=0.,
                                          toData=1., duration=dFade)
                     ),
            LerpScaleInterval(ring, duration, targetScale),
            )

        successTrack = Sequence(
            Wait(self.RING_RESPONSE_DELAY),
            # play the success sound while doing the rest of the track
            Parallel(SoundInterval(self.sndTable["gotRing"][ringIndex]),
                     Sequence(Func(ring.wrtReparentTo, render),
                              fadeAwayTrack,
                              Func(self.__removeRingDropShadow, ring),
                              Func(ring.reparentTo, hidden),
                              ),
                     ),
            )

        return successTrack

    def __makeRingFailureFadeTrack(self, ring, duration, ringIndex):
        ts = 0.01
        targetScale = Point3(ts,ts,ts)

        # ring's shadow gets scaled by shadow task

        missedTextNode = self.__genText(TTLocalizer.RingGameMissed)
        missedText = hidden.attachNewNode(missedTextNode)
        ringColor = RingGameGlobals.ringColors[self.colorIndices[ringIndex]][1]
        def addMissedText(ring=ring, ringColor=ringColor,
                          missedText=missedText):
            missedText.reparentTo(render)
            missedText.setPos(ring.getPos(render) + Point3(0,-1,0))
            missedText.setColor(ringColor)
        def removeMissedText(missedText=missedText):
            missedText.removeNode()
            missedText = None

        failureTrack = Sequence(
            Wait(self.RING_RESPONSE_DELAY),
            # play the failure sound while doing the rest of the track
            Parallel(SoundInterval(self.sndTable["missedRing"][ringIndex]),
                     Sequence(Func(ring.wrtReparentTo, render),
                              Func(addMissedText),
                              LerpScaleInterval(ring, duration, targetScale,
                                                blendType='easeIn'),
                              Func(removeMissedText),
                              Func(self.__removeRingDropShadow, ring),
                              Func(ring.reparentTo, hidden),
                              ),
                     ),
            )

        return failureTrack

    def __makeRingFadeAway(self, ring, success, ringIndex):
        # make the ring fade away
        if success:
            track = self.__makeRingSuccessFadeTrack(ring, 0.5, 2., ringIndex)
        else:
            track = self.__makeRingFailureFadeTrack(ring, 0.5, ringIndex)
        self.__ringTracks.append(track)
        track.start()

    def __collisionDetectionTask(self, task):
        # check for localToon/ring collisions
        nextRingGroupIndex = self.__ringGroupsPassed
        nextRingGroup = self.ringGroups[nextRingGroupIndex]

        # have we just passed the ring group?
        if nextRingGroup.getY(render) < 0:
            groupIndex = nextRingGroupIndex
            gotRing = 0
            # Check if we are close enough to our ring in X and Z
            ourRing = nextRingGroup.getRing(\
                        self.avIdList.index(self.localAvId))
            ringPos = ourRing.getPos(render)
            localToonPos = base.localAvatar.getPos(render)
            distX = localToonPos[0] - ringPos[0]
            distZ = localToonPos[2] - ringPos[2]
            distSqrd = (distX * distX) + (distZ * distZ)
            if distSqrd <= (self.RING_RADIUS_SQRD):
                # we went through the ring!
                gotRing = 1

            # make the ring fade away
            self.__makeRingFadeAway(ourRing, gotRing,
                                    self.avIdList.index(self.localAvId))

            if gotRing:
                self.resultTable[groupIndex] = self.RT_SUCCESS
            else:
                self.resultTable[groupIndex] = self.RT_FAILURE
            # update the onscreen success tally
            self.__updateTallyDisplay(groupIndex)

            # tell the server our results
            self.sendUpdate("setToonGotRing", [gotRing])

            # if multiplayer, we'll wait to hear from the server
            # about the other players' results
            # otherwise, cut to the chase
            if self.isSinglePlayer():
                self.__processRingGroupResults([gotRing])

            self.__ringGroupsPassed += 1
            if self.__ringGroupsPassed >= self.__numRingGroups:
                # stop this task
                self.__killCollisionDetectionTask()

        return Task.cont

    def __endGameDolater(self, task):
        self.gameOver()
        return Task.done

    # network messages
    def setTimeBase(self, timestamp):
        if not self.hasLocalToon: return
        self.__timeBase = \
                    globalClockDelta.networkToLocalTime(timestamp)

    def setColorIndices(self, a, b, c, d):
        if not self.hasLocalToon: return
        self.colorIndices = [a, b, c, d]

    def __getSuccessTrack(self, groupIndex):

        # if last round:
        #   if multiplayer:
        #     if EVERYONE got EVERY ring:
        #       "GROUP PERFECT!!"
        #   if YOU got ALL rings:
        #     "PERFECT!"
        # if multiplayer:
        #   if EVERYONE got all rings in this ring group:
        #     "GROUP BONUS"

        def makeSuccessTrack(text, holdDuration, fadeDuration=.5,
                             perfect=0, self=self):
            successText = hidden.attachNewNode(self.__genText(text))
            successText.setScale(0.25)
            successText.setColor(1,1,.5,1)

            def fadeFunc(t, text):
                text.setColorScale(1,1,1,1.-t)
            def destroyText(text):
                text.removeNode()
                text=None

            track = Sequence(
                Func(successText.reparentTo, aspect2d),
                Wait(holdDuration),
                LerpFunctionInterval(fadeFunc, extraArgs=[successText],
                                     fromData=0., toData=1.,
                                     duration=fadeDuration,
                                     blendType="easeIn"),
                Func(destroyText, successText),
                )
            if perfect:
                track = Parallel(
                    track,
                    SoundInterval(self.sndPerfect),
                    )
            return track

        def isPerfect(list, goodValues):
            for value in list:
                if value not in goodValues:
                    return 0
            return 1

        # was that the last ring group?
        if groupIndex >= (self.__numRingGroups-1):
            # if multiplayer, was this a perfect game?
            if not self.isSinglePlayer():
                # did EVERYONE get EVERY ring??
                if isPerfect(self.resultTable, [self.RT_GROUPSUCCESS]):
                    return makeSuccessTrack(TTLocalizer.RingGameGroupPerfect,
                                            1.5, perfect=1)
            # did the local player get all rings?
            if isPerfect(self.resultTable,
                         [self.RT_SUCCESS, self.RT_GROUPSUCCESS]):
                return makeSuccessTrack(TTLocalizer.RingGamePerfect,
                                        1.5, perfect=1)
            # otherwise, just wait
            return Wait(1.)
        # if multiplayer, did everyone get their ring in this last ring group?
        if not self.isSinglePlayer():
            if self.resultTable[groupIndex] == self.RT_GROUPSUCCESS:
                return makeSuccessTrack(TTLocalizer.RingGameGroupBonus,
                                        0., fadeDuration = .4)

        return None

    def __processRingGroupResults(self, results):
        """'results' is a list of booleans, one entry per player
        0 == missed, non-zero == got the ring"""
        groupIndex = self.__nextRingGroupResultIndex
        ringGroup = self.ringGroups[self.__nextRingGroupResultIndex]
        self.__nextRingGroupResultIndex += 1

        # make all of the remote toons' rings and their shadows fade away
        for i in range(0,self.numPlayers):
            if self.avIdList[i] != self.localAvId:
                ring = ringGroup.getRing(i)
                self.__makeRingFadeAway(ring, results[i], i)

        if not self.isSinglePlayer():
            # did everyone get their ring?
            if not 0 in results:
                self.notify.debug("Everyone got their rings!!")
                self.resultTable[groupIndex] = self.RT_GROUPSUCCESS
                # update the onscreen success tally
                self.__updateTallyDisplay(groupIndex)

        successTrack = self.__getSuccessTrack(groupIndex)

        # if that was the last group, end the game
        endGameTrack = None
        if groupIndex >= (self.__numRingGroups-1):
            def endTheGame(self=self):
                if not RingGameGlobals.ENDLESS_GAME:
                    taskMgr.doMethodLater(self.GAME_END_DELAY,
                                          self.__endGameDolater,
                                          self.END_GAME_WAIT_TASK)

            endGameTrack = Func(endTheGame)

        if None != successTrack or None != endGameTrack:
            track = Sequence()
            if None != successTrack:
                # delay the track until the ring responds
                track.append(Wait(self.RING_RESPONSE_DELAY))
                track.append(successTrack)
            if None != endGameTrack:
                track.append(endGameTrack)

            self.__ringTracks.append(track)
            track.start()
        

    def setRingGroupResults(self, bitfield):
        """
        bitfield == 0 means everyone got their rings
        otherwise, set bits indicate missed rings
        i.e. 0x05 (0000 0101) means toons 3 and 1 missed
        """
        if not self.hasLocalToon: return
        # if game ended prematurely, ignore this message
        if self.gameFSM.getCurrentState().getName() != 'swim':
            return

        #self.notify.debug("setRingGroupResults: " + hex(bitfield))

        results = []
        mask = 0x01
        for avId in self.avIdList:
            results.append(not (bitfield & mask))
            mask <<= 1

        self.__processRingGroupResults(results)
