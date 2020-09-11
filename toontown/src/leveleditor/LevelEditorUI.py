import os
from pandac.PandaModules import *
from direct.leveleditor.LevelEditorUIBase import *
from direct.gui import DirectGui
from SceneGraphUI import *
from FlatBuildingObj import *
from LandmarkObj import *
from PropObj import *
from AnimPropObj import *
from AnimBuildingObj import *
from GroupObj import *
from SignEditFrame import *
from VisGroupsUI import *

from LevelEditorGlobals import HOOD_IDS

ID_SAVE_DNA    = 1101
ID_SAVE_DNA_AS = 1102
ID_OPEN_DNA    = 1103

ID_EDIT_VIS = 1201

ID_SHOW_BATTLE_CELLS = 1301
ID_SHOW_SUIT_PATH = 1302
ID_USE_DRIVE_MODE = 1303
ID_MAKE_LONG_STREET = 1304

AppName = 'ToonTown Level Editor'

class LevelEditorUI(LevelEditorUIBase):
    """ Class for Panda3D LevelEditor """
    frameWidth = 800
    frameHeight = 600
    appversion      = '2.0'
    appname         = AppName

    def __init__(self, editor, *args, **kw):
        if not kw.get('size'):
            kw['size'] = wx.Size(self.frameWidth, self.frameHeight)

        self.MENU_TEXTS.update({
        ID_OPEN_DNA : ("Open DNA", None),
        ID_SAVE_DNA : ("&Save DNA", "LE-SaveDNA"),
        ID_SAVE_DNA_AS : ("Save DNA &As", None),
        ID_EDIT_VIS : ("Edit Vis Groups", None),
        ID_SHOW_BATTLE_CELLS : ("Show Battle Cells", None),
        ID_SHOW_SUIT_PATH : ("Show Suit Path", None),
        ID_USE_DRIVE_MODE : ("Use Drive Mode", None),
        ID_MAKE_LONG_STREET : ("Make Long Street", None),
        })

        LevelEditorUIBase.__init__(self, editor, *args, **kw)       
        self.appName = AppName
        self.activeMenu = None
        self.visGroupsUI = None

        # SUIT POINTS
        # Create a sphere model to show suit points
        self.suitPointMarker = loader.loadModel('models/misc/sphere')
        self.suitPointMarker.setScale(0.25)

        # Initialize the suit points
        self.startSuitPoint = None
        self.endSuitPoint = None
        self.currentSuitPointType = DNASuitPoint.STREETPOINT

        # BATTLE CELLS
        self.battleCellMarker = loader.loadModel('models/misc/sphere')
        self.battleCellMarker.setName('battleCellMarker')
        self.battleCellMarker.setScale(1)

        # Used to store whatever edges and points are loaded in the level
        self.edgeDict = {}
        self.np2EdgeDict = {}
        self.pointDict = {}
        self.point2edgeDict = {}
        self.cellDict = {}

        self.visitedPoints = []
        self.visitedEdges = []

        self.zoneLabels = []
        
    def createInterface(self):
        LevelEditorUIBase.createInterface(self)
        self.sceneGraphUI = SceneGraphUI(self.leftBarDownPane0, self.editor)

    def createMenu(self):
        LevelEditorUIBase.createMenu(self)
        menuItem = self.menuFile.Insert(self.menuFile.GetMenuItemCount() - 3, ID_OPEN_DNA, self.MENU_TEXTS[ID_OPEN_DNA][0])
        self.Bind(wx.EVT_MENU, self.onOpenDna, menuItem)

        menuItem = self.menuFile.Insert(self.menuFile.GetMenuItemCount() - 1, ID_SAVE_DNA, self.MENU_TEXTS[ID_SAVE_DNA][0])
        self.Bind(wx.EVT_MENU, self.onSaveDna, menuItem)

        menuItem = self.menuFile.Insert(self.menuFile.GetMenuItemCount() - 1, ID_SAVE_DNA_AS, self.MENU_TEXTS[ID_SAVE_DNA_AS][0])
        self.Bind(wx.EVT_MENU, self.onSaveDnaAs, menuItem)

        menuItem = self.menuEdit.Append(ID_EDIT_VIS, self.MENU_TEXTS[ID_EDIT_VIS][0])
        self.Bind(wx.EVT_MENU, self.onEditVis, menuItem)
        
        self.showBattleCellsMenuItem = self.menuOptions.Append(ID_SHOW_BATTLE_CELLS, self.MENU_TEXTS[ID_SHOW_BATTLE_CELLS][0], kind = wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onShowBattleCells, self.showBattleCellsMenuItem)

        self.showSuitPathMenuItem = self.menuOptions.Append(ID_SHOW_SUIT_PATH, self.MENU_TEXTS[ID_SHOW_SUIT_PATH][0], kind = wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onShowSuitPath, self.showSuitPathMenuItem)

        self.useDriveModeMenuItem = self.menuOptions.Append(ID_USE_DRIVE_MODE, self.MENU_TEXTS[ID_USE_DRIVE_MODE][0], kind = wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onUseDriveMode, self.useDriveModeMenuItem)
        
        self.makeLongStreetMenuItem = self.menuOptions.Append(ID_MAKE_LONG_STREET, self.MENU_TEXTS[ID_MAKE_LONG_STREET][0], kind = wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.onMakeLongStreet, self.makeLongStreetMenuItem)

    def reset(self):
        LevelEditorUIBase.reset(self)
        if self.visGroupsUI:
            self.visGroupsUI.Destroy()
            
    def buildContextMenu(self, nodePath):
        LevelEditorUIBase.buildContextMenu(self, nodePath)
        obj = self.editor.objectMgr.findObjectByNodePath(nodePath)
        if obj is None:
            return

        objNP = obj[OG.OBJ_NP]
        objDef = obj[OG.OBJ_DEF]

        def addSubMenuItem(name, subMenu, menuMode, dnaTarget, dnaParent=None, hood=None):
            if hood is None:
               hood = objDef.hood
            self.contextMenu.addItem(name, subMenu,
                                     lambda \
                                     p0=None, p1=menuMode, p2=dnaTarget, p3=dnaParent, p4=objNP, p5=hood:\
                                     self.spawnMenu(p0, p1, p2, p3, p4, p5))

        def addSignMenuItem(objNP):
            dnaTarget = DNAGetChildOfClass(objNP.dna, DNA_SIGN)
            addSubMenuItem('Sign Texture', None, 'sign_texture', dnaTarget, objNP.dna)
            if dnaTarget:
               addSubMenuItem('Sign Color', None, 'sign_color', dnaTarget, objNP.dna)
               self.buildSignTextSubMenu(dnaTarget, objNP)
               self.buildSignGraphicsSubMenu(dnaTarget, objNP)

        if isinstance(objNP, FlatBuildingObj):
            heightList, offsetList = objNP.computeWallNum()

            for i in range(len(heightList)-1,-1,-1):
                subMenu = self.contextMenu.addMenu('Menu for floor %d'%i)
                wall = objNP.getWall(i)
                addSubMenuItem('Wall Texture', subMenu, 'wall_texture', wall, objNP)
                addSubMenuItem('Wall Style', subMenu, 'wall_style', wall, objNP)
                addSubMenuItem('Wall Orientation', subMenu, 'wall_orientation', wall, objNP)
                addSubMenuItem('Wall Color', subMenu, 'wall_color', wall, objNP)
                
                subMenu.AppendSeparator()
                dnaTarget = DNAGetChildOfClass(wall, DNA_CORNICE)
                addSubMenuItem('Cornice Texture', subMenu, 'cornice_texture', dnaTarget, wall)
                addSubMenuItem('Cornice Orientation', subMenu, 'cornice_orientation', dnaTarget, wall)
                addSubMenuItem('Cornice Color', subMenu, 'cornice_color', dnaTarget, wall)


                subMenu.AppendSeparator()
                dnaTarget = DNAGetChildOfClass(wall, DNA_FLAT_DOOR)
                addSubMenuItem('Door Texture', subMenu, 'door_single_texture', dnaTarget, wall)
                addSubMenuItem('Door Orientation', subMenu, 'door_orientation', dnaTarget, wall)
                addSubMenuItem('Door Color', subMenu, 'door_color', dnaTarget, wall)

                subMenu.AppendSeparator()
                dnaTarget = DNAGetChildOfClass(wall, DNA_WINDOWS)
                addSubMenuItem('Window Texture', subMenu, 'window_texture', dnaTarget, wall)
                addSubMenuItem('Window Count', subMenu, 'window_count', dnaTarget, wall)
                addSubMenuItem('Window Orientation', subMenu, 'window_orientation', dnaTarget, wall)
                addSubMenuItem('Window Color', subMenu, 'window_color', dnaTarget, wall)
                
        elif isinstance(objNP, LandmarkObj):
            if obj[OG.OBJ_PROP]['Special Type'] not in ['hq', 'kartshop']:
                # beacuse hq or kartshop can't have doors
                dnaTarget = DNAGetChildOfClass(objNP.dna, DNA_DOOR)
                addSubMenuItem('Door Texture', None, 'door_double_texture', dnaTarget, objNP.dna)            
                addSubMenuItem('Door Orientation', None, 'door_orientation', dnaTarget, objNP.dna)
                addSubMenuItem('Door Color', None, 'door_color', dnaTarget, objNP.dna)
                self.contextMenu.AppendSeparator()
            addSignMenuItem(objNP)

        elif isinstance(objNP, PropObj):
            if objDef.hood == 'Generic':
                for hoodId in HOOD_IDS.keys():
                    addSubMenuItem('Prop Color for %s'%hoodId, None, 'prop_color', objNP.dna, None, hoodId) 
            else:
                addSubMenuItem('Prop Color', None, 'prop_color', objNP.dna)         
            addSignMenuItem(objNP)
        elif isinstance(objNP, AnimBuildingObj):
            addSignMenuItem(objNP)

        elif isinstance(objNP, AnimPropObj):
            addSubMenuItem('Prop Color', None, 'prop_color', objNP.dna)
            addSignMenuItem(objNP)

        elif isinstance(objNP, VisGroupObj):
            # add/remove battle cell...
            battleCellTypeList = ['20w 20l', '20w 30l', '30w 20l', '30w 30l']
            self.buildBattleCellSubMenu(objNP.dna, objNP, battleCellTypeList)

    def buildBattleCellSubMenu(self, visGroupDNA, objNP, battleCellTypeList):
        subMenu = self.contextMenu.addMenu('Battle Cells')
        subMenuBattleCells = self.contextMenu.addMenu('Add Battle Cell', subMenu)
        for battleCellType in battleCellTypeList:
            self.contextMenu.addItem(battleCellType, subMenuBattleCells, lambda p0=None, p1=objNP, p2=visGroupDNA, p3=battleCellType: self.addBattleCell(p0, p1, p2, p3))
        subMenu.AppendSeparator()
        numCells = visGroupDNA.getNumBattleCells()
        for i in range(numCells):
            cell = visGroupDNA.getBattleCell(i)
            if cell:
               subMenuBattleCells = self.contextMenu.addMenu("Cell %d (%dx%d)"%(i, cell.getWidth(), cell.getHeight()), subMenu)
               self.contextMenu.addItem('Remove', subMenuBattleCells, lambda p0=None, p1=objNP, p2=visGroupDNA, p3=cell: self.removeBattleCell(p0, p1, p2, p3))

    def addBattleCell(self, evt, objNP, visGroupDNA, battleCellType):
        absPos = self.editor.lastMousePos

        if (battleCellType == '20w 20l'):
            cell = DNABattleCell(20, 20, absPos)
        elif (battleCellType == '20w 30l'):
            cell = DNABattleCell(20, 30, absPos)
        elif (battleCellType == '30w 20l'):
            cell = DNABattleCell(30, 20, absPos)
        elif (battleCellType == '30w 30l'):
            cell = DNABattleCell(30, 30, absPos)

        # Store the battle cell in the storage
        DNASTORE.storeBattleCell(cell)
        # Draw the battle cell
        numCells = visGroupDNA.getNumBattleCells()
        marker = self.drawBattleCell(cell, objNP, numCells)
        # Keep a handy dict of the visible markers
        self.cellDict[cell] = marker
        # Store the battle cell in the current vis group
        objNP.addBattleCell(cell)
        self.buildContextMenu(objNP)

    def removeBattleCell(self, evt, objNP, visGroupDNA, cell):
        marker = self.cellDict[cell]
        if not marker:
           return
        marker.remove()

        objNP.removeBattleCell(cell)
        # Remove cell from DNASTORE
        if DNASTORE.removeBattleCell(cell):
            print "Removed from DNASTORE"
        else:
            print "Not found in DNASTORE"        

        del self.cellDict[cell]
        for i in range(visGroupDNA.getNumBattleCells()):
            cell = visGroupDNA.getBattleCell(i)
            if not cell:
               continue
            marker = self.cellDict[cell]
            if not marker:
               continue
            label = marker.find('**/+PGItem')
            if label:
               label.remove()
            self.drawBattleCellLabel(marker, i)
        self.buildContextMenu(objNP)

    def populateBattleCells(self):
        visGroups = self.editor.getDNAVisGroups(self.editor.NPToplevel)
        for visGroup in visGroups:
            np = visGroup[0]
            dnaVisGroup = visGroup[1]
            numCells = dnaVisGroup.getNumBattleCells()
            for i in range(numCells):
                cell = dnaVisGroup.getBattleCell(i)
                marker = self.drawBattleCell(cell, np, i)
                self.cellDict[cell] = marker

        self.onShowBattleCells()
                
    def drawBattleCellLabel(self, marker, cellId=0):
        marker.setTag('cellId', '%d'%cellId)
        label = DirectGui.DirectLabel(text = '%d'%cellId,
                                      parent = marker,
                                      relief = None, scale = 3)
        label.setBillboardPointEye(0)
        label.setScale(0.4)

    def drawBattleCell(self, cell, parent, cellId=0):
        marker = self.battleCellMarker.copyTo(parent)
        self.drawBattleCellLabel(marker, cellId)
        # Greenish
        marker.setColor(0.25, 0.75, 0.25, 0.5)
        marker.setTransparency(1)
        marker.setPos(cell.getPos())
        # scale to radius which is width/2
        marker.setScale(cell.getWidth()/2.0,
                        cell.getHeight()/2.0,
                        1)
        return marker

    def resetBattleCellMarkers(self):
        for cell, marker in self.cellDict.items():
            if not marker.isEmpty():
                marker.remove()
        self.cellDict = {}

    def buildSignTextSubMenu(self, signDNA, objNP):
        subMenu = self.contextMenu.addMenu('Sign Text')
        self.contextMenu.addItem('Add Baseline', subMenu, lambda p0=None, p1=objNP, p2=signDNA, p3=None: self.openSignTextDialog(p0, p1, p2, p3))
        subMenu.AppendSeparator()
        baselineDNAList = DNAGetChildren(signDNA, DNA_SIGN_BASELINE)
        for baselineDNA in baselineDNAList:
            signGraphicsList = DNAGetChildren(baselineDNA, DNA_SIGN_GRAPHIC)
            if len(signGraphicsList) <= 0:
               baselineDNAText = DNAGetBaselineString(baselineDNA)
               if baselineDNAText == "":
                  baselineDNAText = 'none'
               subMenuBaseline = self.contextMenu.addMenu(baselineDNAText, subMenu)
               self.contextMenu.addItem('Edit', subMenuBaseline, lambda p0=None, p1=objNP, p2=signDNA, p3=baselineDNA: self.openSignTextDialog(p0, p1, p2, p3))
               self.contextMenu.addItem('Remove', subMenuBaseline, lambda p0=None, p1=objNP, p2=signDNA, p3=baselineDNA: self.removeSignBaseline(p0, p1, p2, p3))

    def buildSignGraphicsSubMenu(self, signDNA, objNP):
        subMenu = self.contextMenu.addMenu('Sign Graphics')
        subMenuGraphics = self.contextMenu.addMenu('Add Graphics', subMenu)
        graphicsCodeList = self.editor.styleManager.getCatalogCodes('graphic')
        for graphicsCode in graphicsCodeList:
            self.contextMenu.addItem(graphicsCode, subMenuGraphics, lambda p0=None, p1=objNP, p2=signDNA, p3=None, p4=None, p5=graphicsCode: self.openSignGraphicsDialog(p0, p1, p2, p3, p4, p5))
        subMenu.AppendSeparator()
        baselineDNAList = DNAGetChildren(signDNA, DNA_SIGN_BASELINE)
        for baselineDNA in baselineDNAList:
            signGraphicsList = DNAGetChildren(baselineDNA, DNA_SIGN_GRAPHIC)
            if len(signGraphicsList) > 0:
               baselineDNAText = DNAGetBaselineString(baselineDNA)
               subMenuBaseline = self.contextMenu.addMenu(baselineDNAText, subMenu)
               self.contextMenu.addItem('Edit', subMenuBaseline, lambda p0=None, p1=objNP, p2=signDNA, p3=baselineDNA, p4=signGraphicsList[0], p5=None: self.openSignGraphicsDialog(p0, p1, p2, p3, p4, p5))
               self.contextMenu.addItem('Remove', subMenuBaseline, lambda p0=None, p1=objNP, p2=signDNA, p3=baselineDNA: self.removeSignBaseline(p0, p1, p2, p3))

    def openSignTextDialog(self, evt, objNP, signDNA, baselineDNA):
        if baselineDNA is None:
           baselineDNA = DNASignBaseline()
           DNASetBaselineString(baselineDNA, 'none')
           fontChoices = self.editor.styleManager.getCatalogCodes('font')
           baselineDNA.setCode(fontChoices[0])
           baselineDNA.setColor(VBase4(0.0, 0.0, 0.0, 1.0))
           signDNA.add(baselineDNA)
           objNP.replace()

        SignEditFrame(self.viewFrame, self.editor, baselineDNA, objNP).Show()

    def openSignGraphicsDialog(self, evt, objNP, signDNA, baselineDNA, graphicsDNA, graphicsCode):
        if graphicsDNA is None:
           graphicsDNA = DNASignGraphic()
           graphicsDNA.setCode(graphicsCode)

        if baselineDNA is None:
           baselineDNA = DNASignBaseline()
           signDNA.add(baselineDNA)

        baselineDNA.add(graphicsDNA)
        objNP.replace()

        SignEditFrame(self.viewFrame, self.editor, baselineDNA, objNP, True).Show()
        
    def removeSignBaseline(self, evt, objNP, sign, baselineDNA):
        #DNARemoveAllChidrenOfClass(sign, DNA_SIGN_BASELINE)
        sign.remove(baselineDNA)
        objNP.replace()

    def spawnMenu(self, evt, menuMode, dnaTarget, dnaParent, objNP, hood):
        # set current hood edit mode
        self.editor.setEditMode(hood)
        
        attribute = self.editor.styleManager.getAttribute(menuMode)
        self.activeMenu = attribute.getMenu()
        LE_showInOneCam(self.activeMenu, base.direct.camera.getName())
        # Set initial state
        state = None

        if 'wall' in menuMode:
            dnaType = 'wall'
        elif 'cornice' in menuMode:
            dnaType = 'cornice'
        elif 'sign' in menuMode:
            dnaType = 'sign'
        elif 'door_single' in menuMode:
            dnaType = 'door'
        elif 'door_double' in menuMode:
            dnaType = 'landmark_door'
        elif 'door_color' in menuMode or\
             'door_orientation' in menuMode:
            if isinstance(objNP, LandmarkObj):
                dnaType = 'landmark_door'
            else:
                dnaType = 'door'
        elif 'window' in menuMode:
            dnaType = 'windows'
        elif 'street' in menuMode:
            dnaType = 'street'
        elif 'prop' in menuMode:
            dnaType = 'prop'

        if string.find(menuMode,'texture') >= 0:
            if dnaTarget:
                state = dnaTarget.getCode()
            action = lambda x: objNP.setDNATargetCode(dnaType, dnaTarget, dnaParent, x)
        elif string.find(menuMode, 'color') >= 0:
            if dnaTarget:
                state = dnaTarget.getColor()
            action = lambda x: objNP.setDNATargetColor(dnaType, dnaTarget, dnaParent, x)
        elif string.find(menuMode, 'orientation') >= 0:
            if dnaTarget:
                state = dnaTarget.getCode()[-2:]
            action = lambda x: objNP.setDNATargetOrientation(dnaType, dnaTarget, dnaParent, x)
        elif menuMode == 'window_count':
            if dnaTarget:
                state = dnaTarget.getWindowCount()
            action = lambda x: objNP.setWindowCount(dnaTarget, dnaParent, x)
