from PlayingCard import PlayingCardNodePath
import PlayingCardGlobals
from pandac.PandaModules import NodePath, Vec3
from direct.interval.IntervalGlobal import LerpHprInterval, Parallel, SoundInterval


class PairingGameCard(PlayingCardNodePath):
    """
    The specifc class used for the pairing game
    """
    DoIntervalDefault = True
    FlipTime = 0.25
    UseDifferentCardColors = True

    # these color values were taken from ToonDNA.py
    CardColors = [ (0.933594, 0.265625, 0.28125, 1.0), # bright red
                   (0.550781, 0.824219, 0.324219, 1.0), # light green
                   (0.347656, 0.820312, 0.953125, 1.0), # light blue
                   (0.460938, 0.378906, 0.824219, 1.0), # purple blue
                   (0.710938, 0.234375, 0.4375, 1.0), # plum
                   (0.285156, 0.328125, 0.726562, 1.0), # blue
                   (0.242188, 0.742188, 0.515625, 1.0), # seafoam
                   (0.96875, 0.691406, 0.699219, 1.0), # light pink
                   (0.996094, 0.957031, 0.597656, 1.0), # light yellow
                   (0.992188, 0.480469, 0.167969, 1.0), # orange
                   ]
                   
    def __init__(self, value):
        """Constructor, value should be [0..51]."""
        style = PlayingCardGlobals.Styles[0]
        PlayingCardNodePath.__init__(self, style,value)
        self.enterCallback = None
        self.exitCallback = None
    
    def load(self):
        """Load the assets."""
        # these are just temp assets
        oneCard = loader.loadModel("phase_4/models/minigames/garden_sign_memory")

        # grab the gag icon
        prop = self.attachNewNode('prop')
        PlayingCardGlobals.getImage(self.style, self.suit, self.rank).copyTo(prop)
        prop.setScale(7)
        
        # remove the bits we don't want
        oneCard.find('**/glow').removeNode()
        #oneCard.find('**/shadow').removeNode()
        # munge the collision to fit just the sign
        cs = oneCard.find('**/collision')
        #cs.setScale(1, 1.0, 0.5)
        #cs.setPos(0,0, 0.9)
        for solidIndex in range(cs.node().getNumSolids()):
            cs.node().modifySolid(solidIndex).setTangible(False)
        cs.node().setName('cardCollision-%d' % self.value)

        # munge the sign to fit the rank
        sign = oneCard.find('**/sign1')
        if self.UseDifferentCardColors:
            index = self.rank % len(self.CardColors)
            color = self.CardColors[index]
            sign.setColorScale(*color)

        # set up the prop that shows which tree it is
        prop.setPos(0.0, 0.0, 0.08)
        prop.setP(-90)
        prop.reparentTo(oneCard)

        oneCard.reparentTo(self)

        #set up the back of the card
        cardBack = oneCard.find('**/sign2')
        cardBack.setColorScale(0.12, 0.35, 0.5, 1.0)
        cardModel = loader.loadModel('phase_3.5/models/gui/playingCard')
        logo = cardModel.find('**/logo')
        logo.reparentTo(self)
        logo.setScale(0.45)        
        logo.setP(90)
        logo.setZ(0.025)
        logo.setX(-0.05)
        logo.setH(180)
 
        cardModel.remove()

        self.setR(0) # the default value is face Up
        self.setScale(2.5)

        self.flipIval = None

        self.turnUpSound = base.loadSfx("phase_4/audio/sfx/MG_pairing_card_flip_face_up.mp3")
        self.turnDownSound = base.loadSfx("phase_4/audio/sfx/MG_pairing_card_flip_face_down.mp3")        

    def unload(self):
        """Unload the assets."""
        self.clearFlipIval()
        self.removeNode()
        del self.turnUpSound
        del self.turnDownSound

    def turnUp(self, doInterval = DoIntervalDefault):
        """Turn up the card.

        doInterval -- if true do a sound and flip up animation
        
        """
        assert self.value != PlayingCardGlobals.Unknown
        self.faceUp = 1
        if doInterval:
            self.clearFlipIval()
            self.flipIval = Parallel(
                LerpHprInterval(self, self.FlipTime, Vec3(0,0,0)),
                SoundInterval(self.turnUpSound, node = self,
                              listenerNode = base.localAvatar,
                              cutOff=240)
                )
            self.flipIval.start()
        else:
            self.setR(0)        

    def clearFlipIval(self):
        """Clear any flip intervals on this card."""
        if self.flipIval:
            self.flipIval.finish()
            self.flipIval = None

    def turnDown(self, doInterval = DoIntervalDefault):
        """Turn up the card.

        doInterval -- if true do a sound and flip up animation
        
        """        
        self.faceUp = 0
        if doInterval:
            self.clearFlipIval()
            self.flipIval = Parallel(
                LerpHprInterval(self, self.FlipTime, Vec3(0,0,180)),
                SoundInterval(self.turnDownSound, node = self,
                              listenerNode = base.localAvatar,
                              cutOff = 240)
                )
            self.flipIval.start()
        else:
            self.setR(180)
