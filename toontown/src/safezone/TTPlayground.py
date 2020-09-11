from pandac.PandaModules import *

from toontown.toonbase import ToontownGlobals
import Playground
import random
from toontown.launcher import DownloadForceAcknowledge
from direct.task.Task import Task
from toontown.hood  import ZoneUtil

class TTPlayground(Playground.Playground):
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Playground.Playground.load(self)
    
    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        taskMgr.doMethodLater(1, self.__birds, 'TT-birds')

    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('TT-birds')

    def __birds(self, task):
        base.playSfx(random.choice(self.loader.birdSound))
        t = (random.random() * 20.0) + 1
        taskMgr.doMethodLater(t, self.__birds, 'TT-birds')
        return Task.done

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])

    def enterDFA(self, requestStatus):
        """
        Override the base class because here we specifically ask for
        phase 5, the toontown central streets.
        - NEW: we can now go home.  Check the hood before assuming we
        are going to the streets
        """
        doneEvent = "dfaDoneEvent"
        self.accept(doneEvent, self.enterDFACallback, [requestStatus])
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(doneEvent)
        hood = ZoneUtil.getCanonicalZoneId(requestStatus['hoodId'])
        if hood == ToontownGlobals.MyEstate:
            # Ask if we can enter phase 5.5
            self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(ToontownGlobals.MyEstate))
        elif hood == ToontownGlobals.GoofySpeedway:
            # Ask if we can enter phase 6
            self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(ToontownGlobals.GoofySpeedway))
        elif hood == ToontownGlobals.PartyHood:
            # ask if we can enter phase 13
            self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(ToontownGlobals.PartyHood))
        else:
            # Ask if we can enter phase 5
            self.dfa.enter(5)


    def showPaths(self):
        # Overridden from Playground to fill in the correct parameters
        # for showPathPoints().
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Mickey))
