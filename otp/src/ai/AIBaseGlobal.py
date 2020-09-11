"""instantiate global ShowBase object"""


from AIBase import *

# guard against AI files being imported on the client
assert game.process != 'client'

__builtins__["simbase"] = AIBase()

# Make some global aliases for convenience
__builtins__["ostream"] = Notify.out()
__builtins__["run"] = simbase.run
__builtins__["taskMgr"] = simbase.taskMgr
__builtins__["jobMgr"] = simbase.jobMgr
__builtins__["eventMgr"] = simbase.eventMgr
__builtins__["messenger"] = simbase.messenger
__builtins__["bboard"] = simbase.bboard
__builtins__["config"] = simbase.config
__builtins__["directNotify"] = directNotify

# we don't use ToontownLoader because it just adds progress bar
# functionality to Loader
from direct.showbase import Loader

simbase.loader = Loader.Loader(simbase)
__builtins__["loader"] = simbase.loader

# Set direct notify categories now that we have config
directNotify.setDconfigLevels()

def inspect(anObject):
    from direct.tkpanels import Inspector
    Inspector.inspect(anObject)

__builtins__["inspect"] = inspect
# this also appears in ShowBaseGlobal
if (not __debug__) and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")


# Now the builtins are filled in.
taskMgr.finalInit()
