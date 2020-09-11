"""TTSCIndexedTerminal.py: contains the SCIndexedTerminal class"""

from otp.speedchat.SCTerminal import *
from otp.otpbase.OTPLocalizer import SpeedChatStaticText

# args: taskId, toNpcId, toonProgress, msgIndex
TTSCIndexedMsgEvent = 'SCIndexedMsg'

def decodeTTSCIndexedMsg(msgIndex):
    
    return SpeedChatStaticText.get(msgIndex, None)

class TTSCIndexedTerminal(SCTerminal):
    """ TTSCINdexedTerminal is useful if you want to display a phrase in an SCMenu but have 
          the toon speak a different phrase once it has been selected. 
          
          msg is the text that is displayed in the menu
          msgIndex is the index of the message in OTPLocalizer.SpeedChatStaticText that the toon
          will blather"""
          
    def __init__(self, msg, msgIndex):
        SCTerminal.__init__(self)
        self.text = msg
        self.msgIndex = msgIndex

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCIndexedMsgEvent),
                       [self.msgIndex])
