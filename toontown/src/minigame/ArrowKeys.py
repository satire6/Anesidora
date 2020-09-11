"""ArrowKeys.py: contains the ArrowKeys class"""

from pandac.PandaModules import ModifierButtons
from direct.showbase.DirectObject import DirectObject

class ArrowKeys(DirectObject):
    # keyboard controls
    UP_KEY    = "arrow_up"
    DOWN_KEY  = "arrow_down"
    LEFT_KEY  = "arrow_left"
    RIGHT_KEY = "arrow_right"
    JUMP_KEY  = "control"

    UP_INDEX = 0
    DOWN_INDEX = 1
    LEFT_INDEX = 2
    RIGHT_INDEX = 3
    JUMP_INDEX = 4

    NULL_HANDLERS = (None,None,None,None,None)

    def __init__(self):
        self.__jumpPost = 0

        self.setPressHandlers(self.NULL_HANDLERS)
        self.setReleaseHandlers(self.NULL_HANDLERS)

        # disable modifier-button combo messages (i.e. shift-right-key)
        self.origMb = base.buttonThrowers[0].node().getModifierButtons()
        base.buttonThrowers[0].node().setModifierButtons(ModifierButtons())

        self.enable()

    def enable(self):
        self.disable()
        
        # listen for key presses
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.accept(self.JUMP_KEY, self.__jumpKeyPressed)
        
    def disable(self):
        self.__upPressed = 0
        self.__downPressed = 0
        self.__leftPressed = 0
        self.__rightPressed = 0
        self.__jumpPressed = 0
        
        # ignore all key presses
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        self.ignore(self.JUMP_KEY)
        
        self.ignore(self.UP_KEY + '-up')
        self.ignore(self.DOWN_KEY + '-up')
        self.ignore(self.LEFT_KEY + '-up')
        self.ignore(self.RIGHT_KEY + '-up')
        self.ignore(self.JUMP_KEY + '-up')

    def destroy(self):
        """destroy(self): call before deletion of object"""
        base.buttonThrowers[0].node().setModifierButtons(self.origMb)

        # stop listening for events
        events = [self.UP_KEY, self.DOWN_KEY,
                  self.LEFT_KEY, self.RIGHT_KEY, self.JUMP_KEY]
        for event in events:
            self.ignore(event)
            self.ignore(event + '-up')

    # these functions return the instantaneous state of the buttons
    def upPressed(self):
        return self.__upPressed
    def downPressed(self):
        return self.__downPressed
    def leftPressed(self):
        return self.__leftPressed
    def rightPressed(self):
        return self.__rightPressed
    def jumpPressed(self):
        return self.__jumpPressed
        
    def jumpPost(self):
        jumpCache = self.__jumpPost
        self.__jumpPost = 0
        return jumpCache

    # client can set handlers for button presses/releases
    def setPressHandlers(self, handlers):
        if len(handlers) == 4:
            # we got an old style parameter that just used 4
            handlers.append(None)
        assert(len(handlers) == 5)
        self.__checkCallbacks(handlers)
        self.__pressHandlers = handlers
    def setReleaseHandlers(self, handlers):
        if len(handlers) == 4:
            # we got an old style parameter that just used 4
            handlers.append(None)        
        assert(len(handlers) == 5)
        self.__checkCallbacks(handlers)
        self.__releaseHandlers = handlers

    def clearPressHandlers(self):
        self.setPressHandlers(self.NULL_HANDLERS)
    def clearReleaseHandlers(self):
        self.setReleaseHandlers(self.NULL_HANDLERS)

    def __checkCallbacks(self, callbacks):
        for callback in callbacks:
            assert(callback == None or callable(callback))

    def __doCallback(self, callback):
        if callback:
            callback()

    # PRESS/RELEASE HANDLERS
    # KEY PRESS
    def __upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY+"-up", self.__upKeyReleased)
        self.__upPressed = 1
        self.__doCallback(self.__pressHandlers[self.UP_INDEX])

    def __downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY+"-up", self.__downKeyReleased)
        self.__downPressed = 1
        self.__doCallback(self.__pressHandlers[self.DOWN_INDEX])

    def __leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY+"-up", self.__leftKeyReleased)
        self.__leftPressed = 1
        self.__doCallback(self.__pressHandlers[self.LEFT_INDEX])

    def __rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY+"-up", self.__rightKeyReleased)
        self.__rightPressed = 1
        self.__doCallback(self.__pressHandlers[self.RIGHT_INDEX])
        
    def __jumpKeyPressed(self):
        self.ignore(self.JUMP_KEY)
        self.accept(self.JUMP_KEY+"-up", self.__jumpKeyReleased)
        self.__jumpPressed = 1
        self.__jumpPost = 1
        self.__doCallback(self.__pressHandlers[self.JUMP_INDEX])


    # KEY RELEASE
    def __upKeyReleased(self):
        self.ignore(self.UP_KEY+"-up")
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upPressed = 0
        self.__doCallback(self.__releaseHandlers[self.UP_INDEX])

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY+"-up")
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.__downPressed = 0
        self.__doCallback(self.__releaseHandlers[self.DOWN_INDEX])

    def __leftKeyReleased(self):
        self.ignore(self.LEFT_KEY+"-up")
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.__leftPressed = 0
        self.__doCallback(self.__releaseHandlers[self.LEFT_INDEX])

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY+"-up")
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.__rightPressed = 0
        self.__doCallback(self.__releaseHandlers[self.RIGHT_INDEX])
        
    def __jumpKeyReleased(self):
        self.ignore(self.JUMP_KEY+"-up")
        self.accept(self.JUMP_KEY, self.__jumpKeyPressed)
        self.__jumpPressed = 0
        self.__jumpPost = 0
        self.__doCallback(self.__releaseHandlers[self.JUMP_INDEX])
