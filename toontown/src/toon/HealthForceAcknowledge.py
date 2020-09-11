from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer

class HealthForceAcknowledge:
    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        
    def enter(self, hpLevel):
        doneStatus = {}
        toonHp = base.localAvatar.getHp()
        if (toonHp >= hpLevel):
            doneStatus['mode'] = 'complete'
            messenger.send(self.doneEvent, [doneStatus])
        else:
            # Make the Toon stand still while the panel is up
            base.localAvatar.b_setAnimState('neutral', 1)
            doneStatus['mode'] = 'incomplete'
            self.doneStatus = doneStatus
            msg = TTLocalizer.HealthForceAcknowledgeMessage
            self.dialog = TTDialog.TTDialog(
                text = msg,
                command = self.handleOk,
                style = TTDialog.Acknowledge)

    def exit(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None

    def handleOk(self, value):
        messenger.send(self.doneEvent, [self.doneStatus])
