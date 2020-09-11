from CatalogFurnitureItem import *

# The first 6 CatalogFurnitureItem properties are defined in CatalogFurnitureItem.py
# They are:
# FTModelName = 0
# FTColor = 1
# FTColorOptions = 2
# FTBasePrice = 3
# FTFlags = 4
# FTScale = 5
FTAnimRate = 6

# IMPORTANT this list must be updated if any new animated furniture item gets added
AnimatedFurnitureItemKeys = (
    10020, # winter tree
    270,  # Trolley Bed
    990,  # Gag Fan
    460,  # Coral Fireplace with fire
    470,  # Square Fireplace with fire
    480,  # Round Fireplace with fire
    490,  # Girly Fireplace with fire
    491,  # Bug Room Fireplace with fire
    492,  # Caramel Apple Fireplace with fire
    )

class CatalogAnimatedFurnitureItem(CatalogFurnitureItem):
    """
    This class represents a furniture item that has some kind or animation on it.
    The animation could be in the form of a sequence node, in which case, will be
    handled by this class, or it could be an animating actor, in which case, will
    be handled by CatalogAnimatedFurnitureActor.
    CatalogAnimatedFurnitureActor should derive from CatalogAnimatedFurnitureItem.
    
    This class supports functions to start, stop or change play rate of the animation.
    """

    def loadModel(self):    
        model = CatalogFurnitureItem.loadModel(self)
        self.setAnimRate(model, self.getAnimRate())
        return model
    
    def getAnimRate(self):
        """
        Returns the animation rate of a CatalogAnimatedFurnitureItem
        from its definition found in the FurnitureTypes dict.
        If there is no such it defaults to 1.0.
        Only CatalogAnimatedFurnitureItem (or its derivatives) should use AnimationRate.
        """
        item = FurnitureTypes[self.furnitureType]
        if (FTAnimRate < len(item)):
            animRate = item[FTAnimRate]
            if not (animRate == None):
                return item[FTAnimRate]
            else:
                return 1
        else:
            return 1
        
    def setAnimRate(self, model, rate):
        """
        This function should set the play rate of the animation.
        We are assuming that a CatalogAnimatedFurnitureItem is animated using sequence nodes,
        in which it will loop it's animation as soon as it is loaded. We have to only find
        the sequence nodes and setPlayRate on them.
        We are not handling actors here. For actor based animations make another
        class called CatalogAnimatedFurnitureActor.
        """
        # Find all the sequence nodes in the model.
        seqNodes = model.findAllMatches('**/seqNode*')
        for seqNode in seqNodes:
            seqNode.node().setPlayRate(rate)
