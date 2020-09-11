from otp.ai.AIBaseGlobal import *

from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals
import DistributedGoonAI
from direct.task.Task import Task
from toontown.coghq import DistributedCrushableEntityAI
import random

class DistributedGridGoonAI(DistributedGoonAI.DistributedGoonAI):
    """
    A simple, dumb robot.
    The robot should be flexible and reusable, for uses in CogHQ basements
    and factories, and perhaps other parts of the game.  Let the goon's
    movement, discovery, and attack methods be modular, so different behavior
    types can be easily plugged in.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGridGoonAI')

    def __init__(self, level, entId):
        self.grid = None
        self.h = 0
        DistributedGoonAI.DistributedGoonAI.__init__(self, level, entId)

    def generate(self):
        self.notify.debug('generate')
        # don't call GoonAI's generate, since it sends a walk
        # movie to the client
        DistributedCrushableEntityAI.DistributedCrushableEntityAI.generate(self)

    def initGridDependents(self):
        # anything that needs the grid to be set up before running should
        # be initialized/run here
        # star a timer to get the goon walking
        taskMgr.doMethodLater(2,
                              self.goToNextPoint,
                              self.taskName("walkTask"))
        
    def getPosition(self):
        if self.grid:
            return self.grid.getObjPos(self.entId)

    def getH(self):
        return self.h

    def goToNextPoint(self, task):
        if not self.grid:
            self.notify.warning("couldn't find grid, not starting")
            return
        # check the point in front of us
        if (self.grid.checkMoveDir(self.entId, self.h)):
            # If it is clear, move forward
            #  - get old pos
            ptA = Point3(*self.getPosition())
            #  - make the move
            self.grid.doMoveDir(self.entId, self.h)
            #  - get new position
            ptB = Point3(*self.getPosition())
            #  - tell the client to move the goon
            self.sendUpdate("setPathPts", [ptA[0],ptA[1],ptA[2],
                                           ptB[0],ptB[1],ptB[2]])
            # calculate the time in takes to walk to the next cell
            tPathSegment = Vec3(ptA - ptB).length() / self.velocity
            
        else:
            # if it isn't clear, turn some amount and try again
            turn = int(random.randrange(1,4) * 90)
            self.h = (self.h + turn) % 360
            tPathSegment = .1

        # set a timer for the next segment
        taskMgr.doMethodLater(tPathSegment,
                              self.goToNextPoint,
                              self.taskName("walkTask"))

        return Task.done
                              
