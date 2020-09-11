"""DistributedCogThiefGame module: contains the DistributedCogThiefGame class"""

from pandac.PandaModules import Point3, CollisionSphere, CollisionNode, \
     CollisionHandlerEvent, NodePath, TextNode
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import Wait, LerpFunctionInterval, \
     LerpHprInterval, Sequence, Parallel, Func, SoundInterval, ActorInterval, \
     ProjectileInterval, Track, LerpScaleInterval, WaitInterval, \
     LerpPosHprInterval
from direct.gui.DirectGui import DirectLabel
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase import RandomNumGen
from direct.task import Task
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownTimer
from toontown.minigame import CogThiefGameToonSD
from toontown.minigame.OrthoDrive import OrthoDrive
from toontown.minigame.OrthoWalk import OrthoWalk
from toontown.minigame import CogThiefGameGlobals
from toontown.minigame import CogThief
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame import Trajectory
from toontown.minigame import MinigameGlobals
from toontown.minigame import CogThiefWalk

CTGG = CogThiefGameGlobals
class DistributedCogThiefGame(DistributedMinigame):
    """Client side class for the cog thief  game."""
    notify = directNotify.newCategory("DistributedCogThiefGame")

    # define constants that you won't want to tweak here
    # TODO: scale?
    ToonSpeed = CTGG.ToonSpeed

    # TODO: calc?
    StageHalfWidth = 200.
    StageHalfHeight = 100.


    BarrelScale = 0.25

    TOON_Z = 0

    UPDATE_SUITS_TASK = "CogThiefGameUpdateSuitsTask"
    REWARD_COUNTDOWN_TASK   = "cogThiefGameRewardCountdown"
    
    ControlKeyLimitTime = 1.0 # how many seconds before player can press control again
    #ControlKeyLimitTime = 0.0 # how many seconds before player can press control again

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedCogThiefGame',
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
        #self.cameraTopView = (0, 0, 65, 0, -90.0, 0)
        # this gives a bigger scale, but you lose advance warning of the cogs
        self.cameraTopView = (0, 0, 55, 0, -90.0, 0)
        self.barrels = []

        self.cogInfo = {}
        self.lastTimeControlPressed = 0
        self.stolenBarrels = []
        self.useOrthoWalk = base.config.GetBool('cog-thief-ortho', 1)

        self.resultIval = None
        self.gameIsEnding = False

        # this will be used to generate textnodes
        self.__textGen = TextNode("cogThiefGame")
        self.__textGen.setFont(ToontownGlobals.getSignFont())
        self.__textGen.setAlign(TextNode.ACenter)

    def getTitle(self):
        return TTLocalizer.CogThiefGameTitle

    def getInstructions(self):
        return TTLocalizer.CogThiefGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        self.music = base.loadMusic("phase_4/audio/bgm/MG_CogThief.mid")
        self.initCogInfo()

        # TODO: vary number based on diffculty?
        # Hmmm, should this be done on the AI?
        for barrelIndex in range(CTGG.NumBarrels):
            barrel = loader.loadModel("phase_4/models/minigames/cogthief_game_gagTank")
            barrel.setPos(CTGG.BarrelStartingPositions[barrelIndex])
            barrel.setScale(self.BarrelScale)
            barrel.reparentTo(render)

            barrel.setTag('barrelIndex', str(barrelIndex))
            
            collSphere = CollisionSphere(0, 0, 0, 4)
            # Make the sphere intangible
            collSphere.setTangible(0)
            name = "BarrelSphere-%d" % barrelIndex
            collSphereName = self.uniqueName(name)
            collNode = CollisionNode(collSphereName)
            collNode.setFromCollideMask(CTGG.BarrelBitmask)
            collNode.addSolid(collSphere)
            colNp = barrel.attachNewNode(collNode)

            handler = CollisionHandlerEvent()
            handler.setInPattern('barrelHit-%fn')
            base.cTrav.addCollider(colNp, handler)
            self.accept('barrelHit-' + collSphereName,
                    self.handleEnterBarrel)

            # display the 5 or 10 dollar symbol
            nodeToHide = "**/gagMoneyTen"
            if barrelIndex % 2:
                nodeToHide = "**/gagMoneyFive"
            iconToHide = barrel.find(nodeToHide)
            if not iconToHide.isEmpty():
                iconToHide.hide()
            self.barrels.append(barrel)

            
         # load resources and create objects here
        self.gameBoard = loader.loadModel("phase_4/models/minigames/cogthief_game")
        self.gameBoard.find("**/floor_TT").hide()
        self.gameBoard.find("**/floor_DD").hide()
        self.gameBoard.find("**/floor_DG").hide()
        self.gameBoard.find("**/floor_MM").hide()
        self.gameBoard.find("**/floor_BR").hide()
        self.gameBoard.find("**/floor_DL").hide()
        
        zone = self.getSafezoneId()
        if zone == ToontownGlobals.ToontownCentral:
            self.gameBoard.find("**/floor_TT").show()
        elif zone == ToontownGlobals.DonaldsDock:
            self.gameBoard.find("**/floor_DD").show()
        elif zone == ToontownGlobals.DaisyGardens:
            self.gameBoard.find("**/floor_DG").show()
        elif zone == ToontownGlobals.MinniesMelodyland:
            self.gameBoard.find("**/floor_MM").show()
        elif zone == ToontownGlobals.TheBrrrgh:
            self.gameBoard.find("**/floor_BR").show()
        elif zone == ToontownGlobals.DonaldsDreamland:
            self.gameBoard.find("**/floor_DL").show()
        else:
            self.gameBoard.find("**/floor_TT").show()
            
        #self.gameBoard = loader.loadModel("phase_4/models/minigames/toon_cannon_gameground")
        self.gameBoard.setPosHpr(0,0,0,0,0,0)
        self.gameBoard.setScale(1.0)

        # make a dictionary of CogThiefGameToonSDs; they will track
        # toons' states and animate them appropriately
        self.toonSDs = {}
        # add the local toon now, add remote toons as they join
        avId = self.localAvId
        toonSD = CogThiefGameToonSD.CogThiefGameToonSD(avId, self)
        self.toonSDs[avId] = toonSD
        toonSD.load()

        self.loadCogs()

        # make a dictionary of tracks for showing each toon
        # getting hit by a suit
        self.toonHitTracks = {}

        # a dictionary of throwing pie tracks
        self.toonPieTracks = {}

        self.sndOof = base.loadSfx(
            'phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.sndRewardTick = base.loadSfx(\
                                 "phase_3.5/audio/sfx/tick_counter.mp3")
        self.sndPerfect = base.loadSfx(
            "phase_4/audio/sfx/ring_perfect.mp3")


        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.hide()

        # load the jellybean jar image
        # this model is 'owned' (read: destroyed) by PurchaseBase
        purchaseModels = loader.loadModel(
                "phase_4/models/gui/purchase_gui")
        self.jarImage = purchaseModels.find("**/Jar")
        self.jarImage.reparentTo(hidden)        

       # reward display
        self.rewardPanel = DirectLabel(
            parent = hidden,
            relief = None,
            pos = (1.16, 0.0, 0.45),
            scale = .65,
            text = '',
            text_scale = 0.2,
            text_fg = (0.95, 0.95, 0, 1),
            text_pos = (0, -.13),
            text_font = ToontownGlobals.getSignFont(),
            image = self.jarImage,
            )
        self.rewardPanelTitle = DirectLabel(
            parent = self.rewardPanel,
            relief = None,
            pos = (0, 0, 0.06),
            scale = .08,
            text = TTLocalizer.CannonGameReward,
            text_fg = (.95,.95,0,1),
            text_shadow = (0,0,0,1),
            )


    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        del self.music
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM
        self.gameBoard.removeNode()
        del self.gameBoard

        for barrel in self.barrels:
            barrel.removeNode()
        del self.barrels
            
        for avId in self.toonSDs.keys():
            toonSD = self.toonSDs[avId]
            toonSD.unload()
        del self.toonSDs

        # Goodbye timer
        self.timer.destroy()
        del self.timer

        self.rewardPanel.destroy()
        del self.rewardPanel
        self.jarImage.removeNode()
        del self.jarImage
        
        # Get rid of audio
        del self.sndRewardTick        

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        self.gameBoard.reparentTo(render)

        lt = base.localAvatar
        lt.reparentTo(render)
        self.__placeToon(self.localAvId)
        lt.setSpeed(0,0)

        self.moveCameraToTop()
        
        toonSD = self.toonSDs[self.localAvId]
        toonSD.enter()
        toonSD.fsm.request('normal')
        # disable the local toon's 'input drive' so that the player can't run yet
        self.stopGameWalk()

        # put the cogs on the board
        for cogIndex in xrange(self.getNumCogs()):
            suit= self.cogInfo[cogIndex]['suit'].suit
            pos = self.cogInfo[cogIndex]['pos']
            suit.reparentTo(self.gameBoard)
            suit.setPos(pos)

        # fill in the toonHitTracks dict with bogus tracks
        for avId in self.avIdList:
            self.toonHitTracks[avId] = Wait(0.1)

        # create random num generators for each toon
        self.toonRNGs = []
        for i in xrange(self.numPlayers):
            self.toonRNGs.append(RandomNumGen.RandomNumGen(self.randomNumGen))

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

        # Start music
        # RAUTODO low level bug, music volume playing at full blast even
        # when set to 0.1, revisit when fixed
        base.playMusic(self.music, looping = 1, volume = 0.8)

        self.introTrack = self.getIntroTrack()
        self.introTrack.start()
        

    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        self.gameBoard.hide()
        self.music.stop()
        
        for barrel in self.barrels:
            barrel.hide()

        for avId in self.toonSDs.keys():
            self.toonSDs[avId].exit()

        # reset the toons' LODs and show their dropshadows again
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.resetLOD()

        self.timer.reparentTo(hidden)
        self.rewardPanel.reparentTo(hidden)

        if self.introTrack.isPlaying():
            self.introTrack.finish()
        del self.introTrack        
        
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

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.

        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                self.__placeToon(avId)
                toon.useLOD(1000)
                
                # create the toonSD for this toon
                toonSD = CogThiefGameToonSD.CogThiefGameToonSD(avId, self)
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
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state

        # Start counting down the game clock,
        # call __gameTimerExpired when it reaches 0
        if not base.config.GetBool('cog-thief-endless', 0):        
            self.timer.show()
            self.timer.countdown(CTGG.GameTime,
                             self.__gameTimerExpired)

        self.clockStopTime = None
        self.rewardPanel.reparentTo(aspect2d)
        self.scoreMult = MinigameGlobals.getScoreMult(self.cr.playGame.hood.id)
        self.__startRewardCountdown()

        if self.introTrack.isPlaying():
            self.introTrack.finish()        
            
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
        self.startGameWalk()
        
        self.spawnUpdateSuitsTask()

        self.accept('control', self.controlKeyPressed)

        self.pieHandler = CollisionHandlerEvent()
        self.pieHandler.setInPattern('pieHit-%fn')
            

        # when the game is done, call gameOver()
        #self.gameOver()

    def exitPlay(self):
        self.ignore('control')
        if self.resultIval and self.resultIval.isPlaying():
            self.resultIval.finish()
            self.resultIval = None 
        pass

    def enterCleanup(self):
        """Cleanup everything to shut down cleanly."""
        self.__killRewardCountdown()
        if hasattr(self, 'jarIval'):
            self.jarIval.finish()
            del self.jarIval
        
        for key in self.toonHitTracks:
            ival = self.toonHitTracks[key]
            if ival.isPlaying():
                ival.finish()
        self.toonHitTracks = {}
        for key in self.toonPieTracks:
            ival = self.toonPieTracks[key]
            if ival.isPlaying():
                ival.finish()
        self.toonPieTracks = {}
        
        for key in self.cogInfo:
            cogThief = self.cogInfo[key]['suit']
            cogThief.cleanup()
        self.removeUpdateSuitsTask()
        
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    def __placeToon(self, avId):
        """ places a toon in its starting position """
        toon = self.getAvatar(avId)
        if toon:
            index = self.avIdList.index(avId)
            toon.setPos(CTGG.ToonStartingPositions[index])
            toon.setHpr(0,0,0)

    def moveCameraToTop(self):
        camera.reparentTo(render)
        p = self.cameraTopView
        camera.setPosHpr(p[0], p[1], p[2], p[3], p[4], p[5])

        camera.setZ(camera.getZ() + base.config.GetFloat('cog-thief-z-camera-adjust',0.0))
            

    # orthowalk init/shutdown

    def destroyGameWalk(self):
        self.notify.debug("destroyOrthoWalk")

        if self.useOrthoWalk:
            self.gameWalk.destroy()
            del self.gameWalk
        else:
            self.notify.debug("TODO destroyGameWalk")
            pass

    # orthowalk init/shutdown
    def initGameWalk(self):
        self.notify.debug("startOrthoWalk")

        if self.useOrthoWalk:
            def doCollisions(oldPos, newPos, self=self):
                # make the toon collide against the boundaries of the playfield
                x = bound(newPos[0], CTGG.StageHalfWidth, -CTGG.StageHalfWidth)
                y = bound(newPos[1], CTGG.StageHalfHeight, -CTGG.StageHalfHeight)
                newPos.setX(x)
                newPos.setY(y)
                return newPos

            orthoDrive = OrthoDrive(
                self.ToonSpeed,
                customCollisionCallback=doCollisions,
                instantTurn = True
                )
            self.gameWalk = OrthoWalk(orthoDrive,
                                   broadcast=not self.isSinglePlayer())
        else:        
            self.gameWalk = CogThiefWalk.CogThiefWalk("walkDone")
            forwardSpeed = self.ToonSpeed /2.0
            base.mouseInterfaceNode.setForwardSpeed(forwardSpeed)
            multiplier = forwardSpeed / ToontownGlobals.ToonForwardSpeed
            base.mouseInterfaceNode.setRotateSpeed(ToontownGlobals.ToonRotateSpeed *
                                                   4)

    def initCogInfo(self):
        """For each cog, initialize the info about him."""
        for cogIndex in xrange(self.getNumCogs()):
            self.cogInfo[cogIndex] = {
                'pos' : Point3(CTGG.CogStartingPositions[cogIndex]),
                'goal' : CTGG.NoGoal,
                'goalId' : CTGG.InvalidGoalId,
                'suit' : None
                }
                               
    def loadCogs(self):
        """Create the suits."""
        suitTypes = ['ds',  # downsizer
                     'ac', # ambulance chaser
                     'bc', # bean counter
                     'ms', # mover & shaker
                     ]
        for suitIndex in xrange(self.getNumCogs()):
            st =  self.randomNumGen.choice(suitTypes)
            suit = CogThief.CogThief(suitIndex, st, self, self.getCogSpeed())
            
            self.cogInfo[suitIndex]['suit'] = suit


    def handleEnterSphere(self, colEntry):
        """Handle the toon hitting one of the suits."""
        if self.gameIsEnding:
            return
        intoName = colEntry.getIntoNodePath().getName()
        fromName = colEntry.getFromNodePath().getName()
        debugInto = intoName.split('/')
        debugFrom = fromName.split('/')
        
        self.notify.debug('handleEnterSphere gametime=%s %s into %s' %
                          (self.getCurrentGameTime(),
                           debugFrom[-1],
                           debugInto[-1]))        
        intoName = colEntry.getIntoNodePath().getName()
        if 'CogThiefSphere' in intoName:
            # we hit a suit
            parts = intoName.split('-')
            suitNum = int(parts[1])
            self.localToonHitBySuit(suitNum)

    def localToonHitBySuit(self, suitNum):
        """Handle the local toon hitting a suit."""
        self.notify.debug('localToonHitBySuit %d' % suitNum)
        timestamp = globalClockDelta.localToNetworkTime(\
            globalClock.getFrameTime(), bits=32)
        pos = self.cogInfo[suitNum]['suit'].suit.getPos()
        
        self.sendUpdate("hitBySuit", [self.localAvId, timestamp, suitNum,
                                      pos[0], pos[1], pos[2]])
        self.showToonHitBySuit(self.localAvId, timestamp)
        self.makeSuitRespondToToonHit(timestamp, suitNum)

    def hitBySuit(self, avId, timestamp, suitNum, x, y, z):
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() not in [
            'play', ]:
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return
        if self.gameIsEnding:
            return
        self.notify.debug("avatar " + `avId` + " hit by a suit")
        if avId != self.localAvId:
            self.showToonHitBySuit(avId, timestamp)
            self.makeSuitRespondToToonHit(timestamp, suitNum)
            
    def showToonHitBySuit(self, avId, timestamp):
        """Show the toon flying in the air falling to his starting spot."""
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
                                           gravMult=1.0)
        oldFlyDur= trajectory.calcTimeOfImpactOnPlane(0.)
        
        trajectory = Trajectory.Trajectory(0,
                                           Point3(0,0,0),
                                           Point3(0,0,50),
                                           gravMult=0.55)
        flyDur = trajectory.calcTimeOfImpactOnPlane(0.)
        #self.notify.info('flyDurationIncrease=%s' % (flyDur - oldFlyDur))
        assert(flyDur > 0)

        # choose a random landing point
        #while 1:
        #    endTile = [rng.randint(2,self.maze.width-1),
        #               rng.randint(2,self.maze.height-1)]
        #    if self.maze.isWalkable(endTile[0],endTile[1]):
        #        break
        avIndex = self.avIdList.index(avId)
        endPos = CTGG.ToonStartingPositions[avIndex]
        
        #endWorldCoords = self.maze.tile2world(endTile[0],endTile[1])
        #endPos = Point3(endWorldCoords[0], endWorldCoords[1], startPos[2])

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

        """
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
        """

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
                self.stopGameWalk()
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
                if hasattr(self, 'gameWalk'):
                    # re-enable control of local toon
                    toon = base.localAvatar
                    toon.setSpeed(0,0)
                    self.startGameWalk()

            # get rid of the dropshadow
            dropShadow.removeNode()
            del dropShadow

            # show the toon's dropshadow
            toon = self.getAvatar(avId)
            if toon:
                toon.dropShadow.show()

                # get rid of the extra nodes
                geomNode = toon.getGeomNode()
                rotNode = geomNode.getParent()
                baseNode = rotNode.getParent()
                geomNode.reparentTo(baseNode)
                rotNode.removeNode()
                del rotNode
                geomNode.setZ(oldGeomNodeZ)

            if toon:
                toon.reparentTo(render)
                toon.setPos(endPos)
            parentNode.removeNode()
            del parentNode

            if avId != self.localAvId:
                if toon:
                    toon.startSmooth()

        # call the preFunc _this_frame_ to ensure that the local toon
        # update task does not run this frame
        preFunc()

        slipBack = Parallel(
            Sequence(
              ActorInterval( toon, 'slip-backward', endFrame = 24),
              Wait(CTGG.LyingDownDuration - (flyDur - oldFlyDur)), # we can control how long he stays down
              ActorInterval(toon, 'slip-backward', startFrame = 24)
              ))
                                 
        if toon.doId == self.localAvId:
            slipBack.append( SoundInterval(self.sndOof))
        hitTrack = Sequence(
            Parallel(flyTrack, #cameraTrack,
                     spinHTrack, spinPTrack, soundTrack),
            slipBack,
            Func(postFunc),
            name=toon.uniqueName("hitBySuit"))

        self.notify.debug('hitTrack duration = %s' % hitTrack.getDuration())

        self.toonHitTracks[avId] = hitTrack
        hitTrack.start(globalClockDelta.localElapsedTime(timestamp))
        
    def updateSuitGoal( self,  timestamp, inResponseToClientStamp,  suitNum,  goalType,  goalId,  x , y,  z):
        """AI is telling a suit to do something else."""
        #assert self.notify.debugStateCall(self)
        if not self.hasLocalToon: return
        self.notify.debug('updateSuitGoal gameTime=%s timeStamp=%s cog=%s goal=%s goalId=%s (%.1f, %.1f,%.1f)' %
                          (self.getCurrentGameTime(), timestamp, suitNum,
                           CTGG.GoalStr[goalType], goalId, x,y,z))
        cog = self.cogInfo[suitNum]
        cog['goal'] = goalType
        cog['goalId'] = goalId
        newPos = Point3(x,y,z)
        cog['pos'] = newPos
        suit = cog['suit']
        suit.updateGoal( timestamp, inResponseToClientStamp, goalType, goalId, newPos)

    def spawnUpdateSuitsTask(self):
        """Start the task that makes the suits think."""
        self.notify.debug("spawnUpdateSuitsTask")
        for cogIndex in self.cogInfo:
            suit = self.cogInfo[cogIndex]['suit']
            suit.gameStart(self.gameStartTime)

        taskMgr.remove(self.UPDATE_SUITS_TASK)
        taskMgr.add(self.updateSuitsTask, self.UPDATE_SUITS_TASK)

    def removeUpdateSuitsTask(self):
        """Remove the task that makes the suits think."""        
        taskMgr.remove(self.UPDATE_SUITS_TASK)

    def updateSuitsTask(self, task):
        #print "__updateSuitsTask"
        if self.gameIsEnding:
            return task.done
        for cogIndex in self.cogInfo:
            suit = self.cogInfo[cogIndex]['suit']
            suit.think()
        return task.cont
        
    def makeSuitRespondToToonHit(self, timestamp, suitNum):
        """A toon hit the suit, make the suit do something."""
        cog = self.cogInfo[suitNum]['suit']
        cog.respondToToonHit(timestamp)
        

    def handleEnterBarrel(self, colEntry):
        """Handle a cog hitting the barrel."""
        if self.gameIsEnding:
            return
        intoName = colEntry.getIntoNodePath().getName()
        fromName = colEntry.getFromNodePath().getName()
        debugInto = intoName.split('/')
        debugFrom = fromName.split('/')
        self.notify.debug('handleEnterBarrel gameTime=%s %s into %s' %
                          (self.getCurrentGameTime(),
                           debugFrom[-1],
                           debugInto[-1]))         
        if 'CogThiefSphere' in intoName:
            parts = intoName.split('-')
            cogIndex = int(parts[1])
            
            barrelName = colEntry.getFromNodePath().getName()
            barrelParts = barrelName.split('-')
            barrelIndex = int(barrelParts[1])

            cog = self.cogInfo[cogIndex]['suit']

            # ignore the hit if we are already carrying a barrel
            # and the barrel and is not stolen 
            if cog.barrel == CTGG.NoBarrelCarried and \
               barrelIndex not in self.stolenBarrels:
                timestamp = globalClockDelta.localToNetworkTime(\
                    globalClock.getFrameTime(), bits=32)

                if cog.suit:
                    cogPos = cog.suit.getPos()            
                    collisionPos  = colEntry.getContactPos(render)

                    if (cogPos - collisionPos).length() > 4:
                        import pdb; pdb.set_trace()
                    # do an immediate stop on cog
                    # rely on setPlayRate instead
                    # cog.stopWalking(timestamp)


                    # Just tell the AI, don't tell other clients, 

                    self.sendUpdate("cogHitBarrel", [ timestamp, cogIndex, barrelIndex,
                                                   cogPos[0], cogPos[1], cogPos[2]])

        
    def makeCogCarryBarrel(self, timestamp, inResponseToClientStamp, cogIndex, barrelIndex, x,y,z):
        """Handle the AI telling us the barrel is attached to a cog."""
        if not self.hasLocalToon: return
        if self.gameIsEnding:
            return
        #assert self.notify.debugStateCall(self)
        self.notify.debug('makeCogCarryBarrel gameTime=%s timeStamp=%s cog=%s barrel=%s (%.1f, %.1f,%.1f)' %
                          (self.getCurrentGameTime(), timestamp, cogIndex,
                           barrelIndex, x,y,z))        
        
        barrel = self.barrels[barrelIndex]
        self.notify.debug('barrelPos= %s' % barrel.getPos())
        cog = self.cogInfo[cogIndex]['suit']
        
        #barrel.setPos(0,-1.0,1.5)
        #barrel.reparentTo(cog.suit)
        #cog.suit.setPos(x,y,z)
        
        cogPos = Point3(x,y,z)
        cog.makeCogCarryBarrel(timestamp, inResponseToClientStamp, barrel, barrelIndex, cogPos)

    def makeCogDropBarrel(self, timestamp, inResponseToClientStamp, cogIndex, barrelIndex, x,y,z):
        """Handle the AI telling us the barrel is dropping from a cog."""
        assert self.notify.debugStateCall(self)
        if not self.hasLocalToon: return
        self.notify.debug('makeCogDropBarrel gameTime=%s timeStamp=%s cog=%s barrel=%s (%.1f, %.1f,%.1f)' %
                          (self.getCurrentGameTime(), timestamp, cogIndex,
                           barrelIndex, x,y,z))               
        
        barrel = self.barrels[barrelIndex]
        self.notify.debug('barrelPos= %s' % barrel.getPos())

        cog = self.cogInfo[cogIndex]['suit']
        cogPos = Point3(x,y,z)

        cog.makeCogDropBarrel(timestamp, inResponseToClientStamp, barrel, barrelIndex, cogPos)
        #barrel.reparentTo(render )
        #barrel.setPos(x,y,z)


    def controlKeyPressed(self):
        """Make the toon fire when the player presses the control key."""
        if self.isToonPlayingHitTrack(self.localAvId):
            # don't let player fire a pie while stunned
            return
        if self.gameIsEnding:
            return
        if self.getCurrentGameTime() - self.lastTimeControlPressed > \
           self.ControlKeyLimitTime:
            self.lastTimeControlPressed  = self.getCurrentGameTime()
            
            self.notify.debug('controlKeyPressed')
            
            toonSD = self.toonSDs[self.localAvId]
            curState = toonSD.fsm.getCurrentState().getName()
            #if curState == 'normal':
            #    toonSD.fsm.request('throwPie')
            toon = self.getAvatar(self.localAvId)
            timestamp = globalClockDelta.localToNetworkTime(\
                globalClock.getFrameTime(),bits=32)
            pos = toon.getPos()
            heading = toon.getH()
            self.sendUpdate('throwingPie',[self.localAvId, timestamp, heading,
                                           pos[0], pos[1], pos[2]])
            self.showToonThrowingPie(self.localAvId, timestamp, heading, pos)

    def throwingPie(self, avId, timestamp, heading, x, y, z):
        """Handle another client telling us he's throwing a pie."""
        if not self.hasLocalToon: return
        if self.gameFSM.getCurrentState().getName() not in [
            'play', ]:
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return
        self.notify.debug("avatar " + `avId` + " throwing pie")
        if avId != self.localAvId:
            pos = Point3(x,y,z)            
            self.showToonThrowingPie(avId, timestamp, heading, pos)

    def showToonThrowingPie(self, avId, timestamp, heading, pos):
        """Show local or remote toon throwing a pie."""
        #pie = loader
        toon = self.getAvatar(avId)
        if toon:
            tossTrack, pieTrack, flyPie = self.getTossPieInterval(toon, pos[0], pos[1], pos[2] ,
                                                        heading, 0, 0, 0)

            def removePieFromTraverser(flyPie = flyPie):
                if base.cTrav:
                    if flyPie:
                        base.cTrav.removeCollider(flyPie)
            if avId == self.localAvId:
                flyPie.setTag('throwerId', str(avId))

                collSphere = CollisionSphere(0, 0, 0, 0.5)
                # Make the sphere intangible
                collSphere.setTangible(0)
                name = "PieSphere-%d" % avId
                collSphereName = self.uniqueName(name)
                collNode = CollisionNode(collSphereName)
                collNode.setFromCollideMask(ToontownGlobals.PieBitmask)
                collNode.addSolid(collSphere)
                colNp = flyPie.attachNewNode(collNode)
                colNp.show()

                base.cTrav.addCollider(colNp, self.pieHandler)
            
                self.accept('pieHit-' + collSphereName, self.handlePieHitting)
            
            def matchRunningAnim(toon=toon):
                toon.playingAnim = None
                toon.setSpeed(toon.forwardSpeed, toon.rotateSpeed)
            newTossTrack = Sequence(tossTrack,
                                    Func(matchRunningAnim))
                                    
            pieTrack = Parallel(newTossTrack,pieTrack)

            elapsedTime = globalClockDelta.localElapsedTime(timestamp)
            if elapsedTime < 16. / 24.:
                elapsedTime = 16. / 24. # make the pie fly immediately
            pieTrack.start(elapsedTime)
            self.toonPieTracks[avId] = pieTrack


    def getTossPieInterval(self, toon,  x, y, z, h, p, r, power,
                           beginFlyIval = Sequence()):
        """Adapted from toon.py to suit our needs.
        Returns (toss, pie, flyPie), where toss is an interval to
        animate the toon tossing a pie, pie is the interval to
        animate the pie flying through the air, and pieModel is the
        model that flies.  This is used in the final BossBattle
        sequence of CogHQ when we all throw pies directly at the
        boss cog.
        """
                    
        from toontown.toonbase import ToontownBattleGlobals
        from toontown.battle import BattleProps

        pie = toon.getPieModel()
        pie.setScale(0.9)
        flyPie = pie.copyTo(NodePath('a'))
        pieName = ToontownBattleGlobals.pieNames[toon.pieType]
        pieType = BattleProps.globalPropPool.getPropType(pieName)
        animPie = Sequence()
        if pieType == 'actor':
            animPie = ActorInterval(pie, pieName, startFrame = 48)

        sound = loader.loadSfx('phase_3.5/audio/sfx/AA_pie_throw_only.mp3')

        # First, create a ProjectileInterval to compute the relative
        # velocity.

        t = power / 100.0

        # Distance ranges from 100 - 20 ft, time ranges from 1 - 1.5 s.
        dist = 100 - 70 * t
        time = 1 + 0.5 * t
        proj = ProjectileInterval(
            None, startPos = Point3(0, 0, 0), endPos = Point3(0, dist, 0),
            duration = time)
        relVel = proj.startVel

        def getVelocity(toon = toon, relVel = relVel):
            return render.getRelativeVector(toon, relVel) * 0.6

        toss = Track(
            (0, Sequence(Func(toon.setPosHpr, x, y, z, h, p, r),
                         Func(pie.reparentTo, toon.rightHand),
                         Func(pie.setPosHpr, 0, 0, 0, 0, 0, 0),
                         Parallel(ActorInterval(toon, 'throw', startFrame = 48, partName = 'torso'),
                                  animPie, ),
                         Func(toon.loop, 'neutral'),
                         )),
            (16./24., Func(pie.detachNode)))

        fly = Track(
            (14./24., SoundInterval(sound, node = toon)),
            (16./24.,
             Sequence(Func(flyPie.reparentTo, render),
                      Func(flyPie.setPosHpr, toon,
                           0.52, 0.97, 2.24,
                           0, -45, 0),
                      beginFlyIval,
                      ProjectileInterval(flyPie, startVel = getVelocity ,
                                         duration = 6),
                      #LerpPosInterval(flyPie, duration = 3, Point3(0.52,50,2.24)),
                      Func(flyPie.detachNode),
                      )),
            )
        return (toss, fly, flyPie)


    def handlePieHitting(self, colEntry):
        """Handle the pie thrown by the local toon hitting something."""
        #print colEntry
        if self.gameIsEnding:
            return        
        into = colEntry.getIntoNodePath()
        intoName = into.getName()
        if 'CogThiefPieSphere' in intoName:
            timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
            parts = intoName.split('-')
            suitNum = int(parts[1])
            pos = self.cogInfo[suitNum]['suit'].suit.getPos()
            if pos in CTGG.CogStartingPositions:
                self.notify.debug('Cog %d hit at starting pos %s, ignoring' % (suitNum,pos))
            else:
                self.sendUpdate("pieHitSuit", [self.localAvId, timestamp, suitNum,
                                               pos[0], pos[1], pos[2]])
                self.makeSuitRespondToPieHit(timestamp, suitNum)
            

    def pieHitSuit(self, avId, timestamp, suitNum, x, y, z):        
        if not self.hasLocalToon: return        
        if self.gameFSM.getCurrentState().getName() not in [
            'play', ]:
            self.notify.warning('ignoring msg: av %s hit by suit' % avId)
            return
        if self.gameIsEnding:
            return
        self.notify.debug("avatar " + `avId` + " hit by a suit")
        if avId != self.localAvId:
            self.makeSuitRespondToPieHit(timestamp, suitNum)

    def makeSuitRespondToPieHit(self, timestamp, suitNum):
        """A toon hit the suit, make the suit do something."""
        cog = self.cogInfo[suitNum]['suit']
        cog.respondToPieHit(timestamp)

    
    def sendCogAtReturnPos(self, cogIndex, barrelIndex):
        """Tell the AI a suit has successfully returned with a barrel."""
        timestamp = globalClockDelta.localToNetworkTime(\
            globalClock.getFrameTime(), bits=32)
        
        self.sendUpdate('cogAtReturnPos', [timestamp, cogIndex, barrelIndex])


    def markBarrelStolen(self, timestamp, inResponseToClientStamp, barrelIndex):
        """Handle the AI telling us a barrel was successfully stolen."""
        if not self.hasLocalToon: return
        if not barrelIndex in self.stolenBarrels:
            self.stolenBarrels.append(barrelIndex)
            barrel = self.barrels[barrelIndex]
            barrel.hide()
        if base.config.GetBool('cog-thief-check-barrels', 1):
            if not base.config.GetBool('cog-thief-endless', 0):
                if len(self.stolenBarrels) == len(self.barrels):
                    localStamp = globalClockDelta.networkToLocalTime(timestamp, bits=32)
                    gameTime = self.local2GameTime(localStamp)
                    self.clockStopTime = gameTime
                    self.notify.debug('clockStopTime = %s' % gameTime)

                    # force an update of the jelly bean count
                    score = int(self.scoreMult * CTGG.calcScore(gameTime) + .5)
                    
                    self.rewardPanel['text'] = str(score)                    
                    self.showResults()
             

    def __gameTimerExpired(self):
        """Handle the game timer expiring."""
        self.notify.debug("game timer expired")

        # finish the game
        self.showResults()

    def __startRewardCountdown(self):
        taskMgr.remove(self.REWARD_COUNTDOWN_TASK)
        taskMgr.add(self.__updateRewardCountdown, self.REWARD_COUNTDOWN_TASK)

    def __killRewardCountdown(self):
        taskMgr.remove(self.REWARD_COUNTDOWN_TASK)

    def __updateRewardCountdown(self, task):
        curTime = self.getCurrentGameTime()

        # if it's time for the clock to stop, stop it
        if self.clockStopTime is not None:
            if self.clockStopTime < curTime:
                self.notify.debug('self.clockStopTime < curTime %s %s' %
                                  (self.clockStopTime, curTime))
                self.__killRewardCountdown()
                # force the jbean jar to the clockStopTime, so that
                # we show the same number of jbeans that we'll see
                # in the reward screen
                curTime = self.clockStopTime

        if curTime > CTGG.GameTime:
            curTime = CTGG.GameTime
            
        # if this is the first time through, init the task's
        # record of the score
        score = int(self.scoreMult * CTGG.calcScore(curTime) + .5)
        if not hasattr(task, 'curScore'):
            task.curScore = score

        result = Task.cont
        if hasattr(self, 'rewardPanel'):
            self.rewardPanel['text'] = str(score)

            if task.curScore != score:
                if hasattr(self, 'jarIval'):
                    self.jarIval.finish()

                # make the jar animate
                s = self.rewardPanel.getScale()
                self.jarIval = Parallel(\
                    Sequence(self.rewardPanel.scaleInterval(.15, s*3./4.,
                                                            blendType='easeOut'),
                             self.rewardPanel.scaleInterval(.15, s,
                                                            blendType='easeIn'),
                             ),
                    SoundInterval(self.sndRewardTick),
                    name='cogThiefGameRewardJarThrob')
                self.jarIval.start()

            task.curScore = score

        else:
            result = Task.done

        return result

    def startGameWalk(self):
        """Enable the local toon to be controlled and run around."""
        if self.useOrthoWalk:
            self.gameWalk.start()
        else:
            self.gameWalk.enter()
            self.gameWalk.fsm.request("walking")            

    def stopGameWalk(self):
        """Disable the local toon to be controlled and run around."""        
        pass
        if self.useOrthoWalk:
            self.gameWalk.stop()
        else:
            self.gameWalk.exit()

    def getCogThief(self, cogIndex):
        """Return a reference to the indicated cog thief."""
        return self.cogInfo[cogIndex]['suit']

    def isToonPlayingHitTrack(self, avId):
        """Return true if this toon is still playing the hit track."""
        if avId in self.toonHitTracks:
            track = self.toonHitTracks[avId]
            if track.isPlaying():
                return True
        return False

    def getNumCogs(self):
        """Return the number of cogs we have for this game."""
        result = base.config.GetInt('cog-thief-num-cogs', 0)
        if not result:
            safezone = self.getSafezoneId()
            result = CTGG.calculateCogs(self.numPlayers, safezone)
        return result
        
    def getCogSpeed(self):
        """Return the speed of the cogs in this difficulty."""
        result = 6.0
        safezone = self.getSafezoneId()
        result = CTGG.calculateCogSpeed(self.numPlayers, safezone)
        return result

    
    def showResults(self):
        """Inform the players how well they did."""
        if not self.gameIsEnding:
            self.gameIsEnding = True

            # force all barrels to have render as parent
            # the cogs get hidden
            for barrel in self.barrels:
                barrel.wrtReparentTo(render)
            
            # move all suits somewhere far away
            for key in self.cogInfo:
                thief = self.cogInfo[key]['suit']
                thief.suit.setPos(100,0,0)
                thief.suit.hide()

            self.__killRewardCountdown()
            self.stopGameWalk()
            
            numBarrelsSaved = len(self.barrels) - len(self.stolenBarrels)
            resultStr = ""
            if numBarrelsSaved == len(self.barrels):
                resultStr = TTLocalizer.CogThiefPerfect
            elif numBarrelsSaved > 1:
                resultStr = TTLocalizer.CogThiefBarrelsSaved % {'num': numBarrelsSaved}
            elif numBarrelsSaved == 1:
                resultStr = TTLocalizer.CogThiefBarrelSaved % {'num': numBarrelsSaved}
            else:
                resultStr = TTLocalizer.CogThiefNoBarrelsSaved
                
            perfectTextSubnode = hidden.attachNewNode(
                self.__genText(resultStr))
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

            def safeGameOver(self=self):
                if not self.frameworkFSM.isInternalStateInFlux():
                    self.gameOver()

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
                Func(safeGameOver),
                )

            if numBarrelsSaved == len(self.barrels):
                soundTrack = SoundInterval(self.sndPerfect)
            else:
                soundTrack = Sequence()

            self.resultIval = Parallel(textTrack,
                                        soundTrack)
            self.resultIval.start()                
                

    def __genText(self, text):
        self.__textGen.setText(text)
        return self.__textGen.generate()

    def getIntroTrack(self):
        """Return an intro track showing the barrels."""
        base.camera.setPosHpr(0,-13.66, 13.59, 0, -51.6, 0)
        result =Sequence(
            Wait(2),
            LerpPosHprInterval(base.camera, 13,
                               Point3(self.cameraTopView[0],
                                      self.cameraTopView[1],
                                      self.cameraTopView[2]),
                               Point3(self.cameraTopView[3],
                                      self.cameraTopView[4],
                                      self.cameraTopView[5]),
                               blendType = 'easeIn'
                               )
            )
        return result
