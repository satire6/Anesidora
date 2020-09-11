""" TwoDDrive.py: contains the TwoDDrive class """

from toontown.toonbase.ToonBaseGlobal import *
from otp.otpbase import OTPGlobals
from direct.interval.IntervalGlobal import *
import ArrowKeys
from direct.task.Task import Task

class TwoDDrive:
    """
    monitors the arrow keys and moves the localtoon in a 2D space.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("TwoDDrive")

    TASK_NAME = "TwoDDriveTask"
    SET_ATREST_HEADING_TASK = "setAtRestHeadingTask"

    def __init__(self, game, speed,
                 maxFrameMove=None,
                 customCollisionCallback=None,
                 priority=0, setHeading=1,
                 upHeading=0):
        """
        customCollisionCallback should accept (current position,
        proposed offset) and return a (potentially modified) offset

        upHeading is the heading that corresponds to moving in the direction
        of the 'up' key; defaults to zero
        """
        self.game = game
        self.speed = speed
        self.maxFrameMove = maxFrameMove
        self.customCollisionCallback = customCollisionCallback
        self.priority = priority
        self.setHeading = setHeading
        self.upHeading = upHeading
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.wasUpReleased = True
        self.lt = base.localAvatar
        # Use  2D controls for the 2D game
        base.localAvatar.useTwoDControls()
        base.localAvatar.controlManager.currentControls.avatarControlJumpForce = 30.0
        
        self.ONE_JUMP_PER_UP_PRESSED = True
        self.lastAction = None
        self.isMovingX = False

    def destroy(self):
        # Setting back to the walk controls for the MMO
        self.game = None
        base.localAvatar.controlManager.currentControls.avatarControlJumpForce = 24.0
        base.localAvatar.useWalkControls()
        self.arrowKeys.destroy()
        del self.arrowKeys
        del self.customCollisionCallback
        
        self.lastAction = None

    def start(self):
        self.notify.debug("start")
        self.__placeToonHOG(self.lt.getPos())
        # Enable avatar controls so that Jump works for TwoDWalker
        base.localAvatar.enableAvatarControls()
        taskMgr.remove(TwoDDrive.TASK_NAME)
        taskMgr.add(self.__update, TwoDDrive.TASK_NAME, priority = self.priority)

    def __placeToonHOG(self, pos, h=None):
        # place the toon unconditionally in a new position
        if h == None:
            h = self.lt.getH()

        self.lt.setPos(pos)
        self.lt.setH(h)

        self.lastPos = pos

        self.atRestHeading = h
        self.oldAtRestHeading = h
        self.lastXVel=0; self.lastYVel=0

    def stop(self):
        self.notify.debug("stop")
        # Disable avatar controls so that TwoDWalker does not activate jump
        base.localAvatar.disableAvatarControls()
        taskMgr.remove(TwoDDrive.TASK_NAME)
        taskMgr.remove(TwoDDrive.SET_ATREST_HEADING_TASK)
        if hasattr(self, 'turnLocalToonIval'):
            if self.turnLocalToonIval.isPlaying():
                self.turnLocalToonIval.pause()
            del self.turnLocalToonIval
        # make localToon stop running
        base.localAvatar.setSpeed(0,0)
        base.localAvatar.stopSound()

    def __update(self, task):
        # move the local toon
        vel = Vec3(0,0,0)

        # first figure out which direction to move
        xVel = 0
        yVel = 0

        if self.ONE_JUMP_PER_UP_PRESSED:
            if not self.arrowKeys.upPressed():
                self.wasUpReleased = True
            elif self.arrowKeys.upPressed() and self.wasUpReleased:
                self.wasUpReleased = False
                # Don't jump if the toon head is still in floor1.
                if not self.game.isHeadInFloor:
                    # Calls method from TwoDWalker in direct/src/controls/
                    if (localAvatar.controlManager.currentControls == localAvatar.controlManager.get('twoD')):
                        base.localAvatar.controlManager.currentControls.jumpPressed()
        else:
            if self.arrowKeys.upPressed():
                # Don't jump if the toon head is still in floor1.
                if not self.game.isHeadInFloor:
                    # Calls method from TwoDWalker in direct/src/controls/
                    if (localAvatar.controlManager.currentControls == localAvatar.controlManager.get('twoD')):
                        base.localAvatar.controlManager.currentControls.jumpPressed()            
        if self.arrowKeys.leftPressed():
            xVel -= 1
        if self.arrowKeys.rightPressed():
            xVel += 1

        vel.setX(xVel)
        vel.setY(yVel)

        # calculate velocity
        vel.normalize()
        vel *= self.speed
        
        if (abs(xVel) > 0):
            # Avatar is moving horizontally
            if not self.isMovingX:
                self.isMovingX = True
                messenger.send('avatarMovingX')
        else:
            if self.isMovingX:
                self.isMovingX = False
                messenger.send('avatarStoppedX')

        speed = vel.length()
        action = self.lt.setSpeed(speed, 0)
        
        if (action != self.lastAction):
            self.lastAction = action
            if (action == OTPGlobals.RUN_INDEX):
                base.localAvatar.runSound()
            else:
                base.localAvatar.stopSound()

        if self.setHeading:
            self.__handleHeading(xVel, yVel)

        # move the toon
        toonPos = self.lt.getPos()
        dt = globalClock.getDt()
        posOffset = vel * dt

        '''
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
        '''
        # do custom collisions
        if self.customCollisionCallback:
            toonPos = self.customCollisionCallback(toonPos, toonPos + posOffset)
        else:
            toonPos += posOffset

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
                name='TwoDDriveLerpHpr')
            self.turnLocalToonIval.start()
            if (self.atRestHeading != self.oldAtRestHeading):
                self.oldAtRestHeading = self.atRestHeading
##                self.notify.debug('orientation changed call callBack function here')
                messenger.send('avatarOrientationChanged', [self.atRestHeading])

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
            taskMgr.remove(TwoDDrive.SET_ATREST_HEADING_TASK)

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
                                          TwoDDrive.SET_ATREST_HEADING_TASK)
                else:
                    self.atRestHeading = curHeading
                orientToon(curHeading)

        self.lastXVel = xVel; self.lastYVel = yVel
