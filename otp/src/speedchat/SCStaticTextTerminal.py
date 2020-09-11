"""SCStaticTextTerminal.py: contains the SCStaticTextTerminal class"""

from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText

# args: textId
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)

class SCStaticTextTerminal(SCTerminal):
    """ SCStaticTextTerminal represents a terminal SpeedChat entry that
    contains a piece of static (never-changing/constant) text.

    When selected, generates a 'SCStaticTextMsg' event, with arguments:
    - textId (16-bit; use as index into OTPLocalizer.SpeedChatStaticText)
    """
    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId])
