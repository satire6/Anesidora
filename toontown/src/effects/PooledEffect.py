from pandac.PandaModules import *
from direct.showbase import Pool
from direct.showbase.DirectObject import DirectObject
import re

class PooledEffect(DirectObject, NodePath):

    pool = None
    poolLimit = 124

    @classmethod
    def getEffect(cls, context=''):
##        if __dev__:
##            if base.cr.hasToggledEffects():
##                # if there are any specific effects toggled on/off
##                # extract module name and see if we should show this effect type
##                match = re.split('\.',cls.__module__)
##                moduleName = match[len(match)-1]
##                if (not base.cr.queryShowEffect(moduleName+context)):
##                    return None
##            elif not base.cr.wantSpecialEffects:
##                # global effects config is off
##                return None

        # If we already have a free one, return it
        if cls.pool is None:
            # Create a pool on the derived class object
            cls.pool = Pool.Pool()
        if cls.pool.hasFree():
            return cls.pool.checkout()
        else:
            # Otherwise if we are not at our limit, make a new
            # one and return that one.
            free, used = cls.pool.getNumItems()
            if free + used < cls.poolLimit:
                # Since cls is the derived effect class, just call
                # it to create a new effect object.
                cls.pool.add(cls())
                return cls.pool.checkout()
            else:
                # If we are at our limit return None
                # Make sure your calling code can handle that!
                return None

    @classmethod
    def cleanup(cls):
        if cls.pool:
            cls.pool.cleanup(cls.destroy)
            cls.pool = None

    def __init__(self):
        # Initialize the superclass
        NodePath.__init__(self, self.__class__.__name__)
        
        # When the game shuts down, any effects that may be active
        # should accept this event so their pool gets cleaned up
        self.accept("clientLogout", self.__class__.cleanup)

    def destroy(self,item = None):
        if item:
            self.pool.remove(item)
        self.ignore("clientLogout")
        self.removeNode()
