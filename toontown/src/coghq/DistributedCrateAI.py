from CrateGlobals import *
from direct.directnotify import DirectNotifyGlobal
import DistributedCrushableEntityAI
from direct.task import Task
import CrateGlobals

class DistributedCrateAI(DistributedCrushableEntityAI.DistributedCrushableEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrateAI")
    def __init__(self, level, entId):
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.__init__(self, level, entId)
        self.grid = None
        self.avId = 0
        self.tPowerUp = 0  # time it takes to overcome static friction
        self.width = 2      # number of columns(or rows) wide
        
    def generate(self):
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.generate(self)
    
    def delete(self):
        taskMgr.remove(self.taskName("sendPush"))
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.delete(self)

    def requestPush(self, side):
        self.notify.debug("requestPush")
        avId = self.air.getAvatarIdFromSender()

        # validate the side argument
        if side not in [0,1,2,3]:
            self.air.writeServerEvent('suspicious', avId, 'DistributedCrateAI.requestPush given invalid side arg')
            return
       
        if not self.avId and self.grid.checkPush(self.entId, side):
            self.avId = avId
            self.side = side

            # Handle unexpected exit
            self.acceptOnce(self.air.getAvatarExitEvent(avId),
                            self.__handleUnexpectedExit, extraArgs=[avId])
            
            # delay for a tick and then let the client start pushing
            taskMgr.remove(self.taskName("sendPush"))
            taskMgr.doMethodLater(self.tPowerUp,
                                  self.sendPushTask,
                                  self.taskName("sendPush"))
        else:
            self.sendUpdateToAvatarId(avId, "setReject", [])

    def setDone(self):
        self.notify.debug("setDone")
        avId = self.air.getAvatarIdFromSender()
        # avId has stopped pushing
        if avId == self.avId:
            # tell the AI we want to stop pushing.  We can't stop
            # pushing immediately, we have to wait for the next
            # push in the queue to finish
            taskMgr.remove(self.taskName("sendPush"))
            self.avId = 0

    def sendPushTask(self, task):
        self.notify.debug("sendPushTask")

        # if the grid allows it, then let the client do the push
        oldPos = self.grid.getObjPos(self.entId)

        if self.grid.doPush(self.entId, self.side):
            newPos = self.grid.getObjPos(self.entId)
            self.sendUpdate("setMoveTo",
                            [self.avId,
                             oldPos[0], oldPos[1], oldPos[2],
                             newPos[0], newPos[1], newPos[2]])
            
            # queue up another push
            taskMgr.doMethodLater(CrateGlobals.T_PUSH + CrateGlobals.T_PAUSE,
                                  self.sendPushTask,
                                  self.taskName("sendPush"))
        else:
            taskMgr.remove(self.taskName("sendPush"))
            self.sendUpdateToAvatarId(self.avId, "setReject", [])
            self.avId = 0
            
        return Task.done
    
    def updateGrid(self):
        # Note:  crates automatically update
        # the grid when they are pushed, so they don't need to do
        # anyting special here
        return

    def doCrush(self, crusherId, axis):
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.doCrush(self, crusherId, axis)
        # remove ourselves from grid
        # SDN: take this out for testing
        #self.grid.removeObject(self.entId)

        # delete ourselves?  this is too aggressive for me right now.
        # self.requestDelete()
        
    def setGridId(self, gridId):
        self.gridId = gridId
        grid = self.level.entities.get(gridId, None)
        if grid:
            self.grid = grid
            # put this on the grid
            # add this crate to the grid (if not added already)
            self.grid.addObjectByPos(self.entId, self.pos, width=2)
            self.b_setPosition(self.getPosition())
        
    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        
        if self.avId == avId:
            self.avId = 0
