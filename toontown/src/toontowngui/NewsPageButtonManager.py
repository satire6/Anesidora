from pandac.PandaModules import VBase4, VBase3
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectButton import DirectButton
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *
from toontown.toonbase import TTLocalizer

class NewsPageButtonManager (FSM.FSM):
    """This will control which button shows up in the HUD, the Goto News, Goto Prev Page, or Goto 3d World."""
    notify = DirectNotifyGlobal.directNotify.newCategory("NewsPageButtonManager")
    
    def __init__(self):
        """Create the buttons."""
        FSM.FSM.__init__(self,"NewsPageButtonManager")
        self.buttonsLoaded = False
        self.goingToNewsPageFrom3dWorld = False
        self.goingToNewsPageFromStickerBook = False
        self.__blinkIval = None

        self.load()
            
##        if not launcher.getPhaseComplete(5.5):
##            # We haven't downloaded phase 5.5 yet; set a callback hook
##            # so the pages will load when we do get phase 5.5.
##            self.acceptOnce('phaseComplete-5.5', self.delayedLoadPhase55Stuff)
##            return
##        else:
##            self.loadPhase55Stuff()
##
##    def delayedLoadPhase55Stuff(self):
##        """Load the buttons, and then show the appropriate button."""
##        # we've just finished downloading phase 55
##        self.loadPhase55Stuff()
##        self.showAppropriateButton()

    def load(self):
        """
        We're now loading the assets from phase 3.5.
        """
        btnGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_ign_newsBtnGui')
        self.openNewNewsUp = btnGui.find('**/tt_t_gui_ign_new')
        self.openNewNewsUpBlink = btnGui.find('**/tt_t_gui_ign_newBlink')
        self.openNewNewsHover = btnGui.find('**/tt_t_gui_ign_newHover')
        self.openOldNewsUp = btnGui.find('**/tt_t_gui_ign_oldNews')
        self.openOldNewsHover = btnGui.find('**/tt_t_gui_ign_oldHover')
        self.closeNewsUp = btnGui.find('**/tt_t_gui_ign_open')
        self.closeNewsHover = btnGui.find('**/tt_t_gui_ign_closeHover')
        btnGui.removeNode()
        
        oldScale = 0.5
        newScale = 0.9
        newPos = VBase3(0.914, 0, 0.862)
        textScale = 0.06
        self.gotoNewsButton = DirectButton(
            relief = None,
            image = (self.openOldNewsUp, self.openOldNewsHover, self.openOldNewsHover),
            text = ('', TTLocalizer.EventsPageNewsTabName, TTLocalizer.EventsPageNewsTabName), # TODO replace this with a symbol
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = textScale,
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = newPos,
            scale = newScale,
            command = self.__handleGotoNewsButton,
            )
        
        self.newIssueButton = DirectButton(
            relief = None,
            image = (self.openNewNewsUp, self.openNewNewsHover, self.openNewNewsHover),
            text = ('', TTLocalizer.EventsPageNewsTabName, TTLocalizer.EventsPageNewsTabName), # TODO replace this with a symbol
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = textScale,
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = newPos,
            scale = newScale,
            command = self.__handleGotoNewsButton,
            )
        
        self.gotoPrevPageButton = DirectButton(
            relief = None,
            image = (self.closeNewsUp, self.closeNewsHover, self.closeNewsHover),
            text = ('', TTLocalizer.lClose, TTLocalizer.lClose), #"goto prev page", # TODO replace this with a synmbol
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = textScale,
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = newPos,
            scale = newScale,
            command = self.__handleGotoPrevPageButton,
            )

        self.goto3dWorldButton = DirectButton(
            relief = None,
            image = (self.closeNewsUp, self.closeNewsHover, self.closeNewsHover),
            text = ('', TTLocalizer.lClose, TTLocalizer.lClose), # "goto 3d world", # TODO replace this with a symbol
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = textScale,
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = newPos,
            scale = newScale,
            command = self.__handleGoto3dWorldButton,
            ) 

        self.newIssueButton.hide()
        self.gotoNewsButton.hide()
        self.gotoPrevPageButton.hide()
        self.goto3dWorldButton.hide()


        self.accept('newIssueOut', self.handleNewIssueOut)
        
        bounce1Pos = VBase3(newPos.getX(), newPos.getY(), newPos.getZ() + 0.022)    # (0.914, 0, 0.902)
        bounce2Pos = VBase3(newPos.getX(), newPos.getY(), newPos.getZ() + 0.015)    # (0.914, 0, 0.895)
        
        bounceIval = Sequence(
            LerpPosInterval(self.newIssueButton, 0.1, bounce1Pos, blendType = 'easeOut'),
            LerpPosInterval(self.newIssueButton, 0.1, newPos, blendType = 'easeIn'),
            LerpPosInterval(self.newIssueButton, 0.07, bounce2Pos, blendType = 'easeOut'),
            LerpPosInterval(self.newIssueButton, 0.07, newPos, blendType = 'easeIn')
        )
        
        self.__blinkIval = Sequence(
            Func(self.__showOpenEyes), Wait(2),
            bounceIval, Wait (0.5),
            Func(self.__showClosedEyes), Wait(0.1),
            Func(self.__showOpenEyes), Wait(0.1),
            Func(self.__showClosedEyes), Wait(0.1),
            )
            
        

        # Start it looping, but pause it, so we can resume/pause it to
        # start/stop the flashing.
        self.__blinkIval.loop()
        self.__blinkIval.pause()
        
        self.buttonsLoaded = True
        
    def __showOpenEyes(self):
        self.newIssueButton['image'] = (self.openNewNewsUp, self.openNewNewsHover, self.openNewNewsHover)
            
    def __showClosedEyes(self):
        self.newIssueButton['image'] = (self.openNewNewsUpBlink, self.openNewNewsHover, self.openNewNewsHover)
    
    def clearGoingToNewsInfo(self):
        """Clear our flags on how we got to the news page."""
        self.goingToNewsPageFrom3dWorld = False
        self.goingToNewsPageFromStickerBook = False

    def __handleGotoNewsButton(self):
        # Don't open news if we are jumping
        currentState = base.localAvatar.animFSM.getCurrentState().getName()
        if currentState == 'jumpAirborne':
            return
        assert self.notify.debugStateCall(self)
        from toontown.toon import LocalToon # must do import here to stop cyclic reference
        if not LocalToon.WantNewsPage:
            return
        if base.cr and base.cr.playGame and base.cr.playGame.getPlace() and base.cr.playGame.getPlace().fsm:
            fsm = base.cr.playGame.getPlace().fsm
            curState = fsm.getCurrentState().getName()
            if curState == 'walk':
                if hasattr(localAvatar, "newsPage"):
                    base.cr.centralLogger.writeClientEvent("news gotoNewsButton clicked")
                    localAvatar.book.setPage(localAvatar.newsPage)
                    fsm.request("stickerBook")
                    self.goingToNewsPageFrom3dWorld = True
            elif curState == 'stickerBook':
                if hasattr(localAvatar, "newsPage"):
                    base.cr.centralLogger.writeClientEvent("news gotoNewsButton clicked")
                    localAvatar.book.setPage(localAvatar.newsPage)
                    fsm.request("stickerBook")
                    self.goingToNewsPageFromStickerBook = True
                    self.showAppropriateButton()
                    


    def __handleGotoPrevPageButton(self):
        assert self.notify.debugStateCall(self)
        localAvatar.book.setPageBeforeNews()
        self.clearGoingToNewsInfo()
        self.showAppropriateButton()
        pass

    def __handleGoto3dWorldButton(self):
        assert self.notify.debugStateCall(self)
        localAvatar.book.closeBook()
        pass
            

    def hideAllButtons(self):
        """Hide everything."""
        if not self.buttonsLoaded:
            return
        self.gotoNewsButton.hide()
        self.gotoPrevPageButton.hide()
        self.goto3dWorldButton.hide()
        self.newIssueButton.hide()
        self.__blinkIval.pause()

    def enterHidden(self):
        """There are times when we don't want any of this buttons to show, like when the shtikerbook is hidden."""
        self.hideAllButtons()

    def exitHidden(self):
        pass

    def enterNormalWalk(self):
        """The usual state when the avatar is just walking around the world."""
        if not self.buttonsLoaded:
            return

        if localAvatar.getLastTimeReadNews() < base.cr.inGameNewsMgr.getLatestIssue():
            self.gotoNewsButton.hide()
            self.newIssueButton.show()
            self.__blinkIval.resume()
        else:
            self.gotoNewsButton.show()
            self.newIssueButton.hide()
        self.gotoPrevPageButton.hide()
        self.goto3dWorldButton.hide()

    def exitNormalWalk(self):
        if not self.buttonsLoaded:
            return
        self.hideAllButtons()

    def enterGotoWorld(self):
        """We got here by directly clicking on the goto news button from the 3d world."""
        if not self.buttonsLoaded:
            return
        self.hideAllButtons()
        self.goto3dWorldButton.show()

    def exitGotoWorld(self):
        """Fix our state properly."""
        if not self.buttonsLoaded:
            return
        self.hideAllButtons()
        localAvatar.book.setPageBeforeNews(enterPage = False)
        self.clearGoingToNewsInfo()

    def enterPrevPage(self):
        """We got here by directly clicking on the goto news button from the sticker book."""
        if not self.buttonsLoaded:
            return
        self.hideAllButtons()
        self.gotoPrevPageButton.show()

    def exitPrevPage(self):
        """Fix our state properly."""
        if not self.buttonsLoaded:
            return
        self.hideAllButtons()
