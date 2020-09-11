from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
import string
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer

# No buttons at all
NoButtons = 0
# just an OK button
Acknowledge = 1
# Just a CANCEL button
CancelOnly = 2
# OK and CANCEL buttons
TwoChoice = 3
# Yes and No buttons
YesNo = 4
# custom 2 buttons
TwoChoiceCustom = 5

class OTPDialog(DirectDialog):
    def __init__(self, parent = None, style = NoButtons,**kw):

        if (parent == None):
            parent = aspect2d

        self.style = style

        # Load gui elements if necessary
        buttons = None
        if (self.style != NoButtons):
            assert self.path
            buttons = loader.loadModel(self.path)

        # Init buttons
        if self.style == TwoChoiceCustom:
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                           buttons.find('**/ChtBx_OKBtn_DN'),
                           buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'),
                               buttons.find('**/CloseBtn_DN'),
                               buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]         
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
            if 'buttonText' in kw:
                buttonText =  kw['buttonText']
                del kw['buttonText']
            else:
                buttonText = [OTPLocalizer.DialogOK, OTPLocalizer.DialogCancel]
                
            
        elif (self.style == TwoChoice):
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                           buttons.find('**/ChtBx_OKBtn_DN'),
                           buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'),
                               buttons.find('**/CloseBtn_DN'),
                               buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]
            buttonText = [OTPLocalizer.DialogOK,
                          OTPLocalizer.DialogCancel]
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
        elif (self.style == YesNo):
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                           buttons.find('**/ChtBx_OKBtn_DN'),
                           buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'),
                               buttons.find('**/CloseBtn_DN'),
                               buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]
            buttonText = [OTPLocalizer.DialogYes,
                          OTPLocalizer.DialogNo]
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
        elif (self.style == Acknowledge):
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                           buttons.find('**/ChtBx_OKBtn_DN'),
                           buttons.find('**/ChtBx_OKBtn_Rllvr'))
            buttonImage = [okImageList]
            buttonText = [OTPLocalizer.DialogOK]
            buttonValue = [DGG.DIALOG_OK]
        elif (self.style == CancelOnly):
            cancelImageList = (buttons.find('**/CloseBtn_UP'),
                               buttons.find('**/CloseBtn_DN'),
                               buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [cancelImageList]
            buttonText = [OTPLocalizer.DialogCancel]
            buttonValue = [DGG.DIALOG_CANCEL]
        elif (self.style == NoButtons):
            buttonImage = []
            buttonText = []
            buttonValue = []
        else:
            "Sanity check"
            self.notify.error("No such style as: " + str(self.style))
        
        optiondefs = (
            # Define type of DirectGuiWidget
            ('buttonImageList', buttonImage,          DGG.INITOPT),
            ('buttonTextList',  buttonText,           DGG.INITOPT),
            ('buttonValueList', buttonValue,          DGG.INITOPT),
            ('buttonPadSF',     2.2,                  DGG.INITOPT),
            ('text_font',       DGG.getDefaultFont(), None),
            ('text_wordwrap',   12,                   None),
            ('text_scale',      0.07,                 None),
            ('buttonSize',      (-.05,.05,-.05,.05),  None),
            ('button_pad',      (0,0),                None),
            ('button_relief',   None,                 None),
            ('button_text_pos', (0,-0.1),             None),
            ('fadeScreen',      0.5,                  None),
            ('image_color',     OTPGlobals.GlobalDialogColor,     None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(OTPDialog)

        if buttons != None:
            buttons.removeNode()

class GlobalDialog(OTPDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory("GlobalDialog")
    def __init__(self, message = '', doneEvent = None, style = NoButtons,
                 okButtonText = OTPLocalizer.DialogOK,
                 cancelButtonText = OTPLocalizer.DialogCancel,
                 **kw):
        """
        ___init___(self, doneEvent, style, okButtonText, cancelButtonText, kw)
        """

        # Without this, OTPDialog throws an error.  Longterm solution
        # is to create an OTPModels with the shared model files.
        if not hasattr(self, 'path'):
            # load out of TTMODELS
            self.path = 'phase_3/models/gui/dialog_box_buttons_gui'
          
        # Sanity check
        if (doneEvent == None) and (style != NoButtons):
            self.notify.error("Boxes with buttons must specify a doneEvent.")
            
        self.__doneEvent = doneEvent
        
        if style == NoButtons:
            buttonText = []
        elif style == Acknowledge:
            buttonText = [okButtonText]
        elif style == CancelOnly:
            buttonText = [cancelButtonText]
        else:
            buttonText = [okButtonText, cancelButtonText]

        optiondefs = (
            # Define type of DirectGuiWidget
            ('dialogName',      'globalDialog',     DGG.INITOPT),
            ('buttonTextList',  buttonText,         DGG.INITOPT),
            ('text',            message,            None),
            ('command',         self.handleButton,  None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        OTPDialog.__init__(self, style = style)
        self.initialiseoptions(GlobalDialog)

    def handleButton(self, value):
        assert self.style != NoButtons
        if value == DGG.DIALOG_OK:
            self.doneStatus = "ok"
            messenger.send(self.__doneEvent)
        elif value == DGG.DIALOG_CANCEL:
            self.doneStatus = "cancel"
            messenger.send(self.__doneEvent)

