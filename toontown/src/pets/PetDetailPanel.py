from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.pets import PetTricks
from otp.otpbase import OTPLocalizer
from direct.showbase.PythonUtil import lerp

FUDGE_FACTOR = 0.01

class PetDetailPanel(DirectFrame):
    """
    This is a panel that pops up in response to clicking the "Details"
    button on the Pet Panel.  It displays more details about the
    particular pet (namely trick aptitudes).
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("PetDetailPanel")

    def __init__(self, pet, closeCallback, parent = aspect2d, **kw):
        # Inherits from DirectFrame
        # Must specify petId and avName on creation models
        buttons = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        detailPanel = gui.find('**/PetBattlePannel2')

        # Specify default options
        optiondefs = (
            ('pos',           (-4.52, 0.0, 3.05),  None),
            ('scale',         3.58,               None),
            ('relief',        None,               None),
            ('image',         detailPanel,        None),
            ('image_color',   GlobalDialogColor,  None),
            ('text',          TTLocalizer.PetDetailPanelTitle,   None),
            ('text_wordwrap', 10.4,               None),
            ('text_scale',    0.132,              None),
            ('text_pos',      (-0.2, 0.6125),     None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # initialize our base class.
        DirectFrame.__init__(self, parent)

        # Information about avatar
        self.dataText = DirectLabel(self,
                                    text = '',
                                    text_scale = 0.09,
                                    text_align = TextNode.ALeft,
                                    text_wordwrap = 15,
                                    relief = None,
                                    pos = (-0.7, 0.0, 0.55),
                                    )

        # Create some buttons.
        self.bCancel = DirectButton(
            self,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            relief = None,
            text = TTLocalizer.AvatarDetailPanelCancel,
            text_scale = 0.05,
            text_pos = (0.12, -0.01),
            pos = (-0.88, 0.0, -0.68),
            scale = 2.0,
            command = closeCallback)
        #self.bCancel.hide()

        # Call option initialization functions
        self.initialiseoptions(PetDetailPanel)

        # Labels contain the trick name
        self.labels = {}
        # Bars indicate training progress and amount of laff points healed
        self.bars = {}
        
        # Update trick info gui
        self.update(pet)

        # Clean up
        buttons.removeNode()
        gui.removeNode()

    def cleanup(self):
        """cleanup(self):

        Cancels any pending request and removes the panel from the
        screen.
        
        """
        del self.labels
        del self.bars
        self.destroy()

    def update(self, pet):
        if not pet:
            return
        for trickId in PetTricks.TrickId2scIds.keys():
            trickText = TTLocalizer.PetTrickStrings[trickId]
            if trickId < len(pet.trickAptitudes):
                aptitude = pet.trickAptitudes[trickId]
                bar = self.bars.get(trickId)
                label = self.bars.get(trickId)
                # only show the bar if there is some skill
                if aptitude != 0:
                    # display amount of aptitude gained toward next laff
                    healRange = PetTricks.TrickHeals[trickId]
                    hp = lerp(healRange[0], healRange[1], aptitude)
                    if hp == healRange[1]:
                        # maxed
                        hp = healRange[1]
                        length = 1
                        barColor = (0.7,0.8,0.5,1)
                    else:
                        # still working on it
                        hp, length = divmod(hp, 1)
                        barColor = (0.9,1,0.7,1)
                    if not label:
                        # no labels yet, make them
                        self.labels[trickId] = DirectLabel(
                            parent = self,
                            relief = None,
                            pos = (0, 0, 0.43 - (trickId * 0.155)),
                            scale = 0.7,
                            text = trickText,
                            text_scale = TTLocalizer.PDPtrickText,
                            text_fg = (0.05,0.14,0.4,1),
                            text_align = TextNode.ALeft,
                            text_pos = (-1.4,-0.05),
                            )
                    else:
                        # labels made, just update
                        label['text'] = trickText
                    if not bar:
                        # no bars yet, make them
                        self.bars[trickId] = DirectWaitBar(
                            parent = self,
                            pos = (0, 0, 0.43 - (trickId * 0.155)),
                            relief = DGG.SUNKEN,
                            frameSize = (-0.5,0.9,-0.1,0.1),
                            borderWidth = (0.025,0.025),
                            scale = 0.7,
                            frameColor = (0.4,0.6,0.4,1),
                            barColor = barColor,
                            # A small number was added to these to prevent small
                            # values from not being rendered at odd resolutions.
                            range = 1. + FUDGE_FACTOR,
                            value = length + FUDGE_FACTOR,
                            text = str(int(hp)) + " " + TTLocalizer.Laff,
                            text_scale = TTLocalizer.PDPlaff,
                            text_fg = (0.05,0.14,0.4,1),
                            text_align = TextNode.ALeft,
                            text_pos = TTLocalizer.PDPlaffPos,
                            )
                    else:
                        # bars made, just update
                        bar['value'] = length + FUDGE_FACTOR
                        bar['text'] = str(int(hp)) + " " + TTLocalizer.Laff, 
