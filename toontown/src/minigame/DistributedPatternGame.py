"""DistributedPatternGame module: contains the DistributedPatternGame class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from DistributedMinigame import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownTimer
import PatternGameGlobals
from toontown.toon import ToonHead
from toontown.char import CharDNA
from toontown.char import Char
import ArrowKeys
import random
from toontown.toonbase import ToontownGlobals
import string
from toontown.toonbase import TTLocalizer

class DistributedPatternGame(DistributedMinigame):

    phase4snd = "phase_4/audio/sfx/"

    ButtonSoundNames = (
        phase4snd + "m_match_trumpet.mp3",
        phase4snd + "m_match_guitar.mp3",
        phase4snd + "m_match_drums.mp3",
        phase4snd + "m_match_piano.mp3",
        )

    bgm = "phase_4/audio/bgm/m_match_bg1.mid"

    # Minnie dialogue
    strWatch    = TTLocalizer.PatternGameWatch
    strGo       = TTLocalizer.PatternGameGo
    strRight    = TTLocalizer.PatternGameRight
    strWrong    = TTLocalizer.PatternGameWrong
    strPerfect  = TTLocalizer.PatternGamePerfect
    strBye      = TTLocalizer.PatternGameBye

    # onscreen messages
    strWaitingOtherPlayers = TTLocalizer.PatternGameWaitingOtherPlayers
    strPleaseWait = TTLocalizer.PatternGamePleaseWait
    strRound = TTLocalizer.PatternGameRound

    # left and right are switched
    minnieAnimNames = ['up','left','down','right']
    toonAnimNames   = ['up','left','down','right',
                       'slip-forward', 'slip-backward', 'victory']

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedPatternGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['waitForServerPattern']),
                                State.State('waitForServerPattern',
                                            self.enterWaitForServerPattern,
                                            self.exitWaitForServerPattern,
                                            ['showServerPattern',
                                             'cleanup']),
                                State.State('showServerPattern',
                                            self.enterShowServerPattern,
                                            self.exitShowServerPattern,
                                            ['getUserInput',
                                             'playBackPatterns',
                                             'cleanup']),
                                State.State('getUserInput',
                                            self.enterGetUserInput,
                                            self.exitGetUserInput,
                                            ['waitForPlayerPatterns',
                                             'playBackPatterns',
                                             'cleanup']),
                                State.State('waitForPlayerPatterns',
                                            self.enterWaitForPlayerPatterns,
                                            self.exitWaitForPlayerPatterns,
                                            ['playBackPatterns',
                                             'cleanup',
                                             'checkGameOver']),
                                State.State('playBackPatterns',
                                            self.enterPlayBackPatterns,
                                            self.exitPlayBackPatterns,
                                            ['checkGameOver',
                                             'cleanup']),
                                State.State('checkGameOver',
                                            self.enterCheckGameOver,
                                            self.exitCheckGameOver,
                                            ['waitForServerPattern',
                                             'cleanup']),
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

        self.arrowColor = VBase4(1,0,0,1)
        self.xColor = VBase4(1,0,0,1)
        self.celebrate = 0
        self.oldBgColor = None
        self.trans = VBase4(1,0,0,0)
        self.opaq = VBase4(1,0,0,1)
        self.normalTextColor = VBase4(.537,.84,.33,1.)
        self.__otherToonIndex = {}

    def getTitle(self):
        return TTLocalizer.PatternGameTitle

    def getInstructions(self):
        return TTLocalizer.PatternGameInstructions

    def getMaxDuration(self):
        inputDur = PatternGameGlobals.NUM_ROUNDS * PatternGameGlobals.InputTime
        # fudge it
        return inputDur * 1.3

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)

        # create the timer
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.hide()
        
        # load the room
        self.room = loader.loadModel("phase_4/models/minigames/matching_room")

        # load sounds
        self.buttonSounds = []
        for soundName in self.ButtonSoundNames:
            self.buttonSounds.append(base.loadSfx(soundName))

        self.correctSound = base.loadSfx("phase_4/audio/sfx/MG_pos_buzzer.wav")
        self.incorrectSound = base.loadSfx(\
            "phase_4/audio/sfx/MG_neg_buzzer.wav")
        self.perfectSound = base.loadSfx("phase_4/audio/sfx/MG_win.mp3")

        self.fallSound = base.loadSfx("phase_4/audio/sfx/MG_Tag_A.mp3")

        # load music
        self.music = base.loadMusic(self.bgm)

        # create the onscreen text messages
        self.waitingText = DirectLabel(
            text = self.strPleaseWait,
            text_fg = (.9,.9,.9,1.),
            frameColor = (1,1,1,0),
            text_font = ToontownGlobals.getSignFont(),
            pos = (0,0,-.78),
            scale = .12)
                
        self.roundText = DirectLabel(
            text = self.strRound % 1,
            text_fg = self.normalTextColor,
            frameColor = (1,1,1,0),
            text_font = ToontownGlobals.getSignFont(),
            pos = (0.014, 0, -.84),
            scale = .12)
        
        self.roundText.hide()
        self.waitingText.hide()

        matchingGameGui = loader.loadModel(
            'phase_3.5/models/gui/matching_game_gui')
        minnieArrow = matchingGameGui.find("**/minnieArrow")
        minnieX = matchingGameGui.find("**/minnieX")
        minnieCircle = matchingGameGui.find("**/minnieCircle")

        # Load the arrows for above the toons' heads
        self.arrows = [None] * 5
        for x in range(0,5):
            self.arrows[x] = minnieArrow.copyTo(hidden)
            self.arrows[x].hide()
        # Load the X's for above the toons' heads
        self.xs = [None] * 5
        for x in range(0,5):
            self.xs[x] = minnieX.copyTo(hidden)
            self.xs[x].hide()
        # Load the status balls for above the toons' heads
        self.statusBalls = []
        self.totalMoves = PatternGameGlobals.INITIAL_ROUND_LENGTH + \
                          (PatternGameGlobals.ROUND_LENGTH_INCREMENT * \
                          (PatternGameGlobals.NUM_ROUNDS-1))
        for x in range(0,4):
            self.statusBalls.append([None]*self.totalMoves)
        for x in range(0,4):
            for y in range(0,self.totalMoves):
                self.statusBalls[x][y] = minnieCircle.copyTo(hidden)
                self.statusBalls[x][y].hide()

        minnieArrow.removeNode()
        minnieX.removeNode()
        minnieCircle.removeNode()
        matchingGameGui.removeNode()

        # make Minnie
        self.minnie = Char.Char()
        m = self.minnie
        dna = CharDNA.CharDNA()
        dna.newChar('mn')
        m.setDNA(dna)
        m.setName(TTLocalizer.Minnie)
        m.reparentTo(hidden)

        self.backRowHome = Point3(3,11,0)
        self.backRowXSpacing = 1.8 #3 moose

        self.frontRowHome = Point3(0,18,0)
        self.frontRowXSpacing = 3.

        # all dance step animations may not necessarily have the same
        # number of frames; pick minnie's first animation to be the
        # standard, scale other animations so that they take the same
        # amount of time to ping-pong
        self.stdNumDanceStepPingFrames = \
             self.minnie.getNumFrames(self.minnieAnimNames[0])
        self.stdNumDanceStepPingPongFrames = \
             self.__numPingPongFrames(self.stdNumDanceStepPingFrames)
        
        # how far into a played-back dance step the button gets pressed
        self.buttonPressDelayPercent = ((self.stdNumDanceStepPingFrames-1.) /
                                        self.stdNumDanceStepPingPongFrames)
        
        # speed up the animations with each successive round
        self.animPlayRates = []
        animPlayRate = 1.4
        animPlayRateMult = 1.06
        for i in range(PatternGameGlobals.NUM_ROUNDS):
            self.animPlayRates.append(animPlayRate)
            animPlayRate *= animPlayRateMult

    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)

        # get rid of the timer
        self.timer.destroy()
        del self.timer
        del self.lt
        del self.buttonSounds

        del self.music

        del self.__otherToonIndex

        del self.correctSound
        del self.incorrectSound
        del self.perfectSound
        del self.fallSound
        self.waitingText.destroy()
        del self.waitingText
        
        self.roundText.destroy()
        del self.roundText

        # Arrows is filled with arrows, when needed by minnie, yourself,
        # or other toons, they are popped out and put in arrowDict.
        # Therefore both self.arrows and self.arrowDict may have stuff in
        # them, so clean em!
        for x in self.arrowDict.values():
            x[0].removeNode()
            x[1].removeNode()
            if len(x) == 3:
                for y in x[2]:
                    y.removeNode()
        del self.arrowDict
        for x in self.arrows:
            if x:
                x.removeNode()
        del self.arrows
        for x in self.xs:
            if x:
                x.removeNode()
        del self.xs
        for x in self.statusBalls:
            if x:
                for y in x:
                    if y:
                        y.removeNode()
                        del y
        del self.statusBalls
            
        # get rid of the room model
        self.room.removeNode()
        del self.room

        self.minnie.delete()
        del self.minnie

        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)

        # self.arrowDict is created to hold arrows from self.arrows once
        # they become associated with either 'm' for minnie, 'lt' for
        # localtoon, or an avID for another player
        self.arrowDict = {}
        self.lt = base.localAvatar

        camera.reparentTo(render)
        camera.setPosHpr(0.00, -14.59, 10.56,
                         0.00, -16.39, 0.00)
        base.camLens.setFov(24.66)
        NametagGlobals.setGlobalNametagScale(0.6)

        self.arrowKeys = ArrowKeys.ArrowKeys()

        self.room.reparentTo(render)
        self.room.setPosHpr(0.0, 18.39, -ToontownGlobals.FloorOffset,
                            0.00, 0.00, 0.00)
        self.room.setScale(1)


        # make sure the dance animations are cached for minnie and localToon
        for anim in self.minnieAnimNames:
            self.minnie.pose(anim, 0)
        for anim in self.toonAnimNames:
            self.lt.pose(anim, 0)

        # calc the speed multipliers for each animation
        self.minnieAnimSpeedMult = {}
        self.toonAnimSpeedMult = {}

        for anim in self.minnieAnimNames:
            numFrames = self.minnie.getNumFrames(anim)
            self.minnieAnimSpeedMult[anim] = \
                 (float)(self.__numPingPongFrames(numFrames)) / \
                 (float)(self.stdNumDanceStepPingPongFrames)
        for anim in self.toonAnimNames:
            numFrames = self.lt.getNumFrames(anim)
            self.toonAnimSpeedMult[anim] = \
                 (float)(self.__numPingPongFrames(numFrames)) / \
                 (float)(self.stdNumDanceStepPingPongFrames)

        # show local toon
        lt = self.lt
        lt.reparentTo(render)
        lt.useLOD(1000)
        lt.setPos(-3.5, 11, 0.00)
        lt.setScale(1)
        self.makeToonLookatCamera(lt)
        lt.loop('neutral')
        lt.startBlink()
        lt.startLookAround()

        self.arrowDict['lt'] = [self.arrows.pop(), self.xs.pop(),
                                self.statusBalls.pop()]
        jj = self.lt.nametag3d
        for k in range(0,2):
            self.arrowDict['lt'][k].setBillboardAxis()
            self.arrowDict['lt'][k].setBin('fixed', 100)
            # Parent it to the nametag joint
            self.arrowDict['lt'][k].reparentTo(jj)
            if k==0:
                self.arrowDict['lt'][k].setScale(2.5)
                self.arrowDict['lt'][k].setColor(self.arrowColor)
            else:
                self.arrowDict['lt'][k].setScale(4,4,4)
                self.arrowDict['lt'][k].setColor(self.xColor)
            self.arrowDict['lt'][k].setPos(0,0,1)
        self.formatStatusBalls(self.arrowDict['lt'][2], jj)
        
        # show minnie
        m = self.minnie
        m.reparentTo(render)
        m.setPos(-1.6, 20, 0)
        m.setScale(1)
        self.makeToonLookatCamera(m)
        m.loop('neutral')
        m.startBlink()
        # Activate Minnie's nametag, so we can see what she's saying.
        self.minnie.nametag.manage(base.marginManager)
        self.minnie.startEarTask()
        # But we don't want to be able to pick her
        self.minnie.setPickable(0)
        # And we don't want her speech bubble to extend offscreen.
        self.minnie.nametag.getNametag3d().setChatWordwrap(8)

        self.arrowDict['m'] = [self.arrows.pop(), self.xs.pop()]#, self.statusBalls.pop()]
        jj = self.minnie.nametag3d
        for k in range(0, 2):
            self.arrowDict['m'][k].setBillboardAxis()
            self.arrowDict['m'][k].setBin('fixed', 100)
            # Parent it to the nametag joint
            self.arrowDict['m'][k].setColor(self.arrowColor)
            self.arrowDict['m'][k].reparentTo(jj)
            self.arrowDict['m'][k].setScale(4)
            self.arrowDict['m'][k].setPos(0,0,1.7)
        # Start music
        base.playMusic(self.music, looping = 1, volume = 1)

    def offstage(self):
        self.notify.debug("offstage")
        DistributedMinigame.offstage(self)

        # Stop music
        self.music.stop()
        
        base.camLens.setFov(ToontownGlobals.DefaultCameraFov)
        NametagGlobals.setGlobalNametagScale(1.0)
        
        self.arrowKeys.destroy()
        del self.arrowKeys

        self.room.reparentTo(hidden)

        self.roundText.hide()
        self.minnie.nametag.unmanage(base.marginManager)
        self.minnie.stopEarTask()
        self.minnie.stop()
        self.minnie.stopBlink()
        self.minnie.reparentTo(hidden)

        # reset scalings!
        self.lt.setScale(1)
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                toon.setScale(1)
            
        # reset the toons' LODs
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.resetLOD()
                
                # Also reset the anim play rates.
                for anim in self.toonAnimNames:
                    av.setPlayRate(1.0, anim)

    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return

        # show the remote toons
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            
            if toon:
                self.arrowDict[avId] = [self.arrows.pop(), self.xs.pop(),
                                        self.statusBalls.pop()]
                jj = toon.nametag3d
                for k in range(0, 2):
                    self.arrowDict[avId][k].setBillboardAxis()
                    self.arrowDict[avId][k].setBin('fixed', 100)
                    # Parent it to the nametag joint
                    self.arrowDict[avId][k].reparentTo(jj)
                    if k==0:
                        self.arrowDict[avId][k].setScale(2.5)
                        self.arrowDict[avId][k].setColor(self.arrowColor)
                    else:
                        self.arrowDict[avId][k].setScale(4,4,4)
                        self.arrowDict[avId][k].setColor(self.xColor)
                    # self.arrowDict[avId][k].setScale(1+k*5)
                    self.arrowDict[avId][k].setPos(0,0,1)
                self.formatStatusBalls(self.arrowDict[avId][2], jj)
                
                toon.reparentTo(render)
                toon.useLOD(1000)
                toon.setPos(self.getBackRowPos(avId))
                toon.setScale(.9)
                self.makeToonLookatCamera(toon)

                # make sure the dance animations are cached for this toon
                for anim in self.toonAnimNames:
                    toon.pose(anim, 0)

                toon.loop('neutral')

        if self.isSinglePlayer():
            self.waitingText['text'] = self.strPleaseWait
        else:
            self.waitingText['text'] = self.strWaitingOtherPlayers

        # this will hold the animation tracks for the toons
        # so that we can stop them on unexpected termination
        self.animTracks = {}
        for avId in self.avIdList:
            self.animTracks[avId] = None

        self.__initGameVars()

    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        self.gameFSM.request("waitForServerPattern")

    def __initGameVars(self):
        self.round = 0
        self.perfectGame = 1

    def __numPingPongFrames(self, numFrames):
        return (numFrames * 2) - 1

    def makeToonLookatCamera(self, toon):
        toon.headsUp(camera)

    def setText(self, t, newtext):
        t['text'] = newtext

    def setTextFG(self, t, fg):
        t['text_fg'] = fg

    def getWalkTrack(self, toon, posList, startPos=None,
                     lookAtCam = 1, endHeading = 180):
        """ creates a 'walk track' for the toon
        walks from current position to endPos
        if lookAtCam, toon turns to the camera once at destination
        else, toon turns to endHeading once at destination
        """
        walkSpeed = 7

        origPos = toon.getPos()
        origHpr = toon.getHpr()
        
        # start walkin'
        track = Sequence(
            Func(toon.loop, 'run'),
            )
        
        if startPos:
            toon.setPos(startPos)
            track.append(
                Func(toon.setPos, startPos)
                )
        
        for endPos in posList:
            # face the destination
            toon.headsUp(Point3(endPos))
            track.append(
                Func(toon.setHpr, Point3(toon.getH(),0,0))
                )

            lastPos = toon.getPos()
            distance = Vec3(endPos - lastPos).length()
            duration = distance / walkSpeed

            toon.setPos(endPos)

            # walk to the end pos
            track.append(
                LerpPosInterval(toon, duration=duration,
                                pos=Point3(endPos),
                                startPos=Point3(lastPos))
                )

        if lookAtCam:
            saveHpr = toon.getHpr()
            toon.headsUp(camera)
            endHeading = toon.getHpr()[0]
            toon.setHpr(saveHpr)

        # make sure the end heading is not more than 180 degrees
        # from the current heading
        curHeading = toon.getH()
        if ((endHeading - curHeading) > 180.):
            endHeading -= 360
        elif ((endHeading - curHeading) < -180.):
            endHeading += 360

        # make the toon look in the right direction
        endHpr = Point3(endHeading,0,0)
        duration = (abs(endHeading - curHeading)/180.) * .3
        track.extend([
            Func(toon.loop, 'walk'),
            LerpHprInterval(toon, duration, endHpr),
            Func(toon.loop, 'neutral'),
            ])

        toon.setPos(origPos)
        toon.setHpr(origHpr)

        return track

    # these functions are used to animate a single dance step
    # (animation, button press, and sound, each separate)
    def getDanceStepDuration(self):

        numFrames = self.stdNumDanceStepPingPongFrames

        # NOTE: toon.getFrameRate may return a negative value
        return numFrames / \
               abs(self.animPlayRate * \
                   self.minnieAnimSpeedMult[self.minnieAnimNames[0]] * \
                   self.minnie.getFrameRate(self.minnieAnimNames[0]))

    def __getDanceStepAnimTrack(self, toon, anim, speedScale):
        # ping-pong out X frames and back
        numFrames = toon.getNumFrames(anim)
        return Sequence(
            Func(toon.pingpong, anim, fromFrame = 0, toFrame = numFrames-1),
            Wait(self.getDanceStepDuration()),
            )

    def __getMinnieDanceStepAnimTrack(self, minnie, direction):
        animName = self.minnieAnimNames[direction]
        return self.__getDanceStepAnimTrack(minnie, animName,
                                            self.minnieAnimSpeedMult[animName])

    def __getToonDanceStepAnimTrack(self, toon, direction):
        animName = self.toonAnimNames[direction]
        return self.__getDanceStepAnimTrack(toon, animName,
                                            self.toonAnimSpeedMult[animName])

    def getDanceStepButtonSoundTrack(self, index):
        duration = self.getDanceStepDuration()
        wait = duration * self.buttonPressDelayPercent
        return Sequence(
            Wait(wait),
            Func(base.playSfx, self.__getButtonSound(index)),
            Wait(duration - wait),
            )

    # these functions create entire tracks for a dance sequence
    # (animation, button press, and sound, each separate)

    def getDanceArrowAnimTrack(self, toonID, pattern, speedy):
        track = Sequence()
        track.append(Func(self.showArrow, toonID))
        for buttonIndex in pattern:
            track.append(self.getDanceArrowSingleTrack(toonID,
                                                       buttonIndex, speedy))
        track.append(Func(self.hideArrow, toonID))
        return track

    def changeArrow(self, toonID, index):
        self.arrowDict[toonID][0].setR(-(90 - 90*index))
        
    def showArrow(self, toonID):
        self.arrowDict[toonID][0].show()

    def hideArrow(self, toonID):
        self.arrowDict[toonID][0].hide()

    def showX(self, toonID):
        self.arrowDict[toonID][1].show()

    def hideX(self, toonID):
        self.arrowDict[toonID][1].hide()

    def celebrated(self):
        self.celebrate = 1

    def returnCelebrationIntervals(self, turnOn):
        ri = []
        if turnOn:
            ri.append(ActorInterval(actor=self.lt, animName = 'victory', duration=5.5))
        else:
            ri.append(Func(self.lt.loop, 'neutral'))
        for avId in self.remoteAvIdList:
            toon = self.getAvatar(avId)
            if toon:
                if turnOn:
                    ri.append(ActorInterval(actor=toon, animName = 'victory', duration=5.5))
                else:
                    ri.append(Func(toon.loop, 'neutral'))
        if len(self.remoteAvIdList)==0:
            return ri
        else:
            return Parallel(ri)

    def formatStatusBalls(self, sb, jj):
        for x in range(0,self.totalMoves):
            sb[x].setBillboardAxis()
            sb[x].setBin('fixed', 100)
            sb[x].reparentTo(jj)
            sb[x].setScale(1)
            xpos = +(int(self.totalMoves/2)*.25) - (.25*x)
            sb[x].setPos(xpos,0,.3)
            
    def showStatusBalls(self, toonID):
        sb = self.arrowDict[toonID][2]
        for x in range(0, len(self.__serverPattern)):
            sb[x].setColor(1,1,1,1)
            sb[x].show()

    def hideStatusBalls(self, toonID):
        sb = self.arrowDict[toonID][2]
        for x in range(0, len(sb)):
            sb[x].hide()

    def colorStatusBall(self, toonID, which, good):
        if good:
            self.arrowDict[toonID][2][which].setColor(0,1,0,1)
        else:
            self.arrowDict[toonID][2][which].setColor(1,0,0,1)
    
    def getDanceArrowSingleTrack(self, toonID, index, speedy):
        duration = self.getDanceStepDuration()
        wait = duration * self.buttonPressDelayPercent
        d = duration-wait
        if speedy:
            track = Sequence(
                Func(self.changeArrow, toonID, index),
                Wait(wait)
                )
        else:
            track = Sequence(
                Func(self.changeArrow, toonID, index),
                Wait(wait),
                LerpColorInterval(self.arrowDict[toonID][0], d, self.trans, self.opaq)
                )
        return track
         
 
    def getDanceSequenceAnimTrack(self, toon, pattern):
        getDanceStepTrack = self.__getToonDanceStepAnimTrack
        if toon == self.minnie:
            getDanceStepTrack = self.__getMinnieDanceStepAnimTrack

        tracks = Sequence()
        for direction in pattern:
            tracks.append(getDanceStepTrack(toon,direction))
        if len(pattern):
            tracks.append(Func(toon.loop, 'neutral'))
        #else:
        #    # put in a dummy interval to keep the interval system happy
        #    tracks.append(Wait(0.1))
        return tracks

    def getDanceSequenceButtonSoundTrack(self, pattern):
        track = Sequence()
        for buttonIndex in pattern:
            track.append(self.getDanceStepButtonSoundTrack(buttonIndex))
        return track

    # these functions specify locations where toons should stand
    def __getRowPos(self, rowHome, xSpacing, index, numSpots):
        xOffset = (xSpacing * index) - \
                  ((xSpacing * (numSpots-1))/2.)
        return rowHome + Point3(xOffset,0,0)

    def getBackRowPos(self, avId):
        assert avId != self.localAvId
        index = self.remoteAvIdList.index(avId)
        return self.__getRowPos(self.backRowHome, self.backRowXSpacing,
                                index, len(self.remoteAvIdList))

    def getFrontRowPos(self, avId):
        index = self.avIdList.index(avId)
        return self.__getRowPos(self.frontRowHome, self.frontRowXSpacing,
                                index, len(self.avIdList))

    # make minnie talk
    def __setMinnieChat(self, str, giggle):
        # there may or may not be a %s in the string; replace with
        # toon name
        str = string.replace(str, "%s",
                             self.getAvatar(self.localAvId).getName())
        self.minnie.setChatAbsolute(str, CFSpeech)
        if giggle:
            self.minnie.playDialogue("statementA", 1)

    # make minnie shut up
    def __clearMinnieChat(self):
        self.minnie.clearChat()

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterWaitForServerPattern(self):
        self.notify.debug("enterWaitForServerPattern")

        # tell the server we're ready for the next round
        # and wait for the server to send the next pattern
        self.sendUpdate("reportPlayerReady", [])

        #self.waitingText.show()

    def setPattern(self, pattern):
        if not self.hasLocalToon: return
        self.notify.debug("setPattern: " + str(pattern))
        self.__serverPattern = pattern
        self.gameFSM.request("showServerPattern")

    def exitWaitForServerPattern(self):
        pass #self.waitingText.hide()

    def enterShowServerPattern(self):
        self.notify.debug("enterShowServerPattern")

        # update the round counter
        self.round += 1
        self.roundText.show()
        self.roundText.setScale(0.12)        
        self.roundText['text'] = self.strRound % self.round
        
        self.animPlayRate = self.animPlayRates[self.round-1]

        # Speed everybody up
        for avId in self.avIdList:
            toon = self.getAvatar(avId)
            if toon:
                for anim in self.toonAnimNames:
                    toon.setPlayRate(
                        self.animPlayRate * self.toonAnimSpeedMult[anim],
                        anim)
        # Don't forget minnie
        for anim in self.minnieAnimNames:
            self.minnie.setPlayRate(
                self.animPlayRate * self.minnieAnimSpeedMult[anim],
                anim)

        # we have to show the user the pattern that the
        # server has sent us
        text = self.strWatch

        danceTrack  = self.getDanceSequenceAnimTrack(self.minnie,
                                                     self.__serverPattern)
        arrowTrack = self.getDanceArrowAnimTrack('m',
                                                 self.__serverPattern,0)
        #buttonTrack = self.getDanceSequenceButtonPressTrack(
        #                                              self.__serverPattern)
        soundTrack  = self.getDanceSequenceButtonSoundTrack(
                                                      self.__serverPattern)
        self.showTrack = Sequence(
            Func(self.__setMinnieChat, text, 1),
            Wait(.5),
            Parallel(danceTrack,
                     #buttonTrack,
                     soundTrack,
                     arrowTrack,
                     ),
            Wait(.2),
            Func(self.__clearMinnieChat),
            Func(self.gameFSM.request, "getUserInput"),
            )
        self.showTrack.start()

    def exitShowServerPattern(self):
        if self.showTrack.isPlaying():
            self.showTrack.pause()
        del self.showTrack

    def enterGetUserInput(self):
        self.notify.debug("enterGetUserInput")

        self.setupTrack   = None
        self.proceedTrack = None

        def startTimer(self=self):
            self.currentStartTime = globalClock.getFrameTime()
            self.timer.show()
            self.timer.countdown(PatternGameGlobals.InputTime,
                                 self.__handleInputTimeout)

        def enableKeys(self=self):
            def keyPress(self, index):
                self.__pressHandler(index)
            def keyRelease(self, index):
                self.__releaseHandler(index)
            self.arrowKeys.setPressHandlers([
                lambda self=self,keyPress=keyPress: keyPress(self,0),
                lambda self=self,keyPress=keyPress: keyPress(self,2),
                lambda self=self,keyPress=keyPress: keyPress(self,3),
                lambda self=self,keyPress=keyPress: keyPress(self,1),
                ])
            self.arrowKeys.setReleaseHandlers([
                lambda self=self,keyRelease=keyRelease: keyRelease(self,0),
                lambda self=self,keyRelease=keyRelease: keyRelease(self,2),
                lambda self=self,keyRelease=keyRelease: keyRelease(self,3),
                lambda self=self,keyRelease=keyRelease: keyRelease(self,1),
                ])

        self.__localPattern = []
        self.__otherToonIndex.clear()

        self.showStatusBalls('lt')
        for avId in self.remoteAvIdList:
            self.showStatusBalls(avId)
            self.__otherToonIndex[avId] = 0
            
        self.setupTrack = Sequence(
            Func(self.__setMinnieChat, self.strGo, 0),
            #Func(self.setTextFG, self.roundText, self.opaq),
            Func(self.setText, self.roundText, TTLocalizer.PatternGameGo),
            Func(self.roundText.setScale, .3),
            Func(enableKeys),
            Func(startTimer),
            Wait(.8),
            Func(self.__clearMinnieChat),
            Func(self.setText, self.roundText, ' '),
            Func(self.roundText.setScale, .12),
            Func(self.setTextFG, self.roundText, self.normalTextColor)
            )
        self.setupTrack.start()

    def __handleInputTimeout(self):
        # tell the server that we did not get the pattern right
        self.__doneGettingInput(self.__localPattern)

    # these are callbacks from the local pattern pad for
    # when the buttons are pressed and released
    def __pressHandler(self, index):
        # process the button press
        self.__buttonPressed(index)
    def __releaseHandler(self, index):
        pass

    # a remote player has pressed a button
    def remoteButtonPressed(self, avId, index, wrong):
        if not self.hasLocalToon: return
        if not (self.gameFSM.getCurrentState().getName() in
                ['getUserInput', 'waitForPlayerPatterns',]):
            return
        if avId != self.localAvId:
            if self.animTracks[avId]:
                self.animTracks[avId].finish()

            av = self.getAvatar(avId)

            if wrong:
                acts = ['slip-forward', 'slip-backward']
                ag = random.choice(acts)
                self.arrowDict[avId][0].hide()
                self.animTracks[avId] = Sequence(
                    Func(self.showX, avId),
                    Func(self.colorStatusBall, avId,
                         self.__otherToonIndex[avId], 0),
                    ActorInterval(actor=av, animName = ag, duration=2.35),
                    Func(av.loop, 'neutral'),
                    Func(self.hideX, avId),
                    )
            else:
                self.colorStatusBall(avId, self.__otherToonIndex[avId], 1)
                arrowTrack  = self.getDanceArrowAnimTrack(avId, [index], 1)
                potTrack  = self.getDanceSequenceAnimTrack(av, [index])
                self.animTracks[avId] = Parallel(potTrack, arrowTrack)

            self.__otherToonIndex[avId] += 1
            self.animTracks[avId].start()

    def __getButtonSound(self, index):
        return self.buttonSounds[index]


    def __buttonPressed(self, index):
        # if we've got a full local pattern, ignore this event; kinda dirty
        if len(self.__localPattern) >= len(self.__serverPattern):
            return

        ## get a dance sequence with a single dance step
        if self.animTracks[self.localAvId]:
            self.animTracks[self.localAvId].finish()

        badd = 0
        if index != self.__serverPattern[len(self.__localPattern)]:
            # Your current dance step is not correct, fall and end your turn!
            badd = 1
            acts = ['slip-forward', 'slip-backward']
            ag = random.choice(acts)
        
            self.animTracks[self.localAvId] = Sequence(
                Func(self.showX, 'lt'),
                Func(self.colorStatusBall, 'lt', len(self.__localPattern), 0),
                ActorInterval(actor=self.lt, animName = ag, duration=2.35),
                Func(self.lt.loop, 'neutral'),
                Func(self.hideX, 'lt'),
                )
            self.arrowDict['lt'][0].hide()
            base.playSfx(self.fallSound)
        else:
            # You did good, load in the dance step
            self.colorStatusBall('lt', len(self.__localPattern), 1)
            base.playSfx(self.__getButtonSound(index))
            arrowTrack = self.getDanceArrowAnimTrack('lt', [index], 1)
            potTrack = self.getDanceSequenceAnimTrack(self.lt, [index])
            self.animTracks[self.localAvId] = Parallel(potTrack,
                                                       arrowTrack)
            
        # let everyone else know
        self.sendUpdate("reportButtonPress", [index, badd])
        
        self.animTracks[self.localAvId].start()    
        self.__localPattern.append(index)
        
        if len(self.__localPattern) == len(self.__serverPattern) or badd:
            self.__doneGettingInput(self.__localPattern)

    def __doneGettingInput(self, pattern):
        # don't allow any more presses
        self.arrowKeys.setPressHandlers(self.arrowKeys.NULL_HANDLERS)
        self.currentTotalTime = (globalClock.getFrameTime() -
                                 self.currentStartTime)
        self.proceedTrack = Sequence(
            Wait(self.getDanceStepDuration()),
            Func(self.sendUpdate, "reportPlayerPattern",
                 [pattern, self.currentTotalTime]),
            Func(self.gameFSM.request, "waitForPlayerPatterns"),
            )
        self.proceedTrack.start()

    def exitGetUserInput(self):
        self.timer.stop()
        self.timer.hide()

        self.arrowKeys.setPressHandlers(self.arrowKeys.NULL_HANDLERS)
        self.arrowKeys.setReleaseHandlers(self.arrowKeys.NULL_HANDLERS)

        if self.setupTrack and self.setupTrack.isPlaying():
            self.setupTrack.pause()
        if self.proceedTrack and self.proceedTrack.isPlaying():
            self.proceedTrack.pause()

        del self.setupTrack
        del self.proceedTrack

        self.__clearMinnieChat()

    def enterWaitForPlayerPatterns(self):
        self.notify.debug("enterWaitForPlayerPatterns")
        #self.waitingText.show()

    def setPlayerPatterns(self, pattern1, pattern2,
                          pattern3, pattern4, fastestAvId):
        """this call gives us all players' patterns
        if we have less than 4 players, extra params will be empty lists"""
        if not self.hasLocalToon: return
        self.fastestAvId = fastestAvId
        
        self.notify.debug("setPlayerPatterns:"
                          + " pattern1:" + str(pattern1)
                          + " pattern2:" + str(pattern2)
                          + " pattern3:" + str(pattern3)
                          + " pattern4:" + str(pattern4))

        self.playerPatterns = {}
        patterns = [pattern1,pattern2,pattern3,pattern4]
        for i in range(len(self.avIdList)):
            self.playerPatterns[self.avIdList[i]] = patterns[i]

        self.gameFSM.request('playBackPatterns')

    def exitWaitForPlayerPatterns(self):
        self.waitingText.hide()

        # stop any toon animations
        #for track in self.animTracks.values():
        #    if track:
        #        if track.isPlaying():
        #            track.finish()

    def enterPlayBackPatterns(self):
        self.notify.debug("enterPlayBackPatterns")
        if self.fastestAvId == self.localAvId:
            self.roundText.setScale(0.1)
            if(self.numPlayers != 2):
                self.roundText['text'] = TTLocalizer.PatternGameFastest
            else:
                self.roundText['text'] = TTLocalizer.PatternGameFaster
            jumpTrack = Sequence(
                ActorInterval(actor=self.lt, animName = 'jump', duration=1.7),
                Func(self.lt.loop, 'neutral'))
        elif self.fastestAvId == 0:
            if self.round == PatternGameGlobals.NUM_ROUNDS:
                self.roundText['text'] = " "
            else:
                self.roundText.setScale(0.1)
                self.roundText['text'] = TTLocalizer.PatternGameYouCanDoIt
            jumpTrack = Sequence(Wait(.5),Wait(.5))
        elif self.fastestAvId == 1:
            self.roundText.setScale(0.1)
            self.roundText['text'] = TTLocalizer.PatternGameGreatJob
            jumpTrack = Sequence(Wait(.5),Wait(.5))
        else:
            self.roundText.setScale(0.08)
            av = self.getAvatar(self.fastestAvId)
            jumpTrack = Sequence(ActorInterval(actor=av,
                                               animName='jump', duration=1.7),
                                 Func(av.loop, 'neutral'))
            if(self.numPlayers != 2):
                rewardStr = TTLocalizer.PatternGameOtherFastest
            else:
                rewardStr = TTLocalizer.PatternGameOtherFaster
            self.roundText['text'] = av.getName() + rewardStr

        # minnie reacts
        success = (self.playerPatterns[self.localAvId] == self.__serverPattern)

        self.hideStatusBalls('lt')
        for avId in self.remoteAvIdList:
            self.hideStatusBalls(avId)
            
        if success:
            sound = self.correctSound
            text = self.strRight
        else:
            self.perfectGame = 0
            sound = self.incorrectSound
            text = self.strWrong

        soundTrack = Sequence(
            Func(base.playSfx, sound),
            Wait(1.6),
            )
        textTrack = Sequence(
            Wait(.2),
            Func(self.__setMinnieChat, text, 0),
            Wait(1.3),
            Func(self.__clearMinnieChat),
            )

        self.playBackPatternsTrack = Sequence(
            Parallel(soundTrack,
                     textTrack,
                     jumpTrack),
            Func(self.gameFSM.request, 'checkGameOver'),
            )
        self.playBackPatternsTrack.start()

    def exitPlayBackPatterns(self):
        if self.playBackPatternsTrack.isPlaying():
            self.playBackPatternsTrack.pause()
        del self.playBackPatternsTrack

    def enterCheckGameOver(self):
        self.notify.debug("enterCheckGameOver")
        self.__winTrack = None
        
        if self.round < PatternGameGlobals.NUM_ROUNDS:
            self.gameFSM.request('waitForServerPattern')
        else:
            text = self.strBye
            sound = None
            delay = 2.
            if self.perfectGame:
                text = self.strPerfect
                sound = self.perfectSound
                delay = 2.2
            if self.celebrate:
                text = TTLocalizer.PatternGameImprov
                self.__winTrack = Sequence(
                    Func(self.__setMinnieChat, text, 1),
                    Func(base.playSfx, self.perfectSound),
                    Sequence(self.returnCelebrationIntervals(1)),
                    #Wait(4),
                    Sequence(self.returnCelebrationIntervals(0)),
                    Func(self.__clearMinnieChat),
                    Func(self.gameOver),
                    )
            else:
                self.__winTrack = Sequence(
                    Func(self.__setMinnieChat, text, 1),
                    Func(base.playSfx, sound),
                    Wait(delay),
                    Func(self.__clearMinnieChat),
                    Func(self.gameOver),
                    )
            self.__winTrack.start()

    def exitCheckGameOver(self):
        if self.__winTrack and self.__winTrack.isPlaying():
            self.__winTrack.pause()
        del self.__winTrack

    def enterCleanup(self):
        self.notify.debug("enterCleanup")

        for track in self.animTracks.values():
            if track and track.isPlaying():
                track.pause()
        del self.animTracks

    def exitCleanup(self):
        pass
