
from pandac.PandaModules import *

from direct.directnotify import DirectNotifyGlobal
import string
from direct.fsm import StateData

AttackPanelHidden = 0
def hideAttackPanel(flag):
    """
    This function is just called by the ~hideAttack or ~showAttack
    magic words.  If flag is true, the attack panel is hidden (so you
    can see what's going on).  If flag is false, the attack panel is
    revealed again.
    """
    global AttackPanelHidden
    AttackPanelHidden = flag
    messenger.send('hide-attack-panel')

class TownBattleAttackPanel(StateData.StateData):
    """
    This is the main menu for choosing an attack, a toon up, run away, or SOS.
    Actually it is just a thin wrapper around the Inventory class
    """

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        return

    def load(self):
        StateData.StateData.load(self)
    
    def unload(self):
        StateData.StateData.unload(self)

    def enter(self):
        StateData.StateData.enter(self)
        # Display the inventory
        if not AttackPanelHidden:
            base.localAvatar.inventory.show()
        # If someone clicks an item, we want to know about it.
        self.accept('inventory-selection', self.__handleInventory)
        self.accept('inventory-run', self.__handleRun)
        self.accept('inventory-sos', self.__handleSOS)
        self.accept('inventory-pass', self.__handlePass)
        self.accept('inventory-fire', self.__handleFire)
        self.accept('hide-attack-panel', self.__handleHide)
        # The battle panel uses up a lot of space onscreen; in
        # particular, it will hide all the chat balloons.  Force these
        # to go to the margins.
        # NametagGlobals.setOnscreenChatForced(1)
        return

    def exit(self):
        StateData.StateData.exit(self)
        # Ignore the inventory selection
        self.ignore('inventory-selection')
        self.ignore('inventory-run')
        self.ignore('inventory-sos')
        self.ignore('inventory-pass')
        self.ignore('inventory-fire')
        self.ignore('hide-attack-panel')
        # Put the inventory away
        base.localAvatar.inventory.hide()
        # Restore the normal chat behavior.
        # NametagGlobals.setOnscreenChatForced(0)
        return
    
    def __handleRun(self):
        doneStatus = {'mode':'Run'}
        messenger.send(self.doneEvent, [doneStatus])
        return
        
    def __handleSOS(self):
        doneStatus = {'mode':'SOS'}
        messenger.send(self.doneEvent, [doneStatus])
        return

    def __handlePass(self):
        doneStatus = {'mode':'Pass'}
        messenger.send(self.doneEvent, [doneStatus])
        return
        
    def __handleFire(self):
        doneStatus = {'mode':'Fire'}
        messenger.send(self.doneEvent, [doneStatus])
        return
    
    def __handleInventory(self, track, level):
        if (base.localAvatar.inventory.numItem(track, level) > 0):
            # Report the selection
            doneStatus = {}
            doneStatus['mode'] = 'Inventory'
            doneStatus['track'] = track
            doneStatus['level'] = level
            messenger.send(self.doneEvent, [doneStatus])
        else:
            self.notify.error(
                "An item we don't have: track %s level %s was selected." %
                [track, level])
        return

    def __handleHide(self):
        # Just used for magic words.
        if AttackPanelHidden:
            base.localAvatar.inventory.hide()
        else:
            base.localAvatar.inventory.show()
        return
