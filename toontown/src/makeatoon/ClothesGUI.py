"""ClothesGUI is a base class that contains the clothes picking interface"""

from pandac.PandaModules import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from MakeAToonGlobals import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
import ShuffleButton
import random

CLOTHES_MAKETOON = 0   # used by MakeAToon
CLOTHES_TAILOR = 1     # used by DistributedNPCTailor
CLOTHES_CLOSET = 2     # used by DistributedCloset

class ClothesGUI(StateData.StateData):
    """ClothesGUI class: contains methods for changing the Avatar's
    outfit via user input"""

    notify = DirectNotifyGlobal.directNotify.newCategory("ClothesGUI")

    def __init__(self, type, doneEvent, swapEvent = None):
        """__init__(self, Event)
        """
        StateData.StateData.__init__(self, doneEvent)
        self.type = type
        self.toon = None
        self.swapEvent = swapEvent
        self.gender = '?'
        self.girlInShorts = 0
        self.swappedTorso = 0
        return
        
    def load(self):
        # the basic interface with always have scroll buttons for
        # the shirts and the shorts, some text saying "shirts" and
        # "bottoms", and some sort of accept button

        self.gui = loader.loadModel("phase_3/models/gui/tt_m_gui_mat_mainGui")
        guiRArrowUp = self.gui.find("**/tt_t_gui_mat_arrowUp")
        guiRArrowRollover = self.gui.find("**/tt_t_gui_mat_arrowUp")
        guiRArrowDown = self.gui.find("**/tt_t_gui_mat_arrowDown")
        guiRArrowDisabled = self.gui.find("**/tt_t_gui_mat_arrowDisabled")
        
        shuffleFrame = self.gui.find("**/tt_t_gui_mat_shuffleFrame")
        shuffleArrowUp = self.gui.find("**/tt_t_gui_mat_shuffleArrowUp")
        shuffleArrowDown = self.gui.find("**/tt_t_gui_mat_shuffleArrowDown")
        shuffleArrowRollover = self.gui.find("**/tt_t_gui_mat_shuffleArrowUp")
        shuffleArrowDisabled = self.gui.find("**/tt_t_gui_mat_shuffleArrowDisabled")
            
        # Create an emtpy frame which houses all the option buttons including the shuffle button.
        self.parentFrame = DirectFrame(
            relief = DGG.RAISED,
            pos = (0.98, 0, 0.416),
            frameColor = (1, 0, 0, 0),
            )
            
        # Create the Shirts Frame.
        self.shirtFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.4),
            hpr = (0, 0, 3),
            scale = 1.2,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ClothesShopShirt,
            text_scale = 0.0575,
##            text_pos = (0.002, -0.012),
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.topLButton = DirectButton(
            parent = self.shirtFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.swapTop,
            extraArgs = [-1],
            )
            
        self.topRButton = DirectButton(
            parent = self.shirtFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.swapTop,
            extraArgs = [1],
            )
        
        # Create the Bottoms Frame.
        self.bottomFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.65),
            hpr = (0, 0, -2),
            scale = 1.2,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ColorShopToon,
            text_scale = 0.0575,
##            text_pos = (0.002, -0.012),
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.bottomLButton = DirectButton(
            parent = self.bottomFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.swapBottom,
            extraArgs = [-1],
            )
            
        self.bottomRButton = DirectButton(
            parent = self.bottomFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.swapBottom,
            extraArgs = [1],
            )
        
        self.parentFrame.hide()
        
        self.shuffleFetchMsg = 'ClothesShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)

    def unload(self):
        """unload(self)
        """
        self.gui.removeNode()
        del self.gui

        self.parentFrame.destroy()
        self.shirtFrame.destroy()
        self.bottomFrame.destroy()
        self.topLButton.destroy()
        self.topRButton.destroy()
        self.bottomLButton.destroy()
        self.bottomRButton.destroy()

        del self.parentFrame
        del self.shirtFrame
        del self.bottomFrame
        del self.topLButton
        del self.topRButton
        del self.bottomLButton
        del self.bottomRButton
        self.shuffleButton.unload()
        self.ignore("MAT-newToonCreated")

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()
        
    def enter(self, toon):
        """enter(self, toon)
        """
        self.notify.debug("enter")
        # turn off any user control
        base.disableMouse()
        self.toon = toon

        # setup the scroll interface
        # including which set of clothes
        # we will be scrolling through
        # this method should be defined in the child
        # classes
        self.setupScrollInterface()
        
        # The toon that has entered already has assigned clothes, which is not
        # at the beginning of the self.tops list. the self.topChoice also does
        # not point to it. To have a smooth transition we're going to force the
        # topChoice and bottomChoice to this pre-assigned top and bottom.
        
        # The tailor shop doesn't add the toon's current clothes in the list, so don't do this.
        if not (self.type == CLOTHES_TAILOR):
            currTop = (self.toon.style.topTex, self.toon.style.topTexColor, self.toon.style.sleeveTex, self.toon.style.sleeveTexColor)        
            currTopIndex = self.tops.index(currTop)
            self.swapTop(currTopIndex - self.topChoice)
            currBottom = (self.toon.style.botTex, self.toon.style.botTexColor)
            currBottomIndex = self.bottoms.index(currBottom)
            self.swapBottom(currBottomIndex - self.bottomChoice)
        
        choicePool = [self.tops, self.bottoms]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeClothes)
        self.acceptOnce("MAT-newToonCreated", self.shuffleButton.cleanHistory)

    def exit(self):
        """exit(self)
        Remove events and restore display
        """
        try:
            del self.toon
        except:
            self.notify.warning("ClothesGUI: toon not found")
        self.hideButtons()
        # remove keyboard/gui events
        self.ignore("enter")
        self.ignore("next")
        self.ignore("last")
        self.ignore(self.shuffleFetchMsg)

    def setupButtons(self):
        self.girlInShorts = 0 
        if (self.gender == 'f'):
            # See what kind of torso we need (shorts vs. skirt)
            if (self.bottomChoice == -1):
                botTex = self.bottoms[0][0]
            else:
                botTex = self.bottoms[self.bottomChoice][0]
            if (ToonDNA.GirlBottoms[botTex][1] == ToonDNA.SHORTS):
                self.girlInShorts = 1

        # set the button text based on gender
        if (self.toon.style.getGender() == "m"):
