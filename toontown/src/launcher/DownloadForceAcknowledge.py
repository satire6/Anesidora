from pandac.PandaModules import *
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
import random

class DownloadForceAcknowledge:

    def __init__(self, doneEvent):
        """___init___(self, Event)"""
        self.doneEvent = doneEvent
        self.dialog = None

    def enter(self, phase):
        """enter(phase)
        """
        doneStatus = {}
        if launcher.getPhaseComplete(phase):
            doneStatus['mode'] = 'complete'
            messenger.send(self.doneEvent, [doneStatus])
        else:
            # Make the Toon stand still while the panel is up
            # Careful! You may not have a localToon yet
            try:
                base.localAvatar.b_setAnimState('neutral', 1)
            except:
                pass
            doneStatus['mode'] = 'incomplete'
            self.doneStatus = doneStatus
            percentComplete = base.launcher.getPercentPhaseComplete(phase)
            phaseName = TTLocalizer.LauncherPhaseNames[phase]
            verb = random.choice(TTLocalizer.DownloadForceAcknowledgeVerbList)
            msg = (TTLocalizer.DownloadForceAcknowledgeMsg %
                   {"phase":  phaseName,
                    "verb": verb,})
            self.dialog = TTDialog.TTDialog(text = msg,
                                            command = self.handleOk,
                                            style = TTDialog.Acknowledge)
            # the screen fade won't happen unless we call show()
            self.dialog.show()

    def exit(self):
        """exit(self)
        """
        if self.dialog:
            self.dialog.hide()
            self.dialog.cleanup()
            self.dialog = None

    def handleOk(self, value):
        messenger.send(self.doneEvent, [self.doneStatus])
