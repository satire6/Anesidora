#===============================================================================
# Contact: Edmundo Ruiz, (Schell Games)
# Created: October 2009
#
# Purpose: Input Handler for the Party Cog Activity
#===============================================================================
from direct.showbase.DirectObject import DirectObject

from pandac.PandaModules import ModifierButtons

ROTATE_LEFT_KEY = "arrow_left"
ROTATE_RIGHT_KEY = "arrow_right"
FORWARD_KEY = "arrow_up"
BACKWARDS_KEY = "arrow_down"

THROW_PIE_KEYS = ["control", "delete", "insert"]

class PartyCogActivityInput(DirectObject):
    """Manager for all keyboard input for the party cog activity"""
    
    notify = directNotify.newCategory("PartyCogActivityInput")
    
    leftPressed = 0
    rightPressed = 0
    upPressed = 0
    downPressed = 0
    throwPiePressed = False
    throwPieWasReleased = False
    throwPiePressedStartTime = 0
    
    def __init__(self, exitActivityCallback):
        DirectObject.__init__(self)
        
        self.exitActivityCallback = exitActivityCallback
        
        self._prevModifierButtons = base.mouseWatcherNode.getModifierButtons()
        
    def enable(self):
        self.enableAimKeys()
        self.enableThrowPieKeys()
        #self.enableExitActivityKeys()
    
    def disable(self):
        self.disableAimKeys()
        self.disableThrowPieKeys()
        #self.disableExitActivityKeys()

    def enableExitActivityKeys(self):
        self.accept("escape", self.exitActivityCallback)
        
    def disableExitActivityKeys(self):
        self.ignore("escape")
        
    def enableThrowPieKeys(self):
        for key in THROW_PIE_KEYS:
            self.accept(key, self.handleThrowPieKeyPressed, [key])
            
        self.throwPiePressed = False
        self.readyToThrowPie = False
        
    def disableThrowPieKeys(self):
        for key in THROW_PIE_KEYS:
            self.ignore(key)
            self.ignore(key + "-up")
            
    def handleThrowPieKeyPressed(self, key):
        if self.throwPiePressed:
            return
        
        self.throwPiePressed = True
        self.accept(key + "-up", self.handleThrowPieKeyReleased, [key])
        
        self.throwPiePressedStartTime = globalClock.getFrameTime()
        
    def handleThrowPieKeyReleased(self, key):
        if not self.throwPiePressed:
            return
    
        self.ignore(key + "-up")
        
        self.throwPieWasReleased = True
        self.throwPiePressed = False
        
    def enableAimKeys(self):
        self.leftPressed = 0
        self.rightPressed = 0
        
        # Disable Panda's modifier key events (alt+key, ctrl+key)
        base.mouseWatcherNode.setModifierButtons(ModifierButtons())
        base.buttonThrowers[0].node().setModifierButtons(ModifierButtons())
        
        self.accept(ROTATE_LEFT_KEY, self.__handleLeftKeyPressed)
        self.accept(ROTATE_RIGHT_KEY, self.__handleRightKeyPressed)
        self.accept(FORWARD_KEY, self.__handleUpKeyPressed)
        self.accept(BACKWARDS_KEY, self.__handleDownKeyPressed)
        
    def disableAimKeys(self):
        self.ignore(ROTATE_LEFT_KEY)
        self.ignore(ROTATE_RIGHT_KEY)
        self.ignore(FORWARD_KEY)
        self.ignore(BACKWARDS_KEY)
        
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0
        
        self.ignore(ROTATE_LEFT_KEY + "-up")
        self.ignore(ROTATE_RIGHT_KEY + "-up")
        self.ignore(FORWARD_KEY + "-up")
        self.ignore(BACKWARDS_KEY + "-up")
        
        # Enable Panda's modifier key events (alt+key, ctrl+key) 
        base.mouseWatcherNode.setModifierButtons(self._prevModifierButtons)
        base.buttonThrowers[0].node().setModifierButtons(self._prevModifierButtons)
        
    def __handleLeftKeyPressed(self):
        self.ignore(ROTATE_LEFT_KEY)
        self.accept(ROTATE_LEFT_KEY+"-up", self.__handleLeftKeyReleased)
        self.__leftPressed()

    def __handleRightKeyPressed(self):
        self.ignore(ROTATE_RIGHT_KEY)
        self.accept(ROTATE_RIGHT_KEY + "-up", self.__handleRightKeyReleased)
        self.__rightPressed()
        
    def __handleLeftKeyReleased(self):
        self.ignore(ROTATE_LEFT_KEY + "-up")
        self.accept(ROTATE_LEFT_KEY, self.__handleLeftKeyPressed)
        self.__leftReleased()

    def __handleRightKeyReleased(self):
        self.ignore(ROTATE_RIGHT_KEY + "-up")
        self.accept(ROTATE_RIGHT_KEY, self.__handleRightKeyPressed)
        self.__rightReleased()
        
    def __handleUpKeyPressed(self):
        self.ignore(FORWARD_KEY)
        self.accept(FORWARD_KEY + "-up", self.__handleUpKeyReleased)
        self.__upPressed()
        
    def __handleUpKeyReleased(self):
        self.ignore(FORWARD_KEY + "-up")
        self.accept(FORWARD_KEY, self.__handleUpKeyPressed)
        self.__upReleased()
            
    def __handleDownKeyPressed(self):
        self.ignore(BACKWARDS_KEY)
        self.accept(BACKWARDS_KEY + "-up", self.__handleDownKeyReleased)
        self.__downPressed()
        
    def __handleDownKeyReleased(self):
        self.ignore(BACKWARDS_KEY + "-up")
        self.accept(BACKWARDS_KEY, self.__handleDownKeyPressed)
        self.__downReleased()
        
    def __leftPressed(self):
        assert(self.notify.debug("left pressed"))
        self.leftPressed = self.__enterControlActive(self.leftPressed)

    def __rightPressed(self):
        assert(self.notify.debug("right pressed"))
        self.rightPressed = self.__enterControlActive(self.rightPressed)
        
    def __upPressed(self):
        assert(self.notify.debug("up pressed"))
        self.upPressed = self.__enterControlActive(self.upPressed)
        
    def __downPressed(self):
        assert(self.notify.debug("down pressed"))
        self.downPressed = self.__enterControlActive(self.downPressed)
        
    def __leftReleased(self):
        assert(self.notify.debug("left released"))
        self.leftPressed = self.__exitControlActive(self.leftPressed)

    def __rightReleased(self):
        assert(self.notify.debug("right released"))
        self.rightPressed = self.__exitControlActive(self.rightPressed)
        
    def __upReleased(self):
        assert(self.notify.debug("up released"))
        self.upPressed = self.__exitControlActive(self.upPressed)
        
    def __downReleased(self):
        assert(self.notify.debug("down released"))
        self.downPressed = self.__exitControlActive(self.downPressed)
        
    # __enterControlActive and __exitControlActive are used
    # to update the cannon control 'press reference counts'
    # leftPressed, rightPressed, upPressed, and downPressed
    # are all counts of how many devices (button, keys) are
    # activating that particular cannon control -- so if
    # someone is pressing 'right' on the keyboard and also
    # pressing on the 'right' button with the mouse,
    # rightPressed would be set to 2. A value of zero means
    # that the cannon control is inactive.
    def __enterControlActive(self, input):
        return input + 1

    def __exitControlActive(self, input):
        return max(0, input - 1)
