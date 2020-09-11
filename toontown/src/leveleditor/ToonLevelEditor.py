"""
ToonTown LevelEditor
"""

from pandac.PandaModules import *
from direct.leveleditor.LevelEditorBase import *
from direct.gui import DirectGui
from ObjectMgr import *
from ObjectHandler import *
from ObjectPalette import *
from LevelEditorUI import *
from ProtoPalette import *

from LevelStyleManager import *
from ToonControlManager import *
#from LevelEditorGlobals import *

class ToonLevelEditor(LevelEditorBase):
    """ Class for ToonTown LevelEditor """ 
    def __init__(self):
        self.controlMgr = ToonControlManager(self)
        LevelEditorBase.__init__(self)

        # define your own config file similar to this
        self.settingsFile = os.path.dirname(__file__) + '/LevelEditor.cfg'

        # If you have your own ObjectPalette and ObjectHandler
        # connect them in your own LevelEditor class
        self.objectMgr = ObjectMgr(self)
        self.objectPalette = ObjectPalette()
        self.objectHandler = ObjectHandler(self)
        self.protoPalette = ProtoPalette()

        # LevelEditorUI class must declared after ObjectPalette
        self.ui = LevelEditorUI(self)

        self.DNAData = None
        self.dnaDirectory = Filename.expandFrom(base.config.GetString("dna-directory", "$TTMODELS/src/dna"))

        self.NPToplevel = None
        self.suitPointToplevel = None
        self.lastMousePos = Point3()

        # When you define your own LevelEditor class inheriting LevelEditorBase
        # you should call self.initialize() at the end of __init__() function
        self.initialize()
        self.styleManager = LevelStyleManager(NEIGHBORHOODS, NEIGHBORHOOD_CODES)
        self.accept('DIRECT-mouse1', self.handleMouse1)

    def setTitleWithFilename(self, filename=""):
        title = self.ui.appname
        if filename != "":
           filenameshort = filename.split("\\")
           title = title + " (%s)"%(filenameshort[-1])
        self.ui.SetLabel(title)

    def deleteToplevel(self):
        # Destory old toplevel node path and DNA
        # First the toplevel DNA
        if self.DNAData:
            self.DNAData.remove(self.DNAToplevel)
        # Then the toplevel Node Path
        if self.NPToplevel:
            self.NPToplevel.removeNode()
        if self.suitPointToplevel:
            self.suitPointToplevel.removeNode()
        self.NPParent = render

    def reset(self, fCreateToplevel = 1):
        self.controlMgr.disable()
        LevelEditorBase.reset(self)
        if self.ui.useDriveModeMenuItem.IsChecked():
            self.ui.useDriveModeMenuItem.Toggle()
        
        # Reset path markers
        self.ui.resetPathMarkers()
        # Reset battle cell markers
        self.ui.resetBattleCellMarkers()

        # First destroy existing scene-graph/DNA hierarchy
        self.deleteToplevel()

        # Clear DNASTORE
        DNASTORE.resetDNAGroups()
        # Reset DNA VIS Groups
        DNASTORE.resetDNAVisGroups()
        DNASTORE.resetSuitPoints()
        DNASTORE.resetBattleCells()

        # Create fresh DNA DATA
        self.DNAData = DNAData('level_data')
        if fCreateToplevel:
            self.createToplevel(DNANode('level'))
        # Start block ID at 0 (it will be incremented before use (to 1)):
        self.landmarkBlock=0
        # Set count of groups added to level
        self.setGroupNum(0)
        self.currHoodId = None
        #self.DNATarget = None
        self.setTitleWithFilename()

    def createToplevel(self, dnaNode, nodePath = None):
        # Add toplevel node path for suit points
        self.suitPointToplevel = self.objectMgr.addNewObject('__sys__', parent=render, fSelectObject=False)

        # When you create a new level, data is added to this node
        # When you load a DNA file, you replace this node with the new data
        self.DNAToplevel = dnaNode
        self.NPToplevel = self.objectMgr.addNewObject('__group__', parent=render, fSelectObject=False, nodePath=GroupObj(self, '', dnaNode, nodePath))
        self.DNAData.add(self.DNAToplevel)
        
        # Update parent pointers
        self.DNAParent = self.DNAToplevel
        self.NPParent = self.NPToplevel
        self.VGParent = None
        
    def setEditMode(self, hoodId):
        self.styleManager.setEditMode(HOOD_IDS[hoodId])        
        
    def exportDna(self):
        binaryFilename = Filename(self.currentFile)
        binaryFilename.setBinary()
        if self.DNAData.writeDna(binaryFilename, Notify.out(), DNASTORE):
           self.setTitleWithFilename(binaryFilename)

    # LEVEL OBJECT MANAGEMENT FUNCTIONS
    def findDNANode(self, nodePath):
        """ Find node path's DNA Object in DNAStorage (if any) """
        if nodePath:
            return DNASTORE.findDNAGroup(nodePath.node())
        else:
            return None

    def load(self, fileName):
        self.reset(fCreateToplevel = 0)
        self.fileMgr.loadFromFile(fileName)

        topNodes = render.findAllMatches('=OBJRoot')
        if len(topNodes) == 2:
            for topNode in topNodes:
                obj = self.objectMgr.findObjectByNodePath(topNode)
                if isinstance(obj[OG.OBJ_NP], GroupObj):
                    self.NPToplevel = obj[OG.OBJ_NP]
                else:
                    self.suitPointToplevel = obj[OG.OBJ_NP]
                    
            self.DNAToplevel = self.findDNANode(self.NPToplevel)
            self.DNAData.add(self.DNAToplevel)

            # Update parent pointers
            self.DNAParent = self.DNAToplevel
            self.NPParent = self.NPToplevel
            self.VGParent = None
        else:
            self.createToplevel(DNANode('level'))
            for topNode in topNodes:
                topNode.reparentTo(self.NPToplevel)

        # reset the landmark block number:
        (self.landmarkBlock, needTraverse)=self.findHighestLandmarkBlock(
            self.DNAToplevel, self.NPToplevel)            

        # now update look of objects from loaded DNA
        self.objectMgr.replace(self.NPToplevel)
        self.ui.populateBattleCells()
        self.ui.populateSuitPaths()
        self.currentFile = fileName
        
    def importDna(self, filename):
        self.reset(fCreateToplevel = 0)
        node = loadDNAFile(DNASTORE, Filename.fromOsSpecific(filename).cStr(), CSDefault, 1)        

        for hood in NEIGHBORHOODS:
            if filename.startswith(hood):
                self.currHoodId = NEIGHBORHOOD_CODES[hood]

        if self.currHoodId is None:
            self.currHoodId = 'TT'

        if node.getNumParents() == 1:
            # If the node already has a parent arc when it's loaded, we must
            # be using the level editor and we want to preserve that arc.
            newNPToplevel = NodePath(node)
            newNPToplevel.reparentTo(hidden)
        else:
            # Otherwise, we should create a new arc for the node.
            newNPToplevel = hidden.attachNewNode(node)
        # Make sure the topmost file DNA object gets put under DNARoot
        newDNAToplevel = self.findDNANode(newNPToplevel)

        # reset the landmark block number:
        (self.landmarkBlock, needTraverse)=self.findHighestLandmarkBlock(
            newDNAToplevel, newNPToplevel)

        # Update toplevel variables
        if needTraverse:
            self.createToplevel(newDNAToplevel)
        else:
            self.createToplevel(newDNAToplevel, newNPToplevel)

        self.objectMgr.populateSuitPoints()
        self.objectMgr.createObjects(newDNAToplevel, self.NPToplevel)

        # [gjeon] to be implemented later
        # Create visible representations of all the paths and battle cells
        self.ui.populateSuitPaths()
