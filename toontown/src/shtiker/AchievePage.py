"""AchievePage module: contains the AchievePage class"""

import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class AchievePage(ShtikerPage.ShtikerPage):
    """AchievePage class"""

    # special methods
    def __init__(self):
        """__init__(self)
        AchievePage constructor: create the achieve selector page
        """
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.AchievePageTitle,
            text_scale = 0.12,
            pos = (0,0,0.6),
            )

    def unload(self):
        del self.title
        ShtikerPage.ShtikerPage.unload(self)
