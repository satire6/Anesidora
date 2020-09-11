from direct.leveleditor.ObjectMgrBase import *
from LevelEditorGlobals import *

from SuitPointObj import *
from GroupObj import *
from PropObj import *
from LandmarkObj import *
from FlatBuildingObj import *
from AnimBuildingObj import *
from AnimPropObj import *
from InteractivePropObj import *
from StreetObj import *

class ObjectMgr(ObjectMgrBase):

    def __init__(self, editor):
        ObjectMgrBase.__init__(self, editor)

    def addNewObject(self, typeName, uid=None, model=None, parent=None, anim=None, fSelectObject=True, nodePath=None, nameStr=None):
        """ function to add new obj to the scene """
        if parent is None and typeName in ['SuitPath Point']:
            parent = self.editor.suitPointToplevel

        newobj = ObjectMgrBase.addNewObject(self, typeName, uid, model, parent, anim, fSelectObject, nodePath, nameStr)
        if newobj:
            obj = self.findObjectByNodePath(newobj)
            objProp = obj[OG.OBJ_PROP]
            if hasattr(newobj, 'dna'):
                objProp['_subDna'] = self.populateSubDna(newobj.dna)

                if isinstance(newobj, LandmarkObj):
                    objProp['Special Type'] = newobj.dna.getBuildingType()
                if isinstance(newobj, VisGroupObj):
                    objProp['_visList'] = newobj.getVisList()
                    objProp['_battleCellList'] = newobj.getBattleCellList()
                    objProp['_suitEdgeList'] = newobj.getSuitEdgeList()
        return newobj

    def populateDnaAttribs(self, dnaNode):
        attribList = []

        for attrib in ['Code', 'Height', 'WindowCount',
                       'Pos', 'Scale', 'Hpr', 'Color',
                       'Kern', 'Wiggle', 'Stumble', 'Stomp', 'Width', 'Flags', 'Indent',
                       'Letters']:
            if hasattr(dnaNode, 'set%s'%attrib):
                attribList.append(('set%s'%attrib, eval('dnaNode.get%s()'%attrib)))

        return attribList

    def populateSubDna(self, dnaNode):
        myList = []
        for i in range(dnaNode.getNumChildren()):
            dnaChild = dnaNode.at(i)
            classType = dnaChild.getClassType()
            if classType in SUB_DNAS:
                attribList = self.populateDnaAttribs(dnaChild)
                myChildren = self.populateSubDna(dnaChild)
                myList.append(['%s'%classType, attribList, myChildren])
        return myList

    def replaceBySubDna(self, dnaNode, subDnaList):
        if DNAClassEqual(dnaNode, DNA_FLAT_BUILDING):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_WALL, False)
        elif DNAClassEqual(dnaNode, DNA_WALL):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_WINDOWS, False)
            DNARemoveAllChildrenOfClass(dnaNode, DNA_CORNICE, False)
            DNARemoveAllChildrenOfClass(dnaNode, DNA_FLAT_DOOR, False)
        elif DNAClassEqual(dnaNode, DNA_SIGN):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_SIGN_BASELINE, False)
        elif DNAClassEqual(dnaNode, DNA_SIGN_BASELINE):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_SIGN_TEXT, False)            
            DNARemoveAllChildrenOfClass(dnaNode, DNA_SIGN_GRAPHIC, False)
        elif DNAClassEqual(dnaNode, DNA_LANDMARK_BUILDING) or\
             DNAClassEqual(dnaNode, DNA_ANIM_BUILDING):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_DOOR, False)
            DNARemoveAllChildrenOfClass(dnaNode, DNA_SIGN, False)
        elif DNAClassEqual(dnaNode, DNA_PROP):
            DNARemoveAllChildrenOfClass(dnaNode, DNA_SIGN, False)

        for subDna in subDnaList:
            newDNA = eval("%s()"%subDna[0])
            if newDNA:
                for dnaAttr in subDna[1]:
                    getattr(newDNA, dnaAttr[0])(dnaAttr[1])
                dnaNode.add(newDNA)
                self.replaceBySubDna(newDNA, subDna[2])
            
    def replace(self, parent):
        children = parent.getChildren()
        for child in children:
            if child.hasTag('OBJRoot'):
                obj = self.findObjectByNodePath(child)
                if obj:
                    objNP = obj[OG.OBJ_NP]
                    objProp = obj[OG.OBJ_PROP]

                    # update object's DNA from objProp['_subDna']
                    subDna = objProp.get('_subDna')
                    if subDna:
                        self.replaceBySubDna(objNP.dna, subDna)
                        if hasattr(objNP, 'replace'):
                            objNP.replace(populateSubDna = False)

                    if isinstance(objNP, VisGroupObj):
                        # update visGroup DNA's visList from objProp['_visList']
                        visList = objProp.get('_visList')
                        if visList:
                            for vis in visList:
                                objNP.addVisible2DNA(vis)

                        # update visGroup DNA's battleCellList from objProp['_battleCellList']
                        battleCellList = objProp.get('_battleCellList')
                        if battleCellList:
                            for battleCell in battleCellList:
                                objNP.addBattleCell2DNA(battleCell)

                        # update visGroup DNA's suitEdgeList from objProp['_suitEdgeList']
                        suitEdgeList = objProp.get('_suitEdgeList')
                        if suitEdgeList:
                            for suitEdge in suitEdgeList:
                                objNP.addSuitEdge2DNA(suitEdge)
                                
                    self.replace(objNP)

    def populateObject(self, dnaNode, objType, objClass, parent):
        try:
            nodePath = NodePath(DNASTORE.findPandaNode(dnaNode))
        except:
            print "Can't find Panda Node", dnaNode, parent
            return parent

        if DNAClassEqual(dnaNode, DNA_PROP):
            newNP = objClass(self.editor, objType, dnaNode, nodePath, dnaNode.getName())
        else:
            newNP = objClass(self.editor, objType, dnaNode, nodePath)
        newParent = self.addNewObject(objType,
                                      parent=parent,
                                      fSelectObject = False,
                                      nodePath=newNP)
        if newParent:
            # updating object prop from dna attrib
            obj = self.findObjectByNodePath(newParent)
            objDef = obj[OG.OBJ_DEF]
            objProp = obj[OG.OBJ_PROP]
            for propName in objDef.dnaProperties.keys():
                propDef = objDef.properties[propName]
                propDataType = propDef[OG.PROP_DATATYPE]
                val = getattr(dnaNode, objDef.dnaProperties[propName])()
                objProp[propName] = OG.TYPE_CONV[propDataType](val)

        return newParent

    def populateObjects(self, dnaNode, dnaParent, parent):
        objType = None
        if DNAClassEqual(dnaNode, DNA_GROUP):
            objClass = GroupObj
            objType = '__group__'
        elif DNAClassEqual(dnaNode, DNA_VIS_GROUP):
            objClass = VisGroupObj
            objType = '__vis_group__'
        elif DNAClassEqual(dnaNode, DNA_NODE):
            objClass = NodeObj
            objType = '__node__'
        elif DNAClassEqual(dnaNode, DNA_FLAT_BUILDING):
            objClass = FlatBuildingObj
            name = dnaNode.getName()
            index = name.find(':')
            if index < 0:
                print 'Wrong flat building DNA', name
