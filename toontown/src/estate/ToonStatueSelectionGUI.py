from toontown.estate import PlantingGUI
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.estate import GardenGlobals
from toontown.estate import DistributedToonStatuary
from direct.interval.IntervalGlobal import *
from direct.gui.DirectScrolledList import *
from toontown.toon import Toon
from toontown.toon import DistributedToon
from direct.distributed import DistributedObject

class ToonStatueSelectionGUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonStatueSelectionGUI')
    def __init__(self, doneEvent, specialBoxActive = False):
        base.tssGUI = self
        instructions = TTLocalizer.GardeningChooseToonStatue
        instructionsPos = (0, 0.4)
        DirectFrame.__init__(self,
                             relief = None,
                             state = 'normal',
                             geom = DGG.getDefaultDialogGeom(),
                             geom_color = ToontownGlobals.GlobalDialogColor,
                             #geom_scale = (2.0,1,1.5),
                             geom_scale = (1.5,1.0,1.0),
                             frameSize = (-1,1,-1,1),
                             pos = (0,0,0),
                             text = instructions,
                             text_wordwrap = 18,
                             text_scale = .08,
                             text_pos = instructionsPos,
                             )
        self.initialiseoptions(ToonStatueSelectionGUI)

        # Send this when we are done so whoever made us can get a callback
        self.doneEvent = doneEvent

        # Init buttons
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okImageList = (buttons.find('**/ChtBx_OKBtn_UP'),
                       buttons.find('**/ChtBx_OKBtn_DN'),
                       buttons.find('**/ChtBx_OKBtn_Rllvr'))
        cancelImageList = (buttons.find('**/CloseBtn_UP'),
                           buttons.find('**/CloseBtn_DN'),
                           buttons.find('**/CloseBtn_Rllvr'))
        self.cancelButton = DirectButton(
            parent = self,
            relief = None,
            image = cancelImageList,
            #pos = (0.3, 0, -0.58),
            pos = (-0.3, 0, -0.35),
            text = TTLocalizer.PlantingGuiCancel,
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__cancel,
            )
        self.okButton = DirectButton(
            parent = self,
            relief = None,
            image = okImageList,
            #pos = (0.6, 0, -0.58),
            pos = (0.3, 0, -0.35),
            text = TTLocalizer.PlantingGuiOk,
            text_scale = 0.06,
            text_pos = (0,-0.1),
            command = self.__accept,
            )
        buttons.removeNode()

        self.ffList = []
        self.friends = {}
        self.doId2Dna = {}
        self.textRolloverColor = Vec4(1,1,0,1)
        self.textDownColor = Vec4(0.5,0.9,1,1)
        self.textDisabledColor = Vec4(0.4,0.8,0.4,1)

        self.createFriendsList()

    def destroy(self):
        self.doneEvent = None
        self.previewToon.delete()
        self.previewToon = None
        
        # Destroying the buttons for every name.
        for ff in self.ffList:
            self.friends[ff].destroy()
        self.ffList = []
        self.friends = {}
        self.doId2Dna = {}

        self.scrollList.destroy()
        DirectFrame.destroy(self)

    def __cancel(self):
        assert(self.notify.debug("transaction cancelled"))
        messenger.send(self.doneEvent, [0,"",-1])
        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')

    def __accept(self):
        messenger.send(self.doneEvent, [1, "", DistributedToonStatuary.dnaCodeFromToonDNA(self.dnaSelected)])
        #if we're clicking on buttons, we're not asleep
        messenger.send('wakeup')

    def createFriendsList(self):
        self.__makeFFlist()

        if len(self.ffList) > 0:
            gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
            self.scrollList = DirectScrolledList(
                parent = self,
                relief = None,
                # inc and dec are DirectButtons
                incButton_image = (gui.find("**/FndsLst_ScrollUp"),
                                   gui.find("**/FndsLst_ScrollDN"),
                                   gui.find("**/FndsLst_ScrollUp_Rllvr"),
                                   gui.find("**/FndsLst_ScrollUp"),
                                   ),
                incButton_relief = None,
                incButton_pos = (0.0, 0.0, -0.316),
                # Make the disabled button darker
                incButton_image1_color = Vec4(1.0, 0.9, 0.4, 1.0),
                incButton_image3_color = Vec4(1.0, 1.0, 0.6, 0.5),
                incButton_scale = (1.0, 1.0, -1.0),
                decButton_image = (gui.find("**/FndsLst_ScrollUp"),
                                   gui.find("**/FndsLst_ScrollDN"),
                                   gui.find("**/FndsLst_ScrollUp_Rllvr"),
                                   gui.find("**/FndsLst_ScrollUp"),
                                   ),
                decButton_relief = None,
                decButton_pos = (0.0, 0.0, 0.117),
                # Make the disabled button darker
                decButton_image1_color = Vec4(1.0, 1.0, 0.6, 1.0),
                decButton_image3_color = Vec4(1.0, 1.0, 0.6, 0.6),

                # itemFrame is a DirectFrame
                itemFrame_pos = (-0.17, 0.0, 0.06),
                itemFrame_relief = DGG.SUNKEN,
                itemFrame_frameSize = (-0.01, 0.35, -0.35, 0.04),
                itemFrame_frameColor = (0.85,0.95,1,1),
                itemFrame_borderWidth = (0.01,0.01),
                numItemsVisible = 8,
                itemFrame_scale = 1.0,
                #forceHeight = 0.065,
                items = [],
                )
            gui.removeNode()
            self.scrollList.setPos(0.35, 0, 0.125)
            self.scrollList.setScale(1.25)

            # Set up a clipping plane to truncate names that would extend
            # off the right end of the scrolled list.
            clipper = PlaneNode('clipper')
            clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.17, 0, 0)))
            clipNP = self.scrollList.attachNewNode(clipper)
            self.scrollList.setClipPlane(clipNP)

            self.__makeScrollList()

    def checkFamily(self, doId):
        test = 0
        for familyMember in base.cr.avList:
            if familyMember.id == doId:
                test = 1
        return test

    def __makeFFlist(self):
        # Make the player's avatar the first in the list and make a preview
        playerAvatar = (base.localAvatar.doId, base.localAvatar.name, NametagGroup.CCNonPlayer)
        self.ffList.append(playerAvatar)
        self.dnaSelected = base.localAvatar.style # Making the player's avatarDNA the default dna
        self.createPreviewToon(self.dnaSelected)

        for familyMember in base.cr.avList:
            if familyMember.id != base.localAvatar.doId:
                newFF = (familyMember.id, familyMember.name, NametagGroup.CCNonPlayer)
                self.ffList.append(newFF)
        for friendPair in base.localAvatar.friendsList:
            friendId, flags = friendPair
            #print "adding friend"
            handle = base.cr.identifyFriend(friendId)
            if handle and not self.checkFamily(friendId):
                if hasattr(handle, 'getName'):
                    colorCode = NametagGroup.CCSpeedChat
                    if (flags & ToontownGlobals.FriendChat):
                        colorCode = NametagGroup.CCFreeChat
                    newFF = (friendPair[0], handle.getName(), colorCode)
                    self.ffList.append(newFF)
                else:
                    self.notify.warning("Bad Handle for getName in makeFFlist")

    def __makeScrollList(self):
        for ff in self.ffList:
            ffbutton = self.makeFamilyButton(ff[0], ff[1], ff[2])
            if ffbutton:
                self.scrollList.addItem(ffbutton, refresh=0)
                self.friends[ff] = ffbutton
        self.scrollList.refresh()

    def makeFamilyButton(self, familyId, familyName, colorCode):
        # What color should we display the name in?  Use the
        # appropriate nametag color, according to whether we are
        # "special friends" or not.
        fg = NametagGlobals.getNameFg(colorCode, PGButton.SInactive)

        return DirectButton(
            relief = None,
            text = familyName,
            text_scale = 0.04,
            text_align = TextNode.ALeft,
            text_fg = fg,
            text1_bg = self.textDownColor,
            text2_bg = self.textRolloverColor,
            text3_fg = self.textDisabledColor,
            textMayChange = 0,
            command = self.__chooseFriend,
            extraArgs = [familyId, familyName],
            )

    def __chooseFriend(self, friendId, friendName):
        """
        selects a friend for loading for the preview toon
        I can get my avatar's dna using base.localAvatar.style.
        I can get the dna of all my friends using base.cr.identifyFriend(avId),
        but I cannot get the dna of the other avatars of my account (family) using the above.
        For my family avatars we make a request to the database by using :
        base.cr.getAvatarDetails(familyAvatar, self.__handleFamilyAvatar, "DistributedToon")
        """
        messenger.send('wakeup')

        if self.checkFamily(friendId):
            if friendId == base.localAvatar.doId:
                self.createPreviewToon(base.localAvatar.style)
            else:
                # The request to the database takes too long, so we cache off the value
                # everytime a new family avatar is clicked. Check this list before making a new database request.
                if self.doId2Dna.has_key(friendId):
                    self.createPreviewToon(self.doId2Dna[friendId])
                else:
                    familyAvatar = DistributedToon.DistributedToon(base.cr)
                    familyAvatar.doId = friendId # The doId is required for getAvatarDetails to work
                    # getAvatarDetails puts a DelayDelete on the avatar, and this
                    # is not a real DO, so bypass the 'generated' check
                    familyAvatar.forceAllowDelayDelete()
                    base.cr.getAvatarDetails(familyAvatar, self.__handleFamilyAvatar, "DistributedToon")
        else:
            friend = base.cr.identifyFriend(friendId)
            if friend:
                self.createPreviewToon(friend.style)

    def __handleFamilyAvatar(self, gotData, avatar, dclass):
        self.doId2Dna[avatar.doId] = avatar.style
        self.createPreviewToon(avatar.style)
        avatar.delete()

    def createPreviewToon(self, dna):
        '''Create a toon to show as a preview on the screen'''
        # Clean up any old preview toon
        if hasattr(self, 'previewToon'):
            self.previewToon.delete()

        self.dnaSelected = dna
        self.previewToon = Toon.Toon()
        self.previewToon.setDNA(dna)
        self.previewToon.loop('neutral')
        self.previewToon.setH(180)
        self.previewToon.setPos(-0.3, 0, -0.3)
        # @TODO: Adjust height
        self.previewToon.setScale(0.13)
        self.previewToon.reparentTo(self)
        # Start blinking and looking around.
        self.previewToon.startBlink()
        self.previewToon.startLookAround()
        # Turn on depth write and test so that it renders correctly on the 2D frame.
        self.previewToon.getGeomNode().setDepthWrite(1)
        self.previewToon.getGeomNode().setDepthTest(1)