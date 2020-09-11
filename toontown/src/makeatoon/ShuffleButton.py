"""ShuffleButton module: Contains the ShuffleButton Class."""

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from MakeAToonGlobals import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import random

class ShuffleButton:
    """
    ShuffleButton Class: Contains methods for the shuffle button, which shuffles
    all the options in the current screen of the MakeAToon.
    This class also contains a forward and backward button to save history of the
    different random combinations.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('ShuffleButton')
    def __init__(self, parent, fetchEvent):
        """__init__(self)
        Set-up the shuffle button.
        """
        self.parent = parent    # This is the parent class that instantiated ShuffleButton.
        self.fetchEvent = fetchEvent
        self.history = [0]
        self.historyPtr = 0     # This is the pointer which points to which toon
                                # we're currently looking at in history.
        self.maxHistory = 10
        self.load()

    def load(self):
        """
        Load all the assets pertaining to the shuffle button.
        """
        gui = loader.loadModel("phase_3/models/gui/tt_m_gui_mat_mainGui")
        shuffleFrame = gui.find("**/tt_t_gui_mat_shuffleFrame")
        shuffleUp = gui.find("**/tt_t_gui_mat_shuffleUp")
        shuffleDown = gui.find("**/tt_t_gui_mat_shuffleDown")
        shuffleArrowUp = gui.find("**/tt_t_gui_mat_shuffleArrowUp")
        shuffleArrowDown = gui.find("**/tt_t_gui_mat_shuffleArrowDown")
        shuffleArrowDisabled = gui.find("**/tt_t_gui_mat_shuffleArrowDisabled")
        
        gui.removeNode()
        del gui
        
        # Create an emtpy frame which houses all the option buttons including the shuffle button.
        self.parentFrame = DirectFrame(
            parent = self.parent.parentFrame,
            relief = DGG.RAISED,
            pos = (0, 0, -1),
            frameColor = (1, 0, 0, 0),
            )
        
        # Create the Shuffle Frame.
        self.shuffleFrame = DirectFrame(
##            parent = self.parent.parentFrame,
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
##            pos = (0, 0, -0.875),
##            pos = (0, 0, -1),
            frameColor = (1, 1, 1, 1),
            )
        self.shuffleFrame.hide()
        
        # Create Shuffle Button.
        self.shuffleBtn = DirectButton(
##            parent = self.shuffleFrame,
            parent = self.parentFrame,
            relief = None,
            image = (shuffleUp, shuffleDown, shuffleUp),
            # buttonScale is defined in MakeAToonGlobals
            image_scale = halfButtonInvertScale,
            image1_scale = (-0.63, 0.6, 0.6),
            image2_scale = (-0.63, 0.6, 0.6),
            text = (TTLocalizer.ShuffleButton, TTLocalizer.ShuffleButton, TTLocalizer.ShuffleButton, ""),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_scale = TTLocalizer.SBshuffleBtn,
            text_pos = (0, -0.02),
            text_fg = (1, 1, 1, 1),
            text_shadow = (0, 0, 0, 1),
            command = self.chooseRandom,
            )
##        self.shuffleBtn.hide()

        # Create the Increment Button - Right Arrow.
        self.incBtn = DirectButton(
##            parent = self.shuffleFrame,
            parent = self.parentFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            # buttonScale is defined in MakeAToonGlobals
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
##            pos = (0.195, 0, 0),
            pos = (0.202, 0, 0),
            command = self.__goFrontHistory,
            )
        self.incBtn.hide()
            
        # Create the Decrement Button - Left Arrow.
        self.decBtn = DirectButton(
##            parent = self.shuffleFrame,
            parent = self.parentFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            # buttonScale is defined in MakeAToonGlobals
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
##            pos = (-0.195, 0, 0),
            pos = (-0.202, 0, 0),
            command = self.__goBackHistory,
            )
        self.decBtn.hide()
        
        self.lerpDuration = 0.5
        self.showLerp = None
        self.frameShowLerp =  LerpColorInterval(self.shuffleFrame, self.lerpDuration, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        self.incBtnShowLerp =  LerpColorInterval(self.incBtn, self.lerpDuration, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        self.decBtnShowLerp =  LerpColorInterval(self.decBtn, self.lerpDuration, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))
        
        self.__updateArrows()

    def unload(self):
        """
        Unload all the assets pertaining to the shuffle button.
        """
        if self.showLerp:
            self.showLerp.finish()
            del self.showLerp
        
        self.parent = None
        self.parentFrame.destroy()
        self.shuffleFrame.destroy()
        self.shuffleBtn.destroy()
        self.incBtn.destroy()
        self.decBtn.destroy()
        
        del self.parentFrame
        del self.shuffleFrame
        del self.shuffleBtn
        del self.incBtn
        del self.decBtn
        
    def showButtons(self):
        """
        Shows all the GUI elements of ShuffleButton.
        """
        self.shuffleFrame.show()
        self.shuffleBtn.show()
        self.incBtn.show()
        self.decBtn.show()
        
    def hideButtons(self):
        """
        Hides all the GUI elements of ShuffleButton.
        """
        self.shuffleFrame.hide()
        self.shuffleBtn.hide()
        self.incBtn.hide()
        self.decBtn.hide()
        
    def setChoicePool(self, pool):
        """
        This method is called by the parent class to set the pool of properties
        from which the shuffle selects from.
        pool - is a list of lists, where len(pool) is the number of properties to randomize,
        and all the elements in a list in pool are the choices for that property.
        Eg: From the Body Shop the pool would be something like this:
        [[head1, head2], [body1, body2], [legs1, legs2]]
        """
        self.pool = pool
    
    def chooseRandom(self):
        """
        This method makes a random selection of properties and stores it as a list.
        The number of elements in this list should be the same as len(pool) in self.setChoicePool.
        """
        self.saveCurrChoice()
        self.currChoice = []
        for prop in self.pool:
            self.currChoice.append(random.choice(prop))
        self.notify.debug('current choice : %s' %self.currChoice)
            
        if (len(self.history) == self.maxHistory):
            self.history.remove(self.history[0])
        self.history.append(0)
        self.historyPtr = len(self.history) - 1

        if (len(self.history) == 2):
            self.startShowLerp()
        
        self.__updateArrows()
        messenger.send(self.fetchEvent)
    
    def getCurrChoice(self):
        """
        This method is called by the parent to get the current choice of ShuffleButton.
        """
        return self.currChoice
    
    def saveCurrChoice(self):
        """
        Everytime the Shuffle Button is pressed, it saves the current choice in
        in a list as a history, before generating another choice.
        """
        # Ask the parent what the current configuration of the toon is.
        self.currChoice = self.parent.getCurrToonSetting()
        self.history[self.historyPtr] = self.currChoice
        
    def __goBackHistory(self):
        """
        Go back to the previous toon setting in history.
        This method is called when the left arrow on the shuffle button is pressed.
        """
        self.saveCurrChoice()
        self.historyPtr -= 1
        self.currChoice = self.history[self.historyPtr]
        self.__updateArrows()
        messenger.send(self.fetchEvent)
        
    def __goFrontHistory(self):
        """
        Go front to the next toon setting in history.
        This method is called when the right arrow on the shuffle button is pressed.
        """
        self.saveCurrChoice()
        self.historyPtr += 1
        self.currChoice = self.history[self.historyPtr]
        self.__updateArrows()
        messenger.send(self.fetchEvent)
    
    def __updateArrows(self):
        """
        Update the state of the arrows depending on the position of the historyPtr.
        """
        if (self.historyPtr == 0):
            self.decBtn['state'] = DGG.DISABLED
        else:
            self.decBtn['state'] = DGG.NORMAL
        
        if (self.historyPtr >= (len(self.history) - 1)):
            self.incBtn['state'] = DGG.DISABLED
        else:
            self.incBtn['state'] = DGG.NORMAL
            
    def startShowLerp(self):
        """
        Starts an interval which slowly makes the shuffleFrame, incBtn and decBtn visible.
        """        
        self.showLerp = Sequence(
            Parallel(
                Func(self.shuffleFrame.show),
                Func(self.incBtn.show),
                Func(self.decBtn.show)),
            Parallel(
                self.frameShowLerp,
                self.incBtnShowLerp,
                self.decBtnShowLerp)                
            )
        self.showLerp.start()
    
    
    def cleanHistory(self):
        """
        Clean the history of the Shuffle Button.
        Also hide the shuffleFrame, incBtn and decBtn.
        """
        self.history = [0]
        self.historyPtr = 0
        self.shuffleFrame.hide()
        self.incBtn.hide()
        self.decBtn.hide()