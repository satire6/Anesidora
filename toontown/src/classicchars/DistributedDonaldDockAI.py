"""DistributedDonaldDockAI module: contains the DistributedDonaldDockAI class"""

from otp.ai.AIBaseGlobal import *

import DistributedCCharBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import random
import CharStateDatasAI
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class DistributedDonaldDockAI(DistributedCCharBaseAI.DistributedCCharBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDonaldDockAI")

    def __init__(self, air):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.DonaldDock)
        self.fsm = ClassicFSM.ClassicFSM('DistributedDonaldDockAI',
                           [State.State('Off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['Lonely', 'TransitionToCostume']),
                            State.State('Lonely',
                                        self.enterLonely,
                                        self.exitLonely,
                                        ['Chatty', 'TransitionToCostume']),
                            State.State('Chatty',
                                        self.enterChatty,
                                        self.exitChatty,
                                        ['Lonely', 'TransitionToCostume']),
                            State.State('TransitionToCostume',
                                            self.enterTransitionToCostume,
                                            self.exitTransitionToCostume,
                                            ['Off']),
                            ],
                           # Initial State
                           'Off',
                           # Final State
                           'Off',
                           )

        self.fsm.enterInitialState()
        self.handleHolidays()

    def delete(self):
        self.fsm.requestFinalState()
        DistributedCCharBaseAI.DistributedCCharBaseAI.delete(self)

        self.lonelyDoneEvent = None
        self.lonely = None
        self.chattyDoneEvent = None
        self.chatty = None

    def generate( self ):
        # all state data's that DonaldDock will need
        #
        DistributedCCharBaseAI.DistributedCCharBaseAI.generate(self)
        self.lonelyDoneEvent = self.taskName('DonaldDock-lonely-done')
        self.lonely = CharStateDatasAI.CharLonelyStateAI(
            self.lonelyDoneEvent, self)

        self.chattyDoneEvent = self.taskName('DonaldDock-chatty-done')
        self.chatty = CharStateDatasAI.CharChattyStateAI(
            self.chattyDoneEvent, self)

    # this function kicks off DonaldDock
    def start(self):
        # poor lonely DonaldDock
        self.fsm.request('Lonely')

    def __decideNextState(self, doneStatus):
        """
        doneStatus, info about the finished state

        called when the current state DonaldDock is in
        decides that it is finished and a new state should
        be transitioned into
        """
        assert(doneStatus.has_key('status'))

        if doneStatus['state'] == 'lonely' and \
           doneStatus['status'] == 'done':
            if len(self.nearbyAvatars) > 0:
                self.fsm.request('Chatty')
            else:
                self.fsm.request('Lonely')
        elif doneStatus['state'] == 'chatty' and \
             doneStatus['status'] == 'done':
            self.fsm.request('Lonely')            
        else:
            assert 0, "Unknown status for DonaldDock"

    ### Off state ###
    def enterOff(self):
        pass

    def exitOff(self):
        DistributedCCharBaseAI.DistributedCCharBaseAI.exitOff(self)

    ### Lonely state ###
    def enterLonely(self):
        self.notify.debug("Entering Lonely")
        self.lonely.enter()
        self.acceptOnce(self.lonelyDoneEvent, self.__decideNextState)

    def exitLonely(self):
        self.notify.debug("Exiting Lonely")
        self.ignore(self.lonelyDoneEvent)
        self.lonely.exit()

    ### Chatty state ###
    def enterChatty(self):
        self.notify.debug("Entering Chatty")
        self.chatty.enter()
        self.acceptOnce(self.chattyDoneEvent, self.__decideNextState)

    def exitChatty(self):
        self.notify.debug("Exiting Chatty")
        self.ignore(self.chattyDoneEvent)
        self.chatty.exit()

    def avatarEnterNextState(self):
        """
        decide what to do with the state machine when
        a toon gets near DonaldDock
        """
        # if this is the only avatar, start talking
        if len(self.nearbyAvatars) == 1:
            self.fsm.request('Chatty')
        else:
            self.notify.debug("avatarEnterNextState: num avatars: " +
                              str(len(self.nearbyAvatars)))

    def avatarExitNextState(self):
        """
        decide what to do with the state machine when a
        toon is no longer near DonaldDock
        """
        # no need to re-sort av list after removal
        if len(self.nearbyAvatars) == 0:
            self.fsm.request('Lonely')

    ##TransitionToCostumeState##
    def enterTransitionToCostume(self):
        pass

    def exitTransitionToCostume(self):
        pass
