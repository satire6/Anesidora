from direct.directtools.DirectSelection import *
from direct.directtools.DirectUtil import ROUND_TO
from direct.directtools.DirectGeometry import LineNodePath
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from toontown.catalog import CatalogFurnitureItem
from toontown.catalog import CatalogItemTypes
from direct.showbase import PythonUtil
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer

camPos50 = (Point3(0.00, -10.00, 50.00),
            Point3(0.00, -9.66, 49.06),
            Point3(0.00, 1.50, 12.38),
            Point3(0.00, 1.50, -3.10),
            1,
            )

camPos40 = (Point3(0.00, -15.00, 40.00),
            Point3(0.00, -14.50, 39.13),
            Point3(0.00, 1.50, 12.38),
            Point3(0.00, 1.50, -3.10),
            1,
            )

camPos30 = (Point3(0.00, -20.00, 30.00),
             Point3(0.00, -19.29, 29.29),
             Point3(0.00, 1.50, 12.38),
             Point3(0.00, 1.50, -3.10),
             1,
             )

camPos20 = (Point3(0.00, -20.00, 20.00),
            Point3(0.00, -19.13, 19.50),
            Point3(0.00, 1.50, 12.38),
            Point3(0.00, 1.50, -3.10),
            1,
            )

camPosList = [camPos20, camPos30, camPos40, camPos50]
DEFAULT_CAM_INDEX = 2

NormalPickerPanelColor = (1,0.9,0.745,1)
DisabledPickerPanelColor = (0.7, 0.65, 0.58, 1)
DeletePickerPanelColor = (1, 0.4, 0.4, 1)
DisabledDeletePickerPanelColor = (0.7, 0.3, 0.3, 1)

class FurnitureItemPanel(DirectButton):
    """

    This is a single button in the list of attic items.  It represents
    one item in the attic.
    
    """
    def __init__(self, item, itemId, command = None, deleteMode = 0,
                 withinFunc = None, helpCategory = None):
        self.item = item
        self.itemId = itemId
        self.command = command
        self.origHelpCategory = helpCategory
        self.deleteMode = deleteMode
        if self.deleteMode:
            framePanelColor = DeletePickerPanelColor
        else:
            framePanelColor = NormalPickerPanelColor
        DirectButton.__init__(self,
                              relief=DGG.RAISED,
                              frameSize = (-0.25, 0.25, -0.2, 0.2),
                              frameColor = framePanelColor,
                              borderWidth = (0.02, 0.02),
                              command = self.clicked,
                              )
        if self.deleteMode:
            # No matter what your category was going to be, you are in
            # delte mode, so your help text is regarding deletion
            helpCategory = "FurnitureItemPanelDelete"
        self.bindHelpText(helpCategory)
        if withinFunc:
            self.bind(DGG.WITHIN, lambda event: withinFunc(self.itemId))
        self.initialiseoptions(FurnitureItemPanel)
        self.load()

    def show(self):
        DirectFrame.show(self)
        if self.ival:
            # We use resume() instead of loop(), so the icon won't
            # keep resetting to the initial turning point.  Not sure
            # if this is a great idea, since the different twirling
            # icons can get out of sync this way.
            self.ival.resume()

    def hide(self):
        DirectFrame.hide(self)
        if self.ival:
            self.ival.pause()

    def load(self):
        panelWidth = 7
        panelCenter = 0
        # Some items know how to draw themselves.  Put this first so
        # it will be below any text on the frame.
        self.picture, self.ival = self.item.getPicture(base.localAvatar)
        if self.picture:
            self.picture.reparentTo(self)
            self.picture.setScale(0.14)
            self.picture.setPos(0, 0, -0.02)

            # When we have a picture, the text is short and below the
            # picture.
            text = self.item.getName()
            text_pos = (0, -0.1, 0)

        else:
            # If we don't have a picture, the text is a little longer
            # and centered.
            text = self.item.getTypeName() + ": " + self.item.getName()
            text_pos = (0, -0.3, 0)
            
        if self.ival:
            # Start it looping, but immediately pause it, so resume()
            # above will work.
            self.ival.loop()
            self.ival.pause()
        # name label
        self.nameLabel = DirectLabel(
            parent = self,
            relief = None,
            pos = (0,0,0.17),
            scale = 0.45,
            text = text,
            text_scale = 0.15,
            text_fg = (0, 0, 0, 1),
            text_pos = text_pos,
            text_font = ToontownGlobals.getInterfaceFont(),
            text_wordwrap = panelWidth,
            )
            
    def clicked(self):
        # We can't use a functor to store these two parameters,
        # because the owner of this object might directly adjust
        # self.itemId and we will want to pass in the newly modified
        # value.
        self.command(self.item, self.itemId)

    def unload(self):
        # This object doesn't necessarily 'own' the item.
        if self.item.hasPicture:
            self.item.cleanupPicture()
        del self.item
        # remove panel items
        self.nameLabel.destroy()
        del self.nameLabel
        if self.ival:
            self.ival.finish()
        del self.ival
        del self.picture
        
        self.command = None

    def destroy(self):
        # this is only so the DirectGui code cleans us up properly
        self.unload()
        # call parent destructor
        DirectButton.destroy(self)

    def bindHelpText(self, category):
        self.unbind(DGG.ENTER)
        self.unbind(DGG.EXIT)
        if category is None:
            category = self.origHelpCategory
        self.bind(DGG.ENTER, base.cr.objectManager.showHelpText, extraArgs=[category,
                                                                             self.item.getName()])
        self.bind(DGG.EXIT, base.cr.objectManager.hideHelpText)

    def setDeleteMode(self, deleteMode):
        """ Delete-mode panels are reddish. """
        self.deleteMode = deleteMode
        self.__updateAppearance()
    
    def enable(self, enabled):
        """ Disabled panels are dimmed. """
        if enabled:
            self['state'] = DGG.NORMAL
        else:
            self['state'] = DGG.DISABLED
        self.__updateAppearance()
            
    def __updateAppearance(self):
        """ Change the panel's appearance to match its disabled/delete state. """
        color = NormalPickerPanelColor
        relief = DGG.RAISED
        if self.deleteMode:
            if self['state'] == DGG.DISABLED:
                color = DisabledDeletePickerPanelColor
                relief = DGG.SUNKEN
            else:
                color = DeletePickerPanelColor
                relief = DGG.RAISED
        else:
            if self['state'] == DGG.DISABLED:
                color = DisabledPickerPanelColor
                relief = DGG.SUNKEN
            else:
                color = NormalPickerPanelColor
                relief = DGG.RAISED
        self['frameColor'] = color
        #self['relief'] = relief

class MovableObject(NodePath, DirectObject):
    def __init__(self, dfitem, parent = render):
        # Initialize the superclass
        NodePath.__init__(self)

        # Just create a movable object based upon this node path
        self.assign(dfitem)
        self.dfitem = dfitem

        # Make sure the object knows to broadcast its position based
        # on its previous parent.
        dfitem.transmitRelativeTo = dfitem.getParent()

        # And now we can reparent it at will.
        self.reparentTo(parent)
        
        # Tag this top level node as a movable object
        self.setTag('movableObject', '1')
        # Find the built in collision nodes and get rid of them before
        # computing the object's bounding box
        self.builtInCNodes = self.findAllMatches('**/+CollisionNode')
        self.numBuiltInNodes = self.builtInCNodes.getNumPaths()
        self.stashBuiltInCollisionNodes()
        # See if the object has a shadow polygon
        shadows = self.findAllMatches('**/*shadow*')
        shadows.addPathsFrom(self.findAllMatches('**/*Shadow*'))
        shadows.stash()
        
        # Init flags
        flags = self.dfitem.item.getFlags()
        if flags & CatalogFurnitureItem.FLPainting:
            self.setOnFloor(0)
            self.setOnWall(1)
        else:
            self.setOnFloor(1)
            self.setOnWall(0)

        if flags & CatalogFurnitureItem.FLOnTable:
            self.setOnTable(1)
        else:
            self.setOnTable(0)

        if flags & CatalogFurnitureItem.FLRug:
            self.setIsRug(1)
        else:
            self.setIsRug(0)

        if flags & CatalogFurnitureItem.FLIsTable:
            self.setIsTable(1)
        else:
            self.setIsTable(0)
        
        # Special case fixes
        # Compute bounding box
        m = self.getTransform()
        self.iPosHpr()
        bMin,bMax = self.bounds = self.getTightBounds()
        bMin -= Vec3(.1,.1,0)
        bMax += Vec3(.1,.1,0)
        self.c0 = Point3(bMin[0], bMin[1], 0.2)
        self.c1 = Point3(bMax[0], bMin[1], 0.2)
        self.c2 = Point3(bMax[0], bMax[1], 0.2)
        self.c3 = Point3(bMin[0], bMax[1], 0.2)
        self.center = (bMin + bMax)/2.0
        # Object drag point, center of the object, on the floor
        if flags & CatalogFurnitureItem.FLPainting:
            self.dragPoint = Vec3(self.center[0], bMax[1], self.center[2])
        else:
            self.dragPoint = Vec3(self.center[0],self.center[1], bMin[2])
        delta = self.dragPoint - self.c0
        self.radius = min(delta[0], delta[1])

        if self.getOnWall():
            self.setWallOffset(0.1)
        else:
            self.setWallOffset(self.radius + 0.1)

        # Create a bounding box for collisions during furniture arranging
        self.makeCollisionBox()
        self.setTransform(m)
        # And now restore stashed nodes
        self.unstashBuiltInCollisionNodes()
        shadows.unstash()

    def resetMovableObject(self):
        self.unstashBuiltInCollisionNodes()
        self.collisionNodePath.removeNode()
        self.clearTag('movableObject')

    def setOnFloor(self, fOnFloor):
        self.fOnFloor = fOnFloor

    def getOnFloor(self):
        return self.fOnFloor

    def setOnWall(self, fOnWall):
        self.fOnWall = fOnWall

    def getOnWall(self):
        return self.fOnWall

    def setOnTable(self, fOnTable):
        self.fOnTable = fOnTable

    def getOnTable(self):
        return self.fOnTable

    def setIsRug(self, fIsRug):
        self.fIsRug = fIsRug

    def getIsRug(self):
        return self.fIsRug

    def setIsTable(self, fIsTable):
        self.fIsTable = fIsTable

    def getIsTable(self):
        return self.fIsTable

    def setWallOffset(self, offset):
        self.wallOffset = offset

    def getWallOffset(self):
        return self.wallOffset

    def destroy(self):
        self.removeNode()

    def stashBuiltInCollisionNodes(self):
        self.builtInCNodes.stash()

    def unstashBuiltInCollisionNodes(self):
        self.builtInCNodes.unstash()

    def getFloorBitmask(self):
        # Returns a suitable bitmask to test for surfaces this object
        # may stand on.
        if self.getOnTable():
            return ToontownGlobals.FloorBitmask | ToontownGlobals.FurnitureTopBitmask
        else:
            return ToontownGlobals.FloorBitmask    

    def getWallBitmask(self):
        # Returns a suitable bitmask to test for surfaces this object
        # may not penetrate and may align itself with.
        if self.getIsRug() or self.getOnWall():
            return ToontownGlobals.WallBitmask    
        else:
            return ToontownGlobals.WallBitmask | ToontownGlobals.FurnitureSideBitmask

    def makeCollisionBox(self):
        # Make sure each object has a consistent collision box
        # Node path for holding generated collision solids
        self.collisionNodePath = self.attachNewNode('furnitureCollisionNode')
        if self.getIsRug() or self.getOnWall():
            # Rugs and paintings don't have any collision boxes.
            return
        
        # Get coords of bounding box
        mx = self.bounds[0][0] - 0.01
        Mx = self.bounds[1][0] + 0.01
        my = self.bounds[0][1] - 0.01
        My = self.bounds[1][1] + 0.01
        mz = self.bounds[0][2]
        Mz = self.bounds[1][2]
        # Make four collision polys for the side of the box
        # using the ToontownGlobals.FurnitureSideBitmask
        cn = CollisionNode('sideCollisionNode')
        cn.setIntoCollideMask(ToontownGlobals.FurnitureSideBitmask)

        self.collisionNodePath.attachNewNode(cn)
        # Min X face
        cp = CollisionPolygon(Point3(mx,My,mz),
                              Point3(mx,my,mz),
                              Point3(mx,my,Mz),
                              Point3(mx,My,Mz))
        cn.addSolid(cp)
        # Max X face
        cp = CollisionPolygon(Point3(Mx,my,mz),
                              Point3(Mx,My,mz),
                              Point3(Mx,My,Mz),
                              Point3(Mx,my,Mz))
        cn.addSolid(cp)
        # Min Y face
        cp = CollisionPolygon(Point3(mx,my,mz),
                              Point3(Mx,my,mz),
                              Point3(Mx,my,Mz),
                              Point3(mx,my,Mz))
        cn.addSolid(cp)
        # Max Y face
        cp = CollisionPolygon(Point3(Mx,My,mz),
                              Point3(mx,My,mz),
                              Point3(mx,My,Mz),
                              Point3(Mx,My,Mz))
        cn.addSolid(cp)

        if self.getIsTable():
            # Make one collision poly for the top of the box
            # using the ToontownGlobals.FurnitureTopBitmask
            cn = CollisionNode('topCollisionNode')
            cn.setIntoCollideMask(ToontownGlobals.FurnitureTopBitmask)

            self.collisionNodePath.attachNewNode(cn)
            
            # Min X face
            cp = CollisionPolygon(Point3(mx,my,Mz),
                                  Point3(Mx,my,Mz),
                                  Point3(Mx,My,Mz),
                                  Point3(mx,My,Mz))
            cn.addSolid(cp)
                
