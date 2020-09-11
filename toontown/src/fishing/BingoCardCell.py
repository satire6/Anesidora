#################################################################
# class: BingoCardCell.py
# Purpose: Provide an atmoic cell button that is used to
#          visually represent the Card pieces for the player.
#################################################################

#################################################################
# Direct Specific Modules
#################################################################
from direct.fsm import FSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *

#################################################################
# Toontown Specific Modules
#################################################################
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.fishing import FishPhoto
from toontown.fishing import BingoGlobals

class BingoCardCell(DirectButton, FSM.FSM):
    """ Create a BingoCard Cell that houses all of the
        relevant information about that particular BINGO
        spot of the card. """
    notify = DirectNotifyGlobal.directNotify.newCategory('BingoCardCell')
    #notify.setDebug(True)
    #################################################################
    # Method: __init__
    # Purpose: This method provides initial construction of the Cell.
    #          It initializes the DirectButton and FSM base classes
    #          from which it is derived. In addition, it manually
    #          sets itself to the 'Off' State so that the enterOff
    #          method is called.
    # Input: cellId - Id Number of the Cell
    #        fish - The type of fish it represents with the logo.
    #        parent - The card that to which it belongs.
    #        **kw - OptionDefs for the DirectButton.
    # Output: None
    #################################################################
    def __init__(self, cellId, fish, model, color, parent, **kw):
        assert self.notify.debugStateCall(self)

        self.model = model
        self.color = color
        buttonToUse = self.model.find("**/mickeyButton")
        # Option Definitions for the Cell. This should override any
        # FishPanel specific optiondefs.
        optiondefs = (
            ('relief',                                    None, None),
            ('state',                                 DGG.DISABLED, None),
            ('image',                               buttonToUse, None),
            ('image_color',                          self.color, None),
            ('image_hpr',                              (0,90,0), None),
            ('image_pos',                               (0,0,0), None),
            ('pressEffect',                               False, None),
            )
       
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        FSM.FSM.__init__(self, 'BingoCardCell')
        self.initialiseoptions(BingoCardCell)
       
        # FishPanel Initialization should be completed by this point.
        # Finalize the remaining BingoCardCell initialization.
        self.parent = parent
        self.fish = fish
        # Assign the cell Index of the card
        self.cellId = cellId
        self.request('Off')

    #################################################################
    # Method: destroy
    # Purpose: This method cleans up the Cell so that there are no
    #          persisting memory leaks.
    # Input: None
    # Output: None
    #################################################################
    def destroy(self):
        DirectButton.destroy(self)

    #################################################################
    # Method: setImageTo
    # Purpose: This method sets the image field appropriately
    # Input: NodePath
    # Output: None
    #################################################################
    def setImageTo(self, button):
        button.setHpr(0,90,0)
        button.setPos(0,0,0)
        button.setScale(BingoGlobals.CellImageScale)
        button.setColor(self.color[0], self.color[1], self.color[2], self.color[3])

        self['image'] = button
        self.setImage()

    #################################################################
    # Method: getButtonName
    # Purpose: This method gets the name of the button to use for this fish
    # Input: None
    # Output: None
    #################################################################
    def getButtonName(self):
        genus = self.getFishGenus()
        return BingoGlobals.FishButtonDict[genus][0]

    #################################################################
    # Method: generateLogo
    # Purpose: This method generates the appropriate type of logo
    #           based on its type of Cell, Free or Fish Logo.
    # Input: None
    # Output: None
    #################################################################
    def generateLogo(self):
        buttonName = self.getButtonName()
        buttonToUse = self.model.find("**/" + buttonName)
        self.setImageTo(buttonToUse)

    #################################################################
    # Method: __generateMarkedLogo
    # Purpose: This method generates the actual Marked Logo. At this
    #          point the free logo is cancel button logo so this
    #          SHOULD be CHANGED!!!
    # Input: None
    # Output: None
    #################################################################
    def generateMarkedLogo(self):
        self.setImageTo(self.model.find("**/mickeyButton"))

    #################################################################
    # Method: setFish
    # Purpose: This method sets the type of Fish that this cell
    #          represents.
    # Input: fish - The fish the cell instance represents.
    # Output: None
    ################################################################# 
    def setFish(self, fish):
        if self.fish:
            del self.fish
        self.fish = fish

    #################################################################
    # Method: getFish
    # Purpose: This method returns the type of Fish that the cell
    #          instance represents.
    # Input: None
    # Output: fish - The fish the cell isntance represents.
    ################################################################# 
    def getFish(self):
        return self.fish

    #################################################################
    # Method: getFishGenus
    # Purpose: This method returns the type of Genus of the Fish that
    #          the cell instance represents.
    # Input: None
    # Output: genus - The fish genus the cell instance represents.
    ################################################################# 
    def getFishGenus(self):
        if self.fish == "Free":
            return -1
        
        return self.fish.getGenus()

    #################################################################
    # Method: getFishSpecies
    # Purpose: This method returns the type of Species of the Fish 
    #          that the cell instance represents.
    # Input: None
    # Output: species - The fish species the cell instance represents
    ################################################################# 
    def getFishSpecies(self):
        return self.fish.getSpecies()

    #################################################################
    # Method: enable
    # Purpose: This method requests a state transition to enable
    #          the cell for gameplay use.
    # Input: callback - the callback routine to be called when the
    #                   cell is pressed.
    # Output: None
    ################################################################# 
    def enable(self, callback=None):
        self.request('On', callback)

    #################################################################
    # Method: disable
    # Purpose: This method requests a state transition to disable
    #          the cell for gameplay use. It also hides the fish
    #          logo if it exists.
    # Input: None
    # Output: None
    ################################################################# 
    def disable(self):
        self.request('Off')
        if not self.fish == 'Free':
            # Load the new logo
            self.generateMarkedLogo()  

#################################################################
# Finite State Machine Methods
#################################################################
#  - FSM States:
#     - Off           Transitions To On
#     - On            Transitions To Off
#################################################################

    #################################################################
    # Method: enterOff
    # Purpose: This method disables the Cell Button and removes the
    #          callback method reference.
    # Input: None
    # Output: None
    ################################################################# 
    def enterOff(self):
        self['state'] = DGG.DISABLED
        self['command'] = None

    #################################################################
    # Method: filterOff
    # Purpose: This method filters out the state transitions so that
    #          it only allows valid transition attmepts. It allows
    #          Off to transition to Off or On.
    # Input: request - The Transition State
    #        args - additional arguments
    # Output: None
    ################################################################# 
    def filterOff(self, request, args):
        if request == 'On':
            return (request, args)
        elif request == 'Off':
            return request
        else:
            self.notify.debug("filterOff: Invalid State Transition from Off to %s" %(request))

    #################################################################
    # Method: enterOn
    # Purpose: This method enables the Cell Button and adds a
    #          callback method reference.
    # Input: None
    # Output: None
    ################################################################# 
    def enterOn(self, args):
        # Enable DirectButton Capabilities.
        self['state'] = DGG.NORMAL
        if args[0]:
            self['command'] = Func(args[0],self.cellId).start

    #################################################################
    # Method: filterOn
    # Purpose: This method filters out the state transitions so that
    #          it only allows valid transition attmepts. It allows
    #          On to transition to Off only.
    # Input: request - The Transition State
    #        args - additional arguments
    # Output: None
    ################################################################# 
    def filterOn(self, request, args):
        if request == 'Off':
            return request
        else:
            self.notify.debug("filterOn: Invalid State Transition from Off to %s" %(request))



    
    
