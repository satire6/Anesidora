from direct.directnotify import DirectNotifyGlobal
from otp.avatar import AvatarDetail
from toontown.pets import DistributedPet

class PetDetail(AvatarDetail.AvatarDetail):

    notify = DirectNotifyGlobal.directNotify.newCategory("PetDetail")

    def getDClass(self):
        return "DistributedPet"
    
    def createHolder(self):
        assert(self.notify.debug("Using PetDetail createHolder"))
        pet = DistributedPet.DistributedPet(base.cr, bFake = True)
        # getAvatarDetails puts a DelayDelete on the avatar, and this
        # is not a real DO, so bypass the 'generated' check
        pet.forceAllowDelayDelete()
        
        # We need to call generate before requesting the required fields.
        # The pet needs to create a PetMood object before receiving
        # required updates.
        # getAvatarDetails ends up calling announceGenerate, so I'm not
        # sure why it doesn't also call generate, but changing that
        # behavior broke existing code.
        pet.generateInit()
        pet.generate()

        return pet
    
