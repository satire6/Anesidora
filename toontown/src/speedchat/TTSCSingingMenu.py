"""
TTSCSingingMenu.py: contains the TTSCSingingMenu class
"""

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from TTSCSingingTerminal import TTSCSingingTerminal
from otp.otpbase import OTPLocalizer

#this is the structure of the racing menu
SingingMenuGuide = [ 
(OTPLocalizer.SingingMenuSections[0], [{9000:25}, {9001:26}, {9002:27}, {9003:28}, {9004:29}, {9005:30}, {9006:31}, {9007:32}, {9008:33}]),
]

class TTSCSingingMenu(SCMenu):
    """
    TTSCSingingMenu represents a menu of TTSCSingingTerminals.
    """
    def __init__(self):
        SCMenu.__init__(self)
        # listen for changes to localtoon's singing speedchat messages
        self.__singingMessagesChanged()
        if __debug__:
            base.smenu = self

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __singingMessagesChanged(self):
        # Clear out everything from our menu
        self.clearMenu()
        # If local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return 
        for count in xrange(len(SingingMenuGuide)):
            section = SingingMenuGuide[count]
            if section[0] == -1:
                # This is not a submenu but a terminal!
                for phrase in section[1]:
                    emote = None
                    # If the type of the phrase is a dictionary there must be an emote attached to it.
                    if (type(phrase) == type({})):
                        assert len(phrase.keys()) == 1
                        item = phrase.keys()[0]
                        emote = phrase[item]
                        phrase = item
                    if phrase not in OTPLocalizer.SpeedChatStaticText:
                        print ('warning: tried to link a singing phrase %s which does not seem to exist' % phrase)
                        break
                    terminal = TTSCSingingTerminal(phrase)                    
                    if emote is not None:
                        terminal.setLinkedEmote(emote)
                    self.append(terminal)
##            else: 
##                # This should be a submenu, get the list of phrases from the corresponding zoneId
##                mmenu = SCMenu()
##                for phrase in section[1]:
##                    if phrase not in OTPLocalizer.SpeedChatStaticText:
##                        print ('warning: tried to link a singing phrase %s which does not seem to exist' % phrase)                                
##                        break
##                    menu.append(SCStaticTextTerminal(phrase))
##                    
##                # add the menu to self (SpeedChat won't display empty menus)
##                menuName = str(section[0])
##                self.append(SCMenuHolder(menuName, menu))