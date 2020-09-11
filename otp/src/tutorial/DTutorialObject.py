from direct.fsm.FSM import FSM
from direct.distributed.DistributedObject import DistributedObject 
from direct.distributed.ClockDelta import globalClockDelta
from otp.tutorial.DTutorialObjectBase import DTutorialObjectBase

class DTutorialObject(DistributedObject,DTutorialObjectBase):

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = ''
        self.mealRequest = False

        # we place this object in __builtin__ for convenience.
        # Do not do this in production!
        import __builtin__
        __builtin__.tutObj = self

        
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def announceGenerate(self):
        # all required fields have been set at this point
        # after this function resolves, the remaining 'ram' fields will be applied
        pass

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def disable(self):
        # This function should return the object to a state as if it had just completed the
        # __init__() call.  Basically, anything that you did during and after announceGenerate()
        # needs to be undone.
        pass

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def delete(self):
        # clean up everything here.  This should be the last high-level function called on
        # this object.  Anything done between __init__() and announceGenerate() should be
        # cleaned up here.
        pass

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setName(self, name):
        self.name = name
        
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def b_requestMeal(self, type):
        if not self.mealRequest:
            self.requestMeal(type)
            self.d_requestMeal(type)

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def d_requestMeal(self, type):
        self.sendUpdate('requestMeal', [type])

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def requestMeal(self, type):
        self.mealRequest = True

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setMeal(self, meal, timestamp):
        self.meal = meal
        self.lastMealTime = globalClockDelta.networkToLocalTime(timestamp)
        self.mealRequest = False

    def getTimeSinceLastMeal(self):
        return globalClock.getFrameTime() - self.lastMealTime
    
    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setColor(self, r, g, b):
        self.color = (r,g,b)

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setNumbers(self, a, b, c):
        self.color = (a,b,c)

    @report(types = ['module', 'args', 'deltaStamp'], dConfigParam = ['dtutorial'])
    def setHeight(self, h):
        self.h = h
        
    

class DTutorial(FSM):
    def __init__(self):
        FSM.__init__(self, 'DTutorial')
        import __builtin__
        __builtin__.tut = self

        self.ih = None
        
    def enterPhase2(self):
        self.ih = base.cr.addInterest(201000000, [114], 'tutorial object')

    def exitPhase2(self):
        base.cr.removeInterest(self.ih)
        self.ih = None
        
    def enterPhase4(self):
        pass
    
    def enterPhase5(self):
        self.ih = base.cr.addInterest(201000000, [114], 'tutorial object')
        
    def enterPhase6(self):
        # we placed tutObj in __builtin__ for convenience.
        # Do not do this in production!
        tutObj.b_requestMeal(2)

    def enterPhase7(self):
        print tutObj.getTimeSinceLastMeal()
        
    def enterOff(self):
        if self.ih:
            base.cr.removeInterest(self.ih)
            
DTutorial()


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

 - Follow the instructions in DTutorialObjectAI.py first


 
To use this file, run this line in your client process after
your AI is running and your client is sitting at the character
select screen:

 >>> from otp.tutorial.DTutorialObject import *

This places an object called 'tut' in the global namespace.
Use this object to demonstrate the lifetime of an example
DTutorialObject.  Do this by stepping through the FSM phases
on 'tut'.

If you haven't already done so, do the steps in DTutorialObjectAI
before proceding here:

 >>> tut.request('Phase2')

At this point, you have opened interest in the zone containing the
distributed object.  It has been generated locally and is now running
normally.

TODO: further phase explanations
"""
