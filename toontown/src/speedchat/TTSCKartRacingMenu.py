"""
TTSCKartRacingMenu.py: contains the TTSCKartRacingMenu class
"""

# For standalone testing these are useful:
#base.localAvatar.chatMgr.chatInputSpeedChat.addKartRacingMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.removeKartRacingMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.speedChat[2].getMenu()

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
KartRacingMenuGuide = [ 
(OTPLocalizer.KartRacingMenuSections[1],[3130,3160,3190,3170,3180,3150,3110]),
(OTPLocalizer.KartRacingMenuSections[2],[3200,3201,3210,3211,3220,3221,3222,3223,3224,3225,3230,3231,3232,3233,3234,3235]),
(OTPLocalizer.KartRacingMenuSections[3],[3600,3601,3602,3603,3640,3641,3642,3643,3660,3661,3662,3663]),
(OTPLocalizer.KartRacingMenuSections[4],[3300,3301,3310,3320,3330,3340,3350,3360]),
(OTPLocalizer.KartRacingMenuSections[5],[3410,3400,3430,3450,3451,3452,3453,3460,3461,3462,3470]),
(OTPLocalizer.KartRacingMenuSections[0],[3010,3020,3030,3040,3050,3060,3061]),
]

    
class TTSCKartRacingMenu(SCMenu):
    """
    TTSCKartRacingMenu represents a menu of TTSCKartRacingTerminals.
    """
    
    def __init__(self):
        SCMenu.__init__(self)

        # listen for changes to localtoon's kartRacing speedchat messages
        self.accept("kartRacingMessagesChanged", self.__kartRacingMessagesChanged)
        self.__kartRacingMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __kartRacingMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in KartRacingMenuGuide:
                if section[0] == -1:
                        #This is not a submenu but a terminal!
                        for phrase in section[1]:
                                if phrase not in OTPLocalizer.SpeedChatStaticText:
                                        print ('warning: tried to link kart phrase %s which does not seem to exist' % phrase)
                                        break
                                self.append(SCStaticTextTerminal(phrase))
                else: #this should be a submenu
                        menu = SCMenu()
                        for phrase in section[1]:
                                if phrase not in OTPLocalizer.SpeedChatStaticText:
                                        print ('warning: tried to link kart phrase %s which does not seem to exist' % phrase)                                
                                        break
                                menu.append(SCStaticTextTerminal(phrase))
                    
                            # add the menu to self (SpeedChat won't display empty menus)
                        menuName = str(section[0])
                        self.append( SCMenuHolder(menuName, menu) )
            

