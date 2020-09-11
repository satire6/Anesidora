from direct.showbase.PythonUtil import listToItem2index
from otp.namepanel.PickANamePattern import PickANamePatternTwoPartLastName
from toontown.makeatoon.NameGenerator import NameGenerator
import types

class TTPickANamePattern(PickANamePatternTwoPartLastName):
    NameParts = None
    LastNamePrefixesCapped = None

    def _getNameParts(self, gender):
        if TTPickANamePattern.NameParts is None:
            TTPickANamePattern.NameParts = {}
            ng = NameGenerator()
            TTPickANamePattern.NameParts['m'] = ng.getMaleNameParts()
            TTPickANamePattern.NameParts['f'] = ng.getFemaleNameParts()

        # make sure the dicts haven't been inverted
        assert type(TTPickANamePattern.NameParts[gender][0].keys()[0]) is types.StringType

        return TTPickANamePattern.NameParts[gender]

    def _getLastNameCapPrefixes(self):
        if TTPickANamePattern.LastNamePrefixesCapped is None:
            ng = NameGenerator()
            TTPickANamePattern.LastNamePrefixesCapped = ng.getLastNamePrefixesCapped()[:]

        return TTPickANamePattern.LastNamePrefixesCapped

if __debug__:
    assert TTPickANamePattern('Alvin', 'm').hasNamePattern()
    assert TTPickANamePattern('Fireball', 'm').hasNamePattern()
    assert TTPickANamePattern('King Alvin Sourflap', 'm').hasNamePattern()
    assert not TTPickANamePattern('King Alvin ASDFflap', 'm').hasNamePattern()
    assert not TTPickANamePattern('test name', 'm').hasNamePattern()
    
    assert TTPickANamePattern('', 'm').getNameString(TTPickANamePattern('King Alvin Sourflap', 'm').getNamePattern(), 'm') == 'King Alvin Sourflap'
    assert TTPickANamePattern('', 'm').getNameString(TTPickANamePattern('Knuckles McFlipper', 'm').getNamePattern(), 'm') == 'Knuckles McFlipper'
