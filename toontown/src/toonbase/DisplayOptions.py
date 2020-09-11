import copy
import string
import os
import sys
import datetime
from pandac.PandaModules import loadPrcFileData, Settings, WindowProperties
from otp.otpgui import OTPDialog
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from direct.directnotify import DirectNotifyGlobal

try:        
    import embedded
except:
    pass

class DisplayOptions:
    """A class stolen from Pirates so we can respect saved window settings when we get to Pick A Toon."""
    notify = DirectNotifyGlobal.directNotify.newCategory("DisplayOptions")
    
    def __init__(self):
        self.restore_failed = False
        #self.restrictToEmbedded(1, False)
        self.loadFromSettings()

    def loadFromSettings(self):
        """Read the saved settings."""
        Settings.readSettings()
        mode = not Settings.getWindowedMode()
        music = Settings.getMusic()
        sfx = Settings.getSfx()
        toonChatSounds = Settings.getToonChatSounds()
        musicVol = Settings.getMusicVolume()
        sfxVol = Settings.getSfxVolume()
        resList = [(640, 480),(800,600),(1024,768),(1280,1024),(1600,1200)] #copied from Resolution in settingsFile.h
        res = resList[Settings.getResolution()]
        embed = Settings.getEmbeddedMode()
        self.notify.debug("before prc settings embedded mode=%s" % str(embed))
        self.notify.debug("before prc settings full screen mode=%s" % str(mode)) 
        if mode == None:
            mode = 1
        if res == None:
            res = (800,600)

        loadPrcFileData("toonBase Settings Window Res", ("win-size %s %s" % (res[0], res[1])))
        self.notify.debug("settings resolution = %s" % str(res))
        loadPrcFileData("toonBase Settings Window FullScreen", ("fullscreen %s" % (mode)))
        self.notify.debug("settings full screen mode=%s" % str(mode))        
        loadPrcFileData("toonBase Settings Music Active", ("audio-music-active %s" % (music)))
        loadPrcFileData("toonBase Settings Sound Active", ("audio-sfx-active %s" % (sfx)))
        loadPrcFileData("toonBase Settings Music Volume", ("audio-master-music-volume %s" % (musicVol)))
        loadPrcFileData("toonBase Settings Sfx Volume", ("audio-master-sfx-volume %s" % (sfxVol)))
        loadPrcFileData("toonBase Settings Toon Chat Sounds", ("toon-chat-sounds %s" % (toonChatSounds)))
        self.settingsFullScreen = mode
        self.settingsWidth = res[0]
        self.settingsHeight = res[1]
        self.settingsEmbedded = embed
        self.notify.debug("settings embedded mode=%s" % str(self.settingsEmbedded))   

        self.notify.info("settingsFullScreen = %s, embedded = %s width=%d height=%d" %
                         (self.settingsFullScreen, self.settingsEmbedded,
                          self.settingsWidth, self.settingsHeight))
        # these settings test error recovery, as no one has a 16000 x 12000 monitor (yet)
        #self.settingsFullScreen = True
        #self.settingsWidth = 16000
        #self.settingsHeight = 12000
        
    def restrictToEmbedded(self, restrict, change_display = True):
        # to completely disable restrict to embedded, uncomment:
        #restrict = 0
 
        # if we are not running embedded, restricting to
        # embedded is not an option
        if base.appRunner is None or base.appRunner.windowProperties is None:
            restrict = 0

        self.restrict_to_embedded = choice(restrict, 1, 0)
        self.notify.debug("restrict_to_embedded: %s" % self.restrict_to_embedded)
            
        # window mode may have changed 
        if change_display:
            self.set( base.pipe, self.settingsWidth, self.settingsHeight,
                      self.settingsFullScreen, self.settingsEmbedded)

    def set(self, pipe, width, height, fullscreen, embedded):
        self.notify.debugStateCall(self)
        state = False
        
        self.notify.info("SET")

        #fullscreen = options.fullscreen_runtime
        #embedded = options.embedded_runtime
        if self.restrict_to_embedded:
            fullscreen = 0
            embedded = 1
            
        if embedded:
            if base.appRunner.windowProperties:
                width = base.appRunner.windowProperties.getXSize ()
                height = base.appRunner.windowProperties.getYSize ()

        self.current_pipe = base.pipe
        self.current_properties = WindowProperties(base.win.getProperties())

        properties = self.current_properties
        self.notify.debug("DISPLAY PREVIOUS:")
        self.notify.debug("  EMBEDDED:   %s" % bool(properties.getParentWindow ( )))
        self.notify.debug("  FULLSCREEN: %s" % bool(properties.getFullscreen ( )))
        self.notify.debug("  X SIZE:     %s" % properties.getXSize ( ))
        self.notify.debug("  Y SIZE:     %s" % properties.getYSize ( ))
        self.notify.debug("DISPLAY REQUESTED:")
        self.notify.debug("  EMBEDDED:   %s" % bool(embedded))
        self.notify.debug("  FULLSCREEN: %s" % bool(fullscreen))
        self.notify.debug("  X SIZE:     %s" % width)
        self.notify.debug("  Y SIZE:     %s" % height)

        if ((self.current_pipe == pipe) and \
            (bool(self.current_properties.getParentWindow( )) == bool(embedded)) and \
            (self.current_properties.getFullscreen ( ) == fullscreen) and \
            (self.current_properties.getXSize ( ) == width) and \
            (self.current_properties.getYSize ( ) == height)):
            # no display change required
            self.notify.info("DISPLAY NO CHANGE REQUIRED")
            state = True
        else:
            properties = WindowProperties()
            properties.setSize(width, height)
            properties.setFullscreen(fullscreen)
            properties.setParentWindow(0)

            if embedded:
                if base.appRunner.windowProperties:
                    properties = base.appRunner.windowProperties
            
            # get current sort order
            original_sort = base.win.getSort ( )
            
            if self.resetWindowProperties(pipe, properties):
                self.notify.debug("DISPLAY CHANGE SET")

                # verify display change
                properties = base.win.getProperties()

                self.notify.debug("DISPLAY ACHIEVED:")
                self.notify.debug("  EMBEDDED:   %s" % bool(properties.getParentWindow ( )))
                self.notify.debug("  FULLSCREEN: %s" % bool(properties.getFullscreen ( )))
                self.notify.debug("  X SIZE:     %s" % properties.getXSize ( ))
                self.notify.debug("  Y SIZE:     %s" % properties.getYSize ( ))

                if ((bool(properties.getParentWindow( )) == bool(embedded)) and \
                    (properties.getFullscreen ( ) == fullscreen) and \
                    (properties.getXSize ( ) == width) and \
                    (properties.getYSize ( ) == height)):
                    self.notify.info("DISPLAY CHANGE VERIFIED")
                    state = True
                else:
                    self.notify.warning("DISPLAY CHANGE FAILED, RESTORING PREVIOUS DISPLAY")
                    self.restoreWindowProperties () 
            else:
                self.notify.warning("DISPLAY CHANGE FAILED")
                self.notify.warning("DISPLAY SET - BEFORE RESTORE")
                self.restoreWindowProperties ()
                self.notify.warning("DISPLAY SET - AFTER RESTORE")

            # set current sort order
            base.win.setSort (original_sort)

            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
                
        return state

    def resetWindowProperties(self, pipe, properties):
        if base.win:
            currentProperties = WindowProperties(base.win.getProperties())
            gsg = base.win.getGsg()
        else:
            currentProperties = WindowProperties.getDefault()
            gsg = None

        # Check to see if the window properties will change in any
        # important way.
        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)

        if base.pipe != pipe:
            gsg = None

        if (gsg == None) or \
            (currentProperties.getFullscreen() != newProperties.getFullscreen()) or \
            (currentProperties.getParentWindow() != newProperties.getParentWindow()):
            # For now, assume that if we change fullscreen state, we
            # need to destroy the window and create a new one.

            self.notify.debug("window properties: %s" % properties)
            self.notify.debug("gsg: %s" % gsg)

            base.pipe = pipe
            if not base.openMainWindow(props = properties, gsg = gsg,
                                       keepCamera = True):
                self.notify.warning("OPEN MAIN WINDOW FAILED")
                return 0

            self.notify.info("OPEN MAIN WINDOW PASSED")

            base.graphicsEngine.openWindows()
            if base.win.isClosed():
                self.notify.warning("Window did not open, removing.")
                base.closeWindow(base.win)
                return 0

            base.disableShowbaseMouse()

            # If we've already imported (and therefore downloaded)
            # libotp.dll, then we already have a NametagGlobals, and
            # we should keep it up-to-date with the new MouseWatcher
            # etc.
            if 'libotp' in sys.modules:
                from libotp import NametagGlobals
                NametagGlobals.setCamera(base.cam)
                NametagGlobals.setMouseWatcher(base.mouseWatcherNode)

        else:
            # If the properties are changing only slightly
            # (e.g. window size), we can keep the current window and
            # just adjust its properties directly.
            self.notify.debug("Adjusting properties")
            base.win.requestProperties(properties)
            base.graphicsEngine.renderFrame()

        return 1

    def restoreWindowProperties (self):
        if (self.resetWindowProperties(self.current_pipe, self.current_properties)):
            self.restore_failed = False
        else:
            # Oops, we couldn't get the original settings back!
            self.notify.warning("Couldn't restore original display settings!")
            
            if base.appRunner and base.appRunner.windowProperties:
                # Try to go back into embedded.  That might help.
                fullscreen = 0
                embedded = 1
                tryProps = base.appRunner.windowProperties
                if (self.resetWindowProperties(self.current_pipe, tryProps)):
                    self.current_properties = copy.copy(tryProps)
                    self.restore_failed = False
                    return

            if self.current_properties.getFullscreen():
                # Try again without the fullscreen option.  That might
                # help.
                fullscreen = 0
                embedded = 0
                tryProps = self.current_properties
                tryProps.setFullscreen(0)
                if (self.resetWindowProperties(self.current_pipe, tryProps)):
                    self.current_properties = copy.copy(tryProps)
                    self.restore_failed = False
                    return

            # Couldn't even open a regular window.  This is kind of
            # like a low-level panic situation.
            self.notify.error("Failed opening regular window!")
            base.panda3dRenderError()
            self.restore_failed = True            
        return
