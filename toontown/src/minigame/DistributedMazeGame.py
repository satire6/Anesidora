"""DistributedMazeGame module: contains the DistributedMazeGame class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from DistributedMinigame import *
from MazeSuit import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from OrthoWalk import *
from direct.showbase.PythonUtil import lerp
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
import MazeGameGlobals
import MazeData
import MazeTreasure
import Trajectory
from direct.showbase import RandomNumGen
import MinigameAvatarScorePanel
import MinigameGlobals
from direct.task.Task import Task

class DistributedMazeGame(DistributedMinigame):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMazeGame')
    # define constants that you won't want to tweak here
    CAMERA_TASK = "MazeGameCameraTask"
    UPDATE_SUITS_TASK = "MazeGameUpdateSuitsTask"

    TREASURE_GRAB_EVENT_NAME = "MazeTreasureGrabbed"

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedMazeGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup',
                                             'showScores']),
                                State.State('showScores',
                                            self.enterShowScores,
                                            self.exitShowScores,
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

        # we make the toons look around during the intro movie
        self.usesLookAround = 1

    def getTitle(self):
        return TTLocalizer.MazeGameTitle

    def getInstructions(self):
        return TTLocalizer.MazeGameInstructions

    def getMaxDuration(self):
        return MazeGameGlobals.GAME_DURATION

    def __defineConstants(self):
        self.TOON_SPEED = 8.

        self.TOON_Z = 0

        # actually lower the minimum speed for higher difficulty
        # levels; a really slow suit will get in the way and make
        # it harder to get all the coins
        self.MinSuitSpeedRange = [.8 * self.TOON_SPEED, .6 * self.TOON_SPEED]
        self.MaxSuitSpeedRange = [1.1 * self.TOON_SPEED, 2. * self.TOON_SPEED]

        # set these to true to allocate suit speeds on a curve,
        # where more suits are closer to the median speed and
        # fewer suits are closer to the max and min suit speeds
        self.FASTER_SUIT_CURVE = 1
        # for easier difficulties, there are fewer REALLY slow suits
        self.SLOWER_SUIT_CURVE = (self.getDifficulty() < .5)

        # All of the suits operate entirely independently of the
        # AI server; the server doesn't even really know that they
        # exist. Each suit walks around the maze at a fixed rate,
        # using a seeded random number generator to decide what
        # path to take. Identical seeds are used on all clients.

        # To ensure that the suits on various clients behave
        # exactly the same, it is necessary to avoid the use of
        # floating point numbers in any calculations that affect the
        # paths of the suits. Due to the spatial interactions between
        # suits that can significantly affect their decisions, it is
        # very important that the suits are told to make path decisions
        # in exactly the same order on every client.

        # Therefore, rather than intuitively storing the walking speed
        # of each suit as a feet-per-second floating point number, we
        # store the suits' walk periods, or the number of 'tics' that
        # pass while a suit walks from one position to the next. (Suits
        # only make path decisions when they arrive at new grid positions)
        # We choose an arbitrary number (MazeGameGlobals.SUIT_TIC_FREQ)
        # of 'suit tics' per second. Higher numbers of tics per
        # second give greater suit speed granularity, at the cost of
        # overflowing Python's int range more quickly. For the purposes
        # of a one-minute game, we can choose a fairly high value without
        # worrying about overflow.

        # Each suit is assigned a number of tics that represents the amount
        # of time that it will take that suit to walk from one grid cell
        # to the next grid cell. This is the suit's 'walk period'. If a
        # suit's walk period is the same as MazeGameGlobals.SUIT_TIC_FREQ,
        # that suit will take one second to walk the length of a cell. If
        # the walk period is equal to .5 * SUIT_TIC_FREQ, it will take
        # 1/2 second, etc.

        # compute the suit periods
        if __debug__:
            def printPeriodTable(name, numSuitList, fasterSuits,
                                 tTransFunc=None):
                str = '%s = {\n' % name
                # cycle through the safezones and calculate the
                # corresponding suit speeds
                for zone in MinigameGlobals.SafeZones:
                    str += '%s%s : {' % (' '*4, zone)

                    difficulty = MinigameGlobals.getDifficulty(zone)
                    minSpeed = lerp(self.MinSuitSpeedRange[0],
                                    self.MinSuitSpeedRange[1],
                                    difficulty)
                    maxSpeed = lerp(self.MaxSuitSpeedRange[0],
                                    self.MaxSuitSpeedRange[1],
                                    difficulty)
                    # all the 'slower' suits will be slower than this speed,
                    # all the 'faster' suits will be faster.
                    midSpeed = (minSpeed + maxSpeed) / 2.

                    # cycle through the suit counts (how many suits
                    # will be in play)
                    for numSuits in numSuitList:
                        # there must be an even number of suits
                        assert not numSuits % 2
                        speeds = []
                        for i in xrange(numSuits/2):
                            if fasterSuits:
                                i += numSuits/2
                            t = i / float(numSuits-1)
                            # map t into 0..1
                            if fasterSuits:
                                t -= .5
                            t *= 2.
                            # apply any time transformation function
                            if tTransFunc != None:
                                t = tTransFunc(t)

                            if fasterSuits:
                                speed = lerp(midSpeed, maxSpeed, t)
                            else:
                                speed = lerp(minSpeed, midSpeed, t)
                            speeds.append(speed)

                        # calculate the corresponding suit periods
                        def calcUpdatePeriod(speed):
                            # result in tics
                            # SUIT_TIC_FREQ: tics/sec
                            # CELL_WIDTH: feet
                            # speed: feet/sec
                            # tics = ((tics/sec) * feet) / (feet/sec)
                            return int((float(MazeGameGlobals.SUIT_TIC_FREQ) * \
                                        float(MazeData.CELL_WIDTH)) / speed)

                        periods = map(calcUpdatePeriod, speeds)

                        filler = ""
                        if numSuits < 10:
                            filler = " "

                        str += '%s%s : %s,\n%s%s' % (numSuits, filler, periods,
                                                     ' '*4, ' '*8)
                    str += '},\n'
                str += '%s}' % (' '*4)
                print str

            # these helper functions are used to distort the t time value.
            def rampIntoCurve(t):
                t = 1. - t
                t = t * t * t
                t = 1. - t
                return t
            def rampOutOfCurve(t):
                return t * t * t

            numSuitList = [4,8,12,16]
            printPeriodTable("self.slowerSuitPeriods", numSuitList, 0)
            printPeriodTable("self.slowerSuitPeriodsCurve", numSuitList, 0,
                             rampIntoCurve)
            printPeriodTable("self.fasterSuitPeriods", numSuitList, 1)
            printPeriodTable("self.fasterSuitPeriodsCurve", numSuitList, 1,
                             rampOutOfCurve)

        # these tables were generated from the code above
        # and pasted in
        self.slowerSuitPeriods = {
            2000 : {4  : [128, 76],
                    8  : [128, 99, 81, 68],
                    12 : [128, 108, 93, 82, 74, 67],
                    16 : [128, 112, 101, 91, 83, 76, 71, 66],
                    },
            1000 : {4  : [110, 69],
                    8  : [110, 88, 73, 62],
                    12 : [110, 95, 83, 74, 67, 61],
                    16 : [110, 98, 89, 81, 75, 69, 64, 60],
                    },
            5000 : {4  : [96, 63],
                    8  : [96, 79, 66, 57],
                    12 : [96, 84, 75, 67, 61, 56],
                    16 : [96, 87, 80, 73, 68, 63, 59, 55],
                    },
            4000 : {4  : [86, 58],
                    8  : [86, 71, 61, 53],
                    12 : [86, 76, 68, 62, 56, 52],
                    16 : [86, 78, 72, 67, 62, 58, 54, 51],
                    },
            3000 : {4  : [78, 54],
                    8  : [78, 65, 56, 49],
                    12 : [78, 69, 62, 57, 52, 48],
                    16 : [78, 71, 66, 61, 57, 54, 51, 48],
                    },
            9000 : {4  : [71, 50],
                    8  : [71, 60, 52, 46],
                    12 : [71, 64, 58, 53, 49, 45],
                    16 : [71, 65, 61, 57, 53, 50, 47, 45],
                    },
            }
        self.slowerSuitPeriodsCurve = {
            2000 : {4  : [128, 65],
                    8  : [128, 78, 66, 64],
                    12 : [128, 88, 73, 67, 64, 64],
                    16 : [128, 94, 79, 71, 67, 65, 64, 64],
                    },
            1000 : {4  : [110, 59],
                    8  : [110, 70, 60, 58],
                    12 : [110, 78, 66, 61, 59, 58],
                    16 : [110, 84, 72, 65, 61, 59, 58, 58],
                    },
            5000 : {4  : [96, 55],
                    8  : [96, 64, 56, 54],
                    12 : [96, 71, 61, 56, 54, 54],
                    16 : [96, 76, 65, 59, 56, 55, 54, 54],
                    },
            4000 : {4  : [86, 51],
                    8  : [86, 59, 52, 50],
                    12 : [86, 65, 56, 52, 50, 50],
                    16 : [86, 69, 60, 55, 52, 51, 50, 50],
                    },
            3000 : {4  : [78, 47],
                    8  : [78, 55, 48, 47],
                    12 : [78, 60, 52, 48, 47, 47],
                    16 : [78, 63, 55, 51, 49, 47, 47, 47],
                    },
            9000 : {4  : [71, 44],
                    8  : [71, 51, 45, 44],
                    12 : [71, 55, 48, 45, 44, 44],
                    16 : [71, 58, 51, 48, 45, 44, 44, 44],
                    },
            }
        self.fasterSuitPeriods = {
            2000 : {4  : [54, 42],
                    8  : [59, 52, 47, 42],
                    12 : [61, 56, 52, 48, 45, 42],
                    16 : [61, 58, 54, 51, 49, 46, 44, 42],
                    },
            1000 : {4  : [50, 40],
                    8  : [55, 48, 44, 40],
                    12 : [56, 52, 48, 45, 42, 40],
                    16 : [56, 53, 50, 48, 45, 43, 41, 40],
                    },
            5000 : {4  : [47, 37],
                    8  : [51, 45, 41, 37],
                    12 : [52, 48, 45, 42, 39, 37],
                    16 : [52, 49, 47, 44, 42, 40, 39, 37],
                    },
            4000 : {4  : [44, 35],
                    8  : [47, 42, 38, 35],
                    12 : [48, 45, 42, 39, 37, 35],
                    16 : [49, 46, 44, 42, 40, 38, 37, 35],
                    },
            3000 : {4  : [41, 33],
                    8  : [44, 40, 36, 33],
                    12 : [45, 42, 39, 37, 35, 33],
                    16 : [45, 43, 41, 39, 38, 36, 35, 33],
                    },
            9000 : {4  : [39, 32],
                    8  : [41, 37, 34, 32],
                    12 : [42, 40, 37, 35, 33, 32],
                    16 : [43, 41, 39, 37, 35, 34, 33, 32],
                    },
            }
        self.fasterSuitPeriodsCurve = {
            2000 : {4  : [62, 42],
                    8  : [63, 61, 54, 42],
                    12 : [63, 63, 61, 56, 50, 42],
                    16 : [63, 63, 62, 60, 57, 53, 48, 42],
                    },
            1000 : {4  : [57, 40],
                    8  : [58, 56, 50, 40],
                    12 : [58, 58, 56, 52, 46, 40],
                    16 : [58, 58, 57, 56, 53, 49, 45, 40],
                    },
            5000 : {4  : [53, 37],
                    8  : [54, 52, 46, 37],
                    12 : [54, 53, 52, 48, 43, 37],
                    16 : [54, 54, 53, 51, 49, 46, 42, 37],
                    },
            4000 : {4  : [49, 35],
                    8  : [50, 48, 43, 35],
                    12 : [50, 49, 48, 45, 41, 35],
                    16 : [50, 50, 49, 48, 46, 43, 39, 35],
                    },
            3000 : {4  : [46, 33],
                    8  : [47, 45, 41, 33],
                    12 : [47, 46, 45, 42, 38, 33],
                    16 : [47, 46, 46, 45, 43, 40, 37, 33],
                    },
            9000 : {4  : [43, 32],
                    8  : [44, 42, 38, 32],
                    12 : [44, 43, 42, 40, 36, 32],
                    16 : [44, 44, 43, 42, 40, 38, 35, 32],
                    },
            }

        self.CELL_WIDTH = MazeData.CELL_WIDTH
        self.MAX_FRAME_MOVE = self.CELL_WIDTH/2 # maximum movement in one frame

        startOffset = 3
        self.startPosHTable = [
            [Point3(0, startOffset,self.TOON_Z),  0],
            [Point3(0,-startOffset,self.TOON_Z),180],
            [Point3( startOffset,0,self.TOON_Z),270],
            [Point3(-startOffset,0,self.TOON_Z), 90],
            ]

        self.camOffset = Vec3(0, -19, 45)

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here

        self.__defineConstants()

        mazeName = MazeGameGlobals.getMazeName(self.doId, self.numPlayers,
                                               MazeData.mazeNames)
        self.maze = Maze.Maze(mazeName)

        model = loader.loadModel("phase_3.5/models/props/mickeySZ")
        self.treasureModel = model.find("**/mickeySZ")
        model.removeNode()
        self.treasureModel.setScale(1.6)
        #self.treasureModel.setP(-80) # tilt the mickey heads toward the camera
        self.treasureModel.setP(-90)

        self.music = base.loadMusic(
            "phase_4/audio/bgm/MG_toontag.mid"
            #"phase_4/audio/bgm/TC_SZ.mid"
            )

        # make a dictionary of tracks for showing each toon
        # getting hit by a suit
        self.toonHitTracks = {}

        self.scorePanels = []

        if __debug__:
            # this flag will allow you to walk right through suits
            self.cheat = config.GetBool('maze-game-cheat', 0)

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here

        del self.toonHitTracks

        self.maze.destroy()
        del self.maze

        self.treasureModel.removeNode()
        del self.treasureModel

        del self.music
        
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)

        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        self.maze.onstage()

        # place the toons in random starting lineups by
        # shuffling the starting position list
        self.randomNumGen.shuffle(self.startPosHTable)

        lt = base.localAvatar
        lt.reparentTo(render)
        lt.hideName()
        self.__placeToon(self.localAvId)
        lt.setAnimState('Happy', 1.0)
        lt.setSpeed(0,0)

        self.camParent = render.attachNewNode('mazeGameCamParent')
        self.camParent.reparentTo(base.localAvatar)
        self.camParent.setPos(0,0,0)
        self.camParent.setHpr(render, 0,0,0)
        camera.reparentTo(self.camParent)
        camera.setPos(self.camOffset)

        self.__spawnCameraTask()

        # create random num generators for each toon
        self.toonRNGs = []
        for i in xrange(self.numPlayers):
            self.toonRNGs.append(RandomNumGen.RandomNumGen(self.randomNumGen))

        # create the treasures
        self.treasures = []
        for i in xrange(self.maze.numTreasures):
            self.treasures.append(MazeTreasure.MazeTreasure(
                self.treasureModel, self.maze.treasurePosList[i], i, self.doId))

        self.__loadSuits()
        for suit in self.suits:
            suit.onstage()

        # create an instance of each sound so that they can be
        # played simultaneously, one for each toon
        # these sounds must be loaded here (and not in load()) because
        # we don't know how many players there will be until the
        # minigame has recieved all required fields
        self.sndTable = {
            "hitBySuit" : [None] * self.numPlayers,
            "falling"   : [None] * self.numPlayers,
            }
        for i in xrange(self.numPlayers):
            self.sndTable["hitBySuit"][i] =  base.loadSfx(
                "phase_4/audio/sfx/MG_Tag_C.mp3"
                #"phase_4/audio/sfx/MG_cannon_fire_alt.mp3"
                )
            self.sndTable["falling"][i] = base.loadSfx(
                "phase_4/audio/sfx/MG_cannon_whizz.mp3")

        # load a few copies of the grab sound
        self.grabSounds = []
        for i in xrange(5):
            self.grabSounds.append(base.loadSfx(
                "phase_4/audio/sfx/MG_maze_pickup.mp3"
                ))
        # play the sounds round-robin
        self.grabSoundIndex = 0

        # fill in the toonHitTracks dict with bogus tracks
        for avId in self.avIdList:
            self.toonHitTracks[avId] = Wait(0.1)

        self.scores = [0] * self.numPlayers

        # this will show what percentage of the treasures
        # have been picked up
        self.goalBar = DirectWaitBar(
            parent = render2d,
            relief = DGG.SUNKEN,
            frameSize = (-0.35, 0.35, -0.15, 0.15),
            borderWidth = (0.02, 0.02),
            scale = 0.42,
            pos = (.84, 0, (0.5 - .28*self.numPlayers) + .05),
            barColor = (0, 0.7, 0, 1),
            )
        self.goalBar.setBin('unsorted', 0)
        self.goalBar.hide()

        self.introTrack = self.getIntroTrack()
        self.introTrack.start()

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...

        if self.introTrack.isPlaying():
            self.introTrack.finish()
        del self.introTrack

        for avId in self.toonHitTracks.keys():
            track = self.toonHitTracks[avId]
            if track.isPlaying():
                track.finish()

        self.__killCameraTask()

        camera.wrtReparentTo(render)
        self.camParent.removeNode()
        del self.camParent

        for panel in self.scorePanels:
            panel.cleanup()
        self.scorePanels = []

        self.goalBar.destroy()
        del self.goalBar

        # Restore the offscreen popups.
        base.setCellsAvailable(base.rightCells, 1)

        for suit in self.suits:
            suit.offstage()
        self.__unloadSuits()

        for treasure in self.treasures:
            treasure.destroy()
        del self.treasures

        del self.sndTable
        del self.grabSounds

        del self.toonRNGs

        self.maze.offstage()
        
        base.localAvatar.showName()

        # this parents toons to hidden, so do it last
        # just to be sure
        DistributedMinigame.offstage(self)

    def __placeToon(self, avId):
        """ places a toon in its starting position """
        toon = self.getAvatar(avId)
        if self.numPlayers == 1:
            toon.setPos(0,0,self.TOON_Z)
            toon.setHpr(180,0,0)
        else:
            posIndex = self.avIdList.index(avId)
            toon.setPos(self.startPosHTable[posIndex][0])
            toon.setHpr(self.startPosHTable[posIndex][1],0,0)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        
        # all of the remote toons have joined the game;
        # it's safe to show them now.

        # show the remote toons
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)
                toon.setAnimState('Happy', 1.0)
                # Start the smoothing task.
                toon.startSmooth()
                toon.startLookAround()

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        if self.introTrack.isPlaying():
            self.introTrack.finish()

        # make the remote toons stop looking around
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.stopLookAround()

        # transition to the appropriate state
        self.gameFSM.request("play")

    def handleDisabledAvatar(self, avId):
        # yikes, this avatar is about to disappear
        # if it's playing, finish up his fly interval before it's too late
        hitTrack = self.toonHitTracks[avId]
        if hitTrack.isPlaying():
            hitTrack.finish()

        # hand it off to the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # Initialize the scoreboard
        for i in xrange(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = \
                       MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId,
                                                                         avName)
            scorePanel.setPos(1.12, 0.0, .5 - 0.28*i)
            self.scorePanels.append(scorePanel)

        self.goalBar.show()
        self.goalBar['value'] = 0.

        # We need the right edge of the screen for display of the
        # scoreboard, so we can't have any offscreen popups there.
        base.setCellsAvailable(base.rightCells, 0)

        self.__spawnUpdateSuitsTask()

        orthoDrive = OrthoDrive(
            self.TOON_SPEED,
            maxFrameMove=self.MAX_FRAME_MOVE,
            customCollisionCallback=self.__doMazeCollisions,
            priority = 1
            )
        self.orthoWalk = OrthoWalk(orthoDrive,
                                   broadcast=not self.isSinglePlayer())
        self.orthoWalk.start()

        # listen for collisions with the suits
        self.accept(MazeSuit.COLLISION_EVENT_NAME, self.__hitBySuit)

        # listen for treasure pickups
        self.accept(self.TREASURE_GRAB_EVENT_NAME, self.__treasureGrabbed)

        # Start counting down the game clock,
        # call timerExpired when it reaches 0
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(MazeGameGlobals.GAME_DURATION)
        self.timer.countdown(MazeGameGlobals.GAME_DURATION, self.timerExpired)

        # listen for resetClock messages so we can keep our clock in sync
        self.accept("resetClock", self.__resetClock)

        base.playMusic(self.music, looping = 0, volume = .8)

    def exitPlay(self):
        self.notify.debug("exitPlay")
        self.ignore("resetClock")

        self.ignore(MazeSuit.COLLISION_EVENT_NAME)
        self.ignore(self.TREASURE_GRAB_EVENT_NAME)

        self.orthoWalk.stop()
        self.orthoWalk.destroy()
        del self.orthoWalk

        self.__killUpdateSuitsTask()

        self.timer.stop()
        self.timer.destroy()
        del self.timer

        # keep the toons from walking in place
        for avId in self.avIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.loop('neutral')

    def __resetClock(self, tOffset):
        self.notify.debug("resetClock")
        self.gameStartTime += tOffset
        self.timer.countdown(self.timer.currentTime + tOffset,
                             self.timerExpired)

    def __treasureGrabbed(self, treasureNum):
        # local toon grabbed this treasure
        # another toon may actually get the credit,
        # but proceed as if we got it

        # make the treasure react
        self.treasures[treasureNum].showGrab()
        # play a sound
        self.grabSounds[self.grabSoundIndex].play()
        self.grabSoundIndex = (self.grabSoundIndex + 1) % len(self.grabSounds)
        # tell the AI we're claiming this treasure
        self.sendUpdate("claimTreasure", [treasureNum])

    def setTreasureGrabbed(self, avId, treasureNum):
        if not self.hasLocalToon: return
        #self.notify.debug("treasure %s grabbed by %s" % (treasureNum, avId))

        if avId != self.localAvId:
            # destroy the treasure
            self.treasures[treasureNum].showGrab()

        # update the toon's score
        i = self.avIdList.index(avId)
        self.scores[i] += 1
        self.scorePanels[i].setScore(self.scores[i])

        # update the total treasure percentage
        total = 0
        for score in self.scores:
            total += score
        self.goalBar['value'] = 100. * \
                                (float(total) / float(self.maze.numTreasures))

    def __hitBySuit(self, suitNum):
        # localtoon was hit by a suit
        self.notify.debug("hitBySuit")
        if __debug__:
            if self.cheat:
                return
        timestamp = globalClockDelta.localToNetworkTime(\
            globalClock.getFrameTime())
        self.sendUpdate("hitBySuit", [self.localAvId, timestamp])
        self.__showToonHitBySuit(self.localAvId, timestamp)

    def hitBySuit(self, avId, timestamp):
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() not in [
            'play', 'showScores']:
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return
        self.notify.debug("avatar " + `avId` + " hit by a suit")
        if avId != self.localAvId:
            self.__showToonHitBySuit(avId, timestamp)
        
    def __showToonHitBySuit(self, avId, timestamp):
        toon = self.getAvatar(avId)
        if toon == None:
            return
        rng = self.toonRNGs[self.avIdList.index(avId)]

        # make sure this toon's old track is done
        curPos = toon.getPos(render)
        oldTrack = self.toonHitTracks[avId]
        if oldTrack.isPlaying():
            oldTrack.finish()
        # preserve the toon's current position, in case he gets hit
        # by two suits at a time
        toon.setPos(curPos)
        toon.setZ(self.TOON_Z)

        # put the toon under a new node
        assert (toon.getParent() == render)
        parentNode = render.attachNewNode('mazeFlyToonParent-'+`avId`)
        parentNode.setPos(toon.getPos())
        toon.reparentTo(parentNode)
        toon.setPos(0,0,0)

        # shoot the toon up into the air
        startPos = parentNode.getPos()

        # make a copy of the toon's dropshadow
        dropShadow = toon.dropShadow.copyTo(parentNode)
        dropShadow.setScale(toon.dropShadow.getScale(render))
        
        trajectory = Trajectory.Trajectory(0,
                                           Point3(0,0,0),
                                           Point3(0,0,50),
                                           gravMult=1.)
        flyDur = trajectory.calcTimeOfImpactOnPlane(0.)
        assert(flyDur > 0)

        # choose a random landing point
        while 1:
            endTile = [rng.randint(2,self.maze.width-1),
                       rng.randint(2,self.maze.height-1)]
            if self.maze.isWalkable(endTile[0],endTile[1]):
                break

        endWorldCoords = self.maze.tile2world(endTile[0],endTile[1])
        endPos = Point3(endWorldCoords[0], endWorldCoords[1], startPos[2])

        def flyFunc(t, trajectory, startPos=startPos, endPos=endPos,
                    dur=flyDur, moveNode=parentNode, flyNode=toon):
            u = (t/dur)
            moveNode.setX(startPos[0] + (u * (endPos[0]-startPos[0])))
            moveNode.setY(startPos[1] + (u * (endPos[1]-startPos[1])))
            # set the full position, since the toon might get banged
            # by telemetry
            flyNode.setPos(trajectory.getPos(t))

        flyTrack = Sequence(
            LerpFunctionInterval(flyFunc,
                                 fromData=0., toData=flyDur,
                                 duration=flyDur,
                                 extraArgs=[trajectory]),
            name=toon.uniqueName("hitBySuit-fly"))

        # if localtoon, move the camera to get a better view
        if avId != self.localAvId:
            cameraTrack = Sequence()
        else:
            # keep the camera parent node on the ground
            # with the toon parent node
            self.camParent.reparentTo(parentNode)
            startCamPos = camera.getPos()

            destCamPos = camera.getPos()
            # trajectory starts at Z==0, ends at Z==0
            zenith = trajectory.getPos(flyDur/2.)[2]
            # make the camera go up above the toon's zenith...
            destCamPos.setZ(zenith * 1.3)
            # and pull in fairly far towards the toon
            destCamPos.setY(destCamPos[1] * .3)

            # make sure the camera keeps looking at the toon
            def camTask(task, zenith=zenith,
                              flyNode=toon,
                              startCamPos=startCamPos,
                              camOffset=destCamPos-startCamPos):
                # move the camera proportional to the current height
                # of the toon wrt the height of its total trajectory
                u = flyNode.getZ() / zenith
                camera.setPos(startCamPos + (camOffset * u))
                camera.lookAt(toon)
                return Task.cont

            camTaskName = "mazeToonFlyCam-"+`avId`
            taskMgr.add(camTask, camTaskName, priority=20)

            def cleanupCamTask(self=self, toon=toon,
                               camTaskName=camTaskName,
                               startCamPos=startCamPos):
                taskMgr.remove(camTaskName)
                self.camParent.reparentTo(toon)
                camera.setPos(startCamPos)
                camera.lookAt(toon)

            cameraTrack = Sequence(
                Wait(flyDur),
                Func(cleanupCamTask),
                name="hitBySuit-cameraLerp")

        # make the toon spin in H and P
        # it seems like we need to put the rotations on two different
        # nodes in order to avoid interactions between the rotations
        geomNode = toon.getGeomNode()
        
        # apply the H rotation around the geomNode, since it's OK
        # to spin the toon in H at a node at his feet
        startHpr = geomNode.getHpr()
        destHpr = Point3(startHpr)
        # make the toon rotate in h 1..7 times
        hRot = rng.randrange(1,8)
        if rng.choice([0,1]):
            hRot = -hRot
        destHpr.setX(destHpr[0]+(hRot*360))
        spinHTrack = Sequence(
            LerpHprInterval(geomNode, flyDur, destHpr, startHpr=startHpr),
            Func(geomNode.setHpr, startHpr),
            name=toon.uniqueName("hitBySuit-spinH"))
        
        # put an extra node above the geomNode, so we can spin the
        # toon in P around his waist
        parent = geomNode.getParent()
        rotNode = parent.attachNewNode('rotNode')
        geomNode.reparentTo(rotNode)
        rotNode.setZ(toon.getHeight()/2.)
        oldGeomNodeZ = geomNode.getZ()
        geomNode.setZ(-toon.getHeight()/2.)

        # spin the toon in P around his waist
        startHpr = rotNode.getHpr()
        destHpr = Point3(startHpr)
        # make the toon rotate in P 1..2 times
        pRot = rng.randrange(1,3)
        if rng.choice([0,1]):
            pRot = -pRot
        destHpr.setY(destHpr[1]+(pRot*360))
        spinPTrack = Sequence(
            LerpHprInterval(rotNode, flyDur, destHpr, startHpr=startHpr),
            Func(rotNode.setHpr, startHpr),
            name=toon.uniqueName("hitBySuit-spinP"))

        # play some sounds
        i = self.avIdList.index(avId)
        soundTrack = Sequence(
            Func(base.playSfx, self.sndTable['hitBySuit'][i]),
            Wait(flyDur * (2./3.)),
            SoundInterval(self.sndTable['falling'][i],
                          duration=(flyDur*(1./3.))),
            name=toon.uniqueName("hitBySuit-soundTrack"))

        def preFunc(self=self, avId=avId, toon=toon, dropShadow=dropShadow):
            forwardSpeed = toon.forwardSpeed
            rotateSpeed = toon.rotateSpeed

            if avId == self.localAvId:
                # disable control of local toon
                self.orthoWalk.stop()
            else:
                toon.stopSmooth()
            
            # preserve old bug/feature where toon would be running in the air
            # if toon was moving, make him continue to run
            if forwardSpeed or rotateSpeed:
                toon.setSpeed(forwardSpeed, rotateSpeed)

            # set toon's speed to zero to stop any walk animations
            # leave it, it's funny to see toon running in mid-air
            #toon.setSpeed(0,0)

            # hide the toon's dropshadow
            toon.dropShadow.hide()

        def postFunc(self=self, avId=avId, oldGeomNodeZ=oldGeomNodeZ,
                     dropShadow=dropShadow, parentNode=parentNode):
            if avId == self.localAvId:
                base.localAvatar.setPos(endPos)
                # game may have ended by now, check
                if hasattr(self, 'orthoWalk'):
                    # re-enable control of local toon only if we're still in the play state.
                    if (self.gameFSM.getCurrentState().getName() == "play"):
                        self.orthoWalk.start()

            # get rid of the dropshadow
            dropShadow.removeNode()
            del dropShadow

            # show the toon's dropshadow
            toon.dropShadow.show()

            # get rid of the extra nodes
            geomNode = toon.getGeomNode()
            rotNode = geomNode.getParent()
            baseNode = rotNode.getParent()
            geomNode.reparentTo(baseNode)
            rotNode.removeNode()
            del rotNode
            geomNode.setZ(oldGeomNodeZ)

            toon.reparentTo(render)
            toon.setPos(endPos)
            parentNode.removeNode()
            del parentNode

            if avId != self.localAvId:
                toon.startSmooth()

        # call the preFunc _this_frame_ to ensure that the local toon
        # update task does not run this frame
        preFunc()

        hitTrack = Sequence(
            Parallel(flyTrack, cameraTrack,
                     spinHTrack, spinPTrack, soundTrack),
            Func(postFunc),
            name=toon.uniqueName("hitBySuit"))

        self.toonHitTracks[avId] = hitTrack
        hitTrack.start(globalClockDelta.localElapsedTime(timestamp))
        
    def allTreasuresTaken(self):
        if not self.hasLocalToon: return
        # all of the treasures are gone, move on
        self.notify.debug("all treasures taken")
        if not MazeGameGlobals.ENDLESS_GAME:
            self.gameFSM.request('showScores')

    def timerExpired(self):
        self.notify.debug("local timer expired")
        if not MazeGameGlobals.ENDLESS_GAME:
            self.gameFSM.request('showScores')

    def __doMazeCollisions(self, oldPos, newPos):
        # we will calculate an offset vector that
        # keeps the toon out of the walls
        offset = newPos - oldPos

        # toons can only get this close to walls
        WALL_OFFSET = 1.

        # make sure we're not in a wall already
        curX = oldPos[0]; curY = oldPos[1]
        curTX, curTY = self.maze.world2tile(curX, curY)
        assert(not self.maze.collisionTable[curTY][curTX])

        def calcFlushCoord(curTile, newTile, centerTile):
            # calculates resulting one-dimensional coordinate,
            # given that the object is moving from curTile to
            # newTile, where newTile is a wall
            EPSILON = 0.01
            if newTile > curTile:
                return ((newTile-centerTile)*self.CELL_WIDTH)\
                       -EPSILON-WALL_OFFSET
            else:
                return ((curTile-centerTile)*self.CELL_WIDTH)+WALL_OFFSET

        offsetX = offset[0]; offsetY = offset[1]

        WALL_OFFSET_X = WALL_OFFSET
        if offsetX < 0:
            WALL_OFFSET_X = -WALL_OFFSET_X
        WALL_OFFSET_Y = WALL_OFFSET
        if offsetY < 0:
            WALL_OFFSET_Y = -WALL_OFFSET_Y

        # check movement in X direction
        newX = curX + offsetX + WALL_OFFSET_X; newY = curY
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTX != curTX:
            # we've crossed a tile boundary
            if self.maze.collisionTable[newTY][newTX]:
                # there's a wall
                # adjust the X offset so that the toon
                # hits the wall exactly
                offset.setX(calcFlushCoord(curTX, newTX,
                                           self.maze.originTX)-curX)

        newX = curX; newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if newTY != curTY:
            # we've crossed a tile boundary
            if self.maze.collisionTable[newTY][newTX]:
                # there's a wall
                # adjust the Y offset so that the toon
                # hits the wall exactly
                offset.setY(calcFlushCoord(curTY, newTY,
                                           self.maze.originTY)-curY)

        # at this point, if our new position is in a wall, we're
        # running right into a protruding corner:
        #
        #  \
        #   ###
        #   ###
        #   ###
        #
        offsetX = offset[0]; offsetY = offset[1]

        newX = curX + offsetX + WALL_OFFSET_X
        newY = curY + offsetY + WALL_OFFSET_Y
        newTX, newTY = self.maze.world2tile(newX, newY)
        if self.maze.collisionTable[newTY][newTX]:
            # collide in only one of the dimensions
            cX = calcFlushCoord(curTX, newTX, self.maze.originTX)
            cY = calcFlushCoord(curTY, newTY, self.maze.originTY)
            if (abs(cX - curX) < abs(cY - curY)):
                offset.setX(cX - curX)
            else:
                offset.setY(cY - curY)

        return oldPos + offset

    def __spawnCameraTask(self):
        self.notify.debug("spawnCameraTask")

        camera.lookAt(base.localAvatar)

        taskMgr.remove(self.CAMERA_TASK)
        # The camera control needs to run after the toon collision/movement processing
        taskMgr.add(self.__cameraTask, self.CAMERA_TASK, priority=45)

    def __killCameraTask(self):
        self.notify.debug("killCameraTask")
        taskMgr.remove(self.CAMERA_TASK)

    def __cameraTask(self, task):
        # simulate a compass node; always make sure the camera
        # parent node is rotated correctly, regardless of the
        # orientation of the parent (localtoon)
        self.camParent.setHpr(render, 0,0,0)
        return Task.cont

    ## SUITS
    def __loadSuits(self):
        self.notify.debug("loadSuits")
        self.suits = []
        self.numSuits = 4 * self.numPlayers

        safeZone = self.getSafezoneId()

        slowerTable = self.slowerSuitPeriods
        if self.SLOWER_SUIT_CURVE:
            slowerTable = self.slowerSuitPeriodsCurve
        slowerPeriods = slowerTable[safeZone][self.numSuits]

        fasterTable = self.fasterSuitPeriods
        if self.FASTER_SUIT_CURVE:
            fasterTable = self.fasterSuitPeriodsCurve
        fasterPeriods = fasterTable[safeZone][self.numSuits]

        suitPeriods = slowerPeriods + fasterPeriods
        self.notify.debug("suit periods: " + `suitPeriods`)

        self.randomNumGen.shuffle(suitPeriods)
        
        for i in xrange(self.numSuits):
            self.suits.append(MazeSuit(i, self.maze, self.randomNumGen,
                                       suitPeriods[i], self.getDifficulty()))

    def __unloadSuits(self):
        self.notify.debug("unloadSuits")
        for suit in self.suits:
            suit.destroy()
        del self.suits

    def __spawnUpdateSuitsTask(self):
        self.notify.debug("spawnUpdateSuitsTask")
        for suit in self.suits:
            suit.gameStart(self.gameStartTime)

        taskMgr.remove(self.UPDATE_SUITS_TASK)
        taskMgr.add(self.__updateSuitsTask, self.UPDATE_SUITS_TASK)

    def __killUpdateSuitsTask(self):
        self.notify.debug("killUpdateSuitsTask")
        taskMgr.remove(self.UPDATE_SUITS_TASK)

        for suit in self.suits:
            suit.gameEnd()

    def __updateSuitsTask(self, task):
        #print "__updateSuitsTask"
        
        curT = globalClock.getFrameTime() - self.gameStartTime
        curTic = int(curT * float(MazeGameGlobals.SUIT_TIC_FREQ))

        # this list will hold a sorted list of (tic, suit index) pairs
        # that represent the suit updates that must be executed
        # this frame
        suitUpdates = []

        # aggregate a list of all the suit update times
        for i in xrange(len(self.suits)):
            updateTics = self.suits[i].getThinkTimestampTics(curTic)
            suitUpdates.extend(zip(updateTics, [i]*len(updateTics)))
        # sort the list in-place
        suitUpdates.sort(lambda a,b: a[0]-b[0])

        if len(suitUpdates) > 0:
            # see below
            curTic = 0

            # run through the sorted update list, and execute the updates
            for i in xrange(len(suitUpdates)):
                update = suitUpdates[i]
                tic = update[0]
                suitIndex = update[1]
                suit = self.suits[suitIndex]

                # if multiple suits are scheduled to update at exactly the
                # same time, call prepareToMove() on them, to prevent
                # collisions between a suit and another suit's
                # old (about to be changed) position
                if tic > curTic:
                    curTic = tic
                    j = i + 1
                    while j < len(suitUpdates):
                        if suitUpdates[j][0] > tic:
                            break
                        self.suits[suitUpdates[j][1]].prepareToThink()
                        j += 1

                # make list of tiles where this suit may not walk
                # (because other suits are already there)
                unwalkables = []
                for si in xrange(suitIndex):
                    unwalkables.extend(self.suits[si].occupiedTiles)
                for si in xrange(suitIndex+1,len(self.suits)):
                    unwalkables.extend(self.suits[si].occupiedTiles)

                # do the actual update
                suit.think(curTic, curT, unwalkables)

        return Task.cont

    def enterShowScores(self):
        self.notify.debug("enterShowScores")

        # lerp up the goal bar, score panels
        lerpTrack = Parallel()
        lerpDur = .5
        # goal panel
        lerpTrack.append(Parallel(
            LerpPosInterval(self.goalBar, lerpDur, Point3(0,0,-.6),
                            blendType='easeInOut'),
            LerpScaleInterval(self.goalBar, lerpDur,
                              Vec3(self.goalBar.getScale())*2.,
                              blendType='easeInOut'),
            ))
        # score panels
        # top/bottom Y
        tY = .6; bY = -.05
        # left/center/right X
        lX = -.5; cX = 0; rX = .5
        scorePanelLocs = (
            ((cX,bY),),
            ((lX,bY),(rX,bY)),
            ((cX,tY),(lX,bY),(rX,bY)),
            ((lX,tY),(rX,tY),(lX,bY),(rX,bY)),
            )
        scorePanelLocs = scorePanelLocs[self.numPlayers-1]
        for i in xrange(self.numPlayers):
            panel = self.scorePanels[i]
            pos = scorePanelLocs[i]
            lerpTrack.append(Parallel(
                LerpPosInterval(panel, lerpDur, Point3(pos[0],0,pos[1]),
                                blendType='easeInOut'),
                LerpScaleInterval(panel, lerpDur,
                                  Vec3(panel.getScale())*2.,
                                  blendType='easeInOut'),
                ))

        self.showScoreTrack = Parallel(
            lerpTrack,
            Sequence(Wait(MazeGameGlobals.SHOWSCORES_DURATION),
                     Func(self.gameOver),
                     ),
            )

        self.showScoreTrack.start()

    def exitShowScores(self):
        # calling finish() here would cause problems if we're
        # exiting abnormally, because of the gameOver() call
        self.showScoreTrack.pause()
        del self.showScoreTrack

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        # play and showScores are currently self-contained enough
        # to clean themselves up in their exit() funcs

    def exitCleanup(self):
        pass

    def getIntroTrack(self):
        # show a close-up of the toon, and pull back to the final
        # camera position

        # pump the camera task to make sure the camera parent is
        # rotated correctly
        self.__cameraTask(None)

        # store the camera's original parent/pos/hpr
        origCamParent = camera.getParent()
        origCamPos = camera.getPos()
        origCamHpr = camera.getHpr()

        # put a node under the toon, and put the camera under that node
        iCamParent = base.localAvatar.attachNewNode('iCamParent')
        # In the final camera position that is used during the game,
        # a toon with a heading of 0 will be facing away from the camera.
        # We want to start out facing the toon, and smoothly transition to
        # the final camera pos. Therefore, we should give the camera parent
        # node a 180-degree rotation.
        iCamParent.setH(180)

        camera.reparentTo(iCamParent)
        toonHeight = base.localAvatar.getHeight()
        camera.setPos(0, -15, toonHeight * 3)
        camera.lookAt(0, 0, toonHeight/2.)

        # put the new parent node under the original parent node
        # so that all we have to do to make the new parent node
        # coincide with the old parent node is lerp the new parent's
        # pos/hpr to zero
        iCamParent.wrtReparentTo(origCamParent)

        waitDur = 5.
        lerpDur = 4.5

        lerpTrack = Parallel()
        # lerp the camera parent to where the old parent is
        # make sure that we don't lerp more than 180 degrees
        # we're lerping to H=0, so make sure -180 <= startH <= 180
        startHpr = iCamParent.getHpr()
        startHpr.setX(reduceAngle(startHpr[0]))
        lerpTrack.append(
            LerpPosHprInterval(iCamParent, lerpDur,
                               pos = Point3(0,0,0),
                               hpr = Point3(0,0,0),
                               startHpr = startHpr,
                               name=self.uniqueName('introLerpParent')))

        # lerp the camera to its old offset/orientation
        lerpTrack.append(
            LerpPosHprInterval(camera, lerpDur,
                               pos = origCamPos,
                               hpr = origCamHpr,
                               blendType = 'easeInOut',
                               name=self.uniqueName('introLerpCameraPos')))

        base.localAvatar.startLookAround()

        def cleanup(origCamParent=origCamParent,
                    origCamPos=origCamPos,
                    origCamHpr=origCamHpr,
                    iCamParent=iCamParent):
            camera.reparentTo(origCamParent)
            camera.setPos(origCamPos)
            camera.setHpr(origCamHpr)
            iCamParent.removeNode()
            del iCamParent
            base.localAvatar.stopLookAround()
            
        return Sequence(
            Wait(waitDur),
            lerpTrack,
            Func(cleanup),
            )
