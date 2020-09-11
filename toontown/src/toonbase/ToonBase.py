"""ToonBase module: contains the ToonBase class"""

#from ShowBaseGlobal import *
from otp.otpbase import OTPBase
from otp.otpbase import OTPLauncherGlobals
from direct.showbase.PythonUtil import *
import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import ToontownLoader
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import sys
import os
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from toontown.launcher import ToontownDownloadWatcher


class ToonBase(OTPBase.OTPBase):
    """ToonBase class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("ToonBase")

    # special methods
    
    def __init__(self):
        """__init__(self)
        ToonBase constructor: create a toon and launch it into the world
        """
        if not config.GetInt('ignore-user-options',0):
            Settings.readSettings()
            mode = not Settings.getWindowedMode()
            music = Settings.getMusic()
            sfx = Settings.getSfx()
            toonChatSounds = Settings.getToonChatSounds()
            musicVol = Settings.getMusicVolume()
            sfxVol = Settings.getSfxVolume()
            resList = [(640, 480),(800,600),(1024,768),(1280,1024),(1600,1200)] #copied from Resolution in settingsFile.h
            res = resList[Settings.getResolution()]
            
            if mode == None:
                mode = 1
            if res == None:
                res = (800,600)
            
            loadPrcFileData("toonBase Settings Window Res", ("win-size %s %s" % (res[0], res[1])))
            loadPrcFileData("toonBase Settings Window FullScreen", ("fullscreen %s" % (mode)))
            loadPrcFileData("toonBase Settings Music Active", ("audio-music-active %s" % (music)))
            loadPrcFileData("toonBase Settings Sound Active", ("audio-sfx-active %s" % (sfx)))
            loadPrcFileData("toonBase Settings Music Volume", ("audio-master-music-volume %s" % (musicVol)))
            loadPrcFileData("toonBase Settings Sfx Volume", ("audio-master-sfx-volume %s" % (sfxVol)))
            loadPrcFileData("toonBase Settings Toon Chat Sounds", ("toon-chat-sounds %s" % (toonChatSounds)))
                        
        OTPBase.OTPBase.__init__(self)        

        if not self.isMainWindowOpen():
            try:
                # For toontown, it is possible that window open failed
                # because of a graphics card issue. In that case, take
                # user to the appropriate page.
                launcher.setPandaErrorCode(7)
            except:
                pass
            sys.exit(1)
            
        self.disableShowbaseMouse()

        self.toonChatSounds = self.config.GetBool('toon-chat-sounds', 1)

        # Toontown doesn't care about dynamic shadows for now.
        self.wantDynamicShadows = 0
        # this is temporary until we pull in the new launcher code in production
        self.exitErrorCode = 0
        
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setFov(ToontownGlobals.DefaultCameraFov)
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear,
                                ToontownGlobals.DefaultCameraFar)

        # Music should be a bit quieter in toontown
        self.musicManager.setVolume(0.65)

        # Set the default background color.
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)

        # Set up the default colors of the IME candidate strings.
        tpm = TextPropertiesManager.getGlobalPtr()
        candidateActive = TextProperties()
        candidateActive.setTextColor(0, 0, 1, 1)
        tpm.setProperties('candidate_active', candidateActive)
        candidateInactive = TextProperties()
        candidateInactive.setTextColor(0.3, 0.3, 0.7, 1)
        tpm.setProperties('candidate_inactive', candidateInactive)        

        # set the showbase iris and fade models to point to
        # models in the ttmodels tree
        self.transitions.IrisModelName = "phase_3/models/misc/iris"
        self.transitions.FadeModelName = "phase_3/models/misc/fade"

        # When the user closes the main window, we want to get a
        # chance to shut down cleanly.
        self.exitFunc = self.userExit

        # Now that we've got the exit hook set, we can set error code
        # 11, indicating an abnormal termination.  If the user exits
        # via alt-F4, that will reset the error code to 0 before
        # exiting; if we get a Python exception, that will reset the
        # error code to 12.  But if we terminate for any other reason
        # without giving Python a chance to catch the error, it will
        # remain exit code 11: sudden death without Python cleanup.
        if __builtins__.has_key("launcher") and launcher:
            launcher.setPandaErrorCode(11)
        
        # Set our max dt so avatars with a low frame rate will
        # not pop through collision walls

        # Actually, we don't need such a low value these days, now
        # that collisions are better behaved; and setting this number
        # too low is frustrating for users with a poor frame rate.
        # 1.0 seems to be large enough to ease that frustration, while
        # small enough to prevent us from careening through space
        # during a particularly big chug.

        # On second thought, Dave Schuyler argues that we should have
        # a lower value now to prevent the various physics integrators
        # from blowing up.  And besides, there are still some
        # collision holes in the world.  So we compromise with 0.2 for
        # now.
        globalClock.setMaxDt(0.2)

        # Enable particles if desired
        if (self.config.GetBool('want-particles', 1) == 1):
            self.notify.debug('Enabling particles')
            self.enableParticles()

        # Turn off screen clear (enable this when there are not any
        # cracks left in the world)
        # self.win.getGsg().enableFrameClear(0, 1)

        # Accept the screenshot key
        self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)

        # If panda throws a panic event, we know we're not rendering
        # properly; send the user to the appropriate web page.
        self.accept('panda3d-render-error', self.panda3dRenderError)

        # make a ToontownLoader. Overwrite the ShowBase one.
        oldLoader = self.loader
        self.loader = ToontownLoader.ToontownLoader(self)
        __builtins__["loader"] = self.loader
        oldLoader.destroy()

        # Handle Alt-tab notification from gsg
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        
        self.friendMode = self.config.GetBool("switchboard-friends", 0)
        self.wantPets = self.config.GetBool('want-pets', 1)
        self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
        self.wantKarts = self.config.GetBool('want-karts', 1)
        self.wantNewSpecies = self.config.GetBool('want-new-species', 0)

        # tell panda to ignore repeated key presses
        self.inactivityTimeout = self.config.GetFloat("inactivity-timeout", ToontownGlobals.KeyboardTimeout)
        if self.inactivityTimeout:
            self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
            self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
            
        # minigame debug flags
        self.randomMinigameAbort = self.config.GetBool(
            'random-minigame-abort', 0)
        self.randomMinigameDisconnect = self.config.GetBool(
            'random-minigame-disconnect', 0)
        self.randomMinigameNetworkPlugPull = self.config.GetBool(
            'random-minigame-netplugpull', 0)
        self.autoPlayAgain = self.config.GetBool(
            'auto-play-again', 0)
        self.skipMinigameReward = self.config.GetBool(
            'skip-minigame-reward', 0)
        self.wantMinigameDifficulty = self.config.GetBool(
            'want-minigame-difficulty', 0)

        self.minigameDifficulty = self.config.GetFloat(
            'minigame-difficulty', -1.)
        if self.minigameDifficulty == -1.:
            del self.minigameDifficulty
        self.minigameSafezoneId = self.config.GetInt(
            'minigame-safezone-id', -1)
        if self.minigameSafezoneId == -1:
            del self.minigameSafezoneId

        ToontownBattleGlobals.SkipMovie = self.config.GetBool(
            'skip-battle-movies', 0)

        # this must be retrieved as an int (and not a bool) so
        # that we can detect the absence of this config var; if
        # we get it as a bool, our default value of -1 is
        # converted to a 1.
        self.creditCardUpFront = self.config.GetInt(
            'credit-card-up-front', -1)
        if self.creditCardUpFront == -1:
            del self.creditCardUpFront
        else:
            # convert to a bool
            self.creditCardUpFront = (self.creditCardUpFront != 0)
        
        # housing
        self.housingEnabled = self.config.GetBool(
            'want-housing', 1)

        # cannons
        self.cannonsEnabled = self.config.GetBool(
            'estate-cannons', 0)

        # firework cannons
        self.fireworksEnabled = self.config.GetBool(
            'estate-fireworks', 0)

        # day/night in estates
        self.dayNightEnabled = self.config.GetBool(
            'estate-day-night', 0)

        # cloud platforms in estates
        self.cloudPlatformsEnabled = self.config.GetBool(
            'estate-clouds', 0)
            
        # greySpacing Allowed?
        self.greySpacing = self.config.GetBool(
            'allow-greyspacing', 0)

        self.goonsEnabled = self.config.GetBool(
            'estate-goon', 0)

        self.restrictTrialers = self.config.GetBool(
            'restrict-trialers', 1)

        self.roamingTrialers = self.config.GetBool(
            'roaming-trialers', 1)

        self.slowQuietZone = self.config.GetBool(
            'slow-quiet-zone', 0)
        self.slowQuietZoneDelay = self.config.GetFloat(
            'slow-quiet-zone-delay', 5)

        self.killInterestResponse = self.config.GetBool(
            'kill-interest-response', 0)
        
        #whitelist text styles        
        tpMgr = TextPropertiesManager.getGlobalPtr()
        
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.3)
        
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0,0.0,0.0,1)
        
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        
        del tpMgr
            
        self.lastScreenShotTime = globalClock.getRealTime()
        self.accept('InputState-forward', self.__walking)
        self.canScreenShot = 1
        self.glitchCount = 0
        self.walking = 0

        self.resetMusic = self.loadMusic("phase_3/audio/bgm/MIDI_Events_16channels.mid")

    def disableShowbaseMouse(self):
        # Hack:
        # Enable drive mode but turn it off, and reset the camera
        # This is here because ShowBase sets up a drive interface, this
        # can be removed if ShowBase is changed to not set that up.
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface:
            self.mouseInterface.reparentTo(self.dataUnused)
        if base.mouse2cam:
            self.mouse2cam.reparentTo(self.dataUnused)
        # end of hack.
        
    def __walking(self, pressed):
        self.walking = pressed
        

    def takeScreenShot(self):
        namePrefix = 'screenshot'
        namePrefix = launcher.logPrefix + namePrefix
            
        #requires that you have at least 1 second between shots
        timedif = globalClock.getRealTime() - self.lastScreenShotTime  
        if self.glitchCount > 10 and self.walking:
            return
        if timedif < 1.0 and self.walking:
            self.glitchCount += 1
            return
        if not hasattr(self, "localAvatar"):
            self.screenshot(namePrefix = namePrefix)
            self.lastScreenShotTime = globalClock.getRealTime()
            return
        coordOnScreen = self.config.GetBool('screenshot-coords', 0)

        # avoid problems where the toon can run through collision barriers
        # if they hold down arrow_up while saving screenshots because
        # scrnshot saves take so long.
        self.localAvatar.stopThisFrame=1

        ctext = self.localAvatar.getAvPosStr()

        self.screenshotStr = ''
        messenger.send('takingScreenshot')

        if coordOnScreen:
            # add coord text to lower left corner so our user's bug report
            # screenshots contain better info
            coordTextLabel = DirectLabel(
                pos = (-0.81,0.001,-0.87),
                text = ctext,
                text_scale = 0.05, 
                text_fg = VBase4(1.0,1.0,1.0,1.0),
                text_bg = (0,0,0,0),
                text_shadow = (0,0,0,1),
                relief = None)
            # make sure it appears in front of arrows and other gui items
            coordTextLabel.setBin("gui-popup",0)
            strTextLabel = None
            if len(self.screenshotStr):
                strTextLabel = DirectLabel(
                    pos = (0.,0.001,0.9),
                    text = self.screenshotStr,
                    text_scale = 0.05, 
                    text_fg = VBase4(1.0,1.0,1.0,1.0),
                    text_bg = (0,0,0,0),
                    text_shadow = (0,0,0,1),
                    relief = None)
                # make sure it appears in front of arrows and other gui items
                strTextLabel.setBin("gui-popup",0)

        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix = namePrefix,
                        imageComment = ctext+' '+self.screenshotStr)
        self.lastScreenShotTime = globalClock.getRealTime()

        if coordOnScreen:
            if strTextLabel is not None:
                strTextLabel.destroy()
            coordTextLabel.destroy()

    def addScreenshotString(self, str):
        if len(self.screenshotStr):
            self.screenshotStr += '\n'
        self.screenshotStr += str

    def initNametagGlobals(self):
        """
        Should be called once during startup to initialize a few
        defaults for the Nametags.
        """

        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox'))
        thought3d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModelNode('phase_3/models/props/chatbox_noarrow'))

        chatButtonGui = loader.loadModel("phase_3/models/gui/chat_button_gui")

        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find("**/Horiz_Arrow_UP"))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find("**/Horiz_Arrow_DN"))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find("**/Horiz_Arrow_Rllvr"))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find("**/CloseBtn_UP"))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find("**/CloseBtn_DN"))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find("**/CloseBtn_Rllvr"))

        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        
        # For now, we'll leave the Toon at the same point as the
        # camera.  When we have a real toon later, we'll change it.
        NametagGlobals.setToon(self.cam)

        # We need a node to be the parent of all of the 2-d onscreen
        # messages along the margins.  This should be in front of many
        # things, but not all things.
        self.marginManager = MarginManager()
        self.margins = \
          self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)

        # And define a bunch of cells along the margins.
        mm = self.marginManager
        self.leftCells = [
            mm.addGridCell(0, 1, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 2, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(0, 3, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)
            ]
        self.bottomCells = [
            mm.addGridCell(0.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(1.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(2.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(3.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(4.5, 0, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)
            ]
        self.rightCells = [
            mm.addGridCell(5, 2, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop),
            mm.addGridCell(5, 1, base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop)
            ]

    def setCellsAvailable(self, cell_list, available):
        """setCellsAvailable(self, cell_list, bool available)

        Activates (if available is true) or deactivates (if available
        is false) a list of cells that are to be used for displaying
        margin popups, like red arrows and offscreen chat messages.

        This can be called from time to time to free up real estate
        along the edges of the screen when necessary for special
        purposes.

        cell_list should be a list of cell index numbers.  Suitable
        values are base.leftCells, base.bottomCells, or
        base.rightCells.
        """
        for cell in cell_list:
            self.marginManager.setCellAvailable(cell, available)

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        self.downloadWatcher = None

    def startShow(self, cr, launcherServer=None):
        self.cr = cr
        # force the screen to update
        base.graphicsEngine.renderFrame()

        self.downloadWatcher = ToontownDownloadWatcher.ToontownDownloadWatcher(TTLocalizer.LauncherPhaseNames)
        if launcher.isDownloadComplete():
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce("launcherAllPhasesComplete", self.cleanupDownloadWatcher)
        # Find the right server
        gameServer = base.config.GetString("game-server", "")
        if gameServer:
            self.notify.info("Using game-server from Configrc: %s " % (gameServer))
        elif launcherServer:
            gameServer = launcherServer
            self.notify.info("Using gameServer from launcher: %s " % (gameServer))
        else:
            gameServer = 'localhost'

        serverPort = base.config.GetInt("server-port", 6667)

        # The gameServer string will be a semicolon-separated list of
        # URL's.
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            # Insist on a secure (SSL-wrapped) connection, regardless
            # of what was requested.
            url.setScheme('s')
            if not url.hasPort():
                url.setPort(serverPort)
            serverList.append(url)

        if len(serverList) == 1:
            # If the gameServer list has only one element in it, check
            # for a failover port.  This is a holdover from the old
            # way of doing it, from before we could support multiple
            # gameservers on the launcher command line.  Once this
            # code has been published and the startup scripts modified
            # appropriately, we can remove this code.
            
            failover = base.config.GetString("server-failover", "")
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)
            
        # Connect to the server
        cr.loginFSM.request("connect", [serverList])
        
    def removeGlitchMessage(self):
        self.ignore('InputState-forward')
        print("ignoring InputState-forward")
        

    def exitShow(self, errorCode = None):
        self.notify.info("Exiting Toontown: errorCode = %s" % errorCode)
        if errorCode:
            # tell the activeX control we exited cleanly
            launcher.setPandaErrorCode(errorCode)
        else:
            # tell the activeX control we exited cleanly
            launcher.setPandaErrorCode(0)
        sys.exit()

    # this is temporary until we pull in the new launcher code in production
    def setExitErrorCode(self, code):
        self.exitErrorCode = code
        if os.name == 'nt':
            exitCode2exitPage = {
                OTPLauncherGlobals.ExitEnableChat: "chat",
                OTPLauncherGlobals.ExitSetParentPassword: "setparentpassword",
                OTPLauncherGlobals.ExitPurchase: "purchase",
                }
            if code in exitCode2exitPage:
                launcher.setRegistry("EXIT_PAGE", exitCode2exitPage[code])
    def getExitErrorCode(self):
        return self.exitErrorCode

    # this is called when the user presses Alt+F4 (closes the window)
    def userExit(self):
        # The user has just closed the main window; we should shut
        # down as cleanly as possible, without taking overly long
        # about it.

        # It's nice if the rest of the world sees our toon teleport
        # out (if we have a toon).
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass

        # Tell the AI (if we have one) why we're going down.
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)

        # in case the user has started logging out through the book, reset this flag
        # to indicate that they have forcibly closed the window and will not be going
        # back into the game.
        base.cr._userLoggingOut = False
        # make sure to get rid of all the DistributedObjects before tearing down
        # the playgame/login FSMs
        try: 
            localAvatar
        except:
            pass
        else:
            messenger.send('clientLogout')
            self.cr.dumpAllSubShardObjects()
        
        self.cr.loginFSM.request("shutdown")

        # If that returned, it didn't stick.  No problem.
        self.notify.warning("Could not request shutdown; exiting anyway.")
        self.exitShow()

    def panda3dRenderError(self):
        # The low-level graphics API has thrown an event indicating
        # that something's fubar down there, so we should just give up
        # and boot the user to the appropriate web page.

        launcher.setPandaErrorCode(14)
            
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)

        # Disconnect cleanly from the server
        self.cr.sendDisconnect()
        sys.exit()

    def getShardPopLimits(self):
        # returns (low, mid, high)
        if self.cr.productName == "JP":
            return (config.GetInt("shard-low-pop", ToontownGlobals.LOW_POP_JP),
                    config.GetInt("shard-mid-pop", ToontownGlobals.MID_POP_JP),
                    config.GetInt("shard-high-pop", ToontownGlobals.HIGH_POP_JP),)
        elif self.cr.productName in ["BR", "FR"]:
            return (config.GetInt("shard-low-pop", ToontownGlobals.LOW_POP_INTL),
                    config.GetInt("shard-mid-pop", ToontownGlobals.MID_POP_INTL),
                    config.GetInt("shard-high-pop", ToontownGlobals.HIGH_POP_INTL),)
        else:
            return (config.GetInt("shard-low-pop", ToontownGlobals.LOW_POP),
                    config.GetInt("shard-mid-pop", ToontownGlobals.MID_POP),
                    config.GetInt("shard-high-pop", ToontownGlobals.HIGH_POP),)

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        # play the reset midi file to kill stuck notes
        OTPBase.OTPBase.playMusic(self, self.resetMusic)
        OTPBase.OTPBase.playMusic(self, music, looping, interrupt, volume, time)
