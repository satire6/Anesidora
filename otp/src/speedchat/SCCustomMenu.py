"""SCCustomMenu.py: contains the SCCustomMenu class"""

from SCMenu import SCMenu
from SCCustomTerminal import SCCustomTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings

class SCCustomMenu(SCMenu):
    """ SCCustomMenu represents a menu of SCCustomTerminals. """
    def __init__(self):
        SCMenu.__init__(self)
        # listen for changes to localtoon's custom speedchat messages
        self.accept("customMessagesChanged", self.__customMessagesChanged)
        self.__customMessagesChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __customMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        for msgIndex in lt.customMessages:
            if CustomSCStrings.has_key(msgIndex):
                self.append(SCCustomTerminal(msgIndex))
