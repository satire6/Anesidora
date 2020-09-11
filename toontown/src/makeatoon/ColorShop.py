"""ColorShop module: contains the ColorShop class"""

from pandac.PandaModules import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from MakeAToonGlobals import *
from toontown.toonbase import TTLocalizer
import ShuffleButton
import random
from direct.directnotify import DirectNotifyGlobal

class ColorShop(StateData.StateData):
    """ColorShop class: contains methods for changing the Avatar's
    color via user input"""

    notify = DirectNotifyGlobal.directNotify.newCategory("ColorShop")
    
    def __init__(self, doneEvent):
        """__init__(self, Event)
        Set-up the color shop interface to change the color of the
        parts of the given toon
        """
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.colorAll = 1
        return

    def getGenderColorList(self, dna):
        if self.dna.getGender() == "m":
            return ToonDNA.defaultBoyColorList
        else:
            return ToonDNA.defaultGirlColorList

    def enter(self, toon, shopsVisited=[]):
        """enter(self, toon)
        """
        # turn off any user control
        base.disableMouse()

        # load up the given toon
        self.toon = toon
        self.dna = toon.getStyle()

        colorList = self.getGenderColorList(self.dna)

        # Make note of the curent color.
        try:
            self.headChoice = colorList.index(self.dna.headColor)
            self.armChoice = colorList.index(self.dna.armColor)
            self.legChoice = colorList.index(self.dna.legColor)
            #self.startColor = self.headChoice
        except:
            self.headChoice = random.choice(colorList)
            self.armChoice = self.headChoice
            self.legChoice = self.headChoice
            #self.startColor = self.headChoice
            self.__swapHeadColor(0)
            self.__swapArmColor(0)
            self.__swapLegColor(0)
        self.startColor = 0
        
        # set up the "done" button
        self.acceptOnce("last", self.__handleBackward)        
        self.acceptOnce("next", self.__handleForward)
        # This is not supported with the new running toons
        # self.acceptOnce("enter", self.__handleForward)
        
        choicePool = [self.getGenderColorList(self.dna), self.getGenderColorList(self.dna), self.getGenderColorList(self.dna)]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeColor)
        self.acceptOnce("MAT-newToonCreated", self.shuffleButton.cleanHistory)        

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()

    def exit(self):
        """exit(self)
        Remove events and restore display
        """
        self.ignore("last")        
        self.ignore("next")
        self.ignore("enter")
        self.ignore(self.shuffleFetchMsg)
        try:
            del self.toon
        except:
            print "ColorShop: toon not found"
        self.hideButtons()

    def load(self):
        """load(self)
        """
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
        
##        self.guiAllUp = self.gui.find("**/tt_t_gui_mat_allUp")
##        self.guiAllDown = self.gui.find("**/tt_t_gui_mat_allDown")
##        self.guiPartsUp = self.gui.find("**/tt_t_gui_mat_partsUp")
##        self.guiPartsDown = self.gui.find("**/tt_t_gui_mat_allDown")
##        guiRadioFrame = self.gui.find("**/tt_t_gui_mat_radioFrame")
        
        # Create an emtpy frame which houses all the option buttons including the shuffle button.
        self.parentFrame = DirectFrame(
            relief = DGG.RAISED,
            pos = (0.98, 0, 0.416),
            frameColor = (1, 0, 0, 0),
            )
        
        # Create the Toon Color Frame.
        self.toonFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.073),
            hpr = (0, 0, 0),
            scale = 1.3,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ColorShopToon,
            text_scale = 0.0575,
##            text_pos = (0.002, -0.012),
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.allLButton = DirectButton(
            parent = self.toonFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapAllColor,
            extraArgs = [-1],
            )

        self.allRButton = DirectButton(
            parent = self.toonFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapAllColor,
            extraArgs = [1],
            )
        
        # Create the Head Color Frame.
        self.headFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.3),
            hpr = (0, 0, 2),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ColorShopHead,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.headLButton = DirectButton(
            parent = self.headFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapHeadColor,
            extraArgs = [-1],
            )

        self.headRButton = DirectButton(
            parent = self.headFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapHeadColor,
            extraArgs = [1],
            )

        # Create the Body Color Frame.
        self.bodyFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonScale,
            relief = None,
            pos = (0, 0, -0.5),
            hpr = (0, 0, -2),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ColorShopBody,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.armLButton = DirectButton(
            parent = self.bodyFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),command = self.__swapArmColor,
            extraArgs = [-1],
            )

        self.armRButton = DirectButton(
            parent = self.bodyFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapArmColor,
            extraArgs = [1],
            )

        # Create the Legs Color Frame.
        self.legsFrame = DirectFrame(
            parent = self.parentFrame,
            image = shuffleFrame,
            image_scale = halfButtonInvertScale,
            relief = None,
            pos = (0, 0, -0.7),
            hpr = (0, 0, 3),
            scale = 0.9,
            frameColor = (1, 1, 1, 1),
            text = TTLocalizer.ColorShopLegs,
            text_scale = 0.0625,
            text_pos = (-0.001, -0.015),
            text_fg = (1, 1, 1, 1),
            )
        
        self.legLButton = DirectButton(
            parent = self.legsFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.2, 0, 0),
            command = self.__swapLegColor,
            extraArgs = [-1],
            )

        self.legRButton = DirectButton(
            parent = self.legsFrame,
            relief = None,
            image = (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled),
            image_scale = halfButtonInvertScale,
            image1_scale = halfButtonInvertHoverScale,
            image2_scale = halfButtonInvertHoverScale,
            pos = (0.2, 0, 0),
            command = self.__swapLegColor,
            extraArgs = [1],
            )