##         self.hideSuitPaths()
        self.ui.populateBattleCells()
##         self.hideBattleCells()

##         #[gjeon] Handle Animated Props
##         self.loadAnimatedProps(newNPToplevel)
        self.currentFile = filename
        self.setTitleWithFilename(filename)

    def findHighestLandmarkBlock(self, dnaRoot, npRoot):
        npc=npRoot.findAllMatches("**/*:toon_landmark_*")
        highest=0
        for i in range(npc.getNumPaths()):
            path=npc.getPath(i)
            block=path.getName()
            block=int(block[2:block.find(':')])
            if (block > highest):
                highest=block
        # Make a list of flat building names, outside of the
        # recursive function:
        self.flatNames=['random'] + BUILDING_TYPES
        self.flatNames=map(lambda n: n+'_DNARoot', self.flatNames)
        # Search/recurse the dna:
        newHighest=self.convertToLandmarkBlocks(highest, dnaRoot)
        # Get rid of the list of flat building names:
        del self.flatNames

        needToTraverse = (highest!=newHighest)
        return (newHighest, needToTraverse)

    def convertToLandmarkBlocks(self, block, dnaRoot):
        """
        Find all the buildings without landmark blocks and
        assign them one.
        """
        for i in range(dnaRoot.getNumChildren()):
            child = dnaRoot.at(i)
            if DNAClassEqual(child, DNA_LANDMARK_BUILDING):
                # Landmark buildings:
                name=child.getName()
                if name.find('toon_landmark_')==0:
                    block=block+1
                    child.setName('tb'+str(block)+':'+name)
            elif DNAClassEqual(child, DNA_FLAT_BUILDING):
                # Flat buildings:
                name=child.getName()
                if (name in self.flatNames):
                    child.setName('tb0:'+name)
            else:
                block = self.convertToLandmarkBlocks(block, child)
        return block
        
    def handleMouse1(self, modifiers):
        if base.direct.fAlt or modifiers == 4:
            return

        if self.ui.activeMenu:
            self.ui.activeMenu.removePieMenuTask()

    def setName(self, nodePath, newName):
        """ Set name of nodePath's DNA (if it exists) """
        # Find the DNA that corresponds to this node path
        dnaNode = self.findDNANode(nodePath)
        if dnaNode:
            # If it exists, set the name of the DNA Node
            dnaNode.setName(newName)

    def createNewGroup(self, type = 'dna'):
        print "createNewGroup"
        """ Create a new DNA Node group under the active parent """
        # Create a new DNA Node group
        if type == 'dna':
            newDNANode = DNANode('group_' + `self.getGroupNum()`)
        else:
            newDNANode = DNAVisGroup('VisGroup_' + `self.getGroupNum()`)
            # Increment group counter
        self.setGroupNum(self.getGroupNum() + 1)
        # Add new DNA Node group to the current parent DNA Object
        self.DNAParent.add(newDNANode)
        # The new Node group becomes the active parent
        self.DNAParent = newDNANode
        # Traverse it to generate the new node path as a child of NPParent
        newNodePath = self.DNAParent.traverse(self.NPParent, DNASTORE, 1)
        # Update NPParent to point to the new node path
        self.NPParent = newNodePath
        # Update scene graph explorer
        # self.panel.sceneGraphExplorer.update()

    def addGroup(self, nodePath):
        """ Add a new DNA Node Group to the specified Node Path """
        # Set the node path as the current parent
        base.direct.setActiveParent(nodePath)
        # Add a new group to the selected parent
        self.createNewGroup()

    # Count of groups added to level
    def setGroupNum(self, num):
        self.groupNum = num

    def getGroupNum(self):
        return self.groupNum

    def getDNAVisGroups(self, nodePath):
        """ Find the highest level vis groups in the scene graph """
        dnaNode = self.findDNANode(nodePath)
        if dnaNode:
            if DNAClassEqual(dnaNode, DNA_VIS_GROUP):
                obj = self.objectMgr.findObjectByNodePath(nodePath)
                if obj:
                    return [[obj[OG.OBJ_NP], dnaNode]]
                else:
                    return [[nodePath, dnaNode]]
        childVisGroups = []
        children = nodePath.getChildren()
        for child in children:
            childVisGroups = (childVisGroups + self.getDNAVisGroups(child))
        return childVisGroups

    def storeMousePos(self):
        v = self.getGridSnapIntersectionPoint()
        mat = base.direct.grid.getMat(self.NPParent)
        self.lastMousePos = Point3(mat.xformPoint(v))         

    def getGridSnapIntersectionPoint(self):
        """
        Return point of intersection between ground plane and line from cam
        through mouse. Return false, if nothing selected. Snap to grid.
        """
        return base.direct.grid.computeSnapPoint(base.direct.manipulationControl.objectHandles.getMouseIntersectPt())

    def updateSelectedPose(self, nodePathList):
        """
        Update the DNA database to reflect selected objects current positions
        """
        for selectedNode in nodePathList:
            # Is this a DNA Object in the DNASTORE database?
            dnaObject = self.findDNANode(selectedNode)
            if dnaObject:
                # It is, is it a DNA_NODE (i.e. does it have pos/hpr/scale)?
                if DNAIsDerivedFrom(dnaObject, DNA_NODE):
                    # First snap selected node path to grid
                    pos = selectedNode.getPos(base.direct.grid)
                    snapPos = base.direct.grid.computeSnapPoint(pos)
                    #if self.panel.fPlaneSnap.get():
                    #    zheight = 0
                    #else:
                    zheight = snapPos[2]
                    selectedNode.setPos(base.direct.grid,
                                        snapPos[0], snapPos[1], zheight)
                    # Angle snap
                    h = base.direct.grid.computeSnapAngle(selectedNode.getH())
                    if base.direct.grid.getHprSnap():
                        selectedNode.setH(h)
                    if selectedNode == base.direct.selected.last:
                        self.setLastAngle(h)
                    # Update DNA
                    self.updatePose(dnaObject, selectedNode)
            else:
                pointOrCell, type = self.findPointOrCell(selectedNode)
                if pointOrCell and type:
                    # First snap selected node path to grid
                    pos = selectedNode.getPos(base.direct.grid)
                    snapPos = base.direct.grid.computeSnapPoint(pos)
                    #if self.panel.fPlaneSnap.get():
                    #    zheight = 0
                    #else:
                    zheight = snapPos[2]
                    selectedNode.setPos(
                        base.direct.grid,
                        snapPos[0], snapPos[1], zheight)
                    newPos = selectedNode.getPos(self.NPToplevel)
                    # Update DNA
                    pointOrCell.setPos(newPos)
                    if (type == 'suitPointMarker'):
                        print "Found suit point!", pointOrCell
                        # Ok, now update all the lines into that node
                        for edge in self.point2edgeDict[pointOrCell]:
                            # Is it still in edge dict?
                            oldEdgeLine = self.edgeDict.get(edge, None)
                            if oldEdgeLine:
                                del self.edgeDict[edge]
                                oldEdgeLine.reset()
                                oldEdgeLine.removeNode()
                                del oldEdgeLine
                                newEdgeLine = self.drawSuitEdge(
                                    edge, self.NPParent)
                                self.edgeDict[edge] = newEdgeLine
                    elif (type == 'battleCellMarker'):
                        print "Found battle cell!", pointOrCell

    def updatePose(self, dnaObject, nodePath):
        """
        Update a DNA Object's pos, hpr, and scale based upon
        node path's current pose
        """
        # Set DNA's pos, hpr, and scale
        dnaObject.setPos(nodePath.getPos())
        dnaObject.setHpr(nodePath.getHpr())
        dnaObject.setScale(nodePath.getScale())

    def adjustPropChildren(self, nodePath, maxPropOffset = -4):
        for np in nodePath.getChildren():
            dnaNode = self.findDNANode(np)
            if dnaNode:
                if DNAClassEqual(dnaNode, DNA_PROP):
                    if np.getY() < maxPropOffset:
                        np.setY(maxPropOffset)
                        self.updateSelectedPose([np])


base.le = ToonLevelEditor()
run()
