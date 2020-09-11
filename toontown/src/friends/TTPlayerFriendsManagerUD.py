from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.otpbase import OTPGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD

from otp.otpbase import OTPLocalizerEnglish as localizer

if __debug__:
    notify = directNotify.newCategory('PlayerFriendsManagerUD')

       
#--------------------------------------------------



class TTPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    """
    The Player Friends Manager is a global object.
    This object handles client requests on player-level (as opposed to avatar-level) friends.

    See Also:
        "otp/src/friends/AvatarFriendsManager.py"
        "otp/src/friends/PlayerFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    if __debug__:
        notify = notify

    def __init__(self, air):
        assert self.notify.debugCall()
        wedgeName = uber.config.GetString("sb-dev-name","toontown")
        PlayerFriendsManagerUD.__init__(self,air,1452,wedgeName,"Toontown")

    def _whisperAllowed(self, fromPlayer, toPlayer):
        fromFriends = self.accountId2Friends.get(fromPlayer)

        if fromFriends:
            if [toPlayer,True] in fromFriends:
                return True
            else:
                return False
        else:
            return False
