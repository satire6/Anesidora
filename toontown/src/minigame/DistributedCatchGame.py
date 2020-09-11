"""DistributedCatchGame module: contains the DistributedCatchGame class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from DistributedMinigame import *
from direct.interval.IntervalGlobal import *
from OrthoWalk import *
from direct.showbase.PythonUtil import Functor, bound, lineupPos, lerp
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import TTLocalizer
import CatchGameGlobals
from direct.task.Task import Task
from toontown.toon import Toon
from toontown.suit import Suit
import MinigameAvatarScorePanel
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
import CatchGameToonSD
import Trajectory
import math
from direct.distributed import DistributedSmoothNode
from direct.showbase.RandomNumGen import RandomNumGen
import MinigameGlobals
from toontown.toon import ToonDNA
from toontown.suit import SuitDNA

# explicitly bring some drop-object-type tables into the local scope
from CatchGameGlobals import DropObjectTypes
from CatchGameGlobals import Name2DropObjectType

# and bring in everything from DropPlacer
from DropPlacer import *
from DropScheduler import *

class DistributedCatchGame(DistributedMinigame):

    DropTaskName = 'dropSomething'
    EndGameTaskName = 'endCatchGame'
    SuitWalkTaskName = 'catchGameSuitWalk'

    DropObjectPlurals = {
        'apple'      : TTLocalizer.CatchGameApples,
        'orange'     : TTLocalizer.CatchGameOranges,
        'pear'       : TTLocalizer.CatchGamePears,
        'coconut'    : TTLocalizer.CatchGameCoconuts,
        'watermelon' : TTLocalizer.CatchGameWatermelons,
        'pineapple'  : TTLocalizer.CatchGamePineapples,
        'anvil'      : TTLocalizer.CatchGameAnvils,
        }

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedCatchGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
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

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        self.setUsesSmoothing()
        self.setUsesLookAround()

    def getTitle(self):
        return TTLocalizer.CatchGameTitle

    def getInstructions(self):
        return TTLocalizer.CatchGameInstructions % {
            'fruit'    : self.DropObjectPlurals[self.fruitName],
            'badThing' : self.DropObjectPlurals['anvil']}

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return CatchGameGlobals.GameDuration + 5

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here
        self.defineConstants()

        groundModels = [
            "phase_4/models/minigames/treehouse_2players",
            "phase_4/models/minigames/treehouse_2players",
            "phase_4/models/minigames/treehouse_3players",
            "phase_4/models/minigames/treehouse_4players",
            ]
        index = self.getNumPlayers()-1
        self.ground = loader.loadModel(groundModels[index])
        self.ground.setHpr(180,-90,0)

        self.dropShadow = loader.loadModel(
            'phase_3/models/props/drop_shadow')
        # load the models for the drop objects (see CatchGameGlobals.py)
        # index by object type name
        self.dropObjModels = {}
        for objType in DropObjectTypes:
            # optimization: assuming we're only going to be
            # dropping anvils and one type of fruit per game,
            # only load those two models
            if objType.name not in ['anvil', self.fruitName]:
                continue
            
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
            if objType == Name2DropObjectType['pear']:
                # pear needs to be moved down
                model.setZ(-.6)
            if objType == Name2DropObjectType['coconut']:
                # turn the coconut upside-down so we can see the dots
                model.setP(180)
            if objType == Name2DropObjectType['watermelon']:
                # turn the watermelon to an interesting angle, and move it down
                model.setH(135)
                model.setZ(-.5)
            if objType == Name2DropObjectType['pineapple']:
                # move the pineapple down
                model.setZ(-1.7)
            if objType == Name2DropObjectType['anvil']:
                # anvil needs to be moved down a foot
                model.setZ(-self.ObjRadius)
            model.flattenMedium()

        self.music = base.loadMusic("phase_4/audio/bgm/MG_toontag.mid")
        self.sndGoodCatch = base.loadSfx('phase_4/audio/sfx/SZ_DD_treasure.mp3')
        self.sndOof = base.loadSfx(
            'phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.sndAnvilLand = base.loadSfx(
            'phase_4/audio/sfx/AA_drop_anvil_miss.mp3')

        self.sndPerfect = base.loadSfx(
            "phase_4/audio/sfx/ring_perfect.mp3")

        # make a dictionary of CatchGameToonSDs; they will track
        # toons' states and animate them appropriately
        self.toonSDs = {}
        # add the local toon now, add remote toons as they join
        avId = self.localAvId
        toonSD = CatchGameToonSD.CatchGameToonSD(avId, self)
        self.toonSDs[avId] = toonSD
        toonSD.load()

        # create a few suits that will be walked across the play area
        if self.WantSuits:
            suitTypes = ['f',  # flunky
                         'tm', # telemarketer
                         'pp', # penny pincher
                         'dt', # double talker
                         ]
            self.suits = []
            for type in suitTypes:
                suit = Suit.Suit()
                d = SuitDNA.SuitDNA()
                d.newSuit(type)
                suit.setDNA(d)
                # cache the walk anim
                suit.pose('walk', 0)

                self.suits.append(suit)

        # this will be used to generate textnodes
        self.__textGen = TextNode("ringGame")
        self.__textGen.setFont(ToontownGlobals.getSignFont())
        self.__textGen.setAlign(TextNode.ACenter)

        self.introMovie = self.getIntroMovie()

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        self.introMovie.finish()
        del self.introMovie

        del self.__textGen

        for avId in self.toonSDs.keys():
            toonSD = self.toonSDs[avId]
            toonSD.unload()
        del self.toonSDs

        for suit in self.suits:
            suit.reparentTo(hidden)
            suit.delete()
        del self.suits

        self.ground.removeNode()
        del self.ground

        self.dropShadow.removeNode()
        del self.dropShadow

        for model in self.dropObjModels.values():
            model.removeNode()
        del self.dropObjModels
            
        del self.music
        del self.sndGoodCatch
        del self.sndOof
        del self.sndAnvilLand
        del self.sndPerfect

    def getObjModel(self, objName):
        """ returns a copy of the drop object corresponding to 'objName',
        parented under hidden """
        return self.dropObjModels[objName].copyTo(hidden)

    def __genText(self, text):
        self.__textGen.setText(text)
        return self.__textGen.generate()

    def calcDifficultyConstants(self, difficulty, numPlayers):
        """ This function calculates the constants that depend on
        the difficulty settings and/or the number of players
        This function can be called repeatedly with different parameters
        at the start of a minigame session. """
        # Choose a speed for the toons. This is the main difficulty parameter.
        # The onscreen time for falling objects is calculated directly based
        # on this value. More difficult games simply move faster; faster toons,
        # faster falling objects.
        ToonSpeedRange = [16., 25.]
        self.ToonSpeed = lerp(ToonSpeedRange[0],
                              ToonSpeedRange[1],
                              difficulty)
        # no need to scale up the toon speed when more toons are playing;
        # each individual toon doesn't need to be able to cover the
        # entire stage

        self.SuitSpeed = self.ToonSpeed / 2.
        self.SuitPeriodRange = [lerp(5., 3., self.getDifficulty()),
                                lerp(15., 8., self.getDifficulty())]

        def scaledDimensions(widthHeight,scale):
            """
            returns [w2,h2], where (w2*h2 == scale*w*h) and w/h==w2/h2
            In other words, it returns a width and height whose area is
            'scale' times the area of the provided width and height,
            preserving the width:height ratio.
            """
            # we know:
            # w2*h2 = s*w*h
            # w/h = w2/h2
            #
            # solve for h2 in terms of w2, w, and h
            # w/h = w2/h2
            # h2 = h*w2/w
            #
            # plug it in the other eq
            # w2*h2 = s*w*h
            # w2*h*w2/w = s*w*h
            # w2^2*h/w = s*w*h
            # w2^2 = s*w^2
            # the same holds true for height:
            # h2^2 = s*h^2
            #
            # since width and height cannot be negative:
            # w2 = sqrt(s*w^2)
            # h2 = sqrt(s*h^2)
            w,h = widthHeight
            return [math.sqrt(scale * w * w),
                    math.sqrt(scale * h * h),
                    ]

        # width, height (in feet)
        BaseStageDimensions = [20,15]
        # scale up the stage for 3 and 4 players
        areaScales = [1.,1.,3./2,4./2]
        self.StageAreaScale = areaScales[numPlayers-1]
        self.StageLinearScale = math.sqrt(self.StageAreaScale)
        self.notify.debug("StageLinearScale: %s" % self.StageLinearScale)
        self.StageDimensions = scaledDimensions(BaseStageDimensions,
                                                self.StageAreaScale)
        self.notify.debug("StageDimensions: %s" % self.StageDimensions)
        self.StageHalfWidth = self.StageDimensions[0]/2.
        self.StageHalfHeight = self.StageDimensions[1]/2.

        # MinOffscreenHeight (moH): this is a Z height that is just
        # off the top of the screen; it's safe for objects to pop
        # into existence at this height.
        MOHs = [24]*2 + [26,28]
        self.MinOffscreenHeight = MOHs[self.getNumPlayers()-1]

        # Calculate an onscreen time for the baseline falling objects so
        # that toons can reasonably run from one corner of the stage
        # to the opposite corner in time to catch a fruit.
        #
        # Keep in mind that the toon most likely just caught the previous
        # fruit, most likely close to the end of its fall; that means the
        # next fruit is either halfway through its fall, or even 3/4
        # of the way down during the end-game drop blitz (assuming that
        # the drop period, defined below, is 1/2 of the baseline drop
        # duration)
        #
        # Also keep in mind that the drop period is based off of the
        # _entire_ fall duration of the baseline object, of which
        # the onscreen fall duration is only a part (see definition
        # of self.OffscreenTime, below;
        # fall duration = offscreen time + onscreen time
        distance = math.sqrt(
            (self.StageDimensions[0] * self.StageDimensions[0]) +
            (self.StageDimensions[1] * self.StageDimensions[1]))
        # when there are more players, each individual toon doesn't need
        # to be able to cover the entire stage...
        distance /= self.StageLinearScale

        # when we're dropping objects in a spatially contiguous fashion,
        # we don't need to be able to run as far between catches
        if self.DropPlacerType == PathDropPlacer:
            distance /= 1.5

        ToonRunDuration = distance / self.ToonSpeed
        # this is the ratio of offscreen to onscreen time for the baseline
        # object.
        # 1. == object is offscreen for same duration that it's onscreen
        # .5 == object is offscreen 1/2 as long as it's onscreen
        offScreenOnScreenRatio = 1.
        # this is the fraction of the total baseline object fall duration
        # (offscreen and on, from the moment the shadow shows up to the
        # moment the obj hits the ground) during which the toon should be
        # able to run the full diagonal of the stage
        fraction = (1./3)*.85
        # ToonRunDuration = fraction * (FallDur)
        # ToonRunDuration = fraction * (OnscreenDur + OffscreenDur)
        # ToonRunDuration = fraction * (OnscreenDur + (OnscreenDur*OffOnratio))
        # (OnscreenDur + (OnscreenDur*OffOnratio)) = ToonRunDuration / fraction
        # OnscreenDur * (1 + OffOnratio) = ToonRunDuration / fraction
        # OnscreenDur = ToonRunDuration / [fraction * (1 + OffOnratio)]
        self.BaselineOnscreenDropDuration = (
            ToonRunDuration / (fraction * (1. + offScreenOnScreenRatio)))
        self.notify.debug("BaselineOnscreenDropDuration=%s" %
                          self.BaselineOnscreenDropDuration)

        # tOff. How long all objects 'drop' before reaching moH (during this
        # period, you just see the shadow growing on the ground)
        self.OffscreenTime = (offScreenOnScreenRatio *
                              self.BaselineOnscreenDropDuration)
        self.notify.debug("OffscreenTime=%s" % self.OffscreenTime)

        # at this point, we can calculate the total drop duration for
        # baseline objects
        self.BaselineDropDuration = (self.BaselineOnscreenDropDuration +
                                     self.OffscreenTime)

        # this should be OK as long as we don't make any object types
        # that fall slower than the baseline type...
        self.MaxDropDuration = self.BaselineDropDuration

        # period at which to drop objects; based on the baseline object's
        # fall duration
        self.DropPeriod = self.BaselineDropDuration / 2.
        # dampen the impact of each successive player, on the theory that
        # it's actually more difficult to catch all the fruit with more players
        scaledNumPlayers = (((numPlayers - 1.) * .75) + 1.)
        self.DropPeriod /= scaledNumPlayers

        # figure out how many fruits and anvils will be dropped

        # relative probabilities that a given drop object will
        # be of a particular type
        typeProbs = {'fruit' : 3,
                     'anvil' : 1,
                     }
        # normalize the probabilities to [0..1]
        probSum = reduce(lambda x,y: x+y, typeProbs.values())
        for key in typeProbs.keys():
            typeProbs[key] = float(typeProbs[key]) / probSum

        scheduler = DropScheduler(
            CatchGameGlobals.GameDuration,
            self.FirstDropDelay, self.DropPeriod, self.MaxDropDuration,
            self.FasterDropDelay, self.FasterDropPeriodMult)

        self.totalDrops = 0
        while not scheduler.doneDropping():
            scheduler.stepT()
            self.totalDrops += 1

        # calc number of fruits
        self.numFruits = int(self.totalDrops * typeProbs['fruit'])
        # however many drop slots are left, that's how many anvils
        # there will be
        self.numAnvils = int(self.totalDrops - self.numFruits)

    def getNumPlayers(self):
        """
        the return value of this function can be monkeyed with
        to get the game to act as if it's being played by a certain
        number of players
        code that would get messed up by using the wrong value for
        number of players should use self.numPlayers directly
        """
        # uncomment for debugging
        #return 4
        #return 3
        #return 2
        #return 1
        return self.numPlayers

    def defineConstants(self):
        self.notify.debug('defineConstants')

        # choose a drop placer
        #self.DropPlacerType = RandomDropPlacer
        self.DropPlacerType = RegionDropPlacer
        #self.DropPlacerType = PathDropPlacer
        assert (self.DropPlacerType)

        # determine what fruit we'll be using
        fruits = {
            ToontownGlobals.ToontownCentral:   'apple',
            ToontownGlobals.DonaldsDock:       'orange',
            ToontownGlobals.DaisyGardens:      'pear',
            ToontownGlobals.MinniesMelodyland: 'coconut',
            ToontownGlobals.TheBrrrgh:         'watermelon',
            ToontownGlobals.DonaldsDreamland:  'pineapple',
            }
        self.fruitName = fruits[self.getSafezoneId()]
        # override
        #self.fruitName = 'watermelon'

        self.ShowObjSpheres = 0
        self.ShowToonSpheres = 0
        self.ShowSuitSpheres = 0

        self.PredictiveSmoothing = 1

        self.UseGravity = 1

        # set this to true to make shadows of fast-falling objects grow
        # as if they were standard shadows until their associated object
        # comes on-screen, then scale up to full size, faster, in time
        # for the landing
        self.TrickShadows = 1

        self.WantSuits = 1

        # this is how long the game waits to start dropping stuff
        self.FirstDropDelay = .5

        # after this many seconds, the game starts dropping things faster
        self.FasterDropDelay = int((2./3) * CatchGameGlobals.GameDuration)
        self.notify.debug('will start dropping fast after %s seconds' %
                          self.FasterDropDelay)

        # how much shorter should the drop period be (time between
        # drops) during the 'faster drop' interval at the end of
        # the game? .5 == 2x as fast, 1. == no difference
        self.FasterDropPeriodMult = .5

        if __debug__:
            # assert that the numFruits table in CatchGameGlobals
            # is up-to-date
            upToDate = 1
            correctTable = [{},{},{},{}]
            for numPlayers in [1,2,3,4]:
                for zone in MinigameGlobals.SafeZones:
                    self.calcDifficultyConstants(
                        MinigameGlobals.getDifficulty(zone), numPlayers)
                    correctTable[numPlayers-1][zone] = self.numFruits
                    if (CatchGameGlobals.NumFruits[numPlayers-1][zone] !=
                        self.numFruits):
                        upToDate = 0

            # construct the source code for the correct numFruits table
            str = '\n'
            str += ('# THIS TABLE WAS GENERATED BY %s.py; DO NOT EDIT\n' %
                    __name__)
            str += 'NumFruits = ['
            for numPlayers in [1,2,3,4]:
                playerStr = 'player'
                if numPlayers > 1:
                    playerStr = 'players'
                str += '\n    # %s %s' % (numPlayers, playerStr)
                str += '\n    {'
                for zone in MinigameGlobals.SafeZones:
                    str += ('%s:%s,' %
                            (zone, correctTable[numPlayers-1][zone]))
                str += '},'
            str += '\n    ]\n'

            if not upToDate:
                # print out the correct table with the assertion
                self.notify.error(
                    str +
                    '\nCatchGameGlobals.NumFruits table for the AI server '
                    'is out-of-date.\n'
                    'Please replace with the preceding table.'
                    )
            else:
                print str
            

        self.calcDifficultyConstants(self.getDifficulty(),
                                     self.getNumPlayers())

        self.notify.debug("ToonSpeed: %s" % self.ToonSpeed)
        self.notify.debug("total drops: %s" % self.totalDrops)
        self.notify.debug("numFruits: %s" % self.numFruits)
        self.notify.debug("numAnvils: %s" % self.numAnvils)

        self.ObjRadius = 1.

        # objects fall on a grid; these are the dimensions of the grid
        dropGridDimensions = [
            [5,5],
            [5,5],
            [6,6],
            [7,7],
            ]
        self.DropRows, self.DropColumns = dropGridDimensions[
            self.getNumPlayers()-1]

        self.cameraPosTable = [
            [0,-29.36,28.17]] * 2 + [
            [0,-32.87,30.43],
            [0,-35.59,32.10],
            ]
        self.cameraHpr = [0,-35,0]

        self.CameraPosHpr = (self.cameraPosTable[self.getNumPlayers()-1] +
                             self.cameraHpr)

        # fix up the drop object table according to the difficulty level,
        # set up per-object-type Trajectory objects and related variables
        for objType in DropObjectTypes:
            self.notify.debug("*** Object Type: %s" % objType.name)

            # each object type has an onscreen drop duration multiplier
            # that specifies how long the object should be onscreen,
            # relative to the baseline duration.
            objType.onscreenDuration = (objType.onscreenDurMult *
                                        self.BaselineOnscreenDropDuration)
            self.notify.debug("onscreenDuration=%s" % objType.onscreenDuration)

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
            self.notify.debug("gravity=%s" % g)

            # create a Trajectory object that will be used by all instances of
            # this object type
            objType.trajectory = Trajectory.Trajectory(
                # start time
                0,
                # start pos
                Vec3(0,0,x_0),
                # start vel
                Vec3(0,0,v_0),
                # gravity multiplier
                gravMult = abs(g / Trajectory.Trajectory.gravity))

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
        x = column / float(self.DropColumns-1)
        y = row / float(self.DropRows-1)
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
        self.posts=[
            Toon.Toon(), Toon.Toon(),
            Toon.Toon(), Toon.Toon(),
            ]
        for i in range(len(self.posts)):
            toon=self.posts[i]
            toon.setDNA(base.localAvatar.getStyle())
            toon.reparentTo(render)
            x=self.StageHalfWidth
            y=self.StageHalfHeight
            if i>1:
                 x=-x
            if i%2:
                y=-y
            toon.setPos(x,y,0)

    def hidePosts(self):
        if hasattr(self, 'posts'):
            for toon in self.posts:
                toon.removeNode()
            del self.posts

    def showDropGrid(self):
        """ debugging aid; show the drop grid """
        self.hideDropGrid()
        self.dropMarkers = []
        print "dropRows: %s" % self.DropRows
        print "dropCols: %s" % self.DropColumns
        for row in range(self.DropRows):
            self.dropMarkers.append([])
            rowList = self.dropMarkers[row]
            for column in range(self.DropColumns):
                toon = Toon.Toon()
                toon.setDNA(base.localAvatar.getStyle())
                toon.reparentTo(render)
                toon.setScale(1./3)
                x,y = self.grid2world(column, row)
                toon.setPos(x,y,0)
                rowList.append(toon)

    def hideDropGrid(self):
        if hasattr(self, 'dropMarkers'):
            for row in self.dropMarkers:
                for marker in row:
                    marker.removeNode()
            del self.dropMarkers

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        self.ground.reparentTo(render)

        self.scorePanels = []

        camera.reparentTo(render)
        camera.setPosHpr(*self.CameraPosHpr)

        lt = base.localAvatar
        lt.reparentTo(render)
        self.__placeToon(self.localAvId)
        lt.setSpeed(0,0)

        toonSD = self.toonSDs[self.localAvId]
        toonSD.enter()
        toonSD.fsm.request('normal')
        # disable the local toon's 'input drive' so that the player
        # can't run yet
        self.orthoWalk.stop()

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
        self.ltLegsCollNode.setCollideMask(ToontownGlobals.CatchGameBitmask)
        self.ltHeadCollNode = CollisionNode('catchHeadCollNode')
        self.ltHeadCollNode.setCollideMask(ToontownGlobals.CatchGameBitmask)
        self.ltLHandCollNode = CollisionNode('catchLHandCollNode')
        self.ltLHandCollNode.setCollideMask(ToontownGlobals.CatchGameBitmask)
        self.ltRHandCollNode = CollisionNode('catchRHandCollNode')
        self.ltRHandCollNode.setCollideMask(ToontownGlobals.CatchGameBitmask)
        legsCollNodepath = lt.attachNewNode(self.ltLegsCollNode)
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
        lt.cTrav.addCollider(legsCollNodepath, handler)
        lt.cTrav.addCollider(headCollNodepath, handler)
        lt.cTrav.addCollider(lHandCollNodepath, handler)
        lt.cTrav.addCollider(lHandCollNodepath, handler)
        if self.ShowToonSpheres:
            legsCollNodepath.show()
            headCollNodepath.show()
            lHandCollNodepath.show()
            rHandCollNodepath.show()
        self.ltLegsCollNode.addSolid( CollisionSphere(0,0, radius, radius))
        self.ltHeadCollNode.addSolid( CollisionSphere(0,0,0, radius))
        self.ltLHandCollNode.addSolid( CollisionSphere(0,0,0, 2*radius/3.))
        self.ltRHandCollNode.addSolid( CollisionSphere(0,0,0, 2*radius/3.))
        self.toonCollNodes = [legsCollNodepath,
                              headCollNodepath,
                              lHandCollNodepath,
                              rHandCollNodepath,
                              ]

        #self.showPosts()
        #self.showDropGrid()

        if self.PredictiveSmoothing:
            # Turn on predictive smoothing!
            DistributedSmoothNode.activateSmoothing(1, 1)

        # play the intro movie
        self.introMovie.start()

        """
        this pauses the intro movie at a convenient point for adjusting
        the anvil in the mouse's hand (rightToon)
        def stopRules(self=self):
            self.rulesPanel.timer.stop()
        debugIval = Sequence(
            WaitInterval(2.7932795927973757),
            Func(self.introMovie.pause),
            Func(stopRules),
            )
        debugIval.start()
        """

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...

        # Restore normal non-predictive smoothing.
        DistributedSmoothNode.activateSmoothing(1, 0)

        # make sure the intro movie is finished
        self.introMovie.finish()

        for avId in self.toonSDs.keys():
            self.toonSDs[avId].exit()

        # it's always safe to call these
        self.hidePosts()
        self.hideDropGrid()

        # restore localToon's collision setup
        for collNode in self.toonCollNodes:
            while collNode.node().getNumSolids():
                collNode.node().removeSolid(0)
            base.localAvatar.cTrav.removeCollider(collNode)
        del self.toonCollNodes

        for panel in self.scorePanels:
            panel.cleanup()
        del self.scorePanels

        self.ground.reparentTo(hidden)

        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)

    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears
        self.toonSDs[avId].exit(unexpectedExit = True)
        del self.toonSDs[avId]

        # then call the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def __placeToon(self, avId):
        """ places a toon in its starting position """
        toon = self.getAvatar(avId)
        idx = self.avIdList.index(avId)
        x = lineupPos(idx, self.numPlayers, 4.)
        toon.setPos(x,0,0)
        toon.setHpr(180,0,0)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        
        # Cheezy effects change the ordering of the scene graph
        headCollNP = base.localAvatar.find("**/catchHeadCollNode")
        if headCollNP and not headCollNP.isEmpty():
            headCollNP.hide()

        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)

                # create the toonSD for this toon
                toonSD = CatchGameToonSD.CatchGameToonSD(avId, self)
                self.toonSDs[avId] = toonSD
                toonSD.load()
                toonSD.enter()
                toonSD.fsm.request('normal')

                # Start the smoothing task.
                toon.startSmooth()

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)

        # make sure the intro movie is finished
        self.introMovie.finish()

        # make sure the camera is in the right position
        camera.reparentTo(render)
        camera.setPosHpr(*self.CameraPosHpr)

        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("play")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # allow the local player to move
        self.orthoWalk.start()

        # set up the suit collisions
        for suit in self.suits:
            # Make a sphere, give it a unique name, and parent it
            # to the suit.
            suitCollSphere = CollisionSphere(0, 0, 0, 1.)
            suit.collSphereName = 'suitCollSphere%s' % self.suits.index(suit)
            # Make the sphere intangible
            suitCollSphere.setTangible(0)
            suitCollNode = CollisionNode(self.uniqueName(suit.collSphereName))
            suitCollNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
            suitCollNode.addSolid(suitCollSphere)
            suit.collNodePath = suit.attachNewNode(suitCollNode)
            suit.collNodePath.hide()
            if self.ShowSuitSpheres:
                suit.collNodePath.show()

            # Add a hook looking for collisions with localToon
            self.accept(self.uniqueName('enter' + suit.collSphereName),
                        self.handleSuitCollision)

        # Initialize the scoreboard
        self.scores = [0] * self.numPlayers
        spacing = .4
        for i in xrange(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = \
                       MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId,
                                                                         avName)
            scorePanel.setScale(.9)
            scorePanel.setPos(.75 - spacing*((self.numPlayers-1)-i), 0.0, .85)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels.append(scorePanel)

        # keep a tally of the fruits that are caught so we can figure out if
        # it was a perfect game
        self.fruitsCaught = 0

        # this dict keeps track of which fruits we have shown being eaten;
        # prevents a single fruit from being eaten by multiple toons
        self.droppedObjCaught = {}
        # dict of drop intervals, indexed by obj num
        self.dropIntervals = {}

        # this will hold the names of the objects to be dropped
        self.droppedObjNames = []
        # this will hold a list of drops to perform and when to perform them
        self.dropSchedule = []

        self.numItemsDropped = 0

        # calculate a sequence of drops, using the game's seeded rng
        self.scheduleDrops()
        # start the drop task
        self.startDropTask()

        if self.WantSuits:
            self.startSuitWalkTask()

        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(CatchGameGlobals.GameDuration)
        self.timer.countdown(CatchGameGlobals.GameDuration, self.timerExpired)
        self.timer.setTransparency(1)
        self.timer.setColorScale(1,1,1,.75)

        # Start music
        base.playMusic(self.music, looping = 0, volume = 0.9)

    def exitPlay(self):
        self.stopDropTask()
        self.stopSuitWalkTask()

        if hasattr(self, 'perfectIval'):
            self.perfectIval.pause()
            del self.perfectIval

        self.timer.stop()
        self.timer.destroy()
        del self.timer

        # Stop music
        self.music.stop()

        # tear down suit collisions
        for suit in self.suits:
            self.ignore(self.uniqueName('enter' + suit.collSphereName))
            suit.collNodePath.removeNode()

        # get rid of the drop intervals
        for ival in self.dropIntervals.values():
            ival.finish()
        del self.dropIntervals
        # get rid of list of dropped-objs
        del self.droppedObjNames
        del self.droppedObjCaught

        del self.dropSchedule

        # this may have been added by the last drop interval that was 'finish'ed
        taskMgr.remove(self.EndGameTaskName)

    def timerExpired(self):
        pass

    def __handleCatch(self, objNum):
        self.notify.debug("catch: %s" % objNum)
        # localtoon just caught obj (serial number 'objNum')
        self.showCatch(self.localAvId, objNum)
        # tell the AI we caught this obj
        objName = self.droppedObjNames[objNum]
        objTypeId = CatchGameGlobals.Name2DOTypeId[objName]
        self.sendUpdate('claimCatch', [objNum, objTypeId])
        # make the object disappear
        # NOTE: it is important to do this AFTER sending the claimCatch msg
        # the interval will send a 'reportDone' msg if it's the last item
        self.finishDropInterval(objNum)

    def showCatch(self, avId, objNum):
        """ show the result of the catch action """
        isLocal = (avId == self.localAvId)
        objName = self.droppedObjNames[objNum]
        objType = Name2DropObjectType[objName]
        if objType.good:
            # have we already shown this fruit being eaten?
            if not self.droppedObjCaught.has_key(objNum):
                if isLocal:
                    # TODO (maybe): move this to CatchGameToonSD, move sound
                    # loads to ToonSD
                    base.playSfx(self.sndGoodCatch)

                # make the toon eat the fruit
                fruit = self.getObjModel(objName)
                toon = self.getAvatar(avId)
                rHand = toon.getRightHands()[0]
                self.toonSDs[avId].eatFruit(fruit, rHand)
        else:
            self.toonSDs[avId].fsm.request('fallForward')

        self.droppedObjCaught[objNum] = 1

    def setObjectCaught(self, avId, objNum):
        """ called by the AI to announce a catch """
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.warning('ignoring msg: object %s caught by %s' %
                                (objNum, avId))
            return

        isLocal = (avId == self.localAvId)

        if not isLocal:
            self.notify.debug("AI: avatar %s caught %s" % (avId, objNum))
            # if remote av caught an object, its interval might still
            # be playing. make sure it's finished
            self.finishDropInterval(objNum)
            self.showCatch(avId, objNum)

        # update the toon's score
        objName = self.droppedObjNames[objNum]
        if Name2DropObjectType[objName].good:
            i = self.avIdList.index(avId)
            self.scores[i] += 1
            self.scorePanels[i].setScore(self.scores[i])

            self.fruitsCaught += 1

    def finishDropInterval(self, objNum):
        """ this function ensures that the drop interval for object
        number 'objNum' has finished; if interval already finished,
        does nothing """
        if self.dropIntervals.has_key(objNum):
            self.dropIntervals[objNum].finish()

    def scheduleDrops(self):
        # We give out a 'perfect' bonus for catching all of the fruit.
        # To make the difficulty of catching them all consistent from
        # session to session, we need to hold the number of fruits
        # constant. So, rather than deciding what to drop on-the-fly,
        # based on a probability table, we need something more precise.
        # We need to create a list of drop types, with the correct number
        # of fruits, and randomize that list, thus ensuring that we drop
        # a precise total number of fruits.

        # make a big list of all the drops that should be done
        self.droppedObjNames = ([self.fruitName] * self.numFruits) + \
                               (['anvil'] * self.numAnvils)
        # scramble the list (using the game's RNG so it comes out the
        # same on each client)
        self.randomNumGen.shuffle(self.droppedObjNames)

        # self.droppedObjNames now contains a complete, ordered list
        # of the types of each object that will be dropped

        # create a drop placer, and construct a schedule of drops
        # self.DropPlacerType is actually a DropPlacer constructor
        dropPlacer = self.DropPlacerType(self, self.droppedObjNames)

        while not dropPlacer.doneDropping():
            self.dropSchedule.append(dropPlacer.getNextDrop())

    def startDropTask(self):
        taskMgr.add(self.dropTask, self.DropTaskName)

    def stopDropTask(self):
        taskMgr.remove(self.DropTaskName)

    def dropTask(self, task):
        curT = self.getCurrentGameTime()

        # start all the drops that should already be happening
        # the drop schedule is a time-ordered list of
        # (time, objName, dropRegion) tuples
        while self.dropSchedule[0][0] <= curT:
            drop = self.dropSchedule[0]
            # pop this one off the front
            self.dropSchedule = self.dropSchedule[1:]

            dropTime, objName, dropCoords = drop
            objNum = self.numItemsDropped
            lastDrop = (len(self.dropSchedule) == 0)
            x,y = self.grid2world(*dropCoords)
            
            dropIval = self.getDropIval(x, y, objName, objNum)

            def cleanup(self=self, objNum=objNum, lastDrop=lastDrop):
                del self.dropIntervals[objNum]
                if lastDrop:
                    self.sendUpdate('reportDone')

            dropIval.append(Func(cleanup))

            # add this drop interval to the master table
            self.dropIntervals[objNum] = dropIval
            # and increment the tally of dropped objects
            self.numItemsDropped += 1

            # Interval.start takes # seconds into the interval at which to start
            dropIval.start(curT - dropTime)

            if lastDrop:
                return Task.done

        return Task.cont

    def setEveryoneDone(self):
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.warning('ignoring setEveryoneDone msg')
            return

        self.notify.debug('setEveryoneDone')
        def endGame(task, self=self):
            if not CatchGameGlobals.EndlessGame:
                self.gameOver()
            return Task.done

        self.notify.debug("num fruits: %s" % self.numFruits)
        self.notify.debug("num catches: %s" % self.fruitsCaught)

        # hide the timer
        self.timer.hide()

        # if it was a perfect game, let the players know
        if self.fruitsCaught >= self.numFruits:
            self.notify.debug("perfect game!")

            perfectTextSubnode = hidden.attachNewNode(
                self.__genText(TTLocalizer.CatchGamePerfect))
            perfectText = hidden.attachNewNode('perfectText')
            perfectTextSubnode.reparentTo(perfectText)
            # offset the subnode so that the text is centered on both axes
            # we need the parent node so that the text will scale correctly
            frame = self.__textGen.getCardActual()
            offsetY = -abs(frame[2] + frame[3])/2.
            perfectTextSubnode.setPos(0,0,offsetY)

            perfectText.setColor(1,.1,.1,1)

            def fadeFunc(t, text=perfectText):
                text.setColorScale(1,1,1,t)
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
                Func(endGame, None),
                )
            
            soundTrack = SoundInterval(self.sndPerfect)

            self.perfectIval = Parallel(textTrack,
                                        soundTrack)
            self.perfectIval.start()
        else:
            taskMgr.doMethodLater(1, endGame, self.EndGameTaskName)

    def getDropIval(self, x, y, dropObjName, num):
        """ x, y: -1..1 """
        objType = Name2DropObjectType[dropObjName]

        dropNode = hidden.attachNewNode('catchDropNode%s' % num)
        dropNode.setPos(x, y, 0)
        # must be copy, not instance
        shadow = self.dropShadow.copyTo(dropNode)
        shadow.setZ(.2)
        shadow.setColor(1,1,1,1)
        # must be copy, not instance
        object = self.getObjModel(dropObjName)
        object.reparentTo(dropNode)

        # turn the obj
        if dropObjName in ['watermelon','anvil']:
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
        sphereName = 'FallObj%s' % num
        # x,y,z,radius
        radius = self.ObjRadius
        # make the sphere larger on higher difficulty levels
        if objType.good:
            radius *= lerp(1., 1.3, self.getDifficulty())
        collSphere = CollisionSphere(0,0,0,radius)
        # don't let it push the toons
        collSphere.setTangible(0)
        collNode = CollisionNode(sphereName)
        collNode.setCollideMask(ToontownGlobals.CatchGameBitmask)
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
                            Functor(self.__handleCatch, num)))

        def cleanup(self=self, dropNode=dropNode, num=num,
                    event=catchEventName):
            self.ignore(event)
            dropNode.removeNode()

        duration = objType.fallDuration
        onscreenDuration = objType.onscreenDuration
        dropHeight = self.MinOffscreenHeight

        targetShadowScale = .3
        if self.TrickShadows:
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
                                  duration-self.OffscreenTime,
                                  targetShadowScale,
                                  startScale=intermedScale))
        else:
            shadowScaleIval = LerpScaleInterval(shadow, duration,
                                                targetShadowScale, startScale=0)

        # gradually alpha the shadow in
        targetShadowAlpha = .4
        shadowAlphaIval = LerpColorScaleInterval(
            shadow, self.OffscreenTime, Point4(1,1,1,targetShadowAlpha),
            startColorScale = Point4(1,1,1,0))

        shadowIval = Parallel(
            shadowScaleIval,
            shadowAlphaIval,
            )

        if self.UseGravity:
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
            startPos = Point3(0,0,self.MinOffscreenHeight)
            # put the object at its starting position, which happens to be
            # off-screen
            object.setPos(startPos)
            dropIval = LerpPosInterval(object, onscreenDuration,
                                       Point3(0,0,0), startPos = startPos,
                                       blendType='easeIn')

        ival = Sequence(
            Func(Functor(dropNode.reparentTo, render)),
            Parallel(Sequence(WaitInterval(self.OffscreenTime),
                              dropIval,
                              ),
                     shadowIval,
                     ),
            Func(cleanup),
            name = 'drop%s' % num,
            )

        # conditionally play a 'land' sound
        # note that if the interval is explicitly 'finish'ed,
        # the sound will not play
        landSound = None
        if objType == Name2DropObjectType['anvil']:
            landSound = self.sndAnvilLand
        if landSound:
            ival.append(SoundInterval(landSound))

        return ival

    #### SUIT WALK ######################################################
    def startSuitWalkTask(self):
        """ kicks off the 'task' that makes the suits periodically
        walk across the screen
        suits are not actually controlled by a task, but by one long interval
        """
        # create an interval of suits walking across the stage
        # that's long enough to cover the entire game, and start
        # playing it
        # The interval will be a series of suit walk intervals,
        # with some of the walk intervals potentially overlapping
        # each other in time.
        ival = Parallel(name='catchGameMetaSuitWalk')
        
        # since the suit intervals will be generating random numbers
        # on-the-fly, we need to fork off an rng for the suit ivals
        # to use
        rng = RandomNumGen(self.randomNumGen)

        delay = 0.
        
        # keep adding suit walk ivals until we've reached the length
        # of the game
        while delay < CatchGameGlobals.GameDuration:
            delay += lerp(self.SuitPeriodRange[0], self.SuitPeriodRange[0],
                          rng.random())
            walkIval = Sequence(name='catchGameSuitWalk')
            # add the wait
            walkIval.append(Wait(delay))
            # add a suit walk
            def pickY(self=self, rng=rng):
                #return self.StageHalfHeight
                return lerp(-self.StageHalfHeight, self.StageHalfHeight,
                            rng.random())
            # mult for suit X positions
            m = [2.5,2.5,2.3,2.1][self.getNumPlayers()-1]
            startPos = Point3(-(self.StageHalfWidth*m), pickY(), 0)
            stopPos = Point3((self.StageHalfWidth*m), pickY(), 0)
            # randomly walk from right-to-left or left-to-right
            if rng.choice([0,1]):
                startPos, stopPos = stopPos, startPos
            walkIval.append(self.getSuitWalkIval(startPos, stopPos, rng))
            # add this suit to the overall parallel interval
            ival.append(walkIval)

        ival.start()
        self.suitWalkIval = ival

    def stopSuitWalkTask(self):
        """ shuts down the suit walk system and cleans up """
        self.suitWalkIval.finish()
        del self.suitWalkIval

    def getSuitWalkIval(self, startPos, stopPos, rng):
        """ returns an interval of the game's suit walking from
        startPos to stopPos """
        # shared data repository for setup and cleanup funcs
        data = {}
        # since we won't have the suit until the interval actually
        # runs, we can't create a LerpPosInterval that acts directly
        # on the suit; instead, we create a nodepath, put the suit
        # under that nodepath, and lerp it (instead of the suit).
        lerpNP = render.attachNewNode('catchGameSuitParent')
        
        def setup(self=self, startPos=startPos, stopPos=stopPos,
                  data=data, lerpNP=lerpNP, rng=rng):
            if len(self.suits) == 0:
                # oops, there are no available suits.
                return

            # pick a suit from the list of availables
            suit = rng.choice(self.suits)
            # put a reference in the data dict so that cleanup() can get to it
            data['suit'] = suit
            self.suits.remove(suit)

            suit.reparentTo(lerpNP)
            suit.loop('walk')
            suit.setPlayRate(
                self.SuitSpeed / ToontownGlobals.SuitWalkSpeed, 'walk')
            suit.setPos(0,0,0)
            lerpNP.setPos(startPos)
            suit.lookAt(stopPos)

        def cleanup(self=self, data=data, lerpNP=lerpNP):
            # if there were no available suits when the ival started,
            # there's no suit to clean up
            if data.has_key('suit'):
                suit = data['suit']
                suit.reparentTo(hidden)
                # put the suit back in the available list
                self.suits.append(suit)
            lerpNP.removeNode()

        distance = Vec3(stopPos - startPos).length()
        duration = distance / self.SuitSpeed

        ival = Sequence(
            FunctionInterval(setup),
            LerpPosInterval(lerpNP, duration, stopPos),
            FunctionInterval(cleanup),
            )
        return ival

    def handleSuitCollision(self, collEntry):
        """ called when suit collides with localToon """
        self.toonSDs[self.localAvId].fsm.request('fallBack')
        timestamp = globalClockDelta.localToNetworkTime(\
            globalClock.getFrameTime())
        self.sendUpdate('hitBySuit', [self.localAvId, timestamp])

    def hitBySuit(self, avId, timestamp):
        """ called when remote toon is hit by suit """
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() != 'play':
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return

        # try to see if the avId is valid, return if not
        toon = self.getAvatar(avId)
        if toon == None:
            return
        
        self.notify.debug("avatar %s hit by a suit" % avId)
        if avId != self.localAvId:
            self.toonSDs[avId].fsm.request('fallBack')
    #### END SUIT WALK ##################################################

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    # orthowalk init/shutdown
    def initOrthoWalk(self):
        self.notify.debug("startOrthoWalk")

        def doCollisions(oldPos, newPos, self=self):
            # make the toon collide against the boundaries of the playfield
            x = bound(newPos[0], self.StageHalfWidth, -self.StageHalfWidth)
            y = bound(newPos[1], self.StageHalfHeight, -self.StageHalfHeight)
            newPos.setX(x)
            newPos.setY(y)
            return newPos

        orthoDrive = OrthoDrive(
            self.ToonSpeed,
            customCollisionCallback=doCollisions,
            )
        self.orthoWalk = OrthoWalk(orthoDrive,
                                   broadcast=not self.isSinglePlayer())

    def destroyOrthoWalk(self):
        self.notify.debug("destroyOrthoWalk")

        self.orthoWalk.destroy()
        del self.orthoWalk

    # INTRO MOVIE
    def getIntroMovie(self):
        locNode = self.ground.find("**/locator_tree")
        treeNode = locNode.attachNewNode('treeNode')
        # align the node's axes with render's axes
        treeNode.setHpr(render,0,0,0)

        def cleanupTree(treeNode=treeNode):
            treeNode.removeNode()

        # note that this PosHpr is relative to the treeNode
        # (-X, -Z, -Y)
        #initialCamPosHpr = (-0.37, -15.91, 15.42, 0.00, 26.57, 0.00)
        initialCamPosHpr = (-0.21, -19.56, 13.94, 0.00, 26.57, 0.00)
        suitViewCamPosHpr = (0, -11.5, 13, 0, -35, 0)
        finalCamPosHpr = self.CameraPosHpr
        cameraIval = Sequence(
            Func(camera.reparentTo, render),
            Func(camera.setPosHpr, treeNode, *initialCamPosHpr),
            WaitInterval(4.),
            LerpPosHprInterval(camera, 2.,
                               Point3(*suitViewCamPosHpr[:3]),
                               Point3(*suitViewCamPosHpr[3:]),
                               blendType = 'easeInOut',
                               name = 'lerpToSuitView',
                               ),
            WaitInterval(4.),
            LerpPosHprInterval(camera, 3.,
                               Point3(*finalCamPosHpr[:3]),
                               Point3(*finalCamPosHpr[3:]),
                               blendType = 'easeInOut',
                               name = 'lerpToPlayView',
                               ),
            )

        # create the toons that will throw things from the tree

        def getIntroToon(toonProperties, parent, pos):
            toon = Toon.Toon()
            dna = ToonDNA.ToonDNA()
            dna.newToonFromProperties(*toonProperties)
            toon.setDNA(dna)
            toon.reparentTo(parent)
            toon.setPos(*pos)
            toon.setH(180)
            toon.startBlink()
            return toon

        def cleanupIntroToon(toon):
            toon.detachNode()
            toon.stopBlink()
            toon.delete()

        def getThrowIval(toon, hand, object, leftToon, isAnvil=0):
            anim = 'catch-intro-throw'
            grabFrame = 12
            fullSizeFrame = 30
            framePeriod = 1./toon.getFrameRate(anim)
            objScaleDur = (fullSizeFrame - grabFrame) * framePeriod

            releaseFrame = 35
            trajDuration = 1.6
            trajDistance = 4
            if leftToon:
                releaseFrame = 34
                trajDuration = 1.
                trajDistance = 1

            animIval = ActorInterval(toon, anim, loop=0)

            def getThrowDest(object=object, offset=trajDistance):
                dest = object.getPos(render)
                dest += Point3(0,-offset,0)
                dest.setZ(0)
                return dest

            # the left toon drops the fruit, the right toon tosses
            # the anvil up in the air
            if leftToon:
                trajIval = ProjectileInterval(object,
                                              startVel = Point3(0,0,0),
                                              duration = trajDuration)
            else:
                trajIval = ProjectileInterval(object,
                                              endPos = getThrowDest,
                                              duration = trajDuration)

            trajIval = Sequence(Func(object.wrtReparentTo, render),
                                trajIval,
                                Func(object.wrtReparentTo, hidden),
                                )
            if isAnvil:
                trajIval.append(SoundInterval(self.sndAnvilLand))

            objIval = Track(
                (grabFrame * framePeriod,
                 Sequence(Func(object.reparentTo, hand),
                          Func(object.setPosHpr,
                               .05, -.13, .62, 0, 0, 336.8),
                          LerpScaleInterval(object, objScaleDur, 1.,
                                            startScale=.1,
                                            blendType='easeInOut'))),
                (releaseFrame * framePeriod, trajIval),
                )

            def cleanup(object=object):
                object.reparentTo(hidden)
                object.removeNode()

            throwIval = Sequence(
                Parallel(animIval,
                         objIval,
                         ),
                Func(cleanup),
                )
            return throwIval

        # their positions share identical Y and Z
        tY = -4.
        tZ = 19.5

        # orange cat, MM skirt
        props = ['css', 'md', 'm', 'f', 9, 0, 9, 9, 13, 5, 11, 5, 8, 7]
        leftToon = getIntroToon(props, treeNode, [-2.3, tY, tZ])

        # brown mouse, LL shorts
        props = ['mss', 'ls', 'l', 'm', 6, 0, 6, 6, 3, 5, 3, 5, 5, 0]
        rightToon = getIntroToon(props, treeNode, [1.8, tY, tZ])

        fruit = self.getObjModel(self.fruitName)
        if self.fruitName == 'pineapple':
            fruit.setZ(.42)
            fruit.flattenMedium()

        anvil = self.getObjModel('anvil')
        anvil.setH(100)
        anvil.setZ(.42)
        anvil.flattenMedium()

        """
        leftToonIval = Sequence(
            ActorInterval(leftToon, 'catch-intro-throw', loop=1,
                          duration = cameraIval.getDuration(),
                          startTime = \
                          leftToon.getDuration('catch-intro-throw')/2.),
            )
        rightToonIval = Sequence(
            ActorInterval(rightToon, 'catch-intro-throw', loop=1,
                          duration = cameraIval.getDuration()))
        """

        # it just happens that the left toon's right hand and the right
        # toon's left hand have good coordinate systems
        leftToonIval  = getThrowIval(leftToon,
                                     leftToon.getRightHands()[0],
                                     fruit,
                                     leftToon=1)
        rightToonIval = getThrowIval(rightToon,
                                     rightToon.getLeftHands()[0],
                                     anvil,
                                     leftToon=0,
                                     isAnvil=1)

        animDur = (leftToon.getNumFrames('catch-intro-throw') /
                   leftToon.getFrameRate('catch-intro-throw'))

        toonIval = Sequence(
            Parallel(Sequence(leftToonIval,
                              Func(leftToon.loop, 'neutral'),
                              ),
                     Sequence(Func(rightToon.loop, 'neutral'),
                              WaitInterval(animDur/2.),
                              rightToonIval,
                              Func(rightToon.loop, 'neutral'),
                              ),
                     WaitInterval(cameraIval.getDuration()),
                     ),
            Func(cleanupIntroToon, leftToon),
            Func(cleanupIntroToon, rightToon),
            )

        # keep handles around for debugging
        self.treeNode = treeNode
        self.fruit = fruit
        self.anvil = anvil
        self.leftToon = leftToon
        self.rightToon = rightToon

        introMovie = Sequence(
            Parallel(cameraIval, toonIval),
            Func(cleanupTree),
            )

        return introMovie
