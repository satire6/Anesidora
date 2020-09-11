"""
AnimProp object
"""

import glob, os
from ToonTownObj import *
from LevelEditorGlobals import importModule

class AnimPropObj(ToonTownObj):
    def __init__(self, editor, animPropType, dna=None, nodePath=None):
        self.animPropType = animPropType
        ToonTownObj.__init__(self, editor, dna, nodePath)
        self.createAnimatedProp()

    def initDNA(self):
        dnaNode = DNAAnimProp(self.animPropType + '_DNARoot')
        dnaNode.setCode(self.animPropType)
        dnaNode.setPos(VBase3(0))
        dnaNode.setHpr(VBase3(0))
        return dnaNode

    def createAnimatedProp(self):
        objDef = self.editor.objectPalette.findItem(self.animPropType)
        if objDef is None or\
           not objDef.properties.has_key('anims'):
            return
        animNameList = objDef.properties['anims'][4]
        
        dnaNode = self.dna
        code = dnaNode.getCode()

        if dnaNode.getAnim() == '':
            dnaNode.setAnim(animNameList[0])

        self.setTag('DNAAnim', dnaNode.getAnim())
        className = 'GenericAnimatedProp'
        if code.startswith('animated_prop_') and \
           not code.startswith('animated_prop_generic_'):
            splits = code.split('_')
            className = splits[2]

        # do some special python magic to get a handle to class
        # from the name of the class
        symbols = {}
        importModule(symbols, 'toontown.hood', [className])
        classObj = getattr(symbols[className], className)
        self.animPropObj = classObj(self)
        self.animPropObj.enter()

##         # [gjeon] connect interactive prop and battle cell
##         if DNAClassEqual(dnaNode, DNA_INTERACTIVE_PROP):
##             cellId = dnaNode.getCellId()
##             if cellId != -1:
##                 visGroup = self.getVisGroup(newNodePath)
##                 if visGroup is None:
##                     return
##                 for battleCellMarkerNP in visGroup.findAllMatches("**/battleCellMarker"):
##                     if battleCellMarkerNP.getTag('cellId') == '%d'%cellId:
##                         battleCellNP = battleCellMarkerNP.find('Sphere')
##                         self.drawLinkLine(battleCellNP, newNodePath)
##                         return
