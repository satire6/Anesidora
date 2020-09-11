from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import types
from toontown.toon import NPCToons
from toontown.toon import NPCFriendPanel
from toontown.toonbase import ToontownBattleGlobals

class TownBattleSOSPanel(DirectFrame, StateData.StateData):
    """TownBattleSOSPanel:

    This is the panel that lists all of our friends, or at least those
    who are currently online.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleSOSPanel')

    def __init__(self, doneEvent):
        """__init__(self, doneEvent)
        """
        
        DirectFrame.__init__(self, relief = None)
        self.initialiseoptions(TownBattleSOSPanel)
        StateData.StateData.__init__(self, doneEvent)
        # Friends maps (friendId, flags) pairs to the button in the scrollList
        self.friends = {}
        self.NPCFriends = {}
        self.textRolloverColor = Vec4(1,1,0,1)
        self.textDownColor = Vec4(0.5,0.9,1,1)
        self.textDisabledColor = Vec4(0.4,0.8,0.4,1)
        self.bldg = 0
        self.chosenNPCToons = []

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1

        # This is the dialog background.
        #bgd = loader.loadModel('phase_3/models/gui/dialog_box_gui')
        bgd = loader.loadModel('phase_3.5/models/gui/frame')

        # This has the up-and-down scroll buttons in it.
        gui = loader.loadModel("phase_3.5/models/gui/frame4names")

        # We need this for the scroll buttons
        scrollGui = loader.loadModel(
            "phase_3.5/models/gui/friendslist_gui")

        # We need this to get the "back" button.
        backGui = loader.loadModel("phase_3.5/models/gui/battle_gui")

        self['image'] = bgd
        self['image_pos'] = (0.0, 0.1, -0.08)
        self.setScale(0.3)

        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.TownBattleSOSNoFriends,
            text_scale = 0.4,
            text_fg = (1, 1, 1, 1),
            text_shadow = (0, 0, 0, 1),
            pos = (0.0, 0.0, 1.45),
            )

        self.NPCFriendPanel = NPCFriendPanel.NPCFriendPanel(
            parent = self, doneEvent = self.doneEvent)
        self.NPCFriendPanel.setPos(-0.75,0,-0.15)
        self.NPCFriendPanel.setScale(0.325)

        self.NPCFriendsLabel = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.TownBattleSOSNPCFriends,
            text_scale = 0.3,
            text_fg = (1, 1, 1, 1),
            text_shadow = (0, 0, 0, 1),
            pos = (-0.75, 0.0, -1.85),
            )

        self.scrollList = DirectScrolledList(
            parent = self,
            relief = None,
            image = gui.find("**/frame4names"),
            image_scale = (0.11,1,.1),
            text = TTLocalizer.FriendsListPanelOnlineFriends,
            text_scale = 0.04,
            text_pos = (-0.02,0.275),
            text_fg = (0,0,0,1),
            # inc and dec are DirectButtons
            incButton_image = (scrollGui.find("**/FndsLst_ScrollUp"),
                               scrollGui.find("**/FndsLst_ScrollDN"),
                               scrollGui.find("**/FndsLst_ScrollUp_Rllvr"),
                               scrollGui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_pos = (0.0, 0.0, -0.3),
            # Make the disabled button darker
            incButton_image3_color = Vec4(0.6, 0.6, 0.6, 0.6),
            incButton_scale = (1.0, 1.0, -1.0),
            decButton_image = (scrollGui.find("**/FndsLst_ScrollUp"),
                               scrollGui.find("**/FndsLst_ScrollDN"),
                               scrollGui.find("**/FndsLst_ScrollUp_Rllvr"),
                               scrollGui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_pos = (0.0, 0.0, 0.175),
            # Make the disabled button darker
            decButton_image3_color = Vec4(0.6, 0.6, 0.6, 0.6),
            # itemFrame is a DirectFrame
            itemFrame_pos = (-0.17, 0.0, 0.11),
            itemFrame_relief = None,
            # each item is a button with text on it
            numItemsVisible = 9,
            items = [],
            pos = (2.3, 0.0, 0.025),
            scale = 3.5,
            )

        # Set up a clipping plane to truncate names that would extend
        # off the right end of the scrolled list.
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.32, 0, 0)))
        clipNP = self.scrollList.component('itemFrame').attachNewNode(clipper)
        self.scrollList.component('itemFrame').setClipPlane(clipNP)

        self.close = DirectButton(
            parent = self,
            relief = None,
            image = (backGui.find("**/PckMn_BackBtn"),
                     backGui.find("**/PckMn_BackBtn_Dn"),
                     backGui.find("**/PckMn_BackBtn_Rlvr")),
            pos = (2.2, 0.0, -1.65),
            scale = 3,
            text = TTLocalizer.TownBattleSOSBack,
            text_scale = 0.05,
            text_pos = (0.01,-0.012),
            text_fg = Vec4(0,0,0.8,1),
            command = self.__close,
            )

        gui.removeNode()
        scrollGui.removeNode()
        backGui.removeNode()
        bgd.removeNode()

        self.hide()

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()

        del self.title
        del self.scrollList
        del self.close
        del self.friends
        del self.NPCFriends
        DirectFrame.destroy(self)

    def makeFriendButton(self, friendPair):
        friendId, flags = friendPair
        
        #handle = base.cr.identifyFriend(friendId)
        handle = base.cr.playerFriendsManager.identifyFriend(friendId)
        if handle == None:
            # If we don't know who this friend is, we can't make a
            # button.  We'll find out later; for now, leave it out.
            base.cr.fillUpFriendsMap()
            return None

        friendName = handle.getName()

        # On this panel, we display all names in black, regardless of
        # chat permission.
        fg = Vec4(0.0, 0.0, 0.0, 1.0)

        if handle.isPet():
            com = self.__chosePet
        else:
            com = self.__choseFriend
        
        return DirectButton(
            relief = None,
            text = friendName,
            text_scale = 0.04,
            text_align = TextNode.ALeft,
            text_fg = fg,
            text1_bg = self.textDownColor,
            text2_bg = self.textRolloverColor,
            text3_fg = self.textDisabledColor,
            command = com,
            extraArgs = [friendId, friendName],
            )

    def makeNPCFriendButton(self, NPCFriendId, numCalls):
        if (not TTLocalizer.NPCToonNames.has_key(NPCFriendId)):
            return None

        friendName = TTLocalizer.NPCToonNames[NPCFriendId]
        friendName += " %d" % numCalls

        # On this panel, we display all names in black, regardless of
        # chat permission.
        fg = Vec4(0.0, 0.0, 0.0, 1.0)
        
        return DirectButton(
            relief = None,
            text = friendName,
            text_scale = 0.04,
            text_align = TextNode.ALeft,
            text_fg = fg,
            text1_bg = self.textDownColor,
            text2_bg = self.textRolloverColor,
            text3_fg = self.textDisabledColor,
            command = self.__choseNPCFriend,
            extraArgs = [NPCFriendId],
            )

    def enter(self, canLure = 1, canTrap = 1):
        """enter(self)
        """
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        # Use isLoaded to avoid redundant loading
        if self.isLoaded == 0:
            self.load()
        self.canLure = canLure
        self.canTrap = canTrap

        self.factoryToonIdList = None

        # allow other parts of the system to make modifications
        messenger.send('SOSPanelEnter', [self])

        self.__updateScrollList()
        self.__updateNPCFriendsPanel()
        self.__updateTitleText()
        self.show()
        
        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendOffline', self.__friendOffline)
        self.accept('friendsListChanged', self.__friendsListChanged)
        self.accept('friendsMapComplete', self.__friendsListChanged)

    def exit(self):
        """exit(self)
        """
        if self.isEntered == 0:
            return None
        self.isEntered = 0

        self.hide()

        self.ignore('friendOnline')
        self.ignore('friendOffline')
        self.ignore('friendsListChanged')
        self.ignore('friendsMapComplete')

        messenger.send(self.doneEvent)

    def __close(self):
        doneStatus = {}
        doneStatus['mode'] = 'Back'
        messenger.send(self.doneEvent, [doneStatus])

    def __choseFriend(self, friendId, friendName):
        doneStatus = {}
        doneStatus['mode'] = 'Friend'
        doneStatus['friend'] = friendId
        messenger.send(self.doneEvent, [doneStatus])

    def __chosePet(self, petId, petName):
        doneStatus = {}
        doneStatus['mode'] = 'Pet'
        doneStatus['petId'] = petId
        doneStatus['petName'] = petName
        messenger.send(self.doneEvent, [doneStatus])

    def __choseNPCFriend(self, friendId):
        doneStatus = {}
        doneStatus['mode'] = 'NPCFriend'
        doneStatus['friend'] = friendId
        self.chosenNPCToons.append(friendId)
        messenger.send(self.doneEvent, [doneStatus])

    def setFactoryToonIdList(self, toonIdList):
        # this list acts as a sort of 'mask' for online friends;
        # only friends in this list should show up in the SOS panel
        self.factoryToonIdList = toonIdList[:]

    def __updateScrollList(self):

        # Make a list of just those who are actually online.
        # newFriends is a list of 2-item tuples (friendId, flags)
        newFriends = []

        battlePets = base.config.GetBool('want-pets-in-battle', 1)

        if base.wantPets and battlePets == 1 and base.localAvatar.hasPet():
            newFriends.append((base.localAvatar.getPetId(), 0))
        
        # Only NPC friends should be visible inside buildings
        # in factories, we should show friends that are with us in the factory
        if (not self.bldg) or (self.factoryToonIdList is not None):
            for friendPair in base.localAvatar.friendsList:
                if base.cr.isFriendOnline(friendPair[0]):
                    if ((self.factoryToonIdList is None) or
                        (friendPair[0] in self.factoryToonIdList)):
                        newFriends.append(friendPair)
                        
            if hasattr(base.cr, "playerFriendsManager"):
                for avatarId in base.cr.playerFriendsManager.getAllOnlinePlayerAvatars():
                    if not base.cr.playerFriendsManager.askAvatarKnownElseWhere(avatarId):
                        newFriends.append((avatarId, 0))

        
        # Remove old buttons
        for friendPair in self.friends.keys():
            if friendPair not in newFriends:
                friendButton = self.friends[friendPair]
                self.scrollList.removeItem(friendButton)
                if (not friendButton.isEmpty()):
                    friendButton.destroy()
                del self.friends[friendPair]

        # Add buttons for new friends
        for friendPair in newFriends:
            if not self.friends.has_key(friendPair):
                friendButton = self.makeFriendButton(friendPair)
                if friendButton:
                    self.scrollList.addItem(friendButton)
                    self.friends[friendPair] = friendButton
                    



    def __updateNPCFriendsPanel(self):
        # Make a dict of the NPC Toons that are callable at this time
        self.NPCFriends = {}
        
        # Determine if any should be disabled because their
        # attacks won't work (e.g. all the cogs are already lured)
        for friend, count in base.localAvatar.NPCFriendsDict.items():
            track = NPCToons.getNPCTrack(friend)
            if ((track == ToontownBattleGlobals.LURE_TRACK and
                 self.canLure == 0) or 
                (track == ToontownBattleGlobals.TRAP_TRACK and
                 self.canTrap == 0)):
                self.NPCFriends[friend] = 0
            else:
                self.NPCFriends[friend] = count

        self.NPCFriendPanel.update(self.NPCFriends, fCallable = 1)

    def __updateTitleText(self):
        # Change the top text according to whether anyone's
        # available.
        isEmpty = (len(self.friends) == 0) and (len(self.NPCFriends) == 0)
        if isEmpty:
            self.title['text'] = TTLocalizer.TownBattleSOSNoFriends
        else:
            self.title['text'] = TTLocalizer.TownBattleSOSWhichFriend


    def __friendOnline(self, doId, commonChatFlags, whitelistChatFlags):
        """__friendOnline(self, int doId):

        Called when a friend comes online, this should update the
        friends list appropriately.
        """
        self.__updateScrollList()
        self.__updateTitleText()
        
    def __friendOffline(self, doId):
        """__friendOffline(self, int doId):

        Called when a friend goes offline, this should update the
        friends list appropriately.
        """
        self.__updateScrollList()
        self.__updateTitleText()
        
    def __friendsListChanged(self):
        """__friendsListChanged(self):

        Called when the friends list changes (by adding or removing a
        friend), this should update the friends list appropriately.
        """
        self.__updateScrollList()
        self.__updateTitleText()
        