##        self.toggleAllButton = DirectButton(
##            parent = aspect2d,
##            relief = None,
##            image = (self.guiPartsUp, self.guiPartsDown, self.guiPartsUp, self.guiPartsDown),
##            image_scale = halfButtonScale,
##            image1_scale = halfButtonHoverScale,
##            image2_scale = halfButtonHoverScale,
##            image3_scale = halfButtonHoverScale,
##            pos = (-0.8, 0, -0.8744),
##            text = ('', TTLocalizer.ColorShopParts, TTLocalizer.ColorShopParts, ''), 
##            text_scale = 0.08,
##            text_pos = (0.0, 0.13),
##            text_fg = (1, 1, 1, 1),
##            text_shadow = (0,0,0,1),
##            command = self.__toggleAllColor,
##            )
        
        self.parentFrame.hide()
        
        self.shuffleFetchMsg = 'ColorShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)

    def unload(self):
        """unload(self)
        """
        self.gui.removeNode()
        del self.gui

        self.parentFrame.destroy()
        self.toonFrame.destroy()
        self.headFrame.destroy()
        self.bodyFrame.destroy()
        self.legsFrame.destroy()
        self.headLButton.destroy()
        self.headRButton.destroy()
        self.armLButton.destroy()
        self.armRButton.destroy()
        self.legLButton.destroy()
        self.legRButton.destroy()
        self.allLButton.destroy()
        self.allRButton.destroy()

        del self.parentFrame
        del self.toonFrame
        del self.headFrame
        del self.bodyFrame
        del self.legsFrame
        del self.headLButton
        del self.headRButton
        del self.armLButton
        del self.armRButton
        del self.legLButton
        del self.legRButton 
        del self.allLButton
        del self.allRButton
        
        self.shuffleButton.unload()
        self.ignore("MAT-newToonCreated")
        
    def __swapAllColor(self, offset):
        colorList = self.getGenderColorList(self.dna)        
        length = len(colorList)
        choice = (self.headChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(choice, length, self.allLButton, self.allRButton)
        self.__swapHeadColor(offset)

        oldArmColorIndex = colorList.index(self.toon.style.armColor)
        oldLegColorIndex = colorList.index(self.toon.style.legColor)        
        self.__swapArmColor(choice - oldArmColorIndex)
        self.__swapLegColor(choice - oldLegColorIndex)
        
    def __swapHeadColor(self, offset):
        colorList = self.getGenderColorList(self.dna)        
        length = len(colorList)
        self.headChoice = (self.headChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.headChoice, length, self.headLButton,
                                   self.headRButton)
        newColor = colorList[self.headChoice]
        self.dna.headColor = newColor
        self.toon.swapToonColor(self.dna)

    def __swapArmColor(self, offset):
        colorList = self.getGenderColorList(self.dna)        
        length = len(colorList)
        self.armChoice = (self.armChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.armChoice, length, self.armLButton,
                                   self.armRButton)
        newColor = colorList[self.armChoice]
        self.dna.armColor = newColor
        self.toon.swapToonColor(self.dna)

    def __swapLegColor(self, offset):
        colorList = self.getGenderColorList(self.dna)        
        length = len(colorList)
        self.legChoice = (self.legChoice + offset) % length
        self.__updateScrollButtons(self.legChoice, length, self.legLButton,
                                   self.legRButton)
        newColor = colorList[self.legChoice]
        self.dna.legColor = newColor
        self.toon.swapToonColor(self.dna)

    def __updateScrollButtons(self, choice, length, lButton, rButton):
        # ghost the pickers if at the end of the 'wheel'
        if choice == (self.startColor - 1) % length:
            rButton['state'] = DGG.DISABLED
        else:
            rButton['state'] = DGG.NORMAL
        if choice == self.startColor % length:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL
        
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'        
        messenger.send(self.doneEvent)

    def changeColor(self):
        """
        This method is called when we need to display a new color because player
        pressed the shuffle button.
        """
        self.notify.debug('Entering changeColor')
        
        colorList = self.getGenderColorList(self.dna)
        newChoice = self.shuffleButton.getCurrChoice()
        
        newHeadColorIndex = colorList.index(newChoice[0])
        newArmColorIndex = colorList.index(newChoice[1])
        newLegColorIndex = colorList.index(newChoice[2])
        
        oldHeadColorIndex = colorList.index(self.toon.style.headColor)
        oldArmColorIndex = colorList.index(self.toon.style.armColor)
        oldLegColorIndex = colorList.index(self.toon.style.legColor)
        
        self.__swapHeadColor(newHeadColorIndex - oldHeadColorIndex)
        if self.colorAll:
            self.__swapArmColor(newHeadColorIndex - oldArmColorIndex)
            self.__swapLegColor(newHeadColorIndex - oldLegColorIndex)
        else:
            self.__swapArmColor(newArmColorIndex - oldArmColorIndex)
            self.__swapLegColor(newLegColorIndex - oldLegColorIndex)
        
    def getCurrToonSetting(self):
        """
        This method is called by ShuffleButton to get the current setting of the toon.
        The ShuffleButton saves this setting for it's history.
        """        
        return [self.dna.headColor, self.dna.armColor, self.dna.legColor]
        