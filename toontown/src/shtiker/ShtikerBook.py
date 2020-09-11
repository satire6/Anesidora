"""ShtikerBook module: contains the ShtikerBook class"""

from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.effects import DistributedFireworkShow
from toontown.parties import DistributedPartyFireworksActivity
from direct.directnotify import DirectNotifyGlobal

class ShtikerBook(DirectFrame, StateData.StateData):
    """ShtikerBook class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("ShtikerBook")
    
    # special methods
    def __init__(self, doneEvent):
        DirectFrame.__init__(self,
                             relief = None,
                             sortOrder = DGG.BACKGROUND_SORT_INDEX)
        self.initialiseoptions(ShtikerBook)
        StateData.StateData.__init__(self, doneEvent)
        self.pages = []
        self.pageTabs = []
        self.currPageTabIndex = None
        self.pageTabFrame = DirectFrame(parent = self, relief = None,
                                        pos = (0.93, 1, 0.575),
                                        scale = 1.25)
        self.pageTabFrame.hide()
        self.currPageIndex = None
        # what was the last shtiker page he was on before he went to news
        self.pageBeforeNews = None 
        self.entered = 0
        self.safeMode = 0
        self.__obscured = 0
        self.__shown = 0
        self.__isOpen = 0
        self.hide()
        # Slide the whole book up a tad to keep it out of the space
        # reserved for the onscreen chat balloons.
        self.setPos(0, 0, 0.1)
        
        self.pageOrder = [
            TTLocalizer.OptionsPageTitle,
            TTLocalizer.ShardPageTitle,
            TTLocalizer.MapPageTitle,
            TTLocalizer.InventoryPageTitle,
            TTLocalizer.QuestPageToonTasks,
            TTLocalizer.TrackPageShortTitle,
            TTLocalizer.SuitPageTitle,
            TTLocalizer.FishPageTitle,
            TTLocalizer.KartPageTitle,
            TTLocalizer.DisguisePageTitle,
            TTLocalizer.NPCFriendPageTitle,
            TTLocalizer.GardenPageTitle,
            TTLocalizer.GolfPageTitle,
            TTLocalizer.EventsPageName,
            TTLocalizer.NewsPageName
        ]
        
        if __debug__:
            base.sb = self

    def setSafeMode(self, setting):
        """
        Safe Mode is primarily used for the tutorial. When pages enter(), they
        should check this flag on the book to turn off buttons or options that
        may allow the guest to escape or otherwise damage the movie
        """
        self.safeMode = setting

    def enter(self):
        if self.entered:
            return
        self.entered = 1
        
        # If we're currently in move-furniture mode, stop it.
        messenger.send("releaseDirector")
        
        # Send a message saying that we have entered. We can use this to hide boarding gui, etc.
        messenger.send("stickerBookEntered")

        # play the book open sound
        base.playSfx(self.openSound)
        
        # turn off any user control
        base.disableMouse()

        # hide the world and turn on screen clear color
        base.render.hide()
        base.setBackgroundColor(0.05, 0.15, 0.4)

        # Turn off the one nametag cell that obscures some of the page
        # tabs.
        base.setCellsAvailable([base.rightCells[0]], 0)

        # Make the onscreen chat messages, etc. be somewhat more opaque.
        self.oldMin2dAlpha = NametagGlobals.getMin2dAlpha()
        self.oldMax2dAlpha = NametagGlobals.getMax2dAlpha()
        NametagGlobals.setMin2dAlpha(0.8)
        NametagGlobals.setMax2dAlpha(1.0)

        # switch from the open to the close button
        self.__isOpen = 1
        self.__setButtonVisibility()

        # manage the book
        self.show()
        self.showPageArrows()
        
        if not self.safeMode:
            # register events
            self.accept("shtiker-page-done", self.__pageDone)
            self.accept(ToontownGlobals.StickerBookHotkey, self.__close)
            # Add hooks so the keyboard arrow keys work too
##            self.accept("arrow_right", self.__pageChange, [1])
##            self.accept("arrow_left", self.__pageChange, [-1])
            # Show the jump buttons
            self.pageTabFrame.show()

        # Enter the current page
        self.pages[self.currPageIndex].enter()

    def exit(self):
        """exit(self)
        Remove events and restore display
        """
        if not self.entered:
            return
        self.entered = 0
        
        # Send a message saying that we have exited. We can use this to show boarding gui, etc.
        messenger.send("stickerBookExited")

        # play the book open sound
        base.playSfx(self.closeSound)
        
        # Exit the current pagex
        self.pages[self.currPageIndex].exit()
        
        # put the world back
        base.render.show()
        
        setBlackBackground = 0
        for obj in base.cr.doId2do.values():
            if isinstance(obj, DistributedFireworkShow.DistributedFireworkShow) or \
                isinstance(obj, DistributedPartyFireworksActivity.DistributedPartyFireworksActivity):
                setBlackBackground = 1
        
        if setBlackBackground:
            base.setBackgroundColor(Vec4(0,0,0,1))
        else:
            base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

        # Force all the textures to reload, just in case we switched
        # GSG's from the OptionsPage while the book was open.
        gsg = base.win.getGsg()
        if gsg:
            base.render.prepareScene(gsg)

        # Restore the opacity of the chat messages and nametags.
        NametagGlobals.setMin2dAlpha(self.oldMin2dAlpha)
        NametagGlobals.setMax2dAlpha(self.oldMax2dAlpha)

        # Restore the nametag cell.
        base.setCellsAvailable([base.rightCells[0]], 1)

        # unmanage interface
        self.__isOpen = 0
        self.hide()
        self.hideButton()

        # kill any open dialog boxes
        cleanupDialog("globalDialog")

        # Hide the page tabs in case you enter in safe mode next time
        self.pageTabFrame.hide()

        self.ignore("shtiker-page-done")
        self.ignore(ToontownGlobals.StickerBookHotkey)
        self.ignore("arrow_right")
        self.ignore("arrow_left")

    def load(self):
        """load(self)
        """
        self.checkGardenStarted = localAvatar.getGardenStarted()
        # models
        bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
        self['image'] = bookModel.find("**/big_book")
        self['image_scale'] = (2,1,1.5)
        self.resetFrameSize()
        
        self.bookOpenButton = DirectButton(
            image = (bookModel.find("**/BookIcon_CLSD"),
                     bookModel.find("**/BookIcon_OPEN"),
                     bookModel.find("**/BookIcon_RLVR"),
                     ),
            relief = None,
            pos = (1.175, 0, -0.83),
            scale = 0.305,
            command = self.__open,
            )
        
        self.bookCloseButton = DirectButton(
            image = (bookModel.find("**/BookIcon_OPEN"),
                     bookModel.find("**/BookIcon_CLSD"),
                     bookModel.find("**/BookIcon_RLVR2"),
                     ),
            relief = None,
            pos = (1.175, 0, -0.83),
            scale = 0.305,
            command = self.__close,
            )
                      
        self.bookOpenButton.hide()
        self.bookCloseButton.hide()

        self.nextArrow = DirectButton(
            parent = self,
            relief = None,
            image = (bookModel.find("**/arrow_button"),
                     bookModel.find("**/arrow_down"),
                     bookModel.find("**/arrow_rollover"),
                     ),
            scale = (0.1, 0.1, 0.1),
            pos = (0.838, 0, -0.661),
            command = self.__pageChange,
            extraArgs = [1],
            )

        self.prevArrow = DirectButton(
            parent = self,
            relief = None,
            image = (bookModel.find("**/arrow_button"),
                     bookModel.find("**/arrow_down"),
                     bookModel.find("**/arrow_rollover"),
                     ),
            scale = (-0.1, 0.1, 0.1), # negative to flip the image
            pos = (-0.838, 0, -0.661),
            command = self.__pageChange,
            extraArgs = [-1],
            )                     

        bookModel.removeNode()

        # sounds
        self.openSound = base.loadSfx(
            "phase_3.5/audio/sfx/GUI_stickerbook_open.mp3")
        self.closeSound = base.loadSfx(
            "phase_3.5/audio/sfx/GUI_stickerbook_delete.mp3")
        self.pageSound = base.loadSfx(
            "phase_3.5/audio/sfx/GUI_stickerbook_turn.mp3")

    def unload(self):
        """unload(self)
        """
        loader.unloadModel("phase_3.5/models/gui/stickerbook_gui")

        self.destroy()
        self.bookOpenButton.destroy()
        del self.bookOpenButton
        self.bookCloseButton.destroy()
        del self.bookCloseButton

        self.nextArrow.destroy()
        del self.nextArrow
        self.prevArrow.destroy()
        del self.prevArrow

        for page in self.pages:
            page.unload()
        del self.pages

        for pageTab in self.pageTabs:
            pageTab.destroy()
        del self.pageTabs
        del self.currPageTabIndex

        del self.openSound
        del self.closeSound
        del self.pageSound

    def addPage(self, page, pageName = 'Page'):
        """addPage(self, ShtikerPage)
        add a page to the ShtikerBook ClassicFSM"""
        if not (pageName in self.pageOrder):
            self.notify.error('Trying to add page %s in the ShtickerBook. Page not listed in the order.' %pageName)
            return
        
        pageIndex = 0
        if len(self.pages):
            newIndex = len(self.pages)
            prevIndex = newIndex - 1
            
            # A page probably came in late. This page has to be inserted before the
            # News Page, which happens to be the last page.
            # This is done so that there is no gap in the tabs on the right side.
            # Take care of all the indices now while inserting the new page.
                        
            if (self.pages[prevIndex].pageName == TTLocalizer.NewsPageName):
                self.pages.insert(prevIndex, page)
                pageIndex = prevIndex
                if (self.currPageIndex >= pageIndex):
                    self.currPageIndex += 1
            else:
                self.pages.append(page)
                pageIndex = len(self.pages) - 1
        else:
            self.pages.append(page)
            pageIndex = len(self.pages) - 1
        
        page.setBook(self)
        page.setPageName(pageName)
        page.reparentTo(self)
        self.addPageTab(page, pageIndex, pageName)
        from toontown.shtiker import MapPage
        if isinstance(page, MapPage.MapPage):
            self.pageBeforeNews = page

    def addPageTab(self, page, pageIndex, pageName = 'Page'):
        tabIndex = len(self.pageTabs)
        def goToPage():
            messenger.send('wakeup')
            base.playSfx(self.pageSound)
            self.setPage(page)
            localAvatar.newsButtonMgr.setGoingToNewsPageFromStickerBook(False)
            localAvatar.newsButtonMgr.showAppropriateButton()

        def goToNewsPage():
            messenger.send('wakeup')
            base.playSfx(self.pageSound)
            localAvatar.newsButtonMgr.setGoingToNewsPageFromStickerBook(True)
            localAvatar.newsButtonMgr.showAppropriateButton()
            self.setPage(page)
            
##        yOffset = 0.07 * (len(self.pages) - 1)
        yOffset = 0.07 * pageIndex
        iconGeom = None
        iconImage = None
        iconScale = 1
        iconColor = Vec4(1)
        buttonPressedCommand = goToPage
        if pageName == TTLocalizer.OptionsPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/switch')
            iconModels.detachNode()
        elif pageName == TTLocalizer.ShardPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/district')
            iconModels.detachNode()
        elif pageName == TTLocalizer.MapPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/teleportIcon')
            iconModels.detachNode()
        elif pageName == TTLocalizer.InventoryPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/inventory_icons")
            iconGeom = iconModels.find('**/inventory_tart')
            iconScale = 7
            iconModels.detachNode()
        elif pageName == TTLocalizer.QuestPageToonTasks:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/stickerbook_gui")
            iconGeom = iconModels.find("**/questCard")
            iconScale = 0.9
            iconModels.detachNode()
        elif pageName == TTLocalizer.TrackPageShortTitle:
            iconGeom = iconModels = loader.loadModel(
                "phase_3.5/models/gui/filmstrip")            
            iconScale = 1.1
            iconColor = Vec4(.7,.7,.7,1)
            iconModels.detachNode()
        elif pageName == TTLocalizer.SuitPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/gui_gear')
            iconModels.detachNode()
        elif pageName == TTLocalizer.FishPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/fish')
            iconModels.detachNode()
        elif pageName == TTLocalizer.GardenPageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/gardenIcon')
            iconModels.detachNode()            
        elif pageName == TTLocalizer.DisguisePageTitle:
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/disguise2')
            iconColor = Vec4(.7,.7,.7,1)
            iconModels.detachNode()
        elif pageName == TTLocalizer.NPCFriendPageTitle:
            iconModels = loader.loadModel(
                'phase_3.5/models/gui/playingCard')
            iconImage = iconModels.find('**/card_back')
            iconGeom = iconModels.find('**/logo')
            iconScale = 0.22
            iconModels.detachNode()
        elif( pageName == TTLocalizer.KartPageTitle ):
            iconModels = loader.loadModel( "phase_3.5/models/gui/sos_textures" )
            iconGeom = iconModels.find( "**/kartIcon" )
            iconModels.detachNode()
        elif( pageName == TTLocalizer.GolfPageTitle ):
            iconModels = loader.loadModel( "phase_6/models/golf/golf_gui" )
            iconGeom = iconModels.find( "**/score_card_icon" )
            iconModels.detachNode()
        elif( pageName == TTLocalizer.EventsPageName ):
            iconModels = loader.loadModel("phase_4/models/parties/partyStickerbook")
            iconGeom = iconModels.find('**/Stickerbook_PartyIcon')
            iconModels.detachNode()
        elif( pageName == TTLocalizer.NewsPageName ):
            iconModels = loader.loadModel(
                "phase_3.5/models/gui/sos_textures")
            iconGeom = iconModels.find('**/switch')
            iconModels.detachNode()
            buttonPressedCommand = goToNewsPage
        # elif( pageName == TTLocalizer.TIPPageTitle ):
            # iconModels = loader.loadModel(
                # 'phase_3.5/models/gui/playingCard')
            # iconImage = iconModels.find('**/card_back')
            # iconGeom = iconModels.find('**/logo')
            # iconScale = 0.22
            # iconModels.detachNode()
        
        # Changing the page name for the tab for the Options Page
        if (pageName == TTLocalizer.OptionsPageTitle):
            pageName = TTLocalizer.OptionsTabTitle
        
        pageTab = DirectButton(
            parent = self.pageTabFrame,
            relief = DGG.RAISED,
            frameSize = (-0.575, 0.575, -0.575, 0.575),
            borderWidth = (0.05,0.05),
            text = ("","",pageName,""),
            text_align = TextNode.ALeft,
            text_pos = (1,-0.2),
            text_scale = TTLocalizer.SBpageTab,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            image = iconImage,
            image_scale = iconScale,
            geom = iconGeom,
            geom_scale = iconScale,
            geom_color = iconColor,
            pos = (0, 0, -yOffset),
            scale = 0.06,
            command = buttonPressedCommand)
##        self.pageTabs.append(pageTab)
        self.pageTabs.insert(pageIndex, pageTab)

        # hide the news page button, so only 1 way to go in and out of news
        if pageName == TTLocalizer.NewsPageName:
            pageTab.hide()

    def setPage(self, page, enterPage = True):
        """setPage(self, ShtikerPage)
        go to a specific page"""
        # Exit the previous page if there was one
        if self.currPageIndex is not None:
            self.pages[self.currPageIndex].exit()
        # Enter this page
        self.currPageIndex = self.pages.index(page)
        self.setPageTabIndex(self.currPageIndex)
        if enterPage:
            self.showPageArrows()
            page.enter()
        from toontown.shtiker import NewsPage
        
        if not isinstance(page, NewsPage.NewsPage):
            self.pageBeforeNews = page

    def setPageBeforeNews(self, enterPage = True):
        self.setPage(self.pageBeforeNews, enterPage)
        
    def setPageTabIndex(self, pageTabIndex):
        if ((self.currPageTabIndex is not None) and
            (pageTabIndex != self.currPageTabIndex)):
            self.pageTabs[self.currPageTabIndex]['relief'] = DGG.RAISED
        self.currPageTabIndex = pageTabIndex
        self.pageTabs[self.currPageTabIndex]['relief'] = DGG.SUNKEN

    def isOnPage(self, page):
        """Return True if the sticker book is on a certain page."""
        result = False
        if self.currPageIndex is not None:
            curPage = self.pages[self.currPageIndex]
            if curPage == page:
                result = True
        return result
        

    def obscureButton(self, obscured):
        """obscureButton(self, int obscured)
        Make the be button be obscured, regardless of show and hide
        1 = obscure, 0 = unobscured
        """
        self.__obscured = obscured
        self.__setButtonVisibility()

    def isObscured(self):
        return self.__obscured
        
    def showButton(self):
        """
        show the ShtikerBook button, but only if it is not obscured
        """
        self.__shown = 1
        self.__setButtonVisibility()
        localAvatar.newsButtonMgr.showAppropriateButton()

    def hideButton(self):
        """
        hide the ShtikerBook button
        """
        self.__shown = 0
        self.__setButtonVisibility()
        localAvatar.newsButtonMgr.request('Hidden')

    def __setButtonVisibility(self):
        if self.__isOpen:
            # The close button must always be visible while the book
            # is open.
            self.bookOpenButton.hide()
            self.bookCloseButton.show()

        elif self.__shown and not self.__obscured:
            # The open button should be visible.
            self.bookOpenButton.show()
            self.bookCloseButton.hide()
            
        else:
            # The open button is either hidden or obscured.
            self.bookOpenButton.hide()
            self.bookCloseButton.hide()

    def shouldBookButtonBeHidden(self):
        """Mimic __setButtonVisibility returning True in the last case."""
        result = False
        if self.__isOpen:
            pass
        elif self.__shown and not self.__obscured:
            pass
        else:
            result = True
        return result            

    def __open(self):
        messenger.send("enterStickerBook")
        if not localAvatar.getGardenStarted():
            for tab in self.pageTabs:
                if tab["text"][2] == TTLocalizer.GardenPageTitle:
                    tab.hide()

    def __close(self):
        base.playSfx(self.closeSound)
        self.doneStatus = {"mode" : "close"}
        messenger.send("exitStickerBook")
        messenger.send(self.doneEvent)

    def closeBook(self):
        self.__close()

    def __pageDone(self):
        page = self.pages[self.currPageIndex]
        pageDoneStatus = page.getDoneStatus()
        if pageDoneStatus:
            if (pageDoneStatus["mode"] == "close"):
                self.__close()
            else:
                self.doneStatus = pageDoneStatus
                messenger.send(self.doneEvent)

    def __pageChange(self, offset):
        messenger.send('wakeup')
        base.playSfx(self.pageSound)
        # Exit the current page
        self.pages[self.currPageIndex].exit()
        self.currPageIndex = (self.currPageIndex + offset)
        messenger.send("stickerBookPageChange-" + str(self.currPageIndex))
        # Clamp the page index
        self.currPageIndex = max(self.currPageIndex, 0)
        self.currPageIndex = min(self.currPageIndex, (len(self.pages) - 1))
        self.setPageTabIndex(self.currPageIndex)
                
        self.showPageArrows()
        
        # Enter the new current page
        page = self.pages[self.currPageIndex]
        page.enter()
        
        from toontown.shtiker import NewsPage
        if not isinstance(page, NewsPage.NewsPage):
            self.pageBeforeNews = page

    def showPageArrows(self):
        # If we are at the end of the list, disable the next button
        if (self.currPageIndex == (len(self.pages) - 1)):
            self.prevArrow.show()
            self.nextArrow.hide()
        else:
            self.prevArrow.show()
            self.nextArrow.show()
        
        self.checkForNewsPage()
        
        # If we are at the beginning of the list, disable the prev button
        if (self.currPageIndex == 0):
            self.prevArrow.hide()
            self.nextArrow.show()

    def checkForNewsPage(self):
        """
        Check if the next and previous page is the News Page. 
        """
        from toontown.shtiker import NewsPage        
        self.ignore("arrow_left")
        self.ignore("arrow_right")
        
        if ((self.currPageIndex + 1) <= (len(self.pages) - 1)) and \
           (isinstance(self.pages[self.currPageIndex + 1], NewsPage.NewsPage)):
            self.prevArrow.show()
            self.nextArrow.hide()
            self.accept("arrow_left", self.__pageChange, [-1])
        else:
            self.prevArrow.show()
            self.nextArrow.show()
            if not (isinstance(self.pages[self.currPageIndex], NewsPage.NewsPage)):
                # Add hooks so the keyboard arrow keys work too
                self.accept("arrow_right", self.__pageChange, [1])
                self.accept("arrow_left", self.__pageChange, [-1])
        
    # these two functions are for the tutorial
    def disableBookCloseButton(self):
        if self.bookCloseButton:
            self.bookCloseButton['command'] = None

    def enableBookCloseButton(self):
        if self.bookCloseButton:
            self.bookCloseButton['command'] = self.__close

    def disableAllPageTabs(self):
        """The news page overlaps the page tab buttons, but they are still clickable."""
        for button in self.pageTabs:
            button['state'] = DGG.DISABLED

    def enableAllPageTabs(self):
        """When closing the news page, renable them."""
        for button in self.pageTabs:
            button['state'] = DGG.NORMAL
