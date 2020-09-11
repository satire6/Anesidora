from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from otp.avatar import AvatarPanel
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from otp.distributed import CentralLogger

IGNORE_SCALE = 0.06
STOP_IGNORE_SCALE = 0.04

class AvatarPanelBase(AvatarPanel.AvatarPanel):
    """
    Base class to hold features in common between ToonPanel and PlayerPanel
    """

    def __init__(self, avatar, FriendsListPanel = None):
        self.dialog = None
        self.category = None
        AvatarPanel.AvatarPanel.__init__(self, avatar, FriendsListPanel)

    def getIgnoreButtonInfo(self):
        # determine how the ignore button should look and work based on the target avatar's current status
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            return (TTLocalizer.AvatarPanelStopIgnoring, self.handleStopIgnoring, STOP_IGNORE_SCALE)
        else:
            return (TTLocalizer.AvatarPanelIgnore, self.handleIgnore, IGNORE_SCALE)
    
    def handleIgnore(self):
        isAvatarFriend = base.cr.isFriend(self.avatar.doId)
        isPlayerFriend = base.cr.playerFriendsManager.isAvatarOwnerPlayerFriend(self.avatar.doId)
        
        isFriend = isAvatarFriend or isPlayerFriend
        

        if isFriend:
            # tell the player they can't ignore a friend
            self.dialog  = TTDialog.TTGlobalDialog(
                style = TTDialog.CancelOnly,
                text = TTLocalizer.IgnorePanelAddFriendAvatar % self.avName,
                text_wordwrap = 18.5,
                text_scale = 0.06,
                #okButtonText = TTLocalizer.AvatarPanelIgnoreCant,
                cancelButtonText = TTLocalizer.lCancel,
                doneEvent = "IgnoreBlocked",
                command = self.freeLocalAvatar, 
                )
        else:
        
            # put up an ignore confirmation dialog
            self.dialog  = TTDialog.TTGlobalDialog(
                style = TTDialog.TwoChoice,
                text = TTLocalizer.IgnorePanelAddIgnore % self.avName,
                text_wordwrap = 18.5,
                text_scale = TTLocalizer.APBignorePanelAddIgnoreTextScale,
                okButtonText = TTLocalizer.AvatarPanelIgnore,
                cancelButtonText = TTLocalizer.lCancel,
                doneEvent = "IgnoreConfirm",
                command = self.handleIgnoreConfirm, 
                )

        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            #pos = (0, 0, 0.15),
            pos = (0, TTLocalizer.APBignorePanelTitlePosY, 0.125),
            text = TTLocalizer.IgnorePanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleStopIgnoring(self):
        # put up a stop ignoring confirmation dialog
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.TwoChoice,
            text = TTLocalizer.IgnorePanelRemoveIgnore % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            okButtonText = TTLocalizer.AvatarPanelStopIgnoring,
            cancelButtonText = TTLocalizer.lCancel,
            buttonPadSF = 4.0,
            doneEvent = "StopIgnoringConfirm",
            command = self.handleStopIgnoringConfirm, 
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, TTLocalizer.APBignorePanelTitlePosY, 0.15),
            text = TTLocalizer.IgnorePanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleIgnoreConfirm(self, value):
        if value == -1:
            self.freeLocalAvatar()
            return
            
        # ignore target avId
        base.cr.avatarFriendsManager.addIgnore(self.avId)
        
        # notify user they are now ignoring avId
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.Acknowledge,
            text = TTLocalizer.IgnorePanelIgnore % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.1,
            doneEvent = "IgnoreComplete",
            command = self.handleDoneIgnoring,
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, TTLocalizer.APBignorePanelTitlePosY, 0.15),
            text = TTLocalizer.IgnorePanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleStopIgnoringConfirm(self, value):
        if value == -1:
            self.freeLocalAvatar()
            return
        
        # ignore target avId
        base.cr.avatarFriendsManager.removeIgnore(self.avId)

        # notify user they are now ignoring avId
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.Acknowledge,
            text = TTLocalizer.IgnorePanelEndIgnore % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.1,
            doneEvent = "StopIgnoringComplete",
            command = self.handleDoneIgnoring,
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, TTLocalizer.APBignorePanelTitlePosY, 0.15),
            text = TTLocalizer.IgnorePanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleDoneIgnoring(self, value):
        self.freeLocalAvatar()

    def handleReport(self):
        if base.cr.centralLogger.hasReportedPlayer(self.playerId, self.avId):
            self.alreadyReported()
        else:
            self.confirmReport()
            
    def confirmReport(self):
        # determine if we are friends already
        if base.cr.isFriend(self.avId) or base.cr.playerFriendsManager.isPlayerFriend(self.avId):
            string = TTLocalizer.ReportPanelBodyFriends
            titlePos = 0.410
        else:
            string = TTLocalizer.ReportPanelBody
            titlePos = 0.350

        # put up a confirmation dialog
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.TwoChoice,
            text = string % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            okButtonText = TTLocalizer.AvatarPanelReport,
            cancelButtonText = TTLocalizer.lCancel,
            doneEvent = "ReportConfirm",
            command = self.handleReportConfirm, 
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, 0, titlePos),
            text = TTLocalizer.ReportPanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleReportConfirm(self, value):
        self.cleanupDialog()
        if value == 1:
            self.chooseReportCategory()
        else:
            self.requestWalk()

    def alreadyReported(self):
        # already reported, notify user
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.Acknowledge,
            text = TTLocalizer.ReportPanelAlreadyReported % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.1,
            doneEvent = "AlreadyReported",
            command = self.handleAlreadyReported,
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, 0, 0.2),
            text = TTLocalizer.ReportPanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleAlreadyReported(self, value):
        self.freeLocalAvatar()
        
    def chooseReportCategory(self):
        # put up a confirmation dialog - need to make a custom one for buttons
        self.dialog  = TTDialog.TTGlobalDialog(
            pos = (0, 0, 0.2),
            style = TTDialog.CancelOnly,
            text = TTLocalizer.ReportPanelCategoryBody % (self.avName, self.avName),
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.05,
            midPad = 0.65,
            cancelButtonText = TTLocalizer.lCancel,
            doneEvent = "ReportCategory",
            command = self.handleReportCategory, 
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, 0, 0.225),
            text = TTLocalizer.ReportPanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )
        
        guiButton = loader.loadModel("phase_3/models/gui/quit_button")

        # Foul Language
        DirectButton(
            parent = self.dialog,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (2.125, 1.0, 1.0),
            text = TTLocalizer.ReportPanelCategoryLanguage,
            text_scale = 0.06,
            text_pos = (0, -0.0124),
            pos = (0, 0, -0.3),
            command = self.handleReportCategory,
            extraArgs = [0],
            )

        # Personal Info
        DirectButton(
            parent = self.dialog,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (2.25, 1.0, 1.0),
            text = TTLocalizer.ReportPanelCategoryPii,
            text_scale = 0.06,
            text_pos = (0, -0.0125),
            pos = (0, 0, -0.425),
            command = self.handleReportCategory,
            extraArgs = [1],
            )

        # Rude Behavior
        DirectButton(
            parent = self.dialog,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (2.125, 1.0, 1.0),
            text = TTLocalizer.ReportPanelCategoryRude,
            text_scale = 0.06,
            text_pos = (0, -0.0125),
            pos = (0, 0, -0.55),
            command = self.handleReportCategory,
            extraArgs = [2],
            )

        # Bad Name
        DirectButton(
            parent = self.dialog,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (2.125, 1.0, 1.0),
            text = TTLocalizer.ReportPanelCategoryName,
            text_scale = 0.06,
            text_pos = (0, -0.0125),
            pos = (0, 0, -0.675),
            command = self.handleReportCategory,
            extraArgs = [3],
            )
        
        guiButton.removeNode()
        self.dialog.show()
        self.__acceptStoppedStateMsg()
        self.requestStopped()

    def handleReportCategory(self, value):
        self.cleanupDialog()
        if value >= 0:
            # map into central logger tokens
            cat = [
                CentralLogger.ReportFoulLanguage,
                CentralLogger.ReportPersonalInfo,
                CentralLogger.ReportRudeBehavior,
                CentralLogger.ReportBadName,
                ]
            self.category = cat[value]
            self.confirmReportCategory(value)
        else:
            self.requestWalk()

    def confirmReportCategory(self, category):
        string = TTLocalizer.ReportPanelConfirmations[category]
        string += "\n\n" + TTLocalizer.ReportPanelWarning
        # put up a confirmation category dialog
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.TwoChoice,
            text = string % self.avName,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.1,
            okButtonText = TTLocalizer.AvatarPanelReport,
            cancelButtonText = TTLocalizer.lCancel,
            doneEvent = "ReportConfirmCategory",
            command = self.handleReportCategoryConfirm, 
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, 0, 0.5),
            text = TTLocalizer.ReportPanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        self.dialog.show()
        self.__acceptStoppedStateMsg()

    def handleReportCategoryConfirm(self, value):
        self.cleanupDialog()
        removed = 0
        isPlayer = 0
        if value > 0:
            # log the chat records
            base.cr.centralLogger.reportPlayer(self.category, self.playerId, self.avId)

            # if we are avatar friends, break the friendship
            if base.cr.isFriend(self.avId):
                base.cr.removeFriend(self.avId)
                removed = 1
                
            # if we are player friends, break the friendship
            if base.cr.playerFriendsManager.isPlayerFriend(self.playerId):
                if self.playerId:
                    base.cr.playerFriendsManager.sendRequestRemove(self.playerId)
                    removed = 1
                    isPlayer = 1
                
            # TODO: session-based ignore
            self.reportComplete(removed, isPlayer)
        else:
            self.requestWalk()

    def reportComplete(self, removed, isPlayer):
        # Notify user if we have removed a friend
        string = TTLocalizer.ReportPanelThanks
        titlePos = 0.25
        if removed:
            if isPlayer:
                string += " " + TTLocalizer.ReportPanelRemovedPlayerFriend % self.playerId
            else:
                string += " " + TTLocalizer.ReportPanelRemovedFriend % self.avName
                
            titlePos = 0.3

        # put up a confirmation category dialog
        self.dialog  = TTDialog.TTGlobalDialog(
            style = TTDialog.Acknowledge,
            text = string,
            text_wordwrap = 18.5,
            text_scale = 0.06,
            topPad = 0.1,
            doneEvent = "ReportComplete",
            command = self.handleReportComplete, 
            )
        
        # Title
        DirectLabel(
            parent = self.dialog,
            relief = None,
            pos = (0, 0, titlePos),
            text = TTLocalizer.ReportPanelTitle,
            textMayChange = 0,
            text_scale = 0.08,
            )

        # TODO: notify user we are ignoring

        self.dialog.show()
        self.__acceptStoppedStateMsg()

    def handleReportComplete(self, value):
        self.freeLocalAvatar()
        
    def freeLocalAvatar(self, value = None):
        self.cleanupDialog()
        self.requestWalk()
        
    def cleanupDialog(self):
        if self.dialog:
            self.dialog.ignore("exitingStoppedState")
            self.dialog.cleanup()
            self.dialog = None

    def requestStopped(self):
        """Safely go to the stopped state for the place."""
        #Make sure we aren't in the stickerBook state or else we can get into a bad state where the player gets stuck
        if not base.cr.playGame.getPlace().fsm.getCurrentState().getName() == "stickerBook":
            if base.cr.playGame.getPlace().fsm.hasStateNamed('stopped'): 
                base.cr.playGame.getPlace().fsm.request('stopped')
            else:
                self.notify.warning('skipping request to stopped in %s' %
                                    base.cr.playGame.getPlace())
        else:
            self.cleanup()
            
    def requestWalk(self):
        """Safely go to the walked state for the place."""
        if base.cr.playGame.getPlace().fsm.hasStateNamed('finalBattle'):
            # if we go to walk, toons can teleport out in the middle
            # of a boss battle
            base.cr.playGame.getPlace().fsm.request('finalBattle')
        elif base.cr.playGame.getPlace().fsm.hasStateNamed('walk'):
            # Go to the walk state only if you were in the stopped state.
            if (base.cr.playGame.getPlace().getState() == 'stopped'):
                base.cr.playGame.getPlace().fsm.request('walk')
        else:
            self.notify.warning('skipping request to walk in %s' %
                                base.cr.playGame.getPlace())

    def __acceptStoppedStateMsg(self):
        # The player might be able to exit the stop state either through some other
        # panel or if his boarding party leader boards the elevator. Close any other
        # panels like report or ignore if the toon moves out of the stopped state.
        self.dialog.ignore("exitingStoppedState")
        self.dialog.accept("exitingStoppedState", self.cleanupDialog)