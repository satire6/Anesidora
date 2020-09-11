"""DistributedGoofyAI module: contains the DistributedGoofyAI class"""

from otp.ai.AIBaseGlobal import *
import DistributedCCharBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import random
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import CharStateDatasAI

class DistributedGoofyAI(DistributedCCharBaseAI.DistributedCCharBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGoofyAI")

    def __init__(self, air):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.Goofy)
        self.fsm = ClassicFSM.ClassicFSM('DistributedGoofyAI',
                           [State.State('Off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['Lonely']),
                            State.State('Lonely',
                                        self.enterLonely,
                                        self.exitLonely,
                                        ['Chatty', 'Walk']),
                            State.State('Chatty',
                                        self.enterChatty,
                                        self.exitChatty,
                                        ['Lonely', 'Walk']),
                            State.State('Walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['Lonely', 'Chatty']),
                            ],
                           # Initial State
                           'Off',
                           # Final State
                           'Off',
                           )

        self.fsm.enterInitialState()

    def delete(self):
        self.fsm.requestFinalState()
        DistributedCCharBaseAI.DistributedCCharBaseAI.delete(self)

        self.lonelyDoneEvent = None
        self.lonely = None
        self.chattyDoneEvent = None
        self.chatty = None
        self.walkDoneEvent = None
        self.walk = None

    def generate( self ):
        # all state data's that Goofy will need
        #
        DistributedCCharBaseAI.DistributedCCharBaseAI.generate(self)
        name = self.getName()
        self.lonelyDoneEvent = self.taskName(name + '-lonely-done')
        self.lonely = CharStateDatasAI.CharLonelyStateAI(
            self.lonelyDoneEvent, self)

        self.chattyDoneEvent = self.taskName(name + '-chatty-done')
        self.chatty = CharStateDatasAI.CharChattyStateAI(
            self.chattyDoneEvent, self)

        self.walkDoneEvent = self.taskName(name + '-walk-done')
        self.walk = CharStateDatasAI.CharWalkStateAI(
            self.walkDoneEvent, self)

    def walkSpeed(self):
        return ToontownGlobals.GoofySpeed

    # this function kicks off Goofy
    def start(self):
        # poor lonely Goofy
        self.fsm.request('Lonely')

    def __decideNextState(self, doneStatus):
        """
        doneStatus, info about the finished state
        
        called when the current state Goofy is in
        decides that it is finished and a new state should
        be transitioned into
        """
        assert(doneStatus.has_key('status'))
        if doneStatus['state'] == 'lonely' and \
           doneStatus['status'] == 'done':
            self.fsm.request('Walk')
        elif doneStatus['state'] == 'chatty' and \
             doneStatus['status'] == 'done':
            self.fsm.request('Walk')
        elif doneStatus['state'] == 'walk' and \
             doneStatus['status'] == 'done':
            if len(self.nearbyAvatars) > 0:
                self.fsm.request('Chatty')
            else:
                self.fsm.request('Lonely')
        else:
            assert 0, "Unknown status for Goofy"

    ### Off state ###
    def enterOff(self):
        pass

    def exitOff(self):
        DistributedCCharBaseAI.DistributedCCharBaseAI.exitOff(self)

    ### Lonely state ###
    def enterLonely(self):
        self.lonely.enter()
        self.acceptOnce(self.lonelyDoneEvent, self.__decideNextState)

    def exitLonely(self):
        self.ignore(self.lonelyDoneEvent)
        self.lonely.exit()

    def __goForAWalk(self, task):
        self.notify.debug("going for a walk")
        self.fsm.request('Walk')
        return Task.done

    ### Chatty state ###
    def enterChatty(self):
        self.chatty.enter()
        self.acceptOnce(self.chattyDoneEvent, self.__decideNextState)

    def exitChatty(self):
        self.ignore(self.chattyDoneEvent)
        self.chatty.exit()


    ### Walk state ###
    def enterWalk(self):
        self.notify.debug("going for a walk")
        self.walk.enter()
        self.acceptOnce(self.walkDoneEvent, self.__decideNextState)

    def exitWalk(self):
        self.ignore(self.walkDoneEvent)
        self.walk.exit()


    def avatarEnterNextState(self):
        """
        decide what to do with the state machine when
        a toon gets near Goofy
        """
        # if this is the only avatar, start talking
        if len(self.nearbyAvatars) == 1:
            if self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Chatty')
            else:
                self.notify.debug("avatarEnterNextState: in walk state")
        else:
            self.notify.debug("avatarEnterNextState: num avatars: " +
                              str(len(self.nearbyAvatars)))

    def avatarExitNextState(self):
        """
        decide what to do with the state machine when a
        toon is no longer near Goofy
        """
        # no need to re-sort av list after removal
        if len(self.nearbyAvatars) == 0:
            if self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Lonely')

