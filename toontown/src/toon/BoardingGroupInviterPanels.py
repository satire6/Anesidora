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
    
class BoardingGroupInviterPanels:
    """
    BoardingGroupInviterPanels:
    This is the class that controls the BoardingGroupInvitingPanel
    and the BoardingGroupInvitationRejectedPanel.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("BoardingGroupInviterPanels")
    
    def __init__(self):
        self.__invitingPanel = None
        self.__invitationRejectedPanel = None
        if __debug__:
            base.inviterPanels = self
        
    def cleanup(self):
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()
    
    def createInvitingPanel(self, boardingParty, inviteeId, **kw):
        """
        This methotd opens the Boarding Group Inviting Panel, 
        after destroying any previously opened panels.
        """
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()
        self.notify.debug('Creating Inviting Panel.')
        self.__invitingPanel = BoardingGroupInvitingPanel(boardingParty, inviteeId, **kw)
    
    def createInvitationRejectedPanel(self, boardingParty, inviteeId, **kw):
        """
        This method opens the Boarding Group Invititation Rejected Panel,
        after destroying any previously opened panels.
        """
        self.destroyInvitingPanel()
        self.destroyInvitationRejectedPanel()
        self.notify.debug('Creating Invititation Rejected Panel.')
        self.__invitationRejectedPanel = BoardingGroupInvitationRejectedPanel(boardingParty, inviteeId, **kw)
        
    def destroyInvitingPanel(self):
        """
        This method destroys any open Boarding Group Inviting Panel.
        """
        if self.isInvitingPanelUp():
            self.__invitingPanel.cleanup()
            self.__invitingPanel = None
    
    def destroyInvitationRejectedPanel(self):
        """
        This method destroys any open Boarding Group Invititation Rejected Panel.
        """
        if self.isInvitationRejectedPanelUp():
            self.__invitationRejectedPanel.cleanup()
            self.__invitationRejectedPanel = None
            
    def isInvitingPanelIdCorrect(self, inviteeId):
        """
        Helper function to verify whether we're dealing with a panel of the same invitee.
        """
        if self.isInvitingPanelUp():
            if (inviteeId == self.__invitingPanel.avId):
                return True
            else:
                self.notify.warning('Got a response back from an invitee, but a different invitee panel was open. Maybe lag?')
        return False
    
    def isInvitingPanelUp(self):
        """
        Helper function to determine whether any Inviting panel is up or not.
        """        
        if self.__invitingPanel:            
            if not self.__invitingPanel.isEmpty():
                return True
            self.__invitingPanel = None
        return False
        
    def isInvitationRejectedPanelUp(self):
        """
        Helper function to determine whether any Invitation Rejected panel is up or not.
        """
        if self.__invitationRejectedPanel:            
            if not self.__invitationRejectedPanel.isEmpty():
                return True
            self.__invitationRejectedPanel = None
        return False
        
    def forceCleanup(self):
        """
        Cancels any pending request and removes the panel from the screen, unanswered.
        This should be called only when the toon leaves the zone with an unanswered panel.
        """
        if self.isInvitingPanelUp():
            self.__invitingPanel.forceCleanup()
            self.__invitingPanel = None
        
        if self.isInvitationRejectedPanelUp():
            self.__invitationRejectedPanel.forceCleanup()
            self.__invitationRejectedPanel = None
        
class BoardingGroupInviterPanelBase(ToonHeadDialog.ToonHeadDialog):
    """
    BoardingGroupInviter:
    This is a panel that pops up in the middle of your screen whenever
    you invite someone to your Boarding Group.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("BoardingGroupInviterPanelBase")
    
    def __init__(self, boardingParty, inviteeId, **kw):
        if __debug__:
            base.inviterPanel = self
        self.boardingParty = boardingParty
        self.avId = inviteeId
        avatar = base.cr.doId2do.get(self.avId)
        self.avatarName = ''
        if avatar:
            self.avatar = avatar
            self.avatarName = avatar.getName()
            avatarDNA = avatar.getStyle()
        
        # Get all the parameters from the derived class
        self.defineParams()
        
        command = self.handleButton
        optiondefs = (
            ('dialogName',    self.dialogName,        None),
            ('text',          self.inviterText,       None),
            ('style',         self.panelStyle,        None),
            ('buttonTextList',self.buttonTextList,    None),
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
        # Initialize our base class.
        ToonHeadDialog.ToonHeadDialog.__init__(self, avatarDNA)
        # Make sure dialog is visible by default
        self.show()
        
    def defineParams(self):
        self.notify.error('setupParams: This method should not be called from the base class. Derived class should override this method')
    
    def cleanup(self):
        """
        Removes the panel from the screen.
        """
        self.notify.debug('Destroying Panel.')
        ToonHeadDialog.ToonHeadDialog.cleanup(self)
        
    def forceCleanup(self):
        """
        Cancels any pending request and removes the panel from the screen, unanswered.
        This should be called only when the toon leaves the zone with an unanswered panel.
        """
        self.handleButton(0)
        
    def handleButton(self, value):
        self.cleanup()
        
        
class BoardingGroupInvitingPanel(BoardingGroupInviterPanelBase):
    """
    BoardingGroupInvitingPanel:
    This is a panel that pops up in the middle of your screen whenever
    you invite someone to your Boarding Group.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("BoardingGroupInvitingPanel")
    
    def __init__(self, boardingParty, inviteeId, **kw):
        BoardingGroupInviterPanelBase.__init__(self, boardingParty, inviteeId, **kw)
        # Initialize the dialog
        self.initialiseoptions(BoardingGroupInvitingPanel)
        self.setupUnexpectedExitHooks()
        
    def defineParams(self):
        self.dialogName = 'BoardingGroupInvitingPanel'
        self.inviterText = TTLocalizer.BoardingInvitingMessage %self.avatarName
        self.panelStyle = TTDialog.CancelOnly
        self.buttonTextList = [OTPLocalizer.GuildInviterCancel]
        
    def handleButton(self, value):
        self.boardingParty.requestCancelInvite(self.avId)
        BoardingGroupInviterPanelBase.cleanup(self)
        
    def setupUnexpectedExitHooks(self):
        """Setup hooks to inform us when other toons exit unexpectedly."""
        if base.cr.doId2do.has_key(self.avId):
            toon = base.cr.doId2do[self.avId]
            self.unexpectedExitEventName = toon.uniqueName('disable')
            self.accept(self.unexpectedExitEventName, self.forceCleanup)
            
    def forceCleanup(self):
        self.ignore(self.unexpectedExitEventName)
        BoardingGroupInviterPanelBase.forceCleanup(self)
        
        
class BoardingGroupInvitationRejectedPanel(BoardingGroupInviterPanelBase):
    """
    BoardingGroupInvitationRejectedPanel:
    This is a panel that pops up in the middle of your screen whenever
    someone rejected your invitation to the Boarding Group.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("BoardingGroupInvitationRejectedPanel")
    
    def __init__(self, boardingParty, inviteeId, **kw):
        BoardingGroupInviterPanelBase.__init__(self, boardingParty, inviteeId, **kw)
        # Initialize the dialog
        self.initialiseoptions(BoardingGroupInvitationRejectedPanel)
        
    def defineParams(self):
        self.dialogName = 'BoardingGroupInvitationRejectedPanel'
        self.inviterText = TTLocalizer.BoardingInvitationRejected %self.avatarName
        self.panelStyle = TTDialog.Acknowledge
        self.buttonTextList = [OTPLocalizer.GuildInviterOK]