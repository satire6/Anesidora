## Silly PhaseThree speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
SillyPhaseThreeMenu = [ 
    (OTPLocalizer.SillyHolidayMenuSections[1],            # WORLD
        [60323, 60324, 60325, 60326, 60327,]),
    (OTPLocalizer.SillyHolidayMenuSections[2],            # BATTLE
        [60318, 60319, 60320, 60321, 60322,]),
    ]
        
class TTSCSillyPhaseThreeMenu(SCMenu):
    """
    Speedchat phrases for Silly PhaseThree
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__SillyPhaseThreeMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __SillyPhaseThreeMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in SillyPhaseThreeMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseThree phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Silly PhaseThree phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )