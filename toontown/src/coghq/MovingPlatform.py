"""MovingPlatform module: contains the MovingPlatform class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import types

# TODO: every MovingPlatform listens to every on-floor/off-floor event and
# compares the floor's name to its name. It would be more efficient to have
# a global MovingPlatformMgr that MovingPlatforms would register with. The
# mgr would listen for on-floor and off-floor events, match the floor node
# up with one of the registered platforms, and pass the event on to that
# one platform.

# TODO: it should be possible to become unparented from the platform without
# walking off of it, i.e. when jumping. If the jump code generates an
# 'off-floor' event upon jumping and an 'on-floor' event upon landing, that
# should take care of it.

class MovingPlatform(DirectObject.DirectObject, NodePath):

    notify = DirectNotifyGlobal.directNotify.newCategory('MovingPlatform')
    
    def __init__(self):
        self.hasLt = 0
        DirectObject.DirectObject.__init__(self)
        NodePath.__init__(self)
    
    def setupCopyModel(self, parentToken, model, floorNodeName=None,
                       parentingNode=None):
        """parentingNode is the node that avatars will be parented to when
        they are on this MovingPlatform; defaults to self"""
        assert(self.debugPrint("setupCopyModel(token=%s, model=%s, floorNodeName=%s)"%(
            parentToken, model, floorNodeName)))
        if floorNodeName is None:
            floorNodeName = 'floor'
        if type(parentToken) == types.IntType:
            parentToken = ToontownGlobals.SPDynamic + parentToken
        self.parentToken = parentToken
        self.name = "MovingPlatform-%s" % (parentToken)
        self.assign(hidden.attachNewNode(self.name))
        self.model = model.copyTo(self)
        self.ownsModel = 1
        floorList = self.model.findAllMatches("**/%s" % floorNodeName)
        if len(floorList) == 0:
            MovingPlatform.notify.warning('no floors in model')
            return
        for floor in floorList:
            floor.setName(self.name)
        if parentingNode == None:
            parentingNode = self
        base.cr.parentMgr.registerParent(self.parentToken, parentingNode)
        self.parentingNode = parentingNode
        self.accept('enter%s' % self.name, self.__handleEnter)
        self.accept('exit%s' % self.name, self.__handleExit)

    """ this doesn't appear to be used
    def setupEntity(self, entityId, parent, floorNodeName=None):
        assert(self.debugPrint("setupEntity(entityId=%s, parent=%s, floorNodeName=%s)"%(
                entityId, parent, floorNodeName)))
        self.parentToken = ToontownGlobals.SPDynamic + entityId
        self.assign(parent)
        self.ownsModel = 0
        self.name = floorNodeName
        base.cr.parentMgr.registerParent(self.parentToken, parent)
        self.parentingNode = parent
        self.accept('enter%s' % self.name, self.__handleEnter)
        self.accept('exit%s' % self.name, self.__handleExit)
        """

    def destroy(self):
        base.cr.parentMgr.unregisterParent(self.parentToken)
        self.ignoreAll()
        if self.hasLt:
            self.__releaseLt()
        if self.ownsModel:
            self.model.removeNode()
            del self.model
        # Only cleanup the parentingNode if it is set to yourself
        # If some external party set it up, they are responsible for
        # cleaning up the parentingNode. (for instance ConveyorBelt)
        if (hasattr(self, "parentingNode") and
            (self.parentingNode is self)):
            del self.parentingNode
        
    def getEnterEvent(self):
        return '%s-enter' % self.name
    def getExitEvent(self):
        return '%s-exit' % self.name

    def releaseLocalToon(self):
        """ if localToon is parented to us, parents localToon to render """
        if self.hasLt:
            self.__releaseLt()

    def __handleEnter(self, collEntry):
        self.notify.debug('on movingPlatform %s' % (self.name))
        self.__grabLt()
        messenger.send(self.getEnterEvent())
    def __handleExit(self, collEntry):
        self.notify.debug('off movingPlatform %s' % (self.name))
        self.__releaseLt()
        messenger.send(self.getExitEvent())

    def __handleOnFloor(self, collEntry):
        if (collEntry.getIntoNode().getName() == self.name):
            self.__handleEnter(collEntry)
    def __handleOffFloor(self, collEntry):
        if (collEntry.getIntoNode().getName() == self.name):
            self.__handleExit(collEntry)
            
    def __grabLt(self):
        base.localAvatar.b_setParent(self.parentToken)
        self.hasLt = 1
    def __releaseLt(self):
        if base.localAvatar.getParent().compareTo(self.parentingNode) == 0:
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)
            base.localAvatar.controlManager.currentControls.doDeltaPos()
        self.hasLt = 0
    
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('name', '?'))+' '+message)

"""
platformModel = loader.loadModel("phase_4/models/minigames/block")

# x,y,z,time (position is relative to localToon, +Y is forward, +X is left)
platformPaths = [
    [0, (0,10,1,2), (0,20,6,2), (10,20,6,2), (10,10,6,2), (10,10,1,2)],
]

for platformPath in platformPaths:
    token = platformPath[0]
    coords = platformPath[1:]
    platform = MovingPlatform.MovingPlatform(token, platformModel)
    platform.reparentTo(base.localAvatar)
    platform.setPos(coords[0][0],coords[0][1],coords[0][2])
    platform.wrtReparentTo(render)
    iList = []
    node = base.localAvatar.attachNewNode('platformPlacer')
    # we're already at first pos, start with 2nd and end with first
    for coord in coords[1:]+[coords[0]]:
        node.setPos(coord[0], coord[1], coord[2])
        iList.append(LerpPosInterval(platform, coord[3], bakeInStart=0,
                                     pos=node.getPos(render)))
    node.removeNode()
    del node
    track = Track(iList)
    track.loop()

"""
