from otp.level import DistributedEntityAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCrusherEntityAI(DistributedEntityAI.DistributedEntityAI):
    """ This is a crushable version of NodePathEntity.  To make
    it functionally crushable, a crushMgrEntId attribute must
    be specified."""
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrusherEntityAI")
    def __init__(self, level, entId):
        self.isCrusher = 0
        self.crushCell = None
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)
        self.crushMsg = self.getUniqueName('crusherDoCrush')

    def generate(self):
        DistributedEntityAI.DistributedEntityAI.generate(self)
        self.setActiveCrushCell()
        
    def delete(self):
        self.ignoreAll()
        DistributedEntityAI.DistributedEntityAI.delete(self)
        
    def destroy(self):
        self.notify.info('destroy entity %s' % self.entId)
        if self.crushCell != None:
            self.crushCell.unregisterCrusher(self.entId)
            self.crushCell = None
        DistributedEntityAI.DistributedEntityAI.destroy(self)

    def setActiveCrushCell(self):
        self.notify.debug("setActiveCrushCell, entId: %d" % self.entId)
        if self.crushCellId != None:
            self.crushCell = self.level.entities.get(self.crushCellId, None)

            if self.crushCell == None:
                self.accept(self.level.getEntityCreateEvent(self.crushCellId),
                            self.setActiveCrushCell)
            else:
                # we found the associated crusherCell, now this entity
                # is marked as a CRUSHER!!!
                self.isCrusher = 1

                # register with a crusherCell as a crusher entity
                self.crushCell.registerCrusher(self.entId)
                
    def sendCrushMsg(self, axis=0):
        assert(self.notify.debug("sendCrushMsg (%s)" % self.isCrusher))
        if self.isCrusher:
            messenger.send(self.crushMsg, [self.entId, axis])

    def getPosition(self):
        # derived class should override this method if it wants
        # to do something smarter.  For most crushers (e.g. stompers)
        # there is a self.pos set that is usually the crush position
        if hasattr(self, 'pos'):
            return self.pos
