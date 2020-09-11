import TownLoader
import TTTownLoader
import TutorialStreet
from toontown.suit import Suit
from toontown.toon import Toon
from toontown.hood import ZoneUtil

class TutorialTownLoader(TTTownLoader.TTTownLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        TTTownLoader.TTTownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = TutorialStreet.TutorialStreet

    # Override of of TTTownLoader, since the dna file is different.
    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadTutorialSuit()
        dnaFile = ("phase_3.5/dna/tutorial_street.dna")
        self.createHood(dnaFile, loadStorage=0)
        self.alterDictionaries()

    def loadBattleAnims(self):
        Toon.loadTutorialBattleAnims()

    def unloadBattleAnims(self):
        Toon.unloadTutorialBattleAnims()

    def alterDictionaries(self):
        # HACK: 20001 is a special zone number reserved explicitly for
        # the tutorial street. We need to change it to the real zone
        # number that has been assigned by the AI. I know this is strange,
        # but I don't know how else to go about this.
        # We need to use the external street zone, which we hackfully
        # extract from ZoneUtil.
        zoneId = ZoneUtil.tutorialDict["exteriors"][0]
        self.nodeDict[zoneId] = self.nodeDict[20001]
        del self.nodeDict[20001]

        
