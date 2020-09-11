""" In-Game Editor/Control Panel module """
from pandac.PandaModules import Point3, Vec3, VBase3
from direct.tkwidgets.AppShell import *
from direct.showbase.TkGlobal import *
from direct.tkwidgets.Tree import *
from direct.tkwidgets import Slider, Floater
from tkSimpleDialog import askstring
from tkMessageBox import showwarning, askyesno
from Tkinter import *
from direct.showbase.PythonUtil import Functor, list2dict
from direct.gui.DirectGui import DGG
import tkFileDialog
from direct.showbase import DirectObject
import math
import operator
from direct.tkwidgets import Valuator
from direct.tkwidgets import VectorWidgets
from otp.level import LevelConstants
from direct.directtools import DirectSession
import types
import Pmw

class InGameEditor(AppShell):
    # Override class variables
    appname = 'In-Game Editor'
    frameWidth  = 900
    frameHeight = 475
    usecommandarea = 1
    usestatusarea  = 1
    contactname = 'Darren Ranalli'
    contactphone = '(818) 623-3904'
    contactemail = "darren.ranalli@disney.com"

    WantUndo = False

    def __init__(self, level, doneEvent, requestSaveEvent,
                 saveAsEvent, undoEvent, redoEvent,
                 wireframeEvent, oobeEvent, csEvent,
                 runEvent, texEvent,
                 **kw):
        DGG.INITOPT = Pmw.INITOPT
        optiondefs = (
            ('title',  'In-Game ' + level.getName() + ' Editor',        None),
            )
        self.defineoptions(kw, optiondefs)

        self.level = level
        self.doneEvent = doneEvent
        self.requestSaveEvent = requestSaveEvent
        self.saveAsEvent = saveAsEvent
        self.undoEvent = undoEvent
        self.redoEvent = redoEvent
        self.wireframeEvent = wireframeEvent
        self.oobeEvent = oobeEvent
        self.csEvent = csEvent
        self.runEvent = runEvent
        self.texEvent = texEvent
        self.entityCopy = None
        self.curEntId = None
        self.curEntWidgets = {}
        self.visZonesEditor = None

        AppShell.__init__(self)

        self.initialiseoptions(self.__class__)

        self.accept(self.level.getAttribChangeEventName(),
                    self.handleAttribChange)
        self.accept('DIRECT_selectedNodePath', self.selectedNodePathHook)
        self.accept('DIRECT_manipulateObjectCleanup', self.manipCleanupHook)
        self.accept('DIRECT_undo', self.manipCleanupHook)
        self.accept('DIRECT_redo', self.manipCleanupHook)

    def getEventMsgName(self, event):
        return 'InGameEditor%s_%s' % (self.level.getLevelId(), event)

    def getEntityName(self, entId):
        return self.level.levelSpec.getEntitySpec(entId)['name']
        
    def appInit(self):
        # Initialize any instance variables you use here
        from direct.directtools import DirectSession
        direct.enableLight()
        # DIRECT disabled by default, so we don't accidentally move geometry
        direct.disable()
        # make sure DIRECT stays off
        bboard.post(DirectSession.DirectSession.DIRECTdisablePost)

    def createMenuBar(self):
        menuBar = self.menuBar
        # FILE
        # add file entries before calling down, since we can't control order
        menuBar.addmenuitem('File', 'command',
                            'Save the level spec on the AI',
                            label = 'Save on AI',
                            command = self.handleRequestSave)
        menuBar.addmenuitem('File', 'command',
                            'Save the level spec locally',
                            label = 'Save Locally As...',
                            command = self.handleSaveAs)

        menuBar.addmenuitem('File', 'separator')

        menuBar.addmenuitem('File', 'command',
                            'Export a single entity',
                            label = 'Export Entity...',
                            command = self.level.handleExportEntity)
        menuBar.addmenuitem('File', 'command',
                            'Export a tree of entities',
                            label = 'Export Entity Tree...',
                            command = self.level.handleExportEntityTree)

        menuBar.addmenuitem('File', 'separator')

        menuBar.addmenuitem('File', 'command',
                            'Import a tree of entities',
                            label = 'Import Entities...',
                            command = self.level.handleImportEntities)

        menuBar.addmenuitem('File', 'separator')

        if InGameEditor.WantUndo:
            # EDIT
            menuBar.addmenu('Edit', 'Edit Operations')
            menuBar.addmenuitem('Edit', 'command',
                                'Undo the last edit',
                                label = 'Undo',
                                command = self.doUndo)
            menuBar.addmenuitem('Edit', 'command',
                                'Redo the last undo',
                                label = 'Redo',
                                command = self.doRedo)

        # ENTITY
        menuBar.addmenu('Entity', 'Entity Operations')

        # To get this menubar entry's index:
        # self.menuBar.component('Entity-menu').index('Remove Selected Entity')
        # To disable this entry (index 0)
        # self.menuBar.component('Entity-menu').entryconfigure(0,state='disabled')
        
        menuBar.addmenuitem('Entity', 'command',
                            'Duplicate Selected Entity',
                            label = 'Duplicate Selected Entity',
                            command = self.level.duplicateSelectedEntity)

        menuBar.addmenuitem('Entity', 'separator')

        # add the 'insert' entries -- this should be a single entry that opens
        # a choice dialog with a list of entity types, or something
        permanentTypes = self.level.entTypeReg.getPermanentTypeNames()
        entTypes = list(self.level.entTypes)
        map(entTypes.remove, permanentTypes)
        entTypes.sort()
        numEntities = len(entTypes)
        cascadeMenu = ''
        for index in range(numEntities):
            type = entTypes[index]
            if (index % 10) == 0:
                lastIndex = min(index + 9, numEntities - 1)
                cascadeMenu = '%s->%s' % (entTypes[index],entTypes[lastIndex])
                menuBar.addcascademenu('Entity', cascadeMenu)

            # permanent entity types cannot be inserted or removed
            def doInsert(self=self, type=type):
                self.level.insertEntity(type)
                self.explorer.update(fUseCachedChildren = 0)
            menuBar.addmenuitem(cascadeMenu, 'command',
                                'Insert %s' % type,
                                label = 'Insert %s' % type,
                                command = doInsert)

        menuBar.addmenuitem('Entity', 'separator')

        menuBar.addmenuitem('Entity', 'command',
                            'Remove Selected Entity',
                            label = 'Remove Selected Entity',
                            command = self.removeSelectedEntity)
        menuBar.addmenuitem('Entity', 'command',
                            'Remove Selected EntityTree',
                            label = 'Remove Selected Entity Tree',
                            command = self.removeSelectedEntityTree)

        menuBar.addmenuitem('Entity', 'separator')

        menuBar.addmenuitem('Entity', 'command',
                            'Go To Selected Entity',
                            label = 'Go To Selected Entity',
                            command = self.level.moveAvToSelected)

        menuBar.addmenuitem('Entity', 'command',
                            'Refresh Entity Explorer',
                            label = 'Refresh Entity Explorer',
                            command = self.refreshExplorer)

        # Add placer commands to menubar
        self.menuBar.addmenu('DIRECT', 'Direct Session Panel Operations')

        self.menuBar.addmenuitem('DIRECT', 'checkbutton',
                                 'DIRECT Enabled',
                                 label = 'Enable',
                                 variable = direct.panel.directEnabled,
                                 command = direct.panel.toggleDirect)
        
        self.menuBar.addmenuitem('DIRECT', 'checkbutton',
                                 'DIRECT Grid Enabled',
                                 label = 'Enable Grid',
                                 variable = direct.panel.directGridEnabled,
                                 command = direct.panel.toggleDirectGrid)

        self.menuBar.addmenuitem('DIRECT', 'command',
                                 'Toggle Object Handles Visability',
                                 label = 'Toggle Widget Viz',
                                 command = direct.toggleWidgetVis)

        self.menuBar.addmenuitem(
            'DIRECT', 'command',
            'Toggle Widget Move/COA Mode',
            label = 'Toggle Widget Mode',
            command = direct.manipulationControl.toggleObjectHandlesMode)
        
        self.menuBar.addmenuitem('DIRECT', 'checkbutton',
                                 'DIRECT Widget On Top',
                                 label = 'Widget On Top',
                                 variable = direct.panel.directWidgetOnTop,
                                 command = direct.panel.toggleWidgetOnTop)

        self.menuBar.addmenuitem('DIRECT', 'command',
                                 'Deselect All',
                                 label = 'Deselect All',
                                 command = direct.deselectAll)

        if InGameEditor.WantUndo:
            # Get a handle to the menu frame
            undoFrame = Frame(self.menuFrame)
            # Add buttons
            self.redoButton = Button(undoFrame, text = 'Redo',
                                     command = self.doRedo)
            self.redoButton.pack(side = RIGHT, expand = 0)
            self.undoButton = Button(undoFrame, text = 'Undo',
                                     command = self.doUndo)
            self.undoButton.pack(side = RIGHT, expand = 0)
            undoFrame.pack(side = RIGHT, expand = 0)

        # TODO: put these buttons in their own frame, with padx, so that
        # there's some space between the rightmost button and the undo/redo
        # buttons, but no space between the buttons within the frame.
        toggleFrame = Frame(self.menuFrame)
        self.wireframeButton = Button(toggleFrame, text = 'Wire',
                                      command = self.doWireframe)
        self.wireframeButton.pack(side = RIGHT, expand = 0)
        self.texButton = Button(toggleFrame, text = 'Tex',
                                command = self.doTex)
        self.texButton.pack(side = RIGHT, expand = 0)
        self.csButton = Button(toggleFrame, text = 'Cs',
                                 command = self.doCs)
        self.csButton.pack(side = RIGHT, expand = 0)
        self.runButton = Button(toggleFrame, text = 'Run',
                                command = self.doRun)
        self.runButton.pack(side = RIGHT, expand = 0)
        self.oobeButton = Button(toggleFrame, text = 'Oobe',
                                 command = self.doOobe)
        self.oobeButton.pack(side = RIGHT, expand = 0)
        toggleFrame.pack(side=RIGHT, expand=0, padx=5)

        AppShell.createMenuBar(self)

    def createInterface(self):
        # Create the tk components
        interior = self.interior()

        # Paned widget for dividing two halves
        mainFrame = Frame(interior)
        self.framePane = Pmw.PanedWidget(mainFrame, orient = DGG.HORIZONTAL)
        self.explorerFrame = self.framePane.add('left', min = 250)
        self.widgetFrame = self.framePane.add('right', min = 300)

        self.explorer = LevelExplorer(parent = self.explorerFrame,
                                      editor = self)
        self.explorer.pack(fill = BOTH, expand = 1)
        self.explorerFrame.pack(fill = BOTH, expand = 1)

        self.pageOneFrame = Pmw.ScrolledFrame(self.widgetFrame,
                                              borderframe_relief = GROOVE,
                                              horizflex = 'elastic')
        self.pageOneFrame.pack(expand = 1, fill = BOTH)

        self.widgetFrame.pack(fill = BOTH, expand = 1)

        self.framePane.pack(fill = BOTH, expand = 1)

        mainFrame.pack(fill = BOTH, expand = 1)

        self.createButtons()

        self.initialiseoptions(self.__class__)

        self.attribWidgets = []

    def selectedNodePathHook(self, nodePath):
        np = nodePath.findNetTag('entity')
        if not np.isEmpty():
            if np.id() != nodePath.id():
                np.select()
            else:
                self.findEntityFromNP(np)

    def findEntityFromNP(self, nodePath):
        # Get a list of all current selectable (i.e. nodepath) entities
        entId = self.level.nodePathId2EntId.get(nodePath.id())
        if entId:
            # Got one, find corresponding TreeNode in Level explorer
            self.selectEntity(entId)
        else:
            # this may be a distributed entity that's not in our lookup
            # table; for now, do a linear search
            for entId in self.level.levelSpec.getAllEntIds():
                np = self.level.getEntInstanceNP(entId)
                if np:
                    if np.id() == nodePath.id():
                        self.selectEntity(entId)
                        return

    def manipCleanupHook(self, nodePathList):
        # Get entId based on nodePath ID of first nodepath in list
        if not nodePathList:
            return
        entId = self.level.nodePathId2EntId.get(nodePathList[0].id())
        if entId:
            t = nodePathList[0].getTransform()
            entSpec = self.level.levelSpec.getEntitySpec(entId)
            # Make sure we make copies of these tform values
            entPos = entSpec.get('pos')
            if entPos and (t.getPos() != entPos):
                self.level.setAttribEdit(entId, 'pos',
                                           Point3(t.getPos()))
            entHpr = entSpec.get('hpr')
            if entHpr and (t.getHpr() != entHpr):
                self.level.setAttribEdit(entId, 'hpr',
                                           Vec3(t.getHpr()))
            entScale = entSpec.get('scale')
            if entScale and (t.getScale() != entScale):
                self.level.setAttribEdit(entId, 'scale',
                                           Vec3(t.getScale()))

    def refreshExplorer(self):
        """ refreshes entity explorer """
        self.explorer.update()

    def selectEntity(self, entId):
        """ show and select the entity in the tree view"""
        node = self.explorer._node.find(entId)
        if node:
            # Make sure you can see this tree item
            node.reveal()
            # Clear out previously selected items
            self.explorer._node.deselecttree()
            # Select current item
            node.select()

    def removeSelectedEntity(self):
        if self.level.selectedEntity:
            parentEntId = self.level.selectedEntity.parentEntId
        else:
            parentEntId = None
        if self.level.removeSelectedEntity() != -1:
            self.explorer.update(fUseCachedChildren = 0)
            if parentEntId:
                self.selectEntity(parentEntId)
        
    def removeSelectedEntityTree(self):
        if self.level.selectedEntity:
            parentEntId = self.level.selectedEntity.parentEntId
        else:
            parentEntId = None
        if self.level.removeSelectedEntityTree() != -1:
            self.explorer.update(fUseCachedChildren = 0)
            if parentEntId:
                self.selectEntity(parentEntId)
        
    def clearAttribEditPane(self):
        for widg in self.attribWidgets:
            widg.destroy()
        if self.visZonesEditor:
            self.visZonesEditor.destroy()
        self.attribWidgets = []
        self.curEntId = None
        self.curEntWidgets = {}
        self.cbDict = {}

    def updateEntityCopy(self, entId):
        if self.entityCopy == None:
            self.entityCopy = self.level.getEntInstanceNPCopy(
                entId)
            if self.entityCopy is not None:
                self.entityCopy.setRenderModeWireframe()
                self.entityCopy.setTextureOff(1)
                self.entityCopy.setColor(1,0,0)
                
    def updateAttribEditPane(self, entId, levelSpec, entTypeReg):
        self.clearAttribEditPane()

        self.curEntId = entId
        widgetSetter = None

        entSpec = levelSpec.getEntitySpec(entId)
        assert entSpec.has_key('type')
        typeDesc = entTypeReg.getTypeDesc(entSpec['type'])
        attribNames = typeDesc.getAttribNames()
        attribDescs = typeDesc.getAttribDescDict()

        for attribName in attribNames:
            desc = attribDescs[attribName]
            params = desc.getParams()
            datatype = desc.getDatatype()
            if datatype == 'int':
                self.addIntWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'float':
                self.addFloatWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'bool':
                self.addBoolWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'choice':
                self.addChoiceWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'multiChoice':
                self.addMultiChoiceWidget(levelSpec,entSpec,entId,
                                          attribName,params)
            elif datatype in ['pos', 'hpr', 'scale']:
                self.addVec3Widget(levelSpec,entSpec,entId,attribName,
                                   params, datatype)
            elif datatype == 'color':
                self.addColorWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'bamfilename':
                self.addFileWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'visZoneList':
                self.addVisZoneWidget(
                    levelSpec, entSpec, entId, attribName, params)
            elif datatype == 'entId':
                self.addEntIdWidget(levelSpec,entSpec,entId,attribName,params,
                                    entTypeReg)
            elif datatype == 'string':
                self.addStringWidget(levelSpec,entSpec,entId,attribName,params)
            elif datatype == 'const':
                self.addConstWidget(levelSpec,entSpec,entId,attribName,params)
            else:
                self.addPythonWidget(levelSpec,entSpec,entId,attribName,params)

    def addIntWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Check for min/max values
        minVal = params.get('min', None)
        maxVal = params.get('max', None)
        # If min and max specified, use a slider, else a floater
        if (minVal is not None) and (maxVal is not None):
            widgClass = Slider.Slider
        else:
            widgClass = Floater.Floater
        # Create the appropriate widget
        widg = widgClass(self.pageOneFrame.interior(),
                         text = attribName,
                         value = entSpec[attribName],
                         numDigits = 0,
                         label_width = 15,
                         label_anchor = W,
                         label_justify = LEFT,
                         label_font = None,
                         min = minVal, max = maxVal,
                         resolution = 1.0)
        def clientIntCommand(val):
            entity = self.level.getEntInstance(entId)
            if entity:
                entity.handleAttribChange(attribName,int(val))
        def finalIntCommand():
            self.level.setAttribEdit(entId, attribName, int(widg.get()))
        widg['command'] = clientIntCommand
        widg['postCallback'] = finalIntCommand
        widg.pack(fill = X, expand = 1)
        self.attribWidgets.append(widg)
        # Add setter for undo/redo
        self.curEntWidgets[attribName] = lambda x: widg.set(x, 0)
        
    def addFloatWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Check for min/max values
        minVal = params.get('min', None)
        maxVal = params.get('max', None)
        # Create widget
        widg = Floater.Floater(self.pageOneFrame.interior(),
                               text = attribName,
                               value = entSpec[attribName],
                               label_width = 15,
                               label_anchor = W,
                               label_justify = LEFT,
                               label_font = None,
                               min = minVal, max = maxVal)
        def clientFloatCommand(val):
            entity = self.level.getEntInstance(entId)
            if entity:
                entity.handleAttribChange(attribName, val)
        def finalFloatCommand():
            self.level.setAttribEdit(entId, attribName, widg.get())
        widg['command'] = clientFloatCommand
        widg['postCallback'] = finalFloatCommand
        widg.pack(fill = X, expand = 1)
        self.attribWidgets.append(widg)        
        # Add setter for undo/redo
        self.curEntWidgets[attribName] = lambda x: widg.set(x, 0)

    def addBoolWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Create boolean variable to store current value
        flag = BooleanVar()
        flag.set(entSpec[attribName])
        # Create command which uses this variable
        def booleanCommand(booleanVar = flag):
            self.level.setAttribEdit(entId, attribName, flag.get())
        # Create widgets
        frame = Frame(self.pageOneFrame.interior())
        label = Label(frame, text = attribName,
                      width = 15, anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        trueButton = Radiobutton(
            frame,
            text = 'True',
            value = 1,
            variable = flag,
            command = booleanCommand)
        trueButton.pack(side = LEFT, expand = 0)
        falseButton = Radiobutton(
            frame,
            text = 'False',
            value = 0,
            variable = flag,
            command = booleanCommand)
        falseButton.pack(side = LEFT, expand = 0)
        frame.pack(fill = X, expand = 1)
        self.attribWidgets.append(frame)
        # Use set function of Tkinter variable
        self.curEntWidgets[attribName] = flag.set

    def addChoiceWidget(self, levelSpec, entSpec, entId, attribName, params):
        # See if value needs to be converted
        # if not in value dict, use current value
        if attribName in entSpec:
            attributeValue = entSpec.get(attribName)
        else:
            typeDesc = self.level.entTypeReg.getTypeDesc(entSpec['type'])
            attribDesc = typeDesc.getAttribDescDict()[attribName]
            attributeValue = attribDesc.getDefaultValue()
        valueDict = params.get('valueDict', {})
        for key,value in valueDict.items():
            if value == attributeValue:
                attributeValue = key
                break
        # Tkinter value to hold current choice
        radioVar = StringVar()
        radioVar.set(attributeValue)
        # Command to update level based upon current radio button value
        def radioCommand(radioVar = radioVar):
            # Use value dict to translate current value
            # If entry not found, just use current value
            value = valueDict.get(radioVar.get(), radioVar.get())
            self.level.setAttribEdit(entId, attribName, value)
        frame = Frame(self.pageOneFrame.interior(),
                      relief = GROOVE, borderwidth = 2)
        # Create label
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        # Add radio buttons
        for choice in params.get('choiceSet', []):
            if type(choice) is types.StringType:
                choiceStr = choice
            else:
                choiceStr = `choice`
            # Store desired value by string repr (since that's what
            # we'll get back from the radio button command
            if choiceStr not in valueDict:

                valueDict[choiceStr] = choice
            choiceButton = Radiobutton(
                frame,
                text = choiceStr,
                value = choiceStr,
                variable = radioVar,
                command = radioCommand)
            choiceButton.pack(side = LEFT, expand = 0)
        frame.pack(fill = X, expand = 1)
        self.attribWidgets.append(frame)
        # Update Tkinter variable on edits and undo/redo
        def setRadioVar(attributeValue):
            for key,value in valueDict.items():
                if value == attributeValue:
                    attributeValue = key
                    break
            radioVar.set(attributeValue)
        self.curEntWidgets[attribName] = setRadioVar

    def addMultiChoiceWidget(self,levelSpec,entSpec,entId,attribName,params):
        # Set up frame and label
        frame = Frame(self.pageOneFrame.interior(),
                      relief = GROOVE, borderwidth = 2)
        # Create label
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        # Add check buttons
        valueDict = params.get('valueDict', {})
        self.cbDict[attribName] = list2dict(entSpec[attribName], value = 1)
        checkbuttonDict = {}
        base.cbButtons = []
        base.checkbuttonDict = checkbuttonDict
        for choice in params.get('choiceSet', []):
            # See if this translates into a something else
            # otherwise use value of choice as actual value
            trueValue = valueDict.get(choice, choice)
            # Tkinter value to hold current choice
            cbVar = IntVar()
            cbVar.set(trueValue in self.cbDict[attribName])
            checkbuttonDict[trueValue] = cbVar
            # Command to update level based upon current radio button value
            def cbCommand(var, trueValue=trueValue):
                vd = self.cbDict[attribName]
                print vd
                # Use value dict to translate current value
                # If entry not found, just use current value
                if var.get():
                    print 'got it', trueValue, vd
                    vd[trueValue] = 1
                else:
                    print 'not it', trueValue, vd
                    if trueValue in vd:
                        del vd[trueValue]
                value = vd.keys()
                print 'SENDING', value
                self.level.setAttribEdit(entId, attribName, value)
            # Create check button
            if type(choice) is types.StringType:
                labelStr = choice
            else:
                labelStr = `choice`
            func = Functor(cbCommand, cbVar)
            choiceButton = Checkbutton(
                frame,
                text = labelStr,
                variable = cbVar,
                command = lambda: func())
            choiceButton.pack(side = LEFT, expand = 0)
            base.cbButtons.append(choiceButton)
        frame.pack(fill = X, expand = 1)
        self.attribWidgets.append(frame)
        # Update Tkinter variable on edits and undo/redo
        def setCheckbuttonVar(attributeValueList):
            print 'COMING BACK', attributeValueList
            for attributeValue, cb in checkbuttonDict.items():
                if attributeValue in attributeValueList:
                    cb.set(1)
                else:
                    cb.set(0)
        self.curEntWidgets[attribName] = setCheckbuttonVar

    def addVec3Widget(self,levelSpec,entSpec,entId,attribName,params,datatype):
        def veCommand(poslist):
            self.level.setAttribEdit(entId, attribName, Point3(*poslist))
        # Create vector from current value
        vec = entSpec[attribName]
        if not isinstance(vec, VBase3):
            vec = Vec3(vec)
        # Compute some defaults for the widgets
        value = [vec[0],vec[1],vec[2]]
        minVal = maxVal = None            
        if datatype == 'pos':
            floaterLabels = ['x','y','z']
            floaterType = 'floater'
        elif datatype == 'hpr':
            floaterLabels = ['h','p','r']
            floaterType = 'angledial'
        else:
            floaterLabels = ['sx','sy','sz']
            floaterType = 'slider'
            minVal = 0
            maxVal = 1000
        # Create the vector entry widgets with appropriate popups
        widg = VectorWidgets.VectorEntry(
            self.pageOneFrame.interior(),
            text = attribName, value = value,
            type = floaterType, bd = 0, relief = None,
            min = minVal, max = maxVal, label_justify = LEFT,
            label_anchor = W, label_width = 14, label_bd = 0,
            labelIpadx = 0, floaterGroup_labels = floaterLabels)
        widg['command'] = veCommand
        widg.pack(fill = X, expand = 1)
        if attribName in ('pos', 'hpr', 'scale'):
            def placeEntity():
                selectedEntityNP = self.level.getEntInstanceNP(entId)
                if selectedEntityNP is not None:
                    selectedEntityNP.place()
            widg.menu.add_command(label = 'Place...', command = placeEntity)
        # Method to move a copy of the selected entity during interaction
        def adjustCopy(vec):
            self.updateEntityCopy(entId)
            if self.entityCopy is not None:
                if datatype == 'pos':
                    self.entityCopy.setPos(vec[0], vec[1], vec[2])
                elif datatype == 'hpr':
                    self.entityCopy.setHpr(vec[0], vec[1], vec[2])
                elif datatype == 'scale':
                    self.entityCopy.setScale(vec[0], vec[1], vec[2])
            widg.set(vec,0)
        widg._floaters['command'] = adjustCopy
        # A method to call final command at the end of slider interaction
        widg._floaters.component('valuatorGroup')['postCallback'] = (
            lambda x,y,z: veCommand([x,y,z]))
        # Record widget and undo/redo function
        self.attribWidgets.append(widg)
        self.curEntWidgets[attribName] = lambda x: widg.set(x, 0)

    def addColorWidget(self, levelSpec, entSpec, entId, attribName, params):
        def veCommand(colorlist):
            self.level.setAttribEdit(entId, attribName,
                                       Vec4(*colorlist)/255.0)
        # Initialize value
        vec = entSpec[attribName]
        value = [vec[0] * 255.0,vec[1] * 255.0,vec[2] * 255.0,vec[3] * 255.0]
        # Create Color Entry
        floaterLabels = ['r','g','b','a']
        widg = VectorWidgets.ColorEntry(
            self.pageOneFrame.interior(), text = attribName,
            type = 'slider', relief = None, bd = 0,
            label_justify = LEFT, label_anchor = W, label_width = 14,
            label_bd = 0, labelIpadx = 0, floaterGroup_labels = floaterLabels,
            value = value, floaterGroup_value = value)
        widg['command'] = veCommand
        widg.pack(fill = X, expand = 1)
        # Method to move a copy of the selected entity during interaction
        def adjustEntity(vec):
            entity = self.level.getEntInstance(entId)
            if entity is not None:
                entity.setColor(vec[0]/255.0, vec[1]/255.0,
                                vec[2]/255.0, vec[3]/255.0)
            widg.set(vec,0)
        widg._floaters['command'] = adjustEntity
        widg._floaters.component('valuatorGroup')['postCallback'] = (
            lambda x, y, z, a: veCommand([x,y,z,a]))
        # Record widget and undo/redo function
        self.attribWidgets.append(widg)
        self.curEntWidgets[attribName] = lambda x: widg.set(x * 255.0, 0)

    def addFileWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Tkinter variable to hold current filename
        text = StringVar()
        text.set(repr(entSpec[attribName]))
        # Method to handle <Return> in entry
        def handleReturn(event):
            self.handleAttributeChangeSubmit(attribName,text,entId,levelSpec)
        # Function to pop open file dialog
        def askFilename(callback = handleReturn):
            """ TODO: this is close to working right. I'd like it to open the
            last working directory if the file exists, otherwise open the
            root of $TTMODELS. Currently it starts from the root of $TTMODELS
            the first time every time."""
            if text.get() == 'None':
                initialDir = Filename.expandFrom('$TTMODELS/built/').toOsSpecific()
            else:
                initialDir = Filename.expandFrom('$TTMODELS/built/%s' % text.get()[1:-1]).toOsSpecific()
            print text, text.get()[1:-1], initialDir
            #import pdb;pdb.set_trace()
            rawFilename = askopenfilename(
                defaultextension = '*',
                initialdir = initialDir,
                filetypes = (('Bam Files', '*.bam'), ('Egg Files', '*.egg'),
                             ('Maya Binaries', '*.mb'),('All files', '*')),
                title = 'Load Model File',
                parent = self.interior())
            if rawFilename != '':
                filename = Filename.fromOsSpecific(rawFilename)
                filename.findOnSearchpath(getModelPath().getValue())
                text.set("'%s'" % `filename`)
                handleReturn(None)
        # Create widgets, label which does double duty as a button
        frame = Frame(self.pageOneFrame.interior())
        label = Button(frame, text = attribName, width = 14,
                       borderwidth = 0, anchor = W, justify = LEFT)
        label['command'] = askFilename
        label.pack(side = LEFT, expand = 0)
        # Methods to highlight label-button
        def enterWidget(event, widg = label):
            widg['background'] = '#909090'
        def leaveWidget(event, widg = label):
            widg['background'] = 'SystemButtonFace'
        label.bind('<Enter>', enterWidget)
        label.bind('<Leave>', leaveWidget)
        # Text entry to show current filename
        widg = Entry(frame, textvariable=text)
        widg.bind('<Return>', handleReturn)
        widg.pack(side = LEFT, fill = X, expand = 1)
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)
        self.curEntWidgets[attribName] = lambda x: text.set(repr(x))

    def addVisZoneWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Tkinter variable to hold current filename
        text = StringVar()
        text.set(repr(entSpec[attribName]))
        # Method to handle <Return> in entry
        def handleReturn(event):
            self.handleAttributeChangeSubmit(attribName,text,entId,levelSpec)
        def handleUpdate(visZoneList):
            self.level.setAttribEdit(entId, attribName, visZoneList)
        # Function to pop open file dialog
        def getZoneList(callback = handleReturn):
            zoneEntIds = list(self.level.entType2ids['zone'])
            # the uberZone is always visible
            zoneEntIds.remove(LevelConstants.UberZoneEntId)
            zoneEntIds.sort()
            self.visZonesEditor = LevelVisZonesEditor(
                self, entId, entSpec[attribName],
                modelZones = zoneEntIds, updateCommand = handleUpdate)
        # Create widgets, label which does double duty as a button
        frame = Frame(self.pageOneFrame.interior())
        label = Button(frame, text = attribName, width = 14,
                       borderwidth = 0, anchor = W, justify = LEFT)
        label['command'] = getZoneList
        label.pack(side = LEFT, expand = 0)
        # Methods to highlight label-button
        def enterWidget(event, widg = label):
            widg['background'] = '#909090'
        def leaveWidget(event, widg = label):
            widg['background'] = 'SystemButtonFace'
        label.bind('<Enter>', enterWidget)
        label.bind('<Leave>', leaveWidget)
        # Text entry to show current filename
        widg = Entry(frame, textvariable=text)
        widg.bind('<Return>', handleReturn)
        widg.pack(side = LEFT, fill = X, expand = 1)
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)
        def refreshWidget(visZoneList):
            text.set(repr(visZoneList))
            if self.visZonesEditor:
                self.visZonesEditor.setVisible(visZoneList)
        self.curEntWidgets[attribName] = refreshWidget

    def addEntIdWidget(self, levelSpec, entSpec, entId, attribName, params,
                       entTypeReg):
        # Tkinter variable to hold current entity id
        text = StringVar()
        text.set(repr(entSpec[attribName]))
        # Methods to handle <Return> and menu interaction
        def handleReturn(event):
            self.handleAttributeChangeSubmit(attribName,text,entId,levelSpec)
        def handleMenu(id):
            text.set(id)
            self.level.setAttribEdit(entId, attribName, id)
        # Create frame to hold label and menu
        frame = Frame(self.pageOneFrame.interior())
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        widg = Entry(frame, textvariable=text)
        widg.bind('<Return>', handleReturn)
        widg.pack(side = LEFT, fill = X, expand = 1)
        # Popup menu of possible entities
        if attribName is 'parentEntId':
            buttonText = "Reparent To"
        else:
            buttonText = "Select Entity"
        entButton = Menubutton(frame, width = 8,
                               text = buttonText,
                               relief = RAISED,
                               borderwidth = 2)
        entMenu = Menu(entButton, tearoff = 0)
        entButton['menu'] = entMenu
        entButton.pack(side = LEFT, fill = 'x', expand = 1)
        # Get list of entities to put into menu
        entType = params.get('type')
        entOutput = params.get('output')
        idDict = {}
        if entType == 'grid':
            for eType in entTypeReg.getDerivedTypeNames('grid'):
                idDict[eType] = self.level.entType2ids.get(eType, [])
        elif entType == 'nodepath':
            for eType in entTypeReg.getDerivedTypeNames('nodepath'):
                idDict[eType] = self.level.entType2ids.get(eType, [])
        elif entOutput == 'bool':
            for eType in entTypeReg.getTypeNamesFromOutputType('bool'):
                idDict[eType] = self.level.entType2ids.get(eType, [])
        else:
            for eType in self.level.entType2ids.keys():
                idDict[eType] = self.level.entType2ids.get(eType, [])
        # Now build popup menu
        typeKeys = idDict.keys()
        # Arrange according to entity type
        typeKeys.sort()
        def getChildEntIds(entity):
            entIds = []
            for child in entity.getChildren():
                entIds.append(child.entId)
                entIds.extend(getChildEntIds(child))
            return entIds
        thisEntity = self.level.getEntity(entId)
        forbiddenEntIds = [entId, thisEntity.parentEntId]
        forbiddenEntIds.extend(getChildEntIds(thisEntity))
        for eType in typeKeys:
            idList = list(idDict[eType])
            # we can't reparent to ourselves, our parent, or any of our children
            for forbiddenId in forbiddenEntIds:
                if forbiddenId in idList:
                    idList.remove(forbiddenId)
            # any ents of this type left?
            if len(idList) == 0:
                continue
            subMenu = Menu(entMenu, tearoff = 0)
            # Add a cascade menu for each entity type
            entMenu.add_cascade(label = eType, menu = subMenu)
            idList.sort()
            numIds = len(idList)
            idIndex = 0
            for id in idList:
                if (idIndex % 10) == 0:
                    # If number of ids is greater then 10, break into submenus
                    if numIds > 10:
                        m = Menu(subMenu, tearoff = 0)
                        firstId = idList[idIndex]
                        lastIndex = min(idIndex + 9, numIds - 1)
                        lastId = idList[lastIndex]
                        subMenu.add_cascade(
                            label = ('Ids %d-%d' % (firstId, lastId)),
                            menu = m)
                    else:
                        m = subMenu
                m.add_command(
                    label = '%d: %s' % (id,self.getEntityName(id)),
                    command = lambda id = id, h=handleMenu: h(id))
                idIndex += 1
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)
        self.curEntWidgets[attribName] = text.set
        
    def addStringWidget(self, levelSpec, entSpec, entId, attribName, params):
        # String widget for valid python strings
        # Tkinter variable to hold python string
        text = StringVar()
        text.set(str(entSpec[attribName]))
        # Method to evaluate when user hits <Return>
        def handleReturn(event):
            self.level.setAttribEdit(entId, attribName, text.get())
        # Create a frame to hold label and entry
        frame = Frame(self.pageOneFrame.interior())
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        widg = Entry(frame, textvariable=text)
        widg.bind('<Return>', handleReturn)
        widg.pack(side = LEFT, fill = X, expand = 1)
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)
        self.curEntWidgets[attribName] = text.set

    def addConstWidget(self, levelSpec, entSpec, entId, attribName, params):
        # Create a frame to hold label and entry
        frame = Frame(self.pageOneFrame.interior())
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        text = str(entSpec[attribName])
        valueLabel = Label(frame, text = text,
                           anchor = W, justify = LEFT,
                           relief = GROOVE
                           )
        valueLabel.pack(side = LEFT, fill = X, expand = 1)
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)

    def addPythonWidget(self, levelSpec, entSpec, entId, attribName, params):
        # String widget for valid python strings
        # Tkinter variable to hold python string
        text = StringVar()
        text.set(repr(entSpec[attribName]))
        # Method to evaluate when user hits <Return>
        def handleReturn(event):
            self.handleAttributeChangeSubmit(attribName,text,entId,levelSpec)
        # Create a frame to hold label and entry
        frame = Frame(self.pageOneFrame.interior())
        label = Label(frame, text = attribName, width = 15,
                      anchor = W, justify = LEFT)
        label.pack(side = LEFT, expand = 0)
        widg = Entry(frame, textvariable=text)
        widg.bind('<Return>', handleReturn)
        widg.pack(side = LEFT, fill = X, expand = 1)
        frame.pack(fill = X, expand = 1)
        # Record widget and undo/redo function
        self.attribWidgets.append(frame)
        self.curEntWidgets[attribName] = lambda x: text.set(repr(x))

    def handleAttributeChangeSubmit(self, attribName, textObj,
                                    entId, levelSpec):
        newText = textObj.get()
        try:
            value = eval(newText)
        except:
            showwarning('ERROR', 'that is not a valid Python object',
                        parent = self.parent)
            return
        # request the new value
        self.level.setAttribEdit(entId, attribName, value)

    def handleAttribChange(self, entId, attribName, value, username):
        # the editor just got notified of an official attribute change
        if username == self.level.editUsername:
            if self.entityCopy:
                self.entityCopy.removeNode()
                self.entityCopy = None
        if entId == self.curEntId:
            widgetSetter = self.curEntWidgets[attribName]
            if widgetSetter is not None:
                widgetSetter(value)

    def createButtons(self):
        """
        self.buttonAdd('Reset Level',
                       helpMessage='Reset the level',
                       statusMessage='Resets the level',
                       command=self.resetLevel)
                       """
        pass

    def toggleBalloon(self):
        # 'balloon' shows balloon help
        # 'status' shows status bar
        # 'both' shows in both places
        # 'none' shows nothing
        if self.toggleBalloonVar.get():
            self.balloon().configure(state = 'both')
        else:
            self.balloon().configure(state = 'none')
            
    def onDestroy(self, event):
        """ Called on Level Panel shutdown """
        from direct.directtools import DirectSession
        direct.disable()
        bboard.remove(DirectSession.DirectSession.DIRECTdisablePost)
        self.ignore(self.level.getAttribChangeEventName())
        self.ignore('DIRECT_selectedNodePath')
        self.ignore('DIRECT_manipulateObjectCleanup')
        self.ignore('DIRECT_undo')
        self.ignore('DIRECT_redo')
        print 'InGameEditor.onDestroy()'
        if self.visZonesEditor:
            self.visZonesEditor.destroy()
        self.explorer._node.destroy()
        del self.level
        messenger.send(self.doneEvent)

    def handleRequestSave(self):
        messenger.send(self.requestSaveEvent)

    def handleSaveAs(self):
        # error if we set parent=self
        filename = tkFileDialog.asksaveasfilename(
            parent=self.parent,
            defaultextension='.py',
            filetypes=[('Python Source Files', '.py'),
                       ('All Files', '*'),
                       ],
            )
        if len(filename) > 0:
            messenger.send(self.saveAsEvent, [filename])

    def doUndo(self):
        messenger.send(self.undoEvent)
    def doRedo(self):
        messenger.send(self.redoEvent)
    def doWireframe(self):
        messenger.send(self.wireframeEvent)
    def doOobe(self):
        messenger.send(self.oobeEvent)
    def doCs(self):
        messenger.send(self.csEvent)
    def doRun(self):
        messenger.send(self.runEvent)
    def doTex(self):
        messenger.send(self.texEvent)

    def resetLevel(self):
        self.showTodo(what='resetLevel')
        
    def showTodo(self, what=''):
        self.showWarning('%s\nThis is not yet implemented.' % what,
                         'TODO')

    def showWarning(self, msg, title='Warning'):
        showwarning(title, msg, parent = self.parent)

    def askYesNo(self, msg, title='Query'):
        return askyesno(title, msg, parent = self.parent)

    def popupLevelDialog(self):
        data = askstring('Input Level Data', 'Level Data:',
                         parent = self)
        if data:
            self.messageBar().helpmessage(data)

