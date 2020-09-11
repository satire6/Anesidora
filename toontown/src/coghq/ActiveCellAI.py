from otp.level import DistributedEntityAI
from direct.directnotify import DirectNotifyGlobal

class ActiveCellAI(DistributedEntityAI.DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("ActiveCellAI")

    def __init__(self, level, entId):
        self.state = 0
        self.grid = None
        self.occupantIds = []
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)

        def setGrid(gridId=self.gridId, self=self):
            self.grid = self.level.entities.get(gridId, None)
            if self.grid:
                # add ourselves to the activeCell list on the grid
                self.grid.addActiveCell(self)
                return 1
            return 0

        if not setGrid():
            self.accept(self.level.getEntityCreateEvent(self.gridId), setGrid)

    def generate(self):
        DistributedEntityAI.DistributedEntityAI.generate(self)
        
    def delete(self):
        self.notify.debug('delete')
        self.ignoreAll()
        DistributedEntityAI.DistributedEntityAI.delete(self)

    def getState(self):
        return self.state

    def b_setState(self, state, objId = None):
        self.setState(state, objId)
        self.d_setState(state, objId)
        
    def d_setState(self, state, objId = None):
        # SDN: note, we should send all occupantIds instead
        # of just the current objId
        if not objId:
            objId = 0
        self.sendUpdate('setState', [state, objId])
    
    def setState(self, state, objId=None):
        assert(self.notify.debug("setState(%s,%s)" % (state,objId)))
        # derived classes should override this method to do something meaningful
        # when the state of this grid cell changes
        self.state = state

        # object (i.e. crate, goon) contained in this cell
        if state:
            self.occupantIds.append(objId)
        else:
            try:
                self.occupantIds.remove(objId)
            except:
                self.notify.warning("couldn't remove %s from active cell" % objId)

    def getRowCol(self):
        return [self.row,self.col]
