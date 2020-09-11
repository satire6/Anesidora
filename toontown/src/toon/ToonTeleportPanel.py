from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import ToonAvatarDetailPanel
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil

globalTeleport = None

def showTeleportPanel(avId, avName, avDisableName):
    # A module function to open the global avatar detail panel.
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None
        
    globalTeleport = ToonTeleportPanel(avId, avName, avDisableName)

def hideTeleportPanel():
    # A module function to close the global avatar detail if it is open.
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None

def unloadTeleportPanel():
    # A module function to completely unload the global friend
    # inviter.  This is the same thing as hideTeleportPanel, actually.
    global globalTeleport
    if globalTeleport != None:
        globalTeleport.cleanup()
        globalTeleport = None

class ToonTeleportPanel(DirectFrame):
    """ToonTeleportPanel:

    This panel pops up in response to clicking the "Go To" button from
    the Avatar panel.  It handles determining where the avatar is and
    teleporting to him/her, if possible.

    """

    notify = DirectNotifyGlobal.directNotify.newCategory("ToonTeleportPanel")

    def __init__(self, avId, avName, avDisableName):

        # initialize our base class.
        DirectFrame.__init__(self,
                             pos = (0.3, 0.1, 0.65),
                             image_color = ToontownGlobals.GlobalDialogColor,
                             image_scale = (1.0, 1.0, 0.6),
                             text = '',
                             text_wordwrap = 13.5,
                             text_scale = 0.06,
                             text_pos = (0.0, 0.18), 
                             )

        # If we're currently in move-furniture mode, stop it.
        messenger.send("releaseDirector")

        # For some reason, we need to set this after construction to
        # get it to work properly.
        self['image'] = DGG.getDefaultDialogGeom()

        self.avId = avId
        self.avName = avName
        self.avDisableName = avDisableName

        self.fsm = ClassicFSM.ClassicFSM('ToonTeleportPanel',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff),
                            State.State('begin',
                                        self.enterBegin,
                                        self.exitBegin),
                            State.State('checkAvailability',
                                        self.enterCheckAvailability,
                                        self.exitCheckAvailability),
                            State.State('notAvailable',
                                        self.enterNotAvailable,
                                        self.exitNotAvailable),
                            State.State('ignored',
                                        self.enterIgnored,
                                        self.exitIgnored),
                            State.State('notOnline',
                                        self.enterNotOnline,
                                        self.exitNotOnline),
                            State.State('wentAway',
                                        self.enterWentAway,
                                        self.exitWentAway),
                            State.State('self',
                                        self.enterSelf,
                                        self.exitSelf),
                            State.State('unknownHood',
                                        self.enterUnknownHood,
                                        self.exitUnknownHood),
                            State.State('unavailableHood',
                                        self.enterUnavailableHood,
                                        self.exitUnavailableHood),
                            State.State('otherShard',
                                        self.enterOtherShard,
                                        self.exitOtherShard),
                            State.State('teleport',
                                        self.enterTeleport,
                                        self.exitTeleport),
                            ],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )


        # This is imported here instead of at the top of the file to
        # protect against circular imports.
        from toontown.friends import FriendInviter

        # Now set up the panel.
        FriendInviter.hideFriendInviter()
        ToonAvatarDetailPanel.hideAvatarDetail()

        # Create some buttons.
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')

        self.bOk = DirectButton(self,
                                image = (buttons.find('**/ChtBx_OKBtn_UP'),
                                         buttons.find('**/ChtBx_OKBtn_DN'),
                                         buttons.find('**/ChtBx_OKBtn_Rllvr')),
                                relief = None,
                                text = TTLocalizer.TeleportPanelOK,
                                text_scale = 0.05,
                                text_pos = (0.0, -0.1),
                                pos = (0.0, 0.0, -0.1),
                                command = self.__handleOk)
        self.bOk.hide()

        self.bCancel = DirectButton(self,
                                    image = (buttons.find('**/CloseBtn_UP'),
                                             buttons.find('**/CloseBtn_DN'),
                                             buttons.find('**/CloseBtn_Rllvr')),
                                    relief = None,
                                    text = TTLocalizer.TeleportPanelCancel,
                                    text_scale = 0.05,
                                    text_pos = (0.0, -0.1),
                                    pos = (0.0, 0.0, -0.1),
                                    command = self.__handleCancel)
        self.bCancel.hide()

        self.bYes = DirectButton(self,
                                 image = (buttons.find('**/ChtBx_OKBtn_UP'),
                                          buttons.find('**/ChtBx_OKBtn_DN'),
                                          buttons.find('**/ChtBx_OKBtn_Rllvr')),
                                 relief = None,
                                 text = TTLocalizer.TeleportPanelYes,
                                 text_scale = 0.05,
                                 text_pos = (0.0, -0.1),
                                 pos = (-0.15, 0.0, -0.15),
                                 command = self.__handleYes)
        self.bYes.hide()

        self.bNo = DirectButton(self,
                                image = (buttons.find('**/CloseBtn_UP'),
                                         buttons.find('**/CloseBtn_DN'),
                                         buttons.find('**/CloseBtn_Rllvr')),
                                relief = None,
                                text = TTLocalizer.TeleportPanelNo,
                                text_scale = 0.05,
                                text_pos = (0.0, -0.1),
                                pos = (0.15, 0.0, -0.15),
                                command = self.__handleNo)
        self.bNo.hide()

        buttons.removeNode()

        self.accept(self.avDisableName, self.__handleDisableAvatar)

        self.show()
        self.fsm.enterInitialState()
        self.fsm.request('begin')


    def cleanup(self):
        """cleanup(self):

        Cancels any pending request and removes the panel from the
        screen.
        
        """
        self.fsm.request('off')
        del self.fsm
        self.ignore(self.avDisableName)
        self.destroy()

    ##### Off state #####

    # Represents the initial state of the teleport query: no query in
    # progress.
    
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    ##### Begin state #####

    # We have clicked on the "go to" button from the Avatar detail
    # panel.  Perform a few sanity checks.
    
    def enterBegin(self):
        myId = base.localAvatar.doId
        hasManager = hasattr(base.cr, "playerFriendsManager")

        if (self.avId == myId):
            self.fsm.request('self')

        elif base.cr.doId2do.has_key(self.avId):
            # The avatar is online, and in fact, nearby.
            self.fsm.request('checkAvailability')

        elif base.cr.isFriend(self.avId):
            # The avatar is a friend of ours.  Is she online?
            if base.cr.isFriendOnline(self.avId):
                self.fsm.request('checkAvailability')
            else:
                self.fsm.request('notOnline')
                
        elif hasManager and base.cr.playerFriendsManager.getAvHandleFromId(self.avId):
            # The avatar is a transient friend of ours.  Is she online?
            id = base.cr.playerFriendsManager.findPlayerIdFromAvId(self.avId)
            info = base.cr.playerFriendsManager.getFriendInfo(id)
            if info:
                if info.onlineYesNo:
                    self.fsm.request('checkAvailability')
                else:
                    self.fsm.request('notOnline')
            else:
                self.fsm.request('wentAway')
            
        else:
            # The avatar is not our friend and isn't around.
            self.fsm.request('wentAway')

    def exitBegin(self):
        pass
        
    ##### Checking availability state #####

    # Ask the other avatar if he's available to be teleported to, and
    # where is he.

    def enterCheckAvailability(self):

        myId = base.localAvatar.getDoId()
        base.localAvatar.d_teleportQuery(myId, sendToId = self.avId)
        self['text'] = TTLocalizer.TeleportPanelCheckAvailability % (self.avName)
        self.accept('teleportResponse', self.__teleportResponse)
        self.bCancel.show()

    def exitCheckAvailability(self):
        self.ignore('teleportResponse')
        self.bCancel.hide()

    ##### Not available state #####

    # In this state, the avatar we have tried to teleport to is
    # currently not available to answer that query: maybe he's in a
    # minigame or something.

    def enterNotAvailable(self):
        self['text'] = TTLocalizer.TeleportPanelNotAvailable  % (self.avName)
        self.bOk.show()

    def exitNotAvailable(self):
        self.bOk.hide()

    ##### Ignored state #####

    # In this state, the avatar we have tried to teleport to is
    # ignoring us.  Too bad for us.

    def enterIgnored(self):
        self['text'] = TTLocalizer.TeleportPanelNotAvailable  % (self.avName)
        self.bOk.show()

    def exitIgnored(self):
        self.bOk.hide()

    ##### Not online state #####

    # In this state, the avatar is not even online.

    def enterNotOnline(self):
        self['text'] = TTLocalizer.TeleportPanelNotOnline % (self.avName)
        self.bOk.show()

    def exitNotOnline(self):
        self.bOk.hide()

    ##### Went away state #####

    # The avatar was here, but now he's gone.

    def enterWentAway(self):
        self['text'] = TTLocalizer.TeleportPanelWentAway % (self.avName)
        self.bOk.show()

    def exitWentAway(self):
        self.bOk.hide()

    ##### UnknownHood state #####

    # Invalid attempt to teleport to a hood we haven't been to yet.

    def enterUnknownHood(self, hoodId):
        self['text'] = TTLocalizer.TeleportPanelUnknownHood % \
                       base.cr.hoodMgr.getFullnameFromId(hoodId)
        self.bOk.show()

    def exitUnknownHood(self):
        self.bOk.hide()

    ##### UnavailableHood state #####

    # Invalid attempt to teleport to a hood we haven't downloaded yet.

    def enterUnavailableHood(self, hoodId):
        self['text'] = (TTLocalizer.TeleportPanelUnavailableHood % 
                        base.cr.hoodMgr.getFullnameFromId(hoodId))
        self.bOk.show()

    def exitUnavailableHood(self):
        self.bOk.hide()

    ##### Self state #####

    # Invalid attempt to teleport to yourself.

    def enterSelf(self):
        self['text'] = TTLocalizer.TeleportPanelDenySelf
        self.bOk.show()

    def exitSelf(self):
        self.bOk.hide()


    ##### OtherShard state #####

    # Warn the user that we're about to switch shards, and give
    # him/her an opportunity to bail.

    def enterOtherShard(self, shardId, hoodId, zoneId):
        shardName = base.cr.getShardName(shardId)
        if shardName is None:
            # unknown shard. potentially a hacker--just ignore
            self.fsm.request('notAvailable')
            return
        myShardName = base.cr.getShardName(base.localAvatar.defaultShard)

        # determine the population of new shard
        pop = None
        for shard in base.cr.listActiveShards():
            if shard[0] == shardId:
                pop = shard[2]
 
        # if we got a pop for the shard in question and it's full
        if pop and pop > localAvatar.shardPage.midPop:
            self.notify.warning("Entering full shard: issuing performance warning")
            self['text'] = (TTLocalizer.TeleportPanelBusyShard %
                            ({"avName" : self.avName}))
        else:
            self['text'] = (TTLocalizer.TeleportPanelOtherShard %
                            ({"avName" : self.avName,
                              "shardName" : shardName,
                              "myShardName" : myShardName,
                              }))
        self.bYes.show()
        self.bNo.show()

        # Save the parameter variables for when we click "yes".
        self.shardId = shardId
        self.hoodId = hoodId
        self.zoneId = zoneId

    def exitOtherShard(self):
        self.bYes.hide()
        self.bNo.hide()

    ##### Teleport state #####

    # Actually perform the teleport operation.

    def enterTeleport(self, shardId, hoodId, zoneId):
        hoodsVisited = base.localAvatar.hoodsVisited

        canonicalHoodId = ZoneUtil.getCanonicalZoneId(hoodId)

        if hoodId == ToontownGlobals.MyEstate:
            if shardId == base.localAvatar.defaultShard:
                # If we're staying on the same shard, don't make the
                # shardId part of the request.
                shardId = None
            place = base.cr.playGame.getPlace()
            place.requestTeleport(hoodId, zoneId, shardId, self.avId)
            unloadTeleportPanel()

        elif canonicalHoodId not in (hoodsVisited + ToontownGlobals.HoodsAlwaysVisited):
            # We've never been to this hood before, so we can't go
            # there now.
            self.fsm.request('unknownHood', [hoodId])

        elif canonicalHoodId not in base.cr.hoodMgr.getAvailableZones():
            print "hoodId %d not ready" % hoodId
            # We haven't finished downloading this hood yet.
            self.fsm.request('unavailableHood', [hoodId])

        else:
            # All right already, just go there.
            if shardId == base.localAvatar.defaultShard:
                # If we're staying on the same shard, don't make the
                # shardId part of the request.
                shardId = None

            # All right already, just go there.
            place = base.cr.playGame.getPlace()
            place.requestTeleport(hoodId, zoneId, shardId, self.avId)
            unloadTeleportPanel()
            
        return

    def exitTeleport(self):
        pass


    ### Button handing methods

    def __handleOk(self):
        unloadTeleportPanel()

    def __handleCancel(self):
        unloadTeleportPanel()

    def __handleYes(self):
        self.fsm.request('teleport', [self.shardId, self.hoodId,
                                      self.zoneId])

    def __handleNo(self):
        unloadTeleportPanel()


    ### Support methods

    def __teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        if avId != self.avId:
            # Ignore responses from an unexpected avatar.
            return
        
        if available == 0:
            # The other avatar is not available to teleport to.
            self.fsm.request('notAvailable')
        elif available == 2:
            # The other avatar is ignoring us.
            self.fsm.request('ignored')
        elif shardId != base.localAvatar.defaultShard:
            self.fsm.request('otherShard', [shardId, hoodId, zoneId])
        else:
            self.fsm.request('teleport', [shardId, hoodId, zoneId])
        

    def __handleDisableAvatar(self):
        """__handleDisableAvatar(self)

        Called whenever the avatar in question is disabled, this
        should update the panel appropriately.

        """
        self.fsm.request('wentAway')
