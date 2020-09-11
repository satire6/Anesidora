
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import FishPokerBase
import FishGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

class FishPokerCard(DirectFrame):

    UnlockedColor = Vec4(*ToontownGlobals.GlobalDialogColor)
    LockedColor = Vec4(0.8,0.4,0.4,1)
    
    def __init__(self, index, lockCallback, **kw):
        optiondefs = (
            ('relief',                                    None,    None),
            ('image',                   DGG.getDefaultDialogGeom(),    None),
            ('image_color',  ToontownGlobals.GlobalDialogColor,    None),
            ('image_scale',                    (0.35, 1, 0.45),    None),
            ('text',                                        "",    None),
            ('text_scale',                                0.06,    None),
            ('text_fg',                           (0, 0, 0, 1),    None),
            ('text_pos',                          (0, 0.35, 0),    None),
            ('text_font',   ToontownGlobals.getInterfaceFont(),    None),
            ('text_wordwrap',                             13.5,    None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self)
        self.initialiseoptions(FishPokerCard)
        self.index = index
        self.fish = None
        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        self.lockCallback = lockCallback
        self.lockButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = 1,
            text = TTLocalizer.FishPokerLock,
            text_scale = 0.06,
            textMayChange = 1,
            pos = (0,0,0.2),
            command = self.toggleLock,
            )
        # TODO: image of fish here
        self.fishFrame = DirectFrame(
            parent = self,
            relief = None,
            text = "",
            text_scale = 0.05,
            pos = (0,0,-0.2),
            )
        guiButton.removeNode()

    def toggleLock(self):
        # Call the callback, passing in our index
        self.lockCallback(self.index)

    def update(self, fish, lockedStatus):
        self.fish = fish
        if self.fish:
            self.lockButton['state'] = DGG.NORMAL
            self.fishFrame['text'] = fish.getGenusName()
        else:
            self.lockButton['state'] = DGG.DISABLED
            self.fishFrame['text'] = ""
        self.setLockStatus(lockedStatus)
        return

    def setLockStatus(self, lockStatus):
        if lockStatus:
            self.lockButton['text'] = TTLocalizer.FishPokerUnlock
            self['image_color'] = self.LockedColor
        else:
            self.lockButton['text'] = TTLocalizer.FishPokerLock
            self['image_color'] = self.UnlockedColor
        return

    def clear(self):
        self.update(None, 0)
        return
    

class FishPokerGui(FishPokerBase.FishPokerBase,
                   DirectFrame):
    def __init__(self, lockCallback, cashInCallback):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(FishPokerGui)
        self.setPos(0,0,0.8)
        self.setScale(0.7)
        self.lockCallback = lockCallback
        self.cashInCallback = cashInCallback

        self.__cardGuis = {}
        for i in range(self.NumSlots):
            card = FishPokerCard(i, self.toggleLock)
            card.reparentTo(self)
            card.setPos(-0.8 + i*0.4, 0, 0)
            self.__cardGuis[i] = card

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        self.cashInButton = DirectButton(
            parent = self,
            relief = None,
            image = (guiButton.find("**/QuitBtn_UP"),
                     guiButton.find("**/QuitBtn_DN"),
                     guiButton.find("**/QuitBtn_RLVR"),
                     ),
            image_scale = 1.15,
            text = TTLocalizer.FishPokerCashIn % (0, ""),
            text_scale = 0.06,
            # textMayChange = 0,
            pos = (0,0,-0.3),
            command = self.cashIn,
            )
        guiButton.removeNode()
        
        # Now update the base class, since it touched some of the
        # buttons on initialization
        FishPokerBase.FishPokerBase.__init__(self)

    def updateCashIn(self):
        value, handName = self.getCurrentValue()
        self.cashInButton['text'] = TTLocalizer.FishPokerCashIn % (handName, value)

    def cashIn(self):
        # Gui will be update by the call to clear inside FishPokerBase
        result = FishPokerBase.FishPokerBase.cashIn(self)
        # Call back to the spot, which sends the update to the AI
        self.cashInCallback()
        return result

    def toggleLock(self, index):
        if self.isLocked(index):
            self.setLockStatus(index, 0)
        else:
            self.setLockStatus(index, 1)

    def setLockStatus(self, index, lockStatus):
        result = FishPokerBase.FishPokerBase.setLockStatus(self, index, lockStatus)
        # Update the gui
        self.__cardGuis[index].setLockStatus(lockStatus)
        # Call back to the spot, which sends the update to the AI
        self.lockCallback(index, lockStatus)
        return result

    def drawCard(self, card):
        index = FishPokerBase.FishPokerBase.drawCard(self, card)
        if index != -1:
            self.__cardGuis[index].update(card, 0)
        self.updateCashIn()
        return index

    def clear(self):
        FishPokerBase.FishPokerBase.clear(self)
        # Update the gui
        for cardGui in self.__cardGuis.values():
            cardGui.clear()
        # Update value
        self.updateCashIn()
