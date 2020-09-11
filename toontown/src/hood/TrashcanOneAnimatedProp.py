from toontown.hood import ZeroAnimatedProp
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal


class TrashcanOneAnimatedProp(ZeroAnimatedProp.ZeroAnimatedProp):
    """Our trashcan zero class that gradually increases movements."""

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'TrashcanOneAnimatedProp')

    PauseTimeMult = base.config.GetFloat('zero-pause-mult', 1.0)

    PhaseInfo = {
        0 : ('tt_a_ara_dga_trashcan_firstMoveLidFlip1',40 * PauseTimeMult),
        1 : ('tt_a_ara_dga_trashcan_firstMoveStruggle', 20 * PauseTimeMult),
        2 : ('tt_a_ara_dga_trashcan_firstMoveLidFlip2', 10 * PauseTimeMult),
        3 : ('tt_a_ara_dga_trashcan_firstMoveJump', 8 * PauseTimeMult),
        4 : ('tt_a_ara_dga_trashcan_firstMoveLidFlip3', 6 * PauseTimeMult),
        5 : ('tt_a_ara_dga_trashcan_firstMoveJumpHit', 4 * PauseTimeMult),
        6 : ('tt_a_ara_dga_trashcan_firstMoveJumpJuggle', 2 * PauseTimeMult),
        }
    
    PhaseWeStartAnimating = 3
    
    def __init__(self, node):
        """Constuct ourself and correct assumptions in base class."""
        ZeroAnimatedProp.ZeroAnimatedProp.__init__(self, node,
                                                   'trashcan',
                                                   self.PhaseInfo,
                                                   ToontownGlobals.TRASHCAN_ZERO_HOLIDAY
                                                   )
        
    def startIfNeeded(self):
        """Check our current phase, if valid go to the right state."""
        assert self.notify.debugStateCall(self)
        # we need a try to stop the level editor from crashing
        try:            
            self.curPhase = self.getPhaseToRun()
            if self.curPhase >= self.PhaseWeStartAnimating:
                self.request('DoAnim')
        except:
            pass

    def handleNewPhase(self, newPhase):
        """Handle the  zero manager telling us we're in a new phase."""
        assert self.notify.debugStateCall(self)
        if newPhase < self.PhaseWeStartAnimating:
            self.request('Off')
        else:
            self.startIfNeeded()
