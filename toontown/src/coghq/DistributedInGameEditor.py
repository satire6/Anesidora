from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import lineInfo, Functor
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.level import Level
from otp.level import LevelConstants
from otp.level import Entity
from otp.level import EditMgr
# this is required in order to eval the incoming spec repr string
from SpecImports import *
from InGameEditorElements import *
#import FactoryEntityCreator
from toontown.cogdominium import CogdoEntityCreator
import string

class InGameEditorEntityBase(InGameEditorElement):
    """ base class for editor entities that are also level Elements """
    def __init__(self):
        InGameEditorElement.__init__(self)

    def attribChanged(self, attrib, value):
        """this is called when one of our attributes changes"""
        Entity.Entity.attribChanged(self, attrib, value)
        print 'attribChange: %s %s, %s = %s' % (
            self.level.getEntityType(self.entId), self.entId,
            attrib, repr(value))

    # editor InGameEditorElement methods
    def getTypeName(self):
        return self.level.getEntityType(self.entId)

    def privGetNamePrefix(self):
        return '[%s-%s] ' % (self.getTypeName(), self.entId)

    def privGetEntityName(self):
        return self.level.levelSpec.getEntitySpec(self.entId)['name']

    def getName(self):
        return '%s%s' % (self.privGetNamePrefix(), self.privGetEntityName())

    def setNewName(self, newName):
        # OK, user typed in a new name. For now, assume that they either
        # deleted the prefix or left it intact
        prefix = self.privGetNamePrefix()
        # if prefix matches, remove it
        if newName[:len(prefix)] == prefix:
            newName = newName[len(prefix):]
        # if different, send out a name change
        oldName = self.privGetEntityName()
        if oldName != newName:
            self.level.setAttribEdit(self.entId, 'name', newName)

    def setParentEntId(self, parentEntId):
        self.parentEntId = parentEntId
        self.level.buildEntityTree()

    def setName(self, name):
        self.name = name
        self.level.buildEntityTree()

class InGameEditorEntity(Entity.Entity, InGameEditorEntityBase):
    """this is the in-game editor's representation of an entity"""
    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)

    def id(self):
        return self.entId

    def destroy(self):
        Entity.Entity.destroy(self)

# we need a real editMgr
class InGameEditorEditMgr(EditMgr.EditMgr, InGameEditorEntityBase):
    def __init__(self, level, entId):
        EditMgr.EditMgr.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)
    def destroy(self):
        EditMgr.EditMgr.destroy(self)

