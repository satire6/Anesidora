"""SCTerminal.py: contains the SCTerminal class"""

from SCElement import SCElement
from SCObject import SCObject
from SCMenu import SCMenu
from direct.fsm.StatePush import StateVar, FunctionCall
from direct.showbase.DirectObject import DirectObject
from otp.avatar import Emote

# this event is generated whenever any SpeedChat terminal is chosen
# args: none
SCTerminalSelectedEvent = 'SCTerminalSelected'
# this event is generated if the selected terminal has a linked emote
# args: emoteId
SCTerminalLinkedEmoteEvent = 'SCTerminalLinkedEmoteEvent'
# someone needs to generate this event whenever the speedchat tree goes
# in or out of whisper mode
SCWhisperModeChangeEvent = 'SCWhisperModeChange'

class SCTerminal(SCElement):
    """ SCTerminal is the base class for all 'terminal' speedchat
    entities """
    def __init__(self, linkedEmote=None):
        SCElement.__init__(self)
        self.setLinkedEmote(linkedEmote)

        scGui = loader.loadModel(SCMenu.GuiModelName)
        self.emotionIcon = scGui.find('**/emotionIcon')
        self.setDisabled(False)
        self.__numCharges = -1

        # should we listen for whisper mode changes?
        self._handleWhisperModeSV = StateVar(False)
        # can't set this up until we're ready to have the handler func called
        self._handleWhisperModeFC = None

    def destroy(self):
        self._handleWhisperModeSV.set(False)
        if self._handleWhisperModeFC:
            self._handleWhisperModeFC.destroy()
        self._handleWhisperModeSV.destroy()
        SCElement.destroy(self)

    def privSetSettingsRef(self, settingsRef):
        SCElement.privSetSettingsRef(self, settingsRef)
        if self._handleWhisperModeFC is None:
            self._handleWhisperModeFC = FunctionCall(self._handleWhisperModeSVChanged,
                                                     self._handleWhisperModeSV)
            self._handleWhisperModeFC.pushCurrentState()
        # if this terminal is not whisperable, we need to listen for whisper mode changes
        self._handleWhisperModeSV.set((self.settingsRef is not None) and
                                      (not self.isWhisperable()))

    def _handleWhisperModeSVChanged(self, handleWhisperMode):
        if handleWhisperMode:
            # this terminal can't be whispered. we need to reconstruct
            # our GUI element when the whisper mode changes
            # listen for that mode change
            # create a DirectObject to avoid conflicts with other parts of this
            # object that are listening for this event
            self._wmcListener = DirectObject()
            self._wmcListener.accept(self.getEventName(SCWhisperModeChangeEvent),
                                     self._handleWhisperModeChange)
        else:
            if hasattr(self, '_wmcListener'):
                # we no longer need to listen for whisper mode changes
                self._wmcListener.ignoreAll()
                del self._wmcListener
                # make sure our GUI element is appropriate
                self.invalidate()

    def _handleWhisperModeChange(self, whisperMode):
        # whisper mode changed, we need to change our GUI element
        self.invalidate()

    # the meat of SCTerminal; inheritors should override this
    # and perform the appropriate action
    def handleSelect(self):
        """ called when the user selects this node """
        # send the generic 'something was selected' event
        messenger.send(self.getEventName(SCTerminalSelectedEvent))

        # if we have a linked emote, and it isn't disabled, generate a msg
        if self.hasLinkedEmote() and self.linkedEmoteEnabled():
                messenger.send(self.getEventName(SCTerminalLinkedEmoteEvent),
                               [self.linkedEmote])

    def isWhisperable(self):
        # can this terminal be sent as a whisper message?
        return True

    # Some terminal nodes have an emote associated with them, which
    # should be invoked when the node is selected.
    def getLinkedEmote(self):
        return self.linkedEmote
    def setLinkedEmote(self, linkedEmote):
        self.linkedEmote = linkedEmote
        # TODO: we should make sure we're listening for emote
        # enable state changes if this is set while we're visible
        self.invalidate()
    def hasLinkedEmote(self):
        return (self.linkedEmote is not None)
    def linkedEmoteEnabled(self):
        if Emote.globalEmote:
            return Emote.globalEmote.isEnabled(self.linkedEmote)

    def getCharges(self):
        return self.__numCharges
    
    def setCharges(self, nCharges):
        self.__numCharges = nCharges
        if (nCharges is 0):
            self.setDisabled(True)
    
    # support for disabled terminals
    def isDisabled(self):
        return self.__disabled or (self.isWhispering() and not self.isWhisperable())

    def setDisabled(self, bDisabled):
        # make the button 'unclickable'
        self.__disabled = bDisabled

    # from SCElement
    def onMouseClick(self, event):
        if not self.isDisabled():
            SCElement.onMouseClick(self, event)
            self.handleSelect()

    def getMinDimensions(self):
        width, height = SCElement.getMinDimensions(self)
        if self.hasLinkedEmote():
            # add space for the emotion icon
            width += 1.3
        return width, height

    def finalize(self, dbArgs={}):
        """ catch this call and influence the appearance of our button """
        if not self.isDirty():
            return

        args = {}

        if self.hasLinkedEmote():
            self.lastEmoteIconColor = self.getEmoteIconColor()
            self.emotionIcon.setColorScale(*self.lastEmoteIconColor)
            args.update({
                'image':         self.emotionIcon,
                'image_pos':     (self.width-.6,0,-self.height*.5),
                })

        if self.isDisabled():
            args.update({
                'rolloverColor': (0,0,0,0),
                'pressedColor': (0,0,0,0),
                'rolloverSound': None,
                'clickSound': None,
                'text_fg': self.getColorScheme().getTextDisabledColor()+(1,),
                })

        args.update(dbArgs)
        SCElement.finalize(self, dbArgs=args)

    def getEmoteIconColor(self):
        if self.linkedEmoteEnabled() and (not self.isWhispering()):
            r,g,b = self.getColorScheme().getEmoteIconColor()
        else:
            r,g,b = self.getColorScheme().getEmoteIconDisabledColor()
        return (r,g,b,1)

    def updateEmoteIcon(self):
        if hasattr(self, 'button'):
            self.lastEmoteIconColor = self.getEmoteIconColor()
            for i in range(self.button['numStates']):
                self.button['image%s_image' % i].setColorScale(
                    *self.lastEmoteIconColor)
        else:
            self.invalidate()

    # from SCObject
    def enterVisible(self):
        SCElement.enterVisible(self)

        # Check if the emote state has changed since the last time
        # we were finalized, and invalidate if it's different.
        if hasattr(self, 'lastEmoteIconColor'):
            if self.getEmoteIconColor() != self.lastEmoteIconColor:
                self.invalidate()

        # listen for whisper-mode changes
        def handleWhisperModeChange(whisperMode, self=self):
            if self.hasLinkedEmote():
                # we are leaving or entering whisper mode;
                # the appearance of our emote icon needs to change
                # (no linked emotes on whispers)
                if self.isVisible() and not self.isWhispering():
                    self.updateEmoteIcon()
        self.accept(self.getEventName(SCWhisperModeChangeEvent),
                    handleWhisperModeChange)

        # listen for emote-enable state changes
        def handleEmoteEnableStateChange(self=self):
            if self.hasLinkedEmote():
                # emotions have just become enabled/disabled
                # update our emote icon
                # (no emotes when whispering)
                if self.isVisible() and not self.isWhispering():
                    self.updateEmoteIcon()
        if self.hasLinkedEmote():
            if Emote.globalEmote:
                self.accept(Emote.globalEmote.EmoteEnableStateChanged,
                            handleEmoteEnableStateChange)

    def exitVisible(self):
        SCElement.exitVisible(self)
        self.ignore(self.getEventName(SCWhisperModeChangeEvent))
        if Emote.globalEmote:
            self.ignore(Emote.globalEmote.EmoteEnableStateChanged)

    def getDisplayText(self):
        if self.getCharges() is not -1:
            return self.text + " (%s)" % self.getCharges()
        else:
            return self.text

