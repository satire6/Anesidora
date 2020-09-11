"""PetActionFSM.py"""

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.distributed.ClockDelta import globalClockDelta
from direct.showbase.PythonUtil import lerp
from toontown.pets import PetTricks
from toontown.toon import DistributedToonAI

class PetActionFSM(FSM.FSM):
    """This FSM contains states that represent and implement discrete
    actions that a Pet can perform. It ensures that the pet doesn't try
    to do more than one thing at a time. PetBrain does the majority of
    the state transition requests, and this FSM does the work of making the
    pet carry out the action."""
    
    notify = DirectNotifyGlobal.directNotify.newCategory("PetActionFSM")

    def __init__(self, pet):
        FSM.FSM.__init__(self, PetActionFSM.__name__)
        self.pet = pet
        self.trickSerialNum = 0

    def destroy(self):
        self.cleanup()

    # states

    def enterNeutral(self):
        PetActionFSM.notify.debug('enterNeutral')
    def exitNeutral(self):
        pass

    def enterChase(self, target):
        PetActionFSM.notify.debug('enterChase: %s' % target)
        # chase a target
        self.pet.chaseImpulse.setTarget(target)
        self.pet.mover.addImpulse('chase', self.pet.chaseImpulse)
        self.pet.unstickFSM.request('on')
    def exitChase(self):
        self.pet.unstickFSM.request('off')
        self.pet.mover.removeImpulse('chase')

    def enterFlee(self, chaser):
        PetActionFSM.notify.debug('enterFlee: %s' % chaser)
        # flee from a chaser
        self.pet.fleeImpulse.setChaser(chaser)
        self.pet.mover.addImpulse('flee', self.pet.fleeImpulse)
        self.pet.unstickFSM.request('on')
    def exitFlee(self):
        self.pet.unstickFSM.request('off')
        self.pet.mover.removeImpulse('flee')

    def enterWander(self):
        PetActionFSM.notify.debug('enterWander')
        self.pet.mover.addImpulse('wander', self.pet.wanderImpulse)
    def exitWander(self):
        self.pet.mover.removeImpulse('wander')

    def enterUnstick(self):
        PetActionFSM.notify.debug('enterUnstick')
        self.pet.mover.addImpulse('unstick', self.pet.wanderImpulse)
    def exitUnstick(self):
        self.pet.mover.removeImpulse('unstick')

    def enterInspectSpot(self, spot):
        """pick a random spot to investigate"""
        PetActionFSM.notify.debug('enterInspectSpot')
        self.pet.chaseImpulse.setTarget(spot)
        self.pet.mover.addImpulse('inspect', self.pet.chaseImpulse)
        self.pet.unstickFSM.request('on')
    def exitInspectSpot(self):
        self.pet.unstickFSM.request('off')
        self.pet.mover.removeImpulse('inspect')

    def enterStay(self, avatar):
        PetActionFSM.notify.debug('enterStay')
    def exitStay(self):
        pass

    def enterHeal(self, avatar):
        PetActionFSM.notify.debug('enterHeal')
        avatar.toonUp(3)
        # keep chasing the avatar
        self.pet.chaseImpulse.setTarget(avatar)
        self.pet.mover.addImpulse('chase', self.pet.chaseImpulse)
    def exitHeal(self):
        self.pet.mover.removeImpulse('chase')

    def enterTrick(self, avatar, trickId):
        PetActionFSM.notify.debug('enterTrick')
        if not self.pet.isLockedDown():
            self.pet.lockPet()
        self.pet.sendUpdate('doTrick',
                            [trickId, globalClockDelta.getRealNetworkTime()])
        def finish(avatar=avatar, trickId=trickId, self=self):
            # check to make sure we're not being deleted
            if hasattr(self.pet, 'brain'):
                # heal toons that are looking at us
                healRange = PetTricks.TrickHeals[trickId]
                aptitude = self.pet.getTrickAptitude(trickId)
                healAmt = int(lerp(healRange[0], healRange[1], aptitude))
                if healAmt:
                    for avId in self.pet.brain.getAvIdsLookingAtUs():
                        av = self.pet.air.doId2do.get(avId)
                        if av:
                            if isinstance(av,
                                          DistributedToonAI.DistributedToonAI):
                                av.toonUp(healAmt)
                self.pet._handleDidTrick(trickId)
                if not self.pet.isLockedDown():
                    self.pet.unlockPet()
                messenger.send(self.getTrickDoneEvent())
        self.trickDoneEvent = 'trickDone-%s-%s' % (self.pet.doId,
                                                   self.trickSerialNum)
        self.trickSerialNum += 1
        self.trickFinishIval = Sequence(
            WaitInterval(PetTricks.TrickLengths[trickId]),
            Func(finish),
            name='petTrickFinish-%s' % self.pet.doId)
        self.trickFinishIval.start()

    def getTrickDoLaterName(self):
        return 'petTrickDoLater-%s' % self.pet.doId
    def getTrickDoneEvent(self):
        assert hasattr(self, 'trickDoneEvent')
        return self.trickDoneEvent

    def exitTrick(self):
        if self.trickFinishIval.isPlaying():
            self.trickFinishIval.finish()
        del self.trickFinishIval
        if self.pet.isLockedDown():
            self.pet.unlockPet()
        del self.trickDoneEvent

    def enterMovie(self):
        # sit tight and don't do anything
        PetActionFSM.notify.debug('enterMovie')
    def exitMovie(self):
        pass
