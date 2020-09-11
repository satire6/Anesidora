"""
This is just a sample code.

LevelEditor, ObjectHandler, ObjectPalette should be rewritten
to be game specific.
"""

from direct.actor import Actor
from direct.leveleditor import ObjectGlobals as OG

class ObjectHandler:
    """ ObjectHandler will create and update objects """
    
    def __init__(self, editor):
        self.editor = editor

    def createDoubleSmiley(self, horizontal=True):
        root = render.attachNewNode('doubleSmiley')
        a = loader.loadModel('models/smiley.egg')
        b = loader.loadModel('models/smiley.egg')
        if horizontal:
            a.setName('left')
            b.setName('right')
            a.setPos(-1, 0, 0)
            b.setPos(1, 0, 0)
        else:
            a.setName('top')
            b.setName('bottom')
            a.setPos(0, 0, 1)
            b.setPos(0, 0, -1)

        a.reparentTo(root)
        b.reparentTo(root)
        return root
    
    def updateDoubleSmiley(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        if objNP.find('left'):
            objNP.find('left').setPos(-1 * val, 0, 0)
            objNP.find('right').setPos(val, 0, 0)
        else:
            objNP.find('top').setPos(0, 0, 1 * val)
            objNP.find('bottom').setPos(0, 0, -1 * val)

    def updateSmiley(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        if base.direct:
            base.direct.deselectAllCB()
        for child in objNP.findAllMatches("+GeomNode"):
            child.removeNode()

        for i in range(val):
            a = loader.loadModel(obj[OG.OBJ_MODEL])
            b = a.find("+GeomNode")
            b.setPos(0, i*2, 0)
            b.reparentTo(objNP)
            a.removeNode()

    def createPanda(self):
        pandaActor = PandaActor()
        return pandaActor

    def createGrass(self):
        environ = loader.loadModel("models/environment.egg")
        environ.setScale(0.25,0.25,0.25)
        #environ.setPos(-8,42,0)
        return environ

    def createToontownTree(self):
        root = loader.loadModel('phase_3.5/models/props/trees.bam')
        root.findAllMatches("**/prop_tree_fat/*/prop_tree_*").hide()
        root.findAllMatches("**/prop_tree_small/*/prop_tree_*").hide()
        root.findAllMatches("**/prop_tree_large/*/prop_tree_*").hide()        
        root.find("**/prop_tree_fat_no_box_ul").show()
        return root

    def updateToontownTree(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.findAllMatches("**/prop_tree_fat/*/prop_tree_*").hide()
        objNP.findAllMatches("**/prop_tree_small/*/prop_tree_*").hide()
        objNP.findAllMatches("**/prop_tree_large/*/prop_tree_*").hide()
        objNP.find("**/%s"%val).show()

    def createStreetlightTT(self):
        root = loader.loadModel('phase_3.5/models/props/streetlight_TT.bam')
        root.find("**/prop_post_three_light").hide()
        root.find("**/prop_post_sign").hide()
        return root

    def updateStreetlightTT(self, val, obj):
        objNP = obj[OG.OBJ_NP]
        objNP.find("**/prop_post_one_light").hide()
        objNP.find("**/prop_post_three_light").hide()
        objNP.find("**/prop_post_sign").hide()
        objNP.find("**/%s"%val).show()

    def createTortuga(self):
        root = loader.loadModel('models/islands/pir_m_are_isl_tortuga.bam')
        root.find("**/minimap").hide()
        return root
            
class PandaActor(Actor.Actor):
    def __init__(self):
        Actor.Actor.__init__(self, "models/panda-model.egg")
        self.setScale(0.005)


    
