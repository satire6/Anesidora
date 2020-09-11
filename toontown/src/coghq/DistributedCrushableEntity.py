from otp.level import DistributedEntity
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NodePath
from otp.level import BasicEntities

class DistributedCrushableEntity(DistributedEntity.DistributedEntity,
                                 NodePath, BasicEntities.NodePathAttribs):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedCrushableEntity')

    def __init__(self, cr):
        DistributedEntity.DistributedEntity.__init__(self, cr)
        node = hidden.attachNewNode('DistributedNodePathEntity')
        # don't call NodePath constructor here so we don't have
        # collisions with Actor's nodepath inheritance

    def initNodePath(self):
        # call this in the __init__ of any derived class that
        # doesn't already derive from NodePath
        node = hidden.attachNewNode('DistributedNodePathEntity')
        NodePath.__init__(self, node)
    
    def announceGenerate(self):
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathAttribs.initNodePathAttribs(self)
        # inheritors should make sure to reparent geom to something under render
        
    def disable(self):
        self.reparentTo(hidden)
        BasicEntities.NodePathAttribs.destroy(self)
        DistributedEntity.DistributedEntity.disable(self)

    def delete(self):
        self.removeNode()
        DistributedEntity.DistributedEntity.delete(self)

    def setPosition(self, x, y, z):
         self.setPos(x,y,z)

    def setCrushed(self, crusherId, axis):
        assert(self.notify.debug("setCrushed, axis = %s" % axis))
        # we have been crushed along the given axis, play
        # crush movie
        self.playCrushMovie(crusherId, axis)

    def playCrushMovie(self, crusherId, axis):
        # Derived classes should do something pretty here,
        # such as scaling the object along the axis, or playing
        # a crush animation
        return


    
