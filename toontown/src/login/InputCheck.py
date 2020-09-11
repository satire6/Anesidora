"""InputCheck module: contains the InputCheck class"""

from pandac.PandaModules import *
import string

def isValidEmailAddr(addr):
    strict = config.GetBool('strict-email-check', 1)
    if not strict:
        return len(addr) > 0
        
    sections = addr.split('@')
    # there must be exactly one '@'
    if len(sections) != 2:
        return 0
    name, host = sections
    # there must be something before the '@'
    if len(name) == 0:
        return 0

    sections = host.split('.')
    # there must be at least one '.' after the '@'
    if len(sections) < 2:
        return 0
    # make sure there's something after the last '.'
    if len(sections[-1]) == 0:
        return 0
    
    return 1

# this is used as a callback in a list of input check functors
def emailAddrMatch(addr1, addr2):
    return addr1 == addr2

# for credit card numbers, etc.
def stripWhitespace(str):
    return str.replace(' ', '')

def isBlank(text):
    return stripWhitespace(text) == ''

def stripCreditCardNumber(str):
    """ removes spaces, dashes, etc. from a credit card number """
    legalChars = (' ', '-',)
    for char in legalChars:
        str = str.replace(char, '')
    return str

def isNumeric(str):
    return str.isdigit()

def isCorrectCreditCardLength(num, ccType='any'):
    # check the length of the number
    if ccType == 'American Express':
        if len(num) != 15: return 0
    elif ccType == 'Visa':
        if len(num) != 16: return 0
    elif ccType == 'MasterCard':
        if len(num) != 16: return 0
    elif ccType == 'any':
        if len(num) not in (15, 16,): return 0
    else:
        assert('unknown credit card type')
    return 1

def creditCardNumberMatchesType(num, ccType='any'):
    # check the first digit of the number
    if ccType == 'American Express':
        if num[0] != '3': return 0
    elif ccType == 'Visa':
        if num[0] != '4': return 0
    elif ccType == 'MasterCard':
        if num[0] != '5': return 0
    elif ccType == 'any':
        if num[0] not in ('3','4','5'): return 0
    else:
        assert('unknown credit card type')
    return 1

def isValidCreditCardNum(num, ccType='any'):
    # if there any chars that are not digits, fail
    if not isNumeric(num): return 0

    # check the length of the number and the first digit
    # against the credit card type
    if not isCorrectCreditCardLength(num, ccType): return 0
    if not creditCardNumberMatchesType(num, ccType): return 0

    return 1

def isValidCreditCardExpDate(month, year,
                             curMonth=None, curYear=None):
    if curYear == None:
        curYear = base.cr.dateObject.getYear()
    if curMonth == None:
        curMonth = base.cr.dateObject.getMonth()

    year = int(year)
    month = int(month)

    if year < curYear:
        # 'this card expires in 1993...'
        return 0
    if year > curYear:
        # if year is greater than current, we're good
        return 1
    if month < curMonth:
        # 'this card expired last month...'
        return 0
    # card expires this month or later
    return 1
