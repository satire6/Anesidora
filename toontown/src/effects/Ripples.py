from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import globalPropPool


class Ripples(NodePath):
    rippleCount = 0
    def __init__(self, parent = hidden):
        """__init()"""
        # Initialize the superclass
        NodePath.__init__(self)
        # Make yourself a copy of the ripples texture flip
        self.assign(globalPropPool.getProp('ripples'))
        self.reparentTo(parent)
        # Move the tflip slightly above origin to avoid coincident polys
        self.getChild(0).setZ(0.1)
        self.seqNode = self.find('**/+SequenceNode').node()
        self.seqNode.setPlayRate(0)
        # This will hold an interval to play back the tflip
        self.track = None
        self.trackId = Ripples.rippleCount
        # Increment instance counter
        Ripples.rippleCount += 1
        self.setBin('fixed', 100, 1)
        self.hide()

    def createTrack(self, rate = 1):
        # Compute tflip duration
        tflipDuration = (self.seqNode.getNumChildren()/(float(rate) * 24))
        # Create new track of proper duration
        self.track = Sequence(
            Func(self.show),
            Func(self.seqNode.play, 0, self.seqNode.getNumFrames() - 1),
            Func(self.seqNode.setPlayRate,rate),
            Wait(tflipDuration),
            Func(self.seqNode.setPlayRate, 0),
            Func(self.hide),
            name = 'ripples-track-%d' % self.trackId
            )
    
    def play(self, rate = 1):
        # Stop existing track, if one exists
        self.stop()
        # Create new track
        self.createTrack(rate)
        # Start track
        self.track.start()
    
    def loop(self, rate = 1):
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
        self.stop()
        self.track = None
        del self.seqNode
        self.removeNode()
