from Quests import *
from direct.showbase.TkGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.tkwidgets.Tree import *
import Pmw
from Pmw import *
from direct.showbase.TkGlobal import *
from direct.showbase import TkGlobal
from direct.gui.DirectGui import DGG

DEFAULT_MENU_ITEMS = []

class QuestExplorer(Pmw.MegaWidget, DirectObject):
    "Graphical display of a scene graph"
    def __init__(self, parent = None, quest = 0, **kw):
        # Define the megawidget options.
        optiondefs = (
            ('menuItems',   [],   Pmw.INITOPT),
            )
        self.defineoptions(kw, optiondefs)
 
        # Initialise superclass
        Pmw.MegaWidget.__init__(self, parent)
        
        # Initialize some class variables
        self.quest = quest

        # Create the components.
        
        # Setup up container
        interior = self.interior()
        interior.configure(relief = "groove", borderwidth = 2)
        
        # Create a label and an entry
        self._scrolledCanvas = self.createcomponent(
            'scrolledCanvas',
            (), None,
            Pmw.ScrolledCanvas, (interior,),
            hull_width = 200, hull_height = 300,
            usehullsize = 1)
        self._canvas = self._scrolledCanvas.component('canvas')
        self._canvas['scrollregion'] = ('0i', '0i', '2i', '4i')
        self._scrolledCanvas.resizescrollregion()
        self._scrolledCanvas.pack(padx = 3, pady = 3, expand=1)
        
        self._canvas.bind('<ButtonPress-2>', self.mouse2Down)
        self._canvas.bind('<B2-Motion>', self.mouse2Motion)
        self._canvas.bind('<Configure>',
                          lambda e, sc = self._scrolledCanvas:
                          sc.resizescrollregion())
        self.interior().bind('<Destroy>', self.onDestroy)
        
        # Create the contents
        self._treeItem = QuestExplorerItem(self.quest)

        self._node = TreeNode(self._canvas, None, self._treeItem,
                              DEFAULT_MENU_ITEMS + self['menuItems'])
        self._node.expand()

        # Check keywords and initialise options based on input values.
        self.initialiseoptions(QuestExplorer)

    def update(self):
        """ Refresh scene graph explorer """
        self._node.update()

    def mouse2Down(self, event):
        self._width = 1.0 * self._canvas.winfo_width()
        self._height = 1.0 * self._canvas.winfo_height()
        xview = self._canvas.xview()
        yview = self._canvas.yview()        
        self._left = xview[0]
        self._top = yview[0]
        self._dxview = xview[1] - xview[0]
        self._dyview = yview[1] - yview[0]
        self._2lx = event.x
        self._2ly = event.y

    def mouse2Motion(self,event):
        newx = self._left - ((event.x - self._2lx)/self._width) * self._dxview
        self._canvas.xview_moveto(newx)
        newy = self._top - ((event.y - self._2ly)/self._height) * self._dyview
        self._canvas.yview_moveto(newy)
        self._2lx = event.x
        self._2ly = event.y
        self._left = self._canvas.xview()[0]
        self._top = self._canvas.yview()[0]

    def onDestroy(self, event):
        pass

class QuestExplorerItem(TreeItem):

    """Example TreeItem subclass -- browse the file system."""
    maxTier = max(Tier2QuestsDict.keys())
    def __init__(self, quest):
        self.quest = quest

    def GetText(self):
        if self.quest == -1:
            return "Quest Root"
        elif self.quest <= self.maxTier:
            if self.quest < DD_TIER:
                tierName = 'TT_TIER'
            elif self.quest < DG_TIER:
                tierName = 'DD_TIER'                
            elif self.quest < MM_TIER:
                tierName = 'DG_TIER'                
            elif self.quest < BR_TIER:
                tierName = 'MM_TIER'                
            elif self.quest < DL_TIER:
                tierName = 'BR_TIER'
            else:
                tierName = 'DL_TIER'
            return "%s: %d" % (tierName, self.quest)
        else:
            id = self.quest
            try:
                questEntry = QuestDict.get(id)
                if questEntry:
                    questDesc = questEntry[QuestDictDescIndex]
                    # Instantiate a quest object from this class
                    questClass = questDesc[0]
                    quest = questClass(id, questDesc[1:])
                    # Extract other details
                    toNpcId = questEntry[QuestDictToNpcIndex]
                    if ((toNpcId == Any) or
                        (toNpcId == NA) or
                        (toNpcId == Same)):
                        toNpcId = None
                    # Generate dialog
                    dialog = fillInQuestNames(quest.getDefaultQuestDialog(),
                                              avName = 'Questy Lazar',
                                              fromNpcId = 1000,
                                              toNpcId = toNpcId)
                    # Strip out end of page symbols
                    dialog = dialog.replace("\a", "")
                else:
                    dialog = 'Quest Entry not found'
            except:
                dialog = getQuest(self.quest).getPosterString()
            # Tack on reward string
            nextQuest = QuestDict[id][QuestDictNextQuestIndex]
            if nextQuest == NA:
                reward = getReward(getFinalRewardId(id, fAll = 1))
                if reward:
                    rewardString = " %s" % reward.getPosterString()
                else:
                    rewardString = ' - Just for fun!'
            else:
                rewardString = ""
            return "%d: %s%s" % (id, dialog, rewardString)

    def GetTextFg(self):
        if self.quest <= self.maxTier:
            return "black"
        else:
            # See if this is a required task
            id = self.quest
            reward = getReward(getFinalRewardId(id, fAll = 1))
            if reward:
                return "red"
            else:
                return "black"

    def GetKey(self):
        return self.quest

    def IsEditable(self):
        # All nodes' names can be edited nowadays.
        return 1

    def SetText(self, text):
        pass

    def GetIconName(self):
        return "sphere2" # XXX wish there was a "file" icon

    def IsExpandable(self):
        if self.quest <= self.maxTier:
            return 1
        nextQuest = QuestDict[self.quest][QuestDictNextQuestIndex]
        if nextQuest == NA:
            return 0
        else:
            return 1

    def GetSubList(self):
        if self.quest == -1:
            nextQuests = Tier2QuestsDict.keys()
        elif self.quest <= self.maxTier:
            nextQuests = getStartingQuests(self.quest)
        else:
            nextQuests = list(nextQuestList(QuestDict[self.quest][QuestDictNextQuestIndex]))
        if nextQuests == None:
            return []
        else:
            return map(QuestExplorerItem, nextQuests)

def exploreQuests(quest = -1):
    # Pop open a hierarchical viewer to explore quest system
    import QuestExplorer
    tl = TkGlobal.Toplevel()
    tl.title('Explore Quests')
    qe = QuestExplorer.QuestExplorer(parent = tl, quest = quest)
    qe.pack(expand = 1, fill = 'both')
    return qe
