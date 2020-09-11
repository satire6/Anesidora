from otp.level.EntityTypes import *

class CogdoLevelMgr(LevelMgr):
    type = 'levelMgr'

class CogdoCraneGameSettings(Entity):
    type = 'cogdoCraneGameSettings'
    attribs = (
        ('GameDuration', 180., 'float'),
        )