##             elif menuMode == 'baseline_style':
##                 # Extract the baseline style
##                 state = DNABaselineStyle(
##                     baseline = self.panel.currentBaselineDNA)
        elif menuMode == 'wall_style':
            if dnaTarget:
                # Extract the wall style from the current wall
                state = DNAWallStyle(wall = dnaTarget)
            action = lambda x: objNP.setWallStyle(dnaTarget, x)                
##         elif menuMode.startswith('animlist_'):
##             if dnaTarget:
##                 state = dNATarget.getAnim()

        self.activeMenu.setInitialState(state)
        # Spawn active menu's task
        self.activeMenu.spawnPieMenuTask()
        self.activeMenu.action = action

    def onSaveDna(self, evt=None):
        if not self.editor.currentFile or\
           not self.editor.currentFile.endswith('.dna'):
            return self.onSaveDnaAs(evt)
        self.editor.exportDna()

    def onSaveDnaAs(self, evt):
        path = self.editor.dnaDirectory.toOsSpecific()
        if not os.path.isdir(path):
           path = '.'
        dialog = wx.FileDialog(None, "Save DNA File As", path, "", "*.dna", wx.SAVE)
        result = True
        if dialog.ShowModal() == wx.ID_OK:
            self.editor.currentFile = dialog.GetPath();
            self.editor.exportDna()
        else:
            result = False
        dialog.Destroy()
        return result

    def onOpenDna(self, evt=None):
        path = self.editor.dnaDirectory.toOsSpecific()
        if not os.path.isdir(path):
           path = '.'
        dialog = wx.FileDialog(None, "Choose a DNA file", path, "", "*.dna", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.editor.importDna(dialog.GetPath())
        dialog.Destroy()

    def onEditVis(self, evt=None):
        if self.visGroupsUI:
            self.visGroupsUI.Destroy()
        visGroups = self.editor.getDNAVisGroups(self.editor.NPToplevel)
        if visGroups:
            self.visGroupsUI = VisGroupsUI(self, -1, 'Edit Vis Groups', self.editor, visGroups)
            self.visGroupsUI.Show()
        else:
            wx.MessageBox("No DNA Vis Groups Found!", 'Edit Vis Groups', wx.ICON_EXCLAMATION)

    def onRightDown(self, evt=None):
        """Invoked when the viewport is right-clicked."""
        if evt == None:
            mpos = wx.GetMouseState()
            mpos = self.ScreenToClient((mpos.x, mpos.y))
        else:
            mpos = evt.GetPosition()

        self.editor.storeMousePos()
        base.direct.fMouse3 = 0
        self.PopupMenu(self.contextMenu, mpos)

    def onShowBattleCells(self, evt=None):
        for cell, marker in self.cellDict.items():
            if self.showBattleCellsMenuItem.IsChecked():
               marker.show()
            else:
               marker.hide()

    def onShowSuitPath(self, evt=None):
        for edge, edgeLine in self.edgeDict.items():
            if self.showSuitPathMenuItem.IsChecked():
                edgeLine.show()
            else:
                edgeLine.hide()
        for point, marker in self.pointDict.items():
            if self.showSuitPathMenuItem.IsChecked():
                marker.show()
            else:
                marker.hide()

    def onUseDriveMode(self, evt=None):
        if self.useDriveModeMenuItem.IsChecked():
            self.editor.controlMgr.enable()
        else:
            self.editor.controlMgr.disable()

    def drawSuitEdge(self, edge, parent):
        # Draw a line from start to end
        edgeLine = LineNodePath(parent)
        edgeLine.lineNode.setName('suitEdge')
        edgeLine.setColor(VBase4(0.0, 0.0, 0.5, 1))
        edgeLine.setThickness(1)
        edgeLine.reset()
        # We need to draw the arrow relative to the parent, but the
        # point positions are relative to the NPToplevel. So get the
        # start and end positions relative to the parent, then draw
        # the arrow using those points
        tempNode = self.editor.NPToplevel.attachNewNode('tempNode')
        mat = self.editor.NPToplevel.getMat(parent)
        relStartPos = Point3(mat.xformPoint(edge.getStartPoint().getPos()))
        relEndPos = Point3(mat.xformPoint(edge.getEndPoint().getPos()))
        # Compute offset: a vector rotated 90 degrees clockwise
        offset = Vec3(relEndPos - relStartPos)
        offset.normalize()
        offset *= 0.1
        a = offset[0]
        offset.setX(offset[1])
        offset.setY(-1 * a)
        # Just to get it above the street
        offset.setZ(0.05)
        # Add offset to start and end to help differentiate lines
        relStartPos += offset
        relEndPos += offset
        # Draw arrow
        edgeLine.drawArrow(relStartPos,
                           relEndPos,
                           15, # arrow angle
                           1) # arrow length
        edgeLine.create()
        # Add a clickable sphere
        marker = self.suitPointMarker.copyTo(edgeLine)
        marker.setName('suitEdgeMarker')
        midPos = (relStartPos + relEndPos)/2.0
        marker.setPos(midPos)
        # Adjust color of highlighted lines
        if edge in self.visitedEdges:
            NodePath.setColor(edgeLine, 1, 0, 0, 1)
        # Clean up:
        tempNode.removeNode()
        return edgeLine

    def drawSuitPoint(self, suitPoint, pos, type, parent):
        marker = self.suitPointMarker.copyTo(parent)
        marker.setName("suitPointMarker")
        marker.setPos(pos)
        if (type == DNASuitPoint.STREETPOINT):
            marker.setColor(0, 0, 0.6)
            marker.setScale(0.4)
        elif (type == DNASuitPoint.FRONTDOORPOINT):
            marker.setColor(0, 0, 1)
            marker.setScale(0.5)
        elif (type == DNASuitPoint.SIDEDOORPOINT):
            marker.setColor(0, 0.6, 0.2)
            marker.setScale(0.5)
        # Highlight if necessary
        if suitPoint in self.visitedPoints:
            marker.setColor(1, 0, 0, 1)
        return marker

    def resetPathMarkers(self):
        for edge, edgeLine in self.edgeDict.items():
            if not edgeLine.isEmpty():
                edgeLine.reset()
                edgeLine.removeNode()
        self.edgeDict = {}
        self.np2EdgeDict = {}
        for point, marker in self.pointDict.items():
            if not marker.isEmpty():
                marker.removeNode()
        self.pointDict = {}
        self.point2edgeDict = {}

    def populateSuitPaths(self):
##         # Points
##         numPoints = DNASTORE.getNumSuitPoints()
##         for i in range(numPoints):
##             point = DNASTORE.getSuitPointAtIndex(i)
##             marker = self.drawSuitPoint(point,
##                 point.getPos(), point.getPointType(),
##                 self.editor.suitPointToplevel)
##             self.pointDict[point] = marker

        # Edges
        visGroups = self.editor.getDNAVisGroups(self.editor.NPToplevel)
        for visGroup in visGroups:
            np = visGroup[0]
            dnaVisGroup = visGroup[1]
            numSuitEdges = dnaVisGroup.getNumSuitEdges()
            for i in range(numSuitEdges):
                edge = dnaVisGroup.getSuitEdge(i)
                edgeLine = self.drawSuitEdge(edge, np)
                self.edgeDict[edge] = edgeLine
                self.np2EdgeDict[edgeLine.id()] = [edge, dnaVisGroup]
                # Store the edge on each point in case we move the point
                # we can update the edge
                for point in [edge.getStartPoint(), edge.getEndPoint()]:
                    if self.point2edgeDict.has_key(point):
                        self.point2edgeDict[point].append(edge)
                    else:
                        self.point2edgeDict[point] = [edge]

        self.onShowSuitPath()

    def updateBarricadeDict(self, side, barricadeOrigNum, curBldgGroupIndex):
        barricadeDict = None
        if (side == 'outer'):
            barricadeDict = self.outerBarricadeDict
        elif (side == 'inner'):
            barricadeDict = self.innerBarricadeDict
        else:
            print("unhandled side %s" % side)
            return

        if not barricadeDict.has_key(barricadeOrigNum):
            barricadeDict[barricadeOrigNum] = [curBldgGroupIndex, curBldgGroupIndex]

        if curBldgGroupIndex < barricadeDict[barricadeOrigNum][0]:
            barricadeDict[barricadeOrigNum][0] = curBldgGroupIndex

        if barricadeDict[barricadeOrigNum][1] < curBldgGroupIndex:
            barricadeDict[barricadeOrigNum][1] = curBldgGroupIndex

        print "---------- %s barricadeDict origNum=%d  data=(%d, %d)" %(side, barricadeOrigNum, barricadeDict[barricadeOrigNum][0], barricadeDict[barricadeOrigNum][1])

    def reparentStreetBuildings(self, nodePath):
        dnaNode = self.editor.findDNANode(nodePath)
        if dnaNode:
            if (DNAClassEqual(dnaNode, DNA_FLAT_BUILDING) or
                DNAClassEqual(dnaNode, DNA_LANDMARK_BUILDING)):
                base.direct.reparent(nodePath, fWrt = 1)
        children = nodePath.getChildren()
        for child in children:
            self.reparentStreetBuildings(child)

    def consolidateStreetBuildings(self):
        # First put everything under the ATR group so the leftover
        # can be easily deleted
        originalChildren = self.editor.NPToplevel.getChildren()
        self.editor.addGroup(self.editor.NPToplevel)
        atrGroup = self.editor.NPParent
        atrGroup.setName('ATR')
        self.editor.setName(atrGroup, 'ATR')
        base.direct.setActiveParent(atrGroup)
        for child in originalChildren:
            base.direct.reparent(child)
        # Now create a new group with just the buildings
        self.editor.addGroup(self.editor.NPToplevel)
        newGroup = self.editor.NPParent
        newGroup.setName('LongStreet')
        self.editor.setName(newGroup, 'LongStreet')
        base.direct.setActiveParent(newGroup)
        self.reparentStreetBuildings(self.editor.NPToplevel)
        return newGroup

    def makeNewBuildingGroup(self, sequenceNum, side, curveName):
        print "-------------------------- new building group %s  curveName=%s------------------------" % (sequenceNum, curveName)
        # Now create a new group with just the buildings
        self.editor.addGroup(self.editor.NPToplevel)
        newGroup = self.editor.NPParent
        groupName = ''
        #if curveName == "urban_curveside_inner_1_1":
        #    import pdb; pdb.set_trace()

        if 'curveside' in curveName:
            #we want to preserve which group the side street is closest to
            print "special casing %s" % curveName
            parts = curveName.split('_')
            groupName = 'Buildings_' + side + "-" + parts[3] + "_" + parts[4]
            print "groupname = %s" % groupName
        else:
            groupName = 'Buildings_' + side + "-" + str(sequenceNum)
        newGroup.setName(groupName)
        self.editor.setName(newGroup, groupName)
        base.direct.setActiveParent(newGroup)

        if 'barricade_curve' in curveName:
            parts = curveName.split('_')
            origBarricadeNum = parts[3]
            self.updateBarricadeDict(side, int(origBarricadeNum),  sequenceNum)

    def getBuildingWidth(self, bldg):
        dnaNode = self.editor.findDNANode(bldg)
        bldgWidth = 0
        if DNAClassEqual(dnaNode, DNA_FLAT_BUILDING):
            bldgWidth = dnaNode.getWidth()
        elif DNAClassEqual(dnaNode, DNA_LANDMARK_BUILDING):
            objectCode = dnaNode.getCode()
            if objectCode[-2:-1] == 'A':
                bldgWidth = 25.0
            elif objectCode[-2:-1] == 'B':
                bldgWidth = 15.0
            elif objectCode[-2:-1] == 'C':
                bldgWidth = 20.0
        return bldgWidth

    def calcLongStreetLength(self, bldgs):
        streetLength = 0
        for bldg in bldgs:
            streetLength += self.getBuildingWidth(bldg)
        return streetLength

    def addStreetUnits(self, streetLength):
        base.direct.grid.setPosHpr(0, -40, 0, 0, 0, 0)
        currLength = 0
        while (currLength < streetLength):
            self.editor.objectMgr.addNewObject(self.editor.currHoodId + '_80x40')
            currLength += 80

    def onMakeLongStreet(self, evt):
        bldgGroup = self.consolidateStreetBuildings()
        bldgs = bldgGroup.getChildren()
        numBldgs = len(bldgs)
        streetLength = self.calcLongStreetLength(bldgs)/2.0
        ref = None
        base.direct.grid.fXyzSnap = 0
        currLength = 0
        for i in range(numBldgs):
            bldg = bldgs[i]
            if ref == None:
                base.direct.grid.iPosHpr(bldgGroup)
            else:
                ref.select()
                #self.editor.autoPositionGrid(fLerp = 0)
            if base.direct.grid.getX() >= streetLength:
                base.direct.grid.setPosHpr(base.direct.grid, 0, -40, 0, 180, 0, 0)
            bldg.iPosHpr(base.direct.grid)
            self.editor.updateSelectedPose([bldg])
            self.editor.adjustPropChildren(bldg)
            ref = bldg
        self.addStreetUnits(streetLength)

    def drawSuitEdge(self, edge, parent):
        # Draw a line from start to end
        edgeLine = LineNodePath(parent)
        edgeLine.lineNode.setName('suitEdge')
        edgeLine.setColor(VBase4(0.0, 0.0, 0.5, 1))
        edgeLine.setThickness(1)
        edgeLine.reset()
        # We need to draw the arrow relative to the parent, but the
        # point positions are relative to the NPToplevel. So get the
        # start and end positions relative to the parent, then draw
        # the arrow using those points
        tempNode = self.editor.NPToplevel.attachNewNode('tempNode')
        mat = self.editor.NPToplevel.getMat(parent)
        relStartPos = Point3(mat.xformPoint(edge.getStartPoint().getPos()))
        relEndPos = Point3(mat.xformPoint(edge.getEndPoint().getPos()))
        # Compute offset: a vector rotated 90 degrees clockwise
        offset = Vec3(relEndPos - relStartPos)
        offset.normalize()
        offset *= 0.1
        a = offset[0]
        offset.setX(offset[1])
        offset.setY(-1 * a)
        # Just to get it above the street
        offset.setZ(0.05)
        # Add offset to start and end to help differentiate lines
        relStartPos += offset
        relEndPos += offset
        # Draw arrow
        edgeLine.drawArrow(relStartPos,
                           relEndPos,
                           15, # arrow angle
                           1) # arrow length
        edgeLine.create()
        # Add a clickable sphere
        marker = self.suitPointMarker.copyTo(edgeLine)
        marker.setName('suitEdgeMarker')
        midPos = (relStartPos + relEndPos)/2.0
        marker.setPos(midPos)
        # Adjust color of highlighted lines
        if edge in self.visitedEdges:
            NodePath.setColor(edgeLine, 1, 0, 0, 1)
        # Clean up:
        tempNode.removeNode()
        return edgeLine

    def drawSuitPoint(self, suitPoint, pos, type, parent):
        marker = self.suitPointMarker.copyTo(parent)
        marker.setName("suitPointMarker")
        marker.setPos(pos)
        if (type == DNASuitPoint.STREETPOINT):
            marker.setColor(0, 0, 0.6)
            marker.setScale(0.4)
        elif (type == DNASuitPoint.FRONTDOORPOINT):
            marker.setColor(0, 0, 1)
            marker.setScale(0.5)
        elif (type == DNASuitPoint.SIDEDOORPOINT):
            marker.setColor(0, 0.6, 0.2)
            marker.setScale(0.5)
        # Highlight if necessary
        if suitPoint in self.visitedPoints:
            marker.setColor(1, 0, 0, 1)
        return marker

    def resetPathMarkers(self):
        for edge, edgeLine in self.edgeDict.items():
            if not edgeLine.isEmpty():
                edgeLine.reset()
                edgeLine.removeNode()
        self.edgeDict = {}
        self.np2EdgeDict = {}
        for point, marker in self.pointDict.items():
            if not marker.isEmpty():
                marker.removeNode()
        self.pointDict = {}
        self.point2edgeDict = {}

    def populateSuitPaths(self):
        # Points
        numPoints = DNASTORE.getNumSuitPoints()
        for i in range(numPoints):
            point = DNASTORE.getSuitPointAtIndex(i)
            marker = self.drawSuitPoint(point,
                point.getPos(), point.getPointType(),
                self.editor.suitPointToplevel)
            self.pointDict[point] = marker

        # Edges
        visGroups = self.editor.getDNAVisGroups(self.editor.NPToplevel)
        for visGroup in visGroups:
            np = visGroup[0]
            dnaVisGroup = visGroup[1]
            numSuitEdges = dnaVisGroup.getNumSuitEdges()
            for i in range(numSuitEdges):
                edge = dnaVisGroup.getSuitEdge(i)
                edgeLine = self.drawSuitEdge(edge, np)
                self.edgeDict[edge] = edgeLine
                self.np2EdgeDict[edgeLine.id()] = [edge, dnaVisGroup]
                # Store the edge on each point in case we move the point
                # we can update the edge
                for point in [edge.getStartPoint(), edge.getEndPoint()]:
                    if self.point2edgeDict.has_key(point):
                        self.point2edgeDict[point].append(edge)
                    else:
                        self.point2edgeDict[point] = [edge]
