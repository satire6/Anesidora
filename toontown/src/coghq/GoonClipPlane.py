from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.level import BasicEntities

class GoonClipPlane(BasicEntities.NodePathEntity):

    def __init__(self, level, entId):
        BasicEntities.NodePathEntity.__init__(self, level, entId)
        self.zoneNum = self.getZoneEntity().getZoneNum()
        self.initPlane()
        self.registerWithFactory()

    def destroy(self):
        self.unregisterWithFactory()
        BasicEntities.NodePathEntity.destroy(self)
        self.removeNode()

    def registerWithFactory(self):
        # register this clip plane with the factory
        clipList = self.level.goonClipPlanes.get(self.zoneNum)
        if clipList:
            if not self.entId in clipList:
                clipList.append(self.entId)
        else:
            self.level.goonClipPlanes[self.zoneNum]= [self.entId]
            
    def unregisterWithFactory(self):
        # unregister this clip plane with the factory
        clipList = self.level.goonClipPlanes.get(self.zoneNum)
        if clipList:
            if self.entId in clipList:
                clipList.remove(self.entId)
        
    def initPlane(self):
        # Graphical debugging
        if __debug__:
            plane = loader.loadModel("phase_5/models/modules/suit_walls.bam")
            plane.reparentTo(self)
            plane.setH(90)

        # Setup clip plane
        self.coneClip = PlaneNode('coneClip')
        self.coneClip.setPlane(Plane(Vec3(1,0,0), Point3(0,0,0)))
        self.coneClipPath = self.attachNewNode(self.coneClip)

    def getPlane(self):
        return self.coneClipPath

         
            
        
        
    
