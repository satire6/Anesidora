from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
import Avatar
from direct.distributed import DistributedObject

class AvatarPanel(DirectObject.DirectObject):
    """
    This is a panel that pops up in response to clicking on a Toon or
    Cog nearby you, or to picking a Toon from your friends list.  It
    draws a little picture of the avatar's head, and gives you a few
    options to pick from re the avatar.
    """
    # Limit to only have one avatar panel at a time
    currentAvatarPanel = None

    def __init__(self, avatar, FriendsListPanel = None):
        # You can only have one open at a time
        if AvatarPanel.currentAvatarPanel:
            AvatarPanel.currentAvatarPanel.cleanup()
        AvatarPanel.currentAvatarPanel = self

        # Clean up any friends list panels that may be up
        self.friendsListShown = False
        self.FriendsListPanel = FriendsListPanel
        if FriendsListPanel:
            self.friendsListShown = FriendsListPanel.isFriendsListShown()
            FriendsListPanel.hideFriendsList()
        
        if avatar:
            self.avatar = avatar
            self.avName = avatar.getName()
        else:
            self.avatar = None
            self.avName = "Player"

        if (hasattr(avatar, "uniqueName")):
            self.avId = avatar.doId
            self.avDisableName = avatar.uniqueName('disable')
            self.avGenerateName = avatar.uniqueName('generate')
            self.avHpChangeName = avatar.uniqueName('hpChange')

            # If we have an actual DistributedObject for this avatar, use
            # that one instead of whatever we're given.
            if base.cr.doId2do.has_key(self.avId):
                self.avatar = base.cr.doId2do[self.avId]
        else:
            self.avDisableName = None
            self.avGenerateName = None
            self.avHpChangeName = None
            self.avId = None

        if self.avDisableName:
            self.accept(self.avDisableName, self.__handleDisableAvatar)
            
    def cleanup(self):
        if AvatarPanel.currentAvatarPanel != self:
            # Must already be cleaned up
            return

        if self.avDisableName:
            self.ignore(self.avDisableName)
        if self.avGenerateName:
            self.ignore(self.avGenerateName)
        if self.avHpChangeName:
            self.ignore(self.avHpChangeName)

        AvatarPanel.currentAvatarPanel = None
        
    def __handleClose(self):
        self.cleanup()
        AvatarPanel.currentAvatarPanel = None
        if self.friendsListShown:
            # Restore the friends list if it was up before.
            self.FriendsListPanel.showFriendsList()
            
    def __handleDisableAvatar(self):
        #  the old __handleDisableAvatar was sneaking past the inherited class
        if AvatarPanel.currentAvatarPanel:
            AvatarPanel.currentAvatarPanel.handleDisableAvatar()
        else:
            self.handleDisableAvatar()
    
    def handleDisableAvatar(self):
        """
        Called whenever an avatar is disabled, this should cleanup the
        avatar panel if it's not a friend.
        """
        # If the avatar wandered away (or disconnected) shut down the panel.
        self.cleanup()
        AvatarPanel.currentAvatarPanel = None
        
    def isHidden(self):
        # this function should be sub-classed
        return 1
        
    def getType(self):
        return None
