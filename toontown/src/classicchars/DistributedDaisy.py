"""DistributedDaisy module: contains the DistributedDaisy class"""

from direct.showbase.ShowBaseGlobal import *
import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from direct.fsm import State
import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import TTHood

class DistributedDaisy(DistributedCCharBase.DistributedCCharBase):
    """DistributedDaisy class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedDaisy")

    def __init__(self, cr):
        try:
            self.DistributedDaisy_initialized
        except:
            self.DistributedDaisy_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr,
                                                               TTLocalizer.Daisy,
                                                               'dd')
            self.fsm = ClassicFSM.ClassicFSM(self.getName(),
                            [State.State('Off',
                                         self.enterOff,
                                         self.exitOff,
                                         ['Neutral']),
                             State.State('Neutral',
                                         self.enterNeutral,
                                         self.exitNeutral,
                                         ['Walk']),
                             State.State('Walk',
                                         self.enterWalk,
                                         self.exitWalk,
                                         ['Neutral']),
                             ],
                             # Initial State
                             'Off',
                             # Final State
                             'Off',
                             )

            self.fsm.enterInitialState()
        self.handleHolidays()

    def disable(self):
        self.fsm.requestFinalState()
        DistributedCCharBase.DistributedCCharBase.disable(self)

        del self.neutralDoneEvent
        del self.neutral
        del self.walkDoneEvent
        del self.walk
        self.fsm.requestFinalState()

    def delete(self):
        """
        remove Daisy and state data information
        """
        try:
            self.DistributedDaisy_deleted
        except:
            del self.fsm
            self.DistributedDaisy_deleted = 1
            DistributedCCharBase.DistributedCCharBase.delete(self)

    def generate( self ):
        """
        create Daisy and state data information
        """
        DistributedCCharBase.DistributedCCharBase.generate(self, self.diffPath)
        name = self.getName()
        self.neutralDoneEvent = self.taskName(name + '-neutral-done')
        self.neutral = CharStateDatas.CharNeutralState(
            self.neutralDoneEvent, self)
        self.walkDoneEvent = self.taskName(name + '-walk-done')
        if self.diffPath == None:
            self.walk = CharStateDatas.CharWalkState(
            self.walkDoneEvent, self)
        else:
            self.walk = CharStateDatas.CharWalkState(
            self.walkDoneEvent, self, self.diffPath)
        self.fsm.request('Neutral')

    ### Off state ###
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ### Neutral state ###
    def enterNeutral(self):
        self.neutral.enter()
        self.acceptOnce(self.neutralDoneEvent, self.__decideNextState)

    def exitNeutral(self):
        self.ignore(self.neutralDoneEvent)
        self.neutral.exit()

    ### Walk state ###
    def enterWalk(self):
        self.walk.enter()
        self.acceptOnce(self.walkDoneEvent, self.__decideNextState)

    def exitWalk(self):
        self.ignore(self.walkDoneEvent)
        self.walk.exit()

    def __decideNextState(self, doneStatus):
        self.fsm.request('Neutral')

    def setWalk(self, srcNode, destNode, timestamp):
        """
        srcNode, were to walk from
        destNode, where to walk to
        timestamp, when server started walk

        message sent from the server to say that this
        character should now go into walk state
        """
        if destNode and (not destNode == srcNode):
            self.walk.setWalk(srcNode, destNode, timestamp)
            # request to enter walk if we have a state machine
            self.fsm.request('Walk')

    def walkSpeed(self):
        return ToontownGlobals.DaisySpeed
        
    def handleHolidays(self):
        """
        Handle holiday specific behaviour
        """
        DistributedCCharBase.DistributedCCharBase.handleHolidays(self)
        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds and isinstance(self.cr.playGame.hood, TTHood.TTHood):
                self.diffPath = TTLocalizer.Mickey
