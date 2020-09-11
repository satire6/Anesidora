
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from toontown.toonbase import ToontownGlobals

"""
blockModel = loader.loadModel("phase_4/models/minigames/block")

blockPaths = [
[0, (75,-45,0,2), (75,-35,0,2), (85,-35,0,2), (85,-45,0,2)],
[0, (71,-45,-0,2), (65,-45,0,2)],
]

for blockPath in blockPaths:
    block = MovingBlock.MovingBlock(blockPath[0], blockModel)
    block.reparentTo(render)
    iList = []
    for coord in blockPath[1:]:
        iList.append(LerpPosInterval(block, coord[3], pos=Point3(coord[0], coord[1], coord[2])))
    track = Track(iList)
    track.loop()

"""


class MovingBlock(DirectObject.DirectObject, NodePath):

    def __init__(self, index, model):
        self.token = ToontownGlobals.SPDynamic + index
        self.name = "MovingBlock-%d" % (index)
        NodePath.__init__(self, hidden.attachNewNode(self.name))
        self.model = model.copyTo(self)
        self.model.find("**/floor").setName(self.name)
        base.cr.parentMgr.registerParent(self.token, self)
        self.accept('on-floor', self.__handleOnFloor)
        self.accept('off-floor', self.__handleOffFloor)

    def delete(self):
        base.cr.parentMgr.unregisterParent(self.token)
        self.model.removeNode()
        del self.model
        self.ignore('on-floor')
        self.ignore('off-floor')

    def __handleOnFloor(self, collEntry):
        if (collEntry.getIntoNode().getName() == self.name):
            print ('on floor %s' % (self.name))
            base.localAvatar.b_setParent(self.token)

    def __handleOffFloor(self, collEntry):
        if (collEntry.getIntoNode().getName() == self.name):
            print ('off floor %s' % (self.name))
            base.localAvatar.b_setParent(ToontownGlobals.SPRender)

