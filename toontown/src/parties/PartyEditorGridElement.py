#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Oct 2008
#
# Purpose: PartyEditorGridElements are placed on PartyEditorGridSquares
#-------------------------------------------------------------------------------

from pandac.PandaModules import Vec3,Vec4,Point3,TextNode,VBase4,NodePath

from direct.gui.DirectGui import DirectFrame,DirectButton,DirectLabel,DirectScrolledList,DirectCheckButton
from direct.gui import DirectGuiGlobals
from direct.showbase import DirectObject
from direct.showbase import PythonUtil
from direct.task.Task import Task

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfo
from toontown.parties import PartyUtils

class PartyEditorGridElement(DirectButton):
    """
    PartyEditorGridElement is created when a PartyEditorListElement is created.
    They are what are placed on PartyEditorGridSquares to represent the element.
    """
    notify = directNotify.newCategory("PartyEditorGridElement")
    
    def __init__(self, partyEditor, id, isDecoration, checkSoldOutAndPaidStatusAndAffordability, **kw):
        self.partyEditor = partyEditor
        self.id = id
        self.isDecoration = isDecoration
        self.checkSoldOutAndPaidStatusAndAffordability = checkSoldOutAndPaidStatusAndAffordability # method
        # Change the name and the up, down, rollover, and disabled colors
        if self.isDecoration:
            self.name = TTLocalizer.PartyDecorationNameDict[self.id]["editor"]
            colorList = ( (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 1.0, 1.0), (0.5, 0.5, 0.5, 1.0))
            self.geom = self.partyEditor.partyPlanner.gui.find("**/%s"%PartyGlobals.DecorationInformationDict[self.id]["gridAsset"])
        else:
            self.name = TTLocalizer.PartyActivityNameDict[self.id]["editor"]
            colorList = ( (1.0, 1.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.5, 0.5, 0.5, 1.0))
            self.geom = self.partyEditor.partyPlanner.gui.find("**/%s"%PartyGlobals.ActivityInformationDict[self.id]["gridAsset"])

        optiondefs = (
            ('geom', self.geom, None),
            ('geom_scale', 1.0, None),
            ('geom_color', colorList[0], None),
            ('geom1_color', colorList[0], None),
            ('geom2_color', colorList[0], None),
            ('geom3_color', colorList[0], None),
            ('relief', None, None),
        )
        
        # Merge keyword options with default options, plus, this call makes
        # DirectButton work... that and the initializeoptions below... without
        # those two calls, strange... and I mean hard to debug, stuff happens.
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, self.partyEditor.parent)
        self.initialiseoptions(PartyEditorGridElement)
        self.setName("%sGridElement"%self.name)
        
        # Since normal buttons only call their command methods upon release
        # of the mouse button, we will not specify a command method and
        # instead bind our own methods to press and release.
        self.bind(DirectGuiGlobals.B1PRESS, self.clicked)
        self.bind(DirectGuiGlobals.B1RELEASE, self.released)
        self.bind(DirectGuiGlobals.ENTER, self.mouseEnter)
        self.bind(DirectGuiGlobals.EXIT, self.mouseExit)
        
        self.uprightNodePath = NodePath("%sUpright"%self.name)
        self.uprightNodePath.reparentTo(self)
        #debugAxis = loader.loadModel("models/misc/xyzAxis")
        #debugAxis.reparentTo(self.uprightNodePath)
        #debugAxis.setScale(0.01)
        rollOverZOffset = self.getGridSize()[1] / 30.0
        self.rolloverTitle = DirectLabel(
            relief = None,
            parent = self.uprightNodePath,
            pos = Point3(0.0, 0.0, rollOverZOffset),
            text = self.name,
            text_fg = (1.0, 1.0, 1.0, 1.0),
            text_shadow = (0.0, 0.0, 0.0, 1.0),
            text_scale = 0.075,
        )
        self.rolloverTitle.stash()
            
        self.stash()
        self.overValidSquare = False
        self.lastValidPosition = None
        self.setColorScale(0.9, 0.9, 0.9, 0.7)
        self.setTransparency(True)
        self.mouseOverTrash = False
        self.centerGridSquare = None

    def getCorrectRotation(self):
        """
        Since the y value is inverted in our grid, we need to flip the rotation
        of elements that are to either side, but not top/bottom.
        """
        r = self.getR()
        if r == 90.0:
            r = 270.0
        elif r == 270.0:
            r = 90.0
        if self.id == PartyGlobals.ActivityIds.PartyCannon:
            return PartyUtils.convertDegreesToPartyGrid((r+180.0))
        return PartyUtils.convertDegreesToPartyGrid(r)

    def getDecorationTuple(self, x, y):
        return (self.id, self.centerGridSquare.x, PartyGlobals.PartyEditorGridSize[1]-1-self.centerGridSquare.y, self.getCorrectRotation())

    def getActivityTuple(self, x, y):
        return (self.id, self.centerGridSquare.x, PartyGlobals.PartyEditorGridSize[1]-1-self.centerGridSquare.y, self.getCorrectRotation())

    def attach(self, mouseEvent):
        PartyEditorGridElement.notify.debug("attached grid element %s" % self.name)
        taskMgr.remove("gridElementDragTask%s"%self.name)
        vWidget2render2d = self.getPos(render2d)
        vMouse2render2d = Point3(mouseEvent.getMouse()[0], 0, mouseEvent.getMouse()[1])
        taskMgr.add(self.elementDragTask, "gridElementDragTask%s"%self.name)
        self.unstash()
        self.rolloverTitle.unstash()
        self.uprightNodePath.reparentTo(self)
        self.setPosHprToDefault()

    def elementDragTask(self, state):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d
            # Check to see if the new position is within the grounds bounds
            if newPos[0] > PartyGlobals.PartyEditorGridBounds[0][0] and \
               newPos[0] < PartyGlobals.PartyEditorGridBounds[1][0] and \
               newPos[2] < PartyGlobals.PartyEditorGridBounds[0][1] and \
               newPos[2] > PartyGlobals.PartyEditorGridBounds[1][1]:
                centerGridSquare = self.snapToGrid(newPos)
                if centerGridSquare is not None:
                    # The mouse is over the grid and over a valid square
                    self.centerGridSquare = centerGridSquare
                    if not self.overValidSquare:
                        self.setOverValidSquare(True)
                    if self.mouseOverTrash:
                        self.setOverTrash(False)
                    return Task.cont
            # Check to see if it is within the trash bounds
            if self.id != PartyGlobals.ActivityIds.PartyClock and \
               newPos[0] > PartyGlobals.PartyEditorTrashBounds[0][0] and \
               newPos[0] < PartyGlobals.PartyEditorTrashBounds[1][0] and \
               newPos[2] < PartyGlobals.PartyEditorTrashBounds[0][1] and \
               newPos[2] > PartyGlobals.PartyEditorTrashBounds[1][1]:            
                if not self.mouseOverTrash:
                    self.setOverTrash(True)
            else:
                if self.mouseOverTrash:
                    self.setOverTrash(False)
            self.setPos(render2d, newPos)
            if self.overValidSquare:
                self.setOverValidSquare(False)
        return Task.cont

    def setOverTrash(self, value):
        self.mouseOverTrash = value
        if value:
            self.partyEditor.trashCanButton["state"] = DirectGuiGlobals.DISABLED
            self.setColorScale(1.0, 0.0, 0.0, 1.0)
        else:
            self.partyEditor.trashCanButton["state"] = DirectGuiGlobals.NORMAL
            self.setColorScale(0.9, 0.9, 0.9, 0.7)

    def setOverValidSquare(self, value):
        self.overValidSquare = value
        if value:
            self.setColorScale(1.0, 1.0, 1.0, 1.0)
        else:
            self.setColorScale(0.9, 0.9, 0.9, 0.7)

    def removeFromGrid(self):
        assert self.notify.debugStateCall(self)
        if self.centerGridSquare is not None:
            self.partyEditor.partyEditorGrid.removeElement(self.centerGridSquare, self.getGridSize())
        self.setOverValidSquare(False)
        self.lastValidPosition = None
        self.stash()

    def snapToGrid(self, newPos):
        gridSquare = self.getGridSquareFromPosition(newPos)
        # If it's None, it's not a square that is allowed to be used
        if gridSquare == None:
            self.setPosHprToDefault()
            self.setPos(render2d, newPos)
            return None
        else:
            # We know the grid square the mouse is over is good, but is it good
            # for all the squares that our element would take up?
            if not self.partyEditor.partyEditorGrid.checkGridSquareForAvailability(gridSquare, self.getGridSize()):
                # It's not available... sorry.
                self.setPos(render2d, newPos)
                return None

        self.setPosHprBasedOnGridSquare(gridSquare)
        return gridSquare

    def getGridSize(self):
        if self.isDecoration:
            return PartyGlobals.DecorationInformationDict[self.id]["gridsize"]
        else:
            return PartyGlobals.ActivityInformationDict[self.id]["gridsize"]

    def setPosHprToDefault(self):
        """Handle edge case we move the element of the edge of grid."""
        self.setR(0.0)
        self.uprightNodePath.setR(0.0)
        # assert self.notify.debug("uprightNodePathR=%s" % self.uprightNodePath.getR())

    def setPosHprBasedOnGridSquare(self, gridSquare):
        gridPos = gridSquare.getPos()
        # Move the position over if the element has any even dimensions
        if self.getGridSize()[0] % 2 == 0:
            gridPos.setX(gridPos[0]+PartyGlobals.PartyEditorGridSquareSize[0]/2.0)
        if self.getGridSize()[1] % 2 == 0:
            gridPos.setZ(gridPos[2]+PartyGlobals.PartyEditorGridSquareSize[1]/2.0)
        # Rotate the element so it always faces towards the center of the grid
        if self.id != PartyGlobals.ActivityIds.PartyFireworks:
            if gridPos[0] > PartyGlobals.PartyEditorGridCenter[0] + PartyGlobals.PartyEditorGridRotateThreshold:
                self.setR(90.0)
                self.uprightNodePath.setR(-90.0)
                # assert self.notify.debug("uprightNodePathR=%s" % self.uprightNodePath.getR())
            elif gridPos[0] < PartyGlobals.PartyEditorGridCenter[0] - PartyGlobals.PartyEditorGridRotateThreshold:
                self.setR(270.0)
                self.uprightNodePath.setR(-270.0)
                # assert self.notify.debug("uprightNodePathR=%s" % self.uprightNodePath.getR())
            elif gridPos[2] < PartyGlobals.PartyEditorGridCenter[1] - PartyGlobals.PartyEditorGridRotateThreshold:
                self.setR(180.0)
                self.uprightNodePath.setR(-180.0)
                # assert self.notify.debug("uprightNodePathR=%s" % self.uprightNodePath.getR())
            else:
                self.setR(0.0)
                self.uprightNodePath.setR(0.0)
                # assert self.notify.debug("uprightNodePathR=%s" % self.uprightNodePath.getR())
        else:
            self.setR(270.0)
            self.uprightNodePath.setR(-270.0)
            # assert self.notify.debug("not fireworks uprightNodePathR=%s" % self.uprightNodePath.getR())
            
        self.setPos(render2d, gridPos)
        self.lastValidPosition = gridPos
        
    def getGridSquareFromPosition(self, newPos):
        localX = newPos[0] - PartyGlobals.PartyEditorGridBounds[0][0]
        localY = newPos[2] - PartyGlobals.PartyEditorGridBounds[1][1]
        x = int(localX / PartyGlobals.PartyEditorGridSquareSize[0])
        y = int(localY / PartyGlobals.PartyEditorGridSquareSize[1])
        # Reverse y value because y goes from bottom to top
        y = PartyGlobals.PartyEditorGridSize[1] - 1 - y
        return self.partyEditor.partyEditorGrid.getGridSquare(x,y)

    def detach(self, mouseEvent):
        assert PartyEditorGridElement.notify.debug("detached grid element %s" % self.name)
        taskMgr.remove("gridElementDragTask%s"%self.name)
        self.rolloverTitle.stash()
        if self.overValidSquare:
            self.partyEditor.partyEditorGrid.registerNewElement(self, self.centerGridSquare, self.getGridSize())
            self.partyEditor.updateCostsAndBank()
            self.partyEditor.handleMutuallyExclusiveActivities()
        else:
            if self.lastValidPosition is not None:
                if self.mouseOverTrash:
                    self.partyEditor.trashCanButton["state"] = DirectGuiGlobals.NORMAL
                    self.lastValidPosition = None
                    self.partyEditor.updateCostsAndBank()
                    self.stash()
                else:
                    self.setPos(render2d, self.lastValidPosition)
                    self.setOverValidSquare(True)
                    self.partyEditor.partyEditorGrid.registerNewElement(self, self.centerGridSquare, self.getGridSize())
                    self.partyEditor.updateCostsAndBank()
                    self.partyEditor.handleMutuallyExclusiveActivities()
                    
            else:
                self.stash()
        self.checkSoldOutAndPaidStatusAndAffordability()

    def placeInPartyGrounds(self, desiredXY=None):
        self.centerGridSquare = self.partyEditor.partyEditorGrid.getClearGridSquare(self.getGridSize(), desiredXY)
        if self.centerGridSquare is not None:
            self.setOverValidSquare(True)
            self.unstash()
            self.setPosHprBasedOnGridSquare(self.centerGridSquare)
            self.partyEditor.partyEditorGrid.registerNewElement(self, self.centerGridSquare, self.getGridSize())
            self.partyEditor.updateCostsAndBank()
            self.partyEditor.partyPlanner.instructionLabel["text"] = TTLocalizer.PartyPlannerEditorInstructionsPartyGrounds
            self.checkSoldOutAndPaidStatusAndAffordability()
            #self.uprightNodePath.wrtReparentTo(aspect2dp)
            return True
        else:
            return False

    def clicked(self, mouseEvent):
        PartyEditorGridElement.notify.debug("clicked grid element %s" % self.name)
        if self.centerGridSquare is not None:
            self.attach(mouseEvent)
            self.partyEditor.partyEditorGrid.removeElement(self.centerGridSquare, self.getGridSize())

    def released(self, mouseEvent):
        PartyEditorGridElement.notify.debug("released grid element %s" % self.name)
        self.detach(mouseEvent)

    def mouseEnter(self, mouseEvent):
        # make sure our text isn't obscured by other stuff in the grid
        parent = self.getParent()
        self.reparentTo(parent)
        self.rolloverTitle.unstash()
    
    def mouseExit(self, mouseEvent):
        self.rolloverTitle.stash()
    
    def destroy(self):
        self.unbind(DirectGuiGlobals.B1PRESS)
        self.unbind(DirectGuiGlobals.B1RELEASE)
        self.unbind(DirectGuiGlobals.ENTER)
        self.unbind(DirectGuiGlobals.EXIT)
        DirectButton.destroy(self)

