"""TTSCSingingTerminal.py: contains the TTSCSingingTerminal class."""

from otp.speedchat.SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText

# args: textId
TTSCSingingMsgEvent = 'SCSingingMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)

class TTSCSingingTerminal(SCTerminal):
    """ TTSCSingingTerminal represents a terminal SpeedChat entry that
    contains a note from the singing system.

    When selected, generates a 'TTSCSingingMsgEvent' event, with arguments:
    - textId (16-bit; use as index into OTPLocalizer.SpeedChatStaticText)
    
    This event in turn makes the avatar sing a selected note depending on the
    toon species and torso size.
    """
    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCSingingMsgEvent), [self.textId])

    def finalize(self):
        """
        Making sure that these buttons don't have any rollover or click sound,
        since affects the music making skills. :)
        """
        args = {
            'rolloverSound': None,
            'clickSound': None,}    
        SCTerminal.finalize(self, args)