class ObjectManager(NodePath, DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("ObjectManager")

    def __init__(self):
        # Initialize the superclass and become a node path
        NodePath.__init__(self)
        self.assign(render.attachNewNode('objectManager'))
        # Dictionary to keep track of all objects placed in world
        self.objectDict = {}
        # Object currently being moved about
        self.selectedObject = None
        self.movingObject = 0
        self.deselectEvent = None
        # Some auxiliary node paths
        # Node path to record initial position each frame
        self.startPose = render.attachNewNode('startPose')
        # This is aligned with the object's drag point
        self.dragPointNP = self.attachNewNode('dragPoint')
        # This is used to offset the object to the nearest grid point
        self.gridSnapNP = self.dragPointNP.attachNewNode('gridSnap')
        # This is used to respond to collisions
        self.collisionOffsetNP = self.gridSnapNP.attachNewNode(
            'collisionResponse')
        # Selection Ray for picking objects
        self.iRay = SelectionRay()
        # Selection Segments for testing object/wall collisions
        self.iSegment = SelectionSegment(numSegments = 6)
        self.iSegment4 = SelectionSegment(numSegments = 4)
        # Selection Sphere for testing for snap to face
        self.iSphere = SelectionSphere()
        # Set top node path for collision testing and reparenting
        self.houseExtents = None
        self.doorBlocker = None
        # Collision poly used to drag objects about the house
        cp = CollisionPolygon(Point3(-100,-100,0),
                              Point3(100,-100,0),
                              Point3(100,100,0),
                              Point3(-100,100,0))

        cn = CollisionNode('dragCollisionNode')
        cn.addSolid(cp)
        cn.setIntoCollideMask(ToontownGlobals.FurnitureDragBitmask)

        self.collisionNP = NodePath(cn)
        # Create a lineNodePath for showing feedback during the move
        self.lnp = LineNodePath()
        # Flag for enabling/disabling button tracking
        self.fRecenter = 0
        self.gridSpacing = None
        self.firstTime = 0
        # Create gui for controlling selectedObject
        guiModels = loader.loadModel('phase_5.5/models/gui/house_design_gui')
        self.createSelectedObjectPanel(guiModels)
        self.createMainControls(guiModels)
        self.furnitureManager = None
        self.atticPicker = None
        self.inRoomPicker = None
        self.inTrashPicker = None
        self.dialog = None
        
        self.deleteMode = 0
        self.nonDeletableItem = None
        self.verifyFrame = None
        self.deleteItemText = None
        self.okButton = None
        self.cancelButton = None
        self.itemIval = None
        self.itemPanel = None
        self.guiInterval = None
        
        self.accept('enterFurnitureMode', self.enterFurnitureMode)
        self.accept('exitFurnitureMode', self.exitFurnitureMode)

    def enterFurnitureMode(self, furnitureManager, fDirector):
        if not fDirector:
            # For now, we ignore requests to enter furniture mode when
            # we're not the director.
            if self.furnitureManager:
                self.exitFurnitureMode(self.furnitureManager)
            return
            
        if furnitureManager == self.furnitureManager:
            # Already in furniture mode.
            return
        
        if self.furnitureManager != None:
            # In furniture mode with some other manager; reset.
            self.exitFurnitureMode(self.furnitureManager)

        self.notify.info("enterFurnitureMode, fDirector = %s" % (fDirector))

        self.furnitureManager = furnitureManager
        self.furnitureManager.d_avatarEnter()

        house = furnitureManager.getInteriorObject()
        house.hideExteriorWindows()
        self.setTargetNodePath(house.interior)
        self.createAtticPicker()
        self.initializeDistributedFurnitureItems(furnitureManager.dfitems)
        self.setCamPosIndex(DEFAULT_CAM_INDEX)
        # The AI will set our ghost mode flag on, but we'll do it
        # locally too, just to ensure it gets set promptly.
        base.localAvatar.setGhostMode(1)
        taskMgr.remove('editModeTransition')
        self.orientCamH(base.localAvatar.getH(self.targetNodePath))
        self.accept('mouse1', self.moveObjectStart)
        self.accept('mouse1-up', self.moveObjectStop)
        self.furnitureGui.show()
        self.deleteMode = 0
        self.__updateDeleteButtons()
        self.showAtticPicker()
        # Hide laff meter and scale up gui
        base.localAvatar.laffMeter.stop()
        # Disable overlapped chat cells
        base.setCellsAvailable(base.leftCells +
                                   [base.bottomCells[0]], 0)
        if self.guiInterval:
            self.guiInterval.finish()
        self.guiInterval = self.furnitureGui.posHprScaleInterval(
            1.0, Point3(-1.16,1,-0.03), Vec3(0), Vec3(0.06),
            startPos = Point3(-1.19, 1, 0.33),
            startHpr = Vec3(0),
            startScale = Vec3(0.04),
            blendType = 'easeInOut',
            name = 'lerpFurnitureButton')
        self.guiInterval.start()
        taskMgr.add(self.recenterButtonFrameTask,'recenterButtonFrameTask',10)
        messenger.send('wakeup')
        
    def exitFurnitureMode(self, furnitureManager):
        if (furnitureManager != self.furnitureManager):
            return

        self.notify.info("exitFurnitureMode")

        house = furnitureManager.getInteriorObject()
        if house:
            house.showExteriorWindows()
        self.furnitureManager.d_avatarExit()
        self.furnitureManager = None
        base.localAvatar.setCameraPositionByIndex(0)
        # The AI will set our ghost mode flag off, but we'll do it
        # locally too, just to ensure it gets set promptly.

        # On reflection, this causes problems if for some reason the
        # AI doesn't set ghost mode off.  Better not to risk getting
        # out-of-sync.
        #base.localAvatar.setGhostMode(0)

        self.exitDeleteMode()
        # Clean up temp collision solids
        self.houseExtents.detachNode()
        self.doorBlocker.detachNode()
        self.deselectObject()
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        if self.atticPicker:
            self.atticPicker.destroy()
            self.atticPicker = None
        if self.inRoomPicker:
            self.inRoomPicker.destroy()
            self.inRoomPicker = None
        if self.inTrashPicker:
            self.inTrashPicker.destroy()
            self.inTrashPicker = None
        self.__cleanupVerifyDelete()
        # Hide gui and show laff meter
        self.furnitureGui.hide()
        # Enable overlapped chat cells
        base.setCellsAvailable(base.leftCells +
                                   [base.bottomCells[0]], 1)
        base.localAvatar.laffMeter.start()
        taskMgr.remove('recenterButtonFrameTask')
        self.cleanupDialog()
        taskMgr.remove("showHelpTextDoLater")
        messenger.send('wakeup')


    def initializeDistributedFurnitureItems(self, dfitems):
        self.objectDict = {}
        for item in dfitems:
            mo = MovableObject(item, parent = self.targetNodePath)
            self.objectDict[mo.id()] = mo

    def setCamPosIndex(self, index):
        self.camPosIndex = index
        base.localAvatar.setCameraSettings(camPosList[index])

    def zoomCamIn(self):
        self.setCamPosIndex(max(0, self.camPosIndex - 1))
        messenger.send('wakeup')

    def zoomCamOut(self):
        self.setCamPosIndex(min(len(camPosList) - 1, self.camPosIndex + 1))
        messenger.send('wakeup')

    def rotateCamCW(self):
        self.orientCamH(base.localAvatar.getH(self.targetNodePath) - 90)
        messenger.send('wakeup')

    def rotateCamCCW(self):
        self.orientCamH(base.localAvatar.getH(self.targetNodePath) + 90)
        messenger.send('wakeup')

    def orientCamH(self, toonH):
        targetH = ROUND_TO(toonH, 90)
        base.localAvatar.hprInterval(duration = 1,
                                       hpr = Vec3(targetH, 0, 0),
                                       other = self.targetNodePath,
                                       blendType = 'easeInOut',
                                       name = 'editModeTransition').start()

    def setTargetNodePath(self, nodePath):
        self.targetNodePath = nodePath
        # Delete old collision solids
        if self.houseExtents:
            self.houseExtents.removeNode()
        if self.doorBlocker:
            self.doorBlocker.removeNode()
        self.makeHouseExtentsBox()
        self.makeDoorBlocker()
        # Put the drag plane under the house
        self.collisionNP.reparentTo(self.targetNodePath)

    def loadObject(self, filename):
        mo = MovableObject(filename, parent = self.targetNodePath)
        self.objectDict[mo.id()] = mo
        self.selectObject(mo)
        return mo

    def pickObject(self):
        # Check to see if any furniture object lies under cursor
        self.iRay.setParentNP(base.cam)
        entry = self.iRay.pickGeom(
            targetNodePath = self.targetNodePath,
            skipFlags = SKIP_ALL)
        # Collision!  Is it a movable object?
        if entry:
            nodePath = entry.getIntoNodePath()
            if self.isMovableObject(nodePath):
                # Yes! Select it
                self.selectObject(self.findObject(nodePath))
                return
        # No! Select nothing
        self.deselectObject()

    def pickInRoom(self, objectId):
        self.selectObject(self.objectDict.get(objectId))
        
    def selectObject(self, selectedObject):
        messenger.send('wakeup')
        if self.selectedObject:
            # Deselect the previous object.
            self.deselectObject()
        if selectedObject:
            # Select a new object.
            self.selectedObject = selectedObject
            # Start listening for the object's unexpected demise.
            self.deselectEvent = self.selectedObject.dfitem.uniqueName("disable")
            self.acceptOnce(self.deselectEvent, self.deselectObject)
            # Update feedback line
            self.lnp.reset()
            self.lnp.reparentTo(selectedObject)
            self.lnp.moveTo(selectedObject.c0)
            self.lnp.drawTo(selectedObject.c1)
            self.lnp.drawTo(selectedObject.c2)
            self.lnp.drawTo(selectedObject.c3)
            self.lnp.drawTo(selectedObject.c0)
            self.lnp.create()
            # Show button frame
            self.buttonFrame.show()
            self.enableButtonFrameTask()
            self.sendToAtticButton.show()
            self.atticRoof.hide()

    def deselectObject(self):
        # Deselect the currently selected object.
        self.moveObjectStop()
        if self.deselectEvent:
            self.ignore(self.deselectEvent)
            self.deselectEvent = None
        self.selectedObject = None
        self.lnp.detachNode()
        self.buttonFrame.hide()
        self.disableButtonFrameTask()
        self.sendToAtticButton.hide()
        self.atticRoof.show()

    def isMovableObject(self, nodePath):
        # Is this the child of a movable object?
        return nodePath.hasNetTag('movableObject')

    def findObject(self, nodePath):
        # Search up hierachy to find the parent node path with the movable object tag
        np = nodePath.findNetTag('movableObject')
        if np.isEmpty():
            return None
        else:
            return self.objectDict.get(np.id(), None)

    def moveObjectStop(self, *args):
        if self.movingObject:
            self.movingObject = 0
            # Kill existing task
            taskMgr.remove('moveObjectTask')
            # Put selected object back in hierarchy
            if self.selectedObject:
                self.selectedObject.wrtReparentTo(self.targetNodePath)
                # Unstash furniture collision node of selected object
                self.selectedObject.collisionNodePath.unstash()
                self.selectedObject.dfitem.stopAdjustPosHpr()
            # Make sure collision nodes are unstashed
            for object in self.objectDict.values():
                object.unstashBuiltInCollisionNodes()
            # Adjust center marker image
            self.centerMarker['image'] = [self.grabUp,self.grabDown,
                                          self.grabRollover]
            self.centerMarker.configure(
                text = ['',TTLocalizer.HDMoveLabel],
                text_pos = (0,1),
                text_scale = 0.7,
                text_fg = (1,1,1,1),
                text_shadow = (0,0,0,1),
                image_scale = 0.3)

    def moveObjectStart(self):
        self.moveObjectStop()
        # Check for new selected object
        self.pickObject()
        self.moveObjectContinue()

    def moveObjectContinue(self, *args):
        messenger.send('wakeup')
        # If user selected an object
        if self.selectedObject:
            for object in self.objectDict.values():
                object.stashBuiltInCollisionNodes()
            # And stash furniture collision node of selected object
            self.selectedObject.collisionNodePath.stash()
            self.selectedObject.dfitem.startAdjustPosHpr()
            # Set init flag
            self.firstTime = 1
            # Init self
            self.iPosHpr()
            self.startPoseValid = 0
            # Adjust grab button
            self.centerMarker['image'] = self.grabDown
            self.centerMarker.configure(
                text = TTLocalizer.HDMoveLabel,
                text_pos = (0,1),
                text_scale = 0.7,
                text_fg = (1,1,1,1),
                text_shadow = (0,0,0,1),
                image_scale = 0.3)
            # Start moving object
            taskMgr.add(self.moveObjectTask, 'moveObjectTask')
            self.movingObject = 1

    def setLnpColor(self, r, g, b):
        for i in range(5):
            self.lnp.lineSegs.setVertexColor(i,r,g,b)

    def markNewPosition(self, isValid):
        # Called by moveObjectTask to indicate the object has moved
        # into a new position, and whether the new position is valid
        # or not.

        # If the position is not valid, the object is snapped back to
        # its last known valid position.

        if not isValid:
            if self.startPoseValid:
                self.collisionOffsetNP.setPosHpr(
                    self.startPose, self.selectedObject.dragPoint, Vec3(0))
            #The following call is incorrect because the lineNodePath does not
            #contain functionality to change colors yet.
            #self.setLnpColor(1,0,0)

        else:
            # Ok, we've seen a valid position.  Next time around,
            # startPose will be valid.
            self.startPoseValid = 1

    def moveObjectTask(self,state):
        # Get some local variables
        so = self.selectedObject
        target = self.targetNodePath
        # Record start pose so we can restore object to current pose if neeeded
        self.startPose.iPosHpr(so)
        #The following call is incorrect because the lineNodePath does not
        #contain functionality to change colors yet.
        #self.setLnpColor(1,1,1)

        # Check for a collision with the drag plane
        self.iRay.setParentNP(base.cam)
        entry = self.iRay.pickBitMask(
            bitMask = ToontownGlobals.FurnitureDragBitmask,
            targetNodePath = target,
            skipFlags = SKIP_BACKFACE | SKIP_CAMERA | SKIP_UNPICKABLE)
        # If no collision, just return
        if not entry:
            return Task.cont

        # Got a collision, move self to hit point
        self.setPos(base.cam, entry.getSurfacePoint(base.cam))
        # If this is the first time, you can now reparent the selected object 
        if self.firstTime:
            # Initialize auxiliary node paths and reparent selected object
            self.moveObjectInit()
            self.firstTime = 0
        else:
            # Otherwise just reset auxiliary node paths
            self.gridSnapNP.iPos()
            self.collisionOffsetNP.iPosHpr()

        # If grid spacing is set snap gridSnapNP to grid
        if self.gridSpacing:
            # But base snap on drag point
            pos = self.dragPointNP.getPos(target)
            self.gridSnapNP.setPos(target,
                                   ROUND_TO(pos[0],self.gridSpacing),
                                   ROUND_TO(pos[1],self.gridSpacing),
                                   pos[2])

        # Now see if ray from camera through gridSnapNP (which is coincident
        # with the object's drag point) is intersecting a wall
        self.iRay.setParentNP(base.cam)
        entry = self.iRay.pickBitMask3D(
            bitMask = so.getWallBitmask(),
            targetNodePath = target,
            dir = Vec3(self.getNearProjectionPoint(self.gridSnapNP)),
            skipFlags = SKIP_BACKFACE | SKIP_CAMERA | SKIP_UNPICKABLE)
        fWall = 0
        if not so.getOnTable():
            while entry:
                # If you've bumped into a wall, align the object's
                # back to the wall.  Otherwise, just align the closest
                # edge.
                intoMask = entry.getIntoNodePath().node().getIntoCollideMask()
                fClosest = (intoMask & ToontownGlobals.WallBitmask).isZero()
                if self.alignObject(entry, target, fClosest = fClosest):
                    # Skip the next test
                    fWall = 1
                    break
                # Not a vertical wall, try the next collision
                entry = self.iRay.findNextCollisionEntry(
                    skipFlags = SKIP_BACKFACE | SKIP_CAMERA | SKIP_UNPICKABLE)

        if so.getOnWall():
            # If the object hangs on a wall, we're done--no more tests
            # are required.  If the object didn't make it onto the
            # wall, then flag it as an error.
            self.markNewPosition(fWall)
            return Task.cont

        # Drop a ray from the object's current location to find the floor
        # Check to make sure we ended up over a floor (to avoid moving
        # the object outside of the house)
        # Force object to sit on the floor if its fFloor flag is set
        # Put the collisionRay in target space

        # And just test against the target
        self.iRay.setParentNP(target)
        entry = self.iRay.pickBitMask3D(
            bitMask = so.getFloorBitmask(),
            targetNodePath = target,
            origin = Point3(self.gridSnapNP.getPos(target) + Vec3(0,0,10)),
            dir = Vec3(0,0,-1),
            skipFlags = SKIP_BACKFACE|SKIP_CAMERA|SKIP_UNPICKABLE
            )

        if not entry:
            # Hey, it's not over the floor.  Forget it.
            self.markNewPosition(0)
            return Task.cont

        nodePath = entry.getIntoNodePath()
        if self.isMovableObject(nodePath):
            # The object is on top of another object, such as a table.
            self.gridSnapNP.setPos(
                target,
                Point3(entry.getSurfacePoint(target)))

        else:
            # The object is on the floor.
            self.gridSnapNP.setPos(
                target,
                Point3(entry.getSurfacePoint(target) +
                       Vec3(0,0,ToontownGlobals.FloorOffset)))

            # See if we're close enough to the wall to snap
            # orientation to the wall.
            if not fWall:
                self.iSphere.setParentNP(self.gridSnapNP)
                self.iSphere.setCenterRadius(0, Point3(0), so.radius * 1.25)
                entry = self.iSphere.pickBitMask(
                    bitMask = so.getWallBitmask(),
                    targetNodePath = target,
                    skipFlags = SKIP_CAMERA | SKIP_UNPICKABLE)
                if entry:
                    self.alignObject(entry, target, fClosest = 1)

        # Now check for collisions and try to respond accordingly
        isValid = self.collisionTest()
        self.markNewPosition(isValid)
        
        # Done for this frame
        return Task.cont

    def collisionTest(self):
        # Returns true if the position is valid, false otherwise.
        
        so = self.selectedObject
        target = self.targetNodePath
        entry = self.segmentCollision()
        if not entry:
            # If no collisions, we're done
            return 1
        # We did detect some collisions, see if we can correct the problem
        offsetDict = {}
        # Process each collision entry
        while entry:
            # Determine how much to offset the segment in normal direction
            # to clear the collision
            # This offset is in the selectedObject's space
            offset = self.computeSegmentOffset(entry)
            if offset:
                # Which collision polygon did we collide with?
                eid = entry.getInto()
                # Get current max offset for this collision polygon
                # If no existing entry in offset dict, return zero vec
                maxOffsetVec = offsetDict.get(eid, Vec3(0))
                if offset.length() > maxOffsetVec.length():
                    maxOffsetVec.assign(offset)
                # Store it back in offset dict
                offsetDict[eid] = maxOffsetVec
            # Process next entry
            entry = self.iSegment.findNextCollisionEntry(
                skipFlags = SKIP_CAMERA | SKIP_UNPICKABLE)
        # We detected some collisions, try to sum up offsets to fix
        if offsetDict:
            # Find orthogonal components
            keys = offsetDict.keys()
            # Pick first offset as first cardinal direction
            ortho1 = offsetDict[keys[0]]
            ortho2 = Vec3(0)
            v1 = Vec3(ortho1)
            v1.normalize()
            # Compare parallel and orthogonal components of
            # the remaining offset vectors 
            for key in keys[1:]:
                # Get next offset and convert to offset1 space
                offset = offsetDict[key]
                # Check angle between offset and ortho1
                v2 = Vec3(offset)
                v2.normalize()
                dp = v1.dot(v2)
                if abs(dp) > 0.95:
                    if offset.length() > ortho1.length():
                        ortho1.assign(offset)
                elif abs(dp) < 0.05:
                    if offset.length() > ortho2.length():
                        ortho2.assign(offset)
                else:
                    o1Len = ortho1.length()
                    # Compute the parallel and perpendicular components
                    parallelVec = Vec3(
                        (ortho1 * offset.dot(ortho1))/(o1Len * o1Len))
                    perpVec = Vec3(offset - parallelVec)
                    # Compare length with current ortho vecs
                    if parallelVec.length() > o1Len:
                        ortho1.assign(parallelVec)
                    if perpVec.length() > ortho2.length():
                        ortho2.assign(perpVec)
            # Sum orthogonal components and adjust position
            totalOffset = ortho1 + ortho2
            self.collisionOffsetNP.setPos(self.collisionOffsetNP, totalOffset)
            if not self.segmentCollision():
                return 1
        # We did detect some collisions, see if we can correct the problem
        # How far have we moved the object this frame?
        m = self.startPose.getMat(so)
        deltaMove = Vec3(m.getRow3(3))
        if deltaMove.length() == 0:
            # If we haven't moved, quit, since we can't use
            # zero length collision segments
            return 1
        # Check for collisions along segments from currentPose to startPose 
        # To see how far you have to move to clear the collision condition
        self.iSegment4.setParentNP(so)
        entry = self.iSegment4.pickBitMask(
            bitMask = so.getWallBitmask(),
            targetNodePath = target,
            endPointList = [(so.c0, Point3(m.xformPoint(so.c0))),
                            (so.c1, Point3(m.xformPoint(so.c1))),
                            (so.c2, Point3(m.xformPoint(so.c2))),
                            (so.c3, Point3(m.xformPoint(so.c3)))],
            skipFlags = SKIP_CAMERA | SKIP_UNPICKABLE)
        # The maximum length offset is a good guess of how far you have
        # to move the selected object to clear the collision
        maxLen = 0
        maxOffset = None
        while entry:
            offset = Vec3(entry.getSurfacePoint(entry.getFromNodePath()) -
                          entry.getFrom().getPointA())
            offsetLen = Vec3(offset).length()
            if offsetLen > maxLen:
                maxLen = offsetLen
                maxOffset = offset
            # Process next entry
            entry = self.iSegment4.findNextCollisionEntry(
                skipFlags = SKIP_CAMERA | SKIP_UNPICKABLE)
        if maxOffset:
            self.collisionOffsetNP.setPos(self.collisionOffsetNP, maxOffset)
        # One more collision test to see if we resolved the problem
        if not self.segmentCollision():
            return 1

        # Collision still detected! Give up and revert to original position
        return 0

    def segmentCollision(self):
        # Now check to see if collision segments surrounding and criss-crossing
        # the selected object are colliding with the wall or other objects
        so = self.selectedObject
        self.iSegment.setParentNP(so)
        entry = self.iSegment.pickBitMask(
            bitMask = so.getWallBitmask(),
            targetNodePath = self.targetNodePath,
            endPointList = [(so.c0, so.c1),(so.c1, so.c2),
                            (so.c2, so.c3),(so.c3, so.c0),
                            (so.c0, so.c2),(so.c1, so.c3)],
            skipFlags = SKIP_CAMERA | SKIP_UNPICKABLE)
        return entry

    def computeSegmentOffset(self, entry):
        # The object doesn't have a surface normal (e.g. a collision sphere)
        # Just punt for now
        fromNodePath = entry.getFromNodePath()
        if entry.hasSurfaceNormal():
            normal = entry.getSurfaceNormal(fromNodePath)
        else:
            return None
        hitPoint = entry.getSurfacePoint(fromNodePath)
        # Check angle between normal for this collision and vector from
        # the startPose drag point to hit point.  If dot product is positive
        # then the startPose dragPoint was on the back side of this polygon
        # (like second wall in double faced wall).  Ignore this collision
        # Do this check relative to the object's start pose
        # Get xform from startPose to current selectedObject pose
        m = self.selectedObject.getMat(self.startPose)
        # Where is hitPoint relative to startPose
        hp = Point3(m.xformPoint(hitPoint))
        # Convert normal to startPose coordinate system
        hpn = Vec3(m.xformVec(normal))
        # Compute vec from dragPoint to hitPoint
        hitPointVec = Vec3(hp - self.selectedObject.dragPoint)
        # Check angle between this vec and the hitPoint normal
        if (hitPointVec.dot(hpn) > 0):
            # Backface, ignore this collision
            return None
        # We're on the front side, continue....
        # Precompute length of normal
        nLen = normal.length()
        # Determine how much you have to offset collision segment 
        # to move it to the front side of the collision plane
        # Check position of endpoints relative to collision plane
        # Test point A first
        # Compute vector from hit point to collision segment end point A
        offsetVecA = hitPoint - entry.getFrom().getPointA()
        # Compute the projection of this vector along the collision normal
        offsetA = (normal * offsetVecA.dot(normal))/(nLen * nLen)
        # Return offset vector if this point is on polygon backside
        if offsetA.dot(normal) > 0:
            # Scale offset slightly to clear collision
            return offsetA * 1.01
        else:
            # That point was on the polygon's front side, need to test point B
            offsetVecB =  hitPoint - entry.getFrom().getPointB()
            offsetB = (normal * offsetVecB.dot(normal))/(nLen * nLen)
            # Scale offset slightly to clear collision
            return offsetB * 1.01

    def alignObject(self, entry, target, fClosest = 0,
                    wallOffset = None):
        # Align object's orientation with object it collided with
        # Check's to make sure wall is vertical (returns 1 on success)

        if not entry.hasSurfaceNormal():
            # No way to check the alignment of the object it collided
            # with; give up.
            return 0
        
        # Convert the normal to the target's (i.e. room's) space
        normal = entry.getSurfaceNormal(target)
        # Check how upright the collision surface was
        if (abs(normal.dot(Vec3(0,0,1))) < 0.1):
            # Pointing at a vertical wall
            # Align back of object with wall
            tempNP = target.attachNewNode('temp')
            # Force normal to horizontal
            normal.setZ(0)
            normal.normalize()
            # Compute point for tempNP to look at
            # This assumes Y axis points out furniture's back
            lookAtNormal = Point3(normal)
            lookAtNormal *= -1
            # Orient temp NP so its Y axis is aligned with lookAtNormal
            tempNP.lookAt(lookAtNormal)
            if fClosest:
                # Now align gridSnapNP with tempNP
                angle = ROUND_TO(self.gridSnapNP.getH(tempNP), 90.0)
            else:
                angle = 0
            self.gridSnapNP.setHpr(tempNP, angle, 0, 0)
            # Now we need to offset object so its back is against the wall
            # Move tempNP to the hit point
            hitPoint = entry.getSurfacePoint(target)
            tempNP.setPos(hitPoint)
            # Offset object along normal to get it in front of the wall
            if wallOffset == None:
                wallOffset = self.selectedObject.getWallOffset()
            self.gridSnapNP.setPos(tempNP, 0, -wallOffset, 0)
            # Clean up tempNP
            tempNP.removeNode()
            return 1
        return 0

    def rotateLeft(self):
        if not self.selectedObject:
            return
        # Rotate object about the drag point
        so = self.selectedObject
        so.dfitem.startAdjustPosHpr()
        self.iPosHpr(so)
        self.moveObjectInit()
        if so.getOnWall():
            startR = self.gridSnapNP.getR()
            newR = ROUND_TO(startR + 22.5, 22.5)
            self.gridSnapNP.setR(newR)
        else:
            startH = self.gridSnapNP.getH(self.targetNodePath)
            newH = ROUND_TO(startH - 22.5, 22.5)
            self.gridSnapNP.setHpr(self.targetNodePath, newH, 0, 0)
            self.collisionTest()
            
        so.wrtReparentTo(self.targetNodePath)
        self.disableButtonFrameTask()
        so.dfitem.stopAdjustPosHpr()

    def rotateRight(self):
        if not self.selectedObject:
            return
        # Rotate object about the drag point 
        so = self.selectedObject
        so.dfitem.startAdjustPosHpr()
        self.iPosHpr(so)
        self.moveObjectInit()
        if so.getOnWall():
            startR = self.gridSnapNP.getR()
            newR = ROUND_TO(startR - 22.5, 22.5)
            self.gridSnapNP.setR(newR)
        else:
            startH = self.gridSnapNP.getH(self.targetNodePath)
            newH = ROUND_TO(startH + 22.5, 22.5) % 360.0
            self.gridSnapNP.setHpr(self.targetNodePath, newH, 0, 0)
            self.collisionTest()
            
        so.wrtReparentTo(self.targetNodePath)
        self.disableButtonFrameTask()
        so.dfitem.stopAdjustPosHpr()

    def moveObjectInit(self):
        self.dragPointNP.setPosHpr(self.selectedObject,
                                   self.selectedObject.dragPoint, Vec3(0))
        self.gridSnapNP.iPosHpr()
        self.collisionOffsetNP.iPosHpr()
        self.selectedObject.wrtReparentTo(self.collisionOffsetNP)

    def resetFurniture(self):
        for o in self.objectDict.values():
            o.resetMovableObject()
        self.objectDict = {}
        self.deselectObject()
        self.buttonFrame.hide()

    def destroy(self):
        self.ignore('enterFurnitureMode')
        self.ignore('exitFurnitureMode')
        if self.guiInterval:
            self.guiInterval.finish()
        if self.furnitureManager:
            self.exitFurnitureMode(self.furnitureManager)
        self.cleanupDialog()
        self.resetFurniture()
        self.buttonFrame.destroy()
        self.furnitureGui.destroy()
        if self.houseExtents:
            self.houseExtents.removeNode()
        if self.doorBlocker:
            self.doorBlocker.removeNode()
        self.removeNode()
        if self.verifyFrame:
            self.verifyFrame.destroy()
            self.verifyFrame = None
            self.deleteItemText = None
            self.okButton = None
            self.cancelButton = None

    def createSelectedObjectPanel(self,guiModels):
        self.buttonFrame = DirectFrame(scale = 0.5)
        # Grab handle
        self.grabUp = guiModels.find('**/handup')
        self.grabDown = guiModels.find('**/handdown')
        self.grabRollover = guiModels.find('**/handrollover')
        self.centerMarker = DirectButton(
            parent = self.buttonFrame,
            text = ['',TTLocalizer.HDMoveLabel],
            text_pos = (0,1),
            text_scale = 0.7,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            image = [self.grabUp, self.grabDown, self.grabRollover],
            image_scale = 0.3,
            relief = None,
            scale = 0.12)
        self.centerMarker.bind(DGG.B1PRESS, self.moveObjectContinue)
        self.centerMarker.bind(DGG.B1RELEASE, self.moveObjectStop)
        # Left arrow (CCW rotation)
        guiCCWArrowUp = guiModels.find("**/LarrowUp")
        guiCCWArrowDown = guiModels.find("**/LarrowDown")
        guiCCWArrowRollover = guiModels.find("**/LarrowRollover")
        self.rotateLeftButton = DirectButton(
            parent = self.buttonFrame,
            relief = None,
            image = (guiCCWArrowUp, guiCCWArrowDown,
                     guiCCWArrowRollover,guiCCWArrowUp),
            image_pos = (0,0,0.1),
            image_scale = 0.15,
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = ('',TTLocalizer.HDRotateCCWLabel,TTLocalizer.HDRotateCCWLabel,''),
            text_pos = (0.135, -0.1),
            text_scale = 0.1,
            text_align = TextNode.ARight,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            pos = (-.125,0,-.2),
            scale = 0.7,
            command = self.rotateLeft,
            )
        self.rotateLeftButton.bind(DGG.EXIT, self.enableButtonFrameTask)
        # Right arrow (CW rotation)
        guiCWArrowUp = guiModels.find("**/RarrowUp")
        guiCWArrowDown = guiModels.find("**/RarrowDown")
        guiCWArrowRollover = guiModels.find("**/RarrowRollover")
        self.rotateRightButton = DirectButton(
            parent = self.buttonFrame,
            relief = None,
            image = (guiCWArrowUp, guiCWArrowDown,
                     guiCWArrowRollover, guiCWArrowUp),
            image_pos = (0,0,0.1),
            image_scale = 0.15,
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = ('',TTLocalizer.HDRotateCWLabel,TTLocalizer.HDRotateCWLabel,''),
            text_pos = (-0.135, -0.1),
            text_scale = 0.1,
            text_align = TextNode.ALeft,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            pos = (0.125,0,-0.2),
            scale = 0.7,
            command = self.rotateRight,
            )
        self.rotateRightButton.bind(DGG.EXIT, self.enableButtonFrameTask)
        self.buttonFrame.hide()

    def recenterButtonFrameTask(self, state):
        if self.selectedObject and self.fRecenter:
            self.buttonFrame.setPos(self.getSelectedObjectScreenXY())
        return Task.cont

    def disableButtonFrameTask(self, event=None):
        self.fRecenter = 0

    def enableButtonFrameTask(self, event=None):
        self.fRecenter = 1

    def getNearProjectionPoint(self,nodePath):
        # Find the position of the projection of the specified node path
        # on the near plane
        origin = nodePath.getPos(camera)
        # project this onto near plane
        if origin[1] != 0.0:
            return origin * (base.camLens.getNear() / origin[1])
        else:
            # Object is coplaner with camera, just return something reasonable
            return Point3(0, base.camLens.getNear(), 0)

    def getSelectedObjectScreenXY(self):
        tNodePath = self.selectedObject.attachNewNode('temp')
        tNodePath.setPos(self.selectedObject.center)
        # Where does the node path's projection fall on the near plane
        nearVec = self.getNearProjectionPoint(tNodePath)
        # Where does this fall on focal plane
        nearVec *= base.camLens.getFocalLength()/base.camLens.getNear()
        # Convert to aspect2d coords (clamping to visible screen
        render2dX = CLAMP(nearVec[0]/(base.camLens.getFilmSize()[0]/2.0),
                          -.9,.9)
        aspect2dX = render2dX * base.getAspectRatio()
        aspect2dZ = CLAMP(nearVec[2]/(base.camLens.getFilmSize()[1]/2.0),
                          -.8,.9)
        tNodePath.removeNode()
        # Return the resulting value
        return Vec3(aspect2dX,0,aspect2dZ)

    def createMainControls(self, guiModels):
        attic = guiModels.find('**/attic')
        # Main attic/stop button
        self.furnitureGui = DirectFrame(
            relief = None,
            pos = (-1.19, 1, 0.33),
            scale= 0.04,
            image = attic)
        bMoveStopUp = guiModels.find('**/bu_atticX/bu_attic_up')
        bMoveStopDown = guiModels.find('**/bu_atticX/bu_attic_down')
        bMoveStopRollover = guiModels.find('**/bu_atticX/bu_attic_rollover')
        self.bStopMoveFurniture = DirectButton(
            parent = self.furnitureGui,
            relief = None,
            image = [bMoveStopUp,bMoveStopDown,bMoveStopRollover,bMoveStopUp],
            text = ["", TTLocalizer.HDStopMoveFurnitureButton,
                    TTLocalizer.HDStopMoveFurnitureButton],
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_font = ToontownGlobals.getInterfaceFont(),
            pos = (-0.3, 0, 9.4),
            command = base.localAvatar.stopMoveFurniture,
            )
        self.bindHelpText(self.bStopMoveFurniture, "DoneMoving")
        self.atticRoof = DirectLabel(
            parent = self.furnitureGui,
            relief = None,
            image = guiModels.find('**/rooftile')
            )
        # Main frames to hold other stuff
        self.itemBackgroundFrame = DirectFrame(
            parent = self.furnitureGui,
            relief = None,
            image = guiModels.find('**/item_backgroun'),
            image_pos = (0,0,-22),
            image_scale = (1,1,5),
            )
        self.scrollUpFrame = DirectFrame(
            parent = self.furnitureGui,
            relief = None,
            image = guiModels.find('**/scrollup'),
            pos = (0,0,-0.58)
            )
        self.camButtonFrame = DirectFrame(
            parent = self.furnitureGui,
            relief = None,
            image = guiModels.find('**/low'),
            pos = (0,0,-11.69),
            )
        tagUp = guiModels.find('**/tag_up')
        tagDown = guiModels.find('**/tag_down')
        tagRollover = guiModels.find('**/tag_rollover')
        self.inAtticButton = DirectButton(
            parent = self.itemBackgroundFrame,
            relief = None,
            text = TTLocalizer.HDInAtticLabel,
            text_pos = (-0.1,-0.25),
            image = [tagUp, tagDown, tagRollover],
            pos = (2.85,0,4),
            scale = 0.8,
            command = self.showAtticPicker,
            )
        self.bindHelpText(self.inAtticButton, "Attic")

        self.inRoomButton = DirectButton(
            parent = self.itemBackgroundFrame,
            relief = None,
            text = TTLocalizer.HDInRoomLabel,
            text_pos = (-0.1,-0.25),
            image = [tagUp, tagDown, tagRollover],
            pos = (2.85,0,1.1),
            scale = 0.8,
            command = self.showInRoomPicker,
            )
        self.bindHelpText(self.inRoomButton,"Room")

        self.inTrashButton = DirectButton(
            parent = self.itemBackgroundFrame,
            relief = None,
            text = TTLocalizer.HDInTrashLabel,
            text_pos = (-0.1,-0.25),
            image = [tagUp, tagDown, tagRollover],
            pos = (2.85,0,-1.8),
            scale = 0.8,
            command = self.showInTrashPicker,
            )
        self.bindHelpText(self.inTrashButton,"Trash")

        for i in range(4):
            self.inAtticButton.component('text%d' % i).setR(-90)
            self.inRoomButton.component('text%d' % i).setR(-90)
            self.inTrashButton.component('text%d' % i).setR(-90)
        # Move selected item to attic
        backInAtticUp = guiModels.find('**/bu_backinattic_up1')
        backInAtticDown = guiModels.find('**/bu_backinattic_down1')
        backInAtticRollover = guiModels.find('**/bu_backinattic_rollover2')
        self.sendToAtticButton = DirectButton(
            parent = self.furnitureGui,
            relief = None,
            pos = (0.4,0,12.8),
            text = ['', TTLocalizer.HDToAtticLabel],
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_pos = (1.2,-0.3),
            image = [backInAtticUp, backInAtticDown, backInAtticRollover],
            command = self.sendItemToAttic,
            )
        self.sendToAtticButton.hide()
        self.bindHelpText(self.sendToAtticButton, "SendToAttic")

        # Control snap grid
        #self.gridMenu = DirectOptionMenu(
        #    parent = self.furnitureGui,
        #    relief = DGG.RAISED,
        #    scale = 0.087,
        #    pos = (.376,0,0),
        #    items = ['None', '0.1', '0.25', '0.5', '1.0'],
        #    command = self.setGridSpacingString,
        #    )
        zoomInUp = guiModels.find('**/bu_RzoomOut_up')
        zoomInDown = guiModels.find('**/bu_RzoomOut_down')
        zoomInRollover = guiModels.find('**/bu_RzoomOut_rollover')
        self.zoomInButton = DirectButton(
            parent = self.camButtonFrame,
            image = [zoomInUp, zoomInDown, zoomInRollover],
            relief = None,
            pos = (0.9,0,-0.75),
            command = self.zoomCamIn,
            )
        self.bindHelpText(self.zoomInButton, "ZoomIn")
        zoomOutUp = guiModels.find('**/bu_LzoomIn_up')
        zoomOutDown = guiModels.find('**/bu_LzoomIn_down')
        zoomOutRollover = guiModels.find('**/buLzoomIn_rollover')
        self.zoomOutButton = DirectButton(
            parent = self.camButtonFrame,
            image = [zoomOutUp, zoomOutDown, zoomOutRollover],
            relief = None,
            pos = (-1.4,0,-0.75),
            command = self.zoomCamOut,
            )
        self.bindHelpText(self.zoomOutButton, "ZoomOut")
        camCCWUp = guiModels.find('**/bu_Rarrow_up1')
        camCCWDown = guiModels.find('**/bu_Rarrow_down1')
        camCCWRollover = guiModels.find('**/bu_Rarrow_orllover')
        self.rotateCamLeftButton = DirectButton(
            parent = self.camButtonFrame,
            image = [camCCWUp, camCCWDown, camCCWRollover],
            relief = None,
            pos = (0.9,0,-3.0),
            command = self.rotateCamCCW,
            )
        self.bindHelpText(self.rotateCamLeftButton, "RotateLeft")
        camCWUp = guiModels.find('**/bu_Larrow_up1')
        camCWDown = guiModels.find('**/bu_Larrow_down1')
        camCWRollover = guiModels.find('**/bu_Larrow_rollover2')
        self.rotateCamRightButton = DirectButton(
            parent = self.camButtonFrame,
            image = [camCWUp, camCWDown, camCWRollover],
            relief = None,
            pos = (-1.4,0,-3.0),
            command = self.rotateCamCW,
            )
        self.bindHelpText(self.rotateCamRightButton, "RotateRight")
        # For toggling delete mode
        trashcanGui = loader.loadModel("phase_3/models/gui/trashcan_gui")
        trashcanUp = trashcanGui.find("**/TrashCan_CLSD")
        trashcanDown = trashcanGui.find("**/TrashCan_OPEN")
        trashcanRollover = trashcanGui.find("**/TrashCan_RLVR")
        self.deleteEnterButton = DirectButton(
            parent = self.furnitureGui,
            image = (trashcanUp, trashcanDown, trashcanRollover, trashcanUp),
            text = ["",TTLocalizer.InventoryDelete,TTLocalizer.InventoryDelete,""],
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = 0.1,
            text_align = TextNode.ACenter,
            text_pos = (0, -0.12),
            text_font = ToontownGlobals.getInterfaceFont(),
            textMayChange = 0,    
            relief = None,
            pos = (3.70, 0.00, -13.80),
            scale = 7.13,
            command = self.enterDeleteMode,
            )
        self.bindHelpText(self.deleteEnterButton, "DeleteEnter")
        self.deleteExitButton = DirectButton(
            parent = self.furnitureGui,
            image = (trashcanUp, trashcanDown, trashcanRollover, trashcanUp),
            text = ("",TTLocalizer.InventoryDone,TTLocalizer.InventoryDone,""),
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = 0.1,
            text_align = TextNode.ACenter,
            text_pos = (0, -0.12),
            text_font = ToontownGlobals.getInterfaceFont(),
            textMayChange = 0,    
            relief = None,
            pos = (3.70, 0.00, -13.80),
            scale = 7.13,
            command = self.exitDeleteMode,
            )
        self.bindHelpText(self.deleteExitButton, "DeleteExit")
        self.deleteExitButton.hide()
        self.trashcanBase = DirectLabel(
            parent = self.furnitureGui,
            image = guiModels.find('**/trashcan_base'),
            relief = None,
            pos = (0,0,-11.64))
        self.furnitureGui.hide()

        self.helpText = DirectLabel(
            parent = self.furnitureGui,
            relief=DGG.SUNKEN,
            frameSize = (-0.5, 10, -3, 0.9),
            frameColor = (0.2,0.2,0.2,0.5),
            borderWidth = (0.01, 0.01),
            text = '',
            text_wordwrap = 12,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = 0.8,
            pos = (3, 0.0, -7),
            scale = 1,
            text_align = TextNode.ALeft,
            )
        self.helpText.hide()

    def createAtticPicker(self):
        assert(self.atticPicker == None)
        
        # First, generate a list of FurnitureItemPanels.
        self.atticItemPanels = []
        for itemIndex in range(len(self.furnitureManager.atticItems)):
            panel = FurnitureItemPanel(
                self.furnitureManager.atticItems[itemIndex],
                itemIndex, command = self.bringItemFromAttic,
                deleteMode = self.deleteMode,
                helpCategory = "FurnitureItemPanelAttic")
            self.atticItemPanels.append(panel)

        self.atticWallpaperPanels = []
        for itemIndex in range(len(self.furnitureManager.atticWallpaper)):
            panel = FurnitureItemPanel(
                self.furnitureManager.atticWallpaper[itemIndex],
                itemIndex, command = self.bringWallpaperFromAttic,
                deleteMode = self.deleteMode,
                helpCategory = "FurnitureItemPanelAttic")
            self.atticWallpaperPanels.append(panel)

        self.atticWindowPanels = []
        for itemIndex in range(len(self.furnitureManager.atticWindows)):
            panel = FurnitureItemPanel(
                self.furnitureManager.atticWindows[itemIndex],
                itemIndex, command = self.bringWindowFromAttic,
                deleteMode = self.deleteMode,
                helpCategory = "FurnitureItemPanelAttic")
            self.atticWindowPanels.append(panel)

        # Now make a scrolled list of those panels.
        self.regenerateAtticPicker()

    def regenerateAtticPicker(self):
        selectedIndex = 0
        # Delete existing picker
        if self.atticPicker:
            selectedIndex = self.atticPicker.getSelectedIndex()
            for panel in self.atticItemPanels:
                panel.detachNode()
            for panel in self.atticWallpaperPanels:
                panel.detachNode()
            for panel in self.atticWindowPanels:
                panel.detachNode()
            self.atticPicker.destroy()
            self.atticPicker = None
        # Compose itemList
        itemList = (self.atticItemPanels + self.atticWallpaperPanels +
                    self.atticWindowPanels)
        # Determine appropriate text
        if self.deleteMode:
            text = TTLocalizer.HDDeletePickerLabel
        else:
            text = TTLocalizer.HDAtticPickerLabel
        # Create picker
        self.atticPicker = self.createScrolledList(
            itemList, text, 'atticPicker', selectedIndex)
        # Show or hide depending upon current mode
        if self.inRoomPicker or self.inTrashPicker:
            self.atticPicker.hide()
        else:
            self.atticPicker.show()

    def createInRoomPicker(self):
        assert(self.inRoomPicker == None)
        # The inRoomPicker is a panel that allows you to directly
        # select the furniture that should already be somewhere within
        # the room.
        # First, generate a list of FurnitureItemPanels.
        self.inRoomPanels = []
        for objectId, object in self.objectDict.items():
            panel = FurnitureItemPanel(object.dfitem.item, objectId,
                                       command = self.requestReturnToAttic,
                                       deleteMode = self.deleteMode,
                                       withinFunc = self.pickInRoom,
                                       helpCategory = "FurnitureItemPanelRoom")
            self.inRoomPanels.append(panel)
        # Now make a scrolled list of those panels.
        self.regenerateInRoomPicker()

    def regenerateInRoomPicker(self):
        selectedIndex = 0
        # Delete existing if it already exists
        if self.inRoomPicker:
            selectedIndex = self.inRoomPicker.getSelectedIndex()
            for panel in self.inRoomPanels:
                panel.detachNode()
            self.inRoomPicker.destroy()
            self.inRoomPicker = None
        # Get appropriate text
        if self.deleteMode:
            text = TTLocalizer.HDDeletePickerLabel
        else:
            text = TTLocalizer.HDInRoomPickerLabel
        self.inRoomPicker = self.createScrolledList(
            self.inRoomPanels, text, 'inRoomPicker', selectedIndex)

    def createInTrashPicker(self):
        assert(self.inTrashPicker == None)
        # The inTrashPicker is a panel that allows you to directly
        # select the furniture that should already be somewhere within
        # the room.
        # First, generate a list of FurnitureItemPanels.
        self.inTrashPanels = []
        for itemIndex in range(len(self.furnitureManager.deletedItems)):
            panel = FurnitureItemPanel(
                self.furnitureManager.deletedItems[itemIndex], itemIndex,
                command = self.requestReturnToAtticFromTrash,
                helpCategory = "FurnitureItemPanelTrash")
            self.inTrashPanels.append(panel)
        # Now make a scrolled list of those panels.
        self.regenerateInTrashPicker()

    def regenerateInTrashPicker(self):
        selectedIndex = 0
        # Delete existing if it already exists
        if self.inTrashPicker:
            selectedIndex = self.inTrashPicker.getSelectedIndex()
            for panel in self.inTrashPanels:
                panel.detachNode()
            self.inTrashPicker.destroy()
            self.inTrashPicker = None
        # Get appropriate text
        text = TTLocalizer.HDInTrashPickerLabel
        self.inTrashPicker = self.createScrolledList(
            self.inTrashPanels, text, 'inTrashPicker', selectedIndex)

    def createScrolledList(self, itemList, text, name, selectedIndex):
        gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
        picker = DirectScrolledList(
            parent = self.furnitureGui,
            pos = (-0.38, 0.00, 3),
            scale = 7.125,
            relief = None,
            items = itemList,
            numItemsVisible = 5,
            text = text,
            text_fg = (1,1,1,1),
            text_shadow = (0,0,0,1),
            text_scale = 0.1,
            text_pos = (0,0.4),
            # inc and dec are DirectButtons
            decButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            decButton_relief = None,
            decButton_scale = (1.5,1.5,1.5),
            decButton_pos = (0,0,0.3),
            # Make the disabled button fade out
            decButton_image3_color = Vec4(1,1,1,0.1),
            incButton_image = (gui.find("**/FndsLst_ScrollUp"),
                               gui.find("**/FndsLst_ScrollDN"),
                               gui.find("**/FndsLst_ScrollUp_Rllvr"),
                               gui.find("**/FndsLst_ScrollUp"),
                               ),
            incButton_relief = None,
            incButton_scale = (1.5,1.5,-1.5),
            incButton_pos = (0,0,-1.878),
            # Make the disabled button fade out
            incButton_image3_color = Vec4(1,1,1,0.1),
            )
        picker.setName(name)
        picker.scrollTo(selectedIndex)
        return picker

    def reset():
        self.destroy()
        furnitureMenu.destroy()
        #resetButton.destroy()

    def showAtticPicker(self):
        if self.inRoomPicker:
            self.inRoomPicker.destroy()
            self.inRoomPicker = None
        if self.inTrashPicker:
            self.inTrashPicker.destroy()
            self.inTrashPicker = None
        self.atticPicker.show()
        self.inAtticButton['image_color'] = Vec4(1,1,1,1)
        self.inRoomButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.inTrashButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.deleteExitButton['state'] = 'normal'
        self.deleteEnterButton['state'] = 'normal'

    def showInRoomPicker(self):
        messenger.send('wakeup')
        if not self.inRoomPicker:
            self.createInRoomPicker()
        self.atticPicker.hide()
        if self.inTrashPicker:
            self.inTrashPicker.destroy()
            self.inTrashPicker = None
        self.inAtticButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.inRoomButton['image_color'] = Vec4(1,1,1,1)
        self.inTrashButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.deleteExitButton['state'] = 'normal'
        self.deleteEnterButton['state'] = 'normal'

    def showInTrashPicker(self):
        messenger.send('wakeup')
        if not self.inTrashPicker:  
            self.createInTrashPicker()
        self.atticPicker.hide()
        if self.inRoomPicker:
            self.inRoomPicker.destroy()
            self.inRoomPicker = None
        self.inAtticButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.inRoomButton['image_color'] = Vec4(0.8,0.8,0.8,1)
        self.inTrashButton['image_color'] = Vec4(1,1,1,1)
        self.deleteExitButton['state'] = 'disabled'
        self.deleteEnterButton['state'] = 'disabled'

    def sendItemToAttic(self):
        messenger.send('wakeup')
        if self.selectedObject:
            callback = PythonUtil.Functor(
                self.__sendItemToAtticCallback, self.selectedObject.id())
                                          
            self.furnitureManager.moveItemToAttic(
                self.selectedObject.dfitem, callback)

            # Deselect the item immediately.
            self.deselectObject()

    def __sendItemToAtticCallback(self, objectId, retcode, item):
        # Reset disabled buttons
        self.__enableItemButtons(1)
        # Process error codes
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to send item %s to attic, reason %s." % (item.getName(), retcode))
            return

        # The item was successfully sent to the attic.  Remove it from
        # our active list.
        del(self.objectDict[objectId])
        if self.selectedObject != None and \
           self.selectedObject.id() == objectId:
            # It's about to be deleted; go ahead and remove it from
            # the scene graph.
            self.selectedObject.detachNode()
            self.deselectObject()
        
        # Add the item to the end of our attic list (since that's what
        # the AI did).
        itemIndex = len(self.atticItemPanels)
        assert(item == self.furnitureManager.atticItems[itemIndex])
        panel = FurnitureItemPanel(item, itemIndex,
                                   command = self.bringItemFromAttic,
                                   deleteMode = self.deleteMode,
                                   helpCategory = "FurnitureItemPanelAttic")
        self.atticItemPanels.append(panel)

        # DistributedScrolledList.addItem() has some issues.  For now,
        # just regenerate the list object.
        #self.atticPicker.addItem(panel)
        self.regenerateAtticPicker()

        # Also remove the item from the inRoomPicker, if we have it
        # up.
        if self.inRoomPicker:
            for i in range(len(self.inRoomPanels)):
                if self.inRoomPanels[i].itemId == objectId:
                    del self.inRoomPanels[i]
                    self.regenerateInRoomPicker()
                    return

    def cleanupDialog(self, buttonValue = None):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
            self.__enableItemButtons(1)

    def enterDeleteMode(self):
        self.deleteMode = 1
        self.__updateDeleteMode()

    def exitDeleteMode(self):
        self.deleteMode = 0
        self.__updateDeleteMode()

    def __updateDeleteMode(self):
        if not self.atticPicker:
            return
            
        self.notify.debug("__updateDeleteMode deleteMode=%s" % (self.deleteMode))

        if self.deleteMode:
            framePanelColor = DeletePickerPanelColor
            atticText = TTLocalizer.HDDeletePickerLabel
            inRoomText = TTLocalizer.HDDeletePickerLabel
            helpCategory = "FurnitureItemPanelDelete"
        else:
            framePanelColor = NormalPickerPanelColor
            atticText = TTLocalizer.HDAtticPickerLabel
            inRoomText = TTLocalizer.HDInRoomPickerLabel
            helpCategory = None

        if self.inRoomPicker:
            self.inRoomPicker['text'] = inRoomText
            for panel in self.inRoomPicker['items']:
                panel.setDeleteMode(self.deleteMode)
                panel.bindHelpText(helpCategory)

        if self.atticPicker:
            self.atticPicker['text'] = atticText
            for panel in self.atticPicker['items']:
                panel.setDeleteMode(self.deleteMode)
                panel.bindHelpText(helpCategory)

        self.__updateDeleteButtons()

    def __updateDeleteButtons(self):
        if self.deleteMode:
            self.deleteExitButton.show()
            self.deleteEnterButton.hide()
        else:
            self.deleteEnterButton.show()
            self.deleteExitButton.hide()

    def deleteItemFromRoom(self, dfitem, objectId, itemIndex):
        messenger.send('wakeup')
        callback = PythonUtil.Functor(
            self.__deleteItemFromRoomCallback, objectId, itemIndex)
        self.furnitureManager.deleteItemFromRoom(dfitem, callback)

    def __deleteItemFromRoomCallback(self, objectId, itemIndex, retcode, item):
        # Reset disabled buttons
        self.__enableItemButtons(1)
        # Process error codes
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to delete item %s from room, reason %s." %
                             (item.getName(), retcode))
            return
        # The item was successfully sent to the attic.  Remove it from
        # our active list.
        del(self.objectDict[objectId])
        if self.selectedObject != None and \
           self.selectedObject.id() == objectId:
            # It's about to be deleted; go ahead and remove it from
            # the scene graph.
            self.selectedObject.detachNode()
            self.deselectObject()
        # Also remove the item from the inRoomPicker, if we have it
        # up.
        if self.inRoomPicker and (itemIndex is not None):
            del self.inRoomPanels[itemIndex]
            self.regenerateInRoomPicker()

    def bringItemFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticItems[itemIndex])

        # Make sure we can't press the button again until we hear from the AI
        self.__enableItemButtons(0)

        if self.deleteMode:
            self.requestDelete(item, itemIndex, self.deleteItemFromAttic)
            return

        pos = self.targetNodePath.getRelativePoint(
            base.localAvatar, Point3(0, 2, 0))
        hpr = Point3(0, 0, 0)

        # x and y limited to [-3276.8, 3276.7], z is limited to [-327.68, 327.67]. Warn if pos is 
        # near those values (dclass definition will throw an exception if it's out of range). This
        # warning provides more info for TOON-1959.
        assert abs(pos[0]) <= 3000 and abs(pos[1]) <= 3000 and abs(pos[2]) <= 300
        if abs(pos[0]) > 3000 or abs(pos[1]) > 3000 or abs(pos[2]) > 300:
            self.notify.warning("bringItemFromAttic extreme pos targetNodePath=%s avatar=%s %s" % 
                (repr(self.targetNodePath.getPos(render)), 
                 repr(base.localAvatar.getPos(render)), 
                 repr(pos)))

        if item.getFlags() & CatalogFurnitureItem.FLPainting:
            # Paintings are started out on a wall.
            for object in self.objectDict.values():
                object.stashBuiltInCollisionNodes()
            self.gridSnapNP.iPosHpr()
            target = self.targetNodePath
            self.iRay.setParentNP(base.localAvatar)
            entry = self.iRay.pickBitMask3D(
                bitMask = ToontownGlobals.WallBitmask,
                targetNodePath = target,
                origin = Point3(0, 0, 6),
                dir = Vec3(0, 1, 0),
                skipFlags = SKIP_BACKFACE | SKIP_CAMERA | SKIP_UNPICKABLE)
            for object in self.objectDict.values():
                object.unstashBuiltInCollisionNodes()
            if entry:
                self.alignObject(entry, target, fClosest = 0, wallOffset = 0.1)

                pos = self.gridSnapNP.getPos(target)
                hpr = self.gridSnapNP.getHpr(target)
                assert self.notify.debug("painting placed on wall at %s, %s" % (repr(pos), repr(hpr)))
            else:
                self.notify.warning("wall not found for painting")

        self.furnitureManager.moveItemFromAttic(
            itemIndex, (pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2]),
            self.__bringItemFromAtticCallback)

    def __bringItemFromAtticCallback(self, retcode, dfitem, itemIndex):
        # Reset disabled buttons
        self.__enableItemButtons(1)

        # Add furniture to the room (and remove it from the attic).
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to bring furniture item %s into room, reason %s." % (itemIndex, retcode))
            return

        # No problem; the furniture was successfully added to the room.
        mo = self.loadObject(dfitem)
        objectId = mo.id()

        # Remove the item from the attic list and slide all the
        # subsequent items down (since that's what the AI did).
        self.atticItemPanels[itemIndex].destroy()
        del self.atticItemPanels[itemIndex]
        for i in range(itemIndex, len(self.atticItemPanels)):
            self.atticItemPanels[i].itemId -= 1

        # I don't understand DirectScrolledList.removeItem(), so
        # we'll just regenerate the list object for now.
        self.regenerateAtticPicker()

        # Also add the item to the inRoomPicker, if we have it
        # up.
        if self.inRoomPicker:
            panel = FurnitureItemPanel(dfitem.item, objectId,
                                       command = self.requestReturnToAttic,
                                       helpCategory = "FurnitureItemPanelRoom")
            self.inRoomPanels.append(panel)
            self.regenerateInRoomPicker()

    def deleteItemFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticItems[itemIndex])

        self.furnitureManager.deleteItemFromAttic(
            item, itemIndex,
            self.__deleteItemFromAtticCallback)

    def __deleteItemFromAtticCallback(self, retcode, item, itemIndex):
        # Reset disabled button
        self.__enableItemButtons(1)
        # Add furniture to the room (and remove it from the attic).
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to delete furniture item %s, reason %s." % (itemIndex, retcode))
            return

        # Remove the item from the attic list and slide all the
        # subsequent items down (since that's what the AI did).
        self.atticItemPanels[itemIndex].destroy()
        del self.atticItemPanels[itemIndex]
        for i in range(itemIndex, len(self.atticItemPanels)):
            self.atticItemPanels[i].itemId -= 1

        # I don't understand DirectScrolledList.removeItem(), so
        # we'll just regenerate the list object for now.
        self.regenerateAtticPicker()
            

    def bringWallpaperFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticWallpaper[itemIndex])

        # Make sure we can't press the button again until we hear from the AI
        self.__enableItemButtons(0)

        if self.deleteMode:
            self.requestDelete(item, itemIndex, self.deleteWallpaperFromAttic)
            return

        # For now, we have no way to ask the user which room he
        # wants to replace.

        # As a terrible hack, if the toon's position is left of the
        # room dividing line (about y == 2.3), we call it room 0;
        # otherwise, it's room 1.

        if (base.localAvatar.getY() < 2.3):
            room = 0
        else:
            room = 1

        self.furnitureManager.moveWallpaperFromAttic(
            itemIndex, room, self.__bringWallpaperFromAtticCallback)

    def __bringWallpaperFromAtticCallback(self, retcode, itemIndex, room):
        # Can clear disabledButton and verify panel now
        self.__enableItemButtons(1)

        # Add wallpaper to the room (and remove it from the attic).
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to bring wallpaper %s into room %s, reason %s." % (itemIndex, room, retcode))

            return

        # Replace the original item in the attic list (since that's
        # what the AI did).
        self.atticWallpaperPanels[itemIndex].destroy()
        item = self.furnitureManager.atticWallpaper[itemIndex]
        panel = FurnitureItemPanel(item, itemIndex,
                                   command = self.bringWallpaperFromAttic,
                                   deleteMode = self.deleteMode,
                                   helpCategory = "FurnitureItemPanelAttic")
        self.atticWallpaperPanels[itemIndex] = panel

        # Regenerate the scrolled list with the new panel in it.
        self.regenerateAtticPicker()

    def deleteWallpaperFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticWallpaper[itemIndex])

        self.furnitureManager.deleteWallpaperFromAttic(
            item, itemIndex,
            self.__deleteWallpaperFromAtticCallback)

    def __deleteWallpaperFromAtticCallback(self, retcode, item, itemIndex):
        # Reset disabled button
        self.__enableItemButtons(1)
        # Process error codes
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to delete wallpaper %s, reason %s." % (itemIndex, retcode))
            return

        # Remove the item from the attic list and slide all the
        # subsequent wallpapers down (since that's what the AI did).
        self.atticWallpaperPanels[itemIndex].destroy()
        del self.atticWallpaperPanels[itemIndex]
        for i in range(itemIndex, len(self.atticWallpaperPanels)):
            self.atticWallpaperPanels[i].itemId -= 1

        self.regenerateAtticPicker()

    def bringWindowFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticWindows[itemIndex])

        # Make sure we can't press the button again until we hear from the AI
        self.__enableItemButtons(0)

        if self.deleteMode:
            self.requestDelete(item, itemIndex, self.deleteWindowFromAttic)
            return

        # For now, we have no way to ask the user which window he
        # wants to replace.

        # As a terrible hack, if the toon's position is left of the
        # room dividing line (about y == 2.3), we call it slot 2;
        # otherwise, it's slot 4.

        if (base.localAvatar.getY() < 2.3):
            slot = 2
        else:
            slot = 4
        
        self.furnitureManager.moveWindowFromAttic(
            itemIndex, slot, self.__bringWindowFromAtticCallback)

    def __bringWindowFromAtticCallback(self, retcode, itemIndex, slot):
        # Can clear disabledButton since it was deleted above
        self.__enableItemButtons(1)

        # Add furniture to the room (and remove it from the attic).
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to bring window %s into slot %s, reason %s." % (itemIndex, slot, retcode))

            return

        if retcode == ToontownGlobals.FM_SwappedItem:
            # There was already a window in that slot.  Replace the
            # original item in the attic list (since that's what the
            # AI did).
            self.atticWindowPanels[itemIndex].destroy()
            item = self.furnitureManager.atticWindows[itemIndex]
            panel = FurnitureItemPanel(item, itemIndex,
                                       command = self.bringWindowFromAttic,
                                       deleteMode = self.deleteMode,
                                       helpCategory = "FurnitureItemPanelAttic")
            self.atticWindowPanels[itemIndex] = panel

        else:
            # There was not already a window in that slot.  Remove the
            # window item from the attic list (since that's what the
            # AI did).
            self.atticWindowPanels[itemIndex].destroy()
            del self.atticWindowPanels[itemIndex]
            for i in range(itemIndex, len(self.atticWindowPanels)):
                self.atticWindowPanels[i].itemId -= 1

        # Regenerate the scrolled list with the new panel in it.
        self.regenerateAtticPicker()

    def deleteWindowFromAttic(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.atticWindows[itemIndex])

        self.furnitureManager.deleteWindowFromAttic(
            item, itemIndex,
            self.__deleteWindowFromAtticCallback)

    def __deleteWindowFromAtticCallback(self, retcode, item, itemIndex):
        # Reset disabled button
        self.__enableItemButtons(1)
        # Process error codes
        if retcode < 0:
            # There was a problem.
            self.notify.info("Unable to delete window %s, reason %s." % (itemIndex, retcode))
            return

        # Remove the item from the attic list and slide all the
        # subsequent windows down (since that's what the AI did).
        self.atticWindowPanels[itemIndex].destroy()
        del self.atticWindowPanels[itemIndex]
        for i in range(itemIndex, len(self.atticWindowPanels)):
            self.atticWindowPanels[i].itemId -= 1

        self.regenerateAtticPicker()
        
    def setGridSpacingString(self, spacingStr):
        spacing = eval(spacingStr)
        self.setGridSpacing(spacing)

    def setGridSpacing(self, gridSpacing):
        self.gridSpacing = gridSpacing

    def makeHouseExtentsBox(self):
        houseGeom = self.targetNodePath.findAllMatches('**/group*')
        targetBounds = houseGeom.getTightBounds()
        # Make sure each object has a consistent collision box
        # Node path for holding generated collision solids
        self.houseExtents = self.targetNodePath.attachNewNode(
            'furnitureCollisionNode')
        # Get coords of bounding box
        mx = targetBounds[0][0]
        Mx = targetBounds[1][0]
        my = targetBounds[0][1]
        My = targetBounds[1][1]
        mz = targetBounds[0][2]
        Mz = targetBounds[1][2]
        # Make four collision polys for the side of the box
        # using the ToontownGlobals.GhostBitmask
        cn = CollisionNode('extentsCollisionNode')
        cn.setIntoCollideMask(ToontownGlobals.GhostBitmask)

        self.houseExtents.attachNewNode(cn)
        # Min X face
        cp = CollisionPolygon(Point3(mx,my,mz),
                              Point3(mx,My,mz),
                              Point3(mx,My,Mz),
                              Point3(mx,my,Mz))
        cn.addSolid(cp)
        # Max X face
        cp = CollisionPolygon(Point3(Mx,My,mz),
                              Point3(Mx,my,mz),
                              Point3(Mx,my,Mz),
                              Point3(Mx,My,Mz))
        cn.addSolid(cp)
        # Min Y face
        cp = CollisionPolygon(Point3(Mx,my,mz),
                              Point3(mx,my,mz),
                              Point3(mx,my,Mz),
                              Point3(Mx,my,Mz))
        cn.addSolid(cp)
        # Max Y face
        cp = CollisionPolygon(Point3(mx,My,mz),
                              Point3(Mx,My,mz),
                              Point3(Mx,My,Mz),
                              Point3(mx,My,Mz))
        cn.addSolid(cp)

    def makeDoorBlocker(self):
        # Make sphere to prevent people from placing geometry in doorway
        self.doorBlocker = self.targetNodePath.attachNewNode('doorBlocker')
        cn = CollisionNode('doorBlockerCollisionNode')
        cn.setIntoCollideMask(ToontownGlobals.FurnitureSideBitmask)
        self.doorBlocker.attachNewNode(cn)
        # Sphere filling up entry way
        cs = CollisionSphere(Point3(-12,-33,0), 7.5)
        cn.addSolid(cs)

    def createVerifyDialog(self, item, verifyText, okFunc, cancelFunc):
        if self.verifyFrame == None:
            buttons = loader.loadModel(
                'phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'),
                             buttons.find('**/ChtBx_OKBtn_DN'),
                             buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (buttons.find('**/CloseBtn_UP'),
                                 buttons.find('**/CloseBtn_DN'),
                                 buttons.find('**/CloseBtn_Rllvr'))
            self.verifyFrame = DirectFrame(
                pos = (-0.4, 0.1, 0.3),
                scale = 0.75,
                relief = None,
                image = DGG.getDefaultDialogGeom(),
                image_color = ToontownGlobals.GlobalDialogColor,
                image_scale = (1.2, 1, 1.3),
                text = '',
                text_wordwrap = 19,
                text_scale = 0.06,
                text_pos = (0, 0.5),
                textMayChange = 1,
                sortOrder = NO_FADE_SORT_INDEX,
                )
            self.okButton = DirectButton(
                parent = self.verifyFrame,
                image = okButtonImage,
                relief = None,
                text = OTPLocalizer.DialogOK,
                text_scale = 0.05,
                text_pos = (0.0, -0.1),
                textMayChange = 0,
                pos = (-0.22, 0.0, -0.5))
            self.cancelButton = DirectButton(
                parent = self.verifyFrame,
                image = cancelButtonImage,
                relief = None,
                text = OTPLocalizer.DialogCancel,
                text_scale = 0.05,
                text_pos = (0.0, -0.1),
                textMayChange = 0,
                pos = (0.22, 0.0, -0.5))
            self.deleteItemText = DirectLabel(
                parent = self.verifyFrame,
                relief = None,
                text = '',
                text_wordwrap = 16,
                pos = (0.0, 0.0, -0.4),
                scale = 0.09,
                )

        # Update text here (in case verify frame already exists)
        self.verifyFrame['text'] = verifyText
        self.deleteItemText['text'] = item.getName()
        self.okButton['command'] = okFunc
        self.cancelButton['command'] = cancelFunc
        self.verifyFrame.show()

        # Update picture
        self.itemPanel, self.itemIval = item.getPicture(base.localAvatar)
        if self.itemPanel:
            # Ensure the item panel is behind any other text.
            self.itemPanel.reparentTo(self.verifyFrame, -1)
            self.itemPanel.setPos(0, 0, 0.05)
            self.itemPanel.setScale(0.35)
            self.deleteItemText.setPos(0.0, 0.0, -0.4)
        else:
            # There's no picture for this item.  Scooch the item text
            # up to fill up the space.
            self.deleteItemText.setPos(0, 0, 0.07)

        if self.itemIval:
            self.itemIval.loop()

    def __handleVerifyDeleteOK(self):
        deleteFunction = self.verifyItems[0]
        # Copy args before deleting them
        deleteFunctionArgs = self.verifyItems[1:]
        self.__cleanupVerifyDelete()
        deleteFunction(*deleteFunctionArgs)

    def __cleanupVerifyDelete(self, *args):
        if self.nonDeletableItem:
            self.nonDeletableItem.cleanup()
            self.nonDeletableItem = None
        if self.verifyFrame:
            self.verifyFrame.hide()
        if self.itemIval:
            self.itemIval.finish()
            self.itemIval = None
        if self.itemPanel:
            self.itemPanel.destroy()
            self.itemPanel = None
        self.verifyItems = None

    def __enableItemButtons(self, enabled):
        """ Enable or disable all item panels. """
        self.notify.debug("__enableItemButtons %d" % enabled)

        if enabled:
            buttonState = DGG.NORMAL
        else:
            buttonState = DGG.DISABLED
        
        # Also control paging between pickers to prevent exceptions if you
        # switch pickers while waiting for an AI response.
        if hasattr(self, 'inAtticButton'):
            self.inAtticButton['state'] = buttonState
        if hasattr(self, 'inRoomButton'):
            self.inRoomButton['state'] = buttonState
        if hasattr(self, 'inTrashButton'):
            self.inTrashButton['state'] = buttonState
        
        # Update the enabled state of all panels.
        pickers = [self.atticPicker,
                   self.inRoomPicker,
                   self.inTrashPicker
                  ]
       
        for picker in pickers:
            if picker:
                for panel in picker['items']:
                    if not panel.isEmpty():
                        panel.enable(enabled)
    
    def __resetAndCleanup(self, *args):
        self.__enableItemButtons(1)
        self.__cleanupVerifyDelete()

    def requestDelete(self, item, itemIndex, deleteFunction):
        # prompt the user to verify delete
        self.__cleanupVerifyDelete()

        if self.furnitureManager.ownerId != base.localAvatar.doId or \
           not item.isDeletable():
            self.warnNonDeletableItem(item)
            return

        self.createVerifyDialog(item, TTLocalizer.HDDeleteItem,
                                self.__handleVerifyDeleteOK,
                                self.__resetAndCleanup)
        self.verifyItems = (deleteFunction, item, itemIndex)

    def requestRoomDelete(self, dfitem, objectId, itemIndex):
        # prompt the user to verify delete
        self.__cleanupVerifyDelete()
        item = dfitem.item
        if self.furnitureManager.ownerId != base.localAvatar.doId or \
           not item.isDeletable():
            self.warnNonDeletableItem(item)
            return
        self.createVerifyDialog(item, TTLocalizer.HDDeleteItem,
                                self.__handleVerifyDeleteOK,
                                self.__resetAndCleanup)
        self.verifyItems = (self.deleteItemFromRoom, dfitem, objectId, itemIndex)

    def warnNonDeletableItem(self, item):
        message = TTLocalizer.HDNonDeletableItem
        if not item.isDeletable():
            if item.getFlags() & CatalogFurnitureItem.FLBank:
                message = TTLocalizer.HDNonDeletableBank
            elif item.getFlags() & CatalogFurnitureItem.FLCloset:
                message = TTLocalizer.HDNonDeletableCloset
            elif item.getFlags() & CatalogFurnitureItem.FLPhone:
                message = TTLocalizer.HDNonDeletablePhone

        if self.furnitureManager.ownerId != base.localAvatar.doId:
            message = TTLocalizer.HDNonDeletableNotOwner % (self.furnitureManager.ownerName)
            
        self.nonDeletableItem = TTDialog.TTDialog(
            text = message,
            style = TTDialog.Acknowledge,
            fadeScreen = 0,
            command = self.__resetAndCleanup)
        self.nonDeletableItem.show()

    def requestReturnToAttic(self, item, objectId):
        # prompt the user to verify delete
        self.__cleanupVerifyDelete()

        # Figure out which button is associated with this item and disable it
        itemIndex = None
        for i in range(len(self.inRoomPanels)):
            if self.inRoomPanels[i].itemId == objectId:
                itemIndex = i
                # Make sure we can't press the button again
                # until we hear from the AI
                self.__enableItemButtons(0)
                break

        if self.deleteMode:
            dfitem = self.objectDict[objectId].dfitem
            self.requestRoomDelete(dfitem, objectId, itemIndex)
            return

        self.createVerifyDialog(item, TTLocalizer.HDReturnVerify,
                                self.__handleVerifyReturnOK,
                                self.__resetAndCleanup)
        self.verifyItems = (item, objectId)

    def __handleVerifyReturnOK(self):
        item, objectId = self.verifyItems
        self.__cleanupVerifyDelete()
        self.pickInRoom(objectId)
        self.sendItemToAttic()

    def requestReturnToAtticFromTrash(self, item, itemIndex):
        # prompt the user to verify delete
        self.__cleanupVerifyDelete()

        # Make sure we can't press the button again until we hear from the AI
        self.__enableItemButtons(0)

        # Popup verify panel
        self.createVerifyDialog(item, TTLocalizer.HDReturnFromTrashVerify,
                                self.__handleVerifyReturnFromTrashOK,
                                self.__resetAndCleanup)
        self.verifyItems = (item, itemIndex)

    def __handleVerifyReturnFromTrashOK(self):
        item, itemIndex = self.verifyItems
        self.__cleanupVerifyDelete()
        self.recoverDeletedItem(item, itemIndex)

    def recoverDeletedItem(self, item, itemIndex):
        messenger.send('wakeup')
        assert(item == self.furnitureManager.deletedItems[itemIndex])
        self.furnitureManager.recoverDeletedItem(
            item, itemIndex, self.__recoverDeletedItemCallback)

    def __recoverDeletedItemCallback(self, retcode, item, itemIndex):
        # Clean up dialog
        self.__cleanupVerifyDelete()
        # Process errors
        if retcode < 0:
            # There was a problem.
            if retcode == ToontownGlobals.FM_HouseFull:
                # No room in the attic.
                self.showHouseFullDialog()
            self.notify.info("Unable to recover deleted item %s, reason %s." %
                             (itemIndex, retcode))
            return

        # Restore button before deleting it
        self.__enableItemButtons(1)

        # Remove the item from the in trash list and slide all the
        # subsequent windows down (since that's what the AI did).
        self.inTrashPanels[itemIndex].destroy()
        del self.inTrashPanels[itemIndex]
        for i in range(itemIndex, len(self.inTrashPanels)):
            self.inTrashPanels[i].itemId -= 1
        self.regenerateInTrashPicker()

        # Create panel with appropriate bring from attic command
        itemType = item.getTypeCode()
        if ((itemType == CatalogItemTypes.WALLPAPER_ITEM) or
            (itemType == CatalogItemTypes.FLOORING_ITEM) or
            (itemType == CatalogItemTypes.MOULDING_ITEM) or
            (itemType == CatalogItemTypes.WAINSCOTING_ITEM)):
            itemIndex = len(self.atticWallpaperPanels)
            assert(item == self.furnitureManager.atticWallpaper[itemIndex])
            bringCommand = self.bringWallpaperFromAttic
        elif itemType == CatalogItemTypes.WINDOW_ITEM:
            itemIndex = len(self.atticWindowPanels)
            assert(item == self.furnitureManager.atticWindows[itemIndex])
            bringCommand = self.bringWindowFromAttic
        else:
            itemIndex = len(self.atticItemPanels)
            assert(item == self.furnitureManager.atticItems[itemIndex])
            bringCommand = self.bringItemFromAttic
        panel = FurnitureItemPanel(item, itemIndex,
                                   command = bringCommand,
                                   deleteMode = self.deleteMode,
                                   helpCategory = "FurnitureItemPanelAttic")

        # Add panel to appropriate list
        if ((itemType == CatalogItemTypes.WALLPAPER_ITEM) or
            (itemType == CatalogItemTypes.FLOORING_ITEM) or
            (itemType == CatalogItemTypes.MOULDING_ITEM) or
            (itemType == CatalogItemTypes.WAINSCOTING_ITEM)):
            self.atticWallpaperPanels.append(panel)
        elif itemType == CatalogItemTypes.WINDOW_ITEM:
            self.atticWindowPanels.append(panel)
        else:
            self.atticItemPanels.append(panel)

        # DistributedScrolledList.addItem() has some issues.  For now,
        # just regenerate the list object.
        self.regenerateAtticPicker()

    def showHouseFullDialog(self):
        self.cleanupDialog()
        self.dialog = TTDialog.TTDialog(
            style = TTDialog.Acknowledge,
            text = TTLocalizer.HDHouseFull,
            text_wordwrap = 15,
            command = self.cleanupDialog,
            )
        self.dialog.show()
    
    def bindHelpText(self, button, category):
        # No item names are needed here
        button.bind(DGG.ENTER, self.showHelpText, extraArgs=[category, None])
        button.bind(DGG.EXIT, self.hideHelpText)
        
    def showHelpText(self, category, itemName, xy):

        def showIt(task):            
            helpText = TTLocalizer.HDHelpDict.get(category)
            if helpText:
                if itemName:
                    helpText = helpText % itemName
                self.helpText['text'] = helpText
                self.helpText.show()
            else:
                print "category: %s not found"

        # Give it a pause before displaying
        taskMgr.doMethodLater(0.75, showIt, "showHelpTextDoLater")

    def hideHelpText(self, xy):
        taskMgr.remove("showHelpTextDoLater")
        self.helpText['text'] = ''
        self.helpText.hide()
