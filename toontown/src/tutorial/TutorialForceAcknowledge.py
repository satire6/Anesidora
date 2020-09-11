from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer

class TutorialForceAcknowledge:

    def __init__(self, doneEvent):
        """___init___(self, Event)"""
        self.doneEvent = doneEvent
        self.dialog = None
        return

    def enter(self):
        """enter(phase)
        """
        # Make the toon stop running.
        base.localAvatar.loop("neutral")
        self.doneStatus = {'mode' : 'incomplete'}
        msg = TTLocalizer.TutorialForceAcknowledgeMessage
        self.dialog = TTDialog.TTDialog(text = msg,
                                                    command = self.handleOk,
                                                    style = TTDialog.Acknowledge)
        return

    def exit(self):
        """exit(self)
        """
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        return

    def handleOk(self, value):
        messenger.send(self.doneEvent, [self.doneStatus])
        return
