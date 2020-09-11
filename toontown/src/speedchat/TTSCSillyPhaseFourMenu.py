## Silly PhaseFour speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
SillyPhaseFourMenu = [ 
    (OTPLocalizer.SillyHolidayMenuSections[1],            # WORLD
        [60325, 60326, 60327,]),
    (OTPLocalizer.SillyHolidayMenuSections[2],            # BATTLE
        [60329, 60330, 60331, 60332,]),
    ]
        
class TTSCSillyPhaseFourMenu(SCMenu):
    """
    Speedchat phrases for Silly PhaseFour
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__SillyPhaseFourMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __SillyPhaseFourMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in SillyPhaseFourMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseFour phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseFour phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )