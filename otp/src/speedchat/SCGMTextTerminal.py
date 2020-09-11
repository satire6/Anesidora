"""SCGMTextTerminal.py: contains the SCGMTextTerminal class"""

from SCTerminal import SCTerminal
from otp.speedchat import SpeedChatGMHandler

# args: textId
SCGMTextMsgEvent = 'SCGMTextMsg'

class SCGMTextTerminal(SCTerminal):
    """ SCGMTextTerminal represents a terminal SpeedChat entry that
    contains a piece of static (never-changing/constant) text sent
    from the GM.

    When selected, generates a 'SCGMTextMsg' event, with arguments:
    - textId (32-bit; use as index)
    """
    def __init__(self, textId):
        SCTerminal.__init__(self)
        gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
        self.textId = textId
        self.text = gmHandler.getPhrase(textId)

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCGMTextMsgEvent), [self.textId])
