"""
Street object
"""

from ToonTownObj import *

class StreetObj(ToonTownObj):
    def __init__(self, editor, streetType, dna=None, nodePath=None):
        self.hoodId = streetType[:2]
        self.editor = editor
        if not streetType.endswith('_pond'):
            self.streetType = 'street_' + streetType[3:]
        else:
            self.streetType = 'street_' + streetType
        self.editor.setEditMode(self.hoodId)
        ToonTownObj.__init__(self, editor, dna, nodePath)

    def initDNA(self):
        dnaNode = DNAStreet(self.streetType + '_DNARoot')
        dnaNode.setCode(self.streetType)
        dnaNode.setPos(VBase3(0))
        dnaNode.setHpr(VBase3(0))
        

        # Set street texture to neighborhood dependant texture
        dnaNode.setStreetTexture(
            'street_street_' + self.hoodId + '_tex')
        dnaNode.setSidewalkTexture(
            'street_sidewalk_' + self.hoodId + '_tex')
        dnaNode.setCurbTexture(
            'street_curb_' + self.hoodId + '_tex')
        return dnaNode