class LevelVisZonesEditor(Pmw.MegaToplevel):
    def __init__(self, editor, entId, visible, modelZones = [],
                 updateCommand = None, parent = None, **kw):

        DGG.INITOPT = Pmw_INITOPT
        optiondefs = (
            ('title',       'Level Vis-Zone Editor',       None),
            )
        self.defineoptions(kw, optiondefs)

        Pmw.MegaToplevel.__init__(self, parent, title = self['title'])

        self.editor = editor
        self.entId = entId
        self.modelZones = modelZones
        self.modelZones.sort()
        self.updateCommand = updateCommand

        # Handle to the toplevels hull
        hull = self.component('hull')

        balloon = self.balloon = Pmw.Balloon(hull)
        # Start with balloon help disabled
        self.balloon.configure(state = 'none')
        
        menuFrame = Frame(hull, relief = GROOVE, bd = 2)
        menuFrame.pack(fill = X, expand = 1)

        menuBar = Pmw.MenuBar(menuFrame, hotkeys = 1, balloon = balloon)
        menuBar.pack(side = LEFT, expand = 1, fill = X)
        menuBar.addmenu('Vis Zones Editor',
                        'Visability Zones Editor Operations')
        menuBar.addmenuitem('Vis Zones Editor', 'command',
                            'Exit Visability Zones Editor',
                            label = 'Exit',
                            command = self.destroy)

        menuBar.addmenu('Help', 'Visibility Zones Editor Help Operations')
        self.toggleBalloonVar = IntVar()
        self.toggleBalloonVar.set(0)
        menuBar.addmenuitem('Help', 'checkbutton',
                            'Toggle balloon help',
                            label = 'Balloon Help',
                            variable = self.toggleBalloonVar,
                            command = self.toggleBalloon)

        # Scrolled frame to hold radio selector
        sf = Pmw.ScrolledFrame(hull, horizflex = 'elastic',
                               usehullsize = 1, hull_width = 200,
                               hull_height = 400)
        frame = sf.interior()
        sf.pack(padx=5, pady=3, fill = BOTH, expand = 1)

        # Add vis zones selector
        self.radioSelect = Pmw.RadioSelect(frame, selectmode=MULTIPLE,
                                        orient = DGG.VERTICAL,
                                        pady = 0,
                                        command = self.toggleVisZone)
        self.buttons = []
        for modelZoneNum in self.modelZones:
            buttonStr = '%d - %s' % (
                modelZoneNum,
                self.editor.getEntityName(modelZoneNum))
            button = self.radioSelect.add(buttonStr, width = 12)
            button.configure(anchor = W, justify = LEFT)
            self.buttons.append(button)
        # Pack the widget
        self.radioSelect.pack(expand = 1, fill = X)
        # And make sure scrolled frame is happy
        sf.reposition()

        buttonFrame = Frame(hull)
        self.showMode = IntVar()
        self.showMode.set(self.editor.level.level.getColorZones())
        self.showActiveButton = Radiobutton(buttonFrame,
                                            text = 'Stash Invisible',
                                            value = 0, indicatoron = 1,
                                            variable = self.showMode,
                                            command = self.setVisRenderMode)
        self.showActiveButton.pack(side = LEFT, fill = X, expand = 1)
        self.showAllButton = Radiobutton(buttonFrame,
                                         text = 'Color Invisible',
                                         value = 1, indicatoron = 1,
                                         variable = self.showMode,
                                         command = self.setVisRenderMode)
        self.showAllButton.pack(side = LEFT, fill = X, expand = 1)
        buttonFrame.pack(fill=X, expand = 1)

        # Make sure input variables processed 
        self.initialiseoptions(LevelVisZonesEditor)
        self.setVisible(visible)
        
    def toggleVisZone(self, zoneStr, state):
        zoneNum = int(zoneStr.split('-')[0])
        if state == 0:
            if zoneNum in self.visible:
                self.visible.remove(zoneNum)
        else:
            if zoneNum not in self.visible:
                self.visible.append(zoneNum)
                self.visible.sort()
        if self.updateCommand:
            self.updateCommand(self.visible)

    def setVisible(self, visible):
        self.visible = visible
        self.refreshVisibility()

    def setVisRenderMode(self):
        # Controls display of "hidden" zones
        # When show All, hidden zones will be visible and colored red
        self.editor.level.level.setColorZones(self.showMode.get())

    def refreshVisibility(self):
        # Update buttons to reflect current visibility
        # Recreate code from Pmw.RadioSelect.invoke to change
        # the state of the button.  Necessary so that we could
        # avoid invoking button's command
        self.radioSelect.selection = []
        for button in self.buttons:
            componentName = button['text']
            modelZone = int(componentName.split('-')[0])
            if modelZone in self.visible:
                button.configure(relief = 'sunken')
                self.radioSelect.selection.append(componentName)
            else:
                button.configure(relief = 'raised')

    def destroy(self):
        # Insert code you need to perform before widget destruction
        self.editor.visZonesEditor = None
        Pmw.MegaToplevel.destroy(self)

    def toggleBalloon(self):
        if self.toggleBalloonVar.get():
            self.balloon.configure(state = 'balloon')
        else:
            self.balloon.configure(state = 'none')

