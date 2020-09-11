"""
        ZoneUtil
        
        Get various information from a zone ID.
"""

from toontown.toonbase.ToontownGlobals import *
from direct.directnotify import DirectNotifyGlobal

zoneUtilNotify = DirectNotifyGlobal.directNotify.newCategory("ZoneUtil")

tutorialDict = None

def isGoofySpeedwayZone(zoneId):
    return (zoneId == 8000)

def isCogHQZone(zoneId):
    return ((zoneId >= 10000) and (zoneId < 15000))

def isMintInteriorZone(zoneId):
    return zoneId in (CashbotMintIntA, CashbotMintIntB, CashbotMintIntC)

def isDynamicZone(zoneId):
    return ((zoneId >= DynamicZonesBegin) and (zoneId < DynamicZonesEnd))

def getStreetName(branchId):
    global tutorialDict
    if tutorialDict:
        return StreetNames[20000][-1]
    else:
        return StreetNames[branchId][-1]

def getLoaderName(zoneId):
    # examples:
    # zoneId ==> returns
    # 1 ==> townLoader
    # 2000 ==> safeZoneLoader
    # 2100 ==> townLoader
    # 2135 ==> townLoader
    # 2501 ==> safeZoneLoader
    # 40000 => safeZoneLoader
    # 40135 => townLoader
    global tutorialDict
    if tutorialDict:
        # If the override is on, we are in the tutorial, and therefore
        # the townloader is the only one we care about, unless we are going
        # through the tunnel to ToontownCentral.
        if zoneId == ToontownCentral:
            loaderName = "safeZoneLoader"
        else:
            loaderName = "townLoader"
    else:
        suffix = zoneId%1000

        # We always assume toon interiors, never suit interiors, with
        # getLoaderName().  And toon interiors are loaded with the safe
        # zone or toon they correspond to.
        if suffix >= 500:
            suffix -= 500
        
        if isCogHQZone(zoneId):
            loaderName="cogHQLoader"
        elif suffix < 100:
            loaderName="safeZoneLoader"
        else:
            loaderName="townLoader"
            
    assert(zoneUtilNotify.debug("getLoaderName(zoneId="
            +str(zoneId)+") returning "+loaderName))
    assert(loaderName)
    return loaderName

def getBranchLoaderName(zoneId):
    """Convert to a branch zone ID before getting loader name."""
    # i.e. don't get any interiors, minigames, or the like.
    # examples:
    # zoneId ==> returns
    # 1 ==> townLoader
    # 2000 ==> safeZoneLoader
    # 2100 ==> townLoader
    # 2135 ==> townLoader
    # 2501 ==> safeZoneLoader
    # 40000 => safeZoneLoader
    # 40135 => townLoader
    return getLoaderName(getBranchZone(zoneId))

def getSuitWhereName(zoneId):
    where=getWhereName(zoneId, 0)
    assert(zoneUtilNotify.debug("getWhereName(zoneId="
            +str(zoneId)+") returning "+where))
    assert(where)
    return where

def getToonWhereName(zoneId):
    where=getWhereName(zoneId, 1)
    assert(zoneUtilNotify.debug("getWhereName(zoneId="
            +str(zoneId)+") returning "+where))
    assert(where)
    return where

def isPlayground(zoneId):
    whereName = getWhereName(zoneId, False)
    if whereName == "cogHQExterior":
        return True        
    else:
        return (zoneId%1000 == 0 and zoneId < DynamicZonesBegin)

def isPetshop(zoneId):
    if (zoneId == 2522 or
        zoneId == 1510 or
        zoneId == 3511 or
        zoneId == 4508 or
        zoneId == 5505 or
        zoneId == 9508):
        return True
    return False

