"""
TTSCResistanceMenu.py: contains the TTSCResistanceMenu class
"""

# For standalone testing these are useful:
#base.localAvatar.chatMgr.chatInputSpeedChat.addResistanceMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.removeResistanceMenu()
#base.localAvatar.chatMgr.chatInputSpeedChat.speedChat[2].getMenu()

from direct.showbase import PythonUtil
from otp.speedchat.SCMenu import SCMenu
from otp.speedchat.SCMenuHolder import SCMenuHolder
from toontown.chat import ResistanceChat
#from toontown.toonbase.TTLocalizer import ResistanceSCStrings
from TTSCResistanceTerminal import TTSCResistanceTerminal

class TTSCResistanceMenu(SCMenu):
    """
    TTSCResistanceMenu represents a menu of TTSCResistanceTerminals.
    """
    
    def __init__(self):
        SCMenu.__init__(self)

        # listen for changes to localtoon's resistance speedchat messages
        self.accept("resistanceMessagesChanged", self.__resistanceMessagesChanged)
        self.__resistanceMessagesChanged()
        submenus = []

    def destroy(self):
        SCMenu.destroy(self)

    def clearMenu(self):
        SCMenu.clearMenu(self)

    def __resistanceMessagesChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        #create the necessary items in the appropriate submenus
        phrases = lt.resistanceMessages
        #create the menus
        for menuIndex in ResistanceChat.resistanceMenu:
            # build a submenu of a particular type (toonup, etc)
            menu = SCMenu()
            for itemIndex in ResistanceChat.getItems(menuIndex):
                textId = ResistanceChat.encodeId(menuIndex, itemIndex)
                charges = lt.getResistanceMessageCharges(textId)
                if charges > 0:
                    menu.append(TTSCResistanceTerminal(textId, charges))
                    
            # add the menu to self (SpeedChat won't display empty menus)
            textId = ResistanceChat.encodeId(menuIndex, 0)
            menuName = ResistanceChat.getMenuName(textId)
            self.append( SCMenuHolder(menuName, menu) )
            
