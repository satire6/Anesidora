"""
Defines Scene Graph tree UI
"""
from direct.leveleditor.SceneGraphUIBase import *
        
class SceneGraphUI(SceneGraphUIBase):
    def __init__(self, parent, editor):
        SceneGraphUIBase.__init__(self, parent, editor)

    def populateExtraMenu(self):
        menuitem = self.menu.Append(-1, 'Add Group')
        self.Bind(wx.EVT_MENU, self.onAddGroup, menuitem)
        menuitem = self.menu.Append(-1, 'Add Vis Group')
        self.Bind(wx.EVT_MENU, self.onAddVisGroup, menuitem)

    def onAddGroup(self, evt=None):
        if self.currObj is None:
            return

        self.editor.objectMgr.addNewObject('__group__',
                                           parent = self.currObj[OG.OBJ_NP],
                                           fSelectObject = False)

    def onAddVisGroup(self, evt=None):
        if self.currObj is None:
            return

        self.editor.objectMgr.addNewObject('__vis_group__',
                                           parent = self.currObj[OG.OBJ_NP],
                                           fSelectObject = False)
