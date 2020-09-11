""" MMPlayground module:  contains the MMPlayground
    class which represents the client version of
    Minnie's Melodyland safezone."""

from pandac.PandaModules import *

import Playground
import random
from direct.fsm import ClassicFSM, State
from direct.actor import Actor
from toontown.toonbase import ToontownGlobals

class MMPlayground(Playground.Playground):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // MMPlayground:  client side version of Minnie's Melodyland
    //                safezone.  Handle's the safezone activity for
    //                the local player.
    //
    ////////////////////////////////////////////////////////////////////
    """
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)

        self.activityFsm = ClassicFSM.ClassicFSM('Activity',
                              [State.State('off',
                                      self.enterOff,
                                      self.exitOff,
                                      ['OnPiano']),
                              State.State('OnPiano',
                                      self.enterOnPiano,
                                      self.exitOnPiano,
                                      ['off'])],
                              # Initial state
                              'off',
                              # Final state
                              'off',
                              )
        self.activityFsm.enterInitialState()

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        del self.activityFsm
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        
    def exit(self):
        Playground.Playground.exit(self)

    def handleBookClose(self):
        Playground.Playground.handleBookClose(self)

    def teleportInDone(self):
        Playground.Playground.teleportInDone(self)

    ##### Off state #####

    def enterOff(self):
        return None

    def exitOff(self):
        return None

    ##### OnPiano state #####

    def enterOnPiano(self):
        """
        reparent the local toon to the piano in the safezone.
        """
        base.localAvatar.b_setParent(ToontownGlobals.SPMinniesPiano)

    def exitOnPiano(self):
        """
        unparent the local toon from the piano
        """
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)



    def showPaths(self):
        # Overridden from Playground to fill in the correct parameters
        # for showPathPoints().
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Minnie))
