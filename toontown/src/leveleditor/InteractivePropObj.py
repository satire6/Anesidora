"""
InteractiveProp object
"""

from AnimPropObj import *

class InteractivePropObj(AnimPropObj):
    def __init__(self, editor, interactivePropType, dna=None, nodePath=None):
        self.interactivePropType = interactivePropType
        AnimPropObj.__init__(self, editor, interactivePropType, dna, nodePath)

    def initDNA(self):
        dnaNode = DNAInteractiveProp(self.interactivePropType + '_DNARoot')
        dnaNode.setCode(self.interactivePropType)
        dnaNode.setPos(VBase3(0))
        dnaNode.setHpr(VBase3(0))
        return dnaNode