##                 if dnaNode.getNumChildren() == 0:
##                     dnaParent.remove(dnaNode)
            else:
                typeName = name[index+1:].split('_DNARoot')[0]
                if typeName == 'random':
                    typeName = "%s%d"%(typeName, int(dnaNode.getCurrentWallHeight()))
                objType = self.editor.currHoodId + '_' + typeName
        elif DNAClassEqual(dnaNode, DNA_LANDMARK_BUILDING):
            objClass = LandmarkObj
            objType = dnaNode.getCode()
##             name = dnaNode.getName()
##             index = name.find('toon_landmark')
##             if index < 0:
##                 print 'Wrong landmark building DNA', name
## ##                 if dnaNode.getNumChildren() == 0:
## ##                     dnaParent.remove(dnaNode)
##             else:
##                 objType = name[index:].split('_DNARoot')[0]
        elif DNAClassEqual(dnaNode, DNA_ANIM_BUILDING):
            objClass = AnimBuildingObj
            objType = dnaNode.getCode()
            #objType = dnaNode.getName().split('_DNARoot')[0]
        elif DNAClassEqual(dnaNode, DNA_PROP):
            objClass = PropObj
            objType = dnaNode.getCode()
            #objType = dnaNode.getName().split('_DNARoot')[0]
        elif DNAClassEqual(dnaNode, DNA_ANIM_PROP):
            objClass = AnimPropObj
            objType = dnaNode.getCode()
            #objType = dnaNode.getName().split('_DNARoot')[0]
        elif DNAClassEqual(dnaNode, DNA_INTERACTIVE_PROP):
            objClass = InteractivePropObj
            objType = dnaNode.getCode()
            #objType = dnaNode.getName().split('_DNARoot')[0]
        elif DNAClassEqual(dnaNode, DNA_STREET):
            objClass = StreetObj
            #name = dnaNode.getName().split('_DNARoot')[0]
            name = dnaNode.getCode()
            if name.endswith('_pond'):
                objType = name[len('street_'):]
            else:
                objType = self.editor.currHoodId + '_' + name[len('street_'):]

        if objType:
            newParent = self.populateObject(dnaNode, objType, objClass, parent)
        else:
            newParent = parent

        dnaChildren = []
        for i in range(dnaNode.getNumChildren()):
            dnaChildren.append(dnaNode.at(i))

        for dnaChild in dnaChildren:
            self.populateObjects(dnaChild, dnaNode, newParent)

    def createObjects(self, dnaNode, parent):
        for i in range(dnaNode.getNumChildren()):
            dnaChild = dnaNode.at(i)
            self.populateObjects(dnaChild, dnaNode, parent)

    def getPreSaveData(self):
        self.editor.suitPointToplevel.reparentTo(hidden)
        self.traverse(hidden)
