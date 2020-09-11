""" DistributedGridAI.py:
    Manage grid based objects in CogHQ.
    AI objects are responsible for adding themselves to the grid, usually in their
    generate method.  Objects are usually entities, but do not necessarily have to
    be.  This means the objId is usually a entId, but not necessarily.  However,
    these id's should be unique, so it's a good idea if they are all either
    entId's or doId's.

    SDN: All objects currently take up a 2x2 area of the grid.  This is because
    the grid was originally designed with crates in mind.  this should be changed.
"""
from CrateGlobals import *
from otp.level import DistributedEntityAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGridAI(DistributedEntityAI.DistributedEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGridAI")

    def __init__(self, level, entId):
        self.initialized = 0
        DistributedEntityAI.DistributedEntityAI.__init__(self, level, entId)

        # Keep a list of "activeCells", cells that listen to on/off events.
        # Instead of sending out on/off messages for every
        # cell, we just need to send on/off messages to the activeCells.
        self.activeCellList = []

    def delete(self):
        DistributedEntityAI.DistributedEntityAI.delete(self)
        del self.activeCellList
        
    def generate(self):
        DistributedEntityAI.DistributedEntityAI.generate(self)

    def initializeGrid(self):
        if not self.initialized:
            self.objPos = {}
            self.gridCells = [None] * self.numRow
            for i in range(len(self.gridCells)):
                self.gridCells[i] = [None] * self.numCol
                for j in range(len(self.gridCells[i])):
                    self.gridCells[i][j] = []
            self.initialized = 1

    def addActiveCell(self, cell):
        self.activeCellList.append(cell)

    # Return the positions between the four cells taken up by a obj
    def getObjPos(self, objId):
        objPos = self.objPos.get(objId, None)
        if objPos:
            row,col = objPos
            if row >= 0 and row < self.numRow and col >= 0 and col < self.numCol:
                return [(col+1) * self.cellSize,
                        (row+1) * self.cellSize,
                        0]
            else:
                self.notify.debug( "row/col out of range %s/%s" % (row, col))
        else:
            self.notify.debug("didn't have record of obj")
        return None

    def addObjectByPos(self, objId, pos, width=1):
        if not self.initialized:
            self.initializeGrid()
        if self.objPos.get(objId, None):
            return 1
        # convert the pos to a grid position and try to
        # add the obj
        x,y = pos[0], pos[1]
        col = min(int(x/self.cellSize),self.numCol-width)
        row = min(int(y/self.cellSize),self.numRow-width)
        self.notify.debug("attempt add %d at %s, row,col = %d,%d" % (objId, pos, row, col))
        while (col >= 0 and col < self.numCol):
            while (row >= 0 and row < self.numRow):
                if self.addObjectByRowCol(objId, row, col):
                    return 1
                else:
                    # something was already there, try the next row
                    row += 2
            else:
                # try the next column
                row = 0
                col += 2
        else:
            self.notify.debug( "requestObjPos: row/col out of range %s/%s" % (row,col))
            row = min(row,self.numRow)
            row = max(0, row)
            col = min(col,self.numRow)
            col = max(0, col)
            return self.addObjectByRowCol(objId,row,col)
        
    def addObjectByRowCol(self, objId, row, col):
        # first check if it is a valid cell
        if (row >=0 and row < self.numRow-1 and
            col >=0 and col < self.numCol-1):
            self.notify.debug("adding obj %s to grid cell %s,%s" % (objId, row,col))
            # add the obj
            self.gridCells[row][col].append(objId)
            self.gridCells[row+1][col].append(objId)
            self.gridCells[row][col+1].append(objId)
            self.gridCells[row+1][col+1].append(objId)
            self.objPos[objId] = [row,col]
            self.__setChangedActiveCells(onList = [[row,col], [row+1,col], [row, col+1], [row+1, col+1]],
                                         objId = objId)
            #self.printGrid()
            return 1
        self.notify.debug("couldn't obj to grid cell %s,%s" % (row,col))
        return 0

    def removeObject(self, objId):
        objPos = self.objPos.get(objId)
        if not objPos:
            return
        row, col = objPos
        # remove the obj
        self.notify.debug("removing obj %s from %s, %s" % (objId, row, col))
        self.gridCells[row][col].remove(objId)
        self.gridCells[row+1][col].remove(objId)
        self.gridCells[row][col+1].remove(objId)
        self.gridCells[row+1][col+1].remove(objId)
        del self.objPos[objId]
        self.__setChangedActiveCells(offList = [[row,col], [row+1,col], [row, col+1], [row+1, col+1]],
                                     objId = objId)
        #self.printGrid()
        

    def checkMoveDir(self, objId, h):
        # this function is useful mainly for maze goons.
        # Given a heading, determine if the next cell
        # in that direction is occupied or not.
        if h > 225 and h < 315:
            return self.checkMove(objId, 0, 1)
        elif h > 45 and h < 135:
            return self.checkMove(objId, 0, -1)
        elif h < 45 or h > 315:
            return self.checkMove(objId, 1, 0)
        elif h > 135 and h < 225:
            return self.checkMove(objId, -1, 0)
        
    def doMoveDir(self, objId, h):
        # this function is useful mainly for maze goons.
        # Given a heading, determine if the next cell
        # in that direction is occupied or not.
        if h > 225 and h < 315:
            return self.doMove(objId, 0, 1)
        elif h > 45 and h < 135:
            return self.doMove(objId, 0, -1)
        elif h < 45 or h > 315:
            return self.doMove(objId, 1, 0)
        elif h > 135 and h < 225:
            return self.doMove(objId, -1, 0)
        
    def checkPush(self, objId, side):
        # side is opposite of direction.  Used mainly for crates
        
        # determine how many units in i,j the obj is
        # requesting to move (based on CrateGlobals.CrateNormals)
        if side == 0:
            return self.checkMove(objId, 0, -1)
        elif side == 1:
            return self.checkMove(objId, 0, 1)
        elif side == 2:
            return self.checkMove(objId, -1, 0)
        elif side == 3:
            return self.checkMove(objId, 1, 0)

    def doPush(self, objId, side):
        if side == 0:
            return self.doMove(objId, 0, -1)
        elif side == 1:
            return self.doMove(objId, 0, 1)
        elif side == 2:
            return self.doMove(objId, -1, 0)
        elif side == 3:
            return self.doMove(objId, 1, 0)

            
    def checkMove(self, objId, dRow, dCol):
        objPos = self.objPos.get(objId)
        if not objPos:
            return
        row, col = objPos

        validMove = 1
        if dRow < 0:
            validMove = validMove & self.__isEmpty(row-1,col) & self.__isEmpty(row-1,col+1)
        elif dRow > 0:
            validMove = validMove & self.__isEmpty(row+2,col) & self.__isEmpty(row+2,col+1)
            
        if dCol < 0:
            validMove = validMove & self.__isEmpty(row,col-1) & self.__isEmpty(row+1,col-1)
        elif dCol > 0:
            validMove = validMove & self.__isEmpty(row,col+2) & self.__isEmpty(row+1,col+2)

        return validMove

    def doMove(self, objId, dRow, dCol):
        objPos = self.objPos.get(objId)
        if not objPos:
            return 0
        row, col = objPos

        validMove = self.checkMove(objId, dRow, dCol)
        if validMove:
            # empty out the current cells
            self.gridCells[row][col].remove(objId)
            self.gridCells[row+1][col].remove(objId)
            self.gridCells[row][col+1].remove(objId)
            self.gridCells[row+1][col+1].remove(objId)
            
            # take the requested cells
            newRow = row + dRow
            newCol = col + dCol
            self.gridCells[newRow][newCol].append(objId)
            self.gridCells[newRow+1][newCol].append(objId)
            self.gridCells[newRow][newCol+1].append(objId)
            self.gridCells[newRow+1][newCol+1].append(objId)

            self.objPos[objId] = [newRow,newCol]
            self.updateActiveCells(objId, row, col, dRow, dCol)
            #self.printGrid()
        return validMove

    def updateActiveCells(self, objId, row, col, dRow, dCol):
        # check if any of the activeCells have been newly occupied
        # or unoccupied
        newRow = row + dRow
        newCol = col + dCol

        # make lists of new cells and old cells
        newCells = [[newRow, newCol],[newRow+1,newCol],
                    [newRow, newCol+1], [newRow+1,newCol+1]]
        oldCells = [[row, col], [row+1,col],
                    [row, col+1], [row+1,col+1]]

        # find new cells that aren't in the old cell list
        onList = []
        offList = []
        for cell in newCells:
            if cell not in oldCells:
                onList.append(cell)
        for cell in oldCells:
            if cell not in newCells:
                offList.append(cell)
        self.__setChangedActiveCells(onList, offList, objId)


    def __setChangedActiveCells(self, onList = [], offList = [], objId = None):
        """ setChangedActiveCells takes a list of newly inhabited
        cells and newly vacated cells.  if any of these cells
        are activeCells, the activeCell states are updated """

        # make sure objId is supplied if onList is supplied
        assert((onList == [] or (onList != [] and objId != None)))
                
        for cell in self.activeCellList:
            self.notify.debug("onList = %s, offList = %s, cell = %s" % (onList, offList, cell.getRowCol()))
            if cell.getRowCol() in onList:
                cell.b_setState(1, objId)
            elif cell.getRowCol() in offList:
                cell.b_setState(0, objId)
                

    def __isEmpty(self, row, col):
        if row < 0 or row >= self.numRow or col < 0 or col >= self.numCol:
            return 0
        if len(self.gridCells[row][col]) > 0:
            return 0
        return 1
        
    
        
    def printGrid(self):
        # this slows the AI down too much, do nothing instead
        #return
    
        if not __debug__:
            return
            
        for i in range(len(self.gridCells)):
            str = ""
            for j in range(len(self.gridCells[i])):
                col = self.gridCells[i][j]
                active = 0
                for cell in self.activeCellList:
                    if cell.getRowCol() == [i,j]:
                        active = 1
                if len(col) > 0:
                    if active:
                        str += '[X]'
                    else:
                        str += ' X '
                else:
                    if active:
                        str += '[.]'
                    else:
                        str += ' . '
            print str + ("  : %d" % i)
        print ""
            
                
                    
    
