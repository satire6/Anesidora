import AnimatedProp
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.hood import ZoneUtil
from toontown.hood import HoodUtil

class GenericAnimatedProp(AnimatedProp.AnimatedProp):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'GenericAnimatedProp')

    AnimsUsingWav = [] # which anims use wav files
    
    def __init__(self, node):
        AnimatedProp.AnimatedProp.__init__(self, node)
        self.origAnimNameToSound = {}
        # [gjeon] to find path from code
        code = node.getTag('DNACode')
        if code.startswith('interactive_prop_'):
            pathStr = code[len('interactive_prop_'):].split('__')[0]
        elif code.startswith('animated_prop_generic_'):
            pathStr = code[len('animated_prop_generic_'):].split('__')[0]
        elif code.startswith('animated_prop_'):
            # we expect generic to be replaced with the class name
            tempStr = code[len('animated_prop_'):]
            nextUnderscore = tempStr.find('_')
            finalStr = tempStr[nextUnderscore+1:]                           
            pathStr = finalStr.split('__')[0]
        elif code.startswith('animated_building_'):
            pathStr = code[len('animated_building_'):].split('__')[0]            
        phaseDelimeter = len('phase_') + pathStr[len('phase_'):].find('_')
        phaseStr = pathStr[:phaseDelimeter]
        pathTokens = pathStr[phaseDelimeter+1:].split('_')
        self.path = phaseStr
        for path in pathTokens:
            self.path += '/'
            self.path += path
        self.notify.debug("self.path=%s" % self.path)
        self.calcHoodId(node)
        self.propType = HoodUtil.calcPropType(node)
        self.setupActor(node)        
        self.code = code

    def delete(self):
        AnimatedProp.AnimatedProp.delete(self)
        self.node.cleanup()
        del self.node
        del self.trashcan
   
    def enter(self):
        self.node.postFlatten()
        AnimatedProp.AnimatedProp.enter(self)
        doAnimLoop=True
        try:
            # we need this try for level editor
            if type(self).__name__=='instance':
                if self.__class__.__name__=='GenericAnimatedProp':
                    #import pdb; pdb.set_trace()
                    # ok we don't have a subclass
                    if base.cr.newsManager.isHolidayRunning(ToontownGlobals.HYDRANTS_BUFF_BATTLES):
                        doAnimLoop = True
                    else:
                        doAnimLoop = False
        except:
            pass
        if doAnimLoop:
            self.node.loop('anim')

    def exit(self):
        AnimatedProp.AnimatedProp.exit(self)
        self.node.stop()
    
    def getActor(self):
        """Return the actor node."""
        return self.node

    def setupActor(self, node):
        """Setup the animation/s for our actor."""
        assert self.notify.debugStateCall(self)        
        anim = node.getTag('DNAAnim')
        self.trashcan = Actor.Actor(node, copy = 0)
        self.trashcan.reparentTo(node)
        self.trashcan.loadAnims({'anim' : "%s/%s"%(self.path,anim)})
        self.trashcan.pose('anim', 0)
        self.node = self.trashcan


    def calcHoodId(self,node):
        """Calculated our hoodId based on the node full path."""
        self.hoodId = ToontownGlobals.ToontownCentral
        fullString = str(node)
        splits = fullString.split('/')
        try:            
            visId = int(splits[2])
            self.visId = visId
            self.hoodId = ZoneUtil.getCanonicalHoodId(visId)
            self.notify.debug("calcHoodId %d from %s" % (self.hoodId,fullString))
        except Exception, generic:
            if  not ('Editor' in fullString):
                self.notify.warning("calcHoodId couldn't parse %s using 0" % fullString)
            self.hoodId = 0
            self.visId =0


    def createSoundInterval(self, origAnimNameWithPath, maximumDuration):
        """Return a sound interval for the appropriate animation.

        origAnimName must be an animation entry in self.phaseInfo.
        """
        if not hasattr(base,'localAvatar'):
            # we are in level editor
            return Sequence()
            
        sfxVolume = 1.0
        cutoff = 45
        # lets figure out the correct path
        if not hasattr(self, 'soundPath'):
            self.soundPath = self.path.replace('/models/char', '/audio/sfx')
        origAnimName = origAnimNameWithPath.split('/')[-1] # just get the filename
        theSound = self.origAnimNameToSound.get(origAnimName)
        if not theSound:
            soundfile = origAnimName.replace('tt_a_ara', 'tt_s_ara')
            fullPath = self.soundPath + '/' + soundfile
            if origAnimName in self.AnimsUsingWav:
                theSound = loader.loadSfx(fullPath + '.wav')
            else:
                theSound = loader.loadSfx(fullPath + '.mp3')
            self.origAnimNameToSound[origAnimName]=theSound
        if theSound:
            soundDur = theSound.length()
            if maximumDuration  < soundDur :
                if base.config.GetBool("interactive-prop-info", False):
                    # punt on tt_s_ara_dga_hydrant_idleIntoFight ,
                    # engine is reporting it as 1 seconds when it's at 0.625
                    if self.visId == localAvatar.zoneId and \
                       origAnimName != "tt_a_ara_dga_hydrant_idleIntoFight":
                        self.notify.warning("anim %s had duration of %s while sound  has duration of %s" %(
                            origAnimName, maximumDuration , soundDur ))
                soundDur = maximumDuration
            result = SoundInterval(theSound,
                                   node=self.node,
                                   listenerNode = base.localAvatar,
                                   volume = sfxVolume,
                                   cutOff = cutoff,
                                   startTime = 0,
                                   duration = soundDur)
        else:
            # just return an empty sequence
            result = Sequence()
        return result
