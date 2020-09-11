from direct.distributed import DistributedObjectAI
import Entity
from direct.directnotify import DirectNotifyGlobal

class DistributedEntityAI(DistributedObjectAI.DistributedObjectAI,
                          Entity.Entity):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedEntityAI')

    def __init__(self, level, entId):
        ###
        ### THIS IS WHERE AI-SIDE DISTRIBUTED ENTITIES GET THEIR ATTRIBUTES SET
        ###
        if hasattr(level, "air"):
            air = level.air
            self.levelDoId = level.doId

        else:
            # Assume we were given an AIRepository for the first
            # parameter, not a DistributedLevelAI.  This is used when
            # we are creating an entity not associated with a level
            # (e.g. a Goon walking around somewhere else).
            air = level
            level = None
            self.levelDoId = 0
            
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        Entity.Entity.__init__(self, level, entId)

    def generate(self):
        self.notify.debug('generate')
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def destroy(self):
        self.notify.debug('destroy')
        Entity.Entity.destroy(self)
        self.requestDelete()

    def delete(self):
        self.notify.debug('delete')
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getLevelDoId(self):
        return self.levelDoId

    def getEntId(self):
        return self.entId

    if __dev__:
        def setParentEntId(self, parentEntId):
            self.parentEntId = parentEntId
            # switch to new zone
            newZoneId = self.getZoneEntity().getZoneId()
            if newZoneId != self.zoneId:
                self.sendSetZone(newZoneId)
