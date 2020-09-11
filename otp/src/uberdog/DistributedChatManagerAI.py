"""
The Chat Manager AI handles all the district chat.
"""

from otp.ai.AIBaseGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory('ChatManagerAI')


class DistributedChatManagerAI(DistributedObjectAI):
    """
    The Chat Manager AI is a global object.

    See Also:
        "otp/src/guild/ChatManager.py"
        "otp/src/guild/ChatManagerUD.py"
        "otp/src/configfiles/otp.dc"
    """
    notify = notify

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectAI.__init__(self, air)
        self.notify.warning("ChatManagerAI going online")

    def delete(self):
        assert self.notify.debugCall()
        self.notify.warning("ChatManagerAI going offline")
        DistributedObjectAI.delete(self)
    
    def online(self):
        assert self.notify.debugCall()
