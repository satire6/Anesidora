"""
TTSCCogMenu.py: contains the TTSCCogMenu class

For standalone testing these are useful:
base.localAvatar.chatMgr.chatInputSpeedChat.addCogMenu()
base.localAvatar.chatMgr.chatInputSpeedChat.removeCogMenu()
base.localAvatar.chatMgr.chatInputSpeedChat.speedChat[2].getMenu()

"""

from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal

class TTSCCogMenu(SCMenu):
    """
    TTSCCogMenu represents a menu of SCCogTerminals.
    """
    
    def __init__(self, indices):
        SCMenu.__init__(self)

        for index in indices:
            term = SCStaticTextTerminal(index)
            self.append(term)

    def destroy(self):
        SCMenu.destroy(self)

