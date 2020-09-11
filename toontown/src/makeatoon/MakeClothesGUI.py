import ClothesGUI
from toontown.toon import ToonDNA

class MakeClothesGUI(ClothesGUI.ClothesGUI):
    notify = directNotify.newCategory("MakeClothesGUI")

    def __init__(self, doneEvent):
        ClothesGUI.ClothesGUI.__init__(self, ClothesGUI.CLOTHES_MAKETOON,
                                       doneEvent)
        
    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        gender = self.dna.getGender()

        # Handle the case where we're in MakeAToon, either for the first time
        # or backing up far enough to change gender (the first time through,
        # this thinks we are changing gender because gender is initialized
        # to be = '?'
        if (gender != self.gender):
            self.tops = ToonDNA.getRandomizedTops(gender, 
                                                    tailorId = ToonDNA.MAKE_A_TOON)
            self.bottoms = ToonDNA.getRandomizedBottoms(gender, 
                                                          tailorId = ToonDNA.MAKE_A_TOON)
            self.gender = gender
            # Don't try and preserve choices made as a different gender
            self.topChoice = 0
            self.bottomChoice = 0

        # setup the buttons
        self.setupButtons()

    def setupButtons(self):
        ClothesGUI.ClothesGUI.setupButtons(self)

        # cover thy nakedness
        # This only happens in MakeAToon
        if (len(self.dna.torso) == 1):
            if (self.gender == 'm'):
                torsoStyle = 's'
            else:
                if (self.girlInShorts == 1):
                    torsoStyle = 's'
                else:
                    torsoStyle = 'd'
            self.toon.swapToonTorso(self.dna.torso[0] + torsoStyle)
            self.toon.loop("neutral", 0)
            self.toon.swapToonColor(self.dna)            
            # set texture to start of clothes choices
            self.swapTop(0)
            self.swapBottom(0)
        return None
         
