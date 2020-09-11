from direct.directnotify.DirectNotifyGlobal import directNotify
import math
import string

class TTCodeDict:
    notify = directNotify.newCategory('TTCodeDict')

    # characters used for auto-generated codes
    Characters = 'CDFGHJKLMNPQRVWX3469'
    NumChars = len(Characters)

    # characters used for manually-created codes
    IgnoredManualCharacters = '-' + ' '
    ManualCharacters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + string.digits + IgnoredManualCharacters
    # all manually-created codes must contain at least one of these characters
    # ensures that code can never collide with an auto-generated code
    ManualOnlyCharacters = ''

    for char in ManualCharacters:
        if char not in IgnoredManualCharacters:
            if char not in Characters:
                ManualOnlyCharacters += char

    CharactersSet = set(Characters)
    ManualCharactersSet = set(ManualCharacters)

    _Primes = {}
    _PrimeModuli = {}

    # prevent brute-force attacks by using one in N codes
    BruteForceFactor = 1000

    @classmethod
    def isLegalUniqueCode(cls, code):
        chars = set(cls.getFromReadableCode(code))
        return len(chars.difference(cls.CharactersSet)) == 0

    @classmethod
    def isLegalNonUniqueCode(cls, code):
        for c in code:
            if not cls.isValidManualChar(c):
                return False
        return True

    @classmethod
    def isLegalCode(cls, code):
        return cls.isLegalUniqueCode(code) or cls.isLegalNonUniqueCode(code)

    @classmethod
    def isValidManualChar(cls, c):
        if c in cls.IgnoredManualCharacters:
            return True
        return c.isalnum()

    @classmethod
    def isManualOnlyChar(cls, c):
        if c.upper() in cls.CharactersSet:
            return False
        # any unicode alphanumeric character that is not in the auto-generated character set
        # is a manual-only character
        return c.isalnum()

    @staticmethod
    def _isPrime(value):
        maxTestVal = int(math.ceil(math.sqrt(value)))
        if (maxTestVal % 2) == 0:
            maxTestVal -= 1
        testVal = 3
        while testVal <= maxTestVal:
            if (value % testVal) == 0:
                return False
            testVal += 2
        return True

    @staticmethod
    def _nextPrime(value):
        if (value % 2) == 0:
            value += 1
        while not TTCodeDict._isPrime(value):
            value += 2
        return value

    @classmethod
    def getNumValuesInCodeSpace(cls, codeLength):
        return pow(cls.NumChars, codeLength)

    @classmethod
    def getNumUsableValuesInCodeSpace(cls, codeLength):
        return int(cls.getNumValuesInCodeSpace(codeLength) / cls.BruteForceFactor)

    @classmethod
    def _getPrimeModulus(cls, codeLength):
        # get the largest prime in this code value space to use as the code value modulus
        if codeLength in cls._PrimeModuli:
            return cls._PrimeModuli[codeLength]
        print ('calculating prime modulus for code length %s...' % codeLength),
        i = cls.getNumValuesInCodeSpace(codeLength)
        while not cls._isPrime(i):
            i -= 1
            if i < 0:
                raise 'could not find prime modulus for code length %s' % codeLength
        cls._PrimeModuli[codeLength] = i
        print 'done.'
        return i

    @classmethod
    def _getPrime(cls, codeLength):
        if (codeLength in cls._Primes):
            return cls._Primes[codeLength]
        print ('calculating prime multiplier for code length %s...' % codeLength),
        numValues = cls.getNumValuesInCodeSpace(codeLength)
        if '_scatterPrime' not in cls.__dict__:
            # longer codes will require a larger (longer/more digits/more 7's!) prime here
            cls._scatterPrime = 677770777
            cls._scatterPow10 = 1
            scratch = cls._scatterPrime
            while scratch:
                cls._scatterPow10 *= 10
                scratch = int(scratch / 10)
            cls._scatterFactor = float(cls._scatterPrime) / cls._scatterPow10
        subdivisions = cls.NumChars * cls._scatterPow10
        primeFactor = cls._scatterFactor
        multiplier = (subdivisions * primeFactor)
        prime = cls._nextPrime(int((float(numValues) * multiplier) / subdivisions))
        if prime >= numValues:
            prime = cls._nextPrime(int(float(numValues) / subdivisions))
        if prime >= numValues:
            prime = cls._nextPrime(0)
        if prime >= numValues:
            raise 'could not find prime smaller than %s' % numValues
        cls._Primes[codeLength] = prime
        #print 'codeLength %s, prime=%s' % (codeLength, prime)
        print 'done.'
        return prime

    @classmethod
    def getObfuscatedCodeValue(cls, codeValue, codeLength):
        prime = cls._getPrime(codeLength)
        modulus = cls._getPrimeModulus(codeLength)
        obfValue = (prime * codeValue) % modulus
        return obfValue

    @classmethod
    def getCodeFromValue(cls, codeValue, codeLength):
        codeStr = ''
        charsLeft = codeLength
        while charsLeft > 0:
            index = codeValue % cls.NumChars
            codeValue = int(codeValue / cls.NumChars)
            codeStr = cls.Characters[index] + codeStr
            charsLeft -= 1
        return codeStr

    @classmethod
    def getReadableCode(cls, code):
        """
        01 X
        02 XX
        03 XXX
        04 XXXX
        05 XX-XXX
        06 XXX-XXX
        07 XXX-XXXX
        08 XXXX-XXXX
        09 XXX-XXX-XXX
        10 XXX-XXX-XXXX # 6 + 4
        11 XXX-XXXX-XXXX # 7 + 4
        12 XXXX-XXXX-XXXX # 8 + 4
        13 XXX-XXX-XXX-XXXX # 9 + 4
        14 XXX-XXX-XXXX-XXXX # 6 + 8
        15 XXX-XXXX-XXXX-XXXX # 7 + 8
        16 XXXX-XXXX-XXXX-XXXX # 8 + 8
        17 XXX-XXX-XXX-XXXX-XXXX # 9 + 8
        18 XXX-XXX-XXXX-XXXX-XXXX # 6 + 12
        19 XXX-XXXX-XXXX-XXXX-XXXX # 7 + 12
        20 XXXX-XXXX-XXXX-XXXX-XXXX # 8 + 12
        21 XXX-XXX-XXX-XXXX-XXXX-XXXX # 9 + 12
        22 XXX-XXX-XXXX-XXXX-XXXX-XXXX # 6 + 16
        """
        length = len(code)
        if length < 5:
            return code
        if length == 5:
            return '%s-%s' % (code[:2], code[2:])
        if length == 6:
            return '%s-%s' % (code[:3], code[3:])
        if length == 7:
            return '%s-%s' % (code[:3], code[3:])
        if length == 8:
            return '%s-%s' % (code[:4], code[4:])
        if length == 9:
            return '%s-%s-%s' % (code[:3], code[3:6], code[6:])
        numQuads = (len(code) - 6) / 4
        prefixLen = len(code) - (numQuads * 4)
        prefix = cls.getReadableCode(code[:prefixLen])
        toQuad = code[prefixLen:]
        rc = prefix
        while len(toQuad):
            rc = '%s-%s' % (rc, toQuad[:4])
            toQuad = toQuad[4:]
        return rc

    @classmethod
    def getFromReadableCode(cls, code):
        cls.notify.debug('getFromReadableCode: input: %s' % code)
        # remove dashes
        code = ''.join(code.split('-'))
        # remove spaces
        code = ''.join(code.split(' '))
        # uppercase only
        code = code.upper()
        cls.notify.debug('getFromReadableCode: output: %s' % code)
        return code
    
    @classmethod
    def _testCodeUniqueness(cls, codeLength=None, verbose=True):
        if not codeLength:
            codeLength = 4
        while 1:
            print 'testing code uniqueness for code length: %s' % codeLength
            codes = set()
            maxVal = cls._getPrimeModulus(codeLength)
            #print maxVal
            i = 0
            while i < maxVal:
                x = cls.getObfuscatedCodeValue(i, codeLength)
                code = cls.getCodeFromValue(x, codeLength)
                if verbose:
                    print '%s %s/%s -> %s' % (cls.getReadableCode(code), i, maxVal-1, x)
                if code in codes:
                    raise 'code %s already encountered!' % code
                codes.add(code)
                i += 1
            codeLength += 1
            
