from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase.MessengerGlobal import *
from direct.showbase.BulletinBoardGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.showbase.JobManagerGlobal import *
from direct.showbase.EventManagerGlobal import *
from direct.showbase.PythonUtil import *
from direct.showbase import PythonUtil
from direct.interval.IntervalManager import ivalMgr

from direct.task import Task
from direct.showbase import EventManager
from direct.showbase import ExceptionVarDump
import math
import sys
import time
import gc

## assert game.process == 'ai', "Are you intentionally running ai code on %s"%(game.process,)

class AIBase:
    notify = directNotify.newCategory("AIBase")

    def __init__(self):
        # Get the dconfig object
        self.config = getConfigShowbase()
        __builtins__["__dev__"] = self.config.GetBool('want-dev', 0)
        if self.config.GetBool('want-variable-dump', 0):
            ExceptionVarDump.install()
    
        if self.config.GetBool('use-vfs', 1):
            vfs = VirtualFileSystem.getGlobalPtr()
        else:
            vfs = None

        # Store dconfig variables
        self.wantTk = self.config.GetBool('want-tk', 0)

        # How long should the AI sleep between frames to keep CPU usage down
        self.AISleep = self.config.GetFloat('ai-sleep', 0.04)
        self.AIRunningNetYield = self.config.GetBool('ai-running-net-yield', 0)
        self.AIForceSleep = self.config.GetBool('ai-force-sleep', 0)
        self.eventMgr = eventMgr
        self.messenger = messenger
        self.bboard = bulletinBoard

        self.taskMgr = taskMgr
        Task.TaskManager.taskTimerVerbose = self.config.GetBool('task-timer-verbose', 0)
        Task.TaskManager.extendedExceptions = self.config.GetBool('extended-exceptions', 0)

        self.sfxManagerList = None
        self.musicManager = None
        self.jobMgr = jobMgr

        self.hidden = NodePath('hidden')
        # each zone has its own render
        #self.render = NodePath('render')

        # This graphics engine is not intended to ever draw anything, it
        # advanced clocks and clears pstats state, just like on the client.
        self.graphicsEngine = GraphicsEngine()

        # Get a pointer to Panda's global ClockObject, used for
        # synchronizing events between Python and C.
        # object is exactly in sync with the TrueClock.
        globalClock = ClockObject.getGlobalClock()

        # Since we have already started up a TaskManager, and probably
        # a number of tasks; and since the TaskManager had to use the
        # TrueClock to tell time until this moment, make sure the
        # globalClock
        self.trueClock = TrueClock.getGlobalPtr()
        globalClock.setRealTime(self.trueClock.getShortTime())
        # set the amount of time used to compute average frame rate
        globalClock.setAverageFrameRateInterval(30.)
        globalClock.tick()

        # Now we can make the TaskManager start using the new globalClock.
        taskMgr.globalClock = globalClock

        __builtins__["ostream"] = Notify.out()
        __builtins__["globalClock"] = globalClock
        __builtins__["vfs"] = vfs
        __builtins__["hidden"] = self.hidden
        #__builtins__["render"] = self.render
        
        AIBase.notify.info('__dev__ == %s' % __dev__)

        # set up recording of Functor creation stacks in __dev__
        PythonUtil.recordFunctorCreationStacks()

        # This is temporary:
        __builtins__["wantTestObject"] = self.config.GetBool('want-test-object', 0)       
        

        self.wantStats = self.config.GetBool('want-pstats', 0)
        Task.TaskManager.pStatsTasks = self.config.GetBool('pstats-tasks', 0)
        # Set up the TaskManager to reset the PStats clock back
        # whenever we resume from a pause.  This callback function is
        # a little hacky, but we can't call it directly from within
        # the TaskManager because he doesn't know about PStats (and
        # has to run before libpanda is even loaded).
        taskMgr.resumeFunc = PStatClient.resumeAfterPause

        # in production, we want to use fake textures.
        defaultValue = 1
        if __dev__:
            defaultValue = 0
        wantFakeTextures = self.config.GetBool('want-fake-textures-ai',
                                               defaultValue)
                                               
        if wantFakeTextures:
            # Setting textures-header-only is a little better than
            # using fake-texture-image.  The textures' headers are
            # read to check their number of channels, etc., and then a
            # 1x1 blue texture is created.  It loads quickly, consumes
            # very little memory, and doesn't require a bogus texture
            # to be loaded repeatedly.
            loadPrcFileData('aibase', 'textures-header-only 1')

        # If there's a Toontown-specific AIBase, that's where the following
        # config flags should be.
        # I tried putting this logic in ToontownAIRepository, but wantPets is
        # needed during the import of ToontownAIRepository.py
        self.wantPets = self.config.GetBool('want-pets', 1)
        if self.wantPets:
            if game.name == 'toontown':
                from toontown.pets import PetConstants
                self.petMoodTimescale = self.config.GetFloat(
                    'pet-mood-timescale', 1.)
                self.petMoodDriftPeriod = self.config.GetFloat(
                    'pet-mood-drift-period', PetConstants.MoodDriftPeriod)
                self.petThinkPeriod = self.config.GetFloat(
                    'pet-think-period', PetConstants.ThinkPeriod)
                self.petMovePeriod = self.config.GetFloat(
                    'pet-move-period', PetConstants.MovePeriod)
                self.petPosBroadcastPeriod = self.config.GetFloat(
                    'pet-pos-broadcast-period',
                    PetConstants.PosBroadcastPeriod)
                
        self.wantBingo = self.config.GetBool('want-fish-bingo', 1)
        self.wantKarts = self.config.GetBool('wantKarts', 1)

        self.newDBRequestGen = self.config.GetBool(
            'new-database-request-generate', 1)

        self.waitShardDelete = self.config.GetBool('wait-shard-delete', 1)
        self.blinkTrolley = self.config.GetBool('blink-trolley', 0)
        self.fakeDistrictPopulations = self.config.GetBool('fake-district-populations', 0)

        self.wantSwitchboard = self.config.GetBool('want-switchboard', 0)
        self.wantSwitchboardHacks = self.config.GetBool('want-switchboard-hacks', 0)
        self.GEMdemoWhisperRecipientDoid = self.config.GetBool('gem-demo-whisper-recipient-doid', 0)
        self.sqlAvailable = self.config.GetBool('sql-available', 1)
            
        self.createStats()

        self.restart()

        ## ok lets over ride the time yieldFunction
        #self.MaxEpockSpeed = 1.0/60.0;        
        #taskMgr.doYield = self.taskManagerDoYield;
                
        
    def setupCpuAffinities(self, minChannel):
        if game.name == 'uberDog':
            affinityMask = self.config.GetInt('uberdog-cpu-affinity-mask', -1)
        else:
            affinityMask = self.config.GetInt('ai-cpu-affinity-mask', -1)
        if affinityMask != -1:
            TrueClock.getGlobalPtr().setCpuAffinity(affinityMask)
        else:
            # this is useful on machines that perform better with each process
            # assigned to a single CPU
            autoAffinity = self.config.GetBool('auto-single-cpu-affinity', 0)
            if game.name == 'uberDog':
                affinity = self.config.GetInt('uberdog-cpu-affinity', -1)
                if autoAffinity and (affinity == -1):
                    affinity = 2
            else:
                affinity = self.config.GetInt('ai-cpu-affinity', -1)
                if autoAffinity and (affinity == -1):
                    affinity = 1
            if affinity != -1:
                TrueClock.getGlobalPtr().setCpuAffinity(1 << affinity)
            elif autoAffinity:
                if game.name == 'uberDog':
                    # set the affinity based on our channel range
                    channelSet = int(minChannel / 1000000)
                    channelSet -= 240
                    # add an offset so that the default uberdog affinity is 2
                    affinity = channelSet + 3
                    # this could be better if we know how many CPUs we have
                    # for now spread the uberdogs across 4 processors
                    TrueClock.getGlobalPtr().setCpuAffinity(1 << (affinity % 4))

    #########################################################################
    # This is the yield function for simple timing based .. no consideration for Network and such..
    ###########################################################################        
    def  taskManagerDoYield(self , frameStartTime, nextScheuledTaksTime):
        minFinTime = frameStartTime + self.MaxEpockSpeed
        if nextScheuledTaksTime > 0 and nextScheuledTaksTime < minFinTime:
            minFinTime = nextScheuledTaksTime;
            
        delta = minFinTime - globalClock.getRealTime();
        while(delta > 0.002):
            time.sleep(delta)           
            delta = minFinTime - globalClock.getRealTime();
        

    def createStats(self, hostname=None, port=None):
        # You can specify pstats-host in your Config.prc or use ~pstats/~aipstats
        # The default is localhost
        if not self.wantStats:
            return False

        if PStatClient.isConnected():
            PStatClient.disconnect()
        # these default values match the C++ default values
        if hostname is None:
            hostname = ''
        if port is None:
            port = -1
        PStatClient.connect(hostname, port)
        return PStatClient.isConnected()

    def __sleepCycleTask(self, task):
        # To keep the AI task from running too fast, we sleep a bit here
        time.sleep(self.AISleep)
        return Task.cont

    def __resetPrevTransform(self, state):
        # Clear out the previous velocity deltas now, after we have
        # rendered (the previous frame).  We do this after the render,
        # so that we have a chance to draw a representation of spheres
        # along with their velocities.  At the beginning of the frame
        # really means after the command prompt, which allows the user
        # to interactively query these deltas meaningfully.

        PandaNode.resetAllPrevTransform()
        return Task.cont

    def __ivalLoop(self, state):
        # Execute all intervals in the global ivalMgr.
        ivalMgr.step()
        return Task.cont

    def __igLoop(self, state):
        # This advances the clocks and clears pstats state
        self.graphicsEngine.renderFrame()
        return Task.cont

    def shutdown(self):
        self.taskMgr.remove('ivalLoop')        
        self.taskMgr.remove('igLoop')
        self.taskMgr.remove('aiSleep')
        self.eventMgr.shutdown()

    def restart(self):
        self.shutdown()
        # __resetPrevTransform goes at the very beginning of the frame.
        self.taskMgr.add(
            self.__resetPrevTransform, 'resetPrevTransform', priority = -51)
        # spawn the ivalLoop with a later priority, so that it will
        # run after most tasks, but before igLoop.
        self.taskMgr.add(self.__ivalLoop, 'ivalLoop', priority = 20)
        self.taskMgr.add(self.__igLoop, 'igLoop', priority = 50)
        if self.AISleep >= 0 and  (not self.AIRunningNetYield or self.AIForceSleep):
            self.taskMgr.add(self.__sleepCycleTask, 'aiSleep', priority = 55)
                    
        self.eventMgr.restart()

    def getRepository(self):
        return self.air

    def run(self):
        self.taskMgr.run()