##        localAvatar.book.setPageBeforeNews()
        self.clearGoingToNewsInfo()
    
    def showAppropriateButton(self):
        """We know we want to show one of the 3 buttons, figure out which one."""
        self.notify.debugStateCall(self)
        from toontown.toon import LocalToon # must do import here to stop cyclic reference
        if not LocalToon.WantNewsPage:
            return
        if not self.buttonsLoaded:
            return
        if base.cr and base.cr.playGame and base.cr.playGame.getPlace() and \
           hasattr(base.cr.playGame.getPlace(),'fsm') and base.cr.playGame.getPlace().fsm:
            fsm = base.cr.playGame.getPlace().fsm
            curState = fsm.getCurrentState().getName()
            # do not show the news page button if we are in the tutorial
            # or in cog hq lobbies
            if curState == 'walk':
                if localAvatar.tutorialAck and not localAvatar.isDisguised:
                    self.request("NormalWalk")
                else:
                    self.request("Hidden")
            elif curState == 'stickerBook':
                if self.goingToNewsPageFrom3dWorld:
                    if localAvatar.tutorialAck:
                        self.request("GotoWorld")
                    else:
                        self.request("Hidden")
                elif self.goingToNewsPageFromStickerBook:
                    if localAvatar.tutorialAck:
                        self.request("PrevPage")
                    else:
                        self.request("Hidden")
                else:
                    # we get here when he just clicked on the sticker book button
                    if localAvatar.tutorialAck:
                        self.request("NormalWalk")
                    else:
                        self.request("Hidden")

                
    def setGoingToNewsPageFromStickerBook(self, newVal):
        """Called when the news page tab gets clicked in sticker book."""
        assert self.notify.debugStateCall(self)
        self.goingToNewsPageFromStickerBook = newVal

    def enterOff(self):
        """Clean up the buttons."""
        self.ignoreAll()
        if not self.buttonsLoaded:
            return
                
        if self.__blinkIval:
            self.__blinkIval.finish()
            self.__blinkIval = None
        
        self.gotoNewsButton.destroy()
        self.newIssueButton.destroy()
        self.gotoPrevPageButton.destroy()
        self.goto3dWorldButton.destroy()
        
        del self.openNewNewsUp
        del self.openNewNewsUpBlink
        del self.openNewNewsHover
        del self.openOldNewsUp
        del self.openOldNewsHover
        del self.closeNewsUp
        del self.closeNewsHover

    def exitOff(self):
        """Print a warning if we get here."""
        self.notify.warning('Should not get here. NewsPageButtonManager.exitOff')

    def simulateEscapeKeyPress(self):
        # Go back to the 3D World if you have come from the 3D World.
        if self.goingToNewsPageFrom3dWorld:
            self.__handleGoto3dWorldButton()        
        # Else, go back to the previous page in the shticker book if you have come from there.
        if self.goingToNewsPageFromStickerBook:
            self.__handleGotoPrevPageButton()

    def handleNewIssueOut(self):
        """Handle the message that a new issue has been released."""
        # Our code does not deal with the case when it gets the new issue out message
        # while you are reading the news
        if localAvatar.isReadingNews():
            # do nothing he'll get informed when he closes the news that there's a new issue
            pass
        else:
            self.showAppropriateButton()
