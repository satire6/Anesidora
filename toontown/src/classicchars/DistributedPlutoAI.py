"""DistributedPlutoAI module: contains the DistributedPlutoAI class"""

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

class DistributedPlutoAI(DistributedCCharBaseAI.DistributedCCharBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPlutoAI")

    def __init__(self, air):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.Pluto)
        self.fsm = ClassicFSM.ClassicFSM('DistributedPlutoAI',
                           [State.State('Off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['Lonely', 'TransitionToCostume', 'Walk']),
                            State.State('Lonely',
                                        self.enterLonely,
                                        self.exitLonely,
                                        ['Chatty', 'Walk', 'TransitionToCostume']),
                            State.State('Chatty',
                                        self.enterChatty,
                                        self.exitChatty,
                                        ['Lonely', 'Walk', 'TransitionToCostume']),
                            State.State('Walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['Lonely', 'Chatty', 'TransitionToCostume']),
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
        self.walkDoneEvent = None
        self.walk = None

    def generate( self ):
        # all state data's that Pluto will need
        #
        DistributedCCharBaseAI.DistributedCCharBaseAI.generate(self)
        self.lonelyDoneEvent = self.taskName('pluto-lonely-done')
        self.lonely = CharStateDatasAI.CharLonelyStateAI(
            self.lonelyDoneEvent, self)

        self.chattyDoneEvent = self.taskName('pluto-chatty-done')
        self.chatty = CharStateDatasAI.CharChattyStateAI(
            self.chattyDoneEvent, self)

        self.walkDoneEvent = self.taskName('pluto-walk-done')
        if self.diffPath == None:
            self.walk = CharStateDatasAI.CharWalkStateAI(
                self.walkDoneEvent, self)
        else:
            self.walk = CharStateDatasAI.CharWalkStateAI(
                self.walkDoneEvent, self, self.diffPath)


    def walkSpeed(self):
        return ToontownGlobals.PlutoSpeed

    # this function kicks off Pluto
    def start(self):
        # poor lonely Pluto
        self.fsm.request('Lonely')

    def __decideNextState(self, doneStatus):
        """
        doneStatus, info about the finished state

        called when the current state Pluto is in
        decides that it is finished and a new state should
        be transitioned into
        """
        assert(doneStatus.has_key('status'))

        if(self.transitionToCostume == 1):
            curWalkNode = self.walk.getDestNode()
            if simbase.air.holidayManager:
                if ToontownGlobals.HALLOWEEN_COSTUMES in simbase.air.holidayManager.currentHolidays and \
                   simbase.air.holidayManager.currentHolidays[ToontownGlobals.HALLOWEEN_COSTUMES]:
                    simbase.air.holidayManager.currentHolidays[ToontownGlobals.HALLOWEEN_COSTUMES].triggerSwitch(curWalkNode, self)
                    self.fsm.request('TransitionToCostume')
                elif ToontownGlobals.APRIL_FOOLS_COSTUMES in simbase.air.holidayManager.currentHolidays and \
                   simbase.air.holidayManager.currentHolidays[ToontownGlobals.APRIL_FOOLS_COSTUMES]:
                    simbase.air.holidayManager.currentHolidays[ToontownGlobals.APRIL_FOOLS_COSTUMES].triggerSwitch(curWalkNode, self)
                    self.fsm.request('TransitionToCostume')
                else:
                    self.notify.warning('transitionToCostume == 1 but no costume holiday')
            else:
                self.notify.warning('transitionToCostume == 1 but no holiday Manager')

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
            assert 0, "Unknown status for Pluto"

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
        a toon gets near Pluto
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
        toon is no longer near Pluto
        """
        # no need to re-sort av list after removal
        if len(self.nearbyAvatars) == 0:
            if self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Lonely')
                
    def handleHolidays(self):
        """
        Handle Holiday specific behaviour
        """
        DistributedCCharBaseAI.DistributedCCharBaseAI.handleHolidays(self)
        if hasattr(simbase.air, "holidayManager"):
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in simbase.air.holidayManager.currentHolidays:
                if simbase.air.holidayManager.currentHolidays[ToontownGlobals.APRIL_FOOLS_COSTUMES] != None \
                    and simbase.air.holidayManager.currentHolidays[ToontownGlobals.APRIL_FOOLS_COSTUMES].getRunningState():
                    self.diffPath = TTLocalizer.Minnie

    ##TransitionToCostumeState##
    def enterTransitionToCostume(self):
        pass

    def exitTransitionToCostume(self):
        pass
