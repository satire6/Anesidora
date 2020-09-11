from pandac.PandaModules import *

class SuitPointObj(NodePath):
    def __init__(self, editor, dna=None):
        NodePath.__init__(self)
        self.editor = editor

        if dna:
            self.spDna = dna
        else:
            self.spDna = DNASTORE.storeSuitPoint(0, Point3(0))

        np = loader.loadModel('models/misc/sphere')
        # need to rename geomnode since 'Sphere' is defined as unpickable
        np.find("**/+GeomNode").setName('SuitPointSphere')
        self.assign(np)

    def setPos(self, newPos):
        NodePath.setPos(self, newPos)
        self.spDna.setPos(newPos)

    def setPointType(self, type):
        self.spDna.setPointType(type)
        marker = self.find("SuitPointSphere")
        if (type == DNASuitPoint.STREETPOINT):
            marker.setColor(0, 0, 0.6)
            marker.setScale(0.4)
        elif (type == DNASuitPoint.FRONTDOORPOINT):
            marker.setColor(0, 0, 1)
            marker.setScale(0.5)
        elif (type == DNASuitPoint.SIDEDOORPOINT):
            marker.setColor(0, 0.6, 0.2)
            marker.setScale(0.5)
        else:
            marker.setColor(1,1,1)
            marker.setScale(1)
