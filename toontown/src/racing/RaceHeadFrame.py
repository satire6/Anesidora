from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toon import ToonHead

class RaceHeadFrame(DirectFrame):
    def __init__(self, av = None, color = Vec4(1,1,1,1), *args, **kwargs):
        self.panelGeom = loader.loadModel('phase_4/models/karting/racing_panel')         
        self.panelGeom.find('**/*fg').setColor(color)


        opts = {'relief':None,
                'geom':self.panelGeom,
                'geom_scale':(1,1,0.5),
                'pos':(0,0,0),
                }
        opts.update(kwargs)
        apply(DirectFrame.__init__,(self,)+args,opts)
        self.initialiseoptions(RaceHeadFrame)

        if (av):
            self.setAv(av)

    def setAv(self,av):
        self.head = self.stateNodePath[0].attachNewNode('head', 20)
        self.head.setPosHprScale(0, -0.5, -0.09,
                                 180.0, 0.0, 0.0,
                                 0.2, 0.2, 0.2)
        
        self.headModel = ToonHead.ToonHead()
        self.headModel.setupHead(av.style, forGui = 1)
        self.headModel.reparentTo(self.head)

##         # now enable a chat balloon
##         self.tag1Node = NametagFloat2d()
##         self.tag1Node.setContents(Nametag.CSpeech | Nametag.CThought)
##         self.av.nametag.addNametag(self.tag1Node)

##         self.tag1 = self.attachNewNode(self.tag1Node.upcastToPandaNode())
##         self.tag1.setPosHprScale(-0.16,0,-0.09,
##                                  0,0,0,
##                                  0.055,0.055,0.055)
##         self.tag1.hide()
        
##         # As well as a nametag just to display the name.
##         self.tag2Node = NametagFloat2d()
##         self.tag2Node.setContents(Nametag.CName)
##         self.av.nametag.addNametag(self.tag2Node)

##         self.tag2 = self.attachNewNode(self.tag2Node.upcastToPandaNode())
##         self.tag2.setPosHprScale(-0.27, 10.0, 0.16,
##                                  0,0,0,
##                                  0.05,0.05,0.05)
##         self.tag2.hide()
        
    def destroy(self):
##         print '\ndestroying head frame for %s.\n' %(`self.av`,)
##         if( self.av ):
##             self.headModel.delete()
##             del self.headModel
##             self.head.removeNode()
##             del self.head
##             self.av.nametag.removeNametag(self.tag1Node)
##             self.av.nametag.removeNametag(self.tag2Node)
##             self.tag1.removeNode()
##             self.tag2.removeNode()
##             del self.tag1
##             del self.tag2
##             del self.tag1Node
##             del self.tag2Node
##             del self.av
##             del self.avKeep
##         DirectFrame.destroy(self)

        self.headModel.delete()
        del self.headModel
        self.head.removeNode()
        del self.head
        DirectFrame.destroy(self)

        
