"""TTSCResistanceTerminal.py: contains the TTSCResistanceTerminal class"""

from otp.speedchat.SCTerminal import SCTerminal
from toontown.chat import ResistanceChat

# args: textId
TTSCResistanceMsgEvent = 'TTSCResistanceMsg'

def decodeTTSCResistanceMsg(textId):
    return ResistanceChat.getChatText(textId)

class TTSCResistanceTerminal(SCTerminal):
    """ TTSCResistanceTerminal represents a terminal SpeedChat entry that
    contains a phrase that was purchased from the catalog. """
    def __init__(self, textId, charges):
        SCTerminal.__init__(self)
        self.setCharges(charges)
        self.textId = textId
        self.text = ResistanceChat.getItemText(self.textId)

    def isWhisperable(self):
        # this terminal is used to trigger area-of-effect abilities
        # don't allow whisper
        return False

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCResistanceMsgEvent),
                       [self.textId])
