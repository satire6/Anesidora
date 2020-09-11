from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from direct.showbase import Transitions
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import LaffMeter

class DeathForceAcknowledge:
    def __init__(self, doneEvent):
        """___init___(self, Event)"""

        # We create a DirectFrame for the fade polygon, instead of
        # simply loading the polygon model and using it directly,
        # so that it will also obscure mouse events for objects
        # positioned behind it.
        # Normally, this is done as a transition fade screen, but
        # it doesn't work here (noTransitions gets called after
        # the dialog is brought up)
        fadeModel = loader.loadModel("phase_3/models/misc/fade")
        if fadeModel:
            self.fade = DirectFrame(
                parent = aspect2dp,
                relief = None,
                image = fadeModel,
                image_color = (0, 0, 0, 0.4),
                image_scale = 3.0,
                state = DGG.NORMAL,
                )
            self.fade.reparentTo(aspect2d, FADE_SORT_INDEX)
            fadeModel.removeNode()
        else:
            print "Problem loading fadeModel."
            self.fade = None

        self.dialog = TTDialog.TTGlobalDialog(
            message = TTLocalizer.PlaygroundDeathAckMessage,
            doneEvent = doneEvent,
            style = TTDialog.Acknowledge,
            suppressKeys = True,
            )
        self.dialog['text_pos'] = (-.26,.1)
        scale = self.dialog.component('image0').getScale()
        scale.setX(scale[0] * 1.3)
        self.dialog.component('image0').setScale(scale)


        av = base.localAvatar
        self.laffMeter = LaffMeter.LaffMeter(av.style, av.hp, av.maxHp)
        self.laffMeter.reparentTo(self.dialog)
        if av.style.getAnimal() == "monkey":
            self.laffMeter.setPos(-0.46, 0, -0.035)
            self.laffMeter.setScale(0.085)
        else:
            self.laffMeter.setPos(-0.48, 0, -0.035)
            self.laffMeter.setScale(0.1)
        self.laffMeter.start()

        self.dialog.show()

    def cleanup(self):
        if self.fade:
            self.fade.destroy()
        if self.laffMeter:
            self.laffMeter.destroy()
            del self.laffMeter
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
