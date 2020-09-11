
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal

class AnimatedProp(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("AnimatedProp")
    
    def __init__(self, node):
        self.node = node

    def delete(self):
        pass

    def uniqueName(self, name):
        return (name + "-" + str(self.node.this))

    def enter(self):
        # Note: this must be safe and efficient to be called multiple times
        self.notify.debug("enter")

    def exit(self):
        # Note: this must be safe and efficient to be called multiple times
        self.notify.debug("exit")
    
    
