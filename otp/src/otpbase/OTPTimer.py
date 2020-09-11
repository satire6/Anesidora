from pandac.PandaModules import Vec4

from direct.gui.DirectGui import DirectFrame, DGG
from direct.task import Task
from direct.showbase.PythonUtil import bound

from otp.otpbase import OTPGlobals

class OTPTimer(DirectFrame):
    """
    Implements a generic onscreen timer.
    """

    ClockImage = None
    TimerId = 0
    
    def __init__(self, useImage=True, highlightNearEnd=True):
        if useImage:
            image = self.getImage()
        else:
            image = None
            
        DirectFrame.__init__(self,
                             state = DGG.DISABLED,
                             relief = None,
                             scale = 0.45,
                             image = image,
                             image_pos = (0,0,0),
                             text = "0",
                             text_fg = (0, 0, 0, 1),
                             text_font = OTPGlobals.getInterfaceFont(),
                             text_pos = (-0.01, -0.15),
                             text_scale = 0.35,
                             )
        self.initialiseoptions(OTPTimer)
        
        self.timerId = OTPTimer.TimerId
        OTPTimer.TimerId += 1
        
        self.highlightNearEnd = highlightNearEnd
        self.countdownTask = None
        self.currentTime = 0
        self.taskTime = 0.0
        
        self.setFontColor(Vec4(0, 0, 0, 1))
        
    def setFontColor(self, vColor):
        self.vFontColor = vColor
        
    def getImage(self):
        """
        Returns the image suitable for rendering the clock face.  This
        is loaded once if it has not been loaded before.  This
        function is useful to prevent loading this image (and leaking
        it) every time a OTPTimer is created.  Derived classes can override
        this function to get a game-specific timer image
        """
        if OTPTimer.ClockImage == None:
            model = loader.loadModel("phase_3.5/models/gui/clock_gui")
            OTPTimer.ClockImage = model.find("**/alarm_clock")
            model.removeNode()
        return OTPTimer.ClockImage

    def posInTopRightCorner(self):
        self.setPos(1.16, 0, 0.83)
        
    def posBelowTopRightCorner(self):
        self.setPos(1.16, 0, 0.58)

    def posAboveShtikerBook(self):
        self.setPos(1.16, 0, -.63)
        
    def setTime(self, time):
        """
        Sets the timer's current time.
        """
        # timer is only valid from 0 to 999
        time = bound(time, 0, 999)

        if time == self.currentTime:
            # No need to do anything if the new time to display is the
            # same as the last value.
            return

        self.currentTime = time
        timeStr = str(time)
        timeStrLen = len(timeStr)

        if timeStrLen == 1:
            if time <= 5 and self.highlightNearEnd:
                self.setTimeStr(timeStr, 0.34, (-0.025, -0.125), Vec4(1, 0, 0, 1))
            else:
                self.setTimeStr(timeStr, 0.34, (-0.025, -0.125))
        elif timeStrLen == 2:
            self.setTimeStr(timeStr, 0.27, (-0.025, -0.10))
        elif timeStrLen == 3:
            self.setTimeStr(timeStr, 0.2, (-0.01, -0.08))

    def setTimeStr(self, timeStr, scale = 0.2, pos = (-0.01, -0.08), fg = None):
        """
        Sets the time label being displayed.
        """
        # First, set the text to empty while we adjust the parameters.
        self["text"] = ""
        self["text_fg"] = (fg or self.vFontColor)
        self["text_scale"] = scale
        self["text_pos"] = pos
        self["text"] = timeStr
        
    def getElapsedTime(self):
        return self.taskTime
    
    def _timerTask(self, task):
        """
        Task function called every frame to implement the timer
        Note the task.time counts up from 0 so we have to subtract
        it from the duration to get the countdown time
        """
        countdownTime = int(task.duration - task.time)
        self.setTime(countdownTime)

        self.taskTime = task.time

        if task.time >= task.duration:
            # Time is up, call the callback and return Task.done
            self.timerExpired()
            if task.callback:
                task.callback()
            return Task.done
        else:
            # Timer has not expired, come back next frame
            return Task.cont

    def countdown(self, duration, callback=None):
        """
        Spawn the timer task for duration seconds.
        Calls callback when the timer is up.
        """
        self.countdownTask = Task.Task(self._timerTask)
        self.countdownTask.duration = duration
        self.countdownTask.callback = callback
        taskMgr.remove("timerTask%s" % self.timerId)
        
        return taskMgr.add(self.countdownTask, "timerTask%s" % self.timerId)

    def timerExpired(self):
        """
        Add show elements here
        """
        return
    
    def stop(self):
        """
        Stops the timer countdown. It gets rid of any countdowns.
        """
        if self.countdownTask:
            taskMgr.remove(self.countdownTask)

    def reset(self):
        """
        Resets the timer. It geta rid of any countdowns and reset the clock to 0
        """        
        self.stop()
        self.setTime(0)
        taskMgr.remove("timerTask%s" % self.timerId)
        self.taskTime = 0.0
        
    def destroy(self):
        self.reset()
        self.countdownTask = None
        DirectFrame.destroy(self)

    def cleanup(self):
        self.destroy()
        self.notify.warning("Call destroy, not cleanup")
    
