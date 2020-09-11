from toontown.toonbase.ToontownGlobals import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
import BasicEntities
from toontown.suit import GoonPathData

class PathEntity(BasicEntities.NodePathEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory('PathEntity')
    def __init__(self, level, entId):
        self.pathScale = 1.
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.setPathIndex(self.pathIndex)
            
    def destroy(self):
        BasicEntities.NodePathEntity.destroy(self)

    def setPathIndex(self, pathIndex):
        self.pathIndex = pathIndex
        pathTableId = GoonPathData.taskZoneId2pathId[self.level.getTaskZoneId()]
        if self.pathIndex in GoonPathData.Paths[pathTableId]:
            self.path = GoonPathData.Paths[pathTableId][self.pathIndex]
            if __dev__:
                messenger.send(self.getChangeEvent())
        else:
            PathEntity.notify.warning('invalid pathIndex: %s' % pathIndex)
            self.path = None
    
    def makePathTrack(self, node, velocity, name, turnTime=1,
                      lookAroundNode=None):
        track = Sequence(name = name)
        if self.path is None:
            track.append(WaitInterval(1.))
            return track
        assert len(self.path) > 1

        # end with the starting point at the end, so we have a continuous loop
        path = self.path + [self.path[0]]
        for pointIndex in range(len(path) - 1):
            startPoint = Point3(path[pointIndex]) * self.pathScale
            endPoint = Point3(path[pointIndex + 1]) * self.pathScale
            # Face the endpoint
            v = startPoint - endPoint

            # figure out the angle we have to turn to look at the next point
            # Note: this will only look right for paths that are defined in a
            # counterclockwise order.  Otherwise the goon will always turn the
            # "long" way to look at the next point
            node.setPos(startPoint[0], startPoint[1],startPoint[2])
            node.headsUp(endPoint[0], endPoint[1], endPoint[2])
            theta = node.getH() % 360
                              
            track.append(
                LerpHprInterval(node, # stop and look around
                                turnTime,
                                Vec3(theta,0,0)))
            
            # Calculate the amount of time we should spend walking
            distance = Vec3(v).length()
            duration = distance / velocity
            
            # Walk to the end point
            track.append(
                LerpPosInterval(node, duration=duration,
                                pos=endPoint, startPos=startPoint))
        return track

    if __dev__:
        def getChangeEvent(self):
            return self.getUniqueName('pathChanged')

        def setPathScale(self, pathScale):
            self.pathScale = pathScale
            self.setPathIndex(self.pathIndex)