##            self.bottomLButton['text'] = TTLocalizer.ClothesShopShorts
##            self.bottomRButton['text'] = TTLocalizer.ClothesShopShorts
            self.bottomFrame['text'] = TTLocalizer.ClothesShopShorts
        else:
##            self.bottomLButton['text'] = TTLocalizer.ClothesShopBottoms
##            self.bottomRButton['text'] = TTLocalizer.ClothesShopBottoms
            self.bottomFrame['text'] = TTLocalizer.ClothesShopBottoms
        
        # set exit event
        self.acceptOnce("last", self.__handleBackward)
        self.acceptOnce("next", self.__handleForward)
        # This is not supported with the new running toons
        # self.acceptOnce("enter", self.__handleForward)
        return None

    # event handlers

    def swapTop(self, offset):
        length = len(self.tops)
        self.topChoice += offset 
        if (self.topChoice <= 0):
            self.topChoice = 0
        # ghost the pickers if at the end of the 'wheel'
        self.updateScrollButtons(self.topChoice, length, 0,
                                 self.topLButton, self.topRButton)
        # Put some index range checking here
        if ((self.topChoice < 0) or (self.topChoice >= len(self.tops)) or 
            (len(self.tops[self.topChoice]) != 4)):
            self.notify.warning("topChoice index is out of range!")
            return None
        self.toon.style.topTex = self.tops[self.topChoice][0]
        self.toon.style.topTexColor = self.tops[self.topChoice][1]
        self.toon.style.sleeveTex = self.tops[self.topChoice][2]
        self.toon.style.sleeveTexColor = self.tops[self.topChoice][3]
        assert(self.notify.debug("topChoice: %s" % (self.topChoice)))
        assert(self.notify.debug('shirt: %d color: %d sleeve color: %d' % (self.toon.style.topTex, self.toon.style.topTexColor, self.toon.style.sleeveTexColor)))
        self.toon.generateToonClothes()
        if (self.swapEvent != None):
            messenger.send(self.swapEvent)
        messenger.send('wakeup')
        
    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if (self.bottomChoice <= 0):
            self.bottomChoice = 0
        # ghost the pickers if at the end of the 'wheel'
        assert(self.notify.debug("bottoms: choice = %s, length = %s" % (self.bottomChoice, length)))
        
        self.updateScrollButtons(self.bottomChoice, length, 0,
                                   self.bottomLButton, self.bottomRButton)
        if ((self.bottomChoice < 0) or (self.bottomChoice >= len(self.bottoms))
            or (len(self.bottoms[self.bottomChoice]) != 2)):
            self.notify.warning("bottomChoice index is out of range!")
            return None
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        
        if (self.toon.generateToonClothes() == 1):       
            self.toon.loop("neutral", 0)
            self.swappedTorso = 1

        if (self.swapEvent != None):
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def updateScrollButtons(self, choice, length, startTex,
                              lButton, rButton):
        # ghost the pickers if at the end of the 'wheel'
        if choice >= length-1: 
            rButton['state'] = DGG.DISABLED 
        else:
            rButton['state'] = DGG.NORMAL 
        if choice <= 0:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL

    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def resetClothes(self, style):
        if self.toon:
            self.toon.style.makeFromNetString(style.makeNetString())
            # In case we've switched to the skirt torso and are reverting back
            # to shorts, we need to regenerate clothes for the toon
            if (self.swapEvent != None and self.swappedTorso == 1):
                self.toon.swapToonTorso(self.toon.style.torso, genClothes = 0)
                self.toon.generateToonClothes()
                self.toon.loop("neutral", 0)

    def changeClothes(self):
        """
        This method is called when we need to display new clothes because player
        pressed the shuffle button.
        """
        self.notify.debug('Entering changeClothes')
        newChoice = self.shuffleButton.getCurrChoice()        
        newTopIndex = self.tops.index(newChoice[0])
        newBottomIndex = self.bottoms.index(newChoice[1])
        oldTopIndex = self.topChoice
        oldBottomIndex = self.bottomChoice        
        self.swapTop(newTopIndex - oldTopIndex)
        self.swapBottom(newBottomIndex - oldBottomIndex)
        
    def getCurrToonSetting(self):
        """
        This method is called by ShuffleButton to get the current setting of the toon.
        The ShuffleButton saves this setting for it's history.
        """        
        return [self.tops[self.topChoice], self.bottoms[self.bottomChoice]]