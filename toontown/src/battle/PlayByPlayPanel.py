
from pandac.PandaModules import *
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toonbase.ToontownGlobals import *
from SuitBattleGlobals import *

from direct.directnotify import DirectNotifyGlobal
from direct.gui import OnscreenText

class PlayByPlayText(OnscreenText.OnscreenText):
    """
    This shows info about names of attacks as they happen, etc.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayByPlayText')

    def __init__(self):
        OnscreenText.OnscreenText.__init__(
            self, 
            mayChange = 1,
            pos = (0.0, 0.75),
            scale = 0.1,
            font = getSignFont(),
            )

    
