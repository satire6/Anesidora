from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from otp.level import BasicEntities
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import LiftConstants
import MovingPlatform

class DistributedLift(BasicEntities.DistributedNodePathEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLift')

    def __init__(self, cr):
        BasicEntities.DistributedNodePathEntity.__init__(self, cr)

    def generateInit(self):
        self.notify.debug('generateInit')
        BasicEntities.DistributedNodePathEntity.generateInit(self)
        # load stuff

        self.moveSnd = base.loadSfx('phase_9/audio/sfx/CHQ_FACT_elevator_up_down.mp3')

        self.fsm = ClassicFSM.ClassicFSM('DistributedLift',
                           [
                            State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['moving']),
                            State.State('moving',
                                        self.enterMoving,
                                        self.exitMoving,
                                        ['waiting']),
                            State.State('waiting',
                                        self.enterWaiting,
                                        self.exitWaiting,
                                        ['moving']),
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
        # nodepath that will be lerped, regardless of whether or not
        # model loaded correctly
        self.platform = self.attachNewNode('platParent')

    def setStateTransition(self, toState, fromState, arrivalTimestamp):
        self.notify.debug('setStateTransition: %s->%s' % (fromState, toState))
        # the lift should reach state 'toState' precisely
        # at time 'arrivalTimestamp'
        if not self.isGenerated():
            self.initialState = toState
            self.initialFromState = fromState
            self.initialStateTimestamp = arrivalTimestamp
        else:
            self.fsm.request('moving', [toState, fromState, arrivalTimestamp])

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        BasicEntities.DistributedNodePathEntity.announceGenerate(self)

        self.initPlatform()

        # fire it up
        self.state = None
        self.fsm.request('moving', [self.initialState,
                                    self.initialFromState,
                                    self.initialStateTimestamp])
        del self.initialState
        del self.initialStateTimestamp

    def disable(self):
        self.notify.debug('disable')
        # stop things
        self.ignoreAll()
        self.fsm.requestFinalState()

        BasicEntities.DistributedNodePathEntity.disable(self)

    def delete(self):
        self.notify.debug('delete')
        # unload things
        del self.moveSnd
        del self.fsm
        self.destroyPlatform()
        self.platform.removeNode()
        del self.platform
        BasicEntities.DistributedNodePathEntity.delete(self)

    def initPlatform(self):
        model = loader.loadModel(self.modelPath)
        if model is None:
            return
        model.setScale(self.modelScale)

        # create our moving platform
        if self.floorName is None:
            return
        self.platformModel = MovingPlatform.MovingPlatform()
        self.platformModel.setupCopyModel(
                self.getParentToken(), model, self.floorName)

        # listen for the platform's enter and exit event
        self.accept(self.platformModel.getEnterEvent(), self.localToonEntered)
        self.accept(self.platformModel.getExitEvent(), self.localToonLeft)

        # get handles on the start and end guard collision polys
        self.startGuard = None
        self.endGuard = None
        zoneNp = self.getZoneNode()
        if len(self.startGuardName):
            self.startGuard = zoneNp.find('**/%s' % self.startGuardName)
        if len(self.endGuardName):
            self.endGuard = zoneNp.find('**/%s' % self.endGuardName)

        # get handles on the start and end boarding collision planes
        # (actually, they're the planes we need to stash so that toons
        # can get off the lift)
        side2srch = {
            'front': '**/wall_front',
            'back': '**/wall_back',
            'left': '**/wall_left',
            'right': '**/wall_right',
            }
        if 0:
            # Hack to stop getting out of lift:
            floor = self.platformModel.model.find("**/MovingPlatform-*")
            assert not floor.isEmpty()
            safetyNet = floor.copyTo(floor.getParent())
            safetyNet.setName("safetyNet")
            safetyNet.setZ(-0.1)
            safetyNet.setScale(2.0)
            safetyNet.setCollideMask(ToontownGlobals.safetyNetBitmask)
            safetyNet.flattenLight()
            safetyNet.show() #*#

        # Hack for falling off of the lift:
        for side in side2srch.values():
            np = self.platformModel.find(side)
            if not np.isEmpty():
                np.setScale(1.0, 1.0, 2.0)
                np.setZ(-10)
                np.flattenLight()
        
        self.startBoardColl = NodePathCollection()
        self.endBoardColl = NodePathCollection()
        for side in self.startBoardSides:
            np = self.platformModel.find(side2srch[side])
            if np.isEmpty():
                DistributedLift.warning(
                    "couldn't find %s board collision" % side)
            else:
                self.startBoardColl.addPath(np)
        for side in self.endBoardSides:
            np = self.platformModel.find(side2srch[side])
            if np.isEmpty():
                DistributedLift.warning(
                    "couldn't find %s board collision" % side)
            else:
                self.endBoardColl.addPath(np)

        # now that we've found the guards, we can reparent the platform
        # otherwise our finds would venture into the platform model
        self.platformModel.reparentTo(self.platform)

    def destroyPlatform(self):
        if hasattr(self, 'platformModel'):
            self.ignore(self.platformModel.getEnterEvent())
            self.ignore(self.platformModel.getExitEvent())
            self.platformModel.destroy()
            del self.platformModel
            if self.startGuard is not None:
                self.startGuard.unstash()
            if self.endGuard is not None:
                self.endGuard.unstash()
            del self.startGuard
            del self.endGuard
            del self.startBoardColl
            del self.endBoardColl

    def localToonEntered(self):
        self.sendUpdate('setAvatarEnter')

    def localToonLeft(self):
        self.sendUpdate('setAvatarLeave')

    # ClassicFSM state enter/exit funcs
    def enterOff(self):
        self.notify.debug('enterOff')
    def exitOff(self):
        pass

    def getPosition(self, state):
        if state is LiftConstants.Down:
            return self.startPos
        else:
            return self.endPos

    def getGuard(self, state):
        """returns guard that should be disabled when lift is in 'state'"""
        if state is LiftConstants.Down:
            return self.startGuard
        else:
            return self.endGuard

    def getBoardColl(self, state):
        """returns collision geom that should be disabled when lift is in
        'state'"""
        if state is LiftConstants.Down:
            return self.startBoardColl
        else:
            return self.endBoardColl

    def enterMoving(self, toState, fromState, arrivalTimestamp):
        self.notify.debug('enterMoving, %s->%s' % (fromState, toState))
        if self.state == toState:
            self.notify.warning('already in state %s' % toState)

        # TODO: optimization:
        # if timestamp < now:
        #   just set lift to target state
        # else:
        #   create and play interval

        startPos = self.getPosition(fromState)
        endPos = self.getPosition(toState)

        startGuard = self.getGuard(fromState)
        endGuard = self.getGuard(toState)

        startBoardColl = self.getBoardColl(fromState)
        endBoardColl = self.getBoardColl(toState)

        def startMoving(self=self, guard=startGuard, boardColl=startBoardColl):
            if guard is not None and not guard.isEmpty():
                guard.unstash()
            boardColl.unstash()
            # start the lift sound looping, so that the attenuation recalcs
            # every time it loops
            self.soundIval = SoundInterval(self.moveSnd, node=self.platform)
            self.soundIval.loop()

        def doneMoving(self=self, guard=endGuard, boardColl=endBoardColl,
                       newState=toState):
            self.state = newState
            if hasattr(self, 'soundIval'):
                self.soundIval.pause()
                del self.soundIval
            if guard is not None and not guard.isEmpty():
                guard.stash()
            boardColl.stash()
            self.fsm.request('waiting')

        self.moveIval = Sequence(
            Func(startMoving),
            LerpPosInterval(self.platform, self.duration,
                            endPos, startPos = startPos,
                            blendType='easeInOut',
                            name='lift-%s-move' % self.entId,
                            fluid = 1),
            Func(doneMoving),
            )
        # move should finish at 'arrivalTimestamp'
        ivalStartT = (
            globalClockDelta.networkToLocalTime(arrivalTimestamp, bits=32)
            - self.moveIval.getDuration())
        self.moveIval.start(globalClock.getFrameTime() - ivalStartT)
        
    def exitMoving(self):
        if hasattr(self, 'soundIval'):
            self.soundIval.pause()
            del self.soundIval
        # 'finish'ing here causes ClassicFSM problems
        self.moveIval.pause()
        del self.moveIval

    def enterWaiting(self):
        self.notify.debug('enterWaiting')
    def exitWaiting(self):
        pass

    if __dev__:
        def attribChanged(self, *args):
            BasicEntities.DistributedNodePathEntity.attribChanged(self, *args)
            self.destroyPlatform()
            self.initPlatform()
