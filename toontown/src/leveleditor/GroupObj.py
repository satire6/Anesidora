"""
ToonTown Group object
"""

from ToonTownObj import *

class GroupObj(ToonTownObjBase):
    def __init__(self, editor, groupName, dna=None, nodePath=None):
        self.groupName = groupName
        ToonTownObjBase.__init__(self, editor, dna, nodePath)

    def initDNA(self):
        dnaNode = DNAGroup(self.groupName)
        return dnaNode

class VisGroupObj(GroupObj):
    def __init__(self, editor, groupName, dna=None, nodePath=None):
        GroupObj.__init__(self, editor, groupName,  dna, nodePath)

    def initDNA(self):
        dnaNode = DNAVisGroup(self.groupName)
        return dnaNode    

    def setName(self, newName):
        oldName = self.getName()
        self.dna.removeVisible(oldName)
        self.dna.addVisible(newName)
        GroupObj.setName(self, newName)

    def getVisList(self):
        result = []
        for i in range(self.dna.getNumVisibles()):
            result.append(self.dna.getVisibleName(i))

        return result

    def updateVisList(self):
        obj = self.editor.objectMgr.findObjectByNodePath(self)
        obj[OG.OBJ_PROP]['_visList'] = self.getVisList()

    def addVisible(self, visible):
        if visible not in self.getVisList():
            self.dna.addVisible(visible)
            self.updateVisList()

    def removeVisible(self, visible):
        self.dna.removeVisible(visible)
        self.updateVisList()
                         
    def addVisible2DNA(self, visible):
        if visible not in self.getVisList():
            self.dna.addVisible(visible)

    def updateBattleCellList(self):
        obj = self.editor.objectMgr.findObjectByNodePath(self)
        obj[OG.OBJ_PROP]['_battleCellList'] = self.getBattleCellList()

    def addBattleCell(self, cell):
        self.dna.addBattleCell(cell)
        self.updateBattleCellList()

    def removeBattleCell(self, cell):
        self.dna.removeBattleCell(cell)
        self.updateBattleCellList()

    def addBattleCell2DNA(self, battleCell):
        if len(battleCell) == 3:
            cell = DNABattleCell(battleCell[0], battleCell[1], battleCell[2])
            # Store the battle cell in the storage
            DNASTORE.storeBattleCell(cell)
            self.dna.addBattleCell(cell)

    def getBattleCellList(self):
        result = []
        for i in range(self.dna.getNumBattleCells()):
            cell = self.dna.getBattleCell(i)
            result.append([cell.getWidth(), cell.getHeight(), cell.getPos()])

        return result

    def updateSuitEdgeList(self):
        obj = self.editor.objectMgr.findObjectByNodePath(self)
        obj[OG.OBJ_PROP]['_suitEdgeList'] = self.getSuitEdgeList()

    def addSuitEdge(self, edge):
        self.dna.addSuitEdge(edge)
        self.updateSuitEdgeList()

    def removeSuitEdge(self, edge):
        self.dna.removeSuitEdge(edge)
        self.updateSuitEdgeList()

    def addSuitEdge2DNA(self, suitEdge):
        if len(suitEdge) == 2:
            startPoint = DNASTORE.getSuitPointWithIndex(suitEdge[0])
            endPoint = DNASTORE.getSuitPointWithIndex(suitEdge[1])
            edge = DNASuitEdge(startPoint, endPoint, self.groupName)
            # Store the suit edge in the storage
            DNASTORE.storeSuitEdge(edge)
            self.dna.addSuitEdge(edge)

    def getSuitEdgeList(self):
        result = []
        for i in range(self.dna.getNumSuitEdges()):
            suitEdge = self.dna.getSuitEdge(i)
            startPoint = suitEdge.getStartPoint()
            endPoint = suitEdge.getEndPoint()
            result.append([startPoint.getIndex(), endPoint.getIndex()])

        return result

class NodeObj(ToonTownObj):
    def __init__(self, editor, nodeName, dna=None, nodePath=None):
        self.nodeName = nodeName
        ToonTownObj.__init__(self, editor, dna, nodePath)

    def initDNA(self):
        dnaNode = DNANode(self.nodeName)
        return dnaNode    

