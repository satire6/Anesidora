from direct.fsm import StateData
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DGG
from direct.gui.DirectGui import DirectLabel
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.shtiker import ShtikerPage
from toontown.toonbase import TTLocalizer

UseDirectNewsFrame = config.GetBool("use-direct-news-frame", True)
HaveNewsFrame = True
if UseDirectNewsFrame:
    # we are using a news page that does not use awesomium or a browser
    from toontown.shtiker import DirectNewsFrame
else:
    try:
        from toontown.shtiker import InGameNewsFrame
    except :
        HaveNewsFrame = False

class NewsPage(ShtikerPage.ShtikerPage):
    """
    NewsPage shows the in game nes.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("NewsPage")
    
    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)


    def load(self):
        self.noNewsLabel = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.NewsPageImportError ,
            text_scale = 0.12,
        )
        
        if HaveNewsFrame:
            if UseDirectNewsFrame:
                import datetime
                start = datetime.datetime.now()
                self.newsFrame = DirectNewsFrame.DirectNewsFrame(parent = self)
                ending = datetime.datetime.now()
                self.notify.info("time to load news = %s" % str(ending-start))
            else:
                self.newsFrame = InGameNewsFrame.InGameNewsFrame(parent = self)
                # this forces a preload of the news web site
                self.newsFrame.activate()

        
    def unload(self):
        if HaveNewsFrame:
            self.newsFrame.unload()
            del self.newsFrame

    def clearPage(self):        
        return

    def updatePage(self):        
        return

    def enter(self):
        """enter(self)
        """
        self.updatePage()
        ShtikerPage.ShtikerPage.enter(self)
        # don't let user click on the buttons under the news page
        if HaveNewsFrame:
            if self.book:
                # hide the previous arrow
                self.book.prevArrow.hide()
                self.book.disableAllPageTabs()        
            self.newsFrame.activate()
            # turn off the cells that obstruct
            base.setCellsAvailable(base.leftCells, 0)
            base.setCellsAvailable([base.rightCells[1]], 0)
            localAvatar.book.bookCloseButton.hide()
            localAvatar.setLastTimeReadNews(base.cr.toontownTimeManager.getCurServerDateTime())
        return

    def exit(self):
        """exit(self)
        """
        self.clearPage()
        if self.book:
            self.book.prevArrow.show()
            self.book.enableAllPageTabs()
        ShtikerPage.ShtikerPage.exit(self)
        if HaveNewsFrame:
            self.newsFrame.deactivate()
            base.setCellsAvailable(base.leftCells, 1)
            base.setCellsAvailable([base.rightCells[1]], 1)            
            if localAvatar.book.shouldBookButtonBeHidden():
                localAvatar.book.bookCloseButton.hide()
            else:
                localAvatar.book.bookCloseButton.show()
        return
              
    def doSnapshot(self):
        """Save our current browser page as png file."""
        if HaveNewsFrame:
            return self.newsFrame.doSnapshot()
        else:
            return "No News Frame"
