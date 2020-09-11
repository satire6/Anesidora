from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from otp.avatar import Avatar
from direct.distributed import DistributedObject
import SuitDNA
from toontown.toonbase import TTLocalizer
from otp.avatar import AvatarPanel
from toontown.friends import FriendsListPanel

class SuitAvatarPanel(AvatarPanel.AvatarPanel):
    """
    This is a panel that pops up in response to clicking on a Toon or
    Cog nearby you, or to picking a Toon from your friends list.  It
    draws a little picture of the avatar's head, and gives you a few
    options to pick from re the avatar.
    """

    # Limit to only have one avatar panel at a time
    currentAvatarPanel = None

    def __init__(self, avatar):
        AvatarPanel.AvatarPanel.__init__(
            self, avatar, FriendsListPanel = FriendsListPanel)

        self.avName = avatar.getName()

        gui = loader.loadModel("phase_3.5/models/gui/suit_detail_panel")
        self.frame = DirectFrame(
                geom = gui.find("**/avatar_panel"),
                geom_scale = 0.21,
                geom_pos = (0,0,0.02),
                relief = None,
                pos = (1.1, 100, 0.525),
                )
            
        disabledImageColor = Vec4(1,1,1,0.4)
        text0Color = Vec4(1,1,1,1)
        text1Color = Vec4(0.5,1,0.5,1)
        text2Color = Vec4(1,1,0.5,1)
        text3Color = Vec4(1,1,1,0.2)

        # Now put the avatar's head in the panel.
        self.head = self.frame.attachNewNode('head')
        for part in avatar.headParts:
            copyPart = part.copyTo(self.head)
            # Turn on depth write and test.
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)
        p1 = Point3()
        p2 = Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.3/biggest
        self.head.setPosHprScale(
            0, 0, 0,
            180, 0, 0,
            s, s, s)

        # Put the avatar's name across the top.
        self.nameLabel = DirectLabel(
                parent = self.frame,
                pos = (0.0125, 0, 0.36),
                relief = None,
                text = self.avName,
                text_font = avatar.getFont(),
                text_fg = Vec4(0,0,0,1),
                text_pos = (0, 0),
                text_scale = 0.047,
                text_wordwrap = 7.5,
                text_shadow = (1, 1, 1, 1),
                )

        level = avatar.getActualLevel()
        dept = SuitDNA.getSuitDeptFullname(avatar.dna.name)
            
        self.levelLabel = DirectLabel(
                parent = self.frame,
                pos = (0, 0, -0.1),
                relief = None,
                text = (TTLocalizer.AvatarPanelCogLevel % level),
                text_font = avatar.getFont(),
                text_align = TextNode.ACenter,
                text_fg = Vec4(0,0,0,1),
                text_pos = (0, 0),
                text_scale = 0.05,
                text_wordwrap = 8.0,
                )

        # Get a temp copy of the corporate medallion for this suit
        corpIcon = avatar.corpMedallion.copyTo(hidden)
        corpIcon.iPosHprScale()
        self.corpIcon = DirectLabel(
                parent = self.frame,
                geom = corpIcon,
                geom_scale = 0.13,
                pos = (0, 0, -0.175),
                relief = None,
                )
        # Delete copy
        corpIcon.removeNode()

        self.deptLabel = DirectLabel(
                parent = self.frame,
                pos = (0, 0, -0.28),
                relief = None,
                text = dept,
                text_font = avatar.getFont(),
                text_align = TextNode.ACenter,
                text_fg = Vec4(0,0,0,1),
                text_pos = (0, 0),
                text_scale = 0.05,
                text_wordwrap = 8.0,
                )

        self.closeButton = DirectButton(
                parent = self.frame,
                relief = None,
                pos = (0., 0, -0.36),
                text = TTLocalizer.AvatarPanelCogDetailClose,
                text_font = avatar.getFont(),
                text0_fg = Vec4(0,0,0,1),
                text1_fg = Vec4(0.5,0,0,1),
                text2_fg = Vec4(1,0,0,1),
                text_pos = (0, 0),
                text_scale = 0.05,
                command = self.__handleClose,
                )
                
        gui.removeNode()

        menuX = -0.05
        menuScale = 0.064

        # hide the friend and clarabelle gui
        base.localAvatar.obscureFriendsListButton(1)
        
        self.frame.show()
        messenger.send("avPanelDone")
        
    def cleanup(self):
        if self.frame == None:
            return
        self.frame.destroy()
        del self.frame
        self.frame = None

        self.head.removeNode()
        del self.head

        # show the friend and clarabelle gui
        base.localAvatar.obscureFriendsListButton(-1)

        AvatarPanel.AvatarPanel.cleanup(self)

    def __handleClose(self):
        self.cleanup()
        AvatarPanel.currentAvatarPanel = None
