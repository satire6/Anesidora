"""EmotePage module: contains the EmotePage class"""

from toontown.toonbase import ToontownGlobals
import ShtikerPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon

PICKER_START_POS = (-0.555, 0, 0)
MAX_FRAMES = 15

emoteAnimDict = {'Jump':  'jump',
                 'Happy': 'Happy',
                 'Sad':   'Sad',
                 'Sleepy':'Sleep',
                 'Dance': 'victory'}

class EmoteFrame(DirectFrame):
    def __init__(self, emoteName = "?"):
        DirectFrame.__init__(self, relief = None)
        bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
        self.normalTextColor = (0.3,0.25,0.2,1)
        self.name = emoteName
        self.frame = DirectFrame(
            parent = self,
            relief = None,
            image = bookModel.find("**/paper_note"),
            image_scale = (0.8,0.9,0.9),
            text = self.name,
            text_pos = (0,-0.34),
            text_fg = self.normalTextColor,
            text_scale = 0.15,
            )
        self.question = DirectLabel(
            parent = self.frame,
            relief = None,
            pos = (0,0,-0.15),
            text = "?",
            text_scale = 0.4,
            text_pos = (0,0),
            text_fg = (0.3,0.25,0.2,0.1),
            )
        self.toon = None
        if self.name != '?':
            self.makeToon()
        bookModel.removeNode()

    def updateEmote(self, emoteName):
        self.name = emoteName
        self.frame['text'] = self.name
        self.frame.setText()
        self.makeToon()
        self.question.hide()
        
    def makeToon(self):
        if self.toon != None:
            del self.toon
            
        self.toon = Toon.Toon()
        self.toon.setDNA(base.localAvatar.getStyle())
        self.toon.getGeomNode().setDepthWrite(1)
        self.toon.getGeomNode().setDepthTest(1)
        # Conserve polygons
        self.toon.useLOD(500)
        self.toon.reparentTo(self.frame)
        self.toon.setPosHprScale(0,10,-0.25, 210,0,0, 0.15,0.15,0.15)
        self.toon.loop('neutral')

        try:
            anim = emoteAnimDict[self.name]
        except:
            print "we didnt get the right animation"
            anim = 'neutral'
            
        #self.toon.pose(anim, self.toon.getNumFrames(anim)/2)
        self.toon.animFSM.request(anim)
        
    def play(self, trackId):
        if ((not base.launcher) or
            (base.launcher and base.launcher.getPhaseComplete(5))):
            anim = emoteAnimDict[self.emoteName]
        else:
            anim = 'neutral'
        if self.toon == None:
            self.makeToon()
        self.toon.play(anim)

    def setTrained(self, trackId):
        # make sure this frame has a toon
        if self.toon == None:
            self.makeToon()
        # Make sure we are downloaded
        # TODO: show something better here or download these animations sooner
        if ((not base.launcher) or
            (base.launcher and base.launcher.getPhaseComplete(5))):
            anim = emoteAnimDict[self.emoteName]
        else:
            anim = 'neutral'
        self.toon.pose(anim, 0)
        self.toon.show()
        self.question.hide()
        self.frame['image_color'] = Vec4(1,1,1,1)

    def setUntrained(self, trackId):
        if self.toon:
            self.toon.hide()
        self.question.show()
        self.frame['image_color'] = Vec4(0.8,0.8,0.8,0.5)
        
class EmotePage(ShtikerPage.ShtikerPage):
    """EmotePage class: keeps track of which emotes a toon can use"""

    # special methods
    def __init__(self):
        """__init__(self)
        EmotePage constructor: create the emote page
        """
        ShtikerPage.ShtikerPage.__init__(self)
        self.emotes = []
        self.emoteFrames = []
        self.avatar = None
        self.state = DGG.NORMAL
        
    def setAvatar(self, av):
        self.avatar = av

    def getAvatar(self):
        return self.avatar
    
    def placeFrames(self):
        rowPos = [0.26, -0.09, -0.44]
        colPos = [-0.70, -0.35, 0, 0.35, 0.70]
        for index in range(1, MAX_FRAMES+1):
            frame = self.emoteFrames[index-1]
            col = (index - 1) % 5
            row = (index - 1) / 5
            frame.setPos(colPos[col], 0, rowPos[row])
            frame.setScale(0.4)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        # page title
        self.title = DirectLabel(
            parent = self,
            relief = None,
            text = TTLocalizer.EmotePageTitle,
            text_scale = 0.12,
            pos = (0,0,0.6),
            )
        # Count up from 1
        for index in range(1, MAX_FRAMES+1):
            if index < len(self.emotes):
                frame = EmoteFrame(self.emotes[index-1])
            else:
                frame = EmoteFrame()
            frame.reparentTo(self)
            self.emoteFrames.append(frame)
        self.placeFrames()

        self.updatePage()

    def unload(self):
        del self.title
        del self.emoteFrames
        
        ShtikerPage.ShtikerPage.unload(self)

    def updatePage(self):
        # the emote list has changed, update the picker
        newEmotes = base.localAvatar.emotes

        # Add new buttons
        for i in range(len(newEmotes)):
            emote = newEmotes[i]
            self.emotes.append(emote)
            self.emoteFrames[i].updateEmote(emote)

    def makeEmoteButton(self, emote):
        return DirectButton(
            parent = self, 
            relief = None,
            text = emote,
            text_scale = 0.08,
            text_align = TextNode.ALeft,
            text1_bg = Vec4(1,1,0,1),
            text2_bg = Vec4(0.5,0.9,1,1),
            text3_fg = Vec4(0.4,0.8,0.4,1),
            command = self.showEmotePanel,
            extraArgs = [emote],
            pos = (-0.25+.05*len(self.emotes), 0, -0.25),
            )

    def showEmotePanel(self):
        # pop up a little doober
        self.emotePanel.show()
        
    def hideEmotePanel(self):
        # hide the little doober        
        self.emotePanel.hide()

