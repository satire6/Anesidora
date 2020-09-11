from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify.DirectNotifyGlobal import directNotify


class GuildManagerAI(DistributedObjectGlobalAI):
    """
    The Player Friends Manager is a global object.
    This object handles client requests on player-level (as opposed to avatar-level) friends.

    See Also:
        "otp/src/friends/GuildManagerAIUD.py"
        "otp/src/friends/AvatarFriendsManager.py"
        "pirates/src/friends/PiratesFriendsList.py"
        "otp/src/configfiles/otp.dc"
        "pirates/src/configfiles/pirates.dc"
    """
    notify = directNotify.newCategory('GuildManagerAI')

    def __init__(self, cr):
        DistributedObjectGlobalAI.__init__(self, cr)
        self.doNotListenToChannel = True
        
    def avatarOnline(self, avatarId):
        pass

    def avatarOffline(self, avatarId, rep):
        simbase.air.sendUpdateToChannel(self, self.doId, "updateRep", [avatarId, rep])

    def d_sendAvatarBandId(self, avatarId, bandManagerId, bandId):
        simbase.air.sendUpdateToChannel(self, self.doId, "sendAvatarBandId", [avatarId, bandManagerId, bandId])
        
