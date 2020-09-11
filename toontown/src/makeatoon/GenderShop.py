"""GenderShop module: contains the GenderShop class"""

from pandac.PandaModules import *
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonDNA
from toontown.toon import Toon
from MakeAToonGlobals import *
from direct.directnotify import DirectNotifyGlobal
import random

class GenderShop(StateData.StateData):
    """GenderShop class: contains methods for changing the Avatar's
    gender via user input"""

    notify = DirectNotifyGlobal.directNotify.newCategory("GenderShop")
    
    def __init__(self, makeAToon, doneEvent):
        """__init__(self, Event)
        Set-up the gender to shop to query user about toons gender
        """
        StateData.StateData.__init__(self, doneEvent)
        self.shopsVisited = []
        self.toon = None
        self.gender = "m"
        self.makeAToon = makeAToon
        return

    def enter(self):
        """enter(self)
        """
        # turn off any user control
        base.disableMouse()
        # set up the "next" button
        self.accept("next", self.__handleForward)
        return None

    def showButtons(self):
        return None
        
    def exit(self):
        """exit(self)
        Remove events and restore display
        """
        self.ignore("next")

    def load(self):
        """
        Load all the assets pertaining to the gender selection.
        """
        gui = loader.loadModel("phase_3/models/gui/tt_m_gui_mat_mainGui")
        guiBoyUp = gui.find("**/tt_t_gui_mat_boyUp")
        guiBoyDown = gui.find("**/tt_t_gui_mat_boyDown")
        guiGirlUp = gui.find("**/tt_t_gui_mat_girlUp")
        guiGirlDown = gui.find("**/tt_t_gui_mat_girlDown")

        # Create Random Boy Button
        self.boyButton = DirectButton(
            relief = None,
            image = (guiBoyUp, guiBoyDown, guiBoyUp, guiBoyDown),
            # buttonScale is defined in MakeAToonGlobals
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (-0.4, 0, -0.8),
            command = self.createRandomBoy,
            text = ("", TTLocalizer.GenderShopBoyButtonText, TTLocalizer.GenderShopBoyButtonText, ""),
            text_font = ToontownGlobals.getInterfaceFont(),
            text_scale = 0.08,
            text_pos = (0, 0.19),
            text_fg = (1, 1, 1, 1),
            text_shadow = (0, 0, 0, 1),
            )
        self.boyButton.hide()
        
        # Create Random Girl Button
        self.girlButton = DirectButton(
            relief = None,
            image = (guiGirlUp, guiGirlDown, guiGirlUp, guiGirlDown),
            image_scale = halfButtonScale,
            image1_scale = halfButtonHoverScale,
            image2_scale = halfButtonHoverScale,
            pos = (0.4, 0, -0.8),
            command = self.createRandomGirl,
            text = ("", TTLocalizer.GenderShopGirlButtonText, TTLocalizer.GenderShopGirlButtonText, ""),
            text_font = ToontownGlobals.getInterfaceFont(),
            
            text_scale = 0.08,
            text_pos = (0, 0.19),
            text_fg = (1, 1, 1, 1),
            text_shadow = (0, 0, 0, 1),
            )
        self.girlButton.hide()
            
        gui.removeNode()
        del gui
        
        self.toon = None

    def unload(self):
        """unload(self)
        """
        self.boyButton.destroy()
        self.girlButton.destroy()
        
        del self.boyButton
        del self.girlButton
        
        if self.toon:
            self.toon.delete()
            
        self.makeAToon = None

    def setGender(self, choice):
        self.__setGender(choice)
        
    # event handlers

    def __setGender(self, choice):
        self.gender = "m"
        if self.toon:
            self.gender = self.toon.style.gender
        messenger.send(self.doneEvent)
    
    def hideButtons(self):
        """
        Hides all the buttons in the gender selection screen.
        """
        self.boyButton.hide()
        self.girlButton.hide()
        
    def showButtons(self):
        """
        Shows all the buttons in the gender selection screen.
        """
        self.boyButton.show()
        self.girlButton.show()
        
    def createRandomBoy(self):
        """
        Creates a random boy toon.
        Takes care if the player is free of paid.
        """
        self._createRandomToon('m')
    
    def createRandomGirl(self):
        """
        Creates a random girl toon.
        Takes care if the player is free of paid.
        """
        self._createRandomToon('f')
    
    def _createRandomToon(self, gender):
        """
        Creates a random toon with a given gender.
        """
        # Cleanup any old toon.
        if self.toon:
            self.toon.stopBlink()
            self.toon.stopLookAroundNow()
            self.toon.delete()
            
        self.dna = ToonDNA.ToonDNA()
        # stage = 1 is MAKE_A_TOON
        self.dna.newToonRandom(gender = gender, stage = 1)
        
        self.toon = Toon.Toon()
        self.toon.setDNA(self.dna)
        # make sure the avatar uses its highest LOD
        self.toon.useLOD(1000)
        # make sure his name doesn't show up
        self.toon.setNameVisible(0)
        self.toon.startBlink()
        self.toon.startLookAround()
        self.toon.reparentTo(render)
        self.toon.setPos(self.makeAToon.toonPosition)
        self.toon.setHpr(self.makeAToon.toonHpr)
        self.toon.setScale(self.makeAToon.toonScale)
        self.toon.loop("neutral")
        
        # Make the Next Button Active if a gender selection is made.
        self.makeAToon.setNextButtonState(DGG.NORMAL)
        self.makeAToon.setToon(self.toon)
        
        messenger.send("MAT-newToonCreated")
        
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)
