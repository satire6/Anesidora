from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.level.DistributedLevelAI import DistributedLevelAI
from toontown.cogdominium.DistCogdoGameAI import DistCogdoGameAI
from toontown.cogdominium.CogdoEntityCreatorAI import CogdoEntityCreatorAI

class DistCogdoLevelGameAI(DistributedLevelAI, DistCogdoGameAI):
    notify = directNotify.newCategory("DistCogdoLevelGameAI")

    def __init__(self, air, interior):
        DistCogdoGameAI.__init__(self, air, interior)
        DistributedLevelAI.__init__(self, air, self.zoneId, 0, self.getToonIds())
        
    def createEntityCreator(self):
        return CogdoEntityCreatorAI(level=self)

    def generate(self):
        # create our spec
        self.notify.info('loading spec')
        spec = self.getLevelSpec()
        if __dev__:
            # create an EntityTypeRegistry and hand it to the spec
            self.notify.info('creating entity type registry')
            typeReg = self.getEntityTypeReg()
            spec.setEntityTypeReg(typeReg)

        DistributedLevelAI.generate(self, spec)
        DistCogdoGameAI.generate(self)
        self.startHandleEdits()
        
    def requestDelete(self):
        DistCogdoGameAI.requestDelete(self)

    def delete(self):
        self.stopHandleEdits()
        DistCogdoGameAI.delete(self)
        DistributedLevelAI.delete(self, deAllocZone=False)
        
