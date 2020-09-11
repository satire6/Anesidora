"""SCObject.py: contains the SCObject class"""

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

class SCObject(DirectObject):
    """ SCObject is the base class for all entities that make up a
    SpeedChat tree. """

    notify = DirectNotifyGlobal.directNotify.newCategory('SpeedChat')
    
    def __init__(self):
        self.settingsRef = None
        self.__visible = 0
        self.__dirty = 1

    def destroy(self):
        self.ignoreAll()
        if self.isVisible():
            self.exitVisible()

    """ The owner of this SCObject should call enter/exitVisible when
    this object appears on screen and no longer appears on the screen,
    respectively. Derived classes can override these functions and
    perform the appropriate actions """
    def enterVisible(self):
        #print 'enterVisible: %s' % self
        self.__visible = 1
    def exitVisible(self):
        #print 'exitVisible: %s' % self
        self.__visible = 0
    def isVisible(self):
        return self.__visible

    # call 'invalidate' to indicate that the appearance of this object
    # has changed, such that it needs to rebuild itself before being shown
    def invalidate(self):
        self.__dirty = 1
    def isDirty(self):
        return self.__dirty
    def validate(self):
        self.__dirty = 0

    def finalize(self):
        """ subclasses should override this function and perform whatever
        processing is necessary to 'finalize' the appearance of this
        object so that it's ready to be displayed """
        pass

    def getEventName(self, name):
        """ the names of all events that pertain to a specific SpeedChat
        object should come from this function """
        return '%s%s' % (self.settingsRef.eventPrefix, name)

    def getColorScheme(self):
        return self.settingsRef.colorScheme

    def isWhispering(self):
        return self.settingsRef.whisperMode

    def getSubmenuOverlap(self):
        return self.settingsRef.submenuOverlap

    def getTopLevelOverlap(self):
        if self.settingsRef.topLevelOverlap is None:
            return self.getSubmenuOverlap()
        else:
            return self.settingsRef.topLevelOverlap

    def privSetSettingsRef(self, settingsRef):
        """ Subclasses that contain nested SCObjects are responsible for
        overriding this function, calling it for all of their children,
        and calling this function. This propogates the reference through
        the entire tree. """
        self.settingsRef = settingsRef

    def privAdoptSCObject(self, scObj):
        """ Subclasses that contain nested SCObjects must call this
        function whenever they gain a new child, with a reference to
        the new child. """
        scObj.privSetSettingsRef(self.settingsRef)

    def invalidateAll(self):
        """ inheritors should call down to this function, and also call
        invalidateAll for all of their child objects """
        self.invalidate()

    def finalizeAll(self):
        """ inheritors should call down to this function, and also call
        finalizeAll for all of their child objects """
        self.finalize()
