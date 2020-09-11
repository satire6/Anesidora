#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: Contains the catch activity toon statedata.  Used by local and remote
#          avatars
#-------------------------------------------------------------------------------

from pandac.PandaModules import Vec3

from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from direct.interval.IntervalGlobal import LerpScaleInterval 
from direct.interval.IntervalGlobal import WaitInterval, ActorInterval, FunctionInterval
from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from toontown.minigame.OrthoWalk import OrthoWalk
from toontown.minigame.MinigameRulesPanel import MinigameRulesPanel
from toontown.parties import PartyGlobals
from direct.fsm import ClassicFSM, State

#from toontown.distributed.DelayDelete import DelayDelete

class PartyCatchActivityToonSD(StateData.StateData):
    """ PartyCatchActivityToonSD catching activity char anim statedata """
    notify = DirectNotifyGlobal.directNotify.newCategory("PartyCatchActivityToonSD")

    FallBackAnim     = 'slip-backward'
    FallFwdAnim      = 'slip-forward'
    CatchNeutralAnim = 'catch-neutral'
    CatchRunAnim     = 'catch-run'
    EatNeutralAnim   = 'catch-eatneutral'
    EatNRunAnim      = 'catch-eatnrun'

    animList = [FallBackAnim, FallFwdAnim,
                CatchNeutralAnim, CatchRunAnim,
                EatNeutralAnim, EatNRunAnim,
                ]

    def __init__(self, avId, activity):
        PartyCatchActivityToonSD.notify.debug("init : avId = %s, activity = %s " % (avId, activity))
        self.avId = avId
        self.activity = activity
        self.isLocal = (avId == base.localAvatar.doId)
        self.toon = self.activity.getAvatar(self.avId)
        # prevent crash during cleanup if this client exits during the activity
        self.unexpectedExit = False        

        self.fsm = ClassicFSM.ClassicFSM(
            'CatchActivityAnimFSM-%s' % self.avId,
            [
            State.State('init',
                        self.enterInit,
                        self.exitInit,
                        ['notPlaying', 'normal', 'rules', ]),
            State.State('notPlaying',
                        self.enterNotPlaying,
                        self.exitNotPlaying,
                        ['normal', 'rules', 'cleanup']),
            State.State('rules',
                        self.enterRules,
                        self.exitRules,
                        ['normal', 'cleanup']),
            State.State('normal',
                        self.enterNormal,
                        self.exitNormal,
                        ['eatFruit', 'fallBack', 'fallForward', 'notPlaying']),
            State.State('eatFruit',
                        self.enterEatFruit,
                        self.exitEatFruit,
                        ['normal', 'fallBack', 'fallForward', 'eatFruit', 'notPlaying']),
            State.State('fallBack',
                        self.enterFallBack,
                        self.exitFallBack,
                        ['normal', 'notPlaying']),
            State.State('fallForward',
                        self.enterFallForward,
                        self.exitFallForward,
                        ['normal', 'notPlaying']),
            State.State('cleanup',
                        self.enterCleanup,
                        self.exitCleanup,
                        []),
            ],
            'init',
            'cleanup',
            )
        self.enteredAlready = False

    def load(self):
        self.setAnimState('off', 1.)
        # cache the animations
        for anim in self.animList:
            self.toon.pose(anim, 0)
        
    def unload(self):
        del self.fsm

    def enter(self):
        if not self.enteredAlready:
            self.enteredAlready = True
            self.fsm.enterInitialState()
            self._exiting = False

    def exit(self, unexpectedExit = False):
        # prevent re-entry
        if self._exiting:
            return
        self._exiting = True
        self.unexpectedExit = unexpectedExit        
        
        if not self.unexpectedExit:
            self.fsm.requestFinalState()
        del self._exiting

    def enterInit(self):
        self.notify.debug('enterInit')
        self.toon.startBlink()
        self.toon.stopLookAround()
        if self.isLocal:
            self.activity.initOrthoWalk()
        self.dropShadow = self.toon.dropShadow
        # fade out the drop shadow a bit
        self.origDropShadowColor = self.dropShadow.getColor()
        c = self.origDropShadowColor
        alpha = 0.35
        self.dropShadow.setColor(c[0],c[1],c[2], alpha)

    def exitInit(self):
        pass

    def enterNotPlaying(self):
        self.toon.stopBlink()
        self.toon.startLookAround()
        self.setAnimState("neutral", 1.0)
        if self.isLocal:
            self.activity.orthoWalk.stop()
        self.dropShadow.setColor(self.origDropShadowColor)

    def exitNotPlaying(self):
        self.dropShadow = self.toon.dropShadow
        # fade out the drop shadow a bit
        self.origDropShadowColor = self.dropShadow.getColor()
        c = self.origDropShadowColor
        alpha = 0.35
        self.dropShadow.setColor(c[0],c[1],c[2], alpha)

    def enterRules(self):
        if self.isLocal:
            self.notify.debug('enterNormal')
            self.setAnimState('Catching', 1.0)
            self.activity.orthoWalk.stop()

            # show the rules panel
            # most activities show the rules as part of their FSM
            # catch is always in 'Active' state, so show the rules as part of this separate FSM

            self.accept(self.activity.rulesDoneEvent, self.handleRulesDone)
            # The rules panel is an onscreen panel
            self.rulesPanel = MinigameRulesPanel(
                "PartyRulesPanel",
                self.activity.getTitle(),
                self.activity.getInstructions(),
                self.activity.rulesDoneEvent,
                PartyGlobals.DefaultRulesTimeout,
            )
            # turn off use of all the bottom cells, and the cell nearest the bottom
            # on each side
            base.setCellsAvailable(base.bottomCells + [base.leftCells[0], base.rightCells[1]], False)
            self.rulesPanel.load()
            self.rulesPanel.enter()
        else:
            self.fsm.request('normal')

    def handleRulesDone(self):
        self.fsm.request('normal')

    def exitRules(self):
        self.setAnimState('off', 1.)
        # Hide the rules
        self.ignore(self.activity.rulesDoneEvent)
        if hasattr(self, "rulesPanel"):
            self.rulesPanel.exit()
            self.rulesPanel.unload()
            del self.rulesPanel
            
            base.setCellsAvailable(base.bottomCells + [base.leftCells[0], base.rightCells[1]], True)

    def enterNormal(self):
        self.notify.debug('enterNormal')
        self.setAnimState('Catching', 1.0)
        if self.isLocal:
            self.activity.orthoWalk.start()
        self.toon.lerpLookAt(Vec3.forward() + Vec3.up(), time=.2, blink=0)

    def exitNormal(self):
        self.setAnimState('off', 1.)
        if self.isLocal:
            self.activity.orthoWalk.stop()
        self.toon.lerpLookAt(Vec3.forward(), time=.2, blink=0)

    def eatFruit(self, fruitModel, handNode):
        """ this is a nasty little hack to work around the fact
        that FSMs will not exit/re-enter a state if you try to
        transition to the current state.
        """
        if self.fsm.getCurrentState().getName() == 'eatFruit':
            assert(self.notify.debug("eatFruit() already in eatFruit state, requesting Normal first."))
            self.fsm.request('normal')
        self.fsm.request('eatFruit', [fruitModel, handNode])

    def enterEatFruit(self, fruitModel, handNode):
        """ fruit model is placed under handNode in this state;
        this function takes ownership of the fruit model """
        self.notify.debug('enterEatFruit')
        self.setAnimState('CatchEating', 1.0)
        if self.isLocal:
            self.activity.orthoWalk.start()

        self.fruitModel = fruitModel
        # make sure the scale stays the same wrt render
        renderScale = fruitModel.getScale(render)
        fruitModel.reparentTo(handNode)
        fruitModel.setScale(render, renderScale)

        duration = self.toon.getDuration('catch-eatneutral')
        self.eatIval = Sequence(
            Parallel(WaitInterval(duration),
                     # toon eats the fruit halfway through animation
                     Sequence(LerpScaleInterval(fruitModel, duration/2.,
                                                fruitModel.getScale()*.5,
                                                blendType='easeInOut'),
                              Func(fruitModel.hide),
                              ),
                     ),
            Func(self.fsm.request, "normal"),
            name=self.toon.uniqueName('eatingIval')
            )
        self.eatIval.start()

    def exitEatFruit(self):
        # if we were to 'finish' the ival, we could run into trouble with
        # nested 'request' calls
        self.eatIval.pause()
        del self.eatIval

        self.fruitModel.reparentTo(hidden)
        self.fruitModel.removeNode()
        del self.fruitModel

        self.setAnimState('off', 1.)
        if self.isLocal:
            self.activity.orthoWalk.stop()

    def enterFallBack(self):
        self.notify.debug('enterFallBack')

        if self.isLocal:
            # play 'oof'
            base.playSfx(self.activity.sndOof)

        duration = 1.
        animName = self.FallBackAnim
        startFrame = 12
        totalFrames = self.toon.getNumFrames(animName)
        frames = (totalFrames-1) - startFrame
        frameRate = self.toon.getFrameRate(animName)
        newRate = frames / duration
        playRate = newRate / frameRate

        def resume(self=self):
            self.fsm.request('normal')

        self.fallBackIval = Sequence(
            ActorInterval(self.toon, animName, startTime=startFrame/newRate,
                          endTime=totalFrames/newRate, playRate=playRate),
            FunctionInterval(resume),
            )

        self.fallBackIval.start()

    def exitFallBack(self):
        # don't 'stop/finish' the stunnedIval; it will attempt to
        # transition to 'normal', when we're already in the process
        # of transitioning somewhere
        self.fallBackIval.pause()
        del self.fallBackIval

    def enterFallForward(self):
        self.notify.debug('enterFallForward')

        if self.isLocal:
            # play 'oof'
            base.playSfx(self.activity.sndOof)

        duration = 2.
        animName = self.FallFwdAnim
        startFrame = 12
        totalFrames = self.toon.getNumFrames(animName)
        frames = (totalFrames-1) - startFrame
        pauseFrame = 19
        frameRate = self.toon.getFrameRate(animName)
        newRate = frames / (duration * .5)
        playRate = newRate / frameRate

        def resume(self=self):
            self.fsm.request('normal')

        self.fallFwdIval = Sequence(
            ActorInterval(self.toon, animName, startTime=startFrame/newRate,
                          endTime=pauseFrame/newRate, playRate=playRate),
            WaitInterval(duration / 2.),
            ActorInterval(self.toon, animName, startTime=pauseFrame/newRate,
                          endTime=totalFrames/newRate, playRate=playRate),
            FunctionInterval(resume),
            )

        self.fallFwdIval.start()
        
    def exitFallForward(self):
        # don't 'stop/finish' the stunnedIval; it will attempt to
        # transition to 'normal', when we're already in the process
        # of transitioning somewhere
        self.fallFwdIval.pause()
        del self.fallFwdIval

    def enterCleanup(self):
        self.notify.debug('enterCleanup')
        self.toon.stopBlink()
        self.toon.startLookAround()
        if self.isLocal:
            self.activity.orthoWalk.stop()
            self.activity.destroyOrthoWalk()
        # restore the LODs
        #self.toon.resetLOD()
        self.dropShadow.setColor(self.origDropShadowColor)

    def exitCleanup(self):
        pass

    def setAnimState(self, newState, playRate):
        """Safe change the anim state of the toon."""
        if not self.unexpectedExit:
            # we do this to stop an animFSM state in flux error
            self.toon.setAnimState(newState, playRate)
        else:
            self.notify.debug("setAnimState(): Toon unexpectedExit flag is set.")
