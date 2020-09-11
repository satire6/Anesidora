from pandac.PandaModules import *
from direct.gui.DirectGui import *
from otp.otpbase import OTPLocalizer

class MultiPageTextFrame(DirectFrame):
    defWidth = 1.8
    defHeight = .9
    def __init__(self, textList,
                 width = defWidth, height = defHeight,
                 wordWrap = None, hidePageNum = 0,
                 pageChangeCallback = None,
                 parent = aspect2d, **kw):
        # text must be a list of strings, one string per page
        self.textList = textList
        self.numPages = len(self.textList)
        self.pageChangeCallback = pageChangeCallback

        if not wordWrap:
            # attempt to guess a reasonable default
            wordWrap = round(18.8 * width)

        # half-width, half-height
        hWidth = width/2.
        hHeight = height/2.
        
        optiondefs = (
            ('relief',        DGG.SUNKEN,                             None),
            ('frameSize',     (-hWidth,hWidth, -hHeight,hHeight), None),
            ('frameColor',    (0.85,0.85,0.6,1),                  None),
            ('borderWidth',   (0.01, 0.01),                       None),
            ('text',          '',                                 None),
            ('text_pos',      (-hWidth*.95,hHeight*.93),          None),
            ('text_scale',    .05,                                None),
            ('text_align',    TextNode.ALeft,                     None),
            ('text_wordwrap', wordWrap,                           None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(MultiPageTextFrame)        

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")

        # scale the buttons according to the frame height
        buttonScale = .7 * (float(height) / self.defHeight)
        buttonZ = -hHeight * .83
        self.nextButton = DirectButton(
            parent = self,
            relief = None,
            scale = buttonScale,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (0.75,1,1),
            pos = (hWidth*.35,0,buttonZ),
            text = OTPLocalizer.MultiPageTextFrameNext,
            text_scale = 0.05,
            text_pos = (0,-0.02),
            command = self.turnPage,
            extraArgs = [1],
            )
        self.prevButton = DirectButton(
            parent = self,
            relief = None,
            scale = buttonScale,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (0.75,1,1),
            pos = (-hWidth*.35,0,buttonZ),
            text = OTPLocalizer.MultiPageTextFramePrev,
            text_scale = 0.05,
            text_pos = (0,-0.02),
            command = self.turnPage,
            extraArgs = [-1],
            )
        self.pageNum = DirectLabel(
            relief = None,
            parent = self,
            pos = (0,0,-hHeight*.86),
            text = '',
            text_scale = 0.05,
            text_pos = (0,0),
            )
        if hidePageNum:
            self.pageNum.hide()

        # Show the first page
        self.setPage(0)

        guiButton.removeNode()

    def setPageChangeCallback(self, callback):
        self.pageChangeCallback = callback
        # call the callback
        self.setPage(self.curPage)

    def setPage(self, pageNum):
        # Figure out the right state for page buttons
        self.curPage = max(0, min(self.numPages-1, pageNum))
        if (self.numPages == 1):
            self.nextButton.hide()
            self.prevButton.hide()
            self.curPage = 0
        elif (self.curPage == (self.numPages - 1)):
            self.nextButton.hide()
            self.prevButton.show()
        elif (self.curPage == 0):
            self.nextButton.show()
            self.prevButton.hide()
        else:
            self.nextButton.show()
            self.prevButton.show()
        # Now display the text
        self.pageNum['text'] = (OTPLocalizer.MultiPageTextFramePage % \
                                (self.curPage+1, self.numPages))
        self['text'] = self.textList[self.curPage]

        if self.pageChangeCallback:
            self.pageChangeCallback(self.getCurPage())

    def getCurPage(self):
        return self.curPage

    def turnPage(self, delta):
        self.setPage(self.curPage + delta)

    def acceptAgreementKeypresses(self):
        self.accept('page_down-up', self.turnPage, extraArgs=[1])
        self.accept('page_up-up', self.turnPage, extraArgs=[-1])
    def ignoreAgreementKeypresses(self):
        self.ignore('page_down-up')
        self.ignore('page_up-up')
