from otp.otpbase import OTPGlobals
from otp.ai import BanManagerAI

from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil


def canAccess(avatarId, zoneId):
    avatar = simbase.air.doId2do.get(avatarId)
    if avatar and avatar.getGameAccess() != OTPGlobals.AccessFull and not openToAll(zoneId, avatar):
        simbase.air.writeServerEvent('suspicious', avatarId, 'User requesting enter for paid access content without proper rights.')
        commentStr = "Tried to gain access to an area they were not allowed to using TTInjector Hack"
        dislId = avatar.DISLid
        simbase.air.banManager.ban(avatarId, dislId, commentStr)
        return False
    else:
        return True
        
# Determine if we're in a zone that free players have access to
def openToAll(zoneId, avatar):
    canonicalZoneId = ZoneUtil.getCanonicalHoodId(zoneId)
    if  canonicalZoneId in \
       (ToontownGlobals.ToontownCentral,
        ToontownGlobals.MyEstate,
        ToontownGlobals.GoofySpeedway,
        ToontownGlobals.Tutorial,
        ) or avatar.isInEstate():
        return True
    elif(canonicalZoneId >= ToontownGlobals.DynamicZonesBegin and not avatar.getTutorialAck()): 
        # Check for being in the tutorial
        return True
    else:
        return False