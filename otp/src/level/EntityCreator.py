"""EntityCreator module: contains the EntityCreator class"""

import CutScene
import EntityCreatorBase
import BasicEntities
from direct.directnotify import DirectNotifyGlobal
import EditMgr
import EntrancePoint
import LevelMgr
import LogicGate
import ZoneEntity
import ModelEntity
import PathEntity
import VisibilityExtender
import PropSpinner
import AmbientSound
import LocatorEntity
import CollisionSolidEntity

# some useful constructor functions
# ctor functions must take (level, entId)
# and they must return the entity that was created, or 'nothing'
def nothing(*args):
    """For entities that don't exist on the client at all"""
    return 'nothing'

def nonlocal(*args):
    """For entities that don't need to be created by the client and will
    show up independently (they're distributed and created by the AI)"""
    return 'nonlocal'

class EntityCreator(EntityCreatorBase.EntityCreatorBase):
    """
    This class is responsible for creating instances of Entities on the
    client. It can be subclassed to handle more Entity types.
    """
    
    def __init__(self, level):
        EntityCreatorBase.EntityCreatorBase.__init__(self, level)
        self.level = level
        self.privRegisterTypes({
            'attribModifier': nothing,
            'ambientSound': AmbientSound.AmbientSound,
            'collisionSolid': CollisionSolidEntity.CollisionSolidEntity,
            'cutScene': CutScene.CutScene,
            'editMgr': EditMgr.EditMgr,
            'entityGroup': nothing,
            'entrancePoint': EntrancePoint.EntrancePoint,
            'levelMgr': LevelMgr.LevelMgr,
            'locator': LocatorEntity.LocatorEntity,
            'logicGate': LogicGate.LogicGate,
            'model': ModelEntity.ModelEntity,
            'nodepath': BasicEntities.NodePathEntity,
            'path': PathEntity.PathEntity,
            'propSpinner': PropSpinner.PropSpinner,
            'visibilityExtender': VisibilityExtender.VisibilityExtender,
            'zone': ZoneEntity.ZoneEntity,
            })

    def doCreateEntity(self, ctor, entId):
        return ctor(self.level, entId)
