"""DistributedWitchMinnie module: contains the DistributedWitchMinnie class"""

from pandac.PandaModules import *
import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.classicchars import DistributedMinnie
import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import DistributedCCharBase

class DistributedWitchMinnie(DistributedMinnie.DistributedMinnie):
    """DistributedWitchMinnie class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedWitchMinnie")

    def __init__(self, cr):
        try:
            self.DistributedMinnie_initialized
        except:
            self.DistributedMinnie_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr,
                                                               TTLocalizer.WitchMinnie,
                                                               'wmn')
            self.fsm = ClassicFSM.ClassicFSM(self.getName(),
                            [State.State('Off',
                                         self.enterOff,
                                         self.exitOff,
                                         ['Neutral']),
                             State.State('Neutral',
                                         self.enterNeutral,
                                         self.exitNeutral,
                                         ['Walk']),
                             State.State('Walk',
                                         self.enterWalk,
                                         self.exitWalk,
                                         ['Neutral']),
                             ],
                             # Initial State
                             'Off',
                             # Final State
                             'Off',
                             )

            self.fsm.enterInitialState()
            
            # We want him to show up as Minnie
            self.nametag.setName(TTLocalizer.Minnie)
            
    def walkSpeed(self):
        return ToontownGlobals.WitchMinnieSpeed
