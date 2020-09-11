from toontown.hood import GenericAnimatedProp

class GenericAnimatedBuilding(GenericAnimatedProp.GenericAnimatedProp):
    def __init__(self, node):
        """Construct a landmark animated building."""
        # also see DistributedAnimatedBuilding.py
        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)

        
    def enter(self):
        """Don't animate if the buildings are not meant to animate yet."""
        if base.config.GetBool("buildings-animate", False):
            GenericAnimatedProp.GenericAnimatedProp.enter(self)
        else:
            # dont animate or do anything else
            pass
            