def getWhereName(zoneId, isToon):
    global tutorialDict
    if tutorialDict:
        # If the override is in effect, look in the dictionary.
        if zoneId in tutorialDict["interiors"]:
            where = "toonInterior"
        elif zoneId in tutorialDict["exteriors"]:
            where = "street"
        # This clause is for walking through the tunnel.
        elif zoneId == ToontownCentral or zoneId == WelcomeValleyToken:
            where = "playground"
        else:
            zoneUtilNotify.error("No known zone: " + str(zoneId))
    else:
        suffix = zoneId % 1000
        # Strip off the tens and ones - those zones are considered part of the larger zone
        suffix = (suffix - (suffix % 100))

        if isCogHQZone(zoneId):
            if suffix == 0:
                where = "cogHQExterior"
            elif suffix == 100:
                where = "cogHQLobby"
            elif suffix == 200:
                where = "factoryExterior"
            elif getHoodId(zoneId) == LawbotHQ and suffix in (300,400,500,600):
                where = "stageInterior"
            elif getHoodId(zoneId) == BossbotHQ and suffix in (500,600,700):
                where = "countryClubInterior"
            elif suffix >= 500:
                if getHoodId(zoneId) == SellbotHQ:
                    where = "factoryInterior"
                elif getHoodId(zoneId) == CashbotHQ:
                    where = "mintInterior"
                else:
                    zoneUtilNotify.error("unknown cogHQ interior for hood: " + str(getHoodId(zoneId)))
            else:
                zoneUtilNotify.error("unknown cogHQ where: " + str(zoneId))
        elif suffix == 0:
            where="playground"
        elif suffix >= 500:
            if isToon:
                where="toonInterior"
            else:
                where="suitInterior"
        else:
            where="street"
    return where

def getBranchZone(zoneId):
    # examples:
    # zoneId ==> returns
    # 1 ==> 0
    # 2000 ==> 2000
    # 2100 ==> 2100
    # 2135 ==> 2100
    # 2501 ==> 2000
    # 3678 ==> 3100
    # 40000 => 40000
    # 40135 => 40100

    # If the override is in effect, then return the given branch.
    global tutorialDict
    if tutorialDict:
        branchId = tutorialDict["branch"]
    else:
        branchId = zoneId - (zoneId % 100)
        if not isCogHQZone(zoneId):
            if (zoneId % 1000) >= 500:
                # ...this is an interior zone id.
                branchId -= 500        
    assert(zoneUtilNotify.debug("getBranchZone(zoneId="
            +str(zoneId)+") returning "+str(branchId)))
    return branchId

def getCanonicalBranchZone(zoneId):
    # examples:
    # zoneId ==> returns
    # 1 ==> 0
    # 2000 ==> 2000
    # 2100 ==> 2100
    # 2135 ==> 2100
    # 2501 ==> 2000
    # 3678 ==> 3100
    # 40000 => 2000
    # 40135 => 2100
    return getBranchZone(getCanonicalZoneId(zoneId))

def isWelcomeValley(zoneId):
    """
    Returns true if the indicated zoneId represents one of the special
    "WelcomeValley" zones, false otherwise.

    # 2000 ==> 0
    # 2100 ==> 0
    # 3678 ==> 0
    # 40000 => 1
    # 40135 => 1

    """
    return zoneId == WelcomeValleyToken or (
        zoneId >= WelcomeValleyBegin and zoneId < WelcomeValleyEnd)

def getCanonicalZoneId(zoneId):
    """
    Returns zoneId unchanged, except when we are in a WelcomeValley, in
    which case it returns the corresponding static zoneId.

    # 2000 ==> 2000
    # 2100 ==> 2100
    # 2135 ==> 2135
    # 2501 ==> 2501
    # 3678 ==> 3678
    # 40000 => 2000
    # 40135 => 2135

    """
    if zoneId == WelcomeValleyToken:
        # need GS case?
        zoneId = ToontownCentral
    elif zoneId >= WelcomeValleyBegin and zoneId < WelcomeValleyEnd:
        zoneId = (zoneId%2000)
        if zoneId < 1000:
            zoneId = zoneId + ToontownCentral
        else:
            zoneId = zoneId - 1000 + GoofySpeedway
    return zoneId

def getTrueZoneId(zoneId, currentZoneId):
    """
    If we are in WelcomeValley, converts the canonical (e.g. 2000, 2100,
    etc.) zoneId to the actual WelcomeValley-appropriate zoneId
    (e.g. 40000, 40100, etc.  The currentZoneId is used to determine
    which WelcomeValley we are in.

    # 2000 ==> 40000
    # 2100 ==> 40100
    # 2135 ==> 40135
    # 2501 ==> 40501
    # 3678 ==> 3678
    # 40000 => 40000
    # 40135 => 40135
    """
    if (zoneId >= WelcomeValleyBegin and \
       zoneId < WelcomeValleyEnd) or zoneId == WelcomeValleyToken:
        zoneId = getCanonicalZoneId(zoneId)

    if currentZoneId >= WelcomeValleyBegin and \
       currentZoneId < WelcomeValleyEnd:
        hoodId = getHoodId(zoneId)
        offset = currentZoneId - (currentZoneId % 2000)
        if hoodId == ToontownCentral:
            return (zoneId - ToontownCentral) + offset
        elif hoodId == GoofySpeedway: 
            return (zoneId - GoofySpeedway) + offset + 1000
    return zoneId

