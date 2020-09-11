"""SCCustomTerminal.py: contains the SCCustomTerminal class"""

from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings

# args: textId
SCCustomMsgEvent = 'SCCustomMsg'

def decodeSCCustomMsg(textId):
    return CustomSCStrings.get(textId, None)

class SCCustomTerminal(SCTerminal):
    """ SCCustomTerminal represents a terminal SpeedChat entry that
    contains a phrase that was purchased from the catalog. """
    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = CustomSCStrings[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCCustomMsgEvent),
                       [self.textId])
