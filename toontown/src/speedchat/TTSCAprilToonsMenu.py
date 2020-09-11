## April Toon's speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
AprilToonsMenu = [ 
    (OTPLocalizer.AprilToonsMenuSections[1],            # GREETINGS
        [60100, 60101,]),
    (OTPLocalizer.AprilToonsMenuSections[2],            # PLAYGROUNDS
        [60110, 60111, 60112, 60113, 60114, 60115,]),
    (OTPLocalizer.AprilToonsMenuSections[3],            # CHARACTERS
        [60120, 60121, 60122, 60123, 60124, 60125, 60126,]),
    (OTPLocalizer.AprilToonsMenuSections[4],            # ESTATES
        [60130, 60131, 60132, 60133,]),   
    (OTPLocalizer.AprilToonsMenuSections[0],    
        [60140, 60141,]),
    ]
        
class TTSCAprilToonsMenu(SCMenu):
    """
    Speedchat phrases for April Toon's
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__aprilToonsMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __aprilToonsMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in AprilToonsMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link April Toons phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link April Toons phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )