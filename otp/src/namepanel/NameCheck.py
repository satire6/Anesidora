"""NameCheck module: contains avatar name-checking routines"""

import string
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NSError
from pandac.PandaModules import TextEncoder, TextNode

notify = DirectNotifyGlobal.directNotify.newCategory('NameCheck')

def filterString(str, filter):
    """ returns a version of str that only contains characters in filter """
    result = ''
    for char in str:
        if char in filter:
            result = result + char
    return result

def justLetters(str):
    letters = ''
    for c in str:
        if c.isalpha():
            letters = letters + c
    return letters

def justUpper(str):
    upperCaseLetters = ''
    for c in str:
        if c.upper() != c.lower():
            if c == c.upper():
                upperCaseLetters = upperCaseLetters + c
    return upperCaseLetters

def wordList(str):
    """ just like split, but treats dashes as whitespace """
    words = str.split()
    result = []
    for word in words:
        subWords = word.split('-')
        for sw in subWords:
            if sw:
                result.append(sw)
    return result

def checkName(name, otherCheckFuncs=[], font=None):
    # misc check functions;
    # name should not be a wide-character string (for example it should be utf-8)
    # return None if name is OK, error string if name is not OK
    # check functions are given unicode strings
    # if font is passed in, checkName() will make sure all characters in the name
    # are valid characters in the font
    def longEnough(name):
        if len(name) < 2:
            notify.info('name is too short')
            return OTPLocalizer.NCTooShort

    def emptyName(name):
        if name.strip() == '':
            notify.info('name is empty')
            return OTPLocalizer.NCTooShort
        
    def printableChars(name):
        for char in name:
            # If it is an extended character, we cannot test it for printability here (but
            # presumably it is some printable character.)
            if ord(char) < 0x80 and char not in string.printable:
                notify.info('name contains non-printable char #%s' % ord(char))
                return OTPLocalizer.NCGeneric

    validAsciiChars = set(".,'-" + string.letters + string.whitespace)
    def _validCharacter(c, validAsciiChars=validAsciiChars, font=font):
        if c in validAsciiChars:
            return True
        # check for Unicode alphabetic characters and whitespace
        if c.isalpha() or c.isspace():
            return True
        return False
        
    def badCharacters(name, _validCharacter=_validCharacter):
        for char in name:
            if not _validCharacter(char):
                if char in string.digits:
                    notify.info('name contains digits')
                    return OTPLocalizer.NCNoDigits
                else:
                    notify.info('name contains bad char: %s' % TextEncoder().encodeWtext(char))
                    return OTPLocalizer.NCBadCharacter % TextEncoder().encodeWtext(char)

    def fontHasCharacters(name, font=font): 
        if font:
            tn = TextNode('NameCheck')
            tn.setFont(font)
            for c in name:
                if not tn.hasCharacter(ord(c)):
                    notify.info('name contains bad char: %s' % TextEncoder().encodeWtext(c))
                    return OTPLocalizer.NCBadCharacter % TextEncoder().encodeWtext(c)

    def hasLetters(name):
        #,...,
        words = wordList(name)
        for word in words:
            letters = justLetters(word)

            if len(letters) == 0:
                notify.info('word "%s" has no letters' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCNeedLetters

    def hasVowels(name):
        # ndssmvwls
        def perWord(word):
            # if there's a period, assume it's an abbrevation
            if '.' in word:
                return None

            # Check if there's an extended character; if
            # so, it might be a vowel.
            for char in word:
                if ord(char) >= 0x80:
                    return None
                
            letters = filterString(word, string.letters)
            # things like 'MD' are ok without periods
            if len(letters) > 2:
                vowels = filterString(letters, 'aeiouyAEIOUY')
                if len(vowels) == 0:
                    notify.info('word "%s" has no vowels' % TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCNeedVowels

        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def monoLetter(name):
        # eeeeeeeee
        def perWord(word):
            word = word
            letters = justLetters(word)
            if len(letters) > 2:
                # make case-insensitive
                letters = TextEncoder().decodeText(
                    TextEncoder.lower(
                    TextEncoder().encodeWtext(letters)))
                filtered = filterString(letters, letters[0])
                if filtered == letters:
                    notify.info('word "%s" uses only one letter' % TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCGeneric
        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def checkDashes(name):
        def validDash(index, name=name):
            # if the dash is at the beginning or the end, fail
            if (index == 0) or (i == len(name)-1):
                return 0
            # dash must be surrounded by letters on both sides
            if not (name[i-1].isalpha()):
                return 0
            if not (name[i+1].isalpha()):
                return 0
            return 1
        i = 0
        while 1:
            i = name.find('-', i, len(name))
            if i < 0:
                return None
            if not validDash(i):
                notify.info('name makes invalid use of dashes')
                return OTPLocalizer.NCDashUsage
            i += 1
        
    def checkCommas(name):
        def validComma(index, name=name):
            # if the comma is at the beginning or the end, fail
            if (index == 0) or (i == len(name)-1):
                return OTPLocalizer.NCCommaEdge
            # comma must follow a word and be followed by a space
            if (name[i-1].isspace()):
                return OTPLocalizer.NCCommaAfterWord
            if not (name[i+1].isspace()):
                return OTPLocalizer.NCCommaUsage
            return None
        i = 0
        while 1:
            i = name.find(',', i, len(name))
            if i < 0:
                return None
            problem = validComma(i)
            if problem:
                notify.info('name makes invalid use of commas')
                return problem
            i += 1
        
    def checkPeriods(name):
        """ periods are allowed at the end of words, or in two-letter
        words, like 'J.T.' """
        words = wordList(name)
        for word in words:
            # strip off any trailing commas
            if word[-1] == ',':
                word = word[:-1]

            numPeriods = word.count('.')
            if not numPeriods:
                continue

            letters = justLetters(word)
            numLetters = len(letters)

            # word must end in '.'
            if word[-1] != '.':
                notify.info('word "%s" does not end in a period' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCPeriodUsage

            # max periods is 2
            if numPeriods > 2:
                notify.info('word "%s" has too many periods' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCPeriodUsage

            if numPeriods == 2:
                # 2nd and 4th characters should be periods
                if not ((word[1] == '.') and (word[3] == '.')):
                    notify.info('word "%s" does not fit the J.T. pattern' %
                                TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCPeriodUsage

        return None

    def checkApostrophes(name):
        words = wordList(name)
        for word in words:
            numApos = word.count("'")
            if numApos > 2:
                notify.info('word "%s" has too many apostrophes.' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCApostrophes
        numApos = name.count("'")
        if numApos > 3:
            notify.info('name has too many apostrophes.')
            return OTPLocalizer.NCApostrophes
        
    def tooManyWords(name):
        if len(wordList(name)) > 4:
            notify.info('name has too many words')
            return OTPLocalizer.NCTooManyWords
        
    def allCaps(name):
        # MICKEY MOUSE
        letters = justLetters(name)
        # J.T. -> OK
        if len(letters) > 2:
            upperLetters = TextEncoder().decodeText(
                TextEncoder.upper(
                TextEncoder().encodeWtext(letters)))
            # some unicode characters can't be capitalized
            for i in xrange(len(upperLetters)):
                if not upperLetters[0].isupper():
                    # at least one letter is not upper-case
                    # name is not all-caps
                    # excessive capitalization will be caught by mixedCase()
                    return
            if upperLetters == letters:
                notify.info('name is all caps')
                return OTPLocalizer.NCAllCaps

    def mixedCase(name):
        # MiCkeY MoUsE
        words = wordList(name)
        for word in words:
            if len(word) > 2:
                # allow McQuack
                capitals = justUpper(word)
                if len(capitals) > 2:
                    notify.info('name has mixed case')
                    return OTPLocalizer.NCMixedCase

    def checkJapanese(name):
        # Japan allows ASCII space, hiragana, katakana, and half-width katakana,
        # but, allows not ASCII and kanji(CJK) characters for a name
        # All Japanese characters are three-byte-encoded utf-8 characters from unicode
        # Reference: http://unicode.org/charts/
        asciiSpace = range(0x20, 0x21)
        asciiDigits = range(0x30, 0x40)
        hiragana = range(0x3041, 0x30A0)
        katakana = range(0x30A1, 0x3100)
        halfwidthKatakana = range(0xFF65, 0xFFA0)
        halfwidthCharacter = set(asciiSpace + halfwidthKatakana)
        allowedUtf8 = set(asciiSpace + hiragana + katakana + halfwidthKatakana)
        te = TextEncoder()
        dc = 0.0

        # Return None if name is OK, error string if name is not OK
        for char in (ord(char) for char in te.decodeText(name)):
            if char not in allowedUtf8:
                # Notify error string, if not allowed utf-8 character
                if char in asciiDigits:
                    notify.info('name contains not allowed ascii digits')
                    return OTPLocalizer.NCNoDigits
                else:
                    notify.info('name contains not allowed utf8 char: 0x%04x' % char)
                    return OTPLocalizer.NCBadCharacter % te.encodeWtext(unichr(char))
            else:
                # Restrict the number of characters, if three-byte-encoded utf-8 character
                # The full-width characters would fit into a single display cell, 
                # and the half-width characters would fit two to a display cell
                if char in halfwidthCharacter:
                    dc += 0.5
                else:
                    dc += 1

        # Japan restricts the number of the characters, if occupied less then two display cell
        # and more then eight display cell.
        if (dc < 2):
            notify.info('name is too short: %0.1f' % dc)
            return OTPLocalizer.NCTooShort
        elif (dc > 8):
            notify.info('name has been occupied more than eight display cells: %0.1f' % dc)
            return OTPLocalizer.NCGeneric

    def repeatedChars(name):
        count = 1
        lastChar = None
        i = 0
        while i < len(name):
            char = name[i]
            i += 1
            
            if char == lastChar:
                # character is repeating
                count += 1
            else:
                count = 1

            lastChar = char

            if count > 2:
                notify.info('character %s is repeated too many times' % TextEncoder().encodeWtext(char))
                return OTPLocalizer.NCRepeatedChar % TextEncoder().encodeWtext(char)

    checks = [
        printableChars,
        badCharacters,
        fontHasCharacters,
        longEnough,
        emptyName,
        hasLetters,
        hasVowels,
        monoLetter,
        checkDashes,
        checkCommas,
        checkPeriods,
        checkApostrophes,
        tooManyWords,
        allCaps,
        mixedCase,
        repeatedChars,
        ] + otherCheckFuncs

    # checks that should be run on the reversed name string
    symmetricChecks = [
        ]

    # make sure we are working with a wide-character version of the string
    name = TextEncoder().decodeText(name)
    notify.info('checking name "%s"...' % TextEncoder().encodeWtext(name))

    # run through all the checks
    for check in checks:
        problem = check(name[:])
        if (not problem) and (check in symmetricChecks):
            # check it backwards.
            nName = name[:]
            bName.reverse()
            problem = check(bName)
            print "problem = %s" % (problem)

        if problem:
            return problem

    return None

# prevent log spam during testing
severity = notify.getSeverity()
notify.setSeverity(NSError)

# these tests can be removed or replaced for international versions of the codebase

# long enough
assert     checkName('J')
assert not checkName('Jo')
# empty name
assert     checkName('')
assert     checkName('\t')
assert     checkName(TextEncoder().encodeWtext(u'\xa0'))
assert     checkName(TextEncoder().encodeWtext(u'\u1680'))
assert     checkName(TextEncoder().encodeWtext(u'\u2001'))
# printable chars
for i in xrange(32):
    assert checkName(chr(i))
assert     checkName(chr(0x7f))
# bad characters
for c in '!"#$%&()*+/:;<=>?@[\]^_`{|}~':
    assert checkName('Bob' + c)
# has letters
assert     checkName(',...,')
#   katakana = range(0x30A1, 0x30FB)
#assert not checkName(TextEncoder().encodeWtext(u'\u30a1\u30a2'))
# has vowels
assert     checkName('Qwrt')
assert not checkName('MD')
# mono letter
assert     checkName('Eeee')
assert     checkName('Jjj')
assert     checkName(TextEncoder().encodeWtext(u'\u30a1\u30a1\u30a1'))
# dashes
assert     checkName('-Conqueror')
assert     checkName('Conqueror-')
assert     checkName('--Bobby--')
assert     checkName('Mary- Jo')
assert not checkName('Mary-Jo')
# commas
assert     checkName(',Conqueror')
assert     checkName('Conqueror,')
assert     checkName('Bob , MD')
assert not checkName('Bob, MD')
assert     checkName('Bob,MD')
# periods
assert     checkName('.Conqueror')
assert not checkName('Conqueror.')
assert not checkName('J.T.')
assert     checkName('J.T .')
# apostrophes
assert not checkName("Bobby's Brother")
#   more than two per word
assert not checkName("O'Shannon's Brother")
assert     checkName("O'Shann'on's Brother")
#   more than three total
assert not checkName("Bobby's Bud's Brother's")
assert     checkName("O'Shannon's Bud's Brother's")
# number of words
assert not checkName('One')
assert not checkName('Two Words')
assert not checkName('Three Great Words')
assert not checkName('Four Words Are Super')
assert     checkName('Five Words Are Too Many')
#assert not checkName(TextEncoder().encodeWtext(u'\u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2'))
#assert not checkName(TextEncoder().encodeWtext(u'\u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2'))
#assert     checkName(TextEncoder().encodeWtext(u'\u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2 \u30a1\u30a2'))
# all caps
assert     checkName('MCQUACK')
assert     checkName('DUCK MQQUACK')
# mixed case
assert not checkName('McQuack')
assert     checkName('McQuacK')
assert     checkName('Duck McQuacK')
# repeated character
assert not checkName('Woody')
assert     checkName('Wooody')

notify.setSeverity(severity)
del severity
