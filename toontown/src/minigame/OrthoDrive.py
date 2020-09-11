""" OrthoDrive.py: contains the OrthoDrive class """

from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
import ArrowKeys
from direct.task.Task import Task

class OrthoDrive:
    """
    monitors the arrow keys and moves the localtoon orthogonally and
    diagonally wrt its parent node, where 'up' maps to +Y and
    'right' maps to +X
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("OrthoDrive")

    TASK_NAME = "OrthoDriveTask"
    SET_ATREST_HEADING_TASK = "setAtRestHeadingTask"

    def __init__(self, speed,
                 maxFrameMove=None,
                 customCollisionCallback=None,
                 priority=0, setHeading=1,
                 upHeading=0,
                 instantTurn=False):
        """
        customCollisionCallback should accept (current position,
        proposed offset) and return a (potentially modified) offset

        upHeading is the heading that corresponds to moving in the direction
        of the 'up' key; defaults to zero
        instantTurn - True makes the toon turn instantly to his direction, needed for CogThief game
        """
        self.speed = speed
        self.maxFrameMove = maxFrameMove
        self.customCollisionCallback = customCollisionCallback
        self.priority = priority
        self.setHeading = setHeading
        self.upHeading = upHeading
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.lt = base.localAvatar
        self.instantTurn = instantTurn

    def destroy(self):
        self.arrowKeys.destroy()
        del self.arrowKeys
        del self.customCollisionCallback

    def start(self):
        self.notify.debug("start")
        self.__placeToonHOG(self.lt.getPos())
        taskMgr.add(self.__update, OrthoDrive.TASK_NAME,
                    priority=self.priority)

    def __placeToonHOG(self, pos, h=None):
        # place the toon unconditionally in a new position
        if h == None:
            h = self.lt.getH()

        self.lt.setPos(pos)
        self.lt.setH(h)

        self.lastPos=pos

        self.atRestHeading=h
        self.lastXVel=0; self.lastYVel=0

    def stop(self):
        self.notify.debug("stop")
        taskMgr.remove(OrthoDrive.TASK_NAME)
        taskMgr.remove(OrthoDrive.SET_ATREST_HEADING_TASK)
        if hasattr(self, 'turnLocalToonIval'):
            if self.turnLocalToonIval.isPlaying():
                self.turnLocalToonIval.pause()
            del self.turnLocalToonIval
        # make localToon stop running
        base.localAvatar.setSpeed(0,0)

    def __update(self, task):
        # move the local toon
        vel = Vec3(0,0,0)

        # first figure out which direction to move
        xVel = 0
        yVel = 0
        if self.arrowKeys.upPressed():
            yVel += 1
        if self.arrowKeys.downPressed():
            yVel -= 1
        if self.arrowKeys.leftPressed():
            xVel -= 1
        if self.arrowKeys.rightPressed():
            xVel += 1

        vel.setX(xVel)
        vel.setY(yVel)

        # calculate velocity
        vel.normalize()
        vel *= self.speed

        ## animate the toon
        speed = vel.length()
        self.lt.setSpeed(speed, 0)

        if self.setHeading:
            self.__handleHeading(xVel, yVel)

        # move the toon
        toonPos = self.lt.getPos()
        dt = globalClock.getDt()
        posOffset = vel * dt

        # toon may have been pushed at the end of last frame
        # remove any amount that the toon has been pushed,
        # and tack it on to the offset that we're testing this
        # frame
        posOffset += toonPos - self.lastPos
        toonPos = self.lastPos

        # make sure we don't move too far in one frame
        if self.maxFrameMove:
            posOffsetLen = posOffset.length()
            if posOffsetLen > self.maxFrameMove:
                posOffset *= self.maxFrameMove
                posOffset /= posOffsetLen
                #self.notify.debug("clipped to: " + `posOffset.length()`)

        # do custom collisions
        if self.customCollisionCallback:
            toonPos = self.customCollisionCallback(toonPos, toonPos + posOffset)
        else:
            toonPos = toonPos + posOffset

        self.lt.setPos(toonPos)
        self.lastPos = toonPos

        return Task.cont

    def __handleHeading(self, xVel, yVel):
        def getHeading(xVel, yVel):
            # this table is indexed by x,y speed values;
            # speeds expected to be in [-1,0,1]
            # -1 wraps to end of lists
            angTab = [
                #y = 0, 1, -1
                [None,   0,  180], # x = 0
                [ -90, -45, -135], # x = 1
                [  90,  45,  135], # x = -1
                ]
            return angTab[xVel][yVel] + self.upHeading

        def orientToon(angle, self=self):
            startAngle = self.lt.getH()
            startAngle = fitSrcAngle2Dest(startAngle,angle)
            dur = .1 * abs(startAngle-angle)/90
            self.turnLocalToonIval = LerpHprInterval(
                self.lt, dur, Point3(angle,0,0),
                startHpr = Point3(startAngle,0,0),
                name='OrthoDriveLerpHpr')
            if self.instantTurn:
                self.turnLocalToonIval.finish()
            else:
                self.turnLocalToonIval.start()

        # if this frame's pressed keys are different from last frame's:
        #   clear the doLater
        #   if no keys are down:
        #     orient the toon using the at-rest heading
        #   else:
        #     if it was a diagonal, and one of them was released:
        #       set up a doLater to set the at-rest heading
        #     else:
        #       set the at-rest heading using the current key combo
        #     orient the toon according to the current key combo
        #
        # this algorithm makes it easier for the player to leave the
        # toon facing diagonally
        if (xVel != self.lastXVel) or (yVel != self.lastYVel):
            # user is now pressing a different key combo
            taskMgr.remove(OrthoDrive.SET_ATREST_HEADING_TASK)

            if not (xVel or yVel):
                # user is not pressing anything
                # we just came to rest; turn to the at-rest heading
                orientToon(self.atRestHeading)
            else:
                # user is pressing at least one key
                curHeading = getHeading(xVel, yVel)
                # test: were they pressing a diagonal, and now are not?
                if ((self.lastXVel and self.lastYVel) and
                    not (xVel and yVel)):
                    # delay a little bit before accepting this new
                    # heading as the at-rest heading
                    def setAtRestHeading(task, self=self,
                                         angle=curHeading):
                        self.atRestHeading = angle
                        return Task.done
                    taskMgr.doMethodLater(.05, setAtRestHeading,
                                          OrthoDrive.SET_ATREST_HEADING_TASK)
                else:
                    self.atRestHeading = curHeading
                orientToon(curHeading)

        self.lastXVel = xVel; self.lastYVel = yVel
