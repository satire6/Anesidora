"""
TTSCBoardingMenu.py: contains the TTSCBoardingMenu class
"""

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer

#this is the structure of the racing menu
BoardingMenuGuide = [ 
(OTPLocalizer.BoardingMenuSections[0], []),
(OTPLocalizer.BoardingMenuSections[1], []),
(OTPLocalizer.BoardingMenuSections[2], []),
(OTPLocalizer.BoardingMenuSections[3],[5005, 5006, 5007, 5008, 5009]),
]

GroupPhrases = [5000, 5001, 5002, 5003, 5004]

ZoneIdsToMsgs = {
    10000 : [GroupPhrases, [5100, 5101, 5102], [5200, 5201, 5202]],
    10100 : [GroupPhrases, [5103], [5203]],
    11100 : [GroupPhrases, [5104], [5204]],
    11200 : [GroupPhrases, [5105, 5106], [5205, 5206]], 
    12000 : [GroupPhrases, [5107, 5108, 5109], [5207, 5208, 5209]],
    12100 : [GroupPhrases, [5110], [5210]],
    13100 : [GroupPhrases, [5111], [5211]],
    13200 : [GroupPhrases, [5112, 5113, 5114, 5115], [5212, 5213, 5214, 5215]],
}

class TTSCBoardingMenu(SCMenu):
    """
    TTSCBoardingMenu represents a menu of TTSCBoardingTerminals.
    """
    def __init__(self, zoneId):
        SCMenu.__init__(self)
        # listen for changes to localtoon's boarding speedchat messages
        self.__boardingMessagesChanged(zoneId)

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __boardingMessagesChanged(self, zoneId):
        # Clear out everything from our menu
        self.clearMenu()
        # If local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for count in xrange(len(BoardingMenuGuide)):
            section = BoardingMenuGuide[count]
            if section[0] == -1:
                # This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link boarding phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: 
                # This should be a submenu, get the list of phrases from the corresponding zoneId
                menu = SCMenu()
                phrases = ZoneIdsToMsgs[zoneId][count]
                for phrase in phrases:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link boarding phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))
                    
                # add the menu to self (SpeedChat won't display empty menus)
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu))