from toontown.hood import ZeroAnimatedProp
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal


class MailboxTwoAnimatedProp(ZeroAnimatedProp.ZeroAnimatedProp):
    """Our mailbox two class that gradually increases movements."""

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'MailboxTwoAnimatedProp')

    PauseTimeMult = base.config.GetFloat('zero-pause-mult', 1.0)

    PhaseInfo = {
        0 : ('tt_a_ara_dod_mailbox_firstMoveFlagSpin1', 40 * PauseTimeMult),
        1 : (('tt_a_ara_dod_mailbox_firstMoveStruggle',
              'tt_a_ara_dod_mailbox_firstMoveJump')
             , 20 * PauseTimeMult),
        2 : ('tt_a_ara_dod_mailbox_firstMoveFlagSpin2', 10 * PauseTimeMult),
        3 : ('tt_a_ara_dod_mailbox_firstMoveFlagSpin3',8 * PauseTimeMult),
        4 : ('tt_a_ara_dod_mailbox_firstMoveJumpSummersault',6 * PauseTimeMult),
        5 : ('tt_a_ara_dod_mailbox_firstMoveJumpFall',4 * PauseTimeMult),
        6 : ('tt_a_ara_dod_mailbox_firstMoveJump3Summersaults',2 * PauseTimeMult),        
        }

    PhaseWeStartAnimating = 5
    
    def __init__(self, node):
        """Constuct ourself and correct assumptions in base class."""
        ZeroAnimatedProp.ZeroAnimatedProp.__init__(self, node,
                                                   'mailbox',
                                                   self.PhaseInfo,
                                                   ToontownGlobals.MAILBOX_ZERO_HOLIDAY
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
