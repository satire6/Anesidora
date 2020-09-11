66#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: The Party Catch Activity is like the trolley catch activity, only
#          party-wide.  Toons enter the catch area and the game starts.  Fruit
#          falls beneath the party tree.
#-------------------------------------------------------------------------------
from pandac.PandaModules import Vec3, Point3, Point4, TextNode, NodePath
from pandac.PandaModules import CollisionHandlerEvent, CollisionNode, CollisionSphere

from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.IntervalGlobal import LerpScaleInterval, LerpFunctionInterval, LerpColorScaleInterval, LerpPosInterval
from direct.interval.IntervalGlobal import SoundInterval, WaitInterval
from direct.showbase.PythonUtil import Functor, bound, lerp, SerialNumGen
from direct.showbase.RandomNumGen import RandomNumGen
from direct.task.Task import Task
from direct.distributed import DistributedSmoothNode
from direct.directnotify import DirectNotifyGlobal
from direct.interval.FunctionInterval import Wait, Func

from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.minigame.Trajectory import Trajectory
from toontown.minigame.OrthoDrive import OrthoDrive
from toontown.minigame.OrthoWalk import OrthoWalk
from toontown.minigame.DropPlacer import PartyRegionDropPlacer

from toontown.parties import PartyGlobals
from toontown.parties.PartyCatchActivityToonSD import PartyCatchActivityToonSD
from toontown.parties.DistributedPartyActivity import DistributedPartyActivity
from toontown.parties.DistributedPartyCatchActivityBase import DistributedPartyCatchActivityBase
from toontown.parties.DistributedPartyCannonActivity import DistributedPartyCannonActivity
from toontown.parties.activityFSMs import CatchActivityFSM

