from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.toontowngui import ToonHeadDialog
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals
from toontown.toonbase import TTLocalizer

class GroupInvitee(ToonHeadDialog.ToonHeadDialog):
    """GroupInvitee:
    This is a panel that pops up in the middle of your screen whenever
    someone invites you to a group.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("GroupInvitee")

    def __init__(self):
        pass

        
    def make(self, party,toon, leaderId, **kw):
        self.leaderId = leaderId
        self.avName = toon.getName()
        self.av = toon
        self.avId = toon.doId
        self.avDNA = toon.getStyle()
        self.party = party
        # Dialog depends upon number of friends in friends list
   
        text = TTLocalizer.BoardingInviteeMessage % (self.avName)
        style = TTDialog.TwoChoice
        buttonTextList = [OTPLocalizer.FriendInviteeOK,
                          OTPLocalizer.FriendInviteeNo]
        command = self.__handleButton

        optiondefs = (
            ('dialogName',    'GroupInvitee',        None),
            ('text',          text,                   None),
            ('style',         style,                  None),
            ('buttonTextList',buttonTextList,         None),
            ('command',       command,                None),
            ('image_color',   (1.0, 0.89, 0.77, 1.0), None),
            # Make the head smaller so the panel can be smaller
            ('geom_scale',    0.2,                    None),
            # Don't have to move it over as much
            ('geom_pos',      (-0.1,0,-0.025),        None),
            # Reduce padding
            ('pad',           (0.075,0.075),          None),
            ('topPad',        0,                      None),
            ('midPad',        0,                      None),
            # Position panel right next to friends panel
            ('pos',           (0.45, 0, 0.75),        None),
            ('scale',         0.75,                   None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # initialize our base class.
        ToonHeadDialog.ToonHeadDialog.__init__(self, self.avDNA)

        # Add cancel hook
        #self.accept('cancelFriendInvitation', self.__handleCancelFromAbove)

        # Initialize dialog
        self.initialiseoptions(GroupInvitee)
        # Make sure dialog is visible by default
        self.show()

    def cleanup(self):
        """cleanup(self):
        Removes the panel from the screen.
        """
        ToonHeadDialog.ToonHeadDialog.cleanup(self)
        
    def forceCleanup(self):
        """
        Cancels any pending request and removes the panel from the screen, unanswered.
        This should be called only when the toon leaves the zone with an unanswered panel.
        """
        self.party.requestRejectInvite(self.leaderId, self.avId)
        self.cleanup()

    ### Button handing methods
    def __handleButton(self, value):
        # Don't request to leave if the toon is already in the elevator.
        # Automatically send a reject if the toon is in the elevator.
        place = base.cr.playGame.getPlace()
        if (value == DGG.DIALOG_OK) and place and not (place.getState() == 'elevator'):
            self.party.requestAcceptInvite(self.leaderId, self.avId)
        else:
            self.party.requestRejectInvite(self.leaderId, self.avId)
        self.cleanup()