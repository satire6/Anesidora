"""SCStaticTextTerminal.py: contains the SCStaticTextTerminal class"""

from otp.speedchat.SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText

# args: textId
SCStaticTextMsgEvent = 'SCStaticTextMsg'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)

class TTSCWhiteListTerminal(SCTerminal):
    """ SCStaticTextTerminal represents a terminal SpeedChat entry that
    contains a piece of static (never-changing/constant) text.

    When selected, generates a 'SCStaticTextMsg' event, with arguments:
    - textId (16-bit; use as index into OTPLocalizer.SpeedChatStaticText)
    """
    def __init__(self, textId, parentMenu = None):
        SCTerminal.__init__(self)
        self.parentClass = parentMenu
        
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

        print ("SpeedText %s %s" % (self.textId, self.text))

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        #messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId])
        #print ("Message Sent %s %s" % (self.getEventName(SCStaticTextMsgEvent), [self.textId]))
        #base.whiteList.activate()
        if not self.parentClass.whisperAvatarId:
            base.localAvatar.chatMgr.fsm.request("whiteListOpenChat")
        elif self.parentClass.toPlayer:
            base.localAvatar.chatMgr.fsm.request("whiteListPlayerChat", [self.parentClass.whisperAvatarId])
        else:
            base.localAvatar.chatMgr.fsm.request("whiteListAvatarChat", [self.parentClass.whisperAvatarId])
        
        
