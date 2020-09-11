#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Oct 2008
#
# Purpose: The PartyEditorGrid which keeps track of PartyEditorGridSquares
#-------------------------------------------------------------------------------

from pandac.PandaModules import Vec3,Vec4,Point3,TextNode,VBase4

from direct.gui.DirectGui import DirectFrame,DirectButton,DirectLabel,DirectScrolledList,DirectCheckButton
from direct.gui import DirectGuiGlobals
from direct.showbase import DirectObject
from direct.showbase import PythonUtil

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfo
from toontown.parties import PartyUtils
from toontown.parties.PartyEditorGridSquare import PartyEditorGridSquare

class PartyEditorGrid:
    """
    This class holds PartyEditorGridSquares
    """
    notify = directNotify.newCategory("PartyEditorGrid")
    
    def __init__(self, partyEditor):
        self.partyEditor = partyEditor
        self.initGrid()
        self.lastActivityIdPlaced = None

    def initGrid(self):
        # In the grid matrix, None means there is no square there to place items
        self.grid = [[None, None, None, None, None, None, True, True, True, True, True, None, None, None, None, None, None, None],
                     [None, None, None, None, None, True, True, True, True, True, True, True, None, None, None, None, None, None],
                     [None, None, None, None, True, True, True, True, True, True, True, True, True, None, None, None, None, None],
                     [None, True, True, True, True, True, True, True, True, True, True, True, True, True, None, None, None, None],
                     [None, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [None, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [None, None, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, None],
                     [None, None, None, True, True, True, True, True, True, True, True, True, True, True, True, True, None, None],
                     [None, None, None, True, True, True, True, True, True, True, True, True, True, True, True, True, None, None],
                     [None, None, None, None, True, True, True, True, True, True, True, True, True, True, True, None, None, None],
                     [None, None, None, None, None, True, True, True, True, True, True, True, True, True, True, None, None, None],
                    ]
        assert(len(self.grid) == PartyGlobals.PartyEditorGridSize[1])
        assert(len(self.grid[0]) == PartyGlobals.PartyEditorGridSize[0])
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]:
                    self.grid[y][x] = PartyEditorGridSquare(self.partyEditor, x, y)

    def getActivitiesOnGrid(self):
        """
        Return a list of tuples of all activities ( id, x, y, h )
        """
        activities = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] and self.grid[y][x].gridElement:
                    if not self.grid[y][x].gridElement.isDecoration:
                        activityTuple = self.grid[y][x].gridElement.getActivityTuple(x,y)
                        if activityTuple not in activities:
                            activities.append(activityTuple)
        return activities

    def getActivitiesElementsOnGrid(self):
        """
        Return a list of tuples of all activities ( id, x, y, h )
        """
        activities  = []
        activityElems = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] and self.grid[y][x].gridElement:
                    if not self.grid[y][x].gridElement.isDecoration:
                        activityTuple = self.grid[y][x].gridElement.getActivityTuple(x,y)
                        if activityTuple not in activities:
                            activities.append(activityTuple)
                            activityElems.append(self.grid[y][x].gridElement)
        return activityElems

    def getDecorationsOnGrid(self):
        """
        Return a list of tuples of all decorations ( id, x, y, h )
        """
        decorations = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] and self.grid[y][x].gridElement:
                    if self.grid[y][x].gridElement.isDecoration:
                        decorationTuple = self.grid[y][x].gridElement.getDecorationTuple(x,y)
                        if decorationTuple not in decorations:
                            decorations.append(decorationTuple)
        return decorations

    def getGridSquare(self, x, y):
        if y < 0 or y >= PartyGlobals.PartyEditorGridSize[1]:
            return None
        if x < 0 or x >= PartyGlobals.PartyEditorGridSize[0]:
            return None
        return self.grid[y][x]

    def checkGridSquareForAvailability(self, gridSquare, size):
        """
        Check to see if the gridSquare passed in, and any surrounding squares
        based on size, are available for an element to be placed on it/them.
        Every square must be available for this method to return true.
        """
        xOffsetLow, xOffsetHigh, yOffset = self.getXYOffsets(size)
        for y in range(int(gridSquare.y-size[1]/2), int(gridSquare.y+size[1]/2)+yOffset):
            for x in range(int(gridSquare.x-size[0]/2)+xOffsetLow, int(gridSquare.x+size[0]/2)+xOffsetHigh):
                testGridSquare = self.getGridSquare(x,y)
                if testGridSquare is None:
                    return False
                if testGridSquare.gridElement is not None:
                    return False
        return True

    def getClearGridSquare(self, size, desiredXY=None):
        if desiredXY is not None:
            x = desiredXY[0]
            y = desiredXY[1]
            if self.grid[y][x] is not None:
                if self.checkGridSquareForAvailability(self.grid[y][x], size):
                    return self.grid[y][x]
            
        for y in range(PartyGlobals.PartyEditorGridSize[1]):
            for x in range(PartyGlobals.PartyEditorGridSize[0]):
                if self.grid[y][x] is not None:
                    if self.checkGridSquareForAvailability(self.grid[y][x], size):
                        return self.grid[y][x]
        return None

    def getXYOffsets(self, size):
        if size[0]%2 == 0:
            xOffsetLow = 1
            xOffsetHigh = 1
        else:
            xOffsetLow = 0
            xOffsetHigh = 1
        if size[1]%2 == 0:
            yOffset = 0
        else:
            yOffset = 1
        return (xOffsetLow, xOffsetHigh, yOffset)

    def registerNewElement(self, gridElement, centerGridSquare, size):
        assert self.notify.debugStateCall(self)
        xOffsetLow, xOffsetHigh, yOffset = self.getXYOffsets(size)
        assert self.notify.debug("centerGridSquare x=%d y=%d" %
                                 (centerGridSquare.x, centerGridSquare.y))
        assert self.notify.debug("xOffsetLow=%s, xOffsetHight=%s, yOffset=%s" % ( xOffsetLow, xOffsetHigh, yOffset))
        for y in range(int(centerGridSquare.y-size[1]/2), int(centerGridSquare.y+size[1]/2)+yOffset):
            for x in range(int(centerGridSquare.x-size[0]/2)+xOffsetLow, int(centerGridSquare.x+size[0]/2)+xOffsetHigh):
                testGridSquare = self.getGridSquare(x,y)
                if testGridSquare is None:
                    return False
                if testGridSquare.gridElement is not None:
                    return False
                else:
                    testGridSquare.gridElement = gridElement
                    if not gridElement.isDecoration:
                        self.lastActivityIdPlaced = gridElement.id

    def removeElement(self, centerGridSquare, size):
        xOffsetLow, xOffsetHigh, yOffset = self.getXYOffsets(size)
        for y in range(int(centerGridSquare.y-size[1]/2), int(centerGridSquare.y+size[1]/2)+yOffset):
            for x in range(int(centerGridSquare.x-size[0]/2)+xOffsetLow, int(centerGridSquare.x+size[0]/2)+xOffsetHigh):
                testGridSquare = self.getGridSquare(x,y)
                if testGridSquare is None:
                    return False
                if testGridSquare.gridElement is None:
                    return False
                else:
                    testGridSquare.gridElement = None

    def destroy(self):
        # kill the leak caused by a cycle
        self.partyEditor = None
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]:
                    self.grid[y][x].destroy()
        del self.grid

