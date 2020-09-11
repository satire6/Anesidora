import wx
from wx.lib.scrolledpanel import ScrolledPanel

class VisGroupsUI(wx.Dialog):
    def __init__(self, parent, id, title, editor, visGroups):
        wx.Dialog.__init__(self, parent, id, title, size=(200, 240))

        self.parent = parent
        self.editor = editor
        self.visGroups = visGroups

        self.visGroupNames = map(lambda pair: pair[1].getName(),
                                 self.visGroups)        

        # Initialize dictionary of visibility relationships
        self.visDict = {}
        # Group we are currently setting visGroups for
        self.target = None
        # Flag to enable/disable toggleVisGroup command
        self.fCommand = 1        
        self.createInterface()
        self.Bind(wx.EVT_CLOSE, self.onQuit)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def createInterface(self):
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(panel, label='Current Vis Group : '))
        currVisGroupCombo = wx.Choice(panel, -1, choices=self.visGroupNames)
        currVisGroupCombo.Bind(wx.EVT_CHOICE, self.selectVisGroup)
        hbox.Add(currVisGroupCombo)
        panel.SetSizer(hbox)

        scrolledPanel = ScrolledPanel(self)
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        self.checkBoxes = []
        for groupInfo in self.visGroups:
            nodePath = groupInfo[0]
            group = groupInfo[1]
            name = group.getName()
            checkBox = wx.CheckBox(scrolledPanel, -1, name)
            checkBox.Bind(wx.EVT_CHECKBOX, lambda p0=None, p1=name: self.toggleVisGroup(p0, p1))
            self.checkBoxes.append(checkBox)
            vbox2.Add(checkBox)
            # Assemble list of groups visible from this group
            visible = []
            for i in range(group.getNumVisibles()):
                visible.append(group.getVisibleName(i))
            visible.sort()
            self.visDict[name] = [nodePath, group, visible]

        scrolledPanel.SetSizer(vbox2)
        scrolledPanel.SetupScrolling(scroll_y = True, rate_y = 20)

        buttonPanel = wx.Panel(self, -1)
        self.showOptionBox = wx.RadioBox(buttonPanel, -1, "", choices=['Show All', 'Show Target'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.showOptionBox.Bind(wx.EVT_RADIOBOX, self.refreshVisibility)
        vbox.Add(panel)
        vbox.Add(scrolledPanel, 1, wx.EXPAND, 0)
        vbox.Add(buttonPanel)
        self.SetSizer(vbox)

    def selectVisGroup(self, evt):
        target = evt.GetString()
        print 'Setting vis options for group:', target
        # Record current target
        oldTarget = self.target
        # Record new target
        self.target = target
        # Deselect buttons from old target (first deactivating command)
        self.fCommand = 0
        if oldTarget:
            visList = self.visDict[oldTarget][2]
            for group in visList:
                self.checkBoxes[self.visGroupNames.index(group)].SetValue(False)
        # Now set buttons to reflect state of new target
        visList = self.visDict[target][2]
        for group in visList:
            self.checkBoxes[self.visGroupNames.index(group)].SetValue(True)
        # Reactivate command
        self.fCommand = 1
        # Update scene
        self.refreshVisibility()

    def toggleVisGroup(self, evt, groupName):
        if self.fCommand:
            state = evt.GetInt()
            targetInfo = self.visDict[self.target]
            targetNP = targetInfo[0]
            target = targetInfo[1]
            visList = targetInfo[2]
            groupNP = self.visDict[groupName][0]
            group = self.visDict[groupName][1]
            # MRM: Add change in visibility here
            # Show all vs. show active
            if state == 1:
                print 'Vis Group:', self.target, 'adding group:', groupName
                if groupName not in visList:
                    visList.append(groupName)
                    if hasattr(targetNP, 'addVisible'):
                        targetNP.addVisible(groupName)
                    else:
                        target.addVisible(groupName)
                    # Update vis and color
                    groupNP.show()
                    groupNP.setColor(1, 0, 0, 1)
            else:
                print 'Vis Group:', self.target, 'removing group:', groupName
                if groupName in visList:
                    visList.remove(groupName)
                    if hasattr(targetNP, 'removeVisible'):
                        targetNP.removeVisible(groupName)
                    else:
                        target.removeVisible(groupName)
                    # Update vis and color
                    if self.showOptionBox.GetStringSelection() == 'Show Target':
                        groupNP.hide()
                    groupNP.clearColor()

    def refreshVisibility(self, evt=None):
        # Get current visibility list for target
        targetInfo = self.visDict[self.target]
        visList = targetInfo[2]
        for key in self.visDict.keys():
            groupNP = self.visDict[key][0]
            if key in visList:
                groupNP.show()
                if key == self.target:
                    groupNP.setColor(0, 1, 0, 1)
                else:
                    groupNP.setColor(1, 0, 0, 1)
            else:
                if self.showOptionBox.GetStringSelection() == 'Show All':
                    groupNP.show()
                else:
                    groupNP.hide()
                groupNP.clearColor()

    def onQuit(self, evt):
        self.Destroy()
        
    def onDestroy(self, evt):
        # Get current visibility list for target
        targetInfo = self.visDict[self.target]
        visList = targetInfo[2]
        for key in self.visDict.keys():
            groupNP = self.visDict[key][0]        
            groupNP.show()
            groupNP.clearColor()

        self.editor.ui.visGroupsUI = None
        #self.Destroy()
