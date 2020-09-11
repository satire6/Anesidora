## Victory Parties speedchat phrases ##

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
from toontown.speedchat.TTSCIndexedTerminal import TTSCIndexedTerminal
from otp.otpbase import OTPLocalizer


#this is the structure of the victory parties menu
VictoryPartiesMenu = [ 
    (OTPLocalizer.VictoryPartiesMenuSections[1],[60350, 60351, 60352, 60353, 60354]),
    (OTPLocalizer.VictoryPartiesMenuSections[2],[60355, 60356, 60357, 60358, 60359, 60360, 60361]),
    (OTPLocalizer.VictoryPartiesMenuSections[0],[]),
    ]
        
class TTSCVictoryPartiesMenu(SCMenu):
    """
    Speedchat phrases for Victory Parties
    """
    
    def __init__(self):
        SCMenu.__init__(self)        
        
        self.__messagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __messagesChanged(self):
        """
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in VictoryPartiesMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1].keys():
                    blatherTxt = section[1][phrase]
                    if blatherTxt not in OTPLocalizer.SpeedChatStaticText:
                        self.notify.warning("tried to link Victory Parties phrase %s which does not seem to exist" % blatherTxt)
                        break
                    self.append(TTSCIndexedTerminal(SpeedChatStaticText.get(phrase, None), blatherTxt))
            else: 
            #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        self.notify.warning("tried to link Victory Parties phrase %s which does not seem to exist" % phrase)
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )
        """
        
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for section in VictoryPartiesMenu:
            if section[0] == -1:
                #This is not a submenu but a terminal!
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Victory Parties phrase %s which does not seem to exist' % phrase)
                        break
                    self.append(SCStaticTextTerminal(phrase))
            else: #this should be a submenu
                menu = SCMenu()
                for phrase in section[1]:
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link Victory Parties phrase %s which does not seem to exist' % phrase)                                
                        break
                    menu.append(SCStaticTextTerminal(phrase))                    
                                        
                menuName = str(section[0])
                self.append( SCMenuHolder(menuName, menu) )
                