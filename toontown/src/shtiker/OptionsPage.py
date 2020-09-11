"""OptionsPage module: contains the OptionsPage class"""

from pandac.PandaModules import *
import ShtikerPage
from toontown.toontowngui import TTDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import DisplaySettingsDialog
from direct.task import Task
from otp.speedchat import SpeedChat
from otp.speedchat import SCColorScheme
from otp.speedchat import SCStaticTextTerminal
from direct.showbase import PythonUtil
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

# array of the possible speedChatStyles and colors to use
# R,G,B for arrow, rollover, and frame color if we want to specify it
# the first parameter refers to the key in the SpeedChatStaticText variable
# in the localizer
# framecolor must be included so that the talk-bubble backgrounds are correct
speedChatStyles = (
     # Purple
    (2000, (200/255.,  60/255., 229/255.),
           (200/255., 135/255., 255/255.),
           (220/255., 195/255., 229/255.)),
     # Blue
    (2001, (  0/255.,   0/255., 255/255.),
           (140/255., 150/255., 235/255.),
           (201/255., 215/255., 255/255.)),
     # Cyan
    (2002, ( 90/255., 175/255., 225/255.),
           (120/255., 215/255., 255/255.),
           (208/255., 230/255., 250/255.)),
     # Teal
    (2003, (130/255., 235/255., 235/255.),
           (120/255., 225/255., 225/255.),
           (234/255., 255/255., 255/255.)),
     # Green
    (2004, (  0/255., 200/255.,  70/255.),
           (  0/255., 200/255.,  80/255.),
           (204/255., 255/255., 204/255.)),
     # Yellow
    (2005, (235/255., 230/255.,   0/255.),
           (255/255., 250/255., 100/255.),
           (255/255., 250/255., 204/255.)),
     # Orange
    (2006, (255/255., 153/255.,   0/255.),
           (229/255., 147/255.,   0/255.),
           (255/255., 234/255., 204/255.)),
     # Red
    (2007, (255/255.,   0/255.,  50/255.),
           (229/255.,   0/255.,  50/255.),
           (255/255., 204/255., 204/255.)),
     # Pink
    (2008, (255/255., 153/255., 193/255.),
           (240/255., 157/255., 192/255.),
           (255/255., 215/255., 238/255.)),
     # Brown
    (2009, (170/255., 120/255.,  20/255.),
           (165/255., 120/255.,  50/255.),
           (210/255., 200/255., 180/255.)),
     )

##########################################################################
# Global Variables and Enumerations
##########################################################################
PageMode = PythonUtil.Enum("Options, Codes")

class OptionsPage(ShtikerPage.ShtikerPage):
    """OptionsPage class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("OptionsPage")

    # special methods
    def __init__(self):
        """__init__(self)
        OptionsPage constructor: create the options page
        """
        ShtikerPage.ShtikerPage.__init__(self)
        
        if __debug__:
            base.op = self

    def load(self):
        assert self.notify.debugStateCall(self)
        ShtikerPage.ShtikerPage.load(self)
        
        # Create the OptionsTabPage
        self.optionsTabPage = OptionsTabPage(self)
        self.optionsTabPage.hide()
        
        # Create the CodesTabPage
        self.codesTabPage = CodesTabPage(self)
        self.codesTabPage.hide()
            
        titleHeight = 0.61 # bigger number means higher the title
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.OptionsPageTitle,
            text_scale = 0.12,
            pos = (0,0,titleHeight),
            )
        
        # The blue and yellow colors are trying to match the
        # rollover and select colors on the options page:
        normalColor = (1, 1, 1, 1)
        clickColor = (.8, .8, 0, 1)
        rolloverColor = (0.15, 0.82, 1.0, 1)
        diabledColor = (1.0, 0.98, 0.15, 1)
        
        # Load the Fish Page to borrow its tabs
        gui = loader.loadModel( "phase_3.5/models/gui/fishingBook" )

        self.optionsTab = DirectButton(
            parent = self,
            relief = None,
            text = TTLocalizer.OptionsPageTitle,
            text_scale = TTLocalizer.OPoptionsTab,
            text_align = TextNode.ALeft,
            text_pos = (0.01, 0.0, 0.0),
            image = gui.find("**/tabs/polySurface1"),
            image_pos = (0.55,1,-0.91),
            image_hpr = (0,0,-90),
            image_scale = (0.033,0.033,0.035),
            image_color = normalColor,
            image1_color = clickColor,
            image2_color = rolloverColor,
            image3_color = diabledColor,
            text_fg = Vec4(0.2,0.1,0,1),
            command = self.setMode,
            extraArgs = [PageMode.Options],
            pos = (-0.36, 0, 0.77),
            )
            
        self.codesTab = DirectButton(
            parent = self,
            relief = None,
            text = TTLocalizer.OptionsPageCodesTab,
            text_scale = TTLocalizer.OPoptionsTab,
            text_align = TextNode.ALeft,
            text_pos = (-0.035, 0.0, 0.0),
            image = gui.find("**/tabs/polySurface2"),
            image_pos = (0.12,1,-0.91),
            image_hpr = (0,0,-90),
            image_scale = (0.033,0.033,0.035),
            image_color = normalColor,
            image1_color = clickColor,
            image2_color = rolloverColor,
            image3_color = diabledColor,
            text_fg = Vec4(0.2,0.1,0,1),
            command = self.setMode,
            extraArgs = [PageMode.Codes],
            pos = (0.11, 0, 0.77),
            )
        
    def enter(self):
        assert self.notify.debugStateCall(self)
        
        # Default to the Options Page.
        self.setMode(PageMode.Options, updateAnyways = 1)
        
        # Make the call to the superclass enter method.
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        assert self.notify.debugStateCall(self)
        self.optionsTabPage.exit()
        self.codesTabPage.exit()
        
        # Make the call to the superclass exit method.
        ShtikerPage.ShtikerPage.exit(self)

    def unload(self):
        assert self.notify.debugStateCall(self)
        self.optionsTabPage.unload()
        
        del self.title
        
        # Make the call to the superclass unload method.
        ShtikerPage.ShtikerPage.unload(self)
    
    def setMode(self, mode, updateAnyways = 0):
        """
        Purpose: The setMode Method sets the current mode of the OptionsPage
        of the Shtiker Book.
        Params: mode - the new mode.
                updateAnyways - update the page based on the mode.
        Return: None
        """
        messenger.send('wakeup')
        if (not updateAnyways):
            if(self.mode == mode):
                return
            else:
                self.mode = mode

        if (mode == PageMode.Options):
            self.mode = PageMode.Options
            self.title['text'] = TTLocalizer.OptionsPageTitle
            self.optionsTab['state'] = DGG.DISABLED
            self.optionsTabPage.enter()
            self.codesTab['state'] = DGG.NORMAL
            self.codesTabPage.exit()
            
        elif(mode == PageMode.Codes):
            self.mode = PageMode.Codes
            self.title['text'] = TTLocalizer.CdrPageTitle
            self.optionsTab['state'] = DGG.NORMAL
            self.optionsTabPage.exit()
            self.codesTab['state'] = DGG.DISABLED
            self.codesTabPage.enter()
            
        else:
            raise StandardError, "OptionsPage::setMode - Invalid Mode %s" % (mode)

            
class OptionsTabPage(DirectFrame):
    """
    Purpose: The OptionsTabPage class initializes the user interface for
    the Options Tab. We are splitting the Options Page into the Options Tab
    and the Code Redemption Tab.
    """

    ######################################################################
    # Class Variables
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    notify = DirectNotifyGlobal.directNotify.newCategory("OptionsTabPage")
    
    # When the user changes the display settings, even after he goes
    # through the "yes I approve of this new setting" hoopla, we don't
    # write the new setting to disk immediately, just in case it will
    # crash as soon as he starts to render a real scene.  Rather, we
    # write it out after a certain amount of time has elapsed after he
    # leaves the options page.  These parameters specify the name of
    # the doLater task and the amount of time in seconds to wait.
    DisplaySettingsTaskName = "save-display-settings"
    DisplaySettingsDelay = 60

    # If this variable is set to false, we're not allowed to change
    # the display settings using this interface, except for the screen
    # resolution.
    ChangeDisplaySettings = base.config.GetBool('change-display-settings', 1)
    ChangeDisplayAPI = base.config.GetBool('change-display-api', 0)

    # This maps our expected API interfaces to a symbolic constant in the settings file.
    DisplaySettingsApiMap = {
        'OpenGL' : Settings.GL,
        'DirectX7' : Settings.DX7,
        'DirectX8' : Settings.DX8
        }
    
    def __init__(self, parent = aspect2d):
        """
        Purpose: The __init__ Method provides the initial construction of
        the OptionsTabPage object that will provide the base interface
        for the Options Page.
        Params: None
        Return: None
        """
        self.parent = parent
        self.currentSizeIndex = None
        # Construct the super class object from which the selector derives.
        DirectFrame.__init__(
            self,
            parent = self.parent,
            relief = None,
            pos = ( 0.0, 0.0, 0.0 ),
            scale = ( 1.0, 1.0, 1.0 ),
            )
        self.load()
    
    def destroy(self):
        """
        Purpose: The destroy Method properly handles the destruction of
        the OptionsTabPage instance by handling appropriate reference
        cleanup.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        # Destroy UI Components of the CustomizeUI        

        # Remove references to UI Components and instance variables for
        # garbage collection purposes.
        self.parent = None
        
        # Destroy the DirectFrame super class.
        DirectFrame.destroy(self)

    def load(self):
        """
        Purpose: The load Method handles the construction of the specific
        UI components that make up the OptionsTabPage object.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)

        self.displaySettings = None

        # These properties are set when we come back from looking at
        # the DisplaySettings page.  At some later point, we'll
        # actually save these to the Settings file.
        self.displaySettingsChanged = 0
        self.displaySettingsSize = (None, None)
        self.displaySettingsFullscreen = None
        self.displaySettingsEmbedded = None
        self.displaySettingsApi = None
        self.displaySettingsApiChanged = 0

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")

        # tweak these constants to change the layout
        # the coordinate system is (0,0) in the middle of the page
        # Vertical: -1.0 is the bottom, and 1.0 is the top  of the screen
        # Horizontal: -1.0 is left edge of shticker book, 1.0 is right edge
        titleHeight = 0.61 # bigger number means higher the title
        textStartHeight = 0.45 # bigger number means higher text
        textRowHeight = 0.15 # bigger number means more space between rows
        leftMargin = -0.72 # smaller number means farther left
        buttonbase_xcoord = 0.35 # bigger number means farther right
        buttonbase_ycoord = 0.45 # bigger number means higher buttons
        button_image_scale = (0.7,1,1)
        button_textpos = (0,-0.02)
        options_text_scale = 0.052
        disabled_arrow_color = Vec4(0.6, 0.6, 0.6, 1.0)  # Make the disabled button darker
        self.speed_chat_scale = 0.055

        self.Music_Label = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            pos = (leftMargin, 0,
                   textStartHeight),
            )

        self.SoundFX_Label = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            text_wordwrap = 16,
            pos = (leftMargin, 0,
                   textStartHeight - textRowHeight),
            )

        self.Friends_Label = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            text_wordwrap = 16,
            # adjust for taller two-row text
            pos = (leftMargin, 0,
                   textStartHeight - 3 * textRowHeight),
            )

        self.DisplaySettings_Label = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            text_wordwrap = 10,
            pos = (leftMargin, 0,
                   textStartHeight - 4 * textRowHeight),
            )

        self.SpeedChatStyle_Label = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.OptionsPageSpeedChatStyleLabel,
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            text_wordwrap = 10,
            pos = (leftMargin, 0,
                   textStartHeight - 5 * textRowHeight),
            )

        self.ToonChatSounds_Label = DirectLabel(
            parent = self,
            relief = None,
            text = "",
            text_align = TextNode.ALeft,
            text_scale = options_text_scale,
            text_wordwrap = 15,
            pos = (leftMargin, 0,
                   textStartHeight - (2 * textRowHeight) + 0.025),
            )
        self.ToonChatSounds_Label.setScale(0.9)

        self.Music_toggleButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = button_image_scale,
            text = "",
            text_scale = options_text_scale,
            text_pos = button_textpos,
            pos = (buttonbase_xcoord, 0.0, buttonbase_ycoord),
            command = self.__doToggleMusic,
            )

        self.SoundFX_toggleButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = button_image_scale,
            text = "",
            text_scale = options_text_scale,
            text_pos = button_textpos,
            pos = (buttonbase_xcoord, 0.0, buttonbase_ycoord-textRowHeight),
            command = self.__doToggleSfx,
            )

        self.Friends_toggleButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = button_image_scale,
            text = "",
            text_scale = options_text_scale,
            text_pos = button_textpos,
            pos = (buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight*3),
            command = self.__doToggleAcceptFriends,
            )

        self.DisplaySettingsButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image3_color = Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale = button_image_scale,
            text = TTLocalizer.OptionsPageChange,
            text3_fg = (0.5, 0.5, 0.5, 0.75),
            text_scale = options_text_scale,
            text_pos = button_textpos,
            pos = (buttonbase_xcoord, 0.0,
                   buttonbase_ycoord - textRowHeight * 4),
            command = self.__doDisplaySettings,
            )

        self.speedChatStyleLeftArrow = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/Horiz_Arrow_UP"),
                     gui.find("**/Horiz_Arrow_DN"),
                     gui.find("**/Horiz_Arrow_Rllvr"),
                     gui.find("**/Horiz_Arrow_UP"),
                     ),
            # make the disabled color more transparent
            image3_color = Vec4(1, 1, 1, 0.5),
            scale = (-1.0, 1.0, 1.0),  # make the arrow point left
            pos = (0.25, 0, buttonbase_ycoord - textRowHeight * 5),
            command = self.__doSpeedChatStyleLeft,
            )

        self.speedChatStyleRightArrow = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/Horiz_Arrow_UP"),
                     gui.find("**/Horiz_Arrow_DN"),
                     gui.find("**/Horiz_Arrow_Rllvr"),
                     gui.find("**/Horiz_Arrow_UP"),
                     ),
            # make the disabled color more transparent
            image3_color = Vec4(1, 1, 1, 0.5),
            pos = (0.65, 0, buttonbase_ycoord - textRowHeight * 5),
            command = self.__doSpeedChatStyleRight,
            )

        self.ToonChatSounds_toggleButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     guiButton.find("**/QuitBtn_UP"),
                     ),
            image3_color = Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale = button_image_scale,
            text = "",
            text3_fg = (0.5, 0.5, 0.5, 0.75),
            text_scale = options_text_scale,
            text_pos = button_textpos,
            pos = (buttonbase_xcoord, 0.0, (buttonbase_ycoord-textRowHeight * 2) + 0.025),
            command = self.__doToggleToonChatSounds,
            )
        self.ToonChatSounds_toggleButton.setScale(0.8)

        # The [2000] refers to the default color.  In the localizer, refer
        # to the SpeedChatStaticText variable
        self.speedChatStyleText = SpeedChat.SpeedChat(
            name='OptionsPageStyleText', structure=[2000],
            backgroundModelName='phase_3/models/gui/ChatPanel',
            guiModelName='phase_3.5/models/gui/speedChatGui')
        self.speedChatStyleText.setScale(self.speed_chat_scale)
        # This will be horizontally centered later
        self.speedChatStyleText.setPos(0.37, 0, -0.27)
        self.speedChatStyleText.reparentTo(self, DGG.FOREGROUND_SORT_INDEX)

        self.exitButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = 1.15,
            text = TTLocalizer.OptionsPageExitToontown,
            text_scale = options_text_scale,
            text_pos = button_textpos,
            textMayChange = 0,
            pos = (0.45,0,-0.6),
            command = self.__handleExitShowWithConfirm,
            )

        guiButton.removeNode()
        gui.removeNode()

    def enter(self):
        """
        Purpose: This method gets called when the Options Tab is selected.
        Also, this is the default tab in this page and gets selected by default
        everytime the Options and Codes page is selected.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        self.show()
        
        # If we haven't yet saved the display settings we set last
        # time, stop the task until we leave the page again.
        taskMgr.remove(self.DisplaySettingsTaskName)
        self.settingsChanged = 0

        self.__setMusicButton()
        self.__setSoundFXButton()
        self.__setAcceptFriendsButton()
        self.__setDisplaySettings()
        self.__setToonChatSoundsButton()

        self.speedChatStyleText.enter()
        # get the proper index for the speedChatStyle and set it
        # this function is actually found in DistributedToon.py
        self.speedChatStyleIndex = base.localAvatar.getSpeedChatStyleIndex()
        self.updateSpeedChatStyle()

        if self.parent.book.safeMode:
            self.exitButton.hide()
        else:
            self.exitButton.show()

    def exit(self):
        assert self.notify.debugStateCall(self)
        self.hide()
        if(self.settingsChanged != 0):
            Settings.writeSettings()

        self.speedChatStyleText.exit()

        if self.displaySettingsChanged:
            # If we have changed the display settings, then spawn a
            # task to write the new changes to the SettingsFile in
            # about a minute or so.  We do this just to be paranoid,
            # to give the user a chance to crash first in case it's
            # going to.
            taskMgr.doMethodLater(self.DisplaySettingsDelay,
                                  self.writeDisplaySettings,
                                  self.DisplaySettingsTaskName)
                                  
    def unload(self):
        assert self.notify.debugStateCall(self)
        # Now that we're unloading, we're confident the user is
        # exiting the game through one of the normal,
        # non-graphics-driver crashing interfaces: either by clicking
        # the exit or logout button, Alt-F4'ing the window, or
        # experiencing a Python exception.  In any of these cases,
        # we'll go ahead and save the display settings if they haven't
        # been saved yet.
        self.writeDisplaySettings()

        taskMgr.remove(self.DisplaySettingsTaskName)
        if self.displaySettings != None:
            self.ignore(self.displaySettings.doneEvent)
            self.displaySettings.unload()
        self.displaySettings = None
        self.exitButton.destroy()
        self.Music_toggleButton.destroy()
        self.SoundFX_toggleButton.destroy()
        self.Friends_toggleButton.destroy()
        self.DisplaySettingsButton.destroy()
        self.speedChatStyleLeftArrow.destroy()
        self.speedChatStyleRightArrow.destroy()
        del self.exitButton
        del self.SoundFX_Label
        del self.Music_Label
        del self.Friends_Label
        del self.SpeedChatStyle_Label
        del self.SoundFX_toggleButton
        del self.Music_toggleButton
        del self.Friends_toggleButton
        del self.speedChatStyleLeftArrow
        del self.speedChatStyleRightArrow
        self.speedChatStyleText.exit()
        self.speedChatStyleText.destroy()
        del self.speedChatStyleText
        self.currentSizeIndex = None
    
    def __doToggleMusic(self):
        messenger.send('wakeup')
        if base.musicActive:
            base.enableMusic(0)
            Settings.setMusic(0)
        else:
            base.enableMusic(1)
            Settings.setMusic(1)

        self.settingsChanged = 1
        self.__setMusicButton()

    def __setMusicButton(self):
        if base.musicActive:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOnLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Music_Label['text'] = TTLocalizer.OptionsPageMusicOffLabel
            self.Music_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __doToggleSfx(self):
        messenger.send('wakeup')
        if base.sfxActive:
            base.enableSoundEffects(0)
            Settings.setSfx(0)
        else:
            base.enableSoundEffects(1)
            Settings.setSfx(1)

        self.settingsChanged = 1
        self.__setSoundFXButton()

    def __doToggleToonChatSounds(self):
        messenger.send('wakeup')
        if base.toonChatSounds:
            base.toonChatSounds = 0
            Settings.setToonChatSounds(0)
        else:
            base.toonChatSounds = 1
            Settings.setToonChatSounds(1)

        self.settingsChanged = 1
        self.__setToonChatSoundsButton()        

    def __setSoundFXButton(self):
        if base.sfxActive:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOnLabel
            self.SoundFX_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.SoundFX_Label['text'] = TTLocalizer.OptionsPageSFXOffLabel
            self.SoundFX_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

        # we affect the toon chat sounds button
        self.__setToonChatSoundsButton()

    def __setToonChatSoundsButton(self):
        if base.toonChatSounds:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOnLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.ToonChatSounds_Label['text'] = TTLocalizer.OptionsPageToonChatSoundsOffLabel
            self.ToonChatSounds_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

        # we are affected by the sfx active flag
        if base.sfxActive:
            self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
            self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
        else:
            self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
            self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

    def __doToggleAcceptFriends(self):
        messenger.send('wakeup')
        if base.localAvatar.acceptingNewFriends:
            # now we dont accept friends
            base.localAvatar.acceptingNewFriends = 0
            Settings.setAcceptingNewFriends(0)
        else:
            base.localAvatar.acceptingNewFriends = 1
            Settings.setAcceptingNewFriends(1)
        
        self.settingsChanged = 1
        self.__setAcceptFriendsButton()

        # We certainly don't want to save the friends setting in the
        # Configrc file, since it's something that should be specific
        # to the toon, not to the PC the user happens to be playing
        # on.  In fact, it's a little strange to even have this
        # particular option here along with with these PC-specific
        # options like screen resolution.

        # If we were to save this property, it would be saved in the
        # database along with all the other toon properties.  But
        # maybe we shouldn't be saving it at all, and force the user
        # to re-enable it at each session.

    def __setAcceptFriendsButton(self):
        if base.localAvatar.acceptingNewFriends:
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsEnabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOff
        else:
            self.Friends_Label['text'] = TTLocalizer.OptionsPageFriendsDisabledLabel
            self.Friends_toggleButton['text'] = TTLocalizer.OptionsPageToggleOn

    def __doDisplaySettings(self):
        if self.displaySettings == None:
            self.displaySettings = DisplaySettingsDialog.DisplaySettingsDialog()
            self.displaySettings.load()
            self.accept(self.displaySettings.doneEvent, self.__doneDisplaySettings)
        self.displaySettings.enter(self.ChangeDisplaySettings, self.ChangeDisplayAPI)
        return

    def __doneDisplaySettings(self, anyChanged, apiChanged):
        if anyChanged:
            self.__setDisplaySettings()

            # Save the new settings so we can copy them to the
            # SettingsFile a little later.
            properties = base.win.getProperties()
            self.displaySettingsChanged = 1
            self.displaySettingsSize = (properties.getXSize(), properties.getYSize())
            self.displaySettingsFullscreen = properties.getFullscreen()
            self.displaySettingsEmbedded = self.isPropertiesEmbedded(properties)
            self.displaySettingsApi = base.pipe.getInterfaceName()
            self.displaySettingsApiChanged = apiChanged

    def isPropertiesEmbedded(self, properties):
        """Returns true if the current game window is inside a browser."""
        result = False
        if properties.getParentWindow():
            result = True
        return result            

    def __setDisplaySettings(self):
        properties = base.win.getProperties()
        if properties.getFullscreen():
            screensize = "%s x %s" % (properties.getXSize(), properties.getYSize())
        else:
            screensize = TTLocalizer.OptionsPageDisplayWindowed
        isEmbedded = self.isPropertiesEmbedded(properties)
        if isEmbedded:
            screensize = TTLocalizer.OptionsPageDisplayEmbedded
            
        api = base.pipe.getInterfaceName()

        settings = {
            'screensize' : screensize,
            'api' : api
            }
        if self.ChangeDisplayAPI:
            OptionsPage.notify.debug("change display settings...")
            text = TTLocalizer.OptionsPageDisplaySettings % settings
        else:
            OptionsPage.notify.debug("no change display settings...")
            text = TTLocalizer.OptionsPageDisplaySettingsNoApi % settings
        self.DisplaySettings_Label['text'] = text

    def __doSpeedChatStyleLeft(self):
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleIndex = self.speedChatStyleIndex - 1
            self.updateSpeedChatStyle()

    def __doSpeedChatStyleRight(self):
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleIndex = self.speedChatStyleIndex + 1
            self.updateSpeedChatStyle()

    def updateSpeedChatStyle(self):
        # update the text color and value
        nameKey, arrowColor, rolloverColor, frameColor = \
                 speedChatStyles[self.speedChatStyleIndex]
        # create the new color scheme object for the text label
        newSCColorScheme = SCColorScheme.SCColorScheme(
            arrowColor=arrowColor,
            rolloverColor=rolloverColor,
            frameColor=frameColor,
            )
        # set the new color scheme
        self.speedChatStyleText.setColorScheme(newSCColorScheme)
        # set the new text
        self.speedChatStyleText.clearMenu()
        colorName = SCStaticTextTerminal.SCStaticTextTerminal(nameKey)
        self.speedChatStyleText.append(colorName)
        # we must finalize to get the accurate width
        self.speedChatStyleText.finalize()
        # manual horizonal centering
        self.speedChatStyleText.setPos(
            0.445 - self.speedChatStyleText.getWidth() * self.speed_chat_scale / 2, 0, -0.27)

        # show the appropriate arrows
        if self.speedChatStyleIndex > 0:
            self.speedChatStyleLeftArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleLeftArrow['state'] = DGG.DISABLED
        if self.speedChatStyleIndex < len(speedChatStyles) - 1:
            self.speedChatStyleRightArrow['state'] = DGG.NORMAL
        else:
            self.speedChatStyleRightArrow['state'] = DGG.DISABLED

        # actually cause the speed chat color to change and propagate to the DB
        # this function is actually found in DistributedToon.py
        base.localAvatar.b_setSpeedChatStyleIndex(self.speedChatStyleIndex)

    def writeDisplaySettings(self, task = None):
        # Writes the previously-saved display settings to the
        # SettingsFile, after the safety timer has expired.
        if not self.displaySettingsChanged:
            return

        # Make sure our timer task has been removed (we might call
        # this method explicitly, before the timer has expired).
        taskMgr.remove(self.DisplaySettingsTaskName)

        self.notify.info("writing new display settings %s, %s, %s to SettingsFile." %
                         (self.displaySettingsSize, self.displaySettingsFullscreen,
                          self.displaySettingsApi))

        Settings.setResolutionDimensions(self.displaySettingsSize[0], self.displaySettingsSize[1])

        Settings.setWindowedMode(not self.displaySettingsFullscreen)
        if self.displaySettingsApiChanged:
            api = self.DisplaySettingsApiMap.get(self.displaySettingsApi)
            if api == None:
                self.notify.warning("Cannot save unknown display API: %s" % (self.displaySettingsApi))
            else:
                Settings.setDisplayDriver(api)
        Settings.writeSettings()

        self.displaySettingsChanged = 0

        return Task.done

    def __handleExitShowWithConfirm(self):
        # For exiting from the options panel to the avatar chooser.
        """__handleExitShowWithConfirm(self)
        """
        self.confirm = TTDialog.TTGlobalDialog(
                                   doneEvent = "confirmDone",
                                   message = TTLocalizer.OptionsPageExitConfirm,
                                   style = TTDialog.TwoChoice)
        self.confirm.show()
        self.parent.doneStatus = {
                "mode": "exit",
                "exitTo": "closeShard"}
        self.accept("confirmDone", self.__handleConfirm)

    def __handleConfirm(self):
        """__handleConfirm(self)
        """
        status = self.confirm.doneStatus
        self.ignore("confirmDone")
        self.confirm.cleanup()
        del self.confirm
        if (status == "ok"):
            base.cr._userLoggingOut = True
            messenger.send(self.parent.doneEvent)
            #self.cr.loginFSM.request("chooseAvatar", [self.cr.avList])
            
