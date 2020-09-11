"""
TTSCFactoryMenu.py: contains the TTSCFactoryMenu class

For standalone testing these are useful:
base.localAvatar.chatMgr.chatInputSpeedChat.addFactoryMenu()
base.localAvatar.chatMgr.chatInputSpeedChat.removeFactoryMenu()
base.localAvatar.chatMgr.chatInputSpeedChat.speedChat[2].getMenu()

"""

from otp.speedchat.SCMenu import SCMenu
from otp.speedchat import SCMenuHolder
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from otp.otpbase import OTPLocalizer

# TODO: create a table for each factory
ZoneToMsgs = {
    3: [1803, 1903],
    4: [1804, 1904],
    5: [1805, 1905],
    6: [1806, 1906],
    7: [1807, 1907],
    8: [1808, 1908],
    9: [1809, 1909],
    10: [1810, 1910],
    11: [1811, 1911],
    12: [1812, 1912],
    13: [1813, 1913],
    14: [1814, 1914],
    15: [1815, 1915],
    16: [1816, 1916],
    17: [1817, 1917],
    18: [1818, 1918],
    19: [1819, 1919],
    20: [1820, 1920],
    21: [1821, 1921],
    22: [1822, 1922],
    23: [1823, 1923],
    24: [1824, 1924],
    25: [1825, 1925],
    27: [1827, 1927],
    30: [1830, 1930],
    31: [1831, 1931],
    32: [1832, 1932],
    33: [1833, 1933],
    34: [1834, 1934],
    35: [1835, 1935],
    36: [1836, 1936],
    37: [1837, 1937],
    38: [1838, 1938],
    40: [1840, 1940],
    41: [1841, 1941],
    60: [1860, 1960],
    61: [1861, 1961],
    }
# Messages you always want in any zone
GLOBAL_MSGS = [1700, 1701, 1702, 1703, 1704,]

class TTSCFactoryMenu(SCMenu):
    """
    SCFactoryMenu represents a menu of factory-related terminals.
    """
    
    def __init__(self):
        SCMenu.__init__(self)

        self.meetMenuHolder = None
        # the meet menu really only makes sense for Sellbot HQ
        zoneId = base.cr.playGame.getPlaceId()
        if zoneId and (zoneId == 11000):
            meetMenu = SCMenu()
            for msgIndex in OTPLocalizer.SCFactoryMeetMenuIndexes:
                term = SCStaticTextTerminal(msgIndex)
                meetMenu.append(term)
            self.meetMenuHolder = SCMenuHolder.SCMenuHolder(OTPLocalizer.SCMenuFactoryMeet,
                                                            meetMenu)
            self[0:0] = [self.meetMenuHolder]

        # listen for changes to the factory location
        self.accept("factoryZoneChanged", self.__zoneChanged)
        self.__zoneChanged()

    def destroy(self):
        self.ignore("factoryZoneChanged")
        SCMenu.destroy(self)

    def __zoneChanged(self, zoneId=0):

        # save the meet menu if we have one
        if self.meetMenuHolder:
            del self[0]
            
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        # keep a list of the phrases we've added to the menu, to
        # detect duplicates
        phrases = []
        def addTerminal(terminal, self=self, phrases=phrases):
            displayText = terminal.getDisplayText()
            if displayText not in phrases:
                self.append(terminal)
                phrases.append(displayText)

        # rebuild our menu
        # Everybody gets the global messages
        # Plus add the ones for the zone you are in if you have some
        for msg in (GLOBAL_MSGS + ZoneToMsgs.get(zoneId, [])):
            assert (msg in OTPLocalizer.SpeedChatStaticText)
            addTerminal(SCStaticTextTerminal(msg))

        # put the meet menu back, if we had one
        if self.meetMenuHolder:
            self[0:0] = [self.meetMenuHolder]
