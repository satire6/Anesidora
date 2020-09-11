from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
from otp.otpgui.OTPDialog import *
from direct.interval.LerpInterval import LerpPosInterval, LerpScaleInterval, LerpFunc
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait
from direct.task import Task
import random

class ToontownLoadingBlocker(TTDialog.TTDialog):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownLoadingBlocker")
    
    def __init__(self, avList):
        if not self.__shouldShowBlocker(avList):
            return
             
        TTDialog.TTDialog.__init__(self)
        
        gui = loader.loadModel("phase_3/models/gui/tt_m_gui_pat_mainGui")
        img = gui.find("**/tt_t_gui_pat_loadingPopup")
        self['image'] = img
        self['image_scale'] = (1, 0, 1)
        self['image_pos'] = (0, 0, -0.4)
        
        gui.removeNode()
        
        self.loadingTextChangeTimer = 10.0
        self.loadingTextTimerVariant = 3.0
        self.loadingTextFreezeTime = 3.0
        self.hideBlockerIval = None
        self.canChangeLoadingText = True
        
        self.__setupLoadingBar()
        self.__createTitleText()
        self.__createToonTip()
        self.__createLoadingText()
        self.__showBlocker()
        
        self.accept("phaseComplete-4", self.__shrinkLoadingBar)
        self.accept("launcherPercentPhaseComplete", self.__update)
        
    def destroy(self):
        taskMgr.remove("changeLoadingTextTask")
        taskMgr.remove("canChangeLoadingTextTask")
        
        self.ignore("phaseComplete-4")
        self.ignore("launcherPercentPhaseComplete")
        
        self.__cleanupHideBlockerIval()
        
        self.title.destroy()
        self.title = None
        
        self.loadingText.destroy()
        self.loadingText = None
        self.loadingTextList = None
        
        self.toonTipText.destroy()
        self.toonTipText = None
        
        self.bar.destroy()
        self.bar = None
        
        TTDialog.TTDialog.destroy(self)
    
    def __hideBlocker(self):
        """
        Hide the blocker panel.
        """
        self.hide()
        # Show the smaller loading text at the left bottom corner when the blocker panel is hidden.
        if self.__isValidDownloadBar():
            base.downloadWatcher.text.show()
        
    def __showBlocker(self):
        """
        Show the blocker panel.
        """
        self.show()
        # Hide the smaller loading text at the left bottom corner when the blocker panel is up.
        if self.__isValidDownloadBar():
            base.downloadWatcher.text.hide()
    
    def __setupLoadingBar(self):
        """
        Setup the loading bar for the ToontownLoadingBlocker.
        Make sure it is in the right bin so that it is visible in front of the
        ToontownLoadingBlocker.
        """
        self.bar = DirectWaitBar(
            parent = self,
            guiId = 'DownloadBlockerBar',
            pos = (0, 0, -0.3138),
            relief = DGG.SUNKEN,
            frameSize = (-0.6,0.6,-0.1,0.1),
            borderWidth = (0.02,0.02),
            scale = (0.8, 0.8, 0.5),
            range = 100,
            sortOrder = 5000,
            frameColor = (0.5,0.5,0.5,0.5),
            barColor = (0.2,0.7,0.2,0.5),
            text = "0%",
            text_scale = (0.08, 0.128),
            text_fg = (1, 1, 1, 1),
            text_align = TextNode.ACenter,
            text_pos = (0, -0.035),
            )
        self.bar.setBin('gui-popup', 1)
            
        if self.__isValidDownloadBar():
            base.downloadWatcher.bar.hide()
        
    def __resetLoadingBar(self):
        """
        Reset the bin for the loading bar so that it appears unchanged
        as part of the ToontownDownloadWatcher.
        """
        self.bar.clearBin()
        if self.__isValidDownloadBar():
            base.downloadWatcher.bar.show()
    
    def __isValidDownloadBar(self):
        """
        Just a validity function to check if base.downloadWatcher.bar is valid.
        """
        if hasattr(base, "downloadWatcher") and base.downloadWatcher:
            if hasattr(base.downloadWatcher, "bar") and base.downloadWatcher.bar:
                return True
        return False
    
    def __createTitleText(self):
        """
        Create the title text for the blocker panel.
        """
        self.title = DirectLabel(
            parent = self,
            relief = None,
            guiId = 'BlockerTitle',
            pos = (0, 0, 0.38),
            text = TTLocalizer.BlockerTitle,
            text_font = ToontownGlobals.getSignFont(),
            text_fg = (1,0.9,0.1,1),
            text_align = TextNode.ACenter,
            # text_shadow = (0,0,0,1),
            text_scale = 0.1,
            textMayChange = 1,
            sortOrder = 50,
            )    
    
    def __createLoadingText(self):
        """
        Create a loading text.
        This will have crazy toony loading texts, irrelevant to what is being loaded.
        """
        self.loadingText = DirectLabel(
            parent = self,
            relief = None,
            guiId = 'BlockerLoadingText',
            pos = (0, 0, -0.2357),
            text = "Loading...",
            text_fg = (1, 1, 1, 1),
            # text_shadow = (0,0,0,1),
            text_scale = 0.055,
            textMayChange = 1,
            text_align = TextNode.ACenter,
            sortOrder = 50,
            )
        
        self.loadingTextList = TTLocalizer.BlockerLoadingTexts
        
        # Set the first random loading text.
        self.__changeLoadingText()
        
        # Start a task to change the loading text every loadingTextChangeTimer seconds.
        taskMgr.doMethodLater(self.loadingTextChangeTimer, self.__changeLoadingTextTask, "changeLoadingTextTask")
    
    def __changeLoadingText(self):
        """
        Change the loading text every time the loading bar goes to 0%,
        either when it starts loading a new phase or a new patch.
        """        
        def getLoadingText():
            listLen = len(self.loadingTextList)
            if (listLen > 0):
                randomIndex = random.randrange(listLen)
                randomLoadingText = self.loadingTextList.pop(randomIndex)
                return randomLoadingText
            else:
                # Oops the loading took so long, that we exhausted
                # all our loading texts. Start over again.
                self.loadingTextList = TTLocalizer.BlockerLoadingTexts 
        if self.canChangeLoadingText:
            self.loadingText['text'] = getLoadingText()
            self.canChangeLoadingText = False
            taskMgr.doMethodLater(self.loadingTextFreezeTime, self.__canChangeLoadingTextTask, "canChangeLoadingTextTask")
        
    def __changeLoadingTextTask(self, task):
        """
        The task that requests a change of loading text.
        This task is kept going so that the loading text changes every 5 secs.
        Along with this the loading text also changes everytime the loading
        bar goes to 0%.
        """
        self.__changeLoadingText()
        # Adding a random time variation in changing the loading text,
        # so that the loading text change looks less fake.
        randVariation = random.uniform(-self.loadingTextTimerVariant, self.loadingTextTimerVariant)
        task.delayTime = self.loadingTextChangeTimer + randVariation
        return task.again
    
    def __canChangeLoadingTextTask(self, task):
        """
        We want the loading text to stay on screen for at least
        3 seconds. If we have just changed the loading text, and then the
        loading bar goes to 0%, it will try to change the loading text again.
        This task will make sure this doesn't happen. Without this it is highly
        possible for the loading text to change immediately resulting in a bad show.
        """
        self.canChangeLoadingText = True
        return task.done
    
    def __createToonTip(self):
        """
        Create the toon tip text.
        """
        def getTip(tipCategory):
            return TTLocalizer.TipTitle + "\n" + random.choice(TTLocalizer.TipDict.get(tipCategory))
        
        self.toonTipText = DirectLabel(
            parent = self,
            relief = None,
            guiId = 'BlockerToonTip',
            pos = (0, 0, -0.4688),
            text = getTip(TTLocalizer.TIP_GENERAL),
            text_fg = (1, 1, 1, 1),
            # text_shadow = (0,0,0,1),
            text_scale = 0.05,
            textMayChange = 1,
            text_align = TextNode.ACenter,
            text_wordwrap = 32,
            sortOrder = 50,
            )
            
    def __shouldShowBlocker(self, avList):
        """
        Determines if the ToontownLoadingBlocker should be visible.
        Returns True if the ToontownLoadingBlocker should be visible,
        Returens False if the ToontownLoadingBlocker should be hidden.
        """
        def hasPlayableToon(avList):
            # Check if there is a playable toon.
            if (len(avList) > 0):
                if base.cr.isPaid():
                    return True
                else:
                    for av in avList:
                        if (av.position == 1):
                            return True
            return False
        
        if hasPlayableToon(avList):
            # Return True if there is anything to load.
            if not (base.launcher.getPhaseComplete(3.5) and base.launcher.getPhaseComplete(4)):
                return True
        return False
    
    def __shrinkLoadingBar(self):
        if self.__isValidDownloadBar():
            ivalDuration = 0.5
            barPosIval = LerpPosInterval(self.bar, ivalDuration, (-0.81,0,-0.96))
            barScaleIval = LerpScaleInterval(self.bar, ivalDuration, (0.25, 0.25, 0.25))
            
            def posText(pos):
                self.bar['text_pos'] = (0, pos)
            
            def scaleText(scale):
                self.bar['text_scale'] = (scale, scale)
            
            textScaleIval = LerpFunc(scaleText, 
                fromData = 0.08,
                toData = 0.16,
                duration = ivalDuration)
                
            textPosIval = LerpFunc(posText, 
                fromData = -0.035,
                toData = -0.05,
                duration = ivalDuration)
            
            shrinkIval = Parallel(barPosIval, barScaleIval, 
                                  textPosIval, textScaleIval, 
                                  Func(self.loadingText.hide))
            
            self.hideBlockerIval = Sequence(
                shrinkIval, Wait(0.5), 
                Func(self.__hideBlocker),
                Func(self.__resetLoadingBar),
                Func(self.destroy))
            self.hideBlockerIval.start()
        
    def __cleanupHideBlockerIval(self):
        """
        Cleans up the hideBlockerIval.
        """
        if self.hideBlockerIval:
            self.hideBlockerIval.finish()
            self.hideBlockerIval = None
    
    def __update(self, phase, percent, reqByteRate, actualByteRate):
        """
        Track the percent loads of the various phases.
        """
        # Track the DownloadWatcherBar and replicate it's percentage complete
        if self.__isValidDownloadBar():
            percent = base.downloadWatcher.bar['value']
            self.bar['text'] = ("%s %%" % (percent))
            self.bar['value'] = percent
        # Change the loading text everytime we start from 0%.
        if (percent == 0):
            self.__changeLoadingText()
    