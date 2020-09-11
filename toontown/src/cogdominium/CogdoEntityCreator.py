from otp.level import EntityCreator
from toontown.cogdominium import CogdoCraneGameConsts
from toontown.cogdominium.CogdoLevelMgr import CogdoLevelMgr
from toontown.cogdominium import CogdoCraneGameConsts

class CogdoEntityCreator(EntityCreator.EntityCreator):
    def __init__(self, level):
        EntityCreator.EntityCreator.__init__(self, level)

        # create short aliases for EntityCreator create funcs
        nothing = EntityCreator.nothing
        nonlocal = EntityCreator.nonlocal

        self.privRegisterTypes({
            'levelMgr': CogdoLevelMgr,
            'cogdoCraneGameSettings': self._createCogdoSettings,
            })

    def _createCogdoSettings(self, level, entId):
        CogdoCraneGameConsts.Settings.initializeEntity(level, entId)
        return CogdoCraneGameConsts.Settings
    