class DistributedPartyCatchActivity(DistributedPartyActivity, DistributedPartyCatchActivityBase):
    
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPartyCatchActivity")

    DropTaskName = 'dropSomething'

    DropObjectPlurals = {
        'apple'      : TTLocalizer.PartyCatchActivityApples,
        'orange'     : TTLocalizer.PartyCatchActivityOranges,
        'pear'       : TTLocalizer.PartyCatchActivityPears,
        'coconut'    : TTLocalizer.PartyCatchActivityCoconuts,
        'watermelon' : TTLocalizer.PartyCatchActivityWatermelons,
        'pineapple'  : TTLocalizer.PartyCatchActivityPineapples,
        'anvil'      : TTLocalizer.PartyCatchActivityAnvils,
        }

    class Generation:
        def __init__(self, generation, startTime, startNetworkTime, numPlayers):
            self.generation = generation
            self.startTime = startTime
            # store the network time to make sure clients are in sync with each other
            self.startNetworkTime = startNetworkTime
            self.numPlayers = numPlayers
            self.hasBeenScheduled = False
            # this will hold the names of the objects to be dropped
            self.droppedObjNames = []
            # this will hold a list of drops to perform and when to perform them
            self.dropSchedule = []
            self.numItemsDropped = 0
            # this dict keeps track of which fruits we have shown being eaten;
            # prevents a single fruit from being eaten by multiple toons
            self.droppedObjCaught = {}

    def __init__(self, cr):
        DistributedPartyActivity.__init__(
            self,
            cr,
            PartyGlobals.ActivityIds.PartyCatch,
            PartyGlobals.ActivityTypes.HostInitiated,
            wantRewardGui=True,
        )
        self.setUsesSmoothing()
        self.setUsesLookAround()
        self._sNumGen = SerialNumGen()

    def getTitle(self):
        return TTLocalizer.PartyCatchActivityTitle

    def getInstructions(self):
        return TTLocalizer.PartyCatchActivityInstructions % {
            'badThing' : self.DropObjectPlurals['anvil']}

    def generate(self):
        DistributedPartyActivity.generate(self)
        self.notify.info('localAvatar doId: %s' % base.localAvatar.doId)
        self.notify.info('generate()')
        # keep track of what frame it is when we generate
        self._generateFrame = globalClock.getFrameCount()
        self._id2gen = {}
        # chronological ordering of drop generations
        self._orderedGenerations = []
        # currently-active generation
        self._orderedGenerationIndex = None
        rng = RandomNumGen(self.doId)
        self._generationSeedBase = rng.randrange(1000)
        self._lastDropTime = 0.

    def getCurGeneration(self):
        if self._orderedGenerationIndex is None:
            return None
        return self._orderedGenerations[self._orderedGenerationIndex]

    def _addGeneration(self, generation, startTime, startNetworkTime, numPlayers):
        self._id2gen[generation] = self.Generation(generation, startTime, startNetworkTime, numPlayers)
        i = 0
        while 1:
            if i >= len(self._orderedGenerations):
                break
            gen = self._orderedGenerations[i]
            startNetT = self._id2gen[gen].startTime
            genId = self._id2gen[gen].generation
            # maintain ordering based on time, then on generation ID
            if startNetT > startNetworkTime:
                break
            if ((startNetT == startNetworkTime) and (genId > generation)):
                break
            i += 1
        self._orderedGenerations = (
            self._orderedGenerations[:i] + [generation,] + self._orderedGenerations[i:])
        if self._orderedGenerationIndex is not None:
            if self._orderedGenerationIndex >= i:
                self._orderedGenerationIndex += 1

    def _removeGeneration(self, generation):
        del self._id2gen[generation]
        i = self._orderedGenerations.index(generation)
        self._orderedGenerations = (
            self._orderedGenerations[:i] + self._orderedGenerations[i+1:])
        if self._orderedGenerationIndex is not None:
            if len(self._orderedGenerations):
                if self._orderedGenerationIndex >= i:
                    self._orderedGenerationIndex -= 1
            else:
                self._orderedGenerationIndex = None

    def announceGenerate(self):
        self.notify.info('announceGenerate()')
        self.catchTreeZoneEvent = "fence_floor"
        DistributedPartyActivity.announceGenerate(self)

    # Called at the end of DistributedPartyActivity.announceGenerate
    def load(self):
        self.notify.info('load()')
        DistributedPartyCatchActivity.notify.debug("PartyCatch: load")
        # create state machine and set initial state
        self.activityFSM = CatchActivityFSM(self)

        if __dev__:
            # log stats on drop rates for diff numbers of players
            for o in xrange(3):
                print {0: 'SPOTS PER PLAYER',
                       1: 'DROPS PER MINUTE PER SPOT DURING NORMAL DROP PERIOD',
                       2: 'DROPS PER MINUTE PER PLAYER DURING NORMAL DROP PERIOD',
                       }[o]
                for i in xrange(1, self.FallRateCap_Players+10):
                    self.defineConstants(forceNumPlayers=i)
                    numDropLocations = self.DropRows * self.DropColumns
                    numDropsPerMin = 60. / self.DropPeriod
                    if o == 0:
                        spotsPerPlayer = numDropLocations / float(i)
                        print '%2d PLAYERS: %s' % (i, spotsPerPlayer)
                    elif o == 1:
                        numDropsPerMinPerSpot = numDropsPerMin / numDropLocations
                        print '%2d PLAYERS: %s' % (i, numDropsPerMinPerSpot)
                    else:
                        if i > 0:
                            numDropsPerMinPerPlayer = numDropsPerMin / i
                            print '%2d PLAYERS: %s' % (i, numDropsPerMinPerPlayer)

        # load resources and create objects here
        self.defineConstants()
        self.treesAndFence = loader.loadModel("phase_13/models/parties/partyCatchTree")
        #self.treesAndFence.setPos(-7.0, 0.0, 0.0)
        self.treesAndFence.setScale(0.9)
        self.treesAndFence.find("**/fence_floor").setPos(0.0, 0.0, 0.1)
        self.treesAndFence.reparentTo(self.root)
        
        ground = self.treesAndFence.find("**/groundPlane")
        # Make the ground plane draw before the shadow!
        ground.setBin("ground", 1)
        
        DistributedPartyActivity.load(self)

        # put EXIT on the exit sign
        exitText = TextNode('PartyCatchExitText')
        exitText.setCardAsMargin(.1, .1, .1, .1)
        exitText.setCardDecal(True)
        exitText.setCardColor(1., 1., 1., 0.)
        exitText.setText(TTLocalizer.PartyCatchActivityExit)
        exitText.setTextColor(0., 8., 0., .9)
        exitText.setAlign(exitText.ACenter)
        exitText.setFont(ToontownGlobals.getBuildingNametagFont())
        exitText.setShadowColor(0, 0, 0, 1)
        exitText.setBin('fixed')
        if TTLocalizer.BuildingNametagShadow:
            exitText.setShadow(*TTLocalizer.BuildingNametagShadow)

        # place the text
        exitTextLoc = self.treesAndFence.find('**/loc_exitSignText')
        exitTextNp = exitTextLoc.attachNewNode(exitText)
        exitTextNp.setDepthWrite(0)
        exitTextNp.setScale(4)
        exitTextNp.setZ(-.5)

        # place the activity sign
        self.sign.reparentTo(self.treesAndFence.find("**/loc_eventSign"))
        # reparent back to root so we don't get the treesAndFence scaling, but
        # still keep the locator position
        self.sign.wrtReparentTo(self.root)

        self.avatarNodePath = NodePath("PartyCatchAvatarNodePath")
        self.avatarNodePath.reparentTo(self.root)
        self._avatarNodePathParentToken = 3#'PartyCatch-%s' % self.doId
        base.cr.parentMgr.registerParent(self._avatarNodePathParentToken, self.avatarNodePath)

        # make a dictionary of PartyCatchActivityToonSDs; they will track
        # toons' states and animate them appropriately
        self.toonSDs = {}
        self.dropShadow = loader.loadModelOnce('phase_3/models/props/drop_shadow')
        # load the models for the drop objects (see PartyGlobals.py)
        # index by object type name
        self.dropObjModels = {}
        for objType in PartyGlobals.DropObjectTypes:
            model = loader.loadModel(objType.modelPath)
            self.dropObjModels[objType.name] = model

            # all of the models need to be rescaled
            modelScales = {
                'apple' : .7,
                'orange' : .7,
                'pear' : .5,
                'coconut' : .7,
                'watermelon' : .6,
                'pineapple' : .45,
                }
            if modelScales.has_key(objType.name):
                model.setScale(modelScales[objType.name])

            # adjust the model if necessary
            # don't compare the name; this will crash if someone changes
            # or removes any of the referenced objects (and crashing is the
            # desired behaviour)
            if objType == PartyGlobals.Name2DropObjectType['pear']:
                # pear needs to be moved down
                model.setZ(-.6)
            if objType == PartyGlobals.Name2DropObjectType['coconut']:
                # turn the coconut upside-down so we can see the dots
                model.setP(180)
            if objType == PartyGlobals.Name2DropObjectType['watermelon']:
                # turn the watermelon to an interesting angle, and move it down
                model.setH(135)
                model.setZ(-.5)
            if objType == PartyGlobals.Name2DropObjectType['pineapple']:
                # move the pineapple down
                model.setZ(-1.7)
            if objType == PartyGlobals.Name2DropObjectType['anvil']:
                # anvil needs to be moved down a foot
                model.setZ(-self.ObjRadius)
            model.flattenStrong()

        self.sndGoodCatch = base.loadSfx('phase_4/audio/sfx/SZ_DD_treasure.mp3')
        self.sndOof = base.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.sndAnvilLand = base.loadSfx('phase_4/audio/sfx/AA_drop_anvil_miss.mp3')
        self.sndPerfect = base.loadSfx('phase_4/audio/sfx/ring_perfect.mp3')

        # this will be used to generate textnodes
        self.__textGen = TextNode("partyCatchActivity")
        self.__textGen.setFont(ToontownGlobals.getSignFont())
        self.__textGen.setAlign(TextNode.ACenter)

        #self.timer = ToontownTimer()
        #self.timer.posInTopRightCorner()
        #self.timer.setTime(PartyGlobals.CatchActivityDuration)
        #self.timer.setTransparency(1)
        #self.timer.setColorScale(1, 1, 1, .75)
        #self.timer.stash()

        self.activityFSM.request("Idle")
        
    def unload(self):
        DistributedPartyCatchActivity.notify.debug("unload")
        self.finishAllDropIntervals()
        self.destroyOrthoWalk()
        DistributedPartyActivity.unload(self)
        self.stopDropTask()
        # unload resources and delete objects from load() here
        del self.activityFSM
        
        del self.__textGen

        for avId in self.toonSDs.keys():
            if self.toonSDs.has_key(avId):
                toonSD = self.toonSDs[avId]
                toonSD.unload()
        del self.toonSDs

        #self.timer.destroy()
        #del self.timer

        self.treesAndFence.removeNode()
        del self.treesAndFence

        self.dropShadow.removeNode()
        del self.dropShadow

        base.cr.parentMgr.unregisterParent(self._avatarNodePathParentToken)

        for model in self.dropObjModels.values():
            model.removeNode()
        del self.dropObjModels
            
        del self.sndGoodCatch
        del self.sndOof
        del self.sndAnvilLand
        del self.sndPerfect

    def setStartTimestamp(self, timestamp32):
        self.notify.info('setStartTimestamp(%s)' % (timestamp32, ))
        self._startTimestamp = globalClockDelta.networkToLocalTime(timestamp32, bits=32)

    def getCurrentCatchActivityTime(self):
        return globalClock.getFrameTime() - self._startTimestamp

    def getObjModel(self, objName):
        """ returns a copy of the drop object corresponding to 'objName',
        parented under hidden """
        return self.dropObjModels[objName].copyTo(hidden)

    def joinRequestDenied(self, reason):
        DistributedPartyActivity.joinRequestDenied(self, reason)
        base.cr.playGame.getPlace().fsm.request("walk")

    def handleToonJoined(self, toonId):
        if not self.toonSDs.has_key(toonId):
            toonSD = PartyCatchActivityToonSD(toonId, self)
            self.toonSDs[toonId] = toonSD
            toonSD.load()
        self.notify.debug("handleToonJoined : currentState = %s" % self.activityFSM.state)
        self.cr.doId2do[toonId].useLOD(500)
        if self.activityFSM.state == "Active":
            if self.toonSDs.has_key(toonId):
                self.toonSDs[toonId].enter()
            if base.localAvatar.doId == toonId:
                base.localAvatar.b_setParent(self._avatarNodePathParentToken)
                self.putLocalAvatarInActivity()
            else:
                pass
                #self.cr.doId2do[toonId].reparentTo(self.avatarNodePath)
            if self.toonSDs.has_key(toonId):
                self.toonSDs[toonId].fsm.request('rules')

    def handleToonExited(self, toonId):
        self.notify.debug("handleToonExited( toonId=%s )" % toonId)
        if self.cr.doId2do.has_key(toonId):
            self.cr.doId2do[toonId].resetLOD()
            if self.toonSDs.has_key(toonId):
                self.toonSDs[toonId].fsm.request("notPlaying")
                del self.toonSDs[toonId]
                
            if base.localAvatar.doId == toonId:
                base.localAvatar.b_setParent(ToontownGlobals.SPRender)
            else:
                pass
                #self.cr.doId2do[toonId].reparentTo(render)

    def takeLocalAvatarOutOfActivity(self):
        self.notify.debug("localToon has left the circle")

        #base.localAvatar.wrtReparentTo(render)
        camera.reparentTo(base.localAvatar)
        base.localAvatar.startUpdateSmartCamera()
        base.localAvatar.enableSmartCameraViews()
        base.localAvatar.setCameraPositionByIndex(base.localAvatar.cameraIndex)
        
        #self.timer.stash()
        # Restore normal non-predictive smoothing.
        DistributedSmoothNode.activateSmoothing(1, 0)

    def _enableCollisions(self):
        DistributedPartyActivity._enableCollisions(self)
        self._enteredTree = False
        self.accept('enter' + self.catchTreeZoneEvent, self._toonMayHaveEnteredTree)
        self.accept('again' + self.catchTreeZoneEvent, self._toonMayHaveEnteredTree)
        self.accept('exit' + self.catchTreeZoneEvent, self._toonExitedTree)
        self.accept(DistributedPartyCannonActivity.LOCAL_TOON_LANDED_EVENT, self._handleCannonLanded)
        
    def _disableCollisions(self):
        self.ignore(DistributedPartyCannonActivity.LOCAL_TOON_LANDED_EVENT)
        self.ignore('enter' + self.catchTreeZoneEvent)
        self.ignore('again' + self.catchTreeZoneEvent)
        self.ignore('exit' + self.catchTreeZoneEvent)
        DistributedPartyActivity._disableCollisions(self)

    def _handleCannonLanded(self):
        """
        # 'blast' localToon downward so that they collide with the ground again
        # and trigger collisions
        # otherwise toon can land in catch arena and run around normally
        localAvatar.controlManager.currentControls.addBlastForce(Vec3(0,0,-10.))
        """
        # NOTE: this assumes that the toon is in the same coordinate space as
        # self.x and self.y
        x = base.localAvatar.getX()
        y = base.localAvatar.getY()
        if x > (self.x - self.StageHalfWidth) and \
           x < (self.x + self.StageHalfWidth) and \
           y > (self.y - self.StageHalfHeight) and \
           y < (self.y + self.StageHalfHeight):
            self._toonEnteredTree(None)

    def _toonMayHaveEnteredTree(self, collEntry):
        # if we've already entered the play area, ignore
        if self._enteredTree:
            return
        # if we're jumping, ignore
        if base.localAvatar.controlManager.currentControls.getIsAirborne():
            return
        self._toonEnteredTree(collEntry)
    
    def _toonEnteredTree(self, collEntry):
        self.notify.debug("_toonEnteredTree : avid = %s" % base.localAvatar.doId)
        self.notify.debug("_toonEnteredTree : currentState = %s" % self.activityFSM.state)
        if self.isLocalToonInActivity():
            # You've landed from the cannon... don't start catch
            assert(self.notify.debug("\tLocal toon in activity"))
            return
        if self.activityFSM.state == "Active":
            assert(self.notify.debug("\tRequest join"))
            base.cr.playGame.getPlace().fsm.request("activity")
            self.d_toonJoinRequest()
        elif self.activityFSM.state == "Idle":    
            assert(self.notify.debug("\tRequest start"))
            base.cr.playGame.getPlace().fsm.request("activity")
            # game is always running
            #self.sendUpdate("requestActivityStart")
            self.d_toonJoinRequest()
        self._enteredTree = True
    
    def _toonExitedTree(self, collEntry):
        self.notify.debug("_toonExitedTree : avid = %s" % base.localAvatar.doId)
        self._enteredTree = False
        if (hasattr(base.cr.playGame.getPlace(), 'fsm') and self.activityFSM.state == "Active" and
            self.isLocalToonInActivity()):
            if self.toonSDs.has_key(base.localAvatar.doId):
                self.takeLocalAvatarOutOfActivity()
                self.toonSDs[base.localAvatar.doId].fsm.request("notPlaying")
            self.d_toonExitDemand()

    def setToonsPlaying(self, toonIds):
        self.notify.info('setToonsPlaying(%s)' % (toonIds, ))
        DistributedPartyActivity.setToonsPlaying(self, toonIds)
        if self.isLocalToonInActivity() and (base.localAvatar.doId not in toonIds):
            if self.toonSDs.has_key(base.localAvatar.doId):
                self.takeLocalAvatarOutOfActivity()
                self.toonSDs[base.localAvatar.doId].fsm.request("notPlaying")
    
    def __genText(self, text):
        self.__textGen.setText(text)
        return self.__textGen.generate()

    def getNumPlayers(self):
        """
        This is leftover code that minigame/DropPlacer needs to call
        """
        return len(self.toonIds)

    def defineConstants(self, forceNumPlayers=None):
        DistributedPartyCatchActivity.notify.debug('defineConstants')

        self.ShowObjSpheres = 0
        self.ShowToonSpheres = 0

        self.useGravity = True

        # set this to true to make shadows of fast-falling objects grow
        # as if they were standard shadows until their associated object
        # comes on-screen, then scale up to full size, faster, in time
        # for the landing
        self.trickShadows = True

        if forceNumPlayers is None:
            numPlayers = self.getNumPlayers()
        else:
            numPlayers = forceNumPlayers
        self.calcDifficultyConstants(numPlayers)

        DistributedPartyCatchActivity.notify.debug("ToonSpeed: %s" % self.ToonSpeed)
        DistributedPartyCatchActivity.notify.debug("total drops: %s" % self.totalDrops)
        DistributedPartyCatchActivity.notify.debug("numFruits: %s" % self.numFruits)
        DistributedPartyCatchActivity.notify.debug("numAnvils: %s" % self.numAnvils)

        self.ObjRadius = 1.0

        # objects fall on a grid; these are the dimensions of the grid
        dropRegionTable = PartyRegionDropPlacer.getDropRegionTable(numPlayers)
        self.DropRows, self.DropColumns = len(dropRegionTable), len(dropRegionTable[0])

        # fix up the drop object table according to the difficulty level,
        # set up per-object-type Trajectory objects and related variables
        for objType in PartyGlobals.DropObjectTypes:
            DistributedPartyCatchActivity.notify.debug("*** Object Type: %s" % objType.name)

            # each object type has an onscreen drop duration multiplier
            # that specifies how long the object should be onscreen,
            # relative to the baseline duration.
            objType.onscreenDuration = (objType.onscreenDurMult * 
                                        self.BaselineOnscreenDropDuration)
            DistributedPartyCatchActivity.notify.debug("onscreenDuration=%s" % objType.onscreenDuration)

            # calculate a value of gravity that will make the object
            # fall from moH to the ground in the correct amount of time.
            #
            # from the standard constant acceleration equation:
            # x = x_0 + v_0*t + .5*a*t^2
            # solve for the acceleration term, 'a' (gravity)
            # a = 2*(x - x_0 - v_0*t) / t^2

            # by default, we'll start all the objects from moH, at rest.
            v_0 = 0.
            t = objType.onscreenDuration
            x_0 = self.MinOffscreenHeight
            x = 0. # the ground

            # this will come out negative, but it doesn't really matter
            # one way or the other; we specify a positive gravity ratio
            # for the Trajectory object
            g = (2. * (x - x_0 - (v_0 * t))) / (t * t)
            DistributedPartyCatchActivity.notify.debug("gravity=%s" % g)

            # create a Trajectory object that will be used by all instances of
            # this object type
            objType.trajectory = Trajectory(
                # start time
                0,
                # start pos
                Vec3(0, 0, x_0),
                # start vel
                Vec3(0, 0, v_0),
                # gravity multiplier
                gravMult=abs(g / Trajectory.gravity))

            # the total 'fall' duration for this object type is its
            # onscreen time plus the universally constant OffscreenTime
            objType.fallDuration = objType.onscreenDuration + self.OffscreenTime

    def grid2world(self, column, row):
        """
        column: 0..(DropColumns-1)
           row: 0..(DropRows-1)
        returns (x, y) pair
        """
        # x,y in [0..1]
        x = column / float(self.DropColumns - 1)
        y = row / float(self.DropRows - 1)
        # x,y in [-1..1]
        x = (x * 2.) - 1.
        y = (y * 2.) - 1.
        # x,y in world space
        x *= self.StageHalfWidth
        y *= self.StageHalfHeight
        return (x, y)

    def showPosts(self):
        """ debugging aid; show the extremes of the playfield """
        self.hidePosts()
        self.posts = [Toon.Toon(), Toon.Toon(), Toon.Toon(), Toon.Toon()]
        for i in range(len(self.posts)):
            tree = self.posts[i]
            tree.reparentTo(render)
            x = self.StageHalfWidth
            y = self.StageHalfHeight
            if i > 1:
                x = - x
            if i % 2:
                y = - y
            tree.setPos(x + self.x, y + self.y, 0)

    def hidePosts(self):
        if hasattr(self, 'posts'):
            for tree in self.posts:
                tree.removeNode()
            del self.posts

    def showDropGrid(self):
        """ debugging aid; show the drop grid """
        self.hideDropGrid()
        self.dropMarkers = []
        for row in range(self.DropRows):
            self.dropMarkers.append([])
            rowList = self.dropMarkers[row]
            for column in range(self.DropColumns):
                toon = Toon.Toon()
                toon.setDNA(base.localAvatar.getStyle())
                toon.reparentTo(self.root)
                toon.setScale(1. / 3)
                x, y = self.grid2world(column, row)
                toon.setPos(x, y, 0)
                rowList.append(toon)

    def hideDropGrid(self):
        if hasattr(self, 'dropMarkers'):
            for row in self.dropMarkers:
                for marker in row:
                    marker.removeNode()
            del self.dropMarkers

    def handleToonDisabled(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        DistributedPartyCatchActivity.notify.debug("handleToonDisabled")
        DistributedPartyCatchActivity.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears
        if self.toonSDs.has_key(avId):
            self.toonSDs[avId].exit(unexpectedExit=True)
        del self.toonSDs[avId]
    
    def turnOffSmoothingOnGuests(self):
        """ Override parent class, we want smoothing! """
        pass

    def setState(self, newState, timestamp):
        self.notify.info('setState(%s, %s)' % (newState, timestamp, ))
        DistributedPartyCatchActivity.notify.debug("setState( newState=%s, ... )" % newState)
        DistributedPartyActivity.setState(self, newState, timestamp)
        # pass additional parameters only to those states that need it
        self.activityFSM.request(newState)
        if newState == "Active":
            # We're going to active, check to see if I'm the host
            if base.localAvatar.doId != self.party.partyInfo.hostId:
                # give localToon time to adjust to being in the party (new pos etc)
                if globalClock.getFrameCount() > self._generateFrame:
                    # if not host, check to see if I'm within the fence
                    if base.localAvatar.getX() > self.x - self.StageHalfWidth and \
                        base.localAvatar.getX() < self.x + self.StageHalfWidth and \
                        base.localAvatar.getY() > self.y - self.StageHalfHeight and \
                        base.localAvatar.getY() < self.y + self.StageHalfHeight:
                        self._toonEnteredTree(None)

    def putLocalAvatarInActivity(self):
        if base.cr.playGame.getPlace() and \
           hasattr(base.cr.playGame.getPlace(), "fsm"):
            base.cr.playGame.getPlace().fsm.request("activity", [False])
        else:
            self.notify.info("Avoided crash: toontown.parties.DistributedPartyCatchActivity:632, toontown.parties.DistributedPartyCatchActivity:1198, toontown.parties.activityFSMMixins:49, direct.fsm.FSM:423, AttributeError: 'NoneType' object has no attribute 'fsm'")
        base.localAvatar.stopUpdateSmartCamera()
        #base.localAvatar.wrtReparentTo(self.avatarNodePath)

        camera.reparentTo(self.treesAndFence)
        camera.setPosHpr(0.0, - 63.0, 30.0, 0.0, - 20.0, 0.0)
        #self.timer.unstash()

        if not hasattr(self, "ltLegsCollNode"):
            self.createCatchCollisions()

    def createCatchCollisions(self):
        # attach some collision spheres so that we can catch things
        # with any part of our body
        # four spheres seems to be enough for the body
        # one on the legs, one on the head, one on each hand
        # (having one on each hand is slight overkill; it's useful during the
        # falling-down animations when the hands are widely separated. meh.)
        radius = .7
        handler = CollisionHandlerEvent()
        handler.setInPattern('ltCatch%in')
        self.ltLegsCollNode = CollisionNode('catchLegsCollNode')
        self.ltLegsCollNode.setCollideMask(PartyGlobals.CatchActivityBitmask)
        self.ltHeadCollNode = CollisionNode('catchHeadCollNode')
        self.ltHeadCollNode.setCollideMask(PartyGlobals.CatchActivityBitmask)
        self.ltLHandCollNode = CollisionNode('catchLHandCollNode')
        self.ltLHandCollNode.setCollideMask(PartyGlobals.CatchActivityBitmask)
        self.ltRHandCollNode = CollisionNode('catchRHandCollNode')
        self.ltRHandCollNode.setCollideMask(PartyGlobals.CatchActivityBitmask)
        legsCollNodepath = base.localAvatar.attachNewNode(self.ltLegsCollNode)
        legsCollNodepath.hide()
        # get the 1000-lod head node
        head = base.localAvatar.getHeadParts().getPath(2)
        headCollNodepath = head.attachNewNode(self.ltHeadCollNode)
        headCollNodepath.hide()
        # get the 1000-lod nodes for the left hand
        lHand = base.localAvatar.getLeftHands()[0]
        lHandCollNodepath = lHand.attachNewNode(self.ltLHandCollNode)
        lHandCollNodepath.hide()
        # get the 1000-lod nodes for the right hand
        rHand = base.localAvatar.getRightHands()[0]
        rHandCollNodepath = rHand.attachNewNode(self.ltRHandCollNode)
        rHandCollNodepath.hide()
        # add collision nodepaths to the traverser
        base.localAvatar.cTrav.addCollider(legsCollNodepath, handler)
        base.localAvatar.cTrav.addCollider(headCollNodepath, handler)
        base.localAvatar.cTrav.addCollider(lHandCollNodepath, handler)
        base.localAvatar.cTrav.addCollider(lHandCollNodepath, handler)
        if self.ShowToonSpheres:
            legsCollNodepath.show()
            headCollNodepath.show()
            lHandCollNodepath.show()
            rHandCollNodepath.show()
        self.ltLegsCollNode.addSolid(CollisionSphere(0, 0, radius, radius))
        self.ltHeadCollNode.addSolid(CollisionSphere(0, 0, 0, radius))
        self.ltLHandCollNode.addSolid(CollisionSphere(0, 0, 0, 2 * radius / 3.))
        self.ltRHandCollNode.addSolid(CollisionSphere(0, 0, 0, 2 * radius / 3.))
        self.toonCollNodes = [legsCollNodepath,
                              headCollNodepath,
                              lHandCollNodepath,
                              rHandCollNodepath,
                              ]

    def destroyCatchCollisions(self):
        if not hasattr(self, "ltLegsCollNode"):
            return

        for collNode in self.toonCollNodes:
            while collNode.node().getNumSolids():
                collNode.node().removeSolid(0)
            base.localAvatar.cTrav.removeCollider(collNode)
        del self.toonCollNodes        
        del self.ltLegsCollNode
        del self.ltHeadCollNode
        del self.ltLHandCollNode
        del self.ltRHandCollNode
    
    def timerExpired(self):
        pass

    def __handleCatch(self, generation, objNum):
        DistributedPartyCatchActivity.notify.debug("catch: %s" % [generation, objNum])
        if base.localAvatar.doId not in self.toonIds:
            return
        # localtoon just caught obj (serial number 'objNum')
        self.showCatch(base.localAvatar.doId, generation, objNum)
        # tell the AI we caught this obj
        objName = self._id2gen[generation].droppedObjNames[objNum]
        objTypeId = PartyGlobals.Name2DOTypeId[objName]
        self.sendUpdate('claimCatch', [generation, objNum, objTypeId])
        # make the object disappear
        # NOTE: it is important to do this AFTER sending the claimCatch msg
        # the interval will send a 'reportDone' msg if it's the last item
        self.finishDropInterval(generation, objNum)

    def showCatch(self, avId, generation, objNum):
        """ show the result of the catch action """
        if not self.toonSDs.has_key(avId):
            return
        isLocal = (avId == base.localAvatar.doId)
        if generation not in self._id2gen:
            return
        if not self._id2gen[generation].hasBeenScheduled:
            return
        objName = self._id2gen[generation].droppedObjNames[objNum]
        objType = PartyGlobals.Name2DropObjectType[objName]
        if objType.good:
            # have we already shown this fruit being eaten?
            if not self._id2gen[generation].droppedObjCaught.has_key(objNum):
                if isLocal:
                    base.playSfx(self.sndGoodCatch)

                # make the toon eat the fruit
                fruit = self.getObjModel(objName)
                toon = self.getAvatar(avId)
                # 500 LOD
                rHand = toon.getRightHands()[1]
                self.toonSDs[avId].eatFruit(fruit, rHand)
        else:
            self.toonSDs[avId].fsm.request('fallForward')

        self._id2gen[generation].droppedObjCaught[objNum] = 1

    def setObjectCaught(self, avId, generation, objNum):
        """ called by the AI to announce a catch """
        self.notify.info('setObjectCaught(%s, %s, %s)' % (avId, generation, objNum))

        if self.activityFSM.state != 'Active':
            DistributedPartyCatchActivity.notify.warning(
                'ignoring msg: object %s caught by %s' % (objNum, avId)
                )
            return

        isLocal = (avId == base.localAvatar.doId)

        if not isLocal:
            DistributedPartyCatchActivity.notify.debug("AI: avatar %s caught %s" % (avId, objNum))
            # if remote av caught an object, its interval might still
            # be playing. make sure it's finished
            self.finishDropInterval(generation, objNum)
            self.showCatch(avId, generation, objNum)

        # make sure we've scheduled drops before continuing
        self._scheduleGenerations()

        # update the toon's score
        gen = self._id2gen[generation]
        if gen.hasBeenScheduled:
            objName = gen.droppedObjNames[objNum]
            if PartyGlobals.Name2DropObjectType[objName].good:
                # If we're going from Idle to Conclusion because we entered the party
                # during conclusion, we won't have scores.
                if hasattr(self, "scores"):
                    i = self.toonIds.index(avId)
                    self.scores[i] += 1
                    self.fruitsCaught += 1

    def finishDropInterval(self, generation, objNum):
        """ this function ensures that the drop interval for object
        number 'objNum' has finished; if interval already finished,
        does nothing """
        if hasattr(self, "dropIntervals"):
            if self.dropIntervals.has_key((generation, objNum)):
                self.dropIntervals[(generation, objNum)].finish()

    def finishAllDropIntervals(self):
        if hasattr(self, "dropIntervals"):    
            for dropInterval in self.dropIntervals.values():
                dropInterval.finish()

    def setGenerations(self, generations):
        # some factor (such as the number of players) has changed and
        # there is a new drop generation forced by the server
        # some expired generations may have been discarded as well
        self.notify.info('setGenerations(%s)' % (generations,))
        gen2t = {}
        gen2nt = {}
        gen2np = {}
        for id, timestamp32, numPlayers in generations:
            gen2t[id] = globalClockDelta.networkToLocalTime(timestamp32, bits=32) - self._startTimestamp
            gen2nt[id] = timestamp32
            gen2np[id] = numPlayers
        # prune removed generations
        ids = self._id2gen.keys()
        for id in ids:
            if id not in gen2t:
                self._removeGeneration(id)
        # add new generations
        for id in gen2t:
            if id not in self._id2gen:
                self._addGeneration(id, gen2t[id], gen2nt[id], gen2np[id])

    def scheduleDrops(self, genId=None):
        # We give out a 'perfect' bonus for catching all of the fruit.
        # To make the difficulty of catching them all consistent from
        # session to session, we need to hold the number of fruits
        # constant. So, rather than deciding what to drop on-the-fly,
        # based on a probability table, we need something more precise.
        # We need to create a list of drop types, with the correct number
        # of fruits, and randomize that list, thus ensuring that we drop
        # a precise total number of fruits.

        if genId is None:
            genId = self.getCurGeneration()
        gen = self._id2gen[genId]

        if gen.hasBeenScheduled:
            return

        # add a bit to compensate for network time resolution error
        fruitIndex = int((gen.startTime + (.5 * self.DropPeriod)) /
                      PartyGlobals.CatchActivityDuration)
        fruitNames = ['apple', 'orange', 'pear', 'coconut', 'watermelon', 'pineapple']
        fruitName = fruitNames[fruitIndex % len(fruitNames)]

        rng = RandomNumGen(genId + self._generationSeedBase)
        # it's important to do this after we seed the rng because of
        # the implementation of dropTask()
        #self._generation += 1

        # make a big list of all the drops that should be done
        gen.droppedObjNames = ([fruitName] * self.numFruits) + \
                              (['anvil'] * self.numAnvils)
        # scramble the list (using the game's RNG so it comes out the
        # same on each client)
        rng.shuffle(gen.droppedObjNames)

        # self.droppedObjNames now contains a complete, ordered list
        # of the types of each object that will be dropped

        # create a drop placer, and construct a schedule of drops
        dropPlacer = PartyRegionDropPlacer(self, genId, gen.droppedObjNames,
                                           startTime=gen.startTime)
        # reset the dropped item counter
        gen.numItemsDropped = 0

        # fast-forward the placer to sync up relative to the game start time,
        # to preserve the drop-frequency interest curve
        tIndex = gen.startTime % PartyGlobals.CatchActivityDuration
        tPercent = float(tIndex) / PartyGlobals.CatchActivityDuration
        gen.numItemsDropped += dropPlacer.skipPercent(tPercent)

        while not dropPlacer.doneDropping(continuous=True):
            nextDrop = dropPlacer.getNextDrop()
            #dropTime, objName, dropCoords = nextDrop
            gen.dropSchedule.append(nextDrop)

        assert len(gen.droppedObjNames) == len(gen.dropSchedule)

        gen.hasBeenScheduled = True

    def startDropTask(self):
        taskMgr.add(self.dropTask, self.DropTaskName)

    def stopDropTask(self):
        taskMgr.remove(self.DropTaskName)

    def _scheduleGenerations(self):
        curT = self.getCurrentCatchActivityTime()

        genIndex = self._orderedGenerationIndex
        newGenIndex = genIndex

        # advance through the drop generations when it's time to do so
        while ((genIndex is None) or
               (genIndex < (len(self._orderedGenerations)-1))):
            if genIndex is None:
                nextGenIndex = 0
            else:
                nextGenIndex = genIndex + 1
            nextGenId = self._orderedGenerations[nextGenIndex]
            nextGen = self._id2gen[nextGenId]
            startT = nextGen.startTime
            ## allow for one minute of network time discrepancy
            #if (curT < (startT - 60.)):
            #    break
            if (curT >= startT):
                newGenIndex = nextGenIndex
            if (not nextGen.hasBeenScheduled):
                # adjust the constants to the new conditions
                self.defineConstants(forceNumPlayers=nextGen.numPlayers)
                self.scheduleDrops(genId=self._orderedGenerations[nextGenIndex])

            genIndex = nextGenIndex

        self._orderedGenerationIndex = newGenIndex

    def dropTask(self, task):
        self._scheduleGenerations()

        curT = self.getCurrentCatchActivityTime()

        # start all the drops that should already be happening
        # the drop schedule is a time-ordered list of
        # (time, objName, dropRegion) tuples

        if self._orderedGenerationIndex is not None:
            # only process drops from the most recent generation
            i = self._orderedGenerationIndex

            genIndex = self._orderedGenerations[i]
            gen = self._id2gen[genIndex]

            while ((len(gen.dropSchedule) > 0) and (gen.dropSchedule[0][0] < curT)):
                drop = gen.dropSchedule[0]
                # pop this one off the front
                gen.dropSchedule = gen.dropSchedule[1:]

                dropTime, objName, dropCoords = drop
                objNum = gen.numItemsDropped
                #lastDrop = (len(self.dropSchedule) == 0)
                x, y = self.grid2world(*dropCoords)

                dropIval = self.getDropIval(x, y, objName, genIndex, objNum)

                def cleanup(generation, objNum, self=self, ):#lastDrop=lastDrop):
                    del self.dropIntervals[(generation, objNum)]
                    #if lastDrop:
                    #    self.sendUpdate('reportDone')

                dropIval.append(Func(Functor(cleanup, genIndex, objNum)))

                # add this drop interval to the master table
                self.dropIntervals[(genIndex, objNum)] = dropIval
                # and increment the tally of dropped objects
                gen.numItemsDropped += 1

                # Interval.start takes # seconds into the interval at which to start
                dropIval.start(curT - dropTime)

                self._lastDropTime = dropTime

                """
                if lastDrop:
                    return Task.done
                    """

        return Task.cont

    def getDropIval(self, x, y, dropObjName, generation, num):
        """ x, y: -1..1 """
        objType = PartyGlobals.Name2DropObjectType[dropObjName]

        id = (generation, num)
        dropNode = hidden.attachNewNode('catchDropNode%s' % (id, ))
        dropNode.setPos(x, y, 0)
        # must be copy, not instance
        shadow = self.dropShadow.copyTo(dropNode)
        shadow.setZ(PartyGlobals.CatchDropShadowHeight)
        shadow.setColor(1, 1, 1, 1)
        # must be copy, not instance
        object = self.getObjModel(dropObjName)
        object.reparentTo(hidden)

        # turn the obj
        if dropObjName in ['watermelon', 'anvil']:
            # these objs shouldn't stray too far from their original heading
            objH = object.getH()
            absDelta = {'watermelon' : 12,
                        'anvil' : 15,
                        }[dropObjName]
            delta = ((self.randomNumGen.random() * 2.) - 1.) * absDelta
            newH = objH + delta
        else:
            newH = self.randomNumGen.random() * 360.
        object.setH(newH)

        # give the object a collision sphere
        sphereName = 'FallObj%s' % (id, )
        # x,y,z,radius
        radius = self.ObjRadius
        # make the sphere larger on higher difficulty levels
        if objType.good:
            radius *= lerp(1., 1.3, 0.5)
        collSphere = CollisionSphere(0, 0, 0, radius)
        # don't let it push the toons
        collSphere.setTangible(0)
        collNode = CollisionNode(sphereName)
        collNode.setCollideMask(PartyGlobals.CatchActivityBitmask)
        collNode.addSolid(collSphere)
        collNodePath = object.attachNewNode(collNode)
        collNodePath.hide()
        if self.ShowObjSpheres:
            collNodePath.show()

        # listen for collisions
        catchEventName = 'ltCatch' + sphereName
        # collision callback accepts a 'collision entry' object
        # with details about the collision; we forward through a function
        # whose sole purpose is to 'eat' the collision entry object
        def eatCollEntry(forward, collEntry):
            forward()
        self.accept(catchEventName,
                    Functor(eatCollEntry,
                            Functor(self.__handleCatch, id[0], id[1])))

        def cleanup(self=self, dropNode=dropNode, id=id,
                    event=catchEventName):
            self.ignore(event)
            dropNode.removeNode()

        duration = objType.fallDuration
        onscreenDuration = objType.onscreenDuration
        #dropHeight = self.MinOffscreenHeight

        targetShadowScale = .3
        if self.trickShadows:
            intermedScale = (
                targetShadowScale * 
                (self.OffscreenTime / self.BaselineDropDuration))
            # grow at the standard rate...
            shadowScaleIval = Sequence(
                LerpScaleInterval(shadow,
                                  self.OffscreenTime,
                                  intermedScale,
                                  startScale=0))
            # then balloon up quicker in time for the landing, now that
            # the object is on-screen
            shadowScaleIval.append(
                LerpScaleInterval(shadow,
                                  duration - self.OffscreenTime,
                                  targetShadowScale,
                                  startScale=intermedScale))
        else:
            shadowScaleIval = LerpScaleInterval(shadow, duration,
                                                targetShadowScale, startScale=0)

        # gradually alpha the shadow in
        targetShadowAlpha = .4
        shadowAlphaIval = LerpColorScaleInterval(
            shadow, self.OffscreenTime, Point4(1, 1, 1, targetShadowAlpha),
            startColorScale=Point4(1, 1, 1, 0))

        shadowIval = Parallel(
            shadowScaleIval,
            shadowAlphaIval,
            )

        if self.useGravity:
            # object should drop according to the path defined by
            # the Trajectory object corresponding to the object type.
            def setObjPos(t, objType=objType, object=object):
                z = objType.trajectory.calcZ(t)
                object.setZ(z)
                
            # put the object at its starting position, which happens to be
            # off-screen
            setObjPos(0)

            dropIval = LerpFunctionInterval(setObjPos,
                                            fromData=0,
                                            toData=onscreenDuration,
                                            duration=onscreenDuration)
        else:
            startPos = Point3(0, 0, self.MinOffscreenHeight)
            # put the object at its starting position, which happens to be
            # off-screen
            object.setPos(startPos)
            dropIval = LerpPosInterval(object, onscreenDuration,
                                       Point3(0, 0, 0), startPos=startPos,
                                       blendType='easeIn')

        ival = Sequence(
            Func(Functor(dropNode.reparentTo, self.root)),
            Parallel(Sequence(WaitInterval(self.OffscreenTime),
                              Func(Functor(object.reparentTo, dropNode)),
                              dropIval,
                              ),
                     shadowIval,
                     ),
            Func(cleanup),
            name='drop%s' % (id, ),
            )

        if objType == PartyGlobals.Name2DropObjectType['anvil']:
            ival.append(Func(self.playAnvil))
        return ival

    def playAnvil(self):
        if base.localAvatar.doId in self.toonIds:
            base.playSfx(self.sndAnvilLand)

    # orthowalk init/shutdown
    def initOrthoWalk(self):
        DistributedPartyCatchActivity.notify.debug("startOrthoWalk")

        def doCollisions(oldPos, newPos, self=self):
            # make the toon collide against the boundaries of the playfield
            x = bound(newPos[0], self.StageHalfWidth, - self.StageHalfWidth)
            y = bound(newPos[1], self.StageHalfHeight, - self.StageHalfHeight)
            newPos.setX(x)
            newPos.setY(y)
            return newPos

        orthoDrive = OrthoDrive(
            self.ToonSpeed,
            #customCollisionCallback=doCollisions,
            instantTurn=True,
            )
        self.orthoWalk = OrthoWalk(orthoDrive, broadcast=True)

    def destroyOrthoWalk(self):
        DistributedPartyCatchActivity.notify.debug("destroyOrthoWalk")
        if hasattr(self, "orthoWalk"):
            self.orthoWalk.stop()
            self.orthoWalk.destroy()
            del self.orthoWalk

##     def startRequestResponse(self, started):
##         """
##         Response from the server to our request to start the activity.
##         """
##         started = bool(started) # convert back from integer
##         if started:
##             self.d_toonJoinRequest()
##         else:
##             self.showMessage(TTLocalizer.PartyCatchCannotStart)
    
    # FSM transition methods
    def startIdle(self):
        DistributedPartyCatchActivity.notify.debug("startIdle")
    
    def finishIdle(self):
        DistributedPartyCatchActivity.notify.debug("finishIdle")
        
    def startActive(self):
        DistributedPartyCatchActivity.notify.debug("startActive")
        for avId in self.toonIds:
            if self.toonSDs.has_key(avId):
                toonSD = self.toonSDs[avId]
                toonSD.enter()
                toonSD.fsm.request('normal')
                """
            if avId != base.localAvatar.doId:
                if self.cr.doId2do.has_key(avId):
                    self.cr.doId2do[avId].reparentTo(self.avatarNodePath)
                    """

        # Initialize the scoreboard
        self.scores = [0] * 20
        #spacing = 0.4

        # This line puts 4 of your toons at the 4 corners of the falling grid
#        self.showPosts()

        # keep a tally of the fruits that are caught so we can figure out if
        # it was a perfect game
        self.fruitsCaught = 0

        # dict of drop intervals, indexed by (generation, obj num)
        self.dropIntervals = {}

        """
        # this will hold the names of the objects to be dropped
        self.droppedObjNames = []
        # this will hold a list of drops to perform and when to perform them
        self.dropSchedule = []

        self.numItemsDropped = 0
        """

        # calculate a sequence of drops, using the game's seeded rng
        #self.scheduleDrops()
        # start the drop task
        self.startDropTask()

        #self.timer.countdown(PartyGlobals.CatchActivityDuration, self.timerExpired)
        #if base.localAvatar.doId in self.toonIds:
        #    self.timer.unstash()

        if base.localAvatar.doId in self.toonIds:
            self.putLocalAvatarInActivity()

    def finishActive(self):
        DistributedPartyCatchActivity.notify.debug("finishActive")
        self.stopDropTask()
        if hasattr(self, 'finishIval'):
            self.finishIval.pause()
            del self.finishIval

        #self.timer.stop()
        #self.timer.stash()

        if base.localAvatar.doId in self.toonIds:
            self.takeLocalAvatarOutOfActivity()
        # get rid of the drop intervals
        for ival in self.dropIntervals.values():
            ival.finish()
        del self.dropIntervals


    def startConclusion(self):
        DistributedPartyCatchActivity.notify.debug("startConclusion")
        
        for avId in self.toonIds:
            if self.toonSDs.has_key(avId):
                toonSD = self.toonSDs[avId]
                toonSD.fsm.request('notPlaying')

        # restore localToon's collision setup
        self.destroyCatchCollisions()

        if base.localAvatar.doId not in self.toonIds:
            return
        else:
            # Because conclusion is bypassing d_toonExitRequest during the conclusion, this needs to be
            # set in order for the server to clean up the Toon properly.
            self.localToonExiting()

        # if it was a perfect game, let the players know
        if self.fruitsCaught >= self.numFruits:
            finishText = TTLocalizer.PartyCatchActivityFinishPerfect
        else:
            finishText = TTLocalizer.PartyCatchActivityFinish

        perfectTextSubnode = hidden.attachNewNode(
            self.__genText(finishText))
        perfectText = hidden.attachNewNode('perfectText')
        perfectTextSubnode.reparentTo(perfectText)
        # offset the subnode so that the text is centered on both axes
        # we need the parent node so that the text will scale correctly
        frame = self.__textGen.getCardActual()
        offsetY = - abs(frame[2] + frame[3]) / 2.
        perfectTextSubnode.setPos(0, 0, offsetY)

        perfectText.setColor(1, .1, .1, 1)

        def fadeFunc(t, text=perfectText):
            text.setColorScale(1, 1, 1, t)
        def destroyText(text=perfectText):
            text.removeNode()

        textTrack = Sequence(
            Func(perfectText.reparentTo, aspect2d),
            Parallel(LerpScaleInterval(perfectText, duration=.5,
                                       scale=.3, startScale=0.),
                     LerpFunctionInterval(fadeFunc,
                                          fromData=0., toData=1.,
                                          duration=.5,)
                     ),
            Wait(2.),
            Parallel(LerpScaleInterval(perfectText, duration=.5,
                                       scale=1.),
                     LerpFunctionInterval(fadeFunc,
                                          fromData=1., toData=0.,
                                          duration=.5,
                                          blendType="easeIn"),
                     ),
            Func(destroyText),
            WaitInterval(.5),
            )
        
        soundTrack = SoundInterval(self.sndPerfect)

        self.finishIval = Parallel(textTrack,
                                    soundTrack)
        self.finishIval.start()

    def finishConclusion(self):
        DistributedPartyCatchActivity.notify.debug("finishConclusion")
        if base.localAvatar.doId in self.toonIds:
            self.takeLocalAvatarOutOfActivity()
            base.cr.playGame.getPlace().fsm.request('walk')

    def showJellybeanReward(self, earnedAmount, jarAmount, message):
        # don't show reward panel if no jellybeans earned
        # player probably joined game by accident
        if earnedAmount > 0:
            DistributedPartyActivity.showJellybeanReward(self, earnedAmount, jarAmount, message)
        else:
            base.cr.playGame.getPlace().fsm.request('walk')
