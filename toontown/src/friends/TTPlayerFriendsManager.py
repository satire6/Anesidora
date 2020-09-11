from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.friends.PlayerFriendsManager import PlayerFriendsManager

if __debug__:
    notify = directNotify.newCategory('TTPlayerFriendsManager')

class TTPlayerFriendsManager(PlayerFriendsManager):
    """
    The Player Friends Manager is a global object.
    This object handles client requests on player-level (as opposed to avatar-level) friends.

    See Also:
        "otp/src/friends/PlayerFriendsManagerUD.py"
        "otp/src/friends/AvatarFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    if __debug__:
        notify = notify

    def __init__(self, cr):
        assert self.notify.debugCall()
        PlayerFriendsManager.__init__(self,cr)

    def sendRequestInvite(self,playerId):
        assert self.notify.debugCall()
        self.sendUpdate("requestInvite", [0,playerId,False])
