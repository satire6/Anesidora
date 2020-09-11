"""DistributedPluto module: contains the DistributedPluto class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
import CharStateDatas
from direct.fsm import StateData
from direct.task import Task
from toontown.toonbase import TTLocalizer
from toontown.hood import MMHood

class DistributedPluto(DistributedCCharBase.DistributedCCharBase):
    """DistributedPluto class"""

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPluto')

    def __init__(self, cr):
        try:
            self.DistributedPluto_initialized
        except:
            self.DistributedPluto_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr,
                                                               TTLocalizer.Pluto,
                                                               'p')
            self.fsm = ClassicFSM.ClassicFSM('DistributedPluto',
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

        taskMgr.remove('enterNeutralTask')
        taskMgr.remove('enterWalkTask')
        del self.neutralDoneEvent
        del self.neutral
        del self.walkDoneEvent
        del self.walk
        del self.neutralStartTrack
        del self.walkStartTrack
        self.fsm.requestFinalState()

    def delete(self):
        """
        remove Pluto and state data information
        """
        try:
            self.DistributedPluto_deleted
        except:
            self.DistributedPluto_deleted = 1
            del self.fsm
            DistributedCCharBase.DistributedCCharBase.delete(self)

    def generate( self ):
        """
        create Pluto and state data information
        """
        DistributedCCharBase.DistributedCCharBase.generate(self, self.diffPath)
        self.neutralDoneEvent = self.taskName('pluto-neutral-done')
        self.neutral = CharStateDatas.CharNeutralState(self.neutralDoneEvent, self)
        self.walkDoneEvent = self.taskName('pluto-walk-done')
        if self.diffPath == None:
            self.walk = CharStateDatas.CharWalkState(
            self.walkDoneEvent, self)
        else:
            self.walk = CharStateDatas.CharWalkState(
            self.walkDoneEvent, self, self.diffPath)
        self.walkStartTrack = Sequence(self.actorInterval('stand'),
                                       Func(self.stand))
        self.neutralStartTrack = Sequence(self.actorInterval('sit'),
                                          Func(self.sit))
        self.fsm.request('Neutral')

    # Pluto's geometry changes dramatically from sitting to standing so
    # we will perform some subtle transformations upon transitions
    def stand(self):
        self.dropShadow.setScale(0.9, 1.35, 0.9)
        if hasattr(self, 'collNodePath'):
            self.collNodePath.setScale(1.0, 1.5, 1.0)

    def sit(self):
        self.dropShadow.setScale(0.9)
        if hasattr(self, 'collNodePath'):
            self.collNodePath.setScale(1.0)

    ### Off state ###
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ### Neutral state ###
    def enterNeutral(self):
        self.notify.debug("Neutral " + self.getName() + "...")
        # pass in the stand track to the walk state data
        self.neutral.enter(self.neutralStartTrack)
        self.acceptOnce(self.neutralDoneEvent, self.__decideNextState)

    def exitNeutral(self):
        self.ignore(self.neutralDoneEvent)
        self.neutral.exit()

    ### Walk state ###
    def enterWalk(self):
        self.notify.debug("Walking " + self.getName() + "...")
        # pass in the stand track to the walk state data
        self.walk.enter(self.walkStartTrack)
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
        return ToontownGlobals.PlutoSpeed
        
    def handleHolidays(self):           
        """        
        Handle Holiday specific behaviour        
        """         
        DistributedCCharBase.DistributedCCharBase.handleHolidays(self)
        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds and isinstance(self.cr.playGame.hood, MMHood.MMHood):
                self.diffPath = TTLocalizer.Minnie
        
    def getCCLocation(self):
        if self.diffPath == None:
            return 1
        else:
            return 0
