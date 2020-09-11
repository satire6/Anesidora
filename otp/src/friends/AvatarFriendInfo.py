from otp.avatar.AvatarHandle import AvatarHandle


class AvatarFriendInfo(AvatarHandle):
    def __init__(self,
                 avatarName = "",
                 playerName = "",
                 playerId = 0,
                 onlineYesNo = 0,
                 openChatEnabledYesNo = 0,
                 openChatFriendshipYesNo = 0,
                 wlChatEnabledYesNo = 0):
        self.avatarName = avatarName
        self.playerName = playerName
        self.playerId = playerId
        self.onlineYesNo = onlineYesNo
        self.openChatEnabledYesNo = openChatEnabledYesNo
        self.openChatFriendshipYesNo = openChatFriendshipYesNo
        self.wlChatEnabledYesNo = wlChatEnabledYesNo

        # just in case we dont get a NoAttribute error
        # all values we're getting at this point is zero
        self.understandableYesNo = self.isUnderstandable() 

    def calcUnderstandableYesNo(self):
        # ideally other classes should call isUnderstandable()
        # but since they're accessing understandableYesNo
        # let's just initially set it to the result of isUnderstandable()
        self.understandableYesNo = self.isUnderstandable()

    def getName(self):
        """
        AvatarHandle interface
        """
        if self.avatarName:
            return self.avatarName
        elif self.playerName:
            return self.playerName
        else:
            return ""

    def isUnderstandable(self):
        """
        AvatarHandle interface
        """
        result = False
        try:
            if self.openChatFriendshipYesNo:
                # ok they are true friends and have blacklist chat
                result = True
            elif self.openChatEnabledYesNo and base.cr.openChatEnabled:
                # they both have black list chat
                result = True
            elif self.wlChatEnabledYesNo and base.cr.whiteListChatEnabled:
                result = True
                
        except:
            # what to do with no base.cr? do we need this in uberdog or AI?
            pass
        
        return result

    def isOnline(self):
        """
        AvatarHandle interface
        """
        return self.onlineYesNo
