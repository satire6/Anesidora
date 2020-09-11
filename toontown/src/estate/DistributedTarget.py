from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.toonbase import ToontownTimer
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer

class DistributedTarget(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTarget")
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.geom = None
        self.numConsecutiveHits = 0
        self.enabled = 0
        self.score = 0
        self.hitTime = 0
        self.targetBounceTrack = None
        self.pinballInfo = {}
        self.pinballHiScore = 0
        self.pinballHiScorer = ""
        self.onscreenMessage = None
        self.fadeTrack = None
        
    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)
        if self.targetBounceTrack:
            self.targetBounceTrack.finish()
            self.targetBounceTrack = None
        if self.fadeTrack:
            self.fadeTrack.pause()
            self.fadeTrack = None
        self.__clearOnscreenMessage()
        pass

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.load()
        
    def load(self):
        # create the timer
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.setPos(1.1, 0, -0.15)
        self.timer.hide()
        
        # load the model
        self.geom = loader.loadModel("phase_5.5/models/estate/target")
        self.geom.reparentTo(base.cr.playGame.hood.loader.geom)
        self.geom.setPos(0, 0, 40)
        self.geom.setScale(3)
        self.geom.stash()
        self.hitSound = base.loadSfx("phase_4/audio/sfx/MG_Tag_A.mp3")
        self.rewardSound = base.loadSfx("phase_4/audio/sfx/MG_pos_buzzer.wav")

        # create a text node to display the score
        self.scoreText = TextNode("scoreText")
        self.scoreText.setTextColor(1, 0, 0, 1)
        self.scoreText.setAlign(self.scoreText.ACenter)
        self.scoreText.setFont(getSignFont())
        self.scoreText.setText("0")
        self.scoreNode = self.timer.attachNewNode(self.scoreText)
        self.scoreNode.setPos(0, 0, .35)
        self.scoreNode.setScale(.25)

        # create pinballInfo stuff
        self.curPinballScoreText = TextNode("pinballScoreText")
        self.curPinballScoreText.setTextColor(1,0,0,1)
        self.curPinballScoreText.setAlign(self.scoreText.ACenter)
        self.curPinballScoreText.setFont(getSignFont())
        self.curPinballScoreText.setText("")
        self.curPinballScoreNode = render.attachNewNode(self.curPinballScoreText)
        self.curPinballScoreNode.setPos(0.5,0.5,.30)
        self.curPinballScoreNode.setScale(.25)
        
        # setup a collision sphere
        colSphere = CollisionSphere(0,0,0,3.5)
        colSphere.setTangible(0)
        colNode = CollisionNode("targetSphere")
        colNode.addSolid(colSphere)
        colSphereNode = self.geom.attachNewNode(colNode)

        self.accept("hitTarget", self.handleHitTarget)
        self.accept("missedTarget", self.handleMissedTarget)
        #self.accept('f3-up', self.handleHitTarget)
        self.accept("entertargetSphere", self.handleEnterTarget)
        #self.accept("hitCloud", self.handleHitCloud)
        
    def delete(self):
        self.ignoreAll()

        self.scoreNode.removeNode()
        del self.scoreNode

        self.curPinballScoreNode.removeNode()
        del self.curPinballScoreNode

        self.geom.removeNode()
        del self.geom

        self.timer.destroy()
        del self.timer

        del self.rewardSound
        del self.hitSound
        DistributedObject.DistributedObject.delete(self)

    def setState(self, enabled, score, time):
        assert(self.notify.debug("setState(%s)" % enabled))

        # only need to do these on true state changes
        if self.enabled != enabled:
            if self.fadeTrack:
                self.fadeTrack.pause()

            if enabled:
                # show and fade in the target
                self.fadeTrack = Sequence(
                    Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameStart),
                    Func(self.geom.unstash),
                    Func(self.geom.lerpColorScale, Vec4(1.0, 1.0, 1.0, 0.0), Vec4(1.0, 1.0, 1.0, 1.0), 1.0),
                    Wait(1),
                    Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameInst),
                    )
            else:
                # fade out and hide the target
                self.fadeTrack = Sequence(
                    Func(self.geom.lerpColorScale, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 1.0, 1.0, 0.0), 1.0),
                    Func(self.geom.stash),
                    Func(self.hideTimer),
                    Func(base.localAvatar.setSystemMessage, 0, TTLocalizer.EstateTargetGameEnd),
                    )

            self.fadeTrack.start()
            self.enabled = enabled

        if score != self.score:
            self.setLevel(score)

        if time != self.hitTime:
            self.setTimer(time)
            
    def setReward(self, reward):
        assert(self.notify.debug("setReward"))
        # play the reward sound
        base.playSfx(self.rewardSound)
        
    def handleEnterTarget(self, collEntry):
        assert(self.notify.debug("handleEnterTarget"))
        # we walked off a cloud into the target
        self.handleHitTarget()
        
    def handleHitTarget(self, avId=None, vel=None):
        assert(self.notify.debug("handleHitTarget"))
        if not avId:
            avId = base.localAvatar.doId
        # tell the AI we hit the target and to increment the
        # number of consecutive hits
        if self.enabled:
            self.sendUpdate("setResult", [avId])

        if vel:
            # if we are provide a velocity of the avatar,
            # have the target bounce slightly in that direction, and
            # then bounce back
            if self.targetBounceTrack:
                self.targetBounceTrack.finish()
            pos = self.geom.getPos()
            dist = Vec3(vel)
            dist.normalize()
            newPos = pos - dist * 1.5
            springPos = pos + dist
            self.notify.debug("reaction distance = %s,%s,%s" % (vel[0],vel[1],vel[2]))
            self.targetBounceTrack = Sequence(LerpPosInterval( self.geom,
                                                              duration = .1,
                                                              pos = newPos,
                                                              blendType="easeOut"),
                                              LerpPosInterval( self.geom,
                                                              duration = .25,
                                                              pos = springPos,
                                                              blendType="easeOut"),
                                              LerpPosInterval( self.geom,
                                                              duration = .2,
                                                              pos = pos,
                                                              blendType="easeOut"))
            self.targetBounceTrack.start()
                                                           

    def handleMissedTarget(self):
        assert(self.notify.debug("handleMissedTarget"))
        # tell the AI we missed the target, and to reward the
        # points for consecutive hits, if any
        if self.enabled:
            self.sendUpdate("setResult", [0])

    def handleHitCloud(self):
        assert(self.notify.debug("handleHitCloud"))
        # add some small amount for hitting a cloud
        if self.enabled:
            self.sendUpdate("setBonus", [.5])
    """
    # For WeakestLink-style game
    def setLevel(self, level):
        assert(self.notify.debug("setLevel %s" % level))
        self.numConsecutiveHits = level
        brightness = level/5.0
        self.geom.setColor(0,1,brightness)
    """

    """
    # For CannonGame-style game
    def setLevel(self, level):
        self.enabled = level
        brightness = level/15.0
        self.geom.setColor(1-brightness,brightness,0)
    """

    def setLevel(self, level):
        self.notify.debug("setLevel(%s)" % level)

        # score is increasing, play the hit sound
        self.score = level
        base.playSfx(self.hitSound)

        # update score and time
        self.scoreText.setText("+" + str(int(self.score)))

    def setTimer(self, time):
        self.hitTime = time
        self.notify.debug("updateTimer(%s)" % self.enabled)
        if self.enabled:
            self.showTimer()
            self.notify.debug("hitTime = %s" % self.hitTime)
            self.timer.setTime(self.hitTime)
            self.timer.countdown(self.hitTime)

    def showTimer(self):
        # Don't show the timer if the sticker book is open
        if base.localAvatar.animFSM.getCurrentState().getName() != "ReadBook":
            # turn off message cells under timer
            base.setCellsAvailable([base.rightCells[0]], 0)
            self.timer.show()

    def hideTimer(self):
        self.timer.hide()
        # turn on message cells under timer
        base.setCellsAvailable([base.rightCells[0]], 1)

    def setPosition(self, x, y, z):
        self.geom.setPos(x,y,z)

    def showScore(self):
        scoreName = self.pinballHiScorer[0:12]
        if scoreName:
            if len(self.pinballHiScorer) > 12: 
                # indicate that the name has been truncated
                scoreName += TTLocalizer.PinballHiScoreAbbrev
        titleText = TTLocalizer.PinballHiScore % (scoreName)
        scoreText = TTLocalizer.PinballScoreHolder % (self.pinballHiScore)
        pinballEntry = self.pinballInfo.get(base.localAvatar.doId)
        if pinballEntry:
            titleText += TTLocalizer.PinballYourBestScore
            scoreText += TTLocalizer.PinballScoreHolder % (pinballEntry[0])
            titleText += TTLocalizer.PinballScore % (pinballEntry[1], pinballEntry[2])
            scoreText += TTLocalizer.PinballScoreHolder % (pinballEntry[1] * pinballEntry[2])
        self.__showOnscreenMessage(titleText, scoreText)

    def setCurPinballScore(self, avId, score, multiplier):
        self.notify.debug('setCurPinballScore %d %d %d' % (avId, score, multiplier))

        if self.pinballInfo.get(avId) == None:
            #first number is max score, 2nd is cur score, 3rd is multiplier
            self.pinballInfo[avId] = [0,0,0]

        pinballEntry = self.pinballInfo[avId]
        pinballEntry[1] = score
        pinballEntry[2] = multiplier
        curScore = score * multiplier

        if curScore > pinballEntry[0]:
            pinballEntry[0] = curScore

        if curScore > self.pinballHiScore:
            self.pinballHiScore = pinballEntry[0]
            toon = base.cr.doId2do.get(avId)
            if toon:
                self.pinballHiScorer = toon.getName()
        
        self.showScore()
        
    def b_setCurPinballScore(self, avId, score, multiplier):
        self.setCurPinballScore(avId, score, multiplier)
        self.sendUpdate( 'setCurPinballScore', [avId,score, multiplier])

    def __showOnscreenMessage(self, titleText, scoreText):
        """
        Shows a screen message.  Stays up forever unless __clearOnscreenMessage is called
        """
        self.notify.debug("----- __showOnscreenmessage")
        if not self.onscreenMessage:
            self.onscreenMessage = DirectFrame(
                relief = None,
                geom = DGG.getDefaultDialogGeom(),
                geom_color = GlobalDialogColor,
                geom_scale = (12, 1, 3),
                pos = (0, 0, 0.8),
                scale = 0.1,
                )
            titles = DirectLabel(
                parent = self.onscreenMessage,
                relief = None,
                text = titleText,
                text_fg = VBase4(0, 0, 0, 1),
                text_align = TextNode.ALeft,
                text_scale = 0.7,
                pos = (-5.75, 0, 0.5),
                )
            scores = DirectLabel(
                parent = self.onscreenMessage,
                relief = None,
                text = scoreText,
                text_fg = VBase4(1, 0, 0, 1),
                text_align = TextNode.ARight,
                text_scale = 0.7,
                pos = (5.75, 0, 0.5),
                )
            self.onscreenMessage.titles = titles
            self.onscreenMessage.scores = scores
        else:
            self.onscreenMessage.titles["text"] = titleText
            self.onscreenMessage.scores["text"] = scoreText
            
        # debug
        base.foobar = self.onscreenMessage

    def __clearOnscreenMessage(self):
        """
        Clears the screen message, if any
        """
        self.notify.debug("----- __clearOnscreenMessage")
        if self.onscreenMessage:
            self.onscreenMessage.destroy()
            self.onscreenMessage = None


    def setPinballHiScore(self, score):
        self.pinballHiScore = score
        self.showScore()

    def setPinballHiScorer(self,name):
        self.pinballHiScorer = name
        self.showScore()

    # global hide and show for sticker book
    def hideGui(self):
        if self.timer:
            self.hideTimer()
        if self.onscreenMessage:
            self.onscreenMessage.hide()

    def showGui(self):
        if self.timer:
            if self.enabled:
                self.showTimer()
        if self.onscreenMessage:
            self.onscreenMessage.show()
        