# changing these strings requires changing DirectSession.py Level_ strs too!
DEFAULT_MENU_ITEMS = [
    'Update Explorer',
    'Separator',
    'Select', 'Deselect', 
    'Separator',
    'Delete',
    'Separator',
    'Fit', 'Flash', 'Isolate', 'Toggle Vis', 'Show All',
    'Separator',
    'Set Reparent Target', 'Reparent', 'WRT Reparent',
    'Separator',
    'Place', 'Set Name', 'Set Color', 'Explore',
    'Separator']

class LevelExplorer(Pmw.MegaWidget, DirectObject.DirectObject):
    "Graphical display of a level's contents"
    def __init__(self, parent = None, editor = None, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('menuItems',   [],   Pmw.INITOPT),
            )
        self.defineoptions(kw, optiondefs)
 
        # Initialise superclass
        Pmw.MegaWidget.__init__(self, parent)
        
        # Initialize some class variables
        self.editor = editor

        # Create the components.
        
        # Setup up container
        interior = self.interior()
        interior.configure(relief = GROOVE, borderwidth = 2)
        
        # Create a label and an entry
        self._scrolledCanvas = self.createcomponent(
            'scrolledCanvas',
            (), None,
            Pmw.ScrolledCanvas, (interior,),
            hull_width = 300, hull_height = 80,
            usehullsize = 1)
        self._canvas = self._scrolledCanvas.component('canvas')
        self._canvas['scrollregion'] = ('0i', '0i', '2i', '4i')
        self._scrolledCanvas.resizescrollregion()
        self._scrolledCanvas.pack(padx = 3, pady = 3, expand=1, fill = BOTH)
        
        self._canvas.bind('<ButtonPress-2>', self.mouse2Down)
        self._canvas.bind('<B2-Motion>', self.mouse2Motion)
        self._canvas.bind('<Configure>',
                          lambda e, sc = self._scrolledCanvas:
                          sc.resizescrollregion())
        self.interior().bind('<Destroy>', self.onDestroy)
        
        # Create the contents
        self._treeItem = LevelExplorerItem(self.editor.level, self.editor)

        self._node = TreeNode(self._canvas, None, self._treeItem,
                              DEFAULT_MENU_ITEMS + self['menuItems'])
        self._node.expand()

        self._parentFrame = Frame(interior)

        # Add update hook
        self.accept('Level_Update Explorer',
                    lambda f, s = self: s.update())

        # Check keywords and initialise options based on input values.
        self.initialiseoptions(LevelExplorer)

    def update(self, fUseCachedChildren = 1):
        """ Refresh scene graph explorer """
        # always expand to show the UberZone
        self._node.update(fUseCachedChildren)
        self._node.expand()

    def mouse2Down(self, event):
        self._width = 1.0 * self._canvas.winfo_width()
        self._height = 1.0 * self._canvas.winfo_height()
        xview = self._canvas.xview()
        yview = self._canvas.yview()        
        self._left = xview[0]
        self._top = yview[0]
        self._dxview = xview[1] - xview[0]
        self._dyview = yview[1] - yview[0]
        self._2lx = event.x
        self._2ly = event.y

    def mouse2Motion(self,event):
        newx = self._left - ((event.x - self._2lx)/self._width) * self._dxview
        self._canvas.xview_moveto(newx)
        newy = self._top - ((event.y - self._2ly)/self._height) * self._dyview
        self._canvas.yview_moveto(newy)
        self._2lx = event.x
        self._2ly = event.y
        self._left = self._canvas.xview()[0]
        self._top = self._canvas.yview()[0]

    def onDestroy(self, event):
        # Remove hooks
        self.ignore('Level_Update Explorer')

class LevelExplorerItem(TreeItem):

    """Example TreeItem subclass -- browse the file system."""

    def __init__(self, levelElement, editor):
        self.levelElement = levelElement
        self.editor = editor

    def GetText(self):
        return self.levelElement.getName()

    def GetKey(self):
        return self.levelElement.id()

    def IsEditable(self):
        # All nodes' names can be edited nowadays.
        return 1

    def SetText(self, text):
        self.levelElement.setNewName(text)

    def GetIconName(self):
        return "sphere2" # XXX wish there was a "file" icon

    def IsExpandable(self):
        return self.levelElement.getNumChildren() != 0

    def GetSubList(self):
        sublist = []
        for element in self.levelElement.getChildren():
            item = LevelExplorerItem(element, self.editor)
            sublist.append(item)
        return sublist

    def OnSelect(self):
        messenger.send(self.editor.getEventMsgName('Select'),
                       [self.levelElement])

    def MenuCommand(self, command):
        messenger.send(self.editor.getEventMsgName(command),
                       [self.levelElement])
