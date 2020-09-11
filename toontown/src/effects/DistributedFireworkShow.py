from direct.distributed import DistributedObject
from toontown.effects.FireworkShowMixin import FireworkShowMixin

class DistributedFireworkShow(DistributedObject.DistributedObject, FireworkShowMixin):

    notify = directNotify.newCategory("DistributedFireworkShow")

    def __init__(self, cr):
        assert(self.notify.debug("__init__"))
        DistributedObject.DistributedObject.__init__(self, cr)
        FireworkShowMixin.__init__(self)

    def generate(self):
        assert(self.notify.debug("generate"))
        DistributedObject.DistributedObject.generate(self)

    def disable(self):
        assert(self.notify.debug("disable"))
        DistributedObject.DistributedObject.disable(self)
        # self.ignore("+")
        FireworkShowMixin.disable(self)

    def delete(self):
        assert(self.notify.debug("delete"))
        DistributedObject.DistributedObject.delete(self)

    def d_requestFirework(self, x, y, z, style, color1, color2):
        assert(self.notify.debug("requestFirework: style: %s" % style))
        self.sendUpdate("requestFirework", (x, y, z, style, color1, color2))

    

    
    
        
        
