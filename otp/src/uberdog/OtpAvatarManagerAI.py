"""
The Avatar Manager AI handles all the avatar (avatar groups) accross all districts.
"""

#from cPickle import loads, dumps

#from otp.ai.AIBaseGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory('AvatarManagerAI')

class OtpAvatarManagerAI(DistributedObjectAI):
    """
    The Avatar Manager AI is a global object.

    The Avatar Manager has a collection of Avatar objects.

    See Also:
        "otp/src/guild/AvatarManager.py"
        "otp/src/guild/AvatarManagerUD.py"
        "otp/src/configfiles/otp.dc"
    """
    notify = notify

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectAI.__init__(self, air)
        self.notify.warning("AvatarManagerAI going online")

    def delete(self):
        assert self.notify.debugCall()
        self.notify.warning("AvatarManagerAI going offline")
        DistributedObjectAI.delete(self)
    
    def online(self):
        assert self.notify.debugCall()
