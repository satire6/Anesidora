from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleProps import globalPropPool


class Wake(NodePath):
    wakeCount = 0
    def __init__(self, parent = hidden, target = hidden):
        """
        __init(parent, target)
        parent is the render frame in which the ripples are drawn
        target is the node path which determines the ripples' positions
        """
        # Initialize the superclass
        NodePath.__init__(self)
        # Create a container node to hold ripple sequences
        self.assign(parent.attachNewNode('wake'))
        # Record the target node path
        self.target = target
        # Get a copy of the ripples sequence
        self.ripples = globalPropPool.getProp('ripples')
        # Move the master tflip slightly above origin to avoid coincident polys
        tformNode = self.ripples.getChild(0)
        tformNode.setZ(0.01)
        self.seqNodePath = self.ripples.find('**/+SequenceNode')
        self.seqNode = self.seqNodePath.node()
        # Used to specify sort order of ripples within the fixed bin
        self.sortBase = 10
        self.rippleCount = 0
        self.doLaters = [None] * 20
        self.trackId = Wake.wakeCount
        # Increment instance counter
        Wake.wakeCount += 1
    
    def createRipple(self, zPos, rate = 1.0, startFrame = 0):
        # Make a copy of the master tflip, inheriting its xform and rate
        ripple = self.ripples.copyTo(self)
        # Move it to the target
        ripple.iPos(self.target)
        ripple.setZ(render,zPos + self.rippleCount * 0.001)
        # Adjust visibility
        ripple.setBin('fixed', self.sortBase + self.rippleCount, 1)
        # Find sequence node
        seqNode = ripple.find('**/+SequenceNode').node()
        # Adjust play rate
        seqNode.setPlayRate(rate)
        # Set ripple's visible child to startFrame
        seqNode.play(startFrame, seqNode.getNumFrames() - 1)
        # Compute duration
        duration = (24 - startFrame)/24.0
        # Add doLater to get rid of this ripple when done
        # The task only removes do later from local list
        def clearDoLaterList(rippleCount):
            # Remove doLater from local list
            self.doLaters[rippleCount] = None
        # The real work is done by the upon death
        # This is so you can kill the task prematurely and stil
        # get the work done
        def destroyRipple(task):
            ripple.removeNode()
        t = taskMgr.doMethodLater(duration,
                                  clearDoLaterList,
                                  ('wake-%d-destroy-%d' % (self.trackId, self.rippleCount)),
                                  extraArgs = (self.rippleCount,),
                                  uponDeath = destroyRipple)
        self.doLaters[self.rippleCount] = t
        self.rippleCount = (self.rippleCount + 1) % 20

    def stop(self):
        # Clean out any pending do laters
        for i in range(len(self.doLaters)):
            if self.doLaters[i]:
                taskMgr.remove(self.doLaters[i])
                self.doLaters[i] = None
        
    def destroy(self):
        self.stop()
        self.removeNode()
        self.ripples.removeNode()
        del self.target


class WakeSequence(NodePath):
    wakeCount = 0
    def __init__(self, parent = hidden):
        """__init()"""
        # Initialize the superclass
        NodePath.__init__(self)
        # Make yourself a copy of the wake texture flip
        self.assign(globalPropPool.getProp('wake'))
        self.reparentTo(parent)
        # Move the tflip slightly above origin to avoid coincident polys
        tformNode = self.getChild(0)
        tformNode.setZ(0.1)
        self.startNodePath = self.find('**/+SequenceNode')
        self.startSeqNode = self.startNodePath.node()
        self.startSeqNode.setName('start')
        self.startSeqNode.setPlayRate(0)
        # Create two more sequence Nodes to hold the different parts of
        # the effect (start, cycle, end)
        # cycle sequence
        self.cycleNodePath = NodePath(SequenceNode(0, 'cycle'))
        self.cycleNodePath.reparentTo(tformNode)
        self.cycleSeqNode = self.cycleNodePath.node()
        # end sequence
        self.endNodePath = NodePath(SequenceNode(0, 'end'))
        self.endNodePath.reparentTo(tformNode)
        self.endSeqNode = self.endNodePath.node()
        # Copy appropriate frames to the cycle and end sequence
        children = self.startNodePath.getChildren()
        for child in children[12:16]:
            child.reparentTo(self.cycleNodePath)
        for child in children[16:]:
            child.reparentTo(self.endNodePath)
        # This will hold an interval to play back the tflip
        self.tracks = []
        self.rate = None
        self.trackId = Wake.wakeCount
        # Increment instance counter
        Wake.wakeCount += 1
        self.setBin('fixed', 10, 1)
        self.hide()
    
    def createTracks(self, rate = 1):
        # Stop existing track, if one exists
        self.stop()
        # Clear out old tracks
        self.tracks = []
        # Start track
        # Compute tflip duration
        tflipDuration = (self.startSeqNode.getNumChildren()/(float(rate) * 24))
        # Create new track of proper duration
        startTrack = Sequence(
            Func(self.show),
            Func(self.showTrack, 0),
            Func(self.startSeqNode.play, 0, self.startSeqNode.getNumFrames() - 1),
            Func(self.startSeqNode.setPlayRate, rate),
            Wait(tflipDuration),
            Func(self.showTrack, 1),
            Func(self.startSeqNode.play, 0, self.startSeqNode.getNumFrames() - 1),
            Func(self.cycleSeqNode.setPlayRate, rate),
            name = 'start-wake-track-%d' % self.trackId
            )
        self.tracks.append(startTrack)
        # End track
        # Compute tflip duration
        tflipDuration = (self.endSeqNode.getNumChildren()/(float(rate) * 24))
        # Create new track of proper duration
        endTrack = Sequence(
            Func(self.showTrack, 2),
            Func(self.endSeqNode.play, 0, self.endSeqNode.getNumFrames() - 1),
            Func(self.endSeqNode.setPlayRate, rate),
            Wait(tflipDuration),
            Func(self.endSeqNode.setPlayRate, 0),
            Func(self.hide),
            name = 'end-wake-track-%d' % self.trackId
            )
        self.tracks.append(endTrack)
        # Record rate
        self.rate = rate

    def showTrack(self, trackId):
        if trackId == 0:
            self.startNodePath.show()
        else:
            self.startNodePath.hide()
        if trackId == 1:
            self.cycleNodePath.show()
        else:
            self.cycleNodePath.hide()
        if trackId == 2:
            self.endNodePath.show()
        else:
            self.endNodePath.hide()

    def play(self, trackId, rate = 1):
        # Create new track if necessary
        if self.rate != rate:
            self.createTracks(rate)
        # Start track
        self.tracks[trackId].start()
    
    def loop(self, trackId, rate = 1):
        # Create new track if necessary
        if self.rate != rate:
            self.createTracks(rate)
        # Start track
        self.tracks[trackId].loop()
    
    def stop(self):
        for track in self.tracks:
            track.finish()
    
    def destroy(self):
        self.stop()
        self.tracks = None
        self.removeNode()
