from direct.fsm.FSM import FSM
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.tutorial.DTutorialObjectBase import DTutorialObjectBase 
from direct.distributed.ClockDelta import globalClockDelta

class DTutorialObjectAI(DistributedObjectAI, DTutorialObjectBase):

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def __init__(self, air, name):
        DistributedObjectAI.__init__(self, air)
        self.name = name
        self.numbers = (34,42,103)
        self.height = 14
        self.meal = []
        self.lastMealTime = 0

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def announceGenerate(self):
        # all required fields have been set at this point
        # after this function resolves, the remaining ram fields will be applied
        pass

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def delete(self):
        # clean up everything here.  This should be the last high-level function called on
        # this object
        pass

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def getName(self):
        return self.name

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def getNumbers(self):
        return self.numbers
    
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def requestMeal(self, type):
        self.b_setMeal(DTutorialObjectAI.Meals[type])

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def b_setMeal(self, meal):
        local_time = globalClock.getFrameTime()
        net_time = globalClockDelta.localToNetworkTime(local_time)
        net_time = globalClockDelta.getFrameNetworkTime()
        self.d_setMeal(meal, net_time)
        self.setMeal(meal, local_time)
    
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def d_setMeal(self, meal, timestamp):
        self.sendUpdate('setMeal', [meal, timestamp])
    
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setMeal(self, meal, timestamp):
        self.meal = meal
        self.lastMealTime = timestamp

    def getTimeSinceLastMeal(self):
        return globalClock.getFrameTime() - self.lastMealTime
    
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def d_setColor(self, r, g, b):
        self.sendUpdate('setColor', [r,g,b])

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def d_setHeight(self, h):
        self.sendUpdate('setHeight', [h])

class DTutorialAI(FSM):
    def __init__(self):
        FSM.__init__(self, 'DTutorialAI')
        import __builtin__
        __builtin__.tut = self

        self.tutObj = None
        
    def enterPhase1(self):
        self.tutObj = DTutorialObjectAI(simbase.air, 'Tom')
        self.tutObj.generateOtpObject(201000000, 114, optionalFields = ['setNumbers'])
        self.tutObj.d_setColor(52,93,193)
        
    def enterPhase3(self):
        self.tutObj.d_setHeight(4)

    def enterOff(self):
        if self.tutObj:
            self.tutObj.requestDelete()

DTutorialAI()


"""
Before starting:
 - Add these lines to your local.par:
    ADDKEY=TUTORIAL_DEV  # at the top
 
    ##########################################  Tutorial
    [TUTORIAL_DEV]
    OTP_FILE_PATH=C:\cygwin\home\joswilso\dev\otp\src\tutorial\
    DC_FILE=tutorial.dc
    
 - Add this line to your Config.prc:
   dc-file $OTP/src/tutorial/tutorial.dc


   
To use this file, run this line in your AI process after your AI
is running and your client is sitting at the character select screen:

 >>> from otp.tutorial.DTutorialObjectAI import *

This places an object called 'tut' in the global namespace.
Use this object to demonstrate the lifetime of an example
DTutorialObject.  Do this by stepping through the FSM phases
on 'tut':

 >>> tut.request('Phase1')

At this point, you have created the distributed object on the
OTP server.  Go to the client and see DTutorialObject.py to invoke
Phase2.  Continue through the phases in the correct order to
demonstrate distributed object behavior.
"""
