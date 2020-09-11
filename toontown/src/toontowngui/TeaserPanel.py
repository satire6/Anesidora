from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import TTDialog
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from direct.showbase.DirectObject import DirectObject
from otp.login import LeaveToPayDialog
#from otp.otpbase import OTPLauncherGlobals

"""
d.destroy()
from direct.gui import DirectDialog
buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
guiButton = loader.loadModel("phase_3/models/gui/quit_button")
cancelImageList = (buttons.find('**/CloseBtn_UP'),buttons.find('**/CloseBtn_DN'),buttons.find('**/CloseBtn_Rllvr'))
subscribeImageList = (guiButton.find('**/QuitBtn_DN'),guiButton.find("**/QuitBtn_DN"),guiButton.find("**/QuitBtn_RLVR"),)
buttonImage = [subscribeImageList,cancelImageList]
buttonText = ('Subscribe Now!', 'Cancel')
d = DirectDialog.DirectDialog(buttonImageList=buttonImage,buttonTextList=buttonText)
"""

Pages = {

    # "stringToken" : (localized text,
    #                  image filename,
    #                  image format flag [square = 2, portrait = 1, landscape = 0],
    #                  members only flag,
    #                  )
    
    'otherHoods' : (TTLocalizer.TeaserOtherHoods,),
    'typeAName' : (TTLocalizer.TeaserTypeAName,),
    'sixToons'   : (TTLocalizer.TeaserSixToons,),
    'otherGags'  : (TTLocalizer.TeaserOtherGags,),
    'clothing'   : (TTLocalizer.TeaserClothing,),
    #'furniture'  : (TTLocalizer.TeaserFurniture,),
    'cogHQ'      : (TTLocalizer.TeaserCogHQ,),
    'secretChat' : (TTLocalizer.TeaserSecretChat,),
    #'mailers'    : (TTLocalizer.TeaserCardsAndPosters,),
    #'holidays'   : (TTLocalizer.TeaserHolidays,),
    'quests'     : (TTLocalizer.TeaserQuests,),
    'emotions'   : (TTLocalizer.TeaserEmotions,),
    'minigames'  : (TTLocalizer.TeaserMinigames,),
    'karting'    : (TTLocalizer.TeaserKarting,),
    'kartingAccessories'    : (TTLocalizer.TeaserKartingAccessories,),
    'gardening'    : (TTLocalizer.TeaserGardening,),
    #'bigger'    : (TTLocalizer.TeaserBigger,),
    #'rental'    : (TTLocalizer.TeaserRental,),
    'tricks'    : (TTLocalizer.TeaserTricks,),
    'species'    : (TTLocalizer.TeaserSpecies,),
    'golf'       : (TTLocalizer.TeaserGolf,),
    'fishing'       : (TTLocalizer.TeaserFishing,),
    'parties'       : (TTLocalizer.TeaserParties,),
    }

PageOrder = [
    'sixToons',
    'typeAName',
    'species',
    'otherHoods',
    'otherGags',
    'clothing',
    #'furniture',
    #'bigger',
    #'rental',
    'parties',
    'tricks',
    'cogHQ',
    'secretChat',
    #'mailers',
    #'holidays',
    'quests',
    'emotions',
    'minigames',
    'karting',
    'kartingAccessories',
    'gardening',
    'golf',
    'fishing',
    ]

