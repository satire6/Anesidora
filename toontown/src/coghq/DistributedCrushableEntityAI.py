from otp.level import DistributedEntityAI
from direct.directnotify import DirectNotifyGlobal


class DistributedCrushableEntityAI(DistributedEntityAI.DistributedEntityAI):
    """ This is a crushable version of NodePathEntity.  To make
    it functionally crushable, a crushMgrEntId attribute must
    be specified."""
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrushableEntityAI")
    def __init__(self, level, entId):
        self.isCrushable = 0
        self.crushCellId = None
        self.crushCell = None
        self.grid = None
        self.width=1
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)

    def generate(self):
        DistributedEntityAI.DistributedEntityAI.generate(self)
        self.setActiveCrushCell()
        if self.level:
            self.attachToGrid()

    def delete(self):
        self.ignoreAll()
        DistributedEntityAI.DistributedEntityAI.delete(self)

    def destroy(self):
        if self.crushCell != None:
            self.crushCell.unregisterCrushable(self.entId)
            self.crushCell = None
        DistributedEntityAI.DistributedEntityAI.destroy(self)
                
    def attachToGrid(self):
        if self.gridId is not None:
            # get grid, or listen for grid
            def setGrid(gridId=self.gridId, self=self):
                grid = self.level.entities.get(gridId, None)
                if grid:
                    self.grid = grid
                    # put this on the grid
                    # add this object to the grid (if not added already)
                    self.grid.addObjectByPos(self.entId, self.pos, self.width)
                    self.b_setPosition(self.getPosition())
                    self.initGridDependents()
                    return 1
                return 0
            self.level.setEntityCreateCallback(self.gridId,
                                               setGrid)

    def initGridDependents(self):
        # anything that needs the grid to be set up before running should
        # be initialized/run here
        return
    
    def setActiveCrushCell(self):
        if self.crushCellId != None:
            self.notify.debug("setActiveCrushCell, entId: %d" % self.entId)
            self.crushCell = self.level.entities.get(self.crushCellId, None)

            if self.crushCell == None:
                self.accept(self.level.getEntityCreateEvent(self.crushCellId),
                            self.setActiveCrushCell)
            else:
                # we found the associated activeCrushCell, now this entity
                # is marked as a CRUSHER!!!
                self.isCrushable = 1

                # register with crusherCell as a crushable entity
                self.crushCell.registerCrushable(self.entId)
                
                
    def b_setPosition(self, pos):
        self.d_setPosition(pos)
        self.setPosition(pos)
        
    def d_setPosition(self, pos):
        self.sendUpdate('setPosition', [pos[0],pos[1],pos[2]])

    def setPosition(self, pos):
        self.pos = pos
        
    def getPosition(self):
        return self.grid.getObjPos(self.entId)

    def updateGrid(self):
        # The AI may want to force the crushable entity to update
        # it's position on the grid.  This is used by the stompers
        # before the stomper sends it's STOMPER_STOMP message to
        # the client.  This way the client has updated info on what is in
        # the crusherCells before it stomps.

        # Derived classes should implement this method if they want
        # to update the grid.  Note:  crates automatically update
        # the grid when they are pushed, so they don't need to do
        # anyting special.
        return

    def doCrush(self, crusherId, axis):
        assert(self.notify.debug("doCrush, axis = %s" % axis))
        # derived classes can define this method if they
        # want something else to happen when they are crushed
        # (i.e. animation, removal from grid, etc)

        # tell client about being crushed
        # self.sendUpdate("setCrushed", [crusherId, axis])
        
    def setGridId(self, gridId):
        self.gridId = gridId
        self.attachToGrid() 

    def setCrushCellId(self, crushCellId):
        self.crushCellId = crushCellId
        self.setActiveCrushCell()
        
 
