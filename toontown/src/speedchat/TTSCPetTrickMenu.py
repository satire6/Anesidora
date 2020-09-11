"""TTSCPetTrickMenu.py"""

from direct.directnotify import DirectNotifyGlobal
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer
from toontown.pets import PetTricks

class TTSCPetTrickMenu(SCMenu):
    """
    SCPetTrickMenu represents a menu of pet trick-training terminals.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TTSCPetTrickMenu")
    
    def __init__(self):
        SCMenu.__init__(self)

        # listen for changes to the pet trick phrases we have
        self.accept("petTrickPhrasesChanged", self.__phrasesChanged)
        self.__phrasesChanged()

    def destroy(self):
        self.ignore("petTrickPhrasesChanged")
        SCMenu.destroy(self)

    def __phrasesChanged(self, zoneId=0):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        # rebuild our menu
        for trickId in lt.petTrickPhrases:
            if trickId not in PetTricks.TrickId2scIds:
                TTSCPetTrickMenu.notify.warning(
                    'unknown trick ID: %s' % trickId)
            else:
                # there may be multiple msgs per trick
                for msg in PetTricks.TrickId2scIds[trickId]:
                    assert msg in OTPLocalizer.SpeedChatStaticText
                    self.append(SCStaticTextTerminal(msg))
