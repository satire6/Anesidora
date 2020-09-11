import types
import math
from direct.interval.IntervalGlobal import Sequence, Wait, ActorInterval, Func, SoundInterval,Parallel
from direct.task import Task
from direct.fsm import FSM
from direct.showbase.PythonUtil import weightedChoice
from toontown.hood import GenericAnimatedProp
from toontown.hood import AnimatedProp
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal

class ZeroAnimatedProp(GenericAnimatedProp.GenericAnimatedProp, FSM.FSM):
    """Our base class for mailbox, trashcan, and hydrant zero that gradually increases movements."""

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'ZeroAnimatedProp')
    
    def __init__(self, node, propString, phaseInfo, holidayId):        
        """Constuct ourself and correct assumptions in base class.

        propString should be either 'mailbox','trashcan' or 'hydrant'
        phaseInfo is a dict: key is phase, tuple is (animation, pauseTime)
                             animation can be a single animation or a list of animations to play sequentially
        """
        self.propString = propString
        self.phaseInfo = phaseInfo
        self.holidayId = holidayId

        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)        
        FSM.FSM.__init__(self, '%sZeroAnimPropFsm' % self.propString)
        # we've loaded anim by default
        # now unload it and load all the anims we need
        self.node.unloadAnims('anim')
        self.loadPhaseAnims()
        self.phaseIvals = []
        # self.createPhaseIntervals() # why must this be done in enter()?
        self.curIval = None
        self.curPhase = -1
        self.okToStartNextAnim = False

    def delete(self):
        """Handle going to a different street or to the playground."""
        # exit contains our clean up code
        self.exit()
        GenericAnimatedProp.GenericAnimatedProp.delete(self)
               

    def loadPhaseAnims(self):
        """Load our animations to our actor."""
        animDict = {}
        for key,info in self.phaseInfo.iteritems():
            if type(info[0]) == types.TupleType:
                for index,anims in enumerate(info[0]):
                    fullPath = self.path + '/' + anims
                    animName = "phase%d_%d" % (key, index)
                    animDict[animName] = fullPath
            else:
                animName = 'phase%d' % key
                fullPath = self.path + '/' + info[0]
                animDict[animName] = fullPath
        self.node.loadAnims(animDict)

            
    def createPhaseIntervals(self):
        """Create the intervals for each phase."""
        if self.phaseIvals:
            self.notify.debug("not creating phase ivals again")
            return
        self.phaseIvals = []
        for key,info in self.phaseInfo.iteritems():
            self.notify.debug("key=%s"%key)
            if type(info[0]) == types.TupleType:
                ival = Sequence()
                for index,anims in enumerate(info[0]):
                    animName = "phase%d_%d" % (key, index)
                    animIval = self.node.actorInterval(animName)
                    animIvalDuration = animIval.getDuration() 
                    soundIval = self.createSoundInterval(anims, animIvalDuration)                   
                    soundIvalDuration = soundIval.getDuration()                                       
                    animAndSound = Parallel( soundIval, animIval)
                    ival.append(animAndSound)
                self.phaseIvals.append(ival)
            else:
                animName = "phase%d" % key                
                animIval = self.node.actorInterval( 'phase%d' % key)
                animIvalDuration = animIval.getDuration()
                soundIval = self.createSoundInterval(info[0], animIvalDuration )             
                soundIvalDuration = soundIval.getDuration()
                ival = Parallel(
                    animIval,
                    soundIval,
                    )
                self.phaseIvals.append(ival)
            
        
    def enter(self):
        """Show and animate the prop."""
        # lets not immediately run the animation
        assert self.notify.debugStateCall(self)
        self.node.postFlatten()
        # for some reason phaseIvals must be created here, doesn't work in __init__
        self.createPhaseIntervals()
        AnimatedProp.AnimatedProp.enter(self)

        # make it look like the other props by forcing pose 0
        defaultAnim = self.node.getAnimControl('anim')
        numFrames = defaultAnim.getNumFrames()
        self.node.pose('phase0', 0)
        self.accept("%sZeroPhase" % self.propString, self.handleNewPhase)
        self.accept("%sZeroIsRunning" % self.propString, self.handleNewIsRunning)
        self.startIfNeeded()

    def startIfNeeded(self):
        """Check our current phase, if valid go to the right state."""
        assert self.notify.debugStateCall(self)
        # we need a try to stop the level editor from crashing
        try:            
            self.curPhase = self.getPhaseToRun()
            if self.curPhase >= 0:
                self.request('DoAnim')
        except:
            pass

    def chooseAnimToRun(self):
        """Returns a weighted number between 0 and self.curPhase, inclusive"""
        # e.g. if self.curPhase is 2, we have a 4/7 chance of picking 2
        # a 2/7 chance of picking 1
        # and a 1/7 chance of picking 0
        assert self.notify.debugStateCall(self)
        result = self.curPhase
        if base.config.GetBool("anim-props-randomized", True):
            pairs = []
            for i in xrange(self.curPhase +1):
                pairs.append(( math.pow(2,i) , i))
            sum = math.pow(2,self.curPhase+1) - 1
            result = weightedChoice(pairs, sum=sum)
            self.notify.debug("chooseAnimToRun curPhase=%s pairs=%s result=%s" %
                              (self.curPhase,pairs,result))
        return result

    def createAnimSequence(self, animPhase):
        """Return a sequence which plays an anims, waits the right time, then starts next one."""
        result = Sequence( self.phaseIvals[animPhase],
                           Wait(self.phaseInfo[self.curPhase][1]),
                           Func(self.startNextAnim)
                           )
        # self.notify.debug("createAnimSequence %s" % result)
        return result

    def startNextAnim(self):
        """Start up the next anim sequence."""
        self.notify.debug("startNextAnim self.okToStartNextAnim=%s" % self.okToStartNextAnim)
        #import pdb; pdb.set_trace()
        self.curIval = None
        if self.okToStartNextAnim:
            self.notify.debug("got pass okToStartNextAnim")
            whichAnim = self.chooseAnimToRun()
            self.notify.debug("whichAnim=%s" % whichAnim)
            self.lastPlayingAnimPhase = whichAnim # merely for debugging
            self.curIval = self.createAnimSequence(whichAnim)
            self.notify.debug("starting curIval of length %s" % self.curIval.getDuration())
            self.curIval.start()
        else:
            self.notify.debug("false self.okToStartNextAnim=%s" %self.okToStartNextAnim)
        
    def enterDoAnim(self):
        """Start playing the appropriate animation."""
        self.notify.debug("enterDoAnim curPhase=%d" % self.curPhase)
        self.okToStartNextAnim = True
        self.startNextAnim()
        
    def exitDoAnim(self):
        """Stop the currently playing animation."""
        self.notify.debug("exitDoAnim curPhase=%d" % self.curPhase)
        self.okToStartNextAnim = False
        self.curIval.finish()
        self.curIval = None

    def getPhaseToRun(self):
        """This will return -1 if we should not be running, otherwise it returns
        the phase we should go to."""
        result = -1
        enoughInfoToRun = False
        # first see if the holiday is running, and we can get the cur phase
        if base.cr.newsManager.isHolidayRunning(self.holidayId):
            zeroMgrString = "%sZeroMgr" % self.propString            
            if hasattr(base.cr, zeroMgrString):
                zeroMgr = eval("base.cr.%s" % zeroMgrString)
                if not zeroMgr.isDisabled():
                    enoughInfoToRun = True
                else:
                    self.notify.debug("isDisabled = %s" % zeroMgr.isDisabled())
            else:
                self.notify.debug("base.cr does not have %s" % zeroMgrString)
        else:
            self.notify.debug("holiday is not running")
        self.notify.debug("enoughInfoToRun = %s" % enoughInfoToRun)        
        if enoughInfoToRun and \
           zeroMgr.getIsRunning():
            curPhase = zeroMgr.getCurPhase()
            if curPhase >= len (self.phaseIvals):
                curPhase = len(self.phaseIvals) -1
                self.notify.warning("zero mgr says to go to phase %d, but we only have %d ivals.  forcing curPhase to %d" % (curPhase, len(self.phaseIvals), curPhase))
            result = curPhase        
        return result
                
    def exit(self):
        """Stop showing the prop."""
        assert self.notify.debugStateCall(self)
        self.okToStartNextAnim = False
        self.ignore("%sZeroPhase" % self.propString)
        self.ignore("%sZeroIsRunning" % self.propString)
        GenericAnimatedProp.GenericAnimatedProp.exit(self)
        self.request('Off')

    def handleNewPhase(self, newPhase):
        """Handle the  zero manager telling us we're in a new phase."""
        assert self.notify.debugStateCall(self)
        self.startIfNeeded()
                

    def handleNewIsRunning(self, isRunning):
        """Handle the  zero manager telling us we're in a new phase."""
        assert self.notify.debugStateCall(self)
        if isRunning:
            self.startIfNeeded()
        else:
            self.request('Off')
        
        
