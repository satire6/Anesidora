"""PetGoal.py"""

from direct.task import Task
from direct.fsm import FSM, ClassicFSM, State
from direct.showbase.PythonUtil import randFloat, Functor
from direct.directnotify import DirectNotifyGlobal
from toontown.pets import PetConstants
from toontown.toon import DistributedToonAI

class PetGoal(FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("PetGoal")
    SerialNum = 0
        
    def __init__(self):
        FSM.FSM.__init__(self, self.__class__.__name__)
        self.goalMgr = None
        self.pet = None
        self.brain = None
        # set this to nonzero to make the goal remove itself from the mgr
        # when announceDone is called
        self.removeOnDone = 0

        self.serialNum = PetGoal.SerialNum
        PetGoal.SerialNum += 1

        self.fsm = ClassicFSM.ClassicFSM(
            'PetGoalFSM',
            [State.State('off',
                         self.enterOff,
                         self.exitOff,
                         ['background']),
             State.State('background',
                         self.enterBackground,
                         self.exitBackground,
                         ['foreground']),
             State.State('foreground',
                         self.enterForeground,
                         self.exitForeground,
                         ['background']),
             ],
            # init
            'off',
            # final
            'off',
            )
        self.fsm.enterInitialState()

    def destroy(self):
        if hasattr(self, 'fsm'):
            self.fsm.requestFinalState()
            del self.fsm
        # cleanup the FSM base class
        self.cleanup()

    def _removeSelf(self):
        # removes ourselves from our goalMgr
        self.goalMgr.removeGoal(self)

    def getDoneEvent(self):
        return 'PetGoalDone-%s' % self.serialNum
    def announceDone(self):
        if self.removeOnDone:
            self._removeSelf()
        messenger.send(self.getDoneEvent())
        if self.removeOnDone:
            self.destroy()

    def setGoalMgr(self, goalMgr):
        self.goalMgr = goalMgr
        self.pet = goalMgr.pet
        self.brain = self.pet.brain
        self.fsm.request('background')
    def clearGoalMgr(self):
        self.goalMgr = None
        self.pet = None
        self.brain = None
        self.fsm.requestFinalState()

    def getPriority(self):
        return PetConstants.PriorityDefault

    # state handlers
    def enterOff(self):
        pass
    def exitOff(self):
        pass

    def enterBackground(self):
        # we're active on the pet, but not the primary goal
        # we will always go through this state before entering Foreground state
        pass
    def exitBackground(self):
        pass

    def enterForeground(self):
        # we are currently the pet's primary goal
        pass
    def exitForeground(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.getPriority())

class InteractWithAvatar(PetGoal):
    """abstract base class for goals that require that we are next to an
    avatar"""
    SerialNum = 0
    def __init__(self, avatar):
        PetGoal.__init__(self)
        self.avatar = avatar
        self.serialNum = InteractWithAvatar.SerialNum
        InteractWithAvatar.SerialNum += 1
        self.transitionDoLaterName = '%s-doLater-%s' % (
            InteractWithAvatar.__name__,
            self.serialNum)
    def destroy(self):
        PetGoal.destroy(self)
        if hasattr(self, 'avatar'):
            del self.avatar

    def enterForeground(self):
        # we kick into action when we are the foreground
        self.request('Chase')
    def exitForeground(self):
        self.request('Off')

    def enterChase(self):
        PetGoal.notify.debug('enterChase')
        if self.brain.lookingAt(self.avatar.doId):
            # we can't immediately transition to the Interact state
            # spawn a doLater
            def goToInteract(task=None, self=self):
                self.request('Interact')
                return Task.done
            taskMgr.doMethodLater(.0001, goToInteract,
                                  self.transitionDoLaterName)
        else:
            # chase until we are looking at them
            self.accept(
                self.brain.getObserveEventAttendingAvStart(self.avatar.doId),
                Functor(self.request, 'Interact'))
            self.brain._chase(self.avatar)
    def exitChase(self):
        self.ignore(
            self.brain.getObserveEventAttendingAvStart(self.avatar.doId))
        taskMgr.remove(self.transitionDoLaterName)

    def enterInteract(self):
        PetGoal.notify.debug('enterInteract')
        if self._chaseAvInInteractMode():
            self.accept(
                self.brain.getObserveEventAttendingAvStop(self.avatar.doId),
                Functor(self.request, 'Chase'))
        self.startInteract()
    def exitInteract(self):
        self.stopInteract()
        self.ignore(
            self.brain.getObserveEventAttendingAvStop(self.avatar.doId))

    # override these
    def startInteract(self):
        pass
    def stopInteract(self):
        pass

    # override this to return false if you don't want to chase the avatar
    # once you have entered 'interact' mode
    def _chaseAvInInteractMode(self):
        return True

    def __str__(self):
        return '%s-%s: %s' % (self.__class__.__name__, self.avatar.doId,
                              self.getPriority())

class Wander(PetGoal):
    def enterForeground(self):
        self.brain._wander()

class ChaseAvatar(PetGoal):
    def __init__(self, avatar):
        PetGoal.__init__(self)
        self.avatar = avatar
        self.isToon = isinstance(self.avatar,
                                 DistributedToonAI.DistributedToonAI)
    def destroy(self):
        PetGoal.destroy(self)
        if hasattr(self, 'avatar'):
            del self.avatar

    def setGoalMgr(self, goalMgr):
        PetGoal.setGoalMgr(self, goalMgr)
        self.basePriority = PetConstants.PriorityChaseAv
        """
        # this would work better in a probability-based system; we have
        # an absolute highest-priority system
        if self.avatar.doId == self.goalMgr.pet.ownerId:
            self.basePriority *= 1.2
            """

    def getPriority(self):
        priority = self.basePriority
        if self.isToon and self.pet.mood.getDominantMood() == 'hunger':
            priority *= PetConstants.HungerChaseToonScale
        lastInteractTime = self.brain.lastInteractTime.get(self.avatar.doId)
        if lastInteractTime is not None:
            elapsed = globalClock.getFrameTime() - lastInteractTime
            if elapsed < PetConstants.GettingAttentionGoalScaleDur:
                priority *= PetConstants.GettingAttentionGoalScale
        return priority

    def enterForeground(self):
        self.brain._chase(self.avatar)

    def __str__(self):
        return '%s-%s: %s' % (self.__class__.__name__, self.avatar.doId,
                              self.getPriority())

# for debug
class ChaseAvatarLeash(PetGoal):
    def __init__(self, avId):
        PetGoal.__init__(self)
        self.avId = avId

    def getPriority(self):
        return PetConstants.PriorityDebugLeash

    def enterForeground(self):
        av = simbase.air.doId2do.get(self.avId)
        if av:
            self.brain._chase(av)
        else:
            self._removeSelf()

    def __str__(self):
        return '%s-%s: %s' % (self.__class__.__name__, self.avatar.doId,
                              self.getPriority())

class FleeFromAvatar(PetGoal):
    def __init__(self, avatar):
        PetGoal.__init__(self)
        self.avatar = avatar

    def destroy(self):
        PetGoal.destroy(self)
        if hasattr(self, 'avatar'):
            del self.avatar

    def getPriority(self):
        priority = PetConstants.PriorityFleeFromAvatar
        # TODO: factor in fear of avatar?
        if self.avatar.doId == self.goalMgr.pet.ownerId:
            priority *= PetConstants.FleeFromOwnerScale
        return priority

    def enterForeground(self):
        self.brain._chase(self.avatar)

    def __str__(self):
        return '%s-%s: %s' % (self.__class__.__name__, self.avatar.doId,
                              self.getPriority())

class DoTrick(InteractWithAvatar):
    def __init__(self, avatar, trickId):
        InteractWithAvatar.__init__(self, avatar)
        self.trickId = trickId
        self.removeOnDone = 1

    def getPriority(self):
        # TODO: make contingent on how much we like the avatar
        return PetConstants.PriorityDoTrick

    def setGoalMgr(self, goalMgr):
        # there should be only one DoTrick at a time in the GoalMgr
        assert not goalMgr.hasTrickGoal()
        goalMgr._setHasTrickGoal(True)
        InteractWithAvatar.setGoalMgr(self, goalMgr)
    def clearGoalMgr(self):
        assert self.goalMgr.hasTrickGoal()
        self.goalMgr._setHasTrickGoal(False)
        InteractWithAvatar.clearGoalMgr(self)

    # once we've started doing the trick, don't try to follow the avatar
    def _chaseAvInInteractMode(self):
        return False

    def startInteract(self):
        self.brain._doTrick(self.trickId, self.avatar)
        self.trickDoneEvent = self.pet.actionFSM.getTrickDoneEvent()
        self.accept(self.trickDoneEvent, self.announceDone)
    def stopInteract(self):
        self.ignore(self.trickDoneEvent)
        del self.trickDoneEvent

    def __str__(self):
        return '%s-%s-%s: %s' % (self.__class__.__name__, self.avatar.doId,
                                 self.trickId, self.getPriority())

    
