from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.avatar import AvatarDetail
from toontown.toon import DistributedToon

class ToonDetail(AvatarDetail.AvatarDetail):

    notify = directNotify.newCategory("ToonDetail")

    def getDClass(self):
        return "DistributedToon"
    
    def createHolder(self):
        toon = DistributedToon.DistributedToon(base.cr, bFake = True)
        # getAvatarDetails puts a DelayDelete on the avatar, and this
        # is not a real DO, so bypass the 'generated' check
        toon.forceAllowDelayDelete()
        return toon
    
