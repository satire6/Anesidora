from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.fsm import StateData
from direct.showbase import AppRunnerGlobal
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals

class DisplaySettingsDialog(DirectFrame, StateData.StateData):
    """DisplaySettingsDialog:

    This is a pop-up from the Options page that allows the user to
    change his or her screen resolutions, rendering API, etc.
    """

    ApplyTimeoutSeconds = 15
    TimeoutCountdownTask = "DisplaySettingsTimeoutCountdown"

    WindowedMode = 0
    FullscreenMode = 1
    EmbeddedMode = 2 # embedded inside the web browser

    notify = DirectNotifyGlobal.directNotify.newCategory("DisplaySettingsDialog")
    
    def __init__(self):
        """__init__(self)
        """
        DirectFrame.__init__(self,
                             pos = (0, 0, 0.30),
                             relief = None,
                             image = DGG.getDefaultDialogGeom(),
                             image_scale = (1.6, 1, 1.2),
                             image_pos = (0,0,-0.05),
                             image_color = ToontownGlobals.GlobalDialogColor,
                             text = TTLocalizer.DisplaySettingsTitle,
                             text_scale = 0.12,
                             text_pos = (0, 0.4),
                             borderWidth = (0.01, 0.01),
                             )
        StateData.StateData.__init__(self, "display-settings-done")
        self.setBin('gui-popup', 0)
        self.initialiseoptions(DisplaySettingsDialog)

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        DirectFrame.destroy(self)

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1

        self.anyChanged = 0
        self.apiChanged = 0
        self.screenSizes = ((640, 480),
                            (800, 600),
                            (1024, 768),
                            (1280, 1024),
                            (1600, 1200))

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        nameShopGui = loader.loadModel("phase_3/models/gui/nameshop_gui")
        circle = nameShopGui.find("**/namePanelCircle")

        # Make a copy of the circle so we can move it up a bit.
        innerCircle = circle.copyTo(hidden)
        innerCircle.setPos(0, 0, 0.2)

        # Also copy the circle to the frame itself, as a white
        # circular background behind the radio button circles (and a
        # black ring behind that).
        self.c1b = circle.copyTo(self, -1)
        self.c1b.setColor(0, 0, 0, 1)
        self.c1b.setPos(0.044, 0, -0.21)
        self.c1b.setScale(0.4)
        c1f = circle.copyTo(self.c1b)
        c1f.setColor(1, 1, 1, 1)
        c1f.setScale(0.8)
        self.c2b = circle.copyTo(self, -2)
        self.c2b.setColor(0, 0, 0, 1)
        self.c2b.setPos(0.044, 0, -0.30)
        self.c2b.setScale(0.4)
        c2f = circle.copyTo(self.c2b)
        c2f.setColor(1, 1, 1, 1)
        c2f.setScale(0.8)

        self.c3b = circle.copyTo(self, -2)
        self.c3b.setColor(0, 0, 0, 1)
        self.c3b.setPos(0.044, 0, -0.40)
        self.c3b.setScale(0.4)
        c3f = circle.copyTo(self.c3b)
        c3f.setColor(1, 1, 1, 1)
        c3f.setScale(0.8)        
        
        self.introText = DirectLabel(
            parent = self,
            relief = None,
            scale = TTLocalizer.DSDintroText,
            text = TTLocalizer.DisplaySettingsIntro,
            text_wordwrap = TTLocalizer.DSDintroTextwordwrap,
            text_align = TextNode.ALeft,
            pos = (-0.725, 0, 0.3),
            )
        
        self.introTextSimple = DirectLabel(
            parent = self,
            relief = None,
            scale = 0.06,
            text = TTLocalizer.DisplaySettingsIntroSimple,
            text_wordwrap = 25,
            text_align = TextNode.ALeft,
            pos = (-0.725, 0, 0.3),
            )

        self.apiLabel = DirectLabel(
            parent = self,
            relief = None,
            scale = 0.06,
            text = TTLocalizer.DisplaySettingsApi,
            text_align = TextNode.ARight,
            pos = (-0.08, 0, 0),
            )
        self.apiMenu = DirectOptionMenu(
            parent = self,
            relief = DGG.RAISED,
            scale = 0.06,
            items = ['x'],
            pos = (0, 0, 0),
            )
        
        self.screenSizeLabel = DirectLabel(
            parent = self,
            relief = None,
            scale = 0.06,
            text = TTLocalizer.DisplaySettingsResolution,
            text_align = TextNode.ARight,
            pos = (-0.08, 0, -0.10),
            )
        self.screenSizeLeftArrow = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/Horiz_Arrow_UP"),
                     gui.find("**/Horiz_Arrow_DN"),
                     gui.find("**/Horiz_Arrow_Rllvr"),
                     gui.find("**/Horiz_Arrow_UP"),
                     ),
            scale = (-1.0, 1.0, 1.0),  # make arrow point the other way
            pos = (0.04, 0, -0.085),
            command = self.__doScreenSizeLeft,
            )
        
        self.screenSizeRightArrow = DirectButton(
            parent = self,
            relief = None,
            image = (gui.find("**/Horiz_Arrow_UP"),
                     gui.find("**/Horiz_Arrow_DN"),
                     gui.find("**/Horiz_Arrow_Rllvr"),
                     gui.find("**/Horiz_Arrow_UP"),
                     ),
            pos = (0.54, 0, -0.085),
            command = self.__doScreenSizeRight,
            )
        
        self.screenSizeValueText = DirectLabel(
            parent = self,
            relief = None,
            text = "x",
            text_align = TextNode.ACenter,
            text_scale = 0.06,
            pos = (0.29, 0, -0.10),
            )

        self.windowedButton = DirectCheckButton(
            parent = self,
            relief = None,
            text = TTLocalizer.DisplaySettingsWindowed,
            text_align = TextNode.ALeft,
            text_scale = 0.6,
            scale = 0.1,
            boxImage = innerCircle,
            boxImageScale = 2.5,
            boxImageColor = VBase4(0, 0.25, 0.5, 1),
            boxRelief = None,
            pos = TTLocalizer.DSDwindowedButtonPos,
            command = self.__doWindowed,
            )

        self.fullscreenButton = DirectCheckButton(
            parent = self,
            relief = None,
            text = TTLocalizer.DisplaySettingsFullscreen,
            text_align = TextNode.ALeft,
            text_scale = 0.6,
            scale = 0.1,
            boxImage = innerCircle,
            boxImageScale = 2.5,
            boxImageColor = VBase4(0, 0.25, 0.5, 1),
            boxRelief = None,
            pos = TTLocalizer.DSDfullscreenButtonPos,
            command = self.__doFullscreen,
            )

        self.embeddedButton = DirectCheckButton(
            parent = self,
            relief = None,
            text = TTLocalizer.DisplaySettingsEmbedded,
            text_align = TextNode.ALeft,
            text_scale = 0.6,
            scale = 0.1,
            boxImage = innerCircle,
            boxImageScale = 2.5,
            boxImageColor = VBase4(0, 0.25, 0.5, 1),
            boxRelief = None,
            pos = TTLocalizer.DSDembeddedButtonPos,
            command = self.__doEmbedded,
            )        

        self.apply = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (0.6,1,1),
            text = TTLocalizer.DisplaySettingsApply,
            text_scale = 0.06,
            text_pos = (0,-0.02),
            pos = (0.52, 0, -0.53),
            command = self.__apply,
            )

        self.cancel = DirectButton(
            parent = self,
            relief = None,
            text = TTLocalizer.DisplaySettingsCancel,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = (0.6,1,1),
            text_scale = TTLocalizer.DSDcancel,
            text_pos = (TTLocalizer.DSDcancelButtonPositionX,-0.02),
            pos = (0.20, 0, -0.53),
            command = self.__cancel,
            )

        guiButton.removeNode()
        gui.removeNode()
        nameShopGui.removeNode()
        innerCircle.removeNode()

        self.hide()

    def enter(self, changeDisplaySettings, changeDisplayAPI):
        """enter(self, changeDisplaySettings)
        if changeDisplaySettings is false, only the resolution may be
        changed.
        """
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        # Use isLoaded to avoid redundant loading
        if self.isLoaded == 0:
            self.load()

        self.applyDialog = None
        self.timeoutDialog = None
        self.restoreDialog = None
        self.revertDialog = None
        base.transitions.fadeScreen(.5)

        properties = base.win.getProperties()

        self.screenSizeIndex = self.chooseClosestScreenSize(
            properties.getXSize(), properties.getYSize())
        self.isFullscreen = properties.getFullscreen()

        # at this point we need to figure out correct display mode
        # TODO check if we are embedded
        if self.isCurrentlyEmbedded(): # check if embedded
            self.displayMode = self.EmbeddedMode
            pass
        elif self.isFullscreen:
            self.displayMode = self.FullscreenMode
        else:
            self.displayMode = self.WindowedMode

        self.updateApiMenu(changeDisplaySettings, changeDisplayAPI)
        self.updateWindowed()
        self.updateScreenSize()

        if changeDisplaySettings:
            self.introText.show()
            self.introTextSimple.hide()
            if (changeDisplayAPI and (len(self.apis) > 1)):
                self.apiLabel.show()
                self.apiMenu.show()
            else:
                self.apiLabel.hide()
                self.apiMenu.hide()
            self.windowedButton.show()
            self.fullscreenButton.show()
            self.c1b.show()
            self.c2b.show()
            if self.isEmbeddedPossible():
                self.c3b.show()
                self.embeddedButton.show()
            else:
                self.c3b.hide()
                self.embeddedButton.hide()
        else:
            self.introText.hide()
            self.introTextSimple.show()
            self.apiLabel.hide()
            self.apiMenu.hide()
            self.windowedButton.hide()
            self.fullscreenButton.hide()
            self.c1b.hide()
            self.c2b.hide()
            self.c3b.hide()

        # Mark whether the user has made any changes since enter().
        self.anyChanged = 0
        self.apiChanged = 0

        self.show()
        return

    def exit(self):
        """exit(self)
        """
        if self.isEntered == 0:
            return None
        self.isEntered = 0

        self.cleanupDialogs()
        base.transitions.noTransitions()

        taskMgr.remove(self.TimeoutCountdownTask)
        self.ignoreAll()
        self.hide()

        messenger.send(self.doneEvent, [self.anyChanged, self.apiChanged])
        return

    def cleanupDialogs(self):
        if self.applyDialog != None:
            self.applyDialog.cleanup()
            self.applyDialog = None

        if self.timeoutDialog != None:
            self.timeoutDialog.cleanup()
            self.timeoutDialog = None

        if self.restoreDialog != None:
            self.restoreDialog.cleanup()
            self.restoreDialog = None

        if self.revertDialog != None:
            self.revertDialog.cleanup()
            self.revertDialog = None

    def updateApiMenu(self, changeDisplaySettings, changeDisplayAPI):
        # Get all of the available graphics pipes up front.
        self.apis = []
        self.apiPipes = []
        # Only make the pipes if we are allowed to change APIs
        if changeDisplayAPI:
            base.makeAllPipes()
        for pipe in base.pipeList:
            if pipe.isValid():
                self.apiPipes.append(pipe)
                self.apis.append(pipe.getInterfaceName())

        self.apiMenu['items'] = self.apis
        self.apiMenu.set(base.pipe.getInterfaceName())

    def updateWindowed(self):
        if self.displayMode == self.FullscreenMode:
            self.windowedButton['indicatorValue'] = 0
            self.fullscreenButton['indicatorValue'] = 1
            self.embeddedButton['indicatorValue'] = 0
        elif self.displayMode == self.WindowedMode:
            self.windowedButton['indicatorValue'] = 1
            self.fullscreenButton['indicatorValue'] = 0
            self.embeddedButton['indicatorValue'] = 0
        elif self.displayMode == self.EmbeddedMode:
            self.windowedButton['indicatorValue'] = 0
            self.fullscreenButton['indicatorValue'] = 0
            self.embeddedButton['indicatorValue'] = 1
            

    def updateScreenSize(self):
        xSize, ySize = self.screenSizes[self.screenSizeIndex]
        self.screenSizeValueText['text'] = '%s x %s' % (xSize, ySize)
        if self.screenSizeIndex > 0:
            self.screenSizeLeftArrow.show()
        else:
            self.screenSizeLeftArrow.hide()
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeRightArrow.show()
        else:
            self.screenSizeRightArrow.hide()

    def chooseClosestScreenSize(self, currentXSize, currentYSize):
        # First, look for an exact match.
        for i in range(len(self.screenSizes)):
            xSize, ySize = self.screenSizes[i]
            if currentXSize == xSize and currentYSize == ySize:
                return i

        # Failing that, look for the nearest match in total pixel
        # count.
        currentCount = currentXSize * currentYSize
        bestDiff = None
        bestI = None
        for i in range(len(self.screenSizes)):
            xSize, ySize = self.screenSizes[i]
            diff = abs(xSize * ySize - currentCount)
            if bestI == None or diff < bestDiff:
                bestI = i
                bestDiff = diff

        return bestI

    def __doWindowed(self, value):
        self.displayMode = self.WindowedMode
        self.updateWindowed()

    def __doFullscreen(self, value):
        self.displayMode = self.FullscreenMode 
        self.updateWindowed()

    def __doEmbedded(self,value):
        """Change the cur settings embedded mode."""
        self.displayMode = self.EmbeddedMode
        self.updateWindowed()

    def __doScreenSizeLeft(self):
        if self.screenSizeIndex > 0:
            self.screenSizeIndex = self.screenSizeIndex - 1
            self.updateScreenSize()

    def __doScreenSizeRight(self):
        if self.screenSizeIndex < len(self.screenSizes) - 1:
            self.screenSizeIndex = self.screenSizeIndex + 1
            self.updateScreenSize()

    def __apply(self):
        self.cleanupDialogs()

        # Move our dialog under the fade screen.
        self.clearBin()
            
        self.applyDialog = TTDialog.TTDialog(
            dialogName = 'DisplaySettingsApply',
            style = TTDialog.TwoChoice,
            text = TTLocalizer.DisplaySettingsApplyWarning % (self.ApplyTimeoutSeconds),
            text_wordwrap = 15,
            command = self.__applyDone,
            )
        self.applyDialog.setBin('gui-popup', 0)

    def __applyDone(self, command):
        self.applyDialog.cleanup()
        self.applyDialog = None

        # Restore our dialog to the top of the fade screen.
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(.5)

        if command != DGG.DIALOG_OK:
            return

        # Now apply the new settings.
        self.origPipe = base.pipe
        self.origProperties = base.win.getProperties()

        pipe = self.apiPipes[self.apiMenu.selectedIndex]
        properties = WindowProperties()
        xSize, ySize = self.screenSizes[self.screenSizeIndex]
        properties.setSize(xSize, ySize)
        properties.setFullscreen(self.displayMode == self.FullscreenMode)
        fullscreen = self.displayMode == self.FullscreenMode
        embedded = self.displayMode == self.EmbeddedMode
        if embedded:
            if self.isEmbeddedPossible():
                # yeah you can go embedded
                pass
            else:
                self.notify.warning("how was the player able to choose embedded")
                embedded = False
        #if not self.resetDisplayProperties(pipe, properties):
        if not self.changeDisplayProperties(pipe, xSize, ySize, fullscreen, embedded):
            # If we couldn't open the window, go back without
            # bothering to prompt the user.
            self.__revertBack(1)
            return

        # And pop up a dialog giving the user a chance to acknowledge
        # that the new settings worked.

        # Move our dialog back under the fade screen.
        self.clearBin();
        
        self.timeoutDialog = TTDialog.TTDialog(
            dialogName = 'DisplaySettingsTimeout',
            style = TTDialog.TwoChoice,
            text = TTLocalizer.DisplaySettingsAccept % (self.ApplyTimeoutSeconds),
            text_wordwrap = 15,
            command = self.__timeoutDone
            )
        self.timeoutDialog.setBin('gui-popup', 0)
        self.timeoutRemaining = self.ApplyTimeoutSeconds
        self.timeoutStart = None
        taskMgr.add(self.__timeoutCountdown, self.TimeoutCountdownTask)

    def changeDisplayProperties(self, pipe, width, height, fullscreen = False, embedded = False):
        """Do some processing before we call resetDisplayProperties."""
        result = False
        self.notify.info("changeDisplayProperties")
        if embedded:
            if self.isEmbeddedPossible():
                width = base.appRunner.windowProperties.getXSize()
                height = base.appRunner.windowProperties.getYSize()
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
                properties = base.appRunner.windowProperties
            
            # get current sort order
            original_sort = base.win.getSort ( )
            
            if self.resetDisplayProperties(pipe, properties):
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
                    result = True
                else:
                    self.notify.warning("DISPLAY CHANGE FAILED, RESTORING PREVIOUS DISPLAY")
                    #self.restoreWindowProperties ( options )
            else:
                self.notify.warning("DISPLAY CHANGE FAILED")
                #self.notify.warning("DISPLAY SET - BEFORE RESTORE")
                #self.restoreWindowProperties ( options )
                #self.notify.warning("DISPLAY SET - AFTER RESTORE")

            # set current sort order
            base.win.setSort (original_sort)

            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()
                
        return result
    

    def __timeoutCountdown(self, task):
        # This task monitors the countdown timer for accepting the new
        # display settings.

        # Reset the time we started to the first time this task runs.
        # We do it this way, instead of setting it when we spawn the
        # task, to ensure we don't start counting until after the new
        # window is created.
        if self.timeoutStart == None:
            self.timeoutStart = globalClock.getRealTime()
        elapsed = int(globalClock.getFrameTime() - self.timeoutStart)
        remaining = max(self.ApplyTimeoutSeconds - elapsed, 0)
        if remaining < self.timeoutRemaining:
            self.timeoutRemaining = remaining
            self.timeoutDialog['text'] = TTLocalizer.DisplaySettingsAccept % (remaining),
        if remaining == 0:
            # Automatically cancel when the time is up.
            self.__timeoutDone('cancel')
            return Task.done
        return Task.cont

    def __timeoutDone(self, command):
        taskMgr.remove(self.TimeoutCountdownTask)

        self.timeoutDialog.cleanup()
        self.timeoutDialog = None

        # Restore our dialog to the top of the fade screen.
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(.5)

        if command == DGG.DIALOG_OK:
            # An 'ok' means we're happy with the new settings.
            self.anyChanged = 1
            self.exit()
            return

        # A cancel or timeout means we want the old settings back.
        self.__revertBack(0)
        return

    def __revertBack(self, reason):
        # Reason code:
        #  0 - user cancelled.  No explanation needed.
        #  1 - pipe just didn't work.
        # First, restore the original display settings.
        if not self.resetDisplayProperties(self.origPipe, self.origProperties):
            # Oops, we couldn't get the original settings back!
            self.notify.warning("Couldn't restore original display settings!")
            # This is kind of like a low-level panic situation.
            base.panda3dRenderError()

        # Now open a dialog telling the user they've been restored.
        
        # Move our dialog under the fade screen.
        self.clearBin()

        if reason == 0:
            revertText = TTLocalizer.DisplaySettingsRevertUser
        else:
            revertText = TTLocalizer.DisplaySettingsRevertFailed
            
        self.revertDialog = TTDialog.TTDialog(
            dialogName = 'DisplaySettingsRevert',
            style = TTDialog.Acknowledge,
            text = revertText,
            text_wordwrap = 15,
            command = self.__revertDone,
            )
        self.revertDialog.setBin('gui-popup', 0)

    def __revertDone(self, command):
        self.revertDialog.cleanup()
        self.revertDialog = None

        # Restore our dialog to the top of the fade screen.
        self.setBin('gui-popup', 0)
        base.transitions.fadeScreen(.5)

        return

    def __cancel(self):
        self.exit()
    
    def resetDisplayProperties(self, pipe, properties):
        if base.win:
            currentProperties = base.win.getProperties()
            gsg = base.win.getGsg()
        else:
            currentProperties = WindowProperties.getDefault()
            gsg = None

        # Check to see if the window properties will change in any
        # important way.
        newProperties = WindowProperties(currentProperties)
        newProperties.addProperties(properties)

        if base.pipe != pipe:
            self.apiChanged = 1
            gsg = None

        if gsg == None or \
           currentProperties.getFullscreen() != newProperties.getFullscreen() or \
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
            
            base.disableShowbaseMouse()
            NametagGlobals.setCamera(base.cam)
            NametagGlobals.setMouseWatcher(base.mouseWatcherNode)

            # Force a frame to render for good measure.  This should
            # force the window open right now, which helps us avoid
            # starting the countdown timer before the window is open.
            # Also, we can check to see if the window actually opened
            # or not.
            base.graphicsEngine.renderFrame()
            base.graphicsEngine.renderFrame()

            base.graphicsEngine.openWindows()
            if base.win.isClosed():
                self.notify.info("Window did not open, removing.")
                base.closeWindow(base.win)
                return 0
                
        else:
            # If the properties are changing only slightly
            # (e.g. window size), we can keep the current window and
            # just adjust its properties directly.
            self.notify.debug("Adjusting properties")
            base.win.requestProperties(properties)
            base.graphicsEngine.renderFrame()
            
        return 1

    def isEmbeddedPossible(self):
        """Returns True if embedded in the browser is a valid option."""
        result = False
        # RAU per Robin we don't want embedded, uncomment if they change their minds
        #if base.appRunner and base.appRunner.windowProperties:
        #    result = True
        return result
    
    def isCurrentlyEmbedded(self):
        """Returns true if the current game window is inside a browser."""
        result = False
        if base.win.getProperties().getParentWindow():
            result = True
        return result
        
