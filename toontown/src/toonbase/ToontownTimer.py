from otp.otpbase.OTPTimer import OTPTimer
from pandac.PandaModules import *

class ToontownTimer(OTPTimer):
    """
    Implements the generic onscreen Toontown timer.
    """

    def __init__(self, useImage=True, highlightNearEnd=True):
        # Initialize the parental stuff
        OTPTimer.__init__(self, useImage, highlightNearEnd)
        self.initialiseoptions(ToontownTimer)   

    def getImage(self):
        """
        Returns the image suitable for rendering the clock face.  This
        is loaded once if it has not been loaded before.  This
        function is useful to prevent loading this image (and leaking
        it) every time a ToontownTimer is created.
        """
        if ToontownTimer.ClockImage == None:
            model = loader.loadModel("phase_3.5/models/gui/clock_gui")
            ToontownTimer.ClockImage = model.find("**/alarm_clock")
            model.removeNode()
        return ToontownTimer.ClockImage
