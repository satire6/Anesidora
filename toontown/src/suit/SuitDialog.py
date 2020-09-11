import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer

# Centralize everything a suit can say
# import this file
# Then call SuitDialog.requestBattle.get() to get the next dialog in the list

notify = DirectNotifyGlobal.directNotify.newCategory('SuitDialog')

def getBrushOffIndex(suitName):
    """ getBrushOffIndex(suitName)

    Chooses a suitable brushoff for a suit of the given type, and
    returns its index number (which can later be passed to
    getBrushOffText() to retrieve the message itself).
    
    """
    if SuitBrushOffs.has_key(suitName):
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]

    # Why do we go through all this work to choose a random brushoff
    # when we could just choose one directly via random.randint()?
    num = len(brushoffs)
    chunk = 100 / num
    randNum = random.randint(0, 99)
    count = chunk
    for i in range(num):
        if (randNum < count):
            return i
        count += chunk
    notify.error('getBrushOffs() - no brush off found!')

def getBrushOffText(suitName, index):
    """ getBrushOffText(suitName, index)

    Returns the text of the brushoff with the given index number for
    the given suit type.
    
    """
    if SuitBrushOffs.has_key(suitName):
        brushoffs = SuitBrushOffs[suitName]
    else:
        brushoffs = SuitBrushOffs[None]

    return brushoffs[index]

SuitBrushOffs = OTPLocalizer.SuitBrushOffs
