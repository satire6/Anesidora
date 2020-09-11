"""SCEmoteMenu.py: contains the SCEmoteMenu class"""

from SCMenu import SCMenu
from SCEmoteTerminal import SCEmoteTerminal

class SCEmoteMenu(SCMenu):
    """ SCEmoteMenu represents a menu of SCEmoteTerminals. """
    def __init__(self):
        SCMenu.__init__(self)
        self.accept('emotesChanged', self.__emoteAccessChanged)
        self.__emoteAccessChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __emoteAccessChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        for i in range(len(lt.emoteAccess)):
            # Only add entries we actually have.
            if lt.emoteAccess[i]:
                self.append(SCEmoteTerminal(i))
