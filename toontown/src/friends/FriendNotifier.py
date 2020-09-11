from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.toontowngui import ToonHeadDialog
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals

class FriendNotifier(ToonHeadDialog.ToonHeadDialog):
    """FriendInvitee:
    This is a panel that pops up in the middle of your screen whenever
    someone invites to be his/her friend.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("FriendNotifier")

    def __init__(self, avId, avName, avDNA, context, **kw):

        self.avId = avId
        self.avName = avName
        self.avDNA = avDNA
        self.context = context
        

        # Room for more
        text = OTPLocalizer.FriendNotifictation % (self.avName)
        style = TTDialog.Acknowledge
        buttonText = [OTPLocalizer.FriendInviteeOK, OTPLocalizer.FriendInviteeOK]
        command = self.__handleButton

        optiondefs = (
            ('dialogName',    'FriendInvitee',        None),
            ('text',          text,                   None),
            ('style',         style,                  None),
            ('buttonText',    buttonText,             None),
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
        self.initialiseoptions(FriendNotifier)
        # Make sure dialog is visible by default
        self.show()

    def cleanup(self):
        print("cleanup calling!")
        """cleanup(self):
        Cancels any pending request and removes the panel from the
        screen, unanswered.
        """
        ToonHeadDialog.ToonHeadDialog.cleanup(self)
        #self.ignore('cancelFriendInvitation')
        #if self.context != None:
        #    # Send back a non-committal reply.
        #    base.cr.friendManager.up_inviteeFriendResponse(
        #         2, self.context)
        #    self.context = None
        
        

    ### Button handing methods
    def __handleButton(self, value):
        if value == DGG.DIALOG_OK:
            #base.cr.friendManager.up_inviteeFriendResponse(
            #    1, self.context)
            #self.cleanup()
            #base.cr.avatarFriendsManager.sendRequestInvite(self.avId)
            pass
        else:
            pass
            #base.cr.friendManager.up_inviteeFriendResponse(
            #    0, self.context)
            #base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
        self.context = None
        self.cleanup()

    def __handleOhWell(self, value):
        self.cleanup()

    def __handleCancelFromAbove(self, context = None):
        if context == None or context == self.context:
            # We've just been told by the FriendManager to forget it;
            # the inviter has rescinded his/her offer.
            self.context = None
            self.cleanup()


