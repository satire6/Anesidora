from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from toontown.battle.BattleProps import globalPropPool
from direct.directnotify import DirectNotifyGlobal

SFX = PythonUtil.Enum( 'poof, magic' )

SFXPATHS = {
    SFX.poof:'phase_4/audio/sfx/firework_distance_02.mp3',
    SFX.magic:'phase_4/audio/sfx/SZ_DD_treasure.mp3',
    }

class DustCloud(NodePath):
    dustCloudCount = 0
    sounds = {}
        
    notify = DirectNotifyGlobal.directNotify.newCategory("DustCloud")
    
    def __init__(self, parent = hidden, fBillboard = 1, wantSound = 0):
        """__init()"""
        # Initialize the superclass
        NodePath.__init__(self)
        # Make yourself a copy of the dustCloud texture flip
        self.assign(globalPropPool.getProp('suit_explosion_dust'))
        if fBillboard:
            self.setBillboardAxis()
        self.reparentTo(parent)
        # Init sequence node
        self.seqNode = self.find('**/+SequenceNode').node()
        self.seqNode.setFrameRate(0)
        # if we want sounds for this effect, import them
        # we should only use this if we're sure we're in phase_4 already
        self.wantSound = wantSound
        if self.wantSound and not DustCloud.sounds:
            DustCloud.sounds[SFX.poof] = loader.loadSfx(SFXPATHS[SFX.poof])
            #DustCloud.sounds[SFX.magic] = loader.loadSfx(SFXPATHS[SFX.magic])
        # This will hold an interval to play back the tflip
        self.track = None
        self.trackId = DustCloud.dustCloudCount
        # Increment instance counter
        DustCloud.dustCloudCount += 1
        self.setBin('fixed', 100, 1)
        self.hide()

    def createTrack(self, rate = 24):
        def getSoundFuncIfAble(soundId):
            sound = DustCloud.sounds.get(soundId)
            if self.wantSound and sound:
                return sound.play
            else:
                def dummy():
                    pass
                return dummy
        # Compute tflip duration
        tflipDuration = (self.seqNode.getNumChildren()/(float(rate)))
        # Create new track of proper duration
        self.track = Sequence(
            Func(self.show),
            Func(self.messaging),
            Func(self.seqNode.play, 0, self.seqNode.getNumFrames() - 1),
            Func(self.seqNode.setFrameRate,rate),
            Func(getSoundFuncIfAble(SFX.poof)),
            Wait(tflipDuration),
            #Func(getSoundFuncIfAble(SFX.magic)),
            Func(self.seqNode.setFrameRate, 0),
            Func(self.hide),
            name = 'dustCloud-track-%d' % self.trackId,
            )
            
            
    def messaging(self):
        self.notify.debug("CREATING TRACK ID: %s" %self.trackId)
    
    def play(self, rate = 24):
        # Stop existing track, if one exists
        self.stop()
        # Create new track
        self.createTrack(rate)
        # Start track
        self.track.start()
    
    def loop(self, rate = 24):
        # Stop existing track, if one exists
        self.stop()
        # Create new track
        self.createTrack(rate)
        # Start track
        self.track.loop()
    
    def stop(self):
        if self.track:
            self.track.finish()
    
    def destroy(self):
        self.notify.debug("DESTROYING TRACK ID: %s" %self.trackId)
        self.stop()
        del self.track
        del self.seqNode
        self.removeNode()
