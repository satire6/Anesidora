"""
ToonTown ObjectHandler
"""
from pandac.PandaModules import *

from direct.actor import Actor
from direct.leveleditor import ObjectGlobals as OG

from SuitPointObj import *
from GroupObj import *
from PropObj import *
from LandmarkObj import *
from FlatBuildingObj import *
from AnimBuildingObj import *
from AnimPropObj import *
from InteractivePropObj import *
from StreetObj import *

class ObjectHandler:
    """ ObjectHandler will create and update objects """
    
    def __init__(self, editor):
        self.editor = editor

    def createGroup(self, name=None):
        if name is None:
            groupName = 'group_' + `self.editor.getGroupNum()`
            self.editor.setGroupNum(self.editor.getGroupNum() + 1)
        else:
            groupName = name
        return GroupObj(self.editor, groupName)

    def createVisGroup(self, name=None):
        if name is None:
            groupName = 'VisGroup_' + `self.editor.getGroupNum()`
            self.editor.setGroupNum(self.editor.getGroupNum() + 1)
        else:
            groupName = name
        visGroupObj = VisGroupObj(self.editor, groupName)
        visGroupObj.dna.addVisible(groupName)
        return visGroupObj

    def createNode(self, name=None):
        if name is None:
            groupName = 'node_' + `self.editor.getGroupNum()`
            self.editor.setGroupNum(self.editor.getGroupNum() + 1)
        else:
            groupName = name
        return NodeObj(self.editor, groupName)

    def createProp(self, propType, name=None):
        return PropObj(self.editor, propType, nameStr=name)

    def createStreet(self, streetType):
        return StreetObj(self.editor, streetType)

    def createLandmark(self, landmarkType):
        return LandmarkObj(self.editor, landmarkType)

    def createFlatBuilding(self, buildingType):
        return FlatBuildingObj(self.editor, buildingType)

    def createAnimBuilding(self, animBuildingType):
        return AnimBuildingObj(self.editor, animBuildingType)

    def createAnimProp(self, animPropType):
        return AnimPropObj(self.editor, animPropType)

    def createInteractiveProp(self, interactivePropType):
        return InteractivePropObj(self.editor, interactivePropType)

    def createSys(self):
        return hidden.attachNewNode('SuitPoints')

    def createSuitPathPoint(self):
        suitPointObj = SuitPointObj(self.editor)
        return suitPointObj

    def updateSpecialBuildingType(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.dna.setBuildingType(val)
        if val in ['hq', 'kartshop']:
            DNARemoveChildOfClass(objNP.dna, DNA_DOOR)
            objNP.replace()

    def updateTitle(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.dna.setTitle(val)        

    def updateFlatBuildingWidth(self, val, obj, no_loading):
        objNP = obj[OG.OBJ_NP]
        objNP.dna.setWidth(float(val))
        objNP.replace(no_loading)

    def updateAnimPropAnim(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.dna.setAnim(val)
        objNP.animPropObj.exit()
        objNP.animPropObj.node.loadAnims({'anim':"%s/%s"%(objNP.animPropObj.path,val)})
        objNP.animPropObj.enter()        

    def updateSuitPointIndex(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        pointPos = objNP.spDna.getPos()
        pointType = objNP.spDna.getPointType()
        lbIndex = objNP.spDna.getLandmarkBuildingIndex()
        DNASTORE.removeSuitPoint(objNP.spDna)
        objNP.spDna = DNASuitPoint(val, pointType, pointPos, lbIndex)
        DNASTORE.storeSuitPoint(objNP.spDna)

    def updateSuitPointLbIndex(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.spDna.setLandmarkBuildingIndex(val)

    def updateSuitPointType(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.setPointType(eval('DNASuitPoint.%s'%val))
