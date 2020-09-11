import ActiveCellAI
from direct.directnotify import DirectNotifyGlobal

class CrusherCellAI(ActiveCellAI.ActiveCellAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CrusherCellAI")

    def __init__(self, level, entId):
        ActiveCellAI.ActiveCellAI.__init__(self, level, entId)

        # Lists of crushers and crushables that are associated with this cell.
        # Mostly the crushers will be stompers and the crushables will be
        # crates, barrels, goons, etc.
        self.crushers = []
        self.crushables = []

    def destroy(self):
        self.notify.info('destroy entity %s' % self.entId)
        # we may be destroyed before entities that are registered with us
        # clean up so that this will not be a problem
        for entId in self.crushers:
            self.unregisterCrusher(entId)
        ActiveCellAI.ActiveCellAI.destroy(self)


    def registerCrusher(self, entId):
        if entId not in self.crushers:
            ent = self.level.entities.get(entId, None)
            if ent:
                self.crushers.append(entId)
                # listen for crush msgs from crusher
                self.accept(ent.crushMsg, self.doCrush)

    def unregisterCrusher(self, entId):
        if entId in self.crushers:
            self.crushers.remove(entId)
            if not hasattr(self, 'level'):
                # We're about to crash anyway. Print out an informative
                # error. During level destruction, this is preceded in the
                # log by the entIds of crusher entities and CrusherCells as
                # they're destroyed.
                self.notify.error('unregisterCrusher(%s): CrusherCellAI %s has no attrib \'level\'' %
                                  (entId, self.entId))
            ent = self.level.entities.get(entId, None)
            if ent:
                self.ignore(ent.crushMsg)
            

    def registerCrushable(self, entId):
        if entId not in self.crushables:
            self.crushables.append(entId)

    def unregisterCrushable(self, entId):
        if entId in self.crushables:
            self.crushables.remove(entId)
        
    def doCrush(self, crusherId, axis):
        self.notify.debug("doCrush %s" % crusherId)
        # extraArgs should have  axis information so we know 
        # in which direction the crushed objects are smushed.

        for occupantId in self.occupantIds:
            # the cell is occupied, check if it is one of our crushables
            if occupantId in self.crushables:
                crushObj = self.level.entities.get(occupantId, None)
                if crushObj:
                    crushObj.doCrush(crusherId, axis)
                else:
                    self.notify.warning("couldn't find crushable object %d" % self.occupantId)
            
            
    def updateCrushables(self):
        for id in self.crushables:
            crushable = self.level.entities.get(id, None)
            if crushable:
                crushable.updateGrid()
