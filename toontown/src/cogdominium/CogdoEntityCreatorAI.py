from direct.showbase.PythonUtil import Functor
from otp.level import EntityCreatorAI
from toontown.cogdominium.CogdoLevelMgrAI import CogdoLevelMgrAI
from toontown.cogdominium import CogdoCraneGameConsts

class CogdoEntityCreatorAI(EntityCreatorAI.EntityCreatorAI):
    def __init__(self, level):
        EntityCreatorAI.EntityCreatorAI.__init__(self, level)

        # create short aliases for EntityCreatorAI create funcs
        cDE = EntityCreatorAI.createDistributedEntity
        cLE = EntityCreatorAI.createLocalEntity
        nothing = EntityCreatorAI.nothing

        self.privRegisterTypes({
            'levelMgr': Functor(cLE, CogdoLevelMgrAI),
            'cogdoCraneGameSettings': Functor(cLE, self._createCogdoSettings),
            })

    def _createCogdoSettings(self, level, entId):
        CogdoCraneGameConsts.Settings.initializeEntity(level, entId)
        return CogdoCraneGameConsts.Settings
