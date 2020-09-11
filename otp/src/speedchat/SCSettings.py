"""SCSettings.py: contains the SCSettings class"""

from SCColorScheme import SCColorScheme
from otp.otpbase import OTPLocalizer

class SCSettings:
    """ SCSettings holds values that are global for an entire SpeedChat
    tree. By convention, these values are accessed through functions
    defined in the SCObject base class (e.g. self.getColorScheme()).

    eventPrefix: string to prepend to all the event names that pertain to
                 this specific SpeedChat instance
    whisperMode: are we whispering?
    colorScheme: an SCColorScheme for this SpeedChat
    submenuOverlap: how much of their parent menu submenus should overlap,
                    in [0..1]
    topLevelOverlap: same as submenuOverlap but for submenus of the top-level
                     menu; None means 'same as submenuOverlap'
    """
    def __init__(self, eventPrefix, whisperMode=0, colorScheme=None,
                 submenuOverlap=OTPLocalizer.SCOsubmenuOverlap, topLevelOverlap=None):
        self.eventPrefix = eventPrefix
        self.whisperMode = whisperMode
        if colorScheme is None:
            colorScheme = SCColorScheme()
        self.colorScheme = colorScheme
        self.submenuOverlap = submenuOverlap
        self.topLevelOverlap = topLevelOverlap
