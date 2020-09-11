"""DelayDelete module: contains the DelayDelete class"""

# Deprecated. Please do not use outside of $TOONTOWN

# DelayDelete is being phased out and should not be used in any tree
# outside of $TOONTOWN. Usage of DelayDelete leads to client bugs that
# - are easily introduced when unrelated DistributedObject code is changed
# - don't typically show up during development of unrelated changes
# - are difficult to identify as DelayDelete-related
# - are difficult to repro

# DelayDelete-related client bugs typically involve an object that has
# been DelayDeleted but hasn't cleaned up a task or messenger hook,
# and has 'trash' data members that are considered to be destroyed but
# are still accessible. DelayDelete-related bugs can occur when a
# DelayDeleted copy of an object is still active on the client, and
# the same object zones in and is re-generated alongside the
# DelayDeleted copy. If they overlap in usage of some resource,
# problems are likely to occur.

# Please use alternative methods of referencing an object's data
# after it is has been deleted, for instance:
# - abandon the operation when the DistributedObject is deleted
# - store a copy of the data, independent of the DistributedObject,
#   that is unaffected by its deletion

class DelayDelete:
    """
    The DelayDelete class is a special class whose sole purpose is
    management of the DistributedObject.delayDelete() counter.

    Normally, a DistributedObject has a delayDelete count of 0.  When
    we need to bracket a region of code that cannot tolerate a
    DistributedObject being deleted, we call do.delayDelete(1) to
    increment the delayDelete count by 1.  While the count is nonzero,
    the object will not be deleted.  Outside of our critical code, we
    call do.delayDelete(0) to decrement the delayDelete count and
    allow the object to be deleted once again.

    Explicit management of this counter is tedious and risky.  This
    class implicitly manages the counter by incrementing the count in
    the constructor, and decrementing it in the destructor.  This
    guarantees that every increment is matched up by a corresponding
    decrement.

    Thus, to temporarily protect a DistributedObject from deletion,
    simply create a DelayDelete object.  While the DelayDelete object
    exists, the DistributedObject will not be deleted; when the
    DelayDelete object ceases to exist, it may be deleted.
    """

    def __init__(self, distObj, name):
        self._distObj = distObj
        self._name = name
        self._token = self._distObj.acquireDelayDelete(name)

    def getObject(self):
        return self._distObj

    def getName(self):
        return self._name

    def destroy(self):
        token = self._token
        # do this first to catch cases where releaseDelayDelete causes
        # this method to be called again
        del self._token
        self._distObj.releaseDelayDelete(token)
        del self._distObj
        del self._name

# There is code in Toontown that puts interval-related DelayDeletes
# directly on interval objects, relying on Python to __del__ the
# DelayDelete when the interval is garbage-collected. DelayDelete now
# requires .destroy() to be called.
# To reduce code duplication, this method may be called to clean up
# delayDeletes that have been placed on an interval.
def cleanupDelayDeletes(interval):
    if hasattr(interval, 'delayDelete'):
        delayDelete = interval.delayDelete
        # get rid of all references before calling destroy in case destroy causes
        # this function to be called again
        del interval.delayDelete
        if type(delayDelete) == type([]):
            for i in delayDelete:
                i.destroy()
        else:
            delayDelete.destroy()
    if hasattr(interval, 'delayDeletes'):
        delayDeletes = interval.delayDeletes
        # get rid of the reference before calling destroy in case destroy causes
        # this function to be called again
        del interval.delayDeletes
        if type(delayDeletes) == type([]):
            for i in delayDeletes:
                i.destroy()
        else:
            delayDeletes.destroy()
