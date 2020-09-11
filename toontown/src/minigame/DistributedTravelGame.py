"""DistributedMinigameTemplate module: contains the DistributedMinigameTemplate class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import GlobalDialogColor
from DistributedMinigame import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
import TravelGameGlobals
import math
from pandac.PandaModules   import rad2Deg
from toontown.toontowngui import TTDialog

from direct.interval.IntervalGlobal import *
import VoteResultsPanel
import VoteResultsTrolleyPanel

# For each minigame, what's the corresponding icon
IconDict = {
    ToontownGlobals.RaceGameId : 'mg_trolley_sign_race',
    ToontownGlobals.CannonGameId : 'mg_trolley_sign_cannon',
    ToontownGlobals.TagGameId : 'mg_trolley_sign_tag',
    ToontownGlobals.PatternGameId : 'mg_trolley_sign_minnie',
    ToontownGlobals.RingGameId : 'mg_trolley_sign_ring',
    ToontownGlobals.MazeGameId : 'mg_trolley_sign_maze',
    ToontownGlobals.TugOfWarGameId : 'mg_trolley_sign_tugawar',
    ToontownGlobals.CatchGameId : 'mg_trolley_sign_catch',
    ToontownGlobals.DivingGameId : 'mg_trolley_sign_dive',
    ToontownGlobals.TargetGameId :  'mg_trolley_sign_umbrella',
    ToontownGlobals.PairingGameId : 'mg_trolley_sign_card',
    ToontownGlobals.VineGameId : 'mg_trolley_sign_vine',
    ToontownGlobals.IceGameId : 'mg_trolley_sign_ice',
    ToontownGlobals.PhotoGameId : 'mg_trolley_sign_photo',
    ToontownGlobals.TwoDGameId: 'mg_trolley_sign_2d',
    ToontownGlobals.CogThiefGameId: 'mg_trolley_sign_theif',    
    }

# For each minigame, what is it called
MinigameNameDict ={
    ToontownGlobals.RaceGameId : TTLocalizer.RaceGameTitle,
    ToontownGlobals.CannonGameId : TTLocalizer.CannonGameTitle, 
    ToontownGlobals.TagGameId :  TTLocalizer.TagGameTitle,
    ToontownGlobals.PatternGameId :  TTLocalizer.PatternGameTitle,
    ToontownGlobals.RingGameId :  TTLocalizer.RingGameTitle,
    ToontownGlobals.MazeGameId :  TTLocalizer.MazeGameTitle,
    ToontownGlobals.TugOfWarGameId :  TTLocalizer.TugOfWarGameTitle,
    ToontownGlobals.CatchGameId :  TTLocalizer.CatchGameTitle,
    ToontownGlobals.DivingGameId :  TTLocalizer.DivingGameTitle,
    ToontownGlobals.TargetGameId :  TTLocalizer.TargetGameTitle,
    ToontownGlobals.PairingGameId : TTLocalizer.PairingGameTitle,
    ToontownGlobals.VineGameId : TTLocalizer.VineGameTitle,    
    ToontownGlobals.TravelGameId : TTLocalizer.TravelGameTitle,
    ToontownGlobals.IceGameId : TTLocalizer.IceGameTitle,
    ToontownGlobals.PhotoGameId : TTLocalizer.PhotoGameTitle,
    ToontownGlobals.TwoDGameId: TTLocalizer.TwoDGameTitle,
    ToontownGlobals.CogThiefGameId: TTLocalizer.CogThiefGameTitle,
    }

# create a label from a number
def makeLabel(itemName, itemNum, *extraArgs):
    # we use a negative number to indicate going up
    intVersion = int(itemName)
    if intVersion < 0:
        textColor = Vec4(0,0,1,1)
        intVersion = -intVersion
    elif intVersion == 0:
        textColor = Vec4(0,0,0,1)
    else:
        textColor = Vec4(1,0,0,1)
        
    return DirectLabel(text = str(intVersion),
                       text_fg = textColor,
                       relief = DGG.RIDGE,
                       frameSize = (-1.2, 1.2, -0.225, 0.8),
                       scale =1.0, # 0.85,
                       )

def map3dToAspect2d(node, point):
    """Maps the indicated 3-d point (a Point3), which is relative to
    the indicated NodePath, to the corresponding point in the aspect2d
    scene graph.  Returns the corresponding Point3 in aspect2d.
    Returns None if the point is not onscreen. """
    
    # Convert the point to the 3-d space of the camera
    p3 = base.cam.getRelativePoint(node, point)

    # Convert it through the lens to render2d coordinates
    p2 = Point2()
    if not base.camLens.project(p3, p2):
        return None
    
    r2d = Point3(p2[0], 0, p2[1])

    # And then convert it to aspect2d coordinates
    a2d = aspect2d.getRelativePoint(render2d, r2d)

    return a2d

# invert a dictionary, turn the keys into values and vice versa
def invertTable(table):
    index = { }				#empty dictionary
    for key in table.keys():
        value = table[key]
        if not index.has_key(value):
            index[value] = key			# empty list
    return index        

        
class DistributedTravelGame(DistributedMinigame):

    notify = directNotify.newCategory("DistributedTravelGame")

    # define constants that you won't want to tweak here
    idToNames = MinigameNameDict 
    TrolleyMoveDuration = 3
    UseTrolleyResultsPanel = True
    FlyCameraUp = True
    FocusOnTrolleyWhileMovingUp = False    

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        self.gameFSM = ClassicFSM.ClassicFSM('DistributedTravelGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['inputChoice']),
                                State.State('inputChoice',
                                            self.enterInputChoice,
                                            self.exitInputChoice,
                                            ['waitServerChoices',
                                             'displayVotes',
                                             'cleanup']),
                                State.State('waitServerChoices',
                                            self.enterWaitServerChoices,
                                            self.exitWaitServerChoices,
                                            ['displayVotes',
                                             'cleanup']),
                                State.State('displayVotes',
                                            self.enterDisplayVotes,
                                            self.exitDisplayVotes,
                                            ['moveTrolley',
                                             'cleanup']),                                
                                State.State('moveTrolley',
                                            self.enterMoveTrolley,
                                            self.exitMoveTrolley,
                                            ['inputChoice', 'winMovie',
                                             'cleanup']),
                                State.State('winMovie',
                                            self.enterWinMovie,
                                            self.exitWinMovie,
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

        self.currentVotes = {}
        self.cameraTopView = (100, -20, 280, 0, -89, 0)

        # These are None to indicate we have not yet established a
        # timer; they are filled in as we enter the inputChoice state
        # and as the AI reports a start time, respectively.  When both
        # are filled in, the timer will be displayed.
        self.timer = None
        self.timerStartTime = None

        # we always start at node 0
        self.currentSwitch = 0
        self.destSwitch = 0

        self.minigameLabels = []
        self.minigameIcons = []        
        self.bonusLabels = []

        self.trolleyAwaySfx = base.loadSfx("phase_4/audio/sfx/SZ_trolley_away.mp3")
        self.trolleyBellSfx = base.loadSfx("phase_4/audio/sfx/SZ_trolley_bell.mp3")
        self.turntableRotateSfx = base.loadSfx("phase_4/audio/sfx/MG_sfx_travel_game_turntble_rotate_2.mp3")
        self.wonGameSfx = base.loadSfx("phase_4/audio/sfx/MG_sfx_travel_game_bonus.mp3")
        self.lostGameSfx = base.loadSfx("phase_4/audio/sfx/MG_sfx_travel_game_no_bonus_2.mp3")
        self.noWinnerSfx = base.loadSfx("phase_4/audio/sfx/MG_sfx_travel_game_no_bonus.mp3")
        
        self.boardIndex = 0 # which board layour are we using

        self.avNames = [] # names of the players, useful if one disconnects after casting a vote
        self.disconnectedAvIds = [] # keep track which players have disconnected
        
    def getTitle(self):
        return TTLocalizer.TravelGameTitle

    def getInstructions(self):
        return TTLocalizer.TravelGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def load(self):
        """
        load travel game assets, not necessarily showing them onscreen
        """
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky")
        self.gameBoard = loader.loadModel("phase_4/models/minigames/toon_cannon_gameground")
        self.gameBoard.setPosHpr(100,0,0,0,0,0)
        self.gameBoard.setScale(1.0)

        station = loader.loadModel('phase_4/models/modules/trolley_station_TT.bam')
        self.trolleyCar = station.find('**/trolley_car')
        self.trolleyCar.reparentTo(hidden)
        self.trolleyCarOrigPos = self.trolleyCar.getPos()
        self.trolleyCarOrigHpr = self.trolleyCar.getHpr()
        self.trolleyCar.setPosHpr(0,0,0,0,0,0)
        self.trolleyCar.setScale(1.0)
        self.trolleyCar.setX(self.trolleyCar.getX() - TravelGameGlobals.xInc)
        station.removeNode()

        # Variables used to animate trolley parts
        # Key
        self.keys = self.trolleyCar.findAllMatches('**/key')
        self.numKeys = self.keys.getNumPaths()
        self.keyInit = []
        self.keyRef = []
        for i in range(self.numKeys):
            key = self.keys[i]
            key.setTwoSided(1)
            ref = self.trolleyCar.attachNewNode('key' + `i` + 'ref')
            ref.iPosHpr(key)
            self.keyRef.append(ref)
            self.keyInit.append(key.getTransform())
        # Front wheels
        self.frontWheels = self.trolleyCar.findAllMatches('**/front_wheels')
        self.numFrontWheels = self.frontWheels.getNumPaths()
        self.frontWheelInit = []
        self.frontWheelRef = []
        for i in range(self.numFrontWheels):
            wheel = self.frontWheels[i]
            ref = self.trolleyCar.attachNewNode('frontWheel' + `i` + 'ref')
            ref.iPosHpr(wheel)
            self.frontWheelRef.append(ref)
            self.frontWheelInit.append(wheel.getTransform())
        # Back wheels
        self.backWheels = self.trolleyCar.findAllMatches('**/back_wheels')
        self.numBackWheels = self.backWheels.getNumPaths()
        self.backWheelInit = []
        self.backWheelRef = []
        for i in range(self.numBackWheels):
            wheel = self.backWheels[i]
            ref = self.trolleyCar.attachNewNode('backWheel' + `i` + 'ref')
            ref.iPosHpr(wheel)
            self.backWheelRef.append(ref)
            self.backWheelInit.append(wheel.getTransform())

        trolleyAnimationReset = Func(self.resetAnimation)

        self.trainSwitches = {}
        self.trainTracks = {}
        self.tunnels = {} # switch to tunnel dict
        self.extraTrainTracks = [] # the tracks that connects to the root and the leaves
        
        turnTable = loader.loadModel("phase_4/models/minigames/trolley_game_turntable")
        minPoint = Point3(0,0,0)
        maxPoint = Point3(0,0,0)
        turnTable.calcTightBounds(minPoint, maxPoint)

        self.fullLength = maxPoint[0]

        for key in TravelGameGlobals.BoardLayouts[self.boardIndex].keys():
            info = TravelGameGlobals.BoardLayouts[self.boardIndex][key]

            switchModel = turnTable.find('**/turntable1').copyTo(render)

            switchModel.setPos(* info['pos'])
            switchModel.reparentTo(hidden)            
            self.trainSwitches[key] = switchModel
            
            # load the links
            zAdj = 0
            for otherSwitch in info['links']:
                info2 = TravelGameGlobals.BoardLayouts[self.boardIndex][otherSwitch]
                x1,y1,z1 = info['pos']
                x2,y2,z2 = info2['pos']
                linkKey = (key, otherSwitch)
                trainTrack = self.loadTrainTrack(x1,y1,x2,y2, zAdj)
                trainTrack.reparentTo(hidden)
                self.trainTracks[linkKey] = trainTrack
                zAdj += 0.005

        # lay an extra track for the trolley coming in
        rootInfo = TravelGameGlobals.BoardLayouts[self.boardIndex][0]
        rootX, rootY, rootZ = rootInfo['pos']
        startX = rootX - TravelGameGlobals.xInc
        trainTrack = self.loadTrainTrack(startX,rootY, rootX, rootY)
        self.extraTrainTracks.append(trainTrack)

        # lay more extra tracks for the trolley going out
        tunnelX = None
        for key in TravelGameGlobals.BoardLayouts[self.boardIndex].keys():
            if self.isLeaf(key):
                info = TravelGameGlobals.BoardLayouts[self.boardIndex][key]
                switchX, switchY, switchZ = info['pos']
                endX = switchX + TravelGameGlobals.xInc
                trainTrack = self.loadTrainTrack( switchX, switchY, endX, switchY)
                self.extraTrainTracks.append(trainTrack)
                # load a tunnel at the end
                tempModel = loader.loadModel("phase_4/models/minigames/trolley_game_turntable")
                tunnel = tempModel.find('**/tunnel1')
                tunnel.reparentTo(render)
                tempModel.removeNode()
                if not tunnelX:
                    minTrackPoint = Point3(0,0,0)
                    maxTrackPoint = Point3(0,0,0)
                    trainTrack.calcTightBounds(minTrackPoint, maxTrackPoint)
                    tunnelX = maxTrackPoint[0]
                tunnel.setPos(tunnelX, switchY, 0)                
                tunnel.wrtReparentTo(trainTrack)
                self.tunnels[key] = tunnel

        turnTable.removeNode()
        self.loadGui()
        self.introMovie = self.getIntroMovie()

        self.music = base.loadMusic("phase_4/audio/bgm/MG_Travel.mid")
        self.flashWinningBeansTrack = None

    def loadTrainTrack(self, x1, y1, x2, y2, zAdj = 0):
        """
        load a train track that connects those 2 points
        """
        turnTable = loader.loadModel("phase_4/models/minigames/trolley_game_turntable")
        trainPart = turnTable.find('**/track_a2')

        trackHeight = 0.03
        trainTrack = render.attachNewNode('trainTrack%d%d%d%d' % (x1,y1,x2,y2))
        trainTrack.setPos(x1,y1,trackHeight)

        xDiff = abs(x2-x1)
        yDiff = abs(y2-y1)
        angleInRadians = math.atan((float(y2)-y1) / (x2-x1))
        angle = rad2Deg(angleInRadians)

        # repeat our straight track as necessary to cover the distance
        desiredLength = math.sqrt( (xDiff * xDiff) + (yDiff*yDiff))
        lengthToGo = desiredLength
        partIndex = 0
        lengthCovered = 0
        while lengthToGo > self.fullLength / 2.0:
            onePart = trainPart.copyTo(trainTrack)
            onePart.setX(lengthCovered)
            lengthToGo -= self.fullLength
            lengthCovered += self.fullLength
        
        trainTrack.setH(angle)

        newX = x1 + (x2 - x1) / 2.0
        newY = y1 + (y2-y1) / 2.0

        trainTrack.setPos(x1, y1, trackHeight + zAdj)

        turnTable.removeNode()
        return trainTrack
        
    def loadGui(self):
        """
        load gui and other 2d parts of the game
        """
        scoreText = [ str(self.currentVotes[self.localAvId]),]
        
        self.gui = DirectFrame()

        self.remainingVotesFrame = DirectFrame(
            parent = self.gui,
            relief = None,
            geom = DGG.getDefaultDialogGeom(),
            geom_color = GlobalDialogColor,
            geom_scale = (7, 1, 1),
            pos = (-0.9, 0, 0.8),
            scale = 0.1,
            text = TTLocalizer.TravelGameRemainingVotes,
            text_align = TextNode.ALeft,
            text_scale = TTLocalizer.DTGRemainingVotesFrameTextScale,
            text_pos = (-3.4,-0.1, 0.0)
            )
        self.localVotesRemaining = DirectLabel(
                parent = self.remainingVotesFrame,
                relief = None,
                text = scoreText,
                text_fg = VBase4(0, 0.5, 0, 1),
                text_align = TextNode.ARight,
                text_scale = 0.7,
                pos = (3.2, 0, -0.15),
                )

        guiModel = loader.loadModel("phase_3.5/models/gui/friendslist_gui")

        self.choiceFrame = DirectFrame(
            parent = self.gui,
            relief = None,
            pos = (-0.55,0,-0.85),
            image = DGG.getDefaultDialogGeom(),
            image_scale = (1.4, 1, 0.225),
            image_color = GlobalDialogColor,
            )

        self.useLabel = DirectLabel(text = TTLocalizer.TravelGameUse,
                                    parent = self.choiceFrame,
                                    pos = (-0.59,0,-0.01),
                                    text_scale = TTLocalizer.DTGUseLabelTextScale,
                                    relief = None,
                                    )
        self.votesPeriodLabel = DirectLabel(text = TTLocalizer.TravelGameVotesWithPeriod,
                                    parent = self.choiceFrame,
                                    pos = (-0.21,0,-0.01),
                                    text_scale = TTLocalizer.DTGVotesPeriodLabelTextScale,
                                    relief = None,
                                    text_align = TextNode.ALeft,
                                    )

        self.votesToGoLabel = DirectLabel(text = TTLocalizer.TravelGameVotesToGo,
                                    parent = self.choiceFrame,
                                    pos = (-0.21,0,-0.01),
                                    text_scale = TTLocalizer.DTGVotesToGoLabelTextScale,
                                    relief = None,
                                    text_align = TextNode.ALeft,
                                    )
        
        self.upLabel = DirectLabel(text = TTLocalizer.TravelGameUp,
                                   parent = self.choiceFrame,
                                   pos = (0.31,0,-0.01),
                                   text_scale = TTLocalizer.DTGUpLabelTextScale,
                                   text_fg = Vec4(0,0,1,1),
                                   relief = None,
                                   text_align = TextNode.ALeft,
                                   )

        self.downLabel = DirectLabel(text = TTLocalizer.TravelGameDown,
                                   parent = self.choiceFrame,
                                   pos = (0.31,0,-0.01),
                                   text_scale = TTLocalizer.DTGDownLabelTextScale,
                                   text_fg = Vec4(1,0,0,1),
                                   relief = None,
                                   text_align = TextNode.ALeft,
                                   )

        self.scrollList = DirectScrolledList(
            parent = self.choiceFrame,
            relief = None,
            pos = (-0.36,0,-0.02),
            # inc and dec are DirectButtons
            incButton_image = (guiModel.find("**/FndsLst_ScrollUp"),
                               guiModel.find("**/FndsLst_ScrollDN"),
                               guiModel.find("**/FndsLst_ScrollUp_Rllvr"),
                               guiModel.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_pos = (0.0, 0.0, -0.04),
            # Make the disabled button darker
            incButton_image3_color = Vec4(0.6, 0.6, 0.6, 0.6),
            incButton_scale = (1.0, 1.0, -1.0),
            decButton_image = (guiModel.find("**/FndsLst_ScrollUp"),
                               guiModel.find("**/FndsLst_ScrollDN"),
                               guiModel.find("**/FndsLst_ScrollUp_Rllvr"),
                               guiModel.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_pos = (0.0, 0.0, 0.095),
            # Make the disabled button darker
            decButton_image3_color = Vec4(0.6, 0.6, 0.6, 0.6),
            # itemFrame is a DirectFrame
            itemFrame_pos = (0.0, 0.0, 0.0),
            itemFrame_relief = DGG.GROOVE,
            # each item is a button with text on it
            numItemsVisible = 1,
            itemMakeFunction = makeLabel,
            items = [],
            scrollSpeed = 3.0,
            itemFrame_scale = 0.1,
            command = self.scrollChoiceChanged,
            )
        self.putChoicesInScrollList()

        # Init buttons
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                       buttons.find('**/ChtBx_OKBtn_DN'),
                       buttons.find('**/ChtBx_OKBtn_Rllvr'))
        self.voteButton = DirectButton(
            parent = self.choiceFrame,
            relief = None,
            image = okImageList,
            image_scale = 3.0,
            pos = (0.85, 0, 0.0),
            text = TTLocalizer.TravelGameVoteWithExclamation,
            text_scale = TTLocalizer.DTGVoteBtnTextScale,
            text_pos = (0,0),
            command = self.handleInputChoice,
            )        

        self.waitingChoicesLabel = DirectLabel(
            text = TTLocalizer.TravelGameWaitingChoices,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.2, 0, -0.85),
            scale = 0.075)
        self.waitingChoicesLabel.hide()        

        self.gui.hide()
        
    def unload(self):
        """
        unloads the assets, should correspond to load()
        """
        self.notify.debug("unload")
        DistributedMinigame.unload(self)

        self.introMovie.finish()
        del self.introMovie

        self.gameBoard.removeNode()
        del self.gameBoard

        self.sky.removeNode()
        del self.sky

        self.trolleyCar.removeNode()
        del self.trolleyCar

        for key in self.trainSwitches.keys():
            self.trainSwitches[key].removeNode()
            del self.trainSwitches[key]
        self.trainSwitches = {}

        for key in self.tunnels.keys():
            self.tunnels[key].removeNode()
            del self.tunnels[key]
        self.tunnels = {}

        for key in self.trainTracks.keys():
            self.trainTracks[key].removeNode()
            del self.trainTracks[key]
        self.trainTracks = {}

        for trainTrack in self.extraTrainTracks:
            trainTrack.removeNode()
            del trainTrack
        self.extraTrainTracks = []

        self.gui.removeNode()
        del self.gui

        self.waitingChoicesLabel.destroy()
        del self.waitingChoicesLabel

        if self.flashWinningBeansTrack:
            self.flashWinningBeansTrack.finish()
            del self.flashWinningBeansTrack

        for label in self.minigameLabels:
            label.destroy()
            del label
        self.minigameLabels = []

        for icon in self.minigameIcons:
            icon.destroy()
            icon.removeNode()
        self.minigameIcons = []
        if hasattr(self, 'mg_icons'):
            del self.mg_icons

        for label in self.bonusLabels:
            label.destroy()
            del label
        self.bonusLabels = []

        self.scrollList.destroy()
        del self.scrollList

        self.voteButton.destroy()
        del self.voteButton
        
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        del self.music
            

    def moveCameraToTop(self):
        """
        snaps camera to top
        """
        camera.reparentTo(render)
        p = self.cameraTopView
        camera.setPosHpr(p[0], p[1], p[2], p[3], p[4], p[5])

    def moveCameraToTrolley(self):
        """
        snaps camera to facing the trolley
        """
        camera.reparentTo(self.trolleyCar)
        camera.setPos(-25, 0, 7.5)
        camera.setHpr(-90,0,0)

    def onstage(self):
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons
        
        self.notify.debug("onstage")

        # make sure we can see chat text
        NametagGlobals.setOnscreenChatForced(1)
        DistributedMinigame.onstage(self)

        self.gameBoard.reparentTo(render)
        self.sky.reparentTo(render)
        self.moveCameraToTop()

        self.trolleyCar.reparentTo(render)

        for key in self.trainSwitches.keys():
            self.trainSwitches[key].reparentTo(render)

        for key in self.trainTracks.keys():
            self.trainTracks[key].reparentTo(render)

        for trainTrack in self.extraTrainTracks:
            trainTrack.reparentTo(render)
       
        base.transitions.irisIn(0.4)
        # set the background color to match the gameboard
        base.setBackgroundColor(0.1875, 0.7929, 0)

        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.9)
        
        # play the intro movie
        self.introMovie.start()        

    def offstage(self):
        self.notify.debug("offstage")
        
        # stop the minigame; parent things to hidden, stop the
        # music...
        NametagGlobals.setOnscreenChatForced(0)

        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        
        # make sure the intro movie is finished
        self.introMovie.finish()

        self.gameBoard.hide()
        self.sky.hide()

        self.trolleyCar.hide()

        self.gui.hide()

        self.hideMinigamesAndBonuses()

        for key in self.trainSwitches.keys():
            self.trainSwitches[key].hide()

        for key in self.trainTracks.keys():
            self.trainTracks[key].hide()            

        for trainTrack in self.extraTrainTracks:
            trainTrack.hide()

        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)
        
        # show the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.start()

        # Stop music
        self.music.stop()
        
    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return
        # all of the remote toons have joined the game;
        # it's safe to show them now.

        # Make the avatars all sit in the trolley
        for index in range(self.numPlayers):
            avId = self.avIdList[index]
            name = ''
            
            # Find the actual avatar in the cr
            avatar = self.getAvatar(avId)
            if avatar:
                # Position the avatar in lane i, place 0 (the starting place)
                avatar.reparentTo(self.trolleyCar)
                # Neutral animation cycle
                avatar.animFSM.request('Sit')
                avatar.setPosHpr(-4,-4.5 + (index*3),2.8,90,0,0)
                name = avatar.getName()
                
            self.avNames.append(name)

        # put trolley car in the right position
        self.trolleyCar.setH(90)

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)

        # make sure the intro movie is finished
        self.introMovie.finish()
        
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        self.gameFSM.request("inputChoice")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterInputChoice(self):
        self.notify.debug("enterInputChoice")

        # make sure we can read the chat
        NametagGlobals.setOnscreenChatForced(1)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.hide()
        if self.timerStartTime != None:
            self.startTimer()

        # hide the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.stop()

        # show the gui now
        self.gui.show()

        self.showMinigamesAndBonuses()

    def exitInputChoice(self):
        NametagGlobals.setOnscreenChatForced(0)
        if self.timer != None:
            self.timer.destroy()
            self.timer = None
        self.timerStartTime = None
        self.gui.hide()

    def enterWaitServerChoices(self):
        """ we've voted and are waiting for other people to finish voting """
        self.notify.debug("enterWaitServerChoices")
        self.waitingChoicesLabel.show()
        self.gui.hide()

    def exitWaitServerChoices(self):
        self.waitingChoicesLabel.hide()

    def enterDisplayVotes(self, votes, directions, directionToGo, directionReason):
        """
        Display how people voted to the player, with a fancy show
        """
        assert self.notify.debugStateCall()

        if self.UseTrolleyResultsPanel:
            self.moveCameraToTrolley()
            self.hideMinigamesAndBonuses()
        else:
            self.moveCameraToTop()

        self.resultVotes = votes
        self.resultDirections = directions
        self.directionToGo = directionToGo
        self.directionReason = directionReason
        
        self.resultsStr = ''
        assert len(votes) == len(directions)
        directionTotals = [0] * TravelGameGlobals.MaxDirections
        for index in range(len(votes)):
            if index < len(self.avNames):
                avId = self.avIdList[index]
                dir = directions[index]
                numVotes = votes[index]
                directionTotals[dir] += numVotes                
                curStr = TTLocalizer.TravelGameOneToonVote % {
                    'name': self.avNames[index],
                    'numVotes' : numVotes,
                    'dir' : TTLocalizer.TravelGameDirections[dir]
                    }

                # if a player has disconnected and has zero votes, skip him
                if not ( numVotes == 0 and avId in self.disconnectedAvIds):
                    self.resultsStr += curStr
        directionStr = TTLocalizer.TravelGameTotals
        
        for index in range(len(directionTotals)):
            directionStr += ' ' + TTLocalizer.TravelGameDirections[index] + ':'
            directionStr += str(directionTotals[index])

        directionStr += '\n'
        self.resultsStr += directionStr

        reasonStr = ''
        if directionReason == TravelGameGlobals.ReasonVote:
            if directionToGo == 0:
                losingDirection = 1
            else:
                losingDirection = 0
            diffVotes = directionTotals[directionToGo] - \
                        directionTotals[losingDirection]
            reasonStr = ''
            if diffVotes > 1:
                reasonStr  = TTLocalizer.TravelGameReasonVotesPlural % {
                    'dir': TTLocalizer.TravelGameDirections[directionToGo],
                    'numVotes' : diffVotes,}
            else:
                reasonStr  = TTLocalizer.TravelGameReasonVotesSingular % {
                    'dir': TTLocalizer.TravelGameDirections[directionToGo],
                    'numVotes' : diffVotes,}
        elif directionReason == TravelGameGlobals.ReasonRandom :
            reasonStr  = TTLocalizer.TravelGameReasonRandom % {
                'dir': TTLocalizer.TravelGameDirections[directionToGo],
                'numVotes' : directionTotals[directionToGo],}
        elif directionReason == TravelGameGlobals.ReasonPlaceDecider:
            reasonStr = TravelGameReasonPlace % {
                'name' : "TODO NAME",
                'dir' : TTLocalizer.TravelGameDirections[directionToGo],}
        self.resultsStr += reasonStr
        
        self.dialog = TTDialog.TTDialog(
            text = self.resultsStr,
            command = self.__cleanupDialog,
            style = TTDialog.NoButtons,
            pos = (0,0,1)
            )
        self.dialog.hide()
        if self.UseTrolleyResultsPanel:
            self.votesPanel = VoteResultsTrolleyPanel.VoteResultsTrolleyPanel(
                len(self.avIdList),
                self.avIdList,
                votes,
                directions,
                self.avNames,
                self.disconnectedAvIds,
                directionToGo,
                directionReason,
                directionTotals,
                )
        else:
            self.votesPanel = VoteResultsPanel.VoteResultsPanel(
                len(self.avIdList),
                self.avIdList,
                votes,
                directions,
                self.avNames,
                self.disconnectedAvIds,
                directionToGo,
                directionReason,
                directionTotals,
                )
            
            
        self.votesPanel.startMovie()

        numPlayers = len(self.avIdList)
        if TravelGameGlobals.SpoofFour:
            numPlayers =4
        delay = TravelGameGlobals.DisplayVotesTimePerPlayer * (numPlayers +1)
        taskMgr.doMethodLater(delay,
                              self.displayVotesTimeoutTask,
                              self.taskName("displayVotes-timeout")) 

        # calculate the new switch we're going to
        curSwitch = TravelGameGlobals.BoardLayouts[self.boardIndex][self.currentSwitch]
        self.destSwitch = curSwitch['links'][directionToGo]
        self.updateCurrentVotes()

    def exitDisplayVotes(self):
        assert self.notify.debugStateCall()
        taskMgr.remove(self.taskName("displayVotes-timeout"))
        self.__cleanupDialog(0)
        if not self.UseTrolleyResultsPanel:
            self.showMinigamesAndBonuses()
        self.votesPanel.destroy()
        pass

    def enterMoveTrolley(self):
        """
        We've finished displaying the votes, now show the trolley moving
        """
        self.notify.debug("enterMoveTrolley")
        camera.wrtReparentTo(render)

        # How many revolutions of the wheel?
        keyAngle = round(self.TrolleyMoveDuration) * 360
        dist = Vec3(self.trainSwitches[self.destSwitch].getPos()- \
                    self.trainSwitches[self.currentSwitch].getPos()).length()
        wheelAngle = dist/(2.0 * math.pi * 0.95) * 360
        trolleyAnimateInterval = LerpFunctionInterval(
            self.animateTrolley,
            duration = self.TrolleyMoveDuration,
            blendType = "easeInOut",
            extraArgs = [keyAngle, wheelAngle],
            name = "TrolleyAnimate")     
        
        moveTrolley = Sequence()
        moveTrolley.append(Func(self.resetAnimation))
        newPos = self.trainSwitches[self.destSwitch].getPos()
        linkKey = (self.currentSwitch, self.destSwitch)
        origHeading = self.trainTracks[linkKey].getH() 
        heading = origHeading + 90
        firstTurn = Parallel()
        firstTurn.append( LerpHprInterval(self.trolleyCar, 1, Vec3(heading,0,0)))
        firstTurn.append( LerpHprInterval(self.trainSwitches[self.currentSwitch], 1, Vec3(origHeading,0,0)))
        firstTurn.append( LerpHprInterval(self.trainSwitches[self.destSwitch], 1, Vec3(origHeading,0,0)))                          
        moveTrolley.append( firstTurn)
        moveTrolley.append( Parallel(
            LerpPosInterval(self.trolleyCar, self.TrolleyMoveDuration, newPos, blendType='easeInOut'),
            trolleyAnimateInterval
            ))

        secondTurn = Parallel()
        secondTurn.append( LerpHprInterval(self.trolleyCar, 1, Vec3(90,0,0)))
        secondTurn.append( LerpHprInterval(self.trainSwitches[self.currentSwitch], 1, Vec3(0,0,0)))
        secondTurn.append( LerpHprInterval(self.trainSwitches[self.destSwitch], 1, Vec3(0,0,0)))
                          
        moveTrolley.append( secondTurn)                                     

        soundTrack = Sequence()
        trolleyExitBellInterval = Parallel(
            SoundInterval(self.trolleyBellSfx, duration=1),
            SoundInterval(self.turntableRotateSfx, duration=1, volume = 0.5)
            )
        trolleyExitAwayInterval = SoundInterval(self.trolleyAwaySfx, duration=3)
        soundTrack.append(trolleyExitBellInterval)
        soundTrack.append(trolleyExitAwayInterval)
        soundTrack.append(trolleyExitBellInterval)

        self.moveTrolleyIval = Parallel(moveTrolley, soundTrack)

        duration = self.moveTrolleyIval.getDuration()

        def focusOnTrolley(t, self = self):
            pos = self.trolleyCar.getPos()
            pos.setZ(pos.getZ() + 7.5)
            camera.lookAt(pos)
            self.lastFocusHpr = camera.getHpr()


        setRightHprTime = 0
        if self.FlyCameraUp:
            setRightHprTime = 1.0
        
        camIval1 = Parallel()
        camIval1.append(LerpFunc(focusOnTrolley,duration - setRightHprTime,
                                name='focusOnTrolley'))
        finalPos = Vec3(self.cameraTopView[0],self.cameraTopView[1],self.cameraTopView[2])
        finalHpr = Vec3(self.cameraTopView[3],self.cameraTopView[4],self.cameraTopView[5])
        if self.FlyCameraUp:
            if self.FocusOnTrolleyWhileMovingUp:
                camIval1.append(LerpPosInterval(camera,duration - setRightHprTime,
                                                finalPos,
                                                name='cameraMove'))
                camIval2 = Sequence(LerpHprInterval(camera, setRightHprTime,
                                                    finalHpr,
                                                    name='cameraHpr'))
            else:
                camIval2 = Sequence(LerpPosHprInterval(camera, setRightHprTime,
                                                       finalPos,
                                                       finalHpr,
                                                       blendType='easeIn',
                                                       name='cameraHpr'))
            camIval = Sequence( camIval1, camIval2)
        else:
            camIval = Sequence( camIval1)
        

        if self.UseTrolleyResultsPanel:
            self.moveTrolleyIval.append(camIval)

        # make sure the fsm request happens after all ivals
        temp = self.moveTrolleyIval
        self.moveTrolleyIval = Sequence(temp)
        
        if self.isLeaf(self.destSwitch):
            self.moveTrolleyIval.append( Func ( self.gameFSM.request, 'winMovie'))
        else:
            self.moveTrolleyIval.append( Func ( self.gameFSM.request, 'inputChoice'))
             
        self.moveTrolleyIval.start()

    def exitMoveTrolley(self):
        self.notify.debug("exitMoveTrolley")
        self.currentSwitch = self.destSwitch
        self.moveTrolleyIval.finish()
        self.moveCameraToTop()
        self.showMinigamesAndBonuses()
        pass

    def enterWinMovie(self):
        resultStr = TTLocalizer.TravelGamePlaying % {
            'game' : self.idToNames[self.switchToMinigameDict[self.currentSwitch]]}
        
        # if we have only 1 player left, tell them we're going to the gag shop instead.
        numToons = 0
        for avId in self.avIdList:
            if avId not in self.disconnectedAvIds:
                numToons += 1
        if numToons <= 1:
            resultStr = TTLocalizer.TravelGameGoingBackToShop
        
        reachedGoalStr = None
        localAvatarWon = False
        localAvatarLost = False
        noWinner = True
        for avId in self.avIdBonuses.keys():
            name = ''
            avatar = self.getAvatar(avId)
            if avatar:
                name = avatar.getName()
                # if we don't have a name, let's not display an empty name
                if self.avIdBonuses[avId][0] == self.currentSwitch:
                    noWinner = False
                    reachedGoalStr = TTLocalizer.TravelGameGotBonus % {
                        'name' : name,
                        'numBeans' : self.avIdBonuses[avId][1]
                        }
                    if avId == base.localAvatar.doId:
                        if not TravelGameGlobals.ReverseWin:
                            self.wonGameSfx.play()
                            bonusLabel = self.switchToBonusLabelDict[self.currentSwitch]
                            self.flashWinningBeansTrack = Sequence(
                                LerpColorScaleInterval(bonusLabel, 0.75, Vec4(0.5,1,0.5,1)),
                                LerpColorScaleInterval(bonusLabel, 0.75, Vec4(1,1,1,1)),
                                )
                            self.flashWinningBeansTrack.loop()
                        else:
                            self.lostGameSfx.play()
                    else:
                        if not TravelGameGlobals.ReverseWin:
                            self.lostGameSfx.play()
                        else:
                            self.wonGameSfx.play()
        if noWinner:
            self.noWinnerSfx.play()
            resultStr += '\n\n'
            resultStr += TTLocalizer.TravelGameNoOneGotBonus
                    
        if reachedGoalStr:
            resultStr += '\n\n'
            resultStr += reachedGoalStr
            
                                         
        self.winDialog = TTDialog.TTDialog(
            text = resultStr,
            command = self.__cleanupWinDialog,
            style = TTDialog.NoButtons)

        # create a sequence of the trolley moving out
        info = TravelGameGlobals.BoardLayouts[self.boardIndex][self.currentSwitch]
        leafX, leafY, leafZ = info['pos']
        endX = leafX + TravelGameGlobals.xInc
        heading = 90
        
        moveTrolley = Sequence()
        moveTrolley.append( LerpHprInterval(self.trolleyCar, 1, Vec3(heading,0,0)))
        moveTrolley.append( LerpPosInterval(self.trolleyCar, 3, Vec3(endX + 20, leafY, 0)))
        
        soundTrack = Sequence()
        trolleyExitBellInterval = SoundInterval(self.trolleyBellSfx, duration=1)
        trolleyExitAwayInterval = SoundInterval(self.trolleyAwaySfx, duration=3)
        soundTrack.append(trolleyExitBellInterval)
        soundTrack.append(trolleyExitAwayInterval)
        soundTrack.append(trolleyExitBellInterval)

        self.moveTrolleyIval = Parallel(moveTrolley, soundTrack)
        self.moveTrolleyIval.start()        

        delay = 8
        taskMgr.doMethodLater(delay,
                              self.gameOverCallback,
                              self.taskName("playMovie")) 
        
        
    def exitWinMovie(self):
        taskMgr.remove(self.taskName("playMovie"))
        self.moveTrolleyIval.finish()
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

    def exitCleanup(self):
        pass

    def setStartingVotes(self, startingVotesArray):
        """
        server telling us how many starting votes each avatar have
        """
        if not len(startingVotesArray) == len(self.avIdList):
            self.notify.error('length does not match, startingVotes=%s, avIdList=%s' %
                              (startingVotesArray, self.avIdList))
            return
        
        for index  in range(len( self.avIdList)):
            avId = self.avIdList[index]
            self.startingVotes[avId] = startingVotesArray[index]
            if not self.currentVotes.has_key(avId):
                self.currentVotes[avId] = startingVotesArray[index]

        self.notify.debug('starting votes = %s' % self.startingVotes)

    def startTimer(self):
        """startTimer(self)
        Starts the timer display running during the inputChoice state,
        once we have received the timerStartTime from the AI.
        """
        now = globalClock.getFrameTime()
        elapsed = now - self.timerStartTime

        self.timer.setPos(1.16, 0, -0.83)
        self.timer.setTime(TravelGameGlobals.InputTimeout)
        self.timer.countdown(TravelGameGlobals.InputTimeout - elapsed,
                             self.handleChoiceTimeout)
        self.timer.show()

    def setTimerStartTime(self, timestamp):
        """setTimeStartTime(self, int16 timestamp)

        This message is sent from the AI to indicate the point at
        which the timer starts (or started) counting.  It's used to
        synchronize the timer display with the actual countdown on the
        AI.
        """
        if not self.hasLocalToon: return
        self.timerStartTime = globalClockDelta.networkToLocalTime(timestamp)
        if self.timer != None:
            self.startTimer()        

    def handleChoiceTimeout(self):
        """ If we timeout locally, send a 0,0 for our choice """
        self.sendUpdate("setAvatarChoice", [0,0])
        self.gameFSM.request("waitServerChoices")
        pass

    def putChoicesInScrollList(self):
        """
        put the available votes in the scrollList
        """
        available = self.currentVotes[self.localAvId]
        if len(self.scrollList['items']) > 0:
            self.scrollList.removeAllItems()
        
        self.indexToVotes = {}

        index = 0
        # we need to put then in reverse order first, for the up direction
        for vote in range(available)[::-1]:
            self.scrollList.addItem(str( -(vote + 1)))
            self.indexToVotes[index] = vote+1
            index += 1

        # don't forget zero
        self.scrollList.addItem(str(0))
        self.indexToVotes[index] = 0
        self.zeroVoteIndex = index
        index +=1

        for vote in range(available):
            self.scrollList.addItem(str(vote + 1))
            self.indexToVotes[index] = vote+1
            index += 1            

        self.scrollList.scrollTo(self.zeroVoteIndex)

    def getAbsVoteChoice(self):
        """
        get an absolute number on his vote choice
        """
        available = self.currentVotes[self.localAvId]

        retval = 0
        if hasattr(self,'scrollList'):
            selectedIndex = self.scrollList.getSelectedIndex()
            if self.indexToVotes.has_key(selectedIndex):
                retval = self.indexToVotes[selectedIndex]

        return retval

    def getAbsDirectionChoice(self):
        """
        get an absolute number on his direction choice
        if we add more directions, this will need to change
        """
        selectedIndex = self.scrollList.getSelectedIndex()
        if selectedIndex < self.zeroVoteIndex:
            # we are voting to going up
            retval = 0
        elif selectedIndex == self.zeroVoteIndex:
            # not using votes
            retval = 0
        else:
            # we are voting to go down
            retval = 1 


        return retval    

    def makeTextMatchChoice(self):
        """
        show the proper text based on the number of votes, and the direction
        """
        self.votesPeriodLabel.hide()
        self.votesToGoLabel.hide()
        self.upLabel.hide()
        self.downLabel.hide()

        if not hasattr(self,'scrollList') or not hasattr(self,"zeroVoteIndex"):
            return
        
        selectedIndex = self.scrollList.getSelectedIndex()
        if selectedIndex < self.zeroVoteIndex:
            # we are voting to going up
            self.votesToGoLabel.show()
            self.upLabel.show()
        elif selectedIndex == self.zeroVoteIndex:
            # not using votes
            self.votesPeriodLabel.show()
        else:
            # we are voting to go down
            self.votesToGoLabel.show()
            self.downLabel.show()
            
        
    def scrollChoiceChanged(self):
        choiceVotes = self.getAbsVoteChoice()

        if choiceVotes == 1:
            self.votesToGoLabel['text'] = TTLocalizer.TravelGameVoteToGo
        else:
            self.votesToGoLabel['text'] = TTLocalizer.TravelGameVotesToGo
        
        available = self.currentVotes[self.localAvId]
        self.localVotesRemaining['text'] = str( available - choiceVotes)
        self.makeTextMatchChoice()

    def setAvatarChose(self, avId):
        if not self.hasLocalToon: return
        # The server is telling the client that this
        # avatar has finished choosing his number
        self.notify.debug("setAvatarChose: avatar: " + str(avId) + " choose a number")
        # TODO: represent this graphically

    def handleInputChoice(self):
        # The number we choose will be checked on the server to prevent hacking
        numVotes = self.getAbsVoteChoice()
        direction = self.getAbsDirectionChoice()
        
        self.sendUpdate("setAvatarChoice", [numVotes, direction])
        self.gameFSM.request("waitServerChoices")
 
    def setServerChoices(self, votes, directions, directionToGo, directionReason):
        if not self.hasLocalToon: return

        assert self.notify.debugStateCall()
        # The server sends this when all avatars have choosen their votes

        self.notify.debug('requesting displayVotes, curState=%s' % self.gameFSM.getCurrentState().getName())
        self.gameFSM.request("displayVotes", [votes, directions, directionToGo, directionReason])
        
    def __cleanupDialog(self, value):
        """
        cleanup the votes dialog
        """
        if (self.dialog):
            self.dialog.cleanup()
            self.dialog = None

    def displayVotesTimeoutTask(self, task):
        self.notify.debug("Done waiting for display votes")
        self.gameFSM.request('moveTrolley')
        return Task.done

    def updateCurrentVotes(self):
        """
        update the current votes, subtract what they used
        """
        for index in range(len(self.resultVotes)):
            avId = self.avIdList[index]
            oldCurrentVotes = self.currentVotes[avId]
            self.currentVotes[avId] -= self.resultVotes[index]

        self.putChoicesInScrollList()
        self.makeTextMatchChoice()

    def isLeaf(self, switchIndex):
        """
        returns True if the switch is a leaf
        """
        retval = False
        links = TravelGameGlobals.BoardLayouts[self.boardIndex][switchIndex]['links']
        if len(links) == 0:
            retval = True
        return retval

    def __cleanupWinDialog(self, value):
        """
        cleanup the win dialog
        """
        if hasattr(self,'winDialog') and self.winDialog:
            self.winDialog.cleanup()
            self.winDialog = None
    
    def gameOverCallback(self,task):
        self.__cleanupWinDialog(0)
        self.gameOver()
        return Task.done

    def setMinigames(self, switches, minigames):
        """
        we've received from the server 2 parallel arrays of switches
        and the minigame for each switch
        """
        if not self.hasLocalToon: return
 
        self.switchToMinigameDict = {}
        for index in range(len(switches)):
            switch = switches[index]
            minigame = minigames[index]
            self.switchToMinigameDict[switch] = minigame

        self.notify.debug('minigameDict = %s' % self.switchToMinigameDict)
        self.loadMinigameIcons()

    def loadMinigameIcons(self):
        """
        load an icon, if missing use a direct Label
        """
        self.mg_icons = loader.loadModel('phase_4/models/minigames/mg_icons')
        for switch in self.switchToMinigameDict.keys():
            minigame = self.switchToMinigameDict[switch]
            switchPos = self.trainSwitches[switch].getPos()
            labelPos = map3dToAspect2d(render, switchPos)
            useText = True
            iconName = None
            if minigame in IconDict.keys():
                iconName = IconDict[minigame]
            icon = None
            if self.mg_icons:
                icon = self.mg_icons.find('**/%s' % iconName)
                if not icon.isEmpty():
                    useText = False
            if labelPos:
                if useText:
                    labelPos.setZ( labelPos.getZ() -  0.1)
                    label = DirectLabel(text = self.idToNames[minigame],
                                        relief = None,
                                        scale =0.1,
                                        pos = labelPos,
                                        text_fg = (1.0,1.0,1.0,1.0),
                                        )
                    label.hide()
                    self.minigameLabels.append(label)
                else:
                    placeHolder = DirectButton(
                        image = icon,
                        relief = None,
                        text = ('','',self.idToNames[minigame],''),
                        text_scale = 0.3,
                        text_pos = (0, -0.7, 0),
                        text_fg = (1, 1, 1, 1),
                        clickSound = None,
                        pressEffect = 0,                        
                        )
                    placeHolder.setPos(labelPos)
                    placeHolder.setScale(0.2)
                    placeHolder.hide()
                    self.minigameIcons.append(placeHolder)

                    # show the yellow sign above the tunnel
                    tunnel = self.tunnels[switch]
                    sign = tunnel.attachNewNode('sign')
                    icon.copyTo(sign)
                    sign.setH(-90)
                    sign.setZ(26)
                    sign.setScale(10)

    def showMinigamesAndBonuses(self):
        for label in self.minigameLabels:
            label.show()
        for label in self.bonusLabels:
            label.show()
        for icon in self.minigameIcons:
            icon.show()            

    def hideMinigamesAndBonuses(self):
        for label in self.minigameLabels:
            label.hide()
        for label in self.bonusLabels:
            label.hide()
        for icon in self.minigameIcons:
            icon.hide()                    
                                
    def loadBonuses(self):
        self.switchToBonusLabelDict = {}
        for avId in self.avIdBonuses.keys():
            # make sure we show only this local toon's bonus
            if avId == self.localAvId:
                switch = self.avIdBonuses[avId][0]
                beans = self.avIdBonuses[avId][1]
                switchPos = self.trainSwitches[switch].getPos()
                labelPos = map3dToAspect2d(render, switchPos)
                if labelPos:
                    labelPos.setX( labelPos.getX() + 0.1)
                    labelPos.setZ( labelPos.getZ() - 0.02)
                    bonusStr = TTLocalizer.TravelGameBonusBeans % {'numBeans' : beans}
                    label = DirectLabel(text = bonusStr,
                                    relief = None,
                                    scale =0.1, # 0.85,
                                    pos = labelPos,
                                    text_fg = (1.0,1.0,1.0,1.0),
                                    text_align = TextNode.ALeft,
                                    )
                    label.hide()
                    self.bonusLabels.append(label)
                    self.switchToBonusLabelDict[switch] = label
                break
        

    def setBonuses(self, switches, beans):
        """
        server has sent the bonus beans for the leaf switches
        """
        if not self.hasLocalToon: return
 
        self.avIdBonuses = {}
        for index in range(len(self.avIdList)):
            avId = self.avIdList[index]
            switch = switches[index]
            bean = beans[index]
            self.avIdBonuses[avId] = ( switch, bean)

        self.notify.debug('self.avIdBonuses = %s' % self.avIdBonuses)

        self.loadBonuses()

    def handleDisabledAvatar(self, avId):
        """
        Code to deal with an avatar unexpectedly being deleted
        If inheritors override, they should call this base function

        we must not request frameworkAvatarExited, since
        that leads to requesting the cleanup on self.gameFSM
        """
        self.notify.warning("DistrbutedTravelGame: handleDisabledAvatar: disabled avId: " +
                            str(avId))

        self.disconnectedAvIds.append(avId)

        # instead of aborting the game, we continue on if we still have a player
        # self.frameworkFSM.request('frameworkAvatarExited')

    def setBoardIndex(self, boardIndex):
        """ server setting which of the 4 board layouts we'll use """
        self.boardIndex = boardIndex

    def getIntroMovie(self):
        """
        create an intro movie of the trolley coming to switch 0
        """
        rootInfo = TravelGameGlobals.BoardLayouts[self.boardIndex][0]
        rootX, rootY, rootZ = rootInfo['pos']
        startX = rootX - TravelGameGlobals.xInc

        heading = 90
        moveTrolley = Sequence()
        moveTrolley.append( Func( self.trolleyCar.setH, 90))
        moveTrolley.append( LerpPosInterval(self.trolleyCar, 3, Vec3(rootX, rootY, 0), startPos = Vec3(startX, rootY, 0)))        
        moveTrolley.append( LerpHprInterval(self.trolleyCar, 1, Vec3(heading,0,0)))
        
        soundTrack = Sequence()
        trolleyExitAwayInterval = SoundInterval(self.trolleyAwaySfx, duration=3)
        trolleyExitBellInterval = SoundInterval(self.trolleyBellSfx, duration=1)
        soundTrack.append(trolleyExitAwayInterval)
        soundTrack.append(trolleyExitBellInterval)

        retval = Parallel(moveTrolley, soundTrack)
        return retval

    ##### Miscellaneous support functions #####

    def animateTrolley(self, t, keyAngle, wheelAngle):
        """ Make key rotate at 1 rotation per second, and make wheels move """
        for i in range(self.numKeys):
            key = self.keys[i]
            ref = self.keyRef[i]
            key.setH(ref, t * keyAngle)
        for i in range(self.numFrontWheels):
            frontWheel = self.frontWheels[i]
            ref = self.frontWheelRef[i]
            frontWheel.setH(ref, t * wheelAngle)
        for i in range(self.numBackWheels):
            backWheel = self.backWheels[i]
            ref = self.backWheelRef[i]
            backWheel.setH(ref, t * wheelAngle)

    def resetAnimation(self):
        """ clear trolley animations """
        for i in range(self.numKeys):
            self.keys[i].setTransform(self.keyInit[i])
        for i in range(self.numFrontWheels):
            self.frontWheels[i].setTransform(self.frontWheelInit[i])
        for i in range(self.numBackWheels):
            self.backWheels[i].setTransform(self.backWheelInit[i])