class AttribModifier(Entity.Entity, InGameEditorEntityBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('AttribModifier')    
    def __init__(self, level, entId):
        Entity.Entity.__init__(self, level, entId)
        InGameEditorEntityBase.__init__(self)
    def destroy(self):
        Entity.Entity.destroy(self)
    def setValue(self, value):
        # here's the magic. Start at our parent, and modify the attributes.
        # If recursive, work through all children.
        # check entity typeName
        if len(self.typeName) == 0:
            AttribModifier.notify.warning('no typeName set')
            return
        entTypeReg = self.level.entTypeReg
        if self.typeName not in entTypeReg.getAllTypeNames():
            AttribModifier.notify.warning('invalid typeName: %s' % self.typeName)
            return
        typeDesc = entTypeReg.getTypeDesc(self.typeName)
        # check attribName
        if len(self.attribName) == 0:
            AttribModifier.notify.warning('no attribName set')
            return
        if self.attribName not in typeDesc.getAttribNames():
            AttribModifier.notify.warning(
                'invalid attribName: %s' % self.attribName)
            return
        # check value
        if len(value) == 0:
            AttribModifier.notify.warning('no value set')
        # TODO: check that it's valid Python, check that it evals and reprs,
        # check that it's the right type for the attrib

        # OK, let's get going
        def setAttrib(entId, typeName=self.typeName, attribName=self.attribName,
                      value=eval(value), recursive=self.recursive):
            # if this entity is of the right type, set the value
            if typeName == self.level.getEntityType(entId):
                self.level.setAttribEdit(entId, attribName, value)
            # if recursive, continue on to each child
            if recursive:
                entity = self.level.getEntity(entId)
                for child in entity.getChildren():
                    setAttrib(child.entId)
        setAttrib(self.parentEntId)

## class InGameEditorEntityCreator(FactoryEntityCreator.FactoryEntityCreator):
##     """this is a factory entity creator hijacked to create editor-specific
##     entity classes for all of its types"""
##     def __init__(self, level):
##         FactoryEntityCreator.FactoryEntityCreator.__init__(self, level)
##         # it's a little dirty to be reaching down directly into
##         # EntityCreatorBase like this. But I'm over it.
##         entTypes = self.entType2Ctor.keys()
##         for type in entTypes:
##             self.entType2Ctor[type] = InGameEditorEntity
##         # we need a real editMgr
##         self.entType2Ctor['editMgr'] = InGameEditorEditMgr
##         # and we have AttribModifiers
##         self.entType2Ctor['attribModifier'] = AttribModifier

def getInGameEditorEntityCreatorClass(level):
    entCreator = level.createEntityCreator()
    EntCreatorClass = entCreator.__class__
    class InGameEditorEntityCreator(EntCreatorClass):
        """this is a factory entity creator hijacked to create editor-specific
        entity classes for all of its types"""
        def __init__(self, editor):
            EntCreatorClass.__init__(self, editor)
            # it's a little dirty to be reaching down directly into
            # EntityCreatorBase like this. But I'm over it.
            entTypes = self.entType2Ctor.keys()
            for type in entTypes:
                self.entType2Ctor[type] = InGameEditorEntity
            # we need a real editMgr
            self.entType2Ctor['editMgr'] = InGameEditorEditMgr
            # and we have AttribModifiers
            self.entType2Ctor['attribModifier'] = AttribModifier
    return InGameEditorEntityCreator

"""
class InGameEditorEntityCreator:
    # this is an entity creator hijacked to create editor-specific
    # entity classes for all of its types
    def __init__(self, editor):
        self.__dict__['_impl'] = editor.level.createEntityCreator()
        # it's a little dirty to be reaching down directly into
        # EntityCreatorBase like this. But I'm over it.
        entTypes = self.__dict__['_impl'].entType2Ctor.keys()
        for type in entTypes:
            self.__dict__['_impl'].entType2Ctor[type] = InGameEditorEntity
        # we need a real editMgr
        self.__dict__['_impl'].entType2Ctor['editMgr'] = InGameEditorEditMgr
        # and we have AttribModifiers
        self.__dict__['_impl'].entType2Ctor['attribModifier'] = AttribModifier

    def __getattr__(self, attrName):
        if hasattr(self.__dict__['_impl'], attrName):
            return getattr(self.__dict__['_impl'], attrName)
        if attrName in self.__dict__:
            return self.__dict__[attrName]
        return self.__class__.__dict__[attrName]

    def __setattr__(self, attrName, value):
        setattr(self.__dict__['_impl'], attrName, value)
"""

class DistributedInGameEditor(DistributedObject.DistributedObject,
                              Level.Level,
                              InGameEditorElement):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedInGameEditor')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        Level.Level.__init__(self)
        InGameEditorElement.__init__(self)
        self.editorInitialized = 0
        self.specModified = 0
        
        # these are stacks of
        # ([actions to get from new state to old state (undo)],
        #  [actions to get from old state to new state (redo)])
        # each action is functor or (entId, attrib, value)
        self.undoStack = []
        self.redoStack = []

        # this is a FIFO of callbacks to handle entity creation events
        # for entities we requested; callbacks must accept entId
        self.entCreateHandlerQ = []

        # FIFO of entIds of entities that we created
        self.entitiesWeCreated = []

        # Dictionary relating nodePath id (if entity has a nodepath) to
        # entity id
        self.nodePathId2EntId = {}

    def generate(self):
        self.notify.debug('generate')
        DistributedObject.DistributedObject.generate(self)
        # NOTE: this code will run for all clients, not just the editing client
        # put any real init functionality below in gotCurrentSpec()
        base.inGameEditor = self

    # required fields
    def setEditorAvId(self, editorAvId):
        self.editorAvId = editorAvId

    def setEditUsername(self, editUsername):
        self.editUsername = editUsername

    def getEditUsername(self):
        return self.editUsername
        
    def setLevelDoId(self, levelDoId):
        self.levelDoId = levelDoId
        self.level = base.cr.doId2do[self.levelDoId]

    def getLevelDoId(self):
        return self.levelDoId

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        DistributedObject.DistributedObject.announceGenerate(self)

        # load stuff
        if self.editorIsLocalToon():
            # make sure we're set up for editing
            from otp.level import EditorGlobals
            EditorGlobals.assertReadyToEdit()
            assert self.editUsername == EditorGlobals.getEditUsername()
            
            # ask for the current spec; it will arrive in pieces, since
            # it's so large
            self.notify.debug('requesting an up-to-date copy of the level spec')
            self.sendUpdate('requestCurrentLevelSpec')

    def setSpecSenderDoId(self, doId):
        DistributedInGameEditor.notify.debug('setSpecSenderDoId: %s' % doId)
        blobSender = base.cr.doId2do[doId]

        def setSpecBlob(specBlob, blobSender=blobSender, self=self):
            blobSender.sendAck()
            from otp.level.LevelSpec import LevelSpec
            curSpec = eval(specBlob)
            self.gotCurrentSpec(curSpec)

        if blobSender.isComplete():
            setSpecBlob(blobSender.getBlob())
        else:
            evtName = self.uniqueName('specDone')
            blobSender.setDoneEvent(evtName)
            self.acceptOnce(evtName, setSpecBlob)

    def gotCurrentSpec(self, curSpec):
        self.entTypeReg = self.level.getEntityTypeReg()

        curSpec.setEntityTypeReg(self.entTypeReg)

        # for showing entities
        self.axis = loader.loadModel("models/misc/xyzAxis.bam")
        self.axis.setColorOff()
        # last 1 overrides default colorScale
        self.axis.setColorScale(1,1,1,1,1)

        ## by default, color the zones
        #self.level.setColorZones(1)

        # init the Level; this will create all the entities
        self.initializeLevel(self.doId, curSpec, curSpec.getScenario())

        # maybe this should come from the actual level object? or from the AI?
        entCreator = self.level.createEntityCreator()
        self.entTypes = entCreator.getEntityTypes()

        self.selectedEntity = None

        base.startTk()
        import InGameEditor
        doneEvent = self.uniqueName('editorDone')
        saveAsEvent = self.uniqueName('saveSpec')
        requestSaveEvent = self.uniqueName('requestSpecSave')
        undoEvent = self.uniqueName('undoEvent')
        redoEvent = self.uniqueName('redoEvent')
        wireframeEvent = self.uniqueName('wireframeEvent')
        oobeEvent = self.uniqueName('oobeEvent')
        csEvent = self.uniqueName('csEvent')
        runEvent = self.uniqueName('runEvent')
        texEvent = self.uniqueName('texEvent')
        self.editor = InGameEditor.InGameEditor(
            level=self,
            doneEvent=doneEvent,
            requestSaveEvent=requestSaveEvent,
            saveAsEvent=saveAsEvent,
            undoEvent=undoEvent,
            redoEvent=redoEvent,
            wireframeEvent=wireframeEvent,
            oobeEvent=oobeEvent,
            csEvent=csEvent,
            runEvent=runEvent,
            texEvent=texEvent,
            )
        self.acceptOnce(doneEvent, self.doneEditing)
        self.accept(saveAsEvent, self.saveSpec)
        self.accept(requestSaveEvent, self.requestSpecSave)
        self.accept(undoEvent, self.doUndo)
        self.accept(redoEvent, self.doRedo)
        self.accept(wireframeEvent, self.doWireframe)
        self.accept(oobeEvent, self.doOobe)
        self.accept(csEvent, self.doCs)
        self.accept(runEvent, self.doRun)
        self.accept(texEvent, self.doTex)

        self.accept(self.editor.getEventMsgName('Select'),
                    self.handleEntitySelect)
        self.accept(self.editor.getEventMsgName('Flash'),
                    self.handleEntitySelect)
        
        self.editorInitialized = 1
        self.buildEntityTree()

    def editorIsLocalToon(self):
        """returns true if we own this editor"""
        return self.editorAvId == base.localAvatar.doId

    def createEntityCreator(self):
        return getInGameEditorEntityCreatorClass(self.level)(self)

    def doneEditing(self):
        self.notify.debug('doneEditing')
        assert self.editorIsLocalToon()
        if self.specModified:
            if self.editor.askYesNo('Save the spec on the AI?'):
                self.requestSpecSave()
        self.sendUpdate('setFinished')

    def disable(self):
        self.notify.debug('disable')

        if self.editorInitialized and self.editorIsLocalToon():
            self.axis.removeNode()
            del self.axis

            if hasattr(self, 'entTypeReg'):
                del self.entTypeReg

            self.editorInitialized = 0
            Level.Level.destroyLevel(self)

            if hasattr(self, 'editor'):
                self.editor.quit()
                del self.editor

        DistributedObject.DistributedObject.disable(self)

        self.ignoreAll()

    def getEntInstance(self, entId):
        """ get the actual instance of an entity from the actual level;
        might return None """
        return self.level.getEntity(entId)

    def getEntInstanceNP(self, entId):
        """ get the nodepath that represents an entity from the actual
        level; might return None """
        entity = self.getEntInstance(entId)
        if entity is None:
            return None
        if isinstance(entity, NodePath):
            return entity
        if hasattr(entity, 'getNodePath'):
            return entity.getNodePath()
        # not a visible entity?
        return None

    def getEntInstanceNPCopy(self, entId):
        """ get a copy of the nodepath that represents an entity from
        the actual level; might return None. Caller is responsible
        for removing the copy.
        """
        np = self.getEntInstanceNP(entId)
        if np is None:
            return np

        stashNodeGroups = []
        searches = (
            '**/+ActorNode',
            '**/+Character',
            #'**/+CollisionNode',
            #'**/+LODNode',
            #'**/+Nametag3d',
            )
        # stash nodes to avoid crashes when copying
        for search in searches:
            stashNodeGroups.append(np.findAllMatches(search))

        for group in stashNodeGroups:
            if not group.isEmpty():
                group.stash()

        par = np.getParent()
        copy = np.copyTo(par)

        for group in stashNodeGroups:
            if not group.isEmpty():
                group.unstash()
        
        return copy

    def saveSpec(self, filename):
        return self.levelSpec.saveToDisk(filename)
        
    def setEntityParent(self, entity, parent):
        parent.addChild(entity)
        entity._parentEntity = parent

    def insertEntityIntoTree(self, entId):
        ent = self.getEntity(entId)

        # TODO: should the UberZone be the tree root?
        # if it's the UberZone, put it under self
        if (entId == LevelConstants.UberZoneEntId):
            self.setEntityParent(ent, self)
            return

        parentEnt = self.getEntity(ent.parentEntId)
        if parentEnt is not None:
            self.setEntityParent(ent, parentEnt)
            return

        # TODO: left-pane parent info should coincide with entities'
        # parent entries, but there should be a separate left-pane parent
        # registry on the spec object to allow non-parented entities
        # to be parented anywhere in the editor

        # everything else goes under the UberZone.
        self.setEntityParent(ent, self.uberZoneEntity)

    def buildEntityTree(self):
        # clear out all heirarchy
        self.setChildren([])
        entIds = self.entities.keys()
        entIds.sort()
        for entId in entIds:
            ent = self.getEntity(entId)
            ent.setChildren([])
        for entId in entIds:
            self.insertEntityIntoTree(entId)
        self.editor.refreshExplorer()

    def onEntityCreate(self, entId):
        DistributedInGameEditor.notify.debug('onEntityCreate %s' % entId)
        Level.Level.onEntityCreate(self, entId)

        entityNP = self.getEntInstanceNP(entId)
        if entityNP:
            self.nodePathId2EntId[entityNP.id()] = entId

        if not self.editorInitialized:
            return

        self.insertEntityIntoTree(entId)
        self.editor.refreshExplorer()

        if entId == self.entitiesWeCreated[0]:
            self.entitiesWeCreated = self.entitiesWeCreated[1:]
            self.editor.selectEntity(entId)

    def onEntityDestroy(self, entId):
        DistributedInGameEditor.notify.debug('onEntityDestroy %s' % entId)
        ent = self.getEntity(entId)

        if self.editorInitialized:
            # Remove from nodePath dict
            entityNP = self.getEntInstanceNP(entId)
            if entityNP in self.nodePathId2EntId:
                del self.nodePathId2EntId[entityNP.id()]

            if ent is self.selectedEntity:
                self.editor.clearAttribEditPane()
                self.selectedEntity = None
            ent._parentEntity.removeChild(ent)
            del ent._parentEntity

            self.editor.refreshExplorer()

        Level.Level.onEntityDestroy(self, entId)

    def handleEntitySelect(self, entity):
        self.selectedEntity = entity
        if hasattr(self, 'identifyIval'):
            self.identifyIval.finish()
        if entity is self:
            self.editor.clearAttribEditPane()
        else:
            entityNP = self.getEntInstanceNP(entity.entId)
            if entityNP is not None:
                dur = float(.5)
                oColor = entityNP.getColorScale()
                flashIval = Sequence(
                    Func(Functor(entityNP.setColorScale, 1, 0, 0, 1)),
                    WaitInterval(dur/3),
                    Func(Functor(entityNP.setColorScale, 0, 1, 0, 1)),
                    WaitInterval(dur/3),
                    Func(Functor(entityNP.setColorScale, 0, 0, 1, 1)),
                    WaitInterval(dur/3),
                    Func(Functor(entityNP.setColorScale, oColor[0], oColor[1], oColor[2], oColor[3])),#Func(entityNP.clearColorScale),
                    )
                boundIval = Sequence(
                    Func(entityNP.showBounds),
                    WaitInterval(dur*.5),
                    Func(entityNP.hideBounds),
                    )
                entCp = self.getEntInstanceNPCopy(entity.entId)
                entCp.setRenderModeWireframe()
                entCp.setTextureOff(1)
                wireIval = Sequence(
                    Func(Functor(entCp.setColor,1,0,0,1,1)),
                    WaitInterval(dur/3),
                    Func(Functor(entCp.setColor,0,1,0,1,1)),
                    WaitInterval(dur/3),
                    Func(Functor(entCp.setColor,0,0,1,1,1)),
                    WaitInterval(dur/3),
                    Func(entCp.removeNode),
                    )
                self.identifyIval = Parallel(
                    flashIval,
                    boundIval,
                    wireIval,
                    )
                def putAxis(self=self, entityNP=entityNP):
                    self.axis.reparentTo(entityNP)
                    self.axis.setPos(0,0,0)
                    self.axis.setHpr(0,0,0)
                def takeAxis(self=self):
                    self.axis.reparentTo(hidden)
                self.identifyIval = Sequence(
                    Func(putAxis),
                    Parallel(self.identifyIval,
                             WaitInterval(1000.5), #leaving the axis around JML
                             ),
                    Func(takeAxis),
                    )
                self.identifyIval.start()
            self.editor.updateAttribEditPane(entity.entId, self.levelSpec,
                                             self.entTypeReg)

            # Disable remove menu button for permanent entities
            entType = self.getEntityType(entity.entId)
            # Get the menu that needs to be disabled
            menu = self.editor.menuBar.component('Entity-menu')
            # Get the index of the remove command
            index = menu.index('Remove Selected Entity')
            if entType in self.entTypeReg.getPermanentTypeNames():
                menu.entryconfigure(index,state='disabled')
            else:
                menu.entryconfigure(index,state='normal')

    def privSendAttribEdit(self, entId, attrib, value):
        """this sends an edit to the AI; it does not manipulate the
        undo/redo stacks"""
        # This is a proposed change; it has not been approved yet.
        # Send it up to the AI. We will get a response with a new value
        # for the attribute; it may not be the value we are suggesting.
        self.specModified = 1
        valueStr = repr(value)
        self.notify.debug("sending edit: %s: '%s' = %s" %
                          (entId, attrib, valueStr))
        self.sendUpdate('setEdit', [entId, attrib, valueStr, self.editUsername])

    def privExecActionList(self, actions):
        """execute an undo/redo action list"""
        for action in actions:
            if callable(action):
                action()
            else:
                entId, attrib, value = action
                self.privSendAttribEdit(entId, attrib, value)

    def setUndoableAttribEdit(self, old2new, new2old):
        """old2new is list of actions to do op,
        new2old is list of actions to undo op"""
        self.redoStack = []
        self.undoStack.append((new2old, old2new))
        self.privExecActionList(old2new)

    def setAttribEdit(self, entId, attrib, value, canUndo=1):
        # this func should be used for run-of-the-mill (right-pane)
        # attribute edits
        oldValue = eval(repr(self.levelSpec.getEntitySpec(entId)[attrib]))
        new2old = [(entId, attrib, oldValue)]
        old2new = [(entId, attrib, value)]
        self.setUndoableAttribEdit(old2new, new2old)
        # temp hack for edits that are not simple to undo
        if not canUndo:
            self.undoStack = []

    def doUndo(self):
        if len(self.undoStack) == 0:
            self.editor.showWarning('Nothing left to undo')
            return
        undo = self.undoStack.pop()
        self.redoStack.append(undo)
        new2old, old2new = undo
        self.privExecActionList(new2old)

    def doRedo(self):
        if len(self.redoStack) == 0:
            self.editor.showWarning('Nothing to redo')
            return
        redo = self.redoStack.pop()
        self.undoStack.append(redo)
        new2old, old2new = redo
        self.privExecActionList(old2new)

    def doWireframe(self):
        messenger.send('magicWord', ['~wire'])
    def doOobe(self):
        messenger.send('magicWord', ['~oobe'])
    def doCs(self):
        messenger.send('magicWord', ['~cs'])
    def doRun(self):
        messenger.send('magicWord', ['~run'])
    def doTex(self):
        messenger.send('magicWord', ['~tex'])

    def insertEntity(self, entType, parentEntId=None, callback=None):
        # request insertion of an instance of this type of entity
        # under the currently-selected entity
        # if supplied, callback will be called with new ent's entId
        # !!!BUT entity will not yet exist!!!
        # you can call Level.getEntityCreateEvent to listen for creation
        if parentEntId is None:
            try:
                # TODO: check if it's a NodePath entity; nodepaths can only
                # be parented to nodepaths
                parentEntId = self.selectedEntity.entId
            except AttributeError:
                self.editor.showWarning(
                    'Please select a valid parent entity first.',
                    'error',)
                return

        # we don't know the entId yet; fill in when we do know
        removeAction = (self.editMgrEntity.entId,
                        'removeEntity',
                        {'entId':'REPLACEME'},
                        )
        new2old = [removeAction,]
        def setNewEntityId(entId, self=self, action=removeAction,
                           callback=callback):
            action[2]['entId'] = entId
            if callback:
                callback(entId)
        def setEntCreateHandler(self=self, handler=setNewEntityId):
            self.entCreateHandlerQ.append(handler)
        old2new = [setEntCreateHandler,
                   (self.editMgrEntity.entId, 'requestNewEntity',
                    {'entType': entType,
                     'parentEntId': parentEntId,
                     # add this so we can determine which new entities
                     # are the ones we requested
                     'username': self.editUsername,
                     })]
        self.setUndoableAttribEdit(old2new, new2old)

    def setEntityCreatorUsername(self, entId, editUsername):
        """this is called just before the new entity is created; if
        editUsername matches our username, this is an entity that we
        requested."""
        Level.Level.setEntityCreatorUsername(self, entId, editUsername)
        if editUsername == self.getEditUsername():
            print 'entity %s about to be created; we requested it' % entId
            callback = self.entCreateHandlerQ[0]
            del self.entCreateHandlerQ[:1]
            callback(entId)
            self.entitiesWeCreated.append(entId)

    def removeSelectedEntity(self):
        # request removal of selected entity
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity to be removed first.',
                'error')
            return -1
        if self.getEntity(selectedEntId).getNumChildren() > 0:
            self.editor.showWarning('Remove children first.')
            return -1
        self.doRemoveEntity(selectedEntId)

    def removeSelectedEntityTree(self):
        # request removal of selected entity and all of its children
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity to be removed first.',
                'error')
            return -1
        def removeEntity(entId):
            # recursively deletes children, then deletes entity
            entity = self.getEntity(entId)
            for child in entity.getChildren():
                removeEntity(child.entId)
            self.doRemoveEntity(entId)
        removeEntity(selectedEntId)

    def doRemoveEntity(self, entId):
        parentEntId = self.getEntity(entId)._parentEntity.entId

        entType = self.getEntityType(entId)
        if entType in self.entTypeReg.getPermanentTypeNames():
            self.editor.showWarning("Cannot remove entities of type '%s'" %
                                    entType)
            return

        # to undo removal, we first need to create the entity, then
        # set all of its attribs
        removeAction = (self.editMgrEntity.entId,
                        'removeEntity',
                        {'entId':entId})
        old2new = [removeAction,]

        oldAttribs = []
        spec = self.levelSpec.getEntitySpecCopy(entId)
        del spec['type']
        for attrib, value in spec.items():
            oldAttribs.append((attrib, value))
        def setNewEntityId(entId, self=self, removeAction=removeAction,
                           oldAttribs=oldAttribs):
            # user just undid the removal; change the redo action to
            # reflect the object's new entId
            removeAction[2]['entId'] = entId
            # now that we have the new entId, set all of the old entity's
            # attribs on the new entity
            for attrib, value in spec.items():
                self.privSendAttribEdit(entId, attrib, value)
            # TODO: update map of old entIds -> new entIds?
            # during string of redos/undos, if entities are being
            # re-created, other entities that are subsequently re-created
            # may reference a previously re-created entity by its old entId
        def setEntCreateHandler(self=self, handler=setNewEntityId):
            self.entCreateHandlerQ.append(handler)
        new2old = [setEntCreateHandler,
                   (self.editMgrEntity.entId,
                    'requestNewEntity',
                    {'entType': self.getEntityType(entId),
                     'parentEntId': parentEntId,
                     # add this so we can determine which new entities
                     # are the ones we requested
                     'username': self.editUsername,
                     })]

        self.setUndoableAttribEdit(old2new, new2old)

    def makeCopyOfEntName(self, name):
        prefix = 'copy of '
        suffix = ' (%s)'
        oldName = name
        if len(oldName) <= len(prefix):
            # old name is shorter or as long as prefix; add the prefix
            newName = prefix + oldName
        elif oldName[:len(prefix)] != prefix:
            # old name doesn't have the prefix
            newName = prefix + oldName
        else:
            # old name has the prefix
            # does the old name end in the suffix?
            hasSuffix = True
            copyNum = 2
            if oldName[-1] != ')':
                hasSuffix = False
            if hasSuffix and (oldName[-2] in string.digits):
                i = len(oldName)-2
                numString = ''
                while oldName[i] in string.digits:
                    numString = oldName[i] + numString
                    i -= 1
                if oldName[i] != '(':
                    hasSuffix = False
                else:
                    i -= 1
                    if oldName[i] != ' ':
                        hasSuffix = False
                    else:
                        print 'numString: %s' % numString
                        copyNum = int(numString)+1
            if hasSuffix:
                newName = oldName[:i] + suffix % copyNum
            else:
                newName = oldName + suffix % copyNum
        return newName

    def duplicateSelectedEntity(self):
        try:
            selectedEntId = self.selectedEntity.entId
            parentEntId = self.selectedEntity._parentEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity to be removed first.',
                'error')
            return

        if self.selectedEntity.getNumChildren() > 0:
            self.editor.showTodo('Cannot duplicate entity with children.')
            return

        # to undo, remove the entity
        removeAction = (self.editMgrEntity.entId,
                        'removeEntity',
                        {'entId':selectedEntId})
        new2old = [removeAction,]

        # to duplicate the entity, create a new entity and set (most of)
        # the same attribs
        # make sure we get a deep copy of the spec
        copyAttribs = self.levelSpec.getEntitySpecCopy(selectedEntId)
        copyAttribs['comment'] = ''
        copyAttribs['name'] = self.makeCopyOfEntName(copyAttribs['name'])
        # remove any constant attribs
        typeDesc = self.entTypeReg.getTypeDesc(copyAttribs['type'])
        attribDescs = typeDesc.getAttribDescDict()
        for attribName, attribDesc in attribDescs.items():
            if attribDesc.getDatatype() == 'const':
                del copyAttribs[attribName]
        def setNewEntityId(entId, self=self, removeAction=removeAction,
                           copyAttribs=copyAttribs):
            # user just undid the removal; change the redo action to
            # reflect the object's new entId
            removeAction[2]['entId'] = entId

            # set attribs
            for attribName, value in copyAttribs.items():
                self.privSendAttribEdit(entId, attribName, value)
            # TODO: update map of old entIds -> new entIds?
            # during string of redos/undos, if entities are being
            # re-created, other entities that are subsequently re-created
            # may reference a previously re-created entity by its old entId
        def setEntCreateHandler(self=self, handler=setNewEntityId):
            self.entCreateHandlerQ.append(handler)
        old2new = [setEntCreateHandler,
                   (self.editMgrEntity.entId,
                    'requestNewEntity',
                    {'entType': self.getEntityType(selectedEntId),
                     'parentEntId': parentEntId,
                     # add this so we can determine which new entities
                     # are the ones we requested
                     'username': self.editUsername,
                     })]

        self.setUndoableAttribEdit(old2new, new2old)

    def specPrePickle(self, spec):
        # prepares a spec for pickling
        # WARNING: modifies 'spec'
        for attribName, value in spec.items():
            spec[attribName] = repr(value)
        return spec

    def specPostUnpickle(self, spec):
        # fixes up a spec after being unpickled
        # WARNING: modifies 'spec'
        for attribName, value in spec.items():
            spec[attribName] = eval(value)
        return spec

    def handleImportEntities(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity first.',
                'error')
            return
        # for now, only import a single entity
        import tkFileDialog
        filename = tkFileDialog.askopenfilename(
            parent=self.editor.parent,
            defaultextension='.egroup',
            filetypes=[('Entity Group', '.egroup'),
                       ('All Files', '*'),
                       ],
            )
        if len(filename) == 0:
            return
        try:
            import pickle
            f = open(filename, 'r')
            eTree = pickle.load(f)
            eGroup = pickle.load(f)
            for entId, spec in eGroup.items():
                eGroup[entId] = self.specPostUnpickle(spec)
        except:
            self.editor.showWarning(
                'Error importing entity group from \'%s\'.' % filename,
                'error')
            return
            
        oldEntId2new = {}
        def addEntities(treeEntry, parentEntId, eGroup=eGroup):
            # recursively adds the entities described by the entId tree
            for entId, children in treeEntry.items():
                spec = eGroup[entId]
                entType = spec['type']
                del spec['type']
                del spec['parentEntId']
                # remove all other 'const' attributes
                typeDesc = self.entTypeReg.getTypeDesc(entType)
                for attribName, attribDesc in typeDesc.getAttribDescDict().items():
                    if attribDesc.getDatatype() == 'const':
                        if attribName in spec:
                            del spec[attribName]
                def handleEntityInsertComplete(newEntId, oldEntId=entId,
                                               oldEntId2new=oldEntId2new,
                                               spec=spec, treeEntry=treeEntry,
                                               addEntities=addEntities):
                    oldEntId2new[oldEntId] = newEntId
                    def assignAttribs(entId=newEntId, oldEntId=oldEntId,
                                      spec=spec, treeEntry=treeEntry):
                        for attribName in spec:
                            self.setAttribEdit(entId, attribName,
                                               spec[attribName])
                        # add our children
                        addEntities(treeEntry[oldEntId], newEntId)
                    # once the entity has been added, assign its attributes
                    self.acceptOnce(self.getEntityCreateEvent(newEntId),
                                    assignAttribs)
                self.insertEntity(entType,
                                  parentEntId=parentEntId,
                                  callback=handleEntityInsertComplete)
        # kick off the entity insertions
        addEntities(eTree, selectedEntId)

    def handleExportEntity(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity first.',
                'error')
            return
        import tkFileDialog
        filename = tkFileDialog.asksaveasfilename(
            parent=self.editor.parent,
            defaultextension='.egroup',
            filetypes=[('Entity Group', '.egroup'),
                       ('All Files', '*'),
                       ],
            )
        if len(filename) == 0:
            return
        # entity groups are just dictionaries of entId:spec, where
        # spec attrib values are repr'ed, along with a 'tree' of entIds
        eTree = {selectedEntId:{}}
        eGroup = {}
        eGroup[selectedEntId] = self.levelSpec.getEntitySpecCopy(selectedEntId)
        for entId, spec in eGroup.items():
            eGroup[entId] = self.specPrePickle(spec)
        try:
            import pickle
            f = open(filename, 'w')
            pickle.dump(eTree, f)
            pickle.dump(eGroup, f)
        except:
            self.editor.showWarning(
                'Error exporting entity group to \'%s\'.' % filename,
                'error')
            return

    def handleExportEntityTree(self):
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity first.',
                'error')
            return
        import tkFileDialog
        filename = tkFileDialog.asksaveasfilename(
            parent=self.editor.parent,
            defaultextension='.egroup',
            filetypes=[('Entity Group', '.egroup'),
                       ('All Files', '*'),
                       ],
            )
        if len(filename) == 0:
            return
        # entity groups are just dictionaries of entId:spec, where
        # spec attrib values are repr'ed, along with a 'tree' of entIds
        eTree = {}
        eGroup = {}
        def addEntity(entId, treeEntry):
            # recursively adds this entity and all its children to the
            # entity group structure
            treeEntry[entId] = {}
            eGroup[entId] = self.levelSpec.getEntitySpecCopy(entId)
            entity = self.getEntity(entId)
            for child in entity.getChildren():
                addEntity(child.entId, treeEntry[entId])
        addEntity(selectedEntId, eTree)
        for entId, spec in eGroup.items():
            eGroup[entId] = self.specPrePickle(spec)
        try:
            import pickle
            f = open(filename, 'w')
            pickle.dump(eTree, f)
            pickle.dump(eGroup, f)
        except:
            self.editor.showWarning(
                'Error exporting entity group to \'%s\'.' % filename,
                'error')
            return

    def moveAvToSelected(self):
        """move avatar to the selected entity"""
        try:
            selectedEntId = self.selectedEntity.entId
        except AttributeError:
            self.editor.showWarning(
                'Please select a valid entity first.',
                'error')
            return

        entNp = self.getEntInstanceNP(selectedEntId)
        # if we can't get a handle on the entity, go to the zone
        if entNp is None:
            zoneEntId = self.levelSpec.getEntityZoneEntId(selectedEntId)
            entNp = self.getEntInstanceNP(zoneEntId)

        base.localAvatar.setPos(entNp,0,0,0)
        base.localAvatar.setHpr(entNp,0,0,0)
        zoneNum = self.getEntityZoneEntId(selectedEntId)
        self.level.enterZone(zoneNum)

    def requestSpecSave(self):
        # if we're partially destroyed, our editMgrEntity may not be valid
        # also, don't add this to the undo stack
        self.privSendAttribEdit(LevelConstants.EditMgrEntId, 'requestSave',
                                None)
        self.specModified = 0

    def setAttribChange(self, entId, attrib, valueStr, username):
        """AI has informed us of an accepted value change"""
        if username == self.editUsername:
            print 'we got our own edit back!'
        value = eval(valueStr)
        self.levelSpec.setAttribChange(entId, attrib, value, username)

    # editor InGameEditorElement methods
    def getTypeName(self):
        return 'Level'
