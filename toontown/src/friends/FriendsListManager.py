from pandac.PandaModules import *
import FriendsListPanel
import FriendInviter
import FriendInvitee
import FriendNotifier
from direct.directnotify import DirectNotifyGlobal
from toontown.toon import ToonTeleportPanel
from toontown.friends import ToontownFriendSecret
from toontown.pets import PetAvatarPanel
from toontown.toon import ToonAvatarPanel
from toontown.toon import PlayerInfoPanel
from toontown.suit import SuitAvatarPanel
from toontown.toon import ToonDNA
from toontown.toon import ToonAvatarDetailPanel
from toontown.toon import PlayerDetailPanel
from toontown.toonbase import ToontownGlobals
from toontown.toon import Toon
import FriendHandle
from otp.otpbase import OTPGlobals

class FriendsListManager:
    """
    This is intended to be a base class for state data type objects
    (like PublicWalk) that represent states in which the friends list,
    and associated panels like the avatar panel, are available.  It
    handles all the esoteric message handling and state munging to
    make this work.
    """
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("FriendsListManager")
    
    def __init__(self):
        # Place holders
        self.avatarPanel = None
        self._preserveFriendsList = False
        self._entered = False
        self.friendsRequestQueue = []
      

    def load(self):
        base.cr.friendManager.setGameSpecificFunction(self.processQueuedRequests)
        self.accept(OTPGlobals.AvatarNewFriendAddEvent, self.__friendAdded)
        pass
            
    def unload(self):
        base.cr.friendManager.setGameSpecificFunction(None)
        # Call up the chain
        self.exitFLM()
        if self.avatarPanel:
            del self.avatarPanel
        FriendInviter.unloadFriendInviter()
        ToonAvatarDetailPanel.unloadAvatarDetail()
        ToonTeleportPanel.unloadTeleportPanel()

    def enterFLM(self):
        self.notify.debug("FriendsListManager: enterFLM()")
        # check to see if we're staying active over a Place state transition

        if self._preserveFriendsList:
            self._preserveFriendsList = 0
            return

        self._entered = True
        
        # The friends list and associated events
        self.accept("openFriendsList", self.__openFriendsList)
        self.accept("clickedNametag", self.__handleClickedNametag)
        self.accept("clickedNametagPlayer", self.__handleClickedNametagPlayer)
        base.localAvatar.setFriendsListButtonActive(1)

        # Since we're listening for the click event now, make the
        # nametags clickable.
        NametagGlobals.setMasterNametagsActive(1)
        
        # The Avatar panel buttons
        self.accept("gotoAvatar", self.__handleGotoAvatar)
        self.accept("friendAvatar", self.__handleFriendAvatar)
        self.accept("avatarDetails", self.__handleAvatarDetails)
        self.accept("playerDetails", self.__handlePlayerDetails)

        # An invitation to be someone's friend might come out of the
        # blue.
        self.accept("friendInvitation", self.__handleFriendInvitation)
        
        # todo: check if player friends are available first?
        self.accept(OTPGlobals.PlayerFriendInvitationEvent, self.__handlePlayerFriendInvitation)
        
        if base.cr.friendManager:
            base.cr.friendManager.setAvailable(1)

    def exitFLM(self):
        self.notify.debug("FriendsListManager: exitFLM()")
        # check to see if we're staying active over a Place state transition

        if self._preserveFriendsList:
            return

        if not self._entered:
            return

        self._entered = False
        
        # Put away the friends list
        self.ignore("openFriendsList")
        self.ignore("clickedNametag")
        self.ignore("clickedNametagPlayer")
        base.localAvatar.setFriendsListButtonActive(0)

        # Since we're no longer listening for the click event, make the
        # nametags not be clickable.
        NametagGlobals.setMasterNametagsActive(0)

        # Put away the avatar panel
        if self.avatarPanel:
            self.avatarPanel.cleanup()
            self.avatarPanel = None
        self.ignore("gotoAvatar")
        self.ignore("friendAvatar")
        self.ignore("avatarDetails")
        self.ignore("playerDetails")

        # And the friends list panel
        FriendsListPanel.hideFriendsList()

        # Put away the Secrets panel
        ToontownFriendSecret.hideFriendSecret()

        # No longer interested in invitations from friends
        if base.cr.friendManager:
            base.cr.friendManager.setAvailable(0)
        self.ignore("friendInvitation")

        # Close these auxiliary panels, if they are open.
        FriendInviter.hideFriendInviter()
        ToonAvatarDetailPanel.hideAvatarDetail()
        ToonTeleportPanel.hideTeleportPanel()
        
    def __openFriendsList(self):
        """
        Opens up the friends list when the user presses the hotkey.
        """
        FriendsListPanel.showFriendsList()

    # Handle the Avatar panel
    def __handleClickedNametag(self, avatar, playerId = None):
        """
        Called when an avatar in the world has been picked directly by
        clicking on his nametag, either in the 3-d world or on the
        margins of the 2-d screen.  This should open up an AvatarPanel
        featuring the selected avatar.
        """
        self.notify.debug("__handleClickedNametag. doId = %s" % avatar.doId)
        if avatar.isPet():
            self.avatarPanel = PetAvatarPanel.PetAvatarPanel(avatar)
        elif (isinstance(avatar, Toon.Toon) or
            isinstance(avatar, FriendHandle.FriendHandle)):
            if hasattr(self, "avatarPanel"):
                if self.avatarPanel:
                    if (not hasattr(self.avatarPanel, "getAvId")) or (self.avatarPanel.getAvId() == avatar.doId):
                        if not self.avatarPanel.isHidden():
                            if self.avatarPanel.getType() == "toon":
                                return
            self.avatarPanel = ToonAvatarPanel.ToonAvatarPanel(avatar, playerId)
        else:
            self.avatarPanel = SuitAvatarPanel.SuitAvatarPanel(avatar)
            
    def __handleClickedNametagPlayer(self, avatar, playerId, showType = 1):
        """
        Called when an avatar in the world has been picked directly by
        clicking on his nametag, either in the 3-d world or on the
        margins of the 2-d screen.  This should open up an AvatarPanel
        featuring the selected avatar.
        """
        self.notify.debug("__handleClickedNametagPlayer PlayerId%s" % (playerId))
        if showType == 1:
            if hasattr(self, "avatarPanel"):
                if self.avatarPanel:
                    if (not hasattr(self.avatarPanel, "getPlayerId")) or (self.avatarPanel.getPlayerId() == playerId):
                        if not self.avatarPanel.isHidden():
                            if self.avatarPanel.getType() == "player":
                                return
            self.avatarPanel = PlayerInfoPanel.PlayerInfoPanel(playerId)
        elif (isinstance(avatar, Toon.Toon) or
            isinstance(avatar, FriendHandle.FriendHandle)):
            if hasattr(self, "avatarPanel"):
                if self.avatarPanel:
                    if (not hasattr(self.avatarPanel, "getAvId")) or (self.avatarPanel.getAvId() == avatar.doId):
                        if not self.avatarPanel.isHidden():
                            if self.avatarPanel.getType() == "toon":    
                                return
            self.avatarPanel = ToonAvatarPanel.ToonAvatarPanel(avatar, playerId)
            


    # Teleport to an avatar when you click "goto" from the Avatar panel. 
    def __handleGotoAvatar(self, avId, avName, avDisableName):
        """__handleGotoAvatar(self, int avId, string avName, string avDisableName)

        Called when the user clicks the "goto" button from the Avatar
        panel, this should initiate the teleport-to-avatar process.
        """
        # This whole process is a little circuitous.  We can't go
        # directly to the avatar, since we're not sure which shard,
        # hood, and zone the avatar is in.  We have to ask these
        # questions of the avatar, which involves a round-trip
        # peer-to-peer message.

        # The TeleportPanel will manage this communication, and will
        # tell the place fsm to enter the teleportOut state when it's got
        # the information for us.  Of course, the TeleportPanel might
        # fail or be canceled by the user, in which case nothing
        # happens.
        ToonTeleportPanel.showTeleportPanel(avId, avName, avDisableName)

    # Invite an avatar to be your friend.
    def __handleFriendAvatar(self, avId, avName, avDisableName):
        """__handleFriendAvatar(self, int avId, string avName, string avDisableName)

        Called when the user clicks the "friend" button from the
        Avatar panel, this should send an invitation to the avatar to
        be our friend.
        """
        FriendInviter.showFriendInviter(avId, avName, avDisableName)

    # Be invited by another avatar to be their friend.
    def __handleFriendInvitation(self, avId, avName, inviterDna, context):
        """__handleFriendInvitation(self, int avId, string avName,
                                    AvatarDNA dna, int context)

        Called when another avatar somewhere in the world has invited
        us to be their friend.
        """
        # We create a new FriendInvitee panel, but we don't save the
        # pointer.  We don't need to do anything else with the panel,
        # and we trust the panel to manage itself and clean itself up
        # properly when the user answers yes or no.

        dna = ToonDNA.ToonDNA()
        dna.makeFromNetString(inviterDna)

        if not base.cr.avatarFriendsManager.checkIgnored(avId):
            FriendInvitee.FriendInvitee(avId, avName, dna, context)
        
    # Be invited by another player to be their friend.
    def __handlePlayerFriendInvitation(self, avId, avName, inviterDna = None, context = None):
        self.notify.debug("incoming switchboard friend event")
        self.friendsRequestQueue.append((avId, avName, inviterDna, context))
        if base.cr.friendManager.getAvailable():
            self.processQueuedRequests()
            
    def processQueuedRequests(self):
        if len(self.friendsRequestQueue):
            request = self.friendsRequestQueue.pop(0)
            self.__processFriendRequest(request[0], request[1], request[2], request[3])          
            
    def __processFriendRequest(self, avId, avName, inviterDna = None, context = None):
        """__handleAvatarFriendInvitation(self, int avId, string avName,
                                    AvatarDNA dna, int context)

        Called when another avatar somewhere in the world has invited
        us to be their friend.
        """
        # We create a new FriendInvitee panel, but we don't save the
        # pointer.  We don't need to do anything else with the panel,
        # and we trust the panel to manage itself and clean itself up
        # properly when the user answers yes or no.

        self.notify.debug("__handleAvatarFriendInvitation")

        askerToon = base.cr.doId2do.get(avId)
        if askerToon:
            self.notify.debug("got toon")
            dna = askerToon.getStyle()
            #dna.makeFromNetString(askerToon.getStyle)
            if not base.cr.avatarFriendsManager.checkIgnored(avId):
                FriendInvitee.FriendInvitee(avId, avName, dna, context)
        else:
            self.notify.debug("no toon")

    def __handleAvatarDetails(self, avId, avName, playerId = None):
        """__handleAvatarDetails(self, int avId, string avName)

        Bring up a detail panel on a particular avatar.
        """
        ToonAvatarDetailPanel.showAvatarDetail(avId, avName, playerId)
        
    def __handlePlayerDetails(self, avId, avName, playerId = None):
        """__handleAvatarDetails(self, int avId, string avName)

        Bring up a detail panel on a particular avatar.
        """
        PlayerDetailPanel.showPlayerDetail(avId, avName, playerId)

    def preserveFriendsList(self):
        """call this just before calling setState if you do not want the
        friends list mgr to reset when transitioning between two states
        that have the friends list enabled"""
        self.notify.debug("Preserving Friends List")
        self._preserveFriendsList = True
        
    def __friendAdded(self, avId):
        if FriendInviter.globalFriendInviter != None:
            messenger.send("FriendsListManagerAddEvent", [avId])
        else:
            friendToon = base.cr.doId2do.get(avId)
            if friendToon:
                print("got toon")
                dna = friendToon.getStyle()
                #dna.makeFromNetString(askerToon.getStyle)
                FriendNotifier.FriendNotifier(avId, friendToon.getName(), dna, None)
        

