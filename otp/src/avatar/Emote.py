from otp.otpbase import OTPLocalizer
import types

class Emote:

    EmoteClear = -1
    EmoteEnableStateChanged = 'EmoteEnableStateChanged'

    # Emote data is stored in the order it appears in the SpeedChat m
    # The integer stored is the reference count to the Emote.  If the
    # count goes above zero, it means that the emote is disabled.  Fo
    # a minigame might increment the reference count if it wants to e
    # disable emotes.
    
    def __init__(self):
        self.emoteFunc = None

    def isEnabled(self, index):
        # find the emotes index if we are given a string
        if isinstance(index, types.StringType):
            index = OTPLocalizer.EmoteFuncDict[index]

        if self.emoteFunc == None:
            return 0
        elif self.emoteFunc[index][1] == 0:
            return 1
        return 0

globalEmote = None 
