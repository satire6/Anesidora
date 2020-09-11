from pandac.PandaModules import *

import Playground
import random

class DLPlayground(Playground.Playground):
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)


    def showPaths(self):
        # Overridden from Playground to fill in the correct parameters
        # for showPathPoints().
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Donald))
