#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: KeyCodes is used to match a pattern sequence of keys input by the player.
#          It requires 1) a series of keys that can be pressed,
#          2) a map with equivalent name for the keys used in the pattern (e.g. arrow_up is u)
#          and 3) a list of key codes (e.g. ["udlrababss", "udud", "lrlr"])
#          These are set during initialization, but patterns can be changed
#          through the listenForPatterns method as well.
#          When a pattern is made, the event KeyCodes.PATTERN_MATCH_EVENT is triggered
#          When the player presses the keys, they have KEYCODE_TIMEOUT_SECONDS
#          to enter the next key, otherwise the creation of the pattern times out.
#-------------------------------------------------------------------------------

from pandac.PandaModules import *

from direct.showbase.DirectObject import DirectObject

ARROW_KEYCODE_MAP = {"arrow_up" : "u",
                     "arrow_down" : "d",
                     "arrow_left" : "l",
                     "arrow_right" : "r",
                     }

KEYCODE_TIMEOUT_SECONDS = 1.5

class KeyCodes(DirectObject):
    notify = directNotify.newCategory("KeyCodes")
    
    PATTERN_MATCH_EVENT = "KeyCodes-PATTERN_MATCH"
    PATTERN_NO_MATCH_EVENT = "KeyCodes-PATTERN_NO_MATCH"
    KEY_DOWN_EVENT = "KeyCodes-KEY_DOWN_EVENT"
    KEY_UP_EVENT = "KeyCodes-KEY_UP_EVENT"
    CLEAR_CODE_EVENT = "KeyCodes-CLEAR_CODE_EVENT"
    
    def __init__(self,
                 keyMap=ARROW_KEYCODE_MAP,
                 patterns=None,
                 timeout=KEYCODE_TIMEOUT_SECONDS):
        """
        Initialize KeyCodes.
        
        Parameters:
            keyMap is map of Panda keys to their pattern name equivalent.
            For example, "arrow_up" -> "u"
        
            patterns is a list of pattern strings that the class will identify.
            For example: "udlrlrababss"
        """
        self._keyMap = keyMap
        self._timeout = timeout
        self._keyCode = ""
        self._keyCodeCount = 0
        self._keyCodeTime = 0.0
        self._patterns = []
        self._patternLimit = 0
        self._enabled = False
        self._keyDown = None
        self._keysPressed = 0
        
        self.listenForPatterns(patterns)
    
    
    def destroy(self):
        self.disable()
        self.ignoreAll()
        
        self._patterns = []
        del self._patterns
        del self._keyMap
        del self._timeout
    
    def listenForPatterns(self, patterns):
        """
        Set the current patterns to list to.
        
        Parameters:
            patterns is a list of pattern strings that the class will identify.
            For example: "udlrlrababss"
        """
        self._patterns = patterns
        for pattern in self._patterns:
            if len(pattern) > self._patternLimit:
                self._patternLimit = len(pattern)
        
        if self._enabled:
            self.disable()
            self.enable()
    
    def isAnyKeyPressed(self):
        return (self._keysPressed > 0)
        
    def getCurrentInputLength(self):
        """
        Returns length of currently entered keycode.
        """
        return self._keyCodeCount + 1
    
    def getLargestPatternLength(self):
        """
        Returns length of largest possible keycode.
        """
        return self._patternLimit
    
    def getPossibleMatchesList(self):
        """
        Returns list of possible matches based on the current entered keycode.
        """
        return [p for p in self._patterns if p.startswith(self._keyCode)]
    
    def reset(self):
        """
        Reset current key code.
        """
        self._keyCode = ""
        self._keyCodeCount = 0
        self._keyCodeTime = 0.0
        
    def enable(self):
        """
        Enable key codes.
        """
        if not self._enabled:
            self.notify.debug("Key codes enabled")
            self._enabled = True
            self.__enableControls()
      
    def disable(self):
        """
        Disable key codes.
        """
        if self._enabled:
            self.notify.debug("Key codes disabled")
            self.__disableControls()
            self.reset()
            self._enabled = False
            self._keyDown = None
            self._keysPressed = 0
    
    def __enableControls(self):
        """
        Enables keys that will be used to create patterns.
        """
        for key in self._keyMap.keys():
            self.__acceptKeyDown(key)
            self.__acceptKeyUp(key)
    
    def __disableControls(self):
        """
        Disables event listeners for pushing keys.
        """
        self.ignoreAll()
        
    def __acceptKeyDown(self, key):
        """
        Accepts when the player pushes down a certain key.
        """
        self.accept(key, self.__handleKeyDown, [key])
    
    def __acceptKeyUp(self, key):
        """
        Accepts when the player releases their finger from a certain key.
        """
        self.accept(key + "-up", self.__handleKeyUp, [key])
    
    def __handleKeyDown(self, key):
        """
        Handles the pressing down of a key. Only record a keypress is no other
        key that the pattern accepts is pressed and it's the first key to be
        pressed down.
        """
        self._keysPressed += 1
        if self._keyDown is None and self._keysPressed == 1:
            assert(self.notify.debug("Key Down for Pattern: " +  key))
            self.__updateElapsedTime()
            # Inform that a key has been pressed
            messenger.send(KeyCodes.KEY_DOWN_EVENT, [self._keyMap[key], self._keyCodeCount])
            
            self._keyCode += self._keyMap[key]
            self._keyCodeCount += 1
            self._keyDown = key
            self.__checkForPattern()
        else:
            messenger.send(KeyCodes.KEY_DOWN_EVENT, [-1, -1])
        
    
    def __handleKeyUp(self, key):
        """
        Handles the pressing up of a key.
        If the key that was last added to the pattern is down, then set it to up
        and make it available to accept another key into the pattern.
        """
        arg = -1
        if self._keysPressed > 0:
            self._keysPressed -= 1
            if self._keyDown == key and self._keysPressed == 0:
                arg = self._keyMap[key]
                      
        if self._keysPressed == 0:
            self._keyDown = None
            
        messenger.send(KeyCodes.KEY_UP_EVENT, [arg])
            
    def __updateElapsedTime(self):
        """
        Updates the code time with the most recent frame time.
        If player is pressing a key, and it's been too long,
        then reset the code sequence.
        """
        if self._keyCodeTime != 0.0 and \
                (globalClock.getFrameTime() - self._keyCodeTime) >= self._timeout:
                self.notify.debug("Key code timed out. Resetting...")
                self.reset()
                messenger.send(KeyCodes.CLEAR_CODE_EVENT)
        self._keyCodeTime = globalClock.getFrameTime()
        
    def __checkForPattern(self):
        """
        Checks to see if a pattern has been matched.
        Note that pattern matching is first come first serve, meaning that if abab is
        before ababcd, then ababcd will never be matched.
        """
        if self._keyCode in self._patterns:
            assert(self.notify.debug("Pattern Match: " +  self._keyCode))
            messenger.send(KeyCodes.PATTERN_MATCH_EVENT, [self._keyCode])
            self.reset()
            
        # If the key code is longer than the longest pattern possible,
        # Then reset!            
        elif self._keyCodeCount == self._patternLimit or len(self.getPossibleMatchesList()) == 0:
            assert(self.notify.debug("No pattern match!"))
            messenger.send(KeyCodes.PATTERN_NO_MATCH_EVENT)
            self.reset()
            
            
            