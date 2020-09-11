"""
Landmark object
"""

from ToonTownObj import *

class LandmarkObj(ToonTownObj):
    def __init__(self, editor, landmarkType, dna=None, nodePath=None):
        self.landmarkType = landmarkType
        ToonTownObj.__init__(self, editor, dna, nodePath)

    def initDNA(self):
        block=self.getNextLandmarkBlock()
        dnaNode = DNALandmarkBuilding(
            'tb'+block+':'+self.landmarkType + '_DNARoot')
        dnaNode.setCode(self.landmarkType)
        dnaNode.setPos(VBase3(0))
        dnaNode.setHpr(VBase3(0))

        if 'hq' in self.landmarkType:
            dnaNode.setBuildingType('hq')
        elif 'kart_shop' in self.landmarkType:
            dnaNode.setBuildingType('kartshop')
        else:
            # add random doors by default
            doorDNA = self.createDoor('landmark_door')
            dnaNode.add(doorDNA)

        return dnaNode
