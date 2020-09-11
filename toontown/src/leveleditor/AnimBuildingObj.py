"""
AnimBuilding object
"""

from AnimPropObj import *

class AnimBuildingObj(AnimPropObj):
    def __init__(self, editor, animBuildingType, dna=None, nodePath=None):
        self.animBuildingType = animBuildingType
        AnimPropObj.__init__(self, editor, animBuildingType, dna, nodePath)

    def initDNA(self):
        # And create new anim building
        block = self.getNextLandmarkBlock()
        dnaNode = DNAAnimBuilding(
            'tb'+block+':'+self.animBuildingType + '_DNARoot')
        dnaNode.setCode(self.animBuildingType)
        dnaNode.setPos(VBase3(0))
        dnaNode.setHpr(VBase3(0))
        dnaNode.setBuildingType('animbldg')
        return dnaNode
