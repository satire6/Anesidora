"""LocalChar module: contains the LocalChar class"""

import DistributedChar
from otp.avatar import LocalAvatar
from otp.chat import ChatManager
import Char

class LocalChar(DistributedChar.DistributedChar, LocalAvatar.LocalAvatar):
    """LocalChar class:"""

    def __init__(self, cr):
        """
        Local char constructor
        """
        try:
            self.LocalChar_initialized
        except:
            self.LocalChar_initialized = 1
            DistributedChar.DistributedChar.__init__(self, cr)
            LocalAvatar.LocalAvatar.__init__(self, cr)
            # Is this redundant with LocalAvatar: ---> self.chatMgr = ChatManager.ChatManager()
            self.setNameVisible(0)

            # Init the avatar sounds
            Char.initializeDialogue()


