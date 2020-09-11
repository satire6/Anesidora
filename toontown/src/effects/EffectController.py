from pandac.PandaModules import *

class EffectController:
    
    particleDummy = None

    def __init__(self):        
        # Standard Intervals
        self.track = None
        self.startEffect = None
        self.endEffect = None

        # Standard Particle References
        self.f = None
        self.p0 = None
        
    def createTrack(self):
        # Define the interval parameters here
        pass

    def destroy(self):
        # Destroy & Cleanup Effect
        self.finish()
        if self.f:
            self.f.cleanup()
        self.f = None
        self.p0 = None
        self.removeNode()

    def cleanUpEffect(self):
        if self.f:
            self.setPosHpr(0,0,0,0,0,0)
            self.f.disable()
            self.detachNode()

    def reallyCleanUpEffect(self):
        self.cleanUpEffect()
        self.finish()
        

    #######################################
    # Single Playback
    #######################################
    
    def play(self, lod=None):
        # Create the Interval
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError, e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)
        else:
            self.createTrack()        
        # Play back track
        self.track.start()
        
    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        self.cleanUpEffect()
            
    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        
        
    #######################################
    # Continual Playback
    #######################################
    
    def startLoop(self, lod=None):
        # Create the Interval
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError, e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)
        else:
            self.createTrack()        
        # Play back track
        if self.startEffect:
            self.startEffect.start()
            
    def stopLoop(self):
        # Stop Playback
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect and not self.endEffect.isPlaying():
            self.endEffect.start()

    def getTrack(self):
        if not self.track:
            self.createTrack()
        return self.track

    def enableEffect(self):
        if self.f and self.particleDummy:
            self.f.start(self, self.particleDummy)
        elif self.f:
            self.f.start(self, self)

    def disableEffect(self):
        if self.f:
            self.f.disable()
