from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import LaffMeter

class MinigameAvatarScorePanel(DirectFrame):
    def __init__(self, avId, avName):

        self.avId = avId

        if base.cr.doId2do.has_key(self.avId):
            self.avatar = base.cr.doId2do[self.avId]
        else:
            # Must be a suit
            self.avatar = None

        # initialize our base class.
        DirectFrame.__init__(self,
                             relief = None,
                             image_color = GlobalDialogColor,
                             image_scale = (0.4, 1.0, 0.24),
                             image_pos = (0.0, 0.1, 0.0),
                             )
                                    
        # For some reason, we need to set this after construction to
        # get it to work properly.
        self['image'] = DGG.getDefaultDialogGeom()

        # Make a label for showing the score.
        self.scoreText = DirectLabel(self,
                                     relief = None,
                                     text = "0",
                                     text_scale = TTLocalizer.MASPscoreText,
                                     pos = (0.1, 0.0, -0.09))

        if self.avatar:
            self.laffMeter = LaffMeter.LaffMeter(self.avatar.style,
                                                 self.avatar.hp,
                                                 self.avatar.maxHp)
            self.laffMeter.reparentTo(self)
            self.laffMeter.setPos(-0.085, 0, -0.035)
            self.laffMeter.setScale(0.05)
            self.laffMeter.start()
        else:
            self.laffMeter = None

        # Make a label for showing the avatar's name.  This goes down
        # here at the end, so the name will be on top of the other
        # stuff.
        self.nameText = DirectLabel(self,
                                    relief = None,
                                    text = avName,
                                    text_scale = TTLocalizer.MASPnameText,
                                    text_pos = (0.0, 0.06),
                                    text_wordwrap = 7.5,
                                    text_shadow = (1, 1, 1, 1))

        self.show()

    def cleanup(self):
        if self.laffMeter:
            self.laffMeter.destroy()
            del self.laffMeter
        del self.scoreText
        del self.nameText
        self.destroy()

    def setScore(self, score):
        self.scoreText['text'] = str(score)

    def getScore(self):
        return int(self.scoreText['text'])

    def makeTransparent(self, alpha):
        self.setTransparency(1)
        self.setColorScale(1,1,1,alpha)
        
