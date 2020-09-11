from direct.showbase.ShowBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from toontown.toon import LaffMeter
from toontown.toonbase import TTLocalizer

# simple way for players to see how many treasures have been gotten
class TreasureScorePanel(DirectFrame):
    def __init__(self):

        
        # initialize our base class.
        DirectFrame.__init__(self,
                             relief = None,
                             image_color = GlobalDialogColor,
                             image_scale = (0.24, 1.0, 0.24),
                             image_pos = (0.0, 0.1, 0.0),
                             )
                                    
        # right now I'm getting a bug when calling this to get the image
        # not sure why, it happened after the big Direct update
        #self['image'] = getDefaultDialogGeom()

        # Make a label for showing the score.
        
        self.score = 0
        
        self.scoreText = DirectLabel(self,
                                     relief = None,
                                     text = str(self.score),
                                     text_scale = 0.08,
                                     pos = (0.0, 0.0, -0.09))

        # Make a label for showing the avatar's name.  This goes down
        # here at the end, so the name will be on top of the other
        # stuff.
        self.nameText = DirectLabel(self,
                                    relief = None,
                                    text = TTLocalizer.DivingGameTreasuresRetrieved,
                                    text_scale = 0.05,
                                    text_pos = (0.0, 0.06),
                                    text_wordwrap = 7.5,
                                    text_shadow = (1, 1, 1, 1))
                                    
        

        self.show()

    def cleanup(self):
        del self.scoreText
        del self.nameText
        self.destroy()

    def incrScore(self):
        self.score += 1
        self.scoreText['text'] = str(self.score)

    def makeTransparent(self, alpha):
        self.setTransparency(1)
        self.setColorScale(1,1,1,alpha)
        
