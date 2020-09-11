"""Stomper module: contains the Stomper class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.showbase.PythonUtil import lerp
from direct.fsm import StateData
import math

class Stomper(StateData.StateData, NodePath):
    SerialNum = 0

    MotionLinear = 0
    MotionSinus = 1
    MotionHalfSinus = 2

    DefaultStompSound = 'phase_5/audio/sfx/AA_drop_safe.mp3'

    def __init__(self,
                 model,
                 range=5.,  # range of motion in feet along Z-axis
                 period=1., # duration of full cycle
                 phaseShift=0.,  # 0..1 phase shift
                 zOffset=0., # how close the stomper should get to Z=0
                 motionType=None,
                 shadow=None,
                 sound=None,
                 soundLen=None,
                 ):
        StateData.StateData.__init__(self, 'StomperDone')

        self.SerialNum = Stomper.SerialNum
        Stomper.SerialNum += 1

        # get the stomp sound
        self.sound = sound
        self.soundLen = soundLen
        if self.sound is not None:
            self.sound = base.loadSfx(sound)

        self.motionType = motionType
        if self.motionType is None:
            self.motionType = Stomper.MotionSinus

        node = hidden.attachNewNode('Stomper%s' % self.SerialNum)
        NodePath.__init__(self, node)

        self.model = model.copyTo(self)

        self.shadow = shadow
        if shadow is not None:
            self.shadow = shadow.copyTo(self)
            self.shadow.setPos(0,0,.2)

        self.TaskName = 'Stomper%sTask' % self.SerialNum

        self.range = range
        self.zOffset = zOffset
        self.period = period
        self.phaseShift = phaseShift

    def destroy(self):
        self.removeNode()

    def enter(self, startTime):
        # stomper should hit at t=0
        if self.motionType is Stomper.MotionLinear:
            motionIval = Sequence(
                LerpPosInterval(self.model, self.period/2.,
                                Point3(0,0,self.zOffset+self.range),
                                startPos=Point3(0,0,self.zOffset)),
                WaitInterval(self.period/4.),
                LerpPosInterval(self.model, self.period/4.,
                                Point3(0,0,self.zOffset),
                                startPos=Point3(0,0,self.zOffset+self.range)),
                )
        elif self.motionType is Stomper.MotionSinus:
            def sinusFunc(t, self=self):
                # t: 0..1
                # cos(pi) == -1 (hit/down)
                # theta: pi..3*pi
                theta = math.pi + (t * 2.*math.pi)
                # c: -1..1
                c = math.cos(theta)
                # z: 0..self.range
                self.model.setZ(self.zOffset +
                                ((.5 + (c*.5)) * self.range))
            motionIval = Sequence(
                LerpFunctionInterval(sinusFunc, duration=self.period),
                )
        elif self.motionType is Stomper.MotionHalfSinus:
            def halfSinusFunc(t, self=self):
                # t: 0..1
                self.model.setZ(self.zOffset +
                                (math.sin(t * math.pi) * self.range))
            motionIval = Sequence(
                LerpFunctionInterval(halfSinusFunc, duration=self.period),
                )
        # put the motion interval into a Parallel so that we can easily add
        # concurrent ivals on (like sound, etc)
        self.ival = Parallel(
            motionIval,
            name='Stomper%s' % self.SerialNum,
            )

        # 'stomp' sound
        if self.sound is not None:
            # make sure we don't play a sound that's too long; cap the
            # sound length to the motion period
            if self.soundLen is None:
                sndDur = motionIval.getDuration()
            else:
                sndDur = min(self.soundLen, motionIval.getDuration())
            self.ival.append(
                SoundInterval(self.sound, duration=sndDur, node=self))

        # shadow
        if self.shadow is not None:
            def adjustShadowScale(t, self=self):
                # scale the shadow according to the position of the
                # stomper
                modelZ = self.model.getZ()
                # a=0..1, 0=down, 1=up
                a = modelZ/self.range
                self.shadow.setScale(lerp(.7, 1., (1.-a)))
            self.ival.append(
                LerpFunctionInterval(adjustShadowScale, duration=self.period))

        self.ival.loop()
        self.ival.setT((globalClock.getFrameTime() - startTime) +
                       (self.period * self.phaseShift))
        
    def exit(self):
        self.ival.finish()
        del self.ival