class TeaserPanel(DirectObject):
    """Tease trialers with descriptions of what they'll get if they subscribe
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TeaserPanel")

    def __init__(self, pageName, doneFunc=None):

        self.doneFunc = doneFunc
 
        # if we don't have a feature browser, make one
        if not hasattr(self, "browser"):
            self.browser = FeatureBrowser()
            self.browser.load()
            self.browser.setPos(0, 0, TTLocalizer.TSRPbrowserPosZ)
            # make room for the top five features
            self.browser.setScale(0.75)
            self.browser.reparentTo(hidden)
        
        self.upsellBackground = loader.loadModel("phase_3/models/gui/tt_m_gui_ups_panelBg")
        
        self.leaveDialog = None
        self.showPage(pageName)
        
        # The player might be able to exit the stop state either through some other
        # panel or if his boarding party leader boards the elevator. 
        # Close any Teaser panel if the toon moves out of the stopped state.
        self.ignore("exitingStoppedState")
        self.accept("exitingStoppedState", self.cleanup)
        

    def __handleDone(self, choice = 0):
        # clean up the teaser panel and take appropriate action
        self.cleanup()
        self.unload()
        
        if choice == 1:
            self.__handlePay()
        else:
            self.__handleContinue()
            
    def __handleContinue(self):
        # call the user done function
        if self.doneFunc:
            self.notify.debug("calling doneFunc")
            self.doneFunc()

    def __handlePay(self):
        if base.cr.isWebPlayToken() or __dev__:
            if self.leaveDialog == None:
                self.notify.debug("making LTP")
                self.leaveDialog = LeaveToPayDialog.LeaveToPayDialog(0, doneFunc=self.doneFunc)
            self.notify.debug("showing LTP")
            self.leaveDialog.show()
        else:
            self.notify.error("You should not have a TeaserPanel without a PlayToken")


    def destroy(self):
        self.cleanup()
        
    # dialog callback code passes a value
    def cleanup(self):
        if hasattr(self, 'browser'):
            self.browser.reparentTo(hidden)
            self.browser.ignoreAll()
        if hasattr(self, 'dialog'):
            base.transitions.noTransitions()
            self.dialog.cleanup()
            del self.dialog
        if self.leaveDialog:
            self.leaveDialog.destroy()
            self.leaveDialog = None
        self.ignoreAll()

    def unload(self):
        # there is a chance the gui code might have already deleted this
        if hasattr(self, 'browser'):
            self.browser.destroy()
            del self.browser
        
    def showPage(self, pageName):
        if not pageName in PageOrder:
            self.notify.error("unknown page '%s'" % pageName)

        # log velvet rope hits
        base.cr.centralLogger.writeClientEvent('velvetRope: %s' % pageName)
        
        # map page name to browser index
        self.browser.scrollTo(PageOrder.index(pageName))

        # remove current global dialog if present
        self.cleanup()

        self.dialog = TTDialog.TTDialog(
            parent = aspect2dp,
            text = TTLocalizer.TeaserTop,
            text_align = TextNode.ACenter,
            text_wordwrap = TTLocalizer.TSRPdialogWordwrap,
            text_scale = TTLocalizer.TSRPtop,
            topPad =-0.15,
            midPad = 1.25,
            sidePad = 0.25,
            pad = (0.25, 0.25),
            command = self.__handleDone,
            fadeScreen = .5,
            style = TTDialog.TwoChoice,
            buttonTextList = [TTLocalizer.TeaserSubscribe,
                              TTLocalizer.TeaserContinue,
                              ],
            button_text_scale = TTLocalizer.TSRPbutton,
            buttonPadSF = 5.5,
            sortOrder = NO_FADE_SORT_INDEX,
            image =  self.upsellBackground,
            )
        self.dialog.setPos(0, 0, 0.75)
        self.browser.reparentTo(self.dialog)
        base.transitions.fadeScreen(.5)
        
        if base.config.GetBool('want-teaser-scroll-keys',0):
            self.accept('arrow_right', self.showNextPage)
            self.accept('arrow_left',  self.showPrevPage)
        self.accept('stoppedAsleep', self.__handleDone)

    def showNextPage(self):
        self.notify.debug("show next")
        self.browser.scrollBy(1)
        
    def showPrevPage(self):
        self.notify.debug("show prev")
        self.browser.scrollBy(-1)

    def showPay(self):
        # show the pay button
        self.dialog.buttonList[0].show()

    def hidePay(self):
        # hide the pay button
        self.dialog.buttonList[0].hide()

    def removed(self):
        # return the removed status of our nodepath object
        if hasattr(self, 'dialog') and self.dialog:
            return self.dialog.removed()
        elif hasattr(self, 'leaveDialog') and self.leaveDialog:
            return self.leaveDialog.removed()
        else:
            return 1


class FeatureBrowser(DirectScrolledList):

    # special methods
    def __init__(self, parent=aspect2dp, **kw):
        """__init__(self)
        FeatureBrowser constructor: create a scrolling list of features
        """
        assert PythonUtil.sameElements(Pages.keys(), PageOrder)

        self.parent = parent
                
        optiondefs = (
            ('parent', self.parent,    None),
            ('relief', None,    None),
            ('numItemsVisible',  1,    None),
            ('items', [],    None),
            )
            
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectScrolledList.__init__(self, parent)
        # We'll scroll using the arrow keys on the keyboard   
        self.incButton.hide()
        self.decButton.hide()
        self.initialiseoptions(FeatureBrowser)

    def destroy(self):
        DirectScrolledList.destroy(self)

    def load(self):
        # load up the images
        # upsellModel = loader.loadModel("phase_3/models/gui/tt_m_gui_ups_mainGui")
        # guiModel = upsellModel.find("**/tt_t_gui_ups_logo_noBubbles")
        guiModel = loader.loadModel("phase_3/models/gui/tt_m_gui_ups_logo_noText")
        
        
        leftLocator = guiModel.find("**/bubbleLeft_locator")
        rightLocator = guiModel.find("**/bubbleRight_locator")
        
        haveFunNode = TextNode("Have Fun")
        haveFunNode.setText(TTLocalizer.TeaserHaveFun)
        haveFunNode.setTextColor(0,0,0,1)
        haveFunNode.setWordwrap(6)
        haveFunNode.setAlign(TextNode.ACenter)
        haveFunNode.setFont(DirectGuiGlobals.getDefaultFont())
        haveFun = NodePath(haveFunNode)
        haveFun.reparentTo(rightLocator)
        haveFun.setScale(TTLocalizer.TSRPhaveFunText)
        
        JoinUsNode = TextNode("Join Us")
        JoinUsNode.setText(TTLocalizer.TeaserJoinUs)
        JoinUsNode.setTextColor(0,0,0,1)
        JoinUsNode.setWordwrap(6)
        JoinUsNode.setAlign(TextNode.ACenter)
        JoinUsNode.setFont(DirectGuiGlobals.getDefaultFont())
        JoinUs = NodePath(JoinUsNode)
        JoinUs.reparentTo(leftLocator)
        JoinUs.setPos(0,0,-0.025)
        JoinUs.setScale(TTLocalizer.TSRPjoinUsText)
        
        # axis = loader.loadModel("models/misc/xyzAxis")
        # axis.reparentTo(guiModel)
        
        # make a panel for each feature
        for page in PageOrder:
            textInfo = Pages.get(page)
            textInfo = textInfo[0] +TTLocalizer.TeaserDefault
                
            panel = DirectFrame(
                parent = self,
                relief = None,
                image = guiModel,
                image_scale = (0.65,0.65,0.65),
                image_pos = (0, 0, 0.0),
                text_align = TextNode.ACenter,
                text = textInfo,
                text_scale = TTLocalizer.TSRPpanelScale,
                text_pos = TTLocalizer.TSRPpanelPos,
                )
            self.addItem(panel)
        guiModel.removeNode()

