from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import Functor
from direct.task.Task import Task
from direct.distributed import DistributedObject
from otp.avatar import Avatar, AvatarPanel
from toontown.toon import ToonHead
from toontown.toon import LaffMeter
from toontown.toon import ToonAvatarDetailPanel
from toontown.friends import FriendHandle
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.pets import Pet, PetConstants, PetDetailPanel

class PetAvatarPanel(AvatarPanel.AvatarPanel):
    """PetAvatarPanel:

    This is a panel that pops up in response to clicking on a Pet nearby you, 
    or to picking a Toon from your friends list.  It draws a little picture
    of the pet's head, and gives you a few options to pick from re the avatar.

    """

    notify = directNotify.newCategory("PetAvatarPanel")

    def __init__(self, avatar):
        """__init__(self)"""
        self.notify.debug("Init(): doId=%s" % avatar.doId)

        #determine if this avatar is in the same zone as the localtoon
        distPet = base.cr.doId2do.get(avatar.doId)
        if distPet and not distPet.isProxy():
            self.avatar = distPet
            self.petIsLocal = True
        else:
            self.avatar = avatar
            self.petIsLocal = False

        from toontown.friends import FriendsListPanel
        AvatarPanel.AvatarPanel.__init__(
            self, self.avatar, FriendsListPanel = FriendsListPanel)

        base.localAvatar.obscureFriendsListButton(1)

        base.panel = self

        gui = loader.loadModel("phase_3.5/models/gui/PetControlPannel")
        guiScale = 0.116
        guiPos = (1.12, 0, 0.30)
        self.frame = DirectFrame(
                parent = aspect2dp,
                image = gui,
                scale = guiScale,
                pos = guiPos,
                relief = None,
                )
            
        disabledImageColor = Vec4(.6,.6,.6,1)
        text0Color = Vec4(1,1,1,1)
        text1Color = Vec4(0.5,1,0.5,1)
        text2Color = Vec4(1,1,0.5,1)
        text3Color = Vec4(.6,.6,.6,1)

        self.closeButton = DirectButton(
                parent = self.frame,
                image = (gui.find("**/CancelButtonUp"),
                         gui.find("**/CancelButtonDown"),
                         gui.find("**/CancelButtonRollover"),
                         ),
                relief = None,
                command = self.__handleClose,
                )
        self.feedButton = DirectButton(
                parent = self.frame,
                image = (gui.find("**/ButtonFeedUp"),
                         gui.find("**/ButtonFeedDown"),
                         gui.find("**/ButtonFeedRollover"),
                         gui.find("**/ButtonFeedUp"),
                         ),
                geom = gui.find("**/PetControlFeedIcon"),
                geom3_color = disabledImageColor,
                image3_color = disabledImageColor,
                relief = None,
                text = TTLocalizer.PetPanelFeed,
                text_scale = TTLocalizer.PAPfeed,
                text0_fg = text0Color,
                text1_fg = text1Color,
                text2_fg = text2Color,
                text3_fg = text3Color,
                text_pos = (-0.5,2.8),
                text_align = TextNode.ALeft,
                command = self.__handleFeed,
                )
        if not self.petIsLocal:
            self.feedButton['state'] = DGG.DISABLED
        else:
            self.feedButton['state'] = self.feedButtonState()

        self.callButton = DirectButton(
                parent = self.frame,
                image = (gui.find("**/ButtonGoToUp"),
                         gui.find("**/ButtonGoToDown"),
                         gui.find("**/ButtonGoToRollover"),
                         gui.find("**/ButtonGoToUp"),
                         ),
                geom = gui.find("**/PetControlGoToIcon"),
                geom3_color = disabledImageColor,
                image3_color = disabledImageColor,
                relief = None,
                text = TTLocalizer.PetPanelCall,
                text0_fg = text0Color,
                text1_fg = text1Color,
                text2_fg = text2Color,
                text3_fg = text3Color,
                text_scale = TTLocalizer.PAPcall,
                text_pos = (-0.5,1.3),
                text_align = TextNode.ALeft,
                command = self.__handleCall,
                )
        if not self.petIsLocal:
            self.callButton['state'] = DGG.DISABLED

        self.scratchButton = DirectButton(
                parent = self.frame,
                image = (gui.find("**/ButtonScratchUp"),
                         gui.find("**/ButtonScratchDown"),
                         gui.find("**/ButtonScratchRollover"),
                         gui.find("**/ButtonScratchUp"),
                         ),
                geom = gui.find("**/PetControlScratchIcon"),
                geom3_color = disabledImageColor,
                image3_color = disabledImageColor,
                relief = None,
                text = TTLocalizer.PetPanelScratch,
                text0_fg = text0Color,
                text1_fg = text1Color,
                text2_fg = text2Color,
                text3_fg = text3Color,
                text_scale = TTLocalizer.PAPscratch,
                text_pos = (-0.5,2.05),
                text_align = TextNode.ALeft,
                command = self.__handleScratch,
                )
        if not self.petIsLocal:
            self.scratchButton['state'] = DGG.DISABLED

        self.ownerButton = DirectButton(
                parent = self.frame,
                image = (gui.find("**/PetControlToonButtonUp"),
                         gui.find("**/PetControlToonButtonDown"),
                         gui.find("**/PetControlToonButtonRollover"),
                         ),
                geom = gui.find("**/PetControlToonIcon"),
                geom3_color = disabledImageColor,
                relief = None,
                image3_color = disabledImageColor,
                text = ("", TTLocalizer.PetPanelOwner,
                        TTLocalizer.PetPanelOwner, ""),
                text_fg = text2Color,
                text_shadow = (0, 0, 0, 1),
                text_scale = TTLocalizer.PAPowner,
                text_pos = (0.3,1.05),
                text_align = TextNode.ACenter,
                command = self.__handleToOwner,
                )

        if self.avatar.getOwnerId() == base.localAvatar.doId:
            self.ownerButton['state'] = DGG.DISABLED

        toonGui = loader.loadModel("phase_3.5/models/gui/avatar_panel_gui")
        self.detailButton = DirectButton(
                parent = self.frame,
                image = (toonGui.find("**/ChtBx_BackBtn_UP"),
                         toonGui.find("**/ChtBx_BackBtn_DN"),
                         toonGui.find("**/ChtBx_BackBtn_Rllvr"),
                         toonGui.find("**/ChtBx_BackBtn_UP"),
                         ),
                relief = None,
                pos = (-1.3, 0, 0.67),
                image3_color = disabledImageColor,
                text = ("", TTLocalizer.PetPanelDetail,
                        TTLocalizer.PetPanelDetail, ""),
                text_fg = text2Color,
                text_shadow = (0, 0, 0, 1),
                text_scale = 0.05,
                text_pos = (0.05, 0.05),
                text_align = TextNode.ACenter,
                command = self.__handleDetail,
                )
        self.detailButton.setScale(7.5)
        
        if (not self.petIsLocal):
            self.detailButton['state'] = DGG.DISABLED 

        gui.removeNode()
        toonGui.removeNode()

        self.petDetailPanel = None
        
        self.__fillPetInfo(self.avatar)
        
        self.accept("petNameChanged", self.__refreshPetInfo)
        self.accept("petStateUpdated", self.__refreshPetInfo)
        
        self.frame.show()
 
        if self.petIsLocal:
            #if this pet is real, set up a task to check his proximity
            proxTask = Task.loop(Task(self.__checkPetProximity),
                                 Task.pause(0.5))
            taskMgr.add(proxTask, "petpanel-proximity-check",
                        priority=ToontownGlobals.PetPanelProximityPriority)

        if base.localAvatar.isLockedDown():
            self.disableInteractionButtons()

        if self.petIsLocal:
            self.listenForInteractionDone()

        messenger.send("petPanelDone")
        
        # refresh the pet info
        if ((not self.petIsLocal) and
            hasattr(self.avatar, 'updateMoodFromServer')):
            # can we use previously-cached mood info? Only do this for
            # localAv's pet. We can't reliably know if the mood of someone
            # else's pet has changed since we last queried their info...
            if (self.avatar.doId != localAvatar.getPetId() or
                bboard.get(PetConstants.OurPetsMoodChangedKey, False)):
                # clear out the state text, since it may be stale and we'll be
                # setting it to a correct string in a moment
                self.stateLabel['text'] = ''
                def refresh(self=self, av=self.avatar):
                    # clear the 'mood dirty' flag for localAv's pet
                    bboard.remove(PetConstants.OurPetsMoodChangedKey)
                    self.__refreshPetInfo(av)
                self.avatar.updateMoodFromServer(refresh)

    def __checkPetProximity(self, task=None):
        if self.petIsLocal:
            if base.localAvatar.isInWater():
                self.scratchButton['state'] = DGG.DISABLED
                self.feedButton['state'] = DGG.DISABLED
                self.callButton['state'] = DGG.DISABLED
                self.notify.debug("local avatar is in water")
            else:
                petPos = self.avatar.getPos()
                toonPos = base.localAvatar.getPos()

                diff = Vec3(petPos - toonPos)
                distance = diff.length()

                self.notify.debug("pet distance is %s" % distance)
                
                if distance > 20.0:
                    self.scratchButton['state'] = DGG.DISABLED
                    self.feedButton['state'] = DGG.DISABLED
                else:
                    # is the pet too high or low relative to us?
                    # this takes care of scratching the pet from a roof
                    # can still scratch a pet's privates
                    tooVert = abs(diff[2]) > 5.
                    if tooVert:
                        self.scratchButton['state'] = DGG.DISABLED
                    else:
                        self.scratchButton['state'] = DGG.NORMAL

                    self.feedButton['state'] = self.feedButtonState()
                self.callButton['state'] = DGG.NORMAL

        return Task.done

    def enableInteractionButtons(self):
        self.notify.debug("enable buttons")
        proxTask = Task.loop(Task(self.__checkPetProximity),
                             Task.pause(0.5))
        taskMgr.add(proxTask, "petpanel-proximity-check",
                    priority=ToontownGlobals.PetPanelProximityPriority)
        """
        if pet is out of range, this would flash feed/scratch for a frame
        after feeding or scratching
        self.scratchButton['state'] = DGG.NORMAL
        self.feedButton['state'] = self.feedButtonState()
        self.callButton['state'] = DGG.NORMAL
        """
        # instead, call this to set the button states
        self.__checkPetProximity()

    def disableInteractionButtons(self):
        self.notify.debug("disable buttons")
        taskMgr.remove("petpanel-proximity-check")
        self.scratchButton['state'] = DGG.DISABLED
        self.feedButton['state'] = DGG.DISABLED
        self.callButton['state'] = DGG.DISABLED

    def listenForInteractionDone(self):
        self.accept('pet-interaction-done', self.enableInteractionButtons)
    def cancelListenForInteractionDone(self):
        self.ignore('pet-interaction-done')

    def feedButtonState(self):
        if base.localAvatar.getMoney() >= PetConstants.FEED_AMOUNT:
            return DGG.NORMAL
        else:
            return DGG.DISABLED
    
    def cleanup(self):
        self.notify.debug("cleanup(): doId=%s" % self.avatar.doId)
        """cleanup(self)"""
        if (self.frame == None):
            return

        self.cancelListenForInteractionDone()

        taskMgr.remove("petpanel-proximity-check")
        
        if hasattr(self, "toonDetail"):
            del self.toonDetail
        
        self.frame.destroy()
        del self.frame
        self.frame = None

        self.petView.removeNode()
        del self.petView

        self.petModel.delete()
        del self.petModel

        base.localAvatar.obscureFriendsListButton(-1)

        self.ignore('petStateUpdated')
        self.ignore('petNameChanged')

        if self.avatar.bFake:
             self.avatar.disable()
             self.avatar.delete()

        AvatarPanel.AvatarPanel.cleanup(self)

        base.panel = None
        
        return

    def disableAll(self):
        self.disableInteractionButtons()
        self.ownerButton['state'] = DGG.DISABLED
        self.closeButton['state'] = DGG.DISABLED
        self.detailButton['state'] = DGG.DISABLED

    def __handleDetailDone(self):
        if self.petDetailPanel != None:
            self.petDetailPanel.cleanup()
            self.petDetailPanel = None
        self.detailButton['state'] = DGG.NORMAL

    def __handleDetail(self):
        self.petDetailPanel = PetDetailPanel.PetDetailPanel(
                                        pet = self.avatar,
                                        closeCallback = self.__handleDetailDone,
                                        parent = self.frame,
                                        )
        self.detailButton['state'] = DGG.DISABLED

    def __handleToOwner(self):
        self.notify.debug("__handleToOwner(): doId=%s" % self.avatar.doId)
        handle = base.cr.identifyFriend(self.avatar.ownerId)
        if handle != None:
            self.cleanup()
            messenger.send("clickedNametag", [handle])
        else:
            self.disableAll()
            from toontown.toon import ToonDetail
            self.toonDetail = ToonDetail.ToonDetail(self.avatar.ownerId, self.__ownerDetailsLoaded)
            
    def __ownerDetailsLoaded(self, avatar):
        self.notify.debug("__ownerDetailsLoaded(): doId=%s" % self.avatar.doId)
        self.cleanup()
        if avatar is not None:
            messenger.send("clickedNametag", [avatar])

    def __handleCall(self):
        self.notify.debug("__handleCall(): doId=%s" % self.avatar.doId)
        base.localAvatar.b_setPetMovie(self.avId, PetConstants.PET_MOVIE_CALL)
        base.panel.disableInteractionButtons()
        #self.listenForInteractionDone()
        # For precaution, in case a pet is doing a trick
        if self.avatar.trickIval is not None and self.avatar.trickIval.isPlaying():
            self.avatar.trickIval.finish()
        # Go into pet mode so we get out of walk mode
        base.cr.playGame.getPlace().setState('pet')        
        base.localAvatar.lock()

    def __handleFeed(self):
        self.notify.debug("__handleFeed(): doId=%s" % self.avatar.doId)
        base.localAvatar.b_setPetMovie(self.avId, PetConstants.PET_MOVIE_FEED)
        base.panel.disableInteractionButtons()
        #self.listenForInteractionDone()
        # For precaution, in case a pet is doing a trick
        if self.avatar.trickIval is not None and self.avatar.trickIval.isPlaying():
            self.avatar.trickIval.finish()
        # Go into pet mode so we get out of walk mode
        base.cr.playGame.getPlace().setState('pet')
        base.localAvatar.lock()
            
    def __handleScratch(self):
        self.notify.debug("__handleScratch(): doId=%s" % self.avatar.doId)
        base.localAvatar.b_setPetMovie(self.avId, PetConstants.PET_MOVIE_SCRATCH)
        base.panel.disableInteractionButtons()
        #self.listenForInteractionDone()
        # For precaution, in case a pet is doing a trick
        if self.avatar.trickIval is not None and self.avatar.trickIval.isPlaying():
            self.avatar.trickIval.finish()
        # Go into pet mode so we get out of walk mode
        base.cr.playGame.getPlace().setState('pet')        
        base.localAvatar.lock()
            
    def __handleDisableAvatar(self):
        self.notify.debug("__handleDisableAvatar(): doId=%s" % self.avatar.doId)
        """__handleDisableAvatar(self)

        Called whenever an avatar is disabled, this should cleanup the
        avatar panel if it's not a friend.

        """
        self.cleanup()
        AvatarPanel.currentAvatarPanel = None

    def __handleGenerateAvatar(self, avatar):
        return

    def __handleClose(self):
        self.notify.debug("__handleClose(): doId=%s" % self.avatar.doId)
        self.cleanup()
        AvatarPanel.currentAvatarPanel = None
        if self.friendsListShown:
            # Restore the friends list if it was up before.
            self.FriendsListPanel.showFriendsList()

    def __fillPetInfo(self, avatar):
        self.notify.debug("__fillPetInfo(): doId=%s" % avatar.doId)
        #add the view of the pet
        self.petView = self.frame.attachNewNode('petView')
        self.petView.setPos(0, 0, 5.4)
        self.petModel = Pet.Pet(forGui = 1)
        self.petModel.setDNA(avatar.getDNA())
        self.petModel.fitAndCenterHead(3.575, forGui = 1)
        self.petModel.reparentTo(self.petView)
        self.petModel.enterNeutralHappy()
        self.petModel.startBlink()
        
        # Put the avatar's name across the top.
        self.nameLabel = DirectLabel(
                parent = self.frame,
                pos = (0, 0, 5.2),
                relief = None,
                text = avatar.getName(),
                text_font = avatar.getFont(),
                text_fg = Vec4(0,0,0,1),
                text_pos = (0, 0),
                text_scale = 0.4,
                text_wordwrap = 7.5,
                text_shadow = (1, 1, 1, 1),
                )
                
        # Put the avatar's 'state' (biggest need)
        self.stateLabel = DirectLabel(
                parent = self.frame,
                pos = TTLocalizer.PAPstateLabelPos,
                relief = None,
                text = "",
                text_font = avatar.getFont(),
                text_fg = Vec4(0,0,0,1),
                text_scale = TTLocalizer.PAPstateLabel,
                text_wordwrap = TTLocalizer.PAPstateLabelwordwrap,
                text_shadow = (1, 1, 1, 1),
                )
        
        self.__refreshPetInfo(avatar)
        
    def __refreshPetInfo(self, avatar):
        self.notify.debug("__refreshPetInfo(): doId=%s" % avatar.doId)
        if avatar.doId != self.avatar.doId:
            self.notify.warning("avatar not self!") 
            return

        # Check to see if this panel has already been cleaned up
        if (self.frame == None):
            return

        if not self.petIsLocal:
            # Refresh the 'state' info
            self.avatar.updateOfflineMood()
        mood = self.avatar.getDominantMood()
        self.stateLabel['text'] = TTLocalizer.PetMoodAdjectives[mood]

        # Refresh the pets name
        self.nameLabel['text'] = avatar.getName()

        # Update the pets detail panel if it is open
        if self.petDetailPanel != None:
            self.petDetailPanel.update(avatar)
