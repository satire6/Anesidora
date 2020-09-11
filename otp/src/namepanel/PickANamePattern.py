class PickANamePattern:
    """Given a name string, converts it to a pick-a-name if possible"""
    def __init__(self, nameStr, gender):
        self._nameStr = nameStr
        self._namePattern = self._compute(self._nameStr, gender)

    def hasNamePattern(self):
        return self._namePattern is not None

    def getNamePattern(self):
        return self._namePattern

    def getNameString(self, pattern, gender):
        nameParts = self._getNameParts(gender)
        # convert from string->index to index->string
        invNameParts = []
        for i in xrange(len(nameParts)):
            invNameParts.append(invertDict(nameParts[i]))
        name = ''
        for i in xrange(len(pattern)):
            if pattern[i] != -1:
                if len(name):
                    name += ' '
                name += invNameParts[i][pattern[i]]
        return name

    def getNamePartString(self, gender, patternIndex, partIndex):
        nameParts = self._getNameParts(gender)
        # convert from string->index to index->string
        invNamePart = invertDict(nameParts[patternIndex])
        return invNamePart[partIndex]

    def _genWordListSplitPermutations(self, words):
        # recursively generate each possible permutation of words in the word list
        # joined with a space
        if not len(words):
            # list doesn't contain any words, yield nothing
            return
        if len(words) == 1:
            # list contains only one word, yield only one permutation
            yield words
            return
        for permutation in self._genWordListSplitPermutations(words[1:]):
            # yield a version with the current word as a separate word
            yield [words[0]] + permutation
            # yield a version with the current word joined with the following word
            yield [words[0] + ' ' + permutation[0]] + permutation[1:]

    def _genNameSplitPermutations(self, name):
        """yields each possible permutation of combinations of word splits for the provided
        name string, using a single space to combine split strings, since that is what separates
        multi-word name parts.
        Allows us to match a name part like 'Boo Boo' which has a space in it
        """
        for splitName in self._genWordListSplitPermutations(name.split()):
            yield splitName

    def _compute(self, nameStr, gender):
        """this does the work of calculating a pick-a-name pattern from
        a name string, if possible"""
        # get the appropriate name parts for the specified gender
        return self._computeWithNameParts(nameStr, self._getNameParts(gender))

    def _computeWithNameParts(self, nameStr, nameParts):
        # run through each permutation of consecutive words joined with a space
        # to catch name parts like "Boo Boo"
        for splitPermutation in self._genNameSplitPermutations(nameStr):
            pattern = self._recursiveCompute(splitPermutation, nameParts)
            if pattern is not None:
                return pattern
        return None

    def _getNameParts(self, gender):
        # override and return list of name word dicts
        # each name word dict should be word->index
        # for instance [{'Captain': 0}, {'Bigbeard': 0, 'Longbeard': 1}]
        pass

    def _recursiveCompute(self, words, nameParts, wi=0, nwli=0, pattern=None):
        if wi >= len(words):
            # matches have been found for every word in the name
            return pattern
        if nwli >= len(nameParts):
            # matches have not been found for every word in the name, and we've run out
            # of name parts
            return None
        
        if words[wi] in nameParts[nwli]:
            # we got a match between the current word and the current list of name parts
            if pattern is None:
                pattern = [-1] * len(nameParts)
            word2index = nameParts[nwli]
            newPattern = pattern[:]
            newPattern[nwli] = word2index[words[wi]]
            # try to find a complete match for the name using this partial match
            result = self._recursiveCompute(words, nameParts, wi+1, nwli+1, newPattern)
            if result:
                return result

        # can't use a match with this name part, try the next one
        return self._recursiveCompute(words, nameParts, wi,   nwli+1, pattern)
        
class PickANamePatternTwoPartLastName(PickANamePattern):
    def getNameString(self, pattern, gender):
        name = PickANamePattern.getNameString(self, pattern, gender)
        if pattern[-2] != -1:
            # remove the space between the two parts of the last name
            words = name.split()
            name = ''
            for word in words[:-2]:
                if len(name):
                    name += ' '
                name += word
            if len(name):
                name += ' '
            name += words[-2]
            # capitalize the last name suffix if appropriate (Mc, Mac, etc.)
            if words[-2] in set(self._getLastNameCapPrefixes()):
                name += words[-1].capitalize()
            else:
                name += words[-1]
        return name

    def _getLastNameCapPrefixes(self):
        # returns list of last name prefixes that capitalize their suffix
        return []
    
    def _compute(self, nameStr, gender):
        nameParts = self._getNameParts(gender)
        combinedNameParts = nameParts[:-2]
        
        # temporarily combine the two name parts of the last names into one unified name part
        combinedNameParts.append({})
        combinedIndex2indices = {}
        lastNamePrefixesCapped = set(self._getLastNameCapPrefixes())
        k = 0
        for first, i in nameParts[-2].iteritems():
            capitalize = first in lastNamePrefixesCapped
            for second, j in nameParts[-1].iteritems():
                combinedLastName = first
                # capitalize the last name suffix if appropriate (Mc, Mac, etc.)
                if capitalize:
                    combinedLastName += second.capitalize()
                else:
                    combinedLastName += second
                combinedNameParts[-1][combinedLastName] = k
                # store the original indices so we can assign them if this last name
                # combination is chosen
                combinedIndex2indices[k] = (i, j)
                k += 1
                
        pattern = self._computeWithNameParts(nameStr, combinedNameParts)
        
        if pattern:
            combinedIndex = pattern[-1]
            pattern = pattern[:-1]
            pattern.append(-1)
            pattern.append(-1)
            if combinedIndex != -1:
                # split out the last name into the original two indices
                pattern[-2] = combinedIndex2indices[combinedIndex][0]
                pattern[-1] = combinedIndex2indices[combinedIndex][1]

        return pattern

if __debug__:
    class TestClass(PickANamePattern):
        def _getNameParts(self, gender):
            return [{'Test': 0, 'Some': 1,}, {'Name': 0, 'Thing': 1,}]

    assert not TestClass('', None).hasNamePattern()
    assert TestClass('Test', None).getNamePattern() == [0, -1]
    assert TestClass('Some', None).getNamePattern() == [1, -1]
    assert TestClass('Thing', None).getNamePattern() == [-1, 1]
    assert TestClass('Test Name', None).getNamePattern() == [0, 0]
    assert TestClass('Some Thing', None).getNamePattern() == [1, 1]

    assert TestClass('', None).getNameString(TestClass('Some Thing', None).getNamePattern(), None) == 'Some Thing'

    del TestClass

    class TestClass2(PickANamePatternTwoPartLastName):
        def _getNameParts(self, gender):
            return [{'Test': 0, 'Some': 1,}, {'Name': 0, 'Thing': 1,},
                    {'Fluffy': 0, 'Poofy': 1, 'Mc': 2,}, {'pants': 0, 'kins': 1,},]
        def _getLastNameCapPrefixes(self):
            return ['Mc',]

    assert not TestClass2('', None).hasNamePattern()
    assert not TestClass2('bleh', None).hasNamePattern()
    assert TestClass2('Test', None).hasNamePattern()
    assert TestClass2('McPants', None).hasNamePattern()

    assert TestClass2('Test', None).getNamePattern() == [0, -1, -1, -1]
    assert TestClass2('Test Thing', None).getNamePattern() == [0, 1, -1, -1]
    assert TestClass2('Test Name Fluffypants', None).getNamePattern() == [0, 0, 0, 0]
    assert TestClass2('Some Poofykins', None).getNamePattern() == [1, -1, 1, 1]
    assert TestClass2('McPants', None).getNamePattern() == [-1, -1, 2, 0]

    assert not TestClass2('Test Name QWERkins', None).hasNamePattern()
    assert not TestClass2('Test Name PoofyQWER', None).hasNamePattern()
    assert TestClass2('Test Name Poofykins', None).hasNamePattern()

    assert TestClass2('', None).getNameString(TestClass2('Test Name Fluffypants', None).getNamePattern(), 'None') == 'Test Name Fluffypants'
    assert TestClass2('', None).getNameString(TestClass2('McPants', None).getNamePattern(), 'None') == 'McPants'

    del TestClass2