##         # to save suit path points
##         numPoints = DNASTORE.getNumSuitPoints()
##         if numPoints > 0:
##             self.saveData.append("\nif hasattr(objectMgr, 'addSuitPoint'):")
##             for i in range(numPoints):
##                 point = DNASTORE.getSuitPointAtIndex(i)
##                 lbIndex = point.getLandmarkBuildingIndex()
##                 if lbIndex >= 0:
##                     self.saveData.append("    objectMgr.addSuitPoint(%d, %d, %s, %d)"%(point.getIndex(), point.getPointType(), point.getPos(), lbIndex))
##                 else:
##                     self.saveData.append("    objectMgr.addSuitPoint(%d, %d, %s)"%(point.getIndex(), point.getPointType(), point.getPos()))

    def getPostSaveData(self):
        self.editor.suitPointToplevel.reparentTo(render)

    def populateSuitPoints(self):
        # Points
        numPoints = DNASTORE.getNumSuitPoints()
        for i in range(numPoints):
            point = DNASTORE.getSuitPointAtIndex(i)
            suitPointObj = SuitPointObj(self.editor, point)
            newobj = self.addNewObject('SuitPath Point', fSelectObject=False, nodePath=suitPointObj)
            obj = self.findObjectByNodePath(newobj)
            objNP = obj[OG.OBJ_NP]
            objProp = obj[OG.OBJ_PROP]

            objNP.setPos(point.getPos())
            objNP.setPointType(point.getPointType())
            objProp['index'] = point.getIndex()
            objProp['lbIndex'] = point.getLandmarkBuildingIndex()
            # update pointType string value
            objProp['pointType'] = obj[OG.OBJ_DEF].properties['pointType'][OG.PROP_RANGE][point.getPointType()]
            
    def removeObjectByNodePath(self, nodePath):
        obj = self.findObjectByNodePath(nodePath)
        if obj:
            objNP = obj[OG.OBJ_NP]
            if hasattr(objNP, 'removeDNA'):
                objNP.removeDNA()
        ObjectMgrBase.removeObjectByNodePath(self, nodePath)
