from pandac.PandaModules import *
from direct.task.Task import Task
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.toon import ToonTeleportPanel
from toontown.suit import Suit
from toontown.pets import Pet
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog import RejectCode

globalFriendInviter = None

def showFriendInviter(avId, avName, avDisableName):
    # A module function to open the global friend inviter panel.
    global globalFriendInviter
    if globalFriendInviter != None:
        globalFriendInviter.cleanup()
        globalFriendInviter = None

    globalFriendInviter = FriendInviter(avId, avName, avDisableName)

def hideFriendInviter():
    # A module function to close the global friend inviter if it is open.
    global globalFriendInviter
    if globalFriendInviter != None:
        globalFriendInviter.cleanup()
        globalFriendInviter = None

def unloadFriendInviter():
    # A module function to completely unload the global friend
    # inviter.  This is the same thing as hideFriendInviter, actually.
    global globalFriendInviter
    if globalFriendInviter != None:
        globalFriendInviter.cleanup()
        globalFriendInviter = None

class FriendInviter(DirectFrame):
    """FriendInviter:
    This is a panel that pops up in response to clicking the "Friend"
    button on the AvatarPanel.  It contacts the FriendManager to
    invite the given avatar to be your friend, and keeps you informed
    of the current status.

    """

    notify = DirectNotifyGlobal.directNotify.newCategory("FriendInviter")

    def __init__(self, avId, avName, avDisableName):

        # config player friends off until PAM templates integrate with the website
        self.wantPlayerFriends = base.config.GetBool('want-player-friends', 0)
        
        # initialize our base class.
        DirectFrame.__init__(
            self,
            pos = (0.3, 0.1, 0.65),
            image_color = GlobalDialogColor,
            image_scale = (1.0, 1.0, 0.6),
            text = '',
            text_wordwrap = TTLocalizer.FIdirectFrameTextWorkWrap,
            text_scale = TTLocalizer.FIdialog,
            text_pos = (0.0, TTLocalizer.FIdirectFrameTextPosZ),
            )

        # For some reason, we need to set this after construction to
        # get it to work properly.
        self['image'] = DGG.getDefaultDialogGeom()

        self.avId = avId
        self.toonName = avName
        avatar = base.cr.doId2do.get(self.avId)
        self.playerId = None
        self.playerName = None
        
        if avatar:
            # todo: what if these aren't defined?
            self.playerId = avatar.DISLid
            # todo: why do we need to do this?
            self.playerName = avatar.DISLname + " " + str(avatar.DISLid)
        self.avDisableName = avDisableName

        # set this if we want to make a player/account friend
        self.playerFriend = 0

        self.fsm = ClassicFSM.ClassicFSM('FriendInviter',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff),
                            State.State('getNewFriend',
                                        self.enterGetNewFriend,
                                        self.exitGetNewFriend),
                            State.State('begin',
                                        self.enterBegin,
                                        self.exitBegin),
                            State.State('check',
                                        self.enterCheck,
                                        self.exitCheck),
                            State.State('tooMany',
                                        self.enterTooMany,
                                        self.exitTooMany),
                            State.State('checkAvailability',
                                        self.enterCheckAvailability,
                                        self.exitCheckAvailability),
                            State.State('notAvailable',
                                        self.enterNotAvailable,
                                        self.exitNotAvailable),
                            State.State('notAcceptingFriends',
                                        self.enterNotAcceptingFriends,
                                        self.exitNotAcceptingFriends),
                            State.State('wentAway',
                                        self.enterWentAway,
                                        self.exitWentAway),
                            State.State('already',
                                        self.enterAlready,
                                        self.exitAlready),
                            State.State('askingCog',
                                        self.enterAskingCog,
                                        self.exitAskingCog),
                            State.State('askingPet',
                                        self.enterAskingPet,
                                        self.exitAskingPet),
                            State.State('endFriendship',
                                        self.enterEndFriendship,
                                        self.exitEndFriendship),
                            State.State('friendsNoMore',
                                        self.enterFriendsNoMore,
                                        self.exitFriendsNoMore),
                            State.State('self',
                                        self.enterSelf,
                                        self.exitSelf),
                            State.State('ignored',
                                        self.enterIgnored,
                                        self.exitIgnored),
                            State.State('asking',
                                        self.enterAsking,
                                        self.exitAsking),
                            State.State('yes',
                                        self.enterYes,
                                        self.exitYes),
                            State.State('no',
                                        self.enterNo,
                                        self.exitNo),
                            State.State('otherTooMany',
                                        self.enterOtherTooMany,
                                        self.exitOtherTooMany),
                            State.State('maybe',
                                        self.enterMaybe,
                                        self.exitMaybe),
                            State.State('down',
                                        self.enterDown,
                                        self.exitDown),
                            State.State('cancel',
                                        self.enterCancel,
                                        self.exitCancel),
                            ],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )

        # This will be filled in with the active context, when we are
        # in states that have a context.
        self.context = None

        # This is imported here instead of at the top of the file to
        # protect against circular imports.
        from toontown.toon import ToonAvatarDetailPanel

        # Now set up the panel.
        ToonTeleportPanel.hideTeleportPanel()
        ToonAvatarDetailPanel.hideAvatarDetail()

        # Create some buttons.
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')

        self.bOk = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendInviterOK,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (0.0, 0.0, -0.1),
            command = self.__handleOk
            )
        self.bOk.hide()

        self.bCancel = DirectButton(
            self,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendInviterCancel,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (TTLocalizer.FIcancelButtonPositionX, 0.0, -0.1),
            command = self.__handleCancel
            )
        self.bCancel.hide()

        self.bStop = DirectButton(
            self,
            image = (gui.find('**/Ignore_Btn_UP'),
                     gui.find('**/Ignore_Btn_DN'),
                     gui.find('**/Ignore_Btn_RLVR')),
            relief = None,
            text = OTPLocalizer.FriendInviterStopBeingFriends,
            text_align = TextNode.ALeft,
            text_scale = TTLocalizer.FIstopButton,
            text_pos = (0.075, TTLocalizer.FIstopTextPositionY),
            pos = (TTLocalizer.FIstopButtonPositionX, 0.0, 0.05),
            command = self.__handleStop
            )
        self.bStop.hide()

        self.bYes = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendInviterYes,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (TTLocalizer.FIyesButtonPositionX, 0.0, -0.1),
            command = self.__handleYes
            )
        self.bYes.hide()

        self.bNo = DirectButton(
            self,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            relief = None,
            text = OTPLocalizer.FriendInviterNo,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (0.15, 0.0, -0.1),
            command = self.__handleNo
            )
        self.bNo.hide()

        # make an avatar friend
        self.bToon = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = TTLocalizer.FriendInviterToon,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (-0.35, 0.0, -0.05),
            command = self.__handleToon
            )

        # make a label to show feature desc on rollover
        toonText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(0.35, 0, -0.2),
            text = TTLocalizer.FriendInviterToonFriendInfo,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.045,
            text_align = TextNode.ACenter,
            )
        toonText.reparentTo(self.bToon.stateNodePath[2])
            
        self.bToon.hide()

        # make an account friend
        self.bPlayer = DirectButton(
            self,
            image = (buttons.find('**/ChtBx_OKBtn_UP'),
                     buttons.find('**/ChtBx_OKBtn_DN'),
                     buttons.find('**/ChtBx_OKBtn_Rllvr')),
            relief = None,
            text = TTLocalizer.FriendInviterPlayer,
            text_scale = 0.05,
            text_pos = (0.0, -0.1),
            pos = (0.0, 0.0, -0.05),
            command = self.__handlePlayer
            )
        
        # make a label to show feature desc on rollover
        playerText = DirectLabel(
            parent = self,
            relief = None,
            pos = Vec3(0, 0, -0.2),
            text = TTLocalizer.FriendInviterPlayerFriendInfo,
            text_fg = (0, 0, 0, 1),
            text_pos = (0, 0),
            text_scale = 0.045,
            text_align = TextNode.ACenter,
            )
        playerText.reparentTo(self.bPlayer.stateNodePath[2])

        self.bPlayer.hide()

        buttons.removeNode()
        gui.removeNode()

        self.fsm.enterInitialState()

        if self.avId == None:
            # If we don't have an initial avatar ID, make the user
            # indicate one.
            self.fsm.request('getNewFriend')
        else:
            self.fsm.request('begin')

    def cleanup(self):
        """cleanup(self):

        Cancels any pending request and removes the panel from the
        screen.

        """
        self.fsm.request('cancel')
        del self.fsm

        self.destroy()

    
    def getName(self):
        """getName(self):

        Return the appropritate name for the type of friend we are making/breaking.
        If the name is not defined, use a reasonable default.

        """
        if self.playerFriend:
            name = self.playerName
            if name == None:
                name = TTLocalizer.FriendInviterThatPlayer
        else:
            name = self.toonName
            if name == None:
                name = TTLocalizer.FriendInviterThatToon
        return name

    ##### Off state #####

    # Represents the initial state of the friend query: no query in
    # progress.

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ##### GetNewFriend state #####

    # We have clicked on the "new friend" from the friends list panel,
    # but we haven't identified who we'd like to add as our new friend
    # yet.

    def enterGetNewFriend(self):
        self['text'] = (TTLocalizer.FriendInviterClickToon % (len(base.localAvatar.friendsList)))
        if base.cr.productName in ['JP', 'DE', 'BR', 'FR']:
            self.bOk.show()
        else:
            self.bCancel.show()
        self.accept("clickedNametag", self.__handleClickedNametag)

    def exitGetNewFriend(self):
        self.bCancel.hide()
        self.ignore("clickedNametag")

    def __handleClickedNametag(self, avatar):
        self.avId = avatar.doId
        self.toonName = avatar.getName()
        if hasattr(avatar, "DISLid"):
            self.playerId = avatar.DISLid
            self.playerName = avatar.DISLname
        self.avDisableName = avatar.uniqueName('disable')
        self.fsm.request('begin')


    ##### Begin state #####

    # We have clicked on the "friend" button from a panel.
    # Determine what type of friendship the player would like to make.

    def enterBegin(self):
        myId = base.localAvatar.doId

        # ask the user what kind of friend we want to make
        self['text'] = TTLocalizer.FriendInviterBegin
        
        
        # slide this button over a bit to accomodate three options
        self.bCancel.setPos(0.35, 0.0, -0.05)
        self.bCancel.show()
        
        
        self.bToon.show()
        # cling-on products are not yet swicthboard compliant
        if self.wantPlayerFriends and (base.cr.productName != 'DisneyOnline-UK') and (base.cr.productName != 'DisneyOnline-AP'):
            self.bPlayer.show()
        else: #we can assume toon
            self.__handleToon()
            


        # handle go away
        assert(self.avDisableName != None)
        self.accept(self.avDisableName, self.__handleDisableAvatar)    


    def exitBegin(self):
        self.ignore(self.avDisableName)
        self.bToon.hide()
        # cling-on products are not yet swicthboard comliant
        if self.wantPlayerFriends and (base.cr.productName != 'DisneyOnline-UK') and (base.cr.productName != 'DisneyOnline-AP'):
            self.bPlayer.hide()
        # slide this button back to two option position
        self.bCancel.setPos(0.0, 0.0, -0.1)
        self.bCancel.hide()

    ##### Check state #####

    # We have chosen what sort of friend to make.
    # Decide whether we are already friends or not.

    def enterCheck(self):
        myId = base.localAvatar.doId
        
        assert(self.avDisableName != None)
        self.accept(self.avDisableName, self.__handleDisableAvatar)

        # the player has asked themselves
        if (self.avId == myId):
            self.fsm.request('self')
        # already avatar friends
        elif not self.playerFriend and base.cr.isFriend(self.avId):
            self.fsm.request('already')
        # already player friends
        elif self.playerFriend and base.cr.playerFriendsManager.isPlayerFriend(self.avId):
        # test
        #elif self.playerFriend:
            self.fsm.request('already')
        else:
            # check for full friends list
            if not self.playerFriend:
                tooMany = (len(base.localAvatar.friendsList) >= MaxFriends)
            elif self.playerFriend:
                tooMany = base.cr.playerFriendsManager.friendsListFull()
            if tooMany:
                self.fsm.request('tooMany')
            else:
                # we made it - ask them to be friends
                self.fsm.request('checkAvailability')

    def exitCheck(self):
        self.ignore(self.avDisableName)

    ##### TooMany state #####

    # We are not yet friends with the given avatar, but we have too
    # many friends on our list to add another one.

    def enterTooMany(self):
        if self.playerFriend:
            text = OTPLocalizer.FriendInviterPlayerTooMany
            name = self.playerName
        else:
            text = OTPLocalizer.FriendInviterToonTooMany
            name = self.toonName
        self['text'] = text % name
        self.bCancel.show()
        self.bCancel.setPos(0.0, 0.0, -0.16)

    def exitTooMany(self):
        self.bCancel.hide()

    ##### Checking availability state #####

    # We have indicated that we would like another avatar or player
    # to be our friend.  We are now checking whether the avatar is
    # available to be invited.

    def enterCheckAvailability(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)

        # This should only matter if we are making toon friends
        if not self.playerFriend:
            # If the avatar is not in the same zone as us, s/he's not
            # available.  Don't even bother the AI about it.  This really
            # shouldn't be possible, but maybe someone managed to click
            # the "Friend" button before the AvatarPanel shut itself down
            # or something dumb like that.
            if not base.cr.doId2do.has_key(self.avId):
                self.fsm.request('wentAway')
                return

        if not base.cr.doId2do.has_key(self.avId):            
            self.fsm.request('wentAway')
            return
        else:
            avatar = base.cr.doId2do.get(self.avId)
        
        if isinstance(avatar, Suit.Suit):
            # If we accidentally ask a Cog to be our friend, the Cog
            # will always say no!
            self.fsm.request('askingCog')
            return

        if isinstance(avatar, Pet.Pet):
            # Handle if we ask a pet to be our friend
            self.fsm.request('askingPet')
            return

        # This should only matter if we are making toon friends
        if not self.playerFriend:
            # If we don't have a FriendManager, something's badly wrong.
            # Most likely we're running in a development environment
            # without an AI client.
            if not base.cr.friendManager:
                self.notify.warning("No FriendManager available.")
                self.fsm.request('down')
                return

        # ask switchboard for player friend
        if self.playerFriend:
            self.notify.info("Inviter requesting player friend")
            self['text'] = OTPLocalizer.FriendInviterAsking % (self.playerName)
            base.cr.playerFriendsManager.sendRequestInvite(self.playerId)
            self.accept(OTPGlobals.PlayerFriendRejectInviteEvent, self.__playerFriendRejectResponse)
            self.accept(OTPGlobals.PlayerFriendAddEvent, self.__playerFriendAcceptResponse)
            #self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__playerFriendAcceptResponse)
            self.bOk.show()
        # ask otp server for avatar friend
        else:
            base.cr.friendManager.up_friendQuery(self.avId)
            self['text'] = OTPLocalizer.FriendInviterCheckAvailability % (self.toonName)
            self.accept('friendResponse', self.__friendResponse)
            self.bCancel.show()        

        self.accept('friendConsidering', self.__friendConsidering)

    def exitCheckAvailability(self):
        self.ignore(self.avDisableName)
        self.ignore('friendConsidering')
        self.ignore('friendResponse')
        self.bCancel.hide()

    ##### Not available state #####

    # In this state, the avatar we have invited to be our friend is
    # currently not available to answer that query: maybe he's in a
    # minigame or something.

    def enterNotAvailable(self):
        self['text'] = OTPLocalizer.FriendInviterNotAvailable % (self.getName())
        self.context = None
        self.bOk.show()

    def exitNotAvailable(self):
        self.bOk.hide()

    ##### notAcceptingFriends state #####

    # In this state, the avatar we have invited is not accepting new friends

    def enterNotAcceptingFriends(self):
        self['text'] = OTPLocalizer.FriendInviterFriendSaidNoNewFriends % (self.getName())
        self.context = None
        self.bOk.show()

    def exitNotAcceptingFriends(self):
        self.bOk.hide()

    ##### Went away state #####

    # The avatar was here, but now he's gone.

    def enterWentAway(self):
        self['text'] = OTPLocalizer.FriendInviterWentAway % (self.getName())
        if not self.playerFriend:
            if self.context != None:
                base.cr.friendManager.up_cancelFriendQuery(self.context)
                self.context = None
        self.bOk.show()

    def exitWentAway(self):
        self.bOk.hide()

    ##### Already state #####

    # The avatar is already our friend.  Does the user want to end the
    # friendship?

    def enterAlready(self):
        # set the correct messaging for the type of friendship
        if self.playerFriend:
            self['text'] = TTLocalizer.FriendInviterPlayerAlready % (self.getName())
            self.bStop['text'] = TTLocalizer.FriendInviterStopBeingPlayerFriends
        else:
            self['text'] = TTLocalizer.FriendInviterToonAlready % (self.getName())
            self.bStop['text'] = TTLocalizer.FriendInviterStopBeingToonFriends
        self.context = None
        if base.cr.productName in ['JP', 'DE', 'BR', 'FR']:
            self.bStop.setPos(-0.20, 0.0, -0.1)
            self.bCancel.setPos(0.20, 0.0, -0.1)
        self.bStop.show()
        self.bCancel.show()

    def exitAlready(self):
        self['text'] = ''
        self.bStop.hide()
        self.bCancel.hide()


    ##### AskingCog state #####

    # We are asking a cog to be our friend.  Delay for a moment to
    # pretend we're actually doing something, then say no.

    def enterAskingCog(self):
        self['text'] = OTPLocalizer.FriendInviterAskingCog % (self.getName())
        taskMgr.doMethodLater(2.0, self.cogReplies, "cogFriendship")
        self.bCancel.show()

    def exitAskingCog(self):
        taskMgr.remove("cogFriendship")
        self.bCancel.hide()

    def cogReplies(self, task):
        # The cog said no!
        self.fsm.request('no')
        return Task.done


    ##### AskingPet state #####

    # We are asking a pet to be our friend.  Delay for a moment to
    # pretend we're actually doing something, then say no.

    def enterAskingPet(self):
        self['text'] = OTPLocalizer.FriendInviterAskingPet % (self.getName())
        if base.localAvatar.hasPet():
            if base.localAvatar.getPetId() == self.avId:
                #this is MY pet!
                self['text'] = OTPLocalizer.FriendInviterAskingMyPet % (self.getName())

        self.context = None
        self.bOk.show()

    def exitAskingPet(self):
        self.bOk.hide()


    ##### EndFriendship state #####

    # We asked to end the existing friendship with the avatar.

    def enterEndFriendship(self):
        # if we want to break a player friendship
        if self.playerFriend:
            self['text'] = TTLocalizer.FriendInviterEndFriendshipPlayer % (self.getName())
            if base.cr.isFriend(self.avId):
                # tell the user they will remain toon friends
                self['text'] = self['text'] + (TTLocalizer.FriendInviterRemainToon % self.toonName)
        # if we want to break toon friendship
        else:
            self['text'] = TTLocalizer.FriendInviterEndFriendshipToon % (self.getName())
            if base.cr.playerFriendsManager.isPlayerFriend(self.playerId):
            # test
            #if 1:
                # tell the user they will remain player friends
                self['text'] = self['text'] + (TTLocalizer.FriendInviterRemainPlayer % self.playerName)

        self.context = None
        self.bYes.show()
        self.bNo.show()

    def exitEndFriendship(self):
        self.bYes.hide()
        self.bNo.hide()

    ##### FriendsNoMore state #####

    # We are no longer friends with the avatar.

    def enterFriendsNoMore(self):
        if self.playerFriend:
            self.notify.info("### send player remove")
            base.cr.playerFriendsManager.sendRequestRemove(self.playerId)
        else:
            self.notify.info("### send avatar remove")
            base.cr.removeFriend(self.avId)
            
        self['text'] = OTPLocalizer.FriendInviterFriendsNoMore % (self.getName())
        self.bOk.show()

        # TODO: determine if we need to do the below for player & toon friends
        
        # Now, one special case.  Since the AvatarPanel is only
        # allowed to remain on a toon not in the zone if the toon is
        # our friend, we must shut down the AvatarPanel now if the
        # toon is not in the zone.

        # We cheat by sending a spurious "disable" message in this
        # case.  Presumably this will not confuse anyone, since no one
        # else should be listening for this toon's disable message.
        if not base.cr.doId2do.has_key(self.avId):
            messenger.send(self.avDisableName)

    def exitFriendsNoMore(self):
        self.bOk.hide()

    ##### Self state #####

    # Invalid attempt to be friends with yourself.

    def enterSelf(self):
        self['text'] = OTPLocalizer.FriendInviterSelf
        self.context = None
        self.bOk.show()

    def exitSelf(self):
        self.bOk.hide()

    ##### Ignored state #####

    # The toon we invited to friendship is ignoring us.

    def enterIgnored(self):
        self['text'] = OTPLocalizer.FriendInviterIgnored % (self.toonName)
        self.context = None
        self.bOk.show()

    def exitIgnored(self):
        self.bOk.hide()

    ##### Asking state #####

    # In this state, we have asked the other avatar to be our friend,
    # and we're waiting for a response from his user.

    def enterAsking(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self['text'] = OTPLocalizer.FriendInviterAsking % (self.toonName)
        self.accept('friendResponse', self.__friendResponse)
        self.bCancel.show()

    def exitAsking(self):
        self.ignore(self.avDisableName)
        self.ignore('friendResponse')
        self.bCancel.hide()

    ##### Yes state #####

    # The other user has indicated that he would like to be our
    # friend.

    def enterYes(self):
        self['text'] = OTPLocalizer.FriendInviterFriendSaidYes % (self.toonName)
        self.context = None
        self.bOk.show()

    def exitYes(self):
        self.bOk.hide()

    ##### No state #####

    # The other user has indicated that he does not want to be
    # friends.

    def enterNo(self):
        self['text'] = OTPLocalizer.FriendInviterFriendSaidNo % (self.toonName)
        self.context = None
        self.bOk.show()

    def exitNo(self):
        self.bOk.hide()

    ##### OtherTooMany state #####

    # The other user has too many friends already.

    def enterOtherTooMany(self):
        self['text'] = OTPLocalizer.FriendInviterOtherTooMany % (self.toonName)
        self.context = None
        self.bOk.show()

    def exitOtherTooMany(self):
        self.bOk.hide()

    ##### Maybe state #####

    # The other user didn't get a chance to reply when something made the
    # panel go away.

    def enterMaybe(self):
        self['text'] = OTPLocalizer.FriendInviterMaybe % (self.toonName)
        self.context = None
        self.bOk.show()

    def exitMaybe(self):
        self.bOk.hide()

    ##### Down state #####

    # The FriendInviter is down right now because something is
    # wrong--like maybe the AI client isn't running?

    def enterDown(self):
        self['text'] = OTPLocalizer.FriendInviterDown
        self.context = None
        self.bOk.show()

    def exitDown(self):
        self.bOk.hide()

    ##### Cancel state #####

    # We got tired of waiting and hit the cancel button.

    def enterCancel(self):
        # we cannot cancel switchboard requests (by design)
        if not self.playerFriend:
            if self.context != None:
                base.cr.friendManager.up_cancelFriendQuery(self.context)
                self.context = None
        self.fsm.request('off')

    def exitCancel(self):
        pass


    ### Button handing methods

    def __handleOk(self):
        unloadFriendInviter()

    def __handleCancel(self):
        if base.friendMode == 1:
            if self.avId:
                base.cr.avatarFriendsManager.sendRequestRemove(self.avId) #friends change 7
        unloadFriendInviter()

    def __handleStop(self):
        self.fsm.request('endFriendship')

    def __handleYes(self):
        if (self.fsm.getCurrentState().getName() == 'endFriendship'):
            # yes: we want to end our friendship with the avatar.
            self.fsm.request('friendsNoMore')
        else:
            unloadFriendInviter()

    def __handleToon(self):
        if (self.fsm.getCurrentState().getName() == 'begin'):
            self.fsm.request('check')
        else:
            unloadFriendInviter()

    def __handlePlayer(self):
        if (self.fsm.getCurrentState().getName() == 'begin'):
            self.playerFriend = 1
            self.fsm.request('check')
        else:
            unloadFriendInviter()

    def __handleNo(self):
        unloadFriendInviter()

    def __handleList(self):
        messenger.send('openFriendsList')


    ### Support methods

    def __friendConsidering(self, yesNoAlready, context):
        if yesNoAlready == 1:
            # The other avatar is considering our request.
            self.context = context
            self.fsm.request('asking')
        elif yesNoAlready == 0:
            # The other avatar cannot consider our request now.
            self.fsm.request('notAvailable')
        elif yesNoAlready == 2:
            # The other avatar is already our friend!
            self.fsm.request('already')
        elif yesNoAlready == 3:
            # Oops, attempt to befriend ourselves.
            self.fsm.request('self')
        elif yesNoAlready == 4:
            # We're being ignored.
            self.fsm.request('ignored')
        elif yesNoAlready == 6:
            # The other avatar is not accepting new friends
            self.fsm.request('notAcceptingFriends')
        elif yesNoAlready == 10:
            # You recently asked, and he said no last time.
            self.fsm.request('no')
        elif yesNoAlready == 13:
            # You recently asked, and he had too many friends.
            self.fsm.request('otherTooMany')
        else:
            # Something went wrong.
            self.notify.warning("Got unexpected response to friendConsidering: %s" % (yesNoAlready))
            self.fsm.request('maybe')

    def __friendResponse(self, yesNoMaybe, context):
        if self.context != context:
            self.notify.warning("Unexpected change of context from %s to %s." % \
                                (self.context, context))
            self.context = context

        if yesNoMaybe == 1:
            # The other avatar is willing to be our friend.
            self.fsm.request('yes')
        elif yesNoMaybe == 0:
            # The other avatar will not be our friend.
            self.fsm.request('no')
        elif yesNoMaybe == 3:
            # The other avatar has too many friends.
            self.fsm.request('otherTooMany')
        else:
            # The other avatar had some trouble with the panel.
            self.notify.warning("Got unexpected response to friendResponse: %s" % (yesNoMaybe))
            self.fsm.request('maybe')

    def __playerFriendRejectResponse(self, avId, reason):
        self.notify.debug("Got reject response to friendResponse: %s" % (reason))
        if reason == RejectCode.RejectCode.INVITATION_DECLINED:
            # The other avatar will not be our friend.
            self.fsm.request('no')
        elif reason == RejectCode.RejectCode.FRIENDS_LIST_FULL:
            # The other avatar has too many friends.
            self.fsm.request('otherTooMany')
        else:
            # The other avatar had some trouble with the panel.
            self.notify.warning("Got unexpected response to friendResponse: %s" % (reason))
            self.fsm.request('maybe')

    def __playerFriendAcceptResponse(self):
        # The other avatar is willing to be our friend.
        self.fsm.request('yes')

    def __handleDisableAvatar(self):
        """__handleDisableAvatar(self)

        Called whenever the avatar in question is disabled, this
        should update the panel appropriately.

        """
        self.fsm.request('wentAway')
        
