""" DistributedMMPiano module:  contains the DistributedMMPiano
    class which represents the client version of the round,
    spinning piano in Minnie's Melodyland safezone."""

from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *

from direct.distributed import DistributedObject
from pandac.PandaModules import NodePath
from toontown.toonbase import ToontownGlobals

# This is the amount of time, in seconds, that must elapse between two
# subsequent "change direction" requests from the same client are
# processed.  It serves to limit the "bounce" effect from
# inadvertently generating two change direction requests in a short
# time.
ChangeDirectionDebounce = 1.0

# This is the amount of time over which to effect a change in
# velocity.  Having this be nonzero allows the piano to gradually spin
# up or spin down in response to a message from the server, which
# avoids "popping" as it suddenly resets to a new position based on
# the new velocity.
ChangeDirectionTime = 1.0

class DistributedMMPiano(DistributedObject.DistributedObject): 
    """
    ////////////////////////////////////////////////////////////////////
    //
    // DistributedMMPiano:  client side version of the spinning piano
    //                      located in Minnie's Melodyland safezone.
    //                      Handle's calculating the spin of the piano
    //                      as well as detecting and letting the
    //                      'playground' know when the local toon
    //                      steps onto the piano.
    //
    ////////////////////////////////////////////////////////////////////
    """
    def __init__(self, cr):
        """__init__(cr)
        """
        DistributedObject.DistributedObject.__init__(self, cr)

        # spin information
        #
        self.spinStartTime = 0.0
        self.rpm = 0.0
        self.degreesPerSecond = (self.rpm/60.0) * 360.0
        self.offset = 0.0
        self.oldOffset = 0.0
        self.lerpStart = 0.0
        self.lerpFinish = 1.0

        self.speedUpSound = None
        self.changeDirectionSound = None
        self.lastChangeDirection = 0.0

    def generate(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   This method is called when the DistributedObject is
        //             reintroduced to the world, either for the first time
        //             or from the cache.
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.piano = base.cr.playGame.hood.loader.piano
        base.cr.parentMgr.registerParent(ToontownGlobals.SPMinniesPiano,
                                              self.piano)
        self.accept('enterlarge_round_keyboard_collisions', self.__handleOnFloor)
        self.accept('exitlarge_round_keyboard_collisions', self.__handleOffFloor)

        # We want to have some interaction from the toons in the
        # world.  For now, if a toon bumps into a mailbox or planter
        # or something, we consider that triggering the
        # "changeDirection" button.  Weird to the user--what does a
        # trashcan have to do with changing the piano?--but in the
        # absence of a "push me" button, this is the next best thing.
        self.accept('entero7', self.__handleChangeDirectionButton)

        # We need some handy sound effects to play in response to the
        # above.
        self.speedUpSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.mp3')
        self.changeDirectionSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_cymbal.mp3')

        self.__setupSpin()
        DistributedObject.DistributedObject.generate(self)

    def __setupSpin(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   Start spinning the piano
        // Parameters: ts, time at which the server initially started
        //             spinning the piano
        // Changes:    self.spinStartTime
        ////////////////////////////////////////////////////////////////////
        """
        # create a task that will update the heading of the piano often
        # in order to make it 'spin', also remember what time we first
        # started spinning so we can calculate the same heading on all
        # clients
        #
        taskMgr.add(self.__updateSpin, self.taskName("pianoSpinTask"))

    def __stopSpin(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   Stop spinning the piano
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        taskMgr.remove(self.taskName("pianoSpinTask"))

    def __updateSpin(self,task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   set the new heading/facing for the piano based
        //             on the current time and the time that the server
        //             says it started the piano spinning
        // Parameters: task, task that called this function
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getFrameTime()

        # What is the current offset?  This depends on how much time
        # has elapsed since we got the last speed update message,
        # since after we get a new update-speed message, we gradually
        # lerp the offset from the old value to the new value.
        if now > self.lerpFinish:
            offset = self.offset
        elif now > self.lerpStart:
            t = (now - self.lerpStart) / (self.lerpFinish - self.lerpStart)
            offset = self.oldOffset + t * (self.offset - self.oldOffset)
        else:
            offset = self.oldOffset
        
        heading = \
                (self.degreesPerSecond * (now - self.spinStartTime)) + \
                offset
        self.piano.setHprScale( heading % 360.0, 0.0, 0.0,
                                1.0, 1.0, 1.0 )
        return Task.cont

    def disable(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   This method is called when the DistributedObject is
        //             removed from active duty and stored in a cache.
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        del self.piano
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPMinniesPiano)

        self.ignore('enterlarge_round_keyboard_collisions')
        self.ignore('exitlarge_round_keyboard_collisions')

        self.ignore('entero7')
        self.ignore('entericon_center_collisions')
        
        self.speedUpSound = None
        self.changeDirectionSound = None
        self.__stopSpin()
        DistributedObject.DistributedObject.disable(self)

    def setSpeed(self, rpm, offset, timestamp):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   Updates the speed of the piano from the server
        // Parameters: rpm, the revolutions per minute of the piano
        //             offset, the orientation of the piano at the
        //               indicated start time, in degrees.
        //             timestamp, the 'start' time at which the piano
        //               was at the orientation indicated by offset.
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        timestamp = globalClockDelta.networkToLocalTime(timestamp)
        degreesPerSecond = (rpm/60.0) * 360.0
        now = globalClock.getFrameTime()

        # First, compute what the offset should be to keep the same
        # heading given the new rpm and timestamp.
        oldHeading = \
                   (self.degreesPerSecond * (now - self.spinStartTime)) + \
                   self.offset
        oldHeading = oldHeading % 360.0
        oldOffset = oldHeading - (degreesPerSecond * (now - timestamp))

        # Now update to the new rpm and timestamp.
        self.rpm = rpm
        self.degreesPerSecond = degreesPerSecond
        self.offset = offset
        self.spinStartTime = timestamp

        # Make sure the old and new offsets are within 180 degrees of
        # each other, so we don't try to lerp the wrong way around the
        # circle.
        while oldOffset - offset < -180.0:
            oldOffset += 360.0

        while oldOffset - offset > 180.0:
            oldOffset -= 360.0

        # Now gradually lerp from oldOffset to offset, to effect a
        # gradual change in velocity.
        self.oldOffset = oldOffset
        self.lerpStart = now
        self.lerpFinish = timestamp + ChangeDirectionTime
        
    def playSpeedUp(self, avId):
        """playSpeedUp(self, uint32 avId)

        Plays the speed-up sound effect in response to some *other*
        player (indicated by avId) hitting the speed-up button.  (We
        don't play the sound effect if avId is ourselves, because
        we've already played it directly.)
        """
        if avId != base.localAvatar.doId:
            base.playSfx(self.speedUpSound)

    def playChangeDirection(self, avId):
        """playChangeDirection(self, uint32 avId)

        Plays the speed-up sound effect in response to some *other*
        player (indicated by avId) hitting the speed-up button.  (We
        don't play the sound effect if avId is ourselves, because
        we've already played it directly.)
        """
        if avId != base.localAvatar.doId:
            base.playSfx(self.changeDirectionSound)

    def __handleOnFloor(self, collEntry):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the local toon steps on the piano
        // Parameters: collEntry, what floor local toon collided with
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.cr.playGame.getPlace().activityFsm.request('OnPiano')

        # Start the piano turning, or speed it up.
        self.sendUpdate('requestSpeedUp', [])
        base.playSfx(self.speedUpSound)

    def __handleOffFloor(self, collEntry):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the local toon steps off the piano
        // Parameters: collEntry, what floor the local toon is now off of
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.cr.playGame.getPlace().activityFsm.request('off')


    def __handleSpeedUpButton(self, collEntry):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the local toon bumps into the
        //             "speed up" button.  This speeds up the piano a
        //             notch and gives the user a satisfactory
        //             reaction indication.
        // Parameters: collEntry, ignored.
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.sendUpdate('requestSpeedUp', [])
        base.playSfx(self.speedUpSound)

    def __handleChangeDirectionButton(self, collEntry):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the local toon bumps into the
        //             "speed up" button.  This speeds up the piano a
        //             notch and gives the user a satisfactory
        //             reaction indication.
        // Parameters: collEntry, ignored.
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getFrameTime()
        if now - self.lastChangeDirection < ChangeDirectionDebounce:
            # Too soon.
            return

        self.lastChangeDirection = now
        self.sendUpdate('requestChangeDirection', [])
        base.playSfx(self.changeDirectionSound)


# History
#
# 08Oct01    jlbutler    created.
# 08Oct22    drose       modified to change speeds from time to time.
#

