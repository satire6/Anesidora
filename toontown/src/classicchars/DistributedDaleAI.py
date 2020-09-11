"""DistributedDaisyAI module: contains the DistributedDaisyAI class"""

from otp.ai.AIBaseGlobal import *
import DistributedCCharBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
import random
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import CharStateDatasAI

class DistributedDaleAI(DistributedCCharBaseAI.DistributedCCharBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDaleAI")

    def __init__(self, air, chipId):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.Dale)
        self.chipId =chipId
        self.chip = air.doId2do.get(chipId)
        self.fsm = ClassicFSM.ClassicFSM('DistributedDaleAI',
                           [State.State('Off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['Lonely']),
                            State.State('Lonely',
                                        self.enterLonely,
                                        self.exitLonely,
                                        ['Chatty', 'FollowChip', 'Walk']),
                            State.State('Chatty',
                                        self.enterChatty,
                                        self.exitChatty,
                                        ['Lonely', 'FollowChip', 'Walk']),
                            State.State('Walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['Lonely', 'Chatty']),
                            State.State('FollowChip',
                                        self.enterFollowChip,
                                        self.exitFollowChip,
                                        ['Lonely', 'Chatty', 'FollowChip']),                            
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
        # all state data's that Dale will need
        #
        DistributedCCharBaseAI.DistributedCCharBaseAI.generate(self)

        # the old CharStateDatasAI won't work since dale is dependent on chip
        # lets create hooks to accept when he's entering and leaving states
        #chip = simbase.air.doId2do.get(self.chipId)
        #name = chip.getName()
        #self.lonelyDoneEvent = self.taskName(name + '-lonely-done')
        self.lonely = CharStateDatasAI.CharLonelyStateAI(
            None, self)

        #self.chattyDoneEvent = self.taskName(name + '-chatty-done')
        self.chatty = CharStateDatasAI.CharChattyStateAI(
            None, self)

        #self.walkDoneEvent = self.taskName(name + '-walk-done')
        #self.walk = CharStateDatasAI.CharWalkStateAI(
        #    self.walkDoneEvent, self)

        #self.followChipDoneEvent = self.taskName(name + '-follow-done')        
        self.followChip = CharStateDatasAI.CharFollowChipStateAI(
            None, self, self.chip)

    def walkSpeed(self):
        return ToontownGlobals.DaleSpeed

    # this function kicks off Dale
    def start(self):
        # poor lonely Dale
        self.fsm.request('Lonely')

    def __decideNextState(self, doneStatus):
        """
        doneStatus, info about the finished state
        
        called when the current state Dale is in
        decides that it is finished and a new state should
        be transitioned into
        """
        assert self.notify.debugStateCall(self)
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
            assert 0, "Unknown status for Dale"

    ### Off state ###
    def enterOff(self):
        pass

    def exitOff(self):
        DistributedCCharBaseAI.DistributedCCharBaseAI.exitOff(self)

    ### Lonely state ###
    def enterLonely(self):
        assert self.notify.debugStateCall(self)
        self.lonely.enter()
        #self.acceptOnce(self.lonelyDoneEvent, self.__decideNextState)

    def exitLonely(self):
        assert self.notify.debugStateCall(self)
        #self.ignore(self.lonelyDoneEvent)
        self.lonely.exit()

    def __goForAWalk(self, task):
        self.notify.debug("going for a walk")
        self.fsm.request('Walk')
        return Task.done

    ### Chatty state ###
    def enterChatty(self):
        self.chatty.enter()
        #self.acceptOnce(self.chattyDoneEvent, self.__decideNextState)

    def exitChatty(self):
        #self.ignore(self.chattyDoneEvent)
        self.chatty.exit()


    ### Walk state ###
    def enterWalk(self):
        self.notify.debug("going for a walk")
        self.walk.enter()
        self.acceptOnce(self.walkDoneEvent, self.__decideNextState)

    def exitWalk(self):
        self.ignore(self.walkDoneEvent)
        self.walk.exit()

    ### Follow Chip state ###
    def enterFollowChip(self):
        self.notify.debug("enterFollowChip")
        #import pdb; pdb.set_trace()
        walkState = self.chip.walk
        destNode = walkState.getDestNode()        
        self.followChip.enter(destNode)
        #self.acceptOnce(self.Event, self.__decideNextState)

    def exitFollowChip(self):
        #self.ignore(self.walkDoneEvent)
        self.notify.debug('exitFollowChip')
        self.followChip.exit()        


    def avatarEnterNextState(self):
        """
        decide what to do with the state machine when
        a toon gets near Dale
        """
        # if this is the only avatar, start talking
        if len(self.nearbyAvatars) == 1:
            if False: #self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Chatty')
            else:
                self.notify.debug("avatarEnterNextState: in walk state")
        else:
            self.notify.debug("avatarEnterNextState: num avatars: " +
                              str(len(self.nearbyAvatars)))

    def avatarExitNextState(self):
        """
        decide what to do with the state machine when a
        toon is no longer near Dale
        """
        # no need to re-sort av list after removal
        if len(self.nearbyAvatars) == 0:
            if self.fsm.getCurrentState().getName() != 'Walk':
                #self.fsm.request('Lonely')
                pass

    def chipEnteringState(self, newState):
        """Handle chip entering a new state."""
        assert self.notify.debugStateCall(self)
        if newState == 'Walk':
            self.doFollowChip()
        #elif newState == 'Chatty':
        #    self.doChatty()

    def chipLeavingState(self, oldState):
        """Handle chip leaving his state."""
        assert self.notify.debugStateCall(self)

    def doFollowChip(self):
        """Actually make dale follow chip."""
        walkState = self.chip.walk
        destNode = walkState.getDestNode()
        #import pdb; pdb.set_trace()
        self.fsm.request('FollowChip')

    def doChatty(self):
        """Make Dale's chatter sync with Chip's."""
        #self.fsm.request('Chatty')
        pass
                
    def getChipId(self):
        """Return chip's doId."""
        return self.chipId
