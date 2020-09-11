## April Toon's speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the racing menu
CarolMenu = [ 
    (OTPLocalizer.CarolMenuSections[0],    
        {60200:60220, 60201:60221, 60202:60222, 60203:60223, 60204:60224, 60205:60225}),
    ]
        
class TTSCCarolMenu(SCMenu):
    """
    Speedchat phrases for Caroling
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__carolMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __carolMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in CarolMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1].keys():
                    blatherTxt = section[1][phrase]
                    if blatherTxt not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Carol phrase %s which does not seem to exist' % blatherTxt)
                        break
                    self.append(TTSCIndexedTerminal(SpeedChatStaticText.get(phrase, None), blatherTxt))
            else: 
            #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Carol phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )