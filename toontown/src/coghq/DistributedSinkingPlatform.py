from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from otp.level import BasicEntities
import MovingPlatform
from direct.distributed import DistributedObject
import SinkingPlatformGlobals
from direct.directnotify import DirectNotifyGlobal

# DistributedSinkingPlatform
# This entity is much like a regular PlatformEntity, except it sinks
# when stood on, and raises up to it's starting level when exited.
# It reacts to a toons enter/exit events on the floor collision polygon.
# Since it may not be the local toon that is making the platform sink,
# this must be a distributed class so the AI can tell all the clients
# when the platform has been entered or exited.

class DistributedSinkingPlatform(BasicEntities.DistributedNodePathEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSinkingPlatform')

    def __init__(self, cr):
        BasicEntities.DistributedNodePathEntity.__init__(self,cr)
        self.moveIval = None
        
    def generateInit(self):
        self.notify.debug('generateInit')
        BasicEntities.DistributedNodePathEntity.generateInit(self)

        self.fsm = ClassicFSM.ClassicFSM('DistributedSinkingPlatform',
                           [
                            State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['sinking']),
                            State.State('sinking',
                                        self.enterSinking,
                                        self.exitSinking,
                                        ['rising']),
                            State.State('rising',
                                        self.enterRising,
                                        self.exitRising,
                                        ['sinking', 'off']),
                            ],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()
        
    def generate(self):
        self.notify.debug('generate')
        BasicEntities.DistributedNodePathEntity.generate(self)

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)

        # at this point all the entity attributes have been initialized
        # we can load the model now.
        self.loadModel()

        # listen to enter/exit events of the MovingPlatform, so we
        # can send messages to the AI about the state of the platform
        self.accept(self.platform.getEnterEvent(), self.localToonEntered)
        self.accept(self.platform.getExitEvent(), self.localToonLeft)


    def disable(self):
        self.notify.debug('disable')
        # stop things
        self.ignoreAll()
        self.fsm.requestFinalState()
        BasicEntities.DistributedNodePathEntity.disable(self)

    def delete(self):
        self.notify.debug('delete')
        self.ignoreAll()
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval

        self.platform.destroy()
        del self.platform

        BasicEntities.DistributedNodePathEntity.delete(self)

    def loadModel(self):
        self.notify.debug("loadModel")
        model = loader.loadModel('phase_9/models/cogHQ/platform1')
        self.platform = MovingPlatform.MovingPlatform()
        self.platform.setupCopyModel(self.getParentToken(), model,
                                     'platformcollision')
        self.platform.reparentTo(self)
        self.platform.setPos(0,0,0)
        
    def localToonEntered(self):
        ts = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.sendUpdate('setOnOff', [1, ts])
        # TODO: make this smoother for the local toon
        # Since we are the local toon, this should happen immediately, so
        # we don't see any jumps as a result of the server roundtrip
        #self.fsm.request('sinking', [ts])
        
    def localToonLeft(self):
        ts = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.sendUpdate('setOnOff', [0, ts])
        # TODO: make this smoother for the local toon
        #self.fsm.request('rising', [ts])
    
    # ClassicFSM state enter/exit funcs
    def enterOff(self):
        self.notify.debug('enterOff')
    def exitOff(self):
        self.notify.debug('exitOff')


    def enterSinking(self, ts=0):
        self.notify.debug('enterSinking')
        self.startMoving(SinkingPlatformGlobals.SINKING, ts)

    def exitSinking(self):
        self.notify.debug('exitSinking')
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
            self.moveIval = None
        
    def enterRising(self, ts=0):
        self.notify.debug('enterRising')
        self.startMoving(SinkingPlatformGlobals.RISING, ts)
        
    def exitRising(self):
        self.notify.debug('exitRising')
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
            self.moveIval = None

    
    def setSinkMode(self, avId, mode, ts):
        # AI tells us if the platform is sinking, rising, or off
        # and at what time it started moving
        self.notify.debug("setSinkMode %s" % mode)
        if mode == SinkingPlatformGlobals.OFF:
            # this is a clear message sitting on wire
            self.fsm.requestInitialState()
        # if it is the localToon that caused this sink/rise message
        # to be passed to the AI, don't do anything (since
        # the localToon reacts to the exit event without the server
        # round trip)
        elif mode == SinkingPlatformGlobals.RISING:
            #if avId != base.localAvatar.doId:
            self.fsm.request('rising', [ts])
            #else:
            #    print "ignoring server rise message"
        elif mode == SinkingPlatformGlobals.SINKING:
            #if avId != base.localAvatar.doId:
            self.fsm.request('sinking', [ts])
            #else:
            #    print "ignoring server sink message"
                
    def startMoving(self, direction, ts):
        if direction == SinkingPlatformGlobals.RISING:
            endPos = Vec3(0,0,0)
            pause = self.pauseBeforeRise
            duration = self.riseDuration
        else:
            endPos = Vec3(0,0,-self.verticalRange)
            pause = None
            duration = self.sinkDuration

        # For non-local toons, we will have less time than "duration" to
        # actually complete the interval, because of the server roundtrip.
        # Calculate the actual time (ivalTime) we have to complete the interval.
        startT = globalClockDelta.networkToLocalTime(ts, bits=32)
        curT = globalClock.getFrameTime()
        ivalTime = curT - startT
        if ivalTime < 0:
            ivalTime = 0
        elif ivalTime > duration:
            ivalTime = duration

        duration = duration - ivalTime
        duration = max(0., duration)

        #print "ivalTime = %s" % ivalTime

        moveNode = self.platform
        self.moveIval = Sequence()
        if pause is not None:
            self.moveIval.append(WaitInterval(pause))
        self.moveIval.append(
            LerpPosInterval(moveNode, duration,
                            endPos, startPos = moveNode.getPos(),
                            blendType='easeInOut',
                            name='%s-move' % self.platform.name,
                            fluid = 1),
            )

        #print "timeStamp = %s, ivalStartT = %s, startTime = %s, curT = %s, duration= %s" % (
        #    timestamp, ivalStartT, startT, curT, duration)
        self.moveIval.start()
        

  
