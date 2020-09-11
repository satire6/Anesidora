from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from direct.task import Task

def acquirePetManager():
    if not hasattr(base, 'petManager'):
        PetManager()
    base.petManager.incRefCount()

def releasePetManager():
    base.petManager.decRefCount()

class PetManager:
    # A global non-distributed object that exists as long as at least one pet
    # is instantiated on the client.
    CollTaskName = 'petFloorCollisions'

    def __init__(self):
        base.petManager = self
        self.refCount = 0

        # Create a collision traverser that will be used to keep pets
        # on the ground.
        # Pets are moved by the AI in X and Y only, and lifters are
        # used to keep the pets on the surface of the ground.
        # If the pet lifters are placed in the global cTrav, they may or
        # may not act before another collider in cTrav, leading to
        # unpredictable behavior.
        self.cTrav = CollisionTraverser('petFloorCollisions')
        taskMgr.add(self._doCollisions, PetManager.CollTaskName,
                    priority=ToontownGlobals.PetFloorCollPriority)

    def _destroy(self):
        taskMgr.remove(PetManager.CollTaskName)
        del self.cTrav

    def _doCollisions(self, task):
        self.cTrav.traverse(render)
        return Task.cont

    def incRefCount(self):
        self.refCount += 1
    def decRefCount(self):
        self.refCount -= 1
        if self.refCount == 0:
            self._destroy()
            del base.petManager