def getHoodId(zoneId):
    """includes HQ zones"""
    # examples:
    # zoneId ==> returns
    # 1 ==> 0
    # 2000 ==> 2000
    # 2100 ==> 2000
    # 2135 ==> 2000
    # 2501 ==> 2000
    # 3678 ==> 3000
    # 40000 => 40000
    # 40135 => 40000

    # if the override is in effect, then return the TutorialHood
    global tutorialDict
    if tutorialDict:
        hoodId = Tutorial
    else:
        hoodId = zoneId - (zoneId % 1000)
    assert(zoneUtilNotify.debug("getHoodId(zoneId="
            +str(zoneId)+") returning "+str(hoodId)))
    return hoodId

def getSafeZoneId(zoneId):
    """returns hoodId of nearest playground; maps HQ zones to their
    closest safezone"""
    # examples:
    # zoneId ==> returns
    # 1 ==> 0
    # 2000 ==> 2000
    # 2100 ==> 2000
    # 2135 ==> 2000
    # 2501 ==> 2000
    # 3678 ==> 3000
    # 40000 => 40000
    # 40135 => 40000
    # 11000 => 5000
    # 11100 => 5000
    hoodId = getHoodId(zoneId)
    if hoodId in HQToSafezone:
        hoodId = HQToSafezone[hoodId]
    return hoodId

def getCanonicalHoodId(zoneId):
    # examples:
    # zoneId ==> returns
    # 1 ==> 0
    # 2000 ==> 2000
    # 2100 ==> 2000
    # 2135 ==> 2000
    # 2501 ==> 2000
    # 3678 ==> 3000
    # 40000 => 2000
    # 40135 => 2000
    return getHoodId(getCanonicalZoneId(zoneId))

def getCanonicalSafeZoneId(zoneId):
    # Just like getCanonicalHoodId except HQs get translated as well.
    return getSafeZoneId(getCanonicalZoneId(zoneId))

def isInterior(zoneId):
    global tutorialDict
    if tutorialDict:
        # if the override is in effect, check the list.
        if zoneId in tutorialDict["interiors"]:
            r = 1
        else:
            r = 0
    else:
        # if the override is not in effect, do the math.
        r = (zoneId%1000)>=500
    assert(zoneUtilNotify.debug("isInterior(zoneId="
            +str(zoneId)+") returning "+str(r)))
    return r

def overrideOn(branch, exteriorList, interiorList):
    #print "OVERRIDE ON: "
    #print exteriorList
    #print interiorList
    # This lets us override the math of ZoneUtil during the tutorial.
    global tutorialDict
    if tutorialDict:
        zoneUtilNotify.warning("setTutorialDict: tutorialDict is already set!")

    tutorialDict = {"branch" : branch,
                    "exteriors" : exteriorList,
                    "interiors" : interiorList,
                    }

def overrideOff():
    #print "OVERRIDE OFF:"
    global tutorialDict
    # This is used to turn off the override when the tutorial is over.
    tutorialDict = None

def getWakeInfo(hoodId=None, zoneId=None):
    """returns showWake, wakeWaterHeight"""
    wakeWaterHeight = 0
    showWake = 0
    try:
        # Determine wake water level based on hood
        if hoodId is None:
            hoodId = base.cr.playGame.getPlaceId()
        if zoneId is None:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        canonicalZoneId = getCanonicalZoneId(zoneId)
        # Lets show wake in Toontown Central and Donalds Dock
        if (canonicalZoneId == DonaldsDock):
            wakeWaterHeight = DDWakeWaterHeight
            showWake = 1
        elif (canonicalZoneId == ToontownCentral):
            wakeWaterHeight = TTWakeWaterHeight
            showWake = 1
        elif (canonicalZoneId == OutdoorZone):
            wakeWaterHeight = OZWakeWaterHeight
            showWake = 1
        elif (hoodId == MyEstate):
            wakeWaterHeight = EstateWakeWaterHeight
            showWake = 1
        else:
            # Don't show it everywhere else
            pass
    except AttributeError:
        # We don't know what hood we're in, pass
        pass

    return showWake, wakeWaterHeight
