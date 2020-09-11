""" DistributedMMPianoAI module:  contains the DistributedMMPiano
    class which represents the server version of the round,
    spinning piano in Minnie's Melodyland safezone."""

from otp.ai.AIBase import *
from toontown.toonbase.ToontownGlobals import *
from direct.distributed.ClockDelta import *

from direct.distributed import DistributedObjectAI
from direct.task import Task

# These are the various speeds the piano cycles through as people push
# the button.
PianoSpeeds = [
    1.0, 2.0, 3.0, 4.0, 5.0, 6.0,
    8.0, 10.0, 12.0, 14.0, 16.0, 18.0
    ]

PianoMaxSpeed = PianoSpeeds[len(PianoSpeeds) - 1]

# This is the factor by which the piano slows down every 10 seconds
# when people are not pushing the button. 1.0 would keep a constant
# speed; 0.0 would instantly stop.
PianoSlowDownFactor = 0.7
PianoSlowDownInterval = 10.0
PianoSlowDownMinimum = 0.1

class DistributedMMPianoAI(DistributedObjectAI.DistributedObjectAI):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // DistributedMMPianoAI:  server side version of the spinning piano
    //                        located in Minnie's Melodyland safezone.
    //                        Handle's state management of the piano.
    //
    ////////////////////////////////////////////////////////////////////
    """
    def __init__(self, air):
        """__init__(air)
        """
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.spinStartTime = 0.0
        self.rpm = 0.0
        self.degreesPerSecond = (self.rpm/60.0) * 360.0
        self.offset = 0.0
        self.direction = 1
        return None

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def requestSpeedUp(self):
        """
        requestSpeedUp(self)

        Sent from a client to speed up the piano, if allowed.

        """
        if self.rpm < PianoMaxSpeed:
            # Look for the first speed greater then self.rpm.
            for speed in PianoSpeeds:
                if speed > self.rpm:
                    break
                
            self.updateSpeed(speed, self.direction)

        self.d_playSpeedUp(self.air.getAvatarIdFromSender())
        self.__slowDownLater()

    def requestChangeDirection(self):
        """
        requestChangeDirection(self)

        Sent from a client to reverse the direction of the piano.

        """
        rpm = self.rpm
        if rpm == 0.0:
            rpm = PianoSpeeds[0]

        self.updateSpeed(rpm, -self.direction)
        self.__slowDownLater()

        self.d_playChangeDirection(self.air.getAvatarIdFromSender())

    def d_setSpeed(self, rpm, offset, startTime):
        """d_setSpeed(self, float rpm, float offset, float startTime)
        Tells the clients about the new rotate speed of the piano.
        """
        self.sendUpdate('setSpeed', [rpm, offset, globalClockDelta.localToNetworkTime(startTime)])

    def d_playSpeedUp(self, avId):
        """d_playSpeedUp(self, uint32 avId)
        Tells the clients (other than avId) to play the speed-up
        sound effect.
        """
        self.sendUpdate('playSpeedUp', [avId])

    def d_playChangeDirection(self, avId):
        """d_playChangeDirection(self, uint32 avId)
        Tells the clients (other than avId) to play the change-direction
        sound effect.
        """
        self.sendUpdate('playChangeDirection', [avId])


    ### Support functions ###
    def updateSpeed(self, rpm, direction):
        """updateSpeed(self, rpm, direction)

        Changes the speed of the piano to the indicated RPM, while
        maintaining continuity with its previous position.

        """
        now = globalClock.getRealTime()

        # First, determine its current orientation at this time.
        heading = \
                (self.degreesPerSecond * (now - self.spinStartTime)) + \
                self.offset

        # That becomes the new offset as of the new start time, now.
        self.rpm = rpm
        self.direction = direction
        self.degreesPerSecond = (rpm/60.0) * 360.0 * direction
        self.offset = heading % 360.0
        self.spinStartTime = now

        # Inform all the clients.
        self.d_setSpeed(self.rpm * self.direction, self.offset,
                        self.spinStartTime)


    ### How you start up the piano ###
    def start(self):
        # Nothing to do here at the moment.  The piano starts up
        # stationary, and starts to move when clients bump into stuff.
        return None

    def __slowDownLater(self):
        # Slow down the piano after a period of time.
        taskName = self.uniqueName("slowDown")
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(PianoSlowDownInterval, self.__slowDown, taskName)

    def __slowDown(self, task):
        """__slowDown(self)

        This is called every PianoSlowDownInterval seconds while the
        piano is turning, to cause its speed to gradually decay.

        """
        rpm = self.rpm * PianoSlowDownFactor
        if rpm < PianoSlowDownMinimum:
            # Consider it stopped.
            self.updateSpeed(0.0, self.direction)

        else:
            self.updateSpeed(rpm, self.direction)
            self.__slowDownLater()
            
        return Task.done

        
            
        

# History
#
# 08Oct01    jlbutler    created.
# 08Oct22    drose       modified to change speeds from time to time.
#
