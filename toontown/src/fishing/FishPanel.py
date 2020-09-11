"""FishPanel module: comtains the FishPanel class"""

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *
import FishGlobals
import FishPhoto

class FishPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory("FishPanel")

    # special methods
    def __init__(self, fish=None, parent=aspect2d, doneEvent=None, **kw):
        """
        Create a DirectFrame for displaying the fish and it's info.
        """
        assert self.notify.debugStateCall(self)
        optiondefs = (
            ('relief',                                    None, None),
            ('state',                                 DGG.DISABLED, None),
            ('image',                   DGG.getDefaultDialogGeom(), None),
            ('image_color',  ToontownGlobals.GlobalDialogColor, None),
            ('image_scale',                    (0.65, 1, 0.85), None),
            ('text',                                        "", None),
            ('text_scale',                                0.06, None),
            ('text_fg',                           (0, 0, 0, 1), None),
            ('text_pos',                          (0, 0.35, 0), None),
            ('text_font',   ToontownGlobals.getInterfaceFont(), None),
            ('text_wordwrap',                             13.5, None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(FishPanel)
        self.doneEvent = doneEvent
        self.fish = fish
        self.parent = parent
        self.photo = None
        
    def destroy(self):
        assert self.notify.debugStateCall(self)
        if self.photo:
            self.photo.destroy()
            self.photo = None
        self.fish = None
        DirectFrame.destroy(self)
        self.parent = None

    def load(self):
        assert self.notify.debugStateCall(self)
        # fish detail panel
        self.weight =  DirectLabel(
            parent = self,
            pos = (0, 0, -0.28),
            relief = None,
            state = DGG.NORMAL,
            text = "",
            text_scale = 0.05,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0., 0),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_wordwrap = 10.5
            )
        self.value =  DirectLabel(
            parent = self,
            pos = (0, 0, -0.35),
            relief = None,
            state = DGG.NORMAL,
            text = "",
            text_scale = 0.05,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0, 0),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_wordwrap = 10.5
            )
        self.mystery = DirectLabel(
            parent = self,
            pos = (-0.025, 0, -0.055),
            relief = None,
            state = DGG.NORMAL,
            text = "?",
            text_scale = 0.25,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0, 0),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_wordwrap = 10.5
            )

        self.extraLabel = DirectLabel(
            parent = self,
            relief = None,
            state = DGG.NORMAL,
            text = "",
            text_fg = (0.2, 0.8, 0.4, 1),
            text_font = ToontownGlobals.getSignFont(),
            text_scale = 0.08,
            pos = (0,0,0.26),
            )

        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        # fish detail close button
        self.cancel = DirectButton(
            parent = self,
            pos = (0.275, 0, -0.375),
            relief = None,
            state = DGG.NORMAL,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            image_scale = (0.6, 1, 0.6),
            command = self.handleCancel,            
            )
        buttons.removeNode()
        self.photo = FishPhoto.FishPhoto(parent=self)
        # make the scroll list
        self.update(self.fish)
        
    def update(self, fish):
        assert self.notify.debugStateCall(self)
        self.fish = fish
        if self.fish == None:
            return
        # pop up a little doober
        self['text'] = self.fish.getSpeciesName()
        weight = self.fish.getWeight()
        conv = TTLocalizer.FishPageWeightConversion
        large = weight / conv
        if large == 1:
            largeStr = TTLocalizer.FishPageWeightLargeS % large
        else:
            largeStr = TTLocalizer.FishPageWeightLargeP % large
        small = weight % conv
        if small == 1:
            smallStr = TTLocalizer.FishPageWeightSmallS % small
        else:
            smallStr = TTLocalizer.FishPageWeightSmallP % small
        self.weight['text'] = TTLocalizer.FishPageWeightStr + largeStr + smallStr
        value = self.fish.getValue()
        if value == 1:
            self.value['text'] = (TTLocalizer.FishPageValueS % value)
        else:
            self.value['text'] = (TTLocalizer.FishPageValueP  % value)
        self.photo.update(fish)

    def setSwimBounds(self, *bounds):
        """
        bounds are floats: left, right, top, bottom
        """
        assert len(bounds) == 4
        self.swimBounds=bounds
        
    def setSwimColor(self, *colors):
        """
        colors are floats: red, green, blue, alpha
        """
        assert len(colors) == 4
        self.swimColor=colors
        
    def handleCancel(self):
        assert self.notify.debugStateCall(self)
        self.hide()
        if self.doneEvent:
            messenger.send(self.doneEvent)

    def show(self, code=FishGlobals.FishItem):
        assert self.notify.debugStateCall(self)
        # if we are browsing fish we must be awake
        messenger.send('wakeup')
        apply(self.photo.setSwimBounds, self.swimBounds)
        apply(self.photo.setSwimColor, self.swimColor)

        if code == FishGlobals.FishItem:
            self.extraLabel.hide()
        elif code == FishGlobals.FishItemNewEntry:
            self.extraLabel.show()
            self.extraLabel['text'] = TTLocalizer.FishingNewEntry
            self.extraLabel['text_scale'] = TTLocalizer.FPnewEntry
            self.extraLabel.setPos(0,0,0.26)
        elif code == FishGlobals.FishItemNewRecord:
            self.extraLabel.show()
            self.extraLabel['text'] = TTLocalizer.FishingNewRecord
            self.extraLabel['text_scale'] = TTLocalizer.FPnewRecord

        self.photo.show()
        DirectFrame.show(self)

    def hide(self):
        assert self.notify.debugStateCall(self)
        self.photo.hide()
        DirectFrame.hide(self)
