from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.level.DistributedLevel import DistributedLevel
from otp.level import LevelConstants
from otp.level import EditorGlobals
from toontown.cogdominium.DistCogdoGame import DistCogdoGame
from toontown.cogdominium.CogdoEntityCreator import CogdoEntityCreator

class DistCogdoLevelGame(DistributedLevel, DistCogdoGame):
    notify = directNotify.newCategory("DistCogdoLevelGame")

    def __init__(self, cr):
        DistributedLevel.__init__(self, cr)
        DistCogdoGame.__init__(self, cr)

    def createEntityCreator(self):
        return CogdoEntityCreator(level=self)

    def generate(self):
        DistributedLevel.generate(self)
        DistCogdoGame.generate(self)
        if __dev__:
            bboard.post(EditorGlobals.EditTargetPostName, self)

    def announceGenerate(self):
        DistributedLevel.announceGenerate(self)
        DistCogdoGame.announceGenerate(self)
        self.startHandleEdits()
        
    def levelAnnounceGenerate(self):
        self.notify.debug('levelAnnounceGenerate')
        DistributedLevel.levelAnnounceGenerate(self)

        # create our spec
        # NOTE: in dev, the AI will probably send us another spec to use
        spec = self.getLevelSpec()
        if __dev__:
            # give the spec an EntityTypeRegistry.
            typeReg = self.getEntityTypeReg()
            spec.setEntityTypeReg(typeReg)
        
        DistributedLevel.initializeLevel(self, spec)

        # if the AI is sending us a spec, we won't have it yet and the
        # level isn't really initialized yet. So we can't assume that we
        # can start doing stuff here. Much of what used to be here
        # has been moved to FactoryLevelMgr, where it really belongs, but...
        # this could be cleaner.

    def privGotSpec(self, levelSpec):
        # OK, we've got the spec that we're going to use, either the one
        # we provided or the one from the AI. When we call down, the level
        # is going to be initialized, and all the local entities will be
        # created.
        if __dev__:
            # First, give the spec a factory EntityTypeRegistry if it doesn't
            # have one.
            if not levelSpec.hasEntityTypeReg():
                typeReg = self.getEntityTypeReg()
                levelSpec.setEntityTypeReg(typeReg)

        DistributedLevel.privGotSpec(self, levelSpec)

    def initVisibility(self):
        # prevent crash in initVisibility
        levelMgr = self.getEntity(LevelConstants.LevelMgrEntId)
        levelMgr.geom.reparentTo(render)
        DistributedLevel.initVisibility(self)

    def placeLocalToon(self):
        # don't let the level move the local toon at init
        DistributedLevel.placeLocalToon(self, moveLocalAvatar=False)

    def disable(self):
        self.stopHandleEdits()
        DistCogdoGame.disable(self)
        DistributedLevel.disable(self)

    def delete(self):
        DistCogdoGame.delete(self)
        DistributedLevel.delete(self)
        if __dev__:
            bboard.removeIfEqual(EditorGlobals.EditTargetPostName, self)
