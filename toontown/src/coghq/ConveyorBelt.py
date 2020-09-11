"""ConveyorBelt module: contains the ConveyorBelt class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import MovingPlatform
from otp.level import BasicEntities

# TODO: fix cracks between treads

class ConveyorBelt(BasicEntities.NodePathEntity):
    """
    Conveyer belt is made up of a series of contiguous MovingPlatforms,
    called 'treads'. Belt extends in +Y. You must provide a tread model
    and the length of that tread model in Y. Model should have floor poly
    that starts at Y=0 and extends to Y=treadLength. Model should match up
    with itself; two tread models aligned in X and Z and separated by
    treadLength in Y should fit together seamlessly.

    ConveyerBelt will calculate how many treads are needed to cover 'length'
    feet of belt, and instantiate that many MovingPlatforms using the
    provided tread model. Treads are then moved forward in +Y at 'speed'.
    There is an extra tread created to sit behind Y=0; this extra tread
    fills in the beginning of the belt as the last tread slides past the end.
    Once the belt has moved treadLength feet, last tread is placed at the
    beginning, and so on.

    To avoid popping localToon back to the beginning of the belt, last tread
    explicitly dumps localToon just before popping back to the beginning.
    """
    UseClipPlanes = 1

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)

        self.initBelt()
        
    def destroy(self):
        self.destroyBelt()
        BasicEntities.NodePathEntity.destroy(self)

    def initBelt(self):
        treadModel = loader.loadModel(self.treadModelPath)
        treadModel.setSx(self.widthScale)
        treadModel.flattenLight()
        
        # add one to cover the full belt length, one to compensate for
        # the tread's origin placement, then one more to cover a tread's
        # length of movement
        self.numTreads = int(self.length/self.treadLength) + 3

        self.beltNode = self.attachNewNode('belt')

        # make copies of the tread model
        self.treads = []
        for i in xrange(self.numTreads):
            mp = MovingPlatform.MovingPlatform()
            mp.parentingNode = render.attachNewNode('parentTarget')
            mp.setupCopyModel('conv%s-%s' % (self.getParentToken(), i),
                              treadModel, self.floorName,
                              parentingNode=mp.parentingNode)
            # we can't attach the parenting node until we've called
            # setupCopyModel
            mp.parentingNode.reparentTo(mp)
            mp.reparentTo(self.beltNode)
            self.treads.append(mp)

        self.start()

    def destroyBelt(self):
        self.stop()
        for tread in self.treads:
            tread.destroy()
            tread.parentingNode.removeNode()
            del tread.parentingNode
        del self.treads
        self.beltNode.removeNode()

        del self.beltNode
            
    def start(self):
        startTime = self.level.startTime
        treadsIval = Parallel(name='treads')
        treadPeriod = self.treadLength / abs(self.speed)
        # the first tread should start fully behind the origin
        startY = -self.treadLength
        for i in xrange(self.numTreads):
            # one lerp will bring this tread to the end
            # another will bring it from the beginning to its starting point
            periodsToEnd = self.numTreads - i
            periodsFromStart = self.numTreads - periodsToEnd
            ival = Sequence()
            if periodsToEnd != 0:
                ival.append(LerpPosInterval(
                    self.treads[i], duration=treadPeriod*periodsToEnd,
                    pos=Point3(0,startY+self.numTreads*self.treadLength,0),
                    startPos=Point3(0,startY+i*self.treadLength,0),
                    fluid = 1,
                    ))
            def dumpContents(tread=self.treads[i]):
                # wrtReparent everything to render
                # shouldn't have to do this, but it's better to
                # be safe -- having a toon pop back to the start
                # of the belt would look really bad.
                # There should be ground covering up the start and
                # end of the conveyor belt that picks up the toon.
                tread.releaseLocalToon()
            ival.append(Sequence(
                Func(dumpContents),
                # now that we've dumped localToon, make SURE the tread
                # goes away so he can't get back on
                Func(self.treads[i].setPos,
                     Point3(0,startY+self.numTreads*self.treadLength,0)),
                ))
            if periodsFromStart != 0:
                ival.append(LerpPosInterval(
                    self.treads[i], duration=treadPeriod*periodsFromStart,
                    pos=Point3(0,startY+i*self.treadLength,0),
                    startPos=Point3(0,startY,0),
                    fluid = 1,
                    ))
            treadsIval.append(ival)

        self.beltIval = Sequence(treadsIval,
                                 name='ConveyorBelt-%s' % self.entId,
                                 )
        playRate = 1.
        startT = 0.
        endT = self.beltIval.getDuration()
        if self.speed < 0.:
            playRate = -1.
            temp = startT
            startT = endT
            endT = temp
        self.beltIval.loop(playRate=playRate)
        self.beltIval.setT(globalClock.getFrameTime() - startTime)

        if ConveyorBelt.UseClipPlanes:
            # add some clip planes to get rid of the tread parts that poke out
            # of the start and end of the belt
            headClip = PlaneNode('headClip')
            tailClip = PlaneNode('tailClip')

            self.headClipPath = self.beltNode.attachNewNode(headClip)
            self.headClipPath.setP(-90)
            self.tailClipPath = self.beltNode.attachNewNode(tailClip)
            self.tailClipPath.setY(self.length)
            self.tailClipPath.setP(90)

            self.beltNode.setClipPlane(self.headClipPath)
            self.beltNode.setClipPlane(self.tailClipPath)

            # don't clip things that are parented to the treads
            for tread in self.treads:
                tread.parentingNode.setClipPlaneOff(self.headClipPath)
                tread.parentingNode.setClipPlaneOff(self.tailClipPath)

    def stop(self):
        if hasattr(self, 'beltIval'):
            self.beltIval.pause()
            del self.beltIval

        if ConveyorBelt.UseClipPlanes:
            # get rid of clip planes
            self.headClipPath.removeNode()
            del self.headClipPath
            self.tailClipPath.removeNode()
            del self.tailClipPath
            self.clearClipPlane()

            for tread in self.treads:
                tread.parentingNode.clearClipPlane()

    if __dev__:
        def attribChanged(self, attrib, value):
            self.destroyBelt()
            self.initBelt()

"""
import ConveyorBelt
from toontown.toonbase import ToontownGlobals
treadModel = loader.loadModel("phase_4/models/minigames/block")
treadModel.setSx(3.)
treadModel.setSz(.1)
cb = ConveyorBelt.ConveyorBelt(0, speed=ToontownGlobals.ToonForwardSpeed * .5,
                               length=80, treadModel=treadModel, treadLength=4)
cb.reparentTo(base.localAvatar)
cb.setPos(0,10,1)
cb.wrtReparentTo(render)
cb.start()
"""
