## Silly PhaseOne speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
SillyPhaseOneMenu = [     
    (OTPLocalizer.SillyHolidayMenuSections[1],            # WORLD
        [60303, 60304, 60305, 60306,]),
    (OTPLocalizer.SillyHolidayMenuSections[2],            # BATTLE
        [60307, 60308,]),
    (OTPLocalizer.SillyHolidayMenuSections[0],            # SILLY METER
        [60301, 60302,]),
    ]
        
class TTSCSillyPhaseOneMenu(SCMenu):
    """
    Speedchat phrases for Silly PhaseOne
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__SillyPhaseOneMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __SillyPhaseOneMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in SillyPhaseOneMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseOne phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseOne phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )