"""SCEmoteTerminal.py: contains the SCEmoteTerminal class"""

from direct.gui.DirectGui import *
from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import EmoteList, EmoteWhispers
from otp.avatar import Emote

# args: emoteId
SCEmoteMsgEvent = 'SCEmoteMsg'
# args: none
SCEmoteNoAccessEvent = 'SCEmoteNoAccess'

# emote terminals don't produce any spoken text
# when whispered, they produce msgs like 'Flippy waves'
def decodeSCEmoteWhisperMsg(emoteId, avName):
    if emoteId >= len(EmoteWhispers):
        return None
    return EmoteWhispers[emoteId] % avName

class SCEmoteTerminal(SCTerminal):
    """ SCEmoteTerminal represents a terminal SpeedChat node that
    contains an emotion. """
    def __init__(self, emoteId):
        SCTerminal.__init__(self)
        self.emoteId = emoteId
        # look up the emote name that should be displayed
        if not self.__ltHasAccess():
            self.text = '?'
        else:
            self.text = EmoteList[self.emoteId]

    def __ltHasAccess(self):
        # returns non-zero if localToon has access to this emote
        #
        # Note that the current design stipulates that this object
        # will be destroyed and replaced by the SCEmoteMenu if and
        # when the lt's emote-access state changes. Therefore the
        # result of this function should be constant throughout
        # the lifetime of the object.
        try:
            lt = base.localAvatar
            return lt.emoteAccess[self.emoteId]
        except:
            return 0

    def __emoteEnabled(self):
        # all of the emotes are always available for whispering
        if self.isWhispering():
            return 1
        assert Emote.globalEmote != None
        return Emote.globalEmote.isEnabled(self.emoteId)

    def finalize(self, dbArgs={}):
        if not self.isDirty():
            return

        args = {}

        if ((not self.__ltHasAccess()) or
            (not self.__emoteEnabled())):
            # make the button 'unclickable'
            args.update({
                'rolloverColor': (0,0,0,0),
                'pressedColor': (0,0,0,0),
                'rolloverSound': None,
                'text_fg': self.getColorScheme().getTextDisabledColor()+(1,),
                })
        if not self.__ltHasAccess():
            # if localToon doesn't have access to this emote, the
            # button has a '?' on it. make sure it's centered
            args.update({
                'text_align': TextNode.ACenter,
                })
        elif not self.__emoteEnabled():
            # don't play a sound if user clicks on a disabled emote
            # that they have access to
            args.update({
                'clickSound': None,
            })

        self.lastEmoteEnableState = self.__emoteEnabled()
        
        args.update(dbArgs)
        SCTerminal.finalize(self, dbArgs=args)

    def __emoteEnableStateChanged(self):
        if self.isDirty():
            # we're marked as dirty, don't bother trying to change
            # our appearance here; we may not even have a button yet
            self.notify.info(
                "skipping __emoteEnableStateChanged; we're marked as dirty")
            return
        elif not hasattr(self, 'button'):
            self.notify.error(
                "SCEmoteTerminal is not marked as dirty, but has no button!")

        btn = self.button
        if self.__emoteEnabled():
            rolloverColor = self.getColorScheme().getRolloverColor()+(1,)
            pressedColor = self.getColorScheme().getPressedColor()+(1,)
            btn.frameStyle[DGG.BUTTON_ROLLOVER_STATE].setColor(*rolloverColor)
            btn.frameStyle[DGG.BUTTON_DEPRESSED_STATE].setColor(*pressedColor)
            btn.updateFrameStyle()
            btn['text_fg'] = (
                self.getColorScheme().getTextColor()+(1,))
            btn['rolloverSound'] = DGG.getDefaultRolloverSound()
            btn['clickSound'] = DGG.getDefaultClickSound()
        else:
            btn.frameStyle[DGG.BUTTON_ROLLOVER_STATE].setColor(0,0,0,0)
            btn.frameStyle[DGG.BUTTON_DEPRESSED_STATE].setColor(0,0,0,0)
            btn.updateFrameStyle()
            btn['text_fg'] = (
                self.getColorScheme().getTextDisabledColor()+(1,))
            btn['rolloverSound'] = None
            btn['clickSound'] = None

    def enterVisible(self):
        SCTerminal.enterVisible(self)
        if self.__ltHasAccess():
            # if the emote enable state has changed since the last time
            # we were finalized, invalidate
            if hasattr(self, 'lastEmoteEnableState'):
                if self.lastEmoteEnableState != self.__emoteEnabled():
                    self.invalidate()
                    
            if not self.isWhispering():
                self.accept(Emote.globalEmote.EmoteEnableStateChanged,
                            self.__emoteEnableStateChanged)

    def exitVisible(self):
        SCTerminal.exitVisible(self)
        self.ignore(Emote.globalEmote.EmoteEnableStateChanged)

    # from SCTerminal
    def handleSelect(self):
        if not self.__ltHasAccess():
            messenger.send(self.getEventName(SCEmoteNoAccessEvent))
        else:
            if self.__emoteEnabled():
                # calling this makes the speedchat menu go away
                SCTerminal.handleSelect(self)
                messenger.send(self.getEventName(SCEmoteMsgEvent),
                               [self.emoteId])
