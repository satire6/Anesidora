"""
TTSCGolfMenu.py: contains the TTSCGolfMenu class
"""

# For standalone testing these are useful:
#base.localAvatar.chatMgr.chatInputSpeedChat.addGolfMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.removeGolfMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.speedChat[2].getMenu()

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
GolfMenuGuide = [ 
(OTPLocalizer.GolfMenuSections[1],[4100,4101,4102,4103,4104,4105]),
(OTPLocalizer.GolfMenuSections[2],[4200,4201,4202,4203,4204,4205,4206,4207]),
(OTPLocalizer.GolfMenuSections[3],[4300,4301,4302,4303,4304,4305,4306,4307]),
(OTPLocalizer.GolfMenuSections[0],[4000,4001,4002]),
]

    
class TTSCGolfMenu(SCMenu):
    """
    TTSCGolfMenu represents a menu of TTSCGolfTerminals.
    """
    
    def __init__(self):
        SCMenu.__init__(self)

        # listen for changes to localtoon's golf speedchat messages
        self.accept("golfMessagesChanged", self.__golfMessagesChanged)
        self.__golfMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __golfMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in GolfMenuGuide:
                if section[0] == -1:
                        #This is not a submenu but a terminal!
                        for phrase in section[1]:
                                if phrase not in OTPLocalizer.SpeedChatStaticText:
                                        print ('warning: tried to link golf phrase %s which does not seem to exist' % phrase)
                                        break
                                self.append(SCStaticTextTerminal(phrase))
                else: #this should be a submenu
                        menu = SCMenu()
                        for phrase in section[1]:
                                if phrase not in OTPLocalizer.SpeedChatStaticText:
                                        print ('warning: tried to link golf phrase %s which does not seem to exist' % phrase)                                
                                        break
                                menu.append(SCStaticTextTerminal(phrase))
                    
                        # add the menu to self (SpeedChat won't display empty menus)
                        menuName = str(section[0])
                        self.append( SCMenuHolder(menuName, menu) )
            

