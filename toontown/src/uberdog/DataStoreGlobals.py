from toontown.uberdog.ScavengerHuntDataStore import *
from toontown.uberdog.DataStore import *

SH = 1
GEN = 2

TYPES = {
    # id : { classType, }
    # Trick-or-treat scavenger hunt
    SH : ( ScavengerHuntDataStore, ),
    GEN : ( DataStore , ),
    }

def getStoreClass(type):
    storeClass = TYPES.get(type,None)
    if storeClass:
        return storeClass[0]
