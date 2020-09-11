"""DistributedChar module: contains the DistributedChar class"""

from otp.avatar import DistributedAvatar
import Char

class DistributedChar(DistributedAvatar.DistributedAvatar, Char.Char):
    """DistributedChar class:"""

    def __init__(self, cr):
        try:
            self.DistributedChar_initialized
        except:
            self.DistributedChar_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            Char.Char.__init__(self)

    def delete(self):
        try:
            self.DistributedChar_deleted
        except:
            self.DistributedChar_deleted = 1
            Char.Char.delete(self)
            DistributedAvatar.DistributedAvatar.delete(self)

    # We need to force the Char version of these to be called, otherwise
    # we get the generic Avatar version which is undefined
    def setDNAString(self, dnaString):
        Char.Char.setDNAString(self, dnaString)

    def setDNA(self, dna):
        Char.Char.setDNA(self, dna)

    def playDialogue(self, *args):
        # Force the right inheritance chain to be called
        Char.Char.playDialogue(self, *args)

#    def setPos(self, x, y, z):
#        from ToonBaseGlobal import *
#        self.reparentTo(render)
#        Char.Char.setPos(self, x, y, z)

#    def setHpr(self, h, p, r):
#        from ToonBaseGlobal import *
#        self.reparentTo(render)
#        Char.Char.setHpr(self, h, p, r)

#    def setPosHpr(self, x, y, z, h, p, r):
#        from ToonBaseGlobal import *
#        self.reparentTo(render)
#        Char.Char.setPosHpr(self, x, y, z, h, p, r)

    def setHp(self, hp):
        self.hp = hp
        
