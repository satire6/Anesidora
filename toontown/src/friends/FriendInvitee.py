from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TTDialog
from otp.otpbase import OTPLocalizer
from toontown.toontowngui import ToonHeadDialog
from direct.gui.DirectGui import DGG
from otp.otpbase import OTPGlobals

class FriendInvitee(ToonHeadDialog.ToonHeadDialog):
    """FriendInvitee:
    This is a panel that pops up in the middle of your screen whenever
    someone invites to be his/her friend.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("FriendInvitee")

    def __init__(self, avId, avName, avDNA, context, **kw):

        self.avId = avId
        self.avName = avName
        self.avDNA = avDNA
        self.context = context

        # Dialog depends upon number of friends in friends list
        if (len(base.localAvatar.friendsList) >= MaxFriends):
            # Too many friends
            base.cr.friendManager.up_inviteeFriendResponse(
                3, self.context)
            self.context = None
            text =  OTPLocalizer.FriendInviteeTooManyFriends % (self.avName)
            style = TTDialog.Acknowledge
            buttonTextList = [OTPLocalizer.FriendInviteeOK]
            command = self.__handleOhWell
        else:
            # Room for more
            text = OTPLocalizer.FriendInviteeInvitation % (self.avName)
            style = TTDialog.TwoChoice
            buttonTextList = [OTPLocalizer.FriendInviteeOK,
                              OTPLocalizer.FriendInviteeNo]
            command = self.__handleButton

        optiondefs = (
            ('dialogName',    'FriendInvitee',        None),
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
        self.accept('cancelFriendInvitation', self.__handleCancelFromAbove)

        # Initialize dialog
        self.initialiseoptions(FriendInvitee)
        # Make sure dialog is visible by default
        self.show()

    def cleanup(self):
        """cleanup(self):
        Cancels any pending request and removes the panel from the
        screen, unanswered.
        """
        ToonHeadDialog.ToonHeadDialog.cleanup(self)
        self.ignore('cancelFriendInvitation')
        if self.context != None:
            # Send back a non-committal reply.
            base.cr.friendManager.up_inviteeFriendResponse(
                2, self.context)
            self.context = None
        
        if base.friendMode == 1:
            base.cr.friendManager.executeGameSpecificFunction()
        

    ### Button handing methods
    def __handleButton(self, value):
        print("handleButton")
        if value == DGG.DIALOG_OK:
            if base.friendMode == 0:
                base.cr.friendManager.up_inviteeFriendResponse(1, self.context)
            elif base.friendMode == 1:
                print("sending Request Invite")
                base.cr.avatarFriendsManager.sendRequestInvite(self.avId)              
        else:
            if base.friendMode == 0:
                base.cr.friendManager.up_inviteeFriendResponse(0, self.context)
            elif base.friendMode == 1:    
                base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
            
            
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


