"""DistributedSuperGoofyAI module: contains the DistributedMickeyAI class"""

from otp.ai.AIBaseGlobal import *
from toontown.classicchars import DistributedGoofySpeedwayAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import random
from toontown.toonbase import ToontownGlobals
import DistributedCCharBaseAI
import CharStateDatasAI
from toontown.toonbase import TTLocalizer

class DistributedSuperGoofyAI(DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSuperGoofyAI")

    def __init__(self, air):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.SuperGoofy)
        self.fsm = ClassicFSM.ClassicFSM('DistributedSuperGoofyAI',
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

        # We do not want to move into the transitionCostume state unless signalled to do so.
        self.transitionToCostume = 0
        self.fsm.enterInitialState()
        
    def walkSpeed(self):
        return ToontownGlobals.SuperGoofySpeed