class CodesTabPage(DirectFrame):
    """
    Purpose: The CodesTabPage class initializes the user interface for
    the Code Redemption Tab. We are splitting the Options Page into the Options Tab
    and the Code Redemption Tab.
    """

    ######################################################################
    # Class Variables
    ######################################################################
    #__metaclass__ = PythonUtil.Singleton
    notify = DirectNotifyGlobal.directNotify.newCategory("CodesTabPage")
    
    def __init__(self, parent = aspect2d):
        """
        Purpose: The __init__ Method provides the initial construction of
        the CodesTabPage object that will provide the base interface
        for the Code Redemption Page.
        Params: None
        Return: None
        """        
        self.parent = parent
        # Construct the super class object from which the selector derives.
        DirectFrame.__init__(
            self,
            parent = self.parent,
            relief = None,
            pos = ( 0.0, 0.0, 0.0 ),
            scale = ( 1.0, 1.0, 1.0 ),
            )
        self.load()

    def destroy(self):
        """
        Purpose: The destroy Method properly handles the destruction of
        the CodesTabPage instance by handling appropriate reference
        cleanup.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        # Destroy UI Components of the CustomizeUI        

        # Remove references to UI Components and instance variables for
        # garbage collection purposes.
        self.parent = None
        
        # Destroy the DirectFrame super class.
        DirectFrame.destroy(self)

    def load(self):
        """
        Purpose: The load Method handles the construction of the specific
        UI components that make up the CodesTabPage object.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        
        cdrGui = loader.loadModel("phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui")
        instructionGui = cdrGui.find("**/tt_t_gui_sbk_cdrPresent")
        flippyGui = cdrGui.find("**/tt_t_gui_sbk_cdrFlippy")
        codeBoxGui = cdrGui.find("**/tt_t_gui_sbk_cdrCodeBox")
        self.resultPanelSuccessGui = cdrGui.find("**/tt_t_gui_sbk_cdrResultPanel_success")
        self.resultPanelFailureGui = cdrGui.find("**/tt_t_gui_sbk_cdrResultPanel_failure")
        self.resultPanelErrorGui = cdrGui.find("**/tt_t_gui_sbk_cdrResultPanel_error")
        
        self.successSfx = base.loadSfx("phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.mp3")
        self.failureSfx = base.loadSfx("phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.mp3")
        
        self.instructionPanel = DirectFrame(
            parent = self,
            relief = None,
            image = instructionGui,
            image_scale = 0.8,
            text = TTLocalizer.CdrInstructions,
            text_pos = TTLocalizer.OPCodesInstructionPanelTextPos,
            text_align = TextNode.ACenter,
            text_scale = TTLocalizer.OPCodesResultPanelTextScale,
            text_wordwrap = TTLocalizer.OPCodesInstructionPanelTextWordWrap,
            pos = (-0.429, 0, -0.05),
            )
        
        self.codeBox = DirectFrame(
            parent = self,
            relief = None,
            image = codeBoxGui,
            pos = (0.433, 0, 0.35),
            )
        
        self.flippyFrame = DirectFrame(
            parent = self,
            relief = None,
            image = flippyGui,
            pos = (0.44, 0, -0.353),
            )
        
        self.codeInput = DirectEntry(
            parent = self.codeBox,
            relief = DGG.GROOVE,
            scale = 0.08,
            pos = (-0.33, 0, -0.006),
            borderWidth = (0.05, 0.05),
            frameColor = ((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)),
            state = DGG.NORMAL,
            text_align = TextNode.ALeft,
            text_scale = TTLocalizer.OPCodesInputTextScale,
            width = 10.5,
            numLines = 1,
            focus = 1,
            backgroundFocus = 0,
            cursorKeys = 1,
            text_fg = (0, 0, 0, 1),
            suppressMouse = 1,
            autoCapitalize = 0,
            command = self.__submitCode,
            )
        
        submitButtonGui = loader.loadModel("phase_3/models/gui/quit_button")
        self.submitButton = DirectButton(
            parent = self,
            relief = None,
            image = (submitButtonGui.find("**/QuitBtn_UP"),
                     submitButtonGui.find("**/QuitBtn_DN"),
                     submitButtonGui.find("**/QuitBtn_RLVR"),
                     submitButtonGui.find("**/QuitBtn_UP"),
                     ),
            image3_color = Vec4(0.5, 0.5, 0.5, 0.5),
            image_scale = 1.15,
            state = DGG.NORMAL,
            text = TTLocalizer.NameShopSubmitButton,
            text_scale = TTLocalizer.OPCodesSubmitTextScale,
            text_align = TextNode.ACenter,
            text_pos = TTLocalizer.OPCodesSubmitTextPos,
            text3_fg = (0.5, 0.5, 0.5, 0.75),
            textMayChange = 0,
            pos = (0.45, 0.0, 0.0896),
            command = self.__submitCode,
            )
        
        self.resultPanel = DirectFrame(
            parent = self,
            relief = None,
            image = self.resultPanelSuccessGui,
            text = "",
            text_pos = TTLocalizer.OPCodesResultPanelTextPos,
            text_align = TextNode.ACenter,
            text_scale = TTLocalizer.OPCodesResultPanelTextScale,
            text_wordwrap = TTLocalizer.OPCodesResultPanelTextWordWrap,
            pos = (-0.42, 0, -0.0567),
            )
        self.resultPanel.hide()
            
        # Result Panel Close Button
        closeButtonGui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.closeButton = DirectButton(
            parent = self.resultPanel,
            pos = (0.296, 0, -0.466),
            relief = None,
            state = DGG.NORMAL,
            image = (closeButtonGui.find('**/CloseBtn_UP'),
                     closeButtonGui.find('**/CloseBtn_DN'),
                     closeButtonGui.find('**/CloseBtn_Rllvr')),
            image_scale = (1, 1, 1),
            command = self.__hideResultPanel,            
            )
        
        closeButtonGui.removeNode()
        cdrGui.removeNode()
        submitButtonGui.removeNode()
            
    def enter(self):
        """
        Purpose: This method gets called when the Codes Tab is selected.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        self.show()
        
        # While the entry's on the screen, we have to turn off the
        # background focus on the normal chat entry.  Otherwise,
        # keypresses would start chatting!
        localAvatar.chatMgr.fsm.request("otherDialog")

        # And now we can set the focus on our entry.
        self.codeInput['focus'] = 1
        
        # Make sure we always start with a blank entry box.
        self.codeInput.enterText('')
        
        # Enable the code entry box.
        self.__enableCodeEntry()

    def exit(self):
        """
        Purpose: This method gets called when we leave the Codes Tab.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        self.resultPanel.hide()
        self.hide()
        
        # Restore the background focus on the chat entry.
        localAvatar.chatMgr.fsm.request("mainMenu")
    
    def unload(self):
        """
        Purpose: This method gets called when we are exiting the game.
        Params: None
        Return: None
        """
        assert self.notify.debugStateCall(self)
        
        self.instructionPanel.destroy()
        self.instructionPanel = None
        
        self.codeBox.destroy()
        self.codeBox = None
        
        self.flippyFrame.destroy()
        self.flippyFrame = None
        
        self.codeInput.destroy()
        self.codeInput = None
        
        self.submitButton.destroy()
        self.submitButton = None
            
        self.resultPanel.destroy()
        self.resultPanel = None
        
        self.closeButton.destroy()
        self.closeButton = None
        
        del self.successSfx
        del self.failureSfx
        
    def __submitCode(self, input = None):
        """
        Purpose: This method the player submits the code.
        It could be called by pressing the submit button or by pressing Enter
        on the keyboard
        Params: input - This is the string the user entered.
        Return: None
        """
        if input == None:
            input = self.codeInput.get()
        
        # Keep focus on the code input even after entering a code.
        self.codeInput['focus'] = 1
        
        # Ignoring Blank.
        if (input == ''):
            return
        
        # If the player typed something he must be awake.
        messenger.send('wakeup')
        
        if hasattr(base, "codeRedemptionMgr"):
            base.codeRedemptionMgr.redeemCode(input, self.__getCodeResult)
        
        # Make the code entry box empty after submitting a code.
        self.codeInput.enterText('')
        
        # Disable the code entry till we get a result from the Uberdog.
        self.__disableCodeEntry()

    def __getCodeResult(self, result, awardMgrResult):
        """
        Purpose: This method is called from the AI as a callback from self.__submitCode.
        Params: result - result of the code submitted.
                awardMgrResult - the award, if the code was successful.
        Return: None
        """
        assert self.notify.debugStateCall(self)
        self.notify.debug("result = %s" %result)
        self.notify.debug("awardMgrResult = %s" %awardMgrResult)
        
        # We've received a response from the Uberdog, enable the code entry again.
        self.__enableCodeEntry()
        
        # Code Successfully Redeemed
        if (result == 0):
            self.resultPanel['image'] = self.resultPanelSuccessGui
            self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
            
        # Code is Invalid
        elif (result == 1 or result == 3):
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultInvalidCode
        
        # Code has expired    
        elif (result == 2):
            self.resultPanel['image'] = self.resultPanelFailureGui
            self.resultPanel['text'] = TTLocalizer.CdrResultExpiredCode
        
        # Code is correct, but something else went wrong. Check awardMgrResult.
        elif (result == 4):
            self.resultPanel['image'] = self.resultPanelErrorGui
            
            if (awardMgrResult == 0):
                self.resultPanel['text'] = TTLocalizer.CdrResultSuccess
                
            elif (awardMgrResult == 1 or awardMgrResult == 2 or awardMgrResult == 15 or awardMgrResult == 16):
                self.resultPanel['text'] = TTLocalizer.CdrResultUnknownError
                
            elif (awardMgrResult == 3 or awardMgrResult == 4):
                self.resultPanel['text'] = TTLocalizer.CdrResultMailboxFull
                
            elif (awardMgrResult == 5 or awardMgrResult == 10):
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInMailbox
            
            elif (awardMgrResult == 6 or awardMgrResult == 7 or awardMgrResult == 11):
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInQueue
                
            elif (awardMgrResult == 8):
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyInCloset
            
            elif (awardMgrResult == 9):
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyBeingWorn
                
            elif (awardMgrResult == 12 or awardMgrResult == 13 or awardMgrResult == 14):
                self.resultPanel['text'] = TTLocalizer.CdrResultAlreadyReceived
                
        elif (result == 5):
            # Too many failed attempts - Display correct error and disable the code entry and submit button.
            self.resultPanel['text'] = TTLocalizer.CdrResultTooManyFails
            self.__disableCodeEntry()
            
        elif (result == 6):
            # Service Unavailable.
            self.resultPanel['text'] = TTLocalizer.CdrResultServiceUnavailable
            self.__disableCodeEntry()
            
        # Play the success or failure sounds.
        if (result == 0):
            self.successSfx.play()
        else:
            self.failureSfx.play()
        
        self.resultPanel.show()
        
    def __hideResultPanel(self):
        """
        Purpose: To hide the Result Panel.
        Params: None
        Return: None
        """
        self.resultPanel.hide()

    def __disableCodeEntry(self):
        """
        Purpose: Disable the the code entry box and the submit button.
                 We'll disable it right after submitting a code, while waiting for
                 a result, and if the player has submitted too many invalid codes.
        Params: None
        Return: None
        """
        self.codeInput['state'] = DGG.DISABLED
        self.submitButton['state'] = DGG.DISABLED
        
    def __enableCodeEntry(self):
        """
        Purpose: Enable the the code entry box and the submit button.
                 We'll enable it right after the Uberdog gets back to us after
                 a code submit. This is to ensure that the 2nd code is not submitted
                 before the result from the 1st has arrived.
        Params: None
        Return: None
        """
        self.codeInput['state'] = DGG.NORMAL
        self.codeInput['focus'] = 1
        self.submitButton['state'] = DGG.NORMAL
        