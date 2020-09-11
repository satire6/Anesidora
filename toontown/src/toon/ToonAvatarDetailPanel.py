from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import DistributedToon
from toontown.friends import FriendInviter
import ToonTeleportPanel
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
from toontown.toonbase.ToontownBattleGlobals import Tracks, Levels

globalAvatarDetail = None

def showAvatarDetail(avId, avName, playerId = None):
    # A module function to open the global avatar detail panel.
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None
        
 
    playerId = base.cr.playerFriendsManager.findPlayerIdFromAvId(avId)
        
    globalAvatarDetail = ToonAvatarDetailPanel(avId, avName, playerId)

def hideAvatarDetail():
    # A module function to close the global avatar detail if it is open.
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None

def unloadAvatarDetail():
    # A module function to completely unload the global friend
    # inviter.  This is the same thing as hideAvatarDetail, actually.
    global globalAvatarDetail
    if globalAvatarDetail != None:
        globalAvatarDetail.cleanup()
        globalAvatarDetail = None

class ToonAvatarDetailPanel(DirectFrame):
    """
    This is a panel that pops up in response to clicking the "Details"
    button on the AvatarPanel.  It displays more details about the
    particular avatar.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("ToonAvatarDetailPanel")

    def __init__(self, avId, avName,  playerId = None, parent = aspect2dp, **kw):
        # Inherits from DirectFrame
        # Must specify avId and avName on creation
        print("ToonAvatarDetailPanel %s" % (playerId))
        
        # Load required models
        buttons = loader.loadModel(
            'phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        detailPanel = gui.find('**/avatarInfoPanel')
        self.playerId = playerId
        textScale = 0.095
        textWrap = 16.4
        self.playerInfo = None
        if self.playerId:
           #textScale = 0.100
           #textWrap = 18.0
           #self.isPlayer = 1
           self.playerInfo = base.cr.playerFriendsManager.playerId2Info.get(playerId)
        # Specify default options
        optiondefs = (
            ('pos',           (0.525, 0.0, 0.525),   None),
            ('scale',         0.5,                None),
            ('relief',        None,               None),
            ('image',         detailPanel,        None),
            ('image_color',   GlobalDialogColor,  None),
            ('text',          '',                 None),
            ('text_wordwrap', textWrap,               None),
            ('text_scale',    textScale,              None),
            ('text_pos',      (-0.125, 0.775),        None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # initialize our base class.
        DirectFrame.__init__(self, parent)

        # Information about avatar
        self.dataText = DirectLabel(self,
                                    text = '',
                                    text_scale = 0.09,
                                    text_align = TextNode.ALeft,
                                    text_wordwrap = 15,
                                    relief = None,
                                    pos = (-0.85, 0.0, 0.645),
                                    )

        self.avId = avId
        self.avName = avName
        self.avatar = None
        self.createdAvatar = None

        self.fsm = ClassicFSM.ClassicFSM('ToonAvatarDetailPanel',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['begin']),
                            State.State('begin',
                                        self.enterBegin,
                                        self.exitBegin,
                                        ['query', 'data', 'off']),
                            State.State('query',
                                        self.enterQuery,
                                        self.exitQuery,
                                        ['data', 'invalid', 'off']),
                            State.State('data',
                                        self.enterData,
                                        self.exitData,
                                        ['off']),
                            State.State('invalid',
                                        self.enterInvalid,
                                        self.exitInvalid,
                                        ['off'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )

        ToonTeleportPanel.hideTeleportPanel()
        FriendInviter.hideFriendInviter()

        # Create some buttons.
        self.bCancel = DirectButton(
            self,
            image = (buttons.find('**/CloseBtn_UP'),
                     buttons.find('**/CloseBtn_DN'),
                     buttons.find('**/CloseBtn_Rllvr')),
            image_scale = 1.1,
            relief = None,
            text = TTLocalizer.AvatarDetailPanelCancel,
            text_scale = TTLocalizer.TADPcancelButton,
            text_pos = (0.12, -0.01),
            pos = TTLocalizer.TADPcancelPos,
            scale = 2.0,
            command = self.__handleCancel)
        self.bCancel.hide()

        # Call option initialization functions
        self.initialiseoptions(ToonAvatarDetailPanel)

        # Initialize ClassicFSM
        self.fsm.enterInitialState()
        self.fsm.request('begin')

        # Clean up
        buttons.removeNode()
        gui.removeNode()

    def cleanup(self):
        """cleanup(self):

        Cancels any pending request and removes the panel from the
        screen.
        
        """
        if self.fsm:
            self.fsm.request('off')
            self.fsm = None
            # Remove any pending detail requests
            base.cr.cancelAvatarDetailsRequest(self.avatar)
        if self.createdAvatar:
            self.avatar.delete()
            self.createdAvatar = None

        self.destroy()

    ##### Off state #####

    # Represents the initial state of the detail query: no query in
    # progress.
    
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ##### Begin state #####

    # We have clicked on the "details" button from the Avatar panel.
    # Start the ball rolling.
    
    def enterBegin(self):
        myId = base.localAvatar.doId

        # Update name label
        self['text'] = self.avName

        if (self.avId == myId):
            self.avatar = base.localAvatar
            self.createdAvatar = 0
            self.fsm.request('data')
        else:
            self.fsm.request('query')

    def exitBegin(self):
        pass

    ##### Query state #####

    # We are waiting for detailed information on the avatar to return
    # from the server.
    
    def enterQuery(self):
        self.dataText['text'] = (
            TTLocalizer.AvatarDetailPanelLookup % (self.avName))
        self.bCancel.show()

        # We need to get a DistributedObject handle for the indicated
        # avatar.  Maybe we have one already, if the avatar is
        # somewhere nearby.
        self.avatar = base.cr.doId2do.get(self.avId)
        if self.avatar != None and not self.avatar.ghostMode:
            self.createdAvatar = 0
        else:
            # Otherwise, we have to make one up just to hold the
            # detail query response.  This is less than stellar,
            # because it means we'll do a lot of extra work we don't
            # need (like loading up models and binding animations,
            # etc.), but it's not *too* horrible.
            self.avatar = DistributedToon.DistributedToon(base.cr)
            self.createdAvatar = 1
            self.avatar.doId = self.avId
            # getAvatarDetails puts a DelayDelete on the avatar, and this
            # is not a real DO, so bypass the 'generated' check
            self.avatar.forceAllowDelayDelete()
 
        # Now ask the server to tell us more about this avatar.
        base.cr.getAvatarDetails(self.avatar, self.__handleAvatarDetails, "DistributedToon")
        
    def exitQuery(self):
        self.bCancel.hide()
        
    ##### Data state #####

    # We have detailed information now available in self.avatar.

    def enterData(self):
        self.bCancel['text'] = TTLocalizer.AvatarDetailPanelClose
        self.bCancel.show()
        self.__showData()
    
    def exitData(self):
        self.bCancel.hide()
        
    ##### Invalid state #####

    # For some reason, the server was unable to return data on the
    # avatar in question.

    def enterInvalid(self):
        self.dataText['text'] = (
            TTLocalizer.AvatarDetailPanelFailedLookup % (self.avName))
    
    def exitInvalid(self):
        self.bCancel.hide()

    ### Button handing methods
    def __handleCancel(self):
        unloadAvatarDetail()


    ### Support methods

    def __handleAvatarDetails(self, gotData, avatar, dclass):
        if ((not self.fsm) or (avatar != self.avatar)):
            # This may be a query response coming back from a previous
            # request.  Ignore it.
            self.notify.warning("Ignoring unexpected request for avatar %s" % (avatar.doId))
            return
            
        if gotData:
            # We got a valid response.
            self.fsm.request('data')
        else:
            # No information available about the avatar.  This is an
            # unexpected error condition, but we go out of our way to
            # handle it gracefully.
            self.fsm.request('invalid')

    def __showData(self):
        av = self.avatar
        online = 1
        if base.cr.isFriend(self.avId):
            online = base.cr.isFriendOnline(self.avId)
            
        if online:
            shardName = base.cr.getShardName(av.defaultShard)
            hoodName = base.cr.hoodMgr.getFullnameFromId(av.lastHood)
            if ZoneUtil.isWelcomeValley(av.lastHood):
                shardName = "%s (%s)" % (TTLocalizer.WelcomeValley[-1], shardName)
            if self.playerInfo:
                guiButton = loader.loadModel("phase_3/models/gui/quit_button")
                self.gotoAvatarButton = DirectButton(
                        parent = self,
                        relief = None,
                        image = (guiButton.find("**/QuitBtn_UP"),
                                 guiButton.find("**/QuitBtn_DN"),
                                 guiButton.find("**/QuitBtn_RLVR"),
                                 ),
                        image_scale = 1.1,
                        text = TTLocalizer.AvatarShowPlayer,
                        text_scale = 0.07,
                        text_pos = (0.0, -0.02),
                        textMayChange = 0,
                        pos = (0.44, 0, 0.41),
                        command = self.__showAvatar,
                        )
                
                text = (TTLocalizer.AvatarDetailPanelOnlinePlayer %
                    {"district": shardName, "location": hoodName, "player" : self.playerInfo.playerName})
            else:
                text = (TTLocalizer.AvatarDetailPanelOnline %
                    {"district": shardName, "location": hoodName})
                
        else:
            text = TTLocalizer.AvatarDetailPanelOffline
        self.dataText['text'] = text

        self.__updateTrackInfo()
        self.__updateTrophyInfo()
        self.__updateLaffInfo()
        
    def __showAvatar(self):
        messenger.send('wakeup')
        # Picking a friend from your friends list has exactly the same
        # effect as clicking on his or her name in the world.
        hasManager = hasattr(base.cr, "playerFriendsManager")
        handle = base.cr.identifyFriend(self.avId)
        if not handle and hasManager:
            handle = base.cr.playerFriendsManager.getAvHandleFromId(self.avId)
        if handle != None:
            self.notify.info("Clicked on name in friend's list. doId = %s" % handle.doId)
            messenger.send("clickedNametagPlayer", [handle, self.playerId, 1])

    def __updateLaffInfo(self):
        # Send a message to force the avatar panel to display the laff meter
        avatar = self.avatar
        messenger.send('updateLaffMeter', 
                       [avatar, avatar.hp, avatar.maxHp])

    def __updateTrackInfo(self):
        xOffset = -0.501814
        xSpacing = 0.1835
        yOffset =  0.1
        ySpacing = -0.115
        inventory =  self.avatar.inventory
        inventoryModels = loader.loadModel(
            "phase_3.5/models/gui/inventory_gui")
        buttonModel = inventoryModels.find("**/InventoryButtonUp")
        for track in range(0, len(Tracks)):
            # Track Label
            DirectLabel(parent = self,
                        relief = None, 
                        text = TextEncoder.upper(TTLocalizer.BattleGlobalTracks[track]),
                        text_scale = TTLocalizer.TADPtrackLabel,
                        text_align = TextNode.ALeft,
                        pos = (-0.90, 0, TTLocalizer.TADtrackLabelPosZ + track * ySpacing)
                        )
            # Fill in track if avatar has access
            if self.avatar.hasTrackAccess(track):
                curExp, nextExp = inventory.getCurAndNextExpValues(track)
                for item in range(0, len(Levels[track])):
                    level = Levels[track][item]
                    if curExp >= level:
                        numItems = inventory.numItem(track,item)
                        if numItems == 0:
                            image_color = Vec4(0.5,0.5,0.5,1)
                            geom_color = Vec4(0.2,0.2,0.2,0.5)
                        else:
                            image_color = Vec4(0,0.6,1,1)
                            geom_color = None
                        DirectLabel(
                            parent = self,
                            image = buttonModel,
                            image_scale = (0.92,1,1),
                            image_color = image_color,
                            geom = inventory.invModels[track][item],
                            geom_color = geom_color,
                            geom_scale = 0.6,
                            relief = None,
                            pos = (xOffset + item * xSpacing,
                                   0,
                                   yOffset + track * ySpacing),
                            )
                    else:
                        break

    def __updateTrophyInfo(self):
        # For now we don't know how many buildings a created avatar has
        if self.createdAvatar:
            return
        if (self.avatar.trophyScore >= TrophyStarLevels[2]):
            # A gold star!
            color = TrophyStarColors[2]
        elif self.avatar.trophyScore >= TrophyStarLevels[1]:
            # A silver star!
            color = TrophyStarColors[1]
        elif self.avatar.trophyScore >= TrophyStarLevels[0]:
            # A bronze star.
            color = TrophyStarColors[0]
        else:
            color = None

        if color:
            gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
            star = gui.find('**/avatarStar')
            self.star = DirectLabel(
                parent = self,
                image = star,
                image_color = color,
                pos = (0.610165, 0, -0.760678),
                scale = 0.9,
                relief = None)
            gui.removeNode()
                
