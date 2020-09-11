from direct.fsm.StatePush import StateVar
from otp.level.EntityStateVarSet import EntityStateVarSet
from toontown.cogdominium.CogdoEntityTypes import CogdoCraneGameSettings

# constants that can be modified by the IGE (~edit)
Settings = EntityStateVarSet(CogdoCraneGameSettings)

CranePosHprs = [
    (13.4, -136.6, 6, -45, 0, 0),
    (13.4, -91.4, 6, -135, 0, 0),
    (58.6, -91.4, 6, 135, 0, 0),
    (58.6, -136.6, 6, 45, 0, 0),
    ]
