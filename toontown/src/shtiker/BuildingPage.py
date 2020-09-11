"""BuildingPage module: contains the BuildingPage class"""

import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class BuildingPage(ShtikerPage.ShtikerPage):
    """BuildingPage class"""

    # special methods
    def __init__(self):
        """__init__(self)
        BuildingPage constructor: create the building selector page
        """
        ShtikerPage.ShtikerPage.__init__(self)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.BuildingPageTitle,
            text_scale = 0.12,
            pos = (0,0,0.6),
            )

    def unload(self):
        del self.title
        ShtikerPage.ShtikerPage.unload(self)
